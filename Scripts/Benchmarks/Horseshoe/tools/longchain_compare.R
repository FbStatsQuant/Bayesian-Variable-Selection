#!/usr/bin/env Rscript
# longchain_compare.R -- per-fit comparison of a longer-chain A3 fit (8 x budget, PREREG_c050 R6) with
# the production fit of the same case (diagnostics only; reads no truth). Writes one CSV row:
# ESS of log tau^2 / log sigma^2, split R-hat, min ESS of ci95-selected coefficients, flags of both
# fits, whether ess_tau (and ess_ci95) clears, ci95 and km2 supports of both, Jaccard (J(empty, empty)
# = 1; NA if either fit failed), number of differing decisions, draws and runtime of both.
# Usage: Rscript longchain_compare.R <long A3.rds> <production A3.rds> <out.csv>
a <- commandArgs(trailingOnly = TRUE)
L <- readRDS(a[1]); P <- readRDS(a[2])
stopifnot(identical(L$case$case_id, P$case$case_id), identical(L$input$y_sha256, P$input$y_sha256),
          identical(as.integer(L$case$method_seed), as.integer(P$case$method_seed)))
sup <- function(r, rule) {
  x <- r$rows[r$rows$rule_id == rule, ]
  if (!nrow(x) || x$status == "failed" || is.na(x$support)) return(NULL)
  if (x$support == "") integer(0) else as.integer(strsplit(x$support, ";")[[1]])
}
jac <- function(a, b) if (is.null(a) || is.null(b)) NA_real_ else if (!length(union(a, b))) 1 else
  length(intersect(a, b)) / length(union(a, b))
ndiff <- function(a, b) if (is.null(a) || is.null(b)) NA_integer_ else length(setdiff(union(a, b), intersect(a, b)))
codes <- function(r) { c <- r$rows$diag_codes[1]; if (is.na(c)) "" else c }
has <- function(r, k) k %in% strsplit(codes(r), ";")[[1]]
num <- function(x) if (is.null(x) || !length(x)) NA_real_ else as.numeric(x)
out <- data.frame(
  case_id = L$case$case_id, scale_key = L$case$scale_key, status_prod = P$rows$status[1], status_long = L$rows$status[1],
  draws_prod = length(P$diagnostics$trace_log_tau2), draws_long = length(L$diagnostics$trace_log_tau2),
  ess_log_tau2_prod = num(P$diagnostics$ess_log_tau2), ess_log_tau2_long = num(L$diagnostics$ess_log_tau2),
  ess_log_sigma2_prod = num(P$diagnostics$ess_log_sigma2), ess_log_sigma2_long = num(L$diagnostics$ess_log_sigma2),
  rhat_log_tau2_prod = num(P$diagnostics$split_rhat_log_tau2), rhat_log_tau2_long = num(L$diagnostics$split_rhat_log_tau2),
  min_ess_ci95_prod = num(P$diagnostics$min_ess_ci95), min_ess_ci95_long = num(L$diagnostics$min_ess_ci95),
  codes_prod = codes(P), codes_long = codes(L),
  ess_tau_prod = has(P, "ess_tau"), ess_tau_long = has(L, "ess_tau"),
  ess_tau_cleared = has(P, "ess_tau") && !has(L, "ess_tau") && L$rows$status[1] != "failed",
  ess_ci95_prod = has(P, "ess_ci95"), ess_ci95_long = has(L, "ess_ci95"),
  k_ci95_prod = length(sup(P, "ci95")), k_ci95_long = length(sup(L, "ci95")),
  k_km2_prod = length(sup(P, "km2")), k_km2_long = length(sup(L, "km2")),
  jaccard_ci95 = jac(sup(P, "ci95"), sup(L, "ci95")), n_differ_ci95 = ndiff(sup(P, "ci95"), sup(L, "ci95")),
  jaccard_km2 = jac(sup(P, "km2"), sup(L, "km2")), n_differ_km2 = ndiff(sup(P, "km2"), sup(L, "km2")),
  support_ci95_prod = paste(sup(P, "ci95"), collapse = ";"), support_ci95_long = paste(sup(L, "ci95"), collapse = ";"),
  support_km2_prod = paste(sup(P, "km2"), collapse = ";"), support_km2_long = paste(sup(L, "km2"), collapse = ";"),
  runtime_prod_s = round(num(P$runtime_s), 1), runtime_long_s = round(num(L$runtime_s), 1),
  source_sha256_long = L$rows$source_sha256[1], stringsAsFactors = FALSE)
dir.create(dirname(a[3]), recursive = TRUE, showWarnings = FALSE)
tmp <- paste0(a[3], ".tmp.", Sys.getpid())
utils::write.csv(out, tmp, row.names = FALSE)
if (!file.rename(tmp, a[3])) stop("rename failed: ", a[3])
print(out[, c("case_id", "ess_log_tau2_prod", "ess_log_tau2_long", "ess_tau_cleared", "k_ci95_prod", "k_ci95_long", "jaccard_ci95")], row.names = FALSE)
