#!/usr/bin/env Rscript
# compare_runs.R: canary comparison of two F5 result trees. The scientific content (selection
# columns of the rule rows; beta; the saved path, coefficients and candidates) must be
# bit-identical; timing and provenance columns are excluded.
# Usage: Rscript --vanilla tools/compare_runs.R <results_dir_reference> <results_dir_new>
a <- commandArgs(trailingOnly = TRUE)
sci <- c("case_id", "rule_id", "role", "status", "k", "support", "support_audit", "diag_flag",
         "diag_codes", "converged", "rss", "crit_value", "k_valid_max", "k_path_max",
         "x_sha256", "y_sha256", "fold_sha256", "data_seed", "fold_seed", "method_seed")
load_tree <- function(d) {
  f <- sort(list.files(d, pattern = "^F5[.]rds$", recursive = TRUE, full.names = TRUE))
  stats::setNames(lapply(f, readRDS), basename(dirname(f)))
}
A <- load_tree(a[1]); B <- load_tree(a[2])
common <- intersect(names(A), names(B))
cat("cases: reference", length(A), " new", length(B), " common", length(common), "\n")
# Coverage first: both sets non-empty, unique and identical (Astra prod follow-up, point 8).
coverage_ok <- length(A) > 0L && !anyDuplicated(names(A)) && !anyDuplicated(names(B)) &&
  setequal(names(A), names(B))
if (!coverage_ok) cat("COVERAGE MISMATCH: only in reference:", setdiff(names(A), names(B)),
                      "; only in new:", setdiff(names(B), names(A)), "\n")
bad <- character()
for (cid in common) {
  x <- A[[cid]]; y <- B[[cid]]
  same <- identical(x$rows[sci], y$rows[sci]) && identical(x$beta, y$beta) &&
    identical(x$diagnostics$path, y$diagnostics$path) &&
    identical(x$diagnostics$coefficients, y$diagnostics$coefficients) &&
    identical(x$diagnostics$candidates, y$diagnostics$candidates)
  if (!same) bad <- c(bad, cid)
}
ok <- coverage_ok && !length(bad)
cat("CANARY", if (ok) "IDENTICAL" else paste("FAILED; differing cases:", paste(bad, collapse = ",")), "\n")
quit(save = "no", status = if (ok) 0L else 1L)
