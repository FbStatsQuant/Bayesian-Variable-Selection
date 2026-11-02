"""One production poll with the GO_2400 C3 stop rule (NOTS login node; Python 3.9 standard library only).

Usage: python3 poll.py [--no-hold] RUN_DIR [RUN_DIR ...]
       python3 poll.py --cadence RUN_DIR       (check the gaps between the polls recorded so far; exit 1 if one was late during production)
OPS polls every 5 to 10 minutes over ONE ssh connection (never more often than every 5 minutes). A gap of MORE than 600 s between two polls
is LATE: it is flagged in the poll record, in the warnings and in `late_polls_so_far`, throughout active production (not only in the first 200
units). The poll is read-only except for the stop rule: for each run it calls reconcile.main(--sacct) (no lock clearing), then, across all
runs, reports finished, ok, method_failed, resource_limit (its own category, C5), timeout, infra, infra_repeat, orphan, ever_infra
(infrastructure failures), escalated, running, rerun_queued, not_run, in total and per p (the two primary arrays).
C3 window = the first 200 finished units ordered by event_utc (reconcile: the time of a unit's first failed attempt, else its finish),
so failures stay in the window after reruns. finished = done, pulled, timeout, infra, infra_repeat, orphan, or ever_infra.
Trigger if, inside the window: any resource_limit or timeout; or ever_infra units > 4. The 2 % of GO_2400 C3 is fixed as "more than 4
infrastructure failures within the first 200 finished units" (2 % of 200), so no interpretation is needed before 200 units exist; the count
can only grow, so the trigger fires as soon as it is certain. After 200 finished units the window is frozen: later failures are reported
in the counts but never trigger a HOLD.

HOLD (Sol review 2, R2-1). On a new trigger the poll requests `scontrol hold` for every primary job of the run (pending tasks only; running
tasks go on, nothing is ever cancelled) and then CONFIRMS it from squeue (every pending task of the job shows a Held reason). The per-job
state is persisted in RUN_DIR/hold_state.json BEFORE the first scontrol call and again after the confirmation:
  hold_requested    written first; a crash between request and confirmation leaves this state and the next poll retries
  hold_established  every pending task of the job is held (confirmed from squeue)
  hold_failed       scontrol returned non-zero, or the confirmation shows pending tasks that are not held (a partial hold counts as failed)
  hold_not_needed   the job is terminal or has no pending task (nothing to hold; running tasks go on)
While any job is hold_failed (or still hold_requested) every later poll RETRIES the hold, the decision is HOLD_FAILED, the process exits with
status 3 and URGENT_HOLD_FAILED.md (an urgent request for OPS/HQ) is written; it is archived as URGENT_HOLD_FAILED.resolved_<utc>.md once the
hold is established. HOLD.json records the trigger units; HQ_REQUEST_<utc>.md is the request for HQ.
Acknowledgement: while a run has HOLD.json and no newer HOLD_RELEASED.json, the poll reports STILL_HELD (retrying any unconfirmed hold) and
does not trigger again. HOLD_RELEASED.json (written only on HQ's instruction) lists acknowledged case_ids; they no longer trigger, and the
infra threshold becomes max(4, number of acknowledged infra units).
Logs: every poll appends one JSON line to LOGROOT/polls.jsonl (scratch, append-only execution log); the latest record is kept in
RUN_DIR/poll_latest.json (home, small state). Importable: main(argv) returns the record dict.
"""
import csv
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import nc_sched as sched  # noqa: E402
import reconcile  # noqa: E402

WINDOW, INFRA_MAX = 200, 4          # 2 % of 200
LATE_POLL_S = 600                   # C3: polls at most 10 minutes apart: a gap of MORE than 600 s is late
EARLY_POLL_S = 300                  # charter rule: never more often than every 5 minutes (one ssh connection per poll)
SATISFIED = ("hold_established", "hold_not_needed")


def cfg_of(run):
    return dict(line.split("=", 1) for line in (run / "config.env").read_text().split())


