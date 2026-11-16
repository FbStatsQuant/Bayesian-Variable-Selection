# start_common.R -- W3-START sharpness-gate numerics: shared helpers.
# OBSERVATIONS ONLY, never proofs; all theorems are asymptotic. Runs the PRODUCTION core (Scripts/SMC_BVS/core,
# compiled locally with Rcpp; no NOTS): pi_0 is read from the coded start (cpp_start_logmass), the block tables from
# cpp_setup. Nothing in the core is edited.
#
# Quantities (STATEMENT.md section 2):
#   o0   = (1 - pi0(S0))/pi0(S0)                         start odds against S0 (from the coded log pi0)
#   T1   = sum_{l notin S0} gamma0(S0+l)/gamma0(S0)      single-null block Bayes factors, prior weighted (from tables)
#   fn   = (s0+1)(p-s0)/((2p-1-s0) sqrt(n+1))            deterministic floor (claim FLOOR): T1 >= fn always
#   U    = p^-1 sum_{l notin S0} m_l                     m_l = max one-step table ratio of l over T >= U*_b in its block
#   en   = 2p max [r_b(U)/r_b(U + U*_b)]^(1/a)           truth-deletion functional
#   Lb0  = p^-1 sum_l J_n(delta_{U*_b,l}, tau_{U*_b})    block-relative leading leakage functional (deterministic in X,theta)
#   pred = ((s0+1) p/(2p-1-s0)) n^-1/2 Lb0               the scale the theorem assigns to T1 (up to an O(1) factor)
#   cnull_max = max_l delta^2_{U*_b,l}/(tau^2 log n)     realised leakage level of the worst null (block relative)
#   ctruth_min = min_j delta^2_{U*_b - j, j}/(tau^2 log n) realised visibility level of the weakest truth
#   cvis_all = min over truths j and ALL U in the block of delta^2_{U,j}/(tau_U^2 log n)   (the (V-c) quantity; seeds <= 2)
#   Xi_del = sum over truth blocks b and U not containing U*_b of w(U) r_b(U)/r_b(U*_b), w(U) = (2p)^((d-a)+) (16 s0/p)^((a-d)+),
#            d = |U*_b - U|, a = |U - U*_b|   (refined truth-block deletion functional Xi)
#   Xi_in  = the same sum over U strictly containing U*_b (in-block null additions)

core_dir <- Sys.getenv("W3START_CORE", "C:/Users/felip/BVS-wt/W3-START/Scripts/SMC_BVS/core")
suppressMessages(source(file.path(core_dir, "v3.R")))

std_cols <- function(X) {
  Xc <- sweep(X, 2, colMeans(X))
  s <- sqrt(colSums(Xc^2) / (nrow(X) - 1))
  sweep(Xc, 2, s, "/")
}
std_vec <- function(y) { yc <- y - mean(y); yc / sqrt(sum(yc^2) / (length(y) - 1)) }

zn <- function(n, p) sqrt(2 * log(2^21 * p) + 2 * log(log(n)))

# J_n(d, t) = E[exp((d + sigma Z)^2/(2 t^2)); |Z| <= z], closed form (complete the square); vectorised in d, t.
Jn <- function(d, t, sigma, z) {
  a <- pmin(sigma^2 / t^2, 1)
  out <- numeric(length(d))
  eq <- (1 - a) < 1e-12
  if (any(eq)) {                       # t = sigma: integrand (2 pi)^-1/2 exp(d^2/(2 s^2) + d u / s)
    de <- abs(d[eq]) / sigma
    out[eq] <- ifelse(de < 1e-10, sqrt(2 / pi) * z,
                      exp(de^2 / 2) * (exp(de * z) - exp(-de * z)) / (de * sqrt(2 * pi)))
  }
  if (any(!eq)) {
    dd <- d[!eq]; tt <- t[!eq]; aa <- a[!eq]
    cc <- dd * sigma / tt^2; m <- cc / (1 - aa); sq <- sqrt(1 - aa)
    out[!eq] <- exp(dd^2 / (2 * tt^2) + cc^2 / (2 * (1 - aa))) / sq * (pnorm((z - m) * sq) - pnorm((-z - m) * sq))
  }
  out
}

popcount <- function(x) { c <- integer(length(x)); while (any(x > 0)) { c <- c + bitwAnd(x, 1L); x <- bitwShiftR(x, 1L) }; c }

