# T38: full proof — corrected after A-REV1 (supersedes W4-T38FULL/T38_PROOF.md)

Run W6-FIXREV1, 2026-11-02. This is a **candidate**, not reviewed after these edits and not adopted. The statement and
the dependency map are in `T38_STATEMENT.md`; its Part 0 is the change log. Other corrected ingredients are in
`CONSOLIDATED.md` ([CON]). The cross-family review is A-REV1 ([AR]).

**What is new here and what is copied.**
- §0, §1, §4, §5, §6 and §7 are rewritten.
- §2 (part (a)) and §3 (Lemma LS-score, Lemma M, Theorem b1, Proposition LH-LAT, Corollary b1-LH, and the numerical
  check) are copied from W4-T38FULL with the edits marked **[W6]**. I re-checked Lemma M and Lemma LS-score line by
  line in this run (REPORT §5). A-REV1 did not review them.
- Notation: 00_COMMON. Φ(S) = |S Δ S₀|, Δ(T) = ‖(I − P_T)μ‖²/(n−1), Lat(·) as in T38_STATEMENT, K = min(p, ⌊n/2⌋).

---

## 0. Conventions

**(0.1) The production local search** (METHODOLOGY_v3 §6.10; engine `local_search` in
`Scripts/SMC_BVS/core/cpp/v3_engine.h`).
- Given a centre C and a move counter t = 0, the search repeats two steps:
  1. **Scan.** Score every feasible flip of C (additions only if |C| < K) and every swap.
  2. **Move or stop.** Let T* be the best scanned neighbour, with exact ties broken lexicographically. If F(T*) > F(C)
     and t < ℓ, set C ← T*, t ← t + 1, and go back to step 1. Otherwise stop.
- A scan always precedes the move-limit test.
- The centre is scored only if `emit_centre` is true. **LS0 sets it** (T38_STATEMENT, Objects).
- Production callers pass false, because their centre is already scored.
- Every scanned model enters the scored set.

**(0.2) Runs, statuses, outputs** (W2-BOOK §0).
- R̄ is the potential uninterrupted run under EX-A. Its status is st̄ ∈ {exact, completed, schedule_limit}, and
  `numerical_failure` cannot occur under EX-A.
- On the SMC branch, {st̄ = completed} = 𝒜 (the final run is launched, and in R̄ it executes all its rounds and the final
  local search). Also {st̄ = schedule_limit} = 𝒜ᶜ, where no final run is launched and the scored set is 𝒮_cal (pilot,
  calibration, diagnostic islands and their local searches).
- On the exact branch, every model of Ω is scored.
- R̄⁺ is R̄ followed by LS0, which is a deterministic function of the data.
- **GUARD.** (G1) The guard consumes no randomness and changes no setting. (G2) A run that no check stops performs the
  R̄ (R̄⁺) computation. Hence on 𝒢ᶜ, st = st̄ and every reported output equals its R̄⁺ version. This is Lemma RO(1)
  (W2-BOOK §0.2), with 𝒪 = 𝒢ᶜ ∩ 𝒪̄ and 𝒪_H = 𝒢ᶜ ∩ 𝒪̄_H.
- Under OP-LS0, LS0 runs to completion on every fit counted as output, so on those fits 𝒮⁺ = 𝒮̄⁺. A stopped LS0
  is in 𝒢 ⊆ U.

**(0.3) Probability.** P is the joint law of the data and the algorithm, and P₀ is the law of the data. Bounds are
P₀-probabilities, or expectations of conditional probabilities given the data or given a boundary σ-field, combined by
the tower property. "→ 0 in P₀-probability" becomes "→ 0 in expectation" for [0,1]-valued quantities by bounded
convergence. **No event is ever placed behind a conditioning bar unless it is measurable with respect to the past at
that point.** In particular, nothing is conditioned on completion, diagnostics or later success.

---

## 1. Part (0): the composition

### 1.1 Strict convention

**Claim. PROVED.** For every n, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[δ₁] + D_n, where D_n := P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}).

