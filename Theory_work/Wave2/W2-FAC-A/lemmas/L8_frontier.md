# L8 — Part III frontier: the path route for exact-Gram compound symmetry (tools proved; target open)

Status: Lemma CS-1D and Lemma GAP: **PROVED (by this seat, unchecked)** (tools; not used by Parts I–II). Conjecture
PATH-CS: **OPEN** (evidence only). Numerics: numerics/cs1d.py (selftest), D2_summary.md, D3_summary.md.

## Lemma CS-1D (exact one-dimensional reduction)

Exact Gram XᵀX = (n − 1)[(1 − a)I + a11ᵀ], a ∈ (0, 1), response scaled to yᵀy = n − 1, z := Xᵀy. Put
A := (n + 1)(n − 1)(1 − a) + 1, B := (n + 1)(n − 1)a, A′ := (n − 1)(1 − a) + 1, B′ := (n − 1)a, N_k := k + A/B,
P_T := Σ_{j∈T}z_j², L_T := Σ_{j∈T}z_j. For every T with |T| = k ≤ K,

  F(T) = log w(k) + D_k − ν log(0.02 + (n − 1) − (n/A)Φ(T)),   Φ(T) := P_T − L_T²/N_k,
  D_k := −½[(k − 1) log A + log(A + kB) − (k − 1) log A′ − log(A′ + kB′)]  (D_0 := 0), up to the constant log c_n.

*Proof.* For |T| = k, G_T = (n − 1)[(1 − a)I_k + a11ᵀ] does not depend on which T; H_T = AI + B11ᵀ,
G_T + I = A′I + B′11ᵀ; det(αI + β11ᵀ) = α^{k−1}(α + kβ) and (αI + β11ᵀ)⁻¹ = α⁻¹(I − β(α + kβ)⁻¹11ᵀ); hence
z_TᵀH_T⁻¹z_T = A⁻¹(P_T − B(A + kB)⁻¹L_T²) = A⁻¹Φ(T) since B/(A + kB) = 1/N_k. Insert into the score of FINAL s1. ∎
(numerics/cs1d.py selftest: agreement with the exact scorer to 5.6e-9 at n = 10⁶; identical LS0 endpoints and move
counts in the selftest — paths themselves were not compared; R06 item 12.)

**Move identities (exact).** With c_T := L_T/N_k and N := N_k:
  deletion of e ∈ T:  Φ(T) − Φ(T ∖ e) = (N/(N − 1))(z_e − c_T)²;
  addition of l ∉ T:  Φ(T ∪ l) − Φ(T) = (N/(N + 1))(z_l − c_T)²;
  swap e → l:         Φ(T ∖ e ∪ l) − Φ(T) = u² − v² − (u − v)²/N,  u := z_l − c_T, v := z_e − c_T.
(Elementary algebra from Φ = P − L²/N.) Since F is increasing in Φ at fixed size, the best deletion from T removes the
element of T closest to c_T, the best addition adds the outside element farthest from c_T, and every comparison between
moves reduces to these one-dimensional quantities. For T ⊇ S₀ the signal parts cancel: the null z-values are
z_j = ẑ + τh_j (common ẑ, τ = σ√((n−1)(1−a))/s_Y, h_j iid N(0,1) up to a common shift), truths are displaced by
(n − 1)(1 − a)θ*_j/s_Y, i.e. by order n (order √n in units of τ), and c_T − ẑ is
τ times (Σ_{j∈T}h_j − γ_n)/N with a common γ_n = O_P(1) (L1 U(a) with singleton groups).

## Lemma GAP (deterministic invariant of a deletion path)

Suppose LS0 starts at [p] and its first t moves are deletions of nulls, each the element of the current set closest to
its centre c_T. Let D_t be the deleted set. Then (i) D_t is a contiguous run in the order of the null z-values, and
(ii) c_{T_t} lies in the closed interval between the largest kept null below D_t and the smallest kept null above D_t
(with ±∞ if none).
*Proof.* Induction. t = 1: e₁ is the null closest to c_{[p]}; the nearest kept nulls on either side of z_{e₁} are at
least as far from c as z_{e₁}. Step: let e be the kept element closest to c := c_T, say z_e ≥ c (the other case is
symmetric). Then c_{T∖e} = c + (c − z_e)/(N − 1) moves away from z_e by (z_e − c)/(N − 1) < z_e − c ≤ c − ℓ′ (ℓ′ the
nearest kept below; by minimality of e), because N − 1 > 1 (N ≥ s₀ + 1 + A/B > 2 while a null is kept). So the new centre
stays strictly between ℓ′ and the next kept element above z_e; D ∪ {e} is still contiguous. ∎

