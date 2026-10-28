# fit_A2_ssl.R -- benchmark A2, spike-and-slab lasso (SSLASSO 1.2.3.9001, native routine).
# Implements master §III.3.7 (items a-h, k) under the common rules of §III.3.0.
#   Model (§III.3.7 a): y ~ N(X beta, sigma^2 I), no intercept, y not centred;
#   pi(beta | theta) = prod_j [theta psi(beta_j | lambda1) + (1 - theta) psi(beta_j | lambda0)],
#   psi(b | lambda) = (lambda / 2) exp(-lambda |b|); theta ~ Beta(a, b = p); sigma^2 estimated.
#   Quantity read: the posterior mode beta-hat at the last point of an increasing lambda0
#   ladder (coordinate ascent with warm starts). Selected support {j : beta-hat_j != 0}.
#   Variants: "primary" (lambda1 = 1, lambda0 = seq(1, n, length.out = 100)) and
#   "RS" (S1, Ray & Szabo 2022: lambda1 = 0.01, lambda0 = seq(1, p, length.out = 200)).
# Uses from common.R: assert_inputs, assert_pkg_version, with_captured_conditions,
# support_key, make_rule_rows, fail_rows, registry_row.

# Version and registration checks (§III.3.7 b "Version assertions"; e step 1).
a2_check_backend <- function(settings) {
  if (!requireNamespace("SSLASSO", quietly = TRUE)) stop("a2_check_backend: SSLASSO not available")
  assert_pkg_version("SSLASSO", settings$A2$PKG_VERSION)
  n_par <- getDLLRegisteredRoutines("SSLASSO")$.Call$SSL_gaussian$numParameters
  if (is.null(n_par) || !identical(as.integer(n_par), as.integer(settings$A2$N_PARAMS)))
    stop("a2_check_backend: SSL_gaussian is not registered with ", settings$A2$N_PARAMS, " parameters")
  invisible(TRUE)
}

# Resolve the strings "n" and "p" of config.R to numbers (§III.3.7 d, note under the table).
a2_resolve <- function(value, n, p) {
  if (identical(value, "n")) return(as.numeric(n))
  if (identical(value, "p")) return(as.numeric(p))
  as.numeric(value)
}

# Ladder (§III.3.7 e step 2): primary lambda0 = seq(1, n, length.out = 100), lambda1 = 1;
# S1 "RS" lambda0 = seq(1, p, length.out = 200), lambda1 = 0.01.
a2_ladder <- function(n, p, variant, settings) {
  blk <- switch(variant,
                primary = settings$A2,
                RS      = settings$A2RS,
                stop("a2_ladder: variant '", variant, "' is not registered (S2 'wrapper' is not run)"))
  list(lambda0 = seq(1, a2_resolve(blk$LAMBDA0_MAX, n, p), length.out = blk$NLAMBDA),
       lambda1 = blk$LAMBDA1)
}

# Native path (§III.3.7 e, code block). Calls the registered routine SSL_gaussian directly
# with the stored X and the uncentred y (O5 default; the public SSLASSO() centres X and y).
# Initialisation reproduced from the wrapper (SSLASSO.R l. 154-166): sigma0 from sd(y),
# min_sigma2 = sd(y)^2 / n, theta0 = THETA_INIT, beta0 = 0. sigma0 argument: tests only.
a2_native_path <- function(X, y, lambda0, lambda1, settings, sigma0 = NULL) {
  n <- nrow(X); p <- ncol(X)
  stopifnot(all(diff(lambda0) > 0), lambda1 <= min(lambda0))   # the wrapper's own checks (l. 140-148)
  s_y  <- stats::sd(y)
  ncp  <- s_y^2 * stats::qchisq(1 - settings$A2$SIGMA_QUANT, settings$A2$SIGMA_DF) / settings$A2$SIGMA_DF
  sig0 <- if (is.null(sigma0)) sqrt(settings$A2$SIGMA_DF * ncp / (settings$A2$SIGMA_DF + 2)) else sigma0
  storage.mode(X) <- "double"
  res <- .Call("SSL_gaussian", X, as.double(y), as.double(numeric(p)),
               settings$A2$PENALTY, settings$A2$VARIANCE,
               as.double(lambda1), as.double(lambda0), as.double(settings$A2$THETA_INIT),
               as.double(sig0), as.double(s_y^2 / n), as.double(settings$A2$A),
               as.double(a2_resolve(settings$A2$B, n, p)),
               as.double(settings$A2$EPS), as.integer(settings$A2$MAX_ITER),
               as.integer(settings$A2$COUNTER), PACKAGE = "SSLASSO")
  # Output list: beta (p x L, column-major), loss, iter, theta, sigma (SSL_gaussian.c l. 21-40).
  # res[[2]] (loss) is not used: it is uninitialised at a capped point (§III.3.7 e step 4).
  list(beta = matrix(res[[1]], nrow = p, ncol = length(lambda0)),
       iter = res[[3]], theta = res[[4]], sigma = res[[5]],
       sigma0 = sig0, min_sigma2 = s_y^2 / n, max_iter = as.integer(settings$A2$MAX_ITER))
}

