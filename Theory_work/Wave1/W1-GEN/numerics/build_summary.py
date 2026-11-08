"""build_summary.py -- assembles SUMMARY.md from the per-experiment summary tables and the hand-written factual readings."""
import json, os

def rd(fn):
    return open(fn).read() if os.path.exists(fn) else "(missing: %s)\n" % fn

e1 = json.load(open("E1_results.json"))
e7 = "E7_summary.md" if os.path.exists("E7_summary.md") else "E7_summary_main.md"

TOP = r"""# W1-GEN numerics -- SUMMARY

Sub-agent: test/numerics helper for ticket W1-GEN. Everything is in `Theory_work/Wave1/W1-GEN/numerics/` (library `bvs_core.py`, shared code
`exp_common.py`, `lh_common.py`, `study_common.py`, one script `e*.py` per experiment, raw per-run CSVs `E*_raw.csv`, per-experiment
`E*_summary.md/json`, console logs `E*_output.txt`, `EXTRA_stats.md`). No file outside this folder was written; no git command was run.
Environment: Python 3.13 (numpy 2.3.0, scipy 1.15.3) -- the default `python` (3.15) has no numpy. All statements below are about these runs only
(20 noise seeds per row unless stated; "x/y" = number of runs with the property / number of runs); they are numerical observations, not proofs.

## 0. Items that contradict or do not match the expectations in STATEMENT.md / PLAN.md  (read first)

No asymptotic claim of the statement (C1, C2, C3, C5(a)(b)) is contradicted: at n = 3200 every flag (start = S*, path in V, S0 scored, certified, final = S0, HPM = S0) holds in 80/80 (E2),
160/160 (E3, both p), 40/40 (E4(i)) and 20/20 (E4(ii)) runs, and every centre of the sweeps passes. The following points do **not** match what
the statement / plan says or implicitly expects:

1. **S2 (AR(1), rho = 0.5) is not covered, which the plan did not anticipate** (it only expects S5 outside). Population, p = 100, V = the 4 signal groups:
   the canonical S* (smallest-size minimiser, tolerance 1e-7) has 18 elements (14 non-truths, i.e. proxies of truths that sit in neighbouring blocks) instead of 4; VIS(S*) margin is 1.2e-8 to 1.3e-7 (c = 1, n = 200 ... 3200) -- i.e. (H2b) fails for the
   canonical S*; with a noise-level tolerance sigma^2 log n the reference has 4-7 elements but the VIS margin does not grow with n
   (c = 1: 0.165, 0.162, 0.194 at n = 200, 800, 3200; c = 0.5: 2.0 (reference = S0 there), 0.39, 0.40). SEP ratio zeta/(n theta_min^2) = 0.36 for that V (constant in n, so (H1b) fails); enlarging V by one neighbouring
   group on each side of each signal group (|V| = 55) brings the (restricted-family, lower-bound) ratio to 3.5e-4 and by two groups (|V| = 90) to 0 (table E6b) -- so S2 is covered only
   if v-bar may grow. Behaviour of the method on S2 nevertheless: S0 is scored by LS0 in 120/120 runs, final = S0 (and HPM = S0) in 118/120, but the LS0 path leaves the 4 signal groups in 5 / 15 / 26 of 40 runs at n = 200 / 800 / 3200 (up to 7 moves).
2. **Study groups of 5 versus the block size (SIZE / PART-pairing).** With p = 100, B = min(floor sqrt n, floor sqrt p, 16) = 10 = 2g (n >= 100) and with p = 500, n = 200, B = 14:
   the partition packs *pairs of groups* into blocks; blocks == groups in 0/720 route runs and in 0 of 36 population rows (E6), also for S1, S3, S4, S6. This does not affect S* for S1, S3, S4, S6 (no block contains two truths:
   `blocks_with_2plus_truths` = 0 in every row, S* = S0 exactly) but SIZE g_max <= B < 2 g_min is violated, so any argument for (C5)(d) that goes through "blocks = groups" does not apply at these sizes.
3. **S5 degrades with n, and is benign at n = 200.** E5/E6: S5 with p = 100: LS0 scores S0 in 20/20 (iid and exact Gram) at n = 200 (HPM = S0 in 19/20 and 18/20), 18/20 and 20/20 at n = 800, and **0/20 at n = 3200** (both designs): the start mode has 18-21 (iid) / 19-21 (exact) non-S0 elements, LS0 uses all
   ell = 12 moves and stops with local_limit (20/20); the uncapped search reaches S0 in 20/20 runs after 18-21 moves (iid) / 19-21 (exact). SEP ratio is 0.31 (n-free) and the population reference is S* = all 100 variables (tolerance 1e-7; 14-80 variables with a noise-level tolerance). The onset of failure is between n = 800 and 3200; nothing visible at n = 200.
4. **(C6) threshold is very loose.** E7 (p = 120, d proxies with r = 0.6, exact Gram, B = 10, ell = 9/10/12): d = 40, n = 800 and 3200: LS0 scores S0 in **0/20** runs although d/(2B) = 2 << ell + 1; |start \ S0| = 19-25 (n = 800), 30-31 (n = 3200) while the quoted lower bound d/B is 4.
   The mechanism of (C6) is confirmed (the start mode contains x1 plus 19-31 proxies and no other variable, the deletions needed exceed ell, the uncapped LS0 reaches S0 in 20/20 runs after 20-32 moves for n >= 800) but the sufficient condition d/(2B) > ell + 1 is far from where failure starts. d = 20: LS0 succeeds in all runs (moves 3-5, 6-8, 11 at n = 200, 800, 3200; the last one is one move below ell = 12).
5. **Finite-n trap inside the class (E4(i), n = 200, r12 = 0, noise seed 15).** Local search from the centres {} and {x3} stops *certified* at {x3} although F(S0) - F({x3}) = +25.6 nats, because neither {x1,x3} nor {x1} nor {x2} is an improving neighbour.
   Population Lemma-3 decrement for this design at n = 200 is 24.0 = 4.5 log n (9.2 log n for r12 = 0.3). With 20 seeds this happened once (n = 200 only; n = 800 and 3200: no such event). It is a finite-n event, not a contradiction of (C2) (asymptotic), but it shows that the "combination look-alike" trap is realisable at n = 200.
6. **Slow convergence of the centre law (C1).** 1 - pi_0(S*) has median 0.15 / 0.075 / 0.039 (LH exact, n = 200 / 800 / 3200; roughly halves per factor 4 in n), 0.27 / 0.14 / 0.07 (LH-iid p = 108) and 0.30 / 0.17 / 0.09 (p = 396); max over runs at n = 3200 is 0.049 (exact), 0.39 / 0.30 (iid). At n = 200, pi_0(S*) < 1/2 in 7/80 (p = 108) and 10/80 (p = 396) LH-iid runs
   and in 15/40 (S1), 25/40 (S3), 35/40 (S4), 33/40 (S6) study runs, so the "unique maximiser on {pi_0(S*) > 1/2}" shortcut is not available there; nevertheless S~_0 = S* in 78/80, 73/80 of those LH-iid runs.
7. **Shrinking signals (E4(iii), theta = n^{-1/4})**: with n theta_min^2 / log n between 0.1 and 1.8 the BM-infinity regime is not reached at n <= 3200: S~_0 = S* in 6/80, 29/80, 71/80 runs (n = 200, 800, 3200), S0 is the HPM of LS0's scored set in 0/80, 0/80, 4/80. Population VIS margins are 0.44-1.45 (n = 200) and 1.27-4.2 (n = 3200).

Everything else matches the expectations (LH exact Gram: S* = S0 minus masked hubs, blocks = groups in 240/240 runs, S~_0 = S* 240/240, VIS margins positive and increasing ~ n/log n, NL = 0, SEP zeta = 0 to rounding).

## 1. Choices made where the spec was ambiguous (closest reading to the cited source)

* Score: log m(U) = -0.5[logdet H_U - logdet(G_U+I)] - nu log(0.02+Q_U), nu = 0.01 + n/2, y'y = n-1, constant dropped. log w(k) = -log 2 - log binom(2p-1, k) (log-gamma); the common normaliser W_K is dropped in F, gamma_0, Z_0 (it cancels in every ratio).
* Partition: own complete-linkage code (distance 1-|r|; ties within 1e-10 broken by the lexicographically smallest sorted union; left child = child with the smaller minimum index; top-down cut at B visiting left child first; next-fit packing in leaf order). Verified equal to scipy `linkage(method="complete")` merge heights on random data (E1c). For the design with exact ties (population Sigma) this is the only place where the tie rule matters; blocks are listed in packing order, each sorted.
* Start mode: block tables for all U subset C_b, |U| <= K; per-block per-size maxima; max-plus convolution; size chosen by strict improvement from size 0 up (ties keep the smaller size); all optimal choices are enumerated (cap 20000) with absolute tie tolerance 1e-12 and the lexicographically smallest sorted union is returned (production uses exact double equality and a 1e6 cap). log Z_0 by log-sum-exp convolution of block size profiles.
* Local search: exactly the M 6.10 / LS0 reading in the spec: centre is scored; each scan scores all feasible adds (only if |S| < K), deletes and swaps; move to the neighbour with the largest F if it strictly exceeds F(centre), exact-equal ties by smallest sorted tuple; after ell moves one further scan; `local_limit` if that scan still improves; `certified` if a scan has no strict improvement. `S0 scored` means S0 is in the set of centres + all scanned neighbours of LS0 (tables/other stages are not part of this set). `HPM=S0` is the HPM (largest F, then smallest size, then lexicographic) of **LS0's scored set only**.
* ell = ceil(log2(n+p+1)). K = min(p, floor(n/2)).
* Population objects: Lambda_T = (n-1) theta'[Sigma - Sigma_.T Sigma_TT^-1 Sigma_T.] theta (exact-Gram designs: identical to ||(I-P_T) X theta||^2, E1e). Block minimiser U*_b: smallest size, then lexicographic, within **absolute tolerance 1e-7** of the minimum of Lambda_U over U subset C_b (main reading; with this tolerance any block member with delta^2 > 1e-7 enters, which is why S* is large for S2/S5). A second, "noise-level" reading (tolerance sigma^2 log n) is reported as `*_noise` / `S*noise` in E6 and in the S2/S5 route rows. S* in the per-run route tables is computed from the **actual (data) blocks** and the population Sigma. VIS margin = min over (b,U), U*_b not subset of U, of g_{b,U}/(v_U log n) with g = Lambda_U - Lambda_{U u U*_b}, v_U = sigma^2 + Lambda_U/(n-1); NL leakage = max over l in C_b\U*_b, U*_b subset T subset C_b\{l} of delta^2_{T,l}/(sigma^2 log n) (only the block-wise family L(S*); NL_avg(kappa)/E_{T,l} of T22(iii) was not computed). SEP zeta = max over S subset V, l not in V of Lambda_S - Lambda_{S+l}; ratio zeta/(n theta_min^2) with theta_min = min over truths of |theta| (n-1 vs n differences are immaterial). Lemma-3 decrement = min over S subset V not containing all truths of max over missing truths j of (Lambda_S - Lambda_{S+j}); reported as dec/log n. **SEP and decrement are exhaustive over all S subset V when |V| <= 20 (E6 small scale, E4(i), E5, E6b r = 0) and otherwise use a restricted family** (all S with |S \ S0| <= 2, all |S| <= 3, 3000 random subsets): for LH (|V| = 27 or 45) and E4(ii) (|V| = 12, exhaustive) / E6b (|V| = 55, 90) the reported zeta is a lower bound on the true maximum and the decrement an upper bound on the true minimum.
* Designs. Exact Gram: X = sqrt(n-1) Q chol(Sigma)' with Q from QR of a centred Gaussian matrix (fixed per (design, n)), then 20 noise seeds, y = X theta + eps (sigma = 1), centred/scaled to squared norm n-1. iid rows: rows ~ N(0, Sigma), columns centred/scaled; LH-iid follows model G (y^r = X^r beta + eps on the *raw* rows, then standardise), E6/E5 follow `gen_dev_data.R` (X standardised first, y = c X beta + eps). LH: groups of 9, hub = first member, linked pairs = groups (1,2), (3,4) [c = 2], visible group = next one, theta_hub_a = 1, theta_hub_b = -psi, visible = 1. 'p = 400' in E3 was run as p = 396 (44 groups of 9). Study generator ported verbatim from `gen_dev_data.R` (S6: rho_i = 0.4 + 0.1((group_i - 1) mod 6), matrix(rho,p,p) recycled column-major => row-wise); small scale p = 100, s0 = 4, step 5 (active 0-based 2, 26, 53, 75; beta 1.4,-1.0,1.8,-1.2; c scales beta); real size p = 500, s0 = 14, step 7.
* V in the route statistics: LH: union of the signal groups (27 or 45 variables); E4(i): {x1,x2,x3}; E4(ii): groups A and B (12); E6/E5: union of the signal groups (20); E7: {x1} u proxies. "Path in V" = every LS0 centre on the path is a subset of V (scanned neighbours may leave V). 'Centre sweep' (E2, E3, E4(ii)): LS (production ell) from {} , up to 30 singletons of V, S*, S0, every S0 minus one element, S0 plus one random element of V (5), and 10 (E2), 6 (E3), 40 (E4(ii)) random subsets of V of size 2..8 -- about 47-61 centres per run; counts are pooled over seeds. E4(i): all 8 subsets of {x1,x2,x3}.
* "Non-progress move" (E4(i)): a move after which |S symmetric-difference S0| does not decrease; adding x3 to a subset of {x1,x2} is non-progress, and so is its first-move classification "first = add x3".
* E4(i): x3 = a(x1+x2)/sqrt(2(1+r12)) + sqrt(1-a^2) z with a = 0.85, run for r12 in {0, 0.3}, theta1 = theta2 = 1, 60 independent nulls (p = 63, exact Gram). E4(ii): p = 60, ten groups of six (rho = 0.7); group A contains hub a (index 0, theta = 1); group B (indices 6-11) contains two masked truths (6, 7; theta = -psi = -0.4), two proxies (8, 9) and two other members; Sigma[A,B] = Sigma[A,a] * (psi Sigma_BB w)', w = e_6 + e_7 (so A independent of B given a), which makes Cov(x_B, mu) = 0 exactly (checked: 5.6e-17) and keeps B < 2g (B = 7, g = 6). psi = 0.4 (not the LH 0.2) so that the masked effect is not below the noise at n = 200. E4(iii): all coefficients (hubs and visible) = n^{-1/4}, sigma = 1, on the E2 design (so the masked hub has psi n^{-1/4}).
* E7: x1 at index 0, proxies = indices 1..d (corr 0.6 with x1, 0.36 mutually), exact Gram; the 'extra' E7b run (p = 160, d = 80, n in {800, 3200}, 5 seeds, B = 12) is beyond the spec; a first attempt with p = 300, d = 200 (B = 16) was aborted as too slow (uncapped LS0 with >100 moves) and is not reported.
* Seeds: noise seeds 0..19 per row; the same seed index gives the same noise vector in rows with the same (design, n) (e.g. E4(i) r12 = 0 and 0.3 share noise, so single-seed events repeat).
"""

