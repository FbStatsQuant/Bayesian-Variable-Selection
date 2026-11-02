# Patch list for v2.2 (CONF, 2026-10-28)

Two markings are used:
- **NON-BEHAVIOURAL**: an extra output only, a statistical observer, implemented in `code/core/v2_2/`. The conditional guarantee tested here (any acceptance of it in place of the brief's literal wording is HQ's decision):
  - it draws no random numbers;
  - no new value is an input to any move, weight, schedule, grid, escalation, guard, status, HPM, store, cache or flag;
  - so in the same numerical environment, whenever execution reaches the same operations, the statistical trajectory and every pre-existing output are bit-identical.

  **Disclosed exception.** The observer adds a little wall-clock time, and the runtime guard reads wall-clock time. A fit that is *near* its allocation can therefore stop at a different checkpoint, as any rerun of v2.1 itself can (same-version reruns differ in stop point; REGRESSION). Time, memory and provenance fields are not deterministic.
- **BEHAVIOURAL**: a proposal. HQ decides.

Regression evidence for the implemented patches is in `REGRESSION.md`.

| Patch | Marking | Status | Changes existing outputs? | Cost |
|---|---|---|---|---|
| P1 Plain PIPs | NON-BEHAVIOURAL | implemented | No (bit-identical, REGRESSION) | O(N·\|S\|) counting per measured round. The one end-to-end p = 500 timing pair (3,172 s v2.2, 3,216 s v2.1, run concurrently) shows no visible overhead but does not isolate it |
| P2 Instrumentation | NON-BEHAVIOURAL | implemented | No | Per fresh score event: one hash over S and an HLL register update. At p ≤ 64, a hash-map probe as well; at a model's first insertion, a node allocation and an LSE update. Registry memory is **O(distinct models)** at p ≤ 64, with no bound. *Observed:* 0.27–4.8 MB in the smoke fits (p ≤ 30); 21 kB (HLL only) at p = 500 |
| P3 "Truth scored, when, by which route" | NON-BEHAVIOURAL | p ≤ 32 implemented (scored set in the fit output); p ≫ n replay proposed, not built | No | Export: O(M log M) sort plus R columns. *Observed:* 0.07 MB (p20) and 0.27 MB (p30) per fit, xz-compressed, so ≈ 0.4 GB of scored-set storage for 2,400 low-p fits (total RDS storage not included). Replay: one extra fit per replayed unit |
| P4 cut_group | NON-BEHAVIOURAL (reporting) | recommendation; one extra field implemented | No | none |
| P5 Stop policy | **BEHAVIOURAL** (study policy) | proposal | Yes: which fits are available | ≈ 70 core-h and ≈ 13.5 h wall at p ≫ n if the same 6 stop again |
| P6 Low-p readiness | (check) | the core is ready; the study adapter is not | — | Adapter generalisation ≈ ½ day of code + regression |

---

## P1. Plain PIPs (NON-BEHAVIOURAL, implemented)

**What.** Per island, after each of the 4 measured rounds, every particle's current model is counted. That gives
plain PIP_rj = (number of particle-rounds that include j) / (N · 4).
Pooling is the same as for RB: the equal-weight mean over the 4 islands. Islandwise values are kept. MPM_plain = {plain PIP > ½}.

**Where.** `cpp/v3_engine.h` (measured loop), `v3_core.cpp` (`island_to_list`, appended), `v3_run.R` (`pip_plain_r`, `pip_plain`, `mpm_plain`), `study/adapter.R` (record `pip_plain`, `mpm_plain`). The exact branch has none (undefined there).

**Reason.** D4 (Felipe): track both RB and plain PIPs. Headline question 3.

**Changes outputs?** No. It reads particle states after the round; it draws nothing.
- Every islands list, including the calibration islands, gains `pip_plain`, `plain_acc` and `plain_round` at the end.
- At the top level, `pip_plain_r`, `pip_plain` and `mpm_plain` are re-appended in `finish()`, after every v2.1 field and before `instrumentation`. This was fixed after review (Sol finding 4): the v2.1 name vector is a prefix of the v2.2 one.

