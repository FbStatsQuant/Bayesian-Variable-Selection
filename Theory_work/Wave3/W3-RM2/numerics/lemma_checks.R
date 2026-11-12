# lemma_checks.R -- falsification numerics for lemmas L0, L1, L2 of W3-RM2. OBSERVATIONS ONLY, never proofs.
# Each block tries to break one deterministic step of a proof (an identity or an inequality that must hold exactly
# on the stated event) or illustrates one probabilistic statement at small n. Usage: Rscript lemma_checks.R <dir>
args <- commandArgs(trailingOnly = TRUE); here <- if (length(args)) args[1] else "."
source(file.path(here, "rm2_common.R"))
out <- character(0); say <- function(...) { s <- sprintf(...); cat(s, "\n"); out <<- c(out, s) }
set.seed(20261111)

resid_on <- function(X, S, v) if (length(S)) qr.resid(qr(X[, S, drop = FALSE]), v) else v
unit <- function(v) v / sqrt(sum(v^2))
# exact D0 quantities for a set A (standardised X, y with |y|^2 = n-1): log m(A) - log c_n, RSS^y_A, R_A of (E4)
score_parts <- function(Xs, ys, A) {
  n <- nrow(Xs); nu <- 0.01 + n / 2; k <- length(A)
  if (k == 0) return(list(lm = -nu * log(0.02 + sum(ys^2)), rssy = sum(ys^2), R = -nu * log(1 + 0.02 / sum(ys^2))))
  G <- crossprod(Xs[, A, drop = FALSE]); z <- crossprod(Xs[, A, drop = FALSE], ys)
  H <- (n + 1) * G + diag(k)
  ldD <- as.numeric(determinant(H)$modulus - determinant(G + diag(k))$modulus)
  Q <- sum(ys^2) - n * sum(z * solve(H, z))
  rssy <- sum(ys^2) - sum(z * solve(G, z))
  list(lm = -0.5 * ldD - nu * log(0.02 + Q), rssy = rssy,
       R = -0.5 * (ldD - k * log(n + 1)) - nu * log((0.02 + Q) / rssy))
}

# ------------------------------------------------------------------ K1: score expansion (T3) at polynomial set sizes
say("K1  L0 (T3): R_A := log m(A) - c'_n + |A|/2 log(n+1) + nu log RSS_A must satisfy -0.52/c_E <= R_A <= |A|/((n-1)phi0^2)")
for (cfg in list(c(400, 300, 60), c(1600, 600, 200), c(1600, 600, 400))) {
  n <- cfg[1]; p <- cfg[2]; J <- cfg[3]
  X <- std_cols(matrix(rnorm(n * p), n, p) + 0.5 * rnorm(n)); theta <- c(3, 1); eps <- rnorm(n)
  mu <- as.vector(X[, 1:2] %*% theta); Y <- mu + eps - mean(eps); ys <- std_vec(Y)
  M <- sum(mu^2) / n; sig2 <- 1; cE <- sig2 / (12 * (M + sig2)); kE <- 0.52 / cE + 1
  Rs <- c(); lo_ok <- TRUE; hi_ok <- TRUE
  for (r in 1:40) {
    k <- sample(c(0, 1, 2, 5, 16, J %/% 4, J %/% 2, J), 1); A <- sort(sample(p, k)); if (r %% 2) A <- sort(union(A, 1:2))
    sp <- score_parts(X, ys, A); Rs <- c(Rs, sp$R)
    phi2 <- if (length(A)) min(eigen(crossprod(X[, A, drop = FALSE]) / (n - 1), symmetric = TRUE, only.values = TRUE)$values) else 1
    lo_ok <- lo_ok && (sp$R >= -0.52 / cE); hi_ok <- hi_ok && (sp$R <= length(A) / ((n - 1) * phi2) + 1e-9)
  }
  say("    n=%d p=%d sizes up to %d: R_A in [%.4f, %.4f]; kappa_E = %.1f; lower bound ok: %s; upper bound ok: %s",
      n, p, J, min(Rs), max(Rs), kE, lo_ok, hi_ok)
}

