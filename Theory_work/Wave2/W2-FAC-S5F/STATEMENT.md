# W2-FAC-S5F — STATEMENT (target statement)

Ticket W2-FAC-S5F, Theory Wave 2. Lead: Claude Fable 5.1 (Claude Personal). Status of this file: **v1 — for statement
lock** (2026-11-09). All results are asymptotic (Wave-2 scope rule). Abbreviations as in FAC-B: SoP =
`Theory_work/State_of_Project/sections/`; FINAL = `Theory_work/Wave1C/FINAL/sections/`; FAC-A/FAC-B =
`Theory_work/Wave2/W2-FAC-A/`, `Theory_work/Wave2/W2-FAC-B/`.

## 0. Target, route and scope

HQ target: reported-model consistency of the merged method (v3.1, main 599d59d/4676af6: LS0 from the start mode with
cap a_n = ℓ_n + |S̃₀|) on block compound symmetry (study S5: groups of 5, within 0.7, between 0.3), growing p, ideally
any p ≤ n/2. Known: FAC-A (whole-lattice no-addition) covers log p/log n < 1/6 and proves that route stops there;
FAC-B covers plain compound symmetry for any p ≤ n/2 by an exact one-dimensional path analysis, which breaks for S5.

**Route (independent of the two-level gap invariant of W2-FAC-S5, which is not used or read).** Exact,
design-general tools: (i) all neighbour gains are size terms plus −(n/2)log(1 + σ²Z²/RSS_T) + O(1) with Z² the exact
RSS (projection) increment; (ii) the Pythagorean *jump inequality* Z²(l; T∖j) ≤ Z²(l; T) + Z²(j; T); (iii) *swap
domination*: F(T∖j∪l) − F(T) = G_add(l; T∖j) + G_del(j; T), so swaps are dominated by the best deletion whenever no
addition improves at the one-below sets T∖j; (iv) the *drift identity* for the global centre c̄_T = E[√a η | P_Tε]:
c̄_T − c̄_{T∖j} = κ_T(j)·r_j(T) with κ > 0. For block CS: an exact ANOVA split of the fit into within-group sums of
squares and a heterogeneous group-level compound-symmetry fit; every null statistic is a *local* configuration statistic
(depending on the retained group-mates only) plus a multiple of the global centre. A *level lemma* (counting fully-large
configurations) bounds the running deletion level by 2 log(2^{q+1}p/m) + O(log log n) with m kept nulls, and a
*top-order-statistics bound* controls the global centre at the same scale — both without any path structure. This
closes the whole path **except the end phase** (m ≤ p n^{−c₀}), where the global centre needs a majority-side
argument at the group level; that part is stated as an explicit hypothesis (CC) and is the exact obstruction.

## 1. Setting (as FAC-B STATEMENT §1, with the design class changed)

* **D0**, **G**, **blocks**, **method** (v3.1 + LS0, cap a_n = ℓ_n + |S̃₀|, production tie rule, deterministic search,
  single-search prefix property), **implementation premises** (EX-A, EX-S, SR, GUARD-W, OP-LS0, e4′, complete scans;
  CAL only in the [M5-0] route), 𝒪, U_n, D_n: exactly as FAC-B STATEMENT §1 (`Theory_work/Wave2/W2-FAC-B/STATEMENT.md`
  §1), which is incorporated by reference. θ* := D_xβ, μ := Xθ*, Y := μ + Cε, y := Y/s, yᵀy = n − 1.

## 2. Hypotheses (class BCS)

* **(BCS) exact-Gram block compound symmetry.** XᵀX = (n − 1)Σ_n, Σ_n = Υ_n[a·11ᵀ + b·H_n + c·I_p]Υ_n with fixed
  a > 0, b ≥ 0, c > 0, a + b + c = 1, where H_n is the indicator matrix of a deterministic partition of [p] into groups
  of size ≤ q (q fixed; S5: a = 0.3, b = 0.4, c = 0.3, q = 5, groups of exactly 5), and Υ_n is a diagonal ±1 matrix
  (column sign flips; removed as in FAC-B L1.0). λ_min(Σ_n) = c =: c_min. Requires p ≤ n − 1. (b = 0 or q = 1 is plain
  CS with ρ = a.)