E1 = """
## 2. Results

### E1 -- unit tests (E1_results.json, E1_output.txt)

| test | result |
|---|---|
| (a) batched Cholesky score vs an independent n x n Gaussian-integral implementation (differences vs the empty model), 300 models | max abs difference %.2e |
| (b) DP start mode vs brute force over all |S| <= K (p <= 12): 50 random cases (16 with random user-supplied partitions) | mode equal in %d/%d; max abs diff of log Z_0 and of log pi_0(S) = %.2e |
| (b') start-mode tie rule: 10 cases with an exactly duplicated column (exact ties) | %d/%d equal to brute force (tie tolerance 1e-9 in the brute force) |
| (c) own complete linkage vs scipy: sorted merge heights, 20 random cases; partition invariants (cover, block size <= B) | max difference %.1e; invariants hold %d/20 |
| (d) production local search vs an independent naive implementation (path, scored set, certified/local_limit), 15 cases | identical in %d/15 |
| (e) population Lambda vs ||(I-P_T) X theta||^2 on exact-Gram LH designs (90 subsets) | max abs diff %.1e |
| (e') VIS margin and NL leakage helpers vs brute-force enumeration (tiny LH, p = 12); SEP zeta and Lemma-3 decrement sweep vs brute force | differences %.1e, %.1e; %.1e, %.1e |

All E1 tests pass.
""" % (e1["a_score_max_abs_diff"], e1["b_dp_vs_bruteforce_random"]["mode_matches"], e1["b_dp_vs_bruteforce_random"]["cases"],
       e1["b_dp_vs_bruteforce_random"]["max_abs_diff_logZ_or_logpi"], e1["b_dp_vs_bruteforce_ties"]["mode_matches"], e1["b_dp_vs_bruteforce_ties"]["cases"],
       e1["c_linkage_max_height_diff_vs_scipy"], e1["c_partition_invariants_ok"], e1["d_ls_vs_naive"], e1["e_pop_lambda_max_abs_diff"],
       e1["e_vis_diff"], e1["e_nl_diff"], e1["e_sep_diff"], e1["e_dec_diff"])

