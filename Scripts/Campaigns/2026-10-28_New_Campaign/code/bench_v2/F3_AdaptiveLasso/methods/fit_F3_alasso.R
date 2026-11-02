# Adaptive lasso with the F1 CV-min lasso as its first-stage estimator.
alasso_weights <- function(b, F3) {
  if (!identical(F3$gamma, 1) || any(!is.finite(b)) || any(b == 0))
    stop("invalid pilot coefficients or gamma")
  w <- abs(b)^(-F3$gamma)
  if (any(!is.finite(w)) || any(w <= 0)) stop("unrepresentable adaptive weights")
  r <- w / max(w)
  v <- length(w) * (r / sum(r))
  if (any(!is.finite(v)) || any(v <= 0) ||
      abs(sum(v) - length(w)) > 1e-10 * length(w))
    stop("unrepresentable normalised adaptive weights")
  list(w = w, v = v)
}

codes_string <- function(fired, settings) {
  vocab <- c(settings$DIAG_FLAG_CODES, settings$DIAG_INFO_CODES)
  if (length(setdiff(fired, vocab))) stop("code outside the closed vocabulary")
  paste(vocab[vocab %in% fired], collapse = ";")
}

# Exact scalar path, with the Gram denominator recomputed for each training fold.
scalar_cv_engine <- function(X, y, foldid, lam, v) {
  n <- nrow(X); K <- max(foldid); L <- length(lam)
  solve_path <- function(xx, yy) {
    z <- sum(xx * yy) / length(yy)
    gram <- sum(xx * xx) / length(yy)
    if (!is.finite(gram) || gram <= 0) stop("nonpositive scalar Gram denominator")
    B <- matrix(sign(z) * pmax(abs(z) - lam * v, 0) / gram, nrow = 1L)
    scale <- max(1, abs(z))
    list(B = B, s = sqrt(mean(yy^2)), jerr = 0L, npasses = NA_real_,
         kkt = kkt_glmnet(matrix(xx, ncol = 1L), yy, B, lam, 1, v, scale))
  }
  full <- solve_path(X[, 1L], y)
  oof <- matrix(NA_real_, n, L); kkt_fold <- matrix(NA_real_, K, L)
  fold_diag <- vector("list", K)
  for (k in seq_len(K)) {
    te <- foldid == k
    fk <- solve_path(X[!te, 1L], y[!te])
    oof[te, ] <- X[te, , drop = FALSE] %*% fk$B
    kkt_fold[k, ] <- fk$kkt
    fold_diag[[k]] <- fk[c("s", "jerr", "npasses")]
  }
  nk <- tabulate(foldid, K)
  mse <- t(vapply(seq_len(K), function(k)
    colMeans((y[foldid == k] - oof[foldid == k, , drop = FALSE])^2), numeric(L)))
  cvm <- drop(nk %*% mse) / n
  cvsd <- sqrt(drop(nk %*% sweep(mse, 2, cvm)^2) / n / (K - 1))
  if (any(!is.finite(cvm)) || any(!is.finite(cvsd)) || any(!is.finite(kkt_fold)))
    stop("non-finite scalar CV result")
  list(full = full, oof = oof, mse = mse, cvm = cvm, cvsd = cvsd,
       kkt_fold = kkt_fold, fold_diag = fold_diag)
}

fit_diagnostics <- function(cv) {
  data.frame(data = c("full", paste0("fold", seq_along(cv$fold_diag))),
    s = c(cv$full$s, vapply(cv$fold_diag, function(d) d$s, 0)),
    jerr = c(cv$full$jerr, vapply(cv$fold_diag, function(d) as.numeric(d$jerr), 0)),
    npasses = c(cv$full$npasses, vapply(cv$fold_diag, function(d) as.numeric(d$npasses), 0)),
    kkt_max = c(max(cv$full$kkt), apply(cv$kkt_fold, 1L, max)))
}

