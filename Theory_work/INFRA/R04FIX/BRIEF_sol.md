# R04FIX — independent correctness review (Sol) — brief

Context: this is a software-correctness review of a research-project bookkeeping tool (a Python registry of
mathematical claims and the checks that decide when a claim counts as reviewed). No security testing is involved.

You are an independent correctness reviewer (Codex GPT-6.1 Sol, effort high). Work in the worktree
`C:/Users/felip/BVS-wt/INFRA-R04` (branch `theory/infra-r04fix`, base main 80e6acd), whose working copy holds an
**uncommitted** fix. **Change no git state in this worktree** (no commit, stash, checkout, reset, add). The only file
you write in it is your output `Theory_work/INFRA/R04FIX/R04FIX_review_sol.md`. Start no subagents. Do not touch the
main checkout `C:/Users/felip/Bayesian-Variable-Selection`, any live registry, scheduled task or hold file.

## What to review
The defects are in `Theory_work/Wave3/PIPELINE_REVIEW/R04_reconciliation_sol.md`, §R04-N1 and §R04-N2 (read both in
full, including the reproductions):
- **R04-N1 (MAJOR):** an accepted input's evidence or council outcome could change without invalidating its
  acceptance record, so a consumer could still be accepted against it.
- **R04-N2 (MAJOR):** the acceptance fingerprint omitted statement-file provenance; a documented statement
  relocation (`registry.py set <id> file=...`) left an accepted-input record current.

The fix (see `git diff` in the worktree): `Theory_work/INFRA/tools/bvsreg.py` (`accept_artifacts`, `accept_identity`,
`accept_stamp` — new `v<version> fp2:<24 hex>` record over row fields incl. `file`/`lines`/`premises`/`status_source`,
ticket folder, effective resolved inputs, names, and the content of every cited gate-evidence file, council review file
and matching frozen manifest; `unaccepted_inputs` now also revalidates matching inputs), `check.py`
(`claim_checks` extracted from `acceptance_checks`; A5 revalidation of every non-legacy accepted input, memoised),
`LIFECYCLE.md` §4 A5 and §4.1 "Acceptance record" (format + migration note), and 7 new scenarios in
`test_lifecycle.py` (block "pipeline review R04"). The 128-claim legacy boundary (`LEGACY_ACCEPTED.tsv`, check
L1-legacy) is intended to stay unchanged (no extra rows can be added).

## Do
1. Make every fixture run and git mutation in a disposable clone outside the worktree:
   `git -c core.longpaths=true clone --no-hardlinks --quiet -c core.longpaths=true C:/Users/felip/BVS-wt/INFRA-R04 <dest>`
   under a short temp path (e.g. `C:/Users/felip/AppData/Local/Temp/r4s-<random>`; long paths fail on Windows), then
   copy the worktree's modified files over the clone (`Theory_work/INFRA/tools/*.py`, `Theory_work/INFRA/LIFECYCLE.md`),
   since the fix is uncommitted.
2. Reproduce R04-N1 (variant A evidence deleted, variant B verdict withdrawn) and R04-N2 (file relocation) on the
   fixed tree, following your original fixtures (the original scripts are in
   `C:/Users/felip/AppData/Local/Temp/bvs-r04-d1d6ed5190454fdabedfa2c9b9595813/` and
   `C:/Users/felip/AppData/Local/Temp/bvs-toolfix3-sol/probe.py`; read them, do not run them against the worktree).
   A condensed version is `C:/Users/felip/AppData/Local/Temp/r4f/repro.py <clone root>` (its variant C is refused by
   registry.py itself — `status_source` is not settable there — so it is not a relevant case).
3. Give a verdict **RESOLVED / PARTIAL / OPEN** for R04-N1 and for R04-N2, each with exact commands, exit codes and
   relevant output.
4. Check for any **remaining gap in the invalidation logic** (a consumer still accepted although an input it depends on
   would currently fail acceptance), introduced or left by the fix: e.g. edits to an accepted input that neither alter
   the identity nor fail revalidation; alias / tickets.tsv folder edits; transitive inputs; inputs
   named in the same run; the `ingest.py claims F --staged --record` path; legacy boundary rows staying fixed; the
   record/check consistency between staged and live runs; old-format (`fp:`) records. Report each with severity
   (CRITICAL / MAJOR / MINOR), a reproduction, and a fix direction. Do not report the intended fail-closed strictness
   (e.g. any cited-artifact edit making a record stale) as a defect unless it breaks a documented workflow.
5. Run the full regression suite once in a disposable clone (copy the modified files in first):
   `python -B Theory_work/INFRA/tools/test_lifecycle.py` (expected 134 PASS, 0 FAIL; it takes ~9 minutes; wait for it).

## Output
`Theory_work/INFRA/R04FIX/R04FIX_review_sol.md`: overall verdict line first; then a table of R04-N1 / R04-N2 verdicts
with commands and outputs; new findings (or "none found"), each with severity, reproduction and fix direction; the
suite result; the scratch paths you used. Keep it factual and compact. End your run with a ≤ 5-line summary.
