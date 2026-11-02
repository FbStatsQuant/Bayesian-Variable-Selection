# Independent Sol review: PROD-L, round 1

**Verdict: REJECT. Do not stage this revision.** Three blocking findings concern truth-lock safety, missing P5 outcomes, and preservation of attempts under Slurm requeue. The remaining findings have concrete repairs below. This is a review of the bundle, not a rejection of the frozen sampler or the accepted pilot.

Reviewer: Sol 6.1, independent reviewer, 2026-10-30. Paths below are relative to `CAMP/jobs/PROD_L` unless prefixed `CAMP/`. Reviewed HQ decisions, the D49 answers, binding design, operational commands, all bundle scripts and test sources, build notes, accepted pilot references, sizing, and the real enumeration/SMC/P5 CLIs. No SSH, network, NOTS connection, fit, benchmark, or data regeneration was performed. Only this review is written in the campaign; offline test artifacts are under `<PC_TEMP_PATH>`.

## Findings

1. **Blocking — an invalid old job ID makes the all-wave unlock check fail open.** `slurm/s8_unlock.sbatch:21` gathers fitting IDs from every wave, but `slurm/s8_unlock.sbatch:24` converts any failed query containing `invalid job id` into an empty successful result. An old purged ID is not evidence that all other IDs are inactive; the branch even discards any active rows returned alongside that error. Offline injection of `7004_0|RUNNING` plus the invalid-ID diagnostic and exit 1 caused the real sbatch wrapper to call unlock and exit 0. This directly defeats the required all-wave check. **Fix:** query the user's full live queue successfully, filter it against every recorded fitting ID, and refuse on every query/parse error. Require complete terminal accounting evidence before opening the trees; do not infer inactivity from an error message. Use the same fail-closed terminal proof in `recover_truth.sh:17`, which currently uses queue absence alone. Add mixed old/new-ID, active earlier-wave, missing-accounting, and scheduler-error tests of the actual unlock wrapper; keep B2's never-locked hash verification.

2. **Blocking — a missing P5 rerun can disappear from acceptance and be closed permanently.** `reconcile_prodl.py:143` inspects a retry only if retry artifacts already exist, never reconciles the expected `RUN_HOME/p5/units.tsv` or `ledger/p5`, and `reconcile_prodl.py:180` returns success from primary completion alone. `make_manifests.sh:52` consequently permits closure with an eligible retry absent; it also has no machine-enforced proof that the required scan/P5 phase occurred. Offline fixture: a valid `resource_limit` primary, an expected P5 row, a P5 `.start` without `.end`, and a terminal NODE_FAIL job produced reconciliation **exit 0**, primary `done`, no P5 exception, and successful SMC closure. Subsequent P5 submission is forbidden by CLOSED. Additionally, `submit_prodl.sh:14` permits only one `p5` wave, `submit_prodl.sh:34` retires that name after launch, and `make_resubmit.sh:4` excludes P5: deferred or never-started P5 units have no supported resubmission path. The same fixed `p5scan` name prevents a retry of a failed scan or a separate final scan.

   **Fix:** persist a validated initial scan receipt and expected retry inventory; reconcile every expected P5 unit independently of primary completion, including no-artifact, deferred, killed, and invalid retry states. Before SMC/repeat closure require a final scan that validates binding to the primary, seed and doubled allocation using the frozen scanner, plus complete retry outcomes or explicitly acknowledged exceptions. Permit fresh scan phases and idempotent lists/waves for P5 units that never consumed an attempt. Preserve the one-attempt cap for started P5 units and report unsuccessful attempts explicitly rather than refitting them. Add interrupted/never-started P5 end-to-end tests; the retained live integration exercises no P5 fit.

3. **Blocking — automatic Slurm requeue overwrites attempt evidence and defeats the cap.** `submit_prodl.sh:88` does not specify `--no-requeue`; no wrapper checks `SLURM_RESTART_COUNT`. `batch_runner.sh:5` uses only job/task IDs for names, then `batch_runner.sh:49` and `batch_runner.sh:89` replace existing start/end records. A requeued task keeps those IDs. Two offline invocations with the same job/task and restart counts 0/1 left **one** `.start`; the first end record (`rc=1`) was replaced by the second (`rc=2`). `make_resubmit.sh:38` therefore counts one attempt after two executions. An interrupted SMC can instead encounter its stale adapter lock, consume an untracked extra failure, and exhaust the intended recovery allowance. Whether NOTS currently requeues a particular failure is unverified; this bundle must not depend on an unstated cluster default. **Fix:** explicitly submit these jobs with `--no-requeue` and reject unexpected nonzero restart counts before any ledger/attempt mutation. Alternatively, implement immutable restart-aware attempt IDs, stale-lock recovery, and cumulative caps. Add the same-ID restart negative control and preserve the first attempt's logs, inventory and ledger byte-for-byte.

