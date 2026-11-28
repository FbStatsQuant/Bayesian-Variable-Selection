# stage_readback.R -- P1M G0 Part S read-back: stage_p*.rds -> small TSV tables (no core needed; base R only).
# Usage: Rscript --vanilla stage_readback.R OUTDIR stage_p5000.rds [stage_p10000.rds ...]
# Writes into OUTDIR:
#   g0_stage_long.tsv        one row per (p, island, stage): phi, log increment, cum log Z, ESS share, distinct counts, moves
#   g0_stage_dispersion.tsv  one row per (p, stage): mean / variance over the finished islands of the log increment,
#                            variance of cum log Z, ESS shares, gibbs_state_changes per particle
#   g0_islands.tsv           one row per (p, island): log Z_r, seconds, partial, min ESS share, the stage with the
#                            largest |log increment - stage mean|
#   g0_runs.tsv              one row per p: status, islands done, sd(log Z_r), calibration (T, rebuilds, hours), store size,
#                            log sum e^F, HPM = truth, B3 line-up, peak memory, node
#   g0_calib_stage_long.tsv  diagnostic-island stage tables of every calibration iteration (rows tagged by iteration)
args <- commandArgs(trailingOnly = TRUE); stopifnot(length(args) >= 2)
out <- args[1]; dir.create(out, showWarnings = FALSE, recursive = TRUE)
long <- list(); disp <- list(); isl <- list(); runs <- list(); cal <- list()
for (f in args[-1]) {
  r <- readRDS(f); p <- r$meta$budgets$p; fin <- r$final
  if (!is.null(fin)) {
    for (i in seq_along(fin$stage_tables)) { d <- fin$stage_tables[[i]]; if (is.null(d)) next
      long[[length(long) + 1]] <- cbind(p = p, island = i, d) }
    if (!is.null(fin$stage_dispersion)) disp[[length(disp) + 1]] <- cbind(p = p, islands = fin$islands_done, fin$stage_dispersion)
    sd_tab <- fin$stage_dispersion
    for (i in seq_along(fin$stage_tables)) { d <- fin$stage_tables[[i]]; if (is.null(d)) next
      dev <- if (!is.null(sd_tab)) abs(d$log_increment[seq_len(nrow(sd_tab))] - sd_tab$mean_inc) else NA
      isl[[length(isl) + 1]] <- data.frame(p = p, island = i, log_Z_r = fin$islands[[i]]$log_Z, partial = fin$island_partial[i],
        seconds = fin$island_seconds[i], T = nrow(d), min_ess_share = min(d$ess_share),
        stage_max_dev = if (all(is.na(dev))) NA else which.max(dev), max_dev = if (all(is.na(dev))) NA else max(dev, na.rm = TRUE)) }
  }
  c0 <- r$calibration
  if (!is.null(c0)) for (it in c0$iterations) for (i in seq_along(it$stage_tables)) { d <- it$stage_tables[[i]]; if (is.null(d)) next
    cal[[length(cal) + 1]] <- cbind(p = p, iteration = it$iteration, island = i, d) }
  st <- fin$store
  runs[[length(runs) + 1]] <- data.frame(p = p, node = r$meta$host, cpu = r$meta$cpu, status = r$status,
    final_status = if (is.null(fin)) NA else fin$status, islands_requested = if (is.null(fin)) NA else fin$islands_requested,
    islands_done = if (is.null(fin)) NA else fin$islands_done, sd_log_Z_r = if (is.null(fin)) NA else fin$sd_log_Z_r,
    sum_var_inc = if (is.null(fin$stage_dispersion)) NA else sum(fin$stage_dispersion$var_inc),
    T_grid = c0$T_grid, cal_rebuilds = c0$rebuilds, cal_hours = c0$seconds / 3600,
    island_hours_mean = if (is.null(fin)) NA else mean(fin$island_seconds) / 3600,
    store_entries = if (is.null(st)) NA else length(st$F), store_capacity = if (is.null(st)) NA else st$capacity,
    log_sum_exp_F = if (is.null(st)) NA else st$log_sum_exp_F, hpm_equals_truth = if (is.null(fin)) NA else fin$hpm_equals_truth,
    b3_grid_identical = if (is.null(r$b3_lineup)) NA else r$b3_lineup$grid_identical,
    b3_log_Z_r_identical = if (is.null(r$b3_lineup)) NA else r$b3_lineup$log_Z_r_identical,
    b3_islands_compared = if (is.null(r$b3_lineup)) NA else r$b3_lineup$islands_compared,
    peak_gib = if (is.null(r$meta$peak_gib)) NA else r$meta$peak_gib, total_hours = if (is.null(r$meta$total_seconds)) NA else r$meta$total_seconds / 3600)
}
w <- function(x, name) if (length(x)) { d <- do.call(rbind, x); write.table(d, file.path(out, name), sep = "\t", quote = FALSE, row.names = FALSE); cat(name, nrow(d), "rows\n") }
w(long, "g0_stage_long.tsv"); w(disp, "g0_stage_dispersion.tsv"); w(isl, "g0_islands.tsv"); w(runs, "g0_runs.tsv"); w(cal, "g0_calib_stage_long.tsv")
