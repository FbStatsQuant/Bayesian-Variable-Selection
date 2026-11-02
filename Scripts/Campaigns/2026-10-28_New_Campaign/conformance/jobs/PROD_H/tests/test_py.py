"""Python-side dry-run tests of PROD-H: reconcile.py (two arrays, global indices, P5 separate, the five fabricated outcomes), the C3 stop rule
of poll.py, and accounting_summary.py. The scheduler is replaced in process (nc_sched.run); no Slurm, no NOTS.

    py -3 test_py.py WORKDIR        exit 0 if every case passes; prints one PASS/FAIL line per case
"""
import csv
import json
import shutil
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parent
sys.path.insert(0, str(BUNDLE / "runner"))
sys.path.insert(0, str(HERE))
import accounting_summary  # noqa: E402
import fabricate  # noqa: E402
import nc_sched  # noqa: E402
import poll  # noqa: E402
import reconcile  # noqa: E402

PASS = FAIL = 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print("PASS  " + name)
    else:
        FAIL += 1
        print("FAIL  %s  %s" % (name, detail))


class Res:
    def __init__(self, out="", rc=0, err=""):
        self.stdout, self.returncode, self.stderr = out, rc, err


class Sched:
    """Fake scheduler: live = {task: state} for jobs 7002/7003; task_states = {job_task: SLURM state} for sacct rows.
    held = job ids / job_task ids already held. scontrol hold J: fail_hold = {J: rc} (non-zero, no effect); noeffect = {J} (rc 0, nothing held);
    partial = {J: k} (rc 0, only the first k pending tasks held); otherwise every pending task of J is held."""

    def __init__(self, live=None, task_states=None, held=(), fail_hold=None, noeffect=(), partial=None):
        self.live, self.task_states, self.held, self.calls = live or {}, task_states or {}, set(held), []
        self.fail_hold, self.noeffect, self.partial = dict(fail_hold or {}), set(noeffect), dict(partial or {})

    def run(self, args, env=None):
        self.calls.append(list(args))
        if args[0] == "squeue":
            fmt = args[args.index("-o") + 1]
            rows = []
            for task, state in self.live.items():
                job = "7002" if int(task) <= 600 else "7003"
                held = state == "PENDING" and ((job + "_" + str(task)) in self.held or job in self.held)
                vals = {"%i": "%s_%s" % (job, task), "%T": state, "%r": "JobHeldUser" if held else "None"}
                rows.append("|".join(vals[t] for t in fmt.split("|")))
            return Res("\n".join(rows) + ("\n" if rows else ""))
        if args[0] == "sacct":
            rows = []
            for jt, st in self.task_states.items():
                rows.append("%s|smcbvs|%s|0:0|01:00:00||node1|2026-10-29T13:00:00" % (jt, st))
            return Res("\n".join(rows) + ("\n" if rows else ""))
        if args[0] == "scontrol":
            job = args[2]
            if args[1] == "release":
                self.held = {h for h in self.held if not h.startswith(job)}
                return Res("")
            if job in self.fail_hold:
                return Res("", self.fail_hold[job], "slurm_update error: Socket timed out on send/recv operation")
            if job in self.noeffect:
                return Res("")
            if job in self.partial:
                pend = [t for t, st in sorted(self.live.items()) if st == "PENDING" and (("7002" if int(t) <= 600 else "7003") == job)]
                self.held |= {"%s_%s" % (job, t) for t in pend[:self.partial[job]]}
                return Res("")
            self.held.add(job)
            return Res("")
        raise AssertionError("unexpected scheduler call " + " ".join(args))

    def scontrol(self):
        return [c for c in self.calls if c[0] == "scontrol"]


def logs_of(run):
    cfg = dict(l.split("=", 1) for l in (run / "config.env").read_text().split())
    return Path(cfg["LOGROOT"])