4. **Should-fix — collection runs the guard after an unsuccessful unlock.** `submit_prodl.sh:114` releases collection with `afterany` on unlock. `slurm/s9_collect.sbatch:22` checks only a partial list of nonterminal accounting states; `slurm/s9_collect.sbatch:23` calls the home-scanning guard without checking open truth modes or `WAVE_UNLOCK_VERIFIED`. Failed/cancelled/timed-out unlock jobs are terminal and can leave mode-000 trees. Offline injection of terminal fits and a FAILED unlock still called the guard and returned success. **Fix:** require this wave's verified unlock receipt and verified open trees before any guard/du; otherwise retain accounting only, exit with a clear recovery instruction, and leave the guard for after verified recovery. Test failed, cancelled and never-locked finalizers.

5. **Should-fix — stale cleanup does not recognize the real enumerator's temporary filenames.** `clear_stale.sh:19` matches `*.tmp.*` and `*.tmp`, whereas `CAMP/code/lowp/enum/run_enum_dataset.R:157` creates `EXACT.rds.tmp<PID>`, `EXACT.sha256.tmp<PID>` and `.done.tmp<PID>`. `make_resubmit.sh:40` refuses these because it matches any `.tmp`, and `make_manifests.sh:43` also refuses them, but the advertised remedy leaves them untouched. An offline `EXACT.rds.tmp4242` survived `clear_stale.sh --yes` with exit 0. This is a normal hard-kill/NODE_FAIL recovery case, not an invented filename. **Fix:** recognize the actual CLI temporary-name contracts (including hidden `.done.tmp<PID>`), move them to the cleanup evidence after the terminal gate, and test these names alongside adapter `*.tmp.<PID>` and `.lock` directories. Do not alter the frozen CLIs to fit the cleanup glob.

6. **Should-fix — completion verification accepts sidecars that do not describe the required output.** `reconcile_prodl.py:29` verifies whatever basenames a sidecar happens to list, without requiring exactly `EXACT.rds`, or exactly the SMC prefix's `.rds` and `.csv`; `make_resubmit.sh:36` similarly trusts unrestricted `sha256sum -c`. The existence of any `.done` is enough. An offline call to the original verifier returned `(True, 'verified')` for `EXACT.done` plus a checksum of `unrelated.bin`, with **no EXACT.rds**. CSV exceptions at `reconcile_prodl.py:134` and unexpected folders at `reconcile_prodl.py:157` also do not affect the success return. **Fix:** require the exact per-prefix file set, no duplicate/escaping names, required nonempty outputs and valid completion-marker format; fail acceptance on malformed CSVs and unexplained output exceptions. Preserve the distinction between an operationally committed scientific failure and missing/malformed data. Share this validation between reconciliation and resubmission; add missing-RDS, one-line SMC sidecar, duplicate filename, malformed marker/CSV and unexpected-output controls.

7. **Should-fix — reconciliation forgets CLOSED pieces once their scratch folders are pulled.** `reconcile_prodl.py:121` always reads scratch and never uses the authoritative closing inventories described in `JOB.md:41`. Every close reruns it over all pieces (`make_manifests.sh:49`), overwriting `inventory_final` as earlier folders leave scratch. Offline closure followed by moving the result to a simulated downloaded tree changed the unit from `done` to `not_run` and reconciliation from exit 0 to 1 despite its CLOSED marker and saved inventory. Thus the mandated continuous pull flow cannot produce a trustworthy final combined inventory; the last snapshot can report previously completed pieces missing. **Fix:** distinguish closed/archived pieces and verify/load their immutable inventory plus manifest identity/transfer evidence, while verifying live pieces against scratch. Preserve the original closing inventory, include its hash in CLOSED, and produce one final reconciled inventory covering all 15,600 units. Test close → pull/delete → later wave → final reconciliation.

