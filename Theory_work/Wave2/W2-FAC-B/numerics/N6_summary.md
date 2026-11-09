## N6: direct test of the extended-gap invariant (C2)(iii) (script n6_gap.py, raw N6_raw.jsonl)

Exact CS paths started at S* = [p] minus N0 (production lexicographic tie rule, cs_gain.py). At every pre-move set,
including T_0 and the one/two-extra states: a_T < x_T < b_T with extended endpoints, deleted nulls = {a_T < xi < b_T},
the move deletes a null at a gap edge. Layout 'oneblock' = all truths in a 16-block, N0 = the other 16 - s0 nulls of
that block, outside from the start and eligible for additions/swaps.

72 data sets; gap invariant held in 72, centre in gap in 72, pure null deletion in 70, final = S0 in 72; ties 0.

| rho | s0 | layout | n | p | N | N0 | gap inv | centre in gap | pure null del | final=S0 | max add gain/log n | max swap gain (vs F(T)) | max (best swap - best del) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.3 | 1 | oneblock | 2e+04 | 10000 | 3 | 15 | 3 | 3 | 2 | 3 | 0.209 | 7.03 | 2.07 |
| 0.3 | 1 | oneblock | 1e+05 | 2000 | 3 | 15 | 3 | 3 | 3 | 3 | -0.181 | 3.68 | -2.09 |
| 0.3 | 1 | oneblock | 1e+07 | 3000 | 3 | 15 | 3 | 3 | 3 | 3 | -0.277 | 3.61 | -4.46 |
| 0.3 | 1 | spread | 2e+04 | 10000 | 3 | 0 | 3 | 3 | 3 | 3 | -0.472 | -0.00 | -4.95 |
| 0.3 | 1 | spread | 1e+05 | 2000 | 3 | 0 | 3 | 3 | 3 | 3 | -0.394 | -0.00 | -5.06 |
| 0.3 | 1 | spread | 1e+07 | 3000 | 3 | 0 | 3 | 3 | 3 | 3 | -0.500 | -0.00 | -8.06 |
| 0.3 | 3 | oneblock | 2e+04 | 10000 | 3 | 13 | 3 | 3 | 3 | 3 | -0.246 | 2.52 | -2.43 |
| 0.3 | 3 | oneblock | 1e+05 | 2000 | 3 | 13 | 3 | 3 | 3 | 3 | -0.393 | 1.25 | -4.52 |
| 0.3 | 3 | oneblock | 1e+07 | 3000 | 3 | 13 | 3 | 3 | 3 | 3 | -0.424 | 1.23 | -6.83 |
| 0.3 | 4 | spread | 2e+04 | 10000 | 3 | 0 | 3 | 3 | 3 | 3 | -0.483 | -0.00 | -4.95 |
| 0.3 | 4 | spread | 1e+05 | 2000 | 3 | 0 | 3 | 3 | 3 | 3 | -0.470 | -0.00 | -5.76 |
| 0.3 | 4 | spread | 1e+07 | 3000 | 3 | 0 | 3 | 3 | 3 | 3 | -0.481 | -0.00 | -8.06 |
| 0.9 | 1 | oneblock | 2e+04 | 10000 | 3 | 15 | 3 | 3 | 2 | 3 | 0.209 | 7.03 | 2.07 |
| 0.9 | 1 | oneblock | 1e+05 | 2000 | 3 | 15 | 3 | 3 | 3 | 3 | -0.181 | 3.69 | -2.08 |
| 0.9 | 1 | oneblock | 1e+07 | 3000 | 3 | 15 | 3 | 3 | 3 | 3 | -0.277 | 3.61 | -4.46 |
| 0.9 | 1 | spread | 2e+04 | 10000 | 3 | 0 | 3 | 3 | 3 | 3 | -0.302 | -0.00 | -3.66 |
| 0.9 | 1 | spread | 1e+05 | 2000 | 3 | 0 | 3 | 3 | 3 | 3 | -0.308 | -0.00 | -4.01 |
| 0.9 | 1 | spread | 1e+07 | 3000 | 3 | 0 | 3 | 3 | 3 | 3 | -0.378 | -0.00 | -7.24 |
| 0.9 | 3 | oneblock | 2e+04 | 10000 | 3 | 13 | 3 | 3 | 3 | 3 | -0.246 | 2.52 | -2.43 |
| 0.9 | 3 | oneblock | 1e+05 | 2000 | 3 | 13 | 3 | 3 | 3 | 3 | -0.393 | 1.25 | -4.52 |
| 0.9 | 3 | oneblock | 1e+07 | 3000 | 3 | 13 | 3 | 3 | 3 | 3 | -0.379 | 1.23 | -6.83 |
| 0.9 | 4 | spread | 2e+04 | 10000 | 3 | 0 | 3 | 3 | 3 | 3 | -0.480 | -0.00 | -4.95 |
| 0.9 | 4 | spread | 1e+05 | 2000 | 3 | 0 | 3 | 3 | 3 | 3 | -0.487 | -0.00 | -5.76 |
| 0.9 | 4 | spread | 1e+07 | 3000 | 3 | 0 | 3 | 3 | 3 | 3 | -0.469 | -0.00 | -8.06 |

**Non-pure paths**: rho=0.3, n=20001, p=10000, s0=1, oneblock, seed=2; rho=0.9, n=20001, p=10000, s0=1, oneblock, seed=2

These are at n = 20001, p = n/2, N0 nonempty: with k ~ n/2 the multiplier M_T is ~1 (residual dimension n-1-p ~ n/2) and an
N0 coordinate with |xi| ~ 2.5 beats 1/2 log n ~ 5 at this n; asymptotically |xi_l| <= L_n with L_n^2 = o(log n) (L3 E1),
so this is a finite-n effect, not evidence on the event E_n (whose E6 with m1 = ceil(250000 L_n) cannot hold at this n; R04 item 7).
max swap gain relative to F(T) is positive (O(1)) on many paths, as R01 predicted; swaps never beat the best deletion
except in the two finite-n paths above.
(In the two non-pure runs the check loop stops at the first non-deletion move: 1 set checked; the path then makes one swap and still ends at S0 after m0 + 1 moves.)
