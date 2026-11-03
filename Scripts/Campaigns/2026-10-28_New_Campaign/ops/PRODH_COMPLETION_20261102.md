# PROD-H completion report (OPS, 2026-11-02) — run 20261030T0934Z_prodH

Bundle `conformance/jobs/PROD_H` (JOB.md rev 4+, Sol 7; BUNDLE_SHA256SUMS 2a2a8b1f…, 53 files), frozen SMC-BVS v2.2.1 core d880afdb…13e1, p ≫ n regime (n = 200, p ∈ {500, 1000}, S1–S6, r001–r100, c ∈ {1.00, 0.50}). Submitted 2026-10-30 09:36:15Z under HQ D51: precompile **2469859**, primary_p1000 **2469860** (`1-600%30`, 1,200 fits), primary_p500 **2469861** (`601-1200%30`, 1,200 fits). Closed without P5 under HQ D62.

## 1. Reconciliation (reconcile.py --sacct --full-verify, 2026-11-02 03:45Z)

Slurm: precompile + 600 + 600 tasks **COMPLETED** (sacct). Every one of the 2,400 units is finished; none is infra, orphan, timeout, method_failed, rerun-queued or not run.

| p | c | units | ok | of which escalated | resource_limit | infra / orphan / timeout |
|---|---|---:|---:|---:|---:|---:|
| 500 | 1.00 | 600 | 599 | 56 | 1 | 0 |
| 500 | 0.50 | 600 | 600 | 6 | 0 | 0 |
| 1000 | 1.00 | 600 | 597 | 109 | 3 | 0 |
| 1000 | 0.50 | 600 | 598 | 31 | 2 | 0 |
| **Total** | | **2,400** | **2,394** | **202** (+6 resource_limit = 208 escalated) | **6** | **0** |

The six resource_limit fits (all S5, all escalated, native status `resource_limit`: the fitter stopped at its native budget; HPM path recorded, no Z/PIP):

| case | wall s | max RSS | diag codes |
|---|---:|---:|---|
| p1000_S5_r030_c100 | 24,001 | 386,568K | escalated; cut_group; local_certified_false |
| p1000_S5_r044_c100 | 24,000 | 289,732K | escalated; cut_group; local_certified_false |
| p1000_S5_r044_c050 | 24,016 | 414,964K | escalated; cut_group; local_certified_false |
| p1000_S5_r064_c100 | 24,011 | 378,256K | escalated; cut_group; local_certified_false |
| p1000_S5_r064_c050 | 24,015 | 476,700K | grid_unconverged; escalated; cut_group; local_certified_false |
| p0500_S5_r088_c100 | 6,307 | 287,844K | escalated; cut_group; local_certified_false |

**P5 sensitivity: not run (HQ D62, Felipe).** Felipe (2026-11-02): "if the remaining 6 are not done then feel free to kill them, we have enough". No P5 scan or P5 array was ever submitted for PROD-H (accounting `p5`/`p5scan` = 0 tasks). The six stay as recorded primaries, counted as non-recoveries. This deviates from JOB.md §F–G, which assume P5.

## 2. Cost

Final accounting (`final_accounting.sh`, rc 0): **906.49 elapsed core-h, 1,812.98 billed CPU-h** (p500 225.82 / 451.63; p1000 680.67 / 1,361.34; precompile 0.01 billed). JOB.md's estimate was ≈ 920 elapsed core-h; the requested-wall ceiling was 10,541 core-h. Max step RSS: 296.7 MB (p500) and 465.5 MB (p1000).

## 3. Manifests, pull, deletion