8. **Should-fix — OPS cannot execute the documented sequence literally.** There are three concrete command-order problems:

   - `JOB.md:42` passes the relative path `results/<STAMP>_lowp_<piece>` to `nots_pull.py`; `JOB.md:43` does the same for `logs/<RID>`. `CAMP/ops/transfer/nots_pull.py:125` requires an absolute NOTS path and refuses these before transfer. **Fix:** use quoted `/scratch/fb31/New_Campaign/results/${STAMP}_lowp_${piece}` and `/scratch/fb31/New_Campaign/logs/${STAMP}_lowp_prodL`. Give an explicit, approved command for fetching the individual home summary directories/files as well; the brace expression in step 8 is not a transfer command and includes optional paths that may not exist.
   - `JOB.md:35` uses a waiter that deliberately exits 3 immediately on one failed row. That is **not** proof that main/all jobs are terminal or truth is unlocked. Step 4 assumes both. **Fix:** document separate early-failure triage and all-jobs-terminal/unlock checks, including repeated observation after a failure, before reconciliation, stale cleanup or later submissions. Never treat an early failure as terminal completion of the wave.
   - `JOB.md:37` says “for each incomplete piece” create and submit `r1`. After the first piece, `launch/r1` exists and `submit_prodl.sh:34` refuses the next. **Fix:** build all nonempty piece lists for a round first, submit them once using `--pieces enum20,enum30,smc,smcrep` restricted to those lists, then use a fresh wave name for the next round; alternatively document unique names for sequential per-piece waves. Include a two-incomplete-piece command-sequence test.

9. **Should-fix — retuning bypasses the resource admission check and does not wait for a lower allocation.** `retune_throttle.sh:11` checks only for `_prodH` names when raising, then `retune_throttle.sh:18` issues updates without a CPU plan/combined-ceiling receipt. It can raise L to 132 while non-H jobs already use more than 60 billed CPUs. Lowering the pending throttle does not terminate already running tasks, so the immediate H submission suggested by `JOB.md:39` does not itself prove that L has fallen to 68. PROD-H's array-task guard counts running tasks as well as pending throttles and may refuse until they drain; task counts also fail to express enum30's 16 CPUs. **Fix:** run a fresh fail-closed ceiling calculation for retuning, record the actual updates and scheduler confirmation, and require running allocations to drain to the withH budget before H is admitted. Keep the H task guard and the 192-billed-CPU check as separate constraints. Add raising-with-other-work and lowering-while-over-throttle controls. This is a resource-policy finding, not a claim of changed scientific output.

10. **Should-fix — the waiter can declare success with missing job accounting.** `waiter.sh:19` requires only a positive number of returned terminal rows, not coverage of every requested ID. A single COMPLETED row for three requested jobs is accepted when the queue is empty; the existing WT40 test even encodes this as success (`tests/test_waiter.sh:76`, the WT40 scenario). This recreates an accounting-lag blind spot despite the improved terminal-state vocabulary. **Fix:** use a delimited, untruncated JobID/State query and require every requested job/array to be represented with complete terminal evidence; missing or unparsable rows mean UNKNOWN, never ALL_TERMINAL. Retain immediate notification of any real failure and add partial-accounting controls.

11. **Should-fix — manifest diagnostics are written into home.** `make_manifests.sh:49` redirects reconciliation stdout/stderr to `RUN_HOME/manifests/.reconcile_<piece>.out`, contrary to the all-logs-on-scratch requirement. These are diagnostic logs, not the small authoritative inventory. **Fix:** keep these logs under `LOG_RUN/reconcile/`, retaining only the inventory and its checksum/closure metadata in home. Ensure they are created before the logs manifest is frozen and included in the log download.

12. **Minor — the P5 “at most 16 used” bound excludes its explicit margins.** `CORE_HOURS.md:19` and `JOB.md:65` state at most 16 billed core-hours per P5 fit. `prodl.env:39` permits 29,100 seconds plus 60 seconds kill grace, already **16.2 billed core-hours** at two CPUs before task setup/commit overhead; the actual scheduler ceiling is 18. **Fix:** label 16 as the nominal doubled core allocation only, distinguish it from the wrapper/task bound, and retain 18 as the per-unit requested-wall ceiling. The expected/conservative/sensitivity totals otherwise tie out; no change to the frozen allocation is requested.

