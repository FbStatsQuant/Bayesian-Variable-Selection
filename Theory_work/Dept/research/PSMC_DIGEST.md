# PSMC_DIGEST: facts for a "parallel-SMC theory" campaign (research helper, 2026-11-15)

Read-only digest. Pin conventions:
- `CORE` = `Scripts/SMC_BVS/core/`. Its tree hash is the same (1c639ca) on HEAD, origin/main, origin/exp/P1M and
  origin/theory/W3-SCALE, so there is **one** coded method.
- `P1M:` = `origin/exp/P1M:Docs/Experiments/P1M/` (snapshot 781c27a).
- `W3S:` = `origin/theory/W3-SCALE:Theory_work/Wave3/W3-SCALE/` (299cbc5).
- `PLAN:` = `P1M:EXPERIMENT_PLAN.md`; `OD:` = `P1M:OWNER_DECISIONS.md`.
- `T12` = `Docs/Theory/proofs/T12_T8_frozen_run_identities/STATEMENT.md`.

## 1. What the code does (v3.1)

**Islands.**
- There are R′ = 4 final islands, a literal constant (`CORE/v3_run.R:91`).
- They run **serially**, inside one `cpp_final_run` (`CORE/cpp/v3_core.cpp:443-451`).
- Island r uses its own fresh stream 9 + r: `seed_stream(seed, 9+r)` (`:444`). The seed map is x = (seed≪32) + stream
  (`CORE/cpp/v3_util.h:47-48`).
- Final streams 10–13 are independent of the calibration streams 0–9 (`CORE/v3_run.R:22`).

**Shared state.**
- Deterministic objects are shared: start tables and π₀ (`h->st`) and the frozen grid.
- So are a single `Ledger` and a single `ScoreCache` (`v3_core.cpp:407-411`).
- The shared ledger and cache affect only the HPM, stores and counters. They do not affect any particle's law.
- Given 𝒞 the islands are therefore iid, as stated in T12:71 (iv.c). They are **not** independent unconditionally,
  because they share 𝒞 (same line).

**One island** (`run_island_s`, `CORE/cpp/v3_engine.h:274-368`):
1. N iid π₀ draws (`:289`).
2. log Ẑ initialised to log m(∅) + log Z̄₀ (`:299`).
3. At each grid stage t, with incremental weight e^{Δ_t d(S)}:
   - inc_t = LSE(Δ_t d) − log N, added to log Ẑ (`:319-322`);
   - multinomial resampling at **every** stage (`:324`; sampler `:234-266`);
   - one random-order round at φ_t (`:331`).
4. L burn-in rounds at φ = 1 (`:343`), then Hm = 4 measured rounds.
5. RB PIP: p̂_r(j) = (N·Hm)⁻¹ Σ o_j, where o_j is the Gibbs conditional recorded *before* the draw (`:128`, `:364`).

**Pooling** (`v3_assemble_final`, `CORE/v3_run.R:150-163`):
- log Ẑ = LSE_r log Ẑ_r − log R, i.e. the **equal-weight mean of Ẑ_r** (`:154`).
- `log_Z_lower95` = log 0.05 + log Ẑ, a Markov bound (`:155`).
- **`pip_primary` = rowMeans(P), the equal-weight mean of the island RB-PIPs** (`:162`).
- MPM = {pip_primary > ½} (`:163`).
- HPM = best model in the shared ledger over the tables, inherited calibration models, all islands, the final local
  search and LS0 (`:142`; `v3_core.cpp:453-481`). No weights enter it.
- Flag E2 = sd(log Ẑ_r) > 1 (`v3_run.R:183`). It is reported only; it does not trigger a rerun.
- Nothing in the code is Ẑ-weighted. The README confirms this: "retain equal-island primary PIP arithmetic"
  (`CORE/README.md`, production changes, bullet 2).

**Spec vs code (pooling).**
- METHOD_v3.1 specifies the **Ẑ-weighted** PIP as primary and the equal-weight mean as secondary
  (`Theory_work/State_of_Project/sections/02_method.tex:442-448`). That swaps v3, where equal weights were primary
  (`:451`).
