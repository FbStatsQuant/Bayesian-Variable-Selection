# X5 · Re-check of `W3-READER:PoolZ` — PROOF v1 (line check)

PoolZ's proof (W3-READER STATEMENT.md lines 23–31 on `theory/W3-READER`) has four steps; each is checked.

1. *Per-island identity.* `W1-N1:Thm-N1` states, for every fixed r ≥ 1, a.s. on 𝒜 ∩ {r ≤ R′}: E[Ẑ_r·H_r(h) | 𝓒] = Zπ(h)
   and "in particular, with W_r := Ẑ_r/Z, E[W_r | 𝓒] = 1" (`Theory_work/Wave1/W1-N1/STATEMENT.md:98-104`; h ≡ 1). The
   localised meaning is E[1_{E₀}Y | 𝓒] = 1_{E₀}(right side) with E₀ = 𝒜 ∩ {r ≤ R′} ∈ σ(𝓒)
   (`Theory_work/Wave1/W1-N1/STATEMENT.md:94-96`). Correctly quoted.
2. *Four islands.* In the code of record R′ = `islands = 4L` (`Scripts/SMC_BVS/core/v3_run.R:91`), so on 𝒜 the identity holds
   for r = 1, 2, 3, 4; the union of four null sets is null. Correct.
3. *Linearity.* The reported evidence is log Ẑ = log((1/R)Σ_r Ẑ_r) with R = 4 islands (`Scripts/SMC_BVS/core/v3_run.R:150-154`;
   the island values are the potential records on completed runs, `W3-SAMP:PC`, and are the potential records by
   definition in N1's statement). E[Ẑ/Z | 𝓒] = ¼Σ_r E[W_r | 𝓒] = 1 a.s. on 𝒜. With the data fixed, Z > 0 is a constant,
   so E[Ẑ | 𝓒] = Z on 𝒜. Correct (Ẑ_r ≥ 0, so all conditional expectations exist).
4. *Joint law.* Under the joint data/algorithm law with the final streams independent of the data and of streams 0–9
   (H-U/SI, `Theory_work/Wave3/W3-SAMP/STATEMENT.md:35-36`), the fixed-data identity is a version of the conditional
   expectation given (data, 𝓒) (W1-N1's freezing lemma pattern); taking expectations of 1_𝒜E[Ẑ | data, 𝓒] = 1_𝒜Z gives
   E[1_𝒜Ẑ] = E[1_𝒜Z]. Correct.

*The precision (X5-b).* Step 1 uses 𝒜 ∈ σ(𝓒). By T1 (GW-iv) and T5 (CAL-b), 𝒜° ∈ σ(𝓒°) and 𝒜 = 𝒜° ∩ G ⊆ 𝒜°, where G
depends on clock readings during calibration. Steps 1–4 therefore prove the claim with (𝒜°, 𝓒°). Passing to the actual
𝒜: E[1_𝒜Ẑ°] = E[1_{𝒜°}1_G Ẑ°]; if G is conditionally independent of the final streams given 𝓒° (true if the
calibration-time clock is a function of the calibration's own execution and of noise independent of streams 10–13),
E[1_G Ẑ° | 𝓒°, G] = 1_G Z on 𝒜° and the identity follows; without a probability model for the clock this step is not
available (T1, Not claimed). No upper-bound transfer helps here, because PoolZ is an equality. ∎
