# v3_fit.R -- the fit: preprocess -> preflight (resource_limit) -> exact branch unless force_smc (R10) -> setup ->
# final run on a supplied grid (core layer). CORE_SPEC v2 §7; M §2, §6.1, §8.6.

v3_peak_memory_kb <- function() {
  s <- tryCatch(readLines("/proc/self/status"), error = function(e) character(0))
  l <- grep("^VmHWM:", s, value = TRUE)
  if (!length(l)) return(NA_real_)
  as.numeric(gsub("[^0-9]", "", l))
}

# Resource preflight (M §8.6): peak memory and wall time of the branch about to run, estimated before allocation.
# Time = (score count) x (measured seconds per fresh score at a typical size). Documented planning assumptions:
# SMC score count = tables (ceil(p/B) 2^B) + R N (T + L + 4)(p + B + 2) (one fresh score per step, no cache credit)
# + local search (ell + 1)(p + k(p - k)) at k = min(K, 10); T = length(grid) - 1 (supplied grid) or 50 otherwise.
# Calibration (grid = "calibrate", tier e): adds the pilot H_e (50 + L + 4)(p + B + 2), ell rebuilds of 4 H_e (T + L + 4)
# (p + B + 2) and (ell + 2) local searches, with T = 50 planned stages; the final run then uses N_e.
# Run BEFORE any p x p allocation (code review D-1): the inputs are (n, p) and the seconds per fresh score measured on
# a small timing context (the first min(p, 64) standardised columns; the cost of a score depends on n and |S| only).
# Memory counts the R copies of X and the standardised X, the C++ copy of X, the Gram (p x p) and, for the SMC branch,
# the correlation and clustering-distance matrices (2 more p x p) that exist together during block construction.
v3_time_scores <- function(Xs, ys, kbar) {
  m <- min(ncol(Xs), max(64, kbar))
  tctx <- v3_context(Xs[, seq_len(m), drop = FALSE], ys, return_gram = FALSE)
  .v3cpp$cpp_time_scores(tctx, min(kbar, tctx$K), 200)[["seconds_per_score"]]
}
v3_preflight <- function(n, p, b, branch, grid, ro, allocation, tier = 0, time_fun) {
  K <- b$K
  mem_gb <- allocation[["mem_gb"]] %||% 8; hours <- allocation[["hours"]] %||% 24
  W <- ceiling(p / 64)
  if (branch == "exact") {
    kbar <- min(K, ceiling(p / 2))
    s <- time_fun(kbar)
    scores <- b$exact_count
    mem <- 8 * (3 * n * p + p * p) + 8 * (40 * p + 1) * (kbar + 8) + 8 * 4 * p
  } else {
    B <- ro$B; N <- ro$N; R <- ro$islands; L <- ro$L
    T <- if (is.numeric(grid)) length(grid) - 1 else 50
    kbar <- min(K, 10)
    s <- time_fun(kbar)
    N <- N * 4^tier
    comp <- c(tables = ceiling(p / B) * 2^B, final = R * N * (T + L + ro$measured_rounds) * (p + B + 2),
              final_local = (b$ell + 1) * (p + kbar * (p - kbar)))
    if (identical(grid, "calibrate")) {
      H <- b$tiers$H[tier + 1]
      comp <- c(comp, pilot = H * (50 + L + 4) * (p + B + 2), rebuild_islands = b$ell * 4 * H * (50 + L + 4) * (p + B + 2),
                calibration_local = (b$ell + 2) * (b$ell + 1) * (p + kbar * (p - kbar)))
    }
    scores <- sum(comp)
    cache_entries <- ro$cache_capacity
    mem <- 8 * (3 * n * p + 3 * p * p) +                  # X copies (R raw, R standardised, C++), Gram, correlations, distances
      16 * ceiling(p / B) * 2^B +                          # tables (log r, log m)
      8 * ceiling(p / B) * (K + 1) * (B + 1) +             # convolution / sampler tables
      2^ceiling(log2(2 * cache_entries)) * 29 + cache_entries * 4 * kbar +   # cache: slots + member-list key pool
      (40 * p + 1 + 40 * p) * (4 * kbar + 64) +            # top store + leader stores
      2 * N * (8 * W + 4 * kbar + 96)                      # population and its resampled copy
    if (isTRUE(ro$dump_scored)) mem <- mem + 1e3 * 2^min(p, 20)
  }
  time <- scores * s
  list(branch = branch, grid = if (is.numeric(grid)) "supplied" else grid, est_seconds = time, est_bytes = mem,
       seconds_per_score = s, score_count = scores, score_components = if (branch == "exact") c(enumeration = scores) else comp,
       allocation = list(mem_gb = mem_gb, hours = hours),
       exceeds = (mem > mem_gb * 2^30) || (time > hours * 3600))
}

