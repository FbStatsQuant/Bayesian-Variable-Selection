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
  (plan key "restart": {"attempts": A, "margin_s": m}; WP7 O4) the islands array is submitted A times, attempt k+1
                          after attempt k (afterany): an island that reached a soft stop (--stop-after-s = limit - margin,
                          exit 22: checkpoint written) or was killed at its limit resumes from island_r.ckpt.{a,b};
                          a finished island's task exits at once (island_<r>.done); a failed one repeats its exit code
                          (island_<r>.failed). Merge waits for the last attempt (afterok).
  stage_t6.sbatch         (plan key "t6" + "t6_only": true; WP7 O4) T6 by real kills (p1m_t6.py) on one island of a finished
                          fit's inputs; submit_t6.sh submits it alone
  stage_isa_check.sbatch  (plan key "isa_check" only; D-32) one task per fit, afterok on its island array: island r re-run
                          with the PORTABLE build (bin/smcbvs4_isa_check) and compared with the island_isa run
                          (p1m_stage_cost.py isa: meta.output_hash + every non-meta section hash); fails if they differ
  ledger_row.md           the LEDGER.md row (worst case = sum of allocated CPUs x time limit, billed core-h)
  SHA256SUMS              hashes of every generated file (submit.sh verifies them first)
  plan.resolved.json      the plan with every default filled in
  (theory mode: a fit whose mode is law or compat -- the coded calibration, which can escalate tier 0 -> 1 (N x 4, D-26))
                          the island and merge stages take N from calib.bin.json (tiers[tier_final].N_final) at STAGE time
                          (p1m_calib_n.py set-n after the fill; the engine refuses an island whose N differs from calib's and checks the islands' N
                          against calib's at the merge, whose manifest N is only a record; the plan's N stays as the pre-calibration record;
                          the calibrate stage records both in the run manifest, key calib_N); the islands' time limit is requested
                          for the escalated N up front: base x ceil(4 N0 / N_plan), capped at 2 h (THEORY_ISLANDS_MAX_H) and max_task_hours
                          (see law_islands_time). isa_check is refused in a theory-mode plan (V's class-A check).
                          V mode is byte-identical to before.
(Campaign freeze: the optional plan keys method_tag and core_tree, written by p1m_cells.py, are validated and copied into
every run manifest next to code_commit.)

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
import difflib
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
INT31 = 2 ** 31 - 1          # seeds, p, n
CPU_CAP = 1536
STAGES = ["setup", "calibrate", "islands", "merge", "eval"]
MODES = ("compat", "law", "V")
DESIGNS = ("IND", "AR", "BLK", "ADJ-OPP", "NULL")     # NULL = AR with no signal
SIGNALS = ("strong", "weak", "null")                  # amplitude 1.0 / 0.6 / 0.0 (the generator's `a`)
STAGE_KEYS = ("cpus", "mem", "time")
# Required top-level keys (a missing one is a plan error: a typo in core_h_cap must not mean "no cap"). island_isa is also
# required, but only for V-mode plans (checked where the mode is known).
REQUIRED_KEYS = ("core_h_cap", "max_task_hours", "mode", "code_commit", "binary", "fits")
# Keys the driver reads, plus the ones it writes into plan.resolved.json (so that a resolved plan can be fed back in).
# Anything else is reported as a WARNING (other tools may add keys), or refused under --strict.
KNOWN_KEYS = {"batch", "kind", "island_isa", "eval", "island_throttle", "restart", "t6", "t6_only", "pilot", "pilot_only",
              "isa_check", "resources", "created_utc", "method_tag", "core_tree", "n_tasks", "worst_case_core_h", "worst_case_pilot_core_h", "warnings"} | set(REQUIRED_KEYS)
KNOWN_FIT_KEYS = {"run_id", "design", "p", "n", "signal", "data_seed", "seed", "Rp", "N", "mode", "resources", "params",
                  "islands_time_base"}   # islands_time_base: written by resolve() for a theory-mode fit whose island limit was scaled


def unknown_keys(plan):
    """Warnings for top-level and per-fit keys the driver does not know, with a 'did you mean' where one is close."""
    out = []
    def hint(k, known):
        m = difflib.get_close_matches(str(k), sorted(known), n=1, cutoff=0.6)
        return " (did you mean %r?)" % m[0] if m else ""
    for k in plan:
        if k not in KNOWN_KEYS:
            out.append("unknown top-level key %r%s" % (k, hint(k, KNOWN_KEYS)))
    fits = plan.get("fits")
    for i, f in enumerate(fits if isinstance(fits, list) else []):
        if isinstance(f, dict):
            name = f["run_id"] if isinstance(f.get("run_id"), str) else str(i)
            for k in f:
                if k not in KNOWN_FIT_KEYS:
                    out.append("unknown key %r in fit %s%s" % (k, name, hint(k, KNOWN_FIT_KEYS)))
    return out

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
            # merge task: planned 43.7 GiB at n = 200, 58.5 GiB at n = 1,000 IND (PR45 INFO-3: 2.5 x setup.bin before StartView), but the
            # 10^6 pilot fit MEASURED 75.1 GiB (sacct MaxRSS), too close to the old 80G -> 128G (HQ H-14) until a measured 10^6
            # peak_rss_kb (PR #65); 48G proposed after.
            "merge": {"cpus": 32, "mem": "128G", "time": "01:00:00"},
            "eval": {"cpus": 8, "mem": "16G", "time": "01:00:00"}},
}


