# O-MIX: three fixes for masked-regime discovery (LS0, mixture of block starts, common plug-in σ²)

Run O-MIX (Opus 5.5), 2026-11-02, branch `theory/O-MIX`. Candidates only: nothing here is reviewed or adopted. Status words follow `theory_campaign/PROTOCOL.md` and are never upgraded. Notation follows `00_COMMON.md`, `METHODOLOGY_v3.md` §§5–6.3 and F-DRAFT `NEW_TARGETS.md` §0: ν = a₀ + n/2, t_S = n z_SᵀH_S⁻¹z_S, Q_S = yᵀy − t_S, D_S = det H_S/det(G_S + I), c := 2b₀ + yᵀy, Φ(S) = |S Δ S₀|.

## 1. Headline

1. **The two candidates attack two different masking mechanisms, and neither one covers both.** In the masked regime the start fails for one of two reasons:
   - **cancellation masking** (CL(0)/CL(L): LH, LH-iid, T27);
   - **dilution masking** (σ² integrated per block against the full-y residual: Lemma W1, W3-VEXP Prop D, which is the study's n = 200 mechanism).

   **(B)**, the mixture over linked-merge partitions, undoes cancellation masking at a cost of log 2 nats and does nothing for dilution. **(C)**, common plug-in σ² tables, undoes dilution exactly under BO and leaves cancellation masking untouched. Both claims are PROVED in the forms stated in §2. (A) LS0 remains the only fix proved on LH that needs no change to the start.
2. **(B), validity.** A finite mixture of exact block starts is exactly samplable with an exactly known density. T09(ii), T12, T13 and T22(iv) hold verbatim with γ₀ := π₀^mix. T22(i) holds with a factor λ_i. The identity T22(ii-a) becomes a two-sided sandwich (Prop B1). **PROVED.**
3. **(B) on LH, exact Gram (Thm B3).** With the deterministic, X-only "merge linked block pairs" partition 𝒫⁺ mixed ½ : ½ with the v3 partition:
   - π₀^mix(S₀) ≥ ½ − O_P(2^{2g} n^{−1/2});
   - the final run's iid draws then score S₀ (route (a), T11(iii)), so **T38(b) on LH holds without LS0**.

   **PROVED-UNDER** the VERIFIED W1-EXP Thm 6 and the locked T03, T11(iii) and T21, for 2g ≤ 16. On LH-iid (p ≫ n) it is a PROOF SKETCH.
4. **(C), validity and limits.** Common-σ̂² tables are positive product-form tables, so every locked identity holds **verbatim**: T09, T12, T13, T22(i)(ii)(iv). Two results (both **PROVED**):
   - **Thm C1** (deterministic, under BO): π₀^C(S₀) ≥ π(S₀)·exp{−ν ψ(u)}, where ψ(u) = u − 1 − log u and u = (2b₀ + Q_{S₀})/(2νσ̂²). So a plug-in with |Q_{S′} − Q_{S₀}| = o(√n) gives π₀^C(S₀) ≥ π(S₀) − o_P(1).
   - **Prop C3:** on any CL(0) chain, π₀^C(S₀) ≤ p^{−c} n^{−c/2} e^{O_P(1)}. So (C) alone does **not** make T38(b) provable on LH, by route (a) or by (b1′).
5. **Recommendation (§8).** Keep LS0 as the main-theorem route, since it is already approved and its risk is the smallest. Add (B-merge) as the second fix if Felipe wants T38(b) to hold *without* a local-search patch: it is cheap, it is bounded no-regret (π₀^mix ≥ ½π₀ everywhere), and it gives the strongest statement (route (a) discovery). Do not adopt (C) as a masking fix for the theorem. It is the right tool for the n = 200 *dilution* masking, but it introduces a null-inflation risk (§5.4) and needs its own pilot.

## 2. Setting and the three candidates

- **Common.** G, the v3 target π (unchanged by every candidate), Ω = {|S| ≤ K}, the bridge q_φ ∝ γ₀e^{φd} with d := log(ϖ·BF) − log γ₀ (γ₀ unnormalised) and Z̄₀ = Σ_Ω γ₀.
- **The masked families** are LH (exact Gram, p ≤ n − 1; W1-EXP §4) and LH-iid (W3-PXN). The masked set is M = {j_{b_1}, …, j_{b_c}}, the reference is S° = S₀ ∖ M ∈ 𝓡₀, and masking is π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)} (W1-EXP Thm 5(b)).
- **(A) LS0.** The production local search (M §6.10) is run once more from S̃₀ = argmax π₀ (exact, by max-plus convolution), with the centre emitted (T38_STATEMENT, OP-LS0).
- **(B) Mixture start.** Partitions 𝒫₁, …, 𝒫_m are fixed before any start randomness, as functions of X only (or of X, y and streams 0–9). Each has positive tables r_b^{(i)}. The mixture start is
  - π₀^mix := Σ_i λ_i π₀^{(i)}, with π₀^{(i)} = γ₀^{(i)}/Z̄₀^{(i)} and λ_i > 0;
  - γ₀ := π₀^mix (so Z̄₀ = 1) and d^mix(S) = log ϖ(S)BF(S) − log π₀^mix(S).

  The concrete choice is **(B-merge)**, with m = 2 and λ = (½, ½):
  - 𝒫₁ = the v3 partition;
  - 𝒫₂ = 𝒫⁺ := the v3 partition after merging every connected component of the *link graph* E_τ = {(b, b′) : max_{j∈C_b, l∈C_b′} |r_jl| > τ_n}, with τ_n := 3√(log p/n). A component is merged only if its size is ≤ B⁺ := 16, the implementation limit; otherwise it is left unmerged.

  Random partitions are treated in Prop B2.
