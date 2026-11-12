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
