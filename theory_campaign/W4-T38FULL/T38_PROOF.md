# T38: full proof (assembled from the campaign; every repair applied)

Run W4-T38FULL, 2026-11-02. This is a **candidate**: it has not been reviewed or adopted. The statement and the dependency map are in `T38_STATEMENT.md`; labels such as "a3" or "b1.4" refer to that map.

Source proofs are cited by label and not copied. Four results are new in this run, and their proofs are given in full:
- Lemma LS-score (§3.1);
- Lemma M (§3.2);
- Theorem b1 (§3.3);
- Proposition LH-LAT (§3.4).

The §2.3 ORTH composition and the §4.2 D2 sketch are also new. Notation follows 00_COMMON, with Φ(S) = |S Δ S₀|, Δ(T) = ‖(I − P_T)μ‖²/(n−1), and Lat(·) as in T38_STATEMENT Part I.

---

## 0. Conventions used throughout

**(0.1) The production local search** (METHODOLOGY_v3 §6.10; engine `local_search`, `Scripts/SMC_BVS/core/cpp/v3_engine.h` lines 378–418, re-read in this run; also W3-VT38E §4 and W3-VT37R §5).
- Given a centre C and a move counter t = 0, the search repeats the following two steps.
  1. **Scan.** Score every feasible flip of C (additions only if |C| < K) and every swap of C.
  2. **Move or stop.** Let T* be the best scanned neighbour, with exact ties broken lexicographically. If F(T*) > F(C) and t < ℓ, set C ← T* and t ← t + 1, and go back to step 1. Otherwise stop.
- So a scan always precedes the move-limit test: the code completes the scan, and only then tests `A.moves >= ell`. The centre is passed to `eval` with the flag `emit_centre`, so it is scored only when that flag is true.
- Every scanned model enters the scored set.

**(0.2) Output-available event.** 𝒪 = {status ∈ {exact, completed}}, and U = 𝒪ᶜ.
- On 𝒪 ∩ (SMC branch), the final run was launched and executed all its rounds. This is status semantics, M §6.9.
- On 𝒪 ∩ (exact branch), every feasible model is scored (M §6.2).
- Under GUARD, Lemma RO [W2-BOOK] gives 𝒪 = 𝒢ᶜ ∩ 𝒪̄, and on 𝒪 every reported output equals its R̄-version. Here 𝒢 = {resource_limit}, and 𝒪̄, 𝒮̄, Ŝ̄ refer to the potential uninterrupted run R̄.
- LS0 is a deterministic function of the data. Under OP-LS0 it is executed on 𝒪 (post hoc is allowed), so 𝒮⁺ = 𝒮̄⁺ on 𝒪.

**(0.3) Probability.** P is the joint law of the data and the algorithm; P₀ is the law of the data. Every bound below is either a P₀-probability or the expectation of an algorithmic conditional probability given the data. They are combined by the tower property, and bounded convergence turns "→ 0 in P₀-probability" into "→ 0 in expectation" for [0,1]-valued quantities.

---

## 1. Part (0): the composition

**Claim.** For every n,

  P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[δ₁] + P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}).   (1.1)

*Proof.*
1. By (0.2) and Lemma RO(2) [W2-BOOK], P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ P(𝒪̄ ∩ {Ŝ̄⁺ ≠ S₀}).
2. On {π(S₀) > ½}, every S ≠ S₀ has π(S) ≤ 1 − π(S₀) < ½ < π(S₀). So F(S₀) > F(S) strictly, and S₀ is the unique global maximiser.
3. On 𝒪̄ ∩ {S₀ ∈ 𝒮̄⁺} ∩ {π(S₀) > ½}, the running-best rule over 𝒮̄⁺ therefore returns S₀. No tie is possible, so the tie rule plays no part (T11(vii); [W1-T38E §7 step (1)]).
4. Hence 𝒪̄ ∩ {Ŝ̄⁺ ≠ S₀} ⊆ {δ₁ ≥ ½} ∪ (𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}).
5. Markov's inequality gives P₀(δ₁ ≥ ½) ≤ 2E₀δ₁. ∎

This is locked T21 (C1), with the GUARD form of [W2-BOOK Thm 4]. It is re-derived here because T38 uses no T21 route. In particular, it does not use route (e) or H24.

**Consequence (liminf form).**
- Under (P), δ₁ ∈ [0,1] and δ₁ → 0 in P₀-probability, so E₀δ₁ → 0.
- If moreover D_n := P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}) → 0, then P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0.
- Since P(𝒪 ∩ {Ŝ⁺ = S₀}) = P(𝒪) − P(𝒪 ∩ {Ŝ⁺ ≠ S₀}), we get P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − P(U) − o(1).
- In particular liminf_n P(𝒪 ∩ {Ŝ⁺ = S₀}) ≥ 1 − limsup_n P(U), and P(𝒪, Ŝ⁺ = S₀) → 1 − u whenever P(U) → u.
- The brief's "P(Ŝ = S₀) → 1 − limsup P(U)" is not a well-formed limit [W1-T38E headline 1]; the forms above replace it.

**Sources of (P).**
- Locked T03(i): 1 − π(S₀) = O_P(√(log n/n)) under G, R, SE, BM-C or BM-∞, with H-T02 closed by locked T02(i).
- Or T03♯ [W1-T03R]: G, R, SE_λ(j₀), SE_w(m♯_n; g₀), BM-∞ or BM(c) with c > L*. This was VERIFIED by W2-VT03R.
- Repairs carried:
  - W2-VT03R R1: the proof's own deterministic thresholds hold only from n ≈ 2×10⁶. This matters for disclosure only.
  - W2-VT03R R2: by Lemma A1 the anchored SE is equivalent to SE on every T with |T ∖ S₀| ≤ m.

It remains to bound the discovery term D_n route by route. Throughout:
- on the exact branch, S₀ ∈ 𝒮̄ as soon as s₀ ≤ K;
- P₀(s₀ > K_n) → 0 under R;
- so only 𝒪̄ ∩ (SMC branch) needs work.

---

## 2. Part (a): favourable regime

**2.1 Bound.** On 𝒪̄ ∩ SMC, the final run of R̄ draws Q_f ≥ 4N_e(L+6) ≥ 1 iid π₀ models, and all of them are scored (00_COMMON §2). By locked T11(iii), in the R̄ form of [W2-BOOK §2],

  P(𝒪̄ ∩ SMC ∩ {S₀ ∉ 𝒮̄} ∣ data, 𝓒) ≤ (1 − π₀(S₀))^{Q_f} ≤ 1 − π₀(S₀).

