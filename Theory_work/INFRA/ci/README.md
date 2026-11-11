# Continuous audit (CI) for the theory program

`run_ci.py` is a local, read-only audit: every ticket script (falsification numerics, citecheck) runs inside a
disposable DETACHED git worktree of HEAD in a temp directory (stdout to a file, the whole process tree killed on
timeout, the sandbox reset after each script and removed at the end), so the working checkout is never touched. CI
therefore audits the COMMITTED state.
Sandboxes are created only as strict `sb-*` children of `<temp>/bvs-ci-sandboxes/`. Ownership is a lock, not a pid:
the creating process holds an exclusive lock on `<sandbox>.lock` (manifest line + sandbox path) for the sandbox's
whole life. A later run removes a stale sandbox only if it is such a child, its lock file carries the manifest for
exactly that path, and the lock can be acquired (owner gone); anything else is left untouched. No global
`git worktree prune` is run. On Windows each script starts suspended inside a Job Object and the Job is terminated
on every exit path (all and only that run's processes; no recycled-pid killing). On POSIX the session group is
killed on timeout while its leader is unreaped; orphans of a normally exiting script are not tracked there. This
isolates relative writes; it is not a security sandbox against scripts that write to absolute paths. It schedules nothing by
itself: **HQ schedules it with T3 scheduled tasks**. Rules behind each step: `../LIFECYCLE.md`.

## Steps

| step | what | fails the run when | typical time |
|---|---|---|---|
| `check` | `tools/check.py`: statement hashes, use-level dependency lifecycle, dangling ids, cycles, statuses vs `State_of_Project/registry/theory_loop.tsv` and `Wave1C/FINAL/sections/*.tex`, method pins (M1), strength-layer consistency | any ERROR | seconds |
| `paper` | `tools/assemble.py --check`: generated paper blocks match the registry | stale | seconds |
| `falsify` | re-runs the **cheap** (< 120 s, calibrated) saved falsification scripts in `falsification.tsv`; compares regenerated output files with the committed ones; runs `kind=boundary` entries (just outside an assumption: a PASS is reported as an *improvable* SIGNAL) | a script fails / times out | minutes |
| `cite` | re-runs every ticket's `citecheck.py` (Wave1C/FINAL, W2-APP, W2-LOC2, W2-UNI, the `reviews/citecheck.py` ones) and compares MISS counts with the committed `CITECHECK.txt` | MISS count increased | < 1 min |
| `reaudit` | picks one random ACTIVE PROVED-CHECKED claim (seed = date) and writes `reaudit_<id>.md`, the brief for a fresh adversarial reviewer | never | instant |
| `optimize` | **event-triggered only** (`--event wave-boundary\|technique\|strategy-review --note "..."`): picks one binding claim of an unsettled headline hypothesis and writes `improve_<id>_<A>.md`, priced in re-proof + re-review | never | instant |

Output: `ci/out/<YYYY-MM-DD>/SUMMARY.md` (+ `check.txt`, `check.json`, `falsify.log`, briefs). `ci/out/` is not
committed; HQ copies what it acts on into the relevant ticket or issue.

## How HQ schedules it (T3 scheduled tasks)

1. **Daily audit** (cheap): schedule a task in the Theory HQ project, e.g. every day 06:00, prompt:
   > In C:\Users\felip\Bayesian-Variable-Selection on an up-to-date checkout of main, run
   > `python Theory_work/INFRA/ci/run_ci.py --steps check,paper,falsify,cite`. Report the SUMMARY.md verdict per
   > step to Theory HQ. If `check` has ERRORs or a falsification script fails, open one issue per finding with the
   > repo's issue templates (label `suspect` or `lemma-gap`) — do not change the registry yourself.
2. **Weekly re-audit** (one strong review per week): e.g. Monday, prompt:
   > Run `python Theory_work/INFRA/ci/run_ci.py --steps reaudit`, then start ONE fresh Codex `gpt-6-astra`
   > reviewer at reasoningEffort **high** (never xhigh/max) with the brief in `ci/out/<date>/reaudit_*.md` as its whole
   > task. When it replies, HQ dispositions it: HOLDS → add the file to the claim's `evidence`
   > (`registry.py set`); anything else → `propagate.py suspect|patch|downgrade ... --dry-run` and an issue.
3. **Optimizer** — not scheduled. HQ runs it at events: end of a wave, a technique newly landed in some ticket, or a
   new strategy-review proposal:
   `python Theory_work/INFRA/ci/run_ci.py --steps optimize --event wave-boundary --note "Wave 2 closed"`.
   HQ decides whether to launch the improvement ticket (with a kill budget); Felipe approves if it would change a
   headline.

Run from a checkout of `main` that is up to date (`git pull`) and has no uncommitted ticket work, or pass
`--out` to keep outputs elsewhere. The audit never edits tracked files (restores them), but if a ticket thread is
running numerics in the same checkout at the same time, run CI in a separate worktree
(`git worktree add ../BVS-ci main`); the sandboxing makes this a convenience, not a safety requirement.

## Maintaining `falsification.tsv`

Columns: `kind` (falsify | boundary), `claims` (registry ids), `assumption` (boundary entries: which assumption is
violated), `script` (repo-relative), `args`, `timeout_s`, `runtime_s`, `cheap`, `outputs` (committed output files to
compare, `;`-separated), `expect` (regex that must appear in stdout), `notes`.
- Seeded from the registry's `falsification` column (every script a lemma file / review names as its falsification
  check). Re-time all entries after adding scripts: `python Theory_work/INFRA/ci/run_ci.py --calibrate`
  (120 s cap per script; sets `cheap`). Calibration is resumable (it persists after every script and skips rows
  already timed; `--recalibrate-all` re-times everything). Run it on an otherwise idle machine: under load
  (parallel ticket numerics) runtimes are pessimistic and fewer scripts qualify as cheap.
- Tickets add their own entries in their PR (one row per script; boundary-violation numerics with
  `kind=boundary` and the `assumption` id).
- A boundary script must end by printing exactly one line `BOUNDARY-RESULT: HOLDS` (the conclusion still held just
  outside the assumption: an *improvable* signal) or `BOUNDARY-RESULT: FAILS`; a crash, import error or timeout is
  an execution FAILURE, never a scientific outcome.
