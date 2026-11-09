# W2-FAC-X — LOG

* 2026-11-09 08:31 — Ticket start. Read PROTOCOL (Wave2, Wave1C, Wave1), FACB REPORT/STATEMENT/L1–L5, FACA L5.
* 08:45 — numerics/iid_core.py: exact iid-row sufficient statistics via Bartlett (any n) + incremental exact LS0 path.
  Self-test numerics/iid_selftest_out.txt: incremental gains = direct closed-form scan (fac_core.scan) to ≤ 4.4e-8 at
  n ≤ 1e7; Bartlett law check vs explicit rows OK.
* 08:50 — Analytic mechanism (X1): noise coordinates ξ iid and exactly independent of the idiosyncratic Wishart W;
  iid-row score = FACB 1-D scan + path-dependent perturbation (first order (Rc)_j). Band self-consistency ⇒ A < 1/2.
* 08:55 — N1X restarted with p ≤ 1000 (p = 2000 too slow: ~5 min/job). Quick check (n = 1e5, ρ = .5, s0 = 4):
  p = 200, 400 pure deletion to S0; hull defect 13 / 46 (hole is NOT an exact interval: band present); δ̂ ≈ 0.13–0.20.
* 08:57 — STATEMENT v1 (Target 1) + PLAN drafted; statement lock R01 requested (Codex gpt-6.1-sol high).
* 09:05 — R01 statement lock (Sol high): REJECT, 6 required changes (X3 counterexample to PLAN's informal soft gap;
  no family-wide no-addition; normalisation/absolute errors; random N0; s0 ≥ 1 and (FS′); frontier algebra).
  Disposition reviews/R01_disposition.md. Lemma drafts X1–X4 written; X3 now carries an explicit density hypothesis.
  N1X complete: 121/121 pure deletions to S0 (numerics/N1X_summary.md). N3X: 0 violations (numerics/N3X_out.txt).
  Perturbation scale renamed ϖ.
* 09:21 — STATEMENT v2 + PLAN v2; fresh lock review R02 (Sol high) requested.
* 09:22 — HQ scope update: target item 3 (k ≥ 2) moved to ticket W2-FAC-K2. W2-FAC-X = items 1 (iid CS, largest
  exponent) and 2 (general one-factor loadings, exact Gram then iid). STATEMENT §0/§6 and PLAN updated.
* 09:24 — N2X (Target 2 diagnosis, numerics/N2X_summary.md): 64/64 heterogeneous-loading paths (exact reference and iid)
  pure deletions to S0; exact-reference path = argmin of the variable-centre statistic |ξ_j − ℓ_jX_T|/norm_j; a common
  centre does not describe it. Parallel prover (Opus subagent, Claude Personal) launched on the finite-class exact-Gram
  case, writing to T2/.
* 09:27 — X5 (start mode, conditional on X) and X6 (assembly, delivery) drafted. N5X: start = [p] ∖ N0 in 48/48
  iid-row data sets (numerics/N5X_out.txt).
* 09:30 — R02 (fresh Sol high): LOCK-WITH-CHANGES (5 items). All applied (reviews/R02_disposition.md): X3 prefix form +
  general crossing bound; X2 event constants for bounded p (|η|, truths ≤ √(2L_n) ≤ H̄); (C2) bindings S*(N), m₀(N);
  X4.1 slack, E-add factor 2ϖ, end-phase structure re-proved; frontier wording. **STATEMENT v3 LOCKED.**
  N3X extended to the prefix conclusions of (vii): 480 runs, 151 under the hypothesis, 0 violations.
* 09:34 — Lemma checks launched in parallel: R03 (X1–X3, Sol high), R04 (X4 key lemma, Sol xhigh), R05 (X5–X6, Sol high).
* 09:50 — R05 (X5–X6, Sol high): VERIFIED-WITH-AMENDMENTS ×2, no FATAL; MAJOR: condition on the raw design Z = X^r
  (θ* = D_xβ is not standardised-X-measurable); two-sided zero-pair event. All applied (reviews/R05_disposition.md);
  STATEMENT v3 wording "conditionally on X" → "on the raw design X^r" (no claim changed).
* 09:40 — R03 (X1–X3, Sol high): X1, X2 VERIFIED-WITH-AMENDMENTS (minor); X3 FAILED as written (MAJOR: crossing bound
  stated on the wrong side, false strict inequality — explicit counterexamples). Repaired as R03 proposed
  (d_i < 2ϖ/(|K_i| − 2 + κ′), ω_i ≤ 2d_i + 2ϖ; consequences unchanged). Disposition reviews/R03_disposition.md.
* 09:42 — R04 (X4 key lemma, Sol xhigh): VERIFIED-WITH-AMENDMENTS, no FATAL/MAJOR; 7 MINOR applied
  (reviews/R04_disposition.md). R03b (X3 re-check) running. HQ note: W2-SIM (NOTS) available for large simulations.
