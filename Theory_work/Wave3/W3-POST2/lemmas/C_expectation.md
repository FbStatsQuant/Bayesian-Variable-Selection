# C — Proposition ER: the expectation rate E[1 − π(S₀)] = O(r_n) (W3-POST2, Claim C; v2)

Status: **PROVED (by this seat, unchecked)**. **Check record [C1B-2]:** v1 line check K-BC (VERIFIED-WITH-AMENDMENTS); v2 line check K2 (gpt-6.1-sol high, `../reviews/K2_v2_check_sol.md`): **VERIFIED**; M01: sound; S01: no defect; council C1 (PASS). v2 (STATEMENT v1.2) adopts R03b's proposal C+ (`../reviews/R03b_better_theorem_astra.md`
§C): the v1 bound C n^{−1/2}e^{2√(2 log n)} is superseded by C r_n. Notation:
`../STATEMENT.md`, [P1] (`lem:slab`, `lem:prior`, `lem:num`, `lem:den`, `thm:T01iii`, `thm:Ta`), [P3], [T03R],
[L1a′], `A_occam.md` ((G3′), (C5′), (C8′)), `E_visibility.md` (Lemma E1, event 𝒢⁵_n).

## Statement (per-n hypotheses [L01-3])
Fix s₀ ≥ 1, A ≥ 1 and constants (σ*², M, φ₀, c) and g₀ (case i) or C_OS (cases ii–iii). There are n₀ and C depending only
on these such that for every n ≥ n₀ and every fixed design X and θ* for which, at that n, s₀ ≤ K, 2 ≤ p ≤ n^A, G, (E),
(F₀) and one of
(i) (F_λ), (F_w; g₀), BM(c), c > c₀;  (ii) (F_λ), (OS; C_OS), BM(c), c > c₀;  (iii) (OS; C_OS), (ID^M; c), c > c₁
hold:  **E δ_n ≤ C r_n.** Under BM-∞ the same holds with n₀ depending also on the envelope. For random designs on
(X, θ*)-measurable events 𝒜_n on which the hypotheses hold: E δ_n ≤ C r_n + P(𝒜_nᶜ) (condition on (X, θ*); ε ⫫ (X, θ*)).
Every step is a bound at a single n using hypotheses at that n only.

## Lemma C1 (deterministic denominator on a high-probability event)
Assume G, (E), (F₀), s₀ ≤ K, n ≥ 16. Let E′ := ‖ε_c‖²/σ*² ~ χ²_N. On {E′ ≤ 2N},
  m^c_{b₊}(S₀)/f₀(y_c) ≥ c_den D_{S₀}^{−1/2} n^{−1/2},  c_den := σ*²·c′_IG·exp{−3 − ρ̄/σ*²},
where ρ̄ := M + M/(2φ₀²) and c′_IG := min_{v∈[σ*²/2, 2σ*²]} IG(v; 0.51, b₊) > 0 (depends on (σ*², M) only).
*Proof.* By (F₀), (E) and [L1a′] (its "changed step" with T = S₀, θ = θ*; ‖θ*‖² ≤ 1.5M/φ₀² by [L1a′] Remark 1):
Q^c_{S₀} ≤ σ*²E′ + ρ with deterministic 0 ≤ ρ ≤ ρ̄. As in [P1] `lem:den` ("Integral representation"),
  m^c_{b₊}(S₀)/f₀(y_c) = D_{S₀}^{−1/2}∫_0^∞ exp{−(N/2)log(v/σ*²) + E′/2 − Q^c_{S₀}/(2v)} IG(v; 0.51, b₊) dv.
With u := v/σ*², the exponent is ≥ F(u) − ρ/(2σ*²u), F(u) := −(N/2)log u + (E′/2)(1 − 1/u). F(1) = 0,
F′(1) = (E′ − N)/2, F″(u) = N/(2u²) − E′/u³. Let I := [1, 1 + n^{−1/2}] if E′ ≥ N and I := [1 − n^{−1/2}, 1] if E′ < N
(I ⊆ [3/4, 5/4] for n ≥ 16; the choice depends on the data, which is allowed in a pointwise lower bound). On I and on
{E′ ≤ 2N}: |F″(u)| ≤ N/(2·(3/4)²) + 2N/(3/4)³ ≤ 6N, and F′(1)(u − 1) ≥ 0, so by Taylor's theorem
F(u) ≥ −3N(u − 1)² ≥ −3N/n ≥ −3. Also ρ/(2σ*²u) ≤ ρ̄/σ*² (u ≥ 3/4 > ½). Restricting the integral to v ∈ σ*²I
(length σ*²n^{−1/2}, inside [σ*²/2, 2σ*²]) gives the claim. ∎

## Lemma C2 (expected size tail)
Under the assumptions of C1, for every integer m (deterministic) (if R_m = 0 then π(|S| > m) = 0 and there is nothing to
prove [K-BC-2]; below R_m > 0):
  E π(|S| > m) ≤ (κ²/c_den)·R_m √(D_{S₀}) √n + (8 + 24M/σ*²)/(n − 1) + e^{−N/8}.
