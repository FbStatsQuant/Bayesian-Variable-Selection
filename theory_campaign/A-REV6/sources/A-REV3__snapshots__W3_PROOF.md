# W3-PXN — PROOF.md: one p ≫ n family carrying all of T38(b)'s premises jointly

Notation of `Docs/Theory/theorems/00_COMMON.md`, of the T22/T27 locked statements, and of W1-EXP / W1-T38E / W1-T37R.
Every result is a **candidate pending cross-family review**. Status words: PROVED, PROOF SKETCH, COUNTEREXAMPLE,
CONJECTURE, OPEN. "Cited" means a result of another run or of the locked register, whose status is stated where used.

Cited results and their status:
- **[T22i], [T22ii]**: locked T22(i-a), (ii-a) (PROVED-LOCKED, deterministic; any partition, positive tables).
- **[T03]**: locked T03(i) (PROVED-LOCKED): under G, R, SE, BM-∞, 1 − π(S₀) = O_P(√(log n/n)).
- **[EXP-L1.1], [EXP-L1.2], [EXP-L1.4], [EXP-T1]**: W1-EXP Lemmas 1.1, 1.2, 1.4 and Theorem 1 (EXP′) (candidate PROVED in W1-EXP).
  Their proofs use only λ_min(G_A) ≥ φ²(n−1) for the sets involved and a polynomial count of sets; they apply
  verbatim to any polynomial family of sets of bounded size, not just within-block sets (checked line by line for this run).
- **[T37R-A]**: W1-T37R Theorem A(A3), lattice version (candidate PROVED).
- **[T38E-D2], [T38E-E3], [T38E-R]**: W1-T38E Theorem D2, Theorem E3, Theorem T38(b)-R (candidate PROVED).
- **[CONC]**: a standard Gaussian concentration fact (Lemma C1 below), cited from the literature.

New symbols are defined where introduced.

---------------------------------------------------------------------------------------------------------

## 0. The family LH-iid

**Fixed parameters.** Integers g ≥ 2, c ≥ 1, v ≥ 0; ρ ∈ (0,1); ψ₁,…,ψ_c with 0 < |ψ_i| < ρ; nonzero β₁,…,β_c (pairs)
and β^vis_1,…,β^vis_v (visible groups); σ² > 0. Exponents 1 ≤ a ≤ A (p ≫ n is a > 1).

**Design.** p = p_n = G_n g with n^a ≤ p_n ≤ n^A. The index set is cut into G_n groups C_1,…,C_{G_n} of size g; the
first member of each group is its *hub* j_h. Groups 1..2c form c *linked pairs* (a_i, b_i) = (2i−1, 2i); groups
2c+1..2c+v are *visible*; all other groups are *null*. Rows of X^r are iid N(0, Σ), with Σ = Σ_LH the W1-EXP linked-hub
correlation:
- within each group: equicorrelation ρ (unit diagonal);
- distinct groups independent, except that for each pair i, Σ[C_{a_i}, C_{b_i}] = ψ_i Σ[C_{a_i}, j_{a_i}] Σ[j_{b_i}, C_{b_i}]
  (rank one through the hubs; corr(j_a, j_b) = ψ, corr(j_a, k) = ψρ (k ∈ C_b∖j_b), corr(k′, k) = ψρ² off hubs).

**Truth.** θ_{j_{a_i}} = β_i, θ_{j_{b_i}} = −ψ_iβ_i (the *suppressor*), θ_{j_h} = β^vis_h for visible groups, all other
coefficients 0. y^r = X^rθ + ε, ε ~ N(0, σ²I_n) independent of X^r. Hence s₀ = 2c + v (fixed),
S₀ = {j_{a_i}, j_{b_i}}_i ∪ {visible hubs}, the masked set M = {j_{b_1},…,j_{b_c}}, the reference
**S° := S₀ ∖ M** (s := |S°| = c + v), and S₀ = S° ∪ M.

**Block parameter.** B_n = min(⌊√n⌋, ⌊√p⌋, 16) and we require **g ≤ B_n < 2g** for all large n. Since B_n = 16 once
n ≥ 256, this means **9 ≤ g ≤ 16** asymptotically (any g with g ≤ B < 2g at a given finite n).

**Population facts** (W1-EXP Lemma 4.1, re-derived here because they are used repeatedly). For every pair i:
- (F1) Σ[C_{b_i}, j_{a_i}] = ψ_iΣ[C_{b_i}, j_{b_i}] and Σ[C_{a_i}, j_{b_i}] = ψ_iΣ[C_{a_i}, j_{a_i}].
- (F2) Cov(X_{C_{b_i}}, μ_i) = 0 where μ_i := β_i(x_{j_{a_i}} − ψ_i x_{j_{b_i}}) (by F1).
- (F3) Conditional independence: C_{a_i} ⊥ C_{b_i} | x_{j_{a_i}} (Cov(X_{C_a}, X_{C_b} | x_{j_a}) = ψΣ[C_a,j_a]Σ[j_b,C_b]
  − Σ[C_a,j_a]·ψΣ[j_b,C_b] = 0, using Σ[j_a, C_b] = ψΣ[j_b, C_b] from F1) and symmetrically C_{a_i} ⊥ C_{b_i} | x_{j_{b_i}}.
- (F4) λ₀ := λ_min(Σ) ≥ (1 − max_i|ψ_i|)(1 − ρ) > 0 (W1-EXP Lemma 4.1(a): Cauchy–Schwarz in the Σ_aa-inner product).
- (F5) **Components.** Put K_i := C_{a_i} ∪ C_{b_i}, V_h := C_h (visible). The components K_1,…,K_c, V_1,…,V_v and the
  null groups are mutually independent, and μ := X^rθ = Σ_i μ_i + Σ_h β^vis_h x_{j_h}.

**Neutral variables.** l is *neutral* if l ∉ S₀ and l ∉ ∪_i C_{b_i} (null-group members, non-hub members of the
a-groups and of the visible groups). The non-neutral non-truths are the *proxies* C_{b_i}∖{j_{b_i}} of the masked hubs.

**Standing event.** 𝒜_n := {blocks = groups} ∩ {SE-type events of Lemma P2} ∩ {‖μ‖²/n ≤ M}, with M := 2θᵀΣθ + 1.
It is X-measurable, and P(𝒜_n) → 1 (Lemmas P1, P2).

---------------------------------------------------------------------------------------------------------

## 1. Concentration

**Lemma C1 [CONC] (cited, standard).** For iid N(0, Σ) rows with unit-diagonal Σ and log p = o(n), the sample
correlations satisfy max_{j<k}|r̂_jk − Σ_jk| ≤ C₁√(log p/n) w.p. → 1, for a constant C₁ depending only on A.
(E.g. Bickel & Levina 2008, Ann. Statist. 36, Lemma A.3 for covariances; the passage to correlations is the usual
ratio argument with the diagonal entries.) Not re-proved here.

**Lemma C2 (PROVED).** For any T ⊆ [p], ‖R̂_T − Σ_T‖_op ≤ |T|·max_{j,k∈T}|r̂_jk − Σ_jk|.
*Proof.* ‖E‖_op ≤ ‖E‖_F ≤ |T|·max|E_jk|. ∎

