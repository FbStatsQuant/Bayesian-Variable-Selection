# A — Proposition A: the √(log p) factor is attained (W3-PSHARP, Claim A)

Status: **PROVED (by this seat, unchecked)**. Check record: see `../REPORT.md` §2.
Notation: `../STATEMENT.md` §0, §2. Uses Lemma V and Lemma S(1), (2), (4) (`S_one_step.md`); nothing else is cited
except two standard facts, stated where used (Chebyshev's inequality; the law of one coordinate of a uniform point of
a sphere).

Throughout: P_n := (s₀+1)/(2p−1−s₀), N := N_n = |𝒩_n|, τ := τ_n = 2 log N, so that
  Λ_n = P_n n^{−1/2} · N √(2τ/π).                                                                              (0)
(Indeed P_n n^{−1/2} N √(4 log N/π) = (s₀+1)[2N/(2p−1−s₀)]√(log N/(πn)).) "odds" := δ_n/(1 − δ_n).

## 1. Lemma W (truncated weak law)
Let ζ₁, …, ζ_N be iid nonnegative random variables, N ≥ 2, τ = 2 log N, W_j := e^{ζ_j/2}1{ζ_j ≤ τ}, T_N := Σ_j W_j.
Suppose that for some η ∈ [0, 1), η′ ≥ 0:
  E W₁ ≥ (1 − η)√(2τ/π),   E W₁² ≤ (1 + η′)√(2τ/π) e^{τ/2} = (1 + η′) N √(2τ/π).
Then for every ϵ′ ∈ (0, 1):
  P( T_N < (1 − ϵ′)(1 − η) N √(2τ/π) ) ≤ (1 + η′)√π / (2 ϵ′² (1 − η)² √(log N)).
*Proof.* (1 − ϵ′)(1 − η)N√(2τ/π) ≤ (1 − ϵ′)E T_N, so by Chebyshev's inequality the probability is at most
Var(T_N)/(ϵ′²(E T_N)²) ≤ N E W₁²/(ϵ′² N² (E W₁)²) ≤ (1 + η′)N²√(2τ/π)/(ϵ′² N² (1 − η)² (2τ/π)) =
(1 + η′)/(ϵ′²(1 − η)²√(2τ/π)), and √(2τ/π) = 2√(log N/π). ∎

**(i) χ²₁.** If ζ = Z², Z ~ N(0, 1), the hypotheses hold with η = η′ = 0:
E W = ∫_{|z|≤√τ} e^{z²/2} (2π)^{−1/2} e^{−z²/2} dz = 2√τ/√(2π) = √(2τ/π) (**exactly**), and
E W² = (2π)^{−1/2}∫_{|z|≤√τ} e^{z²/2} dz ≤ (2π)^{−1/2} · 2√τ · e^{τ/2} = √(2τ/π) e^{τ/2}.

**(ii) Sphere.** Let d ≥ 3, ω uniform on the unit sphere of ℝ^d, t := √d ω₁, ζ := t² = d ω₁². The density of t is
h_d(t) = c_d (1 − t²/d)^{(d−3)/2} on |t| < √d, c_d = Γ(d/2)/(√(πd) Γ((d−1)/2)) (standard: ω₁² ~ Beta(½, (d−1)/2)).
If τ ≤ d/2, the hypotheses hold with
  1 − η = (1 − 1/d) e^{−τ²/(2d)},   1 + η′ = e^{3τ/(2d)}.
