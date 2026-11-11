# W3-POST2 — PLAN (v1.0, 2026-11-09)

Proof route per claim (each a diff against the locked chain [P1] → [P3] → [T03R]; changed steps written in full,
unchanged steps cited by label):

- **A1** (`lemmas/A_occam.md`): (F_w) enters [T03R] only through Lemma B(B1) — full rank of S₀ ∪ J and the determinant
  ratio — used in (C2)/(G3), (C4), (C5), T02(ii♯). Replace: (G3) by rank domination ([P3] `lem:chi`(a) last claim);
  (C4) without the determinant bound; Υ_n with the exact weights (D_{S₀}/D_{S₀∪J})^{1/2}; the truncated moment
  E[e^{χ²_d/2}1{χ²_d ≤ τ_j}] = (τ_j/2)^{d/2}/Γ(d/2+1) bounded for d ≤ j; (C5)(b) and (C8) then read off (OS). 5(a) via
  [P3] Step 0 + prop:sup (no (F_λ)). Implications F_w ⇒ DG ⇒ ADG ⇒ OS.
- **A2**: the [LB] argument summed over all supersets (fit factor ≥ 1 by [P1] `lem:spec`(d)).
- **B** (`lemmas/B_tail_approx.md`): [L1a′] with ϑ not an exact representation: Q^c_T ≤ σ*²E′ + 2|εᵀr| + B; the
  [P1] `lem:den` integral argument needs only a nonnegative excess; keep D_T^{−1/2}. Check that [P1] `thm:T01iii`,
  `lem:num`, `thm:Ta` hold for an arbitrary centred mean (G′).
- **C** (`lemmas/C_expectation.md`): decompose δ_n as in [P3] §main; tail term by E min(1, a e^Λ Z) ≤ a e^λ + P(Λ > λ)
  with the χ² tail of Λ (deterministic ρ via [L1a′]); other terms have expectation O(r_n) on 𝒢_n; P(𝒢_nᶜ ∪ 𝓑_nᶜ) = O(1/n).
- **D** (`lemmas/D_hellinger.md`): Π(bad | y) ≤ Π(Ω∖𝒮_n | y) + max_{S∈𝒮_n} Π(bad | S, y) with 𝒮_n = {S₀} (D(a)) or
  {S₀} ∪ {underfits with |S∖S₀| ≤ j₀, Δ_S < L*σ*² log n} (D(b)); conditional Gaussian/IG computations; the mass of
  the rest by [P3] lem:signalgain/assemble and A1.
- **E** (`lemmas/E_visibility.md`): replace [P3] lem:SvsSp(b)/signal/signalgain by a floor-free comparison of S with
  S′ = S ∪ S₀: Q^c_{S′} ≤ Q^c_{S₀} ≤ ‖(I − P_{S₀})e‖² + R_n (floor on S₀ only), Q^c_S ≥ ‖(I − P_S)y_c‖²; noise terms on
  𝒢_n and a union-bound event for the cross terms; then [P3] lem:assemble with A1's Υ_n.

Pipeline (PROTOCOL Wave3 + Wave1/1C/2): statement lock (gpt-6.1-sol high) → sharpness gate (ASSUMPTION_MAP.md,
boundary-violation numerics `numerics/`, "better theorem" review gpt-6-astra high) → lemma files + falsification
numerics + cross-family line checks (gpt-6.1-sol high) → mid-point (gpt-6-astra high, fresh) → exhaustive sweep
(gpt-6.1-sol high) → citation check → council (gpt-6-astra high + Opus 5.5 high claudeAgent), ≤ 3 rounds.
Compute local only (exact enumeration p ≤ 10, ≤ 20 seeds).
