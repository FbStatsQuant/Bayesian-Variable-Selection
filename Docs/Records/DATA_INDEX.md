# Data index: where the New Campaign's bulk data lives (not in Git)

Written 2026-11-03 for the GitHub refresh. Bulk data never enters this repo. The authoritative per-run table, with bundle MANIFEST sha256 values, job IDs and outcomes, is `Scripts/Campaigns/2026-10-28_New_Campaign/ops/FINAL_NOTS_STATE.md`.

## Locations

| Store | What | Notes |
|---|---|---|
| **Felipe's PC**, OneDrive "NOTS Data/New_Campaign/" | Every run's `inputs/`, `results/<run_id>/`, `logs/<run_id>/`, `runs/<run_id>/` (home summaries, uploads, acceptance), `nots_home_final/`, `nots_scratch_final/` | The campaign data mirror. Each piece was sha256-verified against its NOTS manifest before the NOTS copy was deleted (`ops/OPS_LOG.md`, PULL … VERIFIED lines) |
| **Felipe's PC**, OneDrive "NOTS Data/NOTS_home_archive/" | D31 archive-then-erase material (old Quant_Reg tarballs, Codex db-backups) | Not BVS results |
| **Felipe's PC**, "Documents/NOTS_BVS" | Earlier campaigns: the 2026-10-23 v2.1 production fits, the bench20261019 benchmark study, v3 profiling, Owls migration copies | Durable relocation manifests in its `_scripts/sha/` |
| **Owls** `/home/fb31/BVS_GH/_data/` (git-ignored) | Intended always-on bulk store | **Empty.** Moving data there is Felipe's call (check the Owls quota first) |
| **NOTS** | Only 2.4 MB of frozen code in `/home/fb31/projects/BVS/New_Campaign` | Scratch `New_Campaign` was removed (D93). The benchmark-freeze trees are untouched |

## Runs (summary; hashes in FINAL_NOTS_STATE)

| Run ID | Content | Results manifest(s) |
|---|---|---|
| `20261030T0934Z_prodH` | PROD-H, 2,400 SMC fits, p ∈ {500, 1000} | p0500 `7893396c…`, p1000 `a0196198…`, logs `8048e0b8…` |
| `20261030T1811Z_lowp_prodL` | PROD-L enum20/enum30/smc/smcrep, p ∈ {20, 30} | see FINAL_NOTS_STATE (four result pieces + logs) |
| `20261030T1855Z_bench_f3v2_dev` | BENCH_F3_DEV, 26 fits | see FINAL_NOTS_STATE |
| `20261102T1252Z_bench_f3v2_prod` | BENCH_F3_PROD, 2,400 aLasso fits | p0500 `e2600c82…`, p1000 `6b61c4b2…`, logs `5c96e7f6…` |
| `20261102T2309Z_lowp_bench` | PROD_L_BENCH rev 2, 8 methods × 2,400 cases | results `0dd8ced3…`, logs `0b8bc30d…` |
| `20261102T1311Z_lowp_bench` | PROD_L_BENCH rev 1 (failed, D82) | evidence logs only |

## Analysis outputs kept out of the repo (in the old project's campaign `analysis/` folders)

These are per-fit or per-case data rows and working areas. The repo keeps the reports, the aggregated tables, the tie-outs and the reviews (`Results/2026-10-28_New_Campaign/`):
- per-case tables: `L_20261102/case_theory.csv` (2.2 MB), `H2_20261102/case_theory_H.csv` (1.6 MB);
- per-fit tables: `H2_20261102/tables/smc_h2_per_fit.csv`, `tables/f3/f3_new_rows.csv`, `H_existing_20261030/tables/smc_per_fit.csv`;
- other case-level rows:
  - `H2_20261102/tables/{ev_case_derived, ev_td0_cases, ev_stops, ev_td0_diagnosis, ev_td0_diagnosis_b}.csv`;
  - `H2_20261102/tieout/terra_code/pi50.csv` and `pi51.csv`;
  - `L_20261102/abess_check/{test.csv, test_cases.txt}`;
  - `H_existing_20261030/tables/resource_limit_fits.csv`;
  - the generated fit outputs under `H2_20261102/tests/out*/`.

  The reports cite some of these files by name; they remain in the old project folder;
- the per-case ABESS check `L_20261102/abess_check/abess_size_check.csv` (its summary is in the repo);
- the reproduction detail `H2_20261102/repro/repro_detail.tsv` (its summary and mismatch list are in the repo);
- scoring outputs `L_20261102/score_final*/` (≈ 35 MB each), `work/` (465 MB), and H2 `extract/` and `theory/` (≈ 10,000 small files);
- superseded pre-benchmark and pre-F3 tables, Sol scratch folders, and tie-out copies of the frozen core.
