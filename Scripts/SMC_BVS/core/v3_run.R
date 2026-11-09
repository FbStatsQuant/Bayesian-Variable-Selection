# v3_run.R -- production final run on frozen calibration; outputs and local-search certificate.
# CORE_SPEC v2 §§4-7; M §§6.5, 6.8, 6.10-6.12. Loops are in cpp/v3_engine.h; this file validates and assembles.

v3_log_sum_exp <- function(x) { m <- max(x); if (!is.finite(m)) return(m); m + log(sum(exp(x - m))) }

# Operational reproducibility metadata, retained independently of any trace/testing surface.
v3_randomness <- function(seed) list(
  stream_map = data.frame(stream = 0:13,
    phase = c("pilot", rep("diag", 4), "pilot", rep("diag", 4), rep("final", 4)),
    tier = c(rep(0L, 5), rep(1L, 5), rep(NA_integer_, 4)),
    island = c(0L, 1:4, 0L, 1:4, 1:4)),
  seeding_doc = paste(
    "Seed =", seed, "; one serial stream per pilot/island, particles processed in order; no particle reseeding.",
    "All generator arithmetic is unsigned 64-bit modulo 2^64; x = (uint64(seed) << 32) + stream.",
    "Four successive SplitMix64 outputs seed xoshiro256** state a[0..3]:",
    "x += 0x9E3779B97F4A7C15; z=x; z=(z^(z>>30))*0xBF58476D1CE4E5B9;",
    "z=(z^(z>>27))*0x94D049BB133111EB; output=z^(z>>31).",
    "next: result=rotl(a[1]*5,7)*9; t=a[1]<<17; a[2]^=a[0]; a[3]^=a[1];",
    "a[1]^=a[2]; a[0]^=a[3]; a[2]^=t; a[3]=rotl(a[3],45); return result.",
    "rotl(z,k)=(z<<k)|(z>>(64-k)); uniform=(next>>11)*2^-53 in [0,1).",
    "Stream positions count next_uint64 calls since seeding, starting at zero (SplitMix64 seeding excluded).",
    "Diagnostic streams continue across rebuilds without reseeding; final streams 10..13 are fresh and independent of streams 0..9.",
    "Exact enumeration uses no sampler streams. See cpp/v3_util.h for the retained implementation."),
  variate_order_doc = paste(
    "Initial draws: particles 1..N, each complete pi0 draw: pi0_size (sizes 0..K),",
    "pi0_block_size for b=J..1 while remaining>0, then pi0_submodel for b=1..J with k_b>0.",
    "Within-size submodels use increasing binary inclusion code, first original-index member least significant bit;",
    "start categorical lookup uses first cumulative >u, final cumulative exactly 1.",
    "Per bridge stage: all N resample uniforms first, then particles 1..N, one complete round each.",
    "Each round: m-1 order uniforms, Fisher-Yates i=m..2, j=floor(u*i)+1,",
    "on canonical labels G1..Gp,U,N1..NB,I, m=p+B+2; then steps in the drawn order:",
    "G: one gibbs uniform even at deterministic probabilities or infeasible cap addition;",
    "U: none at size 0 or p, otherwise uswap_j,uswap_l,uswap_accept;",
    "N: none at empty S, otherwise nswap_j, then nswap_l,nswap_accept only if N(j)\\S is nonempty;",
    "I: complete pi0 draw then indep_accept, including unchanged proposals and acceptance probability 1.",
    "Uniform candidate choice uses floor(u*m)+1 on original-index sorted candidates; Bernoulli/MH succeeds iff u<probability.",
    "Resampling keeps prototype double cumulative arithmetic, final cumulative 1, zero uniform replaced by 2^-1074 without a draw,",
    "first cumulative >=u_eff via inverse-CDF guide table (forward then backward adjustment).",
    "After bridge: L burn-in then four measured rounds; particles 1..N, same round order, no resampling.",
    "N=H_e in calibration, N=N_e in final. This is the prototype bit-level consumption convention in the same numerical environment."))

v3_bind_records <- function(tables) {
  tables <- Filter(function(x) !is.null(x) && nrow(x) > 0L, tables)
  if (!length(tables)) return(data.frame())
  out <- do.call(rbind, tables); rownames(out) <- NULL; out
}

# Pure assembly: rho is copied from the grid used by these islands, never recalculated.
# Pilot stages have no frozen restricted grid and therefore rho_V is NA.
v3_stage_table <- function(islands, rho = NULL, grid_label = NA_character_) {
  v3_bind_records(lapply(islands, function(x) {
    if (is.null(x) || !length(x$phi)) return(NULL)
    n <- length(x$phi); m <- x$stage_moves
    data.frame(phase = x$phase, tier = x$tier, iter = x$iter, island = x$island,
      grid_label = grid_label, partial = isTRUE(x$partial), stage = seq_len(n), phi = x$phi,
      rho_V = if (is.null(rho)) rep(NA_real_, n) else rho[seq_len(n)],
      ess = x$ess, log_increment = x$log_increment, cum_log_Z = x$cum_log_Z,
      distinct_resampled = x$distinct_resampled, distinct_moved = x$distinct_moved,
      acc_gibbs_change = m$gibbs_state_changes / pmax(m$gibbs, 1),
      acc_uswap = m$uswap_acc / pmax(m$uswap_exec, 1),
      acc_nswap = m$nswap_acc / pmax(m$nswap_exec, 1),
      acc_indep = m$indep_acc / pmax(m$indep_exec, 1), m)
  }))
}

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

