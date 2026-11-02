"""Aggregate results/route.jsonl into results/route_table.txt (API-PXNGAP)."""
import json, math, collections
R = [json.loads(l) for l in open("results/route.jsonl")]
G = collections.defaultdict(list)
for r in R: G[(r["cfg"], r["n"], r["p"])].append(r)
print("cfg   n    p   reps blocks=grp mode=S° |min(1-pi0(S°)) med max| med log pi0(S0) | LS0 scored S0 | certified | path=c in lattice | min D_S margin | min (L) margin | q med")
for k in sorted(G):
    rs = G[k]; m = len(rs)
    one = [1 - math.exp(r["log_pi0_ref"]) for r in rs]
    print(f"{k[0]:3s} {k[1]:5d} {k[2]:5d} {m:3d}   {sum(r['blocks_eq_groups'] for r in rs):3d}/{m}    {sum(r['mode_eq_ref'] for r in rs):3d}/{m}  "
          f"{min(one):.3f} {sorted(one)[m//2]:.3f} {max(one):.3f}   {sorted(r['log_pi0_S0'] for r in rs)[m//2]:7.2f}    "
          f"{sum(r['ls_scored_S0'] for r in rs):3d}/{m}      {sum(r['ls_certified'] and r['ls_end_is_S0'] for r in rs):3d}/{m}    "
          f"{sum(r['ls_path_len']==r['c'] and r['ls_path_in_lattice'] for r in rs):3d}/{m}        "
          f"{min(r['min_DS_margin'] for r in rs):7.2f}      {min(r['L_margin'] for r in rs):7.2f}   {sorted(r['q'] for r in rs)[m//2]:.3f}")
print("(L) failures (L_margin < 0):", sum(r["L_margin"] < 0 for r in R), "of", len(R))
print("D_S failures (min_DS_margin <= 0):", sum(r["min_DS_margin"] <= 0 for r in R), "of", len(R))
