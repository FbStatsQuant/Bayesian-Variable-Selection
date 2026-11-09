"""Builds D1_raw.csv, D2_raw.csv, D3_raw.csv and D1_summary.md, D2_summary.md, D3_summary.md from RAW_*_raw.csv (written by d123_run.py)."""
import glob
import numpy as np, pandas as pd

files = sorted(glob.glob("RAW_*_raw.csv"))
df = pd.concat([pd.read_csv(f).assign(src=f) for f in files], ignore_index=True)
G = ["scen", "p", "c", "n"]
SC = {2: "S2", 5: "S5"}


def label(k):
    return "%s p=%d c=%g n=%d" % (SC[k[0]], k[1], k[2], k[3])


def rng(s, f="%d"):
    return (f + "-" + f) % (s.min(), s.max())


def md(rows, cols):
    s = "| " + " | ".join(cols) + " |\n|" + "|".join("---" for _ in cols) + "|\n"
    for r in rows:
        s += "| " + " | ".join(str(r[c]) for c in cols) + " |\n"
    return s


def frac(s):
    return "%d/%d" % (int(s.sum()), len(s))


# ---------------- raw splits
common = ["scen", "p", "c", "n", "seed", "B", "K"]
d2cols = common + ["ell_n", "start_size", "n_extra", "n_missing", "start_contains_S0", "start_eq_S0", "symdiff", "start", "extras",
                   "ell_n_S0_scored", "ell_n_final_eq_S0", "ell_n_local_limit", "ell_n_certified", "ell_n_moves", "ell_n_tau", "t_start"]
d3cols = common + ["symdiff", "n_extra", "n_missing", "extra_same_group", "extra_same_block", "extra_elsewhere", "extra_min_idx_dist", "extra_max_idx_dist"]
for nm in ("ell_n", "2ell_n", "size+ell_n", "unc"):
    d3cols += ["%s_cap" % nm, "%s_tau" % nm, "%s_S0_scored" % nm, "%s_final_eq_S0" % nm, "%s_local_limit" % nm, "%s_moves" % nm]
d3cols += ["tau_minus_symdiff", "seq_only_addT_delN", "seq_adds_first", "seq_minimal", "seq_n_addT", "seq_n_addN", "seq_n_delT", "seq_n_delN", "seq_n_swap", "unc_seq", "unc_seq_to_tau"]
d1cols = [c for c in df.columns if c.startswith("D1") or c in common] + ["symdiff"]
df[d2cols].to_csv("D2_raw.csv", index=False)
df[d3cols].to_csv("D3_raw.csv", index=False)
if "D1b_log_sum_nb" in df:
    df[[c for c in d1cols if c in df.columns]].to_csv("D1_raw.csv", index=False)

# ---------------- D2
rows = []
for k, g in df.groupby(G):
    rows.append({"design": label(k), "N": len(g), "|S~0| med (min-max)": "%g (%d-%d)" % (g.start_size.median(), g.start_size.min(), g.start_size.max()),
                 "|S~0 minus S0| med (max)": "%g (%d)" % (g.n_extra.median(), g.n_extra.max()), "|S0 minus S~0| max": g.n_missing.max(),
                 "S~0 contains S0": frac(g.start_contains_S0), "S~0 = S0": frac(g.start_eq_S0), "ell_n": g.ell_n.iloc[0],
                 "S0 scored": frac(g.ell_n_S0_scored), "final = S0": frac(g.ell_n_final_eq_S0), "local_limit": frac(g.ell_n_local_limit),
                 "moves med (max)": "%g (%d)" % (g.ell_n_moves.median(), g.ell_n_moves.max())})
D2 = md(rows, list(rows[0].keys()))
open("D2_summary.md", "w").write("## D2: LS0 with the production cap ell_n = ceil(log2(n+p+1)) from the start mode (script d123_run.py -> RAW_*_raw.csv -> D2_raw.csv)\n\n" + D2)

