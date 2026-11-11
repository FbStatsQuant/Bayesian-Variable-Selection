# INFRA tool fix — R04-N1 / R04-N2 (acceptance record fingerprint) — brief (HQ, 2026-11-11)

You are the implementer (Claude Opus 5.5, effort high, Claude Work). Worktree `C:/Users/felip/BVS-wt/INFRA-R04`
(branch `theory/infra-r04fix`, from main 80e6acd). Work only there. **Change no git state** (HQ commits).

## Defects
Read `Theory_work/Wave3/PIPELINE_REVIEW/R04_reconciliation_sol.md` §R04-N1 and §R04-N2 in full, including the
reproductions.
- **R04-N1 (MAJOR):** an accepted input's evidence or council outcome can change without invalidating its acceptance
  record, so a consumer can still be accepted against it.
- **R04-N2 (MAJOR):** the acceptance fingerprint omits statement-file provenance; a documented statement relocation
  leaves an accepted-input record current.

Sol's fix direction: include all acceptance-relevant source, provenance and dependency metadata in the acceptance
identity (at minimum `file`), make relevant mutations invalidate it, and validate the effective dependency graph and the
referenced artifacts (evidence files, council verdict lines bound to the frozen manifest), not only selected row strings.

## Do
1. Reproduce both defects with the R04 fixtures in a disposable clone (`git clone --no-hardlinks` under your temp folder).
2. Fix in `Theory_work/INFRA/tools/` (bvsreg, check, ingest, registry; `Theory_work/Wave3/tools/manifest.py` if needed).
   Update `LIFECYCLE.md` §4.1 if the record format changes. Keep the 128-claim legacy boundary (`LEGACY_ACCEPTED.tsv`,
   check L1-legacy) unchanged and impossible to widen. Existing accept records on main must either stay valid or be
   migrated by a documented, tested step.
3. Add regression scenarios to `test_lifecycle.py` (evidence change, verdict change, file relocation, each followed by
   consumer acceptance → refused) and run the full suite (currently 127/127). **Wait for it in your run.**
4. Then start ONE fresh correctness reviewer: `delegate_task`, provider `codex`, model `gpt-6.1-sol`, reasoningEffort
   high, mode wait. Save its brief to `Theory_work/INFRA/R04FIX/BRIEF_sol.md`: reproduce R04-N1/N2 on your fixed tree,
   give a verdict RESOLVED / PARTIAL / OPEN for each, plus any new route around acceptance; output
   `Theory_work/INFRA/R04FIX/R04FIX_review_sol.md`. Fix what it finds (one more Sol round at most).
5. Write `Theory_work/INFRA/R04FIX/REPORT.md` (changes, test count, Sol verdicts) and end your run with a ≤ 10-line
   summary.

No other agents. Any Claude helper only on provider `claudeAgent`, never Claude Personal. Stay in your run while tests
or the reviewer are working.
