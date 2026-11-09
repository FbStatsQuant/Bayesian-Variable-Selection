"""Pooled counts over all RAW_*_raw.csv runs (used for 'Findings that matter') -> POOLED.md"""
import glob
import numpy as np, pandas as pd
df = pd.concat([pd.read_csv(f) for f in sorted(glob.glob("RAW_*_raw.csv"))], ignore_index=True)
out = ["## Pooled counts (script build_pooled.py <- RAW_*_raw.csv)\n"]
def line(name, g):
    ok = g[g.unc_tau >= 0]
    nsw = (ok.seq_n_swap > 0).sum()
    out.append("| %s | %d | %d | %d | %d | %d | %d | %d | %d | %d | %d |" % (name, len(g), len(ok), ok.seq_only_addT_delN.sum(), ok.seq_adds_first.sum(), (ok.tau_minus_symdiff <= 0).sum(),
        int(ok.tau_minus_symdiff.max()) if len(ok) else -99, nsw, int(ok.seq_n_swap.sum()), int(ok.seq_n_addN.sum()), int(ok.seq_n_delT.sum())))
hdr = "| subset | runs | uncapped reaches S0 | only +T/-N tokens | +T before all -N | tau <= |symdiff| | max(tau-|symdiff|) | runs with a swap before tau | #swaps | #+N | #-T |\n|---|---|---|---|---|---|---|---|---|---|---|"
out.append(hdr)
line("all runs", df)
for scen in (2, 5):
    for p in sorted(df.p.unique()):
        g = df[(df.scen == scen) & (df.p == p)]
        if len(g): line("S%d p=%d" % (scen, p), g)
# swaps: which kinds
import collections
cnt = collections.Counter()
for s in df.unc_seq_to_tau.dropna():
    if s == "NA": continue
    for t in str(s).split(): cnt[t] += 1
out.append("\nToken counts up to tau over all runs reaching S0: " + ", ".join("%s: %d" % kv for kv in sorted(cnt.items())))
# swaps: position in the sequence
pos = collections.Counter()
for s in df.unc_seq_to_tau.dropna():
    if s == "NA": continue
    toks = str(s).split()
    for i, t in enumerate(toks):
        if t.startswith("sw"): pos[(t, "first" if i == 0 or all(x.startswith("sw") for x in toks[:i]) else "later")] += 1
out.append("Swap tokens: position (leading block of swaps vs after a non-swap move): " + ", ".join("%s %s: %d" % (k[0], k[1], v) for k, v in sorted(pos.items())))
# D1 pooled
d1 = df[df.D1b_log_sum_nb.notna()]
out.append("\n### D1 pooled\n")
out.append("runs: %d; runs with F(S0) < max F over LS-scored models: %d; incl. MC3-proposed: %d; runs with a better one-flip/swap neighbour than S0: %d; MC3 best visited = S0: %d" % (
    len(d1), (d1.D1a_LS_F_S0_minus_max < -1e-9).sum(), (d1.D1a_all_F_S0_minus_max < -1e-9).sum(), (d1.D1b_max_nb_gap > 0).sum(), d1.D1c_best_visited_eq_S0.sum()))
b = d1[d1.D1a_all_F_S0_minus_max < -1e-9]
out.append("beaten runs by (scen, p, n): " + ", ".join("S%d p=%d c=%g n=%d seed=%d (%.2f, best symdiff to S0 = %d)" % (r.scen, r.p, r.c, r.n, r.seed, r.D1a_all_F_S0_minus_max, r.D1a_LS_best_symdiff) for r in b.itertuples()))
out.append("max over runs of the symmetric difference between S0 and the best model found (LS union): %d; of those beating S0: %s" % (d1.D1a_LS_best_symdiff.max(), sorted(b.D1a_LS_best_symdiff.unique().tolist())))
out.append("MC3 fraction of the second half at supersets of S0: min over all runs %.3f" % d1.D1c_frac_supset_S0_second_half.min())
open("POOLED.md", "w").write("\n".join(out) + "\n")
print("\n".join(out))
