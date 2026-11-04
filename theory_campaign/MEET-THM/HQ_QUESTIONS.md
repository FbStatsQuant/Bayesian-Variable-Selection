# MEET-THM · Questions for HQ

Chair, 2026-11-04 ~03:00 UTC. Raised in Round 1 (`R1_*.md` §I; side-by-side `evidence/R1_SIDE_BY_SIDE.md` T6). Only decisions outside the meeting's authority are listed here (binding-goal readings and anything that touches the method). The meeting continues on everything else and, where a question is pending, on both readings.

## Q1. Proposal §5.3: what does "weight stability under weak cross-block dependence" require? (binding goal)

- **Facts.** The literal one-shot form ("the variance of importance weights from the block-product start π₀ to π stays bounded when cross-block dependence is weak") is refuted for the shipped method, *independently of correlation*: OWS-WS6(d) (χ²(π‖π₀) → ∞ already under exact block orthogonality with a growing number of nulls) and OWS-WS7 (ESS → 0 under masking). Both are PROVED by their author with no independent check yet; check wave 1 is looking at them.
- **What the seats propose to ship:** a *bridge-form* theorem, meaning per-stage χ² and weights, stage count and constants continuous in the cross-block correlation ε around the block-orthogonal baseline, on a genuinely correlated design family. The four statements differ: A:605–625, B:499–517, C:347–362, D:504–524.
- **Positions.**
  - A, B and D: the bridge form is the goal's meaning (A:721, D:601).
  - C: it does not waive the goal, and if both its main route and its fallback fail, the unmet goal escalates (C:467).
- **Decision needed.** Does HQ accept the bridge form, together with a stated (and checked) refutation of the one-shot form, as meeting §5.3? Or does the one-shot form go to Felipe as a binding-goal escalation?

## Q2. Proposal §5.4: what does "credible-interval coverage error" mean? (binding goal)

- **The seats' readings, all four agreeing on the frequentist point:**
  - **A:** the Monte Carlo error of posterior credible intervals for declared functionals (A:722).
  - **B:** output-event coverage of the certificates; intervals for continuous functionals are outside paper 1 (B:689).
  - **C:** the posterior-content error of output-selected model-space sets (C:465).
  - **D:** interval error bounded by the model-space TV via its F1 bound, conditional on N1 (D:541).
  - **All four:** frequentist coverage of the exact posterior's intervals is a new target-theory question, with no route and outside objectives (1)–(3).
- **Decision needed.** Is "the Monte Carlo / posterior-content error of the reported credible quantities" an acceptable meaning? Or is frequentist coverage required? If it is required, the meeting records it as an unmet binding goal and escalates; it does not drop it.

## Q3. Proposal §5.4: TV/KL of the final pooled estimate in the masked regime (binding goal, or a listed obligation?)

- **What ships:**
  - TV and KL of the start π₀;
  - the exact reported-posterior TV = 1 − Z_𝒯/Z (deterministic);
  - the Lemma KL lower bound and the exp(KL) cost;
  - terminal-law TV ≤ q^L (C:379);
  - TV of the delivered population in the favourable regime.
- **What is not provable now:** a TV/KL error bound for the final pooled estimate under masking. It needs V11 or N10, both OPEN (D:602, A:645–646).
- **A definitional obstruction:** reverse KL of the unsmoothed sparse empirical measure is infinite whenever support is missed (C:466).
- **Decision needed.** Does HQ treat "final-estimate TV/KL under masking" as binding? If so, it is an escalation. The alternative is to carry it as a theorem obligation with a fallback (the shipped items above), with the reverse-KL obstruction stated as a definitional fact.

## Q4. Run-card additions (reporting only)

