# PK_R01 design review — disposition (family PK lead, 2026-11-09)

Review: reviews/PK_R01_design.md (Codex gpt-6.1-sol high), verdict GO-WITH-FIXES. All six findings accepted.

1. MAJOR (conclusions not implied by statistics) — ACCEPTED. DESIGN.md v2: cap conclusions only from k_hit vs cap;
   scoring / arrival / certified endpoint separated; finite-n outcomes described as evidence/diagnostics, never as theorem
   contradictions. (Confirmed by our own R1 pilot: unsaturated start 1805 < K = 3000 with W = 69 and MR1 miss.)
2. MAJOR (partition validation misstated; validators do not fail) — ACCEPTED. History corrected (5/27 failures incl.
   (3001,16)); closed form replaced by next-fit packing of group sizes; validate_general.py / validate_s5_partition.py exit 1
   on any disagreement (validate_general also requires finite max |dF| < 1e-8); complete validation of the revised frozen
   scripts run as prerequisite RUN pk_val01; production released only after both exit 0.
3. MAJOR (move-limit censoring) — ACCEPTED. pk_common.trace_general: executed moves only (props[:moves]), `limited` flag
   (last scan still improving), assertion len(centres) = moves + 1; R1 driver: limited = n_moves >= 10^7. summarize.py v2
   excludes censored units from endpoint/m*/k_hit statistics and lists them.
4. MAJOR (numerical protection at large K) — ACCEPTED. NaN/+inf guards on every scan (abort, rc != 0); direct Cholesky
   re-scoring (bvs_core.Problem.F) of the centre + 5 best neighbours at scans 0, 1, every 250th, last, first 50 near-tie
   scans; recorded max |dF|, winner-order check, minimum winner margin; endpoints != S0 get direct F(final), F(S0).
   summarize flags |dF| > 1e-6 and order failures.
5. MAJOR (ingestion) — ACCEPTED. summarize.py v2 reconciles against the frozen task tables (unit = output file), collapses
   identical duplicates, excludes+lists conflicting ones, lists missing units, enforces one module-sha256 set.
6. MINOR (diagnostics) — ACCEPTED. R1 now records exact-tie counts, arrival, limit flag, NaN guards, minimum margin among
   evaluated candidates; event vs run counts separated; log-log slope table of median W implemented; k_hit_finite count
   shown next to the excess summary.
