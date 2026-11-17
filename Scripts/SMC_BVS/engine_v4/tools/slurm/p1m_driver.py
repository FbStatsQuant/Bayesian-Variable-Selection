#!/usr/bin/env python3
"""p1m_driver.py -- P1M Slurm driver, DRY-RUN ONLY (WP5; ENGINEERING_SPEC §1, §3, §6; PROTOCOL §4, §7; NOTS_FACTS).

Writes, for one batch, everything the manager deploys to NOTS `~/SMC_Engineering_Department/scripts/<batch>/` and runs:
  stage_setup.sbatch      job ARRAY over fits (gen -> prep -> setup)
  stage_calibrate.sbatch  job ARRAY over fits, --dependency=aftercorr on the setup array (task i waits for task i)
  stage_islands.sbatch    one ARRAY of R' tasks per fit, --dependency=afterok:<calibrate>_<i>  (replicates pipeline:
                          fit i's islands start as soon as fit i's calibration ends, while fit i+1 still calibrates)
  stage_merge.sbatch      one task per fit, afterok on that fit's island array
  stage_eval.sbatch       one task per fit, afterok on its merge (eval, then post)
  manifests/<run_id>/<command>.json   job-manifest templates (INTERFACES §5.3); inputs filled at run time by
                          p1m_manifest.py from the previous stage's <out>.json records
  run_manifests/<run_id>.json         ONE manifest per run (PROTOCOL §4), copied into the run dir before the first output
  submit.sh               the manager's submission script (sbatch --parsable, ids logged); NEVER run by this driver
  stage_pilot.sbatch      (plan key "pilot" only; WP7 O5) job ARRAY over fits, aftercorr on the setup array: the
                          calibration pilot island alone (v4_pilot_island; H-11's 10^6 calibration pilot), cost record
                          in <run>/cost_pilot/
  submit_pilot.sh         (plan key "pilot" only) submits setup -> pilot and nothing else; its own worst case
  stage_isa_check.sbatch  (plan key "isa_check" only; D-32) one task per fit, afterok on its island array: island r re-run
                          with the PORTABLE build (bin/smcbvs4_isa_check) and compared with the island_isa run
                          (p1m_stage_cost.py isa: meta.output_hash + every non-meta section hash); fails if they differ
  ledger_row.md           the LEDGER.md row (worst case = sum of allocated CPUs x time limit, billed core-h)
  SHA256SUMS              hashes of every generated file (submit.sh verifies them first)
  plan.resolved.json      the plan with every default filled in

Usage:  p1m_driver.py --plan plan.json --out <dir> [--dept /home/fb31/SMC_Engineering_Department]
There is no submit mode. The driver never calls sbatch, squeue, sacct or ssh.

Rules enforced: --constraint=sapphirerapids; account/partition commons, qos nots_commons; no task above the QOS wall
(24 h) and none above `max_task_hours` of the plan (default 2 h, §0-v2.5); at most 150 queued tasks per batch; worst
case <= the plan's `core_h_cap` when given; all paths inside the department folder (outputs, --output and TMPDIR through
the `scratch` link); job arrays only.
"""
import argparse
import copy
import datetime
import hashlib
import json
import math
import os
import re
import stat
import sys

DEPT_DEFAULT = "/home/fb31/SMC_Engineering_Department"
QOS_WALL_H = 24.0
TASK_CAP = 150
CPU_CAP = 1536
STAGES = ["setup", "calibrate", "islands", "merge", "eval"]

# PLANNING VALUES (ENGINEERING_SPEC §0-v2.5, §2, §7; NOTS_FACTS: island default 64 CPUs + 32 GB). Gate G0 / the 10^4-10^5
# pilots replace them; every plan may override any entry. cpus = allocated (billed) CPUs = hardware threads.
DEFAULT_RES = {
    "1e4": {"setup": {"cpus": 8, "mem": "8G", "time": "00:20:00"},
            "calibrate": {"cpus": 16, "mem": "8G", "time": "00:45:00"},
            "islands": {"cpus": 16, "mem": "4G", "time": "00:15:00"},
            "merge": {"cpus": 8, "mem": "4G", "time": "00:15:00"},
            "eval": {"cpus": 4, "mem": "8G", "time": "00:20:00"}},
    "1e5": {"setup": {"cpus": 32, "mem": "16G", "time": "00:30:00"},
            "calibrate": {"cpus": 64, "mem": "16G", "time": "01:30:00"},
            "islands": {"cpus": 64, "mem": "8G", "time": "01:00:00"},
            "merge": {"cpus": 16, "mem": "8G", "time": "00:30:00"},
            "eval": {"cpus": 8, "mem": "16G", "time": "00:45:00"}},
    "1e6": {"setup": {"cpus": 96, "mem": "48G", "time": "01:30:00"},   # WP2 --count-only peak: IND n = 1,000 ≈ 22.7 GB (D-31)
            # P5 re-size (manager 11-17) from WP3's StartView plans, results/WP3_PLANS_1e6.md (--mem-budget = 90% of the request):
            # calibrate task (N-1 rule + SetupView) 71.9 / 81.2 GiB at n = 200 (G 64 / 256), up to 97.7 GiB at n = 1,000 IND -> 128G.
            "calibrate": {"cpus": 96, "mem": "128G", "time": "02:00:00"},
            # final island 24.5 / 33.8 GiB at n = 200, up to 46.8 GiB at n = 1,000 IND G 256 -> 64G (two per 257 GB SPR node).
            "islands": {"cpus": 96, "mem": "64G", "time": "02:00:00"},
            # merge task 43.7 GiB at n = 200, 58.5 GiB at n = 1,000 IND (PR45 INFO-3: 2.5 x setup.bin before StartView) -> 80G.
            "merge": {"cpus": 32, "mem": "80G", "time": "01:00:00"},
            "eval": {"cpus": 8, "mem": "16G", "time": "01:00:00"}},
}


# D-32: island ISAs with FMA (class A has the same bits in all of them: x86-64-v3 = x86-64-v4, MEASURED on Owls)
FMA_ISAS = {"x86-64-v3", "x86-64-v4", "sapphirerapids", "icelake-server", "cascadelake", "skylake-avx512"}
# D-32 (3): the bit-form check of stage_isa_check: one particle-major bit-form island (the theory path) on the
# benchmark's AR(0.6) data, run by the plan-ISA, comparison and portable builds; the output hashes must be equal
BITFORM_ARGS = "island 20000 64 $OMP_NUM_THREADS bit pm 1 128 geo:4 1 1"


class PlanError(Exception):
    pass


