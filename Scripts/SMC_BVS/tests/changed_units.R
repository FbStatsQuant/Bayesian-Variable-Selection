# Loaded in the production worker only, after raw regression outputs are saved.
add("production_api_has_no_test_controls", {
  exact(names(formals(v3_fit)), c("X", "y", "seed", "allocation"))
  forbidden <- c("v3_trace", "v3_step_sample", "v3_round_sample", "v3_resample_sample",
    "v3_replicate_final", "v3_observer_prepare", "v3_observer_report", "v3_pilot_schedule", "v3_reference")
  need(!any(vapply(forbidden, exists, TRUE, envir = globalenv(), inherits = FALSE)), "excluded R profiling interface remains")
  exports <- ls(.v3cpp)
  need(!any(grepl("^cpp_(trace|observer|replicate|step_sample|round_sample|resample_sample|reference)", exports)), "excluded C++ profiling export remains")
  need(!("hooks" %in% names(formals(v3_context))), "production scorer hook remains")
  need(!("B_override" %in% names(formals(v3_setup))), "production B override remains")
  TRUE
})
add("secondary_pip_removed_without_primary_change", {
  need(!("pip_secondary" %in% names(final)), "secondary PIP remains in final")
  exact(final$pip_primary, setNames(rowMeans(final$pip_r), ctx$orig))
  exact(final$mpm, as.integer(ctx$orig[final$pip_primary > .5]))
  TRUE
})
add("r2_randomness_and_full_stage_metadata", {
  need(is.data.frame(final$stream_map), "complete stream map missing")
  exact(final$stream_map$stream, 0:13)
  exact(final$stream_map$phase, c("pilot", rep("diag",4), "pilot", rep("diag",4), rep("final",4)))
  need(all(final$stream_map$tier[11:14] == ro$tier), "final stream tier missing")
  for (s in c("0x9E3779B97F4A7C15", "0xBF58476D1CE4E5B9", "0x94D049BB133111EB", "xoshiro256**"))
    need(grepl(s, final$seeding_doc, fixed=TRUE), paste("seed convention missing", s))
  for (s in c("pi0_size", "pi0_block_size", "pi0_submodel", "uswap_accept", "nswap_accept", "indep_accept", "Fisher-Yates"))
    need(grepl(s, final$variate_order_doc, fixed=TRUE), paste("draw convention missing", s))
  required <- c("phase","tier","iter","island","stage","rho_V","partial","gibbs","gibbs_state_changes",
                "uswap_acc","uswap_exec","nswap_acc","nswap_exec","indep_acc","indep_exec")
  need(all(required %in% names(final$stage_table)), "complete labelled stage diagnostics missing")
  need(all(final$stage_table$phase == "final_bridge") && all(final$stage_table$tier == 0) &&
       all(final$stage_table$iter == -1) && !any(final$stage_table$partial), "incorrect final stage labels")
  need(all(is.na(final$stage_table$rho_V)), "supplied test grid has invented restricted rho")
  if (calibration_full$status == "ok") {
    tab <- calibration_full$stage_table
    need(nrow(tab) > 0 && all(required %in% names(tab)), "consolidated calibration stage table missing")
    for (tier in calibration_full$tiers) {
      pt <- tab[tab$phase == "pilot" & tab$tier == tier$tier, , drop=FALSE]
      need(nrow(pt) == length(tier$pilot$schedule)-1L && all(is.na(pt$rho_V)), "pilot stage labels/rho incorrect")
      for (it in tier$iterations) for (r in 1:4) {
        rows <- tab[tab$phase == "diag" & tab$tier == tier$tier & tab$iter == it$iteration & tab$island == r, , drop=FALSE]
        exact(rows$rho_V, it$rho_V)
        need(all(rows$grid_label == it$grid_label), "restricted rho uses wrong grid label")
      }
    }
    last <- tail(calibration_full$tiers,1)[[1]]
    exact(calibration_full$frozen$rho_V, last$rho_V)
    exact(calibration_full$frozen$grid_label, last$grid_label)
    recomputed <- v3_frozen(calibration_full$frozen$grid, calibration_full$frozen$tier,
      calibration_full$frozen$N, calibration_full$frozen$L, calibration_full$frozen$inherited)
    exact(recomputed$sha256, calibration_full$frozen$sha256)
  }
  TRUE
})
add("local_certified_exact_tie_change_false", {
  # Fabricated raw assembly fixture represents the real exact-tie local-search
  # situation: search centre was scanned, lex-smaller equal-F HPM was not.
  r <- raw
  r$ledger$hpm$model <- as.integer(ctx$orig[1])
  r$local_search$returned <- as.integer(ctx$orig[2])
  r$local_search$returned_F <- r$ledger$hpm$F
  r$local_search$local_certified <- TRUE
  r$hpm_before_local$F <- r$ledger$hpm$F
  z <- assemble(r)
  need(!z$local_certified, "tie changed selected model but certificate remained true")
  need(!z$flags$E3, "equal-F tie incorrectly fires E3")
  r$local_search$returned <- r$ledger$hpm$model
  need(assemble(r)$local_certified, "same scanned centre lost certificate")
  r$local_search$local_certified <- FALSE
  need(!assemble(r)$local_certified, "uncertified scan upgraded to certificate")
  list(changed_hpm = z$hpm, scanned_centre = z$local_search$returned, certified = z$local_certified)
})
add("real_local_search_exact_tie_changes_hpm_without_move", {
  i <- seq_len(32); x <- sin(2*pi*i/32)
  X <- cbind(x, x, sin(4*pi*i/32), cos(4*pi*i/32), sin(6*pi*i/32), cos(6*pi*i/32))
  p <- v3_preprocess(X, x)
  orig <- c(2L, 5L, 9L, 12L, 17L, 22L)
  c <- v3_context(p$X, p$y, orig = orig); s <- v3_setup(c)
  z <- .v3cpp$test_local(s$ptr, 5L, 3L)
  need(z$archive$termination == "no_improvement" && z$archive$moves == 0L, "duplicate exact tie became strict local move")
  exact(z$archive$returned, 5L); exact(z$hpm, 2L)
  exact(v3_score(c, 2L)$F, v3_score(c, 5L)$F)
  # Feed that actual archive/tie outcome through production assembly.
  r <- raw; r$local_search <- z$archive; r$ledger$hpm$model <- z$hpm
  r$ledger$hpm$F <- r$hpm_before_local$F <- z$F
  a <- assemble(r)
  need(!a$local_certified && !a$flags$E3, "actual tied HPM has erroneous certificate/E3")
  z
})
add("near_tie_inclusive_and_truncation", {
  r <- raw; best <- r$ledger$hpm$F
  r$ledger$top$value <- c(best, best - 1e-9)
  r$ledger$top$models <- list(as.integer(ctx$orig[1]), as.integer(ctx$orig[2]))
  r$ledger$top$full <- TRUE
  z <- assemble(r)
  need(length(z$near_ties) == 2L && z$near_tie_truncated, "inclusive full-store near tie failed")
  r$ledger$top$value[2] <- .v3cpp$test_adjacent(best - 1e-9, FALSE)
  need(!assemble(r)$near_tie_truncated, "outside threshold wrongly truncated")
  r$ledger$top$full <- FALSE
  need(!assemble(r)$near_tie_truncated, "non-full store wrongly truncated")
  TRUE
})
add("cut_group_exact_threshold_original_map", {
  n <- 200L; p <- 4L; rho <- sqrt(2 * log(p) / n)
  M <- diag(p); M[1, 2] <- M[2, 1] <- rho
  orig <- c(2L, 5L, 9L, 12L); block <- 0:3
  z <- .v3cpp$test_cut(M, orig, block, n)
  need(z$cut_group && z$count == 1L, "cut-group used strict > at threshold")
  exact(z$components[[1]]$members, c(2L, 5L))
  need(z$components[[1]]$size == 2L && z$components[[1]]$block_span == 2L, "bad component dimensions")
  M[1, 2] <- M[2, 1] <- .v3cpp$test_adjacent(rho, FALSE)
  need(!.v3cpp$test_cut(M, orig, block, n)$cut_group, "below-threshold edge or forced best partner used")
  M[1, 2] <- M[2, 1] <- -rho
  need(.v3cpp$test_cut(M, orig, block, n)$cut_group, "sign-duplicate correlation ignored")
  z
})
add("cut_group_uncapped_multiple_components_and_small_split", {
  p <- 10L; n <- 200L; rho <- sqrt(2 * log(p)/n)
  M <- diag(p)
  # Two dense components joined by one weak >=threshold bridge. Any per-node
  # B cap drops that bridge when B<=3; uncapped connectivity must retain it.
  M[1:4, 1:4] <- .9; M[5:8, 5:8] <- .9; diag(M) <- 1
  M[4, 5] <- M[5, 4] <- rho
  M[9, 10] <- M[10, 9] <- rho
  orig <- as.integer(seq(2, 20, 2)); block <- as.integer(c(0,0,1,1,2,2,3,3,4,5))
  z <- .v3cpp$test_cut(M, orig, block, n)
  need(z$count == 2L, "uncapped bridge lost or components merged incorrectly")
  exact(z$components[[1]]$members, orig[1:8])
  exact(z$components[[2]]$members, orig[9:10])
  need(z$components[[1]]$size == 8L && z$components[[1]]$block_span == 4L, "large split component omitted")
  need(z$components[[2]]$size == 2L && z$components[[2]]$block_span == 2L, "split component <=B omitted")
  block[10] <- block[9]
  need(.v3cpp$test_cut(M, orig, block, n)$count == 1L, "whole component incorrectly flagged")
  z
})
add("memory_formula_all_terms_tiers_and_strict_limit", {
  evidence <- list()
  for (np in list(c(9, 7), c(200, 500), c(200, 1000), c(256, 65))) for (tier in 0:1) {
    n <- np[1]; p <- np[2]; b <- v3_budgets(n, p); K <- b$K; B <- b$B
    N <- b$N0 * 4^tier; C <- 500 * p; W <- ceiling(p / 64)
    expected <- 8 * (3*n*p + 3*p*p) + 16*ceiling(p/B)*2^B +
      8*ceiling(p/B)*(K+1)*(B+1) + 29*2^ceiling(log2(2*C)) + 4*C*K +
      (80*p+1)*(4*K+64) + 2*N*(8*W+4*K+96)
    bad_time <- function(k) stop("SMC memory preflight called score timer")
    z <- v3_preflight(n, p, b, "smc", list(mem_gb = 1e6, hours = 1e-100), tier, bad_time)
    exact(z$est_bytes, expected)
    need(!z$exceeds && is.na(z$est_seconds), "SMC uses removed wall-time projection")
    exact(z$est_bytes, sum(z$memory_components))
    at <- v3_preflight(n, p, b, "smc", list(mem_gb = expected/2^30), tier, bad_time)
    need(!at$exceeds, "memory equality incorrectly stops")
    below <- .v3cpp$test_adjacent(expected/2^30, FALSE)
    need(v3_preflight(n, p, b, "smc", list(mem_gb = below), tier, bad_time)$exceeds, "strict memory overage not stopped")
    evidence[[paste(n, p, tier, sep = "_")]] <- z
  }
  n <- 20; p <- 7; b <- v3_budgets(n, p); seen <- NULL
  z <- v3_preflight(n, p, b, "exact", list(), time_fun = function(k) { seen <<- k; 2 })
  k <- min(b$K, ceiling(p/2))
  exact(z$est_bytes, 8*(3*n*p+p*p)+8*(40*p+1)*(k+8)+32*p)
  need(seen == k && z$est_seconds == b$exact_count*2, "exact projection/timing size differs")
  need(z$allocation$mem_gb == 8 && z$allocation$hours == 24, "allocation defaults differ")
  at <- v3_preflight(n, p, b, "exact", list(hours = z$est_seconds/3600), time_fun = function(k) 2)
  need(!at$exceeds, "exact time equality incorrectly stops")
  need(v3_preflight(n,p,b,"exact",list(hours = z$est_seconds/7200),time_fun=function(k) 2)$exceeds,
       "exact time overage not stopped")
  evidence$exact <- z; evidence
})
add("exact_score_timing_recipe_200_first_columns", {
  e <- new.env(parent = globalenv()); calls <- list()
  e$v3_context <- function(Xs, ys, return_gram) {
    calls$X <<- Xs; calls$return_gram <<- return_gram
    list(K = min(ncol(Xs), nrow(Xs) %/% 2))
  }
  e$.v3cpp <- list(cpp_time_scores = function(ctx, k, count) {
    calls$k <<- k; calls$count <<- count; list(seconds_per_score = .125)
  })
  f <- v3_time_scores; environment(f) <- e
  X <- matrix(seq_len(300L*90L), 300L, 90L)
  for (k in c(3, 80)) {
    need(f(X, seq_len(300), k) == .125, "timing result changed")
    exact(calls$X, X[, seq_len(min(90, max(64, k))), drop = FALSE])
    need(!calls$return_gram && calls$count == 200 && calls$k == k, "wrong timing recipe")
  }
  TRUE
})
add("runtime_guard_strict_comparison", {
  z <- .v3cpp$test_guard_boundary()
  need(!z$equality_stops && z$strict_stops && !z$safe_stops, "runtime guard does not use strict >")
  z
})
add("runtime_guard_final_all_stage_and_local_checkpoints", {
  rt <- .v3cpp$cpp_runtime_new(1e6, 0)
  z <- .v3cpp$cpp_final_run(setup$ptr, grid, ro, seed, NULL, rt)
  report <- .v3cpp$cpp_runtime_report(rt); cp <- report$checkpoints
  stages <- Filter(function(c) c$checkpoint == "bridge_stage", cp)
  local <- Filter(function(c) c$checkpoint == "local_search", cp)
  need(z$status == "completed" && length(stages) == 4L*(length(grid)-1L) && length(local) == 1L,
       "missing final bridge/local checkpoint")
  for (r in 1:4) need(identical(vapply(Filter(function(c) c$island == r, stages), `[[`, 0L, "stage"), 1:4),
                     "wrong per-island checkpoint stages")
  for (c in cp) need(c$operation_seconds >= 0 && c$projected_seconds == c$elapsed_seconds + c$operation_seconds,
                   "guard does not record elapsed+completed-operation duration")
  report
})
add("runtime_guard_stops_and_retains_first_stage", {
  rt <- .v3cpp$cpp_runtime_new(1, 1e6)
  z <- .v3cpp$cpp_final_run(setup$ptr, grid, ro, seed, NULL, rt)
  need(z$status == "resource_limit", "runtime guard failed to stop")
  report <- .v3cpp$cpp_runtime_report(rt)
  need(length(report$checkpoints) == 1L && report$checkpoints[[1]]$stage == 1L, "continued after guard stop")
  need(length(z$islands[[1]]$phi) == 1L && z$islands[[1]]$partial, "completed stage not retained as partial")
  need(length(z$ledger$hpm$model) >= 0 && is.finite(z$ledger$hpm$F), "best scored HPM lost")
  a <- assemble(z)
  need(!a$estimates_available && a$partial_results && !is.null(a$partial_final), "partial output falsely reported final")
  list(raw = z, guard = report)
})
add("runtime_guard_pilot_diagnostic_and_grid_checkpoints", {
  # Clone only the R orchestration environment to select small internal budgets.
  # It invokes unmodified production C++ pilot/diagnostic/guard implementations.
  e <- new.env(parent = globalenv())
  e$v3_cal_settings <- function(setup, tier)
    list(tier = tier, H = 7L, T_e = 64L, L = 1L, Hm = 4L, ell = 2L)
  f <- v3_cal_tier; environment(f) <- e
  rt <- .v3cpp$cpp_runtime_new(1e6, 0)
  state <- .v3cpp$cpp_cal_new(setup$ptr, seed, ro, rt)
  z <- f(state, setup, 0L, rt); need(z$status == "ok", "tiny calibration tier failed")
  report <- .v3cpp$cpp_runtime_report(rt); cp <- report$checkpoints
  count <- function(name) sum(vapply(cp, function(c) c$checkpoint == name, TRUE))
  need(count("grid_construction") == length(z$grids), "missing whole-grid checkpoint")
  need(count("local_search") == 1L + length(z$iterations), "wrong calibration local-search scope/checkpoints")
  stages <- Filter(function(c) c$checkpoint == "bridge_stage", cp)
  expected <- length(z$pilot$schedule)-1L + sum(vapply(z$iterations, function(it) 4L*(length(it$grid)-1L), 0L))
  need(length(stages) == expected, "missing pilot/diagnostic per-island bridge checkpoint")
  need(any(vapply(stages, function(c) c$phase == "pilot", TRUE)) &&
       any(vapply(stages, function(c) c$phase == "diag", TRUE)), "missing calibration checkpoint phase")
  list(calibration = z, guard = report)
})
add("exact_branch_cut_group_NA_primary_only", {
  d <- fixture(1L); X <- d$X[, 1:6, drop = FALSE]
  z <- v3_fit(X, d$y, seed, allocation = list(mem_gb = 8, hours = 24))
  need(z$status == "exact" && z$branch_run == "exact", "mandatory exact branch bypassed")
  need(is.na(z$cut_group) && length(z$cut_group) == 1L, "exact cut_group is not NA")
  need(!("pip_secondary" %in% names(z)), "exact branch secondary PIP remains")
  need(z$local_certified, "completed enumeration not locally certified")
  z
})
add("runtime_guard_grid_stop_preserves_grid_and_prior_results", {
  e <- new.env(parent = globalenv())
  e$v3_cal_settings <- function(setup, tier)
    list(tier = tier, H = 7L, T_e = 64L, L = 1L, Hm = 4L, ell = 2L)
  rt <- .v3cpp$cpp_runtime_new(1, 0)
  # Expire the testing copy's clock immediately after actual grid construction.
  # The ordinary R checkpoint then calls the actual production RuntimeGuard.
  e$v3_build_grid <- function(logg0_V, d_V, pilot_temps, T_e) {
    g <- v3_build_grid(logg0_V, d_V, pilot_temps, T_e)
    .v3cpp$test_runtime_elapsed(rt, 1e6)
    g
  }
  f <- v3_cal_tier; environment(f) <- e
  state <- .v3cpp$cpp_cal_new(setup$ptr, seed, ro, rt)
  z <- f(state, setup, 0L, rt)
  need(z$status == "resource_limit" && z$partial_results, "grid checkpoint failed to stop")
  need(length(z$grids) == 1L && length(z$snapshots) == 1L && !is.null(z$pilot), "grid stop discarded earlier output")
  cp <- .v3cpp$cpp_runtime_report(rt)$checkpoints
  need(tail(cp, 1)[[1]]$checkpoint == "grid_construction" && tail(cp, 1)[[1]]$exceeded,
       "wrong stopping checkpoint")
  z
})

current_unit_source <- "metadata_units.R"
source(file.path(testdir, current_unit_source), local = globalenv())
current_unit_source <- "changed_units.R"
