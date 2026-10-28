# fit_F2_enet.R -- benchmark F2, elastic net (master §III.3.2 a-l; common rules §III.3.0).
# Target objective: RSS/(2n) + λ [α ||β||_1 + (1 - α) ||β||^2 / 2], no intercept, with
# (α, λ) tuned jointly by 10-fold CV on the common folds over α in F2$alphas.
# Uses common.R (assert_inputs, assert_pkg_version, lambda_fraction, support_key,
# ebic_candidates, ebic_pick, occurrence_ok, make_rule_rows, fail_rows,
# with_captured_conditions) and glmnet_helpers.R (glmnet_cv_engine, kkt_glmnet).
# Fitting code: receives only (X, y, foldid, seed, settings); never reads files.

# Extra rule-row columns (§III.3.2 g; `index` and `ebic1_value` added as in F1 g, see
# ASSUMPTIONS.md). diag_codes is part of the common rule frame.
F2_EXTRA_COLS <- c("alpha", "lambda", "index", "cv_mean", "cv_se", "rss", "ebic1_value",
                   "crit_value", "k_valid_max", "k_path_max")

# Tie rule (§III.3.2 f): minimum cvm over all (α, λ); exact ties -> largest α, then largest λ.
# cv_1se: at the chosen α only, the largest λ with cvm <= cvm_min + cvsd_min.
# Returns row numbers of cv_table.
enet_choose <- function(cv_table) {
  ties <- which(cv_table$cvm == min(cv_table$cvm))
  win <- ties[order(-cv_table$alpha[ties], -cv_table$lambda[ties])[1L]]
  same_alpha <- cv_table$alpha == cv_table$alpha[win]
  eligible <- which(same_alpha & cv_table$cvm <= cv_table$cvm[win] + cv_table$cvsd[win])
  one_se <- eligible[which.max(cv_table$lambda[eligible])]
  c(min = win, one_se = one_se)
}

fit_F2_enet <- function(X, y, foldid, seed, settings) {
  C <- settings$COMMON; G <- settings$GLMNET
  meth <- settings$METHODS[settings$METHODS$method_id == "F2", , drop = FALSE]
  if (nrow(meth) != 1L) stop("F2 is not registered in settings$METHODS")
  # Assertions and seed (§III.3.1 e steps 1-2). Errors here reach the runner's outer layer.
  assert_inputs(X, y, foldid, C)
  assert_pkg_version("glmnet", G$pkg_version)
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(seed)
  foldid <- as.integer(foldid)
  frac <- lambda_fraction(settings$GRID)
  stopifnot(length(frac) == settings$GRID$nlambda)

  # The package calls and our own fit-level gates run inside the capture layer.
  cap <- with_captured_conditions(enet_fit_core(X, y, foldid, frac, settings, meth))
  if (!is.na(cap$error)) {
    return(list(rules = fail_rows(meth, cap$error, F2_EXTRA_COLS),
                pip = NULL, beta = rep(NA_real_, ncol(X)), converged = FALSE,
                diagnostics = list(error = cap$error),
                warnings = cap$warnings, messages = cap$messages))
  }
  res <- cap$value
  # status: failed rules stay failed; otherwise warning if any condition was captured.
  if (length(cap$warnings) || length(cap$messages))
    res$rules$status[res$rules$status != "failed"] <- "warning"
  list(rules = res$rules, pip = NULL, beta = res$beta, converged = TRUE,
       diagnostics = res$diagnostics, warnings = cap$warnings, messages = cap$messages)
}

