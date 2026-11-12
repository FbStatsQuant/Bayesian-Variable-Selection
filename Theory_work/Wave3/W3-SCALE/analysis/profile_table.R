# profile_table.R -- tables of the v3.1 profile (leg A item 1) from the profile records written by profile_fit.R.
# Usage: Rscript --vanilla profile_table.R DIR OUT_PREFIX   (DIR holds <run>/res/prof_*.rds)
`%||%` <- function(a, b) if (is.null(a)) b else a
a <- commandArgs(trailingOnly = TRUE)
files <- list.files(a[1], pattern = "^prof_p.*\\.rds$", recursive = TRUE, full.names = TRUE)
files <- files[!grepl("_fit\\.rds$", files)]
ord <- order(vapply(files, function(f) readRDS(f)$budgets$p %||% 0, 0)); files <- files[ord]
phase_rows <- list(); stage_rows <- list(); cost_rows <- list()
for (f in files) {
  p <- readRDS(f); b <- p$budgets; mode <- p$meta$args$mode
  ph <- setNames(p$phases$seconds, p$phases$phase); pk <- setNames(p$phases$peak_kb / 1024, p$phases$phase)
  g <- function(v, k) if (k %in% names(v)) v[[k]] else NA
  cal <- p[["calibration"]]; fin <- p[["final"]]
  phase_rows[[length(phase_rows) + 1]] <- data.frame(
    p = b$p, mode = mode, status = p$status %||% "running", N = if (mode == "full") (fin$N %||% b$N0) else as.integer(p$meta$args$n_island),
    preprocess_s = g(ph, "preprocess"), gram_s = g(ph, "context_gram"), setup_s = g(ph, "setup_total"),
    blocks_s = p$setup$seconds[["blocks"]], tables_s = p$setup$seconds[["tables"]], start_s = p$setup$seconds[["start"]], graph_s = p$setup$seconds[["neighbours"]],
    calibration_s = g(ph, "calibration"), pilot_island_s = g(ph, "pilot_island"), final_s = if (mode == "full") g(ph, "final_run") else g(ph, "final_island"),
    local_s = if (mode == "full") fin$timings$local %||% NA else fin$seconds_local %||% NA, ls0_s = if (mode == "full") fin$timings$ls0 %||% NA else fin$seconds_ls0 %||% NA,
    total_s = p$total_seconds %||% NA,
    peak_gram_MB = g(pk, "context_gram"), peak_setup_MB = g(pk, "setup_total"), peak_cal_MB = if (mode == "full") g(pk, "calibration") else g(pk, "pilot_island"),
    peak_final_MB = if (mode == "full") g(pk, "final_run") else g(pk, "final_island"), peak_all_MB = max(pk, na.rm = TRUE),
    v31_preflight_refuses_24h = p$preflight$job_mem_24h$exceeds, v31_ls0_charge_h = (p$preflight$job_mem_24h$ls0_worst_case$est_seconds %||% NA) / 3600,
    s_K_us = 1e6 * p$preflight$seconds_per_size_K_score, mem_model_GB = p$preflight$default_8g_24h$est_bytes / 2^30, stringsAsFactors = FALSE)
  isl <- if (mode == "full") fin$islands else list(fin[["island"]])
  tiers <- cal$tiers
  stage_rows[[length(stage_rows) + 1]] <- data.frame(
    p = b$p, mode = mode, ell = b$ell, J = p$setup$J,
    tier_final = cal$tier_final %||% NA, escalated = cal$escalated %||% NA,
    T_pilot = if (length(tiers)) paste(vapply(tiers, function(t) t$T_pilot, 0L), collapse = "/") else (p$pilot$T %||% NA),
    rebuilds_I = if (length(tiers)) paste(vapply(tiers, function(t) t$rebuilds %||% NA_integer_, 0L), collapse = "/") else NA,
    converged = if (length(tiers)) paste(vapply(tiers, function(t) isTRUE(t$converged), TRUE), collapse = "/") else NA,
    T_final = fin$T %||% NA, V_size = if (length(tiers)) max(unlist(lapply(tiers, function(t) t$V_sizes))) else (p$grid$V_size %||% NA),
    grid_build_s = if (length(tiers)) mean(unlist(lapply(tiers, function(t) vapply(t$grids, function(x) x$seconds, 0)))) else (p$grid$seconds %||% NA),
    sd_log_Z_r = fin$sd_log_Z_r %||% NA, hpm_equals_truth = fin$hpm_equals_truth %||% NA, stringsAsFactors = FALSE)
  # cost per elementary step (one step of a round of m = p + B + 2 labels, per particle), from the final island(s)
  if (length(isl) && !is.null(isl[[1]])) {
    m <- b$p + b$B + 2; N <- phase_rows[[length(phase_rows)]]$N; L <- b$L; Hm <- 4
    br <- mean(vapply(isl, function(x) x$seconds[["bridge"]] / x$T, 0)); bu <- mean(vapply(isl, function(x) x$seconds[["burn_in"]] / L, 0))
    me <- mean(vapply(isl, function(x) x$seconds[["measured"]] / Hm, 0))
    cc <- fin$cache
    cost_rows[[length(cost_rows) + 1]] <- data.frame(p = b$p, N = N, m = m, steps_per_round = N * m, bridge_s_per_stage = br, burn_s_per_round = bu, measured_s_per_round = me,
      us_per_step_bridge = 1e6 * br / (N * m), us_per_step_phi1 = 1e6 * (bu * L + me * Hm) / ((L + Hm) * N * m),
      island_s = mean(vapply(isl, function(x) sum(x$seconds), 0)), cache_hit_rate = cc[["hits"]] / (cc[["hits"]] + cc[["misses"]]), cache_clears = cc[["clears"]],
      stringsAsFactors = FALSE)
  }
}
out <- function(x, nm) { x <- do.call(rbind, x); write.table(format(x, digits = 4), paste0(a[2], "_", nm, ".tsv"), sep = "\t", quote = FALSE, row.names = FALSE); cat("\n==", nm, "\n"); print(format(t(x), digits = 4), quote = FALSE) }
out(phase_rows, "phases"); out(stage_rows, "stages"); out(cost_rows, "step_cost")