**Lemma C3 (PROVED).** Let 𝒮𝒱 := ∪_i K_i ∪ ∪_h V_h (a fixed finite index set, |𝒮𝒱| = g(2c+v)). All sample moments of
the finitely many columns X^r_{𝒮𝒱}, ε converge a.s. to their population values (SLLN); in particular every
sample partial correlation among finitely many of these columns and y converges a.s. ∎

---------------------------------------------------------------------------------------------------------

## 2. Lemma P1 (the v3 partition equals the groups) — PROVED (given C1)

**Statement.** On LH-iid, P(the v3 partition = {C_1,…,C_{G_n}}) → 1.

**Proof.** *Deterministic part.* Let d_jk = 1 − |r̂_jk|, D_in := max over pairs in a common group of d_jk, and
D_out := min over pairs in different groups of d_jk. Suppose **D_in < D_out** and **g ≤ B < 2g**.
(a) *Each group is a dendrogram node.* Induction on merges: all current clusters are subsets of groups. If some group
is not yet a single cluster, two of its clusters are at complete-linkage distance ≤ D_in, while any two clusters
lying in different groups are at distance ≥ D_out (complete linkage is the maximum of pairwise distances, each ≥ D_out).
So the closest pair (ties broken by any rule, R13 included) lies in a common group; the invariant persists until
every group is one cluster. Hence the dendrogram is laminar with respect to the groups: every node is either a subset
of a group or a union of whole groups.
(b) *Top-down cut.* A node that is a union of ≥ 2 groups has size ≥ 2g > B and is split; a group node has size
g ≤ B and is retained; no proper ancestor of a group node is retained. So the retained clusters are exactly the groups.
(c) *Next-fit packing.* A bin holding one group (g members) cannot accept another (2g > B). So blocks = groups.
*Probabilistic part.* Population within-group |corr| = ρ; population cross-group |corr| ∈ {0, |ψ_i|, |ψ_i|ρ, |ψ_i|ρ²}
≤ max|ψ_i| < ρ. With η := (ρ − max|ψ_i|)/3 > 0 and C1, w.p. → 1 every within-group |r̂| ≥ ρ − η and every
cross-group |r̂| ≤ max|ψ_i| + η < ρ − η, i.e. D_in < D_out. ∎

*Remark (what the hypothesis g ≤ B < 2g buys).* See §13: if 2g ≤ B, complete linkage co-blocks each linked pair and
masking disappears. This is why the family uses groups of 9–16 rather than the study's groups of 5.

---------------------------------------------------------------------------------------------------------

## 3. Lemma P2 (G, R, SE, SE-blk, anchored SE, BM-∞) — PROVED (given C1)

**Statement.** On LH-iid, with φ₀² := λ₀/2, each of the following holds w.p. → 1:
(a) **SE** in the locked form: λ_min(R̂_T) ≥ φ₀² for every nonempty T with |T| ≤ min(p, m_n + s₀), where
    m_n = ⌈(s₀ log 2p + (s₀+1)(log n)/2 + ½ log n)/log 2⌉ = O(log n);
(b) hence **SE-blk(φ₀)**, W1-T03R's **SE_λ(j₀)** and **SE_w(m♯_n; g₀)** for any g₀ > 0 (all are restrictions of (a),
    since j₀ and m♯_n ≤ m_n are O(log n)), and λ_min(R̂_{S₀}) ≥ φ₀²;
(c) **R**: s₀ fixed, p ≤ n^A, ‖μ‖²/n ≤ M, s₀ ≤ K = ⌊n/2⌋;
(d) **BM-∞**: min_{j∈S₀} θ*_j² ≥ b₀ := ½ min(|β_i|²ψ_i², |β_i|², |β^vis_h|²) > 0, so BM-∞ holds with M_n := b₀nφ₀²/(σ² log n) → ∞;
(e) **G** holds conditionally on X (ε ~ N(0, σ²I) independent of X^r).

**Proof.** (a) By C2 and C1, for |T| ≤ k_n := m_n + s₀ = O(log n): λ_min(R̂_T) ≥ λ_min(Σ_T) − k_nC₁√(log p/n)
≥ λ₀ − O(log^{3/2} n/√n) ≥ λ₀/2 eventually (λ_min(Σ_T) ≥ λ_min(Σ) by interlacing). (b) Restrictions. (c) ‖μ‖²/(n−1) =
θ*ᵀR̂_{S₀}θ* with θ*_j = β*_j·sd_j (00_COMMON: θ* = D_xβ*), and R̂_{S₀} → Σ_{S₀}, sd_j → 1 a.s. (C3). (d) θ*_j → θ_j a.s.
(e) Definition of the model. ∎

---------------------------------------------------------------------------------------------------------

## 4. Lemma B (exact Beta laws of the start statistics) — PROVED

For a set A ⊆ [p] write Π_A^⊥ := C − P_A (projection onto 1^⊥ ⊖ span X_A; X is centred), RSS_A := ‖Π_A^⊥Y‖²,
Y = Cy^r. For a group h put U_h° := S° ∩ C_h (= {j_h} for a-groups and visible groups, ∅ for b-groups and null groups).
For V ⊆ C_h∖U_h° nonempty define the *block explained fraction*
  X_{h,V} := 1 − RSS_{U_h°∪V}/RSS_{U_h°}.
For a set A ⊇ S° with A∖S° neutral and a neutral l ∉ A define x_{A,l} := 1 − RSS_{A+l}/RSS_A.

**Statement.** (i) X_{h,V} ~ Beta(|V|/2, (n−1−|U_h°|−|V|)/2) whenever n − 1 − |U_h°| − |V| ≥ 1.
(ii) x_{A,l} ~ Beta(½, (n−2−|A|)/2) whenever n − 2 − |A| ≥ 1.
(iii) The masked hubs: the c columns x^r_{j_{b_i}} and the vector y^r are mutually independent; consequently
(n−1)·(r̂_{j_{b_1},y}², …, r̂_{j_{b_c},y}²) →_d (χ²_{1,1}, …, χ²_{1,c}) independent, where r̂_{j,y} is the sample correlation.