# Fixed production settings. The frozen tier is selected by calibration, before final randomness.
# ls0 (v3.1 #8, default on): append LS0 after the final local search. ls0 = FALSE reproduces v3 (no LS0 fields in the
# settings, the run or the fit). LS0 uses the production ell and the e4 tie DP of the start mode; the options
# v3.ls0_tie_dp = FALSE (v3 start-mode rule) and v3.ls0_ell (move cap override) exist for testing only.
v3_run_settings <- function(setup, frozen, ls0 = getOption("v3.ls0", TRUE)) {
  b <- setup$budgets; tier <- frozen[["tier"]] %||% 0L
  ro <- list(N = as.integer(b$tiers$N[tier + 1]), L = as.integer(b$L), measured_rounds = 4L,
       islands = 4L, tier = as.integer(tier), ell = as.integer(b$ell),
       cache_capacity = as.numeric(500 * setup$ctx$p))
  if (isTRUE(ls0)) {
    ro$ls0 <- TRUE
    ro$ls0_ell <- as.integer(getOption("v3.ls0_ell", b$ell))
    ro$ls0_tie_dp <- isTRUE(getOption("v3.ls0_tie_dp", TRUE))
  }
  ro
}

# GUARD-W / v3.1 #15: on every return without complete output, every estimate field is NA by exact name, so no
# consumer can read a partial value (e.g. fit$log_Z partially matching log_Zbar0). Partial island values stay only in
# their labelled archives (partial_final, stage_record, calibration). Used in v3.1 mode (ls0 on) only.
V3_ESTIMATE_FIELDS <- c("log_Z", "log_Z_r", "log_Z_lower95", "log_Z_rel_m0", "log_Z_r_rel_m0", "pip_primary", "pip_r", "mpm")
v3_unavailable_estimates <- function(fit) {
  for (nm in V3_ESTIMATE_FIELDS) fit[nm] <- list(NA)
  fit$estimates_available <- FALSE
  fit
}

v3_model_key <- function(S) paste(S, collapse = ",")