*Proof.* (a) c_d√(2π) ∈ [1 − 1/d, 1]. By log-convexity of Γ, for x > 0 and s ∈ [0, 1]: Γ(x+s) ≤ Γ(x)^{1−s}Γ(x+1)^{s} =
x^sΓ(x); applying this to (x+s, 1−s): Γ(x+1) ≤ (x+s)^{1−s}Γ(x+s), i.e. Γ(x+s) ≥ x^sΓ(x)(x/(x+s))^{1−s}. With
x = (d−1)/2, s = ½: Γ(d/2)/Γ((d−1)/2) ∈ [x/√(x+½), √x] = [(d−1)/√(2d), √((d−1)/2)], so
c_d√(2π) = √(2/d) Γ(d/2)/Γ((d−1)/2) ∈ [(d−1)/d, √((d−1)/d)].
(b) For t² ≤ τ ≤ d/2 put x := t²/d ∈ [0, ½]; then −x − x² ≤ log(1 − x) ≤ −x, and (d−3)/2 ≥ 0, so
  t²/2 + ((d−3)/2) log(1 − t²/d) ≤ t²/2 − (d−3)t²/(2d) = 3t²/(2d) ≤ 3τ/(2d),
  t²/2 + ((d−3)/2) log(1 − t²/d) ≥ 3t²/(2d) − (d−3)t⁴/(2d²) ≥ −t⁴/(2d) ≥ −τ²/(2d).
Hence c_d e^{−τ²/(2d)} ≤ e^{t²/2}h_d(t) ≤ c_d e^{3τ/(2d)} on |t| ≤ √τ, and
E W = ∫_{|t|≤√τ} e^{t²/2}h_d(t) dt ≥ 2√τ c_d e^{−τ²/(2d)} ≥ √(2τ/π)(1 − 1/d)e^{−τ²/(2d)};
E W² = ∫_{|t|≤√τ} e^{t²/2}·e^{t²/2}h_d(t) dt ≤ c_d e^{3τ/(2d)} · 2√τ e^{τ/2} ≤ √(2τ/π) e^{τ/2} e^{3τ/(2d)}. ∎

## 2. Reduction (both witnesses)
**Lemma R.** Suppose there are random variables ζ_j ≥ 0 (j ∈ 𝒩_n) and κ with νγ_j ≥ κζ_j/2 for all j ∈ 𝒩_n, the
ζ_j being iid and satisfying the hypotheses of Lemma W with some (η, η′). Then for every ϵ ∈ (0, 1) with η ≤ ϵ/4:
  P( odds < (1 − ϵ)Λ_n ) ≤ P( κ < 1 − ϵ/(2 log N) ) + 8(1 + η′)√π / (ϵ² (1 − η)² √(log N)).
*Proof.* Let c := ϵ/τ = ϵ/(2 log N). On {κ ≥ 1 − c}, for every j (ζ_j ≥ 0):
e^{νγ_j} ≥ e^{(1−c)ζ_j/2} ≥ e^{−cτ/2} e^{ζ_j/2}1{ζ_j ≤ τ} = e^{−ϵ/2}W_j. By Lemma S(4) and (0), on that event
odds ≥ P_n n^{−1/2} e^{−ϵ/2} T_N = Λ_n e^{−ϵ/2} T_N/(N√(2τ/π)). So {odds < (1−ϵ)Λ_n} ∩ {κ ≥ 1 − c} ⊆
{T_N < (1−ϵ)e^{ϵ/2} N√(2τ/π)}. For ϵ ∈ (0, 1): e^{ϵ/2} ≤ 1 + ϵ/2 + ϵ²/4 ≤ 1 + (ϵ/2)/(1−ϵ) = (1 − ϵ/2)/(1 − ϵ), so
(1−ϵ)e^{ϵ/2} ≤ 1 − ϵ/2 ≤ (1 − ϵ/4)² ≤ (1 − ϵ/4)(1 − η). Lemma W with ϵ′ = ϵ/4 bounds the probability of the last
event by (1+η′)√π·16/(2ϵ²(1−η)²√(log N)). (No independence between κ and the ζ_j is used.) ∎