v3_summary_json <- function(fit, path) {
  f <- function(x) if (is.null(x)) NA else x
  key <- function(S) if (is.null(S)) NA else paste(S, collapse = ",")
  s <- list(status = fit$status, branch_decision = f(fit$branch_decision), branch_run = f(fit$branch_run),
            n = f(fit$n), p = f(fit$p), K = f(fit$budgets$K), B = f(fit$B), seed = f(fit$seed),
            hpm = key(fit$hpm), hpm_F = f(fit$hpm_F), hpm_size = length(fit$hpm), mpm = key(fit$mpm),
            log_Z = f(fit$log_Z), log_Z_rel_m0 = f(fit$log_Z_rel_m0), log_Z_lower95 = f(fit$log_Z_lower95),
            local_certified = f(fit$local_certified), global_certified = f(fit$global_certified),
            local_limit = f(fit$local_limit), near_tie_truncated = f(fit$near_tie_truncated),
            E1 = f(fit$flags$E1), E2 = f(fit$flags$E2), E3 = f(fit$flags$E3), low_empirical_ESS = f(fit$flags$low_empirical_ESS),
            checks_passed_final = f(fit$flags$checks_passed_final), n_islands = length(fit$log_Z_r),
            seconds_total = f(fit$timings$total), peak_memory_kb = f(fit$peak_memory_kb))
  if (!is.null(fit$log_Z_r)) for (r in seq_along(fit$log_Z_r)) s[[paste0("log_Z_r", r)]] <- fit$log_Z_r[r]
  jsonlite::write_json(s, path, auto_unbox = TRUE, digits = NA, pretty = TRUE, na = "null")
}

