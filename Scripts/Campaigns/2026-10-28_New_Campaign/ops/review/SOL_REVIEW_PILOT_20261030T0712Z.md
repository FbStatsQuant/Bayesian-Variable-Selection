# Independent Sol review: LOWP pilot and PROD-L sizing

Reviewer: Sol 6.1, independent review, 2026-10-30. Run: `20261030T0712Z_lowp_pilot`, jobs 2469168–2469179, JOB revision 7d.

**(A) Pilot accepted: YES WITH CAVEATS.** The computational acceptance evidence supports acceptance. Operational closure is attested in OPS_LOG, but the supplied evidence lacks the cleanup command transcript required to independently close JOB §10.7; see finding 1. Acceptance does not clear BENCH-AUDIT or authorize production.

**(B) PROD-L sizing: ACCEPT WITH FIXES.** Counts, observed allocation factors, the 16-thread enumeration estimate, and the separately gated benchmark estimate tie out. Correct the 8-thread derivation, qualify the stall model, repair the conservative arithmetic, and make batch deadlines and combined throttles explicit before the production bundle is accepted. No blocking computational defect was found in this pilot. Findings below are should-fix or minor.

## Scope and method

Read-only review of the named local specifications, summary tables, raw downloads, transfer receipts, OPS evidence/logs, and earlier failure report. No SSH/NOTS/Owls connection, fit, simulation, or benchmark was run. Only this review file was written. Checks used Python 3, R 4.4.1, and Git's awk locally; the R checks read saved records, without loading benchmark packages or regenerating data.

Abbreviations: `CAMP` = `02_Experiments/I_2026-10-28_New_Campaign`; `DATA` = `<PC_NOTS_DATA>/New_Campaign`; `LOG` = `DATA/logs/20261030T0712Z_lowp_pilot`; `SUM` = `CAMP/code/lowp/pilot/summary_20261030T0712Z_lowp_pilot`.

I independently rehashed **1,682 downloaded files** against the eight distinct transfer manifests, with no mismatch. The repeated scale_t32 pull is identical and counted once. I also checked all **259 unit sidecars** and EXACT completion hashes. The retained bundle tar hashes to the upload receipt and all **1,447 staged file hashes** match its internal staging list. Its summarizer and shared EXACT validator match the current versions. Archived JOB.md differs from current JOB.md only in the status paragraph documenting the subsequent submission; acceptance criteria are unchanged.

## Acceptance evidence

