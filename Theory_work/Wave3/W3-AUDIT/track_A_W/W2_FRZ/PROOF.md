# W2 · Lemma FRZ — PROOF v1 (line check of `W1-N1:F` and of `W3-SAMP:MR` Steps 2–4 at pin 4676af6; paths relative to `Scripts/SMC_BVS/core/`)

Reuse: T5 CAL-C (`Theory_work/Wave3/W3-AUDIT/track_A/T5_CAL/STATEMENT.md`, (CAL-a)–(CAL-d)), T1 GW (potential run), W1
ISL (`Theory_work/Wave3/W3-AUDIT/track_A_W/W1_ISL/STATEMENT.md`: (ISL-0), (ISL-d)), FR (`Theory_work/Wave3/W3-AUDIT/track_A_X/X1_T12/STATEMENT.md`:
the fixed-c identities and the evidence recursion at the pin).

## (FRZ-a) Freezing lemma — line check of T12 PROOF_v6 Lemma "freezing"
(`Docs/Theory/proofs/T12_T8_frozen_run_identities/PROOF_v6.tex:157-162`.) Let 𝓗 be the class of bounded
𝓔 ⊗ 𝓤-measurable g such that ḡ(c) = E[g(c, U)] is 𝓔-measurable and E[g(𝓒, U)1_C(𝓒)] = E[ḡ(𝓒)1_C(𝓒)] for every C ∈ 𝓔.
*Rectangles.* For g = 1_{A×B}: ḡ = 1_A·P(U ∈ B) is measurable, and E[1_A(𝓒)1_B(U)1_C(𝓒)] = P(𝓒 ∈ A ∩ C)P(U ∈ B) by
independence = E[ḡ(𝓒)1_C(𝓒)]. *Closure.* 𝓗 is a vector space containing the constants (linearity of E and of
c ↦ E[g(c, U)]); if 0 ≤ g_k ↑ g bounded with g_k ∈ 𝓗, then ḡ_k ↑ ḡ (monotone convergence for each c), so ḡ is
measurable, and both sides converge (monotone convergence). The rectangles form a π-system generating 𝓔 ⊗ 𝓤; by the
monotone class theorem (functional form) 𝓗 contains every bounded 𝓔 ⊗ 𝓤-measurable g. Measurability of ḡ (Fubini–Tonelli
for the bounded g) and the defining property of conditional expectation give E[g(𝓒, U) | 𝓒] = ḡ(𝓒) a.s. The T12 text
proves exactly this (rectangles, closure under linear combinations and bounded monotone limits, monotone class); its
U = (U₁, …, U₄) is any random element of (Υ, 𝓤), so it applies to the single stream U_r. Agrees. ∎

## (FRZ-b) The hypotheses at the pin
(i) *SI.* By T5 (CAL-a), until `v3_calibrate` returns only streams 0–9 are created or read, and by (CAL-b) 𝓒° =
Ψ(X, y, seed, U^{(0)}, …, U^{(9)}) with Ψ measurable; the data are fixed and the seed is a constant label. The only stream
objects in the fit path are the calibration map `streams` (keys k = 0..9, `cpp/v3_core.cpp:596`) and the final islands'
`RngSource` (`cpp/v3_core.cpp:444`); `cpp/v3_core.cpp:241` is an inspection helper off the `v3_fit` call graph. Under
H-U the streams are independent, so U_r = U^{(9+r)} ⊥ (U^{(0)}, …, U^{(9)}) and hence U_r ⊥ 𝓒°.
(ii) *A₀.* 𝒜° ∈ σ(𝓒°) (CAL-b), so 𝒜° = {𝓒° ∈ A_𝒜} for some A_𝒜 ∈ 𝓔 (Doob). On 𝒜° the potential fit reaches
`v3_final_run` (`v3_fit.R:154-162`), which checks the frozen grid (`v3_run.R:225`, `v3_check_grid`, `v3_run.R:77-82`:
finite, length ≥ 2, starts at exactly 0, ends at exactly 1, strictly increasing); this check is an X2 site, unreachable on
𝒜° (the grid is a successful construction or a fallback that passed the same check, `v3_calib.R:164`; C1 (C1-b) (vii),
`Theory_work/Wave3/W3-AUDIT/track_A_C/C1_AUDITS/PROOF.md`). The executed N_e = `b$tiers$N[tier + 1]` ≥ N₀ ≥ 2500 and
L = `b$L` ≥ 4 are integers (`v3_run.R:89-90`; `v3_preprocess.R:24-25, 30`). So 𝓒° ∈ A_s on 𝒜°, and A₀ := A_𝒜 ∩ A_s ∈ 𝓔
gives E₀ = 𝒜° = {𝓒° ∈ A₀} (R′ = `islands` = 4, `v3_run.R:91`, so {r ≤ R′} is the whole space for r ≤ 4).
(iii) *O_r = Φ(𝓒°, U_r) on E₀.* `cpp_final_run` receives `frozen[["grid"]]` and `ro` (N_e, L, Hm = 4, tier, islands)
(`v3_run.R:226-227`), all functions of 𝓒° and (n, p) (T5 CAL-c). Before the islands it ingests the block tables and the
inherited models with the scorer only (`cpp/v3_core.cpp:407-439`): no uniform. The islands run serially; island r creates
its `RngSource` seeded on stream 9 + r and runs `E.run_island(r, o.N, g, o.L, o.Hm, o.tier, nullptr)`
(`cpp/v3_core.cpp:443-446`); no other code reads that source, and island r's record does not depend on islands < r (W1
ISL-0: the shared cache and ledger do not feed transitions). In P° the guard Booleans are FALSE (T1), so island r's
potential record is the W1 program run with c = 𝓒° on u = U_r: O_r = Φ(𝓒°, U_r), and likewise for Φ̃. ∎(FRZ-b)

