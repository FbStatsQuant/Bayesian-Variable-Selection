# v3_calib.R -- calibration layer (CORE_SPEC v2 §10; M §§6.1, 6.6-6.9; rulings R3-R6). Pure rules and the islands are
# in cpp/ (v3_calib.h, cpp_cal_* in v3_core.cpp); this file orchestrates the pilot, V, grid, rebuild loop, checks,
# escalation and the freeze.

# Testing interfaces (B1, B2). v3_pilot_schedule: the pilot next-phi rule applied repeatedly to a FIXED supplied
# discrepancy vector (threshold 0.9 H; floor 1/T_e). v3_build_grid: grid construction on a supplied frozen V.
v3_pilot_schedule <- function(d_vector, H, T_e) .v3cpp$cpp_pilot_schedule(as.numeric(d_vector), as.numeric(H), as.integer(T_e))
v3_build_grid <- function(logg0_V, d_V, pilot_temps, T_e)
  .v3cpp$cpp_build_grid(as.numeric(logg0_V), as.numeric(d_V), as.numeric(pilot_temps), as.integer(T_e))

# Calibration settings at tier e (M §3): H_e, T_e, L, ell; test-only overrides (recorded in the settings):
# opts[["H"]] (pilot and diagnostic particles at tier 0; x4 at tier 1), opts[["T_e_override"]] (stage ceiling T_e:
# a scalar applies to both tiers, a length-2 vector gives tier 0 and tier 1), opts[["ell"]] (rebuild budget and
# local-search move limit), opts[["L"]].
v3_cal_settings <- function(setup, opts, tier) {
  b <- setup$budgets
  Te <- opts[["T_e_override"]]
  Te <- if (is.null(Te)) b$tiers$T[tier + 1] else if (length(Te) == 2) Te[tier + 1] else Te
  H <- if (is.null(opts[["H"]])) b$tiers$H[tier + 1] else opts[["H"]] * 4^tier
  list(tier = tier, H = as.integer(H), T_e = as.integer(Te), L = as.integer(opts[["L"]] %||% b$L), Hm = 4L,
       ell = as.integer(opts[["ell"]] %||% b$ell),
       overrides = opts[intersect(names(opts), c("H", "T_e_override", "ell", "L", "calibration_seed", "escalate"))])
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
v3_cal_tier <- function(state, setup, tier, opts) {
  cs <- v3_cal_settings(setup, opts, tier)
  t_all <- proc.time()[["elapsed"]]
  out <- list(tier = tier, settings = cs, status = "ok")
  fail <- function(x) { out$status <- "numerical_failure"; out$message <- x$message; out }
  pil <- .v3cpp$cpp_cal_pilot(state, tier, cs$H, cs$T_e, cs$L, cs$Hm, cs$ell)
  if (pil$status != "ok") return(fail(pil))
  out$pilot <- list(schedule = pil$schedule, forced_pilot_steps = pil$forced_pilot_steps, stream = pil$stream, local_search = pil$local_search,
                    best_before_local = pil$best_before_local, best_after_local = pil$best_after_local, seconds = pil$seconds,
                    calibration_estimate = list(label = "calibration estimate (pilot); never reported as the estimate",
                                                log_Z = pil$island$log_Z, pip = setNames(pil$island$pip, setup$ctx$orig),
                                                ess = pil$island$ess, log_increment = pil$island$log_increment))
  improved <- v3_E3_fires
  E3 <- improved(pil); llim <- isTRUE(pil$local_search$local_limit)
  trig <- list(E1 = FALSE, E2 = FALSE, E3 = E3, forced_pilot_steps = pil$forced_pilot_steps > 0, grid_failure = FALSE,
               grid_unconverged = FALSE, local_limit = llim)
  if (isTRUE(opts[["switch_no_candidate_grid"]])) {
    # E4 arm: no candidate grid; the pilot schedule is frozen as the final grid (recommendation-only arm)
    out$grid <- pil$schedule; out$grid_source <- "pilot_schedule (switch_no_candidate_grid)"
    out$triggers <- trig; out$iterations <- list(); out$snapshots <- list()
    out$seconds <- c(pilot = sum(pil$seconds), total = proc.time()[["elapsed"]] - t_all)
    return(out)
  }
  p <- setup$ctx$p
  snapshots <- list(); grids <- list(); iters <- list(); t_grid <- 0; evals <- 0
  build <- function(label) {
    V <- .v3cpp$cpp_cal_V(state)
    g <- v3_build_grid(V$log_gamma0, V$d, pil$schedule, cs$T_e)
    snapshots[[length(snapshots) + 1]] <<- c(list(label = label), v3_V_snapshot(V, p))
    grids[[length(grids) + 1]] <<- list(label = label, grid = g$grid, ok = g$ok, reason = g$reason, intervals = g$intervals,
                                        F_V_evaluations = g$F_V_evaluations, seconds = g$seconds)
    t_grid <<- t_grid + g$seconds; evals <<- evals + g$F_V_evaluations
    g
  }
  g <- build("preliminary")
  if (!g$ok) trig$grid_failure <- TRUE
  converged <- FALSE
  if (g$ok) {
    for (it in seq_len(cs$ell)) {
      dg <- .v3cpp$cpp_cal_diag(state, tier, g$grid, cs$H, cs$L, cs$Hm, cs$ell, it)
      if (dg$status != "ok") return(fail(dg))
      E1 <- any(dg$island_best < dg$best_after_local$F - 1)          # R5 island bests vs the overall best
      E2 <- stats::sd(dg$log_Z_r) > 1
      E3it <- improved(dg)
      iters[[it]] <- list(iteration = it, grid = g$grid, streams = dg$streams, log_Z_r = dg$log_Z_r, island_best = dg$island_best,
                          overall_best = dg$best_after_local$F, E1 = E1, E2 = E2, E3 = E3it,
                          local_search = dg$local_search, seconds = dg$seconds,
                          calibration_estimate = list(label = "calibration estimate (diagnostic islands); never reported",
                                                      log_Z_r = dg$log_Z_r,
                                                      pip_r = sapply(dg$islands, function(x) x$pip),
                                                      ess = lapply(dg$islands, function(x) x$ess)))
      trig$E3 <- trig$E3 || E3it; trig$local_limit <- trig$local_limit || isTRUE(dg$local_search$local_limit)
      gn <- build(paste0("rebuild_", it))
      if (!gn$ok) { trig$grid_failure <- TRUE; break }
      if (identical(gn$grid, g$grid)) { converged <- TRUE; break }     # exact equality of the temperature vector
      g <- gn
    }
    if (length(iters)) { last <- iters[[length(iters)]]; trig$E1 <- last$E1; trig$E2 <- last$E2 }
    if (!trig$grid_failure && !converged) trig$grid_unconverged <- TRUE
  }
  out$grid <- if (trig$grid_failure) NULL else g$grid
  out$grid_source <- "candidate grid"
  out$converged <- converged; out$rebuilds <- length(iters)
  out$triggers <- trig; out$iterations <- iters; out$snapshots <- snapshots; out$grids <- grids
  out$grid_construction <- list(seconds = t_grid, F_V_evaluations = evals)
  out$seconds <- c(pilot = sum(pil$seconds), rebuild_islands = sum(vapply(iters, function(x) x$seconds[["islands"]], 0)),
                   rebuild_local = sum(vapply(iters, function(x) x$seconds[["local"]], 0)), grid_construction = t_grid,
                   total = proc.time()[["elapsed"]] - t_all)
  out
}

# v3_calibrate(setup, seed, tier = 0, opts = list()) (CORE_SPEC §10): calibration starting at `tier`; at most one
# escalation to tier 1 (leaders kept, R3), decided before any final randomness; freeze. Returns status ("ok",
# "schedule_limit", "numerical_failure", "resource_limit"), `frozen` (v3_frozen with inherited leaders and HPM),
# `tiers` (archives), `flags`, `hpm`. opts[["calibration_seed"]] (test only) replaces `seed` for streams 0-9.
# preflight (internal) = function(tier) returning TRUE if the allocation would be exceeded before that tier.
v3_calibrate <- function(setup, seed, tier = 0, opts = list(), .obs_ptr = NULL, preflight = NULL) {
  t0 <- proc.time()[["elapsed"]]
  cseed <- opts[["calibration_seed"]] %||% seed
  v3_check_seed(seed); v3_check_seed(cseed, "calibration_seed")
  ro <- list(dump_scored = isTRUE(opts[["dump_scored"]]),
             cache_capacity = as.numeric(opts[["cache_capacity"]] %||% max(500 * setup$ctx$p, 2^15)))
  state <- .v3cpp$cpp_cal_new(setup$ptr, as.numeric(cseed), ro, .obs_ptr)
  tiers <- list(); status <- "ok"; e <- tier; blocked <- NULL
  repeat {
    a <- v3_cal_tier(state, setup, e, opts)
    tiers[[length(tiers) + 1]] <- a
    if (a$status != "ok") { status <- a$status; break }
    fired <- any(unlist(a$triggers))
    if (!fired || e == 1 || isFALSE(opts[["escalate"]])) break
    # preflight again before the escalation (M §8.6); if it fails the escalation does not happen (review RC-3)
    if (!is.null(preflight) && isTRUE(preflight(1))) { status <- "resource_limit"; blocked <- "resource_limit"; break }
    e <- 1                                                              # one escalation at most
  }
  ex <- .v3cpp$cpp_cal_export(state)
  last <- tiers[[length(tiers)]]
  if (status == "ok" && is.null(last$grid)) status <- if (e == 1) "schedule_limit" else "grid_failure_no_escalation"
  out <- list(status = status, calibration_seed = cseed, tier_final = e, escalated = e == 1 && tier == 0,
              escalation_blocked = blocked, tiers = tiers, hpm = ex$inherited$hpm, ledger = ex$ledger, cache = ex$cache)
  if (!is.null(last$triggers)) {
    tr <- last$triggers
    out$flags <- list(escalated = out$escalated, escalation_blocked = blocked, checks_passed_calibration = !any(unlist(tr)),
                      forced_pilot_steps = sum(vapply(tiers, function(x) x$pilot$forced_pilot_steps %||% 0L, 0)),
                      grid_unconverged = isTRUE(tr$grid_unconverged), triggers_fired = names(tr)[unlist(tr)],
                      triggers_by_tier = lapply(tiers, function(x) x$triggers))
  }
  if (status == "ok") {
    N <- opts[["N"]] %||% setup$budgets$tiers$N[e + 1]
    out$frozen <- v3_frozen(last$grid, tier = e, N = N, L = last$settings$L, inherited = ex$inherited, budgets = setup$budgets)
    out$frozen$source <- if (isTRUE(opts[["switch_no_candidate_grid"]])) "calibration (switch_no_candidate_grid)" else "calibration"
  }
  out$seconds <- proc.time()[["elapsed"]] - t0
  out
}

# Observer view of the calibration (§8.5): watched-model membership in every frozen V snapshot, grid per rebuild,
# triggers fired. Reads the operational archive only.
v3_observer_calibration <- function(cal, watched) {
  wk <- vapply(watched, function(S) paste(S, collapse = ","), "")
  per_tier <- lapply(cal$tiers, function(a) {
    snaps <- a$snapshots %||% list()
    mem <- if (length(snaps)) t(vapply(snaps, function(s) { k <- vapply(s$models, paste, "", collapse = ","); wk %in% k }, logical(length(wk))))
           else NULL
    if (!is.null(mem)) { mem <- matrix(mem, nrow = length(snaps)); dimnames(mem) <- list(vapply(snaps, `[[`, "", "label"), names(watched)) }
    list(tier = a$tier, watched_in_V = mem, V_truncated = vapply(snaps, function(s) isTRUE(s$truncated), TRUE),
         grids = lapply(a$grids %||% list(), function(g) g$grid), triggers = a$triggers)
  })
  per_tier
}
