# L2 — probabilistic events (Model G: ε ~ N_n(0, σ²I), X deterministic)

Tools. (T1) For Z ~ N(0, v²) and r ≥ 0: P(|Z| > r) ≤ 2exp(−r²/(2v²)). (T2) Laurent–Massart (2000, Lemma 1): for
χ²_d and x > 0, P(χ²_d ≥ d + 2√(dx) + 2x) ≤ e^{-x} and P(χ²_d ≤ d − 2√(dx)) ≤ e^{-x}; note
d + 2√(dx) + 2x ≤ (√d + √(2x))². (T3) If A is symmetric with 0 ⪯ A ⪯ I and rank ≤ m, then εᵀAε ≤ εᵀΠε where Π is the
orthogonal projector on range(A); εᵀΠε/σ² ~ χ²_{rank A}, which is stochastically dominated by χ²_m.
Recall y_c = μ + Cε, μ centred, τ̂² = ‖y_c‖²/(n−1), τ_n² = ‖μ‖²/(n−1) + σ², ε̃ = [Cε; 0] ∈ R^{n+p} (L1.7).
Convention: a Gaussian variable with variance 0 is the constant 0, for which every bound below holds trivially (this
covers e.g. μ = 0 when true columns cancel).

**Deterministic witness.** For every S ⊆ [p] with S ⊉ S₀ fix t(S) ∈ S₀∖S, the smallest index maximising γ(·|S) over
S₀∖S. t(S) is a function of (X, θ*) only (not of ε), and γ(t(S)|S)/σ_S² is also the maximum of γ(·|S)/σ_S² (σ_S does
not depend on t).

**E1(q, x) (one-dimensional noise at the witness, uniform over sparse models).** With r_n(q, x) = (2 log(2N_q) + 2x)^{1/2}:
 E1 := { |x_{t(S)}ᵀR_S Cε| ≤ σ·r_n(q,x)·a(t(S)|S)^{1/2} for all S ⊆ [p] with |S| ≤ q, S ⊉ S₀ }, P(E1ᶜ) ≤ e^{-x}.

*Proof.* For t ∉ S, R_Sx_t is centred (L1.1), so x_tᵀR_SCε = (R_Sx_t)ᵀε ~ N(0, σ²x_tᵀR_S²x_t), and
x_tᵀR_S²x_t ≤ x_tᵀR_Sx_t ≤ a(t|S) (L1.1). By (T1) each S fails with probability ≤ 2exp(−r_n²/2) = e^{-x}/N_q, and there
are at most N_q sets S (one Gaussian variable per S, because t(S) is deterministic). ∎

**E4(q, x) (cross term between the unexplained mean and the noise).** Put m_S² := μᵀR_Sμ.
 E4 := { μᵀR_SCε ≤ σ·m_S·r_n(q, x) for all S ⊆ [p] with |S| ≤ q }, P(E4ᶜ) ≤ e^{-x}.

*Proof.* R_Sμ is centred, so μᵀR_SCε = (R_Sμ)ᵀε ~ N(0, σ²μᵀR_S²μ) with μᵀR_S²μ ≤ m_S². By the one-sided bound
P(Z > r) ≤ exp(−r²/(2v²)), each S fails with probability ≤ exp(−r_n²/2) = e^{-x}/(2N_q); sum over ≤ N_q sets. ∎

**E2⁺(x), E2⁻(x) (scale of the standardised response).** With a_x = √(x/(n−1)):
 E2⁺ := {‖Cε‖² ≤ σ²(n−1)(1 + 2a_x + 2a_x²)} ∩ {μᵀε ≤ σ‖μ‖√(2x)}, P((E2⁺)ᶜ) ≤ 2e^{-x}; on E2⁺: τ̂ ≤ τ_n(1 + 2a_x) = τ̄_n(x).
 E2⁻ := {‖Cε‖² ≥ σ²(n−1)(1 − 2a_x)} ∩ {μᵀε ≥ −σ‖μ‖√(2x)}, P((E2⁻)ᶜ) ≤ 2e^{-x}; on E2⁻: τ̂² ≥ τ_n²(1 − 4a_x).

