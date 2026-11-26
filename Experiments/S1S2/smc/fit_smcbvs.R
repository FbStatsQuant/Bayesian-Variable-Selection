# fit_smcbvs.R -- SMC-BVS adapter for the S1/S2 harness.  fit_smcbvs(X, y, method_seed, ctrl = list()) -> INTERFACE list.
# PROVENANCE
#   Method: SMC-BVS v3.1.1, the owner-frozen method (Docs/Experiments/P1M/DECISIONS.md H-17: "frozen method = tag
#     method-v3.1.1-listpip (main 7100bb3b; core tree 61b0a582)"). Engine arm "T, the theorem-covered method" of
#     EXPERIMENT_PLAN.md §2.0.7 (law N = max(2500, n, p), R' = 4 islands, coded calibration with escalation, LS0 on).
#   Software: R core Scripts/SMC_BVS/core @ tag method-v3.1.1-listpip = commit 15a6d841c57fa9b66bfa46223336ebbec61f8049,
#     core tree 61b0a5822019b2737fe415ff15625e410f3227b2, exported by `git archive` (not edited) to
#     ROOT/ext/smcbvs_core@7100bb3b/ ; compiled with its own pinned Makevars.v3 (-O2 -ffp-contract=off -march=x86-64-v2).
#     Entry point: v3_fit(X, y, seed, allocation) (core README). ls0 = TRUE (v3.1 default). No option is overridden.
#   Settings: every statistical setting (prior, N, R', schedule, calibration, kernels, LS0) is the method's own and is
#     fixed inside v3_fit; the adapter passes only data, seed and allocation.
#   OURS:
#     - allocation = list(mem_gb = 8, hours = 1e6): the allocation is an operational guard ("lead ruling 2026-10-22:
#       operational guard, not a statistical setting", v3_preflight label). With the default 24 h, the v3.1 preflight's
#       LS0 worst-case charge (ell_n + K + 1 complete scans, K = min(p, n/2)) refuses S1 at n = 500 (84 h projected on Owls)
#       before any computation. hours = 1e6 makes admission pass; the harness enforces its own wall limit instead.
#     - Selection = MPM, PIP > 0.5 on pip_primary (fit$mpm). INTERFACE.md rule for Bayesian methods.
#     - "top models with weights": the returned top store (models with F(S) = log prior + log marginal), weights
#       renormalised over the store, u_S = exp(F(S) - max F) / sum (SPEC_LIST_PIP; a list view, not the SMC estimate).
#     - seed = method_seed (INTERFACE.md); v3_fit accepts integers in [1, 2^31 - 1].
#   Preprocessing (HQ ruling (b), 2026-11-25: Bayesian methods get X <- scale(X), y <- scale(y, scale = FALSE), as in
#     The-PARNI-scheme@3b95d669 R/simulation/dataset_generation.R:28-29): v3_fit ALWAYS standardises X columns and y itself
#     (v3_preprocess.R, v3_standardise, M §4.4: /max|x|, centre, /sample SD). Feeding it scale(X), centred y instead of raw
#     data changes its working input by <= 1.8e-15 (specs/generator_check.md), so the adapter passes raw X, y unchanged.

`%||%` <- function(a, b) if (is.null(a)) b else a
SMCBVS_CORE_DIR <- Sys.getenv("SMCBVS_CORE_DIR",
                              "/home/fb31/Bayesian-Variable-Selection/_local/engineering/ext/smcbvs_core@7100bb3b")
SMCBVS_ENGINE_TAG <- "method-v3.1.1-listpip (commit 15a6d841, core tree 61b0a582; R core v3.1.1, ls0 = TRUE)"

smcbvs_top_models <- function(top, k = 50) {
  if (is.null(top) || !length(top$value)) return(NULL)
  F <- as.numeric(top$value); o <- order(-F)[seq_len(min(k, length(F)))]
  u <- exp(F - max(F)); w <- u / sum(u)
  data.frame(rank = seq_along(o), F = F[o], weight_list = w[o], size = vapply(top$models[o], length, 1L),
             model = vapply(top$models[o], function(m) paste(sort(as.integer(m)), collapse = ","), ""),
             stringsAsFactors = FALSE)
}

