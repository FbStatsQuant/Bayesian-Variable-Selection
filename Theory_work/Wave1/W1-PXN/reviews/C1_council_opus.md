GATES: G1 PASS, G2 PASS, G3 PASS, G4 PASS, G5 PASS, G6 PASS
SCORE: 8.3 / 10

Reviewer: council seat C1 (Claude Opus 5.5). Independent reading; I did not open reviews/ (other than the brief), LOG.md or PLAN.md.

## Gate reasons (one line each)
- **G1 PASS.** I re-derived every step on the FINAL_PROOF.md route and found no error. Checked: Lemma CR and [CONC′]; Tr-J(a)–(c); Lemma E (E1)–(E6); Lemma B(i), (i′), (iii) (Haar/Beta and independence); P3′ moment, Jensen and deletion steps; P4 single-column BF and limit law; P5; Lemma Λ(a)–(c); the full D_S case list and c₅ ≥ c₂; the repaired (L) addition step; Lemma LS (i)–(iii) against v3_engine.h; P8♯ m♯_n bound and de-randomisation; (C) closure; W7 Lemma 2 / Corollary B constant chain.
- **G2 PASS.** The hypotheses used are exactly LH-iid + SIZE + (OP) + A fixed. T03♯'s R1/G/R/SE_λ(j₀)/SE_w(m♯_n; g₀)/BM-∞ are discharged on ℰ♯_n with constants that do not depend on the sequence.
- **G3 PASS.** No hidden assumptions. EX-A (exact DP and score ties), GUARD and OP-LS0 are declared, and the exact-branch convention is explicit. Nothing assumes p ≤ n or a lower growth bound on p.
- **G4 PASS.** Statuses I rely on:
  - T22(i-a), (ii-a): PROVED-LOCKED, cross-family (TH116).
  - T03♯: PROVED, SF + XF VERIFIED (TH128).
  - Lemma RO: PROVED, SF VERIFIED, XF VERIFIED* (TH01 row).
  - W7 Lemma 2 / Corollary B: the registry says "Corollary B XF GAP" (TH163, ID_REGISTRY.md:311). I re-checked the constant chain myself (W7-PART/PROOF.md:198-228, 240-272). The (R′) fallback (CR_corr_tails.md:41-51) also gives (R-c) on its own.
  - W7 Theorem A: used only through the direct strict-margin argument (R_branch_repair.md:20-26), which I checked against v3_blocks.h:139-161.
  - Classical results: Laurent–Massart, Hotelling's density, Wendel's inequality, the Mills ratio.
- **G5 PASS.** The rates √(log n/n) do not depend on A. A enters D = A, A(s₀+2), δ_n, L_n, k_n, j₀, the U3 penalty (2A+1) log n, the (L) remainder and the Theorem R onset, and each is tracked in STATEMENT §3 / FINAL_PROOF §7. One inaccurate sentence about the form of the onsets: issue 5.
- **G6 PASS.** Each part of the method the proof relies on matches the code:
  - Partition (v3_blocks.h:144-161): split while size > B, then next-fit with whole clusters.
  - LS0 search (v3_engine.h:378-418): all flips (additions capped at K) and swaps; strict improvement; lexicographic ties; at most ℓ moves, then a final scan; `local_limit` on an improving scan at the cap.
  - ℓ_n = ⌈log₂(n+p+1)⌉ (v3_preprocess.R:23).
  - Start-mode DP with a unique optimum on {π₀(S°) > ½} (v3_start.h:183-239).
  - Exact-branch rule (v3_preprocess.R:18).

  The statement correctly says LS0 is not in the production core: production calls `local_search(led.hpmS, ell, tier, false)` (v3_core.cpp:447), and the LS0 call `local_search(S̃₀, ell, tier, true)` exists only as an interface.

## Issues

1. **MAJOR (form, not mathematics). The proof is a map over a patched text, not a supplement-ready document.**
   - Evidence: FINAL_PROOF.md:4-6 says unchanged steps are "proved by the cited lines of PROOF … as amended by ERRATA". ERRATA.md:6-29 has 22 line-keyed corrections, several of which are verbatim replacement sentences. Six further lemma files override PROOF in places. A referee has to merge four layers by line number: PROOF, then ERRATA, then lemmas/, then FINAL_PROOF.
   - The mathematics survives this, but I would not accept the material *as a supplement* in this form.
   - **Fix required before any paper use:** one consolidated proof text that applies E-1..E-22 and the lemma files in place, in the FINAL_PROOF order. It should have no line-number cross-references to the candidate, no status chatter inside proofs, and must not use the superseded P2/[CONC]/[T03] labels. This does not block the verdict "proved".

2. **MINOR. The errata range is inconsistent.** FINAL_PROOF.md:6 says "rows E-1..E-20", but ERRATA.md has E-21 (PROOF:475-477, the (O3) probability gloss) and E-22 (PROOF:483-484, the (O5) numbers), and the brief says E-1..E-22. **Fix:** change the range to E-1..E-22 (both rows concern remarks, not proof steps).

3. **MINOR. A lemma header is stale.** L_strict_localmax.md:3 still reads "role in (L) under review by R17", while FINAL_PROOF.md:56-57 and ERRATA E-12 record R17 as VERIFIED. **Fix:** update the status line.