def make_run(root: Path, name, spec, extra_jobs=()):
    run = root / name
    scr = root / (name + "_scr")
    logs = scr / "logs" / (name)
    run.mkdir(parents=True)
    logs.mkdir(parents=True)
    (run / "config.env").write_text("RUN_ID=%s\nOUTROOT=%s\nLOGROOT=%s\n" % (name, scr, logs))
    shutil.copy(BUNDLE / "tables" / "units.tsv", run / "units.tsv")
    shutil.copy(BUNDLE / "tables" / "chunks.tsv", run / "chunks.tsv")
    (run / "manifest.json").write_text(json.dumps({"submitted_utc": "2026-10-29T11:00:00+00:00"}))
    (run / "jobs.tsv").write_text("job\tkind\tsubmitted_utc\tarray\tunits\n7001\tprecompile\tx\t-\t1\n7002\tprimary_p1000\tx\t1-600%50\t1200\n"
                                  "7003\tprimary_p500\tx\t601-1200%50\t1200\n" + "".join(extra_jobs))
    (root / (name + "_spec.json")).write_text(json.dumps(spec))
    n = fabricate.main(run, spec)
    return run, n


def klass(run):
    with open(run / "reconcile.tsv", newline="") as f:
        return {r["case_id"]: r for r in csv.DictReader(f, delimiter="\t")}


def units(run):
    return [r["case_id"] for r in csv.DictReader(open(run / "units.tsv", newline=""), delimiter="\t")]


