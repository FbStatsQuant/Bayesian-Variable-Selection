# BRIEF — W1-EXP (stored scheduled prompt, saved verbatim in substance)

You are a cloud research run in the SMC-BVS theory campaign (HQ-managed). TASK_ID = W1-EXP. Work as a careful research mathematical statistician; this is deep research, take the time it needs.

## PROTOCOL
- Branch `theory/W1-EXP` from main; write ONLY under `theory_campaign/W1-EXP/`. Never touch main, no PR, no notifications.
- First commit: save this prompt as `theory_campaign/W1-EXP/BRIEF.md`; `git push -u origin theory/W1-EXP`.
- Commit AND push after every meaningful step; the run may be stopped any time.
- Status words only: PROVED (complete, checked line by line), PROOF SKETCH, COUNTEREXAMPLE (reproducible), CONJECTURE, OPEN. Never upgrade; results are candidates pending cross-family review.
- Numerics: Python 3 (pip install numpy scipy sympy mpmath); R NOT available. Exact enumeration at p <= 20 preferred; scripts in `theory_campaign/W1-EXP/scripts/`, fixed seeds, record findings.
- Notation of `Docs/Theory/theorems/00_COMMON.md`. Stay in scope.
- Deliverable `theory_campaign/W1-EXP/REPORT.md`: Headline; refined statements in full with named hypotheses; proofs/sketches (long ones in PROOF.md); evidence; what fails and why; needs escalation; outside scope; confidence card per target (statement, P(true), P(provable at reasonable cost), crux, method change needed?).

## Context
Paper Thm 2 = the start: T22 + T27. T22(i)(ii)(iv) deterministic, PROVED-LOCKED (wave 1; proofs in `Docs/Theory/proofs/COLLECTED_PROOFS_v2.tex`, statements in `Docs/Theory/proofs/T22_T16_start_aggregation/`). T22(iii) (favourable regime: 1 - pi0(S0) = O_P(2^B sqrt(log n) n^{-kappa})) and T27(i) (masked regime: pi0(S0) = p^{-c} n^{-c/2} e^{O_P(1)}) are PROVED-LOCKED but CONDITIONAL (`Docs/Theory/proofs/T22iii_T16_start_aggregation/`, `Docs/Theory/proofs/T27i_T20C_cancellation_budget/`, register LOCKED_PROOFS.md): T22(iii) rests on EXP' (log-ratio expansion with O_P(1) remainder; Decision Point 2 D1; an audit sketch suggests it may follow from G, R and within-block SE, unverified), VIS (visibility), NL_eta (leakage bound), NL_avg(kappa); T27(i) rests on H2 (sequential ratio law: along a chain of c feasible single additions from S^(0) to the truth each table ratio ~ n^{-1/2}) and H3 (normalised reference-mass lower bound). NEVER combine T22(iii) and T27(i) on one sequence (different regimes). Astra's rule for the paper: prove compatible premises JOINTLY on ONE design family. Common setting: triangular array, s0 fixed, p_n <= n^A, B <= 16. Near-truth region R_d = {U ∪ P: U ⊆ S0, P ⊆ S0^c, |P| <= d}. The main theorem T38's masked-regime branch needs: pi0(S0) vanishing as in T27 but pi0(R_d) >= b_n via T22(i) with a reference S° in R_d (S° != S0 allowed). Preliminary p>>n data (n=200, p in {500,1000}, s0=14, unreviewed): 1 of 2,394 fits favourable; median pi0(S0) ~ 1e-12; median pi0(R_2) ~ 0.8. Fable warned a restricted T22 regime with uncheckable hypotheses must not eat the repair theorem's time: favour clean, checkable conditions.

## TASK
1. EXP' in the block-orthogonal benchmark (columns orthogonal across blocks, arbitrary within-block correlation): prove it from G, R, within-block SE. Then say how far it extends (weak cross-block correlation; iid Gaussian designs with the actual X-dependent partition).
2. Replace T27's assumed ratio law H2 by a bounded-leakage condition along the chain (two-sided law with a controlled multiplier); prove T27(i) from it.
3. Construct ONE explicit design family (e.g. correlated blocks with cancelling true variables) on which T27 masking holds (pi0(S0) -> 0 at the stated rate) AND T22(i) gives near-truth start mass pi0(R_d) >= b_n with b_n non-vanishing or at most polynomially vanishing. Keep it as close as possible to the study's correlated scenarios S3-S6 (generators `Scripts/Data_generators/` + the R scenario code they source; reimplement in Python). This is the input T38(b) needs.
4. Exact computation at small p (<= 20) of pi0(S0) and pi0(R_d) on the family as n grows; show the predicted rates. The start sampler pi0 is specified in `Docs/Methodology/METHODOLOGY_v3.md` (block tables, composite start) and implemented in `Scripts/SMC_BVS/core/`.
5. Make the regime split explicit in every statement.
Read first: 00_COMMON.md, METHODOLOGY_v3.md start-sampler sections, the T22/T22iii/T27i statements and proofs, LOCKED_PROOFS.md.
