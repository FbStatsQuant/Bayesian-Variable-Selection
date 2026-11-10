# L6 — Proposition SCR-N (sharpness of the visibility threshold at q = 0)

Uses L1 (L1.2-L1.4), L2 ((T1), E2⁻).

**Statement.** Model G, EX-A, n ≥ 3, p ≥ 1. Let L_n := 2 log(2p−1) + log n,
B_n := ((n+1)/n)(n − 0.98)(1 − exp(−L_n/(n + 0.02))), and x > 0 with 4a_x ≤ 1 (a_x = √(x/(n−1))). If
 (i) √γ(t|∅) + σ√(2 log(2s₀) + 2x) ≤ τ_n(1 − 4a_x)√B_n for every t ∈ S₀, and
 (ii) √γ(j|∅) + σ√(2 log(2p) + 2x) ≤ τ_n(1 − 4a_x)√B_n for every j ∉ S₀,
then P(∅ is LO) ≥ 1 − 4e^{-x}. Here γ(j|∅) = (x_jᵀμ)²(n+1)/n², and
(1 − n^{-2})(1 − u_n/2)L_n ≤ B_n ≤ L_n with u_n := L_n/(n + 0.02); so B_n = L_n(1 + o(1)) when log p = o(n).

*Proof.* *At the empty model.* R_∅ = I, a(j|∅) = n − 1 + 1/(n+1) = n²/(n+1), a_1(j|∅) = n, so D(j|∅) = n,
γ(j|∅) = (x_jᵀμ)²(n+1)/n², Q_∅ = n − 1 and (n/(n+1))g_y(j|∅) = (x_jᵀy)²/n. K ≥ 1, so 𝒩(∅) is the set of the p
singletons, and by L1.4 (k = 0)
 F({j}) − F(∅) = −log(2p−1) − ½ log n + ν·log[(n − 0.98)/(n − 0.98 − (x_jᵀy)²/n)].
Since (log(2p−1) + ½ log n)/ν = L_n/(n + 0.02), F({j}) ≤ F(∅) iff (x_jᵀy)²/n ≤ (n − 0.98)(1 − exp(−L_n/(n+0.02))),
i.e. (using (x_jᵀy)²/n = (n/(n+1))·g_{y_c}(j|∅)/τ̂²) iff
 g_{y_c}(j|∅) ≤ τ̂²·B_n.   (★)
The bounds on B_n: put c_n := (n+1)(n − 0.98)/(n(n + 0.02)) = 1 − 0.98/(n² + 0.02n) ∈ [1 − n^{-2}, 1), so
B_n = c_n(n + 0.02)(1 − e^{-u_n}). Upper: 1 − e^{-u} ≤ u gives B_n ≤ c_nL_n ≤ L_n. Lower: if u_n ≥ 2 the claimed lower
bound is ≤ 0 < B_n; if u_n < 2, 1 − e^{-u} ≥ u(1 − u/2) ≥ 0 gives B_n ≥ c_n(1 − u_n/2)L_n ≥ (1 − n^{-2})(1 − u_n/2)L_n.
*Noise.* g_{y_c}(j|∅)^{1/2} = |x_jᵀμ + x_jᵀε|/a(j|∅)^{1/2} ≤ √γ(j|∅) + |ζ_j|, ζ_j := x_jᵀε/a(j|∅)^{1/2} ~ N(0, σ²v),
v = (n−1)(n+1)/n² < 1 (x_j is centred, so x_jᵀCε = x_jᵀε). By (T1) and union bounds, with probability ≥ 1 − 2e^{-x}:
|ζ_t| ≤ σ√(2 log(2s₀) + 2x) for all t ∈ S₀ and |ζ_j| ≤ σ√(2 log(2p) + 2x) for all j ∉ S₀. On E2⁻(x) (probability
≥ 1 − 2e^{-x}; it is an event about the noncentral quantity ‖μ + Cε‖², see L2), τ̂² ≥ τ_n²(1 − 4a_x) ≥ τ_n²(1 − 4a_x)².
*Conclusion.* On the intersection (probability ≥ 1 − 4e^{-x}), (i)-(ii) give
g_{y_c}(j|∅)^{1/2} ≤ τ_n(1 − 4a_x)√B_n ≤ τ̂√B_n for every j, i.e. (★): no addition to ∅ strictly improves F, and ∅ has
no other neighbour. ∎

