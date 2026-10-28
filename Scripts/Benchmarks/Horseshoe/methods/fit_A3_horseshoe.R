# Benchmark A3: horseshoe regression with bayesreg 1.3 (master §III.3.8, items a-l).
# Model (item a): y_i = b0 + sum_j xs_ij b_j + e_i, e_i ~ N(0, s2), with bayesreg's unit-length
# standardisation xs_j = (x_j - mean x_j) / ||x_j - mean x_j||; b_j ~ N(0, s2 tau2 lambda_j^2),
# lambda_j, tau ~ C+(0, 1); pi(s2) ~ 1/s2; flat b0. Draws are returned on the scale of X.
# Rules (item f): ci95 (primary) = {j : 0 outside the equal-tailed 95% interval of beta_j};
# km2 (S0) = the larger-centre cluster of a 2-means fit to |posterior mean of beta_j|.
# Uses common.R: assert_inputs, assert_pkg_version, with_captured_conditions, make_rule_rows,
# fail_rows, support_key, elapsed. Every constant is read from `settings` (§III.3.0).

# Item (e) step 1: exact package versions (bayesreg, pgdraw, doParallel).
a3_check_backend <- function(settings) {
  for (pk in names(settings$A3$PKG_VERSIONS))
    assert_pkg_version(pk, settings$A3$PKG_VERSIONS[[pk]])
  invisible(TRUE)
}

# Item (e) steps 2-3: one chain of bayesreg on the global RNG, seeded here; the hash of
# .Random.seed is taken right after the MCMC (before any other random draw) for the
# common-random-numbers check done at scoring.
a3_call <- function(X, y, seed, settings) {
  p <- ncol(X)
  colnames(X) <- paste0("X", seq_len(p))
  df <- data.frame(X, y = y)          # formula y ~ . keeps the intercept column that bayesreg drops (item c)
  set.seed(seed)
  res <- with_captured_conditions(bayesreg::bayesreg(y ~ ., data = df,
            model = settings$A3$MODEL, prior = settings$A3$PRIOR,
            n.samples = settings$A3$N_SAMPLES, burnin = settings$A3$BURNIN,
            thin = settings$A3$THIN, t.dof = settings$A3$T_DOF, n.cores = settings$A3$N_CORES))
  rng_after <- digest::digest(get(".Random.seed", envir = globalenv()), algo = "sha256")
  list(fit = res$value, error = res$error, warnings = res$warnings, messages = res$messages,
       rng_after = rng_after)
}

# Item (e) step 4 and item (h): fit-level checks. Returns NULL when all pass, else the
# reason (a failed check fails the fit).
a3_fit_checks <- function(fit, p, settings) {
  M <- as.integer(settings$A3$N_SAMPLES)
  B <- fit$beta
  if (!identical(as.integer(fit$p), as.integer(p))) return("fit$p != p")
  if (!is.matrix(B) || !identical(dim(B), c(as.integer(p), M))) return("dim(fit$beta) != c(p, n.samples)")
  if (!all(is.finite(B))) return("non-finite draws of beta")
  tau2 <- as.vector(fit$tau2); sigma2 <- as.vector(fit$sigma2)
  if (length(tau2) != M || !all(is.finite(tau2) & tau2 > 0)) return("bad tau2 draws")
  if (length(sigma2) != M || !all(is.finite(sigma2) & sigma2 > 0)) return("bad sigma2 draws")
  if (!identical(as.numeric(fit$n.cores), 1)) return(paste0("fit$n.cores = ", fit$n.cores, ", expected 1"))
  # Orientation and back-transformation check. Only in the Bhattacharya branch (p/n >= 2, every
  # production fit) is fit$mu.beta the mean of the draws (r$m = r$x, bayesreg.R l. 2334-2335);
  # Rue's branch (p/n < 2, unit-test canary only) returns the Rao-Blackwellised mean, which
  # differs from rowMeans(B) by Monte Carlo error, so the check does not apply there.
  if (p / fit$n >= 2) {
    mu <- rowMeans(B)
    dmu <- max(abs(as.vector(fit$mu.beta) - mu))
    if (!is.finite(dmu) || dmu > settings$A3$MU_TOL * (1 + max(abs(mu))))
      return(sprintf("max|mu.beta - rowMeans(beta)| = %.3g exceeds tolerance", dmu))
  }
  NULL
}

