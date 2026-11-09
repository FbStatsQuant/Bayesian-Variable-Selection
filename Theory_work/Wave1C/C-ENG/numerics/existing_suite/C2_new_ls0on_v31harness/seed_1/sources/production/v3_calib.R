# v3_calib.R -- calibration layer (CORE_SPEC v2 §10; M §§6.1, 6.6-6.9; rulings R3-R6). Pure rules and the islands are
# in cpp/ (v3_calib.h, cpp_cal_* in v3_core.cpp); this file orchestrates the pilot, V, grid, rebuild loop, checks,
# escalation and the freeze.

v3_build_grid <- function(logg0_V, d_V, pilot_temps, T_e)
  .v3cpp$cpp_build_grid(as.numeric(logg0_V), as.numeric(d_V), as.numeric(pilot_temps), as.integer(T_e))

# Calibration budgets are fixed by Part I; no profiling overrides.
v3_cal_settings <- function(setup, tier) {
  b <- setup$budgets
  list(tier = tier, H = as.integer(b$tiers$H[tier + 1]), T_e = as.integer(b$tiers$T[tier + 1]),
       L = as.integer(b$L), Hm = 4L, ell = as.integer(b$ell))
}

# V snapshot for the archive (§8.5): every model of V with log gamma_0 and d when p <= 25, else the top 10^4 by
# log gamma_1 = log gamma_0 + d (ties: V order). The full V is always used for the construction itself.
v3_V_snapshot <- function(V, p) {
  n <- length(V$models)
  keep <- if (p <= 25 || n <= 1e4) seq_len(n) else order(-(V$log_gamma0 + V$d), seq_len(n))[1:1e4]
  list(size = n, truncated = length(keep) < n, models = V$models[keep], log_gamma0 = V$log_gamma0[keep], d = V$d[keep])
}

# E3 (lead ruling RC-1, consistent with R14): fires iff the global best's F strictly increased during a calibration
# local search; an exact-F change of the reported model through the tie rule does not fire E3.
v3_E3_fires <- function(x) x$best_after_local$F > x$best_before_local$F

