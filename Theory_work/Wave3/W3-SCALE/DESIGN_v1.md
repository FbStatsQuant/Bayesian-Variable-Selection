# DESIGN_v1 — many-island SMC-BVS on NOTS, from measured numbers (W3-SCALE leg A)

**Status:** design only, revision 3 (after the Astra break reviews R03 and R04, `reviews/R03_design_astra.md`,
`R04_design_astra.md`; dispositions `reviews/R03_disposition.md`, `R04_disposition.md`). Revision 3 is not re-reviewed. It replaces the extrapolations of `Pause_2026-11/SCALING_DESIGN_v0.md` by leg A's
measurements and keeps v0's notation and tags ([OP-bit], [OP-law], [Δ𝒞], [Δlaw], UNVERIFIED). Nothing here changes
the method. The two questions reserved for the owner are framed in §7 and **not decided**.

**Evidence base, and its limits.** One thread on NOTS sapphirerapids nodes (Xeon Platinum 8468), GCC 14.3.0, R 4.5.2,
pinned flags; n = 200. Three profiles of v3.1 (p = 1k: PROD-H `p1000_S3_r001_c100`; p = 2k: one S3-type dataset; p = 20k:
one S3-type dataset, one pilot island and one final island with N = 2,500); p = 5k: one S3-type dataset, calibration
escalated to tier 1, completed in leg B (12.2 h on one Sapphire Rapids node; folded in 2026-11-12); 24 PROD-H fits (one replicate per p × S × c cell) and one tie design. One seed each, R = 4
islands per fit. Every statement below that goes beyond these runs is marked. Source tables: `results/*.tsv`
(scripts in `analysis/`). Memory is in GiB (2³⁰ bytes).

## 1. What changed since v0

| v0 statement | leg A measurement (source) | consequence |
|---|---|---|
| elementary step ≈ 3 µs (local i7) | bridge stages 1.14 / 1.16 / 0.90 µs, rounds at φ = 1 1.64 / 1.90 / 1.80 µs at p = 1k / 2k / 20k (`profile_v31_step_cost.tsv`) | at T = 30 an island costs 51.6 µs per particle and predictor against v0's 126: 0.41 of v0's estimate |
| T = 30, UNVERIFIED | final grids 26–40 stages over the 24 PROD-H units (median 32.5 at p = 500, 31 at p = 1000), 33 at 2k, 29 at 20k with N = 2,500; pilots 20–30 (`leg_a_units_calibration.tsv`, `profile_v31_stages.tsv`) | v0's 30 holds on these designs; how T moves with p beyond them is not established |
| calibration ≈ 2.6 final-island equivalents (I = 3) | rebuilds I: 2–8 (median 4) at p = 500, 2–10 (median 6) at p = 1000, 8 at 2k, 11 at 5k (then an escalation); calibration / (calibration + final) time: median 0.45 at p = 500, 0.56 at p = 1000 (tier-0 units), 0.51 for the 1k profile, 0.62 at 2k | calibration is 30–69% of calibration + final time on these units (median 45% and 56%), and it is sequential (§2) |
| setup dominated by complete linkage | v3.1 at 20k: Gram 16.4 s, blocks 25.5 s, neighbour graph 59.1 s, tables 0.5 s; setup peak 9.24 GiB resident (the three dense p × p arrays are 24 p² = 8.94 GiB) (`leg_a_setup_compare_roundA.tsv`) | the neighbour graph was the largest setup cost; fixed bit for bit (§3) |
| preflight refusal from p ≈ 2.3k (by reading) | v3.1's LS0 charge against 24 h: 11.2 h at 2k (admitted), 53–94 h at 5k, 231 h at 10k, 934–1,372 h at 20k (the charge is proportional to a timed score, which varied 134–237 µs between runs) | refusal confirmed from 5k; changed in v3.2-dev (admission only) |
| σ̂ = sd(log Ẑ_r): no data | §4.4 | first numbers: small at p ≤ 2k; 0.5–2.5 between diagnostic islands in the one 5k calibration |

