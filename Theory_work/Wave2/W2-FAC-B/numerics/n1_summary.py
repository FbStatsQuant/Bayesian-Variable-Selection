import json, sys, math, collections
import numpy as np
rows = [json.loads(l) for l in open(sys.argv[1] if len(sys.argv) > 1 else "N1_raw.jsonl")]
err = [r for r in rows if "error" in r]
rows = [r for r in rows if "error" not in r]
g = collections.defaultdict(list)
for r in rows:
    g[(r["design"], r["p"], r["c"], r["n"])].append(r)
print("errors:", len(err), [e["error"][:80] for e in err[:3]])
hdr = "| design | p | c | n | A=log p/log n | N | K | start size med (min-max) | start=[p] | S0 in start | moves - symdiff max | #swap tot | #+N tot | #-T tot | final=S0 | scored S0 | max NA margin / log n (max over path) | min delN gain | max delT gain |"
print(hdr); print("|" + "---|" * (hdr.count("|") - 1))
for key in sorted(g):
    R = g[key]; d, p, c, n = key
    ss = [r["start_size"] for r in R]
    print(f"| {d} | {p} | {c} | {n:.0e} | {math.log(p)/math.log(n):.2f} | {len(R)} | {R[0]['K']} | {int(np.median(ss))} ({min(ss)}-{max(ss)}) | "
          f"{sum(r['start_is_full'] for r in R)}/{len(R)} | {sum(r['start_has_S0'] for r in R)}/{len(R)} | "
          f"{max(r['moves'] - r['symdiff'] for r in R)} | {sum(r['n_swap'] for r in R)} | {sum(r['n_addN'] for r in R)} | {sum(r['n_delT'] for r in R)} | "
          f"{sum(r['final_is_S0'] for r in R)}/{len(R)} | {sum(r['scored_S0'] for r in R)}/{len(R)} | {max(r['max_best_add_over_logn'] for r in R):.3f} | "
          f"{min(r['min_best_delN_on_path'] for r in R if r['min_best_delN_on_path']==r['min_best_delN_on_path']) if any(r['min_best_delN_on_path']==r['min_best_delN_on_path'] for r in R) else float('nan'):.2f} | {max(r['max_best_delT'] for r in R):.1f} |")
