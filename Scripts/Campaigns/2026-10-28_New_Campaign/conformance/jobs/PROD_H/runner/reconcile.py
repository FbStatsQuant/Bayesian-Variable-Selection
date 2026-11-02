"""Classify every unit of a run (NOTS login node; Python 3.9 standard library only).

Usage: python3 reconcile.py RUN_DIR [--sacct] [--clear-stale-locks] [--full-verify]
Writes RUN_DIR/reconcile.tsv (atomically), RUN_DIR/p5_reconcile.tsv (only when a P5 array exists) and prints one JSON line of counts.
Importable: main(argv) returns the summary dict (poll.py uses it; all scheduler calls go through sched.run).

Job IDs (PROD-H): jobs.tsv lists the precompile job, the two primary arrays (primary_p1000: global tasks 1-600, primary_p500: 601-1200),
any reruns (rerun_N) and the P5 array. Task indices are GLOBAL (unique across the two primary arrays); a rerun re-uses the original
indices under its own job id. Only primary_* and rerun_* jobs take part in the primary classification; precompile and p5 are separate
(P5 is reported by p5_report(), its files live in <case>/P5_retry/ and never enter the primary counts).
Order matters: the squeue snapshot is taken FIRST, then sacct, then the files are read, so a task absent from the snapshot has already
written its end record.

Classes (primary units only):
  done          valid .done (sha256 of rds+csv match; cached by size+mtime unless --full-verify)
  pulled        .done/.sha256 kept but rds+csv deleted after a verified pull (the laptop receipt is authoritative)
  running       its last attempt has no end record and its task is running in that attempt's job
  rerun_queued  listed in a rerun's units file whose task is still pending/running (never selected again)
  timeout       the unit hit its hard kill (L + margin), or Slurm ended the task with State TIMEOUT: reported and held, never rerun
  infra         attempted, no .done, not timeout, not live: eligible for ONE rerun, same seed (node failure, OOM-kill, exit 1, no native status)
  infra_repeat  a second infrastructure failure: never rerun automatically; reported to HQ
  orphan        never attempted although its task is no longer queued in any job of the run (the task died before reaching this unit)
  not_run       never attempted; its task is still queued
Outcome (done units, from the CSV rows): ok (all rules ok/warning), resource_limit (native status; GO_2400 C5 "budget-censored", its own
category and never a failure), method_failed (any other failed native status).
event_utc (C3 window): the end (else start) of the FIRST attempt that did not finish the unit, else the finish of the attempt that did.
ever_infra: some attempt ended without .done and not by timeout, or a non-last attempt never wrote an end record.
--clear-stale-locks removes SMCBVS.lock of a dead unit (infra/infra_repeat/orphan/timeout) only when its task index is neither running
nor pending in ANY job of the run; each removal goes to LOGROOT/locks_cleared.jsonl (scratch).
"""
import csv
import hashlib
import json
import os
import re
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import nc_sched as sched  # noqa: E402  (scheduler access: tests substitute nc_sched.run)

PRIMARY_KIND = re.compile(r"^(primary_p(500|1000)|rerun_\d+)$")
LIVE_STATES = ("RUNNING", "COMPLETING", "CONFIGURING")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read_json(p):
    try:
        return json.loads(p.read_text())
    except (FileNotFoundError, json.JSONDecodeError):      # being written right now
        return None


def atomic_write(path, text):
    tmp = path.with_name(path.name + ".tmp.%d" % os.getpid())
    tmp.write_text(text)
    os.replace(tmp, path)


def sched_out(args, what, env=None):
    r = sched.run(args, env=env)
    if r.returncode != 0:
        raise SystemExit("%s failed (exit %s): %s" % (what, r.returncode, (r.stderr or "").strip()[:300]))
    return r.stdout


def make_done_valid(cache):
    def done_valid(key_id, prefix, names=None):
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
        if cache.get(key_id) == key:
            return True
        ok = all(sha(prefix.parent / n) == h for h, n in pairs)
        if ok:
            cache[key_id] = key
        return ok
    return done_valid