Taking expectations:

  D_n ≤ P₀(s₀ > K) + E₀[1 − π₀(S₀)].   (2.1)

Under (F), 1 − π₀(S₀) → 0 in P₀-probability, so D_n → 0 by bounded convergence. This holds with or without LS0, since 𝒮 ⊆ 𝒮⁺. ∎

**2.2 Sources of (F).**
- **(F1)** Locked T22(iii), under G, R, SE-blk, EXP′, VIS, NL_η and NL_avg(κ), gives 1 − π₀(S₀) = O_P(2^B √(log n) n^{−κ}) → 0, because B ≤ 16.
  - EXP′ is a *conclusion* of [W1-EXP Thm 1], whose hypotheses (G, R-lite, SE-blk) are among T22(iii)'s.
  - So EXP′ is removed from the hypothesis list (a3, VERIFIED by W3-VEXP).
  - W3-VEXP R1 is the data-computable finite-n certificate. It replaces κ_EXP, which is ≈ 100–1,700 nats at the study's signal scale.
- **(F2)** Under BO, [W1-EXP Lemma 2.3] gives δ_{T,l} = 0 on the leakage family. That is the locked NL_η with η = 0, and NL_avg(½) follows. BM-blk gives VIS. So (F1) applies verbatim with κ = ½ (a4; W3-VEXP R2).
- **(F3)** [W1-EXP Thm 6] with S° = S₀ gives 1 − π₀(S₀) = O_P(2^B n^{−1/2}) under G, R-lite, SE-blk, ZL(S₀), SPREAD and VIS-lin(S₀) (a5; VERIFIED).

**2.3 A joint family for (a) and (P): ORTH (new composition, checked here).**
- **Setting.** X′X = (n−1)I_p, with p ≤ min(n−1, n^A); s₀ fixed; fixed nonzero θ on S₀; G.
- **(P).** We need locked T03's hypotheses:
  - R holds, since λ_min(R_{S₀}) = 1 and ‖μ‖²/n = (n−1)‖θ_{S₀}‖²/n is bounded;
  - SE holds with φ₀² = 1;
  - BM-∞ holds, because fixed θ means M_n := θ²_min nφ₀²/(σ² log n) → ∞.
- **(F).** The partition is arbitrary, since every pair of columns is orthogonal (ties in the complete linkage), but BO holds for every partition.
  - SE-blk holds with φ₀² = 1.
  - EXP′ holds by Thm 1.
  - NL_η holds with η = 0, because δ_{T,l} = x_lᵀμ/√(n−1) = 0 for l ∉ S₀.
  - NL_avg(½) holds, because every E_{T,l} = 0.
  - VIS holds: for U_b* ⊄ T ⊆ C_b, ‖(P_{T∪U_b*} − P_T)μ‖² = (n−1)Σ_{j∈U_b*∖T}θ_j² ≥ (n−1)θ²_min ≫ M_n^V v_T log n, with v_T ≤ σ² + ‖θ‖² bounded.
  - So locked T22(iii) applies with κ = ½.
- **Conclusion.** Part (a) holds on ORTH with no open statistical input.
- **Limits.** ORTH has p < n, and it is not the study design.
- **Study relevance (a7, a8).** At the study size the start is dilution-masked [W3-VEXP Prop. D]. In-sample favourability for the iid S1/S3/S4/S6 designs is a GAP: it needs partition–noise decoupling.

---

## 3. Part (b1): the LS0 route

### 3.1 Lemma LS-score (new). Status: PROVED

**Definition.** For a model S ≠ S₀, let 𝒫(S) be its *feasible* progress neighbours (Φ decreases) and 𝒩(S) its other *feasible* flip or swap neighbours. The event **D_S** (W1-T37R) is: max_{T∈𝒫(S)} F(T) > max{F(S), max_{T∈𝒩(S)} F(T)}.

**Lemma LS-score.** Fix the data. Let C₀ be a centre with s₀ + |C₀ ∖ S₀| ≤ K. Suppose:
- (i) D_S holds for every S ∈ Lat(C₀) with Φ(S) ≥ 2;
- (ii) ℓ ≥ Φ(C₀) − 1;
- (iii) C₀ ≠ S₀, or the centre is emitted.

Then the production local search from C₀ scores S₀. It needs at most Φ(C₀) − 1 moves.

*Proof.*
1. **Lattice closure.** Progress moves map Lat(C₀) into itself [W1-T37R Lemma 2(a), VERIFIED by W3-VT37R]:
   - adding a missing truth enlarges U′ inside S₀;
   - deleting an extra shrinks P′;
   - swapping an extra for a truth does both.
2. **One step of the search.** Let S be the current centre, with S ∈ Lat(C₀) and Φ(S) ≥ 2. Under D_S, the best scanned neighbour T* is a progress neighbour, because the maximum over 𝒫(S) strictly exceeds every value in 𝒩(S). Also F(T*) > F(S).
   - So if t < ℓ the search moves to T* ∈ Lat(C₀), and Φ(T*) ≤ Φ(S) − 1.
3. **Moves needed.** Starting from C₀, Φ falls by at least 1 at each move as long as Φ ≥ 2. So after at most Φ(C₀) − 1 ≤ ℓ moves, the centre S′ has Φ(S′) ≤ 1. Hence the move limit never stops the search at a centre with Φ ≥ 2.
4. **Scoring S₀.** Consider the first centre S′ with Φ(S′) ≤ 1.
   - If Φ(S′) = 0, then S′ = S₀. Either S₀ = C₀, which is scored when the centre is emitted, or S₀ was scanned, and so scored, as a neighbour of the previous centre.
   - If Φ(S′) = 1, then S′ = S₀ ∖ {j} or S₀ ∪ {e}. S′ is scanned, because a scan precedes the limit test (0.1). Its scan contains S₀: the addition of j is feasible because |S′| = s₀ − 1 < K, and the deletion of e is always feasible. ∎

