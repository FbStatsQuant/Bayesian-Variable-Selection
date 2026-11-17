# W2 · Lemma FRZ (freezing on the calibration value, at general c, at the pin) — STATEMENT v1 (draft, not locked)

Track A_W item W2 (manager 11-17; D97 edge verdicts, recorder package §2 edge 4). Tier B (line check of `W1-N1:F`'s
freezing step and of its use by `W3-SAMP:MR` at the code of record). **Lean target: yes** for (FRZ-a) (the freezing
lemma: for 𝓒 independent of U and bounded jointly measurable g, E[g(𝓒, U) | 𝓒] = ḡ(𝓒); a monotone-class argument) and
for (FRZ-d) (a finite product bound); no for (FRZ-b), (FRZ-c) (code facts).

## Steps under check (the conditions to discharge)
- `W1-N1:F` (registry: `Theory_work/Wave1/W1-N1/lemmas/L3_freezing.md:21-23`; proof `:25-46`), written for the v2.2.1
  core: conditioning island-r identities on the calibration record 𝓒 (localisation E₀, set A₀, evidence bound, T12
  freezing lemma `Docs/Theory/proofs/T12_T8_frozen_run_identities/PROOF_v6.tex:157-162`).
- Its extension in **`W3-SAMP:MR`** (Steps 2–4, `Theory_work/Wave3/W3-SAMP/lemmas/MR_identities.md:57-79`) from
  terminal endpoints to stage-t populations, post-terminal populations and pre-step states, with the stage evidence ratio
  bound. FR (`W3-AUDIT-AX:FR`) gives the identities at **fixed** c only and excludes T12 (iii) (D97 edge 4).

## Code of record
`Scripts/SMC_BVS/core/` at pin 4676af6 (= HEAD for the core); paths relative to it.

## Setting
Fixed valid data on the SMC branch. Streams U^{(k)} as in T5 (`Theory_work/Wave3/W3-AUDIT/track_A/T5_CAL/STATEMENT.md`);
H-U: the streams are independent i.i.d. U[0, 1) sequences. 𝓒° (calibration record of the potential fit P°) and
𝒜° ∈ σ(𝓒°) as in T5 (CAL-b), a random element of a measurable space (E, 𝓔) on which c ↦ (T, grid, N_e, L, tier) is
measurable. For r ∈ {1, …, 4}: U_r := U^{(9+r)} ∈ (Υ, 𝓤) = ([0, 1)^ℕ, Borel); Φ the island record map and A_s the
success set of W1 (ISL). R′ = 4 (`v3_run.R:90-91`), so E₀ := 𝒜° ∩ {r ≤ R′} = 𝒜°. EX-A. Potential run (T1).

## Lemma FRZ
- **(FRZ-a) Freezing lemma.** If 𝓒 is a random element of (E, 𝓔), U of (Υ, 𝓤), 𝓒 ⊥ U, and g : E × Υ → ℝ is bounded
  and 𝓔 ⊗ 𝓤-measurable, then ḡ(c) := E[g(c, U)] is 𝓔-measurable and E[g(𝓒, U) | 𝓒] = ḡ(𝓒) a.s.
  (T12 `Docs/Theory/proofs/T12_T8_frozen_run_identities/PROOF_v6.tex:157-162`, line-checked.)
- **(FRZ-b) The code meets its hypotheses at the pin.** (i) U_r ⊥ 𝓒° (SI): 𝓒° is a measurable function of the fixed
  data and U^{(0)}, …, U^{(9)} (T5 CAL-a, CAL-b) and U^{(9+r)} is independent of these streams (H-U). (ii) There is
  A₀ ∈ 𝓔 with A₀ ⊆ A_s and E₀ = {𝓒° ∈ A₀}. (iii) On E₀, the potential record of final island r is O_r = Φ(𝓒°, U_r) (and its augmented record is Φ̃(𝓒°, U_r)):
  the final run's settings are functions of 𝓒° and (n, p) (T5 CAL-c), stream 9 + r is seeded inside `cpp_final_run`
  for island r alone and read by nothing else, and the frozen grid lies in A_s.
- **(FRZ-c) Conditioning at general c.** For every 𝓔 ⊗ 𝓤-measurable g with |g| ≤ B < ∞ and g(c, ·) = 0 for c ∉ A₀:
  E[1_{E₀} Y | 𝓒°] = 1_{E₀} ḡ(𝓒°) a.s. for every Y with 1_{E₀} Y = g(𝓒°, U_r) (localised form, `W1-N1:F`'s
  convention). In particular `W1-N1:F`'s statement (terminal endpoints, h jointly measurable with a deterministic bound)
  `W3-SAMP:MR` (MR-a)–(MR-c) and the freezing step of `W3-SAMP:D` (D-i) (g = 1{no draw of Φ̃ equals S₀}) given 𝓒 hold at the pin with (𝒜°, 𝓒°), the fixed-c values ḡ(c) being FR (FR-b), (FR-c).
  On 𝒜 the actual record equals 𝓒° (T5 CAL-d), so they hold for the actual (𝒜, 𝓒) on 𝒜 in the sense T5 states.
- **(FRZ-d) Evidence bounds.** For c ∈ A_s, t ≤ T, u ∈ Υ, with d_min := min_Ω d, d_max := max_Ω d (finite, Ω finite,
  EX-A): Ẑ_t(Φ(c, u)) ∈ [Z₀e^{φ_t d_min}, Z₀e^{φ_t d_max}] and Z_t(c) ∈ the same interval, Z₀ = m(∅)Z̄₀; hence
  0 < Ẑ_t/Z_t ≤ C_d := e^{d_max − d_min}, and Ẑ = Ẑ_T ≤ Z₀e^{d_max}, uniformly in (c, u). So the integrands of
  `W1-N1:F` and `W3-SAMP:MR` (with |h| ≤ B_h) are bounded by B_h·Z₀e^{d_max} and B_h·C_d.

## Not claimed
- The fixed-c identities themselves (FR); measurability of Φ (W1 ISL-d, used); IND-T / independence between islands.
- Binary64; interrupted runs (T1 GW).

## Changelog
| version | clause | tag | reason | trigger | check |
|---|---|---|---|---|---|
| v1 | all | NEW-CLAIM (line check of `W1-N1:F`'s freezing step and `W3-SAMP:MR`'s extension at the pin) | track A_W W2 | manager 11-17; D97 edge 4 | `CHECK.md` |
