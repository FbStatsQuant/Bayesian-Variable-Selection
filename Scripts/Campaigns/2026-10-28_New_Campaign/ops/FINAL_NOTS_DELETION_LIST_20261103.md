# Final NOTS sweep — exact deletion list (OPS, HQ D92, 2026-11-03) — for Sol narrow check

Scope: the campaign's own NOTS footprint only, `/scratch/fb31/New_Campaign` and `/home/fb31/projects/BVS/New_Campaign`. Inventory (read-only, 13:26:53Z): `ops/evidence/ops_final_inventory_20261103.txt`. It found no fb31 jobs; guard home 8.42 GB, campaign_home 0.01 GB; no symlinks, foreign-owned or special entries in either tree.

**Never touched:**
- the benchmark freeze paths (`/projects/ml75/fb31/BVS/bench20261019/`, `/home/fb31/projects/BVS/Benchmarks/`);
- `~/.claude/remote` and `~/.t3-recovery`;
- anything outside the two campaign trees.

**Kept on NOTS (small, reusable, HQ D92):**
- `/home/fb31/projects/BVS/New_Campaign/code/{core, v2_2, bench_v2, ops}` (frozen code trees plus ops helpers, 2.4 MB, 71 files);
- `README.md`;
- the empty `inputs/` and `manifests/`.

## Archive (done and verified before any deletion)
Local destination: `<PC_NOTS_DATA>\New_Campaign\`.

- **Folders:** `nots_pull`, copy only, VERIFIED receipts in `ops/transfer/receipts/`, 0 mismatched, 0 missing. Evidence `ops/evidence/ops_final_archive_pulls.txt`.
  - `nots_home_final\code\{core,v2_2,bench_v2,ops}`
  - `nots_home_final\jobs\CONF_NOTS_IDENTITY`
  - `nots_home_final\runs\20261030T0934Z_prodH` (its HOME_MANIFEST `ca245339…` was re-checked locally: OK)
  - `nots_scratch_final\upload\ops_bg`
- **Single files:** one connection, tar plus NOTS-side sha256 list, local `sha256sum -c` OK. They are in `nots_scratch_final\` (README.md, upload\cleanup_receipt_*.txt, SHA256SUMS_remote.txt). Evidence `ops/evidence/ops_final_archive_files.txt`.
- **PROD-H upload tar:** its NOTS sha256 equals the local bundle copy `runs\20261030T0934Z_prodH\bundle\prodH_bundle_20261030T0934Z.tar` (`845de40e…`), so it was not re-copied.
- **Home README:** archived as `nots_home_final\README.md` (b98b337f…). It is not deleted.

## Deletions (executor `ops/scaffold/final_delete_remote_v2.sh`, after Sol R1; launched as `ssh nots "timeout 270 bash -s" < executor`, output saved to `ops/evidence/ops_final_delete.txt`)
The executor runs as ONE direct control-lane ssh (`bash -s` from stdin, ≤ 5 min). It does not use remote_bg, because remote_bg writes into `upload/ops_bg`, which is a target. Its cwd is `/home/fb31`, outside every target.

Before deleting, it requires:
- an empty `squeue -u fb31`;
- the D79 fail-closed `/proc` scan, byte-identical block (sha prefix 31034a821b9d341e), over the roots `/scratch/fb31/New_Campaign` and the home `jobs`, `runs`, `logs`, `results`. The HQ D79-accepted pinned sftp-server exemption applies only if that same pid:starttime is still present.

It stops at the first failure.

| # | Target | How | Gate |
|---|---|---|---|
| 1 | `/home/fb31/projects/BVS/New_Campaign/jobs/CONF_NOTS_IDENTITY` (8 files, 46,193 B) | `remote_pack.sh delete` | receipt manifest `1428212c068b125b0a0db857e85092614e95936cae285724ce1d8632a6b27cff` (re-hashed on NOTS) |
| 2 | `/home/fb31/projects/BVS/New_Campaign/runs/20261030T0934Z_prodH` (54 files, 4,070,345 B; PROD-H home run folder, HQ D92) | `remote_pack.sh delete` | `efd3abe307320ad8f3ada5f7ba8c0c577b5c2126ff4a6d52d5429718c445626b` |
| 3 | `/scratch/fb31/New_Campaign/upload/ops_bg` (46 files, 206,135 B) | `remote_pack.sh delete` | `d283478ec9311fec79046e9265d4db6d2e4d61eaf6ba64491962c1839b2202a6` |
| 4 | `/scratch/fb31/New_Campaign/README.md` | `rm -f` after the check | regular fb31 file, sha256 = `89127fdd…b38d` (archived) |
| 5 | `/scratch/fb31/New_Campaign/upload/cleanup_receipt_20261030T1811Z_lowp_prodL.txt` | same | `0dc2620c…dd66` |
| 6 | `/scratch/fb31/New_Campaign/upload/cleanup_receipt_20261102T1311Z_lowp_bench.txt` | same | `3c0e37ee…c1f5` |
| 7 | `/scratch/fb31/New_Campaign/upload/cleanup_receipt_20261102T2309Z_lowp_bench.txt` | same | `4dda357f…61e8` |
| 8 | `/scratch/fb31/New_Campaign/upload/prodH_bundle_20261030T0934Z.tar` (720 KB; HQ D92) | same | `845de40e…e72e` = local bundle copy |
| 9 | `/scratch/fb31/New_Campaign` (root) | only after `find ! -type d` returns nothing; then `find -depth -type d -empty -delete`; the root must be absent afterwards | empty directories only: code, inputs, logs, manifests, results (+ the empty `20261030T0934Z_prodH` left from the PROD-H pull), runs, tmp, upload |
| 10 | home `jobs/`, `runs/`, `logs/`, `results/` | `rmdir` (fails if not empty) | empty after rows 1–2 |

Afterwards, the executor prints the final campaign home tree, its `du`, and confirms that the scratch campaign folder is absent. A separate read-only call then takes the guard reading for `ops/FINAL_NOTS_STATE.md`.

## Round-1 fixes (Sol R1 ACCEPT WITH FIXES, `review/SOL_REVIEW_FINAL_NOTS_SWEEP.md`)
- **/tmp workspace (disclosed):** `remote_pack.sh delete` creates its own workspace `mktemp -d /tmp/fb31_rp.XXXXXX` and removes it through its EXIT trap. This is the same reviewed helper behind every campaign delete, and the workspace holds only the helper's manifest temp files. It is the only path outside the two campaign trees that the sweep creates or removes. v2 also verifies afterwards that no `/tmp/fb31_rp.*` workspace of fb31 is left, and refuses DONE otherwise.
- **Strict final checks:**
  - each home dir in row 10 must exist, be a real directory and be empty, or the executor stops;
  - the final campaign home top level must equal exactly `README.md code inputs manifests`;
  - `code/` must equal exactly `bench_v2 core ops v2_2`;
  - `inputs/` and `manifests/` must be empty;
  - `du`, the find statuses and the absence of scratch are all checked;
  - `FINAL_DELETE_DONE` prints only after every check passes.
- **Deadline:** the remote side runs under `timeout 270`, and the laptop shim also bounds the ssh at 300 s. The full output and exit status are saved locally.
