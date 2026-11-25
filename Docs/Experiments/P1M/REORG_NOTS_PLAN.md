# REORG NOTS plan (Phase 0, read-only), Opus-NOTS, 2026-11-25

Spec: `REORG_SPEC.md` (binding). ROOT = `/home/fb31/SMC-BVS`; `ROOT/scratch` → `/scratch/fb31/SMC-BVS`.
Inventory taken 2026-11-25 ~16:30–17:10Z: 4 serial `ssh nots` calls, niced, read-only; queue empty (`squeue -u fb31`: none); no crontab on NOTS.
Sizes are apparent bytes (`du --apparent-size` / `find -printf %s`). Raw data (Owls scratchpad): `scratch_files.tsv` (45,543 rows), `match.tsv` (each file vs desktop-verified units, matched by run-relative path + size).
Home quota now: **5,776 MB of 10,240 MB**.

## 1. Inventory

### Home (`/home/fb31`), SMC only
| path | bytes | content |
|---|---:|---|
| `~/SMC_Engineering_Department/scripts/` | 231,773,780 | 90 batch dirs (sbatch, submit.sh, build.sh, env.sh, manifests, bin/smcbvs4, cmake build dirs) |
| `~/SMC_Engineering_Department/crews/` | 43,641 | home_guard/ (log, orig/), laptop_route/ (test file + an `authorized_keys.bak-20261115`, public keys; moved as is, never opened) |
| `~/SMC_Engineering_Department/INDEX.md` | 5,020 | home index |
| `~/SMC_Engineering_Department/results/` | 4,096 | empty |
| `~/SMC_Engineering_Department/scratch` | symlink | → `/scratch/fb31/SMC_Engineering_Department` |
| `~/SMC_Theory_Department/W3-AUDIT-C/pkg/OFFLOADED_theory.txt` | 681 | Theory tombstone (only file) |
| `~/bin/home_guard.sh`, `~/bin/home_guard_job.sh` | 8,296 + 833 | Engineering's home guard (INDEX "owned by Engineering since 11-15") |

Not SMC, untouched: `~/projects` (v3 deploy, never touched), `~/archive` (4.9 MB, Sept quantile/ADMM/brantley work), `~/archive_control`, `~/lib`, `~/Python`, `~/R` (205 MB, BQTF libs), `~/bin/{check_project_paths.py,prepare_nots.sh,codex,__pycache__}`, `~/.cache` (276 KB, tool caches only, no SMC cache), `~/.claude-science-scratch`, `Bayesian-Quantile-Trend-Filtering` link, all dot-dirs, `~/.ssh`.

### Scratch (`/scratch/fb31`), SMC only
| path | files | bytes | content |
|---|---:|---:|---|
| `SMC_Engineering_Department/runs/` | 32,064 | 211,102,395,569 | see breakdown below (du incl. dirs: 211,107,327,153) |
| `.../archive/home_guard/` | 5 | 1,080,773,347 | 3 Claude-CLI builds moved by the guard (holding_20261111 341.9 MB, **atime 15.6 d**; holding_20261124 365.8 + 373.0 MB) + 2 OFFLOADED notes |
| `.../code_ws/VN_e993ece2_code/` | (~100k) | 353,474,015 | F2 worktree (protected per NOTS_SCRATCH_PROTECT.txt) |
| `.../vn_minileg/clone_e993ece2/` | 29 | 159,374,684 | shallow clone, source of that worktree (protected); commit e993ece2 is on origin/exp/P1M-engine |
| `.../slurm_out/` | 13,441 | 16,317 | wave Slurm logs (almost all empty files) |
| `.../{INDEX.md,gcd_setup_sha.txt,gcd_setup_verify.txt,gct2_inputs_sha.txt}` | 4 | 13,609 | scratch index + input checksums |
| `.../data/`, `.../tmp/` | 0 | 0 | empty dirs |
| `SMC_Theory_Department/W3-AUDIT-C/OFFLOADED_theory.txt` | 1 | 697 | tombstone |
| `theory_w2/`, `theory_w3/` | 1 + 1 | 1,162 + 654 | tombstones (data offloaded 11-18) |
| `w3scale/OFFLOADED_theory.txt` | 1 | 1,318 | tombstone |
| `w3scale/code/v32dev_6866f57/` | 28 | 1,878,266 | S31 code kept "until G0 closed"; Owls copy `records/W3-SCALE/w3scale/code` exists but W3-SCALE is **not** in desktop_verified.txt |
| `scr_{BVS,BVS_Paired,Exp_Mixture,v3prof,archive_staging}_MOVED.md` | 5 | 1,892 | Oct relocation tombstones of BVS data (destination `NOTS_BVS`) |