| JOB §10 requirement | Independent check and result |
|---|---|
| Exact sets and valid records | 39 EXACT records = 30 enum20 + 6 enum30 + 3 scaling; shared strict EXACT contract passes all 39. Read all 28 SMC and 192 benchmark RDS records; CSV/RDS/completion statuses agree and are `ok`. Counts total 259. No failed records were silently omitted. |
| Timing, CPU, memory | All 269 timing rows have rc 0, positive wall and positive GNU RSS. Each of the 259 units has exactly one matching timing row, and its wall agrees with `pilot_units.csv`. The other ten rows are the required non-unit commands/subsets. Enumeration has observed user+system CPU. All sizing units use GNU RSS, so the summarizer's fallback path is not involved. |
| Launch and frozen source | Archived source/staging hashes verified; `pilot.env` matches its saved SHA-256. Twelve submission vectors, real module settings, empty test hooks, and guard receipt are present. Guard probes refuse 513 MB and the home-overflow addition. Saved scripts request Sapphire Rapids; node evidence identifies Xeon Platinum 8468, 192 logical CPUs, two threads/core. Frozen-tree checks are recorded by the SMC tasks. |
| P0a, revision 7d | Raw report: 1,200 production + 60 dev regenerations, 1,260 truth files and six pilot input copies compared; zero mismatches. Mismatch CSV has its header only. Max scaled discrepancy is 3.55e-15, below 1e-12. Exact sealed-file/hash checks and tolerant regeneration are correctly distinguished; cross-platform regenerated arrays are not claimed identical. |
| Truth test and wave | 37 checks, zero failed, final exit 0. Production/dev pre-test hash lists contain 1,200/60 entries; lists after unlock and both recoveries are byte-identical to the respective pre-test lists. Wave lock verifies mode 000 and denied access; unlock reports 755/444 and equal hashes. Scheduler ordering independently places all fits after lock completion (02:16:00 scheduler time) and before unlock start (02:25:32). Last fit ends 02:25:15. UTC log times are five hours ahead of these scheduler timestamps. |
| Bit identity | Raw CSV has 26 passing rows covering T1–T5, zero byte mismatches/nonfinite values. T2 covers all 2^20 models at both scales; T3 covers 20,000 random p30 models at both scales. Aggregate discrepancies are within the declared tolerances. |
| Scaling | Four subset rows have the required dataset, 2^30 total models, 1,024 tasks, 31 tasks run, 32,505,856 scores, and one common 64-hex subset digest. Independently compared the four saved scale objects: outputs identical at 8/16/16/32 threads. Performance interpretation needs finding 2. |
| SMC and repeats | All 28 native statuses `completed`, no exceeded guard, allocations 2 GiB/4 h. Saved fit seeds agree with CSV/case seeds and data-seed offsets; all four repeats add exactly 1,000. Repeat log-Z differences reproduce the summary; all four HPMs agree. |
| Benchmark provenance | All 192 records specify R 4.5.2, `test_library=FALSE`, and the exact pinned R452 library. Non-base/non-recommended package provenance is directly under that directory, with versions and R 4.5.x builds. Method versions agree with CSV: glmnet 5.1, ncvreg 3.16.0, abess 0.4.11, susieR 0.14.2, SSLASSO 1.2.3.9001, bayesreg 1.3. This validates the pilot's provenance, not the pending benchmark-method audit. |
| Terminal Slurm | All 201 rows, including 67 parent jobs/tasks plus batch/extern rows, are COMPLETED with exit 0:0. The collector is terminal in `sacct_final.tsv`. |
| P5 | TSV has 28 units, all native `completed`, zero eligible, retry state `none`; consistent with all raw SMC records. No automatic retry occurred. |
| Cleanup | Transfer/delete receipts cover all seven result folders and the logs folder. OPS_LOG's 07:53:10Z entry attests `cleanup_pilot --yes CLEANUP VERIFIED`, empty runs/logs/results, and home 9.42 GiB. The actual cleanup stdout/exit/guard/residue transcript is absent from the named evidence. See finding 1. |

No evidence of a wrongly accepted failed computational unit was found. The summarizer's unqualified overall PASS does, however, omit the cleanup criterion, and its `accepted` projections are not production request approvals (findings 1 and 4).

## Measured pilot cost

Ran the requested helper, using its actual executable path:

```powershell
& 'C:/Program Files/Git/usr/bin/awk.exe' -F'|' -f "$CAMP/ops/scaffold/sacct_summary.awk" "$LOG/accounting/sacct_final.tsv"
```

An independent Python parse also summed only parent rows, excluding `.batch`/`.extern`: **10,066 allocated CPU-seconds / 3,600 = 2.796111 CPU-hours**, correctly rounded to **2.80**. The helper and OPS table agree:

| Step | Tasks | AllocCPUS/task | Allocated CPU-h | Max elapsed s | Max batch RSS MiB |
|---|---:|---:|---:|---:|---:|
| build | 1 | 2 | 0.015000 | 27 | 575.38 |
| verify | 1 | 2 | 0.005000 | 9 | 102.29 |
| truthlock | 1 | 2 | 0.032778 | 59 | 80.69 |
| lock | 1 | 2 | 0.002778 | 5 | 73.93 |
| enum20 | 1 | 4 | 0.074444 | 67 | 77.78 |
| enum30 | 6 | 16 | 0.853333 | 33 | 87.21 |
| scale | 1 | 32 | 0.862222 | 97 | 91.23 |
| bitid | 1 | 16 | 0.035556 | 8 | 261.39 |
| smc | 28 | 2 | 0.463889 | 526 | 188.75 |
| bench | 24 | 2 | 0.447778 | 35 | 255.74 |
| unlock | 1 | 2 | 0.002222 | 4 | 65.64 |
| collect | 1 | 2 | 0.001111 | 2 | 7.91 |
| **Total** | **67** | | **2.796111** | | |

