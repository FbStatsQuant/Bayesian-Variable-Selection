# From the p ≫ n rerun to the theory phase: extraction strategy (HQ, 2026-10-30)

Felipe's condition (D23a): "Re-run is approved, as long as we have a clear strategy to extract insight from that data into the theory building phase." This page is that strategy.

**Targets:** the frozen paper list in `Theory_architecture_v3/PAPER_SELECTION_20261028/FROZEN_LIST.md`.

**What the rerun adds over the existing 2,400 fits.** The core and seeds are identical, so Ẑ, the HPM and the RB PIPs are reproduced. The rerun adds:
1. plain PIPs and the plain MPM;
2. the scored-model registry summary (distinct models, scored mass `log_sum_exp_F`, and the phase × mechanism matrix of first scores);
3. stop-phase and stop-timing records;
4. a P5 same-seed retry at double allocation for every `resource_limit` fit.

**Limit, stated up front.** The per-model scored set, which traces when the truth was first scored, is exported only at p ≤ 32. At p ≫ n "was the truth scored?" is known only through the score comparison below. The full trace comes from the low-p study, which reports the same fields with an exact reference.

## Mapping: question → quantity → source

| Theory question | Quantity | Source (rerun = R; post hoc on fits or data = P; low p = L) |
|---|---|---|
| **T37** (Thm 3): does the production local search repair a near-truth centre to the truth, in finite n? Literal or "toward S₀" wording? | TD(d = 0) audit, both variants: margins, ties, truth-in-swap diagnosis; share of first scores credited to local-search mechanisms | P: `run_theory_H.R`, about 300 core-h, d = 0 (D18). R: `scored$first_scored`. L: `truth_first_mech` and `truth_first_phase` |
| **T22 + T27** (Thm 2): start mass in the favourable and masked regimes | π₀(S₀), π₀(R₀), π₀(R₁), π₀(R₂) per case; regime class by scenario | P: `theory_measures.R` (exact DP over blocks). Needs only the data, so it can run before the rerun lands |
| **T38** (Thm 5): HPM consistency in both regimes, including delivery, plus the polynomial-cost corollary | Recovery by regime and by π₀ class; cost against p (500 vs 1000): runtime, escalation tier, number of distinct models scored | R: registry size, timings, tiers. P: π₀ classes. Existing recovery tables |
| **T21** (Thm 4): P(wrong) ≤ P(no output) + 2E[mass off the truth] + P(truth never scored) | Per miss: `no_output` (primary `resource_limit`, then its P5 status), `search_miss` (F(S₀) > F(HPM), so the truth was never scored), `posterior_miss` (F(S₀) ≤ F(HPM), with HPM ≠ S₀). Scored-mass share exp(log_mass_scored − log Ẑ) as a proxy for mass captured | R: stop records, P5, registry mass. P: F(S₀) from the scorer (truth used only at scoring) |
| **Resource-stop vs complete-run gap** (the theorems assume a completed run) | Share of fits that completed every phase; stop phase; for each `resource_limit` fit, primary vs P5 outcome (does completion change the HPM or recovery?) | R: stop phase, P5 pairs |
| **T03 / T07** (Thm 1, Prop 1): concentration; same-size swaps | Among `posterior_miss` cases: is the HPM a superset of S₀, or a same-size swap? Size and composition of the gap F(HPM) − F(S₀) | P, on the rerun or the existing fits |
| **T26(i)–(ii), T12** (Thm 6, Prop 2): evidence and PIP consistency, Ẑ unbiasedness | p ≫ n: RB vs plain PIP agreement and MPM-RB vs MPM-plain selection; spread of Ẑ across islands. Exactness is tested only at low p (D22) | R: plain PIPs, per-island stage records. L: errors against the exact posterior |

## How the evidence is extracted
1. **Before the rerun lands:** run the post-hoc measures (π₀, TD d = 0, F(S₀) − F(HPM), miss class) on the existing fits and data with `code/scoring/run_theory_H.R`, under the D22 scope. Truth is read only by scoring.
2. **After the rerun:**
   - pull and verify the outputs;
   - extract the R fields through `code/scoring` (FIELD_MAP, `case_theory.csv`, `case_smc_accuracy.csv`);
   - confirm that the reproduced Ẑ, HPM and RB PIPs equal the existing fits; any mismatch is a defect;
   - join everything per case.
3. **Output:** `analysis/EVIDENCE_H.md`, one section per row above. Each section gives the measured quantities, a support / contradict / silent verdict for the conjectured statement, and the cases that break it. It is read together with the low-p `EVIDENCE_L.md`. Both feed Phase 4 ("let the data talk") and Fable's statement refinement (Phase 6).
4. **Review:** an independent tie-out of the evidence tables, then a Sol review, as for every deliverable (charter §4).