- The frozen core computes only the equal-weight mean and calls it `pip_primary` (`:819`).
- T12 defines "primary P̄ = ¼Σ PIP̂_r, secondary P̃ = Ẑ-weighted" (T12:52). W3-SAMP uses pip_primary = ¼Σ p̂_r
  (`Theory_work/Wave3/W3-SAMP/STATEMENT.md:53-55`).
- The campaign must name which object it calls "primary".

**N, calibration, LS0.**
- N₀ = max(2500, n, p), H₀ = ⌈512N₀/2500⌉, T₀ = max(1000, ℓ²); tier 1 multiplies each by 4
  (`CORE/v3_preprocess.R:25-30`). The final N comes from the budgets (`v3_run.R:90`).
- Calibration (`CORE/v3_calib.R:28-137`) runs in this order:
  1. an adaptive pilot (CESS-type rule: population ESS ≥ 0.9H, floor 1/T_e; `cpp/v3_calib.h:30-45`);
  2. a grid built on the **finite candidate set V** with restricted ρ_V(u, v) ≥ 0.90 per interval
     (`v3_calib.h:61-96`);
  3. up to ℓ rebuilds, each with 4 diagnostic islands (streams 1–4 or 6–9);
  4. triggers E1/E2/E3/forced/grid-failure ⇒ one escalation to tier 1 (`v3_calib.R:101-110, 150-158`);
  5. the tier-1 grid-failure fallback, C-DLV B (`:122-125, 163-169`).
- The paper's own caveat: the grid "controls restricted one-step weight dispersion only; it does not control
  full-space ESS, particle occupancy, mixing, or modes never scored" (`02_method.tex:330-331`).
- LS0 runs one local search from the start mode after the final search, on the shared ledger. It reads no uniforms
  (`CORE/README.md` §v3.1; `v3_core.cpp:462-469`).

## 2. Engineering Department's spec (P1M, draft v0.1, 2026-11-15)

**Engine ("v4").**
- A standalone C++ binary with subcommands setup → calibrate (4×96 CPUs) → `island --id r` (16×96) → merge (union
  store and HPM, then final local search and LS0) (`P1M:ENGINEERING_STRATEGY.md:24-33`).
- Islands run as processes with no communication.
- Inside an island, threads run over particles. Each particle has its own xoshiro stream seeded by
  SplitMix64(seed, island, stage, particle), and reductions run in particle order (`:53-58`).
- A "compat mode" must reproduce v3.1 bit for bit (`:60-61`).

**Output-preservation contract (tags, `PLAN:12-14`).**
- [OP-bit]: same bits as v3.1.
- [OP-law]: same law, different bits or stream use.
- [Δ𝒞]: only how 𝒞 is computed changes.
- [Δlaw]: same target, different sampler law.

Gates:
- T1/T2: kernels and compat mode bit-identical to v3.1.
- T3: thread invariance.
- **T4: law check.** Compat vs production over 200 seeds at p ≤ 1k, with two-sample tests on log Ẑ, PIPs, HPM
  frequency and stage counts (`ENGINEERING_STRATEGY.md:78-87`).

O17, the HQ ruling for process-parallel islands: "identical" covers every statistical output and every published or
theorem-check quantity. Only `fresh`/cache counters fail (`W3S:DESIGN_v1.md:67-71, 125-135`; `W3S:CHECKPOINT_2.md:82-87`).

**The production path is not bit-identical.** The owner's wall-time limit flipped OD-8 to (b), per-particle streams
[OP-law] (`OD:119-127`). Fixed N is [Δlaw]/[Δ𝒞] (G10, `PLAN:221`), and the 1M partition rule is [Δlaw] on π₀
(OD-5, `OD:53-63`). So HQ_NOW's "output-identical engine ⇒ inherited guarantees"
(`origin/main:Theory_work/Wave3/HQ_NOW.md:82`) holds for compat mode only. Production needs **in-law** transfer plus
premise re-checks.

