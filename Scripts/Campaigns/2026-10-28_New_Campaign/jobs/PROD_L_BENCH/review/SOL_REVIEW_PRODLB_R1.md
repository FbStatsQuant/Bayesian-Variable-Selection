# PROD_L_BENCH — independent Sol review, round 1

**Verdict: NOT READY.** Four class (i) acceptance defects must be fixed before OPS stages this bundle. The execution machinery is substantially sound; the blocking defects are in the final scientific acceptance gate. The two scoped post-READY PROD_L changes are accepted. One class (ii) recovery procedure should be added to JOB.md §14.

This is round 1 under D53: at most two full rounds. After round 2, class (i) fixes receive narrow checks; class (ii) findings are documented for HQ acceptance. No SSH, NOTS, network, new fits, delegation, or running production-stage changes were performed. The only campaign write is this report. Review-local copies and saved-record experiments are under `<PC_TEMP_PATH>`.

Paths below are relative to CAMP; `B` means `jobs/PROD_L_BENCH`, `PL` means `jobs/PROD_L`. Line numbers refer to the hashed files in the appendix.

## Findings

### I1 — **class (i)** — the first record can redefine the required rule registry

**Location:** `B/accept_bench.R:52–60`, particularly lines 54 and 57–58.

The checker requires the original registry IDs as a subset, then learns the complete rule/role signature from the first result of each method/p. It does not require all LA-4 derived rules, reject extra rules, or independently establish most roles. A systematic omission therefore passes every subsequent record. On a saved real case, removing F4 `ebic1_lam005` from rows and both coefficient lists still returned ACCEPTED, exit 0. Changing all A1 roles to `S0` also returned ACCEPTED. Either can remove a scientific result or change its attribution. The supplied positive acceptance fix correctly recognized derived rows, but replaced a false rejection with an insufficient reference check.

**Concrete fix:** construct the exact expected ordered `(rule_id, role)` vector from the frozen registry and the deterministic structural transformations in `R/common.R::lowp_derive`. For F1–F5, cap `ebic1/ebic05/bic` roles become secondary; F4/F5 append the three K37 aliases and their respective `ebic1_lam005`/`sic_smax` rule, with the frozen roles. Require exact equality, including order, and reject missing/extra IDs. A1–A3 must equal their registry exactly. Add negative controls for a missing F4/F5 derived rule, extra rule, and incorrect role in the first and every record of a method/p; keep the genuine live records positive.

### I2 — **class (i)** — missing coefficient evidence can satisfy D42.5 acceptance

**Location:** `B/accept_bench.R:73–85`.

F1–F5 OLS evidence is checked only for length. Replacing every F1 `beta_ols` with `rep(NA_real_,20)` on successful rules still returned ACCEPTED. A1 PIPs are checked only if present: deleting `fit$pip` from the successful SuSiE record also returned ACCEPTED. Thus an output can lose required evidence yet receive the report's explicit D42.5 certification. The existing short-vector negative controls do not exercise these holes.

**Concrete fix:** for successful/warning rules, require numeric, finite p-vectors for both coefficient versions, and require the appropriate zero-outside-support contract; retain the frozen runner's permitted NA/audit evidence for failed rules. Require PIPs for successful A1 fits, numeric length p, finite and in [0,1]; specify the evidence contract per method rather than testing presence opportunistically. Add all-NA OLS and deleted-PIP negative controls, alongside legitimate whole-fit/selected-rule failure positives. No changes to frozen r2 fitting code are needed.

### I3 — **class (i)** — case labels do not bind the accepted record to its input, scale or seeds

**Location:** `B/accept_bench.R:41–64`, especially lines 62–63.

Only method/case labels and `method_seed = data_seed + 4e6` are checked. The data seed is not independently derived from the dataset ID; fold seed, scale_key/scale, run ID, and consumed-input/X/Y/fold hashes are not checked against an authoritative source. A saved-record control changed every row to data_seed 1, method_seed 4000001, scale_key c050/scale .5 in the c100 directory, and a zero Y hash. All eight records passed. This is a wrong scientific record accepted under a correct-looking case label, even though the frozen runner itself correctly validates inputs at execution time.

**Concrete fix:** require the sealed inputs manifest (or an explicitly hash-bound inputs-only acceptance reference) at laptop acceptance, pass it in JOB.md §5 step 7, and compare the complete required identity fields with the list, directory/run ID and manifest. Derive p/scenario/replicate and production seeds independently using the frozen CLI formulas at `code/bench_lowp/run_bench_case.R:70–85`; select the Y hash for the requested scale. Require these fields to exist and be nonmissing, and cross-check the record's input hashes and row identity. Add independently mutated seed, fold seed, scale, run ID and input-hash controls. This needs no truth access.

### I4 — **class (i)** — empty provenance and unanchored source fingerprints pass

