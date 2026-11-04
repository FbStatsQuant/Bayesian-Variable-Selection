# Deployment RUNS (merged by the managing lead)

## A

# Thread A RUNS candidates for lead merge (R-2)

These are individual development/verification jobs, not arrays or production fits. Root RUNS.md is untouched. All executed jobs used Owls R 4.6.0/GCC 11.5.0, nice 19, one numerical thread per job, with frozen source and per-job command/environment/exit evidence. The lead should deduplicate historical candidates against existing entries.

| Run | Source revision | PID | Result | Evidence |
|---|---|---:|---|---|
| build_v1 | v1 | 998611 | PASS exit 0, 11.41s, 458068KiB | v1_pass_and_smoke500 archive; HANDOFF_v1.md |
| regression_v1 | v1 | 998294 | PASS 32 seeds, 768 checks, detailed units, 166.25s, 516856KiB | v1_pass_and_smoke500 archive |
| adapter03 | candidate02, core identical v1 | 993596 | PASS 40 fixtures, 2.87s | interim01 archive |
| guards01 | launch revision before v1 | ? | PASS 20 guard/path checks | regression_pass01 archive |
| smoke500 | candidate02, core identical v1 | 993079 | PASS n200/p500 dev S1/r001 c100, data2420001 method6420001; 688.60s | v1_pass_and_smoke500 archive |
| smoke1000 | candidate02, core identical v1 | 993115 | PASS n200/p1000 dev S1/r001 c100, data2520001 method6520001; 1664.68s | smoke_final01 archive |
| smoke_audit | v1 audit | ? | PASS both saved fits; no new fits | smoke_final01 archive |

Archive SHA-256 values and exact laptop locations are in HANDOFF_v1.md. Historical rows use the original unresolved adapter mapping; native fits are preserved and the R-1 saved-output mapping audit is separately identified below. No production case, truth scoring or holdout was used. Failed historical harness jobs are documented in the original evidence; they are not successful runs.

NOTS: no job submitted. GCC/14.3.0 and R/4.5.2 compile plus full prototype regression are mandatory before any NOTS fit. Prepared scripts remain gated on the lead's exact `NOTS: open for runs` line.

| r1checks01 | interim v1_r1 (unreleased) | 1008955 | FAILED before tests: CRLF shell option error; no numerical work | A_build/evidence/v1_r1_upload.json; remote launcher.log retained |

| v2_candidate01 build/checks/regression | v2_candidate01 | 1010507 / 1010478 / 1010540 | PASS build12.06s457212KiB; 76adapter+savedmapping+4trap; 32seed896checks184.54s517964KiB | v2_candidate01_evidence.tar.gz SHA256 4e44b4592d3bca97ae71eed54aca009429f5469bf853037120ae4a416cb116b5; superseded by final failure-record repairs |

## Final frozen v2 verification (R-5)

Source archive SHA25617bdd21a719f3c7c4d876b21e926aeac4ba447ec71634e5ba20242068661e1ff; master and all file hashes in snapshots/v2/manifest.json. Owls R4.6/GCC11.5, nice19, single numerical thread per job. No Slurm/NOTS or production fit.

| Job | PID | Evidence | Result |
|---|---:|---|---|
| v2build | 1015949 | runs/v2build; laptop v2_regression_pass.tar.gz | PASS 12.18s peak457572KiB |
| v2checks01 | 1015923 | runs/v2checks01; same archive | PASS 76 adapter checks, mapping audit, syntax and4 trap cases |
| v2regression | 1015982 | runs/v2regression; same archive | PASS32seeds/896checks plus units,193.83s peak516904KiB |
| v2smoke500 | 1018922 | runs/v2smoke500; v2dev500 | Launched21:13:43Z; final outcome appended below |
| v2smoke1000 | 1018953 | runs/v2smoke1000; v2dev1000 | Launched21:13:43Z; final outcome appended below |

### Final v2 smoke outcomes (supersedes pending rows above)

