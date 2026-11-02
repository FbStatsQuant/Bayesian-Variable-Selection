# W5-B2ENV — PROOF.md: no-method-change masked theorems on LH

Notation of `Docs/Theory/theorems/00_COMMON.md`, W1-EXP `PROOF.md` §§1–4 (cited [E]), W1-T38E `PROOF.md` (cited
[T38E]), W3-VT38E `REPORT.md` §3.1 (cited [V]), W2-PREM `PROOF.md` (cited [P]), W4-SHARE `PROOF.md` (cited [SH]).
Every result is a **candidate**: not reviewed, not adopted. Status words: PROVED, PROOF SKETCH, COUNTEREXAMPLE,
CONJECTURE, OPEN. "PROVED (given X)" means: complete proof here, using the cited candidate result X, whose own status is
stated.

Cited candidate results and their status:
- [E-T1] W1-EXP Theorem 1 (EXP′) and its Lemmas 1.1–1.4: PROVED in W1-EXP, VERIFIED by W3-VEXP. Their proofs use only
  λ_min(R_V) ≥ φ² for the sets V involved and a polynomial count of sets; they apply verbatim to any polynomial family
  of sets of bounded size (noted also by W3-PXN).
- [E-L4] W1-EXP Lemma 4.1 (population algebra of LH) and Lemma 4.2 (blocks = groups): PROVED, VERIFIED.
- [E-T6] W1-EXP Theorem 6 Step 2 (the bound on e_n°): PROVED, VERIFIED.
- [T03] locked T03(i). [E-T5d] W1-EXP Thm 5(d): T03's hypotheses hold on LH (exact Gram).
- [D2] W1-T38E Theorem D2 with W3-VT38E's corrected no-blow-up event NB′ (r* = (11+2√10)/9): PROVED, VERIFIED.
- [T38E-R] W1-T38E Theorem T38(b)-R (composition): PROVED, VERIFIED.
- [IND-T] W2-PREM Theorem IND-T: PROVED (unverified).
- [LA] W1-T38E Lemma A (Gibbs change probability ≤ max endpoint odds; more generally γ_φ(S′)/γ_φ(S) ≤ max(ρ₀, ρ₁)):
  PROVED, VERIFIED.

---------------------------------------------------------------------------------------------------------

## 0. Setting and notation

**LH, exact Gram** ([E] §4.1–4.2). Fixed integers g ≥ 2, c ≥ 1, v ≥ 0; within-group correlations ρ_h ∈ [ρ₋, ρ₊] ⊂ (0,1);
linked pairs (a_i, b_i, ψ_i), 0 < |ψ_i| < min(ρ_{a_i}, ρ_{b_i}); fixed nonzero β_i (pairs) and β_h (visible groups);
σ² > 0 fixed. p = p_n = G_n g ≤ n − 1, X′X = (n − 1)Σ_LH exactly; g ≤ B_n < 2g for all large n (so the v3 blocks are
the groups, [E-L4]). Truth θ_{j_{a_i}} = β_i, θ_{j_{b_i}} = −ψ_iβ_i, θ_{j_h} = β_h (visible), all else 0. S₀ as usual,
M := {j_{b_1},…,j_{b_c}} (masked hubs), S° := S₀ ∖ M, s := |S°| = c + v.

**Units.** Each pair union u_i := C_{a_i} ∪ C_{b_i}, each visible group, each null group. Columns of different units are
orthogonal (exact Gram), μ = Σ_u μ_u with μ_u ∈ span(unit u). 𝒮𝒰 := union of the 2c + v signal units' columns,
u₀ := |𝒮𝒰| = (2c+v)g (fixed).

**Variable classes.** 𝔅 := ⋃_i C_{b_i} (masked hubs and their *proxies*); the **neutral** variables are
𝒩eu := [p] ∖ (S₀ ∪ 𝔅) (non-hubs of a-groups and visible groups, and all null-group members). ν(S) := |S ∩ 𝒩eu|.

