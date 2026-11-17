# W3-D2 — Council diff round D1, seat `opus`

Seat: Opus 5.5 (claude-opus-5-5), fresh agent. Brief: `reviews/BRIEF_D1_opus.md`. Manifest under review:
`MANIFEST f62740c74ee1740a4cfbbcd9d12e0c845dc8435fb0adde6e380ca9bda3469d2b`.

## What I checked

**Manifest binding.** I recomputed the sha256 of all 14 ticket files and all 10 `EXT:` inputs in `reviews/MANIFEST_D1.txt`.
All 24 match the working tree, so this review covers exactly the manifest's content.
- The 10 `EXT:` hashes are the same as in MANIFEST_R1, so no source changed.
- The R1 manifest content is commit 934a2b43. Its blobs of STATEMENT, PROOF, REPORT, DEPS and N1_out hash to the R1 manifest values.
- `git diff 934a2b43 HEAD` over the ticket directory, excluding reviews/ and LOG.md, matches `reviews/D1_diff_since_R1.txt` line for line (index lines aside).
- The only uncommitted change in the worktree is LOG.md. It is not in the manifest, and I did not read it.

**What I read.**
- All hunks of the diff.
- The full current STATEMENT, PROOF, READER_DELTA and N1 script, plus REPORT :1-81 and TARGET :20-27.
- The two R1 reviews and PROTOCOL_v4 §0 and §5, for the C/S/F/E classes.
- Sources:
  - L1_POST.md :15-30
  - R1_set_sizes.md (whole)
  - W3-POST STATEMENT :14-45
  - NOTATION :14-25
  - MISR-R :48-56
  - MISR :116-120
  - READER_VERSIONS :260-276

I did not open LOG, CHECKPOINT or disposition files.

**What I re-ran.** Scratch files went in `.rc_tmp/`, which I deleted at the end.
- **N1 re-run.** `numerics/N1_floor_and_e2e.py 300` produced output byte-identical to `numerics/N1_out.txt` (sha256 e6dd3e95…, as in the manifest).
- **Independent check of m♯_n.** I computed m♯_n from its definition ([W3P] `:36-39`) in 100-digit Decimal arithmetic.
  - Method: q_k = C(p,k)·½/C(2p−1,k), built from the binomial factors themselves rather than the script's ratio. R_m = Σ_{k>m} q_k / w(s₀). The threshold is n^{−(s₀+1)/2}·n^{−1/2}, and m♯_n is the least m ≥ s₀ with R_m ≤ threshold.
  - Truncation: since q_{k+1}/q_k ≤ ½ for k ≥ 1, cutting the tail at 10^{−400} is harmless.
  - Result: all 150 grid cutoffs equal the script's (0 differences), and the grid maximum of k_n/[3(A+1)(s₀+1) log n] is 0.3928391, matching N1_out's 0.3928.
  - Margins: the smallest gap at a cut is |log(R_m/thr)| = 0.003, far above floating-point error.
  - Sol's test case (A = 3, s₀ = 1, n = 10⁵, p = 10¹⁵) gives m♯ = 76, with R₇₆/thr = 0.83705 and R₇₅/thr = 1.67410, exactly Sol's figures.
  - **Disclosure:** importing the script left a git-ignored `numerics/__pycache__/` in the ticket directory. I deleted it, and the script's hash is unchanged (8202c144…).
- **The script's new code** (`:37-61`):
  - The ratio q_{k+1}/q_k = [(p−k)/(k+1)]·[(k+1)/(2p−1−k)] = (p−k)/(2p−1−k) is exact, and q₀ = ½.
  - log w(s₀) uses a sum of logs with no cancellation.
  - The threshold uses ω = ½ log n.
  - The search starts at m = s₀, and R_K = 0 guarantees it terminates.
  - This matches the definition.
- **DEPS hashes.** I recomputed every span hash with my own code (I did not run deps_hand.py, which rewrites DEPS.tsv). All 11 rows reproduce, and sha = checked_sha:
  - S:det `2d04f4d7…` (:60-64)
  - S:inputs `f8b42733…` (:81-86)
  - P:P3 `b2487f87…` (:60-83)
  - P:P5 `8d16597b…` (:84-97)
  - R:registry `b2140e82…` (REPORT :61-81)
- **Unchanged spans.**
  - S:Thm2X (:29-48), S:Cor2X (:50-58) and S:setting (:14-27) hash identically to the R1 blob.
  - PROOF :7-59 (P0–P2) is byte-identical to R1.
  - The text of S:inputs (:81-86) is byte-identical to the R1 lines :79-84; only the line numbers moved.
- **P5 by hand.** I checked every constant (below) and ran a grid of the P5 claim: A ∈ [1,10] in steps of 0.01, s₀ ≤ 300, n ∈ 3..199 ∪ {10³,…,10¹⁵}, p = ⌊n^A⌋. That is 56,763,000 cases with 0 violations.

