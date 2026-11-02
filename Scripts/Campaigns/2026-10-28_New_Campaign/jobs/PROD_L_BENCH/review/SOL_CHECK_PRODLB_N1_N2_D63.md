# Sol narrow check: PROD_L_BENCH N1/N2 and PROD_L D63

Date: 2026-11-02 UTC. Scope is HQ D53 N1/N2, extended by D63 only. B = CAMP/jobs/PROD_L_BENCH; PL = CAMP/jobs/PROD_L. No implementation changes were made. The only campaign write is this report.

**N1 — RESOLVED.** `B/accept_bench.R:111–123` requires support/k for every method, enforces sorted unique indices in 1:p and finite integer cardinality for successful rules, permits the empty selection with k=0, and requires NA selection/size for failed rules. Lines 155 and 171–179 bind F coefficient-entry support/k and A fit$rules support/k/status to rows; A2 additionally checks which(beta != 0). This matches `code/bench_lowp/R/common.R:62–64`, `R/methods/fit_A2_ssl.R:152–155`, and `run_bench_case.R:147–165`. No new class-(i) selection defect was found in these fixes.

**N2 — RESOLVED.** `B/accept_bench.R:165–169` now includes bic, checking support, k and criterion equality with bic_K37 using the existing NA-aware comparator. `common.R:79–84` creates all three aliases for F4/F5. The exact original bic_alias_mismatch attack now fails specifically with `bic / bic_K37 pair differs`; genuine aliases remain accepted. No new class-(i) alias defect was found in this fix.

**D63 — NOT RESOLVED.** The fixed 00:30:00 has correctly been replaced: `PL/prodl.env:43–48` sets BASE=600 s, MS_PER_UNIT=1500, MIN=7200 s; `PL/submit_prodl.sh:97–104` counts smc+smcrep rows, rounds up fractional seconds, applies the floor, and passes the resulting --time explicitly. For 14,400 rows the value is 22,200 s = 06:10:00, matching `PL/slurm/s5_p5scan.sbatch:10–11` and JOB.md §6. The batch script runs smc then smcrep and writes scan_<phase>.ok only when both succeed (`:24–26`; `slurm/common.sh:128–160` accumulates failures and exits nonzero). These mechanics pass the tests below.

One scoped class-(i) deficiency remains in the new time calculation: **its list count does not include P5 retry records that a legitimate final scan also reads.** `code/core/v2_2_1/tools/p5_scan.R:30–37,64–80` calls status_of for each valid primary and again for an existing retry; status_of validates sidecars, reads CSV and deserializes RDS. `PL/JOB.md:43` requires scans after fitting/P5 and a final scan; P5 is allowed once per eligible primary, with no small-fraction cap. Yet --time depends only on the unchanged primary list, irrespective of phase or number of retries. Thus 14,400 primary records plus up to 14,400 legitimate retry records still receive the same 06:10:00. The new formula is not proportional to all records actually scanned.

Margin judgment: 1.5 s per primary plus 600 s is a reasonable provisional margin for the initial scan, but is insufficient as a general allowance for the supported final-scan workload. The supplied observation is a lower bound (>=0.75 s per smc record), not an upper-bound timing measurement. At p=30 the documented repeat/primary file-size ratio is 711/588, about 1.21 (`ops/PROD_L_SIZING_20261030.md` §5). Under a simple byte-proportional illustration, 2,400 smc plus 12,000 smcrep records cost approximately 12,683 s at a 0.75 s smc baseline, leaving approximately 1.70 times the work allowance after the 600 s base. Scanning equally costly retries for all those units would cost approximately 25,365 s before fixed overhead, exceeding 22,200 s. This is an illustrative permitted workload, **not a measured new timeout**; retry records need not be identical in size to primaries. Even assuming every read cost only 0.75 s, full retry coverage consumes the entire 21,600 s variable budget, leaving no factor-of-two margin. Larger smcrep records and retry validation make treating that as an adequate safety allowance unjustified.

A different margin is needed for final scans: include existing retry records in the workload count, or conservatively reserve for one retry per listed primary, and apply the per-read margin to that total. Retain the base/floor, ceiling arithmetic and explicit sbatch override. Validate an initial and a heavily retried final workload rather than only checking >=1.5 times the primary-row count. This finding is confined to the D63 sizing fix; it does not reopen the prior P5 correctness review.

PROD_L_BENCH has no P5 scan: `B/submit_bench.sh` supports main/rN and bench/benchretry submissions; its slurm directory contains common.sh, s0_verify, s1_bench, s2_benchretry and s9_collect only. D63 applies to PROD_L.

## Independent execution and saved evidence

Fresh scratch root (TEMP): `<PC_TEMP_PATH>`.

Copied the R2 `extra_checks.R`, R2's R1 replay `check_accept.R`, and one.tsv from `r2_20261102T111720Z`. Each script differs only in its root literal. The replay retains the R2 CLI arguments and genuine run basename; fresh p0020 junctions reproduce the R2 layout without rewriting record run IDs. The historical raw R1 script lacks the now-required CLI arguments, so the requested replay is the R2-compatible R1 replay, as in the prior review.