**Population residuals.** For V ⊆ [p], Δ(V) := ‖(I − P_V)μ‖²/(n − 1) = θᵀΣθ − (Σθ)_Vᵀ Σ_VV⁻¹(Σθ)_V (exact in exact Gram).
λ₀ := λ_min(Σ_LH) ≥ (1 − max|ψ_i|)(1 − ρ₊) > 0 ([E-L4](a)); hence λ_min(R_V) ≥ λ₀ for every V (interlacing).
R_i := β_i²ψ_i²(1 − ψ_i²) (residual of pair i when only its a-hub is present, [W4-T38FULL §3.4]).

**Zero-leakage facts (exact, deterministic; [E-L4], [P] §8 "ZJL", re-derived in §4.1).**
- (ZL°) every block has zero leakage relative to S°: P_{C_h}μ ∈ span X_{U_h°}, U_h° := S° ∩ C_h ([E] Thm 5(a) proof).
  In particular block C_{b_i} carries no signal: X_{C_{b_i}}ᵀμ = 0.
- (ZJL) for V ⊇ S° and l ∈ 𝒩eu ∖ V: ⟨x_l, (I − P_V)μ⟩ = 0.
- (PZL) for V ⊇ S₀ and k ∈ 𝔅 ∖ V: ⟨x_k, (I − P_V)μ⟩ = 0 (V ⊇ S₀ ⇒ (I − P_V)μ = 0).

**Budgets** (00_COMMON §2). Since p ≤ n − 1: N₀ = max(2500, n), H₀ = ⌈512N₀/2500⌉ ≤ 0.205 max(2500, n) + 1,
T₀ = max(1000, ℓ²) with ℓ = ⌈log₂(n+p+1)⌉, N_e ≤ 4N₀, T_e ≤ 4T₀, L = max(4, ⌈log₂(n+1)⌉).

**Standing data event.** 𝔈_n denotes an event (depending on ε only; X is fixed) with P₀(𝔈_n) → 1, on which the
finitely many uniform estimates listed where used hold. Every "w.p. → 1" below means "on 𝔈_n". The algorithm's
randomness is independent of ε; statements "P(·|data)" are conditional on the data.

---------------------------------------------------------------------------------------------------------

## 1. Lemma OF (orthogonal factorisation of the discrepancy) — PROVED

**Statement.** Let S ∈ Ω and suppose the blocks met by S are mutually orthogonal: X_{C_h}ᵀX_{C_{h′}} = 0 for distinct
blocks h, h′ with S ∩ C_h ≠ ∅ ≠ S ∩ C_{h′}. Put U_h := S ∩ C_h, Y₀ := 2b₀ + yᵀy and κ_h(U) := n z_Uᵀ H_U⁻¹ z_U (κ_h(∅) = 0),
e_h := κ_h(U_h)/Y₀. Then
  (a) log BF(S) = Σ_h [−½ log D_{U_h}] − ν log(1 − Σ_h e_h),  log r_h(U_h) = −½ log D_{U_h} − ν log(1 − e_h);
  (b) d(S) = ν[ −log(1 − Σ_h e_h) + Σ_h log(1 − e_h) ];
  (c) d is non-decreasing in each e_h, and each e_h is non-decreasing in U_h (under inclusion).
  (d) If S′ ⊇ S also meets only mutually orthogonal blocks, 0 ≤ d(S′) − d(S) ≤ ν·(Σ_h e_h(S′) − Σ_h e_h(S))/(1 − Σ_h e_h(S′))
      = ν[Q_S − Q_{S′}]/(2b₀ + Q_{S′}).

