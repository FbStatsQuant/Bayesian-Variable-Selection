# Source in the production worker after common.R and the test-only exports load.
# Required harness callbacks: add(label, expression), need(), exact().
# No production source or global .v3cpp binding is mutated by these units.

v2_runtime_fixture <- function(p = 2L, n = max(8L, 2L * p)) {
  X <- outer(seq_len(n), seq_len(p), function(i, j)
    sin(i * (j + 1) * .37) + cos(i * (j + 2) * .19) + ((i * j) %% 7) / 11)
  y <- sin(seq_len(n) * 1.23) + X[, 1L] * .3
  pre <- v3_preprocess(X, y)
  need(pre$status == "ok" && pre$p == p, "runtime fixture lost a predictor")
  ctx <- v3_context(pre$X, pre$y, orig = pre$kept)
  list(X = X, y = y, ctx = ctx, setup = v3_setup(ctx))
}

add("v2_cache_capacity_exactly_500p_run_and_calibration", local({
  # The R callback captures the actual calibration constructor options, then
  # invokes that constructor. Small tier budgets affect this test environment only.
  evidence <- list()
  for (p in c(2L, 30L, 66L)) {
    b <- v3_budgets(2L * p + 4L, p)
    s <- list(ctx = list(p = p), budgets = b)
    for (tier in 0:1) {
      r <- v3_run_settings(s, list(tier = tier))
      exact(r$cache_capacity, as.numeric(500 * p))
    }
  }
  d <- v2_runtime_fixture(); s <- d$setup
  e <- new.env(parent = globalenv())
  e$.v3cpp <- as.list(.v3cpp)
  seen <- NULL
  e$.v3cpp$cpp_cal_new <- function(setup, seed, ro, runtime) {
    seen <<- ro
    .v3cpp$cpp_cal_new(setup, seed, ro, runtime)
  }
  e$v3_cal_settings <- function(setup, tier)
    list(tier = tier, H = 3L, T_e = 64L, L = 1L, Hm = 4L, ell = 1L)
  e$v3_cal_tier <- v3_cal_tier; environment(e$v3_cal_tier) <- e
  f <- v3_calibrate; environment(f) <- e
  z <- f(s, 171L)
  need(z$status %in% c("ok", "schedule_limit"), "small calibration failed")
  exact(seen$cache_capacity, as.numeric(500 * s$ctx$p))
  exact(unname(z$cache[["capacity"]]), as.numeric(500 * s$ctx$p))
  r <- v3_run_settings(s, list(tier = 0L)); r$N <- 3L; r$L <- 1L; r$ell <- 1L
  final <- .v3cpp$cpp_final_run(s$ptr, c(0, 1), r, 172L, NULL, NULL)
  need(final$status == "completed", "small final failed")
  exact(unname(final$cache[["capacity"]]), as.numeric(500 * s$ctx$p))
  list(calibration_options = seen, calibration_cache = z$cache, final_cache = final$cache)
}))

add("v2_actual_score_timing_exact_size_including_stride_seven_reproducer", local({
  evidence <- list()
  for (pk in list(c(14L, 7L), c(14L, 14L), c(7L, 7L), c(21L, 3L), c(13L, 6L), c(14L, 0L))) {
    p <- pk[1]; k <- pk[2]; d <- v2_runtime_fixture(p); ctx <- d$ctx
    reps <- 200L
    before <- .v3cpp$cpp_numerical_routes(ctx)
    actual <- .v3cpp$cpp_time_scores(ctx, k, reps)
    after <- .v3cpp$cpp_numerical_routes(ctx)
    need(after$numerical_failures == before$numerical_failures, "timing swallowed a scorer failure")
    need(sum(unlist(after[c("chol", "chol_refactor", "qr")])) -
      sum(unlist(before[c("chol", "chol_refactor", "qr")])) == reps, "did not time exactly 200 successful scores")
    expected <- old_bug <- 0
    sizes <- integer(reps)
    for (r in 0:(reps - 1L)) {
      S <- sort(as.integer((r + seq_len(k) - 1L) %% p + 1L))
      sizes[r + 1L] <- length(S)
      need(length(S) == k && !anyDuplicated(S), "reference probe has wrong size")
      expected <- expected + .v3cpp$cpp_score(ctx, S)$log_m
      if (p == 14L && k == 7L) {
        old <- sort(unique(as.integer((r + (seq_len(k) - 1L) * 7L) %% p + 1L)))
        need(length(old) == 2L, "lost B's minimal bug reproducer")
        old_bug <- old_bug + .v3cpp$cpp_score(ctx, old)$log_m
      }
    }
    exact(unname(actual[["sink"]]), expected)
    if (p == 14L && k == 7L) need(actual[["sink"]] != old_bug, "timed old size-two models")
    evidence[[paste(p, k, sep = "_")]] <- list(probe = actual, expected_sink = expected,
      model_sizes = sizes, old_size_two_sink = if (p == 14L && k == 7L) old_bug else NULL)
  }
  evidence
}))