**Proof.** *Key covariance identity.* Let W be one of the following column sets with conditioning set U:
(α) W = V ⊆ C_h∖U_h°, U = U_h°; (β) W = {l}, U = A. In both cases, Cov(x_w, μ | X_U) = 0 for every w ∈ W
(population partial covariance, row-wise):
- null group: x_w is independent of all truth-carrying columns.
- b-group, U = ∅: Cov(X_{C_b}, μ) = Cov(X_{C_b}, μ_i) = 0 by (F2), other components independent.
- a-group, U ∋ j_a (case α: U = {j_a}; case β: U ⊇ {j_a} ∪ (other neutral members of C_a)): given X_U, the only part of
  μ correlated with C_a is μ_i, whose X_U-conditional randomness is −ψβx_{j_b}; and x_w ⊥ x_{j_b} | X_U by (F3) and the
  weak-union property of conditional independence (C_a∖{j_a} ⊥ C_b | x_{j_a} implies x_w ⊥ x_{j_b} | (x_{j_a}, X_{U∩C_a}).
- visible group, U ∋ j_h: Cov(x_w, β_h x_{j_h} | X_U) = 0 because x_{j_h} ∈ X_U; other components independent.
- case β with A containing members of several components: the components are independent (F5), so the statement reduces
  to the component of l.
*Independence.* Let W^r := X^r_W − X^r_UΓ (Γ = Σ_UU⁻¹Σ_UW, the population regression). Rows of (W^r, X^r_U, X^r_{S₀}, ε)
are iid jointly Gaussian; Cov(W^r, X^r_U) = 0 by construction and Cov(W^r, X^r_{S₀}θ) = Cov(X_W, μ | X_U) = 0 by the
identity; ε is independent of X. Hence W^r is independent of (X^r_U, y^r) (for case α also of nothing else needed).
*Geometry.* Standardisation multiplies columns by positive scalars and centres them, so
span((C − P_U)X_W) = span((C − P_U)X^r_W) = span((C − P_U)W^r), because (C − P_U)X^r_U = 0 (CX^r_U spans span X_U).
Let E := 1^⊥ ⊖ span X_U (dimension m = n − 1 − |U| a.s.); C − P_U = Π_E. Conditionally on (X^r_U, y^r), the vector
r := Π_E Y is fixed and nonzero a.s., and Π_E W^r = Π_E G Σ_{W|U}^{1/2} with G an n × |W| iid N(0,1) matrix independent
of E and r; Q_EᵀG is an m × |W| iid Gaussian matrix (Q_E an orthonormal basis of E), so span(Π_E W^r) is Haar-distributed
on the Grassmannian of |W|-planes of E (a.s. of full dimension). Since C − P_{U∪W} = Π_E − P_{span Π_E W^r},
1 − RSS_{U∪W}/RSS_U = ‖P_{span}r‖²/‖r‖², the squared length of the projection of a fixed unit vector onto a uniform
random |W|-plane of an m-dimensional space: Beta(|W|/2, (m − |W|)/2). This gives (i) and (ii).
(iii) Cov(x_{j_{b_i}}, x_{j_{b_k}}) = 0 (i ≠ k, independent components), Cov(x_{j_{b_i}}, y^r) = Cov(x_{j_{b_i}}, μ_i) = 0 (F2):
the c + 1 Gaussian vectors are uncorrelated, hence independent. Given y, the unit vectors u_i := Cx_{j_{b_i}}/‖Cx_{j_{b_i}}‖
are iid uniform on the unit sphere of 1^⊥ (dimension n − 1), so the √(n−1)r̂_i = √(n−1)⟨u_i, Y/‖Y‖⟩ are iid with the law of
√(n−1) times one coordinate of a uniform point of S^{n−2}, which → N(0,1). ∎

---------------------------------------------------------------------------------------------------------

## 5. Lemma Tr (truncated moment and tail of the Beta statistics) — PROVED

**Statement.** Let X ~ Beta(j/2, (m−j)/2), 1 ≤ j ≤ 16, m = n − 1 − u with 0 ≤ u ≤ 16, ν = 0.01 + n/2, τ ∈ (0, ½].
(a) E[(1 − X)^{−ν}1{X ≤ τ}] ≤ 2^{e₁}(mτ/2)^{j/2}/Γ(j/2 + 1), e₁ := (u + j + 3)/2 + 0.01.
(b) P(X > τ) ≤ exp(−(m−j)/16) + P(χ²_j > τ(m−j)/2).
(c) With τ_n := t_n/n, t_n := 4(A + 3) log n, and any family of at most n^{A+1}·2^{17} such variables (not necessarily
independent), P(max X > τ_n) → 0.

**Proof.** (a) The Beta density is x^{j/2−1}(1−x)^{(m−j)/2−1}/B(j/2, (m−j)/2). The integrand of the truncated moment is
x^{j/2−1}(1−x)^{(m−j)/2−1−ν} and (m−j)/2 − 1 − ν = −e₁ < 0, so (1−x)^{−e₁} ≤ (1−τ)^{−e₁} ≤ 2^{e₁} on [0, τ].
∫₀^τ x^{j/2−1}dx = (2/j)τ^{j/2}. Finally 1/B(j/2,(m−j)/2) = Γ(m/2)/(Γ(j/2)Γ((m−j)/2)) and
Γ(y + a)/Γ(y) ≤ (y + a)^a for y > 0, a = j/2 (integer a: product of a factors ≤ y + a; half-integer a = k + ½: Wendel's
inequality Γ(z+½)/Γ(z) ≤ z^{1/2} with z = y + k, times the integer case). With y + a = m/2:
E ≤ 2^{e₁}(2/j)τ^{j/2}(m/2)^{j/2}/Γ(j/2) = 2^{e₁}(mτ/2)^{j/2}/Γ(j/2+1).
(b) X = χ²_j/(χ²_j + χ²_{m−j}) with independent chi-squares, so X ≤ χ²_j/χ²_{m−j}; on {χ²_{m−j} ≥ (m−j)/2},
X > τ forces χ²_j > τ(m−j)/2. Laurent–Massart: P(χ²_k ≤ k − 2√(kx)) ≤ e^{−x}; take x = k/16.
(c) τ_n(m−j)/2 = (t_n/2)(1 − O(1/n)) =: t′. Laurent–Massart upper tail: P(χ²_j ≥ j + 2√(jx) + 2x) ≤ e^{−x}; choose
x = t′/2 − √(jt′) − j (positive for large n), so P(χ²_j > t′) ≤ exp(−t_n/4 + O(√log n)) = n^{−(A+3)}e^{O(√log n)}.
Union bound: n^{A+1}2^{17}[n^{−(A+3)}e^{O(√log n)} + e^{−(n−34)/16}] → 0. ∎

---------------------------------------------------------------------------------------------------------

## 6. Theorem P3 (near-truth start mass on the reference S°) — PROVED

**Statement.** On LH-iid (any c ≥ 1, any 1 ≤ a ≤ A): with q, e the T22(i) aggregation quantities of S° on the actual
blocks,
  q = O_P(√(log n/n)),  e = O_P(p√n·e^{−c₆n}) for a constant c₆ > 0,
and therefore
  **1 − π₀(S°) ≤ (s+1)q/(1−q) + s·e = O_P(√(log n/n))**, in particular π₀(𝓡_d) ≥ π₀(𝓡₀) ≥ π₀(S°) → 1 for every d ≥ 0
(near-truth start mass b_n = 1 − O_P(√(log n/n)), with reference S° ∈ 𝓡₀).

**Proof.** Work with the group-defined quantities ã_hj, D̃_h, q̃, ẽ (the T22 definitions with blocks replaced by groups);
on 𝒜_n they equal the actual a_bj, D_b, q, e. Let E_n be the event of [EXP-T1] (W1-EXP Theorem 1; the RSS-floor event of
[EXP-L1.4], whose probability bound is uniform over designs satisfying SE-blk and R-lite). On 𝒜_n ∩ E_n every within-block
addition (h, T, l) satisfies log[r(T+l)/r(T)] = −½log(n+1) − ν log(1 − x_{T,l}) + R, |R| ≤ κ, with κ := sup_n κ_EXP < ∞.
*Chain.* For V = {l₁,…,l_j} ⊆ C_h∖U_h°, add l₁,…,l_j in order starting from U_h°. The product of the (1 − x) factors
telescopes to RSS_{U°∪V}/RSS_{U°} = 1 − X_{h,V}. Hence on 𝒜_n ∩ E_n
  r_h(U°∪V)/r_h(U°) ≤ e^{jκ}(n+1)^{−j/2}(1 − X_{h,V})^{−ν}.                                                     (6.1)
*Truncation.* Let 𝒢_n := 𝒜_n ∩ E_n ∩ {X_{h,V} ≤ τ_n for all h, V}. The number of pairs (h, V) is ≤ G_n2^g ≤ n^A2^{16};
by Lemma B(i) each X_{h,V} is Beta(j/2, (m−j)/2) with m = n − 1 − |U_h°|, so Lemma Tr(c) gives P(𝒢_n^c) → 0.
*Moment.* By (6.1) and Lemma Tr(a) (mτ_n ≤ t_n), with C_e := 2^{g+3}:
  E[ã_hj1_{𝒢_n}] ≤ e^{jκ}(n+1)^{−j/2}·C(g, j)·C_e(t_n/2)^{j/2}/Γ(j/2+1).
Since j!C(g, j) ≤ g^j and Γ(j/2+1) ≥ 0.88: E[j!ã_hj1_{𝒢_n}] ≤ 1.14C_e(gξ_n)^j with ξ_n := e^κ√(t_n/(2(n+1))).
Jensen (x ↦ x^{1/j} concave): E[(j!ã_hj)^{1/j}1_{𝒢_n}] ≤ (1.14C_e)^{1/j}gξ_n ≤ 1.14C_e gξ_n. Since D̃_h ≤ Σ_{j=1}^{g}(j!ã_hj)^{1/j},
E[D̃_h1_{𝒢_n}] ≤ 1.14C_e g²ξ_n, and q̃ = (p−s)⁻¹Σ_hD̃_h over G_n = p/g groups gives
  E[q̃1_{𝒢_n}] ≤ 1.14C_e g ξ_n·p/(p−s) ≤ 2.3C_e g ξ_n = O(√(log n/n)).
Markov's inequality and P(𝒢_n^c) → 0 give q = O_P(√(log n/n)).
*The deletion quantity e.* Only the c + v truth-carrying groups have U_h° ≠ ∅, each with U_h° = {j_h}, so a = 1 in the
definition of e and e = 2p·max{r_h(U)/r_h(U + j_h) : h truth-carrying, U ⊆ C_h∖j_h} — a fixed finite family of
(h, U) indices (at most (c+v)2^{g−1}). On 𝒜_n ∩ E_n, log[r(U + j_h)/r(U)] ≥ −½log(n+1) − κ + νx_{U,j_h} (since
−log(1−x) ≥ x). By C3, x_{U,j_h} → x^pop(h, U) a.s., the population squared partial correlation of y and x_{j_h} given X_U.
It is positive: for an a-group, Cov(x_{j_a}, μ | X_U) = βVar(x_{j_a}|X_U) − ψβCov(x_{j_a}, x_{j_b}|X_U), and by (F1)
Cov(x_{j_a}, x_{j_b}|X_U) = ψΣ_aa − Σ_{aU}Σ_UU⁻¹ψΣ_{Ua} = ψVar(x_{j_a}|X_U), so the covariance is β(1−ψ²)Var(x_{j_a}|X_U) ≠ 0
with Var(x_{j_a}|X_U) ≥ λ₀; for a visible group it is β_hVar(x_{j_h}|X_U) ≠ 0. With x₀ := ½min x^pop > 0, w.p. → 1
e ≤ 2p√(n+1)e^{κ}e^{−νx₀}. Put c₆ := x₀/2.
*Conclusion.* [T22i](i-a) (deterministic, any partition): if q < 1 then 1 − π₀(S°) ≤ (s+1)q/(1−q) + se. ∎

*Remarks.* (1) No NL_η, no VIS-lin, no exact-zero-leakage hypothesis is used: the Beta structure of Lemma B replaces them.
This closes W1-EXP's §4.3 PROOF SKETCH (the iid-Gaussian, p > n version of its Theorem 5(a)), with the better rate
√(log n/n) in place of 2^B√(log n)n^{−1/2}. (2) The rate is sharp in order: numerically √(n/log n)(1 − π₀(S°)) stays
in [1.5, 2.6] for n ∈ [200, 1600] (REPORT §4). The √log n is the price of the max of p chi-squares; W1-EXP's exact-Gram
realisation has no null sample correlations and gets n^{−1/2}.

---------------------------------------------------------------------------------------------------------

## 7. Theorem P4 (masking at the CL(L) rate, with a limit law) — PROVED

**Statement.** On LH-iid,
  Mstat_n := log π₀(S₀) + c log p + (c/2)log n  →_d  Σ_{i=1}^{c} log((s+i)/2) + ½χ²_c.
In particular π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)} (two-sided), and T27(i)'s premises hold on the chain
S° ⊂ S° + j_{b_1} ⊂ … ⊂ S₀: H1 (deterministic chain, T_i = ∅), H2 (E_{n,i} = ½(n−1)r̂²_{j_{b_i},y}(1+o_P(1)) = O_P(1), i.e.
CL(L) with L = O_P(1)) and H3 (π₀(S°) → 1).

