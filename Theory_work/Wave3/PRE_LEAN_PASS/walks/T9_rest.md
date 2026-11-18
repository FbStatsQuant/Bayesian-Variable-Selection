# Walk T9-rest — row 3.5 (the evidence estimate is unbiased) and row 4.1 (pooling over the four islands)

Walker: Fable-CT-D (Fable 5.2, Claude Third). Depth: standard walk. Snapshot: origin/main at branch creation
(`theory/PRE-LEAN-walkD`). Masters: `W1-N1:Thm-N1@1.0.0` (`Theory_work/Wave1/W1-N1/STATEMENT.md:98-104`),
`W3-READER:PoolZ@1.0.2` (`Theory_work/Wave3/W3-READER/STATEMENT.md:12-39`), `W3-SAMP:LT#@2.0.6` clause (LT-d)
(`Theory_work/Wave3/W3-SAMP/STATEMENT.md:134-135`).

## Findings

| # | Severity | file:line | Claim | Why |
|---|---|---|---|---|
| F1 | MINOR | `Theory_work/Wave3/W3-READER/STATEMENT.md:14-20, 25-27`; registry row `W3-READER:PoolZ` (depends_on) | PoolZ is a claim about main's core (`Scripts/SMC_BVS/core/v3_run.R:91, 154`) and is proved by citing `W1-N1:Thm-N1` alone | N1 and its code bridge (Lemma B) are stated for the frozen v2.2.1 core (`W1-N1/STATEMENT.md:14-15`; `lemmas/L1_bridge.md:4, 27-31`). The step "N1's bridge holds for main's island" is recorded, but elsewhere: `W3-SAMP/lemmas/CC_code_check.md:9-21` (CODE-CHECKED at 4676af6) and `W3-SAMP:MR` (MR-b) with h ≡ 1, which is E[W_r \| 𝓒] = 1 on main's core. PoolZ's proof does not cite either, and its depends_on lists only `W1-N1:Thm-N1@proof:linearity`. A missing edge, not a wrong step: the result stands. Fix: cite `W3-SAMP:MR` (MR-b) or `W3-SAMP:CC` in the proof and add it to depends_on. |
| F2 | MINOR | `Theory_work/Wave3/W3-READER/STATEMENT.md:22-23, 33-36` | "Under the joint data/algorithm law … the same identity holds conditionally on (data, 𝓒)", hence E[1_𝒜Ẑ] = E[1_𝒜Z] | N1 is a fixed-data statement; its measurability premise MEAS is joint in (calibration value, stream) at fixed data (`W1-N1/STATEMENT.md:83-85`). Passing to a conditional expectation given (data, 𝓒) needs the island record and Z to be jointly measurable in the data as well, plus independence of the final stream from (data, streams 0–9). The independence is stated (H-U/SI under the joint law, `W3-SAMP/STATEMENT.md:35-36`); the measurability in the data is used but stated nowhere I could find. It is true for the coded map (finitely many arithmetic operations and comparisons), so no result changes. It blocks a Lean statement of the joint-law clause, and of the card's "given the frozen calibration and the data" if read as a conditional expectation rather than "for each fixed data set". Also: the unconditional equality holds in [0, ∞] (Ẑ ≥ 0, Tonelli); finiteness of E[1_𝒜Z] is neither shown nor needed. |
| F3 | NOTE | `Theory_work/Wave3/W3-READER/CLAIMS_CARD.md:76, 97` | "On completed runs this quantity equals the printed evidence" | Main's core now prints two evidence fields: `log_Z` (pooled estimate, `v3_run.R:154`) and `log_Z_list` (`v3_run.R:236-266`, row 3.1L). PoolZ covers exp(`log_Z`) only. The master pins the line, so it is unambiguous; the card rows should name the field. The R-only drift 4676af6 → main (`v3_fit.R`, `v3_run.R`; no cpp change) leaves `:91`, `:154`, `:160` as cited — I checked them on the working tree. |
| F4 | NOTE | `Theory_work/Wave1/W1-N1/STATEMENT.md:70-90` | N1 "PROVED-CHECKED" | Proved under named premises that Lean can only take as hypotheses: EX-A, H-U (idealisations), START and KERNEL (code bridges, inherited status "PROVED (candidate), code-checked"), CAL, SI, MEAS, potential run. The reader carries them in words (`READER_VERSIONS.md:62-70`). The Lean-formalisable content is Lemma P (the SMC unbiasedness induction on a finite state space), Lemma F (freezing) and linearity; Lemma B is a code bridge and stays outside. |