# One calibration tier (M §6.1 CALIBRATION(e)). Returns the archive of the tier, its grid and triggers.
v3_cal_tier <- function(state, setup, tier, runtime = NULL) {
  cs <- v3_cal_settings(setup, tier)
  t_all <- proc.time()[["elapsed"]]
  out <- list(tier = tier, settings = cs, status = "ok")
  tier_env <- environment()
  fail <- function(x) {
    out$status <- x$status; out$message <- x$message
    out$partial_results <- TRUE; out$partial_operation <- x
    # Preserve previous successful grid builds, snapshots and diagnostic iterations on a later stop.
    for (nm in c("snapshots", "grids", "iters")) if (exists(nm, envir = tier_env, inherits = FALSE)) out[[if (nm == "iters") "iterations" else nm]] <- get(nm, envir = tier_env, inherits = FALSE)
    if (exists("trig", envir = tier_env, inherits = FALSE)) out$triggers <- trig
    if (exists("t_grid", envir = tier_env, inherits = FALSE))
      out$grid_construction <- list(seconds = t_grid, F_V_evaluations = evals)
    out$seconds_total <- proc.time()[["elapsed"]] - t_all
    out
  }
  pil <- .v3cpp$cpp_cal_pilot(state, tier, cs$H, cs$T_e, cs$L, cs$Hm, cs$ell)
  if (!is.null(pil$local_search)) {
    pil$local_search$phase <- "pilot"; pil$local_search$tier <- tier
    pil$local_search$iter <- 0L; pil$local_search$island <- 0L
  }
  out$pilot <- list(schedule = pil$schedule, forced_pilot_steps = pil$forced_pilot_steps, stream = pil$stream, stage_record = pil$island, local_search = pil$local_search,
                    best_before_local = pil$best_before_local, best_after_local = pil$best_after_local, seconds = pil$seconds,
                    partial = pil$status != "ok",
                    calibration_estimate = list(label = "calibration estimate (pilot); partial if stopped; never reported as the estimate",
                                                partial = pil$status != "ok",
                                                log_Z = pil$island$log_Z,
                                                pip = if (length(pil$island$pip)) setNames(pil$island$pip, setup$ctx$orig) else NULL,
                                                ess = pil$island$ess, log_increment = pil$island$log_increment))
  if (pil$status != "ok") return(fail(pil))
  improved <- v3_E3_fires
  E3 <- improved(pil); llim <- isTRUE(pil$local_search$local_limit)
  trig <- list(E1 = FALSE, E2 = FALSE, E3 = E3, forced_pilot_steps = pil$forced_pilot_steps > 0, grid_failure = FALSE,
               grid_unconverged = FALSE, local_limit = llim)
  p <- setup$ctx$p
  snapshots <- list(); grids <- list(); iters <- list(); t_grid <- 0; evals <- 0
  build <- function(label) {
    t_build <- proc.time()[["elapsed"]]
    V <- .v3cpp$cpp_cal_V(state)
    if (identical(V$status, "numerical_failure")) return(V)
    g <- v3_build_grid(V$log_gamma0, V$d, pil$schedule, cs$T_e)
    snapshots[[length(snapshots) + 1]] <<- c(list(label = label), v3_V_snapshot(V, p))
    g$label <- label
    grids[[length(grids) + 1]] <<- list(label = label, grid = g$grid, rho_appended = g$rho_appended,
                                        ok = g$ok, reason = g$reason, intervals = g$intervals,
                                        F_V_evaluations = g$F_V_evaluations, seconds = g$seconds)
    t_grid <<- t_grid + g$seconds; evals <<- evals + g$F_V_evaluations
    g$resource_limit <- !is.null(runtime) && .v3cpp$cpp_runtime_check(runtime,
      proc.time()[["elapsed"]] - t_build, "grid_construction", as.integer(tier), as.integer(length(grids) - 1L))
    g
  }
  g <- build("preliminary")
  if (identical(g$status, "numerical_failure")) return(fail(g))
  if (isTRUE(g$resource_limit)) return(fail(c(g, list(status = "resource_limit"))))
  if (!g$ok) trig$grid_failure <- TRUE
  converged <- FALSE
  if (g$ok) {
    for (it in seq_len(cs$ell)) {
      dg <- .v3cpp$cpp_cal_diag(state, tier, g$grid, cs$H, cs$L, cs$Hm, cs$ell, it)
      if (!is.null(dg$local_search)) {
        dg$local_search$phase <- "diag"; dg$local_search$tier <- tier
        dg$local_search$iter <- it; dg$local_search$island <- "all"
      }
      # Archive completed islands and any completed local search before inspecting stop status.
      iters[[it]] <- list(iteration = it, grid = g$grid, rho_V = g$rho_appended, grid_label = g$label,
                          streams = dg$streams, log_Z_r = dg$log_Z_r, island_best = dg$island_best,
                          stage_record = dg$islands, local_search = dg$local_search, seconds = dg$seconds,
                          partial = dg$status != "ok",
                          calibration_estimate = list(label = "calibration estimate (diagnostic islands); partial if stopped; never reported",
                                                      partial = dg$status != "ok", log_Z_r = dg$log_Z_r,
                                                      pip_r = lapply(dg$islands, function(x) x$pip),
                                                      ess = lapply(dg$islands, function(x) x$ess)))
      if (dg$status != "ok") return(fail(dg))
      E1 <- any(dg$island_best < dg$best_after_local$F - 1)          # R5 island bests vs the overall best
      E2 <- stats::sd(dg$log_Z_r) > 1
      E3it <- improved(dg)
      iters[[it]]$overall_best <- dg$best_after_local$F
      iters[[it]]$E1 <- E1; iters[[it]]$E2 <- E2; iters[[it]]$E3 <- E3it
      iters[[it]]$calibration_estimate$pip_r <- sapply(dg$islands, function(x) x$pip)
      # These checks belong to the last completed diagnostic, including when
      # the following V/grid rebuild stops with a numerical or resource failure.
      trig$E1 <- E1; trig$E2 <- E2
      trig$E3 <- trig$E3 || E3it; trig$local_limit <- trig$local_limit || isTRUE(dg$local_search$local_limit)
      gn <- build(paste0("rebuild_", it))
      if (identical(gn$status, "numerical_failure")) return(fail(gn))
      if (isTRUE(gn$resource_limit)) return(fail(c(gn, list(status = "resource_limit"))))
      if (!gn$ok) { trig$grid_failure <- TRUE; break }
      if (identical(gn$grid, g$grid)) { g <- gn; converged <- TRUE; break } # same temperatures; retain latest construction metadata
      g <- gn
    }
    if (!trig$grid_failure && !converged) trig$grid_unconverged <- TRUE
  }
  out$grid <- if (trig$grid_failure) NULL else g$grid
  out$rho_V <- if (trig$grid_failure) NULL else g$rho_appended
  out$grid_label <- if (trig$grid_failure) NULL else g$label
  out$grid_source <- "candidate grid"
  out$converged <- converged; out$rebuilds <- length(iters)
  out$triggers <- trig; out$iterations <- iters; out$snapshots <- snapshots; out$grids <- grids
  out$grid_construction <- list(seconds = t_grid, F_V_evaluations = evals)
  out$seconds <- c(pilot = sum(pil$seconds), rebuild_islands = sum(vapply(iters, function(x) x$seconds[["islands"]], 0)),
                   rebuild_local = sum(vapply(iters, function(x) x$seconds[["local"]], 0)), grid_construction = t_grid,
                   total = proc.time()[["elapsed"]] - t_all)
  out
}