# v3_fit(X, y, seed, grid = NULL, observer = NULL, opts = list(), allocation = list(mem_gb = 8, hours = 24)).
# opts (test/experiment, recorded): N, islands, L, measured_rounds, force_smc, dump_scored, cache_capacity,
# B_override, resampler_trace, switch_no_candidate_grid (calibration layer; recorded only), hooks (scorer test
# hooks), out_dir (writes fit.rds and summary.json there).
v3_fit <- function(X, y, seed, grid = NULL, observer = NULL, opts = list(), allocation = list(mem_gb = 8, hours = 24)) {
  t_start <- proc.time()[["elapsed"]]
  if (length(seed) != 1) stop("seed must be a single integer"); v3_check_seed(seed)
  pre <- v3_preprocess(X, y, dup_components = FALSE)   # duplicate check after the preflight (D-1)
  fit <- list(seed = seed, opts = opts, allocation = allocation)
  finish <- function(fit) {
    fit$peak_memory_kb <- v3_peak_memory_kb()
    fit$timings$total <- proc.time()[["elapsed"]] - t_start
    if (!is.null(opts[["out_dir"]])) {
      dir.create(opts[["out_dir"]], recursive = TRUE, showWarnings = FALSE)
      saveRDS(fit, file.path(opts[["out_dir"]], "fit.rds"))
      v3_summary_json(fit, file.path(opts[["out_dir"]], "summary.json"))
    }
    fit
  }
  fit$preprocessing <- pre[setdiff(names(pre), c("X", "y"))]
  if (pre$status != "ok") {
    fit$status <- pre$status
    if (pre$status %in% c("no_predictors", "y_constant")) fit$hpm <- integer(0)   # M §4: S-hat = empty
    fit$estimates_available <- FALSE
    return(finish(fit))
  }
  n <- pre$n; p <- pre$p
  fit$n <- n; fit$p <- p
  b <- v3_budgets(n, p); fit$budgets <- b
  fit$branch_decision <- if (b$exact_branch) "exact" else "smc"                 # production decision (R10)
  fit$branch_run <- if (b$exact_branch && !isTRUE(opts[["force_smc"]])) "exact" else "smc"
  B <- if (is.null(opts[["B_override"]])) b$B else as.integer(opts[["B_override"]])
  fit$B <- B
  ro_plan <- list(B = B, N = as.integer(opts[["N"]] %||% b$tiers$N[1]), islands = as.integer(opts[["islands"]] %||% 4L),
                  L = as.integer(opts[["L"]] %||% b$L), measured_rounds = as.integer(opts[["measured_rounds"]] %||% 4L),
                  cache_capacity = as.numeric(opts[["cache_capacity"]] %||% max(500 * p, 2^15)), dump_scored = isTRUE(opts[["dump_scored"]]))
  if (is.null(grid)) grid <- "calibrate"           # production default (M §6.1), resolved BEFORE the preflight (review D-2)
  if (!identical(grid, "calibrate") && !is.numeric(grid)) stop("grid must be numeric or \"calibrate\"")
  tcache <- list()
  time_fun <- function(k) { key <- as.character(k); if (is.null(tcache[[key]])) tcache[[key]] <<- v3_time_scores(pre$X, pre$y, k); tcache[[key]] }
  pf <- v3_preflight(n, p, b, fit$branch_run, grid, ro_plan, allocation, time_fun = time_fun)
  fit$preflight <- pf
  if (pf$exceeds) {   # before any p x p allocation (M §8.6)
    fit$status <- "resource_limit"; fit$estimates_available <- FALSE
    return(finish(fit))
  }
  ctx <- v3_context(pre$X, pre$y, orig = pre$kept, hooks = opts[["hooks"]] %||% list(), return_gram = FALSE)
  fit$preprocessing$dup_components <- .v3cpp$cpp_dup_components(ctx)   # M §4.5, from the Gram (no p x p temporaries)
  if (fit$branch_run == "exact") {
    t0 <- proc.time()[["elapsed"]]
    e <- v3_enumerate(ctx)
    fit$timings$exact <- proc.time()[["elapsed"]] - t0
    fit$status <- e$status
    fit$exact <- e
    fit$hpm <- e$hpm; fit$hpm_F <- e$hpm_F; fit$hpm_provenance <- list(phase = "exact")
    fit$near_ties <- e$near_ties; fit$near_tie_truncated <- e$near_tie_truncated
    if (e$status == "exact") {
      fit$log_Z <- e$log_Z; fit$log_Z_rel_m0 <- e$log_Z_rel_m0
      fit$pip_primary <- e$pip; fit$pip_secondary <- e$pip; fit$mpm <- e$mpm
      fit$global_certified <- e$global_certified; fit$local_certified <- e$local_certified
      fit$estimates_available <- TRUE
    } else {   # numerical_failure: best scored model so far, labelled incomplete (M §2), as on the SMC branch
      fit$message <- e$message; fit$hpm_incomplete <- TRUE; fit$estimates_available <- FALSE
    }
    return(finish(fit))
  }
  t0 <- proc.time()[["elapsed"]]
  setup <- v3_setup(ctx, B_override = opts[["B_override"]])
  if (inherits(setup, "v3_setup_failed")) {
    fit$status <- "numerical_failure"; fit$message <- setup$message
    fit$hpm <- setup$hpm; fit$hpm_F <- setup$hpm_F; fit$hpm_provenance <- setup$hpm_provenance
    fit$hpm_incomplete <- TRUE; fit$estimates_available <- FALSE
    return(finish(fit))
  }
  fit$timings$setup <- setup$seconds; fit$timings$setup_total <- proc.time()[["elapsed"]] - t0
  fit$blocks <- setup$blocks; fit$neighbours <- setup$neighbours
  fit$log_Zbar0 <- setup$start$log_Zbar0
  obs_ptr <- if (!is.null(observer) && identical(grid, "calibrate")) .v3cpp$cpp_observer_new(setup$ptr, v3_observer_prepare(setup, observer)) else NULL
  if (identical(grid, "calibrate")) {
    pf_fun <- function(e) v3_preflight(n, p, b, "smc", "calibrate", ro_plan, allocation, tier = e, time_fun = time_fun)$exceeds
    t0 <- proc.time()[["elapsed"]]
    cal <- v3_calibrate(setup, seed, 0, opts, .obs_ptr = obs_ptr, preflight = pf_fun)
    fit$timings$calibration <- proc.time()[["elapsed"]] - t0
    fit$calibration <- cal
    if (cal$status != "ok") {
      fit$status <- cal$status; fit$estimates_available <- FALSE
      fit$hpm <- cal$hpm$model; fit$hpm_F <- cal$hpm$F; fit$hpm_provenance <- cal$hpm$provenance
      if (cal$status == "numerical_failure") { fit$hpm_incomplete <- TRUE; fit$message <- cal$tiers[[length(cal$tiers)]]$message }
      if (!is.null(obs_ptr)) fit$observer <- list(calibration = v3_observer_calibration(cal, list()))
      return(finish(fit))
    }
    frozen <- cal$frozen
  } else frozen <- v3_frozen(grid, tier = 0, budgets = b)
  fit$frozen <- frozen
  t0 <- proc.time()[["elapsed"]]
  fr <- v3_final_run(setup, frozen, seed, if (is.null(obs_ptr)) observer else NULL, opts, .obs_ptr = obs_ptr)
  fit$timings$final <- proc.time()[["elapsed"]] - t0
  fit$timings$final_detail <- fr$timings
  fr$timings <- NULL
  obs <- fr$observer; fr$observer <- NULL
  if (!is.null(obs_ptr)) {
    rep <- .v3cpp$cpp_observer_report(obs_ptr, length(frozen[["grid"]]) - 1L)
    obs <- v3_observer_report(setup, observer, NULL, list(status = fr$.raw_status, islands = lapply(fr$log_Z_r, function(z) list(log_Z = z))), rep)
    if (!is.null(fit$calibration)) {
      st0 <- obs$start
      w <- c(if (!is.null(observer[["truth"]])) list(truth = as.integer(observer[["truth"]])), list(start_mode = st0$start_mode$model),
             v3_observer_names(lapply(observer[["watch"]] %||% list(), as.integer), "watch"))
      obs$calibration <- v3_observer_calibration(fit$calibration, w)
    }
  }
  fr$.raw_status <- NULL
  if (!is.null(fit$calibration)) {   # calibration flags (M §2, §6.9) next to the final flags
    cf <- fit$calibration$flags
    fr$flags$escalated <- cf$escalated; fr$flags$checks_passed_calibration <- cf$checks_passed_calibration
    fr$flags$forced_pilot_steps <- cf$forced_pilot_steps; fr$flags$grid_unconverged <- cf$grid_unconverged
    fr$flags$calibration_triggers <- cf$triggers_fired
  }
  keep <- setdiff(names(fr), c("opts"))
  for (nm in keep) fit[[nm]] <- fr[[nm]]
  fit$status <- fr$status
  if (!is.null(obs)) fit$observer <- obs
  finish(fit)
}
