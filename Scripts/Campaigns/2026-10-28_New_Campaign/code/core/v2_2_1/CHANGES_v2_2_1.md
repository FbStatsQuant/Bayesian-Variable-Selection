# v2.2.1 versus v2.2 (CONF, 2026-10-29)

v2.2.1 = v2.2 core, byte-identical, plus one merged study layer. Diff: `../v2_2_1.diff`; manifest: `../v2_2_1.SHA256SUMS`; ledger: `code/CODE_LEDGER.md`.

| File | Change | Authority |
|---|---|---|
| `core/**` | none (byte-identical to `v2_2.SHA256SUMS`) | D19 |
| `study/adapter.R` | (1) regime table `smcbvs_regimes()`: H = v2.2's bases, manifest names, strict input record; L = the LOWP runner's (`code/lowp/smc/adapter_lowp.R`, changes A3-A10) bases, I1 manifest, relaxed extras, `fold_sha256` column. (2) `smcbvs_case_spec(..., repeat_m)`: accepts p0020/p0030/p0500/p1000; repeat m = 1..5 for regime L only; `record$case` keeps v2.2's layout in H and the LOWP runner's in L. (3) `study`/`regime` columns from the regime. (4) `smcbvs_study_fit(..., repeat_m, p5_retry)`: `SMCBVS_rep{m}` prefix; P5 rerun (`smcbvs_p5_primary`, `P5_retry/` subfolder, doubled allocation, `record$p5`). (5) `adapter_version = "2.2.1-R1"`. (6) return value adds `stop`. | D11, D14, D16, D19; LOWP_SPEC L.3; master sec. II.7 |
| `study/run_case.R` | `--repeat m`, `--p5-retry`; a last stdout line of key=value fields with the stop phase | D11, P2 |
| `study/SCHEMA.md`, `study/README.md` | v2.2.1 section / paragraph | |
| `tools/p5_scan.R` (new, outside `study/`, so not in `source_sha256`) | P5 table per run: primary and rerun status and stop phase, eligibility | D11 |

Unchanged on purpose: CSV schema (88 columns), R-1 policy and status map, diagnostics, hashes, lock, `.done` last, resume and identity rules, path guards, the core call `v3_fit(X, y, method_seed, allocation)`. `code/lowp/smc/` (the LOWP fork) is retired in favour of this tree; see its README.

## Review fixes (Sol, `conformance/review/CONF2B_REVIEW1_sol.md`; CONF-2b, 2026-10-29)

| Finding | File | Fix |
|---|---|---|
| F1 (blocking) | `study/adapter.R` | All checks are repeated **under the unit lock**: identity (refuses a new mismatch), completion (a unit that another caller committed in the meantime is returned as skipped, never refit or overwritten) and, for a P5 rerun, the primary binding (same, still valid `resource_limit` primary, same `.sha256` lines). This applies to the primary and the rerun path alike. |
| F2 | `study/adapter.R` | In regime H, `n`, `kind` and `scales` are always checked, so a named NULL is refused as in v2.2. Regime L keeps "checked when present". The lookups use `[[ ]]` (no partial matching). |
| F3 | `tools/p5_scan.R` | A rerun counts as done only if it is **bound** to its primary: the same run, case, seed, source, policy and input hashes; allocation exactly ×2 with a consistent hash; `record$p5` naming this primary's `.sha256` lines. Otherwise the state is `invalid_inspect`, with `retry_problem`. Every unit's RDS is read, and its `record$native_status` (the field the rerun itself checks; no fallback to `fit$status`, Sol review 2 R2-3; absent means invalid) must equal the CSV `v3_status` in both directions: for a rerun the state is `invalid_inspect`; for a primary the scan refuses (exit 1). |
| F4 | `study/adapter.R` | A skipped (already valid) unit returns its saved `native_status` and `fit$instrumentation$stop`, so `run_case.R` prints the stop phase on resume too. |
| F7 | `tools/p5_scan.R` | Any rerun artefact (rds, csv, sha256, done, lock, temporary files) counts as present (`retry_artefacts`). New states `locked` and `invalid_inspect`; a new column `launchable` = eligible and no artefact at all (only these may be launched). The summary line appends `launchable=`, `locked=`, `invalid_inspect=` after its first six fields, which keep their order. |

No numerical path changed. The core and the CSV schema are unchanged.

## FROZEN (2026-10-29, CONF-2b)

**v2.2.1 is FROZEN.** It is the single SMC-BVS code tree for PILOT, PROD-L and PROD-H (D19).

- Authority: Sol review 3, Part A, "YES, ready to FREEZE" (`conformance/review/CONF2B_REVIEW3_sol.md`). That review verified all 27 manifest hashes (manifest sha256 df4e7cf0e20981ef9fe4632fe2280355cbdb9e15d2dd724f1615b2c232054c41) and a core byte-identical to v2.2.
- This FROZEN section is the only change since that review. It changes the hash of this file alone; the final manifest is recorded in `code/CODE_LEDGER.md`.
- Any later change needs a new version number, a regression and a review.
