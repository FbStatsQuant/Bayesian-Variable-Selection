# L5 — Random design (claim (L5)) and instances (claim (I))

Status: **PROVED (by this seat, unchecked)** — v1.1, 2026-11-09; lemma check R04 (Codex gpt-6.1-sol high,
reviews/R04_L5L6L7_check_sol.md): all parts VERIFIED or VERIFIED-WITH-AMENDMENTS, amendments applied (R04 also
reproduced the exact S5 minima 2023/32500 and 7/2080 by an independent rational enumeration with a different but
equivalent closed form). Certificates: numerics/tv_cert.py → TV_cert_out.txt;
κ: numerics/kappa.py → kappa_out.txt (numerical illustration; the proof below is algebraic).

## L5.0 Uniformity remark (used for de-randomisation)

Every probability bound and every threshold n₀ in L1 (Corollary U), L2, L3 and L4 depends on the design X only through
the constants (γ̄, ψ₀, κ̄, A, α₁ (from (P)), M, s₀, σ², the BM-∞ envelope θ*²_min n/log n, the TV envelope M_n, the
(AG) envelope δ_n) and through n, p. Hence: if 𝒜_n is a set of designs on which these hypotheses hold with common
constants and envelopes, then
  sup_{x∈𝒜_n} P(Sand_nᶜ ∪ NA(𝓛)ᶜ ∪ TL(𝓛)ᶜ | X = x) → 0.                                                    (0.1)
