# n8 - end-to-end LS0 route on LH-iid (SIZE holds, p > n): falsification diagnostic

Files (all in `numerics/n8/`): `n8_route.py` (driver), `n8_route.txt` (one table row per cell + per-fit lines), `n8_selfcheck.py`
(scorer / DP checks), this file. Python 3 + numpy 1.26 + scipy 1.13. Run: `python -B n8_route.py 10` (27 s wall).
Nothing outside `n8/` was touched; no git state change; no subagents.

## What was run
- LH-iid: g = 9, rho = 0.7, psi_i = 0.5 (one extra cell with psi = (0.5, 0.3)), beta_i = beta_vis = 1, sigma = 1.
  c in {1,2}, v in {0,1}, (n,p) in {(150,270),(300,540)}; B = 12 resp. 16. 8 base cells + the unequal-psi cell at both n = **10 cells x 10 seeds = 100 fits**.
  Seeds: `default_rng([seed, n, p, c, v, int(1000*psi[-1])])`, seed = 0..9.
- Score F exactly as STATEMENT s1 (standardised X, y; Cholesky logdets; w(k) = 0.5/binom(2p-1,k) in log space; K = min(p, n/2)); constants common to all
  models (the Gamma/pi factors, W_K) dropped, which changes no comparison and no pi0.
- Partition: Pearson |r| -> scipy complete linkage on 1-|r| -> my own left-first top-down cut at B and next-fit packing.
- Block tables r_b(U) for **all** 2^9 subsets of every block (no truncation in any fit). pi0 start mode by max-plus DP over blocks with total size as state
  (smallest size, then lex first on ties); normaliser and pi0(S_ref), pi0(S0) by log-sum-exp convolution.
- LS0: production search from S~0 (all flips and swaps, every scanned model scored, strict improvement, lex ties, <= ell = ceil(log2(n+p+1)) moves = 9 / 10, then one final scan).
- Self-checks passed (`n8_selfcheck.py`): scorer vs naive det/inv formula max err 8e-14; DP start mode, log Z and log pi0 vs brute force over all 4096 subsets of a toy p = 12
  (err ~1e-14); r_b(U) equals m(U)/m(empty) from the scorer. The g = 5 (SIZE-violating) path exercises blocks != groups without error.
- Notation: S_ref = S° = S0 minus masked hubs. "Visited" margin = (D_S) margin at lattice states on the LS0 path; "all" = over all 2^c - 1 lattice states whether visited or not;
  "Lgap" = F(S0) - max_neighbour F(A) (positive = (L) holds).

## Table (counts out of 10 seeds; margins min/median over the 10 fits)

| n,p,c,v,psi | blocks=groups | S~0=S° | S0 scored | S0 returned + certified | (L) | mean moves | 1-pi0(S°) med/max | D_S visited min/med | D_S all lattice min/med | Lgap min/med |
|---|---|---|---|---|---|---|---|---|---|---|
| 150,270,1,0,.5 | 10 | 9 | 10 | 9 | 9 | 0.90 | 0.22/0.88 | -0.00/2.76 | -0.00/3.51 | -0.00/1.92 |
| 150,270,1,1,.5 | 10 | 10 | 10 | 8 | 8 | 0.80 | 0.28/0.70 | -3.58/3.22 | -3.58/3.22 | -3.58/2.57 |
| 150,270,2,0,.5 | 10 | 8 | 10 | 8 | 8 | 2.30 | 0.40/0.97 | -1.52/1.27 | -1.52/1.38 | -1.52/1.78 |
| 150,270,2,1,.5 | 10 | 7 | **8** | 6 | 7 | 1.70 | 0.68/0.997 | -2.29/1.49 | -7.32/0.81 | -7.32/0.81 |
| 150,270,2,1,(.5,.3) | 10 | 9 | **8** | 3 | 3 | 1.30 | 0.51/0.76 | -4.23/-2.01 | -7.29/-3.11 | -4.56/-2.50 |
| 300,540,1,0,.5 | 10 | 10 | 10 | 10 | 10 | 1.00 | 0.13/0.19 | 6.83/13.30 | 6.83/13.30 | 0.35/4.53 |
| 300,540,1,1,.5 | 10 | 9 | 10 | 10 | 10 | 1.10 | 0.25/0.70 | 8.02/13.46 | 8.02/13.46 | 0.82/3.35 |
| 300,540,2,0,.5 | 10 | 10 | 10 | 10 | 10 | 2.10 | 0.22/0.43 | **-0.44**/5.92 | -0.44/5.92 | 0.69/4.06 |
| 300,540,2,1,.5 | 10 | 9 | 10 | 9 | 9 | 2.10 | 0.26/0.74 | 1.35/8.58 | 1.35/8.41 | **-0.82**/2.57 |
| 300,540,2,1,(.5,.3) | 10 | 10 | 10 | 10 | 10 | 2.00 | 0.26/0.49 | 0.26/2.40 | 0.26/2.40 | 0.26/2.34 |

(D_S visited: `nan` for fits whose path never entered the lattice because S~0 != S°; they are excluded from min/median. 5 such fits at n = 150, 1 at n = 300.)

