# fit_F5_abess.R: benchmark F5 Best subset (ABESS + external EBIC), Regime H.
# Implements master §III.3.5 a-h (MASTER_Methodology_and_Plan.md, 2026-10-19), with the
# common rules of §III.3.0. Ported from Oct-14 scripts/methods.R::bench_abess; differences:
# sizes and every constant read from settings$F5, three EBIC rules (gamma 1, 0.5, 0),
# consistency failures turned into registered failed rows with support_audit, rule frame.
# Uses from common.R: assert_inputs, assert_pkg_version, support_key, ols_rss,
# ebic_candidates, ebic_pick, make_rule_rows, fail_rows, with_captured_conditions.
# Receives only (X, y, foldid, seed, settings); no oracle information (§III.3.9).

# Mandatory consistency checks of §III.3.5 e step 3. Never stops: returns the list of
# failed checks (empty when all pass) and the path table, so that a failed fit keeps its
# supports for audit (§III.3.0 "Failures").
abess_consistency <- function(fit, X, y, yc, F5, ols_tol) {
  n <- nrow(X); p <- ncol(X); S <- as.integer(F5$sizes); ybar <- mean(y)
  b <- tryCatch(unname(as.matrix(fit$beta)), error = function(e) NULL)
  if (is.null(b) || !identical(dim(b), c(p, length(S))))
    return(list(failures = "dim(beta) != c(p, length(sizes))", b = NULL, supports = NULL, path = NULL))
  if (any(!is.finite(b)))
    return(list(failures = "non-finite coefficients", b = NULL, supports = NULL, path = NULL))
  supports <- lapply(seq_len(ncol(b)), function(j) which(b[, j] != 0))   # SUPPORT_ZERO_TOL = 0
  fail <- character()
  if (!identical(as.integer(fit$support.size), S)) fail <- c(fail, "support.size != requested sizes")
  if (!identical(lengths(supports), S)) fail <- c(fail, "support of column k does not have k elements")
  intercept <- as.numeric(fit$intercept); dev <- as.numeric(fit$dev)
  if (length(intercept) != length(S) || any(!is.finite(intercept)) ||
      any(abs(intercept) > F5$intercept_tol)) fail <- c(fail, "intercept not zero")
  if (length(dev) != length(S) || any(!is.finite(dev))) {
    fail <- c(fail, "package dev missing or non-finite"); dev <- rep(NA_real_, length(S))
  }
  # RSS on the original y; package dev is the training loss on yc, RSS_c / (2n), and
  # RSS(y) = RSS(yc) + n ybar^2 because 1'X = 0 (§III.3.5 c).
  rss_rec <- colSums((y - X %*% b)^2)
  rss_cen <- colSums((yc - X %*% b)^2)
  rss_ols <- vapply(supports, function(s) ols_rss(X, y, s, ols_tol)$rss, 0.0)
  # Relative tolerance with a floor of 1, as Oct-14 bench_abess.
  close <- function(a, c) is.finite(a) & is.finite(c) & abs(a - c) <= F5$rss_rel_tol * pmax(1, abs(a), abs(c))
  if (!all(close(rss_rec, rss_ols))) fail <- c(fail, "reconstructed RSS != OLS RSS of the support")
  if (!all(close(rss_rec, 2 * n * dev + n * ybar^2))) fail <- c(fail, "reconstructed RSS != 2n dev + n ybar^2")
  # Active-set stationarity: max_j in S |X_j'(y - X b_k)| / n <= stat_rel_tol * max(1, zmax).
  zmax <- max(abs(crossprod(X, y))) / n
  G <- crossprod(X, y - X %*% b) / n
  stat <- vapply(seq_along(S), function(j)
    if (!length(supports[[j]])) 0 else max(abs(G[supports[[j]], j])), 0.0)
  stat_tol <- F5$stat_rel_tol * max(1, zmax)
  if (any(!is.finite(stat)) || any(stat > stat_tol)) fail <- c(fail, "active-set stationarity above tolerance")
  path <- data.frame(size = S, key = vapply(supports, support_key, ""), k = lengths(supports),
                     dev = dev, rss_reconstructed = rss_rec, rss_ols = rss_ols,
                     rss_centred = rss_cen, stationarity = stat,
                     intercept = if (length(intercept) == length(S)) intercept else NA_real_,
                     stringsAsFactors = FALSE)
  list(failures = fail, b = b, supports = supports, path = path,
       zmax = zmax, stat_tol = stat_tol)
}

# EBIC/BIC rules of §III.3.5 f over the path supports. Rule ids equal the gamma names.
abess_rules <- function(X, y, supports, COMMON, rule_ids) {
  cand <- ebic_candidates(X, y, supports, COMMON$kmax_ebic, COMMON$ebic_gamma, COMMON$ols_tol)
  picks <- lapply(rule_ids, function(id) ebic_pick(cand, id)); names(picks) <- rule_ids
  list(candidates = cand, picks = picks)
}