# Everything about the coded start for one data set. Xs: standardised design; y: raw response; mu = Xs theta (known).
start_stats <- function(Xs, y, S0, sigma, mu, lattice_Q = NULL, ndraw = 0, draw_seed = 1L, full_vis = FALSE) {
  n <- nrow(Xs); p <- ncol(Xs); s0 <- length(S0)
  ctx <- v3_context(Xs, std_vec(y), return_gram = FALSE)
  su <- v3_setup(ctx)
  if (inherits(su, "v3_setup_failed")) return(list(status = "setup_failed"))
  lp0 <- v3_start_logmass(su$start, sort(S0))
  o0 <- expm1(-lp0)
  blk <- integer(p); for (b in seq_along(su$blocks)) blk[su$blocks[[b]]] <- b
  isS0 <- logical(p); isS0[S0] <- TRUE
  z <- zn(n, p)
  sum_step <- 0; sum_m <- 0; maxdel <- -Inf
  Jsum <- 0; cnull_max <- 0; ctruth_min <- Inf; Xi_del <- 0; Xi_in <- 0; cvis_all <- Inf
  for (b in seq_along(su$blocks)) {
    mem <- su$blocks[[b]]; m <- length(mem); lr <- su$tables[[b]]$log_r
    tr <- isS0[mem]; ustar <- sum(bitwShiftL(1L, which(tr) - 1L)); codes <- 0:(2^m - 1)
    has_u <- bitwAnd(codes, ustar) == ustar
    # ---- data functionals from the tables
    for (i in which(!tr)) {
      lbit <- bitwShiftL(1L, i - 1L)
      sel <- codes[has_u & bitwAnd(codes, lbit) == 0L]
      st <- lr[sel + lbit + 1L] - lr[sel + 1L]
      sum_m <- sum_m + exp(max(st))
      sum_step <- sum_step + exp(lr[ustar + lbit + 1L] - lr[ustar + 1L])
    }
    if (ustar > 0L) {
      miss <- popcount(bitwAnd(bitwXor(codes, ustar), ustar))       # a = |U* \ U|
      sel <- which(miss >= 1L)
      v <- (lr[sel] - lr[bitwOr(codes[sel], ustar) + 1L]) / miss[sel]
      maxdel <- max(maxdel, max(v))
      # refined truth-block functionals: every alternative configuration U of the truth block, prior weighted
      extra <- popcount(bitwAnd(codes, bitwNot(ustar)))             # a = |U \ U*|
      wgt <- pmax(miss - extra, 0) * log(2 * p) + pmax(extra - miss, 0) * log(16 * s0 / p) + lr - lr[ustar + 1L]
      Xi_del <- Xi_del + sum(exp(wgt[miss >= 1L]))
      Xi_in <- Xi_in + sum(exp(wgt[miss == 0L & extra >= 1L]))
      if (full_vis) {                                               # min over ALL U of the single-step level (V-c)
        Gb <- crossprod(Xs[, mem, drop = FALSE]); cb <- as.numeric(crossprod(Xs[, mem, drop = FALSE], mu)); mu2 <- sum(mu^2)
        Lam <- numeric(2^m); Lam[1] <- mu2
        for (cd in 1:(2^m - 1)) { ii <- which(bitwAnd(cd, bitwShiftL(1L, 0:(m - 1))) > 0L)
          Lam[cd + 1L] <- mu2 - sum(cb[ii] * solve(Gb[ii, ii, drop = FALSE], cb[ii])) }
        for (i in which(tr)) { jb <- bitwShiftL(1L, i - 1L); selU <- codes[bitwAnd(codes, jb) == 0L]
          d2 <- Lam[selU + 1L] - Lam[selU + jb + 1L]; t2 <- sigma^2 + pmax(Lam[selU + 1L], 0) / (n - 1)
          cvis_all <- min(cvis_all, min(d2 / (t2 * log(n)))) }
      }
    }
    # ---- deterministic functionals of (X, theta): delta_{U*,l}, tau_{U*}
    nul <- mem[!tr]; tru <- mem[tr]
    if (length(tru)) { qrU <- qr(Xs[, tru, drop = FALSE]); rmu <- qr.resid(qrU, mu) } else rmu <- mu
    tau2 <- sigma^2 + sum(rmu^2) / (n - 1)
    if (length(nul)) {
      Xl <- Xs[, nul, drop = FALSE]
      if (length(tru)) Xl <- qr.resid(qrU, Xl)
      nr <- sqrt(colSums(Xl^2))
      del <- ifelse(nr > 1e-8, as.numeric(crossprod(Xl, rmu)) / nr, 0)
      Jsum <- Jsum + sum(Jn(del, rep(sqrt(tau2), length(del)), sigma, z))
      cnull_max <- max(cnull_max, max(del^2) / (tau2 * log(n)))
    }
    for (j in tru) {                                                # visibility of j at U = U*_b - j
      oth <- setdiff(tru, j)
      if (length(oth)) { q2 <- qr(Xs[, oth, drop = FALSE]); r2 <- qr.resid(q2, mu); xj <- qr.resid(q2, Xs[, j]) } else { r2 <- mu; xj <- Xs[, j] }
      dj <- sum(xj * r2) / sqrt(sum(xj^2)); t2 <- sigma^2 + sum(r2^2) / (n - 1)
      ctruth_min <- min(ctruth_min, dj^2 / (t2 * log(n)))
    }
  }
  T1 <- (s0 + 1) / (2 * p - 1 - s0) * sum_step
  U <- sum_m / p
  en <- if (s0 > 0) 2 * p * exp(maxdel) else 0
  fn <- (s0 + 1) * (p - s0) / ((2 * p - 1 - s0) * sqrt(n + 1))
  Lb0 <- Jsum / p
  pred <- (s0 + 1) * p / (2 * p - 1 - s0) * Lb0 / sqrt(n)
  out <- list(status = "ok", n = n, p = p, s0 = s0, B = su$B, logpi0 = lp0, pi0 = exp(lp0), o0 = o0, T1 = T1, fn = fn,
              U = U, en = en, Lb0 = Lb0, pred = pred, cnull_max = cnull_max,
              ctruth_min = if (s0 > 0) ctruth_min else NA_real_, lat = NA_real_, nblk_truth = length(unique(blk[S0])),
              Xi_del = Xi_del, Xi_in = Xi_in, cvis_all = if (full_vis && s0 > 0) cvis_all else NA_real_)
  if (!is.null(lattice_Q) && ndraw > 0) {                           # lattice mass by exact iid draws from the coded sampler
    inQ <- logical(p); inQ[lattice_Q] <- TRUE
    dr <- v3_start_draw(su$start, ndraw, draw_seed)
    ok <- vapply(dr, function(S) all(S0 %in% S) && all(inQ[S]), TRUE)
    out$lat <- mean(ok)
  }
  out
}

