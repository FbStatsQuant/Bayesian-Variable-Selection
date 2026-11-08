# L6 — Instances (claim (C5)) — v2

Status (v2, after lemma check R07 (Codex Sol): (a)–(c) VERIFIED-WITH-AMENDMENTS, (d) GAP; and mid-point R05 items
2, 5, 8): (a), (c): **PROVED (by this seat, unchecked)** given the cited partition inputs; (b) **PROVED (by this seat,
unchecked), conditional on** W7-PART Theorem B (candidate) and [CONC]; (d-covered) **PROVED (by this seat, unchecked)
— new selection-uniform argument (Lemma SEL) written in v2 to close R07's GAP; Lemma SEL was checked only inside the
exhaustive sweep R10 (one minor item, fixed); no dedicated lemma check**; (d-not covered):
**PROVED (by this seat, unchecked)** that no bounded certificate satisfies the sufficient conditions (not that the
method fails). Disposition: reviews/R07_disposition.md.

Notation: L ≤ 16 denotes the block cap (B_n); Beta variates are written Z. Common tool (unit algebra): if μ ⊥ span X_W
then δ_{T,l} = 0 for every T ⊆ W, l ∈ W ∖ T.

## (a) LH, exact Gram (BS/W4-T38FULL/T38_PROOF.md:217-235)

Setting as in STATEMENT (C5)(a): X'X = (n − 1)Σ_LH, p ≤ n − 1, groups C_h of size g, within ρ_h ∈ [ρ₋, ρ₊] ⊂ (0,1),
pair units K_i := C_{a_i} ∪ C_{b_i} with rank-one hub link ψ_i, units mutually orthogonal (T38_PROOF.md:224-228);
θ_{a_i} = β_i, θ_{b_i} = −ψ_iβ_i, visible hubs θ_h; c, v, g, ρ's, ψ's, β's fixed; SIZE g ≤ L_n < 2g eventually.
(Inner products below are per n − 1.) Empty minima (e.g. v = 0) are omitted.

