# mock_packages.R -- TEST ONLY (PR12 MINOR-11): stand-ins with the result structure p1m_competitors.R reads from glmnet,
# ncvreg, biglasso/bigmemory, L0Learn, susieR, varbvs and BAS. They check the harness's extraction and record logic,
# not the packages (whose real APIs are verified when they are installed on NOTS). Loaded via P1M_COMPETITOR_MOCK.
.mock_fit <- function(X, y, k = 5) {   # top-k marginal correlations + OLS: a plausible sparse coefficient vector
  r <- abs(drop(stats::cor(X, y))); keep <- sort(order(-r)[seq_len(k)])
  f <- stats::lm.fit(cbind(1, X[, keep, drop = FALSE]), y)
  b <- numeric(ncol(X)); b[keep] <- f$coefficients[-1]
  list(a = unname(f$coefficients[1]), b = b, s2 = sum(f$residuals^2) / (length(y) - k - 1), keep = keep)
}
MOCK[["glmnet::cv.glmnet"]] <- function(X, y, foldid, family, alpha) {
  m <- .mock_fit(X, y); structure(list(m = m, lambda = c(0.2, 0.1), lambda.min = 0.1, lambda.1se = 0.2, cvm = c(m$s2 * 1.1, m$s2)), class = "mock_cvglmnet")
}
coef.mock_cvglmnet <- function(object, s, ...) c(object$m$a, object$m$b)
MOCK[["ncvreg::cv.ncvreg"]] <- function(X, y, penalty, fold, seed) { m <- .mock_fit(X, y); structure(list(m = m, cve = c(m$s2 * 1.2, m$s2)), class = "mock_cvncv") }
coef.mock_cvncv <- function(object, ...) c(`(Intercept)` = object$m$a, object$m$b)
MOCK[["bigmemory::as.big.matrix"]] <- function(X) X
MOCK[["biglasso::cv.biglasso"]] <- function(X, y, nfolds, seed, ncores) { m <- .mock_fit(X, y); structure(list(m = m, cve = c(m$s2 * 1.2, m$s2)), class = "mock_cvncv") }
MOCK[["L0Learn::L0Learn.cvfit"]] <- function(X, y, penalty, nFolds, seed) {
  m <- .mock_fit(X, y)
  structure(list(m = m, cvMeans = list(c(m$s2 * 1.3, m$s2 * 1.1), c(m$s2 * 1.2, m$s2)),
                 fit = list(lambda = list(c(0.2, 0.1), c(0.3, 0.15)), gamma = c(0, 0.01))), class = "mock_l0")
}
coef.mock_l0 <- function(object, lambda, gamma, ...) { stopifnot(lambda == 0.15, gamma == 0.01); c(object$m$a, object$m$b) }
MOCK[["susieR::susie"]] <- function(X, y, L) {
  m <- .mock_fit(X, y); pip <- rep(0.001, ncol(X)); pip[m$keep] <- 0.97
  structure(list(m = m, pip = pip, sigma2 = m$s2), class = "mock_susie")
}
coef.mock_susie <- function(object, ...) c(object$m$a, object$m$b)
MOCK[["varbvs::varbvs"]] <- function(X, Z, y, family, verbose) {
  m <- .mock_fit(X, y); pip <- rep(0.002, ncol(X)); pip[m$keep] <- 0.95
  structure(list(m = m, pip = pip, w = c(0.4, 0.6), sigma = c(m$s2, m$s2)), class = "mock_vb")
}
coef.mock_vb <- function(object, ...) { v <- c(object$m$a, object$m$b); cbind(v * 0.9, v * 1.1, v) }   # last column = averaged
MOCK[["BAS::beta.binomial"]] <- function(a, b) list(a = a, b = b)
MOCK[["BAS::bas.lm"]] <- function(formula, data, method, prior, alpha, modelprior, MCMC.iterations, initprobs) {
  X <- as.matrix(data[, -1]); m <- .mock_fit(X, data$y)
  pr <- rep(0.003, ncol(X)); pr[m$keep] <- 0.9
  list(postprobs = c(0.7, 0.3), which = list(c(0, m$keep), c(0, m$keep[-1])), probne0 = c(1, pr))
}
