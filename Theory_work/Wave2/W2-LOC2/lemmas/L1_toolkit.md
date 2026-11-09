# L1 — Quasi-polynomial toolkit (Lemma L0′) and sample regularity for polylogarithmic sets

Status: **PROVED (by this seat, unchecked)**. Sources: GEN `lemmas/L1_lemmaE.md` ([GEN-L1]; PROVED (by this seat,
unchecked), R02 VERIFIED-WITH-AMENDMENTS), GROW `lemmas/L0_toolkit.md` (L0; R03 VERIFIED), GROW `lemmas/L2_NA_TL.md`
(L2.0–L2.2; R03 VERIFIED-WITH-AMENDMENTS), GROW `lemmas/L6_random_AR1.md` L6.2 (R07 VERIFIED), APP `lemmas/L3_LOC.md`
L3.2. This file is a delta proof: every place where those proofs use "|A| ≤ C log n" or "|𝔉| ≤ C n^D" is listed.
Check record: R02 (Codex gpt-6.1-sol high, `reviews/R02_L1L3_check_sol.md`): VERIFIED-WITH-AMENDMENTS; amendments 2, 3 applied (`reviews/R02_disposition.md`).

## L1.1 Lemma L0′
Let 𝔉 = 𝔉_n be a deterministic family of subsets of [p] with ∅ ∈ 𝔉, |A| ≤ J_n for A ∈ 𝔉, a Gram floor
λ_min(R̂_A) ≥ φ₀² > 0 on nonempty A ∈ 𝔉, ‖μ‖² ≤ Mn, and 𝒱𝒱 = 𝒱𝒱_n a deterministic vector set, with
  J_n ≤ (log n)^κ, log|𝔉_n| ≤ (log n)^κ, log|𝒱𝒱_n| ≤ (log n)^κ  (κ ≥ 1 fixed).
Replace in [GEN-L1] t_n := 4(D + 2) log n by t_n := 4(log|𝔉_n| + 2 log n + J_n), and h_n := √(2(D_V + 1) log n) by
h_n := √(2(log|𝒱𝒱_n| + log n)). Then, with these replacements and the inherited premises (∅ ∈ 𝔉, Gram floor, energy,
𝒱𝒱 ⊇ {r_A} ∪ {r_A − r_{A′}} as each consequence requires), the event bounds and the score/contrast conclusions of
[GEN-L1] L1.1–L1.4 and GROW L0.2(a)–(c) hold with the same constants C_R, c_E, κ_E, for n ≥ n₀(κ, σ², M, φ₀) [R01-6].
Facts used: t_n + h_n² = O((log n)^κ) = o(n), J_n/n → 0, (t_n + h_n²)log n/n → 0. For random designs the families are
fixed after conditioning on the raw design and the failure bounds are uniform in it.
*Proof.* [GEN-L1] uses J, D, D_V only at the following places.
(i) L1.1, 𝒟₂: for a deterministic projection of rank d ≤ J_n, P(‖Pε‖²/σ² > t_n) ≤ 2^{d/2}e^{−t_n/4}
  = 2^{d/2}e^{−J_n}|𝔉_n|⁻¹n^{−2} ≤ |𝔉_n|⁻¹n^{−2}; union over 𝔉_n: P(𝒟₂ᶜ) ≤ n^{−2}.
  𝒟₃: P(|N(0,1)| > h_n) ≤ 2e^{−h_n²/2} = 2|𝒱𝒱_n|⁻¹n⁻¹; union: P(𝒟₃ᶜ) ≤ 2/n. 𝒟₁ does not involve 𝔉.
(ii) L1.2(a): RSS_A ≥ σ²(n − 1 − 2n^{2/3} − 2n^{1/3} − h_n² − t_n) ≥ nσ²/2 needs h_n² + t_n ≤ n/2 − O(n^{2/3}): true
  since h_n², t_n = O((log n)^κ). L1.2(b)–(d) do not involve 𝔉.
(iii) L1.3: needs (n − 1)φ₀² ≥ max(J_n, 100) and J_n/((n − 1)φ₀²) ≤ 1: true for n ≥ n₀.
(iv) L1.4 uses only the events. GROW L0.2(a): ω_n := 4n^{−1/3} + (h_n² + t_n + 1)/n → 0; (b), (c) use only (a) and L1.3. ∎

