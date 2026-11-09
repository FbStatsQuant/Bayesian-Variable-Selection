# L5 — Instances (claim (C5))

Status: (a), (b) **PROVED (by this seat, unchecked)**; lemma check R04 (Codex Sol high,
reviews/R04_L4L5_check_sol.md): VERIFIED-WITH-AMENDMENTS (amendments 2–7 applied, reviews/R04_disposition.md). (b) uses one finite exact computation (TV margin τ₀ on the coded partition: R04 amendment 6,
re-run as numerics/f2_exact_tau0.py → numerics/F2_exact_tau0.txt).

## (a) AR(1), exact Gram (study S2's population design)

**Design.** Σ_ij = ρ^{|i−j|} (p × p), fixed ρ ∈ (−1, 1) ∖ {0}; X standardized with XᵀX = (n − 1)Σ (requires
p ≤ n − 1; A := 1, any A ≥ 1 may be used); fixed s₀ and θ* (on the standardized scale), σ² > 0 fixed;
**separation**: for every j ∈ S₀, Σ_{k∈S₀∖{j}} |θ*_k||ρ|^{|j−k|} ≤ ½|θ*_j|(1 − ρ²)/(1 + ρ²). Any partition with blocks
of size ≤ 16 (in particular the method's). Put η := η_A/2, θ_max := max|θ*_k|,
  d_n := ⌈log n/(2 log(1/|ρ|))⌉  (so |ρ|^{2d_n} ≤ 1/n),
  𝒫⁰_n := {l ∉ S₀ : min_{k∈S₀}|l − k| ≤ d_n},  Q⁰_n := S₀ ∪ 𝒫⁰_n  (|𝒫⁰_n| ≤ 2s₀d_n);
  **definition (R04 amendment 2):** 𝒫_n := 𝒫⁰_n if Q⁰_n = [p] or p ≥ 2|Q⁰_n| + 32s₀ + 1, and 𝒫_n := [p] ∖ S₀
  otherwise; Q := S₀ ∪ 𝒫_n. In all cases |Q| ≤ 4s₀d_n + 34s₀ + 1 = O(log n) (in the second case p < 2|Q⁰_n| + 32s₀ + 1).

**Reduction to ρ > 0.** With D := diag((−1)^i), XD has Gram (n − 1)DΣD, (DΣD)_ij = |ρ|^{|i−j|}; replace θ* by Dθ*
(μ unchanged). Every quantity used below (δ², Z², RSS, F, |r̂| and hence the partition, λ_min) is invariant under
column sign flips. So assume 0 < ρ < 1.

**Population facts (Gaussian AR(1) vector x ~ N(0, Σ)).**
(P1) Spectrum: λ(Σ_T) ∈ [(1 − ρ)/(1 + ρ), (1 + ρ)/(1 − ρ)] for every nonempty T (the eigenvalues of the Toeplitz
matrix Σ lie between the extrema of its spectral density (1 − ρ²)/(1 − 2ρ cos ω + ρ²); principal submatrices
interlace).
(P2) Markov: for l ∉ T, E[x_l | x_T] = c_a x_a + c_b x_b where a (b) is the largest (smallest) element of T below
(above) l (a term is absent if no such element exists): the AR(1) chain is Markov, so x_l ⟂ x_{T∖{a,b}} | (x_a, x_b).
(P3) Conditional variance: Var(x_l | x_T) ≥ Var(x_l | x_{−l}) = 1/(Σ⁻¹)_ll ≥ (1 − ρ²)/(1 + ρ²) (for p ≥ 2 the AR(1)
precision is tridiagonal with diagonal entries (1 + ρ²)/(1 − ρ²) inside and 1/(1 − ρ²) at the ends; for p = 1,
Var = 1 and the bound is immediate).
(P4) Conditional covariance: for j ≠ k, both ∉ T: 0 ≤ Cov(x_j, x_k | x_T) ≤ ρ^{|j−k|}.
*Proof of (P4).* If some element of T lies strictly between j and k, the Markov property gives
Cov(x_j, x_k | x_T) = 0. Otherwise let j < k (wlog), a := max{t ∈ T : t < j}, b := min{t ∈ T : t > k} (either may be
absent); by the Markov property Cov(x_j, x_k | x_T) = Cov(x_j, x_k | x_a, x_b). For a < s ≤ t:
Cov(x_s, x_t | x_a) = ρ^{t−s} − ρ^{s−a}ρ^{t−a} = ρ^{t−s}(1 − ρ^{2(s−a)}); conditioning further on x_b (b > t):
Cov(x_j, x_k | x_a, x_b) = ρ^{k−j}(1 − ρ^{2(j−a)}) − [ρ^{b−j}(1 − ρ^{2(j−a)})][ρ^{b−k}(1 − ρ^{2(k−a)})]/(1 − ρ^{2(b−a)})
= ρ^{k−j}(1 − ρ^{2(j−a)})(1 − ρ^{2(b−k)})/(1 − ρ^{2(b−a)}) ∈ [0, ρ^{k−j}]
(algebra: 1 − ρ^{2(b−k)}(1 − ρ^{2(k−a)})/(1 − ρ^{2(b−a)}) = (1 − ρ^{2(b−k)})/(1 − ρ^{2(b−a)}); with A := ρ^{2(j−a)},
B := ρ^{2(b−k)}, C := ρ^{2(k−a)} ≤ A, the factor (1 − A)(1 − B)/(1 − BC) lies in [0, 1] because
(1 − BC) − (1 − A)(1 − B) = A(1 − B) + B(1 − C) ≥ 0). One-sided and empty cases (R04 amendment 4): only a present:
Cov = ρ^{k−j}(1 − ρ^{2(j−a)}); only b present: Cov = ρ^{k−j}(1 − ρ^{2(b−k)}); neither: Cov = ρ^{k−j}. All lie in
[0, ρ^{k−j}]. ∎
(P5) Exact-Gram identities: for U ⊆ [p], l ∉ U: x_lᵀ(I − P_U)μ = (n − 1)Cov(x_l, μ | x_U) with μ := Σ_k θ*_k x_k
(population), ‖(I − P_U)x_l‖² = (n − 1)Var(x_l | x_U), hence δ²_{U,l} = (n − 1)Cov(x_l, μ | x_U)²/Var(x_l | x_U); and
P_U x_l = X_U Σ_UU⁻¹Σ_{Ul} (sample regression = population regression). Also
Cov(x_l, μ | x_U) = Σ_{k∈S₀∖U} θ*_k Cov(x_l, x_k | x_U) (terms with k ∈ U vanish).

**Claim (a).** (H0), (G1), (G2), (G3a–c) and (G4-dir) hold; hence Theorem L4.1 applies (with MR1).
*Proof.*
* (H0): R: ‖μ‖² = (n − 1)θ*ᵀΣθ* ≤ (n − 1)‖θ*‖²(1 + ρ)/(1 − ρ) (P1). SE_λ(j₀) and the floors below: φ₀² :=
  (1 − ρ)/(1 + ρ) (P1). SE_w(m♯_n; g₀): λ_min(X_{S₀∪J}ᵀX_{S₀∪J}) ≥ (n − 1)φ₀² ≥ g₀ := 1 for all J, n ≥ n₀. BM-∞:
  θ*_min fixed > 0. s₀ ≤ K eventually. p ≤ n − 1 ≤ n^A.
* (G1): by the piecewise definition, |Q| ≤ 4s₀d_n + 34s₀ + 1 ≤ C_Q log n eventually; either Q = [p] (then
  p = O(log n) ≤ ⌊n/2⌋ eventually, so K = p = |Q|), or Q = Q⁰_n ≠ [p] with p ≥ 2|Q| + 32s₀ + 1 and, since
  2|Q| + 32s₀ + 1 = O(log n) ≤ ⌊n/2⌋ eventually, K ≥ 2|Q| + 32s₀ + 1. |Q| ≤ K for n ≥ n₀. In the enlarged case NEG
  is vacuous; enlargement only removes indices from the NEG obligation.
* (G2), (G3a): (P1).
* (G3b) TV: for j ∈ S₀ and any U ∌ j (any |U|), by (P5), (P3), (P4) and separation,
  |Cov(x_j, μ | x_U)| ≥ |θ*_j|Var(x_j | x_U) − Σ_{k∈S₀∖(U∪{j})}|θ*_k|ρ^{|j−k|} ≥ ½|θ*_j|(1 − ρ²)/(1 + ρ²),
  and Var(x_j | x_U) ≤ 1, so δ²_{U,j} ≥ (n − 1)θ*²_min(1 − ρ²)²/(4(1 + ρ²)²) =: c_a(n − 1) ≥ M_n log n with
  M_n := c_a(n − 1)/log n → ∞.
* (G3c) NEG(η): for l ∉ Q and any U ∌ l: by (P4), |Cov(x_l, μ | x_U)| ≤ Σ_k |θ*_k|ρ^{|l−k|} ≤ s₀θ_maxρ^{d_n+1}
  ≤ s₀θ_maxρ^{d_n}, and Var(x_l | x_U) ≥ (1 − ρ²)/(1 + ρ²) (P3), so
  δ²_{U,l} ≤ (n − 1)s₀²θ²_maxρ^{2d_n}(1 + ρ²)/(1 − ρ²) ≤ s₀²θ²_max(1 + ρ²)/(1 − ρ²) ≤ ησ² log n for n ≥ n₀
  (ρ^{2d_n} ≤ 1/n). (No restriction on U is needed; the leakage is O(1).)
* (G4-dir): for T ∈ 𝓛 and l ∉ T, by (P5) and (P2), (I − P_T)x_l = x_l − c_a x_a − c_b x_b with a, b the nearest
  elements of T below/above l (T ⊆ Q). So u_{T,l} is determined by (l, a, b) with a, b ∈ Q ∪ {none}:
  |{u_{T,l}}| ≤ p(|Q| + 1)², N_n := (|Q| + 1)² = O(log² n), log N_n = o(log n). ∎

**Scope remark (rewritten after R04 amendment 3).** p ≤ n − 1 is forced by the exact-Gram construction; fixed p is
allowed. When p_n ≥ d_n + 2s₀, |𝒫_n| ≥ min(d_n, p − s₀) − s₀, i.e. the relevance set grows like log n. What is
proved about the start mode is only the sandwich S₀ ⊆ S̃₀ ⊆ Q (L3); no law for which proxies enter is claimed.
Proxies at intermediate distances (squared partial signal comparable to log n) can be neither VIS-strong nor
NL-negligible, which is one obstruction to GEN's bounded-reference route; the sandwich route does not need to
resolve them.

## (b) Study S5 population design, fixed p

**Design.** Exact Gram XᵀX = (n − 1)Σ with Σ = 0.3·11ᵀ + 0.4·blockdiag(1₅1₅ᵀ) + 0.3I (groups of 5, within-group
correlation 0.7, between 0.3), p = 100, s₀ = 4 with **the diagnostic p = 100 truth layout used in the numerical
port** (zero-based support {2, 26, 53, 75}; not the production generator's declared truth, which exists only at
p ∈ {30, 500, 1000}) and θ* = c(1.4, −1.0, 1.8, −1.2), c ∈ {0.5, 1}, σ² = 1; n → ∞.
**Claim (b).** With 𝒫 := [p] ∖ S₀ (Q = [p]): (H0), (G1), (G2), (G3a), (G3c) (vacuous), (G4-χ) hold for n large;
(G3b) holds iff τ₀ := min_b min_{j∈S₀∩C_b} min_{U⊆C_b∖{j}} Cov(x_j, μ | x_U)²/Var(x_j | x_U) > 0 on the coded
partition, which is a finite computation. **Result:** on the coded partition (consecutive blocks {10b, …, 10b + 9}; each truth
block = the truth's group + one paired group), τ₀ = 4/25 for c = 1 and 1/25 for c = 0.5 (exact rational arithmetic
over the 120 truth/count cases; R04 amendment 6, re-run as numerics/f2_exact_tau0.py → numerics/F2_exact_tau0.txt;
the script also computes and prints the partition with the Python port's partition routine, R08 item 6). Hence TV holds, and Theorem L4.1 applies (with MR1, or with ℓ_n once
(1 − δ₀) log n ≥ 96).

*The certificate, written out (after R05 item 1).* (i) **Partition.** The sample correlation matrix equals Σ.
Complete linkage on 1 − |r|: all within-group distances are 0.3 < 0.7 (between-group), so each group of five merges
first (internal ties broken lexicographically, which does not affect the resulting group clusters); the groups then
merge at the common height 0.7, and the lexicographic tie rule on sorted index lists makes the merges proceed in
increasing index order (a chain {g₁}∪{g₂}, then ∪{g₃}, …). The top-down cut at B = 10 splits every node with more than
10 members into its two children; along the chain this leaves the first two groups together and the later groups as
single five-element leaves; next-fit packing in leaf order with capacity 10 then pairs consecutive groups. Result:
blocks {10b, …, 10b + 9}, b = 0, …, 9 (the analytic derivation above is the proof; the Python port's routine —
a diagnostic component with a 10⁻¹⁰ linkage tie tolerance, not the production code — prints the same partition in
numerics/F2_exact_tau0.txt; also derived independently in R04 amendment 6). (ii) **Reduction.** The truths (zero-based 2, 26, 53, 75) lie in blocks
0, 2, 5, 7, one per block; each truth block = the truth's own group (4 other members) + one paired group (5 members).
By exchangeability within groups, Cov(x_j, μ | x_U) and Var(x_j | x_U) depend on U ⊆ C_b ∖ {j} only through
a := |U ∩ own group| ∈ {0, …, 4} and b := |U ∩ paired group| ∈ {0, …, 5}: 30 cases per truth, 120 in all. The
regression of x_j on the conditioning variables has constant coefficients g (own group) and d (paired group) solving
a 2 × 2 system; the unconditional covariances are Cov(x_j, μ) = θ_j + 0.3Σ_{k≠j}θ_k = 0.7θ_j + 0.3Σ_kθ_k (R08 item 1), Cov(x_u, μ) = 0.4θ_j +
0.3Σ_kθ_k for u in the own group and 0.3Σ_kθ_k in the paired group (Σ_kθ_k = c·1.0). (iii) **Exact evaluation** of
Cov²/Var over the 120 cases in rational arithmetic gives the minima 2028/2945, 4/25, 3267/2945, 729/2500 (c = 1;
multiply by c²), minimum 4/25 at truth 26 with U = ∅.
*Proof.* Σ = 0.3I + (positive semidefinite), so λ_min(Σ_T) ≥ 0.3 =: φ₀²
for every T; (H0) as in (a). B = min(⌊√n⌋, ⌊√p⌋, 16) = 10 for n ≥ 100, and the sample correlation matrix equals Σ,
so the coded partition does not depend on n. (G1): |𝒫| = 96 is fixed; Q = [p] (first alternative). (G4-χ):
96 ≤ (1 − δ₀) log n for n ≥ exp(96/(1 − δ₀)). (G3b): by (P5) (valid for any exact-Gram design),
δ²_{U,j} = (n − 1)Cov(x_j, μ | x_U)²/Var(x_j | x_U) ≥ (n − 1)τ₀ ≥ M_n log n with M_n := (n − 1)τ₀/log n. ∎

**Honest reading.** (b) is asymptotic in a strong sense (the sufficient NA route (G4-χ) needs log n ≳ 96); it shows
that S5's population covariance satisfies the hypotheses of Theorem GROW, not that the theorem's onset is near the
study's n. In the observed LS0 runs (D3, iid rows: uncapped LS0 reaches S₀ from the start mode in 80/80 runs at
n = 3200, 12800) the cap was the binding obstruction on those paths; this does not establish NA on the lattice, and
neither the numerics nor the sufficient condition identifies the true onset of NA (R04 amendment 7).

**Fixed-p caveat (council R10 F1).** For fixed p the production run takes the exact-enumeration branch once
Σ_{k≤K} C(p,k) ≤ (5H₀ + 4N₀)p (SoP `02_method.tex:167`); for p = 100 this happens at n ≳ 2.5·10²⁷ (ln n ≈ 63), before
the (G4-χ) onset ln n ≥ 96/(1 − δ₀). At those n, S₀ is scored by enumeration and the conclusion follows from T03♯
alone (L4 note (1)); MR1 and the LS0 descent play no role. (b) therefore shows only that S5's population covariance
satisfies the hypotheses of Theorem GROW, not that LS0 is the operative mechanism. The same applies to fixed-p (or
p growing slower than about log₂ n) sequences in (a) and (c); what Theorem GROW adds beyond T03♯ + enumeration lies
in the regime p ≫ log n, covered by (a) with growing p ≤ n − 1 and (c) with p ≤ n^A.
