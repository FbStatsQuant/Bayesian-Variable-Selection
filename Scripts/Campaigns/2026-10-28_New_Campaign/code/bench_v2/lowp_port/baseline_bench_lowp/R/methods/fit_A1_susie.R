# fit_A1_susie.R -- benchmark A1 SuSiE (susieR 0.14.2), master §III.3.6 (items a-l).
# Ported from Oct-7 `02_Experiments/C_2026-10-07_benchmarks_p30/BVS_Benchmarks/SuSiE/fit.R`.
# Differences from Oct-7: L 10 -> settings$A1$L (50; S1 100); tol 1e-4 -> 1e-3; refine TRUE ->
# FALSE; prior_weights NULL (uniform) instead of rep(1/p, p); warnings AND messages captured;
# Oct-7 settled-increment check dropped; ELBO drops in [1e-6, 1e-3] flag instead of failing;
# registry rule rows (pip05, cslead, bfdr10) instead of a logical selection vector.
# Only defines functions; sourcing it runs nothing. Every constant is read from `settings`.
# Needs the common.R helpers: assert_inputs, assert_pkg_version, with_captured_conditions,
# support_key, registry_rules, make_rule_rows, fail_rows.

# Explicit argument list of susieR::susie (§III.3.6 d, e). Every formal is passed.
a1_args <- function(X, y, L, settings) {
  A <- settings$A1
  list(X = X, y = y, L = L,
       scaled_prior_variance = A$SCALED_PRIOR_VAR,
       residual_variance = A$RESID_VAR_INIT,
       prior_weights = A$PRIOR_WEIGHTS,
       null_weight = A$NULL_WEIGHT,
       standardize = A$STANDARDIZE,
       intercept = A$INTERCEPT,
       estimate_residual_variance = A$EST_RESID_VAR,
       estimate_prior_variance = A$EST_PRIOR_VAR,
       estimate_prior_method = A$EST_PRIOR_METHOD,
       check_null_threshold = A$CHECK_NULL_THRESHOLD,
       prior_tol = A$PRIOR_TOL,
       residual_variance_upperbound = A$RESID_UB,
       s_init = A$S_INIT,
       coverage = A$COVERAGE,
       min_abs_corr = A$MIN_ABS_CORR,
       compute_univariate_zscore = A$UNIV_Z,
       na.rm = A$NA_RM,
       max_iter = A$MAX_ITER,
       tol = A$TOL,
       verbose = A$VERBOSE,
       track_fit = A$TRACK_FIT,
       residual_variance_lowerbound = stats::var(y) / A$RESID_LB_DIVISOR,
       refine = isTRUE(A$REFINE) || identical(settings$variant, "refine"),
       n_purity = A$N_PURITY)
}

# S2 susie_auto arguments (§III.3.6 f; not registered, not run unless approved).
a1_auto_args <- function(X, y, settings) {
  A <- settings$A1
  list(X = X, y = y, L_init = A$AUTO_L_INIT, L_max = A$AUTO_L_MAX, verbose = FALSE,
       init_tol = A$AUTO_INIT_TOL, standardize = A$STANDARDIZE, intercept = A$INTERCEPT,
       max_iter = A$AUTO_MAX_ITER, tol = A$AUTO_TOL)
}

# Rule ids and roles of a variant: the registry row for primary / L100; the S2 constants otherwise.
a1_rule_spec <- function(settings) {
  v <- settings$variant
  M <- settings$METHODS
  i <- which(M$fn == "fit_A1_susie" & M$variant == v)
  if (length(i) == 1L) return(c(registry_rules(settings, M$method_id[i]),
                                method_id = M$method_id[i]))
  if (v %in% c("auto", "refine"))
    return(list(rule_ids = settings$A1$S2_RULE_IDS, roles = settings$A1$S2_ROLES,
                method_id = if (v == "auto") "SuSiE-auto" else "SuSiE-refine"))
  stop("A1: unknown variant ", v)
}

# Posterior BFDR rule (§III.3.6 f; Oct-7 `.susie_bfdr_support`): order by decreasing PIP, ties by
# increasing index; longest prefix with mean(1 - PIP) <= q + eps_mult * machine epsilon.
a1_bfdr_support <- function(pip, q, eps_mult) {
  ord <- order(-pip, seq_along(pip))
  valid <- which(cumsum(1 - pip[ord]) / seq_along(pip) <= q + eps_mult * .Machine$double.eps)
  if (!length(valid)) return(integer())
  sort(as.integer(ord[seq_len(max(valid))]))
}

# CS-lead rule (§III.3.6 f): the largest-PIP member of each reported credible set; ties go to the
# smallest index (which.max on the increasing index vector); sorted union; empty if no set.
a1_cslead_support <- function(sets, pip) {
  cs <- sets$cs
  if (is.null(cs) || !length(cs)) return(integer())
  leads <- vapply(cs, function(s) {
    s <- sort(as.integer(s))
    s[which.max(pip[s])]
  }, 0L)
  sort(unique(as.integer(leads)))
}