*Relation to the sources.* [W1-T37R Thm A(A3), lattice version] asks for D_S at every Φ ≥ 1 state, for (L) (S₀ is a local maximum), and for ℓ ≥ τ(C₀). It concludes *certification* at S₀. T38 needs only *scoring*, because π(S₀) > ½ then makes Ŝ⁺ = S₀ by (1.1). So (L) and the Φ = 1 states are dropped, and the cap requirement becomes ℓ ≥ Φ(C₀) − 1. This applies W3-VT37R R3 ("ℓ ≥ a + d suffices; the exact need is smaller") to the scoring problem.

### 3.2 Lemma M (uniform score comparison under population margins; new). Status: PROVED

**Lemma M.** Assume:
- G;
- p ≤ n^A;
- ‖μ‖² ≤ Mn;
- integers k ≥ s₀ fixed;
- φ₀ > 0;
- a sequence m_n ≥ M_n √(log n / n) with M_n → ∞.

There is an event E_n with P₀(E_n) → 1 on which the following holds for every n ≥ n₀ and for every pair (A, B) of models satisfying four conditions: |A|, |B| ≤ k, A ∪ S₀ has size ≤ k, λ_min(R_A) ≥ φ₀², and Δ(B) − Δ(A) ≥ m_n:

  F(A) − F(B) ≥ M_n √(n log n)/(4 C_R) − 2k log(2p(n+1)) − c₀,   with C_R := 2M + 4σ² and c₀ = c₀(M, σ², φ₀).   (3.1)

Here σ means σ* of 00_COMMON. The constant M in this lemma is the signal bound of R-lite; it is not the masked set M of §3.4.

In particular F(A) > F(B) for all such pairs simultaneously.

*Proof.* Write y_c = μ + e for the centred response, with e = Cε and RSS_S := ‖(I − P_S)y_c‖². The standardised RSS is RSS^y_S = RSS_S/s_y², with s_y² = ‖y_c‖²/(n−1).

1. **Prior and determinant.**
   - w(k+1)/w(k) = (k+1)/(2p−1−k) lies in [1/(2p), 1] for k ≤ p−1, so |log ϖ(A) − log ϖ(B)| ≤ k log(2p).
   - For an addition, D_{S+l}/D_S = (1 + (n+1)a)/(1 + b), with 0 ≤ a ≤ b ≤ ‖x_l‖² = n − 1 (Woodbury, [W1-T38E E1(b)], VERIFIED).
   - So this ratio lies in [1/n, n+1], D_∅ = 1, and |log D_S| ≤ |S| log(n+1).
   - Hence |½(log D_A − log D_B)| ≤ k log(n+1).
2. **Q versus RSS.** Q_S = min_β {‖y − X_Sβ‖² + (‖X_Sβ‖² + ‖β‖²)/n} [W1-T38E E1(a)].
   - So Q_S ≥ RSS^y_S.
   - If λ_min(G_S) ≥ φ₀²(n−1), plugging in the least-squares β̂ (with ‖X_Sβ̂‖² ≤ ‖y‖² = n − 1 and ‖β̂‖² ≤ 1/φ₀²) gives Q_S ≤ RSS^y_S + 1 + 1/(nφ₀²).
   - Therefore, with c_φ := 1.02 + 1/(nφ₀²),

     F(A) − F(B) ≥ ν log(RSS_B/RSS_A) − ν c_φ / RSS^y_A − k log(2p) − k log(n+1).   (3.2)

3. **The event E_n.** Let L := 4A(k+s₀) + 4. E_n is the intersection of three events:
   - (E1) ‖P_Sε‖² ≤ Lσ² log n for all S with |S| ≤ k + s₀;
   - (E2) |⟨(I−P_S)μ, ε⟩| ≤ σ‖(I − P_S)μ‖√(L log n) for all S with |S| ≤ k;
   - (E3) |‖e‖² − σ²(n−1)| ≤ σ²(n−1)n^{−1/3}.

   Each part has probability → 1:
   - for (E1), there are ≤ (2n^A)^{k+s₀} sets, P(χ²_j > t) ≤ 2^{j/2}e^{−t/4}, and L/4 > A(k+s₀);
   - for (E2), ⟨(I−P_S)μ, ε⟩ ~ N(0, σ²‖(I−P_S)μ‖²), the Gaussian tail is ≤ 2n^{−L/2}, and the same count applies;
   - for (E3), Chebyshev applies, since Var χ²_{n−1} = 2(n−1).
4. **RSS bounds on E_n.** Using P_S e = P_S ε and ‖(I−P_S)e‖² = ‖e‖² − ‖P_Sε‖²:
   - RSS_S = (n−1)Δ(S) + 2⟨(I−P_S)μ, ε⟩ + ‖e‖² − ‖P_Sε‖².
   - So RSS_B − RSS_A ≥ (n−1)m_n − 4σ√(LMn log n) − Lσ² log n.
   - RSS_B ≤ ‖y_c‖² ≤ (√(Mn) + σ√(2n))² ≤ C_R n.
   - Because μ ∈ span X_{S₀}, RSS_A ≥ ‖(I − P_{A∪S₀})e‖² ≥ σ²(n−1)(1 − n^{−1/3}) − Lσ² log n ≥ σ²n/2 for n ≥ n₀.
   - s_y² ≤ C_R n/(n−1) ≤ 2C_R, so RSS^y_A ≥ σ²n/(4C_R).
5. **Assembly.** Since m_n ≥ M_n√(log n/n), for n ≥ n₀(M_n, L, M, σ) we have (n−1)m_n − 4σ√(LMn log n) − Lσ² log n ≥ ½ M_n √(n log n).
   - Then log(RSS_B/RSS_A) ≥ (RSS_B − RSS_A)/RSS_B ≥ M_n√(log n)/(2C_R√n).
   - Multiplying by ν ≥ n/2 gives ν log(RSS_B/RSS_A) ≥ M_n√(n log n)/(4C_R), the first term of (3.1).
   - The second term of (3.2) is ≤ (n/2 + 0.01)c_φ·4C_R/(σ²n) =: c₀.
   - Since √(n log n) ≫ log n, F(A) > F(B) for all n ≥ n₀. ∎

*Remarks.*
1. E_n is uniform over all sets of size ≤ k + s₀. So no count of the pairs is needed, and the pairs may even be chosen after seeing the data. T38 uses a deterministic family anyway.
2. The only eigenvalue condition is on A. In the application, A ⊆ S° ∪ S₀ is a fixed set.
3. The lemma is the "population-margin" version of the comparison step in [W1-T37R Thm C / W3-VT37R R5]. It avoids PGD by assuming the margins directly.

