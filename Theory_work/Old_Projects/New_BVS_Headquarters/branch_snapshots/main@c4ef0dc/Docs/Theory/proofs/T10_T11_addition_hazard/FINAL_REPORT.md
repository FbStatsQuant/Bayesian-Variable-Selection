# FINAL REPORT — T10 (old label T11): feasible-addition hazards and ordered paths

**Result: proved (Opus 5.5 lead; reviewed by 2 independent Opus 5.5 xhigh, CP + CW); not adopted.** Adoption is Felipe's word.

- Statement: `STATEMENT.md` (v3). Proof: `proof/PROOF_v4.tex` and `proof/PROOF_v4.pdf` (8 pages, 0 LaTeX errors).
- Protocol: proof.md with the WAVE3_BRIEF overrides. Lead: Claude Opus 5.5 (high), on Claude Work. Date: 2026-10-22.

## What the theorem says (plain words)
- **(i)** At every temperature φ ∈ [0, 1], adding one variable j to a feasible model S of size k < K never lowers the bridge weight by more than the factor r_k = (k+1)/((2p−k−1)√(n+1)). So the Gibbs step adds j with probability at least h_k = r_k/(1+r_k), and π₀(S+j) ≥ r_k·π₀(S).
- **(ii)** In one round, a fixed set J of a new variables is visited with probability at least C(m,a)⁻¹∏h. The factor C(m,a)⁻¹ is the chance that J's Gibbs steps come first. For a = 1 the bound is h_k/m.
- **(ii-neg)** The old v2 claim "no ordering constant for a = 1" is false. Explicit counterexample: p = 2, two orthogonal pure-noise columns, n ≥ 400, every φ ∈ [0, 1]. There the probability of visiting S+j in one round is at most (23/60)β + (31/3)β², which is below h_1, where β = n^{−1/2}.
- **(iii)** At any actual Gibbs-j execution from a state S, given the whole past, j is added with probability o_j ≥ h_k. Hence the expected number of such entries is at least h_k times the expected number of such executions.
- **(iv)** These are visit statements, not end-of-round statements, and they say nothing about discovery within the budget:
  - **(a)** In the same example, the chance of being at S+j at the end of the round is at most (4/3)β². That is below h_1/m and vanishes relative to it.
  - **(b)** For fixed a, the bound in (ii) is at least a!(16√2·n^{2A+1/2})^{−a} when p ≤ n^A: inverse-polynomial.
  - **(c)** With p = n, summed over the whole final-run budget, both the (ii) bound and the (iii) bound tend to 0. So they give no discovery guarantee.
  - **(d)** At the cap (|S| = K) no addition ever happens.

## Statement changes
- Decision at step 1: **(a) correct as stated.** No hypothesis was added or removed and no conclusion was weakened.
- The informal clauses got precise readings: (ii-neg), the filtration form of (iii), and (iv-a)–(iv-d). These were approved by the statement checker (fresh Opus 5.5 xhigh) with changes. All required changes were applied:
  - 𝓕_{u⁻} is defined by the stream variates already consumed;
  - φ ∈ [0, 1] for moves is made explicit;
  - the "ratio → 0" claim is marked supplementary;
  - (iv-b) now includes the visit-probability sentence;
  - (iv-c) is scoped to the final run and includes the (iii) analogue.
- After review round 1, the 00_COMMON definitions (data conditions, budget block, final-run structure, exact-branch rule) were quoted verbatim in STATEMENT.md. These are definitions only.
- Files: `review/STATEMENT_CHANGE_REPORT.md`, `review/STATEMENT_CHECK.md`.

## Cited results
- Wave 1 (`COLLECTED_PROOFS_v2.tex`): T09(ii) (kernels, reversibility) and T22 Lemmas 1–3 (positivity; the floor m(S+l)/m(S) ≥ (n+1)^{−1/2}; prior ratio).
- The T22 citation follows the HQ note. The lead's PROOF_v1 had re-derived the floor and was replaced by the citation in v2.
- No unproved v3 conjecture is used.

## Consequence for T21 (HQ question)
T21's hypothesis H10 ("π₀(S+j) ≥ r_kπ₀(S) for each feasible addition") is exactly wave-1 T22's lemma "One feasible addition under π₀" (`T22:lem:pi0add`). So H10 was already discharged in wave 1. It is now also given by T10(i) (φ = 0 case).

## Review history
| Round | CP reviewer (Claude Personal, delegate_task) | CW reviewer (Claude Work, native agent) |
|---|---|---|
| 1 (PROOF_v3) | not verified: 1 gap (budget formulas not in packet), 6 exposition | not verified: same 1 gap (F1), 8 exposition |
| 2 (PROOF_v4) | **verified**; all round-1 findings resolved; 3 new exposition | **verified**; all round-1 findings resolved; 3 new exposition |

- Fatal findings: none.
- Gap findings: 1, raised by both reviewers, accepted and fixed. See `CLAIMS_OF_FATAL_FLAWS.md`.
- No dispute arose. No judge was used.
- Round-2 exposition notes (not applied, so the verified text stays exactly as reviewed; none affects a conclusion):
  - (1) The conditional-form illustration conditions on a σ-field containing 𝓒 rather than on 𝓒 itself. It is marked not used.
  - (2) φ_u is undefined beyond the last step; the fix is the convention φ_u := 0.
  - (3) Remark 6(a)'s "runs no SMC round" says slightly more than the quoted exact-branch rule; the remark is not used.
  - (4) EX-S has several streams; the consumption-ordered sequence of draws is i.i.d., so the argument is unchanged.
- Reports: `review/REVIEW_R1_CP.md`, `review/REVIEW_R1_CW.md`, `review/REVIEW_R2_CP.md`, `review/REVIEW_R2_CW.md`.

## Caveats
- The counterexamples for (ii-neg) and (iv-a) use p = 2. In production the method would take the exact branch there. They are statements about the round kernel itself, which is defined for all admissible data. The original's own evidence (J8, p = 4) is also on the exact branch.
- A counterexample in a regime where SMC actually runs (p ≳ 18) was not constructed. The statement does not require one.
- Corroboration only, not used in the proof: `checks/` holds single-seed, local scripts (exact rational enumeration of the p = 2 example; random-design checks of the floor and part (i)). Both reviewers independently confirmed the enumerated figures by hand.
- Statement-checker side note: the theorem file's J8 "floor 0.0659" equals h_3, not h_1, for p = 4, n = 200. This is an inconsistency in the provisional evidence, not in the statement.

## Agent counts
- Opus 5.5 (xhigh): 3 agents (1 statement checker on CW; 2 reviewers, CW and CP, each used for 2 rounds).
- Helpers: 0. Sonnet: 0. Judge: 0. Fable: 0.