* 09:44 — CHECKPOINT.md written. SIM request sent to W2-SIM (numerics/SIM_REQUEST.md). X7 (Target 2: near-equal loadings,
  max|λ_j − λ̄| ≤ n^{−c}, exact Gram and iid rows) drafted as a corollary of X1–X6.
* 09:45 — HQ framing update (binding): design-agnostic main theorem under (A1) iid rows + sparse eigenvalue floor,
  (A2) approximate k-factor structure with local Ψ, (A3) beta-min + non-masking (ticket W2-UNI). Action: finish Target 1;
  REPORT.md will list exactly which general ingredients the proof uses and where compound-symmetric structure enters.
* 09:47 — R03b (fresh re-check of repaired X3): VERIFIED-WITH-AMENDMENTS, no FATAL/MAJOR, 3 MINOR applied. All lemma
  checks of Target 1 complete. Independent mid-point R06 (fresh Sol xhigh, statement + proof files only) launched.
* 09:55 — Mid-point R06 (fresh Sol xhigh): **CONTINUE**, no MAJOR+; 3 MINOR applied (reviews/R06_disposition.md).
  Next: exhaustive sweep (Sol xhigh).
* 10:05 — Sweep R07 (Sol xhigh): 0 FATAL / 0 MAJOR / 3 MINOR / 9 EDITORIAL; all fixed (reviews/R07_disposition.md).
  Next: citation check, REPORT draft, council (Sol xhigh + Opus high).
* 10:11 — REPORT.md drafted (Target 1 complete through sweep; Target 2 status; §6 general-assumption ingredients for
  W2-UNI). CITECHECK: 5/5 line citations, 8/8 quoted statuses. Council round 1 launched: R08 Sol xhigh, R09 Opus high
  (brief reviews/COUNCIL_BRIEF.md).
* 10:16 — T2 parallel prover returned PARTIAL: Lemma L4r-S (exact Gram, arbitrary loadings in [λ_lo, λ_hi], uniform over
  all T, p ≤ n^{A₁}, A₁ < A_S(loadings) = 1/6 at CS), per-class gap invariant, exact obstructions beyond A_S
  (T2/NOTES.md), 366/366 exact paths fine. Packaged Target 2 as Theorem FAC-GL (STATEMENT_T2.md v1: (G) exact Gram and
  (R) iid rows, population non-masking (FS-G)) + Corollary FAC-NCS (X7); new lemmas X8 (start mode, general Σ), X9
  (iid uniform transfer, |δ| ≤ C(p/√n)H̄), X10 (assembly). Statement lock R10 (Sol high) requested.
* 10:24 — R10 (T2 statement lock, Sol high): LOCK-WITH-CHANGES (4 items). Applied (reviews/R10_disposition.md);
  FAC-NCS narrowed to Δ_nH̄_n ≤ n^{−1/3}. **STATEMENT_T2 v2 LOCKED.** Next: T2 lemma checks.
* 10:28 — Council R08 (Sol xhigh): 8.8, G1 FAIL only on a REPORT §6 overstatement (log-size eigenvalue floors do not
  suffice for truth moves — explicit non-CS counterexample); G2–G6 PASS; no blocking gap in (C1)–(C4). REPORT §6 fixed
  (items 1–3). Waiting for R09 (Opus) before round 2.
* 10:31 — Council R09 (Opus high): 9.0, all six gates PASS, nothing required. Round 1 NOT passed (R08 G1). All
  recommendations of both seats applied (reviews/R08_R09_disposition.md). Council round 2 launched (fresh seats).
* 10:33 — R12 (X7/X8/X10): X8, X10 VERIFIED; X7 (R) V-W-A, (G) FAILED as written (iid multiplier bound false for exact
  Gram). FAC-NCS narrowed to iid rows (STATEMENT_T2 v2.1, flagged); MINOR applied (reviews/R12_disposition.md).
* 10:36 — R11 (L4r-S + X9, Sol xhigh): L4r.0–L4r.3 VERIFIED; X9 V-W-A (3 MINOR applied); no FATAL/MAJOR. Target-2 lemma
  checks complete. Next: T2 mid-point (fresh Sol xhigh).
* 10:41 — T2 mid-point R15 (fresh Sol xhigh): CONTINUE, 3 MINOR applied. T2 sweep R16 launched.
* 10:51 — Council round 2 R13 (Sol xhigh): 9.2, all gates PASS, nothing required (optional table fix applied).
  T2 sweep R16: 0/0/1/4, all fixed (reviews/R16_disposition.md). Waiting for R14 (Opus) to close Target-1 council;
  then T2 council.
* 10:52 — T2 council launched (R17 Sol xhigh, R18 Opus high; reviews/COUNCIL_BRIEF_T2.md). W2-SIM results/X/Q2_visibility.md:
  population non-masking constant c₀ is small but n-free for CS (ρ ≠ ½ with the study coefficients) and two-class
  loadings, and → 0 generically for continuous loadings (sign change of a truth's partial covariance over conditioning
  sets) — so (FS-G) is restrictive for continuous loadings; to be flagged in REPORT §5 with the fix route (G2 holds from
  any start ⊇ S₀; only sure screening of the start mode is needed).
