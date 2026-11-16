# BRIEF — machines crew, leg 1: inventory and reorganization plan (Opus 5.5 helper, high). SMC - Engineering, 2026-11-15

Owner rule (via HQ, POLICIES §12 when on main): compute discipline, "no flying folders", "squeaky clean 24/7".
- NOTS home ≤ 10 GB (guard 8 GB, target < 7 GB); heavy data only in `/scratch/fb31/`.
- **One unified, indexed SMC-BVS tree on NOTS scratch** with an `INDEX.md` at its root (what lives where, provenance).
- Move only idle data, never anything used by queued or running jobs; leave a symlink or an index entry for old paths.
- Owls: no clutter in `/home/fb31`; outputs live in a worktree or a department folder.
- **Never touch, read into, or move** `/home/fb31/projects/BVS/SMC_BVS_v3/deploy/` or `/projects/ml75`: list them as
  excluded, do not descend.

This leg is **read-only: inventory and plan only. No move, delete, chmod or write on NOTS. No sbatch or srun.**
Access: `ssh nots` (read-only use); local Owls shell. Write only under `Docs/Experiments/P1M/machines/` in
`/home/fb31/Bayesian-Variable-Selection`. Change no git state. Start no sub-agents. Owner memo: solve problems inside the
department; report big problems at once in your final message.

## Tasks
1. **NOTS inventory (SMC-BVS material only).**
   - `/scratch/fb31` (all of it), `/home/fb31` on NOTS (sizes by top-level dir; caches such as `.cache`, `R` libraries,
     `.cpp_cache`), and `/home/fb31/projects/BVS` (excluding `SMC_BVS_v3/deploy`).
   - For each top-level and second-level directory: size (`du -sh`, run with `nice` and a timeout; never a recursive
     `find` over the whole scratch without limits), last modification, file count, what it is (ticket or campaign, from
     names, manifests and READMEs), and which repo files point to it (grep the repo for the path).
   - Home quota: `quota -s | grep -A1 export/nots/home | tail -1`. Use exactly this line; the last line of plain
     `quota -s` is a different filesystem.
2. **In-use check.** `squeue -u fb31` and `sacct -u fb31 -S now-7days --format=JobID,JobName%30,State,WorkDir%80` give the
   paths used by queued, running or recent jobs. Anything under such a path is IN USE and must not be moved.
3. **Classify every item.** ACTIVE (in use or referenced by a live ticket) / IDLE-KEEP (results of record, frozen code,
   run manifests) / TEMP (caches, compile caches, scratch temporaries, `*.lock`, partial outputs of cancelled jobs) /
   UNKNOWN (owner unclear: list it, never propose deleting it).
4. **Target tree** under `/scratch/fb31/smcbvs/` (propose the layout). For example `code/` (frozen code by commit),
   `data/`, `runs/<ticket>/<run_id>/`, `results/`, `archive/`, `tmp/` (crew-cleaned), and `INDEX.md`. Map every existing
   item to its target path.
5. **Reorganization plan** `machines/REORG_PLAN.md`:
   - an ordered list of moves (source → target; symlink at the old path or an INDEX entry);
   - which items wait because they are in use;
   - what is TEMP and safe to clean, with the exact command and why;
   - total bytes per class;
   - the draft `INDEX.md` for the new tree;
   - a list of the repo files whose hard-coded paths would change: these need updates, by ticket owner.
6. **Owls footprint** (SMC-BVS only): `/home/fb31/p1m_feas_bench`, `/home/fb31/p1m_g0_dryrun` (the latter **in use by a
   running helper; plan its move for later**), `/home/fb31/BVS-wt/*` (sizes, branch per worktree, last use), and any other
   `/home/fb31/*` directory that is clearly SMC-BVS. Propose where each belongs. Note `/tmp` usage by SMC-BVS work if
   identifiable. Do not touch other users' or other projects' files.
7. **Daily crew design** `machines/CREW.md`:
   - what a daily check runs (home quota line, scratch tree versus INDEX, stray-folder detection, Owls footprint, temp
     cleanup rules);
   - what it may delete automatically (only TEMP classes inside the tree's `tmp/` and named compile caches) and what it only
     reports;
   - the 8 GB guard action.

## Output
- `machines/INVENTORY.md`, `machines/REORG_PLAN.md`, `machines/CREW.md`, each with sizes and the commands used.
- Final message: at most 12 lines: totals by class, home usage, the 3 biggest issues, and anything that needs a decision.
