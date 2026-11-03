"""abess_summary.py ABESS_DIR : summarises abess_size_check.csv (D54.3) into ABESS_CHECK.md and the one-line ABESS_LINE.txt used by the headline."""
import sys
from pathlib import Path
import pandas as pd
D = Path(sys.argv[1]); d = pd.read_csv(D / "abess_size_check.csv")
t = lambda s: s.astype(str).str.upper() == "TRUE"
hs, he, be = t(d.head_suboptimal), t(d.head_eq_truth), t(d.best_at_head_k_eq_truth)
lost = int((hs & ~he & be).sum()); gained = int((hs & he & ~be).sum())
rows = []
for (p, c), g in list(d.groupby(["p", "scale_key"])) + [(("all", "all"), d)]:
    h = t(g.head_suboptimal)
    rows.append(dict(p=p, scale_key=c, fits=len(g), headline_suboptimal=int(h.sum()),
                     lost_recoveries=int((h & ~t(g.head_eq_truth) & t(g.best_at_head_k_eq_truth)).sum()),
                     gained_recoveries=int((h & t(g.head_eq_truth) & ~t(g.best_at_head_k_eq_truth)).sum()),
                     max_rel_rss_gap_headline=float(g.head_rel_gap.max()), fits_any_path_size_suboptimal=int((g.n_sizes_suboptimal > 0).sum()),
                     path_size_pairs_suboptimal=int(g.n_sizes_suboptimal.sum()), path_size_pairs=int((g.n_sizes - 1).sum())))
S = pd.DataFrame(rows); S.to_csv(D / "abess_size_summary.csv", index=False)
ks = [(int(k), 4 if x.p == 20 else 5) for _, x in d.iterrows() if isinstance(x.sizes_suboptimal, str) and x.sizes_suboptimal for k in x.sizes_suboptimal.split(";")]
share_above = sum(k > s0 for k, s0 in ks) / len(ks)
o = S.iloc[-1]
line = (f"the ebic1_K37 (headline) ABESS support is the exact best subset of its size (by RSS, ties allowed) in {o.fits - o.headline_suboptimal:,}/{o.fits:,} fits; "
        f"in the other {o.headline_suboptimal} (max relative RSS gap {o.max_rel_rss_gap_headline:.3f}) the exact best subset would have recovered the truth in {lost} "
        f"and ABESS recovered it while the best subset would not in {gained}, so replacing each suboptimal support by the exact best subset of the same size (holding the selected sizes fixed; EBIC selection over an exact path was not recomputed) would change ABESS's /2,400 count by {lost - gained:+d}. "
        f"Over the whole stored path (sizes 1–p), {o.path_size_pairs_suboptimal:,} of {o.path_size_pairs:,} size-k supports are not RSS-optimal, {100 * share_above:.1f}% of them at sizes above the true size.")
(D / "ABESS_LINE.txt").write_text(line + "\n", encoding="utf-8")
md = ["# ABESS (F5) exact size-k check, HQ D54.3", "",
      "**Method.** `scripts/abess_size_check.R`. F5 fits abess on column-centred X and centred y, with no intercept. For every saved fit, every stored path size k was compared with the exact best subset of size k: `leaps::regsubsets`, exhaustive branch and bound, `intercept = FALSE`, on the same X and centred y. Comparison is by centred RSS with relative tolerance 1e-8, and ties are allowed. This was run from the saved fits and the sealed inputs; truth was used only to classify outcomes.",
      "",
      f"**Validation.** Our OLS RSS of each stored ABESS support equals the stored `rss_centred` (max relative difference {d.align_err.max():.1e}). The largest |column mean| of X is {d.xc_max.max():.1e}. No ABESS RSS falls below the exact minimum ({int(d.n_below_exact.sum())} cases).",
      "", "**Result.** " + line, "", "| p | c | fits | headline suboptimal | lost recoveries | gained recoveries | max rel. RSS gap | fits with any suboptimal path size | suboptimal (fit, size) pairs |",
      "|---|---|---|---|---|---|---|---|---|"]
for _, x in S.iterrows():
    md.append(f"| {x.p} | {x.scale_key} | {x.fits} | {x.headline_suboptimal} | {x.lost_recoveries} | {x.gained_recoveries} | {x.max_rel_rss_gap_headline:.4f} | {x.fits_any_path_size_suboptimal} | {x.path_size_pairs_suboptimal} / {x.path_size_pairs} |")
md += ["", "Per-fit rows: `abess_size_check.csv`. The 'lost' cases are those where the exact best subset at the selected size is the truth but ABESS returned another support."]
(D / "ABESS_CHECK.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print(line)