COLS = """
Column key (route tables): `blocks=groups` actual partition equals the design groups; `start=S*` LS0 centre (start mode) equals the population reference S* (union of block minimisers from Sigma on the actual blocks); `|start|`, `|S*|` ranges; `path in V` all LS0 centres inside V; `moves (max)` LS0 moves; `ell` cap; `S0 scored`, `certified` (scan without improvement), `HPM=S0` (over LS0's scored set); `max(1-pi0(S*))` maximum over runs; `sweep:` pooled over the centre family (inV = path inside V; S0 reached = S0 on the path; S0 scored; cert=S0 = returned S0 with `certified`; max tau = largest number of moves needed to reach S0).
"""

E2 = """
### E2 -- LH, exact Gram (g = 9, p = 108, v = 1 visible group, beta = 1, sigma^2 = 1)

""" + rd("E2_summary.md").split("\n", 2)[2] + """
Reading (facts only). Blocks equal the groups and S~_0 equals S* = S0 minus the masked hubs in 240/240 runs (|S*| = 2 for c = 1, 3 for c = 2; the sample S* from the population matches S0 \\ M in every row). LS0 from the start mode makes at most 3 moves, always ends `certified` (never `local_limit`), and the path stays in V in 238/240 runs (the two exceptions: rho = 0.7, psi = 0.5, n = 200, noise seed 12 -- after reaching S0 the search adds the null variable 57). Because S* misses the masked hubs, S0 is a neighbour of S* for c = 1 and two additions away for c = 2: S0 is scored in 20/20 (c = 1) and 6/20 (c = 2, rho = 0.4, psi = 0.2) at n = 200, in all runs for n >= 800; S0 is the HPM of LS0's scored set in 37/80, 78/80, 80/80 runs at n = 200, 800, 3200 (mainly the rho = 0.4, psi = 0.2 rows, HPM = S0 in 1/20 and 1/20 runs, where the masked hub has n theta^2 = 8 against log n = 5.3; the (0.7, 0.5) rows have 17-18/20). Population: NL leakage = 0, SEP zeta = 0 (restricted family; computed values are exactly 0 or <= 1e-13), VIS margin 2.3-8.7 at n = 200 and 24-91 at n = 3200, Lemma-3 decrement 1.0-3.1 log n (n = 200), 3.1-9.8 log n (n = 800), 10-32 log n (n = 3200). Centre sweep at n = 3200: every one of the 940/1060 centres per row stays in V, reaches S0, scores S0 and returns S0 certified, with tau <= 9 <= ell = 12; at n = 800 all but the rho = 0.4, c = 2 row pass (971/1060 reach, 954/1060 certified at S0); at n = 200 the sweep reaches S0 from only 161-172 of 940-1060 centres for (0.4, 0.2) (the masked hub is not added) and from 890-965 for (0.7, 0.5).
"""

