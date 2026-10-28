# v3_run.R -- final run on a frozen grid and its outputs; replication; trace; step/round samplers; local search.
# CORE_SPEC v2 §§4-7; M §§6.5, 6.8, 6.10-6.12. Loops are in cpp/v3_engine.h; this file validates and assembles.

v3_log_sum_exp <- function(x) { m <- max(x); if (!is.finite(m)) return(m); m + log(sum(exp(x - m))) }

# Frozen-calibration object (CORE_SPEC §6): grid, tier e, N_e, L, inherited state. Core layer: grid supplied,
# inherited state empty (or list(models = list(...)) of models offered to the stores with provenance "inherited").
v3_frozen <- function(grid, tier = 0, N = NULL, L = NULL, inherited = NULL, budgets = NULL) {
  grid <- as.numeric(grid)
  v3_check_grid(grid)
  fr <- list(grid = grid, tier = as.integer(tier), N = N %||% (if (!is.null(budgets)) budgets$tiers$N[tier + 1]),
             L = L %||% (if (!is.null(budgets)) budgets$L), inherited = inherited, source = "supplied")
  fr$sha256 <- digest::digest(fr[c("grid", "tier", "N", "L", "inherited")], algo = "sha256")
  class(fr) <- "v3_frozen"
  fr
}
v3_check_grid <- function(grid) {
  if (!is.numeric(grid) || length(grid) < 2 || any(!is.finite(grid))) stop("grid must be a finite numeric vector of length >= 2")
  if (grid[1] != 0 || grid[length(grid)] != 1) stop("grid must start at exactly 0 and end at exactly 1")
  if (any(diff(grid) <= 0)) stop("grid must be strictly increasing")
  invisible(TRUE)
}

# Resolved run settings: budgets of M §3 unless overridden by test/experiment opts (recorded in the output).
v3_run_settings <- function(setup, frozen, opts) {
  b <- setup$budgets; tier <- frozen[["tier"]] %||% 0L
  list(N = as.integer(opts[["N"]] %||% frozen[["N"]] %||% b$tiers$N[tier + 1]),
       L = as.integer(opts[["L"]] %||% frozen[["L"]] %||% b$L),
       measured_rounds = as.integer(opts[["measured_rounds"]] %||% 4L),
       islands = as.integer(opts[["islands"]] %||% 4L),
       tier = as.integer(tier), ell = as.integer(opts[["ell"]] %||% b$ell),
       dump_scored = isTRUE(opts[["dump_scored"]]), resampler_trace = isTRUE(opts[["resampler_trace"]]),
       cache_capacity = as.numeric(opts[["cache_capacity"]] %||% max(500 * setup$ctx$p, 2^15)))
}

v3_model_key <- function(S) paste(S, collapse = ",")