**Theory items the 1M run names** (`PLAN:226-227`, `PLAN:47-51`, `OD:13`):
- **T-N** (= O4): restate TH01(e)(f)(i), TH06 and TH08 for general (N, R′); confirm that RM-0, LT♯, TR and D need
  nothing. Sized "≤ 1 Opus leg (HQ_NOW: short Opus note)".
- **T-PART**: does START/START2/RM2/(V) use any partition property beyond "blocks ≤ B built from |r|"?
- Claim C7 is listed as "measured, not claimed: unbiased pooling holds (N1, O1, O19; O2 is open)".
- Also needed: O5 (counter-based streams: EX-S/IND-T, Prop W) for OD-8(b). OD-2(b) asks to "check that no delivered
  theorem uses E2".

**Open owner decisions touching theory.**
- **OD-1 fixed N = 2,500 per island.** Recommended, since it is the only option under which 1M exists. Its theory
  note: "RM-0 is pathwise for every N_e; LT♯ and TR hold for any N_e and frozen schedule; D holds per draw"
  (`OD:9-18`).
- **OD-2 E2 does not escalate in fixed-N mode.** Recommended; this is [Δ𝒞] (`OD:20-31`).
- **OD-4 keep equal-weight PIP primary, report PIP_Z, R_eff/R′ and max W_r.** Reason: "max |PIP_Z − PIP_eq| ≤ 0.0023"
  over 25 fits and 6 B3 runs, and "PIP_Z is exactly the estimator that degenerates" (`OD:44-51`). HQ's hybrid (union
  HPM, evidence-weighted PIPs with an R_eff fallback) is kept as secondary (`P1M:BRIEF.md:57-64`).
- **OD-8(b) per-particle streams** (`OD:119-127`).
- **OD-9 R′ = 16**, plus a 64-island census at 10⁴/10⁵ (`OD:96-101`).
- Risk R1 states the policy on log Ẑ dispersion: "report, never switch on it" (`PLAN:291`).

## 3. W3-SCALE and SCALING_DESIGN_v0: measured evidence dispersion

**B3 census** (`W3S:CHECKPOINT_2.md:44-72`; `W3S:results/b3_census.tsv`):
- Setup: one dataset per p, tier-0 grid frozen (H = 512), R islands per N, no escalation.

| p | N | islands | σ̂ | robust σ̂ | max−median | R_eff/R | max W | T |
|---|---|---|---|---|---|---|---|---|
| 2k | 2,500 | 16 | 0.086 | 0.154 | 0.16 | 0.99 | 0.07 | 33 |
| 2k | 10,000 | 16 | 0.029 | 0.048 | 0.06 | 1.00 | 0.07 | 33 |
| 5k | 2,500 | 16 | 0.755 | 0.999 | 1.72 | 0.56 | 0.22 | 36 |
| 5k | 10,000 | 14 | 1.348 | 0.544 | 4.39 | 0.11 | **0.79** | 36 |
| 10k | 2,500 | 6 | 1.152 | 0.959 | 2.56 | 0.33 | 0.69 | 28 |
| 20k | 2,500 | 11 | 0.954 | 0.723 | 2.49 | 0.38 | 0.42 | 30 |

- At 2k, ×4 N shrinks σ̂ by 2.9× (1/√N predicts 2×).
- At 5k, the bulk narrows and "the median log Ẑ_r rises by 0.7", but one island sits 4.4 above the median and carries
  79% of the weight (`:62-64`).
- Every island found the same best model (= truth); per-island PIP sd ≤ 0.001; max_j |PIP_Z − PIP_eq| ≤ 0.0005
  (`:65-66`).
- p is confounded with the dataset and the seed. The 10k row has only 5 df (`:59, :71-72`).

**Earlier data** (`W3S:DESIGN_v1.md:165-198`):
- Final islands at N = 2,500: median σ̂ 0.065 at p = 500 and 0.088 at p = 1k (max 0.70).
- Escalated fits at N = 10⁴: σ̂ 1.00 and 0.82.
- 5k diagnostic islands: 0.49–2.52; a tie design gave 5.7–6.1.
- W3-P6 E2 rate at n = 50: 0/137 → 6/16 as p goes 50 → 500 (`:189-192`).
- Grids have T ≈ 26–40 stages and do not grow visibly with p up to 20k (`:20`; table above).