- **Proposal** (B:691, from Seat D's Round 0): report on the run card the Jeffreys estimate Ĵ and a cross-block leakage proxy (the maximum cross-block |r| after blocking).
  - The method's law and its draws do not change.
  - Two theorems (the §5.3 card and the stage laws) would then be statements about reported numbers.
- **Decision needed.** Does HQ count these as reporting additions the meeting may assume, or as method changes, which are outside the meeting's authority?

## Decided by the chair (procedure, no HQ action needed)

- **N9 independent review** (D:603). N9-KERNEL PROOF.md §1–3 goes to the cross-family proof checker in check wave 2. Theorem V (everyone's rank 1) rests on it.
- **R_n as a hypothesis in Theorem H(f)** (B:690). This is a meeting matter: ground rule 5 against ground rule 6, because E[W²|𝒞] is not a model or design condition. Round 2 settles it.

## HQ rulings (2026-11-04), verbatim in `evidence/2026-11-04_HQ_RULINGS_Q1-Q4.md`; how the meeting applies them

| Q | Ruling | Applied as |
|---|---|---|
| Q1 §5.3 | Bridge form ACCEPTED if paper 1 ships all of (a) the discrepancy half (π₀ vs π divergence controlled by cross-block terms + the σ²-coupling term, ε > 0 family, constants), (b) the bridge-form stability theorem (IC3 exhibited), (c) the refutation of the one-shot form (OWS-WS6(d), WS7) after a cross-family check | Round 2 must produce one §5.3 package with three named parts (a), (b), (c). OWS-WS6d and OWS-WS7 (author Opus 5.5, O-WSTAB PROOF.md §6–§7, author-only) go to PC1 (gpt-6.1-sol) in check wave 2; if the check fails, Q1 returns to HQ. If (a) or (b) lacks a credible route at close → escalation to HQ, never dropped. |
| Q2 §5.4 coverage | Posterior-content / Monte Carlo reading ACCEPTED: |π(C(π̂)) − nominal| for reported credible quantities + their MC error | Round 2 cards state it in that form. Frequentist coverage of the exact posterior → `FUTURE_WORK.md` (entry FW1). |
| Q3 §5.4 masked TV/KL | Not binding; obligation with fallback | Masked final-estimate TV/KL → `FUTURE_WORK.md` (FW2, V11/N10 OPEN); reverse-KL obstruction stated as a definitional fact. **Requirement:** the final list names at least one masked-regime accuracy statement paper 1 proves — Round 2 seats must name it (candidates: the certificate card's detection of underestimation, K42/K43/K45; a PIP bound conditional on delivery). |
| Q4 Ĵ, leakage proxy | REPORTING, allowed (from existing quantities only; no random numbers; no feedback; POST HOC) | Round 2/3 seats give exact definitions (estimator, numerical label); the chair sends them to HQ at close for AMENDMENT_HQ_02. |
| Chair | N9 → cross-family check in wave 2; R_n in H(f) is the meeting's | N9-KERNEL PROOF.md §1–3 → PC1 in wave 2 (author Claude; checker Codex Sol). R_n settled in Round 2. |

**Q1(c) check, done 2026-11-04** (`evidence/CHK_INHERITED/REPORT.md`, PC1 gpt-6.1-sol, cross-family, line by line):
- **Verdicts:**
  - OWS-WS6(d): VERIFIED WITH AMENDMENT. Its TV conclusion needs the bounded-block setting (shipped B ≤ 16) or π₀(S₀) → 1 as a premise. The χ² divergence does not need either.
  - OWS-WS7: VERIFIED WITH AMENDMENT. The amendment is wording only, on particle presence and the stage-count approximation; the obstruction is unchanged.
  - OWS-WS3: VERIFIED.
  - OWS-WS4: VERIFIED.
  - N9-KERNEL §0–3: VERIFIED WITH AMENDMENT. The prose treats sufficient order conditions as necessary; the RB consequence needs stationarity made explicit.
- **One-shot refutation:** the report's answer is "Yes, for the mathematical laws of the shipped start and target", in the bounded-block setting (§6). WS6(d) refutes it already at zero cross-block dependence. WS7's masked-family premises (H3, the joint ratio law) remain non-design premises.
- **Consequence:** the Q1(c) condition is met, so (c) can ship as a stated proposition with these amendments. It does not reopen with HQ.

## Q5 (2026-11-04, after check wave 2). How should "stage count continuous in ε" in Q1(b) be read?

**Facts from check wave 2** (`evidence/W2_PC1/VERDICTS.md` §"Seat D/B item 1" and its "Disposition for the chair"; `evidence/W2_PC2/VERDICTS.md` §0 item 2):
- The stage count T of the coded greedy grid is an **integer**, so it cannot be continuous in ε at a threshold crossing.
- PC1 builds an actual BVS design where the block-orthogonal baseline sits at a threshold (one-sided counts {2, 4}). A cross-block correlation of ε = 10⁻⁵ then gives T = 3.
- **What is true and checked as written** (TRUE-AS-WRITTEN, design verified, ε > 0):
  - **The sandwich:** T_bd(.9e^{−4η}) ≤ T_true(.9) ≤ T_bd(.9e^{4η}), for common pilot targets, with η → 0 as ε → 0 (PC1, A/B/D (b)(iii)).
  - **Local constancy:** T equals the baseline count for small ε when the baseline is not at a threshold (a "non-critical threshold" condition).
  - **Continuous envelopes:** the stage χ² and weights, the Doeblin constants, M₂ ≤ e^{D_*}, and an upper envelope T ≤ 2⌈D_*/c_ρ⌉ + 2 that is continuous in ε (PC2, against the coded pilot).
- PC1: *"A fallback omitting stage count entirely would not meet binding Q1(b)."*

**Decision needed.** Does Q1(b) accept "stage count controlled continuously in ε"? That would mean all three of the following:
- the sandwich between baseline counts at thresholds e^{±4η}·0.9 (η → 0);
- local constancy at non-critical thresholds;
- a continuous upper envelope.

The literal alternative, the integer T as a continuous function, is false by construction, as PC1's counterexample shows. The meeting proceeds on the reading above unless HQ rules otherwise.