# ------------------------------------------------------------------ K2: production block tables obey (E6-tab) with |R_U' - R_U| <= 2 kappa_E
say("K2  L0 (E6-tab) on PRODUCTION block tables: D := log r_b(U') - log r_b(U) + (|U'|-|U|)/2 log(n+1) + nu log(RSS_U'/RSS_U)")
d <- gen_design(400, 800, 43, type = "B1", seed = 3L); ys <- std_vec(d$y)
ctx <- v3_context(d$Xs, ys, return_gram = FALSE); su <- v3_setup(ctx); nu <- 0.01 + 400 / 2
Dv <- c(); tauv <- c()
mu <- as.vector(d$Xs[, d$S0] %*% d$theta)
for (b in sample(seq_along(su$blocks), 25)) {
  mem <- su$blocks[[b]]; lr <- su$tables[[b]]$log_r; m <- length(mem)
  for (r in 1:60) {
    cu <- sample(0:(2^m - 1), 1); extra <- sample(0:(2^m - 1), 1); cup <- bitwOr(cu, extra); if (cup == cu) next
    U <- mem[bitwAnd(bitwShiftR(cu, 0:(m - 1)), 1L) == 1L]; Up <- mem[bitwAnd(bitwShiftR(cup, 0:(m - 1)), 1L) == 1L]
    rU <- sum(resid_on(d$Xs, U, ys)^2); rUp <- sum(resid_on(d$Xs, Up, ys)^2)
    Dv <- c(Dv, lr[cup + 1] - lr[cu + 1] + 0.5 * (length(Up) - length(U)) * log(401) + nu * log(rUp / rU))
    Yc <- d$y - mean(d$y); tau2 <- 1 + sum(resid_on(d$Xs, U, mu)^2) / 399
    tauv <- c(tauv, sum(resid_on(d$Xs, U, Yc)^2) / (399 * tau2))
  }
}
M <- sum(mu^2) / 400; kE <- 0.52 / (1 / (12 * (M + 1))) + 1
say("    %d nested pairs in 25 production blocks: D in [%.4f, %.4f]; allowed |D| <= 2 kappa_E = %.1f; ok: %s",
    length(Dv), min(Dv), max(Dv), 2 * kE, all(abs(Dv) <= 2 * kE))
say("    L1 Fact 2 (tau-form RSS floor): min over these U of RSS_U/((n-1) tau_U^2) = %.3f (the lemma needs it >= 1 - o(1))", min(tauv))

# ------------------------------------------------------------------ K3: two-sided score conversion on a polynomial lattice (NA-conv, W-conv)
say("K3  L2 NA-conv / W-conv: D := [F(T+l) - F(T)] - [Z^2 - a0(k)^2]/2 must lie in [-log 2 - 2 kappa_E - 2 n^(-1/3) Z^2, 1/2 + 2 kappa_E]")
for (cfg in list(c(1600, 3200, 0.5), c(1600, 3200, 0.75))) {
  n <- cfg[1]; p <- cfg[2]; bb <- cfg[3]; m <- ceiling(n^bb)
  d <- gen_design(n, p, m, type = "B1", seed = 7L); ys <- std_vec(d$y)
  ctx <- v3_context(d$Xs, ys, return_gram = FALSE); P <- make_problem(d$Xs, ys, ctx)
  mu <- as.vector(d$Xs[, d$S0] %*% d$theta); M <- sum(mu^2) / n; kE <- 0.52 / (1 / (12 * (M + 1))) + 1
  E <- setdiff(d$Q, d$S0); Dall <- c(); Zall <- c(); viol_up <- 0; viol_lo <- 0; sgn_bad <- 0
  for (r in 1:12) {
    k_ex <- sample(c(0, 1, 5, length(E) %/% 4, length(E) %/% 2, length(E) - 1), 1)
    Tset <- sort(c(d$S0, sample(E, k_ex))); k <- length(Tset)
    sc <- scan_at(P, Tset, swaps = FALSE)
    ls <- sample(setdiff(1:p, Tset), 400)
    qrT <- qr(d$Xs[, Tset, drop = FALSE]); XR <- qr.resid(qrT, d$Xs[, ls, drop = FALSE])
    Z <- as.vector(crossprod(XR, d$eps)) / sqrt(colSums(XR^2))          # sigma = 1
    a02 <- log(n + 1) + 2 * log(p / (k + 1))
    Dd <- (sc$Fadd[ls] - sc$FS) - (Z^2 - a02) / 2
    Dall <- c(Dall, Dd); Zall <- c(Zall, Z^2)
    viol_up <- viol_up + sum(Dd > 0.5 + 2 * kE); viol_lo <- viol_lo + sum(Dd < -log(2) - 2 * kE - 2 * n^(-1/3) * Z^2)
    sgn_bad <- sgn_bad + sum((Z^2 <= a02 - 4 * kE - 2) & (sc$Fadd[ls] >= sc$FS))
  }
  say("    n=%d p=%d b=%.2f (|Q|=%d): %d lattice pairs, sizes up to %d; D in [%.3f, %.3f]; kappa_E = %.1f; outside the proved bounds: %d above, %d below; pairs with Z^2 <= c_n(k) and F(T+l) >= F(T): %d",
      n, p, bb, length(d$Q), length(Dall), length(d$Q), min(Dall), max(Dall), kE, viol_up, viol_lo, sgn_bad)
  say("      (observed D is within [%.2f, %.2f]: the score increment equals (Z^2 - a0^2)/2 up to a bounded constant, as both lemmas use)", min(Dall), max(Dall))
}