| Exact attack/control | Gate exit | Saved CSV outcome |
|---|---:|---|
| genuine live records, --local-test | 0 | 24 PASS, 0 FAIL, 0 INCOMPLETE |
| wrong_k | 2 | 7 PASS, F1 FAIL: cardinality and coefficient/row k mismatch |
| a2_wrong_selection | 2 | 7 PASS, A2 FAIL: fit$rules mismatch and beta support mismatch |
| a_selections_deleted | 2 | 5 PASS, A1/A2/A3 FAIL: support/k columns missing |
| bic_alias_mismatch | 2 | 7 PASS, F4 FAIL: bic/bic_K37 pair differs |
| foreign_dataset | 2 | 7 PASS, F1 FAIL |
| altered_files_refp | 2 | 7 PASS, F1 FAIL |
| missing_record | 3 | 7 PASS, A3 INCOMPLETE |

R1 replay controls remain unchanged: baseline exit 0, eight PASS; missing_derived, wrong_role, missing_ols, missing_pip, wrong_identity and missing_provenance each exit 2. Saved evidence: TEMP/extra_checks.log, check_accept.log, extra_accept_<variant>/{accept_bench.csv,ACCEPT_BENCH.md}, accept_<variant>/{accept_bench.csv,ACCEPT_BENCH.md}, and per-gate stdout/stderr. Gate artifacts and attack reasons were inspected. PowerShell wrappers reported status 1 while capturing R locale startup warnings; the completed replay logs and gate outputs above supply the individual gate outcomes, rather than treating wrapper status as their result.

Suites were run sequentially from TEMP/campaign/jobs/{PROD_L_BENCH,PROD_L}/tests, preserving the CAMP-relative layout and copying frozen bench_lowp and its r2 manifest. Only the prodl_tests path literal in each copied lib.sh was replaced with the fresh scratch path (lowercase in its case guard, which lowercases input). test_accept.sh, test_driver.sh, fixtures and vector checker were unchanged.

- Fresh `test_accept.sh`: **156 passed, 0 failed**, shell exit 0; TEMP/test_accept.log. ACN1a–h and ACN2a–c reject their intended mutations with the expected reasons. ACN3a null selection and ACN3b failed rule each remain accepted with 24 PASS and no FAIL. The frozen CLI's real-case positives and genuine live control pass.
- Fresh `test_driver.sh`: **367 passed, 0 failed**, shell exit 0; TEMP/test_driver.log. D40–D48 verify the primary-count formula, floor, ceiling and exclusion of enum rows. They do not exercise retry-record-dependent time allocation: scan_case always uses phase initial and its margin assertion counts only primary-list rows.
- Supplied logs inspected: B/tests/TEST_ACCEPT_n12.out = 156/0; PL/tests/TEST_DRIVER_d63.out = 367/0; PL/tests/TEST_P5_d63.out = 152/0. The P5 suite log was inspected; that suite was not rerun (only the two requested suites were rerun).

Launch commands (absolute paths; one suite at a time):

```powershell
& 'C:/Program Files/R/R-4.4.1/bin/Rscript.exe' '<PC_TEMP_PATH>'
& 'C:/Program Files/R/R-4.4.1/bin/Rscript.exe' '<PC_TEMP_PATH>'
& 'C:/Program Files/Git/bin/bash.exe' '<PC_TEMP_PATH>' '<PC_TEMP_PATH>'
& 'C:/Program Files/Git/bin/bash.exe' '<PC_TEMP_PATH>' '<PC_TEMP_PATH>'
```

Actual launches redirect stdout/stderr to the corresponding TEMP logs. Laptop R 4.4.1 uses the existing lowp_Rlib; at most two R processes are involved concurrently (replay/fixture plus child); driver uses scheduler/R stubs. No SSH, NOTS connection or network was used. No real truth folder or truth manifest was accessed. The expressly requested driver suite creates and checks synthetic truth-named fixtures solely under TEMP/driver_work; these contain dummy text, not campaign truth. No seeds, frozen fitting code or campaign configuration were changed.

Noted, out of scope: no additional findings reported; historical R1/R2 dispositions are not reopened.

**NOT RESOLVED: D63**

## SHA-256 of reviewed campaign files

Paths below are relative to CAMP. Snapshots are retained under TEMP/campaign; hashes are also saved in TEMP/SHA256_reviewed.txt.

```text
af50bd6f4395f91f285cfe5b61f68f9598255fa6370984b3aa40a3327cd0e151  jobs/PROD_L_BENCH/accept_bench.R
276c0fdb1b4bc63838915427882639ea075927d17b7f159264d4704f8dcc98e6  jobs/PROD_L_BENCH/tests/test_accept.sh
87d41625fd009e3703c56c081374ac4c8507df492a0d2e1237d0391d76ebd3d2  jobs/PROD_L_BENCH/tests/make_accept_fixture.R
df2b064136c6f661a60063f18fa0091906d81e2f38fd01fe704d188963da4b1a  jobs/PROD_L/prodl.env
d45887e6b42b8f7ff0e6684f92091f82833d71b223a8935492b2095e17c6efbe  jobs/PROD_L/submit_prodl.sh
17d2ba85adda091cb7cf3e6559444e734086931f4d658c55ed1db39391e2e192  jobs/PROD_L/slurm/s5_p5scan.sbatch
ede350e2a1f2ca71a10bfa2b37283e844cd7c106bc6aadeb49585fcb61bc5368  jobs/PROD_L/tests/test_driver.sh
```