No FATAL or MAJOR finding.

## 0. Presented statements against the masters

* **Row 3.5.** "On calibration success, given the frozen calibration and the data, the equal-weight mean of the four
  potential uninterrupted evidence records has expectation Z" = PoolZ: data fixed, a.s. on 𝒜, E[Ẑ | 𝓒] = Z,
  Ẑ = ¼Σ_{r≤4}Ẑ_r. Law: the final streams only; conditional on 𝓒; localised on 𝒜 ∈ σ(𝓒); holds for every n (not
  asymptotic). "No unbiasedness conditional on completion" and "no condition on the design" agree with N1 §5 and
  PoolZ. The statement is about Ẑ, not about the printed log Ẑ. ✓ (F2 on "given … the data"; F3 on "printed evidence".)
* **Row 4.1, first clause.** "The pooled PIP is the equal-weight island mean, so its sup-norm error is at most the worst
  island's" = (LT-d), first inequality. Deterministic; holds for any reference vector. ✓
* **Row 4.1, second clause** = PoolZ, as row 3.5. ✓
* Reader remark (`READER_VERSIONS.md:1320-1322`) matches PoolZ. ✓

## 1. Lemma P (post-terminal identity, fixed calibration value) — `W1-N1/lemmas/L2_post_terminal.md`

Fixed data, fixed c: grid 0 = φ₀ < … < φ_T = 1, N ≥ 1, then rounds at φ = 1. Ω finite, γ_φ > 0.
* (bridge) Z_{t−1}q_{t−1}(G_tf) = Z_tq_t(f): γ_{φ_{t−1}}e^{Δ_td} = γ_{φ_t}. ✓
* (P-a), t = 0: Ẑ₀ = Z₀ deterministic, starts iid π₀ = q₀ (R1). ✓
* (P-a), step: Ẑ_t = Ẑ_{t−1}·(1/N)Σ_lw^l is measurable before the resampling (the text says 𝓗-measurable; it is even
  𝓕-measurable); multinomial resampling (R2) gives E[(1/N)Σ_lw^l·(1/N)Σ_ig(Y^i) | 𝓕] = (1/N)Σ_kG_t(X^k)g(X^k) ✓; the
  round (R3) gives K_{φ_t}f ✓; induction with the function G_t·K_{φ_t}f, then (bridge) and q_{φ_t}K_{φ_t} = q_{φ_t}. ✓
* (P-b): rounds at φ = 1 leave Ẑ unchanged; invariance of π under K₁. ✓ Z_T = Z and q_T = π because φ_T = 1.
Used: finite Ω, positivity, (R1)–(R3), invariance of each round kernel (state-independent uniform order). No
independence across islands, no stationarity, no design condition. Order of the coded operations (weights from the
current population, increment, resampling, one round at φ_t) agrees with the recursion (`W1-N1/STATEMENT.md:35-41`).

## 2. Lemma B (code bridge) — `W1-N1/lemmas/L1_bridge.md`

Read as a recorded code-level claim; the arguments I checked:
* (B-a) control flow gives Ẑ_r = m(∅)Z̄₀∏_t(1/N_e)Σ_ie^{Δ_td(S_i)} under EX-A and START. ✓
* (B-0) the statistical record is a function of (c, u): the score cache and ledger, shared across islands, do not feed
  transitions under EX-A. ✓ This is what makes each of the four potential records a function of its own stream.
