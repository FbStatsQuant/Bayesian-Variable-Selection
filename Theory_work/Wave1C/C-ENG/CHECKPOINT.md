# C-ENG — CHECKPOINT (written 2026-11-08 22:42 CST, ahead of the 01:30 checkpoint)

Branch `w1c/ls0-merge` (pushed to origin). Commits: 71ecd37 (PLAN v1.0), 5c14c4e (R01, PLAN v1.1), 9b9d234 (implementation),
b0c4511 (tests, R02/R03, PLAN v1.2), plus later commits.

## Done and checked
- **Implemented in the production core `Scripts/SMC_BVS/core/`** (switch `ls0`, default TRUE; `ls0 = FALSE` = v3):
  LS0 after the final local search (start mode, production ℓ, centre emitted, same ledger/cache, phase `ls0`, guard
  checkpoint `ls0`); e4 tie-aware DP (TDP-E) in `start_mode` on truncation; E3 before LS0; certificate on the returned
  HPM; `local_limit` = either cap; `ls0_improved` / `ls0_hpm_changed`; GUARD-W/#15 exact-name NA estimate fields; study
  adapter reads the NA markers.
- **Reviews:** R01 plan review REJECT → all 7 fixed (PLAN v1.1); R02 plan re-check REJECT on plan text → adapter (already in
  code), public-path gate, wording fixed (PLAN v1.2); **R03 code review of the diff: APPROVE, no findings**
  (`reviews/R03_code_review_raw.md`).
- **Tests (all PASS):** TDP-E 2 × 3000 random instances + W1-N3 p = 44 counterexample (now S*) + family + rounding/boundary
  fixtures (`numerics/out_test_tdp_seed*.txt`); cross-check vs W1-N3 reference TDP 600/600 (`numerics/out_xcheck_n3_tdp.txt`);
  LS0 fixtures 33/33, guard stop 9/9, numerical failure 5/5, public paths/forced stops 10/10 (`numerics/out_test_ls0_*.txt`);
  regression p = 30, S1–S6 × 4 reps × 2 scales = 48 datasets: LS0-off == old 48/48, LS0-on sampler identical 48/48, HPM
  unchanged 48/48, O-LS0 prototype replay identical 48/48 (`numerics/out_regress_p30.txt`).

## Running / left
- p = 500 replay of the 3 named designs (dev S1 r001, S4 r001, S5 r002) new core vs O-LS0 prototype — running locally.
- Existing `Scripts/SMC_BVS/tests` suite (prototype vs production, 3 configurations) — Sonnet helper running.
- `build/check_smokes.R` inspects saved Owls smoke records that do not exist locally: cannot run as is (will report).
- REPORT.md; citation check; second code review only if further code changes are made.

## Estimate
On track to close by 04:30. No HQ method requirement (e.g. ℓ_n schedule) received yet; the hook `v3.ls0_ell` / `ro$ls0_ell`
exists if one arrives.
