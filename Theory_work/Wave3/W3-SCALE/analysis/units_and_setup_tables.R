# units_and_setup_tables.R -- auditable sources for numbers quoted in CHECKPOINT_1.md and DESIGN_v1.md:
#  (1) per-unit calibration / stage table of the v3.1 bit-identity records (rebuild counts, stage counts, share of
#      calibration in calibration + final time, LS0 preflight charge, peak memory);
#  (2) setup-only comparison v3.1 vs v3.2-dev (times by component, peak resident memory, hash equality, LS0 charge).
# Memory is reported in GiB (2^30 bytes): VmHWM is in kB = 2^10 bytes.
# Usage: Rscript --vanilla units_and_setup_tables.R RECS_DIR SETUP_DIR_A SETUP_DIR_C OUT_PREFIX
`%||%` <- function(a, b) if (is.null(a)) b else a
a <- commandArgs(trailingOnly = TRUE)
fs <- list.files(a[1], pattern = "__v31[.]rec[.]rds$", full.names = TRUE)
rows <- lapply(fs, function(f) { r <- readRDS(f); cs <- r$calibration_summary; if (is.null(cs)) return(NULL)
  data.frame(unit = sub("^[a-z]+:", "", r$unit), p = r$scalars$p, tiers = length(cs),
    rebuilds_tier0 = cs[[1]]$rebuilds, T_pilot_tier0 = cs[[1]]$T_pilot, T_grid_tier0 = cs[[1]]$T_grid %||% NA,
    rebuilds_tier1 = if (length(cs) > 1) cs[[2]]$rebuilds else NA, T_pilot_tier1 = if (length(cs) > 1) cs[[2]]$T_pilot else NA,
    T_final = r$scalars$T_final, calibration_s = r$timings$calibration, final_s = r$timings$final, setup_s = r$timings$setup_total, wall_s = r$wall_s,
    cal_share = r$timings$calibration / (r$timings$calibration + r$timings$final),
    ls0_charge_s = r$preflight$ls0_worst_case$est_seconds, allocation_s = if (r$scalars$p == 500) 6300 else if (r$scalars$p == 1000) 24000 else 7200,
    preflight_exceeds = r$preflight$exceeds, peak_GiB = r$scalars$peak_memory_kb / 2^20,
    triggers_tier0 = paste(names(cs[[1]]$triggers)[unlist(cs[[1]]$triggers)], collapse = ","), stringsAsFactors = FALSE) })
t <- do.call(rbind, rows); t <- t[order(t$p, t$unit), ]
write.table(format(t, digits = 4), paste0(a[4], "_units_calibration.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
s <- do.call(rbind, lapply(c(500, 1000), function(pp) { d <- t[t$p == pp & t$tiers == 1 & grepl("^p", t$unit), ]
  data.frame(p = pp, fits_tier0_only = nrow(d), rebuilds_median = median(d$rebuilds_tier0), rebuilds_min = min(d$rebuilds_tier0), rebuilds_max = max(d$rebuilds_tier0),
    T_pilot_min = min(d$T_pilot_tier0), T_pilot_max = max(d$T_pilot_tier0), T_final_median = median(d$T_final), T_final_min = min(d$T_final), T_final_max = max(d$T_final),
    cal_share_median = median(d$cal_share), cal_share_min = min(d$cal_share), cal_share_max = max(d$cal_share), wall_s_median = median(d$wall_s),
    ls0_charge_s_max = max(t$ls0_charge_s[t$p == pp]), allocation_s = d$allocation_s[1], peak_GiB_max = max(t$peak_GiB[t$p == pp])) }))
write.table(format(s, digits = 4), paste0(a[4], "_units_calibration_summary.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
print(format(t(s), digits = 4), quote = FALSE)
for (k in 2:3) {
  d <- a[k]; tag <- c("", "roundA", "roundC")[k]; out <- list()
  for (pp in c(5000, 10000, 20000)) for (l in c("v31", "v32")) {
    f <- file.path(d, sprintf("setup_p%d_%s.rds", pp, l)); if (!file.exists(f)) next
    p <- readRDS(f); ph <- setNames(p$phases$seconds, p$phases$phase); pk <- setNames(p$phases$peak_kb, p$phases$phase) / 2^20
    o <- readRDS(file.path(d, sprintf("setup_p%d_%s.rds", pp, if (l == "v31") "v32" else "v31")))
    out[[length(out) + 1]] <- data.frame(round = tag, p = pp, core = l, gram_s = ph[["context_gram"]], gram_copied_to_R = !is.null(p$gram_sha),
      blocks_s = p$setup$seconds[["blocks"]], tables_s = p$setup$seconds[["tables"]], start_s = p$setup$seconds[["start"]], graph_s = p$setup$seconds[["neighbours"]],
      setup_s = ph[["setup_total"]], peak_setup_GiB = pk[["setup_total"]], peak_gram_GiB = pk[["context_gram"]],
      dense_24p2_GiB = 24 * pp^2 / 2^30, dense_16p2_GiB = 16 * pp^2 / 2^30,
      tables_identical = identical(p$tables_sha, o$tables_sha), setup_objects_identical = identical(p$setup_hash, o$setup_hash),
      gram_identical = if (is.null(p$gram_sha)) NA else identical(p$gram_sha, o$gram_sha), routes_identical = identical(p$numerical_routes, o$numerical_routes),
      ls0_charge_h_at_24h = (p$preflight$job_mem_24h$ls0_worst_case$est_seconds %||% NA) / 3600, preflight_refuses_24h = p$preflight$job_mem_24h$exceeds,
      s_K_us = 1e6 * p$preflight$seconds_per_size_K_score, stringsAsFactors = FALSE)
  }
  x <- do.call(rbind, out)
  write.table(format(x, digits = 4), paste0(a[4], "_setup_compare_", tag, ".tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
  print(format(x[, c("round", "p", "core", "gram_s", "blocks_s", "tables_s", "graph_s", "setup_s", "peak_setup_GiB", "ls0_charge_h_at_24h", "preflight_refuses_24h")], digits = 4), row.names = FALSE)
}
