# usage: Rscript n4_run.R design n p seeds
args <- commandArgs(TRUE)
design <- args[1]; n <- as.integer(args[2]); p <- as.integer(args[3]); seeds <- as.integer(strsplit(args[4], ",")[[1]])
NUM <- "C:/Users/felip/Bayesian-Variable-Selection/Theory_work/Wave1C/C-DLV/numerics"
setwd(NUM)
source(file.path(NUM, "core_copy/v3.R")); source(file.path(NUM, "dlv_lib.R"))
spec <- switch(design,
  S1 = list(psis = c(.2, .2, .2), betas = c(1, 1, 1), vis = 0.7),
  S2 = list(psis = c(.5, .5), betas = c(1, .6), vis = NA),
  S3 = list(psis = .2, betas = .35, vis = NA))
make4 <- function(n, p, seed, g = 9, rho = .4) {
  G <- p / g; Sigma <- lh_sigma(G, g, rho, spec$psis)
  th <- numeric(p); S0 <- integer(0)
  for (i in seq_along(spec$psis)) {
    a <- hub(2 * (i - 1)); b <- hub(2 * (i - 1) + 1)
    th[a] <- spec$betas[i]; th[b] <- -spec$psis[i] * spec$betas[i]; S0 <- c(S0, a, b)
  }
  if (!is.na(spec$vis)) { v <- hub(2 * length(spec$psis)); th[v] <- spec$vis; S0 <- c(S0, v) }
  set.seed(seed); Lc <- t(chol(Sigma))
  if (p <= n - 1) { Z <- matrix(rnorm(n * p), n, p); Z <- sweep(Z, 2, colMeans(Z)); X <- sqrt(n - 1) * qr.Q(qr(Z)) %*% t(Lc) }
  else X <- matrix(rnorm(n * p), n, p) %*% t(Lc)
  list(X = X, y = as.numeric(X %*% th + rnorm(n)), S0 = S0)
}
peak_ws_kb <- function() tryCatch({ o <- system2("powershell", c("-NoProfile","-Command", sprintf("(Get-Process -Id %d).PeakWorkingSet64", Sys.getpid())), stdout = TRUE); as.numeric(o[1]) / 1024 }, error = function(e) NA_real_)
for (seed in seeds) {
  tag <- sprintf("%s_n%d_p%d_s%d", design, n, p, seed)
  if (file.exists(file.path("n4parts", paste0(tag, "_fit.csv")))) next
  dat <- make4(n, p, seed); S0 <- dat$S0
  t0 <- proc.time()[["elapsed"]]
  fit <- tryCatch(v3_fit(dat$X, dat$y, 1000L + seed, allocation = list(mem_gb = 16, hours = 24)),
                  error = function(e) list(status = "R_error", message = conditionMessage(e), timings = list(total = NA)))
  wall <- proc.time()[["elapsed"]] - t0
  cal <- fit$calibration; hpm <- fit$hpm
  row <- data.frame(design = design, n = n, p = p, seed = seed, status = fit$status %||% NA, message = fit$message %||% "",
    branch_run = fit$branch_run %||% NA, estimates_available = isTRUE(fit$estimates_available),
    escalated = if (!is.null(cal)) cal$escalated else NA, tier_final = if (!is.null(cal)) cal$tier_final else NA,
    hpm = paste(sort(hpm), collapse = "+"), S0 = paste(sort(S0), collapse = "+"),
    hpm_eq_S0 = identical(sort(as.integer(hpm)), sort(as.integer(S0))),
    total_seconds = fit$timings$total, peak_ws_kb = peak_ws_kb(), preflight_est_bytes = fit$preflight$est_bytes %||% NA,
    guard_exceeded = isTRUE(fit$runtime_guard$exceeded), stringsAsFactors = FALSE)
  cons <- NULL
  if (!is.null(cal)) {
    lt <- tail(cal$tiers, 1)[[1]]
    row$rebuilds_final_tier <- lt$rebuilds %||% NA; row$converged_final_tier <- lt$converged %||% NA
    row$triggers_by_tier <- paste(vapply(cal$tiers, function(t) paste0("t", t$tier, ":", paste(names(t$triggers)[unlist(t$triggers)], collapse = "|")), ""), collapse = ";")
    row$max_pilot_step <- paste(vapply(cal$tiers, function(t) format(max(diff(t$pilot$schedule)), digits = 6), ""), collapse = ";")
    row$tier_status <- paste(vapply(cal$tiers, function(t) t$status, ""), collapse = ";")
    cl <- list()
    for (tt in cal$tiers) { Np <- length(tt$pilot$schedule) - 1L
      for (k in seq_along(tt$grids)) { gr <- tt$grids[[k]]; sn <- tt$snapshots[[k]]; lam <- Lambda_V(sn)
        cl[[length(cl) + 1]] <- data.frame(design = design, n = n, p = p, seed = seed, tier = tt$tier, T_e = tt$settings$T_e,
          N_p = Np, forced_pilot_steps = tt$pilot$forced_pilot_steps, max_pilot_step = max(diff(tt$pilot$schedule)),
          construction = gr$label, ok = gr$ok, reason = gr$reason %||% "", intervals = gr$intervals, N_b = gr$intervals - Np,
          S0_in_V = has_S0(sn, S0), V_size = sn$size, truncated = sn$truncated, Lambda_V = lam,
          Lambda_lt_log109 = if (is.na(lam)) NA else lam < log(10/9), stringsAsFactors = FALSE) } }
    if (length(cl)) cons <- do.call(rbind, cl)
  }
  write.csv(row, file.path("n4parts", paste0(tag, "_fit.csv")), row.names = FALSE)
  if (!is.null(cons)) write.csv(cons, file.path("n4parts", paste0(tag, "_cons.csv")), row.names = FALSE)
  cat(sprintf("[%s] %s status=%s esc=%s secs=%.1f hpm=%s S0=%s\n", format(Sys.time(), "%H:%M:%S"), tag, row$status, row$escalated, wall, row$hpm, row$S0), flush = TRUE)
}
