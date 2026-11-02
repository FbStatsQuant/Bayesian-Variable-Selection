# fit_F3_alasso.R: benchmark F3, adaptive lasso (Zou 2006, gamma = 1) with a CV ridge pilot.
# Implements master §III.3.3 (items a-k) under the common rules of §III.3.0.
# Uses common.R (assertions, supports, EBIC scorer, rule rows, condition capture) and
# methods/glmnet_helpers.R (glmnet_cv_engine, cv_choose). Sourcing computes nothing.
#
# Objective (§III.3.3 a, c): minimise RSS/(2n) + lambda * sum_j v_j |beta_j|, no intercept,
# with v = p w / sum(w), w_j = 1 / max(|b_j|, eps)^gamma, b = ridge pilot at kappa_min.

# ---- ridge pilot (§III.3.3 c) ----

# b(kappa) minimises ||y - X b||^2 / (2n) + kappa ||b||^2 / 2, i.e. (X'X + n kappa I) b = X'y.
# With the thin SVD X = U D V': b(kappa) = V diag(d / (d^2 + n kappa)) U'y.
# Replaces solve(crossprod(X) + n * kappa * diag(p), crossprod(X, y)): it needs no p x p
# matrix and gives every kappa from one decomposition. Returns the p x length(kappa) matrix.
ridge_path_svd <- function(X, y, kappa) {
  n <- nrow(X)
  sv <- svd(X)                                    # min(n, p) singular values
  uty <- drop(crossprod(sv$u, y))                 # U'y
  shrink <- sv$d / outer(sv$d^2, n * kappa, "+")  # [i, j] = d_i / (d_i^2 + n kappa_j)
  sv$v %*% (shrink * uty)                         # uty recycles down each column
}

# Relative residual of the normal equations (X'X/n + kappa I) b = X'y/n for each kappa,
# max_j |residual_j| / (1 + max_j |X_j'y/n|). X'X b is formed as X'(X b): no p x p matrix.
ridge_normal_residual <- function(X, y, B, kappa) {
  n <- nrow(X)
  xty <- drop(crossprod(X, y)) / n
  r <- crossprod(X, X %*% B) / n + sweep(B, 2L, kappa, "*") - xty
  apply(abs(r), 2L, max) / (1 + max(abs(xty)))
}

# 10-fold CV of the ridge path on the common folds, then the full-data path.
# cvm and cvsd use the same formulas as glmnet_cv_engine (fold-size-weighted mean of the
# fold MSEs; grouped SE). The kappa grid is decreasing, so the smallest index among exact
# minima is the larger kappa (tie rule "larger").
ridge_cv <- function(X, y, foldid, kappa) {
  n <- nrow(X); K <- max(foldid); J <- length(kappa)
  oof <- matrix(NA_real_, n, J)
  for (k in seq_len(K)) {
    te <- foldid == k
    Bk <- ridge_path_svd(X[!te, , drop = FALSE], y[!te], kappa)
    oof[te, ] <- X[te, , drop = FALSE] %*% Bk
  }
  if (any(!is.finite(oof))) stop("non-finite ridge out-of-fold prediction")
  nk  <- tabulate(foldid, K)
  mse <- t(vapply(seq_len(K), function(k)
           colMeans((y[foldid == k] - oof[foldid == k, , drop = FALSE])^2), numeric(J)))
  cvm  <- drop(nk %*% mse) / n
  cvsd <- sqrt(drop(nk %*% sweep(mse, 2, cvm)^2) / n / (K - 1))
  if (any(!is.finite(cvm)) || any(!is.finite(cvsd))) stop("non-finite ridge CV summary")
  i_min <- min(which(cvm <= min(cvm)))
  B <- ridge_path_svd(X, y, kappa)
  if (any(!is.finite(B))) stop("non-finite full-data ridge coefficients")
  list(B = B, cvm = cvm, cvsd = cvsd, mse = mse, i_min = i_min, kappa_min = kappa[i_min],
       resid = ridge_normal_residual(X, y, B, kappa))
}

# ---- adaptive weights (§III.3.3 c) ----

# w_j = 1 / max(|b_j|, eps)^gamma with eps = max(floor_abs, floor_rel * max|b|).
# glmnet rescales penalty factors to sum to p; passing v = p w / sum(w) makes that a no-op,
# so the objective is exactly RSS/(2n) + lambda sum v_j |beta_j|.
alasso_weights <- function(b, F3) {
  eps <- max(F3$floor_abs, F3$floor_rel * max(abs(b)))
  w <- pmax(abs(b), eps)^(-F3$gamma)
  v <- length(b) * w / sum(w)
  if (any(!is.finite(v)) || any(v <= 0)) stop("non-finite or non-positive penalty factors")
  list(w = w, v = v, eps = eps, floored = abs(b) < eps, n_floored = sum(abs(b) < eps))
}