def p5_report(run_dir, cfg, out, live_jobs, done_valid):
    """P5 retry state of the units selected by p5_submit.sh (RUN_DIR/p5/units.tsv). Separate from the primary counts."""
    units_file = run_dir / "p5" / "units.tsv"
    if not units_file.exists():
        return None
    logroot = Path(cfg["LOGROOT"])
    rows = []
    for u in csv.DictReader(open(units_file, newline=""), delimiter="\t"):
        case = u["case_id"]
        prefix = out / "results" / cfg["RUN_ID"] / ("p%04d" % int(u["p"])) / case / "P5_retry" / "SMCBVS_p5retry"
        start = read_json(logroot / "p5_attempts" / (case + ".start.json"))
        end = read_json(logroot / "p5_attempts" / (case + ".end.json"))
        refused = (logroot / "p5_attempts" / (case + ".refused.jsonl")).exists()
        v3 = ""
        if done_valid("p5:" + case, prefix):
            state = "valid"
            rr = list(csv.DictReader(open(prefix.with_suffix(".csv"), newline="")))
            v3 = rr[0]["v3_status"]
        elif start is None:
            state = "not_started" if u["idx"] and live_jobs else "never_started"
        elif end is None:
            state = "running" if live_jobs else "incomplete"
        else:
            state = "incomplete"          # attempt ended without a valid .done (reported; never retried: one P5 attempt per unit, ever)
        rows.append(dict(idx=u["idx"], case_id=case, p=u["p"], state=state, retry_v3_status=v3,
                         exit=(end or {}).get("exit", ""), wall_s=(end or {}).get("wall_s", ""),
                         timed_out=str((end or {}).get("timed_out", "")).lower(), second_attempt_refused=str(refused).lower()))
    if rows:
        atomic_write(run_dir / "p5_reconcile.tsv", "\n".join(["\t".join(rows[0])] + ["\t".join(str(r[k]) for k in rows[0]) for r in rows]) + "\n")
    count = {s: sum(1 for r in rows if r["state"] == s) for s in sorted({r["state"] for r in rows})}
    return dict(units=len(rows), states=count,
                outcomes={v: sum(1 for r in rows if r["retry_v3_status"] == v) for v in sorted({r["retry_v3_status"] for r in rows}) if v})


