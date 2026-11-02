# Regime L (p << n) headline answers

Roster: inputs manifest; 12 datasets x 2 scales = 24 cases; registry registry_fixture.csv (7 required rows). **PARTIAL STUDY: cell sizes are not the planned 100 / 600.**

Unit: the main SMC fit of each EXPECTED case (inputs manifest x scales) against the exact posterior (full enumeration). Missing or failed fits and missing references stay in every denominator and are counted in the tables (miss = no main fit, fail = failed fit, no exact = no ready exact reference).

## H1. Is the evidence estimate accurate?

e = log Z-hat - log Z (same standardised working-model scale), over the n_evid cases with a valid fit and exact reference. Lower-bound coverage = share of those n_evid fits with log Z-hat + log 0.05 <= log Z.

**p = 8, c050**

| scenario | n_cases | miss | fail | no_exact | n_evid | bias | rmse | median_abs_e | p90_abs_e | lb_coverage |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 3 | 0 | 0 | 0 | 3 | 0.038 | 0.0398 | 0.0372 | 0.0499 | 1 |
| 2 | 3 | 0 | 0 | 0 | 3 | 0.03 | 0.0365 | 0.0383 | 0.0479 | 1 |
| all | 6 | 0 | 0 | 0 | 6 | 0.034 | 0.0382 | 0.0378 | 0.0517 | 1 |

**p = 8, c100**

| scenario | n_cases | miss | fail | no_exact | n_evid | bias | rmse | median_abs_e | p90_abs_e | lb_coverage |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 3 | 0 | 0 | 0 | 3 | 0.122 | 0.189 | 0.0339 | 0.267 | 1 |
| 2 | 3 | 0 | 0 | 0 | 3 | 0.0393 | 0.0413 | 0.0357 | 0.0521 | 1 |
| all | 6 | 0 | 0 | 0 | 6 | 0.0809 | 0.137 | 0.0348 | 0.191 | 1 |

**p = 10, c050**

| scenario | n_cases | miss | fail | no_exact | n_evid | bias | rmse | median_abs_e | p90_abs_e | lb_coverage |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 3 | 0 | 0 | 0 | 3 | 1.34 | 2.31 | 0.0264 | 3.21 | 0.667 |
| 2 | 3 | 0 | 0 | 0 | 3 | 0.00216 | 0.0304 | 0.0297 | 0.0403 | 1 |
| all | 6 | 0 | 0 | 0 | 6 | 0.673 | 1.63 | 0.028 | 2.02 | 0.833 |

**p = 10, c100**

| scenario | n_cases | miss | fail | no_exact | n_evid | bias | rmse | median_abs_e | p90_abs_e | lb_coverage |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 3 | 0 | 0 | 0 | 3 | 0.0127 | 0.0216 | 0.012 | 0.0299 | 1 |
| 2 | 3 | 0 | 1 | 0 | 2 | 0.0479 | 0.055 | 0.0479 | 0.0695 | 1 |
| all | 6 | 0 | 1 | 0 | 5 | 0.0268 | 0.0386 | 0.0209 | 0.0587 | 1 |

## H2. Is the HPM accurate?

Percent of expected cases (missing or failed fits and missing references count as not equal).

**p = 8, c050**

| scenario | n_cases | miss | fail | no_exact | % SMC HPM = exact HPM | % exact HPM = truth | % SMC HPM = truth |
|---|---|---|---|---|---|---|---|
| 1 | 3 | 0 | 0 | 0 | 100 | 100 | 100 |
| 2 | 3 | 0 | 0 | 0 | 66.7 | 100 | 66.7 |
| all | 6 | 0 | 0 | 0 | 83.3 | 100 | 83.3 |

**p = 8, c100**

| scenario | n_cases | miss | fail | no_exact | % SMC HPM = exact HPM | % exact HPM = truth | % SMC HPM = truth |
|---|---|---|---|---|---|---|---|
| 1 | 3 | 0 | 0 | 0 | 100 | 100 | 100 |
| 2 | 3 | 0 | 0 | 0 | 100 | 100 | 100 |
| all | 6 | 0 | 0 | 0 | 100 | 100 | 100 |

**p = 10, c050**

| scenario | n_cases | miss | fail | no_exact | % SMC HPM = exact HPM | % exact HPM = truth | % SMC HPM = truth |
|---|---|---|---|---|---|---|---|
| 1 | 3 | 0 | 0 | 0 | 66.7 | 100 | 66.7 |
| 2 | 3 | 0 | 0 | 0 | 100 | 100 | 100 |
| all | 6 | 0 | 0 | 0 | 83.3 | 100 | 83.3 |