Dependency table (R08 suggestion 2):
| bound / threshold | depends on |
|---|---|
| L1 Corollary U: event probability ≥ 1 − 4/log n; envelope ε_n | γ̄, ψ₀ (L_ψ), κ̄ (κ'_bd ≤ κ̄/√ψ₀), δ_n, n, p |
| L2: [GEN-L1] events 𝒟₁–𝒟₃ on the block family; 𝓩; n₀ | M, φ₀² = 3ψ₀/4, A, σ², block size 16, family size ≤ 2^{16}p; M_n (TV) |
| L3.0: (E1), (E2), E_Y, η_n, s̄ | φ₀, M, σ², n, p |
| L3.1 NA n₀ | α₁, ε (from α₀(κ̄)), C_ω (M, σ²), ε_n |
| L3.2 TL n₀ | BM-∞ envelope θ*²_min n/log n, φ₀, s̄, σ², Z̄_n (γ̄, κ̄, ψ₀, p) |
| L4 | inputs above; T03♯ constants (A, M, φ₀, g₀, s₀, BM envelope) |

## L5.1 Random design (claim (L5))

**Setting.** Rows of X^r iid N(m, Σ_n), Σ_n ∈ 𝔉(γ̄, ψ₀, κ̄) a correlation matrix; X the standardised design; ε ⊥ X^r;
fixed s₀, σ² > 0, fixed nonzero θ*_{S₀}; (P); (TV-pop) with 𝔅_n, 𝓔'_n, τ₀.

**Design events.** By Lemma CR / [CONC′] (PXN lemmas/CR_corr_tails.md, "PROVED (by this seat); XF VERIFIED (R19)"),
since p ≤ n^A with A := 1 (implied by (P)), with δ'_n := 32√(2(A + 1) log n/(n − 1)):
  P(max_{j<k}|R̂_jk − (Σ_n)_jk| > δ'_n) ≤ 3n^{−2}.
On the complement, ‖R̂ − Σ_n‖_op ≤ ‖R̂ − Σ_n‖_F ≤ pδ'_n =: δ_n, and δ_n√(p log log n) = p^{3/2}δ'_n√(log log n) → 0
because p ≤ n^{α₁} with α₁ < 1/6 (so p^{3/2} ≤ n^{1/4}). Let 𝒜_n := {max|R̂ − Σ_n| ≤ δ'_n} ∩ 𝓔'_n; P(𝒜_n) → 1.

**Hypotheses on 𝒜_n with common constants (n ≥ n₀).**
(i) (AG) with δ_n as above.
(ii) (H0): λ_min(R̂) ≥ ψ₀ − δ_n ≥ 3ψ₀/4 on all subsets ⇒ anchored eigenvalue conditions (normalised ≥ 3ψ₀/4,
unnormalised ≥ (n − 1)3ψ₀/4 ≥ g₀); energy: ‖μ‖² = (n − 1)θ*_{S₀}ᵀR̂_{S₀S₀}θ*_{S₀} ≤ (n − 1)s₀‖θ*‖² =: Mn-type bound with M := s₀‖θ*‖²
(‖R̂_{S₀S₀}‖ ≤ s₀ since its entries are bounded by 1 in absolute value; R08 suggestion 1); BM-∞ since θ* is fixed and nonzero; s₀ ≤ K.
(iii) (TV) on the actual blocks: on 𝓔'_n every realised block C belongs to 𝔅_n. For j ∈ S₀ ∩ C and U ⊆ C ∖ {j},
δ_{U,j} = u_{U,j}ᵀμ = √(n − 1) f(R̂_V), V := U ∪ {j} ∪ S₀ (|V| ≤ 16 + s₀), with
f(M) := (M_{j,S₀}θ* − M_{jU}M_UU⁻¹M_{U,S₀}θ*)/√(M_jj − M_{jU}M_UU⁻¹M_{Uj}),
and f(Σ_V)² = (Σ_{jμ|U})²/Σ_{jj|U} ≥ τ₀ by (TV-pop). On {‖M − Σ_V‖_op ≤ |V|δ'_n ≤ ψ₀/4}, f is Lipschitz with a
constant depending only on (ψ₀, |V|, ‖θ*‖) (the same Schur-complement bounds as L1 U(d): regression vector norm
≤ 1/√λ_min, Schur complement ≥ λ_min ≥ 3ψ₀/4). Hence |f(R̂_V) − f(Σ_V)| ≤ C(16 + s₀)δ'_n → 0 and
δ²_{U,j} ≥ (n − 1)τ₀/2 for n ≥ n₀. Put M_n := (n − 1)τ₀/(2 log n) → ∞ (deterministic, common).
(iv) The partition is a deterministic function of X; L2's block events are conditional on X.

**Proposition L5.1.** Under the setting, P(Sand_n ∩ NA(𝓛) ∩ TL(𝓛)) → 1 and, with the method premises (interpreted
conditionally on X), D_n → 0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 and liminf P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − limsup P(U_n), under the
joint law of (X^r, ε) and the algorithm's randomness.
*Proof.* P(failure) ≤ P(𝒜_nᶜ) + sup_{x∈𝒜_n} P(failure | X = x) → 0 by (0.1) and (i)–(iii). For the posterior term,
E[1 − π(S₀)] ≤ P(𝒜_nᶜ) + sup_{x∈𝒜_n} E[1 − π(S₀) | X = x]; if the sup did not tend to 0, a deterministic sequence
x_n ∈ 𝒜_n with E[1 − π(S₀) | x_n] ≥ η > 0 along a subsequence would satisfy (H0) with common constants, contradicting
T03♯ (1 − π(S₀) = O_P(√(log n/n)) along every such sequence, bounded by 1) — the every-sequence/common-envelope
argument of FINAL s3 "Random designs" (GEN (C4), C-PACK I-c; C-MIS Lemma DR). [OP] and M5(0) hold for every fixed X,
hence after integration: D_n ≤ P(LS0 misses S₀) → 0 and P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) ≤ 2E[1 − π(S₀)] + D_n → 0. ∎

## L5.2 Instances

**Lemma κ (block compound symmetry).** For Σ = ρ_b11ᵀ + (ρ_w − ρ_b)H + (1 − ρ_w)I (0 < ρ_b < ρ_w < 1, H the indicator of
groups of size ≤ γ̄), the representation λ = √ρ_b 1, Ψ = bH + dI (b := ρ_w − ρ_b, d := 1 − ρ_w) is admissible with
λ_min(Ψ) ≥ d > 0 (equality whenever some group has ≥ 2 members; R04 item 2) and κ = 1. Compound symmetry (1 − a)I + a11ᵀ is the case of singleton groups (λ = √a 1, Ψ = (1 − a)I).
*Proof.* For U ⊆ g ∖ {l}, |U| = u: Ψ_UU = dI + b11ᵀ, Ψ_UU⁻¹1 = 1/(d + ub), Ψ_{lU} = b1ᵀ. Hence
λ̃_{l|U} = √ρ_b(1 − ub/(d + ub)) = √ρ_b d/(d + ub), ψ_{l|U} = (b + d) − b²u/(d + ub) = d(d + (u + 1)b)/(d + ub).
For ∅ ≠ V ⊆ g, |V| = v: λ_VᵀΨ_VV⁻¹λ_V = ρ_b v/(d + vb), increasing in v, so c_min = ρ_b/(d + b) = ρ_b/(1 − ρ_b).
Then λ̃²/(ψ c_min) = d(d + b)/[(d + ub)(d + (u + 1)b)] ≤ 1 with equality iff u = 0. (Singleton groups: u = 0 only.) ∎
Consequently α₀(1) = 1/6 for all block CS (incl. CS and S5).

**(I)(a) Exact-Gram compound symmetry.** (AG) with δ_n = 0, Σ_n = (1 − a)I + a11ᵀ ∈ 𝔉(1, 1 − a, 1); (H0) for fixed
nonzero θ*_{S₀} (energy (n − 1)θ*ᵀΣθ* ≤ (n − 1)s₀‖θ*‖², BM-∞, eigenvalues ≥ 1 − a). (TV) from (GC-CS): the population
partial covariance of x_j (j ∈ S₀) with μ given x_U (U ⊆ [p] ∖ {j}, |U| = u) is
  Σ_{jμ|U} = (1 − a)θ*_j + aΘ − (a/(1 − a + ua))[(1 − a)Θ_U + uaΘ] = (1 − a)[θ*_j + a(Θ − Θ_U)/(1 − a + au)],
(using Σ_{jU}Σ_UU⁻¹ = (a/(1 − a + ua))1ᵀ, (Σθ*)_i = (1 − a)θ*_i + aΘ, Θ_U := Σ_{i∈U}θ*_i), and Σ_{jj|U} ≤ 1, so with
exact Gram δ²_{U,j} = (n − 1)(Σ_{jμ|U})²/Σ_{jj|U} ≥ (n − 1)(1 − a)²g₀², g₀ := minimum of the ABSOLUTE values of the (GC-CS) expressions over the configurations realised at some n in the
sequence (R04 item 1), i.e. over
j ∈ S₀, V ⊆ S₀ ∖ {j} and the *feasible* sizes u ∈ {|V|, …, min(15, |V| + p − s₀)} (R05 item 3: a conditioning
set with |V| truths and u − |V| nulls exists only if u − |V| ≤ p − s₀); finitely many distinct values as p varies,
> 0 by (GC-CS) (which quantifies over actual subsets U ⊆ [p] ∖ {j}). For p → ∞ the restriction is eventually void. Every block has size ≤ 16,
so |U| ≤ 15. Hence Theorem L4.1 applies: for p ≤ n − 1 with limsup log p/log n < 1/6. Numerical values of g₀ for the
diagnostic and study patterns: numerics/TV_cert_out.txt.

**(I)(b) Iid rows, compound symmetric Σ.** Proposition L5.1 with 𝔅_n := all sets of size ≤ 16, 𝓔'_n := everything,
τ₀ := (1 − a)²g₀² (the computation above is a population identity for any U).

**(I)(c) S5.** Σ = 0.3·11ᵀ + 0.4H + 0.3I, groups of 5 (block CS, κ = 1). Assume p_n = 5G_n with G_n ≥ 5 (so B ≥ 5
once n ≥ 25; in general Lemma P5 needs B ≥ g, i.e. p ≥ g² and n ≥ g²; R08 suggestion 5).
*Lemma P5 (blocks are unions of whole groups).* Let R be any correlation matrix with |R_jk − Σ_jk| < 0.2 for all j ≠ k
(on the design event of L5.1 for n ≥ n₀; exactly for exact Gram). Then the method's partition (complete linkage on
1 − |R|, top-down cut at B ≥ 5, next-fit packing; FINAL s1) consists of unions of whole groups, at most ⌊16/5⌋ = 3
groups per block.
*Proof.* Within-group distances 1 − |R_jk| < 1 − 0.5 = 0.5 and cross-group distances > 1 − 0.5 = 0.5 (|R_jk| < 0.5).
Complete linkage merges the closest pair of clusters (complete-linkage distance = max pairwise distance). By induction,
while some group is not yet a single cluster, every cluster is contained in one group: if two clusters within one group
exist, their complete-linkage distance is < 0.5, whereas any two clusters from different groups are at distance > 0.5;
hence the next merge is within a group. So each group is a subtree of the dendrogram. In the top-down cut at B, a node
is split only if it has more than B ≥ 5 leaves; a group's subtree (5 leaves) is never split, and every cut cluster is a
subtree, hence either inside a group's subtree — impossible unless it is the whole group, since that subtree is not
split — or a union of whole group subtrees. Next-fit packing concatenates cut clusters into blocks of size ≤ B ≤ 16,
so blocks are unions of whole groups, ≤ 3 groups. (Tie rules are irrelevant: all comparisons used are strict.) ∎
So 𝔅_n := {unions of ≤ 3 whole groups} and 𝓔'_n := the design event of L5.1 (δ'_n < 0.2) cover the realised blocks.
*Certificate.* For the diagnostic layout (s₀ = 4, step 5) and the study's high-p layouts (s₀ = 14, step 7 and 13;
positions and coefficients of GEN STATEMENT (C5)(d) / W1-GEN numerics/study_common.py), numerics/tv_cert.py computes
τ(U, j) = (Σ_{jμ|U})²/Σ_{jj|U} at unit scale for every truth j, every block C = g(j) ∪ (≤ 2 other groups: null groups or
other truth groups) and every U ⊆ C ∖ {j}, using the exact symmetry reduction (within a null group only |U ∩ g|
matters; within truth group i only whether i ∈ U and the number of its nulls; within g(j) the number of nulls). Null
groups are exchangeable and their number does not enter τ. The minimum is reported in numerics/TV_cert_out.txt;
if positive, (TV-pop) holds with τ₀ = c²·min for the fixed scale c. Exact Gram: (TV) as in (I)(a) with this τ₀ and
Lemma P5 with R = Σ.

