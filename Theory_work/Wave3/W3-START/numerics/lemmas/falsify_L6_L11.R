# falsify_L6_L11.R -- falsification attempt for lemmas/L7_NEC.md, L9_BR.md, L10_INTERFACES.md, L11_EXAMPLES.md
# (and the two analytic facts of L6 that are cheap to test). Base R. FALSIFICATION ATTEMPTS, never proofs.
# Part A (L9): Gaussian rows with a known Sigma. For random (l, U0, V): asserted identities
#   A1  J_n(delta_{U,l}, tau_U) = F(g_{U,l}, a_U)                       (L9.3)
#   A2  rho_U = (z0 - a'R^-1 d)/sqrt((1 - a'R^-1 a)(1 - d'R^-1 d)),  Delta_U = Delta_U0 (1 - d'R^-1 d)   (L9.4)
#   A3  g^2 = N (xi + d0)^2/((xi + d0)^2 + R) with xi, d0, R built from the POPULATION regression of W_l on W_D   (9.1)
#   A4  the one-dimensional Gaussian identity behind L9.5, its exact value at d0 = 0, eta = 0, and closed form <= Phi_n
#   A5  (F1) monotone in |g|; (F2) comparison inequality on a grid
# Part B (L7): (C2)(i) and (ii) on orthogonal designs with one leaking null / one weak truth. Asserted: the
#   leaking-null (f1) chain with the realised RSS envelope and the exact score remainder. Printed: competing-odds
#   exponents for both cases. The weak-truth (f3) chain and the uniform constants are not asserted.
# Part C (L10): Proposition OVL, step (iii): realised log m_l / log n against (a_l - 1)/2 (printed), and (10.1).
# Part D (L11): the quantities claimed for examples F-2, F-3, G-2 at concrete n (asserted).
# A violation prints "VIOLATION". Usage: Rscript falsify_L6_L11.R [seed]
args <- commandArgs(TRUE); seed <- if (length(args) >= 1) as.integer(args[1]) else 20261111L
src <- sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)); source(file.path(dirname(src), "lem_common.R"))
set.seed(seed); viol <- 0L
bad <- function(...) { viol <<- viol + 1L; cat("VIOLATION", ..., "\n") }
res <- function(v, XT) if (ncol(XT)) qr.resid(qr(XT), v) else v
Jnum <- function(d, t, sigma, h) integrate(function(z) exp((d + sigma * z)^2 / (2 * t^2)) * dnorm(z), -h, h, rel.tol = 1e-10, subdivisions = 2000L)$value
Fga <- function(g, a, zn) integrate(function(z) exp((sqrt(1 - a) * g + sqrt(a) * z)^2 / 2) * dnorm(z), -zn, zn, rel.tol = 1e-10, subdivisions = 2000L)$value

