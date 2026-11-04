# BRIEF — W1-T37R (verbatim scheduled prompt, fired 2026-11-02 16:57 UTC)

You are a cloud research run in the SMC-BVS theory campaign (HQ-managed). TASK_ID = W1-T37R. Work as a careful research mathematical statistician; this is deep research, take the time it needs.

## PROTOCOL
- Branch: create `theory/W1-T37R` from main; write ONLY under `theory_campaign/W1-T37R/`. Never touch main, no PR, no notifications.
- First commit: save this whole prompt as `theory_campaign/W1-T37R/BRIEF.md`; push with `git push -u origin theory/W1-T37R`.
- Commit AND push after every meaningful step (lemma, counterexample, script, draft section). The run may be stopped any time; unpushed work is lost.
- Status words only: PROVED (complete, checked line by line), PROOF SKETCH, COUNTEREXAMPLE (reproducible), CONJECTURE, OPEN. Never upgrade. Everything is a candidate pending cross-family review.
- Numerics: Python 3 available (pip install numpy scipy sympy mpmath); R is NOT available. Prefer exact enumeration at p <= 20. Scripts under `theory_campaign/W1-T37R/scripts/` with fixed seeds; record what each showed.
- Use notation of `Docs/Theory/theorems/00_COMMON.md`. Stay in scope; note outside-scope findings briefly.
- Deliverable `theory_campaign/W1-T37R/REPORT.md`: 1 Headline (3-6 lines, status words); 2 Refined statements in full with named hypotheses; 3 Proofs/sketches (long ones in PROOF.md); 4 Evidence; 5 What fails and why; 6 Needs escalation (steps needing a stronger prover/independent check); 7 Outside scope; 8 Confidence card per target (refined statement, P(true), P(provable at reasonable cost), crux, method change needed?).

## Context
The paper story: what SMC-BVS v3 reports is consistent because the truth gets SCORED (HPM = best model ever scored), not because the sampler converges. Main theorem T38 has a favourable regime (start mass on S0 large) and a masked regime (start mass on S0 ~ 1e-12 but on the near-truth region R_d ~ 0.8); in the masked regime a near-truth model must be delivered and then REPAIRED to S0. T37 is the primary repair route; T24 (Gibbs path) the alternative. Repo references: method spec `Docs/Methodology/METHODOLOGY_v3.md`; theorem files `Docs/Theory/theorems/` (incl. T24_T18p_terminal_repair.md, 00_COMMON.md); proofs `Docs/Theory/proofs/` (T01_T02 PROOF_v3.tex; wave-1 proofs inside COLLECTED_PROOFS_v2.tex; LOCKED_PROOFS.md); engine `Scripts/SMC_BVS/core/`; data generators `Scripts/Data_generators/` (+ R scenario code they source; reimplement in Python).

Preliminary data (p >> n, n=200, p in {500,1000}, s0=14, 2,400 fits; unreviewed): masked regime almost everywhere; ~98% of fresh scores come from Gibbs flips; the final local search repaired 0 fits although 541 fits had a centre in R_2 minus S0; all misses are posterior misses (F(S0) <= F(HPM)), none search misses. Literal TD held strictly in 0 of 95 sampled d=0 cases; decision D18: the literal TD fails generically whenever a swap that brings in a missing truth is available; a 'toward S0' variant did not separate from the literal one in that partial audit. Fable's earlier note: a look-alike l of a missing truth has leakage delta^2 ~ (n-1) theta^2 r^2.

## The current T37 file (verbatim)
# T37: Finite-n truth dominance and deterministic greedy repair
Definitions: Local search = the production local search: scores every feasible flip and swap of the centre, moves to the best strict improvement, at most l moves, ends with a final certifying scan. Near-truth region R_d = {U ∪ P : U ⊆ S0, P ⊆ S0^c, |P| <= d}, s0 + d <= K. Gains g(S,l) = F(S+l) - F(S), h(S,j) = F(S-j) - F(S); swap gains likewise. TD(d,m), m >= 0: (1) for every S in R_d with S not ⊇ S0, some missing true j has g(S,j) >= m + gain of every other feasible move at S; (2) for every S in R_d with S ⊋ S0, some extra l has h(S,l) >= m + gain of every other move; (3) at S0 every move has gain <= -m.
Assumptions: EX-A; fixed X and S0. (ii) adds G; (iii) adds R, SE, BM-inf, s0 and d fixed.
(i) Deterministic: under TD(d,0) strict, from any centre S in R_d the local search with l >= |S Δ S0| moves monotonically to S0 in exactly |S Δ S0| moves, scores S0, reports local_certified at S0, never leaves R_d. Hence S0 in scored set, and Shat = S0 whenever pi(S0) > 1/2 (T21).
(ii) Finite n: under G, fixed X, P0(TD(d,m) fails) <= sum over the <= 2^{s0} C(p,d)(p + s0 p) distinct move comparisons of P0(single score difference < m); each a 1- or 2-dim non-central Gaussian event with non-centrality (n-1) delta^2_{T,l} / sigma*^2 and penalty (1/2) log(n+1) + log[(2p-k-1)/(k+1)].
(iii) s0, d fixed, l_n = ceil(log2(n+p+1)) >= s0 + d eventually, G, R, SE, BM-inf: bound in (ii) -> 0, so TD(d,0) w.p. -> 1; (i) becomes an unconditional repair route replacing GAIN_d, LK_d, EXIT_d.
Why: each gain is monotone in one residual projection u^T y (two for swaps); adding missing true j gains full non-centrality (n-1)||(P_{T+j} - P_T) mu||^2, its look-alike only the r^2 share; once S0 ⊆ S, nulls have zero leakage and pay the size penalty; greedy order 'truths in, then extras out'. Margin (n-1) theta^2 (1-r^2)/(2 sigma^2) proposed as mechanism of the correlated-design advantage (S3-S6 at c=0.5).
Risks: 2^{s0} union loose at s0=14 (~10 nats); at n=200 l=10 < s0+d=15; T37 does not deliver an eligible centre (T38's job).

## TASK
1. Diagnose exactly why literal TD fails: which move beats the missing-truth addition, at which states, with what score gap (in T01 contrast coordinates / residual projections). Confirm by exact computation on small designs (p <= 20) mimicking scenarios S1-S6.
2. Restate: propose the WEAKEST condition TD' under which greedy best-improvement local search from any S in R_d reaches and certifies S0 (candidates: a progress/potential condition where every best move strictly decreases a potential such as |S Δ S0| or a lexicographic (missing truths, extras) potential, counting truth-bringing swaps as progress; a path-wise condition along the greedy path only; an extra-scan version). State refined T37(i) and PROVE it.
3. Finite-n: analogue of T37(ii) for TD' with an explicit bound, preferably dependence-aware/path-wise instead of the 2^{s0} union; then T37(iii) (-> 0 under G, R, SE, BM-inf) with proof or sketch.
4. On simulated small cases, report how often TD' holds at n=200-like signal (c=1 and c=0.5, correlated scenarios). If it fails at n=200, say so plainly (theorem then asymptotic only). Address the move cap l=10 < s0+d.
5. Briefly: is the right repair statement for this method about Gibbs flips rather than the local search? (Another run covers the Gibbs route; just give your view.)
Read first: 00_COMMON.md, METHODOLOGY_v3.md (local search spec, score F, g-prior, BB(1,p)), T01 statement/proof, T24 theorem file.
