# check_identity.R -- algebraic test suggested by review BT1 (P1): for T containing S0, i in S0, l outside T,
# A = (T \ {i}) + {l}:   RSS_A - RSS_T = (theta_i ||(I-P_A) x_i|| + sigma Z_{A,i})^2 - sigma^2 Z_{T,l}^2,
# and for a deletion A = T \ {i}:  RSS_A - RSS_T = (theta_i ||(I-P_A) x_i|| + sigma Z_{A,i})^2.
# Correlated columns, signed coefficients. Pure linear algebra (no method object).
set.seed(3)
n <- 60; p <- 25; maxerr <- 0; ntest <- 0
for (rep in 1:200) {
  L <- matrix(rnorm(p * p), p, p); X <- matrix(rnorm(n * p), n, p) %*% (diag(p) + 0.4 * L)
  X <- scale(X, center = TRUE, scale = FALSE)
  S0 <- 1:3; theta <- c(1.3, -0.7, 2.1); sigma <- 1.7
  eps <- rnorm(n, sd = sigma); eps <- eps - mean(eps)
  mu <- X[, S0] %*% theta; Y <- mu + eps
  Tset <- sort(c(S0, sample(4:15, sample(0:8, 1)))); i <- sample(S0, 1); l <- sample(setdiff(1:p, Tset), 1)
  rss <- function(S) sum(qr.resid(qr(X[, S, drop = FALSE]), Y)^2)
  u <- function(S, j) { v <- qr.resid(qr(X[, S, drop = FALSE]), X[, j]); list(u = v / sqrt(sum(v^2)), nrm = sqrt(sum(v^2))) }
  A1 <- setdiff(Tset, i); A2 <- sort(c(A1, l))
  a1 <- u(A1, i); a2 <- u(A2, i); tl <- u(Tset, l)
  th <- theta[match(i, S0)]
  lhs1 <- rss(A1) - rss(Tset); rhs1 <- (th * a1$nrm + sum(a1$u * eps))^2
  lhs2 <- rss(A2) - rss(Tset); rhs2 <- (th * a2$nrm + sum(a2$u * eps))^2 - sum(tl$u * eps)^2
  maxerr <- max(maxerr, abs(lhs1 - rhs1) / (1 + abs(lhs1)), abs(lhs2 - rhs2) / (1 + abs(lhs2))); ntest <- ntest + 2
}
cat(sprintf("identity (1) of BT1-P1: %d comparisons (deletions and swaps), max relative error = %.2e\n", ntest, maxerr))
