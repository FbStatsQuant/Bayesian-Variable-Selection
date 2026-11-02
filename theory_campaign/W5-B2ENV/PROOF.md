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

---------------------------------------------------------------------------------------------------------

## 4. Route (b2) on LH without a method change: confinement + one-round repair

### 4.0 Idea
Choose the delivery region **closed under the favourable dynamics**: all states that contain the visible reference S°,
carry *any* subset of the masked groups 𝔅 (masked hubs and proxies), and at most k neutral extras. Leaving it requires
either deleting a strongly visible truth (odds e^{−Θ(n)} at both endpoints, hence at every φ by Lemma A — this needs the
population margin STAB below) or accumulating junk, and junk is **non-persistent**: every round re-draws each neutral
coordinate, which is kept only with probability O(n^{−1/2}polylog). So the whole particle system stays in the region
for **every grid**, with no SHARE, no LT and no envelope; at φ = 1 every state of the region scores S₀ in one round with
a fixed probability, and N → ∞ independent stage-T rounds finish the job. In D5's language: h_t ≡ 1_𝒩, 𝔛_t = 𝒩,
κ_t ≡ 0, Γ = 0 (§4.6).

### 4.1 Definitions and the population hypothesis
k₀ := 2, k := 16 + 1 + k₀ = 19 (≥ B + 1 + k₀ since B ≤ 16), k₁ := k + 17 + 2k₀ = 40.
  𝒩 := {S ∈ Ω : S° ⊆ S, ν(S) ≤ k},   𝒩′ := {S ∈ Ω : S° ⊆ S, ν(S) ≤ k₁}.
(No constraint on S ∩ 𝔅; |S| ≤ s + cg + k₁ ≤ K for n large.)

**(STAB-LH), a finite population condition on the fixed LH parameters.**
  m_STAB := min{ Δ(V − t) − Δ(V),  Δ(V − t + l) − Δ(V) : S° ⊆ V ⊆ 𝒮𝒰, t ∈ S°, l ∈ 𝒮𝒰 ∖ V } > 0.
