# rerun2400 verdict (OLD v2.2.1 vs NEW v3.1)

run_id: rr2400_20261118T0636Z; fit pairs: 121; same-node pairs: 121

**OVERALL: NO REGRESSION**

Rule: legacy fields identical on completed fits; 0 completed->stopped; cell runtime ratio <= 1.25; pooled per p <= 1.1; RSS ratio <= 1.2.

| p | c | n_pairs | n_both_completed | n_legacy_differs | n_ls0_hpm_gain_disclosed | n_completed_to_stopped | n_stopped_to_completed | n_data_sha_problem | n_missing | n_admission_refusal | rt_median_old_s | rt_median_new_s | rt_ratio_row | rt_worst_cell | rt_worst_cell_ratio | n_cells_over_tol | rss_max_old_mb | rss_max_new_mb | rss_ratio | n_same_node | pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|  500 | c100 |   31 |   30 |    0 |    0 |    0 |    0 |    0 |    0 |    0 |  547 |  538 | 0.985 | S5 | 0.997 |    0 |  236 |  250 | 1.06 |   31 | TRUE |
|  500 | c050 |   30 |   30 |    0 |    0 |    0 |    0 |    0 |    0 |    0 |  586 |  570 | 0.972 | S1 | 1.02 |    0 |  252 |  253 |    1 |   30 | TRUE |
| 1e+03 | c100 |   30 |   30 |    0 |    0 |    0 |    0 |    0 |    0 |    0 | 1.71e+03 | 1.64e+03 | 0.961 | S6 | 0.978 |    0 |  377 |  382 | 1.01 |   30 | TRUE |
| 1e+03 | c050 |   30 |   30 |    0 |    0 |    0 |    0 |    0 |    0 |    0 | 1.65e+03 | 1.61e+03 | 0.975 | S5 |    1 |    0 |  383 |  393 | 1.03 |   30 | TRUE |

Pooled per p:

| p | c | n_pairs | rt_median_old_s | rt_median_new_s | rt_ratio_row | pooled_paired_median_ratio | pass |
|---|---|---|---|---|---|---|---|
|  500 | all |   61 |  586 |  549 | 0.938 | 0.975 | TRUE |
| 1e+03 | all |   60 | 1.67e+03 | 1.61e+03 | 0.967 | 0.978 | TRUE |

Failed fits: 0

Disclosed (not failed): 0
