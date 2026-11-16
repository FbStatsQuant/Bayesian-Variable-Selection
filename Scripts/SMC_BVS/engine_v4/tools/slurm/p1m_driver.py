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
            "eval": {"cpus": 4, "mem": "4G", "time": "00:20:00"}},
    "1e5": {"setup": {"cpus": 32, "mem": "16G", "time": "00:30:00"},
            "calibrate": {"cpus": 64, "mem": "16G", "time": "01:30:00"},
            "islands": {"cpus": 64, "mem": "8G", "time": "01:00:00"},
            "merge": {"cpus": 16, "mem": "8G", "time": "00:30:00"},
            "eval": {"cpus": 4, "mem": "8G", "time": "00:30:00"}},
    "1e6": {"setup": {"cpus": 96, "mem": "48G", "time": "01:30:00"},
            "calibrate": {"cpus": 64, "mem": "32G", "time": "02:00:00"},
            "islands": {"cpus": 64, "mem": "32G", "time": "02:00:00"},
            "merge": {"cpus": 32, "mem": "16G", "time": "01:00:00"},
            "eval": {"cpus": 8, "mem": "16G", "time": "00:45:00"}},
}


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
    tasks = sum(3 + f["Rp"] for f in P["fits"]) + F    # setup + calibrate + Rp islands + merge + eval
    P["n_tasks"] = tasks
    if tasks > TASK_CAP:
        raise PlanError("batch has %d tasks > the 150-task cap: split it into waves (fewer fits per batch)" % tasks)
    wc = 0.0
    for f in P["fits"]:
        for st in STAGES:
            r = f["resources"][st]
            n = f["Rp"] if st == "islands" else 1
            wc += n * int(r["cpus"]) * hours(r["time"])
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
# Submitted only by submit.sh (the manager's). Worst case of this file: {wc:.1f} billed core-h.
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
#SBATCH --output={dept}/scratch/slurm_out/%x_%A_%a.out
#SBATCH --error={dept}/scratch/slurm_out/%x_%A_%a.err
set -euo pipefail
DEPT={dept}
SCR=$DEPT/scripts/{batch}
BIN=$SCR/{binary}
export TMPDIR=$DEPT/scratch/tmp/${{SLURM_JOB_ID}}
mkdir -p "$TMPDIR"; trap 'rm -rf "$TMPDIR"' EXIT
export OMP_NUM_THREADS=${{SLURM_CPUS_PER_TASK}}
[[ -f $SCR/env.sh ]] && source "$SCR/env.sh"
"""

FIT_TABLE = """# fit table: index (1-based) -> run_id
RUNS=({runs})
"""


def fit_selector(by_array):
    sel = "${SLURM_ARRAY_TASK_ID}" if by_array else "${1:?fit index}"
    return ("FIT=%s\nRUN_ID=${RUNS[$((FIT-1))]}\nRUN=$DEPT/scratch/runs/%s/$RUN_ID\nMAN=$SCR/manifests/$RUN_ID\n" % (sel, "{batch}"))


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
                + run.format(cmd="prep", suffix="", extra=' --in "$RUN/raw.bin"', out="data.bin")
                + fill.format(cmd="setup", suffix="") + "\n"
                + run.format(cmd="setup", suffix="", extra=' --threads "$OMP_NUM_THREADS"', out="setup.bin"))
    if stage == "calibrate":
        return (fill.format(cmd="calibrate", suffix="") + "\n"
                + run.format(cmd="calibrate", suffix="", extra=' --threads "$OMP_NUM_THREADS"', out="calib.bin"))
    if stage == "islands":
        return ("R=${SLURM_ARRAY_TASK_ID}\n"
                + fill.format(cmd="island", suffix="_$R") + " --set params.id=$R\n"
                + run.format(cmd="island", suffix="_$R", extra=' --threads "$OMP_NUM_THREADS"', out="island_$R.bin"))
    if stage == "merge":
        return (fill.format(cmd="merge", suffix="") + "\n"
                + run.format(cmd="merge", suffix="", extra=' --threads "$OMP_NUM_THREADS"', out="fit.bin"))
    if stage == "eval":
        return ('"$BIN" eval --fit "$RUN/fit.bin" --data "$RUN/data.bin" --truth "$RUN/truth.json" --threads "$OMP_NUM_THREADS" '
                '--n-draws "$NDRAWS" --n-x "$NX" --n-test "$NTEST" --out "$RUN/eval.bin" > "$RUN/log/eval.log" 2>&1\n'
                'if [[ $POST == 1 ]]; then "$BIN" post --fit "$RUN/fit.bin" --data "$RUN/data.bin" --out "$RUN/law.bin" > "$RUN/log/post.log" 2>&1; fi\n')
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
    for st in STAGES:
        rs = {json.dumps(f["resources"][st], sort_keys=True) for f in P["fits"]}
        if len(rs) != 1:
            raise PlanError("stage %s: all fits of one batch must share resources (split the batch by rung)" % st)
        r = P["fits"][0]["resources"][st]
        n_per_fit = P["fits"][0]["Rp"] if st == "islands" else 1
        wc = sum((f["Rp"] if st == "islands" else 1) * int(r["cpus"]) * hours(r["time"]) for f in P["fits"])
        name = "stage_%s.sbatch" % st
        txt = HEADER.format(name=name, batch=batch, stage=st, wc=wc, cpus=r["cpus"], mem=r["mem"], time=r["time"],
                            dept=dept, binary=P["binary"])
        txt += FIT_TABLE.format(runs=runs)
        txt += fit_selector(st in ("setup", "calibrate")).replace("{batch}", batch)
        if st == "eval":
            e = P["eval"]
            txt += "NDRAWS=%d\nNX=%d\nNTEST=%d\nPOST=%d\n" % (e.get("n_draws", 10000), e.get("n_x", 4000), e.get("n_test", 10000),
                                                           1 if e.get("post", True) else 0)
        txt += 'printf \'{"stage":"%s","run_id":"%%s","job":"%%s","task":"%%s","host":"%%s","start":"%%s"}\\n\' "$RUN_ID" "${SLURM_JOB_ID}" "${SLURM_ARRAY_TASK_ID:-}" "$(hostname -s)" "$(date -u +%%FT%%TZ)" >> "$DEPT/scratch/runs/%s/starts.jsonl"\n' % (st, batch)
        txt += stage_body(st)
        txt += 'printf \'{"stage":"%s","run_id":"%%s","job":"%%s","task":"%%s","end":"%%s"}\\n\' "$RUN_ID" "${SLURM_JOB_ID}" "${SLURM_ARRAY_TASK_ID:-}" "$(date -u +%%FT%%TZ)" >> "$DEPT/scratch/runs/%s/ends.jsonl"\n' % (st, batch)
        write(os.path.join(out, name), txt, 0o755)
        files.append(name)
        del n_per_fit
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
                 "params": dict(gen_params) if cmd == "gen" else dict(base_params, threads="@slurm"),
                 "budget": {"task_seconds": int(hours(f["resources"]["islands" if cmd == "island" else
                                                                 ("setup" if cmd in ("gen", "prep") else cmd)]["time"]) * 3600),
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
DEPT=${{P1M_DEPT:-{dept}}}
SCR=$DEPT/scripts/{batch}
[[ ${{CONFIRM:-}} == yes ]] || {{ echo "refusing: set CONFIRM=yes (the manager's submission, after HQ's go)" >&2; exit 64; }}
cd "$SCR"
sha256sum --quiet -c SHA256SUMS || {{ echo "FATAL: scripts differ from SHA256SUMS" >&2; exit 66; }}
[[ -x $SCR/{binary} ]] || {{ echo "FATAL: binary $SCR/{binary} missing" >&2; exit 66; }}
[[ -d $DEPT/scratch/slurm_out && -d $DEPT/scratch/tmp ]] || {{ echo "FATAL: scratch/slurm_out or scratch/tmp missing" >&2; exit 66; }}
mkdir -p "$DEPT/scratch/runs/{batch}"
LOG=$DEPT/scratch/runs/{batch}/submissions.jsonl
log() {{ printf '{{"stage":"%s","fit":"%s","job":"%s","submitted_utc":"%s"}}\\n' "$1" "$2" "$3" "$(date -u +%FT%TZ)" | tee -a "$LOG"; }}
RUNS=({runs})
js=$(sbatch --parsable --array=1-{F} stage_setup.sbatch); log setup all "$js"
jc=$(sbatch --parsable --array=1-{F} --dependency=aftercorr:$js stage_calibrate.sbatch); log calibrate all "$jc"
for i in $(seq 1 {F}); do
  rp=$(sed -n "${{i}}p" fit_rp.txt)
  ji=$(sbatch --parsable --array=1-$rp{thr} --dependency=afterok:${{jc}}_$i stage_islands.sbatch $i); log islands "${{RUNS[$((i-1))]}}" "$ji"
  jm=$(sbatch --parsable --dependency=afterok:$ji stage_merge.sbatch $i); log merge "${{RUNS[$((i-1))]}}" "$jm"
  je=$(sbatch --parsable --dependency=afterok:$jm stage_eval.sbatch $i); log eval "${{RUNS[$((i-1))]}}" "$je"
done
echo "submitted; ledger row: see ledger_row.md (fill job ids from $LOG)"
""".format(batch=batch, F=F, ntask=P["n_tasks"], wc=P["worst_case_core_h"], ncalls=2 + 3 * F, dept=dept,
           binary=P["binary"], runs=runs, thr=thr)
    write(os.path.join(out, "submit.sh"), sub, 0o755)
    files.append("submit.sh")
    write(os.path.join(out, "fit_rp.txt"), "".join("%d\n" % f["Rp"] for f in P["fits"]))
    files.append("fit_rp.txt")
    # helper copied next to the scripts (stdlib-only Python, run on the compute node)
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "p1m_manifest.py")) as fh:
        write(os.path.join(out, "p1m_manifest.py"), fh.read(), 0o755)
    files.append("p1m_manifest.py")
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


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--plan", required=True)
    ap.add_argument("--out", required=True, help="local directory = the future scripts/<batch>/ (deployed by the manager)")
    ap.add_argument("--dept", default=DEPT_DEFAULT, help="department root ON NOTS (paths written into the scripts)")
    ap.add_argument("--now", default=None, help="timestamp to record (tests); default: current UTC")
    a = ap.parse_args(argv)
    if not a.dept.startswith("/home/fb31/SMC_Engineering_Department") and not os.environ.get("P1M_DRIVER_TEST"):
        print("refusing: --dept must be the department folder (POLICIES §12)", file=sys.stderr)
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
