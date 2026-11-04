# Paper 1 theorem list: for Felipe's approval

HQ, 2026-11-04. The theorem meeting closed with no open questions (`MINUTES.md`). HQ has reviewed and approves the package below, subject to your approval. The full statements are the cards in `THEOREM_LIST_FINAL.md`; each main theorem has an HQ charter in `HQ_CHARTERS/`.

## How it was made

- **Seats:** four, two Fable 5.1, Astra, and a fresh-eyes Fable that first saw only the method; plus a one-shot raw Astra. The chair did not vote.
- **Candidates:** 108 in total, from the earlier draft list (24), the two fresh-eyes plans (72 + 44) and the 17 obligations left by the method meeting.
- **Checks:** two rounds of cross-family proof checks (Sol 6.1 on the Fable seats, Opus on Astra), plus a line-by-line check of the inherited proofs the list depends on.
  - They found 20 counterexamples to draft statements, which were repaired or removed.
  - Every synthesis was audited: one failed audit was fixed, and the final audit was "pass with corrections", all applied.
- **Outcome:** every candidate ended up in the list, in future work (27, each with a reason), as a cited published result, or dropped (6, with reasons).

## The 8 main theorems (unanimous)

| # | Theorem | What it guarantees, plainly | Your goal it serves |
|---|---|---|---|
| M1 | **Validity and accuracy** | For any data and any correlation, the method targets the exact posterior: unbiased evidence and correct PIP and general-summary identities on every island, with any number of islands fixed in advance. The reported PIPs, joint inclusions and general posterior summaries have explicit error bounds and converge to the truth as islands grow. | §5.1, §5.2, §13.1 (binding), objective 1 |
| M2 | **Weight stability (§5.3 package)** | (a) The distance between the local-to-global start and the true posterior is controlled by the cross-block correlation, plus a noise-variance term present even for orthogonal blocks. (b) The bridge is stable as cross-block correlation grows from zero. The per-stage weight bounds are continuous; the stage count is a whole number held within two-sided bounds. (c) The literal one-shot version (bounded weights from the start alone) is false, and the paper proves it. | §5.3 (binding) |
| M3 | **The start** | How much posterior mass the start carries: a deterministic lower bound; the exact decomposition of the start's error; the masking law (how cross-block masking reduces the true model's start mass); dilution. | §5.3, local-to-global |
| M4 | **Evidence and certificates** | The top-model store gives a deterministic two-sided bracket on the evidence and PIPs. The run's certificate card is sound (5% joint error at most), and it detects underestimation. Also the paper's proved accuracy statement for masked designs. | §5.4, objective 1 |
| M5 | **Selection by the reported HPM** | A finite-n bound on selection error at every n. With LS0, the reported HPM finds the true model with probability → 1 on masked (correlated) designs of the LH family. Greedy local search provably repairs the start. | objective 3 |
| M6 | **Why the merge alone fails** | Correcting the start in one shot needs polynomially many (in p) draws, which is the bridge's reason to exist. A KL lower bound gives the exact cost scale. | local-to-global thesis |
| M7 | **Stage laws** | How many sequential tempering stages the coded schedule uses: a bounded number for favourable designs, about log₂(masking depth) for masked ones. This is the formal sense in which correlation costs sequential depth. | objective 2, thesis |
| M8 | **Work, depth and width** | The parallel cost at the island level, in the same units as Song–Liang §6, with no speed claim beyond what is proved. | objective 2 |

**The thesis sentence** ("correlation costs depth and particles, never correctness") appears as a remark scoped to exactly what M1, M2, M7 and M8 prove.

## 12 supplement cards

These are full results in the supplement, proved by grouped "lemma-pack" HQs:
- target consistency (the posterior concentrates on the true model, T03♯);
- target properties and the exact branch;
- block-construction facts;
- kernel validity (N9) and the start sampler;
- the divergence and credible-set calculus;
- certificate and local-search semantics;
- output validity and worker equivalence;
- evidence variance and masked tails;
- pooling rules;
- limitations stated as theorems;
- the two new run-card numbers;
- a leakage corollary.

## What I need you to decide

1. **Approve the list:** 8 main theorems and 12 supplement cards.
2. **The Song–Liang separation is in future work.** The meeting could not get a sound analytic proof that Song–Liang's split-and-merge loses true predictors under correlation. Its key step is an unproved claim about their algorithm, which both check waves rejected. So paper 1 *compares* with Song–Liang (Theorems 1, 2, 4 and §6) and cites the numerical counterexample as labelled evidence; it does not claim a proved separation. Your thesis needs only half of this: our validity under any correlation (M1) is proved. **My recommendation:** run one small scout HQ on the separation alongside wave 1. If it lands, it becomes a ninth main theorem; if not, nothing else waits on it.
3. **Prop D (M8) in the main text,** for objective 2. The fresh-eyes seat's alternative is to move it to the supplement, leaving 7 main theorems. My recommendation: keep it main, because parallel scalability is objective 2.
4. **My readings of your proposal goals (you may overrule):**
   - **§5.3** is met by the bridge-form package M2 (a)(b)(c). **Honest scale:** the exhibited family gives useful constants only for very weak cross-block correlation, of order ε ≲ n^{−1/2}/p. A sharp statement of how weak is weak enough is future work.
   - **§5.4 "credible-interval coverage"** means how far the computed credible quantities are from the exact posterior's, not frequentist coverage (which is future work).
   - **§5.4 TV/KL of the final estimate in masked designs** is future work. §5.4 is still met by the PIP, joint-inclusion, store-TV and start-TV/KL results, and M4 gives a proved masked-design accuracy statement.
   - **The stage count is a step function** of the correlation strength, controlled by two-sided bounds.
5. **Two new run-card numbers** (a Jeffreys-divergence estimate and a cross-block correlation measure) are added as reporting only (AMENDMENT_HQ_02). The method's law is unchanged.

## After approval: the per-theorem HQs, in 4 waves

| Wave | HQs | Why first |
|---|---|---|
| 1 | M1 (validity/accuracy), M3 (start), LP-FOUND (target, blocks, kernel) | Foundations; M1's general-summary identity is the longest pole |
| 2 | M2 (§5.3), M7 (stages), M6 (merge fails), LP-IDENT | §5.3 needs M3, M6 and M7 |
| 3 | M5 (HPM), M4 (evidence/certificates), M8 (work/depth), LP-AUDIT | Code-audit wave (LS0, stop handling, parallel execution) |
| 4 | LP-REST, LP-REP | Consequences and reporting corollaries |

Each HQ loops to a referee-checked proof and a Lean certificate for its finite core. Waves run 3–4 HQs at a time on the subscriptions. The binding goals have safeguards: if the proof behind §13.1 or §5.3 fails, it comes back to you rather than being dropped.