def rung(p):
    return "1e4" if p <= 2e4 else ("1e5" if p <= 2e5 else "1e6")


def hours(t):
    m = re.fullmatch(r"(?:(\d+)-)?(\d+):(\d\d):(\d\d)", t)
    if not m:
        raise PlanError("bad time limit %r (use [D-]HH:MM:SS)" % t)
    d, h, mi, s = m.groups()
    return (int(d or 0) * 24 + int(h)) + int(mi) / 60.0 + int(s) / 3600.0


def safe_id(s, what):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}", s):
        raise PlanError("%s %r: use letters, digits, _ . - (max 64)" % (what, s))
    return s


def resolve(plan):
    """Fill defaults and validate. Returns the resolved plan (a new dict)."""
    P = copy.deepcopy(plan)
    safe_id(P.get("batch", ""), "batch")
    P.setdefault("mode", "V")
    if P["mode"] not in ("compat", "law", "V"):
        raise PlanError("mode must be compat, law or V")
    P.setdefault("binary", "bin/smcbvs4")          # relative to scripts/<batch>/ (deployed with the frozen code)
    P.setdefault("code_commit", "UNSET")
    P.setdefault("max_task_hours", 2.0)
    P.setdefault("eval", {"threads": None, "post": True, "n_draws": 10000, "n_x": 4000, "n_test": 10000})
    P.setdefault("island_throttle", None)           # optional %k on each island array
    P.setdefault("island_isa", "")                  # WP7 O5: -DV4_ISLAND_ISA for build.sh ("" = the portable default)
    if P["island_isa"] and not re.fullmatch(r"[A-Za-z0-9_.-]+", P["island_isa"]):
        raise PlanError("island_isa must be a -march name such as sapphirerapids")
    # D-32 (1): class-A values (V mode) use a true FMA in every FMA build and a*b + c without one (amath.h fma8), so a
    # V plan needs an island ISA with FMA, at least x86-64-v3; one fit = one FMA family (one binary for every stage)
    v_plan = P["mode"] == "V" or any(f.get("mode", P["mode"]) == "V" for f in P.get("fits") or [])
    if v_plan and P["island_isa"] not in FMA_ISAS:
        raise PlanError("a V-mode plan needs island_isa with FMA (one of %s; D-32); got %r" % (", ".join(sorted(FMA_ISAS)), P["island_isa"]))
    # review PR55 MAJOR: a pilot-only batch (P7) generates setup + pilot and nothing that could launch the fit; its
    # worst case, cap and ledger row are the pilot's (the real fit later gets its own plan)
    P.setdefault("pilot_only", False)
    if P["pilot_only"] and P.get("pilot") is None:
        raise PlanError("pilot_only needs a pilot section")
    if P["pilot_only"] and P.get("isa_check") is not None:
        raise PlanError("pilot_only batches have no islands: remove isa_check")
    if P.get("pilot") is not None:                  # WP7 O5: {"cpus", "mem", "time", "with_ledger"} of the pilot task
        pl = P["pilot"]
        # memory (WP3 11-17): the calibration island plans 54.5 GiB at G 256 at 10^6 before Gram rows (+4.9) and the setup
        # inputs (4-14 GB), so 64G is too small: default 128G (one 257 GB SPR node holds two such tasks), or sized from a
        # `smcbvs4 calibrate --plan-only 1` record: island_plan.total (+ setup_inputs_gb when the record was made from
        # sizes only) x 1.15, / 0.9 because the task's --mem-budget is 90% of the allocation; refused above 240G
        pl.setdefault("mem", "128G")
        mfp = pl.get("mem_from_plan")
        if mfp is not None:
            try:
                with open(mfp["record"]) as fh:
                    rec = json.load(fh)
            except (OSError, ValueError, KeyError, TypeError) as e:
                raise PlanError("pilot.mem_from_plan: cannot read the plan record (%s)" % e)
            ip = rec.get("island_plan")
            if not ip or "total" not in ip:
                raise PlanError("pilot.mem_from_plan: %s has no island_plan.total (calibrate --plan-only 1 with WP3's island plan)" % mfp["record"])
            extra = 0.0 if ip.get("setup_inputs") else float(mfp.get("setup_inputs_gb", 14)) * 1e9
            need = (float(ip["total"]) + extra) * 1.15 / 0.9
            gib = int(math.ceil(need / 2 ** 30 / 8.0) * 8)
            if gib > 240:
                raise PlanError("pilot.mem_from_plan: %d G needed (> 240G of a 257 GB SPR node)" % gib)
            pl["mem"] = "%dG" % gib
            pl["mem_basis"] = {"island_plan_total": ip["total"], "setup_inputs_added": extra, "factor": "x1.15 / 0.9", "record": mfp["record"]}
        for k in ("cpus", "mem", "time"):
            if k not in pl:
                raise PlanError("pilot: missing %r" % k)
        if not (1 <= int(pl["cpus"]) <= 192) or not re.fullmatch(r"\d+[MG]", pl["mem"]):
            raise PlanError("pilot: cpus in 1..192 and mem like 64G")
        h = hours(pl["time"])
        if h > QOS_WALL_H or h > P["max_task_hours"] + 1e-9:
            raise PlanError("pilot: %s exceeds max_task_hours = %.2f" % (pl["time"], P["max_task_hours"]))
        pl.setdefault("with_ledger", 1)
    if P.get("isa_check") is not None:              # D-32: T2 across island ISAs (one island re-run with a comparison build)
        if not P["island_isa"]:
            raise PlanError("isa_check needs island_isa (the comparison build is the other side)")
        r = P["isa_check"].get("island")
        if not isinstance(r, int) or r < 1:
            raise PlanError("isa_check: island must be an integer >= 1")
        # the comparison build's island ISA: class A uses a true FMA when the build has one (amath.h fma8), so its bits
        # are those of every FMA build (x86-64-v3 = AVX2 + FMA matched AVX-512 on Owls) and differ from a build without
        # FMA ("portable" = x86-64-v2) by design; the bit form (theory/compat) is ISA-free
        P["isa_check"].setdefault("against", "x86-64-v3")
        if P["isa_check"]["against"] not in FMA_ISAS:   # D-32 (3): the class-A comparison is within the FMA family
            raise PlanError("isa_check.against must be an FMA ISA (one of %s)" % ", ".join(sorted(FMA_ISAS)))
        if P["isa_check"]["against"] == P["island_isa"]:   # review PR55 m5: the same ISA makes the comparison vacuous
            raise PlanError("isa_check.against equals island_isa: the class-A comparison would compare a build with itself")
        # its own time limit (review PR55 m5): one island re-run, two `info --meta` reads, three bit-form islands
        P["isa_check"].setdefault("time", "00:40:00")
        h = hours(P["isa_check"]["time"])
        if h > QOS_WALL_H or h > P["max_task_hours"] + 1e-9:
            raise PlanError("isa_check.time %s exceeds max_task_hours = %.2f" % (P["isa_check"]["time"], P["max_task_hours"]))
    if not P.get("fits"):
        raise PlanError("plan has no fits")
    seen = set()
    for i, f in enumerate(P["fits"]):
        for k in ("run_id", "design", "p", "n", "signal", "data_seed", "seed"):
            if k not in f:
                raise PlanError("fit %d: missing %r" % (i, k))
        safe_id(f["run_id"], "run_id")
        if f["run_id"] in seen:
            raise PlanError("duplicate run_id %s" % f["run_id"])
        seen.add(f["run_id"])
        if f["design"] not in ("IND", "AR", "BLK", "ADJ-OPP", "NULL"):
            raise PlanError("fit %s: design %s is not generated by WP1 gen (IND, AR, BLK, ADJ-OPP, NULL)" % (f["run_id"], f["design"]))
        for k in ("seed", "data_seed"):
            if not (isinstance(f[k], int) and 1 <= f[k] <= 2 ** 31 - 1):
                raise PlanError("fit %s: %s must be an integer in [1, 2^31-1]" % (f["run_id"], k))
        f.setdefault("Rp", 16)
        f.setdefault("N", 2500)
        f.setdefault("mode", P["mode"])
        res = copy.deepcopy(DEFAULT_RES[rung(f["p"])])
        for st, over in (P.get("resources") or {}).items():
            if st not in res:
                raise PlanError("unknown stage %r in resources" % st)
            res[st].update(over)
        for st, over in (f.get("resources") or {}).items():
            res[st].update(over)
        for st, r in res.items():
            h = hours(r["time"])
            if h > QOS_WALL_H:
                raise PlanError("fit %s stage %s: %s exceeds the QOS wall of 24 h" % (f["run_id"], st, r["time"]))
            if h > P["max_task_hours"] + 1e-9:
                raise PlanError("fit %s stage %s: %s exceeds max_task_hours = %.2f (§0-v2.5: no job longer than 2 h)"
                                % (f["run_id"], st, r["time"], P["max_task_hours"]))
            if not (1 <= int(r["cpus"]) <= 192):
                raise PlanError("fit %s stage %s: cpus must be in 1..192 (one SPR node)" % (f["run_id"], st))
            if not re.fullmatch(r"\d+[MG]", r["mem"]):
                raise PlanError("fit %s stage %s: mem like 32G" % (f["run_id"], st))
        f["resources"] = res
    F = len(P["fits"])
    if P.get("isa_check") is not None:
        for f in P["fits"]:
            if P["isa_check"]["island"] > f["Rp"]:
                raise PlanError("isa_check: island %d > Rp of fit %s" % (P["isa_check"]["island"], f["run_id"]))
    tasks = sum(3 + f["Rp"] for f in P["fits"]) + F    # setup + calibrate + Rp islands + merge + eval
    if P.get("isa_check") is not None:
        tasks += F                                       # + one island re-run per fit with the comparison build (D-32)
    if P["pilot_only"]:
        tasks = 2 * F                                    # setup + pilot
    P["n_tasks"] = tasks
    if tasks > TASK_CAP:
        raise PlanError("batch has %d tasks > the 150-task cap: split it into waves (fewer fits per batch)" % tasks)
    wc = 0.0
    for f in P["fits"]:
        for st in STAGES:
            r = f["resources"][st]
            n = f["Rp"] if st == "islands" else 1
            wc += n * int(r["cpus"]) * hours(r["time"])
        if P.get("isa_check") is not None:   # the comparison-build island re-run: one task at the islands' CPUs, its own limit
            wc += int(f["resources"]["islands"]["cpus"]) * hours(P["isa_check"]["time"])
    if P.get("pilot") is not None:                  # submit_pilot.sh: setup + pilot per fit
        P["worst_case_pilot_core_h"] = round(sum(int(f["resources"]["setup"]["cpus"]) * hours(f["resources"]["setup"]["time"])
                                                 + int(P["pilot"]["cpus"]) * hours(P["pilot"]["time"]) for f in P["fits"]), 1)
    if P["pilot_only"]:
        wc = P["worst_case_pilot_core_h"]
    P["worst_case_core_h"] = round(wc, 1)
    cap = P.get("core_h_cap")
    if cap is not None and wc > cap + 1e-9:
        raise PlanError("worst case %.1f billed core-h exceeds the plan's core_h_cap %.1f" % (wc, cap))
    peak = max(f["Rp"] * int(f["resources"]["islands"]["cpus"]) for f in P["fits"])
    if peak > CPU_CAP:
        raise PlanError("one fit's island array needs %d CPUs > the 1,536-CPU user cap" % peak)
    return P


