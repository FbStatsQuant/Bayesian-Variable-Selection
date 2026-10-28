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
v3_preflight <- function(n, p, b, branch, allocation, tier = 0, time_fun = NULL) {
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
  }
  bytes <- sum(comp)
  list(branch = branch, tier = tier, est_bytes = bytes, memory_components = comp,
       est_seconds = seconds, seconds_per_score = s, score_count = scores,
       score_components = if (branch == "exact") c(enumeration = scores) else NULL,
       timing_procedure = if (branch == "exact") list(label = "operational measurement, not a statistical setting",
         scores = 200L, size = kstar, columns = min(p, max(64, kstar)),
         environment = list(R = R.version.string, platform = R.version$platform,
           compiler = Sys.getenv(c("CC", "CXX", "CXX17")), modules = Sys.getenv("LOADEDMODULES"))) else NULL,
       label = "lead ruling 2026-10-22: operational guard, not a statistical setting",
       allocation = list(mem_gb = mem_gb, hours = hours),
       exceeds = bytes > mem_gb * 2^30 || (branch == "exact" && seconds > hours * 3600))
}

# Public production interface. Callers own persistence and the study adapter.
v3_fit <- function(X, y, seed, allocation = list(mem_gb = 8, hours = 24)) {
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
  pf <- v3_preflight(n, p, b, fit$branch_run, allocation, time_fun = time_fun)
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
    pf <- v3_preflight(n, p, b, "smc", allocation, tier = e)
    fit$preflight_escalation <<- pf
    pf$exceeds
  }
  t0 <- proc.time()[["elapsed"]]
  cal <- v3_calibrate(setup, seed, preflight = pf_fun, runtime = runtime)
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
  t0 <- proc.time()[["elapsed"]]; fr <- v3_final_run(setup, frozen, seed, runtime)
  fr$stage_table <- v3_bind_records(list(cal$stage_table, fr$stage_table))
  fit$timings$final <- proc.time()[["elapsed"]] - t0; fit$timings$final_detail <- fr$timings; fr$timings <- NULL
  cf <- cal$flags
  fr$flags$escalated <- cf$escalated; fr$flags$checks_passed_calibration <- cf$checks_passed_calibration
  fr$flags$forced_pilot_steps <- cf$forced_pilot_steps; fr$flags$grid_unconverged <- cf$grid_unconverged
  fr$flags$calibration_triggers <- cf$triggers_fired
  for (nm in names(fr)) fit[[nm]] <- fr[[nm]]
  fit$flags$cut_group <- fit$cut_group
  finish(fit)
}
