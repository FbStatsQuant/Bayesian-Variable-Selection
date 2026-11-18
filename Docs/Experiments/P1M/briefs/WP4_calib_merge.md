# WP4 — calibration (bounded and coded rules), merge, tail (final local search + LS0), statuses (Opus 5.5 builder)
Read BUILD_COMMON.md first. Branch: `exp/P1M-wp4-calib-merge`. Code against `Docs/Experiments/P1M/INTERFACES.md` (WP1)
and the island API of WP3 (coordinate through the manager; stub the island until WP3 lands).

Inputs: ENGINEERING_SPEC §0-v2.2 (#2, #6, #7, #8, #10), §1 rows 3–5, §3, §4, §6; `core/v3_calib.R`, `core/cpp/v3_calib.h`,
`core/cpp/v3_core.cpp:403-520` (final run, tail), `:690-760` (V), `core/v3_run.R` (assembly, flags, PIPs, log Z);
REVIEW_fable R1 (the seven triggers), R6; DECISIONS D-2, D-12, D-13, D-11.

Scope:
1. **Calibration, two rules.**
   - *coded* (theory mode; equals `core/v3_calib.R` + `v3_calib.h`): pilot, the rebuild loop to ℓ with bitwise grid
     convergence, all seven triggers, one escalation, the C-DLV fallback;
   - *bounded* (V-1M): pilot + at most I_max rebuilds (parameter; default 3), no escalation except construction failure,
     freeze with the flag `grid_unconverged`; plus grid refinement ×m (parameter; default 1).
   - V re-scoring and grid construction threaded, with a fixed blocked sum (class C, declared).
2. **Merge** of R′ island files: stores (top-c of the union, deduplicated by model identity), the HPM with provenance by
   event key, `island_best`, logical counters; log Ẑ (LSE − log R′), PIP_eq (primary), PIP_Z + R_eff + max W_r, PIP_𝒯,
   log Z_𝒯, Ẑ_occ (top-M sets, M ∈ {1, 10, 100, 1000}, with the terminal occupancy from the island files), MPM, flags.
   Refuse to merge a subset (GUARD-W).
3. **Tail**: final local search from the merged HPM (cap ℓ), the start mode, LS0 (cap ℓ + |S̃₀|), as in
   `core/cpp/v3_core.cpp:453-481`, with **threaded scans** and a max-reduction that keeps the tie rule.
4. Statuses and failure paths (spec §6; T10).
5. Tests: coded calibration bit-equal to `core/` on PROD-H-size fixtures (p ≤ 2k) in compat mode; merge at R′ = 4 with
   v3.1's N equal to the serial run (T9, class B except counters); T10 failure paths.
