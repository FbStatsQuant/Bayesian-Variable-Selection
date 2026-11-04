# T27(i): final report

**proved (Astra lead; reviewed by Sol 6.1 x2); not adopted**

Date: 2026-10-22. Only part (i) is proved. Felipe alone decides adoption.

The result is the conditional implication

\[
\pi_0(S_0)=p^{-c}n^{-c/2}\exp\{O_{P_0}(1)\}.
\]

Both the multiplier and its reciprocal are tight. The proof does **not** establish the two statistical premises: the sequential table-ratio law or the normalized starting-model mass bound. The profiling campaign's support for the algebra does not turn either premise into a theorem.

## Deliverables

- [Final proof PDF](proof/PROOF_v2.pdf) and [LaTeX source](proof/PROOF_v2.tex).
- [Precise statement with every premise](STATEMENT.md).
- [Findings and responses](CLAIMS_OF_FATAL_FLAWS.md).
- Final independent reports: [reviewer 1](review/round_2/REVIEWER_1_REPORT.md), [reviewer 2](review/round_2/REVIEWER_2_REPORT.md).
- [Astra statement ruling](helpers/ASTRA_STATEMENT_RULING.md).

## What is assumed

The statement explicitly supplies the v3 standardized data, actual deterministic block construction, positive full-response Bayes-factor tables, capped BB(1,p) prior, and exact composite normalizer. The asymptotic setting is n tending to infinity and p comparable to n^a, with fixed a>=0.

1. A specified feasible chain makes exactly c single-variable additions from a reference of fixed size s to S_0. Both s and c are fixed. A data-selected chain is allowed only if the following premise holds on that very chain.
2. At every successive table state, the log table ratio plus one-half log n is jointly O_{P_0}(1), with absolute values controlled. These are the ratios after previous additions, including previous additions within the same block.
3. A fixed c_0>0 satisfies P_0{pi_0(S^(0))>=c_0}->1. This bounds the normalized probability of the reference, not merely its unnormalized weight.
4. The theorem file's EX-A, EX-S, CAL and successful-final-execution conditions are retained explicitly. They mean exact arithmetic, independent separated ideal streams, calibration before fresh final randomness, and completion of the frozen final schedule. The mass conclusion is under the unconditional data law P_0, not conditioned on a selected successful run or diagnostics. No completion-probability theorem is asserted.

For bounded p, the method eventually enumerates; pi_0 then denotes the analytically defined component law rather than an executed sampling stage. The c=0 empty-chain extension is stated separately.

## Why the implication holds

The full normalizer cancels in a ratio of two normalized model masses. The exact size-prior ratio for a single addition at size k is (k+1)/(2p-k-1). Along the chain this gives

\[
\pi_0(S_0)=\pi_0(S^{(0)})p^{-c}n^{-c/2}
A_{p,s,c}\exp\!\left\{\sum_{i=0}^{c-1}E_{n,i}\right\},
\qquad
\frac{(s+c)!}{2^c s!}\le A_{p,s,c}\le\frac{(s+c)!}{s!}.
\]

The reference mass has a tight logarithm by premise 3. The sum of c remainders is tight by premise 2 because c is fixed. This proves the mass law without independence assumptions. The proof reproduces the exact odds calculation directly; it also cites the proved wave-1 T22(ii-a) identity. It does not rely on another unproved v3 conjecture.

## Statement changes and EXP-prime

The conclusion and substantive hypotheses of T27(i) were not changed. Their quantifiers and two-sided stochastic meaning were made explicit. A fresh Astra xhigh checker approved these clarifications, including selected-chain scope, unconditional probability meaning, the exact-branch interpretation and the separately labelled empty-chain extension. No theorem file or method source was edited.

T27(i) assumes the sequential ratio law directly, so neither EXP nor EXP' is an additional premise needed for its mass implication. All expansion discussion uses Decision Point 2's EXP' exclusively. Under EXP' with a uniform tight absolute remainder on a comparison family containing the chain, the sequential law is equivalent to tightness of max_i n x_i. The weaker max_i n x_i^2=O_{P_0}(1) controls only the Taylor remainder. The proof defines partial R-squared and its required nondegeneracy, does not claim an unproved Gaussian quadratic-score identity, and does not transfer leakage-family control to missing-true-coordinate comparisons.