# Assemble the reported outputs of a final run (CORE_SPEC §6, §7; M §§6.9-6.12).
v3_assemble_final <- function(raw, setup, frozen, ro, seed, opts) {
  isl <- raw$islands
  out <- list(status = raw$status, message = raw$message, seed = seed, settings = ro,
              frozen_sha256 = frozen[["sha256"]], grid = frozen[["grid"]], B = setup$B, stream_map = c(final_islands = "10..13 (stream = 9 + r)"))
  led <- raw$ledger
  out$hpm <- led$hpm$model; out$hpm_F <- led$hpm$F; out$hpm_provenance <- led$hpm$provenance
  if (raw$status != "completed") {   # numerical_failure: best scored model so far, labelled incomplete (M §2)
    out$ledger <- led; out$hpm_incomplete <- TRUE; out$estimates_available <- FALSE; return(out)
  }
  logZr <- vapply(isl, function(r) r$log_Z, 0)
  R <- length(isl)
  out$log_Z_r <- logZr
  out$log_Z <- v3_log_sum_exp(logZr) - log(R)                    # pooled Zhat = (1/R) sum_r Zhat_r (log-sum-exp)
  out$log_Z_lower95 <- log(0.05) + out$log_Z                     # Markov bound 0.05 Zhat (one-sided)
  out$log_Z_rel_m0 <- out$log_Z - raw$log_m0                     # relative to m(empty)
  out$log_Z_r_rel_m0 <- logZr - raw$log_m0
  out$log_increment <- lapply(isl, function(r) r$log_increment)  # per island, per stage (reconstructs W_t, PW2)
  P <- do.call(cbind, lapply(isl, function(r) r$pip))
  w <- exp(logZr - max(logZr)); w <- w / sum(w)
  orig <- setup$ctx$orig
  out$pip_r <- P; rownames(out$pip_r) <- orig
  out$pip_primary <- setNames(rowMeans(P), orig)                 # equal-weight mean over islands (M §6.11)
  out$pip_secondary <- setNames(drop(P %*% w), orig)             # sum_r Zhat_r PIP_r / sum_r Zhat_r
  out$mpm <- as.integer(orig[out$pip_primary > 0.5])
  # per-stage table
  out$stage_table <- do.call(rbind, lapply(seq_len(R), function(r) {
    x <- isl[[r]]; m <- x$stage_moves
    data.frame(island = r, stage = seq_along(x$phi), phi = x$phi, ess = x$ess, log_increment = x$log_increment,
               cum_log_Z = x$cum_log_Z, distinct_resampled = x$distinct_resampled, distinct_moved = x$distinct_moved,
               acc_gibbs_change = m$gibbs_state_changes / pmax(m$gibbs, 1), acc_uswap = m$uswap_acc / pmax(m$uswap_exec, 1),
               acc_nswap = m$nswap_acc / pmax(m$nswap_exec, 1), acc_indep = m$indep_acc / pmax(m$indep_exec, 1),
               m[, c("uswap_exec", "uswap_self", "nswap_exec", "nswap_reject_noscore", "nswap_self", "indep_exec")])
  }))
  out$terminal_table <- do.call(rbind, lapply(seq_len(R), function(r) {
    x <- isl[[r]]; m <- x$terminal_moves; Lr <- ro$L
    data.frame(island = r, phase = c(rep("burn_in", Lr), rep("measured", ro$measured_rounds)),
               round = c(seq_len(Lr), seq_len(ro$measured_rounds)), distinct = x$terminal_distinct, m)
  }))
  # HPM, near ties (M §6.10)
  top <- led$top
  near <- which(top$value >= out$hpm_F - 1e-9)
  out$near_ties <- top$models[near]; out$near_tie_F <- top$value[near]
  out$near_tie_truncated <- isTRUE(top$full) && min(top$value) >= out$hpm_F - 1e-9
  # final local search and flags (M §6.9-6.10; R4, R5)
  ls <- raw$local_search
  ls$phase <- "final"; ls$tier <- ro$tier; ls$island <- "final"     # archive labels (CORE_SPEC §7, R4)
  out$local_search <- ls
  out$local_limit <- isTRUE(ls$local_limit)
  out$local_certified <- isTRUE(ls$local_certified)   # R14: refers to the search's returned model (may differ from
                                                       # the HPM only by an exact-F tie won under the HPM tie rule)
  out$global_certified <- FALSE
  hb <- raw$hpm_before_local
  E1 <- any(led$island_best < out$hpm_F - 1)
  E2 <- R >= 2 && stats::sd(logZr) > 1
  E3 <- out$hpm_F > hb$F   # strict F increase of the global best in the final local search (ruling RC-1, M §6.9)
  lowESS <- any(out$stage_table$ess < 0.5 * ro$N)
  out$flags <- list(E1 = E1, E2 = E2, E3 = E3, low_empirical_ESS = lowESS, local_limit = out$local_limit,
                    near_tie_truncated = out$near_tie_truncated, checks_passed_final = !(E1 || E2 || E3 || lowESS),
                    escalated = (frozen[["tier"]] %||% 0) == 1, grid_unconverged = NA, forced_pilot_steps = NA,
                    checks_passed_calibration = NA)
  out$island_best <- led$island_best
  out$hpm_before_local <- hb
  out$leaders_gamma0 <- led$leaders_gamma0; out$leaders_gamma1 <- led$leaders_gamma1; out$top_store <- led$top
  out$score_counts <- list(logical = led$logical, fresh = led$fresh)   # mechanisms incl. gibbs_held / gibbs_flip (R15)
  out$cache <- raw$cache
  if (!is.null(led$dump)) out$dump_scored <- led$dump
  if (isTRUE(ro$resampler_trace)) out$resampler_trace <- lapply(isl, function(r) r$offspring)
  out$rb <- lapply(isl, function(r) list(rb_acc = r$rb_acc, rb_round = r$rb_round))
  out$timings <- list(islands = do.call(rbind, lapply(isl, function(r) r$seconds)), local = raw$seconds_local,
                      final_total = raw$seconds_total)
  out$log_m0 <- raw$log_m0; out$log_Zbar0 <- raw$log_Zbar0
  out$estimates_available <- TRUE
  out
}

