#!/bin/bash
set -euo pipefail
STAMP=${1:?}; piece=${2:?}; wave=${3:?}; shift 3; dry=0; [[ ${1:-} != --dry-run ]] || { dry=1; shift; }; (($#==0)) || exit 2
[[ $piece == enum20 || $piece == enum30 || $piece == smc || $piece == smcrep ]] || exit 2
[[ $wave =~ ^r[1-9][0-9]*$ ]] || exit 2

[[ $STAMP =~ ^[0-9]{8}T[0-9]{4}Z$ ]] || exit 2
export STAMP
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd); source "$HERE/prodl.env"
SQUEUE=${SQUEUE:-squeue}; SACCT=${SACCT:-sacct}
[[ -r $RUN_HOME/JOBIDS.tsv ]] || { echo 'missing JOBIDS' >&2; exit 3; }
ids=$(awk -F '\t' 'NR>1 {if($3 !~ /^[0-9]+$/) exit 1; print $3}' "$RUN_HOME/JOBIDS.tsv" | paste -sd, -) || exit 3
[[ -n $ids ]] || exit 3
q=$("$SQUEUE" -h -u fb31 -o '%i|%j|%T|%C') || exit 4
if printf '%s\n' "$q" | awk -F'|' -v ids="$ids" 'BEGIN{split(ids,a,",");for(i in a)x[a[i]]=1} NF{split($1,b,"_");if(x[b[1]])f=1} END{exit !f}'; then echo 'active jobs' >&2; exit 3; fi
acct=$("$SACCT" -X -n -P -j "$ids" -o JobID,State) || exit 4
printf '%s\n' "$acct" | awk -F'|' -v ids="$ids" 'BEGIN{split(ids,a,",");for(i in a)x[a[i]]=1} NF>=2{split($1,b,"_");if(x[b[1]]){seen[b[1]]=1;if($2 !~ /^(COMPLETED|FAILED|CANCELLED|TIMEOUT|OUT_OF_MEMORY|NODE_FAIL|DEADLINE|BOOT_FAIL|PREEMPTED)/)bad=1}} END{for(i in x)if(!seen[i])bad=1;exit bad}' || { echo 'accounting not terminal or missing' >&2; exit 3; }


# a CLOSED piece (make_manifests.sh) may already have left scratch: computing a list from a missing folder would resubmit every unit
[[ ! -e $RUN_HOME/manifests/$piece.CLOSED ]] || { echo "REFUSED: $piece is CLOSED ($RUN_HOME/manifests/$piece.CLOSED); its inventory at closing is $RUN_HOME/manifests/$piece.inventory.tsv" >&2; exit 2; }
export RUN_HOME LOG_RUN SCR_ROOT LISTS piece wave dry HERE
"${PYTHON:-python3}" - <<'PY'
import csv, os, pathlib, subprocess, sys
sys.path.insert(0, os.environ["HERE"])
from prodl_verify import verify
from io import StringIO
p=os.environ; piece=p["piece"]; wave=p["wave"]
rows=list(csv.DictReader(open(pathlib.Path(p["LISTS"])/"units.tsv", newline=""),delimiter="\t"))
rows=sorted((r for r in rows if r["piece"]==piece),key=lambda r:(int(r["task"]),r["unit"]))
if not rows: sys.exit("no units")
root=pathlib.Path(p["SCR_ROOT"])/"results"/(p["STAMP"]+"_lowp_"+piece)
stale=set()
if root.exists():
    found=subprocess.run(["bash","-c",'source "$1"; stale_find "$2"',"stale",str(pathlib.Path(p["HERE"])/"stale_lib.sh"),str(root)],capture_output=True,check=True,text=True).stdout
    stale={pathlib.Path(x) for x in found.splitlines()}
selected=[]; exceptions=[]
for row in rows:
    unit=row["unit"]; case=unit.rsplit("_rep",1)[0] if piece=="smcrep" else unit
    folder=pathlib.Path(p["SCR_ROOT"])/"results"/(p["STAMP"]+"_lowp_"+piece)/row["dataset"][:5]/case
    prefix="EXACT" if piece.startswith("enum") else ("SMCBVS" if piece=="smc" else "SMCBVS_rep"+row["repeat"])
    done=folder/(prefix+".done"); side=folder/(prefix+".sha256")
    valid=verify(folder,prefix)[0]
    if valid: continue
    starts=list((pathlib.Path(p["LOG_RUN"])/"ledger"/piece/unit).glob("*.start"))
    if len(starts)>=2: exceptions.append(row); continue
    if folder.exists() and any(folder in x.parents for x in stale):
        print("REFUSED: stale artifacts for "+unit+"; use clear_stale.sh",file=sys.stderr); sys.exit(5)
    selected.append(row)
fields=["piece","task","unit","dataset","scale","repeat"]
def tsv(items, renumber):
    f=StringIO(newline=""); w=csv.DictWriter(f,fields,delimiter="\t",lineterminator="\n"); w.writeheader()
    for i,row in enumerate(items):
        row={k:row[k] for k in fields}
        if renumber: row["task"]=i//25
        w.writerow(row)
    return f.getvalue()
if not selected and not exceptions: print("NOTHING_TO_RESUBMIT"); sys.exit(0)
out=pathlib.Path(p["RUN_HOME"])/"resubmit"
targets=[]
if selected: targets.append((out/(piece+"_"+wave+".tsv"),tsv(selected,True)))
if exceptions: targets.append((out/(piece+"_"+wave+"_exceptions.tsv"),tsv(exceptions,False)))
for path,data in targets:
    if path.exists() and path.read_text()!=data: print("REFUSED: different existing list "+str(path),file=sys.stderr); sys.exit(2)
if p["dry"]=="1":
    print("DRY RUN",len(selected),"resubmit",len(exceptions),"exceptions")
    for r in selected: print("resubmit",r["unit"])
    for r in exceptions: print("exception",r["unit"])
    sys.exit(0)
out.mkdir(parents=True,exist_ok=True)
for path,data in targets:
    if path.exists(): print("SAME_LIST",path)
    else: path.write_text(data)
if not selected: print("NOTHING_TO_RESUBMIT")
PY
