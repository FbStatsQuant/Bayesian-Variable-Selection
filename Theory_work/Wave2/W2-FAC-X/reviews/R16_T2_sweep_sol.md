# R16 — Exhaustive Target-2 proof sweep

Counts: **FATAL 0; MAJOR 0; MINOR 1; EDITORIAL 4.**

Locations below are relative to `Theory_work/Wave2/W2-FAC-X/`. The reviewed target is locked `STATEMENT_T2.md` v2.1, Theorem FAC-GL (G1)–(G4) and iid-row Corollary FAC-NCS. These findings do not require changing its hypotheses or conclusions. The binding asymptotic scope is respected; no finding concerns the size of an onset.

1. **MINOR — The displayed Q/RSS upper bound does not imply the asserted bound on ψ.**

   **Location:** `T2/L4r_path.md:93–94` (standing consequence (s5)).

   **Reason:** From `Q_U ≤ RSS_U/s² + 1 + δ_n` and `RSS_U/s² ≤ n − 1`, one obtains only `ψ_U = 0.02 + Q_U ≤ n + 0.02 + δ_n`, not `ψ_U ≤ n`. Thus the written “hence” is unjustified. The sharper conclusion itself is true and is subsequently used in the truth-move comparison at lines 101–102. R11's exact-Gram audit already pointed out the correct independent justification, but that justification has not been incorporated here.

   **Fix:** After the Q/RSS comparison, write separately: `quad_U ≥ 0`, so `Q_U = (n − 1) − n quad_U ≤ n − 1` and `ψ_U ≤ n − 0.98 < n`. This works for every U, including the empty set, and leaves all truth-move constants unchanged.

2. **EDITORIAL — The near-CS representation identifies a raw column with a centred, mean-zero factor representation.**

   **Location:** `lemmas/X7_near_cs_loadings.md:32–33`.

   **Reason:** The first equality is written `x^r_j = λ_j f + √ψ_j u_j`, although model (R) permits an arbitrary mean vector `m_n`, and the inherited X1 notation defines `f = CF` and `u_j = CU_{·j}`. The equality therefore describes the centred column `g_j = Cx^r_{·j}`, rather than the raw column `x^r_{·j}`. It is literally false for an allowed nonzero mean. The following orthogonal-frame formula for g_j is correct, so this does not invalidate the transfer.

   **Fix:** Replace the first equality by `g_j := Cx^r_{·j} = λ_j f + √ψ_j u_j`. Alternatively give the raw representation `x^r_{·j} = m_{n,j}1 + λ_j F + √ψ_j U_{·j}` and then centre it explicitly, as X1.1 does.

3. **EDITORIAL — The covariance-continuity paragraph treats diagonal entries as having CS value ρ.**

   **Location:** `lemmas/X7_near_cs_loadings.md:61–62`.

   **Reason:** The text says that the relevant covariance entries are “each within 2Δ_n of the CS value ρ (λ_jλ_k − λ̄²).” This is correct for off-diagonal entries. Diagonal entries of both covariance matrices equal 1, and their discrepancy is zero; their CS value is not ρ. Taken literally for all the stated entries, the assertion fails even at Δ_n = 0. The required matrix-continuity estimate remains valid.

   **Fix:** State that the diagonal discrepancies vanish and the off-diagonal discrepancies satisfy `|λ_jλ_k − λ̄²| ≤ 2Δ_n`. Then apply the Lipschitz estimate to the difference from the full CS covariance matrix, whose diagonal is 1.

4. **EDITORIAL — X7 retains an obsolete instruction about where its result will be locked.**

   **Location:** `lemmas/X7_near_cs_loadings.md:3–5`.

   **Reason:** The header says “to be locked as STATEMENT §6 (Target 2 block),” while the result is already separately locked in `STATEMENT_T2.md` v2.1, and `STATEMENT.md:107–110` contains only the Target-2 scope note. The statement that X7 is not part of locked Target-1 v3 is correct; the future lock destination is stale. This makes the recorded status/destination inconsistent with the actual locked document.

   **Fix:** Retain the exact base proof and R12 verdict strings, but replace the future-lock clause by “supports Corollary FAC-NCS in separately locked STATEMENT_T2.md v2.1; iid rows (R) only.” Keep the explicit withdrawal of (G).

5. **EDITORIAL — The X9 header conflates the review-wide amendment count with the X9-specific count.**

   **Location:** `lemmas/X9_iid_general.md:3–4`; compare `reviews/R11_L4rS_X9_check_sol.md`, its verdict table and numbered issues 1–3.

   **Reason:** The X9 header records `VERIFIED-WITH-AMENDMENTS (3 MINOR, applied)`. R11's X9-specific verdict requires two MINOR amendments, issues 1–2. Its third MINOR amendment belongs to the separate input `T2/STATEMENT_T2.md` §2 and corrects the unused limiting offset/centre. All three fixes are present in their proper files, but the scope of the count in the X9 annotation is inaccurate/ambiguous.

   **Fix:** Record X9's verdict as `VERIFIED-WITH-AMENDMENTS (2 MINOR, applied)` and, if retaining the aggregate count, explicitly say that R11 also required one MINOR correction to `T2/STATEMENT_T2.md`.

## Re-verification and coverage

The proof audit used the locked statement; `T2/STATEMENT_T2.md` §§1–3; `T2/L4r_path.md` §§L4r.0–L4r.3; X7–X10; the reused parts of X1–X6; FAC-B's statement and L1–L5; FAC-A L5.1; Lemma CR; FINAL s3, s6, s7; and A2's delivery extension. R10, R11, R12, R15 and their dispositions were checked against the current text. The supplied numerical summaries were treated as evidence only; no numerical experiment is claimed by this review.

The earlier substantive corrections are present: sign-corrected (FS-G); a bound uniform in the loading array's indices; the fixed A₁ and onset qualifications; the corrected truth-noise contribution to the exact-Gram centre; both terms in X9's second-order remainder; absolute values in its addition square; the retained logarithmic term in X7's remainder; the iid-only FAC-NCS restriction; the tightened dispersion condition; and omission of the raw-sd event for exact Gram. The remaining withdrawn (G) paragraphs in X7 are explicitly identified as notes and are not used to prove the locked iid-only corollary.

In particular, the exact-Gram sign identity, top-square centre bound, size-prior cancellation, and logarithmic deletion/addition margins close uniformly over all supersets of S₀. The iid transfer uses its correctly normalised reference statistic and a full-matrix operator-norm bound, so it does not import a path/band hypothesis. X7 preserves the CS reference drift and reruns the Target-1 approximate-argmin/soft-gap proof; the enlarged scale still satisfies its spacing, tail-window, band-absorption and `pw² + w log n = o(1)` requirements. The start proof conditions on the raw design, and the assembly retains the every-sequence/common-constant posterior argument, MR1 prefix property, separate scored-truth event, amended allocation, and total fallback. No independence of the realised partition from the noise coordinates is required. No further FATAL, MAJOR, or MINOR issue was identified in those uses.
