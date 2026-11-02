# CONF-2b review 3 — independent Sol re-check

Reviewer: Sol 6.1, 2026-10-29. Binding context: CHARTER §§2/3/6, DECISIONS D10/D11/D19–D21, and historical GO_2400 C1–C5. Review 2, its disposition, REVIEW2_FIXES.md, CONF2B_PROGRESS.md and the pre-review-2 bundle were read. No SSH, NOTS access, submission, compilation, numerical sampler fits or subagents. All execution was local, explicitly authorized review validation with R 4.4.1, Git Bash and `py -3`; scheduler and fit execution in PROD-H checks were stubbed.

**Part A: YES — v2.2.1 is ready to FREEZE at the verified manifest below.**

**Part B: NOT READY for HQ → OPS.** The previous blocking hold defect is resolved. Two should-fix defects remain in the new scan-job machinery (R3-1/R3-2). No blocking finding remains. R3-3 is minor.

Evidence root **E**: `<PC_TEMP_PATH>`. All paths below are relative to the campaign directory **C**, unless stated otherwise. Reviewed files were not edited; this review and scratch files are the only writes to review deliverables.

## Part A — freeze decision

| Finding | Verdict | Re-check |
|---|---|---|
| R2-2 / review-1 F5: different-checkpoint classifier | RESOLVED | Both stop timings must be finite scalar doubles without attributes; all eight invariant fields must be present and identical; non-NULL type changes fail. The four saved pairs retain their intended classifications, all 27 supplied controls pass, and my original string-timing/string-p corruptions now fail on all three different-checkpoint pairs. D10 pairs remain explicitly timing-excluded, not numerical identity evidence. |
| R2-3 / review-1 F3: missing native status | RESOLVED | Scanner uses `record$native_status` without the raw-fit fallback. Missing-native primaries refuse with exit 1; a missing-native retry is `invalid_inspect`; neither is launchable. Legitimate `adapter_error` records remain accepted despite a different/missing raw fit status. The retry adapter and real CLI refuse the stripped primary before a retry is created. F3/F7 lane: 44/44. |
| Review-1 F1: competing commit / lock | RESOLVED | Re-ran lane G: 23/23, including a real saved competing commit and rechecks under the lock. |
| Review-1 F2: H named-NULL extras | RESOLVED | Re-ran lane G: 24/24. |
| Review-1 F4: resume stop phase | RESOLVED | Re-ran lane G: 22/22, with saved primary/retry guard and preflight stops and repeat-1 resume. |
| Review-1 F6: unlisted symlinks | RESOLVED (carried forward) | Reviewed frozen-check implementation is unchanged from review 2. PROD-H's fresh shell suite exercises frozen-tree and staging refusals; the prior pilot native-symlink evidence remains applicable. |
| Review-1 F7: partial retry artefacts | RESOLVED | Covered again by the 44/44 scanner checks: lock-only, temp-only, CSV-only and other incomplete states cannot launch a retry. |
| Pilot fixture consequence of R2-3 | RESOLVED | `code/lowp/pilot/tests/make_fabricated_pilot.R:88` supplies the native field. Read revision 7b and saved evidence for 89/89 negative and 54/54 shell checks; these pilot suites were not rerun in this review. |

Verified `code/core/v2_2_1.SHA256SUMS` SHA-256:

`df4e7cf0e20981ef9fe4632fe2280355cbdb9e15d2dd724f1615b2c232054c41`

All **27/27** listed file hashes match; the non-cache tree contains exactly those 27 files. All **21 core files** and their relative path sets are byte-identical to `code/core/v2_2/core`. The six-file diff applies cleanly to a scratch copy of v2.2 and reconstructs the entire current v2.2.1 tree byte for byte. Diff SHA-256:

`26303af84092f23179d8e02fd0d361693b2a337e8e6fcdaf111c7fe220ec5860`

The saved RESULTS.md has zero FAIL rows in every section. This review reran the changed classifier and all four lane-G scripts against copied code and saved fixtures; it did not rerun the historical numerical experiments. FREEZE approval concerns this reviewed tree and hash. PROD-H runner fixes below do not require changes to the numerical core or study tree.

## Part B — review-2 dispositions