add("v2_exact_hpm_phase_and_mechanism", local({
  X <- matrix(c(-1, -1, 1, 1), ncol = 1L); y <- c(-1, 1, -1, 1)
  z <- v3_fit(X, y, 1L)
  need(z$status == "exact", "B-O5 fixture did not enumerate")
  exact(z$hpm_provenance, list(phase = "exact", mechanism = "enumeration"))
  z$hpm_provenance
}))

add("v2_inherited_rescore_failure_retains_hpm_and_is_contained", local({
  # Orthogonal predictors, with a strong joint signal in columns 2/3. Singleton
  # blocks deliberately keep the genuinely scored calibration best out of tables.
  X <- cbind(rep(c(-1, 1), 16L), rep(rep(c(-1, 1), each = 2L), 8L),
             rep(rep(c(-1, 1), each = 4L), 4L), rep(rep(c(-1, 1), each = 8L), 2L))
  y <- 5 * X[, 2L] + 4 * X[, 3L] + .1 * X[, 2L] * X[, 3L]
  pre <- v3_preprocess(X, y)
  ctx <- v3_context(pre$X, pre$y, orig = pre$kept)
  small <- .v3cpp$cpp_setup(ctx, 1L)
  need(small$status == "ok" && all(lengths(small$blocks) == 1L), "singleton setup failed")
  s <- list(ptr = small$ptr, ctx = ctx, B = 1L, budgets = v3_budgets(ctx$n, ctx$p))
  r <- v3_run_settings(s, list(tier = 0L)); r$N <- 3L; r$L <- 1L; r$ell <- 1L
  evidence <- list()
  for (after_hpm in c(FALSE, TRUE)) {
    injected <- .v3cpp$test_v2_final_rescore_failure(s$ptr, r, 173L, after_hpm)
    z <- injected$raw; saved <- injected$calibration_export$inherited$hpm
    exact(saved$model, c(2L, 3L))
    need(saved$F > injected$ledger_before$hpm$F && is.finite(injected$scored_best_log_m),
         "saved HPM is not a real scored non-table best")
    need(!any(vapply(small$blocks, function(b) all(saved$model %in% b), TRUE)), "best is a table model")
    # Every provenance field is exercised, rather than a phase-only surrogate.
    exact(saved$provenance, list(phase = "diag", mechanism = "gibbs_flip", tier = 1L,
      island = 2L, stage = 3L, round = 4L, particle = 5L, position = 6L, phi = .625, iter = 2L))
    need(is.finite(injected$control_log_m) && injected$scorer_failure_delta == 1,
         "injection did not reach a real scorer failure")
    exact(injected$successful_rescore_delta, injected$expected_successful_rescores)
    need(z$status == "numerical_failure" && grepl("after Cholesky, refactor and augmented QR", z$message, fixed = TRUE),
         "inherited rescore escaped the native failure handler")
    exact(z$ledger$hpm$model, saved$model); exact(z$ledger$hpm$F, saved$F)
    exact(z$ledger$hpm$provenance, saved$provenance)
    exact(z$ledger$logical, injected$ledger_before$logical)
    exact(z$ledger$fresh, injected$ledger_before$fresh)
    need(all(vapply(z$islands, is.null, TRUE)) && !length(z$local_search), "continued after failed inheritance")
    fr <- v3_frozen(c(0, 1), inherited = injected$calibration_export$inherited, budgets = s$budgets)
    a <- v3_assemble_final(z, s, fr, r, 173L)
    need(a$status == "numerical_failure" && a$hpm_incomplete && a$partial_results && !a$estimates_available,
         "ordinary assembly lost the contained failure")
    exact(a$hpm, saved$model); exact(a$hpm_F, saved$F); exact(a$hpm_provenance, saved$provenance)
    need(is.null(a$pip_primary) && is.null(a$log_Z), "failed inheritance exposed estimates")
    # RAII fault restoration: the formerly failing singleton scores normally again.
    need(is.finite(.v3cpp$cpp_score(ctx, injected$failure_model)$log_m), "test corruption was not restored")
    evidence[[if (after_hpm) "after_hpm" else "before_hpm"]] <- list(injection = injected, assembled = a)
  }
  evidence
}))

