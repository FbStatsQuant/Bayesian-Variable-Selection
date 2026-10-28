"""One production poll over all runs of the campaign, with the GO_2400 C3 stop rule (NOTS login node).

Usage: python3 poll.py [--no-hold] RUN_DIR [RUN_DIR ...]
For each run: reconcile.py --sacct (no lock clearing). Then, across all runs:
  counts (total and per p): finished, ok, method_failed, resource_limit, timeout, infra, infra_repeat,
  orphan, ever_infra, escalated, running, rerun_queued, not_run.
  C3 window = the first 200 finished units ordered by event_utc (reconcile: the time of a unit's first
  failed attempt, else its finish), so failures stay in the window after reruns (review R4).
  finished = done, pulled, timeout, infra, infra_repeat, orphan, or ever_infra.
  Trigger if, inside the window: any resource_limit or timeout; or ever_infra units > 4 (= 2 % of 200;
  the count can only grow, so the trigger fires as soon as it is certain).
Acknowledgement (review R5): HOLD.json records the trigger units. While a run has HOLD.json and no newer
HOLD_RELEASED.json, the poll reports STILL_HELD and does not hold again. HOLD_RELEASED.json (written by
the lead only on HQ's instruction) lists acknowledged case_ids; they no longer trigger, and the infra
threshold becomes max(4, number of acknowledged infra units).
On a new trigger: `scontrol hold` every array job of every run (pending tasks only; running tasks go on),
write HOLD.json in every run and print HOLD. Every poll appends one JSON line to RUN_DIR/polls.jsonl.
"""
import csv
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

args = sys.argv[1:]
no_hold = "--no-hold" in args
runs = [Path(a).resolve() for a in args if a != "--no-hold"]
WINDOW, INFRA_MAX = 200, 4          # 2 % of 200
rows, jobs, per_run = [], set(), {}
for r in runs:
    res = subprocess.run([sys.executable, str(r / "runner" / "reconcile.py"), str(r), "--sacct"],
                         capture_output=True, text=True, check=True)
    summary = json.loads(res.stdout.strip().splitlines()[-1])
    per_run[r.name] = summary
    jobs |= set(summary["jobs"])
    with open(r / "reconcile.tsv") as f:
        for x in csv.DictReader(f, delimiter="\t"):
            x["run"] = r.name
            rows.append(x)

ack, hold_state = set(), "none"
for r in runs:
    h, rel = r / "HOLD.json", r / "HOLD_RELEASED.json"
    if rel.exists():
        ack |= set(json.loads(rel.read_text()).get("acknowledged", []))
    if h.exists() and (not rel.exists() or h.stat().st_mtime > rel.stat().st_mtime):
        hold_state = "held"

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
held_now = 0
q = subprocess.run(["squeue", "-h", "-r", "-u", "fb31", "-o", "%i|%r"], capture_output=True, text=True)
for line in q.stdout.split():
    jid, reason = line.split("|", 1)
    if jid.split("_")[0] in jobs and "Held" in reason:
        held_now += 1
held, warnings = [], []
if hold_state == "held":
    decision = "STILL_HELD"
    # Review N4: a release without HOLD_RELEASED.json would silently disable the stop rule.
    if held_now == 0 and (counts["not_run"] or counts["running"]):
        warnings.append("HOLD.json present but no task is held in the queue: if HQ released the hold, "
                        "write HOLD_RELEASED.json in every run dir; the stop rule is otherwise inactive")
elif reasons:
    decision = "HOLD"
    if not no_hold:
        for j in sorted(jobs):
            res = subprocess.run(["scontrol", "hold", j], capture_output=True, text=True)
            held.append(dict(job=j, rc=res.returncode, err=res.stderr.strip()))
else:
    decision = "continue"
rec = dict(utc=datetime.now(timezone.utc).isoformat(), decision=decision, reasons=reasons, counts=counts, by_p=by_p,
           window=dict(size=len(window), resource_limit=len(w_rl), timeout=len(w_to), ever_infra=len(w_inf),
                       infra_limit=inf_limit, acknowledged=len(ack)),
           tasks_held_in_queue=held_now, held=held, warnings=warnings,
           trigger_units=dict(resource_limit=w_rl, timeout=w_to, infra=w_inf), runs=per_run)
for r in runs:
    with open(r / "polls.jsonl", "a") as f:
        f.write(json.dumps(rec) + "\n")
    if decision == "HOLD" and not no_hold:
        (r / "HOLD.json").write_text(json.dumps(rec, indent=1) + "\n")
print(json.dumps(rec))
