# Final council round 2 — disposition (writer, 2026-11-09)

Round 2: Sol 7.9 (G1, G6 FAIL), Opus 8.8 (all PASS) → not passed. Replies verbatim: `C2_council_sol.md`, `C2_council_opus.md`.
All findings ACCEPTED and applied with the reviewers' exact replacement texts. No other textual change was made (exceptions
listed at the end).

## Sol seat
| # | sev | exact change | location |
|---|---|---|---|
| 1 | MAJOR | `$\xi_q:=\{j:\mathrm{PIP}_j>q\}$` → `… for $q\in(0,1)$` | sections/s1_setting.tex:13 |
| 1 | MAJOR | SL1 clause (b) replaced by Sol's text ("for every deterministic sequence $q_n\in(0,1)$ … in particular for every fixed $q\in(0,1)$ …") | sections/s3_posterior.tex, Corollary SL1 (b) |
| 1 | MAJOR | "for fixed $q$ or $r_n=o(\min(q_n,1-q_n))$" → "for fixed $q\in(0,1)$ or deterministic $q_n\in(0,1)$ with $r_n=o(\min(q_n,1-q_n))$" | sections/s2_map.tex, ξ_q row |
| 2 | MINOR | whole Misspecification item replaced by Sol's text (GR results, EP under Theorem F's hypotheses, Lemma Z; open items reworded) | sections/s8_scope.tex, item "Misspecification" |
| 3 | MINOR | `\author` replaced by Sol's three-line block; page 1 rendered and checked: byline fits, no overfull box on page 1 (the round-1 overfull at the title is gone) | consistency.tex:6-8 |

## Opus seat
| # | sev | exact change | location |
|---|---|---|---|
| 1 | MINOR | inserted "(for random-design members of the GEN class, model G is assumed on every realisation: $X^r$ has nonconstant columns almost surely; Lemma S.1 proves this for fixed standardised designs and nonsingular Gaussian rows)" after "…used in Corollary~\ref{cor:Dprime}" | sections/s6_delivery.tex, Proposition F conclusion |
| 2 | MINOR | Thm S row: "unconditionally $\PP(\Shat=S_0)\to1$" → "without the output qualifier (ideal machine, amended allocation) $\PP(\Shat=S_0)\to1$"; plain paragraph: "…with a total tier-1 calibration fallback, also without the output qualifier, on an ideal unit-cost machine with a declared polynomial allocation (Props.~F and F-GROW: IDEAL-W, MACH, amended allocation; not checked for the C-MIS setting)" | sections/s2_map.tex, Thm S row and plain box |
| 3 | MINOR | appended to (L2): the branch's `stop("LS0 move cap out of range")` exit (cap > INT_MAX) is excluded by IDEAL-W and does not exist in the specified method; citation `BR/Scripts/SMC_BVS/core/cpp/v3_core.cpp:474` (verified by citecheck) | sections/s7_impl.tex, (L2) |
| 4 | NIT | "$C$ a large enough implementation-dependent constant" → "$C$ a large enough constant for the fixed implementation and concurrency (fixed worker count)" | sections/s6_delivery.tex, Proposition F allocation |
| 5 | NIT | "…joint design/noise law (iid rows)." → "…(iid rows), together with the algorithm's randomness." | sections/s6_delivery.tex, Proposition F-GROW |
| 6 | MINOR | after "N9 START/KERNEL (candidate)" added ", e4 for the integrated LS0 centre (W1-N3: OPEN; used by the delivery results through TDP-IMPL, while the consistency results need only e4′ or `some maximiser')" | sections/s8_scope.tex, item "Implementation premises" |
| 7 | NIT | "(e.g.\ $|\tilde S_0|<\ell_n$)" → "(e.g.\ the cap $|\tilde S_0|$ when $|\tilde S_0|<\ell_n$)" | sections/s7_impl.tex, after the transfer list |
| 8 | NIT | table cell → "all results are established simultaneously for caps $\ge\max(\ell_n,|\tilde S_0|)$ (and $\le\ell_n+K$ for the delivery envelopes); none is claimed for smaller caps" | sections/s7_impl.tex, MR1 (C-GROW) row |
| 9 | NIT | Lemma CAP provenance commit → "5bcde3b (draft v1), e95adc2 (v2)" | sections/s9_prov.tex, Lemma CAP row |
| 10 | NIT | title source line → "…council round 1; disposition in e95adc2) and branch…" | consistency.tex, \date |
| opt. | — | optional v3_calib.R citation in Remark (5): **not applied** (HQ: no other change) | — |

## Other necessary changes (not text of the chapter)
- `citecheck.py`: branch citations are now resolved at commit `8a27652` (the C-ENG head the chapter cites) instead of the
  moving ref `origin/w1c/ls0-merge`, which has advanced to `98fac03` and shifted the report's line numbers. Result: 180
  citations, 0 problems (`CITECHECK.txt`).

## Build check
LuaLaTeX clean (0 errors), 25 pages. Overfull boxes: none in any region changed in round 2 and none on page 1. Three
pre-existing ones remain, untouched per HQ's "no other change": (H-MIS) line in s3_posterior.tex:41 (24.7 pt),
PXN (R) line in s5_hpm.tex:28 (13.0 pt), provenance cell "(not merged)" in s9_prov.tex:30 (1.5 pt).
