# Independent review: PROD-H completion

Verdict: **ACCEPT WITH FIXES**. The production results and reproduction comparisons are supported. Correct the monitoring narrative and disclose the download/deletion sequencing deviation before declaring procedural closure. No blocking defect in the saved fits was found. P5 omission is accepted under the explicitly supplied HQ D62 authorization.

Reviewed 2026-11-02, read-only except for this file. No SSH, NOTS connection, simulations, or production workloads were run. Local work consisted of evidence inspection, metadata checks, limited SHA-256 checks, and the expressly authorized R validation. No other file was written. Paths below use CAMP for the campaign, HOME for `NOTS Data/New_Campaign/runs/20261030T0934Z_prodH/home_summary`, RESULTS for the corresponding local results folder, and LOGS for the corresponding local logs folder. Report line references are to the reviewed version of `ops/PRODH_COMPLETION_20261102.md`.

## Findings

### F1 — should-fix: acknowledge the all-four-verification sequencing deviation

References: report:38–43; HOME/JOB.md:142; CAMP/ops/evidence/ops_pulls_20261102.txt:1–20; ops_pulls2_20261102.txt:1–4; CAMP/ops/OPS_LOG.md:109–117.

Each scratch folder was copied and verified by the transfer helper before that folder was deleted, with a fresh remote transfer-manifest check. This supports safe preservation of those folders. However, JOB.md explicitly says **neither scratch nor home is pruned until all four folders verify locally**. Scratch deletion occurred at 13:20:44Z, 13:35:20Z, and 13:48:37Z; the first home pull then failed at 13:48:39Z, and the home copy verified only at 14:08:37Z. Moreover, the printed bundle-manifest acceptance lines follow the respective deletion lines, although the helper had already verified all copied files against its transfer manifest.

The eventual four copies are intact; this is a procedural deviation, not evidence of data loss. Explicitly record the deviation and obtain HQ disposition for closure. Distinguish the helper's transfer manifest from the bundle's MANIFEST.sha256: their different hashes are expected, because the transfer inventory includes the bundle manifest itself. The report's deletion times match OPS_LOG; the pull transcript's section timestamps are start times, not deletion times.

### F2 — should-fix: correct and complete the cadence account

References: report:53–59; CAMP/ops/evidence/ops5_prodh_20261030T0934Z_poll.log:68–70, 120–132, 203–217, 288–362; LOGS/polls.jsonl; HOME/runner/poll.py:128–148; CAMP/ops/evidence/ops_finish_h_f3_20261102.txt:33–36.

The saved JSONL has **59 polls / 58 intervals: 18 late, 14 early, 26 within 300–600 s**. Thus “Every interval recorded by --cadence is flagged late” is false for the complete cadence result. The saved completion transcript starts partway through its JSON, apparently retaining only the late-list tail, and prints rc=0 despite `ok:false`; the actual poll.py CLI exits 1 for that result. Do not treat that wrapper status as successful cadence compliance.

The report omits the **12:09:58Z–12:30:23Z gap (1,225.000175 s)**. The local poll log explicitly records connection timeouts and 15-minute backoffs at 12:14:57Z and 12:18:52Z. Add this explanation. Correct the next long-gap endpoint from approximately 14:25Z to **14:26:36Z** (3,480.788112 s). The long final interval is correctly approximately 55 hours: 198,334.519849 s, or 55.093 h.

The sleep-510 explanation is plausible for the later 606–717 s intervals, but many earlier intervals were compliant. Describe the later pattern rather than implying every poll exceeded 600 s. The early-poll list also includes the 18:54:17Z–18:56:51Z relaunch interval (153.840393 s), outside the stated overlap window. Preserve a complete cadence summary, including the noncompliant result, and explain all late gaps to HQ as JOB.md requires.

### F3 — should-fix: separate evidenced monitoring facts from inferred causes and unsupported remediation claims

References: report:56–61; CAMP/ops/OPS_LOG.md:92–94, 98; CAMP/ops/scaffold/prodh_poller.sh:18–23, 36; local poll log:288, 362.