**(I)(d) General block CS** (fixed 0 < ρ_b < ρ_w < 1, fixed group size g ≤ 16): κ = 1 (Lemma κ), α₀ = 1/6.
Lemma P5 holds with the same proof once B ≥ g, with 0.2 replaced by (ρ_w − ρ_b)/2 and the threshold 0.5 by
(ρ_w + ρ_b)/2 (within-group |R_jk| > (ρ_w + ρ_b)/2 > cross-group |R_jk|); blocks are unions of ≤ ⌊16/g⌋ whole groups.
(TV-pop) is then a finite population condition of the same type as for S5, to be certified per layout (or use
𝔅_n = all sets of size ≤ 16).

## L5.3 Exact certificates (R05 item 1)

**Lemma TVF (closed form of the population partial signal, one factor + block-diagonal Ψ).** Let Σ = λλᵀ + Ψ (Ψ ≻ 0
block-diagonal over groups), θ supported on S₀, μ-covariances Σθ, L := λᵀθ. For j ∉ U put U₀ := U ∩ g(j),
λ̃ := λ_j − Ψ_{jU₀}Ψ_{U₀U₀}⁻¹λ_{U₀}, ψ := Ψ_jj − Ψ_{jU₀}Ψ_{U₀U₀}⁻¹Ψ_{U₀j}, η := (Ψθ)_j − Ψ_{jU₀}Ψ_{U₀U₀}⁻¹(Ψθ)_{U₀},
s := λ_UᵀΨ_UU⁻¹λ_U, t := λ_UᵀΨ_UU⁻¹(Ψθ)_U. Then
  Σ_{jμ|U} = λ̃(L − t)/(1 + s) + η,   Σ_{jj|U} = ψ + λ̃²/(1 + s).
