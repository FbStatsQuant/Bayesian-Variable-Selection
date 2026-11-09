#!/usr/bin/env bash
# Validation: original W2-FAC-S5 s3_cc.py vs W2-SIM S5 s5cc.py (original fields must be identical).
# Run from this directory: bash validate_s5cc.sh  (local PC, py -3.13; numpy 2.3.0, scipy 1.15.3)
T=../../../W2-FAC-S5/numerics
export BCS_CORE_DIR=$T
sha256sum $T/bcs_core.py $T/s3_cc.py ../scripts/s5cc.py > val_sha256.txt
: > val_orig.jsonl; : > val_new.jsonl
for c in "500 1e12 1" "500 1e4 3" "2000 1e6 2" "1000 1e20 5" "600 1e12 1 3 .2 .6" "1200 1e8 4 3 .2 .6"; do
  (cd $T && py -3.13 s3_cc.py $c) >> val_orig.jsonl &
  py -3.13 ../scripts/s5cc.py $c > "new_$(echo $c | tr ' ' _).json" &
  wait
  cat "new_$(echo $c | tr ' ' _).json" >> val_new.jsonl; rm "new_$(echo $c | tr ' ' _).json"
done
py -3.13 - <<'PY' > val_compare.txt
import json
o=[json.loads(l) for l in open("val_orig.jsonl")]; nw=[json.loads(l) for l in open("val_new.jsonl")]
ok=True
for a,b in zip(o,nw):
    same=all(a[k]==b[k] for k in a)
    ok&=same
    print(a["p"],a["n"],a["seed"],"original fields identical:",same, "| r_bulk %.4f r_mid %.4f r_end %.4f I30/10/5 %s/%s/%s"%(b["r_bulk"],b["r_mid"],b["r_end"],b["I30"],b["I10"],b["I5"]))
print("ALL IDENTICAL:", ok, "cases:", len(o))
PY
cat val_compare.txt