def polls_path(run):
    d = Path(cfg_of(run)["LOGROOT"])
    d.mkdir(parents=True, exist_ok=True)
    return d / "polls.jsonl"


def atomic_write(path, text):
    tmp = path.with_name(path.name + ".tmp.%d" % os.getpid())
    tmp.write_text(text)
    os.replace(tmp, path)


def queue_snapshot(jobs):
    """({job: dict(pending, held, running)}, "") from one squeue call (-r expands pending array ranges), or (None, error text)."""
    q = sched.run(["squeue", "-h", "-r", "-u", "fb31", "-o", "%i|%T|%r"])
    if q.returncode != 0:
        return None, (q.stderr or "").strip()[:300]
    snap = {j: dict(pending=0, held=0, running=0) for j in jobs}
    for line in q.stdout.splitlines():
        if not line.strip():
            continue
        jid, state, reason = (line.split("|", 2) + ["", ""])[:3]
        s = snap.get(jid.split("_")[0])
        if s is None:
            continue
        if state.startswith("PENDING"):
            s["pending"] += 1
            s["held"] += 1 if "Held" in reason else 0
        else:
            s["running"] += 1
    return snap, ""


def hold_status(s):
    if s["pending"] == 0:
        return "hold_not_needed"
    return "hold_established" if s["held"] == s["pending"] else "hold_failed"


def enforce_hold(jobs, prev, no_hold, now):
    """Request (where needed) and CONFIRM the hold of `jobs`. prev = persisted per-job states. Returns the new per-job states."""
    snap, err = queue_snapshot(jobs)
    todo = [j for j in jobs if snap is None or hold_status(snap[j]) == "hold_failed"]
    calls = {}
    if not no_hold:
        for j in todo:
            r = sched.run(["scontrol", "hold", j])
            calls[j] = dict(rc=r.returncode, err=(r.stderr or "").strip()[:300])
    snap2, err2 = (snap, err) if not calls else queue_snapshot(jobs)
    out = {}
    for j in jobs:
        old = prev.get(j, {})
        e = dict(attempts=int(old.get("attempts", 0)) + (1 if j in calls else 0))
        if snap2 is None:
            e.update(state="hold_failed", reason="squeue failed, the hold is not confirmed: " + err2)
        else:
            e.update(state=hold_status(snap2[j]), pending=snap2[j]["pending"], held=snap2[j]["held"], running=snap2[j]["running"])
            if e["state"] == "hold_failed":
                if j in calls and calls[j]["rc"] != 0:
                    e["reason"] = "scontrol hold exited %s: %s" % (calls[j]["rc"], calls[j]["err"])
                else:
                    e["reason"] = "%d of %d pending tasks are not held" % (snap2[j]["pending"] - snap2[j]["held"], snap2[j]["pending"])
        if j in calls:
            e.update(last_rc=calls[j]["rc"], last_err=calls[j]["err"], last_attempt_utc=now.isoformat())
        elif "last_rc" in old:
            e.update(last_rc=old["last_rc"], last_err=old.get("last_err", ""), last_attempt_utc=old.get("last_attempt_utc", ""))
        out[j] = e
    return out


def hold_overall(states):
    return "hold_established" if all(v.get("state") in SATISFIED for v in states.values()) else "hold_failed"


def cadence(run, now=None):
    """Gaps between consecutive polls of one run (LOGROOT/polls.jsonl). A gap is `active` if production was still going at its start."""
    pl = polls_path(run)
    recs = [json.loads(ln) for ln in pl.read_text().splitlines() if ln.strip()] if pl.exists() else []
    gaps = []
    for a, b in zip(recs, recs[1:]):
        g = (datetime.fromisoformat(b["utc"]) - datetime.fromisoformat(a["utc"])).total_seconds()
        c = a.get("counts", {})
        active = bool(c.get("running", 0) or c.get("not_run", 0) or c.get("rerun_queued", 0) or a.get("tasks_pending_or_running", 0))
        gaps.append(dict(from_utc=a["utc"], to_utc=b["utc"], gap_s=g, active=active, late=g > LATE_POLL_S, early=g < EARLY_POLL_S))
    since_last = None
    if recs and now is not None:
        since_last = (now - datetime.fromisoformat(recs[-1]["utc"])).total_seconds()
    return dict(polls=len(recs), gaps=gaps, late_active=[g for g in gaps if g["late"] and g["active"]], since_last_s=since_last)