**Diagnosis given: none.** The ticket states "**Not known:** … why the right tail occurs (no mode-occupancy record
exists)" (`DESIGN_v1.md:197-198`). The only mechanisms on record are:
- the restricted-V caveat (§1 above);
- "one poor shared grid impairs every final island" (`DESIGN_v1.md:207`);
- O2: "the restricted-ESS grid controls dispersion on V only … open research; the main statistical risk"
  (`Theory_work/Pause_2026-11/SCALING_DESIGN_v0.md:451`).

Two observations, mine, not on record:
1. A median log Ẑ_r that rises with N, plus a lone high island, is the signature of E Ẑ_r = Z carried by rare
   islands (Jensen: E log Ẑ_r < log Z, T12:66, :69). This is an under-estimation-with-rare-recovery picture, not a
   symmetric noise picture.
2. Since T is flat in p, the growth is not "more stages". It points to unscored or under-occupied mass outside V.

**Revision D** (6866f57): output bit-identical to v3.1. PROD-H 24/24 and supplementary 10/10 are IDENTICAL; tables,
Gram and routes are identical at 5k/10k/20k. Setup is 3.7× faster (85.8 → 22.8 s at 20k). Steps run 1.69 → 1.22 µs
at 2k and 1.76 → 1.27 µs at 20k (about 28% faster). No Sol code review was done; the claim rests on the gate
(`W3S:CHECKPOINT_2.md:11-12, 20-34`). HQ accepted it 2026-11-13 (`W3S:LOG.md:239`).

**Merge theory already drafted** (`W3S:DESIGN_v1.md:151-163`; `SCALING_DESIGN_v0.md:350-388, 446-470`):
- PIP_Z = Σ W_r p̂_r is consistent as R′ → ∞ at fixed N, with a CLT and a ratio bias of −Cov(ω(H−μ), ω)/R′.
- "PIP_eq is consistent in R′ only if each island is itself unbiased" (`DESIGN_v1.md:162`).
- R_eff/R′ ≈ e^{−σ²} for log-normal Ẑ (`:182`).
- Obligation list O1–O21: O1 merge CLT; **O2 degeneracy (open)**; O3 census; O4 general N; O5 streams; O17–O20
  (`DESIGN_v1.md:226-247`).
- O1(c): "N1 does not cover the shipped Rao–Blackwellised PIP at all" (`:233`). **T12 (ii) does**:
  E_c[Ẑ·PIP̂_j] = Z·PIP_j (T12:64, PROVED-LOCKED; registry `SOP:TH110`). W3-SAMP MR-c gives it given 𝒞
  (`W3-SAMP/STATEMENT.md:113-116`). So O1(c) is discharged by citation.

## 4. Existing theory to build on

Registry rows from `Theory_work/INFRA/registry/claims.tsv` (row number = file line). Statuses are verbatim, truncated.