*Proof.* (n−1)τ̂² = ‖μ‖² + 2μᵀε + ‖Cε‖² (μᵀC = μᵀ). ‖Cε‖²/σ² ~ χ²_{n−1} and μᵀε ~ N(0, σ²‖μ‖²). By AM–GM,
2σ‖μ‖ ≤ √(n−1)·(σ² + ‖μ‖²/(n−1)) = √(n−1)τ_n², and σ² ≤ τ_n².
Upper: on E2⁺ (probability ≥ 1 − 2e^{-x} by (T2), since σ²(n−1)(1 + 2a_x + 2a_x²) = σ²(n−1 + 2√((n−1)x) + 2x), and
the one-sided Gaussian bound P(Z > r) ≤ e^{−r²/(2v²)}),
 (n−1)τ̂² ≤ (n−1)τ_n² + τ_n²√(n−1)√(2x) + 2τ_n²√((n−1)x) + 2τ_n²x,
i.e. τ̂² ≤ τ_n²(1 + (2+√2)a + 2a²) ≤ τ_n²(1 + 2a)² with a = √(x/(n−1)).
Lower: on E2⁻ (probability ≥ 1 − 2e^{-x}),
 (n−1)τ̂² ≥ (n−1)τ_n² − τ_n²√(n−1)√(2x) − 2τ_n²√((n−1)x), i.e. τ̂² ≥ τ_n²(1 − (2+√2)a) ≥ τ_n²(1 − 4a). ∎

**E2ᶜʰⁱ(x) (noise energy from below).** { ‖Cε‖² ≥ σ²(n−1 − 2√((n−1)x)) }, failure probability ≤ e^{-x} (T2).

**E3a(q, x) (noise captured by sparse models).** For 1 ≤ k ≤ q put U(k, x) := (√k + √(2 log C(p,k) + 2x))².
 E3a := { ‖P̃_Sε̃‖² ≤ σ²U(|S|, x) and ‖P_Sε‖² ≤ σ²U(|S|, x) for all S with 1 ≤ |S| ≤ q }, P(E3aᶜ) ≤ 2q·e^{-x}.

*Proof.* Let B ∈ R^{(n+p)×k} be an orthonormal basis of span X̃_S (dimension k by L1.7) with top block B₁ ∈ R^{n×k}.
‖P̃_Sε̃‖² = ‖B₁ᵀCε‖² = εᵀAε with A = CB₁B₁ᵀC, 0 ⪯ A ⪯ I (B₁ᵀB₁ ⪯ BᵀB = I), rank A ≤ k. By (T3), (T2):
P(‖P̃_Sε̃‖² > σ²(√k + √(2x′))²) ≤ e^{-x′}; take x′ = log C(p,k) + x and sum over the C(p,k) sets of size k and over
k ≤ q: ≤ q e^{-x}. The same argument with A = P_S (rank ≤ k) gives the statement for ‖P_Sε‖². ∎

**E3b(q, x′) (noise captured by the excess directions).** Let x′ > 0. (If q − s₀ < 1 the event is the whole space.)
For E ⊆ [p]∖S₀ with |E| = m ≥ 1 let
W(E) := span X̃_{S₀∪E} ⊖ span X̃_{S₀} (dimension m) and U′(m, x′) := (√m + √(2 log C(p−s₀, m) + 2x′m))².
 E3b := { ‖P_{W(E)}ε̃‖² ≤ σ²U′(|E|, x′) for all E ⊆ [p]∖S₀ with 1 ≤ |E| ≤ q − s₀ }, P(E3bᶜ) ≤ e^{-x′}/(1 − e^{-x′}).

*Proof.* As for E3a with the m-dimensional subspace W(E): each E fails with probability
≤ exp(−log C(p−s₀, m) − x′m); sum over E and m ≥ 1: ≤ Σ_{m≥1}e^{-x′m}. ∎
