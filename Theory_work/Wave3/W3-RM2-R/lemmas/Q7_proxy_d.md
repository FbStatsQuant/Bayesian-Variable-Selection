# Q7 — Ex-Proxy-d: one truth with n^b weak proxies and a decaying signal (claim W3-RM2-R:Ex-Proxy-d; STATEMENT (C5⁺))

Status: **PROVED (by this seat, unchecked)** — 2026-11-16, lead Claude Opus 5.5. Ticket W3-RM2-R; statement:
`../STATEMENT.md` v1.0 §5. New file. It re-uses the verification of PARENT example E4
(`Theory_work/Wave3/W3-RM2/lemmas/L6_examples.md:330-384`, claim W3-RM2:Ex-Proxy@1.0.0, "PROVED-CHECKED, conditional on
SOP:TH09; …"), citing each step that does not involve the signal size, and re-proves the steps that do.
PARENT := `Theory_work/Wave3/W3-RM2/`.

## 0. The design (PARENT `lemmas/L6_examples.md:334-347`)

Fix 0 < b < ½, C₀ ∈ (0, ∞), σ² > 0. p = ⌊n/3⌋, q = ⌊n^b⌋, r² = C₀ log n/n, s := √(1 − r²); e₁, …, e_p centred orthonormal
vectors of ℝⁿ; z₁ = e₁, z_j = r e₁ + s e_j (2 ≤ j ≤ q), z_j = e_j (j > q); x_j = √(n − 1) z_j; Q = {1, …, q}, S₀ = {1};
μ = θ_n x₁ with a deterministic θ_n ≠ 0, |θ_n| ≤ θ_hi (θ_hi fixed). For large n: 0 < r < 1, q ≤ p, φ₀² = ½ is a global
Gram floor, A = 1 (p ≤ n), and ‖μ‖² = θ_n²(n − 1) ≤ Mn with M := θ_hi² + 1. (PARENT E4 is the case θ_n ≡ θ.)
λ_n := (n − 1)φ₀²θ_n²/σ² = (n − 1)θ_n²/(2σ²). Noise g ~ N(0, I_n); g_k := e_kᵀg are iid N(0, 1) (orthonormality).

## 1. Part (a): the truth-removal width is bounded

**Lemma P1 (truth-removal directions).** Every v ∈ 𝒟ᵀ_n has the form
  u_P := (s e₁ − r Σ_{j∈P} e_j)/√(s² + r²|P|)
for some P ⊆ {2, …, q}.
*Proof.* 𝒟ᵀ_n = {u_{A,1} : T ∈ 𝓛, A = T ∖ {1} or A = (T ∖ {1}) ∪ {l}, l ∈ [p] ∖ T} (S₀ = {1}; PARENT
`lemmas/L2_width.md:184`). T ⊆ Q, so T ∖ {1} ⊆ {2, …, q}; l ∉ T, l ≠ 1. If l ∈ Q, A ⊆ {2, …, q}. If l > q, x_l = √(n−1)e_l is
orthogonal to e₁ and to every e_j, j ≤ q, hence to x₁ and to span X_{A∖{l}}; so (I − P_A)x₁ = (I − P_{A∖{l}})x₁ and
u_{A,1} = u_{A∖{l},1} with A ∖ {l} ⊆ {2, …, q}. It remains to compute u_{P,1} for P ⊆ {2, …, q}, t := |P|. Put
w := s e₁ − r Σ_{j∈P} e_j. (i) w ⊥ z_k for k ∈ P: z_kᵀw = r·s + s·(−r) = 0. (ii) e₁ − c w ∈ span{z_j : j ∈ P} for
c := 1/(s + tr²/s): since Σ_{j∈P} z_j = t r e₁ + s Σ_{j∈P} e_j, we have Σ_{j∈P} e_j = (Σ_{j∈P} z_j − t r e₁)/s, so
w = (s + t r²/s)e₁ − (r/s)Σ_{j∈P} z_j, i.e. e₁ = c w + (cr/s)Σ_{j∈P} z_j. By (i)–(ii), (I − P_P)e₁ = c w ≠ 0, and
u_{P,1} = w/‖w‖ with ‖w‖² = s² + r²t (orthonormality). For P = ∅, u_∅ = e₁. ∎

**Lemma P2 (part (a)).** d_n ≤ √(2/π)(1 + r(q − 1))/s. Since r q ≤ √C₀ n^{b−½}√(log n) → 0 (b < ½) and s → 1,
d_n ≤ √(2/π) + o(1); in particular d_n = O(1).
*Proof.* For every P, |u_Pᵀg| ≤ (s|g₁| + r Σ_{j∈P}|g_j|)/√(s² + r²|P|) ≤ (|g₁| + r Σ_{j=2}^{q}|g_j|)/s (numerator: s ≤ 1 and
P ⊆ {2, …, q}; denominator ≥ s). So max_{v∈𝒟ᵀ_n}|vᵀg| ≤ (|g₁| + r Σ_{j=2}^{q}|g_j|)/s, and E|g_k| = √(2/π). ∎

## 2. Part (b): RM2-F (PARENT v1.4) with a decaying signal

Assume nθ_n²/log n → ∞. The hypotheses of RM2-F (PARENT `STATEMENT.md:206-207`): (T1-F), (FL), (V), (L^b) with
b < β(η, A), (BM-W), (W).
* **Not involving θ_n — cited from PARENT E4 verbatim** (`lemmas/L6_examples.md:340-357, 369-383`): the global Gram floor
  ½ (so (FL-16), (FL-Q), SE_λ(j₀), SE_w(m♯_n; g₀) with g₀ = 1, A = 1, φ₀² = ½); (L-size^b), (L-feas) (K = p ≥ 2q + 33
  eventually); (L-gain) with η = 0 — for l > q, x_l ⊥ every other column, so u_{U,l}ᵀμ = θ_n u_{U,l}ᵀx₁ = 0 for every U ∌ l,
  whatever θ_n; b < β(0, 1) = ½; (W) through (W-loc) with N_l = {1} (2 ≤ l ≤ q), N_l = ∅ otherwise, L_n = η_n = 0,
  ν_n = 1 — a statement about X and Q only. (Each of these steps uses only X, Q, S₀; the fixed θ of E4 enters none.)
* **Energy:** ‖μ‖² ≤ Mn with M = θ_hi² + 1 (§0). Fixed s₀ = 1, p ≤ n, s₀ ≤ K eventually: the remaining R1/R clauses of (H0).
* **BM-∞:** θ_n² nφ₀²/(σ² log n) = nθ_n²/(2σ² log n) → ∞.
* **(V):** for U ∌ 1, |U| ≤ 15, at most 15 proxies lie in U and the outside columns are orthogonal to x₁ and to the
  proxies; by PARENT E4 (`L6_examples.md:359-367`), Var_G(1 | U) := ‖(I − P_U)x₁‖²/(n − 1) = (1 − r²)/(1 + (t − 1)r²) ≥ ½
  eventually (t ≤ 15 proxies in U; also from the floor), so δ²_{U,1} = θ_n²‖(I − P_U)x₁‖² ≥ θ_n²(n − 1)/2 =: M_n log n with
  M_n := θ_n²(n − 1)/(2 log n) → ∞ (deterministic).
* **(BM-W):** by Lemma P2, d_n² + log n ≤ log n + O(1), and λ_n = (n − 1)θ_n²/(2σ²), so λ_n/(d_n² + log n) → ∞.
* **(BM-Q) iff n^{1−b}θ_n² → ∞:** (BM-Q) is θ_n²nφ₀²/(σ²(q + log n)) → ∞ (PARENT `STATEMENT.md:138`); q + log n ~ n^b
  (q = ⌊n^b⌋, log n = o(n^b)), so (BM-Q) ⇔ nθ_n²/n^b → ∞.
* **Witness:** θ_n² := (log n)²/n (≤ θ_hi² for large n): nθ_n²/log n = log n → ∞, so (b) applies and (BM-W) holds; and
  n^{1−b}θ_n² = (log n)²/n^b → 0, so (BM-Q) fails. Hence (BM-W) is strictly weaker than (BM-Q) on a design satisfying
  every other hypothesis of RM2-F. ∎

## 3. Part (c): RM2-F-plus at the constant level

Let κ₀ := 2 max{c₀(1, 1), c_TL⁰, M_V⁰/σ²} with A = 1, s₀ = 1, M = θ_hi² + 1, C_R = 3(M + σ²) (STATEMENT §2:
M_V⁰ = (σ√2 + √(3C_R))², c_TL⁰ = 16 + 12C_R/σ², c₀(1, 1) = max{4C_*, 32·4}). Assume κ := liminf nθ_n²/(σ² log n) > κ₀ and
fix κ′ ∈ (κ₀, κ); then nθ_n² ≥ κ′σ² log n for n ≥ n₀. The hypotheses of RM2-F-plus (STATEMENT (C1⁺)): (T1-F♭), (FL),
(V♭), (L^b) with b < β(η, A), (BM-W⁺), (W).
* (FL), (L^b) with η = 0, (W), and the non-beta-min clauses of (T1-F♭): as in §2 (they do not involve θ_n).
* **BM(c) of (T1-F♭):** take c := κ′/2 > c₀(1, 1). θ_n² ≥ κ′σ² log n/n = cσ² log n/(nφ₀²) (φ₀² = ½).
* **(V♭):** δ²_{U,1} ≥ θ_n²(n − 1)/2 ≥ (κ′σ²/2)(1 − 1/n) log n; with M_V := (κ′σ²/2 + M_V⁰)/2 ∈ (M_V⁰, κ′σ²/2) (κ′σ²/2 > M_V⁰),
  δ²_{U,1} ≥ M_V log n for n ≥ n₀.
* **(BM-W⁺):** λ_n = (n − 1)θ_n²/(2σ²) ≥ (κ′/2)(1 − 1/n) log n. (ii): with c_TL := (κ′/2 + c_TL⁰)/2 ∈ (c_TL⁰, κ′/2),
  λ_n ≥ c_TL log n for n ≥ n₀. (i): by Lemma P2, d_n ≤ D₀ := 2√(2/π) for n ≥ n₀, so 4(d_n + √(2 log n))² ≤
  8 log n + 16D₀√(log n) + 4D₀² ≤ 9 log n for n ≥ n₀, while λ_n ≥ c_TL log n with c_TL > c_TL⁰ > 16 > 9; so
  √λ_n ≥ 2(d_n + √(2 log n)). ∎

## 4. Remarks

1. In (b), (BM-W) is BM-∞ on this design (d_n bounded), which is part of (T1-F) anyway; in (c), (BM-W⁺) is a BM(c)
   condition. The table of PARENT (C5) gains its first example where (BM-W) holds and (BM-Q) fails.
2. Conditionality: the claim is about the hypotheses only; any conclusion drawn from it through RM2-F / RM2-F-plus
   carries their condition (SOP:TH09).
3. C₀ > 0 is arbitrary and only enters r; with C₀ fixed, the bound of (a) holds for all large n.