# v3_final_run(setup, frozen, seed, observer = NULL, opts = list()) (CORE_SPEC §6).
# .obs_ptr (internal, v3_fit): an observer object shared with the calibration; its report is assembled by the caller.
v3_final_run <- function(setup, frozen, seed, observer = NULL, opts = list(), .obs_ptr = NULL) {
  stopifnot(inherits(setup, "v3_setup"))
  if (!inherits(frozen, "v3_frozen")) frozen <- v3_frozen(frozen[["grid"]], frozen[["tier"]] %||% 0, frozen[["N"]], frozen[["L"]], frozen[["inherited"]], setup$budgets)
  v3_check_grid(frozen[["grid"]])
  v3_check_seed(seed)
  ro <- v3_run_settings(setup, frozen, opts)
  obs <- if (!is.null(.obs_ptr)) .obs_ptr else if (!is.null(observer)) v3_observer_prepare(setup, observer) else NULL
  raw <- .v3cpp$cpp_final_run(setup$ptr, frozen[["grid"]], ro, as.numeric(seed), obs, frozen[["inherited"]], NULL, NULL, FALSE)
  out <- v3_assemble_final(raw, setup, frozen, ro, seed, opts)
  out$opts <- opts
  if (!is.null(observer) && is.null(.obs_ptr)) out$observer <- v3_observer_report(setup, observer, obs, raw)
  if (!is.null(.obs_ptr)) out$.raw_status <- raw$status
  out
}

# v3_replicate_final(setup, frozen, seeds, opts): for each seed, log Zhat_r per island, PIP_r and per-stage
# increments; loop in C++ (A11, E4). Replication s equals v3_final_run(seed = seeds[s]) island by island.
v3_replicate_final <- function(setup, frozen, seeds, opts = list()) {
  if (!inherits(frozen, "v3_frozen")) frozen <- v3_frozen(frozen[["grid"]], frozen[["tier"]] %||% 0, frozen[["N"]], frozen[["L"]], NULL, setup$budgets)
  ro <- v3_run_settings(setup, frozen, opts)
  v3_check_seed(seeds, "seeds")
  r <- .v3cpp$cpp_replicate(setup$ptr, frozen[["grid"]], ro, as.numeric(seeds))
  dimnames(r$pip) <- list(NULL, NULL, setup$ctx$orig)
  c(r, list(seeds = seeds, settings = ro, frozen_sha256 = frozen[["sha256"]], log_m0 = setup$ctx$log_m0,
            log_Zbar0 = setup$start$log_Zbar0))
}

