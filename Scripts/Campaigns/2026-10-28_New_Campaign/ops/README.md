# ops/ (OPS thread): NOTS operations for the New Campaign

| File | What |
|---|---|
| NOTS_INVENTORY.md | read-only inventory taken before clean-up (2026-10-29) |
| CLEANUP_PLAN.md / CLEANUP_LOG.md | class A/B/C plan; what was deleted, with its verification (class B: pip cache deleted; old VS Code server versions deferred to Felipe) |
| NOTS_ENV.md | R modules, compilers, partitions, Sapphire Rapids constraint, scratch purge notes |
| OPS_LOG.md | every transfer, stage and delete event (written by the tools) |
| DISK_LOG.md | one usage line per guard check |
| guard.sh | NOTS disk guard (staged at `/home/fb31/projects/BVS/New_Campaign/code/ops/guard.sh`). Limits (charter §2, D7): REFUSE (exit 1) if `New_Campaign` in home + planned add > **0.5 GiB**, or total home + planned add > **9.6 GiB**; `/scratch/fb31/New_Campaign` is reported for information only. Exit 2 = bad input or failed measurement. |
| disk_check.sh | laptop wrapper: validates PLANNED_ADD_MB locally (0..9999999), runs the guard once and appends to DISK_LOG.md |
| transfer/nots_pull.py | pull ONE NOTS folder, sha256-verify every file, then (with `--delete`) delete the remote copy |
| transfer/remote_pack.sh | NOTS side of nots_pull (manifest / tar / gated delete); staged next to guard.sh |
| transfer/verified_delete.sh | one-off A1 deletion against a verified list (allowlisted bases only) |
| verify_against_local.py | compare a NOTS sha256 list with a laptop folder |
| review/ | Sol 6.1 reviews and OPS responses |
| evidence/ | raw probe outputs, hash lists, test outputs, verification reports |

## Routine use (from Git Bash in this folder)
- Before every submission: `bash disk_check.sh <planned_MB> "<run_id> submit"`. A non-zero exit means **do not submit**. Only code, manifests and small inputs go to home (≤ 0.5 GiB total); logs and outputs go to `/scratch/fb31/New_Campaign`.
- After a run: `py -3 transfer/nots_pull.py /scratch/fb31/New_Campaign/results/<run_id> --delete`. This mirrors the run to `<PC_NOTS_DATA>\New_Campaign\results\<run_id>\`. Repeat for `logs/<run_id>`, and so on, one folder per call.
- After changing guard.sh or remote_pack.sh: `py -3 transfer/nots_pull.py --stage` (it uploads them and checks their sha256).
- After an ssh timeout: wait 15 minutes, then rerun. The tools never retry on their own.
