# OUTPUTS: Campaign 2 production (written by HQ, 2026-10-28)

## Runs
| run_id | Slurm array | units | outcome |
|---|---|---|---|
| prod_p0500_20261023T1227Z | 2365495 (600/600 tasks COMPLETED) | 1,200 | 1,199 ok, 1 resource_limit |
| prod_p1000_20261023T1227Z | 2365494 (600/600 tasks COMPLETED) | 1,200 | 1,195 ok, 5 resource_limit |

- Units: 2,400/2,400 finished. 0 timeout, 0 infra, 0 orphan, 0 method_failed. ever_infra = 0. 208 escalated (p500 63, p1000 145).
- **Reruns: none.** No unit needed an infrastructure rerun, so there is exactly one bundle per unit, from the original job.
- resource_limit (GO_2400 C5): 6 units are budget-censored. They count as non-recovery and get their own category in the analysis.

## Verification
1. On NOTS (2026-10-28), `reconcile.py RUN --sacct --full-verify` on both runs: all 1,200 units in each are `done`, and every RDS+CSV was re-hashed against its `.done`/`.sha256`.
2. Transfer: one tar streamed over ssh, `prod_results.tar`, 4,012,247,040 bytes, sha256 c6dcfeb7d83cf118f3a7586b6c6d2f73518b80e8e101f7fc9fcc7cf00dcb2d91.
3. On the laptop: `sha256sum -c SMCBVS.sha256` in every bundle dir. 2,400/2,400 pass, 0 fail; 2,400 `.done` files are present.

## Laptop results roots (scoring inputs)
- `C:\Users\felip\Documents\NOTS_BVS\smcbvs_v3_deploy_20261022\claude\prod_p0500_20261023T1227Z\` (contains `p0500/<case_id>/SMCBVS.*`)
- `C:\Users\felip\Documents\NOTS_BVS\smcbvs_v3_deploy_20261022\claude\prod_p1000_20261023T1227Z\` (contains `p1000/<case_id>/SMCBVS.*`)

The run_id equals the folder basename, so score each root in its own pipeline pass.

## NOTS copy
The originals are still at `/scratch/fb31/smcbvs_v3_deploy_20261022/claude/prod_*/results/`. They are NOT yet deleted; deleting them needs Felipe's go-ahead (he ordered a stop on 2026-10-24).
