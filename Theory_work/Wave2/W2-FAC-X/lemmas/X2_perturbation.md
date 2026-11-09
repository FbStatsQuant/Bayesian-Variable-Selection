# X2 — The perturbation δ_j(T) on band-structured sets, and the design/noise event 𝔈_n

Status: **PROVED (by this seat, unchecked)**; lemma check R03 (Codex Sol high, reviews/R03_X1X2X3_check_sol.md):
VERIFIED-WITH-AMENDMENTS (MINOR items 1–4, applied; reviews/R03_disposition.md). Falsification numerics:
numerics/N1X_summary.md — the fitted empirical proxy δ̂ (not the exact δ_j(T)) along the path vs √(k log p/n): tabulated
maxima of the ratio range from 1.48 to 3.10 (n ≤ 10⁶, p ≤ 1000); exact-δ runs at extreme ρ: reviews/R09_scratch/c3_out.txt.

Setting: X1 (Υ_n = I, the rotation representation, notation ξ, a, η, φ, W, ṽ1, ṽ2, κ, ϱ, x_T, τ̂, δ). Let A₁ ∈ (0, ½)
with p ≤ n^{A₁} for n ≥ n₀ ((P-½)). 𝒩_all := [p] ∖ S₀ (all nulls; deterministic). m_all := p − s₀,
H̄² := 2 log(2m_all + 2) + 2L_n (one definition throughout X2–X4 and STATEMENT §3; note H̄ ≥ √(2L_n) for every p,
R02 item 2). The constant C_X of Proposition X2 depends on ρ only (Proposition X2 involves only W, ξ, a, η, φ, D3/D4, κ and ℓ); other constants C depend on ρ only unless stated; only the onset n₀ depends on (σ, ϑ, s₀, A₁) as well (R14 item 5).

## X2.1 The event 𝔈_n

Convention (R07 item 2): maxima of nonnegative quantities over empty index sets are 0 (e.g. D4 when p = s₀, D2's
off-diagonal maximum when p = 1); eigenvalue statements concern nonempty principal submatrices.
* **D1** (Davidson–Szarek) ‖W/N − I‖_op ≤ r_n := 3√(p/N) + 3√(2 log n/N).
* **D2** max_j|W_jj/N − 1| ≤ 3√(log n/N), max_j‖u_j^⊥‖² ≤ 2N, max_{j≠l}|W_jl|/N ≤ 4√(log n/N).
* **D3** |φ²/N − 1| ≤ n^{−1/3}, |‖e‖²/(σ²(n − 1)) − 1| ≤ n^{−1/3}, |η| ≤ √(2L_n), max_j|a_j| ≤ 2√(log n).
* **D4** max_{j∈𝒩_all}|ξ_j| ≤ H̄ and max_{j∈S₀}|ξ_j| ≤ √(2L_n) (so |η| and every |ξ_j|, j ∈ [p], are ≤ H̄).
* **D5** (Gaussian sums, conditional on ξ) with t_n := √(10 log n): for every j ∈ [p] and every A in the family
  𝒜_j := {[p] ∖ {j}} ∪ {(𝒩_all ∩ (a, b)) ∖ {j} : a < b, a, b ∈ {ξ_l : l ∈ 𝒩_all} ∪ {±∞}}:
  |Σ_{l∈A}W_jlξ_l| ≤ t_n‖u_j^⊥‖(Σ_{l∈A}ξ_l²)^{1/2} and |Σ_{l∈A}W_jl| ≤ t_n‖u_j^⊥‖|A|^{1/2}.
* **D6** (window counts) for each of the finitely many deterministic widths w ∈ 𝒲_n := {4.3ϖ_n, 9ϖ_n} (all in
  [n^{−1}, 1] for n ≥ n₀) and every closed interval J of length w: #{l ∈ 𝒩_all : ξ_l ∈ J} ≤ 2e²pw + 3 log n + 1
  (R03 item 2: the event is the intersection over these widths, not simultaneous in w).

**Lemma X2.1.** P(𝔈_n) → 1 (for each fixed choice of the deterministic window width in D6).

