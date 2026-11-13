# b3_census_table.R -- leg B item B3: dispersion of island evidences against p and N on a frozen grid, from the
# records written by scripts/census_measure.R. One row per (p, N). Node and CPU are recorded per row; timings are
# never pooled across node types. Robust spread: 1.4826 * MAD of log Zhat_r.
# Usage: Rscript --vanilla b3_census_table.R DIR OUT.tsv   (DIR holds b3_p*/res/census_p*.rds)
a <- commandArgs(trailingOnly = TRUE)
rows <- list()
for (f in Sys.glob(file.path(a[1], "b3_p*/res/census_p*.rds"))) {
  r <- readRDS(f); cal <- r$calibration
  for (x in r$runs) {
    lz <- x$log_Z_r; m <- median(lz)
    rows[[length(rows) + 1]] <- data.frame(p = as.integer(r$meta$args$p), dataset = r$meta$dataset_id, node = r$meta$host,
      cpu_type = if (grepl("^bb", r$meta$host)) "sapphirerapids" else if (grepl("^bc", r$meta$host)) "cascadelake" else "other",
      core = substr(r$meta$core_key, 1, 12), H_cal = cal$H, cal_rebuilds = cal$rebuilds, cal_h = round(cal$seconds / 3600, 2),
      T = x$T, N = x$N, islands = x$islands_done, requested = x$islands_requested, status = x$status,
      sd_log_Z_r = round(sd(lz), 3), robust_sd = round(1.4826 * mad(lz), 3), median_log_Z_r = round(m, 2),
      max_minus_median = round(max(lz) - m, 2), R_eff = round(x$R_eff, 2), R_eff_share = round(x$R_eff / x$islands_done, 3),
      max_W = round(x$max_W, 3), island_s_median = round(median(x$island_seconds)), island_s_min = round(min(x$island_seconds)),
      island_s_max = round(max(x$island_seconds)), hpm_equals_truth = x$hpm_equals_truth, islands_same_best = length(unique(round(x$island_best, 8))) == 1,
      max_abs_pip_Z_minus_eq = signif(x$max_abs_diff, 3), sd_pip_r_max = signif(x$sd_pip_r_max, 3), pip_max_null = round(x$pip_Z_max_null, 3),
      min_ess_share = round(x$min_ess_share, 3), stringsAsFactors = FALSE)
  }
}
d <- do.call(rbind, rows); d <- d[order(d$p, d$N), ]
write.table(d, a[2], sep = "\t", quote = FALSE, row.names = FALSE); print(d[, c("p", "N", "node", "islands", "status", "sd_log_Z_r", "robust_sd", "max_minus_median", "R_eff", "max_W", "island_s_median", "cal_h", "cal_rebuilds", "T")])
