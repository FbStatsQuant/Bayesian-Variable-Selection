# BRIEF — variable-selection strategy campaign (drafted by the lead from Felipe's message of 2026-10-13)

> The protocol expects the person to write this file. Felipe gave the brief in chat; the lead transcribed it here
> and marked its own readings in ASSUMPTIONS.md. Felipe: correct anything that is wrong.

## Felipe's words (2026-10-13)
"I'm working on a SMC method that already yields an accurate estimate of the normalizing constant of the true
posterior, and reasonably good plain estimates of PIP and accurate estimates via RB as well. When it comes to variable
selection, it has been tested for several scenarios, based on median and multiple BFDR levels. Result overall seem
decent given the size of the data and other natural limitations. However, I want a very deep dive into whether there is
a variable selection strategy that is aligned with SMC in general that would yield better results than the current one,
such that the underlying SMC whether it is the same I have now or a different version still yields at least the same
level of accuracy when it comes to Z and PIP. Execute protocols, and bring me a list of 5 concrete plans, organized by
which to try first, so we start running sims today."

## Target (as read by the lead)
Find a selection strategy, native to SMC output, that beats the current one (Bernoulli(0.2) model prior, median-probability
model, BFDR at 1/5/10 %) on support recovery in S1–S6, while the SMC that feeds it stays at least as accurate for Z and
PIPs (each measured against exhaustive enumeration of its own target) as the current engine.

## Success criteria (lead's reading; see ASSUMPTIONS.md A1–A4)
- Primary: exact support recovery (count out of 100 per scenario) on a fresh-seed confirmation set, S1–S6.
  Win = better than the current best rule (median, Bernoulli(0.2)) in the pooled count, with no scenario worse by more than
  3/100, and paired McNemar evidence in at least one scenario.
- Secondary: truth included, FP, FN per dataset, model size; agreement of the SMC decision with the exact-posterior decision.
- Non-inferiority of the SMC: median |log Z error| and median RB-PIP MAE against exact enumeration of the (possibly new)
  target are no worse than the current engine's (Experiment 2 rerun / FD1) by more than 10 %; SMC decision = exact decision
  in at least 97 % of datasets per scenario.

## Previous attempts (references)
- Methodology: `Methodology/SMC_Composite_Likelihood_Methodology.tex` (7 Oct 2026).
- Z/PIP accuracy: `Experiment/Experiment_ 1/` (report), `Experiment/Experiment_2_BVS_Rerun/report/` (median and BFDR results).
- Benchmarks: `Experiment/Experiment_ 2/results/RESULTS.md` (exact MPM/HPM ceilings, PARNI, SuSiE, best subset).
- FD1 (X-aligned blocks + hybrid visited-set estimator): `Others/Further_directions/FD1_xblocks_hybrid/`.
- Selection brainstorm 5–6 Oct 2026 (about 30 prior/rule combinations, five candidates):
  `Others/2_BVS_brainstorm_20261005/FINAL_RECOMMENDATIONS.md`, `CHECKPOINT.md`, `precheck/`.
- Cycle 1 and earlier: `SMC_BVS_Manuscript.tex` (root), `Others/1_Latest_work_cycle1_and_next/cycle1_diagnosis/`.

## Constraints (Felipe's rules R1–R9, from the 5 Oct brainstorm, still in force)
SMC-based; the decision is a functional of SMC output; it must scale to large p (validated by enumeration at p <= 30);
target changes only with inference-grounded justification and a closed-form score; competitiveness, not perfection;
literature-backed.

## Familiarity
Felipe has an SMC background; this is his first BVS project (memory, 2026-10-07).