**Accuracy (smoke, n = 200).**
- Against the full p20 enumeration: maximum error RB 0.0009–0.0018, plain 0.0023–0.0041.
- Against the p30 size ≤ 12 reference: RB 0.0012–0.0017, plain 0.0018–0.0034.
- MPM_plain = reference MPM in all six fits.

## P2. Instrumentation (NON-BEHAVIOURAL, implemented)

All of these are extra outputs under `fit$instrumentation` (and `record$instrumentation`); none consumes random numbers.

| Item | Field | Notes |
|---|---|---|
| Log-sum-exp of F over the distinct models scored | `scored$log_sum_exp_F` (+ `after_calibration$…`) | Exact at p ≤ 64. Coverage = exp(lse − exact log Z). NA at p > 64 |
| Number of distinct models scored | `scored$n_distinct` (exact, p ≤ 64); `scored$n_distinct_hll` (HyperLogLog, every p; nominal relative s.e. 1.04/√16384 ≈ 0.8%, observed within 0.7%) | At p > 64 an exact set is infeasible: p = 500 scored ≈ 1.26 × 10⁸ distinct models. At p = 33–64 the registry is exact, but no scored set is exported |
| Distinct models by first-score phase × mechanism | `scored$first_scored` | p ≤ 64 |
| Stage count used | `stages$final`, `stages$pilot` (per tier), `stages$diag_grid_intervals`, `stages$tier_final` | |
| Per-island log Ẑ_r and islandwise PIPs | already present: `log_Z_r`, `log_Z_r_rel_m0`, `pip_r`; new `pip_plain_r` | Not duplicated |
| Best scored model before and after the final local search | `best_before_local`, `best_after_local` (`changed` flag) | Completed SMC fits |
| Stop phase of a `resource_limit` | `stop` (`where` = preflight / escalation_preflight / runtime_guard; checkpoint, phase, tier, iter, island, stage, elapsed, projected, allocation) | The first exceeded guard checkpoint |
| Escalation reasons | `escalation$reasons` (tier-0 triggers fired), `escalated`, `blocked` | |
| Version | `version = "v2.2"` | |

**Reason.** The theory instrumentation requested by HQ, the LOWP metrics pipeline, and audit gaps U3/U4 (escalation reasons and stop points were only recoverable by hand).

**Note (D41).** The relative-scale 95% lower bound is still not its own field. It is exactly `log_Z_rel_m0 + log(0.05)`, so the analysis derives it. Adding it costs one line in `v3_assemble_final` plus a regression; it is deferred to avoid churn after the regression.

## P3. "Was the truth scored, when, and by which route" (truth-free)

The fit never receives the truth. Two designs were considered.

**(a) Scored set in the fit output, p ≤ 32: recommended for regime L. NON-BEHAVIOURAL, implemented.**
- What the fit returns: `instrumentation$scored_set` is the sorted list of every distinct model scored in the whole fit (tables, calibration, final run, local searches). Each model is stored as a bitmask key, with its first score's phase, mechanism ("route"), tier, iteration, island and stage.
- How the truth is checked: the scoring job, which alone holds the truth, looks up the truth key afterwards and reports scored or not, when and by which route.
- What else it gives:
  - the same lookup for the exact HPM;
  - coverage, via `scored$log_sum_exp_F`.
- Size (measured, n = 200): about 25k distinct models at p20 and 110k at p30. That is 1.0–1.2 MB and 4.5–4.8 MB in memory, and **0.07 MB and 0.27 MB xz** in the RDS, so ≈ 0.4 GB for all 2,400 low-p fits.
- Cost: the registry work per fresh score (above) plus an O(M log M) export at the end of the fit. In the R3 smoke the whole fit took 3–11 s. The overhead was not isolated.
- `v3_fit(..., keep_scored_set = NULL)` defaults to TRUE exactly when p ≤ 32.

