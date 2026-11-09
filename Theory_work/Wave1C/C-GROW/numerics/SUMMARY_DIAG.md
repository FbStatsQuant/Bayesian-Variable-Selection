# C-GROW diagnostics (SUMMARY_DIAG) -- test sub-agent, assembled 2026-11-08 22:46

## Findings that matter  (FINAL, 22:48; observations only; each item names its section/output; p = 100/200/400, S2 and S5, iid rows)
1. **D1: S0 is the mode almost always, but the posterior is not sharp.** In 517 runs (`D1_raw.csv`) the best model found by uncapped LS (from S~0, from S0, from {} in 470 runs) and MC3 is S0 in 504; in 13 runs (9 at n = 200, 2 at 800, 2 at 3200) a model beats S0 by 0.07-1.4 nats: S0 + one null in 12, a distance-2 model (MC3 only, 0.07 nats) in 1. log sum over all add/delete/swap neighbours of exp(F(N)-F(S0)) is made of one-variable *additions* (delete / swap parts: medians -46 / -30 at n = 200 down to -3800 / -2500 at n = 12800; per-run maxima for n >= 800: -52 / -30); its median is -0.77 / -1.52 / -2.17 / -2.93 at n = 200 / 800 / 3200 / 12800, fit 1.93 - 0.51 ln n (S2 ~ S5, p = 100 ~ 400): (1-pi(S0))/pi(S0) >= ~7/sqrt(n). MC3 (20000 steps from S~0) spends 0.63 / 0.81 / 0.90 / 0.95 (medians) of its 2nd half at S0 and almost all of the rest at S0 + {null} (fraction at supersets of S0: mean 0.9985, min 0.46 in a beaten run).
2. **D2: with the production cap LS0 scores S0 for S2, fails for S5 once n >= ~800.** S2: S0 scored in 160/160 (p = 100), 35/35 (p = 200), 65/65 (p = 400). S5: 40/40, 38/40, 2/40, 0/40 at n = 200/800/3200/12800 (p = 100); 18/20, 6/20, 0/7 (p = 400); 0/10 (n = 800, c = 1), 6/10 (c = 0.5), 0/20 (n = 3200) at p = 200; all 138 runs (of 517) with S0 not scored are `local_limit`. S~0 contains S0 in 34/40 (n = 800), 40/40 (n >= 3200) of the S5 p = 100 runs: failure = number of extras, not missing truths (missing truths only at n = 200: S5 p = 400 S~0 misses >= 1 truth in 20/20).
3. **D3: extras |S~0 minus S0| grow like p x sqrt(n) for S5, stay <= 7 for S2.** S5 c = 1 medians: p = 100: 0 / 9 / 19 / 37 (n = 200/800/3200/12800) = 0.33 sqrt(n); p = 200: 1.5 / 20 / 39; p = 400: 1 / 28.5 / 70 (1.0-1.2 sqrt(n)); c = 0.5: 50-85% of that. Per null block (D3e): ~0.9 extras at n = 800 (in 85-92% of null blocks), 1.8-2.1 at n = 3200 (in 100%), max 4, independent of p and B (10/14/16): extras ~ 0.03-0.04 sqrt(n) x (#null blocks), against ell_n = 9..14. S2: median <= 3, max 7, no growth for n >= 800 or in p. Location (S5): p = 100 63-76% in blocks with no truth, 17-19% in a truth's block (not its group), 4-18% in a truth's group; p = 400 85-88% / 10-15% / <= 3%.
4. **D3: caps.** Cap |S~0| + ell_n scores S0 in 100% of runs in every cell. 2 ell_n is not enough once extras > 2 ell_n (S5 n = 12800 p = 100: 0/20 (c = 1), 12/20 (c = 0.5); p = 200 n = 3200: 0/10, 1/10; p = 400 n = 800: 9/20, n = 3200: 0/7). Uncapped LS0 reaches S0 in 508/517 runs; the 9 others are all among the 13 beaten runs of item 1.
5. **D3: path shape.** In the 508 runs reaching S0 the moves before tau are only +T (85), -N (4775), swN>N (24), swN>T (49): never +N, -T, or a swap that removes a truth. "Add missing truths, then delete extras one at a time" (only +T/-N, adds first) holds in 452/508; the other 56 runs contain a swap (70 of 73 swaps lead the path). tau <= |S~0 Delta S0| in 491/508; the 17 violations all contain a null->null swap (17 of the 18 runs with a swN>N token violate); max(tau - |Delta|) = 0 (S2), 1 (S5, p = 100, 200), 3 (S5, p = 400, c = 0.5, n = 800).
6. **D4 (production core `v3_fit`, no LS0; p = 100, c = 1; 27 fits, S2 n = 200/800/3200: 5/5/4, S5: 5/4/2 fits; S5 n = 3200 only 2 fits (1820-2285 s each on a shared machine), n = 12800 and p = 400 not run):** S0 is the reported HPM in all 25 fits on data seeds 0-4, found by the SMC stage itself (`hpm_before_local` = S0; first scored in pilot gibbs_flip / init_draw) and certified by the final LS from the global best. S0 is the exact HPM, hence in the scored set; also rank 1 in the top store. On the two data sets where Python finds S0 + one null better (S2 n = 200 seed 19, S5 n = 200 seed 12) the production HPM is that same S0 + null model (S0 is in the top store, hence scored). The scored set is observable only through HPM / top store (4001 models) / final-LS archive / HLL count (no model list for p > 32). R and Python scores agree up to one additive constant per data set (max deviation 1.8e-11).

---

## Notes: what was run, conventions, limitations (read before the tables)

**Files / provenance.** Library copied unchanged from `Theory_work/Wave1/W1-GEN/numerics/`: `bvs_core.py` (score F, Problem, partition, block tables, start_mode, local_search, ell_cap), `study_common.py` (study generator, `scenario_sigma`, `build_xy`), `exp_common.py` (`pmap`, writers). The templates `e5_outside.py` / `e6_study.py` in that folder (also at git HEAD) contain literal `\S0` junk in place of digits/identifiers (e.g. `p=\S00`, `NS = [\S00, \S00, 3\S00]`) and do not run as committed, so they were not copied; own drivers `d123_run.py`, `d123_run400.py`, `d123_run_extra.py` call `study_common.build_xy` exactly as E5/E6 did. Python 3.13 (numpy 2.3.0, scipy 1.15.3). Other files in this folder (`f1_run.py`, `f2_run.py`, `f3_run.py`, `f_*.py`, `f*_log.txt`, `f3_results.pkl`) are not mine.

**Designs.** S2 = AR(1), rho = 0.5; S5 = compound symmetry (0.3 between groups, 0.7 within), groups of 5; iid N(0, Sigma) rows, X standardised, y = c X beta + eps, sigma = 1 (`study_common.build_xy`, design "iid"; seed index `seed` gives the same (X, y) in every driver and in D4). s0 = 4, step 5, beta = (1.4, -1.0, 1.8, -1.2): truths at 0-based indices **2, 26, 53, 75** (groups 0, 5, 10, 15, positions 3, 2, 4, 1) **at every p** (p = 100, 200, 400): at p = 400 the truths are the same four variables, i.e. they sit in the first 76 columns and the other ~324 columns are pure null. c = 1 everywhere; c = 0.5 for S2 and S5 at p = 100 (all n), p = 400 (S2 n <= 3200, S5 n <= 800) and p = 200 (S5 n = 800, 3200; S2 n = 3200). Data seeds per row: p = 100: 20 (all n incl. 12800); p = 400: 10 (S5 c = 1 n = 3200: 7; S2 n = 12800: 5; **no S5 run at p = 400, n = 12800 (extrapolated cost: |S~0| ~ 150, scans of ~40k models of size ~150, hours per run) and none for S5 c = 0.5, n = 3200**); p = 200: 10 (S2 c = 0.5 n = 3200: 5), n in {200, 800, 3200} only. A p = 800 attempt was killed (machine shared with other jobs, 1 run finished; file `NOTUSED_p800_partial_raw.csv`, not used anywhere).

**Per-run procedure (`d_common.run`).** Partition = `bc.partition(X)` (data-based complete-linkage blocks, B = min(isqrt n, isqrt p, 16)), start mode S~0 = `bc.start_mode` (size-then-lex tie rule), K = min(p, n//2), ell_n = ceil(log2(n+p+1)). One *uncapped* local search from S~0 is traced (`ls_trace`, same move rule as `bc.local_search`: all feasible adds/deletes/swaps scanned, move to the neighbour with the largest F if it strictly exceeds F(centre), ties by smallest sorted tuple). The search with cap ell is **derived** from the trace (identical path prefix; local_limit iff the uncapped search needs more than ell moves; "S0 scored" = S0 is a centre or a one-flip/swap neighbour of some centre scanned within the cap). Validation: this derivation reproduced the results of direct `bc.local_search` calls for all four caps (34 columns x 320 rows at p = 100; 0 mismatches; kept as `OLD_p100_direct_ls_raw.csv`). Scan neighbours are scored without caching (memory); same arithmetic as `Problem.F_many`. tau = index of S0 on the path (0 = start mode is S0); |Delta| = |S~0 symmetric-difference S0|. Move tokens: `+T/+N` add truth/null, `-T/-N` delete truth/null, `swX>Y` swap out an X in, a Y (T = truth, N = null).

**D1.** F is the production score (prior as in bvs_core: log w(k) = -log 2 - log binom(2p-1, k)); D4 confirms the Python F equals the R production score up to one additive constant per data set (max deviation over the top-40 models 1.8e-11, `D4_raw.csv`, column scorer_offset_maxdev). (a) maximum over every model scored by: uncapped LS from S~0, from S0, from {} (**LS from {} was not run for S5 at p = 400 n >= 800 and p = 200 n = 3200** -- cost; column "LS from {} ends at S0" says "not run"/counts accordingly); the "incl. MC3" column adds all models proposed by the chain. D4's scored models are **not** included: the production core only exports the top store / HPM (see D4). (b) log sum over **all** add/delete/swap neighbours of S0 of exp(F(N) - F(S0)) (`bc.neighbours`, K-feasible), split by move type in the supplement. (c) MC3: 20000 steps from S~0, move type chosen uniformly among the valid types {add, delete, swap}, element(s) uniform, Hastings correction; target pi(S) proportional to exp F(S), |S| <= K; fraction of steps 10001..20000 with state exactly S0 (and with state a superset of S0); best model visited = max F among visited states. Single chain per data set (no convergence diagnostics beyond the comparison with LS from {} and the superset fraction).

**Limits to remember.** (i) D1(a) is a search-based lower bound on "a model beats S0": not exhaustive. (ii) "S0 scored" in D2/D3 refers to LS0's scan set only (as in W1-GEN), not to the full SMC. (iii) All numbers are observations for these designs and seeds.

**D4 completion status (stopped at the 90-minute budget).** 27 production fits completed (`d4_out/sum_*.json`, `D4_raw.csv`): S2 n = 200/800/3200: 5/5/4 fits (+1 targeted at n = 200), S5 n = 200/800/3200: 5/4/2 fits (+1 targeted at n = 200), c = 1, p = 100, data seeds 0-4 (subset). Killed unfinished at 22:46: S5 n = 3200 seeds 2 and 3 (seed 2 had run 30 min), S5 n = 800 seed 4, S2 n = 3200 seed 4 (not started); n = 12800 not run; S5 c = 0.5 and p = 400 not run in D4. The machine was shared with other jobs (S5 n = 3200: 1820 s and 2285 s wall per fit; 1 h allocation guard never triggered). The two "targeted" fits are the data sets (S2 n = 200 seed 19, S5 n = 200 seed 12, p = 100, c = 1) where the Python search finds S0 + one null better than S0. The 165 MB of exported CSV inputs (`d4_data/`) were deleted after use; regenerate with `py -3.13 d4_export.py 200,800,3200 5` (+ seeds 19 / 12 at n = 200, see d4_batch_extra.py). `d4_core/` is an unmodified copy of `Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core` (compiled in place, `.cpp_cache` inside it); nothing outside this folder was written.

---

## D1: posterior concentration on S0 (script d123_run.py -> RAW_*_raw.csv -> D1_raw.csv)

| design | N | (a) F(S0)-max F, LS-scored: min / #<0 | (a) same incl. MC3-proposed: min / #<0 | (a) best = S0 (LS) | (b) log sum_N exp(F(N)-F(S0)) med [min,max] | (b) #runs with a better neighbour | (c) frac time at S0, 2nd half: med [min,max] | (c) frac at supersets of S0 (med) | (c) best visited = S0 | (c) acc | LS from {} ends at S0 | LS from S0 stays |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S2 p=100 c=0.5 n=200 | 20 | -1.41 / 1 | -1.41 / 1 | 19/20 | -0.92 [-1.34, 1.86] | 1/20 | 0.670 [0.046, 0.744] | 1.000 | 19/20 | 0.067 | 19/20 | 19/20 |
| S2 p=100 c=0.5 n=800 | 20 | 0.00 / 0 | 0.00 / 0 | 20/20 | -1.63 [-1.92, -0.73] | 0/20 | 0.812 [0.623, 0.869] | 1.000 | 20/20 | 0.033 | 20/20 | 20/20 |
| S2 p=100 c=0.5 n=3200 | 20 | 0.00 / 0 | 0.00 / 0 | 20/20 | -2.14 [-2.70, 0.11] | 0/20 | 0.883 [0.476, 0.944] | 1.000 | 20/20 | 0.019 | 20/20 | 20/20 |
| S2 p=100 c=0.5 n=12800 | 20 | 0.00 / 0 | 0.00 / 0 | 20/20 | -3.00 [-3.28, -1.62] | 0/20 | 0.951 [0.851, 0.970] | 1.000 | 20/20 | 0.009 | 20/20 | 20/20 |
| S2 p=100 c=1 n=200 | 20 | -1.19 / 1 | -1.19 / 1 | 19/20 | -0.95 [-1.35, 1.66] | 1/20 | 0.679 [0.081, 0.748] | 1.000 | 19/20 | 0.066 | 19/20 | 19/20 |
| S2 p=100 c=1 n=800 | 20 | 0.00 / 0 | 0.00 / 0 | 20/20 | -1.64 [-1.93, -0.75] | 0/20 | 0.815 [0.629, 0.872] | 1.000 | 20/20 | 0.033 | 20/20 | 20/20 |
| S2 p=100 c=1 n=3200 | 20 | 0.00 / 0 | 0.00 / 0 | 20/20 | -2.14 [-2.70, 0.10] | 0/20 | 0.883 [0.482, 0.944] | 1.000 | 20/20 | 0.019 | 20/20 | 20/20 |
| S2 p=100 c=1 n=12800 | 20 | 0.00 / 0 | 0.00 / 0 | 20/20 | -3.00 [-3.28, -1.62] | 0/20 | 0.951 [0.851, 0.970] | 1.000 | 20/20 | 0.009 | 20/20 | 20/20 |
| S2 p=200 c=0.5 n=3200 | 5 | 0.00 / 0 | 0.00 / 0 | 5/5 | -2.15 [-2.40, -1.33] | 0/5 | 0.875 [0.792, 0.918] | 1.000 | 5/5 | 0.022 | 5/5 | 5/5 |
| S2 p=200 c=1 n=200 | 10 | -0.46 / 1 | -0.46 / 1 | 9/10 | -0.83 [-1.17, 0.79] | 1/10 | 0.648 [0.304, 0.714] | 1.000 | 9/10 | 0.068 | 9/10 | 9/10 |
| S2 p=200 c=1 n=800 | 10 | 0.00 / 0 | 0.00 / 0 | 10/10 | -1.38 [-1.71, -1.15] | 0/10 | 0.772 [0.697, 0.827] | 1.000 | 10/10 | 0.035 | 10/10 | 10/10 |
| S2 p=200 c=1 n=3200 | 10 | 0.00 / 0 | 0.00 / 0 | 10/10 | -2.18 [-2.40, -1.10] | 0/10 | 0.879 [0.760, 0.918] | 1.000 | 10/10 | 0.020 | 10/10 | 10/10 |
| S2 p=400 c=0.5 n=200 | 10 | 0.00 / 0 | -0.07 / 1 | 10/10 | -0.64 [-0.95, 0.44] | 0/10 | 0.568 [0.080, 0.693] | 1.000 | 9/10 | 0.071 | 10/10 | 10/10 |
| S2 p=400 c=0.5 n=800 | 10 | -0.76 / 1 | -0.76 / 1 | 9/10 | -1.37 [-1.65, 0.86] | 1/10 | 0.778 [0.050, 0.840] | 1.000 | 9/10 | 0.038 | 9/10 | 9/10 |
| S2 p=400 c=0.5 n=3200 | 10 | -0.57 / 1 | -0.57 / 1 | 9/10 | -2.10 [-2.52, 0.72] | 1/10 | 0.904 [0.385, 0.935] | 1.000 | 9/10 | 0.018 | 9/10 | 9/10 |
| S2 p=400 c=1 n=200 | 10 | 0.00 / 0 | 0.00 / 0 | 10/10 | -0.69 [-0.99, 0.27] | 0/10 | 0.590 [0.163, 0.696] | 1.000 | 10/10 | 0.070 | 10/10 | 10/10 |
| S2 p=400 c=1 n=800 | 10 | -0.69 / 1 | -0.69 / 1 | 9/10 | -1.39 [-1.66, 0.79] | 1/10 | 0.780 [0.102, 0.841] | 1.000 | 9/10 | 0.037 | 9/10 | 9/10 |
| S2 p=400 c=1 n=3200 | 10 | -0.55 / 1 | -0.55 / 1 | 9/10 | -2.11 [-2.52, 0.70] | 1/10 | 0.904 [0.385, 0.935] | 1.000 | 9/10 | 0.018 | 9/10 | 9/10 |
| S2 p=400 c=1 n=12800 | 5 | 0.00 / 0 | 0.00 / 0 | 5/5 | -2.82 [-2.96, -2.42] | 0/5 | 0.953 [0.935, 0.956] | 1.000 | 5/5 | 0.010 | 5/5 | 5/5 |
| S5 p=100 c=0.5 n=200 | 20 | -0.22 / 1 | -0.22 / 1 | 19/20 | -0.71 [-1.30, 0.76] | 1/20 | 0.571 [0.251, 0.785] | 1.000 | 19/20 | 0.072 | 19/20 | 19/20 |
| S5 p=100 c=0.5 n=800 | 20 | 0.00 / 0 | 0.00 / 0 | 20/20 | -1.55 [-1.90, 0.06] | 0/20 | 0.803 [0.428, 0.881] | 1.000 | 20/20 | 0.036 | 20/20 | 20/20 |
| S5 p=100 c=0.5 n=3200 | 20 | 0.00 / 0 | 0.00 / 0 | 20/20 | -2.15 [-2.66, -1.51] | 0/20 | 0.889 [0.819, 0.946] | 1.000 | 20/20 | 0.021 | 20/20 | 20/20 |
| S5 p=100 c=0.5 n=12800 | 20 | 0.00 / 0 | 0.00 / 0 | 20/20 | -2.78 [-3.29, -1.29] | 0/20 | 0.936 [0.742, 0.965] | 1.000 | 20/20 | 0.013 | 20/20 | 20/20 |
| S5 p=100 c=1 n=200 | 20 | -0.09 / 1 | -0.09 / 1 | 19/20 | -0.75 [-1.31, 0.66] | 1/20 | 0.594 [0.296, 0.786] | 1.000 | 19/20 | 0.071 | 19/20 | 19/20 |
| S5 p=100 c=1 n=800 | 20 | 0.00 / 0 | 0.00 / 0 | 20/20 | -1.56 [-1.90, 0.03] | 0/20 | 0.806 [0.434, 0.881] | 1.000 | 20/20 | 0.036 | 20/20 | 20/20 |
| S5 p=100 c=1 n=3200 | 20 | 0.00 / 0 | 0.00 / 0 | 20/20 | -2.15 [-2.66, -1.51] | 0/20 | 0.889 [0.820, 0.946] | 1.000 | 20/20 | 0.022 | 20/20 | 20/20 |
| S5 p=100 c=1 n=12800 | 20 | 0.00 / 0 | 0.00 / 0 | 20/20 | -2.78 [-3.29, -1.29] | 0/20 | 0.936 [0.742, 0.964] | 1.000 | 20/20 | 0.014 | 20/20 | 20/20 |
| S5 p=200 c=0.5 n=800 | 10 | 0.00 / 0 | 0.00 / 0 | 10/10 | -1.66 [-1.89, -0.93] | 0/10 | 0.814 [0.676, 0.883] | 1.000 | 10/10 | 0.034 | 10/10 | 10/10 |
| S5 p=200 c=0.5 n=3200 | 10 | 0.00 / 0 | 0.00 / 0 | 10/10 | -2.36 [-2.55, -2.03] | 0/10 | 0.910 [0.854, 0.944] | 1.000 | 10/10 | 0.018 | not run | 10/10 |
| S5 p=200 c=1 n=200 | 10 | -0.95 / 1 | -0.95 / 1 | 9/10 | -0.42 [-1.14, 1.44] | 1/10 | 0.535 [0.131, 0.709] | 1.000 | 9/10 | 0.071 | 9/10 | 9/10 |
| S5 p=200 c=1 n=800 | 10 | 0.00 / 0 | 0.00 / 0 | 10/10 | -1.66 [-1.89, -0.95] | 0/10 | 0.814 [0.681, 0.884] | 1.000 | 10/10 | 0.035 | 10/10 | 10/10 |
| S5 p=200 c=1 n=3200 | 10 | 0.00 / 0 | 0.00 / 0 | 10/10 | -2.36 [-2.55, -2.04] | 0/10 | 0.910 [0.854, 0.944] | 1.000 | 10/10 | 0.020 | not run | 10/10 |
| S5 p=400 c=0.5 n=200 | 10 | -0.94 / 1 | -0.94 / 1 | 9/10 | -0.61 [-1.13, 1.42] | 1/10 | 0.551 [0.086, 0.737] | 1.000 | 9/10 | 0.070 | 9/10 | 9/10 |
| S5 p=400 c=0.5 n=800 | 10 | 0.00 / 0 | 0.00 / 0 | 10/10 | -1.47 [-1.70, -0.85] | 0/10 | 0.788 [0.697, 0.843] | 1.000 | 10/10 | 0.038 | not run | 10/10 |
| S5 p=400 c=1 n=200 | 10 | -0.76 / 1 | -0.76 / 1 | 9/10 | -0.71 [-1.16, 1.27] | 1/10 | 0.610 [0.129, 0.740] | 1.000 | 9/10 | 0.070 | 9/10 | 9/10 |
| S5 p=400 c=1 n=800 | 10 | 0.00 / 0 | 0.00 / 0 | 10/10 | -1.48 [-1.71, -0.86] | 0/10 | 0.789 [0.700, 0.843] | 1.000 | 10/10 | 0.038 | not run | 10/10 |
| S5 p=400 c=1 n=3200 | 7 | 0.00 / 0 | 0.00 / 0 | 7/7 | -2.42 [-2.47, -1.79] | 0/7 | 0.912 [0.835, 0.935] | 1.000 | 7/7 | 0.022 | not run | 7/7 |

### D1 supplement: medians over runs of log sum_N exp(F(N)-F(S0)) [all / adds only / deletes only / swaps only] and MC3 mass at S0 (second half), c = 1

| design | n | runs | log-sum all | adds | deletes | swaps | MC3 frac at S0 (2nd half) |
|---|---|---|---|---|---|---|---|
| S2 p=100 | 200 | 20 | -0.95 | -0.95 | -62.01 | -52.36 | 0.679 |
| S2 p=100 | 800 | 20 | -1.64 | -1.64 | -266.14 | -215.86 | 0.815 |
| S2 p=100 | 3200 | 20 | -2.14 | -2.14 | -1097.85 | -880.75 | 0.883 |
| S2 p=100 | 12800 | 20 | -3.00 | -3.00 | -4407.30 | -3547.53 | 0.951 |
| S2 p=200 | 200 | 10 | -0.83 | -0.83 | -59.32 | -54.49 | 0.648 |
| S2 p=200 | 800 | 10 | -1.38 | -1.38 | -269.17 | -215.48 | 0.772 |
| S2 p=200 | 3200 | 10 | -2.18 | -2.18 | -1147.12 | -905.77 | 0.879 |
| S2 p=400 | 200 | 10 | -0.69 | -0.69 | -60.84 | -53.36 | 0.590 |
| S2 p=400 | 800 | 10 | -1.39 | -1.39 | -274.92 | -218.71 | 0.780 |
| S2 p=400 | 3200 | 10 | -2.11 | -2.11 | -1086.85 | -877.51 | 0.904 |
| S2 p=400 | 12800 | 5 | -2.82 | -2.82 | -4453.10 | -3585.34 | 0.953 |
| S5 p=100 | 200 | 20 | -0.75 | -0.75 | -55.21 | -34.28 | 0.594 |
| S5 p=100 | 800 | 20 | -1.56 | -1.56 | -230.90 | -152.59 | 0.806 |
| S5 p=100 | 3200 | 20 | -2.15 | -2.15 | -957.52 | -627.05 | 0.889 |
| S5 p=100 | 12800 | 20 | -2.78 | -2.78 | -3856.15 | -2518.71 | 0.936 |
| S5 p=200 | 200 | 10 | -0.42 | -0.42 | -49.61 | -31.51 | 0.535 |
| S5 p=200 | 800 | 10 | -1.66 | -1.66 | -233.09 | -142.64 | 0.814 |
| S5 p=200 | 3200 | 10 | -2.36 | -2.36 | -946.76 | -611.64 | 0.910 |
| S5 p=400 | 200 | 10 | -0.71 | -0.71 | -50.03 | -33.04 | 0.610 |
| S5 p=400 | 800 | 10 | -1.48 | -1.48 | -232.11 | -156.35 | 0.789 |
| S5 p=400 | 3200 | 7 | -2.42 | -2.42 | -947.86 | -618.91 | 0.912 |


---

## D2: LS0 with the production cap ell_n = ceil(log2(n+p+1)) from the start mode (script d123_run.py -> RAW_*_raw.csv -> D2_raw.csv)

| design | N | |S~0| med (min-max) | |S~0 minus S0| med (max) | |S0 minus S~0| max | S~0 contains S0 | S~0 = S0 | ell_n | S0 scored | final = S0 | local_limit | moves med (max) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S2 p=100 c=0.5 n=200 | 20 | 4 (3-6) | 0 (2) | 1 | 15/20 | 10/20 | 9 | 20/20 | 19/20 | 0/20 | 0 (2) |
| S2 p=100 c=0.5 n=800 | 20 | 5.5 (4-10) | 1.5 (6) | 0 | 20/20 | 3/20 | 10 | 20/20 | 20/20 | 0/20 | 1.5 (6) |
| S2 p=100 c=0.5 n=3200 | 20 | 7 (5-9) | 3 (5) | 0 | 20/20 | 0/20 | 12 | 20/20 | 20/20 | 0/20 | 3 (5) |
| S2 p=100 c=0.5 n=12800 | 20 | 7 (6-9) | 3 (5) | 0 | 20/20 | 0/20 | 14 | 20/20 | 20/20 | 0/20 | 3 (5) |
| S2 p=100 c=1 n=200 | 20 | 5 (4-6) | 1 (2) | 1 | 19/20 | 8/20 | 9 | 20/20 | 19/20 | 0/20 | 1 (2) |
| S2 p=100 c=1 n=800 | 20 | 6 (4-11) | 2 (7) | 0 | 20/20 | 2/20 | 10 | 20/20 | 20/20 | 0/20 | 2 (7) |
| S2 p=100 c=1 n=3200 | 20 | 7 (5-10) | 3 (6) | 0 | 20/20 | 0/20 | 12 | 20/20 | 20/20 | 0/20 | 3 (6) |
| S2 p=100 c=1 n=12800 | 20 | 7 (6-9) | 3 (5) | 0 | 20/20 | 0/20 | 14 | 20/20 | 20/20 | 0/20 | 3 (5) |
| S2 p=200 c=0.5 n=3200 | 5 | 7 (5-8) | 3 (4) | 0 | 5/5 | 0/5 | 12 | 5/5 | 5/5 | 0/5 | 3 (4) |
| S2 p=200 c=1 n=200 | 10 | 4 (3-6) | 0 (2) | 1 | 9/10 | 5/10 | 9 | 10/10 | 9/10 | 0/10 | 0.5 (2) |
| S2 p=200 c=1 n=800 | 10 | 6 (4-7) | 2 (3) | 0 | 10/10 | 1/10 | 10 | 10/10 | 10/10 | 0/10 | 2 (3) |
| S2 p=200 c=1 n=3200 | 10 | 7 (4-8) | 3 (4) | 0 | 10/10 | 1/10 | 12 | 10/10 | 10/10 | 0/10 | 3 (4) |
| S2 p=400 c=0.5 n=200 | 10 | 4 (3-5) | 0 (1) | 1 | 7/10 | 5/10 | 10 | 10/10 | 10/10 | 0/10 | 0.5 (1) |
| S2 p=400 c=0.5 n=800 | 10 | 4.5 (4-6) | 0.5 (2) | 0 | 10/10 | 5/10 | 11 | 10/10 | 9/10 | 0/10 | 0.5 (2) |
| S2 p=400 c=0.5 n=3200 | 10 | 6 (4-8) | 2 (4) | 0 | 10/10 | 1/10 | 12 | 10/10 | 9/10 | 0/10 | 2 (4) |
| S2 p=400 c=1 n=200 | 10 | 4.5 (4-6) | 1 (2) | 1 | 9/10 | 4/10 | 10 | 10/10 | 10/10 | 0/10 | 1 (2) |
| S2 p=400 c=1 n=800 | 10 | 5.5 (4-7) | 1.5 (3) | 0 | 10/10 | 3/10 | 11 | 10/10 | 9/10 | 0/10 | 1.5 (3) |
| S2 p=400 c=1 n=3200 | 10 | 6 (4-9) | 2 (5) | 0 | 10/10 | 1/10 | 12 | 10/10 | 9/10 | 0/10 | 2 (5) |
| S2 p=400 c=1 n=12800 | 5 | 7 (6-8) | 3 (4) | 0 | 5/5 | 0/5 | 14 | 5/5 | 5/5 | 0/5 | 3 (4) |
| S5 p=100 c=0.5 n=200 | 20 | 2 (2-6) | 0 (2) | 2 | 1/20 | 0/20 | 9 | 20/20 | 19/20 | 0/20 | 2 (3) |
| S5 p=100 c=0.5 n=800 | 20 | 10 (4-14) | 6 (10) | 2 | 15/20 | 0/20 | 10 | 20/20 | 20/20 | 0/20 | 6 (10) |
| S5 p=100 c=0.5 n=3200 | 20 | 20 (17-23) | 16 (19) | 0 | 20/20 | 0/20 | 12 | 2/20 | 0/20 | 20/20 | 12 (12) |
| S5 p=100 c=0.5 n=12800 | 20 | 33 (27-38) | 29 (34) | 0 | 20/20 | 0/20 | 14 | 0/20 | 0/20 | 20/20 | 14 (14) |
| S5 p=100 c=1 n=200 | 20 | 3 (2-7) | 0 (4) | 2 | 2/20 | 1/20 | 9 | 20/20 | 19/20 | 0/20 | 2 (4) |
| S5 p=100 c=1 n=800 | 20 | 13 (10-16) | 9 (12) | 1 | 19/20 | 0/20 | 10 | 18/20 | 15/20 | 5/20 | 9 (10) |
| S5 p=100 c=1 n=3200 | 20 | 23 (22-25) | 19 (21) | 0 | 20/20 | 0/20 | 12 | 0/20 | 0/20 | 20/20 | 12 (12) |
| S5 p=100 c=1 n=12800 | 20 | 41 (37-46) | 37 (42) | 0 | 20/20 | 0/20 | 14 | 0/20 | 0/20 | 20/20 | 14 (14) |
| S5 p=200 c=0.5 n=800 | 10 | 14.5 (9-24) | 10.5 (20) | 1 | 6/10 | 0/10 | 10 | 6/10 | 5/10 | 5/10 | 10 (10) |
| S5 p=200 c=0.5 n=3200 | 10 | 34.5 (28-38) | 30.5 (34) | 0 | 10/10 | 0/10 | 12 | 0/10 | 0/10 | 10/10 | 12 (12) |
| S5 p=200 c=1 n=200 | 10 | 4 (2-14) | 1.5 (11) | 2 | 1/10 | 0/10 | 9 | 9/10 | 8/10 | 1/10 | 2 (9) |
| S5 p=200 c=1 n=800 | 10 | 24 (19-26) | 20 (22) | 0 | 10/10 | 0/10 | 10 | 0/10 | 0/10 | 10/10 | 10 (10) |
| S5 p=200 c=1 n=3200 | 10 | 43 (38-46) | 39 (42) | 0 | 10/10 | 0/10 | 12 | 0/10 | 0/10 | 10/10 | 12 (12) |
| S5 p=400 c=0.5 n=200 | 10 | 2.5 (2-17) | 0 (16) | 3 | 0/10 | 0/10 | 10 | 9/10 | 8/10 | 1/10 | 2 (10) |
| S5 p=400 c=0.5 n=800 | 10 | 17 (8-36) | 13.5 (32) | 1 | 8/10 | 0/10 | 11 | 5/10 | 5/10 | 5/10 | 11 (11) |
| S5 p=400 c=1 n=200 | 10 | 3 (2-25) | 1 (23) | 2 | 0/10 | 0/10 | 10 | 9/10 | 7/10 | 2/10 | 2 (10) |
| S5 p=400 c=1 n=800 | 10 | 32.5 (15-41) | 28.5 (37) | 0 | 10/10 | 0/10 | 11 | 1/10 | 1/10 | 9/10 | 11 (11) |
| S5 p=400 c=1 n=3200 | 7 | 74 (68-79) | 70 (75) | 0 | 7/7 | 0/7 | 12 | 0/7 | 0/7 | 7/7 | 12 (12) |

---

## D3: LS0 with larger caps (script d123_run.py -> RAW_*_raw.csv -> D3_raw.csv)

### D3a larger caps

| design | N | sym-diff med (max) | cap=ell_n | cap=2ell_n | cap=size+ell_n | cap=unc |
|---|---|---|---|---|---|---|
| S2 p=100 c=0.5 n=200 | 20 | 0.5 (3) | [9] reach 19/20, scored 20/20, final=S0 19/20, limit 0/20 | [18] reach 19/20, scored 20/20, final=S0 19/20, limit 0/20 | [12-15] reach 19/20, scored 20/20, final=S0 19/20, limit 0/20 | [10000] reach 19/20, scored 20/20, final=S0 19/20, limit 0/20 |
| S2 p=100 c=0.5 n=800 | 20 | 1.5 (6) | [10] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [20] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [14-20] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [10000] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 |
| S2 p=100 c=0.5 n=3200 | 20 | 3 (5) | [12] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [24] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [17-21] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [10000] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 |
| S2 p=100 c=0.5 n=12800 | 20 | 3 (5) | [14] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [28] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [20-23] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [10000] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 |
| S2 p=100 c=1 n=200 | 20 | 1 (2) | [9] reach 19/20, scored 20/20, final=S0 19/20, limit 0/20 | [18] reach 19/20, scored 20/20, final=S0 19/20, limit 0/20 | [13-15] reach 19/20, scored 20/20, final=S0 19/20, limit 0/20 | [10000] reach 19/20, scored 20/20, final=S0 19/20, limit 0/20 |
| S2 p=100 c=1 n=800 | 20 | 2 (7) | [10] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [20] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [14-21] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [10000] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 |
| S2 p=100 c=1 n=3200 | 20 | 3 (6) | [12] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [24] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [17-22] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [10000] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 |
| S2 p=100 c=1 n=12800 | 20 | 3 (5) | [14] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [28] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [20-23] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [10000] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 |
| S2 p=200 c=0.5 n=3200 | 5 | 3 (4) | [12] reach 5/5, scored 5/5, final=S0 5/5, limit 0/5 | [24] reach 5/5, scored 5/5, final=S0 5/5, limit 0/5 | [17-20] reach 5/5, scored 5/5, final=S0 5/5, limit 0/5 | [10000] reach 5/5, scored 5/5, final=S0 5/5, limit 0/5 |
| S2 p=200 c=1 n=200 | 10 | 0.5 (2) | [9] reach 9/10, scored 10/10, final=S0 9/10, limit 0/10 | [18] reach 9/10, scored 10/10, final=S0 9/10, limit 0/10 | [12-15] reach 9/10, scored 10/10, final=S0 9/10, limit 0/10 | [10000] reach 9/10, scored 10/10, final=S0 9/10, limit 0/10 |
| S2 p=200 c=1 n=800 | 10 | 2 (3) | [10] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 | [20] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 | [14-17] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 | [10000] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 |
| S2 p=200 c=1 n=3200 | 10 | 3 (4) | [12] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 | [24] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 | [16-20] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 | [10000] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 |
| S2 p=400 c=0.5 n=200 | 10 | 0.5 (2) | [10] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 | [20] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 | [13-15] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 | [10000] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 |
| S2 p=400 c=0.5 n=800 | 10 | 0.5 (2) | [11] reach 9/10, scored 10/10, final=S0 9/10, limit 0/10 | [22] reach 9/10, scored 10/10, final=S0 9/10, limit 0/10 | [15-17] reach 9/10, scored 10/10, final=S0 9/10, limit 0/10 | [10000] reach 9/10, scored 10/10, final=S0 9/10, limit 0/10 |
| S2 p=400 c=0.5 n=3200 | 10 | 2 (4) | [12] reach 9/10, scored 10/10, final=S0 9/10, limit 0/10 | [24] reach 9/10, scored 10/10, final=S0 9/10, limit 0/10 | [16-20] reach 9/10, scored 10/10, final=S0 9/10, limit 0/10 | [10000] reach 9/10, scored 10/10, final=S0 9/10, limit 0/10 |
| S2 p=400 c=1 n=200 | 10 | 1 (2) | [10] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 | [20] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 | [14-16] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 | [10000] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 |
| S2 p=400 c=1 n=800 | 10 | 1.5 (3) | [11] reach 9/10, scored 10/10, final=S0 9/10, limit 0/10 | [22] reach 9/10, scored 10/10, final=S0 9/10, limit 0/10 | [15-18] reach 9/10, scored 10/10, final=S0 9/10, limit 0/10 | [10000] reach 9/10, scored 10/10, final=S0 9/10, limit 0/10 |
| S2 p=400 c=1 n=3200 | 10 | 2 (5) | [12] reach 9/10, scored 10/10, final=S0 9/10, limit 0/10 | [24] reach 9/10, scored 10/10, final=S0 9/10, limit 0/10 | [16-21] reach 9/10, scored 10/10, final=S0 9/10, limit 0/10 | [10000] reach 9/10, scored 10/10, final=S0 9/10, limit 0/10 |
| S2 p=400 c=1 n=12800 | 5 | 3 (4) | [14] reach 5/5, scored 5/5, final=S0 5/5, limit 0/5 | [28] reach 5/5, scored 5/5, final=S0 5/5, limit 0/5 | [20-22] reach 5/5, scored 5/5, final=S0 5/5, limit 0/5 | [10000] reach 5/5, scored 5/5, final=S0 5/5, limit 0/5 |
| S5 p=100 c=0.5 n=200 | 20 | 2 (3) | [9] reach 20/20, scored 20/20, final=S0 19/20, limit 0/20 | [18] reach 20/20, scored 20/20, final=S0 19/20, limit 0/20 | [11-15] reach 20/20, scored 20/20, final=S0 19/20, limit 0/20 | [10000] reach 20/20, scored 20/20, final=S0 19/20, limit 0/20 |
| S5 p=100 c=0.5 n=800 | 20 | 6 (10) | [10] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [20] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [14-24] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [10000] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 |
| S5 p=100 c=0.5 n=3200 | 20 | 16 (19) | [12] reach 0/20, scored 2/20, final=S0 0/20, limit 20/20 | [24] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [29-35] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [10000] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 |
| S5 p=100 c=0.5 n=12800 | 20 | 29 (34) | [14] reach 0/20, scored 0/20, final=S0 0/20, limit 20/20 | [28] reach 9/20, scored 12/20, final=S0 9/20, limit 11/20 | [41-52] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [10000] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 |
| S5 p=100 c=1 n=200 | 20 | 2 (5) | [9] reach 20/20, scored 20/20, final=S0 19/20, limit 0/20 | [18] reach 20/20, scored 20/20, final=S0 19/20, limit 0/20 | [11-16] reach 20/20, scored 20/20, final=S0 19/20, limit 0/20 | [10000] reach 20/20, scored 20/20, final=S0 19/20, limit 0/20 |
| S5 p=100 c=1 n=800 | 20 | 9 (12) | [10] reach 15/20, scored 18/20, final=S0 15/20, limit 5/20 | [20] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [20-26] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [10000] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 |
| S5 p=100 c=1 n=3200 | 20 | 19 (21) | [12] reach 0/20, scored 0/20, final=S0 0/20, limit 20/20 | [24] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [34-37] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [10000] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 |
| S5 p=100 c=1 n=12800 | 20 | 37 (42) | [14] reach 0/20, scored 0/20, final=S0 0/20, limit 20/20 | [28] reach 0/20, scored 0/20, final=S0 0/20, limit 20/20 | [51-60] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 | [10000] reach 20/20, scored 20/20, final=S0 20/20, limit 0/20 |
| S5 p=200 c=0.5 n=800 | 10 | 10.5 (20) | [10] reach 5/10, scored 6/10, final=S0 5/10, limit 5/10 | [20] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 | [19-34] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 | [10000] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 |
| S5 p=200 c=0.5 n=3200 | 10 | 30.5 (34) | [12] reach 0/10, scored 0/10, final=S0 0/10, limit 10/10 | [24] reach 1/10, scored 1/10, final=S0 1/10, limit 9/10 | [40-50] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 | [10000] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 |
| S5 p=200 c=1 n=200 | 10 | 3 (12) | [9] reach 9/10, scored 9/10, final=S0 8/10, limit 1/10 | [18] reach 10/10, scored 10/10, final=S0 9/10, limit 0/10 | [11-23] reach 10/10, scored 10/10, final=S0 9/10, limit 0/10 | [10000] reach 10/10, scored 10/10, final=S0 9/10, limit 0/10 |
| S5 p=200 c=1 n=800 | 10 | 20 (22) | [10] reach 0/10, scored 0/10, final=S0 0/10, limit 10/10 | [20] reach 5/10, scored 9/10, final=S0 5/10, limit 5/10 | [29-36] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 | [10000] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 |
| S5 p=200 c=1 n=3200 | 10 | 39 (42) | [12] reach 0/10, scored 0/10, final=S0 0/10, limit 10/10 | [24] reach 0/10, scored 0/10, final=S0 0/10, limit 10/10 | [50-58] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 | [10000] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 |
| S5 p=400 c=0.5 n=200 | 10 | 2 (19) | [10] reach 8/10, scored 9/10, final=S0 8/10, limit 1/10 | [20] reach 9/10, scored 10/10, final=S0 9/10, limit 0/10 | [12-27] reach 9/10, scored 10/10, final=S0 9/10, limit 0/10 | [10000] reach 9/10, scored 10/10, final=S0 9/10, limit 0/10 |
| S5 p=400 c=0.5 n=800 | 10 | 14 (32) | [11] reach 5/10, scored 5/10, final=S0 5/10, limit 5/10 | [22] reach 7/10, scored 7/10, final=S0 7/10, limit 3/10 | [19-47] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 | [10000] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 |
| S5 p=400 c=1 n=200 | 10 | 3 (25) | [10] reach 7/10, scored 9/10, final=S0 7/10, limit 2/10 | [20] reach 8/10, scored 9/10, final=S0 8/10, limit 1/10 | [12-35] reach 9/10, scored 10/10, final=S0 9/10, limit 0/10 | [10000] reach 9/10, scored 10/10, final=S0 9/10, limit 0/10 |
| S5 p=400 c=1 n=800 | 10 | 28.5 (37) | [11] reach 1/10, scored 1/10, final=S0 1/10, limit 9/10 | [22] reach 2/10, scored 2/10, final=S0 2/10, limit 8/10 | [26-52] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 | [10000] reach 10/10, scored 10/10, final=S0 10/10, limit 0/10 |
| S5 p=400 c=1 n=3200 | 7 | 70 (75) | [12] reach 0/7, scored 0/7, final=S0 0/7, limit 7/7 | [24] reach 0/7, scored 0/7, final=S0 0/7, limit 7/7 | [80-91] reach 7/7, scored 7/7, final=S0 7/7, limit 0/7 | [10000] reach 7/7, scored 7/7, final=S0 7/7, limit 0/7 |

### D3b uncapped path (from start mode): tau and move types up to tau

| design | N | unc reaches S0 | tau med (max) | tau <= |symdiff| | max (tau - |symdiff|) | tau == |symdiff| | only +T/-N tokens | adds first then dels (only +T,-N) | #swaps (total) | #+N | #-T | #+T | #-N |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S2 p=100 c=0.5 n=200 | 20 | 19/20 | 0 (2) | 19/19 | 0 | 17/19 | 17/19 | 17/19 | 2 | 0 | 0 | 3 | 6 |
| S2 p=100 c=0.5 n=800 | 20 | 20/20 | 1.5 (6) | 20/20 | 0 | 20/20 | 20/20 | 20/20 | 0 | 0 | 0 | 0 | 34 |
| S2 p=100 c=0.5 n=3200 | 20 | 20/20 | 3 (5) | 20/20 | 0 | 20/20 | 20/20 | 20/20 | 0 | 0 | 0 | 0 | 57 |
| S2 p=100 c=0.5 n=12800 | 20 | 20/20 | 3 (5) | 20/20 | 0 | 20/20 | 20/20 | 20/20 | 0 | 0 | 0 | 0 | 60 |
| S2 p=100 c=1 n=200 | 20 | 19/20 | 1 (2) | 19/19 | 0 | 18/19 | 18/19 | 18/19 | 1 | 0 | 0 | 0 | 13 |
| S2 p=100 c=1 n=800 | 20 | 20/20 | 2 (7) | 20/20 | 0 | 20/20 | 20/20 | 20/20 | 0 | 0 | 0 | 0 | 42 |
| S2 p=100 c=1 n=3200 | 20 | 20/20 | 3 (6) | 20/20 | 0 | 20/20 | 20/20 | 20/20 | 0 | 0 | 0 | 0 | 62 |
| S2 p=100 c=1 n=12800 | 20 | 20/20 | 3 (5) | 20/20 | 0 | 20/20 | 20/20 | 20/20 | 0 | 0 | 0 | 0 | 63 |
| S2 p=200 c=0.5 n=3200 | 5 | 5/5 | 3 (4) | 5/5 | 0 | 5/5 | 5/5 | 5/5 | 0 | 0 | 0 | 0 | 13 |
| S2 p=200 c=1 n=200 | 10 | 9/10 | 0 (2) | 9/9 | 0 | 9/9 | 9/9 | 9/9 | 0 | 0 | 0 | 1 | 4 |
| S2 p=200 c=1 n=800 | 10 | 10/10 | 2 (3) | 10/10 | 0 | 10/10 | 10/10 | 10/10 | 0 | 0 | 0 | 0 | 19 |
| S2 p=200 c=1 n=3200 | 10 | 10/10 | 3 (4) | 10/10 | 0 | 10/10 | 10/10 | 10/10 | 0 | 0 | 0 | 0 | 25 |
| S2 p=400 c=0.5 n=200 | 10 | 10/10 | 0.5 (1) | 10/10 | 0 | 8/10 | 8/10 | 8/10 | 2 | 0 | 0 | 1 | 2 |
| S2 p=400 c=0.5 n=800 | 10 | 9/10 | 0 (2) | 9/9 | 0 | 9/9 | 9/9 | 9/9 | 0 | 0 | 0 | 0 | 6 |
| S2 p=400 c=0.5 n=3200 | 10 | 9/10 | 2 (4) | 9/9 | 0 | 9/9 | 9/9 | 9/9 | 0 | 0 | 0 | 0 | 20 |
| S2 p=400 c=1 n=200 | 10 | 10/10 | 1 (2) | 10/10 | 0 | 9/10 | 9/10 | 9/10 | 1 | 0 | 0 | 0 | 7 |
| S2 p=400 c=1 n=800 | 10 | 9/10 | 1 (3) | 9/9 | 0 | 9/9 | 9/9 | 9/9 | 0 | 0 | 0 | 0 | 11 |
| S2 p=400 c=1 n=3200 | 10 | 9/10 | 2 (5) | 9/9 | 0 | 9/9 | 9/9 | 9/9 | 0 | 0 | 0 | 0 | 25 |
| S2 p=400 c=1 n=12800 | 5 | 5/5 | 3 (4) | 5/5 | 0 | 5/5 | 5/5 | 5/5 | 0 | 0 | 0 | 0 | 16 |
| S5 p=100 c=0.5 n=200 | 20 | 20/20 | 2 (2) | 20/20 | 0 | 19/20 | 19/20 | 19/20 | 1 | 0 | 0 | 33 | 2 |
| S5 p=100 c=0.5 n=800 | 20 | 20/20 | 6 (10) | 18/20 | 1 | 13/20 | 13/20 | 13/20 | 8 | 0 | 0 | 0 | 112 |
| S5 p=100 c=0.5 n=3200 | 20 | 20/20 | 16 (19) | 20/20 | 0 | 20/20 | 20/20 | 20/20 | 0 | 0 | 0 | 0 | 326 |
| S5 p=100 c=0.5 n=12800 | 20 | 20/20 | 29 (34) | 18/20 | 1 | 18/20 | 18/20 | 18/20 | 2 | 0 | 0 | 0 | 579 |
| S5 p=100 c=1 n=200 | 20 | 20/20 | 2 (4) | 20/20 | 0 | 14/20 | 14/20 | 14/20 | 7 | 0 | 0 | 20 | 6 |
| S5 p=100 c=1 n=800 | 20 | 20/20 | 9 (12) | 18/20 | 1 | 17/20 | 17/20 | 17/20 | 3 | 0 | 0 | 0 | 181 |
| S5 p=100 c=1 n=3200 | 20 | 20/20 | 19 (21) | 20/20 | 0 | 20/20 | 20/20 | 20/20 | 0 | 0 | 0 | 0 | 382 |
| S5 p=100 c=1 n=12800 | 20 | 20/20 | 37 (42) | 17/20 | 1 | 17/20 | 17/20 | 17/20 | 3 | 0 | 0 | 0 | 745 |
| S5 p=200 c=0.5 n=800 | 10 | 10/10 | 10.5 (20) | 9/10 | 1 | 5/10 | 5/10 | 5/10 | 5 | 0 | 0 | 0 | 116 |
| S5 p=200 c=0.5 n=3200 | 10 | 10/10 | 30.5 (34) | 9/10 | 1 | 9/10 | 9/10 | 9/10 | 1 | 0 | 0 | 0 | 299 |
| S5 p=200 c=1 n=200 | 10 | 10/10 | 2 (11) | 10/10 | 0 | 4/10 | 4/10 | 4/10 | 9 | 0 | 0 | 6 | 13 |
| S5 p=200 c=1 n=800 | 10 | 10/10 | 20 (22) | 10/10 | 0 | 10/10 | 10/10 | 10/10 | 0 | 0 | 0 | 0 | 190 |
| S5 p=200 c=1 n=3200 | 10 | 10/10 | 39 (42) | 10/10 | 0 | 10/10 | 10/10 | 10/10 | 0 | 0 | 0 | 0 | 388 |
| S5 p=400 c=0.5 n=200 | 10 | 9/10 | 2 (16) | 9/9 | 0 | 6/9 | 6/9 | 6/9 | 5 | 0 | 0 | 13 | 13 |
| S5 p=400 c=0.5 n=800 | 10 | 10/10 | 14.5 (34) | 6/10 | 3 | 5/10 | 5/10 | 5/10 | 11 | 0 | 0 | 0 | 153 |
| S5 p=400 c=1 n=200 | 10 | 9/10 | 2 (23) | 9/9 | 0 | 3/9 | 3/9 | 3/9 | 9 | 0 | 0 | 8 | 32 |
| S5 p=400 c=1 n=800 | 10 | 10/10 | 28.5 (39) | 8/10 | 2 | 8/10 | 8/10 | 8/10 | 3 | 0 | 0 | 0 | 266 |
| S5 p=400 c=1 n=3200 | 7 | 7/7 | 70 (75) | 7/7 | 0 | 7/7 | 7/7 | 7/7 | 0 | 0 | 0 | 0 | 487 |

### D3c growth and location of the extras S~0 minus S0

| design | |S~0 minus S0| mean | median | max | same group as truth | same block (not same group) | elsewhere | min idx-dist to a truth (pooled) |
|---|---|---|---|---|---|---|---|
| S2 p=100 c=0.5 n=200 | 0.5 | 0.0 | 2 | 7 (78%) | 0 (0%) | 2 (22%) | 1 |
| S2 p=100 c=0.5 n=800 | 1.7 | 1.5 | 6 | 25 (74%) | 3 (9%) | 6 (18%) | 1 |
| S2 p=100 c=0.5 n=3200 | 2.9 | 3.0 | 5 | 39 (68%) | 1 (2%) | 17 (30%) | 1 |
| S2 p=100 c=0.5 n=12800 | 3.0 | 3.0 | 5 | 36 (60%) | 0 (0%) | 24 (40%) | 1 |
| S2 p=100 c=1 n=200 | 0.8 | 1.0 | 2 | 12 (80%) | 0 (0%) | 3 (20%) | 1 |
| S2 p=100 c=1 n=800 | 2.1 | 2.0 | 7 | 31 (74%) | 4 (10%) | 7 (17%) | 1 |
| S2 p=100 c=1 n=3200 | 3.1 | 3.0 | 6 | 41 (66%) | 1 (2%) | 20 (32%) | 1 |
| S2 p=100 c=1 n=12800 | 3.1 | 3.0 | 5 | 37 (59%) | 0 (0%) | 26 (41%) | 1 |
| S2 p=200 c=0.5 n=3200 | 2.6 | 3.0 | 4 | 10 (77%) | 0 (0%) | 3 (23%) | 1 |
| S2 p=200 c=1 n=200 | 0.6 | 0.0 | 2 | 5 (83%) | 1 (17%) | 0 (0%) | 1 |
| S2 p=200 c=1 n=800 | 1.9 | 2.0 | 3 | 14 (74%) | 0 (0%) | 5 (26%) | 1 |
| S2 p=200 c=1 n=3200 | 2.5 | 3.0 | 4 | 19 (76%) | 0 (0%) | 6 (24%) | 1 |
| S2 p=400 c=0.5 n=200 | 0.4 | 0.0 | 1 | 2 (50%) | 1 (25%) | 1 (25%) | 1 |
| S2 p=400 c=0.5 n=800 | 0.7 | 0.5 | 2 | 6 (86%) | 0 (0%) | 1 (14%) | 1 |
| S2 p=400 c=0.5 n=3200 | 2.2 | 2.0 | 4 | 16 (73%) | 0 (0%) | 6 (27%) | 1 |
| S2 p=400 c=1 n=200 | 0.8 | 1.0 | 2 | 3 (38%) | 2 (25%) | 3 (38%) | 1 |
| S2 p=400 c=1 n=800 | 1.3 | 1.5 | 3 | 9 (69%) | 0 (0%) | 4 (31%) | 1 |
| S2 p=400 c=1 n=3200 | 2.7 | 2.0 | 5 | 20 (74%) | 0 (0%) | 7 (26%) | 1 |
| S2 p=400 c=1 n=12800 | 3.2 | 3.0 | 4 | 6 (38%) | 0 (0%) | 10 (62%) | 1 |
| S5 p=100 c=0.5 n=200 | 0.1 | 0.0 | 2 | 2 (67%) | 0 (0%) | 1 (33%) | 1 |
| S5 p=100 c=0.5 n=800 | 5.9 | 6.0 | 10 | 5 (4%) | 23 (19%) | 90 (76%) | 1 |
| S5 p=100 c=0.5 n=3200 | 16.3 | 16.0 | 19 | 37 (11%) | 57 (17%) | 232 (71%) | 1 |
| S5 p=100 c=0.5 n=12800 | 28.9 | 29.0 | 34 | 101 (17%) | 111 (19%) | 367 (63%) | 1 |
| S5 p=100 c=1 n=200 | 0.7 | 0.0 | 4 | 2 (15%) | 2 (15%) | 9 (69%) | 1 |
| S5 p=100 c=1 n=800 | 9.1 | 9.0 | 12 | 13 (7%) | 32 (18%) | 137 (75%) | 1 |
| S5 p=100 c=1 n=3200 | 19.1 | 19.0 | 21 | 53 (14%) | 68 (18%) | 261 (68%) | 1 |
| S5 p=100 c=1 n=12800 | 37.2 | 37.0 | 42 | 132 (18%) | 139 (19%) | 474 (64%) | 1 |
| S5 p=200 c=0.5 n=800 | 12.0 | 10.5 | 20 | 1 (1%) | 13 (11%) | 106 (88%) | 1 |
| S5 p=200 c=0.5 n=3200 | 29.9 | 30.5 | 34 | 18 (6%) | 23 (8%) | 258 (86%) | 1 |
| S5 p=200 c=1 n=200 | 2.2 | 1.5 | 11 | 0 (0%) | 4 (18%) | 18 (82%) | 1 |
| S5 p=200 c=1 n=800 | 19.0 | 20.0 | 22 | 5 (3%) | 17 (9%) | 168 (88%) | 1 |
| S5 p=200 c=1 n=3200 | 38.8 | 39.0 | 42 | 27 (7%) | 35 (9%) | 326 (84%) | 1 |
| S5 p=400 c=0.5 n=200 | 2.3 | 0.0 | 16 | 1 (4%) | 0 (0%) | 22 (96%) | 1 |
| S5 p=400 c=0.5 n=800 | 15.5 | 13.5 | 32 | 0 (0%) | 23 (15%) | 132 (85%) | 1 |
| S5 p=400 c=1 n=200 | 4.8 | 1.0 | 23 | 0 (0%) | 1 (2%) | 47 (98%) | 3 |
| S5 p=400 c=1 n=800 | 26.6 | 28.5 | 37 | 0 (0%) | 33 (12%) | 233 (88%) | 1 |
| S5 p=400 c=1 n=3200 | 69.6 | 70.0 | 75 | 16 (3%) | 47 (10%) | 424 (87%) | 1 |

### D3d growth: |S~0 minus S0| (median; max) and |S~0| (median) by n and p, c as stated (script build_growth.py <- RAW_*_raw.csv)

### S5, c = 1: |S~0 minus S0| median (max) [|S~0| median] [runs]

| n | p=100 | p=200 | p=400 |
|---|---|---|---|
| 200 | 0 (4) [3] [20] | 1.5 (11) [4] [10] | 1 (23) [3] [10] |
| 800 | 9 (12) [13] [20] | 20 (22) [24] [10] | 28.5 (37) [32.5] [10] |
| 3200 | 19 (21) [23] [20] | 39 (42) [43] [10] | 70 (75) [74] [7] |
| 12800 | 37 (42) [41] [20] | - | - |

### S5, c = 0.5: |S~0 minus S0| median (max) [|S~0| median] [runs]

| n | p=100 | p=200 | p=400 |
|---|---|---|---|
| 200 | 0 (2) [2] [20] | - | 0 (16) [2.5] [10] |
| 800 | 6 (10) [10] [20] | 10.5 (20) [14.5] [10] | 13.5 (32) [17] [10] |
| 3200 | 16 (19) [20] [20] | 30.5 (34) [34.5] [10] | - |
| 12800 | 29 (34) [33] [20] | - | - |

### S2, c = 1: |S~0 minus S0| median (max) [|S~0| median] [runs]

| n | p=100 | p=200 | p=400 |
|---|---|---|---|
| 200 | 1 (2) [5] [20] | 0 (2) [4] [10] | 1 (2) [4.5] [10] |
| 800 | 2 (7) [6] [20] | 2 (3) [6] [10] | 1.5 (3) [5.5] [10] |
| 3200 | 3 (6) [7] [20] | 3 (4) [7] [10] | 2 (5) [6] [10] |
| 12800 | 3 (5) [7] [20] | - | 3 (4) [7] [5] |

### S2, c = 0.5: |S~0 minus S0| median (max) [|S~0| median] [runs]

| n | p=100 | p=200 | p=400 |
|---|---|---|---|
| 200 | 0 (2) [4] [20] | - | 0 (1) [4] [10] |
| 800 | 1.5 (6) [5.5] [20] | - | 0.5 (2) [4.5] [10] |
| 3200 | 3 (5) [7] [20] | 3 (4) [7] [5] | 2 (4) [6] [10] |
| 12800 | 3 (5) [7] [20] | - | - |

### ratio |S~0 minus S0| / sqrt(n), S5 c = 1 and c = 0.5, medians (the true number of blocks J is in D3e)

| c | p | n | runs | median extras | extras/sqrt(n) |
|---|---|---|---|---|---|
| 1 | 100 | 200 | 20 | 0 | 0.00 |
| 1 | 100 | 800 | 20 | 9 | 0.32 |
| 1 | 100 | 3200 | 20 | 19 | 0.34 |
| 1 | 100 | 12800 | 20 | 37 | 0.33 |
| 1 | 200 | 200 | 10 | 1.5 | 0.11 |
| 1 | 200 | 800 | 10 | 20 | 0.71 |
| 1 | 200 | 3200 | 10 | 39 | 0.69 |
| 1 | 400 | 200 | 10 | 1 | 0.07 |
| 1 | 400 | 800 | 10 | 28.5 | 1.01 |
| 1 | 400 | 3200 | 7 | 70 | 1.24 |
| 0.5 | 100 | 200 | 20 | 0 | 0.00 |
| 0.5 | 100 | 800 | 20 | 6 | 0.21 |
| 0.5 | 100 | 3200 | 20 | 16 | 0.28 |
| 0.5 | 100 | 12800 | 20 | 29 | 0.26 |
| 0.5 | 200 | 800 | 10 | 10.5 | 0.37 |
| 0.5 | 200 | 3200 | 10 | 30.5 | 0.54 |
| 0.5 | 400 | 200 | 10 | 0 | 0.00 |
| 0.5 | 400 | 800 | 10 | 13.5 | 0.48 |


### D3e add-on: distribution of the extras S~0 minus S0 over the blocks of the start mode (5 seeds per row, c = 1; script d3_extras_blocks.py -> D3_blocks_raw.csv)

| scen | p | n | runs | J | B | extras | in_truth_blocks | in_null_blocks | null_blocks | null_blocks_with_extra | mean_extra_per_null_block | max_in_block |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S2 | 100 | 200 | 5 | 12 | 10 | 1.0 | 0.2 | 0.8 | 9.8 | 0.8 | 0.08 | 1 |
| S2 | 100 | 800 | 5 | 14 | 10 | 2.8 | 0.8 | 2.0 | 9.8 | 2.0 | 0.2 | 1 |
| S2 | 100 | 3200 | 5 | 13 | 10 | 2.2 | 0.2 | 2.0 | 9.2 | 2.0 | 0.22 | 1 |
| S2 | 200 | 200 | 5 | 21 | 14 | 0.8 | 0.2 | 0.6 | 16.8 | 0.6 | 0.04 | 1 |
| S2 | 200 | 800 | 5 | 20 | 14 | 2.0 | 0.2 | 1.8 | 16.2 | 1.8 | 0.11 | 1 |
| S2 | 200 | 3200 | 5 | 21 | 14 | 3.0 | 0.2 | 2.8 | 16.0 | 2.8 | 0.18 | 1 |
| S2 | 400 | 200 | 5 | 40 | 14 | 0.2 | 0.0 | 0.2 | 36.2 | 0.2 | 0.01 | 1 |
| S2 | 400 | 800 | 5 | 35 | 16 | 1.0 | 0.0 | 1.0 | 31.0 | 1.0 | 0.03 | 1 |
| S2 | 400 | 3200 | 5 | 37 | 16 | 2.6 | 0.0 | 2.6 | 31.2 | 2.6 | 0.08 | 1 |
| S5 | 100 | 200 | 5 | 11 | 10 | 0.0 | 0.0 | 0.0 | 7.2 | 0.0 | 0.0 | 0 |
| S5 | 100 | 800 | 5 | 10 | 10 | 8.8 | 1.4 | 7.4 | 7.8 | 7.2 | 0.95 | 2 |
| S5 | 100 | 3200 | 5 | 11 | 10 | 18.6 | 6.0 | 12.6 | 7.2 | 7.2 | 1.76 | 4 |
| S5 | 200 | 200 | 5 | 25 | 14 | 3.2 | 0.4 | 2.8 | 19.0 | 2.8 | 0.14 | 1 |
| S5 | 200 | 800 | 5 | 22 | 14 | 18.2 | 2.4 | 15.8 | 18.4 | 15.6 | 0.86 | 2 |
| S5 | 200 | 3200 | 5 | 23 | 14 | 39.6 | 7.0 | 32.6 | 18.8 | 18.8 | 1.74 | 4 |
| S5 | 400 | 200 | 5 | 45 | 14 | 6.8 | 0.0 | 6.8 | 41.0 | 6.8 | 0.17 | 1 |
| S5 | 400 | 800 | 5 | 33 | 16 | 30.4 | 3.6 | 26.8 | 30.0 | 26.0 | 0.89 | 2 |
| S5 | 400 | 3200 | 5 | 34 | 16 | 70.2 | 9.0 | 61.2 | 29.4 | 29.4 | 2.08 | 4 |

---

## D4: production core WITHOUT LS0 (R 4.4.1, `v3_fit`, allocation 8 GB / 1 h), same (X, y) as the Python runs

Scripts: `d4_export.py` (writes X, y from the Python generator) -> `d4_run.R` / `d4_batch.py` (fits; the core was copied to `d4_core/` and compiled there, 28 s) -> `d4_post.py` (this table, `D4_raw.csv`). Fields used: `hpm` (reported HPM), `top_store` (top 4001 scored models by F), `local_search` (final local-search archive), `instrumentation$scored` (distinct-model count, HLL), `hpm_before_local`, `hpm_provenance`.

**Is the scored set observable?** Not exactly. `v3_fit` exports the per-model scored set (`cpp_registry_scored_set`) only for p <= 32; at p = 100 the registry is in HLL mode (`n_distinct_hll` = approximate number of distinct scored models, no model list). What is exact: (i) the HPM (best F over all scored models, so F(S0) > F(HPM) would prove that S0 was never scored); (ii) the top store (the 4001 best scored models; full in every fit); (iii) the final local-search archive (centre, path, scanned centres, `scan_size`). 'S0 in scored set (decided)': scored if HPM = S0, or S0 in the top store, or S0 adjacent to a final-LS centre; not scored if F(S0) is above the top-store minimum yet S0 is absent; otherwise undecidable (count shown). The R scores equal the Python F up to one additive constant per data set (last column), so F(S0) is taken from the Python scorer. R seed = 1000 + data seed. c = 1, p = 100.

| design | fits | HPM = S0 | HPM contains S0 | HPM before final LS = S0 | S0 in scored set (decided) | S0 in top store | extras in HPM (total, max) | HPM first scored in (phase/mechanism) | final LS from global best certified | secs med (min-max) | max dev. of R-vs-Python score offset (top-40) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S2 p=100 c=1 n=200 (seeds 0-4) | 5 | 5/5 | 5/5 | 5/5 | 5 scored / 0 not / 0 undecidable | 5/5 | 0 (max 0) | pilot/gibbs_flip x2, pilot/init_draw x3 | 5/5 | 57 (20-95) | 1.1e-12 |
| S2 p=100 c=1 n=200 (targeted seed (Python best model != S0)) | 1 | 0/1 | 1/1 | 0/1 | 1 scored / 0 not / 0 undecidable | 1/1 | 1 (max 1) | pilot/init_draw x1 | 1/1 | 141 (141-141) | 6.8e-13 |
| S2 p=100 c=1 n=800 (seeds 0-4) | 5 | 5/5 | 5/5 | 5/5 | 5 scored / 0 not / 0 undecidable | 5/5 | 0 (max 0) | pilot/gibbs_flip x5 | 5/5 | 69 (40-176) | 1.8e-12 |
| S2 p=100 c=1 n=3200 (seeds 0-4) | 4 | 4/4 | 4/4 | 4/4 | 4 scored / 0 not / 0 undecidable | 4/4 | 0 (max 0) | pilot/gibbs_flip x4 | 4/4 | 94 (70-116) | 9.1e-12 |
| S5 p=100 c=1 n=200 (seeds 0-4) | 5 | 5/5 | 5/5 | 5/5 | 5 scored / 0 not / 0 undecidable | 5/5 | 0 (max 0) | pilot/gibbs_flip x2, pilot/init_draw x3 | 5/5 | 112 (39-160) | 1.1e-12 |
| S5 p=100 c=1 n=200 (targeted seed (Python best model != S0)) | 1 | 0/1 | 1/1 | 0/1 | 1 scored / 0 not / 0 undecidable | 1/1 | 1 (max 1) | pilot/gibbs_flip x1 | 1/1 | 262 (262-262) | 8.0e-13 |
| S5 p=100 c=1 n=800 (seeds 0-4) | 4 | 4/4 | 4/4 | 4/4 | 4 scored / 0 not / 0 undecidable | 4/4 | 0 (max 0) | pilot/gibbs_flip x4 | 4/4 | 632 (504-670) | 1.8e-12 |
| S5 p=100 c=1 n=3200 (seeds 0-4) | 2 | 2/2 | 2/2 | 2/2 | 2 scored / 0 not / 0 undecidable | 2/2 | 0 (max 0) | pilot/gibbs_flip x2 | 2/2 | 2053 (1820-2285) | 9.1e-12 |

---

## Pooled counts (script build_pooled.py <- RAW_*_raw.csv)

| subset | runs | uncapped reaches S0 | only +T/-N tokens | +T before all -N | tau <= |symdiff| | max(tau-|symdiff|) | runs with a swap before tau | #swaps | #+N | #-T |
|---|---|---|---|---|---|---|---|---|---|---|
| all runs | 517 | 508 | 452 | 452 | 491 | 3 | 56 | 73 | 0 | 0 |
| S2 p=100 | 160 | 158 | 155 | 155 | 158 | 0 | 3 | 3 | 0 | 0 |
| S2 p=200 | 35 | 34 | 34 | 34 | 34 | 0 | 0 | 0 | 0 | 0 |
| S2 p=400 | 65 | 61 | 58 | 58 | 61 | 0 | 3 | 3 | 0 | 0 |
| S5 p=100 | 160 | 160 | 138 | 138 | 151 | 1 | 22 | 24 | 0 | 0 |
| S5 p=200 | 50 | 50 | 38 | 38 | 48 | 1 | 12 | 15 | 0 | 0 |
| S5 p=400 | 47 | 45 | 29 | 29 | 39 | 3 | 16 | 28 | 0 | 0 |

Token counts up to tau over all runs reaching S0: +T: 85, -N: 4775, swN>N: 24, swN>T: 49
Swap tokens: position (leading block of swaps vs after a non-swap move): swN>N first: 24, swN>T first: 46, swN>T later: 3

### D1 pooled

runs: 517; runs with F(S0) < max F over LS-scored models: 12; incl. MC3-proposed: 13; runs with a better one-flip/swap neighbour than S0: 12; MC3 best visited = S0: 504
beaten runs by (scen, p, n): S2 p=100 c=1 n=200 seed=19 (-1.19, best symdiff to S0 = 1), S2 p=100 c=0.5 n=200 seed=19 (-1.41, best symdiff to S0 = 1), S5 p=100 c=1 n=200 seed=12 (-0.09, best symdiff to S0 = 1), S5 p=100 c=0.5 n=200 seed=12 (-0.22, best symdiff to S0 = 1), S5 p=200 c=1 n=200 seed=3 (-0.95, best symdiff to S0 = 1), S2 p=200 c=1 n=200 seed=6 (-0.46, best symdiff to S0 = 1), S5 p=400 c=1 n=200 seed=5 (-0.76, best symdiff to S0 = 1), S5 p=400 c=0.5 n=200 seed=5 (-0.94, best symdiff to S0 = 1), S2 p=400 c=1 n=3200 seed=7 (-0.55, best symdiff to S0 = 1), S2 p=400 c=1 n=800 seed=8 (-0.69, best symdiff to S0 = 1), S2 p=400 c=0.5 n=3200 seed=7 (-0.57, best symdiff to S0 = 1), S2 p=400 c=0.5 n=800 seed=8 (-0.76, best symdiff to S0 = 1), S2 p=400 c=0.5 n=200 seed=3 (-0.07, best symdiff to S0 = 0)
max over runs of the symmetric difference between S0 and the best model found (LS union): 1; of those beating S0: [0, 1]
MC3 fraction of the second half at supersets of S0: min over all runs 0.458
