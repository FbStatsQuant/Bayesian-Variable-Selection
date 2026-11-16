# AE — Proposition A-E and Corollaries A1-E, A2-E (W3-PSHARP-R, claim `W3-PSHARP-R:AE`)

Status: **PROVED (by this seat, unchecked)**. Repair [L02-S1] (Lemma F starting index; §4, §5 indices) after line check
L02 (`../reviews/L02_line_check_sol.md`, `../reviews/L02_disposition.md`). Statement: `../STATEMENT.md` v1.1 §2 (notation, Setting-E, (W-orth-E),
(W-sph-E)), §3.1–§3.3. PARENT := `Theory_work/Wave3/W3-PSHARP/`; "P-A :a-b" := PARENT `lemmas/A_log_factor.md` lines
a-b; "P-S" := PARENT `lemmas/S_one_step.md`; "P-ST :a" := PARENT `STATEMENT.md` line a.
Consumed, unchanged: Lemma S(4) and Lemma V (`W3-PSHARP:S`@1.0.0, P-ST :32-44; P-S); from the proof of
`W3-PSHARP:A`@1.0.0: P-A :26-37 (sphere density bounds), :53-63 ((W-orth) identities and the bound on V), :75-99
((W-sph) scores, their law, the bound on κ′_n); Corollary B (B1), P-ST :99 (`W3-PSHARP:B`@1.0.0), in §8 only.
Standard facts used: Chebyshev's inequality; independence of uncorrelated jointly Gaussian vectors.

Throughout: odds := δ_n/(1 − δ_n) (finite, since π(S₀) > 0); c_n, ℓ_n, Λ^E_n as in STATEMENT §2; N := N_n ≥ 1.
Note c_n = P_n n^{−1/2} with P_n := (s₀ + 1)/(2p − 1 − s₀), the factor in Lemma S(4).

## 1. Lemma T (truncated expectation inequality)
Let δ ∈ [0, 1), odds := δ/(1 − δ), and suppose odds ≥ Y := c e^{−e} Σ_{j=1}^N U_j 1_{G_j}, where c > 0, e ≥ 0, T > 0 are
deterministic, G_1, …, G_N are events, and U_1, …, U_N are random variables with (a) U_1, …, U_N iid, (b) 0 ≤ U_j ≤ T,
(c) U_j independent of G_j for each j. Put L := cN E U_1. Then
  E δ ≥ L·( e^{−e} min_j P(G_j) − cT − L ).
*Proof.* x ↦ x/(1 + x) is increasing on [0, ∞) and δ = odds/(1 + odds), so δ ≥ Y/(1 + Y) ≥ Y − Y² (because
x − x/(1 + x) = x²/(1 + x) ≤ x² for x ≥ 0). By (c), E Y = c e^{−e} E U_1 Σ_j P(G_j) ≥ e^{−e} min_j P(G_j)·L. Since e ≥ 0
and indicators are ≤ 1, Y² ≤ c²(Σ_j U_j)², and by (a), (b) (U_j² ≤ T U_j; E U_jU_k = (E U_1)² for j ≠ k):
E(Σ_j U_j)² ≤ N T E U_1 + N(N − 1)(E U_1)² ≤ N T E U_1 + N²(E U_1)². Hence E Y² ≤ cT·L + L², and
E δ ≥ E Y − E Y² gives the claim. ∎
(Only independence of each U_j from its own G_j, and of the U_j among themselves, is used.)

## 2. Truncated means
Let T ≥ 1.
**(i) Gaussian.** Z ~ N(0, 1), U := e^{Z²/2}1{Z² ≤ 2 log T}: E U = ∫_{|z|≤√(2 log T)} (2π)^{−1/2} dz = 2√(log T/π)
**exactly** (the computation of P-A :23 with τ replaced by 2 log T).
**(ii) Sphere.** d ≥ 3, ω uniform on the unit sphere of ℝ^d, ζ := dω₁², U := e^{ζ/2}1{ζ ≤ 2 log T}. If 2 log T ≤ d/2:
  2√(log T/π)·(1 − 1/d)·e^{−2(log T)²/d} ≤ E U ≤ 2√(log T/π)·e^{3 log T/d}.