# v3_trace(setup, init_states, grid, opts, variates = NULL) (CORE_SPEC §4): complete execution trace of a tiny final
# run. init_states = list of N models used as the initial population of every island (NULL: iid pi_0 draws).
# variates = list(uniforms = numeric vector consumed in order, orders = list of label vectors (character, e.g.
# c("G2","U","N1","G1","I")) one per particle-round in execution order, draws = list of models consumed in order by
# every pi_0 draw (initial draws when init_states is NULL, and independence proposals)). Any element may be absent;
# absent pieces come from the seeded streams. opts: N, islands (default 1), L, measured_rounds, seed (default 1).
v3_trace <- function(setup, init_states, grid, opts = list(), variates = NULL) {
  if (!is.null(init_states)) opts[["N"]] <- length(init_states)
  opts[["islands"]] <- opts[["islands"]] %||% 1L
  opts[["dump_scored"]] <- TRUE
  frozen <- v3_frozen(grid, 0, budgets = setup$budgets)
  ro <- v3_run_settings(setup, frozen, opts)
  if (ro$N > 4 || setup$ctx$p > 6) warning("v3_trace is meant for N <= 4, p <= 6")
  init <- if (is.null(init_states)) NULL else lapply(init_states, as.integer)
  seed <- opts[["seed"]] %||% 1
  v3_check_seed(seed, "opts$seed")
  raw <- .v3cpp$cpp_final_run(setup$ptr, frozen[["grid"]], ro, as.numeric(seed), NULL, NULL, init, variates, TRUE)
  out <- v3_assemble_final(raw, setup, frozen, ro, seed, opts)
  out$trace <- raw$trace
  out$variate_order_doc <- paste(
    "Per island r (stream 9 + r, or the prescribed uniforms continuing across islands):",
    "initial draws (pi0_size, pi0_block_size for b = J..1 while remaining > 0, pi0_submodel for b = 1..J with k_b > 0);",
    "then per stage: N 'resample' uniforms, then particle 1..N each a round: m - 1 'order' uniforms (Fisher-Yates,",
    "i = m..2, j = floor(u i) + 1) unless prescribed, then per step: Gibbs 1 ('gibbs'); U: none at |S| in {0,p} else",
    "uswap_j, uswap_l, uswap_accept; N: none at S empty, else nswap_j, then (if N(j)\\S nonempty) nswap_l,",
    "nswap_accept; I: pi_0 draw uniforms then indep_accept; then L burn-in and measured rounds the same way.")
  out
}

# Elementary-step and round samplers (CORE_SPEC §4). Labels "G<j>" (j = original index), "U", "N<b>", "I".
# Returns data.frame(state = key "j1,j2,...", count). Stream 100 of `seed`.
v3_step_sample <- function(setup, S, label, phi, M, seed) {
  v3_check_seed(seed)
  r <- .v3cpp$cpp_step_sample(setup$ptr, as.integer(S), as.character(label), as.numeric(phi), as.numeric(M), as.numeric(seed))
  data.frame(state = r$state, count = r$count, stringsAsFactors = FALSE)
}
v3_round_sample <- function(setup, S, phi, M, seed, trace = FALSE) {
  v3_check_seed(seed)
  r <- .v3cpp$cpp_round_sample(setup$ptr, as.integer(S), as.numeric(phi), as.numeric(M), as.numeric(seed), isTRUE(trace))
  out <- data.frame(state = r$state, count = r$count, stringsAsFactors = FALSE)
  if (isTRUE(trace)) attr(out, "trace") <- r$trace
  out
}
# Multinomial resampler on fixed log weights (A17): M x N matrix of offspring counts (stream 101 of seed).
# uniforms (test option): prescribed uniforms, N per resampling (then M = length(uniforms) / N).
v3_resample_sample <- function(logw, M, seed, uniforms = numeric(0)) {
  v3_check_seed(seed)
  .v3cpp$cpp_resample_sample(as.numeric(logw), as.integer(M), as.numeric(seed), as.numeric(uniforms))
}
# Key of a model as used by the samplers ("" = empty model) and its inverse.
v3_key_to_model <- function(key) if (identical(key, "")) integer(0) else as.integer(strsplit(key, ",", fixed = TRUE)[[1]])

# v3_local_search(setup, centre, state = NULL) (CORE_SPEC §7; M §6.10). state = list(ell = ..., dump = TRUE/FALSE)
# for tests; default ell from the budgets. The ledger starts empty, so the centre is the initial best.
v3_local_search <- function(setup, centre, state = NULL) {
  ell <- state[["ell"]] %||% setup$budgets$ell
  .v3cpp$cpp_local_search(setup$ptr, as.integer(centre), as.integer(ell), isTRUE(state[["dump"]]))
}
