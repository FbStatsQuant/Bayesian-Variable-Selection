"""Growth of |S~0 minus S0| and |S~0| with n and p (c = 1; and c = 0.5 for S5) -> D3_growth_summary.md ; and D1 p/n table of log-sum / chain mass."""
import glob
import numpy as np, pandas as pd
df = pd.concat([pd.read_csv(f) for f in sorted(glob.glob("RAW_*_raw.csv"))], ignore_index=True)
SC = {2: "S2", 5: "S5"}
out = "## D3 growth: |S~0 minus S0| (median; max) and |S~0| (median) by n and p, c as stated (script build_growth.py <- RAW_*_raw.csv)\n\n"
for scen in (5, 2):
    for c in (1.0, 0.5):
        g = df[(df.scen == scen) & (df.c == c)]
        if g.empty: continue
        ps = sorted(g.p.unique()); ns = sorted(g.n.unique())
        out += "### %s, c = %g: |S~0 minus S0| median (max) [|S~0| median] [runs]\n\n| n | " % (SC[scen], c) + " | ".join("p=%d" % p for p in ps) + " |\n|---|" + "---|" * len(ps) + "\n"
        for n in ns:
            cells = []
            for p in ps:
                h = g[(g.p == p) & (g.n == n)]
                cells.append("%g (%d) [%g] [%d]" % (h.n_extra.median(), h.n_extra.max(), h.start_size.median(), len(h)) if len(h) else "-")
            out += "| %d | " % n + " | ".join(cells) + " |\n"
        out += "\n"
out += "### ratio |S~0 minus S0| / sqrt(n), S5 c = 1 and c = 0.5, medians (the true number of blocks J is in D3e)\n\n| c | p | n | runs | median extras | extras/sqrt(n) |\n|---|---|---|---|---|---|\n"
for c in (1.0, 0.5):
    g = df[(df.scen == 5) & (df.c == c)]
    for (p, n), h in g.groupby(["p", "n"]):
        out += "| %g | %d | %d | %d | %g | %.2f |\n" % (c, p, n, len(h), h.n_extra.median(), h.n_extra.median() / np.sqrt(n))
# D1 by (scen, p, n): log-sum over neighbours, add part, chain mass
d1 = df[df.D1b_log_sum_nb.notna()]
out += "\n## D1 supplement: medians over runs of log sum_N exp(F(N)-F(S0)) [all / adds only / deletes only / swaps only] and MC3 mass at S0 (second half), c = 1\n\n| design | n | runs | log-sum all | adds | deletes | swaps | MC3 frac at S0 (2nd half) |\n|---|---|---|---|---|---|---|---|\n"
for (scen, p, n), h in d1[d1.c == 1.0].groupby(["scen", "p", "n"]):
    out += "| %s p=%d | %d | %d | %.2f | %.2f | %.2f | %.2f | %.3f |\n" % (SC[scen], p, n, len(h), h.D1b_log_sum_nb.median(), h.D1b_log_sum_add.median(), h.D1b_log_sum_del.median(), h.D1b_log_sum_swap.median(), h.D1c_frac_S0_second_half.median())
open("D3_growth_summary.md", "w").write(out)
print(out)
