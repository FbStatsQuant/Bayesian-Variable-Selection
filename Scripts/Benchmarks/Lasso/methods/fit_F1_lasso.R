# fit_F1_lasso.R -- benchmark F1, the lasso (master §III.3.1, items e-h).
# Objective RSS/(2n) + λ‖β‖₁ on the supplied X, no intercept, no standardisation; λ on the fraction
# grid 1.01 · zmax · frac; 10-fold CV on the common folds by the shared glmnet engine.
# Rules (§III.3.1 f): cv_min (primary), cv_1se, ebic1, ebic05 (S0).
# Receives only (X, y, foldid, seed, settings); requires common.R and glmnet_helpers.R in scope.

fit_F1_lasso <- function(X, y, foldid, seed, settings) {
  cap <- with_captured_conditions(f1_lasso_core(X, y, foldid, seed, settings))
  p <- ncol(X)
  if (!is.na(cap$error)) {
    rules <- fail_rows(settings$METHODS, "F1")
    return(list(rules = rules, pip = NULL, beta = rep(NA_real_, p), converged = FALSE,
                diagnostics = list(), warnings = cap$warnings, messages = cap$messages,
                error = cap$error))
  }
  out <- cap$value
  # §III.3.0 "Status": any captured warning or message turns ok rows into warning rows;
  # failure takes precedence; a captured condition never changes a selection or a flag.
  if (length(cap$warnings) + length(cap$messages) > 0L)
    out$rules$status[out$rules$status == "ok"] <- "warning"
  out$warnings <- cap$warnings; out$messages <- cap$messages; out$error <- NA_character_
  out
}

