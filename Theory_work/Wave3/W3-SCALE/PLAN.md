# W3-SCALE leg A — plan (lead, 2026-11-11)

Branch `theory/W3-SCALE` (base main 613f063). Brief: `BRIEF.md`. Stop at `CHECKPOINT_1.md`.

## Order of work
1. **Profile v3.1 on NOTS** (submitted before any coding). Driver `scripts/profile_fit.R`: the `v3_fit` flow of the
   unmodified v3.1 core, phase by phase, with wall time and peak memory (VmHWM, reset per phase) recorded after every
   phase and a progress file written as it goes. The LS0 worst-case preflight is evaluated and recorded, but only the
   shipped memory-only preflight gates the run ("preflight bypassed in a copy", SCALING_DESIGN_v0 §6.1 set A).
   - p = 1k: PROD-H dataset `p1000_S3_r001` (c100), regenerated on NOTS and checked against the input manifest.
   - p = 2k, 5k: full fits, S3-type design at general p (same law as PROD-H S3; O(np) generator).
   - p = 20k: setup + one adaptive pilot island (H = 2,500) + one fixed-grid island (N = 2,500).
   - p = 10k full fit: admitted only after the 5k measurement.
   - Measured: stage count T (pilot, each rebuild, final), rebuild count I, time by phase and by stage, memory by phase.
2. **v3.2-dev** = `Scripts/SMC_BVS/core_v32dev/` (copy of the v3.1 core; v3.1 stays frozen). Bit-identical changes only:
   - T1: block tables by DFS with a bordered (prefix-reused) Cholesky; any unusual event falls back to the production
     scorer for that subset, so route counters stay identical;
   - B1: neighbour graph by partial selection under the same total order;
   - G: Gram by lane-parallel sums with the same summation order per entry; correlation matrix built once and shared;
   - L4: LS0 preflight charged with the method's scan bound p + k*(p − k*) (delivery only, Lemma RO).
   Local checks first (Rtools GCC 14.3, production flags): element-wise `memcmp`/`identical` against the v3.1 routines.
3. **Bit-identity on NOTS** (sapphirerapids, GCC 14.3.0, R 4.5.2, one thread): 24 PROD-H units (one per p × S × c cell,
   chosen to include escalated fits) + a small supplementary set for the exact branch, fallback score routes and ties.
   v3.1 vs v3.2-dev, fit fingerprints (every output field except timings and the preflight record); A1–A8 where the old
   v2.2.1 records are reachable.
4. **Free task**: sd(log Ẑ_r) by p from the PROD-H records and the P6 runs.
5. **DESIGN_v1.md** last, from measured numbers; slips to leg B if CW runs short.
6. Reviews: Sol (code review of the bit-identity claims and test coverage); Astra (break review of DESIGN_v1, if written).
7. `CHECKPOINT_1.md`, commit, CP1 summary.

## NOTS rules (binding)
- Hard cap 150 task-hours. Admission ledger in `LOG.md`: worst case (Σ time limits) before each submission, sacct
  actuals after. Commons/scavenge only. Job names `w3scale_*`. Small arrays with a throttle; W3-P6 keeps priority.
- `Wave3/HOLDS.md` (main checkout) read before every submission; a `HOLD SCALE` line stops submissions.
- Workspace on NOTS: `/scratch/fb31/w3scale` (home quota is at 98%).

## Reserved for Felipe (framed with numbers only, not decided)
(i) p = 1M with fixed N per island; (ii) switching the primary PIP to evidence-weighted.
