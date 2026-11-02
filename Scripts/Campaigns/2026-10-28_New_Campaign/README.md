# New Campaign (2026-10-28): vetted code, job bundles and their review records

This folder is a byte-exact mirror of the campaign's code folders, keeping their relative paths, so bundles still resolve one another. Snapshot taken 2026-11-02. Only frozen or approved code that was actually used is here, together with the reviews and fix records that vetted it. The decisions behind it are in `Docs/HQ/DECISIONS.md` (D1–D70); the plan is in `Docs/PLAN.md`.

**Verify everything** (run from the repo root):
```sh
sh Scripts/Campaigns/2026-10-28_New_Campaign/verify_manifests.sh
```
The script prints one PASS/FAIL line per manifest and exits 0 only if nothing fails. `EXPECTED_MISMATCHES.tsv` lists the documented supersessions: entries of the 2026-10-29 LOWP ledger block that later ledger entries replaced. Those are tolerated; anything else fails.

## What is here

| Path | What | Manifest (headline sha256) | Used by |
|---|---|---|---|
| `code/CODE_LEDGER.md` | Provenance of every tree: authors, reviews, manifests, regressions | — | all |
| `code/core/v2_2_1/` | **SMC-BVS v2.2.1, FROZEN.** Core byte-identical to v2.2. Study layer: regimes H/L, low-p repeats, P5 retry; `tools/p5_scan.R` | `code/core/v2_2_1.SHA256SUMS` `d880afdb…13e1` (27) | pilot rev 7d, PROD-L, PROD-H |
| `code/core/v2_2/` | v2.2: plain PIPs, scored-model registry, instrumentation | `code/core/v2_2.SHA256SUMS` (25) | CONF_NOTS_IDENTITY gate |
| `code/lowp/` | Low-p study: spec, generator, sealing and verification (`R/`), exact enumerator (`enum/`), pilot bundle rev 7d (`pilot/`), tests | CODE_LEDGER LOWP block + rev-7d block | pilot, PROD-L |
| `code/bench_lowp/` | The 8 benchmark methods adapted to p ≤ 30 (ADAPTATIONS LA-1–LA-4), r2 | `code/bench_v2/lowp_port/BENCH_LOWP_MANIFEST_SHA256_r2.txt` `85a18248…a6b7` (34) | PROD_L_BENCH |
| `code/bench_v2/` | p ≫ n F1–F3 adapters with the adaptive-lasso lasso-`cv_min` pilot fix (D42), coefficient evidence; SPEC, CHANGES, tests, Sol reviews | `code/bench_v2/MANIFEST_SHA256.txt` `8905f52e…b373` (23) | BENCH_F3_DEV/PROD |
| `code/scoring/` | Metrics, theory measures (π₀, TD audit, miss classes), headline tables | CODE_LEDGER LOWP block | analysis threads |
| `code/review/` | Sol reviews of the LOWP build | — | — |
| `conformance/` | Conformance verdict, patches, regression record, output fields | — | — |
| `conformance/jobs/CONF_NOTS_IDENTITY/` | NOTS identity gate for v2.2 (job 2455971, D20) with comparator `cmp2.R` | `v2_2.SHA256SUMS` copy | — |
| `conformance/jobs/PROD_H/` | p ≫ n production bundle, 2,400 fits (run `20261030T0934Z_prodH`); `REVIEW2_FIXES.md` … `REVIEW7_FIXES.md` | `BUNDLE_SHA256SUMS` `2a2a8b1f…` (53) | — |
| `conformance/review/` | Sol reviews: conformance, regression, CONF-2b rounds 1–7, pilot rev 7d, identity result | — | — |
| `jobs/PROD_L/` | Low-p production: enumeration, SMC primary, 100×5 repeats (run `20261030T1811Z_lowp_prodL`) | built at staging by `stage_local.sh` (no static ledger) | — |
| `jobs/PROD_L_BENCH/` | Low-p benchmark wave (run `20261102T1311Z_lowp_bench`) | `BUNDLE_SHA256SUMS.txt` `2a7ceba7…dfc3` (32) | — |
| `bench_audit/AUDIT.md`, `bench_audit/review/` | Lasso/EN/aLasso/ABESS full-chain audit and its Sol reviews (D35, D42) | — | — |
| `bench_audit/jobs/BENCH_F3_DEV/`, `BENCH_F3_PROD/` | Adaptive-lasso dev pilot (26/26) and the production rerun (run `20261102T1252Z_bench_f3v2_prod`) | `BUNDLE_SHA256SUMS_FINAL` DEV `3353b6f6…` (26), PROD `90579ad6…7e07` (63) | — |
| `bench_audit/jobs/staging/` | The exact staged upload snapshots for the dev and prod runs | `UPLOAD_SHA256.txt` (34 each) | — |
| `ops/` | `guard.sh` (disk guard), `disk_check.sh`, `verify_against_local.py`, `transfer/` (`nots_pull.py`, `remote_pack.sh`, `verified_delete.sh`), `scaffold/` (incl. the `sshlock/` ssh lock shim and run chains), `review/` (Sol reviews of the deletion lists) | — | OPS |

## Also added by this import, outside this folder
- `Scripts/Benchmarks/<Method>/…`: 16 ledgered files of the n = 200 benchmark study that the repo lacked, mostly dev and test scaffolding.
- `Scripts/Archive/bench20261019/Benchmarks/…`: 20 ledgered versions of files the repo already holds in a different version. Kept for provenance; the repo's `Scripts/Benchmarks` copies are unchanged. Open point: for A1/A3, which version was frozen into the c = 1 run can only be settled from that run's code snapshot.

## Not here, by design
- Regression harnesses and outputs (`conformance/work/`, 154 MB), audit work folders, pilot and run outputs, `.rds` results, logs, transfer receipts, `__pycache__`/`.cpp_cache`.
- `code/core/v2_1_baseline/`: byte-identical to the repo's `Scripts/SMC_BVS/` (24/24 files).
- Live OPS progress logs: added after the campaign (`Docs/SYNC_LATER.md`).

## Rules for this code
- **Frozen means frozen.** Never edit a file here in place. A change needs a new version (e.g. v2.2.2), a regression, a Sol review and a new CODE_LEDGER entry.
- **Paths.** The scripts contain the NOTS paths they ran with (`/home/fb31/projects/BVS/New_Campaign`, `/scratch/fb31/New_Campaign`). Bundles read manifests at run time, so a hash is never hard-coded.
- **Line endings.** Several files are CRLF and the manifests hash the exact bytes. `.gitattributes` sets `-text` here, so no clone converts line endings.
- **Ignored file types.** A few manifest-covered fixtures and test logs have `.rds`, `.log` or `.out` extensions, which the root `.gitignore` excludes elsewhere. They are re-included by negation rules in `.gitignore`: `.log` and `.out` under this folder, and the seven small `.rds` test fixtures of BENCH_F3_PROD.
