# fit_F4_mcp.R -- benchmark F4: MCP (primary) and SCAD on X/s (S1, method_id F4_SCAD), by ncvreg 3.16.0.
# Implements master §III.3.4 a-k (MASTER_Methodology_and_Plan.md, 2026-10-19) under the common rules
# of §III.3.0. Ported from Oct-14 Experiments_October_14_Benchmarks/scripts/methods.R::bench_mcp;
# differences: SCAD variant, residual-reconstruction gate, registry rule frame, BIC rule, method-wide
# diag_flag, beta at the first KKT-passing occurrence, explicit λ check.
# Uses from common.R: assert_inputs, assert_pkg_version, lambda_fraction, support_key, ols_rss
# (via ebic_candidates), ebic_candidates, ebic_pick, occurrence_ok, make_rule_rows, fail_rows,
# fail_fit_rows, registry_row, with_captured_conditions.
# `foldid` is accepted for the interface and is not used (§III.3.4 k; the CV rule is S2, not run).

fit_F4_mcp <- function(X, y, foldid, seed, settings) {
  if (!identical(settings$variant, "primary")) stop("fit_F4_mcp expects settings$variant == 'primary'")
  ncv_fit(X, y, foldid, seed, settings, penalty = "MCP", method_id = "F4")
}

fit_F4_scad <- function(X, y, foldid, seed, settings) {
  if (!identical(settings$variant, "scad")) stop("fit_F4_scad expects settings$variant == 'scad'")
  ncv_fit(X, y, foldid, seed, settings, penalty = "SCAD", method_id = "F4_SCAD")
}

# §III.3.4 e step 2: the ncvreg call. ncvreg always centres y and rescales X by its column RMS
# s_j = sqrt(sum((x_ij - mean_j)^2) / n) = s = sqrt((n - 1) / n) for our X (§III.3.4 c).
#  - MCP: passing lambda = λ/s and gamma = 3 s^2 reproduces the original-scale MCP(λ, γ = 3)
#    objective exactly, up to a constant (identity in §III.3.4 c).
#  - SCAD: no exact compensation; lambda = λ/s, gamma = 3.7 is "SCAD (a = 3.7) on X/s".
# `lam` is the original-scale grid.
ncv_call <- function(X, y, lam, settings, penalty) {
  F4 <- settings$F4
  n <- nrow(X); s <- sqrt((n - 1) / n)
  gamma_int <- if (penalty == "MCP") F4$mcp_gamma * s^2 else F4$scad_gamma
  ncvreg::ncvreg(X, y, family = "gaussian", penalty = penalty, gamma = gamma_int,
                 alpha = F4$alpha, lambda = lam / s, eps = F4$eps, max.iter = F4$maxit,
                 convex = F4$convex, dfmax = ncol(X), warn = F4$warn, returnX = F4$returnX)
}

# §III.3.4 e step 5: original-scale KKT residual of MCP(λ, γ) per path point.
# g = X'(y - X b)/n; active j: |g_j - sign(b_j) max(λ - |b_j|/γ, 0)|; inactive j: max(|g_j| - λ, 0).
# Returns the maximum over j for each column of b (lam has one entry per column).
kkt_mcp <- function(X, y, b, lam, gamma) {
  n <- nrow(X)
  G <- crossprod(X, y - X %*% b) / n                        # p x L matrix of gradients
  vapply(seq_len(ncol(b)), function(l) {
    bl <- b[, l]; g <- G[, l]; nz <- bl != 0
    act <- abs(g[nz] - sign(bl[nz]) * pmax(lam[l] - abs(bl[nz]) / gamma, 0))
    ina <- pmax(abs(g[!nz]) - lam[l], 0)
    max(c(act, ina, 0))
  }, 0.0)
}

# §III.3.4 e step 7: SCAD KKT residual on ncvreg's internal scale, theta = s b, λ' = λ/s, g' = g/s.
# active: |g'_j - sign(theta_j) d(|theta_j|)| with d(t) = λ' (t <= λ'), (a λ' - t)/(a - 1)
# (λ' < t <= a λ'), 0 beyond; inactive: max(|g'_j| - λ', 0). `lam` is the original-scale λ.
kkt_scad_internal <- function(X, y, b, lam, a, s) {
  n <- nrow(X)
  G <- crossprod(X, y - X %*% b) / n / s                    # g' = g / s
  vapply(seq_len(ncol(b)), function(l) {
    th <- s * b[, l]; g <- G[, l]; lp <- lam[l] / s; nz <- th != 0
    t <- abs(th[nz])
    d <- ifelse(t <= lp, lp, ifelse(t <= a * lp, (a * lp - t) / (a - 1), 0))
    act <- abs(g[nz] - sign(th[nz]) * d)
    ina <- pmax(abs(g[!nz]) - lp, 0)
    max(c(act, ina, 0))
  }, 0.0)
}