| folder | files | bundle MANIFEST sha256 | pulled to `NOTS Data\New_Campaign\` | scratch |
|---|---:|---|---|---|
| results/…/p0500 | 4,800 (+manifest) | 7893396c… | transfer VERIFIED; local `sha256sum -c` OK | deleted 13:20:44Z (remote transfer manifest re-checked) |
| results/…/p1000 | 4,800 (+manifest) | a0196198… | transfer VERIFIED; local OK | deleted 13:35:20Z |
| logs/20261030T0934Z_prodH | 9,611 (+manifest) | 8048e0b8… | transfer VERIFIED; local OK | deleted 13:48:37Z |
| home runs/20261030T0934Z_prodH | HOME_MANIFEST 31 entries | ca245339… | copied 14:08:37Z to `runs\20261030T0934Z_prodH\home_summary\`; local OK | kept on home (summary) |

The `===` timestamps in the pull transcript are pull start times; the deletion times above are from OPS_LOG. Two different manifests are involved, and their hashes are expected to differ. The transfer helper builds a transfer manifest (e.g. 07b85a1b… for p0500), which covers every file including the bundle `MANIFEST.sha256`, and it deletes only after re-checking that transfer manifest remotely. The local `sha256sum -c` then checks the bundle manifest (7893396c…) on the copy.

The first attempt to copy the home summary (13:48:39Z) was refused safely: `nots_pull` will not merge into a non-empty local folder, and `runs\20261030T0934Z_prodH\` already held the staging `bundle\`. It was re-pulled at 14:08Z into the fresh sibling `home_summary\`. Nothing was merged and nothing local was deleted.

**Deviation from JOB.md §H (Sol F1; needs HQ disposition).** JOB.md says: "Neither scratch nor the home run folder is pruned until all four verify locally". OPS instead deleted each scratch folder as soon as that folder's own copy had verified. That is the per-piece rule of PROD-L (HQ D49), wrongly applied by OPS to PROD-H. As a result, the three scratch folders were deleted before the fourth, the home summary, had verified. The home summary's first copy was refused at 13:48:39Z, and its copy verified only at 14:08:37Z. Each deleted folder had been fully copied and verified first, and all four copies now verify. No data was lost. The deviation is procedural. For PROD-H, the home run folder has not been pruned.

**HQ D92 (2026-11-03): accepted** as a disclosed procedural deviation. Every folder verified before its deletion, all four copies verify now, and no data was lost. With all four verified, the PROD-H home run folder is pruned in the D92 final NOTS sweep (archive, Sol check, verified delete). The old upload tar is removed at the same time. Both are logged in `ops/CLEANUP_LOG.md`.

## 4. Reproduction spot-check against the 2026-10-23 production (D51 step 5)

`ops/scaffold/prodh_repro_check.R` (sha256 6d1d7673…a270 at review). The sample is a fixed deterministic grid hard-coded in the script, independent of any fit value. The script was written before the check ran, but no earlier timestamped commitment exists. The grid is: p ∈ {500, 1000} × S1–S6 × r ∈ {1, 25, 50, 75, 100} × c ∈ {1.00, 0.50} = 120 fits, plus all 6 resource_limit cases, for **126 cases and 882 field comparisons**. Each case compares `fit$log_Z`, `fit$log_Z_r`, `fit$hpm`, `fit$pip_primary`, `fit$pip_r`, the record `pip` and `native_status` with R `identical()`. The old fits are in `Documents\NOTS_BVS\smcbvs_v3_deploy_20261022\claude\prod_p{0500,1000}_20261023T1227Z`.

**Result: 882/882 identical, 0 mismatching cases, max |diff| = 0. VERDICT: IDENTICAL.** The check is not vacuous: the 120 sampled fits are `completed` on both sides with real Ẑ, four replicate Ẑ and full PIP vectors. The six resource_limit cases were also `resource_limit` in the 2026-10-23 run. Their Z/PIP estimates are unavailable on both sides (absent fit fields, NA record-PIP placeholders), so equality there carries no numerical information. Their HPM paths are nonempty and match. The record-PIP comparison applies `unname()` first; Sol found strict named identity as well. Invocation: `Rscript prodh_repro_check.R "<PC_NB_ARCHIVE>/smcbvs_v3_deploy_20261022/claude/prod_{p}_20261023T1227Z" <NOTS Data>/New_Campaign/results/20261030T0934Z_prodH <home_summary>/reconcile.tsv ops/evidence/prodh_repro_20261102`. Sol independently re-ran the comparison in memory and also got 126/882 identical. Output: `ops/evidence/prodh_repro_20261102.txt` and `ops/evidence/prodh_repro_20261102/repro_check_detail.tsv`.

## 5. Monitoring cadence (poll.py --cadence)

JOB.md §D asks for a poll every 5–10 min: an interval over 600 s is LATE, and one under 300 s is EARLY. `logs/20261030T0934Z_prodH/polls.jsonl` has **59 polls and 58 intervals: 26 within 300–600 s, 18 late, 14 early**. On these figures **the cadence requirement was not met**. `poll.py --cadence` returned `ok: false`. The `rc=0` printed after it in `ops_finish_h_f3_20261102.txt` is the wrapper's status, not a pass. That transcript also kept only the tail of the JSON, which is why an earlier draft of this report wrongly said that every interval was late. All times below are 2026-10-30 unless stated.

Late intervals (18). The facts come from the poll log. The causes are OPS's account at the time (OPS_LOG); where the log alone cannot tell sleep from a stalled ssh call, that is stated.
- **11:05:50→11:30:14Z (1,464 s):** ssh connection failure followed by the 15-min back-off (BACKOFF lines in the poll log).
- **12:09:58→12:30:23Z (1,225 s):** ssh connection timeouts at 12:14:57Z and 12:18:52Z, each followed by the 15-min back-off (BACKOFF lines in the poll log).
- **13:28:35→14:26:36Z (3,481 s):** OPS account: a T3 restart killed the in-session poller, and it was relaunched at 14:25Z. A third restart came after 14:26Z, and the poller was relaunched detached at 14:38Z.
- **14:26:36→14:38:34Z (717 s) and 14:48:14→14:59:40Z (686 s):** relaunch delay, then sleep plus ssh time.
- **15:47:27→16:21:10Z (2,023 s) and 16:50:20→18:12:28Z (4,928 s):** no poll and no BACKOFF line. OPS_LOG recorded "ssh call stalled … or laptop sleep" at the time, and the log cannot tell the two apart. During the second gap, a relaunch was refused by the PID guard at 18:10:14Z (`EXIT ALREADY_RUNNING pid 1648`).
- **18:12:28Z→20:02:50Z (ten intervals, 606–675 s):** the poller slept 510 s, then made an ssh call that took about 100–165 s. Each interval therefore came out slightly over 600 s. This was a sizing error by OPS. A shorter fixed sleep alone would not guarantee the 600 s bound under slow ssh; the sleep has to be measured from the start of the previous poll.
- **20:02:50Z Oct 30 → 03:08:24Z Nov 2 (198,335 s ≈ 55.1 h):** the laptop slept and the local poller was dead. The poller's last line is `EXIT TIME_UP`, stamped 2026-10-31T19:24:42Z, meaning its 720-min limit ran out. Nothing records why it was stamped then (perhaps a brief wake). Recovery came from disk.

Early intervals (14):
- **11:39:07→13:19:34Z (13 intervals, 210–299 s):** after the T3 restart at about 11:40Z, two pollers overlapped (the old one survived). OPS stopped the extra one at 13:24Z.
- **18:54:17→18:56:51Z (154 s):** an OPS relaunch of the poller around the BENCH_F3_DEV submission attempt (18:57Z). The poll log shows only the two polls.

Remediation, stated exactly. The PROD-H poller (`ops/scaffold/prodh_poller.sh`) still runs ssh with only BatchMode and ConnectTimeout. The stall bound (`ServerAliveInterval=30, ServerAliveCountMax=4`) and the global one-connection lock exist only in the shim `ops/scaffold/sshlock/ssh`. That shim is put first in PATH for processes launched through `ops/scaffold/detach_run.sh` (the 2026-11-02 pull and submission chains). The PID single-instance guard reduces the chance of overlapping pollers. Its check-then-write is not atomic, so it does not guarantee against simultaneous launches; the shim's mkdir lock does serialize ssh itself.

Effect on the run: the monitoring lapses did not hide a failure. The final full-verify reconcile has no unresolved production failure, and the first-200 window was clear at the polls crossing 200 and remains clear in `poll_latest.json`. No hold was raised.

**Transient "infra" counts (Sol F4).** Seventeen mid-run polls reported nonzero infra counts. These include 2 p500 at 14:26Z (gone by 14:38Z), 3 p500 at 14:48Z, and p1000 counts at other times. Because they are per-poll aggregates, they cannot be added up to a number of failed units. `reconcile.py` recomputes `ever_infra` from the current attempt records on every pass. It is not a running union of earlier poll classifications, so the final `ever_infra = 0` means "no unit's attempt record shows an infra failure now", not "no poll ever counted infra". The likely mechanism is a snapshot race: the reconciler snapshots the queue first and then reads accounting and files, so a task that starts in between has an open attempt and no queue entry. This is plausible but not proven case by case, because the poll history keeps no case IDs. Sol checked the final state independently: exactly 2,400 `attempt_1` starts and 2,400 ends, every end `done=true, timed_out=false`, and every reconcile row has one attempt, ever_infra false and no lock. `jobs.tsv` and the accounting show no reruns. Nothing is hidden or missing.

## 6. Remaining housekeeping

- **Deferred, open:** `/scratch/fb31/New_Campaign/upload/prodH_bundle_20261030T0934Z.tar` (720 KB, JOB.md §H) is not removed yet. It goes in the next batched upload clean-up, with a receipt. Closure carries this item.
- The home run folder `runs/20261030T0934Z_prodH` (the summary, 31 manifest entries, no `*.log`/`*.jsonl`) stays on NOTS. Guard after production: home 9.49 GB, campaign home 0.08 GB, OK (`ops/evidence/ops_status_20261102T0305Z.txt:50`).

## 7. Review

Sol 6.1 (high), 2026-11-02: **ACCEPT WITH FIXES** (`review/SOL_REVIEW_PRODH_COMPLETION.md`). F1–F4 were should-fix and are addressed above: F1 as a disclosed deviation awaiting HQ disposition, F2 by the corrected cadence account, F3 by separating facts from causes and stating the remediation exactly, and F4 by the transient-infra explanation. F5 (sampling wording) and F6 (upload tar, guard reference) were notes and are reflected. Sol found no defect in the saved fits, the reconciliation, the accounting, the manifests or the reproduction check.

Raw evidence (ops/evidence): `ops5_prodh_20261030T0934Z_{gates,stage,upload,submit}.txt`, `ops5_prodh_20261030T0934Z_poll.log`, `ops_status_20261102T0305Z.txt`, `ops_reconcile_20261102.txt`, `ops_finish_h_f3_20261102.txt`, `ops_pulls_20261102.txt`, `ops_pulls2_20261102.txt`, `prodh_repro_20261102*`. The transfer receipts are in `ops/transfer/receipts/`.
