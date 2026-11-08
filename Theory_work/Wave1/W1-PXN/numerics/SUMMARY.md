# W1-PXN numerics: SUMMARY (falsification attempts N1-N7)

Scripts run with `C:/Users/felip/anaconda3/python.exe` (numpy 1.26.4, scipy 1.13.1, mpmath 1.3.0). Fixed seeds (`default_rng([20260108, ...])`).
Per-script output is in `NAME.txt` next to `NAME.py`. Helper modules: `lhcommon.py` (LH-iid design, score F, tee), `enumlib.py` (p=10 enumeration, production local search).
Each script ran in under 2 minutes, with at most 20 seeds per experiment and exact enumeration only at p = 10.
Nothing was tuned to make a check pass. One bug in my own N6 check was found and fixed, and it is described under N6.
The folder `numerics/n8/` was not created by this run and was left untouched.

**Overall: no violation of any checked inequality, identity or implication in N1-N7.** These are numerical checks on finite grids and seeds, not proofs.

## N1 `n1_trJ.py` (Lemma Tr-J): no violation
- **(a) truncated moment.** The grid was n in {50,100,200,800}, u in {0,1,5,20}, tau in {0.01,0.05,0.2,0.5}, j in 1..24, which is 1536 cells.
  - Quadrature used a substitution that removes the x^{j/2-1} singularity. It agrees with a direct x-quadrature to 1.5e-13 on a subsample.
  - The exponent e1 = (u+j+3)/2+0.01 was asserted equal to nu+1-(m-j)/2 in every cell.
  - **Max ratio exact/bound = 0.462**, at (n,u,tau,j) = (800,0,0.5,8). The maximum ratio by tau is 0.25, 0.26, 0.29, 0.46.
- **(b) tail.** On the same 1536 cells the **max ratio exact/bound = 0.999987**, at (n,u,tau,j) = (200,0,0.01,18), so there is **no violation**.
  - The bound is essentially attained there: the exp(-(m-j)/16) term is negligible and the chi2 term is nearly the exact tail. The inequality is therefore tight in that corner, but it holds.