*Proof.* D1: W = GᵀG with G an N × p standard Gaussian matrix (X1.1); Davidson–Szarek: P(s_max(G) > √N + √p + t or
s_min(G) < √N − √p − t) ≤ 2e^{−t²/2}; with t = √(2 log n) and p/N → 0, (1 ± (√p + t)/√N)² − 1 ≤ 3(√p + t)/√N.
D2: W_jj ~ χ²_N (Laurent–Massart, union over p ≤ n); given u_j^⊥, (W_jl)_{l≠j} are iid N(0, ‖u_j^⊥‖²) (the u_l^⊥ are iid
standard Gaussian in V₃, independent of u_j^⊥), so
P(|W_jl| > ‖u_j^⊥‖√(6 log n) | u_j^⊥) ≤ 2n^{−3}, union over p² ≤ n pairs, and on ‖u_j^⊥‖² ≤ 2N this gives
|W_jl|/N ≤ √(12 log n/N) ≤ 4√(log n/N). D3: χ² concentration (Laurent–Massart) for φ² ~ χ²_{n−2} and ‖e‖²/σ² ~ χ²_{n−1};
Gaussian tails for η (P(|η| > √(2L_n)) ≤ e^{−L_n} = 1/log n) and the p ≤ n coordinates a_j. D4: union bound,
2m_all·Φ̄(H̄) ≤ e^{−L_n} and s₀·2Φ̄(√(2L_n)) ≤ s₀e^{−L_n} → 0 (s₀ fixed).
D5: by X1.1, (W_jl)_{l≠j} given (u_j^⊥, ξ) are iid N(0, ‖u_j^⊥‖²) — W is independent of ξ, and the conditional law of
(u_l^⊥)_{l≠j} given u_j^⊥ does not involve ξ. The family 𝒜_j is a function of ξ only: an open interval (a, b) with
endpoints in the finite set {ξ_l} ∪ {±∞} selects a run of consecutive order statistics, so |𝒜_j| ≤ (p + 1)² + 1. For
fixed A, Σ_AW_jlξ_l and Σ_AW_jl are conditionally centred Gaussian with variances ‖u_j^⊥‖²Σ_Aξ_l² and ‖u_j^⊥‖²|A|;
P(|Z| > t_n sd) ≤ 2e^{−5 log n} = 2n^{−5}; the union over j ≤ p, A ∈ 𝒜_j and the two sums has ≤ 2p((p + 1)² + 1) ≤ 16n²
terms, total ≤ 32n^{−3} → 0. D6 (for one w ∈ 𝒲_n): the grid intervals [rw, (r + 2)w], r ∈ ℤ, meeting [−H̄, H̄]
number ≤ 2H̄/w + 4 ≤ 3n(H̄ + 1) (R03 item 1); every interval J of length w inside [−H̄ − w, H̄ + w] lies in one of them,
and outside [−H̄, H̄] there are no nulls on D4 (handled by adding P(D4ᶜ), not by conditioning). For a fixed grid
interval the count is Bin(m_all, q), stochastically dominated by Bin(p, q), q ≤ 2w/√(2π) ≤ w; P(Bin(p, q) ≥ t) ≤
(epq/t)^t; with t := max(e²pq, 3 log n) + 1 the bound is ≤ e^{−t} ≤ n^{−3}; union ≤ 3(H̄ + 1)n^{−2} = O(√(log n)/n²),
and the intersection over the two widths costs a factor 2. ∎

On 𝔈_n (n ≥ n₀) one also has (R03 item 4): sd_j² = ‖g_j‖²/(n − 1) ∈ [½, 2] (g_j's coordinates, D1–D4: the e₁
coordinate contains ξ_j); λ_min of every principal
submatrix of the sample correlation R̂ ≥ c₀ := (1 − ρ)/5 (G^r ⪰ (1 − ρ)W ⪰ (1 − ρ)N(1 − r_n) I and sd² ≤ 2), hence
λ_min(G_T) ≥ c₀(n − 1); q_T ≤ 2‖ṽ1_T‖²/N ≤ 2p(1 + ℓ)²H̄²/N ≤ 1/10 (A = ṽ2ṽ2ᵀ + W ⪰ N(1 − r_n)I);
|x_T| ≤ (|Σ_Tξ| + |ϱ|)/(k + κ) ≤ H̄ + ℓ|η| ≤ H̄ + ℓ√(2L_n) ≤ C_ρH̄, C_ρ := 1 + ℓ, for every T ⊇ S₀ (|ϱ| = κℓ|η| ≤ (k + κ)ℓ|η|); κ ∈ [κ_∞/2, 2κ_∞]; s² bounds:
G^r_{S₀S₀}/(n − 1) = Σ_{S₀S₀} + o(1) (fixed-size support, D1–D4) and eᵀμ/(n − 1) = O(H̄/√n), so
s² = σ² + ϑᵀΣ_{S₀S₀}ϑ + o(1) ∈ [s_min², s_max²] for fixed positive bounds; and ω_j(T)² ≤ q_T (Schur). These are the
standing assumptions of X1.4.

## X2.2 Band-structured sets