## 3. Proof under (W-orth)
Let u_j := x_j/√(n−1), j ∈ 𝒩_n: an orthonormal family, orthogonal to col X_{S₀} and (centred columns) to 1. Put
g_j := u_jᵀε/σ*: under G these are iid N(0, 1). Fix j ∈ 𝒩_n and use Lemma S with S = S₀:
- g_{S₀,j} = X_{S₀}ᵀx_j = 0, so s_{S₀,j} = n², and x_jᵀρ̃_{S₀} = x_jᵀy − (n+1)(X_{S₀}ᵀx_j)ᵀH⁻¹X_{S₀}ᵀy = x_jᵀy.
- Cy^r = CX^rβ* + Cε = μ + Cε (C1 = 0), μ ∈ col X_{S₀}, x_jᵀC = x_jᵀ: x_jᵀy = x_jᵀ(μ + Cε)/s_y = x_jᵀε/s_y = √(n−1)σ*g_j/s_y.
- By Lemma S(2): Q_{S₀} − Q_{S₀∪{j}} = n(x_jᵀy)²/n² = (n−1)σ*²g_j²/(n s_y²).
So, with V := s_y²(2b₀ + Q_{S₀}): γ_j = (n−1)σ*²g_j²/(nV), and νγ_j = κ_n g_j²/2 with
  κ_n := 2ν(n−1)σ*²/(nV) ≥ (n−1)σ*²/V   (2ν ≥ n).
**Bound on V.** By Lemma V with ϑ = θ*_{S₀} (Cy^r − X_{S₀}θ*_{S₀} = Cε, and ϑᵀ(G+I)ϑ = ‖μ‖² + ‖θ*‖²):
s_y²Q_{S₀} ≤ ‖Cε‖² + (‖μ‖² + ‖θ*‖²)/n ≤ ‖Cε‖² + M + M′. Also 2b₀s_y² = 0.02‖μ + Cε‖²/(n−1) ≤ 0.04(nM + ‖Cε‖²)/(n−1)
≤ 0.06M + 0.04‖Cε‖²/(n−1) (n ≥ 3). With E := ‖Cε‖²/σ*² ~ χ²_{n−1}:
  V ≤ σ*²E(1 + 0.04/(n−1)) + 1.06M + M′.
By Chebyshev (Var E = 2(n−1)), P(E > (n−1) + x√(2(n−1))) ≤ 1/x² for x > 0. On the complement,
  V/(σ*²(n−1)) ≤ (1 + x√(2/(n−1)))(1 + 0.04/(n−1)) + (1.06M + M′)/(σ*²(n−1)) =: 1 + r_n(x),
and κ_n ≥ 1/(1 + r_n(x)) ≥ 1 − r_n(x). Take x = x_n := n^{1/4}: r_n(x_n) ≤ C_σ n^{−1/4} with C_σ depending only on
(M + M′)/σ*². Since N ≤ n − 1 under (W-orth), r_n(x_n) · 2 log N ≤ 2C_σ n^{−1/4} log n → 0, so for n ≥ n(ϵ, C_σ):
P(κ_n < 1 − ϵ/(2 log N)) ≤ P(κ_n < 1 − r_n(x_n)) ≤ n^{−1/2}.
**Conclusion.** Lemma R with ζ_j = g_j² (Lemma W(i): η = η′ = 0) gives, for n ≥ n(ϵ, C_σ),
  P( odds < (1−ϵ)Λ_n ) ≤ n^{−1/2} + 8√π/(ϵ²√(log N_n)) → 0.
The bound depends on the problem only through (ϵ, (M+M′)/σ*², n, N_n): this is the uniformity claimed (N_n ≥ N̲_n → ∞).
(The g_j also enter V; this is harmless — Lemma R needs a deterministic inequality on an event, not independence.) ∎

## 4. Proof under (W-sph)
X_{S₀}, θ* (hence μ = X_{S₀}θ*_{S₀}) are deterministic, so y, s_y, Q_{S₀} and ρ̃ := ρ̃_{S₀} are functions of ε alone.
Write P_H := (n+1)X_{S₀}H⁻¹X_{S₀}ᵀ (H = H_{S₀}), so ρ̃ = (I − P_H)y. With the spectral decomposition
X_{S₀}X_{S₀}ᵀ = Σ_{i≤r₀} λ_i v_iv_iᵀ (λ_i > 0, r₀ = rank X_{S₀} ≤ s₀; v_i ∈ 1^⊥ because the columns are centred),
P_H = Σ_i e_i v_iv_iᵀ with e_i := (n+1)λ_i/((n+1)λ_i + 1) ∈ (0, 1). Hence I − P_H is invertible, ρ̃ ≠ 0, and ρ̃ ∈ 1^⊥.
**Scores.** For j ∈ 𝒩_n, by Lemma S(2), Q_{S₀} − Q_{S₀∪{j}} ≥ (x_jᵀρ̃)²/n = (n−1)⟨ω_j, ρ̃⟩²/n. Put
  ζ_j := (n−1)⟨ω_j, ρ̃/‖ρ̃‖⟩²,   κ′_n := 2ν‖ρ̃‖²/(n(2b₀ + Q_{S₀})) ≥ ‖ρ̃‖²/(2b₀ + Q_{S₀}).