* **Partition.** blocks = groups for n large (W1-EXP Lemma 4.2, used by Thm5-LH, status "PROVED; SF: VERIFIED (W3-VEXP);
  XF: none", SAME-FAMILY-ONLY; M5 IC3 row "W1PC2 D4 DESIGN-VERIFIED").
* **Eigenvalue.** λ_min(Σ_LH) ≥ φ₀² := (1 − max_i|ψ_i|)(1 − ρ₊) > 0 (W1-EXP Lemma 4.1(a), cited at T38_PROOF.md:267;
  R07 re-derived it: in a pair unit the cross term is ≥ −2|ψ|‖u‖_a‖v‖_b, so the quadratic form is ≥ (1 − |ψ|)(‖u‖²_a +
  ‖v‖²_b) ≥ (1 − |ψ|)(1 − ρ₊)‖·‖²). Fixed constant; g₀ := φ₀² eventually.
* **(H0).** R1 (s₀ = 2c + v fixed, p ≤ n − 1, s₀ ≤ K eventually); R (‖μ‖² = (n − 1)θᵀΣθ); SE_λ(j₀), SE_w(m♯; g₀)
  at every order by interlacing; BM-∞ (θ* = θ fixed nonzero on S₀; columns standardized). (S-T IC3 row: "LH satisfies
  fixed sparsity, bounded energy, positive full Gram eigenvalue and BM-∞".)
* **(H1)** with 𝒱 := ∪_i K_i ∪ ∪_h C_h, |𝒱| = g(2c + v): (H1a) by φ₀²; (H1b) with ζ_n = 0, c_S = 0: null columns are
  orthogonal to every column of 𝒱 and to μ.
* **(H2)** with S* := S₀ ∖ M (M = {b_i}) — equivalently S*_can of L8.1 — on blocks = groups. (H2a): λ_min = 1 − ρ_h.
  - b-groups (U* = ∅): ⟨x_k, μ_i⟩ = 0 for every k ∈ C_{b_i} (k = b_i: ψ_i − ψ_i; k ≠ b_i: ψ_iρ_{b_i} − ψ_iρ_{b_i});
    other units orthogonal; so μ ⊥ span X_{C_{b_i}}: all leakage δ = 0; VIS vacuous.
  - a-groups (U* = {a_i}): μ_i = β_i(1 − ψ_i²)x_{a_i} − β_iψ_iw_i, w_i := x_{b_i} − ψ_ix_{a_i} ⊥ span X_{C_{a_i}}. For T ∋ a_i,
    (I − P_T)x_l ⊥ x_{a_i}, w_i, other units: δ = 0. VIS: for U ∌ a_i, ρ := (I − P_U)x_{a_i}: ⟨ρ, μ⟩ = β_i(1 − ψ_i²)‖ρ‖²,
    g = β_i²(1 − ψ_i²)²‖ρ‖² ≥ β_i²(1 − ψ_i²)²(n − 1)(1 − ρ₊).
  - visible groups (U* = {h}): δ = 0 for T ∋ h; g = θ_h²‖(I − P_U)x_h‖² ≥ θ_h²(n − 1)(1 − ρ₊).
  - null groups: μ ⊥ span X_C: δ = 0; VIS vacuous.
  v_U ≤ σ² + θᵀΣθ·n/(n − 1); VIS with M_n := c_LH(n − 1)/(2 log n), c_LH := (min over the nonempty signal
  collections of β_i²(1 − ψ_i²)², θ_h²)(1 − ρ₊)/(σ² + θᵀΣθ). (H2c): η = 0, so NL_C (C_L = 0) and NL_avg(κ), κ ≤ ½.
* **Conclusion.** (C3) applies with S* = S₀ ∖ M: masked LH is an instance; this recovers M5(b1-LH) under the same
  premises (incl. N3).

## (b) LH-iid (BS/API-PXNGAP/PROOF.md:36-60), SIZE, 18 ≤ p ≤ n^A

Rows of X^r iid N(0, Σ_LH), independent of ε. **Raw model** (as in the source, PROOF.md:48-50): y^r = X^rθ + ε with
fixed raw θ, μ = CX^rθ, θ* = D_xθ (sample scales) — exact population cancellations refer to raw columns.

**Group versions first (Lemma T discipline, PROOF.md:104-119).** All leakage/SEP/VIS quantities below are defined with
the deterministic groups C_h in place of the blocks ("group versions"); their laws are computed unconditionally; the
partition-recovery event is intersected only at the end.

* **Beta law for fixed pairs.** For each fixed pair (T, l) of the group families — (i) S ⊆ 𝒱, l a null-group column
  (SEP); (ii) the group-version leakage triples of 𝓛(S*) — the raw population residual w of x^r_l on X^r_T has iid
  Gaussian rows and is independent of (X^r_T, μ): null groups are independent of the signal units (F5); for b-groups the
  whole group has zero covariance with μ_i (F2), hence (Gaussian) is independent of it; for a-groups write
  x_b = ψx_a + z with z independent of the a-group: if a ∈ T, w is independent of X_T and of z, hence of x_b and μ;
  visible groups likewise. Given (X^r_T, μ), (I − P_T)Cw is isotropic in E := 1^⊥ ⊖ span X_T (standardizing columns
  changes neither E nor the direction), so δ²_{T,l} = Λ_T·Z_{T,l}, Z_{T,l} ~ Beta(½, (n − 2 − |T|)/2); if Λ_T = 0 then
  δ = E = 0.
* **Tails.** Z = χ²₁/(χ²₁ + χ²_{m−1}) ≤ 2χ²₁/(m − 1) on {χ²_{m−1} ≥ (m − 1)/2} (P ≥ 1 − e^{−(m−1)/16}); with t := 4(A + 3) log n and the union over
  ≤ 2^{|𝒱|}p + p2^L fixed pairs, max Z ≤ 16(A + 3) log n/n w.p. → 1 (m ≥ n/2 eventually).
* **Exponential moment.** E_{T,l} ≤ δ²/(2Δ_T) = (n − 1)Z/2. For Z ~ Beta(½, (m − 1)/2), m := dim E:
  E e^{(n−1)Z/2} ≤ e^{(L+3)/2}·√(m/(2π))·(Γ(¼)/2)(4/(m − 3))^{1/4} = O(n^{1/4}) [Γ(m/2)/(√πΓ((m − 1)/2)) ≤ √(m/(2π));
  (n − 1)z/2 + ((m − 3)/2)log(1 − z) ≤ (L + 3)/2 − (m − 3)z²/4; ∫₀^∞z^{−1/2}e^{−(m−3)z²/4}dz = (Γ(¼)/2)(4/(m − 3))^{1/4}]
  (R07 item 3 verified these constants).
* **The X-event** 𝒜_n := ℛ_n ∩ 𝒞_n ∩ 𝒮_n ∩ 𝒩_n ∩ 𝒱𝒮_n, each defined by explicit inequalities:
  - ℛ_n := {blocks = groups}; P(ℛ_nᶜ) → 0 by Theorem R = W7-PART Theorem B (**candidate**; A-REV6 "VERIFIED on SIZE";
    PROOF.md:77-100).
  - 𝒞_n := {λ_min(R̂_T) ≥ λ₀/2 ∀|T| ≤ min(p, m♯_n + s₀ + j₀ + |𝒱| + 1); ‖μ‖²/n ≤ M; θ*²_min ≥ b₀} with
    λ₀ := (1 − max|ψ|)(1 − ρ₊), M := 2θᵀΣθ + 1, b₀ := ½min_{j∈S₀}θ_j²; P → 1 by [CONC] (max|r̂_jk − Σ_jk| ≤ C√(log p/n),
    operator error O(log n)·C√(log p/n) = o(1) at these orders) and the SLLN for the fixed signal columns (as in
    API-PXNGAP Lemma P2, PROOF.md:213-220, "verified by A-REV3"); m♯_n = O(log n).
  - 𝒮_n := {ζ_n ≤ 16(A + 3)M log n} (group version; then SEP holds with c_S = ½ eventually, uniformly on 𝒮_n ∩ 𝒞_n).
  - 𝒩_n := {max over group-version 𝓛(S*) of δ² ≤ C_Lσ² log n} ∩ {(p − s*)⁻¹Σ_l max_T e^{E_{T,l}} ≤ n^{3/8}},
    C_L := 16(A + 3)M/σ²; P(𝒩_nᶜ) → 0 by the tail bound and by Markov: E[average] ≤ 2^L·O(n^{1/4}) (max ≤ sum over
    ≤ 2^L sets T), so P(average > n^{3/8}) = O(n^{−1/8}). (κ = 1/8; ε₀ = 1.)
  - 𝒱𝒮_n := {g_{b,U} ≥ c_V(n − 1)/2 for the finitely many (fixed) sets U ⊆ C_h of a- and visible groups (h fixed
    indices)}, c_V := the minimal population gain of (a) > 0; P → 1 by the SLLN (fixed finitely many raw columns).
  On ℛ_n the block objects equal the group versions, so every deterministic design sequence in 𝒜_n satisfies
  (H0)–(H2) with S* = S₀ ∖ M, 𝒱 = signal units, fixed constants φ₀² = λ₀/2, g₀ = λ₀/2, M, v̄ = g(2c + v), c_S = ½,
  C_L, κ = 1/8, ε₀ = 1, and envelopes BM: b₀λ₀n/(2σ² log n), VIS: M_n := c_V(n − 1)/(2v̄_y log n), v̄_y := σ² + 2M.
* **Conclusion.** (C4) gives (C3) under the joint law, **conditional on W7-PART Theorem B (candidate)** and [CONC]. (It
  does not use API-PXNGAP's P3′ or Lemma LS.)

## (c) W (exact Gram; BS/MEET-THM/THEOREM_LIST_FINAL.md:71,178; R1_C.md:362-364)

Groups of 9 within ¼, every cross-group correlation ε_n ∈ {1/(np), n^{−1/2}/p}, two truths j₁, j₂ in different groups
with θ = n^{−1/4}, σ² = 1, p = 9⌊n^{1/3}/9⌋, n ≥ 9⁶.
* **Partition (proved inline; TLF:71 states it without a separate status).** Exact Gram: within-group distance
  1 − ¼ = ¾ < 1 − ε_n = cross-group distance, so complete linkage completes every group before any cross merge; for
  n ≥ 9⁶, p ≥ 81 and B = min(⌊√n⌋, ⌊√p⌋, 16) ∈ [9, 16]; a group node (size 9 ≤ B) is retained and every union of ≥ 2
  groups (size ≥ 18 > B) is split; next-fit cannot place two groups in one block (9 + 9 > B). So blocks = groups.
  (Ties among the equal within-group distances only affect the order of merges inside a group.)
* **Spectrum.** Σ_n has eigenvalues 3/4 (within-group contrasts), 3 − 9ε (group-constant contrasts orthogonal to 1),
  3 + (p − 9)ε (all-ones); so λ_min(Σ_n) = 3/4 eventually for both ε-variants (R07 item 5). Fixed φ₀² := ½, g₀ := ½.
* **(H0)** directly (no S-T row for W, SoP 04_theory.tex:846): s₀ = 2; p < n (A = 1); R: ‖μ‖² = (n − 1)θ²(2 + 2ε_n)
  ≤ Mn; SE_λ, SE_w at every order; BM-∞: θ²nφ₀²/(σ² log n) = √n/(2 log n) → ∞.
* **(H2)** with S* = S₀ ((C3-fav); (H1) not needed). (H2a): λ_min(Σ_C) = 3/4. For U ⊆ group G (|U| = q ≤ 8), k ∈ G ∖ U
  and j ∉ G: ⟨(I − P_U)x_k, x_j⟩ = (n − 1)[Σ_kj − Σ_{kU}Σ_UU⁻¹Σ_{Uj}] = (n − 1)·3ε_n/(3 + q) ≤ (n − 1)ε_n
  (Σ_{kU}Σ_UU⁻¹ = 1ᵀ/(3 + q)); ‖(I − P_U)x_k‖² ≥ (n − 1)·¾.
  - VIS at j₁'s block (U ∌ j₁): ⟨ρ, μ⟩ = θ(‖ρ‖² + ⟨ρ, x_{j₂}⟩) with |⟨ρ, x_{j₂}⟩| ≤ (n − 1)ε_n, so
    g = ⟨ρ, μ⟩²/‖ρ‖² ≥ θ²(n − 1)(¾)(1 − o(1)) ≍ √n; v_U ≤ 1 + 3θ²; VIS with M_n := √n/(4 log n).
  - Leakage: l in j₁'s block, T ∋ j₁: δ² = θ²⟨u, x_{j₂}⟩² ≤ θ²(n − 1)ε_n²·(4/3) → 0; l in a null block:
    δ² ≤ θ²((n − 1)ε_n + (n − 1)ε_n)²/((n − 1)·¾) = (16/3)θ²(n − 1)ε_n² → 0. Hence NL_η for any fixed
    η ∈ (0, (√3 − √2)²) eventually (A = 1), and NL_C and NL_avg(κ) for 0 < κ ≤ ½ − η/2 − √(2η(1 + ε₀)) with small ε₀
    (T22iii PROOF_v2.tex:404-425). (Also L8.2 with γ^L = θe_{j}.)
* **Conclusion.** (C3-fav): P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 on W — new relative to the regime map (SoP 04_theory.tex:846: W,
  layer (iii) "not covered").

## (d) The study generator (Scripts/Data_generators/gen_dev_data.R:18-61)

**Sequence** (STATEMENT (C5)(d), as locked after sweep R10 item 6): a theoretical sequence extending the study's
high-p layout — it is not a property of the R function beyond its domain p ∈ {30, 500, 1000}. Groups of 5 consecutive
indices; p_n = 5G_n → ∞, p_n ≤ n^A, p_n large enough to contain the fixed signal indices; s₀ = 14 with one of the
two study layouts at fixed indices (step 7 (p = 500 layout) or step 13 (p = 1000 layout); positions and the 14-entry pattern β^pat = (1.4, −1.0, 1.8, −1.2, 0.8,
−1.6, 1.4, −1.0, 1.8, −1.2, 0.8, −1.6, 1.4, −1.0) as in the R code) and fixed scale c; iid N(0, Σ_s) rows; σ² = 1;
signal = c·X_std β^pat (R:54-61), so θ* = cβ^pat exactly and μ = X_{S₀}θ* ∈ span X_{S₀} (β_raw X-measurable, (C4)).

### Covered: S1, S3, S4, S6 — by (C3-fav) via (C4) with S* = S₀

Scenarios (R:22-30): S1 Σ = I; S3 within 0.7; S4 within 0.85; S6 within ρ_h ∈ {0.4, …, 0.9}; between 0. λ_min(Σ_s)
≥ 0.1. Let 𝒢_n := {max_{j,k}|r̂_jk − Σ_jk| ≤ C√(log p/n)} ([CONC]); P(𝒢_n) → 1. On 𝒢_n, all sample partial
correlations among ≤ 40 columns given ≤ 20 columns are within C′√(log p/n) of their population values, uniformly
(smooth functions of a correlation submatrix with eigenvalues ≥ 0.05).

* **Partition (S3/S4/S6).** On 𝒢_n (within ≥ 0.4 − o(1) > between = O(√(log p/n))), complete linkage completes every
  group before any cross merge (PXN P1(a), BS/API-PXNGAP/PROOF.md:89-91), so every node is a subset of a group or a
  union of whole groups; the top-down cut splits only nodes of size > L, a group node has size 5 ≤ L (n, p ≥ 25), so
  every retained cluster is a union of whole groups, and next-fit packs whole clusters: **every block is a union of
  whole groups** (R07 item 7: verified). S1: any partition.
* **(H0), (H2a)** on 𝒢_n as in (b) (φ₀² := 0.05, θ*_min = c·0.8 fixed).
* **VIS at S* = S₀** (uniformly over all admissible U, not only selected ones). For a truth j in block b and U ⊆ C_b,
  j ∉ U, |U| ≤ 16: g_{b,U} ≥ ‖(P_{U+j} − P_U)μ‖² = ⟨(I − P_U)x_j, μ⟩²/‖(I − P_U)x_j‖². Population: the partial covariance
  of x_j with μ given X_U is θ*_jVar(x_j | X_U) (other truths lie in other, independent groups, ≤ one truth per group;
  in S1 everything is independent), and Var(x_j | X_U) ≥ 0.1. On 𝒢_n, for **all** such (j, U) simultaneously, the sample
  versions are within C′√(log p/n) relatively, so g_{b,U} ≥ (n − 1)θ*²_j·0.1/2 for n ≥ n₀. v_U = σ² + Λ_U/(n − 1) ≤
  v̄_y := 1 + 2M on {‖μ‖²/n ≤ M} (an X-event, M := 2c²β^patᵀΣ_sβ^pat + 1; P → 1 by [CONC]). VIS with M_n := 0.05θ*²_min(n − 1)/(v̄_y log n).
* **NL at S* = S₀: Lemma SEL (selection-uniform leakage).** Leakage triples (b, T, l): l ∈ C_b ∖ S₀, S₀ ∩ C_b ⊆ T ⊆
  C_b ∖ {l}. For such (T, l) let G_l be l's group (S1: G_l := {l}), 𝒮𝒢 := union of the 14 signal groups (S1: S₀), and
  T₀ := T ∩ (G_l ∪ 𝒮𝒢), T_x := T ∖ T₀ (members of other null groups that the realised packing put in the block;
  |T_x| ≤ 15). Note S₀ ∩ C_b ⊆ T₀ and, since blocks are unions of whole groups, l's group-mates and (if G_l is a
  signal group) its active truth are in C_b. Define 𝒯₀(l) := {T₀ ⊆ (G_l ∪ 𝒮𝒢) ∖ {l} : |T₀| ≤ 15, T₀ ⊇ S₀ ∩ G_l} — a **deterministic**
  family of size ≤ 2^{75} (a constant), containing every T₀ that can arise from any packing.
  Convention: Q_{T₀,l} := δ²_{T₀,l}/Λ_{T₀} if Λ_{T₀} > 0 and Q_{T₀,l} := 0 otherwise (e.g. T₀ ⊇ S₀).
  (i) *Fixed-pair Beta law.* For fixed l and T₀ ∈ 𝒯₀(l) with Λ_{T₀} > 0 (T₀ ⊇ S₀ ∩ G_l by definition of 𝒯₀(l)): the raw population residual w of x_l on
  X_{T₀} depends only on G_l's columns (groups independent) and, if G_l is a signal group, its active truth is in T₀;
  hence w is independent of (X_{T₀}, all truth columns) and so of μ (θ* = cβ^pat and the sample scales of the truth
  columns are functions of the truth columns). As in (b), Q_{T₀,l} = Z ~ Beta(½, (n − 2 − |T₀|)/2), and
  E e^{(n−1)Q/2} = O(n^{1/4}); when Λ_{T₀} = 0, Q = 0 trivially satisfies the same tail and moment bounds.
  (ii) *Perturbation.* Write ρ_{T,l} for the sample partial correlation of x_l and μ given X_T (when Λ_T > 0), so that
  the first branch of E is E_{T,l} ≤ (n − 1)ρ²_{T,l}/2. If T₀ ⊇ S₀ then μ ∈ span X_{T₀} ⊆ span X_T and
  δ_{T,l} = δ_{T₀,l} = 0. Otherwise Λ_{T₀}, Λ_T ≥ (n − 1)·0.1·θ*²_min/2 on 𝒢_n (a truth is omitted; SE), and by the
  recursive partial-correlation formula (exact for sample vectors), with a := partial correlations of (x_l, X_{T_x})
  given X_{T₀}, b := those of (μ, X_{T_x}) given X_{T₀}, R := partial correlation matrix of X_{T_x} given X_{T₀}:
    ρ_{T,l} = [ρ_{T₀,l} − aᵀR⁻¹b] / √((1 − aᵀR⁻¹a)(1 − bᵀR⁻¹b)).
  The population values of a and b are 0 (columns of T_x lie in other null groups, independent of x_l, μ and X_{T₀}),
  and λ_min(R) ≥ 0.05; so on 𝒢_n, ‖a‖, ‖b‖ ≤ C″√(log p/n) uniformly over all admissible (T, l), and
    |ρ_{T,l} − ρ_{T₀,l}| ≤ C‴(log p/n)(1 + |ρ_{T₀,l}|).
  (iii) *Uniform size of ρ_{T₀,l}.* By (i) and the tail bound, on an event 𝒦_n with P → 1, Q_{T₀,l} ≤ 16(A + 3) log n/n
  (Q_{T₀,l} = ρ²_{T₀,l} when Λ_{T₀} > 0) for all l and all T₀ ∈ 𝒯₀(l) (a deterministic family of size ≤ 2^{75}p).
  Hence on 𝒢_n ∩ 𝒦_n, for every leakage triple, E_{T,l} ≤ (n − 1)ρ²_{T₀,l}/2 + ω_n with
  ω_n := n·C‴(log p/n)(1 + o(1))·(2√(16(A+3) log n/n) + C‴ log p/n) = O((log n)^{3/2}/√n) → 0, and
  δ²_{T,l} = Λ_Tρ²_{T,l} ≤ Mn·2·16(A + 3) log n/n = 32(A + 3)M log n =: C_Lσ² log n (NL_C), using
  ρ²_{T,l} ≤ (|ρ_{T₀,l}| + O(log p/n))² ≤ 2·16(A + 3) log n/n eventually.
  (iv) *Average.* max_{T} e^{E_{T,l}} ≤ e^{ω_n} Σ_{T₀∈𝒯₀(l)} e^{(n−1)Q_{T₀,l}/2}, whose expectation is ≤ 2^{75}·O(n^{1/4})
  by (i); Markov gives P((p − s₀)⁻¹Σ_l max_T e^{E_{T,l}} > n^{3/8}) → 0: NL_avg(1/8). ∎(SEL)
* **The X-event and (C4).** 𝒜_n := 𝒢_n ∩ 𝒦_n ∩ {NL_avg(1/8) inequality} ∩ {‖μ‖²/n ≤ M} ∩ {λ_min(R̂_T) ≥ 0.05 for all
  |T| ≤ min(p, m♯_n + s₀ + j₀)} — all X-measurable with P → 1 ([CONC], as in (b)). On 𝒜_n every deterministic design satisfies (H0), (H2) with S* = S₀ and the fixed constants
  (φ₀² = 0.05, g₀ = 0.05, M := 2c²β^patᵀΣ_sβ^pat + 1, C_L, κ = 1/8, ε₀ = 1) and envelopes (BM: θ*²_min n·0.05/log n;
  VIS as above). (C4) gives (C3-fav) under the joint law: **the covered scenarios are in the favourable regime
  asymptotically** — the start mode is S₀ w.p. → 1, no masking survives as n → ∞.
* **σ²-dilution is a finite-n effect.** VIS's ratio g/(v_U log n) ≍ θ*²_j n/(v̄_y log n) grows without bound, but at
  n = 200 it is O(1) because v_U contains every other truth's signal (dilution). numerics/ reports the ratios at the
  study sizes.

### Not covered: S2 (AR(1), ρ = 0.5) and S5 (within 0.7, between 0.3) — no bounded certificate exists

(These are statements about the sufficient class, not about the method's behaviour.)
* **S5.** For a column l in a null group, the population covariance with μ is 0.3·c·Σ_jβ^pat_j = 0.24c ≠ 0 (the
  14-entry pattern sums to 0.8). On 𝒢_n every null-group column has ⟨x_l, μ⟩/(n − 1) ≥ 0.12c eventually, so for any
  block with U*_b = ∅ the leakage triple (b, ∅, l) has δ²_{∅,l} ≥ (n − 1)(0.12c)² ≫ C_L log n: (H2c)(i) fails unless
  every block containing a null-group column meets S*. All but O(1) columns are null-group columns, so
  s* ≥ (p − O(1))/L → ∞, for **any** reference S* (proxies allowed) and any 𝒱. (R07 item 10; the earlier SEP sentence
  was deleted: SEP can hold at particular S, e.g. omitting truths with coefficients summing to 0.)
* **S2.** Let j_max be the last truth. For l > j_max the population covariance with μ is q·2^{−(l − j_max)},
  q := cΣ_kβ^pat_k2^{−(j_max − j_k)}; the last coefficient is −1.0 and its predecessor is ≥ 32 positions earlier, so
  |q| ≥ c(1 − Σ_{k<14}|β^pat_k|2^{−32}) > 0. For 1 ≤ l − j_max ≤ D_n := min(p_n − j_max, ⌊α log₄ n⌋) (fixed α ∈ (0,1)),
  the absolute covariance is ≥ |q|n^{−α/2}, which dominates the uniform O(√(log p/n)) sample error; so δ²_{∅,l} ≥ c₁n^{1−α}
  ≫ log n on 𝒢_n. Each such column in a block with U*_b = ∅ violates (H2c)(i); hence ≥ ⌈D_n/L⌉ → ∞ blocks must meet S*,
  so no bounded S* exists. (No partition assumption used.) Frontier: relevance/centre sets growing like log n.

**At n = 200**: no asymptotic clause gives a number; M5(0)/N200 remains the finite-n account (SoP 04_theory.tex:851).
