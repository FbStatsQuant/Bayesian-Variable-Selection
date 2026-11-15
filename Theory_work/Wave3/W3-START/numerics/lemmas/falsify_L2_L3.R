# falsify_L2_L3.R -- falsification attempt for lemmas/L2_TK.md and lemmas/L3_LEAK.md. Base R.
# Part A (L2): fixed designs with NEAR-TWIN columns (unnormalised Gram eigenvalue of order 1, correlation eigenvalue
#   of order 1/n). For random sets U (|U| <= 16) and l: (E1), (E2) against the REALISED floor g = lambda_min(G_U);
#   identity (2.1) and (TK-e) (asserted with tolerances); (f1)-(f3) and the score remainder R_U in [-kappa_1, kappa_2]
#   with the REALISED constants (omega = max |rho| over the sets used, g_* = smallest sampled eigenvalue,
#   c_E = smallest RSS^y_U/n): these test the algebra, not the fixed constants or the probability of the event.
#   max|rho_U| versus omega_n is PRINTED as a diagnostic only (a draw outside the event is not a counterexample).
# Part B (L3.1): (J0)-(J3) by numerical integration on a grid.
# Part C (L3.3, L3.4): the step bound on small-gain pairs, and Monte Carlo of U_Q/(n^-1/2 L^b), T1/((s0+1) n^-1/2 L^b0).
# A violation prints "VIOLATION". Usage: Rscript falsify_L2_L3.R [seed]
args <- commandArgs(TRUE); seed <- if (length(args) >= 1) as.integer(args[1]) else 20261111L
src <- sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)); source(file.path(dirname(src), "lem_common.R"))
set.seed(seed); viol <- 0L
bad <- function(...) { viol <<- viol + 1L; cat("VIOLATION", ..., "\n") }
make_design <- function(n, p, dtw) {            # every second column is a near-twin of its left neighbour
  X <- matrix(rnorm(n * p), n, p)
  for (j in seq(2, p, 2)) X[, j] <- X[, j - 1] + dtw * rnorm(n) / sqrt(n)
  std_cols(X)
}
res <- function(v, XT) if (ncol(XT)) qr.resid(qr(XT), v) else v
omega_n <- function(n, p) { tn <- 4 * log(2^24 * p * n); qn <- sqrt(2 * log(2^17 * p * n))
  qn / sqrt(n - 1) + (2 * sqrt((n - 1) * n^(1 / 3)) + 2 * n^(1 / 3) + tn) / (n - 1) }

