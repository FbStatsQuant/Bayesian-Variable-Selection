"""Classify every unit of a run (NOTS login node; Python 3.9 standard library only).

Usage: python3 reconcile.py RUN_DIR [--sacct] [--clear-stale-locks] [--full-verify]
Writes RUN_DIR/reconcile.tsv (atomically) and prints one JSON line of counts.

Job IDs: every array job of the run (GO_2400 C4) = manifest.json + RUN_DIR/jobs.tsv (original + reruns).
Order matters (review R3): the squeue snapshot is taken FIRST, then sacct, then the files are read, so a
task that is absent from the snapshot has already written its end record.

Classes (ASSUMPTIONS.md 4-5):
  done          valid .done (sha256 of rds+csv match; cached by size+mtime unless --full-verify)
  pulled        .done/.sha256 kept but rds+csv deleted after a verified pull (laptop receipt is authoritative)
  running       its last attempt has no end record and its task is running in that attempt's job
  rerun_queued  listed in a rerun's units file whose task is still pending/running (never selected again)
  timeout       last attempt hit the hard kill (L + margin): a recorded non-recovery, never rerun
  infra         attempted, no .done, not timeout, not live: eligible for ONE rerun, same seed
  infra_repeat  a second infrastructure failure: never rerun automatically; reported to HQ
  orphan        never attempted although its task is no longer queued in any job of the run (the task
                died before reaching this unit): rerun as a FIRST attempt (review R1)
  not_run       never attempted; its task is still queued
Outcome (done units, from the CSV rows): ok (all rules ok/warning), resource_limit (native status;
GO_2400 C5 "budget-censored", its own category), method_failed (any other failed native status).
event_utc (C3 window, review R4): the end (else start) of the FIRST attempt that did not finish the unit,
else the finish of the attempt that did.  ever_infra: some attempt ended without .done and not by timeout,
or a non-last attempt never wrote an end record.
--clear-stale-locks removes SMCBVS.lock of a dead unit (infra/infra_repeat/orphan/timeout) only when its
task index is neither running nor pending in ANY job of the run; each removal goes to locks_cleared.jsonl.
"""
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

run_dir = Path(sys.argv[1]).resolve()
use_sacct = "--sacct" in sys.argv
clear_locks = "--clear-stale-locks" in sys.argv
full_verify = "--full-verify" in sys.argv
if clear_locks and not use_sacct:
    raise SystemExit("--clear-stale-locks needs --sacct (live-job check)")
cfg = dict(line.split("=", 1) for line in (run_dir / "config.env").read_text().split())
out = Path(cfg["OUTROOT"])
manifest = json.loads((run_dir / "manifest.json").read_text())

# ---- 1. job IDs of the run, rerun units files --------------------------------------------------
jobs, rerun_units = {manifest["slurm_job_id"].split(";")[0]}, {}
if (run_dir / "jobs.tsv").exists():
    for r in csv.DictReader(open(run_dir / "jobs.tsv"), delimiter="\t"):
        jobs.add(r["job"])
        if r["kind"].startswith("rerun_"):
            f = run_dir / r["kind"] / "units.txt"
            rerun_units[r["job"]] = set(f.read_text().split()) if f.exists() else set()
jobs = sorted(j for j in jobs if j.isdigit())

