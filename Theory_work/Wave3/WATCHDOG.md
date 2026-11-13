# Wave 3 watchdog log (PROTOCOL rule 12)

Independent check on Theory HQ. Each run appends one timestamped section: OK, or the flags.

## 2026-11-11 21:02 UTC (15:02 CT) — OK

Thresholds: checkpoint unanswered > 6 h; ticket silent > 3 h without a final report; P6 > 1,200 core-h (early warning,
fail-closed hold) / > 1,400 core-h (ceiling).

**(a) Tickets**
| ticket | branch @ head | last LOG entry | open checkpoint | status |
|---|---|---|---|---|
| W3-P6 | theory/W3-P6 @ 8c63542 | 14:02 CT (1 h 00 m ago) | CHECKPOINT_0 (14:02–14:05 CT, commit 8c63542), no HQ decision yet: open ≈ 1 h | OK (< 6 h); waits for HQ/owner on the smoke manifest (S3 in/out) and the ceiling-unit decision |
| W3-START | theory/W3-START @ 58309da | 13:43 CT (1 h 19 m ago) | none: CP1 answered (HQ decision 13:43 CT, checkpoint commit d4e4c6e) | OK; waits for the owner's leg-B go |
| W3-MEMO-SCR-RM | theory/W3-MEMO-SCR-RM @ 20bf513 | 11:55 CT (3 h 07 m ago) | none | OK: complete (MEMO.md v2 delivered; HQ decision "done", adopt (a), main d784448). Silent > 3 h but finished, not stalled |
| W3-RM2 | no branch, no folder | — | — | not started |

Other theory/W3-* branches (origin only: W3-PGD, W3-PXN, W3-VEXP, W3-VT37R, W3-VT38E) were last committed 2026-11-02:
earlier work, not active Wave 3 tickets. No new theory/W3-* branch.

**(b) HQ_DECISIONS.md:** last entry "W3-START CP1" (entries carry a date only); its commit ca7b54b is 2026-11-11 13:54 CT
(19:54 UTC), 1 h 08 m ago.