*Proof.* Put τ := 2 log T ≤ d/2 and t := √d ω₁ with density h_d (P-A :27). P-A :30-37 (which use only t² ≤ τ ≤ d/2) give
c_d√(2π) ∈ [(d − 1)/d, √((d − 1)/d)] ⊆ [1 − 1/d, 1] and c_d e^{−τ²/(2d)} ≤ e^{t²/2}h_d(t) ≤ c_d e^{3τ/(2d)} on |t| ≤ √τ.
Integrating over |t| ≤ √τ: E U ∈ [2√τ c_d e^{−τ²/(2d)}, 2√τ c_d e^{3τ/(2d)}], and 2√τ c_d ∈ [(1 − 1/d), 1]·2√(log T/π)
(2√τ/√(2π) = 2√(log T/π)); finally τ²/(2d) = 2(log T)²/d and 3τ/(2d) = 3 log T/d. ∎

## 3. Truncation level, and the assembly step
Fix ϵ ∈ (0, 1), put α := ϵ/4 and **T := α/c_n**. Since 1/c_n = [p√n/(s₀ + 1)]·[(2p − 1 − s₀)/p] and
(2p − 1 − s₀)/p ∈ [1, 2) (because s₀ + 1 ≤ K ≤ p):
  log T = ℓ_n + log(α(2p − 1 − s₀)/p) ∈ [ℓ_n − log(4/ϵ), ℓ_n]   (α < 2α < ½).                                      (3.1)
Also ℓ_n ≥ ½ log n (s₀ + 1 ≤ p), and ℓ_n ≤ log p + ½ log n. Hence T ≥ 1 for n ≥ (4/ϵ)², and
  a_n := √(1 − 2 log(4/ϵ)/log n) ≤ √(log T/ℓ_n) ≤ 1   (n > (4/ϵ)²).                                               (3.2)
Since 2c_nN√(ℓ_n/π) = Λ^E_n: **2c_nN√(log T/π) = Λ^E_n·√(log T/ℓ_n) ∈ [a_nΛ^E_n, Λ^E_n]**, and c_nT = α.

**Lemma F (assembly).** Suppose that for n ≥ n₁, where n₁ depends only on (ϵ, 𝔭) [L02-S1],
  E δ_n ≥ L_n(b_n − α − L_n),  L_n = θ_nΛ^E_n,  θ_n ∈ [θ⁻_n, θ⁺_n] ⊆ (0, 2],  b_n ≤ 1,
where θ^±_n → 1 and b_n → 1 at rates that depend only on (n, ϵ) and a set of parameters 𝔭. Then there is n₀ depending
only on (ϵ, 𝔭) with E δ_n ≥ (1 − ϵ − Λ^E_n)Λ^E_n for n ≥ n₀.
*Proof.* Write Λ := Λ^E_n. If Λ ≥ 1 − ϵ the right side is ≤ 0 ≤ E δ_n. Otherwise Λ < 1 and
L(b − α − L) − Λ(1 − ϵ − Λ) = Λ[(θb − 1) + (ϵ − θα) + Λ(1 − θ²)] ≥ Λ[ϵ/2 − |θb − 1| − |1 − θ²|], using θ ≤ 2,
α = ϵ/4. As |θb − 1| ≤ |θ − 1| + 2|1 − b| and |1 − θ²| ≤ 3|1 − θ|, the bracket is ≥ 0 once
max(|θ⁻_n − 1|, |θ⁺_n − 1|) ≤ ϵ/16 and 1 − b_n ≤ ϵ/16, which holds for n ≥ n_rates(ϵ, 𝔭). Take
n₀ := max(n₁, n_rates) [L02-S1]. ∎

## 4. Proof under (W-orth-E)
**Setup (P-A :53-63, unchanged; these lines use (G), (E), (C), (W-orth) and n ≥ 3 only, not N → ∞).** u_j :=
x_j/√(n − 1), g_j := u_jᵀε/σ*, j ∈ 𝒩_n: iid N(0, 1). For j ∈ 𝒩_n: νγ_j = κ_n g_j²/2 with κ_n ≥ (n − 1)σ*²/V and
  V ≤ σ*²E(1 + 0.04/(n − 1)) + 1.06M + M′,  E := ‖Cε‖²/σ*²   (P-A :58-63).
