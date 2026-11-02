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

## Step 2: independent engine
- scripts/ref_engine.py (vectorised round, exact enumeration), scripts/exact_laws.py (exact per-label laws).
  Written from METHODOLOGY + the C++; no W1 code imported.
- validate_engine.py: elementary laws pi-reversible (max log residual 1e-3, from 1-o cancellation; 508 pairs
  with underflowed Gibbs odds, 0 unexplained zeros); vectorised round vs slow exact-law round: TV within MC noise.
- FINDING (evidence-level GAP in W1): W1's blocks (scipy to_tree pre_order leaf order) differ from the
  production packing (v3_blocks.h: left child = child with smaller min index; leaves left-first). The retained
  clusters agree, the packing does not (e.g. S5: production [[0],[1..4],[10,12,13],[11,14,15,16],[17,18,19],
  [5,7,8],[6,9]] vs W1 [[5,7,8],[6,9,15,16],[0,17,18,19],[1..4],[11,14],[10,12,13]]). This changes pi_0 and the
  independence move, hence W1's start-law statements (T4b, "S5 masked"), not the theorem.
- CE2 (ce2_check.py): exact; brief's form violated in 395/1050 (v,H,c) cases, including v=2, H=12, c=1/20
  (0.88 > 0.74). W1's v(1-c)^floor(H/v) dominates in all. VERIFIED.
