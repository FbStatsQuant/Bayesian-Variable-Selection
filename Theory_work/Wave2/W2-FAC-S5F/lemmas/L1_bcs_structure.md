# L1 — Block compound symmetry: exact structure of every scan statistic (local part + global centre)

Status: **PROVED (by this seat, unchecked)** (v1, 2026-11-09). Falsification numerics: numerics/n3_tools.py →
N3_out.txt Part B (B2 drift identity: κ > 0 and class-constant, matching a·w_u/(1 + aW_T) to 4 digits; B3 ỹ-identity to
2e-14; B4 closed-form add statistic vs the exact scanner to 1e-6 incl. O(1/n) ridge/scale corrections); bcs_core.py
(closed-form scanner built on L1.2–L1.3, verified against FAC-B's general scanner, bcs_selftest_out.txt). Lemma check:
pending (reviews/R02).

Setting: STATEMENT §1–3, hypotheses G, (BCS), (P). Throughout, groups G₁, …, G_J (|G| ≤ q), grp(j) the group of j;
for T ⊆ [p] and a group G: U_G := T ∩ G, u_G := |U_G|; hit groups: u_G ≥ 1; W_T := Σ_{G hit} 1/d_{u_G},
d_u := b + c/u, w_u := 1/(c + bu) (so u w_u = 1/d_u, 1 − b u w_u = c w_u, w_u d_u = 1/u), w₀ := 1/c.

## L1.0 Sign flips
As FAC-B L1.0: replacing X by XΥ and θ* by Υθ* leaves every quantity used by the method (and every Z²) unchanged.
We take Υ_n = I.

## L1.1 Noise representation and Gram-level fit
g := Xᵀε/(σ√(n − 1)) ~ N(0, Σ). Enlarging the probability space (as FAC-B L1.1; it changes no probability of an event
measurable in the data), g = √a η 1 + √b ζ_{grp} + √c ξ with η ~ N(0,1), ζ ~ N(0, I_J), ξ ~ N(0, I_p) independent.
For T ⊆ [p]: ‖P_T e‖² = eᵀX_T G_T⁻¹X_Tᵀe = σ² g_TᵀΣ_{TT}⁻¹g_T =: σ²Φ(T) (Xᵀe = Xᵀε since Xᵀ1 = 0). For T ⊇ S₀,
RSS_T = ‖(I − P_T)e‖² = ‖e‖² − σ²Φ(T) and Z²(l; T) = Φ(T∪l) − Φ(T), Z²(j; T) = Φ(T) − Φ(T∖j) (L0 notation).

## L1.2 Inverse and the exact ANOVA split
For M := aJ + bH_T + c′I on T (c′ > 0): with D := c′⁻¹(I − Σ_G b w′_{u_G} J_{U_G}) (w′_u := 1/(c′ + bu)) and
w̃ := D1 (= w′_{u_G} on U_G), W′ := 1ᵀw̃ = Σ_G u_G w′_{u_G}:
  M⁻¹ = D − a w̃ w̃ᵀ/(1 + aW′),   zᵀM⁻¹z = [Σ_{j∈T} z_j² − Σ_G b w′_{u_G} S_G²]/c′ − a B′²/(1 + aW′),  B′ := Σ_G w′_{u_G} S_G,
  log det M = Σ_{G hit}[(u_G − 1) log c′ + log(c′ + b u_G)] + log(1 + aW′),   S_G := Σ_{j∈U_G} z_j.
(Sherman–Morrison twice; D is the inverse of bH_T + c′I; D1 = w̃ because (bH + c′I)w̃ = 1 on each hit group.) With
c′ = c and z = g, writing ĝ_G := √a η + ỹ_G(U_G), ỹ_G(U) := √b ζ_G + √c ξ̄_U (ξ̄_U := mean of ξ over U), B := Σ_G ĝ_G/d_{u_G}
and c̄_T := aB/(1 + aW_T), a direct expansion (using 1 − b u w_u = c w_u and w_u d_u = 1/u) gives the **ANOVA split**

  Φ(T) = Σ_{G hit} Σ_{j∈U_G} (ξ_j − ξ̄_{U_G})²  +  Σ_{G hit} (ĝ_G − c̄_T)²/d_{u_G}  +  c̄_T²/a.

(The last two terms equal Σ_G ĝ_G²/d_G − aB²/(1 + aW): indeed Σ(ĝ − c̄)²/d = Σĝ²/d − 2c̄B + c̄²W and
−2c̄B + c̄²W + c̄²/a = −2c̄B + c̄²(1 + aW)/a = −2c̄B + c̄B = −c̄B = −aB²/(1 + aW).) The method's quantities use
c′ = c₁ := c + 1/(n² − 1) (for H_T) and c′ = c₂ := c + 1/(n − 1) (for G_T + I); bcs_core implements exactly these.

## L1.3 Every statistic in closed form: local configuration part + global centre
For T ⊆ [p], l ∉ T with G := grp(l), u := u_G ∈ {0, …, q − 1}, U := U_G, define the **residual** and its variance
  r_l(T) := g_l − Σ_{l,T}Σ_{TT}⁻¹g_T = √c(ξ_l − ξ̄_U) + c w_u(ĝ_G − c̄_T)   (u ≥ 1);   r_l(T) = g_l − c̄_T   (u = 0),
  var_l(T) := Σ_ll − Σ_{l,T}Σ_{TT}⁻¹Σ_{T,l} = c(1 + b w_u) + a c² w_u²/(1 + aW_T)   (u ≥ 0, with w₀ = 1/c: = b + c + a/(1 + aW_T)).
Then **Z²(l; T) = r_l(T)²/var_l(T)** (exactly, Schur complement of Σ_{T∪l,T∪l} at l), and for fixed (T, l), r_l(T) ~
N(0, var_l(T)) — the noise part of x̃_lᵀe/(σ√(n−1)) (for T ⊇ S₀ the μ-part vanishes: Z²(l;T) is a pure noise statistic).
*Proof.* Σ_{l,T} = a1ᵀ + b1_{U}ᵀ (restricted to T). Using L1.2: 1ᵀM⁻¹g = B/(1 + aW), 1_UᵀM⁻¹g = w_u S_G − a u w_u B/(1 + aW),
so Σ_{l,T}Σ⁻¹g_T = b w_u S_G + a c w_u B/(1 + aW) = b w_u S_G + c w_u c̄_T. With g_l = √aη + √bζ_G + √cξ_l and
S_G = u(√aη + √bζ_G) + √c u ξ̄_U: g_l − b w_u S_G = c w_u(√aη + √bζ_G) + √c(ξ_l − b w_u u ξ̄_U), and
√c ξ_l − √c b u w_u ξ̄_U − c w_u√c ξ̄_U + c w_u √c ξ̄_U = √c(ξ_l − ξ̄_U) + c w_u √c ξ̄_U; hence r_l = √c(ξ_l − ξ̄_U) +
c w_u(√aη + √bζ_G + √cξ̄_U − c̄_T) = √c(ξ_l − ξ̄_U) + c w_u(ĝ_G − c̄_T). For the variance: 1ᵀM⁻¹1 = W/(1+aW),
1_UᵀM⁻¹1 = u w_u/(1 + aW), 1_UᵀM⁻¹1_U = u w_u − a u²w_u²/(1 + aW), so var_l = (a + b + c) − [a²W + 2ab u w_u − a b² u² w_u²]/(1+aW)
− b²u w_u = c(1 + b w_u) + a(1 − b u w_u)²/(1 + aW) = c(1 + b w_u) + a c² w_u²/(1 + aW). ∎
**Deletion.** For j ∈ T: Z²(j; T) = r_j(T∖j)²/var_j(T∖j), with the configuration U_{G(j)} ∖ {j} (u_G − 1 mates).

**Local statistics.** Put var^{loc}_u := c(1 + b w_u) = c(c + b(u + 1))/(c + bu) (= b + c for u = 0) and
  Z^{loc}_l(U) := [√c(ξ_l − ξ̄_U) + c w_u ỹ_G(U)]/√(var^{loc}_u)   (u ≥ 1),   Z^{loc}_l(∅) := (√bζ_G + √cξ_l)/√(b + c).
(i) Z^{loc}_l(U) is exactly the add statistic of l to U in the **pure block design** Σ⁰ := bH + cI with noise
    g⁰ := √bζ + √cξ (set a = 0 in L1.3); it depends only on (ζ_G, ξ_G) — hence the families {Z^{loc}_l(U)}_{l,U⊆G} are
    independent across groups — and Z^{loc}_l(U) ~ N(0,1) for fixed (l, U).
(ii) **Exact decomposition.** r_l(T) = √(var^{loc}_u) Z^{loc}_l(U) − c w_u δ′_T, where δ′_T := c̄_T − √a η, and
    var_l(T) = var^{loc}_u + a c²w_u²/(1 + aW_T) ≥ var^{loc}_u. Consequently, with š_u := c w_u/√(var^{loc}_u) =
    √c w_u/√(1 + b w_u) (S5: š₀ = 1/√(b+c) = 1.195, š₁ = 0.624, š₂ = 0.426, š₃ = 0.324, š₄ = 0.262; š_max = š₀) and
    ρ_u(T)² := var^{loc}_u/var_l(T) ∈ [(b + c)/(b + c + a), 1]:
      Z_l(T) = ρ_u(T)·[Z^{loc}_l(U) − š_u δ′_T],   so   |Z_l(T)| ≤ |Z^{loc}_l(U)| + š_u|δ′_T|   and   |Z^{loc}_l(U)| ≤ ρ_u⁻¹|Z_l(T)| + š_u|δ′_T|.
(iii) **Local Pythagoras / jump inequality.** By (i) and L0.4 applied to the design Σ⁰ (block diagonal, so sets outside G
    are irrelevant): for U ⊆ G, j ∈ U, l ∈ G∖U: Z^{loc}_l(U∖j)² ≤ Z^{loc}_l(U)² + Z^{loc}(j; U)², where Z^{loc}(j; U) :=
    Z^{loc}_j(U∖j) is the local deletion statistic. Telescoping within the group (L0.4′): if the group's retained set goes
    U⁰ ⊃ U¹ ⊃ … ⊃ Uʳ by deleting d₁, …, d_r (in this order) and l = d_i, then
      Z^{loc}_l(Uʳ)² ≤ Σ_{i′=i}^{r} Z^{loc}(d_{i′}; U^{i′−1})²  ≤ (q − |Uʳ|)·max_{i′≥i} Z^{loc}(d_{i′}; U^{i′−1})².
(iv) **Group mean from member statistics.** For U ≠ ∅, u = |U|:
      ỹ_G(U) = (√(var^{loc}_{u−1})/(c u w_{u−1})) · Σ_{j∈U} Z^{loc}(j; U).
    *Proof.* Σ_{j∈U} √c(ξ_j − ξ̄_{U∖j}) = √c[Σ_jξ_j − Σ_j(Ξ − ξ_j)/(u−1)] = 0 and Σ_j ỹ_G(U∖j) = u√bζ_G + √c(uΞ − Ξ)/(u−1) =
    u ỹ_G(U) (Ξ := Σ_U ξ); for u = 1 read w₀ = 1/c, var^{loc}_0 = b + c. ∎

## L1.4 The global centre: trivial bound and drift identity
c̄_T = aB/(1 + aW_T) with B = √aη W_T + Σ_{G hit} ỹ_G(U_G)/d_{u_G}; hence
  δ′_T = c̄_T − √a η = a Σ_{G hit} ỹ_G(U_G)/d_{u_G}/(1 + aW_T) − √a η/(1 + aW_T).
(Remark, not used: c̄_T = E[√a η | P_T ε] on the enlarged space — a posterior mean with prior N(0, a) and
"observations" ĝ_G ~ N(√aη, d_{u_G}); the within-group contrasts are independent of η.)
**(a) Trivial bound.** |δ′_T| ≤ (aW_T/(1 + aW_T)) max_{G hit}|ỹ_G(U_G)| + √a|η|/(1 + aW_T) ≤ max_{G,U≠∅}|ỹ_G(U)| + √a|η|
(weighted mean with weights (1/d_G)/W_T).
**(b) Drift identity.** For j ∈ T with u := u_{grp(j)}(T) ≥ 1:
  c̄_T − c̄_{T∖j} = κ_T(j)·r_j(T∖j),   κ_T(j) := a w_u/(1 + aW_T) > 0.
*Proof.* Write B′, W′ for T∖j. Then c̄_T − c̄_{T∖j} = a[(B − B′) − (W − W′)c̄_{T∖j}]/(1 + aW_T) (clear denominators).
If u ≥ 2: W − W′ = 1/d_u − 1/d_{u−1} = c w_u w_{u−1}; ĝ_G(U) = ĝ_G(U∖j) + √c(ξ_j − ξ̄_{U∖j})/u; so (B − B′) − (W − W′)c̄′ =
(ĝ_G(U) − c̄′)/d_u − (ĝ_G(U∖j) − c̄′)/d_{u−1} = (ĝ_G(U∖j) − c̄′) c w_u w_{u−1} + √c(ξ_j − ξ̄_{U∖j}) w_u = w_u r_j(T∖j) (L1.3
with configuration U∖j). If u = 1: (B − B′) − (W − W′)c̄′ = (ĝ_j − c̄′)/d₁ = w₁(g_j − c̄′) = w₁ r_j(T∖j). ∎
(N3 B2b: κ constant within each class u and equal to a w_u/(1 + aW_T) to 4 digits.)
**(c) Oscillation bound (consequence).** |c̄_T − c̄_{T∖j}| ≤ κ_T(j)√(var_j(T∖j))|Z_j(T)| ≤ (a w_u/(1 + aW_T))·√(1 + a/(b+c))·... ≤
C_κ |Z_j(T)|/(1 + aW_T) with C_κ := a w_{1}√(b + c + a) ≤ a√2/(b + c); and W_T ≥ m_T/(c + bq)·… precisely W_T ≥ Σ_{G hit} 1/d_max
≥ (m_T/q)/d_max (at least m_T/q hit groups).

## L1.5 Configuration families and the size of each
For a group G, a **configuration** is a nonempty U ⊆ G; the local statistics attached to G are {Z^{loc}_l(U) : U ⊆ G, l ∈ G∖U}
(≤ q 2^{q−1} of them) and the means {ỹ_G(U) : ∅ ≠ U ⊆ G} (≤ 2^q, each N(0, d_{|U|}) with d_{|U|} ≤ d_max := b + c).
Groups containing truths: the retained configuration always contains G ∩ S₀; the formulas of L1.3 hold verbatim (the
noise statistics do not see θ*), and the number of configurations is still ≤ 2^q.

## L1.6 Path-free uniform bounds (used for (TR), (TR′) in L0.6 and in the end phase)
Let E^{loc}_n := {|Z^{loc}_l(U)| ≤ R_loc := √(2 log(2^q p) + 2L_n) for all G, U ⊆ G, l ∈ G∖U; |ỹ_G(U)| ≤ √(d_max)R_loc for
all G, U ≠ ∅; |η| ≤ L_n}. P(E^{loc}_n) → 1 (≤ 2^{q+1}p + 2^q J + 1 Gaussian variables; union bound costs ≤ 3·2^q p·e^{−L_n}·
e^{−log(2^q p)} ≤ 3e^{−L_n} → 0). On E^{loc}_n, **for every T ⊆ [p] and every l ∉ T** (no path information):
  |δ′_T| ≤ √(d_max) R_loc + √a L_n =: Δ_triv,   |Z_l(T)| ≤ R_loc + š_max Δ_triv = R_loc(1 + š_max√d_max) + o(R_loc) = 2R_loc(1 + o(1)),
since š_max√d_max = √(d_max/(b + c)) = 1. The same holds for the truth residual x̃_jᵀe/(σ‖x̃_j‖) = r_j(A)/√var_j(A), j ∈ S₀,
A ∌ j (L1.3 with l = j, T = A). Hence (TR) and (TR′) of L0.6 hold on E^{loc}_n ∩ E⁰_n with R_n = R′_n = 2R_loc(1 + o(1)) = O(√log p).
*Remark.* This is FAC-A's mechanism: configuration union bound (local) + a bound on the factor statistic uniform over all
sets (here the trivial centre bound, θ = 1), giving Z² ≤ 8 log p(1 + o(1)) and hence the exponent 1/6 on the whole
lattice; the path analysis of L4 improves the centre bound at the level scale.

## L1.7 The multiplier on the class
Φ(T) = g_TᵀΣ_{TT}⁻¹g_T ≤ ‖g_T‖²/c (λ_min(Σ) = c), so on {max_j |g_j| ≤ √(2 log(2p) + 2L_n)} (probability → 1, added to
E^{loc}_n): Φ(T) ≤ |T|(2 log(2p) + 2L_n)/c ≤ n/log n whenever |T| ≤ n/log³n (n ≥ n₀), and then M_T ≤ ½(1 + 2/log n) (L0.2).