**Decoupling.** Fix j. u_j is a unit vector of 1^⊥, so C = u_ju_jᵀ + P_j with P_j := C − u_ju_jᵀ the orthogonal projection
of rank n − 2 onto 1^⊥ ∩ u_j^⊥. Then E = g_j² + R_j, R_j := ‖P_jε‖²/σ*². The Gaussian vectors u_jᵀε and P_jε are
uncorrelated (P_ju_j = 0), hence independent: **R_j ~ χ²_{n−2} is independent of g_j.** (R_j involves the other scores;
this does not matter, see Lemma T(c).)
**Events.** For x ≥ 1 let G_j := {R_j ≤ (n − 2) + x√(2(n − 2))}; by Chebyshev (Var R_j = 2(n − 2)) P(G_jᶜ) ≤ x⁻². Let
U_j := e^{g_j²/2}1{g_j² ≤ 2 log T}. On G_j ∩ {g_j² ≤ 2 log T}: E ≤ (n − 1)(1 + x√(2/(n − 1)) + 2 log T/(n − 1)), so
V/(σ*²(n − 1)) ≤ 1 + e_n with
  e_n := 1.02·(x√(2/(n − 1)) + 2 log T/(n − 1)) + (0.04 + (1.06M + M′)/σ*²)/(n − 1)
(using (1 + a)(1 + b) − 1 ≤ 1.02a + b for a ≥ 0, 0 ≤ b := 0.04/(n − 1) ≤ 0.02). Hence κ_n ≥ 1/(1 + e_n) ≥ 1 − e_n and
νγ_j ≥ (1 − e_n)g_j²/2 ≥ g_j²/2 − e_n log T. So e^{νγ_j} ≥ e^{−e_n log T}U_j on G_j, and trivially e^{νγ_j} ≥ 0 elsewhere:
  e^{νγ_j} ≥ e^{−e_n log T}·U_j1_{G_j}   for every j ∈ 𝒩_n.
**Application.** Lemma S(4) with 𝒩 = 𝒩_n: odds ≥ c_n Σ_{j∈𝒩_n} e^{νγ_j} ≥ Y := c_n e^{−e_n log T} Σ_j U_j1_{G_j}. The
hypotheses of Lemma T hold: U_j = f(g_j) iid, 0 ≤ U_j ≤ T, U_j a function of g_j and G_j of R_j. With §2(i) and §3:
  E δ_n ≥ L_n( e^{−e_n log T}(1 − x⁻²) − α − L_n ),  L_n = 2c_nN√(log T/π) = θ_nΛ^E_n,  θ_n ∈ [a_n, 1].
**Rates.** Let ω_n → 0 be the sequence of (W-orth-E): (log p)² ≤ ω_n n. Then log T ≤ ℓ_n ≤ √(ω_n n) + ½ log n, so
log T/√n ≤ ψ_n := √ω_n + log n/(2√n) → 0. Take x = x_n := ψ_n^{−1/2} (≥ 1 when ψ_n ≤ 1). Then
e_n log T ≤ 1.02(√2·x_n log T/√(n − 1) + 2(log T)²/(n − 1)) + (0.04 + (1.06M + M′)/σ*²) log T/(n − 1)
≤ C(ψ_n^{1/2} + ψ_n² + (1 + (M + M′)/σ*²)ψ_n/√n) with an absolute C (n ≥ 3, n/(n − 1) ≤ 3/2). So
b_n := e^{−e_n log T}(1 − ψ_n) → 1 and θ⁻_n = a_n → 1 at rates depending only on (n, ϵ, ω_n, (M + M′)/σ*²). Lemma F
gives n₀ = n₀(ϵ, (M + M′)/σ*², (ω_n)) with E δ_n ≥ (1 − ϵ − Λ^E_n)Λ^E_n for n ≥ n₀; here the starting index of the
displayed inequality is n₁ := the least n with n ≥ 3, n > (4/ϵ)² and ψ_n ≤ 1, a function of (ϵ, (ω_n)) only [L02-S1]. ∎

