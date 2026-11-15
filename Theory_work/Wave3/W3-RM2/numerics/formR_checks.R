# W3-RM2 — falsification checks for lemmas L4 (SAND-R^b), L5 (p = 1 endpoint) and L6 (examples E4, E5).
# Local machine, base R only. Output: formR_checks_out.txt. Each block tries to break one step.
set.seed(20261111)
out <- file("formR_checks_out.txt", "w"); say <- function(...) { cat(..., "\n", file = out, sep = ""); cat(..., "\n", sep = "") }
pick <- function(v, k = 1) v[sample.int(length(v), k)]   # safe sampling (sample() misreads a length-1 vector)
ccov <- function(S, a, b, B) { if (length(B) == 0) return(S[a, b, drop = FALSE]); S[a, b, drop = FALSE] - S[a, B, drop = FALSE] %*% solve(S[B, B, drop = FALSE], S[B, b, drop = FALSE]) }

## ---- design: polynomial covariance decay on a line -------------------------------------------------
p <- 80; alpha <- 2.5; d <- abs(outer(1:p, 1:p, "-")); Sig <- 0.35 * (1 + d)^(-alpha); diag(Sig) <- 1
stopifnot(min(eigen(Sig, symmetric = TRUE)$values) > 0.2)
S0 <- 40; theta <- 1; rQ <- 12; Q <- which(abs((1:p) - S0) <= rQ); r0 <- 3
Hl <- function(l) which(pmin(abs((1:p) - l), abs((1:p) - S0)) <= r0)
draw_pair <- function() { l <- pick(setdiff(1:p, Q)); k <- sample(2:15, 1)
  near <- setdiff(which(abs((1:p) - l) <= 8 | abs((1:p) - S0) <= 8), c(l)); U <- pick(near, min(k, length(near))); list(l = l, U = U) }

## K8: population product-form identity (L4, (star)):  Cov(l,j|U) = Cov(l,j|U0) - c_l' S_VV^{-1} c_j
err <- 0; for (it in 1:2000) { z <- draw_pair(); l <- z$l; U <- setdiff(z$U, S0); U0 <- intersect(U, Hl(l)); V <- setdiff(U, U0)
  if (length(V) == 0) next
  lhs <- ccov(Sig, l, S0, U); cl <- ccov(Sig, l, V, U0); cj <- ccov(Sig, V, S0, U0); SVV <- ccov(Sig, V, V, U0)
  rhs <- ccov(Sig, l, S0, U0) - cl %*% solve(SVV, cj); err <- max(err, abs(lhs - rhs)) }
say("K8  product-form identity, 2000 (l,U): max abs error = ", signif(err, 3))

## K9: sample version of Lemma 2: |z_U - z_U0| against zeta = ell + r*h + h^2 (population ell, r for the tested pairs)
n <- 4000; N <- n - 1; hn <- sqrt(log(n) / n); L <- chol(Sig)
pc <- function(Wc, Yc, l, B) { if (length(B)) { ql <- qr(Wc[, B, drop = FALSE]); a <- qr.resid(ql, Wc[, l]); y <- qr.resid(ql, Yc) } else { a <- Wc[, l]; y <- Yc }
  sum(a * y) / sqrt(sum(a^2) * sum(y^2)) }
worst <- 0; worst_naive <- 0; maxz0 <- 0
for (rep in 1:5) { W <- matrix(rnorm(n * p), n, p) %*% L; Wc <- scale(W, center = TRUE, scale = FALSE); tj <- sqrt(colSums(Wc^2) / N)
  Yc <- theta * Wc[, S0] / tj[S0] + (function(e) e - mean(e))(rnorm(n))
  for (it in 1:200) { z <- draw_pair(); l <- z$l; U <- z$U; U0 <- intersect(U, Hl(l)); V <- setdiff(U, U0); if (length(V) == 0) next
    Us <- setdiff(U, S0); U0s <- setdiff(U0, S0)
    ell <- max(if (S0 %in% U) 0 else abs(ccov(Sig, l, S0, U)), if (S0 %in% U0) 0 else abs(ccov(Sig, l, S0, U0)))
    r <- max(abs(ccov(Sig, l, V, U0)), if (S0 %in% U0) 0 else abs(ccov(Sig, S0, V, U0)))
    dz <- abs(pc(Wc, Yc, l, U) - pc(Wc, Yc, l, U0)); zeta <- ell + r * hn + hn^2
    worst <- max(worst, dz / zeta); worst_naive <- max(worst_naive, dz / (r^2 + hn^2)); maxz0 <- max(maxz0, abs(pc(Wc, Yc, l, U0)) / hn) } }
say("K9  sample selection removal, n = 4000, 5 designs x 200 (l,U): max |z_U - z_U0| / (ell + r h + h^2) = ", signif(worst, 3),
    " ; max |z_U0| / h_n = ", signif(maxz0, 3), " ; (ratio to the norm-product scale r^2 + h^2: ", signif(worst_naive, 3), ")")