### 3.3 Theorem b1 (new). Status: PROVED-UNDER (M1)–(M3)

**Theorem b1.** Assume G, (P), OP-LS0, and a deterministic S° = U° ∪ P° with |P°| ≤ d and Φ(S°) ≤ φ̄ (d and φ̄ fixed). Assume also (M1) ELIG(S°), (M2) POP-LAT(S°, m_n) and (M3). Then D_n → 0, so

  P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0.

*Proof.*
1. **Eligibility.** On {π₀(S°) > ½}, S̃₀ = S°: by [W1-T38E E3(i)], no other state can have π₀-mass ≥ ½, so there is no tie.
2. **Lattice progress.** Put k := s₀ + d + 1. For S ∈ Lat(S°) with Φ(S) ≥ 2, the progress neighbour A_S of (M2) is a subset of S° ∪ S₀. By (M3) and interlacing, λ_min(R_{A_S}) ≥ φ₀².
   - Every B ∈ 𝒩(S) ∪ {S} has |B| ≤ k, and Δ(B) − Δ(A_S) ≥ m_n.
   - By Lemma M, on E_n we get F(A_S) > F(B) for all such B. Hence max_𝒫(S) F ≥ F(A_S) > max(F(S), max_𝒩(S) F), which is D_S.
3. **Scoring.** For n large, ℓ_n = ⌈log₂(n+p+1)⌉ ≥ φ̄ − 1 and s₀ + d ≤ K. Lemma LS-score with C₀ = S° then gives S₀ ∈ 𝒮_LS0. Under OP-LS0, LS0 runs on 𝒪̄.
4. **Bound.** D_n ≤ P₀(π₀(S°) ≤ ½) + P₀(E_nᶜ) + 1{n < n₀} + 1{ℓ_n < φ̄ − 1} + P₀(s₀ + d > K) → 0, where n₀ is Lemma M's threshold. The exact branch is covered by §1 once s₀ ≤ K. Then apply §1. ∎

*Sufficient condition for (M1).* [W1-EXP Thm 6] at the reference S° (b1.6): G, R-lite, SE-blk, ZL(S°), SPREAD and VIS-lin(S°) give 1 − π₀(S°) = O_P(2^B n^{−1/2}) → 0.

*Alternative for (M2), with a data-dependent centre.* If TD′_P(R_{a,d}) holds with probability → 1 and ℓ ≥ a + d, then [W1-T37R Thm A(A3)] gives repair from *every* centre in R_{a,d}. So (M1) can be weakened to P(S̃₀ ∈ R_{a,d}) → 1.
- The asymptotic source is [W1-T37R Thm C(C2)] under PGD(η) + LD*, with repairs [W3-VT37R R4, R5]. Its status is PROOF SKETCH.
- PGD can fail under SE + BM-∞ (COUNTEREXAMPLE C3, VERIFIED).
- The union bound over R_{a,d} costs C(s₀, ≤a)·p^d states [W3-VT37R R6]. Theorem b1 avoids that cost because S° is deterministic.

### 3.4 Proposition LH-LAT and Corollary b1-LH (new). Status: PROVED

**Setting.** LH in its exact-Gram realisation [W1-EXP §4.1–4.2]:
- X′X = (n−1)Σ_LH and p ≤ n−1;
- groups of size g with within-group equicorrelation ρ_h ∈ [ρ₋, ρ₊] ⊂ (0,1);
- c linked pairs (a_i, b_i, ψ_i) with 0 < |ψ_i| < min(ρ_{a_i}, ρ_{b_i});
- hubs a_i = j_{a_i} and b_i = j_{b_i}, with θ_{a_i} = β_i ≠ 0 and θ_{b_i} = −ψ_iβ_i;
- visible hubs h with θ_h ≠ 0; all other coefficients zero;
- M = {b_1, …, b_c} and S° = S₀ ∖ M, so P° = ∅ and Φ(S°) = c.

**Units and additivity.**
- The *units* are: each pair union C_{a_i} ∪ C_{b_i}, each visible group, and each null group. Σ is block-diagonal over units (W1-EXP §4.1: groups are independent except for the linked pairs).
- Each unit's coordinates of μ = Xθ lie in that unit's span. In exact Gram, columns from different units are orthogonal.
- So P_T = Σ_u P_{T∩u}, and Δ(T) = Σ_u Δ_u(T ∩ u), where Δ_u(T_u) = ‖(I − P_{T_u})μ_u‖²/(n−1).
- Each Δ_u is the population residual variance, because X′X = (n−1)Σ exactly.

**Unit algebra for pair i** (drop the index i; unit-variance population inner products). μ_u corresponds to β(x_a − ψx_b), with ⟨x_a, x_b⟩ = ψ. For k ∈ C_b ∖ b, ⟨x_k, x_b⟩ = ρ_b and ⟨x_k, x_a⟩ = ψρ_b. For k′ ∈ C_a ∖ a, ⟨x_{k′}, x_a⟩ = ρ_a and ⟨x_{k′}, x_b⟩ = ψρ_a.
- Δ({a,b}) = 0, Δ({a}) = β²ψ²(1−ψ²) =: R, and Δ(∅) = Δ({b}) = β²(1−ψ²). The value Δ({b}) holds because ⟨μ_u, x_b⟩ = β(ψ − ψ) = 0.
- **Reduction from adding l to the state {a}**, i.e. ⟨r_l, r_μ⟩²/‖r_l‖² with residuals taken on x_a. Here r_μ = −βψ(x_b − ψx_a).
  - For k′ ∈ C_a ∖ a: ⟨x_{k′} − ρ_a x_a, x_b − ψx_a⟩ = ψρ_a − ψρ_a − ρ_aψ + ρ_aψ = 0, so the reduction is 0.
  - For k ∈ C_b ∖ b: the inner product is ρ_b − ψ²ρ_b, and ‖r_k‖² = 1 − ψ²ρ_b². So the reduction is Rκ, with κ := ρ_b²(1−ψ²)/(1−ψ²ρ_b²). Here κ < 1 because ρ_b < 1.
  - Every l outside the pair unit gives reduction 0. At the state {a,b} the residual of μ_u is 0, so every addition gives reduction 0.
- **Deletion increases.**
  - At {a,b}: deleting b increases Δ by R; deleting a increases it by β²(1−ψ²).
  - At {a}: deleting a increases Δ by β²(1−ψ²)².
  - Visible unit {h}: deleting h increases Δ by θ_h².

