#!/usr/bin/env Rscript
# Follow-up diagnostic (not a gate) for unit test i.1: the G3 run gave max|z| = 4.27 over 50
# coordinates, inside the pre-declared bound 5 but in the tail (about 1e-3 under correct
# sampling). Repeats the Bhattacharya kernel check on the same frozen fixture with four other
# draw seeds and reports, per seed, max|z|, the whitened statistic
# Q = M (xbar - m)' Sigma^-1 (xbar - m) (chi-square with 50 df under correct sampling; the
# marginal z_j are correlated, so sum z_j^2 is not chi-square) and the Frobenius ratio. Also
# reruns the G3 draw seed and lists the largest |z| coordinates. Usage: Rscript tests/diag_kernel_z.R
code_dir <- dirname(dirname(normalizePath(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1]))))
sys.source(file.path(code_dir, "config.R"), envir = globalenv())
.libPaths(c(COMMON$LIB, .Library))
RNGkind(COMMON$RNG_KIND[1], COMMON$RNG_KIND[2], COMMON$RNG_KIND[3])
set.seed(TEST_SEED)
n <- 20L; p <- 50L; M <- 200000L
Phi <- matrix(rnorm(n * p), n); alpha <- rnorm(n); d <- runif(p, 0.5, 2)
Sigma <- solve(crossprod(Phi) + diag(1 / d, p))
m <- drop(Sigma %*% crossprod(Phi, alpha))
for (sd_ in TEST_SEED + c(1L, 2L, 3L, 4L, 5L)) {
  set.seed(sd_)
  D <- matrix(0, p, M)
  for (i in seq_len(M)) D[, i] <- as.vector(bayesreg:::bayesreg.fastmvg_bhat(Phi, alpha, d)$x)
  xbar <- rowMeans(D)
  z <- (xbar - m) / sqrt(diag(Sigma) / M)
  S <- tcrossprod(D - xbar) / (M - 1)
  dm <- xbar - m
  Q <- M * drop(crossprod(dm, solve(Sigma, dm)))      # solve() instead of an explicit inverse
  cat(sprintf("draw seed %d: max|z| = %.3f at j = %d; Q = %.1f (chi2_50: P(>= Q) = %.3f); relF = %.5f\n",
              sd_, max(abs(z)), which.max(abs(z)), Q, pchisq(Q, p, lower.tail = FALSE),
              norm(S - Sigma, "F") / norm(Sigma, "F")))
  if (sd_ == TEST_SEED + 1L) { o <- order(-abs(z))[1:5]; cat("  largest |z|:", sprintf("j=%d z=%.2f", o, z[o]), "\n") }
}