Wave-1 T22(i) could help establish the reference-mass premise in an application only if its lower bound exceeds a fixed positive constant with probability tending to one. Merely checking q_n<1 is not sufficient. That application is not proved here.

## Review outcome

Round 1: the two independent Sol 6.1 high reviewers were launched together in separate restricted packets. Both returned **verified**, with no fatal or gap finding. Both independently identified the same exposition ambiguity: “uniformly on that family” could be read as referring to the full EXP' comparison family.

The lead accepted the finding and changed that phrase to “uniformly over the selected chain comparisons i=0,...,c-1” in v2. All formulas and the precise statement remained unchanged. The verbatim findings and response are preserved in the claims log.

Round 2: both reviewer roles received the unified v2 proof, the unchanged statement, their earlier reports and the findings log. Both returned **verified**, explicitly confirmed that the fix works, and reported no new or unresolved findings. The lead inspected both reports. No judge was needed; no counterexample or failure ruling occurred.

The reviewers' source-access limitation is explicit: their packets were self-contained and they did not inspect external sources. The lead read the cited source material; the proof derives the only needed odds identity internally.

## Validation, provenance and limits

The five-page final PDF was compiled twice successfully using TinyTeX and visually checked on every page. There are no unresolved references, LaTeX box warnings, clipping or overlapping equations. [Validation evidence](proof/VALIDATION.md) includes build logs, timestamps and rendered pages. Source snapshots, SHA-256 hashes, task IDs, prompts and full review responses are saved in this folder.

No simulations, numerical experiments or benchmarks were needed or run. No numerical evidence is substituted for a proof of the premises. The remote NOTS connection attempt timed out before any remote file was read; the EXP' decision is sourced to the local deployment DP2_DECISIONS.md snapshot actually read and the matching decision summary in the user's brief. Remote freshness is not claimed. The external proof.md file changed concurrently in one session-opener sentence; this run preserved its original snapshot and did not edit it. The user's explicit Astra/OpenAI-only overrides govern. See [provenance notes](helpers/PROVENANCE_NOTES.md).

## Agent and call counts

- Astra: one high-effort lead (this thread), one fresh xhigh statement checker (one delegated call).
- Sol 6.1 high: exactly two reviewer roles, two rounds, four delegated review calls/sessions. T3 requires fresh delegated tasks for subsequent review rounds, so the same two roles were reconstituted with their original briefs and prior findings rather than resumed through backing threads.
- Helpers: zero. Counterexample referees: zero. Judges: zero.
- Total: six sessions including the lead; five child-agent calls. All used provider `codex`; no non-OpenAI agents.

No proof work remains pending. The result remains not adopted.


## Claude audit wording fixes (2026-10-23)

Source: WAVE2_CLAUDE_AUDIT/AUDIT_T22iii_T27i.md (optional fix E-T27-1, applied). Wording only; no mathematical content changed. Final proof is now proof/PROOF_v3.tex (copy of PROOF_v2.tex) and its PDF proof/PROOF_v3.pdf; PROOF_v1.* and PROOF_v2.* are superseded and kept. STATEMENT.md unchanged.
- E-T27-1: in section 2, "Multiplying (odds) along the chain and applying H2 yields the exact expression" now reads "... and writing each table ratio as n^{-1/2} e^{E_{n,i}} (the definition of E_{n,i}) yields the exact identity" (H2 is first used in the next paragraph).
- SHA-256: STATEMENT.md da6d6e8a8d67ac94ce23edbf80599701a4c8b1fe9ea109e852181caed6110a95; PROOF_v3.tex 7c875932d33165ed7a570fc2dce9774208215a161ddc1f5a93687a2514f4ef64; PROOF_v3.pdf 8822047e93d0cd2cb4ad24131d94ad28006d6288739bbfa14ce7ec8234f9a90f.
- pdflatex (TinyTeX), two passes: 0 errors, 0 undefined references, 5 pages. Build logs proof/build_PROOF_v3_pass1.txt, pass2.txt.