## K10: spherical tail of Lemma 3 at a deterministic reference set: P(h >= t) vs P(chi^2_1 >= t)
n <- 300; N <- n - 1; l <- 5; U0 <- c(3, 4, 6); D <- c(U0, S0); idx <- c(D, l); Ls <- chol(Sig[idx, idx]); R <- 40000; hs <- numeric(R)
for (i in 1:R) { Wd <- matrix(rnorm(n * length(idx)), n) %*% Ls; Wd <- scale(Wd, center = TRUE, scale = FALSE)
  y <- theta * Wd[, 4] / sqrt(sum(Wd[, 4]^2) / N) + (function(e) e - mean(e))(rnorm(n)); q0 <- qr(Wd[, 1:3]); a <- qr.resid(q0, Wd[, 5]); yy <- qr.resid(q0, y)
  hs[i] <- n * sum(a * yy)^2 / (sum(a^2) * sum(yy^2)) }
for (t in c(4, 8, 12)) say("K10 spherical tail, n = 300, 40000 draws: P(h >= ", t, ") = ", signif(mean(hs >= t), 3), " ; chi2_1 tail = ", signif(pchisq(t, 1, lower.tail = FALSE), 3),
                            " ; ratio = ", signif(mean(hs >= t) / pchisq(t, 1, lower.tail = FALSE), 3))
say("K10 population leak of this pair: |Cov(W_l, W_j | W_U0)| = ", signif(abs(ccov(Sig, l, S0, U0)), 3), " (sqrt(n)*leak = ", signif(sqrt(n) * abs(ccov(Sig, l, S0, U0)), 3), ")")

## K11: p = 1 endpoint of L5 section 3: closed form of F({1}) - F(empty) against the D0 definition
mx <- 0; for (i in 1:200) { n <- sample(20:200, 1); x <- rnorm(n); x <- x - mean(x); x <- x * sqrt((n - 1) / sum(x^2)); y <- 0.7 * x + rnorm(n); y <- y - mean(y); y <- y * sqrt((n - 1) / sum(y^2))
  nu <- 0.01 + n / 2; G <- sum(x^2); H <- (n + 1) * G + 1; Dd <- H / (G + 1); zA <- sum(x * y); QA <- sum(y^2) - n * zA^2 / H; Q0 <- sum(y^2)
  direct <- (-0.5 * log(Dd) - nu * log(0.02 + QA)) - (-nu * log(0.02 + Q0)); rh <- zA / (n - 1)
  closed <- -0.5 * log(n) - nu * log((0.02 + (n - 1) * (1 - rh^2 * (n - 1) / n)) / (0.02 + n - 1)); mx <- max(mx, abs(direct - closed)) }
say("K11 p = 1 score difference, 200 cases: max |definition - closed form| = ", signif(mx, 3))

## K12: example E4 (one truth, weak proxies): Gram floor and exactness of (W-loc)
n <- 900; b <- 0.4; q <- floor(n^b); pp <- floor(n / 3); r <- sqrt(1.0 * log(n) / n)
G <- diag(pp); G[1, 2:q] <- r; G[2:q, 1] <- r; G[2:q, 2:q] <- r^2; diag(G) <- 1
me <- min(eigen(G, symmetric = TRUE)$values); bad <- 0
for (it in 1:500) { Tset <- c(1, pick(2:q, sample.int(q - 1, 1) - 1)); l <- pick(setdiff(2:q, Tset)); beta <- solve(G[Tset, Tset, drop = FALSE], G[Tset, l]); bad <- max(bad, abs(beta[1] - r), if (length(beta) > 1) max(abs(beta[-1])) else 0) }
say("K12 E4, n = 900, q = ", q, ", p = ", pp, ": min eigenvalue of the Gram = ", signif(me, 4), " ; max deviation of the proxy regression from (r, 0, ..., 0) over 500 (T, l) = ", signif(bad, 3))

## K13: example E5 (equicorrelated group): residual-norm formula and the bound (5.1)
a <- 0.5; q <- 15; viol <- -Inf; verr <- 0
for (it in 1:300) { t <- sample.int(q - 1, 1); Tset <- pick(1:q, t); l <- pick(setdiff(1:q, Tset))
  Z <- cbind(sqrt(a), sqrt(1 - a) * diag(q))            # rows: columns z_j in coordinates (e_0, e_1..e_q)
  A_t <- a / (1 - a + t * a); res <- Z[l, ] - A_t * colSums(Z[Tset, , drop = FALSE]); v_t <- (1 - a) * (1 + a / (1 - a + t * a)); verr <- max(verr, abs(sum(res^2) - v_t))
  # orthogonality of the residual to the columns of T (so A_t is the regression coefficient)
  verr <- max(verr, max(abs(Z[Tset, , drop = FALSE] %*% res)))
  u <- res / sqrt(sum(res^2)); g <- rnorm(q + 1); viol <- max(viol, abs(sum(u * g)) - (2 * max(abs(g[-1])) + sqrt(a / (1 - a)) * abs(g[1]))) }
say("K13 E5, a = 0.5, q = 15, 300 (T, l): max error in v_t and orthogonality = ", signif(verr, 3), " ; max(lhs - rhs) of (5.1) = ", signif(viol, 3), " (must be <= 0)")
close(out)