| Finding / question | Verdict | Re-check |
|---|---|---|
| R2-1 (blocking): failed C3 hold | RESOLVED | Failed and partial holds are unconfirmed, retried and urgent; exit 3 is tested. My original failed-hold reproduction now returns HOLD_FAILED twice with two new hold calls on the second poll. Recovery confirms held tasks, returns STILL_HELD and archives the urgent request. No cancellation is used. |
| R2-4: full scanner on login node | PARTIAL | Full scan now runs on a 1-CPU/4G/1-hour compute job with scratch logs. Job COMPLETED, phase/job binding, table SHA-256, rows and scanner summary are checked before selection. The wrapper is missing its disk guard and mishandles a scheduler-query failure; R3-1/R3-2. |
| R2-5: killed P5 artefacts | RESOLVED | Terminal cleanup checks squeue and sacct for every recorded job, requires durable attempt evidence and P5 selection, archives proven locks/temps and preserves attempts; unproven/live-owner paths refuse. Fresh suite covers killed P5 → final scan → cleanup → manifests, primary kill, nested temps and scheduler failure. Independent cleanup archived the two selected P5 artefacts with attempt count unchanged. |
| R2-6: partial manifest pass / rerun | RESOLVED, minor edge R3-3 | All three folders are preflighted and temporary manifests verified before committing; existing manifests are revalidated. Independent late-folder refusal committed no earlier manifest; with nonempty folders cleanup/retry succeeds, unchanged rerun reuses all four manifests, and a later file addition refuses. Binary-marker normalization is effective. |
| R2-7: accepted sbatch / failed journal | RESOLVED | Accepted IDs are added before guarded journal writes; submission/rerun/P5/scan error paths cancel by explicit ID and report cancellation failure. Tests include actual accepted-stub-sbatch followed by journal failure. Scan retry handling has the separate R3-1 defect. |
| R2-8: name-filtered throttle | RESOLVED | Every fb31 array counts; unknown names, unlimited arrays and scheduler failures refuse. Defaults remain 50 + 50, reruns 10, P5 min(N,10). |
| R2-9: home execution logs / summary transfer | RESOLVED | Poll, scan, refusal, scheduler-stderr and lock execution logs use scratch. Home holds state/receipts/summaries and a verified HOME_MANIFEST. Source paths and fresh shell coverage agree. |
| R2-10: 600-second cadence | RESOLVED | JOB.md assigns 5–10-minute monitoring to OPS throughout production; >600 seconds is late, and the 601-second control passes. `--cadence` retains/checks active-production gaps. Monitoring remains an OPS responsibility, as documented. |
| Q1: QoS | RESOLVED | Explicit `--qos=nots_commons` appears on precompile, both primaries, rerun, P5 and scan submissions. JOB.md B2 assigns current eligibility verification to OPS; no remote eligibility claim is made here. |
| Q2: terminal exceptions before P5 | RESOLVED | Reconciled timeout/infra_repeat units are reported separately and excluded from P5; live/not_run/rerun_queued/infra/orphan still block. HQ acknowledgement is explicitly procedural in JOB.md F. |
| Accounting ceiling clarification | RESOLVED | Native primary budgets = 2,100 + 8,000 = 10,100 core-hours. Requested primary walls = 2,320 + 8,220 = 10,540; with precompile = 10,541. Scan jobs have a separate accounting group; reruns/P5 are additional. Allocated CPU time and elapsed core time remain distinct. |

## Numbered findings

### R3-1 — should-fix — a scheduler-query failure retires a possibly live scan and permits a replacement

**Location:** `conformance/jobs/PROD_H_DRAFT/runner/p5_submit.sh:74`, `:49`; `runner/p5_scan_run.sh:84`.

The wrapper exits 2 when squeue/sacct cannot be read. The parent treats every exit other than 0/10 as a failed scan and renames its job record. On a later invocation, live scan jobs are excluded from the live-job gate, and the missing current job record permits another submission. The original scan can still be running and writing the same `p5_scan_primary.tsv` and `.receipt`. This breaks the promised resume/one-recorded-scan semantics and can create competing table/receipt writers; it is not evidence of a duplicated fit or a consumed P5 attempt.

**Reproduction:** E/scan_full_final.log executes the real `p5_submit.sh` twice on a one-unit checksum-valid fabricated fixture. Stub sbatch accepts scan 8001; the first post-submit squeue query fails; the parent exits 2 and removes the current job record by retirement. The next invocation sees the still-live scan but accepts scan 8002 for the same phase. Both remain live in the stub queue. No real scheduler was contacted.

**Concrete fix:** distinguish unknown/query-failed state from proven terminal failure. Preserve the recorded job and receipt paths on scheduler errors and resume that same ID later. Retire/relaunch only after both queue/accounting establish that the old job cannot write anymore. Apply the same rule to post-acceptance abort/cancel uncertainty. Add a full-parent test: accepted scan → transient query failure → repeat invocation, exactly one sbatch total and the original job handle retained.

