"""Laptop side of one production poll: ONE ssh call running runner/poll.py on NOTS, then
POLL_LOG.md (append) and the "## Latest poll" section of STATUS.md (replace).  Usage: py -3 -I poll_local.py"""
import json
import re
import subprocess
from pathlib import Path

E = Path(__file__).resolve().parents[1]
RUNS = "runs/prod_p1000_20261023T1227Z runs/prod_p0500_20261023T1227Z"
# Same single connection: raise the p1000 throttle to %100 once the p500 array has left the queue
# (combined throttle stays <= 100).
THROTTLE = ('q=$(squeue -h -u fb31 -o %i); if echo "$q" | grep -q "^2365495"; then echo P500_STILL_QUEUED; '
            'else t=$(scontrol show job 2365494 | grep -o "ArrayTaskThrottle=[0-9]*" | head -1); '
            'if [ "$t" = "ArrayTaskThrottle=100" ]; then echo THROTTLE_ALREADY_100; '
            'else scontrol update JobId=2365494 ArrayTaskThrottle=100 && echo "THROTTLE_RAISED (was $t)"; fi; fi; ')
cmd = ("cd /home/fb31/projects/BVS/SMC_BVS_v3/deploy/claude && " + THROTTLE +
       "python3 runner/poll.py " + RUNS + " && "
       # Same connection: name every non-ok unit (class infra/infra_repeat/orphan/timeout or outcome
       # resource_limit/method_failed) so STATUS can report it before the rerun stage.
       "for r in " + RUNS + "; do awk -F'\t' 'NR==1{for(i=1;i<=NF;i++)c[$i]=i;next} "
       "$c[\"klass\"]~/infra|orphan|timeout/||$c[\"outcome\"]~/resource_limit|method_failed/"
       "{print \"UNIT\",$c[\"case_id\"],$c[\"klass\"],$c[\"outcome\"],$c[\"step_state\"],$c[\"last_exit\"],$c[\"node\"]}' $r/reconcile.tsv; done; "
       "squeue -u fb31 -h -t R | wc -l")
r = subprocess.run(["ssh", "-T", "-o", "BatchMode=yes", "-o", "ConnectTimeout=25", "nots", cmd],
                   capture_output=True, text=True, timeout=600)
if r.returncode != 0:
    print("POLL FAILED rc=%d\n%s" % (r.returncode, r.stderr[-2000:]))
    raise SystemExit(1)
lines = r.stdout.strip().splitlines()
d = json.loads(next(l for l in lines if l.startswith("{")))
# Our arrays only (the last line is squeue over ALL of fb31's running jobs, other campaigns included).
n_all_fb31 = lines[-1].strip()
n_running = str(sum(v.get("running_tasks", 0) for v in d["runs"].values()))
for l in lines:
    if not l.startswith("{") and l is not lines[-1]:
        print(l)
c, w = d["counts"], d["window"]
p = {k: v for k, v in d["by_p"].items()}
line = ("| %s | **%s** | %d/%d | %d | %d | %d | %d | %d | %d | %d | %d | %d (p1000 %d, p500 %d) | %d/%d rl %d to %d inf %d | %s |" % (
    d["utc"][:16] + "Z", d["decision"], c["finished"], c["units"], c["ok"], c["method_failed"], c["resource_limit"],
    c["timeout"], c["infra"] + c["infra_repeat"], c["orphan"], c["ever_infra"], c["escalated"], int(n_running),
    p.get("1000", {}).get("finished", 0), p.get("500", {}).get("finished", 0),
    w["size"], 200, w["resource_limit"], w["timeout"], w["ever_infra"],
    "; ".join(d["reasons"] + d["warnings"]) or "—"))
log = E / "POLL_LOG.md"
if not log.exists():
    log.write_text("# Production poll log (C3 stop rule; one ssh connection per poll)\n\n"
                   "| UTC | decision | finished | ok | method_failed | resource_limit | timeout | infra | orphan | ever_infra | escalated | running tasks (finished p1000, p500) | C3 window | reasons |\n"
                   "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n", encoding="utf-8")
with open(log, "a", encoding="utf-8", newline="\n") as f:
    f.write(line + "\n")
st = E / "STATUS.md"
s = st.read_text(encoding="utf-8")
new = ("## Latest poll\n\n%s\n\n| finished | ok | method_failed | resource_limit | timeout | infra | orphan | ever_infra | escalated |"
       " running tasks | held tasks |\n|---|---|---|---|---|---|---|---|---|---|---|\n| %d/%d (p1000 %d, p500 %d) | %d | %d | %d | %d | %d | %d | %d | %d | %s | %d |\n\n"
       "C3 window: %d of the first 200 finished; resource_limit %d, timeout %d, ever_infra %d (limit %d). Full log: POLL_LOG.md.\n\n" % (
           "**%s** at %s%s" % (d["decision"], d["utc"][:19] + "Z", (" — " + "; ".join(d["reasons"] + d["warnings"])) if d["reasons"] or d["warnings"] else ""),
           c["finished"], c["units"], p.get("1000", {}).get("finished", 0), p.get("500", {}).get("finished", 0),
           c["ok"], c["method_failed"], c["resource_limit"], c["timeout"], c["infra"] + c["infra_repeat"], c["orphan"],
           c["ever_infra"], c["escalated"], n_running, d["tasks_held_in_queue"],
           w["size"], w["resource_limit"], w["timeout"], w["ever_infra"], w["infra_limit"]))
s = re.sub(r"## Latest poll\n.*?(?=\n## )", new.rstrip("\n") + "\n", s, flags=re.S)
st.write_text(s, encoding="utf-8", newline="\n")
print(line)
