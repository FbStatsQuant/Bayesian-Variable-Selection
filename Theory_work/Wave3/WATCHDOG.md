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