**Proof.** S₀ ∩ C_{b_i} = {j_{b_i}}, S° ∩ C_{b_i} = ∅, and S₀ ∩ C_h = S° ∩ C_h for every other group. On 𝒜_n, [T22ii](ii-a)
gives exactly
  π₀(S₀) = π₀(S°)·[w(s+c)/w(s)]·∏_i r_{b_i}({j_{b_i}}).
*Prior.* w(k+1)/w(k) = (k+1)/(2p−1−k), so log[w(s+c)/w(s)] + c log p = Σ_{i=1}^c log((s+i)p/(2p−s−i)) → Σ log((s+i)/2).
*Single-column table, exactly.* For U = {j}: G = n − 1, H = (n+1)(n−1) + 1 = n², det(G + 1) = n, so D_{j} = n; z = (n−1)r̂
(r̂ := r̂_{j,y}), Q_j = (n−1) − nz²/n² = (n−1) − (n−1)²r̂²/n. Hence
  log r({j}) + ½log n = −ν log(1 − κ_n r̂²),  κ_n := (n−1)²/(n(n−0.98)) ∈ (0, 1].
By Lemma B(iii), (n−1)r̂²_i →_d independent χ²_1, so −ν log(1 − κ_n r̂_i²) = (n/2)r̂_i²(1 + O_P(1/n)) →_d ½χ²_{1,i} jointly.
*Reference mass.* log π₀(S°) → 0 in probability (Theorem P3). Slutsky. ∎

---------------------------------------------------------------------------------------------------------

## 8. Theorem P5 (eligibility of the start mode) — PROVED

P(S̃₀ = S°) → 1, where S̃₀ = argmax π₀ (computable exactly by max-plus convolution). Hence S̃₀ ∈ 𝓡₀ ⊆ 𝓡_d and
|S̃₀ Δ S₀| = c w.p. → 1.
*Proof.* On {π₀(S°) > ½} no other model has mass ≥ ½, so S̃₀ = S° ([T38E-E3](i)); Theorem P3. ∎

---------------------------------------------------------------------------------------------------------

## 9. Theorem P6 (repair input TD′: lattice condition at the centre S°; LS0 repairs) — PROVED

