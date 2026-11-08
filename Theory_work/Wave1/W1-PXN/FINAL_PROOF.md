# W1-PXN — FINAL PROOF (consolidated, v1, 2026-11-08)

Theorem: STATEMENT.md §2 (locked v2, with §5 change notes). This file is the single definitive reading of the proof: it
fixes the order of steps, the events, the onset conditions, and which text proves each step. Unchanged steps are proved by
the cited lines of PROOF = `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/API-PXNGAP/PROOF.md` **as amended by
`lemmas/ERRATA.md` (rows E-1..E-22)**; replaced steps are proved in the named `lemmas/` files, which supersede PROOF there.
NBH = `Theory_work/Old_Projects/New_BVS_Headquarters/`.

## 0. Standing conventions
- Setting, score, method, runs, (OP): STATEMENT §1. Fixed: g, c, v, ρ, ψ_i, β's, σ², A ≥ 1; s₀ = 2c+v; s = c+v.
- **Exact arithmetic**: EX-A (scores and the start-mode DP exact). GUARD and OP-LS0 are hypotheses (STATEMENT §1).
- **Exact-branch convention** (lemmas/R_branch_repair.md §3): blocks, tables, π₀, S̃₀, LS0 of R̄⁺ are the deterministic
  data functions computed on every branch.
- **Group versions / Lemma T** (PROOF:69-71, 104-119; VERIFIED R14): every block object has a group version; on
  𝒜_n := {blocks = groups} they coincide; P(E) ≤ P(Ẽ) + P(𝒜_nᶜ); all laws used are unconditional.
- Population facts F2–F5, λ₀ := λ_min(Σ) ≥ (1−ψ̄)(1−ρ) (PROOF:55-58; VERIFIED R13). Constants φ₀² := λ₀/2,
  M := 2θᵀΣθ + 1, b_min := ½ min(β_i²ψ_i², β_i², (β^vis_h)²).