Not SMC, untouched: `BQTF/`, `qr_data/` (7.6 MB), `.claude-science/`, `qr_small_del2_MOVED.md`, `scr_backups_MOVED.md`, `scr_onizuka_MOVED.md` (destination `NOTS_scratch_other`), and the 4 relocation helpers `cksum_units.sh`, `del_unit.sh`, `mkchunks.sh`, `mkunits.sh` (shared by BVS and qr units; HQ 11-15 "untouched").

### `runs/` breakdown (32,064 files, 211,102,395,569 B)
| class | files | bytes | copy |
|---|---:|---:|---|
| R1a: the 64 protected GB_/RG_ `.bin` (protected.tsv) | 64 | 35,392,235,904 | 57 in `hygiene_20261124_nots/` (34,081,390,720) + 7 already in `gb/`, `rung1e5/` (1,310,845,184); all desktop-verified (name + size + unit sha; fresh NOTS sha in Phase 1) |
| R1b: other files with a desktop-verified copy: fit.bin ×16, law.bin ×4, eval.bin ×16, 1,636 json/jsonl/log | 1,672 | 5,286,540,906 | units `rung1e5/` 909, `gc1m/` 438, `gb/` 332 (files) |
| R2: small files with NO desktop copy (json 4,341, jsonl 2,094, log 1,773, sha256 350, txt 131, list 73, tsv 254, 33 `*_sacct.txt` at runs/ root, `RG_T6/.../t6/ref_island.bin` 221.8 MB) | 24,810 | 356,047,687 | none |
| R3: island_*.bin, NO copy anywhere | 5,518 | 170,067,571,072 | none (PL 83.91 GB, RG 43.10, VN 19.34, GB 14.28, OV 9.22, FREEZE 0.22) |

Atime: only the 11-11 CLI build is past 14 d; every `runs/` file is < 10 d.

## 2. Move table
Same-filesystem moves are `mv` renames (metadata only; atime kept). Cross-filesystem moves are `rsync -a`, then a per-file sha256 compare, then `rm` of the source.