def t_reconcile(root):
    # the first 14 units = p1000 tasks 1-7 (c100, c050)
    cases = units(root / "x") if False else [r["case_id"] for r in csv.DictReader(open(BUNDLE / "tables" / "units.tsv", newline=""), delimiter="\t")]
    modes = {cases[0]: "ok", cases[1]: "resource_limit", cases[2]: "method_failed", cases[3]: "escalated", cases[4]: "infra",
             cases[6]: "infra_repeat", cases[8]: "hardtimeout", cases[10]: "running", cases[12]: "none", cases[13]: "infra_then_ok",
             cases[14]: "stalelock"}
    spec = dict(default="none", limit=16, modes=modes)
    # --- scenario A: tasks of units 10/11 (task 6) running, every task >= 7 pending (not yet reached) ---
    live = {6: "RUNNING"}
    live.update({t: "PENDING" for t in range(7, 1201)})
    run, n = make_run(root, "T_reconA", spec)
    s = Sched(live=live, task_states={"7002_5": "COMPLETED", "7002_7": "COMPLETED"})
    nc_sched.run = s.run
    out = reconcile.main([str(run), "--sacct"])
    k = klass(run)
    cl = lambda i: k[cases[i]]["klass"]
    check("reconcile: completed unit -> done / ok", cl(0) == "done" and k[cases[0]]["outcome"] == "ok", cl(0))
    check("reconcile: native resource_limit -> done, outcome resource_limit (its own category, not method_failed)",
          cl(1) == "done" and k[cases[1]]["outcome"] == "resource_limit")
    check("reconcile: other native failure -> outcome method_failed", k[cases[2]]["outcome"] == "method_failed")
    check("reconcile: escalated flag read from diag_codes", k[cases[3]]["escalated"] == "true")
    check("reconcile: attempt ended without .done -> infra (ever_infra)", cl(4) == "infra" and k[cases[4]]["ever_infra"] == "true")
    check("reconcile: two failed attempts -> infra_repeat", cl(6) == "infra_repeat")
    check("reconcile: unit hard kill (exit 124, timed_out) -> timeout, not infrastructure",
          cl(8) == "timeout" and k[cases[8]]["ever_infra"] == "false")
    check("reconcile: attempt without end record, task running -> running", cl(10) == "running")
    check("reconcile: never attempted and task still queued -> not_run", cl(12) == "not_run" and cases[100] in k and k[cases[100]]["klass"] == "not_run")
    check("reconcile: failed attempt then ok in a rerun job -> done, ever_infra true", cl(13) == "done" and k[cases[13]]["ever_infra"] == "true")
    check("reconcile: global indices: p1000 tasks 1-600 and p500 tasks 601-1200 both classified",
          {k[c]["p"] for c in k} == {"500", "1000"} and out["units"] == 2400 and set(out["by_array"]) == {"p1000", "p500"})
    # --- scenario B: nothing queued: missing units are orphans; Slurm TIMEOUT and NODE_FAIL tasks ---
    run, n = make_run(root, "T_reconB", dict(default="none", limit=16, modes={cases[0]: "ok", cases[1]: "ok"}))
    s = Sched(live={}, task_states={"7002_3": "TIMEOUT", "7002_4": "NODE_FAIL", "7002_1": "COMPLETED"})
    nc_sched.run = s.run
    out = reconcile.main([str(run), "--sacct"])
    k = klass(run)
    # unit index 4,5 = task 3 ; 6,7 = task 4
    check("reconcile: missing outputs with Slurm State TIMEOUT -> timeout (reported, never an infrastructure rerun)",
          k[cases[4]]["klass"] == "timeout" and k[cases[4]]["ever_infra"] == "false" and k[cases[5]]["klass"] == "timeout")
    check("reconcile: missing outputs, no native status, NODE_FAIL / not queued -> orphan (infrastructure, rerunnable)",
          k[cases[6]]["klass"] == "orphan" and k[cases[6]]["ever_infra"] == "true")
    check("reconcile: orphan count = every unit not fabricated, not timeout", out["classes"]["orphan"] == 2400 - 2 - 2, str(out["classes"]))
    # --- scenario C: stale lock cleared only when the task is not live ---
    run, n = make_run(root, "T_reconC", dict(default="none", limit=2, modes={cases[0]: "stalelock", cases[1]: "ok"}))
    lock = Path(dict(l.split("=", 1) for l in (run / "config.env").read_text().split())["OUTROOT"]) / "results" / "T_reconC" / "p1000" / cases[0] / "SMCBVS.lock"
    nc_sched.run = Sched(live={1: "RUNNING"}).run
    reconcile.main([str(run), "--sacct", "--clear-stale-locks"])
    still = lock.is_dir()
    nc_sched.run = Sched(live={}).run
    reconcile.main([str(run), "--sacct", "--clear-stale-locks"])
    check("reconcile: stale lock kept while its task is live, cleared (and logged) once it is not",
          still and not lock.is_dir() and (logs_of(run) / "locks_cleared.jsonl").exists() and not (run / "locks_cleared.jsonl").exists())
    # --- scenario D: P5 reported separately, never in the primary counts ---
    cfg = dict(l.split("=", 1) for l in (root / "T_reconA" / "config.env").read_text().split())
    rl = cases[1]
    scr = Path(cfg["OUTROOT"])
    nc_sched.run = Sched(live=live, task_states={"7002_5": "COMPLETED", "7002_7": "COMPLETED"}).run
    before = reconcile.main([str(root / "T_reconA"), "--sacct"])
    (root / "T_reconA" / "p5").mkdir()
    (root / "T_reconA" / "p5" / "units.tsv").write_text("idx\tcase_id\tdataset\tscale\tp\tL\n1\t%s\t%s\tc050\t1000\t24000\n2\t%s\t%s\tc100\t1000\t24000\n"
                                                         % (rl, rl.rsplit("_", 1)[0], cases[2], cases[2].rsplit("_", 1)[0]))
    fabricate.write_result(scr / "results" / "T_reconA" / "p1000" / rl / "P5_retry" / "SMCBVS_p5retry", "completed", "ok")
    att = Path(cfg["LOGROOT"]) / "p5_attempts"
    att.mkdir(parents=True)
    (att / (rl + ".start.json")).write_text("{}")
    (att / (rl + ".end.json")).write_text('{"exit":0,"wall_s":5,"timed_out":false,"done":true}')
    (att / (cases[2] + ".start.json")).write_text("{}")
    (att / (cases[2] + ".end.json")).write_text('{"exit":1,"wall_s":5,"timed_out":false,"done":false}')
    (root / "T_reconA" / "jobs.tsv").write_text((root / "T_reconA" / "jobs.tsv").read_text() + "7020\tp5\tx\t1-2%2\t2\n")
    nc_sched.run = Sched(live=live, task_states={"7002_5": "COMPLETED", "7002_7": "COMPLETED"}).run
    after = reconcile.main([str(root / "T_reconA"), "--sacct"])
    check("reconcile: P5 retry files (valid / incomplete) are reported under 'p5' and leave the primary classes and outcomes unchanged",
          after["p5"]["states"] == {"incomplete": 1, "valid": 1} and after["p5"]["outcomes"] == {"completed": 1}
          and after["classes"] == before["classes"] and after["outcomes"] == before["outcomes"], str(after.get("p5")) + str(before["classes"]) + str(after["classes"]))
    check("reconcile: p5_reconcile.tsv written; the P5 job id is not part of the primary job list",
          (root / "T_reconA" / "p5_reconcile.tsv").exists() and "7020" not in after["jobs"])