- **(c-core).** For j = 1..30 and t' >= 6j the **max ratio P(chi2_j>t')/exp(-t'/2+sqrt(j t')) = 0.0248**, at j=1, t'=6.
  - On the fine grid t'/j in [1,10] (step 0.001) the inequality **never fails for any j <= 30**. There is no "first failing ratio".
  - The max log-ratio is at t'/j = 1 and is negative (-1.65 at j=1, falling to -15.8 at j=30).
  - So the condition t' >= 6j has plenty of numerical slack. It is needed only for x = t'/2 - sqrt(j t') > 0 in the proof, and the claimed bound is true across [1,10].

## N2 `n2_lemmaE.py` (Lemma E, E1-E5): no violation
Setting: LH-iid with g=10, rho=.7, psi=.5, c=v=1 (s0=3), 5 seeds, 12.7k sets per seed (10 701 subsets of size <= 3 of the first 4 groups, plus 2000 random sets of size <= 5). That is 63 505 sets per (n,p) in {(100,60),(200,120),(400,200)}.
Constants: lambda_min(Sigma) = 0.235, phi0^2 = 0.1175, M = 4.5, c_E = 0.01515, kappa_E = 35.3.
- **Sample min eigenvalue of R_A.** It was never below phi0^2: 0.144 at n=100, 0.188 at n=200, 0.220 at n=400. The event E(F, phi0) therefore held for every set.
- **(E1)** eta_A lies in [-0.150, 0], [-0.061, 0], [-0.025, 0] for the three n. It uses at most 23% / 17% / 17% of the allowed negative range -2|A|/((n-1)phi0^2). There were 0 violations.
- **(E2)**
  - The identity G^-1 - nH^-1 = G^-1(G+I)H^-1 holds to max abs error 7e-17.
  - Q_A - RSS^y_A lies in [0, 0.71], [0, 0.71], [0, 0.67]. It uses at most 65-68% of the upper bound 1 + 1/((n-1)phi0^2), and a_A is in [0.02, 0.73]. There were 0 violations.
  - RSS^y_A from the formula and from direct least squares agree to 1e-6 relative (asserted for every set).
- **(E3)**
  - min RSS_A = 83.5 / 178.2 / 385.1, against the n sigma^2/2 floor of 50 / 100 / 200.
  - max ||Y||^2 = 294 / 643 / 1210, against the bound 3(M+sigma^2)n = 1650 / 3300 / 6600.
  - ||mu||^2/n <= 2.15, against M = 4.5. min RSS^y_A/n >= 0.281, against c_E = 0.0152.
  - There were 0 violations.
- **(E4)** R_A lies in [-1.24, 0.051], [-1.24, 0.013], [-1.06, 0.001], against kappa_E = 35.3. The proven range is therefore about 30x looser than what is observed.
  - The identity F(A) = log w - |A|/2 log(n+1) - nu log RSS_A + c_n + R_A holds to 7e-13 across all sets.
- **(E5)** max |RSS_A - n sigma^2 - Lambda_A| / n^{2/3} = 3.05 / 3.04 / 1.64. This gives an empirical C2 of about 3 (C2 is not explicit in the PROOF).

## N3 `n3_haar.py` (Haar-span step of Lemma Lambda(a), Lemma B): no violation
Setting: n=60, p=40, 5 seeds x 2000 draws, so 10 000 draws per test. The test list includes the specified cases and extra ones.
- **Lambda cases.** The pooled KS p-values (against the Beta law) were:
  - A_s={j_a}, A_0 = 2 null members: 0.356, mean 0.03480 vs 0.03448.
  - A_s={j_a}, A_0 = 3 null members: 0.504.
  - Extra cases: A_s={j_a, j_vis} 0.440; A_s=empty 0.182; A_0 = 1 member 0.510.
- **Lemma B cases.** The pooled KS p-values were:
  - B(i') (U={j_a, a-nonhub}, l = a second a-nonhub): 0.900, mean 0.01745 vs 0.01754.
  - B(i): a-group V of size 2: 0.558. b-group V={j_b}: 0.870. b-group {j_b, proxy}: 0.928. Visible nonhub: 0.964. Null group V of size 2: 0.534.
  - B(ii): 0.171.
- All 12 non-control tests have pooled p >= 0.17 and |mean z| <= 1.65. The variance ratio emp/theory is in [0.96, 1.03].
- **Per seed**, 6 of 60 KS p-values are below 0.05 (10%, against 5% nominal; the binomial tail P(X>=6) is about 0.08). This is not significant, and the pooled tests are all fine.
- **Negative control.** A deliberately wrong case (a-group U={}, V={j_a}, where j_a carries signal) is rejected with p = 0 in all 5 seeds. So the KS test has power.
- Outcome: no evidence against the Haar/Beta laws, including for equicorrelated null groups.

## N4 `n4_pairlaw.py` (W7-PART Lemma 2, Corollary B): no violation
- **Density checks.**
  - The Hotelling density integrates to 1 within 5.8e-13 over n in {10..500}, r in {-.9..,.9}.
  - scipy's 2F1 matches mpmath to 4e-16 (7 points, including n=500 and z=.985).
  - Against 400k-draw Monte Carlo for 10 (n,r,t) tails, max |z| = 1.15.
  - An independent exact route (Lemma 1: mixture of noncentral t over W ~ chi2_{n-1}) agrees to 1e-14 relative on 5 tails. One scipy `nct` RuntimeWarning appeared on stderr; the value still agreed to 1e-14.
- **(U) and (L).** There are 1482 (n,r,t) triples for each (n in {10,20,50,100,200,500}, r in -0.9..0.9, 13 t-offsets).
  - **Max ratio exact/bound = 0.443**, at n=10, r=0, t=0. By n: 0.443, 0.295, 0.181, 0.127, 0.089, 0.056. **There were 0 violations** for (U) and (L). The (L) numbers equal the (U) numbers by the r -> -r symmetry.
  - Two-sided consequences: the cross form (750 triples) has max ratio 0.286, and the within form (144 triples) has max ratio 0.140. There were 0 violations.
- **Corollary B** at rho=.7, psibar=.5: q = 1.2127, **t* = 0.6096, I* = 0.012587** (W7: 0.0126), and Lambda_rho(t*) = Lambda_psibar(t*) to 1e-12.
  - For p in {100,500}, g=10, n in {200,1000,5000}, the Corollary-B bound dominates the exact union bound N_w P_rho(|r|<=t*) + N_x P_psibar(|r|>=t*) by a factor of 673-15 000. It also dominates the B-explicit bound. There were 0 violations.
  - At n=200 the Corollary-B bound is e^{10.7} (p=100) and e^{13.9} (p=500), so it is **vacuous as a probability** there, as the PROOF says. It becomes non-trivial at n=5000: e^{-48} and e^{-45}.
  - The same domination holds for 4 other (rho,psibar) pairs with p=500, n=200/1000 (extra check, 0 violations).

## N5 `n5_margins.py` (population lattice margins; Lemma Lambda(c)): no violation
- Two batches of 40 settings: 40 random settings (c in 1..3, v in 0..2, g in 3..5, rho in (.3,.9), |psi| in rho*(.02,.98), |beta| in [.5,2]), and 40 extra adversarial ones (|psi| in (.9,.995)rho, rho in {.3,.5,.9}, |beta| in {.5,2}).
- All lattice states S in Lat(S°)\{S0}, and all non-progress neighbours (additions of any signal variable except progress hubs, all deletions, all swaps k -> l with l any signal variable, and A=S), were enumerated exactly.
- **c2.** min over settings of (min margin - c2) = -1.0e-15 (random) and -7.2e-16 (adversarial), i.e. **zero up to rounding**. Min margin/c2 = 1.000, with 0 violations.
  - The bound c2 is **attained** (|diff| < 1e-9) in 34/40 random and 21/40 adversarial settings. It is therefore sharp in those cases, and the minimisers are mostly "add-proxy" and "swap-diff-component".
  - Per-category min margin/c2: delete 2.66 (random) / 2.20 (adversarial), swap-same-component 2.40 / 2.10, add-proxy and swap-diff-component 1.000, A=S and add-other 1.11 / 1.09.
- **c5 for (L).** min over deletions and swaps of S0 of lambda(A) minus c5 is -1.0e-15 / -7.2e-16 (attained, 0 violations).
  - lambda(S0) and lambda(S0+l) are both 0 up to 2e-15, as used in the proof.
- **Lemma Lambda(c).** All equalities (lambda_i at {}, {j_b}, {j_a}, {j_a,j_b}, {j_a,l} for l in C_a and in C_b with the eta_i factor; the visible variances; additivity (b)) hold to 1.8e-15.
  - The inequality lambda_i(B) >= lambda0 beta^2 (1+psi^2 1{j_b notin B}) for |B| <= 2, j_a notin B has min slack 4.2e-2 (random) and 6.9e-3 (adversarial), so it holds.
  - The case-list values of 8.3 (lambda(S) = sum G_i, proxy drop G_i eta_i, deletion rises) hold to 2.3e-15.
  - (F4) lambda_min(Sigma) >= (1-psibar)(1-rho) holds, min slack 4.7e-3 (random) and 4.7e-2 (adversarial).
- Caveat: these are population quantities. At the smallest c2 (about 1.5e-4 to 7e-4 in some settings) the sample-level margin (D_S) needs astronomically large n, as PROOF (O5) already says.

## N6 `n6_ls_and_C.py` (Lemma LS and (C), exact enumeration, p=10): no implication violated
Design: g=2, c=2 (4 groups) plus 1 null group, rho=.7, psi=.5, beta=1, sigma=1. The production search was run from S° with ell = ceil(log2(n+p+1)) = 6, 8, 10. There are 20 seeds per n.

| n | D_S on all lattice states | (L) | search scores S0 | search certifies S0 | pi(S0)>1/2 |
|---|---|---|---|---|---|
| 50 | 3/20 | 5/20 | 14/20 | 3/20 | 0/20 |
| 200 | 20/20 | 19/20 | 20/20 | 19/20 | 18/20 |
| 1000 | 20/20 | 20/20 | 20/20 | 20/20 | 20/20 |

- **Implications checked.** Counts are premise-true cases / violations.
  - LS(i): the first c moves each add a masked hub, stay in Lat, and the c-th state is S0. 3 / 0, 20 / 0, 20 / 0.
  - LS(ii): D_S on all states and ell >= c-1 imply S0 is scored. 3 / 0, 20 / 0, 20 / 0.
  - LS(iii): D_S and (L) and ell >= c imply certified at S0 with no local_limit. 3 / 0, 19 / 0, 20 / 0.
  - (C): S0 scored and pi(S0) > 1/2 imply the best scored model is S0. The premise is vacuous at n=50 (pi(S0) never exceeds 1/2); it holds in 18 and 20 data sets at n=200 and 1000, with 0 violations.
  - Also pi(S0) > 1/2 implies MAP = S0, with 0 violations.
- **Bug in my first check.** An initial "violation" at n=200 seed 16 came from my own check being stricter than the lemma. I required the whole search to stop after c moves, but LS(i) constrains only the first c moves.
  - In that data set (L) fails (S0 + variable 7 beats S0, pi(S0) = 0.097), so the search continues past S0 and ends `local_certified` at (0,1,2,4,7). S0 is still scored, as LS(ii) says and as PROOF (O3) describes.
  - After correcting the check there is no violation.
- **Info.** At n=50 D_S holds in only 3/20 data sets, and (L) fails in 15/20. Yet S0 is still scored in 14/20, including 11 data sets where D_S fails. The lemma's premises are sufficient, not necessary, and they are not met at small n in this miniature.

## N7 `n7_posterior.py` (miniature of (P)): 1 - pi(S0) decreases in the median, but the upper tail does not shrink cleanly
Same p=10 design, 20 seeds per n, with no start involved.

| n | median 1-pi(S0) | 90% q | median ratio to sqrt(log n/n) | 90% q ratio | max 1-pi(S0) |
|---|---|---|---|---|---|
| 100 | 0.478 | 0.851 | 2.23 | 3.97 | 0.914 |
| 400 | 0.167 | 0.250 | 1.36 | 2.04 | 0.328 |
| 1600 | 0.0814 | 0.181 | 1.20 | 2.67 | 0.870 |
| 6400 | 0.0492 | 0.166 | 1.33 | 4.49 | 0.782 |

- **Trend.** The median and the 90% quantile of 1 - pi(S0) are both decreasing in n.
- **Scale.** The median of (1-pi)*sqrt(n) is about 3.3, 3.3, 3.9 for n = 400, 1600, 6400, so the decay is about n^{-1/2}.
  - For n >= 400 essentially all of 1 - pi(S0) is mass on strict supersets of S0 (the median mass of models not containing S0 is <= 1e-8). At n=100 the median missing mass is 0.19.
- **Caveat on the ratio.** The ratio to sqrt(log n/n) does **not** decrease or stabilise in its upper quantile (q90 3.97, 2.04, 2.67, 4.49; max 21 at n=6400). This is driven by rare draws with 1 - pi(S0) > 1/2:
  - n=1600 seed 17 (1-pi = 0.87, MAP = S0 + variable 9, Z^2 about 12.9 for the extra variable).
  - n=6400 seed 15 (1-pi = 0.78, MAP = S0 + variable 7, Z^2 about 13.4).
  - A 6000-replication check at n=400 found the generator's extra-variable statistic Z^2 follows chi2_1 (KS p between 0.11 and 0.84 per variable), so this is not a data-generation bug. It is the e^{Z^2/2} heavy tail of an extra variable.
  - With 20 seeds this is consistent with O_P(sqrt(log n/n)) but cannot confirm it. It is a sanity check only, far from p >> n.

## Violations list
**None** in N1-N7: no inequality, identity or implication failed. Observed near-tightness is worth recording:
- N1(b) is attained to 1.3e-5.
- The N5 bounds c2 and c5 are attained exactly in many settings.
- N4 Corollary B is vacuous at n=200 (as the PROOF says) but dominates the exact union bound everywhere.

Only items for a reviewer to be aware of, not violations: the N2 constants (kappa_E about 35) are about 30x looser than observed, N7's upper-tail ratio is not stabilised with 20 seeds, and N6 shows (D_S) and (L) are often false at n=50, which is consistent with PROOF (O5).