*Proof.*
1. By (0.2), 𝒪 = 𝒢ᶜ ∩ 𝒪̄, and on 𝒪 we have Ŝ⁺ = Ŝ̄⁺. So 𝒪 ∩ {Ŝ⁺ ≠ S₀} ⊆ 𝒪̄ ∩ {Ŝ̄⁺ ≠ S₀}.
2. **Direct set argument (locked T21(C1); this replaces W4's "T11(vii)" citation, [AR] §8).** On {π(S₀) > ½}, every
   S ≠ S₀ has π(S) ≤ 1 − π(S₀) < π(S₀), so F(S₀) > F(S). The method's HPM is the strict maximiser of F over *every
   model ever scored*. Under the all-scored rule (M §6.10, `Ledger::offer_hpm`), a model enters the running best when it
   is first scored, and later scoring or cache eviction cannot displace a strict global maximum. So on
   {π(S₀) > ½} ∩ {S₀ ∈ 𝒮̄⁺} the HPM over 𝒮̄⁺ is S₀, with no tie possible.
3. Hence 𝒪̄ ∩ {Ŝ̄⁺ ≠ S₀} ⊆ {δ₁ ≥ ½} ∪ (𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}). Markov gives P₀(δ₁ ≥ ½) ≤ 2E₀δ₁. ∎

**Consequences.**
- Under (P), δ₁ ∈ [0,1] → 0 in probability, so E₀δ₁ → 0 (bounded convergence).
- If D_n → 0, then P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0.
- Since P(𝒪 ∩ {Ŝ⁺ = S₀}) = P(𝒪) − P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) and P(𝒪) = 1 − P(U), we get
  P(𝒪 ∩ {Ŝ⁺ = S₀}) − (1 − P(U)) → 0.
- So liminf P(𝒪, Ŝ⁺ = S₀) = 1 − limsup P(U), and the two sides agree. If P(U) → u, the joint success probability tends
  to 1 − u.
- Nothing here bounds P(U).

**Exact branch.** On 𝒪̄ ∩ {exact} every model of Ω is scored, so S₀ ∈ 𝒮̄ whenever s₀ ≤ K. Hence

  D_n ≤ P₀(s₀ > K) + P(𝒪̄ ∩ SMC ∩ {S₀ ∉ 𝒮̄⁺}) = P₀(s₀ > K) + P(SMC ∩ 𝒜 ∩ {S₀ ∉ 𝒮̄⁺}).   (1.1)

Under R, P₀(s₀ > K) → 0, with K = min(p, ⌊n/2⌋).

### 1.2 HPM convention (usable-but-unexecuted outputs, [AR] §7.3)

**Claim. PROVED.** P(𝒪_H ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E₀[δ₁] + D_n + D_n^{sl}, where
D_n^{sl} := P(SMC ∩ 𝒜ᶜ ∩ {S₀ ∉ 𝒮_cal ∪ 𝒮_LS0}). Here 𝒮_LS0 = ∅ if LS0 is not used, or not run on schedule_limit fits.

*Proof.*
- 𝒪_H = 𝒢ᶜ ∩ 𝒪̄_H by (0.2). Steps 1–3 of §1.1 apply verbatim with 𝒪̄_H in place of 𝒪̄.
- 𝒪̄_H ∩ {S₀ ∉ 𝒮̄⁺} is the disjoint union of 𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺} and {st̄ = schedule_limit} ∩ {S₀ ∉ 𝒮̄⁺}.
- {st̄ = schedule_limit} = SMC ∩ 𝒜ᶜ, and on it 𝒮̄⁺ = 𝒮_cal ∪ 𝒮_LS0. ∎

*Reading.* If the paper counts a `schedule_limit` best-scored model as output, its discovery term must include
D_n^{sl}. Route (b1′) controls D_n^{sl} for free, since 𝒮_cal contains the pilot. So does route (b1), when LS0 is run on
those fits. Routes (a) and (b2) need the final run, and they leave D_n^{sl} ≤ P(SMC ∩ 𝒜ᶜ), which no result here controls.
`numerical_failure` cannot occur in R̄ (EX-A). In the actual run it occurs only if EX-A fails, and then GUARD's
"st = st̄ on 𝒢ᶜ" fails too. A floating-point statement needs a VAL-FP-type contract (W2-BOOK Prop. 2(f)), which is
outside this theorem.

### 1.3 Relation to A-REV1's actual-run form ([AR] §7.4)

A-REV1 writes, for actual failure M = {S₀ ∉ 𝒮⁺}, an availability event A (an eligible particle selected at an actual
terminal boundary, false if the boundary is never reached) and an execution event E (the designated H rounds execute):

  P(Uᶜ ∩ M) ≤ P(Uᶜ ∩ M ∩ Aᶜ) + P(Uᶜ ∩ M ∩ A ∩ Eᶜ) + E[1_A β_H(x)].