The log establishes gaps, backoffs, a PID-guard rejection at 18:10:14Z, and a final `EXIT TIME_UP` stamped 2026-10-31T19:24:42Z. It does not by itself distinguish sleep from a stalled SSH session. OPS_LOG:94 explicitly says “ssh call stalled ... or laptop sleep”; the report upgrades this to a definite stall. Restart/sleep explanations can be attributed to OPS's contemporaneous account, but should not be presented as independently proved by the poll log. “None of the gaps affected the outcome” should be narrowed to the supported observation that final reconciliation found no unresolved production failures and the first-200 window was clear.

The assertion “All pollers now use ServerAliveInterval=30, CountMax=4” is not supported by the available PROD-H poller: its SSH invocation still has only BatchMode and ConnectTimeout. Its PID check/write is also not atomic, so it reduces accidental overlap but does not guarantee prevention of simultaneous launches. Cite the actual updated artifact/configuration if one exists, or qualify these claims. A shorter fixed sleep alone would not guarantee a 600 s bound under slow SSH.

### F4 — should-fix: explain transient infra counts without implying ever_infra is a persistent incident counter

References: report:61; local poll log:90, 156, 186, 198, 211, 223, 259, 296, 345; HOME/runner/reconcile.py:159–181, 205–258; LOGS/attempts; HOME/reconcile.tsv.

The stated two p500 infra classifications at 14:26Z are real and disappear by 14:38Z, but they were not the only transient classifications: **17 polls** report nonzero infra, including three p500 at 14:48Z and p1000 classifications at other times. These aggregate counts cannot be added to obtain unique failed units.

Final ever_infra=0 is consistent with the code and saved final evidence. The reconciler first snapshots the queue, then reads accounting and files. A newly starting task absent from that earlier queue snapshot can have an unfinished attempt and be classified infra. It recomputes ever_infra from current attempt records on every pass; it does not retain a historical union of previous poll classifications. This is a plausible snapshot race, not a proven diagnosis of each individual transient case, because the aggregate poll history does not preserve those case identities.

Independent inspection found exactly **2,400 attempt_1 starts and 2,400 ends**, every end with `done=true` and `timed_out=false`; every reconcile row has one attempt, ever_infra=false, and no lock. jobs.tsv and accounting show no reruns. Therefore this is not evidence of hidden final failures or missing work. Expand the narrative to cover the transient pattern and explain what final ever_infra=0 actually means. The first-200 window was clear at the polls crossing 200 and remains clear in poll_latest.json; no unacknowledged hold is shown.

### F5 — note: reproduction is sound, but chronological preregistration is not established

References: report:47–49; CAMP/ops/scaffold/prodh_repro_check.R:2–14, 19–28; CAMP/ops/evidence/prodh_repro_20261102.txt; corresponding repro_check_detail.tsv; CAMP/ops/OPS_LOG.md:124.

The 120-case grid is explicitly hard-coded and independent of fit values; the six extra cases are selected by the declared resource_limit rule. There is no filtering on agreement. However, the supplied artifacts do not establish when that grid was chosen relative to inspecting old/new results. The script's comment “fixed, not data-driven” establishes the mechanism, not chronological preregistration. Prefer “fixed deterministic grid in the comparison script,” or cite a timestamped earlier commitment if “fixed in advance” is intended to mean before examining results. Preserve the exact invocation and script hash with the check output.

`identical()` is appropriate for an exact reproducibility claim: it detects numerical, type, shape, and attribute differences. The record-level pip comparison explicitly applies `unname()` first, so the report should state that exception to strict object identity. My independent check also found strict named pip identity for these 126 cases, so that qualification does not change this result.

The checked script uses exact `[[f]]` lookup for fit fields. Missing/NULL values can compare identically, and its numeric maximum discards NA, so “max difference 0” alone would be insufficient. This is not a vacuous check here: independently reading all 126 pairs confirmed the 120 completed cases have finite scalar log_Z, four finite log_Z_r values, nonempty HPM, primary and record PIP vectors of length p, and nonempty replicate PIPs (length 4p). Resource-limit records carry absent fit Z/PIP estimates and NA record-PIP placeholders, with nonempty matching HPM. Describe those as unavailable estimates rather than useful numerical equality.

### F6 — note: upload-tar housekeeping remains; home budget is supported

