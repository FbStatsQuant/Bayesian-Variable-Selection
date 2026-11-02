# Conformance of the executed p ≫ n SMC-BVS run with the written method

CONF thread (Opus 5.5), 2026-10-28. Revision 2 adopts every finding of the independent review, `review/CONFORMANCE_REVIEW_sol.md` (ACCEPT WITH FIXES); the dispositions are in `review/CONFORMANCE_REVIEW_disposition.md`.

## Verdict

**PASS, qualified. The historical run has no unauthorized behavioural deviation from master Part I.**

- **Statistical core.** It conforms item by item: preprocessing, budgets, scorer, blocks, start, moves, resampling, pilot, grid, rebuild loop, escalation, final run, local search, HPM, PIPs, evidence, seeds and flags. Evidence: worker code audit, the reviewer's independent inspection of the high-risk paths, and output checks, part sampled and part population-wide (below).
- **One authorized behavioural difference, at the study/resource-policy level (S1).** Part I's settings table makes the guard allocation the job's actual request. Production instead used a per-unit allocation, L500 = 6,300 s and L1000 = 24,000 s, with `mem_gb = 2`. This was adopted explicitly in GO_2400 C1 ("the in-run `--hours` equals the unit limit"). It changes output *availability*: 6 fits ended `resource_limit` without estimates. It is a release policy, not a code defect. Part I needs a wording reconciliation, and the stop policy for the rerun is proposal **P5**.
- **Two conditional behavioural differences, neither of which fired in this run:**
  - D30, the near-constant centring fallback: 0 of 2,400 fits, for X and y alike.
  - D03, the guard's timed "grid construction" includes the V re-scoring: no stop occurred at a grid checkpoint.
- **Everything else is wording or cosmetic.**
- **Redeploy is not needed for conformance.** This verdict stands on its own. The SMC arm is being rerun under D5 for other reasons (one code version, new outputs).

## Evidence base (kept separate)

| Layer | Who | Scope | File |
|---|---|---|---|
| Provenance | manager | `code/core/v2_1_baseline/` = production `SHA256SUMS`, 24 of 24 files (re-hashed) | this file |
| Code against text | Sonnet worker | 31 deviation rows (D01–07, D10–21, D30–32, D40–45, D50–52) and 33 "equal" rows, all with line citations | `work/A_code_vs_text.md` |
| Independent code inspection | Sol reviewer | RB before the draw, increment before resampling, escalation, all-scored HPM including the inherited calibration HPM, final flags never trigger reruns, exact rule, cap handling, seeds and streams | `review/CONFORMANCE_REVIEW_sol.md` |
| Output checks, sample | Terra worker | 86 RDS (6 `resource_limit`, 20 escalated, 60 stratified); all 2,400 CSVs | `work/B_outputs.md`, `work/B_outputs/` |
| Output checks, population | manager | all 2,400 RDS | `work/C_population/{scan.R, population_scan.csv, population_summary.txt}` |

**What the output checks do and do not test.** Most are assembly checks: saved fields are consistent with each other and with the definitions. Three examples:
- HPM is checked against the saved top store, which shares the ledger's update path; this is not a replay of every model scored.
- RB PIPs are checked against their saved accumulators, which tests normalisation, not when recording happens.
- Evidence is checked against its saved increments, which tests assembly, not that the incoming particles were used.

Timing, coverage and RNG use rest on code inspection, by the worker and by Sol independently. The CSV diagnostic check calls the production `smcbvs_diagnostics`, so it tests RDS ↔ CSV consistency, not the policy itself.

## Output checks: all pass

| Check | Basis | n | fail |
|---|---|---|---|
| Reported HPM = max-F model of the saved top store, tie rule (size, then lexicographic) | sample | 80 | 0 |
| hpm_F ≥ best before final local search and ≥ every island best; = local-search return when certified | sample | 80 | 0 |
| PIPs finite, in [0,1], = island mean; island PIP = rb_acc/(4N); original-index vector; MPM = {PIP > ½} | sample | 80 | 0 |
| log Ẑ_r = log m(∅) + log Z̄₀ + Σ increments; pooled = LSE − log 4; lower bound; relative scale | sample | 80 | 0 |
| Final-stage E1/E2/E3/low-ESS recomputed = stored flags; checks_passed_final; CSV diag codes (via production helper) | sample | 80 / 86 | 0 |
| Escalated ⇔ any tier-0 trigger (both directions); tier IDs 0 or 0,1; N = N0·4^tier | **population** | 2,400 | 0 |
| Every final island's φ sequence = grid[−1], and grid = frozen grid | **population** | 2,394 | 0 |
| Method seed = data seed + 4,000,000 | population (CSV) | 2,400 | 0 |
| Fit seed = CSV seed; stream map 0–13 (static metadata, not draw consumption) | sample | 86 | 0 |
| Budget values K = 100, B = 14, N0 = 2,500 checked by the worker. L = 8, ℓ = 10 (p500)/11 (p1000), H0 = 512, T0 = 1,000 recorded by the worker and verified by the manager and Sol against `v3_preprocess.R:19–30` and T:151–159 | sample | 86 | 0 |
| resource_limit: first exceeded checkpoint satisfies projected = elapsed + operation > allocation; both rules failed; `support` NA; `support_audit` = reported HPM | **population** | 6 | 0 |
| Centring fallback (`stable_centering`, X or y) absent; no dropped columns | **population** | 2,400 | 0 |