# ---- 2. queue snapshot first, then accounting -----------------------------------------------------
running_tasks, pending_tasks, steps, task_end = set(), set(), {}, {}
if use_sacct:
    # All of this user's queued tasks (-r expands pending ranges), filtered to the run's jobs.
    q = subprocess.run(["squeue", "-h", "-r", "-u", "fb31", "-o", "%i|%T"], capture_output=True, text=True, check=True)
    for line in q.stdout.split():
        jid, state = line.split("|")
        m = re.match(r"^(\d+)_(\d+)$", jid)
        if m and m.group(1) in jobs:
            (running_tasks if state in ("RUNNING", "COMPLETING", "CONFIGURING") else pending_tasks).add((m.group(1), m.group(2)))
    since = (datetime.fromisoformat(manifest["submitted_utc"]) - timedelta(days=1)).strftime("%Y-%m-%d")
    # TZ=UTC: sacct prints times in the local zone (CDT) by default; attempt files are UTC ("...Z").
    r = subprocess.run(["sacct", "-S", since, "-j", ",".join(jobs), "-P", "-n", "-o",
                        "JobID,JobName,State,ExitCode,Elapsed,MaxRSS,NodeList,End"], capture_output=True, text=True,
                       check=True, env=dict(os.environ, TZ="UTC"))
    for line in r.stdout.splitlines():
        jid, name, state, code, elapsed, maxrss, node, end = line.split("|")
        end = end + "Z" if re.match(r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d$", end) else ""
        m = re.match(r"^(\d+)_(\d+)\.(\d+)$", jid)          # a unit's srun step: ARRAYJOB_TASK.STEP
        if m:
            steps[(m.group(1), m.group(2), name)] = dict(state=state, exit=code, elapsed=elapsed, maxrss=maxrss, node=node, end=end)
        m = re.match(r"^(\d+)_(\d+)$", jid)                  # the whole array task
        if m and end and m.group(1) not in rerun_units:      # end of the ORIGINAL task (orphan event time)
            task_end[m.group(2)] = min(task_end.get(m.group(2), end), end)
live = running_tasks | pending_tasks
live_task_ids = {t for _, t in live}


# ---- 3. files --------------------------------------------------------------------------------------
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


cache_path = run_dir / "verify_cache.json"
cache = {} if full_verify or not cache_path.exists() else json.loads(cache_path.read_text())


def done_valid(case, prefix):
    d, s = prefix.with_suffix(".done"), prefix.with_suffix(".sha256")
    if not (d.exists() and s.exists()):
        return False
    pairs = [line.split("  ", 1) for line in s.read_text().splitlines()]
    if {n for _, n in pairs} != {prefix.name + ".rds", prefix.name + ".csv"}:
        return False
    files = [prefix.parent / n for _, n in pairs]
    if not all(f.exists() for f in files):
        return False
    key = [s.read_text()] + [[f.stat().st_size, f.stat().st_mtime_ns] for f in files]
    if cache.get(case) == key:
        return True
    ok = all(sha(prefix.parent / n) == h for h, n in pairs)
    if ok:
        cache[case] = key
    return ok


def read_json(p):
    try:
        return json.loads(p.read_text())
    except (FileNotFoundError, json.JSONDecodeError):      # being written right now (review R10)
        return None


def attempts_of(case):
    d = out / "attempts" / case
    res = []
    if d.exists():
        for p in sorted(d.glob("attempt_*.start.json"), key=lambda p: int(p.name.split("_")[1].split(".")[0])):
            s = read_json(p)
            if s is not None:
                res.append((s, read_json(p.with_name(p.name.replace(".start", ".end")))))
    return res


def lock_log(rec):
    with open(run_dir / "locks_cleared.jsonl", "a") as f:
        f.write(json.dumps(rec) + "\n")


units = list(csv.DictReader(open(run_dir / "units.tsv"), delimiter="\t"))
rows = []
for u in units:
    case, task = u["case_id"], u["task"]
    prefix = out / "results" / cfg["RUN_ID"] / ("p%04d" % int(u["p"])) / case / "SMCBVS"
    att = attempts_of(case)
    last_start, last_end = att[-1] if att else (None, None)
    # Queued = listed in a rerun whose task is live AND that rerun job has not attempted this unit yet
    # (review N1: otherwise a finished rerun attempt, e.g. a timeout, would be masked while the same
    # task runs its other unit).
    queued_rerun = any(case in us and ((j, task) in live) and not any(s.get("array_job") == j for s, _ in att)
                       for j, us in rerun_units.items())
    native = statuses = runtime = codes = escalated = outcome = ""
    if done_valid(case, prefix):
        klass = "done"
        rr = list(csv.DictReader(open(prefix.with_suffix(".csv"), newline="")))
        statuses = ",".join(x["rule_id"] + "=" + x["status"] for x in rr)
        native, runtime, codes = rr[0]["v3_status"], rr[0]["runtime_s"], rr[0]["diag_codes"]
        escalated = str("escalated" in codes.split(";")).lower()
        outcome = ("resource_limit" if native == "resource_limit" else
                   "ok" if all(x.endswith(("=ok", "=warning")) for x in statuses.split(",")) else "method_failed")
    elif (prefix.with_suffix(".done").exists() and prefix.with_suffix(".sha256").exists()
          and not prefix.with_suffix(".rds").exists() and not prefix.with_suffix(".csv").exists()):
        klass = "pulled"
    elif last_start and last_end is None and (not use_sacct or (last_start["array_job"], last_start["task"]) in running_tasks):
        klass = "running"          # without sacct the state is unknown and never treated as rerunnable
    elif queued_rerun:
        klass = "rerun_queued"
    elif last_end is not None and last_end.get("timed_out"):
        klass = "timeout"
    elif att:
        failed = sum(1 for s, e in att if not (e and e.get("done")))
        klass = "infra_repeat" if failed >= 2 else "infra"
    else:
        klass = "not_run" if (not use_sacct or task in live_task_ids) else "orphan"
    # C3 event time and infra history (review R4).
    event, ever_infra = "", False
    for i, (s, e) in enumerate(att):
        last = i == len(att) - 1
        if e is None and last and klass == "running":
            break
        if not (e and e.get("done")):
            if e is None or not e.get("timed_out"):
                ever_infra = True
            if not event:
                st = steps.get((s["array_job"], s["task"], case), {})
                event = (e or {}).get("finished_utc") or st.get("end") or s["started_utc"]   # all UTC "...Z"
        elif not event:
            event = e["finished_utc"]
    # Review N2: an orphan (its task died before reaching it) is an infrastructure failure, also after its
    # first attempt has run inside a rerun job; its event is the end of the original task.
    if klass == "orphan" or (att and att[0][0].get("array_job") in rerun_units):
        ever_infra = True
        event = task_end.get(task) or (att[0][0]["started_utc"] if att else "")
    # Stale-lock clearance (only with live-job information).
    lock = prefix.with_suffix(".lock")
    lock_cleared = False
    if clear_locks and lock.is_dir() and klass in ("infra", "infra_repeat", "orphan", "timeout") and task not in live_task_ids:
        owner = (lock / "owner.txt").read_text() if (lock / "owner.txt").exists() else ""
        shutil.rmtree(lock)
        lock_cleared = True
        lock_log(dict(utc=datetime.now(timezone.utc).isoformat(), case_id=case, klass=klass,
                      lock=str(lock), owner=owner, jobs_checked=jobs))
    st = steps.get((last_start["array_job"], last_start["task"], case), {}) if last_start else {}
    rows.append(dict(case_id=case, p=u["p"], task=task, klass=klass, outcome=outcome, escalated=escalated,
                     attempts=len(att), ever_infra=str(ever_infra).lower(), event_utc=event,
                     last_job=(last_start or {}).get("array_job", ""),
                     last_exit="" if last_end is None else last_end["exit"],
                     wall_s="" if last_end is None else last_end["wall_s"],
                     step_state=st.get("state", ""), step_maxrss=st.get("maxrss", ""),
                     step_elapsed=st.get("elapsed", ""), node=st.get("node", ""),
                     native=native, statuses=statuses, diag_codes=codes, runtime_s=runtime,
                     lock_present=str(lock.is_dir()).lower(), lock_cleared=str(lock_cleared).lower()))


def atomic_write(path, text):
    tmp = path.with_name(path.name + ".tmp.%d" % os.getpid())
    tmp.write_text(text)
    os.replace(tmp, path)


lines = ["\t".join(rows[0])] + ["\t".join(str(r[k]) for k in rows[0]) for r in rows]
atomic_write(run_dir / "reconcile.tsv", "\n".join(lines) + "\n")
atomic_write(cache_path, json.dumps(cache))
count = lambda key: {v: sum(1 for r in rows if r[key] == v) for v in sorted({r[key] for r in rows}) if v}
print(json.dumps(dict(run=cfg["RUN_ID"], jobs=jobs, units=len(rows), classes=count("klass"), outcomes=count("outcome"),
                      escalated=sum(r["escalated"] == "true" for r in rows),
                      ever_infra=sum(r["ever_infra"] == "true" for r in rows),
                      locks_cleared=sum(r["lock_cleared"] == "true" for r in rows),
                      running_tasks=len(running_tasks), pending_tasks=len(pending_tasks))))
