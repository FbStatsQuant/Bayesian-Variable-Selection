#!/bin/bash
# make_resubmit.sh -- the resubmission lists of one round rN for the benchmark wave (DESIGN.md section 5). Derived from PROD_L's
# make_resubmit.sh (same terminal gate, CLOSED refusal, stale refusal, idempotence and exit codes).
#   bash make_resubmit.sh STAMP rN [--dry-run]
# For every case that is not done (bench_verify.verify_case), from its ledger history over the pieces bench and benchretry:
#   never started (deferred / not reached / never submitted)            -> RUN_HOME/resubmit/bench_rN.tsv
#   exactly one start, ended unit_failed or killed_external (no .end)    -> bench_rN.tsv (one rerun, same budget)
#   exactly one start, ended killed_timeout                             -> benchretry_rN.tsv (D56: one retry at DOUBLED budget)
#   anything else (two or more starts, or a benchretry attempt made)    -> bench_rN_exceptions.tsv (never relisted; report to HQ)
# Exit 0 lists written / SAME_LIST / NOTHING_TO_RESUBMIT; 2 usage, CLOSED, or a different existing list (use a new wave name);
# 3 a run job is active or accounting is not terminal; 4 scheduler error; 5 stale artefacts present (run clear_stale.sh).
set -euo pipefail
STAMP=${1:?usage: make_resubmit.sh STAMP rN [--dry-run]}; wave=${2:?}; shift 2; dry=0; [[ ${1:-} != --dry-run ]] || { dry=1; shift; }; (($#==0)) || exit 2
[[ $wave =~ ^r[1-9][0-9]*$ ]] || { echo "wave must be rN" >&2; exit 2; }
[[ $STAMP =~ ^[0-9]{8}T[0-9]{4}Z$ ]] || exit 2
export STAMP
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd); source "$HERE/bench.env"; source "$HERE/stale_lib.sh"
SQUEUE=${SQUEUE:-squeue}; SACCT=${SACCT:-sacct}
[[ -r $RUN_HOME/JOBIDS.tsv ]] || { echo 'missing JOBIDS' >&2; exit 3; }
ids=$(awk -F '\t' 'NR>1 {if($3 !~ /^[0-9]+$/) exit 1; print $3}' "$RUN_HOME/JOBIDS.tsv" | paste -sd, -) || exit 3
[[ -n $ids ]] || exit 3
q=$("$SQUEUE" -h -u fb31 -o '%i|%j|%T|%C') || exit 4
if printf '%s\n' "$q" | awk -F'|' -v ids="$ids" 'BEGIN{split(ids,a,",");for(i in a)x[a[i]]=1} NF{split($1,b,"_");if(x[b[1]])f=1} END{exit !f}'; then echo 'active jobs' >&2; exit 3; fi
acct=$("$SACCT" -X -n -P -j "$ids" -o JobID,State) || exit 4
printf '%s\n' "$acct" | awk -F'|' -v ids="$ids" 'BEGIN{split(ids,a,",");for(i in a)x[a[i]]=1} NF>=2{split($1,b,"_");if(x[b[1]]){seen[b[1]]=1;if($2 !~ /^(COMPLETED|FAILED|CANCELLED|TIMEOUT|OUT_OF_MEMORY|NODE_FAIL|DEADLINE|BOOT_FAIL|PREEMPTED)/)bad=1}} END{for(i in x)if(!seen[i])bad=1;exit bad}' || { echo 'accounting not terminal or missing' >&2; exit 3; }
[[ ! -e $RUN_HOME/manifests/bench.CLOSED ]] || { echo "REFUSED: bench is CLOSED ($RUN_HOME/manifests/bench.CLOSED); its inventory at closing is $RUN_HOME/manifests/bench.inventory.tsv" >&2; exit 2; }
res="$SCR_ROOT/results/$RUNID_bench"
stale=$(stale_find "$res" | head -n 5)
[[ -z $stale ]] || { echo "REFUSED: stale artefacts (run clear_stale.sh first): $(printf '%s' "$stale" | tr '\n' ' ')" >&2; exit 5; }
export RUN_HOME LOG_RUN LISTS wave dry HERE res
"${PYTHON:-python3}" - <<'PY'
import csv, io, os, pathlib, sys
sys.path.insert(0, os.environ["HERE"])
from bench_verify import verify_case
p = os.environ; wave = p["wave"]
rows = [r for r in csv.DictReader(open(pathlib.Path(p["LISTS"]) / "units.tsv", newline=""), delimiter="\t") if r["piece"] == "bench"]
rows.sort(key=lambda r: (int(r["task"]), r["unit"]))
if not rows: sys.exit("no bench units in the list")
logs = pathlib.Path(p["LOG_RUN"]) / "ledger"
def history(unit):
    """[(piece, tag, outcome)] for every started attempt of the unit, over bench and benchretry"""
    out = []
    for piece in ("bench", "benchretry"):
        d = logs / piece / unit
        if not d.is_dir(): continue
        for s in sorted(d.glob("*.start")):
            e = s.with_suffix(".end")
            if e.exists():
                kv = dict(x.split("=", 1) for x in e.read_text(encoding="utf-8").split() if "=" in x)
                out.append((piece, s.stem, kv.get("outcome", "invalid")))
            else:
                out.append((piece, s.stem, "killed_external"))
    return out
lists = {"bench": [], "benchretry": [], "exceptions": []}
for r in rows:
    case_dir = pathlib.Path(p["res"]) / r["dataset"][:5] / r["unit"]
    ok, _ = verify_case(case_dir, r["unit"]) if case_dir.is_dir() else (False, None)
    if ok: continue
    h = history(r["unit"])
    if not h: lists["bench"].append(r)
    elif len(h) == 1 and h[0][0] == "bench" and h[0][2] in ("unit_failed", "killed_external"): lists["bench"].append(r)
    elif len(h) == 1 and h[0][0] == "bench" and h[0][2] == "killed_timeout": lists["benchretry"].append(r)
    elif len(h) == 1 and h[0][0] == "bench" and h[0][2] in ("ok", "skipped"): lists["bench"].append(r)   # ended ok but not valid now: one rerun
    else: lists["exceptions"].append(r)
fields = ["piece", "task", "unit", "dataset", "scale", "repeat"]
def tsv(items, piece, renumber):
    f = io.StringIO(newline=""); w = csv.DictWriter(f, fields, delimiter="\t", lineterminator="\n"); w.writeheader()
    for i, r in enumerate(items):
        row = {k: r[k] for k in fields}; row["piece"] = piece
        if renumber: row["task"] = i // 25
        w.writerow(row)
    return f.getvalue()
out = pathlib.Path(p["RUN_HOME"]) / "resubmit"
targets = []
if lists["bench"]: targets.append((out / ("bench_" + wave + ".tsv"), tsv(lists["bench"], "bench", True)))
if lists["benchretry"]: targets.append((out / ("benchretry_" + wave + ".tsv"), tsv(lists["benchretry"], "benchretry", True)))
if lists["exceptions"]: targets.append((out / ("bench_" + wave + "_exceptions.tsv"), tsv(lists["exceptions"], "bench", False)))
if not targets: print("NOTHING_TO_RESUBMIT"); sys.exit(0)
for path, data in targets:
    if path.exists() and path.read_text() != data:
        print("REFUSED: different existing list " + str(path) + " (use a new wave name)", file=sys.stderr); sys.exit(2)
if p["dry"] == "1":
    print("DRY RUN", len(lists["bench"]), "bench", len(lists["benchretry"]), "benchretry", len(lists["exceptions"]), "exceptions")
    for k in ("bench", "benchretry", "exceptions"):
        for r in lists[k]: print(k, r["unit"])
    sys.exit(0)
out.mkdir(parents=True, exist_ok=True)
for path, data in targets:
    if path.exists(): print("SAME_LIST", path)
    else:
        tmp = path.with_name("." + path.name + ".tmp"); tmp.write_text(data); tmp.replace(path); print("WROTE", path)
if not lists["bench"] and not lists["benchretry"]: print("NOTHING_TO_RESUBMIT (exceptions only: report to HQ)")
PY