add("v2_V_rescore_failure_propagates_preliminary_and_rebuild_and_calibration", local({
  evidence <- list()
  # Run both paths: failure before the first grid, and after a completed grid
  # and real diagnostic iteration. All pilot/diagnostic calls are production C++.
  for (fail_call in 1:2) {
    d <- v2_runtime_fixture(); s <- d$setup
    e <- new.env(parent = globalenv()); e$.v3cpp <- as.list(.v3cpp)
    calls <- 0L; grid_calls <- 0L; injection <- NULL; diag_control <- NULL
    e$.v3cpp$cpp_cal_V <- function(state) {
      calls <<- calls + 1L
      if (calls == fail_call) {
        injection <<- .v3cpp$test_v2_V_rescore_failure(state)
        return(injection$result)
      }
      .v3cpp$cpp_cal_V(state)
    }
    e$.v3cpp$cpp_cal_diag <- function(...) {
      dg <- .v3cpp$cpp_cal_diag(...)
      need(dg$status == "ok", "real diagnostic failed before controlled check canary")
      diag_control <<- dg[c("island_best", "log_Z_r", "best_after_local")]
      # Controlled TRUE E1/E2, after real diagnostic islands/local search finish.
      # The following V still fails in the real scorer and production handler.
      dg$island_best <- rep(dg$best_after_local$F - 2, length(dg$island_best))
      dg$log_Z_r <- c(0, 4, 8, 12)
      dg
    }
    e$v3_build_grid <- function(...) { grid_calls <<- grid_calls + 1L; v3_build_grid(...) }
    e$v3_cal_settings <- function(setup, tier)
      list(tier = tier, H = 3L, T_e = 64L, L = 1L, Hm = 4L, ell = 1L)
    e$v3_cal_tier <- v3_cal_tier; environment(e$v3_cal_tier) <- e
    f <- v3_calibrate; environment(f) <- e
    z <- f(s, 174L)
    need(z$status == "numerical_failure" && calls == fail_call, "V failure escaped or calibration continued")
    need(injection$scorer_failure_delta == 1, "V injection did not exercise the real scorer")
    need(grid_calls == fail_call - 1L, "failed/partial V reached grid construction")
    tier <- tail(z$tiers, 1L)[[1L]]
    need(tier$partial_results && tier$partial_operation$status == "numerical_failure", "tier lost failure record")
    need(grepl("after Cholesky, refactor and augmented QR", tier$message, fixed = TRUE), "scorer message lost")
    need(!is.null(tier$pilot) && is.finite(z$hpm$F), "previous results/HPM lost")
    need(length(tier$grids) == fail_call - 1L && length(tier$snapshots) == fail_call - 1L &&
      length(tier$iterations) == fail_call - 1L, "discarded earlier successful calibration work")
    exact(z$flags$triggers_by_tier[[1L]], tier$triggers)
    if (fail_call == 2L) {
      last <- tail(tier$iterations, 1L)[[1L]]
      need(isTRUE(last$E1) && isTRUE(last$E2) && !is.null(diag_control), "TRUE E1/E2 canary did not run")
      exact(tier$triggers$E1, last$E1); exact(tier$triggers$E2, last$E2)
      need(all(c("E1", "E2") %in% z$flags$triggers_fired), "calibration dropped completed diagnostic triggers")
      exact(tier$triggers$E3, v3_E3_fires(tier$pilot) || last$E3)
      exact(tier$triggers$local_limit, isTRUE(tier$pilot$local_search$local_limit) || isTRUE(last$local_search$local_limit))
    } else {
      exact(tier$triggers$E1, FALSE); exact(tier$triggers$E2, FALSE)
      need(is.null(diag_control), "diagnostic ran after preliminary failure")
    }
    need(is.null(z$frozen), "failed calibration produced a frozen grid")
    need(is.finite(.v3cpp$cpp_score(d$ctx, 1L)$log_m), "V fault was not restored")
    evidence[[as.character(fail_call)]] <- list(calibration = z, injection = injection, grid_calls = grid_calls,
      original_diagnostic_checks = diag_control)
  }
  evidence
}))