cat("== Part A: Gaussian-row bridge, identities ==\n")
errA <- c(A1 = 0, A2r = 0, A2d = 0, A3 = 0, A4 = 0); nA <- 0
for (rep in 1:60) {
  n <- sample(c(60, 200, 600), 1); N <- n - 1; p <- 24; sigma <- 1; S0 <- c(1, 2)
  # population covariance: AR(1) blocks of size 6 with random rho (unit diagonal), so partial covariances are non-trivial
  Sig <- diag(p); for (b in 0:3) { r <- runif(1, 0.1, 0.7); idx <- b * 6 + 1:6; Sig[idx, idx] <- r^abs(outer(1:6, 1:6, "-")) }
  mvec <- rnorm(p); W <- matrix(rnorm(n * p), n, p) %*% chol(Sig) + rep(mvec, each = n)
  Xs <- std_cols(W); theta <- numeric(p); theta[S0] <- c(0.8, -0.6); mu <- as.numeric(Xs %*% theta)
  zn <- sqrt(2 * log(2^21 * p) + 2 * log(log(n)))
  l <- sample(setdiff(1:p, S0), 1); pool <- setdiff(1:p, l)
  U0 <- sort(sample(pool, sample(0:3, 1))); if (all(S0 %in% U0)) U0 <- setdiff(U0, 1)
  V <- sort(sample(setdiff(pool, c(U0, S0)), sample(1:2, 1))); U <- sort(c(U0, V)); nA <- nA + 1
  pc <- function(u, w, Uset) { XU <- Xs[, Uset, drop = FALSE]; ru <- res(u, XU); rw <- res(w, XU); sum(ru * rw) / sqrt(sum(ru^2) * sum(rw^2)) }
  # A1
  XU <- Xs[, U, drop = FALSE]; xl <- res(Xs[, l], XU); rmu <- res(mu, XU); u <- xl / sqrt(sum(xl^2))
  delta <- sum(u * mu); DeltaU <- sum(rmu^2) / N; tau <- sqrt(sigma^2 + DeltaU); aU <- sigma^2 / tau^2
  gU <- sqrt(N) * pc(Xs[, l], mu, U)
  errA["A1"] <- max(errA["A1"], abs(Jnum(delta, tau, sigma, zn) / Fga(gU, aU, zn) - 1))
  # A2
  X0 <- Xs[, U0, drop = FALSE]; xt <- res(Xs[, l], X0); mt <- res(mu, X0); XV <- apply(Xs[, V, drop = FALSE], 2, res, XT = X0)
  z0 <- sum(xt * mt) / sqrt(sum(xt^2) * sum(mt^2)); nv <- sqrt(colSums(XV^2))
  av <- as.numeric(crossprod(XV, xt)) / (nv * sqrt(sum(xt^2))); dv <- as.numeric(crossprod(XV, mt)) / (nv * sqrt(sum(mt^2)))
  R <- crossprod(XV) / outer(nv, nv); Ri <- solve(R)
  rhoF <- (z0 - sum(av * (Ri %*% dv))) / sqrt((1 - sum(av * (Ri %*% av))) * (1 - sum(dv * (Ri %*% dv))))
  errA["A2r"] <- max(errA["A2r"], abs(rhoF - gU / sqrt(N)))
  errA["A2d"] <- max(errA["A2d"], abs(DeltaU / (sum(mt^2) / N * (1 - sum(dv * (Ri %*% dv)))) - 1))
  # A3: population regression of W_l on W_D, D = U0 + S0
  D <- sort(union(U0, S0)); gam <- solve(Sig[D, D], Sig[D, l]); e <- (W[, l] - mvec[l]) - sweep(W[, D, drop = FALSE], 2, mvec[D]) %*% gam
  taue <- sqrt(Sig[l, l] - sum(Sig[l, D] * gam))
  Ce <- e - mean(e); et <- res(Ce, X0)                                   # Pi e
  g2 <- gam[match(setdiff(S0, U0), D)]; WS <- W[, setdiff(S0, U0), drop = FALSE]
  m <- res(sweep(WS, 2, colMeans(WS)) %*% g2, X0)                         # Pi W_{S0 - U0} gamma^2
  v <- mt / sqrt(sum(mt^2)); xi <- sum(et * v) / taue; d0 <- sum(m * v) / taue
  w <- m + et; Rr <- (sum(w^2) - sum(w * v)^2) / taue^2
  g0 <- sqrt(N) * z0
  errA["A3"] <- max(errA["A3"], abs(g0^2 - N * (xi + d0)^2 / ((xi + d0)^2 + Rr)) / (1 + g0^2))
  # the centred column l must equal (m + e-tilde) up to the U0-part: check (I - P_U0) C W_l = m + Pi e
  if (max(abs(res(W[, l] - mean(W[, l]), X0) - (m + et))) > 1e-7) bad("A3 decomposition", rep)
}
# A4: (i) the one-dimensional Gaussian identity used in L9.5, E_xi exp((s xi + c)^2/2) = (1 - s^2)^(-1/2) exp(c^2/(2(1 - s^2)))
#     (the double integral then follows by Fubini); (ii) the resulting closed form against the bound Phi_n.
for (s2 in c(0.1, 0.5, 0.8, 0.95)) for (cc0 in c(0, 0.7, -3, 6)) { s <- sqrt(s2); mm <- s * cc0 / (1 - s2); sd <- 1 / sqrt(1 - s2)
  lhs <- integrate(function(x) exp((s * x + cc0)^2 / 2 - x^2 / 2 - cc0^2 / (2 * (1 - s2))) / sqrt(2 * pi), mm - 12 * sd, mm + 12 * sd, rel.tol = 1e-11)$value
  errA["A4"] <- max(errA["A4"], abs(lhs * sqrt(1 - s2) - 1)) }           # both sides divided by exp(c^2/(2(1 - s^2)))
