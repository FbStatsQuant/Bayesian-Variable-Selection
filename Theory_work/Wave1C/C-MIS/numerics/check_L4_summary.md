# check_L4 summary (max over 300 random models x 10 seeds per cell; violations must be <= ~1e-8)

| n | Delta | C1_rel_identity_err | C2_superset_lb_violation | C3_underfit_ub_violation | C4a_uniform_lb_violation | C4b_B3_violation | min(||r||^2+2r'e+2log n) on G5 | G5 freq |
|---|---|---|---|---|---|---|---|---|
| 200 | 0.5 | 3.28e-15 | -2.62e+00 | -7.89e+00 | -4.03e+00 | -2.67e-02 | 80.462 | 10/10 |
| 200 | 4.0 | 1.09e-15 | -2.99e+00 | -1.48e+01 | -5.04e+00 | -5.55e-02 | 779.841 | 10/10 |
| 800 | 0.5 | 4.89e-15 | -3.02e+00 | -7.67e+00 | -4.82e+00 | -7.85e-03 | 373.512 | 10/10 |
| 800 | 4.0 | 8.72e-16 | -3.03e+00 | -1.45e+01 | -4.58e+00 | -1.35e-02 | 3099.575 | 10/10 |