**Location:** `B/accept_bench.R:87–104`, especially lines 92–97 and 102–104.

The package loop permits a missing/empty provenance list. The source fingerprint is only compared between records: NULL fingerprints disappear, and a single common but wrong fingerprint is accepted. Removing both `environment$package_provenance` and `code$source_sha256` from every method record returned ACCEPTED, reporting an empty fingerprint. Package versions are not checked here, and any package can use a path shaped as `.../R/library` regardless of whether it is base/recommended. This falls short of the claimed source/library provenance gate and can accept records from another code/library environment.

**Concrete fix:** require complete provenance structures and required packages, validate the frozen pinned versions (including A3's dependency pins), and allow R's own library only for an explicit base/recommended package set. Require a nonmissing SHA-256 fingerprint in both rows and record code metadata, and anchor it to the supplied frozen r2 code by reproducing the runner's source fingerprint algorithm at CLI lines 87–89. Check the supplied code against the r2 manifest. Add empty provenance, missing/common-wrong fingerprint, wrong package version and non-base-in-R-library negatives. Retain the existing genuine/pinned-fixture positives.

### II1 — **class (ii)** — corrupted completed method units need an explicit recovery procedure

**Location:** `B/stale_lib.sh:10`, `B/make_resubmit.sh:57–64`, and frozen `code/bench_lowp/run_bench_case.R:124–136`; documentation gap at `B/JOB.md:98–105` (§14).

A method with `.done` present but a missing/corrupt companion is invalid to `bench_verify`, yet `clear_stale.sh` deliberately skips its method files because `.done` exists. Resubmission can list the case, but CLI resume refuses the completed corrupt unit. It halts safely; blindly retrying spends the remaining permitted start without repairing anything. This is distinct from interrupted uncommitted units, which the current stale handler correctly handles.

**Concrete fix / exact manual resolution to add to JOB.md §14:** after complete terminal accounting and before generating another round, inspect the reported invalid method and preserve its four exact paths (`M.rds`, `M.csv`, `M.sha256`, `M.done`), hashes and diagnostic in a fresh `LOG_RUN/cleanup/<UTC>/<case>/` archive. Obtain HQ's determination whether it is recoverable storage/transfer damage or a scientific exception. For an HQ-approved refit, move only the existing files of that one invalid method into that archive; leave every other method and every ledger/start record untouched. Only if the existing ledger permits another attempt, generate a fresh `rN` with `make_resubmit.sh`, inspect bench versus benchretry routing, and submit once; the CLI resumes intact methods. If a doubled-time attempt already occurred or there are two starts, retain an exception for HQ and do not reset the ledger or bypass the cap. Reconcile again before closing. Do not use this procedure on the already-running PROD_L stage. A preflight diagnostic preventing an unrepaired relaunch is optional; documentation suffices under D53 for this safe halt.

## Checks and accepted design choices

- Read the specified decisions, bundle designs/operating documentation, scripts, test sources/evidence, relevant BENCH-FIX release records, frozen CLI/config/helpers/adaptations, sizing, OPS guard/transfer implementation and pilot benchmark launcher. Historical source-review acceptance is preserved; this is deployment/acceptance review, not another numerical method audit.
- Independently rehashed all 34 frozen r2 members: 34 match, no mismatch. Manifest SHA-256 is `85a182488450e04ac960810b0c496e05e2c951aebf0b85dd9cff34f2bd07a6b7`. Staging normalization preserves `(hash,path)` pairs, retains and anchors the original manifest, and frozen checks run during staging, submission, verification and fitting. The copied generic frozen checker still permits its inherited compile-cache exclusion; this bundle does not generate such a cache and no deviation was observed.
- `make_lists.py --check` independently passed: 2,400 unique cases, 96 tasks of 25, both scales. Deadline/timeout accounting is coherent. CLI 2 is committed failed rules, not a timeout or infrastructure retry; 124/137 route to the once-only 1,200-second benchretry. Valid completed methods are skipped by the frozen CLI with input/source/environment identity checks.
- Stale detection matches actual CLI `tempfile('.<basename>')` names, method lock directories and partial method units. Archival preserves them in logs. Close/pull/verify/delete uses hash-bound inventories and preserves acknowledged exceptions. No truth is selected by the stage copy operations; the stage and submit path checks reject truth/holdout names, and the CLI does not consume truth. This appropriately replaces a truth lock for this bundle.
- R 4.5.2 and pinned package checks occur in the main verify gate; fits use the pinned library argument, package-closure location checks and single-thread limits. Source/runtime records are saved. I4 concerns downstream acceptance completeness, not evidence that deployed fits currently use the wrong library.
- PROD_L fitting-lane serialization, potential-CPU admission across both retry pieces and all other fb31 work, withH throttles, and the documented retune/confirmation/drain sequence are consistent with D47/D49/D50. Pilot-based 38.3/40.6 billed-core-hour sizing and the separately disclosed F3 sensitivity are coherent estimates, not live NOTS certification. D54.3 ABESS deferral is explicitly disclosed in design, JOB, reconcile and acceptance.
- Supplied `B/tests/SUMMARY_bench_final2.txt` has 14 successful suites totaling 1,099 checks, zero failures. This is inspected supplied evidence, not an independent full-suite rerun. Live evidence demonstrates three real cases, a new-job resume and same-job refusal; the original log's failed acceptance predates the registry change. The later positive evidence is ACCEPTED 24/24 with local provenance skipped, and the later negative CSV rejects the two stated mutations.
- Independently ran `bash -n` on all 32 bundle/test shell and sbatch files: no syntax failures. No Python bytecode was written to the campaign.
- Saved-record checks used one R process at a time with no fits. `check_accept.R` reads the existing live p0020/S1/r001/c100 records, constructs a common pinned-provenance fixture, then makes six separate content mutations. The baseline and all six defective variants returned exit 0, ACCEPTED 8/8. Each has copied markers, rewritten CSV and recomputed RDS/CSV sidecars; `check_verify.py` independently returned True for baseline and every defective case. Thus checksum verification does not close I1–I4. Outputs and scripts remain in the review-local directory. These synthetic provenance fixtures are tests, not claims of an actual R 4.5.2 run.

## PROD_L post-READY changes

**D57 accepted:** `PL/prodl.env` separates 110 MB pre-stage from 10 MB post-extraction growth; `PL/submit_prodl.sh:26–27` uses the growth value. Bench separates 75/5 MB and records stage_on_disk_kb. Both guard checkers are identical and compute their home probe from the parsed guard limit; 9.70 requires the corresponding allowed ceiling and HQ authorization. The regression reproduces the old double-count refusal, admits the corrected path and rejects insufficient growth headroom. Independent `PL/tests/test_stage_guard.sh`: **24 passed, 0 failed, exit 0**.

**Logs-close change accepted:** the stale scan remains on result pieces and is omitted on the evidence/logs folder. Archived files and hidden ledger temporaries are included in the logs manifest, rather than silently discarded. Independent `PL/tests/test_manifests.sh`: **136 passed, 0 failed, exit 0**, including D5701–D5709. PL JOB.md §14 supplies a bounded manual manifest/pull workaround for the already-staged old copy; cleanup does not require logs.CLOSED. Preserve that running stage unchanged.

The requested `PL/tests/SUMMARY_pl_postready1.txt` was absent when checked, so the three requested fallback suites were run sequentially from a copied bundle in the review-local directory. Only the `prodl_tests` path literal was changed in copied test files. Independent `PL/tests/test_driver.sh`: **324 passed, 0 failed, exit 0**. All three required fallback suites passed (484 checks total).

## Release disposition

Fix I1–I4 with targeted saved-record regression tests, document II1, and use round 2 for the final integrated review. Keep the frozen r2 tree unchanged. The verdict does not revoke PROD_L's prior READY status or authorize any edit to run `20261030T1811Z_lowp_prodL`. Real NOTS module availability, quota, scheduling, transfer and execution remain OPS checks; none was contacted in this review.

## Final verification and SHA-256 inventory

Independent fallback launch commands (PowerShell invocation of Git Bash; one suite at a time, no live scheduler commands):

```text
& 'C:/Program Files/Git/bin/bash.exe' '<PC_TEMP_PATH>' '<PC_TEMP_PATH>'
& 'C:/Program Files/Git/bin/bash.exe' '<PC_TEMP_PATH>' '<PC_TEMP_PATH>'
& 'C:/Program Files/Git/bin/bash.exe' '<PC_TEMP_PATH>' '<PC_TEMP_PATH>'
& 'C:/Program Files/R/R-4.4.1/bin/Rscript.exe' '<PC_TEMP_PATH>'
py -3 -B <PC_TEMP_PATH> <CAMP>/jobs/PROD_L_BENCH
```

The shell suites' terminal outputs were inspected directly; their per-scenario logs, receipts and fixtures remain in the three work directories. R variant stdout/stderr and acceptance CSV/Markdown reports are retained beside the scripts. R startup locale warnings did not change exit statuses. An initial inline Python verifier command lost string quotes in Windows argument handling and failed with NameError; the saved `check_verify.py` replaced it and passed. No delivery defect is inferred from that reviewer-command failure.

The following hashes bind the reviewed campaign files, the complete verified frozen r2 tree (including implementation members whose scientific review is inherited), and the principal independent saved-record evidence. Campaign paths are relative to CAMP; `TEMP/` denotes the review-local directory. Bytecode caches are excluded. This report's own final digest is supplied with delivery, rather than included recursively in its contents.


```text
73f3000f52fd1c67d9e3a57dbea402290b12ede615148d61fc88b03fbd45b7a8  code/bench_lowp/ADAPTATIONS.md
bf6d3b702a25ba5e05c98f71c21d2da9858dbd67776c8b5993d098ce3344c10a  code/bench_lowp/R/common.R
5bad82cbb2086b905f31b7353a98f13ee10abe4b05a29cf6efcdb26429af7848  code/bench_lowp/R/config_lowp.R
93331f6530c33ee13ce886381c6c04f31661223c463dd1a333434332fd7ad223  code/bench_lowp/R/methods/fit_A1_susie.R
cc8406d21860c24242153ed1efba0d38300bae512ff3ff1bca73828235a9828f  code/bench_lowp/R/methods/fit_A2_ssl.R
9bea247710d4b98234f96dc03dd434bcf74cc675394055e156e7714e4ba79048  code/bench_lowp/R/methods/fit_A3_horseshoe.R
0aa6d65baa7cb8983f70de1e1dab36b80b6f3cfa5e655e9abd4d680b798b77f3  code/bench_lowp/R/methods/fit_F1_lasso.R
04ba82821ac5987087237f217578370f51e8140c31872e8e6dc939703d1bf803  code/bench_lowp/R/methods/fit_F2_enet.R
e12afd04ea6be5468cba1317f08216f6eb484174db192e27defa4ed9e37ef233  code/bench_lowp/R/methods/fit_F3_alasso.R
c6072dc588a8c442fa333f8b92a120d29a2d0580ef74ee428986147a2f2b06e6  code/bench_lowp/R/methods/fit_F4_mcp.R
5edfa0127d0914b6955cfdd7f75535ff441bd855bdeb752309203ffc59bbf7b1  code/bench_lowp/R/methods/fit_F5_abess.R
cd544cb7c3518eb20b6c28ca903812c26392a45ebd35ae367d200db697bc05da  code/bench_lowp/R/methods/glmnet_helpers_F1.R
d2ffc988506171c745e0642041102ab4393b267a085d355bad1998d21db0f3a4  code/bench_lowp/R/methods/glmnet_helpers_F2.R
0d6cd4a894bb1daefeb67b8ad725be24d205ad297b65aef99d285cd3e1e4f4de  code/bench_lowp/R/methods/glmnet_helpers_F3.R
830edf4aee80cddd9fbf4caa3993277c0b91470f2e1ea90b01bd5b519711d2f0  code/bench_lowp/R/production_helpers/common_A1.R
fe7d661c6ebcbf076bebd90994d102ae210b7b7d959d7b866b24012eecb5c3d4  code/bench_lowp/R/production_helpers/common_A2.R
f823725e364b91009dee1e7fc0d945684c9cd5d390f9ea496bd0c291b8b0ac04  code/bench_lowp/R/production_helpers/common_A3.R
4d4e6f65c50b0b0a3f762f9878eb1264f00a7f1d85800c3d3f8e63a3f3904a49  code/bench_lowp/R/production_helpers/common_F1.R
89d83b3eeb0242e469751a228cc3ffbfcfbf5e57b3725bf287c985cd3b92bf2f  code/bench_lowp/R/production_helpers/common_F2.R
1ff848871f850ce51c8e14883c900866d691d7159fef697f3fe0c637c2c34efe  code/bench_lowp/R/production_helpers/common_F3.R
2f1471dde45f61c1984c1d2c60ad0094ebbd5ca41c1379c3bffafbd5569b60cd  code/bench_lowp/R/production_helpers/common_F4.R
f7c9904f93b99354db45fbb9ec6358e7392278cefdb69ad9444f961610da439c  code/bench_lowp/R/production_helpers/common_F5.R
97f2c47a0d414512f36af42c7886113671d1ce657f0518c78dbeffdb547126aa  code/bench_lowp/R/SOURCES_SHA256.txt
fa2daebe93934588352a0ef4be4ef387231843f19099b660a5bd7c72eb665c3f  code/bench_lowp/README.md
24b99c26437b6c2d356971393edfa9e0b2c9cedbc3e08c6270e19dda2e3b9711  code/bench_lowp/run_bench_case.R
b6bbdbc2736c6e6ff96665ee9db620478193c0a8b5c72ef0e1b5f065ef6ba5c6  code/bench_lowp/smoke/check_determinism.R
3ac7453665f6b5958cd2322d741d9be15377bc977cfe4732afcff06f203fcb4c  code/bench_lowp/smoke/derived_checks.R
ec7de83d97fe4f279b1f3b17c29f0156be67dee2d869df9dc5bb2434a77a1b87  code/bench_lowp/smoke/make_smoke_data.R
935aa7c21432e8438f299310c5b0de589d4d36b71fb0bb4443e4a58c6ed4abc7  code/bench_lowp/smoke/measure_memory.ps1
9a37dc139104dde0dbab1abfc1fbc6317c10cebfe96befe86955f79d85a93425  code/bench_lowp/smoke/run_smoke.R
c849636dcb277f2fd7af85f1fe7c53c34d439c7184196ecbfa3d1cd00fa481cd  code/bench_lowp/smoke/SMOKE_REPORT.md
4ca994b5f474a85f4fd3691ad4a3e8528b5edc76073849b3c841074022c2b631  code/bench_lowp/smoke/smoke3.R
a862531f827081bf190b09c5c110cddddb575f8a6e9db0011bc16b7b5f64efbf  code/bench_lowp/smoke/test_derived_conditions.R
99c0aaaa1f8d4eec5693fc05de0bf4e7906282c947ff5b45e1b4e242f9cbecb3  code/bench_lowp/smoke/validate_smoke.R
85a182488450e04ac960810b0c496e05e2c951aebf0b85dd9cff34f2bd07a6b7  code/bench_v2/lowp_port/BENCH_LOWP_MANIFEST_SHA256_r2.txt
52129de4f4f32e99e09d99c8d105a6fa949010b12c2fb7fc7431aad581932e1f  code/bench_v2/lowp_port/LOWP_TEST_REPORT.md
30ad2489fa86f1e1f39ad8b2373115e541e623fde7098656fa0a7640d2b24175  code/bench_v2/review/SOL_NARROW_CHECK_R2.md
024dba065683104548afa285097fb5c251e2b284aab190ecff20b8a4a2367842  code/bench_v2/review/SOL_REVIEW_2.md
409e276ddb59b1d24cfa7c514197a5ee3a4905db1f5203df8c4c3449b4c75064  code/lowp/pilot/slurm/s3_bench.sbatch
cf5ba3574e145eaeb9e592ce29960bcf7edb9b6d9995a89fb95f3812cd7a8af8  DECISIONS.md
6d6926a66b0852f676c98ce6d408d70a21ed837021757425a647096c2941be20  jobs/PROD_L/DESIGN.md
2bb8f76977ac04f759e8c780573e4bac1b74efecb093b47e17025839240ec071  jobs/PROD_L/guard_check.sh
e69edd640b54572cc329b9d7a8a4e3f7a7b6cd101d4168e3faa1b24231829800  jobs/PROD_L/JOB.md
807c468163245647344472f3d7d18000959cb227ce096f1cf637dc697c7c1113  jobs/PROD_L/make_manifests.sh
5194ca9c6611b1e1ec7a7d0a8fa78ddb77dc046abb1637f05abb5384bc0cda64  jobs/PROD_L/prodl.env
5152ff76348e0844e2ad3b932c7bacec7b0a34d988d63f5dee9e774ae0292974  jobs/PROD_L/submit_prodl.sh
5adff612095ebc95f1097745be88dcb21b7def8ead6b406d299993a51b177cd6  jobs/PROD_L/tests/lib.sh
160ef0216c17ae50ec23c43ee59e2cc9f7ac5927b3734ccf7b66510fd2e16872  jobs/PROD_L/tests/test_driver.sh
8cd5a50058064ecbdec1a7e32b7211a0d8e71bcc95eab1bc21b3277e450ebcce  jobs/PROD_L/tests/test_manifests.sh
6291e11af8061367e52786b80ea0e3b5d17deb32f12a1e257ba24ab0504a6d2f  jobs/PROD_L/tests/test_stage_guard.sh
f498e45b2656142f1812157baf56d42a3c332d468d75fa516ad81f174f826d07  jobs/PROD_L/tests/vec_check.py
ffa790f5326ba94d872a933386b4283c4accfd99e68efc1ae464c917e6ca9227  jobs/PROD_L_BENCH/accept_bench.R
bb7551d5a4b6a64a62c91f2f1dfc153dfd9d7a3e7adaaf4871721746d569886f  jobs/PROD_L_BENCH/batch_runner.sh
4cddd62bef1d702bc0300181aec4164dc6c028108cfb79c89accce4aed855582  jobs/PROD_L_BENCH/bench.env
f941f92a4c2681b69c8a2a959cd4b66cd3b1840135462990f4d68f8650537feb  jobs/PROD_L_BENCH/bench_verify.py
3feb24c6403e1834e7c8501a9873c298da3dc30a5c045bc06e609c7df6614683  jobs/PROD_L_BENCH/BUILD_NOTES.md
29a7dfda13abfffff239aff3c48169339d27bb4d2c6f5293907e3bf9867e58da  jobs/PROD_L_BENCH/ceiling_check.py
e1c9d419152f1a1867428e1d2fac283d9a2f72ac1fb5fe6582c6630396bd0899  jobs/PROD_L_BENCH/cleanup_bench.sh
8d99a9ad4646e78bfd99f74c722fb55d75e05e94eae03a9c1bbaaaf10666d6b9  jobs/PROD_L_BENCH/clear_stale.sh
d071897f3fbb6e5688d8ad0715a17c10ab18af64325b2ed91aa0d990589423b1  jobs/PROD_L_BENCH/CORE_HOURS.md
3f043909f9d0d1ad354ad9ec5948d63fd0cf7b05f48152bb1c4747252c395b0e  jobs/PROD_L_BENCH/DESIGN.md
01402fb089e3e32568588febfbbeb70052cf5cfbb43f39c3a58b69fce2d75fcc  jobs/PROD_L_BENCH/final_accounting.sh
055da40ac52341763e32bb5428809e1dc7a7c67a1f720f02608b2d680ff10340  jobs/PROD_L_BENCH/frozen_check.sh
2bb8f76977ac04f759e8c780573e4bac1b74efecb093b47e17025839240ec071  jobs/PROD_L_BENCH/guard_check.sh
c2a08732c475229103c0036ddf200bc7b7a7051b3191f902dae4760c79da39fb  jobs/PROD_L_BENCH/JOB.md
1960075e2b74eb2941fa1d93e5da1b332e7f15e4a10eb21be831a6101ebd0cd0  jobs/PROD_L_BENCH/lists/units.tsv
5d48c95f0c00da92c26d7c6b85b2a9bb9588e4859cc30a862b73cbe0b28392b8  jobs/PROD_L_BENCH/make_manifests.sh
a3b0f5ab62e1460dfdef1c919352a278648322c82a90c0b4f4d3c0f75b8c7642  jobs/PROD_L_BENCH/make_resubmit.sh
d6a9da96de11013ae3e04d6da33e1875c29bbebd70f94ce24d1408e34154b84e  jobs/PROD_L_BENCH/PROGRESS.md
0be94b55d49b348405d65a7be933d7b9341413366fb305b4e4831b399cac64ad  jobs/PROD_L_BENCH/R/bench_env_probe.R
6ebfeff780c39b3a0a8b01cb4f2468942075785b366369f04933eb7f57f2620b  jobs/PROD_L_BENCH/R/prodl_inputs_check.R
c661c3ce6d5bb9f3be38fe46bde1fa74c809cd23936090da262cdbb13236802a  jobs/PROD_L_BENCH/reconcile_bench.py
d5856a22c086466c137534393cfd65fdd91ebcacaf08f4f8b0f2034aada9e41b  jobs/PROD_L_BENCH/retune_throttle.sh
6cf04e754c6ae3f84d77f6c3abf15d9dac46ce1c2838910c966563994f1aac83  jobs/PROD_L_BENCH/REUSE.md
9f6cb68d3ca30e1897c1eed1fdae92c28736c1a3c27397c97e911c758b5d2c21  jobs/PROD_L_BENCH/slurm/common.sh
9518307f36a4e76d42ab3e3b13a1daffc2f2db34438ddc1561331440cec0b4f0  jobs/PROD_L_BENCH/slurm/s0_verify.sbatch
4d171b1399e1e3a5649dc1b37eccd08b7c1b954c790a3ab248b8795658639924  jobs/PROD_L_BENCH/slurm/s1_bench.sbatch
0b06163ca043deada4f832c111d0577915a8439394877cd566c6ef6299a1c666  jobs/PROD_L_BENCH/slurm/s2_benchretry.sbatch
21cd4e79409f78ab87bc55faba114837a2b430b0ea870d84545c8e21daa30f22  jobs/PROD_L_BENCH/slurm/s9_collect.sbatch
6f67a356d5890dc3005b4b005848656aa40aeaf53a289d967368bbe4efc67252  jobs/PROD_L_BENCH/stage_local.sh
0e0668b8f6ca12cc4fc07ff6f34bd6e0af1adad255929bf895e7e8fc37da6a10  jobs/PROD_L_BENCH/stale_lib.sh
be073415b13209cd9535641d46028469606b03dfbbf19c99c45ab0dc85973a57  jobs/PROD_L_BENCH/submit_bench.sh
db5888e9363f0213654125449037a4feaa204ecdacb04d0ba0def3708a415fc5  jobs/PROD_L_BENCH/tests/lib.sh
f4ff54906d44d84ef497d7010a2af3b56bf7f965f243f5fe330047162b269cdd  jobs/PROD_L_BENCH/tests/live/accept_live_negative.csv
9f3e6ea5e11175c8de809e12040ed4c84ab10898d49827e84e412e489fe003fd  jobs/PROD_L_BENCH/tests/live/ACCEPT_live_positive.md
71796aa2981a67bc3314b3036a01a2777166931348c00f5f8d169dd4b02d7913  jobs/PROD_L_BENCH/tests/live/live_bench.sh
6df4c422576a41e81d8c21dc9df9dec48bd725e984b350c30add88f98cdfb340  jobs/PROD_L_BENCH/tests/live/live_bench_run1.out
e49b38f1aefcf2dacd589b19ab0aa6dfe29dec1e1189c8939901bbd85f10bc35  jobs/PROD_L_BENCH/tests/make_accept_fixture.R
73fb4ef4a9aa8557238eea001ce8ae2c8f8799d4ab01b20894ce4ad39bfd0559  jobs/PROD_L_BENCH/tests/run_all.sh
2d4de92232c115986060c3cea797e151e3942adc5c6a7733357ca8d8c169a396  jobs/PROD_L_BENCH/tests/SUMMARY_bench_final2.txt
7e08294330134cc6b3edc61a39bc9b0355e268d8232fbd1d18df6d7c85ecb0fe  jobs/PROD_L_BENCH/tests/test_accept.sh
429b3ed3fc24c460c7cbc4d3c3248adbc83ffc7673859f3146a149a6917ecd32  jobs/PROD_L_BENCH/tests/test_ceiling.py
b7d7b84075771445b335fa6c196bb02273cf37d889330886a24835f24597943a  jobs/PROD_L_BENCH/tests/test_cleanup.sh
ea4d28ae2daa6ab216d6fb0ae81c4c25262068127d60a1dda65354ba19c2bca6  jobs/PROD_L_BENCH/tests/test_collect.sh
9473bf7779cb87535928d23c7f822d92aa347c296c1b45f0a4744701b262055a  jobs/PROD_L_BENCH/tests/test_deadline.sh
94ce1f8c3836ea22b659d81c0ce0ea6e189f151ad108e3ca502104dbb00e147a  jobs/PROD_L_BENCH/tests/test_driver.sh
07e126e1c7703cd2b2196e90bfe13f89446530f328e8e612c83577b5612d89c6  jobs/PROD_L_BENCH/tests/test_jobmd.sh
9c4fe177fd09da6656f20164f58ef637c9456b22330b2589089d566e821e99c8  jobs/PROD_L_BENCH/tests/test_lists.py
b1c5387f414996dfada578cb97996d8ec24019cb19e5aac382706e9174443d2d  jobs/PROD_L_BENCH/tests/test_manifests.sh
8b43803a0bb348da81d67596d97a3623d9aa76ee17b44304a39483577dd0a619  jobs/PROD_L_BENCH/tests/test_reconcile.py
512c4811de25f869dabad283f4193f2a1a8db5f9672eea01e6c13e2f66b17f9e  jobs/PROD_L_BENCH/tests/test_resubmit.sh
c4827a8f4de5256e7fb6931fa3657e7200b59981822f870753f345bb2aa90bc0  jobs/PROD_L_BENCH/tests/test_retune.sh
7c021ff8fa9cd74473102ba202e3d3a899f7e200f450b96e9d404a9eff9d1fdf  jobs/PROD_L_BENCH/tests/test_stage_guard.sh
6a87f1fccaf2b656b8495d31b352f4e5e345ceb416ec0bbd70d23cf572f007ab  jobs/PROD_L_BENCH/tests/test_waiter.sh
fcc6eb9be284917c70e789b85d1ad4ddf03eb42e43057110c661d398a4b2cd26  jobs/PROD_L_BENCH/tests/TESTS.md
359be6a7e565cdb51553fd9f6df4dfb42889efb0341b1c177e1c9ee24ec2a956  jobs/PROD_L_BENCH/tests/vec_check.py
08e727d14f17426a37803a9a9287a2111f0cd20788a86b5207853cde1d166f52  jobs/PROD_L_BENCH/tools/make_lists.py
cce65d85101c05392da479c8796ea82a9664c0facc5a9bb78a1ae752614093e6  jobs/PROD_L_BENCH/waiter.sh
29c1d07cb9e1ddfa51c74139a8ee0c0ed6d9e8db46433da6d22092023350d897  ops/guard.sh
9bb0da4fe4c2d38d0568526b876c742457057114eae729149643453d25c279b5  ops/PROD_L_SIZING_20261030.md
f46fe38edcc35b8d0c266a19daf44c6fa8ee1c9e1e6766163c76806e04ae8827  ops/transfer/nots_pull.py
13cd8bf68e4de3f909ba8573b9bbae4f3384907a73d437ee8624ccd3093851a0  TEMP/accept_baseline/accept_bench.csv
f6195953303458f4bc0d8d4b829cdaddbf11d7349b4f44aafb6877abccb90360  TEMP/accept_baseline/ACCEPT_BENCH.md
13cd8bf68e4de3f909ba8573b9bbae4f3384907a73d437ee8624ccd3093851a0  TEMP/accept_missing_derived/accept_bench.csv
f6195953303458f4bc0d8d4b829cdaddbf11d7349b4f44aafb6877abccb90360  TEMP/accept_missing_derived/ACCEPT_BENCH.md
13cd8bf68e4de3f909ba8573b9bbae4f3384907a73d437ee8624ccd3093851a0  TEMP/accept_missing_ols/accept_bench.csv
f6195953303458f4bc0d8d4b829cdaddbf11d7349b4f44aafb6877abccb90360  TEMP/accept_missing_ols/ACCEPT_BENCH.md
13cd8bf68e4de3f909ba8573b9bbae4f3384907a73d437ee8624ccd3093851a0  TEMP/accept_missing_pip/accept_bench.csv
f6195953303458f4bc0d8d4b829cdaddbf11d7349b4f44aafb6877abccb90360  TEMP/accept_missing_pip/ACCEPT_BENCH.md
13cd8bf68e4de3f909ba8573b9bbae4f3384907a73d437ee8624ccd3093851a0  TEMP/accept_missing_provenance/accept_bench.csv
d4a5b521d3ea42fa8e8935861570a0d7798feca8864b29dca327e8acba4ad574  TEMP/accept_missing_provenance/ACCEPT_BENCH.md
13cd8bf68e4de3f909ba8573b9bbae4f3384907a73d437ee8624ccd3093851a0  TEMP/accept_wrong_identity/accept_bench.csv
f6195953303458f4bc0d8d4b829cdaddbf11d7349b4f44aafb6877abccb90360  TEMP/accept_wrong_identity/ACCEPT_BENCH.md
13cd8bf68e4de3f909ba8573b9bbae4f3384907a73d437ee8624ccd3093851a0  TEMP/accept_wrong_role/accept_bench.csv
f6195953303458f4bc0d8d4b829cdaddbf11d7349b4f44aafb6877abccb90360  TEMP/accept_wrong_role/ACCEPT_BENCH.md
b3aad99a991f98252f3a0842635009f1fbec82b901a63d11a0168dadc69467cb  TEMP/baseline.err
3de41b3a1bc24edeb9cac7b830a9196f85529f69446867347f4294d176da24be  TEMP/baseline.out
63de08d6f757b28eeb660dac628314c58e9ad91b15a3082f7c3c7694271819cb  TEMP/check_accept.R
4f6e74c880000574c094ae0be43b1b4a1993d54d64b13a6755ff94d72177ff67  TEMP/check_verify.py
b3aad99a991f98252f3a0842635009f1fbec82b901a63d11a0168dadc69467cb  TEMP/missing_derived.err
3de41b3a1bc24edeb9cac7b830a9196f85529f69446867347f4294d176da24be  TEMP/missing_derived.out
b3aad99a991f98252f3a0842635009f1fbec82b901a63d11a0168dadc69467cb  TEMP/missing_ols.err
3de41b3a1bc24edeb9cac7b830a9196f85529f69446867347f4294d176da24be  TEMP/missing_ols.out
b3aad99a991f98252f3a0842635009f1fbec82b901a63d11a0168dadc69467cb  TEMP/missing_pip.err
3de41b3a1bc24edeb9cac7b830a9196f85529f69446867347f4294d176da24be  TEMP/missing_pip.out
b3aad99a991f98252f3a0842635009f1fbec82b901a63d11a0168dadc69467cb  TEMP/missing_provenance.err
3de41b3a1bc24edeb9cac7b830a9196f85529f69446867347f4294d176da24be  TEMP/missing_provenance.out
b3aad99a991f98252f3a0842635009f1fbec82b901a63d11a0168dadc69467cb  TEMP/wrong_identity.err
3de41b3a1bc24edeb9cac7b830a9196f85529f69446867347f4294d176da24be  TEMP/wrong_identity.out
b3aad99a991f98252f3a0842635009f1fbec82b901a63d11a0168dadc69467cb  TEMP/wrong_role.err
3de41b3a1bc24edeb9cac7b830a9196f85529f69446867347f4294d176da24be  TEMP/wrong_role.out
ba761f529b848a030b7aee86497db78af450ae5b5a7a6f64ebca4f7ab611367b  TEMP/PROD_L/tests/lib.sh
6291e11af8061367e52786b80ea0e3b5d17deb32f12a1e257ba24ab0504a6d2f  TEMP/PROD_L/tests/test_stage_guard.sh
8cd5a50058064ecbdec1a7e32b7211a0d8e71bcc95eab1bc21b3277e450ebcce  TEMP/PROD_L/tests/test_manifests.sh
701c9be4aa9b04c709c27194ffdb6f7b73e7547d29ba8727b369f569072be162  TEMP/PROD_L/tests/test_driver.sh
f498e45b2656142f1812157baf56d42a3c332d468d75fa516ad81f174f826d07  TEMP/PROD_L/tests/vec_check.py
```