for (a in c(0.2, 0.5, 0.9)) for (d0 in c(0, 0.7, -2)) for (eta in c(0, 0.01, 0.05)) if (eta <= a / 2) { zn <- 6.5
  s2 <- (1 - a) / (1 - eta); s <- sqrt(s2); r <- sqrt(a)
  cf <- (1 - s2)^(-1/2) * integrate(function(z) exp((s * d0 + r * z)^2 / (2 * (1 - s2)) - z^2 / 2) / sqrt(2 * pi), -zn, zn, rel.tol = 1e-10)$value
  Phi <- sqrt(2 / a) * sqrt(2 / pi) * zn * exp(eta * zn^2 / a + 2 * abs(d0) * zn / a + d0^2 / a)
  if (cf > Phi * (1 + 1e-8)) bad("A4 Phi bound", a, d0, eta)
  if (d0 == 0 && eta == 0 && abs(cf / (a^(-1/2) * sqrt(2 / pi) * zn) - 1) > 1e-8) bad("A4 exact value at d0 = 0", a) }
# A5
for (a in c(0.2, 0.6)) { zn <- 6; gs <- seq(0, 6, 0.5); Fv <- vapply(gs, Fga, 0.0, a = a, zn = zn)
  if (any(diff(Fv) < -1e-9 * Fv[-1])) bad("F1 monotone", a)
  alo <- 0.15; ahi <- 0.7; La <- 1 / (2 * sqrt(min(alo, 1 - ahi))); G <- 6
  for (k in 1:40) { g <- runif(1, -G, G); g2 <- max(-G, min(G, g + rnorm(1, 0, 0.05))); a1 <- runif(1, alo, ahi); a2 <- max(alo, min(ahi, a1 + rnorm(1, 0, 0.01)))
    eta <- abs(g2 - g) + La * (G + zn) * abs(a2 - a1)
    if (Fga(g2, a2, zn) > exp(eta * (G + zn + eta)) * Fga(g, a1, zn) * (1 + 1e-8)) bad("F2", g, g2, a1, a2) } }
if (errA["A1"] > 1e-6 || errA["A2r"] > 1e-9 || errA["A2d"] > 1e-9 || errA["A3"] > 1e-8 || errA["A4"] > 1e-8) bad("Part A identity error", errA)
cat(sprintf("%d random (l, U0, V): max relative errors  A1 %.1e | A2 rho %.1e, Delta %.1e | A3 %.1e | A4 %.1e\n", nA, errA["A1"], errA["A2r"], errA["A2d"], errA["A3"], errA["A4"]))

