# pop_lib.R -- population (analytic) quantities for the S1/S2 settings (TH-SONG-ASSUMPTIONS, D1).
# Source this from the other scripts.  No data are simulated here: beta (values, positions, signs), Sigma (AR(1) rho) and
# sigma^2 are derived EXACTLY as harness/generate.R does (gen_beta, quad_ar1, sigma2 rule), by sourcing a verbatim copy of it.
# Population Sigma has unit variance, so the standardised-X coefficient equals beta.  Notation:
#   R(S)  = n * Var(x'beta | x_S) = n * b_D' Sigma_{DD.S} b_D,  D = S0 \ S           (nats*sigma^2 scale)
#   price = log((2p-1-s0)/s0) + 0.5*log(n+1)   (P1's "price"; = price(k) of the brief at k = s0-1; see SIMULATION_DATA_ANALYSIS_draft.md Sec 0)
#   Lambda(S) = 0.5*R(S)/sigma2 - (d-m)*price - m*log(p),  d = |S0\S|, m = |S \ S0|   (heuristic log posterior odds S0 : S)
GEN <- Sys.getenv("S1S2_GEN", "/home/fb31/BVS-wt/THEORY-DEPT/.rc_tmp/song/s1s2_ro/harness/generate.R")
SETTINGS_TSV <- Sys.getenv("S1S2_SETTINGS", "/home/fb31/BVS-wt/THEORY-DEPT/.rc_tmp/song/s1s2_ro/specs/settings.tsv")
ENG <- "/home/fb31/Bayesian-Variable-Selection/_local/engineering/reports/S1S2"
source(GEN)                                   # gen_beta, quad_ar1, read_settings (read-only use)

ar1 <- function(a, b, rho) rho^abs(outer(a, b, "-"))

setting_pop <- function(row) {
  row <- as.list(row)
  n <- as.integer(row$n); p <- as.integer(row$p); rho <- as.numeric(row$rho)
  beta <- gen_beta(row); S0 <- which(beta != 0); b0 <- beta[S0]; s0 <- length(S0)
  vmu <- quad_ar1(beta, rho)
  sigma2 <- if (row$suite == 1) 1 else vmu / as.numeric(row$nu)
  price <- log((2 * p - 1 - s0) / s0) + 0.5 * log(n + 1)
  list(row = row, n = n, p = p, rho = rho, S0 = S0, b0 = b0, s0 = s0, vmu = vmu, sigma2 = sigma2, price = price)
}

# R(S)/n pieces: conditional variance of sum_{k in D} b_k x_k given x_S (population)
cvar <- function(D, bD, S, rho) {
  if (length(D) == 0) return(0)
  SDD <- ar1(D, D, rho)
  if (length(S) == 0) return(drop(t(bD) %*% SDD %*% bD))
  SSS <- ar1(S, S, rho); SDS <- ar1(D, S, rho)
  drop(t(bD) %*% (SDD - SDS %*% solve(SSS, t(SDS))) %*% bD)
}
RS <- function(ps, D_idx, N = integer(0)) {       # D_idx: positions within S0 that are deleted; N: null columns added
  keep <- setdiff(seq_len(ps$s0), D_idx)
  S <- c(ps$S0[keep], N)
  ps$n * cvar(ps$S0[D_idx], ps$b0[D_idx], S, ps$rho)
}

# pool of nulls within `dist` of a set of columns
null_pool <- function(ps, around, dist) {
  c0 <- sort(unique(unlist(lapply(around, function(a) seq(a - dist, a + dist)))))
  c0 <- c0[c0 >= 1 & c0 <= ps$p]
  setdiff(c0, ps$S0)
}

# greedy addition of up to mmax nulls from `pool` minimising R; returns R_m (m = 0..mmax) and the chosen N sets
greedy_add <- function(ps, D_idx, pool, mmax) {
  N <- integer(0); Rm <- RS(ps, D_idx, N); Ns <- list(N)
  for (m in seq_len(mmax)) {
    cand <- setdiff(pool, N)
    if (length(cand) == 0) { Rm <- c(Rm, Rm[length(Rm)]); Ns[[m + 1]] <- N; next }
    vals <- vapply(cand, function(c1) RS(ps, D_idx, c(N, c1)), 0)
    N <- c(N, cand[which.min(vals)])
    Rm <- c(Rm, min(vals)); Ns[[m + 1]] <- N
  }
  list(R = Rm, N = Ns)
}

# exhaustive over N subsets of size <= 2 in the pool (used only to check greedy)
exh_add2 <- function(ps, D_idx, pool) {
  best <- c(RS(ps, D_idx), Inf, Inf)               # m = 0,1,2
  for (c1 in pool) { r <- RS(ps, D_idx, c1); if (r < best[2]) best[2] <- r }
  if (length(pool) >= 2) { cm <- combn(pool, 2)
    for (k in seq_len(ncol(cm))) { r <- RS(ps, D_idx, cm[, k]); if (r < best[3]) best[3] <- r } }
  best
}

wilson <- function(x, n, z = 1.959964) {
  ph <- x / n; den <- 1 + z^2 / n
  ctr <- (ph + z^2 / (2 * n)) / den; hw <- z * sqrt(ph * (1 - ph) / n + z^2 / (4 * n^2)) / den
  c(lo = max(0, ctr - hw), hi = min(1, ctr + hw))
}

auc_mw <- function(score, y) {                    # Mann-Whitney AUC with mid-ranks; y logical (positive = TRUE)
  r <- rank(score); n1 <- sum(y); n0 <- sum(!y)
  if (n1 == 0 || n0 == 0) return(NA_real_)
  (sum(r[y]) - n1 * (n1 + 1) / 2) / (n1 * n0)
}

write_tsv <- function(df, path) utils::write.table(df, path, sep = "\t", quote = FALSE, row.names = FALSE, na = "NA")