| claim (row) | content | status | pin |
|---|---|---|---|
| SOP:TH110 (12) | T12: frozen-run evidence; (i) E[Ẑ_t q̂_t f] = Z_t q_t f; **(ii) RB identity**; (iii) pooled Ẑ unbiased, Jensen and Markov bounds; (iv.b) both normalised PIPs biased (example); (iv.c) islands iid only given 𝒞; (iv.e) conditioning on E2-pass breaks the identities | "PROVED-LOCKED (all parts (i)-(iv), wave 1); not adopted" | T12:58-73 |
| W1-N1:Thm-N1 (31) | E[Ẑ_r H_r(h) \| 𝒞] = Zπ(h) (plain endpoints), R′ = 4k, uses only SI (no inter-island independence) | "PROVED-CHECKED" | `Wave1/W1-N1/STATEMENT.md:98-104` |
| W1-N1:Cor-E (32) | E[W_r\|H_r(h) − h(S₀)\|] ≤ δ₁ | "PROVED under the same premises" | `:108-111` |
| W1-N1:F (35) | freezing lemma | "PROVED under the named premises…" | `lemmas/L3_freezing.md:21-23` |
| W3-SAMP:MR (350) | MR-a/b/c incl. E[W_r p̂_r(j) \| 𝒞] = π(j∈S) | "PROVED-CHECKED" | `Wave3/W3-SAMP/STATEMENT.md:107-116` |
| W3-SAMP:D (352) | draw discovery; (D-ii) union over islands, exponent 4D_r under IND-T | "PROVED-CHECKED" | `:97-105` |
| W3-SAMP:LT# (353) | per-island PIP/MPM transfer via P(W_r < η); (LT-d) ‖pip_primary − 1_{S₀}‖ ≤ max_r ‖p̂_r − 1_{S₀}‖ | "PROVED-CHECKED" | `:126-140` |
| W3-SAMP:LT#(f) (354) | necessity of NC_r | "OPEN; nothing claimed" | `:141-147` |
| W3-SAMP:C (355) | concentrated bridge; **(C-iii) T-free, N-free E\|W_r − 1\| ≤ 2δ̄** | "PROVED-CHECKED" | `:149-163` |
| W3-SAMP:TR (356) | terminal repair; PIP/MPM consistency with **no condition on Ẑ, bridge, N_e or grid** | "PROVED-CHECKED" | `:165-177` |
| W3-RM:RM-0 (368) | reported model = S₀ **pathwise for every seed, N_e, R′ and calibration outcome** | "PROVED-CHECKED" | `Wave3/W3-RM/STATEMENT.md:160-176` |
| W3-RM2:RM2-F / RM2-R (449-450) | polynomial leakage; same "every seed, N_e, R′" clause (`:209`) | "PROVED-CHECKED, conditional on SOP:TH09" / "…on W2-APP:POST" | `Wave3/W3-RM2/STATEMENT.md:206-218` |
| W3-START:START-F/R, W3-START2 (419-448) | start mass π₀(S₀) → 1; π₀ depends on the partition (T-PART) | "PROVED-CHECKED" | `Wave3/W3-START{,2}/STATEMENT.md` |
| C-PACK:SL1/SL2 (72, 74) | PIP corollaries | "PROVED; XF-checked (R34 …)" | `Wave1C/C-PACK/lemmas/I4_SL_corollaries.md` |
| C-DLV:Thm-D (122), Prop-F (125) | delivery reduction; tier-1 fallback | "PROVED-CHECKED (relative to the P1/P3 audits)"; "PROVED-CHECKED for the patched calibration law" | `Wave1C/C-DLV/lemmas/L4_delivery.md:13-22, 79-84` |
| C-DLV:O (126) | open obstruction | "OPEN" | `Wave1C/C-DLV/STATEMENT.md:79-84` |

- The registry has **no row** for O1/O2, R′ > 4 merge, or evidence-variance growth.
- TH01 (e)(f)(i) are the islandwise, finite-R′ and growing-R′_n clauses (`Theory_work/State_of_Project/sections/04_theory.tex:126-130`).
- Many statements hard-code R′ = 4: T12 CAL (T12:50), W3-SAMP (`STATEMENT.md:31, 42`) and LT-d's Σ_{r≤4}.

## 5. Literature already collected (local)

Worktrees are at `/home/fb31/Misc/api_workers/LIT-{PAR,SMC}/theory_campaign/LIT-{PAR,SMC}/`, not under
`/home/fb31/api_workers`.

- **Island particle model** (Vergé–Dubarry–Del Moral–Moulines 2015, arXiv:1306.3911): with independent islands, the
  variance is ∝ 1/(N₁N₂), but "the bias is independent of N2 and is inversely proportional to N1" (equal-weight
  average) (`LIT-PAR/notes/03_parallel_smc_depth.md:13-21`).
- **Whiteley–Lee–Heine 2016 (α-SMC)**, §5.1: at fixed q and s → ∞ the Ẑ-weighted pool converges a.s.; plain
  averaging does not. E[(Ẑ^{(q,s)}/Z − 1)²] = (1/s)·E[(Ẑ^{(q,1)}/Z − 1)²]. A single run's relative second moment "can
  grow exponentially" at fixed q (`notes/03:33-40`).
