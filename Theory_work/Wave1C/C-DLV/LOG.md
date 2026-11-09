# C-DLV — LOG (times CST, 2026-11-08/09)

- 21:20 Read Wave1C/PROTOCOL.md and Wave1/PROTOCOL.md. Read SoP 02_method (inputs/statuses, budgets, calibration,
  GUARD-W, LS0, output convention, settings rows 36-49), A_notation premises box, FR11 card, W1-GEN and W1-PXN reports.
- 21:25 Code read (production core Scripts/SMC_BVS/core): v3_fit.R, v3_calib.R, v3_preprocess.R, v3_run.R, cpp/v3_calib.h,
  v3_runtime.h, v3_core.cpp (final run, pilot, diag, V), v3_engine.h (island loop, local search), v3_score.h (scorer
  routes), v3_ledger.h (stores). Production vs study v2.2.1: v3_calib.h, v3_preprocess.R, v3_util.h byte-identical;
  others differ (production edits per core/README.md).
- Key findings for the plan: (i) every loop is capped (pilot ≤ T_e stages by the 1/T_e floor; ≤ ℓ rebuilds per tier;
  ≤ 1 escalation; local search ≤ ℓ moves; bisection 60 halvings), so total work is deterministically polynomial;
  (ii) the only random no-output path is `schedule_limit` = a tier-1 grid construction failure, in exact arithmetic via
  `too_many_intervals` (pilot points + bisection-inserted points > T_e) or `non_progress`; (iii) every pilot temperature
  is a grid target, and if ρ_V(u,b) ≥ 0.9 at every pilot step the grid IS the pilot schedule (≤ T_e intervals) —
  basis of Lemma G; (iv) v3.1 e7 `unsupported_size` (checked overflow) makes asymptotic delivery false for any fixed word
  size → premise IDEAL-W; (v) LH and LH-iid are masked (S* ≠ S₀), so the simple Ψ_n route cannot cover them.
- 21:40 Numerics helper (Sonnet, background) launched on numerics/BRIEF_numerics.md (production core on masked and
  favourable LH-type designs; statuses, N_p, N_b, Λ_V).
- 21:45 INVENTORY.md, STATEMENT.md v1, PLAN.md written. Statement lock R01 sent to Codex gpt-6.1-sol (high).
- 21:50 N1 numerics (lead): numerics/psi_enum.py (exact Ψ_n, oracle-V Λ_V and grid construction, p = 27, sizes ≤ 5).
  n = 200 smoke: F: Ψ = 69.9, Λ = 1.61, grid({1}) 4 intervals ok; M: post mode = {0} ≠ S₀ at n = 200 (too small).
  Ladder n = 400…25600 × 3 seeds running.
- 21:38 R01 (Codex lock) returned: REJECT — 1 FATAL (conditional plan ≠ ticket target), 7 MAJOR, 2 MINOR. All
  dispositioned in reviews/R01_disposition.md; STATEMENT v2 (target kept, NOT claimed; claims split P/C/F/O),
  INVENTORY v2 (F4 interrupts, F5 allocation exceptions, F6 build/deps; D1a `validation_failed` reachable after the
  snap; F2 call-graph argument), L1 R.4–R.5 (p_raw; envelopes by unit), L3 Prop 3.5 (snap). Locked v2 at ~21:58.
- N1 result (numerics/N1_psi_{F,M}.txt): Ψ_n and sup_{[0,2]} Var explode with n on both designs (start mode ≠ S₀ from
  n = 1600: masked M start mode {0}; F start mode {0,9,18} contains the linked proxy) → the Ψ route is dead; but oracle-V
  constructions need only 8–21 intervals vs T_e = 1000. Pivot: exact identity ρ = q_u(M)q_{2v−u}(M)/q_v(M)² (L3 3.1),
  two-model insertion lemma (L5), reduction theorem (L4), fallback finding (F1).
- Production-core numerics (Sonnet helper; numerics/SUMMARY_dlv.md): 80 fits, designs M/F, (n,p) from (100,27) to
  (1600,135), 8 seeds: 80/80 `completed`, SMC branch, no escalation, no trigger, all constructions ok, max N_p 13,
  max N_b 10, max intervals 17 vs T₀ = 1000; Λ_V < c₀ in only 2/233 constructions (so insertions are the norm);
  HPM = S₀ 8/8 for M at n ≥ 800, 40/40 for F; max fit 67.5 s.
