# check_smcbvs_prior.R -- verifies the SMC-BVS v3.1.1 marginal likelihood (v3_score.h) equals the closed form under
# beta_S | s2 ~ N(0, n s2 (X_S^T X_S + I)^{-1}), s2 ~ IG(0.01, 0.01), by a direct grid integral over s2 (SPEC.md §9).
# (The first integrate() value is inaccurate for IG(0.01, 0.01); the grid line is the check.)
set.seed(1); n <- 30; k <- 3; X <- scale(matrix(rnorm(n*k), n)); y <- drop(scale(X %*% c(1,-1,0.5) + rnorm(n)))
a0 <- 0.01; b0 <- 0.01; G <- crossprod(X); z <- drop(crossprod(X, y)); yty <- sum(y^2)
# engine formula (v3_score.h l.57-59, 181-182, 217, 223)
H <- (n+1)*G + diag(k); A <- G + diag(k); Q <- yty - n * drop(t(z) %*% solve(H, z)); nu <- a0 + n/2
logCn <- a0*log(2*b0) + lgamma(nu) - (n/2)*log(pi) - lgamma(a0)
eng <- logCn - 0.5*(determinant(H)$modulus - determinant(A)$modulus) - nu*log(2*b0 + Q)
# direct: y | sigma2 ~ N(0, sigma2 (I + X V X')), V = n (G + I)^{-1}, sigma2 ~ IG(a0, b0); integrate sigma2 numerically
V <- n * solve(G + diag(k)); Sig <- diag(n) + X %*% V %*% t(X); Si <- solve(Sig); ld <- determinant(Sig)$modulus; q <- drop(t(y) %*% Si %*% y)
f <- function(s2) exp(-n/2*log(2*pi*s2) - 0.5*ld - q/(2*s2) + a0*log(b0) - lgamma(a0) - (a0+1)*log(s2) - b0/s2 + 0)
lf <- function(t) { s2 <- exp(t); f(s2) * s2 }
dir <- log(integrate(lf, -30, 30, subdivisions = 5000, rel.tol = 1e-12)$value)
cat(sprintf("engine %.10f  direct %.10f  diff %.2e\n", eng, dir, eng - dir))
# model prior: BB(1,p): P(S) = B(1+k, 2p-k)/B(1,p) vs 1/2/choose(2p-1,k)
p <- 50; kk <- 0:5; cat(max(abs(lbeta(1+kk, 2*p-kk) - lbeta(1,p) - (-log(2) - lchoose(2*p-1, kk)))), "\n")
lg <- function(t) { s2 <- exp(t); -n/2*log(2*pi*s2) - 0.5*ld - q/(2*s2) + a0*log(b0) - lgamma(a0) - (a0+1)*log(s2) - b0/s2 + t }
tt <- seq(-40, 60, length.out = 2e6); v <- lg(tt); m <- max(v); dir2 <- m + log(sum(exp(v - m)) * diff(tt[1:2]))
cat(sprintf("grid direct %.10f diff %.2e\n", dir2, eng - dir2))
