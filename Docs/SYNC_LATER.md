# Sync later: what to refresh when the experimental phase ends

This repo content is a **snapshot taken 2026-11-02 ~15:30Z**, while the New Campaign was still running. OPS-4, ANALYSIS-L and ANALYSIS-H2 were live, and the BENCH_F3_PROD and PROD_L_BENCH runs were queued. Before the cutover push, refresh the items below from the old project folder (OLD = the old local project root, `02_Experiments/I_2026-10-28_New_Campaign/` = I), then re-run the checks at the end.

## 1. Campaign records (replace the snapshot copies)
| Repo path | Source | Why |
|---|---|---|
| `Docs/HQ/DECISIONS.md` and `Docs/Campaigns/2026-10-28_New_Campaign/DECISIONS.md` | `I/DECISIONS.md` | D70 was the last entry at snapshot time; final decisions (F1 disposition, lasso headline, freeze, etc.) |
| `Docs/Campaigns/2026-10-28_New_Campaign/STATUS.md` | `I/STATUS.md` | the final board (all rows DONE) |
| `Docs/Campaigns/2026-10-28_New_Campaign/CHARTER.md` | `I/CHARTER.md` | only if amended |
| `Docs/PLAN.md` §2 | rewrite from the final STATUS/DECISIONS | "as of" table → final state |
| `Docs/THEORY_PRIORITIES.md` §5 | the final EVIDENCE_H/L | replace the preliminary findings, keep the "preliminary" banner off only once Sol has accepted them |

Apply the same path redaction as the snapshot (`Docs/PUSH_CHECKLIST.md` §3).

## 2. Results and analysis outputs (new; small reports and tables only)
Destination: `Results/2026-10-28_New_Campaign/`.
- `I/analysis/H2_20261102/`: `HEADLINE_H.md`, `EVIDENCE_H.md`, `tables/*.md` and the small CSVs (≤ 5 MiB each), plus `review/` and `tieout/` verdicts.
  - Exclude `case_theory_H.csv` if it exceeds 5 MiB, and all `logs/`, `extract/` and `repro/` bulk.
  - The canary key file must be moved into `tieout/` by that thread first.
- `I/analysis/L_20261102/`: `HEADLINE_L.md`, `EVIDENCE_L.md`, stability/reconciliation tables, `review/`, `tieout/`.
  - Exclude `work/`, `logs/`, chunk outputs, and `STAGED_SHA256_prodL.txt` if over budget (keep its sha256 in a receipt).
- `I/analysis/H_existing_20261030/`: `HEADLINE_H.md`, `BENCH_FLAGS.md`, `BENCH_OPEN_ITEMS.md`, `review/` (history of the 10-23 fits).
- Benchmark result tables after BENCH_F3_PROD (aLasso v2 rows) and PROD_L_BENCH (low-p benchmark rows, `accept_bench.R` verdict).
- The `I/ops/` completion reports: `PRODH_COMPLETION_20261102.md`, the PROD-L completion and accounting reports, F3 PROD and PLB completion, and `I/review/SOL_REVIEW_PRODH_COMPLETION.md`.

## 3. Ops records (now; live at snapshot time)
Destination: `Scripts/Campaigns/2026-10-28_New_Campaign/ops/`.
- Final versions of `OPS_LOG.md`, `DISK_LOG.md`, `CLEANUP_LOG.md`, `CLEANUP_PLAN.md`, `NOTS_INVENTORY.md`, `NOTS_ENV.md`, and `OPS4_PROGRESS.md` … `OPS9_PLB_PROGRESS.md`.
- The `ops/scaffold/` scripts, if any changed after the snapshot (chains, `pull_list.sh` v2): re-hash and re-copy.
- Transfer receipts: do not import them all. Write one receipt index (run ID → manifest sha256 → local/Owls location) to `Docs/Records/DATA_INDEX.md`.

## 4. Code: only if changed after the snapshot
Compare each manifest's headline hash against `Scripts/Campaigns/2026-10-28_New_Campaign/code/CODE_LEDGER.md`. Any new ledger entry (e.g. a v2.2.2, or a bench fix) means re-copying that tree with its review records.
- `jobs/PROD_L/` changed after its READY status (D58 cleanup fix, D63 scan limit). The snapshot copy is the one on disk on 2026-11-02; re-check it against the final ledger.
- `bench_audit/jobs/BENCH_F3_PROD/`: if OPS edited the resources or the run JOB.md during the run.

## 5. Bulk data (never into Git)
- Move or copy the campaign data mirror (PC OneDrive "NOTS Data/New_Campaign": inputs, results, logs, runs) to Owls `/home/fb31/BVS_GH/_data/New_Campaign/`.
  - Use `tar` + `scp` in a few batches, then a sha256 manifest check on Owls.
  - Check the Owls quota first.
  - `_data/` is git-ignored.
- Earlier archives (PC "NOTS_BVS", NOTS_home_archive) stay where they are; record their locations in `Docs/Records/DATA_INDEX.md`.

## 6. Handoff records
- Update `Docs/Records/GH_HANDOFF/GAP_LIST.md` with what was closed.
- Write the cutover acceptance report (`ASTRA_HANDOFF_PLAN.md` §D step 6).
- Record the final commit Felipe pushed in `Docs/HQ/STATUS.md`.

## 7. After the refresh, before Felipe pushes
1. From the repo root: `sh Scripts/Campaigns/2026-10-28_New_Campaign/verify_manifests.sh`. Every line must PASS.
2. Re-run the hygiene scan of `Docs/PUSH_CHECKLIST.md` §2 on the new files.
3. Size check: `git ls-files -z | xargs -0 du -cb | tail -1` < 250 MiB, and no file over 50 MiB.
4. `git status` shows only intended additions; `_data/` is ignored.