def build_poll_run(root, name, modes, n_ok=250, extra=None):
    cases = [r["case_id"] for r in csv.DictReader(open(BUNDLE / "tables" / "units.tsv", newline=""), delimiter="\t")]
    md = {cases[i]: m for i, m in modes.items()}
    spec = dict(default="ok", limit=n_ok, modes=md)
    run, n = make_run(root, name, spec)
    # all tasks of unfabricated units pending in the queue
    first_free = (n_ok + 1) // 2 + 1
    live = {t: "PENDING" for t in range(first_free, 1201)}
    return run, cases, live


def t_poll(root):
    def go(name, modes, n_ok=250, extra_live=None, **kw):
        run, cases, live = build_poll_run(root, name, modes, n_ok)
        live.update(extra_live or {})
        s = Sched(live=live, held=kw.get("held", ()))
        nc_sched.run = s.run
        return run, cases, s, poll.main([str(run)])
    run, cases, s, rec = go("T_poll0", {})
    check("poll: 250 clean finished units -> continue, no hold", rec["decision"] == "continue" and not s.scontrol()
          and rec["counts"]["finished"] == 250 and rec["window"]["size"] == 200, str(rec["decision"]))
    run, cases, s, rec = go("T_poll1", {50: "resource_limit"})
    check("poll C3: a resource_limit inside the first 200 finished -> HOLD of both primary arrays only",
          rec["decision"] == "HOLD" and sorted(c[2] for c in s.scontrol()) == ["7002", "7003"] and all(c[1] == "hold" for c in s.scontrol()),
          str(s.scontrol()))
    check("poll C3: never cancels; HOLD.json and a request for HQ are written",
          not any(c[0] == "scancel" for c in s.calls) and (run / "HOLD.json").exists() and list(run.glob("HQ_REQUEST_*.md")))
    run, cases, s, rec = go("T_poll2", {50: "hardtimeout"})
    check("poll C3: a timeout inside the first 200 -> HOLD", rec["decision"] == "HOLD" and rec["counts"]["timeout"] == 1)
    run, cases, s, rec = go("T_poll3", {i: "infra" for i in (10, 20, 30, 40)})
    check("poll C3: 4 infrastructure failures in the first 200 -> continue (limit is more than 4)",
          rec["decision"] == "continue" and rec["counts"]["ever_infra"] == 4 and rec["window"]["infra_limit"] == 4)
    run, cases, s, rec = go("T_poll4", {i: "infra" for i in (10, 20, 30, 40, 50)})
    check("poll C3: 5 infrastructure failures in the first 200 -> HOLD", rec["decision"] == "HOLD" and rec["window"]["ever_infra"] == 5)
    run, cases, s, rec = go("T_poll5", {230: "resource_limit", 240: "hardtimeout", **{i: "infra" for i in range(205, 215)}})
    check("poll C3: failures AFTER the first 200 finished units are counted but do not trigger",
          rec["decision"] == "continue" and rec["counts"]["resource_limit"] == 1 and rec["counts"]["timeout"] == 1 and rec["counts"]["ever_infra"] == 10,
          str(rec["decision"]) + str(rec["counts"]))
    run, cases, s, rec = go("T_poll6", {10: "resource_limit"}, n_ok=60)
    check("poll C3: fewer than 200 finished units: fires as soon as it is certain (60 finished, one resource_limit)",
          rec["decision"] == "HOLD" and rec["window"]["size"] == 60)
    # acknowledgement: STILL_HELD, no second hold, then HOLD_RELEASED
    run, cases, s, rec = go("T_poll7", {50: "resource_limit"})
    n1 = len(s.scontrol())
    nc_sched.run = s.run
    rec2 = poll.main([str(run)])
    check("poll C3: after a HOLD the next poll reports STILL_HELD and does not hold again", rec2["decision"] == "STILL_HELD" and len(s.scontrol()) == n1)
    (run / "HOLD_RELEASED.json").write_text(json.dumps({"acknowledged": [cases[50]]}))
    rec3 = poll.main([str(run)])
    check("poll C3: HOLD_RELEASED.json acknowledges the unit; the poll returns to continue", rec3["decision"] == "continue", rec3["decision"])
    check("poll: report carries finished / escalated / resource_limit / timeout / infrastructure counts per array",
          {"finished", "escalated", "resource_limit", "timeout", "ever_infra"} <= set(rec["counts"]) and set(rec["by_p"]) == {"1000", "500"})
    check("poll: every poll appends one JSON line to LOGROOT/polls.jsonl (scratch; home keeps only poll_latest.json)", len((logs_of(run) / "polls.jsonl").read_text().splitlines()) == 3 and not (run / "polls.jsonl").exists()
          and (run / "poll_latest.json").exists())