# ---- codes ----

# Joins the codes that fired, flag codes first, in vocabulary order.
codes_string <- function(fired, settings) {
  vocab <- c(settings$DIAG_FLAG_CODES, settings$DIAG_INFO_CODES)
  if (length(setdiff(fired, vocab))) stop("code outside the closed vocabulary")
  paste(vocab[vocab %in% fired], collapse = ";")
}

# ---- fit body (§III.3.3 e, f) ----

alasso_fit_body <- function(X, y, foldid, settings, meth) {
  C <- settings$COMMON; GR <- settings$GRID; G <- settings$GLMNET; P <- settings$F3
  n <- nrow(X); p <- ncol(X)
  if (any(diff(P$kappa) >= 0) || !identical(P$kappa_ties, "larger"))
    stop("F3$kappa must be strictly decreasing with ties to the larger kappa")

  # Step 2: ridge pilot, kappa by CV on the common folds; normal-equation check.
  ridge <- ridge_cv(X, y, foldid, P$kappa)
  if (max(ridge$resid) > P$ridge_tol)
    stop("ridge normal-equation check failed: max relative residual ", signif(max(ridge$resid), 3))
  kappa_edge <- ridge$i_min %in% c(1L, length(P$kappa))

  # Step 3: weights.
  b <- ridge$B[, ridge$i_min]
  wt <- alasso_weights(b, P)

  # Step 4: weighted lambda grid (entry value max_j |X_j'y| / (n v_j)) and the CV engine.
  z <- abs(drop(crossprod(X, y))) / n
  lam <- GR$max_mult * max(z / wt$v) * lambda_fraction(GR)
  if (length(lam) != GR$nlambda || any(!is.finite(lam)) || lam[1L] <= 0)
    stop("invalid weighted lambda grid")
  cv <- glmnet_cv_engine(X, y, foldid, alpha = 1, lam = lam, pf = wt$v, G = G)
  idx <- cv_choose(cv$cvm, cv$cvsd)
  L <- length(lam)

  # Full-data path supports and KKT status of every point.
  B <- cv$full$B
  supports <- lapply(seq_len(L), function(j) which(abs(B[, j]) > C$support_zero_tol))
  keys <- vapply(supports, support_key, "")
  kpath <- lengths(supports)
  full_ok <- cv$full$kkt <= G$kkt_rel_tol
  fold_ok <- cv$kkt_fold <= G$kkt_rel_tol                 # K x L
  diag_flag <- any(!full_ok) || any(!fold_ok)
  jerr_all <- c(cv$full$jerr, vapply(cv$fold_diag, function(d) as.numeric(d$jerr), 0))
  converged <- all(jerr_all == 0)

  # EBIC candidates once: distinct path supports with k <= 100 plus the null model.
  gam <- C$ebic_gamma[c("ebic1", "ebic05")]
  cand <- ebic_candidates(X, y, supports, C$kmax_ebic, gam, C$ols_tol)
  k_valid_max <- max(cand$k[cand$valid])
  k_path_max <- max(kpath)

  fit_codes <- c(if (diag_flag) "kkt_path", if (kappa_edge) "kappa_edge")

  floored_hit <- function(key) {
    s <- parse_key(key)
    length(s) > 0L && any(wt$floored[s])
  }
  rule_values <- function(key, failed, reason, fields, codes) {
    c(list(status = if (failed) "failed" else NA_character_,
           support = if (failed) NA_character_ else key,
           support_audit = if (failed) key else NA_character_,
           k = if (failed) NA_integer_ else length(parse_key(key)),
           converged = converged, diag_flag = diag_flag,
           diag_codes = codes_string(c(fit_codes, codes, if (floored_hit(key)) "floored_selected"),
                                     settings),
           error = if (failed) reason else NA_character_),
      fields)
  }

  # CV rules (§III.3.3 f, failure rules as F1 f).
  cv_rule <- function(i, bad, reason) {
    key <- keys[i]
    own <- ebic_candidates(X, y, list(supports[[i]]), Inf, gam["ebic1"], C$ols_tol)
    own <- own[match(key, own$key), ]
    rule_values(key, bad, reason,
                list(lambda = lam[i], cv_mean = cv$cvm[i], cv_se = cv$cvsd[i], rss = own$rss,
                     ebic1_value = own$ebic1, crit_value = NA_real_, index = i,
                     k_valid_max = NA_integer_, k_path_max = NA_integer_, kappa = ridge$kappa_min),
                c(if (i == 1L) "lambda_first", if (i == L) "lambda_last"))
  }
  i_min <- idx[["min"]]; i_1se <- idx[["one_se"]]
  bad_min <- !full_ok[i_min] || any(!fold_ok[, i_min])
  bad_1se <- !full_ok[i_1se] || any(!fold_ok[, i_1se]) || any(!fold_ok[, i_min])
  values <- list(
    cv_min = cv_rule(i_min, bad_min, "KKT violation at the cv_min index (full or fold fit)"),
    cv_1se = cv_rule(i_1se, bad_1se,
                     "KKT violation at the cv_1se index (full or fold fit) or at cv_min in a fold fit"))

  # EBIC rules: fail if no KKT-passing full-data path occurrence of the chosen support.
  for (rid in c("ebic1", "ebic05")) {
    j <- ebic_pick(cand, rid)
    key <- cand$key[j]
    occ <- which(keys == key)
    occ_ok <- occ[full_ok[occ]]
    i <- if (length(occ_ok)) occ_ok[1L] else if (length(occ)) occ[1L] else NA_integer_
    bad <- !occurrence_ok(key, keys, full_ok)
    values[[rid]] <- rule_values(key, bad, "no KKT-passing path occurrence of the chosen support",
      list(lambda = if (is.na(i)) NA_real_ else lam[i], cv_mean = NA_real_, cv_se = NA_real_,
           rss = cand$rss[j], ebic1_value = cand$ebic1[j], crit_value = cand[[rid]][j],
           index = i, k_valid_max = k_valid_max, k_path_max = k_path_max,
           kappa = ridge$kappa_min),
      if (cand$k[j] == k_valid_max) "ebic_at_largest")
  }
  rules <- make_rule_rows(meth, values)

  fits <- data.frame(
    data = c("full", paste0("fold", seq_along(cv$fold_diag))),
    s = c(cv$full$s, vapply(cv$fold_diag, `[[`, 0, "s")),
    jerr = jerr_all,
    npasses = c(cv$full$npasses, vapply(cv$fold_diag, function(d) as.numeric(d$npasses), 0)),
    kkt_max = c(max(cv$full$kkt), apply(cv$kkt_fold, 1L, max)),
    stringsAsFactors = FALSE)
  diagnostics <- list(
    ridge = data.frame(kappa = P$kappa, cvm = ridge$cvm, cvsd = ridge$cvsd,
                       normal_resid = ridge$resid),
    kappa_min = ridge$kappa_min, kappa_index = ridge$i_min, kappa_boundary = kappa_edge,
    ridge_resid_max = max(ridge$resid), ridge_fold_mse = ridge$mse,
    b = b, w = wt$w, v = wt$v, eps_floor = wt$eps, n_floored = wt$n_floored,
    path = data.frame(lambda = lam, key = keys, k = kpath, cvm = cv$cvm, cvsd = cv$cvsd,
                      kkt_full = cv$full$kkt, kkt_fold_max = apply(cv$kkt_fold, 2L, max),
                      stringsAsFactors = FALSE),
    fold_mse = cv$mse, fits = fits, candidates = cand,
    heldout = cbind(cv_min = cv$oof[, i_min], cv_1se = cv$oof[, i_1se]),
    foldid = foldid, zmax = max(z), lambda_entry = max(z / wt$v), index = idx)
  list(rules = rules, beta = B[, i_min], converged = converged, diagnostics = diagnostics)
}