Then γ_j ≥ ‖ρ̃‖²ζ_j/(n(2b₀ + Q_{S₀})) and νγ_j ≥ κ′_nζ_j/2.
**Law of the ζ_j.** Conditionally on ε, ρ̃/‖ρ̃‖ is a fixed unit vector of 1^⊥ (dimension d := n − 1), and the ω_j are iid
uniform on the unit sphere of 1^⊥ (they are independent of ε). By rotation invariance, conditionally on ε the
⟨ω_j, ρ̃/‖ρ̃‖⟩ are iid with the law of one coordinate of a uniform point of the unit sphere of ℝ^d. This conditional
law does not depend on ε; so the ζ_j are iid with the law of Lemma W(ii) (ζ = dω₁², d = n − 1), unconditionally.
**Bound on κ′_n.** Q_{S₀} = yᵀy − n zᵀH⁻¹z = yᵀ(I − (n/(n+1))P_H)y and ‖ρ̃‖² = yᵀ(I − P_H)²y, so
  Q_{S₀} − ‖ρ̃‖² = yᵀP_Hy/(n+1) + yᵀP_H(I − P_H)y.
First term: ≤ ‖y‖²/(n+1) ≤ 1. Second term: = Σ_i e_i(1−e_i)(v_iᵀy)². Write X_{S₀} = Σ_i √λ_i v_iw_iᵀ (singular value
decomposition); s_y v_iᵀy = v_iᵀ(μ + Cε) = √λ_i w_iᵀθ*_{S₀} + v_iᵀε. Since e_i(1−e_i)λ_i = (n+1)λ_i²/((n+1)λ_i+1)² ≤
1/(n+1) and e_i(1−e_i) ≤ ¼, and (a+b)² ≤ 2a² + 2b²:
  s_y² yᵀP_H(I−P_H)y ≤ 2‖θ*‖²/(n+1) + ½‖P₀ε‖² ≤ 2M′ + ½σ*²E₁,
P₀ := Σ_i v_iv_iᵀ the projection onto col X_{S₀}, E₁ := ‖P₀ε‖²/σ*² ~ χ²_{r₀}. Next, by Lemma V,
s_y²Q_{S₀} ≥ min_ϑ‖Cy^r − X_{S₀}ϑ‖² = ‖(I − P₀)(μ + Cε)‖² = ‖(C − P₀)ε‖² = σ*²E₂, E₂ ~ χ²_{n−1−r₀}. Therefore
  1 − κ′_n ≤ (2b₀ + Q_{S₀} − ‖ρ̃‖²)/(2b₀ + Q_{S₀}) ≤ (2b₀ + 1 + (2M′ + ½σ*²E₁)/s_y²)/Q_{S₀} ≤ (1.02 s_y² + 2M′ + ½σ*²E₁)/(σ*²E₂).
Events (E := E₁ + E₂ ~ χ²_{n−1}; m := n − 1 − r₀ ≥ n − 1 − s₀ ≥ n/2, because s₀ + 1 ≤ K ≤ n/2):
{E ≤ 2(n−1)} has probability ≥ 1 − 2/(n−1) (Chebyshev); {E₂ ≥ m/2} has probability ≥ 1 − 8/m ≥ 1 − 16/n (Chebyshev);
{E₁ ≤ x(r₀+1)} has probability ≥ 1 − 1/x (Markov, E E₁ = r₀). On their intersection,
s_y² = ‖μ + Cε‖²/(n−1) ≤ 2(nM + σ*²E)/(n−1) ≤ 3M + 4σ*² and E₂ ≥ n/4, so
  1 − κ′_n ≤ (C₀ + 2x(r₀+1))/n,   C₀ := 4(1.02(3M + 4σ*²) + 2M′)/σ*².