**Island cost.** With one set of constants, c_b = 1.0 µs (bridge) and c_1 = 1.8 µs (the 12 terminal rounds at n = 200),

  t_island(N, p, T) = N·(p + 16)·(T + 21.6) µs,

the three measured final islands are reproduced with errors −3.2% (1k), −10.8% (2k) and +6.3% (20k). The formula is a
planning tool with about ±11% error on these three points, not a fitted law. A v3.1 fit is about 4.2 + 0.82·I islands
(4 final, the pilot at H = 0.2048 N, four diagnostic islands per rebuild); measured total / island: 8.2 at I = 5 (1k;
formula 8.3) and 10.7 at I = 8 (2k; formula 10.8).

## 2. The walls, re-ranked

All numbers in this section use the formula above with T = 35 unless marked measured.

1. **Sequential depth under the N_e = max(2500, n, p) rule.** One island: 0.39 h at 5k, 1.57 h at 10k, 6.3 h at 20k.
   A fit with I = 8 … 13 rebuilds (10.8–14.9 islands): 4.2–5.9 h at 5k, 17–23 h at 10k, 68–94 h at 20k, all in
   sequence in v3.1. Measured at 5k: calibration alone took 5.40 h (tier 0 with 11 rebuilds: 3.68 h; the E2 trigger then
   fired and the tier-1 calibration took 1.72 h), and the tier-1 final run (N = 20,000, T = 33) took 6.82 h (one island 1.71 h), so the whole fit took 12.2 h
   (Sapphire Rapids node bb4u17c1; HPM = truth; sd(log Z_r) of the 4 final islands 0.77, R_eff share 0.56).
   The 24 h commons limit is reached near 10k without an escalation, and before it with one. An
   escalation reruns calibration with four times the particles and then runs final islands four times as large.
   Leg A's changes do not touch this.
2. **Calibration rebuild loop.** The cap is ℓ = ⌈log₂(n + p + 1)⌉ = 10, 11, 12, 13 at p = 500, 1k, 2k, 5k; observed
   tier-0 maxima 8, 10, 8 and 11 (one fit each at 2k and 5k). A loop that reaches the cap unconverged fires the
   escalation trigger.
   Whether I keeps growing with p is not established by one profile per p.
3. **Setup memory.** v3.2-dev holds the Gram and the linkage distances: 16 p² bytes = 5.96 GiB at 20k (6.26 GiB
   resident, measured), 37 GiB at 50k, 149 GiB at 100k; commons nodes have about 251 GiB.
4. **LS0 preflight.** With the v3.2-dev charge a 24 h allocation admits 5k (5.8–7.0 h charged), 10k (9.2–13.7 h) and
   20k (18.8 h). Extrapolating the charge, refusal returns between 20k and 30k, depending on the timed score. The LS0
   that actually ran took 0.1–2.1 s. Admission only.
5. **Per-step O(p) terms** (particle bitset copies, `v3_engine.h:120,152,172`): the aggregate cost per step did not grow up to 20k, but
   no separate measurement of the copy cost was made. UNVERIFIED beyond.

## 3. v3.2-dev after leg A (on the branch; all [OP-bit]; verification in CHECKPOINT_1 §3)

Setup at 20k: 85.6 → 23.1 s, peak resident 9.24 → 6.26 GiB; neighbour graph 59.1 → 3.6 s; tables 0.50 → 0.12 s
(round A, one run per core). Gram, final kernel: 39.4 → 6.6 s at 20k, 4.2 → 2.6 s at 10k (round C; both times include
copying the Gram to R and ran on shared nodes). Islands unchanged; memory still O(p²).

## 4. The parallel unit: fixed-size islands, evidence-weighted merge