alasso_fit_body <- function(X, y, foldid, settings, meth) {
  C <- settings$COMMON; GR <- settings$GRID; G <- settings$GLMNET; P <- settings$F3
  n <- nrow(X); p <- ncol(X)
  if (!identical(P$pilot, "lasso_cv_min") || !identical(P$gamma, 1))
    stop("invalid adaptive lasso pilot configuration")
  if (n == 200L && (floor(n / log(n)) != P$K_size_bound || P$K_size_bound != 37L))
    stop("K37 bound mismatch")

  zmax <- max(abs(crossprod(X, y))) / n
  if (!is.finite(zmax) || zmax <= 0) stop("invalid pilot zmax")
  lam1 <- GR$max_mult * zmax * lambda_fraction(GR)
  cv1 <- glmnet_cv_engine(X, y, foldid, alpha = 1, lam = lam1, pf = rep(1, p), G = G)
  ip <- cv_choose(cv1$cvm, cv1$cvsd)[["min"]]
  b <- unname(cv1$full$B[, ip])
  if (any(!is.finite(b)) || !is.finite(cv1$full$kkt[ip]) ||
      cv1$full$kkt[ip] > G$kkt_rel_tol ||
      any(!is.finite(cv1$kkt_fold[, ip])) || any(cv1$kkt_fold[, ip] > G$kkt_rel_tol))
    stop("lasso pilot failed selected-point KKT or finiteness check")
  keep <- which(b != 0); m <- length(keep)
  pilot <- list(lambda = lam1, index = ip, beta = b, cvm = cv1$cvm, cvsd = cv1$cvsd,
                kkt_full = cv1$full$kkt, kkt_fold_at_index = cv1$kkt_fold[, ip],
                fits = fit_diagnostics(cv1))
  gam <- C$ebic_gamma[c("ebic1", "ebic05")]
  extras <- list(pilot_k = m, pilot_index = ip, pilot_lambda = lam1[ip])

  if (m == 0L) {
    cand <- ebic_candidates(X, y, list(), C$kmax_ebic, gam, C$ols_tol)
    if (!cand$valid[1L]) stop("invalid null candidate")
    values <- setNames(lapply(meth$rule_ids[[1L]], function(id)
      c(list(status = "ok", support = "", k = 0L, converged = TRUE, diag_flag = FALSE,
             diag_codes = codes_string("pilot_null", settings), rss = sum(y^2),
             ebic1_value = cand$ebic1[1L],
             crit_value = if (startsWith(id, "ebic1")) cand$ebic1[1L] else if (startsWith(id, "ebic05")) cand$ebic05[1L] else NA_real_,
             k_valid_max = if (startsWith(id, "ebic")) 0L else NA_integer_,
             k_path_max = if (startsWith(id, "ebic")) 0L else NA_integer_), extras)),
      meth$rule_ids[[1L]])
    rules <- make_rule_rows(meth, values)
    B <- matrix(0, p, 1L)
    diagnostics <- list(pilot = pilot, pilot_beta = b, keep = keep, w = numeric(), v = numeric(),
      path = data.frame(lambda = NA_real_, key = "", k = 0L, cvm = NA_real_,
                        cvsd = NA_real_, kkt_full = NA_real_, kkt_fold_max = NA_real_),
      candidates = cand, foldid = foldid, heldout = matrix(0, n, 2L))
    return(list(rules = rules, beta = rep(0, p), converged = TRUE,
                coefficients = coefficient_evidence(rules, B, X, y, C$ols_tol),
                diagnostics = diagnostics))
  }

  wt <- alasso_weights(b[keep], P)
  Xk <- X[, keep, drop = FALSE]
  z <- abs(drop(crossprod(Xk, y))) / n
  lam <- GR$max_mult * max(z / wt$v) * lambda_fraction(GR)
  if (length(lam) != GR$nlambda || any(!is.finite(lam)) || lam[1L] <= 0)
    stop("invalid weighted lambda grid")
  cv <- if (m == 1L) scalar_cv_engine(Xk, y, foldid, lam, wt$v) else
    glmnet_cv_engine(Xk, y, foldid, alpha = 1, lam = lam, pf = wt$v, G = G)
  idx <- cv_choose(cv$cvm, cv$cvsd); L <- length(lam)
  B <- matrix(0, p, L); B[keep, ] <- cv$full$B
  supports <- lapply(seq_len(L), function(j) which(B[, j] != 0))
  keys <- vapply(supports, support_key, ""); kpath <- lengths(supports)
  full_ok <- cv$full$kkt <= G$kkt_rel_tol; fold_ok <- cv$kkt_fold <= G$kkt_rel_tol
  diag_flag <- any(!full_ok) || any(!fold_ok)
  converged <- all(c(cv$full$jerr, vapply(cv$fold_diag, function(d) as.numeric(d$jerr), 0)) == 0)
  cand <- ebic_candidates(X, y, supports, C$kmax_ebic, gam, C$ols_tol)
  k_path_max <- max(kpath)
  fit_codes <- c(if (diag_flag) "kkt_path", if (m == 1L) "pilot_single")
  rule_values <- function(key, failed, reason, fields, codes) {
    c(list(status = if (failed) "failed" else "ok",
           support = if (failed) NA_character_ else key,
           support_audit = if (failed) key else NA_character_,
           k = if (failed) NA_integer_ else length(parse_key(key)),
           converged = converged, diag_flag = diag_flag,
           diag_codes = codes_string(c(fit_codes, codes), settings),
           error = if (failed) reason else NA_character_), fields, extras)
  }
  cv_rule <- function(i, bad) {
    key <- keys[i]
    own <- ebic_candidates(X, y, list(supports[[i]]), Inf, gam["ebic1"], C$ols_tol)
    own <- own[match(key, own$key), ]
    rule_values(key, bad, "KKT violation at selected CV point",
      list(lambda = lam[i], cv_mean = cv$cvm[i], cv_se = cv$cvsd[i], rss = own$rss,
           ebic1_value = own$ebic1, index = i),
      c(if (i == 1L) "lambda_first", if (i == L) "lambda_last"))
  }
  imin <- idx[["min"]]; i1se <- idx[["one_se"]]
  values <- list(cv_min = cv_rule(imin, !full_ok[imin] || any(!fold_ok[, imin])),
                 cv_1se = cv_rule(i1se, !full_ok[i1se] || any(!fold_ok[, i1se]) || any(!fold_ok[, imin])))
  for (rid in c("ebic1", "ebic05", "ebic1_K37", "ebic05_K37")) {
    col <- sub("_K37$", "", rid)
    eligible <- if (endsWith(rid, "_K37")) cand[cand$k <= floor(n/log(n)), , drop = FALSE] else cand
    j <- ebic_pick(eligible, col); key <- eligible$key[j]
    occ <- which(keys == key); occ_ok <- occ[full_ok[occ]]
    i <- if (length(occ_ok)) occ_ok[1L] else if (length(occ)) occ[1L] else NA_integer_
    valid_max <- max(eligible$k[eligible$valid])
    values[[rid]] <- rule_values(key, !occurrence_ok(key, keys, full_ok),
      "no KKT-passing path occurrence of the chosen support",
      list(lambda = if (is.na(i)) NA_real_ else lam[i], rss = eligible$rss[j],
           ebic1_value = eligible$ebic1[j], crit_value = eligible[[col]][j], index = i,
           k_valid_max = valid_max, k_path_max = k_path_max),
      if (eligible$k[j] == valid_max) "ebic_at_largest")
  }
  rules <- make_rule_rows(meth, values)
  diagnostics <- list(pilot = pilot, pilot_beta = b, keep = keep, w = wt$w, v = wt$v,
    path = data.frame(lambda = lam, key = keys, k = kpath, cvm = cv$cvm, cvsd = cv$cvsd,
                      kkt_full = cv$full$kkt, kkt_fold_max = apply(cv$kkt_fold, 2L, max)),
    fold_mse = cv$mse, fits = fit_diagnostics(cv), candidates = cand,
    heldout = cbind(cv_min = cv$oof[, imin], cv_1se = cv$oof[, i1se]),
    foldid = foldid, zmax = max(z), lambda_entry = max(z / wt$v), index = idx)
  list(rules = rules, beta = unname(B[, imin]), converged = converged,
       coefficients = coefficient_evidence(rules, B, X, y, C$ols_tol), diagnostics = diagnostics)
}

