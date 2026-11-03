# probe.R: inspect structures and time one theory row (td d=0) on an existing fit.
TRU <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/F_2026-10-19_benchmark_study_n200/Benchmark_Study_20261019/verify/recount/c050/inputs/truth_scoring"
B <- "C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019"
O <- "C:/Users/felip/Documents/NOTS_BVS/smcbvs_v3_deploy_20261022/claude/prod_p1000_20261023T1227Z/p1000"
inp <- readRDS(file.path(B, "inputs/p1000/p1000_S5_r001.rds")); cat("input names:", names(inp), "\n"); cat("Y cols:", colnames(inp$Y), "\n")
tr <- readRDS(file.path(TRU, "p1000/p1000_S5_r001.rds")); cat("truth names:", names(tr), "\n"); str(tr$active)
rec <- readRDS(file.path(O, "p1000_S5_r001_c100", "SMCBVS.rds")); cat("record names:", names(rec), "\n"); cat("fit names:", names(rec$fit), "\n")
cat("instrumentation names:", names(rec$fit$instrumentation), "\n"); cat("native_status:", rec$native_status, "\n")
SD <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/scoring"
Sys.setenv(SCORING_DIR = SD); source(file.path(SD, "run_theory_H.R"))
t0 <- Sys.time()
row <- theory_H_run(file.path(O, "p1000_S5_r001_c100", "SMCBVS.rds"), file.path(B, "inputs/p1000/p1000_S5_r001.rds"), file.path(TRU, "p1000/p1000_S5_r001.rds"), "c100", td_d = integer(0))
cat("no-TD row secs:", as.numeric(difftime(Sys.time(), t0, units = "secs")), "\n"); print(t(as.data.frame(row)))
t0 <- Sys.time()
row2 <- theory_H_run(file.path(O, "p1000_S5_r001_c100", "SMCBVS.rds"), file.path(B, "inputs/p1000/p1000_S5_r001.rds"), file.path(TRU, "p1000/p1000_S5_r001.rds"), "c100", td_d = 0L)
cat("TD0 row secs:", as.numeric(difftime(Sys.time(), t0, units = "secs")), "\n"); print(t(as.data.frame(row2))[grep("^td", names(row2)), , drop = FALSE])