13. **Should-fix — production admission silently falls back from scheduler time to script time.** `batch_runner.sh:10` derives its deadline from the first command in the batch script; `batch_runner.sh:11` ignores an absent/nonnumeric `SLURM_JOB_END_TIME`. Script start alone does not establish the scheduler's remaining wall time; the bundle neither measures nor bounds any scheduler-start-to-script-start delay. No staging/submission gate establishes that NOTS supplies an accurate numeric end time. The supplied DL74 test deliberately accepts a junk value. The margins are conservative once the actual end is known, but cannot establish the D47 deadline guarantee when that value is unavailable. **Fix:** for production require a validated scheduler end time, or derive a conservative deadline from validated Slurm start/limit metadata; refuse before any fit if neither is available. Keep the script-time fallback restricted to local tests. Update `DESIGN.md:61` and add missing/malformed-end and delayed-script-start controls, with the scheduler time source recorded in the task evidence. This does not require a change to the frozen fit allocation.

## Checks and limits of the evidence

- The deterministic list generator checks the entire committed `lists/units.tsv`: **600 enum20, 600 enum30, 2,400 primary SMC, 12,000 repeats**, with the required task grouping and five additional seeds per primary. The adapter derives primary + 1,000·m. The enum requests use 4/16 threads and 1 GiB; primary/repeat core arguments remain 2 GiB/4 h; P5 correctly passes the primary allocation and `--p5-retry`, letting the frozen adapter double it. No benchmark execution path is included.
- The frozen manifest is **`d880afdbd0c1b7836862b5dff01a05168197f044deb757716e9549406f2e13e1`**; all **27** listed source hashes match. The shared P0a script retains the accepted rev-7d tolerance and exact checks; P0b checks all 1,200 staged input files. `frozen_check.sh`, `guard_check.sh`, `truth_lib.sh`, `truth_wave.sh` and `R/pilot_build.R` match their pilot sources after LF normalization. No frozen source was modified.
- **47** shell syntax/Python-3.9 grammar checks passed. Python grammar compatibility is not a claim that Python 3.9 or RHEL was executed locally. The supplied `SUMMARY_run4.txt` sums to **903 passed / 0 failed**. The independent rerun also completed with **903 passed / 0 failed**, all ten suite exit statuses 0; `r1_20261030T104842Z/suite/SUMMARY.txt` and the per-suite logs/exit files retain the evidence. The harness requires `prodl_tests/`; only the temporary test-source copies changed that literal to `prodl_sol/` to obey this review's destination restriction. Operational scripts under test were unchanged. The test snapshot is `<PC_TEMP_PATH>`; no R processes were launched.
- Offline fault injections use the actual bundle wrappers with fabricated Slurm/R/time responses. They establish the control-flow defects above, not current NOTS scheduler behavior. Evidence: `prodl_sol/repro_r1.sh`, `prodl_sol/repro_restart_r1.sh`, `prodl_sol/audit_r1.py`; saved results under `r1_20261030T104842Z/repros/`, `restart_repro/` and `audit.txt`. The retained live local integration was read, not rerun; it confirms successful primary/repeat/enum execution and resume on four units with a timing shim, but does not validate real Slurm, P5, Linux permission enforcement or NFS cleanup.
- Deadline arithmetic consistently uses epoch seconds, records T0 before module initialization, caps against numeric `SLURM_JOB_END_TIME`, and includes hard timeout, kill grace and commit margin before each launch. With an accurate scheduler end time, its start-admission inequality is conservative. Atomic rename protects individual published ledger files; `.start` without `.end` can expose an external kill when the task is not restarted. The unconditional statement in `DESIGN.md:64` that Slurm “never kills a fit mid-write” must be limited to ordinary wall-budget protection: OOM, NODE_FAIL and cancellation can interrupt any stage, which is why the recovery findings matter.
- Normal-path dependency ordering serializes SMC/repeats, shares the truth lock, and gives the stated **132 alone / 68 withH** fit peaks, or **188** combined with H at 120. Explicit-ID cancellation and the named-variable launch environment avoid broad cancellation selectors and recording inherited secrets. Cleanup's canonical target checks, scratch-output refusal, outside-tree receipt and memory re-exec follow B3; local stub tests cannot certify actual NFS behavior. Recovery currently verifies modes/counts, not truth file hashes; after recovery OPS must verify the staged truth hashes before calling it restored, as required by `JOB.md:73`.
- Independent arithmetic reproduces repeat costs **48.428571 expected / 79.428571 conservative / 95.023810 delay-sensitivity billed core-hours**. Adding the other displayed rows gives about **134 / 173 / 191**. These are scenarios from sparse pilot timing, exclude P5/benchmarks and extra recovery waves, and should be revised from production accounting. The approximately 6 GiB scratch baseline and one approximately 100 MiB home stage agree with the expanded repeat count and D49. The guard remains authoritative; D31 precedes any D40 fallback. The guard checker still contains hard-coded 9.6-GiB probes (`guard_check.sh:39`), so an eventual HQ-authorized D40 change must update the required limit and probes coherently rather than editing only OPS's guard.

