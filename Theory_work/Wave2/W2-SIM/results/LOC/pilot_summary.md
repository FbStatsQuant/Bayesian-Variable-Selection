# LOC pilot summary (loc_pilot01, job 2633109; partial: tasks 2, 4, 12 still running at 10:30)

Port runs (component port, scripts/loc_run.py):

| run | p | |S̃₀| | extras | S₀⊆S̃₀ | moves/cap | del/swap/add | final=S₀ | cert | extra dmax | nvis(2logp) | h_max(S₀) | 2log p | add_gap_final | t_start s | t_ls s | fast_err |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AF_0.4_spread_n64000_s_s1 | 765 | 552 | 549 | True | 549/568 | 549/0/0 | True | True | 133 | 760 | 8.76 | 13.28 | 7.10 | 2.82 | 29.87 | 5.2e-10 |
| CSG_0.5,0.8_two_n32000_q_s1 | 7876 | 199 | 195 | True | 195/215 | 195/0/0 | True | True | 0 | 354 | 10.86 | 17.94 | 7.81 | 36.21 | 19.09 | 3.3e-09 |
| PT_0.5_adj_n16000_q_s1 | 4000 | 315 | 312 | True | 314/330 | 312/2/0 | True | True | 1926 | 1265 | 18.02 | 16.59 | 3.43 | 12.97 | 25.95 | 1.2e-10 |
| PT_1.5_spread_n64000_s_s1 | 765 | 11 | 8 | True | 8/27 | 8/0/0 | True | True | 9 | 54 | 8.53 | 13.28 | 7.21 | 1.49 | 0.01 | 1.2e-10 |
| PT_8.5_adj_n16000_q_s1 | 4000 | 3 | 0 | True | 0/18 | 0/0/0 | True | True | 0 | 0 | 13.23 | 16.59 | 5.82 | 29.61 | 0.01 | 1.5e-11 |
| C1_n500_s1 | 125 | 5 | 2 | True | 2/15 | 2/0/0 | True | True | 1 | 4 | 6.37 | 9.66 | 4.05 | 0.05 | 0.0 | 2.3e-13 |
| C2_n2000_s1 | 500 | 7 | 4 | True | 4/19 | 4/0/0 | True | True | 29 | 22 | 9.87 | 12.43 | 4.38 | 1.94 | 0.01 | 1.8e-12 |
| C3_n2000_s1 | 495 | 24 | 21 | True | 21/36 | 21/0/0 | True | True | 0 | 132 | 6.64 | 12.41 | 5.99 | 1.74 | 0.02 | 5.5e-12 |
| C4_n500_s1 | 115 | 6 | 4 | False | 4/16 | 2/2/0 | True | True | 0 | 21 | 6.41 | 9.49 | 3.71 | 0.03 | 0.0 | 9.1e-13 |

Production fits (scripts/loc_prod_fit.R, design = file, same data bytes as the prodport run of the same id):

| id | status | elapsed s | |start mode| | S₀⊆start | LS0 moves/cap | HPM==S₀ | HPM before LS0==S₀ | LS0 returned==S₀ | preflight LS0 est s |
|---|---|---|---|---|---|---|---|---|---|
| C1_n500_s1 | completed | 11.2 | 5 | True | 2/15 | True | True | True | 355 |
| C2_n2000_s1 | completed | 118.5 | 7 | True | 4/19 | True | True | True | 1.45e+06 |
| C4_n500_s1 | completed | 40.7 | 6 | False | 4/16 | True | True | True | 223 |

Note: prod_fit.R's ls0_n_del/swap/add count transitions between entries of ls0$path, which omits the LS0 centre (first move not counted); loc_prod_extract.R (added after this pilot) prepends the centre. Validation: validation_nots.txt ALL_EQUAL True (18/18).