RSS figures above are rounded from the saved batch values; they are MiB-equivalent Slurm M values. OPS's rounded MB labels do not affect its requests. Cost is below JOB's 7–14 CPU-hour forecast. Faster observed timings explain much of the difference, but platform, concurrency and cache conditions differ, so the entire discrepancy should not be assigned to processor speed alone.

For these actual submissions, every 1-CPU script received **AllocCPUS=2**; scripts requesting 4/16/32 received 4/16/32. Thus OPS correctly doubles single-thread wall-based costs under its stated allocated-CPU accounting convention. This is observed allocation accounting, not an independent audit of institutional billing/TRES weights or a universal guarantee for future Slurm configurations.

## Sizing tie-out

Production counts match RUN_DESIGN: 600 enum20 + 600 enum30 datasets, 2,400 SMC primary fits, **24 cells × 20 replicates × 5 extra seeds = 2,400 repeats**, and 2,400 benchmark cases × eight methods = 19,200 method fits. Repeats are extra fits; primary seeds are not counted again.

| Piece | Independently reproduced allocated CPU-h | Assessment |
|---|---:|---|
| enum20 | 600 × 1.951667 s × 4 / 3,600 = **1.301**; p90 2.436 s gives **1.624** | OPS 1.3/1.6 is sound. 600 sequential calls, 4 threads, 1 GiB/1 h is reasonable. |
| enum30, 16 threads | 600 × 27.415 s × 16 / 3,600 = **73.107**; p90 28.61 s gives **76.293** | OPS 73/77 is sound. 24 × 25, 1 GiB/45 min is reasonable against the sampled 11.4-minute task mean. |
| enum30, 8 threads | Actual scaling process wall 35.05 s gives **46.733**; OPS's assumed 42.5 s gives **56.667** | Both arithmetic calculations are correct, but only the first is directly measured on the scaling dataset. OPS's extra 10 s is not measured start-up; see finding 2. |
| SMC primary | Normal cell-balanced mean 7.242879 s: **9.657**; + 96 × 5 s overhead at 2 CPUs = 0.267; + 96/28 × 500 s at 2 CPUs = 0.952; total **10.876** | OPS approximately 11 is correct conditional on its per-task stall assumption. |
| SMC repeats | Mean of the two p-specific repeat means = 6.35 s: **8.467**; + 120 × 5 s overhead = 0.333; + 120/28 × 500 s = 1.190; total **9.990** | OPS approximately 10 is correct under the same assumption; repeat timing coverage is only two fits per p. |
| Benchmarks, current code | Mean case wall 28.535417 s; (2,400 × mean + 96 × 5 s) × 2 / 3,600 = **38.314** | OPS approximately 38 is sound. Per-method contributions reproduce its table. 1 GiB/1 h is reasonable relative to measured 256 MiB and approximately 12-minute tasks, subject to BENCH-AUDIT/re-sizing. |

With OPS's stall model and 16 threads, subtotal excluding benchmarks is **95.274**, and including current benchmarks **133.588** CPU-hours. Its approximately 95/133 figures are approximate rather than precise rounded totals. The 8-thread alternative is provisional; substituting OPS's 42.5-second allowance gives approximately **78.834/117.148**. These estimates exclude production build/gate/collector costs, retries and scoring; make that scope explicit in a production budget.

## Numbered findings and concrete fixes

1. **Should-fix — cleanup acceptance is not independently evidenced.** JOB §10.7 requires `CLEANUP VERIFIED`. `summarize_pilot.R` has no cleanup verdict or receipt input; its sixteen PASS rows therefore cannot establish all of §10. The named collect transcript ends at `COLLECT_DONE`, before cleanup, while OPS_LOG contains only the attestation. **Fix:** OPS should attach the existing cleanup invocation/stdout, exit status, residue check and final guard output, if retained. Otherwise obtain a fresh read-only residue/guard verification through OPS and clearly label it retrospective. Add a distinct operational-closure receipt/verdict to future acceptance, while preserving this historical summary. Until then retain the pilot's qualified acceptance, not an assertion that every criterion was independently evidenced.

