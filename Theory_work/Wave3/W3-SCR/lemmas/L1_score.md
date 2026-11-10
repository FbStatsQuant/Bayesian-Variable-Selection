# L1 — score algebra (deterministic; exact arithmetic)

Setting and notation of `STATEMENT.md` §0-§1. Throughout n ≥ 2, p ≥ 1, λ₀ = 1/(n+1), ν = 0.01 + n/2, columns of X
centred with ‖x_j‖² = n−1, y = y_c/τ̂ with y′y = n−1. For a vector v ∈ R^n and S ⊆ [p] put
q_S(v) := vᵀv − n vᵀX_S H_S^{-1}X_Sᵀv, so that Q_S = q_S(y).

**L1.1 (ridge residual operator).** R_S := I − X_S(G_S + λ₀I)^{-1}X_Sᵀ is symmetric with eigenvalues in (0, 1]; hence
0 ≺ R_S ⪯ I and R_S² ⪯ R_S. For every v: vᵀR_Sv = min_b {‖v − X_Sb‖² + λ₀‖b‖²} ≥ ‖(I − P_S)v‖². If v is centred
then R_Sv is centred. Finally q_S(v) = ‖v‖²/(n+1) + (n/(n+1))·vᵀR_Sv; in particular
(n−1)/(n+1) ≤ Q_S ≤ n−1 and S ⊆ S′ ⇒ Q_{S′} ≤ Q_S.

*Proof.* Write the thin SVD X_S = UDVᵀ. Then X_S(G_S+λ₀I)^{-1}X_Sᵀ = U diag(d_i²/(d_i²+λ₀)) Uᵀ has eigenvalues in
[0, 1), so R_S has eigenvalues in (0, 1]; R_S² ⪯ R_S follows. The minimiser of ‖v − X_Sb‖² + λ₀‖b‖² is
b = (G_S+λ₀I)^{-1}X_Sᵀv and the minimum equals vᵀv − vᵀX_S(G_S+λ₀I)^{-1}X_Sᵀv = vᵀR_Sv; dropping λ₀‖b‖² and
minimising gives the lower bound ‖(I−P_S)v‖². R_Sv = v − X_Sb is a combination of v and centred columns. Since
H_S = (n+1)(G_S + λ₀I), n H_S^{-1} = (n/(n+1))(G_S+λ₀I)^{-1}, so
q_S(v) = vᵀv − (n/(n+1))vᵀ(I − R_S)v = vᵀv/(n+1) + (n/(n+1))vᵀR_Sv. The bounds on Q_S use 0 ⪯ R_S ⪯ I and y′y = n−1;
monotonicity under nesting follows from the variational formula (a larger S enlarges the feasible set). ∎

**L1.2 (one-step identities).** Let t ∉ S and, for λ > 0, a_λ(t|S) := x_tᵀx_t + λ − x_tᵀX_S(G_S+λI)^{-1}X_Sᵀx_t; so
a(t|S) = a_{λ₀}(t|S) = x_tᵀR_Sx_t + λ₀. Then
 (i) det(G_{S∪t} + λI) = det(G_S + λI)·a_λ(t|S), and a_λ(t|S) = λ + min_b{‖x_t − X_Sb‖² + λ‖b‖²} ≥ λ > 0;
 (ii) R_{S∪t} = R_S − R_Sx_tx_tᵀR_S / a(t|S);
 (iii) for every v: vᵀR_Sv − vᵀR_{S∪t}v = g_v(t|S) := (x_tᵀR_Sv)²/a(t|S), and q_S(v) − q_{S∪t}(v) = (n/(n+1))·g_v(t|S);
 (iv) det H_{S∪t}/det H_S = (n+1)·a(t|S) and det(G_{S∪t}+I)/det(G_S+I) = a_1(t|S).
In particular γ(t|S) = g_μ(t|S) = ((n+1)/n)(q_S(μ) − q_{S∪t}(μ)) (the identity quoted in STATEMENT §1).

*Proof.* (i) is the Schur-complement determinant formula for the block matrix
[[G_S+λI, X_Sᵀx_t],[x_tᵀX_S, x_tᵀx_t+λ]]; the variational form is L1.1's computation with (v, λ₀) replaced by
(x_t, λ). (ii): with A = G_S+λ₀I, b = X_Sᵀx_t, s = a(t|S), the block inverse gives
[X_S, x_t]·(G_{S∪t}+λ₀I)^{-1}·[X_S, x_t]ᵀ = X_SA^{-1}X_Sᵀ + s^{-1}(x_t − X_SA^{-1}b)(x_t − X_SA^{-1}b)ᵀ
= (I − R_S) + s^{-1}R_Sx_tx_tᵀR_S. (iii) follows from (ii) and L1.1. (iv): det H_U = (n+1)^{|U|}det(G_U+λ₀I), then
(i) with λ = λ₀ and λ = 1. ∎

**L1.3 (determinant ratio).** D(t|S) := (n+1)·a(t|S)/a_1(t|S) satisfies 1 ≤ D(t|S) ≤ n+1 and D(t|S) ≥ (n+1)a(t|S)/n.

*Proof.* By L1.2(i), λ ↦ a_λ(t|S) is nondecreasing (a minimum of functions nondecreasing in λ, plus λ), so
a(t|S) ≤ a_1(t|S) and D ≤ n+1. Next (n+1)a(t|S) = 1 + min_b{(n+1)‖x_t − X_Sb‖² + ‖b‖²} ≥ 1 + min_b{‖x_t − X_Sb‖² + ‖b‖²}
= a_1(t|S), so D ≥ 1. Taking b = 0, a_1(t|S) ≤ 1 + ‖x_t‖² = n. ∎