E3 = """
### E3 -- LH-iid (iid N(0, Sigma_LH) rows; p = 108 and p = 396)

""" + rd("E3_summary.md").split("\n", 2)[2] + """
Reading. Blocks equal the groups in 480/480 runs (also at n = 200 with p = 396, where B = 14). S~_0 = S*: p = 108: 78/80, 79/80, 80/80; p = 396: 73/80, 79/80, 80/80 at n = 200, 800, 3200 (the exceptions lack an S* element or contain one additional element); LS0 always ends certified, with at most 3 moves. At n = 3200 all flags (start = S*, path in V, S0 scored, certified, final = S0, HPM = S0) hold in 160/160 runs, and every sweep centre in every row passes (860/860, 980/980). At n = 800 the sweep fails in the rows with the weak masked coefficients (e.g. p = 108, rho = 0.4, c = 1: 645/860 certified at S0, 816/860 inside V). HPM = S0 in 40/80, 67/80, 80/80 (p = 108) and 33/80, 69/80, 80/80 (p = 396). 1-pi_0(S*): see EXTRA_stats.md (median 0.27/0.14/0.07 for p = 108).
"""

E4 = """
### E4 -- adversarial designs inside the class

""" + rd("E4_summary.md").split("\n", 2)[2] + """
Reading. (i) In the combination look-alike, the three variables x1, x2, x3 always fall in one block; S* = S0 = {x1,x2}; the start mode is S0 in 38-40/40 runs per n (the two exceptions are the same noise seed 0 at n = 800 for r12 = 0 and 0.3: the start mode contains one extra null). From the centre {} the first move is "add x3" -- a non-progress move -- in 20/20 runs for every n when r12 = 0 and in 18/20, 20/20, 20/20 when r12 = 0.3; the path reaches S0 in 19/20 (n = 200, r12 = 0: the trap of section 0 item 5), 20/20, 20/20 runs (r12 = 0.3: 20/20 each) in at most 4 moves (ell >= 9); the path stays in V = {x1,x2,x3} in 20/20, 19/20, 20/20 runs (the n = 800 exception is noise seed 0, where the search adds a null after S0). From the other subsets of V the first move is never "add x3" (0/20 in every row); for all centres the path stays in V in 19/20 runs at n = 800 (noise seed 0) and 20/20 at n = 200 and 3200. (ii) Masked-suppressor cluster: blocks = groups and S~_0 = S* = {a} in 60/60 runs; LS0 makes at most 2 moves; S0 is scored in 59/60 runs and is the HPM in 6/20, 20/20, 20/20 runs (n = 200, 800, 3200); the sweep passes in all 1227 centres at n = 800 and 3200 and reaches S0 from 606/1227 centres at n = 200. Population: Cov(x_B, mu) = 5.6e-17, S* = {a}, NL = 0, SEP = 0, VIS margin 2.10 / 6.68 / 22.1. (iii) Shrinking signals: S~_0 = S* in 6/80, 29/80, 71/80 runs; certified 80/80, path in V 80/80, but LS0 reaches S0 only rarely (S0 scored in 5/80, 17/80, 44/80; HPM = S0 in 0/80, 0/80, 4/80); n theta_min^2 is 0.57-3.5 (n = 200), 1.1-7.1 (800) and 2.3-14 (3200) against log n = 5.3, 6.7, 8.1.
"""