fit_F3_alasso <- function(X, y, foldid, seed, settings) {
  meth <- settings$METHODS[settings$METHODS$method_id == "F3", , drop = FALSE]
  if (nrow(meth) != 1L) stop("F3 is not registered")
  if (!identical(settings$variant, meth$variant)) stop("unknown F3 variant")
  assert_inputs(X, y, foldid, settings$COMMON)
  assert_pkg_version("glmnet", settings$GLMNET$pkg_version)
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(seed)
  cap <- with_captured_conditions(alasso_fit_body(X, y, as.integer(foldid), settings, meth))
  if (!is.na(cap$error)) {
    rules <- fail_rows(meth, cap$error)
    return(list(rules = rules, coefficients = coefficient_evidence(rules, NULL, X, y, settings$COMMON$ols_tol),
                pip = NULL, beta = rep(NA_real_, ncol(X)), converged = FALSE,
                diagnostics = list(error = cap$error), warnings = cap$warnings, messages = cap$messages))
  }
  fit <- cap$value
  if (length(cap$warnings) + length(cap$messages) > 0L)
    fit$rules$status[fit$rules$status == "ok"] <- "warning"
  for (i in seq_along(fit$coefficients)) fit$coefficients[[i]]$status <- fit$rules$status[i]
  list(rules = fit$rules, coefficients = fit$coefficients, pip = NULL, beta = fit$beta,
       converged = fit$converged, diagnostics = fit$diagnostics, warnings = cap$warnings, messages = cap$messages)
}