References: report:65–66; HOME/JOB.md:183, 186; CAMP/ops/evidence/ops_status_20261102T0305Z.txt:50.

The retained upload tar is openly disclosed, so the report does not yet demonstrate complete JOB.md cleanup. Retire it in the authorized later cleanup and record the receipt, or carry the explicit deferred item in closure. No deletion was attempted in this review. The saved post-production guard output is OK (home 9.49 GB, campaign_home 0.08 GB); the copied home run has no *.log or *.jsonl files. Include this evidence reference beside the budget statement rather than leaving it implicit.

## Verified completion evidence

- Reconcile contains exactly 2,400 unique case IDs, all `done`. Four p-by-c cells each have 600 units. Counts `(ok, escalated among ok, resource_limit)` are p500/c100 `(599,56,1)`, p500/c050 `(600,6,0)`, p1000/c100 `(597,109,3)`, p1000/c050 `(598,31,2)`. Total 2,394 ok, 202 escalated ok, six escalated resource_limit = 208 escalated overall. All six case IDs, wall seconds, RSS and diagnostic strings match the report. The six FAILED unit steps are native resource_limit outcomes; they are not array-task failures or hidden infra failures.
- Recomputed raw parent-job accounting, avoiding step double-counting: p500 elapsed 225.816111 h / allocated 451.632222 h; p1000 680.671944 / 1361.343889; precompile 0.003889 / 0.007778. Totals round to **906.49 elapsed core-h / 1,812.98 billed CPU-h**. All 1+600+600 parent tasks are COMPLETED. Both ceilings, group maxima, and zero P5/P5scan/rerun tasks agree with core_hours.json and the completion transcript.
- Local file inventories match summary.tsv exactly: p0500 4,800 files / 1,159,639,427 bytes; p1000 4,800 / 3,032,338,384; logs 9,611 / 3,119,468, excluding each manifest. Each results folder has 1,200 case folders. Transfer counts include the manifests (4,801 / 4,801 / 9,612). Home transfer has 54 files, while HOME_MANIFEST deliberately covers 31 entries, excluding runner/ and itself.
- Independently hashed manifests: p0500 `7893396cbebb12e29201295b6c9b6f69e9e7f62587765a34ea80414d3c486163`; p1000 `a019619848e90a6c9213a3e07d6f83af218bb58bba275a5b47ea2b5757acab76`; logs `8048e0b82d32edefde0a8e1204bdc1b6f4ae231e69e09782c06fb25678c1f9a6`; home `ca2453397154f6353bc34f77302c321744a82ddb7977a6a87132f6f2931f11cc`. All match the raw evidence and report prefixes.
- All 31 HOME_MANIFEST entries rehashed successfully. Nine scratch-file spot checks passed (first/middle/last manifest entries per folder). I did not rehash the multi-GB result trees. Full-tree acceptance is supported by the saved transfer VERIFIED receipts and LOCAL_BUNDLE_MANIFEST_OK lines; current independent checks are explicitly limited to inventory, manifests, and spot hashes.
- Independently reran the comparison logic read-only, entirely in memory with R 4.4.1 `--vanilla -`; no output directory or data file was created. All **126 cases / 882 comparisons passed**, and saved detail TSV has exactly the same sample IDs and 882 TRUE rows. Paths were distinct and correct: old `<PC_NB_ARCHIVE>/smcbvs_v3_deploy_20261022/claude/prod_p{0500,1000}_20261023T1227Z/p{0500,1000}/<case>/SMCBVS.rds`; new `RESULTS/p{0500,1000}/<case>/SMCBVS.rds`. The script's OLD_ROOT must contain the literal `{p}` placeholder (expanded to p0500/p1000). Script SHA-256 at review: `6d1d7673d5aab22892e22b75adc310126faf39bd3f8be7a71c76d1ce32e9a270`.
- Full-verify reconciliation rc=0, final accounting rc=0, manifest creation rc=0, and cleanup dry-run showing zero stale/unproven artifacts are saved. No cleanup mutation was necessary. D62 explains the absent P5 scan/retry/final-report artifacts; they should not be reported as completed P5 work.

Acceptance is conditional on F1–F4 being addressed in the closure report/HQ disposition. F5–F6 document limits and follow-through; none calls for rerunning the production campaign.