- **Onset.** n₀ is taken large enough that, for n ≥ n₀: SIZE holds (n ≥ n₁); s₀ ≤ K; ℓ_n = ⌈log₂(n+p+1)⌉ ≥ c; n ≥ 2(s₀+2) + g;
  every "for n ≥ n₀" condition of the lemmas below holds (Tr-J: n ≥ 8(J+1), t′ ≥ 6J, τ_n ≤ ½; Lemma E; U3:
  C₂n^{−1/3} ≤ c′H/(4H+c′) with H = σ²+M, c′ = c₂/2; m_n(c₂/2) > 0; L_nδ_n ≤ λ₀/2; (L): x_l ≤ ¼ and the additive remainder
  ≤ 1). All listed conditions hold eventually for every fixed A (C1 Codex #1); each onset is an explicit polylog-vs-polynomial condition in n
  depending on A and the fixed parameters, plus the SIZE onset n₁ of the sequence p_n (C1 Opus #5); a sufficient envelope for the
  slowest of them (L_nδ_n ≤ λ₀/2 and the (L) remainder) is n/(log n)³ ≥ C(A, fixed parameters).

## 1. Probability tools
- [LM] Laurent–Massart (2000), eqs (4.3)–(4.4) (citation checked by R11).
- **Lemma CR, [CONC′]** (lemmas/CR_corr_tails.md; XF VERIFIED R19): P(|r̂−r| > δ) ≤ 6e^{−(n−1)δ²/1024}; with
  δ_n = 32√(2(A+1)log n/(n−1)), P(max_{j<k}|r̂_jk − Σ_jk| > δ_n) ≤ 3n^{−2}.
- **Lemma Tr-J** (PROOF:123-148 with E-5, E-6; XF VERIFIED R11).
- **Lemma E** (PROOF:160-207 with E-1..E-4; XF VERIFIED R12), stated on ℰ* = ℰ(𝔉, φ₀) ∩ {‖μ‖² ≤ Mn}. Its event depends
  on the family (R30 #2); two applications: **𝒟_start** := Lemma E's event for 𝔉_start = {U ⊆ C_h : h ≤ G_n} ∪ {∅}
  (J = g, D = A, C = 2^{16}); **𝒟_search** := its event for 𝔉_n = {A : |A| ≤ s₀+2} (J = s₀+2, D = A(s₀+2), C = 2^{s₀+2}).
  Each has P(𝒟ᶜ ∩ ℰ♯_n) ≤ 2e^{−n^{1/3}} + Cn^D[n^{−4(D+1)}e^{√(8J(D+1) log n)} + 2n^{−2(D+1)}] with its own (J, D, C) (E-1).
  Tr-J thresholds are indexed by D: t_{n,D} := 8(D+1) log n, τ_{n,D} := t_{n,D}/n.

## 2. Design events
- ℰ♯_n (lemmas/P8_T03sharp.md step 2; XF VERIFIED R19): λ_min(R̂_T) ≥ φ₀² for all nonempty T with |T| ≤ L_n :=
  s₀ + max{m_n, k_n, j₀, g, s₀+2} = O(log n); ‖μ‖² ≤ Mn; min_{S₀}θ*² ≥ b_min; s₀ ≤ K. P(ℰ♯_nᶜ) → 0 (CR + SLLN on the
  finitely many signal columns). ℰ♯_n ⊆ ℰ_n of PROOF P2 (PROOF:213-220, VERIFIED R13), so ℰ♯_n serves every use of ℰ_n.
- 𝒜_n: Theorem R (lemmas/R_branch_repair.md §1–2; PROOF:77-96 with E-15..E-17; XF VERIFIED R14): (R-a), (R-b) with
  the explicit constant, (R-c) P(𝒜_nᶜ) ≤ p^{−C} eventually and summable. Independent route (R′) (CR_corr_tails.md).

## 3. Start: (S) and (E)
- Lemma B (PROOF:222-234 with E-7; XF VERIFIED R13 for (i), (i′), (iii); (ii) restricted, unused).
- **P3′** (PROOF:238-268 with E-19, E-20; XF VERIFIED R16): on 𝒢_n := 𝒜_n ∩ ℰ♯_n ∩ 𝒟_start ∩ {max X_{h,V} ≤ τ_{n,A}},
  E[q̃1_{𝒢_n}] ≤ C_q√(log n/n) (C_q ∝ C_e g e^{2κ_E}√(A+1)); ẽ = O_P(p√n e^{−c₆n}); on {q < 1}, T22(i-a) (locked; "for every
  partition and positive tables ... and every S° ∈ Ω", T22 STATEMENT.md:35) gives 1 − π₀(S°) ≤ (s+1)q/(1−q) + se;
  P(q < 1) → 1 ⇒ 1 − π₀(S°) = O_P(√(log n/n)). **(S), first part.**
- **P4** (PROOF:277-284; XF VERIFIED R16): T22(ii-a) on 𝒜_n, prior ratio, singleton BF, Lemma B(iii), Slutsky ⇒ the
  limit law of log π₀(S₀) + c log p + (c/2) log n. **(S), second part.**
- **P5** (PROOF:286-288 with E-10; lemmas/LS_P6_repair.md "P5 qualifications"; XF VERIFIED R15): on {π₀(S°) > ½} the
  start mode is unique, = S°, and exact max-plus DP + backtracking return it (N3 bypassed, not proved). P(π₀(S°) > ½) → 1
  by (S). **(E).**

## 4. Search: (T), (K)
- **Lemma Λ** (PROOF:307-326 with E-5; XF VERIFIED R13 incl. the Haar-span step): max_{A∈𝔉_n}|Λ_A/n − λ(A∩𝒮𝒱)| → 0 in
  probability, 𝔉_n = {|A| ≤ s₀+2}, family exponent D = A(s₀+2).
- **Lemma U, (D_S), (L)** (PROOF:296-370 with E-12..E-14; lemmas/L_strict_localmax.md; XF VERIFIED R17 (key lemma),
  arithmetic R19): on Ω_n := ℰ♯_n ∩ 𝒟_search ∩ {max|Λ_A/n − λ| ≤ c₂/4}, (D_S) holds for every lattice state with margin
  m_n(c₂/2) = (n/2)log(1 + c₂/(4(σ²+M))) − (2A+1) log n − 2κ_E − 2 > 0; on Ω_n ∩ 𝒵_n, (L) holds; P(𝒵_nᶜ) ≤
  2/(√(2π)u_n log n) → 0, u_n := √(2 log p + 2 log log n) (the Mills threshold; not a Tr-J threshold).
- **Lemma LS, P6′** (lemmas/LS_P6_repair.md; PROOF:372-399 superseded; XF VERIFIED R15 for (ii), (iii); repaired (i)
  XF VERIFIED R21): on 𝒯_n := 𝒜_n ∩ Ω_n ∩ 𝒵_n ∩ {S̃₀ = S°}, with ℓ_n ≥ c: LS0 of R̄⁺ scores S₀ at the c-th scan, reaches it
  after exactly c moves, returns it local_certified with c+1 scans and ≤ 1 + (c+1)(p+s₀p) scores. P(𝒯_n) → 1 (union bound
  of vanishing complements; no independence used). **(T), (K).** General cost bound PROOF:441 (VERIFIED R15).

## 5. Posterior: (P)
- **P8♯** (lemmas/P8_T03sharp.md v2; XF VERIFIED R19): T03♯ (theorem of record NBH/branch_snapshots/W6-FIXREV2/
  STATEMENTS.md:19-60, "V03 and A-REV2: VERIFIED under exactly these hypotheses") applies to every deterministic design
  sequence in ℰ♯_n with fixed constants (A, s₀, M, φ₀, g₀ = φ₀², σ², BM-∞ via b_min); the de-randomisation lemma (PROOF:405-410,
  VERIFIED R19 incl. quantifiers and kernels) gives δ₁ = 1 − π(S₀) = O_P(√(log n/n)) under the joint law; Eδ₁ → 0. **(P).**

## 6. Output: (C)
- Deterministic: S₀ ∈ 𝒮⁺ and π(S₀) > ½ ⇒ Ŝ⁺ = S₀ (PROOF:443-444; VERIFIED R15). Markov: P(δ₁ ≥ ½) ≤ 2Eδ₁.
- Closure (lemmas/LS_P6_repair.md "Closure citation"; VERIFIED R15 under (OP)): 𝒪 ∩ {S₀ ∉ 𝒮⁺} ⊆ 𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺} ⊆
  {LS0 of R̄⁺ does not score S₀}, by GUARD (G2) / Lemma RO and the definition of R̄⁺; on the exact branch with s₀ ≤ K the middle event is
  empty; for n with s₀ > K the inclusion is trivial and π(S₀) := 0 (R_branch_repair.md §3, R21 #1).
- Hence for every n: P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2Eδ₁ + D_n and D_n ≤ P(LS0 of R̄⁺ does not score S₀); for n ≥ n₀ also
  P(LS0 of R̄⁺ does not score S₀) ≤ P(𝒯_nᶜ) → 0 (R30 #4); with (P),
  P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0; P(𝒪 ∩ {Ŝ⁺ = S₀}) = P(𝒪) − P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) gives the difference form and the liminf identity. **(C).**

## 7. A-dependence (summary; each item VERIFIED in the review named)
Every step holds for each fixed A ≥ 1 (A > 1 included); no step uses p ≤ n or a lower growth bound on p; only Gram matrices
of size O(log n) are inverted. A enters: Tr-J/Lemma E family exponents D = A, A(s₀+2) (R11, R12); δ_n, L_n, k_n, j₀ (R19);
U3 penalty (2A+1) log n and the (D_S) onset n/log n ≳ (4A+2)·4(σ²+M)/c₂ (R17); (L) remainder O(A n^{−1/3} log n) (R17, R19);
Theorem R onset ((2+C)A+½) log n ≤ (n−4)I* (R14); P3′ constant C_q ∝ √(A+1) (R16). Rates √(log n/n) do not depend on A. No
uniformity over growing A; no finite-n guarantee (all onsets are asymptotic; vacuous at n = 200, PROOF §11 (O5)).