# Production calibration: at most one escalation; persistent stores and independent streams.
# preflight (internal) = function(tier) returning TRUE if the allocation would be exceeded before that tier.
v3_calibrate <- function(setup, seed, tier = 0, preflight = NULL, runtime = NULL) {
  t0 <- proc.time()[["elapsed"]]
  cseed <- seed; v3_check_seed(seed)
  ro <- list(cache_capacity = as.numeric(500 * setup$ctx$p))
  state <- .v3cpp$cpp_cal_new(setup$ptr, as.numeric(cseed), ro, runtime)
  tiers <- list(); status <- "ok"; e <- tier; blocked <- NULL
  repeat {
    a <- v3_cal_tier(state, setup, e, runtime)
    tiers[[length(tiers) + 1]] <- a
    if (a$status != "ok") { status <- a$status; break }
    fired <- any(unlist(a$triggers))
    if (!fired || e == 1) break
    # preflight again before the escalation (M §8.6); if it fails the escalation does not happen (review RC-3)
    if (!is.null(preflight) && isTRUE(preflight(1))) { status <- "resource_limit"; blocked <- "resource_limit"; break }
    e <- 1                                                              # one escalation at most
  }
  ex <- .v3cpp$cpp_cal_export(state)
  last <- tiers[[length(tiers)]]
  if (status == "ok" && is.null(last$grid)) status <- if (e == 1) "schedule_limit" else "grid_failure_no_escalation"
  out <- list(status = status, calibration_seed = cseed, tier_final = e, escalated = e == 1 && tier == 0,
              escalation_blocked = blocked, tiers = tiers, hpm = ex$inherited$hpm, ledger = ex$ledger, cache = ex$cache)
  out$stage_table <- v3_bind_records(lapply(tiers, function(x) {
    v3_bind_records(c(list(v3_stage_table(list(x$pilot$stage_record))),
      lapply(x$iterations, function(it) v3_stage_table(it$stage_record, it$rho_V, it$grid_label))))
  }))
  tr <- last$triggers
  out$flags <- list(escalated = out$escalated, escalation_blocked = blocked,
                      checks_passed_calibration = if (last$status == "ok" && !is.null(tr)) !any(unlist(tr)) else NA,
                      forced_pilot_steps = sum(vapply(tiers, function(x) x$pilot$forced_pilot_steps %||% 0L, 0)),
                      grid_unconverged = isTRUE(tr$grid_unconverged), triggers_fired = names(tr)[unlist(tr)],
                      triggers_by_tier = lapply(tiers, function(x) x$triggers))
  if (status == "ok") {
    N <- setup$budgets$tiers$N[e + 1]
    out$frozen <- v3_frozen(last$grid, tier = e, N = N, L = last$settings$L, inherited = ex$inherited, budgets = setup$budgets)
    # Diagnostic metadata does not enter the computational frozen hash or final RNG.
    out$frozen$rho_V <- last$rho_V; out$frozen$grid_label <- last$grid_label
    out$frozen$source <- "calibration"
  }
  out$seconds <- proc.time()[["elapsed"]] - t0
  out
}

