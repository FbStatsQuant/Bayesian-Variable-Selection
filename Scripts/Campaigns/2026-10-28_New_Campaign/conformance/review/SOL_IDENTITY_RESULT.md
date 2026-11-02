**Gate verdict: PASS-WITH-AMENDMENT.** Both units are bit-identical in all pre-existing computed/non-provenance content under JOB.md's declared timing/memory exclusions. The unchanged acceptance gate remains FAIL (exit 1, two criteria); its sole failing path per unit is an exempt command-provenance vector's length. No numerical identity failure was found.

Reviewed independently by Sol 6.1 on 2026-10-29 using local R 4.4.1 and PowerShell only. No SSH, cluster contact, fits or cluster reruns; no existing bundle/data file modified.

Evidence paths used below:
- J = <OLD_ROOT>\02_Experiments\I_2026-10-28_New_Campaign\conformance\jobs\CONF_NOTS_IDENTITY
- N = <PC_NOTS_DATA>\New_Campaign\results\conf_identity\results\conf_identity\p0500
- H = <PC_NB_ARCHIVE>\smcbvs_v3_deploy_20261022\claude\prod_p0500_20261023T1227Z\p0500
- L = <PC_NOTS_DATA>\New_Campaign\logs\conf_identity
- D = <OLD_ROOT>\02_Experiments\I_2026-10-28_New_Campaign\ops\evidence\conf_identity_command_diag

Findings:
1. **OPS's diagnosis is correct, with "only difference" understood after the specified exclusions.** Re-running J\cmp2.R on each H\<unit>\SMCBVS.rds versus N\<unit>\SMCBVS.rds reproduced J\ACCEPTANCE_2455971.log exactly:
   - p0500_S3_r044_c100: 175927 paths compared; 1 difference; 0 non-allowlisted additions; 46 allowlisted additions.
   - p0500_S5_r059_c100: 221287 paths compared; 1 difference; 0 non-allowlisted additions; 85 allowlisted additions.
   - Both sole failures: record$environment$command [exempt value: length differs].
   - Raw records also contain expected excluded timing, memory, source/provenance and run-identity differences; entire RDS/CSV files are not byte-identical.

2. **Independent computed-content check: YES for each unit.** A separate recursive walk checked 175356 / 220205 pre-existing leaves using strict identical(..., num.eq=FALSE, single.NA=FALSE, attrib.as.set=FALSE) and raw writeBin equality for doubles/complex values; zero unexpected differences and zero non-data objects. Original container types, non-name attributes and old name prefixes were checked; cmp2 additionally enforced the additions allowlist/order.
   - CSVs: each historical/new pair has 2 rows, 88 columns; all 79 non-provenance columns (158 cells per unit) are identical when read as character data. Only the nine declared provenance/timing columns change.
   - Normalizing only the command vector in memory gives 0 differing paths / 0 bad additions for both units, with the original path counts unchanged.
   - Re-evaluating all original compare_identity.R acceptance expressions, substituting PowerShell SHA256 lookup for digest and capturing quit, reproduces precisely the two cmp2 failures; every other criterion passes, including instrumentation and job-environment checks.

3. **The CLI difference is legitimate recorded provenance, not evidence of a changed fit input.** Independently read argv matches D.txt and D.R: both historical commands are attribute-free character vectors of length 22, both new commands length 20.
   - Historical argv includes --run-id prod_p0500_20261023T1227Z, --core-dir /home/fb31/projects/BVS/SMC_BVS_v3/deploy/claude/code/v2_1/code/core, --mem-gb 2, and dataset IDs without _c100.
   - New argv, matching J\job.sh and L\run_env_2455971.txt, uses --run_id conf_identity, --mem_gb 2, the suffixed case IDs, and omits the two-element --core-dir pair. Both use --scale c100, the same study root and --hours 1.75; script/output roots differ by design.
   - Resolved record$case, full record$input (including paths, manifest row and all data hashes), allocation/hash, adapter policy/hash, and fit settings are strictly identical.
   - S3 resolves to dataset p0500_S3_r044, case p0500_S3_r044_c100, data/fold/method seeds 1440044/3440044/5440044; S5 resolves to dataset p0500_S5_r059, case p0500_S5_r059_c100, seeds 1460059/3460059/5460059. Fit seeds equal the corresponding method seeds; both have n=200, p=500, scale=1, development=FALSE.
   - Allocation is 2 GB / 1.75 h in both records and fits; recorded Slurm allocation is 1 CPU / 2048 MB in historical and new runs.
   - The omitted core option resolved to record$code$core_dir=/home/fb31/projects/BVS/New_Campaign/code/v2_2/core, the intended new core. Historical/new adapter source hashes are b28719e65383bd23b29f1ae496c2bd83668e6aee318061e852b9ee33dc394e23 / 2e39575aa31d82797bac4f80108dd4340c9b6eac96a1b70a53c68c2918108d9c; core hashes are 8d03d3649cffe68527ed71efb824c644d3a6245a6109f2929029f1c86cace1f8 / c0aebe86bfd07525bc97e2fd2bcacf4608142c778d25d584a38119e96ef82517, exactly the pinned versions.
   - Run ID changes only the observed excluded provenance/output destination; all saved computed fields, streams, calibration decisions and results match. No computed difference is concealed by the argv exemption in these records. Parser source was outside the permitted paths: this is evidence for these two executions, not a claim about arbitrary CLI forms.