## 5. Proof under (W-sph-E)
**Setup (P-A :75-99, unchanged).** X_{S₀}, θ* deterministic; ρ̃ := ρ̃_{S₀} ≠ 0 is a function of ε; for j ∈ 𝒩_n,
ζ_j := (n − 1)⟨ω_j, ρ̃/‖ρ̃‖⟩² and νγ_j ≥ κ′_nζ_j/2 (P-A :79-81). Conditionally on ε the ζ_j, j ∈ 𝒩_n, are iid with the law
of dω₁², d := n − 1, and this conditional law does not depend on ε (P-A :82-85; the ω_j are iid uniform and independent of
ε, so given ε their projections on the fixed unit vector ρ̃/‖ρ̃‖ are iid). Hence **the vector (ζ_j)_{j∈𝒩_n} is independent
of ε** (for bounded f, g: E[f(ζ)g(ε)] = E[g(ε)·E(f(ζ) | ε)] = E g(ε)·∫ f dμ^{⊗N}) and has iid coordinates.
**Event (P-A :95-99).** With E₁, E₂, E = E₁ + E₂, m := n − 1 − r₀ ≥ n/2 as there, and x ≥ 1, the ε-measurable event
G := {E ≤ 2(n − 1)} ∩ {E₂ ≥ m/2} ∩ {E₁ ≤ x(r₀ + 1)} has P(Gᶜ) ≤ 2/(n − 1) + 16/n + 1/x, and on G
  1 − κ′_n ≤ e′_n := (C₀ + 2x(r₀ + 1))/n,  C₀ := 4(1.02(3M + 4σ*²) + 2M′)/σ*².
**Comparison.** U_j := e^{ζ_j/2}1{ζ_j ≤ 2 log T}. On G ∩ {ζ_j ≤ 2 log T}: κ′_nζ_j/2 ≥ ζ_j/2 − (1 − κ′_n)₊ζ_j/2 ≥
ζ_j/2 − e′_n log T, so e^{νγ_j} ≥ e^{−e′_n log T}U_j1_G for every j ∈ 𝒩_n. Lemma S(4): odds ≥ Y :=
c_n e^{−e′_n log T}Σ_j U_j1_G. Lemma T applies with G_j := G: the U_j are iid functions of the ζ_j, 0 ≤ U_j ≤ T, and each
U_j is independent of G (ε-measurable). With §2(ii) (when 2 log T ≤ (n − 1)/2) and §3:
  E δ_n ≥ L_n( e^{−e′_n log T}P(G) − α − L_n ),  L_n = c_nN E U_1 = θ_nΛ^E_n,
  θ_n ∈ [a_n(1 − 1/(n − 1))e^{−2(log T)²/(n−1)}, e^{3 log T/(n−1)}].
**Rates.** Let ω_n, ω′_n → 0 be the sequences of (W-sph-E): (log p)² ≤ ω_n n, (r₀ + 1) log(pn) ≤ ω′_n n. As in §4,
log T/√n ≤ ψ_n → 0, so 2 log T ≤ (n − 1)/2 eventually and θ^±_n → 1 at rates depending on (n, ϵ, ω_n). Since
log T ≤ log p + ½ log n ≤ log(pn): e′_n log T ≤ C₀ψ_n/√n + 2x ω′_n. Take x = x_n := (ω′_n)^{−1/2} (ω′_n ≥ log(pn)/n > 0; x_n ≥ 1
once ω′_n ≤ 1): e′_n log T ≤ C₀ψ_n/√n + 2(ω′_n)^{1/2} → 0, and
b_n := e^{−e′_n log T}(1 − 2/(n − 1) − 16/n − (ω′_n)^{1/2}) → 1 at rates depending on (n, C₀, ω_n, ω′_n), and b_n ≤ 1.
Lemma F — with n₁ := the least n with n ≥ 4 (so d = n − 1 ≥ 3), n > (4/ϵ)², ψ_n ≤ ¼ (so 2 log T ≤ √n/2 ≤ (n − 1)/2)
and ω′_n ≤ 1, a function of (ϵ, (ω_n), (ω′_n)) only [L02-S1] — gives n₀ = n₀(ϵ, C₀, (ω_n), (ω′_n)) — C₀ is a function of
(σ*², M, M′) — with E δ_n ≥ (1 − ϵ − Λ^E_n)Λ^E_n for
n ≥ n₀. ∎