HEADER = """#!/usr/bin/env bash
# {name} -- P1M batch {batch}, stage {stage}. GENERATED by tools/slurm/p1m_driver.py (dry run); do not edit by hand.
# Submitted only by {submitter} (the manager's). Worst case of this file: {wc:.1f} billed core-h.
#SBATCH --job-name=p1m_{batch}_{stage}
#SBATCH --account=commons
#SBATCH --partition=commons
#SBATCH --qos=nots_commons
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task={cpus}
#SBATCH --mem={mem}
#SBATCH --time={time}
#SBATCH --constraint=sapphirerapids
#SBATCH --export=NONE
#SBATCH --no-requeue
#SBATCH --kill-on-invalid-dep=yes
#SBATCH --output={dept}/scratch/slurm_out/%x_%A_%a.out
#SBATCH --error={dept}/scratch/slurm_out/%x_%A_%a.err
set -euo pipefail
DEPT={dept}
SCR=$DEPT/scripts/{batch}
BIN=$SCR/{binary}
export TMPDIR=$DEPT/scratch/tmp/${{SLURM_JOB_ID}}
mkdir -p "$TMPDIR"; trap 'rm -rf "$TMPDIR"' EXIT
export OMP_NUM_THREADS=${{SLURM_CPUS_PER_TASK}}
# INTERFACES §7: --mem-budget = the whole task's memory. 90% of the Slurm allocation leaves room for the runtime (PR37 re-check INFO-2).
MEMB=$(( ${{SLURM_MEM_PER_NODE:-0}} * 1048576 * 9 / 10 ))
set +u; source "$SCR/env.sh"; set -u          # NOTS modules (GCC 14.3.0 runtime); see env.sh
"""