## (a) R1 findings

| finding | verdict | reason |
|---|---|---|
| Sol F1 (N1 precision at p = 10¹⁵) | **RESOLVED** | Stable ratio recurrence at `N1_floor_and_e2e.py:46-50`. My 100-digit recomputation from the definition matches all 150 cutoffs and the 0.3928 maximum. N1_out:15 and TARGET:24 are updated, and "computed exactly" is gone. |
| Sol E1 (unlabelled side assertion, REPORT:42) | **RESOLVED** | Now "(OPEN, not checked here: the unchecked note says …)". |
| Opus E1 (k̄_n ≤ 3(…) log n stated without proof) | **RESOLVED** | PROOF P5 proves it (all steps check, see (b)), and STATEMENT:111 points to it. |
| Opus E2 ("Σ need not be a correlation matrix" listed as a gain) | **RESOLVED** | STATEMENT:100-101 now calls it cosmetic and cites NOTATION :21-23 (the WLOG sentence is at :22-23). TARGET:25-26 names σ_n² → ∞ as the genuine departure. Residual: READER_DELTA:5-6 still reads "Σ_n need not be a correlation matrix". That is literally true and editorial only, and my R1 pointer "READER_DELTA.md:32" was wrong (the file has 25 lines). I raise no new finding. |
| Opus E3 (§3 attribution over-broad) | **RESOLVED** | STATEMENT:63-64 attributes only the PIP inequality to [MISR] :118-119 and sends HPM/MPM to PROOF P0. Line 62 (the facts) is unchanged. |
| Opus E4 ("α* may even be random") | **RESOLVED** | PROOF:64-65 and :80-81 now say it is a remark on the master, not on Theorem 2X. The [MISR-R] :52-53 citation is correct ("a real random variable α"). |
| Opus E5 (card: other conditional inputs) | **RESOLVED** | REPORT:31 adds "two others are wave-1 results" (C-MIS:GDb, C-MIS:Prop-P, as REPORT:43-44 states). |
| Opus E6 (σ² fixed vs varying; 1 ≤ \|T\|) | **RESOLVED** | READER_DELTA:11 and REPORT:27-28 both say "allowed to depend on n", and READER_DELTA:13 has 1 ≤ \|T\|. |
| Opus E7 ("Theorem 4 with no omitted predictors") | **RESOLVED** | STATEMENT:68-69, READER_DELTA:19 and REPORT:29 now add "plus the deterministic PIP/MPM consequences". |
| Opus E8 (docstring "Lemma D2-B1") | **RESOLVED** | The N1 docstring at :2 now cites `W3-READER:R1` B4.1. |

## (b) Does the diff introduce a C, S or F finding?

**No.** The diff introduces no C, S or F finding.

**Claim spans.** STATEMENT §1 (:29-48) and §2 (:50-58) are unchanged (hashes c84965ed…, 0dc7f82d…, identical to R1).

**§3 (S:det, :60-64).** The change is attribution only:
- The fact line :62 is byte-identical.
- The new :63-64 splits the attribution. The PIP inequality is [MISR] consequence 1, `:118-119` ("for every data set", verified). The HPM/MPM inclusions are proved in P0, and P0 (:12-14) does prove them.

**§5 (S:inputs, :81-86).** The text is identical to R1 (moved by two lines). The statuses are verbatim as before.

**P3 (:60-83).** The only change is the α remark, now confined to the master. The Cor2X argument (:66-76) is untouched. P4's sentence is consistent with §0 :19 (α deterministic).

**P5 (:84-97). Every inequality checks.** Notation: d = 1/log(3/2) = 2.46630, s = s₀, t = log n.
- **j₀ branch.** By [R1] B1.2/B4.1, s + j₀ ≤ (2A+2)s + 2. Also 3(A+1)(s+1) − (2A+2)s − 2 = (A+1)s + 3A + 1 > 0 and t > 1, so s + j₀ ≤ 3(A+1)(s+1)t.
- **m̄_n branch.** The numerator of m̄_n in L1_POST :21 is (As + s/2 + 1)t + (s+1) log 2. The ceiling then gives s + m̄_n ≤ d(As + s/2 + 1)t + (1 + d log 2)(s+1).
  - 1 + d log 2 = log 3 / log(3/2) = d log 3 = 2.709511 < 2.7096.
- **The bracket.** 3(A+1)(s+1) − d(As + s/2 + 1) has coefficients 3 − d = 0.53370 > 0.5336 (on As and on the constant), 3 for A, and 3 − d/2 = 1.76685 > 1.7668 for s. So the lower bound 0.5336As + 3A + 1.7668s + 0.5336 is correct, and it is increasing in A.
- **n ≥ 4.** t ≥ 1.386294.
  - 1.386 × 2.3004 = 3.18835 ≥ 3.188, and 1.386 × 3.5336 = 4.89757 ≥ 4.897.
  - 3.188s + 4.897 > 2.7096(s+1) for all s ≥ 0.
  - Monotonicity in A holds because the bracket's A-coefficient (3−d)s + 3 > 0.
