# BRIEF — W1-T24G (Gibbs-path repair; restated T24)

Saved verbatim-in-substance from the scheduled prompt (fired 2026-11-02 16:08 UTC, routine "W1-T24G Gibbs-path repair").

You are a cloud research run in the SMC-BVS theory campaign (HQ-managed). TASK_ID = W1-T24G. Work as a careful research mathematical statistician; this is deep research, take the time it needs.

## PROTOCOL
- Branch `theory/W1-T24G` from main; write ONLY under `theory_campaign/W1-T24G/`. Never touch main, no PR, no notifications.
- First commit: save this prompt as `theory_campaign/W1-T24G/BRIEF.md`; `git push -u origin theory/W1-T24G`.
- Commit AND push after every meaningful step; the run may be stopped any time.
- Status words only: PROVED (complete, checked line by line), PROOF SKETCH, COUNTEREXAMPLE (reproducible), CONJECTURE, OPEN. Never upgrade; all results are candidates pending cross-family review.
- Numerics: Python 3 (pip install numpy scipy sympy mpmath); R NOT available. Exact enumeration at p <= 20 preferred; scripts in `theory_campaign/W1-T24G/scripts/`, fixed seeds, record findings.
- Notation of `Docs/Theory/theorems/00_COMMON.md`. Stay in scope.
- Deliverable `theory_campaign/W1-T24G/REPORT.md`: Headline; refined statements in full with named hypotheses; proofs/sketches (long ones in PROOF.md); evidence; what fails and why; needs escalation; outside scope; confidence card per target (statement, P(true), P(provable at reasonable cost), crux, method change needed?).

## Context
Paper story: SMC-BVS v3's reported HPM (best model ever scored) is consistent because the truth gets SCORED. Main theorem T38: favourable regime (start mass on S0 large) vs masked regime (start mass on S0 ~1e-12 but near-truth region R_d = {U ∪ P: U ⊆ S0, P ⊆ S0^c, |P| <= d} carries ~0.8); masked regime needs delivery of a near-truth particle then REPAIR to S0. Preliminary p>>n data (n=200, p in {500,1000}, s0=14; unreviewed): ~98% of fresh scores come from Gibbs flips (~1.7% neighbour swaps); every reported HPM was first found by Gibbs/swap moves; the final local search repaired 0 fits; all misses are posterior misses. So the Gibbs path is the likely real repair mechanism.

T24 (`Docs/Theory/theorems/T24_T18p_terminal_repair.md`) bounds P(truth never scored) by (1-a)^H + H eta for a particle in R_d at the terminal rounds, but is useless as written: constant 1/(s0+d+B+2)! = 1/31! at s0=14; and LK_d fails in correlated designs because a look-alike of a missing truth has leakage delta^2 ~ (n-1) theta^2 r^2, more attractive than most nulls. Fable's proposed fix (consultant review, 2026-10-28): evaluate LK_d only at states containing S0 (zero leakage); charge look-alike additions at incomplete states to the budget d; replace the full-ordering event by a one-correct-Gibbs-step-per-round progress argument giving (1-c')^{H/(s0+d)} with c' ~ 1/(B+3); H_n = L_n + 4 already n-indexed. Stated failure point: EXIT_d bounding a non-Gibbs undo of a just-made correct step. T21 (HPM composition, proved conditionally) has route (e) resting on the open hypothesis H24 = T24's inputs: K1(x,{S0}) >= a_n and one-round exit probability <= eta_n uniformly on R_d, with a_n >= c_n/2 and (L+4) eta_n -> 0.

## TASK
1. Model one terminal round at phi=1 exactly (randomly ordered Gibbs sweep, swaps, independence moves) from `Docs/Methodology/METHODOLOGY_v3.md` and T09 (kernel validity; in `Docs/Theory/proofs/COLLECTED_PROOFS_v2.tex`). Define a progress potential on R_d.
2. Restated T24 with proof: for a particle in R_d at the start of the terminal rounds, P(S0 not scored within H rounds) <= (1-c')^{floor(H/(s0+d))} + (leakage/exit terms), with c' explicit and polynomial (not factorial), every hypothesis named and checkable. Resolve the EXIT_d issue (can a non-Gibbs move undo a correct step; how is it charged). Use the T10 addition-hazard floor r_k = (k+1)/((2p-k-1) sqrt(n+1)) (`Docs/Theory/proofs/T10_T11_addition_hazard/`) and T09 facts. Note 'scored' includes rejected proposals and every Gibbs evaluation.
3. Show which premises hold w.p. -> 1 under G, R, SE, BM-inf (s0, d fixed); finite-n expressions where possible.
4. Exact small-p computation (p <= 20) of the per-round progress probability on designs mimicking scenarios S1-S6 (generators in `Scripts/Data_generators/` + the R scenario code they source; reimplement in Python), at c=1 and c=0.5; compare with your c'.
5. Show how the restated T24 discharges H24 in T21 route (e) (`Docs/Theory/proofs/T21_T14H_HPM_composition/`).
Read first: 00_COMMON.md, METHODOLOGY_v3.md, the T24 theorem file, T09/T10/T21/T23 statements and proofs, LOCKED_PROOFS.md.
