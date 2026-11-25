# SMC-BVS layout (REORG 2026-11-25, owner greenlight via HQ)

One ROOT per machine, with the same names below it. A path relative to ROOT means the same thing on both machines.
- Owls ROOT: `/home/fb31/Bayesian-Variable-Selection` (the shared root clone; stays on `main`)
- NOTS ROOT: `/home/fb31/SMC-BVS`

```
ROOT/
  LAYOUT.md          this file (committed; NOTS keeps a verbatim copy)
  _local/            gitignored. Never in git.
    engineering/     was ~/SMC_Engineering_Department (INDEX.md, records/, records_manifests/, crews/, scripts/, bench/, envs/, Rlib/, logs/; staging/ deleted 2026-11-25)
                     Owls records/ is EMPTY since 2026-11-25 (owner ruling D-REC: desktop copy only); records_manifests/<unit>/SHA256SUMS.txt
                     keeps every deleted unit's manifest + desktop_verified/serve.log copies (provenance)
    theory/          was ~/SMC_Theory_Department (its legacy/ and records/ were deleted 2026-11-25 by owner order, see below)
    writing/         was ~/SMC_Writing_Department
    papers/          was ~/Papers_local/Papers (PDFs; copyrighted, never in git)
    hq/              Owls: was ~/.config/bvs-hq minus owls/ (snapshot cron snap/, launch_*.sh, tokens; dir 700, tokens 600)
    tmp/             the ONLY tmp/cache area (TMPDIR=ROOT/_local/tmp/<YYYYMMDD>-<owner>-<what>); empty when idle
  _wt/<name>/        Owls: git worktrees (`git worktree add/move` only, never mv). NOTS: code clones and builds
  scratch            NOTS only: symlink to /scratch/fb31/SMC-BVS/ (runs/, archive/, slurm_out/, _wt/)
```

## Old → new paths
| old | new |
|---|---|
| `~/SMC_Engineering_Department/…` | `ROOT/_local/engineering/…` |
| `~/SMC_Theory_Department/…` | `ROOT/_local/theory/…` |
| `~/SMC_Writing_Department/…` | `ROOT/_local/writing/…` |
| `~/Papers_local/Papers/…` | `ROOT/_local/papers/…` |
| `~/theory_campaign/` | deleted 2026-11-25 (owner order; was `ROOT/_local/theory/legacy/theory_campaign_202611/`) |
| `~/Misc/{api_workers,api_audit_work,abl_work,ablconf_work,ma_work,fresh_eyes,hq_reviews,ls0_work}` (Owls) | deleted 2026-11-25 (owner order; was `ROOT/_local/theory/legacy/misc_20261125/…`) |
| `~/.config/bvs-hq/{snap,api,inputs,gh_token,launch_*.sh,cloud_sessions.log}` (Owls) | `ROOT/_local/hq/…` |
| `~/BVS-wt/<name>` (Owls) | `ROOT/_wt/<name>` (`campaign` removed 2026-11-25, branch theory/campaign pushed) |
| `/scratch/fb31/SMC_{Engineering,Theory}_Department/…` (NOTS) | `ROOT/scratch/…` = `/scratch/fb31/SMC-BVS/…` |
| `/tmp/…`, `~/bvs_tmp/…`, `<dept>/tmp/…` | `ROOT/_local/tmp/…` |

Archived residue of the removed stale worktrees, Engineering/Theory tmp and /tmp items:
`records/reorg_20261125_owls/` units (tars, bundles, patches + SHA256SUMS), shipped to the desktop and verified, then deleted
from Owls with the rest of records/ (manifests in `ROOT/_local/engineering/records_manifests/`).

## Owner deletions after the move (2026-11-25, executed by HQ on Owls)
`_local/theory/legacy` (5.1 GB), `_local/engineering/staging` (2.5 GB), `_local/theory/records` (0.5 GB) deleted; `_wt/campaign`
removed with `git worktree remove` (clean, nothing unpushed). After: `_local` 921 MB, `_wt` 978 MB.

## Rules
- Nothing SMC outside ROOT except the exceptions below. New worktrees: `git worktree add ROOT/_wt/<name>`.
- Never `git clean -x` / `-ff` in ROOT (it would reach `_local/` and the nested `_wt/` worktrees). Tools that honour
  .gitignore (rg, fd) skip `_local/`; plain `grep -r` / `find` from ROOT walk all of `_local/` and `_wt/`: scope them.
- Data, records, PDFs, logs and secrets never enter git; `git status` must be clean of them before any commit.

## Exceptions (stay where they are)
1. Riboflavin: Owls `~/SMC_Engineering_Department/tmp/20261118-riboflavin/`, units ribo-s1..5, its @reboot crontab line, and
   its scripts in ROOT `Docs/Experiments/realdata_riboflavin/` (untracked), until DONE (≈ 11-27 02:46 CST). That folder plus a
   README.md is all that remains of ~/SMC_Engineering_Department.
2. The SMC_BVS_v3 deploy folder on NOTS (`~/projects/BVS/Others/SMC_BVS_v3_history_Oct2026/deploy/`; no Owls copy exists)
   and `/projects/ml75`: never touched (POLICIES §4).
3. T3-managed worktrees of live threads under `~/.t3/worktrees/` (T3 creates them there).
4. `~/.config/bvs-hq/owls/` (Owls compute guard: the `owls-guard` systemd unit, `owls_run`, POLICY.md). Agents in several
   projects call `owls_run` by this absolute path, so it stays.
5. `~/.ssh` and credentials: never touched.
6. Live Claude session scratchpads in `/tmp/claude-<uid>/`; HQ snapshot locks `/tmp/snap_*.lock`.
