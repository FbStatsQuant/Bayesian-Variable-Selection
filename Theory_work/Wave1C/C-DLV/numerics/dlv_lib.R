# helpers: designs (R port of W1-GEN bvs_core.py) and per-fit recording
lh_sigma <- function(G, g, rho, psis) {
  p <- G * g
  Sg <- (1 - rho) * diag(g) + rho * matrix(1, g, g)
  S <- matrix(0, p, p)
  for (h in 0:(G - 1)) S[h * g + 1:g, h * g + 1:g] <- Sg
  for (i in seq_along(psis)) {
    a <- 2 * (i - 1); b <- a + 1
    blk <- psis[i] * outer(Sg[, 1], Sg[1, ])
    S[a * g + 1:g, b * g + 1:g] <- blk
    S[b * g + 1:g, a * g + 1:g] <- t(blk)
  }
  S
}
hub <- function(h, g = 9) h * g + 1   # 1-based index of hub of 0-based group h
make_theta <- function(design, p, g = 9, psi = 0.2) {
  th <- numeric(p)
  if (design == "M") { th[hub(0)] <- 1; th[hub(1)] <- -psi }
  else { th[hub(0)] <- 1; th[hub(2)] <- 0.7 }   # F: first unlinked group = 0-based index 2 (third group)
  th
}
S0_of <- function(design) if (design == "M") c(hub(0), hub(1)) else c(hub(0), hub(2))
make_data <- function(design, n, p, seed, g = 9, rho = 0.4, psi = 0.2) {
  G <- p / g
  Sigma <- lh_sigma(G, g, rho, psi)          # c = 1 linked pair in both designs
  th <- make_theta(design, p, g, psi)
  set.seed(seed)
  Lc <- t(chol(Sigma))                       # lower factor L, Sigma = L L'
  if (p <= n - 1) {
    Z <- matrix(rnorm(n * p), n, p); Z <- sweep(Z, 2, colMeans(Z))
    Q <- qr.Q(qr(Z))
    X <- sqrt(n - 1) * Q %*% t(Lc)
    dtype <- "exact_gram"
  } else {
    X <- matrix(rnorm(n * p), n, p) %*% t(Lc); dtype <- "iid"
  }
  y <- as.numeric(X %*% th + rnorm(n))
  list(X = X, y = y, theta = th, S0 = S0_of(design), dtype = dtype)
}
Lambda_V <- function(snap, tgrid = seq(0, 2, length.out = 2001)) {
  if (snap$truncated) return(NA_real_)
  lg <- snap$log_gamma0; d <- snap$d
  vmax <- -Inf
  for (t in tgrid) {
    w <- lg + t * d; w <- exp(w - max(w)); w <- w / sum(w)
    m <- sum(w * d); v <- sum(w * (d - m)^2)
    if (v > vmax) vmax <- v
  }
  vmax
}
has_S0 <- function(snap, S0) {
  any(vapply(snap$models, function(m) identical(sort(as.integer(m)), sort(as.integer(S0))), TRUE))
}