# ---- wrapper (§III.3.0 interface) ----

fit_F3_alasso <- function(X, y, foldid, seed, settings) {
  meth <- settings$METHODS[settings$METHODS$method_id == "F3", , drop = FALSE]
  if (nrow(meth) != 1L) stop("F3 is not registered in settings$METHODS")
  if (!identical(settings$variant, meth$variant)) stop("unknown F3 variant: ", settings$variant)
  assert_inputs(X, y, foldid, settings$COMMON)
  assert_pkg_version("glmnet", settings$GLMNET$pkg_version)
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(seed)   # F3 draws no numbers
  p <- ncol(X)
  cap <- with_captured_conditions(alasso_fit_body(X, y, as.integer(foldid), settings, meth))
  if (!is.na(cap$error))
    return(list(rules = fail_rows(meth, cap$error), pip = NULL, beta = rep(NA_real_, p),
                converged = FALSE, diagnostics = list(error = cap$error),
                warnings = cap$warnings, messages = cap$messages))
  fit <- cap$value
  rules <- fit$rules
  noisy <- length(cap$warnings) + length(cap$messages) > 0L
  rules$status[is.na(rules$status)] <- if (noisy) "warning" else "ok"
  list(rules = rules, pip = NULL, beta = fit$beta, converged = fit$converged,
       diagnostics = fit$diagnostics, warnings = cap$warnings, messages = cap$messages)
}