## 6. Uniformity, random (X_{S₀}, θ*), and the limit form
**Uniformity.** In §4–§5 the bound on E δ_n involves the problem only through (n, ϵ, σ*², M, M′) and the sequences
(ω_n), resp. (ω_n, ω′_n), and Λ^E_n itself; N_n enters only through Λ^E_n. This is the uniformity of STATEMENT §3.1.
**Random (X_{S₀}, θ*).** Suppose that, conditionally on (X_{S₀}, θ*), the hypotheses hold on an event 𝒜_n measurable in
(X_{S₀}, θ*) (ε ~ N_n(0, σ*²I) and the null-block structure conditionally, with the same constants and sequences), S₀, p
and 𝒩_n deterministic, so Λ^E_n is deterministic. By uniformity, E[δ_n | X_{S₀}, θ*] ≥ (1 − ϵ − Λ^E_n)Λ^E_n on 𝒜_n for
n ≥ n₀. If 1 − ϵ − Λ^E_n ≥ 0: E δ_n ≥ E[1_{𝒜_n}E(δ_n | X_{S₀}, θ*)] ≥ P(𝒜_n)(1 − ϵ − Λ^E_n)Λ^E_n (δ_n ≥ 0); otherwise the
right side is ≤ 0 ≤ E δ_n. (As in P-A :109-112.)
**Limit form.** Λ^E_n > 0 (N_n ≥ 1). If Λ^E_n → 0 (and P(𝒜_n) → 1 in the random case), then for every ϵ,
liminf E δ_n/Λ^E_n ≥ 1 − ϵ; hence liminf E δ_n/Λ^E_n ≥ 1. This proves Proposition A-E. ∎

## 7. Corollary A1-E
s₀ fixed, 𝒩_n = [p]∖S₀, N_n = p − s₀ ≥ 1. Under (W-orth) the vectors u_j, j ∈ 𝒩_n, are orthonormal in
1^⊥ ∩ (col X_{S₀})^⊥, of dimension n − 1 − r₀ (P-ST :55), so p ≤ n − 1 + s₀ ≤ 2n and (log p)² ≤ (log 2n)² = o(n):
(W-orth-E) holds with ω_n := (log 2n)²/n. Under (W-sph-E) there is nothing to check. In both cases Proposition A-E
applies, and Λ^E_n → 0: 2N_n/(2p − 1 − s₀) ≤ 2 and ℓ_n ≤ log p + ½ log n = o(n). With N_n = p − s₀ the displayed
denominator of Cor A1-E is Λ^E_n, so liminf E δ_n/Λ^E_n ≥ 1 is the main display.
(a) If p → ∞, 2(p − s₀)/(2p − 1 − s₀) → 1, which gives the first display of (a). If p = ⌊n^a⌋ (a > 0), resp.
p = min(n − 1, ⌊n^a⌋) (0 < a ≤ 1), then log p = a log n + O(1), so ℓ_n = (a + ½) log n + O(1) and
√(ℓ_n/(πn)) = (1 + o(1))√((a + ½)/π)·r_n. (For (W-sph-E) with p = ⌊n^a⌋: (log p)² = O((log n)²) = o(n).)
(b) If p is fixed, ℓ_n = ½ log n + log(p/(s₀ + 1)), so √(ℓ_n/(πn)) = (1 + o(1))r_n/√(2π). ∎

