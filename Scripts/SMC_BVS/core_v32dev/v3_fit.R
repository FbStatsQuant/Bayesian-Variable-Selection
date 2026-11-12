# SMC-BVS v3 production fit. Part I governs; all statistical settings are fixed.
v3_peak_memory_kb <- function() {
  s <- tryCatch(readLines("/proc/self/status"), error = function(e) character(0))
  l <- grep("^VmHWM:", s, value = TRUE)
  if (!length(l)) return(NA_real_)
  as.numeric(gsub("[^0-9]", "", l))
}

# Exact branch only: 200 operational scores, each of exactly the requested size (R-5 B-O2).
v3_time_scores <- function(Xs, ys, kbar) {
  m <- min(ncol(Xs), max(64, kbar))
  tctx <- v3_context(Xs[, seq_len(m), drop = FALSE], ys, return_gram = FALSE)
  .v3cpp$cpp_time_scores(tctx, min(kbar, tctx$K), 200)[["seconds_per_score"]]
}

# Lead rulings RULINGS_2 G1 / RULINGS_3 N4-N5. SMC preflight is memory only.
# v3.1 (C-GROW MR1 cap; HQ_AUDIT A1 finding 1): with ls0_worst_case = TRUE the SMC preflight also charges LS0 at its worst
# case under the cap ell_n + |S~0| <= ell_n + K: at most ell_n + K + 1 complete scans of at most q(p) = p + p^2/4 models
# each, timed at the measured seconds per score of a size-K model times a declared bookkeeping factor 2 (cache lookup and
# insert, ledger/store offers; an operational estimate, not a rigorous runtime bound), and its archive at the conversion
# peak, when the C++ LocalArchive and its R copy are both alive: (2 scans + 4) models (path, scanned centres, centre,
# returned; C++ vector with capacity growth 8K + 128 bytes, R integer vector + list slot 4K + 128) plus 96 bytes per scan
# for the parallel F / scan_complete / scan_size vectors (both copies, capacity growth) plus 4 scan particles
# (8W + 4K + 96), plus 4096 bytes of fixed list/name/string overhead (R08). Memory is checked first: the size-K timing benchmark runs only if the memory estimate already fits
# (R07 #2). The LS0 time counts against the allocation's hours. ls0_worst_case = FALSE is the shipped preflight.
v3_preflight <- function(n, p, b, branch, allocation, tier = 0, time_fun = NULL, ls0_worst_case = FALSE) {
  K <- b$K; B <- b$B; N <- b$tiers$N[tier + 1]; C_cache <- 500 * p
  mem_gb <- allocation[["mem_gb"]] %||% 8; hours <- allocation[["hours"]] %||% 24
  W <- ceiling(p / 64)
  if (branch == "exact") {
    kstar <- min(K, ceiling(p / 2))
    comp <- c(data_gram = 8 * (3 * n * p + p * p),
              exact_store = 8 * (40 * p + 1) * (kstar + 8), predictors = 32 * p)
    s <- time_fun(kstar); scores <- b$exact_count; seconds <- scores * s
  } else {
    comp <- c(data_gram_correlation_distance = 8 * (3 * n * p + 3 * p * p),
              tables = 16 * ceiling(p / B) * 2^B,
              convolution = 8 * ceiling(p / B) * (K + 1) * (B + 1),
              cache = 29 * 2^ceiling(log2(2 * C_cache)) + 4 * C_cache * K,
              stores = (80 * p + 1) * (4 * K + 64),
              populations = 2 * N * (8 * W + 4 * K + 96))
    s <- scores <- seconds <- NA_real_
    if (isTRUE(ls0_worst_case)) {
      # v3.2-dev (L4, delivery only): one scan from a centre of size k <= K evaluates at most p flips and k (p - k)
      # swaps, so its size is at most p + k* (p - k*), k* = min(K, floor(p / 2)) -- the method's own scan bound
      # (METHOD_v3.1_FINAL #19). v3.1 charged the K-free bound p + p^2 / 4, which refused every fit from p ~ 2.3k at
      # n = 200 and 24 h. options(v3.ls0_scan_bound = "v31") restores the v3.1 charge.
      ls0_kstar <- min(K, p %/% 2)
      ls0_scan <- if (identical(getOption("v3.ls0_scan_bound", "method"), "v31")) p + p^2 / 4 else p + ls0_kstar * (p - ls0_kstar)
      ls0_scans <- b$ell + K + 1; ls0_requests <- ls0_scans * ls0_scan
      comp <- c(comp, ls0_archive = (2 * ls0_scans + 4) * (12 * K + 256) + 96 * ls0_scans + 4 * (8 * W + 4 * K + 96) + 4096)
      ls0_s <- ls0_seconds <- NA_real_
      if (sum(comp) <= mem_gb * 2^30) { ls0_s <- time_fun(K); ls0_seconds <- 2 * ls0_requests * ls0_s }  # R07 #2
    }
  }
  bytes <- sum(comp)
  out <- list(branch = branch, tier = tier, est_bytes = bytes, memory_components = comp,
       est_seconds = seconds, seconds_per_score = s, score_count = scores,
       score_components = if (branch == "exact") c(enumeration = scores) else NULL,
       timing_procedure = if (branch == "exact") list(label = "operational measurement, not a statistical setting",
         scores = 200L, size = kstar, columns = min(p, max(64, kstar)),
         environment = list(R = R.version.string, platform = R.version$platform,
           compiler = Sys.getenv(c("CC", "CXX", "CXX17")), modules = Sys.getenv("LOADEDMODULES"))) else NULL,
       label = "lead ruling 2026-10-22: operational guard, not a statistical setting",
       allocation = list(mem_gb = mem_gb, hours = hours),
       exceeds = bytes > mem_gb * 2^30 || (branch == "exact" && seconds > hours * 3600))
  if (branch != "exact" && isTRUE(ls0_worst_case)) {
    out$ls0_worst_case <- list(label = "v3.1 LS0 worst case (cap ell_n + |S~0| <= ell_n + K); operational estimate",
      scans = ls0_scans, scan_size = ls0_scan,
      scan_bound = if (identical(getOption("v3.ls0_scan_bound", "method"), "v31")) "p + p^2/4 (v3.1)" else "p + k*(p - k*), k* = min(K, floor(p/2))",
      requests = ls0_requests, model_size_timed = K, seconds_per_score = ls0_s,
      bookkeeping_factor = 2, est_seconds = ls0_seconds, timed = !is.na(ls0_seconds), archive_bytes = comp[["ls0_archive"]])
    out$exceeds <- out$exceeds || isTRUE(ls0_seconds > hours * 3600)
  }
  out
}