# Assemble the reported outputs of a final run (CORE_SPEC §6, §7; M §§6.9-6.12).
v3_assemble_final <- function(raw, setup, frozen, ro, seed) {
  isl <- raw$islands
  out <- list(status = raw$status, message = raw$message, seed = seed, settings = ro,
              frozen_sha256 = frozen[["sha256"]], grid = frozen[["grid"]], B = setup$B)
  out <- c(out, v3_randomness(seed))
  out$stream_map$tier[out$stream_map$stream >= 10L] <- ro$tier
  out$stage_record <- isl
  out$streams <- lapply(Filter(Negate(is.null), isl), function(x) x$stream)
  out$stage_table <- v3_stage_table(isl, frozen$rho_V, frozen$grid_label %||% NA_character_)
  if (length(raw$local_search)) {
    out$local_search <- raw$local_search
    out$local_search$phase <- "final"; out$local_search$tier <- ro$tier
    out$local_search$iter <- -1L; out$local_search$island <- "final"
  }
  v31 <- isTRUE(ro$ls0)
  if (v31) {
    out$start_mode <- raw$start_mode; out$hpm_before_ls0 <- raw$hpm_before_ls0
    if (length(raw$ls0)) {
      out$ls0 <- raw$ls0
      out$ls0$phase <- "ls0"; out$ls0$tier <- ro$tier; out$ls0$iter <- -1L; out$ls0$island <- "final"; out$ls0$ell <- ro$ls0_ell
    }
  }
  led <- raw$ledger
  out$hpm <- led$hpm$model; out$hpm_F <- led$hpm$F; out$hpm_provenance <- led$hpm$provenance
  if (raw$status != "completed") {   # numerical_failure: best scored model so far, labelled incomplete (M §2)
    out$ledger <- led; out$hpm_incomplete <- TRUE; out$estimates_available <- FALSE
    out$partial_results <- TRUE; out$partial_final <- raw
    out$local_certified <- FALSE; out$global_certified <- FALSE
    if (v31) out <- v3_unavailable_estimates(out)
    return(out)
  }
  logZr <- vapply(isl, function(r) r$log_Z, 0)
  R <- length(isl)
  out$stage_record <- isl
  out$log_Z_r <- logZr
  out$log_Z <- v3_log_sum_exp(logZr) - log(R)                    # pooled Zhat = (1/R) sum_r Zhat_r (log-sum-exp)
  out$log_Z_lower95 <- log(0.05) + out$log_Z                     # Markov bound 0.05 Zhat (one-sided)
  out$log_Z_rel_m0 <- out$log_Z - raw$log_m0                     # relative to m(empty)
  out$log_Z_r_rel_m0 <- logZr - raw$log_m0
  out$log_increment <- lapply(isl, function(r) r$log_increment)  # per island, per stage (reconstructs W_t, PW2)
  P <- do.call(cbind, lapply(isl, function(r) r$pip))
  orig <- setup$ctx$orig
  out$pip_r <- P; rownames(out$pip_r) <- orig
  out$pip_primary <- setNames(rowMeans(P), orig)                 # equal-weight mean over islands (M §6.11)
  out$mpm <- as.integer(orig[out$pip_primary > 0.5])
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
  ls <- out$local_search
  out$local_search <- ls
  out$local_limit <- isTRUE(ls$local_limit)
  # A certificate is about the selected HPM itself. An equal-F HPM tie change is not a local move.
  out$local_certified <- isTRUE(ls$local_certified) && identical(as.integer(out$hpm), as.integer(ls$returned))
  out$global_certified <- FALSE
  hb <- raw$hpm_before_local
  E1 <- any(led$island_best < out$hpm_F - 1)
  E2 <- R >= 2 && stats::sd(logZr) > 1
  E3 <- out$hpm_F > hb$F   # strict F increase of the global best in the final local search (ruling RC-1, M §6.9)
  if (v31) {
    # v3.1 #8: an LS0 improvement does not fire E3 (E3 = the final local search only, measured before LS0).
    # #10: local_certified attaches to the returned HPM, from whichever search ended on it (final search or LS0).
    # #6/#10: a completed LS0 capped at its move limit returns output; local_limit reports a cap of either search
    # (attribution in final_local_limit / ls0_local_limit); L1 = "n/a" for a capped LS0 (card not implemented).
    hl <- raw$hpm_before_ls0; l0 <- out$ls0
    E3 <- hl$F > hb$F
    cert_final <- out$local_certified
    cert_ls0 <- isTRUE(l0$local_certified) && identical(as.integer(out$hpm), as.integer(l0$returned))
    out$local_certified <- cert_final || cert_ls0
    out$local_certified_by <- if (cert_final && cert_ls0) "both" else if (cert_final) "final" else if (cert_ls0) "ls0" else "none"
    out$final_local_limit <- isTRUE(ls$local_limit); out$ls0_local_limit <- isTRUE(l0$local_limit)
    out$local_limit <- out$final_local_limit || out$ls0_local_limit
    out$ls0_improved <- out$hpm_F > hl$F                                          # LS0 raised the best score (strict)
    out$ls0_hpm_changed <- !identical(as.integer(out$hpm), as.integer(hl$model))  # includes equal-F tie-rule changes
  }
  lowESS <- any(out$stage_table$ess < 0.5 * ro$N)
  out$flags <- list(E1 = E1, E2 = E2, E3 = E3, low_empirical_ESS = lowESS, local_limit = out$local_limit,
                    near_tie_truncated = out$near_tie_truncated, checks_passed_final = !(E1 || E2 || E3 || lowESS),
                    escalated = (frozen[["tier"]] %||% 0) == 1, grid_unconverged = NA, forced_pilot_steps = NA,
                    checks_passed_calibration = NA)
  if (v31) out$flags <- c(out$flags, list(final_local_limit = out$final_local_limit, ls0_local_limit = out$ls0_local_limit,
                                          ls0_improved = out$ls0_improved, ls0_hpm_changed = out$ls0_hpm_changed))
  out$island_best <- led$island_best
  out$hpm_before_local <- hb
  out$leaders_gamma0 <- led$leaders_gamma0; out$leaders_gamma1 <- led$leaders_gamma1; out$top_store <- led$top
  out$score_counts <- list(logical = led$logical, fresh = led$fresh)   # mechanisms incl. gibbs_held / gibbs_flip (R15)
  out$cache <- raw$cache
  out$rb <- lapply(isl, function(r) list(rb_acc = r$rb_acc, rb_round = r$rb_round))
  out$timings <- list(islands = do.call(rbind, lapply(isl, function(r) r$seconds)), local = raw$seconds_local,
                      final_total = raw$seconds_total)
  if (v31) out$timings$ls0 <- raw$seconds_ls0
  out$log_m0 <- raw$log_m0; out$log_Zbar0 <- raw$log_Zbar0
  out$estimates_available <- TRUE
  out
}

# Fresh production final run. The runtime pointer shares the complete-fit clock with calibration.
v3_final_run <- function(setup, frozen, seed, runtime = NULL, ls0 = getOption("v3.ls0", TRUE)) {
  stopifnot(inherits(setup, "v3_setup"), inherits(frozen, "v3_frozen"))
  v3_check_grid(frozen[["grid"]]); v3_check_seed(seed)
  ro <- v3_run_settings(setup, frozen, ls0)
  raw <- .v3cpp$cpp_final_run(setup$ptr, frozen[["grid"]], ro, as.numeric(seed), frozen[["inherited"]], runtime)
  v3_assemble_final(raw, setup, frozen, ro, seed)
}
