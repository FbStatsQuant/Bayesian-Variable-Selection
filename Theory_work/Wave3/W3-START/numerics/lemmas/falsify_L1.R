# falsify_L1.R -- falsification attempt for lemmas/L1_AGG_FLOOR.md (claims (C0), (T0)). Base R; exact enumeration.
# Part A: RANDOM POSITIVE TABLES (AGG uses only positivity of the tables and the prior formula): checks (AGG-a) in the
#         sharper form 1 - 1/F, (AGG-b) both sides incl. o0 >= c_s Xi, (AGG-c), (AGG-d), and assembly inequality (e2).
# Part B: REAL SCORER on random data incl. rank-deficient designs: one-step ratio >= (n+1)^(-1/2), FLOOR, T1 >= f_n(s0).
# A violation prints a line starting with "VIOLATION". Usage: Rscript falsify_L1.R [nA] [nB] [seed]
args <- commandArgs(TRUE)
nA <- if (length(args) >= 1) as.integer(args[1]) else 4000L
nB <- if (length(args) >= 2) as.integer(args[2]) else 400L
seed <- if (length(args) >= 3) as.integer(args[3]) else 20261111L
src <- sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)); source(file.path(dirname(src), "lem_common.R"))
set.seed(seed); tol <- 1e-9
viol <- 0L; cnt <- c(a = 0, b_up = 0, b_lo = 0, b_cs = 0, c = 0, d = 0, e2 = 0); tight <- list(a = c(), b = c(), c = c())
rand_partition <- function(p, maxb) { perm <- sample(p); out <- list(); i <- 1
  while (i <= p) { sz <- min(sample(maxb, 1), p - i + 1); out[[length(out) + 1]] <- sort(perm[i:(i + sz - 1)]); i <- i + sz }; out }