- **n = 3.** t = 1.0986123.
  - 1.0986 × 0.5336 = 0.58621 ≥ 0.5862, and 1.0986 × 3 = 3.2958.
  - 2.7096 − 1.0986 × 1.7668 = 0.76859 ≤ 0.7686, and 2.7096 − 0.58621 = 2.12339 ≤ 2.1239.
  - So the stated sufficient condition A(0.5862s + 3.2958) ≥ 0.7686s + 2.1239 is conservative and valid.
  - For A ≥ 1.32: 1.32 × 0.5862 = 0.77378 and 1.32 × 3.2958 = 4.35046, so the left side is ≥ 0.7737s + 4.350 > 0.7686s + 2.1239.
  - For 1 ≤ A < 1.32: p ≤ 3^A < 3^{1.32} = 4.2638 < 4.27. Since p is an integer, k̄_n ≤ p ≤ 4 < 12 × 1.0986 = 13.18 ≤ 3(A+1)(s+1) log 3.
- **Cross-check.** The cited figure (7,426,052 cases, 0 violations) is my R1 grid, quoted correctly. My new grid of 56.8 million cases also has 0 violations.

**P5 citation range.** One citation range in P5 is imprecise.
- `[R1] B2.1 (:38-40)` points at the identity and the 5(…) bound. The ceiling inequality it invokes is at [R1] :36 (the identity is at :37-38).
- The cited lemma is the right one and contains the step, so this is citation form (PROTOCOL_v4 §5.2: E), not faithfulness.
- Per §5.5 I do not raise it as an E finding. I mention it only to explain why I hold no F.
- P5 is outside every claim and is labelled a remark.

**Registry (REPORT :61-81).**
- Thm2X's premises now cite :60-64 and :81-86, which are exactly §3 and §5's input list.
- The statement spans (29-48, 50-58), the status lines (= PROOF:3 verbatim, unchanged), and the assumptions, conclusion and scope fields are unchanged.
- This also removes R1's slight mismatch between DEPS (76-84) and the registry (77-84).

**Other hunks.**
- STATEMENT §4(a) and §7 add wording only, outside the spans.
- The changelog row 1.4 (EQUAL) is accurate.
- REPORT §3: the card text matches Thm2X (σ² may vary with n; conditional, with the wave-1 inputs named).
- REPORT §3a carries the OPEN label.
- READER_DELTA :11, :13 and :19 match STATEMENT §1.
- TARGET :24-26 is accurate. For N1 (ii), (A3) holds with σ_n² = (log n)^{1/2}: ρ_n ≍ n/(log n)^{3/2} → ∞.
- ERRATA.md is new and makes no mathematical claim.
- deps_hand.py: the rows match DEPS.tsv.
- STATEMENT §4(c) ("at most 0.40") and REPORT §5 remain true at 0.3928.

## (c) Per-claim decisions

| id | decision |
|---|---|
| W3-D2:Thm2X | ACCEPT |
| W3-D2:Cor2X | ACCEPT |

## (d) Gates (manifest D1)

- **correct — PASS.** The claim spans and P0–P2 are unchanged from R1, where both seats accepted them. P3's Cor2X argument is untouched. The new P5 checks step by step.
- **strength — PASS.** No claim span changed. The new wording (E2, E4, E7) narrows or qualifies statements and adds nothing unproved. Caveat (b) is now backed by P5.
- **faithful — PASS.** Sol F1 is fixed: the script matches the definition at [W3P] :36-39, and an independent 100-digit computation agrees on all 150 cases. The new citations check: [MISR] :118-119, [MISR-R] :52-53, NOTATION :21-23, L1_POST :20-21, [R1] :45. The [R1] :38-40 range is imprecise (form only, see (b)).
- **statuses — PASS.** PROOF:3 and both registry status lines are unchanged. The §5 statuses are verbatim and unchanged. Nothing new is called checked.
- **sweep — PASS.** All 11 DEPS hashes reproduce, and every row is OK. The registry premises match the new §3 and §5 spans. N1_out reproduces byte for byte. TARGET and the STATEMENT changelog are consistent with the diff.
- **reader — PASS.** The card sentence and READER_DELTA match Thm2X and keep the conditional mark and COEXIST. The E5–E7 wording is applied.

## (e) Score

**9.6.** I hold no C, S or F finding. All ten R1 findings are resolved, and the one F from R1 (Sol F1) is independently confirmed fixed. The score is unchanged from my R1 score. As there, 0.4 is held back because the result is an instance-of-master proof whose weight rests on the consumed claims, taken as true.

COUNCIL-VERDICT round=D1 manifest=f62740c74ee1740a4cfbbcd9d12e0c845dc8435fb0adde6e380ca9bda3469d2b seat=opus score=9.6 gates=PASS
