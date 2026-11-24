# NOTS cleanup pass 2026-11-24 (owner order via HQ; Engineering sub-agent, run from Owls)

Logs (Owls): `~/SMC_Engineering_Department/crews/nots_cleanup_20261124/` = usage_before.txt, plan.tsv, deleted.tsv, doubt.tsv, inventory.tsv, usage_after.txt.
Etiquette kept: 7 serial ssh calls to NOTS in ~17 min plus the two report-only tools (3 short logins, 2 niced ssh), all `timeout 300`, nice/ionice, no sbatch/srun, queue empty throughout.

## Result: almost nothing in the authorised classes was trash
| class | scanned | deleted |
|---|---|---|
| c1 caches | `~/.cache` is 308 KB (no pip/uv/hf/torch/npm/Trash), `~/.conda` has one txt | 0 |
| c2 pycache | whole home dept + scratch dept trees | 1 pyc + its dir (`scripts/RG_T6/__pycache__`, 17.6 KB) |
| c3 core dumps | 0 found (7 dirs named `core` are source packages) | 0 |
| c4 slurm logs > 7 d | `scratch/slurm_out` 13,442 files, 0 older than 7 d | 0 |
| c5 tmp | home `tmp/` empty -> removed (4 KB); scratch `tmp/` already empty | 1 dir |
| c6 failed run dirs | none qualify (all have fit/eval outputs or sidecars, or are cited in LEDGER/LOG) | 0 |
Total freed by me: 25,794 bytes (3 rows in deleted.tsv, removals.tsv, NOTS INDEX.md DELETED line).
`nots_home_prune.sh` (report-only): nothing to prune (1 T3 nightly + 1 VS Code server, both kept). `nots_wave_hygiene_check.py` (report-only): 0 cores, 0 duplicate build dirs, T3 candidates 174 files / 22.16 GB.

## Usage before -> after
- Home quota 6,344 MB -> 5,771 MB of 10,240. NOT my doing: `~/.t3` shrank 1.6 G -> 606 M (T3 nightly cleanup, concurrent) before my deletes; `.codex` grew 0.70 -> 1.2 G. Biggest home items now: `.vscode-server` 2.6 G (1.8 G extensions, openai.chatgpt 1.1 G; not trash), `.codex` 1.2 G, `.t3` 0.6 G, `.claude` 0.4 G.
- Our scratch `runs/`: 370.2 GB before and after (PL 120.4, GC 111.0, RG 73.1, GB 25.2, VN 22.7, OV 17.6). `/scratch` 83 % system-wide, unchanged. `/rhf/allocations/ea14` (group allocation, not ours) untouched.

## Doubt (not deleted): 176 rows, 22.16 GB + 0.45 GB
- 174 files / 22.16 GB = the wave-check T3 list (calib 8.09 GB x1, data 10.07 GB x132, setup 4.00 GB x41). The tool cannot split by kind and the list holds setup records, so `--apply-trash` was NOT run (your rule). Same files are in inventory.tsv.
- `GC_T2THR/6-AR-n200-r01-V-s1` (6.6 KB) and `RG_T6/5-AR-n200-r01-V-s1` (443.6 MB): cited in LEDGER/LOG and (RG) protected, so not trash.

## Inventory for agent 2 (regenerable *.bin: calib/setup/data/raw), 194.49 GB in 1,007 files
- No copy in Owls records, so not verified anywhere: **166.54 GB** (all of GC 111.0 GB, plus PL/RG/OV/VN/GB remainders).
- Name+size match in a unit listed in desktop_verified.txt: **27.95 GB** (includes the 22.16 GB T3 list). Match is by name and size against the unit's SHA256SUMS; the NOTS side was not re-hashed here, so agent 2 must sha-check before deleting.
- Warning: the wave check shows the oldest unprotected atimes will hit the 14-day scratch purge in 7-10 days (PL 8 d, OV 7 d, GC/"other" 9-10 d).

## Refused / kept on purpose
- Everything under the never-touch list; `.vscode-server` extensions and `data/CachedExtensionVSIXs` (4.4 MB), `.t3/userdata/logs` (105 MB), `.codex`, `.claude` (outside classes c1-c6); `~/.cache` tool dirs (a few KB, not worth it).
- No run dir, island, fit/law/eval, data/setup/calib/raw file, or RG/GB/F2 item was deleted.