def main(argv):
    if argv and argv[0] == "--cadence":
        rep = cadence(Path(argv[1]).resolve(), datetime.now(timezone.utc))
        rep["ok"] = not rep["late_active"]
        return rep
    no_hold = "--no-hold" in argv
    runs = [Path(a).resolve() for a in argv if a != "--no-hold"]
    if not runs:
        raise SystemExit(__doc__)
    rows, jobs, per_run = [], set(), {}
    for r in runs:
        summary = reconcile.main([str(r), "--sacct"])
        per_run[r.name] = summary
        jobs |= set(summary["jobs"])
        with open(r / "reconcile.tsv", newline="") as f:
            for x in csv.DictReader(f, delimiter="\t"):
                x["run"] = r.name
                rows.append(x)

    ack, hold_state, prev_hold = set(), "none", {}
    for r in runs:
        h, rel = r / "HOLD.json", r / "HOLD_RELEASED.json"
        if rel.exists():
            ack |= set(json.loads(rel.read_text()).get("acknowledged", []))
        if h.exists() and (not rel.exists() or h.stat().st_mtime > rel.stat().st_mtime):
            hold_state = "held"
            hs = r / "hold_state.json"
            if hs.exists():
                try:
                    prev_hold.update(json.loads(hs.read_text()).get("jobs", {}))
                except json.JSONDecodeError:
                    pass                      # an unreadable state counts as hold_requested: every job is re-checked and retried

    ever = lambda x: x["ever_infra"] == "true"
    finished = [x for x in rows if x["klass"] in ("done", "pulled", "timeout", "infra", "infra_repeat", "orphan") or ever(x)]
    finished.sort(key=lambda x: (x["event_utc"] or "9999", x["case_id"]))
    window = finished[:WINDOW]
    finished_ids = {(x["run"], x["case_id"]) for x in finished}

    def counts_of(xs):
        c = lambda k, v: sum(1 for x in xs if x[k] == v)
        return dict(units=len(xs), finished=sum(1 for x in xs if (x["run"], x["case_id"]) in finished_ids),
                    ok=c("outcome", "ok"), method_failed=c("outcome", "method_failed"),
                    resource_limit=c("outcome", "resource_limit"), timeout=c("klass", "timeout"),
                    infra=c("klass", "infra"), infra_repeat=c("klass", "infra_repeat"), orphan=c("klass", "orphan"),
                    ever_infra=sum(1 for x in xs if ever(x)), escalated=c("escalated", "true"),
                    running=c("klass", "running"), rerun_queued=c("klass", "rerun_queued"), not_run=c("klass", "not_run"))

    counts = counts_of(rows)
    by_p = {p: counts_of([x for x in rows if x["p"] == p]) for p in sorted({x["p"] for x in rows})}
    w_rl = [x["case_id"] for x in window if x["outcome"] == "resource_limit" and x["case_id"] not in ack]
    w_to = [x["case_id"] for x in window if x["klass"] == "timeout" and x["case_id"] not in ack]
    w_inf = [x["case_id"] for x in window if ever(x)]
    inf_limit = max(INFRA_MAX, sum(1 for c in w_inf if c in ack))
    reasons = []
    if w_rl:
        reasons.append("%d resource_limit in first %d finished: %s" % (len(w_rl), len(window), ",".join(w_rl[:10])))
    if w_to:
        reasons.append("%d timeout in first %d finished: %s" % (len(w_to), len(window), ",".join(w_to[:10])))
    if len(w_inf) > inf_limit:
        reasons.append("%d units with an infrastructure failure (> %d) in first %d finished" % (len(w_inf), inf_limit, len(window)))
    now = datetime.now(timezone.utc)
    sorted_jobs = sorted(jobs)
    snap0, err0 = queue_snapshot(sorted_jobs)
    if snap0 is None:
        raise SystemExit("squeue failed: " + err0)
    held_now = sum(s["held"] for s in snap0.values())
    pending_or_running = sum(s["pending"] + s["running"] for s in snap0.values())
    warnings, hold_jobs, hold_summary = [], {}, "none"
    new_trigger = hold_state != "held" and bool(reasons)
    if hold_state == "held":
        decision = "STILL_HELD"
        targets = sorted(set(sorted_jobs) | set(prev_hold))
        unconfirmed = [j for j in targets if prev_hold.get(j, {}).get("state") not in SATISFIED]
        hold_jobs = {j: prev_hold.get(j, {}) for j in targets if j not in unconfirmed}
        if unconfirmed and not no_hold:                 # retry every hold that was never confirmed, at every poll
            hold_jobs.update(enforce_hold(unconfirmed, prev_hold, no_hold, now))
        else:
            hold_jobs.update({j: prev_hold.get(j, {}) for j in unconfirmed})
        hold_summary = hold_overall(hold_jobs)
        if hold_summary == "hold_failed":
            decision = "HOLD_FAILED"
        # A release without HOLD_RELEASED.json would silently disable the stop rule.
        if held_now == 0 and (counts["not_run"] or counts["running"]):
            warnings.append("HOLD.json present but no task is held in the queue: if HQ released the hold, "
                            "write HOLD_RELEASED.json in every run dir; the stop rule is otherwise inactive")
    elif new_trigger:
        decision = "HOLD"
        if not no_hold:
            for r in runs:                              # persisted BEFORE the first scontrol call
                atomic_write(r / "hold_state.json", json.dumps(dict(
                    state="hold_requested", requested_utc=now.isoformat(), reasons=reasons,
                    jobs={j: dict(state="hold_requested", attempts=0) for j in sorted_jobs}), indent=1) + "\n")
            hold_jobs = enforce_hold(sorted_jobs, {}, no_hold, now)
            hold_summary = hold_overall(hold_jobs)
            if hold_summary == "hold_failed":
                decision = "HOLD_FAILED"
    else:
        decision = "continue"
    urgent = decision == "HOLD_FAILED"

    # cadence (R2-10): the gap since the previous poll of every run, checked at every poll of active production
    gap, late_so_far = None, 0
    for r in runs:
        pl = polls_path(r)
        lines = [ln for ln in pl.read_text().splitlines() if ln.strip()] if pl.exists() else []
        if lines:
            g = (now - datetime.fromisoformat(json.loads(lines[-1])["utc"])).total_seconds()
            gap = g if gap is None else max(gap, g)
        late_so_far = max(late_so_far, sum(1 for ln in lines if json.loads(ln).get("late_poll")))
    late = gap is not None and gap > LATE_POLL_S
    early = gap is not None and gap < EARLY_POLL_S
    late_so_far += 1 if late else 0
    if late:
        warnings.append("LATE POLL: %d s since the previous poll (C3: polls 5 to 10 minutes apart; more than 600 s is late; recorded)" % gap)
    if early:
        warnings.append("early poll: %d s since the previous poll (never poll more often than every 5 minutes)" % gap)

    rec = dict(utc=now.isoformat(), decision=decision, urgent=urgent, reasons=reasons, counts=counts, by_p=by_p,
               window=dict(size=len(window), resource_limit=len(w_rl), timeout=len(w_to), ever_infra=len(w_inf),
                           infra_limit=inf_limit, acknowledged=len(ack)),
               tasks_held_in_queue=held_now, tasks_pending_or_running=pending_or_running,
               hold=dict(state=hold_summary, jobs=hold_jobs), warnings=warnings,
               gap_s=gap, late_poll=late, early_poll=early, late_polls_so_far=late_so_far,
               trigger_units=dict(resource_limit=w_rl, timeout=w_to, infra=w_inf), runs=per_run)
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    for r in runs:
        with open(polls_path(r), "a") as f:
            f.write(json.dumps(rec) + "\n")
        atomic_write(r / "poll_latest.json", json.dumps(rec, indent=1) + "\n")
        if hold_jobs and not no_hold:
            hs = r / "hold_state.json"
            try:
                old = json.loads(hs.read_text()) if hs.exists() else {}
            except json.JSONDecodeError:
                old = {}                                # an unreadable state is replaced by the confirmed one
            atomic_write(hs, json.dumps(dict(old, state=hold_summary, updated_utc=now.isoformat(), jobs=hold_jobs), indent=1) + "\n")
        if new_trigger and not no_hold:
            (r / "HOLD.json").write_text(json.dumps(rec, indent=1) + "\n")
            if urgent:
                state_line = ("Hold state: **FAILED**. The hold of at least one primary job is NOT established (see URGENT_HOLD_FAILED.md); "
                              "pending tasks can still start. Every later poll retries the hold.")
            else:
                state_line = ("Hold state: **established**. Pending tasks of the primary arrays were held with `scontrol hold` and confirmed in "
                              "squeue (running tasks continue; nothing was cancelled).")
            req = ["# Request to HQ: PROD-H stop rule (GO_2400 C3) fired at %s" % now.strftime("%Y-%m-%dT%H:%M:%SZ"), "", state_line, ""]
            req += ["- " + x for x in reasons]
            req += ["", "Counts: finished %d of %d; ok %d; resource_limit %d; timeout %d; infrastructure failures %d; escalated %d."
                    % (counts["finished"], counts["units"], counts["ok"], counts["resource_limit"], counts["timeout"], counts["ever_infra"],
                       counts["escalated"]), "",
                    "Decision needed: release (write `HOLD_RELEASED.json` listing the acknowledged case_ids, then `scontrol release <jobid>`) or stop.",
                    "Hold per job: " + ", ".join("%s %s" % (j, v.get("state")) for j, v in sorted(hold_jobs.items()))]
            atomic_write(r / ("HQ_REQUEST_%s.md" % stamp), "\n".join(req) + "\n")
        urgent_f = r / "URGENT_HOLD_FAILED.md"
        if urgent and not no_hold:
            bad = [j for j, v in sorted(hold_jobs.items()) if v.get("state") not in SATISFIED]
            atomic_write(urgent_f, "\n".join([
                "# URGENT for OPS and HQ: the C3 hold is NOT established (%s)" % now.strftime("%Y-%m-%dT%H:%M:%SZ"), "",
                "The stop rule fired but `scontrol hold` did not hold every pending task. Pending tasks may keep launching after the mandatory stop.", "",
                *["- job %s: %s (attempts %s; last rc %s: %s)" % (j, hold_jobs[j].get("reason", "hold requested, not confirmed"),
                                                                  hold_jobs[j].get("attempts"), hold_jobs[j].get("last_rc"),
                                                                  hold_jobs[j].get("last_err", "")) for j in bad], "",
                "Action NOW: `scontrol hold <jobid>` by hand for each job above and confirm with `squeue -u fb31 -r -o '%i|%T|%r'` that every "
                "pending task shows JobHeldUser. Do NOT cancel running tasks.",
                "The next poll retries the hold automatically and exits with status 3 until it is established.", ""]))
        elif urgent_f.exists() and not urgent and hold_summary == "hold_established":
            os.replace(urgent_f, r / ("URGENT_HOLD_FAILED.resolved_%s.md" % stamp))
    return rec


if __name__ == "__main__":
    result = main(sys.argv[1:])
    print(json.dumps(result))
    sys.exit(3 if result.get("urgent") else (1 if result.get("ok") is False else 0))
