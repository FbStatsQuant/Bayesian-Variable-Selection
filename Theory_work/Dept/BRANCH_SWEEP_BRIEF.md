# Branch sweep brief (HQ order 11-17; owner: everything finished must reach main; no long tail of branches/PRs)

Role: Sonnet sweeper, claudeAgent_personal. Budget ≤ ½ day. Start only after the track V recording lands on main.
Repo: FbStatsQuant/Bayesian-Variable-Selection. Work in your own worktree from origin/main. **Never delete, force-push or rewrite any branch; never touch origin/main directly; never merge a PR (HQ merges after CI).**

## Scope
Every remote branch `origin/theory/*` and `origin/dept/theory` (113; 105 have file diffs vs main on 11-17).

## Step 1 — classify (table: branch | last commit | files differing vs main | class | reason)
For each branch, compare at file level: `git diff --name-status origin/main...origin/<b>` and, for every file, whether the branch tip version is
(i) identical to main, (ii) absent from main, (iii) different from main. For (iii), decide which is newer/final (git log on both sides; main versions
written by the recorder are authoritative).
- **DONE**: finished work whose files are absent from main or newer than main and final (ticket folders, research notes, API cards/results,
  literature notes). Moves to main.
- **LIVE**: still in use. Known LIVE: `dept/theory` (department records), `theory/W3-AUDIT` (V, D5P inputs), `theory/W3-D5P`, `theory/W3-READER`,
  `theory/W3-MISR-R` (family refresh pending), `theory/W3-DIST`. Ask the manager if unsure.
- **OBSOLETE**: everything the branch has is already on main (identical or superseded by a recorded version), or abandoned drafts that a later ticket
  replaced. Name the superseding commit/file.

## Step 2 — PR(s) for DONE content
Prefer **one consolidated PR** `theory/sweep-2026-11` → main (group commits by source branch, one commit per branch, message "sweep: <branch> (DONE)").
Plus one snapshot PR of `Theory_work/Dept/` (QUEUE, DECISIONS, LOG, RIDER_RULES, notes) from dept/theory (LIVE but its finished records belong on main).
Include only finished, non-sensitive files. **Exclude:** `.rc_tmp/`, scratch/tmp folders, anything gitignored (`git check-ignore`), PDFs of papers
(the refs stay out of git), credentials/tokens, `Theory_work/INFRA/registry/*` (the registry changes only through the recorder), and any file whose
main version is newer. Never overwrite a file that exists on main with an older branch version.
Before opening: `Theory_work/INFRA/ci/run_ci.py --steps check,paper,falsify,cite` must PASS on the committed PR tree, in CI's environment: a Python 3.13
venv (uv) with `Theory_work/INFRA/ci/requirements-ci.txt`, `BVS_NUMERICS_PY=<that python>`, `PYTHONUTF8=1`,
`PYTHONPATH=<repo>/Theory_work/Wave1/W1-N3/numerics` (local python3 is 3.9 without mpmath; falsify fails spuriously there). Don't commit regenerated
CITECHECK.txt files of unrelated tickets. Fix pointer/citation breaks only by excluding the offending file and listing it as LIVE/needs-recording.
PR body: the sweep table, exclusions, and CI result; end with the Claude Code attribution line.

## Step 3 — PR #1 (theory/E-SPINE, 11-02, "replace 'tempering is needed' …")
Check whether its changes are already on main or superseded (grep main for the old and new phrases; compare the campaign-decision records). Report
SUPERSEDED (with the evidence) or STILL NEEDED. Do not close it yourself; the manager closes it with a one-line reason.

## Report to the manager (≤ 30 lines)
The table summary (counts DONE/LIVE/OBSOLETE + the DONE and LIVE rows in full; OBSOLETE rows in a file `Theory_work/Dept/BRANCH_SWEEP_2026-11-17.md`,
committed in the sweep PR), PR numbers + URLs, CI result, PR #1 verdict, and anything you were unsure about.
