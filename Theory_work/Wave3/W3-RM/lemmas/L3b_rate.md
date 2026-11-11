# L3b — SAND-R with a slower localisation rate (strengthening adopted from R02 P3a)

Status: **PROVED (by this seat, unchecked)** — a delta to `L3_SANDR.md` §4 (parallel prover; its §8 already proves
the case r_n = C√(log n/n)). Origin: `../reviews/R02_better_theorem_astra.md` P3a. Checks: R04 (Claude Opus 5.5 high,
`../reviews/R04_SANDR_check_opus.md`): VERIFIED; cross-family: R07 mid-point (Codex gpt-6-astra high,
`../reviews/R07_midpoint_astra.md`, derivation (C2) step 2) and sweep R08 (`../reviews/R08_sweep_astra.md`,
verification record) re-derive the four error terms [C1-B5].

**(L-loc-R′)** (= (L-loc-R) as stated in `../STATEMENT.md` v1.2 §3.2 [R08-17].) As the baseline condition of
`L3_SANDR.md` §1 with C_L n^{−2} replaced by a deterministic r_n with
  r_n (n log n)^{1/4} → 0
(for instance r_n = n^{−1/3}): for every l ∉ Q, U ⊆ [p] ∖ {l} with |U| ≤ 15, U₀ = U ∩ H_l, v ∈ U ∖ H_l and
j ∈ S₀ ∖ U₀: |Cov(W_l, W_v | W_{U₀})| ≤ r_n and |Cov(W_j, W_v | W_{U₀})| ≤ r_n.

**Lemma SAND-R′.** Lemma SAND-R (`L3_SANDR.md` §1) holds with (L-loc-R) replaced by (L-loc-R′).

*Proof.* (L-loc-R) is used in `L3_SANDR.md` only in §4, to obtain display (1) there:
|h_{U,l} − h_{U₀,l}| ≤ ω_n → 0 and h_{U,l} ≤ C log n, simultaneously for all l ∉ Q and |U| ≤ 15 on E_cov. We re-derive
(1). Notation of that section: h_n = √(log n/n); z₀ the sample partial correlation of W_l and Y given U₀; a, d the
sample partial-correlation vectors of W_l and of Y with W_V given U₀ (V = U ∖ H_l); R the sample conditional
correlation matrix of W_V, ‖R⁻¹‖ ≤ C by the Schur floor (no remote/remote bound needed, `L3_SANDR.md` §4).
For deterministic b in the coefficient box, (L-loc-R′) gives |Cov(W_l, W_v | W_{U₀})| ≤ r_n and
|Cov(V_b, W_v | W_{U₀})| ≤ Σ_{j∈S₀∖U₀}|b_j| r_n ≤ 2s₀θ_hi r_n (truths in U₀ and the independent noise contribute 0).
With the uniform O(h_n) sample comparison of `L3_SANDR.md` §3 (bounded dimension, conditional variances bounded
below), evaluated at b = θ*/t:
  ‖a‖ + ‖d‖ ≤ C(r_n + h_n) =: Cg_n,  |z₀| ≤ Ch_n  (the latter from (L-gain-R), unchanged).
The recursion z_U = (z₀ − aᵀR⁻¹d)/√((1 − aᵀR⁻¹a)(1 − dᵀR⁻¹d)) gives, for n ≥ n₀ (g_n → 0),
|z_U − z₀| ≤ |aᵀR⁻¹d| + |z₀ − aᵀR⁻¹d|·Cg_n² ≤ Cg_n². Hence, with h_{U,l} = n z_U²,
  |h_{U,l} − h_{U₀,l}| = n|z_U − z₀||z_U + z₀| ≤ Cn g_n²(h_n + g_n²)
    ≤ C[√(n log n) r_n² + (log n)^{3/2}n^{−1/2} + n r_n⁴ + (log n)²/n] =: ω_n.
Under (L-loc-R′): √(n log n) r_n² → 0, and n r_n⁴ = (√(n log n) r_n²)²/log n → 0; so ω_n → 0. Also
h_{U,l} ≤ h_{U₀,l} + ω_n ≤ Cn h_n² + o(1) ≤ C log n. This is display (1); §§5–7 of `L3_SANDR.md` use (L-loc-R) only
through (1). ∎

**Remark.** The leak rate (L-gain-R) (C_L n^{−1/2}) is not relaxed here. R02 P3b proposes the standardised budget
n·aᵀG⁻¹a/v ≤ η log n (η < η_A), which would allow leaks of order √(log n/n); it requires redoing the noncentral
spherical tail and the ladder and is recorded as a separate ticket (`../SHARPNESS.md` §3.1).