2. **Should-fix — the 8-thread cost uses a false start-up derivation.** OPS §2 subtracts 17.7 s from 27.4 s. These are a scaling-job 16-thread in-process measurement and the six enum30 tasks' mean process wall, respectively. Actual mean process overhead in those six tasks is **27.415 − 25.443667 = 1.971333 s**. Raw scaling rows give process/in-process **35.05/32.481**, **19.65/17.686**, **15.31/14.087** s at 8/16/32 threads. The same S4 dataset took **28.69/27.068** s in its primary enum30 task, demonstrating substantial between-job performance variation. **Fix:** remove the claim of fixed 10-second start-up. Use 35.05 s as a clearly labelled single-dataset 8-thread baseline (46.73 CPU-h), or explicitly retain 42.5 s as an added performance allowance (56.67 CPU-h). Do not call the 22% saving established: the matched scaling pair gives 46.73 versus 52.40 CPU-h, about 10.8% savings; comparison with the six-task 73.11 estimate confounds conditions. Keep 16 threads as the supported design unless HQ accepts a provisional 8-thread scenario or obtains additional comparable timings.

3. **Should-fix — the stall allowance is a scenario, not an identified task-level rate.** Raw evidence confirms task 2469176_8 on bb3u18c1: **526 s elapsed**, GNU-timed process **206.51 s wall / 12.23 s CPU**, and **319.49 s outside the timed process**. The saved fit itself reports **3.341 s runtime**, guard elapsed 3.11 s, with no escalation. This supports non-compute delay, plausibly filesystem/start-up I/O; it does not establish node-level causation or whether delays recur once per task, once per R invocation, or in correlated bursts. Pilot tasks contain one fit each, so task and fit incidence cannot be separated. Production still launches one R process per fit. **Fix:** retain the clean-fit means, but label approximately 11/10 CPU-h as conditional on once-per-28-task delays. Include a sensitivity case that retains the observed primary per-fit wall tail and adds task-level outside-process delay: approximately **21.63 CPU-h primary**; applying one excess process delay per 28 fits to repeats gives approximately **19.07 CPU-h repeats**. These are sensitivity scenarios, not confidence limits. Preserve and monitor both per-fit and per-task wall/CPU evidence in production; revise budgets when real batch evidence is available.

4. **Should-fix — the conservative SMC totals do not follow the stated formula.** With 11 s/fit, the same 5 s/task and 500 s per 28 tasks give **15.886 CPU-h primary** and **16.190 repeats**, not approximately 15 each. With exact enum p90 values the non-benchmark conservative subtotal is approximately **110.0**; using OPS's displayed enum30 77 gives approximately **110.7**, so advertise approximately **111**, and approximately **153** with the displayed benchmark reserve of 42. **Fix:** state formulas for every conservative column (including the currently unexplained 8-thread 62 and benchmark 42 allowances) and recompute subtotal/total from unrounded values. Also mark the summarizer's generic `accepted` projection as superseded for production resource sizing: it uses one charged CPU for SMC/bench, p20 p90 below its stall-inflated mean, and 512 MiB/30-minute SMC suggestions incompatible with the intended 2 GiB/4 h allocation. OPS correctly overrides these; downstream users must not copy the generic table unqualified.

5. **Should-fix — a four-hour per-fit guard is not a four-hour batch completion guarantee.** Keeping `--mem-gb 2 --hours 4` is appropriate: reducing them to the summarizer's suggestions would change the operational allocation used by the core. But `v3_fit.R` creates a new four-hour runtime guard for each fit, while a proposed Slurm task holds **25 primary or 20 repeat fits sequentially** under one four-hour deadline. A late long fit can be killed by Slurm before its own guard triggers or before its record is committed. The pilot's one-fit tasks do not validate that case. **Fix:** keep the nominal 2 GiB/4 h fit allocation and define batch deadline handling: stop launching fits without adequate remaining scheduler time, checkpoint completed units and explicitly resubmit remaining units; allow a long fit to run in a fresh task with scheduler headroom, or give the batch a separately justified larger wall limit. Save a completion inventory so skipped/killed units cannot be counted as successes. Four hours is ample for measured ordinary batches, but does not bound the unobserved escalation tail of an entire batch.

