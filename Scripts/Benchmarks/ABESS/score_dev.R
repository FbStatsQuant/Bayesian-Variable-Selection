#!/usr/bin/env Rscript
# score_dev.R: scoring step for the F5 dev test (master §IV.1.2 truth columns, error types).
# The only script of this folder that reads truth/; it runs after fitting and never writes
# into the results tree. Output: a scored copy of all rule rows and a summary table.
# Usage: Rscript --vanilla score_dev.R <results_dir> <dev_root> <out_prefix>

a <- commandArgs(trailingOnly = TRUE)
results_dir <- a[1]; dev_root <- a[2]; out_prefix <- a[3]
csvs <- list.files(results_dir, pattern = "\\.csv$", recursive = TRUE, full.names = TRUE)
if (!length(csvs)) stop("no rule-row CSV under ", results_dir)
rows <- do.call(rbind, lapply(csvs, function(f) utils::read.csv(f, stringsAsFactors = FALSE,
  colClasses = c(support = "character", support_audit = "character", diag_codes = "character",
                 warnings = "character", messages = "character", error = "character",
                 slurm_job_id = "character", slurm_array_task_id = "character"))))

truth_active <- function(dataset_id, p) {
  tr <- readRDS(file.path(dev_root, "truth", sprintf("p%04d", p), paste0(dataset_id, ".rds")))
  stopifnot(identical(tr$dataset_id, dataset_id)); as.integer(tr$active)
}
for (i in seq_len(nrow(rows))) {
  act <- truth_active(rows$dataset_id[i], rows$p[i])
  failed <- rows$status[i] %in% c("failed", "timeout", "not_run")
  s <- if (failed) NA_integer_ else if (!nzchar(rows$support[i])) integer() else
    as.integer(strsplit(rows$support[i], ";", fixed = TRUE)[[1L]])
  if (failed) {                                    # failed rows count as non-recovery
    rows$tp[i] <- NA; rows$fp[i] <- NA; rows$fn[i] <- NA; rows$exact[i] <- FALSE
    rows$error_type[i] <- "failed"
  } else {
    tp <- sum(s %in% act); fp <- length(s) - tp; fn <- length(act) - tp
    rows$tp[i] <- tp; rows$fp[i] <- fp; rows$fn[i] <- fn; rows$exact[i] <- fp == 0 && fn == 0
    rows$error_type[i] <- if (fp == 0 && fn == 0) "exact" else if (fn == 0) "extra_only" else
      if (fp == 0) "missed_only" else "mixed"
  }
  for (j in seq_along(act)) rows[[sprintf("sel_a%02d", j)]][i] <- if (failed) NA else act[j] %in% s
}
rows <- rows[order(rows$p, rows$scenario, match(rows$rule_id, c("ebic1", "ebic05", "bic"))), ]
utils::write.csv(rows, paste0(out_prefix, "_scored_rows.csv"), row.names = FALSE, na = "NA")
tab <- data.frame(dataset = rows$dataset_id, rule = rows$rule_id, role = rows$role,
                  status = rows$status, k = rows$k, TP = rows$tp, FP = rows$fp, FN = rows$fn,
                  exact = rows$exact, error_type = rows$error_type, diag_codes = rows$diag_codes,
                  runtime_s = round(rows$runtime_s, 3), stringsAsFactors = FALSE)
utils::write.csv(tab, paste0(out_prefix, "_table.csv"), row.names = FALSE, na = "NA")
print(tab, right = FALSE, row.names = FALSE)
cat("\nExact recovery by rule (12 datasets, c100):\n")
print(tapply(tab$exact, tab$rule, sum))