**L1.4 (one-step change of F).** Let |S| = k, t ∉ S, k+1 ≤ K. Then
 F(S∪t) − F(S) = −log[(2p−1−k)/(k+1)] − ½ log D(t|S) + ν·log[(0.02 + Q_S)/(0.02 + Q_{S∪t})],
with Q_S − Q_{S∪t} = (n/(n+1))·g_y(t|S) and g_y(t|S) = g_{y_c}(t|S)/τ̂².

*Proof.* w(k+1)/w(k) = C(2p−1,k)/C(2p−1,k+1) = (k+1)/(2p−1−k) (here k+1 ≤ K ≤ p ≤ 2p−1); the determinant terms are
L1.2(iv); the last term is the definition of F with L1.2(iii) for v = y; g is quadratic in v and y = y_c/τ̂. The
constants (log C_n, the prior normaliser) cancel. Both 0.02 + Q's are > 0 by L1.1. ∎

**L1.5 (D-add: a sufficient condition for a strictly improving addition).** Let |S| = k ≤ K−1, t ∉ S. If
 g_y(t|S) ≥ T_n := (1 + 1/n)(2 log(2p−1) + log(n+1)),
then F(S∪t) > F(S).

*Proof.* Put ρ := (n/(n+1))g_y(t|S)/(0.02 + Q_S); then (0.02+Q_{S∪t})/(0.02+Q_S) = 1 − ρ ∈ (0, 1], and
ν log(1/(1−ρ)) ≥ νρ. Since ν > n/2, Q_S ≤ n−1 (L1.1) and g_y ≥ T_n > 0,
νρ > (n/2)·(n/(n+1))·g_y/(n − 0.98) > n g_y/(2(n+1)). By L1.3 and (2p−1−k)/(k+1) ≤ 2p−1, the two penalty terms
are at most log(2p−1) + ½ log(n+1) = n T_n/(2(n+1)). Hence F(S∪t) − F(S) > n(g_y − T_n)/(2(n+1)) ≥ 0. ∎

**L1.5° (D-add, self-normalised form).** Let |S| = k ≤ K−1, t ∉ S, and
ρ̄_n := (2 log(2p−1) + log(n+1))/(n + 0.02) (= (log(2p−1) + ½ log(n+1))/ν). If
 g_{y_c}(t|S) ≥ ρ̄_n·((n+1)/n)·(0.02τ̂² + q_S(y_c)),
then F(S∪t) > F(S). Moreover ρ̄_n(n−1) ≤ T_n.

*Proof.* With ρ as in L1.5, ρ = (n/(n+1))g_{y_c}(t|S)/(0.02τ̂² + q_S(y_c)) ≥ ρ̄_n > 0 (multiply numerator and
denominator by τ̂²), so ν log(1/(1−ρ)) > νρ ≥ νρ̄_n = log(2p−1) + ½ log(n+1), which is at least the sum of the two
penalty terms (L1.3). Finally ρ̄_n(n−1) = T_n·n(n−1)/((n+1)(n+0.02)) ≤ T_n. ∎

**L1.6 (D-del: a necessary condition for a non-improving deletion).** Let |S| = k ≥ 1, j ∈ S, and F(S∖j) ≤ F(S). Then
 g_y(j|S∖j) ≥ ((n+1)/(nν))·(0.02 + Q_S)·[log((2p−k)/k) + ½ log D(j|S∖j)].

*Proof.* L1.4 for (S∖j, j) (sizes k−1 → k): 0 ≤ F(S) − F(S∖j) = −log[(2p−k)/k] − ½ log D(j|S∖j)
+ ν log(1 + (n/(n+1))g_y(j|S∖j)/(0.02 + Q_S)), and log(1+u) ≤ u. ∎

**L1.7 (augmented representation).** Let X̃ := [X; √λ₀·I_p] ∈ R^{(n+p)×p} and ṽ := [v; 0] for v ∈ R^n. Then
X̃_SᵀX̃_S = G_S + λ₀I is invertible; P̃_S := X̃_S(G_S+λ₀I)^{-1}X̃_Sᵀ is the orthogonal projector of R^{n+p} on span X̃_S;
and for u, v ∈ R^n, t ∉ S:
 x_tᵀR_Sv = x̃_tᵀ(I − P̃_S)ṽ,  uᵀR_Sv = ũᵀ(I − P̃_S)ṽ,  a(t|S) = ‖(I − P̃_S)x̃_t‖²,
so g_v(t|S) = (ũ_{S,t}ᵀṽ)² with the unit vector ũ_{S,t} := (I − P̃_S)x̃_t/‖(I − P̃_S)x̃_t‖. Moreover
μ̃ = X̃θ* − b̃ with b̃ := [0; √λ₀θ*], ‖b̃‖ = ‖θ*‖₂/√(n+1).

*Proof.* x̃_j = [x_j; √λ₀e_j], so X̃_SᵀX̃_S = G_S + λ₀I, X̃_Sᵀṽ = X_Sᵀv and, for t ∉ S, X̃_Sᵀx̃_t = X_Sᵀx_t (the lower
blocks e_s, e_t are orthogonal). Hence x̃_tᵀ(I−P̃_S)ṽ = x_tᵀv − x_tᵀX_S(G_S+λ₀I)^{-1}X_Sᵀv = x_tᵀR_Sv, similarly for
ũ, and ‖(I−P̃_S)x̃_t‖² = x_tᵀx_t + λ₀ − x_tᵀX_S(G_S+λ₀I)^{-1}X_Sᵀx_t = a(t|S). Finally X̃θ* = [Xθ*; √λ₀θ*]. ∎