6. **Should-fix — enforce the combined concurrency and wave policy.** The 24×25 enum30, 96×25 primary SMC and 120×20 repeat arrays are sensible; modest throttles and halving while PROD-H runs are reasonable fair-share choices. The advertised **132/68 charged CPUs** assumes at most one of SMC, repeats and benchmarks overlaps enumeration. A cleared benchmark launched concurrently adds 64/32 CPUs, giving **196/100**, and PROD-H is additional. A per-piece cap does not enforce a campaign cap or actual one-node placement. **Fix:** explicitly serialize benchmark versus the SMC/repeat lane, or dynamically lower throttles to an agreed combined PROD-L/PROD-H ceiling. State the full H+L budget and update wall estimates accordingly. In the concrete bundle, complete guard checks/staging before a shared truth lock, and have unlock depend on every consumer of that locked tree; do not run home `du` guards during its locked wave or unlock independently when just one piece finishes. Keep benchmark submission conditional on BENCH-AUDIT, with revised F3 cost and memory validated after changes.

7. **Minor — disk units and repeat-record sizes need clarification.** Home arithmetic is acceptable: one shared approximately 100 MiB addition to 9.42 GiB leaves roughly 80–90 MiB below 9.6 GiB. This is conditional on a fresh guard, all concurrent staging/cache additions being included, and inputs/code not copied afresh for each piece. Raw output means project enum **0.111 GiB**, SMC primary **0.876 GiB**, repeats **1.005 GiB**, current benchmarks **1.492 GiB**: **3.485 GiB = 3.742 decimal GB**, before logs/caches or tails. The repeat records are larger than the primary records at p30 (711 versus 588 KiB), so assigning 0.9 to both is not a literal repeat-based extrapolation. **Fix:** label scratch units as GiB and round the measured baseline up (approximately 3.5 GiB, or at least 4 decimal GB before additional reserve); state whether primary sizes are intentionally substituted for repeats. Include logs, caches and escalation growth separately. Keep the live guard authoritative and use the established archive/verify/review route if it refuses.

8. **Minor — distinguish requested CPU-hours from the allocated ceiling.** JOB's **311 CPU-h** is correct for requested `--cpus-per-task` × wall limits. Under the observed doubled allocations, summing parent `AllocCPUS × Timelimit` gives **472.667 allocated CPU-h**, not 311. **Fix:** preserve JOB's historical requested figure, but distinguish it from the corresponding allocated ceiling in OPS §1. Continue using 2.796111 as actual elapsed allocation cost. Describe the whole-core/SMT explanation as consistent with observed node topology and allocation, rather than treating sacct alone as proof of billing policy.

## Audit anchors

SHA-256 values at review:

| Input | SHA-256 |
|---|---|
| Retained pilot bundle tar | `d54c01a2ce08f96df7c2a8c0f57a94d2a5adcb94a26ee00c62f739e520dd54fc` |
| Archived JOB.md | `408270851e63292b40bfe498b8276cedf277c01eab2ffb078b960b63abc56651` |
| Current JOB.md | `7ff0d3885bea3634d2b3fb77ad9c927bae269474113695166658cda3f3b07dd8` |
| summarize_pilot.R, archived=current | `7e4406c85dae41b9e27cdc9718d864919fa9d419ec5fc3fb42ff7218c1c14520` |
| exact_contract.R, archived=current | `284db4f180c7b4709bcf635d5a196af3fa5ecaf9963d635e3fa4ec4e273c57bc` |
| PROD_L_SIZING_20261030.md | `e79bf125ee216eb3a2232a07db12ea7c3f4f9d8547a05db9b08288f052fb89d5` |
| sacct_final.tsv | `04af560379f255acacabf96ab508294809ed9571f00a84c13e116824378d83f5` |
| pilot_units.csv | `a5b54c335b3a87474439e9e4d5f6c8df8bb38406e33cc3646237912a082c0758` |

Final local record-check invocation: R 4.4.1 `Rscript.exe --vanilla -`, exit 0; 39 strict EXACT validations, 28 SMC checks, 192 benchmark checks, four repeat pairs and four-way scale identity passed. Python independent hashes, accounting and arithmetic checks passed; awk reported `TOTAL core-hours (AllocCPUS x Elapsed): 2.796`. No production changes or remote verification were performed by this reviewer.