# E-flags (manager brief 2026-11-25, batch-1 STOP rule): the engine's own final checks E1 (an island best more than 1
# below the global HPM), E2 (sd of the island log Z > 1), E3 (the final local search raised the global best) and
# low_empirical_ESS (some stage ESS < N/2); checks_passed_final = none of them (v3_run.R:182-204). A v3 status other than
# "completed" is an E-flag too ("status:<value>"). Warnings (recorded, not E-flags): local-search move caps, a truncated
# near-tie list, an unconverged grid, tier escalation, calibration triggers.
smcbvs_eflags <- function(fit) {
  f <- fit$flags %||% list()
  tr <- function(nm) nm[vapply(nm, function(k) isTRUE(f[[k]]), TRUE)]
  e <- tr(c("E1", "E2", "E3", "low_empirical_ESS"))
  if (!identical(fit$status, "completed")) e <- c(e, paste0("status:", fit$status %||% "NA"))
  w <- c(tr(c("local_limit", "final_local_limit", "ls0_local_limit", "near_tie_truncated", "grid_unconverged", "escalated")),
         if (length(f$calibration_triggers)) paste0("calibration_trigger:", f$calibration_triggers))
  list(eflags = as.character(e), eflag_any = length(e) > 0, warnings = as.character(w))
}

# list-renormalised mass by model size over the whole top store (cheap: one number per size)
smcbvs_size_mass <- function(top) {
  if (is.null(top) || !length(top$value)) return(NULL)
  F <- as.numeric(top$value); u <- exp(F - max(F)); w <- u / sum(u)
  sz <- vapply(top$models, length, 1L)
  m <- tapply(w, sz, sum)
  data.frame(size = as.integer(names(m)), mass = as.numeric(m))
}

# Post-fit hook, called by harness/run_one.R AFTER the fit with the true support S0 (the fit itself never sees S0).
# Scores S0, the selected MPM and the engine's HPM with the engine's own scorer v3_score (v3_setup.R:16 -> cpp_score,
# F = log prior + log marginal, the quantity the sampler targets) on the engine's own preprocessed data
# (v3_preprocess(X, y, dup_components = FALSE), as v3_fit does), so no scorer is re-implemented here.
diag_smcbvs <- function(X, y, fit, S0) {
  e <- fit$extra
  if (!identical(e$status, "ok")) return(list(json = list(scorer = "not run: fit failed")))
  pre <- get("v3_preprocess", envir = globalenv())(X, y, dup_components = FALSE)
  ctx <- get("v3_context", envir = globalenv())(pre$X, pre$y, orig = pre$kept, return_gram = FALSE)
  K <- min(length(pre$kept), floor(nrow(X) / 2))
  sc <- function(S) {
    S <- sort(as.integer(S))
    if (length(S) > K) return(list(F = NA_real_, Q = NA_real_, note = "|S| > K: infeasible under the engine prior"))
    if (!all(S %in% pre$kept)) return(list(F = NA_real_, Q = NA_real_, note = "S contains a column dropped by preprocessing"))
    r <- get("v3_score", envir = globalenv())(ctx, S)
    list(F = r$F, Q = r$Q, log_m = r$log_m, log_prior = r$log_prior)
  }
  s0 <- sc(S0); ssel <- sc(fit$selected); shpm <- sc(e$hpm)
  n <- nrow(X); a0 <- 0.01; b0 <- 0.01                 # IG(a0, b0) on sigma^2 (v3_score.h Data defaults; SPEC §9)
  yscale2 <- sum((y - mean(y))^2) / sum(pre$y^2)        # engine works on standardised y; back to the scale of y
  sig2 <- (b0 + ssel$Q / 2) / (a0 + n / 2 - 1) * yscale2
  top <- e$.top_store
  models <- if (!is.null(top) && length(top$value)) {
    F <- as.numeric(top$value); u <- exp(F - max(F))
    data.frame(model = vapply(top$models, model_key, ""), logpost = F, weight = u / sum(u),
               size = vapply(top$models, length, 1L), stringsAsFactors = FALSE)
  } else NULL
  post <- diag_posterior(fit$pip, S0, models, logpost_S0 = s0$F,
                         models_source = paste0("engine top store (", length(top$value), " models, the best visited by F), ",
                                                "weights exp(F - max F) renormalised over the store (list view, not the SMC estimate)"))
  list(json = list(logpost_S0 = s0$F, logpost_selected = ssel$F, logpost_hpm = shpm$F,
                   hpm_F_check = shpm$F - e$hpm_F,              # 0 up to rounding: the scorer reproduces the fit's own F
                   S0_note = s0$note %||% NA_character_,
                   sigma_hat = list(value = sqrt(sig2), which = paste("sqrt of E[sigma^2 | y, MPM] under the engine prior,",
                     "(b0 + Q/2) / (a0 + n/2 - 1) on standardised y, times var(y) / var(standardised y)"))),
       posterior = post, scorer = "v3_score (engine scorer, F = log prior + log marginal)")
}

