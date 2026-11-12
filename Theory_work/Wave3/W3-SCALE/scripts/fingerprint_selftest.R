# fingerprint_selftest.R -- mutation test of ws_fingerprint (review R01 finding 3).
# For a saved fit: every mutation of a non-timing field must change fingerprint$all; every mutation of a pure
# wall-clock / memory field must leave it unchanged. Usage: Rscript --vanilla fingerprint_selftest.R FIT.rds [...]
local({
  a <- grep("^--file=", commandArgs(FALSE), value = TRUE)
  assign("WS_DIR", if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd(), envir = globalenv())
})
source(file.path(WS_DIR, "ws_common.R"))
fail <- 0L
for (f in commandArgs(trailingOnly = TRUE)) {
  fit <- readRDS(f); base <- ws_fingerprint(fit)$all
  must_change <- list(
    allocation_hours = function(x) { x$allocation$hours <- x$allocation$hours + 1; x },
    guard_exceeded = function(x) { x$runtime_guard$exceeded <- !isTRUE(x$runtime_guard$exceeded); x },
    guard_checkpoint_dropped = function(x) { n <- length(x$runtime_guard$checkpoints); if (n) x$runtime_guard$checkpoints <- x$runtime_guard$checkpoints[-n] else x$runtime_guard$checkpoints <- list(1); x },
    guard_checkpoint_stage = function(x) { if (length(x$runtime_guard$checkpoints)) x$runtime_guard$checkpoints[[1]]$stage <- 999L else x$runtime_guard$label <- "x"; x },
    list_attribute = function(x) { attr(x$allocation, "extra") <- 1; x },
    top_attribute = function(x) { attr(x, "extra") <- 1; x },
    status = function(x) { x$status <- paste0(x$status, "_x"); x },
    preflight_bytes = function(x) { if (!is.null(x$preflight)) x$preflight$est_bytes <- x$preflight$est_bytes + 1 else x$seed <- x$seed + 1; x },
    log_Z_one_ulp = function(x) { if (is.numeric(x$log_Z) && !is.na(x$log_Z)) x$log_Z <- x$log_Z * (1 + .Machine$double.eps) else x$seed <- x$seed + 1; x },
    pip_one_bit = function(x) { if (is.numeric(x$pip_primary)) x$pip_primary[1] <- if (x$pip_primary[1] == 0) .Machine$double.xmin else x$pip_primary[1] * (1 - .Machine$double.eps) else x$seed <- x$seed + 1; x },
    stage_table_ess = function(x) { if (is.data.frame(x$stage_table) && nrow(x$stage_table)) x$stage_table$ess[1] <- x$stage_table$ess[1] + 1e-9 else x$seed <- x$seed + 1; x },
    deep_calibration = function(x) { if (length(x$calibration$tiers)) x$calibration$tiers[[1]]$pilot$schedule[2] <- x$calibration$tiers[[1]]$pilot$schedule[2] + 1e-12 else x$seed <- x$seed + 1; x },
    score_counts = function(x) { if (!is.null(x$score_counts)) x$score_counts$fresh[1] <- x$score_counts$fresh[1] + 1 else x$seed <- x$seed + 1; x },
    numerical_routes = function(x) { if (!is.null(x$numerical_routes)) x$numerical_routes$chol <- x$numerical_routes$chol + 1 else x$seed <- x$seed + 1; x })
  must_not_change <- list(
    timings_total = function(x) { x$timings$total <- 1e9; x },
    peak_memory = function(x) { x$peak_memory_kb <- 1; x },
    guard_elapsed = function(x) { x$runtime_guard$elapsed_seconds <- 1e9
      for (i in seq_along(x$runtime_guard$checkpoints)) { x$runtime_guard$checkpoints[[i]]$elapsed_seconds <- 1; x$runtime_guard$checkpoints[[i]]$operation_seconds <- 2; x$runtime_guard$checkpoints[[i]]$projected_seconds <- 3 }; x },
    preflight_timing = function(x) { if (!is.null(x$preflight)) { x$preflight$seconds_per_score <- 1; x$preflight$est_seconds <- 1; if (!is.null(x$preflight$ls0_worst_case)) x$preflight$ls0_worst_case$est_seconds <- 1 }; x },
    island_seconds = function(x) { for (i in seq_along(x$stage_record)) if (!is.null(x$stage_record[[i]]$seconds)) x$stage_record[[i]]$seconds[] <- 1; x },
    calibration_seconds = function(x) { if (!is.null(x$calibration)) { x$calibration$seconds <- 1; for (i in seq_along(x$calibration$tiers)) x$calibration$tiers[[i]]$seconds[] <- 1 }; x })
  d <- 0L; k <- 0L
  for (nm in names(must_change)) if (identical(ws_fingerprint(must_change[[nm]](fit))$all, base)) { fail <- fail + 1L; cat("FAIL (not detected):", nm, "in", basename(f), "
") } else d <- d + 1L
  for (nm in names(must_not_change)) if (!identical(ws_fingerprint(must_not_change[[nm]](fit))$all, base)) { fail <- fail + 1L; cat("FAIL (timing changed the hash):", nm, "in", basename(f), "
") } else k <- k + 1L
  cat(sprintf("%-40s status %-14s mutations detected %d/%d, timing-invariant %d/%d
", basename(f), fit$status, d, length(must_change), k, length(must_not_change)))
}
cat(if (fail == 0L) "SELFTEST PASSED\n" else sprintf("SELFTEST FAILED (%d)\n", fail))
quit(status = if (fail == 0L) 0L else 1L)