- 22:05 L1–L5 drafted. Lemma checks launched: R02 (L1+L2, Codex high), R03 (L3+L5, Codex xhigh — key lemma), R04 (L4,
  Codex high). N2 falsification (numerics/n2_grid_lemmas.py, mpmath 60 digits) running. N3 (helper): save V snapshots
  from production fits, replay build_grid, test the two-model bound on the realised V.
- 22:08 L5 extended with Lemma 5.2′ (remainder needed only on [0, 1+η]); edited after R03 launch (R03 may have seen
  the earlier version; to be rechecked if R03 does not cover 5.2′).
- note: times before 22:09 are approximate (reconstructed); from now on taken from `date`.
- 22:11-22:12 R02 (L1+L2): GAP (cache-probing cost, tie-DP cost, dropped allocation term; minors). R04 (L4):
  VERIFIED-WITH-AMENDMENTS (pathwise Corollary D′; n_β ≈ 2.28·10⁸). All applied (reviews/R02_R04_disposition.md).
  METHOD_REQUIREMENTS A.2: e4 fallback = W1-N3 TDP (or within its bound).
- 22:13 CITECHECK draft: 126 citations, 8 path misses (resolver) fixed, 4 wrong lines fixed (L1 exact_count 69-81;
  L2 engine.h:396, SoP 193-194, 189-192; INVENTORY SoP 365-385).
- 22:15 N2 (numerics/N2_grid_lemmas.txt): 0 violations (identity 300 families × all M; variance bound; dominance;
  closed form 2000; Lemma 5.2 bound; worst N_b/bound 0.36). N2b (pilot cap + 5.2′ with counts) running.
- 22:17 R03 (L3+L5, xhigh): core lemmas VERIFIED / V-W-A; Corollary 5.3 ERROR (wrong bound under Lemma 5.2′; checked
  counterexample) → corrected; all amendments applied (reviews/R03_disposition.md).
- 22:18 N2b: pilot cap 300 runs 0 violations (max k/T_e = 1.000, i.e. the cap is attained by fully forced pilots);
  Lemma 5.2′ 250 families 0 violations (worst N_b/bound 0.33).
- 22:19 Mid-point review R05 launched (fresh Codex xhigh; STATEMENT + lemmas only).
- 22:25 N3 (helper): build_grid replay on saved V/pilot = code grid in 51/51 constructions (validates L3's reading).
  Two-model hypothesis of L5 FAILS on all 51 realised V (r_max ≥ 0.08 on [0,1.25]; median 0.18) at n ≤ 1600 — L5 is an
  asymptotic-regime lemma only; recorded in L5 Remark 5.4(0). Insertions observed ≤ 10 for other reasons (unexplained).
- 22:28 R05 mid-point (fresh Codex xhigh): CONTINUE; 1 MAJOR (TDP-IMPL premise), 2 MINOR — applied (reviews/R05_disposition.md).
- 22:35 Exhaustive sweep R06 launched (fresh Codex high, all files).
- 22:40 R06 sweep: 0 FATAL, 4 MAJOR, 9 MINOR, 2 EDITORIAL — all fixed (reviews/R06_disposition.md). New premise CONFIG; MACH allocation-success clause.
- 22:43 Council round 1 launched: Codex gpt-6.1-sol xhigh, Claude Opus 5.5 high (reviews/COUNCIL_BRIEF.md). CITECHECK final: 150 citations, 0 missing.
- 22:55 N4 stress (helper; numerics/N4_SUMMARY.md): 3 harder designs (3 masked pairs + visible; 2 strongly linked
  pairs; weak masked pair) × (400,81), (1600,135), (3200,189) × 6 seeds = 54 fits: 54/54 completed, no escalation, no
  trigger, no forced pilot steps, all constructions ok, max N_p 31, max N_b 16, max intervals 39 vs T₀ = 1000. (HPM ≠ S₀
  at small n / weak signal, as expected; not a delivery question.)
- 22:52 Council round 1: Codex 7.6 (G1,G2,G3,G5 FAIL: custom-h, Cert terms), Opus 8.6 (all PASS). Not passed. All findings fixed (reviews/C1_disposition.md). Round 2 next.
- 22:59 Council round 2 launched (fresh seats: Codex xhigh, Opus high).
- 23:02 Council round 2: Codex 9.0 (all PASS), Opus 8.9 (all PASS) → COUNCIL PASSED (round 2). Minors applied (reviews/C2_disposition.md).
- 23:03 REPORT.md finalised (PARTIAL; council passed round 2). CHECKPOINT updated.