| # | source | target | method | why |
|---|---|---|---|---|
| M1 | `~/SMC_Engineering_Department/` (whole) | `~/SMC-BVS/_local/engineering/` | `mv` (home FS) | spec layout |
| M2 | `~/SMC-BVS/_local/engineering/scratch` (old link) | removed | `rm` symlink | replaced by `ROOT/scratch` |
| M3 | `/scratch/fb31/SMC_Engineering_Department/` (whole) | `/scratch/fb31/SMC-BVS/` | `mv` (scratch FS) | spec: the scratch trees merge into SMC-BVS |
| M4 | — | `~/SMC-BVS/scratch` → `/scratch/fb31/SMC-BVS` | `ln -s` | the one allowed exception |
| M5 | `/scratch/fb31/SMC-BVS/vn_minileg/clone_e993ece2/` | `~/SMC-BVS/_wt/clone_e993ece2/` | rsync + sha + rm | spec `_wt` (code clones); protected F2 source, kept away from the purge |
| M6 | `/scratch/fb31/SMC-BVS/code_ws/VN_e993ece2_code/` | `~/SMC-BVS/_wt/VN_e993ece2_code/` | rsync + sha + rm, then `git -C _wt/clone_e993ece2 worktree repair ../VN_e993ece2_code` | same; the gitdir links are absolute, so repair is needed |
| M7 | `scripts/VN_ID_1/code` symlink | → `/home/fb31/SMC-BVS/_wt/VN_e993ece2_code` | `ln -sfn` | the only live `code` link; the other 13 already dangle (targets deleted 11-20 under H-41) and stay as provenance |
| M8 | `~/SMC_Theory_Department/W3-AUDIT-C/` | `~/SMC-BVS/_local/theory/W3-AUDIT-C/` | `mv`, then `rmdir ~/SMC_Theory_Department` | spec |
| M9 | the 4 scratch Theory tombstones (SMC_Theory_Department/W3-AUDIT-C, theory_w2, theory_w3) | `~/SMC-BVS/_local/theory/nots_tombstones/<old dir>/OFFLOADED_theory.txt` | copy + sha + rm, then `rmdir` the dirs | records of the 11-18 offload; home is safe from the purge |
| M10 | `w3scale/OFFLOADED_theory.txt` | `~/SMC-BVS/_local/engineering/records_nots/tombstones/w3scale/` | same | Engineering's (records/W3-SCALE) |
| M11 | the 5 BVS `*_MOVED.md` | `~/SMC-BVS/_local/engineering/records_nots/relocations_202610/` | same | SMC-BVS history; INDEX rows updated |
| M12 | scratch root `INDEX.md`, `gcd_setup_sha.txt`, `gcd_setup_verify.txt`, `gct2_inputs_sha.txt` | `~/SMC-BVS/_local/engineering/records_nots/scratch_root/` (INDEX as `INDEX_scratch_legacy.md`) | same | small records, kept off the purge |
| M13 | `~/bin/home_guard.sh`, `~/bin/home_guard_job.sh` | `~/SMC-BVS/_local/engineering/crews/home_guard/` | `mv` + path edits (§4) + a `--dry-run` test | SMC file; must keep working |
| M14 | `~/SMC-BVS/_local/engineering/INDEX.md` | `~/SMC-BVS/_local/engineering/INDEX_home_legacy.md` | `mv` | history kept; the fresh `ROOT/INDEX.md` replaces both indexes |
| M15 | empty `/scratch/fb31/SMC-BVS/{data,tmp,code_ws,vn_minileg}`, emptied `w3scale/code`, `w3scale/` | removed | `rmdir` | spec: `_local/tmp` is the only tmp area |
| — | `runs/` R3 islands, `archive/home_guard/` | stay in `/scratch/fb31/SMC-BVS/` via M3 | — | see decisions D1, D2 |

Nothing is left at `~/SMC_Engineering_Department` or `~/SMC_Theory_Department` on NOTS: no stub, because a stub would be a stray. The pointer is LAYOUT.md.

## 3. Delete list (each deletion only after a fresh NOTS sha256 equals the verified copy, taken in the same detached remote job)
| batch | items | bytes | verified copy |
|---|---:|---:|---|
| DA | R1a: 64 protected GB_/RG_ .bin | 35,392,235,904 | Owls `records/hygiene_20261124_nots/<batch>/<run>/` (57) and `gb/`, `rung1e5/` (7), SHA256SUMS; all 64 units are in `crews/offload/desktop_verified.txt` |
| DB | R1b: fit/law/eval.bin + 1,636 small files | 5,286,540,906 | `rung1e5/`, `gc1m/`, `gb/` units (desktop-verified), per-file sha from the unit's SHA256SUMS |
| DC | R2 small files (24,810) + slurm_out (13,441) + w3scale/code (28) | 357,942,270 | **new** Owls units: `records/hygiene_20261125_nots/runs_meta/` (a tar of R2 + slurm_out + the 4 scratch-root files, `MANIFEST.sha256` per member file computed on NOTS, `SHA256SUMS` for the unit) and `records/hygiene_20261125_nots/w3scale_code/` (28 files + SHA256SUMS). Delete only after both appear in desktop_verified.txt (hourly pull at :20) and `sha256sum -c MANIFEST` passes on NOTS. |
| — | **Total deleted** | **41,036,719,080** (41.04 GB) | |