The required rerun scope is focused: regression controls for the findings above, the repaired OPS sequence, and the existing suites. Acceptance must retain all scientific failures and interrupted attempts explicitly and must not close a folder that still has an unresolved required P5 outcome.

## Reference hashes

SHA-256 of the principal external references read for this review (paths relative to CAMP):

```text
727d30fe968b7031ce40cf511a22f4cb00fd85d4201a02a225e6bf8328adcec8  DECISIONS.md
d583eeebccbc388b5278ff85cb1eb5a79fe927408a69d82fb4f19616a12f8928  CHARTER.md
9bb0da4fe4c2d38d0568526b876c742457057114eae729149643453d25c279b5  ops/PROD_L_SIZING_20261030.md
f1dc1365084c1f24be261b537a651a395f9c71ff3694127cd7e7c5207f401ead  ops/review/SOL_REVIEW_PILOT_20261030T0712Z.md
d880afdbd0c1b7836862b5dff01a05168197f044deb757716e9549406f2e13e1  code/core/v2_2_1.SHA256SUMS
241815a512a90fbcd4a8684a5f317547d85e60e3d94e1cdb3d3bd6f9f5d5442c  code/core/v2_2_1/study/run_case.R
a398c11221f8745efda2583eca211f09d43236c56569022656e3b9984f701518  code/core/v2_2_1/study/adapter.R
0580336bedfda60d0f4b2bc32614948999336f40ce9ebb464a45879c6f14fa8e  code/core/v2_2_1/tools/p5_scan.R
1490643ed17d113921a4c95bed883dbf849408df13cc67f54c693d9bc4730cf1  code/lowp/enum/run_enum_dataset.R
9c49594727b9c6cc00d31c4efa283dba9218f5ce81395cae857769a7a494606b  code/lowp/R/lowp_verify_nots.R
3d0c2da6ff1d7818b8a3e73d80acef2a81ec3b9e421c499635b7eef18c025416  code/lowp/tests/test_truth_lock_linux.sh
f46fe38edcc35b8d0c266a19daf44c6fa8ee1c9e1e6766163c76806e04ae8827  ops/transfer/nots_pull.py
7ff0d3885bea3634d2b3fb77ad9c927bae269474113695166658cda3f3b07dd8  code/lowp/pilot/JOB.md
adb19dd8212fc94e9da1d9705cf54b61c5d6a370a937b71e205b702e0643bf44  code/lowp/pilot/slurm/s8_unlock.sbatch
a0943672da2b9cc97b6e8281e66027fd45c4b34e2b505b7fe9ed561e77f5e4c5  code/lowp/pilot/slurm/s9_collect.sbatch
```

## Bundle-file SHA-256 audit

Raw-byte SHA-256 of every reviewed bundle file, paths relative to B. Source snapshot rechecked against the tested copy; no operational source changed during review. Generated Python bytecode and this review itself are excluded.

