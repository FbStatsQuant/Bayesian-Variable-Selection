CAMP <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign"
base <- file.path(CAMP, "code/bench_v2/lowp_port/smoke_output/results/smoke")
for (cs in c("p0020/p0020_S1_r001_c100", "p0030/p0030_S4_r050_c050")) {
  for (m in c("F1", "F2", "F3", "F4", "F5")) {
    r <- readRDS(file.path(base, cs, paste0(m, ".rds")))
    cat("\n=====", cs, m, "=====\n")
    cat("rows cols (first 30):", paste(head(names(r$rows), 30), collapse = ","), "\n")
    print(r$rows[, intersect(c("rule_id", "role", "status", "support", "k", "crit_value", "ebic1_value", "index", "lambda", "tier", "label", "registry_role", "prereg"), names(r$rows))])
    cat("fit$rules roles:", paste(r$fit$rules$rule_id, r$fit$rules$role, collapse = " | "), "\n")
    cat("coefficient names:", paste(names(r$coefficients), collapse = ","), "\n")
  }
}
r <- readRDS(file.path(base, "p0020/p0020_S1_r001_c100/F4.rds"))
str(r$coefficients[[1]])
str(r$input)
