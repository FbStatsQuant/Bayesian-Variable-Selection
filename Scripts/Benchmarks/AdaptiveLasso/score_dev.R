#!/usr/bin/env Rscript
# score_dev.R: scoring step for the F3 dev test (master §IV.1.2 truth columns, error types).
# Separate from fitting: it is the only F3 script that opens the dev truth files.
#
# Usage: Rscript score_dev.R --results <out>/results/<run_id> --truth-root <dev>/truth
#                            --out <scored csv> [--sacct <csv: job_step,elapsed_s,maxrss_mb>]
# Writes the scored rule rows and prints the table
# (dataset, rule, status, k, TP, FP, FN, exact, runtime).

args <- commandArgs(trailingOnly = TRUE)
get_arg <- function(k, default = NULL) { i <- match(k, args); if (is.na(i)) default else args[i + 1L] }
results <- get_arg("--results"); truth_root <- get_arg("--truth-root"); out <- get_arg("--out")
if (is.null(results) || is.null(truth_root) || is.null(out)) stop("need --results, --truth-root, --out")

parse_key <- function(key) {
  if (is.na(key)) return(NA_integer_)
  if (!nzchar(key)) return(integer())
  as.integer(strsplit(key, ";", fixed = TRUE)[[1L]])
}

csvs <- list.files(results, pattern = "\\.csv$", recursive = TRUE, full.names = TRUE)
if (!length(csvs)) stop("no rule-row CSVs under ", results)
scored <- lapply(csvs, function(f) {
  r <- utils::read.csv(f, stringsAsFactors = FALSE, na.strings = "NA",
                       colClasses = c(support = "character", support_audit = "character",
                                      diag_codes = "character", warnings = "character",
                                      messages = "character", error = "character"))
  tr <- readRDS(file.path(truth_root, sprintf("p%04d", r$p[1L]), paste0(r$dataset_id[1L], ".rds")))
  active <- tr$active
  failed <- r$status %in% c("failed", "timeout", "not_run")
  for (i in seq_len(nrow(r))) {
    if (failed[i]) {
      r$tp[i] <- NA; r$fp[i] <- NA; r$fn[i] <- NA; r$exact[i] <- FALSE; r$error_type[i] <- "failed"
      next
    }
    s <- parse_key(r$support[i])
    r$tp[i] <- sum(s %in% active); r$fp[i] <- sum(!s %in% active); r$fn[i] <- sum(!active %in% s)
    r$exact[i] <- r$fp[i] == 0 && r$fn[i] == 0
    r$error_type[i] <- if (r$exact[i]) "exact" else if (r$fn[i] == 0) "extra_only" else
      if (r$fp[i] == 0) "missed_only" else "mixed"
    for (a in seq_along(active)) r[[sprintf("sel_a%02d", a)]][i] <- as.integer(active[a] %in% s)
  }
  r
})
scored <- do.call(rbind, scored)
scored <- scored[order(scored$p, scored$scenario, match(scored$rule_id, c("cv_min", "cv_1se", "ebic1", "ebic05"))), ]
utils::write.csv(scored, out, row.names = FALSE, na = "NA")

tab <- data.frame(dataset = scored$dataset_id, rule = scored$rule_id, role = scored$role,
                  status = scored$status, k = scored$k, TP = scored$tp, FP = scored$fp, FN = scored$fn,
                  exact = scored$exact, codes = scored$diag_codes,
                  runtime_s = round(scored$runtime_s, 2), stringsAsFactors = FALSE)
sacct <- get_arg("--sacct")
if (!is.null(sacct)) {
  sa <- utils::read.csv(sacct, stringsAsFactors = FALSE)
  tab$maxrss_mb <- sa$maxrss_mb[match(paste0(scored$dataset_id, "_", scored$scale_key), sa$case_id)]
}
print(tab, row.names = FALSE, right = FALSE)
prim <- scored[scored$role == "primary", ]
cat("\nprimary cv_min: exact", sum(prim$exact), "of", nrow(prim),
    "| failed", sum(prim$status == "failed"), "\n")
for (rid in c("cv_1se", "ebic1", "ebic05")) {
  z <- scored[scored$rule_id == rid, ]
  cat(rid, ": exact", sum(z$exact), "of", nrow(z), "| failed", sum(z$status == "failed"), "\n")
}
cat("written:", out, "\n")