This is valid with the coupling "the actual run agrees with its potential continuation until any interruption". That
coupling is (G1)–(G2).

Under the strict convention, Uᶜ ∩ SMC = 𝒪 ∩ SMC ⊆ 𝒢ᶜ ∩ {st̄ = completed}. There the actual run *is* R̄, whose designated
rounds execute, so Uᶜ ∩ A ∩ Eᶜ = ∅. The middle term vanishes, and the inequality becomes §5's (5.1) read through Lemma RO.

Under any convention that counts a partially executed run as usable, for example a guard-partial HPM, the middle term
does not vanish. It must be added explicitly, and nothing here bounds it. This is why T38 uses the strict convention, or
the HPM convention with its explicit D_n^{sl}.

---

## 2. Part (a): favourable regime

*[W6] Copied from W4-T38FULL §2 without change in substance. The only edit is that K = min(p, ⌊n/2⌋) throughout.*

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

---

## 3. Part (b1): the LS0 route

*[W6] Copied from W4-T38FULL §3. Edits: E3(i) is cited as E3′(i) ([CON] §6), whose LS0 emits its centre. Route (b1) never uses E3(ii). I re-checked Lemma LS-score and Lemma M line by line (REPORT §5). A-REV1 did not review §3.*

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
1. **Eligibility.** On {π₀(S°) > ½}, S̃₀ = S°: by E3′(i) ([CON] §6; [W1-T38E E3(i)]), no other state can have π₀-mass ≥ ½, so there is no tie.
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

### 3.5 Numerical check (W4-T38FULL's `scripts/lh_ls0_check.py` on branch `theory/W4-T38FULL`, seed 20261102; output `scripts/lh_ls0_check.txt` there; not re-run in W6)

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

### 4.1 Execution: the potential first pilot stage

On the SMC branch, R̄ runs CALIBRATE(0) first (METHODOLOGY_v3 §7, pseudocode). It starts with the tier-0 pilot: H₀ iid
π₀ draws on stream 0, all scored, followed by the first reweight–resample–round stage at φ₁ chosen by `pilot_next_phi`.
In R̄ there is no preflight and no guard, and under EX-A there is no numerical failure. So **on every R̄ run of the SMC
branch, whatever its eventual status, the first pilot stage executes**, and its scores are in 𝒮_cal ⊆ 𝒮̄ ⊆ 𝒮̄⁺. The pilot
is never conditioned on its later calibration record. D2 is a bound on this potential first stage, conditional on the
data.

### 4.2 Theorem D2 (finite), unchanged

Hypotheses: EX-A, EX-S, SR; (D2-a) x° ∈ Ω with x° Δ S₀ = {j}, and if x° = S₀∖{j} then s₀ ≤ K; (D2-b) π₀(x°) ≥ b > 1/10;
(D2-c) 𝒟 ⊆ [p]∖{j} data-measurable with |𝒟| ≤ k_D, and Dep := Σ_{l∉𝒟∪{j}} max{κ₀(x°,l), κ₁(x°,l)}; (D2-d′) NB′. For
t ∈ (0, b − 1/10), with β := (1−Dep)₊/(k_D + B + 3) and g(f) = f − √(f(1−f))/3,

  P(S₀ ∉ 𝒮_cal | data) ≤ min{1, e^{−2H₀t²} + P(NB′ᶜ | data) + exp(−H₀ β g(b − t))}.

*Proof.* W1-T38E §4, steps 1 and 3–6 verbatim. Step 2 is W3-VT38E §3.1 (NB′). A-REV1 §6 VERIFIED the six steps in this
order. Lemma S′ is used only through its inequality, at e = 0.9 and f ≥ b − t > 1/10 = 1 − e. ∎

### 4.3 Route (b1′) conclusion. PROVED (implication)

**Claim.** Under T38_STATEMENT route (b1′) (fixed margins or general rates), D_n + D_n^{sl} → 0.

*Proof.* By §4.1 and (1.1),

  D_n + D_n^{sl} ≤ P₀(s₀ > K) + P(SMC ∩ {S₀ ∉ 𝒮_cal}) ≤ P₀(s₀ > K) + E₀[ P(S₀ ∉ 𝒮_cal | data) ].