# Progress lines (HQ ruling (b), 2026-11-26; OURS, operational only). The engine prints nothing while it runs, and a fit
# killed by the harness wall timeout leaves no rds, so its progress is otherwise lost. This wraps the four R closures in
# the engine's compiled-call environment .v3cpp that each run one whole SMC pass (calibration pilot, V/grid build,
# diagnostic islands, final run) and writes one line per call to stderr (Slurm .err):
#   PROGRESS <utc> fit_t=<s since v3_fit start> <call> tier=<k> iter=<i> secs=<call s> stages=<per island>
# Arguments and return values pass through unchanged; no random numbers are drawn; engine files are not edited.
# Time per stage is not measured by the engine; secs / stages is the per-stage average of one pass.
smcbvs_progress_hooks <- function() {
  e <- get(".v3cpp", envir = globalenv())
  if (isTRUE(attr(e$cpp_final_run, "smcbvs_progress"))) return(invisible(FALSE))
  t_fit0 <- proc.time()[["elapsed"]]
  assign(".smcbvs_progress_t0", t_fit0, envir = globalenv())
  nst <- function(x) tryCatch(paste(vapply(x, function(i) length(i$ess), 1L), collapse = ","), error = function(err) "NA")
  wrap <- function(nm, tier_at, iter_at, stages) {
    f <- get(nm, envir = e)
    g <- function(...) {
      a <- list(...); t <- proc.time()[["elapsed"]]
      tier <- if (!is.na(tier_at) && length(a) >= tier_at) a[[tier_at]] else NA
      it <- if (!is.na(iter_at) && length(a) >= iter_at) a[[iter_at]] else NA
      now <- function() format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC")
      t0 <- get(".smcbvs_progress_t0", envir = globalenv())
      message(sprintf("PROGRESS %s fit_t=%.0f %s start tier=%s iter=%s", now(), t - t0, nm, tier, it))
      r <- f(...)
      message(sprintf("PROGRESS %s fit_t=%.0f %s end tier=%s iter=%s secs=%.1f status=%s stages=%s", now(),
                      proc.time()[["elapsed"]] - t0, nm, tier, it, proc.time()[["elapsed"]] - t,
                      tryCatch(as.character(r$status %||% "NA"), error = function(err) "NA"), stages(r)))
      r
    }
    attr(g, "smcbvs_progress") <- TRUE
    assign(nm, g, envir = e)
  }
  wrap("cpp_cal_pilot", 2L, NA, function(r) nst(list(r$island)))
  wrap("cpp_cal_V", NA, NA, function(r) "-")
  wrap("cpp_cal_diag", 2L, 8L, function(r) nst(r$islands))
  wrap("cpp_final_run", NA, NA, function(r) tryCatch(nst(r$islands), error = function(err) "NA"))
  invisible(TRUE)
}

fit_smcbvs <- function(X, y, method_seed, ctrl = list()) {
  out <- NULL
  res <- tryCatch(fit_smcbvs_inner(X, y, method_seed, ctrl, function(f) out <<- f), error = function(e) e)
  if (!inherits(res, "error")) return(res)
  # post-processing failed after v3_fit returned: keep the raw fit so nothing is lost; the harness records a failure
  list(selected = integer(0), pip = NULL, runtime_sec = NA_real_, software = list(name = "SMC-BVS R core", version = "v3.1.1"),
       settings = list(), extra = list(status = paste0("failed: adapter post-processing: ", conditionMessage(res)), raw_fit = out,
                                       json_summary = list(engine_tag = SMCBVS_ENGINE_TAG)))
}

