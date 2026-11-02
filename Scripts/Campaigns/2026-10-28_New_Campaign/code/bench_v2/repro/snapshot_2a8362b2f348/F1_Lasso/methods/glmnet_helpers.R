# glmnet_helpers.R -- shared glmnet engine for F1, F2, F3 (master §III.3.1 e, code block "glmnet_helpers.R").
# glmnet_target_path(), glmnet_cv_engine() and cv_choose() follow the master's code; kkt_glmnet() and
# check_glmnet_path() implement the comments and bullets under it.
#
# Target objective on the original scale: RSS/(2n) + λ[α Σ pf_j |β_j| + (1 - α) Σ pf_j β_j² / 2].
# glmnet rescales y internally by s = sqrt(mean(y²)), so its native objective is
# RSS/(2n) + λ a ‖β‖₁ + λ(1 - a)‖β‖²/(2s) (§III.3.1 c); calling it with a = α/m and λ·m,
# m = α + s(1 - α), gives the target (§III.3.2 c). For the lasso (α = 1), m = 1 exactly.

# One glmnet path on data (Xd, yd) at the target grid `lam`; every path is checked and KKT-scored.
glmnet_target_path <- function(Xd, yd, alpha, lam, pf, G) {
  s <- sqrt(mean(yd^2)); m <- alpha + s * (1 - alpha)      # m == 1 exactly when alpha == 1
  fit <- glmnet::glmnet(Xd, yd, family = "gaussian", alpha = alpha / m, lambda = lam * m,
                        penalty.factor = pf, intercept = FALSE, standardize = FALSE,
                        type.gaussian = G$type_gaussian,
                        control = list(thresh = G$thresh, maxit = G$maxit,
                                       fdev = G$fdev, devmax = G$devmax))
  check_glmnet_path(fit, lam * m, G)
  B <- as.matrix(fit$beta)
  scale <- max(1, max(abs(crossprod(Xd, yd))) / nrow(Xd))
  list(B = B, s = s, m = m, a = alpha / m, jerr = fit$jerr, npasses = fit$npasses,
       kkt = kkt_glmnet(Xd, yd, B, lam, alpha, pf, scale))      # length-L relative KKT
}

# Stops unless the returned path is complete and clean: jerr == 0; the returned λ equal the requested
# ones (count and relative tolerance); zero intercept; finite coefficients (§III.3.1 e, h).
# A negative jerr comes with a glmnet warning and a truncated path; a positive jerr is a glmnet error.
check_glmnet_path <- function(fit, lam_req, G) {
  if (fit$jerr != 0) stop("glmnet jerr = ", fit$jerr, " (npasses ", fit$npasses, ", returned ",
                          length(fit$lambda), " of ", length(lam_req), " lambda values)")
  if (length(fit$lambda) != length(lam_req))
    stop("glmnet returned ", length(fit$lambda), " lambda values, requested ", length(lam_req))
  if (max(abs(fit$lambda / lam_req - 1)) > G$lambda_rel_tol)
    stop("glmnet returned lambda values differ from the requested grid")
  if (ncol(fit$beta) != length(lam_req)) stop("glmnet beta has the wrong number of columns")
  if (any(fit$a0 != 0)) stop("glmnet returned a nonzero intercept")
  if (any(!is.finite(as.matrix(fit$beta)))) stop("glmnet returned non-finite coefficients")
  invisible(TRUE)
}

# Relative KKT residual per grid point for the target objective (§III.3.1 e, bullet "kkt_glmnet"):
# g = X_D'(y_D - X_D b)/n_D; active j: |g_j - λ(1 - α) pf_j b_j - λ α pf_j sign(b_j)|;
# inactive j: max(|g_j| - λ α pf_j, 0); the maximum over j divided by `scale`.
# pf must be on glmnet's scale (glmnet rescales factors to sum to p; all-ones factors are unchanged).
kkt_glmnet <- function(Xd, yd, B, lam, alpha, pf, scale) {
  Gr <- crossprod(Xd, yd - Xd %*% B) / nrow(Xd)            # p x L matrix of gradients g
  out <- numeric(length(lam))
  for (l in seq_along(lam)) {
    b <- B[, l]; g <- Gr[, l]; act <- b != 0
    r_act <- abs(g[act] - lam[l] * (1 - alpha) * pf[act] * b[act] -
                 lam[l] * alpha * pf[act] * sign(b[act]))
    r_ina <- pmax(abs(g[!act]) - lam[l] * alpha * pf[!act], 0)
    out[l] <- max(c(r_act, r_ina, 0)) / scale
  }
  out
}

# Full-data path plus the K training-fold paths on the same grid, and glmnet's grouped CV summaries
# (type.measure = "mse", grouped = TRUE): cvm = fold-size-weighted mean of fold MSEs,
# cvsd = sqrt(Σ_k n_k (mse_k - cvm)² / Σ_k n_k / (K - 1))   (cv.glmnet cvstats.R l.6-7).
glmnet_cv_engine <- function(X, y, foldid, alpha, lam, pf, G) {
  n <- nrow(X); K <- max(foldid); L <- length(lam)
  full <- tryCatch(glmnet_target_path(X, y, alpha, lam, pf, G),            # name the failing fit
                   error = function(e) stop("full-data fit: ", conditionMessage(e), call. = FALSE))
  oof <- matrix(NA_real_, n, L); kkt_fold <- matrix(NA_real_, K, L); fold_diag <- vector("list", K)
  for (k in seq_len(K)) {
    te <- foldid == k
    fk <- tryCatch(glmnet_target_path(X[!te, , drop = FALSE], y[!te], alpha, lam, pf, G),
                   error = function(e) stop("fold ", k, " fit: ", conditionMessage(e), call. = FALSE))
    oof[te, ] <- X[te, , drop = FALSE] %*% fk$B
    kkt_fold[k, ] <- fk$kkt; fold_diag[[k]] <- fk[c("s", "m", "a", "jerr", "npasses")]
  }
  if (any(!is.finite(oof))) stop("non-finite out-of-fold prediction")
  nk  <- tabulate(foldid, K)
  mse <- t(vapply(seq_len(K), function(k)
           colMeans((y[foldid == k] - oof[foldid == k, , drop = FALSE])^2), numeric(L)))
  cvm  <- drop(nk %*% mse) / n
  cvsd <- sqrt(drop(nk %*% sweep(mse, 2, cvm)^2) / n / (K - 1))
  if (any(!is.finite(mse)) || any(!is.finite(cvm)) || any(!is.finite(cvsd)) || any(cvsd < 0) ||
      length(cvm) != L || any(!is.finite(full$kkt)) || any(!is.finite(kkt_fold)))
    stop("non-finite CV summary or KKT diagnostic")
  list(full = full, oof = oof, mse = mse, cvm = cvm, cvsd = cvsd,
       kkt_fold = kkt_fold, fold_diag = fold_diag)
}

# glmnet's getOptcv.glmnet rule on a decreasing grid.
cv_choose <- function(cvm, cvsd) {
  i_min <- min(which(cvm <= min(cvm)))        # largest lambda among exact minima
  i_1se <- min(which(cvm <= cvm[i_min] + cvsd[i_min]))
  c(min = i_min, one_se = i_1se)
}