## (FRZ-c) Conditioning at general c
Let g be as stated. By W1 (ISL-d), compositions of g-type functions with Φ, Φ̃ are 𝓔 ⊗ 𝓤-measurable; g is bounded. By
(FRZ-b)(i) and (FRZ-a), E[g(𝓒°, U_r) | 𝓒°] = ḡ(𝓒°) a.s.; since g(c, ·) = 0 off A₀, ḡ = 1_{A₀}ḡ, so
E[1_{E₀}Y | 𝓒°] = E[g(𝓒°, U_r) | 𝓒°] = 1_{E₀}ḡ(𝓒°).
*`W1-N1:F`.* Its g (`Theory_work/Wave1/W1-N1/lemmas/L3_freezing.md:29-31`) is g(c, u) = Ẑ(Φ(c, u))·η_q(Φ(c, u))(h(·; c))
on A₀, 0 off it: measurable (ISL-d; h jointly measurable; N_e(c) a measurable integer coordinate, the sum measurable cell
by cell) and bounded by B_h Z₀e^{d_max} (FRZ-d). By (FRZ-b)(iii), g(𝓒°, U_r) = 1_{E₀}Ẑ_r η_{rq}(h(·; 𝓒°)). The fixed-c
value ḡ(c) = ψ_q(c) is FR (FR-b) at c. This is L3's proof (`Theory_work/Wave1/W1-N1/lemmas/L3_freezing.md:25-39`) with its
three inputs re-established at the pin. Agrees.
*`W3-SAMP:MR`.* Its Step 2 g's (`Theory_work/Wave3/W3-SAMP/lemmas/MR_identities.md:57-65`) are of the stated form: they
vanish off A₀ (and off the index range {T(c) ≥ t}, {s ≤ L(c) + 4}, measurable), are measurable by ISL-d (the stage-t
population, the post-terminal populations and Y^i_{q,ℓ} are coordinates of Φ or a finite case split over the order), and
are bounded by B_h C_d (FRZ-d; its Step 3). Their fixed-c values are FR (FR-b) (stage, post-terminal, prefix) and (FR-c)
(the RB clause). So MR's Step 4 holds at the pin. Agrees.
*`W3-SAMP:D` (D-i) freezing step* (`Theory_work/Wave3/W3-SAMP/lemmas/D_theorem.md:26-31`): g = 1{no draw of Φ̃(c, u)
equals S₀} on A₀, 0 off it — an indicator of a measurable set (ISL-d). Agrees.
*Actual record.* By T5 (CAL-d), 𝒜 = 𝒜° ∩ G ⊆ 𝒜° and on 𝒜 the actual calibration fields equal 𝓒°; T5's "Where the T1
flag bites" gives the transfer rules. ∎(FRZ-c)

## (FRZ-d) Evidence bounds
For c ∈ A_s the island's log Ẑ starts at log Z₀ (`cpp/v3_engine.h:299`; T6 (Z)) and adds, at stage t,
inc_t = LSE(Δ_t d(S_i)) − log N_e (`cpp/v3_engine.h:316-322`), i.e. Ẑ_t = Z₀∏_{s≤t} (1/N_e)Σ_i e^{Δ_s d(S_i^{(s−1)})}
under EX-A (FR Part 1). Each factor lies in [e^{Δ_s d_min}, e^{Δ_s d_max}] (Δ_s > 0), and Σ_{s≤t} Δ_s = φ_t, so
Ẑ_t ∈ [Z₀e^{φ_t d_min}, Z₀e^{φ_t d_max}]. Z_t = m(∅)Σ_Ω γ₀e^{φ_t d} with m(∅)Σ_Ω γ₀ = Z₀ lies in the same interval. Hence
Ẑ_t/Z_t ≤ e^{φ_t(d_max − d_min)} ≤ C_d (φ_t ≤ 1), and Ẑ ≤ Z₀e^{d_max}. d is finite on the finite Ω under EX-A (log m
finite, T4 ENC's finite tables). This is L3's bound (`Theory_work/Wave1/W1-N1/lemmas/L3_freezing.md:34-36`) and MR's Step 3
(`Theory_work/Wave3/W3-SAMP/lemmas/MR_identities.md:67-70`). Agrees. ∎

## Line-check verdict
`W1-N1:F`'s freezing step and `W3-SAMP:MR`'s extension (Steps 2–4) hold at the pin, at general c ∈ A₀, with the
potential pair (𝒜°, 𝓒°) (T5's reading); the fixed-c inputs are FR, the measurability W1 (ISL-d).
