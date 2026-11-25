# HANDOFF v2 → v3 (SMC Engineering Department), 2026-11-25

Read this first, then POLICIES.md (ROOT) and LAYOUT.md (ROOT, the tree and exceptions).

## State
- SMC-BVS is on a break under an OWNER FREEZE (H-54). Start nothing until HQ sets the next goal.
- REORG (owner greenlight 11-25) is DONE. Every SMC-BVS file sits under one ROOT per machine, with the same layout:
  - Owls ROOT = `/home/fb31/Bayesian-Variable-Selection`: `_local/{engineering,theory,writing,papers,tmp,hq}` (gitignored via `.git/info/exclude` and the exp/P1M `.gitignore`) and `_wt/<worktree>`.
  - NOTS ROOT = `~/SMC-BVS`: the same `_local/` names and `_wt/`, plus `scratch` → `/scratch/fb31/SMC-BVS`.
  - Spec: `REORG_SPEC.md`; plans: `REORG_OWLS_PLAN.md`, `REORG_NOTS_PLAN.md` (this folder); LOG.md has one line per deletion batch.
- This Engineering worktree is `ROOT/_wt/P1M` (branch exp/P1M). The old path `~/BVS-wt/P1M` is gone.
- Owner ruling 11-25: the Owls `records/` (desktop-verified units) were deleted ("we will run fresh simulations anyways"). The desktop copy at `D:\SMC_Engineering_Department\records\` is the only copy. Manifests are kept at `ROOT/_local/engineering/records_manifests/<unit>/SHA256SUMS.txt`.
- NOTS run data was deleted, including the island_*.bin files (owner ruling, regenerable). The protected GB_/RG_ data is on the desktop only.

## Open items
1. **Riboflavin** is still running on Owls (units ribo-s1..5, ETA ≈ 11-27 02:46 CST) from `~/SMC_Engineering_Department/tmp/20261118-riboflavin/`, with an @reboot crontab line. It is the one listed exception. After it finishes:
   - move its folder to `ROOT/_local/engineering/runs/20261118-riboflavin/` (or as HQ says);
   - update the @reboot line, or drop it;
   - remove `~/SMC_Engineering_Department`.

   The scripts' backup is in its `scripts_backup/`, with SHA256SUMS.
2. **EXPERIMENT_PLAN.md** is a WIP v0.4 (commit 5cdadd66). The S3 drop is partial and unreviewed. The five approved competitors (Lasso-CV/glmnet, SCAD/ncvreg, MC3/BAS, ASI/PARNI, SuSiE/susieR) are NOT folded in yet. Plan only; no installs.
3. **Daily report:** schedule be4c26b5 is disabled by HQ; f9847b84 is also disabled.
4. **HQ snapshot cron:** `ROOT/_local/hq/snap/snapshot_ticket.sh`. Drop its `~/BVS-wt/$T` fallback once P1M is at `_wt/P1M` (done in the move, if the next line in LOG says so).
5. **Theory and Writing threads:** these must be relaunched by HQ at `ROOT/_wt/THEORY-DEPT` and `ROOT/_wt/WRITING`.

## Paths you will need
| what | Owls | NOTS |
|---|---|---|
| Engineering dept | `ROOT/_local/engineering` (INDEX.md, crews/, scripts/, envs/, Rlib/) | `~/SMC-BVS/_local/engineering` |
| runs | (none on Owls) | `~/SMC-BVS/scratch/runs` = `/scratch/fb31/SMC-BVS/runs` |
| offload | `ROOT/_local/engineering/crews/offload/serve_pull.sh` (the desktop calls it hourly at :20; `desktop_verified.txt` is written there) | — |
| HQ infra | `ROOT/_local/hq/` (snap, tokens; perms 700/600); `~/.config/bvs-hq/owls/` stays (owls-guard runs from it) | — |
| papers (PDFs, never in git) | `ROOT/_local/papers` | — |

Old prefixes in historic batch scripts and docs are NOT rewritten, because the run manifests hash them. Map them as follows:
- `/home/fb31/SMC_Engineering_Department` → `ROOT/_local/engineering`
- `/scratch/fb31/SMC_Engineering_Department` → `/scratch/fb31/SMC-BVS`
- `~/BVS-wt/<name>` → `ROOT/_wt/<name>`

## Rules unchanged
- Public repo: never commit data, records, PDFs, logs or secrets.
- Never force-push.
- NOTS etiquette: ControlMaster, one stream, nice/ionice, no sbatch without HQ.
- Never touch the SMC_BVS_v3 deploy folders, /projects/ml75, ~/.ssh, or other projects.
- Report to HQ only (thread mcp:4f1a2e12-7ac4-4619-9128-1469ea92eb2e, environment 1fde6176-4453-43b0-82cc-70fda5110037, mode queue).