# Theory mode (law, compat): the coded calibration (v3's tiers, calib_run.h budgets()) may freeze tier 1, N = 4 x N0 with
# N0 = max(2500, n, p); V mode never escalates (frozen N = 2,500).
THEORY_TIER_MULT = 4
THEORY_ISLANDS_MAX_H = 2.0   # §0-v2.5 / H-18: islands stay <= 2 h; the only > 2 h exception is the T calibrate (HQ), not a plan-wide max_task_hours


def theory_n_max(f):
    return THEORY_TIER_MULT * max(2500, f["n"], f["p"])


def hhmmss(h):
    s = int(round(h * 3600))
    return "%02d:%02d:%02d" % (s // 3600, s // 60 % 60, s % 60)


def law_islands_time(P, f, base):
    """The final islands' time limit of a theory-mode fit. The islands' N is calib.bin's frozen N, known only after the calibration,
    but sbatch needs the limit at SUBMIT time, and Slurm lets an ordinary user only LOWER a limit afterwards (`scontrol update
    TimeLimit` cannot raise it), so the limit is requested for the largest possible N up front:
        limit = base x ceil(N_tier1 / N_plan),  N_tier1 = 4 max(2500, n, p),  capped at THEORY_ISLANDS_MAX_H = 2 h (and
    max_task_hours, and the QOS wall), but never below the base itself. It is the cost-linear-in-N bound; an island that finishes
    early is billed what it used. Returns (limit string, factor)."""
    factor = max(1, -(-theory_n_max(f) // f["N"]))
    h = max(hours(base), min(hours(base) * factor, THEORY_ISLANDS_MAX_H, P["max_task_hours"], QOS_WALL_H))
    return hhmmss(h), factor


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
    if not isinstance(s, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}", s):
        raise PlanError("%s %r: use letters, digits, _ . - (max 64)" % (what, s))
    return s


# Plan value checks (WP7 freeze item): every numeric key is refused with one line naming the key, the value and the
# allowed range (exit 65); a bool is never a number here (JSON true is not 1).
def plan_int(v, what, lo, hi):
    if isinstance(v, bool) or not isinstance(v, int) or not (lo <= v <= hi):
        raise PlanError("%s must be an integer in [%d, %d], got %r" % (what, lo, hi, v))
    return v


def plan_pos(v, what):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or not v > 0:
        raise PlanError("%s must be a number > 0, got %r" % (what, v))
    return v


def plan_choice(v, what, allowed):
    """An enumerated string: exactly one of `allowed` (case-sensitive: 'Weak' is not 'weak'), else refuse with the allowed set."""
    if not isinstance(v, str) or v not in allowed:
        raise PlanError("%s must be one of %s, got %r" % (what, ", ".join(allowed), v))
    return v


def plan_bool(v, what):
    if not isinstance(v, bool):
        raise PlanError("%s must be true or false, got %r" % (what, v))
    return v


def plan_mem(v, what):
    if not isinstance(v, str) or not re.fullmatch(r"\d+[MG]", v) or int(v[:-1]) < 1:
        raise PlanError("%s must be a positive size like 512M or 32G, got %r" % (what, v))
    return v


def plan_time(v, what):
    if not isinstance(v, str) or not re.fullmatch(r"(?:\d+-)?\d+:\d\d:\d\d", v):
        raise PlanError("%s must be a time limit [D-]HH:MM:SS, got %r" % (what, v))
    h = hours(v)
    if h <= 0:
        raise PlanError("%s must be a time limit > 0, got %r" % (what, v))
    return h


def resolve(plan):
    """Fill defaults and validate. Returns the resolved plan (a new dict)."""
    if not isinstance(plan, dict):
        raise PlanError("the plan must be a JSON object, got %s" % type(plan).__name__)
    P = copy.deepcopy(plan)
    safe_id(P.get("batch", ""), "batch")
    missing = [k for k in REQUIRED_KEYS if k not in P]
    if missing:
        raise PlanError("required plan key%s missing: %s" % ("s" if len(missing) > 1 else "", ", ".join(missing)))
    warn = unknown_keys(P)
    plan_choice(P["mode"], "mode", MODES)
    # (mode, binary, code_commit, max_task_hours, core_h_cap have no defaults any more: they are required, see REQUIRED_KEYS;
    # binary is relative to scripts/<batch>/, deployed with the frozen code)
    for k in ("binary", "code_commit"):
        if not isinstance(P[k], str) or not P[k]:
            raise PlanError("%s must be a non-empty string, got %r" % (k, P[k]))
    # campaign freeze (p1m_cells.py FREEZE): optional, recorded in every run manifest; core_tree is a git tree hash
    for k in ("method_tag", "core_tree"):
        if k in P and (not isinstance(P[k], str) or not P[k]):
            raise PlanError("%s must be a non-empty string, got %r" % (k, P[k]))
    if "core_tree" in P and not re.fullmatch(r"[0-9a-f]{40}", P["core_tree"]):
        raise PlanError("core_tree must be a 40-hex git tree hash, got %r" % (P["core_tree"],))
    P.setdefault("eval", {"threads": None, "post": True, "n_draws": 10000, "n_x": 4000, "n_test": 10000})
    P.setdefault("island_throttle", None)           # optional %k on each island array
    P.setdefault("island_isa", "")                  # WP7 O5: -DV4_ISLAND_ISA for build.sh ("" = the portable default)
    plan_pos(P["max_task_hours"], "max_task_hours")
    plan_pos(P["core_h_cap"], "core_h_cap")          # required; null is not "no cap"
    if P["island_throttle"] is not None:
        plan_int(P["island_throttle"], "island_throttle", 1, TASK_CAP)
    if not isinstance(P["eval"], dict):
        raise PlanError("eval must be a JSON object, got %r" % (P["eval"],))
    if "post" in P["eval"]:
        plan_bool(P["eval"]["post"], "eval.post")
    for k in ("n_draws", "n_x", "n_test"):
        if k in P["eval"]:
            plan_int(P["eval"][k], "eval.%s" % k, 1, INT31)
    if P["eval"].get("threads") is not None:
        plan_int(P["eval"]["threads"], "eval.threads", 1, 192)
    if not isinstance(P["island_isa"], str):
        raise PlanError("island_isa must be a -march name such as sapphirerapids, got %r" % (P["island_isa"],))
    if P["island_isa"] and not re.fullmatch(r"[A-Za-z0-9_.-]+", P["island_isa"]):
        raise PlanError("island_isa must be a -march name such as sapphirerapids")
    # D-32 (1): class-A values (V mode) use a true FMA in every FMA build and a*b + c without one (amath.h fma8), so a
    # V plan needs an island ISA with FMA, at least x86-64-v3; one fit = one FMA family (one binary for every stage)
    for i, f in enumerate(P.get("fits") if isinstance(P.get("fits"), list) else []):
        if isinstance(f, dict) and "mode" in f:
            plan_choice(f["mode"], "fits[%d].mode" % i, MODES)
    v_plan = P["mode"] == "V" or any(f.get("mode", P["mode"]) == "V" for f in P.get("fits") or [] if isinstance(f, dict))
    if v_plan and "island_isa" not in plan:
        raise PlanError("required plan key missing: island_isa (a V-mode plan needs an FMA island_isa: one of %s)" % ", ".join(sorted(FMA_ISAS)))
    if v_plan and P["island_isa"] not in FMA_ISAS:
        raise PlanError("a V-mode plan needs island_isa with FMA (one of %s; D-32); got %r" % (", ".join(sorted(FMA_ISAS)), P["island_isa"]))
    # WP7 O4: the islands' resubmission chain (restart from island_r.ckpt.{a,b}); default: one attempt, no soft stop
    rs = P.get("restart")
    if rs is not None:
        if not isinstance(rs, dict):
            raise PlanError("restart must be a JSON object, got %r" % (rs,))
        plan_int(rs.get("attempts"), "restart.attempts", 1, 6)
        if "margin_s" in rs and (isinstance(rs["margin_s"], bool) or not isinstance(rs["margin_s"], (int, float))
                                 or not math.isfinite(rs["margin_s"]) or rs["margin_s"] < 0):
            raise PlanError("restart.margin_s must be a number >= 0, got %r" % (rs["margin_s"],))
        if P.get("pilot_only"):
            raise PlanError("restart does not apply to a pilot_only batch")
    # WP7 O4: T6 by real kills (a t6_only batch: the island of a finished fit's inputs, nothing else)
    if "t6_only" in P:
        plan_bool(P["t6_only"], "t6_only")
    t6 = P.get("t6")   # no setdefault: a plan without the keys resolves to exactly what it did before O4 (plan.resolved.json)
    if P.get("t6_only") and t6 is None:
        raise PlanError("t6_only needs a t6 section")
    if t6 is not None and not P.get("t6_only"):
        raise PlanError("a t6 section needs t6_only: true (a T6 batch is generated alone: its worst case and submit script are the T6's)")
    if t6 is not None:
        if not isinstance(t6, dict):
            raise PlanError("t6 must be a JSON object, got %r" % (t6,))
        for k in ("source_batch", "cpus", "mem", "time"):
            if k not in t6:
                raise PlanError("t6: missing %r" % k)
        safe_id(t6["source_batch"], "t6.source_batch")
        plan_int(t6["cpus"], "t6.cpus", 1, 192)
        plan_mem(t6["mem"], "t6.mem")
        h = plan_time(t6["time"], "t6.time")
        if h > QOS_WALL_H or h > P["max_task_hours"] + 1e-9:
            raise PlanError("t6: %s exceeds max_task_hours = %.2f" % (t6["time"], P["max_task_hours"]))
        t6.setdefault("island", 1); t6.setdefault("kills", 2); t6.setdefault("ckpt_every_s", 20)
        plan_int(t6["kills"], "t6.kills", 1, 4)
        plan_int(t6["island"], "t6.island", 1, 2 ** 20 - 1)
        plan_pos(t6["ckpt_every_s"], "t6.ckpt_every_s")
        if P.get("pilot") is not None or P.get("pilot_only") or P.get("isa_check") is not None or rs is not None:
            raise PlanError("a t6 batch has no pilot, isa_check or restart section")
    # review PR55 MAJOR: a pilot-only batch (P7) generates setup + pilot and nothing that could launch the fit; its
    # worst case, cap and ledger row are the pilot's (the real fit later gets its own plan)
    P.setdefault("pilot_only", False)
    plan_bool(P["pilot_only"], "pilot_only")
    if P["pilot_only"] and P.get("pilot") is None:
        raise PlanError("pilot_only needs a pilot section")
    if P["pilot_only"] and P.get("isa_check") is not None:
        raise PlanError("pilot_only batches have no islands: remove isa_check")
    if P.get("pilot") is not None:                  # WP7 O5: {"cpus", "mem", "time", "with_ledger"} of the pilot task
        pl = P["pilot"]
        if not isinstance(pl, dict):
            raise PlanError("pilot must be a JSON object, got %r" % (pl,))
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
        plan_int(pl["cpus"], "pilot.cpus", 1, 192)
        plan_mem(pl["mem"], "pilot.mem")
        h = plan_time(pl["time"], "pilot.time")
        if h > QOS_WALL_H or h > P["max_task_hours"] + 1e-9:
            raise PlanError("pilot: %s exceeds max_task_hours = %.2f" % (pl["time"], P["max_task_hours"]))
        pl.setdefault("with_ledger", 1)
        if isinstance(pl["with_ledger"], bool) or pl["with_ledger"] not in (0, 1):
            raise PlanError("pilot.with_ledger must be one of 0, 1, got %r" % (pl["with_ledger"],))
    if P.get("isa_check") is not None:              # D-32: T2 across island ISAs (one island re-run with a comparison build)
        if not P["island_isa"]:
            raise PlanError("isa_check needs island_isa (the comparison build is the other side)")
        if not isinstance(P["isa_check"], dict):
            raise PlanError("isa_check must be a JSON object, got %r" % (P["isa_check"],))
        plan_int(P["isa_check"].get("island"), "isa_check.island", 1, 2 ** 20 - 1)
        # the comparison build's island ISA: class A uses a true FMA when the build has one (amath.h fma8), so its bits
        # are those of every FMA build (x86-64-v3 = AVX2 + FMA matched AVX-512 on Owls) and differ from a build without
        # FMA ("portable" = x86-64-v2) by design; the bit form (theory/compat) is ISA-free
        P["isa_check"].setdefault("against", "x86-64-v3")
        plan_choice(P["isa_check"]["against"], "isa_check.against (an FMA ISA)", tuple(sorted(FMA_ISAS)))   # D-32 (3): the comparison is within the FMA family
        if P["isa_check"]["against"] == P["island_isa"]:   # review PR55 m5: the same ISA makes the comparison vacuous
            raise PlanError("isa_check.against equals island_isa: the class-A comparison would compare a build with itself")
        # its own time limit (review PR55 m5): one island re-run, two `info --meta` reads, three bit-form islands
        P["isa_check"].setdefault("time", "00:40:00")
        h = plan_time(P["isa_check"]["time"], "isa_check.time")
        if h > QOS_WALL_H or h > P["max_task_hours"] + 1e-9:
            raise PlanError("isa_check.time %s exceeds max_task_hours = %.2f" % (P["isa_check"]["time"], P["max_task_hours"]))
    if not P.get("fits"):
        raise PlanError("plan has no fits")
    if not isinstance(P["fits"], list):
        raise PlanError("fits must be a list of fit objects, got %s" % type(P["fits"]).__name__)
    seen = set()
    for i, f in enumerate(P["fits"]):
        if not isinstance(f, dict):
            raise PlanError("fit %d must be a JSON object, got %r" % (i, f))
        for k in ("run_id", "design", "p", "n", "signal", "data_seed", "seed"):
            if k not in f:
                raise PlanError("fit %d: missing %r" % (i, k))
        safe_id(f["run_id"], "run_id")
        if f["run_id"] in seen:
            raise PlanError("duplicate run_id %s" % f["run_id"])
        seen.add(f["run_id"])
        plan_choice(f["design"], "fit %s: design" % f["run_id"], DESIGNS)
        plan_choice(f["signal"], "fit %s: signal" % f["run_id"], SIGNALS)
        for k in ("seed", "data_seed"):
            plan_int(f[k], "fit %s: %s" % (f["run_id"], k), 1, INT31)
        plan_int(f["p"], "fit %s: p" % f["run_id"], 1, INT31)
        plan_int(f["n"], "fit %s: n" % f["run_id"], 3, INT31)     # gen needs n >= 3
        f.setdefault("Rp", 16)
        f.setdefault("N", 2500)
        plan_int(f["Rp"], "fit %s: Rp" % f["run_id"], 1, 2 ** 20 - 1)   # island r < 2^20 (INTERFACES §3)
        plan_int(f["N"], "fit %s: N" % f["run_id"], 1, 2 ** 24)
        f.setdefault("mode", P["mode"])
        plan_choice(f["mode"], "fit %s: mode" % f["run_id"], MODES)
        res = copy.deepcopy(DEFAULT_RES[rung(f["p"])])
        for where, given in (("resources", P.get("resources")), ("fit %s resources" % f["run_id"], f.get("resources"))):
            if given is not None and not isinstance(given, dict):
                raise PlanError("%s must be a JSON object, got %r" % (where, given))
            for st, over in (given or {}).items():
                if st not in res:
                    raise PlanError("unknown stage %r in %s: allowed %s" % (st, where, ", ".join(STAGES)))
                if not isinstance(over, dict):
                    raise PlanError("%s.%s must be a JSON object, got %r" % (where, st, over))
                for rk in over:
                    if rk not in STAGE_KEYS:   # a typo such as "cpu" would otherwise be silently ignored
                        raise PlanError("unknown key %r in %s.%s: allowed %s" % (rk, where, st, ", ".join(STAGE_KEYS)))
                res[st].update(over)
        for st, r in res.items():
            what = "fit %s stage %s" % (f["run_id"], st)
            plan_int(r["cpus"], what + ": cpus", 1, 192)
            plan_mem(r["mem"], what + ": mem")
            h = plan_time(r["time"], what + ": time")
            if h > QOS_WALL_H:
                raise PlanError("fit %s stage %s: %s exceeds the QOS wall of 24 h" % (f["run_id"], st, r["time"]))
            if h > P["max_task_hours"] + 1e-9:
                raise PlanError("fit %s stage %s: %s exceeds max_task_hours = %.2f (§0-v2.5: no job longer than 2 h)"
                                % (f["run_id"], st, r["time"], P["max_task_hours"]))
        if f["mode"] != "V":   # theory mode: islands sized for the escalated N, always recomputed from the base (resolve is idempotent)
            has_base = "islands_time_base" in f
            base = f["islands_time_base"] if has_base else res["islands"]["time"]
            if has_base:
                plan_time(base, "fit %s: islands_time_base" % f["run_id"])
            lim, factor = law_islands_time(P, f, base)
            if has_base and abs(hours(res["islands"]["time"]) - hours(lim)) > 1e-9:
                raise PlanError("fit %s: islands time %s is not the scaled limit %s of islands_time_base %s (remove islands_time_base to rescale)"
                                % (f["run_id"], res["islands"]["time"], lim, base))
            if factor > 1 or has_base:
                f["islands_time_base"] = base
                res["islands"]["time"] = lim
        f["resources"] = res
    F = len(P["fits"])
    if rs is not None:   # the soft-stop margin: the step in flight and its checkpoint must fit before the limit
        lim = int(hours(P["fits"][0]["resources"]["islands"]["time"]) * 3600)
        rs.setdefault("margin_s", max(300, int(0.15 * lim)))
        if rs["margin_s"] >= lim:
            raise PlanError("restart.margin_s %s must be below the islands' time limit (%d s)" % (rs["margin_s"], lim))
    if P.get("isa_check") is not None and any(f["mode"] != "V" for f in P["fits"]):
        # the stage fills the island template with the plan's N, without set-n, and its time is not scaled: a theory-mode fit that escalates would be refused
        raise PlanError("isa_check is a V (class-A) check; theory-mode plans are ISA-free (law / compat fits in the plan: remove isa_check)")
    if P.get("isa_check") is not None:
        for f in P["fits"]:
            if P["isa_check"]["island"] > f["Rp"]:
                raise PlanError("isa_check: island %d > Rp of fit %s" % (P["isa_check"]["island"], f["run_id"]))
    tasks = sum(3 + f["Rp"] for f in P["fits"]) + F    # setup + calibrate + Rp islands + merge + eval
    if P.get("isa_check") is not None:
        tasks += F                                       # + one island re-run per fit with the comparison build (D-32)
    if rs is not None and rs["attempts"] > 1:
        tasks += sum(f["Rp"] for f in P["fits"]) * (rs["attempts"] - 1)   # the retry arrays (queued tasks count toward the cap)
    if P["pilot_only"]:
        tasks = 2 * F                                    # setup + pilot
    if P.get("t6_only"):
        tasks = F                                        # one T6 task per fit
    P["n_tasks"] = tasks
    if warn:
        P["warnings"] = warn
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
    if rs is not None and rs["attempts"] > 1:   # the retry arrays are billed at their limits in the worst case (finished islands exit at once)
        for f in P["fits"]:
            wc += (rs["attempts"] - 1) * f["Rp"] * int(f["resources"]["islands"]["cpus"]) * hours(f["resources"]["islands"]["time"])
    if P["pilot_only"]:
        wc = P["worst_case_pilot_core_h"]
    if P.get("t6_only"):
        wc = sum(int(t6["cpus"]) * hours(t6["time"]) for _ in P["fits"])
    P["worst_case_core_h"] = round(wc, 1)
    cap = P.get("core_h_cap")
    if cap is not None and wc > cap + 1e-9:
        raise PlanError("worst case %.1f billed core-h exceeds the plan's core_h_cap %.1f%s" % (wc, cap,
                        " (theory-mode island limits are scaled for the tier-1 N, see law_islands_time)" if any("islands_time_base" in f for f in P["fits"]) else ""))
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


# the restart-mode islands script leaves through exit 0 / 22 / rc: every attempt writes its end record (review PR62 m5), with
# the attempt number and the exit code, to the batch's ends.jsonl (beside starts.jsonl)
RESTART_END_TRAP = r'''end_record() { local rcx=$?; printf '{"stage":"islands","run_id":"%s","job":"%s","task":"%s","attempt":%s,"rc":%s,"end":"%s"}\n' "$RUN_ID" "${SLURM_JOB_ID}" "${SLURM_ARRAY_TASK_ID:-}" "$ATT" "$rcx" "$(date -u +%FT%TZ)" >> "$(dirname "$RUN")/ends.jsonl"; }
trap 'end_record; rm -rf "$TMPDIR"' EXIT   # replaces the header's trap: keep its TMPDIR cleanup
'''

SKIP_IF_OUTCOME = ('if [[ -e $RUN/OUTCOME ]]; then echo "prep outcome $(cat "$RUN/OUTCOME"): nothing to do"; '
                   'printf \'{{"stage":"%s","run_id":"%s","skipped":"prep_outcome"}}\\n\' "{stage}" "$RUN_ID" >> "$DEPT/scratch/runs/{batch}/ends.jsonl"; exit 0; fi\n')


# theory mode: after the fill, the island / merge manifest's N is set to calib.bin's frozen N, read at stage time (p1m_calib_n.py)
def set_n(manifest):
    return 'python3 "$SCR/p1m_calib_n.py" set-n --manifest %s --calib "$RUN/calib.bin.json"\n' % manifest


def stage_body(stage, restart=None, limit_s=0, theory=False):
    """Command lines of WP1's CLI (src/cli/main.cpp): --out names the .bin, the record is <out>.json; --manifest merges
    `params` into the arguments and refuses to start when an `inputs` path has a different content hash."""
    fill = 'python3 "$SCR/p1m_manifest.py" fill --template "$MAN/{cmd}.json" --out "$RUN/manifests/{cmd}{suffix}.json"'
    sn = (lambda m: set_n(m)) if theory else (lambda m: "")
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
                + run.format(cmd="calibrate", suffix="", extra=' --threads "$OMP_NUM_THREADS" --mem-budget "$MEMB" --cost-dir "$RUN/cost"', out="calib.bin")
                # theory mode: record the plan's N and calib.bin's frozen N in the run manifest (not fatal: the islands re-read calib.bin.json)
                + ('python3 "$SCR/p1m_calib_n.py" record-n --manifest "$MAN/calibrate.json" --calib "$RUN/calib.bin.json" '
                   '--run-manifest "$RUN/run_manifest.json" || echo "WARNING: could not record calib N_final in the run manifest" >&2\n' if theory else ""))
    if stage == "islands" and restart is not None and restart["attempts"] > 1:
        # WP7 O4: attempt ATT of A. A finished island exits at once; a failed one repeats its code; a soft stop (exit 22: the
        # island checkpointed at the first step boundary after limit - margin seconds) ends this attempt cleanly and the next
        # attempt resumes from island_<r>.ckpt.{a,b}; a task killed at its limit leaves its last periodic checkpoint
        A = restart["attempts"]; margin = int(restart["margin_s"])
        return ("R=${SLURM_ARRAY_TASK_ID}\nATT=${2:-1}\n" + RESTART_END_TRAP +
                'DONE="$RUN/island_$R.done"; FAILED="$RUN/island_$R.failed"\n'
                'if [[ -e $DONE ]]; then echo "island $R: already finished"; exit 0; fi\n'
                'if [[ -e $FAILED ]]; then rc=$(cat "$FAILED"); echo "island $R: failed in an earlier attempt (exit $rc)"; exit "$rc"; fi\n'
                + fill.format(cmd="island", suffix="_$R") + " --set params.id=$R\n" + sn('"$RUN/manifests/island_$R.json"')
                + "LIMIT_S=%d; MARGIN_S=%d\n" % (limit_s, margin)
                + 'STOP_S=$(( LIMIT_S - MARGIN_S - SECONDS )); [[ $STOP_S -ge 1 ]] || STOP_S=1   # SECONDS: since this script started\n'
                + 'mkdir -p "$RUN/log"; rc=0\n'
                + '"$BIN" island --manifest "$RUN/manifests/island_$R.json" --threads "$OMP_NUM_THREADS" --mem-budget "$MEMB" '
                  '--stop-after-s "$STOP_S" --out "$RUN/island_$R.bin" > "$RUN/log/island_$R.attempt$ATT.log" 2>&1 || rc=$?\n'
                + 'if [[ $rc == 0 ]]; then echo ok > "$DONE"; exit 0; fi\n'
                + 'if [[ $rc == 22 ]]; then echo "island $R: soft stop in attempt $ATT of %d (checkpoint written)"; [[ $ATT -lt %d ]] && exit 0 || exit 22; fi\n' % (A, A)
                + 'echo "$rc" > "$FAILED"; exit "$rc"\n')
    if stage == "islands":
        return ("R=${SLURM_ARRAY_TASK_ID}\n"
                + fill.format(cmd="island", suffix="_$R") + " --set params.id=$R\n" + sn('"$RUN/manifests/island_$R.json"')
                + run.format(cmd="island", suffix="_$R", extra=' --threads "$OMP_NUM_THREADS" --mem-budget "$MEMB"', out="island_$R.bin"))
    if stage == "merge":
        return (fill.format(cmd="merge", suffix="") + "\n" + sn('"$RUN/manifests/merge.json"')
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
    for st in ([] if P.get("t6_only") else (["setup"] if P["pilot_only"] else STAGES)):
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
        theory = any(f["mode"] != "V" for f in P["fits"]) and not P["pilot_only"]   # a pure V batch generates exactly what it always did
        if theory and st == "islands":
            f0 = P["fits"][0]
            if "islands_time_base" in f0:
                txt += ("# theory mode: time limit %s = base %s x ceil(4 max(2500, n, p) / N_plan), capped at 2 h (tier-1 N, requested up front:\n"
                        "# Slurm lets a user only lower a limit later). The islands' N is calib.bin.json's frozen N_final, read at stage time.\n"
                        % (r["time"], f0["islands_time_base"]))
        txt += stage_body(st, P.get("restart") if st == "islands" else None, int(hours(r["time"]) * 3600), theory)
        txt += 'printf \'{"stage":"%s","run_id":"%%s","job":"%%s","task":"%%s","end":"%%s"}\\n\' "$RUN_ID" "${SLURM_JOB_ID}" "${SLURM_ARRAY_TASK_ID:-}" "$(date -u +%%FT%%TZ)" >> "$DEPT/scratch/runs/%s/ends.jsonl"\n' % (st, batch)
        write(os.path.join(out, name), txt, 0o755)
        files.append(name)
        del n_per_fit
    if P.get("t6") is not None:   # WP7 O4: T6 by real kills on one island of a finished fit's inputs (p1m_t6.py)
        t6 = P["t6"]
        wc6 = sum(int(t6["cpus"]) * hours(t6["time"]) for _ in P["fits"])
        txt = HEADER.format(name="stage_t6.sbatch", batch=batch, stage="t6", wc=wc6, cpus=t6["cpus"], mem=t6["mem"], time=t6["time"],
                            dept=dept, binary=P["binary"], submitter="submit_t6.sh")
        txt += FIT_TABLE.format(runs=runs)
        txt += fit_selector(True).replace("{batch}", batch)
        txt += ('SRC=$DEPT/scratch/runs/%s/$RUN_ID   # the finished fit whose inputs T6 reuses\n'
                'for f in data.bin setup.bin calib.bin; do [[ -s $SRC/$f ]] || { echo "FATAL: $SRC/$f missing (run the source batch first)" >&2; exit 66; }; done\n'
                'SEED=$(python3 -c \'import json,sys; print(json.load(open(sys.argv[1]))["params"]["seed"])\' "$SCR/run_manifests/$RUN_ID.json")\n'
                'mkdir -p "$RUN/t6" "$RUN/log"\n'
                'python3 "$SCR/p1m_t6.py" --bin "$BIN" --data "$SRC/data.bin" --setup "$SRC/setup.bin" --calib "$SRC/calib.bin" --seed "$SEED" '
                '--island %d --threads "$OMP_NUM_THREADS" --mem-budget "$MEMB" --ckpt-every-s %s --kills %d --max-seconds %d '
                '--work "$RUN/t6" --out "$RUN/t6.json" > "$RUN/log/t6.log" 2>&1\n'
                % (t6["source_batch"], t6["island"], t6["ckpt_every_s"], t6["kills"], int(hours(t6["time"]) * 3600 - 300)))
        txt += 'printf \'{"stage":"t6","run_id":"%%s","job":"%%s","task":"%%s","end":"%%s"}\\n\' "$RUN_ID" "${SLURM_JOB_ID}" "${SLURM_ARRAY_TASK_ID:-}" "$(date -u +%%FT%%TZ)" >> "$DEPT/scratch/runs/%s/ends.jsonl"\n' % batch
        write(os.path.join(out, "stage_t6.sbatch"), txt, 0o755)
        files.append("stage_t6.sbatch")
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
        rm.update({k: P[k] for k in ("method_tag", "core_tree") if k in P})   # the freeze pin, when the plan has one
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
  ji=$("$SB" --parsable --array=1-$rp{thr} --dependency=afterok:${{jc}}_$i stage_islands.sbatch $i{att1}); log islands "${{RUNS[$((i-1))]}}" "$ji"{retry}
{isa_line}  jm=$("$SB" --parsable --dependency=afterok:$ji stage_merge.sbatch $i); log merge "${{RUNS[$((i-1))]}}" "$jm"
  je=$("$SB" --parsable --dependency=afterok:$jm stage_eval.sbatch $i); log eval "${{RUNS[$((i-1))]}}" "$je"
done
echo "submitted; ledger row: see ledger_row.md (fill job ids from $LOG)"
""".format(batch=batch, F=F, ntask=P["n_tasks"], wc=P["worst_case_core_h"], ncalls=2 + 3 * F, dept=dept,
           binary=P["binary"], runs=runs, thr=thr,
           att1=" 1" if (P.get("restart") or {}).get("attempts", 1) > 1 else "",
           retry=('\n  for att in $(seq 2 %d); do   # WP7 O4: the restart chain, each attempt after the previous array (afterany)\n'
                  '    ji=$("$SB" --parsable --array=1-$rp%s --dependency=afterany:$ji stage_islands.sbatch $i $att); log "islands_attempt$att" "${RUNS[$((i-1))]}" "$ji"\n'
                  '  done' % (P["restart"]["attempts"], thr)
                  if (P.get("restart") or {}).get("attempts", 1) > 1 else ""),
           portable_check=('[[ -x $SCR/bin/smcbvs4_isa_check ]] || { echo "FATAL: binary $SCR/bin/smcbvs4_isa_check missing (build.sh, D-32 isa_check)" >&2; exit 66; }\n'
                           if P.get("isa_check") is not None else ""),
           isa_line=('  jx=$("$SB" --parsable --dependency=afterok:$ji stage_isa_check.sbatch $i); log isa_check "${RUNS[$((i-1))]}" "$jx"\n'
                     if P.get("isa_check") is not None else ""))
    if not (P["pilot_only"] or P.get("t6_only")):   # a pilot-only / T6-only batch has no full-fit submit.sh (review PR55 MAJOR)
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
    if P.get("t6") is not None:   # submit_t6.sh: the T6 task array and nothing else
        pre = sub[:sub.index("RUNS=(")]
        pre = "\n".join(l for l in pre.split("\n")[1:] if not l.startswith(("# submit.sh", "# Job graph", "# sbatch calls")))
        sp = ("# submit_t6.sh -- P1M batch %s: T6 by real kills (WP7 O4), %d fit(s), worst case %.1f billed core-h. GENERATED (dry run).\n"
              % (batch, F, P["worst_case_core_h"]))
        sp += pre.replace('[[ -x $SCR/{binary} ]]'.format(binary=P["binary"]), '[[ -x $SCR/%s ]]' % P["binary"]) + "RUNS=(%s)\n" % runs
        sp += ('jt=$("$SB" --parsable --array=1-%d stage_t6.sbatch); log t6 all "$jt"\n'
               'echo "submitted T6; worst case %.1f core-h (ledger: fill job ids from $LOG)"\n' % (F, P["worst_case_core_h"]))
        write(os.path.join(out, "submit_t6.sh"), "#!/usr/bin/env bash\n" + sp, 0o755)
        files.append("submit_t6.sh")
    write(os.path.join(out, "fit_rp.txt"), "".join("%d\n" % f["Rp"] for f in P["fits"]))
    files.append("fit_rp.txt")
    # helper copied next to the scripts (stdlib-only Python, run on the compute node)
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "p1m_manifest.py")) as fh:
        write(os.path.join(out, "p1m_manifest.py"), fh.read(), 0o755)
    files.append("p1m_manifest.py")
    if any(f["mode"] != "V" for f in P["fits"]) and not (P["pilot_only"] or P.get("t6_only")):   # theory mode: N from calib.bin at stage time (a pure V batch is byte-identical to before)
        with open(os.path.join(here, "p1m_calib_n.py")) as fh:
            write(os.path.join(out, "p1m_calib_n.py"), fh.read(), 0o755)
        files.append("p1m_calib_n.py")
    if P.get("t6") is not None:   # T6 by real kills (WP7 O4): shipped only with a T6 batch (other batches are byte-identical to before)
        with open(os.path.join(here, "p1m_t6.py")) as fh:
            write(os.path.join(out, "p1m_t6.py"), fh.read(), 0o755)
        files.append("p1m_t6.py")
    with open(os.path.join(here, "p1m_stage_cost.py")) as fh:   # T5 report and the D-32 isa check (WP7 O5)
        write(os.path.join(out, "p1m_stage_cost.py"), fh.read(), 0o755)
    files.append("p1m_stage_cost.py")
    # ledger row
    now = P["created_utc"]
    row = ("| %s | %s (%d fits, %d tasks; dry run %s) | %s | (from submissions.jsonl) | %.1f | — | generated |\n"
           % (now[:10], batch, F, P["n_tasks"], now, P.get("kind", "gated (needs HQ go)"), P["worst_case_core_h"]))
    write(os.path.join(out, "ledger_row.md"), row)
    files.append("ledger_row.md")
    if P.get("warnings"):   # only for a plan with unknown keys: a clean plan's output is byte-identical to before
        write(os.path.join(out, "PLAN_WARNINGS.txt"), "The plan has keys this driver does not know (ignored; --strict refuses them):\n"
              + "".join("  - %s\n" % w for w in P["warnings"]))
        files.append("PLAN_WARNINGS.txt")
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
    ap.add_argument("--strict", action="store_true", help="refuse (exit 65) a plan that has keys the driver does not know, instead of warning")
    a = ap.parse_args(argv)
    # PR12 MINOR-8: resolved (symlink-free), absolute containment checks. --dept and --out must lie inside the
    # department folder; tests may use P1M_TEST_ROOT, itself inside $TMPDIR (never a bare prefix match).
    for what, path in (("--dept", a.dept), ("--out", a.out)):
        if not path_allowed(path):
            print("refusing: %s %s is outside the department folder (POLICIES §12)" % (what, path), file=sys.stderr)
            return 64
    try:
        with open(a.plan) as fh:
            plan = json.load(fh)
    except (OSError, ValueError) as e:   # missing, unreadable, not UTF-8 or not JSON: one clean line, exit 65
        print("plan error: cannot read the plan %s: %s" % (a.plan, str(e).replace("\n", " ")), file=sys.stderr)
        return 65
    try:
        P = resolve(plan)
        for w in P.get("warnings", []):
            print("plan warning: %s" % w, file=sys.stderr)
        if a.strict and P.get("warnings"):
            print("plan error: --strict: %d unknown plan key(s), see the warnings above" % len(P["warnings"]), file=sys.stderr)
            return 65
        P["created_utc"] = a.now or datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        files = generate(P, a.out, a.dept)
    except PlanError as e:
        print("plan error: %s" % e, file=sys.stderr)
        return 65
    print("dry run: wrote %d files to %s; %d fits, %d tasks, worst case %.1f billed core-h. Nothing was submitted."
          % (len(files), a.out, len(P["fits"]), P["n_tasks"], P["worst_case_core_h"])
          + ("" if not P.get("warnings") else " WARNING: %d unknown plan key(s), see PLAN_WARNINGS.txt." % len(P["warnings"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