# ---------------------------------------------------------------- designs
# Each returns list(Xs, y, S0, sigma, mu, [Q]).
gen_iid <- function(n, p, theta, sigma = 1) {
  Xs <- std_cols(matrix(rnorm(n * p), n, p)); S0 <- seq_along(theta)
  mu <- if (length(theta)) as.numeric(Xs[, S0, drop = FALSE] %*% theta) else numeric(n)
  list(Xs = Xs, y = mu + sigma * rnorm(n), S0 = S0, sigma = sigma, mu = mu)
}
# nulls exactly orthogonal to (1, X_S0): zero leakage at every U subset of S0 (fixed-design no-leakage class)
orth_nulls <- function(X, S0) {
  n <- nrow(X); A <- cbind(1, X[, S0, drop = FALSE]); q <- qr(A)
  X[, -S0] <- qr.resid(q, X[, -S0, drop = FALSE]); X
}
gen_orth <- function(n, p, theta, sigma = 1, leak = NULL) {
  X <- matrix(rnorm(n * p), n, p); S0 <- seq_along(theta)
  X[, S0] <- std_cols(X[, S0, drop = FALSE]); X <- orth_nulls(X, S0); Xs <- std_cols(X)
  mu <- as.numeric(Xs[, S0, drop = FALSE] %*% theta)
  if (!is.null(leak)) {     # add a component along mu to chosen nulls: delta_{empty,l}^2 = c tau_empty^2 log n
    Delta <- sum(mu^2) / (n - 1); tau2 <- sigma^2 + Delta
    a2 <- leak$c * tau2 * log(n) / ((n - 1) * Delta); a <- sqrt(min(a2, 0.98))
    mt <- mu / sqrt(sum(mu^2)) * sqrt(n - 1)
    idx <- if (identical(leak$which, "all")) setdiff(seq_len(p), S0) else leak$which
    Xs[, idx] <- sqrt(1 - a^2) * Xs[, idx] + a * mt
    Xs <- std_cols(Xs); mu <- as.numeric(Xs[, S0, drop = FALSE] %*% theta)
  }
  list(Xs = Xs, y = mu + sigma * rnorm(n), S0 = S0, sigma = sigma, mu = mu)
}
# near-twin nulls: floor (FL-16) violated among nulls (lambda_min ~ gam/n)
gen_twin <- function(n, p, theta, sigma = 1, gam = 1) {
  s0 <- length(theta); h <- (p - s0) %/% 2
  base <- matrix(rnorm(n * (s0 + h)), n, s0 + h)
  tw <- base[, s0 + seq_len(h)] + sqrt(2 * gam / n) * matrix(rnorm(n * h), n, h)
  X <- cbind(base, tw); if (ncol(X) < p) X <- cbind(X, matrix(rnorm(n * (p - ncol(X))), n))
  Xs <- std_cols(X); S0 <- seq_len(s0); mu <- as.numeric(Xs[, S0, drop = FALSE] %*% theta)
  list(Xs = Xs, y = mu + sigma * rnorm(n), S0 = S0, sigma = sigma, mu = mu)
}
# Gaussian rows; every null has population correlation rho with truth 1 (population leakage rho*theta_1)
gen_gleak <- function(n, p, theta, sigma = 1, rho = 0) {
  s0 <- length(theta); W <- matrix(rnorm(n * p), n, p)
  W[, -(1:s0)] <- rho * W[, 1] + sqrt(1 - rho^2) * W[, -(1:s0)]
  Xs <- std_cols(W); S0 <- seq_len(s0); mu <- as.numeric(Xs[, S0, drop = FALSE] %*% theta)
  list(Xs = Xs, y = mu + sigma * rnorm(n), S0 = S0, sigma = sigma, mu = mu)
}
# AR(1) rows; truths spaced; Q = neighbourhood of radius d_n = ceil(log n/(2 log(1/rho)))
gen_ar1 <- function(n, p, theta, sigma = 1, rho = 0.5) {
  E <- matrix(rnorm(n * p), n, p); W <- E
  for (j in 2:p) W[, j] <- rho * W[, j - 1] + sqrt(1 - rho^2) * E[, j]
  s0 <- length(theta); S0 <- round(seq(p / (s0 + 1), by = p / (s0 + 1), length.out = s0))
  Xs <- std_cols(W); mu <- as.numeric(Xs[, S0, drop = FALSE] %*% theta)
  d <- ceiling(log(n) / (2 * log(1 / rho)))
  Q <- sort(unique(unlist(lapply(S0, function(j) max(1, j - d):min(p, j + d)))))
  list(Xs = Xs, y = mu + sigma * rnorm(n), S0 = S0, sigma = sigma, mu = mu, Q = Q)
}