**Proof.** (a) G_S = X_SᵀX_S is block diagonal over the met blocks, so H_S = (n+1)G_S + I and G_S + I are block diagonal;
det H_S/det(G_S + I) = ∏_h D_{U_h}, and z_SᵀH_S⁻¹z_S = Σ_h z_{U_h}ᵀH_{U_h}⁻¹z_{U_h}. Hence Q_S = yᵀy − Σ_hκ_h(U_h) and
BF(S) = m(S)/m(∅) = D_S^{−1/2}((2b₀ + Q_S)/(2b₀ + yᵀy))^{−ν} = ∏_h D_{U_h}^{−1/2}(1 − Σ_h e_h)^{−ν}. The table is r_h(U) = BF(U)
(single block), the same formula with one block. (b) d = log BF(S) − Σ_h log r_h(U_h); the determinant terms cancel.
(c) ∂d/∂e_h = ν[1/(1 − E) − 1/(1 − e_h)] ≥ 0 with E := Σ e_{h′} ≥ e_h (all e ≥ 0 because Q_U ≤ yᵀy, 00_COMMON E1(a)
applied with S = ∅). Monotonicity of e_h in U: Q_U = yᵀy − κ_h(U) is non-increasing under inclusion ([T38E] Prop. E1(a)),
so κ_h(U) is non-decreasing. (d) Along the segment from e(S) to e(S′) (coordinatewise increasing), 0 ≤ ∂d/∂e_h ≤ ν/(1 − E),
and E ≤ E(S′) on the segment; integrate. Finally Y₀(1 − E(S′)) = 2b₀ + Q_{S′}. ∎

**Remark.** In LH, the only non-orthogonal block pairs are (C_{a_i}, C_{b_i}). So Lemma OF applies to every S that meets
no C_{b_i} — the S°-side of the start — and fails exactly for states that contain proxies or masked hubs together with
the a-hub, which is where d jumps by Θ(n).

---------------------------------------------------------------------------------------------------------

## 2. NB′ on LH (exact Gram), c = 1, and the no-tweak D2 route

Throughout §2: c = 1, pair (a, b) with hubs j_a, j_b and ψ := ψ₁, β := β₁; v ≥ 0 visible groups; R := β²ψ²(1 − ψ²) > 0.

### 2.1 Start-side aggregation quantities (relative to S°)
For each block h and j ≥ 1 let a_{hj} := Σ_{U: U_h° ⊆ U ⊆ C_h, |U ∖ U_h°| = j} r_h(U)/r_h(U_h°), D_h := max_{j≥1}(j!·a_{hj})^{1/j},
q := p⁻¹Σ_h D_h; e_n := 2p·max_{h, U ⊆ C_h: a := |U_h°∖U| > 0}[r_h(U)/r_h(U ∪ U_h°)]^{1/a} (as in 00_COMMON AGG, with
denominator p instead of p − s; immaterial).

**Lemma 2.1 (aggregation rates). PROVED (given [E-T1], [E-T6]).** On LH (exact Gram, any c), w.p. → 1:
q = O_P(g n^{−1/2}), D_{b} = O_P(g n^{−1/2}) for each masked block b, and e_n ≤ 2n(n+1)^{1/2}e^{κ_EXP}e^{−c₃n} for a
constant c₃ > 0.

*Proof.* Fix h and U ⊇ U_h° with |U ∖ U_h°| = j. By (ZL°), (P_U − P_{U_h°})μ = 0, so RSS_{U_h°} − RSS_U = ‖(P_U − P_{U_h°})Cε‖² =: σ²χ_U,
with χ_U ~ χ²_j exactly. Telescoping [E-T1] along any chain from U_h° to U: on 𝔈_n,
log[r_h(U)/r_h(U_h°)] ≤ −(j/2)log(n+1) + jκ_EXP + ν log(RSS_{U_h°}/RSS_U), and
ν log(RSS_{U°}/RSS_U) ≤ ν σ²χ_U/RSS_U ≤ a χ_U with a := ½σ²/(σ² + Δ₀/2) < ½, where Δ₀ > 0 is the SPREAD constant of
[E] Thm 5(a) (RSS_U ≥ (n−1)(σ² + Δ₀) − n^{3/4} on 𝔈_n, [E] Thm 6 Step 0(ii); n large). Hence
E[a_{hj}1_{𝔈_n}] ≤ C(g,j)(n+1)^{−j/2}e^{jκ_EXP}(1 − 2a)^{−j/2}. By Jensen (x ↦ x^{1/j} concave),
E[D_h1_{𝔈_n}] ≤ Σ_{j=1}^{g}(j!·E[a_{hj}1_{𝔈_n}])^{1/j} ≤ g·C₄n^{−1/2} with C₄ := max_j (j!C(g,j))^{1/j}e^{κ_EXP}(1−2a)^{−1/2}.
Summing over the G_n = p/g blocks and Markov: q = O_P(g n^{−1/2}); the single masked block likewise. e_n: [E-T6] Step 2
verbatim (VIS-lin(S°) holds on LH with c_V = (1 − ρ₊)min{β_i²(1−ψ_i²)², β_h²}, [E] Thm 5(a) proof). ∎

