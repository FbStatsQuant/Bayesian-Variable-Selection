# Pipeline review R04 — narrow reconciliation (Sol), brief (HQ, 2026-11-11)

You are an independent correctness reviewer of a research-registry tool chain (gpt-6.1-sol, reasoningEffort high).
Repo `C:/Users/felip/Bayesian-Variable-Selection`, main at 0b0906c. **Change no git state and no repo file except your
output file.** Run every fixture in your own disposable clone under your temp folder (`git clone --no-hardlinks`).

## Scope
For each item, reproduce the original failure on the current tools and give a verdict RESOLVED / PARTIAL / OPEN:
1. `Theory_work/Wave3/PIPELINE_REVIEW/R03_reconciliation_sol.md`: N1 (MAJOR), N2 (CRITICAL), N3 (MAJOR), N4 (MAJOR) — reuse
   the R03 fixtures in `C:/Users/felip/AppData/Local/Temp/bvs-r03-a09b93b45027434d8436c6a9ddbe3d7a/` (probes.py, more.py).
   N5 and F9 were addressed in the protocol (rule 12 hold file, `Theory_work/Wave3/HOLDS.md`; rule 15 command): check
   the text and the three scheduled-task prompts quoted in `HQ_DECISIONS.md` describe a working fail-closed path.
2. `Theory_work/Wave3/PIPELINE_REVIEW/R03_toolfix3_review_sol.md`: defects N1.a, N1.b, N3.a, N4.a (fixed after that
   review, not re-reviewed).
3. Then look for any remaining route by which, using only the documented commands (`check.py --acceptance … --record`,
   `ingest.py … --staged [--record]`, `manifest.py freeze/verify/bind`, `propagate.py`, `registry.py`), a claim is
   accepted as PROVED-CHECKED although (a) the council verdicts do not approve its current content, (b) a consumed
   claim is not ACTIVE or not accepted, or (c) cited evidence does not exist. Also check the frozen legacy boundary
   (`Theory_work/INFRA/LEGACY_ACCEPTED.tsv`, check L1-legacy) cannot be widened.

Code: `Theory_work/INFRA/tools/` (bvsreg, check, ingest, propagate, registry; `test_lifecycle.py` 127 scenarios),
`Theory_work/INFRA/LIFECYCLE.md` §4.1, `Theory_work/Wave3/tools/manifest.py`, `Theory_work/Wave3/PROTOCOL.md` rules 9–16.

## Output
`Theory_work/Wave3/PIPELINE_REVIEW/R04_reconciliation_sol.md`: one row per item (id, severity, verdict, exact command and
output), new findings with severity and reproduction, and an overall verdict **READY** (no open CRITICAL; MAJORs listed)
or **NOT-READY**. Final message ≤ 10 lines: verdict and every open CRITICAL/MAJOR.
