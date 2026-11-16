# W3-DIST — Lemma T (distribution-free sample-to-population transfer on sparse directions) — stream B

**Status: DRAFT (by this seat, unchecked).** Author: stream B (Claude Opus 5.5, Claude Third). Target: STATEMENT.md
v1.3.1 §3 "Lemma T" (lines 297–308) = API_CARDS card T. Notation binding; here P := p_raw.

**No STATEMENT-CHANGE REQUEST for Lemma T.** The display, the range 1 ≤ d ≤ min(p_raw, n − 1) and the remainder
η²_n(d, δ) are proved exactly as stated (in fact with failure probability δ/2).
**EDITORIAL NOTE on the route text of STATEMENT §3 (not a statement change).** The route quotes the ratio inequality
"P(sup_A (P(A) − P_n(A))/√P(A) > η) ≤ 4S(2n)e^{−nη²/4}" with "attribution and constant to be verified". This file does
**not** use that inequality or any external one. It proves (Proposition R, §T.3) the one-sided *multiplicative*
inequality P(∃A: P(A) > 2P_n(A) + η²) ≤ 2S(2n)e^{−nη²/4} for nη² ≥ 25, by a ghost sample (Cantelli) and random swaps
(Hoeffding), and then uses the layer-cake formula, which is linear, so no Cauchy–Schwarz step is needed. For the record,
Appendix T.A proves the ratio form with the constants this seat can prove, 2S(2n)e^{−(1−θ)²nη²/4} for nθ²η² ≥ 1, and
carries out the layer-cake + Cauchy–Schwarz route: it gives Lemma T with the prefactor 4 of η² replaced by 6. Suggested
replacement of the route sentence: "multiplicative VC inequality, proved in `work/B_transfer/T.md` Prop. R".

Numerical sanity checks: `check_T.py` → `check_T_out.txt` (constants; Sauer bound; Monte Carlo of Prop. R on ℝ for a
Cauchy law and an atomic law).

---

## T.0 Statement

Let ν be any Borel probability measure on ℝ^P, x₁, …, x_n i.i.d. ~ ν, n ≥ 2, and let x denote a further independent draw
(E_x h = νh := ∫h dν, P_n h := n⁻¹Σ_i h(x_i)). For a ∈ ℝ, u ∈ ℝ^P, c > 0 put
  g_{a,u,c}(x) := min{1, (a + uᵀx)²/c} ∈ [0, 1].
**Lemma T.** Let 1 ≤ d ≤ min(P, n − 1) and δ ∈ (0, 1). Put
  L := d log(eP/d) + 2(d + 1) log(2en/(d + 1)),   η² = η²_n(d, δ) := (4/n)[L + log(4/δ)].
Then the event
  Ω_T := { νg_{a,u,c} ≤ 2P_ng_{a,u,c} + η²  for all a ∈ ℝ, c > 0, u ∈ ℝ^P with |supp u| ≤ d }
is measurable and P(Ω_T) ≥ 1 − δ/2 ≥ 1 − δ. All three terms of the bracket are ≥ 0 on this range (d ≤ P gives
eP/d ≥ e; d + 1 ≤ n gives 2en/(d + 1) ≥ 2e; δ < 1 gives 4/δ > 4). No moment, tail, small-ball, continuity or
eigenvalue condition is imposed on ν (atoms allowed).

## T.1 Elementary tools (each with proof)

**(T1) Cantelli.** If Y has finite variance V and t > 0, then P(Y − EY ≤ −t) ≤ V/(V + t²).
*Proof.* For λ ≥ 0, {Y − EY ≤ −t} ⊆ {(EY − Y + λ)² ≥ (t + λ)²}, so by Markov P(Y − EY ≤ −t) ≤ E(EY − Y + λ)²/(t + λ)²
= (V + λ²)/(t + λ)². With λ := V/t: (V + V²/t²)/(t + V/t)² = (V(t² + V)/t²)/((t² + V)²/t²) = V/(V + t²). ∎