**Lemma 2.2 (start tails). PROVED.** On LH (exact Gram, any c), with p ≥ 2(s + k) and whenever eq ≤ ½:
 (i) π₀({S ⊇ S° : |S ∖ S°| ≥ k}) ≤ 2e^{s}(eq)^k;
 (ii) π₀({S : |S ∖ 𝒮𝒰| ≥ k}) ≤ 2e^{u₀}(e q̃)^k, q̃ := p⁻¹Σ_{null h}D_h ≤ q;
 (iii) π₀({S ⊉ S° : |S ∖ 𝒮𝒰| ≤ k}) ≤ 2^{s}·Σ_{a=1}^{s}e_n^{a} whenever u₀ + k + s ≤ K;
 (iv) for a masked block b, if (s+k)D_b ≤ p: π₀({S ⊇ S° : S ∩ C_b ≠ ∅, |S ∖ S°| ≤ k}) ≤ e(s+k)D_b/p.

*Proof.* Write γ₀(S) = w(|S|)∏_h r_h(S∩C_h)/W_K. (i) For S ⊇ S° with extras P, |P| = k:
Σ_{|P|=k}γ₀(S°∪P)/γ₀(S°) = [w(s+k)/w(s)]·[z^k]∏_h(1 + Σ_{j≥1}a_{hj}z^j). Since a_{hj} ≤ D_h^j/j!, the product is dominated
coefficientwise by exp(zΣ_hD_h) = exp(zpq), so [z^k] ≤ (pq)^k/k!. And w(s+k)/w(s) = ∏_{i<k}(s+i+1)/(2p−s−i−1) ≤ ((s+k)/p)^k
because s + k ≤ K ≤ p. So the ratio is ≤ ((s+k)q)^k/k! ≤ e^{s}(eq)^k (using (s+k)^k/k! ≤ e^{s+k}). Sum over k′ ≥ k and use
γ₀(S°)/Z̄₀ ≤ 1. (ii) The same computation with reference V := S ∩ 𝒮𝒰 (any V ⊆ 𝒮𝒰, |V| ≤ u₀) and only null blocks
contributing extras (null blocks have U_h° = ∅ and zero signal, so their D_h are the same numbers); then sum over the
distinct V, Σ_Vπ₀(V)·(…) ≤ max_V(…). (iii) For S ⊉ S° with A := S° ∖ S ≠ ∅ and S′ := S ∪ A: |S′| ≤ u₀ + k + s ≤ K, so S′ ∈ Ω;
γ₀(S)/γ₀(S′) = [w(|S|)/w(|S|+|A|)]∏_h r_h(U_h)/r_h(U_h ∪ A_h) ≤ (2p)^{|A|}·(e_n/(2p))^{|A|} = e_n^{|A|} by the definition of
e_n and w(k)/w(k+a) ≤ (2p)^a. Each S′ ⊇ S° has at most 2^{s} preimages; sum. (iv) Map S ↦ R := S ∖ C_b; with U := S ∩ C_b ≠ ∅,
γ₀(S)/γ₀(R) = [w(|R|+|U|)/w(|R|)]r_b(U) ≤ ((s+k)/p)^{|U|}r_b(U) (|R| + |U| ≤ s + k ≤ p). Since U_b° = ∅,
a_{bj} = Σ_{|U|=j}r_b(U) ≤ D_b^j/j!, so Σ_{U≠∅}((s+k)/p)^{|U|}r_b(U) ≤ exp{(s+k)D_b/p} − 1 ≤ e(s+k)D_b/p. Distinct S give
distinct pairs (R, U), and Σ_Rγ₀(R)/Z̄₀ ≤ 1. ∎

