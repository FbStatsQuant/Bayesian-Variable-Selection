# B1 disposition — W3-MEMO-SCR-RM (lead, 2026-11-11)

Review: `reviews/B1_review_astra.md` (gpt-6-astra, codex, reasoningEffort high; blind first read on
`MANIFEST cd0ebff97cc6e2fc04afd31d45b1abd90527762f3fae73e76c8d66330fca3c20`; `manifest.py bind` OK).
Reviewed text: `reviews/MEMO_v1_reviewed_B1.md` (sha256 equal to the manifest row for `MEMO.md`).
Verdict received: **REJECT as written; recommendation (a) kept after revision.** 6 MAJOR, 2 MINOR.

**Lead's reading.** Every finding is accepted. The review did not overturn the recommendation, and it confirmed the
two load-bearing deductions (I2 in full; I3 with the item-by-item derivation of T1-F from NF, including
m♯_n = O(log n)). What it broke is the memo's *exclusionary* language: version 1 turned the failure of one sufficient
route (LS0 from the start mode) into "no supersession, no strengthening". The evidence supports only "none is
established, and here is exactly what is missing".

| # | Grade | Finding (short) | Disposition | Change in MEMO v2 |
|---|---|---|---|---|
| 1 | MAJOR | An LS0 counterexample is not a counterexample to reported-model recovery; "SCR-C ⇏ RM's conclusion (I2)" does not follow | **Accept.** I checked `W2-FAC-PK/STATEMENT.md` and REPORT flag 3: nothing is claimed about the full method | §0 rewritten: "not established" instead of "no"; the arrow in the §1 summary removed; I2 states what is proved (LS0 route) and what is open (full method) |
| 2 | MAJOR | NF with a fixed margin forces p ≤ n^{(1−ε)/(2ε)}: no non-polynomial-p regime for SCR-C | **Accept.** φ_n ≤ 1 on any set of size ≥ 2, so ϑ_n ≤ 1 − ε. My row A was wrong | Row A corrected; the coupling log p/log n ≤ (1 − ε)/(2ε) stated in §1 and §3 |
| 3 | MAJOR | Regime rows do not imply the table's conclusions (A incomplete; B's "below ϑ+ε" ill-posed; C false as a sufficient condition — cancellation example; D is not a negative result; examples unqualified) | **Accept.** The cancellation example (two truths at correlation 0.2, θ = (1, −5), orthogonal nulls) satisfies NF, A1 and zero leakage and violates (V): I verified x₁ᵀμ = 0 | §3 rewritten: regimes are defined by which full hypothesis sets hold; sufficient conditions and examples are labelled as such; row C no longer claims "NF + no leakage ⇒ RM" |
| 4 | MAJOR | The cap comparison conflates the realised number of extras m₀ with the deterministic envelope \|Q ∖ S₀\|; "C → 1 is deletion-only, i.e. NA" is false; C = 1 + o(1) is not sufficient at polynomial m₀ | **Accept.** PL charges m₀; (N-χ) bounds the envelope. A small realised start inside a large or unknown envelope is not covered by (N-χ), so PL could be a genuine strengthening there | §0 reason 3 and §2 ML2 rewritten: limitation stated for m₀ only; the requirement stated as an *additive* budget (non-deletion moves ≤ slack); the "small realised start, large envelope" case recorded as an open candidate; the claim "(N-χ) already covers it" withdrawn |
| 5 | MAJOR | ML1–ML3 are one sufficient architecture, not an exhaustive decomposition; confinement unstated; M5 overread in phase 1; a small start is not equivalent to global (L) | **Accept.** Under [POST] the target needs only "S₀ is scored", not a certified sparse endpoint. M5 concerns centres that already contain S₀ (`W3-SCR/STATEMENT.md`, SCR-M (M5)) | §2 retitled and restated: target = discovery; ML1–ML3 labelled "one sufficient architecture"; a confinement clause added; phase 1 rests on the gain/range argument only; the sentence "(L) cannot be removed in fixed design" withdrawn (block-relative and counting forms noted) |
| 6 | MAJOR | "NF ⇏ (N)" is not proved; (N) is a disjunction and depends on Q | **Accept.** No construction was given, and the incomparability of the hypothesis sets does not need it | I5 now says: no derivation of (N)/(D-R) from NF is known here; no non-implication is claimed |
| 7 | MINOR | Corollary CERT: valid; state it on a common good data event; the enumeration branch certifies directly, not "by LS0"; no conditional probability given 𝒪 | **Accept.** The reviewer checked the code path (final search before LS0, `v3_core.cpp:453–479`; flag rule `v3_run.R:179, 193–195`; `v3_exact.R:15`; no index-order or type obstruction in `identical`) | I1 and §4 restated in the reviewer's form; the code check is recorded as done by B1 |
| 8 | MINOR | "NF needs ≥ 2/3" is false for p < n; say "need not satisfy NF"; a concrete RM-F-but-not-NF example | **Accept.** ϑ_n depends on log p/log n and can be below 2/3 | I4 corrected and given the reviewer's example (two truths at correlation 0.9, θ = (1, 1), orthogonal nulls, Q = S₀) |

**Further points taken from the review body (not numbered findings).**
* I3: {certified ∧ sparse} ⊆ {Ŝ = S₀} holds on the common good event, not as an identity of raw events; SCR-G(ii)
  gives containment only. Text corrected.
* I2: singletons have λ_min = 1; "every principal submatrix of size ≥ 2". Corrected.
* PL: the factor (1 − o(1)) needs x′ → ∞ with x′ = o(𝐋_n) and the probability bookkeeping redone (the proof of SCR-C
  uses x′ = ε log n/8, which spends a fixed fraction of the margin); the bound is (1/(2 log 2) + o(1)) log n, not a
  literal 0.72 log n. Both stated.
* Missed routes, now listed in §2: (i) size-only or block-relative entry with a confined potential argument;
  (ii) restricted-lattice potential plus exit control (exit control must include additions from deletion bases);
  (iii) exactness from (EC′) / L5.2 with the pair (α, ω) instead of the floor NF.
* Recommendation (c): a regime-D trigger cannot end in SCR-C without NF; it would need an (EC′)-based exactness
  step. Corrected.

**Not changed.** The recommendation (a) with Corollary CERT; I2's construction; I3's deduction; the PL sketch as a
sketch. The reviewer's own recommendation is (a) with corrected CERT and the alternatives recorded as open.

**Status of version 2.** The changes above are substantive (rule 15) and have **not** been re-reviewed: the brief
allows one review and no other agents. Version 2 is therefore "revised after B1, changes unreviewed". The manifest
`MANIFEST_B1.txt` describes version 1; `manifest.py verify` fails on the current tree by design (MEMO.md changed).