**Proposition LH-LAT.** On LH (exact Gram), POP-LAT(S°, m₀) holds with the fixed margin

  m₀ := min{ (1 − κ_max)·R_min,  min_i β_i²(1−ψ_i²)²,  min_h θ_h² } > 0,

where R_i = β_i²ψ_i²(1−ψ_i²), κ_i = ρ_{b_i}²(1−ψ_i²)/(1−ψ_i²ρ_{b_i}²), κ_max = max_i κ_i and R_min = min_i R_i.

*Proof.* Take S ∈ Lat(S°) with Φ(S) ≥ 2. S contains every a_i and every visible hub, a subset of M, and no extras.
- **The chosen progress neighbour.** Let I be the set of pairs whose b-hub is missing, so |I| ≥ 2. Choose i* ∈ argmax_{i∈I} R_i and A_S := S + b_{i*}, a progress neighbour. Then Δ(A_S) = Δ(S) − R_{i*}.

Now go through every B ∈ 𝒩(S) ∪ {S}:
- **B = S.** Δ(B) − Δ(A_S) = R_{i*} ≥ R_min.
- **B = S + l, l ∉ S₀** (a null, a look-alike, or a non-hub of a pair unit). Δ(B) = Δ(S) − red(l), with red(l) = R_iκ_i if l ∈ C_{b_i} ∖ b_i and i ∈ I, and red(l) = 0 otherwise. So Δ(B) − Δ(A_S) ≥ R_{i*} − max_{i∈I}R_iκ_i ≥ (1−κ_max)R_{i*}.
- **B = S − t, t ∈ S.** Δ is monotone under inclusion, so Δ(B) ≥ Δ(S) and the margin is ≥ R_{i*}.
- **B = S − t + l, l ∉ S₀.** Since S − t + l ⊆ S + l, Δ(B) ≥ Δ(S + l), and the previous case applies.
- **B = S − t + b_i, i ∈ I** (a truth-for-truth swap, which is neutral). Δ(B) − Δ(A_S) = [Δ(S + b_i − t) − Δ(S + b_i)] + (R_{i*} − R_i). The second bracket is ≥ 0. The first is the deletion increase of t at its unit's state in S + b_i, which is one of R_k, β_k²(1−ψ_k²), β_k²(1−ψ_k²)² or θ_h². All of these are ≥ m₀.

These are all the flip and swap neighbours, since S has no extras. ∎

**Corollary b1-LH.** On LH (exact Gram), with g ≤ B_n < 2g eventually and LS0 used:

  P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, and liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) ≥ 1 − limsup P(U).

*Proof.* Check the hypotheses of Theorem b1:
- **(M1).** By [W1-EXP Thm 5(a)], 1 − π₀(S°) = O_P(2^B n^{−1/2}), which tends to 0. This uses Lemma 4.2 (blocks = groups) and Theorem 6.
- **(M2).** Proposition LH-LAT, with m_n = m₀.
- **(M3).** λ_min(Σ) ≥ (1 − max_i|ψ_i|)(1−ρ₊) [W1-EXP Lemma 4.1(a)], plus interlacing; ‖μ‖²/n ≤ θᵀΣθ.
- **(P).** By [W1-EXP Thm 5(d)], which applies locked T03 with SE from Lemma 4.1(a) and BM-∞ from the fixed coefficients.
- **The rest.** d = 0 and φ̄ = c. ∎

**Masking on LH** (why this is case (b), not case (a)).
- By [W1-EXP Thm 5(b)], π₀(S₀) = p^{−c} n^{−c/2} e^{O_P(1)}.
- Q_f ≤ 4N₁(T₁ + L + 5) with N₁ = 4N₀ = 4n (for n ≥ 2500, since p < n) and T₁ = 4max(1000, ℓ²). So Q_f = O(n log² n).
- Hence Q_f π₀(S₀) = O_P(n^{1−c/2} p^{−c} log² n). This tends to 0 if c ≥ 2 and p → ∞, or if c = 1 and p/(√n log²n) → ∞.
- In those cases the exact T11(iii) identity P(S₀ ∉ final draws ∣ 𝓒) = (1 − π₀(S₀))^{Q_f} tends to 1: the iid route fails.
- VIS fails at S₀ [W1-EXP Thm 5(c)], so (F1)–(F3) fail too. The two regimes are never combined on one sequence.

**Scope and boundaries of b1-LH.**
- **p < n.** Corollary b1-LH as proved here needs p ≤ n − 1. During this run W3-PXN pushed a REPORT (branch `theory/W3-PXN`, commit 30011cf). It claims the p ≫ n analogue on LH-iid, PROVED as a single unverified run: the partition, the SE family, 1 − π₀(S°) = O_P(√(log n/n)) via exact Beta laws, S̃₀ = S°, the TD′ lattice condition at S° (P6), and π(S₀) → 1. Its P6 uses a margin table of the same kind as Proposition LH-LAT, but it was obtained independently. I have not checked W3-PXN line by line. Until a verifier does, the p ≫ n instance is a candidate input, not part of the theorem.
- **The ψ < ρ cliff.** At ψ ≥ ρ the hubs pair up into one block, π₀(S°) → 0 exponentially [W3-VEXP row 17], and (M1) fails.
- **The study's B = 14 with g = 5.** Packing then merges two groups. If a linked pair is packed together, the masking disappears.

### 3.5 Numerical check (`scripts/lh_ls0_check.py`, seed 20261102; output `scripts/lh_ls0_check.txt`)

**Design.**
- LH exact Gram: G = 12 groups of g = 9, so p = 108, with ρ = 0.7 and ψ = 0.5.
- c ∈ {1, 2, 3} linked pairs with β = (1.4, −1.0, 1.2), plus one visible hub with θ = 1.
- n ∈ {200, 800, 3200}, 10 replicates per cell.
- Blocks are taken to be the groups, as W1-EXP Lemma 4.2 gives. The partition algorithm itself was not rerun.
- π₀ is computed exactly by convolution, and the mode by max-plus.
- The production local search is used, with ℓ = ⌈log₂(n+p+1)⌉.