4. **MINOR. A symbol is undefined in the locked statement.** STATEMENT.md:59 ("S° ∈ 𝓡₀") uses 𝓡₀, which §1 never defines. W6 uses 𝓡_d (T38_STATEMENT.md:86). **Fix:** define 𝓡₀ (the zero-extra lattice references, Φ(S°) = c with S° ⊆ S₀) or drop the clause; Φ(S°) = c already says what is needed.

5. **MINOR. The description of the onset conditions is inaccurate.** FINAL_PROOF.md:21 says every onset condition is of the form "n/log n ≥ const(A, …) or weaker". Two do not fit:
   - L_nδ_n ≤ λ₀/2 with L_n ≍ (As₀ + s₀/2) log₂ n and δ_n ≍ √((A+1) log n/n) is n/(log n)³ ≳ const(A).
   - SIZE's n₁ is a property of the sequence p_n, not of n alone.

   **Fix:** reword to "each onset is an explicit polylog-vs-polynomial condition in n, depending on A and the fixed parameters, plus the SIZE onset n₁ of the sequence".

6. **MINOR. The illustrative number in E-22 depends on an unstated σ².** ERRATA.md:29 uses (n/2) log(1 + c₂/12). With c = 1, v = 0, β = 1, ψ = .5, ρ = .7, one gets θᵀΣθ = 1 + .25 − 2(.5)(.5) = .75, so M = 2.5, and 4(σ² + M) = 12 requires σ² = 0.5. With σ² = 1 the factor is c₂/14 and the value is ≈ 0.775 at n = 200. **Fix:** state σ², or use 0.775 for σ² = 1. The conclusion (vacuous against ≈ 20) is unchanged.

7. **MINOR (scope wording, G6).** STATEMENT.md:35 and LS_P6_repair.md:48-50 correctly keep the production bridge as an implementation obligation. **Fix:** add one sentence naming the concrete obligation, so "v3 + LS0" is unambiguous about what code it refers to: LS0 = `local_search(S̃₀, ell_n, tier, emit_centre = true)` on the start mode returned by `start_mode`, executed after R̄ on every fit counted in 𝒪. Note also that the current core does not call it (v3_core.cpp:447).

8. **MINOR (diagnostic, not a defect). The P4 centring offset in the n8 runs is explained.** numerics/n8/SUMMARY.md item 7 reports that all ten cells sit below the predicted mean. This is consistent with the exact identity of P4 (PROOF.md:281): the offset is log π₀(S°) itself, ≈ log(1 − 0.24) ≈ −0.27 at the n = 300 median, plus the O(1/n) prior-ratio error. It does not bear on the limit claim. **Fix (optional):** one sentence in the write-up saying that the finite-n centring error equals log π₀(S°) + o(1) and is O_P(√(log n/n)).

## Overall reading
The headline is proved by the material, given (OP) and the cited verified results: on LH-iid with SIZE and p ≤ n^A for any fixed A ≥ 1, v3 + LS0 has P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀δ₁ + D_n → 0.

I followed each step on its stated event:
- (R): the W7 Corollary B constant chain, and independently the elementary (R′) route through Lemma CR, which I re-derived.
- (S): P3′ via the unconditional Beta laws of Lemma B, Tr-J truncation with D = A, Lemma E remainders and locked T22(i-a).
- (E): P5 under EX-A.
- (T): Lemma Λ with the Haar step, the full D_S case list (c₂ ≤ c₅ holds, so the single Ω_n event serves both (D_S) and (L)), the repaired (L) addition step, and the repaired Lemma LS with ℓ_n ≥ c.
- (P): the T03♯ hypotheses are discharged on ℰ♯_n with L_n = O(log n), the m♯_n ≤ k_n bound is correct, and the de-randomisation argument is valid as a subsequence/contradiction argument.
- (C): Lemma RO / GUARD closure with the exact-branch cases.

None of these steps uses p ≤ n. A > 1 costs only constants and onsets, and every Gram matrix inverted has size O(log n). The weaknesses are not mathematical. First, the proof exists only as a correct map over a candidate patched by 22 errata and six lemma files, so it must be consolidated before it can serve as a refereed supplement (issue 1). Second, there are several small presentation defects (issues 2–7). The result is purely asymptotic and the statement disclaims any finite-n content, which the numerics confirm: the route is visibly fragile at n = 150 and mostly clean at n = 300. I found no gap that changes a conclusion.

---
## Disposition (W1-PXN lead, 2026-11-08)
Round 1: all gates PASS, score 8.3. Minors fixed: #2 (errata range, already fixed after the Codex seat), #3 (L header),
#4 (𝓡₀ replaced by the explicit lattice-reference statement), #5 (onset wording incl. SIZE onset n₁), #6 (σ² stated in E-22;
value 0.775 for σ² = 1), #7 (concrete LS0 call and the production call named in STATEMENT §1). #8 noted in LOG (already
recorded as a diagnostic). #1 (MAJOR, form): accepted as the next step — a single consolidated supplement text applying
E-1..E-22 and the lemma files in place; recorded as an open item in REPORT.md (non-blocking per the reviewer).
