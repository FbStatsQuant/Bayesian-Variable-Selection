# falsify_L4_L5.R -- falsification attempt for lemmas/L4_VIS.md and lemmas/L5_ASM_STARTF.md. Base R.
# Part A (L4): a truth with a close correlate in its block and signals of order sqrt(log n / n) (visibility near the
#   boundary). For every U in a truth block with U*_b not in U (Q = S0): the chain of Steps 1-3 of L4.1 is checked
#   with the REALISED event constants (zeta = max chi-square in the truth blocks, omega = max |rho|), i.e.
#     log[omega(U) r_b(U)/r_b(T)]  <=  Pi - A1_lower + A2_upper + (R_U - R_T);
#   reported: the realised (V-m) margin c_m (eps0 = 0.1), the realised exponent of the Xi terms, the realised (V-c)
#   level and the exponent of e_n. Claims: exponent(Xi) >= c_m/2 - o(1); exponent(e_n) >= (c_V - 1 - 2A)/2 - o(1).
# Part B (L5): small p, exact enumeration: (AGG-b) + (e3) assembly inequality, o0/T1, o0 sqrt(n).
# A violation prints "VIOLATION". Usage: Rscript falsify_L4_L5.R [seed]
args <- commandArgs(TRUE); seed <- if (length(args) >= 1) as.integer(args[1]) else 20261111L
src <- sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)); source(file.path(dirname(src), "lem_common.R"))
set.seed(seed); viol <- 0L
bad <- function(...) { viol <<- viol + 1L; cat("VIOLATION", ..., "\n") }
res <- function(v, XT) if (ncol(XT)) qr.resid(qr(XT), v) else v

cat("== Part A: visibility bridges ==\n")
for (n in c(200, 800, 3200)) for (ctheta in c(12, 30)) {
  p <- 48; bs <- 6; sigma <- 1; eps1 <- 0.1; eps0 <- 0.1; A <- log(p) / log(n)
  X <- matrix(rnorm(n * p), n, p); X[, 2] <- 0.8 * X[, 1] + 0.6 * X[, 2]            # null 2: close correlate of truth 1
  Xs <- std_cols(X); S0 <- c(1, 7); theta <- numeric(p); theta[S0] <- sqrt(ctheta * log(n) / (n - 1)) * c(1, -1)
  mu <- as.numeric(Xs %*% theta); blocks <- split(seq_len(p), ceiling(seq_len(p) / bs)); tb <- which(vapply(blocks, function(B) any(B %in% S0), TRUE))
  # deterministic quantities per truth block and local mask: Lambda, tau^2
  det <- lapply(tb, function(b) { Cb <- blocks[[b]]; LM <- 0:(2^length(Cb) - 1)
    Lam <- vapply(LM, function(m) sum(res(mu, Xs[, Cb[idx_of(m)], drop = FALSE])^2), 0.0); list(Lam = Lam, tau2 = sigma^2 + Lam / (n - 1)) })
  cm_real <- Inf; cV_real <- Inf
  for (ib in seq_along(tb)) { Cb <- blocks[[tb[ib]]]; LM <- 0:(2^length(Cb) - 1); ust <- mask_of(which(Cb %in% S0)); D <- det[[ib]]
    for (U in LM[bitwAnd(LM, ust) != ust]) { W <- bitwOr(U, ust); d <- popc(bitwAnd(ust, bitwNot(U))); a <- popc(bitwAnd(U, bitwNot(ust)))
      L1 <- D$Lam[U + 1] - D$Lam[W + 1]; L2 <- D$Lam[ust + 1] - D$Lam[W + 1]
      cm_real <- min(cm_real, (L1 / D$tau2[U + 1] - (1 + eps0) * L2 / D$tau2[W + 1]) / log(n) - (1 + 2 * A) * max(d - a, 0))
      for (i in idx_of(bitwAnd(ust, bitwNot(U)))) { Uj <- bitwOr(U, bitwShiftL(1L, i - 1L))      # single-truth gain given U
        cV_real <- min(cV_real, (D$Lam[U + 1] - D$Lam[Uj + 1]) / (D$tau2[U + 1] * log(n))) } } }
  expXi <- c(); expen <- c(); slack <- c()
  for (it in 1:20) { eps <- rnorm(n, 0, sigma); Y <- mu + eps - mean(eps); ys <- std_vec(Y); nu <- 0.01 + n / 2
    worst <- -Inf; en <- 0
    for (ib in seq_along(tb)) { Cb <- blocks[[tb[ib]]]; LM <- 0:(2^length(Cb) - 1); ust <- mask_of(which(Cb %in% S0)); D <- det[[ib]]
      lt <- block_table(Xs, ys, Cb)
      RSS <- vapply(LM, function(m) sum(res(Y, Xs[, Cb[idx_of(m)], drop = FALSE])^2), 0.0)
      Pe <- vapply(LM, function(m) { XT <- Xs[, Cb[idx_of(m)], drop = FALSE]; if (ncol(XT)) sum((eps - res(eps, XT))^2) else 0 }, 0.0)  # ||P_U eps||^2
      om <- max(abs(RSS / ((n - 1) * D$tau2) - 1)); th <- (n + 0.02) / ((n - 1) * (1 - om)) - 1
      RU <- lt + 0.5 * popc(LM) * log(n + 1) + nu * log(RSS)              # R_U - R_empty + const: differences are exact remainders
      for (U in LM[bitwAnd(LM, ust) != ust]) { W <- bitwOr(U, ust); Tm <- ust; d <- popc(bitwAnd(ust, bitwNot(U))); a <- popc(bitwAnd(U, bitwNot(ust)))
        s0 <- length(S0); om_w <- (2 * p)^max(d - a, 0) * (16 * s0 / p)^max(a - d, 0)
        lhs <- log(om_w) + lt[U + 1] - lt[Tm + 1]
        z1 <- (Pe[W + 1] - Pe[U + 1]) / sigma^2; z2 <- (Pe[W + 1] - Pe[Tm + 1]) / sigma^2     # ||(P_W - P_U) eps||^2 / sigma^2 (nested)
        L1 <- D$Lam[U + 1] - D$Lam[W + 1]; L2 <- D$Lam[Tm + 1] - D$Lam[W + 1]
        A1lo <- ((1 - eps1) * L1 - sigma^2 * z1 / eps1) / (2 * D$tau2[U + 1] * (1 + om))
        A2up <- (1 + th) * ((1 + eps1) * L2 + (1 + 1 / eps1) * sigma^2 * z2) / (2 * D$tau2[W + 1])
        Pi <- log(om_w) + 0.5 * (d - a) * log(n + 1)
        rhs <- Pi - A1lo + A2up + (RU[U + 1] - RU[Tm + 1])
        if (lhs > rhs + 1e-7) bad("L4.1 chain", n, ctheta, "U", U, lhs, rhs)
        slack <- c(slack, rhs - lhs); worst <- max(worst, lhs)
        en <- max(en, 2 * p * exp((lt[U + 1] - lt[W + 1]) / d)) } }
    expXi <- c(expXi, -worst / log(n)); expen <- c(expen, -log(en) / log(n)) }
  cat(sprintf("n=%4d c_theta=%2d (1+2A=%.2f): realised (V-m) margin c_m=%.2f -> c_m/2=%.2f; exponent of the largest Xi term: median %.2f, min %.2f | realised (V-c) level c_V=%.2f -> (c_V-1-2A)/2=%.2f; exponent of e_n: median %.2f, min %.2f | chain slack min %.2f\n",
              n, ctheta, 1 + 2 * A, cm_real, cm_real / 2, median(expXi), min(expXi), cV_real, (cV_real - 1 - 2 * A) / 2, median(expen), min(expen), min(slack)))
}

