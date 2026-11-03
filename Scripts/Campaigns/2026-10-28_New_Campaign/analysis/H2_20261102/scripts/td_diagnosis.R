# td_diagnosis.R -- for a few TD d=0 cases, which move type beats the best truth-add at clause-(a) violators (ANALYSIS-H2, T37).
# Usage: Rscript td_diagnosis.R OUT_CSV CASE_ID [CASE_ID ...]   (case ids like p0500_S1_r001_c100)
# Also records the violating centres' sizes |S| (S subset of S0) to show where in the lattice clause (a) fails.
a <- commandArgs(trailingOnly = TRUE); out <- a[1]; ids <- a[-1]
INP <- "C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/inputs"
TRU <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/F_2026-10-19_benchmark_study_n200/Benchmark_Study_20261019/verify/recount/c050/inputs/truth_scoring"
SD <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/scoring"
Sys.setenv(SCORING_DIR = SD); source(file.path(SD, "run_theory_H.R"))
rows <- list()
for (id in ids) {
  ds <- sub("_c[0-9]{3}$", "", id); sc <- sub(".*_(c[0-9]{3})$", "\\1", id); pp <- substr(id, 1, 5)
  inp <- readRDS(file.path(INP, pp, paste0(ds, ".rds"))); tr <- readRDS(file.path(TRU, pp, paste0(ds, ".rds")))
  X <- inp$X; y <- as.numeric(inp$Y[, sc]); S0 <- sort(as.integer(tr$active)); scorer <- make_scorer(X, y)
  t0 <- Sys.time(); r <- run_td(X, y, scorer, S0, 0L, null_pool = NULL, margin = 0, max_scores = Inf, threads = 1L, engine = "auto")
  dg <- r$diagnosis; v <- r$literal$violations
  sz <- if (nrow(v)) table(vapply(strsplit(as.character(v$model[v$clause == "add_true"]), ";"), length, 0L)) else integer(0)
  for (i in seq_len(nrow(dg))) rows[[length(rows) + 1]] <- data.frame(case_id = id, kind = "best_competing_move", key = paste(dg$clause[i], dg$o_label[i]), n = dg$n[i])
  for (k in names(sz)) rows[[length(rows) + 1]] <- data.frame(case_id = id, kind = "violator_size", key = k, n = as.integer(sz[[k]]))
  cat(sprintf("%s %.0fs viol %d\n", id, as.numeric(difftime(Sys.time(), t0, units = "secs")), nrow(v)))
}
utils::write.csv(do.call(rbind, rows), out, row.names = FALSE)