- **Dai–Heng–Jacob–Whiteley 2022**, §4.2 eq. (4.8): Σ Ẑ_r π_r(φ)/Σ Ẑ_r → π(φ) at fixed N. Tuning adaptively may break
  unbiasedness, so the grid is frozen (`notes/07_island_pooling_standard.md:3-17`). The note concludes T31(i) is
  standard; the only novelty is "given the frozen calibration".
- **Syed–Bouchard-Côté–Chern–Doucet** (arXiv:2408.12057; local PDF
  `Papers/Core_bibliography/02_2026_Syed_et_al_*.pdf`), under an idealised performance model:
  - Var[Ẑ/Z] = Π_t(1 + (e^{D_t} − 1)/N) − 1, with D_t the per-stage Rényi-2 divergence;
  - T·Var → E(φ)/N ≥ Λ²/N;
  - in d weak copies, Λ ∝ √d; sparse schedules need N exponential in d (`notes/03:63-72`).
- **Le Fay–Chopin–Vihola 2026** (local PDF `24_2026_Le_Fay_*`): CLT for log(Ẑ_T/Z_T); σ² = Ω(T/γ) when weights
  align with the slowest kernel mode (pdftotext l. 776-810).
- **Cérou–Del Moral–Guyader 2011**: an exact second-moment decomposition with no mixing assumption, and relative
  variance linear in stages under mixing (`LIT-SMC/REPORT.md:160-175`).
- **Dau–Chopin 2022**: log-L CLT (local PDF, l. 655).
- **Beskos–Crisan–Jasra 2014 and Beskos–Jasra–Kantas–Thiery 2016**: abstracts only (`LIT-SMC/REPORT.md:78-79`).
- **Project record:** FAILED_ROUTES RF273, "more islands always helps" is false for equal-weight PIP
  (`Theory_work/INFRA/FAILED_ROUTES.md:170`).
- **Not local; from memory, verify:**
  - Bérard–Del Moral–Doucet (EJP 2014), log-normal CLT for log Ẑ with T ∝ d;
  - Schweizer 2012;
  - Chopin 2004; Del Moral 2004;
  - Jasra et al. 2011;
  - Ionides 2008 (truncated IS) and Vehtari et al. (PSIS), for trimmed weights.
- No local source treats Var(log Ẑ) for discrete or BVS targets, or compares pooling rules at σ ≈ 1.

## 6. Candidate theorems (suggestion)

**P1. In-law transfer (the HQ_NOW note, made exact).**
- *Statement:* if the v4 output is (law given 𝒞) a deterministic merge of R′ conditionally iid copies of I(𝒞) with
  any (N, R′, frozen grid), then every given-𝒞 result transfers verbatim, with 4 → R′ and N_e → N: T12 (i)–(iii), N1,
  MR, D, LT♯, C, TR and RM-0(b).
- The [OP-bit] / [OP-law] / [Δ𝒞] / [Δlaw] ladder says which premise each engine change touches: streams → EX-S (R3);
  E2 off → CAL only; partition → START.
- *Consumes:* T12 §2, N1 SI, W3-SAMP's component clause, RM-0(b), and the gate T4 as empirical side.
- *Difficulty:* restatement plus assembly. It *is* T-N.
- *Gain:* the 1M paper section can say "guarantees hold for the shipped parallel engine".
- *Risk:* per-particle streams must still realise (R3) within-round independence. "Identical" must not be claimed for
  production mode.

**P2. Pooling-rule-free PIP/MPM consistency.**
- *Statement:* for **any** weights w ∈ Δ_{R′}, even output-dependent ones (equal, Ẑ, trimmed),
  ‖Σ w_r p̂_r − 1_{S₀}‖_∞ ≤ max_r ‖p̂_r − 1_{S₀}‖_∞. Hence E-bounds R′(g + e_L) under TR, or R′(g + β/2) under C. MPM
  and PIP are consistent when R′_n(g + e_L) → 0, with no condition on Ẑ.