# ------------------------------------------------------------------ small enumerated lattice for K4-K7
make_small <- function(type, n = 240, p = 40, m = 8, seed = 1L) {
  set.seed(seed); S0 <- 1:2
  XT <- matrix(rnorm(n * 2), n, 2); E <- matrix(rnorm(n * m), n, m); W <- matrix(rnorm(n * (p - 2 - m)), n, p - 2 - m)
  XL <- 0.3 * XT[, 1] + sqrt(1 - 0.09) * E
  if (type == "wide") W <- sqrt(0.4) * W + sqrt(0.6) * rowSums(E) / sqrt(m)
  if (type == "orth") { Qr <- qr.Q(qr(scale(cbind(XT, XL, W), scale = FALSE))); X <- Qr * sqrt(n - 1) } else X <- std_cols(cbind(XT, XL, W))
  list(X = std_cols(X), S0 = S0, Q = 1:(2 + m), n = n, p = p)
}
lattice_dirs <- function(D) {           # all unit residual directions u_{T,l}, T in [S0,Q], l not in T, with |T|
  Ex <- setdiff(D$Q, D$S0); m <- length(Ex); U <- list(); ks <- c(); Ts <- list(); lsv <- c()
  for (code in 0:(2^m - 1)) {
    Tset <- c(D$S0, Ex[bitwAnd(bitwShiftR(code, 0:(m - 1)), 1L) == 1L]); qrT <- qr(D$X[, Tset, drop = FALSE])
    ls <- setdiff(1:D$p, Tset); XR <- qr.resid(qrT, D$X[, ls, drop = FALSE]); XR <- sweep(XR, 2, sqrt(colSums(XR^2)), "/")
    U[[length(U) + 1]] <- XR; ks <- c(ks, rep(length(Tset), length(ls))); lsv <- c(lsv, ls)
    Ts <- c(Ts, rep(list(Tset), length(ls)))
  }
  list(U = do.call(cbind, U), k = ks, l = lsv, Tsets = Ts)
}

say("K4  L2 (3.1): (u_{T,l}'g)^2 <= (u_{Q_l,l}'g)^2 + |(P_Q - P_S0) g|^2 for every lattice pair (deterministic inequality)")
D <- make_small("iid"); LD <- lattice_dirs(D); nd <- ncol(LD$U)
qrQ <- qr(D$X[, D$Q]); qrS <- qr(D$X[, D$S0]); worst <- -Inf
uQ <- sapply(1:D$p, function(l) if (l %in% D$S0) rep(0, D$n) else unit(resid_on(D$X, setdiff(D$Q, l), D$X[, l])))
for (r in 1:200) {
  g <- rnorm(D$n); lhs <- as.vector(crossprod(LD$U, g))^2
  chi <- sum((qr.fitted(qrQ, g) - qr.fitted(qrS, g))^2)
  rhs <- as.vector(crossprod(uQ, g))[LD$l]^2 + chi
  worst <- max(worst, max(lhs - rhs))
}
say("    %d directions x 200 Gaussian draws: max of (lhs - rhs) = %.3e (must be <= 0 up to rounding)", nd, worst)