# Structured fixed design for the leakage boundary: s0 truths, each with B-1 "satellite" nulls (corr 0.9 with it), so
# each truth's block is full and holds exactly the truth and its satellites; all other nulls are orthogonal to the
# truths (zero leakage). leak = list(c, which = "one" | "all"): the chosen non-satellite nulls get a component along mu
# with delta^2_{empty,l} = c tau_empty^2 log n (their block has U* = empty because the truth blocks are full).
gen_sat <- function(n, p, theta, sigma = 1, leak = NULL) {
  s0 <- length(theta); B <- min(floor(sqrt(n)), floor(sqrt(p)), 16); ns <- B - 1
  X <- matrix(rnorm(n * p), n, p); S0 <- seq_len(s0)
  X[, S0] <- std_cols(X[, S0, drop = FALSE]); X <- orth_nulls(X, S0); Xs <- std_cols(X)
  mu <- as.numeric(Xs[, S0, drop = FALSE] %*% theta)
  sat <- integer(0)
  for (k in S0) { idx <- s0 + (k - 1) * ns + seq_len(ns); Xs[, idx] <- 0.9 * Xs[, k] + sqrt(1 - 0.81) * Xs[, idx]; sat <- c(sat, idx) }
  free <- setdiff(seq_len(p), c(S0, sat))
  if (!is.null(leak) && leak$c > 0) {
    Delta <- sum(mu^2) / (n - 1); tau2 <- sigma^2 + Delta
    a <- sqrt(min(leak$c * tau2 * log(n) / ((n - 1) * Delta), 0.98))
    mt <- mu / sqrt(sum(mu^2)) * sqrt(n - 1)
    idx <- if (identical(leak$which, "all")) free else free[length(free)]
    Xs[, idx] <- sqrt(1 - a^2) * Xs[, idx] + a * mt
  }
  list(Xs = Xs, y = mu + sigma * rnorm(n), S0 = S0, sigma = sigma, mu = mu)
}
