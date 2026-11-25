# REORG spec (owner greenlight via HQ, 2026-11-25). Target: done in 2 h or less.

Goal: every SMC-BVS file on Owls lives under `/home/fb31/Bayesian-Variable-Selection` (the ROOT on Owls), and every SMC-BVS file on NOTS lives under `/home/fb31/SMC-BVS` (the ROOT on NOTS). Both machines use the same layout. Old or irrelevant files are deleted after a sha-verified copy (if in doubt, copy first). SMC caches, tmp and trash are wiped.

## Target layout (identical names on both machines)
```
ROOT/
  LAYOUT.md          the tree below plus the exceptions (committed on Owls; a verbatim copy on NOTS)
  _local/            gitignored on Owls. Never in git.
    engineering/     from ~/SMC_Engineering_Department (INDEX.md, records/, crews/, staging/, scripts/, bench/, envs/, Rlib/, logs/)
    theory/          from ~/SMC_Theory_Department
    writing/         from ~/SMC_Writing_Department
    papers/          from ~/Papers_local (PDFs; copyrighted, never in git)
    tmp/             the ONLY tmp/cache area; empty at the end
  _wt/<name>/        Owls: git worktrees (moved with `git worktree move`, never mv). NOTS: code clones and builds (e.g. clone_e993ece2, code_ws)
  scratch            NOTS only: a symlink to /scratch/fb31/SMC-BVS (the one allowed exception, because of the 10 GB home quota)
```
On NOTS, scratch is `/scratch/fb31/SMC-BVS/{runs,archive,_wt?}`. Today's `/scratch/fb31/SMC_Engineering_Department` and `/scratch/fb31/SMC_Theory_Department` merge into it. Owls has no `scratch` entry.
Both ROOTs get the same `_local/<dept>/` names, so a path relative to ROOT means the same thing on both machines.

## Owls .gitignore (the only tracked change, plus LAYOUT.md)
Add `/_local/`, `/_wt/`, `/scratch`. Before any commit, `git status` must show no data, records, PDFs, logs or secrets.

## Listed exceptions (stay where they are; recorded in LAYOUT.md)
1. Riboflavin: `~/SMC_Engineering_Department/tmp/20261118-riboflavin/`, its units ribo-s1..5, and its @reboot crontab line, until DONE (≈ 11-27 02:46 CST). ~/SMC_Engineering_Department therefore keeps only that folder (plus a README.md pointing to the new ROOT).
2. The SMC_BVS_v3 deploy folders. POLICIES §4 says never touch them: Owls `/home/fb31/projects/BVS/Others/SMC_BVS_v3_history_Oct2026/deploy/`, and the NOTS one under `~/projects/`. Also `/projects/ml75`.
3. T3-managed worktrees of LIVE threads under `~/.t3/worktrees/` (stale ones go: pushed or merged, then `git worktree remove`).
4. HQ infrastructure `~/.config/bvs-hq/` (snapshot cron, owls_guard, the gh token). Its path references are updated; the folder is not moved (it holds credentials). HQ decides.
5. ~/.ssh and credentials: never touched.
6. Live Claude session scratchpads in /tmp/claude-71711 of live threads (stale SMC ones are wiped).

## Rules
- Live worktrees: ~/BVS-wt/{THEORY-DEPT,WRITING,P1M}. They move LAST, only after HQ has the new path and says go (HQ re-points the thread).
- Stale worktrees: push any unpushed commits first, then `git worktree remove`. Never lose a commit.
- Update every path reference: crontab (snapshot lines), systemd user units, `~/.config/bvs-hq/snap` and `owls` scripts, offload `serve_pull.sh` and its verify scripts, the NOTS `scripts/<batch>/env.sh`, home_guard and prune scripts, INDEX.md files. The desktop `pull_desktop.ps1` change goes to HQ as exact text.
- After the move, the offload pull must still work (desktop_verified stays consistent; units are not re-sent).
- SMC only. Never touch BNP-Lean, Large-Prior, lhv, BQTF, e03, /projects/ml75, ~/.ssh or Slurm jobs.
- NOTS: low ssh concurrency (one stream at a time, ControlMaster), nice/ionice, no sbatch.
- Deletions: only after a sha-verified copy exists (Owls records → desktop D:\ via the offload, or already desktop-verified). One LOG line per deletion batch, with sizes.