### 2.2 Theorem NB′-LH — PROVED (given [E-T1], [E-T6], [E-L4])

**Statement.** LH, exact Gram, c = 1, any v ≥ 0, p ≤ n − 1, g ≤ B_n < 2g. Let X₁,…,X_H be the H = H₀ iid π₀ initial
draws of the tier-0 pilot and NB′ := {S₀ ∈ {X_i}} ∪ {ESS of the weights e^{d(X_i)/T₀} is ≥ 0.9H} ([V] §3.1). Put k₀ := 2.
There are constants C, n₀ and an event 𝔈_n with P₀(𝔈_n) → 1 such that on 𝔈_n, for n ≥ n₀,

  P(NB′ᶜ | data) ≤ H·[ 2e^{u₀}(eq̃)³ + 2^{s+1}e_n + 2e^{s}(eq)³ + e(s+2)D_b/p ]
               = O_P( √n/p + n^{−1/2} ).

In particular, if p_n/√n → ∞ then P(NB′ᶜ) → 0, at the rate O(√n/p) (which dominates n^{−1/2} because p ≤ n − 1).

**Proof.** *Good and bad draws.* Let 𝒢 := {S° ∪ P : P ⊆ 𝒩eu, |P| ≤ k₀} (no member of C_b). Every S ∉ 𝒢 ∪ {S₀} lies in
one of: (B1) |S ∖ 𝒮𝒰| > k₀; (B2) S ⊉ S° and |S ∖ 𝒮𝒰| ≤ k₀; (B3) S ⊇ S°, |S ∖ S°| > k₀; (B4) S ⊇ S°, |S ∖ S°| ≤ k₀,
S ∩ C_b ≠ ∅. (If S ⊇ S°, |S∖S°| ≤ k₀ and S ∩ C_b = ∅ then S ∖ S° ⊆ 𝒩eu, i.e. S ∈ 𝒢.) Lemma 2.2 (i)–(iv) with k = k₀ + 1
in (i), (ii) and k = k₀ in (iii), (iv) bounds π₀(B1 ∪ … ∪ B4) by the bracket (for (iii): u₀ + k₀ + s ≤ K for n large, and
Σ_{a≤s}e_n^a ≤ 2e_n once e_n ≤ ½). The union bound over the H iid draws gives P(some X_i ∉ 𝒢 ∪ {S₀} | data) ≤ H·[…].
Rates: Lemma 2.1 and H ≤ 0.21n for n ≥ 2500: H q³ = O_P(n·n^{−3/2}), H e_n → 0 exponentially, H D_b/p = O_P(√n/p).

