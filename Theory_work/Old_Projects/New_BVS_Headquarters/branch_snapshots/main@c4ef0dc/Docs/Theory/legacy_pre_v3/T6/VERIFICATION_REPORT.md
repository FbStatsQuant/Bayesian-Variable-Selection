# VERIFICATION_REPORT.md: thread T6 (posterior dimension) and Corollary T9a(i)

Date: 2026-10-14. Lead: Fable 5.1 (high). Protocol: proof.md (theorem proving). Deliverable: `proofs/T6/PROOF.md` (v4), in Markdown as the brief requested.

## Status

- **Theorem T6: verified.** The proof (PROOF.md Sections 1-4, including the nonasymptotic Theorem 8 with the explicit constant K) was reported "every step verified" by all six correctness reviewers (3 Opus 5.5 xhigh, 3 GPT-6 Astra xhigh) in each of three rounds; the only findings against those sections were expository and were fixed.
- **Corollary T9a(i): verified in corrected form.** Sentences (1) and (3) of the draft's corollary (every p; every cap including none; the prior tail, not the cap, enforces the bound) hold as stated. Sentence (2), "m_n = O(s0 l_n)", is false at s0 = 0 (p = 1, omega_n = log log n) and holds as O((s0+1) l_n). The draft must be corrected.
- **Prover-note items.** The exact Markov identity is Proposition 2. The denominator bound with an explicit O_P(1) term (a deterministic constant K, outside an event of probability at most 8/n) is Proposition 7. lambda_min(Gamma_{S0}) >= phi0^2 and ||mu||^2/n <= M enter only in Lemma 4, through delta = (||mu||^2 + ||beta*||^2)/n. The counting objection (Section 6): the identity together with Proposition 7 disposes of it for every polynomial p, and for log p <= c' n with c' < log2/(2 s0) (every p when s0 = 0); the shrinkage floor caps the reward of interpolation (BF <= (n+1)^nu) but does not settle the objection alone; for super-exponential p a reviewer's construction (reported, not proved in the document; consistent with single-draw numerics reproduced independently by three reviewers) indicates that the scenario does occur, with no contradiction to T6 because m_n ~ n^2 there.
- **Not verified:** the Section 6.4 remark's reported construction (the Astra angle-C reviewer's asymptotic analysis, `review/astra_C/ASTRA_REVIEW_C.md`). No result depends on it, and the document says so.
- Hypotheses added: none. Hypothesis not used: p <= n^A (in the convergence statement). Made explicit: n >= 2; sigma*^2, a0, b0, M, phi0 fixed in n.

## Rounds and findings

| Round | Version | Gap or fatal findings (deduplicated across reviewers) | Rulings | Verdict on T6 core / on whole document |
|---|---|---|---|---|
| 1 | v1 | 6: T9a(i) wording at s0 = 0; floor "refutes the premise"; invalid "equivalently" sentence; "for every p" overclaim (Astra C construction); "k ~ n/2" unspecified; l_n not in packet | 5 accepted and fixed; 1 rejected as a packet omission (citation added) | 6/6 verified / 0/6 |
| 2 | v2 | 5: false base-of-log sentence; false "fits a fraction => dominates" heuristic; sigma*^2 unstated and construction not re-derived; m_n ~ n^2/log 2 unqualified; "exactly the polynomial regime" | all accepted and fixed | 6/6 verified / 0/6 |
| 3 | v3 | 0 against the proof or Section 5; 3 in the 6.4 remark (1.24 n inference; wrong event for the dropped models; construction presented as established) | all accepted and fixed in v4 | 6/6 verified, T9a(i) 6/6 verified / Opus 3/3 verified, Astra 0/3 (6.4 remark only) |

Exposition findings: about 40 over the three rounds, all accepted except symbol-reuse notes (no ambiguity) and two packet-omission items (the draft's definition of "in probability" and of l_n, both in the draft but not in the excerpt). Disputed findings: none. Rebuttal rounds: none needed. Rulings: `FINDINGS.md` (rounds 1 and 2) and `FINDINGS_round3.md`.

## Cited results

None external. The Stirling-type lower bound for Gamma is proved inline (Lemma 5); the closed form (1) of the draft is re-derived inline (Lemma 1); the parts of L6 used are proved inline (Lemma 3).

## Numerical checks (not part of the proof)

- `check_T6.py` (lead, single seed): closed form vs quadrature (agreement 1e-12); int m(S) dy = 1 for n = 1 exactly and for n = 6 by defensive importance sampling under the default prior (1.000 +- 0.002); Lemma 3 for p in {1, 2, 5, 50, 500} under every cap; Lemma 5 on a grid; Lemmas 4, 6, 9 including collinear columns; (3.4) on 6000 draws (0 violations, minimum slack 4.8 nats); the Theorem 8 chain and the Markov and Chebyshev frequencies by exact enumeration (p = 10). All pass.
- `review/check_counterexample_astraC.py` (lead, single seed): the reviewer's construction at n = 40 / 80 / 160: posterior mass within 0.1 n of n/2 = 0.60 / 0.73 / 0.88; reproduced independently by Opus A, B and C with their own code.
- Reviewer scripts: `review/REVIEW_{A,B,C}_check.py`, `round2/REVIEW_C_check_round2.py`, `round3/REVIEW_C_check_round3.py`. Opus C ran 20,000 adversarial cases of (3.8) and (3.4) (n up to 2000, s0 up to 40, hyperparameters from 1e-4 to 1e4, collinear columns): minimum slack of (3.4) 2.770 nats, matching the analytic infimum 2.766.

## Agents and calls

- Fable: the lead session only; 0 prover sub-agents; 0 Fable review calls.
- Opus 5.5 xhigh: 3 reviewer agents, each continued across the 3 rounds (9 reviews). No operator or researcher agent was spawned: the records were written by the lead, and no literature search was needed (no external result is cited).
- GPT-6 Astra xhigh: 3 sessions x 3 rounds = 9 codex calls (plus 6 failed launches of round 2 caused by flag ordering; recorded in memory).

## Protocol steps not run, and why

- STATEMENT.md sign-off, the Phase 2 readability review, the Lean decomposition and LEAN_HANDOFF.md, LaTeX compilation, RETRO.md: the brief for this coordinated thread fixed the deliverable as a Markdown proof file against the draft's own statement of T6. These steps are left to the person; the Lean handoff can be prepared from Theorem 8 and Lemmas 1 to 9 on request.
- Adoption: NOT ADOPTED. The person has not walked through the proof.

## Resume point

`proofs/T6/PROOF.md` (= `review/round3/PROOF_v4_final.md`), `review/FINDINGS.md`, `review/FINDINGS_round3.md`, `proofs/T6/STATUS.md`.