* (B-b) each operation starts at a stopping time and reads a bounded number of fresh uniforms; strong Markov property
  of an iid sequence. (R2): the coded resampler returns min{k : W_k ≥ u}, so P(a_i = k) = w_k/Σw. ✓ (R1) by START,
  (R3) by KERNEL and Fisher–Yates. ✓
Not re-checked against source lines: the kernels (N9) and the start sampler (START). Code pin: v2.2.1 core (F1).

## 3. Lemma F (freezing) — `W1-N1/lemmas/L3_freezing.md`

g(c, u) := Ẑ(Φ(c, u))·η_q(Φ(c, u))(h(·; c)) on A₀, 0 elsewhere. Jointly measurable (countable partition by N_e) ✓;
bounded: Ẑ ∈ [Z₀e^{min d}, Z₀e^{max d}] because ΣΔ_t = 1, Δ_t > 0, a bound free of c ✓. 𝓒 independent of U_r (SI, CAL) ⇒
E[g(𝓒, U_r) | 𝓒] = ḡ(𝓒) a.s. ✓ Localised form E[1_{E₀}Y | 𝓒] = 1_{E₀}ψ(𝓒) on E₀ = 𝒜 ∩ {r ≤ R′} ∈ σ(𝓒). ✓
Every premise is used: H-U (law of U), SI (independence), CAL (𝓒 is a function of streams 0–9), MEAS (joint
measurability), boundedness of h.

## 4. Theorem N1 — `W1-N1/lemmas/N1_theorem.md`

Lemma F, then for c ∈ A₀: Lemma B identifies Φ(c, U) with the frozen island, Lemma P gives ψ_q(c) = Zπ(h(·; c)).
(N1) = average over q; h ≡ 1 gives E[Ẑ_r | 𝓒] = Z; Z > 0 is a constant (data fixed). ✓ Event: a.s. on 𝒜 ∩ {r ≤ R′},
fixed r; probability over the final stream only.

## 5. PoolZ — `W3-READER/STATEMENT.md:12-39`

* On 𝒜, R′ = 4 (`v3_run.R:91`, `islands = 4L`; `W3-SAMP/STATEMENT.md:42`), so E₀ = 𝒜 for r = 1..4; four null sets. ✓
* Linearity: E[Ẑ | 𝓒] = ¼Σ_rE[Ẑ_r | 𝓒] = Z a.s. on 𝒜. ✓ No independence between islands is used. ✓
* Code: `log_Z = v3_log_sum_exp(logZr) - log(R)` at `v3_run.R:154`, computed only when the status is "completed"
  (`:142-147`), which is the "potential record; equals the printed field on completed runs" reading (Lemma PC,
  `W3-SAMP:PC`). ✓ Main's core is serial, so N1's worker-equivalence premise is not engaged.
* Code transfer v2.2.1 → main: F1. Joint-law clause: F2.

## 6. (LT-d), pooled PIP — `W3-SAMP/lemmas/LT_theorem.md:53-55`

pip_primary = ¼Σ_rp̂_r (`v3_run.R:160`, `rowMeans(P)`; CC3), so for every j
|pip_primary(j) − 1{j ∈ S₀}| ≤ ¼Σ_r|p̂_r(j) − 1{j ∈ S₀}| ≤ max_r‖p̂_r − 1_{S₀}‖_∞. ✓ Triangle inequality only. The
remaining clauses of (LT-d) (MPM, HPM) are not part of row 4.1 and were not walked.

## 7. Boundary of this walk

Walked: Lemma P, Lemma F, Theorem N1, PoolZ, (LT-d) first inequality; Lemma B at the level of its argument. Not
opened: T12's proof text (Lemma P re-derives the clause used), N9 (START, KERNEL), `W3-SAMP:PC`, `W3-SAMP:MR`.

**WALK COMPLETE** (to recorded inputs; boundary as in §7).
