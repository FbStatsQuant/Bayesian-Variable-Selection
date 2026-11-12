# lem_common.R -- W3-START lemma falsification numerics: shared helpers (base R only; no compiled core).
# FALSIFICATION ATTEMPTS, never proofs. The scorer below is an independent R transcription of the pinned formula
# (STATEMENT.md section 1; Scripts/SMC_BVS/core/cpp/v3_score.h:204-224):
#   log m(S) = log c_n - 1/2 [log det((n+1) G_S + I) - log det(G_S + I)] - nu log(2 b0 + Q_S),
#   Q_S = y'y - n z_S' ((n+1) G_S + I)^{-1} z_S,  nu = a0 + n/2,  a0 = b0 = 0.01   (log c_n dropped: it cancels).
# Tables r_b(U) = m(U)/m(empty) for every U inside a block; gamma0(S) = w(|S|) prod_b r_b(S cap C_b),
# w(k) = 1/2 / choose(2p-1, k); Omega = {|S| <= K}. Everything is computed by brute-force enumeration.

popc <- function(x) { c <- integer(length(x)); while (any(x > 0)) { c <- c + bitwAnd(x, 1L); x <- bitwShiftR(x, 1L) }; c }
mask_of <- function(idx) if (length(idx)) sum(bitwShiftL(1L, idx - 1L)) else 0L      # idx: 1-based positions
idx_of <- function(m) which(bitwAnd(bitwShiftR(m, 0:30), 1L) == 1L)

std_cols <- function(X) { Xc <- sweep(X, 2, colMeans(X)); s <- sqrt(colSums(Xc^2) / (nrow(X) - 1)); sweep(Xc, 2, s, "/") }
std_vec <- function(y) { yc <- y - mean(y); yc / sqrt(sum(yc^2) / (length(y) - 1)) }

logm <- function(Xs, ys, S) {                      # log m(S) - log c_n ; Xs, ys standardised
  n <- nrow(Xs); nu <- 0.01 + n / 2; yty <- sum(ys^2)
  if (!length(S)) return(-nu * log(0.02 + yty))
  XS <- Xs[, S, drop = FALSE]; G <- crossprod(XS); z <- crossprod(XS, ys); k <- length(S)
  H <- (n + 1) * G + diag(k)
  Q <- yty - n * sum(z * solve(H, z))
  -0.5 * (as.numeric(determinant(H)$modulus) - as.numeric(determinant(G + diag(k))$modulus)) - nu * log(0.02 + Q)
}

# log tables of one block: vector of length 2^|Cb| indexed by local mask + 1, log r_b(U) = log m(U) - log m(empty).
block_table <- function(Xs, ys, Cb) {
  nb <- length(Cb); l0 <- logm(Xs, ys, integer(0))
  vapply(0:(2^nb - 1), function(m) logm(Xs, ys, Cb[idx_of(m)]) - l0, 0.0)
}

logw <- function(k, p) -log(2) - lchoose(2 * p - 1, k)

# All table functionals and the exact start by enumeration.
# blocks: list of 1-based index vectors partitioning 1..p; ltab: list of log tables; S0, Q: index vectors (S0 subset Q).
start_enum <- function(p, blocks, ltab, K, S0, Q) {
  s0 <- length(S0); cQ <- length(Q) + 15 * s0
  M <- 0:(2^p - 1); bits <- sapply(0:(p - 1), function(j) bitwAnd(bitwShiftR(M, j), 1L)); size <- rowSums(bits)
  lg <- logw(size, p)
  for (b in seq_along(blocks)) { Cb <- blocks[[b]]; loc <- as.integer(bits[, Cb, drop = FALSE] %*% 2^(0:(length(Cb) - 1))); lg <- lg + ltab[[b]][loc + 1L] }
  ok <- size <= K; lg[!ok] <- -Inf
  mx <- max(lg); g <- exp(lg - mx); Z <- sum(g)
  mS0 <- mask_of(S0); mQ <- mask_of(Q)
  inL <- ok & (bitwAnd(M, mS0) == mS0) & (bitwAnd(M, bitwNot(mQ)) == 0L)
  piL <- sum(g[inL]) / Z; pi0 <- g[mS0 + 1L] / Z
  o0 <- (Z - g[mS0 + 1L]) / g[mS0 + 1L]
  # block-level functionals
  ml <- rep(NA_real_, p); Xi <- numeric(0); en <- 0; T1sum <- 0
  for (b in seq_along(blocks)) {
    Cb <- blocks[[b]]; nb <- length(Cb); lt <- ltab[[b]]; LM <- 0:(2^nb - 1)
    ust <- mask_of(which(Cb %in% S0)); qm <- mask_of(which(Cb %in% Q))
    for (i in seq_len(nb)) { l <- Cb[i]; if (l %in% S0) next
      bit <- bitwShiftL(1L, i - 1L)
      Ts <- LM[bitwAnd(LM, ust) == ust & bitwAnd(LM, bit) == 0L]
      ml[l] <- max(exp(lt[bitwOr(Ts, bit) + 1L] - lt[Ts + 1L]))
      T1sum <- T1sum + exp(lt[bitwOr(ust, bit) + 1L] - lt[ust + 1L])
    }
    if (ust > 0L) {
      Us <- LM[bitwAnd(LM, ust) != ust]
      d <- popc(bitwAnd(ust, bitwNot(Us))); a <- popc(bitwAnd(Us, bitwNot(qm)))
      Tp <- bitwOr(bitwAnd(Us, qm), ust)
      om <- (2 * p)^pmax(d - a, 0) * (cQ / p)^pmax(a - d, 0)
      val <- tapply(om * exp(lt[Us + 1L] - lt[Tp + 1L]), Tp, sum)
      Xi <- c(Xi, max(val))
      en <- max(en, 2 * p * max(exp((lt[Us + 1L] - lt[bitwOr(Us, ust) + 1L]) / d)))
    }
  }
  nulls <- setdiff(seq_len(p), S0); outQ <- setdiff(seq_len(p), Q)
  UQ <- sum(ml[outQ]) / p; U <- sum(ml[nulls]) / p
  T1 <- if (s0 < K) (s0 + 1) / (2 * p - 1 - s0) * T1sum else 0
  list(pi0 = pi0, piL = piL, o0 = o0, T1 = T1, U = U, UQ = UQ, Xi = Xi, en = en, ml = ml, cQ = cQ, s0 = s0,
       maxblock = max(lengths(blocks)), lg = lg, size = size, Mask = M)
}
