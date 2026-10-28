#!/usr/bin/env Rscript
# conditioning_diag.R: diagnostics only (Astra prod finding 10). For every saved F5 path
# support, the condition number of X_S (ratio of extreme singular values) and the ratios of
# the observed RSS and stationarity discrepancies to their tolerances. Reads inputs/ only.
# Usage: Rscript --vanilla tools/conditioning_diag.R <results_dir> <inputs_root>
a <- commandArgs(trailingOnly = TRUE)
f <- sort(list.files(a[1], pattern = "^F5[.]rds$", recursive = TRUE, full.names = TRUE))
out <- do.call(rbind, lapply(f, function(fi) {
  o <- readRDS(fi); pa <- o$diagnostics$path; if (is.null(pa)) return(NULL)
  d <- readRDS(file.path(a[2], sprintf("p%04d", o$case$p), paste0(o$case$dataset_id, ".rds")))
  X <- d$X; n <- nrow(X); F5 <- o$settings$F5
  kap <- vapply(pa$key, function(k) { if (!nzchar(k)) return(1); s <- as.integer(strsplit(k, ";")[[1]])
    sv <- svd(X[, s, drop = FALSE], nu = 0, nv = 0)$d; max(sv) / min(sv) }, 0)
  rel <- function(a, b) abs(a - b) / pmax(1, abs(a), abs(b))
  data.frame(case_id = o$case$case_id,
    max_kappa = max(kap), kappa_at_k100 = kap[length(kap)],
    max_ratio_rss_ols = max(rel(pa$rss_reconstructed, pa$rss_ols)) / F5$rss_rel_tol,
    max_ratio_rss_dev = max(rel(pa$rss_reconstructed, 2 * n * pa$dev + n * o$diagnostics$response_center^2)) / F5$rss_rel_tol,
    max_ratio_stationarity = max(pa$stationarity) / o$diagnostics$stat_tol,
    max_ratio_intercept = max(abs(pa$intercept)) / F5$intercept_tol)
}))
print(format(out, digits = 3), row.names = FALSE)
cat("overall: max kappa", signif(max(out$max_kappa), 3), "; max discrepancy/tolerance ratio",
    signif(max(out[, grep("ratio", names(out))]), 3), "\n")
