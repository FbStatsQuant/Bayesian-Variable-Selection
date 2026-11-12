# W3-PSHARP — STATEMENT (v1.1, 2026-11-11; lead: Claude Fable 5.2, claudeAgent, high; v1.1 = statement-lock amendments [L01-#]; **locked**)

Ticket T3 of `Theory_work/Wave3/API_AUDIT/sharp1/TRIAGE.md`: three **sharpness records** (lower bounds / necessity)
for the posterior theorem. No new upper bound is claimed. All results are about the exact coded target π. Statuses are
verbatim; each claim carries the status of its proof file (`lemmas/S_one_step.md`, `A_log_factor.md`, `B_sparsity.md`,
`C_counterexample.md`).

**Aliases.** **[W3P]** = `Theory_work/Wave3/W3-POST/STATEMENT.md` (v1.4); **[L1a′]** =
`Theory_work/Wave3/W3-POST/lemmas/L1a_size_tail.md`; **[LB]** = `Theory_work/Wave3/W3-POST/lemmas/LB_rate_lower_bound.md`;
**[P2S]** = `Theory_work/Wave3/W3-POST2/STATEMENT.md` (v1.2.1); **[1a″]** = `Theory_work/Wave3/W3-POST2/lemmas/B_tail_approx.md`.
Registry ids of the claims these records sharpen: `W3-POST:Thm-1`@1.0.0, `W3-POST:Prop-LB`@1.0.0,
`W3-POST:Lemma-1a'`@1.0.0, `W3-POST2:A2`@1.0.0, `W3-POST2:B`@1.0.0, `W3-POST2:C`@1.0.0. **None of them is used in a
proof here**: every proof below starts from the definition of π ([W3P] §0, lines 16-34). They are referred to only to
say what is sharpened.

## 0. Notation

Exactly [W3P] §0: data (X^r, y^r), n ≥ 3, s_y > 0; X the standardised design (centred columns, ‖x_j‖² = n − 1), p ≥ 2
columns; y = Cy^r/s_y, s_y² = ‖Cy^r‖²/(n − 1) (C the centring projection); Ω = {S ⊆ [p] : |S| ≤ K},
K = min(p, ⌊n/2⌋); G_S = X_SᵀX_S, H_S = (n + 1)G_S + I, D_S = det H_S/det(G_S + I), z_S = X_Sᵀy,
Q_S = yᵀy − n z_SᵀH_S⁻¹z_S, ν = 0.01 + n/2, b₀ = 0.01; w(k) = ½/C(2p − 1, k); π(S) ∝ w(|S|) D_S^{−1/2}(2b₀ + Q_S)^{−ν}
on Ω. δ_n := 1 − π(S₀). r_n := √(log n/n).

Truth (**G**): y^r = α*1 + X^rβ* + ε, ε ~ N_n(0, σ*²I), μ := CX^rβ* = Xθ*, S₀ = supp θ*, s₀ = |S₀|. In Lemma S and
Claim B, S₀ is **any** subset (no truth, no law is used).

Further notation. For S ∈ Ω and j ∉ S: g_{S,j} := X_Sᵀx_j, s_{S,j} := n² − (n + 1)² g_{S,j}ᵀH_S⁻¹g_{S,j},
ρ̃_S := y − (n + 1)X_SH_S⁻¹X_Sᵀy (ridge residual of y on S; ρ̃_∅ = y). For j ∉ S₀:
  γ_j := (Q_{S₀} − Q_{S₀∪{j}})/(2b₀ + Q_{S₀}).
c(p, s) := (s + 1)(p − s)/(2p − 1 − s). "Unit sphere of 1^⊥" = {ω ∈ ℝⁿ : 1ᵀω = 0, ‖ω‖ = 1}.

## 1. Lemma S (one-step supersets with the fit factor kept; deterministic)

Let n ≥ 3, X any standardised design with p ≥ 2, y any standardised response, S ⊆ [p] with |S| + 1 ≤ K (S = ∅
allowed), j ∉ S. Then:
1. **(determinant)** D_{S∪{j}}/D_S = s_{S,j}/(n − g_{S,j}ᵀ(G_S + I)⁻¹g_{S,j}), 0 < s_{S,j} ≤ n², and
   D_{S∪{j}}/D_S ≤ n, with equality iff x_j ⟂ col X_S. Hence D_{S∪J}/D_S ≤ n^{|J|} for every J disjoint from S.