### 9.1 Lemma U (uniform score approximation on small sets) — PROVED
Let 𝔉_n := {A ⊆ [p] : |A| ≤ s₀ + 2} (|𝔉_n| ≤ (p+1)^{s₀+2}, polynomial in n) and Λ_A := ‖Π_A^⊥μ‖², μ the centred signal.
On an event of probability → 1, simultaneously for all A, A′ ∈ 𝔉_n:
(U1) F(A) = log w(|A|) − ½|A|log(n+1) − ν log RSS_A + c_n + R_A, |R_A| ≤ κ₂ (κ₂ a constant, c_n free of A);
(U2) |RSS_A − nσ² − Λ_A| ≤ C₂n^{2/3};
(U3) consequently, if Λ_{A′}/n ≥ Λ_A/n + c′ for a fixed c′ > 0, then F(A) − F(A′) ≥ (n/2)log(1 + c′/(2(σ² + M))) − C₃log n.
*Proof.* (U1) On 𝒜_n every A ∈ 𝔉_n has λ_min(G_A) ≥ φ₀²(n−1) (Lemma P2(a), s₀ + 2 ≤ m_n + s₀). Iterating [EXP-L1.2] along any
ordering of A gives log D_A = |A|log(n+1) + η_A, |η_A| ≤ |A|(1 + φ₀⁻²)/(φ₀²(n−1)). [EXP-L1.1] gives 2b₀ + Q_A = RSS^y_A + a_A,
a_A ∈ [0.02, 1.02 + 1/(nφ₀²)]. [EXP-L1.4], whose union bound is over the polynomial family 𝔉_n here (choose its L >
4A(s₀ + 3)), gives RSS^y_A ≥ c_*n for all A ∈ 𝔉_n w.p. → 1, so ν log(1 + a_A/RSS^y_A) ≤ ν(1.02 + 1/(nφ₀²))/(c_*n) ≤ 1.
Finally RSS^y_A = (n−1)RSS_A/‖Y‖², whose factor is common to all A.
(U2) RSS_A = Λ_A + 2⟨Π_A^⊥μ, ε⟩ + ‖Cε‖² − ‖P_Aε‖². Given X: ‖Cε‖²/σ² ~ χ²_{n−1}, in [n − n^{2/3}, n + n^{2/3}] w.p. → 1;
‖P_Aε‖²/σ² ~ χ²_{≤ s₀+2} and ⟨Π_A^⊥μ, ε⟩/(σ√Λ_A) ~ N(0,1); a union bound over 𝔉_n gives max_A ‖P_Aε‖² ≤ C log n and
|⟨Π_A^⊥μ, ε⟩| ≤ σ√(Λ_A C log n) ≤ σ√(MCn log n). (U3) By (U1), F(A) − F(A′) = ν log(RSS_{A′}/RSS_A) − |Δ prior| − |Δ det|
− 2κ₂, with |Δprior| ≤ 2log(2p) and |Δdet| ≤ log(n+1) for |A| − |A′| ≤ 2; by (U2) RSS_{A′}/RSS_A ≥ (nσ² + Λ_A + c′n −
C₂n^{2/3})/(nσ² + Λ_A + C₂n^{2/3}) ≥ 1 + c′/(2(σ² + M)) eventually (Λ_A ≤ ‖μ‖² ≤ Mn). Comparisons with a size difference of at most 2 are all that is used below. ∎

### 9.2 Lemma Λ (population residuals) — PROVED
For B ⊆ 𝒮𝒱 let λ(B) := Var(μ | X_B) (population, per row), and λ_i(B) := Var(μ_i | X_B) for B ⊆ K_i.
(a) Uniformly over A ∈ 𝔉_n, Λ_A/n = λ(A ∩ 𝒮𝒱) + o_P(1).
(b) λ(B) = Σ_iλ_i(B ∩ K_i) + Σ_hβ_h²Var(x_{j_h} | X_{B∩V_h}) (components independent, F5).
(c) Values (pair i; write G_i := ψ_i²β_i²(1 − ψ_i²), η_i := ρ²(1 − ψ_i²)/(1 − ψ_i²ρ²) ∈ (0,1)):
   λ_i({j_a, j_b}) = 0; λ_i({j_a}) = G_i; λ_i({j_b}) = β_i²(1 − ψ_i²); λ_i(∅) = β_i²(1 − ψ_i²);
   λ_i({j_a, l}) = G_i for l ∈ C_a∖j_a; λ_i({j_a, l}) = G_i(1 − η_i) for l ∈ C_b∖j_b;
   for l ∉ {j_a, j_b}: λ_i({l}) ≥ λ₀β_i²(1 + ψ_i²) and λ_i({j_b, l}) ≥ λ₀β_i².
*Proof.* (a) For A = A_s ∪ A_0 with A_s ⊆ 𝒮𝒱 and A_0 in null groups (|A_0| ≤ s₀ + 2): Λ_{A_s}/(n−1) = θ*ᵀ(R̂ − R̂_{·A_s}R̂_{A_sA_s}⁻¹
R̂_{A_s·})θ* restricted to 𝒮𝒱 coordinates → λ(A_s) a.s. (C3; finitely many A_s). And 0 ≤ Λ_{A_s} − Λ_A = ‖P_{span Π^⊥_{A_s}X_{A_0}}
Π^⊥_{A_s}μ‖², whose ratio to Λ_{A_s} is Beta(|A_0|/2, ·) by the argument of Lemma B (null columns are independent of
(X_{𝒮𝒱}, μ)); by Lemma Tr(c) its max over the polynomial family is ≤ t_n/n, so Λ_{A_s} − Λ_A ≤ Mt_n = o(n).
(b) Independence of components. (c) Direct Gaussian computations: Var(μ_i) = β²(1 + ψ² − 2ψ²) = β²(1 − ψ²);
Var(μ_i | x_{j_a}) = ψ²β²Var(x_{j_b}|x_{j_a}) = G_i; Var(μ_i | x_{j_b}) = β²Var(x_{j_a}|x_{j_b}) = β²(1 − ψ²); for l ∈ C_a∖j_a,
x_l ⊥ x_{j_b} | x_{j_a} (F3) so conditioning on x_l adds nothing; for l ∈ C_b∖j_b, Cov(x_{j_b}, x_l | x_{j_a}) = ρ − ψ·ψρ =
ρ(1 − ψ²) and Var(x_l | x_{j_a}) = 1 − ψ²ρ², so Var(x_{j_b} | x_{j_a}, x_l) = (1 − ψ²)(1 − η_i). The lower bounds: for
B with |B| ≤ 2 not containing j_a, Var(β(x_{j_a} − ψx_{j_b}) | X_B) = min_t E(β x_{j_a} − ψβx_{j_b} − tᵀx_B)² ≥ λ₀ times the
squared norm of the coefficient vector restricted to {j_a, j_b}∖B, which is ≥ β² (and ≥ β²(1+ψ²) if j_b ∉ B). ∎

### 9.3 The theorem
**Statement.** On LH-iid, w.p. → 1:
(L) S₀ has no strictly improving feasible flip or swap; and
(D) for every S in the lattice Lat(S°) ∖ {S₀} = {S° ∪ M′ : M′ ⊊ M}, the event D_S of W1-T37R holds: the best progress move
    (adding a missing masked hub) beats S itself and every neutral or regressive neighbour of S.