- Corollary: if the islands agree within ε, all rules differ by ≤ ε deterministically.
- *Consumes:* TR, C, LT♯(d).
- *Difficulty:* assembly (a few lines).
- *Gain:* makes OD-4 a theorem. Evidence noise cannot hurt selection or PIPs.
- *Risk:* it is consistency to 1_{S₀}, not to π(j ∈ S). The intermediate-PIP regime (weak signal) is not covered.

**P3. Evidence dispersion: upper bound and honest limit.**
- (i) Upper: P(|log Ẑ_r − log Z| > u | 𝒞) ≤ β/(1 − e^{−u}) with β ≤ 2δ̄. This is T-, N- and p-free. Dispersion
  vanishes whenever start or posterior concentrate (from C-iii).
- (ii) Limit: an abstract (π, π₀, grid) family, design-agnostic, with p ≤ n^A, in which a set A of posterior mass ≥ c
  is unreached by fixed-N islands with probability → 1. Then log W_r → −∞ in probability while E W_r = 1, so σ(log Ẑ_r)
  is unbounded at fixed N and calibration, and R_eff/R′ → 0 for any fixed R′. Also show that ρ_V ≥ 0.9 on V does not
  bound the full-space D_t.
- *Consumes:* C-iii, T12 (iv.a), Cérou–DM–G's second-moment identity.
- *Difficulty:* (i) restatement; (ii) a new key lemma (a mass-transport or bottleneck argument).
- *Gain:* explains B3 and turns R1 into a stated limit.
- *Risk:* (ii) may need a mixing or bottleneck hypothesis that reads as design-specific. Keep it at the level of
  (π, π₀).

**P4. Robust evidence pooling with a guarantee.**
- *Statement:* trimmed weights w_r ∝ min(Ẑ_r, τ_{R′}·m̂) or tempered Ẑ_r^α, with the rule declared before stream 10.
  As R′ → ∞ with τ → ∞ and τ = o(R′), the pooled μ̂(h) → π(h) using only E[W_r | 𝒞] = 1 (T12 ii, MR-c). The bias is
  ≤ E[W 1{W > τ}] and the MSE is O(τ/R′ + bias²).
- Combined with P2, the rule is never worse than equal weights in the concentrated regime.
- *Consumes:* N1/T12(ii), IND-T for R′ islands, O3 (rule measurability).
- *Difficulty:* assembly; truncated IS is known (from memory, verify).
- *Gain:* a principled secondary PIP_Z that does not collapse onto one island (the 79% case).
- *Risk:* an adaptive R′ or τ using final outputs is forbidden (`02_method.tex:389`; T12 iv.e). The rate needs a tail
  condition that P3(ii) may show fails.

**P5. Ẑ-weighted merge CLT with an effective-island law (O1).**
- *Statement:* μ̂_Z → π(h) a.s.; √R′ CLT; R_eff/R′ → 1/E[W² | 𝒞] a.s., for the coded RB PIP.
- *Consumes:* MR-c and T12(ii); Whiteley–Lee–Heine §5.1; Dai et al. (4.8).
- *Difficulty:* restatement (cite as standard).
- *Gain:* C7's "unbiased pooling holds" becomes a theorem about the coded RB output.
- *Risk:* none mathematically. 1/E[W²] is not uniform in p, which ties back to P3.

**P6. Union-HPM and discovery under R′ islands.**
- *Statement:* HPM(R′) ⪰ HPM(4) pathwise. RM-0/RM2 hold for every R′. Discovery
  P(S₀ ∉ ∪𝓜_r | 𝒞) ≤ (1 − π₀(S₀))^{R′·D_r} under IND-T for R′ streams.
- *Consumes:* RM-0(b), D(ii), Lemma S/O10.
- *Difficulty:* restatement. The IND-T extension and O18 are premises.
- *Gain:* the 1M selection claim C2 needs no evidence weights.
- *Risk:* the IND-T audit beyond 4 streams is not discharged (N1 §2 SI, `W1-N1/STATEMENT.md:80-82`).

**Suggested scope.** P1, P2, P5 and P6 together are the "short Opus note" for 1M (restatements and assembly, ≤ 1–2
legs). P3(ii) and P4 are the research core for the scaling paper.