### R3-2 — should-fix — direct scan submission has no disk usage guard

**Location:** `conformance/jobs/PROD_H_DRAFT/runner/p5_scan_run.sh:58–67`; documented direct final scan in `JOB.md`, step F.

The new submission branch checks the frozen tree and cache, then calls sbatch without `nc_run_guard`. The primary scan normally inherits a guard from `p5_submit.sh`, but the documented final scan invokes this wrapper directly. Consequently a final scan can submit and create home tables/receipts when the charter's home/campaign ceiling check should refuse it. Its header's description as “guarded” is not a usage check.

**Reproduction:** E/scan_probes_corrected.log: direct `p5_scan_run.sh final --no-wait` with a deliberately denying GUARD accepts a stub scan job, returns 10, records one sbatch and **zero guard calls**.

**Concrete fix:** put the real charter-limit guard inside the wrapper's new-job branch, before sbatch, with a planned allowance for its home table/receipt/job record and a preserved small guard receipt. It must cover direct primary/final calls and refuse without sbatch on a failing guard. Rechecking an existing job should not resubmit it.

### R3-3 — minor — an empty results folder cannot receive a manifest

**Location:** `conformance/jobs/PROD_H_DRAFT/runner/make_manifests.sh:48–50`, `:53`, `:63`.

An existing empty p folder produces an empty temporary manifest; `sha256sum -c` exits nonzero because it has no checksum lines. The diagnostic incorrectly suggests a file changed during hashing. This appeared in my minimal killed-P5 fixture after cleanup left its p1000 result folder empty. Normal nonempty production folders succeed. An entirely failed subgroup, represented only in attempt logs/terminal exceptions, needs an explicit transfer representation too.

**Evidence:** E/cleanup_manifest_probe.log: cleanup succeeds, then manifest creation refuses on the empty p1000 folder. E/cleanup_manifest_nonempty.log: with a retained file in each result folder, commit and reuse both return 0, while a later file addition returns 2.

**Concrete fix:** explicitly support/record a zero-file folder and validate its empty membership without invoking checksum verification on an empty manifest (including rerun/post-commit and laptop acceptance checks), or document and implement an explicit terminal-exception transfer path for such folders. Test it separately from the normal nonempty manifest cases.

## Checks and evidence

- E/hash_audit.json and E/final_audit.json: independent manifest/tree/core hashes, exact listed membership, diff reconstruction, and 83 reviewed source/table/document files unchanged against the initial snapshot.
- E/check_A_locale_corrected.log; E/a2_results/: four saved classifier pairs, 27 controls, and the six original review-2 corruptions. E/laneG/results/: F1 23/23, F2 24/24, F3/F7 44/44, F4 22/22. Other lane logs: E/remaining_g.log, E/remaining_g_corrected.log, E/g_f4_locale_corrected.log.
- E/hold_probes.log and E/hold_results.json: original failed-hold reproduction, repeated retries, then confirmed recovery.
- E/scan_full_final.log: end-to-end duplicate-scan reproduction through the actual parent and wrapper. E/scan_probes_corrected.log: direct final scan bypasses the denying disk guard; also an isolated execution of the parent's error handler.
- E/cleanup_manifest_probe.log and E/cleanup_manifest_nonempty.log: terminal attempt proof, archived locks/temps, preserved attempt count, late-folder preflight, safe reuse and inconsistent-manifest refusal, plus the empty-folder edge.
- **Fresh full PROD-H suite: overall exit 0.** Python **51/51**, shell **171/171**, real CLI **6/6**, syntax **27/27**, tables **1/1**. Detached wrapper E/run_suite.sh; launcher PID 44048; log E/run_all.log; persistent exit E/run_all.rc. Fresh summary timestamp **2026-10-29T23:51:02Z**; per-suite logs, vectors and copied shell logs are in E/campaign/conformance/jobs/PROD_H_DRAFT/tests/. Inspected the final summary and individual suite outputs. The run took about 34 minutes before its temporary-fixture pruning; no tool call was held open for the suite.

Setup diagnostics are preserved in E. Initial R child processes inherited the Windows-incompatible `C.UTF-8` locale, causing serialization-derived identity mismatches in CLI controls; reruns with `LC_ALL=LANG=en_US.UTF-8` pass. Initial reviewer drivers also collided with the sourced tests' global `S`/local `d` variables; corrected drivers and final CSVs are the evidence. Early scan-stub attempts lacked the Windows bash adapter or correct squeue output columns; the final full-parent reproduction corrects both. These setup errors are not production findings. No numerical fit was run to repair them.