cat("== Part A: toolkit under the unnormalised floor ==\n")
for (n in c(60, 240, 960, 3840)) for (dtw in c(1.5, 0.5)) {
  p <- 32; sigma <- 1; Xs <- make_design(n, p, dtw); theta <- numeric(p); theta[c(1, 5)] <- c(1.0, -0.7)
  mu <- as.numeric(Xs %*% theta); eps <- rnorm(n, 0, sigma); Y <- mu + eps - mean(eps); ys <- std_vec(Y)
  nu <- 0.01 + n / 2; cpr <- nu * log(sum(Y^2) / (n - 1)); Ce <- eps - mean(eps)
  gmin <- Inf; rho <- c(); RU <- c(); rssy_min <- Inf; e1 <- 0; e2 <- 0; idn <- 0; tke <- 0
  recs <- list()
  for (it in 1:400) {
    k <- sample(0:15, 1); blk <- sample(p, 16); U <- sort(blk[seq_len(k)]); l <- blk[16]
    XU <- Xs[, U, drop = FALSE]
    rU <- res(mu, XU); Lam <- sum(rU^2); tau2 <- sigma^2 + Lam / (n - 1); RSS <- sum(res(Y, XU)^2)
    PUe <- if (k) Ce - res(Ce, XU) else 0 * Ce
    idn <- max(idn, abs(RSS - (Lam + 2 * sum(rU * eps) + sum(Ce^2) - sum(PUe^2))) / RSS)        # (2.1)
    rho <- c(rho, RSS / ((n - 1) * tau2) - 1)
    lmU <- logm(Xs, ys, U); RUv <- lmU - cpr + 0.5 * k * log(n + 1) + nu * log(RSS); RU <- c(RU, RUv)
    rssy <- sum(res(ys, XU)^2); rssy_min <- min(rssy_min, rssy / n)
    if (k) { G <- crossprod(XU); ev <- eigen(G, symmetric = TRUE, only.values = TRUE)$values; g <- min(ev); gmin <- min(gmin, g)
      eta <- sum(log(((n + 1) * ev + 1) / (ev + 1))) - k * log(n + 1)
      if (eta > 1e-9 || eta < -k * log(1 + 1 / g) - 1e-9) bad("E1", n, dtw, eta, -k * log(1 + 1 / g))
      z <- crossprod(XU, ys); Qv <- sum(ys^2) - n * sum(z * solve((n + 1) * G + diag(k), z)); dq <- Qv - rssy
      if (dq < -1e-7 || dq > 1 + 1 / g + 1e-7) bad("E2", n, dtw, dq, 1 + 1 / g)
      e1 <- min(e1, eta / (k * log(1 + 1 / g))); e2 <- max(e2, dq / (1 + 1 / g)) }
    # one step U -> U + l
    xl <- res(Xs[, l], XU); u <- xl / sqrt(sum(xl^2)); delta <- sum(u * mu); Z <- sum(u * eps) / sigma
    XW <- Xs[, c(U, l), drop = FALSE]; RSSw <- sum(res(Y, XW)^2)
    tke <- max(tke, abs((RSS - RSSw) - (delta + sigma * Z)^2) / RSS * n)                        # (TK-e), scaled by n
    recs[[it]] <- c(k = k, RSS = RSS, RSSw = RSSw, tau2 = tau2, delta = delta, Z = Z,
                    tau2w = sigma^2 + sum(res(mu, XW)^2) / (n - 1), lstep = logm(Xs, ys, c(U, l)) - lmU)
  }
  R <- do.call(rbind, recs); cE <- rssy_min
  om <- max(abs(rho), abs(R[, "RSSw"] / ((n - 1) * R[, "tau2w"]) - 1))      # realised omega over ALL sets used (U and U + l)
  if (idn > 1e-10) bad("identity (2.1)", n, dtw, idn)
  if (tke > 1e-8) bad("identity (TK-e)", n, dtw, tke)
  k1 <- 0.51 * (1.02 + 1 / gmin) / cE; k2 <- 8 * log(1 + 1 / gmin)
  if (min(RU) < -k1 - 1e-6 || max(RU) > k2 + 1e-6) bad("R_U range", n, dtw, range(RU), -k1, k2)
  # (f1)-(f3) with the realised omega (they are deterministic given |rho| <= omega)
  dR <- R[, "RSS"] - R[, "RSSw"]; lhs <- nu * log(R[, "RSS"] / R[, "RSSw"]); th <- (n + 0.02) / ((n - 1) * (1 - om)) - 1
  if (any(lhs < dR / (2 * R[, "tau2"] * (1 + om)) - 1e-8)) bad("f1", n, dtw)
  if (any(lhs > (1 + th) * dR / (2 * R[, "tau2w"]) + 1e-8)) bad("f2", n, dtw)
  x <- dR / R[, "RSS"]; sm <- x <= 0.5
  if (any(lhs[sm] > ((1 + th) * (1 + x) * dR / (2 * R[, "tau2"]))[sm] + 1e-8)) bad("f3", n, dtw)
  # step remainder: log step + 1/2 log(n+1) - (delta + sigma Z)^2/(2 tau^2). L3.3 claims <= 2 kappa_E + 1 on the event,
  # for n >= n_2 and |Z| <= z_n; here it is an exploratory check with realised constants on small-mean-gain pairs.
  srem <- R[, "lstep"] + 0.5 * log(n + 1) - (R[, "delta"] + sigma * R[, "Z"])^2 / (2 * R[, "tau2"])
  g0 <- 3 * log(n) + 2 * log(4); smg <- R[, "delta"]^2 <= g0 * R[, "tau2"]
  if (any(srem[smg] > 2 * max(k1, k2) + 1 + 1e-8)) bad("L3.3 step", n, dtw)
  cat(sprintf("n=%4d twin-dist=%.1f: min lambda_min(G_U)=%.3f | (E1) eta/(k log(1+1/g)) min=%.3f (claim >= -1) | (E2) dq/(1+1/g) max=%.3f (claim <= 1) | max|rho_U|=%.4f, omega_n=%.3f, omega_n log n=%.2f | R_U in [%.3f, %.3f], bounds [-%.2f, %.2f] | step remainder max=%.3f (small-gain pairs: %d of %d) | (2.1) err=%.1e, (TK-e) err=%.1e\n",
              n, dtw, gmin, e1, e2, om, omega_n(n, p), omega_n(n, p) * log(n), min(RU), max(RU), k1, k2, max(srem[smg]), sum(smg), length(smg), idn, tke))
}

cat("== Part B: Lemma J on a grid (numerical integration) ==\n")
Jnum <- function(d, t, sigma, h) integrate(function(z) exp((d + sigma * z)^2 / (2 * t^2)) * dnorm(z), -h, h, rel.tol = 1e-10, subdivisions = 2000L)$value
nJ <- 0; rJ <- c(Inf, 0, 0)
for (sigma in c(0.3, 1, 2)) for (h in c(1, 1.5, 3, 6)) for (tr in c(1, 1.001, 1.2, 3)) for (dr in c(0, 0.2, -1, 2.5, 5)) {
  t <- tr * sigma; d <- dr * sigma; J <- Jnum(d, t, sigma, h); nJ <- nJ + 1
  j0 <- 0.25 * exp(d^2 / (2 * t^2)); if (J < j0 * (1 - 1e-8)) bad("J0", sigma, h, tr, dr)
  rJ[1] <- min(rJ[1], J / j0)
  if (tr > 1) { j1 <- t / sqrt(t^2 - sigma^2) * exp(d^2 / (2 * (t^2 - sigma^2))); if (J > j1 * (1 + 1e-8)) bad("J1", sigma, h, tr, dr); rJ[2] <- max(rJ[2], J / j1) }
  j2 <- sqrt(2 / pi) * h * exp(d^2 / (2 * t^2) + abs(d) * sigma * h / t^2); if (J > j2 * (1 + 1e-8)) bad("J2", sigma, h, tr, dr)
  rJ[3] <- max(rJ[3], J / j2)
  if (dr == 0 && tr == 1 && abs(J - sqrt(2 / pi) * h) > 1e-7) bad("J3", sigma, h)
}
cat(sprintf("%d grid points: min J/(J0 bound)=%.3f (claim >= 1); max J/(J1 bound)=%.3f, max J/(J2 bound)=%.3f (claims <= 1)\n", nJ, rJ[1], rJ[2], rJ[3]))

