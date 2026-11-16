# gens.R -- designs for the W3-START2-R boundary numerics (OBSERVATIONS ONLY). Sourced after r_common.R.
# Orthonormal frame of 1-perp (BASE L11.0): columns e_i with 1'e_i = 0, e_i'e_j = N 1{i=j}, N = n-1.
frame_e <- function(n, p) { Q <- qr.Q(qr(cbind(1, matrix(rnorm(n * p), n, p)))); Q[, 2:(p + 1), drop = FALSE] * sqrt(n - 1) }
# (V-cp): orthogonal design, one truth e_1, delta^2_{empty,1}/tau^2_empty = target = c log n + 2 log p
gen_vcp <- function(n, p, target, sigma = 1) {
  N <- n - 1; th <- sigma * sqrt(target / (N - target))        # N th^2 = target (sigma^2 + th^2)
  Xs <- frame_e(n, p); mu <- th * Xs[, 1]
  list(Xs = Xs, y = mu + sigma * rnorm(n), S0 = 1L, sigma = sigma, mu = mu, theta = th)
}
# F-2 (BASE L11.3): x1 = e1; x_l = rho e1 + sqrt(1-rho^2) e_l, l = 2..16; x_j = e_j, j >= 17
gen_F2 <- function(n, A, sigma = 1, rho2 = 0.4) {
  N <- n - 1; p <- min(floor(n^A), n - 1); E <- frame_e(n, p); Xs <- E
  Xs[, 2:16] <- sqrt(rho2) * E[, 1] + sqrt(1 - rho2) * E[, 2:16]
  th <- sigma * sqrt(2 * (1 + 2 * A) * log(n) / N); mu <- th * Xs[, 1]
  list(Xs = Xs, y = mu + sigma * rnorm(n), S0 = 1L, sigma = sigma, mu = mu, p = p)
}
# G-1 / (L-gain-0): Gaussian rows Sigma = I, truths 1..s0, optional ONE null (column s0+1) with population corr rho to truth 1
gen_g1 <- function(n, p, theta, sigma = 1, rho = 0) {
  s0 <- length(theta); W <- matrix(rnorm(n * p), n, p)
  if (rho != 0) W[, s0 + 1] <- rho * W[, 1] + sqrt(1 - rho^2) * W[, s0 + 1]
  Xs <- std_cols(W); S0 <- seq_len(s0); mu <- as.numeric(Xs[, S0, drop = FALSE] %*% theta)
  list(Xs = Xs, y = mu + sigma * rnorm(n), S0 = S0, sigma = sigma, mu = mu)
}
