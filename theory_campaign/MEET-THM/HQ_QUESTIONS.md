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
