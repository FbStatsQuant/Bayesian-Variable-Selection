# falsify_P.R -- W3-START2: falsification attempts for lemmas/P1_LEADING.md, P2_OVL.md, P3_NEC.md. Base R.
# FALSIFICATION ATTEMPTS, never proofs. Helpers (scorer transcription, tables, exact start by enumeration) are read
# from the base ticket: Theory_work/Wave3/W3-START/numerics/lemmas/lem_common.R (not modified).
#  A. Lemma P2.1(b): Z_L/gamma0(S0) = piL/pi0 <= prod_{l in Q-S0} (1 + |Q| m_l / p); random positive tables and real scorer.
#  B. P1.1: (p - s0)/(4p) <= L_sharp(h) <= L_n(S0; h), by numerical integration of J_h; random small designs and levels.
#  C. P1.2(a) and Lemma P3.1 (counting): random and adversarial partitions with blocks <= 16.
#  D. Example P3.3: eigenvalues of G_n, the formula for delta^2_{V,l}, and the premise delta^2 >= c tau^2 log n.
# Not tested here: the probability bound of Lemma LEAK-0 (its constant exp(2 kappa_E + 1) makes a Monte Carlo test
# uninformative) and lemmas/P4_BR.md (a case distinction on top of base results).
# A violation prints a line starting with "VIOLATION". Usage: Rscript falsify_P.R [nA] [nB] [nC] [seed]
args <- commandArgs(TRUE)
nA <- if (length(args) >= 1) as.integer(args[1]) else 3000L
nB <- if (length(args) >= 2) as.integer(args[2]) else 300L
nC <- if (length(args) >= 3) as.integer(args[3]) else 20000L
seed <- if (length(args) >= 4) as.integer(args[4]) else 20261112L
src <- sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE))
source(file.path(dirname(src), "..", "..", "W3-START", "numerics", "lemmas", "lem_common.R"))
set.seed(seed); tol <- 1e-9; viol <- 0L
rand_partition <- function(p, maxb) { perm <- sample(p); out <- list(); i <- 1
  while (i <= p) { sz <- min(sample(maxb, 1), p - i + 1); out[[length(out) + 1]] <- sort(perm[i:(i + sz - 1)]); i <- i + sz }; out }
pick <- function(x, k) if (k > 0) x[sample.int(length(x), k)] else integer(0)

## A. Lemma P2.1(b)
chkA <- function(p, blocks, ltab, K, S0, Q, tag) {
  r <- start_enum(p, blocks, ltab, K, S0, Q); N <- setdiff(Q, S0)
  lhs <- r$piL / r$pi0; rhs <- prod(1 + length(Q) * r$ml[N] / p)
  if (!(lhs <= rhs * (1 + tol))) { viol <<- viol + 1L; cat("VIOLATION A", tag, lhs, rhs, "\n") }
  lhs / rhs }
ratA <- c()
for (rep in seq_len(nA)) {
  p <- sample(4:11, 1); blocks <- rand_partition(p, sample(1:4, 1)); mb <- max(lengths(blocks))
  K <- mb + sample.int(p - mb + 1L, 1L) - 1L; s0 <- sample(0:min(K, 4), 1); S0 <- sort(pick(seq_len(p), s0))
  Q <- sort(c(S0, pick(setdiff(seq_len(p), S0), sample(0:min(K - s0, 4), 1))))
  ltab <- lapply(blocks, function(Cb) { v <- rnorm(2^length(Cb), 0, sample(c(0.5, 3, 8), 1)); v[1] <- 0; v })
  ratA <- c(ratA, chkA(p, blocks, ltab, K, S0, Q, "tables")) }