# Item (e) step 5, item (g): per-coefficient summary table (p x 7). ess_coda is filled later
# for the coefficients selected by ci95 or km2 (NA otherwise).
a3_summaries <- function(fit, settings) {
  B <- fit$beta
  probs <- c(settings$A3$CI_PROBS[1], 0.5, settings$A3$CI_PROBS[2])
  q <- apply(B, 1, stats::quantile, probs = probs, names = FALSE, type = settings$A3$QTYPE)  # 3 x p
  data.frame(mean = rowMeans(B), sd = apply(B, 1, stats::sd),
             q025 = q[1, ], q50 = q[2, ], q975 = q[3, ],
             ess_pkg = as.numeric(fit$ess), ess_coda = NA_real_,
             row.names = NULL)
}

# Item (f), rule km2: our 2-means on |posterior mean|, seeded with the method seed; the
# cluster with the larger centre is selected. Fails with < 2 distinct values or a kmeans error.
a3_kmeans2 <- function(absmu, seed, settings) {
  if (length(unique(absmu)) < 2L)
    return(list(failed = TRUE, error = "km2: fewer than two distinct |mu| values",
                selected = NULL, km = NULL, warnings = character(0), messages = character(0)))
  set.seed(seed)
  res <- with_captured_conditions(stats::kmeans(absmu, centers = 2,
            nstart = settings$A3$KM_NSTART, iter.max = settings$A3$KM_ITER_MAX,
            algorithm = settings$A3$KM_ALGORITHM))
  if (!is.null(res$error))
    return(list(failed = TRUE, error = paste("km2: kmeans error:", res$error), selected = NULL,
                km = NULL, warnings = res$warnings, messages = res$messages))
  km <- res$value
  big <- which.max(as.vector(km$centers))
  list(failed = FALSE, error = NA_character_, selected = which(km$cluster == big),
       km = list(centers = as.vector(km$centers), size = as.vector(km$size),
                 tot.withinss = km$tot.withinss, selected_cluster = big,
                 iter = km$iter, ifault = km$ifault),
       warnings = res$warnings, messages = res$messages)
}

# Item (f): ci95 = {j : q025_j > 0 or q975_j < 0}; an endpoint exactly 0 includes 0. No cap.
a3_rules <- function(coef, seed, settings) {
  ci95 <- which(coef$q025 > 0 | coef$q975 < 0)
  km2 <- a3_kmeans2(abs(coef$mean), seed, settings)
  list(ci95 = ci95, km2 = km2)
}

# Item (e) step 7: coda ESS of log tau2, log sigma2 and of the selected coefficients.
# An error or a non-finite value is recorded as NA; warnings and messages raised by coda are
# captured (they are conditions of the fit, §III.3.0 Status) and returned in `warnings`/`messages`.
a3_ess_one <- function(x) {
  res <- with_captured_conditions(unname(coda::effectiveSize(x)))
  v <- res$value
  if (!is.null(res$error) || length(v) != 1L || !is.finite(v)) v <- NA_real_
  list(value = v, warnings = res$warnings, messages = res$messages,
       error = if (is.null(res$error)) character(0) else res$error)
}
a3_ess <- function(fit, sel_ci95, sel_km2) {
  B <- fit$beta
  sel <- sort(unique(c(sel_ci95, sel_km2)))
  warnings <- character(0); messages <- character(0); errors <- character(0)
  ess_of <- function(x) {
    r <- a3_ess_one(x)
    warnings <<- c(warnings, r$warnings); messages <<- c(messages, r$messages); errors <<- c(errors, r$error)
    r$value
  }
  ess_log_tau2 <- ess_of(log(as.vector(fit$tau2)))
  ess_log_sigma2 <- ess_of(log(as.vector(fit$sigma2)))
  ess_sel <- vapply(sel, function(j) ess_of(B[j, ]), 0)
  names(ess_sel) <- sel
  min_over <- function(idx) {
    if (length(idx) == 0L) return(NA_real_)          # empty set: no ESS (flag vacuous, item h)
    v <- ess_sel[as.character(idx)]
    if (any(is.na(v))) NA_real_ else min(v)
  }
  list(ess_log_tau2 = ess_log_tau2, ess_log_sigma2 = ess_log_sigma2, ess_sel = ess_sel,
       min_ess_ci95 = min_over(sel_ci95), min_ess_km2 = min_over(sel_km2),
       warnings = warnings, messages = messages, errors = errors)   # errors: recorded only (value NA)
}