## 8. Corollary A2-E
Hypotheses: Setting-E, 𝒩_n = [p]∖S₀, s₀ ≤ p/2, and (W-orth-E), or the spherical structure of (W-sph-E) with
(log p)² = o(n) (no rank condition).
**Facts.** (F1) (s₀ + 1)/(2p − 1 − s₀) ≤ 1, since s₀ ≤ p/2 ≤ p − 1 (p ≥ 2). (F2) ½ ≤ 2N_n/(2p − 1 − s₀) ≤ 2, since
2N_n = 2(p − s₀) ≥ p, 2p − 1 − s₀ ≤ 2p, and 2(p − s₀) ≤ 2(2p − 1 − s₀) (p ≥ 1). (F3) ℓ_n ≤ log p + ½ log n = o(√n).
**Step 0 (rank condition).** Both (i) and (ii) assume E δ_n → 0 (in (ii), O(r_n) → 0). Since s₀ ≤ min(K − 1, p/2),
PARENT (B1) (P-ST :99) gives π(S₀) ≤ [1 + (s₀ + 1)/(3√n)]⁻¹ surely, i.e. δ_n ≥ (s₀ + 1)/(3√n + s₀ + 1); so E δ_n → 0
forces (s₀ + 1)/√n → 0. Then (r₀ + 1) log(pn) ≤ (s₀ + 1)(log p + log n) = n·[(s₀ + 1)/√n]·[(log p + log n)/√n] = o(n)
by (F3). So, along the sequence, (W-sph-E) holds with its rank condition, and Proposition A-E is available in both cases.
**Step 1 (sub-blocks).** Put Δ_n := 2c_n√(ℓ_n/π), the contribution of one column to Λ^E_n; by (F1), Δ_n ≤ 2√(ℓ_n/(πn)) → 0
by (F3). For 1 ≤ k ≤ N_n let 𝒩^{(k)} ⊆ 𝒩_n consist of any k columns. The witness hypotheses hold for 𝒩^{(k)} (a subfamily of
an orthonormal family, resp. of an iid uniform family independent of ε; the growth conditions involve p, not the block),
and Λ^E for 𝒩^{(k)} equals kΔ_n. Proposition A-E with ϵ = ½ (its n₀ does not depend on the block) gives, for n ≥ n₀ and
every such k, E δ_n ≥ (½ − kΔ_n)kΔ_n. Let λ*_n := min(Λ^E_n, ¼) and k*_n := ⌊λ*_n/Δ_n⌋ ≤ N_n. If k*_n ≥ 1, then
k*_nΔ_n ∈ (λ*_n − Δ_n, λ*_n] ⊆ (λ*_n − Δ_n, ¼], so E δ_n ≥ ¼(λ*_n − Δ_n). If k*_n = 0, then λ*_n < Δ_n and
¼(λ*_n − Δ_n) < 0 ≤ E δ_n. Thus
  E δ_n ≥ ¼( min(Λ^E_n, ¼) − Δ_n )   (n ≥ n₀).
**(i)** If E δ_n → 0, then min(Λ^E_n, ¼) ≤ 4E δ_n + Δ_n → 0, so Λ^E_n → 0, which by (F2) is equivalent to
(s₀ + 1)√(ℓ_n/n) → 0.
**(ii)** If E δ_n = O(r_n), then E δ_n → 0, so Λ^E_n → 0 by (i), and Proposition A-E (limit form) gives
liminf E δ_n/Λ^E_n ≥ 1, so Λ^E_n ≤ 2E δ_n = O(r_n) for n large. By (F2) and ℓ_n ≥ ½ log n,
Λ^E_n ≥ ½(s₀ + 1)√(log n/(2πn)) = (s₀ + 1)r_n/(2√(2π)). Hence s₀ + 1 = O(1). ∎

## 9. Remarks
1. **Where the √(log n) comes from at bounded N.** For one null column, E δ_n is at least about
   E min(c_n e^{Z²/2}, 1) ≈ c_n·2√(log(1/c_n)/π): the truncated mean of e^{Z²/2} grows like the square root of the log of
   the truncation level, and the level 1/c_n ≈ p√n/(s₀ + 1) carries the extra ½ log n. In probability, a bounded number of
   e^{χ²₁/2} terms is O_P(1) (PARENT `ASSUMPTION_MAP.md:15`); the effect is a tail effect only.
2. **Numerics.** `../numerics/ae_fixed_p.py` (exact orthogonal design, p ∈ {2, 3, 5} fixed, n ≤ 10⁶, importance sampling):
   E δ_n/Λ^E_n = 0.99–1.03 at n = 10⁶ (`../numerics/ae_fixed_p_out.txt`). An observation only; no upper bound is claimed.