| c | n | S̃₀ = S° | median π₀(S°) | LS0 scores S₀ | moves | D_S on Lat(S°), all states | min lattice margin (nats) | S₀ best among scored |
|---|---|---|---|---|---|---|---|---|
| 1 | 200 | 10/10 | 0.88 | 10/10 | 1–2 | 10/10 | 11.3 | 8/10 |
| 1 | 800 | 10/10 | 0.94 | 10/10 | 1–2 | 10/10 | 58.4 | 9/10 |
| 1 | 3200 | 10/10 | 0.97 | 10/10 | 1 | 10/10 | 266.1 | 10/10 |
| 2 | 200 | 10/10 | 0.84 | 10/10 | 2 | 9/10 | −1.1 | 9/10 |
| 2 | 800 | 10/10 | 0.92 | 10/10 | 2 | 10/10 | 23.9 | 10/10 |
| 2 | 3200 | 10/10 | 0.96 | 10/10 | 2 | 10/10 | 133.6 | 10/10 |
| 3 | 200 | 10/10 | 0.79 | 10/10 | 3 | 9/10 | −2.9 | 9/10 |
| 3 | 800 | 10/10 | 0.90 | 10/10 | 3 | 10/10 | 29.5 | 10/10 |
| 3 | 3200 | 10/10 | 0.95 | 10/10 | 3 | 10/10 | 135.4 | 10/10 |

**Reading the table.**
- The minimal margin grows roughly linearly in n, as the population margin m₀n/(2C_R) of Lemma M predicts.
- The "D_S on Lat(S°)" column checks *every* Φ ≥ 1 state, which is stronger than Lemma LS-score needs. Its one failure per cell at n = 200 still left LS0 scoring S₀.
- "S₀ best among scored" < 10/10 at small n means a posterior miss among the scored set (π(S₀) ≤ ½ there). This is the statistical half, which T38 does not claim to fix.
- These numbers confirm finite-n behaviour only. They are not evidence for p ≫ n.

**Interim external evidence (not reviewed; W3-PXN is still running).** W3-PXN's `results/study_ls0.jsonl` (branch `theory/W3-PXN`, commit dfc18b6) reports LS0 from the exact start mode on regenerated study designs at n = 200, p ∈ {500, 1000}, S1 and S3. S₀ was scored in 48/49 fits, from start distances 5–14. These are recorded as interim data only.

---

## 4. Part (b1′): the D2 route (no method change)

### 4.1 Theorem D2 with the repairs. Status: PROVED (VERIFIED after the repair)

**Statement** [W1-T38E §4], with W3-VT38E §3.1 applied. Assume EX-A, EX-S and SR, and:
- (D2-a) x° Δ S₀ = {j}; if x° = S₀ ∖ {j}, then s₀ ≤ K;
- (D2-b) π₀(x°) ≥ b > 1/10;
- (D2-c) a data-measurable 𝒟 ⊆ [p] ∖ {j} with |𝒟| ≤ k_D, and Dep := Σ_{l∉𝒟∪{j}} max{κ₀(x°,l), κ₁(x°,l)};
- **(D2-d′)** NB′ := {S₀ is among the initial pilot draws} ∪ {the ESS of e^{d(X_i)/T_e} over the H initial draws is ≥ 0.9H}.

Then, for every t ∈ (0, b − 1/10), with β := (1−Dep)₊/(k_D + B + 3) and g(f) = f − √(f(1−f))/3,

  P(S₀ ∉ 𝒮_cal ∣ data) ≤ e^{−2Ht²} + P(NB′ᶜ ∣ data) + exp{−H β g(b − t)},   H = H₀ ≥ 0.2 max(n, p).

**Proof.**
- Steps 1 and 3–6 of [W1-T38E §4] are used verbatim:
  - Hoeffding for the initial fraction;
  - the share bound from Lemma S with e = 0.9;
  - the binomial resampling;
  - one round from x°, using Lemma A off 𝒟 and SR;
  - independence across particles.
- Step 2 is replaced by W3-VT38E §3.1:
  - by Lemma S(i), the ESS is non-increasing in φ;
  - `pilot_next_phi` accepts φ′ = 1 if it passes, keeps a passing lower end in bisection, and forces φ₁ = 1/T_e otherwise;
  - φ₁ = 1/T_e passes on NB′.
- W1's sufficient condition, "range of d ≤ T_e log 1.925", must read log r* with r* = (11 + 2√10)/9 ≈ 1.92495. At r = 1.925, 4r/(1+r)² = 0.8999927 < 0.9. ∎

**Corollary D2-∞.** Suppose, along R1, that b is fixed, k_D and B are bounded, Dep ≤ 1 − c₁ with probability → 1, and P(NB′ᶜ) → 0. Then P(S₀ ∉ 𝒮_cal) → 0. Since 𝒮_cal ⊆ 𝒮̄ on 𝒪̄ (the calibration precedes the final run, and GUARD), D_n → 0.

**Reporting repair** [W3-VT38E §3.3]. In CF(1), the full bound (optimised over t) is 2.2·10⁻⁷ at n = 400 and 1.6·10⁻⁵ at n = 1600, plus P(NB′ᶜ). Those CF(1) instances are **not masked**: iid discovery succeeds there. So they illustrate the mechanism, not route (b1′)'s added value.

### 4.2 D2's statistical instance on LH with c = 1 (new). Status: PROOF SKETCH

Take x° = S° = S₀ ∖ {b}, with j = b and 𝒟 := C_b ∖ {b} (the g − 1 ≤ 15 look-alikes of the masked hub). Exact Gram; p/(√n log²n) → ∞, which is the range where LH with c = 1 is masked (§3.4).

1. **(D2-b).** π₀(S°) → 1 [W1-EXP Thm 5(a)]. PROVED.
2. **Dep → 0.** The labels split into three groups.
   - (i) **Truth deletions** (s₀ − 1 labels). At φ = 0 the start-law odds are e^{−Θ(n)} by VIS-lin(S°); at φ = 1 they are e^{−Θ(n)} by Lemma M (the deletion margins of §3.4).
   - (ii) **Additions of l ∉ C_b at φ = 0.** Exact zero leakage in l's block (ZL(S°)) gives κ₀(S°, l) ≤ C p⁻¹ n^{−1/2} e^{Z_l²/2}·e^{O(1)} on the EXP′ event, where Z_l is N(0,1) and Z_l² ≤ L log n.
   - (iii) **Additions of l ∉ C_b at φ = 1.** §3.4 gives δ_{S°,l} = 0 for every l ∉ C_b, including C_a ∖ a. So κ₁ satisfies the same bound, with the residual variance σ² + R in place of σ².
   - **Summing.** Σ_l e^{Z_l²/2} 1{Z_l² ≤ L log n} has expectation ≤ p·2√(L log n)/√(2π) whatever the dependence (by linearity; the same computation as in [W2-PREM Prop. NL0]). So Dep = O_P(√(log n/n)).
   - What is not written: the uniform BF expansion at φ = 1 for sets of size s₀. That is Lemma U of W2-PREM, which is unverified; or one can extend Lemma M to two-sided bounds.