add("v2_rebuild_resource_stop_retains_last_completed_diagnostic_checks", local({
  d <- v2_runtime_fixture(); s <- d$setup
  e <- new.env(parent = globalenv()); e$.v3cpp <- as.list(.v3cpp)
  checks <- list(); diag_control <- NULL
  e$.v3cpp$cpp_cal_diag <- function(...) {
    dg <- .v3cpp$cpp_cal_diag(...)
    need(dg$status == "ok", "real diagnostic failed before resource-stop canary")
    diag_control <<- dg[c("island_best", "log_Z_r", "best_after_local")]
    dg$island_best <- rep(dg$best_after_local$F - 2, length(dg$island_best))
    dg$log_Z_r <- c(0, 4, 8, 12)
    dg
  }
  e$.v3cpp$cpp_runtime_check <- function(runtime, operation_seconds, checkpoint, tier, iter) {
    native <- .v3cpp$cpp_runtime_check(runtime, operation_seconds, checkpoint, tier, iter)
    need(!isTRUE(native), "generous real runtime budget unexpectedly expired")
    checks[[length(checks) + 1L]] <<- list(checkpoint = checkpoint, tier = tier, iter = iter, native = native)
    # Only this cloned R callback requests a stop, after a successful rebuild.
    identical(checkpoint, "grid_construction") && iter == 1L
  }
  e$v3_cal_settings <- function(setup, tier)
    list(tier = tier, H = 3L, T_e = 64L, L = 1L, Hm = 4L, ell = 1L)
  e$v3_cal_tier <- v3_cal_tier; environment(e$v3_cal_tier) <- e
  f <- v3_calibrate; environment(f) <- e
  runtime <- .v3cpp$cpp_runtime_new(1e6, 0)
  z <- f(s, 175L, runtime = runtime)
  need(z$status == "resource_limit" && length(z$tiers) == 1L && is.null(z$frozen),
       "resource stop escaped the ordinary calibration handler")
  tier <- z$tiers[[1L]]
  need(tier$partial_results && tier$partial_operation$status == "resource_limit" &&
    isTRUE(tier$partial_operation$resource_limit), "resource failure record lost")
  need(length(checks) == 2L && length(tier$grids) == 2L && length(tier$snapshots) == 2L &&
    length(tier$iterations) == 1L, "resource stop discarded completed calibration work")
  last <- tier$iterations[[1L]]
  need(isTRUE(last$E1) && isTRUE(last$E2) && !is.null(diag_control), "TRUE E1/E2 resource canary did not run")
  exact(tier$triggers$E1, last$E1); exact(tier$triggers$E2, last$E2)
  exact(z$flags$triggers_by_tier[[1L]], tier$triggers)
  need(all(c("E1", "E2") %in% z$flags$triggers_fired), "resource stop dropped completed diagnostic triggers")
  exact(tier$triggers$E3, v3_E3_fires(tier$pilot) || last$E3)
  exact(tier$triggers$local_limit, isTRUE(tier$pilot$local_search$local_limit) || isTRUE(last$local_search$local_limit))
  list(calibration = z, runtime_checks = checks, original_diagnostic_checks = diag_control)
}))
