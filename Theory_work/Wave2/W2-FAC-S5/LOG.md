# W2-FAC-S5 — LOG

* 2026-11-09 08:41 — start; read Wave2/Wave1C/Wave1 protocols, FACB REPORT/STATEMENT/L1–L4, FACA STATEMENT.
* 08:45–09:25 — numerics: bcs_core.py (closed-form BCS scorer + LS0 path, exact increments); bcs_selftest_out.txt
  (5 cases vs FACB fac_core.scan: flips/swaps agree to ≤ 5e-7, best swap on candidate set = exhaustive in 5/5).
  S1 grid (s1_out/, 27 runs, S5, p ∈ {500,2000}, n ∈ {1e3..1e12}): pure null deletion to S0 in 27/27; add and swap
  margins ≈ −0.5 log n; max outside |τ| / d_T ≈ 1.9–2.0 (within-group cascades), Dout ≈ d_T in the bulk;
  |e_T|κ0/H ≤ 0.005 in the bulk, ≤ 0.17 overall. S2 (s2_readd_out.txt): re-add invariants exact within one CS group
  (h known) 300/300; fail for random PD matrices (57/300, 137/300) and mildly for full BCS (6/60, excess ≤ 0.27).
* 09:25–09:33 — analysis: exact reduction τ = group part + κ·e; union bound over (null, mate-set) makes within-group
  jumps irrelevant for α < 1/2; lattice bounds on e_T match the deletion level (=> FACA's 1/6); several bootstrap
  routes for path control of e_T examined (singleton-regime running-max bootstrap works only once e_T ≪ level, which
  the lattice cannot supply; per-group comparison sets are path-dependent). Decision: Tier 1 = reduction theorem
  (provable), Tier 2 = Lemma KL (P(CC_n) → 1) attempted with a parallel Codex prover. STATEMENT v1, PLAN.
* 09:35 — R01 statement lock (Codex Sol high) launched; KL parallel prover (Codex Sol xhigh) launched with
  reviews/KL_BRIEF.md.
* 09:36 — l1_identities.py: identities of L1.3 exact to 1.5e-14 in 400 random BCS instances (l1_identities_out.txt).
  S3 (s3_cc.py, s3b_out/, S3_summary.txt): κ0|e|/H_q ≤ 0.23 overall, attained at m = 2–5 (end phase), ≤ 0.05 for m ≥ 30;
  finding: near the end κ0|e| ≈ H/(s0 + 1 + κ∞) does not vanish, so "κ0|e| ≤ cH for every c" is false → CC redefined
  size-dependently as CC_n(δ): (H_q + κ0|e|)² ≤ (1 − δ)(log n + 2 log((2p − k)/(k + 1))) (KL_BRIEF §6 update; prover
  steered). Note: at the simulated n the CC_n(δ) inequality itself is violated at the START of the path (union-bound
  constants: H_q² includes 2^q and 2 log log n) — it is an asymptotic condition; the e-part is what the numerics track.
* 09:40 — S4 (s4_start.py, S4_out.txt): start mode = S* in 36/36 (two BCS designs, N0 = ∅ and ≠ ∅, n ≤ 1e8).
* 09:41 — HQ note: W2-SIM available; SIM_REQUEST.md written and sent (bulk/end scaling of e_T with p up to 2e5).
* 09:36–09:43 — Deviation (logged, as FACB): lemma drafts L1–L5 written while R01 runs; none sent for checks before the
  lock verdict.
* 09:50 — R01 (Sol high): LOCK-WITH-CHANGES (5 items) — all accepted (reviews/R01_disposition.md); S1-EXH complete-scan
  certification 15/15 (S1X_summary.txt). **STATEMENT v2 LOCKED.** HQ framing note (design-agnostic main theorem W2-UNI):
  will list general-assumption ingredients in REPORT; current target unchanged.
* 09:55 — lemma checks launched: R02 (L1–L3, Sol high), R03 (key lemma L4, Sol xhigh), R04 (L5, Sol high).
* 10:05 — R02 (Sol high): L1 FAILED as written (leakage rate √k/n^{3/2} missing; counterexample), L2/L3 V-W-A; all 4 items applied (reviews/R02_disposition.md); l1_leak.py added.
* 10:10 — R04 (Sol high) L5 V-W-A (CC_n measurable only on the enlarged space; provenance) — applied (reviews/R04_disposition.md).
* 10:15 — KL prover round 1 (Codex Sol xhigh): PARTIAL (lemmas/KL_attempt_sol/README.md): CC proved for full S5 on the
  final ≤ 2-null region (≤ 4 with truths in distinct groups); whole-path CC under a restricted partition (null groups are
  singletons); protected-champion lemma (field-shifted group maximum never the exact greedy deletion while its group has
  ≥ 2 members); explicit dense-size lattice bound. Middle range for genuine 5-null groups open. Not yet cross-checked
  (unchecked prover output; not used by Tier 1). Round 2 launched (Codex Sol max) with the lead's bootstrap/exceptions
  ideas and the champion lemma as the start device.
* 10:25 — R03 (Sol xhigh) key lemma L4: V-W-A, 3 minor items, applied (reviews/R03_disposition.md); STATEMENT v2.1 (wording only, flagged).
* 10:30 — CHECKPOINT.md written (Tier-1 key lemma checked). R05 mid-point (fresh Sol xhigh, statement + proofs only) launched.
* 10:40 — R05 mid-point (fresh Sol xhigh): CONTINUE, 2 minor, applied (STATEMENT v2.2 wording; L4.6 remark 2).
* 10:42 — R06 exhaustive sweep (Sol xhigh) launched.
* ~10:35 — R06 sweep: 0/1/11/7, all fixed (reviews/R06_disposition.md); numerics regenerated (l1_identities, l1_leak, s1_exh2 with tie rule: 15/15, 0 ties); STATEMENT v2.3 (wording).
* ~10:40 — REPORT.md drafted; CITECHECK rerun; council round 1 launched (R07 Codex Sol xhigh, R08 Claude Opus 5.5 high, Claude Personal).
* ~10:42 — KL prover round 2 (Codex Sol max): PARTIAL (lemmas/KL_attempt_sol2/README.md): CC_n(1e−4) at log p/log n ≤ .17 for all parents with k ≥ p^.06 or ≤ 250 retained nulls; singleton no-crossing and cohort interval modules; non-singleton-deletion fraction ≤ exp[−3(xH)²/44] under field bound; conditional terminal theorem (field ≤ .05H until first champion deletion ⇒ CC afterwards for α < .4126). Gap: 251 nulls … k < p^.06. Unchecked; reported as frontier in REPORT §5.
* ~10:50 — council R07 (Sol xhigh): 7.8, G1/G2 FAIL (report scope: N0 exception, s0=4 and exact-argmin qualifiers of frontier), G3–G6 PASS; REPORT fixes applied; waiting R08.
* ~10:55 — council R08 (Opus high): 8.6, all gates PASS; round 1 not passed (R07 7.8). All fixes of both seats applied (reviews/R07_R08_disposition.md). Council round 2 launched with fresh seats.
* ~11:00 — council R09 (Sol xhigh, round 2): 8.8, all gates PASS, no required fixes (one nonblocking numerical erratum).
* 11:05 — council R10 (Opus high, round 2): 8.8, all gates PASS, no required fixes. **Council round 2 PASSED** (R09 8.8, R10 8.8). Tier 1 PROVED-CHECKED; RESULT = PARTIAL (KL open). Optional items applied (reviews/R09_R10_disposition.md); CITECHECK rerun. REPORT final.
  (Timestamps after 10:30 were initially mis-stated and corrected to approximate values; clock read 11:05 CST at the end.)
