"""n0_aggregate.py -- builds the markdown tables of NUMERICS_LOC_VN.md from n1_results.csv, n2_results.csv, n3_results.csv, n3b_results.csv.
Writes agg_tables.md."""
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
L = []


def md(df, floatfmt="%.3g"):
    cols = list(df.columns)
    out = ["| " + " | ".join(str(c) for c in cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.astype(object).iterrows():
        cells = []
        for c in cols:
            v = r[c]
            cells.append((floatfmt % v) if isinstance(v, (float, np.floating)) and not isinstance(v, bool) else str(v))
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


# ------------------------------------------------------------------ n1
d = pd.read_csv(os.path.join(HERE, "n1_results.csv"))
g = d.groupby(["design", "n", "r"]).agg(
    max_dZ=("max_dz", "max"), med_dZ=("med_dz", "mean"), max_sd=("max_sd", "max"), med_sd=("med_sd", "mean"),
    max_popvar=("max_pv", "max"), med_popvar=("med_pv", "mean"), max_sd_far=("max_sd_far", "max"),
    sd_over_sqrt_nout_over_n_med=("med_sd_over_sqrt_nout_n", "mean")).reset_index()
L.append("## n1 table (max over 5 seeds of the per-seed max; 'med' = mean over seeds of the per-seed median)\n")
L.append("columns: max_dZ = max |Z-Z'| (one fixed eps per seed); med_dZ = median |Z-Z'|; max_sd / med_sd = sqrt(Var(Z-Z'|design)) = ||u-ghat||; "
         "max_popvar / med_popvar = Var(E[W_l|W_T]-E[W_l|W_T']); max_sd_far = max_sd over the 50 far l only; last = median of sd / sqrt(|T minus T'|/n).\n")
for dsg in ["L1", "L2", "L3", "L4"]:
    L.append("### %s\n" % dsg)
    L.append(md(g[g.design == dsg].drop(columns=["design"])))
    L.append("")
# n-scaling for L4 r>=1: max_sd * sqrt(n)
L.append("### L4 (AR(1)) scaling of max_sd (sd of Z-Z'), r>=1: max_sd*sqrt(n) and max_sd*sqrt(n)/log n\n")
t = g[(g.design == "L4") & (g.r >= 1)].copy()
t["max_sd*sqrt(n)"] = t.max_sd * np.sqrt(t.n)
t["max_sd*sqrt(n)/log n"] = t.max_sd * np.sqrt(t.n) / np.log(t.n)
t["max_dZ*sqrt(n)/log n"] = t.max_dZ * np.sqrt(t.n) / np.log(t.n)
L.append(md(t[["n", "r", "max_sd", "max_sd*sqrt(n)", "max_sd*sqrt(n)/log n", "max_dZ", "max_dZ*sqrt(n)/log n"]]))
L.append("")
# mean |T| info
L.append("mean over pairs of |T minus T'| at r=8: " + ", ".join("%s n=%d: %.1f" % (a, b, c) for (a, b), c in d[d.r == 8].groupby(["design", "n"]).mean_nout.mean().items()) + "\n")

# ------------------------------------------------------------------ n2
d2 = pd.read_csv(os.path.join(HERE, "n2_results.csv"))
g2 = d2.groupby(["design", "n", "p"]).agg(
    runs=("seed", "count"), S0_in_start=("S0_in_mode", "sum"), start_size_mean=("mode_size", "mean"),
    extra_mean=("n_extra", "mean"), extra_max=("n_extra", "max"), maxdist_extra=("maxdist_extra", "max"),
    LS_S0_scored=("ls_S0_scored", "sum"), LS_final_eq_S0=("ls_final_eq_S0", "sum"), LS_certified=("ls_certified", "sum"),
    LS_capped=("ls_limit", "sum"), moves_mean=("ls_moves", "mean"), moves_max=("ls_moves", "max"),
    B=("B", "first"), nblocks=("nblocks", "mean"), blk_min=("blk_min", "min"), blk_max=("blk_max", "max"), blk_mean=("blk_mean", "mean"),
    truths_in_distinct_blocks=("truths_in_distinct_blocks", "sum"), start_truncated=("start_truncated", "sum"), max_secs=("secs", "max")).reset_index()
L.append("## n2 table (6 seeds per cell; counts are out of 6)\n")
L.append(md(g2))
L.append("")
bad = d2[~d2.ls_final_eq_S0][["design", "n", "p", "seed", "S0", "mode", "n_extra", "ls_final_size", "ls_final_symdiff", "ls_certified", "ls_S0_scored"]]
L.append("### n2: data sets where the LS0 endpoint != S0\n")
L.append(md(bad) if len(bad) else "none")
L.append("")
far = d2[d2.maxdist_extra > 8][["design", "n", "p", "seed", "S0", "mode", "maxdist_extra"]]
L.append("### n2: data sets with a start-mode extra at index distance > 8 from S0\n")
L.append(md(far) if len(far) else "none")
L.append("")
L.append("### n2: block-size histograms (first seed of each cell; size:count)\n")
h = d2[d2.seed == 1][["design", "n", "p", "B", "blk_hist"]]
L.append(md(h))
L.append("")

# ------------------------------------------------------------------ n3
d3 = pd.read_csv(os.path.join(HERE, "n3_results.csv"))
p3 = os.path.join(HERE, "n3b_results.csv")
if os.path.exists(p3):
    d3b = pd.read_csv(p3)
    key = ["design", "n", "p", "seed"]
    d3 = d3.merge(d3b[key + ["ls_moves", "ls_certified", "ls_limit", "ls_timed_out", "ls_S0_scored", "ls_S0_on_path", "ls_final_eq_S0", "ls_final_size", "ls_final_symdiff", "ell"]],
                  on=key, how="left", suffixes=("", "_b"))
    for c in ["ls_moves", "ls_certified", "ls_limit", "ls_timed_out", "ls_S0_scored", "ls_S0_on_path", "ls_final_eq_S0", "ls_final_size", "ls_final_symdiff", "ell"]:
        d3[c] = np.where(d3[c + "_b"].notna(), d3[c + "_b"], d3[c])
        d3.drop(columns=[c + "_b"], inplace=True)
    for c in ["ls_certified", "ls_limit", "ls_timed_out", "ls_S0_scored", "ls_S0_on_path", "ls_final_eq_S0"]:
        d3[c] = d3[c].astype(bool)
d3["bound_met"] = d3.n_visible_in_mode >= d3.lemma_bound
g3 = d3.groupby(["design", "n", "p"]).agg(
    runs=("seed", "count"), s0=("s0", "first"), K=("K", "first"), B=("B", "first"), start_size_mean=("mode_size", "mean"), start_size_min=("mode_size", "min"), start_size_max=("mode_size", "max"),
    extra_mean=("n_extra", "mean"), S0_in_start=("S0_in_mode", "sum"), n_visible=("n_visible", "first"), vis_in_start_mean=("n_visible_in_mode", "mean"),
    vis_in_start_min=("n_visible_in_mode", "min"), lemma_bound=("lemma_bound", "first"), bound_met=("bound_met", "sum"),
    LS_S0_scored=("ls_S0_scored", "sum"), LS_final_eq_S0=("ls_final_eq_S0", "sum"), LS_certified=("ls_certified", "sum"), LS_capped=("ls_limit", "sum"),
    LS_unfinished=("ls_timed_out", "sum"), moves_mean=("ls_moves", "mean"), moves_max=("ls_moves", "max")).reset_index()
L.append("## n3 table (4 seeds per cell; counts out of 4). visible = V1 leaves / V2 nulls in truth blocks / V3 all nulls; lemma_bound = min(K-s0, |visible|-16 s0)\n")
L.append(md(g3))
L.append("")
L.append("### n3 per data set (start/LS detail)\n")
L.append(md(d3[["design", "n", "p", "seed", "s0", "mode_size", "n_extra", "maxdist_extra", "n_visible_in_mode", "n_visible", "lemma_bound", "ell", "ls_moves", "ls_certified", "ls_limit", "ls_timed_out", "ls_S0_scored", "ls_final_eq_S0", "ls_final_size"]]))
d3.to_csv(os.path.join(HERE, "n3_merged.csv"), index=False)
open(os.path.join(HERE, "agg_tables.md"), "w", encoding="utf-8").write("\n".join(L))
print("\n".join(L))
