## F-DRAFT: exact p = 12 check of the start-vs-posterior discrepancy (base R only).
## Target quantities (v3 notation, METHODOLOGY_v3 s5-6.3, 00_COMMON):
##   pi0 = composite start (two blocks, tables against the full y), pi = posterior,
##   d(S) = log BF(S) - sum_b log r_b(S cap C_b),  1 + chi2(pi||pi0) = sum_S pi^2/pi0 = 1/rho_Omega(0,1).
## Claims checked: (C1) under exact block orthogonality d(S) >= 0 with d = 0 iff <= 1 block carries R^2;
##   (C2) 1+chi2 is dominated by the single-null-addition layer S0+j;
##   (C3) log[pi(S0+j)/pi(S0)] - log[pi0(S0+j)/pi0(S0)] ~= kappa_b * G_j (G_j = posterior gain of j net of the
##        dimension penalty), kappa_b = Delta_T/(sigma^2 + Delta_T), T = S0 cap C_b  (dilution fraction);
##   (C4) the ideal adaptive grid (full-space ESS >= 0.9 per stage, 60 halvings) is short even when 1+chi2 is large;
##   (C5) proxy pair split across blocks: pi0 puts its mass on the union {j,l} (naive merge), pi on {j}; chi2 explodes.
## Exact arithmetic up to double precision; no Monte Carlo except the single simulated data set per seed.
set.seed(20261102)
a0 <- 0.01; b0 <- 0.01
std_cols <- function(M){ M <- sweep(M, 2, colMeans(M)); n <- nrow(M); sweep(M, 2, sqrt(colSums(M^2)/(n-1)), "/") }
logm <- function(X, y, S, n){            # log m(S) without the constant C_n
  nu <- a0 + n/2; yy <- sum(y^2)
  if (length(S) == 0) return(-nu*log(2*b0 + yy))
  XS <- X[, S, drop=FALSE]; G <- crossprod(XS); z <- crossprod(XS, y); k <- length(S)
  H <- (n+1)*G + diag(k); RH <- chol(H); RG <- chol(G + diag(k))
  ldH <- 2*sum(log(diag(RH))); ldG <- 2*sum(log(diag(RG)))
  w <- backsolve(RH, forwardsolve(t(RH), z)); Q <- yy - n*sum(z*w)
  -0.5*(ldH - ldG) - nu*log(2*b0 + Q)
}
logw <- function(k, p) -log(2) - lchoose(2*p - 1, k)
run <- function(X, y, blocks, S0, label, sigma_std, mu_std){
  n <- nrow(X); p <- ncol(X); N <- 2^p
  idx <- 0:(N-1); members <- lapply(idx, function(m) which(bitwAnd(m, 2^(0:(p-1))) > 0))
  lm_all <- vapply(members, function(S) logm(X, y, S, n), 0)
  lbf <- lm_all - lm_all[1]
  key <- function(S) if (length(S)==0) 1 else sum(2^(S-1)) + 1
  lt <- sapply(members, function(S) sum(vapply(blocks, function(Cb) lbf[key(intersect(S, Cb))], 0)))
  k <- lengths(members); lpri <- logw(k, p)
  lg0 <- lpri + lt; lg1 <- lpri + lbf; d <- lbf - lt
  lse <- function(v) { m <- max(v); m + log(sum(exp(v - m))) }
  pi0 <- exp(lg0 - lse(lg0)); pi1 <- exp(lg1 - lse(lg1))
  chi2 <- sum(pi1^2/pi0) - 1
  KL <- sum(pi1*log(pi1/pi0)); TV <- 0.5*sum(abs(pi1 - pi0))
  k0 <- key(S0)
  nulls <- setdiff(1:p, S0)
  add <- sapply(nulls, function(j) key(sort(c(S0, j)))); del <- sapply(S0, function(j) key(setdiff(S0, j)))
  terms <- pi1^2/pi0
  rest <- sum(terms) - terms[k0] - sum(terms[add]) - sum(terms[del])
  ## (C3): dilution fractions and log ratios
  P <- function(T) if (length(T)==0) matrix(0, n, n) else { XT <- X[,T,drop=FALSE]; XT %*% solve(crossprod(XT), t(XT)) }
  kap <- sapply(nulls, function(j){ b <- which(sapply(blocks, function(Cb) j %in% Cb)); T <- intersect(S0, blocks[[b]])
    r <- mu_std - P(T) %*% mu_std; Del <- sum(r^2)/(n-1); Del/(sigma_std^2 + Del) })
  LR <- sapply(seq_along(nulls), function(i){ j <- nulls[i]; (lg1[add[i]] - lg1[k0]) - (lg0[add[i]] - lg0[k0]) })
  Gj <- sapply(seq_along(nulls), function(i) lbf[add[i]] - lbf[k0] + 0.5*log(n+1))
  ## (C4): ideal full-space adaptive grid, ESS >= 0.9 per stage
  Fphi <- function(t) lse(lg0 + t*d)
  rho <- function(u, v) exp(2*Fphi(v) - Fphi(u) - Fphi(2*v - u))
  u <- 0; grid <- 0; while (u < 1) { if (rho(u, 1) >= 0.9) { v <- 1 } else { lo <- u; hi <- 1
      for (it in 1:60) { mid <- (lo+hi)/2; if (rho(u, mid) >= 0.9) lo <- mid else hi <- mid }; v <- lo }
    grid <- c(grid, v); u <- v }
  cat(sprintf("\n== %s (n=%d, p=%d) ==\n", label, n, p))
  cat(sprintf("pi(S0)=%.4f  pi0(S0)=%.4g  argmax pi0 = {%s}  argmax pi = {%s}\n", pi1[k0], pi0[k0],
              paste(members[[which.max(pi0)]], collapse=","), paste(members[[which.max(pi1)]], collapse=",")))
  cat(sprintf("min d = %.3g  d(S0) = %.3f  max d = %.3f\n", min(d), d[k0], max(d)))
  cat(sprintf("1+chi2 = %.4g  (one-step ESS fraction %.3g)   KL(pi||pi0) = %.4g   TV = %.4g\n", 1+chi2, 1/(1+chi2), KL, TV))
  cat(sprintf("layers of sum pi^2/pi0: S0 %.4g | S0+j %.4g | S0-j %.4g | rest %.4g\n", terms[k0], sum(terms[add]), sum(terms[del]), rest))
  cat(sprintf("ideal adaptive grid (ESS>=0.9): T = %d stages: %s\n", length(grid)-1, paste(sprintf("%.3f", grid), collapse=" ")))
  cat("null j | kappa_b | G_j (post gain) | LR_j (log pi-odds - log pi0-odds) | kappa_b*G_j | term pi^2/pi0\n")
  o <- order(-terms[add])
  for (i in o[1:min(6, length(o))]) cat(sprintf("%6d | %.3f | %7.3f | %7.3f | %7.3f | %.3g\n", nulls[i], kap[i], Gj[i], LR[i], kap[i]*Gj[i], terms[add[i]]))
  invisible(list(chi2=chi2, T=length(grid)-1, kap=kap, LR=LR, Gj=Gj))
}
make_BO <- function(n, p, blocks, rho_within = 0){
  X <- matrix(rnorm(n*p), n, p)
  if (rho_within > 0) for (Cb in blocks) { f <- rnorm(n); X[,Cb] <- sqrt(rho_within)*f + sqrt(1-rho_within)*X[,Cb] }
  X <- std_cols(X); X1 <- X[, blocks[[1]], drop=FALSE]
  X[, blocks[[2]]] <- X[, blocks[[2]]] - X1 %*% solve(crossprod(X1), crossprod(X1, X[, blocks[[2]]]))
  std_cols(X)
}
p <- 12; blocks <- list(1:6, 7:12)
for (n in c(200, 800)) for (cfg in 1:3) {
  X <- make_BO(n, p, blocks)
  if (cfg == 1) { S0 <- c(1, 7); th <- c(1.5, 1.5); lab <- "BO, one truth per block (dilution in both blocks)" }
  if (cfg == 2) { S0 <- c(1, 2); th <- c(1.5, 1.5); lab <- "BO, both truths in block 1 (dilution only for block-2 nulls)" }
  if (cfg == 3) { S0 <- c(1, 7); th <- c(0.3, 0.3); lab <- "BO, weak signal (small R^2: dilution negligible)" }
  mu <- as.vector(X[, S0] %*% th); yr <- mu + rnorm(n); sy <- sqrt(sum((yr-mean(yr))^2)/(n-1))
  y <- (yr - mean(yr))/sy
  run(X, y, blocks, S0, lab, sigma_std = 1/sy, mu_std = (mu - mean(mu))/sy)
}
## (C5) proxy pair split across blocks: truth {1}, x_7 = 0.9-correlated copy of x_1 placed in block 2
for (n in c(200, 800)) {
  X <- matrix(rnorm(n*p), n, p); X[,7] <- 0.9*X[,1] + sqrt(1-0.81)*X[,7]; X <- std_cols(X)
  S0 <- 1; mu <- 1.5*X[,1]; yr <- mu + rnorm(n); sy <- sqrt(sum((yr-mean(yr))^2)/(n-1)); y <- (yr-mean(yr))/sy
  res <- run(X, y, blocks, S0, "PROXY SPLIT: truth {1}, proxy 7 (r=0.9) in the other block", 1/sy, (mu-mean(mu))/sy)
}
