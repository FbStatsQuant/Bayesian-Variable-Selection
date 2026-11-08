# Theorem N1 (clause M1(b)): measured-endpoint identity for every bounded summary

Status: PROVED under the named premises of STATEMENT §2 — cross-family checked (Codex gpt-6.1-sol: LC1, MP1 CONTINUE, SW1, council C1 9.3) and council-passed (Claude Opus 5.5: C1 8.9), round 1, 2026-11-08. Inherits the premise statuses START/KERNEL (N9: PROVED (candidate), code-checked; CHK_INHERITED: VERIFIED WITH AMENDMENT) and T12 (PROVED-LOCKED). v3. Statement: STATEMENT.md v2 §3 (locked).

## Statement (verbatim from STATEMENT.md §3)

Under the premises of STATEMENT §2 (EX-A, EX-S/H-U, START, KERNEL, CAL, SI, MEAS, potential run; worker equivalence for
v3.1's concurrent workers), for every fixed index r ≥ 1, every q ∈ {1, …, 4} and every h as in §1 (jointly measurable in
(S, c), |h| ≤ B_h deterministic, fixed before stream 10), almost surely on 𝒜 ∩ {r ≤ R′}:

  (N1-q) E[Ẑ_r · (1/N_e)Σ_i h(S_{rqi}; 𝓒) | 𝓒] = Z · π(h(·; 𝓒));
  (N1)   E[Ẑ_r · H_r(h) | 𝓒] = Z · π(h(·; 𝓒)),   H_r(h) = (4N_e)^{-1} Σ_{q=1}^{4} Σ_{i=1}^{N_e} h(S_{rqi}; 𝓒).

In particular E[W_r | 𝓒] = 1 and E[W_r H_r(h) | 𝓒] = π(h) with W_r := Ẑ_r/Z. "Almost surely on E₀ := 𝒜 ∩ {r ≤ R′}" means
the localised form of Lemma F: E[1_{E₀}Y | 𝓒] = 1_{E₀}·(right side) a.s., Y the island-r integrand.

## Proof

By Lemma F, E[1_{E₀} Ẑ_r η_{rq}(h(·; 𝓒)) | 𝓒] = 1_{E₀}ψ_q(𝓒) a.s., with
ψ_q(c) = E[Ẑ(Φ(c, U)) η_q(Φ(c, U))(h(·; c))] for an iid U[0,1) sequence U. Fix c ∈ A₀ (the set with E₀ = {𝓒 ∈ A₀}). By
Lemma B, Φ(c, U) is a realisation of T12's frozen island I(c) with N = N_e(c), L′ = L(c), M = 4, flag unset, satisfying
(R1)–(R3), with Ẑ(Φ(c,U)) = Ẑ_T and η_q(Φ(c,U)) = q̂^{(L+q)} (B-a, B-c). The function f := h(·; c) : Ω → ℝ is fixed (c is
fixed). By Lemma P (T12 (i.b)), ψ_q(c) = E_c[Ẑ q̂^{(L+q)}(f)] = Zπ(f) = Zπ(h(·; c)). Hence the left side of (N1-q) equals
Zπ(h(·; 𝓒)) a.s. on E₀, i.e. E[1_{E₀} Ẑ_r η_{rq}(h) | 𝓒] = 1_{E₀} Zπ(h(·; 𝓒)) a.s. (N1) is the average of (N1-q) over q = 1..4 (linearity of conditional expectation; H_r(h) =
(1/4)Σ_q η_{rq}(h)). h ≡ 1 gives E[Ẑ_r | 𝓒] = Z. Dividing by the constant Z > 0 gives the W_r form. ∎

## Scope notes (what the proof does and does not give)

- Any admissible X (no regime or correlation assumption): only Ω finite, m > 0, ϖ > 0 are used (T12 §0).
- Any frozen grid on the success set; any N_e ≥ 1, L ≥ 0 (the production values are special cases).
- For r > 4 (stacking, R′ = 4k): the proof needs SI for stream 9 + r only; the IND-T extension audit (independence of
  streams 10..9+R′ among themselves, needed by clauses that pool islands) is not discharged here.
- Potential run: the identity is for the uninterrupted island record. Delivered records equal potential ones on 𝒪 under
  GUARD-W (audit open); nothing conditional on completion follows (CEX-guard), nor conditional on favourable final
  diagnostics (T12 (iv.e)).
- The frozen core computes H_r(h) only for h = 1{j ∈ S} (`pip_plain`); for other h the identity concerns the v3.1
  accumulator applied to the same coded endpoints (STATEMENT §1).
- Premise statuses inherited: T12 PROVED-LOCKED; N9 (START, KERNEL) PROVED (candidate), code-checked, CHK_INHERITED VERIFIED
  WITH AMENDMENT; EX-A and H-U are idealisations.