## Conjecture PATH-CS and where a proof stops

**Conjecture PATH-CS.** Exact-Gram CS, fixed a, s₀, θ*, σ², (GC-CS), and the visibility condition making S̃₀ = [p]
(every null has a nonzero conditional factor signal in its block): for every sequence p_n ≤ K (any polynomial growth),
P(LS0 from S̃₀ is a pure deletion path ending at S₀) → 1; in particular D_n → 0.
**Evidence.** D2: exact-Gram simulator, p ∈ {100, 200, 400}, n ∈ {10⁵, 10⁶, 10⁷}: pure deletion paths in every
CS3/CS5/S5/F2 run; F2r p = 200, n = 10⁷: 4/5 pure (one swap); MR1 reached S₀ in every run (D2_summary.md); D3: exact 1-D LS0 from [p], a ∈ {0.3, 0.7, 0.9}, s₀ ∈ {1, 4}, p ∈ {200, 1000},
n ∈ {10⁴, 10⁶, 10⁹} (log p/log n up to 0.75), 720 runs: 720 pure deletion paths, 718 ending at S₀ (D3_summary.md).
**What a proof would need (HEURISTIC outline, not a proved reduction; R06 items 8–10).** With h_k := log w(k) + D_k,
V := 0.02 + n − 1 − (n/A)Φ(T), b := n/A, d := Nδ²/(N − 1) (δ the distance from c_T to the nearest kept null),
a₊ := N max_{l∉T}(z_l − c_T)²/(N + 1) and s₊ := max over swaps of Φ(T ∖ e ∪ l) − Φ(T), the exact gains are
Δ_d = h_{k−1} − h_k − ν log(1 + bd/V), Δ_a = h_{k+1} − h_k − ν log(1 − ba₊/V), Δ_s = −ν log(1 − bs₊/V); the best null
deletion is the chosen move precisely when Δ_d > 0 exceeds Δ_a, Δ_s and the truth-removing gains (tie rule aside). By
Lemma GAP the deleted values lie in the gap containing c_T, so bounding a₊ and s₊ reduces to the balance of the gap
around c_T. While kept nulls remain on both sides, an induction suggests |d₊ − d₋| ≤ (d₊ + d₋)/N + s* (s* a spacing of
consecutive null values), which would make s₊ ≤ (d₊ + d₋)s* — a sketch, not checked. The open case is a late stage in
which all remaining kept nulls lie on one side (m ≥ 2 of them): c_T is pulled towards them and the swap identity gives an
S-gain ≈ 4M²(m − 1)/N (M² ≈ 2 log p) against a deletion gain ≈ log n + M²(1 − r²N/(N − 1)), r := (s₀ + A/B)/N; for large
log p/log n and m ≥ m*(a, s₀) this bound does not exclude a swap. An independent-sign heuristic suggests a scale 2^{−m}
for such endings at fixed m; the probability of these adaptively selected endings is unproved. D3 recorded no swap at
all. Excluding such swaps would establish PATH-CS (pure deletion); controlling a bounded or cap-compatible number of
late swaps would establish only the weaker LS0-discovery conclusion (enough for D_n → 0 via [OP]).

## p > K and k ≥ 2 (not claimed)
* **p > K.** If every variable is visible, S̃₀ has size exactly K; the outside set is then not a gap around the centre,
  and the swap identity predicts improving swaps that bring in outside elements far from c_T, with gain of order
  ρ·2 log p (ρ = n/(n − K) ≈ 2) against a deletion gain ≈ log n. A heuristic count of such swaps is (p − K)·n^{−1/4+o(1)},
  which would exceed the MR1 slack ℓ_n + s₀. Not tested (exact Gram needs p ≤ n − 1 and the regime requires the
  asymptotic start mode); heuristic only.
* **k ≥ 2 global factors.** L1 does not prove a multiple-global-factor theorem. One possible sufficient condition for a
  direct matrix extension of the Cauchy–Schwarz step is a lower bound on λ_min of the T-restricted loading Gram
  proportional to the number of groups hit (with a representation-dependent scale and a treatment of effective rank;
  rank-deficient aligned loadings may reduce to the scalar case). Any obstruction for k ≥ 2 is conjectural.
