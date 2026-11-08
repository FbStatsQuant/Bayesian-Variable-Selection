# Lemma CR — elementary sample-correlation tails; consequences [CONC′] and (R′)

Status: PROVED (by this seat); XF VERIFIED (R19, Codex gpt-6.1-sol) — v1, 2026-11-08. Note (R19): the complement of
the margin event uses error ≥ δ*; apply [CONC′] at δ ↑ δ* (the bound is continuous in δ). Purpose: (1) a self-contained, explicit replacement for
the classical citation [CONC] (PROOF.md:27-28) used by P2 / P8♯; (2) a fallback for dependency point D2: a summable,
explicit partition-recovery bound that does not use Hotelling's density or W7 Corollary B. Only Laurent–Massart [LM]
and the Gaussian tail are used. NBH = `Theory_work/Old_Projects/New_BVS_Headquarters/`.

[LM] (Laurent & Massart 2000, Lemma 1): for k ≥ 1, x > 0, P(χ²_k ≥ k + 2√(kx) + 2x) ≤ e^{−x}, P(χ²_k ≤ k − 2√(kx)) ≤ e^{−x}.

## Lemma CR
Let (u_i, v_i), i ≤ n (n ≥ 3), be iid bivariate normal with correlation r ∈ (−1,1), and r̂ the Pearson sample
correlation (centred, as computed from the standardised Gram matrix; W7 §0.1, `NBH/branch_snapshots/W7-PART/PROOF.md:14-15`).
Then for every δ ∈ (0, 2]:
  P(|r̂ − r| > δ) ≤ 6 exp(−(n−1)δ²/1024).

*Proof.* r̂ is invariant under positive affine maps of each coordinate, so take means 0, variances 1, and write
v = ru + sw, s := √(1−r²), with w iid N(0,1) independent of u. Let C be the centring matrix, N := n−1, and
α := ‖Cu‖²/N, β := ‖Cw‖²/N, γ := ⟨Cu, Cw⟩/N, M := [[α, γ], [γ, β]], x := (r, s)ᵀ (‖x‖ = 1), e₁ := (1,0)ᵀ. Since
Cv = rCu + sCw,
  r̂ = e₁ᵀMx / (√(e₁ᵀMe₁) · √(xᵀMx)).
Let η ∈ (0, ¼] and E_η := {|α − 1| ≤ η, |β − 1| ≤ η, |γ| ≤ η}. On E_η, Δ := M − I has entries bounded by η, so
‖Δ‖_op ≤ ‖Δ‖_F ≤ √(4η²) = 2η ≤ ½ (four entries, each of absolute value ≤ η). Then
|e₁ᵀMx − r| = |e₁ᵀΔx| ≤ 2η, and e₁ᵀMe₁, xᵀMx ∈ [1−2η, 1+2η], so the denominator d ∈ [1−2η, 1+2η]. Hence
  |r̂ − r| ≤ |e₁ᵀMx − r|/d + |r|·|1/d − 1| ≤ 2η/(1−2η) + 2η/(1−2η) ≤ 8η.
Probability of E_ηᶜ: Nα and Nβ are χ²_N. Upper tail with x = Nη²/16: 2√(Nx) + 2x = Nη/2 + Nη²/8 ≤ Nη (η ≤ 1), so
P(α − 1 > η) ≤ e^{−Nη²/16}. Lower tail with x = Nη²/4: P(α − 1 < −η) ≤ e^{−Nη²/4}. Same for β. Given u, Nγ =
⟨Cu, w⟩ ~ N(0, Nα) (w ⊥ u, ⟨Cu, Cw⟩ = ⟨Cu, w⟩); on {α ≤ 1 + η} ⊆ {α ≤ 2}, P(|Nγ| > Nη | u) ≤ 2e^{−N²η²/(4N)} = 2e^{−Nη²/4}.
So P(E_ηᶜ) ≤ 2(e^{−Nη²/16} + e^{−Nη²/4}) + 2e^{−Nη²/4} ≤ 6e^{−Nη²/16}. With η := δ/8 ≤ ¼:
P(|r̂ − r| > δ) ≤ P(E_ηᶜ) ≤ 6e^{−Nδ²/1024}. ∎

## Corollary [CONC′] (replaces the cited [CONC])
For the LH-iid design (any p, rows iid N(0, Σ), Σ a correlation matrix) and any δ ∈ (0, 2]:
  P(max_{j<k} |r̂_jk − Σ_jk| > δ) ≤ 3p² e^{−(n−1)δ²/1024}.
With p ≤ n^A and δ_n := 32√(2(A+1) log n/(n−1)) (≤ 2 for n ≥ n₀(A)): the bound is ≤ 3n^{2A}n^{−2(A+1)} = 3n^{−2}, summable.
So max_{j<k}|r̂_jk − Σ_jk| ≤ C₁√(log p ∨ log n)/√n-type control holds in the explicit form
max|r̂ − Σ| ≤ δ_n = O(√(log n/n)) w.p. ≥ 1 − 3n^{−2}. *Proof.* Union bound over ≤ p²/2 pairs. ∎
*Use.* P2(a) / P8♯ step 2(a): ‖R̂_T − Σ_T‖_op ≤ |T|·δ_n ≤ L_n δ_n = O((log n)^{3/2}n^{−1/2}) → 0, so λ_min(R̂_T) ≥ λ₀/2 for
all |T| ≤ L_n once L_nδ_n ≤ λ₀/2, on an event of probability ≥ 1 − 3n^{−2}.

## Corollary (R′) (fallback for D2)
On LH-iid with (SIZE) at n: within-group population correlations equal ρ; cross-group ones are 0, ψ_i, ψ_iρ, ψ_iρ²,
all ≤ ψ̄ < ρ in absolute value (W7-PART §0.2 example, PROOF.md:41-44 of W7). Put δ* := (ρ − ψ̄)/2 ∈ (0, ½) and t := (ρ+ψ̄)/2.
On {max_{j<k}|r̂_jk − Σ_jk| < δ*}: every within |r̂| > ρ − δ* = t and every cross |r̂| < ψ̄ + δ* = t, i.e. the global
margin of W7 Theorem B's proof holds, and W7 Theorem A (A4 ⇒ A1 ⇒ A3; status "PROVED (W7-PART); XF VERIFIED* (A-REV9:
A1-A4 VERIFIED ...)", `NBH/ID_REGISTRY.md:310`) — equivalently PXN Lemma P1 (XF VERIFIED, A-REV3) — gives blocks = groups.
Hence, for every n ≥ 3 at which SIZE holds,
  P(𝒜_nᶜ) ≤ 3p² exp(−(n−1)(ρ−ψ̄)²/4096).
Consequences: with p ≤ n^A, Σ_n P(𝒜_nᶜ) < ∞, and for every C > 0, P(𝒜_nᶜ) ≤ p^{−C} once
log 3 + (2 + C)A log n ≤ (n−1)(ρ−ψ̄)²/4096 (using p ≤ n^A for p^{2+C}); this is the first-line form of (R) that (C), (P)
use. The exponent (ρ−ψ̄)²/4096 is far from W7's I* (crude constants); it is explicit and needs no Hotelling density.

## Remark on what is (not) claimed
- The 1/1024 constant is not optimised. Only the exponential-in-n form and the explicit constants matter.
- This lemma does not touch W7 Theorem A (deterministic); it replaces only the probabilistic step (Lemma 2 / Corollary B).