cat("== Part B: (C2)(i), (ii) on orthogonal designs ==\n")
ortho <- function(n, p) { Q <- qr.Q(qr(scale(matrix(rnorm(n * p), n, p), scale = FALSE))); Q * sqrt(n - 1) }   # centred, e_i'e_j = (n-1) delta_ij
for (n in c(200, 800, 3200)) for (case in c("leak", "weak")) {
  p <- 40; N <- n - 1; sigma <- 1; E <- ortho(n, p); A <- log(p) / log(n); bs <- 4; blocks <- split(1:p, ceiling((1:p) / bs))
  ex <- c()
  for (it in 1:20) {
    if (case == "leak") { cc <- 1 + 2 * A + 1.5; th <- 1; rho <- sqrt(cc * (sigma^2 + th^2) * log(n) / (N * th^2))
      # truth e1 in block 1; null x5 in block 2 correlated with e1. U*_b(5) = empty: delta^2 = rho^2 N th^2 and
      # tau_empty^2 = sigma^2 + th^2, so the normalised level delta^2/(tau^2 log n) is exactly cc
      X <- E; X[, 5] <- rho * E[, 1] + sqrt(1 - rho^2) * E[, 5]; S0 <- 1; theta <- numeric(p); theta[1] <- th
    } else { cc <- 1 + 2 * A - 1.2; X <- E; S0 <- c(1, 6); theta <- numeric(p); theta[1] <- 1
      theta[6] <- sqrt(cc * (sigma^2 + 1) * log(n) / (N - cc * log(n))) }   # level of truth 6 given U = empty: theta6^2 N/((sigma^2 + 1 + theta6^2) log n) = cc
    mu <- as.numeric(X %*% theta); eps <- rnorm(n, 0, sigma); Y <- mu + eps - mean(eps); ys <- std_vec(Y); nu <- 0.01 + n / 2
    if (case == "leak") { b <- 2; Cb <- blocks[[b]]; lt <- block_table(X, ys, Cb); iL <- which(Cb == 5)
      lr <- lt[bitwShiftL(1L, iL - 1L) + 1L] - lt[1]                                    # log r_b({l}) - log r_b(empty), U*_b = empty
      RSS0 <- sum(Y^2); RSS1 <- sum(res(Y, X[, 5, drop = FALSE])^2); tau2 <- sigma^2 + sum(mu^2) / N; om <- abs(RSS0 / (N * tau2) - 1)
      RU <- lt + 0.5 * popc(0:(2^length(Cb) - 1)) * log(n + 1); Rdiff <- (RU[bitwShiftL(1L, iL - 1L) + 1L] + nu * log(RSS1)) - (RU[1] + nu * log(RSS0))
      lower <- -0.5 * log(n + 1) + (RSS0 - RSS1) / (2 * tau2 * (1 + om)) + Rdiff
      if (lr < lower - 1e-7) bad("C2(i) chain", n)
      ex <- c(ex, (log((length(S0) + 1) / (2 * p - 1 - length(S0))) + lr) / log(n))      # exponent of gamma0(S0+l)/gamma0(S0)
    } else { b <- 2; Cb <- blocks[[b]]; lt <- block_table(X, ys, Cb); iJ <- which(Cb == 6)   # U*_b = {6}, U = empty
      lr <- lt[1] - lt[bitwShiftL(1L, iJ - 1L) + 1L]
      ex <- c(ex, (log((2 * p - length(S0)) / length(S0)) + lr) / log(n)) }
  }
  target <- if (case == "leak") (cc - 1 - 2 * A) / 2 else (1 + 2 * A - cc) / 2
  cat(sprintf("n=%4d %s: level c=%.2f (1+2A=%.2f): exponent of the competing model's odds: median %.2f, min %.2f; limit value %.2f (claim: pi0(S0) <= n^-kappa' w.p.->1 for kappa' below it)\n",
              n, case, cc, 1 + 2 * A, median(ex), min(ex), target))
}

