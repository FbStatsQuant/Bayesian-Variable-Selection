# usage: Rscript run_dlv.R n p seeds(comma) designs(comma, default M,F)
args <- commandArgs(TRUE)
n <- as.integer(args[1]); p <- as.integer(args[2])
seeds <- as.integer(strsplit(args[3], ",")[[1]])
designs <- if (length(args) >= 4) strsplit(args[4], ",")[[1]] else c("M", "F")
NUM <- "C:/Users/felip/Bayesian-Variable-Selection/Theory_work/Wave1C/C-DLV/numerics"
setwd(NUM)
source(file.path(NUM, "core_copy/v3.R"))     # copy only
source(file.path(NUM, "dlv_lib.R"))

peak_ws_kb <- function() tryCatch({ o <- system2("powershell", c("-NoProfile","-Command", sprintf("(Get-Process -Id %d).PeakWorkingSet64", Sys.getpid())), stdout = TRUE); as.numeric(o[1]) / 1024 }, error = function(e) NA_real_)  # process-lifetime peak working set (Windows); fit$peak_memory_kb is NA here (no /proc)
record_fit <- function(fit, design, n, p, seed, S0, secs_wall) {
  cal <- fit$calibration
  hpm <- fit$hpm
  ck <- fit$runtime_guard$checkpoints
  row <- list(design = design, n = n, p = p, seed = seed, status = fit$status %||% NA,
              message = fit$message %||% "", branch_run = fit$branch_run %||% NA,
              estimates_available = isTRUE(fit$estimates_available),
              escalated = if (!is.null(cal)) cal$escalated else NA,
              tier_final = if (!is.null(cal)) cal$tier_final else NA,
              hpm = paste(sort(hpm), collapse = "+"), hpm_eq_S0 = identical(sort(as.integer(hpm)), sort(as.integer(S0))),
              total_seconds = fit$timings$total, wall_seconds = secs_wall,
              peak_memory_kb = peak_ws_kb(), preflight_est_bytes = fit$preflight$est_bytes %||% NA,
              guard_checkpoints = if (is.data.frame(ck)) nrow(ck) else length(ck),
              guard_exceeded = tryCatch(any(unlist(lapply(ck, function(z) z$exceeded %||% z$stop %||% FALSE))), error = function(e) NA),
              rebuilds_final_tier = NA, converged_final_tier = NA, triggers_by_tier = "")
  cons <- list()
  if (!is.null(cal)) {
    row$rebuilds_final_tier <- tail(cal$tiers, 1)[[1]]$rebuilds
    row$converged_final_tier <- tail(cal$tiers, 1)[[1]]$converged
    row$triggers_by_tier <- paste(vapply(seq_along(cal$tiers), function(i) {
      tr <- cal$tiers[[i]]$triggers; paste0("t", cal$tiers[[i]]$tier, ":", paste(names(tr)[unlist(tr)], collapse = "|"))
    }, ""), collapse = ";")
    for (tt in cal$tiers) {
      Np <- length(tt$pilot$schedule) - 1L
      Te <- tt$settings$T_e
      for (k in seq_along(tt$grids)) {
        gr <- tt$grids[[k]]; sn <- tt$snapshots[[k]]
        lam <- Lambda_V(sn)
        cons[[length(cons) + 1]] <- data.frame(design = design, n = n, p = p, seed = seed, tier = tt$tier, T_e = Te,
          N_p = Np, forced_pilot_steps = tt$pilot$forced_pilot_steps, construction = gr$label, ok = gr$ok,
          reason = gr$reason %||% "", intervals = gr$intervals, N_b = gr$intervals - Np,
          S0_in_V = has_S0(sn, S0), V_size = sn$size, truncated = sn$truncated, Lambda_V = lam,
          Lambda_lt_log109 = if (is.na(lam)) NA else lam < log(10 / 9), stringsAsFactors = FALSE)
      }
    }
  }
  list(row = as.data.frame(row, stringsAsFactors = FALSE), cons = if (length(cons)) do.call(rbind, cons) else NULL)
}

for (design in designs) for (seed in seeds) {
  tag <- sprintf("%s_n%d_p%d_s%d", design, n, p, seed)
  if (file.exists(file.path("parts", paste0(tag, "_fit.csv")))) next
  dat <- make_data(design, n, p, seed)
  t0 <- proc.time()[["elapsed"]]
  fit <- tryCatch(v3_fit(dat$X, dat$y, 1000L + seed, allocation = list(mem_gb = 16, hours = 24)),
                  error = function(e) list(status = "R_error", message = conditionMessage(e), timings = list(total = NA)))
  wall <- proc.time()[["elapsed"]] - t0
  rec <- record_fit(fit, design, n, p, seed, dat$S0, wall)
  write.csv(rec$row, file.path("parts", paste0(tag, "_fit.csv")), row.names = FALSE)
  if (!is.null(rec$cons)) write.csv(rec$cons, file.path("parts", paste0(tag, "_cons.csv")), row.names = FALSE)
  small <- list(row = rec$row, cons = rec$cons, schedule = lapply(fit$calibration$tiers, function(t) t$pilot$schedule),
                flags = fit$flags, hpm = fit$hpm, pip_primary = fit$pip_primary, runtime_guard = fit$runtime_guard,
                preflight = fit$preflight, budgets = fit$budgets)
  saveRDS(small, file.path("rds", paste0(tag, ".rds")))
  cat(sprintf("[%s] %s status=%s branch=%s esc=%s secs=%.1f hpm=%s\n", format(Sys.time(), "%H:%M:%S"), tag,
              rec$row$status, rec$row$branch_run, rec$row$escalated, wall, rec$row$hpm), flush = TRUE)
}
