# W3-SCALE leg A — log (times CT)

Agents so far: lead = Claude Fable 5.2, effort high, Claude Work (`claudeAgent`). Reviewers: none started yet.

## NOTS admission ledger (hard cap 150 task-hours)

| # | time (CT) | job | tasks × limit | worst case admitted (h) | cumulative worst case (h) | actual (sacct, h) |
|---|---|---|---|---|---|---|

## Entries

- 2026-11-11 19:05 — Started. `git switch -c theory/W3-SCALE` at 613f063. Read BRIEF, SCALING_DESIGN_v0, RERUN_SPEC,
  scaling_scratch (RESULTS, bench.cpp), Wave3 PROTOCOL, HOLDS (main checkout: no holds), and the whole v3.1 core
  (R drivers and C++ headers).
- 19:16 — NOTS reconnaissance (`ssh nots`, read-only). Only fb31 jobs: W3-P6 smoke `w3p6_smk1_v3` (4 tasks, commons).
  Partitions: commons 24 h (sapphirerapids 192 CPUs / 257 GB; cascadelake), scavenge 1 h. Home quota 10,026 of
  10,240 MB used, so the W3-SCALE workspace goes to `/scratch/fb31/w3scale`.
- 19:20 — PROD-H inputs and results were relocated off NOTS on 2026-11-03 (`bench20261019/RELOCATED_20261103.md`); the
  OneDrive mirror "NOTS Data" is not on this PC (DESKTOP-955G53S). The generator (`Scripts/Data_generators/gen_prod_data.R`)
  and the input manifest with x/y sha256 (`~/projects/BVS/Data_Generation/manifests/high_p/inputs_manifest.csv`) are on
  NOTS, so PROD-H inputs can be regenerated there and checked against the manifest. The old v2.2.1 records (needed for
  A1–A8 against the old study and for the sd(log Ẑ_r) table) are not reachable from here yet.
- 19:25 — PLAN.md written.