Hence, by [T37R-A](A3) (lattice version), since Φ(S°) = c ≤ ℓ_n = ⌈log₂(n+p+1)⌉ eventually, the production local search
from the centre S° returns S₀ with local_certified after exactly c moves; with Theorem P5, **LS0 scores and certifies S₀
w.p. → 1** ([T38E-E3]).

**Proof.** Fix S = S° ∪ M′ (M′ ⊊ M); missing hubs I := {i : j_{b_i} ∉ S} ≠ ∅; i* := argmax_{i∈I} G_i. In population,
λ(S) = Σ_{i∈I}G_i (Lemma Λ(c): complete pairs and visible groups contribute 0), and the progress move P* = S + j_{b_{i*}}
has λ(P*) = λ(S) − G_{i*}. Every other neighbour A of S (flip or swap; S contains no extras) satisfies
λ(A ∩ 𝒮𝒱) ≥ λ(P*) + c₂, with c₂ > 0 the minimum of the margins below:
- *A = S:* margin G_{i*} ≥ min_iG_i.
- *Add a neutral or null l:* the component of l does not lose residual (Lemma Λ(c): a-group members, visible-group members,
  null-group members change nothing) — margin G_{i*}.
- *Add a proxy l ∈ C_{b_i}∖j_{b_i}:* if i ∉ I (pair complete) no change; if i ∈ I the drop is G_iη_i ≤ G_{i*}η_max, margin
  ≥ G_{i*}(1 − η_max) ≥ min_iG_i(1 − η_max).
- *Add a different missing hub j_{b_i}, i ∈ I ∖ {i*}:* this is also a progress move; it is not needed in D_S, and in any case
  λ = λ(S) − G_i ≥ λ(P*).
- *Delete a truth k ∈ S:* the residual of k's component strictly increases, by β_i²(1−ψ_i²)² (k = j_{a_i}, pair incomplete),
  β_i²(1−ψ_i²) (k = j_{a_i}, pair complete), G_i (k = j_{b_i}), or β_h²(1 − 0) (visible hub; Var(x_{j_h}) = 1).
  Margin ≥ c₄ := min of these.
- *Swap truth k → l, different components:* = deletion of k plus addition of l in another component: λ ≥ λ(S) + c₄ − G_{i'}
  ≥ λ(P*) + c₄ (G_{i'} ≤ G_{i*}, and adding j_{b_{i'}} itself is the worst case). Margin c₄.
- *Swap within one component:* visible: {j_h} → {l}, residual β_h²(1 − ρ²) > 0 = before. Complete pair {j_a, j_b} → {j_a, l}
  (≥ G_i(1 − η_i)) or {j_b, l} (≥ λ₀β_i²): increases from 0. Incomplete pair {j_a} → {l}: residual ≥ λ₀β_i²(1+ψ_i²), so
  λ(A) − λ(P*) ≥ λ₀β_i²(1 + ψ_i²) − G_i + G_{i*} ≥ λ₀β_i²(1+ψ_i²) > 0; {j_a} → {j_b} (truth→truth): residual β_i²(1−ψ_i²),
  margin β_i²(1−ψ_i²) − G_i = β_i²(1−ψ_i²)² > 0.
All margins are fixed positive numbers. By Lemma Λ(a) the sample values satisfy Λ_A/n ≥ Λ_{P*}/n + c₂/2 uniformly over the
≤ (s₀ + 1)(p + 1) neighbours of each of the 2^c − 1 lattice states, w.p. → 1, and Lemma U(U3) gives F(P*) − F(A) ≥
(n/2)log(1 + c₂/(4(σ² + M))) − C₃log n > 0. This is D_S (strict, so the lexicographic tie rule is not used).
(L): every deletion or swap A of S₀ misses a truth, and by the deletion and within-component cases above λ(A) ≥ c₂ > 0 = λ(S₀);
Lemma U(U3) gives F(S₀) − F(A) ≥ c n. For additions A = S₀ + l we need the finer scale: μ ∈ span X_{S₀}, so
RSS_{S₀+l}/RSS_{S₀} = 1 − Z_l²σ²/‖Π_{S₀}^⊥Cε‖² with Z_l := ũ_lᵀε/σ ~ N(0,1) given X (ũ_l the unit vector of Π^⊥_{S₀}x_l).
max_{l≤p}Z_l² ≤ 2log p + 2log log n w.p. → 1, and ‖Π^⊥_{S₀}Cε‖² ≥ nσ²(1 − 2n^{−1/3}). By (U1),
F(S₀ + l) − F(S₀) ≤ −½log(n+1) − log((2p−s₀−1)/(s₀+1)) + (Z_l²/2)(1 + O(n^{−1/3})) + 2κ₂ ≤ −½log n + log log n + O(1) → −∞,
uniformly in l. ∎

*Remark (two speeds; numerically visible).* The D_S part rests on Θ(n) margins. The (L) part rests on the much smaller
margin ½log n + log(2p/(s₀+1)) − ½max_lZ_l², and to first order P((L) fails) ≈ p·P(χ²₁ > t_n) = (s₀+1)/√(2π(n+1)t_n),
with t_n := 2log((2p−s₀−1)/(s₀+1)) + log(n+1). This is ≈ 4% at (n, p) = (200, 750) and ≈ 1.2% at (1600, 10120)
(`results/check_L_failure.txt`; one such event occurred among the 12 replicates at n = 1600, with Z² = 24.5 against
t = 23.6). It tends to 0 only like n^{−1/2}(log n)^{−1/2}. A failure of (L) is the event that some S₀ + l beats S₀. That
belongs to the posterior term 2E₀δ₁ of T21/T38(b)-R, not to discovery: the search still passes through, and so *scores*,
S₀. [T38E-E3]'s TD′ only requires that S₀ be scored, so route (b1) needs only the D_S part.

*Remark.* For c = 1, Lat(S°) = {S°, S₀} and the theorem is the statement "from S° the best move adds j_b, then S₀ is
certified". The swap-dominance obstruction of W1-T38E §6.4 does not arise because the centre S° contains no extras; this
is exactly why the *start mode* is a good LS0 centre on this family.

---------------------------------------------------------------------------------------------------------

## 10. Theorem P7 (the no-tweak route D2 for c = 1) — PROVED for (D2-a,b,c); PROOF SKETCH for (D2-d)

**Statement.** On LH-iid with c = 1, put x° = S°, 𝒟 := C_b ∖ {j_b} (k_D = g − 1), b = ½. Then w.p. → 1:
(D2-a) x° Δ S₀ = {j_b} and s₀ ≤ K; (D2-b) π₀(x°) ≥ ½ > 1/10; (D2-c) Dep := Σ_{l∉𝒟∪{j_b}}max{κ₀(x°,l), κ₁(x°,l)} → 0 in
probability, Dep = O_P(√(log n/n)); (D2-d) NB: the initial pilot d-range over the H₀ iid π₀ draws is ≤ T_e log 1.925
(unless S₀ is drawn). Consequently, by [T38E-D2] (under EX-A, EX-S, SR), **P(S₀ ∉ 𝒮_cal) → 0**: the original method scores
S₀ in the first pilot round, with no LS0 tweak and no delivery hypothesis.