f1_lasso_core <- function(X, y, foldid, seed, settings) {
  COMMON <- settings$COMMON; GRID <- settings$GRID; GLMNET <- settings$GLMNET; F1 <- settings$F1
  # e1-e2: inputs, package version, seed (F1 draws no random numbers after this)
  assert_inputs(X, y, foldid, COMMON)
  assert_pkg_version("glmnet", GLMNET$pkg_version)
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(seed)
  n <- nrow(X); p <- ncol(X)

  # e3: grid. zmax = max_j |X_j'y| / n is the smallest λ giving the null lasso on the full data.
  zmax <- max(abs(crossprod(X, y))) / n
  if (!is.finite(zmax) || zmax <= 0) stop("invalid zmax")
  lam <- GRID$max_mult * zmax * lambda_fraction(GRID)
  if (length(lam) != GRID$nlambda) stop("lambda grid does not have GRID$nlambda points")
  L <- length(lam)

  # e4: full-data fit + 10 training-fold fits, all checked (pf = 1: glmnet leaves it unchanged)
  cv <- glmnet_cv_engine(X, y, foldid, alpha = F1$alpha, lam = lam, pf = rep(1, p), G = GLMNET)
  B <- cv$full$B

  # e6: CV choices (glmnet's own rule)
  ch <- cv_choose(cv$cvm, cv$cvsd)
  i_min <- ch[["min"]]; i_1se <- ch[["one_se"]]

  # e7: full-data supports along the path
  supports  <- lapply(seq_len(L), function(j) which(abs(B[, j]) > COMMON$support_zero_tol))
  path_keys <- vapply(supports, support_key, "")
  path_k    <- lengths(supports)

  # KKT checks (§III.3.1 f, h): per grid point, full-data fit and each fold fit
  tol <- GLMNET$kkt_rel_tol
  ok_full <- cv$full$kkt <= tol                     # length L
  ok_fold <- cv$kkt_fold <= tol                     # K x L
  flag_codes <- if (!all(ok_full) || !all(ok_fold)) "kkt_path" else character()

  # EBIC candidates once: null + distinct full-data path supports with k <= kmax_ebic
  gammas <- COMMON$ebic_gamma[c("ebic1", "ebic05")]
  cand <- ebic_candidates(X, y, supports, COMMON$kmax_ebic, gammas, COMMON$ols_tol)
  k_path_max <- max(path_k)

  # OLS RSS and EBIC(1) of a support, uncapped (diagnostics on the CV rows; they never select)
  support_scores <- function(idx) {
    f <- ols_rss(X, y, idx, COMMON$ols_tol)
    k <- length(idx)
    e1 <- if (f$rank == k && is.finite(f$rss) && f$rss > 0)
      ebic_value(f$rss, k, n, p, COMMON$ebic_gamma[["ebic1"]]) else Inf
    list(rss = f$rss, ebic1 = e1)
  }

  cv_rule <- function(i, rule_ok) {
    sc <- support_scores(supports[[i]])
    list(status = if (rule_ok) "ok" else "failed", support = path_keys[i],
         codes = c(if (i == 1L) "lambda_first", if (i == L) "lambda_last"),
         extras = list(lambda = lam[i], cv_mean = cv$cvm[i], cv_se = cv$cvsd[i],
                       rss = sc$rss, ebic1_value = sc$ebic1, index = i))
  }
  # cv_min fails on a KKT violation at i_min in the full fit or any fold fit; cv_1se also at
  # i_min in any fold fit, because its threshold cvm[i_min] + cvsd[i_min] comes from those fits.
  ok_min <- ok_full[i_min] && all(ok_fold[, i_min])
  ok_1se <- ok_full[i_1se] && all(ok_fold[, i_1se]) && all(ok_fold[, i_min])

  ebic_rule <- function(column) {
    pk <- ebic_pick(cand, column)
    # the null support is always valid; otherwise some full-data occurrence must pass KKT
    rule_ok <- pk$key == "" || occurrence_ok(pk$key, path_keys, ok_full)
    occ <- which(path_keys == pk$key & ok_full)
    if (!length(occ)) occ <- which(path_keys == pk$key)
    i <- if (length(occ)) occ[1L] else NA_integer_       # largest λ with that support
    sc <- cand[pk$row, ]
    list(status = if (rule_ok) "ok" else "failed", support = pk$key,
         codes = if (pk$at_largest) "ebic_at_largest",
         extras = list(lambda = if (is.na(i)) NA_real_ else lam[i], rss = sc$rss,
                       ebic1_value = sc$ebic1, crit_value = pk$value, index = i,
                       k_valid_max = pk$k_valid_max, k_path_max = k_path_max))
  }

  values <- list(cv_min = cv_rule(i_min, ok_min), cv_1se = cv_rule(i_1se, ok_1se),
                 ebic1 = ebic_rule("ebic1"), ebic05 = ebic_rule("ebic05"))
  # converged: jerr == 0 in every glmnet fit (a nonzero jerr already stopped the fit)
  jerrs <- as.integer(c(cv$full$jerr, vapply(cv$fold_diag, function(d) as.numeric(d$jerr), 0)))
  converged <- all(jerrs == 0L)
  rules <- make_rule_rows(settings$METHODS, "F1", values, converged, flag_codes, COMMON)

  npasses <- c(cv$full$npasses, vapply(cv$fold_diag, function(d) as.numeric(d$npasses), 0))
  diagnostics <- list(
    path = data.frame(lambda = lam, key = path_keys, k = path_k, cvm = cv$cvm, cvsd = cv$cvsd,
                      kkt_full = cv$full$kkt, kkt_fold_max = apply(cv$kkt_fold, 2, max),
                      stringsAsFactors = FALSE),
    fold_mse = cv$mse,
    fits = data.frame(data = c("full", paste0("fold", seq_len(nrow(cv$kkt_fold)))),
                      jerr = jerrs, npasses = npasses,
                      kkt_max = c(max(cv$full$kkt), apply(cv$kkt_fold, 1, max)),
                      stringsAsFactors = FALSE),
    candidates = cand,
    heldout = cbind(i_min = cv$oof[, i_min], i_1se = cv$oof[, i_1se]),
    foldid = foldid, zmax = zmax, index = c(min = i_min, one_se = i_1se))

  list(rules = rules, pip = NULL, beta = unname(B[, i_min]), converged = converged,
       diagnostics = diagnostics)
}