# Wrapper body shared by MCP and SCAD (§III.3.4 e, f, g, h). Returns the §III.3.0 list.
ncv_fit <- function(X, y, foldid, seed, settings, penalty, method_id) {
  C <- settings$COMMON; GR <- settings$GRID; F4 <- settings$F4
  mrow  <- registry_row(settings, method_id)
  extra <- settings$F4_EXTRA_COLS

  # e step 1: assertions and seed (F4 draws no random numbers after this).
  assert_inputs(X, y, foldid, C)
  assert_pkg_version("ncvreg", F4$pkg_version)
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(seed)
  n <- nrow(X); p <- ncol(X)
  s <- sqrt((n - 1) / n)

  # The F1 grid: 1.01 * zmax * frac, zmax = max_j |X_j'y| / n (lasso entry value; §III.3.1 e step 3).
  frac <- lambda_fraction(GR)
  if (length(frac) != GR$nlambda) stop("grid length != GRID$nlambda")
  zmax <- max(abs(crossprod(X, y))) / n
  if (!is.finite(zmax) || zmax <= 0) stop("invalid zmax")
  lam <- GR$max_mult * zmax * frac

  # e step 2: the package call, captured (§III.3.0 "One capture layer").
  cap <- with_captured_conditions(ncv_call(X, y, lam, settings, penalty))
  if (!is.na(cap$error)) {
    return(list(rules = fail_rows(mrow, extra, paste("ncvreg error:", cap$error)),
                pip = NULL, beta = rep(NA_real_, p), converged = FALSE,
                diagnostics = list(error = cap$error, zmax = zmax),
                warnings = cap$warnings, messages = cap$messages))
  }
  # Post-processing of the returned path. An error here (after the package call) still returns the
  # registered failed rows together with the conditions captured from ncvreg (§III.3.0).
  finish <- function() {
    fit <- cap$value
    b <- as.matrix(fit$beta[-1L, , drop = FALSE])             # original-scale slopes; row 1 = intercept
    dimnames(b) <- NULL
    L <- length(fit$lambda)

    # e step 3: path checks. Non-finite coefficients leave no usable support: the fit errors.
    if (L < 1L) stop("ncvreg returned no path point")
    if (nrow(b) != p || ncol(b) != L) stop("coefficient matrix has wrong dimensions")
    if (any(!is.finite(b))) stop("non-finite ncvreg coefficients")
    gate <- character()                                        # fit-level gate failures (fail the fit)
    lam_rel_err <- max(abs(fit$lambda / (lam / s)[seq_len(L)] - 1))
    if (!(lam_rel_err <= F4$lambda_rel_tol)) gate <- c(gate, "altered lambda")
    lam_orig <- fit$lambda * s
    truncated <- L < length(lam)                               # total-iteration (or dfmax) stop
    tot_iter <- sum(fit$iter)
    iter_capped <- tot_iter >= F4$maxit                        # last returned point may be unconverged

    # e step 4: residual reconstruction against the package loss (RSS on the centred response).
    # Compared directly on centred residuals (not as RSS(y) - n ybar^2) to avoid cancellation.
    yc <- y - mean(y)
    rss_rec  <- colSums((yc - X %*% b)^2)
    loss_pkg <- fit$loss
    rec_err  <- abs(loss_pkg - rss_rec)
    rec_tol  <- F4$loss_abs_tol * sum(yc^2) + F4$loss_rel_tol * pmax(loss_pkg, rss_rec)
    if (length(loss_pkg) != L || any(!(rec_err <= rec_tol))) gate <- c(gate, "residual reconstruction")

    # e steps 5 and 7: KKT per returned point; a point passes if its KKT residual is within the
    # tolerance and, for the last returned point, the total iterations are below max.iter.
    if (penalty == "MCP") {
      kkt <- kkt_mcp(X, y, b, lam_orig, F4$mcp_gamma)
    } else {
      kkt <- kkt_scad_internal(X, y, b, lam_orig, F4$scad_gamma, s)
    }
    if (any(!is.finite(kkt))) stop("non-finite KKT residual")
    kkt_ok <- kkt <= F4$kkt_abs_tol
    passes <- kkt_ok
    if (iter_capped) passes[L] <- FALSE

    # Method-wide flag and codes (§III.3.0 "Flags"; §III.3.4 h).
    fit_codes <- c(if (any(!kkt_ok)) "kkt_path", if (truncated) "path_truncated")
    diag_flag <- length(fit_codes) > 0L
    converged <- !truncated && !iter_capped                    # §III.3.0 "Convergence", F4

    # e step 6: supports on the path and EBIC candidates (§III.3.0).
    supports <- lapply(seq_len(L), function(l) which(abs(b[, l]) > settings$SUPPORT_ZERO_TOL))
    keys <- vapply(supports, support_key, "")
    kpath <- lengths(supports)
    cand <- ebic_candidates(X, y, supports, C$kmax_ebic, C$ebic_gamma, C$ols_tol)
    k_valid_max <- max(cand$k[cand$valid])
    k_path_max  <- max(kpath)

    # f: one rule per registered rule id; the rule id names its criterion column.
    rules <- list()
    for (rid in mrow$rule_ids[[1L]]) {
      i <- ebic_pick(cand, rid)
      key <- cand$key[i]
      ok <- occurrence_ok(key, keys, passes)
      occ <- which(keys == key & passes)
      if (!length(occ)) occ <- which(keys == key)              # for audit only (failed rule)
      pidx <- if (length(occ)) occ[1L] else NA_integer_       # NA: null support not on the path
      rules[[rid]] <- list(
        failed = !ok, key = key,
        codes = if (cand$k[i] == k_valid_max) "ebic_at_largest" else character(),
        error = if (ok) NA_character_ else "selected support has no path occurrence passing KKT and the iteration check",
        extra = list(lambda = if (is.na(pidx)) NA_real_ else lam_orig[pidx],
                     rss = cand$rss[i], crit_value = cand[[rid]][i], path_index = pidx,
                     k_valid_max = as.integer(k_valid_max), k_path_max = as.integer(k_path_max)))
    }
    rows <- make_rule_rows(mrow, rules, converged, diag_flag, fit_codes, extra)

    # g: beta at the first KKT-passing occurrence of the ebic1 support (zero for the null support);
    # NA if that rule failed or the fit failed a gate (§III.3.0: a failed fit has NA beta).
    beta <- rep(NA_real_, p)
    r1 <- rules[["ebic1"]]
    if (!r1$failed) beta <- if (!nzchar(r1$key)) numeric(p) else b[, r1$extra$path_index]
    if (length(gate)) {
      rows <- fail_fit_rows(rows, paste("fit gate failed:", paste(gate, collapse = ", ")))
      beta <- rep(NA_real_, p); converged <- FALSE
    }

    diagnostics <- list(
      path = data.frame(lambda = lam_orig, key = keys, k = kpath, iter = fit$iter, kkt_max = kkt,
                        passes = passes, rec_err = rec_err, stringsAsFactors = FALSE),
      candidates = cand,
      convex_min = if (is.null(fit$convex.min)) NA_integer_ else as.integer(fit$convex.min),
      discarded_intercept = unname(fit$beta[1L, ]),
      n_lambda_requested = length(lam), n_lambda_returned = L,
      internal_scale = s, internal_gamma = fit$gamma, penalty = penalty,
      zmax = zmax, lambda_rel_err = lam_rel_err, total_iter = tot_iter,
      gate_failures = gate)
    list(rules = rows, pip = NULL, beta = beta, converged = converged,
         diagnostics = diagnostics, warnings = cap$warnings, messages = cap$messages)
  }
  out <- tryCatch(finish(), error = function(e) e)
  if (inherits(out, "error")) {
    msg <- conditionMessage(out)
    return(list(rules = fail_rows(mrow, extra, msg), pip = NULL, beta = rep(NA_real_, p),
                converged = FALSE, diagnostics = list(error = msg, zmax = zmax),
                warnings = cap$warnings, messages = cap$messages))
  }
  out
}