- **(C) Common plug-in σ².** Tables r_b^C(U) := D_U^{−1/2} exp{t_U/(2σ̂²)} on the v3 partition, i.e. the known-σ² g-prior Bayes factor with σ² := σ̂². σ̂² is computed before the tables. The concrete choice is **(C-fix)**: σ̂² = (2b₀ + Q_{S′})/(2ν), with S′ the fixed point of S′ ← argmax π₀^C[σ̂²(S′)], started from the v3 start mode. In the numerics this converged in ≤ 3 iterations.
- **(C-grid)**, a (B)∘(C) hybrid: the uniform mixture of the (C) starts over the grid σ̂²_k = σ̂²_∅ e^{−kη/√ν}, k = 0, …, m − 1, with m = ⌈√ν log(n + 1)/η⌉ + 1.

## 3. Statements and proofs: (B)

### Prop B1 (exact samplability; what each locked identity becomes). PROVED.
For any partitions 𝒫_i of [p] into blocks of size ≤ K, any positive tables and any weights λ_i > 0 with Σλ_i = 1:

- **(a) Sampling.** Draw I ~ λ, then S ~ π₀^{(I)} by the backward sampler of T09(i). This returns S with probability exactly π₀^mix(S); fresh streams give iid draws.
- **(b) Density.** log π₀^mix(S) = logsumexp_i [log λ_i + log γ₀^{(i)}(S) − log Z̄₀^{(i)}] is exactly computable: m table products and the m exact convolution normalisers of T09(i).
- **(c) Verbatim identities.** With γ₀ := π₀^mix and Z̄₀ := 1, the following hold verbatim:
  - **T09(ii)–(iv):** reversibility of every step for γ_φ, and self-adjointness of the random-order round;
  - **T12:** unbiased Ẑ_r, the islandwise E[Ẑ_r PIP̂_rj] = Z·PIP_j, and the Markov bound (also T31(i));
  - **T13:** the restricted-ESS identities;
  - **T22(iv):** endpoint propagation.
- **(d) T22(i) per component.** π₀^mix(S°) ≥ max_i λ_i π₀^{(i)}(S°). In particular, the T22(i) bound of any component times λ_i is a bound for the mixture.
- **(e) T22(ii-a) becomes a sandwich.** It is no longer an identity:

  min_i ρ_i ≤ π₀^mix(S₀)/π₀^mix(S°) ≤ max_i ρ_i, with ρ_i := π₀^{(i)}(S₀)/π₀^{(i)}(S°).
- **(f) Weight stability.** sup_S π/π₀^mix ≤ min_i λ_i^{−1} sup_S π/π₀^{(i)}. So the independence-sampler rate 1 − 1/M (F-DRAFT W0(iv)) and the iid discovery budget are at most a factor 1/λ_i worse than the best component's.

