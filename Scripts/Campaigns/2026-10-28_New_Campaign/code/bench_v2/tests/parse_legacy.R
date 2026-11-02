root <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2"
for (f in c("F1_Lasso/tests/test_F1_lasso.R", "F2_ElasticNet/tests/test_F2_enet.R",
            "tests/compare_f1_nointercept.R")) {
  parse(file.path(root, f))
  cat("PASS parse", f, "\n")
}
