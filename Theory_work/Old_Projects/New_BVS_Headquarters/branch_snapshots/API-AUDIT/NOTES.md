# API-AUDIT working notes (R10 CODE-AUDIT)

- 2026-11-02. Engine fingerprints at this branch (e58a949; last commit touching core: 39db138) equal those in
  W5-LOCKBOOK/AUDIT.md (sha256 prefixes v3_engine.h 0a0b95ab126bc23b, v3_core.cpp 64c0a38c569f0abc, v3_runtime.h
  f28e73c129bab734, v3_ledger.h 7641811d73e635bf, v3_score.h 41173ac1460e180e, v3_start.h 19e0a0bd0e479490, v3_run.R
  330b9f8347c1e4f3, v3_fit.R 656f11d704e566c8, v3_calib.R 268aa414e811af96). W5's line references re-read: all hold.
- Production v3 has no LS0 call site (every local_search call passes emit_centre = false, centre = led->hpmS:
  v3_core.cpp:447, 610, 657). LS0 exists only in the O-LS0 testing export (theory/O-LS0 ls0_exports.cpp,
  cpp_final_run_ls0), which calls local_search(start_mode, ell, tier, emit_centre = true, -2) on the SAME ledger and
  cache after the final local search.
- R and Rcpp exist on Owls (R 4.6.0), unlike W5's container: VAL-FP can be measured by a replay.
- 2026-11-02 (resume run). Ran the threshold-log pipeline on fits 1–10 (logging core reproduces production log_Z_r
  bitwise; all tag sequences aligned). Added an exact count of index-draw rounding flips (k ≤ 256). The first-order eps
  is ≤ 2.2e-6 per final run, with resampling dominant. Confirmed the stopped-fit hazard: `fit$log_Z` partially
  matches `log_Zbar0`. Wrote REPORT.md (verdicts per fact). Close.