E5 = """
### E5 -- outside the class: S5 (compound symmetry, between-group 0.3, within-group 0.7), p = 100, s0 = 4, c = 1

""" + rd("E5_summary.md").split("\n", 2)[2] + """
Reading. The population reference (tolerance 1e-7) is all 100 variables; groups are not the blocks (B = 10 = 2g). The start mode is S~_0 != S* in all 120 runs; its size grows with n: 2-7 (iid) / 2-4 (exact) at n = 200, 10-16 / 6-12 at n = 800, 22-25 / 23-25 at n = 3200 (S0 has 4 elements); |start \\ S0| is 0-4 / 0-1, 7-12 / 2-8, 18-21 / 19-21 (iid / exact, n = 200 / 800 / 3200). LS0 moves needed (uncapped, ell = 1000): 0-4, 7-12, 18-21 (iid) and 1-3, 2-9, 19-21 (exact) at n = 200, 800, 3200, after which the uncapped search ends at S0 in 19/20, 20/20, 20/20 (iid) and 18/20, 19/20, 20/20 (exact) runs (the other ends are S0 plus one null variable). With the production cap, S0 is scored in 20/20, 18/20, 0/20 (iid) and 20/20, 20/20, 0/20 (exact) runs at n = 200, 800, 3200; local_limit is reached in 0/20, 5/20, 20/20 (iid) and 0/20, 0/20, 20/20 (exact) runs.
"""