for (rep in seq_len(nA)) {
  p <- sample(4:11, 1); maxb <- sample(1:4, 1); blocks <- rand_partition(p, maxb); mb <- max(lengths(blocks))
  K <- mb + sample.int(p - mb + 1L, 1L) - 1L; stopifnot(mb <= K, K <= p)   # not sample(mb:p, 1): misreads mb == p
  s0 <- sample(0:min(K, 4), 1); S0 <- sort(sample(p, s0))
  qx <- sample(0:min(K - s0, 3), 1); rest <- setdiff(seq_len(p), S0)
  Q <- sort(c(S0, if (qx > 0) rest[sample.int(length(rest), qx)]))     # sample.int: sample(x, k) misreads a length-1 x
  stopifnot(!anyDuplicated(Q), all(S0 %in% Q), length(Q) <= K)
  regime <- sample(3, 1)                      # 1: additive log-table, nulls penalised; 2: wild; 3: near threshold
  ltab <- lapply(blocks, function(Cb) { nb <- length(Cb); LM <- 0:(2^nb - 1)
    coef <- ifelse(Cb %in% S0, runif(nb, 2, 9), -runif(nb, c(2, 0, 0.5)[regime], c(8, 3, 2)[regime]))
    B <- sapply(0:(nb - 1), function(j) bitwAnd(bitwShiftR(LM, j), 1L)); if (is.null(dim(B))) B <- matrix(B, ncol = nb)
    lt <- as.numeric(B %*% coef) + rnorm(2^nb, 0, c(0.5, 2, 0.3)[regime]); lt[1] <- 0; lt })
  r <- start_enum(p, blocks, ltab, K, S0, Q); cQ <- r$cQ
  prodXiQ <- prod(1 + r$Xi)                                  # Xi computed at this Q
  if (r$UQ < 1) {                                            # (AGG-a)
    Fq <- prodXiQ * (1 - r$UQ)^(-(cQ + 1)); cnt["a"] <- cnt["a"] + 1
    if (1 - r$piL > (1 - 1 / Fq) * (1 + tol) + tol) { viol <- viol + 1L; cat("VIOLATION AGG-a rep", rep, 1 - r$piL, 1 - 1 / Fq, "\n") }
    if (1 - r$piL > 1e-12) tight$a <- c(tight$a, (1 - 1 / Fq) / (1 - r$piL))
    if (r$UQ <= 0.25 && (cQ + 1) * r$UQ <= 0.25 && s0 * max(c(r$Xi, 0)) <= 0.5) {   # (e2)
      cnt["e2"] <- cnt["e2"] + 1
      if (Fq - 1 > 2 * s0 * max(c(r$Xi, 0)) + (8 / 3) * (cQ + 1) * r$UQ + tol) { viol <- viol + 1L; cat("VIOLATION e2 rep", rep, "\n") }
    }
    # (AGG-c): needs m_l for l in Q \ S0 (start_enum computes m_l for every l outside S0) and e_n
    QmS <- setdiff(Q, S0); cnt["c"] <- cnt["c"] + 1
    rhs <- (1 + r$en)^s0 * (1 - r$UQ)^(-(length(Q) + 1)) * prod(1 + length(Q) * r$ml[QmS] / p)
    if (1 / r$pi0 > rhs * (1 + tol)) { viol <- viol + 1L; cat("VIOLATION AGG-c rep", rep, 1 / r$pi0, rhs, "\n") }
    tight$c <- c(tight$c, rhs * r$pi0)
  }
  if (s0 >= 1 && cQ * r$UQ <= 1) {                           # (AGG-d)
    cnt["d"] <- cnt["d"] + 1
    if (max(r$Xi) > 2^16 * max(r$en, r$en^16) * (1 + tol)) { viol <- viol + 1L; cat("VIOLATION AGG-d rep", rep, "\n") }
  }
  r0 <- if (identical(Q, S0)) r else start_enum(p, blocks, ltab, K, S0, S0)   # (AGG-b) is at Q = S0
  if (s0 < K) {
    if (r0$T1 > r0$o0 * (1 + tol)) { viol <- viol + 1L; cat("VIOLATION T1<=o0 rep", rep, "\n") }
    if (r0$T1 > (s0 + 1) * r0$U * (1 + tol)) { viol <- viol + 1L; cat("VIOLATION T1<=(s0+1)U rep", rep, "\n") }
    cnt["b_lo"] <- cnt["b_lo"] + 1
    if (r0$U < 1) {
      R2 <- (1 - r0$U)^(-(s0 + 1)) - 1 - (s0 + 1) * r0$U
      up <- r0$T1 + R2 + (prod(1 + r0$Xi) - 1) * (1 - r0$U)^(-(16 * s0 + 1)); cnt["b_up"] <- cnt["b_up"] + 1
      if (r0$o0 > up * (1 + tol) + tol) { viol <- viol + 1L; cat("VIOLATION AGG-b upper rep", rep, r0$o0, up, "\n") }
      if (r0$o0 > 1e-12) tight$b <- c(tight$b, up / r0$o0)
    }
    if (s0 >= 1 && s0 + mb <= K) {            # every S_U is feasible (the statement's s0 + 16 <= K for blocks <= 16)
      cs <- (64 * s0)^(-16); cnt["b_cs"] <- cnt["b_cs"] + 1
      if (r0$o0 < cs * max(r0$Xi) * (1 - tol)) { viol <- viol + 1L; cat("VIOLATION o0>=c_s Xi rep", rep, "\n") }
      # sharper intermediate claim of the proof: w(s0-d+a)/w(s0) >= c_s omega(U) for all (d, a) possible
      for (d in 1:min(s0, 16)) for (a in 0:15) if (s0 - d + a <= p) {
        lhs <- exp(logw(s0 - d + a, p) - logw(s0, p)); om <- (2 * p)^max(d - a, 0) * (16 * s0 / p)^max(a - d, 0)
        if (lhs < cs * om * (1 - tol)) { viol <- viol + 1L; cat("VIOLATION prior-vs-omega", p, s0, d, a, "\n") } }
    }
  }
}
cat(sprintf("Part A: %d random-table cases; checks run: %s\n", nA, paste(names(cnt), cnt, sep = "=", collapse = " ")))
qs <- function(x) if (length(x)) paste(signif(quantile(x, c(0, .1, .5, .9, 1)), 3), collapse = " / ") else "-"
cat("  tightness bound/actual (min / 10% / median / 90% / max):\n   AGG-a (1-1/F)/(1-piL):", qs(tight$a), "\n   AGG-b upper/o0:", qs(tight$b), "\n   AGG-c rhs*pi0:", qs(tight$c), "\n")