3. **NB′.** The initial draws are iid π₀, and each equals S° with probability 1 − O_P(2^B n^{−1/2}).
   - A draw containing a look-alike k ∈ C_b ∖ b has d higher by Θ(n). It occurs with probability ≍ g/(2p√n) per draw, so the expected count among H ≈ 0.2 max(n,p) draws is ≍ g√n/(10p), which tends to 0.
   - Draws that delete a truth have π₀-odds e^{−Θ(n)}.
   - The remaining non-S° draws (null additions) change d by O(Z²) = O(log n) (§3.4: x_l is orthogonal to S° and δ = 0 both globally and in its block). Their share of the draws tends to 0, and their weights e^{O(log n)/T_e} keep the ESS ≥ 0.9H. For n + p ≥ 2^{32}, T_e ≥ ℓ² ≍ log² n.
   - The crux, not written: a uniform bound on d over the non-S° draws, which is a two-sided version of the EXP′ expansion for global versus block Bayes factors.
4. **Conclusion (sketch).** Corollary D2-∞ applies. W3-PXN (P7, unverified) independently claims D2-a, D2-b and D2-c as PROVED on LH-iid with c = 1, with Dep = O_P(√(log n/n)); its NB is a PROOF SKETCH with the same crux as step 3 here. This would give masked-regime consistency on LH with c = 1 **without a method change**, but only for c = 1 and p ≫ √n log² n. Masking there is weak at practical n: Q_fπ₀(S₀) ≍ 64000·√n/p.

---

## 5. Part (b2): the Gibbs-path route (no method change)

### 5.1 The bound. Status: PROVED-UNDER (DELIV, REP)

**The terminal segment.** On 𝒪̄ ∩ SMC, consider the final run of R̄ and the σ-field 𝔉_T up to the end of the stage-T resampling [W2-PREM Thm IND-T]. The terminal segment after the last resampling has H′ = L + 5 rounds at φ = 1:
- the stage-T round at φ_T = 1;
- L burn-in rounds;
- 4 measured rounds.

There is no reweighting and no resampling in it ([W2-BOOK §4] code reading; [W2-VT24G §8]).

**Claim.** Let 𝔛_n be data-measurable, let N_𝔛 be the number of final-run particles in 𝔛_n at time 𝔉_T, and let β_H(x) = P(Bin(H, c′_*(x)) < v(x)) + Hη(x) [W1-T24G Thm B with W2-VT24G Thm B′]. Then

  P(𝒪̄ ∩ SMC ∩ {S₀ ∉ 𝒮̄} ∣ data) ≤ P(𝒪̄ ∩ SMC ∩ {N_𝔛 = 0} ∣ data) + E[ ∏_{i: X_i∈𝔛_n} min{1, β_{L+5}(X_i)} ∣ data ].   (5.1)

*Proof.*
1. By IND-T (EX-S, EX-A), conditionally on 𝔉_T the N terminal trajectories are independent Markov chains with the one-round kernel K̄₁, started at the 𝔉_T-measurable states X_i. The 4 islands use separate streams.
2. Theorem B′ bounds, for each i, the probability that trajectory i does not score S₀ within H′ rounds by min{1, β_{L+5}(X_i)}. Lemma F′ handles the closure issue of W1's Lemma F.
3. Independence turns these bounds into the product.
4. On {N_𝔛 = 0} we use the trivial bound 1. Then take expectations given the data. ∎

**Consequence.**
- Under (DELIV), P(𝒪̄ ∩ SMC ∩ {N_𝔛 = 0}) → 0.
- Under (REP), sup_{x∈𝔛_n} β_{L+5}(x) → 0 in P₀-probability, and the product is ≤ min{1, sup β}.
- So D_n → 0 by bounded convergence.
- A weaker sufficient condition is the multi-particle form [W1-T24G Cor. B-M]: E[∏ min{1, β}] → 0, for example N_𝔛 → ∞ with β ≤ 1 − c on 𝔛_n.
- A one-round, distance-one form [Cor. P1] replaces β by 1 − a₁(x). ∎

**Repairs incorporated.**
- **W2-VT24G Lemma F′.** It is used in Theorem B, part (a), and in the Prop. B2 slot step.
- **Props. B1′/B2′.** At |P| = 1 no deletability premise is needed: c′₂ ≥ 1/(B+3). At x = S₀ ∖ {j}, c′₁ = 1.
- **H = L+5, not L+4** [W2-PREM, W2-VT24G].
- **(R5) is now IND-T.** The particles share one stream, read sequentially; this is still fine by the stopping-time shift lemma.
- **H24 is retired.** Its asymptotic input (L+4)η_n → 0 is false in correlated designs (CE1, Lemma E). T38 never uses H24.

### 5.2 What is open in (b2)

- **DELIV** is OPEN (g4).
  - [W1-T38E Prop. D3] gives P(no 𝓡_d particle after stage T) ≤ (1−π₀(𝓡_d))^N + Σ_t(ζ_t + η_t), under SHARE(ζ) and EXIT-end(η). This is PROVED, conditional on those two inputs.
  - SHARE is close to the conclusion itself [W3-VT38E §5.2].
  - COUNTEREXAMPLE C1, with a reversible kernel: π₀(A) ≈ 1, bridge mass on A ≥ 0.9997 and zero exits from A, yet A is extinct in 56% of islands at N = 10⁵ and in 100% at N = 10⁶. So DELIV cannot come from start mass, bridge mass and exit control alone.
  - The T15 route (D1) needs the islandwise lower tail LT, which fails exactly when particles cross late.
  - W4-SHARE had not been pushed when this run started.