cat("== Part B: assembly at Q = S0, exact enumeration (p = 12, two blocks of 6) ==\n")
for (n in c(100, 400, 1600, 6400)) {
  p <- 12; sigma <- 1; Xs <- std_cols(matrix(rnorm(n * p), n, p)); S0 <- c(1, 7); s0 <- 2; theta <- numeric(p); theta[S0] <- c(0.8, -0.8)
  mu <- as.numeric(Xs %*% theta); blocks <- list(1:6, 7:12); K <- min(p, n %/% 2); out <- c()
  for (it in 1:40) { ys <- std_vec(mu + rnorm(n, 0, sigma)); ltab <- lapply(blocks, function(Cb) block_table(Xs, ys, Cb))
    r <- start_enum(p, blocks, ltab, K, S0, S0); Xi <- max(r$Xi)
    if (r$U <= 0.25 && s0 * Xi <= 0.5) { up <- r$T1 + 0.5 * (s0 + 1) * (s0 + 2) * (4 / 3)^(s0 + 3) * r$U^2 + 2 * s0 * Xi * (4 / 3)^(16 * s0 + 1)
      if (r$o0 > up * (1 + 1e-9)) bad("L5 assembly", n, r$o0, up) }
    if (r$o0 < r$T1 * (1 - 1e-9) || r$T1 < 0.5 / sqrt(n + 1)) bad("L5 lower", n)
    out <- rbind(out, c(o0 = r$o0, T1 = r$T1, U = r$U, Xi = Xi)) }
  cat(sprintf("n=%4d: o0 sqrt(n) median %.3f (90%% %.3f) | o0/T1 median %.4f, max %.4f | U median %.4f | Xi median %.2e\n",
              n, median(out[, "o0"]) * sqrt(n), quantile(out[, "o0"], .9) * sqrt(n), median(out[, "o0"] / out[, "T1"]), max(out[, "o0"] / out[, "T1"]), median(out[, "U"]), median(out[, "Xi"])))
}
cat("TOTAL VIOLATIONS:", viol, "\n")