For the fixed-margin case, let 𝔈_n := {π₀(x°_n) ≥ b₀, |𝒟_n| ≤ k_D, Dep_n ≤ 1 − c₀}, t := (b₀ − 1/10)/2 and
β₀ := c₀/(k_D + 19) (B ≤ 16). On 𝔈_n, §4.2 with b = b₀ gives
P(S₀ ∉ 𝒮_cal | data) ≤ e^{−2H₀t²} + P(NB′ᶜ | data) + exp(−H₀β₀ g(b₀ − t)). Hence

  E₀[P(S₀ ∉ 𝒮_cal | data)] ≤ P₀(𝔈_nᶜ) + e^{−2H₀t²} + P(NB′ᶜ) + exp(−H₀β₀ g(b₀ − t)) → 0,

because H₀ = ⌈512N₀/2500⌉ ≥ 0.2048·max(n, p) → ∞ and g(b₀ − t) > 0 is fixed. The general-rate case is the same with
min{1, ·} and bounded convergence ([CON] §5). ∎

*Why the rate premises are needed ([AR] §7.1).* "D2's hypotheses w.p. → 1" at each n does not suffice. Finite D2 allows
Dep ≥ 1, which gives β = 0. A pointwise b_n > 1/10 can have b_n − 1/10 → 0 too fast for Hoeffding. And β_n → 0 can
outrun H₀.

### 4.4 Statistical instance on LH with c = 1. Status: PROOF SKETCH (unchanged from W4-T38FULL §4.2)

Take x° = S° = S₀∖{b}, j = b, 𝒟 = C_b∖{b} (so k_D = g − 1 ≤ 15).
- **Fixed margins.** π₀(S°) → 1 (W1-EXP Thm 5(a), PROVED) gives b₀ = 0.9 w.p. → 1. Dep = O_P(√(log n/n)) (sketch,
  W4-T38FULL §4.2 step 2) gives c₀ = ½ w.p. → 1.
- **The unfinished step** is NB′: a uniform two-sided bound on d over the non-S° pilot draws. W3-PXN P7 (unverified)
  claims D2-a, b, c on LH-iid with c = 1, and also leaves NB at PROOF SKETCH.

So route (b1′) is PROVED as an implication, and its masked instance is a PROOF SKETCH.

---

## 5. Part (b2): the Gibbs-path route (no method change)

### 5.1 The bound. Status: PROVED (implication; uses IND-T, PROVED under EX-S, EX-A)

**Setting.** Work on SMC ∩ 𝒜 in R̄. For island r, 𝔉_T^{(r)} is the σ-field of the data, 𝓒 and stream 9 + r up to the
end of the stage-T resampling. Let 𝔉 := ∨_r 𝔉_T^{(r)}. The four streams are independent iid sequences given (data, 𝓒)
(EX-S). After its boundary each island runs H′ = L + 5 rounds at φ = 1 (stage-T round, L burn-in, 4 measured) with no
reweighting or resampling (W2-BOOK §4; W2-PREM §1.1). In R̄ these rounds execute. Let 𝔛_n be as in T38_STATEMENT (b2),
let E := {(r,i) : X_{r,i} ∈ 𝔛_n}, which is 𝔉-measurable, and N_𝔛 := |E|.

**IND-T** (W2-PREM §1; A-REV1: VERIFIED for the uninterrupted process). Given 𝔉:
- (a) the extended trajectories of distinct particles over the H′ rounds are independent, including across islands;
- (b) each is a Markov chain from X_{r,i} with the extended round kernel K̄₁, whose output includes every model scored in
  the round.

The Lemma S of W2-PREM §1.2 (shift at a stopping time) is applied per stream. The islands' streams are independent.

**Claim.**

  P(SMC ∩ 𝒜 ∩ {S₀ ∉ 𝒮̄} | data) ≤ P(SMC ∩ 𝒜 ∩ {N_𝔛 = 0} | data) + E[ 1_𝒜 1{N_𝔛 ≥ 1} Π_E | data ],   (5.1)

where Π_E may be taken as either:
- (single) min_{(r,i)∈E} β_{H′}(X_{r,i}), which uses only IND-T(b); or
- (product) ∏_{(r,i)∈E} β_{H′}(X_{r,i}), which uses IND-T(a) and (b).