Take x = x_n := (n/((r₀+1) log N))^{1/2} → ∞ (hypothesis (r₀+1) log N = o(n)). Then
(1 − κ′_n)·2 log N ≤ 2C₀ log N/n + 4((r₀+1) log N/n)^{1/2} → 0, so for n large (depending on ϵ, C₀ and the o(·)
sequences): P(κ′_n < 1 − ϵ/(2 log N)) ≤ 2/(n−1) + 16/n + 1/x_n → 0.
**Conclusion.** (log N)² = o(n) gives τ = 2 log N ≤ d/2 eventually and, in Lemma W(ii), η → 0, η′ → 0. Lemma R gives
  P( odds < (1−ϵ)Λ_n ) ≤ 2/(n−1) + 16/n + 1/x_n + 8(1+η′)√π/(ϵ²(1−η)²√(log N_n)) → 0,
a bound depending only on (ϵ, σ*², M, M′, n, N_n, (r₀+1) log N_n/n, (log N_n)²/n): uniform as claimed. The columns outside
S₀ ∪ 𝒩_n never enter: Lemma S(4) sums over 𝒩_n only, and each term involves only (X_{S₀}, x_j, y). ∎

## 5. Random (X_{S₀}, θ*)
Let (X_{S₀}, θ*) be random and suppose that, conditionally on (X_{S₀}, θ*), the hypotheses hold on an event 𝒜_n
(measurable in (X_{S₀}, θ*)) with P(𝒜_n) → 1: ε ~ N_n(0, σ*²I), and (W-orth) or the (W-sph) structure for the null
block, with the same constants. The bounds of §3–§4 are uniform, so
P(odds < (1−ϵ)Λ_n) ≤ P(𝒜_nᶜ) + sup_{𝒜_n} P(odds < (1−ϵ)Λ_n | X_{S₀}, θ*) → 0. ∎

## 6. Corollaries
**A1.** s₀ fixed, 𝒩_n = [p]∖S₀, p → ∞: N = p − s₀, 2N/(2p−1−s₀) → 1, log N/log p → 1, so
Λ_n = (1+o(1))(s₀+1)√(log p/(πn)). Λ_n → 0: under (W-orth), N ≤ n − 1; under (W-sph), (log N)² = o(n). On
{odds ≥ (1−ϵ)Λ_n}: δ_n = odds/(1+odds) ≥ (1−ϵ)Λ_n/(1 + (1−ϵ)Λ_n) ≥ (1−ϵ)(1−Λ_n)Λ_n (x ↦ x/(1+x) is increasing). So
P(δ_n ≥ (1−2ϵ)Λ_n) → 1 for every ϵ, i.e. δ_n ≥ (1 − o_P(1))(s₀+1)√(log p/(πn)); and
E δ_n ≥ P(odds ≥ (1−ϵ)Λ_n)(1−ϵ)(1−Λ_n)Λ_n gives liminf E δ_n/Λ_n ≥ 1 − ϵ for every ϵ. With p = ⌊n^a⌋:
√(log p/n) = (1+o(1))√a · r_n.
**A2.** 𝒩_n = [p]∖S₀, p → ∞, s₀/p → 0 (s₀ may grow): again Λ_n = (1+o(1))(s₀+1)√(log p/(πn)), and Proposition A
is a statement about the odds, valid whether or not Λ_n → 0. (i) If π(S₀) → 1 in probability then odds → 0 in
probability, which with P(odds ≥ ½Λ_n) → 1 forces Λ_n → 0: s₀ = o(√(n/log p)). (ii) Let log p ≍ log n and
δ_n = O_P(r_n). Then δ_n → 0 in probability, so Λ_n → 0 by (i), and by the argument of A1
P(δ_n ≥ ½Λ_n) → 1; with δ_n = O_P(r_n) this gives Λ_n = O(r_n), i.e. (s₀+1)√(log p/log n) = O(1): s₀ = O(1).
(The hypotheses are satisfiable with s₀ → ∞: e.g. the orthogonal design with θ*_j = s₀^{−1/2} on S₀ has
‖μ‖² = n − 1 and ‖θ*‖² = 1.)

