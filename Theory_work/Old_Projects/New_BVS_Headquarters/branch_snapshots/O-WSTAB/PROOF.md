# O-WSTAB — PROOF.md: start-to-posterior divergence, weight stability and the regime dichotomy

Branch `theory/O-WSTAB`. Every result is a **candidate** (not reviewed, not adopted). Status words follow
`theory_campaign/PROTOCOL.md`. Notation follows `Docs/Theory/theorems/00_COMMON.md`; new symbols are defined where
introduced. "[E]" is W1-EXP (`origin/theory/W1-EXP`, `theory_campaign/W1-EXP/PROOF.md`); "[P]" is W2-PREM.

Contents
- §0 Setting, the fit-fraction form of the score, the cumulant function Λ
- §1 WS1 Exponential-family identities for the bridge (PROVED)
- §2 WS2 One importance step: ESS, evidence variance, PW2 at the first stage (PROVED)
- §3 WS3 The block-orthogonal case: exact relation between π₀ and π (PROVED)
- §4 WS4 Perturbation in the standardised cross-block Gram (PROVED)
- §5 WS5 Leakage decomposition and the regime dichotomy (deterministic parts PROVED; favourable conclusion by composition)
- §6 WS6 Weights in the favourable regime; the noise-chasing obstruction (PROVED lower bound; upper bound CONJECTURE)
- §7 WS7 Weights in the masked regime; why the sampler must move (PROVED)
- §8 The whole bridge and T25(iv)/PW2

---

## §0 Setting

Data, model space Ω = {S ⊆ [p] : |S| ≤ K}, scores m(S), BF(S) = m(S)/m(∅), prior ϖ, posterior π: 00_COMMON §1.
Blocks C₁,…,C_J: **any** partition of [p] (the v3 partition is a special case; no statement below uses how it is
built). Tables r_b(U) = BF(U), U ⊆ C_b. Start γ₀(S) = ϖ(S)∏_b r_b(S∩C_b), π₀ = γ₀/Z̄₀; discrepancy
d(S) = log BF(S) − Σ_b log r_b(S∩C_b); bridge γ_φ = γ₀e^{φd}, Z̄_φ = Σ_Ω γ_φ, q_φ = γ_φ/Z̄_φ for **every real φ**
(q₀ = π₀, q₁ = π). EX-A throughout. As in T13 (locked), γ₀ > 0 and d is finite on Ω, so every q_φ has full
support on Ω.

**New notation.**
- Q̄ := 2b₀ + yᵀy (= n − 1 + 0.02 on the standardised scale); t_S := n z_SᵀH_S⁻¹z_S (so Q_S = yᵀy − t_S);
  **fit fraction** x_S := t_S/Q̄; block fit fractions x_b(S) := x_{S∩C_b}; x̄_S := Σ_b x_b(S).
- Λ(φ) := log(Z̄_φ/Z̄₀) = log E_{π₀}[e^{φd}], φ ∈ ℝ (the cumulant function of d under π₀).
- For A ⊆ Ω nonempty: q_φ(A) = Z̄_φ(A)/Z̄_φ, q_φ^A = q_φ(·|A), osc_A(d) := max_A d − min_A d.
- χ²(μ‖λ) = Σλ(μ/λ)² − 1; KL(μ‖λ) = Σμ log(μ/λ); TV(μ, λ) = ½Σ|μ − λ|; Rényi
  D_α(μ‖λ) = (α−1)⁻¹ log Σμ^αλ^{1−α} (α > 0, α ≠ 1).

**Lemma 0 (fit-fraction form).** For every S ⊆ [p]: 0 ≤ x_S < 1 and
 log BF(S) = −½ log D_S − ν log(1 − x_S).

*Proof.* 2b₀ + Q_S = Q̄ − t_S and Q_∅ = yᵀy, so m(S)/m(∅) = D_S^{−1/2}[(Q̄ − t_S)/Q̄]^{−ν} = D_S^{−1/2}(1 − x_S)^{−ν}.
H_S ≻ 0 gives t_S ≥ 0. By Woodbury Q_S = yᵀ(I + nX_S(G_S + I)⁻¹X_Sᵀ)⁻¹y > 0 because yᵀy = n − 1 > 0, so t_S < yᵀy < Q̄. ∎

**Lemma Λ.** Λ is real-analytic and convex on ℝ, Λ(0) = 0, Λ'(φ) = E_{q_φ}[d], Λ''(φ) = Var_{q_φ}(d).
*Proof.* Λ is the log of a finite sum of exponentials of φ; differentiate. ∎

---

## §1 WS1 — exponential-family identities (PROVED)

**Theorem WS1.** For all real u, v, with Δ := v − u and w := 2v − u:

(a) **Singleton identity.** 1 + χ²(q_v‖q_u) = exp{Λ(w) − 2Λ(v) + Λ(u)} = q_v(S)² / (q_u(S) q_w(S)) for **every** S ∈ Ω.

(a′) **Rényi version.** For every real α and every S ∈ Ω,
 Σ_Ω q_v^α q_u^{1−α} = exp{Λ(u+αΔ) − αΛ(v) − (1−α)Λ(u)} = q_v(S)^α q_u(S)^{1−α} / q_{u+αΔ}(S).

(b) **Set bounds.** For ∅ ≠ A ⊊ Ω,
 q_v(A)²/q_u(A) + q_v(Aᶜ)²/q_u(Aᶜ) ≤ 1 + χ²(q_v‖q_u) ≤ cosh²(|Δ| osc_A(d)/2) · q_v(A)²/(q_u(A) q_w(A)).
(The upper bound also holds for A = Ω.)

(c) **Variance representation.** KL(q_v‖q_u) = ∫ |t − u| Λ''(t) dt over the segment between u and v, and
 log(1 + χ²(q_v‖q_u)) = ∫_{v−|Δ|}^{v+|Δ|} (|Δ| − |t − v|) Λ''(t) dt.
Hence KL(q_v‖q_u) ≤ (Δ²/2) sup_{t between u,v} Var_{q_t}(d) and log(1+χ²(q_v‖q_u)) ≤ Δ² sup_{t between u,w} Var_{q_t}(d).

(d) **TV.** For every S ∈ Ω: TV(q_u, q_v) ≤ max{1 − q_u(S), 1 − q_v(S)}; and TV(q_u, q_v) ≥ |q_v(A) − q_u(A)| for every A.

(e) **Log-concavity in the temperature.** For every S ∈ Ω, φ ↦ log q_φ(S) is concave on ℝ. Hence
q_φ(S) ≥ min{q_a(S), q_b(S)} for φ ∈ [a, b], and sup_{φ,φ'∈[0,1]} TV(q_φ, q_φ') ≤ max{1 − π₀(S), 1 − π(S)}.
(For S = S₀ the first claim on [0,1] is locked T22(iv-b); here it is extended to every S and every interval.)