# NOTS module environment (manager's lesson, 11-15: CMake 3.27.6 sits under GCCcore 13.2 and fails; use these)
ENV_SH = """# env.sh -- NOTS module environment for batch {batch} (GENERATED). Sourced by every stage and by build.sh.
# The Lmod init and `module` return non-zero internally, so under the callers' `set -euo pipefail` sourcing them exits the
# script silently (T5 build, 11-17). Run them with errexit/nounset/pipefail off, restore the caller's options, then check.
__p1m_flags=$-; __p1m_pf=$(shopt -po pipefail); set +e +u +o pipefail   # $- (not $(set +o): a subshell drops errexit)
type module >/dev/null 2>&1 || source /etc/profile.d/modules.sh
module use /opt/apps/modules/Core
module purge
module load GCC/14.3.0 CMake/3.31.8
[[ $__p1m_flags == *e* ]] && set -e; [[ $__p1m_flags == *u* ]] && set -u; eval "$__p1m_pf"; unset __p1m_flags __p1m_pf
command -v g++ >/dev/null && [[ $(g++ -dumpfullversion) == 14.3.0 ]] || {{ echo "FATAL: env.sh: GCC 14.3.0 not loaded" >&2; exit 66; }}
"""

BUILD_SH = """#!/usr/bin/env bash
# build.sh -- build the frozen engine for batch {batch} into $SCR/bin (GENERATED). Run ON NOTS by the manager, after the
# frozen code (`git archive` of commit {commit}) is unpacked in $SCR/code. nice, 3 jobs (POLICIES §12).
set -euo pipefail
DEPT=$(realpath -m "${{P1M_DEPT:-{dept}}}")
in_dir() {{ local r; r=$(realpath -m "$2"); [[ $1 == "$r" || $1 == "$r"/* ]]; }}
in_dir "$DEPT" "$HOME/SMC_Engineering_Department" || {{ [[ -n ${{P1M_TEST_ROOT:-}} ]] && in_dir "$DEPT" "$P1M_TEST_ROOT"; }} || {{ echo "refusing: $DEPT is outside the department folder" >&2; exit 64; }}
SCR=$DEPT/scripts/{batch}
set +u; source "$SCR/env.sh"; set -u
B=$SCR/build; mkdir -p "$B" "$SCR/bin"
nice -n 19 cmake -S "$SCR/code/Scripts/SMC_BVS/engine_v4" -B "$B" -DCMAKE_BUILD_TYPE=Release -DV4_TESTS=OFF{isa} > "$B/cmake.log"
nice -n 19 make -C "$B" -j3 smcbvs4{pilot_target}{bench_target}
cp "$B/smcbvs4" "$SCR/bin/smcbvs4"
"$SCR/bin/smcbvs4" version
sha256sum "$SCR/bin/smcbvs4" | tee "$SCR/bin/smcbvs4.sha256"
{pilot_copy}{bench_copy}{portable}"""

FIT_TABLE = """# fit table: index (1-based) -> run_id
RUNS=({runs})
"""


def fit_selector(by_array):
    sel = "${SLURM_ARRAY_TASK_ID}" if by_array else "${1:?fit index}"
    return ("FIT=%s\nRUN_ID=${RUNS[$((FIT-1))]}\nRUN=$DEPT/scratch/runs/%s/$RUN_ID\nMAN=$SCR/manifests/$RUN_ID\n" % (sel, "{batch}"))


SKIP_IF_OUTCOME = ('if [[ -e $RUN/OUTCOME ]]; then echo "prep outcome $(cat "$RUN/OUTCOME"): nothing to do"; '
                   'printf \'{{"stage":"%s","run_id":"%s","skipped":"prep_outcome"}}\\n\' "{stage}" "$RUN_ID" >> "$DEPT/scratch/runs/{batch}/ends.jsonl"; exit 0; fi\n')


def stage_body(stage):
    """Command lines of WP1's CLI (src/cli/main.cpp): --out names the .bin, the record is <out>.json; --manifest merges
    `params` into the arguments and refuses to start when an `inputs` path has a different content hash."""
    fill = 'python3 "$SCR/p1m_manifest.py" fill --template "$MAN/{cmd}.json" --out "$RUN/manifests/{cmd}{suffix}.json"'
    run = '"$BIN" {cmd} --manifest "$RUN/manifests/{cmd}{suffix}.json"{extra} --out "$RUN/{out}" > "$RUN/log/{cmd}{suffix}.log" 2>&1\n'
    if stage == "setup":
        return ("mkdir -p \"$RUN/manifests\" \"$RUN/log\"\n"
                "[[ -e $RUN/run_manifest.json ]] || cp \"$SCR/run_manifests/$RUN_ID.json\" \"$RUN/run_manifest.json\"\n"
                + fill.format(cmd="gen", suffix="") + "\n"
                + run.format(cmd="gen", suffix="", extra=' --truth "$RUN/truth.json"', out="raw.bin")
                + fill.format(cmd="prep", suffix="") + "\n"
                # INTERFACES §7: prep exit 20 (no_predictors) / 21 (y_constant) are data outcomes: record, end the pipeline
                + "rc=0\n" + run.format(cmd="prep", suffix="", extra=' --in "$RUN/raw.bin"', out="data.bin").rstrip("\n") + " || rc=$?\n"
                + 'if [[ $rc == 20 || $rc == 21 ]]; then echo $([[ $rc == 20 ]] && echo no_predictors || echo y_constant) > "$RUN/OUTCOME"; exit 0; fi\n'
                + '[[ $rc == 0 ]] || exit $rc\n'
                + fill.format(cmd="setup", suffix="") + "\n"
                + run.format(cmd="setup", suffix="", extra=' --threads "$OMP_NUM_THREADS"', out="setup.bin"))
    if stage == "calibrate":
        return (fill.format(cmd="calibrate", suffix="") + "\n"
                # D-30 / WP7 O5: one per-step cost record per calibration island in $RUN/cost/
                + run.format(cmd="calibrate", suffix="", extra=' --threads "$OMP_NUM_THREADS" --mem-budget "$MEMB" --cost-dir "$RUN/cost"', out="calib.bin"))
    if stage == "islands":
        return ("R=${SLURM_ARRAY_TASK_ID}\n"
                + fill.format(cmd="island", suffix="_$R") + " --set params.id=$R\n"
                + run.format(cmd="island", suffix="_$R", extra=' --threads "$OMP_NUM_THREADS" --mem-budget "$MEMB"', out="island_$R.bin"))
    if stage == "merge":
        return (fill.format(cmd="merge", suffix="") + "\n"
                + run.format(cmd="merge", suffix="", extra=' --threads "$OMP_NUM_THREADS" --mem-budget "$MEMB"', out="fit.bin"))
    if stage == "eval":
        return ('if [[ -e $RUN/OUTCOME ]]; then printf \'{"status":"completed","command":"eval","fit_status":"prep_%s","prep_status":"%s","hpm":[]}\\n\' '
                '"$(cat "$RUN/OUTCOME")" "$(cat "$RUN/OUTCOME")" > "$RUN/eval.bin.json"; exit 0; fi\n'
                + fill.format(cmd="eval", suffix="") + "\n"
                + '"$BIN" eval --manifest "$RUN/manifests/eval.json" --fit "$RUN/fit.bin" --data "$RUN/data.bin" --truth "$RUN/truth.json" '
                '--threads "$OMP_NUM_THREADS" --n-draws "$NDRAWS" --n-x "$NX" --n-test "$NTEST" --out "$RUN/eval.bin" > "$RUN/log/eval.log" 2>&1\n'
                'if [[ $POST == 1 ]]; then\n'
                + "  " + fill.format(cmd="post", suffix="") + "\n"
                + '  "$BIN" post --manifest "$RUN/manifests/post.json" --fit "$RUN/fit.bin" --data "$RUN/data.bin" --threads "$OMP_NUM_THREADS" --out "$RUN/law.bin" > "$RUN/log/post.log" 2>&1\nfi\n')
    raise ValueError(stage)


