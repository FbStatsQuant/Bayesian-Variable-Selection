#!/bin/bash
set -euo pipefail
STAMP=${1:?}; mode=${2:?}; value=${3:?}; (($#==3)) || exit 2
[[ $mode == --from-scan && ( $value == initial || $value =~ ^r[1-9][0-9]*$ || $value =~ ^final[0-9]*$ ) || $mode == --wave && ( $value == p5 || $value =~ ^p5r[1-9][0-9]*$ ) ]] || exit 2

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


export RUN_HOME LOG_RUN LISTS SCR_ROOT HERE mode value
"${PYTHON:-python3}" - <<'PY'
import csv, pathlib, os, sys, re, io, hashlib, datetime
sys.path.insert(0, os.environ["HERE"])
from prodl_verify import verify
p=os.environ; out=pathlib.Path(p["RUN_HOME"])/"p5"
def put(path, data):
 if path.exists():
  if path.read_text()!=data: print("REFUSED: different existing list",path,file=sys.stderr); sys.exit(2)
  print("SAME_LIST",path)
 else: path.write_text(data)
def table(fields, rows):
 s=io.StringIO(newline=""); w=csv.DictWriter(s,fields,delimiter="\t",lineterminator="\n"); w.writeheader()
 for r in rows: w.writerow(r)
 return s.getvalue()
out.mkdir(parents=True,exist_ok=True)
fields=["piece","task","unit","dataset","scale","repeat","base_piece"]
if p["mode"]=="--wave":
 path=out/"expected.tsv"
 if not path.exists(): sys.exit("missing expected inventory")
 rows=list(csv.DictReader(path.open(newline=""),delimiter="\t")); selected=[]; exceptions=[]
 for r in rows:
  piece=r["base_piece"]; case=r["dataset"]+"_"+r["scale"]
  folder=pathlib.Path(p["SCR_ROOT"])/"results"/(p["STAMP"]+"_lowp_"+piece)/r["dataset"][:5]/case/"P5_retry"
  prefix="SMCBVS"+("_rep"+r["repeat"] if piece=="smcrep" else "")+"_p5retry"
  if verify(folder,prefix)[0]: continue
  if (pathlib.Path(p["LOG_RUN"])/"p5_attempts"/r["unit"]).exists(): exceptions.append(r)
  else: selected.append(r)
 for i,r in enumerate(selected): r["task"]=str(i)
 for name,items in (("units_",selected),("exceptions_",exceptions)):
  target=out/(name+p["value"]+".tsv")
  if target.exists() and target.read_text()!=table(fields,items):
   print("REFUSED: different existing list",target,file=sys.stderr); sys.exit(2)
 for name,items in (("units_",selected),("exceptions_",exceptions)):
  if items: put(out/(name+p["value"]+".tsv"),table(fields,items))
 if not selected: print("NOTHING_TO_SUBMIT")
 sys.exit(0)
phase=p["value"]
if not (pathlib.Path(p["LOG_RUN"])/"p5"/("scan_"+phase+".ok")).is_file(): sys.exit("missing scan receipt: "+phase)
units={}
with open(pathlib.Path(p["LISTS"])/"units.tsv",newline="") as f:
 for r in csv.DictReader(f,delimiter="\t"):
  if r["piece"] in ("smc","smcrep"): units[(r["piece"],r["unit"])]=r
selected=[]
for piece in ("smc","smcrep"):
 path=pathlib.Path(p["LOG_RUN"])/"p5"/("scan_"+phase+"_"+piece+".tsv")
 if not path.is_file(): sys.exit("missing scan "+str(path))
 with path.open(newline="") as f:
  reader=csv.DictReader(f,delimiter="\t")
  if not reader.fieldnames or reader.fieldnames == ['""']: continue
  required={"case_id","base","primary_v3_status","retry_state","eligible","repeat_m"}
  if not required.issubset(reader.fieldnames): sys.exit("invalid scan header")
  for row in reader:
   if row["primary_v3_status"]!="resource_limit": continue
   if row["retry_state"] in ("locked","incomplete","invalid_inspect"):
    print("REFUSED: unsafe retry state "+row["case_id"],file=sys.stderr); sys.exit(2)
   if row["eligible"]!="TRUE": continue
   if row["base"] != ("SMCBVS_rep"+row["repeat_m"] if piece=="smcrep" else "SMCBVS"):
    print("REFUSED: inconsistent scanner base "+row["case_id"],file=sys.stderr); sys.exit(2)
   key=(piece,row["case_id"]+("_rep"+row["repeat_m"] if piece=="smcrep" else ""))
   if key not in units: sys.exit("unknown unit "+str(key))
   selected.append((key,units[key]))
if len({k for k,r in selected}) != len(selected): sys.exit("duplicate P5 units")
hashes=[hashlib.sha256((pathlib.Path(p["LOG_RUN"])/"p5"/("scan_"+phase+"_"+piece+".tsv")).read_bytes()).hexdigest() for piece in ("smc","smcrep")]
if phase=="initial":
 receipt="".join(h+"  scan_initial_"+piece+".tsv\n" for piece,h in zip(("smc","smcrep"),hashes))
 old=out/"scan_initial.receipt"
 if old.exists() and old.read_text()!=receipt:
  print("REFUSED: initial scan receipt mismatch (a different initial scan against an existing inventory; use a new phase with --from-scan)", file=sys.stderr); sys.exit(2)
target=out/"expected.tsv"
expected=[]
if target.exists():
 with target.open(newline="") as f:
  reader=csv.DictReader(f,delimiter="\t")
  if reader.fieldnames != fields: sys.exit("invalid expected inventory header")
  expected=list(reader)
before=len(expected); existing={(r["base_piece"],r["unit"]) for r in expected}
for key,r in sorted(selected):
 if key not in existing:
  expected.append(dict(piece="p5",task=len(expected),unit=r["unit"],dataset=r["dataset"],scale=r["scale"],repeat=r["repeat"],base_piece=key[0]))
  existing.add(key)
if not target.exists(): target.write_text(table(fields,expected))
elif len(expected)>before:
 with target.open("a",newline="") as f:
  w=csv.DictWriter(f,fields,delimiter="\t",lineterminator="\n")
  w.writerows(expected[before:])
history=out/"expected_history.tsv"
with history.open("a",newline="") as f:
 if f.tell()==0: f.write("utc\tphase\tscan_smc_sha256\tscan_smcrep_sha256\trows_before\trows_after\n")
 f.write("\t".join([datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),phase,*hashes,str(before),str(len(expected))])+"\n")
if phase=="initial":
 put(out/"scan_initial.receipt",receipt)
if not expected: put(out/"none_eligible.txt","No eligible units\n")
print("P5 units:",len(expected))
PY