*d-range on 𝒢.* Every S ∈ 𝒢 meets only C_a, visible groups and null groups, which are mutually orthogonal. By Lemma OF(d)
with S° ⊆ S, 0 ≤ d(S) − d(S°) ≤ ν(Q_{S°} − Q_S)/(2b₀ + Q_S). By Lemma OF(a), Q_{S°} − Q_S = Σ_h[κ_h(U_h) − κ_h(U_h°)], and by
[E] Lemma 1.1 κ_h(U) = (n/(n+1))(t_U − τ_U) with t_U = yᵀP_Uy and 0 ≤ τ_U ≤ 1/((n+1)λ₀). By (ZL°),
yᵀ(P_{U_h} − P_{U_h°})y = ‖(P_{U_h} − P_{U_h°})ε‖²/s_y², and the groups are orthogonal, so
Q_{S°} − Q_S ≤ s_y⁻²‖(P_S − P_{S°})ε‖² + s/((n+1)λ₀). Also s_y²(2b₀ + Q_S) ≥ s_y²RSS^y_S = RSS_S. Let 𝔈_n contain
 (α) max_{P ⊆ [p], |P| ≤ k₀}‖(P_{S°∪P} − P_{S°})ε‖² ≤ 4(k₀ + 1)σ² log n (each is σ²χ²_{|P|}; P(χ²_k > x) ≤ 2^{k/2}e^{−x/4}; at most
     n^{k₀} sets since p ≤ n; the union bound is ≤ 2^{k₀/2}n^{−1} → 0);
 (β) min_{|P|≤k₀}RSS_{S°∪P} ≥ σ²(n−1)/2 ([E] Lemma 1.4's argument over the n^{k₀} sets W = span(X_{S°∪P}, μ), dim ≤ s + k₀ + 1);
 (γ) s_y² ≤ C_R = 2M + 4σ² ([E] Lemma 1.4).
Then for every S ∈ 𝒢: d(S) − d(S°) ≤ (n/2 + 0.01)[4(k₀+1)σ² log n + C_Rs/((n+1)λ₀)]/(σ²(n−1)/2) ≤ 4(k₀+1)log n·(1 + o(1)) =: Δ_n.
So on {all X_i ∈ 𝒢} the weights e^{d(X_i)/T₀} have max/min ≤ e^{Δ_n/T₀}.

*ESS.* Kantorovich ([T38E] Lemma S(ii), constant repaired in [V]): ratio ≤ r* = (11 + 2√10)/9 ⇒ ESS ≥ 0.9H. Now
Δ_n/T₀ ≤ log r* = 0.6549 holds for all n ≥ n₀: T₀ = max(1000, ℓ²) ≥ max(1000, (log₂ n)²) and
12.1·log n ≤ 0.6549·max(1000, (log n/log 2)²) for every n ≥ 3 (for log n ≤ 54 use 1000; for log n > 54 the quadratic term
wins since 0.6549/(log 2)²·log n ≥ 73 > 12.1). So {all X_i ∈ 𝒢 ∪ {S₀}} ⊆ NB′ for n ≥ n₀, which proves the bound. ∎

**Remarks.** (1) The constant 4(k₀+1) = 12 in Δ_n is crude (it is a max over all ≤ k₀-subsets of noise directions); the
sharper Lemma OF form ν·E-increment·(R²-factor) would give ≈ 2(k₀+1)·R²_{S°} log n. Nothing depends on it.
(2) The rate √n/p is real, not an artefact: a draw S° ∪ {k}, k a proxy of j_b, has d(S° ∪ k) − d(S°) = Θ(n) (it captures a
share κ_b = ρ²(1−ψ²)/(1−ψ²ρ²) of the residual R, [W4-T38FULL §3.4]) and π₀-probability ≍ g/(p√n); H such draws are
expected ≍ g√n/p. Once Θ(n) ≫ T₀ log r*, such a draw makes ESS(1/T₀) < 0.9H. So P(NB′ᶜ) ≍ g√n/p up to the
probability that S₀ itself is also drawn (`scripts/s2_nbprime.py`).
(3) Only orthogonality of the S°-side groups and zero leakage relative to S° were used; c = 1 enters through (iv)
(one masked block). For c ≥ 2 the same proof gives NB′ w.p. → 1 under the same rate, but D2 itself needs a one-flip
reference (Gibbs distance 1), so c ≥ 2 is not covered by route (b1′).

### 2.3 Corollary D2-LH (route (b1′), c = 1) — PROVED (given [D2], [E-T1], [E-L4], [E-T5d])

**Statement.** LH, exact Gram, c = 1, v ≥ 0, p ≤ n − 1, g ≤ B_n < 2g, and **p_n/√n → ∞**. Then, under EX-A, EX-S, SR,
P(S₀ ∉ 𝒮_cal) = O(√n/p) + o(1) → 0, where the o(1) is P₀(𝔈_nᶜ) plus exponentially small terms. Consequently, by
[T38E-R] route (b1′) with (P) from [E-T5d]:
  liminf_n P(Uᶜ ∩ {Ŝ = S₀}) ≥ 1 − limsup_n P(U)
for the **original method** (no LS0).

**Proof.** Apply [D2] with x° := S°, j := j_b, 𝒟 := C_b ∖ {j_b} (k_D = g − 1), b := ½, t := 0.2.
(D2-a) x° Δ S₀ = {j_b}, s₀ ≤ K eventually.
(D2-b) 1 − π₀(S°) ≤ π₀(B1 ∪ … ∪ B4) + π₀(S ⊇ S°, 1 ≤ |S∖S°|) ≤ [§2.2 bracket]/H + 2e^{s}eq = O_P(n^{−1/2}) (Lemma 2.2(i), k = 1),
so π₀(S°) ≥ ½ on 𝔈_n.
(D2-c) Dep := Σ_{l ∉ 𝒟 ∪ {j_b}} max(κ₀, κ₁)(S°, l). Additions of neutral l: κ₀(S°, l) = [w(s+1)/w(s)]r_h(U_h°+l)/r_h(U_h°), so
Σ_lκ₀ ≤ ((s+1)/p)·Σ_h a_{h1} ≤ (s+1)q. For κ₁, S° + l meets orthogonal groups, so by Lemma OF(a)
BF(S°+l)/BF(S°) = (D_{U_h°+l}/D_{U_h°})^{−1/2}(1 − δκ_l/(2b₀ + Q_{S°}))^{−ν} with δκ_l = κ_h(U_h°+l) − κ_h(U_h°)
≤ σ²Z_l²/s_y² + 1/((n+1)λ₀), Z_l := u_{U_h°,l}ᵀε/σ ~ N(0,1) (ZL°). [E] Lemma 1.2 gives (D ratio)^{−1/2} ≤ (n+1)^{−1/2}e^{κ_D}.
On 𝔈_n, s_y²(2b₀ + Q_{S°}) ≥ RSS_{S°} ≥ (n−1)(σ² + R) − n^{3/4} (Δ(S°) = R; [E] Thm 6 Step 0(ii) applied to S°) and
max_lZ_l² ≤ 3 log n (union over p ≤ n), so −ν log(1 − x) ≤ νx/(1−x) ≤ a₁Z_l² with a₁ := ½σ²/(σ² + R/2) < ½. Hence
E[Σ_lκ₁1_{𝔈_n}] ≤ ((s+1)/p)·p·(n+1)^{−1/2}e^{κ_D + 1}(1 − 2a₁)^{−1/2} = O(n^{−1/2}). (This is where ψ ≠ 0 matters: R > 0 makes
a₁ < ½, so no truncation is needed.) Deletions of t ∈ S°: κ₀(S°, t) = [w(s−1)/w(s)]r_h(U_h°∖t)/r_h(U_h°) ≤ (2p/s)·e_n/(2p) = e_n/s;
κ₁(S°, t) ≤ (2p/s)·exp{−ν log(RSS_{S°−t}/RSS_{S°}) + κ_EXP + ½log(n+1)} with Δ(S° − t) − Δ(S°) ≥ min{β²(1−ψ²)², min_hβ_h²}
=: m₁ > 0 ([W4-T38FULL §3.4], deletion increases at {a} and at visible {h}; units orthogonal), so κ₁ ≤ e^{−c₅n} on 𝔈_n.
Therefore Dep = O_P(n^{−1/2}).
(D2-d′) NB′: Theorem NB′-LH.
[D2] gives P(S₀ ∉ 𝒮_cal | data) ≤ e^{−2H(0.2)²} + P(NB′ᶜ|data) + exp{−H(1−Dep)₊g(0.3)/(g + B + 2)}, g(0.3) = 0.147; the first and
third terms are exponentially small in n on 𝔈_n (H ≥ 0.2n, B ≤ 16, Dep → 0). The composition is [T38E-R] (b1′) with
(H-T03) from [E-T5d]. ∎

**Masking.** For c = 1, π₀(S₀) = p⁻¹n^{−1/2}e^{O_P(1)} ([E] Thm 5(b)) and Q_f = O(n log²n), so the iid route (a) fails when
p/(√n log²n) → ∞ [W4-T38FULL §3.4]. Corollary D2-LH needs only p/√n → ∞, so it covers the whole c = 1 masked range and
more. It does not cover c ≥ 2 (no one-flip reference).

---------------------------------------------------------------------------------------------------------

## 3. Proposition M-LH (Prop. M(b) on LH: the lattice path is uphill in γ_φ for φ ≥ φ_n → 0) — PROVED (given [E-T1])

**Statement.** LH exact Gram, any c ≥ 1, v ≥ 0, g ≤ B_n < 2g. Lat(S°) := {S° ∪ M′ : M′ ⊆ M}. On an event of probability → 1,
for every S ∈ Lat(S°) and every j = j_{b_i} ∈ M ∖ S:
 (i) start odds: −log(2p/(s+1)) − ½log(n+1) − κ_EXP ≤ log κ₀(S, j) ≤ −log(2p/(s+c)) − ½log(n+1) + κ_EXP + 2 log log n;
 (ii) posterior odds: log κ₁(S, j) ≥ (n/2)·g_*·(1 − o(1)), g_* := min_i log(1 + R_i/(σ² + Σ_{i′}R_{i′})) > 0;
 (iii) hence, with λ_n := log(2p/(s+1)) + ½log(n+1) + κ_EXP and φ_n := λ_n/(λ_n + n g_*/2) = O(log n/n):
     for every φ ∈ [φ_n, 1], γ_φ(S + j)/γ_φ(S) ≥ exp{(φ − φ_n)(λ_n + n g_*/2)} ≥ 1.
In words: under T03's hypotheses there is no posterior-level barrier on the lattice; above φ_n every lattice edge
toward S₀ is uphill and the uphill margin grows linearly in n(φ − φ_n).

**Proof.** (i) S ∈ Lat meets C_{b_i} at most in j_{b_i}; j ∉ S, so S ∩ C_{b_i} = ∅. Hence
κ₀(S, j) = [w(|S|+1)/w(|S|)]·r_{b_i}({j}) with (|S|+1)/(2p−|S|−1) ∈ [(s+1)/(2p), (s+c)/(2p−s−c)]. Block b_i has no signal
(ZL°), so r_{b_i}({j}) = (n+1)^{−1/2}exp{R + ν·(−log(1−x))}, |R| ≤ κ_EXP ([E-T1]), x = σ²Z²/RSS_∅ ∈ [0, 1), Z ~ N(0,1);
the lower bound uses −log(1−x) ≥ 0, the upper bound νx/(1−x) ≤ Z²/(2(1 + o(1))) ≤ 2 log log n on the event
max_{i≤c}Z_i² ≤ 2 log log n (probability → 1, c fixed). (ii) κ₁(S, j) = [w(|S|+1)/w(|S|)]·BF(S + j)/BF(S). [E-T1] applied to
the (finite, c-dependent) family of lattice sets gives log BF(S+j) − log BF(S) = −½log(n+1) − ν log(RSS_{S+j}/RSS_S) + R′,
|R′| ≤ κ_EXP. By unit orthogonality and Δ_{u_i}(S∩u_i + j) = 0, Δ(S) − Δ(S + j) = Δ_{u_i}({j_{a_i}}) = R_i > 0.
RSS_V = (n−1)(σ² + Δ(V)) + O_P(√(n log n)) uniformly over the lattice ([E] Thm 6 Step 0(ii)), so
ν log(RSS_S/RSS_{S+j}) ≥ (n/2)log(1 + R_i/(σ² + Δ(S) − R_i))(1 − o(1)) ≥ (n/2)g_*(1 − o(1)) (Δ(S) ≤ ΣR); the prior
factor and ½ log(n+1) are O(log n) = o(n). (iii) [LA]: log[γ_φ(S+j)/γ_φ(S)] = (1−φ)log κ₀ + φ log κ₁ ≥ −(1−φ)λ_n + φ n g_*/2
(for n large, absorbing (1 − o(1)) into g_*), which is ≥ (φ − φ_n)(λ_n + ng_*/2). ∎

**Use and limits.** Prop. M-LH removes the posterior-level barrier (Prop. X of [SH] cannot bite on the lattice). It says
nothing about states off the lattice (proxies, junk), which is where §4 does the work; route (b2) as proved in §4 does
**not** need Prop. M-LH (the final repair happens at φ = 1).