def t_poll_hold(root):
    """R2-1: the C3 hold is tracked per job, confirmed from squeue, persisted, retried and escalated."""
    cases = [r["case_id"] for r in csv.DictReader(open(BUNDLE / "tables" / "units.tsv", newline=""), delimiter="\t")]

    def go(name, sched_kw=None, modes=None):
        run, _, live = build_poll_run(root, name, modes if modes is not None else {50: "resource_limit"})
        s = Sched(live=live, **(sched_kw or {}))
        nc_sched.run = s.run
        return run, s, live

    state_of = lambda run: json.loads((run / "hold_state.json").read_text())
    holds = lambda s: [c[2] for c in s.scontrol() if c[1] == "hold"]
    # an established hold
    run, s, live = go("T_hold_ok")
    rec = poll.main([str(run)])
    st = state_of(run)
    check("poll hold: both primary jobs held and CONFIRMED from squeue -> HOLD, hold_established, hold_state.json persisted, not urgent",
          rec["decision"] == "HOLD" and not rec["urgent"] and rec["hold"]["state"] == "hold_established" and st["state"] == "hold_established"
          and {j: v["state"] for j, v in st["jobs"].items()} == {"7002": "hold_established", "7003": "hold_established"}
          and not (run / "URGENT_HOLD_FAILED.md").exists(), json.dumps(st)[:300])
    # a failed hold of one job: persisted as failed, urgent request, retried at every poll, established later
    run, s, live = go("T_hold_fail", dict(fail_hold={"7002": 1}))
    rec = poll.main([str(run)])
    st = state_of(run)
    check("poll hold: scontrol fails for one job -> HOLD_FAILED, urgent, hold_failed (that job) / hold_established (the other), error recorded",
          rec["decision"] == "HOLD_FAILED" and rec["urgent"] and st["jobs"]["7002"]["state"] == "hold_failed" and st["jobs"]["7003"]["state"] == "hold_established"
          and st["jobs"]["7002"]["last_rc"] == 1 and "Socket timed out" in st["jobs"]["7002"]["last_err"] and st["state"] == "hold_failed", json.dumps(st)[:400])
    urgent = (run / "URGENT_HOLD_FAILED.md").read_text() if (run / "URGENT_HOLD_FAILED.md").exists() else ""
    check("poll hold: a failed hold writes HOLD.json, the HQ request (marked FAILED) and an URGENT_HOLD_FAILED.md naming the job; nothing is cancelled",
          (run / "HOLD.json").exists() and "7002" in urgent and "URGENT" in urgent and "Do NOT cancel running tasks" in urgent
          and "FAILED" in next(run.glob("HQ_REQUEST_*.md")).read_text() and not any(c[0] == "scancel" for c in s.calls))
    n1 = holds(s)
    rec2 = poll.main([str(run)])
    n2 = holds(s)[len(n1):]
    check("poll hold: the NEXT poll retries ONLY the failed job (not STILL_HELD), still urgent",
          sorted(n1) == ["7002", "7003"] and n2 == ["7002"] and rec2["decision"] == "HOLD_FAILED" and rec2["urgent"]
          and state_of(run)["jobs"]["7002"]["attempts"] == 2 and state_of(run)["jobs"]["7003"]["attempts"] == 1)
    s.fail_hold.clear()
    rec3 = poll.main([str(run)])
    n3 = holds(s)[len(n1) + len(n2):]
    resolved = list(run.glob("URGENT_HOLD_FAILED.resolved_*.md"))
    check("poll hold: once scontrol works the retry establishes the hold -> STILL_HELD, state established, the urgent file is archived as resolved",
          n3 == ["7002"] and rec3["decision"] == "STILL_HELD" and not rec3["urgent"] and state_of(run)["state"] == "hold_established"
          and not (run / "URGENT_HOLD_FAILED.md").exists() and len(resolved) == 1)
    rec4 = poll.main([str(run)])
    check("poll hold: after it is established, later polls make no scontrol call", len(holds(s)) == len(n1) + len(n2) + len(n3) and rec4["decision"] == "STILL_HELD")
    # a partially successful hold (rc 0, only some pending tasks held) counts as failed
    run, s, live = go("T_hold_partial", dict(partial={"7002": 3}))
    rec = poll.main([str(run)])
    st = state_of(run)
    check("poll hold: rc 0 but only 3 of the pending tasks held -> hold_failed ('pending tasks are not held'), urgent",
          rec["decision"] == "HOLD_FAILED" and st["jobs"]["7002"]["state"] == "hold_failed" and "pending tasks are not held" in st["jobs"]["7002"]["reason"]
          and st["jobs"]["7002"]["held"] == 3 and st["jobs"]["7002"]["pending"] > 3 and rec["urgent"], json.dumps(st["jobs"]["7002"]))
    s.partial.clear()
    rec2 = poll.main([str(run)])
    check("poll hold: the retry completes the partial hold -> established", rec2["decision"] == "STILL_HELD" and state_of(run)["state"] == "hold_established")
    # rc 0 with no effect at all is also a failure (the confirmation reads the queue, not the exit status)
    run, s, live = go("T_hold_noeffect", dict(noeffect={"7002", "7003"}))
    rec = poll.main([str(run)])
    check("poll hold: scontrol exits 0 but no task is held -> not trusted (hold_failed for both jobs)",
          rec["decision"] == "HOLD_FAILED" and all(v["state"] == "hold_failed" for v in rec["hold"]["jobs"].values()))
    # terminal / no pending jobs are separate: nothing to hold, no scontrol call, running tasks untouched
    units = list(csv.DictReader(open(BUNDLE / "tables" / "units.tsv", newline=""), delimiter="\t"))
    modes = {u["case_id"]: "none" for u in units if u["p"] == "1000" and int(u["task"]) > 150}
    modes[cases[50]] = "resource_limit"
    run, _ = make_run(root, "T_hold_term", dict(default="ok", modes=modes))
    live = {t: "PENDING" for t in range(151, 601)}
    live[150] = "RUNNING"
    s = Sched(live=live)
    nc_sched.run = s.run
    rec = poll.main([str(run)])
    st = state_of(run)
    check("poll hold: a terminal job (7003: nothing queued) is hold_not_needed with no scontrol call; the job with pending tasks is held; the running task is untouched",
          rec["decision"] == "HOLD" and st["jobs"]["7003"]["state"] == "hold_not_needed" and st["jobs"]["7002"]["state"] == "hold_established"
          and holds(s) == ["7002"] and "7002_150" not in s.held and not any(c[0] == "scancel" for c in s.calls), json.dumps(st["jobs"]))
    run, _ = make_run(root, "T_hold_none", dict(default="ok", modes={cases[50]: "resource_limit"}))
    s = Sched(live={})
    nc_sched.run = s.run
    rec = poll.main([str(run)])
    check("poll hold: no pending task anywhere -> HOLD recorded, hold_not_needed for every job, no scontrol call, not urgent",
          rec["decision"] == "HOLD" and not s.scontrol() and not rec["urgent"] and all(v["state"] == "hold_not_needed" for v in rec["hold"]["jobs"].values()))
    # an unreadable hold_state.json is treated as unconfirmed (retried)
    run, s, live = go("T_hold_corrupt")
    poll.main([str(run)])
    (run / "hold_state.json").write_text("{ not json")
    s.held.clear()
    n_before = len(holds(s))
    rec = poll.main([str(run)])
    check("poll hold: an unreadable hold_state.json is treated as unconfirmed: every job is re-held", len(holds(s)) == n_before + 2 and rec["decision"] == "STILL_HELD")
    # the exit status of the command line: 3 while a hold is not established
    import subprocess
    check("poll hold: the CLI exits with status 3 on HOLD_FAILED and 0 otherwise (checked on the source)",
          "sys.exit(3 if result.get(\"urgent\")" in (BUNDLE / "runner" / "poll.py").read_text())