```text
fff479309e23480d794b6b296e1691a0f4636b4018dc3e70cc8f61da8376f4e2  batch_runner.sh
150dd20ba6e1e3160da3ed9a20cc8e70cdabf87dbdd69142c2cfd54b259329d4  bench_hook/README.md
abb1fc008565d1065ac3791efd505875b17334336970bcf90bc9b360ddffa828  BUILD_NOTES.md
9bdc199041cc2ad479d31c1bb8024c57ecc74b25058e28d6cf1e5a338e530b08  BUILD_NOTES_A.md
ae777dcf597e0a52c265fc10d2276fb961e06daad486684f954b0e411981891a  BUILD_NOTES_B.md
fd769bc89bbb79467122e149cecbd6ae2e800b5e2e60fe8abd65c396d2372c31  BUILD_NOTES_C.md
d89febae16b27714cd6bd097a4b6407bc4bc4bfdce0fc178790235724514d001  ceiling_check.py
5400e033c99889bdc1d532ad999e3852c40a2a2113347c3aaeb4b53cd0c77661  cleanup_prodl.sh
10e501bbbadafbebf147fc53121516223b66a296fe1434a72229bf5681d33e6c  clear_stale.sh
e482d599d9c6d8d5f0d0296c90c854ea27133d8caa35aac17143aec47e94b461  CORE_HOURS.md
f6f95cd2be126295061e755204f4e49e84f6e5cb26913ea88b5d3a97c166db78  DESIGN.md
003b75d86497b2073dee1d6c539b8cc38df99fcec10abc064bf13d48181e4202  final_accounting.sh
f29dc13185aad63d5e0fe1bc8ab8022cd942cbeb7d9d29f43e42f9d7ffac51d5  fixtures/empty.receipt
be41889ec09802b4eea3dd4643ca75a0649fe62c529c46807d0d5ce5c1586278  fixtures/plan_alone.tsv
ab941f22e9430d4407b801280f63cfc07fc7dbb1a594b81f77a1c0343abf4e02  fixtures/prodh.receipt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  fixtures/squeue_empty.txt
953d792ff3eb150dfb736dcd94530c1ebcbf9c68dff073e15d83d28bc28fa7ca  fixtures/squeue_prodh.txt
ae1aacc23c1ff7c9cea7b9c0016872e805f415c1a839163abe2a9665c9ebbf72  frozen_check.sh
3625033365a168dd4e255f4a74453a46378aaf5bfcdcb160ef614923d9232384  guard_check.sh
8772b4617a88d98c3f8d03e5f53b9539ed22d5c2ffb48bf3769a5719f6f23a80  JOB.md
df21f1d702abae64fa5510f1a6997dd45cd607694886b3e4e7e2fc54f33581be  lists/units.tsv
905d360e9163678d60334e6f770d8575f91491c71e1cf9e73411b021e491640f  make_manifests.sh
6bca80529ec22e6f659501cd9da4fa5d34e542a8c5ebcc1e534f4fc8b9f42a2b  make_p5_list.sh
17fd74b82a2c6560111c096167849bc27b699d3559b021b03557874e1085aed3  make_resubmit.sh
c2d735bfc7d106f52613e78200906c437d5df83f4f6f93b37d5b5114c131855a  prodl.env
1215a35568dc0f4cec21c8fa61073e9de7042574461f724b160203ed6f3f7c1d  PROGRESS.md
6363e3466bb038a86564ea8093999d99418338a2b6d71ae0d269e5a8490ff02b  R/pilot_build.R
d7bf0d48dd345a58c70baa9c3574aa968102fe640ba7296f962a134e73ece1f3  R/prodl_inputs_check.R
96260afd5ae500b258234b6505bcb325bf9b01102cc6ae3039cd1c7b27ac86f0  reconcile_prodl.py
bede0b38301b26dbec4fd8316236d42ff1601ebc4ea3b75c43bb2b6207392ae2  recover_truth.sh
bc5696ebbb222ea5ae41b334cff8c04182674db74800b1c80bb0ba3b4966402e  retune_throttle.sh
a1e85423b18af699aa7ad1891bc9b9d1ca205b88d4b284d79f8ec7913b7d6fd8  REUSE.md
e50a7613e475f8a829ecfa079dd5106bc06be05061ba10a52ed4e7a44069b839  slurm/common.sh
4810abea2c3121d20301d15cd8e57a7496e7255a0e5ff25f6cbb6f488dccf582  slurm/s0_build.sbatch
b7afea638bfdd0992e82ac3052b6d9df1c486a19cf86a013cce21b7ff70a79f4  slurm/s0_lock.sbatch
d892b7baaa8d125ca464d8e9ec091f0d311e62b046a8688ad7f4f085a6d9c4d9  slurm/s0_truthlock.sbatch
0220a5624e9d94e935c529cfb7a18dd2c2ce3cc13bdcfff48c8a383fabaa492f  slurm/s0_verify.sbatch
87bd4eb0144e30a822d289e64b6f10f8ea04c1dc0150406eb115cea9bbfac39d  slurm/s1_enum20.sbatch
20072a45ddcc9eb84ab6a66c6c2108c91b0f5d9487039063ff46bab4457dac84  slurm/s1_enum30.sbatch
55f2b69b30eefbf6fadb5410bc541ea4dbaab64270fb4364bf7aaae43a56cdf6  slurm/s2_smc.sbatch
4a5f828a73ba55fff4d5da0dd3be6a5b4c8b89fadd4e851f7ce1c9d1c5bfe51e  slurm/s3_smcrep.sbatch
024e4e9329f0dd6f4b9838f1f79ec7bc95e1eb89629a72f85bacc41eb8739f95  slurm/s4_p5.sbatch
cde5e55b522e4617fcf658f1ea9c1296108d237a012d58e2e740305e97507b38  slurm/s5_p5scan.sbatch
3d9449a891563fd14f0fe196d91ddc16d91046bb9b332bcc3a530bad1ebf49fe  slurm/s8_unlock.sbatch
65770b8d73f4b14cf26175af534224280f22bc67e679d94be52c1bb003cabe0d  slurm/s9_collect.sbatch
167b2906dc98396e8c2c2d345793c46e5f98975dc82c0d2754a4236cfc731316  stage_local.sh
538186709a1637e8172cf0d99f80d3c786924ba5f713625d6400750d35e64ccc  submit_prodl.sh
1985c6c064575be1c49cdb79410b7727be3c9e2b9e7559114583265a926cafed  tests/lib.sh
f2deab792ed7d744ecf2781a2ca13192f8094382b2db1df88b725c19d7f8b796  tests/live/gnutime_shim.sh
9fb3b6f82e095c74e0e899f262e7b9e43f1160886e7a0a1402bed4b408454587  tests/live/live.sh
4c29a6dc50e4e603cfea347f52571bc3d49bd09d78ed8356e799a67b8a694e45  tests/live/live_20261030T0956Z.out
969dabe25f84531650a575e813ac3d35bf1da162e234bb9e7d6116cd8b4829de  tests/run_all.sh
45e97aece1f82248938588dd57113a265bb7fa6a861cd7a182aa391f287ce93b  tests/SUMMARY_run4.txt
493655757ca2020af042798c79be785cca56fa85b154c2291f0df328bf3a7146  tests/test_ceiling.py
96c44fd12090e88a4bf050b0363ce6c5a318fa71d99083d3553d89d8f71e0b76  tests/test_cleanup.sh
f3323c1f559ba3fd4fcdc3bfe7f52fad3de08620f8f3024fad442fe35bda4316  tests/test_deadline.sh
48b1e584267e3ddb1a8c81582fb01754634011c10e562f7e7d768fb74c8885b4  tests/test_driver.sh
16f02f98f9becc5c4b63fb604a6c40e1a251a562d72017ef5dcbcdd2f89f7295  tests/test_lists.py
4d0bdfceb8a8a9522f37f0e5de2a5539d7e9ff5ecd742f2f849a5c964d626f33  tests/test_manifests.sh
e6a8801aeabba9bab97ac7b07a990285bff8cb13af2a5a99806fe73e80c19384  tests/test_reconcile.py
32c90ade9dee242b4ff0c8a28454453348299e7761c02359dd6ec11400a3afe0  tests/test_resubmit.sh
06c503afa43445dce6a537c5851018957ae6bd0849d5c9b8ccd74726a3fad0c2  tests/test_unlock.sh
33eb0eb8b91ffc75a1a56ff5a9529b6570e415c99261b3f1716d8db3d5121ed4  tests/test_waiter.sh
0418ade8f577afdfb392580745d06dde08e8b1a62d12538d91282ca108ea4c23  tests/TESTS.md
134665f7225df9c3f17cdd2c933ed64f24a299b0fca0883edc1a83bd12b91e40  tests/vec_check.py
cfdf0ba05fc3a94f70516ce9cd8d5e8e60e89d215fc969ea7e6b6b1dbe73912e  tools/make_lists.py
a4b4ddcd5b8b680cda3c8b30738949cab46a6baaba267e3dccb9acdd6c2436ae  truth_lib.sh
0fd6b1c80dcefca4b6ab37f1a9b4242cb4ebe46d2102ab3945a42a692ea24e5d  truth_wave.sh
4593d8eda6c4dcfebcedc1e946900958f9eefc9d03474901629f7de8bbe422ae  waiter.sh
```