**Consequence for GROW L2.0–L2.2.** For S₀ ⊆ Q, |Q| ≤ (log n)^κ, and the lattice family 𝔉 of GROW L2.0
(|A| ≤ |Q| + 1, |𝔉| ≤ 1 + 2^{|Q∖S₀|}(1 + p + s₀ + s₀p), 𝒱𝒱 := {r_A − r_{A′}} ∪ {r_A}, |𝒱𝒱| ≤ 2|𝔉|²): J_n = |Q| + 1,
log|𝔉| ≤ |Q| log 2 + (A + 1) log n + log(4s₀) and log|𝒱𝒱| ≤ log 2 + 2 log|𝔉| are O((log n)^κ), hence each is
≤ (log n)^{κ+1} for n ≥ n₀; so L0′ applies with envelope exponent κ_tool := κ + 1 (for (D1): d + 1 replaced by d + 2), with
t_n, h_n still defined from the actual cardinalities (so t_n + h_n² = O((log n)^κ)) [R02-2]; call 𝓔_n its event. Then:
* GROW L2.1 (TL) holds on 𝓔_n for n ≥ n₀, under (G2) and the FIXED beta-min θ_lo > 0 of STATEMENT §1 (signal ≍ n; no
  general BM-∞ version is claimed — the signal must dominate t_n + h_n², not only log n) [R01-6]: its proof uses RSS_A − RSS_T ≥ Λ_A − 2σh_n√Λ_A − σ²t_n
  ≥ Λ_A/4 for Λ_A ≥ L′_n = (n − 1)φ₀²θ²_min, true since h_n², t_n = O((log n)^κ) = o(n); the final comparison
  (A + 1) log n + 1 + 2κ_E − L′_n/(8C_R) < 0 is unchanged.
* GROW L2.2 (NA reduction) holds on 𝓔_n ∩ {max Z²_{T,l} ≤ c_n}: its proof uses k ≤ |Q| (prior term
  ≤ log(|Q| + 1) − log p), x := σ²Z²/RSS_T ≤ c_n/(n(1 − ω_n)) ≤ ¼ (c_n = O(log n)), and an excess
  O(log n)(ϑ_n + log n/n) → 0 with ϑ_n := (1 + 0.02/n)/(1 − ω_n) − 1 = O(ω_n + 1/n). The last step needs the RATE
  [R02-3]: ω_n log n = O(n^{−1/3}log n + (log n)^{κ+1}/n) → 0 (from t_n + h_n² = O((log n)^κ)), hence
  O(log n)(ϑ_n + log n/n) → 0. With q ≤ p, c_n = log n + O(log p + log(q + 1)) = O(log n), so x ≤ ¼ eventually and the
  same strict negative score margin −½ follows. Nothing else depends on |Q| = O(log n).

## L1.2 Sample regularity (delta to GROW L6.2 and APP L3.2)
Setting: raw rows iid N(0, Σ_n), Σ_n unit diagonal with λ_min(Σ_n) ≥ c (or, for (N1) only, on Q ∪ {l});
ħ_n := C_A√(log n/n). GROW L6.2's entrywise event (raw centred columns + noise column; union over (p + 1)² entries;
Gaussian + unit variances only) and its standardised version A_X hold with probability → 1, unchanged. On it:
* **Gram floors for polylog sets.** For every S with |S| ≤ J_n := (log n)^{κ′}, any fixed κ′ [C1-Opus-4], ‖R̂_S − Σ_S‖_op ≤ |S|·max entry error
  ≤ C J_n ħ_n → 0; hence λ_min(R̂_S) ≥ c/2 for n ≥ n₀ whenever λ_min(Σ_S) ≥ c. This covers (G2) (|Q ∪ {l}| ≤ (log n)^κ),
  all blocks (≤ 16), within-block SE and the lattice family (no union over subsets is needed after the entrywise event).
* **m♯_n, SE_w (g₀ = 1), BM-∞, energy:** unchanged (GROW L6.2; APP L1_POST).
* **TV (G3b)** from PTV (APP L3.2), **A_cov** (bounded-size sample partial correlations involving Y within O(ħ_n) of
  population values): unchanged — bounded dimensions, conditional variances ≥ c, residual variance of Y ≥ σ².
* **A_score** (GROW L6.2 [A3]): the L0 events for the first family (all subsets of size ≤ 16; ≤ 17(p + 1)^{16}
  members) and, by L0′, for the lattice family (log size O((log n)^κ)); conditional on X ∈ A_X the Gram floors hold
  with common constants, so L0′'s conditional Gaussian bounds give a uniform o(1) failure probability; integrate.
* **(G1)** Q = [p] or K_n ≥ 2|Q| + 32s₀ + 1: by the enlargement rule (Q⁰ kept iff p ≥ 2|Q⁰| + 32s₀ + 1) and
  K_n = min(p, ⌊n/2⌋) ≥ 2|Q| + 32s₀ + 1 once ⌊n/2⌋ ≥ 2(log n)^κ + 32s₀ + 1; in the enlarged case Q = [p], |Q| = p ≤
  2|Q⁰| + 32s₀ = O((log n)^κ) and K_n = p eventually.