**Population facts** (all 2,400 RDS unless stated):
- 2,394 `completed`, 6 `resource_limit`; 208 escalated (p500: 63, p1000: 145).
- Tier-0 triggers among the 208 escalated fits: E2 alone 169, `grid_unconverged` alone 30, both 9. No other trigger caused an escalation.
- Final checks over the 2,394 completed fits (the 6 stopped fits have none): E1 0, E3 0, E2 83, low ESS 49, `grid_unconverged` 4.
- Final bridge stages: median 31 at both p, range 21–46.
- No completed fit had a guard checkpoint elapsed time, or a total time, above its allocation.

**The 6 stops.** All are S5 fits that had escalated (4× budgets). All six were runtime-guard stops; the memory estimate is ≤ 0.33 GB against 2 GB and never binds. The stop points are listed in `work/B_outputs.md`:

| Where the guard stopped | Fits |
|---|---|
| Final bridge | 4 (p500 r088_c100; p1000 r030_c100, r044_c050, r064_c050) |
| Tier-1 diagnostic island | 1 (p1000 r064_c100) |
| Tier-1 calibration local search | 1 (p1000 r044_c100) |

That last fit's preceding unguarded burn-in and measured block ran past the allocation, reaching 24,003 s against 24,000 s, and the next checkpoint caught it (D12). v2.2 records the stop point directly in `instrumentation$stop`.

## Deviation table

T = master Part I; L0 = METHODOLOGY_v3. Full citations are in `work/A_code_vs_text.md`.