# Per-ladder-point table (§III.3.7 e step 5, g): lambda0, sweeps, capped, theta, sigma, k,
# R-side RSS and support key. theta and sigma that the C code did not write (NaN) are NA.
a2_path_table <- function(X, y, path, lambda0) {
  B <- path$beta
  rss <- colSums((y - X %*% B)^2)              # recomputed in R; native loss is not trusted
  nz <- B != 0
  data.frame(point   = seq_along(lambda0),
             lambda0 = lambda0,
             iter    = path$iter,
             capped  = path$iter >= path$max_iter,
             theta   = ifelse(is.nan(path$theta), NA_real_, path$theta),
             sigma   = ifelse(is.nan(path$sigma), NA_real_, path$sigma),
             k       = colSums(nz, na.rm = TRUE),
             rss     = rss,
             support_key = apply(nz, 2, function(s) support_key(which(s))),
             stringsAsFactors = FALSE)
}

# Fixed-point audit at the final point (§III.3.7 h; port of Oct-7 SSL/fit.R .ssl_coordinate_audit).
# Recomputes, from beta, theta and sigma2, the quantities of §III.3.7 a:
#   d_j = ||x_j||^2, z_j = x_j' r + d_j beta_j with r = y - X beta,
#   p*(b) = theta l1 e^{-l1|b|} / (theta l1 e^{-l1|b|} + (1 - theta) l0 e^{-l0|b|}),
#   lambda*(b) = l1 p*(b) + l0 (1 - p*(b)),
#   Delta_j = sqrt(2 d_j sigma2 log(1 / p*(0))) + sigma2 l1 if g(0) > 0, else sigma2 lambda*(0),
#     g(0) = (lambda*(0) - l1)^2 + (2 d_j / sigma2) log p*(0); Delta_j = sigma2 l1 if l0 = l1,
#   map: beta_j <- 0 if |z_j| <= Delta_j, else sign(z_j) (|z_j| - sigma2 lambda*(beta_j))_+ / d_j,
# applies the map once (all coordinates from the same residual) and compares with beta.
a2_fixed_point_audit <- function(X, y, beta, sigma2, theta, lambda0, lambda1) {
  d <- colSums(X * X)
  r <- as.vector(y - X %*% beta)
  z <- as.vector(crossprod(X, r)) + d * beta
  if (lambda0 == lambda1) {
    lambda_star <- rep(lambda1, length(beta))
    delta <- rep(sigma2 * lambda1, length(beta))
  } else {
    # p*(b) written as plogis(logit(theta) + log(l1/l0) + |b|(l0 - l1)): the same quantity as
    # the ratio above, evaluated without overflow of e^{l0 |b|} for large |b|.
    log_odds0 <- stats::qlogis(theta) + log(lambda1 / lambda0)
    p0 <- stats::plogis(log_odds0)
    pstar <- stats::plogis(log_odds0 + abs(beta) * (lambda0 - lambda1))
    lambda_star0 <- lambda1 * p0 + lambda0 * (1 - p0)
    lambda_star <- lambda1 * pstar + lambda0 * (1 - pstar)
    g0 <- (lambda_star0 - lambda1)^2 + 2 * d / sigma2 * log(p0)
    delta <- ifelse(g0 > 0, sqrt(2 * d * sigma2 * (-log(p0))) + sigma2 * lambda1, sigma2 * lambda_star0)
  }
  mapped <- sign(z) * pmax(abs(z) - sigma2 * lambda_star, 0) / d
  mapped[abs(z) <= delta] <- 0
  list(max_abs_fixed_point_error = max(abs(mapped - beta)),
       support_mismatch = sum((mapped != 0) != (beta != 0)),
       mapped_support_key = support_key(which(mapped != 0)),
       threshold = delta, z = z, rss = sum(r^2))
}

