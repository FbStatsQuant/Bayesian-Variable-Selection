# theory_runner.R -- resumable batch of run_theory_H rows (ANALYSIS-H2).
# Usage: Rscript theory_runner.R LIST_TSV OUT_DIR WORKER NWORKERS TD   (TD = "none" or "0")
# LIST_TSV columns: case_id, dataset_id, p, scale_key, record (SMCBVS.rds path). Worker k (1..N) takes rows with (i-1) %% N == k-1.
# One CSV per case in OUT_DIR (written to .tmp then renamed); an existing CSV is skipped, so a killed run resumes. Errors -> <case>.err, continue.
a <- commandArgs(trailingOnly = TRUE)
lst <- a[1]; out <- a[2]; k <- as.integer(a[3]); N <- as.integer(a[4]); td <- a[5]
INP <- "C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/inputs"
TRU <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/F_2026-10-19_benchmark_study_n200/Benchmark_Study_20261019/verify/recount/c050/inputs/truth_scoring"
SD <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/scoring"
Sys.setenv(SCORING_DIR = SD); source(file.path(SD, "run_theory_H.R"))
dir.create(out, showWarnings = FALSE, recursive = TRUE)
L <- utils::read.delim(lst, stringsAsFactors = FALSE)
mine <- which((seq_len(nrow(L)) - 1L) %% N == k - 1L)
tdd <- if (identical(td, "none")) integer(0) else as.integer(td)
cat(sprintf("%s worker %d/%d: %d cases, td=%s\n", format(Sys.time(), "%FT%TZ", tz = "UTC"), k, N, length(mine), td))
for (i in mine) {
  r <- L[i, ]; f <- file.path(out, paste0(r$case_id, ".csv"))
  if (file.exists(f)) next
  pp <- sprintf("p%04d", as.integer(r$p))
  t0 <- Sys.time()
  row <- tryCatch(theory_H_run(r$record, file.path(INP, pp, paste0(r$dataset_id, ".rds")), file.path(TRU, pp, paste0(r$dataset_id, ".rds")),
                               r$scale_key, td_d = tdd), error = function(e) e)
  if (inherits(row, "error")) { writeLines(conditionMessage(row), file.path(out, paste0(r$case_id, ".err"))); cat("ERR", r$case_id, conditionMessage(row), "\n"); next }
  row$theory_secs <- as.numeric(difftime(Sys.time(), t0, units = "secs"))
  write_csv_na(row, paste0(f, ".tmp")); file.rename(paste0(f, ".tmp"), f)
  cat(sprintf("%s done %s %.1fs\n", format(Sys.time(), "%FT%TZ", tz = "UTC"), r$case_id, row$theory_secs))
}
cat(sprintf("%s WORKER_DONE %d\n", format(Sys.time(), "%FT%TZ", tz = "UTC"), k))
