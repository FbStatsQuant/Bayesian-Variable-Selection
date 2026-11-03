# ABESS (F5) exact size-k check, HQ D54.3

**Method.** `scripts/abess_size_check.R`. F5 fits abess on column-centred X and centred y, with no intercept. For every saved fit, every stored path size k was compared with the exact best subset of size k: `leaps::regsubsets`, exhaustive branch and bound, `intercept = FALSE`, on the same X and centred y. Comparison is by centred RSS with relative tolerance 1e-8, and ties are allowed. This was run from the saved fits and the sealed inputs; truth was used only to classify outcomes.

**Validation.** Our OLS RSS of each stored ABESS support equals the stored `rss_centred` (max relative difference 1.9e-15). The largest |column mean| of X is 4.7e-17. No ABESS RSS falls below the exact minimum (0 cases).

**Result.** the ebic1_K37 (headline) ABESS support is the exact best subset of its size (by RSS, ties allowed) in 2,375/2,400 fits; in the other 25 (max relative RSS gap 0.027) the exact best subset would have recovered the truth in 9 and ABESS recovered it while the best subset would not in 2, so replacing each suboptimal support by the exact best subset of the same size (holding the selected sizes fixed; EBIC selection over an exact path was not recomputed) would change ABESS's /2,400 count by +7. Over the whole stored path (sizes 1–p), 15,712 of 60,000 size-k supports are not RSS-optimal, 98.8% of them at sizes above the true size.

| p | c | fits | headline suboptimal | lost recoveries | gained recoveries | max rel. RSS gap | fits with any suboptimal path size | suboptimal (fit, size) pairs |
|---|---|---|---|---|---|---|---|---|
| 20 | c050 | 600 | 5 | 3 | 0 | 0.0122 | 523 | 2052 / 12000 |
| 20 | c100 | 600 | 1 | 0 | 0 | 0.0122 | 522 | 2007 / 12000 |
| 30 | c050 | 600 | 18 | 6 | 2 | 0.0274 | 592 | 5902 / 18000 |
| 30 | c100 | 600 | 1 | 0 | 0 | 0.0004 | 592 | 5751 / 18000 |
| all | all | 2400 | 25 | 9 | 2 | 0.0274 | 2229 | 15712 / 60000 |

Per-fit rows: `abess_size_check.csv`. The 'lost' cases are those where the exact best subset at the selected size is the truth but ABESS returned another support.