# ---------------- D3
rowsA, rowsB, rowsC = [], [], []
for k, g in df.groupby(G):
    r = {"design": label(k), "N": len(g), "sym-diff med (max)": "%g (%d)" % (g.symdiff.median(), g.symdiff.max())}
    for nm in ("ell_n", "2ell_n", "size+ell_n", "unc"):
        capv = ("%d" % g["%s_cap" % nm].iloc[0]) if nm != "size+ell_n" else ("%d-%d" % (g["%s_cap" % nm].min(), g["%s_cap" % nm].max()))
        r["cap=" + nm] = "[%s] reach %s, scored %s, final=S0 %s, limit %s" % (capv, frac(g["%s_tau" % nm] >= 0), frac(g["%s_S0_scored" % nm]), frac(g["%s_final_eq_S0" % nm]), frac(g["%s_local_limit" % nm]))
    rowsA.append(r)
    ok = g[g.unc_tau >= 0]
    rowsB.append({"design": label(k), "N": len(g), "unc reaches S0": frac(g.unc_tau >= 0), "tau med (max)": "%g (%d)" % (ok.unc_tau.median(), ok.unc_tau.max()) if len(ok) else "NA",
                  "tau <= |symdiff|": frac(ok.tau_minus_symdiff <= 0), "max (tau - |symdiff|)": int(ok.tau_minus_symdiff.max()) if len(ok) else "NA",
                  "tau == |symdiff|": frac(ok.seq_minimal), "only +T/-N tokens": frac(ok.seq_only_addT_delN), "adds first then dels (only +T,-N)": frac(ok.seq_adds_first),
                  "#swaps (total)": int(ok.seq_n_swap.sum()), "#+N": int(ok.seq_n_addN.sum()), "#-T": int(ok.seq_n_delT.sum()), "#+T": int(ok.seq_n_addT.sum()), "#-N": int(ok.seq_n_delN.sum())})
    tot = g.n_extra.sum()
    rowsC.append({"design": label(k), "|S~0 minus S0| mean": "%.1f" % g.n_extra.mean(), "median": g.n_extra.median(), "max": g.n_extra.max(),
                  "same group as truth": "%d (%.0f%%)" % (g.extra_same_group.sum(), 100 * g.extra_same_group.sum() / max(tot, 1)),
                  "same block (not same group)": "%d (%.0f%%)" % (g.extra_same_block.sum(), 100 * g.extra_same_block.sum() / max(tot, 1)),
                  "elsewhere": "%d (%.0f%%)" % (g.extra_elsewhere.sum(), 100 * g.extra_elsewhere.sum() / max(tot, 1)), "min idx-dist to a truth (pooled)": g.extra_min_idx_dist[g.extra_min_idx_dist >= 0].min() if (g.extra_min_idx_dist >= 0).any() else "NA"})
D3 = "### D3a larger caps\n\n" + md(rowsA, list(rowsA[0].keys())) + "\n### D3b uncapped path (from start mode): tau and move types up to tau\n\n" + md(rowsB, list(rowsB[0].keys())) + \
     "\n### D3c growth and location of the extras S~0 minus S0\n\n" + md(rowsC, list(rowsC[0].keys()))
open("D3_summary.md", "w").write("## D3: LS0 with larger caps (script d123_run.py -> RAW_*_raw.csv -> D3_raw.csv)\n\n" + D3)

# ---------------- D1
D1 = ""
if "D1b_log_sum_nb" in df:
    rowsD = []
    for k, g in df.groupby(G):
        rowsD.append({"design": label(k), "N": len(g),
                      "(a) F(S0)-max F, LS-scored: min / #<0": "%.2f / %d" % (g.D1a_LS_F_S0_minus_max.min(), (g.D1a_LS_F_S0_minus_max < -1e-9).sum()),
                      "(a) same incl. MC3-proposed: min / #<0": "%.2f / %d" % (g.D1a_all_F_S0_minus_max.min(), (g.D1a_all_F_S0_minus_max < -1e-9).sum()),
                      "(a) best = S0 (LS)": frac(g.D1a_LS_best_eq_S0),
                      "(b) log sum_N exp(F(N)-F(S0)) med [min,max]": "%.2f [%.2f, %.2f]" % (g.D1b_log_sum_nb.median(), g.D1b_log_sum_nb.min(), g.D1b_log_sum_nb.max()),
                      "(b) #runs with a better neighbour": frac(g.D1b_max_nb_gap > 0),
                      "(c) frac time at S0, 2nd half: med [min,max]": "%.3f [%.3f, %.3f]" % (g.D1c_frac_S0_second_half.median(), g.D1c_frac_S0_second_half.min(), g.D1c_frac_S0_second_half.max()),
                      "(c) frac at supersets of S0 (med)": "%.3f" % g.D1c_frac_supset_S0_second_half.median(),
                      "(c) best visited = S0": frac(g.D1c_best_visited_eq_S0), "(c) acc": "%.3f" % g.D1c_accept.median(),
                      "LS from {} ends at S0": ("%d/%d" % (g[g.D1_LS_empty_done==True].D1_LS_empty_final_eq_S0.astype(bool).sum(), (g.D1_LS_empty_done==True).sum()) if (g.D1_LS_empty_done==True).any() else "not run"), "LS from S0 stays": frac(g.D1_LS_S0_final_eq_S0.astype(bool))})
    D1 = md(rowsD, list(rowsD[0].keys()))
open("D1_summary.md", "w").write("## D1: posterior concentration on S0 (script d123_run.py -> RAW_*_raw.csv -> D1_raw.csv)\n\n" + D1)
print(open("D2_summary.md").read()); print(open("D3_summary.md").read()); print(open("D1_summary.md").read())