### 4.1 Pipeline, and the worker-equivalence contract to be built first
J0 build → J1 setup (once) → J2 calibration with census (once) → J3 final islands as a job array → J4 merge and tail.
None of J3/J4 exists in the code. First build, per R04: **R′ = 4, unchanged N, unchanged primary PIP, no census**,
shown equivalent to the serial `v3_fit`; only then more islands. Ruling O17 (HQ, 2026-11-12): "identical" covers
every statistical output and every quantity that enters a published table or theorem check.

**Field by field** (R04's table, checked here against `v3_run.R`, `v3_core.cpp` and the study scripts):

| output | feeds a published table or check | independent workers + merge reproduce it | needed |
|---|---|---|---|
| log Ẑ, log Ẑ_r, lower bound, PIPs, RB arrays, MPM, stage and terminal tables | yes | yes | full island records in island order; unchanged R arithmetic |
| HPM (model, F, provenance), `hpm_before_local`, `hpm_before_ls0` | yes | yes, with the tail below | worker HPM with its event and mechanism; snapshots in the tail |
| top store, near ties | yes | yes | sorted worker top-c; tail; near ties recomputed after LS0 |
| leader stores γ₀, γ₁ (`v3_run.R:210`) | no consumer found, but returned outputs | yes if merged | each merged under its own order (they are **not** calibration-only) |
| `island_best`, flags E1–E3, low ESS, local limits and certificates | yes | yes | global island id mapped to a ledger slot; E1 against the post-LS0 HPM, E3 before LS0 |
| `score_counts$logical` | yes | yes | island matrices summed, tables once, tail events from the tail |
| **`score_counts$fresh`** | **yes: `ev_cost.csv`, the cost exponent, the phase and mechanism shares (`evidence_h2.py:98-105,139-141`)** | **no** | see "Counters" |
| cache statistics, numerical-route counters | no consumer found | no | follow from the same replay |
| timings, status | runtime column; output event | no (physical times differ by nature) | parallel budgets and statuses defined separately |

**Worker.** Inputs: an immutable manifest (hashes of the data and index map, setup and tables, binary and flags,
frozen calibration and inherited state); the global island id r (stream 9 + r) and its ledger slot (`Ledger::event`
updates `island_best` only for ids ≤ `islands`, `v3_ledger.h:108-111`); N, L, measured rounds and tier taken from
the frozen object (`v3_run_settings` takes N from the budgets today and fixes 4 islands, `v3_run.R:89-93`;
`cpp_final_run` starts every call at stream 10 and runs both searches itself, `v3_core.cpp:443-481`). Execution: the
island only. Output: the full `IslandResult` (every stage and terminal record, RB arrays, stream positions, initial
hash), the worker ledger (top store, both leader stores, HPM with event and mechanism, `island_best`, `logical` and
`fresh` matrices of its own events) and a status.

**Streams.** Seeding is x = seed·2³² + stream, stream < 2³² (`v3_util.h:47`). Calibration 0–9; final islands
10 … 9 + R′; census islands 2³¹ + c with 0 ≤ c < 2³¹, c unique across census sizes and batches, no reseeding on a
retry, the uint64 construction checked, and stream ids kept as doubles in R (they exceed the integer range). The
reported stream map is generated from the manifest (`v3_randomness` hardcodes 0:13 today). Disjoint labels do not
prove independence (O18).

**Merge, then the tail, once, after every manifest island is present and validated.**
- Top store: top_c of the union of the worker top-c stores under the store's comparator. Truncating each worker at c
  is safe, ties across the cut included: a dropped model has c distinct better models in that worker. Deduplicate by
  model identity, not by hash. Memory: O(c + R′) entries for an R′-way merge, or O(c) for a running pairwise union.
- Leader stores: the same, each under its own comparator (γ₁ orders by F then lexicographically, unlike the top store).
- HPM: maximum under `hpm_better` over the table models, the inherited HPM (calibration provenance restored as in
  `v3_core.cpp:428-440`) and the worker HPMs; provenance = the earliest actual source in the order tables, inherited,
  islands by id.
- Tail, exactly `v3_core.cpp:453-481` on the merged ledger: snapshot `hpm_before_local`; final local search (cap ℓ)
  from the merged HPM; snapshot `hpm_before_ls0`; start mode; LS0 (cap ℓ + |S̃₀|). A new best found in the tail takes
  the tail event as provenance. Then near ties, certificates and flags as `v3_run.R:173-212`.

**Counters: what O17 implies.** The serial run shares one score cache across the four islands and both searches,
and clears it completely when it is full (479, 565 and 127 clears in the final runs of the 1k, 2k and 20k profiles).
Whether a lookup is fresh therefore depends on the whole ordered history; the sets or counts of distinct models per
island do not determine it (R04 finding 1). Since `fresh` feeds published tables, case (a) of the ruling fails. Case
(b) — serial-equivalent totals that match exactly — needs an ordered trace of every cache lookup (model identity
or a wide key, phase, mechanism; the non-emitting lookups such as the search centres included) replayed in island
order through the serial cache rule and continued through the tail, with the route counters attached to the replayed
misses. Size: 3.9·10⁸ lookups in the final run of the 1k profile and 9.1·10⁸ at 2k, i.e. about 6 and 15 GB at 16 bytes
per lookup, written by the workers and read once. **Not built; the options are put to HQ in CHECKPOINT_2.**

**Statuses.** To be declared before the build: task and whole-fit budgets (one runtime guard cannot span
processes), retry policy, precedence of terminal statuses, missing or killed tasks, merge or tail failure, atomic
publication. Never aggregate only the islands that succeeded. Every estimate field is NA on non-delivery, as
`v3_run.R:106-116`. Equivalence is claimed for runs completed under both executions; wall-clock guard decisions need
not coincide, and timings are physical.

**Serial tail of the merge, and I/O.** One scan evaluates at most p + k(p − k) models (k + k(p − k) at k = K, where
additions are skipped; `v3_engine.h:394-405`). Measured in the profiles' LS0: 108,999 models in 0.11 s at 1k and
2,198,999 in 2.06 s at 20k (0.94–1.0 µs per model; `LOG.md`, profile records). At p = 1M and k = 100 one scan is
1.0·10⁸ models. Not measured beyond 20k, nor without the Gram, nor on tie-DP cases. Record I/O at large p must be
budgeted too: R′ worker stores of 40p + 1 models (1.0·10¹⁰ entries at p = 1M, R′ = 256, before deduplication), a
p × R′ PIP matrix (1.9 GiB of doubles there) and five RB arrays (9.5 GiB).

### 4.2 Costs with N_isl = 2,500 (the law-changing choice of §7(i); numbers only; formula at T = 30)

| p | t_island | calibration at H = 512, serial, I = 5 … 13 | 64 islands | 256 islands | status |
|---|---|---|---|---|---|
| 5k | 0.18 h | 0.8–2.0 h | 11.5 core-h | 46 core-h | formula |
| 10k | 0.36 h | 1.5–3.9 h | 23 core-h | 92 core-h | formula |
| 20k | 0.72 h (measured: 0.66 h at T = 29) | 3.1–7.8 h (measured pilot at H = 2,500: 0.61 h) | 46 core-h | 184 core-h | one measured island |
| 100k | 3.6 h | — | 229 core-h | 917 core-h | UNVERIFIED extrapolation; the Gram alone is 74.5 GiB |
| 1M | 35.8 h | — | — | 9,173 core-h | UNVERIFIED extrapolation; exceeds the 24 h commons limit per island, so it needs checkpoint/restart or threads; needs the Gram-free core |

Not in the table: setup, census, merge, the serial tail of §4.1, failures. Running the four diagnostic islands of a
rebuild concurrently shortens only their part: calibration depth becomes pilot + I·(one diagnostic island + grid
construction + local search) instead of pilot + I·(four + …).

### 4.3 Merge estimators
Write ω_r = Ẑ_r / Z (unnormalised; E[ω_r | V] = 1) and W_r = Ẑ_r / Σ_s Ẑ_s (normalised merge weights).
- log Ẑ = LSE_r(log Ẑ_r) − log R′.
- PIP_Z,j = Σ_r W_r ĥ_rj (the v3.1 *specified* primary) and PIP_eq,j = mean_r ĥ_rj (the *shipped* primary,
  `v3_run.R:162`); both always reported. Which is primary is §7(ii).
- General declared h: μ̂(h) = Σ_r W_r H_r(h) = [R′⁻¹ Σ ω_r H_r] / [R′⁻¹ Σ ω_r], a ratio of two means.
- Given the data and V, with conditionally iid islands: μ̂ → π(h) as R′ → ∞; √R′ (μ̂ − μ) → N(0, Var(ω(H − μ) | V));
  the bias at finite R′ is −Cov(ω(H − μ), ω | V) / R′ plus higher-order terms, in general not zero. The reported
  SE² = (R′/(R′ − 1)) Σ_r W_r² (ĥ_rj − PIP_Z,j)² estimates Var(μ̂) ≈ E[ω²(H − μ)²]/R′ to first order; a minimum R′ for
  reporting it has to be declared. These are asymptotic statements for conditionally iid islands; neither N1 nor f01
  gives finite-R′ precision.
- PIP_eq is consistent in R′ only if each island is itself unbiased for the PIP, which finite-N SMC does not give in
  general.

### 4.4 Dispersion of the island evidences: what was measured
`results/sd_logZ_by_p.tsv`, `sd_logZ_long.tsv`, `pip_weighting.tsv`.
- Final islands, N = 2,500: σ̂ median 0.065 at p = 500 (12 fits, max 0.17), 0.088 at p = 1000 (11 tier-0 fits, max
  0.70), 0.042 at 2k (one fit). Escalated fits (N = 10,000): 1.00 (`p1000_S5_r001_c100`) and 0.82 (tie design).
- Diagnostic islands, H = 512: median 0.15 (p = 500), 0.18 (p = 1000), 0.22 (2k); the tie design gave 5.7–6.1 at
  H = 512 and 4.2 at H = 2,048.
- p = 5k (one S3-type dataset, calibration only): the four diagnostic islands at H = 1,024 gave σ̂ between 0.49 and
  2.52 over the 11 rebuilds (median 1.39; E2 fired), and 1.56 at H = 4,096 after the escalation. This is the only
  measurement above 2k, it is several times the p ≤ 2k values, and at σ = 1.4 the large-R′ approximation below gives
  R_eff / R′ ≈ 0.14.
- R = 4 weights on the 25 fits: R_eff / R between 0.597 and 1.00, at least 0.97 in 20; the largest weight 0.58.
- The ratio of the diagnostic to the final medians (2.4 at p = 500, 2.1 at p = 1000) is compatible with 1/√N
  (√(2500/512) = 2.2) but does not establish it: the two sets use different grids and streams, fits with more rebuilds
  weigh more, the ratio of the last same-tier diagnostic set to the final set ranges from 0.31 to 13.4 over the fits
  (recomputed by the reviewer, R03 and R04), the 2k ratio is 5.2, and in the escalated S5 fit the tier-1
  diagnostic islands (H = 2,048) gave 0.31 while the final islands (N = 10,000) gave 1.00. A frozen-grid sweep over N
  with replicated islands is needed (leg B).
- For log-normal Ẑ_r and many islands, R_eff / R′ ≈ exp(−σ²): 0.99 at σ = 0.09, 0.94 at 0.25, 0.61 at 0.70, 0.37 at
  1.0, 0.018 at 2.0. This is a large-R′ approximation, not a statement about four islands.
- W3-P6 (n ≤ 100, small-n study; `results/p6_E2_by_np.tsv`, script `analysis/p6_e2_table.py`): share of completed fits
  with the E2 flag (σ̂ > 1 over the four final islands) at n = 50: 0/137, 2/40, 13/105, 6/16 at p = 50, 125, 250, 500.
  Designs, arms and tiers are pooled, and every flagged fit at p ≥ 250 was escalated; these counts show that large
  σ̂ occurs, not how it scales at fixed N.
- **Not known:** σ̂ of final islands beyond p = 2k, and at fixed N (the 5k values are diagnostic islands of one
  dataset); its dependence on the design beyond one replicate per cell; why the
  large values occur (no mode-occupancy record exists).

### 4.5 Diagnostics and census (to be specified; nothing is fixed here)
Reported, never used to switch estimators or to rerun: R_eff = 1/Σ W_r², R_eff / R′, max W_r, σ̂. A degeneracy flag
needs a declared threshold (v0's R_min = 30 was an example) and, if the Pareto shape k̂ of the weights is used, a
declared fitting algorithm and a minimum tail size; neither is validated for evidence weights.
A census (R_c islands of candidate sizes on census streams, after the grid is frozen and before any final stream is
read) can feed a rule for (N_isl, R′) that is V-measurable. The rule itself is not designed: it needs a declared map
from census statistics to (N_isl, R′), a budget ceiling, a rule for failure, and it must be written before the runs.
A census that looks benign can miss rare high-evidence modes, and one poor shared grid impairs every final island
(conditional validity given V is unaffected; the alternative of several independent calibration groups at the same
total work has not been compared). Also undefined: whether census models are inherited into the stores (v0 O3 assumed so, for the card items), with
which provenance and counters. Cost of a measurement census at 20k: 32 islands of N = 2,500 ≈ 21 core-h (measured
island time).

## 5. Memory: path to O(np)

| step | tag | dense arrays at 20k | at 100k | note |
|---|---|---|---|---|
| v3.1 | — | 24 p² = 8.94 GiB (9.24 GiB resident, measured) | 223.5 GiB | Gram + correlation + distance |
| v3.2-dev (leg A) | [OP-bit] | 16 p² = 5.96 GiB (6.26 GiB resident, measured) | 149 GiB | Gram + distance |
| Gram-free scorer + streamed correlation tiles (v0 S2/S3, G1–G5) | [OP-bit] by v0's local check; speed depends on the per-particle factor cache | 8 p² = 2.98 GiB (distance only) | 74.5 GiB; 37 GiB with a condensed distance | Phase 2; excluded from leg A by HQ |
| sparse exact-below-threshold partition (v0 B4) | [Δlaw]; obligation O8 | O(pB + edges) | same | needed where the exact linkage does not fit the node: on 251 GiB the full distance fits to p ≈ 180k, the condensed one to ≈ 260k, before other allocations |

Island phase at 20k with N = 2,500: 5.40 GiB (pilot) and 6.30 GiB (final island) resident, of which the Gram is
2.98 GiB; the rest is the score cache (500p entries), tables, stores and their R copies. What an island needs once the
Gram is gone has not been measured.

## 6. Theory obligations of the parallel method

IDs as in v0 §4. "f01" = `Wave3/API_AUDIT/sharp1/results/f01.md` (handed to this track by HQ; TRIAGE row 1). N1 =
`Wave1/W1-N1/STATEMENT.md`, whose weight is the unnormalised ω_r = Ẑ_r / Z.

| ID | obligation | route and qualifications |
|---|---|---|
| O1 | merge consistency and CLT of §4.3 at fixed N as R′ → ∞ | (a) Island identity E[ω_r H_r(h) \| V] = π(h), V = all calibration-side streams: f01 (b)(ii) gets it from the freezing lemma under SI by the independence argument (the 𝒞-conditional N1 then follows from it by the tower property, not the reverse). (b) Dropping the uniform bound B_h needs f01 (a)(1): integrability of max_S \|h(S; V)\| on E₀ = {calibration succeeded} ∩ {r ≤ R′} (the potential-run event of the freezing lemma, not the delivered-output event), or the regular-conditional-law reading. (c) The extension to all L + 5 post-terminal populations (f01 (b)(i)) is for population averages; the stage-t identities are about Z_t and q_φt; **N1 does not cover the shipped Rao–Blackwellised PIP at all** (its H is the plain four-round average and its §5 excludes Rao–Blackwellised records; R04 finding 2): the merge theory needs the separate RB identity (each recorded Gibbs conditional integrates to the marginal under a kernel that preserves the target), to be located in the v3.1 theory or proved, with the exact-arithmetic and ideal-stream premises carried into §4.3. (d) The ratio limit needs: fixed data and V, a V-measurable sequence of budgets R′, final islands conditionally iid given V (IND-T on the enlarged stream map, O18), bounded Ẑ_r (true on a finite space). If N or p change with the budget it is a triangular-array statement, not covered. (e) Under IND-T, f01 (b)(iii) gives E[ω_r H_r(h) \| V, U_−r] = π(h) for h measurable in (V, U_−r), with the **unnormalised** ω_r. It does not make the normalised contributions W_r H_r orthogonal, nor leave-one-out errors that depend on each other's streams. |
| O3 | census inside calibration | (N_isl, R′) from census islands is V-measurable if the census streams are calibration-side and disjoint from the final range (§4.1), so (a) applies with a V-measurable R′ (f01 (a)4). This protects first moments; it is not by itself an R′ → ∞ theorem (see (d)). The TH01(c) counterexample (R′ adapted to final outputs) does not apply. |
| O2 | degeneracy at high p: bound E[ω_r² \| V], or a lower bound showing growth | open research; §4.4 is the only evidence |
| O4 | N decoupled from p (reversal of "N_e is never split") | owner decision first (§7(i)); then restate TH01 (e)(f)(i), TH06, TH08 with general (N, R′) |
| O5 | counter-based streams | not needed for island-level parallelism (each island keeps its serial stream); needed only for threads inside an island |
| O6 | replay; output event | replayed tasks must validate their inputs (hashes) and be deduplicated atomically by island id; a deterministic numerical failure is not repaired by replay; "all R′ islands completed" is not enough if the merge, its local search or LS0 stop: then there is no output (GUARD-W) |
| O10 | union stores and HPM over R′ islands | Lemma S for the top store and, with their own comparators, the leader stores; the rest of the merge is the specification of §4.1 |
| O14 | preflight change is admission only | implemented and reviewed; it acts at the initial preflight and before an escalation; outputs are identical on equal admission decisions |
| O17 (new) | output equivalence of process-parallel islands with the serial run | ruled by HQ (2026-11-12): every statistical output and every quantity in a published table or theorem check. Met by the contract of §4.1 for everything except `fresh` counts, cache statistics and route counters, which need the lookup-trace replay or a decision on the cost column |
| O18 (new) | independence of the final and census streams on the enlarged stream map | today an assumption about SplitMix64-seeded xoshiro256** streams (EX-S / IND-T); not discharged by relabelling |
| O19 (new) | `log_Z_lower95` = log 0.05 + log Ẑ with R′ islands | Markov's inequality needs only E[Ẑ \| V] = Z and a V-measurable R′: no independence and no R′-dependent factor; it is a statement about the potential run, not conditional on delivery |
| O20 (new) | flags E1, E2, E3 and the escalation rule when R′ ≠ 4 | E1 (any island) and E2 (σ̂ > 1) change their frequency with R′; E3 is the final search before LS0; final flags must not trigger reruns or change the frozen R′ |
| O21 (new) | card items G1, G2, L3 and local certification on the merged HPM | re-audit with the union store; not implied by the pipeline |
| inactive | v0 O7, O9, O12 | not triggered: scorer and kernel are unchanged and no screening is proposed |
| deferred | v0 O8 (sparse partition), O11 (island-level resampling), O13 (smaller store capacity), O15 (calibration numerics), O16 (linkage algorithm) | unchanged from v0; O8 is triggered by §5's last row, O11 by the fallback of §8 |

## 7. Reserved for the owner — framing only; neither question is decided here, and leg A's measurements do not settle either

**(i) Particle count per island at very large p.** The v3.1 ruling is N_e = max(2500, n, p), never split.

| | keep N_e = p | fix N_isl = 2,500 |
|---|---|---|
| one island (formula; T = 30) | 1.4 h at 10k, 5.7 h at 20k, 6.0 days at 100k, 1.6 years at 1M | 0.36 h at 10k, 0.72 h at 20k (0.66 h measured), 3.6 h at 100k, 35.8 h at 1M |
| fits a 24 h task (formula) | one island to p ≈ 40k; a whole serial fit to about 10k (§2) | one island to p ≈ 670k; not at 1M without checkpoint/restart or threads |
| particle memory at 1M | two N × p bit arrays: 233 GiB per island | 0.6 GiB per island |
| what the theory has | TH01 and the delivered v3.1 theorems as they stand | needs O1, O3, O4, O18; PIP_eq keeps the island bias, PIP_Z has the ratio bias of §4.3 |
| what is not known | σ̂ and bias at p ≥ 5k under either rule; whether I and T keep their size | σ̂ at fixed N beyond p = 2k (O2); the census rule; total cost with calibration, census, merge and failures |

Everything at 100k and 1M is an extrapolation of a formula checked at three points up to 20k. A mixed rule (N = p up to
some p, fixed above) is a third option.

**(ii) Primary PIP: equal-weight (shipped, `v3_run.R:162`) or evidence-weighted (the v3.1 specification).**

| | equal-weight | evidence-weighted |
|---|---|---|
| on the 25 saved fits (R = 4, N ≥ 2,500) | — | max_j \|PIP_Z,j − PIP_eq,j\| at most 0.0023 (median over fits 0.00009), which is up to 1.3 equal-weight standard errors; same median-probability model in 25 of 25 |
| bias | the per-island bias, for every R′ | −Cov(ω(H − μ), ω)/R′, vanishing as R′ grows |
| variance (leading term) | Var(ĥ_r)/R′ | E[ω²(H − μ)²]/R′: depends on the joint law of the evidence and the island summary, not on the dispersion of ω alone |
| failure mode | bias that more islands do not remove | few effective islands when σ̂ is large (R_eff / R = 0.60 in the worst of the 25 fits) |
| consequence of switching | — | a reported estimate changes definition: registry and lifecycle; the published PROD-H study used equal-weight PIPs |

No 2k or larger fit is in this table, and four islands cannot show the many-island behaviour of either estimator.
Both columns stay in the output whichever is primary.

## 8. After leg A

Leg B proposal with costs: CHECKPOINT_1 §7. In short: bit-identical engine work and process-parallel islands (the
route to delivering 10k–20k fits under the present law: a validation target, not a measured result), a measurement of σ̂ against p and N on frozen grids, then the
O(np)-memory core. Alternatives kept on the list, none adopted: several independent calibration groups instead of
one shared calibration; island-level resampling (v0 O11, [Δlaw]) as the fallback if the weights degenerate — it
keeps an unbiased evidence estimate at the price of communication and of genealogy-aware variance theory, and it is
not a free cure.

## Appendix: UNVERIFIED items carried forward
Per-step cost beyond p = 20k; every row marked UNVERIFIED or "formula" in §2, §4.2, §5 and §7; σ̂ at fixed N beyond
p = 2k; growth of I and T with p; the Pareto-k̂ diagnostic for evidence weights; glibc `exp`/`log` variant selection
across node types (all leg A runs were pinned to sapphirerapids); the literature named in f01.
