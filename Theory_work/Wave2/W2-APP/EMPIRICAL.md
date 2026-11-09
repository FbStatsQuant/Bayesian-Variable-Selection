# W2-APP Part 2 — real designs: design-only diagnostics and classification

**Nature of this part.** Descriptive. A single finite data set cannot *verify* an asymptotic hypothesis (which is a
statement about a sequence of designs); what can be done is to measure the design-only quantities the hypotheses refer
to and say which theorem class each design **resembles**. Signal-dependent conditions (beta-min, PTV, visibility,
non-cancellation) are not checkable (θ* unknown) and are not assessed; the only plug-in numbers (riboflavin, diabetes
OMP supports in `data_diag/SUMMARY.md`) are labelled there as plug-in, not verification.

**Sources.** The project has no real data set (SoP `06_open_and_plan.tex:279`, ENG19 "Real data ... OPEN"). Public
designs, provenance with md5 in `data_diag/SUMMARY.md` §1 and `data_diag/data/PROVENANCE.txt`: riboflavin (hdi 0.1-10,
CRAN Archive tarball), tecator/Fat spectra (fds 1.8), iclaims (bsts 0.9.10), FRED-QD and FRED-MD (BVAR 1.0.5 data with
BVAR's transformation codes re-implemented), diabetes quadratic model of Efron et al. 2004 (scikit-learn 1.4.2), spam
(kernlab 0.9-33), digits (scikit-learn 1.4.2). Scripts `data_diag/diag_*.R`, `diag_lib.R`, `prep_*.{R,py}`; outputs
`data_diag/out_<name>.*`; master table `data_diag/summary_table.csv`. The method's partition was computed with the
production C++ (`v3_blocks`, byte-identical copy of `Scripts/SMC_BVS/core/`, SHA-256 verified,
`data_diag/core_copy/SOURCE_SHA256.txt`). Helper: Claude Sonnet 5.5 (own provider); numbers spot-read by the lead.

**Labels.** φ²(k) := min_{|S|=k} λ_min(R_S) (sample correlation). EXACT (k = 2; k = 3 by full/pruned enumeration;
iclaims all k); UB = witness set from greedy/random-restart search (upper bound on φ²(k) — evidence of badness);
LB = rigorous lower bound (Gershgorin, or λ_min(R) when p < n by interlacing).

## Master numbers (from `data_diag/summary_table.csv`)

| design | n | p | top-1 share | med. partners abs(r)>.5 (raw → after top factor(s)) | φ² exact k=2 / k=3 | φ² UB k=7 | LB (λ_min R, p<n) | method blocks: #, median/max leakage |
|---|---|---|---|---|---|---|---|---|
| riboflavin | 71 | 4088 | 0.36 | 982.5 → 89 | 0.0094 / n.a. | 0.0026 | uninformative | 683; 0.82 / 0.975 |
| tecator | 215 | 100 | 0.99 | 99 → 75 | 4.0e-6 / 4.1e-9 | 6.8e-11 | 1.7e-11 | 13; 1.00 / 1.00 |
| iclaims | 456 | 10 | 0.83 | 9 → 0 | 0.10 / 0.096 | 0.066 (exact) | 0.064 | 4; 0.86 / 0.87 |
| FRED-QD | 257 | 170 | 0.27 | 7 → 3 | 0.0040 / 1.9e-5 | 1.7e-5 | 2.3e-6 | 17; 0.60 / 0.98 |
| FRED-MD | 775 | 99 | 0.21 | 4 → 2 | 0.015 / 9.1e-5 | 7.0e-5 | 4.2e-5 | 13; 0.46 / 0.88 |
| diabetes (quad.) | 442 | 64 | 0.17 | 2 → 1 | 0.041 / 0.012 | 8.1e-5 | 3.6e-7 | 11; 0.56 / 0.84 |
| spam | 4601 | 57 | 0.12 | 0 → 0 | 0.0039 / 0.0039 | 0.0039 | 0.0039 | 10; 0.16 / 0.57 |
| digits | 1797 | 61 | 0.12 | 2 → 0 | 0.062 / 0.059 | 0.055 | 0.050 | 11; 0.49 / 0.66 |

## Classification (design-only; "resembles" = the class whose design hypotheses the measured pattern matches; v2 after sweep R07)

A single finite design is not a sequence: membership of any asymptotic class (fixed floor, LOC constants, VN floors)
is neither confirmed nor refuted by it; every statement below is descriptive [R07 #4, #7, #8]. "Resembles" refers to
the correlation pattern only: the theorems assume iid Gaussian rows, which none of these designs has (spam: heavy-tailed
counts; digits: integer pixels; diabetes-quadratic: polynomial terms; FRED: serially dependent rows) [C2-Opus-3].
Lower bounds labelled "rigorous" are rigorous up to floating-point error.

1. **Local — resemble the LOC / bounded-block classes (L4 (a), (d), (e)); conditioning ranges from moderate (spam,
   digits) to near-collinear clusters (diabetes)** [C1-Opus-5].
   *spam*: no partners above 0.3 for the median variable; one near-duplicate pair (|r| = 0.996) explains the small
   scale of the sparse eigenvalues: for k ≥ 2, interlacing brackets φ²(k) in [0.003855, 0.003934] (exact φ²(2) =
   0.003934, φ²(3) = 0.003901; k = 9 witness 0.003869; λ_min(R) = 0.003855) [R07 #10]. Pattern: nearly independent
   columns plus one cluster of ≈ 11–12 correlated variables (90% quantile of partners above 0.3 is 10, max 11;
   out_spam_partners.csv) and isolated pairs = bounded blocks [C1-Opus-7]. *digits*: pixel-neighbourhood correlation, flat spectrum, observed
   sparse eigenvalues ≈ 0.05. The variables are pixels of a two-dimensional image; Theorem LOC is proved for
   one-dimensional neighbourhood growth, so an extension to growing two-dimensional grids is not covered by the present
   theorem — membership of a sequence representing this particular design is not established either way [R07 #7].
   *diabetes (quadratic)*: correlation confined to clusters (s1–s5, their products and squares; median 2 partners) —
   local block clusters, with a nearly collinear direction (λ_min(R) = 3.6e-7).
   Reading: these patterns match the classes where POST and, under PTV, Theorem LOC apply. The reported numbers are
   observed sample global/sparse eigenvalues (with their exact/UB/LB roles); they are diagnostics relevant to possible
   theorem constants, not the design's φ₀² (which is a population, anchored quantity depending on the unknown support)
   [R07 #22].

2. **Pervasive factor structure — resemble (g) (equicorrelation / factor): POST class; reported model per FAC.**
   *iclaims* (one factor carries 83% of the trace, every pair ≥ 0.698 [C3-Opus-3]; after removing it, no partner > 0.5; p = 10 is
   fixed, so the exact branch applies — at its actual size (n = 456, p = 10) too — and the reported-model question is
   covered by Lemma ENUM + POST in a fixed-p iid-Gaussian-row model — the actual rows are a weekly time series,
   serially dependent) [C2-Opus-2, C3-Opus-1];
   *riboflavin* (top factor 36%, median 982 partners > 0.5, still 89 after removing the factor; the |r| > 0.9 tail is
   sparse; the largest |r| among 8.4·10⁶ independent pairs at n = 71 would be ≈ 0.6–0.67 (typical value ≈ 0.59; 0.67 is a crude upper reference), an extreme-value context
   statistic only — it does not apportion the bulk of the correlations to noise [R07 #9]); 99.5% of pairs with
   |r| > 0.5 are split across the method's blocks (blocks of size ≤ B = 8 cannot hold a pervasive cluster).
   *FRED-QD / FRED-MD*: a common factor (21–27%) plus tight local clusters (interest-rate spreads, manufacturing
   employment aggregates) with exact φ²(3) ≈ 1.9e-5 / 9.1e-5 — "factor + local".
   Reading: posterior level — POST applies to factor designs whose population correlation matrix has a fixed floor;
   reported model — outside the proved local classes. Dense cross-block marginal correlation motivates, but does not
   establish, Lemma VN's conditional visibility hypotheses (marginal correlation can coexist with zero partial
   correlation); only the quantified models V1–V4 carry the proved route obstruction [R07 #8]. FAC-A/B are the
   relevant tickets.

3. **Smooth-curve / functional, near-collinear.** *tecator*: one component carries 98.6% of the trace, adjacent
   wavelengths correlate at 1 − 4e-6, λ_min(R) = 1.7e-11 (positive), exact φ²(3) = 4.1e-9; the method's blocks are
   mutually correlated at |r| ≈ 0.9999. Observed: extreme near-collinearity. Not claimed: exclusion from the fixed-floor
   classes — that would require a specified grid-refinement sequence (population process, grid, normalisation) with a
   proved vanishing sparse floor, which is not supplied; a fixed 100-variable correlation matrix (or independent copies
   of it) does have a fixed positive floor [R07 #4]. Reading: if the relevant asymptotic model is a densely refined
   smooth curve, a functional theory would be needed; this ticket does not decide it.

## What this says about applicability (summary for HQ)
* Of eight standard public designs, three (spam, digits, diabetes-quadratic) show **local** correlation of the kind
  covered by the posterior theorem and by Theorem LOC's class (digits is an image; growing 2-D grids are outside LOC's
  proved scope); four (riboflavin, iclaims, FRED-QD, FRED-MD) are **pervasive factor** designs — posterior theory
  applies to their class; reported-model theory for growing-p versions: FAC-A's class (one factor + bounded blocks, p ≲ n^{1/6}) where it
  applies, otherwise open (iclaims, p = 10: exact branch, ENUM). With p FIXED, all eight designs are eventually on the
  exact branch (ENUM + POST in an iid-Gaussian-row model with a positive population floor), incl. tecator's fixed-design
  reading; the classification matters for growing-p models [C3-Opus-1]; one (tecator) is an extremely **near-collinear functional**
  design, whose appropriate asymptotic model is not decided here.
* Several real designs contain small **near-collinear clusters** (exact φ²(3) between 4e-9 and 1e-2); these are observed
  sample quantities, recorded as data about where the designs sit, not a statement about the theorems' validity.
* The method's own partition (B ≤ 16) captures local clusters (spam: median leakage 0.16) but cannot capture pervasive
  correlation (riboflavin/FRED/tecator: most strong pairs split across blocks). LOC needs no partition condition; the
  VN obstruction is proved only for the quantified models V1–V4 — the block splitting here is descriptive [C1-Opus-4].