*Proof.*
1. On {N_𝔛 = 0}, use the bound 1.
2. On 𝒜 ∩ {N_𝔛 ≥ 1}, let ι be the element of E minimising β_{H′}(X_{r,i}), with ties broken by lexicographic index. ι
   is 𝔉-measurable, because β_{H′} is a data function evaluated at 𝔉-measurable states.
3. If X_ι = S₀, then S₀ is a visited particle state (an initial draw or an end-of-round state before 𝔉), so it is
   already scored. The event {S₀ ∉ 𝒮̄} is then empty, consistent with β_{H′}(S₀) = 0.
4. Otherwise {S₀ ∉ 𝒮̄} ⊆ {trajectory ι scores no S₀ in its H′ rounds}. By IND-T(b) the conditional probability given 𝔉 is
   P_x(S₀ not scored within H′ rounds) evaluated at x = X_ι.
5. By Theorem B with x's certificate ([CON] §2), that probability is ≤ β_{H′}(X_ι).
6. For the product form, {S₀ ∉ 𝒮̄} ⊆ ⋂_{(r,i)∈E} {trajectory (r,i) scores no S₀}, and IND-T(a) factorises the conditional
   probability.
7. Take conditional expectations given the data. ∎

**Consequence.** By (1.1) and (5.1),

  D_n ≤ P₀(s₀ > K) + P(SMC ∩ 𝒜 ∩ {N_𝔛 = 0}) + E[1_𝒜 1{N_𝔛 ≥ 1} Π_E].

The second term vanishes under DELIV(𝔛_n), and the third under REP(𝔛_n). If sup_{x∈𝔛_n} β_{L+5}(x) → 0 in
P₀-probability, then Π_E ≤ that sup, and the third term vanishes by bounded convergence. A product bound uniformly
below 1 plus N_𝔛 → ∞ also suffices, but that is a delivery statement. ∎

**What the interface requires ([AR] §7.2).**
1. Each x ∈ 𝔛_n∖{S₀} must satisfy the hypotheses of the theorem whose β is used:
   - a family 𝓕(x) or 𝓕♯(x) fixed by data-measurable choices;
   - s₀ + a(x) ≤ K;
   - the conventions of [CON] §2.

   Membership in 𝓡_d alone gives none of this. The symmetric-union neighbour graph does not bound |A(x)| by B.
2. Selection uses only 𝔉. Selecting particles by later success, diagnostics or fresh-score counts is excluded.
3. The boundary and H must match. Either (𝔉_T, H′ = L + 5), or the boundary after the stage-T round with H = L + 4. Never
   mix them.
4. Sufficient statistical inputs, on events of P₀-probability → 1:
   - sup_{𝔛_n} v ≤ v̄;
   - inf_{𝔛_n} c_* ≥ c > 0;
   - (L+5)·sup_{𝔛_n} η → 0.

   With the η-premises in sum-over-labels-of-sups form ([CON] §8), β_{L+5} ≤ v̄(1−c)^{⌊(L+5)/v̄⌋} + o_P(1) → 0. W2-PREM
   Corollary A gives these under named design conditions, and Theorem L (PROOF SKETCH) on LH.
5. v(x) > H′ makes β trivial (W2-VT24G §5), so 𝔛_n must have bounded potential.

### 5.2 DELIV(𝔛_n): what is available. Status: implication PROVED; inputs OPEN

**Proposition D3(𝔛). PROVED (W1-T38E D3, with 𝓡_d replaced by 𝔛_n; same proof).** Fix one final island with
N = N_e particles. Let A_t := {some particle in 𝔛_n after the stage-t round}, and A₀ := {some initial draw in 𝔛_n}.
Assume:
- (SHARE(𝔛)) P(A_{t−1} ∩ {no stage-t resampled particle in 𝔛_n}) ≤ ζ_t;
- (EXIT-end(𝔛)) sup_{x∈𝔛_n} P_x(one round at φ_t ends outside 𝔛_n) ≤ η_t^{end}.

Then P(𝒜 ∩ {no particle in 𝔛_n at 𝔉_T} | 𝓒) ≤ (1 − π₀(𝔛_n))^N + Σ_{t=1}^{T−1}(ζ_t + η_t^{end}) + ζ_T. At the
after-round boundary (H = L + 4), the bound is (1 − π₀(𝔛_n))^N + Σ_{t=1}^{T}(ζ_t + η_t^{end}).

