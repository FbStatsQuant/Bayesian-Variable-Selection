#!/usr/bin/env Rscript
# pilot_diag_c050.R -- diagnostics-only summary of a c050 pilot run (BRIEF_C050_ENG task 5).
# Reads the rule rows (<m>.csv) of the listed cases. Truth-dependent columns (tp, fp, fn, exact,
# error_type, sel_aNN) are dropped on reading and never summarised: no recovery is computed.
# Reads results only (never inputs, truth or scoring). Infrastructure tool; not part of any fit.
#
#   Rscript --vanilla pilot_diag_c050.R <results_dir> <dataset_ids,> <method_ids,> <scale_key> <kmax> <out_txt>

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 6L) stop("usage: pilot_diag_c050.R <results_dir> <ids,> <methods,> <scale_key> <kmax> <out_txt>")
dir <- args[1]; ids <- strsplit(args[2], ",", fixed = TRUE)[[1]]; mids <- strsplit(args[3], ",", fixed = TRUE)[[1]]
sk <- args[4]; kmax <- as.integer(args[5]); out_txt <- args[6]
TRUTH <- c("tp", "fp", "fn", "exact", "error_type")

rows <- list(); missing <- character(0)
for (id in ids) for (m in mids) {
  pp <- sub("^(p[0-9]{4})_.*$", "\\1", id)
  f <- file.path(dir, pp, paste0(id, "_", sk), paste0(m, ".csv"))
  if (!file.exists(f) || !file.exists(sub("\\.csv$", ".done", f))) { missing <- c(missing, f); next }
  r <- read.csv(f, colClasses = "character", check.names = FALSE, na.strings = character(0))
  r <- r[, !(names(r) %in% TRUTH) & !grepl("^sel_a[0-9]+$", names(r)), drop = FALSE]
  rows[[length(rows) + 1L]] <- r
}
keep <- c("dataset_id", "case_id", "p", "scenario", "scale_key", "method_id", "rule_id", "role", "status",
          "converged", "diag_flag", "diag_codes", "n_warnings", "warnings", "error", "k", "runtime_s")
tab <- do.call(rbind, lapply(rows, function(r) r[, intersect(keep, names(r)), drop = FALSE]))

con <- file(out_txt, "w")
w <- function(...) { cat(..., "\n", sep = ""); cat(..., "\n", sep = "", file = con) }
w("pilot_diag_c050  results=", dir, "  scale=", sk, "  kmax=", kmax)
w("cases expected ", length(ids) * length(mids), ", with .csv and .done ", length(rows),
  if (length(missing)) paste0("  MISSING: ", paste(basename(dirname(missing)), collapse = ",")) else "")
w("scale_key values in rows: ", paste(unique(tab$scale_key), collapse = ","))
for (key in unique(paste(tab$method_id, tab$rule_id, sep = " / "))) {
  s <- tab[paste(tab$method_id, tab$rule_id, sep = " / ") == key, ]
  k <- suppressWarnings(as.integer(s$k)); codes <- unlist(strsplit(s$diag_codes[s$diag_codes != "NA"], ";", fixed = TRUE))
  w(""); w("== ", key, " (", s$role[1], "), ", nrow(s), " rows")
  w("  status: ", paste(names(table(s$status)), table(s$status), sep = "=", collapse = " "))
  w("  converged: ", paste(names(table(s$converged)), table(s$converged), sep = "=", collapse = " "))
  w("  diag_flag: ", paste(names(table(s$diag_flag)), table(s$diag_flag), sep = "=", collapse = " "))
  w("  diag_codes: ", if (length(codes)) paste(names(table(codes)), table(codes), sep = "=", collapse = " ") else "(none)")
  w("  n_warnings total: ", sum(as.integer(s$n_warnings), na.rm = TRUE),
    "; distinct warnings: ", paste(unique(s$warnings[!s$warnings %in% c("", "NA")]), collapse = " | "))
  w("  errors: ", paste(unique(s$error[!s$error %in% c("", "NA")]), collapse = " | "))
  w("  k: min ", min(k, na.rm = TRUE), " median ", median(k, na.rm = TRUE), " max ", max(k, na.rm = TRUE),
    " NA ", sum(is.na(k)), "; cap hits (k >= ", kmax, "): ", sum(k >= kmax, na.rm = TRUE))
  w("  k by case: ", paste(sub("_c[0-9]+$", "", s$case_id), k, sep = ":", collapse = " "))
}
rt <- unique(tab[, c("case_id", "method_id", "runtime_s")]); rt$runtime_s <- as.numeric(rt$runtime_s)
w(""); w("runtime_s per case x method (fit time recorded by the runner):")
for (m in unique(rt$method_id)) { x <- rt$runtime_s[rt$method_id == m]
  w(sprintf("  %-8s max %.1f  mean %.1f  (n %d)", m, max(x), mean(x), length(x))) }
for (pp in c("p0500", "p1000")) { x <- rt[grepl(paste0("^", pp), rt$case_id), ]
  if (nrow(x)) w(sprintf("  %s all methods: max %.1f  mean %.1f", pp, max(x$runtime_s), mean(x$runtime_s))) }
close(con)
write.csv(tab, sub("\\.txt$", "_rows.csv", out_txt), row.names = FALSE)