- v2smoke500 PID1018922: exit0, native completed, both rows ok; core688.251s/process692.20s; peak process302608KiB, fit240220KiB.
- v2smoke1000 PID1018953: exit0, native completed, both rows ok; core1564.474s/process1570.95s; peak process398612KiB, fit366772KiB.
- v2smoke_audit PID1021333: exit0, SMOKE_OUTPUT_AUDIT PASS; complete records/stages/seeds/hashes/R1 rows inspected.
- Laptop archive v2_smokes_pass.tar.gz SHA256de13c86f36eb1b92719eb60c89ab734bc4f60154202bf31bde9384161b570e8d verified; individual RDS/CSV hashes also verified. Both development cases n200, S1/r001/c100, data2420001/2520001 and method6420001/6520001. No production cases, truth or holdout.
- HANDOFF_v2.md is the final A deliverable. B independent v2 verification remains required; G1 CLOSED, NOTS not executed.


## B

# B run candidates for root RUNS.md (R-2; append only)

| Run | Backend / process | Frozen manifest | Seed(s) / commands | Outcome / archive |
|---|---|---|---|---|
| local_deterministic_r1_20261022T1900Z | local, authorized temporary moratorium before Amendment1 | B_verify/runs/local_deterministic_r1_20261022T1900Z/manifest.sha256.json | saved command.txt, per-test seed2026102201 | Original deterministic suite PASS; historical superseded oracle, actual times~18:59Z in JSON |
| owls_phase1_r2_20261022T193459Z | Owls PID994329, one CPU nice19 | B_verify/runs/owls_phase1_r2_20261022T193459Z/manifest.json | source/launch_owls.sh; source/run_battery.py --output evidence --law; four intended seeds2026102201..04 | FAIL exit1; scorer13/14,5 other suitesPASS; no statistical draws; bit_count Python3.9 compatibility and awk guard error retained; wall7.60s maxRSS101116KiB |
| owls_phase1_r3_20261022T194056Z | Owls prepared only, NO launch/PID | B_verify/runs/owls_phase1_r3_20261022T194056Z/manifest.json | no execution | HELD before launch due fresh F1/F2 scorer static findings; no outputs |

r2 full archive: C:/Users/felip/Documents/NOTS_BVS/smcbvs_v3_deploy_20261022/B_verify/owls_phase1_r2_20261022T193459Z.finished.tar; sha256 fc140dfe679f632e40a2f19249ae2e8c38b708bad548c7bc66b38f7135d820e0. Independent source reviews and failed evidence are retained, not erased by repairs.

| Run | Backend / process | Frozen manifest | Seed(s) / commands | Outcome / archive |
|---|---|---|---|---|
| owls_phase1_r4_20261022T195415Z | Owls PID1001592,1 CPU nice19 | B_verify/runs/owls_phase1_r4_20261022T195415Z/manifest.json | unchanged full battery, law skipped | FAIL scorer15/16 (raw-map cancellation),6 suitesPASS;7.84s102680KiB; archive sha d989a1fa133905b55ff1e1a2539c9a0f19fa61b1b0c440e325c4c5da26a0b7c4,82 files verified |
| owls_phase1_r5_20261022T195810Z | Owls PID1002478,1 CPU nice19 | B_verify/runs/owls_phase1_r5_20261022T195810Z/manifest.json | full7suite battery + four joint G fixtures,100000 each,seeds2026102201..04 | PASS exit0,56.35s128332KiB; archive sha d423d5c34e48d1d5cd221198b3251bd38bff7182818031fadbbed21f33589d2b,88 files verified |

r2/r4/r5 finished outputs copied to laptop, every artifact hashed, then remote evidence/scratch archives deleted 2026-10-22T20:01:52Z. Source/launch/artifact manifests retained on Owls with cleanup receipts. r3 never launched. R5 statistical family is reference_sampler only; no A draws and no dependent SMC samples tested.
## Phase 2 executions (all Owls, one CPU per worker, nice19)

Every run below has its original local B_verify/runs/<run>/manifest.json (except independent operators, which retain their own source/command receipts). Literal commands, environment, timestamps, source/input hashes, process IDs and per-command exit codes are inside the verified laptop archive. Serializers' exit0 is distinguished from their semantic predicates.

