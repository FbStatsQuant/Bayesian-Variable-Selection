#!/usr/bin/env Rscript
# Compares two dev runs of A3 case by case: the rule-row fields that do not depend on timing or
# provenance (status, support, k, diag_flag, diag_codes, n_warnings, rng_after, input hashes) and
# the saved per-coefficient table `coef` (identical()).
# Used after the Sol-review fixes to show that the fixes left the dev outputs unchanged.
# Usage: Rscript tests/compare_dev_runs.R <outroot> <run_id_a> <run_id_b>
args <- commandArgs(trailingOnly = TRUE)
root <- args[1]; ra <- args[2]; rb <- args[3]
fa <- sort(list.files(file.path(root, "results", ra), pattern = "^A3\\.csv$", recursive = TRUE))
fb <- sort(list.files(file.path(root, "results", rb), pattern = "^A3\\.csv$", recursive = TRUE))
stopifnot(identical(fa, fb), length(fa) > 0L)
cols <- c("case_id", "rule_id", "role", "status", "support", "k", "diag_flag", "diag_codes",
          "n_warnings", "rng_after", "x_sha256", "y_sha256", "fold_sha256", "method_seed")
same_all <- TRUE
for (f in fa) {
  a <- utils::read.csv(file.path(root, "results", ra, f), stringsAsFactors = FALSE, colClasses = c(support = "character"))
  b <- utils::read.csv(file.path(root, "results", rb, f), stringsAsFactors = FALSE, colClasses = c(support = "character"))
  ca <- readRDS(file.path(root, "results", ra, sub("csv$", "rds", f)))$diagnostics$coef
  cb <- readRDS(file.path(root, "results", rb, sub("csv$", "rds", f)))$diagnostics$coef
  rows_same <- identical(a[, cols], b[, cols]); coef_same <- identical(ca, cb)
  same_all <- same_all && rows_same && coef_same
  cat(sprintf("%-28s rule rows identical: %s; coef table identical: %s\n", basename(dirname(f)), rows_same, coef_same))
}
cat(sprintf("\n%d cases compared; all identical: %s\n", length(fa), same_all))
quit(save = "no", status = if (same_all) 0L else 1L)
