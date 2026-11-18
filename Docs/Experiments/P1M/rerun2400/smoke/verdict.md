# rerun2400 verdict (OLD v2.2.1 vs NEW v3.1)

run_id: smoke; fit pairs: 1; same-node pairs: 1

**OVERALL: NO REGRESSION**

Rule: legacy fields identical on completed fits; 0 completed->stopped; cell runtime ratio <= 1.25; pooled per p <= 1.1; RSS ratio <= 1.2.

| p | c | n_pairs | n_both_completed | n_legacy_differs | n_ls0_hpm_gain_disclosed | n_completed_to_stopped | n_stopped_to_completed | n_data_sha_problem | n_missing | n_admission_refusal | rt_median_old_s | rt_median_new_s | rt_ratio_row | rt_worst_cell | rt_worst_cell_ratio | n_cells_over_tol | rss_max_old_mb | rss_max_new_mb | rss_ratio | n_same_node | pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|  500 | c100 |    1 |    1 |    0 |    0 |    0 |    0 |    0 |    0 |    0 |  600 |  583 | 0.972 | S1 | 0.972 |    0 |  211 |  219 | 1.04 |    1 | TRUE |

Pooled per p:

| p | c | n_pairs | rt_median_old_s | rt_median_new_s | rt_ratio_row | pooled_paired_median_ratio | pass |
|---|---|---|---|---|---|---|---|
|  500 | all |    1 |  600 |  583 | 0.972 | 0.972 | TRUE |

Failed fits: 0

Disclosed (not failed): 0