| Run | PID | Commands / seeds | Inspected outcome | Finished archive SHA-256 / verified payload files |
|---|---:|---|---|---|
| score_protocol_20261022T200609Z | 1003358 | independent run_battery --modules score protocol; seed2026102201 | PASS 16score+19protocol; no law repeat | e00d16d408350719a170b028bd8ae246c46e918a1c2de9d2fb2cd67efc70e736 /35 |
| phase2_aux_v1_20261022 | 1003924 | adapter fixture export and saved-smoke extraction | B harness invalid fixture; exit1; preserved, not A FAIL | 7cdec853c1ada4dd49178f44b2bc12f781566d936d11167299431bfae594f7f4 /49 |
| phase2_aux_v1_r2_20261022 | 1004092 | repaired fixture export and smoke extraction; no new smoke fits | exit0;37 fixtures exported, one later excluded | e3ce06a84305a779a0bfa27a2c3b55c4f3572dd7f025b129db3edd7fab4f56ed /58 |
| phase2_auxcheck_v1_20261022 | 1005942 | frozen-oracle adapter and smoke comparisons | exit0;36 mapping FAIL;2smoke PASS | 2da370eb6abb0931295e70b07a46330ebb112a6148067521f9802e313bef4742 /16 |
| phase2_compare_v1_20261022 | 1006147 | compare.py then preprocess.R; first A start family seeds2026102201..04,100000 each,stream200 | 251checks+4G PASS; nearconstant/shapes FAIL | d115fc39c845149b625e7f6078bded58b66d6d7dbb9e5f0a0aaef88771295e52 /101 |
| phase2_kernel_v1_20261022 | 1006811 | kernel R, oracle Python, orchestration R; scripted uniforms/no random draws | B wrapper compile FAIL; kernel NOTTESTED; orchestration results retained | d9b05d055906029a856811641fde9145df36d7f07510cbb1a734675c707a5664 /74 |
| phase2_operator_20261022T2035Z | 1007506 | independent auxcheck, preprocessing(seed123), orchestration(seed1), once each | Reproduced A failures;smokes/preflight PASS; no statistical repeat | 7991f36bd460bb8ddfef5d1b7929af6c1576c5df14648b5039b27ab9a71b612a /92 plus manifest |
| phase2_semantics_v1_20261022 | 1007902 | semantics.R; exact seed20261022; deterministic assembly/cut fixtures | 10/10PASS,exit0,12.09s457488KiB | 7f51e2d54ce483f6cdf91458ae577582fc4d2a62bb4c13305c7cc2db4cefa04e /53 |
| phase2_kernel_v1_r2_20261022 | 1008090 | compiler-plugin-only B repair; same deterministic kernel/ oracle/orchestration commands | elementary/resampling/p1round PASS; actual timing-size FAIL, shell1;18.54s458104KiB kernel | 4f225bfd70425ccb62a98fce6dfc0f9a22bf931d37c213fd9b104fd76bf60225 /77 |

Laptop root: C:/Users/felip/Documents/NOTS_BVS/smcbvs_v3_deploy_20261022/B_verify/. The independent score/protocol archive is under independent_execution/score_protocol_20261022T200609Z/; all other Phase2 archives are <run>.finished.tar at this root. Every extracted file verified. All41 top-level B code ledger identities pass the scoped checker at closeout. Phase2 remote bulk evidence, smoke copies, compiled caches and verified archives removed20:44:00Z, after matching laptop AND remote bytes; source/manifests and small audit records retained. CLEANUP_RECEIPT_v1.json lists exact removed paths. No active numerical jobs or NOTS work.

## V2 verification runs (R-2 append candidates)

All on Owls, persistent nohup, nice19, CPU0 only, BLAS/OMP/etc threads1,2GiB address-space cap. Load/memory admitted below R-3 thresholds; no concurrent B SSH, no NOTS, no Slurm. Environments, exact commands, PIDs, seeds, timing/RSS, exits and source/input hashes are in each immutable worker manifest. Only two Sol high delegates, both complete.

