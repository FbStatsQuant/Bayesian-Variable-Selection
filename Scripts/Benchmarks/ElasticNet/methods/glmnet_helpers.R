# glmnet_helpers.R -- shared glmnet engine for F1, F2, F3 (copy for the F2 thread).
# Master §III.3.1 e (engine code), §III.3.2 c (response-scaling map).
# Fitting code: it never reads files; it sees only (X, y, foldid, seed, settings).

# One glmnet path solving the TARGET objective
#   RSS/(2 n_D) + λ [α ||β||_1 + (1 - α) ||β||^2 / 2]          (§III.3.2 a)
# on data (Xd, yd), no intercept, no standardisation.
# glmnet's gaussian driver divides y by s = sqrt(mean(yd^2)) and the user λ by s, then
# multiplies back, so a native call with (a, l) minimises
#   RSS/(2 n_D) + l a ||β||_1 + l (1 - a) ||β||^2 / (2 s)      (§III.3.2 c, [V-src]).
# Solving l a = λ α and l (1 - a) / s = λ (1 - α) gives m = α + s (1 - α), a = α / m,
# l = λ m (exactly m = 1 when α = 1). s is the fitted data's own (fold's own) response RMS.
glmnet_target_path <- function(Xd, yd, alpha, lam, pf, G) {
  s <- sqrt(mean(yd^2))
  if (!is.finite(s) || s <= 0) stop("response RMS of a fitted data set is not finite and positive")
  m <- alpha + s * (1 - alpha)
  fit <- glmnet::glmnet(Xd, yd, family = "gaussian", alpha = alpha / m, lambda = lam * m,
                        penalty.factor = pf, intercept = FALSE, standardize = FALSE,
                        type.gaussian = G$type_gaussian,
                        control = list(thresh = G$thresh, maxit = G$maxit,
                                       fdev = G$fdev, devmax = G$devmax))
  check_glmnet_path(fit, lam * m, G)
  B <- as.matrix(fit$beta)
  scale <- max(1, max(abs(crossprod(Xd, yd))) / nrow(Xd))
  list(B = B, s = s, m = m, a = alpha / m, jerr = fit$jerr, npasses = fit$npasses,
       kkt = kkt_glmnet(Xd, yd, B, lam, alpha, pf, scale))
}

# Stops on: jerr != 0; a returned path shorter than or different from the requested native
# grid (relative tolerance G$lambda_rel_tol); a nonzero intercept; non-finite coefficients.
check_glmnet_path <- function(fit, lam_native, G) {
  if (!identical(as.integer(fit$jerr), 0L)) stop("glmnet jerr = ", fit$jerr)
  if (length(fit$lambda) != length(lam_native))
    stop(sprintf("glmnet returned %d of %d lambda values", length(fit$lambda), length(lam_native)))
  if (max(abs(fit$lambda / lam_native - 1)) > G$lambda_rel_tol)
    stop("glmnet returned a lambda path different from the requested one")
  if (any(fit$a0 != 0)) stop("glmnet returned a nonzero intercept")
  if (any(!is.finite(as.matrix(fit$beta)))) stop("glmnet returned non-finite coefficients")
  invisible(TRUE)
}

# Relative KKT residual of the target objective at every grid point (§III.3.1 e):
# g = X_D'(y_D - X_D B)/n_D;
#   active j:   |g_j - λ (1 - α) pf_j β_j - λ α pf_j sign(β_j)|
#   inactive j: max(|g_j| - λ α pf_j, 0)
# column maximum divided by scale = max(1, max_j |X_j'y_D| / n_D).
kkt_glmnet <- function(Xd, yd, B, lam, alpha, pf, scale) {
  g <- crossprod(Xd, yd - Xd %*% B) / nrow(Xd)            # p x L
  pen1 <- outer(pf, lam * alpha)                          # λ α pf_j
  pen2 <- outer(pf, lam * (1 - alpha))                    # λ (1 - α) pf_j
  viol <- pmax(abs(g) - pen1, 0)
  act <- B != 0
  viol[act] <- abs(g[act] - pen2[act] * B[act] - pen1[act] * sign(B[act]))
  apply(viol, 2L, max) / scale
}

# Full-data fit plus one fit per training fold on the same target grid; CV summaries as in
# cv.glmnet(type.measure = "mse", grouped = TRUE) [V-src cvstats.R l.6-7].
glmnet_cv_engine <- function(X, y, foldid, alpha, lam, pf, G) {
  n <- nrow(X); K <- max(foldid); L <- length(lam)
  # Re-raise a path error with the fit's identity so a production failure is diagnosable.
  path_or_stop <- function(Xd, yd, label) tryCatch(glmnet_target_path(Xd, yd, alpha, lam, pf, G),
    error = function(e) stop(sprintf("alpha %g, %s fit: %s", alpha, label, conditionMessage(e)), call. = FALSE))
  full <- path_or_stop(X, y, "full")
  oof <- matrix(NA_real_, n, L); kkt_fold <- matrix(NA_real_, K, L); fold_diag <- vector("list", K)
  for (k in seq_len(K)) {
    te <- foldid == k
    fk <- path_or_stop(X[!te, , drop = FALSE], y[!te], sprintf("fold %d", k))
    oof[te, ] <- X[te, , drop = FALSE] %*% fk$B
    kkt_fold[k, ] <- fk$kkt; fold_diag[[k]] <- fk[c("s", "m", "a", "jerr", "npasses")]
  }
  if (any(!is.finite(oof))) stop("non-finite out-of-fold prediction")
  nk  <- tabulate(foldid, K)
  mse <- t(vapply(seq_len(K), function(k)
           colMeans((y[foldid == k] - oof[foldid == k, , drop = FALSE])^2), numeric(L)))
  cvm  <- drop(nk %*% mse) / n                                   # fold-size-weighted mean
  cvsd <- sqrt(drop(nk %*% sweep(mse, 2, cvm)^2) / n / (K - 1))  # grouped SE
  if (any(!is.finite(mse)) || any(!is.finite(cvm)) || any(!is.finite(cvsd)) || any(cvsd < 0) ||
      length(cvm) != L || any(!is.finite(full$kkt)) || any(!is.finite(kkt_fold)))
    stop("non-finite CV summary or KKT diagnostic")
  list(full = full, oof = oof, mse = mse, cvm = cvm, cvsd = cvsd,
       kkt_fold = kkt_fold, fold_diag = fold_diag)
}

# glmnet's getOptcv rule on a decreasing grid [V-src getOptcv.glmnet.R l.5-12].
cv_choose <- function(cvm, cvsd) {
  i_min <- min(which(cvm <= min(cvm)))        # largest lambda among exact minima
  i_1se <- min(which(cvm <= cvm[i_min] + cvsd[i_min]))
  c(min = i_min, one_se = i_1se)
}
