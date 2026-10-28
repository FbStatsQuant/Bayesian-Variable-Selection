#!/usr/bin/env Rscript
# compare_canary.R -- production canaries (master §IV.3): the canary outputs must reproduce the dev
# reference outputs bit for bit in every scientific field (rule rows' selection, criterion and flag
# columns; beta; path, candidate and convergence diagnostics). Provenance, timing and host fields differ
# by construction and are not compared.
# Usage: Rscript compare_canary.R <reference_root> <canary_root> <dataset_ids, comma-separated> <out_file>
args <- commandArgs(trailingOnly = TRUE)
ref <- args[1L]; can <- args[2L]; ids <- strsplit(args[3L], ",", fixed = TRUE)[[1L]]; out <- args[4L]
cols <- c("rule_id", "role", "status", "support", "support_audit", "k", "converged", "diag_flag",
          "diag_codes", "error", "lambda", "rss", "crit_value", "path_index", "k_valid_max", "k_path_max")
diag_fields <- c("path", "candidates", "convex_min", "discarded_intercept", "n_lambda_returned",
                 "internal_scale", "internal_gamma", "zmax", "lambda_rel_err", "total_iter", "gate_failures")
res <- character(); bad <- 0L
for (d in ids) for (mid in c("F4", "F4_SCAD")) {
  pp <- strsplit(d, "_", fixed = TRUE)[[1L]][2L]
  f <- file.path(c(ref, can), pp, paste0(d, "_c100"), paste0(mid, ".rds"))
  if (!all(file.exists(f))) { res <- c(res, paste(d, mid, "MISSING")); bad <- bad + 1L; next }
  a <- readRDS(f[1]); b <- readRDS(f[2])
  ok <- c(rows = identical(a$rows[, cols], b$rows[, cols]), beta = identical(a$beta, b$beta),
          converged = identical(a$converged, b$converged),
          vapply(diag_fields, function(x) identical(a$diagnostics[[x]], b$diagnostics[[x]]), TRUE))
  res <- c(res, sprintf("%s %s %s", d, mid,
                        if (all(ok)) "IDENTICAL" else paste("DIFFERS:", paste(names(ok)[!ok], collapse = ","))))
  if (!all(ok)) bad <- bad + 1L
}
writeLines(c(res, sprintf("canary pairs differing or missing: %d", bad)), out); cat(res, sep = "\n")
quit(save = "no", status = if (bad) 1L else 0L)