cat("== Part C: Monte Carlo of [LEAK]: U/(n^-1/2 L^b) and T1/((s0+1) n^-1/2 L^b0), Q = S0, default levels ==\n")
Jcf <- function(d, t, sigma, h) vapply(seq_along(d), function(i) Jnum(d[i], t[i], sigma, h), 0.0)
for (cfg in list(c(n = 120, p = 60, leak = 0), c(n = 480, p = 96, leak = 0), c(n = 480, p = 96, leak = 1))) {
  n <- cfg[["n"]]; p <- cfg[["p"]]; sigma <- 1; bs <- 6
  X <- matrix(rnorm(n * p), n, p)
  if (cfg[["leak"]] == 1) X[, 2] <- X[, 2] + 0.25 * X[, 1]          # null 2 shares block 1 with truth 1 and correlates with truth 7
  if (cfg[["leak"]] == 1) X[, 8] <- X[, 8] + 0.2 * X[, 7]
  Xs <- std_cols(X); S0 <- c(1, 7); theta <- numeric(p); theta[S0] <- c(0.6, -0.5); mu <- as.numeric(Xs %*% theta)
  blocks <- split(seq_len(p), ceiling(seq_len(p) / bs)); K <- min(p, n %/% 2); zn <- sqrt(2 * log(2^21 * p) + 2 * log(log(n)))
  # deterministic functionals L^b(S0), L^b0
  Lb <- 0; Lb0 <- 0
  for (Cb in blocks) { ust <- intersect(Cb, S0)
    for (l in setdiff(Cb, S0)) { others <- setdiff(Cb, c(l, ust)); best <- 0
      for (m in 0:(2^length(others) - 1)) { Tset <- c(ust, others[idx_of(m)]); XT <- Xs[, Tset, drop = FALSE]
        xl <- res(Xs[, l], XT); u <- xl / sqrt(sum(xl^2)); rT <- res(mu, XT); d <- sum(u * mu); t <- sqrt(sigma^2 + sum(rT^2) / (n - 1))
        J <- Jnum(d, t, sigma, zn); best <- max(best, J); if (m == 0) Lb0 <- Lb0 + J }
      Lb <- Lb + best } }
  Lb <- Lb / p; Lb0 <- Lb0 / p
  rU <- c(); rT <- c()
  for (it in 1:60) { eps <- rnorm(n, 0, sigma); ys <- std_vec(mu + eps)
    ltab <- lapply(blocks, function(Cb) block_table(Xs, ys, Cb))
    r <- start_enum_light <- NULL
    # U and T1 only (no enumeration over Omega: p is too large) -- same formulas as start_enum
    ml <- numeric(0); T1s <- 0
    for (b in seq_along(blocks)) { Cb <- blocks[[b]]; nb <- length(Cb); lt <- ltab[[b]]; LM <- 0:(2^nb - 1); ust <- mask_of(which(Cb %in% S0))
      for (i in seq_len(nb)) { if (Cb[i] %in% S0) next; bit <- bitwShiftL(1L, i - 1L)
        Ts <- LM[bitwAnd(LM, ust) == ust & bitwAnd(LM, bit) == 0L]
        ml <- c(ml, max(exp(lt[bitwOr(Ts, bit) + 1L] - lt[Ts + 1L]))); T1s <- T1s + exp(lt[bitwOr(ust, bit) + 1L] - lt[ust + 1L]) } }
    Uv <- sum(ml) / p; T1 <- (length(S0) + 1) / (2 * p - 1 - length(S0)) * T1s
    rU <- c(rU, Uv / (Lb / sqrt(n))); rT <- c(rT, T1 / ((length(S0) + 1) * Lb0 / sqrt(n))) }
  cat(sprintf("n=%d p=%d leak=%d: L^b=%.2f L^b0=%.2f (z_n=%.2f) | U/(n^-1/2 L^b): median %.3f, 90%% %.3f, max %.3f | T1/((s0+1) n^-1/2 L^b0): median %.3f, 90%% %.3f, max %.3f  (claim: O_P(1); Markov tail c/lambda)\n",
              n, p, cfg[["leak"]], Lb, Lb0, zn, median(rU), quantile(rU, .9), max(rU), median(rT), quantile(rT, .9), max(rT)))
}
cat("TOTAL VIOLATIONS:", viol, "\n")
