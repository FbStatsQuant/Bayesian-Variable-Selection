#!/usr/bin/env bash
# Validation: W2-FAC-S5 s1_path.py (candidate swaps every step) vs W2-SIM S5 s5p_exact.py (SWAP_ALL_P large => swaps every step)
T=../../../W2-FAC-S5/numerics
export BCS_CORE_DIR=$T
sha256sum $T/bcs_core.py $T/s1_path.py ../scripts/s5p_exact.py > val_s5p_sha256.txt
: > val_s5p_orig.jsonl; : > val_s5p_new.jsonl
for c in "500 1e6 1" "200 1e4 3" "1000 2000 2" "400 1000 1" "300 1e3 2 3 .2 .6"; do
  set -- $c
  (cd $T && py -3.13 s1_path.py $c) >> val_s5p_orig.jsonl &
  if [ $# -gt 3 ]; then py -3.13 ../scripts/s5p_exact.py $c 1000000 > tmp_$$.json; else py -3.13 ../scripts/s5p_exact.py $c 5 .3 .7 1000000 > tmp_$$.json; fi
  wait; cat tmp_$$.json >> val_s5p_new.jsonl; rm tmp_$$.json
done
py -3.13 - <<'PY' > val_s5p_compare.txt
import json, math
o=[json.loads(l) for l in open("val_s5p_orig.jsonl")]; nw=[json.loads(l) for l in open("val_s5p_new.jsonl")]
ok=True
for a,b in zip(o,nw):
    pairs=[("moves","moves"),("n_delN","n_delN"),("n_addN","n_addN"),("n_delT","n_delT"),("n_swap",None),("final_is_S0","final_is_S0"),
           ("pure_deletion","pure_deletion"),("nonargmin","nonargmin")]
    res={}
    for x,y in pairs:
        bv = (b["n_swapN"]+b["n_swapT"]) if y is None else b[y]
        res[x]=(a[x]==bv)
    res["add_over_logn"]=abs(a["add_over_logn"]-b["best_add_max"]/math.log(a["n"]))<1e-12
    res["f_ratio"]=abs(a["f_ratio"]-max(b["ratio_bulk"],b["ratio_end"]))<1e-12
    res["eT_over_H"]=abs(a["eT_over_H"]-max(b["eT_bulk"],b["eT_end"]))<1e-12
    res["swapmargin"]=abs(a["swapmargin_over_logn"]-max(b["swap_minus_del_bulk"],b["swap_minus_del_end"]))<1e-12
    allok=all(res.values()); ok&=allok
    print(a["p"],a["n"],a["seed"],a["q"],"moves",a["moves"],"pure",a["pure_deletion"],"S0",a["final_is_S0"],"| all agree:",allok, "" if allok else res)
print("ALL AGREE:",ok,"cases:",len(o))
PY
cat val_s5p_compare.txt