def t_poll_cadence(root):
    """R2-10: polls 5 to 10 minutes apart; a gap of more than 600 s is late and recorded, throughout production."""
    def seeded(name, age_s, counts=None):
        run, cases, live = build_poll_run(root, name, {})
        pl = logs_of(run) / "polls.jsonl"
        pl.write_text(json.dumps(dict(utc=(datetime.now(timezone.utc) - timedelta(seconds=age_s)).isoformat(), counts=counts or {"running": 1})) + "\n")
        nc_sched.run = Sched(live=live).run
        return run, pl, poll.main([str(run)])
    run, pl, rec = seeded("T_cad601", 601)
    last = json.loads(pl.read_text().splitlines()[-1])
    check("poll cadence: a 601 s gap is LATE: flagged in the record, the warnings and late_polls_so_far, and persisted in polls.jsonl",
          rec["late_poll"] and rec["gap_s"] > 600 and any("LATE POLL" in w for w in rec["warnings"]) and rec["late_polls_so_far"] == 1 and last["late_poll"] is True)
    # The gap is measured when poll.main reaches it, after reconciling the fabricated run (tens of seconds on a loaded machine), so the on-time and
    # early cases keep generous slack against the 300/600 s thresholds (a 540 s seed once measured > 600 s under load: test timing, not a code fault).
    run, pl, rec = seeded("T_cad420", 420)
    check("poll cadence: a 420 s gap (7 minutes) is on time (5 to 10 minutes): no warning", not rec["late_poll"] and not rec["early_poll"] and not rec["warnings"], str(rec.get("gap_s")))
    run, pl, rec = seeded("T_cad30", 30)
    check("poll cadence: a poll 30 s after the previous one is flagged early (never more often than every 5 minutes)", rec["early_poll"] and any("early poll" in w for w in rec["warnings"]), str(rec.get("gap_s")))
    run, pl, rec = seeded("T_cad_late_after200", 700)
    check("poll cadence: the late-poll check is not limited to the first 200 finished units (250 finished, 700 s gap -> late)", rec["counts"]["finished"] == 250 and rec["late_poll"])
    lines = pl.read_text().splitlines()
    first = json.loads(lines[-1])
    first["utc"] = (datetime.now(timezone.utc) - timedelta(seconds=650)).isoformat()
    pl.write_text(lines[0] + "\n" + json.dumps(first) + "\n")
    rec2 = poll.main([str(run)])
    check("poll cadence: late_polls_so_far counts every recorded late poll (one recorded earlier + this one)", rec2["late_polls_so_far"] == 2, str(rec2["late_polls_so_far"]))
    # the cadence report over the whole log (OPS / HQ check at the end of production)
    t0 = datetime.now(timezone.utc) - timedelta(hours=3)
    f = lambda sec: (t0 + timedelta(seconds=sec)).isoformat()
    run, cases, live = build_poll_run(root, "T_cadrep", {})
    pl = logs_of(run) / "polls.jsonl"
    pl.write_text("".join(json.dumps(dict(utc=f(t), counts=dict(running=c))) + "\n" for t, c in [(0, 5), (400, 5), (1100, 5), (1500, 0), (3000, 0)]))
    rep = poll.main(["--cadence", str(run)])
    check("poll cadence report: the 700 s gap during active production is listed, the 1,500 s gap after production ended is not; ok = False",
          rep["polls"] == 5 and len(rep["late_active"]) == 1 and rep["late_active"][0]["gap_s"] == 700 and not rep["ok"]
          and [g["late"] for g in rep["gaps"]] == [False, True, False, True] and [g["active"] for g in rep["gaps"]] == [True, True, True, False])
    pl.write_text("".join(json.dumps(dict(utc=f(t), counts=dict(running=5))) + "\n" for t in (0, 400, 900, 1500)))
    check("poll cadence report: gaps of 400, 500 and 600 s are all on time -> ok", poll.main(["--cadence", str(run)])["ok"])