**p = 10, c100**

| scenario | n_cases | miss | fail | no_exact | % SMC HPM = exact HPM | % exact HPM = truth | % SMC HPM = truth |
|---|---|---|---|---|---|---|---|
| 1 | 3 | 0 | 0 | 0 | 100 | 100 | 100 |
| 2 | 3 | 0 | 1 | 0 | 66.7 | 100 | 66.7 |
| all | 6 | 0 | 1 | 0 | 83.3 | 100 | 83.3 |

## H3. Are the PIPs accurate (RB and plain)?

max err = max_j |PIP-hat_j - PIP_j| per fit; mean/p90 over the n_rb (RB) / n_plain (plain) fits that supply valid PIPs. err true / null = mean |error| over true / null variables. MPM = {PIP > 1/2}; % MPM = exact MPM is over all expected cases.

**p = 8, c050**

| scenario | n_cases | miss | fail | no_exact | n_rb | n_plain | rb_mean_max_err | rb_p90_max_err | rb_mean_err_true | rb_mean_err_null | plain_mean_max_err | plain_p90_max_err | plain_mean_err_true | plain_mean_err_null | pct_mpm_rb_eq_exact | pct_mpm_plain_eq_exact |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 3 | 0 | 0 | 0 | 3 | 3 | 0.0173 | 0.0205 | 0.00562 | 0.00787 | 0.0349 | 0.0427 | 0.0161 | 0.0132 | 100 | 100 |
| 2 | 3 | 0 | 0 | 0 | 3 | 3 | 0.0179 | 0.024 | 0.00973 | 0.00575 | 0.0305 | 0.0355 | 0.0129 | 0.0152 | 100 | 100 |
| all | 6 | 0 | 0 | 0 | 6 | 6 | 0.0176 | 0.0234 | 0.00767 | 0.00681 | 0.0327 | 0.0415 | 0.0145 | 0.0142 | 100 | 100 |

**p = 8, c100**

| scenario | n_cases | miss | fail | no_exact | n_rb | n_plain | rb_mean_max_err | rb_p90_max_err | rb_mean_err_true | rb_mean_err_null | plain_mean_max_err | plain_p90_max_err | plain_mean_err_true | plain_mean_err_null | pct_mpm_rb_eq_exact | pct_mpm_plain_eq_exact |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 3 | 0 | 0 | 0 | 3 | 3 | 0.0296 | 0.0444 | 0.0098 | 0.00812 | 0.0582 | 0.0883 | 0.0105 | 0.0152 | 100 | 100 |
| 2 | 3 | 0 | 0 | 0 | 3 | 3 | 0.018 | 0.026 | 0.00566 | 0.00968 | 0.0379 | 0.0445 | 0.0204 | 0.016 | 100 | 100 |
| all | 6 | 0 | 0 | 0 | 6 | 6 | 0.0238 | 0.039 | 0.00773 | 0.0089 | 0.0481 | 0.0725 | 0.0154 | 0.0156 | 100 | 100 |

**p = 10, c050**

| scenario | n_cases | miss | fail | no_exact | n_rb | n_plain | rb_mean_max_err | rb_p90_max_err | rb_mean_err_true | rb_mean_err_null | plain_mean_max_err | plain_p90_max_err | plain_mean_err_true | plain_mean_err_null | pct_mpm_rb_eq_exact | pct_mpm_plain_eq_exact |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 3 | 0 | 0 | 0 | 3 | 3 | 0.0239 | 0.0293 | 0.00741 | 0.00877 | 0.0361 | 0.0385 | 0.0148 | 0.0169 | 100 | 100 |
| 2 | 3 | 0 | 0 | 0 | 3 | 3 | 0.0191 | 0.0226 | 0.00792 | 0.00864 | 0.035 | 0.0392 | 0.0181 | 0.0158 | 100 | 100 |
| all | 6 | 0 | 0 | 0 | 6 | 6 | 0.0215 | 0.0272 | 0.00766 | 0.0087 | 0.0355 | 0.0396 | 0.0164 | 0.0164 | 100 | 100 |

**p = 10, c100**

