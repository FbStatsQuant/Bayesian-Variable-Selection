# W2-SIM / LOC — log (family lead, Claude Opus 5.5). Times CST (local), 2026-11-09.

* 10:00 — read COMMON.md, INFRA.md, briefs/LOC.md, Wave2/PROTOCOL.md, W2-LOC2 REPORT/STATEMENT/numerics (D1_SUMMARY,
  d1_diag.py), W2-FAC-B numerics/bvs_core.py, W2-APP n3b_fastls.py, W2-SIM scripts/prod_fit.R, nots/*.
* 10:03 — deployed bvs_core.py ($CODE/Theory_work/Wave2/W2-FAC-B/numerics/) = git blob of 11dc9b7 with CRLF line endings
  (sha256 7e4d67ba…; LF content sha256 e8283f56… = `git show 11dc9b7:…`); identical after CR stripping.
* 10:05–10:15 — wrote LOC/scripts v1 (loc_core.py, loc_run.py, loc_batch.py, loc_validate.py, make_tasks.py,
  loc_prod_fit.R = copy of W2-SIM/scripts/prod_fit.R (sha256 a32a764d… of the working copy) + design = file). Local
  validation v1: 18/18 equal. R reads the exported X/y bit-identically.
* 10:16 — ssh alias `nots` (HostName 10.226.96.48) timed out; all later commands use `-o HostName=notsx.crc.rice.edu`
  (same NOTS login cluster). ~/.ssh/config not modified.
* 10:17 — submitted loc_pilot01 (job 2633109, 12 tasks, commons 12 h, 32G): NOTS validation v1 (ALL_EQUAL True), 7 large
  port runs, 4 production fits (n = 500, 2000).
* 10:26 — submitted loc_pilot02 (job 2633286, 6 tasks, commons 24 h): production n = 8000 (C1, C2, C3), PT 0.5 adj
  n = 2000/8000, eigcheck.
* 10:30 — pilot summary results/LOC/pilot_summary.md; design review R01 (Codex gpt-6.1-sol high) launched.
* 10:33 — kept seed: CSG(.5, .8) `one` n = 8000 seed 1 (pilot02 task 2): LS0 final = S₀ ∪ {1478}, F(final) − F(S₀) = +0.94;
  h at S₀ = 24.6 (2 log p = 15.2), top-6 h all in the truth group of 1485; fresh-noise simulation on that X:
  P(max_l h > 22.8) ≈ 2.5·10⁻⁴ (4000 draws); local seeds 2–8 of the same cell: final = S₀.
* 10:40 — R01 verdict NO-GO (9 MAJOR, 3 MINOR); saved verbatim reviews/LOC_R01_design.md; disposition
  reviews/LOC_R01_disposition.md (all accepted; #2 in part).
* 10:43–10:55 — v2: certified partition (+ fallback to bc.partition), LS safeguards (non-finite, adaptive window, spot
  checks, returned_prod), CSG arms one/one4/two/twoM, PT α = 10 control, new statistics (pure_deletion_to_S0,
  na margins, exhaustive NA at S₀, full paths, per-truth-group diagnostics), make_tasks v2 (main 4760 runs: 396 light
  + 800 heavy tasks; prod 180 fits), validation v2 (exit 1 on failure). DESIGN.md v2.
  Pilot timings (v1 code): AF 0.4 spread q n = 16000 port 879 s; production n = 8000 PT 1.5 1143 s; production CSG fits
  slower (C3 n = 2000 > 30 min).
* 10:58 — loc_pilot03 (job 2634688, v2 scripts dir sim/loc/scripts_v2): NOTS validation v2 + 9 smoke runs of new arms.
* 11:05 — pilot03 port runs (v2) all completed (results/LOC/pilot03/port). Kept seed #2: CSG(.5, .8) `two` n = 8000 seed 1:
  final ≠ S₀ (S₀ ∪ {1336}), na_at_S0_exhaustive = −0.037 (target failure: an addition in the truth group of 1305/1306 beats
  S₀; h = 22.4). Fresh-noise null on the same X (3000 draws): P(max_l h ≥ 22.4) = 2.3·10⁻³; for kept seed #1:
  P(max_l h ≥ 24.6) = 3.3·10⁻⁴. Both events in truth groups. Frequencies to be estimated by the main grid (10 seeds/cell).
  Added a truth-duplicate exact-tie case to loc_validate.py (tie rule exercised on add and delete steps; PASS locally).