def t_accounting(root):
    run = root / "T_acct"
    run.mkdir()
    (run / "jobs.tsv").write_text("job\tkind\tsubmitted_utc\tarray\tunits\n7001\tprecompile\tx\t-\t1\n7002\tprimary_p1000\tx\t-\t1\n7003\tprimary_p500\tx\t-\t1\n"
                                  "7010\trerun_1\tx\t-\t1\n7020\tp5\tx\t-\t1\n7030\tp5scan_primary\tx\t-\t1\n")
    tsv = root / "sacct.tsv"
    tsv.write_text("JobID|JobName|State|ExitCode|Elapsed|NodeList|MaxRSS|AllocCPUS|CPUTimeRAW\n"
                   "7001|pre|COMPLETED|0:0|00:10:00|n1||1|600\n"
                   "7002_1|a|COMPLETED|0:0|01:00:00|n1||1|3600\n7002_1.batch|batch|COMPLETED|0:0|01:00:00|n1|512000K|1|3600\n"
                   "7002_2|a|TIMEOUT|0:0|1-00:00:00|n1||1|86400\n"
                   "7003_601|b|COMPLETED|0:0|00:30:00|n1||2|3600\n7010_1|r|COMPLETED|0:0|00:30:00|n1||1|1800\n7020_1|p|COMPLETED|0:0|02:00:00|n1||1|7200\n"
                   "7030|scan|COMPLETED|0:0|00:30:00|n1||1|1800\n")
    out = accounting_summary.main([str(run), str(tsv), str(root / "core_hours")])
    check("accounting: core-hour totals by array (p1000, p500, P5, precompile, reruns); steps excluded; MaxRSS from steps",
          out["primary_p1000"]["tasks"] == 2 and out["primary_p1000"]["alloc_cpu_hours"] == 25.0 and out["primary_p1000"]["elapsed_core_hours"] == 25.0
          and out["primary_p500"]["alloc_cpu_hours"] == 1.0 and out["primary_p500"]["elapsed_core_hours"] == 0.5
          and out["p5"]["alloc_cpu_hours"] == 2.0 and out["precompile"]["tasks"] == 1 and out["reruns"]["alloc_cpu_hours"] == 0.5
          and out["primary_p1000"]["states"] == {"COMPLETED": 1, "TIMEOUT": 1} and out["primary_p1000"]["max_step_maxrss_mb"] == 500.0
          and out["p5scan"]["tasks"] == 1 and out["p5scan"]["alloc_cpu_hours"] == 0.5 and "unknown_job_rows" not in out
          and out["total"]["alloc_cpu_hours"] == 29.17, json.dumps(out))
    tsv_text = (root / "core_hours.tsv").read_text()
    check("accounting: the 10,100 figure is the NATIVE-FIT-BUDGET ceiling (2,100 + 8,000) and the REQUESTED-WALL ceiling is shown too "
          "(600 x 03:52:00 = 2,320; 600 x 13:42:00 = 8,220; 10,540 core-h; 10,541 with the 1 h precompile request)",
          out["primary_p500"]["native_fit_budget_ceiling_core_hours"] == 2100.0 and out["primary_p1000"]["native_fit_budget_ceiling_core_hours"] == 8000.0
          and out["total"]["native_fit_budget_ceiling_core_hours"] == 10100.0
          and out["primary_p500"]["requested_wall_ceiling_core_hours"] == 2320.0 and out["primary_p1000"]["requested_wall_ceiling_core_hours"] == 8220.0
          and out["total"]["requested_wall_ceiling_primary_core_hours"] == 10540.0 and out["total"]["requested_wall_ceiling_with_precompile_core_hours"] == 10541.0
          and "allocated_ceiling" not in tsv_text and "native_fit_budget_ceiling_core_hours" in tsv_text and "requested_wall_ceiling_core_hours" in tsv_text
          and tsv_text.strip().splitlines()[-1].split("\t")[5:7] == ["10100.0", "10541.0"], tsv_text)


def main():
    work = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(tempfile.mkdtemp())
    work.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(dir=work))
    try:
        t_reconcile(root)
        t_poll(root)
        t_poll_hold(root)
        t_poll_cadence(root)
        t_accounting(root)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    print("\ntest_py: %d passed, %d failed" % (PASS, FAIL))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