ratR <- c()
for (rep in seq_len(nB)) {
  n <- sample(c(20, 40, 80), 1); p <- sample(5:9, 1); K <- min(p, n %/% 2)
  X <- matrix(rnorm(n * p), n) + rnorm(n) %o% runif(p, 0, 1.5); Xs <- std_cols(X)
  s0 <- sample(0:3, 1); S0 <- sort(pick(seq_len(p), s0)); th <- numeric(p); th[S0] <- runif(s0, 0.2, 1.5) * sample(c(-1, 1), s0, TRUE)
  ys <- std_vec(as.numeric(Xs %*% th) + rnorm(n)); blocks <- rand_partition(p, sample(1:4, 1))
  Q <- sort(c(S0, pick(setdiff(seq_len(p), S0), sample(0:min(K - s0, 3), 1))))
  ltab <- lapply(blocks, function(Cb) block_table(Xs, ys, Cb))
  ratR <- c(ratR, chkA(p, blocks, ltab, K, S0, Q, "scorer")) }
cat(sprintf("A: %d random tables, %d scorer cases; max lhs/rhs = %.6f / %.6f\n", nA, nB, max(ratA), max(ratR)))

## B. P1.1
Jh <- function(d, t, h, sg) integrate(function(z) exp((d + sg * z)^2 / (2 * t^2)) * dnorm(z), -h, h, rel.tol = 1e-10)$value
subsets <- function(v, kmax = 15) { out <- list(integer(0)); for (x in v) out <- c(out, lapply(out, function(u) c(u, x))); out[lengths(out) <= kmax] }
nBB <- 0
for (rep in seq_len(max(20L, nB %/% 5L))) {
  n <- sample(c(30, 100), 1); p <- sample(3:7, 1); s0 <- sample(1:min(3, p - 1), 1); sg <- runif(1, 0.5, 2)
  X <- std_cols(matrix(rnorm(n * p), n) + rnorm(n) %o% runif(p, 0, 1)); S0 <- sort(sample(p, s0))
  th <- numeric(p); th[S0] <- runif(s0, 0.1, 1) * sample(c(-1, 1), s0, TRUE); mu <- as.numeric(X %*% th)
  zn <- sqrt(2 * log(2^21 * p) + 2 * log(log(n)))
  term <- function(l, U, h) { r <- if (length(U)) qr.resid(qr(X[, U, drop = FALSE]), cbind(X[, l], mu)) else cbind(X[, l], mu)
    u <- r[, 1] / sqrt(sum(r[, 1]^2)); Jh(sum(u * mu), sqrt(sg^2 + sum(r[, 2]^2) / (n - 1)), h, sg) }
  nulls <- setdiff(seq_len(p), S0); h <- runif(length(nulls), 1, zn)
  prop <- Filter(function(U) length(U) < s0, subsets(S0))
  Ls <- sum(sapply(seq_along(nulls), function(i) max(sapply(prop, function(U) term(nulls[i], U, h[i]))))) / p
  Ln <- sum(sapply(seq_along(nulls), function(i) max(sapply(subsets(setdiff(seq_len(p), nulls[i])), function(U) term(nulls[i], U, h[i]))))) / p
  nBB <- nBB + 1
  if (!((p - s0) / (4 * p) <= Ls * (1 + tol) && Ls <= Ln * (1 + 1e-7) && 1 / p <= 4 * Ls * (1 + tol))) { viol <- viol + 1L; cat("VIOLATION B", p, s0, Ls, Ln, "\n") } }
cat(sprintf("B: %d designs checked: (p-s0)/(4p) <= L_sharp <= L_n(S0;h), 1/p <= 4 L_sharp\n", nBB))

