# C-GROW — LOG (CST)

* 2026-11-08 21:20 Read Wave1C/Wave1 protocols, GEN REPORT/STATEMENT/lemmas, GEN numerics SUMMARY, T37R Theorem C.
* 21:25 orchestrator_capabilities; numerics helper (Claude Sonnet 5.5, high) launched on D1–D4 (brief: posterior,
  production cap, larger caps, full method), output numerics/SUMMARY_DIAG.md.
* 21:36 D1–D3 (p = 100) available: S2 = proof gap (start ⊇ S₀ from n = 800, ≤ 7 extras, pure deletions, production
  cap suffices); S5 = method gap (extras grow 16 → 37, production cap fails at n ≥ 3200, cap ℓ_n + |S̃₀| succeeds
  80/80). Posterior concentrates in both.
* 21:40 Route chosen: lattice backward elimination (T37R Lemma 2(b) generalised to growing lattices) + centre sandwich
  by exchange on the block product + NA via (G4-χ) or (G4-dir); method requirement MR1 (LS0 cap ℓ_n + |S̃₀|).
  Rejected: (i) GEN-style 2^{v̄} move count (cap 2^{|𝒫|}); (ii) T22(iii) exact centre law for S2 (the AR(1)
  proxy at distance ≈ log n/(2 log(1/ρ)) is always borderline between NL and VIS thresholds for large n, so the
  start mode is not a.s. a deterministic set — a sandwich is needed).
* 21:45 STATEMENT.md v1, PLAN.md written; statement lock requested.
* 21:46–21:53 Drafted lemmas L0–L5 while R01 ran (drafts, adjusted after the lock).
* 21:53 R01 (Sol): LOCK-WITH-CHANGES, 9 required changes (feasibility boundary in G1 — C5(b) as written violated it;
  global size ladder; exact BB ratio; explicit AR(1) radius; S5 layout/TV check; scope language; self-contained
  hypotheses; C4(b) reference; L0 rank factor). All applied → STATEMENT v2 LOCKED (reviews/R01_disposition.md).
  L5 radius changed to d_n = ⌈log n/(2 log(1/|ρ|))⌉. METHOD_REQUIREMENTS.md (MR1) written.
* 21:53 D4 (production core without LS0, R 4.4.1): first fits at n = 200 score S₀ (1/1 S2, 1/1 S5); more running.
* 21:58 Lemma checks launched in parallel (all Codex gpt-6.1-sol): R02 L3 (key lemma, xhigh), R03 L0–L2 (high),
  R04 L4–L5 (high). Falsification numerics F1–F3 (Sonnet helper) running.
* 21:59 D2/D3 at p = 400 (iid): S2 unchanged in kind (≤ 5 extras, production cap scores S₀ 65/65); S5: extras grow to
  70–75 at n = 3200 (p = 400), production cap fails (0/7), cap ℓ_n + |S̃₀| succeeds 7/7 and uncapped 7/7 — so for
  S5 with growing p the method with MR1 still works at these sizes (no trap seen; frontier is a proof gap).
* 21:59 Parallel prover P1 (Codex gpt-6.1-sol high, 2 h budget) launched on the random-design (iid rows) AR(1)
  extension → lemmas/L6_random_AR1.md.
* 22:04 R03 (Sol): L0 VERIFIED, L1 VERIFIED, L2 VERIFIED-WITH-AMENDMENTS (family 𝔉* incl. ∅ and pure truth deletions; wording) — applied (reviews/R03_disposition.md).
* 22:09 R02 (Sol xhigh) on key lemma L3: VERIFIED, no amendments (remark on Q = [p] near-saturated modes added).
* 22:12 R04 (Sol): L4 V-W-A (1), L5 V-W-A (2–7) — all applied (reviews/R04_disposition.md); STATEMENT v2.1 (piecewise
  AR(1) relevance set; logged as a post-lock change that narrows nothing). τ₀ for S5 = 4/25 (c = 1), 1/25 (c = 0.5),
  exact (numerics/F2_exact_tau0.txt). F3 (exact-Gram AR(1), n = 400, p = 399): start mode = S₀ in 20/20, sandwich
  20/20, population TV margin 39.96 log n-units, NEG 1.3e-5 ≪ η = 0.051 (numerics/F3_summary.md).
* 22:13 lemmas/00_MAIN.md written; mid-point review R05 (fresh Sol xhigh; STATEMENT + lemmas only) launched.
* 22:15 P1 (parallel Sol prover) returned lemmas/L6_random_AR1.md: candidate complete proof for iid-row AR(1)
  (p ≤ n^A incl. p ≫ n; selection-uniform reduction of block conditioning sets to a polylog reference family;
  conditional-sphere tail for the RSS-normalised add statistic; NA via exact population innovations; study S2 layouts
  satisfy separation). Status "PROVED (by this seat, unchecked)". Checks launched: R06 (Claude Opus high —
  cross-family to the Sol author) and R07 (fresh Sol xhigh); falsification numerics G1 (Sonnet helper, iid AR(1),
  p up to 4000). If both checks pass, (C5)(c) will be added to STATEMENT (logged as an extension, flagged).
