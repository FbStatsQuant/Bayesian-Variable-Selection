# glmnet_helpers.R (shared by F1, F2, F3): the CV engine of master §III.3.1 e, with the
# KKT and path checks it names. glmnet_target_path(), glmnet_cv_engine() and cv_choose()
# are the master's code; kkt_glmnet() and check_glmnet_path() implement the comments and
# the bullet under that code. Sourcing this file computes nothing.

# Full-path fit of the TARGET objective RSS/(2n) + lambda*[alpha*sum pf_j |b_j| +
# (1 - alpha) * sum pf_j b_j^2 / 2] on (Xd, yd), no intercept, no standardisation.
# glmnet rescales y by s = sqrt(mean(yd^2)); the native (alpha, lambda) = (alpha/m, lam*m)
# with m = alpha + s(1 - alpha) undo it exactly (§III.3.2 c). m == 1 when alpha == 1.
glmnet_target_path <- function(Xd, yd, alpha, lam, pf, G) {
  s <- sqrt(mean(yd^2)); m <- alpha + s * (1 - alpha)
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

# Stops unless glmnet solved the whole requested grid cleanly (§III.3.1 e, h).
check_glmnet_path <- function(fit, lam_native, G) {
  if (fit$jerr != 0) stop("glmnet jerr = ", fit$jerr, " (npasses ", fit$npasses, "; returned ",
                          length(fit$lambda), " of ", length(lam_native), " lambda values)")
  if (length(fit$lambda) != length(lam_native))
    stop("glmnet returned ", length(fit$lambda), " of ", length(lam_native), " lambda values")
  if (max(abs(fit$lambda / lam_native - 1)) > G$lambda_rel_tol)
    stop("glmnet returned a lambda grid different from the requested one")
  if (any(fit$a0 != 0)) stop("glmnet returned a nonzero intercept")
  if (!identical(dim(fit$beta), c(nrow(fit$beta), length(lam_native))) ||
      any(!is.finite(as.matrix(fit$beta)))) stop("glmnet returned non-finite or misshaped coefficients")
  invisible(TRUE)
}

# Relative KKT violation per lambda (target scale). g = Xd'(yd - Xd B)/n_d.
# Active j:   |g_j - lambda(1 - alpha) pf_j b_j - lambda alpha pf_j sign(b_j)|.
# Inactive j: max(|g_j| - lambda alpha pf_j, 0).
# Column maximum divided by scale = max(1, max_j |Xd_j'yd| / n_d).
kkt_glmnet <- function(Xd, yd, B, lam, alpha, pf, scale) {
  g <- crossprod(Xd, yd - Xd %*% B) / nrow(Xd)           # p x L; yd recycles down columns
  pen_l1 <- alpha * outer(pf, lam)                        # lambda alpha pf_j
  pen_l2 <- (1 - alpha) * outer(pf, lam) * B              # lambda (1 - alpha) pf_j b_j
  viol <- pmax(abs(g) - pen_l1, 0)
  act <- B != 0
  viol[act] <- abs(g - pen_l2 - pen_l1 * sign(B))[act]
  apply(viol, 2L, max) / scale
}

glmnet_cv_engine <- function(X, y, foldid, alpha, lam, pf, G) {
  n <- nrow(X); K <- max(foldid); L <- length(lam)
  # Failures name the fit (full data or fold k) so a production error can be traced.
  labelled <- function(label, expr) withCallingHandlers(expr, error = function(e)
    stop(label, ": ", conditionMessage(e), call. = FALSE))
  full <- labelled("full-data fit", glmnet_target_path(X, y, alpha, lam, pf, G))
  oof <- matrix(NA_real_, n, L); kkt_fold <- matrix(NA_real_, K, L); fold_diag <- vector("list", K)
  for (k in seq_len(K)) {
    te <- foldid == k
    fk <- labelled(paste("fold", k), glmnet_target_path(X[!te, , drop = FALSE], y[!te], alpha, lam, pf, G))
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

cv_choose <- function(cvm, cvsd) {            # glmnet's getOptcv rule on a decreasing grid
  i_min <- min(which(cvm <= min(cvm)))        # largest lambda among exact minima
  i_1se <- min(which(cvm <= cvm[i_min] + cvsd[i_min]))
  c(min = i_min, one_se = i_1se)
}