def main(argv):
    run_dir = Path(argv[0]).resolve()
    use_sacct = "--sacct" in argv
    clear_locks = "--clear-stale-locks" in argv
    full_verify = "--full-verify" in argv
    if clear_locks and not use_sacct:
        raise SystemExit("--clear-stale-locks needs --sacct (live-job check)")
    cfg = dict(line.split("=", 1) for line in (run_dir / "config.env").read_text().split())
    out = Path(cfg["OUTROOT"])
    manifest = json.loads((run_dir / "manifest.json").read_text())

    # ---- 1. job IDs of the run, rerun units files ---------------------------------------------------------------
    jobs, rerun_units, all_jobs, p5_jobs = set(), {}, set(), set()
    if (run_dir / "jobs.tsv").exists():
        for r in csv.DictReader(open(run_dir / "jobs.tsv", newline=""), delimiter="\t"):
            if r["job"].isdigit():
                all_jobs.add(r["job"])
            if r["kind"] == "p5":
                p5_jobs.add(r["job"])
            if not PRIMARY_KIND.match(r["kind"]) or not r["job"].isdigit():
                continue                      # precompile and p5 are separate namespaces
            jobs.add(r["job"])
            if r["kind"].startswith("rerun_"):
                f = run_dir / r["kind"] / "units.txt"
                rerun_units[r["job"]] = set(f.read_text().split()) if f.exists() else set()
    jobs = sorted(jobs)

    # ---- 2. queue snapshot first, then accounting -----------------------------------------------------------------
    running_tasks, pending_tasks, steps, task_end, task_states = set(), set(), {}, {}, {}
    p5_live = False
    if use_sacct:
        # All of this user's queued tasks (-r expands pending ranges), filtered to the run's jobs.
        for line in sched_out(["squeue", "-h", "-r", "-u", "fb31", "-o", "%i|%T"], "squeue").split():
            jid, state = line.split("|")
            m = re.match(r"^(\d+)_(\d+)$", jid)
            if m and m.group(1) in jobs:
                (running_tasks if state in LIVE_STATES else pending_tasks).add((m.group(1), m.group(2)))
            if jid.split("_")[0] in p5_jobs:
                p5_live = True
        since = (datetime.fromisoformat(manifest["submitted_utc"]) - timedelta(days=1)).strftime("%Y-%m-%d")
        # TZ=UTC: sacct prints times in the local zone by default; attempt files are UTC ("...Z").
        text = sched_out(["sacct", "-S", since, "-j", ",".join(jobs), "-P", "-n", "-o",
                          "JobID,JobName,State,ExitCode,Elapsed,MaxRSS,NodeList,End"], "sacct", env=dict(os.environ, TZ="UTC"))
        for line in text.splitlines():
            jid, name, state, code, elapsed, maxrss, node, end = line.split("|")
            end = end + "Z" if re.match(r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d$", end) else ""
            m = re.match(r"^(\d+)_(\d+)\.(\d+)$", jid)          # a unit's srun step: ARRAYJOB_TASK.STEP
            if m:
                steps[(m.group(1), m.group(2), name)] = dict(state=state, exit=code, elapsed=elapsed, maxrss=maxrss, node=node, end=end)
            m = re.match(r"^(\d+)_(\d+)$", jid)                  # the whole array task
            if m:
                task_states[(m.group(1), m.group(2))] = state.split()[0].rstrip("+")
            if m and end and m.group(1) not in rerun_units:      # end of the ORIGINAL task (orphan event time)
                task_end[m.group(2)] = min(task_end.get(m.group(2), end), end)
    live = running_tasks | pending_tasks
    live_task_ids = {t for _, t in live}

    # ---- 3. files ---------------------------------------------------------------------------------------------
    cache_path = run_dir / "verify_cache.json"
    cache = {} if full_verify or not cache_path.exists() else json.loads(cache_path.read_text())
    done_valid = make_done_valid(cache)

    def attempts_of(case):
        d = Path(cfg["LOGROOT"]) / "attempts" / case
        res = []
        if d.exists():
            for p in sorted(d.glob("attempt_*.start.json"), key=lambda p: int(p.name.split("_")[1].split(".")[0])):
                s = read_json(p)
                if s is not None:
                    res.append((s, read_json(p.with_name(p.name.replace(".start", ".end")))))
        return res

    def lock_log(rec):
        with open(Path(cfg["LOGROOT"]) / "locks_cleared.jsonl", "a") as f:        # append-only execution log: scratch
            f.write(json.dumps(rec) + "\n")

    units = list(csv.DictReader(open(run_dir / "units.tsv", newline=""), delimiter="\t"))
    rows = []
    for u in units:
        case, task = u["case_id"], u["task"]
        prefix = out / "results" / cfg["RUN_ID"] / ("p%04d" % int(u["p"])) / case / "SMCBVS"
        att = attempts_of(case)
        last_start, last_end = att[-1] if att else (None, None)
        # Queued = listed in a rerun whose task is live AND that rerun job has not attempted this unit yet (otherwise a finished rerun
        # attempt, e.g. a timeout, would be masked while the same task runs its other unit).
        queued_rerun = any(case in us and ((j, task) in live) and not any(s.get("array_job") == j for s, _ in att)
                           for j, us in rerun_units.items())
        # Slurm can kill the entire task before an end record exists (including before the second scale starts). Never classify those
        # missing units as rerunnable: a task that ended in State TIMEOUT is a timeout.
        task_timed_out = any(t == task and state == "TIMEOUT" for (j, t), state in task_states.items()
                             if j not in rerun_units or (last_start and last_start.get("array_job") == j))
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
        elif (last_end is not None and last_end.get("timed_out")) or task_timed_out:
            klass = "timeout"
        elif att:
            failed = sum(1 for s, e in att if not (e and e.get("done")))
            klass = "infra_repeat" if failed >= 2 else "infra"
        else:
            klass = "not_run" if (not use_sacct or task in live_task_ids) else "orphan"
        # C3 event time and infra history.
        event, ever_infra = "", False
        for i, (s, e) in enumerate(att):
            last = i == len(att) - 1
            if e is None and last and klass == "running":
                break
            if not (e and e.get("done")):
                if klass != "timeout" and (e is None or not e.get("timed_out")):
                    ever_infra = True
                if not event:
                    st = steps.get((s["array_job"], s["task"], case), {})
                    event = (e or {}).get("finished_utc") or st.get("end") or s["started_utc"]   # all UTC "...Z"
            elif not event:
                event = e["finished_utc"]
        # An orphan (its task died before reaching it) is an infrastructure failure, also after its first attempt has run inside a
        # rerun job; its event is the end of the original task.
        if klass == "orphan" or (att and att[0][0].get("array_job") in rerun_units):
            ever_infra = True
            event = task_end.get(task) or (att[0][0]["started_utc"] if att else "")
        if klass == "timeout" and not event:
            event = task_end.get(task, "")
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

    lines = ["\t".join(rows[0])] + ["\t".join(str(r[k]) for k in rows[0]) for r in rows]
    atomic_write(run_dir / "reconcile.tsv", "\n".join(lines) + "\n")
    p5 = p5_report(run_dir, cfg, out, p5_live, done_valid)
    atomic_write(cache_path, json.dumps(cache))
    count = lambda key: {v: sum(1 for r in rows if r[key] == v) for v in sorted({r[key] for r in rows}) if v}
    by_array = {}
    for r in rows:
        a = by_array.setdefault("p" + r["p"], {})
        a[r["klass"]] = a.get(r["klass"], 0) + 1
    summary = dict(run=cfg["RUN_ID"], jobs=jobs, units=len(rows), classes=count("klass"), by_array=by_array, outcomes=count("outcome"),
                   escalated=sum(r["escalated"] == "true" for r in rows),
                   ever_infra=sum(r["ever_infra"] == "true" for r in rows),
                   locks_cleared=sum(r["lock_cleared"] == "true" for r in rows),
                   running_tasks=len(running_tasks), pending_tasks=len(pending_tasks))
    if p5 is not None:
        summary["p5"] = p5
    return summary


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    print(json.dumps(main(sys.argv[1:])))