* **(P)** p = p_n ≤ ⌊n/2⌋ for all large n (so K = p).
* **(θ)** s₀ fixed, sign-corrected truth coefficients a fixed vector ϑ ∈ (ℝ∖{0})^{s₀}, positions arbitrary (so the
  truths' group pattern may vary with n), σ² fixed. N₀ := ⋃{C_b ∖ S₀ : S₀ ⊆ C_b}, S* := [p] ∖ N₀, 𝒩* := S* ∖ S₀,
  m₀ := |𝒩*|.
* **(FS-B) full start — generic no-cancellation.** For every U ⊆ [p] with |U| ≤ 15 and l ∉ U, the population partial
  covariance c(U, l) := Cov(x_l, μ | x_U) = (Σ_{l,S₀} − Σ_{l,U}Σ_{U,U}⁻¹Σ_{U,S₀})ϑ (Σ-scale; Σ_{U,U} := empty for U = ∅)
  is nonzero unless U ⊇ S₀ and l ∉ S₀ (where it is 0). Under (BCS), c(U, l) takes finitely many values (it depends on
  the group pattern of (U, l, S₀) only), so (FS-B) excludes finitely many hyperplanes of ϑ for each pattern; for b = 0 it
  is FAC-B's (FS).

**(H0) is automatic on this class** (as FAC-B L5.1 with φ₀² = c, A = 1, g₀ = c): claim (C4)(i).

## 3. Definitions used in the claims (precise forms in lemmas/L0–L1)

* **Statistics (exact).** For T ⊇ S₀ and l ∉ T: Z²(l; T) := (RSS_T − RSS_{T∪l})/σ² ≥ 0 (RSS_A := ‖(I − P_A)Y‖²; for
  T ⊇ S₀ and null l this is the squared standardized partial correlation of x_l with the noise given x_T, a χ²₁ variable
  for fixed (T, l)). For j ∈ T: Z²(j; T) := Z²(j; T∖j) = (RSS_{T∖j} − RSS_T)/σ² (deletion statistic). The **level** at a
  visited set T is ℓ(T) := min_{j∈T∖S₀} Z²(j; T); the **hole bound** is h(T) := max_{l∈𝒩*∖T} Z²(l; T).
* **Noise representation.** g := Xᵀε/(σ√(n − 1)) = √a η 1 + √b ζ_{grp} + √c ξ with η ~ N(0,1), ζ ~ N(0, I_J),
  ξ ~ N(0, I_p) independent (J = number of groups). For a retained configuration U ⊆ G (u = |U| ≥ 1): ξ̄_U := mean of
  ξ over U, ỹ_G(U) := √b ζ_G + √c ξ̄_U, d_u := b + c/u, w_u := 1/(c + b u). W_T := Σ_{G hit} 1/d_{u_G}.
* **Global centre.** c̄_T := a Σ_{G hit}(√a η + ỹ_G(U_G))/d_{u_G} / (1 + aW_T) (= E[√a η | P_T ε] on the enlarged
  space); its bias δ′_T := c̄_T − √a η = a Σ_{G hit} ỹ_G(U_G)/d_{u_G}/(1 + aW_T) − √a η/(1 + aW_T).
* **Thresholds (standardized).** Δ_k := log[(2p − k)/k] + ½ log(n + 1); M_T := nσ²/(2 RSS_T) ∈ [½ − o(1), 1 + o(1)].
  An addition of l to T is improving only if M_T Z²(l; T) ≥ Δ_{k+1} − O(1); a null deletion is improving if
  M_T Z²(j; T) ≤ Δ_k − O(1) (L0).
* **Scales.** L_n := log log n; H := √(2 log p); ℓ′(m) := 2 log(2^{q+1} p/m) + 4 L_n (the level scale with m kept nulls).
* **Bulk/end boundary.** m_e := ⌈C₀ p n^{−c₀}⌉ with explicit constants C₀, c₀ = c₀(a, b, c, q) > 0 fixed in L4.
* **Hypothesis (CC_θ) — end-phase centre control (not proved; the exact obstruction).** For a constant θ ∈ [0, 1):
  with probability → 1, |δ′_T| ≤ θ √(d₁) H + o(H) at every set T visited by the uncapped path from S* with
  |T∖S₀| < m_e and at every one-below set T∖j (j ∈ T∖S₀) of such T.

## 4. Claims

* **(C1) Start mode.** Under G, (BCS), (P), (θ), (FS-B): P(S* is the unique maximiser of γ₀ on Ω) → 1; on this event
  S̃₀ = S* ⊇ S₀ and |S̃₀∖S₀| = m₀ = p − s₀ − |N₀|. (FAC-B L2 with the block-CS population increments.)
* **(C2) Bulk theorem — unconditional, every p_n ≤ ⌊n/2⌋ (key lemma).** Under G, (BCS), (P), (θ) there are events
  with probability → 1 on which the uncapped §6.10 search from S* has, at every visited set T with m_T := |T∖S₀| ≥ m_e:
  (i) the chosen move is the deletion of a null j ∈ argmin_{j∈T∖S₀} Z²(j; T), with gain ≥ c₂ log n;
  (ii) every addition has gain ≤ −c₂ log n; every truth deletion and truth-out swap has negative gain; every null-out
  swap has gain strictly below the chosen deletion's gain (c₂ = c₂(a, b, c, q) > 0);
  (iii) quantitatively, ℓ(T) ≤ (√ℓ′(m_T) + s_max|δ′_T|)², h(T) ≤ C_h ℓ′(m_T) and |δ′_T| ≤ C_δ √ℓ′(m_T), with explicit
  constants (L4).
  Consequently the path performs exactly m₀ − m_e + 1 … i.e. all its first m₀ − m_e + 1 moves are null deletions
  (it visits sets with m_T = m₀, m₀ − 1, …, m_e − 1). If m_e ≤ 1 (which holds when p_n ≤ n^{c₀}/C₀), the path is a pure
  deletion path ending at S₀, where every feasible neighbour has strictly smaller F.
* **(C3) End phase (conditional).** Under G, (BCS), (P), (θ) and (CC_θ): there is an explicit A*(θ) = A*(θ; a, b, c, q)
  ∈ (0, 1] with A*(θ) → min{1, (q − 1)/(2q − 4)} as θ → 0 (q ≥ 3; = 1 for q ≤ 3; for q = 5: 2/3) such that, if
  limsup log p_n/log n < A*(θ), with probability → 1 the uncapped search from S* is a pure null-deletion path of exactly
  m₀ moves ending at S₀, where every feasible neighbour has strictly smaller F; (i)–(ii) of (C2) hold at every visited
  set. Structural content proved unconditionally (L5): in the end phase, the add statistics of hole elements whose group
  retains a singleton are ≤ (c_m H + s|δ′|)² with c_m < 1 explicit; the retained singletons form a heterogeneous
  group-level compound-symmetry problem with κ_g = d₁/a; multi-member configurations with all members' local
  statistics ≥ 2(1 − ε₂) log p do not exist w.p. → 1 (ε₂ = ε₂(a,b,c,q) > 0).
* **(C4) Consequences.** (i) (H0) holds on the class. (ii) Under the hypotheses of (C3) (incl. (CC_θ)) and the
  implementation premises: D_n ≤ P(𝒦_nᶜ) → 0 with 𝒦_n := {deterministic LS0 with cap a_n scores S₀}; P(𝒪 ∩ {Ŝ⁺ ≠ S₀})
  → 0; and delivery P(Ŝ⁺ = S₀) → 1 under Proposition F's premises (exactly as FAC-B L5.3–L5.4; CAL-free). (iii)
  Unconditionally, when p_n ≤ n^{c₀}/C₀ eventually, the same conclusions hold without (CC_θ).
* **(C5) Frontier (evidence; not proved).** (a) (CC_θ) is the exact obstruction: FAC-A's 1/6 equals "configuration
  union bound + trivial centre bound θ = 1"; numerics N2 observe θ ≤ 0.13 (≤ 0.05 in the bulk) and pure deletion paths
  to S₀ for log p/log n up to 0.92. (b) The constant (q − 1) in the hole bound (sum of a group's deletion levels) is
  nearly attained numerically (hole/level up to 4.2 for q = 5) and limits A*(0) to (q − 1)/(2q − 4) for q ≥ 4; sharper
  within-group control (a gap-type invariant) would be needed beyond. (c) p > n/2, k ≥ 2 factors, iid rows: as FAC-B §5.

**Uniformity in p_n.** (C2) is claimed for every sequence p_n ≤ ⌊n/2⌋ with thresholds n₀ independent of the regime.

## 5. Not claimed

Unconditional consistency on S5 beyond FAC-A's 1/6 (only (C2)'s partial path statement is unconditional for large p);
finite-n bounds; p > n/2; random designs; changes to shipped components.

## 6. Dependencies (statuses verbatim)

As FAC-B STATEMENT §6: T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"; T03♯ "PROVED; SF VERIFIED
(W2-VT03R); XF VERIFIED (A-REV2)"; [OP] "PROVED (by this seat, unchecked)" inside Theorem GEN "PROVED-CHECKED"; Lemma
CAP "PROVED (by this seat)", council-checked; Proposition F (A1 corrected form) and F-GROW "PROVED (A2), checked by A3".
FAC-B Theorem FAC-CS "PROVED-CHECKED" (council 9.3/9.0; HQ audit B3 HOLDS-WITH-AMENDMENTS) — used only as the b = 0
consistency check, not as an input.
