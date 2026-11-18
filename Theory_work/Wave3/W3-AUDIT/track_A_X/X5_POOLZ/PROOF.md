# X5 · Re-check of `W3-READER:PoolZ` — PROOF v1.1 (line check)

PoolZ's proof (W3-READER STATEMENT.md lines 25–33 on `theory/W3-READER`; the claim at lines 21–23) has four steps; each is checked.

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
4. *Joint law.* Under the joint data/algorithm law with the final streams independent of (data, streams 0–9) jointly
   (H-U/SI, `Theory_work/Wave3/W3-SAMP/STATEMENT.md:35-36`), the fixed-data identity is a version of the conditional
   expectation given (data, 𝓒) by T12's freezing lemma, **provided** the integrand g(data, c, u) is jointly measurable
   (MEAS-J). W1-N1's MEAS is joint in (c, u) for fixed data only (`Theory_work/Wave1/W1-N1/STATEMENT.md:83-85`); MEAS-J
   follows from the same bounded-computation argument as T5 (CAL-b) PROOF Step 3 (a program of bounded length whose
   steps are Borel operations or branches on comparisons of Borel functions of the scores — Borel in the data — and of
   the uniforms), and 𝓒 is a measurable function of (data, streams 0–9) (T5 CAL-b). Then taking expectations of
   1_𝒜E[Ẑ | data, 𝓒] = 1_𝒜Z gives E[1_𝒜Ẑ] = E[1_𝒜Z], an equality in [0, ∞] (both sides nonnegative). Correct once
   MEAS-J and the joint independence are stated (PoolZ uses them without stating them).

*The precision (X5-b).* Step 1 uses N1, whose conditioning needs CAL for 𝓒. The actual 𝓒 contains its status, so
𝒜 ∈ σ(𝓒), but it depends on the clock through the guard's Booleans, so CAL fails for it. By T1 (GW-iv) and T5 (CAL-b),
𝓒° satisfies CAL, 𝒜° ∈ σ(𝓒°) and 𝒜 = 𝒜° ∩ G ⊆ 𝒜°, where G depends on clock readings during calibration. Steps 1–4 therefore prove the claim with (𝒜°, 𝓒°). Passing to the actual
𝒜: E[1_𝒜Ẑ°] = E[1_{𝒜°}1_G Ẑ°]; if the final streams are independent of (data, streams 0–9, G) jointly (true if the calibration-time clock is a
function of the calibration's own execution and of noise that is independent of streams 10–13 jointly with the data
and streams 0–9; pairwise independence is not enough),
E[1_G Ẑ° | 𝓒°, G] = 1_G Z on 𝒜° and the identity follows; without a probability model for the clock this step is not
available (T1, Not claimed). No upper-bound transfer helps here, because PoolZ is an equality. ∎