**(T2) Hoeffding for Rademacher sums.** σ₁, …, σ_n i.i.d. uniform on {−1, 1}, a ∈ ℝⁿ with ‖a‖² > 0, w > 0:
P(Σ_iσ_ia_i ≥ w) ≤ exp(−w²/(2‖a‖²)).
*Proof.* E e^{λσ_ia_i} = cosh(λa_i) = Σ_{j≥0}(λa_i)^{2j}/(2j)! ≤ Σ_{j≥0}(λ²a_i²/2)^j/j! = e^{λ²a_i²/2}, since
(2j)! ≥ 2^j j!. By independence and Markov, for λ > 0, P(Σσ_ia_i ≥ w) ≤ e^{−λw + λ²‖a‖²/2}; take λ := w/‖a‖². ∎

**(T3) Binomial sums.** For integers 1 ≤ k ≤ m, Φ_k(m) := Σ_{i=0}^k C(m, i) ≤ (em/k)^k. Also Φ_k(m) := 0 for k = −1.
*Proof.* Since 0 < k/m ≤ 1 and i ≤ k: (k/m)^kΦ_k(m) ≤ Σ_{i=0}^k C(m, i)(k/m)^i ≤ Σ_{i=0}^m C(m, i)(k/m)^i = (1 + k/m)^m
≤ e^k. ∎ In particular C(P, d) ≤ Φ_d(P) ≤ (eP/d)^d for 1 ≤ d ≤ P.

**Traces, shattering, growth function.** For a family 𝒜 of subsets of ℝ^P and a finite sequence z = (z₁, …, z_m), the
*trace* of A on z is the index set {i ≤ m : z_i ∈ A}; tr_z(𝒜) is the set of traces. 𝒜 *shatters* an index set
T ⊆ {1, …, m} if every subset of T is of the form T ∩ τ, τ ∈ tr_z(𝒜). The growth function is
S_𝒜(m) := sup_{z ∈ (ℝ^P)^m} |tr_z(𝒜)| (repetitions in z allowed). VC(𝒜) is the largest k such that some set of k
distinct points is shattered. If z_i = z_j with i ≠ j, no index set containing both i and j is shattered (the pattern
{i} is not realised), so an index set shattered on z corresponds to a set of distinct points shattered by 𝒜; hence
tr_z(𝒜), as a family of subsets of {1, …, m}, shatters no index set of size > VC(𝒜).

**(T4) Sauer–Shelah.** If a family 𝒞 of subsets of {1, …, m} (m ≥ 0) shatters no set of size k + 1 (k ≥ −1), then
|𝒞| ≤ Φ_k(m). Consequently |tr_z(𝒜)| ≤ Φ_{VC(𝒜)}(m) for every z ∈ (ℝ^P)^m.
*Proof.* Induction on m, for all k ≥ −1 simultaneously. "Shatters no set of size k + 1" implies "shatters no larger
set" (a subset of a shattered set is shattered). k = −1: every non-empty family shatters ∅, so 𝒞 = ∅ and |𝒞| = 0 = Φ_{−1}.
m = 0: |𝒞| ≤ 1 = Φ_k(0) for k ≥ 0. Step m − 1 → m (m ≥ 1, k ≥ 0): put 𝒞₁ := {C ∖ {m} : C ∈ 𝒞} and
𝒞₂ := {C ⊆ {1, …, m − 1} : C ∈ 𝒞 and C ∪ {m} ∈ 𝒞}. The map C ↦ C ∖ {m} from 𝒞 onto 𝒞₁ has fibres of size 1 or 2,
and of size 2 exactly over 𝒞₂; hence |𝒞| = |𝒞₁| + |𝒞₂|. If 𝒞₁ shatters T ⊆ {1, …, m − 1}, so does 𝒞; hence 𝒞₁ shatters
no set of size k + 1 and |𝒞₁| ≤ Φ_k(m − 1). If 𝒞₂ shatters T, then 𝒞 shatters T ∪ {m} (for R ⊆ T take C ∈ 𝒞₂ with
C ∩ T = R: both C and C ∪ {m} are in 𝒞); hence 𝒞₂ shatters no set of size k, and |𝒞₂| ≤ Φ_{k−1}(m − 1). Pascal's rule
C(m, i) = C(m − 1, i) + C(m − 1, i − 1) gives Φ_k(m − 1) + Φ_{k−1}(m − 1) = Φ_k(m). ∎