# Public production interface. Callers own persistence and the study adapter.
# ls0 (default TRUE = v3.1): LS0 after the final local search and exact-name NA estimate fields on every return without
# complete output (GUARD-W, #15). ls0 = FALSE (or options(v3.ls0 = FALSE)) reproduces the v3 fit.
v3_fit <- function(X, y, seed, allocation = list(mem_gb = 8, hours = 24), ls0 = getOption("v3.ls0", TRUE)) {
  t_start <- proc.time()[["elapsed"]]
  runtime <- ctx <- NULL
  fit <- list(seed = seed, allocation = allocation, local_certified = FALSE, global_certified = FALSE,
              cut_group = NA, cut_group_count = NA_integer_, cut_group_components = list(),
              partial_results = FALSE, estimates_available = FALSE)
  finish <- function(fit) {
    fit$peak_memory_kb <- v3_peak_memory_kb()
    fit$timings$total <- proc.time()[["elapsed"]] - t_start
    if (!is.null(runtime)) fit$runtime_guard <- .v3cpp$cpp_runtime_report(runtime)
    if (!is.null(ctx)) fit$numerical_routes <- .v3cpp$cpp_numerical_routes(ctx)
    if (identical(fit$status, "resource_limit")) fit$partial_results <- TRUE
    if (isTRUE(ls0) && !isTRUE(fit$estimates_available)) fit <- v3_unavailable_estimates(fit)
    fit
  }
  valid_seed <- tryCatch({ if (length(seed) != 1) stop("seed must be a single integer"); v3_check_seed(seed); TRUE }, error = function(e) conditionMessage(e))
  if (!isTRUE(valid_seed)) { fit$status <- "invalid_input"; fit$message <- valid_seed; return(finish(fit)) }
  fit <- c(fit, v3_randomness(seed))
  if (!is.list(allocation)) stop("allocation must be a list containing mem_gb and hours")
  allocation <- list(mem_gb = allocation[["mem_gb"]] %||% 8, hours = allocation[["hours"]] %||% 24)
  for (nm in names(allocation)) if (!is.numeric(allocation[[nm]]) || length(allocation[[nm]]) != 1 ||
    !is.finite(allocation[[nm]]) || allocation[[nm]] <= 0) stop("allocation$", nm, " must be finite and positive")
  fit$allocation <- allocation
  runtime <- .v3cpp$cpp_runtime_new(allocation$hours, proc.time()[["elapsed"]] - t_start)
  pre <- v3_preprocess(X, y, dup_components = FALSE)
  fit$preprocessing <- pre[setdiff(names(pre), c("X", "y"))]
  if (pre$status != "ok") {
    fit$status <- pre$status
    if (pre$status %in% c("no_predictors", "y_constant")) fit$hpm <- integer(0)
    return(finish(fit))
  }
  n <- pre$n; p <- pre$p; fit$n <- n; fit$p <- p
  b <- v3_budgets(n, p); fit$budgets <- b; fit$B <- b$B
  fit$branch_decision <- fit$branch_run <- if (b$exact_branch) "exact" else "smc"
  tcache <- list()
  time_fun <- function(k) {
    key <- as.character(k)
    if (is.null(tcache[[key]])) tcache[[key]] <<- v3_time_scores(pre$X, pre$y, k)
    tcache[[key]]
  }
  # v3.1: charge LS0's worst case under the C-GROW cap; options(v3.ls0_cap = "ell_n") or ls0 = FALSE: shipped preflight
  ls0_wc <- isTRUE(ls0) && !identical(getOption("v3.ls0_cap", "ell_n_plus_mode"), "ell_n")
  pf <- v3_preflight(n, p, b, fit$branch_run, allocation, time_fun = time_fun, ls0_worst_case = ls0_wc)
  fit$preflight <- pf
  if (pf$exceeds) { fit$status <- "resource_limit"; return(finish(fit)) }
  ctx <- v3_context(pre$X, pre$y, orig = pre$kept, return_gram = FALSE)
  fit$preprocessing$dup_components <- .v3cpp$cpp_dup_components(ctx)
  if (fit$branch_run == "exact") {
    t0 <- proc.time()[["elapsed"]]; e <- v3_enumerate(ctx)
    fit$timings$exact <- proc.time()[["elapsed"]] - t0; fit$exact <- e; fit$status <- e$status
    fit$hpm <- e$hpm; fit$hpm_F <- e$hpm_F; fit$hpm_provenance <- list(phase = "exact", mechanism = "enumeration")
    fit$near_ties <- e$near_ties; fit$near_tie_F <- e$near_tie_F; fit$near_tie_truncated <- e$near_tie_truncated
    if (e$status == "exact") {
      fit$log_Z <- e$log_Z; fit$log_Z_rel_m0 <- e$log_Z_rel_m0; fit$log_Z_lower95 <- log(0.05) + e$log_Z
      fit$pip_primary <- e$pip; fit$mpm <- e$mpm
      fit$global_certified <- e$global_certified; fit$local_certified <- e$local_certified
      fit$estimates_available <- TRUE
    } else { fit$message <- e$message; fit$hpm_incomplete <- TRUE }
    return(finish(fit))
  }
  t0 <- proc.time()[["elapsed"]]; setup <- v3_setup(ctx)
  if (inherits(setup, "v3_setup_failed")) {
    fit$status <- "numerical_failure"; fit$message <- setup$message
    fit$hpm <- setup$hpm; fit$hpm_F <- setup$hpm_F; fit$hpm_provenance <- setup$hpm_provenance
    fit$hpm_incomplete <- TRUE; return(finish(fit))
  }
  fit$timings$setup <- setup$seconds; fit$timings$setup_total <- proc.time()[["elapsed"]] - t0
  fit$blocks <- setup$blocks; fit$neighbours <- setup$neighbours; fit$log_Zbar0 <- setup$start$log_Zbar0
  cg <- .v3cpp$cpp_cut_group(setup$ptr)
  fit$cut_group <- cg$cut_group; fit$cut_group_count <- cg$count; fit$cut_group_components <- cg$components
  fit$cut_group_graph <- cg[c("threshold", "graph")]
  pf_fun <- function(e) {
    pf <- v3_preflight(n, p, b, "smc", allocation, tier = e, time_fun = time_fun, ls0_worst_case = ls0_wc)
    fit$preflight_escalation <<- pf
    pf$exceeds
  }
  t0 <- proc.time()[["elapsed"]]
  cal <- v3_calibrate(setup, seed, preflight = pf_fun, runtime = runtime,
                      grid_fallback = isTRUE(ls0) && isTRUE(getOption("v3.grid_fallback", TRUE)))
  fit$timings$calibration <- proc.time()[["elapsed"]] - t0; fit$calibration <- cal
  fit$stage_table <- cal$stage_table
  if (cal$status != "ok") {
    fit$status <- cal$status; fit$flags <- cal$flags
    fit$hpm <- cal$hpm$model; fit$hpm_F <- cal$hpm$F; fit$hpm_provenance <- cal$hpm$provenance
    fit$hpm_incomplete <- TRUE
    if (cal$status == "numerical_failure") fit$message <- cal$tiers[[length(cal$tiers)]]$message
    return(finish(fit))
  }
  frozen <- cal$frozen; fit$frozen <- frozen
  t0 <- proc.time()[["elapsed"]]; fr <- v3_final_run(setup, frozen, seed, runtime, ls0 = ls0)
  fr$stage_table <- v3_bind_records(list(cal$stage_table, fr$stage_table))
  fit$timings$final <- proc.time()[["elapsed"]] - t0; fit$timings$final_detail <- fr$timings; fr$timings <- NULL
  cf <- cal$flags
  fr$flags$escalated <- cf$escalated; fr$flags$checks_passed_calibration <- cf$checks_passed_calibration
  fr$flags$forced_pilot_steps <- cf$forced_pilot_steps; fr$flags$grid_unconverged <- cf$grid_unconverged
  fr$flags$calibration_triggers <- cf$triggers_fired
  # C-DLV B: present only when the fallback fired ("last_successful_construction" or "pilot_schedule"; R05 #1)
  if (!is.null(cf$grid_fallback)) fr$flags$grid_fallback <- cf$grid_fallback
  for (nm in names(fr)) fit[[nm]] <- fr[[nm]]
  fit$flags$cut_group <- fit$cut_group
  finish(fit)
}