*Proof.* Woodbury: Σ_UU⁻¹ = Ψ_UU⁻¹ − Ψ_UU⁻¹λ_Uλ_UᵀΨ_UU⁻¹/(1 + s). With Σ_{jU} = λ_jλ_Uᵀ + Ψ_{jU}, Σ_{Uμ} = λ_UL + (Ψθ)_U,
e := Ψ_{jU}Ψ_UU⁻¹λ_U, f := Ψ_{jU}Ψ_UU⁻¹(Ψθ)_U (only U₀ contributes, Ψ block-diagonal; so λ_j − e = λ̃, (Ψθ)_j − f = η):
Σ_{jU}Σ_UU⁻¹Σ_{Uμ} = λ_j(sL + t) + eL + f − (λ_js + e)(sL + t)/(1 + s) = (λ_j − e)(sL + t)/(1 + s) + eL + f, and
Σ_{jμ} = λ_jL + (Ψθ)_j; subtracting gives (λ_j − e)[L − (sL + t)/(1 + s)] + η = λ̃(L − t)/(1 + s) + η. The variance
formula is L1 (1.1) (innovation variance of x_j given x_U). ∎
*S5 specialisation* (λ_i ≡ λ, λ² = 3/10, Ψ = (2/5)H + (3/10)I, one truth per truth group): for a group g with
u_g := |U ∩ g|, s_g = λ²u_g/(d + u_gb), t_g = λ(dΘ_{U∩g} + u_gbΘ_g)/(d + u_gb) (Θ_g := coefficient of g's truth or 0,
Θ_{U∩g} := that coefficient if the truth is in U, else 0; d = 3/10, b = 2/5), s = Σ_g s_g, t = Σ_g t_g, and with
u₀ := |U₀|: λ̃ = λd/(d + u₀b), ψ = d(d + (u₀ + 1)b)/(d + u₀b), η = θ_jψ. Hence τ(U, j) = Σ_{jμ|U}²/Σ_{jj|U} is a rational
function of the group counts and of the rational coefficients; λ enters only through λ² (λ̃(L − t) = λ²·rational).
*Exhaustiveness.* By Lemma P5 every realised block is g(j) ∪ (≤ 2 other whole groups). τ depends on U only through:
u₀ (j's group contains only nulls besides j); for each other truth group, whether its truth is in U and how many of its
nulls; for each null group, the count. Null groups enter only through their counts (they are exchangeable and groups
not meeting U contribute nothing), so adding null groups to the design does not change the set of values; the
enumeration in numerics/tv_cert_exact.py covers all choices of ≤ 2 other groups (two truth groups, truth + null, null
+ null, one, none), all counts, |U| ≤ 15.
*Results* (numerics/tv_cert_exact.py → TV_cert_exact_out.txt; exact `fractions.Fraction` arithmetic; the closed form
was cross-checked against direct linear algebra on 3000 random configurations, max difference 3.8e-15):
diagnostic layout (s₀ = 4): min τ = 2023/32500 ≈ 0.06225 over 11,060 configurations; study layouts (s₀ = 14, step 7 and
step 13): min τ = 7/2080 ≈ 0.003365 over 612,710 configurations each. Hence (TV-pop) holds with τ₀ = c²·2023/32500,
resp. c²·7/2080, for the fixed scale c > 0. (GC-CS) exact minima for the study patterns: a = 1/10: 39/50, 7/25;
a = 3/10: 17/50, 1/125; a = 1/2: **0** (both); a = 7/10: 8/85, 1/295; a = 9/10: 4/95, 1/95 (s₀ = 4, 14).

## L5.4 Earlier floating-point certificate (superseded by L5.3; numerics/TV_cert_out.txt)

* S5, unit scale c = 1 (τ scales with c²): diagnostic layout (s₀ = 4, step 5): 11,060 configurations, min τ = 0.062246;
  study layouts (s₀ = 14, step 7 and step 13): 612,710 configurations each, min τ = 0.003365. Hence (TV-pop) holds for
  every fixed c > 0 with τ₀ = c²·min (𝔅_n = unions of ≤ 3 whole groups; Lemma P5). (Floating-point computation of
  small linear solves; the minima are far from rounding level.)
* CS (GC-CS) minimum of |θ_j + a(Θ − Θ_V)/(1 − a + au)| for the study patterns: a = 0.1: 0.78 (s₀ = 4), 0.28 (s₀ = 14);
  a = 0.3: 0.34, 0.008; a = 0.7: 0.094, 0.0034; a = 0.9: 0.042, 0.0105; **a = 0.5: exactly 0 for both patterns** —
  e.g. s₀ = 4, θ_j = −1.0, Θ = 1.0, U = ∅: (1 − a)θ_j + aΘ = 0, a truth with zero marginal factor-plus-own signal. So
  (GC-CS) is a genuine restriction (masked truths are excluded, as in GROW's TV); instance (I)(a)/(b) does not cover
  a = 0.5 with these patterns.