**(b) Deterministic replay with a watch list, p ≫ n: proposed, not built.**
- The trajectory is a deterministic function of (X, y, seed), given the same code, preprocessing and numerical environment. Only *termination* depends on the allocation and wall-clock time. The guard does not touch the random stream, as the matched forced-stop pairs in the regression show.
- A separate scoring job can therefore rerun `v3_fit` with an instrumentation-only hook that reports the first score event of each watched model (truth, exact or reference HPM).
- Cost: one extra fit per replayed unit, ≈ 0.5 h (p500) and ≈ 1.5 h (p1000) per non-escalated fit. Replaying only the units whose HPM ≠ truth would cost a fraction of that.
- Build cost: ≈ ½ day plus a regression.
- An exact scored set is infeasible here (≈ 10⁸ models).
- **Recommendation:** build it only if HQ wants "why the truth was missed" at p ≫ n.

## P4. cut_group (recommendation: demote to informational, keep the field)

**Facts** (historical counts from the 2,400-fit run and HQ's brief; supplied background, partly re-checked in CONFORMANCE).
- It fired in 2,398 of 2,400 fits.
- The threshold √(2 log p / n) is ≈ 3.5–3.7 null standard deviations. Across 1.2 × 10⁵ to 5 × 10⁵ pairs, that gives ≈ 52 (p500) and ≈ 100 (p1000) chance edges per dataset.
- 37 sampled components covered the whole retained set.
- It never affected the fit, and R-1 already lists it as informational: it does not set `diag_flag`.

**Recommendation: keep it computed and stored, demote it in every report, and never present its rate as a quality signal.**
- The proposed variant "component larger than B" is not a cure. Sampled flagged components larger than B = 14 are common (sizes 15–1000), so it would also fire almost always. v2.2 records it anyway, as `instrumentation$cut_group_large`, for T26-oriented analysis.
- P4 stays reporting-only only as long as cut_group feeds no `diag_flag`, selection, retry or guard (true today).
- If HQ wants a discriminating flag, the principled redefinition ties the threshold to n and p (a normal-approximation design heuristic, not an exact finite-n calibration). Choose z so that the expected number of chance edges is about 1: p(p−1)·(1 − Φ(z)) = 1, threshold z/√n (≈ 0.33 at p500). This is a new output field, so it is non-behavioural for the fit; cost ≈ 1 h plus a regression.
- Caveat: S5's designed between-block correlation would still fire it legitimately.

## P5. Stop policy (BEHAVIOURAL: study policy; HQ decides)

**Facts** (historical counts from the 2,400-fit run and HQ's brief; supplied background, partly re-checked in CONFORMANCE).
- Benchmarks got one doubled-time retry on timeout; SMC-BVS got none.
- 6 of 2,400 fits stopped with `resource_limit`. All six are escalated S5 fits; 5 are at p1000. 4 stopped in the final bridge, 2 in tier-1 calibration.
- HQ's brief says 3 of the 4 c = 1 stops had already scored the truth. That is supplied background, not verified here.

**Proposed committed rule.** A fit that ends `resource_limit` at the runtime guard gets exactly one rerun:
- same seed;
- the in-run allocation doubled (2L);
- the Slurm wall sized for 2L.

The rerun's result replaces the stop. A second stop stays `resource_limit`, its own category.

**Why this rule.**
1. It is symmetric with the benchmarks.
2. Determinism makes it clean. With the same code, preprocessing and numerical environment, the statistical trajectory depends only on (X, y, seed), and the allocation enters only the guard. The rerun therefore repeats the stopped run's statistical prefix. If it completes, its statistical outputs are those of the uninterrupted run that the theory describes (THEORY_INVENTORY B.2.1). Timing, memory, allocation and checkpoint fields and provenance naturally differ; whole-record identity is not claimed.

**Cost at p ≫ n.** The v2.2 trajectories are identical to v2.1's, so the same 6 units will very likely stop again. That is not certain: stop points depend on wall-clock time and node speed.
- Reruns: 1 × 12,600 s + 5 × 48,000 s ≈ 252,600 s ≈ **70 core-h**, plus the 6 × L already spent.
- Wall per rerun ≤ 48,000 s + margin ≈ 13.5 h, under the 1-day limit.
- Whether 2L suffices is not known. p1000_S5_r064_c100 stopped in the last tier-1 diagnostic iteration, before its final run.

**Alternative (cheaper by ≈ 35 core-h).** Set L1000 = 48,000 s for all p1000 units from the start; this avoids repeating the prefix. The cost is longer wall requests for all 1,200 p1000 tasks, which slows queueing.

**At low p.** Fits take 2–11 s locally (R3), so the guard is irrelevant if L is sized from the pilot. Apply the same rule for symmetry.

**Also note (D12).** Burn-in and measured rounds are unguarded, so a fit can pass L by up to one terminal block. That happened once. Size the Slurm kill margin for it (the current L + 300 s covered it).

## P6. Low-p readiness (p = 20, 30; n = 200)

**Confirmed by a smoke test, not campaign-wide.** Two smoke datasets, three seeds each, no escalation; the p30 reference is truncated at size ≤ 12. Still pending: the low-p adapter and runner, a full p30 reference (LOWP), and validation on the production platform (job `conformance/jobs/CONF_NOTS_IDENTITY`). The six R3 fits show:
- `branch_run = "smc"`: Σ_{k≤K} C(p,k) = 2^p (1,048,576 and 1.07 × 10⁹) exceeds 12,560·p (251,200 and 376,800).
- The budgets follow the committed rules:

| p | K | B | ℓ | L | N0 | H0 | T0 | Cache 500p | Top store 40p+1 | Leaders 20p |
|---|---|---|---|---|---|---|---|---|---|---|
| 20 | 20 | 4 | 8 | 8 | 2,500 | 512 | 1,000 | 10,000 | 801 | 400 |
| 30 | 30 | 5 | 8 | 8 | 2,500 | 512 | 1,000 | 15,000 | 1,201 | 600 |

- Accuracy against the references (p20 full enumeration; p30 size ≤ 12):
  - |Δ log Ẑ_rel| ≤ 0.013;
  - maximum PIP error ≤ 0.0018 (RB) and ≤ 0.0041 (plain);
  - HPM and MPM agree with the reference in 6 of 6;
  - the scored set covers 99.995% of the posterior mass at p20 (full), and 99.89% of the size ≤ 12 reference mass at p30.
- Runtime 2–11 s, no escalation, memory trivial.

**What breaks or needs a decision:**
1. **The study adapter rejects low p** (`study/adapter.R:79,88–95,148–151`):
   - the case-ID regex and the seed bases cover only p ∈ {500, 1000};
   - `smcbvs_load_input` requires the n200 benchmark record with `foldid`, `kind`, `scales` and c100/c050 columns;
   - the design row hard-codes `study = "bench20261019"` and `regime = "H"`.

   A low-p adapter path is needed, with LOWP's seed scheme and input format. This is study-layer code (non-behavioural for the method). It needs LOWP's generator spec before it can be written. HQ to route to CONF (v2.2.1) or LOWP.
2. **The runner** (`runner/task.sh`, `submit.sh`, `make_tables.py`) hard-codes L500/L1000, p ∈ {500, 1000} and c100/c050. It needs L20/L30 from the pilot.
3. **Not a break, but note:** B = ⌊√p⌋ gives blocks of 4 at p20, against the DGP's blocks of 5, and blocks of 5 at p30. The committed rule is followed; no change is proposed.
4. **The exact references are LOWP's job.** The production `cpp_enumerate` took 1.5 s at p20, but a full 2^30 enumeration did not finish in 2 h locally. The smoke used |S| ≤ 12, with a measured size-mass decay of about 10× per size (size 12: 1 × 10⁻⁷). LOWP needs a faster enumerator (Gray-code updates) or NOTS time for p30.