2. **(fit)** Q_S − Q_{S∪{j}} = n (x_jᵀρ̃_S)²/s_{S,j} ≥ (x_jᵀρ̃_S)²/n ≥ 0, and 0 ≤ Q_{S∪{j}} ≤ Q_S.
3. **(one model)** with S = S₀ (so s₀ + 1 ≤ K) [L01]: γ_j ∈ [0, 1) and
   π(S₀∪{j})/π(S₀) ≥ [(s₀ + 1)/(2p − 1 − s₀)] n^{−1/2} (1 − γ_j)^{−ν} ≥ [(s₀ + 1)/(2p − 1 − s₀)] n^{−1/2} e^{νγ_j}.
4. **(sum)** for every 𝒩 ⊆ [p]∖S₀:
   δ_n/(1 − δ_n) ≥ [(s₀ + 1)/(2p − 1 − s₀)] n^{−1/2} Σ_{j∈𝒩} e^{νγ_j}.

(Items 3–4 keep what [LB] line 28 and `W3-POST2:A2` discard: the fit factor. Item 1 improves [LB]'s n + 1 to n.)

## 2. Claim A — Proposition A: the √(log p) factor is attained

**Setting.** A sequence of problems indexed by n → ∞ under G, with S₀ = S₀(n), s₀ + 1 ≤ K (s₀ may be fixed or
grow), and a set of null columns 𝒩_n ⊆ [p]∖S₀ with N_n := |𝒩_n| → ∞. Fixed constants σ*² > 0, M, M′ < ∞ with
- **(E)** ‖μ‖² ≤ nM;  **(C)** ‖θ*‖² ≤ nM′ (recall μ = X_{S₀}θ*_{S₀}).

**Witness conditions** (either one; both are conditions on the null block 𝒩_n only — the columns outside S₀ ∪ 𝒩_n are
arbitrary and may depend on everything):
- **(W-orth)** *(fixed design)* the columns x_j, j ∈ 𝒩_n, are mutually orthogonal and orthogonal to col X_{S₀}.
  (Then N_n ≤ n − 1 − rank X_{S₀}.)
- **(W-sph)** *(random null block)* X_{S₀} and θ* are deterministic; the directions ω_j := x_j/√(n − 1), j ∈ 𝒩_n, are
  iid uniform on the unit sphere of 1^⊥ and independent of ε; and (log N_n)² = o(n), (s₀ + 1) log N_n = o(n).
  (Example: raw null columns with iid N(0, 1) entries, independent of X^r_{S₀} and ε; any p compatible with the two
  logarithmic restrictions, in particular p ≫ n [L01].)

**Proposition A.** Put
  Λ_n := (s₀ + 1) · [2N_n/(2p − 1 − s₀)] · √(log N_n/(πn)).
Under the setting and (W-orth) or (W-sph), for every fixed ϵ ∈ (0, 1):
  P( δ_n/(1 − δ_n) ≥ (1 − ϵ)Λ_n ) → 1,
uniformly over all designs, θ*, S₀ and 𝒩_n that satisfy the hypotheses with the same (σ*², M, M′) and N_n ≥ N̲_n for
a fixed sequence N̲_n → ∞ (in (W-sph) also with common o(·) sequences). Consequently, if (X_{S₀}, θ*) is random and
the hypotheses hold conditionally on (X_{S₀}, θ*) on events of probability → 1, the conclusion holds under the joint
law.

**Corollary A1 (fixed s₀, all nulls).** If s₀ is fixed, 𝒩_n = [p]∖S₀ and p → ∞, then Λ_n = (1 + o(1))(s₀ + 1)√(log p/(πn)) → 0 and
  δ_n ≥ (1 − o_P(1)) (s₀ + 1) √(log p/(πn)),   liminf E δ_n / [(s₀ + 1)√(log p/(πn))] ≥ 1.
With p = ⌊n^a⌋, a > 0: δ_n ≥ (1 − o_P(1)) (s₀ + 1)√(a/π) · r_n.

**Corollary A2 (growing s₀ on witness designs).** With 𝒩_n = [p]∖S₀, p → ∞ and s₀/p → 0: δ_n/(1 − δ_n) ≥
(1 − o_P(1))(s₀ + 1)√(log p/(πn)). So on witness designs π(S₀) → 1 in probability requires
s₀ = o(√(n/log p)), and δ_n = O_P(r_n) with log p ≍ log n requires s₀ = O(1).

**Remark A3 (what this settles; reading with the upper bounds — not part of the claim).** Two sequences satisfy both
Proposition A and the hypotheses of `W3-POST:Thm-1`@1.0.0 (regime R1, fixed s₀ ≥ 1, fixed nonzero coefficients):
(i) the orthogonal design XᵀX = (n − 1)I_p with p = min(n − 1, ⌊n^a⌋), 0 < a ≤ 1 [L01-m2]: (E), (F_λ), (F_w), (BM) hold with
φ₀ = 1, g₀ = 1, A = 1; (ii) raw designs with iid N(0, 1) entries and p = ⌊n^a⌋, any fixed a > 0 — in particular
**p ≫ n** — through `W3-POST:Cor-1R`@1.0.0 (Σ_n = I). On both, conditional on those two claims,
(s₀ + 1)√(a/π)(1 − o_P(1)) ≤ δ_n/r_n = O_P(1): the rate √(log n/n) of Theorem 1 is exact whenever log p ≍ log n, and
the conjecture at [W3P] line 104 ("whether the extra √(log n) is attained for p = n^A") is true. With
`W3-POST2:C`@1.0.0, the same holds for E δ_n on (i), and on (ii) provided the design-event term P(𝒜_nᶜ) of its
random-design form is O(r_n) (not checked here) [L01] (open question 6 of W3-POST2 REPORT §6). Not settled: an upper bound of
order √((1 ∨ log p)/n) when log p = o(log n).

## 3. Claim B — Corollary B: a sparsity obstruction on every design

**Corollary B.** For every n ≥ 3, every standardised design with p ≥ 2, every data set and every S₀ ⊆ [p] with
0 ≤ s₀ ≤ K − 1 (deterministic; no law, no truth):
  δ_n/(1 − δ_n) ≥ 𝒪^{lb}_n := Σ_{j=1}^{K−s₀} C(s₀ + j, j) n^{−j/2} Π_{i=0}^{j−1} (p − s₀ − i)/(2p − 1 − s₀ − i) ≥ c(p, s₀)/√n,
equivalently π(S₀) ≤ √n/(√n + c(p, s₀)). Here c(p, s₀) ≥ (s₀ + 1)/3 whenever s₀ ≤ p/2; c(p, s₀) ≥ 1 for s₀ ≥ 1;
c(p, 0) > ½; and c(p, s₀)/(s₀ + 1) → ½ when p → ∞ and s₀/p → 0 [L01-m1].

**Consequences** (any sequence with s₀ ≤ min(K − 1, p/2); any designs; any data, random or not):
- **(B1)** π(S₀) ≤ [1 + (s₀ + 1)/(3√n)]⁻¹ surely. So π(S₀) → 1 (in probability, along any subsequence) forces
  s₀ = o(√n); if s₀ ≥ λ√n then π(S₀) ≤ 1/(1 + λ/3); and if s₀/√n → ∞ then π(S₀) → 0 surely.
- **(B2)** δ_n = O_P(ρ_n) for a deterministic ρ_n → 0 forces s₀ + 1 = O(√n ρ_n). In particular the rate r_n forces
  s₀ = O(√(log n)) on every design, and — by Corollary A2 — s₀ = O(1) on witness designs with log p ≍ log n.
- **(B3) Target correction.** The recorded growing-s₀ target "s₀ = o(log n/log log n)" (W3-POST REPORT §4 item 8,
  `Theory_work/Wave3/W3-POST/REPORT.md:190`) cannot retain the rate r_n when s₀ → ∞ on the witness sequences of
  Corollary A2 with log p ≍ log n [L01-M1]. On those sequences a concentration theorem must allow at least the rate
  (s₀ + 1)√(log p/n), and consistency (π(S₀) → 1) requires s₀ = o(√(n/log p)); for a general witness block use Λ_n of
  Proposition A. (With log p = o(log n) the rate r_n can survive a slowly growing s₀; no obstruction is claimed there.)
  On **every** design with s₀ ≤ min(K − 1, p/2), π(S₀) ↛ 1 once s₀ ≍ √n (B1): beyond that scale only mode (HPM)
  consistency can be aimed at, not π(S₀) → 1.

(Corollary B is `W3-POST2:A2` with D_{S₀∪J}/D_{S₀} ≤ n^{|J|} inserted and the multiplicity kept; its j = 1 term with
the multiplicity bounded below by 1 is [LB] with n in place of n + 1. It also covers s₀ = 0.)

## 4. Claim C — Proposition C: ridge-cost control of the reference cannot be dropped

**Design 𝔇_n.** Fix σ*² > 0 and b̄ > 0. For n ≥ n₀ put k := ⌈12 log n⌉, p := k + 2, η := n⁻², with n₀ := 200 (then k + 1 ≤ n − 1 and K = p). Let x₁, x₃, …, x_{k+2} be
mutually orthogonal centred vectors in ℝⁿ with squared norm n − 1, u := Σ_{j=3}^{k+2} x_j,
and x₂ := c(x₁ − ηu), c := (1 + η²k)^{−1/2} (so ‖x₂‖² = n − 1; X is standardised). T′ := {3, …, k + 2}, T := {1, 2}.
Truth: G with X^r = X and β* = θ* := (b_n/√k)1_{T′}, i.e. μ = (b_n/√k)u (the law of the data depends on β* only through
μ), where 0 < b_n ≤ b̄ and n b_n² ≥ C_b (σ*² + b̄²)(log n)², C_b := 1200 (e.g. b_n ≡ b̄ and n large).

**Proposition C.** On 𝔇_n:
1. **(hypotheses of [L1a′] except the coefficient bound)** G holds; ‖μ‖² = b_n²(n − 1) ≤ n b̄² (so (E) with M = b̄²);
   T ∈ Ω, t = 2, and μ = X_Tθ **exactly** with θ = (b_n/(η√k))(1, −1/c). But ‖θ‖² ≥ b_n² n⁴/k, so
   ‖θ‖²/n → ∞: only the coefficient bound ‖θ‖² ≤ nM′ of [L1a′] fails. Likewise for [1a″] with reference T: the
   approximation error can be made zero, but every ϑ ∈ ℝ^T has cost B_T(ϑ) ≥ b_n²(n − 1)/2, and
   min_ϑ B_T(ϑ) ≤ b_n²(n − 1): the reference cost is of exact order n b_n² (→ ∞, at least like (log n)²).
   (A bounded-cost reference exists — T′ with ϑ = (b_n/√k)1, cost b_n² ≤ b̄² — but it has k = ⌈12 log n⌉ columns.)
   Here B_T(ϑ) := ‖μ − X_Tϑ‖² + (‖X_Tϑ‖² + ‖ϑ‖²)/n ([P2S] line 44).
2. **(cutoffs)** With m_n := ⌊k/2⌋ and n ≥ n₀: R^T_{m_n} ≤ n⁻², hence m^T_n(½ log n) ≤ m_n ([L1a′] lines 11-12,
   t = 2), and A^T_{m_n} = R^T_{m_n}√(D_T)√n ≤ 2/n ≤ n^{−1/2} ([1a″] line 10).
3. **(failure of the conclusion)** There is c₁ > 0 depending only on (σ*², b̄) such that
   P( π(|S| ≤ m_n) ≤ exp(−c₁ n b_n²) ) → 1; in particular π(|S| > m^T_n(½ log n)) → 1 in probability.

Hence the conclusions of [L1a′] and [1a″] for the reference T — π(|S| > m^T_n(½ log n)) = O_P(n^{−1/2}), resp.
π(|S| > m_n) = O_P(n^{−1/2}) — **fail**: Θ^T_{n,m_n} → ∞ and Θ″_{n,m_n} → ∞ in probability. So:
- in `W3-POST:Lemma-1a'` the coefficient bound (registry assumption A:COEF-REP) cannot be dropped: exact
  representation by T plus (E) is not enough ([L1a′] Remark 2, recorded as open, is settled: **necessary in kind**);
- in `W3-POST2:B` the bounded reference cost cannot be weakened to "small (even zero) approximation error" nor to any
  cost bound B_n with B_n/(log n)² → ∞: some control of the ridge cost is necessary. (It is not necessary that the
  cost be bounded for every reference: W3-POST2 numerics N6b. The gap between O(1) and (log n)² is open.)

## 5. What is not claimed
- No upper bound. No statement about the sampler. No exact constant on general designs: Proposition A is a lower
  bound on two witness classes; for p ≫ n it needs the spherical null block (W-sph). Whether
  δ_n = (1 + o_P(1))Λ_n on the orthogonal witness is a numerical observation only (`numerics/`).
- Proposition C concerns the reference T = {1, 2}; with the bounded-cost reference T′ the lemmas hold and give a
  (correct) cutoff ≥ k.