*Proof.* On 𝓑_n, [P1] `thm:Ta` gives π(E_m) ≤ κ²N_m/(ϖ(S₀)m^c_{b₊}(S₀)/f₀) with N_m := I_{b₋}(E_m)/f₀(y_c), E N_m = ϖ(E_m)
= R_mϖ(S₀) ([P1] `lem:num`, b₋ data-free; W_K cancels). On 𝓑_n ∩ {E′ ≤ 2N}, Lemma C1 gives
π(E_m) ≤ (κ²/c_den)√(D_{S₀})√n·N_m/ϖ(S₀); its expectation is ≤ (κ²/c_den)√(D_{S₀})√n R_m (no independence needed: the
bound is a deterministic multiple of N_m ≥ 0). Off this event use π ≤ 1: P(𝓑_nᶜ) ≤ (8 + 24M/σ*²)/(n−1) ([P1]
`thm:T01iii`), P(E′ > 2N) ≤ e^{−N/8} ([P3] `lem:chi`(a) with x = N/8: N + 2√(Nx) + 2x ≤ 2N). ∎

At m = m♯_n: R_m ≤ n^{−(s₀+1)/2}e^{−½ log n} and D_{S₀} ≤ (n+1)^{s₀} ([P1] `lem:spec`(e)), so
E π(|S| > m♯_n) ≤ (κ²/c_den)(1 + 1/n)^{s₀/2} n^{−1/2} + O(1/n).

## Proof of the statement
δ_n ≤ T₀ + T_sup + T_U as in [P3] §main (i), with T₀ := π(|S| > m♯_n), T_sup := π(S ⊋ S₀, |S| ≤ m♯_n), T_U := π(𝒰),
𝒰 the underfitting S ∈ Ω with |S| ≤ m♯_n. Let 𝒢*_n := 𝒢^sel_n (cases i–ii) or 𝒢^sup_n ∩ 𝒢⁵_n (case iii). Then
  E δ_n ≤ E T₀ + E[(T_sup + T_U)1_{𝒢*_n}] + P((𝒢*_n)ᶜ).
- E T₀ = O(n^{−1/2}) by Lemma C2.
- On 𝒢*_n, T_sup ≤ e^{ρ_n}Υ_n (case i: [P3] `prop:sup`(a) via [T03R] (C5)) or ≤ e^{ρ_n}Υ′_n (cases ii–iii: (C5′)(a));
  so E[T_sup1] ≤ e^{ρ_n}2K_{s₀,0}q_n ≤ C r_n (case i, [T03R] (C5)(b)) or ≤ e^{ρ_n}𝒪_n^{>0} ≤ 2C_OS r_n ((C5′)(b), (OS)).
- On 𝒢*_n, [T03R] (C8) / (C8′): T_U ≤ 2^{s₀}κ̄_n(1 + e^{ρ_n}Υ) + 2^{s₀}e^{2ρ_n}(2p)^{s₀}(n+1)^{s₀/2}Υ^{>j₀} with the
  deterministic κ̄_n = e^{ρ_n}n^{−2} ([T03R] (C10), BM(c), c > c₀) or κ̄_n = n^{−2} (Lemma E1, (ID^M; c), c > c₁). Taking
  expectations: E[T_U1] ≤ C(n^{−2} + (log n)^{(j₀+1)/2}/n) (case i) or ≤ C(n^{−2} + r_n) (ii–iii, (OS)).
- P((𝒢^sel_n)ᶜ) ≤ 5/n, P((𝒢^sup_n)ᶜ) ≤ 4/n ((G3′), A_occam), P((𝒢⁵_n)ᶜ) ≤ 1/n (Lemma E1(a)).
All terms are O(r_n). ∎

## Corollaries and remarks
1. P(HPM ≠ S₀) ≤ 2E δ_n ([P3] (iii)); P(MPM ≠ S₀) ≤ 2Eδ_n; P(ξ_q ≠ S₀) ≤ Eδ_n/min(q, 1 − q) (if δ_n < min(q, 1 − q) then
   PIP_j > q exactly on S₀); E max_j|PIP_j − 1{j ∈ S₀}| ≤ Eδ_n ([SL]/[P3] (ii)). All O(r_n).
2. **Sharpness.** With [LB] (1 ≤ s₀ < p, s₀ + 1 ≤ K): E δ_n ≥ (1 + √(n+1))⁻¹. So E δ_n is of order between n^{−1/2} and
   √(log n/n): the brief's target O(n^{−q/2}), q < 1, is exceeded, and q = 1 (up to √log n) is attained. Where the
   √(log n) comes from: only the superset sum (truncated χ² moments, [P3] `lem:chi`(b)); the size tail is O(n^{−1/2}).
3. Numerics (`../numerics/post2_checks_out.txt` N5, 20 seeds): mean δ_n√n ∈ [2.0, 6.1] for n = 100 … 25600 — compatible;
   not evidence of a constant.
4. Lemma C2 is itself an expectation version of Lemma 1a with the exact determinant: E π(|S| > m) ≤ C R_m√(D_{S₀})√n + O(1/n),
   under (E), (F₀) (exact reference S₀). Its extension to approximate references (Claim B) is not claimed in expectation.