# Item (h), "the split-chain value is recorded only": potential scale reduction of one chain
# split into two halves, sqrt(((m - 1)/m W + B/m) / W) with m draws per half, W the mean of the two
# within-half variances and B = m var(half means). Recorded in the RDS; never a flag.
a3_split_rhat <- function(x) {
  m <- floor(length(x) / 2)
  if (m < 2L) return(NA_real_)
  h1 <- x[1:m]; h2 <- x[(m + 1):(2 * m)]
  W <- (stats::var(h1) + stats::var(h2)) / 2
  B <- m * stats::var(c(mean(h1), mean(h2)))
  v <- sqrt(((m - 1) / m * W + B / m) / W)
  if (is.finite(v)) v else NA_real_
}

# Item (h): flag codes of the fit (ess_tau, ess_ci95). crn_mismatch is set by scoring.
a3_gates <- function(ess, n_ci95, settings) {
  codes <- character(0)
  if (is.na(ess$ess_log_tau2) || ess$ess_log_tau2 < settings$A3$ESS_MIN) codes <- c(codes, "ess_tau")
  if (n_ci95 > 0L && (is.na(ess$min_ess_ci95) || ess$min_ess_ci95 < settings$A3$ESS_MIN))
    codes <- c(codes, "ess_ci95")
  codes
}

# Supports for audit when a fit-level check failed but the draws are usable (§III.3.0 Failures).
a3_audit_supports <- function(fit, p, seed, settings) {
  B <- fit$beta
  if (!is.matrix(B) || nrow(B) != p || !all(is.finite(B))) return(NULL)
  out <- tryCatch({
    coef <- a3_summaries(fit, settings)
    r <- a3_rules(coef, seed, settings)
    list(ci95 = r$ci95, km2 = if (r$km2$failed) NULL else r$km2$selected)
  }, error = function(e) NULL)
  out
}