# Rule supports (§III.3.6 f), in the order of the variant's registered rule ids.
a1_rules <- function(fit, pip, settings, variant = settings$variant) {
  spec <- a1_rule_spec(settings)
  A <- settings$A1
  all <- list(
    pip05 = function() which(pip > settings$PIP_THRESHOLD),
    cslead = function() a1_cslead_support(fit$sets, pip),
    bfdr10 = function() a1_bfdr_support(pip, A$BFDR_Q, A$BFDR_EPS_MULT))
  if (!all(spec$rule_ids %in% names(all))) stop("A1: unknown rule id")
  supports <- lapply(spec$rule_ids, function(r) as.integer(all[[r]]()))
  names(supports) <- spec$rule_ids
  list(rule_ids = spec$rule_ids, roles = spec$roles, supports = supports)
}

# Fit-level gates and flags (§III.3.6 h). Returns list(failed, reasons, flags, converged).
# `conditions` (captured warnings/messages) never fail or flag a fit (§III.3.0); it is accepted
# for the master's signature only. pip, beta and resid_lb are passed so the gate is computed on
# the exact objects the rules use.
a1_gates <- function(fit, conditions, settings, pip, beta, resid_lb) {
  A <- settings$A1
  reasons <- character()
  flags <- character()
  p <- ncol(fit$alpha)
  # Gate 2: package convergence criterion (max_iter reached).
  if (!isTRUE(fit$converged)) reasons <- c(reasons, "not converged: max_iter reached")
  # Gate 3: ELBO finite and no decrease larger than TOL; smaller drops flag (elbo_drop).
  elbo <- as.numeric(fit$elbo)
  if (!length(elbo) || any(!is.finite(elbo))) {
    reasons <- c(reasons, "ELBO non-finite")
  } else if (length(elbo) >= 2L) {
    d <- diff(elbo)
    if (any(d < -A$TOL))
      reasons <- c(reasons, sprintf("ELBO decrease %.3g > TOL", -min(d)))
    if (any(d >= -A$TOL & d < -A$ELBO_DROP_TOL)) flags <- c(flags, "elbo_drop")
  }
  # Gate 4: numerical validity of PIP, beta, sigma2, V.
  if (length(pip) != p || any(!is.finite(pip)) || any(pip < 0 | pip > 1))
    reasons <- c(reasons, "invalid PIP")
  if (length(beta) != p || any(!is.finite(beta))) reasons <- c(reasons, "non-finite beta")
  if (length(fit$sigma2) != 1L || !is.finite(fit$sigma2)) reasons <- c(reasons, "non-finite sigma2")
  if (!is.numeric(fit$V) || any(!is.finite(fit$V)) || any(fit$V < 0))
    reasons <- c(reasons, "invalid prior variance V")
  # Gate 5: contract of item (c) and PIP recomputation of step 4.
  if (!identical(as.numeric(fit$intercept), 0) ||
      length(fit$X_column_scale_factors) != p || any(fit$X_column_scale_factors != 1))
    reasons <- c(reasons, "contract: intercept or column scaling")
  if (!identical(unname(as.numeric(fit$pip)), pip))
    reasons <- c(reasons, "contract: fit$pip differs from susie_get_pip")
  # Flags L_saturated and sigma2_floor.
  n_active <- sum(fit$V > A$CS_V_THRESHOLD, na.rm = TRUE)
  if (n_active == nrow(fit$alpha)) flags <- c(flags, "L_saturated")
  if (isTRUE(fit$sigma2 <= resid_lb)) flags <- c(flags, "sigma2_floor")
  flags <- intersect(c("L_saturated", "elbo_drop", "sigma2_floor"), flags)  # fixed code order
  list(failed = length(reasons) > 0L, reasons = reasons, flags = flags,
       converged = isTRUE(fit$converged))
}

