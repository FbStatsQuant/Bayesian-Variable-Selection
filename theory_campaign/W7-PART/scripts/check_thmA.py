"""Check of Theorem A (PROOF.md §1): (C*) holds  <=>  the full complete-linkage dendrogram is laminar w.r.t. the
groups (a.s.), and laminar + g_max <= B < 2 g_min  =>  blocks = groups. Also: local margin (M) => (C*).
Hard regimes (failures common) so that both outcomes occur. Seed fixed. Output: results/check_thmA.txt"""
import numpy as np
from part_core import *

rng = np.random.default_rng(31)
rows = []
tot = dict(n=0, agree=0, lam=0, beq=0, lam_and_not_beq=0, beq_and_not_lam=0, M=0, M_not_C=0)
configs = [(200, 30, 10, 0.3, 0.0, "indep"), (200, 30, 10, 0.35, 0.0, "indep"), (100, 20, 10, 0.4, 0.0, "indep"),
           (200, 20, 10, 0.7, 0.62, "lh"), (200, 20, 10, 0.7, 0.68, "lh"), (200, 20, 12, 0.5, 0.33, "global"),
           (200, 30, 9, 0.45, 0.0, "indep"), (150, 16, 12, 0.4, 0.0, "indep")]
for (n, G, g, rho, psi, kind) in configs:
    c = dict(n=0, agree=0, lam=0, beq=0)
    for rep in range(40):
        X, groups = gen_groups(n, G, g, rho, psi, kind, rng)
        r = correlation(X)
        p = r.shape[0]
        B = 14 if g <= 14 else 16
        T = complete_linkage_faithful(r)
        lam = laminar(T, p, groups)
        nv = cstar_violations(r, groups)
        blocks, _ = cut_and_pack(T, p, B)
        beq = blocks_equal_groups(blocks, groups)
        m_loc, _ = margins(r, groups)
        c["n"] += 1; c["agree"] += (lam == (nv == 0)); c["lam"] += lam; c["beq"] += beq
        tot["n"] += 1; tot["agree"] += (lam == (nv == 0)); tot["lam"] += lam; tot["beq"] += beq
        tot["lam_and_not_beq"] += lam and not beq; tot["beq_and_not_lam"] += beq and not lam
        tot["M"] += m_loc > 0; tot["M_not_C"] += (m_loc > 0) and nv > 0
    rows.append(f"n={n} G={G} g={g} rho={rho} psi={psi} {kind:6s} B={B}: reps={c['n']} (C*)<=>laminar agree={c['agree']} "
                f"laminar={c['lam']} blocks=groups={c['beq']}")
rows.append(f"TOTAL reps={tot['n']}: (C*)<=>laminar agreement {tot['agree']}/{tot['n']}; laminar {tot['lam']}; "
            f"blocks=groups {tot['beq']}; laminar & blocks!=groups {tot['lam_and_not_beq']}; "
            f"blocks=groups & not laminar {tot['beq_and_not_lam']}; local margin (M) held {tot['M']}, "
            f"(M) & not (C*) {tot['M_not_C']}")
open("../results/check_thmA.txt", "w").write("\n".join(rows) + "\n")
print("\n".join(rows))