## Headline numbers (50 fits per n)
| | n = 150 (p = 270) | n = 300 (p = 540) |
|---|---|---|
| blocks == groups (R) | 50/50 | 50/50 |
| S~0 == S° (E) | 43/50 | 48/50 |
| S0 scored by LS0 (T-score) | 46/50 | **50/50** |
| S0 returned + certified (T-cert) | 34/50 | 49/50 |
| (L) holds at S0 | 35/50 | 49/50 |
| D_S < 0 at some visited lattice state | 11/50 (5 more never entered the lattice) | 1/50 (1 more never entered) |
| D_S < 0 at some lattice state (visited or not) | 14/50 | 1/50 |
| median / max of 1-pi0(S°) | 0.45 / 0.997 | 0.24 / 0.74 (sqrt(log n/n) = 0.18 resp. 0.14) |
| fits with more than c moves (detours) | 3 | 3 |

## Surprises / honest reading
1. **No falsification of the asymptotic route at n = 300, but no strong confirmation either.** At n = 300, 100% blocks = groups and S0 is scored in 50/50. Certification fails in 1/50, (L) fails in 1/50.
   At n = 150 (below the n = 200 the STATEMENT already disclaims) the route degrades clearly: S0 not scored in 4/50 (all four at c = 2, v = 1; both psi settings), certified in 34/50.
   10 seeds per cell is too few for rates better than about +-0.15; the counts are indicative only.
2. **(D_S) fails at a visited lattice state in the n = 300 run (1/50).** Cell (300,540,c=2,v=0), seed 8: margin -0.44; the winning non-progress neighbour of S° is **adding a proxy `12` (a non-hub member of the b_1 group)**,
   not the hub. LS0 then took 3 moves (>c) and still reached S0 and certified. So Lemma LS(i) ("exactly c moves, states stay in Lat") is not literally true in this fit while the conclusion (S0 scored, certified) held.
   This is the proxy term G_i(1 - eta_i) of the population margin in PROOF s8.3 being swamped by noise at finite n; consistent with the asymptotic claim but a concrete D_S failure at n = 300.
3. **At n = 150 the dominant failure is not a null-variable addition but the masked hub itself: F(S0 - masked hub) > F(S0)** (11 of the 15 n=150 fits with (L) failing are the pure deletion of a masked hub; the other 4 swap a masked hub for another member: 2 for a proxy of the same pair, 2 for a null-group member).
   In 4/50 fits F(S0) < F(S°) (min dF = -7.3), i.e. the masked coefficient is not worth its penalty and S° itself beats S0. At n = 300, F(S0) - F(S°) > 10.8 in every fit.
   This is the (L)-at-S0 / (P) "masked regime" being finite-sample fragile, not a contradiction of the asymptotics.
4. **(L) failure at n = 300 is the slow null-addition mode** (cell c=2,v=1, seed 0, Lgap = -0.82, best neighbour `+286` = a null-group non-hub). LS0 made 3 moves (inferred: S0, then S0+286) and stopped certified at S0+286, not at S0; S0 had already been scored.
   One in 50 is of the order of the 2.5%-type rate flagged in PROOF s8.3. This affects certification only.
5. **Start mode != S° in 9/100 fits** (7/50 at n=150, 2/50 at n=300). Typical forms: a hub replaced by a proxy (`8` for hub `0`; `19`, `21` for hub `18`), an extra spurious member (`269`, `399`, `167`, `149`),
   or a missing a-hub (start = `(18,)` at n=300, c=1, v=1, 1-pi0 = 0.70). 1-pi0(S°) is large at these n: median 0.45 (n=150), 0.24 (n=300), 2.4x resp. 1.7x sqrt(log n/n); the ratio is shrinking but nowhere near small.
   Even so, S0 was still scored in 41/43 (n=150) and 48/48 (n=300) of the E = 1 fits, and in 5/7 (n=150) and 2/2 (n=300) of the E = 0 fits.
6. **Triviality caveat for (T-score):** for c = 1 and S~0 = S°, S0 is a flip neighbour of the start, so it is scored in the first scan with no (D_S) needed. The nontrivial part is c = 2 (one move needed); there n = 300 gives 30/30, n = 150 gives 26/30.
7. **P4 centring:** the observed centred statistic log pi0(S0) + c log p + (c/2) log n sits below the predicted mean in every cell (n = 300 differences vs predicted mean: -0.32, -0.72, -0.32, -0.60, -0.62; n = 150: -0.64, -0.06, -0.56, -1.92, -1.04;
   see the `obs mean` vs `pred ... mean` columns of `n8_route.txt`). Per-cell standard error is about 0.2-0.3, so each cell is only 1-3 se off, but all ten are negative (Stouffer z roughly -4 at n = 300).
   Likely finite-n O(1) shift (it is a limit statement) but it is a systematic offset worth a second look when P4 is written up.
8. Partition: complete linkage + cut + packing recovered the groups exactly in 100/100 fits including both p > n cases, even with the nearest cross-group correlation psi = 0.5 against rho = 0.7.

## Caveats
- The script does not test (S)/(P) at the level of pi(S0) (the full posterior); it tests pi0, the start mode and the F-landscape around S0 only.
- scipy's complete linkage resolves exact ties arbitrarily (measure zero here); the code's lexicographic tie rule for the linkage was not reproduced. All other tie rules are as specified.
- "Certified" = LS0 final centre is S0 and the last scan had no strict improvement (no `local_limit` occurred in any fit).
- Seeds are fixed; cells with 8-10 fits per outcome cannot support claims about probabilities. Total runtime 27 s; nothing was reduced.
