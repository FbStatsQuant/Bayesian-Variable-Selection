# W2-VT24G working notes (adversarial referee of W1-T24G)

Source under review: branch origin/theory/W1-T24G, theory_campaign/W1-T24G/{REPORT,PROOF,NOTES}.md, scripts, results.
Checked against: Docs/Methodology/METHODOLOGY_v3.md §§6.5, 6.6, 6.8, 6.10; Scripts/SMC_BVS/core/cpp/v3_engine.h
(the production round); T09/T10 statements; T21 STATEMENT.md and PROOF_v3.tex §Route (e).

## Step 1 (2026-11-02): round model vs implementation
- v3_engine.h::one_round: Fisher-Yates permutation of the m = p+B+2 canonical labels, drawn from the stream before
  any step of the round, independent of the state => (R1) holds. Each label once => (R2).
- step_gibbs: held(P) records the current state, eval(flip) scores the other configuration if feasible (cap) => SR,
  (R3), (R4) hold in the implementation.
- step_uswap / step_nswap / step_indep: exactly the kernels of PROOF.md §0 (Hastings ratio |N(j)\S|/|N(l)\S'|;
  neighbour swap with empty candidate set returns without a score).
- run_island_s: after the last bridge stage (phi = 1, resample, one round) come L burn-in and Hm = 4 measured rounds
  with no resampling => (R5) holds under EX-S. Note: there are actually L+5 rounds at phi = 1 after the last
  resampling (the final bridge stage's round), so H = L+4 is conservative by one round.
- One RNG stream shared sequentially by all particles; under EX-S (iid uniforms) the per-particle blocks are fresh
  at stopping times, so the trajectories are conditionally independent given the population (strong Markov
  property of an iid sequence). (R5) VERIFIED under EX-S; it is not literally "per-particle streams".
