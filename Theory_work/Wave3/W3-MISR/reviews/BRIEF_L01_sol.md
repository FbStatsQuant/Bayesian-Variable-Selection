# BRIEF L01 — statement-lock review (blind first read), seat: Sol (codex gpt-6.1-sol, reasoningEffort high)

You are an independent reviewer of a mathematical **statement** (no proofs exist yet). Your job is to break it.
Repository root = your working directory. Work read-only, except for the one output file named at the end.
Do not read any file under a `reviews/` folder, any `LOG.md`, `PLAN.md`, `CHECKPOINT*.md`, `REPORT.md`, or anything
under `Theory_work/Wave3/API_AUDIT/`. Do not change git state. Do not start subagents.

## What to review
`Theory_work/Wave3/W3-MISR/STATEMENT.md` (v1.0): Lemma R′, Theorem MIS-R (i), (i′), (ii), Corollaries G and H,
Remarks SNR, P, U — a second version of the "misspecified candidate subset" theorem for a Bayesian variable-selection
posterior, in which the residual variance may depend on n and on the design.

## Files you may read (inputs the statement cites)
- `Theory_work/Wave3/W3-POST/STATEMENT.md` (the coded target π, Theorem 1, hypotheses (E), (F_λ), (F_w), (BM)).
- `Theory_work/Wave3/W3-POST2/STATEMENT.md` and `Theory_work/Wave3/W3-POST2/lemmas/{A_occam,C_expectation,D_hellinger,E_visibility}.md`
  (Claims A1, B, C, D, E: the theorems the new statement is reduced to).
- `Theory_work/Wave1C/C-MIS/STATEMENT.md`, `Theory_work/Wave1C/C-MIS/lemmas/{L1_reduction,L2_gaussian,L5_frontier}.md`
  (version 1 of the theorem and its Gaussian-row lemmas).
- Code: `Scripts/SMC_BVS/core/v3_preprocess.R`, `v3_fit.R`, `v3_setup.R`, `cpp/v3_score.h` (and any other file under
  `Scripts/SMC_BVS/core/` you need to follow the response from input to score).
- `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/W1-T03R/PROOF.md` and
  `…/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/` (older locked proofs), only if you need a definition.

## Questions (answer each; give file:line evidence)
1. **Well-posedness.** Is every object, hypothesis and constant in STATEMENT.md defined, and is each claim an
   unambiguous mathematical statement (quantifiers, which n, which law, measurability in §4)? List every ambiguity.
2. **Lemma R′.** (a), (a′): is the invariance / equivariance true for the target as defined in W3-POST §0? Try c < 0,
   constant columns, s_y. (a″): follow the response through the code — does anything on the raw scale of y reach a
   score, a prior, a budget or a decision that changes the target? Are the cited file:line pins right?
   (b): is the reduction to the unit-noise model correct as stated, for the model-space posterior and for the image of
   the parameter posterior? Is "the law of π is the same for every law satisfying GR^c" true?
3. **Hypothesis translation.** Check line by line that (E^σ), (F₀), (OS), (ID^{M,σ}), (F_λ), (BM^σ) for κ = (x, β, v)
   are exactly the W3-POST2 hypotheses for the unit-noise model (x, β/√v, 1) with the same constants. Any hypothesis of
   Claims C, E, A1, D that is not carried over (regime R1, p ≥ 2, A ≥ 1, s₀ ≤ K, "at that n")?
4. **MIS-R (i).** Does it follow from R′(b) + W3-POST2 Claim C exactly as stated there (constants depending only on
   the listed quantities; per-n; uniform)? Are consequences 1–3 right (factor 2, the ξ_q bound, the proxy/cancellation
   bounds)?
5. **MIS-R (i′).** These clauses are in expectation and per n; W3-POST2 states the corresponding facts (A1 item 5(a),
   E (5b′)) only as O_P statements. Is the expectation form derivable from the W3-POST2 proof files (Lemma C2, (C5′)(a),(b),
   Lemma E1(b), the assembly in E2 and in C's proof) with thresholds depending only on the constants? Name any step
   that fails or needs an extra hypothesis. Is (c) right (the constant c″ ≥ cn/(n−1))?
6. **MIS-R (ii).** Is "(GR^c | 𝓕_n): W_n independent of 𝓕_n, N(0, I)" enough for (a)? Any measurability gap (κ_n random,
   p random, S₀(κ_n) random set)? Are (b) and (c) correct as stated (max over slices; the limsup form)?
7. **Corollary G.** (a): does C-MIS Proposition P(a)'s proof give GR^c at each n for n-dependent parameters and σ² ≥ 0?
   (b): do the steps of C-MIS Lemma GD(b) go through with σ²_𝒞 varying, and do they give the class 𝒦^λ_n needed for
   E δ_n = O(r_n) (including (OS) from (F_w), p ≥ 2, the probability of the bad event)? Anything missing?
8. **Corollary H.** Is the transfer of W3-POST2 Claim D correct (thresholds, the constant C_H, what the reference law
   is, what "analog of Song–Liang Theorem 4" may and may not be said to mean)?
9. **Remarks SNR, P, U.** True as stated? In Remark SNR, is any listed claim not a function of the posterior alone
   (so that the scaling argument would not apply)? In Remark P, check Theorem F's hypotheses under rescaling.
10. **Overclaiming.** Is any sentence of §9 ("Implies", "New", "Not claimed") stronger than the statement supports?
11. **Counterexample hunt.** Try to construct a counterexample to any clause as written (edge cases: p = 2, s = K,
    v → 0 or ∞ with n, rank-deficient centred design, non-unique β, y^r constant, c < 0).

## Output
Write your review to `Theory_work/Wave3/W3-MISR/reviews/L01_statement_lock_sol.md` (create it; touch nothing else):
findings numbered, each graded FATAL / MAJOR / MINOR / NIT with file:line evidence and a concrete required change;
then one verdict line `VERDICT: LOCK | LOCK-WITH-CHANGES | REJECT`. Be specific and adversarial; do not praise.
Your final message: the verdict and the counts per grade.
