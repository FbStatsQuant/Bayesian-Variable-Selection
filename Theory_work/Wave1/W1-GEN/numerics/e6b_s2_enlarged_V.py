"""E6b (extra): S2 (AR(1), rho=.5), p=100: SEP ratio zeta/(n theta_min^2) as V is enlarged by r neighbouring groups on each side of each signal group.
For |V|>20 the sweep is the restricted family (lower bound for zeta)."""
import json, time
import numpy as np
import bvs_core as bc, study_common as sc

if __name__ == "__main__":
    t0 = time.time()
    spec = sc.spec_cached(2, 100, 4, 5, 1.0)
    pop = bc.Pop(spec["Sigma"], spec["theta"], 2)
    act_groups = sorted({j // 5 for j in spec["S0"]})
    rows = []
    for r in (0, 1, 2):
        gs = sorted({g for a in act_groups for g in range(a - r, a + r + 1) if 0 <= g < 20})
        V = tuple(sorted(j for g in gs for j in range(5 * g, 5 * g + 5)))
        out = bc.sep_and_decrement(pop, V, rng=np.random.default_rng(1), exhaustive_max=20, S0=spec["S0"])
        rows.append(dict(r=r, V_size=len(V), exhaustive=out["exhaustive"], zeta_ratio=round(out["zeta"] / pop.theta_min ** 2, 5), zeta_arg=str(out["zeta_arg"]), dec_unit=round(out["dec"], 4)))
        print(rows[-1], flush=True)
    json.dump(rows, open("E6b_summary.json", "w"), indent=1)
    with open("E6b_summary.md", "w") as f:
        f.write("## E6b (extra) S2 AR(1) 0.5, p=100: SEP ratio vs size of V (V = signal groups +- r groups)\n\n| r | |V| | exhaustive | zeta/(n theta_min^2) | argmax (S, l) | Lemma-3 decrement (unit, x(n-1)c^2) |\n|---|---|---|---|---|---|\n")
        for r in rows:
            f.write(f"| {r['r']} | {r['V_size']} | {r['exhaustive']} | {r['zeta_ratio']} | {r['zeta_arg']} | {r['dec_unit']} |\n")
    print("secs", time.time() - t0)