*Proof.*
- (a) P(S) = Σ_i λ_i π₀^{(i)}(S) by the law of total probability and T09(i) for each component.
- (b) This is the definition, plus T09(i)'s exact Z̄₀^{(i)}.
- (c) The cited proofs use only four facts about γ₀:
  - γ₀ > 0 on Ω;
  - γ₀ is evaluable pointwise, which is what the Gibbs and swap Hastings ratios need;
  - exact iid draws from γ₀/Z̄₀ (stage 0 and the independence proposal: START in T12's statement);
  - Z̄₀ is known (T12: Ẑ₀ = m(∅)Z̄₀).

  None uses the product form, which enters only in T09(i)'s sampler, and that is replaced by (a). Checked against the statement texts:
  - T09: STATEMENT.md lines 19–33; the steps are defined through γ_φ ratios.
  - T12: STATEMENT.md "START".
  - T22(iv): (iv-a) is Hölder applied to q_φ ∝ γ₀^{1−φ}(ϖBF)^φ and holds for any positive γ₀.
- (d) This is termwise: every term of the mixture is non-negative.
- (e) π₀^mix(S₀)/π₀^mix(S°) = Σ_i λ_iπ₀^{(i)}(S°)ρ_i / Σ_i λ_iπ₀^{(i)}(S°) is a weighted mean of the ρ_i (the mediant inequality).
- (f) π/π₀^mix ≤ π/(λ_iπ₀^{(i)}) for each i.

∎ (This is F-DRAFT Prop P(ii), re-proved here with (c) checked clause by clause and (e) added.)

**What changes in the text.** T22(ii)'s *exact* reference-to-truth odds hold per component, not for the mixture. Every proof that composes T22(ii-a) with a ratio law must therefore be applied to one component and then multiplied by λ_i. This is the case for T27(i) and W1-EXP Thm 4.

**Engine cost of (b).** The engine computes d by block-local increments. Under (B) it has to keep m running sums of log-tables per particle and take a logsumexp: O(m) arithmetic per score on top of the O(k³) score.

### Prop B2 (random partitions do not undo LH masking). PROOF SKETCH (crux PROVED).
On LH (exact Gram, fixed g ≥ 2, ρ ∈ (0, 1)), let 𝒫 be any partition that separates the true hub j_a from a member l of its own group C_a. Then

  π₀^{𝒫}(S₀) ≤ exp{−c n} w.p. → 1, for some c > 0 depending on (ρ, ψ, β).

*Crux (PROVED, modulo W1-EXP Thm 1 = EXP′, VERIFIED).* Let T := S₀ ∩ C_{𝒫(l)}. Then δ_{T,l}²/(n−1) ≥ c₁ > 0. The reason is that Cov(x_l, μ) ⊇ ρβ(1−ψ²), and T contains neither j_a nor (for g ≥ 2, generically) a variable spanning x_l's projection on μ. So x_{T,l} → a positive constant, and EXP′ gives log r(T + l)/r(T) ≥ c₂ n. By T22(ii-a), applied with S° = S₀ and S = S₀ + l inside that component:

  π₀(S₀)/π₀(S₀ + l) ≤ [w(s₀)/w(s₀+1)]·e^{−c₂n} = O(p)·e^{−c₂n}.

A uniformly random partition into blocks of size B keeps C_a whole with probability ≤ (B/p)^{g−1}. With K random partitions, the expected number of components that keep every signal group whole and co-block every linked pair is ≤ K(B/p)^{(g−1)(c + v) + c}, where v is the number of visible groups. So uniform random partitions need K polynomial in p with a large exponent. **Use a structured mixture, not a random one.** The "generic" clause in the crux is where the sketch status comes from: if T happens to contain another group-a member the argument needs λ_min, which it has, but I did not write out that case.

### Lemma B-link (the link graph recovers exactly the linked pairs). PROVED (exact Gram); PROOF SKETCH (iid).
On LH, exact Gram, the in-sample cross-block correlations are ψ_i, ψ_iρ, ψ_iρ² between linked groups and 0 otherwise. Hence, for n with τ_n < min_i |ψ_i|ρ_-², E_τ is exactly the matching {(a_i, b_i)}, and 𝒫⁺ = groups with each linked pair merged (size 2g).

*iid:* each null cross-correlation is ~N(0, 1/n), and there are ≤ p² of them, so P(max > 3√(log p/n)) ≤ p²·p^{−9/2} → 0. Population links ψρ² > 0 are fixed, and their sampling error is O_P(√(log p/n)) uniformly. ∎

### Theorem B3 ((B-merge) on LH, exact Gram). PROVED-UNDER the VERIFIED W1-EXP Thm 6, the locked T03, T11(iii) and T21, and Prop B1.
Assume LH, exact Gram, p ≤ n − 1, g ≤ B_n < 2g, 2g ≤ 16, fixed nonzero β, ψ_i ≠ 0, |ψ_i| < min(ρ_{a_i}, ρ_{b_i}), and at least two signal blocks in 𝒫⁺ (c + #visible ≥ 2). Then:

- **(i)** 1 − π₀^{𝒫⁺}(S₀) = O_P(2^{2g} n^{−1/2}), and hence π₀^mix(S₀) ≥ ½ − O_P(2^{2g}n^{−1/2});
- **(ii)** with Q_f ≥ 4N_e iid π₀^mix draws in the final run, P(S₀ ∉ 𝒮) ≤ E(1 − π₀^mix(S₀))^{Q_f} → 0;
- **(iii)** P(𝒪 ∩ {Ŝ ≠ S₀}) → 0, without LS0. This is T38(b) through route (a).

*Proof.*

(i) Blocks of 𝒫⁺ are, by Lemma B-link and Lemma 4.2 of W1-EXP, the visible groups, the unlinked null groups, and the merged pairs C_{a_i} ∪ C_{b_i}. Apply W1-EXP Thm 6 (VERIFIED by W3-VEXP) to 𝒫⁺ with reference S° := S₀. Its hypotheses are checked one by one below.
  - *SE-blk:* λ_min(R_{C}) ≥ λ_min(Σ) ≥ (1−ψ₊)(1−ρ₊) by W1-EXP Lemma 4.1(a), and the merged block is a principal submatrix.
  - *ZL(S₀):* on a merged block C = C_a ∪ C_b, Cov(X_C, μ − μ_ab) = 0 with μ_ab := β(x_{j_a} − ψx_{j_b}). This holds because the other groups are independent of C_a ∪ C_b, and exact Gram makes it hold in-sample. So P_Cμ = μ_ab ∈ span{x_{j_a}, x_{j_b}} = span X_{S₀∩C}. On visible groups P_{C_h}μ = β_h x_{j_h} (Lemma 4.1(c)), and on null groups P_Cμ = 0.
  - *SPREAD:* every block of 𝒫⁺ misses the signal of at least one other signal block, whose energy is a fixed positive number because λ_min(Σ) > 0 and β ≠ 0. This is where c + #visible ≥ 2 is needed.
  - *VIS-lin(S₀):* for U ⊆ C with S₀∩C ⊄ U,

    ‖(P_{U∪(S₀∩C)} − P_U)μ‖² = ‖(I − P_U)μ_ab‖² ≥ λ_min(G_{U∪{j_a,j_b}})·β²·min(1, ψ²) ≥ (n−1)(1−ψ₊)(1−ρ₊)β² min(1, ψ²).

    The coefficient vector of μ_ab has a nonzero entry on a hub outside U, and ‖(I−P_U)X_Wα‖² ≥ λ_min(G_W)‖α_{W∖U}‖². Visible groups are as in W1-EXP Thm 5(a).
  - *R-lite:* ‖μ‖²/n ≤ θᵀΣθ; p ≤ n.
  - *Block size:* ≤ 16, which Lemma 1.4 (the RSS floor) needs.

  Thm 6 gives 1 − π₀^{𝒫⁺}(S₀) = O_P(2^{2g}n^{−1/2}). Prop B1(d) gives the mixture bound.

(ii) This is T11(iii) (locked), with the draws iid from π₀^mix by Prop B1(a). The proof of T11(iii) uses only iid exact draws from the start law, and Q_f ≥ 4N_e → ∞. Bounded convergence then gives E(1 − π₀^mix(S₀))^{Q_f} ≤ P(π₀^mix(S₀) < ¼) + (¾)^{Q_f} → 0.

(iii) T38(0) (the locked T21 composition, with RO and GUARD as in T38_PROOF) gives

  P(𝒪, Ŝ ≠ S₀) ≤ 2E₀δ₁ + P(S₀ ∉ 𝒮̄).

δ₁ → 0 is W1-EXP Thm 5(d) (locked T03), and (P) concerns the target only, which (B) does not change. The second term is (ii). ∎

**Remarks.**
1. **No-regret.** The base component keeps weight ½, so (F) ⇒ π₀^mix(S₀) ≥ ½π₀(S₀) → ½ and T38(a) survives. Every favourable-regime statement survives with constants changed by at most a factor 2.
2. **c ≥ 2 costs nothing extra.** Every linked pair is merged in the *same* component, so the cost stays log 2 nats. By contrast, a per-edge mixture of components (one merge each) only lifts the masking of one pair at a time: π₀ ≈ (p^{−1}n^{−1/2})^{c−1}/|E|.
3. **Hub-move variant.** Merged blocks of size 2g > 16 (for example the study's B = 14) are too costly. A cheaper variant moves one endpoint of each linked edge into the other's block, giving block sizes B + 1. The algebra above works when j_b is moved into C_a: ZL then holds on C_a ∪ {j_b} and on C_b ∖ {j_b}. Moving j_a into C_b fails, by the Prop B2 crux. Since the data cannot tell which hub is the suppressor, both orientations must be mixed: 2^{|E|} components at weight 2^{−|E|}, a cost of |E| log 2 nats and an O(2^{|E|}) density. This is PROOF SKETCH, and it is acceptable only for small |E|.
4. **LH-iid (p ≫ n).** ZL fails in-sample, so Thm 6 does not apply. The route would be the W3-PXN start argument at reference S₀ on the merged partition; I did not check it line by line. PROOF SKETCH.

### Cost of (B-merge) (iv).
- **Tables:** the base tables, plus Σ_{merged C} 2^{|C|} ≤ |E|·2^{2B} scores. At B = 4–8 this is negligible. At the study's B = 14 a merged pair of 10 + 10 would be capped (20 > 16) and fall back to the hub-move variant: 2·|E| blocks of size ≤ 15, ≈ |E|·2^{16} scores.
- **Normalisers:** one extra convolution per component.
- **Per score:** m = 2 table products (incremental) and one logaddexp.
- **Link graph:** p²/2 correlations, already computed for the neighbour graph (M §6.4).
- **Engine:** the independence proposal and stage-0 draws need one extra uniform for the component.

**Total:** a few times the table cost (2.9 s at p = 1,000, B = 14) and < 5% on SMC scoring. In the masked families, though, |E| can be as large as the number of linked block pairs. The study's S5 (common factor) would link *every* pair of blocks (W1-EXP: leakage in 98/100 blocks), so the merge cap binds and (B) degenerates to the base start (no harm, no help).

## 4. Statements and proofs: (C)

### Prop C0 (validity). PROVED.
r_b^C(U) > 0 for every U, and γ₀^C = ϖ∏_b r_b^C has product form. So T09 (including the backward sampler and the exact Z̄₀), T12, T13, T21 and T22(i)(ii)(iv) hold **verbatim**: their statements quantify over arbitrary positive tables (T22 STATEMENT.md line 17 and change C6). The target π is unchanged.

**What changes:** every *table-specific* expansion must be re-derived:
- EXP′ (W1-EXP Thm 1) becomes exact: log r^C(T+l)/r^C(T) = −½ log(D_{T+l}/D_T) + (t_{T+l} − t_T)/(2σ̂²), with no ν-log remainder;
- T22(iii), T27(i) and W1-EXP Thms 3–6 are stated for BF tables and need re-checking, with the multiplier σ²/σ̂² in place of σ²/v_T.

σ̂² must be frozen before the start randomness. It is a function of (X, y), like the partition, so EX-S and CAL are unaffected.

### Theorem C1 (dilution removed exactly under BO; deterministic). PROVED.
Assume BO: X_{C_b}ᵀX_{C_b′} = 0 for b ≠ b′. Let σ̂² > 0 and u(S) := (2b₀ + Q_S)/(2νσ̂²). Then for every S ∈ Ω:

- **(a)** d^C(S) = h(t_S), with h(t) := −ν log(1 − t/c) − t/(2σ̂²). h is strictly convex on [0, c), and its minimum is at t* with c − t* = 2νσ̂².
- **(b)** h(t_S) − min h = ν ψ(u(S)), with ψ(u) := u − 1 − log u ≥ 0.
- **(c)** π₀^C(S₀) ≥ π(S₀) · exp{−ν ψ(u(S₀))}. More generally, π₀^C(A) ≥ π(A) e^{−max_{S∈A} νψ(u(S))} for every A ⊆ Ω.
- **(d)** Hence, for a plug-in σ̂² = (2b₀ + Q_{S′})/(2ν) with |Q_{S′} − Q_{S₀}| = o_P(√n), and Q_{S₀} ≥ c₀n w.p. → 1 (true under G with σ² > 0):

  π₀^C(S₀) ≥ π(S₀)(1 − o_P(1)).

*Proof.*
- (a) Under BO, G_S and H_S are block diagonal, so D_S = ∏_b D_{S_b} and t_S = Σ_b t_{S_b} (F-DRAFT Lemma W1). Hence

  log BF(S) = −½ log D_S − ν log((2b₀+Q_S)/c),  Σ_b log r_b^C(S_b) = −½ log D_S + t_S/(2σ̂²).

  Since 2b₀ + Q_S = c − t_S, d^C(S) = h(t_S). The function is convex since h″(t) = ν/(c−t)² > 0, and h′(t*) = 0 ⇔ ν/(c − t*) = 1/(2σ̂²).
- (b) Write x := c − t. Then h = −ν log(x/c) + (x − c)/(2σ̂²). With x* = 2νσ̂², h(t) − h(t*) = ν[−log(x/x*) + x/x* − 1] = νψ(x/x*), and x/x* = u(S).
- (c) γ₁/γ₀^C = e^{d^C}, so π(S)/π₀^C(S) = e^{d^C(S)}·Z̄₀/Z̄₁. Then

  π₀^C(A) = Σ_{S∈A} π(S) e^{−d^C(S)}·(Z̄₁/Z̄₀) and Z̄₁/Z̄₀ = E_{π₀^C}[e^{d^C}] ≥ e^{min h}.

  So π₀^C(A) ≥ Σ_A π(S)e^{−(d^C(S) − min h)}, and (b) gives the claim.
- (d) u − 1 = (Q_{S₀} − Q_{S′})/(2b₀ + Q_{S′}) = o_P(n^{−1/2}), and ψ(u) ≤ (u−1)²/min(u, 1). So νψ(u) = o_P(1).

∎

*Reading.* v3's own tables integrate σ² per block, which corresponds to a block-specific "σ̂_b²" of size v_{T_b} = σ² + Δ_{T_b}. That is the dilution loss of Lemma W1, Θ(n) on models whose R² is spread over blocks. Under BO, (C) replaces this Θ(n) loss by νψ(u) → 0. It is the exact cure for dilution, and it holds for *every* S simultaneously in the sense of (c).

The plug-in condition |Q_{S′} − Q_{S₀}| = o(√n) is weak:
- an S′ that misses only truths of energy O(log n) (the weak truths that dilution masks), or carries O(1) extras, satisfies it, since then |Q_{S′} − Q_{S₀}| = O_P(log n);
- the null plug-in S′ = ∅ does not: u − 1 ≈ −R², which brings back the Θ(n) loss.

**That the (C-fix) iteration delivers such an S′ is CONJECTURE.** It is supported by the numerics (§6): on BO-D at n = 200, S₀ ⊆ mode in 92% of replicates.

### Prop C2 (σ̂²-grid mixture; logarithmic cost without a plug-in). PROVED (under BO).
For the (C-grid) mixture with log-spacing η/√ν over [σ̂²_lo, σ̂²_∅], σ̂²_lo := (2b₀ + yᵀy/(n+1))/(2ν) (the floor Q_S ≥ yᵀy/(n+1), M §5):

  π₀^{grid}(S₀) ≥ π(S₀) · exp{−η²/2·(1 + O(η/√n))} / m,  m = ⌈√ν·log(n+1)/η⌉ + 1.

So the cost is log m = ½ log n + log log n + O(1) nats, against the Θ(n) dilution loss. With the masking cost c log p + (c/2)log n, this is cheaper whenever c ≥ 1 and p ≥ log n.

*Proof.* Some grid point has |log u| ≤ η/(2√ν). Then ψ(u) ≤ (log u)²(1 + |log u|)/2, since ψ(e^v) = e^v − 1 − v ≤ v²e^{|v|}/2. Combine with Thm C1(c) and Prop B1(d). ∎

### Prop C3 (cancellation masking is untouched by (C)). PROVED.
Let H1 and CL(0) hold along a chain S° = S^{(0)} ⊂ … ⊂ S^{(c)} = S₀, where the i-th addition l_i enters a block C_{b_i} with T_i = S^{(i)} ∩ C_{b_i} and δ_{T_i,l_i} = 0. This is the LH situation, with T_i = ∅ (W1-EXP Thm 5(b) proof). Let σ̂² ≥ σ_lo² > 0 w.p. → 1. Then w.p. → 1

  π₀^C(S₀) ≤ π₀^C(S₀)/π₀^C(S°) = ∏_{i<c} [w(s+i+1)/w(s+i)] · (D_{T_i+l_i}/D_{T_i})^{−1/2} · e^{σ²Z_i²/(2σ̂²)}(1 + O(1/n))
       = p^{−c} n^{−c/2} e^{O_P(1)},  Z_i ~ N(0, 1).

*Proof.* T22(ii-a) holds verbatim (Prop C0). For one addition:
- t_{T+l} − t_T = n·[x_lᵀ(I − P̃_T)y]²/(…)·(1 + O(1/n)), and its population part is δ_{T,l}² = 0;
- so (t_{T+l} − t_T) = σ²Z²(1 + O(1/n)), with Z the standardised x_lᵀ(I−P_T)ε. This is exactly so on LH, where T = ∅ and x_{j_b}ᵀμ = 0;
- D_{T+l}/D_T = (n+1)(1 + O(1/n)) under SE on the chain sets;
- w(k+1)/w(k) = (k+1)/(2p−k−1).

Multiply over the chain. ∎

**Consequence for T38(b) on LH.**
- *Route (a) fails under (C):* Q_f π₀^C(S₀) → 0 whenever Q_f = o(p^c n^{c/2}). That is the same condition as for v3: c ≥ 2, or c = 1 with p/(√n log²n) → ∞.
- *Route (b1′) is unchanged:* D2 needs a one-flip neighbour of S₀ with π₀ > 1/10. For c = 1 that is S°, exactly as without (C), and D2's statistical instance (NB) is still the open step.
- *Route (b1)* still needs LS0.

So **(C) alone does not make T38(b) provable** on any family where masking is cancellation.

### 4.4 The risk introduced by (C): null inflation. PROOF SKETCH.
Under BO the null increments become −½ log n + σ²Z_l²/(2σ̂²), whereas v3 has (1−κ)Z²/2 (F-DRAFT W5).
- **Start concentration** needs Σ_l p^{−1}n^{−1/2}e^{(σ²/σ̂²)Z_l²/2} → 0. By the heavy-tail argument of F-DRAFT Thm W step 4 this is ≍ p^{σ²/σ̂² − 1}n^{−1/2}·L(p).
- **Condition.** With p ≤ n^A the start therefore stays concentrated iff σ̂²/σ² > 2A/(2A + 1) asymptotically. A plug-in that *overfits*, e.g. S′ with many extras, can push σ̂² below this, and the start then fills with nulls.
- **v3's protection.** v3's dilution protects against exactly this; F-DRAFT W5 describes the trade-off.
- **Safeguard.** Any (C) deployment needs σ̂² ≥ a floor, e.g. the RSS of S̃₀ with a degrees-of-freedom correction, and a pilot.

## 5. (A) LS0 for comparison (from W4-T38FULL; not re-proved here)
- T38(b1) on LH, exact Gram, is PROVED-UNDER (M1)–(M3) with every premise discharged (b1-LH).
- LH-iid (W3-PXN) is unverified.
- **Cost:** (ℓ+1)·max_{k≤K}[p + k(p−k)] scores. At p = 1,000, ℓ = 11, k ≈ 15 that is ≈ 1.7·10⁵ scores, about 1–3 s.
- **Validity:** the search alters no particle, so T09, T12, T13 and T22 are untouched. The HPM only improves, and LS0 can be added post hoc to the 2,400 fits (O-LS0's data check).
- **Weakness:** LS0 does not fix the *start*. Evidence and PIP accuracy in the masked regime are not improved, because the bridge still has to cross (F-DRAFT W″). It also needs a lattice progress condition (M2), which is family-specific.

## 6. Evidence (exact small-p computation)

**Script and method.**
- Script: `scripts/mixnum.py`, seeds 20261102 + 100·config + n-index. It runs on sufficient statistics in the exact-Gram realisation.
- Code: it imports W1-EXP's `bvs_exact.py` and `family.py`, copied verbatim as `scripts/w1exp_*.py`, which port the v3 partition (`v3_blocks.h`).
- π₀ masses use the exact convolution normaliser, start modes use max-plus convolution, and π is computed by full enumeration.
- Raw output: `results/mixnum_{0,1,2}.txt`.

**Families.**
- LH-A: p = 16, c = 1, ρ = 0.7, ψ = 0.5.
- LH-B: p = 20, c = 2.
- BO-D: p = 16, a block-orthogonal dilution family, truths 1.5, 1.5, 0.32 in three groups.

**Columns.** Medians over replicates of log₁₀ π₀(S₀) for each start, then med π(S₀), and the share of replicates in which the v3 mode = S° ("mode=S°") and in which S₀ ⊆ the C-fix mode.

| family | n | base v3 | 𝒫⁺ | **(B) mix** | C-oracle | **C-fix** | C-null | C-grid | π(S₀) | mode=S° | S₀ ⊆ C-fix mode |
|---|---|---|---|---|---|---|---|---|---|---|---|
| LH-A | 200 | −2.18 | −0.09 | **−0.38** | −2.16 | **−2.16** | −2.18 | −2.43 | 0.78 | 1.00 | 0.00 |
| LH-A | 800 | −2.45 | −0.03 | **−0.33** | −2.39 | **−2.41** | −2.45 | −2.75 | 0.88 | 1.00 | 0.00 |
| BO-D | 200 | −1.51 | −1.51 | **−1.51** | −0.27 | **−0.27** | −1.52 | −0.74 | 0.53 | 0.00 | 0.92 |
| BO-D | 800 | −0.11 | −0.11 | **−0.11** | −0.04 | **−0.04** | −0.11 | −0.39 | 0.91 | 0.92 | 1.00 |

Additional rows. C-grid at n = 3200 was skipped because m > 200. LH-B at n = 3200 was still running at hand-back.

| family | n | base v3 | 𝒫⁺ | **(B) mix** | C-oracle | **C-fix** | C-null | C-grid | π(S₀) | mode=S° | S₀ ⊆ C-fix mode |
|---|---|---|---|---|---|---|---|---|---|---|---|
| LH-A | 3200 | −2.73 | −0.02 | **−0.32** | −2.63 | **−2.66** | −2.73 | — | 0.94 | 1.00 | 0.00 |
| LH-B (c = 2) | 200 | −4.33 | −0.14 | **−0.44** | −4.09 | **−4.22** | −4.33 | −4.32 | 0.71 | 1.00 | 0.00 |
| LH-B (c = 2) | 800 | −4.92 | −0.04 | **−0.34** | −4.72 | **−4.84** | −4.92 | −5.23 | 0.81 | 1.00 | 0.00 |
| BO-D | 3200 | −0.02 | −0.02 | **−0.02** | −0.03 | **−0.03** | −0.02 | — | 0.94 | 1.00 | 1.00 |

- **LH-B (c = 2):** the base start falls by ≈ 1 decade per factor 4 in n, which is T27's predicted slope of −c/2 per decade. (B) is ≈ 10^{−0.34…−0.44} with both pairs merged in one component, so the cost is log 2 and does not grow with c. (C) equals the base.
- **BO-D at n = 3200:** with fixed β the v3 start is favourable again, as §7 predicts: dilution masking is a finite-n phenomenon.
- **Not run (time box):** LH-iid and the hub-move variant.

**Readings.**
- **LH.** (B) lifts π₀(S₀) from ≈ 10^{−2.2…−2.5} (masking, falling by ≈ 0.5 decade per factor 4 in n, as T27 predicts) to ≈ 0.4–0.47, consistent with ½·π₀^{𝒫⁺}(S₀) → ½ (Thm B3). The link graph found exactly c pairs in every replicate (Lemma B-link). All three (C) variants equal the base to within 0.06 decades (Prop C3). The base v3 mode is S° in 100% of replicates, which is what LS0 needs (M1).
- **BO-D (dilution).** The base start is masked at n = 200 (π₀(S₀) ≈ 0.03 against π(S₀) = 0.53). C-fix and C-oracle restore π₀^C(S₀) ≈ π(S₀) (0.54), and C-grid pays its log m cost (−0.74). (B) changes nothing, because there are no links. C-null equals the base, since S′ = ∅ is exactly the dilution case.
- **Thm C1's bound** held in 100% of BO-D replicates. On LH, which is not BO, it held in only 42% at n = 200, as expected: C1 is a BO theorem.

## 7. What fails and why
- **Random partitions (B-random).** A uniformly random partition splits signal groups, and every split creates a linear-in-n proxy inclusion in the start (Prop B2, the NM mechanism). Only structured, X-driven mixtures work.
- **Per-edge mixtures for c ≥ 2.** They lift one pair at a time (Remark 2 of Thm B3). All links must be merged within a single component.
- **(C) on LH.** It leaves the cancellation untouched, because the table sees δ = 0 for any σ̂² (Prop C3). No σ² choice can create a signal that the block projection does not contain.
- **(B) on dilution.** Merging does not remove dilution unless one block contains all the signal, and that requires blocks of size ≥ s₀·g. The merge cap prevents this.
- **(C) with the null plug-in.** σ̂² = s_y² reproduces the dilution exactly (u − 1 ≈ −R²).
- **(C) asymptotically on BO with fixed β.** The dilution masking of v3 is a finite-n phenomenon there: VIS-lin gives linear gains, so the v3 start is favourable as n → ∞ (W1-EXP Thm 2/6). An *asymptotic* theorem in which (C) beats v3 needs a weak-signal window θ_w² ∈ (σ², v)·(1+2A)·log n/n. In that window, T03's beta-min in the BM-∞ form fails (M_n → ∞ is required). So (C)'s advantage lives exactly where the locked posterior theorem is silent. This is the main reason (C) cannot carry T38(b).

## 8. Recommendation table (input to the investment-rule decision)

| | (A) LS0 | (B-merge) mixture start | (C) common σ̂² tables |
|---|---|---|---|
| Masking mechanism fixed | cancellation (via lattice repair from S̃₀ = S°) | **cancellation** (start mass ≥ ½ on S₀) | **dilution** (BO: exact, Thm C1); **not** cancellation (Prop C3) |
| T38(b) on LH without other method changes | PROVED-UNDER verified/locked inputs (W4, b1-LH) | **PROVED-UNDER** the verified W1-EXP Thm 6 + locked T03/T11(iii)/T21 (Thm B3), via **route (a)**, the strongest route | **No** (route (a) fails, (b1′) unchanged) |
| LH-iid (p ≫ n) | W3-PXN, unverified | PROOF SKETCH | no |
| Extra premises | (M2) lattice progress, family-specific; ℓ ≥ Φ(S°) − 1 | link detection (τ_n), merged size ≤ 16, ≥ 2 signal blocks | plug-in condition |Q_{S′} − Q_{S₀}| = o(√n) (CONJECTURE for C-fix); σ̂² floor |
| Method-change size | small, post hoc; no particle touched | medium: start sampler + density (m = 2), link graph, engine change in d | small in code (tables only), but changes *every* table and the start's character |
| Score cost | +(ℓ+1)·max_k[p + k(p−k)] ≈ 1.7·10⁵ at p = 1,000 | + ≤ |E|·2^{2B} table scores (capped at 16) + O(1) per score | ≈ 0 (same table count); C-grid ×m ≈ ½√n·log n tables |
| Risk to locked results | none | T09/T12/T13/T22(iv) verbatim; T22(i) ×λ; **T22(ii-a) becomes a sandwich**; T27(i)/W1-EXP chain results apply per component | all locked identities verbatim; **T22(iii), T27, EXP′, W1-EXP Thms 3–6 need re-derivation** for the new tables |
| Risk to performance | O-LS0 data check pending | bounded: π₀^mix ≥ ½π₀ everywhere (no-regret up to log 2) | null-inflation if σ̂² is too small (§4.4); unbounded downside without a floor |
| Needs new runs (investment rule) | no (post hoc) | yes (start changes) | yes (start changes) |
| Helps evidence / PIPs in the masked regime | no | yes (the bridge starts near S₀; weight stability ×2 at worst, Prop B1(f)) | yes for dilution (π₀^C ≈ π under BO) |

**Recommendation.**
1. **Keep LS0 as the main theorem's route.** It is approved, post hoc, and touches nothing locked.
2. **If one start change is made, choose (B-merge).** Of the candidates on the table, it is the only one that yields T38(b) on LH *without* LS0, and it does so through route (a), which needs no lattice condition. Its downside is bounded by log 2. It does not need the 2,400 fits re-validated *for correctness*, because every identity transfers, but under the investment rule it does need a pilot for performance.
3. **Treat (C) as a separate, study-motivated change**, for dilution at n = 200, not as a theorem enabler. If it is pursued, use a floored plug-in and pair it with a pilot.

A combined "(B) + (C)" redeploy is coherent: it is a mixture whose components use common-σ̂² tables (Prop B1 + Prop C0). It is the only option that addresses both mechanisms, but its T27/EXP′ re-derivation cost is the sum of both.

## 9. Needs escalation
1. **Thm B3(i) applies W1-EXP Thm 6 to a partition with block size 2g.** I checked the hypotheses (§3), but not whether Thm 6's proof uses the method's B rule anywhere beyond |C_b| ≤ 16.
2. **The verbatim transfer of T09/T12 to a non-product γ₀** (Prop B1(c)) should be checked against the full proofs (`PROOF_v3.tex`, `PROOF_v6.tex`), not only the statements. I read only the statements.
3. **Prop C3 and §4.4** need a cross-family check of the (1 + O(1/n)) remainders.
4. **The (C-fix) convergence conjecture.**

## 10. Outside scope
- At the study's B = 14, packing already co-blocks two groups of 5 (W1-EXP Lemma 4.2 remark). Whether the 2,400 fits' masking is cancellation or dilution decides which fix matters at n = 200. W3-VEXP Prop D says dilution, and that would favour (C) for *performance*, even though (B) is what the theorem needs.
- (B) also bounds the independence sampler's sup-ratio (Prop B1(f)). This is a free improvement for V11-type evidence results.

## 11. Confidence card

| Target | Refined statement | True? | Provable at reasonable cost? | Crux | Method change? |
|---|---|---|---|---|---|
| (B) validity, Prop B1 | §3 | high | done (PROVED) | full-proof check of T09/T12 for non-product γ₀ | yes (start) |
| (B) on LH, Thm B3 | §3 | high | done modulo the Thm 6 reuse | Thm 6 at block size 2g | yes |
| (B) on LH-iid | Thm B3 for p ≫ n | medium-high | medium | W3-PXN start argument at reference S₀ on 𝒫⁺ | yes |
| (C) validity, Prop C0 | §4 | high | done | — | yes (tables) |
| Thm C1 (BO dilution) | §4 | high | done (PROVED) | — | yes |
| Prop C3 ((C) ∤ cancellation) | §4 | high | done (PROVED) | remainder bookkeeping | — |
| (C) ⇒ T38(b) | false on LH; on BO only in a weak-signal window where T03 is silent | — | low | posterior beta-min in that window | yes |
| C-fix plug-in delivers S′ | CONJECTURE | medium | medium | fixed-point monotonicity under BO | yes |

## 12. Summary (8 lines)
1. (B) and (C) fix different masking mechanisms: (B) fixes cancellation (LH), (C) fixes dilution (BO, the n = 200 mechanism). Neither fixes both.
2. (B) is exactly samplable with an exact density. T09, T12, T13 and T22(iv) hold verbatim, T22(i) holds with a factor λ, and T22(ii-a) becomes a sandwich (PROVED).
3. (B-merge) on LH, exact Gram: π₀^mix(S₀) ≥ ½ − O_P(2^{2g}n^{−1/2}), so T38(b) holds *without* LS0 through route (a) (PROVED-UNDER the verified Thm 6 and locked results). The cost is log 2 nats.
4. (C): all locked identities hold verbatim. Under BO, π₀^C(S₀) ≥ π(S₀)e^{−νψ(u)} (PROVED). On cancellation chains, π₀^C(S₀) = p^{−c}n^{−c/2}e^{O_P(1)} (PROVED), so (C) alone does not give T38(b).
5. Cost: LS0 ≈ 1.7·10⁵ scores; (B) ≤ |E|·2^{2B} table scores + O(1) per score; (C) ≈ 0 (C-grid ×½√n log n tables).
6. Exact numerics (p = 16/20) agree: on LH, (B) 10^{−0.35} against base 10^{−2.3}, with (C) equal to the base; on BO-D at n = 200, (C) 10^{−0.27} ≈ π(S₀) against base 10^{−1.5}.
7. Recommendation: keep LS0 for the main theorem. If a start change is made, choose (B-merge) (no-regret, strongest route). Keep (C) as a separate, piloted, performance-driven change.
8. Head SHA: d1cc689 (content); this line was set in the follow-up commit.