| scenario | n_cases | miss | fail | no_exact | n_rb | n_plain | rb_mean_max_err | rb_p90_max_err | rb_mean_err_true | rb_mean_err_null | plain_mean_max_err | plain_p90_max_err | plain_mean_err_true | plain_mean_err_null | pct_mpm_rb_eq_exact | pct_mpm_plain_eq_exact |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 3 | 0 | 0 | 0 | 3 | 3 | 0.022 | 0.024 | 0.0108 | 0.00781 | 0.0388 | 0.0457 | 0.0121 | 0.0146 | 100 | 100 |
| 2 | 3 | 0 | 1 | 0 | 2 | 2 | 0.0188 | 0.0198 | 0.00712 | 0.00857 | 0.0386 | 0.0502 | 0.0162 | 0.0152 | 66.7 | 66.7 |
| all | 6 | 0 | 1 | 0 | 5 | 5 | 0.0207 | 0.024 | 0.00935 | 0.00811 | 0.0387 | 0.051 | 0.0137 | 0.0149 | 83.3 | 83.3 |

## H4. Exact recovery of the true support

Cells are `all-saved (passing-only)`: exact recoveries out of the number of expected cases in the cell; passing-only removes fits whose diagnostic flag is TRUE (master IV.1.3); failed, timed-out and not-run results are non-recoveries in both. Primary rule of every method, plus SMC pip05 and the exact HPM/MPM references; pooled over scenarios = /600 in the full study.

**p = 8, c050**

| method_id | rule_id | S1 | S2 | pooled |
|---|---|---|---|---|
| EXACT | hpm | 3/3 (3/3) | 3/3 (3/3) | 6/6 (6/6) |
| EXACT | mpm | 3/3 (3/3) | 3/3 (3/3) | 6/6 (6/6) |
| LASSO | cvmin | 1/3 (1/3) | 1/3 (1/3) | 2/6 (2/6) |
| SMCBVS | hpm | 3/3 (2/3) | 2/3 (0/3) | 5/6 (2/6) |
| SMCBVS | pip05 | 3/3 (2/3) | 3/3 (1/3) | 6/6 (3/6) |
| SUSIE | L10 | 1/3 (1/3) | 1/3 (1/3) | 2/6 (2/6) |

**p = 8, c100**

| method_id | rule_id | S1 | S2 | pooled |
|---|---|---|---|---|
| EXACT | hpm | 3/3 (3/3) | 3/3 (3/3) | 6/6 (6/6) |
| EXACT | mpm | 3/3 (3/3) | 3/3 (3/3) | 6/6 (6/6) |
| LASSO | cvmin | 1/3 (1/3) | 1/3 (1/3) | 2/6 (2/6) |
| SMCBVS | hpm | 3/3 (1/3) | 3/3 (2/3) | 6/6 (3/6) |
| SMCBVS | pip05 | 3/3 (1/3) | 3/3 (2/3) | 6/6 (3/6) |
| SUSIE | L10 | 1/3 (1/3) | 1/3 (1/3) | 2/6 (2/6) |

**p = 10, c050**

| method_id | rule_id | S1 | S2 | pooled |
|---|---|---|---|---|
| EXACT | hpm | 3/3 (3/3) | 3/3 (3/3) | 6/6 (6/6) |
| EXACT | mpm | 3/3 (3/3) | 3/3 (3/3) | 6/6 (6/6) |
| LASSO | cvmin | 1/3 (1/3) | 1/3 (1/3) | 2/6 (2/6) |
| SMCBVS | hpm | 2/3 (1/3) | 3/3 (1/3) | 5/6 (2/6) |
| SMCBVS | pip05 | 3/3 (2/3) | 3/3 (1/3) | 6/6 (3/6) |
| SUSIE | L10 | 1/3 (1/3) | 1/3 (1/3) | 2/6 (2/6) |

**p = 10, c100**

| method_id | rule_id | S1 | S2 | pooled |
|---|---|---|---|---|
| EXACT | hpm | 3/3 (3/3) | 3/3 (3/3) | 6/6 (6/6) |
| EXACT | mpm | 3/3 (3/3) | 3/3 (3/3) | 6/6 (6/6) |
| LASSO | cvmin | 1/3 (1/3) | 1/3 (1/3) | 2/6 (2/6) |
| SMCBVS | hpm | 3/3 (2/3) | 2/3 (1/3) | 5/6 (3/6) |
| SMCBVS | pip05 | 3/3 (2/3) | 2/3 (1/3) | 5/6 (3/6) |
| SUSIE | L10 | 1/3 (1/3) | 1/3 (1/3) | 2/6 (2/6) |