# Gates and flags (§III.3.7 h; §III.3.0 status / diag_flag / converged).
# Failure (rule failed, not retried): non-finite beta at the final point; final point capped
# (iterations = max_iter); theta_L or sigma_L non-finite or outside (0, 1) and (0, Inf).
# Flags (diag_flag; never change status): tail_unstable, fixed_point.
# Informational code (diag_codes only; lead decision 2026-10-19, production-readiness brief):
# capped_intermediate. It fired on 24/24 dev fits from the package's own sigma^2 reset cycle.
a2_gates <- function(path, tab, audit, settings) {
  L <- nrow(tab)
  beta_L <- path$beta[, L]
  theta_L <- path$theta[L]; sigma_L <- path$sigma[L]
  reasons <- character()
  if (any(!is.finite(beta_L))) reasons <- c(reasons, "non-finite beta at the final point")
  if (tab$capped[L]) reasons <- c(reasons, "final point capped (iterations = max_iter)")
  if (!is.finite(theta_L) || theta_L <= 0 || theta_L >= 1) reasons <- c(reasons, "theta at the final point non-finite or outside (0, 1)")
  if (!is.finite(sigma_L) || sigma_L <= 0) reasons <- c(reasons, "sigma at the final point non-finite or not positive")

  tail_idx <- seq(max(1L, L - settings$A2$STABLE_TAIL + 1L), L)
  tail_stable <- length(unique(tab$support_key[tail_idx])) == 1L
  fp_tol <- settings$A2$FP_TOL_MULT * settings$A2$EPS * (1 + max(abs(beta_L)))
  fp_fail <- !is.null(audit) && (audit$support_mismatch > 0 || audit$max_abs_fixed_point_error > fp_tol)

  codes <- c(capped_intermediate = L > 1L && any(tab$capped[-L]),   # informational
             tail_unstable = !tail_stable,                          # flag
             fixed_point = fp_fail)                                 # flag
  flags <- codes[c("tail_unstable", "fixed_point")]
  list(fail_reasons = reasons, failed = length(reasons) > 0L,
       converged = !tab$capped[L],                 # solver's own criterion (§III.3.0)
       diag_flag = any(flags), diag_codes = paste(names(codes)[codes], collapse = ";"),
       tail_idx = tail_idx, tail_stable = tail_stable, fp_tol = fp_tol, audit_run = !is.null(audit))
}

# Rules (§III.3.7 f): ssl_final = {j : beta-hat_j != 0} at the last lambda0 (exact zeros).
# The same rule for both registered variants; roles come from the METHODS registry.
a2_rules <- function(beta_final, variant) {
  stopifnot(variant %in% c("primary", "RS"))
  list(ssl_final = which(beta_final != 0))
}

# Wrapper (§III.3.0 interface). foldid is checked and unused; seed is unused (SSL uses no
# random numbers; the runner records it as method_seed).
fit_A2_ssl <- function(X, y, foldid, seed, settings) {
  assert_inputs(X, y, foldid, settings$COMMON)
  a2_check_backend(settings)
  reg <- registry_row(settings, fn = "fit_A2_ssl", variant = settings$variant)
  n <- nrow(X); p <- ncol(X)
  lad <- a2_ladder(n, p, settings$variant, settings)
  L <- length(lad$lambda0)
  echo <- list(variant = settings$variant, A2 = settings$A2,
               A2RS = if (identical(settings$variant, "RS")) settings$A2RS else NULL,
               lambda0 = lad$lambda0, lambda1 = lad$lambda1)

  cap <- with_captured_conditions(a2_native_path(X, y, lad$lambda0, lad$lambda1, settings))
  if (!is.null(cap$error)) {                               # failure 1: the native call errors
    return(list(rules = fail_rows(reg$rule_ids, reg$roles, NULL, paste("native call error:", cap$error)),
                pip = NULL, beta = rep(NA_real_, p), converged = FALSE,
                diagnostics = list(settings_echo = echo, fail_reasons = "native call error"),
                warnings = cap$warnings, messages = cap$messages))
  }
  path <- cap$value
  tab <- a2_path_table(X, y, path, lad$lambda0)
  beta_final <- path$beta[, L]
  theta_L <- path$theta[L]; sigma_L <- path$sigma[L]
  audit_ok <- all(is.finite(beta_final)) && is.finite(theta_L) && theta_L > 0 && theta_L < 1 &&
              is.finite(sigma_L) && sigma_L > 0
  audit <- if (audit_ok) a2_fixed_point_audit(X, y, beta_final, sigma_L^2, theta_L,
                                              lad$lambda0[L], lad$lambda1) else NULL
  g <- a2_gates(path, tab, audit, settings)
  supports <- a2_rules(beta_final, settings$variant)
  stopifnot(identical(names(supports), unlist(reg$rule_ids)))

  if (g$failed) {
    rules <- fail_rows(reg$rule_ids, reg$roles, supports[[1]], paste(g$fail_reasons, collapse = "; "),
                       converged = FALSE, diag_flag = g$diag_flag, diag_codes = g$diag_codes)
  } else {
    status <- if (length(cap$warnings) + length(cap$messages) > 0L) "warning" else "ok"
    rules <- make_rule_rows(reg$rule_ids, reg$roles, supports, status,
                            converged = g$converged, diag_flag = g$diag_flag, diag_codes = g$diag_codes)
  }
  capped_index <- which(tab$capped)
  list(rules = rules, pip = NULL,
       beta = if (g$failed) rep(NA_real_, p) else beta_final,
       converged = if (g$failed) FALSE else g$converged,
       diagnostics = list(
         path = tab, beta_final = beta_final,
         audit = c(audit, list(tolerance = g$fp_tol, run = g$audit_run,
                               tail_keys = tab$support_key[g$tail_idx], tail_stable = g$tail_stable)),
         capped_index = capped_index, n_capped = sum(tab$capped[-L]),
         sigma0 = path$sigma0, min_sigma2 = path$min_sigma2,
         theta_L = theta_L, sigma_L = sigma_L, rss_L = tab$rss[L],
         fail_reasons = g$fail_reasons, settings_echo = echo),
       warnings = cap$warnings, messages = cap$messages)
}
