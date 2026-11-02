CAMP <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign"
base <- file.path(CAMP, "code/bench_v2/lowp_port/smoke_output/results/smoke")
print(list.files(base, recursive = FALSE))
print(list.files(file.path(base, "p0030")))
f <- file.path(base, "p0030/p0030_S4_r050_c100/F3.rds")
r <- readRDS(f)
cat("top:", names(r), "\n")
str(r, max.level = 1, give.attr = FALSE)
if (!is.null(r$rules)) print(r$rules[, c("rule_id", "role", "status", "support", "k")])
if (!is.null(r$fit)) { cat("fit names:", names(r$fit), "\n"); print(r$fit$rules[, c("rule_id","role","status","support","k")]) }