# §III.3.2 e steps 1-5 after the assertions.
enet_fit_core <- function(X, y, foldid, frac, settings, meth) {
  C <- settings$COMMON; G <- settings$GLMNET; GR <- settings$GRID
  alphas <- settings$F2$alphas
  n <- nrow(X); p <- ncol(X); L <- length(frac); K <- C$nfolds
  pf <- rep(1, p)

  # Step 1: entry value of the lasso on the full data.
  zmax <- max(abs(crossprod(X, y))) / n
  if (!is.finite(zmax) || zmax <= 0) stop("zmax is not finite and positive")

  # Step 2: one CV engine run per α on the target grid 1.01 zmax / α * frac
  # (λ α >= zmax gives the null model; the grid is fixed by the full data and shared by
  # the 10 folds).
  runs <- vector("list", length(alphas))
  for (j in seq_along(alphas)) {
    lam <- GR$max_mult * zmax / alphas[j] * frac
    cv <- glmnet_cv_engine(X, y, foldid, alphas[j], lam, pf, G)
    B <- cv$full$B
    supports <- lapply(seq_len(L), function(i) which(B[, i] != 0))   # SUPPORT_ZERO_TOL = 0
    runs[[j]] <- list(alpha = alphas[j], lam = lam, cv = cv, B = B, supports = supports,
                      keys = vapply(supports, support_key, ""), k = lengths(supports))
  }

  # Step 3: the stacked 1,000-row CV table.
  cv_table <- do.call(rbind, lapply(seq_along(runs), function(j) {
    r <- runs[[j]]
    data.frame(alpha_index = j, alpha = r$alpha, lambda_index = seq_len(L), lambda = r$lam,
               cvm = r$cv$cvm, cvsd = r$cv$cvsd, k = r$k)
  }))

  # Step 4: (α*, i*) by the tie rule; i_1se within α*.
  pick <- enet_choose(cv_table)
  ja <- cv_table$alpha_index[pick[["min"]]]
  i_min <- cv_table$lambda_index[pick[["min"]]]
  i_1se <- cv_table$lambda_index[pick[["one_se"]]]
  win <- runs[[ja]]
  for (j in seq_along(runs)) runs[[j]]$B <- NULL   # keep the coefficient matrix of α* only (e)

  # KKT status of all 55 fits (h). ok_full: length L; ok_fold: K x L (at α*).
  tol <- G$kkt_rel_tol
  any_violation <- any(vapply(runs, function(r)
    any(r$cv$full$kkt > tol) || any(r$cv$kkt_fold > tol), logical(1)))
  ok_full <- win$cv$full$kkt <= tol
  ok_fold <- win$cv$kkt_fold <= tol
  flag_codes <- if (any_violation) "kkt_path" else character()
  alpha_edge <- win$alpha %in% range(alphas)

  # EBIC candidates on α*'s full-data path (null + distinct supports with k <= 100).
  gammas <- C$ebic_gamma[c("ebic1", "ebic05")]
  cand <- ebic_candidates(X, y, win$supports, C$kmax_ebic, gammas, C$ols_tol)
  k_path_max <- max(win$k)

  codes <- function(...) paste(c(flag_codes, ...), collapse = ";")
  # EBIC(1) of any support, for the CV rows' diagnostic columns (Inf if rank-deficient).
  ebic1_of <- function(idx) {
    o <- ols_rss(X, y, idx, C$ols_tol); k <- length(idx)
    v <- if (o$rank == k && is.finite(o$rss) && o$rss > 0)
      n * log(o$rss / n) + k * log(n) + 2 * gammas[["ebic1"]] * lchoose(p, k) else Inf
    list(rss = o$rss, ebic1 = v)
  }

  # Rule f: cv_min and cv_1se.
  cv_row <- function(i, ok, why) {
    key <- win$keys[i]; o <- ebic1_of(win$supports[[i]])
    info <- c(if (alpha_edge) "alpha_edge", if (i == 1L) "lambda_first", if (i == L) "lambda_last")
    row <- list(converged = TRUE, diag_flag = any_violation, diag_codes = codes(info),
                alpha = win$alpha, lambda = win$lam[i], index = i,
                cv_mean = win$cv$cvm[i], cv_se = win$cv$cvsd[i], rss = o$rss,
                ebic1_value = o$ebic1, crit_value = win$cv$cvm[i])
    if (ok) c(row, list(status = "ok", support = key, support_audit = NA_character_,
                        k = win$k[i], error = NA_character_))
    else c(row, list(status = "failed", support = NA_character_, support_audit = key,
                     k = NA_integer_, error = why))
  }
  ok_min <- ok_full[i_min] && all(ok_fold[, i_min])
  ok_1se <- ok_full[i_1se] && all(ok_fold[, i_1se]) && all(ok_fold[, i_min])
  rows <- list(
    cv_min = cv_row(i_min, ok_min,
                    "KKT violation at the selected (alpha, lambda) in the full or a fold fit"),
    cv_1se = cv_row(i_1se, ok_1se,
                    "KKT violation at (alpha*, i_1se) in the full or a fold fit, or at (alpha*, i_min) in a fold fit"))

  # Rule f: ebic1 and ebic05 on α*'s full path.
  for (g in names(gammas)) {
    e <- ebic_pick(cand, g)
    occ <- which(win$keys == e$key)
    occ_ok <- occ[ok_full[occ]]
    i <- if (length(occ_ok)) occ_ok[1L] else if (length(occ)) occ[1L] else NA_integer_
    valid <- occurrence_ok(e$key, win$keys, ok_full)
    info <- c(if (alpha_edge) "alpha_edge", if (e$at_largest) "ebic_at_largest")
    row <- list(converged = TRUE, diag_flag = any_violation, diag_codes = codes(info),
                alpha = win$alpha, lambda = if (is.na(i)) NA_real_ else win$lam[i], index = i,
                cv_mean = NA_real_, cv_se = NA_real_, rss = e$rss,
                ebic1_value = cand$ebic1[e$row], crit_value = e$crit,
                k_valid_max = e$k_valid_max, k_path_max = k_path_max)
    rows[[g]] <- if (valid)
      c(row, list(status = "ok", support = e$key, support_audit = NA_character_,
                  k = e$k, error = NA_character_))
    else c(row, list(status = "failed", support = NA_character_, support_audit = e$key,
                     k = NA_integer_, error = "no full-data path occurrence of the EBIC support passes KKT"))
  }
  rules <- make_rule_rows(meth, rows, F2_EXTRA_COLS)

  # Diagnostics (§III.3.2 g).
  fit_rows <- do.call(rbind, lapply(runs, function(r) {
    fd <- r$cv$fold_diag
    data.frame(alpha = r$alpha, data = c("full", sprintf("fold%02d", seq_len(K))),
               s = c(r$cv$full$s, vapply(fd, `[[`, 0, "s")),
               m = c(r$cv$full$m, vapply(fd, `[[`, 0, "m")),
               native_a = c(r$cv$full$a, vapply(fd, `[[`, 0, "a")),
               jerr = c(r$cv$full$jerr, vapply(fd, function(z) as.integer(z$jerr), 0L)),
               npasses = c(r$cv$full$npasses, vapply(fd, function(z) as.integer(z$npasses), 0L)),
               max_kkt = c(max(r$cv$full$kkt), apply(r$cv$kkt_fold, 1L, max)))
  }))
  kkt <- do.call(rbind, lapply(runs, function(r) rbind(r$cv$full$kkt, r$cv$kkt_fold)))
  rownames(kkt) <- paste0("a", fit_rows$alpha, "_", fit_rows$data)
  fold_mse <- array(NA_real_, c(length(alphas), K, L),
                    dimnames = list(paste0("alpha_", alphas), NULL, NULL))
  for (j in seq_along(runs)) fold_mse[j, , ] <- runs[[j]]$cv$mse
  diagnostics <- list(
    cv_table = cv_table,
    paths = setNames(lapply(runs, `[[`, "keys"), paste0("alpha_", alphas)),
    fits = fit_rows, kkt = kkt, fold_mse = fold_mse, candidates = cand,
    heldout = cbind(cv_min = win$cv$oof[, i_min], cv_1se = win$cv$oof[, i_1se]),
    foldid = foldid, zmax = zmax,
    chosen = list(alpha = win$alpha, alpha_index = ja, i_min = i_min, i_1se = i_1se),
    kkt_violation_any = any_violation)
  list(rules = rules, beta = as.numeric(win$B[, i_min]), diagnostics = diagnostics)
}