| ID | Component | Finding | Class | Action |
|---|---|---|---|---|
| D01 | Status `grid_failure_no_escalation` | Emitted by `v3_calib.R:153` but unreachable: a tier-0 grid failure always escalates, or stops with `resource_limit`. | cosmetic | none |
| D02 | Top-level `grid_unconverged` | Selected tier only; tier 0 survives in `triggers_by_tier`. T is silent. | wording | T: "selected tier" |
| D03 | Guard duration at the grid checkpoint | Timed operation = V re-scoring (≤ 40p+1 scores) + grid + snapshot. T:393 describes only the grid algorithm. Under the narrow reading, the projection is larger by the V time, which could change availability near the limit. **Conformance interpretation adopted here: "grid construction" includes its V preparation.** Realised: no stop at a grid checkpoint. | conditional behavioural (resource guard), pending the T wording | T: define the timed operation inclusively |
| D04/D05 | Guard labels; sticky `exceeded` | Grid checkpoint logged with phase `diag`; nothing runs after the first hit. | cosmetic | none |
| D06 | Duplicate report vs preflight order | Preflight first; duplicates absent on a preflight stop. | cosmetic | none |
| D07, D14, D40, D42, D43 | L0 stale where T = code: SMC preflight is memory-only; `resource_limit` includes the in-run guard; secondary PIP removed; endpoint snap; one diagnostic local search per iteration (L0 is internally inconsistent) | T = code | wording (L0 only) | Mark L0 superseded by T |
| D41 | Relative-scale lower bound | T:447 asks for island and pooled evidence with the 95% lower bound "full scale and relative to m(∅)". Code emits `log_Z_lower95` (full scale) and `log_Z_rel_m0`, but no relative-bound field. Derivable exactly as `log_Z_rel_m0 + log 0.05`; no numerical change. | wording (reporting contract) | v2.2 could add the field in assembly; for the historical run the analysis derives it. Recorded in PATCHES (P2 note) |
| D10/D11/**S1** | **Allocation** | T table (T:163, 570): the job's actual request. The runner passed per-unit `hours = L/3600` (6,300 / 24,000 s) and `mem_gb = 2`; the Slurm task wall covers two units (GO_2400 C1, `runner/task.sh:20–22`, `submit.sh:56,68`). | **behavioural, study/resource policy, authorized by GO_2400 C1**; output availability for 6 fits | Reconcile T wording; stop rule for the rerun: **P5** |
| D12 | Unguarded stretches | No checkpoint in initial draws, burn-in or measured rounds (consistent with T). **Realised once:** p1000_S5_r044_c100 crossed its allocation inside an unguarded terminal block, and the next local-search checkpoint caught it (24,003 s). No external timeout. No completed fit exceeded its allocation. | none (consistent with T); residual operational risk | P5 note |
| D13 | Exact branch has no in-run guard | Consistent with T:180; not exercised at p ≥ 500. | none | — |
| D15/D16/D17/**S2** | Status mapping and `diag_flag` | T §I.7 still says "OPEN". Adapter = binding ruling R-1 as written in `study/SCHEMA.md:65–86`, including the documented asymmetry (`grid_unconverged` selected tier; `local_limit` any tier/search). No code path lets it alter HPM, PIP or evidence. The R-1 original text was not read (outside the briefs). | wording (T stale; implementation = adopted written policy) | T §I.7: cite R-1 and its definition |
| D18 | Partial-result labelling | Done; stop point recoverable from `runtime_guard$checkpoints`. | none | v2.2 adds `instrumentation$stop` |
| D19 | `adapter_version` 2.1-R1 vs SCHEMA "2-R1" | Doc mismatch. | cosmetic | v2.2 SCHEMA updated |
| D20 | Folds | Hash-checked, never reach the fit. | cosmetic | — |
| D21 | Hours printed `%.10g` | Allocation 24,000.0000012 s. | cosmetic | — |
| D30 | Near-constant centring fallback (X and y) | Not in T. Changes floating-point preprocessing when it fires. **Fired in 0 of 2,400 fits** (population scan, X and y). | conditional behavioural; inactive in this run | T: one sentence documenting it |
| D31 | Compiler/numerical environment | Flags, GCC 14.3.0, R 4.5.2 and the Sapphire Rapids pin are not in T. | wording | run manifest / T |
| D32 | Final-stream tier filled at assembly | NA on early stops. | cosmetic | — |
| D44 | cut_group scope | T:262 = code ("any split component"). The inventory's "broader than \|C\| > B" compares against L0/T22, not T. | none | see P4 |
| D45 | Scoring-layer fields (tp/fp/fn, truth retained) | NA by design; scoring layer. | none | P3 / LOWP scoring |
| D50/S3 | Scope | Part II: 5 scales and a p = 30 arm. Run: c ∈ {1, .5} at p ∈ {500, 1000}. | wording (study description) | Settled by D1/D5; Part II text to HQ |
| D51 | Seeds | Match T and the adapter (Part II data-seed formula cited by the worker; Sol checked the code chain, not Part II). | none | — |
| D52 | Retry asymmetry | Benchmarks got one doubled-time retry; SMC-BVS got none. | wording (study) | **P5** |

## Prior audits: cross-checked, with amendments

These statements are cross-checked, not wholesale re-certified. The worker spot-checked the THEORY_INVENTORY B.1 matches; Sol independently inspected the high-risk ones.

- **B.2.1** (mid-run stops): confirmed, with an amendment. The guard can also stop a fit during calibration, where no frozen grid and no final run exist (2 of the 6). Statements "conditional on calibration" are undefined there too.
- **B.2.2 and B.3** (secondary PIP, snapping, relative lower bound): confirmed. Note that the relative lower bound is a T reporting item (D41), not only an L0 item.
- **B.3** "diagnostic local search per island": an L0-internal ambiguity.
- **B.3** "cut_group broader than |C| > B": not a divergence from T (D44).
- **B.4 cut_group fired in 2,398 of 2,400 fits.** By arithmetic, the threshold √(2 log p / n) is about 3.5–3.7 null standard deviations. Over 1.2 × 10⁵ to 5 × 10⁵ pairs that gives ≈ 52 (p = 500) and ≈ 100 (p = 1000) chance edges per dataset. In the sample, 37 flagged components span the whole retained set. See P4.
- **B.4 escalation:** calibration-only, now with the population trigger breakdown (above).

## Open points

None needs an Astra ruling. Two items go to HQ:
- the T wording reconciliations (S1, D03, D30, D41, §I.7);
- the stop policy P5.