For a < b in ℝ ∪ {±∞} and w ≥ 0 put I(a, b) := 𝒩_all ∩ (a, b) (the interval part),
Band(a, b; w) := 𝒩_all ∩ ((a − w, a] ∪ [b, b + w)), and T⁰(a, b) := [p] ∖ I(a, b).
A set T with S₀ ⊆ T ⊆ [p] is **(a, b; w)-structured with exceptional set E** if T Δ T⁰(a, b) ⊆ Band(a, b; w) ∪ E,
E ⊆ 𝒩_all, |E| ≤ 17. (The path sets of X4 are of this form with E = N₀; one extra deletion or addition adds one point
to E.)

## X2.3 Proposition (perturbation bound)

**Proposition X2.** On 𝔈_n, n ≥ n₀(ρ, σ, ϑ, s₀, A₁) (note H̄ + |x_T| ≤ (2 + ℓ)H̄ by X2.1): for every (a, b; w)-structured T with exceptional set E and
k = |T| ≥ s₀ + 1, and every null j ∈ T,
  |δ_j(T)| ≤ C_X(H̄ + |x_T|)·[√(p log n/n) + (#Band(a, b; w) + 17)·√(log n/n)].

*Proof.* Write B := A_T/N = I + R + bbᵀ with R := W_T/N − I_T (a principal submatrix of W/N − I, so ‖R‖ ≤ r_n by D1)
and b := ṽ2_T/√N; B₀ := I + bbᵀ ⪰ I, c := B₀⁻¹ṽ1_T; b⁰ := ℓφ1/√N and c⁰ := (I + b⁰b⁰ᵀ)⁻¹ṽ1_T, so that
c⁰_l = ξ_l − x_T (X1.3). Then √N ω_j(T) = (B⁻¹ṽ1)_j/√((B⁻¹)_jj), and the resolvent identity
B⁻¹ = B₀⁻¹ − B₀⁻¹RB₀⁻¹ + B₀⁻¹RB₀⁻¹RB⁻¹ gives
  (B⁻¹ṽ1)_j = c_j − (B₀⁻¹Rc)_j + ((B₀⁻¹R)²B⁻¹ṽ1)_j.                                                  (2.1)
Preliminaries (on 𝔈_n, n ≥ n₀): ‖B⁻¹‖ ≤ 1/(1 − r_n) ≤ 2 (B ⪰ (1 − r_n)I); |b_j| ≤ 2ℓ; ‖b‖ ≥ ℓ√k/2 (‖b⁰‖ =
ℓφ√k/√N ≥ 0.9ℓ√k, ‖b − b⁰‖ = ‖(a_j)_{j∈T}‖/√N ≤ 2√(k log n/N)); ‖c⁰‖² = Σ_{l∈T}(ξ_l − x_T)² ≤ k(H̄ + |x_T|)² (D4).

(i) **a-terms.** Let S(b) := bᵀṽ1/(1 + ‖b‖²), so c = ṽ1 − bS(b), c⁰ = ṽ1 − b⁰S(b⁰), and b⁰_jS(b⁰) = ℓη + x_T (X1.3)
gives |S(b⁰)| ≤ 2(ℓ|η| + |x_T|)/ℓ. With α := b − b⁰ (‖α‖_∞ ≤ 2√(log n/N)):
|αᵀṽ1| ≤ ‖α‖_∞ k(1 + ℓ)H̄, |‖b‖² − ‖b⁰‖²| ≤ 2‖b⁰‖_∞k‖α‖_∞ + k‖α‖²_∞, and 1 + ‖b‖² ≥ ℓ²k/4, so
|S(b) − S(b⁰)| ≤ C√(log n/n)(H̄ + |η| + |x_T|) and
  |c_j − c⁰_j| ≤ |α_j||S(b)| + |b⁰_j||S(b) − S(b⁰)| ≤ C√(log n/n)(H̄ + |x_T|),  ‖c − c⁰‖ ≤ √k·C√(log n/n)(H̄ + |x_T|).

(ii) **Second order.** By ‖B₀⁻¹‖ ≤ 1 and B⁻¹ṽ1 = c − B₀⁻¹RB⁻¹ṽ1 (so ‖B⁻¹ṽ1‖ ≤ ‖c‖/(1 − r_n)):
|((B₀⁻¹R)²B⁻¹ṽ1)_j| ≤ r_n²‖c‖/(1 − r_n) ≤ 2r_n²√k(H̄ + |x_T|)(1 + o(1)) ≤ C(p^{3/2}/n + √p log n/n)(H̄ + |x_T|).
For p ≤ n^{A₁}, A₁ < ½: p^{3/2}/n ≤ √(p/n) once p ≤ √n, so this is ≤ C√(p log n/n)(H̄ + |x_T|).

(iii) **First order, common part.** (B₀⁻¹Rc)_j = (Rc)_j − b_j·bᵀRc/(1 + ‖b‖²) and
|b_j bᵀRc/(1 + ‖b‖²)| ≤ 2ℓ r_n‖c‖/‖b‖ ≤ 4.1 r_n(H̄ + |x_T|)(1 + o(1)).

(iv) **First order, individual part.** (Rc)_j = (R(c − c⁰))_j + (Rc⁰)_j with |(R(c − c⁰))_j| ≤ r_n‖c − c⁰‖ ≤
C r_n√(p log n/n)(H̄ + |x_T|), and
  (Rc⁰)_j = (W_jj/N − 1)(ξ_j − x_T) + N⁻¹Σ_{l∈T∖j}W_jl ξ_l − x_T N⁻¹Σ_{l∈T∖j}W_jl.
The diagonal term is ≤ 3√(log n/N)(H̄ + |x_T|) (D2). For the sums write T ∖ j = (T⁰ ∖ j) ∖ (T⁰ ∖ T) ∪ (T ∖ T⁰) with
T⁰ := T⁰(a, b), and T⁰ ∖ j = ([p] ∖ j) ∖ (I(a, b) ∖ j). The sets [p] ∖ j and I(a, b) ∖ j belong to 𝒜_j, so by D5, D2
(‖u_j^⊥‖ ≤ √(2N)) and D4 (Σ_Aξ_l² ≤ pH̄² — truths have |ξ| ≤ √(2L_n) ≤ H̄):
  N⁻¹|Σ_{T⁰∖j}W_jlξ_l| ≤ 2·t_n√(2N)·√p H̄/N ≤ 2H̄√(20 p log n/N),  N⁻¹|Σ_{T⁰∖j}W_jl| ≤ 2√(20 p log n/N).
The remaining indices T Δ T⁰ ⊆ Band(a, b; w) ∪ E contribute at most (#Band + 17)·4√(log n/N)·(H̄ + |x_T|) (D2, D4).

(v) **Normalisation.** (B⁻¹)_jj − (B₀⁻¹)_jj = −(B₀⁻¹RB⁻¹)_jj has modulus ≤ r_n/(1 − r_n); (B₀⁻¹)_jj = 1 − b_j²/(1 + ‖b‖²)
differs from 1 − γ_k = 1 − (b⁰_j)²/(1 + ‖b⁰‖²) by ≤ C√(log n/n)/k (as in (i)); and 1 − γ_k ≥ κ/(1 + κ) ≥ c(ρ) > 0. Hence
|√(1 − γ_k)/√((B⁻¹)_jj) − 1| ≤ C r_n. By (2.1) and (i)–(iv), |(B⁻¹ṽ1)_j| ≤ |c⁰_j| + (the bounds above) ≤ 2(H̄ + |x_T|)
for n ≥ n₀ (each bound is o(1)·(H̄ + |x_T|) as p ≤ n^{A₁}, #Band ≤ p, A₁ < ½ — note (#Band + 17)√(log n/n) ≤
(p + 17)√(log n/n) ≤ 18p√(log n/n) → 0 for p ≥ 1, R03 item 3).

Collect: τ̂_j(T) = √(1 − γ_k)(B⁻¹ṽ1)_j/√((B⁻¹)_jj) and ξ_j − x_T = c⁰_j, so
|δ_j(T)| ≤ |c_j − c⁰_j| + |(B₀⁻¹Rc)_j| + |second order| + C r_n·2(H̄ + |x_T|), and every term is bounded by
C(H̄ + |x_T|)[√(p log n/n) + (#Band + 17)√(log n/n)] (r_n ≤ 4√(p/n) + 5√(log n/n)). ∎

**Corollary X2 (closed under one move).** If T is (a, b; w)-structured with exceptional set E, |E| ≤ 15, then T ∖ j
and T ∪ l (S₀ ⊆ T ∖ j) are (a, b; w)-structured with exceptional set E ∪ {j}, resp. E ∪ {l}; and T ∖ j ∪ l with
E ∪ {j, l}. So Proposition X2 applies to all deletion, addition and swap statistics used in X1.4 (g3)–(g5) at a path
set T whose exceptional set is N₀.

**Remark (where A < ½ enters).** In X4 the band count is fed back: #Band ≤ 2(2e²p w + 3 log n + 1) with w ≍ ϖ_n, and
the band term C_X(2 + ℓ)H̄·#Band·√(log n/n) is ≤ ϖ_n/4 for n ≥ n₀ provided C·pH̄√(log n/n) → 0 and
H̄(log n)^{3/2}/(√n ϖ_n) → 0 (the latter holds by the n^{−1/3} floor). Under (P-½) the first holds; it is a **sufficient**
absorption criterion, not equivalent to limsup log p/log n < ½ (e.g. p = ⌊√n/log²n⌋ also satisfies it — R02 item 5).
The second-order term was bounded here only under p ≤ √n; no claim is made about the other terms for larger p.