Mechanics: a deletion list per batch (path, bytes, sha, unit) built on Owls from `match.tsv`; the NOTS job runs detached (`setsid nohup nice -n19 ionice -c3`, like gc_tier1) and re-hashes, then removes by literal path. Results come back as a TSV, are appended to `crews/home_hygiene/nots_scratch_removals.tsv`, and get one LOG line per batch. Hashing ≈ 41 GB takes about 15–25 min on the login node.
Order: DA/DB run at the old paths before M3, so the fences and paths stay as they were verified. M3 onward comes after. DC runs at the new paths after the desktop pull.

## Decisions for the manager / HQ
- **D1, R3 islands, 170,067,571,072 B, no copy.** H-41(4)/(5) class them as regenerable intermediates (the merges into fit/law.bin are done and desktop-verified). (a) **Recommended:** they ride M3 into `/scratch/fb31/SMC-BVS/runs/` and the 14-day purge takes them (all atimes < 10 d). (b) Delete now, which frees 170 GB at once but needs an explicit exception to the copy-first rule; 57,379,499,456 B of it is in the protected RG_/GB_ families. (c) Copy them first: 170 GB to Owls and the desktop (≈ 386 + 170 GB against the ≈ 700 GB cap), hours of transfer. Not recommended.
- **D2, archive/home_guard, 1,080,773,347 B** (3 reinstallable Claude-CLI builds). (a) **Recommended:** ride M3 and let the purge take them (the 11-11 one is already due). (b) Delete now (not records).
- **D3, batch scripts content.** 3,114 files under `scripts/` embed the old prefixes, and the run manifests hash those scripts. **Recommended:** do not rewrite them (provenance; no run is planned during the freeze). `env.sh` files hold no path (checked by grep). LAYOUT/INDEX record the prefix map: `/home/fb31/SMC_Engineering_Department` → `/home/fb31/SMC-BVS/_local/engineering`, `/scratch/fb31/SMC_Engineering_Department` → `/scratch/fb31/SMC-BVS`. A reused batch is re-pathed with a `sed` of those two prefixes at that time.
- **D4.** `_wt` on home costs +512,906,043 B of quota (5,776 → ≈ 6,265 MB, under the 7 GB target). The alternative is `/scratch/fb31/SMC-BVS/_wt`, where the purge applies.
- **Coordination with Opus-OWLS:** the DC units must land in whatever `records/` path the offload serves at that moment (old `~/SMC_Engineering_Department/records` or the new `_local/engineering/records`). The serve_pull and desktop_verified paths must not move between my rsync and the :20 pull. Tell me which path to use.

## 4. Path references to update
### NOTS (I apply them in Phase 1)
| file | line | new text |
|---|---|---|
| `crews/home_guard/home_guard.sh` (was ~/bin) | 14 | `... Moves (not deletes) go to /scratch/fb31/SMC-BVS/archive/home_guard/holding_*. Owner: SMC - Engineering (HQ, 11-15).` |
| same | 18 | `LOG="$HOME_DIR/SMC-BVS/_local/engineering/crews/home_guard/home_guard.log"` |
| same | 19 | `LOCK="$HOME_DIR/SMC-BVS/_local/tmp/home_guard.$(id -u).lock"` (0-byte; spec: `_local/tmp` is the only tmp area) |
| same | 22 | `HOLD="/scratch/fb31/SMC-BVS/archive/home_guard/holding_$(date +%Y%m%d)"` |
| `crews/home_guard/home_guard_job.sh` (unused chain) | 7, 11, 12, 15 | `/scratch/fb31/SMC_Engineering_Department/slurm_out/home_guard` → `/scratch/fb31/SMC-BVS/slurm_out/home_guard` (so `slurm_out/` stays as an empty dir) |
| same | 14 | `$HOME/SMC-BVS/_local/engineering/crews/home_guard/home_guard.sh` |
| `scripts/*/env.sh` | — | no change (no path inside) |
| `scripts/VN_ID_1/code` | symlink | M7 |
| `~/SMC-BVS/INDEX.md` | new | fresh index (tree, provenance, prefix map, exceptions, DELETED lines); old indexes kept as `*_legacy.md` |
| `~/SMC-BVS/LAYOUT.md` | new | verbatim copy of the committed Owls LAYOUT.md |

