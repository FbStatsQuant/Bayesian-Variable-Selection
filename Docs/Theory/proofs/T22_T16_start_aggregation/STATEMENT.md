# STATEMENT — T22 (T16), parts (i), (ii), (iv)

Source: `Theory_architecture_v3/theorems/T22_T16_start_aggregation.md` (SMC-BVS v3.0, method SHA-256 93043758…8019c). Only parts (i), (ii), (iv) are stated here; parts (iii) and (v) are out of scope for this run. Parts (i), (ii), (iv-a), (iv-b) are deterministic: they hold for every realisation of the data; (iv-c) is a conditional probabilistic consequence of (iv-b). Exact arithmetic is assumed (idealisation EX-A): π₀, q_φ and all tables are the exact mathematical objects defined below.

Status: statement approved with corrections by Astra (step 1b), 2026-10-22; see "Changes to the statement" at the end.

## 1. Setting and definitions

**Data and model space.** Integers n ≥ 3 and p ≥ 1. X ∈ ℝ^{n×p} (columns x_1, …, x_p) and y ∈ ℝⁿ are fixed (in the method they are the standardised design and response, ‖x_j‖² = ‖y‖² = n − 1; the statements below use only that they are real). K = min(p, ⌊n/2⌋). Ω = {S ⊆ [p] : |S| ≤ K} ("feasible models"). For S ⊆ [p] (any size), with X_S the columns in S:
- G_S = X_SᵀX_S, z_S = X_Sᵀy, H_S = (n+1)G_S + I_{|S|}, D_S = det H_S / det(G_S + I_{|S|}),
- t_S = n z_SᵀH_S⁻¹z_S, Q_S = yᵀy − t_S, ν = a₀ + n/2 with a₀ = b₀ = 0.01,
- m(S) = c_n · D_S^{−1/2}(2b₀ + Q_S)^{−ν}, where c_n = (2b₀)^{a₀}Γ(ν)/(π^{n/2}Γ(a₀)) > 0 (for S = ∅: D_∅ = 1, Q_∅ = yᵀy),
- BF(S) = m(S)/m(∅).
- Size prior: w(k) = ½ / C(2p−1, k) for 0 ≤ k ≤ p; W_K = Σ_{k≤K} C(p,k)w(k); ϖ(S) = w(|S|)/W_K for S ∈ Ω.
- Posterior: π(S) = ϖ(S)m(S)/Z for S ∈ Ω, Z = Σ_{S∈Ω} ϖ(S)m(S).

**Blocks and tables.** C_1, …, C_J is a partition of [p] into nonempty blocks with |C_b| ≤ B ≤ K (in the method: the deterministic complete-linkage/cut/next-fit partition with B = min(⌊√n⌋, ⌊√p⌋, 16); parts (i) and (iv) use only that it is a partition and that tables are positive). b(l) denotes the block containing l. Tables: r_b(U) = BF(U) for U ⊆ C_b (so r_b(∅) = 1 and r_b(U) > 0).

**Start law and bridge.** For S ∈ Ω: γ₀(S) = ϖ(S)∏_b r_b(S ∩ C_b), Z̄₀ = Σ_{S∈Ω} γ₀(S), π₀(S) = γ₀(S)/Z̄₀. Uncapped weight, for every S ⊆ [p]: γ₀^{unc}(S) = w(|S|)∏_b r_b(S ∩ C_b). Discrepancy d(S) = log BF(S) − Σ_b log r_b(S ∩ C_b). For φ ∈ [0,1] and S ∈ Ω: γ_φ(S) = γ₀(S)e^{φ d(S)}, Z̄_φ = Σ_{S∈Ω} γ_φ(S), q_φ(S) = γ_φ(S)/Z̄_φ. (Thus q₀ = π₀; that q₁ = π is a fact to be checked in the proof.) Masses of sets outside Ω are 0.

**Reference quantities (AGG).** Fix a reference S° ∈ Ω, s = |S°|, U_b* = S° ∩ C_b.
- For each block b and integer j ≥ 0: a_{bj} = Σ_{U : U_b* ⊆ U ⊆ C_b, |U ∖ U_b*| = j} r_b(U)/r_b(U_b*) (so a_{b0} = 1, and a_{bj} = 0 for j > |C_b ∖ U_b*|).
- D_b = max_{1 ≤ j ≤ |C_b∖U_b*|} (j! a_{bj})^{1/j}, with D_b = 0 when C_b = U_b* (empty maximum).
- q = (p−s)⁻¹ Σ_b D_b if s < p; q = 0 if s = p.
- e = 2p · max{ [r_b(U)/r_b(U ∪ U_b*)]^{1/a} : b, U ⊆ C_b, a := |U_b* ∖ U| > 0 }; e = 0 when the set is empty (in particular when s = 0).
- u = (p−s)⁻¹ Σ_{l ∉ S°} max{ r_{b(l)}(T ∪ {l})/r_{b(l)}(T) : U*_{b(l)} ⊆ T ⊆ C_{b(l)} ∖ {l} } if s < p; u = 0 if s = p.
- δ^{comp} = sup{ γ₀^{unc}(S)/γ₀^{unc}(S ∪ S°) : S ∈ Ω, S ⊉ S° }, with δ^{comp} = 0 when s = 0. (The proof may use this sup over feasible S; the bound then also holds for the larger sup over all S ⊆ [p] with S ⊉ S°.)

**Addition floors.** For 0 ≤ k ≤ p − 1: r_k = (k+1)/((2p−k−1)√(n+1)).