*Proof.* (a) Σ_S q_v(S)²/q_u(S) = Σ_S γ₀(S)e^{(2v−u)d(S)} Z̄_u/Z̄_v² = Z̄_wZ̄_u/Z̄_v². For any S,
q_v(S)²/(q_u(S)q_w(S)) = [γ₀(S)²e^{2vd(S)}/Z̄_v²]·[Z̄_uZ̄_w/(γ₀(S)²e^{(u+w)d(S)})] = Z̄_uZ̄_w/Z̄_v² because u + w = 2v.
Dividing by Z̄₀² gives the Λ form.
(a′) Identical, with exponent αv + (1−α)u = u + αΔ.
(b) Lower bound: by Cauchy–Schwarz, (Σ_A q_v)² ≤ (Σ_A q_v²/q_u)(Σ_A q_u), and the same on Aᶜ; add.
Upper bound: Z̄_uZ̄_w/Z̄_v² = [Z̄_u(A)Z̄_w(A)/Z̄_v(A)²]·[q_v(A)²/(q_u(A)q_w(A))] since q_φ(A) = Z̄_φ(A)/Z̄_φ.
With Y := e^{Δd} and expectation under q_u^A: E Y = Z̄_v(A)/Z̄_u(A), E Y² = Z̄_w(A)/Z̄_u(A), so the first factor is
E Y²/(E Y)². On A, Y ∈ [m, M] with M/m = e^{|Δ| osc_A(d)}. Kantorovich: (M − Y)(Y − m) ≥ 0 gives
E Y² ≤ (m+M)E Y − mM, and (m+M)E Y − mM ≤ (m+M)²(E Y)²/(4mM) because the difference is
((m+M)E Y − 2mM)²/(4mM) ≥ 0. Finally (m+M)²/(4mM) = cosh²(½ log(M/m)).
(c) KL(q_v‖q_u) = Σ q_v[(v−u)d − Λ(v) + Λ(u)] = ΔΛ'(v) − Λ(v) + Λ(u); Taylor's formula with integral remainder
for Λ around v evaluated at u gives Λ(u) = Λ(v) − ΔΛ'(v) + ∫_v^u (u − t)Λ''(t)dt, and ∫_v^u (u−t)Λ''dt is the stated
integral (both orientations). The second difference identity f(v+h) − 2f(v) + f(v−h) = ∫_{−h}^{h}(h − |s|)f''(v+s)ds
with h = |Δ| gives the χ² form; ∫_{−h}^{h}(h − |s|)ds = h² and the KL kernel integrates to Δ²/2.
(d) TV = ½Σ|q_u − q_v| ≤ ½[|q_u(S) − q_v(S)| + q_u(Sᶜ) + q_v(Sᶜ)] = max(a, b) with a = 1 − q_u(S), b = 1 − q_v(S),
since |q_u(S) − q_v(S)| = |a − b| and ½(|a − b| + a + b) = max(a, b). The lower bound is TV = sup_A |q_v(A) − q_u(A)|.
(e) log q_φ(S) = log γ₀(S) + φd(S) − log Z̄₀ − Λ(φ) is linear minus convex. A concave function on [a,b] is at
least the minimum of its endpoint values. The TV claim follows from (d) with the fixed S. ∎

**Remark (relation to locked T13).** (a) is locked T13(i) with V = {S} (then ρ_V ≡ 1); (b)'s upper bound is
T13(i)+(iii) with V = A, plus Kantorovich. The point of (a) is that it holds *for every S simultaneously*: the
bridge's χ² is controlled exactly when one model dominates q_u, q_v **and the over-tempered law q_w**.

---

## §2 WS2 — one importance step (PROVED)

**Theorem WS2.** Fix real u < v, Δ = v − u, w = 2v − u, g := e^{Δd}/E_{q_u}e^{Δd} = dq_v/dq_u. Let S₁,…,S_N be iid q_u.
(a) (1/N)Σg(S_i) has mean 1 and variance χ²(q_v‖q_u)/N.
(b) ESS_N/N := (Σg(S_i))²/(NΣg(S_i)²) → ESS_∞ := 1/(1 + χ²(q_v‖q_u)) almost surely as N → ∞.
(c) **ESS sandwich.** ESS_∞ = q_u(S)q_w(S)/q_v(S)² for every S ∈ Ω, and ESS_∞ ≤ q_u(A)/q_v(A)² for every A.
For the start-to-target step (u, v) = (0, 1):
 π₀(S)·q₂(S)/π(S)² = ESS_∞(π₀ → π) ≤ π₀(S)/π(S)²  for every S, in particular S = S₀.
(d) **PW2 at the first stage.** In a final island of the v3 run (iid exact π₀ start, W₀ = 1; setting of locked
T25(iv)), PW2 holds at t = 1 **with equality** for a₁ = χ²(q_{φ₁}‖π₀) and ν₁ = 0:
E_c[(q̂₀g₁)² − 1] = χ²(q_{φ₁}‖π₀)/N. If the frozen grid has T = 1 (φ₁ = 1), Var_c(Ẑ_r/Z) = χ²(π‖π₀)/N exactly
and Var_c(Ẑ/Z) = χ²(π‖π₀)/(4N).