E6 = """
### E6 -- study generator S1-S6 (scale p = 100: 20 groups of 5, s0 = 4, step 5; iid rows; c in {1, 0.5})

""" + rd("E6_summary.md").split("\n", 2)[2] + """
Reading. Population (p = 100, V = 4 signal groups; V exhaustive): S1, S3, S4, S6 have S* = S0 exactly (both tolerance readings), NL = 0 (<= 4.5e-13), SEP zeta = 0, positive and increasing VIS margins (smallest: S4, c = 0.5: 0.65 at n = 200, 6.8 at n = 3200); Lemma-3 decrements are 1.2-37.6 log n (n = 200) and larger with n. S2 (AR(1)) and S5 (compound symmetry) violate the checks as in section 0 (S2: |S*| = 18, SEP ratio 0.36, VIS 1e-8 with the canonical tolerance; S5: |S*| = 100, SEP ratio 0.31, VIS 0.0009-0.015). Route statistics (iid rows): for S1, S3, S4, S6 the start mode equals S* (= S0) in 15-32 of 40 runs at n = 200 (S1 32, S3 31, S4 22, S6 15), 39-40 of 40 at n = 800 and 38-40 of 40 at n = 3200 (pooled over c), the LS0 path stays in V in >= 36/40 runs, S0 is scored in 40/40, HPM = S0 in 34-40/40 (S1: 38, 40, 40; S3: 34, 34, 40; S4: 40, 38, 40; S6: 36, 40, 38 at n = 200, 800, 3200); LS0 uses at most 3 moves. For S2: S0 scored in 120/120 runs, HPM = S0 in 118/120, start mode = S0 in 8-10/20 (n = 200), 2-3/20 (n = 800) and 0/20 (n = 3200) with |start \\ S0| up to 7 (6 for c = 0.5) and up to 7 LS0 moves. S5 as in E5 (c = 1 and 0.5; at c = 0.5 and n = 3200 S0 is scored in 2/20 runs). Real study size (population only, p = 500, s0 = 14, step 7, n = 200, B = 14, blocks = pairs of groups): S1, S3, S4, S6 have S* = S0 (|S*| = 14) in both tolerance readings, NL ~ 0; but the VIS margin is only 0.94 / 0.84 (S1, c = 1 / 0.5), 0.35 / 0.31 (S3), 0.18 / 0.16 (S4), 0.24 / 0.21 (S6) at n = 200 (the minimum over blocks and sub-models; the weakest (b, U) is always in the block of truth 144, the coefficient-0.8 truth, with U = {} for S1 and U = the other four members of its group for S3, S4, S6), i.e. below 1; S2: |S*| = 66 / 63 (21 / 19 with noise tolerance), VIS 1e-9 to 2e-9; S5: |S*| = 482 (130 / 63 noise tolerance), VIS 9e-4.
"""

