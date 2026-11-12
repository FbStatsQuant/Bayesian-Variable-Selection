# pip_weighting.R -- numbers for the reserved owner question (ii): equal-weight PIP (v3_run.R:162, the shipped
# primary) versus evidence-weighted PIP (sum_r W_r pip_r, W_r = Zhat_r / sum_s Zhat_s) on the saved v3.1 fits of the
# bit-identity round. Nothing is decided here; the table only shows how far the two estimators are apart at R = 4.
# Usage: Rscript --vanilla pip_weighting.R FITS_DIR OUT.tsv
a <- commandArgs(trailingOnly = TRUE)
fits <- list.files(a[1], pattern = "__v31\\.fit\\.rds$", recursive = TRUE, full.names = TRUE)
rows <- lapply(fits, function(f) {
  x <- readRDS(f); id <- sub("__v31\\.fit\\.rds$", "", basename(f))
  lz <- x$log_Z_r; w <- exp(lz - max(lz)); w <- w / sum(w)
  P <- x$pip_r; eq <- rowMeans(P); zw <- drop(P %*% w)
  se_eq <- apply(P, 1, stats::sd) / sqrt(ncol(P))
  j <- which.max(abs(zw - eq))
  data.frame(unit = id, p = x$p, tier = x$settings$tier, sd_log_Z_r = stats::sd(lz), max_W = max(w), R_eff = 1 / sum(w^2),
             max_abs_diff = max(abs(zw - eq)), diff_over_se = abs(zw[j] - eq[j]) / max(se_eq[j], 1e-300),
             max_island_spread = max(apply(P, 1, function(v) diff(range(v)))),
             mpm_eq_size = sum(eq > 0.5), mpm_same = identical(which(eq > 0.5), which(zw > 0.5)),
             n_pip_cross_half = sum((eq > 0.5) != (zw > 0.5)), stringsAsFactors = FALSE)
})
tab <- do.call(rbind, rows); tab <- tab[order(tab$p, -tab$sd_log_Z_r), ]
write.table(format(tab, digits = 3), a[2], sep = "\t", quote = FALSE, row.names = FALSE)
print(format(tab, digits = 3), row.names = FALSE)
cat(sprintf("fits %d; MPM identical under both weightings in %d; max |PIP_Z - PIP_eq| over all fits %.4f; median %.5f; R_eff/4 min %.3f\n",
            nrow(tab), sum(tab$mpm_same), max(tab$max_abs_diff), stats::median(tab$max_abs_diff), min(tab$R_eff) / 4))
