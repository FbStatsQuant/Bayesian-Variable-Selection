# W1-GEN numerics -- SUMMARY

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

## 2. Results

### E1 -- unit tests (E1_results.json, E1_output.txt)

| test | result |
|---|---|
| (a) batched Cholesky score vs an independent n x n Gaussian-integral implementation (differences vs the empty model), 300 models | max abs difference 8.53e-14 |
| (b) DP start mode vs brute force over all |S| <= K (p <= 12): 50 random cases (16 with random user-supplied partitions) | mode equal in 50/50; max abs diff of log Z_0 and of log pi_0(S) = 1.42e-14 |
| (b') start-mode tie rule: 10 cases with an exactly duplicated column (exact ties) | 10/10 equal to brute force (tie tolerance 1e-9 in the brute force) |
| (c) own complete linkage vs scipy: sorted merge heights, 20 random cases; partition invariants (cover, block size <= B) | max difference 0.0e+00; invariants hold 20/20 |
| (d) production local search vs an independent naive implementation (path, scored set, certified/local_limit), 15 cases | identical in 15/15 |
| (e) population Lambda vs ||(I-P_T) X theta||^2 on exact-Gram LH designs (90 subsets) | max abs diff 1.1e-13 |
| (e') VIS margin and NL leakage helpers vs brute-force enumeration (tiny LH, p = 12); SEP zeta and Lemma-3 decrement sweep vs brute force | differences 0.0e+00, 0.0e+00; 0.0e+00, 2.3e-14 |

All E1 tests pass.

Column key (route tables): `blocks=groups` actual partition equals the design groups; `start=S*` LS0 centre (start mode) equals the population reference S* (union of block minimisers from Sigma on the actual blocks); `|start|`, `|S*|` ranges; `path in V` all LS0 centres inside V; `moves (max)` LS0 moves; `ell` cap; `S0 scored`, `certified` (scan without improvement), `HPM=S0` (over LS0's scored set); `max(1-pi0(S*))` maximum over runs; `sweep:` pooled over the centre family (inV = path inside V; S0 reached = S0 on the path; S0 scored; cert=S0 = returned S0 with `certified`; max tau = largest number of moves needed to reach S0).

### E2 -- LH, exact Gram (g = 9, p = 108, v = 1 visible group, beta = 1, sigma^2 = 1)

| rho | psi | c | n | N | blocks=groups | start=S* | |start| (min-max) | |S*| | path in V | moves (max) | ell | S0 scored | certified | HPM=S0 | max(1-pi0(S*)) | sweep: inV | sweep: S0 reached | sweep: S0 scored | sweep: cert=S0 | sweep: max tau |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.4 | 0.2 | 1 | 200 | 20 | 20/20 | 20/20 | 2-2 | 2-2 | 20/20 | 1 | 9 | 20/20 | 20/20 | 1/20 | 1.56e-01 | 940/940 | 172/940 | 940/940 | 47/940 | 7 |
| 0.4 | 0.2 | 1 | 800 | 20 | 20/20 | 20/20 | 2-2 | 2-2 | 20/20 | 1 | 10 | 20/20 | 20/20 | 20/20 | 7.36e-02 | 940/940 | 940/940 | 940/940 | 940/940 | 8 |
| 0.4 | 0.2 | 1 | 3200 | 20 | 20/20 | 20/20 | 2-2 | 2-2 | 20/20 | 1 | 12 | 20/20 | 20/20 | 20/20 | 3.74e-02 | 940/940 | 940/940 | 940/940 | 940/940 | 8 |
| 0.4 | 0.2 | 2 | 200 | 20 | 20/20 | 20/20 | 3-3 | 3-3 | 20/20 | 2 | 9 | 6/20 | 20/20 | 1/20 | 1.70e-01 | 1060/1060 | 161/1060 | 495/1060 | 53/1060 | 8 |
| 0.4 | 0.2 | 2 | 800 | 20 | 20/20 | 20/20 | 3-3 | 3-3 | 20/20 | 2 | 10 | 20/20 | 20/20 | 18/20 | 8.40e-02 | 1060/1060 | 971/1060 | 1060/1060 | 954/1060 | 9 |
| 0.4 | 0.2 | 2 | 3200 | 20 | 20/20 | 20/20 | 3-3 | 3-3 | 20/20 | 2 | 12 | 20/20 | 20/20 | 20/20 | 4.51e-02 | 1060/1060 | 1060/1060 | 1060/1060 | 1060/1060 | 8 |
| 0.7 | 0.5 | 1 | 200 | 20 | 20/20 | 20/20 | 2-2 | 2-2 | 19/20 | 2 | 9 | 20/20 | 20/20 | 18/20 | 1.62e-01 | 893/940 | 890/940 | 940/940 | 846/940 | 8 |
| 0.7 | 0.5 | 1 | 800 | 20 | 20/20 | 20/20 | 2-2 | 2-2 | 20/20 | 1 | 10 | 20/20 | 20/20 | 20/20 | 8.02e-02 | 940/940 | 940/940 | 940/940 | 940/940 | 8 |
| 0.7 | 0.5 | 1 | 3200 | 20 | 20/20 | 20/20 | 2-2 | 2-2 | 20/20 | 1 | 12 | 20/20 | 20/20 | 20/20 | 4.19e-02 | 940/940 | 940/940 | 940/940 | 940/940 | 8 |
| 0.7 | 0.5 | 2 | 200 | 20 | 20/20 | 20/20 | 3-3 | 3-3 | 19/20 | 3 | 9 | 20/20 | 20/20 | 17/20 | 1.85e-01 | 1007/1060 | 965/1060 | 1060/1060 | 901/1060 | 8 |
| 0.7 | 0.5 | 2 | 800 | 20 | 20/20 | 20/20 | 3-3 | 3-3 | 20/20 | 2 | 10 | 20/20 | 20/20 | 20/20 | 8.80e-02 | 1060/1060 | 1060/1060 | 1060/1060 | 1060/1060 | 9 |
| 0.7 | 0.5 | 2 | 3200 | 20 | 20/20 | 20/20 | 3-3 | 3-3 | 20/20 | 2 | 12 | 20/20 | 20/20 | 20/20 | 4.85e-02 | 1060/1060 | 1060/1060 | 1060/1060 | 1060/1060 | 9 |

### population checks (blocks = groups)

| rho | psi | c | n | Sstar_eq_ref | VIS_margin | NL_leak | zeta | zeta_ratio | dec | dec_over_logn | sep_exhaustive |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.4 | 0.2 | 1 | 200 | True | 8.66 | 0 | 0 | 0 | 5.19 | 0.98 | False |
| 0.4 | 0.2 | 1 | 800 | True | 27.6 | 0 | 0 | 0 | 20.8 | 3.12 | False |
| 0.4 | 0.2 | 1 | 3200 | True | 91.4 | 0 | 0 | 0 | 83.5 | 10.3 | False |
| 0.4 | 0.2 | 2 | 200 | True | 6.36 | 0 | 0 | 0 | 5.48 | 1.03 | False |
| 0.4 | 0.2 | 2 | 800 | True | 20.2 | 0 | 0 | 0 | 22 | 3.29 | False |
| 0.4 | 0.2 | 2 | 3200 | True | 67.1 | 0 | 0 | 0 | 88.1 | 10.9 | False |
| 0.7 | 0.5 | 1 | 200 | True | 2.98 | 0 | 0 | 0 | 15.2 | 2.87 | False |
| 0.7 | 0.5 | 1 | 800 | True | 9.5 | 0 | 0 | 0 | 61.1 | 9.13 | False |
| 0.7 | 0.5 | 1 | 3200 | True | 31.5 | 0 | 0 | 0 | 244 | 30.3 | False |
| 0.7 | 0.5 | 2 | 200 | True | 2.27 | 0 | 0 | 0 | 16.3 | 3.08 | False |
| 0.7 | 0.5 | 2 | 800 | True | 7.22 | 0 | 0 | 0 | 65.4 | 9.79 | False |
| 0.7 | 0.5 | 2 | 3200 | True | 23.9 | 0 | 0 | 0 | 262 | 32.5 | False |

Reading (facts only). Blocks equal the groups and S~_0 equals S* = S0 minus the masked hubs in 240/240 runs (|S*| = 2 for c = 1, 3 for c = 2; the sample S* from the population matches S0 \ M in every row). LS0 from the start mode makes at most 3 moves, always ends `certified` (never `local_limit`), and the path stays in V in 238/240 runs (the two exceptions: rho = 0.7, psi = 0.5, n = 200, noise seed 12 -- after reaching S0 the search adds the null variable 57). Because S* misses the masked hubs, S0 is a neighbour of S* for c = 1 and two additions away for c = 2: S0 is scored in 20/20 (c = 1) and 6/20 (c = 2, rho = 0.4, psi = 0.2) at n = 200, in all runs for n >= 800; S0 is the HPM of LS0's scored set in 37/80, 78/80, 80/80 runs at n = 200, 800, 3200 (mainly the rho = 0.4, psi = 0.2 rows, HPM = S0 in 1/20 and 1/20 runs, where the masked hub has n theta^2 = 8 against log n = 5.3; the (0.7, 0.5) rows have 17-18/20). Population: NL leakage = 0, SEP zeta = 0 (restricted family; computed values are exactly 0 or <= 1e-13), VIS margin 2.3-8.7 at n = 200 and 24-91 at n = 3200, Lemma-3 decrement 1.0-3.1 log n (n = 200), 3.1-9.8 log n (n = 800), 10-32 log n (n = 3200). Centre sweep at n = 3200: every one of the 940/1060 centres per row stays in V, reaches S0, scores S0 and returns S0 certified, with tau <= 9 <= ell = 12; at n = 800 all but the rho = 0.4, c = 2 row pass (971/1060 reach, 954/1060 certified at S0); at n = 200 the sweep reaches S0 from only 161-172 of 940-1060 centres for (0.4, 0.2) (the masked hub is not added) and from 890-965 for (0.7, 0.5).

### E3 -- LH-iid (iid N(0, Sigma_LH) rows; p = 108 and p = 396)

| p | rho | psi | c | n | N | blocks=groups | start=S* | |start| (min-max) | |S*| | path in V | moves (max) | ell | S0 scored | certified | HPM=S0 | max(1-pi0(S*)) | sweep: inV | sweep: S0 reached | sweep: S0 scored | sweep: cert=S0 | sweep: max tau |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 108 | 0.4 | 0.2 | 1 | 200 | 20 | 20/20 | 20/20 | 2-2 | 2-2 | 20/20 | 1 | 9 | 20/20 | 20/20 | 4/20 | 4.62e-01 | 859/860 | 281/860 | 860/860 | 172/860 | 8 |
| 108 | 0.4 | 0.2 | 1 | 800 | 20 | 20/20 | 19/20 | 2-3 | 2-2 | 18/20 | 2 | 10 | 20/20 | 20/20 | 15/20 | 5.93e-01 | 816/860 | 706/860 | 860/860 | 645/860 | 8 |
| 108 | 0.4 | 0.2 | 1 | 3200 | 20 | 20/20 | 20/20 | 2-2 | 2-2 | 20/20 | 1 | 12 | 20/20 | 20/20 | 20/20 | 1.66e-01 | 860/860 | 860/860 | 860/860 | 860/860 | 8 |
| 108 | 0.4 | 0.2 | 2 | 200 | 20 | 20/20 | 20/20 | 3-3 | 3-3 | 20/20 | 1 | 9 | 7/20 | 20/20 | 0/20 | 6.37e-01 | 980/980 | 118/980 | 500/980 | 0/980 | 7 |
| 108 | 0.4 | 0.2 | 2 | 800 | 20 | 20/20 | 20/20 | 3-3 | 3-3 | 18/20 | 3 | 10 | 19/20 | 20/20 | 14/20 | 3.87e-01 | 882/980 | 756/980 | 944/980 | 686/980 | 8 |
| 108 | 0.4 | 0.2 | 2 | 3200 | 20 | 20/20 | 20/20 | 3-3 | 3-3 | 20/20 | 2 | 12 | 20/20 | 20/20 | 20/20 | 3.91e-01 | 980/980 | 980/980 | 980/980 | 980/980 | 8 |
| 108 | 0.7 | 0.5 | 1 | 200 | 20 | 20/20 | 20/20 | 2-2 | 2-2 | 20/20 | 1 | 9 | 20/20 | 20/20 | 18/20 | 4.98e-01 | 860/860 | 791/860 | 860/860 | 774/860 | 8 |
| 108 | 0.7 | 0.5 | 1 | 800 | 20 | 20/20 | 20/20 | 2-2 | 2-2 | 19/20 | 2 | 10 | 20/20 | 20/20 | 19/20 | 5.59e-01 | 817/860 | 850/860 | 860/860 | 817/860 | 8 |
| 108 | 0.7 | 0.5 | 1 | 3200 | 20 | 20/20 | 20/20 | 2-2 | 2-2 | 20/20 | 1 | 12 | 20/20 | 20/20 | 20/20 | 1.00e-01 | 860/860 | 860/860 | 860/860 | 860/860 | 8 |
| 108 | 0.7 | 0.5 | 2 | 200 | 20 | 20/20 | 18/20 | 3-3 | 3-3 | 20/20 | 3 | 9 | 20/20 | 20/20 | 18/20 | 8.28e-01 | 980/980 | 936/980 | 980/980 | 882/980 | 8 |
| 108 | 0.7 | 0.5 | 2 | 800 | 20 | 20/20 | 20/20 | 3-3 | 3-3 | 19/20 | 3 | 10 | 20/20 | 20/20 | 19/20 | 6.61e-01 | 931/980 | 972/980 | 980/980 | 931/980 | 8 |
| 108 | 0.7 | 0.5 | 2 | 3200 | 20 | 20/20 | 20/20 | 3-3 | 3-3 | 20/20 | 2 | 12 | 20/20 | 20/20 | 20/20 | 1.87e-01 | 980/980 | 980/980 | 980/980 | 980/980 | 8 |
| 396 | 0.4 | 0.2 | 1 | 200 | 20 | 20/20 | 19/20 | 2-3 | 2-2 | 19/20 | 1 | 10 | 20/20 | 20/20 | 1/20 | 9.50e-01 | 856/860 | 169/860 | 860/860 | 43/860 | 8 |
| 396 | 0.4 | 0.2 | 1 | 800 | 20 | 20/20 | 19/20 | 2-3 | 2-2 | 19/20 | 1 | 11 | 20/20 | 20/20 | 16/20 | 6.71e-01 | 860/860 | 719/860 | 860/860 | 688/860 | 8 |
| 396 | 0.4 | 0.2 | 1 | 3200 | 20 | 20/20 | 20/20 | 2-2 | 2-2 | 20/20 | 1 | 12 | 20/20 | 20/20 | 20/20 | 1.71e-01 | 860/860 | 860/860 | 860/860 | 860/860 | 8 |
| 396 | 0.4 | 0.2 | 2 | 200 | 20 | 20/20 | 19/20 | 3-4 | 3-3 | 19/20 | 2 | 10 | 3/20 | 20/20 | 1/20 | 9.32e-01 | 977/980 | 158/980 | 353/980 | 49/980 | 7 |
| 396 | 0.4 | 0.2 | 2 | 800 | 20 | 20/20 | 20/20 | 3-3 | 3-3 | 20/20 | 2 | 11 | 20/20 | 20/20 | 13/20 | 4.47e-01 | 980/980 | 687/980 | 980/980 | 637/980 | 8 |
| 396 | 0.4 | 0.2 | 2 | 3200 | 20 | 20/20 | 20/20 | 3-3 | 3-3 | 20/20 | 2 | 12 | 20/20 | 20/20 | 20/20 | 2.38e-01 | 980/980 | 980/980 | 980/980 | 980/980 | 8 |
| 396 | 0.7 | 0.5 | 1 | 200 | 20 | 20/20 | 19/20 | 2-3 | 2-2 | 19/20 | 1 | 10 | 20/20 | 20/20 | 17/20 | 9.01e-01 | 858/860 | 752/860 | 860/860 | 731/860 | 8 |
| 396 | 0.7 | 0.5 | 1 | 800 | 20 | 20/20 | 20/20 | 2-2 | 2-2 | 20/20 | 1 | 11 | 20/20 | 20/20 | 20/20 | 5.05e-01 | 860/860 | 860/860 | 860/860 | 860/860 | 8 |
| 396 | 0.7 | 0.5 | 1 | 3200 | 20 | 20/20 | 20/20 | 2-2 | 2-2 | 20/20 | 1 | 12 | 20/20 | 20/20 | 20/20 | 3.02e-01 | 860/860 | 860/860 | 860/860 | 860/860 | 8 |
| 396 | 0.7 | 0.5 | 2 | 200 | 20 | 20/20 | 16/20 | 2-3 | 3-3 | 19/20 | 3 | 10 | 20/20 | 20/20 | 14/20 | 9.27e-01 | 930/980 | 806/980 | 980/980 | 686/980 | 8 |
| 396 | 0.7 | 0.5 | 2 | 800 | 20 | 20/20 | 20/20 | 3-3 | 3-3 | 20/20 | 2 | 11 | 20/20 | 20/20 | 20/20 | 6.57e-01 | 980/980 | 980/980 | 980/980 | 980/980 | 8 |
| 396 | 0.7 | 0.5 | 2 | 3200 | 20 | 20/20 | 20/20 | 3-3 | 3-3 | 20/20 | 2 | 12 | 20/20 | 20/20 | 20/20 | 1.93e-01 | 980/980 | 980/980 | 980/980 | 980/980 | 8 |

Reading. Blocks equal the groups in 480/480 runs (also at n = 200 with p = 396, where B = 14). S~_0 = S*: p = 108: 78/80, 79/80, 80/80; p = 396: 73/80, 79/80, 80/80 at n = 200, 800, 3200 (the exceptions lack an S* element or contain one additional element); LS0 always ends certified, with at most 3 moves. At n = 3200 all flags (start = S*, path in V, S0 scored, certified, final = S0, HPM = S0) hold in 160/160 runs, and every sweep centre in every row passes (860/860, 980/980). At n = 800 the sweep fails in the rows with the weak masked coefficients (e.g. p = 108, rho = 0.4, c = 1: 645/860 certified at S0, 816/860 inside V). HPM = S0 in 40/80, 67/80, 80/80 (p = 108) and 33/80, 69/80, 80/80 (p = 396). 1-pi_0(S*): see EXTRA_stats.md (median 0.27/0.14/0.07 for p = 108).

### E4 -- adversarial designs inside the class

Route from the LS0 start mode:

| r12 | n | N | x1x2x3 same block | start=S* | |start| (min-max) | path in V | moves (max) | ell | S0 scored | certified | HPM=S0 | max(1-pi0(S*)) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.0 | 200 | 20 | 20/20 | 20/20 | 2-2 | 20/20 | 0 | 9 | 20/20 | 20/20 | 20/20 | 1.59e-01 |
| 0.0 | 800 | 20 | 20/20 | 19/20 | 2-3 | 19/20 | 0 | 10 | 20/20 | 20/20 | 19/20 | 9.16e-01 |
| 0.0 | 3200 | 20 | 20/20 | 20/20 | 2-2 | 20/20 | 0 | 12 | 20/20 | 20/20 | 20/20 | 5.29e-02 |
| 0.3 | 200 | 20 | 20/20 | 20/20 | 2-2 | 20/20 | 0 | 9 | 20/20 | 20/20 | 20/20 | 1.55e-01 |
| 0.3 | 800 | 20 | 20/20 | 19/20 | 2-3 | 19/20 | 0 | 10 | 20/20 | 20/20 | 19/20 | 9.15e-01 |
| 0.3 | 3200 | 20 | 20/20 | 20/20 | 2-2 | 20/20 | 0 | 12 | 20/20 | 20/20 | 20/20 | 5.15e-02 |

Population:

| r12 | n | Sstar | VIS | NL | zeta | dec | dec_over_logn | corr_x3_x1 |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 200 | [0, 1] | 11.375 | 0.0 | 0.0 | 23.991 | 4.528 | 0.601 |
| 0.0 | 800 | [0, 1] | 36.201 | 0.0 | 0.0 | 96.326 | 14.41 | 0.601 |
| 0.0 | 3200 | [0, 1] | 120.044 | 0.0 | 0.0 | 385.664 | 47.784 | 0.601 |
| 0.3 | 200 | [0, 1] | 12.115 | 0.0 | 0.0 | 48.83 | 9.216 | 0.685 |
| 0.3 | 800 | [0, 1] | 38.554 | 0.0 | 0.0 | 196.054 | 29.329 | 0.685 |
| 0.3 | 3200 | [0, 1] | 127.847 | 0.0 | 0.0 | 784.953 | 97.257 | 0.685 |

Local search from every centre C subset V={x1,x2,x3} (per-centre counts over 20 seeds):

| r12 | n | centre(0=x1,1=x2,2=x3) | first move exists | first=add x3 | first non-progress | path in V | reaches S0 | S0 scored | cert=S0 | max moves |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.0 | 200 | [] | 20/20 | 20/20 | 20/20 | 20/20 | 19/20 | 19/20 | 19/20 | 3 |
| 0.0 | 200 | [0] | 20/20 | 0/20 | 0/20 | 20/20 | 20/20 | 20/20 | 20/20 | 1 |
| 0.0 | 200 | [1] | 20/20 | 0/20 | 0/20 | 20/20 | 20/20 | 20/20 | 20/20 | 1 |
| 0.0 | 200 | [2] | 19/20 | 0/20 | 0/19 | 20/20 | 19/20 | 19/20 | 19/20 | 2 |
| 0.0 | 200 | [0, 1] | 0/20 | 0/20 | 0/0 | 20/20 | 20/20 | 20/20 | 20/20 | 0 |
| 0.0 | 200 | [0, 2] | 20/20 | 0/20 | 0/20 | 20/20 | 20/20 | 20/20 | 20/20 | 1 |
| 0.0 | 200 | [1, 2] | 20/20 | 0/20 | 0/20 | 20/20 | 20/20 | 20/20 | 20/20 | 1 |
| 0.0 | 200 | [0, 1, 2] | 20/20 | 0/20 | 0/20 | 20/20 | 20/20 | 20/20 | 20/20 | 1 |
| 0.0 | 800 | [] | 20/20 | 20/20 | 20/20 | 19/20 | 20/20 | 20/20 | 19/20 | 4 |
| 0.0 | 800 | [0] | 20/20 | 0/20 | 0/20 | 19/20 | 20/20 | 20/20 | 19/20 | 2 |
| 0.0 | 800 | [1] | 20/20 | 0/20 | 0/20 | 19/20 | 20/20 | 20/20 | 19/20 | 2 |
| 0.0 | 800 | [2] | 20/20 | 0/20 | 0/20 | 19/20 | 20/20 | 20/20 | 19/20 | 3 |
| 0.0 | 800 | [0, 1] | 1/20 | 0/20 | 1/1 | 19/20 | 20/20 | 20/20 | 19/20 | 1 |
| 0.0 | 800 | [0, 2] | 20/20 | 0/20 | 0/20 | 19/20 | 20/20 | 20/20 | 19/20 | 2 |
| 0.0 | 800 | [1, 2] | 20/20 | 0/20 | 0/20 | 19/20 | 20/20 | 20/20 | 19/20 | 2 |
| 0.0 | 800 | [0, 1, 2] | 20/20 | 0/20 | 1/20 | 19/20 | 19/20 | 20/20 | 19/20 | 1 |
| 0.0 | 3200 | [] | 20/20 | 20/20 | 20/20 | 20/20 | 20/20 | 20/20 | 20/20 | 3 |
| 0.0 | 3200 | [0] | 20/20 | 0/20 | 0/20 | 20/20 | 20/20 | 20/20 | 20/20 | 1 |
| 0.0 | 3200 | [1] | 20/20 | 0/20 | 0/20 | 20/20 | 20/20 | 20/20 | 20/20 | 1 |
| 0.0 | 3200 | [2] | 20/20 | 0/20 | 0/20 | 20/20 | 20/20 | 20/20 | 20/20 | 2 |
| 0.0 | 3200 | [0, 1] | 0/20 | 0/20 | 0/0 | 20/20 | 20/20 | 20/20 | 20/20 | 0 |
| 0.0 | 3200 | [0, 2] | 20/20 | 0/20 | 0/20 | 20/20 | 20/20 | 20/20 | 20/20 | 1 |
| 0.0 | 3200 | [1, 2] | 20/20 | 0/20 | 0/20 | 20/20 | 20/20 | 20/20 | 20/20 | 1 |
| 0.0 | 3200 | [0, 1, 2] | 20/20 | 0/20 | 0/20 | 20/20 | 20/20 | 20/20 | 20/20 | 1 |
| 0.3 | 200 | [] | 20/20 | 18/20 | 18/20 | 20/20 | 20/20 | 20/20 | 20/20 | 3 |
| 0.3 | 200 | [0] | 20/20 | 0/20 | 0/20 | 20/20 | 20/20 | 20/20 | 20/20 | 1 |
| 0.3 | 200 | [1] | 20/20 | 0/20 | 0/20 | 20/20 | 20/20 | 20/20 | 20/20 | 1 |
| 0.3 | 200 | [2] | 20/20 | 0/20 | 0/20 | 20/20 | 20/20 | 20/20 | 20/20 | 2 |
| 0.3 | 200 | [0, 1] | 0/20 | 0/20 | 0/0 | 20/20 | 20/20 | 20/20 | 20/20 | 0 |
| 0.3 | 200 | [0, 2] | 20/20 | 0/20 | 0/20 | 20/20 | 20/20 | 20/20 | 20/20 | 1 |
| 0.3 | 200 | [1, 2] | 20/20 | 0/20 | 0/20 | 20/20 | 20/20 | 20/20 | 20/20 | 1 |
| 0.3 | 200 | [0, 1, 2] | 20/20 | 0/20 | 0/20 | 20/20 | 20/20 | 20/20 | 20/20 | 1 |
| 0.3 | 800 | [] | 20/20 | 20/20 | 20/20 | 19/20 | 20/20 | 20/20 | 19/20 | 4 |
| 0.3 | 800 | [0] | 20/20 | 0/20 | 0/20 | 19/20 | 20/20 | 20/20 | 19/20 | 2 |
| 0.3 | 800 | [1] | 20/20 | 0/20 | 0/20 | 19/20 | 20/20 | 20/20 | 19/20 | 2 |
| 0.3 | 800 | [2] | 20/20 | 0/20 | 0/20 | 19/20 | 20/20 | 20/20 | 19/20 | 3 |
| 0.3 | 800 | [0, 1] | 1/20 | 0/20 | 1/1 | 19/20 | 20/20 | 20/20 | 19/20 | 1 |
| 0.3 | 800 | [0, 2] | 20/20 | 0/20 | 0/20 | 19/20 | 20/20 | 20/20 | 19/20 | 2 |
| 0.3 | 800 | [1, 2] | 20/20 | 0/20 | 0/20 | 19/20 | 20/20 | 20/20 | 19/20 | 2 |
| 0.3 | 800 | [0, 1, 2] | 20/20 | 0/20 | 1/20 | 19/20 | 19/20 | 20/20 | 19/20 | 1 |
| 0.3 | 3200 | [] | 20/20 | 20/20 | 20/20 | 20/20 | 20/20 | 20/20 | 20/20 | 3 |
| 0.3 | 3200 | [0] | 20/20 | 0/20 | 0/20 | 20/20 | 20/20 | 20/20 | 20/20 | 1 |
| 0.3 | 3200 | [1] | 20/20 | 0/20 | 0/20 | 20/20 | 20/20 | 20/20 | 20/20 | 1 |
| 0.3 | 3200 | [2] | 20/20 | 0/20 | 0/20 | 20/20 | 20/20 | 20/20 | 20/20 | 2 |
| 0.3 | 3200 | [0, 1] | 0/20 | 0/20 | 0/0 | 20/20 | 20/20 | 20/20 | 20/20 | 0 |
| 0.3 | 3200 | [0, 2] | 20/20 | 0/20 | 0/20 | 20/20 | 20/20 | 20/20 | 20/20 | 1 |
| 0.3 | 3200 | [1, 2] | 20/20 | 0/20 | 0/20 | 20/20 | 20/20 | 20/20 | 20/20 | 1 |
| 0.3 | 3200 | [0, 1, 2] | 20/20 | 0/20 | 0/20 | 20/20 | 20/20 | 20/20 | 20/20 | 1 |

## E4(ii) masked-suppressor cluster (p=60, g=6, rho=.7, psi=.4); 20 seeds. a=idx0; masked truths m1,m2=idx 6,7; proxies idx 8,9

| n | N | blocks=groups | start=S* | |start| (min-max) | |S*| | path in V | moves (max) | ell | S0 scored | certified | HPM=S0 | max(1-pi0(S*)) | sweep: inV | sweep: S0 reached | sweep: S0 scored | sweep: cert=S0 | sweep: max tau |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 200 | 20 | 20/20 | 20/20 | 1-1 | 1-1 | 20/20 | 2 | 9 | 19/20 | 20/20 | 6/20 | 2.97e-01 | 1193/1227 | 606/1227 | 1197/1227 | 368/1227 | 8 |
| 800 | 20 | 20/20 | 20/20 | 1-1 | 1-1 | 20/20 | 2 | 10 | 20/20 | 20/20 | 20/20 | 1.10e-01 | 1227/1227 | 1227/1227 | 1227/1227 | 1227/1227 | 8 |
| 3200 | 20 | 20/20 | 20/20 | 1-1 | 1-1 | 20/20 | 2 | 12 | 20/20 | 20/20 | 20/20 | 5.46e-02 | 1227/1227 | 1227/1227 | 1227/1227 | 1227/1227 | 8 |

Population:

| n | Sstar | VIS | NL | zeta | dec | max_abs_cov_B_mu | lam_min_Sigma |
|---|---|---|---|---|---|---|---|
| 200 | [0] | 2.099 | 0.0 | 0.0 | 10.058 | 5.551115123125783e-17 | 0.1915 |
| 800 | [0] | 6.679 | 0.0 | 0.0 | 40.383 | 5.551115123125783e-17 | 0.1915 |
| 3200 | [0] | 22.149 | 0.0 | 0.0 | 161.683 | 5.551115123125783e-17 | 0.1915 |

## E4(iii) shrinking signals theta=n^-1/4 in the E2 design; 20 seeds

| rho | psi | c | n | N | blocks=groups | start=S* | |start| (min-max) | |S*| | path in V | moves (max) | ell | S0 scored | certified | HPM=S0 | max(1-pi0(S*)) | sweep: inV | sweep: S0 reached | sweep: S0 scored | sweep: cert=S0 | sweep: max tau |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.4 | 0.2 | 1 | 200 | 20 | 20/20 | 2/20 | 0-2 | 2-2 | 20/20 | 1 | 9 | 3/20 | 20/20 | 0/20 | 1.00e+00 | 940/940 | 75/940 | 342/940 | 0/940 | 6 |
| 0.4 | 0.2 | 1 | 800 | 20 | 20/20 | 13/20 | 0-2 | 2-2 | 20/20 | 1 | 10 | 14/20 | 20/20 | 0/20 | 9.98e-01 | 940/940 | 104/940 | 729/940 | 0/940 | 6 |
| 0.4 | 0.2 | 1 | 3200 | 20 | 20/20 | 20/20 | 2-2 | 2-2 | 20/20 | 0 | 12 | 20/20 | 20/20 | 0/20 | 1.99e-01 | 940/940 | 113/940 | 940/940 | 0/940 | 7 |
| 0.4 | 0.2 | 2 | 200 | 20 | 20/20 | 1/20 | 0-3 | 3-3 | 20/20 | 1 | 9 | 0/20 | 20/20 | 0/20 | 1.00e+00 | 1060/1060 | 56/1060 | 223/1060 | 0/1060 | 1 |
| 0.4 | 0.2 | 2 | 800 | 20 | 20/20 | 12/20 | 0-3 | 3-3 | 20/20 | 1 | 10 | 0/20 | 20/20 | 0/20 | 9.99e-01 | 1060/1060 | 72/1060 | 239/1060 | 0/1060 | 1 |
| 0.4 | 0.2 | 2 | 3200 | 20 | 20/20 | 20/20 | 3-3 | 3-3 | 20/20 | 0 | 12 | 0/20 | 20/20 | 0/20 | 3.54e-01 | 1060/1060 | 85/1060 | 246/1060 | 0/1060 | 4 |
| 0.7 | 0.5 | 1 | 200 | 20 | 20/20 | 2/20 | 0-2 | 2-2 | 20/20 | 0 | 9 | 2/20 | 20/20 | 0/20 | 1.00e+00 | 925/940 | 89/940 | 274/940 | 0/940 | 6 |
| 0.7 | 0.5 | 1 | 800 | 20 | 20/20 | 3/20 | 0-2 | 2-2 | 20/20 | 0 | 10 | 3/20 | 20/20 | 0/20 | 1.00e+00 | 940/940 | 133/940 | 344/940 | 12/940 | 6 |
| 0.7 | 0.5 | 1 | 3200 | 20 | 20/20 | 17/20 | 1-2 | 2-2 | 20/20 | 1 | 12 | 17/20 | 20/20 | 4/20 | 9.21e-01 | 940/940 | 302/940 | 844/940 | 201/940 | 8 |
| 0.7 | 0.5 | 2 | 200 | 20 | 20/20 | 1/20 | 0-3 | 3-3 | 20/20 | 1 | 9 | 0/20 | 20/20 | 0/20 | 1.00e+00 | 1040/1060 | 77/1060 | 221/1060 | 0/1060 | 1 |
| 0.7 | 0.5 | 2 | 800 | 20 | 20/20 | 1/20 | 0-3 | 3-3 | 20/20 | 1 | 10 | 0/20 | 20/20 | 0/20 | 1.00e+00 | 1060/1060 | 113/1060 | 233/1060 | 0/1060 | 6 |
| 0.7 | 0.5 | 2 | 3200 | 20 | 20/20 | 14/20 | 2-3 | 3-3 | 20/20 | 1 | 12 | 7/20 | 20/20 | 0/20 | 9.85e-01 | 1060/1060 | 126/1060 | 541/1060 | 0/1060 | 6 |

Population (blocks = groups):

| rho | psi | c | n | Sstar_eq_ref | VIS_margin | NL_leak | zeta | dec | dec_over_logn | n_theta2 | logn |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.4 | 0.2 | 1 | 200 | True | 1.45 | 0 | 0 | 0.367 | 0.0693 | 0.566 | 5.3 |
| 0.4 | 0.2 | 1 | 800 | True | 2.44 | 0 | 0 | 0.737 | 0.11 | 1.13 | 6.68 |
| 0.4 | 0.2 | 1 | 3200 | True | 4.16 | 0 | 0 | 1.48 | 0.183 | 2.26 | 8.07 |
| 0.4 | 0.2 | 2 | 200 | True | 1.37 | 0 | 0 | 0.388 | 0.0732 | 0.566 | 5.3 |
| 0.4 | 0.2 | 2 | 800 | True | 2.36 | 0 | 0 | 0.778 | 0.116 | 1.13 | 6.68 |
| 0.4 | 0.2 | 2 | 3200 | True | 4.09 | 0 | 0 | 1.56 | 0.193 | 2.26 | 8.07 |
| 0.7 | 0.5 | 1 | 200 | True | 0.457 | 0 | 0 | 1.08 | 0.203 | 3.54 | 5.3 |
| 0.7 | 0.5 | 1 | 800 | True | 0.761 | 0 | 0 | 2.16 | 0.323 | 7.07 | 6.68 |
| 0.7 | 0.5 | 1 | 3200 | True | 1.29 | 0 | 0 | 4.32 | 0.535 | 14.1 | 8.07 |
| 0.7 | 0.5 | 2 | 200 | True | 0.436 | 0 | 0 | 1.15 | 0.218 | 3.54 | 5.3 |
| 0.7 | 0.5 | 2 | 800 | True | 0.742 | 0 | 0 | 2.31 | 0.346 | 7.07 | 6.68 |
| 0.7 | 0.5 | 2 | 3200 | True | 1.27 | 0 | 0 | 4.63 | 0.574 | 14.1 | 8.07 |

Reading. (i) In the combination look-alike, the three variables x1, x2, x3 always fall in one block; S* = S0 = {x1,x2}; the start mode is S0 in 38-40/40 runs per n (the two exceptions are the same noise seed 0 at n = 800 for r12 = 0 and 0.3: the start mode contains one extra null). From the centre {} the first move is "add x3" -- a non-progress move -- in 20/20 runs for every n when r12 = 0 and in 18/20, 20/20, 20/20 when r12 = 0.3; the path reaches S0 in 19/20 (n = 200, r12 = 0: the trap of section 0 item 5), 20/20, 20/20 runs (r12 = 0.3: 20/20 each) in at most 4 moves (ell >= 9); the path stays in V = {x1,x2,x3} in 20/20, 19/20, 20/20 runs (the n = 800 exception is noise seed 0, where the search adds a null after S0). From the other subsets of V the first move is never "add x3" (0/20 in every row); for all centres the path stays in V in 19/20 runs at n = 800 (noise seed 0) and 20/20 at n = 200 and 3200. (ii) Masked-suppressor cluster: blocks = groups and S~_0 = S* = {a} in 60/60 runs; LS0 makes at most 2 moves; S0 is scored in 59/60 runs and is the HPM in 6/20, 20/20, 20/20 runs (n = 200, 800, 3200); the sweep passes in all 1227 centres at n = 800 and 3200 and reaches S0 from 606/1227 centres at n = 200. Population: Cov(x_B, mu) = 5.6e-17, S* = {a}, NL = 0, SEP = 0, VIS margin 2.10 / 6.68 / 22.1. (iii) Shrinking signals: S~_0 = S* in 6/80, 29/80, 71/80 runs; certified 80/80, path in V 80/80, but LS0 reaches S0 only rarely (S0 scored in 5/80, 17/80, 44/80; HPM = S0 in 0/80, 0/80, 4/80); n theta_min^2 is 0.57-3.5 (n = 200), 1.1-7.1 (800) and 2.3-14 (3200) against log n = 5.3, 6.7, 8.1.

### E5 -- outside the class: S5 (compound symmetry, between-group 0.3, within-group 0.7), p = 100, s0 = 4, c = 1

Population (unit scale): SEP zeta/(n theta_min^2) = 0.310 (= zeta_unit/theta_min^2, n-free), Lemma-3 decrement unit = 0.3652 (exhaustive over S subset V=20 variables: True)

| design | n | N | blocks=groups | start=S* | |start| (min-max) | |start\S0| (min-max) | path in V | ell | moves (min-max) | local_limit | S0 scored | certified | HPM=S0 | uncapped: moves (min-max) | uncapped: reach S0 | uncapped: S0 scored | uncapped: final=S0 | uncapped final |.\S0| (min-max) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| iid | 200 | 20 | 0/20 | 0/20 | 2-7 | 0-4 | 13/20 | 9 | 0-4 | 0/20 | 20/20 | 20/20 | 19/20 | 0-4 | 20/20 | 20/20 | 19/20 | 0-1 |
| iid | 800 | 20 | 0/20 | 0/20 | 10-16 | 7-12 | 0/20 | 10 | 7-10 | 5/20 | 18/20 | 15/20 | 18/20 | 7-12 | 20/20 | 20/20 | 20/20 | 0-0 |
| iid | 3200 | 20 | 0/20 | 0/20 | 22-25 | 18-21 | 0/20 | 12 | 12-12 | 20/20 | 0/20 | 0/20 | 0/20 | 18-21 | 20/20 | 20/20 | 20/20 | 0-0 |
| exact | 200 | 20 | 0/20 | 0/20 | 2-4 | 0-1 | 17/20 | 9 | 1-3 | 0/20 | 20/20 | 20/20 | 18/20 | 1-3 | 20/20 | 20/20 | 18/20 | 0-1 |
| exact | 800 | 20 | 0/20 | 0/20 | 6-12 | 2-8 | 0/20 | 10 | 2-9 | 0/20 | 20/20 | 20/20 | 19/20 | 2-9 | 19/20 | 20/20 | 19/20 | 0-1 |
| exact | 3200 | 20 | 0/20 | 0/20 | 23-25 | 19-21 | 0/20 | 12 | 12-12 | 20/20 | 0/20 | 0/20 | 0/20 | 19-21 | 20/20 | 20/20 | 20/20 | 0-0 |

Reading. The population reference (tolerance 1e-7) is all 100 variables; groups are not the blocks (B = 10 = 2g). The start mode is S~_0 != S* in all 120 runs; its size grows with n: 2-7 (iid) / 2-4 (exact) at n = 200, 10-16 / 6-12 at n = 800, 22-25 / 23-25 at n = 3200 (S0 has 4 elements); |start \ S0| is 0-4 / 0-1, 7-12 / 2-8, 18-21 / 19-21 (iid / exact, n = 200 / 800 / 3200). LS0 moves needed (uncapped, ell = 1000): 0-4, 7-12, 18-21 (iid) and 1-3, 2-9, 19-21 (exact) at n = 200, 800, 3200, after which the uncapped search ends at S0 in 19/20, 20/20, 20/20 (iid) and 18/20, 19/20, 20/20 (exact) runs (the other ends are S0 plus one null variable). With the production cap, S0 is scored in 20/20, 18/20, 0/20 (iid) and 20/20, 20/20, 0/20 (exact) runs at n = 200, 800, 3200; local_limit is reached in 0/20, 5/20, 20/20 (iid) and 0/20, 0/20, 20/20 (exact) runs.

### E6 -- study generator S1-S6 (scale p = 100: 20 groups of 5, s0 = 4, step 5; iid rows; c in {1, 0.5})

### population checks (blocks from the population correlation matrix with B=min(floor sqrt n, floor sqrt p, 16)=10; V = union of the 4 signal groups)

| scen | c | n | B | J | blocks_eq_groups | Sstar_size | Sstar_eq_S0 | Sstar_missing | Sstar_extra | Sstar_noise_size | Sstar_noise_eq_S0 | blocks_with_2plus_truths | VIS_margin | NL_leak | VIS_noise | NL_noise | zeta | zeta_over_n_th2 | dec_over_logn | sep_exhaustive |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1.0 | 200 | 10 | 10 | False | 4 | True | [] | 0 | 4 | True | 0 | 4.35 | 0 | 4.35 | 0 | 0 | 0 | 37.6 | True |
| 1 | 1.0 | 800 | 10 | 10 | False | 4 | True | [] | 0 | 4 | True | 0 | 13.8 | 0 | 13.8 | 0 | 0 | 0 | 120 | True |
| 1 | 1.0 | 3200 | 10 | 10 | False | 4 | True | [] | 0 | 4 | True | 0 | 45.9 | 0 | 45.9 | 0 | 0 | 0 | 396 | True |
| 1 | 0.5 | 200 | 10 | 10 | False | 4 | True | [] | 0 | 4 | True | 0 | 3.23 | 0 | 3.23 | 0 | 0 | 0 | 9.39 | True |
| 1 | 0.5 | 800 | 10 | 10 | False | 4 | True | [] | 0 | 4 | True | 0 | 10.3 | 0 | 10.3 | 0 | 0 | 0 | 29.9 | True |
| 1 | 0.5 | 3200 | 10 | 10 | False | 4 | True | [] | 0 | 4 | True | 0 | 34.1 | 0 | 34.1 | 0 | 0 | 0 | 99.1 | True |
| 2 | 1.0 | 200 | 10 | 13 | False | 18 | False | [] | 14 | 5 | False | 0 | 1.21e-08 | 4.36e-10 | 0.165 | 0.587 | 71.6 | 0.358 | 22.5 | True |
| 2 | 1.0 | 800 | 10 | 13 | False | 18 | False | [] | 14 | 6 | False | 0 | 3.87e-08 | 1.39e-09 | 0.162 | 0.672 | 288 | 0.36 | 71.7 | True |
| 2 | 1.0 | 3200 | 10 | 13 | False | 18 | False | [] | 14 | 7 | False | 0 | 1.28e-07 | 4.6e-09 | 0.194 | 0.557 | 1.15e+03 | 0.36 | 238 | True |
| 2 | 0.5 | 200 | 10 | 13 | False | 18 | False | [] | 14 | 4 | True | 0 | 9.02e-09 | 1.09e-10 | 2 | 0.475 | 17.9 | 0.358 | 5.63 | True |
| 2 | 0.5 | 800 | 10 | 13 | False | 18 | False | [] | 14 | 5 | False | 0 | 2.87e-08 | 3.47e-10 | 0.39 | 0.467 | 71.9 | 0.36 | 17.9 | True |
| 2 | 0.5 | 3200 | 10 | 13 | False | 18 | False | [] | 14 | 6 | False | 0 | 9.51e-08 | 1.15e-09 | 0.399 | 0.557 | 288 | 0.36 | 59.5 | True |
| 3 | 1.0 | 200 | 10 | 10 | False | 4 | True | [] | 0 | 4 | True | 0 | 1.72 | 4.29e-14 | 1.72 | 4.29e-14 | 0 | 0 | 13.8 | True |
| 3 | 1.0 | 800 | 10 | 10 | False | 4 | True | [] | 0 | 4 | True | 0 | 5.49 | 6.8e-14 | 5.49 | 6.8e-14 | 0 | 0 | 44 | True |
| 3 | 1.0 | 3200 | 10 | 10 | False | 4 | True | [] | 0 | 4 | True | 0 | 18.2 | 4.51e-13 | 18.2 | 4.51e-13 | 0 | 0 | 146 | True |
| 3 | 0.5 | 200 | 10 | 10 | False | 4 | True | [] | 0 | 4 | True | 0 | 1.25 | 1.07e-14 | 1.25 | 1.07e-14 | 0 | 0 | 3.45 | True |
| 3 | 0.5 | 800 | 10 | 10 | False | 4 | True | [] | 0 | 4 | True | 0 | 3.99 | 1.7e-14 | 3.99 | 1.7e-14 | 0 | 0 | 11 | True |
| 3 | 0.5 | 3200 | 10 | 10 | False | 4 | True | [] | 0 | 4 | True | 0 | 13.2 | 1.13e-13 | 13.2 | 1.13e-13 | 0 | 0 | 36.4 | True |
| 4 | 1.0 | 200 | 10 | 10 | False | 4 | True | [] | 0 | 4 | True | 0 | 0.892 | 6.44e-14 | 0.892 | 6.44e-14 | 0 | 0 | 6.98 | True |
| 4 | 1.0 | 800 | 10 | 10 | False | 4 | True | [] | 0 | 4 | True | 0 | 2.84 | 2.04e-13 | 2.84 | 2.04e-13 | 0 | 0 | 22.2 | True |
| 4 | 1.0 | 3200 | 10 | 10 | False | 4 | True | [] | 0 | 4 | True | 0 | 9.42 | 6.76e-13 | 9.42 | 6.76e-13 | 0 | 0 | 73.7 | True |
| 4 | 0.5 | 200 | 10 | 10 | False | 4 | True | [] | 0 | 4 | True | 0 | 0.645 | 1.61e-14 | 0.645 | 1.61e-14 | 0 | 0 | 1.75 | True |
| 4 | 0.5 | 800 | 10 | 10 | False | 4 | True | [] | 0 | 4 | True | 0 | 2.05 | 5.1e-14 | 2.05 | 5.1e-14 | 0 | 0 | 5.56 | True |
| 4 | 0.5 | 3200 | 10 | 10 | False | 4 | True | [] | 0 | 4 | True | 0 | 6.81 | 1.69e-13 | 6.81 | 1.69e-13 | 0 | 0 | 18.4 | True |
| 5 | 1.0 | 200 | 10 | 10 | False | 100 | False | [] | 96 | 34 | False | 0 | 0.00141 | 0 | 0.00678 | 0.341 | 61.7 | 0.309 | 13.7 | True |
| 5 | 1.0 | 800 | 10 | 10 | False | 100 | False | [] | 96 | 61 | False | 0 | 0.00449 | 0 | 0.00449 | 0.679 | 248 | 0.31 | 43.7 | True |
| 5 | 1.0 | 3200 | 10 | 10 | False | 100 | False | [] | 96 | 80 | False | 0 | 0.0149 | 0 | 0.0149 | 0.474 | 992 | 0.31 | 145 | True |
| 5 | 0.5 | 200 | 10 | 10 | False | 100 | False | [] | 96 | 14 | False | 0 | 0.000882 | 0 | 0.00465 | 0.455 | 15.4 | 0.309 | 3.43 | True |
| 5 | 0.5 | 800 | 10 | 10 | False | 100 | False | [] | 96 | 27 | False | 0 | 0.00281 | 0 | 0.0125 | 0.403 | 62 | 0.31 | 10.9 | True |
| 5 | 0.5 | 3200 | 10 | 10 | False | 100 | False | [] | 96 | 53 | False | 0 | 0.00931 | 0 | 0.00931 | 0.563 | 248 | 0.31 | 36.2 | True |
| 6 | 1.0 | 200 | 10 | 10 | False | 4 | True | [] | 0 | 4 | True | 0 | 0.601 | 4.29e-14 | 0.601 | 4.29e-14 | 0 | 0 | 4.67 | True |
| 6 | 1.0 | 800 | 10 | 10 | False | 4 | True | [] | 0 | 4 | True | 0 | 1.91 | 6.8e-14 | 1.91 | 6.8e-14 | 0 | 0 | 14.9 | True |
| 6 | 1.0 | 3200 | 10 | 10 | False | 4 | True | [] | 0 | 4 | True | 0 | 6.35 | 4.51e-13 | 6.35 | 4.51e-13 | 0 | 0 | 49.3 | True |
| 6 | 0.5 | 200 | 10 | 10 | False | 4 | True | [] | 0 | 4 | True | 0 | 0.434 | 1.07e-14 | 0.434 | 1.07e-14 | 0 | 0 | 1.17 | True |
| 6 | 0.5 | 800 | 10 | 10 | False | 4 | True | [] | 0 | 4 | True | 0 | 1.38 | 1.7e-14 | 1.38 | 1.7e-14 | 0 | 0 | 3.72 | True |
| 6 | 0.5 | 3200 | 10 | 10 | False | 4 | True | [] | 0 | 4 | True | 0 | 4.58 | 1.13e-13 | 4.58 | 1.13e-13 | 0 | 0 | 12.3 | True |

### route statistics, iid rows, 20 seeds per row

| scen | c | n | N | blocks=groups | start=S* | start=S0 | final=S0 | |start| (min-max) | |S*| | start=S*noise | |S*noise| | |start\S0| max | |S0\start| max | path in V | moves (max) | moves med | ell | S0 scored | certified | HPM=S0 | max(1-pi0(S*)) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1.0 | 200 | 20 | 0/20 | 18/20 | 18/20 | 19/20 | 3-4 | 4-4 | 18/20 | 4-4 | 0 | 1 | 19/20 | 2 | 0 | 9 | 20/20 | 20/20 | 19/20 | 9.13e-01 |
| 1 | 1.0 | 800 | 20 | 0/20 | 19/20 | 19/20 | 20/20 | 4-5 | 4-4 | 19/20 | 4-4 | 1 | 0 | 20/20 | 1 | 0 | 10 | 20/20 | 20/20 | 20/20 | 7.57e-01 |
| 1 | 1.0 | 3200 | 20 | 0/20 | 20/20 | 20/20 | 20/20 | 4-4 | 4-4 | 20/20 | 4-4 | 0 | 0 | 20/20 | 0 | 0 | 12 | 20/20 | 20/20 | 20/20 | 2.07e-01 |
| 1 | 0.5 | 200 | 20 | 0/20 | 14/20 | 14/20 | 19/20 | 3-4 | 4-4 | 14/20 | 4-4 | 0 | 1 | 19/20 | 2 | 0 | 9 | 20/20 | 20/20 | 19/20 | 9.55e-01 |
| 1 | 0.5 | 800 | 20 | 0/20 | 20/20 | 20/20 | 20/20 | 4-4 | 4-4 | 20/20 | 4-4 | 0 | 0 | 20/20 | 0 | 0 | 10 | 20/20 | 20/20 | 20/20 | 4.91e-01 |
| 1 | 0.5 | 3200 | 20 | 0/20 | 20/20 | 20/20 | 20/20 | 4-4 | 4-4 | 20/20 | 4-4 | 0 | 0 | 20/20 | 0 | 0 | 12 | 20/20 | 20/20 | 20/20 | 5.19e-01 |
| 2 | 1.0 | 200 | 20 | 0/20 | 0/20 | 8/20 | 19/20 | 4-6 | 25-35 | 0/20 | 6-10 | 2 | 1 | 17/20 | 2 | 1 | 9 | 20/20 | 20/20 | 19/20 | 1.00e+00 |
| 2 | 1.0 | 800 | 20 | 0/20 | 0/20 | 2/20 | 20/20 | 4-11 | 20-29 | 2/20 | 6-9 | 7 | 0 | 12/20 | 7 | 2 | 10 | 20/20 | 20/20 | 20/20 | 1.00e+00 |
| 2 | 1.0 | 3200 | 20 | 0/20 | 0/20 | 0/20 | 20/20 | 5-10 | 20-29 | 1/20 | 8-11 | 6 | 0 | 7/20 | 6 | 3 | 12 | 20/20 | 20/20 | 20/20 | 1.00e+00 |
| 2 | 0.5 | 200 | 20 | 0/20 | 0/20 | 10/20 | 19/20 | 3-6 | 24-34 | 1/20 | 4-9 | 2 | 1 | 18/20 | 2 | 0 | 9 | 20/20 | 20/20 | 19/20 | 1.00e+00 |
| 2 | 0.5 | 800 | 20 | 0/20 | 0/20 | 3/20 | 20/20 | 4-10 | 19-27 | 2/20 | 6-9 | 6 | 0 | 13/20 | 6 | 1 | 10 | 20/20 | 20/20 | 20/20 | 1.00e+00 |
| 2 | 0.5 | 3200 | 20 | 0/20 | 0/20 | 0/20 | 20/20 | 5-9 | 20-28 | 4/20 | 7-10 | 5 | 0 | 7/20 | 5 | 3 | 12 | 20/20 | 20/20 | 20/20 | 1.00e+00 |
| 3 | 1.0 | 200 | 20 | 0/20 | 18/20 | 18/20 | 17/20 | 3-4 | 4-4 | 18/20 | 4-4 | 1 | 1 | 19/20 | 1 | 0 | 9 | 20/20 | 20/20 | 17/20 | 9.75e-01 |
| 3 | 1.0 | 800 | 20 | 0/20 | 20/20 | 20/20 | 17/20 | 4-4 | 4-4 | 20/20 | 4-4 | 0 | 0 | 18/20 | 1 | 0 | 10 | 20/20 | 20/20 | 17/20 | 5.20e-01 |
| 3 | 1.0 | 3200 | 20 | 0/20 | 20/20 | 20/20 | 20/20 | 4-4 | 4-4 | 20/20 | 4-4 | 0 | 0 | 20/20 | 0 | 0 | 12 | 20/20 | 20/20 | 20/20 | 2.87e-01 |
| 3 | 0.5 | 200 | 20 | 0/20 | 13/20 | 13/20 | 17/20 | 2-5 | 4-4 | 13/20 | 4-4 | 1 | 2 | 19/20 | 2 | 0 | 9 | 20/20 | 20/20 | 17/20 | 9.82e-01 |
| 3 | 0.5 | 800 | 20 | 0/20 | 20/20 | 20/20 | 17/20 | 4-4 | 4-4 | 20/20 | 4-4 | 0 | 0 | 18/20 | 1 | 0 | 10 | 20/20 | 20/20 | 17/20 | 7.08e-01 |
| 3 | 0.5 | 3200 | 20 | 0/20 | 20/20 | 20/20 | 20/20 | 4-4 | 4-4 | 20/20 | 4-4 | 0 | 0 | 20/20 | 0 | 0 | 12 | 20/20 | 20/20 | 20/20 | 2.92e-01 |
| 4 | 1.0 | 200 | 20 | 0/20 | 14/20 | 14/20 | 20/20 | 3-4 | 4-4 | 14/20 | 4-4 | 1 | 1 | 20/20 | 1 | 0 | 9 | 20/20 | 20/20 | 20/20 | 9.72e-01 |
| 4 | 1.0 | 800 | 20 | 0/20 | 20/20 | 20/20 | 19/20 | 4-4 | 4-4 | 20/20 | 4-4 | 0 | 0 | 19/20 | 1 | 0 | 10 | 20/20 | 20/20 | 19/20 | 3.18e-01 |
| 4 | 1.0 | 3200 | 20 | 0/20 | 19/20 | 19/20 | 20/20 | 4-5 | 4-4 | 19/20 | 4-4 | 1 | 0 | 20/20 | 1 | 0 | 12 | 20/20 | 20/20 | 20/20 | 7.86e-01 |
| 4 | 0.5 | 200 | 20 | 0/20 | 8/20 | 8/20 | 20/20 | 3-4 | 4-4 | 8/20 | 4-4 | 2 | 2 | 20/20 | 3 | 1 | 9 | 20/20 | 20/20 | 20/20 | 9.98e-01 |
| 4 | 0.5 | 800 | 20 | 0/20 | 20/20 | 20/20 | 19/20 | 4-4 | 4-4 | 20/20 | 4-4 | 0 | 0 | 19/20 | 1 | 0 | 10 | 20/20 | 20/20 | 19/20 | 3.91e-01 |
| 4 | 0.5 | 3200 | 20 | 0/20 | 19/20 | 19/20 | 20/20 | 4-5 | 4-4 | 19/20 | 4-4 | 1 | 0 | 20/20 | 1 | 0 | 12 | 20/20 | 20/20 | 20/20 | 7.74e-01 |
| 5 | 1.0 | 200 | 20 | 0/20 | 0/20 | 1/20 | 19/20 | 2-7 | 100-100 | 0/20 | 31-37 | 4 | 2 | 13/20 | 4 | 2 | 9 | 20/20 | 20/20 | 19/20 | 1.00e+00 |
| 5 | 1.0 | 800 | 20 | 0/20 | 0/20 | 0/20 | 15/20 | 10-16 | 100-100 | 0/20 | 55-63 | 12 | 1 | 0/20 | 10 | 9 | 10 | 18/20 | 15/20 | 18/20 | 1.00e+00 |
| 5 | 1.0 | 3200 | 20 | 0/20 | 0/20 | 0/20 | 0/20 | 22-25 | 100-100 | 0/20 | 72-82 | 21 | 0 | 0/20 | 12 | 12 | 12 | 0/20 | 0/20 | 0/20 | 1.00e+00 |
| 5 | 0.5 | 200 | 20 | 0/20 | 0/20 | 0/20 | 19/20 | 2-6 | 100-100 | 0/20 | 14-16 | 2 | 2 | 18/20 | 3 | 2 | 9 | 20/20 | 20/20 | 19/20 | 1.00e+00 |
| 5 | 0.5 | 800 | 20 | 0/20 | 0/20 | 0/20 | 20/20 | 4-14 | 100-100 | 0/20 | 23-28 | 10 | 2 | 0/20 | 10 | 6 | 10 | 20/20 | 20/20 | 20/20 | 1.00e+00 |
| 5 | 0.5 | 3200 | 20 | 0/20 | 0/20 | 0/20 | 0/20 | 17-23 | 100-100 | 0/20 | 49-56 | 19 | 0 | 0/20 | 12 | 12 | 12 | 2/20 | 0/20 | 2/20 | 1.00e+00 |
| 6 | 1.0 | 200 | 20 | 0/20 | 9/20 | 9/20 | 20/20 | 3-4 | 4-4 | 9/20 | 4-4 | 1 | 1 | 20/20 | 1 | 1 | 9 | 20/20 | 20/20 | 20/20 | 9.67e-01 |
| 6 | 1.0 | 800 | 20 | 0/20 | 20/20 | 20/20 | 20/20 | 4-4 | 4-4 | 20/20 | 4-4 | 0 | 0 | 20/20 | 0 | 0 | 10 | 20/20 | 20/20 | 20/20 | 4.35e-01 |
| 6 | 1.0 | 3200 | 20 | 0/20 | 20/20 | 20/20 | 19/20 | 4-4 | 4-4 | 20/20 | 4-4 | 0 | 0 | 19/20 | 1 | 0 | 12 | 20/20 | 20/20 | 19/20 | 1.79e-01 |
| 6 | 0.5 | 200 | 20 | 0/20 | 6/20 | 6/20 | 16/20 | 3-4 | 4-4 | 6/20 | 4-4 | 2 | 2 | 20/20 | 2 | 1 | 9 | 20/20 | 20/20 | 16/20 | 9.83e-01 |
| 6 | 0.5 | 800 | 20 | 0/20 | 20/20 | 20/20 | 20/20 | 4-4 | 4-4 | 20/20 | 4-4 | 0 | 0 | 20/20 | 0 | 0 | 10 | 20/20 | 20/20 | 20/20 | 7.04e-01 |
| 6 | 0.5 | 3200 | 20 | 0/20 | 20/20 | 20/20 | 19/20 | 4-4 | 4-4 | 20/20 | 4-4 | 0 | 0 | 19/20 | 1 | 0 | 12 | 20/20 | 20/20 | 19/20 | 2.42e-01 |

## E6 real study size (population only, Sigma only): p=500 (100 groups of 5), s0=14, step 7, n=200, B=14

| scen | c | n | p | s0 | B | J | blocks_eq_groups | Sstar_size | Sstar_eq_S0 | Sstar_missing | Sstar_extra | K | Sstar_noise_size | Sstar_noise_eq_S0 | VIS_noise | NL_noise | blocks_with_2plus_truths | VIS_margin | NL_leak | VIS_arg |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1.0 | 200 | 500 | 14 | 14 | 36 | False | 14 | True | 0 | 0 | 100 | 14 | True | 0.938 | 0 | 0 | 0.938 | 0 | (10, (), (144,)) |
| 1 | 0.5 | 200 | 500 | 14 | 14 | 36 | False | 14 | True | 0 | 0 | 100 | 14 | True | 0.839 | 0 | 0 | 0.839 | 0 | (10, (), (144,)) |
| 2 | 1.0 | 200 | 500 | 14 | 14 | 62 | False | 66 | False | 0 | 52 | 100 | 21 | False | 0.0687 | 0.475 | 0 | 1.02e-09 | 8.74e-09 | (28, (224, 230), (224, 231)) |
| 2 | 0.5 | 200 | 500 | 14 | 14 | 62 | False | 63 | False | 0 | 49 | 100 | 19 | False | 0.121 | 0.845 | 0 | 2.34e-09 | 1.71e-08 | (24, (193, 199), (192, 199)) |
| 3 | 1.0 | 200 | 500 | 14 | 14 | 50 | False | 14 | True | 0 | 0 | 100 | 14 | True | 0.35 | 0 | 0 | 0.35 | 0 | (14, (140, 141, 142, 143), (144,)) |
| 3 | 0.5 | 200 | 500 | 14 | 14 | 50 | False | 14 | True | 0 | 0 | 100 | 14 | True | 0.313 | 0 | 0 | 0.313 | 0 | (14, (140, 141, 142, 143), (144,)) |
| 4 | 1.0 | 200 | 500 | 14 | 14 | 50 | False | 14 | True | 0 | 0 | 100 | 14 | True | 0.178 | 1.72e-13 | 0 | 0.178 | 1.72e-13 | (14, (140, 141, 142, 143), (144,)) |
| 4 | 0.5 | 200 | 500 | 14 | 14 | 50 | False | 14 | True | 0 | 0 | 100 | 14 | True | 0.159 | 4.29e-14 | 0 | 0.159 | 4.29e-14 | (14, (140, 141, 142, 143), (144,)) |
| 5 | 1.0 | 200 | 500 | 14 | 14 | 50 | False | 482 | False | 0 | 468 | 100 | 130 | False | 0.000938 | 0.57 | 0 | 0.000938 | 0 | (0, (0, 1, 2, 3, 4, 5, 6, 7, 8), (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)) |
| 5 | 0.5 | 200 | 500 | 14 | 14 | 50 | False | 482 | False | 0 | 468 | 100 | 63 | False | 0.00132 | 0.455 | 0 | 0.000797 | 0 | (0, (0, 1, 2, 3, 4, 5, 6, 7, 8), (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)) |
| 6 | 1.0 | 200 | 500 | 14 | 14 | 50 | False | 14 | True | 0 | 0 | 100 | 14 | True | 0.236 | 1.72e-13 | 0 | 0.236 | 1.72e-13 | (14, (140, 141, 142, 143), (144,)) |
| 6 | 0.5 | 200 | 500 | 14 | 14 | 50 | False | 14 | True | 0 | 0 | 100 | 14 | True | 0.211 | 4.29e-14 | 0 | 0.211 | 4.29e-14 | (14, (140, 141, 142, 143), (144,)) |

Reading. Population (p = 100, V = 4 signal groups; V exhaustive): S1, S3, S4, S6 have S* = S0 exactly (both tolerance readings), NL = 0 (<= 4.5e-13), SEP zeta = 0, positive and increasing VIS margins (smallest: S4, c = 0.5: 0.65 at n = 200, 6.8 at n = 3200); Lemma-3 decrements are 1.2-37.6 log n (n = 200) and larger with n. S2 (AR(1)) and S5 (compound symmetry) violate the checks as in section 0 (S2: |S*| = 18, SEP ratio 0.36, VIS 1e-8 with the canonical tolerance; S5: |S*| = 100, SEP ratio 0.31, VIS 0.0009-0.015). Route statistics (iid rows): for S1, S3, S4, S6 the start mode equals S* (= S0) in 15-32 of 40 runs at n = 200 (S1 32, S3 31, S4 22, S6 15), 39-40 of 40 at n = 800 and 38-40 of 40 at n = 3200 (pooled over c), the LS0 path stays in V in >= 36/40 runs, S0 is scored in 40/40, HPM = S0 in 34-40/40 (S1: 38, 40, 40; S3: 34, 34, 40; S4: 40, 38, 40; S6: 36, 40, 38 at n = 200, 800, 3200); LS0 uses at most 3 moves. For S2: S0 scored in 120/120 runs, HPM = S0 in 118/120, start mode = S0 in 8-10/20 (n = 200), 2-3/20 (n = 800) and 0/20 (n = 3200) with |start \ S0| up to 7 (6 for c = 0.5) and up to 7 LS0 moves. S5 as in E5 (c = 1 and 0.5; at c = 0.5 and n = 3200 S0 is scored in 2/20 runs). Real study size (population only, p = 500, s0 = 14, step 7, n = 200, B = 14, blocks = pairs of groups): S1, S3, S4, S6 have S* = S0 (|S*| = 14) in both tolerance readings, NL ~ 0; but the VIS margin is only 0.94 / 0.84 (S1, c = 1 / 0.5), 0.35 / 0.31 (S3), 0.18 / 0.16 (S4), 0.24 / 0.21 (S6) at n = 200 (the minimum over blocks and sub-models; the weakest (b, U) is always in the block of truth 144, the coefficient-0.8 truth, with U = {} for S1 and U = the other four members of its group for S3, S4, S6), i.e. below 1; S2: |S*| = 66 / 63 (21 / 19 with noise tolerance), VIS 1e-9 to 2e-9; S5: |S*| = 482 (130 / 63 noise tolerance), VIS 9e-4.

## E6b (extra) S2 AR(1) 0.5, p=100: SEP ratio vs size of V (V = signal groups +- r groups)

| r | |V| | exhaustive | zeta/(n theta_min^2) | argmax (S, l) | Lemma-3 decrement (unit, x(n-1)c^2) |
|---|---|---|---|---|---|
| 0 | 20 | True | 0.36 | ((53,), 74) | 0.6 |
| 1 | 55 | False | 0.00035 | ((53,), 69) | 0.6 |
| 2 | 90 | False | 0.0 | ((53,), 90) | 0.6 |

### E7 -- proxy flood

| p | d | n | N | B | blocks w/ proxies | x1 in start | |start| (min-max) | |start\S0| | proxies/nulls in start (max) | ell | moves | local_limit | S0 scored | certified | final=S0 (capped) | HPM=S0 | uncapped moves to S0 (tau) | uncapped reach S0 | uncapped final=S0 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 120 | 20 | 200 | 20 | 10 | 3-3 | 20/20 | 4-6 | 3-5 | 5/0 | 9 | 3-5 | 0/20 | 20/20 | 20/20 | 20/20 | 20/20 | 3-5 | 20/20 | 20/20 |
| 120 | 20 | 800 | 20 | 10 | 3-3 | 20/20 | 7-9 | 6-8 | 8/0 | 10 | 6-8 | 0/20 | 20/20 | 20/20 | 19/20 | 19/20 | -1-8 | 19/20 | 19/20 |
| 120 | 20 | 3200 | 20 | 10 | 3-3 | 20/20 | 12-12 | 11-11 | 11/0 | 12 | 11-11 | 0/20 | 20/20 | 20/20 | 20/20 | 20/20 | 11-11 | 20/20 | 20/20 |
| 120 | 40 | 200 | 20 | 10 | 5-5 | 20/20 | 9-15 | 8-14 | 14/0 | 9 | 8-9 | 18/20 | 10/20 | 2/20 | 2/20 | 10/20 | 8-15 | 20/20 | 20/20 |
| 120 | 40 | 800 | 20 | 10 | 5-5 | 20/20 | 20-26 | 19-25 | 25/0 | 10 | 10-10 | 20/20 | 0/20 | 0/20 | 0/20 | 0/20 | 20-25 | 20/20 | 20/20 |
| 120 | 40 | 3200 | 20 | 10 | 5-5 | 20/20 | 31-32 | 30-31 | 31/0 | 12 | 12-12 | 20/20 | 0/20 | 0/20 | 0/20 | 0/20 | 30-32 | 20/20 | 20/20 |

### E7b (extra, beyond the spec): p=160, d=80, 5 seeds per row

| p | d | n | N | B | blocks w/ proxies | x1 in start | |start| (min-max) | |start\S0| | proxies/nulls in start (max) | ell | moves | local_limit | S0 scored | certified | final=S0 (capped) | HPM=S0 | uncapped moves to S0 (tau) | uncapped reach S0 | uncapped final=S0 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 160 | 80 | 800 | 5 | 12 | 7-7 | 5/5 | 40-47 | 39-46 | 46/0 | 10 | 10-10 | 5/5 | 0/5 | 0/5 | 0/5 | 0/5 | 39-46 | 5/5 | 5/5 |
| 160 | 80 | 3200 | 5 | 12 | 7-7 | 5/5 | 68-70 | 67-69 | 69/0 | 12 | 12-12 | 5/5 | 0/5 | 0/5 | 0/5 | 0/5 | 67-69 | 5/5 | 5/5 |

Reading. In every row the start mode contains x1 (20/20) and no null outside the proxy set; the proxies occupy 3 blocks (d = 20) or 5 blocks (d = 40). The number of non-S0 elements in the start mode is 3-5, 6-8, 11 for d = 20 and 8-14, 19-25, 30-31 for d = 40 at n = 200, 800, 3200, versus ell = 9, 10, 12; the number of uncapped LS0 moves needed to reach S0 is about |start \ S0| (tau = 3-5, 6-8 (one run never reaches S0), 11 for d = 20; 8-15, 20-25, 30-32 for d = 40). With the production cap, S0 is scored in 20/20, 20/20, 20/20 runs for d = 20 and in 10/20, 0/20, 0/20 for d = 40 (n = 200, 800, 3200); local_limit occurs in 0 runs for d = 20 and in 18/20, 20/20, 20/20 runs for d = 40. At d = 40, n = 200 the outcome depends on the realisation (|start \ S0| from 8 to 14 against ell = 9). E7b (d = 80, p = 160, B = 12, 5 seeds): |start \ S0| = 39-46 (n = 800, ell = 10) and 67-69 (n = 3200, ell = 12), LS0 uses all ell moves (local_limit 5/5) and never scores S0 (0/5), the uncapped search reaches S0 in 5/5 runs after 39-46 / 67-69 moves.

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