Only signal-unit sets matter: adding or removing null-group columns (or any l ∉ 𝒮𝒰) changes no Δ (orthogonal, no
signal), so m_STAB bounds the same differences for every V ⊇ S° in Ω. By exchangeability within groups, m_STAB is a
minimum over count-types (has j_{b_i}?, #C_{a_i}-non-hubs, #proxies, #visible non-hubs), computed exactly in
`scripts/s1_stab.py`.
- It **holds** for configuration A (m_STAB = 0.305) and for, e.g., g ∈ {4, 9, 16} with (ρ, ψ) ∈ {(0.4, 0.2), (0.7, 0.2),
  (0.7, 0.5), (0.85, 0.2)}, with or without a visible group (`s1_stab_types.txt`).
- It **fails** for (ρ, ψ) = (0.85, 0.5) (configuration A85, every g tested: m_swap = −0.005, −0.055, −0.070 at g = 4, 9,
  16) and for configuration B (c = 2): m_swap = −0.18. In a random sweep (c = 1, g = 4, one visible group) it failed in
  66/300 draws. In **every** failure the minimising move is: V contains **all** non-hubs of the group of t (an a-hub or a
  visible hub), and the swap replaces t by a masked hub j_b (of the same pair, or — for c ≥ 2 — of another pair): the
  non-hubs stand in for t and j_b collects residual signal R.
The deletion part (m_del > 0) and the hub gain (§4.2 (G)) held in every case computed.

### 4.2 Uniform one-step estimates — PROVED (given [E-T1])

Let 𝔉 := {V ∈ Ω : |V| ≤ v_max}, v_max := s + cg + k₁ + 2 (λ_min(R_V) ≥ λ₀ on 𝔉). On an event 𝔈_n, P₀(𝔈_n) → 1:

(U1) For V, V + l ∈ 𝔉: log BF(V+l) − log BF(V) = −½log(n+1) − ν log(RSS_{V+l}/RSS_V) + R, |R| ≤ κ_EXP; the same for a
     table within a block. ([E-T1]: Lemmas 1.1–1.3 need only λ_min ≥ λ₀ on the two sets and the RSS floor of Lemma 1.4,
     which holds uniformly over 𝔉 because |𝔉| ≤ n^{v_max}.)
(U2) sup_{V∈𝔉}|RSS_V − ‖Cε‖² − (n−1)Δ(V)| ≤ C√(n log n), and |‖Cε‖² − σ²(n−1)| ≤ σ²n^{2/3}.
     (RSS_V − ‖Cε‖² − (n−1)Δ(V) = 2⟨(I−P_V)μ, ε⟩ − ‖P_Vε‖²; Gaussian tails with variance ≤ 4σ²(n−1)θᵀΣθ and χ²_{|V|}
     tails, union over |𝔉|.)
(U3) If δ_{V,l} = 0 then RSS_V − RSS_{V+l} = σ²Z²_{V,l}, Z_{V,l} := u_{V,l}ᵀε/σ ~ N(0,1). For l ∉ 𝒮𝒰 or l in a unit u(l),
     u_{V,l} depends on V only through V ∩ u(l) (orthogonality); write Z_{U,l}, U ⊆ u(l). There are ≤ p·4^g pairs (U,l).
     On 𝔈_n: max Z²_{U,l} ≤ 2 log(p4^g) + 2 log log n =: z_n² (union bound with P(Z² > 2x) ≤ e^{−x}/√(πx)).

**Lemma J (junk and proxy inclusion odds). PROVED (given (U1)–(U3)).** Put
  q_l := sup{max(κ₀(V, l), κ₁(V, l)) : V ∈ 𝒩′, l ∉ V},  ε_n := Σ_{l∈𝒩eu} q_l,
  ε′_n := max{ max_{l∈𝒩eu}q_l,  sup{κ₁(V, k) : k ∈ C_{b_i}∖{j_{b_i}}, V ∈ 𝒩′, j_{a_i}, j_{b_i} ∈ V, k ∉ V, i ≤ c} }.
Then ε_n = O_P(v_max 4^g √(log n/n)) and ε′_n = O_P(v_max 4^g log n/√n).

*Proof.* Posterior odds of a neutral l at V ∈ 𝒩′: by (ZJL), δ_{V,l} = 0, so by (U1), (U3)
κ₁(V,l) = [w(|V|+1)/w(|V|)]·(n+1)^{−1/2}e^{R}(1 − σ²Z²_{V,l}/RSS_V)^{−ν} ≤ (v_max/p)(n+1)^{−1/2}e^{κ_EXP}exp{νσ²Z²/RSS_{V+l}},
and RSS_{V+l} ≥ ‖Cε‖² − C√(n log n) ≥ σ²(n−1)(1 − η_n), η_n = O(√(log n/n)) (U2, Δ ≥ 0). So the exponent is
≤ ½Z²(1 + 2η_n) and, on {Z² ≤ z_n²}, e^{η_nZ²} ≤ e^{2η_n z_n²} → 1. Hence
  q_l^{(1)} ≤ (v_max/p)(n+1)^{−1/2}e^{κ_EXP+1}·Σ_{U⊆u(l)}e^{Z²_{U,l}/2}1{Z²_{U,l} ≤ z_n²}.
E[e^{Z²/2}1{Z² ≤ z²}] = 2z/√(2π), so E[Σ_l q_l^{(1)}] ≤ v_max(n+1)^{−1/2}e^{κ_EXP+1}4^g·2z_n/√(2π) = O(v_max4^g√(log n/n)); Markov.
Start odds: κ₀(V,l) = [w(|V|+1)/w(|V|)]·r_h(U+l)/r_h(U) with U = V ∩ C_h ⊇ U_h° (V ⊇ S°); (ZL°) makes δ = 0 at block
level and the block RSS is ≥ ‖Cε‖² − C√(n log n); identical computation. Single l, and proxies: on 𝔈_n,
e^{Z²/2} ≤ e^{z_n²/2} = p4^g log n, so each term is ≤ (v_max/p)(n+1)^{−1/2}e^{κ_EXP+1}p4^g log n. For a proxy k of pair i at V
with j_{a_i}, j_{b_i} ∈ V, the residual signal of unit i is 0 (μ_{u_i} ∈ span(x_{j_{a_i}}, x_{j_{b_i}})) and other units are
orthogonal, so δ_{V,k} = 0 and the same bound applies. ∎

**Lemma T (truth retention). PROVED under STAB-LH (given (U1)–(U3)).** On 𝔈_n, for every V ∈ 𝒩′, t ∈ S°, l ∉ V and i ∈ {0,1}:
  γ_i(V − t)/γ_i(V) ≤ 2p·e^{−c₆n},  γ_i(V − t + l)/γ_i(V) ≤ e^{−c₆n},
with c₆ := min{ ¼log(1 + m_STAB/(2(σ² + θᵀΣθ))), ¼log(1 + λ₀γ_min²/(2(σ² + θᵀΣθ))) } > 0, γ_min := min{|β_i|(1−ψ_i²), |β_h|}.
Consequently (Lemma A) for every φ ∈ [0,1] the same bounds hold for γ_φ; the probability that a Gibbs step, a swap step
(acceptance includes a proposal ratio ≤ p for neighbour swaps) or the independence step (S′ ⊉ S° has π₀-mass
≤ π₀(S ⊉ S°)) removes an element of S° from a state in 𝒩′ is ≤ 2p²e^{−c₆n} + π₀(S ⊉ S°).

*Proof.* i = 1: the prior ratio is 1 for swaps and ≤ 2p for deletions. Two applications of (U1) give
log BF(V−t+l) − log BF(V) = −ν log(RSS_{V−t+l}/RSS_V) + R₁ + R₂, and by (U2) and STAB-LH
RSS_{V−t+l}/RSS_V ≥ [σ²(n−1)(1 − o(1)) + (n−1)(Δ(V) + m_STAB)]/[σ²(n−1)(1 + o(1)) + (n−1)Δ(V)] ≥ 1 + m_STAB/(2(σ² + θᵀΣθ))
for n large (Δ(V) ≤ θᵀΣθ). With ν ≥ n/2 this gives ≤ e^{2κ_EXP − 2c₆n} ≤ e^{−c₆n}. Deletion: identical with one step.
i = 0: if l is outside the block h of t, the table ratio factorises; r_h(U − t)/r_h(U) ≤ e_n/(2p) (definition of e_n with
a = 1, U ⊇ U_h°) and the factor for l is ≤ (n+1)^{−1/2}e^{κ_EXP}e^{z_n²(1+o(1))/2} ≤ p4^g log n (Lemma J's computation);
e_n is exponentially small (Lemma 2.1). If l ∈ C_h: tables use the full response, and with U ⊇ U_h° ∋ t, (ZL°) gives
(I − P_U)μ = μ − P_{C_h}μ, so ‖(I − P_{U−t+l})μ‖² − ‖(I − P_U)μ‖² = ‖(I − P_{U−t+l})P_{C_h}μ‖² ≥ (n−1)λ₀γ_t², where
P_{C_h}μ = γ_tx_t (γ_t = β(1−ψ²) for an a-hub, β_h for a visible hub) and the Schur bound of [SH] Prop. M(a) with missing
set {t} is used. Then (U1), (U2) as for i = 1. ∎

(G) **Hub gain** (no hypothesis). For V ∋ j_{a_i} with j_{b_i} ∉ V: Δ(V) − Δ(V + j_{b_i}) = Δ_{u_i}(V ∩ u_i) ≥ λ₀ψ_i²β_i² (unit
orthogonality; Δ_{u_i}(V∩u_i + j_{b_i}) = 0; Schur bound with missing set {j_{b_i}}). Hence, as in Lemma T,
κ₁(V, j_{b_i}) ≥ e^{c₇n} on 𝔈_n for every V ∈ 𝒩′ missing j_{b_i}, and γ₁(V − j_{b_i})/γ₁(V) ≤ 2pe^{−c₇n} if j_{b_i} ∈ V.

### 4.3 Proposition CONF (one-round confinement, uniform in φ and in the state) — PROVED under STAB-LH

**Statement.** On 𝔈_n, for every φ ∈ [0,1] and every x ∈ 𝒩,
  P_x(one round at φ ends outside 𝒩) ≤ a_n := 2mp²e^{−c₆n} + π₀(S ⊉ S°) + 2Σ_{j=0}^{k₀+1}π₀(ν ≥ j)·ε_n^{k₀+1−j}/(k₀+1−j)!,
where m = p + B + 2 and π₀(ν ≥ 0) := 1. With Lemmas 2.1–2.2: a_n = O_P((v_max4^g)^{3}(log n/n)^{3/2}).

**Proof.** Run the round step by step from x. Let τ be the first step whose result leaves 𝒩′ (τ = ∞ if none). Every step
before or at τ acts on a state in 𝒩′.
*Neutral Gibbs inclusions (NGI).* Call an execution of a Gibbs label l ∈ 𝒩eu that ends with l included an NGI. Its
conditional probability given the past, when the current state V is in 𝒩′, is o_l^φ(V) ≤ max{κ₀, κ₁}(V∖l, l) ≤ q_l by
Lemma A (V ∖ l ∈ 𝒩′). The order σ is drawn first and independently; by the chain rule in execution order, for a fixed
set A of neutral labels, P(every label in A makes an NGI at a step ≤ τ) ≤ ∏_{l∈A}q_l, hence
P(at least r NGIs at steps ≤ τ) ≤ Σ_{|A|=r}∏_{l∈A}q_l ≤ ε_n^r/r!.
*Accounting for neutrals.* Every label executes exactly once per round. A neutral l present in the state after step τ′
was put there, at its last membership change, by (α) an NGI, (β) a swap step (at most one added variable per swap
label; at most B + 1 ≤ 17 swap labels), or (γ) the independence step (l ∈ S′, S′ ~ π₀ the proposal). A neutral of the
starting state x whose Gibbs label has not yet executed is also present; there are at most ν(x) ≤ k of them. Hence at
every step ν(current) ≤ k + #NGI + 17 + ν(S′), and at the end of the round (all Gibbs labels executed)
ν(end) ≤ #NGI + 17 + ν(S′)·1{I accepted}.
*Exit.* If the end state is outside 𝒩 then either (a) some step ≤ τ removed an element of S°, or (b) ν exceeded k₁ at τ,
or (c) τ = ∞ and ν(end) ≥ k + 1. (b) needs #NGI + ν(S′) > k₁ − k − 17 = 2k₀ and (c) needs #NGI + ν(S′) ≥ k − 17 + 1
= k₀ + 1; so (b) ∪ (c) ⊆ {#NGI(≤ τ) + ν(S′) ≥ k₀ + 1}. S′ is drawn with fresh randomness and the NGI bound holds
conditionally on it, so P((b) ∪ (c)) ≤ Σ_{j=0}^{k₀+1}P(ν(S′) ≥ j)·ε_n^{k₀+1−j}/(k₀+1−j)! (and ε^r/r! ≤ 2ε^r/r! absorbs
the j-split's boundary). P((a)) ≤ 2mp²e^{−c₆n} + π₀(S ⊉ S°) by Lemma T and a union bound over the m steps (the independence step occurs once
per round, so its term π₀(S ⊉ S°) is not multiplied by m).
Rates: π₀(ν ≥ j) ≤ π₀(S ⊉ S°) + 2e^{s}(eq)^j (Lemma 2.2(i)), π₀(S ⊉ S°) ≤ 2e^{u₀}(eq̃)^{k+1} + 2^{s+1}e_n
(Lemma 2.2(ii)(iii), with k + 1 = 20 null extras in (ii); u₀ + k + s ≤ K), q, q̃ = O_P(n^{−1/2}) and ε_n = O_P(v_max4^g√(log n/n)). ∎

**Corollary CONF-run. PROVED under STAB-LH.** For one final island with N particles and *any* frozen grid with T ≤ T_e
stages, let E := {X_t^i ∈ 𝒩 for all i ≤ N and t = 0, …, T − 1}. On 𝔈_n,
  P(Eᶜ | 𝓒, data) ≤ N π₀(𝒩ᶜ) + N(T − 1)·a_n,  π₀(𝒩ᶜ) ≤ π₀(S ⊉ S°) + 2e^{s}(eq)^{k+1}.
*Proof.* [SH] Prop. X (its main inequality, which this run VERIFIED) with U := 𝒩ᶜ: resampling copies states, so a first
entry into U is an initial draw in U or an end-of-round entry from 𝒩, whose conditional probability is ≤ a_n by
Prop. CONF (each round uses fresh randomness; [IND-T]'s Lemma S makes this rigorous for the shared stream). ∎

With N ≤ N_e ≤ 4max(2500, n) and T_e ≤ 4max(1000, ℓ²): N T_e a_n = O_P(n log²n·(log n/n)^{3/2}) = O_P(log^{3.5}n/√n) → 0.
(This is the only place where k₀ = 2 is needed: k₀ = 1 would give O_P(log³n), not o(1).)

### 4.4 Lemma R1 (one-round repair at φ = 1 from every state of 𝒩) — PROVED under the deletion part of STAB-LH

**Statement.** For x ∈ 𝒩 let M_x := M ∖ x (missing masked hubs), c_x := |M_x|, and
Λ_x := {G_j : j ∈ x ∖ S₀} ∪ {G_k : k ∈ C_{b_i}, j_{b_i} ∈ M_x} (Gibbs labels of x's extras and of the whole groups of the missing
hubs; |Λ_x| ≤ k + cg + cg). Put
  c₀(x) := g^{−c_x} / C(|Λ_x| + B + 2, B + 2),  c₀ := inf_{x∈𝒩} c₀(x) ≥ g^{−c}/C(2cg + k + B + 2, B + 2).
On 𝔈_n, for every x ∈ 𝒩: P_x(S₀ is scored during one round at φ = 1) ≥ c₀(x) − r_n,
  r_n := (s + c)·2pe^{−min(c₆,c₇)n} + ε_n + (|Λ_x| + cg)ε′_n → 0.

**Proof.** If x = S₀ there is nothing to prove (x is a visited state, hence scored, [B] R3). Let O be the order event:
(i) all labels of Λ_x precede all B + 2 non-Gibbs labels, and (ii) for each i with j_{b_i} ∈ M_x, G_{j_{b_i}} precedes the other
g − 1 labels of C_{b_i}. The order is a uniform permutation, so P(O) = g^{−c_x}/C(|Λ_x| + B + 2, B + 2) exactly (the set of
positions occupied by Λ_x ∪ non-Gibbs and the relative order inside Λ_x are independent and uniform). On O, consider the
steps up to the last label of Λ_x; all of them are Gibbs steps. Define the good event 𝒢 on which, at each of these steps:
 – a label of S° keeps its variable (failure ≤ 2pe^{−c₆n} each, Lemma T deletion bound with Lemma A at φ = 1; deletion
   part of STAB-LH);
 – a label of a present masked hub keeps it (failure ≤ 2pe^{−c₇n}, (G));
 – the label of a missing hub j_{b_i} — executed, by (ii), before any other label of C_{b_i}, at a state ⊇ S° in 𝒩′ not
   containing j_{b_i} — adds it (failure ≤ e^{−c₇n}, (G));
 – a label of a neutral variable or of a proxy whose hub is present excludes it (failure ≤ ε′_n each for the ≤ |Λ_x| + cg
   such labels that matter: x's extras and the proxies of the missing groups, which by (ii) execute after their hub;
   the remaining neutral labels executed before the last Λ_x label include nothing, failure ≤ ε_n in total by Lemma J).
On O ∩ 𝒢, right after the last label of Λ_x executes, the state is S° ∪ M ∪ ∅ = S₀, and that Gibbs step evaluated both
configurations (SR), so S₀ is scored. P(O ∩ 𝒢) ≥ P(O) − r_n by the chain rule (each failure bound holds conditionally on
the past and on O, since O only concerns the order). ∎

**Size of c₀.** c₀(S°) = 1/(g^c·C(cg + B + 2, B + 2)): for c = 1, g = B = 4 this is 1/(4·C(10,6)) = 1/840; for g = B = 16,
1/(16·C(34,18)) ≈ 2.8·10⁻¹¹; the uniform c₀ is smaller still. Requiring the *whole* group of a missing hub to act before
the non-Gibbs labels is crude; it is what makes the bound uniform over 𝒩 without any occupancy information. The bound is
asymptotic only; `scripts/s3_b2_run.py` reports the actual per-round scoring frequencies (they are orders of magnitude
larger).

### 4.5 Theorem B2-LH (route (b2), every c, no method change) — PROVED under STAB-LH

**Statement.** LH, exact Gram, any c ≥ 1, v ≥ 0, p ≤ n − 1, g ≤ B_n < 2g, fixed parameters with **STAB-LH**; EX-A, EX-S, SR,
CAL. For every successful calibration 𝓒 (any frozen grid with T ≤ T_e) and one island of the final run with N = N_e
particles, on 𝔈_n:
  P(S₀ ∉ 𝒮 | 𝓒, data) ≤ N π₀(𝒩ᶜ) + N T_e a_n + (1 − c₀ + r_n)^N  →  0,
with rate O_P(log^{3.5}n/√n) + (1 − c₀/2)^{n}. Consequently, by [T38E-R] (route (b2), with DELIV+REPAIR replaced by this
bound) and (P) from [E-T5d]:
  liminf_n P(Uᶜ ∩ {Ŝ = S₀}) ≥ 1 − limsup_n P(U)  for the original method (no LS0).

**Proof.** On E (Corollary CONF-run), every stage-T resampled particle is a copy of some X_{T−1}^i ∈ 𝒩. The stage-T round
is at φ_T = 1. Conditionally on F_{T−1} and the stage-T resampling, the N stage-T rounds are independent, each with the
one-round kernel at φ = 1 started at the particle's state ([IND-T], Lemma S: the blocks of the shared stream are read in
order, each block's law given the past is the kernel at the particle's own state). By Lemma R1 each scores S₀ with
conditional probability ≥ c₀ − r_n, so P(no stage-T round scores S₀ | E, …) ≤ (1 − c₀ + r_n)^N. Add P(Eᶜ). For the
composition: P(Uᶜ, S₀ ∉ 𝒮) ≤ E[min(1, bound)·1_{𝔈_n}] + P₀(𝔈_nᶜ) → 0 by bounded convergence (the bound → 0 in
P₀-probability; N ≥ n). [T38E-R] steps (1)–(2) and (P) give the conclusion. ∎

**What this theorem does not need.** No masking condition (it holds whether or not π₀(S₀) → 0), no p → ∞, no condition
on the grid, no SHARE, no evidence lower tail, no envelope (Γ = 0), no LS0, no occupancy statement, and no T24/B♯
progress premises (FS gap, ULR): the one-round order event replaces them. It needs **STAB-LH** (a finite population
inequality) and the v3 budgets only through N T_e a_n → 0 and N → ∞.

**Regime check.** Combined with W1-EXP Thm 5(b), for c ≥ 2 (and c = 1 with p/(√n log²n) → ∞) the iid route fails and
the start is masked; Theorem B2-LH then gives the masked-regime HPM consistency of the original method on LH, for every
c, whenever STAB-LH holds (e.g. configuration A, c = 1; any g ∈ {4, 9, 16} with ρ ≤ 0.85, ψ = 0.2 or ρ ≤ 0.7, ψ = 0.5).
For c = 2, `scripts/s1b_stab_c2.txt` (two pairs, no visible group, g ∈ {4, 9}, ρ ∈ {0.4, 0.7, 0.85}, ψ ∈ {0.1, 0.2, 0.35,
0.5}, two coefficient choices): STAB-LH holds in 38/46 settings, e.g. every ψ ≤ 0.2 and every ρ = 0.4; all 8 failures have
ψ ≥ 0.35 and ρ ≥ 0.7, and the failing move is again "a-hub of one pair → masked hub of the other pair" at states holding
all non-hubs of that a-group. So Theorem B2-LH has masked c = 2 instances (with p → ∞, π₀(S₀) = p^{−2}n^{−1}e^{O_P(1)}).

### 4.6 Relation to W4-SHARE's envelope (D4/D5), and the clean negative for lattice potentials

**(a) The instance above is D5 with Γ = 0.** Take h_t ≡ 1_𝒩, W := 𝒩, 𝔛_t := 𝒩 and η_t := a_n. Then (TRACK) holds
(Prop. CONF), E is D5's confinement event, and κ_t can be taken 0 (there are no states in 𝔛_t with h < 1: empty sup),
so Γ = 0 and D5's conclusion is trivial on E. All the content sits in P(Eᶜ) — a Prop. X union bound — and in the
repair (Lemma R1). So on LH the envelope machinery is **not needed**: the right potential makes it degenerate.

**(b) The lattice-indicator potential of the task brief cannot certify delivery at any budget (PROOF SKETCH).** Take
c = 1, h_t := 1_{{S°, S₀}} for φ_t < φ* and 1_{{S₀}} for φ_t ≥ φ* (any switch point φ*), W := {S°, S₀} (or {S₀}), and any
confinement sets 𝔛_t that contain the states the particles actually visit. Two outsider classes appear:
 – *junk carriers* S° ∪ {l} and S₀ ∪ {l}: each round creates them with probability ≈ Σ_lκ_φ(·, l) ≍ n^{−1/2}, the fittest
   null l* (Z²_{l*} ≈ 2 log p) is added with probability ≍ n^{−1/2}·e^{Z²/2}/(2p) ≍ n^{−1/2} per particle-round, so over
   N T ≍ n log²n particle-rounds it is visited w.p. → 1. By Lemma OF, d(S° ∪ l*) − d(S°) = ϰ·Z²_{l*}/2·(1+o(1)),
   ϰ := σ²(θᵀΣθ − R)/((σ² + θᵀΣθ)(σ² + R)) ∈ (0,1); so κ_t ≥ ϰ log p (1 + o(1)) at every stage and Γ ≥ ϰ log p.
 – *early crossers* S₀ (and S₀ ∪ junk) before the switch: if h_{t−1} gives S° weight 1, the outsider-vs-insider gap is
   d(S₀) − d(S°) = n g_*/2·(1 + o(1)) (Prop. M-LH). The first S₀-particles appear as soon as N·T·κ_φ(S°, j_b) ≳ 1, i.e. at
   φ ≈ φ_n − log(NT)/(λ_n + ng_*/2), and the switch must wait until the j_b-odds exceed 1/η (φ* ≥ φ_n + log(1/η)/(λ_n + ng_*/2))
   for the switch-stage exit η to be small. Over that window Σ_tΔ_tκ_t ≥ (n g_*/2)·(log(NT) + log(1/η))/(λ_n + ng_*/2)
   = (log(NT) + log(1/η))(1 − o(1)). If instead S₀ is given weight 1 from the start, the junk outsiders above remain and
   the switch is unnecessary but then h_{t−1}(S°) = 1 keeps inf d at d(S°) while S₀-side junk carriers sit Θ(n) higher.
So any lattice-type potential has Γ + Σ_tη_t ≥ log(NT) − O(1), while D5 needs Γ + Σ_tη_t ≤ log(Nπ₀(h₀)/T) − ω(1). The
certificate fails by ≥ 2 log T for **every** N: enlarging N_e (a budget sequence) does not help, because the early
crossers that create the oscillation multiply with N. The obstruction is the *choice of potential*, not the dynamics:
the region must be closed under the favourable moves (§4.0). (Status: PROOF SKETCH; the visit claims are first-moment
heuristics made rigorous only for the expected counts.) **Numerics** (`scripts/s3_b2_run.txt`, configurations A and A85,
n ∈ {400, 1600, 6400}, method grid with T = 14–16): the realised Γ of the lattice potential is 6.2–9.9 (median per
setting), against D5's allowance log(N/T_e) = 0.9–1.9 and log(NT) = 10.5–11.5 — the certificate fails as predicted —
while delivery and scoring succeed in every island and the realised envelope barely moves (min_t log P_t ≥ −0.31). D5's
worst-case κ is very pessimistic here; the realised r_t stays ≈ 1. For h = 1_𝒩 the realised Γ is 0 in every island.

**(c) What a budget sequence would buy.** Nothing for (b). For §4.5, larger N only improves (1 − c₀)^N, while N T_e a_n
must still → 0: N_n = o(n^{3/2}/log^{3.5}n) keeps confinement with k₀ = 2, and larger N needs a larger k₀ (k₀ with
N T_e ε_n^{k₀+1} → 0), which costs nothing but a larger k in 𝒩 (and a smaller c₀).

### 4.7 What is open when STAB-LH fails
If m_STAB < 0, the posterior prefers, at some states of 𝒩 carrying all non-hubs of a truth t's group, to swap t for a
masked hub. For φ close to 1, γ_φ(V − t + j_b)/γ_φ(V) ≈ e^{−Θ(n)(1−φ) + Θ(n)φ}, so the uniform swap (and, when j_b ∈ N(t),
the neighbour swaps) can leave 𝒩. The exit is transient (at φ = 1 the posterior re-adds t at the next Gibbs update of t),
but confinement as stated fails. Two repairs are plausible and OPEN: (1) enlarge 𝒩 to allow one missing S°-truth
together with ≥ g − 2 of its group's non-hubs, and extend Lemma R1 to re-add t; (2) show that states carrying ≥ m*
non-hubs of a truth's group are visited with negligible probability (each such non-hub is neutral, so it needs an NGI or
a swap-add, and swap-adds of C_a non-hubs come only from neighbour swaps out of proxies). Route (2) needs an occupancy
bound for the transient proxy states, which is exactly what this proof avoided.

---------------------------------------------------------------------------------------------------------

## 5. LH-iid (p ≫ n): remarks only
- NB′: the proof of §2.2 uses exact orthogonality of the S°-side groups (Lemma OF). On LH-iid the groups are only
  approximately orthogonal (sample cross-correlations O_P(√(log p/n))); the d-range on 𝒢 then picks up cross terms of
  order n·(log p/n) = log p per pair of touched groups, still O(log n) ≪ T₀ log r*. On LH-iid p ≥ n, so H ≍ p and the
  proxy term H·g/(p√n) ≍ g/√n → 0 automatically: P(NB′ᶜ) = O(g n^{−1/2}) is expected, with W3-PXN's Beta-law aggregation
  bounds replacing Lemma 2.1. CONJECTURE (not written).
- Route (b2): Lemma J and Lemma T used exact zero leakage (ZJL) and exact unit orthogonality. On LH-iid, ZJL holds only
  in population; the sample leakage δ_{V,l} = O_P(√(log p)) (W3-PXN's Beta laws) is of the same order as the noise and
  is absorbed by the truncation exactly as in W3-PXN Lemma Tr. CONJECTURE (not written).