cat("== Part C: Proposition OVL, one leaking null in Q ==\n")
for (n in c(200, 800, 3200)) { p <- 12; N <- n - 1; sigma <- 1; E <- ortho(n, p); al <- 2.0; th <- 1
  rho <- sqrt(al * (sigma^2 + th^2) * log(n) / (N * th^2))     # level delta^2/(tau^2 log n) = al for every U not containing the truth
  X <- E; X[, 7] <- rho * E[, 1] + sqrt(1 - rho^2) * E[, 7]; S0 <- 1; Q <- c(1, 7); theta <- numeric(p); theta[1] <- th
  blocks <- list(1:6, 7:12); K <- min(p, n %/% 2); mu <- as.numeric(X %*% theta); ml <- c(); ok <- 0; tot <- 0
  for (it in 1:30) { ys <- std_vec(mu + rnorm(n, 0, sigma)); ltab <- lapply(blocks, function(Cb) block_table(X, ys, Cb))
    r <- start_enum(p, blocks, ltab, K, S0, Q)
    if (r$UQ < 1) { tot <- tot + 1; rhs <- (1 + r$en)^1 * (1 - r$UQ)^(-(length(Q) + 1)) * (1 + length(Q) * r$ml[7] / p)
      if (1 / r$pi0 > rhs * (1 + 1e-9)) bad("OVL (10.1)", n) else ok <- ok + 1 }
    ml <- c(ml, log(r$ml[7]) / log(n)) }
  cat(sprintf("n=%4d: leaking null in Q at level a_l=%.1f: log m_l/log n median %.2f, max %.2f (limit (a_l-1)/2 = %.2f); (10.1) held in %d of %d draws\n",
              n, al, median(ml), max(ml), (al - 1) / 2, ok, tot)) }

cat("== Part D: examples of L11 ==\n")
n <- 400; N <- n - 1; A <- 1; p <- n - 1; sigma <- 1; rho2 <- 0.4; rho <- sqrt(rho2); cc <- 2 * (1 + 2 * A)
E <- ortho(n, 40)                                  # only the first columns are needed for the checks
X <- E; for (l in 2:16) X[, l] <- rho * E[, 1] + sqrt(1 - rho2) * E[, l]
th1 <- sigma * sqrt(cc * log(n) / N); mu <- th1 * E[, 1]
qk <- function(k) if (k == 0) 1 else (1 - rho2) / (1 + (k - 1) * rho2)
for (it in 1:200) { k <- sample(0:15, 1); Nset <- c(if (k) sample(2:16, k), sample(17:40, sample(0:3, 1)))
  if (length(Nset) > 15) Nset <- Nset[1:15]; k <- sum(Nset <= 16)
  Lam <- sum(res(mu, X[, Nset, drop = FALSE])^2)
  if (abs(Lam / (cc * sigma^2 * log(n) * qk(k)) - 1) > 1e-8) bad("F-2 Lambda_N formula", k) }
G16 <- crossprod(X[, 1:16]) / N; gB <- min(eigen(G16, symmetric = TRUE, only.values = TRUE)$values)
if (gB <= 0) bad("F-2 Gram floor")
cm <- (1 + 2 * A) / 6; tau2max <- sigma^2 * (1 + cc * log(n) / N)
m0 <- cc * log(n) / (1 + cc * log(n) / N) / log(n) - (1 + 2 * A + cm); m1 <- cc * qk(15) / (1 + cc * log(n) / N) - cm
lev_vc <- cc * qk(15)                                # (V-c) level at U = {2..16}, upper bound
gain_leak <- max(vapply(0:14, function(k) qk(k) - qk(k + 1), 0.0)) * cc     # largest normalised gain of a correlate
zn <- sqrt(2 * log(2^21 * p) + 2 * log(log(n))); d <- rho * th1 * sqrt(N); t <- sqrt(tau2max)
Jdef <- Jnum(d, t, sigma, zn); Jlow <- (2 * pi)^(-1/2) * exp(d^2 / (2 * t^2) + d * sigma * (zn - 1) / t^2 - (1 - sigma^2 / t^2) * zn^2 / 2)
if (Jdef < Jlow * (1 - 1e-8)) bad("F-2 lower bound on J")
hF4 <- min(zn, sqrt(4 * log(log(n)))); JF4 <- Jnum(d, t, sigma, hF4)
if (m0 < 0 || m1 < 0) cat("  (note: (V-m) margins at n =", n, "are", signif(m0, 3), signif(m1, 3), "- asymptotic claim, n large)\n")
if (lev_vc >= 1 + 2 * A) bad("F-2 (V-c) should fail"); if (gain_leak > 0.4 * cc + 1e-12) bad("F-2 leak level")
cat(sprintf("F-2 at n=%d, A=%g: lambda_min(B'B)=%.3f | (V-m) margins: N empty %.3f, N nonempty %.3f (claim >= 0 for n large) | (V-c) level at the 15 correlates %.2f < 1+2A=%.0f | largest correlate gain %.2f <= 0.4c=%.2f < 1+2A | per-column charge n^-1/2 p^-1 J: default levels %.2e, F4 levels %.2e\n",
            n, A, gB, m0, m1, lev_vc, 1 + 2 * A, gain_leak, 0.4 * cc, Jdef / (sqrt(n) * p), JF4 / (sqrt(n) * p)))
