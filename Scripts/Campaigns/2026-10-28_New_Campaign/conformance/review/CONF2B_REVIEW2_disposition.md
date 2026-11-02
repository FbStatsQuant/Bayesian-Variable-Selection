# CONF-2b review 2: disposition (CONF-2b manager, 2026-10-29)

Review: `CONF2B_REVIEW2_sol.md`. Sol's verdicts:
- **v2.2.1:** ACCEPT WITH FIXES. F1/F2/F4/F6/F7 are RESOLVED; F3 and F5 are PARTIAL.
- **PROD-H:** NOT READY (R2-1 blocking).

All findings are accepted.

## v2.2.1 and the regression harness (fixed by the manager)

| # | Fix | Where |
|---|---|---|
| R2-3 (F3 rest) | The scanner uses `record$native_status` only, the field the rerun itself checks. A record without it is invalid: a primary makes the scan refuse (exit 1); a rerun gets `invalid_inspect`. There is no `fit$status` fallback, so an `adapter_error` record stays legitimate. | `code/core/v2_2_1/tools/p5_scan.R`; `CHANGES_v2_2_1.md` |
| R2-2 (F5 rest) | The different-checkpoint branch now also requires each side's stop timings to be finite scalar doubles without attributes, and the invariant fields (`seed`, `allocation`, `n`, `p`, `budgets`, `preprocessing`, `branch_run`, `B`) to be identical. The only type change allowed is NULL on one side, for an island or stage not yet reached (`stage_record[[4]]` in the 0.0006 pair). Sol's corruptions (string `elapsed_seconds`, string `p`), plus a changed allocation and an NA timing, are added as negative controls on all three D10 pairs. | `conformance/work/v2_2_1_regression/scripts/a2_compare.R` |

**Results.** The four saved a2 pairs are unchanged in class: one is timing-excluded at the same checkpoint, three are D10. All 27 negative controls behave as expected.

**Manifest after R2-3.**
- `code/core/v2_2_1.SHA256SUMS`: 27 files; sha256 df4e7cf0e20981ef9fe4632fe2280355cbdb9e15d2dd724f1615b2c232054c41.
- `code/core/v2_2_1.diff`: 519 lines; sha256 26303af84092f23179d8e02fd0d361693b2a337e8e6fcdaf111c7fe220ec5860.
- The core is unchanged (byte-identical to v2.2).

**Tests of R2-3** (being added by a worker; results recorded below when in):
- a primary without `native_status` makes the scan refuse, and the adapter refuses the rerun too;
- a rerun without it gets `invalid_inspect`;
- a legitimate `adapter_error` record is accepted.

The pilot fixture gains `native_status`, and both pilot suites are rerun.

## PROD-H (delegated fixes; `jobs/PROD_H_DRAFT/REVIEW2_FIXES.md`)

| Item | Fix |
|---|---|
| R2-1 (blocking) | Per-job hold states (requested / failed / established), confirmed with squeue. Failed holds are retried on every poll, with a nonzero exit and an URGENT request. |
| R2-4 | The P5 scan runs as a guarded single-CPU compute job, with a completion receipt. P5 selection uses `launchable`. |
| R2-5 | Terminal cleanup of proven-stale P5 and primary locks and temp files once all jobs are dead. Attempt records are kept; nothing is relaunched. |
| R2-6 | `make_manifests.sh`: all three folders are preflighted first; a rerun is safe. |
| R2-7 | Writes after an accepted sbatch are guarded; on failure the job is cancelled by explicit id. Same in `rerun.sh`. |
| R2-8 | Throttle fails closed: every fb31 array is counted, or a campaign registry is used. |
| R2-9 | Execution logs go to scratch; home holds receipts, state and summaries only, plus a manifest for the run-summary folder. |
| R2-10 | Polls every 5–10 min; a gap > 600 s is late and recorded. |
| Q1 | `--qos=nots_commons` on every job (OPS confirms the QoS exists). |
| Q2 | P5 does not wait on terminal, reconciled, reported `infra_repeat`/timeout units, and never retries them. It still blocks on live, not_run, rerun_queued, infra and orphan. |
| Accounting | "Native-fit-budget ceiling" 10,100 core-h; requested-wall ceiling 10,540 core-h (10,541 with the precompile). |

Status: Sol re-check of the changed paths pending (review 3).