| Run | Worker PID / UTC | Commands and seeds | Inspected result | Archive SHA-256 / verified files |
|---|---|---|---|---|
| phase2_v2_main_20261022 | 1023162;22:02:39?22:03:33Z | worker.sh: reference seven suites;compare;preprocess;orchestration;adapter;smoke export;auxcheck;kernel;matrix verifier;semantics. First v2 G-family seeds2026102201..04,100000 each,stream200. | all10 commands exit0;251 comparisons,4 G-tests,36 valid adapter fixtures,13 input checks,original2centering,14 kernel verifier groups,10 semantics,2smokes PASS | 05c68c8c3c522caa7d587d2754a7d4d45a9a353d3077a2a29271e4db632f733a /194 |
| v2_independent_execution_20261022T2208Z | 1023604;22:06:30Z; repair1023773;22:06:59Z | actual extracted message/warning handlers+writer; timing-only actual200 scores; isolated missing-AST-formal repair; no statistical draws | original B handler harness exit1 preserved; timing PASS once; repaired handler13/13 PASS,exit0 | b1ab5057b5ea41e6883ec7443c0945423d4beec7e7be55fc13eab4c5e1c44bb5 /105 including manifest |
| phase2_v2_containment_20261022 | 1024036;22:10:30?22:10:46Z | v2_containment.R a_code . evidence/containment;v2_nearconstant_R5.R a_code evidence/nearconstant_R5;seed2026102205 for tiny SMC fixture | containment6/6 PASS,exit0;additional reviewer hand canary X/y coordinate error1.8626452602532595e-9,FAIL versus2e-12; overall exit1 | dee7d949ff998862217baffd5f46275f435e9fc445794185356a1be8deecc26c /146 |

Laptop root: C:/Users/felip/Documents/NOTS_BVS/smcbvs_v3_deploy_20261022/B_verify/. ARCHIVES_v2.json indexes all receipts; archive and every-file verification passed. Before cleanup, selected remote directories matched all verified laptop bytes exactly. CLEANUP_RECEIPT_v2.json records removal at22:12:30Z of eight evidence/smoke/cache directories and five transferred/result archives. Frozen sources/manifests remain. All four worker PIDs were absent. Main v2_supplement.R was a separately archived post-main companion, not retroactively added to the main manifest.

The containment source executed is runs/phase2_v2_containment_20261022/v2_containment.R. The author's final top-level file later adds the same centering canary; this difference is recorded in v2_containment_final_addition.patch and the final combined file is NOT claimed executed. The parent separately executed the reviewer-specified canary using the same pre-existing prepared-data tolerance; both implementations use the closed-form standardized vector. No statistical retry or retuning occurred.


## C

# C run candidates — append-only, for managing-lead merge

## data120_20261022T194227Z — Owls input audit

- Frozen package: owls/data/data_120_v2.tar.gz; SHA256 ab98428eac5fb2db9c0d7565146b255437802de4c13412635069f5635cdf5c13.
- Launch: owls/data/Parent-Transfer-And-Launch_v2.ps1, with process-local PowerShell ExecutionPolicy Bypass. Serialized configured owls SSH/SCP. Parent transcript retained beside script.
- Remote: nice19 bash data_120_v2/scripts/launch_audit.sh under ulimit -v2097152; single numerical-library thread. Full argv/environment saved.
- ShellPID997613; RPID997651; launch19:42:27Z; finished19:43:21Z; exit0.120datasets/240units,12611checks,0failures. Wall53.07s; peakRSS120116KiB.
- Remote output: /home/fb31/smcbvs_v3_deploy_20261022/C_ops/data_audits/data120_20261022T194227Z. Local copy: owls/data/remote_results/data120_20261022T194227Z. OUTPUT_SHA256SUMS verified18/18; all21 saved files inventoried; no deletion.
- Frozen tables record seed provenance; the audit draws no random numbers. Independent v2 review pending. No SMC fit.

## Preserved infrastructure failures

- v1 upload19:34Z succeeded; checksum verification rejected CRLF filename. No extraction or audit. Original archive/scripts/log retained.
- A read-only status command lost nested SSH quoting and listed home rather than the audit directory. No mutation. Corrected with encoded owned shell script and inspected saved outputs.
- Pull-helper inspection succeeded; manifest failed on symlink/special file in global disk inventory before any copy. Laptop audit .transfer_audit/20261022T194426Z-c63172960b6940999eb4fb1f917dae1c retained. Evidence copied by serialized scp and SHA256-verified; helper issue under review.