# Compact saved objects (§III.3.6 g). The full alpha (L x p) is not saved.
a1_compact <- function(fit, settings, pip, beta, resid_lb) {
  A <- settings$A1
  V <- as.numeric(fit$V)
  active <- which(V > A$CS_V_THRESHOLD)
  alpha <- fit$alpha
  unreported <- setdiff(active, fit$sets$cs_index)
  pip_unrep <- if (length(unreported))
    max(1 - apply(1 - alpha[unreported, , drop = FALSE], 2L, prod)) else 0
  # Saved alpha entries per active effect: members of its 95% set (n_in_CS_x rule of
  # susie_utils.R) when the set has <= ALPHA_CS_MAX members, else the ALPHA_TOP largest.
  alpha_saved <- do.call(rbind, lapply(active, function(l) {
    a <- alpha[l, ]
    ord <- order(-a, seq_along(a))
    m <- sum(cumsum(a[ord]) < A$COVERAGE) + 1L
    keep <- ord[seq_len(if (m <= A$ALPHA_CS_MAX) m else A$ALPHA_TOP)]
    data.frame(effect = l, index = keep, alpha = a[keep], set_size = m)
  }))
  elbo <- as.numeric(fit$elbo)
  list(pip = pip, beta = beta, V = V, lbf = as.numeric(fit$lbf),
       sigma2 = fit$sigma2, resid_lb = resid_lb, niter = fit$niter,
       converged = fit$converged, intercept = fit$intercept,
       x_scale_all_one = length(fit$X_column_scale_factors) == ncol(alpha) &&
         all(fit$X_column_scale_factors == 1),
       elbo = elbo,
       elbo_last_increment = if (length(elbo) >= 2L) elbo[length(elbo)] - elbo[length(elbo) - 1L] else NA_real_,
       sets = list(cs = fit$sets$cs, purity = fit$sets$purity, cs_index = fit$sets$cs_index,
                   coverage = fit$sets$coverage, requested_coverage = fit$sets$requested_coverage),
       L = nrow(alpha), n_active = length(active), n_cs = length(fit$sets$cs),
       L_saturated = length(active) == nrow(alpha),
       pip_unreported_max = pip_unrep, alpha_saved = alpha_saved)
}

fit_A1_susie <- function(X, y, foldid, seed, settings) {
  assert_inputs(X, y, foldid, settings$COMMON$DESIGN_TOL, settings$COMMON$N_FOLDS)
  assert_pkg_version(settings$A1$PKG, settings$A1$PKG_VERSION)
  spec <- a1_rule_spec(settings)
  p <- ncol(X)
  L <- if (identical(settings$variant, "L100")) settings$A1$L_S1 else settings$A1$L
  storage.mode(X) <- "double"
  resid_lb <- stats::var(y) / settings$A1$RESID_LB_DIVISOR
  set.seed(seed)                                   # purity subsampling only
  res <- if (identical(settings$variant, "auto")) {
    with_captured_conditions(do.call(susieR::susie_auto, a1_auto_args(X, y, settings)))
  } else {
    with_captured_conditions(do.call(susieR::susie, a1_args(X, y, L, settings)))
  }
  out <- function(rules, pip, beta, converged, diagnostics)
    list(rules = rules, pip = pip, beta = beta, converged = converged,
         diagnostics = c(diagnostics, list(L_requested = L, variant = settings$variant,
                                            settings_echo = settings$A1)),
         warnings = res$warnings, messages = res$messages)
  # Gate 1: susie() raised an error; nothing returned (support_audit NA).
  if (!is.null(res$error))
    return(out(fail_rows(spec$rule_ids, spec$roles, NA_character_,
                         paste("susie error:", res$error)),
               NULL, rep(NA_real_, p), FALSE, list()))
  fit <- res$value
  # Step 4: recompute PIPs and the posterior mean.
  pip <- susieR::susie_get_pip(fit, prune_by_cs = FALSE, prior_tol = settings$A1$PRIOR_TOL)
  beta <- susieR::susie_get_posterior_mean(fit, prior_tol = settings$A1$PRIOR_TOL)
  # Step 5: gates; steps 6-7: rules and compact objects (best effort for audit on a failed fit).
  g <- a1_gates(fit, res, settings, pip, beta, resid_lb)
  rules <- tryCatch(a1_rules(fit, pip, settings), error = function(e) NULL)
  compact_error <- NULL
  compact <- tryCatch(a1_compact(fit, settings, pip, beta, resid_lb),
                      error = function(e) {
                        compact_error <<- conditionMessage(e)
                        list(compact_error = compact_error)
                      })
  diag_flag <- length(g$flags) > 0L
  diag_codes <- paste(g$flags, collapse = ";")
  if (g$failed || is.null(rules) || !is.null(compact_error)) {
    # A fit whose item (g) objects cannot be recorded is a recording failure, not a success.
    audit <- if (is.null(rules)) NA_character_ else vapply(rules$supports, support_key, "")
    reasons <- c(g$reasons, if (is.null(rules)) "rule construction failed",
                 if (!is.null(compact_error)) paste("recording: compact diagnostics failed:",
                                                    compact_error))
    return(out(fail_rows(spec$rule_ids, spec$roles, audit, reasons, diag_flag, diag_codes),
               NULL, rep(NA_real_, p), FALSE, compact))
  }
  status <- if (length(res$warnings) || length(res$messages)) "warning" else "ok"
  out(make_rule_rows(rules$rule_ids, rules$roles, rules$supports, status, g$converged,
                     diag_flag, diag_codes),
      pip, beta, g$converged, compact)
}