## C. counting
nCC <- 0
for (rep in seq_len(nC)) {
  p <- sample(17:70, 1); s0 <- sample(1:20, 1); adv <- runif(1) < 0.5
  if (adv && s0 <= 16) {                      # adversarial: one block holds S0 and as many nulls as it can
    perm <- sample(p); big <- perm[1:16]; rest <- perm[-(1:16)]; S0 <- big[seq_len(s0)]
    blocks <- c(list(big), if (length(rest)) lapply(rand_partition(length(rest), 16), function(ix) rest[ix]))
  } else { blocks <- rand_partition(p, 16); S0 <- sample(p, min(s0, p - 1)) }
  s0 <- length(S0); if (s0 == 0 || s0 >= p) next
  bl <- integer(p); for (b in seq_along(blocks)) bl[blocks[[b]]] <- b
  nulls <- setdiff(seq_len(p), S0); exc <- nulls[vapply(nulls, function(l) all(S0 %in% blocks[[bl[l]]]), TRUE)]
  nCC <- nCC + 1
  if (length(exc) > max(0, 16 - s0)) { viol <- viol + 1L; cat("VIOLATION C1", s0, length(exc), "\n") }
  if (s0 <= 15 && length(nulls) >= 17 - s0) {  # worst choice of I: all exceptional nulls first
    I <- c(exc, setdiff(nulls, exc))[seq_len(17 - s0)]
    if (all(I %in% exc)) { viol <- viol + 1L; cat("VIOLATION C2", s0, "\n") } } }
cat(sprintf("C: %d partitions: |N_exc| <= max(0, 16 - s0); every I with 17 - s0 nulls has a null outside the block of S0\n", nCC))

## D. Example P3.3 (the premise holds with equality at s0 = 1, V = empty: hence the relative tolerance 1e-9)
for (s in c(1, 2, 8, 9, 15)) for (n in c(5000, 20000)) { r <- 17 - s; th <- 0.7; sg <- 1.3; cc <- 1.5
  rho <- sqrt(cc * (sg^2 + s * th^2) * log(n) / ((n - 1) * th^2)); G <- diag(17); G[1:s, (s + 1):17] <- rho; G[(s + 1):17, 1:s] <- rho
  ev <- range(eigen(G, symmetric = TRUE)$values)
  if (max(abs(ev - c(1 - rho * sqrt(s * r), 1 + rho * sqrt(s * r)))) > 1e-8) { viol <- viol + 1L; cat("VIOLATION D eig", s, n, "\n") }
  if (ev[1] <= 0) { cat(sprintf("D: s0=%d n=%d: G not yet positive definite (rho*sqrt(sr)=%.3f); skipped\n", s, n, rho * sqrt(s * r))); next }
  O <- qr.Q(qr(scale(matrix(rnorm(n * 17), n), scale = FALSE))); e <- eigen(G, symmetric = TRUE)
  X <- sqrt(n - 1) * O %*% e$vectors %*% diag(sqrt(e$values)) %*% t(e$vectors); mu <- th * rowSums(X[, 1:s, drop = FALSE]); worst <- Inf
  Vs <- subsets(seq_len(s)); Vs <- Vs[lengths(Vs) < s]; if (length(Vs) > 200) Vs <- c(Vs[1], Vs[sample.int(length(Vs), 199)])
  for (V in Vs) { v <- length(V)
    for (l in c(s + 1, 17)) { u <- if (v) qr.resid(qr(X[, V, drop = FALSE]), X[, l]) else X[, l]; d2 <- sum(u * mu)^2 / sum(u^2)
      f <- (n - 1) * th^2 * (s - v)^2 * rho^2 / (1 - v * rho^2); thr <- cc * (sg^2 + (s - v) * th^2) * log(n)
      if (abs(d2 / f - 1) > 1e-6 || d2 < thr * (1 - 1e-9)) { viol <- viol + 1L; cat("VIOLATION D", s, n, v, d2, f, thr, "\n") }
      worst <- min(worst, d2 / thr) } }
  cat(sprintf("D: s0=%d n=%d: lambda_min(G)=%.3f; min over (V,l) of delta^2/(c tau^2 log n) = %.3f\n", s, n, ev[1], worst)) }
cat(sprintf("TOTAL VIOLATIONS: %d (seed %d)\n", viol, seed))