4. **Integrity and numerical environment are corroborated.** PowerShell SHA256 verifies new manifests and all four historical pins; the six bundle hashes match L\run_env_2455971.txt.
   - New S3 RDS/CSV: ff31f83375110ba16854785cf722145042488c9feeabb20f276ed66b3f0a3bcc / d3a0156cd1e05e243a49dc40bbe9a2c4234dc26f246d1cc9b67698443b1748b3.
   - New S5 RDS/CSV: 80b9e8e0ef8c4381824fd3f01ae6d5a8e51e494710d7a11fe70ffb4014bf5551 / cf9e95a9832a520196e8ba0a070ca0df6016e82d92c5568b156c82e64a748bc9.
   - Historical RDS pins: S3 27b7c546359196c5cb6a5e2aafc74c586c61520fc89585d25315ba175460f4a5; S5 83254f90f44258e226b73ddd0a33808a628a275da4ba2af1c2074da002d97dd5. Historical CSV pins also verify.
   - Entire recorded session_info and compiler vectors are identical: R 4.5.2 (2025-10-31), GCC modules 14.3.0, Rcpp 1.1.0, FlexiBLAS OPENBLAS; LAPACK version 3.12.0, x86_64 Linux/RHEL 9.4; RNGkind Mersenne-Twister/Inversion/Rejection; all five recorded thread settings are 1.
   - Both fit statuses are completed, branch smc; S3 tier 0, no escalation/reasons; S5 tier 1, escalation reason exactly E2, not blocked. The real escalation path is confirmed.

5. **Logs and performance qualifications.** L\sacct_2455971.txt: job/batch/extern COMPLETED, 0:0, elapsed 00:22:26, node bb2u17c1, batch MaxRSS 588976K. L\2455971.out reports "status= ok,ok skipped= FALSE" for both units; run_env has one final_status 0, failed_case none, and one successful launch per unit.
   - L\compile_2455971.log warns v3_core.cpp has modification time "14 s in the future" and "Clock skew detected. Your build may be incomplete." It nevertheless records actual compile/link commands and successful fresh compilation; the job refuses a pre-existing cache. Preserve/disclose this warning; it does not overturn the observed saved-output identity.
   - Actual compiler flags include -O2 -fno-math-errno -ffp-contract=off -march=x86-64-v2; the module's reported default -march=native is not the actual compile command.
   - Compile key f8e3c15d6b38c8edd47012fa28706f39f7b6f468d3aa4f9b6a666df50fcdb508; shared-object SHA256 e7b9359005a68c2f9660fb222ec5a62f1fecf0d22f43dd6c8e6f37773a877775.
   - Recorded runtime_s: S3 317.968 versus historical 272.051 (+16.8781%); S5 1003.344 versus 828.098 (+21.1625%). Timing is explicitly excluded. These isolated runs flag a performance concern but cannot identify its cause or establish a controlled regression.

Minimal remedy for CONF:
- In J\cmp2.R, amend shape_cmp's length condition only to: if (length(x) != length(y) && path != "record$environment$command") ... . Keep type, names and attribute checks; retain every other shape/additions/computed-content check and the separate numerical-environment criteria. Changing only CMP2_EXEMPT_REC will not fix this: the environment subtree already delegates recursively to shape_cmp.
- This exact amendment was tested only in memory against untouched records: the full acceptance replay prints ACCEPT, with 175927 / 221287 paths and zero differences/bad additions. Negative controls still reject an unrelated environment-vector length change, a changed computed fit$log_Z, and a non-allowlisted addition.
- CONF should document the narrow spec clarification and version/hash the amended comparator, then rerun local acceptance on these same verified outputs, preserving the original failing log. No NOTS rerun is needed; matching historical argv length would only satisfy an accidental shape constraint.
- Review scripts and hash lookup are in <PC_TEMP_PATH> (review_nobom.R, independent.R, amendment_check.R, hashes.csv). No amendment was written to the bundle.

**Per-unit verdicts: S3 YES; S5 YES. Gate: PASS-WITH-AMENDMENT.**