for (nn in c(1e4, 1e6, 1e9)) { pp <- nn - 1; z <- sqrt(2 * log(2^21 * pp) + 2 * log(log(nn))); dd <- sqrt(0.4 * cc * log(nn)); tt <- sqrt(1 + cc * log(nn) / (nn - 1))
  lJ <- dd^2 / (2 * tt^2) + dd * (z - 1) / tt^2 - (1 - 1 / tt^2) * z^2 / 2 - 0.5 * log(2 * pi)      # log of the lower bound (sigma = 1)
  h4 <- min(z, sqrt(4 * log(log(nn)))); lJ4 <- log(sqrt(2 / pi) * h4) + dd^2 / (2 * tt^2) + dd * h4 / tt^2   # log of the (J2) upper bound
  cat(sprintf("  n=%.0e (p=n-1): log_n of the charge of one correlate in rho_n: default levels >= %.2f (diverges), F4 levels <= %.2f (limit -0.3)\n",
              nn, (lJ - 0.5 * log(nn) - log(pp)) / log(nn), (lJ4 - 0.5 * log(nn) - log(pp)) / log(nn))) }
# F-3
dd <- 1.2; cphi <- 1 - dd^2 / (2 * N); T2 <- cbind(E[, 2], cphi * E[, 2] + sqrt(1 - cphi^2) * E[, 3]); ev <- eigen(crossprod(T2), symmetric = TRUE, only.values = TRUE)$values
if (abs(min(ev) - dd^2 / 2) > 1e-6 || abs(sqrt(sum((T2[, 1] - T2[, 2])^2)) - dd) > 1e-8) bad("F-3 twin Gram")
cat(sprintf("F-3: twin pair at distance %.1f: lambda_min(X_T'X_T)=%.4f (= d^2/2 = %.4f), normalised %.2e\n", dd, min(ev), dd^2 / 2, min(ev) / N))
# G-2: block-diagonal Sigma: population partial covariances across groups vanish
gsz <- 3; pg <- 12; Sig <- diag(pg); for (b in 0:3) { idx <- b * gsz + 1:gsz; M <- matrix(runif(gsz^2, -1, 1), gsz); S <- crossprod(M) + diag(gsz); Dg <- diag(1 / sqrt(diag(S))); Sig[idx, idx] <- Dg %*% S %*% Dg }
pcov <- function(j, k, U) if (length(U)) Sig[j, k] - Sig[j, U, drop = FALSE] %*% solve(Sig[U, U], Sig[U, k, drop = FALSE]) else Sig[j, k]
mx <- 0; for (it in 1:300) { l <- sample(4:12, 1); j <- 1; U <- sample(setdiff(1:12, c(l, j)), sample(0:5, 1)); if ((l - 1) %/% gsz != (j - 1) %/% gsz) mx <- max(mx, abs(pcov(l, j, U))) }
if (mx > 1e-10) bad("G-2 partial covariance across groups"); cat(sprintf("G-2: max |Cov(W_l, W_j | W_U)| across groups over 300 draws = %.1e (claim 0)\n", mx))
cat("TOTAL VIOLATIONS:", viol, "\n")