**Consequence 1 (the constant of (A∞) at q = 0, for the statement about LO models).** Fix A > 0, δ ∈ (0, 1), σ > 0
and take the sequence: p = ⌈n^A⌉ ∨ 2, s₀ = 1, S₀ = {1}, x_1 orthogonal to all other columns (the other columns are
arbitrary centred columns of norm² n−1 in the orthogonal complement of {1, x_1}, n ≥ 4), and θ*_1 > 0 defined by
γ(1|∅) = (1 − δ)²τ_n²(2 log p + log n), i.e. θ*_1²(n−1)²(n+1)/n² = (1−δ)²(σ² + θ*_1²)(2 log p + log n) (solvable for
large n; θ*_1 ≍ √(log n / n), τ_n → σ). Then Γ_n(0) = γ(1|∅), so the ratio in (A∞) at q_n = 0 equals 1 − δ.
Take x_n := √(log n). (ii): γ(j|∅) = 0 for j ≠ 1 and σ√(2 log(2p) + 2x_n) ≤ τ_n(1 − 4a_{x_n})√B_n for large n, because
B_n = (2 log p + log n)(1 + o(1)), τ_n ≥ σ and 2 log(2p) + 2x_n = 2 log p + o(log n). (i):
(1 − δ)τ_n√(2 log p + log n) + σ√(2 log 2 + 2x_n) ≤ τ_n(1 − 4a_{x_n})√B_n for large n. Hence P(∅ is LO) → 1: with
probability → 1 there is an LO model of size 0 missing S₀, although √Γ_n(0) is within the factor 1 − δ of the
threshold of (A∞). So in (A∞) the constant 1 multiplying τ_n√(2 log p + log n) cannot be replaced by a smaller one
(as a statement about all LO models of size ≤ q_n; whether the code then reports ∅ is not claimed — N1 shows that it
does report certified sparse models missing truths when signals are below the threshold).

**Consequence 2 (a margin condition Δ_n(0) ≥ C log(p ∨ n) alone does not give screening).** Take p = s₀ = 2,
S₀ = {1, 2}, x_1ᵀx_2 = (n−1)r with 1 − r = 1/n, θ* = (b, −b) with b² = (log n)², σ fixed. Then μ = b(x_1 − x_2),
Δ_n(0) = Δ(∅) = ‖μ‖² = 2(n−1)b²(1−r) ~ 2(log n)², so Δ_n(0)/log(p ∨ n) → ∞ and τ_n² = σ² + 2b²(1−r) → σ². But
x_1ᵀμ = −x_2ᵀμ = (n−1)b(1−r), so γ(1|∅) = γ(2|∅) = (n−1)²(n+1)b²(1−r)²/n² ~ (log n)²/n → 0. With x_n = √(log n),
(i) holds for large n (left side = o(√log n), right side ~ σ√(log n)) and (ii) is void. Hence P(∅ is LO) → 1: a
hypothesis of the form Δ_n(0) ≥ C log(p ∨ n) alone does not give screening. Here ‖θ*‖₁ = 2 log n, and Lemma B1's lower
bound Δ(√Δ − c_θ)²/(n‖θ*‖₁²) ~ (log n)²/n is asymptotically equal to Γ_n(0) (their ratio tends to 1, since
c_θ/√Δ = √(n/(n²−1)) → 0 and Γ_n(0)/[Δ²/(n‖θ*‖₁²)] = (n+1)/n): B1 is order-sharp on this sequence. (That the numerator of B1 must be homogeneous of degree 4 in θ* — "the square" — follows from scaling:
replacing θ* by tθ* multiplies Γ_n, Δ_n and ‖θ*‖₁² by t², so a bound of the form Γ_n ≥ c·Δ_n/(n‖θ*‖₁²) would fail as
t ↓ 0.)