fit_smcbvs_inner <- function(X, y, method_seed, ctrl = list(), keep = function(f) NULL) {
  p <- ncol(X)
  sw <- list(name = "SMC-BVS R core", version = "v3.1.1", commit = "15a6d841c57fa9b66bfa46223336ebbec61f8049",
             tag = "method-v3.1.1-listpip", core_tree = "61b0a5822019b2737fe415ff15625e410f3227b2", core_dir = SMCBVS_CORE_DIR)
  alloc <- ctrl$allocation %||% list(mem_gb = 8, hours = 1e6)
  settings <- list(allocation_mem_gb = list(value = alloc$mem_gb, source = "OURS (operational guard)"),
                   allocation_hours = list(value = alloc$hours, source = "OURS (operational guard; see header)"),
                   ls0 = list(value = TRUE, source = "author (v3.1 default)"),
                   method_settings = list(value = "all internal to v3_fit (N = max(2500,n,p), R' = 4, calibration, LS0)", source = "author"),
                   selection = list(value = "MPM: pip_primary > 0.5", source = "OURS (INTERFACE.md rule)"),
                   preprocessing = list(value = paste("raw X, y passed; v3_fit's own v3_preprocess centres and scales every X column",
                     "and y (sample SD, n - 1), which is equivalent to the repo's X <- scale(X), y <- scale(y, scale = FALSE)",
                     "up to rounding (specs/generator_check.md); no intercept parameter, centring stands in for it"),
                     source = "authors' repo preprocessing (HQ ruling), applied by the engine itself"))
  t0 <- proc.time()[["elapsed"]]
  fit <- tryCatch({
    if (!exists("v3_fit", envir = globalenv())) {
      Sys.setenv(V3_CORE_DIR = SMCBVS_CORE_DIR)
      source(file.path(SMCBVS_CORE_DIR, "v3.R"), local = FALSE)
    }
    if (!identical(Sys.getenv("SMCBVS_PROGRESS"), "0")) {            # SMCBVS_PROGRESS=0 turns the lines off
      smcbvs_progress_hooks()
      assign(".smcbvs_progress_t0", proc.time()[["elapsed"]], envir = globalenv())
      message(sprintf("PROGRESS %s fit_t=0 v3_fit start n=%d p=%d seed=%s", format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC"),
                      nrow(X), ncol(X), method_seed))
    }
    get("v3_fit", envir = globalenv())(X, y, seed = as.numeric(method_seed), allocation = alloc)
  }, error = function(e) structure(list(status = "error", message = conditionMessage(e)), class = "smcbvs_error"))
  runtime <- proc.time()[["elapsed"]] - t0
  keep(fit)
  ok <- !inherits(fit, "smcbvs_error") && isTRUE(fit$estimates_available) && !is.null(fit$pip_primary)
  if (!ok) {
    msg <- paste0("failed: v3_fit status=", fit$status %||% "NA", if (!is.null(fit$message)) paste0(": ", fit$message) else "")
    return(list(selected = integer(0), pip = NULL, runtime_sec = runtime, software = sw, settings = settings,
                extra = list(status = msg, engine_tag = SMCBVS_ENGINE_TAG,
                             preflight = if (!inherits(fit, "smcbvs_error")) fit$preflight else NULL,
                             eflags = paste0("status:", fit$status %||% "error"), eflag_any = TRUE,
                             json_summary = list(engine_tag = SMCBVS_ENGINE_TAG, v3_status = fit$status %||% "error",
                                                 eflag_any = TRUE, eflags = paste0("status:", fit$status %||% "error")))))
  }
  pip <- numeric(p)                                     # columns dropped by preprocessing (none expected) get PIP 0
  pip[as.integer(names(fit$pip_primary))] <- as.numeric(fit$pip_primary)
  selected <- sort(as.integer(fit$mpm))
  tier <- fit$frozen[["tier"]] %||% 0
  N <- fit$budgets$tiers$N[tier + 1]
  st <- fit$stage_table
  ess <- if (!is.null(st) && "ess" %in% names(st)) st[, intersect(c("phase", "tier", "iter", "island", "stage", "phi", "ess"), names(st))] else NULL
  topm <- smcbvs_top_models(fit$top_store, 50)
  fin <- if (!is.null(ess)) ess[grepl("^final", ess$phase), , drop = FALSE] else NULL
  # (4) min ESS/N over the final (inference) run; N = particles per island of the frozen tier (final ESS <= N per island)
  if (!is.null(st) && "ess" %in% names(st)) st$ess_over_N <- ifelse(grepl("^final", st$phase), st$ess / N, NA_real_)
  mi <- if (!is.null(fin) && nrow(fin)) which.min(fin$ess) else integer(0)
  ess_min <- if (length(mi)) list(min_ess_over_N = fin$ess[mi] / N, phase = fin$phase[mi], island = fin$island[mi],
                                  stage = fin$stage[mi], phi = fin$phi[mi], n_stages_per_island = max(fin$stage)) else
    list(min_ess_over_N = NA_real_)
  lzr <- as.numeric(fit$log_Z_r)
  lz_spread <- list(sd = if (length(lzr) > 1) stats::sd(lzr) else NA_real_, range = if (length(lzr)) diff(range(lzr)) else NA_real_)
  ef <- smcbvs_eflags(fit)
  size_mass <- smcbvs_size_mass(fit$top_store)
  extra <- list(status = "ok", engine_tag = SMCBVS_ENGINE_TAG, v3_status = fit$status,
                N_particles = N, islands = length(fit$log_Z_r), tier = tier, escalated = isTRUE(fit$flags$escalated),
                log_Z = fit$log_Z, log_Z_r = fit$log_Z_r, log_Z_rel_m0 = fit$log_Z_rel_m0, log_Z_lower95 = fit$log_Z_lower95,
                hpm = sort(as.integer(fit$hpm)), hpm_F = fit$hpm_F, top_models = topm,
                ess_per_stage = ess, stage_table = st, flags = fit$flags, timings = fit$timings,
                timings_calibration = lapply(fit$calibration$tiers, function(t) c(tier = t$tier, t$seconds, rebuilds = t$rebuilds %||% NA)),
                pip_list = fit$pip_list, mpm_list = fit$mpm_list, log_Z_list = fit$log_Z_list,
                local_certified = fit$local_certified, peak_memory_kb = fit$peak_memory_kb, preflight = fit$preflight,
                budgets = fit$budgets[c("K", "B", "ell", "L", "N0", "H0", "T0", "R")],
                ess_min = ess_min, log_Z_r_spread = lz_spread, eflags = ef$eflags, eflag_any = ef$eflag_any,
                engine_warnings = ef$warnings, list_size_mass = size_mass,
                top_store_n = length(fit$top_store$value), top_store_full = isTRUE(fit$top_store$full),
                stage_fields_missing = "mean model size and a resample flag per stage are not recorded by the engine",
                .top_store = fit$top_store)   # dot field: used by diag_smcbvs in the harness, never saved
  extra$json_summary <- list(engine_tag = SMCBVS_ENGINE_TAG, v3_status = fit$status, N_particles = N, tier = tier,
                             escalated = extra$escalated, log_Z = fit$log_Z, log_Z_rel_m0 = fit$log_Z_rel_m0,
                             hpm = extra$hpm, n_stages_final = if (!is.null(fin)) nrow(fin) else NA,
                             min_ess_final = if (!is.null(fin) && nrow(fin)) min(fin$ess) else NA,
                             top5 = if (!is.null(topm)) head(topm[, c("model", "weight_list")], 5) else NULL,
                             checks_passed_final = fit$flags$checks_passed_final, total_sec = fit$timings$total,
                             min_ess_over_N = ess_min$min_ess_over_N, log_Z_r_sd = lz_spread$sd, log_Z_r_range = lz_spread$range,
                             eflag_any = ef$eflag_any, eflags = ef$eflags, engine_warnings = ef$warnings)
  list(selected = selected, pip = pip, runtime_sec = runtime, software = sw, settings = settings, extra = extra)
}
