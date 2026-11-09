# C-ENG LOG

- 2026-11-08 21:22 CST: branch `w1c/ls0-merge` created from f16ce15. Read Wave1/Wave1C protocols, CORE, SPEC #6/#8-#10/#15/#26, SoP 02_method LS0 rows, W1-N3 STATEMENT/L7, O-LS0 prototype (`origin/theory/O-LS0`, ls0_exports.cpp, ls0_core.R).
- 21:24: `diff -rq --strip-trailing-cr Scripts/SMC_BVS/core STUDY/`: CORE = STUDY minus plain PIP and scored-set registry; start/score/blocks/calib/runtime/holder/Makevars identical. Decision: implement in CORE only.
- 21:25: local toolchain: R 4.6.1 ucrt + Rtools45; installed Rcpp 1.1.2 to user library; baseline CORE copy compiles via v3.R in 26 s.
- 21:27: PLAN.md v1.0 committed (71ecd37); sent to Codex gpt-6.1-sol (high) plan review R01.
- 21:30: timing: one old-core v3_fit at n = 100, p = 30 (S3) = 6.9 s wall. Old-core regression baseline (48 fits) started in background.
- 21:34: R01 received: REJECT as written, 1 BLOCKER (NA fields on LS0 stop), 4 MAJOR, 2 MINOR; all accepted (reviews/R01_disposition.md). PLAN v1.1; TDP_E.md hypotheses added. R02 (fresh plan re-check) launched in parallel with coding.
