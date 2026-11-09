# L1 — POST: the posterior-level hypotheses for random Gaussian designs

Status: **PROVED (by this seat, unchecked)**. Check record: R02 (Codex gpt-6.1-sol high,
`reviews/R02_L1L2_check_sol.md`): VERIFIED-WITH-AMENDMENTS (1 MAJOR, 2 MINOR on remarks/raw-scale wording), all applied
(marked [R02-#]).
Falsification numerics: `numerics/post_check.py` → `numerics/post_check_out.txt`.

## Setting
STATEMENT §1: raw rows iid N(m, Σ_n), Σ_n unit-diagonal WLOG (population correlation matrix), p = p_n ≤ n^A
(A ≥ 1 fixed, p ≫ n allowed, p ≥ max(2, s₀); p = 1 means s₀ = 1, Ω = {∅, {1}}, and only R and BM matter — omitted), X = centred, sample-standardised design, R̂ := XᵀX/(n − 1) (the sample
correlation matrix), Y = Xθ* + Cε with fixed S₀, |S₀| = s₀, θ*_j ∈ [θ_lo, θ_hi] in absolute value on S₀, θ* = 0 off S₀,
ε ~ N(0, σ²I) independent of the raw design. (Raw-scale convention, fixed raw slopes with |β_j| ∈ [b_lo, b_hi] and unit population variances [R02-3]: then
θ* = D_xβ is raw-design-measurable; use the raw-design event 𝒢_n ∩ ℋ_n, ℋ_n := {all sample/population sd ratios in
[½, 2]} (P(ℋ_n) → 1 by χ² tails and p ≤ n^A), take θ_lo = b_lo/2, θ_hi = 2b_hi, and run the diagonal argument over
raw-design sequences; otherwise unchanged.) For the standardised-signal convention: conditionally on X, Y is
Gaussian on the centred contrast space with mean Xθ* and noise variance σ², so the posterior's noise kernel depends
only on X and the supremum over standardised designs below is legitimate [R02-4] (model G with β := D_x⁻¹θ*, which is
raw-design-measurable, not X-measurable).

Write j₀ := ⌈(2A + 1)s₀⌉ + 1 and
  m̄_n := ⌈[s₀(A log n + log 2) + log 2 + ((s₀ + 2)/2) log n] / log(3/2)⌉,  k̄_n := min(p, s₀ + max(j₀, m̄_n)).

**Hypothesis LSF (logarithmic sparse floor).** (i) λ_min(Σ_{n,S}) ≥ φ² for every S with |S| ≤ min(p, s₀ + j₀),
for a fixed φ ∈ (0, 1]; and (ii) λ_min(Σ_{n,S}) ≥ ψ_n for every S with |S| ≤ k̄_n, where
ψ_n √n/(log n)^{3/2} → ∞. (If λ_min(Σ_n) ≥ c > 0 for all n, both hold with φ² = ψ_n = c.)

## Lemma POST
**(a)** Under LSF there are X-measurable events 𝒜_n with P(𝒜_n) → 1 on which every design satisfies the T03♯
hypotheses R (with M := s₀²θ_hi² + 1 and φ₀² := φ²/2), SE_λ(j₀) (φ₀²), SE_w(m♯_n; g₀) (g₀ := 1), s₀ ≤ K, and BM-∞ with
the deterministic envelope θ_lo² nφ₀²/(σ² log n) → ∞ — with these common constants and envelope, for n ≥ n₀.
**(b)** Consequently, under the joint law of (raw design, ε): 1 − π(S₀) = O_P(√(log n/n)), and the conclusions of
SL1 (a)–(e) hold with r_n = √(log n/n) (PIP sure screening and specificity uniformly in j, MPM, ξ_q for fixed q ∈ (0, 1) or
deterministic q_n with r_n = o(min(q_n, 1 − q_n)) only, exact HPM, model size); without beta-min (θ*_j allowed to vary, some → 0) the inclusion clause for J_n(c) holds likewise.
**(c)** (Fixed exact-Gram designs.) If XᵀX = (n − 1)Σ_n exactly (p ≤ n − 1) and LSF(i) holds with ψ_n ≥ 1/(n − 1) in
(ii), the T03♯ hypotheses hold deterministically with φ₀² = φ², g₀ = 1.

*Proof.* (1) *m♯_n ≤ m̄_n.* For p ≥ 2 and k ≤ p, C(p, k)/C(2p − 1, k) = Π_{i<k}(p − i)/(2p − 1 − i) ≤ (p/(2p − 1))^k ≤ (2/3)^k,
and C(2p − 1, s₀) ≤ (2p)^{s₀}. With w(k) = [2C(2p − 1, k)]⁻¹,
R_m = Σ_{k=m+1}^{K} C(p,k)w(k)/w(s₀) ≤ (2p)^{s₀} Σ_{k>m}(2/3)^k = 2(2p)^{s₀}(2/3)^m.
This is ≤ n^{−(s₀+2)/2} as soon as m log(3/2) ≥ s₀ log(2p) + log 2 + ((s₀+2)/2) log n, which holds at m = m̄_n because
p ≤ n^A. Since R_m is nonincreasing in m and R_K = 0, m♯_n ≤ min(K, max(s₀, m̄_n)). Every set S₀ ∪ J used by
SE_λ(j₀) or SE_w(m♯_n; g₀) therefore has size ≤ k̄_n (and ≤ p), and m̄_n ≤ C₁ log n with C₁ depending on (A, s₀) only.
(2) *Entrywise event.* GROW L6.2, first paragraph (status: PROVED (by this seat, unchecked); checks R07 VERIFIED, R06
VERIFIED-WITH-AMENDMENTS), proves for iid Gaussian rows with unit population variances — its argument uses only
Gaussianity, unit variances and a union bound over (p + 1)² entries, not the AR(1) structure — that with
ħ_n := C_A√(log n/n), C_A a sufficiently large constant depending on A, the event
  𝒢_n := {max_{j,k} |R̂_jk − Σ_jk| ≤ C′ħ_n}
(C′ a fixed multiple) has P(𝒢_n) → 1 and is measurable in X. (The noise column is not needed here.)
(3) *Sparse eigenvalues on 𝒢_n.* For |S| ≤ k̄_n, ‖R̂_S − Σ_S‖₂ ≤ |S| max_{j,k∈S}|R̂_jk − Σ_jk| ≤ k̄_n C′ħ_n
≤ C″(log n)^{3/2}/√n =: ε_n → 0 (Weyl; operator norm ≤ size × max entry). Hence on 𝒢_n:
 – for |S| ≤ s₀ + j₀ (fixed size): λ_min(R̂_S) ≥ φ² − ε_n ≥ φ²/2 for n ≥ n₀; this gives R's eigenvalue part
   (S = S₀) and SE_λ(j₀) with φ₀² = φ²/2;
 – for |S| ≤ k̄_n: λ_min(XᵀX)_S = (n − 1)λ_min(R̂_S) ≥ (n − 1)(ψ_n − ε_n) ≥ (n − 1)ψ_n/2 ≥ 1 = g₀ for n ≥ n₀, since
   ε_n = o(ψ_n) and nψ_n → ∞ by LSF(ii). This is SE_w(m♯_n; 1).
(4) *Energy and beta-min.* ‖μ‖² = ‖Xθ*‖² = (n − 1)θ*_{S₀}ᵀR̂_{S₀}θ*_{S₀} ≤ (n − 1)s₀‖θ*‖² ≤ s₀²θ_hi² n (|R̂_jk| ≤ 1,
so λ_max(R̂_{S₀}) ≤ s₀): R holds deterministically with M. θ*_min ≥ θ_lo deterministically gives BM-∞ with the stated
envelope. s₀ ≤ K = min(p, ⌊n/2⌋) for n ≥ 2s₀.
(5) *Transfer to the joint law (b).* Put 𝒜_n := 𝒢_n for n ≥ n₀. Conditionally on X, Y = Xθ* + Cε with the law of Cε
not depending on X (the convention of GROW L6 §7) [R02-4]. Every deterministic sequence
x_n ∈ 𝒜_n satisfies all T03♯ hypotheses with the common constants (φ₀, g₀, M, A, s₀) and the common BM envelope, so
T03♯ applies along it. The diagonal tightness transfer (C-PACK `lemmas/I4_SL_corollaries.md:57-60`, the argument of
GROW L6 §7 and GEN L5.3) then gives: for every η > 0 there are M_η, n_η with
sup_{x∈𝒜_n} P_ε(1 − π_x(S₀) > M_η√(log n/n)) ≤ η for n ≥ n_η. [Argument: if not, there are η > 0, n_k ↑ ∞ and
x_{n_k} ∈ 𝒜_{n_k} with P_ε(1 − π_{x_{n_k}}(S₀) > k√(log n_k/n_k)) > η; completing with arbitrary x_n ∈ 𝒜_n at the
other indices gives a deterministic sequence satisfying T03♯'s hypotheses along which the ratio is not O_P(1),
contradicting T03♯.] Integrating over the design and adding P(𝒜_nᶜ) → 0 gives the joint-law O_P statement.
SL1 (a)–(e) are deterministic or law-free consequences of δ_n = O_P(r_n) (SL1 is stated "under some law"), so they
hold under the joint law (instance type I-b/I-c). The J_n(c) clause transfers by the same diagonal argument.
(6) *(c).* With XᵀX = (n − 1)Σ_n, R̂ = Σ_n exactly; (3) holds with ε_n = 0; (4) unchanged. ∎

## Remarks (scope; no further claims)
1. λ_max is never used [R02-1]: equicorrelation with 1 − ρ_n bounded below, factor models whose POPULATION
   CORRELATION matrices have a fixed positive eigenvalue floor (sufficient: raw covariance BBᵀ + D with D ⪰ dI and
   uniformly bounded raw marginal variances, giving floor ≥ d/max_jVar(W_j)), and stationary (incl. long-memory)
   Toeplitz correlation matrices whose spectral densities, normalised by γ(0), have a uniform positive lower bound,
   satisfy LSF even though λ_max(Σ_n) → ∞. Counter-examples to unqualified membership: ρ_n = 1 − n⁻²; raw covariance
   n²11ᵀ + I (fixed raw idiosyncratic floor, correlation floor 1/(n² + 1)).
2. [R02-2] A uniform positive population floor on the ANCHORED sets S₀ ∪ J, |J| ≤ j₀, is necessary for the
   corresponding sample anchored floors to hold w.p. → 1 (if λ_min(Σ_{n,S_n}) → 0 for some such S_n, then
   λ_min(R̂_{S_n}) → 0 in probability on 𝒢_n); LSF(i), which quantifies over all sets of that size, is a convenient
   stronger sufficient condition (R02 example: a degenerating 5-null equicorrelated block away from S₀ violates
   LSF(i) but not the anchored floors). Nothing is claimed necessary for posterior consistency itself.
3. Gaussianity enters only through 𝒢_n (and through T03♯'s Gaussian noise). Sub-Gaussian rows would give the same
   entrywise event by Bernstein's inequality; not claimed here.