**Truth.** S₀ ⊆ [p] is a fixed set (the support of the true coefficient vector), s₀ = |S₀|. For i ∈ {0, 1}, when S₀ ∈ Ω: R_i = 1/q_i(S₀) − 1.

## 2. Claims

**(i) Deterministic aggregation.** For every partition and positive tables as above and every S° ∈ Ω:
- (i-a) If q < 1, then π₀(S°) ≥ (1−q)^{s+1}/(1+e)^s and 1 − π₀(S°) ≤ (s+1)q/(1−q) + s·e.
- (i-b) q ≤ u. Hence, if u < 1, both bounds of (i-a) hold with u in place of q.
- (i-c) If u < 1, then π₀(S°) ≥ (1−u)^{s+1}/[1 + (2^s − 1)δ^{comp}].

**(ii) Reference-to-truth odds.** Assume S₀ ∈ Ω (i.e. s₀ ≤ K).
- (ii-a) π₀(S₀) = π₀(S°) · [w(s₀)/w(s)] · ∏_b r_b(S₀ ∩ C_b)/r_b(S° ∩ C_b), exactly.
- (ii-b) If moreover S° ⊆ S₀, then π₀(S₀)/π₀(S°) ≥ ∏_{j=0}^{s₀−s−1} r_{s+j} (empty product = 1).
- Remark (interpretive, not a separate mathematical claim): (ii) controls π₀(S₀) only relative to π₀(S°); a lower bound on the normalised reference mass π₀(S°) (e.g. from (i)) is still required.

**(iv) Endpoint propagation.** Assume S₀ ∈ Ω.
- (iv-a) For every φ ∈ [0,1]: 1/q_φ(S₀) − 1 ≤ R₀^{1−φ}R₁^{φ} ≤ max(R₀, R₁), with the convention 0⁰ = 1.
- (iv-b) Hence inf_{φ∈[0,1]} q_φ(S₀) ≥ min{π₀(S₀), π(S₀)}; equivalently sup_{φ∈[0,1]} [1 − q_φ(S₀)] ≤ max{1 − π₀(S₀), 1 − π(S₀)}.
- (iv-c) Consequence (conditional). Consider a sequence of data sets indexed by n → ∞ under a probability P₀. If P₀(S₀ ∈ Ω) → 1, 1 − π(S₀) → 0 in P₀-probability, and 1 − π₀(S₀) → 0 in P₀-probability, then sup_{φ∈[0,1]} [1 − q_φ(S₀)] → 0 in P₀-probability (uniform concentration of the bridge on [0,1]). The two convergence hypotheses are the conclusions of T03 (posterior concentration) and of part (iii) of T22; here they are explicit hypotheses, not results of this run.

## Changes to the statement

Statement check by Astra (session 01a16418-acfd-7cb3-8783-b91d3752db30, reply in review/astra_01_statement_check.log): **APPROVED WITH CORRECTIONS**, 2026-10-22. The corrections are applied below.

Approved changes:
- C1 (added hypothesis): (ii) and (iv) assume S₀ ∈ Ω (s₀ ≤ K). Reason: π₀, q_φ and π are distributions on Ω; if s₀ > K then π₀(S₀) = 0 while the right side of (ii-a) is positive, so (ii-a) is false (instance: n = 3, p = 2, x₁ = x₂ = y = (−1, 0, 1)ᵀ, singleton blocks, S₀ = {1,2}, S° = ∅), and R_i is undefined in (iv). The method's regime R assumes "eventually s₀ ≤ K", so nothing is lost asymptotically. Astra: necessary and minimal (not needed for (iv-b), which is trivial outside Ω).
- C6 (generalisation, recorded at Astra's request): the source's setting is the standardised design and response and the method's complete-linkage/cut/next-fit partition. STATEMENT.md quantifies over all real X, y and all partitions of [p] into blocks with |C_b| ≤ K (and, for (i), all positive tables). This is a strictly more general statement; the source setting is a special case.
- C7 (scope reading): (i-c) is stated under u < 1, the condition the source attaches to substituting u ("u_n < 1 permits its substitution"); the source's "candidate bound" sentence does not repeat it.

Accepted readings:
- C2: the final sentence of the source's (iv), "With T03 and (iii) this gives uniform concentration on [0,1]", is stated as (iv-c) with the conclusions of T03 and (iii) as explicit hypotheses. (Astra notes that the hypothesis P₀(S₀ ∈ Ω) → 1 is redundant given either concentration hypothesis; it is kept, harmlessly.) (iv-c) is a conditional probabilistic consequence of the deterministic (iv-b); "all three parts are deterministic" refers to (i), (ii), (iv-a), (iv-b).
- C3: δ^{comp}'s supremum is taken over feasible S ⊉ S° (a smaller sup, hence a stronger result that implies the reading over all S ⊆ [p]).
- C4: "Normalised reference mass remains essential" is recorded as an interpretive remark, not a claim.
- C5 (provenance, corrected): r_k = (k+1)/((2p−k−1)√(n+1)) is copied verbatim from `theorems/T10_T11_addition_hazard.md`, "Definitions used" ("r_k := (k+1)/((2p−k−1)√(n+1))"); the lead checked this. Astra objected only because T10 was not in its packet; the formula is used here as an explicit definition. All other definitions are transcriptions of the source and 00_COMMON.md, confirmed by Astra.
- No EXP / EXP′ hypothesis is needed for (i), (ii), (iv) (confirmed by Astra).
