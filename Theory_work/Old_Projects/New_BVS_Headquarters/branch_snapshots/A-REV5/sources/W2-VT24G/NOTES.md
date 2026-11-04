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

## Step 3: numerics
- CE1 (ce1_recheck.py; results/ce1_recheck.json): CONFIRMED independently. Seed 1 (W1's data): exit MC S1 0.16-0.22,
  S2 0.62-0.78, S3 0.90-0.96, S4 0.89-0.96, S5 0.93-0.97, S6 0.72-0.95. New: an EXACT (enumeration) first-change
  lower bound P*_exit >= 0.39 in every S2-S6 cell (>= 0.53 in S3-S6), so the n=200 counterexample does not rest on MC.
  Fresh data seeds 2-4: same picture (S2-S6 exit 0.67-0.98).
- CE1 scaling (ce1_scaling.py): exit probability does not decay with n (S2: 0.77 -> 0.96 from n=200 to 3200).
- Cor. P1 (p1_and_repair.py): a1 min 0.139-0.439, every a1 <= simulated scoring frequency. CONFIRMED (B = 4 only).
- Repair from raw pi_0 draws with the PRODUCTION packing: 100% within 12 rounds in all 12 cells (confirmed);
  round-1 fractions differ from W1 for S5 (0.19-0.25 vs W1 0.11-0.12) because W1's pi_0 differs.
- v = |M|+|A|+c at pi_0 draws: S5 c=0.5 has 10% of draws with v > H = 12 (bound trivially >= 1 there).
- ERROR in W1 PROOF.md §6 (NL0 row): inflation for equicorrelated nulls is (1+r) = 1.3, not (1+r)/(1-r) = 1.86
  (nl0_inflation.py: median max-ratio 1.08 -> 1.21 for p = 1e2 -> 1e6, approaching 1.3). Threshold for NL0(1) failing
  in rate is p >> n^{1/(2r)} = n^{5/3}, not n^{0.58}.