* 22:19 F1–F3 (+F1X) falsification numerics done (numerics/SUMMARY_FALSIF.md). Not contradicted (all
  claims asymptotic), but informative: (i) NA over the FULL lattice [S₀, Q] fails at practical n when |𝒫| = 80–312
  (AR(1) d_n-radius sets, S5 all nulls): worst adds at near-full T (|T| ≈ 80–98), which LS0 paths never visit (176/180
  F1 paths are pure deletions from S̃₀ with ≤ 9 extras); the sufficient NA conditions have onsets far beyond practical
  n (G4-dir needs log n ≳ 6 log|Q|). In the (G4-χ) regime (|𝒫| = ⌊0.9 log n⌋, full lattice enumerated) NA holds in
  0/40 failures at n = 800 and 3200 (4/40 at n = 200). (ii) Sandwich S₀ ⊆ S̃₀ ⊆ Q: 180/180 (F1), 59/60 (F2; the miss
  at n = 800). (iii) TL holds on every tested T. (iv) MR1 cap: F2 40/40 vs production 0/40 at n ≥ 3200.
  Disposition: report honestly as finite-n evidence; a sharper statement (NA only on {T : |T ∖ S₀| ≤ |S̃₀ ∖ S₀|}) is
  noted as a refinement (it is what L1 actually uses along the path) but not adopted now.
* 22:21 R05 mid-point (Sol xhigh): CONTINUE (no fatal/major; 4 minor wording/certificate items applied; STATEMENT v2.2).
* 22:35 R07 (fresh Sol xhigh) on L6: VERIFIED (all of L6.2–L6.8, Theorem L6.1), no amendments.
* 22:35 G1 numerics (iid AR(1), p up to 2000; partial: p = 4000 row not run, 3 seeds at n = 800):
  finite-n violations of the L6 asymptotic events at n ≤ 800 — S₀ ⊄ S̃₀ in 6/20 runs at n = 200 (weak truth θ = −1),
  one far null (distance 44 > d_n = 5) in S̃₀ at n = 800 (ρ = 0.5, seed 1), NA failures for far nulls (max gain
  +4.3), far-null h above 2 log p + ½ log n in ~1/10 runs. Consistent with the asymptotic statements (L6.4's
  polylog reference count (log n)^15 makes the onset astronomically late); recorded as finite-n evidence that the
  theorem is asymptotic only. Path claim (c) held whenever S₀ ⊆ S̃₀; S₀ scored in every run (production cap never bound).
* 22:42 R06 (Opus high, cross-family to L6's Sol author): VERIFIED-WITH-AMENDMENTS A1–A9 (presentation/records
  only, no gap) — applied (reviews/R06_R07_disposition.md). L6 adopted: STATEMENT v2.3 adds (C5)(c) random-design
  AR(1) (study S2) as an **extension** beyond the locked v2 target scope (flag in REPORT). 00_MAIN updated.
* 22:42 Exhaustive sweep R08 (Sol xhigh) launched on all files.
* 22:43 D4 (production core without LS0, R): S₀ = reported HPM in all regular fits (S2 n ≤ 3200, S5 n ≤ 3200; incl. S5 n = 3200 where LS0 with the production cap fails); first scored in the pilot. CHECKPOINT.md written (early).
* 22:43 Citation check: reviews/citecheck.py → reviews/CITECHECK.txt, 14 path:line citations, 0 misses (snippets inspected).
* 22:47 Diagnosis helper final (numerics/SUMMARY_DIAG.md): S5 extras grow ≈ 0.03–0.04√n per null block
  (≈ 1.0–1.2√n total at p = 400); cap ℓ_n + |S̃₀| scores S₀ in 100% of cells, 2ℓ_n not enough; uncapped LS0 reaches
  S₀ in 508/517 runs (the 9 others: S₀ beaten by S₀+null at finite n); D4: production core (no LS0) reports S₀ in all
  25 fits on seeds 0–4 (S2/S5, n ≤ 3200), S₀ found by the SMC itself. Side finding for HQ: W1-GEN numerics templates
  (e.g. Theory_work/Wave1/W1-GEN/numerics/e5_outside.py) contain literal "\S0" text in place of digits at git HEAD and
  do not run (seen also by the lead at 21:30).
* 22:54 R08 sweep (Sol xhigh): 0 fatal, 0 major, 9 minor, 7 editorial — all fixed (reviews/R08_disposition.md); STATEMENT v2.4 (no claim changed); f2 script now prints its partition.
* 22:54 Council round 1 launched: R09 (Codex Sol high), R10 (Claude Opus high); brief reviews/COUNCIL_BRIEF.md.
* 23:05 Council round 1: R09 Sol 9.2, R10 Opus 9.0, all gates PASS in both → PASSED. R10 F1 (fixed-p
  enumeration caveat) applied → STATEMENT v2.5; optional S1/S3/S5 recorded; citation check re-run (18 ok, 0 miss).
  REPORT.md finalised: PROVED-CHECKED (with MR1 and named premises); frontier = S5/factor designs with growing p,
  random-design S5, finite-n onsets.