**(c) W3-P6 spending** (NOTS, read-only `sacct`): job ids from LOG/CHECKPOINT_0: probe01 2647903, b1 2651495,
smoke_v3 2652108, b2 2652199.
- `sacct -S 2026-11-11`, w3p6_: **0 allocations, 0.00 core-h** (nothing submitted since the resume; matches CP0 "nothing
  submitted").
- Cross-check, `sacct -S 2026-11-09`: 381 allocations, **495.88 core-h** (equals CHECKPOINT_0 §2).
- Both below 1,200: no hold. HOLDS.md has no `HOLD P6` line.

Note for HQ (not a flag): on the cumulative measure P6 starts its resume at 495.88 core-h; CHECKPOINT_0 §6.1 asks HQ to
choose the ceiling unit. This watchdog's query counts from 2026-11-11 only, so it will not see the pre-resume 495.88.

No flags. Nothing sent to HQ.

## 2026-11-12 10:17 UTC (04:17 CT) — FLAGS (3)

Thresholds: checkpoint unanswered > 6 h; ticket silent > 3 h without a final report; P6 total since 2026-11-09
> 1,700 core-h (early warning, fail-closed hold) / > 1,896 core-h (ceiling).

**Flags**
1. **W3-P6 silent 11 h 24 m, no final report.** Last LOG entry 2026-11-11 16:53 CT (22:53 UTC, smoke submitted; branch
   @ 3d73164). Context (HQ_NOW 10:05 UTC): waiting on smoke task 4; heartbeat should re-wake the lead. NOTS now: S1, S2,
   S3 and S4 COMPLETED (smk1_v2 1/1, smk1_v3 3/4); smk1_v3 task 4 (S5, (100,1000)) RUNNING (22.79 core-h so far, about 11.4 h of its 24 h
   limit). LOG has no entry for the S1–S4 completions; the summarize.py v3 diff still awaits its rule-15 review.
2. **W3-MISR silent 4 h 47 m, no final report.** Last LOG entry 23:30 CT (05:30 UTC: REPORT, MANIFEST_R1, council
   launched; branch @ 2f360ed). Context: CW limit stop; HQ resumed MISR ~10:05 UTC. On disk, uncommitted and not in the LOG: R1
   council sol 9.3 PASS (23:35 CT), R1 council opus 8.7 PASS (04:14 CT), both on manifest d3f5c91f…. Council result not
   yet logged.
3. **W3-START CHECKPOINT_3 (R2) has no HQ decision in the ticket LOG; open 8 h 45 m** (CHECKPOINT_3.md 19:32 CT = 01:32
   UTC; leg-D commit 9715aef; branch @ 808ddd1). The LOG ends with the HQ-delegate audit (REFUSED, 23:05 CT) and "HQ
   decides §7.1 (T) vs (R3)". The decision exists only in HQ_DECISIONS (option (T) → INFRA R05; main c8a970f, 05:06 UTC).
   This is a gap in the LOG record. The ticket waits on R05 (branch infra/R05-ckpt-status @ b0c21b0). REPORT.md exists, so the
   silence rule does not apply.

**(a) Tickets**
| ticket | branch @ head | last LOG entry | open checkpoint | status |
|---|---|---|---|---|
| W3-P6 | theory/W3-P6 @ 3d73164 | 11-11 16:53 CT (11 h 24 m) | none: CP0 answered (HQ CP0 APPROVED, commit 80e6acd, in LOG) | FLAG 1 |
| W3-START | theory/W3-START @ 808ddd1 | 11-11 23:05 CT (delegate audit; 5 h 12 m) | CP3 (R2): decision not in LOG (see flag 3); CP1, CP2 answered in LOG | FLAG 3 |
| W3-MEMO-SCR-RM | theory/W3-MEMO-SCR-RM @ 20bf513 | 11-11 11:55 CT | none | OK: complete (memo v2; HQ "done", d784448) |
| W3-RM2 | theory/W3-RM2 @ c2257ab (+ uncommitted LOG/lemma edits) | 11-12 04:08 CT (9 m) | none: CP1, CP2 answered (CP2: c2257ab, HQ 23:10 CT, in LOG) | OK; Form R leg → CP3 |
| W3-MISR | theory/W3-MISR @ 2f360ed | 11-11 23:30 CT (4 h 47 m) | CP1 (1c97184, 23:21 CT): pre-approved by HQ (HQ_DECISIONS, 16a7f85) | FLAG 2 |
| W3-PSHARP | theory/W3-PSHARP @ daafaa5 | 11-12 04:15 CT (2 m) | CP1 (04:14 CT): pre-approved, reviews clean | OK; CP2 line checks running |
| W3-SCALE | theory/W3-SCALE @ b2c0194 | 11-12 04:15 CT (2 m) | CP1 (b2c0194): HQ ACCEPTED in HQ_DECISIONS (f1da482, 10:07 UTC); not yet in ticket LOG (10 min) | OK |

Old origin-only theory/W3-* branches (PGD, PXN, VEXP, VT37R, VT38E): last committed 2026-11-02, not active.

**(b) HQ_DECISIONS.md:** last entry "W3-SCALE CP1 ACCEPTED", labelled "~10:40 UTC"; commit f1da482 at 10:07:45 UTC
(10 min ago). Note: this label, and the label "~05:40 UTC" on the W3-START entry (commit c8a970f 05:06 UTC), are later than their commit times by
~33 min. The labels look offset; please check the clock used for them.

**(c) W3-P6 spending** (NOTS, read-only `sacct -S 2026-11-09`, w3p6_): job ids from LOG: probe01 2647903, b1 2651495,
smoke_v3 2652108, b2 2652199, smk1_v2 2689422, smk1_v3 2689423. 386 allocations, **571.72 core-h** total
(pre-pause 495.88 + since resume 75.84: smk1_v2 3.92, smk1_v3 49.13 done + 22.79 running). Smoke worst case
at the running task's 24 h limit ≈ 597 core-h (CP-ledger worst case 695.88). Below 1,700 and below 1,896: no hold.
HOLDS.md has no `HOLD P6` line.

Flags sent to HQ (thread 647bfd65…).

## 2026-11-12 15:03 UTC (09:03 CT) — FLAGS (1)

Thresholds: checkpoint unanswered > 6 h; ticket silent > 3 h without a final report; P6 total since 2026-11-09
> 1,700 core-h (early warning, fail-closed hold) / > 1,896 core-h (ceiling).

**Flags**
1. **W3-P6 silent 4 h 43 m, no final report.** The last LOG entry is the HQ note of 2026-11-12 04:20 CT (10:20 UTC; branch @
   2694592, which says the lead is idle by design until S5 ends). NOTS now: S5 (2689423_4, (100,1000)) still RUNNING, 32.35 core-h
   = about 16.2 h of its 24 h limit, so it ends by about 16:50 CT at the latest. The summarize.py v3 rule-15 review and
   CHECKPOINT_1 are still pending.

**Notes (not flags)**
- Timestamps ahead of the clock: W3-START2 LOG entries are labelled 09:30, 11:00 and 12:40 CT, but LOG.md was last written
  at 07:59 CT and it is now 09:03 CT. The HQ_DECISIONS entry "~09:30 CT acceptance audit" was committed in 849dfb5 at
  07:53 CT. Please check the clock used for these labels (see the label offset noted at 10:17 UTC).
- Checkpoint decisions that are in HQ_DECISIONS but not yet in the ticket LOG (all under 6 h). They reach 6 h at about
  16:30 UTC: W3-RM2 CHECKPOINT_3 (04:29 CT; HQ acceptance-audit decision (3), 849dfb5), W3-MISR CHECKPOINT_3 (04:33 CT;
  HQ "CP3 final", 97748d7), W3-PSHARP CHECKPOINT_3 (07:28 CT; 755bba5). W3-START2 CHECKPOINT_2 (07:59 CT, uncommitted)
  has no HQ decision yet (1 h 04 m).

**(a) Tickets**
| ticket | branch @ head | last LOG entry | open checkpoint | status |
|---|---|---|---|---|
| W3-P6 | theory/W3-P6 @ 2694592 | 11-12 04:20 CT (HQ note; 4 h 43 m) | none: CP0 answered (80e6acd, in LOG) | FLAG 1 |
| W3-START | theory/W3-START @ 0938c08 | 11-12 04:20 CT (HQ CP3 decision, 9715aef, in LOG) | none | OK: REPORT; R05 merged (3ce2e27); acceptance ACCEPTABLE; waits on R06 → `--record` |
| W3-MEMO-SCR-RM | theory/W3-MEMO-SCR-RM @ 20bf513 | 11-11 11:55 CT | none | OK: complete |
| W3-RM2 | theory/W3-RM2 @ 5a1199b | 11-12 04:33 CT (CP3-PASS) | CP3: decision in HQ_DECISIONS only (4 h 34 m) | OK: REPORT; see note |
| W3-START2 | theory/W3-START2 @ 2c66e61 (+ uncommitted CP2, REPORT) | labelled 12:40 CT; file 07:59 CT (1 h 04 m) | CP2 (07:59 CT): no decision yet; CP1 answered in LOG (2c66e61) | OK; see notes |
| W3-MISR | theory/W3-MISR @ 4437ecd | 11-12 04:35 CT (CP3; end of run) | CP3: decision in HQ_DECISIONS only (4 h 30 m) | OK: REPORT; see note |
| W3-PSHARP | theory/W3-PSHARP @ 11524d0 | 11-12 07:30 CT (CP3-PASS) | CP3: decision in HQ_DECISIONS only (1 h 35 m) | OK: REPORT |
| W3-SCALE | theory/W3-SCALE @ 5f1d109 | 11-12 07:34 CT (1 h 29 m) | none: CP1 ACCEPTED, in LOG | OK: B3 2698177-80 running |

**(b) HQ_DECISIONS.md:** the last entry is the acceptance audit (labelled "~09:30 CT"). Commit 849dfb5 is at 07:53 CT (13:53 UTC),
1 h 10 m ago.

**(c) W3-P6 spending** (NOTS, read-only `sacct -S 2026-11-09`, w3p6_). Job ids from the LOG: probe01 2647903, b1 2651495,
smoke_v3 2652108, b2 2652199, smk1_v2 2689422, smk1_v3 2689423. 386 allocations (314 COMPLETED, 71 CANCELLED, 1 RUNNING),
**581.28 core-h** in total: pre-pause 495.88 + 85.40 since the resume (smk1_v2 3.92, smk1_v3 81.48 incl. S5 32.35 running).
Worst case at S5's 24 h limit ≈ 597 core-h. This is below 1,700 and below 1,896, so no hold. HOLDS.md has no `HOLD P6` line.

Flags sent to HQ (thread 647bfd65…).

## 2026-11-12 21:02 UTC (15:02 CT) — FLAGS (2)

**Flags**
1. **W3-SCALE: no LOG entry for 7 h 28 m, no final report.** Last entry 07:34 CT (branch theory/W3-SCALE @ 5f1d109,
   worktree clean). Since then (NOTS sacct, read-only): 5k profile 2692690 COMPLETED (12:13:50); B3 p2000 2698177
   COMPLETED (05:24:10); B3 p5000/p10000/p20000 2698178-80 RUNNING (7:30 elapsed; limits 16:00 / 11:00 / 16:00).
   No read-back logged and no CP2 yet.
2. **W3-START2 CHECKPOINT_2: no HQ decision in the ticket LOG, about 7 h.** CP2 has existed since 07:59 CT (file
   time; seen uncommitted at the 09:03 CT run; committed in 70c8e7f at 10:05 CT). The decision exists in substance:
   START2 was recorded on main (2d2b255, HQ_DECISIONS "afternoon" entry). Only the LOG line with the checkpoint commit
   hash is missing, on the branch and on main.

**Notes (not flags)**
- W3-P6 returned to HQ at 13:23 CT (uncommitted LOG line, 1 h 39 m ago; no CHECKPOINT file). Finding: cascadelake
  (bc12*) nodes are about 1.7–2× slower than the sapphirerapids nodes of the smoke run. s1_c and s1_b (all 18 tasks on
  bc12) are likely to hit their 12:10 / 10:00 limits with no RDS (about 400 core-h lost). Lead released nothing further
  (s1_e held). No HQ reply in the LOG yet.
- W3-PATH: branch theory/W3-PATH @ bd2b95c (10:29 CT) holds only BRIEF.md, with no LOG. HQ_DECISIONS 10:29 CT says
  "LAUNCHED", but the 12:00 CT plan says "not launched yet". Treated as not active. HQ should confirm which is true.

**(a) Tickets**
| ticket | branch @ head | last LOG entry | open checkpoint | status |
|---|---|---|---|---|
| W3-P6 | theory/W3-P6 @ 5795185 (+ uncommitted LOG) | 11-12 13:23 CT (1 h 39 m) | none: CP1 answered in LOG (703a6b2) | OK; see note |
| W3-START | theory/W3-START @ e3bc846 | 11-12 04:20 CT (HQ CP3 decision) | none | OK: REPORT; recorded on main a3404b3 |
| W3-MEMO-SCR-RM | theory/W3-MEMO-SCR-RM @ 20bf513 | 11-11 11:55 CT | none | OK: complete (HQ decision (a)) |
| W3-RM2 | theory/W3-RM2 @ cc0b28e | 11-12 09:05 CT (HQ CP3 decision, 5a1199b) | none (CP4 = HQ acceptance record) | OK: REPORT; recorded 223f8e4 |
| W3-START2 | theory/W3-START2 @ 35b9039 | file 07:59 CT (last entry labelled 12:40 CT) | CP2: no decision in LOG | FLAG 2 |
| W3-MISR | theory/W3-MISR @ 0e700bd | 11-12 09:05 CT (HQ CP3 decision, 4437ecd) | none (CP4 = HQ acceptance record) | OK: REPORT; recorded 81b0131 |
| W3-PSHARP | theory/W3-PSHARP @ 3bf0530 | 11-12 09:05 CT (HQ CP3 decision, 11524d0) | none (CP4 = HQ acceptance record) | OK: REPORT; recorded 07ee8b0 |
| W3-SCALE | theory/W3-SCALE @ 5f1d109 | 11-12 07:34 CT (7 h 28 m) | none: CP1 accepted, in LOG | FLAG 1 |
| W3-PATH | theory/W3-PATH @ bd2b95c | no LOG | none | not active; see note |

**(b) HQ_DECISIONS.md:** last entry "2026-11-12 afternoon" (all five tickets recorded). It was committed in 62e6d8a at
13:21 CT (19:21 UTC), 1 h 41 m ago.

**(c) W3-P6 spending** (NOTS, read-only `sacct -S 2026-11-09`, w3p6_). Job ids from the LOG: 2647903, 2651495, 2652108,
2652199, 2689422, 2689423, 2699408, 2699410-14. There are 440 allocations (336 COMPLETED, 71 CANCELLED, 33 RUNNING).
**953.75 core-h** in total, counting the time the 33 running tasks have used so far (4:40 elapsed, 2 cores each). Of
that, 495.88 was spent before the pause and 457.87 since the resume. Finished work comes to 645.37 core-h, and the
running tasks add 308.39. s1_b1r 2699414 COMPLETED 63.50. Running: d1 46.73, h1 46.73, h2 46.73, c 84.11, b 84.11.
The total is below 1,700 and below 1,896, so no hold is set. HOLDS.md has no `HOLD P6` line.
At every Slurm limit, the worst case is 645.37 + 1,119 = 1,764.4 core-h. That is above the 1,700 early warning and
below the 1,896 ceiling. Running at the limits, the actual total would pass 1,700 at about 21.9 h of job elapsed time
(about 14:20 UTC on 11-13), and only if d1/h1/h2 run to their 24 h limits.

Flags sent to HQ (thread 647bfd65…).

## 2026-11-13 03:03 UTC (2026-11-12 21:03 CT) — FLAGS (1)

Thresholds: checkpoint unanswered > 6 h; ticket silent > 3 h unless idle by design; P6 > 1,880 core-h (stage-1 hold
line, HQ 2026-11-12) / 1,896 (ceiling).

**Flags**
1. **W3-P6: no LOG entry for 5 h 57 m** (last 15:06 CT, N2.5 node types). That entry does not say the run ended or that
   the lead is idle while NOTS runs. HQ_NOW gives a 3-hourly P6 watcher, but no watcher entry has been logged since
   15:06 CT (a wake was due about 18:06 CT). In substance nothing is pending: no w3p6 task has finished since 15:06 CT
   (see (c)). The next events are c_hw at its 12:10 limit (~6.2 h from now at the latest), and d1 1–3 / h1 / h2 (13.3 h
   left at most). s1_b_hw (180) is still waiting for headroom. HQ should log that the lead is idle by design, or wake
   the watcher.

**Notes (not flags)**
- W3-SCALE: last LOG 15:06 CT (5 h 57 m), "Run ends here (HQ re-wakes when they end)", so idle by design. NOTS
  (read-only): B3 p = 10k 2698179 COMPLETED at 18:01 CT (10.49 h of 11:00); p = 5k 2698178 and 20k 2698180 RUNNING
  13.5 h of 16:00. HQ re-wakes after the last one ends (≤ 2.5 h).
- W3-PATH: still only BRIEF.md (bd2b95c), no LOG. Not active (HQ correction 15:10 CT: scoping starts Mon 11-16).

**(a) Tickets**
| ticket | branch @ head | last LOG entry | open checkpoint | status |
|---|---|---|---|---|
| W3-P6 | theory/W3-P6 @ 65b22a2 (clean) | 11-12 15:06 CT (5 h 57 m) | none: CP0 (80e6acd) and CP1 (703a6b2) answered in the LOG | FLAG 1 |
| W3-SCALE | theory/W3-SCALE @ 31183a2 (clean) | 11-12 15:06 CT (5 h 57 m) | none: CP1 accepted, in the LOG; CP2 not written yet | OK: idle by design |
| W3-PATH | theory/W3-PATH @ bd2b95c | no LOG | none | not active |

**(b) HQ_DECISIONS.md:** the last entry is "2026-11-12 ~15:30 CT W3-P6 hardware" (labelled ~15:30; committed in 8a24827
at 15:04:51 CT). That was 5 h 58 m ago.

**(c) W3-P6 spending** (NOTS, read-only `sacct -S 2026-11-09 -X`, w3p6_, 03:02 UTC). There are 451 allocations (336
COMPLETED, 91 CANCELLED, 24 RUNNING). **1,241.94 core-h** in total, counting what the running tasks have used so far.
Finished work is 834.16 core-h, which matches the LOG's 834.165, and running tasks add 407.78. Running now: s1_d1 1–3
(bb*, 10:40 elapsed) 64.00; s1_h1 and s1_h2 (bc12*, 10:40) 213.33; s1_d1hw (bb*, 5:56) 23.71; s1_c_hw (bb*, 5:56)
106.72. No w3p6 job is PENDING, and no job id appears that is missing from the LOG.
If every running task hits its Slurm limit, the worst case is 1,241.94 + 531.3 = **1,773.2 core-h**, which matches the
LOG's L = 1,773.165. That is below 1,880 and 1,896. The total stays below the hold line unless s1_b_hw or later work is
released. Releasing s1_b_hw now (+180) would put L at about 1,953, above the ceiling. The lead has said it will wait,
which is correct.
P6 is below 1,880, so no hold is set. HOLDS.md has no `HOLD P6` line.

Flag sent to HQ (thread 647bfd65…).

## 2026-11-13 09:02 UTC (03:02 CT) — OK

Thresholds: checkpoint unanswered > 6 h; ticket silent > 3 h unless idle by design; P6 > 1,880 core-h (stage-1 hold
line, HQ 2026-11-12) / 1,896 (ceiling).

**No flags.**

**(a) Tickets**
| ticket | branch @ head | last LOG entry | open checkpoint | status |
|---|---|---|---|---|
| W3-P6 | theory/W3-P6 @ 38f0163 (LOG.md modified, uncommitted) | 11-13 01:09 CT (1 h 53 m), s1_b_hw submitted | none: CP0 (80e6acd) and CP1 (703a6b2) answered in the LOG | OK |
| W3-SCALE | theory/W3-SCALE @ 31183a2 (LOG, DESIGN_v1, b3_census.tsv modified; CHECKPOINT_2.md and analysis/b3_census_table.R untracked) | 11-13 01:12 CT (1 h 50 m), "CHECKPOINT_2.md written … Stop: end of leg B" | **CHECKPOINT_2.md** (01:11 CT), no HQ decision yet: 1 h 51 m old | OK: waiting on HQ |
| W3-PATH | theory/W3-PATH @ bd2b95c | no LOG (only BRIEF.md) | none | not active (scoping starts Mon 11-16) |

**(b) HQ_DECISIONS.md:** the last entry is still "2026-11-12 ~15:30 CT W3-P6 hardware" (committed in 8a24827 at 15:04:51 CT),
about 11.5 h ago. Nothing is overdue: the only open checkpoint is SCALE CP2. That crosses the 6-h line at about 07:11 CT
(13:11 UTC).

**(c) W3-P6 spending** (NOTS, read-only `sacct -u fb31 -S 2026-11-09 -X`, w3p6_, 09:02 UTC). There are 460 allocations
(356 COMPLETED, 91 CANCELLED, 13 RUNNING, 0 PENDING). **1,455.96 core-h** in total, counting what the running tasks
have used so far. Finished work is 1,307.83 core-h, and running tasks add 148.13.
- Since the lead's 01:09 CT entry (finished 1,111.70), six tasks completed: s1_d1 1 and 3 at 02:10 and 02:54 CT
  (sapphirerapids, 15.8 h and 16.5 h); s1_h1 1, 2, 3 and 5 at 02:41–03:01 CT (cascadelake, 16.3–16.65 h, no Slurm kill).
  The lead has not logged them yet. They ended less than 1 h ago, so the 3-hourly watcher should pick them up.
- Running: s1_d1 2 (bb*, 16:40); s1_h1 4 (bc12*, 16:40); s1_d1hw 1–2 (bb*, 11:56); s1_b_hw 1–9 (bb*, 1:53). Every job id
  is in the LOG.
- If every running task hits its Slurm limit, the worst case is 1,455.96 + 223.87 = **1,679.8 core-h**. That is below
  1,880 and 1,896. No hold is set, and HOLDS.md has no `HOLD P6` line.
- Note for the lead's next projection: h1 on cascadelake took about 16.5 h per task (≈ 33 core-h), not the 12.6 h
  assumed at 01:09 CT (≈ 25). That adds about 40 core-h. Re-running the 01:09 projection with the actuals gives about
  1,891, which is within 5 core-h of the 1,896 ceiling. h1b/h2b is the next item in the pre-declared cut order.
  This is not a flag, because spend is the trigger and spend is at 1,456.