# ---- Part B: FLOOR with the real scorer ----
cntB <- c(step = 0, floor = 0, T1 = 0); minstep <- Inf; minfl <- Inf
for (rep in seq_len(nB)) {
  n <- sample(c(4:12, 20, 40), 1); p <- sample(2:8, 1)
  X <- matrix(rnorm(n * p), n, p)
  kind <- sample(4, 1)
  if (kind == 2 && p >= 2) X[, 2] <- X[, 1]                                  # exact duplicate (rank deficient)
  if (kind == 3 && p >= 3) X[, 3] <- X[, 1] + X[, 2]                         # exact collinearity
  if (kind == 4 && p >= 2) X[, 2] <- X[, 1] + 1e-3 * rnorm(n)                # near duplicate
  Xs <- std_cols(X); beta <- c(sample(c(0, 0, 1, 3), p, TRUE)); y <- X %*% beta * sample(c(0, 1, 10), 1) + rnorm(n)
  ys <- std_vec(y); K <- min(p, n %/% 2)
  maxb <- min(K, 4); blocks <- rand_partition(p, maxb)
  ltab <- lapply(blocks, function(Cb) block_table(Xs, ys, Cb))
  # one-step ratios for every model S with |S| < K and every l (the claim (FLOOR)(iii), all models not only block sets)
  M <- 0:(2^p - 1); sz <- popc(M); lm_all <- vapply(M, function(m) if (popc(m) <= K) logm(Xs, ys, idx_of(m)) else NA_real_, 0.0)
  for (m in M[sz < K]) for (l in seq_len(p)) if (bitwAnd(m, bitwShiftL(1L, l - 1L)) == 0L) {
    rt <- exp(lm_all[bitwOr(m, bitwShiftL(1L, l - 1L)) + 1L] - lm_all[m + 1L]) * sqrt(n + 1); cntB["step"] <- cntB["step"] + 1
    minstep <- min(minstep, rt)
    if (rt < 1 - 1e-7) { viol <- viol + 1L; cat("VIOLATION FLOOR step rep", rep, "n", n, "p", p, "ratio*sqrt(n+1)", rt, "\n") }
  }
  r <- start_enum(p, blocks, ltab, K, integer(0), integer(0)); g <- exp(r$lg - max(r$lg)); Z <- sum(g)
  for (m in M[sz < K]) { k <- sz[m + 1]; f <- (k + 1) * (p - k) / ((2 * p - 1 - k) * sqrt(n + 1)); cntB["floor"] <- cntB["floor"] + 1
    one_minus <- 1 - g[m + 1] / Z; minfl <- min(minfl, one_minus / (f / (1 + f)))
    if (one_minus < f / (1 + f) * (1 - 1e-7)) { viol <- viol + 1L; cat("VIOLATION FLOOR pi0 rep", rep, "\n") }
    if (f / (1 + f) < (1 / 3) / sqrt(n + 1) - 1e-12) { viol <- viol + 1L; cat("VIOLATION f/(1+f)>=1/(3 sqrt(n+1))\n") } }
  s0 <- sample(0:max(0, K - 1), 1); S0 <- sort(sample(p, s0)); r0 <- start_enum(p, blocks, ltab, K, S0, S0)
  if (s0 < K) { f <- (s0 + 1) * (p - s0) / ((2 * p - 1 - s0) * sqrt(n + 1)); cntB["T1"] <- cntB["T1"] + 1
    if (r0$T1 < f * (1 - 1e-7) || r0$o0 < r0$T1 * (1 - 1e-7)) { viol <- viol + 1L; cat("VIOLATION T0 chain rep", rep, "\n") } }
}
cat(sprintf("Part B: %d data sets; checks run: %s\n  min one-step ratio*sqrt(n+1) = %.6f (claim >= 1); min (1-pi0(S))/(f/(1+f)) = %.4f (claim >= 1)\n",
            nB, paste(names(cntB), cntB, sep = "=", collapse = " "), minstep, minfl))
cat("TOTAL VIOLATIONS:", viol, "\n")