- **REP** is partial (g5).
  - Phase 2 (supersets): truth deletion is PROVED under BM-∞. NL0(a) and UDEL(a ≥ 2) are PROVED UNDER the partner-graph condition PG [W2-PREM §3]; this is unverified, and W2-PREM has no REPORT. COUNTEREXAMPLE: equicorrelated nulls with rβ > ½ break NL0(1) and UDEL(2). The NL0 threshold correction of [W2-VT24G §4] applies.
  - Phase 1 (incomplete starts): the final W2-PREM REPORT (pushed during this run, unverified) shows that BTP is unnecessary (Prop. B1′). It proves TS, TL♯, ULR and IND-M UNDER named conditions. It finds that W1-T24G's repair family is defective on LH (COUNTEREXAMPLE: useless look-alikes make η₁ of order one), and replaces it by Theorem B♯. On LH it discharges every premise (Theorem L, PROOF SKETCH). Under cancellation, TS fails without its coefficient condition. With this, REP on LH is a PROOF SKETCH, and DELIV is the only fully open input of (b2) there.
  - Structurally, v(x) > H makes the bound vacuous [W2-VT24G §5]. So 𝔛_n must have bounded potential.

---

## 6. Part (c): cost. Status: PROVED-UNDER T32(i) (CONJECTURE)

**The ceiling.** On the SMC branch, the number of score evaluations is at most

  Σ_b 2^{|C_b|} + Σ_{e=0}^{1}(1+4ℓ)H_e[1 + 2m(T_e+L+4)] + 4N₁[1 + 2m(T₁+L+4)] + (8ℓ+3)(ℓ+1)[p + k_*(p−k_*)],

with m = p + B + 2. This is T32(i). W3-VT38E checked it against the engine as a valid but loose upper bound: the engine does ≤ m rather than 2m scores per round, and ≤ 2ℓ+3 rather than 8ℓ+3 searches.

**LS0 adds** at most (ℓ+1)·max_{k≤K}[p + k(p−k)] scores [W1-T38E E3].

**Order of growth.** Use Σ_b 2^{|C_b|} ≤ p2^B/B ≤ 2^{16}p, N_e ≤ 4max(2500, n, p), T_e ≤ 4max(1000, ℓ²), L = O(log n), ℓ = O(log(n+p)), and max_k k(p−k) ≤ p²/4. The total is

  O((n+p)(p+B)log²(n+p) + p² log²(n+p)),

which is polynomial in n under R1. The exact branch scores Σ_{k≤K}C(p,k) ≤ (5H₀ + 4N₀)p models by its definition.

**Corrections carried** [W1-T38E]:
- the brief's O(NT(p+B+2) + ℓp) omits the k(p−k) swaps per scan and the O(ℓ²) local searches;
- this is a deterministic ceiling, not an expectation.

---

## 7. Assembly: proof of Theorem 5

- By §1, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀δ₁ + D_n, and E₀δ₁ → 0 under (P).
- D_n → 0:
  - in case (a) by §2.1;
  - in case (b1) by Theorem b1 (§3.3);
  - in case (b1′) by Corollary D2-∞ (§4.1);
  - in case (b2) by §5.1.
- The liminf and o(1) forms follow as in §1.
- Case (b1-LH) is Corollary b1-LH (§3.4).
- Part (c) is §6. ∎

---

## 8. Repairs and corrections incorporated (by source)

| Source | Repair | Where it enters |
|---|---|---|
| W1-T38E | brief's limit form → liminf; now also the stronger o(1) form | §1 |
| W1-T38E | the cost formula counts the k(p−k) swaps and O(ℓ²) searches | §6 |
| W1-T38E | "ℓ_n < s₀ + d" → the path length matters (here ℓ ≥ Φ(S°) − 1) | §3.1 |
| W1-T38E | T27-H3 already implies start mass on 𝓡₀ | §3.4 (M1 via Thm 5(a)) |
| W3-VT38E §3.1 | D2: r* = (11+2√10)/9; NB → NB′ | §4.1 |
| W3-VT38E §3.2 | C1 with a reversible kernel (conclusion unchanged) | §5.2 |
| W3-VT38E §3.3 | D2 numbers: full three-term bound; CF(1) not masked; tier caveat for CF(2) | §4.1 |
| W3-VT38E §3.4 / W1-T37R Prop 1 | TD(d,0) false for d ≥ 1 → T38 uses D_S on a lattice, never TD(d,0) | §3 |
| W3-VT38E §3.5 | GP(d) ⇒ TD′ (subsumed by Lemma LS-score) | §3.1 |
| W3-VT38E §4 | LS0 must emit its centre; fix the argmax π₀ tie rule | OP-LS0; STATEMENT II.8 |
| W3-VT37R R1 | A5 gains POS (TD(d,0) strict ∧ POS ⇒ TD′_P) | not load-bearing: §3 uses Thm A only through the lattice form |
| W3-VT37R R2 | Lemma 0(b): posterior miss ⇏ E_LSᶜ | STATEMENT Remark 3 |
| W3-VT37R R3 | "ℓ ≥ a+d needed" → "suffices"; the exact need is ℓ ≥ τ | §3.1 (scoring: ℓ ≥ Φ − 1) |
| W3-VT37R R4, R5 | Thm C repaired at PROOF SKETCH (LD*, the union-model noise bound) | §3.3, alternative for (M2) |
| W3-VT37R R6 | 2^Φ states only for data-independent centres | §3.3: S° is deterministic |
| W2-VT24G | Lemma F′; B1′/B2′; CE1 wording ("H24's asymptotic input fails"); NL0 threshold | §5 |
| W2-PREM / W2-VT24G | IND-T replaces (R5); H′ = L + 5 | §5.1 |
| W2-BOOK | run/output split (Lemma RO, GUARD); never condition on completion; (e′) replaces H24 | §1, §0.2 |
| W3-VEXP R1 | finite-n EXP′ certificate (κ_EXP is vacuous at study SNR) | §2.2 |
| W3-VEXP R2 | Thm 2 is a verbatim corollary of locked T22(iii) | §2.2 |
| W3-VEXP R3 | LH-iid start law (PROOF SKETCH) | §3.4 scope |
| W3-VEXP row 17 | the \|ψ\| < ρ boundary is sharp in effect | §3.4 scope |
| W3-VEXP Prop. D | study-size masking is dilution | §2.3, STATEMENT Remark 4 |
| W3-VEXP §8 | 𝓡_d contains ∅ → use Lat(S°) with Φ(S°) bounded | §3 |
| W2-VT03R R1, R2 | proof thresholds near n ≈ 2×10⁶; meaning of the anchored SE | §1 |