## 7. Remarks
1. **Moments re-derived (BRIEF).** For W = e^{Z²/2}: P(W > w) = 2Φ̄(√(2 log w)) ~ 1/(w√(π log w)); E[W; W ≤ N] =
   2√(log N/π) exactly; E[W²; W ≤ N] = (2/√(2π))∫₀^{√(2 log N)} e^{z²/2}dz ~ N/√(π log N). The proof uses the cruder
   bound 2N√(log N/π) for the second moment (a factor 2 log N larger), which is enough for Chebyshev. Checked
   numerically: `../numerics/a_orth_out.txt`, E3.
2. **Remark A3 of the STATEMENT (what the two example sequences satisfy; consumes nothing in the proofs above).**
   (i) Orthogonal design, p = min(n−1, ⌊n^a⌋), 0 < a ≤ 1, fixed θ* with fixed support S₀, s₀ ≥ 1: (W-orth) with
   𝒩_n = [p]∖S₀; (E) with M = ‖θ*‖² and (C) with M′ = ‖θ*‖²/3 (n ≥ 3); and, in the notation of [W3P] §2: R1 with A = 1;
   every X_SᵀX_S/(n−1) is the identity, so (F_λ) holds with φ₀ = 1 and (F_w) with g₀ = 1 (λ_min(G_S) = n − 1 ≥ 1);
   BM-∞ holds since θ*_min is fixed. (ii) Raw entries iid N(0, 1), p = ⌊n^a⌋, a > 0, fixed raw β* on a fixed S₀:
   the standardised null columns are x_j = √(n−1) Cx^r_j/‖Cx^r_j‖, and Cx^r_j ~ N_n(0, C) is rotation-invariant in
   1^⊥, so the ω_j are iid uniform on the unit sphere of 1^⊥, independent of (X^r_{S₀}, ε); θ* = D_xβ* is a function of
   X^r_{S₀}; (E), (C) hold on the event that the raw sample standard deviations of the S₀ columns are ≤ 2
   (probability → 1), with M′ = 4‖β*‖², M = s₀M′·(n−1)/n ≤ s₀M′; (log p)² = o(n). So §5 applies. That sequence is in
   the scope of [W3P] Corollary 1R with Σ_n = I (λ_min(Σ_{n,S}) = 1: LSF (i), (ii) with ψ_n = 1) and A = max(a, 1).
   The **upper** bounds δ_n = O_P(r_n) on (i), (ii) are `W3-POST:Thm-1`@1.0.0 and `W3-POST:Cor-1R`@1.0.0; they are
   quoted, not re-proved, and the two-sided reading is conditional on them.
3. **Numerics.** `../numerics/a_orth.py` (orthogonal witness; exact odds by a Gamma-integral/elementary-symmetric
   DP validated against brute force to 1e-13) and `../numerics/a_sph.py` (iid Gaussian design, p up to 4·10⁷; exact
   one-step odds): the ratio to Λ_n has median 0.97–1.09 on the spherical witness (one-step odds) and 1.00–1.51 on the
   orthogonal one (odds over all models of size ≤ s₀ + 60), decreasing in n to 1.003–1.007 at n = 25600, p = n − 1.
   "Exact" means an exact formula evaluated by quadrature (validated against brute force and against all sizes ≤ K where
   affordable), not a certified enclosure. Growing s₀ inside (E), (C) (E2: θ*_j = s₀^{−1/2}): ratio 1.26–1.37, minimum 0.98.
   Boundary experiment (one-step odds only, equicorrelated nulls): `../numerics/a_boundary.py`.