def write(path, text, mode=0o644):
    tmp = path + ".tmp.%d" % os.getpid()
    with open(tmp, "w") as fh:
        fh.write(text)
        fh.flush()
        os.fsync(fh.fileno())
    os.chmod(tmp, mode)
    os.replace(tmp, path)


def generate(P, out, dept):
    batch = P["batch"]
    os.makedirs(out, exist_ok=True)
    for sub in ("manifests", "run_manifests"):
        os.makedirs(os.path.join(out, sub), exist_ok=True)
    runs = " ".join(f["run_id"] for f in P["fits"])
    files = []
    # one sbatch file per stage; per-fit resources must agree within a stage (one --cpus/--mem/--time per file)
    for st in (["setup"] if P["pilot_only"] else STAGES):
        rs = {json.dumps(f["resources"][st], sort_keys=True) for f in P["fits"]}
        if len(rs) != 1:
            raise PlanError("stage %s: all fits of one batch must share resources (split the batch by rung)" % st)
        r = P["fits"][0]["resources"][st]
        n_per_fit = P["fits"][0]["Rp"] if st == "islands" else 1
        wc = sum((f["Rp"] if st == "islands" else 1) * int(r["cpus"]) * hours(r["time"]) for f in P["fits"])
        name = "stage_%s.sbatch" % st
        txt = HEADER.format(name=name, batch=batch, stage=st, wc=wc, cpus=r["cpus"], mem=r["mem"], time=r["time"],
                            dept=dept, binary=P["binary"], submitter="submit_pilot.sh" if P["pilot_only"] else "submit.sh")
        txt += FIT_TABLE.format(runs=runs)
        txt += fit_selector(st in ("setup", "calibrate")).replace("{batch}", batch)
        if st == "eval":
            e = P["eval"]
            txt += "NDRAWS=%d\nNX=%d\nNTEST=%d\nPOST=%d\n" % (e.get("n_draws", 10000), e.get("n_x", 4000), e.get("n_test", 10000),
                                                           1 if e.get("post", True) else 0)
        txt += 'printf \'{"stage":"%s","run_id":"%%s","job":"%%s","task":"%%s","host":"%%s","start":"%%s"}\\n\' "$RUN_ID" "${SLURM_JOB_ID}" "${SLURM_ARRAY_TASK_ID:-}" "$(hostname -s)" "$(date -u +%%FT%%TZ)" >> "$DEPT/scratch/runs/%s/starts.jsonl"\n' % (st, batch)
        if st in ("calibrate", "islands", "merge"):
            txt += SKIP_IF_OUTCOME.format(stage=st, batch=batch)
        txt += stage_body(st)
        txt += 'printf \'{"stage":"%s","run_id":"%%s","job":"%%s","task":"%%s","end":"%%s"}\\n\' "$RUN_ID" "${SLURM_JOB_ID}" "${SLURM_ARRAY_TASK_ID:-}" "$(date -u +%%FT%%TZ)" >> "$DEPT/scratch/runs/%s/ends.jsonl"\n' % (st, batch)
        write(os.path.join(out, name), txt, 0o755)
        files.append(name)
        del n_per_fit
    if P.get("pilot") is not None:   # WP7 O5: the calibration pilot island alone (H-11 gate (2)), after setup
        pl = P["pilot"]
        wc = sum(int(pl["cpus"]) * hours(pl["time"]) for _ in P["fits"])
        txt = HEADER.format(name="stage_pilot.sbatch", batch=batch, stage="pilot", wc=wc, cpus=pl["cpus"], mem=pl["mem"], time=pl["time"],
                            dept=dept, binary=P["binary"], submitter="submit_pilot.sh")
        txt += FIT_TABLE.format(runs=runs)
        txt += fit_selector(True).replace("{batch}", batch)
        txt += SKIP_IF_OUTCOME.format(stage="pilot", batch=batch)
        txt += ('# the same seed as calibrate (the manifest\'s engine seed); stops after the pilot island (no calib.bin)\n'
                'SEED=$(python3 -c \'import json,sys; print(json.load(open(sys.argv[1]))["params"]["seed"])\' "$SCR/run_manifests/$RUN_ID.json")\n'
                'mkdir -p "$RUN/log"\n'
                '# the calibration island plan on the real inputs, for the record (the island\'s own admission refuses if it does not fit)\n'
                '"$BIN" calibrate --plan-only 1 --mode V --data "$RUN/data.bin" --setup "$RUN/setup.bin" --threads "$OMP_NUM_THREADS" '
                '--mem-budget "$MEMB" --out "$RUN/pilot_plan" > "$RUN/log/pilot_plan.log" 2>&1 || true\n'
                '"$SCR/bin/v4_pilot_island" --data "$RUN/data.bin" --setup "$RUN/setup.bin" --seed "$SEED" --threads "$OMP_NUM_THREADS" '
                '--mem-budget "$MEMB" --with-ledger %d --verbose 1 --cost-dir "$RUN/cost_pilot" --out "$RUN/pilot.json" '
                '> "$RUN/log/pilot.log" 2>&1\n' % int(pl.get("with_ledger", 1)))
        txt += 'printf \'{"stage":"pilot","run_id":"%%s","job":"%%s","task":"%%s","end":"%%s"}\\n\' "$RUN_ID" "${SLURM_JOB_ID}" "${SLURM_ARRAY_TASK_ID:-}" "$(date -u +%%FT%%TZ)" >> "$DEPT/scratch/runs/%s/ends.jsonl"\n' % batch
        write(os.path.join(out, "stage_pilot.sbatch"), txt, 0o755)
        files.append("stage_pilot.sbatch")
    if P.get("isa_check") is not None:   # D-32: island r again with the comparison build; same science or the task fails
        r0 = P["fits"][0]["resources"]["islands"]
        wc = sum(int(f["resources"]["islands"]["cpus"]) * hours(P["isa_check"]["time"]) for f in P["fits"])
        txt = HEADER.format(name="stage_isa_check.sbatch", batch=batch, stage="isa_check", wc=wc, cpus=r0["cpus"], mem=r0["mem"],
                            time=P["isa_check"]["time"], dept=dept, binary=P["binary"], submitter="submit.sh")
        txt += FIT_TABLE.format(runs=runs)
        txt += fit_selector(False).replace("{batch}", batch)
        txt += SKIP_IF_OUTCOME.format(stage="isa_check", batch=batch)
        R = P["isa_check"]["island"]
        txt += ('R=%d\n' % R
                + 'python3 "$SCR/p1m_manifest.py" fill --template "$MAN/island.json" --out "$RUN/manifests/island_${R}_isa_check.json" '
                  '--bin "$SCR/bin/smcbvs4_isa_check" --set params.id=$R\n'
                + '"$SCR/bin/smcbvs4_isa_check" island --manifest "$RUN/manifests/island_${R}_isa_check.json" --threads "$OMP_NUM_THREADS" '
                  '--mem-budget "$MEMB" --out "$RUN/island_${R}_isa_check.bin" > "$RUN/log/island_${R}_isa_check.log" 2>&1\n'
                + 'rc=0\n'
                + 'python3 "$SCR/p1m_stage_cost.py" isa "$RUN/island_${R}.bin" "$RUN/island_${R}_isa_check.bin" --bin "$BIN" '
                  '--json "$RUN/isa_check.json" || rc=1\n'
                + '# D-32 (3): the bit form is the same in the plan-ISA, comparison and portable builds\n'
                + 'python3 "$SCR/p1m_stage_cost.py" bitform --json "$RUN/isa_check_bitform.json" --args "%s" '
                  '"$SCR/bin/v4_bench_island" "$SCR/bin/v4_bench_island_isa_check" "$SCR/bin/v4_bench_island_portable" || rc=1\n'
                  % BITFORM_ARGS
                + '[[ $rc == 0 ]] || { echo "D-32 isa check FAILED (isa_check*.json)" >&2; exit 1; }\n')
        txt += 'printf \'{"stage":"isa_check","run_id":"%%s","job":"%%s","task":"%%s","end":"%%s"}\\n\' "$RUN_ID" "${SLURM_JOB_ID}" "${SLURM_ARRAY_TASK_ID:-}" "$(date -u +%%FT%%TZ)" >> "$DEPT/scratch/runs/%s/ends.jsonl"\n' % batch
        write(os.path.join(out, "stage_isa_check.sbatch"), txt, 0o755)
        files.append("stage_isa_check.sbatch")
    write(os.path.join(out, "env.sh"), ENV_SH.format(batch=batch))
    files.append("env.sh")
    has_pilot = P.get("pilot") is not None
    write(os.path.join(out, "build.sh"), BUILD_SH.format(
        batch=batch, dept=dept, commit=P["code_commit"],
        isa=(" -DV4_ISLAND_ISA=" + P["island_isa"]) if P["island_isa"] else "",
        pilot_target=" v4_pilot_island" if has_pilot else "",
        bench_target=" v4_bench_island" if P.get("isa_check") is not None else "",
        bench_copy=('cp "$B/v4_bench_island" "$SCR/bin/v4_bench_island"\n' if P.get("isa_check") is not None else ""),
        pilot_copy=('cp "$B/v4_pilot_island" "$SCR/bin/v4_pilot_island"\nsha256sum "$SCR/bin/v4_pilot_island" | tee "$SCR/bin/v4_pilot_island.sha256"\n'
                    if has_pilot else ""),
        portable=(('# D-32: the comparison island build (isa_check.against = %s) for the cross-ISA island check (stage_isa_check)\n'
                   'BP=$SCR/build_isa_check; mkdir -p "$BP"\n'
                   'nice -n 19 cmake -S "$SCR/code/Scripts/SMC_BVS/engine_v4" -B "$BP" -DCMAKE_BUILD_TYPE=Release -DV4_TESTS=OFF%s > "$BP/cmake.log"\n'
                   'nice -n 19 make -C "$BP" -j3 smcbvs4 v4_bench_island\n'
                   'cp "$BP/smcbvs4" "$SCR/bin/smcbvs4_isa_check"\n'
                   'cp "$BP/v4_bench_island" "$SCR/bin/v4_bench_island_isa_check"\n'
                   'sha256sum "$SCR/bin/smcbvs4_isa_check" | tee "$SCR/bin/smcbvs4_isa_check.sha256"\n'
                   '# D-32 (3): a portable (x86-64-v2) build of the benchmark only, for the bit-form check\n'
                   'B2=$SCR/build_portable_bench; mkdir -p "$B2"\n'
                   'nice -n 19 cmake -S "$SCR/code/Scripts/SMC_BVS/engine_v4" -B "$B2" -DCMAKE_BUILD_TYPE=Release -DV4_TESTS=OFF > "$B2/cmake.log"\n'
                   'nice -n 19 make -C "$B2" -j3 v4_bench_island\n'
                   'cp "$B2/v4_bench_island" "$SCR/bin/v4_bench_island_portable"\n')
                  % (P["isa_check"]["against"], "" if P["isa_check"]["against"] == "portable" else " -DV4_ISLAND_ISA=" + P["isa_check"]["against"])
                  if P.get("isa_check") is not None else "")), 0o755)
    files.append("build.sh")
    # manifests (templates + one run manifest per run)
    for f in P["fits"]:
        md = os.path.join(out, "manifests", f["run_id"])
        os.makedirs(md, exist_ok=True)
        base_params = {"run_id": f["run_id"], "design": f["design"], "p": f["p"], "n": f["n"], "signal": f["signal"],
                       "data_seed": f["data_seed"], "seed": f["seed"], "Rp": f["Rp"], "N": f["N"]}
        for k in ("params",):
            base_params.update(f.get(k) or {})
        rd = "%s/scratch/runs/%s/%s" % (dept, batch, f["run_id"])
        ins = lambda *names: dict((rd + "/" + nm, "@hash") for nm in names)
        tmpl = {
            "gen": {}, "prep": ins("raw.bin"), "setup": ins("data.bin"),
            "calibrate": ins("data.bin", "setup.bin"),
            "island": ins("data.bin", "setup.bin", "calib.bin"),
            "merge": ins("data.bin", "setup.bin", "calib.bin", *["island_%d.bin" % r for r in range(1, f["Rp"] + 1)]),
            "eval": ins("fit.bin", "data.bin"), "post": ins("fit.bin", "data.bin"),
        }
        # gen takes the data seed as `seed` (WP1 gen spec); the other commands take the engine seed
        amp = {"strong": 1.0, "weak": 0.6, "null": 0.0}.get(f["signal"], 1.0)
        if f["design"] == "NULL":
            amp = 0.0
        gen_params = {"design": "AR" if f["design"] == "NULL" else f["design"], "n": f["n"], "p": f["p"],
                      "seed": f["data_seed"], "a": amp, "s0": (f.get("params") or {}).get("s0", 5)}
        for k in ("rho", "b", "sigma"):
            if k in (f.get("params") or {}):
                gen_params[k] = f["params"][k]
        for cmd, inputs in tmpl.items():
            m = {"schema": "smcbvs4.manifest/1", "command": cmd, "run_id": f["run_id"], "mode": f["mode"],
                 "binary": {"sha256": "@binary", "git_commit": P["code_commit"], "compiler": "@binary", "flags": "@binary",
                            "libm": "@binary"},
                 "inputs": dict(sorted(inputs.items())),
                 "params": (dict(gen_params) if cmd == "gen" else
                            {"truth_sha256": "@sha256:" + rd + "/truth.json", "threads": "@slurm"} if cmd == "eval" else
                            {"threads": "@slurm"} if cmd == "post" else dict(base_params, threads="@slurm")),
                 "budget": {"task_seconds": int(hours(f["resources"]["islands" if cmd == "island" else
                                                                 ("setup" if cmd in ("gen", "prep") else ("eval" if cmd == "post" else cmd))]["time"]) * 3600),
                            "fit_core_h": round(P["worst_case_core_h"] / len(P["fits"]), 1), "retries": 2},
                 "machine": {"host": "@slurm", "node_type": "sapphirerapids", "slurm_job_id": "@slurm"},
                 "outputs": {}}
            write(os.path.join(md, cmd + ".json"), json.dumps(m, indent=1) + "\n")
            files.append(os.path.join("manifests", f["run_id"], cmd + ".json"))
        rm = {"schema": "smcbvs4.run/1", "batch": batch, "run_id": f["run_id"], "mode": f["mode"], "code_commit": P["code_commit"],
              "params": base_params, "resources": f["resources"],
              "pipeline": ["setup(gen,prep,setup)", "calibrate", "islands[1..%d]" % f["Rp"], "merge", "eval(+post)"],
              "paths": {"run_dir": "%s/scratch/runs/%s/%s" % (dept, batch, f["run_id"]), "scripts": "%s/scripts/%s" % (dept, batch)},
              "created_utc": P["created_utc"]}
        write(os.path.join(out, "run_manifests", f["run_id"] + ".json"), json.dumps(rm, indent=1) + "\n")
        files.append(os.path.join("run_manifests", f["run_id"] + ".json"))
    # submit.sh (the manager's)
    F = len(P["fits"])
    thr = ("%%%d" % P["island_throttle"]) if P.get("island_throttle") else ""
    sub = """#!/usr/bin/env bash
# submit.sh -- P1M batch {batch}: {F} fits, {ntask} tasks, worst case {wc:.1f} billed core-h. GENERATED (dry run).
# Run ON NOTS by the Engineering manager after HQ's go; helpers never run it. Admission check (LEDGER.md) first.
# Job graph: setup[1-{F}] -> calibrate[1-{F}] (aftercorr) -> per fit i: islands[1-Rp] (afterok calibrate_i) -> merge -> eval.
# sbatch calls: 2 arrays + 3 per fit = {ncalls}. No polling here (POLICIES §12: at most one squeue/sacct per 5 minutes).
set -euo pipefail
DEPT=$(realpath -m "${{P1M_DEPT:-{dept}}}")
# department guard (PR12 MINOR-8): resolved path inside $HOME/SMC_Engineering_Department, or inside P1M_TEST_ROOT (tests)
in_dir() {{ local r; r=$(realpath -m "$2"); [[ $1 == "$r" || $1 == "$r"/* ]]; }}
if ! in_dir "$DEPT" "$HOME/SMC_Engineering_Department"; then
  [[ -n ${{P1M_TEST_ROOT:-}} ]] && in_dir "$DEPT" "$P1M_TEST_ROOT" || {{ echo "refusing: $DEPT is outside the department folder" >&2; exit 64; }}
fi
SB=${{SBATCH:-sbatch}}   # PR12 MINOR-9: tests point SBATCH at a stub by absolute path
SCR=$DEPT/scripts/{batch}
[[ ${{CONFIRM:-}} == yes ]] || {{ echo "refusing: set CONFIRM=yes (the manager's submission, after HQ's go)" >&2; exit 64; }}
cd "$SCR"
sha256sum --quiet -c SHA256SUMS || {{ echo "FATAL: scripts differ from SHA256SUMS" >&2; exit 66; }}
[[ -x $SCR/{binary} ]] || {{ echo "FATAL: binary $SCR/{binary} missing" >&2; exit 66; }}
{portable_check}[[ -d $DEPT/scratch/slurm_out && -d $DEPT/scratch/tmp ]] || {{ echo "FATAL: scratch/slurm_out or scratch/tmp missing" >&2; exit 66; }}
mkdir -p "$DEPT/scratch/runs/{batch}"
LOG=$DEPT/scratch/runs/{batch}/submissions.jsonl
log() {{ printf '{{"stage":"%s","fit":"%s","job":"%s","submitted_utc":"%s"}}\\n' "$1" "$2" "$3" "$(date -u +%FT%TZ)" | tee -a "$LOG"; }}
RUNS=({runs})
js=$("$SB" --parsable --array=1-{F} stage_setup.sbatch); log setup all "$js"
jc=$("$SB" --parsable --array=1-{F} --dependency=aftercorr:$js stage_calibrate.sbatch); log calibrate all "$jc"
for i in $(seq 1 {F}); do
  rp=$(sed -n "${{i}}p" fit_rp.txt)
  ji=$("$SB" --parsable --array=1-$rp{thr} --dependency=afterok:${{jc}}_$i stage_islands.sbatch $i); log islands "${{RUNS[$((i-1))]}}" "$ji"
{isa_line}  jm=$("$SB" --parsable --dependency=afterok:$ji stage_merge.sbatch $i); log merge "${{RUNS[$((i-1))]}}" "$jm"
  je=$("$SB" --parsable --dependency=afterok:$jm stage_eval.sbatch $i); log eval "${{RUNS[$((i-1))]}}" "$je"
done
echo "submitted; ledger row: see ledger_row.md (fill job ids from $LOG)"
""".format(batch=batch, F=F, ntask=P["n_tasks"], wc=P["worst_case_core_h"], ncalls=2 + 3 * F, dept=dept,
           binary=P["binary"], runs=runs, thr=thr,
           portable_check=('[[ -x $SCR/bin/smcbvs4_isa_check ]] || { echo "FATAL: binary $SCR/bin/smcbvs4_isa_check missing (build.sh, D-32 isa_check)" >&2; exit 66; }\n'
                           if P.get("isa_check") is not None else ""),
           isa_line=('  jx=$("$SB" --parsable --dependency=afterok:$ji stage_isa_check.sbatch $i); log isa_check "${RUNS[$((i-1))]}" "$jx"\n'
                     if P.get("isa_check") is not None else ""))
    if not P["pilot_only"]:   # a pilot-only batch has no full-fit submit.sh (review PR55 MAJOR)
        write(os.path.join(out, "submit.sh"), sub, 0o755)
        files.append("submit.sh")
    if P.get("pilot") is not None:   # setup -> pilot only (the fit itself waits for HQ's GO; its setup.bin is reused)
        # the preamble of submit.sh (guards, checksums, log) up to the fit table, without submit.sh's own comment lines
        pre = sub[:sub.index("RUNS=(")]
        pre = "\n".join(l for l in pre.split("\n")[1:] if not l.startswith(("# submit.sh", "# Job graph", "# sbatch calls")))
        sp = ("# submit_pilot.sh -- P1M batch %s: setup -> calibration pilot island only (WP7 O5; H-11 gate (2)), %d fit(s), worst case "
              "%.1f billed core-h. GENERATED (dry run). Never submits calibrate, islands, merge or eval.\n" % (batch, F, P["worst_case_pilot_core_h"]))
        sp += pre + "RUNS=(%s)\n" % runs
        sp += ('[[ -x $SCR/bin/v4_pilot_island ]] || { echo "FATAL: binary $SCR/bin/v4_pilot_island missing (build.sh)" >&2; exit 66; }\n'
               'js=$("$SB" --parsable --array=1-%d stage_setup.sbatch); log setup all "$js"\n'
               'jp=$("$SB" --parsable --array=1-%d --dependency=aftercorr:$js stage_pilot.sbatch); log pilot all "$jp"\n'
               'echo "submitted setup + pilot; worst case %.1f core-h (ledger: fill job ids from $LOG)"\n' % (F, F, P["worst_case_pilot_core_h"]))
        write(os.path.join(out, "submit_pilot.sh"), "#!/usr/bin/env bash\n" + sp, 0o755)
        files.append("submit_pilot.sh")
    write(os.path.join(out, "fit_rp.txt"), "".join("%d\n" % f["Rp"] for f in P["fits"]))
    files.append("fit_rp.txt")
    # helper copied next to the scripts (stdlib-only Python, run on the compute node)
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "p1m_manifest.py")) as fh:
        write(os.path.join(out, "p1m_manifest.py"), fh.read(), 0o755)
    files.append("p1m_manifest.py")
    with open(os.path.join(here, "p1m_stage_cost.py")) as fh:   # T5 report and the D-32 isa check (WP7 O5)
        write(os.path.join(out, "p1m_stage_cost.py"), fh.read(), 0o755)
    files.append("p1m_stage_cost.py")
    # ledger row
    now = P["created_utc"]
    row = ("| %s | %s (%d fits, %d tasks; dry run %s) | %s | (from submissions.jsonl) | %.1f | — | generated |\n"
           % (now[:10], batch, F, P["n_tasks"], now, P.get("kind", "gated (needs HQ go)"), P["worst_case_core_h"]))
    write(os.path.join(out, "ledger_row.md"), row)
    files.append("ledger_row.md")
    write(os.path.join(out, "plan.resolved.json"), json.dumps(P, indent=1, sort_keys=True) + "\n")
    files.append("plan.resolved.json")
    # SHA256SUMS last (covers everything submit.sh relies on)
    lines = []
    for f in sorted(files):
        with open(os.path.join(out, f), "rb") as fh:
            lines.append("%s  %s\n" % (hashlib.sha256(fh.read()).hexdigest(), f))
    write(os.path.join(out, "SHA256SUMS"), "".join(lines))
    return files