fit_F5_abess <- function(X, y, foldid, seed, settings) {
  F5 <- settings$F5; COMMON <- settings$COMMON
  rule_ids <- method_row(settings, "F5")$rule_ids[[1L]]
  # 1. Assertions and seed as F1 (§III.3.5 e step 1). foldid is checked and unused.
  assert_inputs(X, y, foldid, COMMON)
  assert_pkg_version("abess", F5$pkg_version)
  if (!("screening_num" %in% names(F5) && is.null(F5$screening_num)))
    stop("F5$screening_num must be a named NULL (0.4.11 screening bug, §III.3.5 c)")
  S <- as.integer(F5$sizes)
  if (!identical(S, 0:max(S)) || max(S) > COMMON$kmax_ebic || max(S) >= nrow(X) || max(S) > ncol(X))
    stop("F5$sizes must be 0:K with K <= kmax_ebic, K < n and K <= p")
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(seed)
  n <- nrow(X); p <- ncol(X)
  ybar <- mean(y); yc <- y - ybar          # centred response; external EBIC uses y

  cap <- with_captured_conditions({
    # 2. The package call (Oct-14 bench_abess; arguments §III.3.5 d). screening.num = NULL
    #    disables screening in R and C++; important.search = p splices over all variables.
    fit <- abess::abess(X, yc, family = "gaussian", tune.path = F5$tune_path,
                        tune.type = F5$tune_type, normalize = F5$normalize,
                        fit.intercept = F5$fit_intercept, support.size = S, lambda = F5$lambda,
                        screening.num = F5$screening_num, important.search = ncol(X),
                        warm.start = F5$warm_start, early.stop = F5$early_stop,
                        c.max = F5$c_max, max.splicing.iter = F5$max_splicing_iter,
                        splicing.type = F5$splicing_type, num.threads = F5$threads,
                        seed = F5$seed)
    # 3. Consistency checks; 4. EBIC candidates and rules (computed also when a check
    #    failed, for support_audit, as long as the path is well formed).
    chk <- abess_consistency(fit, X, y, yc, F5, COMMON$ols_tol)
    rl <- if (is.null(chk$supports)) NULL else abess_rules(X, y, chk$supports, COMMON, rule_ids)
    list(fit = fit, chk = chk, rl = rl)
  })

  diag <- list(response_center = ybar, sizes = S)
  if (!is.na(cap$error)) {                                     # R error in the fit
    return(list(rules = fail_rows(settings, "F5", converged = NA, diag_flag = FALSE),
                pip = NULL, beta = rep(NA_real_, p), converged = NA, diagnostics = diag,
                warnings = cap$warnings, messages = cap$messages, error = cap$error))
  }
  fit <- cap$value$fit; chk <- cap$value$chk; rl <- cap$value$rl
  diag <- c(diag, list(path = chk$path, candidates = rl$candidates,
                       coefficients = if (is.null(chk$b)) NULL else
                         lapply(seq_along(chk$supports), function(j) chk$b[chk$supports[[j]], j]),
                       best_size_internal = fit$best.size, tune_value_internal = fit$tune.value,
                       zmax = chk$zmax, stat_tol = chk$stat_tol,
                       consistency_failures = chk$failures))
  if (length(chk$failures)) {                                  # fit-level gate failed
    audit <- if (is.null(rl)) NULL else lapply(rl$picks, `[[`, "key")
    return(list(rules = fail_rows(settings, "F5", converged = NA, diag_flag = FALSE, support_audit = audit),
                pip = NULL, beta = rep(NA_real_, p), converged = NA, diagnostics = diag,
                warnings = cap$warnings, messages = cap$messages,
                error = paste("consistency check failed:", paste(chk$failures, collapse = "; "))))
  }
  status <- if (length(cap$warnings) || length(cap$messages)) "warning" else "ok"
  k_path_max <- max(lengths(chk$supports))
  fill <- lapply(rule_ids, function(id) {
    pk <- rl$picks[[id]]
    list(support = pk$key, k = pk$k, rss = pk$rss, crit_value = pk$crit,
         k_valid_max = pk$k_valid_max, k_path_max = k_path_max,
         diag_codes = paste(pk$codes, collapse = ";"))
  })
  names(fill) <- rule_ids
  # beta: the ABESS coefficients at the ebic1 support (the OLS slopes on that support).
  j1 <- match(rl$picks[["ebic1"]]$key, chk$path$key)
  list(rules = make_rule_rows(settings, "F5", fill, converged = NA, diag_flag = FALSE,
                              fit_status = status),
       pip = NULL, beta = chk$b[, j1], converged = NA, diagnostics = diag,
       warnings = cap$warnings, messages = cap$messages, error = NA_character_)
}