# §III.3.0 interface. settings$variant must be "primary" (the S2 variants hsplus and hspkg are
# not approved and not implemented).
fit_A3_horseshoe <- function(X, y, foldid, seed, settings) {
  if (!identical(settings$variant, "primary"))
    stop("fit_A3_horseshoe: variant '", settings$variant, "' is S2 and not approved")
  assert_inputs(X, y, foldid, tol = settings$COMMON$X_TOL, nfolds = settings$COMMON$NFOLDS)
  a3_check_backend(settings)
  if (!identical(RNGkind(), settings$COMMON$RNG_KIND))
    stop("fit_A3_horseshoe: RNGkind is ", paste(RNGkind(), collapse = "/"))
  n <- nrow(X); p <- ncol(X)
  sampler <- if (p / n >= 2) "bhattacharya" else "rue"       # bayesreg's rule (item a)
  detect_cores <- parallel::detectCores()

  call <- a3_call(X, y, seed, settings)
  fail_extra <- list(rng_after = NA_character_, diag_s = NA_real_)
  if (!is.null(call$error)) {
    rows <- fail_rows(settings, "A3", error = call$error, warnings = call$warnings,
                      messages = call$messages, extra = fail_extra)
    return(list(rules = rows, pip = NULL, beta = rep(NA_real_, p), converged = NA,
                diagnostics = list(rng_kind = RNGkind(), detect_cores = detect_cores,
                                   sampler = sampler, rng_after = NA_character_),
                warnings = c(call$warnings, call$messages)))
  }
  fit <- call$fit
  check <- a3_fit_checks(fit, p, settings)
  if (!is.null(check)) {
    rows <- fail_rows(settings, "A3", error = paste("fit check failed:", check),
                      warnings = call$warnings, messages = call$messages,
                      support_audit = a3_audit_supports(fit, p, seed, settings), extra = fail_extra)
    return(list(rules = rows, pip = NULL, beta = rep(NA_real_, p), converged = NA,
                diagnostics = list(rng_kind = RNGkind(), detect_cores = detect_cores,
                                   sampler = sampler, rng_after = NA_character_,
                                   n_cores = fit$n.cores),
                warnings = c(call$warnings, call$messages)))
  }

  coef <- a3_summaries(fit, settings)
  rules <- a3_rules(coef, seed, settings)

  t_diag <- proc.time()[["elapsed"]]
  ess <- a3_ess(fit, rules$ci95, if (rules$km2$failed) integer(0) else rules$km2$selected)
  diag_s <- elapsed(t_diag)
  coef$ess_coda[as.integer(names(ess$ess_sel))] <- ess$ess_sel
  codes <- a3_gates(ess, length(rules$ci95), settings)
  diag_flag <- length(codes) > 0L

  # Status reflects captured conditions only (§III.3.0). Conditions of the bayesreg call and of
  # the ESS step are fit-level and apply to both rules; conditions of the kmeans call apply to
  # km2 only.
  fit_w <- c(call$warnings, ess$warnings)
  fit_m <- c(call$messages, ess$messages)
  fit_cond <- length(fit_w) + length(fit_m) > 0L
  km_cond <- length(rules$km2$warnings) + length(rules$km2$messages) > 0L
  per_rule <- list(
    ci95 = list(status = if (fit_cond) "warning" else "ok", support = rules$ci95,
                warnings = fit_w, messages = fit_m, error = NA_character_),
    km2 = if (rules$km2$failed)
      list(status = "failed", support = NULL, warnings = c(fit_w, rules$km2$warnings),
           messages = c(fit_m, rules$km2$messages), error = rules$km2$error)
    else
      list(status = if (fit_cond || km_cond) "warning" else "ok", support = rules$km2$selected,
           warnings = c(fit_w, rules$km2$warnings),
           messages = c(fit_m, rules$km2$messages), error = NA_character_))
  rows <- make_rule_rows(settings, "A3", per_rule, converged = NA, diag_flag = diag_flag,
                         diag_codes = codes, extra = list(rng_after = call$rng_after, diag_s = diag_s))

  diagnostics <- list(
    coef = coef,
    trace_log_tau2 = log(as.vector(fit$tau2)), trace_sigma2 = as.vector(fit$sigma2),
    ess_log_tau2 = ess$ess_log_tau2, ess_log_sigma2 = ess$ess_log_sigma2,
    split_rhat_log_tau2 = a3_split_rhat(log(as.vector(fit$tau2))),
    split_rhat_log_sigma2 = a3_split_rhat(log(as.vector(fit$sigma2))),
    min_ess_ci95 = ess$min_ess_ci95, min_ess_km2 = ess$min_ess_km2,
    rng_kind = RNGkind(), detect_cores = detect_cores,
    beta0_mean = as.numeric(fit$mu.beta0), waic = as.numeric(fit$waic),
    n_cores = fit$n.cores, sampler = sampler, rng_after = call$rng_after,
    km2 = rules$km2$km, diag_s = diag_s,
    warnings = call$warnings, messages = call$messages,
    ess_warnings = ess$warnings, ess_messages = ess$messages, ess_errors = ess$errors,
    km2_warnings = rules$km2$warnings, km2_messages = rules$km2$messages,
    settings_echo = settings$A3)
  out <- list(rules = rows, pip = NULL, beta = coef$mean, converged = NA,
              diagnostics = diagnostics,
              warnings = c(fit_w, fit_m, rules$km2$warnings, rules$km2$messages))
  rm(fit)
  out
}
