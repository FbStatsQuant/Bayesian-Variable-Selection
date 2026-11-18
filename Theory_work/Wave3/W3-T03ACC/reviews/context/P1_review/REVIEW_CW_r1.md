# Review CW round 1 (Opus 5.5 xhigh, Claude Work, delegate_task clientRequestId T01T02-review-CW-r1) — findings and verdict, copied from the reviewer's reply

Scope stated by the reviewer: checked every step by hand from PROOF_v1.tex, spot-checked PDF pp. 1–3 and 9–11; read only the packet; wrote only the plan-mode plan file outside packet and project. Part-by-part checks of T01(i)–(iv), (T)(a), (T)(b1), (T)(b2), T02(i), T02(ii), each "Verified".

## Findings

**F1** — §6, Theorem 6.1 (tex l.260) and proof (l.264). Exposition. The theorem limits the consequence clause to deterministic events E_n and rates ε_n; STATEMENT (T)(a) says no such thing. The O_P half is never spelled out. Evidence: the first inequality is pointwise, so P₀(Π(E_n|y) > κ²x) ≤ P₀(𝓑_n^c) + P₀(I/Z > x) holds for data-dependent E_n (if measurable); for O_P take x = Lε_n.

**F2** — §7, Lemma 7.2 (l.332–334). Exposition. C_Ω contains φ₀, undefined under R when s₀ = 0; then R_n = 0 and E₀Ω_n ≤ 1/√2 + 1/2.

**F3** — §2, Lemma 2.3(d) (l.107). Exposition. Uses that inversion reverses the Loewner order, not in the preamble's list of elementary facts. Standard: 0 ≺ P ⪯ Q ⇒ P^{-1/2}QP^{-1/2} ⪰ I ⇒ Q⁻¹ ⪯ P⁻¹.

**F4** — throughout. Exposition. Symbol reuse: B_n vs 𝓑_n; ε_n (Thm 6.1 vs Lemma 8.3); θ_n vs θ; π_k vs π; γ (Thm 6.2 vs Lemma 2.3(c)); β constant vs coefficient; M smoother vs constant; A matrix vs exponent vs A_n; Ω_n vs Ω.

**F5** — §§5–8. Exposition. The proof never says the input is valid P₀-a.s. under G (Cy^r = μ + Cε, Cε non-degenerate on 1^⊥, so P₀(Cy^r = 0) = 0).

**F6** — tex l.45. Exposition. Single `\` in `gathered`; display (1) prints on one line; content unaffected.

**Verdict: verified**