**(T5) Open half-spaces (Dudley's argument).** Let 𝒱 be the (d + 1)-dimensional vector space of functions
h(y) = wᵀy + β on ℝ^d (w ∈ ℝ^d, β ∈ ℝ) and ℋ := {{y : h(y) > 0} : h ∈ 𝒱}. Then VC(ℋ) ≤ d + 1.
*Proof.* Let k := d + 1 and suppose distinct z₁, …, z_{k+1} are shattered. The linear map h ↦ (h(z₁), …, h(z_{k+1}))
has image of dimension ≤ k in ℝ^{k+1}, so some γ ≠ 0 satisfies Σ_iγ_ih(z_i) = 0 for all h ∈ 𝒱; replacing γ by −γ if
necessary, I := {i : γ_i > 0} ≠ ∅. By shattering, some h ∈ 𝒱 has h(z_i) > 0 for i ∈ I and h(z_i) ≤ 0 for i ∉ I. Then
Σ_{i∈I}γ_ih(z_i) > 0 and γ_ih(z_i) ≥ 0 for i ∉ I (γ_i ≤ 0, h(z_i) ≤ 0), so Σ_iγ_ih(z_i) > 0, a contradiction. ∎

## T.2 The class of level sets and its growth function

For T ⊆ {1, …, P} with |T| = d, a ∈ ℝ, u ∈ ℝ^P with supp u ⊆ T, and r > 0, put
  A(a, u, r) := {x ∈ ℝ^P : |a + uᵀx| > r},
  𝒜_d := {A(a, u, r) : a ∈ ℝ, r > 0, u ∈ ℝ^P, |supp u| ≤ d},
  𝒜₀ := {A(a, u, r) : a ∈ ℚ, r ∈ ℚ ∩ (0, ∞), u ∈ ℚ^P, |supp u| ≤ d} ⊆ 𝒜_d (countable).
(Supports of size < d are allowed, i.e. "enlarged to size d" with zero coefficients; u = 0 gives ∅ or ℝ^P.)

**Lemma T-G.** For every m ≥ d + 1: S_{𝒜₀}(m) ≤ S_{𝒜_d}(m) ≤ C(P, d)·Φ_{d+1}(m)² ≤ (eP/d)^d (em/(d + 1))^{2(d+1)}.
In particular, as 2n ≥ d + 1: S_{𝒜₀}(2n) ≤ (eP/d)^d (2en/(d + 1))^{2(d+1)} = e^L.
*Proof.* The first inequality holds because 𝒜₀ ⊆ 𝒜_d. Fix z ∈ (ℝ^P)^m. Every u with |supp u| ≤ d has supp u ⊆ T for some
T with |T| = d (d ≤ P); fix such a T and write y_i := (z_i)_T ∈ ℝ^d, u_T := (u_j)_{j∈T}. Then
  {i : z_i ∈ A(a, u, r)} = {i : u_Tᵀy_i + (a − r) > 0} ∪ {i : (−u_T)ᵀy_i + (−a − r) > 0},
because |t| > r ⟺ (t − r > 0 or −t − r > 0). Each of the two index sets is a trace on (y₁, …, y_m) of a member of ℋ
(T5), so by T4 and T5 it takes at most Φ_{d+1}(m) values, and the pair at most Φ_{d+1}(m)² values; the union is a
function of the pair. Summing over the C(P, d) sets T: |tr_z(𝒜_d)| ≤ C(P, d)Φ_{d+1}(m)². Finally T3 with
(k, m) = (d + 1, m) (needs m ≥ d + 1) and with (k, m) = (d, P) (needs 1 ≤ d ≤ P). ∎

## T.3 Proposition R (multiplicative VC inequality; proved here)

**Proposition R.** Let ν be a Borel probability measure on ℝ^P, x₁, …, x_n i.i.d. ~ ν, and 𝒜' a countable family of
Borel sets with S_{𝒜'}(2n) ≤ S̄. For every η > 0 with nη² ≥ 25,
  P( ∃A ∈ 𝒜' : ν(A) > 2P_n(A) + η² ) ≤ 2S̄·exp(−48nη²/169) ≤ 2S̄·exp(−nη²/4).
(48/169 ≥ 1/4 because 192 ≥ 169.)

*Proof.* Enumerate 𝒜' = {A₁, A₂, …} (finite lists are padded by repetition). Let x'₁, …, x'_n be i.i.d. ~ ν,
independent of x₁, …, x_n (the ghost sample), and P'_n(A) := n⁻¹Σ_i1_A(x'_i). Put
  E₁ := ∪_k {ν(A_k) > 2P_n(A_k) + η²},   E₂ := ∪_k {P'_n(A_k) > (4/5)(2P_n(A_k) + η²)}.
Both are countable unions of measurable events (P_n(A_k), P'_n(A_k) are measurable functions of the samples).

*Step 1 (ghost sample): P(E₁) ≤ 2P(E₂).* On E₁ let τ := min{k : ν(A_k) > 2P_n(A_k) + η²}; {τ = k} is measurable in
(x₁, …, x_n). If P(τ = k) > 0 then p_k := ν(A_k) > η² (as P_n ≥ 0). Let Z_k := nP'_n(A_k) ~ Bin(n, p_k), with
EZ_k = np_k and Var Z_k = np_k(1 − p_k). By T1 with t = np_k/5 (if p_k = 1, Z_k = n and the bound below is trivial):
  P(Z_k < (4/5)np_k) ≤ P(Z_k − np_k ≤ −np_k/5) ≤ np_k(1 − p_k)/(np_k(1 − p_k) + n²p_k²/25)
    = (1 − p_k)/((1 − p_k) + np_k/25) ≤ 1/(1 + np_k/25) < 1/(1 + nη²/25) ≤ 1/2,
using that x ↦ x/(x + c) is non-decreasing on [0, ∞) for c > 0, 1 − p_k ≤ 1, p_k > η² and nη² ≥ 25. On
{τ = k} ∩ {Z_k ≥ (4/5)np_k}: P'_n(A_k) ≥ (4/5)ν(A_k) > (4/5)(2P_n(A_k) + η²), so this event is contained in E₂. Since
the ghost sample is independent of (x_i),
  P(E₂) ≥ Σ_k P(τ = k, Z_k ≥ (4/5)np_k) = Σ_k P(τ = k)·P(Z_k ≥ (4/5)np_k) ≥ ½Σ_kP(τ = k) = ½P(E₁).

*Step 2 (random swaps): P(E₂) ≤ S̄·exp(−48nη²/169).* Write Ξ := (z₁, …, z_{2n}) := (x₁, …, x_n, x'₁, …, x'_n); its law is
ν^{⊗2n}. For σ ∈ {−1, 1}ⁿ let Ψ_σ be the map exchanging z_i and z_{n+i} for every i with σ_i = −1. Ψ_σ is a measurable
bijection of (ℝ^P)^{2n} preserving ν^{⊗2n}, so P(Ξ ∈ E₂) = P(Ψ_σΞ ∈ E₂) for every σ, and averaging over the 2ⁿ values,
  P(E₂) = E[ 2^{−n}Σ_σ 1{Ψ_σΞ ∈ E₂} ] = E[ P_σ(Ψ_σΞ ∈ E₂) ],
where, for fixed Ξ, P_σ is the uniform law of σ (i.i.d. Rademacher signs). Fix Ξ. For A ∈ 𝒜' put k_i := 1_A(z_i),
k'_i := 1_A(z_{n+i}), N_A := Σ_i(k_i + k'_i), a_i := k'_i − k_i ∈ {−1, 0, 1}, W_A(σ) := Σ_iσ_ia_i. Under Ψ_σ the first half
contains Σ_i[k_i(1 + σ_i)/2 + k'_i(1 − σ_i)/2] = (N_A − W_A)/2 points of A and the second half (N_A + W_A)/2. Hence
Ψ_σΞ satisfies the condition of E₂ for A iff
  (N_A + W_A)/2 > (4/5)(N_A − W_A + nη²)  ⟺  13W_A > 3N_A + 8nη²  ⟺  W_A > w_A := (3N_A + 8nη²)/13 > 0
(multiply by 10 and rearrange). Here ‖a‖² = #{i : k_i ≠ k'_i} ≤ N_A. If ‖a‖² = 0 then W_A ≡ 0 < w_A. Otherwise, by T2,
  P_σ(W_A > w_A) ≤ exp(−w_A²/(2‖a‖²)) ≤ exp(−w_A²/(2N_A)) ≤ exp(−4·3N_A·8nη²/(169·2N_A)) = exp(−48nη²/169),
using (3N + 8nη²)² ≥ 4·3N·8nη² (AM–GM: (α + β)² ≥ 4αβ). The pair (N_A, (a_i)_i), hence the event {W_A > w_A}, depends on A
only through its trace on Ξ, and there are at most |tr_Ξ(𝒜')| ≤ S̄ distinct traces. A union bound over one
representative A per trace gives P_σ(Ψ_σΞ ∈ E₂) ≤ S̄·exp(−48nη²/169) for every Ξ; take expectations.

Steps 1 and 2 give P(E₁) ≤ 2S̄·exp(−48nη²/169). ∎

## T.4 Proof of Lemma T

*Step 0 (constants).* L ≥ d log e + 2(d + 1) log(2e) ≥ 1 + 4 log(2e) (d ≥ 1, eP/d ≥ e, n/(d + 1) ≥ 1, d + 1 ≥ 2) and
log(4/δ) > log 4, so nη² = 4L + 4 log(4/δ) > 4(1 + 4 log(2e) + log 4) > 36 ≥ 25 (log(2e) > 1.693, log 4 > 1.386).

*Step 1 (the bad event for the countable class).* By Lemma T-G, S_{𝒜₀}(2n) ≤ e^L. Let E₁ := {∃A ∈ 𝒜₀ : ν(A) > 2P_n(A) + η²}.
By Proposition R (applicable since nη² ≥ 25),
  P(E₁) ≤ 2e^L·exp(−nη²/4) = 2e^L·exp(−L − log(4/δ)) = δ/2.
From now on work on E₁ᶜ and fix T ⊆ {1, …, P} with |T| = d.

*Step 2 (all real thresholds).* Let a ∈ ℚ and u ∈ ℚ^P with supp u ⊆ T, and r > 0 real. Choose rationals r_k ↓ r with r_k > r.
Then A(a, u, r_k) ⊆ A(a, u, r_{k+1}) and ∪_kA(a, u, r_k) = A(a, u, r) (if |a + uᵀx| > r then |a + uᵀx| > r_k for all large
k). By continuity from below of the probability ν and of the finite measure P_n, letting k → ∞ in
ν(A(a, u, r_k)) ≤ 2P_n(A(a, u, r_k)) + η² gives ν(A(a, u, r)) ≤ 2P_n(A(a, u, r)) + η².

*Step 3 (layer cake; rational (a, u), every c > 0).* Let g := g_{a,u,c}. Since 0 ≤ g ≤ 1, g(x) = ∫₀¹1{g(x) > s} ds for every
x. For s ∈ (0, 1), min{1, z} > s ⟺ z > s, so {g > s} = {(a + uᵀx)² > sc} = A(a, u, √(sc)) with √(sc) > 0. By Tonelli
(the map (x, s) ↦ 1{g(x) > s} is jointly Borel) and Step 2,
  νg = ∫₀¹ ν(A(a, u, √(sc))) ds ≤ ∫₀¹ [2P_n(A(a, u, √(sc))) + η²] ds = 2P_ng + η².

*Step 4 (all real (a, u), supp u ⊆ T).* Choose rational (a_k, u_k) → (a, u) with supp u_k ⊆ T. For every x,
g_{a_k,u_k,c}(x) → g_{a,u,c}(x) (continuity of (a, u) ↦ a + uᵀx and of t ↦ min{1, t²/c}), and 0 ≤ g ≤ 1. By dominated
convergence νg_{a_k,u_k,c} → νg_{a,u,c}; P_ng_{a_k,u_k,c} → P_ng_{a,u,c} (finite average). Step 3 passes to the limit.

*Step 5 (all supports).* Every u with |supp u| ≤ d has supp u ⊆ T for some |T| = d (d ≤ P). Hence E₁ᶜ ⊆ Ω_T.

*Step 6 (measurability of the supremum).* Let 𝒬 := {(a, u, c) ∈ ℚ × ℚ^P × (ℚ ∩ (0, ∞)) : |supp u| ≤ d} (countable). For
fixed sample, (a, u, c) ↦ νg_{a,u,c} − 2P_ng_{a,u,c} is continuous on ℝ × ℝ^T × (0, ∞) for each T (pointwise continuity
in (a, u, c), domination by 1, dominated convergence), and ℚ × ℚ^T × (ℚ ∩ (0, ∞)) is dense there. Hence
  sup_{a, c>0, |supp u|≤d} (νg_{a,u,c} − 2P_ng_{a,u,c}) = sup_{(a,u,c)∈𝒬} (νg_{a,u,c} − 2P_ng_{a,u,c}),
a supremum of countably many random variables, hence a random variable, and Ω_T = {this supremum ≤ η²} is measurable.

*Conclusion.* P(Ω_T) ≥ P(E₁ᶜ) ≥ 1 − δ/2. ∎

## T.5 Remarks (scope, adversarial cases, use)

1. **Atoms, heavy tails, degenerate directions.** Nothing in §T.1–T.4 uses a property of ν beyond being a Borel
   probability: Step 1 of Prop. R uses only that nP'_n(A) is binomial; Step 2 only exchangeability. If a + uᵀx = 0
   ν-a.s., both sides are handled identically (νg = 0).
2. **d close to n.** The range d ≤ n − 1 is used only through 2n ≥ d + 1 (Lemma T-G) and the sign of log(2en/(d + 1));
   at d = n − 1 the remainder is ≥ 8(d + 1)log(2e)/n ≍ 1, so the lemma is true but empty there, as it should be.
3. **Use in DIST-1/2.** With a := â − α*, u := b − β*, c := 4σ*², g_{a,u,c} = min{1, Δ(x)²/(4σ*²)} of Lemma H (H.md §H.8),
   and |supp u| ≤ |S| + s₀^r. On Ω_T, simultaneously for every posterior draw with |S| ≤ d − s₀^r (and every data set
   with the same design rows): E_x min{1, Δ²/(4σ*²)} ≤ 2n⁻¹Σ_i min{1, Δ_i²/(4σ*²)} + η² ≤ (ε̄² + ‖μ̂ − μ‖²/n)/(2σ*²) + η²,
   by H-id. Ω_T depends on the design rows only, so it is independent of the noise.
4. **Why the multiplicative form.** Proposition R is exactly what the lemma needs; the ratio form (Appendix T.A) is
   stronger than needed and its provable constant is worse after Cauchy–Schwarz (6 instead of 4).

## Appendix T.A — ratio form and the Cauchy–Schwarz route (alternative; not needed above)

**Proposition R′.** Same setting as Proposition R. For θ ∈ (0, 1) and η > 0 with nθ²η² ≥ 1,
  P( ∃A ∈ 𝒜' : ν(A) − P_n(A) > η√ν(A) ) ≤ 2S̄·exp(−(1 − θ)²nη²/4).
*Proof.* E₁′ := ∪_k{ν(A_k) − P_n(A_k) > η√ν(A_k)}, E₂′ := ∪_k{P'_n(A_k) − P_n(A_k) > γ√(P_n(A_k) + P'_n(A_k))} with
γ := (1 − θ)η/√2.
*Ghost.* On E₁′ let τ be the first index as before; p := ν(A_τ) satisfies √p > η (since ν(A) − P_n(A) ≤ ν(A) forces
√ν(A) > η) and q := P_n(A_τ) < p − η√p. With Z := nP'_n(A_τ) ~ Bin(n, p) given τ, T1 with t := nθη√p gives
P(Z/n < p − θη√p) ≤ np(1 − p)/(np(1 − p) + n²θ²η²p) = (1 − p)/((1 − p) + nθ²η²) ≤ 1/(1 + nθ²η²) ≤ ½. Put
p' := p − θη√p = √p(√p − θη) > 0. The function h(x) := (x − q)/√(x + q) is increasing on (0, ∞) (h′(x) = (x + 3q)/(2(x + q)^{3/2})
> 0), so on {P'_n(A_τ) ≥ p'}: h(P'_n(A_τ)) ≥ h(p'), and p' − q > (1 − θ)η√p > 0, 0 < p' + q < 2p, so
h(p') > (1 − θ)η√p/√(2p) = γ; i.e. E₂′ holds. Independence gives P(E₂′) ≥ ½P(E₁′) as in Prop. R.
*Swaps.* With the notation of Step 2 of Prop. R, the condition of E₂′ for A after Ψ_σ reads W_A/n > γ√(N_A/n), i.e.
W_A > γ√(nN_A) (impossible if N_A = 0). By T2, P_σ(W_A > γ√(nN_A)) ≤ exp(−γ²nN_A/(2‖a‖²)) ≤ exp(−γ²n/2)
= exp(−(1 − θ)²nη²/4). Union over ≤ S̄ traces. ∎
**Cauchy–Schwarz route to Lemma T with prefactor 6.** Let η₆² := (6/n)[L + log(4/δ)] and θ := 1/7. Then
nθ²η₆² > 6·9.15/49 > 1 (Step 0 of §T.4) and (1 − θ)²·6/4 = (36/49)(3/2) = 54/49 ≥ 1, so by Prop. R′ and Lemma T-G the bad
event has probability ≤ 2e^L e^{−(54/49)(L + log(4/δ))} ≤ 2e^{−log(4/δ)} = δ/2. On its complement, ν(A) − P_n(A) ≤
η₆√ν(A) for all A ∈ 𝒜₀; it extends to real thresholds by the monotone limits of Step 2 (both sides converge). For
rational (a, u) and c > 0, with A_s := {g > s}: by the layer cake and Cauchy–Schwarz on ([0, 1], ds),
  νg − P_ng = ∫₀¹(ν(A_s) − P_n(A_s)) ds ≤ η₆∫₀¹√ν(A_s) ds ≤ η₆(∫₀¹ν(A_s) ds)^{1/2} = η₆√(νg),
and η₆√(νg) ≤ νg/2 + η₆²/2 (AM–GM) gives νg ≤ 2P_ng + η₆². Steps 4–6 of §T.4 apply verbatim. So this route proves
Lemma T with 4 replaced by 6 in η²_n; the direct route of §T.3–T.4 proves it as stated.