E6B = "\n" + rd("E6b_summary.md")

E7T = """
### E7 -- proxy flood

""" + rd(e7).split("\n", 2)[2] + """
Reading. In every row the start mode contains x1 (20/20) and no null outside the proxy set; the proxies occupy 3 blocks (d = 20) or 5 blocks (d = 40). The number of non-S0 elements in the start mode is 3-5, 6-8, 11 for d = 20 and 8-14, 19-25, 30-31 for d = 40 at n = 200, 800, 3200, versus ell = 9, 10, 12; the number of uncapped LS0 moves needed to reach S0 is about |start \\ S0| (tau = 3-5, 6-8 (one run never reaches S0), 11 for d = 20; 8-15, 20-25, 30-32 for d = 40). With the production cap, S0 is scored in 20/20, 20/20, 20/20 runs for d = 20 and in 10/20, 0/20, 0/20 for d = 40 (n = 200, 800, 3200); local_limit occurs in 0 runs for d = 20 and in 18/20, 20/20, 20/20 runs for d = 40. At d = 40, n = 200 the outcome depends on the realisation (|start \\ S0| from 8 to 14 against ell = 9). E7b (d = 80, p = 160, B = 12, 5 seeds): |start \\ S0| = 39-46 (n = 800, ell = 10) and 67-69 (n = 3200, ell = 12), LS0 uses all ell moves (local_limit 5/5) and never scores S0 (0/5), the uncapped search reaches S0 in 5/5 runs after 39-46 / 67-69 moves.
"""