**Proof of (D2-c).** Split by the flipped coordinate l.
- *Start odds, additions* (l neutral or null): κ₀(x°, l) = [w(s+1)/w(s)]·r_{h(l)}(U° + l)/r_{h(l)}(U°), and Σ_l of the table ratios
  is ≤ Σ_h ã_{h1} ≤ Σ_hD̃_h = (p − s)q. So Σ_lκ₀ ≤ ((s+1)/(2p−s−1))(p−s)q ≤ (s+1)q = O_P(√(log n/n)) (Theorem P3).
- *Start odds, deletions* (l ∈ S°, U° = {l} in its group): κ₀ = [w(s−1)/w(s)]·r(∅)/r({l}) ≤ (2p/s)·e/(2p) = e/s → 0.
- *Posterior odds, additions* (l neutral; proxies are in 𝒟): κ₁ = [w(s+1)/w(s)]·BF(S°+l)/BF(S°). By Lemma U(U1) applied to
  the pair (S°, S° + l) — equivalently [EXP-T1]'s single-addition expansion, valid for any set with SE —
  BF(S°+l)/BF(S°) ≤ e^{κ₂}(n+1)^{−1/2}(1 − x_{S°,l})^{−ν}, and x_{S°,l} ~ Beta(½, (n−3−s)/2) by Lemma B(ii). Truncating at
  τ_n (Lemma Tr(c), p events) and using Lemma Tr(a) with j = 1: E[Σ_lκ₁1_{𝒢}] ≤ ((s+1)/(2p−s−1))·p·e^{κ₂}(n+1)^{−1/2}·
  C_e(t_n/2)^{1/2}/Γ(3/2) = O(√(log n/n)).
- *Posterior odds, deletions* (l ∈ S°): S° − l misses a further truth; by Lemma Λ the residual increases by ≥ c₄ and Lemma
  U(U3) gives κ₁ ≤ (2p/s)e^{−c n + C log n} → 0.
So Dep = O_P(√(log n/n)). (D2-a), (D2-b): definition and Theorem P3. ∎

**Proof sketch of (D2-d).** Let k₀ := ⌈2A⌉ + 1 and 𝒢 := {S° ∪ P : P neutral, |P| ≤ k₀}.
(1) *All H₀ draws lie in 𝒢 ∪ {S₀} w.p. → 1.* H₀ = ⌈512 max(2500, n, p)/2500⌉ ≤ 0.21p + 1. Three bad sets:
 (i) {S ⊉ S°}: mapping S ↦ S ∪ S° and using the per-block deletion ratio bounded by e/(2p) (definition of e) together with
     the prior ratio, π₀(S ⊉ S°) ≤ 2^s·poly(n)·e, which is exponentially small, so H₀·π₀ → 0.
 (ii) {S ∩ C_b ≠ ∅} (j_b or a proxy drawn): conditioning on S ∖ C_b = R with |R| ≤ k₁, the C_b-part has odds
     [w(|R|+|U|)/w(|R|)]r_b(U) against U = ∅, so π₀(S ∩ C_b ≠ ∅, |S| ≤ k₁) ≤ Σ_{j≥1}((k₁+j)/(2p−2k₁−2j))^j ã_{bj} ≤
     (k₁+1)ζ_n/p·O_P(1) with ζ_n = O(√(log n/n)) (Theorem P3's moment bound for the b-group), and H₀ times this is
     O_P((k₁+1)ζ_n) → 0. (This is the only place where H₀ ∝ p and the 1/p prior factor must balance exactly.)
 (iii) {|S ∖ S°| > k₀}: with a_bj ≤ D_b^j/j! the generating function of extras is dominated coefficientwise by e^{z(p−s)q},
     so π₀(|S ∖ S°| = k, S ⊇ S°) ≤ ((s+k)q)^k/k!; H₀((s+k₀+1)q)^{k₀+1} → 0 because q = O_P(√(log n/n)) and k₀ + 1 > 2A.
(2) *d is nearly constant on 𝒢.* For S = S° ∪ P ∈ 𝒢, d(S) − d(S°) is a sum over a chain of ≤ k₀ neutral additions of
[log BF ratio − log table ratio]; the −½log(n+1) terms cancel and each remaining term is ≤ κ + κ₂ + ν|log(1 − x^{full})| +
ν|log(1 − x^{blk})|. All x's are Beta(½, ·) or Beta(j/2, ·) (Lemma B (i)–(ii)) over a polynomial family (≤ p^{k₀+1}k₀!
members), so max ≤ t′_n/n with t′_n = O(log n) by Lemma Tr(c) (with A replaced by A(k₀+1)). Hence the d-range over 𝒢 is
O_P(log n), whereas T_e log 1.925 ≥ max(1000, ℓ²)·0.655 with ℓ ≥ log₂p ≥ a log₂n, which grows like log²n.
*What is not written line by line:* the bound (1)(i) (an AGG-type peeling over missing reference variables) and the
uniformity bookkeeping in (2). Both use only Lemmas B, Tr, U and the definitions of q, e. ∎

---------------------------------------------------------------------------------------------------------

## 11. Theorem P8 (posterior concentration) — PROVED (given [T03])

**Statement.** On LH-iid, 1 − π(S₀) = O_P(√(log n/n)) under the joint law of (X, ε).

**Lemma (design de-randomisation; PROVED).** Let 𝒜′_n be X-measurable events with P(𝒜′_n) → 1, and Z_n ≥ 0 a statistic
with the property: for every deterministic sequence x_n ∈ 𝒜′_n (n ≥ n₀), Z_n = O_P(r_n) under P(· | X = x_n). Then
Z_n = O_P(r_n) unconditionally.
*Proof.* Put f_n(M) := sup_{x∈𝒜′_n}P(Z_n > Mr_n | X = x). If the conclusion fails, there are ε > 0 and n_k ↑ ∞ with
f_{n_k}(k) > ε, hence x_{n_k} ∈ 𝒜′_{n_k} with P(Z_{n_k} > kr_{n_k} | x_{n_k}) > ε/2; complete to a sequence x_n ∈ 𝒜′_n
(possible for n ≥ n₀). By hypothesis there are M, N with P(Z_n > Mr_n | x_n) < ε/2 for n ≥ N; at n_k ≥ N with k ≥ M this
contradicts P(Z > kr | x) ≤ P(Z > Mr | x). So for every ε there are M, N with f_n(M) ≤ ε for n ≥ N, and
P(Z_n > Mr_n) ≤ ε + P((𝒜′_n)^c). ∎

**Proof of P8.** Let 𝒜′_n be the event of Lemma P2 (a)–(d) with fixed constants (A, M, φ₀, b₀). For any deterministic
sequence in 𝒜′_n, the model given X is the fixed-design model G with truth θ*(x_n), and G, R, SE, BM-∞ hold with these
constants; [T03] gives 1 − π(S₀) = O_P(√(log n/n)). Apply the lemma. ∎

---------------------------------------------------------------------------------------------------------

## 12. Corollary (T38(b) on LH-iid) — PROVED given the cited inputs