*Proof.* As W1-T38E D3, stopping the chain at the stage-T resampling for the first form: the failure event is contained
in A₀ᶜ ∪ ⋃_{t<T}(A_{t−1} ∩ A_tᶜ) ∪ (A_{T−1} ∩ {no stage-T resampled particle in 𝔛_n}). The smallest-index resampled
particle in 𝔛_n is measurable at its resampling, and its round uses fresh randomness. ∎

DELIV needs the **aggregate** to vanish: E[(1 − π₀(𝔛_n))^{N_e}] + Σ_t(ζ_t + η_t^{end}) → 0. Listing SHARE and EXIT-end
without their aggregate rates does not discharge DELIV ([AR] §7.2). SHARE is close to the conclusion itself (W3-VT38E
§5.2). COUNTEREXAMPLE C1 (VERIFIED) shows that DELIV does not follow from start mass, bridge mass and zero exits. **DELIV
is OPEN for every BVS family.**

### 5.3 Repairs incorporated in (b2)

- Lemma F′ (W2-VT24G) in Theorem B part (a) and the B2 slot step.
- Props. B1′/B2′ (W2-VT24G).
- Prop. B1′ + PA (W2-PREM, BTP not needed).
- Theorem B♯ (W2-PREM, monotone look-alike map), because W1's 𝒵(x) is defective on LH.
- Prop. U′ ([CON] §1), with the full Bad set. Theorem B's inequality is unaffected ([CON] §1.3).
- β_H conventions and capping ([CON] §2).
- H′ = L + 5 only at 𝔉_T.
- IND-T replaces (R5).
- H24 is not used. CE1-narrow ([CON] §9).
- NL0 in the Λ₂ form ([CON] §8).

---

## 6. Part (c): cost. Status: PROVED UNDER T32(i) (CONJECTURE)

On the SMC branch the number of score evaluations is at most

  Σ_b 2^{|C_b|} + Σ_{e=0}^{1}(1+4ℓ)H_e[1 + 2m(T_e+L+4)] + 4N₁[1 + 2m(T₁+L+4)] + (8ℓ+3)(ℓ+1)[p + k_*(p−k_*)],

with m = p + B + 2 (T32(i); checked by W3-VT38E as a valid, loose upper bound). LS0 adds at most
**1 + (ℓ+1)·max_{k≤K}[p + k(p−k)]** score calls: the emitted centre plus at most ℓ + 1 scans ([CON] §6). Using
Σ_b 2^{|C_b|} ≤ 2^{16}p, N_e ≤ 4max(2500, n, p), T_e ≤ 4max(1000, ℓ²), L = O(log n), ℓ = O(log(n+p)) and k(p−k) ≤ p²/4,
the total is O((n+p)(p+B)log²(n+p) + p²log²(n+p)), which is polynomial in n under R1. The exact branch scores
Σ_{k≤K}C(p,k) ≤ (5H₀ + 4N₀)p models.

---

## 7. Assembly: proof of Theorem 5

- **(0).** §1.1. **(0_H)** is §1.2.
- **(a).** §2: D_n ≤ P₀(s₀ > K) + E₀[1 − π₀(S₀)] → 0 under (F). Under the HPM convention, D_n^{sl} ≤ P(SMC ∩ 𝒜ᶜ) is added.
- **(b1).** Theorem b1 (§3.3) gives D_n → 0. Under the HPM convention with OP-LS0 on schedule_limit fits, the same
  argument gives D_n^{sl} ≤ P₀(π₀(S°) ≤ ½) + P₀(E_nᶜ) + 1{n < n₀} + 1{ℓ_n < φ̄ − 1} + P₀(s₀ + d > K) → 0, because LS0 is a
  function of the data alone.
- **(b1′).** §4.3.
- **(b2).** §5.1.
- **(b1-LH).** Corollary b1-LH (§3.4).
- **(c).** §6. ∎

---

## 8. Repairs and corrections incorporated

The A-REV1-driven changes are tabulated in T38_STATEMENT Part 0 (S1–S9). The W4-T38FULL repair table (its §8: W1-T38E,
W3-VT38E, W3-VT37R, W2-VT24G, W2-PREM, W2-BOOK, W3-VEXP, W2-VT03R items) is carried over unchanged, with three
replacements:
- the "T11(vii)" line is replaced by locked T21(C1) / the direct set proof (§1.1);
- "NL0 threshold" is complemented by the quantifier correction ([CON] §8);
- "Lemma S (tight)" now reads "Lemma S′ (tight only for f > 1 − e)".