TAIL = """
## 3. Notes on isolated events (seeds) mentioned above

* E2, rho = 0.7, psi = 0.5, n = 200, seed 12 (c = 1 and c = 2): after reaching S0 (via the masked hub) the search adds the null variable 57 (a chance correlation with the noise); the same noise realisation produces the event in both c rows.
* E4(i), n = 800, seed 0 (r12 = 0 and 0.3 share the noise vector): the start mode (and the path from {} ) ends one null variable (index 5) above S0; F(final) - F(S0) = +2.28.
* E4(i), n = 200, seed 15, r12 = 0: LS from {} and {x3} certified at {x3}, F(S0) - F({x3}) = +25.6 (section 0 item 5).

## 4. Not done / limitations

* NL_avg(kappa) and E_{T,l} of T22(iii) were not computed (only the block-wise leakage max delta^2/(sigma^2 log n)).
* SEP and Lemma-3 decrement for the LH designs (|V| = 27, 45) are search-based bounds (restricted family), not exhaustive.
* The real study size (p = 500) was checked at the population level only (VIS, NL, S*), as specified; no SEP there (|V| = 70).
* The start-mode tie tolerance (1e-12) and the S* tolerances (1e-7, sigma^2 log n) are numerical choices, see section 1.
* Run times: E2 ~ 25 s, E3 ~ 105 s, E4 ~ 30 s, E5 ~ 60 s, E6 ~ 100 s, E7 main ~ 1-2 min, E7b ~ 1.5 min.
"""

open("SUMMARY.md", "w").write(TOP + E1 + COLS + E2 + E3 + E4 + E5 + E6 + E6B + E7T + TAIL)
print("SUMMARY.md written", len(TOP + E1 + COLS + E2 + E3 + E4 + E5 + E6 + E6B + E7T + TAIL))