### Owls side (exact text; Opus-OWLS or the manager applies). Only the NOTS paths are listed; the Owls `H`/`DEPT`/`HERE` paths are Opus-OWLS's.
| file:line | old | new |
|---|---|---|
| `crews/home_hygiene/nots_wave_hygiene_check.py:27` | `S = '/scratch/fb31/SMC_Engineering_Department'` | `S = '/scratch/fb31/SMC-BVS'` |
| `…/nots_wave_hygiene_check.py:28` | `NH = '/home/fb31/SMC_Engineering_Department'                 # same path on NOTS home` | `NH = '/home/fb31/SMC-BVS/_local/engineering'                 # NOTS ROOT/_local/engineering` |
| `…/nots_wave_hygiene_check.py:109` | `f'[ -L $d/code ] && echo "L $d $(readlink $d/code)"; done\nls {S}/code_ws\nls {S} \| grep -E "^probe_"\n'` | `f'[ -L $d/code ] && echo "L $d $(readlink $d/code)"; done\nls /home/fb31/SMC-BVS/_wt\nls {S} \| grep -E "^probe_"\n'` |
| `…/nots_wave_hygiene_check.py:11,17,120` | text `code_ws` | `_wt` (doc/report text only) |
| `crews/home_hygiene/gc_fence.py:3` | `relative to /home/fb31/SMC_Engineering_Department/scratch/runs` | `relative to /home/fb31/SMC-BVS/scratch/runs` |
| `crews/home_hygiene/gc_fence.py:8` | `ROOT = "/home/fb31/SMC_Engineering_Department/scratch/runs"` | `ROOT = "/home/fb31/SMC-BVS/scratch/runs"` |
| `crews/home_hygiene/test_gc_fence.py:20,22` | every `/home/fb31/SMC_Engineering_Department/scratch` | `/home/fb31/SMC-BVS/scratch` (the refused `.../scratch/GC_W1/...` and `.../runs/../...` cases keep their shape) |
| `crews/home_hygiene/gc_tier1.py:6` | (`H` used for NOTS paths too) | add `NS = "/home/fb31/SMC-BVS/scratch"` after line 6 |
| `crews/home_hygiene/gc_tier1.py:53,63,64,65,80` | `"%s/scratch…" % H` / `(H, …)` for the NOTS paths | the same strings with `NS` in place of `H + "/scratch"` (line 63 has two occurrences; line 80: `"%s/runs/%s" % (NS, x["rel"])`) |
| `crews/nots_cleanup_20261124/nots_delete_verified.py:5,20` | `/scratch/fb31/SMC_Engineering_Department/runs/` | `/scratch/fb31/SMC-BVS/runs/` (one-off tool; only if it is reused) |
| `crews/home_hygiene/nots_home_prune.sh` | — | **no change**: it touches only `~/.t3` and `~/.vscode-server` on NOTS |
| `Docs/Experiments/P1M/machines/CREW.md:3` | `inside \`SMC_Engineering_Department\` on each machine` | `inside ROOT/_local/engineering on each machine (NOTS ROOT = ~/SMC-BVS, scratch via ~/SMC-BVS/scratch)` |
| `CREW.md:37` | `` `ls -1 /scratch/fb31/SMC_Engineering_Department/{runs,archive,data,code}` (depth 2) compared with the path column of `~/SMC_Engineering_Department/INDEX.md` `` | `` `ls -1 /scratch/fb31/SMC-BVS/{runs,archive,slurm_out}` and `ls -1 ~/SMC-BVS/{_local/*,_wt}` (depth 2) compared with `~/SMC-BVS/INDEX.md` `` |
| `CREW.md:38` | allowlist `{SMC_Engineering_Department, … theory_w2, theory_w3, w3scale, home_holding_*, home_guard, qr_data, .claude-science, the listed loose files}` | `{SMC-BVS, BQTF, qr_data, .claude-science, the 3 non-SMC *_MOVED.md + 4 relocation helpers}` |
| `CREW.md:41` | `du -s /scratch/fb31/SMC_Engineering_Department` … `tmp/` size | `du -s /scratch/fb31/SMC-BVS` … total |
| `CREW.md:42, 63` | `/scratch/fb31/SMC_Engineering_Department/tmp…` | `~/SMC-BVS/_local/tmp…` (scratch tmp/ is gone) |
| `CREW.md:43, 81, 138` | `~/home_guard.log` | `~/SMC-BVS/_local/engineering/crews/home_guard/home_guard.log` |
| `CREW.md:64` | `/scratch/fb31/SMC_Engineering_Department/{code,runs}/**` | `/scratch/fb31/SMC-BVS/runs/** and ~/SMC-BVS/_wt/**` |
| `CREW.md:80` | `` `~/bin/home_guard.sh` `` | `` `~/SMC-BVS/_local/engineering/crews/home_guard/home_guard.sh` `` |
| `CREW.md:88-89` | holding path sentence | `The guard's holding path is /scratch/fb31/SMC-BVS/archive/home_guard/holding_<date>/.` |
| **daily prompt** (scheduled tasks `f9847b84…` and `be4c26b5…`, both disabled now) step (a) | `WorkDir under SMC_Engineering_Department` | `WorkDir under /home/fb31/SMC-BVS or /scratch/fb31/SMC-BVS` |
| same, (a) | `~/bin/home_guard.sh` | `~/SMC-BVS/_local/engineering/crews/home_guard/home_guard.sh` |
| same, (a) | `the department folders ~/SMC_Engineering_Department and /scratch/fb31/SMC_Engineering_Department against their INDEX.md` | `the NOTS ROOT ~/SMC-BVS (incl. ~/SMC-BVS/scratch → /scratch/fb31/SMC-BVS) against ~/SMC-BVS/INDEX.md` |
| same, Scope line | `only the SMC_Engineering_Department folders, its NOTS scratch, the home guard` | `only ~/SMC-BVS on NOTS (with its scratch), Engineering's Owls ROOT/_local/engineering, the home guard` |
| `~/.config/bvs-hq/*` | — | no NOTS SMC path found (grep) |

