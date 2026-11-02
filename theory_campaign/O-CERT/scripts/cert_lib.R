# O-CERT certificate library (exact target of METHODOLOGY_v3 §5; no randomness).
# F(S) = log varpi(S) + log m(S), so pi(S) = exp(F(S)) / Z.

cert_data <- function(X, y) {
  n <- nrow(X)
  X <- scale(X, TRUE, TRUE); attr(X, "scaled:center") <- NULL; attr(X, "scaled:scale") <- NULL
  y <- as.numeric(scale(y, TRUE, TRUE))                       # ||y||^2 = n - 1, ||x_j||^2 = n - 1
  p <- ncol(X); K <- min(p, floor(n / 2)); a0 <- 0.01; b0 <- 0.01; nu <- a0 + n / 2
  lCn <- a0 * log(2 * b0) + lgamma(nu) - (n / 2) * log(pi) - lgamma(a0)
  lw <- log(0.5) - lchoose(2 * p - 1, 0:K)                     # log w(k), k = 0..K
  lWK <- matrixStats_logsumexp(lchoose(p, 0:K) + lw)
  list(X = X, y = y, n = n, p = p, K = K, b0 = b0, nu = nu, lCn = lCn, lw = lw, lWK = lWK,
       yy = sum(y^2), Xy = drop(crossprod(X, y)), XtX = NULL)
}
matrixStats_logsumexp <- function(v) { m <- max(v); m + log(sum(exp(v - m))) }

# Q_S and log D_S (Lemma M: Q decreasing, D increasing in S)
QD <- function(dd, S) {
  if (!length(S)) return(c(Q = dd$yy, lD = 0))
  G <- crossprod(dd$X[, S, drop = FALSE]); z <- dd$Xy[S]; k <- length(S)
  H <- (dd$n + 1) * G + diag(k); R <- chol(H); R1 <- chol(G + diag(k))
  v <- backsolve(R, z, transpose = TRUE)
  c(Q = dd$yy - dd$n * sum(v^2), lD = 2 * sum(log(diag(R))) - 2 * sum(log(diag(R1))))
}
Fscore <- function(dd, S) {
  k <- length(S); if (k > dd$K) return(-Inf)
  q <- QD(dd, S)
  dd$lw[k + 1] - dd$lWK + dd$lCn - 0.5 * q[["lD"]] - dd$nu * log(2 * dd$b0 + q[["Q"]])
}

# Closed flip/swap neighbourhood of S (the local-search scan set, M §6.10)
local_scan <- function(dd, S) {
  p <- dd$p; out <- setdiff(seq_len(p), S); F0 <- Fscore(dd, S)
  fadd <- if (length(S) < dd$K) vapply(out, function(j) Fscore(dd, sort(c(S, j))), 0) else numeric(0)
  fdel <- vapply(S, function(j) Fscore(dd, setdiff(S, j)), 0)
  fsw <- matrix(NA_real_, length(S), length(out))
  for (a in seq_along(S)) for (b in seq_along(out)) fsw[a, b] <- Fscore(dd, sort(c(setdiff(S, S[a]), out[b])))
  all <- c(F0, fadd, fdel, as.vector(fsw))
  list(F0 = F0, g_add = F0 - max(fadd), g_del = F0 - max(fdel), g_swap = F0 - max(fsw),
       best_add = out[which.max(fadd)], best_del = S[which.max(fdel)],
       local_max = all(all[-1] <= F0), n_nbr = length(all) - 1,
       log_share = F0 - matrixStats_logsumexp(all),            # log pi(S | closed neighbourhood), exact
       fadd = setNames(fadd, out), fdel = setNames(fdel, S))
}

# Exact enumeration of all subsets of S (the 'subset-type' alternatives)
subset_scan <- function(dd, S) {
  k <- length(S); F0 <- Fscore(dd, S); best <- -Inf; lse <- -Inf; nb <- 0
  for (m in 0:(2^k - 2)) {                                       # all proper subsets
    T <- S[bitwAnd(m, 2^(0:(k - 1))) > 0]
    f <- Fscore(dd, T); best <- max(best, f); lse <- matrixStats_logsumexp(c(lse, f)); nb <- nb + 1
  }
  list(g_sub = F0 - best, log_ratio_sub = lse - F0, n = nb)
}

# Branch and bound over the box 2^U (Theorem C3). Node (L, Up): models S with L <= S <= Up.
#   Phi(L, Up)  = lw(|L|) - lWK + lCn - lD(L)/2 - nu log(2 b0 + Q(Up))          >= F(S)
#   logM(L, Up) = log sum_k C(|Up|-|L|, k-|L|) w(k) - lWK + lCn - lD(L)/2 - nu log(2 b0 + Q(Up))
#               >= log sum_{S in node} exp F(S)
# mode "opt": prune when Phi <= Fhat (certifies max_{2^U} F <= Fhat unless a better model is found).
# mode "mass": prune when logM <= Fhat + tau; returns an upper bound on sum_{S in 2^U, S != Shat} exp(F(S) - Fhat).
bnb <- function(dd, Shat, U, mode = c("opt", "mass"), tau = -12, max_nodes = 2e5, order_score = NULL) {
  mode <- match.arg(mode); Fhat <- Fscore(dd, Shat)
  ord <- if (is.null(order_score)) U else U[order(-order_score[as.character(U)])]
  stack <- list(list(L = integer(0), Up = ord)); nodes <- 0; better <- list(); rest <- -Inf
  leaf_exact <- -Inf
  while (length(stack)) {
    nd <- stack[[length(stack)]]; stack[[length(stack)]] <- NULL; nodes <- nodes + 1
    if (nodes > max_nodes) return(list(done = FALSE, nodes = nodes, better = better, log_rest = NA, Fhat = Fhat))
    L <- nd$L; Up <- nd$Up; kL <- length(L)
    if (kL > dd$K) next
    qL <- QD(dd, L); qU <- QD(dd, Up)
    base <- -dd$lWK + dd$lCn - 0.5 * qL[["lD"]] - dd$nu * log(2 * dd$b0 + qU[["Q"]])
    Phi <- dd$lw[kL + 1] + base
    free <- setdiff(Up, L); kmax <- min(length(Up), dd$K)
    ks <- kL:kmax
    logM <- matrixStats_logsumexp(lchoose(length(free), ks - kL) + dd$lw[ks + 1]) + base
    FL <- if (identical(sort(L), sort(Shat))) -Inf else {
      fl <- dd$lw[kL + 1] - dd$lWK + dd$lCn - 0.5 * qL[["lD"]] - dd$nu * log(2 * dd$b0 + qL[["Q"]]); fl }
    if (FL > Fhat) better[[length(better) + 1]] <- list(S = sort(L), F = FL)
    if (!length(free)) { if (mode == "mass") rest <- matrixStats_logsumexp(c(rest, FL - Fhat)); next }
    if (mode == "opt" && Phi <= Fhat) next
    if (mode == "mass" && logM <= Fhat + tau) { rest <- matrixStats_logsumexp(c(rest, logM - Fhat)); next }
    j <- free[1]
    # node splits into: S contains j (L + j, Up) and S excludes j (L, Up - j). L itself lies in the exclude child.
    stack[[length(stack) + 1]] <- list(L = L, Up = setdiff(Up, j))
    stack[[length(stack) + 1]] <- list(L = c(L, j), Up = Up)
  }
  list(done = TRUE, nodes = nodes, better = better, log_rest = rest, Fhat = Fhat)
}
