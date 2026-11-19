# PREREG ADDENDUM 2: criterion C for escalated T fits, and the during-wave per-fit T rule

**Status: APPROVED by HQ (HQ_DECISIONS 5b26e388, 2026-11-19 early; HQ rules for Theory, which is on hold: experiment protocol).**
**In force from W2.** Pre-declared BEFORE any T fit has crossed 172.5 core-h (max so far: W1 IND-T-s2, 143.96) and BEFORE the W2 read-back.
Date: 2026-11-19. Author: Engineering manager (Opus). Deviation class: OVERLAP_1e4_PREREG.md §9 (protocol; no change to any registered
script, threshold, metric, criterion definition or outcome rule).

## Reason
REPROJECTION_W1.md (Opus) puts P(some remaining T fit > 172.5 core-h, or a calibrate TIMEOUT) at ≈ 0.22 (range 0.11–0.52), all of it
from legitimate tier-1 escalation of the coded calibration (D-26), which the pre-registration makes part of the T method. The plan's
"during" stop rule (T fit > 172) would halt the rung on such a fit, leaving the AR-strong datasets r02–r04 (the ones the precision-study
diagnosis needs) unmeasured. The outcome consequence of such a fit was already registered (§3.7 C fails → §4 rule 3 MARGINAL); what was
not fixed in advance is whether the run continues. This addendum fixes it now, before any breach is observed.

## Rules (and only these)
1. **Criterion C is unchanged.** Pass iff every fit is ≤ 1.5 × its arm's model (V ≤ 15.0, T ≤ 172.5 billed core-h). A T fit that crosses
   172.5 core-h through legitimate escalation is recorded **C = FAIL for that fit**, and the rung outcome follows §4 unchanged (C fail →
   at best MARGINAL). **C is never changed post hoc** (no tier-aware C, no re-basing of the 1.5 × model, no exclusion of escalated fits).
2. **The fit is NOT cancelled and the rung continues to 40/40.** The during-wave per-fit **T** rule (> 172 / 172.5) changes from STOP to
   **REPORT-AND-CONTINUE**: the monitor reports the fit to the manager and HQ immediately; nothing is cancelled and the self-release of the
   next wave is not blocked by this rule alone.
3. **Unchanged stops (still STOP submitting and report):** the per-fit **V** rule (> 15); the wave rule (> 2 × QUOTE); the cumulative rule
   (1.6k, Option A 2.1k to be confirmed at the W2 read-back, H-21); the projection > 2.5k; any non-infrastructure failure (incl. a T
   calibrate TIMEOUT, which still needs an HQ ruling on the re-run); > 2 failed fits; admission refusal; X/y mismatch.
4. **"Legitimate escalation"** = the fit's calib.bin records tier_final ≥ 1 with N_final = 10⁴ × 4^tier_final, its islands ran at that N
   (PREREG_ADDENDUM_1), and every stage COMPLETED. A T fit over 172.5 that is NOT legitimate escalation (e.g. a re-run, a stuck stage, a wrong
   N) is reported as an anomaly for HQ, not covered by rule 2.

## Related HQ rulings in the same decision (5b26e388; operations, not prereg)
- Option A (2.1k cumulative) is to be confirmed at the W2 read-back, as planned.
- T calibrate limit **5:00 for W3 only** (max_task_hours 5.0; second exception to the 2-h norm; W2 stays at 3:00; the 1M campaign keeps the 2-h norm).
  Same engine run, no science change (calibration is deterministic); it removes the TIMEOUT-and-re-run cost tail.

## Implementation
- No change to `compare_overlap.py` (sha 311bbad8…) or `compare_overlap_v2.py` (sha 4f402e51…): both already record C FAIL → MARGINAL.
- `staging/overlap1e4/tools/stop_rules.py` (monitor, not a registered file): the T per-fit line becomes
  `REPORT fit … > 172.5 (PREREG_ADDENDUM_2: report-and-continue; C FAIL for this fit)`; it no longer makes the verdict STOP. The V per-fit
  line stays STOP. Backup `stop_rules.py.bak_20261119`.

## Approval
HQ decision: APPROVED, HQ_DECISIONS 5b26e388 (2026-11-19), ruling for Theory. Committed with its sha256 before the W2 read-back.
