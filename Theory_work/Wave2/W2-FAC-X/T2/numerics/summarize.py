"""summarize.py -- tables for T2/numerics/N_T2_summary.md from T2_raw.jsonl and T2_stress_raw.jsonl."""
import json, collections, sys
for fn in sys.argv[1:]:
    R = [json.loads(l) for l in open(fn)]
    print("==", fn, len(R), "runs; pure deletion", sum(r["pure_deletion"] for r in R), "; final S0", sum(r["final_is_S0"] for r in R),
          "; runs with interval-hole violation", sum(r["interval_viol_steps"] > 0 for r in R), "; ties", sum(r["ties"] for r in R))
    g = collections.defaultdict(list)
    for r in R:
        g[r["design"]].append(r)
    print("design         R     A_S     max lp/ln  S0/runs  max add/ln  min del/ln  max sw-del  max truth  viol  max cr  bulk max|X|/H  bulk max D_c/(2l_c H)  bulk 1-sided steps")
    for d, L in g.items():
        print("%-14s %5.1f %.4f  %.2f      %3d/%-3d  %+.3f     %+.3f     %+.2f     %.1e  %d     %.2f    %.3f          %.3f                  %d" % (
            d, L[0]["R"], min(x["A_S"] for x in L), max(x["logp_logn"] for x in L), sum(x["final_is_S0"] for x in L), len(L),
            max(x["max_add_over_logn"] for x in L), min(x["min_best_del_over_logn"] for x in L),
            max(x["max_swap_minus_del"] for x in L), max(x["max_truth"] for x in L), sum(x["interval_viol_steps"] for x in L),
            max(x["max_centre_ratio"] for x in L), max(x.get("bulk_absX", 0) for x in L),
            max(x.get("bulk_delta_over_l", 0) for x in L), max(x.get("bulk_onesided_steps", 0) for x in L)))
    bad = [r for r in R if not (r["pure_deletion"] and r["final_is_S0"])]
    for r in bad:
        print("  NOT pure/S0:", r["design"], r["truth"], r["n"], r["p"], r["seed"], r["types"], r["final_is_S0"])