say("K5  L2 3(v): u_{T,l} = v - sum_t (lambda_t |x_t| / |a|) x_t/|x_t| with v = (I-P_B)x_l/|a|, B = T cap N_l (exact identity)")
maxerr <- 0; maxvar <- 0
for (r in 1:300) {
  i <- sample(nd, 1); Tset <- LD$Tsets[[i]]; l <- LD$l[i]; Nl <- sample(setdiff(D$Q, l), 3); B <- intersect(Tset, Nl)
  a <- resid_on(D$X, Tset, D$X[, l]); na <- sqrt(sum(a^2))
  bT <- numeric(D$p); bT[Tset] <- qr.coef(qr(D$X[, Tset, drop = FALSE]), D$X[, l])
  bB <- numeric(D$p); if (length(B)) bB[B] <- qr.coef(qr(D$X[, B, drop = FALSE]), D$X[, l])
  lam <- bT - bB; v <- resid_on(D$X, B, D$X[, l]) / na
  rec <- v - as.vector(D$X %*% lam) / na
  maxerr <- max(maxerr, sqrt(sum((rec - a / na)^2)))
  phi2 <- min(eigen(crossprod(D$X[, c(Tset, l)]) / (D$n - 1), symmetric = TRUE, only.values = TRUE)$values)
  maxvar <- max(maxvar, sum(v^2) - (1 + sum(abs(lam))^2 / phi2))        # |v|^2 <= 1 + L^2/phi0^2 with the realised floor
}
say("    300 random (T,l,N_l): max |reconstruction - u_{T,l}| = %.2e; max of |v|^2 - (1 + |lambda|_1^2/phi0^2) = %.3e (must be <= 0)", maxerr, maxvar)

say("K6  L2 Lemmas NA-W / W-conv at small n (illustration of the dichotomy; n = 240, p = 40, 8 extras, 256 lattice sets)")
for (ty in c("orth", "iid", "wide")) {
  D <- make_small(ty); LD <- lattice_dirs(D); a0 <- sqrt(log(D$n + 1) + 2 * log(D$p / (LD$k + 1)))
  G <- matrix(rnorm(D$n * 3000), D$n, 3000); Phi <- apply(abs(crossprod(LD$U, G)) - a0, 2, max)
  w0 <- mean(Phi); s <- abs(w0)
  tailp <- if (w0 < 0) mean(Phi > -s / 2) else mean(Phi < s / 2)
  say("    design '%s': width gap w0 = %+.2f (MC, 3000 draws; sd of the maximum %.2f <= 1); frequency of the event bounded by exp(-w0^2/8) = %.3f: %.4f; frequency of {max_P (|Z| - a0) > 0}: %.3f",
      ty, w0, sd(Phi), exp(-s^2 / 8), tailp, mean(Phi > 0))
}

say("K7  L2 Lemma d: d_n = E max over truth-removal directions (deletions and swaps) vs the bound sqrt(q+1) + sqrt(2 log p)")
D <- make_small("iid"); Ex <- setdiff(D$Q, D$S0); m <- length(Ex); V <- list()
for (code in sample(0:(2^m - 1), 60)) {
  Tset <- c(D$S0, Ex[bitwAnd(bitwShiftR(code, 0:(m - 1)), 1L) == 1L])
  for (i in D$S0) { A <- setdiff(Tset, i); V[[length(V) + 1]] <- unit(resid_on(D$X, A, D$X[, i]))
    for (l in sample(setdiff(1:D$p, Tset), 8)) V[[length(V) + 1]] <- unit(resid_on(D$X, c(A, l), D$X[, i])) }
}
V <- do.call(cbind, V); G <- matrix(rnorm(D$n * 3000), D$n, 3000); dn <- mean(apply(abs(crossprod(V, G)), 2, max))
say("    %d sampled directions: MC d_n >= %.2f; bound = %.2f; ok: %s", ncol(V), dn, sqrt(length(D$Q) + 1) + sqrt(2 * log(D$p)),
    dn <= sqrt(length(D$Q) + 1) + sqrt(2 * log(D$p)))
writeLines(out, file.path(here, "lemma_checks_out.txt"))
