# S5 R01 (design, E-S5CC) — disposition (family lead, 2026-11-09 ~11:10)

Verdict NO-GO; all 8 items ACCEPTED and fixed before any large batch (none had been submitted).

1. BLOCKER (phase chain) — ACCEPTED. Real bug introduced when the bulk-proper fields were added: `elif m >= 5` attached to
   `if m in MCHK`. s5cc.py rewritten with one `bulk / mid / end` chain; checkpoints recorded independently. New
   independent per-state checker `S5/validation/check_s5cc_states.py` (own loop, per-state arrays, numpy masks) agrees on
   every added field in 5/5 cases incl. a case with no bulk phase (`val_states_check.txt`). Original 12 fields still
   identical to s3_cc.py 6/6 (`val_compare.txt`).
2. MAJOR (unvisited phases) — ACCEPTED. Phase statistics initialised to null; `visited_states` per phase; `fail_reason`,
   `m_final`; summariser uses only runs that visited a phase (N shown), slopes use complete paths only, incomplete runs listed.
3. MAJOR (CC delta) — ACCEPTED. Added delta(T) = 1 − (H_q + κ₀ max|e|)²/Λ_k, min over the path (all/bulk/end, argmin m), the
   deterministic e = 0 baseline, pass rates for δ ∈ {0, 0.1, 0.25}; summary text states that cells with negative baseline
   cannot diagnose e and that finite-grid failures do not bear on asymptotic KL. Original field kept unchanged.
4. MAJOR (reached_S0 ≠ LS0 certification) — ACCEPTED. Renamed in all new text to `deletion_path_complete` (original field
   kept); best addition recorded every step (max (add − del)/log n by phase, # steps add ≥ del, # add > 0); candidate swap
   value (bcs_core Path._swaps) at checkpoints (every ⌈p/400⌉-th step and every step with m ≤ 100) — recorded, never acted
   on; terminal state at S0 (best truth deletion / addition / swap, improvable flag). Interpretation for C2-R limited
   accordingly; complete-scan certification remains the ticket's S1-EXH (p ≤ 500) and E-S5P(i).
5. MAJOR (integrity) — ACCEPTED. Summariser validates rows against the task tables (unknown/duplicate keys, rng_seed),
   lists missing tasks, aborts (exit 2) before inference on problems (tested: duplicate row → abort).
6. MINOR (pairing) — ACCEPTED. `del_sequence_sha1` digest + comparison of all unrounded e-statistics; differing fields and
   unpaired seeds reported. end_trace no longer rounded.
7. MINOR (imbalance definitions, power) — ACCEPTED. Prespecified E1 (primary: any |I| ≥ 2 at m ≤ 5 — one excursion
   suffices because the KL-attempt end-phase argument makes |I| ≤ 1 absorbing), E2 re-entry, E3 (≥ 2 of m ∈ {5..1}),
   Wilson intervals; REPORT will state the rates that can be excluded (0/50 → upper 7.1%, 0/20 → 16.1%).
8. MINOR (singleton slopes) — ACCEPTED. Bootstrap CI only if every contributing cell has ≥ 2 complete runs, else "descriptive".
