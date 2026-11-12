# W3-MISR — CHECKPOINT 2 (proofs checked; council R1 passed), 2026-11-12 04:15 CST

Lead: Claude Fable 5.2 (Claude Work, high). Branch `theory/W3-MISR`. The run ends here (CP2), as instructed.

## Outcome
- **Council R1 PASSED** on `MANIFEST d3f5c91f0dfb8d6a201aca3ecd522261d30551068ae9bf46624abdc752554c2d`: sol 9.3, opus 8.7, six gates PASS in both;
  0 FATAL, 0 MAJOR. `manifest.py bind` OK; `manifest.py verify` OK on the final tree. Council cell:
  `R1; MANIFEST d3f5c91f0dfb8d6a201aca3ecd522261d30551068ae9bf46624abdc752554c2d; sol=9.3 PASS(reviews/R1_council_sol.md); opus=8.7 PASS(reviews/R1_council_opus.md)`
- Before it: statement lock L01 REJECT (1 MAJOR, in a side remark) → one fix round → L02 LOCK; better-theorem review
  BT1 (2 proposals adopted, 3 recommended as tickets); line checks K1, K2 (0 FATAL, 0 MAJOR, 3 MINOR, applied).

## What is proved and checked (`STATEMENT.md` v1.2, `lemmas/`, review files in `reviews/`)
1. Lemma R′: the coded posterior is exactly invariant under affine maps of the response (code path pinned and run);
   under a Gaussian contrast residual of any variance it has the law of a unit-noise well-specified model.
2. MIS-R (i): sup over a configuration class of E[1 − π_𝒞(S₀^𝒞)] ≤ C√(log n/n), constants free of the variance —
   "σ², τ² fixed" is gone; the hypotheses are the W3-POST2 interface in signal-to-noise form.
3. MIS-R (i′), (ii): no-margin clauses in expectation; random designs by conditioning, with design-measurable
   variance, slices in s, tight constants.
4. Corollaries G (Gaussian rows, any n-dependence), H (Hellinger contraction: the Song–Liang Theorem 4 analog);
   Remarks SNR (brief item (d)), P, U.
Statuses stay "PROVED (by this seat, unchecked), conditional on W3-POST2:…" in the files: HQ applies labels at CP3.

## What is left (all for HQ; estimate: one short CP3 session)
- Apply the council's wording/bookkeeping items (5 MINOR, 9 NIT; `reviews/R1_disposition.md`) and get a Sol
  "editorial only" diff check; add the `council:` line and the `correct:` gate to the REPORT registry block; staged ingest.
- Acceptance record for the W3-POST2 inputs (the registry still says "PROVED (by this seat, unchecked)").
- Decide: mid-point and sweep layers (not run; not in the brief); supersession of C-MIS:Thm-MIS; tickets BT1-A2
  (Corollary H in expectation), B1 (empty projection at growing p), B2 (out-of-sample Hellinger); whether BT1 must be
  repeated on v1.2.

Agents in this run: Sol ×6 (L01, L02, K1, K2, council; codex, high), Astra ×1 (BT1; codex, high), Opus 5.5 ×1 (council;
Claude Work, high; one failed launch on the rate limit, relaunched). No Claude Personal. HOLDS.md empty throughout.