## smoke_data_v3 — inputs-only preparation, independently verified

2026-10-22 19:58:02–19:58:04Z, Owls. ShellPID1002305, nice19, single numerical-library thread,2GiB address cap, exit0. Frozen manifest SHA8259f3a1ac92a536cdaa22d657680b38599daac88ab2cd6e5ff256289c5c2a89; code inventory SHAfa345de7326a33d3663687334809659e4dd18c4edac6f0fe437c782ce0c00ca5. Launch nohup nice -n19 bash snapshot/generate_smoke.sh /home/fb31/smcbvs_v3_deploy_20261022/C_ops/runs/smoke_data_v3. Saved launch.log/launch.pid/argv manifest/exit/timestamps and GNUtime:0.71s,142300KiBRSS. Beforeload1=1.14 available64GiB, disk772493312bytes plus64MiB reserved, after774942720bytes. Inputs-only seeds2450001/2550001,method6450001/6550001. No SMCfit.

20/20 completed-run checksums verified locally at owls/pilot/remote_results/smoke_data_v3. Six generatedfiles copied to required laptop smoke_inputs root and6/6 hashes verified against INPUT_FINAL_SHA256SUMS. No deletion. Review OWLS_PILOT_TRANSFER_REVIEW_v3.md PASS for exactsources/execution. v1/v2 snapshots preserved; v2 stopped before generation due GNUawk builtin load-name conflict, ownedPID1001415+sleep1001432 terminated by primary after identity checks.

## transfer_v3 lifecycle — disposable infrastructure fixture, independently verified

Linux fixture result evidence/transfer_v3_lifecycle/LINUX_FIXTURE_RESULT.json, helperSHAf5f2f5dec86720b7d29f46372edde8f29eb06201c95257777fb23cfa5cf65e8d, nice19,6checksPASS. RealWindowsclient inspect/pull/freshverify/delete audits at laptop .transfer_audit IDs195536Z-eb9383dd3fc7440c8d29810d9de54f52,195614Z-417f6bebad35469d9766505de4304917,195720Z-c00f0f26514d433e85146f9cb5af5194 (all20261022T prefix). Exact31byte dummy result.csv copied+verified before deletion; separate remoteassert resultabsent and logretained. DeletionworkerPID1002221; alljournalstatusescomplete, no scientificdeletion. Source/code/logs/receipt retained and independently reviewedPASS.
- 2026-10-22T20:34:08Z: isolated infrastructure resource/recovery validation resource_recovery_20261022T203356Z, Owls persistent launcher1007117/inspection1007131, nice19, AS1GiB; FAILED admission exit1 on protected sd-pam cwd, before fixtures/fits. Snapshot archive791d0909d0923d90bf91ff6503596f928e7b0bfd7edf69525a7143a44d0b224e. Full failed evidence archive eb79a9211cc352b1c58b227dcf9ef263c33244df972691bc4626bbb5a80e178f copied and verified to laptop infrastructure_evidence; remote retained. Local integration/evidence/resource_recovery_20261022T203356Z/LOCAL_VERIFICATION.json records per-file count. Earlier203333Z checksum-list CRLF rejection preserved before launch; fixed LF list in203356Z. No science/scheduler run.

- 2026-10-22T20:59:33Z: Owls resource_recovery_20261022T205837Z PID1010452 exit0. Automatic admissionPASS;54resourcechecks,21recoverystubtests,107native-contracttestsPASS. nice19,oneCPU/fixture,address1GiB. Sourcearchive e7b164d4ae4e2a7905e06dc44ef6b72aee43942de74b43c5509a9d1d2a74a411;983regular evidencefilesverified; evidencearchive330a0627e246980c80976d31aa320300911e5256ea1c8e88d65ade131c805834 copiedto designated laptop infrastructure_evidence. Remote retained. Component validation only; noSMC/scheduler, broaderintegration andindependentreviewpending. Stopped perleadtempo afterthisstep.