## 5. Target tree (after Phase 1, with D1a/D2a)
```
~/SMC-BVS/                                   ≈ 745 MB on home (quota ≈ 6,265 MB of 10,240)
  LAYOUT.md, INDEX.md
  scratch -> /scratch/fb31/SMC-BVS
  _local/engineering/                        231.8 MB
     scripts/ (90 batches, unchanged), crews/{home_guard (+2 scripts), laptop_route}, results/ (empty),
     records_nots/{scratch_root, tombstones/w3scale, relocations_202610}  (≈ 20 KB),
     INDEX_home_legacy.md
  _local/theory/{W3-AUDIT-C/pkg, nots_tombstones}   ≈ 3 KB
  _local/{writing,papers,tmp}/              empty
  _wt/clone_e993ece2/                        159.4 MB
  _wt/VN_e993ece2_code/                      353.5 MB
/scratch/fb31/SMC-BVS/                       ≈ 171.15 GB, all purge-bound
  runs/<batch>/<run>/island_*.bin            170,067,571,072 B (5,518 files)
  archive/home_guard/holding_*               1,080,773,347 B
  slurm_out/                                 empty (guard chain / future jobs)
```
With D1b + D2b, scratch drops to ≈ 0 (empty `runs/`, `archive/`, `slurm_out/`).

## 6. Bytes
| | bytes |
|---|---:|
| **Deleted on NOTS** (DA + DB + DC) | **41,036,719,080** |
| **Copied to Owls** (new units runs_meta + w3scale_code; then desktop) | ≈ 357,955,879 (+ tar headers) |
| **Moved across filesystems** scratch → home (M5, M6, M9–M12) | 512,906,043 + 19,332 |
| **Renamed in place** (M1 home 231,826,537; M3 scratch 212,701,073,333; M8 681; M13 9,129) | metadata only |
| Left to the purge (D1a + D2a) | 171,148,344,419 |
| Extra if D1b + D2b | +171,148,344,419 deleted |

Scratch SMC: 212.72 GB now → 171.15 GB (D1a/D2a) or ≈ 0 (D1b/D2b). Home SMC: 0.232 GB → 0.745 GB.
Estimated Phase 1 wall time: ≈ 60–75 min, plus the wait for the next :20 desktop pull for DC.