Under EX-A, EX-S, CAL, SR and the operational setting of [T38E-R], on LH-iid with p_n ∈ [n^a, n^A]:
(b1) with the LS0 tweak (local search also from S̃₀), for every fixed c ≥ 1:
     liminf_n P(Uᶜ ∩ {Ŝ⁺ = S₀}) ≥ 1 − limsup_n P(U);
(b1′) without any tweak, for c = 1: the same conclusion for the original Ŝ, since S₀ ∈ 𝒮_cal w.p. → 1 (Theorem P7)
      — conditional on the PROOF SKETCH status of (D2-d).
*Proof.* [T38E-R] with: H-T03 from Theorem P8; route (b1): ELIG from Theorem P5 (𝔅_n := {S°}), TD′(𝔅_n, ℓ_n) from
Theorem P6; route (b1′): D2's hypotheses from Theorem P7. ∎

Also, consistently with W1-EXP Theorem 5(c), VIS at the reference S₀ fails (the block of j_b sees no signal), so this is
genuinely the masked regime: the favourable branch T22(iii) at S₀ does not apply and π₀(S₀) → 0 (Theorem P4).

---------------------------------------------------------------------------------------------------------

## 13. Proposition Q (co-blocking defeats correlation masking when the linked unit fits in a block) — PROOF SKETCH

**Statement.** Take LH-iid but with 2g ≤ B (e.g. the study's groups of 5 with B ∈ {10,…,16}). Then w.p. → 1 each linked
pair C_{a_i} ∪ C_{b_i} lies inside one block, and the masked hub becomes visible within that block: the start log-odds of
j_{b_i} given j_{a_i} is (n/2)·ψ²β²(1−ψ²)/(σ² + λ(rest)) − O(log n) → +∞, so π₀(S₀) → 1 under the remaining
favourable-regime conditions, and LH loses its masking.
*Sketch.* As in Lemma P1(a), each group is completed first (within-group distances ≈ 1 − ρ are the smallest). After that,
the complete-linkage distance between two groups is 1 − min over the g² cross pairs of |r̂|. For a linked pair this
minimum → |ψ|ρ² > 0 (the off-hub cross correlation), so the distance → 1 − |ψ|ρ² < 1. For two independent groups the
minimum of g² sample |r̂| values whose population value is 0 is O_P(1/√n), so the distance → 1, and a union bound over
the ≤ G_n² group pairs keeps all of them above 1 − |ψ|ρ²/2 w.p. → 1 (each such minimum exceeds |ψ|ρ²/2 only if all g² of
its |r̂| do, probability ≤ e^{−cng²}). Hence a and b merge with each other before either merges with any other group; the
node C_a ∪ C_b has size 2g ≤ B, so the top-down cut retains it and packing keeps it whole. Within that block,
Var(μ_i | x_{j_a}) = G_i > 0 = Var(μ_i | x_{j_a}, x_{j_b}): given j_a, the masked hub explains a fixed share of the
within-block residual, so its block log-odds grows linearly in n.
*Gap:* the claim "P(min of g² independent |r̂| > t) ≤ e^{−cng²}" treats the g² correlations as independent; they are not
(shared columns). A correct bound uses one pair (k, k′) only: P(|r̂_{kk′}| > t) ≤ e^{−cnt²}, which already suffices for a
union over G_n² ≤ n^{2A} group pairs since cnt² ≫ log n. So the gap is cosmetic; not rewritten.
**Consequence.** Masking by correlation-induced cancellation survives the X-dependent partition only when the cancelling
unit is too large to fit in one block (here g > B/2), or when the linking correlations are too weak to drive clustering.
The study's own designs (groups of 5) cannot carry LH-type masking.

---------------------------------------------------------------------------------------------------------

## 14. Proposition W (dilution masking; the study regime) — PROOF SKETCH (asymptotic part), numerics in REPORT §5

Setting: iid Gaussian design whose population is *block-orthogonal* for the w.p. → 1 partition (no cross-block population
leakage: for every block b and T ⊆ C_b, Cov(X_{C_b}, μ | X_T) only through the truths in C_b — true for S1, S3, S4, S6 with
one truth per group, as in the study generator). For a truth j in block b with T := S₀ ∩ C_b ∖ {j}:
(a) the start "keep-j" log-odds is
  LO₀(j) := log π₀(S₀) − log π₀(S₀ − j) = −log((2p − s₀)/s₀) − ½log(n+1) + V₀(j) + O_P(1),
  V₀(j) := −ν log(1 − x_{T,j}),  V₀(j) = (n/2)·θ_j²Var(x_j | X_T)/v_T·(1 + o_P(1)) + O_P(√n),
  v_T := σ² + λ(T) = σ² + (all signal not explained by the truths in the same block);
(b) the posterior keep-j log-odds is the same expression with v_T replaced by σ² (and T by S₀ − j):
  LO₁(j) = −log((2p − s₀)/s₀) − ½log(n+1) + (n/2)log(1 + θ_j²Var(x_j | X_{S₀−j})/σ²)(1 + o_P(1)).
*Sketch.* (a) is [T22ii] for the one-coordinate change plus [EXP-T1]; the population limit of x_{T,j} uses block
orthogonality (only the truth j contributes to δ_{T,j}) and RSS_T/n → v_T. (b) is Lemma U.

**Consequences.**
- *Dilution threshold.* j is start-masked (LO₀(j) < 0) iff, to first order, nθ_j²Var(x_j|X_T)/(2v_T) < (½ + A_n)log n
  with A_n := log(2p/s₀)/log n, while the posterior keeps j iff the same holds with σ² in place of v_T. The window is the
  *dilution factor* v_T/σ² = 1 + (signal outside the block)/σ². In the high-SNR limit v_T ≈ ‖θ‖², so the masking condition
  becomes θ_j²/‖θ‖² ≲ 2(½ + A_n)log n/n: **at fixed n it does not go away as the signal grows** (it is scale-free), and with
  s₀ comparable truths it bites when n/log n ≲ 2s₀(½ + A_n).
- *Under BM-∞ with s₀ fixed (the frozen setting), dilution masking disappears asymptotically:* v_T is bounded, so
  V₀(j) ≥ cn ≫ log n for every truth. Hence, in block-orthogonal designs, **every fixed-s₀ BM-∞ asymptotic family is in
  the favourable regime**; masking in the frozen setting requires population cancellation across blocks (LH-type; with
  Proposition Q, across blocks *larger than half of B*).
- Dilution masking is **not** CL(L) with bounded L: the masked truths have δ²_{T,j}/σ² = nθ_j²Var(x_j|X_T)/σ² of order n (50–200
  at the study size), and the chain multiplier e^{Σ L²σ²/(2v)} of W1-EXP Theorem 3/4 is enormous; T27(i)'s rate p^{−c}n^{−c/2} does
  not describe π₀(S₀) there (REPORT §5: it overshoots by 17–29 orders of magnitude).
- A fixed-s₀ asymptotic version requires leaving BM-∞: e.g. local alternatives θ_j² = κσ² log n/n for the diluted truths plus
  fixed strong truths, with κ in the window (1 + 2A) < κ < (1 + 2A)v_T/σ². Then π₀(S₀) → 0 polynomially
  while LO₁(j) → +∞; but π(S₀) → 1 would need a sharp-constant selection theorem that [T03]/T03♯ do not provide (their BM
  constant c₀ = L* is far above (1 + 2A)). CONJECTURE.