def _inside(path, root):
    p, r = os.path.realpath(os.path.abspath(path)), os.path.realpath(os.path.abspath(root))
    return os.path.commonpath([p, r]) == r


def path_allowed(path):
    if _inside(path, DEPT_DEFAULT):
        return True
    root, tmp = os.environ.get("P1M_TEST_ROOT"), os.environ.get("TMPDIR")
    return bool(root and tmp and _inside(root, tmp) and _inside(path, root))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--plan", required=True)
    ap.add_argument("--out", required=True, help="local directory = the future scripts/<batch>/ (deployed by the manager)")
    ap.add_argument("--dept", default=DEPT_DEFAULT, help="department root ON NOTS (paths written into the scripts)")
    ap.add_argument("--now", default=None, help="timestamp to record (tests); default: current UTC")
    a = ap.parse_args(argv)
    # PR12 MINOR-8: resolved (symlink-free), absolute containment checks. --dept and --out must lie inside the
    # department folder; tests may use P1M_TEST_ROOT, itself inside $TMPDIR (never a bare prefix match).
    for what, path in (("--dept", a.dept), ("--out", a.out)):
        if not path_allowed(path):
            print("refusing: %s %s is outside the department folder (POLICIES §12)" % (what, path), file=sys.stderr)
            return 64
    with open(a.plan) as fh:
        plan = json.load(fh)
    try:
        P = resolve(plan)
        P["created_utc"] = a.now or datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        files = generate(P, a.out, a.dept)
    except PlanError as e:
        print("plan error: %s" % e, file=sys.stderr)
        return 65
    print("dry run: wrote %d files to %s; %d fits, %d tasks, worst case %.1f billed core-h. Nothing was submitted."
          % (len(files), a.out, len(P["fits"]), P["n_tasks"], P["worst_case_core_h"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