*Proof.* (a) E_{q_u}g = 1 and E_{q_u}g² = Σq_v²/q_u = 1 + χ². (b) Strong law for the numerator and denominator.
(c) WS1(a) and WS1(b) (lower bound with A, dropping the Aᶜ term). (d) q̂₀ is the empirical law of N iid π₀ draws
and g₁ = dq_{φ₁}/dπ₀, so the expectation is Var(q̂₀g₁) = Var_{π₀}(g₁)/N; with T = 1, Ẑ_{r,1}/Z₁ = W₁ = q̂₀(g₁)
(T25(iv)'s definitions) and islands are iid given c (CAL, EX-S). ∎

---

## §3 WS3 — the block-orthogonal case (PROVED)

**BO** (00_COMMON): X_{C_b}ᵀX_{C_c} = 0 for b ≠ c.

**Theorem WS3.** Assume BO. For every S ∈ Ω (write S_b = S ∩ C_b):
(a) D_S = ∏_b D_{S_b}, t_S = Σ_b t_{S_b}, hence x_S = x̄_S < 1.
(b) **d is pure noise-variance sharing:** d(S) = d_σ(S) := ν[Σ_b log(1 − x_b(S)) − log(1 − x̄_S)].
(c) 0 ≤ d_σ(S) ≤ ν Σ_{b<c} x_b(S)x_c(S)/(1 − x̄_S); d_σ is nondecreasing in each x_b; d_σ(S) = 0 iff at most one
block has x_b(S) > 0.
(d) **Mean-field representation.** Let λ be the Gamma law with shape ν and rate Q̄/2 for the precision τ = 1/σ²
(the posterior of τ under the null model ∅ in the working model), and f_b(U; τ) := D_U^{−1/2} exp(τ t_U/2). Then
 BF(S) = E_λ[∏_b f_b(S_b; τ)],  r_b(U) = E_λ[f_b(U; τ)].
So π(S) ∝ ϖ(S)E_λ∏_b f_b(S_b; τ) while π₀(S) ∝ ϖ(S)∏_b E_λ f_b(S_b; τ): **π₀ is π with the single shared noise
precision replaced by an independent copy per block.** In the fixed-variance version of the model (τ known,
tables built the same way) d ≡ 0 and π₀ = π exactly.
(e) The size prior (BB(1,p), cap K) enters π₀ and π identically; π(S)/π₀(S) = e^{d_σ(S)}/E_{π₀}e^{d_σ}. So the
BB(1,p) coupling across blocks produces **no** discrepancy; all of it is the noise-sharing term d_σ.
(f) For T ⊆ C_b, l ∈ C_b ∖ T: δ_{T,l} = u_{T,l}ᵀμ_b with μ_b := X_{S₀∩C_b}θ_{S₀∩C_b}: no out-of-block signal leaks
into any table comparison.

*Proof.* (a) After a column permutation (which leaves determinants and quadratic forms unchanged), G_S, H_S and
G_S + I are block diagonal with blocks indexed by b; determinants multiply and zᵀH⁻¹z splits. Lemma 0 gives x_S < 1.
(b) Lemma 0 for S and each S_b, with (a).
(c) Let g(x) = −log(1 − x). Order the blocks with x_b > 0 as 1,…,m and put s_k = x₁ + … + x_k (s_m = x̄ < 1). Then
d_σ/ν = g(s_m) − Σ_k g(x_k) = Σ_{k=2}^m [g(s_k) − g(s_{k−1}) − g(x_k)] and
g(s_k) − g(s_{k−1}) − g(x_k) = log[(1 − s_{k−1})(1 − x_k)/(1 − s_k)] = log(1 + s_{k−1}x_k/(1 − s_k)) ∈ (0, s_{k−1}x_k/(1 − x̄)].
Summing gives 0 ≤ d_σ ≤ νΣ_{b<c}x_bx_c/(1 − x̄), with strict positivity as soon as m ≥ 2. Monotonicity:
∂d_σ/∂x_b = ν[1/(1 − x̄) − 1/(1 − x_b)] ≥ 0 because x̄ ≥ x_b.
(d) For t < Q̄, E_λ e^{τt/2} = (1 − t/Q̄)^{−ν} (Gamma moment generating function). So
E_λ∏_b f_b(S_b; τ) = ∏_b D_{S_b}^{−1/2}(1 − Σ_b t_{S_b}/Q̄)^{−ν} = D_S^{−1/2}(1 − x_S)^{−ν} = BF(S) by (a) and Lemma 0; the
case of one block gives r_b. That λ is the null-model posterior of τ: in the working model, m(∅ | τ) ∝ τ^{n/2}e^{−τyᵀy/2},
prior τ ~ Gamma(a₀, b₀), so the posterior is Gamma(a₀ + n/2, b₀ + yᵀy/2) = Gamma(ν, Q̄/2). With τ known,
BF(S | τ) = ∏_b f_b(S_b; τ) and r_b(U | τ) = f_b(U; τ), so the product of tables equals BF.
(e) ϖ(S) appears as a common factor in γ₀ and in ϖ·m; the cap K is the same state space Ω.
(f) u_{T,l} ∈ span(X_{C_b}) and X_{C_b}ᵀμ_{−b} = 0 under BO, where μ_{−b} = μ − μ_b is a combination of other blocks'
columns. ∎

**Remark (FKG view).** All f_b(·; τ) are increasing in τ, so d ≥ 0 is the Harris–FKG inequality
E∏f_b ≥ ∏E f_b. Under BO the start always **under-rewards** models that fit in several blocks: each table measures its
block's fit against a residual that still contains the other blocks' signal.

**Remark (scale).** For a model fitting several blocks, d_σ is of order n: with block R²'s x_b, d_σ ≈ (n/2)Σ_{b<c}x_bx_c/(1 − x̄).
This does **not** make π₀ far from π — d enters only through its *variation* over the region that carries mass
(WS1(c)). Near S₀ (adding a null l in a truth-free block) the increment is d_σ(S₀+l) − d_σ(S₀) ≈ ω Z_l²/2 with
ω := 1 − RSS_{S₀}/yᵀy (computed exactly in §6): bounded in n, but *unbounded over the p nulls*.

---

## §4 WS4 — perturbation in the standardised cross-block Gram (PROVED)

**Definitions.** For S ∈ Ω with |S| ≥ 2: R_S = G_S/(n − 1); A_S := the block-diagonal part of R_S (entries (j,k) with
j, k in the same block; zero otherwise); E_S := R_S − A_S (the cross-block Gram). Assume A_S ≻ 0 (implied by
SE-blk(φ₀): λ_min(R_{C_b}) ≥ φ₀² for every b, by interlacing). The **cross-block dependence measures**
 ε_S := ‖A_S^{−1/2}E_SA_S^{−1/2}‖_op,  F_S := ‖A_S^{−1/2}E_SA_S^{−1/2}‖_F² ≤ |S|ε_S².
(For |S| ≤ 1 put ε_S = F_S = 0.) Sufficient: ε_S ≤ ‖E_S‖_op/φ₀² ≤ |S| max_{cross pairs}|r_jk|/φ₀².
Decomposition (from Lemma 0, any X): d = d_det + d_fit + d_σ with
 d_det(S) := −½[log D_S − Σ_b log D_{S_b}],  d_fit(S) := −ν log[(1 − x_S)/(1 − x̄_S)],  d_σ as in WS3(b)
(d_σ and d_fit are defined when x̄_S < 1).

**Theorem WS4.** Let S ∈ Ω with A_S ≻ 0 and ε := ε_S < 1. Then
(a) (1 − ε)A_S ⪯ R_S ⪯ (1 + ε)A_S; in particular λ_min(R_S) ≥ (1 − ε) min_b λ_min(R_{S_b}) (global SE on S from
SE-blk plus weak cross-block dependence).
(b) |t_S − Σ_b t_{S_b}| ≤ (ε/(1 − ε)) Σ_b t_{S_b}, i.e. |x_S − x̄_S| ≤ ε x̄_S/(1 − ε).
(c) |d_det(S)| ≤ F_S/(4(1 − ε)).
(d) If x̄_S < 1 − ε: |d_fit(S)| ≤ ν ε x̄_S/(1 − ε − x̄_S), hence
 |d(S) − d_σ(S)| ≤ η_S := ν ε x̄_S/(1 − ε − x̄_S) + F_S/(4(1 − ε)).
(e) **Transfer.** Let W ⊆ Ω be nonempty with (a)–(d) applicable on W and η_W := max_W η_S. Let q^σ_φ ∝ γ₀e^{φd_σ} be the
*BO-equivalent bridge* (same start, discrepancy d_σ). Then for every real v,
 e^{−4|v|η_W} ≤ [1 + χ²(q_v^W ‖ π₀^W)] / [1 + χ²(q_v^{σ,W} ‖ π₀^W)] ≤ e^{4|v|η_W},  TV(q_v^W, q_v^{σ,W}) ≤ 1 − e^{−2|v|η_W}.
With W = Ω this compares (π₀, π) with (π₀, π^σ) globally; for W ⊊ Ω combine with WS1(b).

*Proof.* (a) ‖A^{−1/2}EA^{−1/2}‖ ≤ ε ⇔ −εI ⪯ A^{−1/2}EA^{−1/2} ⪯ εI ⇔ −εA ⪯ E ⪯ εA; add A.
(b) Let c₁ := (n+1)(n−1). H_S = H_d + c₁E with H_d := c₁A + I = blockdiag(H_{S_b}). From −εA ⪯ E ⪯ εA and
c₁A ⪯ H_d: −εH_d ⪯ c₁E ⪯ εH_d, so M_H := H_d^{−1/2}c₁EH_d^{−1/2} has ‖M_H‖ ≤ ε. Then
H_S⁻¹ = H_d^{−1/2}(I + M_H)⁻¹H_d^{−1/2}; with c := H_d^{−1/2}z_S, zᵀH_S⁻¹z − zᵀH_d⁻¹z = cᵀ[(I+M_H)⁻¹ − I]c, and the eigenvalues
of (I + M_H)⁻¹ − I lie in [−ε/(1+ε), ε/(1−ε)]. Since cᵀc = Σ_b z_{S_b}ᵀH_{S_b}⁻¹z_{S_b}, multiply by n.
(c) log D_S = log det H_S − log det(G_S + I). As in (b), log det H_S = log det H_d + log det(I + M_H) and
log det(G_S + I) = log det(G_d + I) + log det(I + M_G), G_d + I := (n−1)A + I, M_G := (G_d+I)^{−1/2}(n−1)E(G_d+I)^{−1/2},
‖M_G‖ ≤ ε. Also Σ_b log D_{S_b} = log det H_d − log det(G_d + I). So log D_S − Σ_b log D_{S_b} =
log det(I + M_H) − log det(I + M_G). Both M's are symmetric with zero diagonal blocks (block-diagonal conjugation of E),
hence trace zero. For |μ| ≤ ε < 1: μ − μ²/(2(1−ε)) ≤ log(1+μ) ≤ μ (series for μ < 0; log(1+μ) ≥ μ − μ²/2 for μ ≥ 0).
Summing over eigenvalues with Σμ_i = 0: −‖M‖_F²/(2(1−ε)) ≤ log det(I + M) ≤ 0. Finally ‖M_H‖_F², ‖M_G‖_F² ≤ F_S by
**Lemma (Frobenius monotonicity):** for symmetric E and 0 ⪯ X ⪯ Y, tr(EXEX) ≤ tr(EYEY). [Proof:
tr(EYEY) − tr(EXEX) = tr((Y − X)EYE) + tr(EXE(Y − X)), each a trace of a product of two PSD matrices, hence ≥ 0.]
Apply with X = H_d⁻¹ (resp. (G_d+I)⁻¹), Y = (c₁A)⁻¹ (resp. ((n−1)A)⁻¹) and E scaled accordingly:
‖M_H‖_F² = tr(c₁E H_d⁻¹ c₁E H_d⁻¹) ≤ tr(c₁E(c₁A)⁻¹c₁E(c₁A)⁻¹) = tr(EA⁻¹EA⁻¹) = F_S. So
d_det = −½ log det(I + M_H) + ½ log det(I + M_G) ∈ [−F_S/(4(1−ε)), F_S/(4(1−ε))].
(d) With h := (x_S − x̄_S)/(1 − x̄_S), (b) gives |h| ≤ h₀ := εx̄/((1−ε)(1−x̄)), and h₀ < 1 ⇔ x̄ < 1 − ε. If h ≥ 0,
0 ≤ −log(1 − h) ≤ h/(1−h) ≤ h₀/(1−h₀); if h < 0, 0 ≤ log(1 + |h|) ≤ |h| ≤ h₀. And h₀/(1 − h₀) = εx̄/(1 − ε − x̄).
(e) Put e := d − d_σ, |e| ≤ η on W. Λ_W(φ) := log E_{π₀^W}e^{φd} and Λ^σ_W likewise satisfy |Λ_W(φ) − Λ^σ_W(φ)| ≤ |φ|η.
By WS1(a) on the bridge restricted to W (which is the same exponential family with γ₀ replaced by γ₀1_W),
log(1 + χ²(q_v^W‖π₀^W)) = Λ_W(2v) − 2Λ_W(v), and the same for σ; the difference is at most 2|v|η + 2|v|η.
For TV: dq_v^W/dq_v^{σ,W} = e^{ve}/E_{q_v^{σ,W}}e^{ve} ≥ e^{−2|v|η}, and TV(P, P') = Σ(P' − P)_+ ≤ 1 − inf dP/dP'. ∎

**Scale of the perturbation regime (important).** η_S ≈ (n/2)ε_S x̄_S/(1 − x̄_S). For a model explaining a fixed
fraction of yᵀy this is o(1) only when **ε_S = o(1/n)**. Sample cross-correlations of unrelated columns are of order
n^{−1/2}, so the uniform perturbation route covers only near-orthogonal designs ("near-BO" benchmarks). The relevant
weak-dependence notion at the n^{−1/2} scale is the leakage of §5, which acts on log-odds through δ²/(2v) = O(1).

---

## §5 WS5 — leakage decomposition and the regime dichotomy

**Truth-dependent cross-block quantities** (deterministic given X and θ*; 00_COMMON μ = Xθ*). For each block b:
U*_b := S₀ ∩ C_b; μ_b := X_{U*_b}θ*_{U*_b}; μ_{−b} := μ − μ_b = X_{S₀∖C_b}θ*_{S₀∖C_b}; and
- **cross-block coefficient shift** α_b := G_{U*_b}⁻¹X_{U*_b}ᵀμ_{−b} ∈ ℝ^{U*_b} (the regression of the out-of-block signal on
  the block's own truths; empty if U*_b = ∅);
- **effective block coefficient** θ̃_b := θ*_{U*_b} + α_b;
- **leakage remainder** Λ_b := ‖(P_{C_b} − P_{U*_b})μ_{−b}‖² (= [E]'s λ_b(S₀));
- total visible leakage κ_b := ‖P_{C_b}μ_{−b}‖² = Λ_b + ‖X_{U*_b}α_b‖².
Under BO: α_b = 0, θ̃_b = θ*_{U*_b}, Λ_b = κ_b = 0.

**Lemma WS5.1.** P_{C_b}μ = X_{U*_b}θ̃_b + ρ_b with ρ_b := (P_{C_b} − P_{U*_b})μ_{−b} ⊥ span(X_{U*_b}), ρ_b ∈ span(X_{C_b}),
‖ρ_b‖² = Λ_b.
*Proof.* P_{C_b}μ = μ_b + P_{U*_b}μ_{−b} + (P_{C_b} − P_{U*_b})μ_{−b}, P_{U*_b}μ_{−b} = X_{U*_b}α_b, and P_{C_b} − P_{U*_b} is the projection
onto span(X_{C_b}) ⊖ span(X_{U*_b}) (U*_b ⊆ C_b). ∎

**Proposition WS5.2 (leakage formulas; PROVED).** Assume SE-blk(φ₀). For b, T ⊆ C_b, l ∈ C_b ∖ T:
(a) δ_{T,l} = u_{T,l}ᵀ(I − P_T)X_{U*_b∖T}θ̃_{b,U*_b∖T} + u_{T,l}ᵀρ_b.
(b) *Null comparisons* (l ∉ S₀, U*_b ⊆ T): δ_{T,l} = u_{T,l}ᵀρ_b and |δ_{T,l}| ≤ √Λ_b. **NL quantities of T22(iii) are pure
cross-block leakage.** In particular NL_η holds if CBL(η): max_b Λ_b ≤ ησ*² log n.
(c) *Block-completing truth addition* (l ∈ U*_b, T = U*_b ∖ {l}): δ_{T,l} = θ̃_{b,l}‖(I − P_T)x_l‖ **exactly**, and
‖(I − P_T)x_l‖ ≥ φ₀√(n−1).
(d) *Visibility*: for T ⊆ C_b with U*_b ⊄ T, ‖(P_{T∪U*_b} − P_T)μ‖ ≥ φ₀√(n−1)‖θ̃_{b,U*_b∖T}‖ − √Λ_b. Hence VIS (with
M_n^V = M_n) holds if
 EBM(M_n): min_{b, j∈U*_b} |θ̃_{b,j}| ≥ [√(M_n(σ*² + 2M) log n) + √Λ_b] / (φ₀√(n−1)), M_n → ∞.
(e) With c_b := max_{j∈C_b, k∈S₀∖C_b}|r_jk|: κ_b ≤ (n−1)|C_b| c_b² ‖θ*_{S₀∖C_b}‖₁²/φ₀² and
‖α_b‖₂ ≤ √|U*_b| c_b ‖θ*_{S₀∖C_b}‖₁/φ₀².

*Proof.* (a) u := u_{T,l} ∈ span(X_{T∪{l}}) ⊆ span(X_{C_b}), so uᵀμ = uᵀP_{C_b}μ = uᵀ(X_{U*}θ̃ + ρ) (Lemma WS5.1). As u ⊥ span(X_T),
uᵀX_{U*}θ̃ = uᵀ(I − P_T)X_{U*}θ̃ = uᵀ(I − P_T)X_{U*∖T}θ̃_{U*∖T}.
(b) U* ⊆ T makes the first term vanish; Cauchy–Schwarz.
(c) T ∪ {l} = U*, so u ∈ span(X_{U*}) ⊥ ρ; the first term is θ̃_l uᵀ(I − P_T)x_l = θ̃_l‖(I − P_T)x_l‖.
‖(I − P_T)x_l‖² = (n−1)/[(R_{U*}⁻¹)_{ll}] ≥ (n−1)λ_min(R_{U*}) ≥ (n−1)φ₀² by interlacing within C_b.
(d) T ∪ U* ⊆ C_b, so (P_{T∪U*} − P_T)μ = (P_{T∪U*} − P_T)(X_{U*}θ̃ + ρ). X_{U*}θ̃ ∈ span(X_{T∪U*}) gives
(P_{T∪U*} − P_T)X_{U*}θ̃ = (I − P_T)X_{U*∖T}θ̃_{U*∖T}, whose squared norm is θ̃ᵀ[X_{U*∖T}ᵀ(I − P_T)X_{U*∖T}]θ̃ ≥
(n−1)λ_min(R_{T∪U*})‖θ̃_{U*∖T}‖² ≥ (n−1)φ₀²‖θ̃_{U*∖T}‖² (Schur complement). The second term has norm ≤ ‖ρ‖. For VIS note
v_T = σ*² + Δ_T ≤ σ*² + ‖μ‖²/(n−1) ≤ σ*² + 2M (R: ‖μ‖² ≤ Mn, n ≥ 2), and ‖θ̃_{U*∖T}‖ ≥ min_j|θ̃_j|.
(e) κ_b = wᵀG_{C_b}⁻¹w with w := X_{C_b}ᵀμ_{−b} = (n−1)R_{C_b,S₀∖C_b}θ*_{S₀∖C_b}, ‖w‖ ≤ (n−1)√|C_b| c_b‖θ*_{S₀∖C_b}‖₁ and
G_{C_b}⁻¹ ⪯ ((n−1)φ₀²)⁻¹I. Likewise α_b = R_{U*U*}⁻¹R_{U*,S₀∖C_b}θ*_{S₀∖C_b}. ∎

**Theorem WS5.3 (regime dichotomy in cross-block terms).**

(F) *Weak leakage ⇒ favourable start.* Assume G, R (with A, M, φ₀), SE-blk(φ₀), EBM(M_n), and CBL(η) with
0 ≤ η < η_A := (√(2A+1) − √(2A))². Then VIS and NL_η hold deterministically (WS5.2(b),(d)); EXP′ holds by [E] Thm 1
(candidate); NL_avg(κ) is supplied by NL_η for every 0 < κ < ½ − η/2 − √(2Aη) (κ = ½ if η = 0), as stated in
locked T22(iii). Hence, by locked T22(iii),
 1 − π₀(S₀) = O_{P₀}(2^B √(log n) n^{−κ}).
Under BO, α ≡ 0 and Λ ≡ 0, so EBM reduces to a block beta-min and η = 0 ([E] Thm 2).
**Status:** the reduction (VIS, NL_η ⇐ EBM, CBL) is **PROVED**; the conclusion is a direct composition with locked
T22(iii) and inherits the candidate status of [E] Thm 1.

(M) *Masking needs order-one cross-block cancellation.* Let S^{(0)} ⊂ … ⊂ S^{(c)} = S₀ be any chain of single
additions (T27's H1), c ≥ 1, T_i := S^{(i)} ∩ C_{b(l_i)}. For every block b that receives an addition, the **last**
addition l in b has T = U*_b ∖ {l}, so (WS5.2(c))
 |δ_{T,l}| = |θ*_l + α_{b,l}| · ‖(I − P_T)x_l‖ ≥ φ₀√(n−1) |θ*_l + α_{b,l}|.
Hence [E]'s chain-leakage condition CL(L) (which yields T27(i)'s masking law, [E] Thms 3–4) forces
 |θ*_l + α_{b,l}| ≤ Lσ*/(φ₀√(n−1)):
the out-of-block signal, regressed on block b's truths, must cancel θ*_l up to O(n^{−1/2}). Consequently:
(M1) under BO (α ≡ 0) and |θ*_j| ≥ θ_min > Lσ*/(φ₀√(n−1)), CL(L) fails for every chain: no T27-type masking
 without cross-block dependence;
(M2) by WS5.2(e), CL(L) requires c_b ≥ φ₀²(|θ*_l| − Lσ*/(φ₀√(n−1)))/(√|U*_b| ‖θ*_{S₀∖C_b}‖₁): a cross-block correlation
 bounded away from zero (it does not vanish with n).
**Status: PROVED** (deterministic).

(N) *Necessity form of (F).* Along any sequence satisfying G, R, SE-blk on which π₀(S₀) ↛ 1 in probability, for every
M_n → ∞ and every η < η_A, infinitely often either some |θ̃_{b,j}| < [√(M_n(σ*²+2M)log n) + √Λ_b]/(φ₀√(n−1))
(**coefficient cancellation**, which needs ‖α_b‖ ≳ θ_min) or max_b Λ_b > ησ*² log n (**large leakage remainder**). Both
quantities vanish identically under BO. *Proof:* contrapositive of (F) (same status as (F)).

**Remark (the LH family of [E]).** corr(x_{j_a}, x_{j_b}) = ψ, θ*_{j_b} = −ψθ*_{j_a}: α_{b,j_b} = ψθ*_{j_a}, so θ̃_{j_b} = 0 exactly,
Λ_b = 0. Masking is exact coefficient cancellation, with zero leakage remainder. If instead θ*_{j_b} is fixed and ψ
varies, θ̃_{j_b} = θ*_{j_b} + ψθ*_{j_a} vanishes at a single ψ: masking is **not monotone** in the cross-block correlation
(numerics N2).

**Remark (random designs).** In iid Gaussian designs with population BO (S1, S3, S4, S6), the sample α_b and ρ_b are
O_P(n^{−1/2}) and O_P(1)·√(Bσ_μ²) respectively, so θ̃ → θ* (EBM holds) but max_b Λ_b is O_P(log p): CBL(η) with small
η is not automatic; the average route NL_avg is needed there ([E] §4.3, PROOF SKETCH). WS5.3(F) is the fixed-design
statement.

---

## §6 WS6 — weights in the favourable regime; the noise-chasing obstruction

**Theorem WS6.**
(a) (*deterministic*) For every S ∈ Ω: 1 + χ²(π‖π₀) = π(S)²/(π₀(S)q₂(S)), and
 1/q₂(S) − 1 = Σ_{S'≠S}[π₀(S')/π₀(S)] e^{2(d(S')−d(S))} = Σ_{S'≠S}[π(S')/π(S)] e^{d(S')−d(S)}.
For α > 1: e^{(α−1)D_α(π‖π₀)} = π(S)^απ₀(S)^{1−α}/q_α(S), 1/q_α(S) − 1 = Σ_{S'≠S}[π(S')/π(S)]e^{(α−1)(d(S')−d(S))}.
(b) (*stable weights ⇐ start sees the truth + tilt control*) χ²(π‖π₀) ≤ 1/(π₀(S₀)q₂(S₀)) − 1, and for **every** grid
0 = φ₀ < … < φ_T = 1, max_t χ²(q_{φ_t}‖q_{φ_{t−1}}) ≤ 1/m² − 1 with m := min{π₀(S₀), q₂(S₀)}.
(c) (*KL needs less tilt control*) For every θ ∈ (0, 1]:
 KL(π‖π₀) ≤ log(π(S₀)/π₀(S₀)) + (π(S₀)/θ)(1/q_{1+θ}(S₀) − 1),
 KL(π₀‖π) ≤ log(π₀(S₀)/π(S₀)) + (π₀(S₀)/θ)(1/q_{−θ}(S₀) − 1).
(d) (*noise-chasing obstruction; ORTH, zero cross-block correlation*) Assume G; ORTH (XᵀX = (n−1)I_p, so BO holds for
**every** partition); s₀ ≥ 1 fixed; θ*_{S₀} fixed and nonzero; S₀ ∈ Ω; let N₀ be the null predictors lying in blocks
that contain no true predictor, with |N₀| → ∞ and log|N₀| = O(log n). Put R̄² := ‖θ*‖²/(‖θ*‖² + σ*²) (population R²).
Then for every fixed α > 1, with probability → 1,
 1/q_α(S₀) − 1 ≥ [(s₀+1)/(2p)] · n^{−1/2} · |N₀|^{1+(α−1)R̄²} · (log|N₀|)^{−(1+(α−1)R̄²)/2} · e^{−O_P(1)}.
Consequently e^{(α−1)D_α(π‖π₀)} ≥ π(S₀)^α × [the same bound]. If |N₀| ≥ p/2 and
p^{(α−1)R̄²}/[√n (log p)^{(1+(α−1)R̄²)/2}] → ∞, then D_α(π‖π₀) → ∞ in probability; for α = 2, **χ²(π‖π₀) → ∞ and the
population ESS fraction → 0**, while TV(π, π₀) → 0 (π(S₀) → 1 by locked T03; π₀(S₀) → 1 by [E] Thm 6 when the truth
meets ≥ 2 blocks, or by WS5.3(F) with η = 0). With p = n − 1 this happens for every R̄² > ½.
(e) **CONJECTURE (threshold).** Under ORTH (more generally BO + SE-blk + favourable), with p = n^A and
ω* := max over truth-free blocks of the limit of 1 − RSS_{S₀}/RSS_{S₀∩C_b} (= R̄² under ORTH):
D_α(π‖π₀) → 0 if A(α−1)ω* < ½ and → ∞ if A(α−1)ω* > ½. KL (α ↓ 1) always vanishes in the favourable regime;
the χ² (α = 2) vanishes iff Aω* < ½. Equivalently the critical Rényi order is α* = 1 + 1/(2Aω*).

*Proof.* (a) WS1(a), (a′) with (u, v) = (0, 1): Σπ^απ₀^{1−α} = π(S)^απ₀(S)^{1−α}/q_α(S), and
1/q_α(S) = Σ_{S'}q_α(S')/q_α(S) = Σ_{S'}[π₀(S')/π₀(S)]e^{α(d(S')−d(S))}; also π(S')/π(S) = [π₀(S')/π₀(S)]e^{d(S')−d(S)}.
(b) First claim: (a) with S = S₀ and π(S₀) ≤ 1. Second: WS1(a) per stage, 1 + χ²_t ≤ 1/(q_{φ_{t−1}}(S₀)q_{w_t}(S₀));
φ_{t−1}, w_t = 2φ_t − φ_{t−1} ∈ [0, 2], and by WS1(e) q_φ(S₀) ≥ min{q₀(S₀), q₂(S₀)} on [0, 2].
(c) log(π/π₀)(S) = log(π(S₀)/π₀(S₀)) + d(S) − d(S₀), so KL(π‖π₀) = log(π(S₀)/π₀(S₀)) + E_π[d − d(S₀)]. For
x > 0, x ≤ (e^{θx} − 1)/θ, so E_π[(d − d(S₀))_+] ≤ θ⁻¹Σ_{S≠S₀}π(S)e^{θ(d(S)−d(S₀))} = θ⁻¹π(S₀)(1/q_{1+θ}(S₀) − 1) by (a)'s
second form with exponent θ = (1+θ) − 1. Same for KL(π₀‖π) = log(π₀(S₀)/π(S₀)) + E_{π₀}[d(S₀) − d], using
q_{−θ}(S)/q_{−θ}(S₀) = [π₀(S)/π₀(S₀)]e^{−θ(d(S)−d(S₀))}.
(d) Fix l ∈ N₀ with block b, U*_b = ∅. ORTH gives, for every T ∌ l: D_{T+l} = D_T·D_l with D_l = ((n+1)(n−1)+1)/n = n,
and t_{T+l} = t_T + t_l with t_l = z_l²/n, z_l := x_lᵀy. By (a),
c_l := q_α(S₀+l)/q_α(S₀) = [π₀(S₀+l)/π₀(S₀)]·e^{α(d(S₀+l)−d(S₀))}, with
π₀(S₀+l)/π₀(S₀) = [w(s₀+1)/w(s₀)]·r_b({l}) = [(s₀+1)/(2p−s₀−1)]·n^{−1/2}(1 − b_l)^{−ν} and
d(S₀+l) − d(S₀) = ν[log(1 − b_l) − log(1 − a_l)], where a_l := t_l/(Q̄ − t_{S₀}) ≥ b_l := t_l/Q̄
(Lemma 0; the D-factors cancel). Hence
 log c_l = log[(s₀+1)/(2p−s₀−1)] − ½ log n + αν(−log(1 − a_l)) − (α−1)ν(−log(1 − b_l))
   ≥ log[(s₀+1)/(2p−s₀−1)] − ½ log n + ανa_l − (α−1)νb_l/(1 − b_l).
On the standardised scale y = Y/s_y, Y = μ + Cε, and x_lᵀμ = 0 for l ∉ S₀ under ORTH, so z_l = σ*√(n−1)Z_l/s_y with
Z_l := x_lᵀε/(σ*√(n−1)); the Z_l, l ∉ S₀, are **iid N(0,1)** (the x_l/√(n−1) are orthonormal). Thus
t_l = (n−1)σ*²Z_l²/(n s_y²). Next, s_y²(Q̄ − t_{S₀}) = RSS_{S₀} + O_P(1), where RSS_{S₀} = ‖(C − P_{S₀})Y‖² ~ σ*²χ²_{n−1−s₀}
[s_y²t_{S₀} = Σ_{j∈S₀}(x_jᵀY)²/n differs from the projection Σ_{j∈S₀}(x_jᵀY)²/(n−1) by Σ(x_jᵀY)²/(n(n−1)) = O_P(1), and
2b₀s_y² = O_P(1)]; and s_y² = ‖Y‖²/(n−1) = ‖θ*‖² + σ*² + O_P(n^{−1/2}) because ‖μ‖² = (n−1)‖θ*‖² under ORTH. Therefore,
with ν = n/2 + 0.01 and ζ_n, ζ'_n = O_P(n^{−1/2}) **not depending on l**:
 νa_l = (Z_l²/2)(1 + ζ_n),  νb_l = (Z_l²/2)(1 − R̄²)(1 + ζ'_n),
and max_l b_l = O_P(log p/n), so b_l/(1 − b_l) = b_l(1 + O_P(log p/n)) uniformly. Hence, uniformly in l ∈ N₀,
 log c_l ≥ log[(s₀+1)/(2p−s₀−1)] − ½ log n + (Z_l²/2)[1 + (α−1)R̄² − |ζ''_n|], ζ''_n = O_P(n^{−1/2}).
Let M₀ := max_{l∈N₀}Z_l². For iid N(0,1), M₀ = 2log|N₀| − log log|N₀| + O_P(1) (Gumbel limit:
P(Z² > a) ~ √(2/π)a^{−1/2}e^{−a/2}). Since M₀|ζ''_n| = O_P(n^{−1/2}log n) = o_P(1) (log|N₀| = O(log n)),
 1/q_α(S₀) − 1 = Σ_{S≠S₀}q_α(S)/q_α(S₀) ≥ max_{l∈N₀}c_l ≥ [(s₀+1)/(2p)]n^{−1/2} exp{(1+(α−1)R̄²)M₀/2 − o_P(1)},
and exp{(1+(α−1)R̄²)M₀/2} = |N₀|^{1+(α−1)R̄²}(log|N₀|)^{−(1+(α−1)R̄²)/2}e^{O_P(1)}. The Rényi bound follows from (a):
e^{(α−1)D_α} = π(S₀)^απ₀(S₀)^{1−α}/q_α(S₀) ≥ π(S₀)^α/q_α(S₀) (π₀(S₀)^{1−α} ≥ 1 for α > 1). With |N₀| ≥ p/2:
the bound is ≳ n^{−1/2}p^{(α−1)R̄²}(log p)^{−(1+(α−1)R̄²)/2}. T03 (locked) applies under ORTH (SE with φ₀ = 1, fixed θ* gives
BM-∞, p ≤ n − 1 ≤ n^A with A = 1), so π(S₀) → 1 and D_α → ∞. TV → 0 by WS1(d) with S = S₀. ∎

**Status.** (a)–(c) **PROVED** (deterministic). (d) **PROVED** (lower bound self-contained; the divergence and TV
consequences cite locked T03 and [E] Thm 6 / WS5.3(F)). (e) **CONJECTURE**; heuristic for the upper side: under BO,
1/q_α(S₀) − 1 ≈ Σ_{N}∏_{l∈N}c_l + (subset terms), and Σ_N∏c_l ≤ exp(Σ_l c_l) − 1 with
Σ_lc_l ≍ n^{−1/2}p^{−1}Σ_le^{(1+(α−1)ω)Z_l²/2} ≍ n^{−1/2}p^{(α−1)ω} (stable-law scaling of a sum of heavy-tailed terms with
index 1/(1+(α−1)ω) < 1); the missing piece is uniform control of large models and of subset terms, where the per-null
expansion fails (a T02-type argument for the doubled-likelihood law q₂ ∝ ϖD^{−1/2}(Q̄ − t)^{−2ν}∏_b(1 − x_b)^ν).

**Interpretation.** The importance weight of S₀ ∪ {l} relative to S₀ is e^{d_σ(S₀+l) − d_σ(S₀)} ≈ e^{ωZ_l²/2}: π₀ judges
the null l against a residual variance inflated by the out-of-block signal (σ*² → σ*² + Δ), π judges it against σ*².
Over p nulls the largest Z_l² is ≈ 2 log p, so a rare start draw S₀ + l carries weight ≈ p^ω. This is a
**noise-variance-sharing** effect, present at zero cross-block correlation: the draft's claim that weak cross-block
dependence bounds the importance-weight variance is false as stated for χ² (it is true for TV, and for KL by (c)
whenever q_{1+θ}(S₀) → 1 for some θ > 0).

---

## §7 WS7 — weights in the masked regime; why the sampler must move (PROVED)

**Theorem WS7.**
(a) ESS_∞(π₀ → π) ≤ π₀(S₀)/π(S₀)², and ≤ π₀(A)/π(A)² for every A ⊆ Ω; KL(π‖π₀) ≥ π(S₀)log(1/π₀(S₀)) − log 2;
TV(π, π₀) ≥ π(S₀) − π₀(S₀).
(b) Under the conclusions of T27(i) [π₀(S₀) = p^{−c}n^{−c/2}e^{O_P(1)}; available from CL(L) + H3 by [E] Thm 4] and of T03
[π(S₀) → 1]: ESS_∞(π₀ → π) ≤ p^{−c}n^{−c/2}e^{O_P(1)}, KL(π‖π₀) ≥ (c log p + (c/2)log n)(1 − o_P(1)) − O_P(1), TV → 1.
(c) *Reweighting cannot create the truth.* Any scheme that starts from N iid π₀ draws and then only reweights and
resamples holds S₀ in some particle with probability 1 − (1 − π₀(S₀))^N ≤ Nπ₀(S₀). In the v3 final run the 4N_e initial
particles contain S₀ with probability ≤ 4N_eπ₀(S₀); every other route to S₀ is a move (independence proposals —
the iid budget Q_f of T11(iii)/T27 — Gibbs flips, swaps, neighbour swaps, local search).
(d) *Accepted grids need only log-log many stages.* Let V ∋ S₀ and let every interval of a grid be accepted at level
ρ̄ ∈ (0,1] (ρ_V(φ_{t−1}, φ_t) ≥ ρ̄; the method uses ρ̄ = 0.9). With ℓ_t := −log q^V_{φ_t}(S₀) and c_ρ := log(1/ρ̄):
 ℓ_t + c_ρ ≥ (ℓ_{t−1} + c_ρ)/2, hence T ≥ log₂[(ℓ₀ + c_ρ)/(ℓ_T + c_ρ)].
Under masking ℓ₀ = log(π₀(V)/π₀(S₀)), so at ρ̄ = 0.9 and ℓ_T ≈ 0, T ≳ log₂(9.5 ℓ₀) ≈ log₂(9.5(c log p + (c/2) log n)). The bound is
attained up to O(1) by two-state families, so restricted-ESS control by itself does not force a long bridge.

*Proof.* (a) WS2(c); data processing for KL on {S₀, S₀ᶜ}: KL ≥ π(S₀)log(π(S₀)/π₀(S₀)) + (1−π(S₀))log((1−π(S₀))/(1−π₀(S₀)))
≥ π(S₀)log(1/π₀(S₀)) − h(π(S₀)) with the binary entropy h ≤ log 2 (the second term is ≥ (1−π(S₀))log(1−π(S₀))).
TV ≥ π(S₀) − π₀(S₀). (b) Substitute. (c) Without mutation the particle set is a subset of the initial draws.
(d) By locked T13(iii) with W = V, ρ_V(u, v)⁻¹ = 1 + χ²(q_v^V‖q_u^V), and q^V is the bridge with γ₀ restricted to V, so
WS1(a) applies to it with S = S₀: ρ_V(u,v)⁻¹ = q_v^V(S₀)²/(q_u^V(S₀)q_w^V(S₀)). Acceptance and q_w^V ≤ 1 give
2ℓ_t ≥ ℓ_{t−1} − c_ρ, i.e. ℓ_t + c_ρ ≥ (ℓ_{t−1} + c_ρ)/2; iterate. q^V_0(S₀) = π₀(S₀)/π₀(V). Two-state attainment: for
a two-point space with odds o_u at u and odds ratio r per unit Δ, 1 + χ² = (1 + o_u)(1 + o_ur²)/(1 + o_ur)²; choosing
r = (0.1/o_u)^{1/2} gives 1 + χ² ≤ 1.1(1 + o_u) ≤ 10/9 when o_u ≤ 0.01, and maps the odds o_u to √(0.1·o_u): the log-odds halve at each stage. ∎

**Reading.** Under masking the importance weights between neighbouring tempered laws can be kept stable with few
stages, but the population holds S₀ with probability ≤ Nπ₀(S₀): what the sampler must supply is **transport**
(moves), not reweighting. This is the T38(b) delivery/repair problem.

---

## §8 The whole bridge and T25(iv)/PW2

**Proposition WS8.**
(a) (PROVED) If the frozen grid has T = 1, Var_c(Ẑ/Z) = χ²(π‖π₀)/(4N_e) exactly (WS2(d)); in the favourable regime
this is ≤ (1/(π₀(S₀)q₂(S₀)) − 1)/(4N_e).
(b) (PROVED under the idealisation IID) Suppose each stage-(t−1) population is N iid draws from q_{t−1}, independent of
the evidence product W_{t−1} (perfect mutation). Then PW2 holds with a_t = χ²(q_{φ_t}‖q_{φ_{t−1}}), ν_t = 0, and locked
T25(iv) gives Var(W_T) ≤ ∏_t(1 + χ²_t/N) − 1 ≤ (1 + (1/m² − 1)/N)^T − 1, m = min{π₀(S₀), q₂(S₀)} (WS6(b)).
(c) (PROVED, exact accounting) For any grid, Σ_{t=1}^T log(1 + χ²(q_{φ_t}‖q_{φ_{t−1}})) = log(π(S)/π₀(S)) +
Σ_t log(q_{φ_t}(S)/q_{w_t}(S)) for every S (telescoping WS1(a)).
(d) (OPEN) PW2 for the actual hybrid particle system at t ≥ 2 (the IID idealisation is not the method).

*Proof.* (a) WS2(d) and WS6(b). (b) Under IID, E[W²_{t−1}((q̂_{t−1}g_t)² − 1)] = E[W²_{t−1}]·Var_{q_{t−1}}(g_t)/N =
E[W²_{t−1}]χ²_t/N. (c) Σ_t[2 log q_{φ_t}(S) − log q_{φ_{t−1}}(S) − log q_{w_t}(S)] telescopes to
log q_{φ_T}(S) − log q_{φ_0}(S) + Σ_t[log q_{φ_t}(S) − log q_{w_t}(S)]. ∎
