#!/usr/bin/env Rscript
# score_dev.R -- scoring step for the F2 dev test (master §IV.1.2 truth columns; §II.10).
# This is the only F2 script that reads truth/. It runs after fitting, in its own process.
# Usage: Rscript score_dev.R <results/<run_id> dir> <dev truth root> <out_dir>
# Writes <out_dir>/scored_rows.csv (all rule rows with tp, fp, fn, exact, error_type and
# sel_a01..sel_a14 filled) and <out_dir>/dev_table.csv (dataset, rule, status, k, TP, FP,
# FN, exact, runtime).

args <- commandArgs(TRUE)
if (length(args) != 3L) stop("usage: score_dev.R <results_run_dir> <truth_root> <out_dir>")
res_dir <- normalizePath(args[1], mustWork = TRUE); truth_root <- normalizePath(args[2], mustWork = TRUE)
out_dir <- args[3]; dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

csvs <- sort(list.files(res_dir, pattern = "^F2\\.csv$", recursive = TRUE, full.names = TRUE))
if (!length(csvs)) stop("no F2.csv under ", res_dir)
rows <- do.call(rbind, lapply(csvs, function(f)
  read.csv(f, stringsAsFactors = FALSE, na.strings = "NA",
           colClasses = c(support = "character", support_audit = "character",
                          diag_codes = "character", warnings = "character",
                          messages = "character", error = "character"))))

parse_support <- function(s) {
  if (is.na(s)) return(NA_integer_)
  if (!nzchar(s)) return(integer())
  as.integer(strsplit(s, ";", fixed = TRUE)[[1L]])
}
truth_cache <- list()
truth_of <- function(dataset_id, p) {
  if (is.null(truth_cache[[dataset_id]]))
    truth_cache[[dataset_id]] <<- readRDS(file.path(truth_root, sprintf("p%04d", p),
                                                    paste0(dataset_id, ".rds")))$active
  truth_cache[[dataset_id]]
}

for (i in seq_len(nrow(rows))) {
  active <- truth_of(rows$dataset_id[i], rows$p[i])
  if (rows$status[i] %in% c("failed", "timeout", "not_run")) {
    rows$error_type[i] <- "failed"; rows$exact[i] <- FALSE
    next
  }
  s <- parse_support(rows$support[i])
  tp <- sum(s %in% active); fp <- length(s) - tp; fn <- length(active) - tp
  rows$tp[i] <- tp; rows$fp[i] <- fp; rows$fn[i] <- fn
  rows$exact[i] <- fp == 0 && fn == 0
  rows$error_type[i] <- if (fp == 0 && fn == 0) "exact" else if (fn == 0) "extra_only" else
    if (fp == 0) "missed_only" else "mixed"
  for (a in seq_along(active)) rows[[sprintf("sel_a%02d", a)]][i] <- active[a] %in% s
}
write.csv(rows, file.path(out_dir, "scored_rows.csv"), row.names = FALSE, na = "NA")

tab <- data.frame(dataset = rows$dataset_id, rule = rows$rule_id, role = rows$role,
                  status = rows$status, k = rows$k, TP = rows$tp, FP = rows$fp, FN = rows$fn,
                  exact = rows$exact, alpha = rows$alpha, index = rows$index,
                  diag_flag = rows$diag_flag, diag_codes = rows$diag_codes,
                  runtime_s = round(rows$runtime_s, 2), stringsAsFactors = FALSE)
write.csv(tab, file.path(out_dir, "dev_table.csv"), row.names = FALSE, na = "NA")
options(width = 200)
print(tab, right = FALSE, row.names = FALSE)
cat("\nExact recovery by rule (out of", length(unique(rows$dataset_id)), "datasets):\n")
print(tapply(rows$exact, rows$rule_id, sum))
