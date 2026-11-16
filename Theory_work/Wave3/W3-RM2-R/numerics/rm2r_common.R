# rm2r_common.R -- W3-RM2-R boundary numerics (weakened hypotheses (V-flat), (BM-W+), BM(c)): shared helpers.
# Adapted from W3-RM2/numerics/rm2_common.R (parent, read-only). Designs, extended LS0 and run functions are new (below).
# OBSERVATIONS ONLY, never proofs; all theorems are asymptotic.
# Method objects: the partition, the block tables, the prior and the score are read from the PRODUCTION core
# (Scripts/SMC_BVS/core, compiled locally with Rcpp FROM A COPY of the core made in $TMPDIR (so the core directory is never written); nothing in the core is edited; no NOTS).
# Two objects are re-implemented here because the production core has no export for them (README.md of the core:
# the start-mode export was removed) and because the coded LS0 rescoring is too slow at |start mode| ~ 100-300:
#   * start_mode_dp(): the start mode S~0 = argmax of gamma_0 on Omega, by the block DP over the production tables
#     (ties broken by first maximum; ties have probability zero in these designs);
#   * ls0_fast(): LS0 re-implemented after cpp/v3_engine.h:379-419 [SW1-3: three boundary departures, see SPEC.md] (one scan = every single flip and every swap; move to
#     the best neighbour on a strict F improvement; cap = ell_n + |centre|), with every neighbour's score obtained
#     from the centre's by exact rank-one updates of the production score
#        log m(U) = -1/2 [log det((n+1) G_U + I) - log det(G_U + I)] - nu log(0.02 + y'y - n z_U' ((n+1)G_U + I)^-1 z_U).
# Both are validated against the production core in validate.R (v3_score on random neighbours; v3_start_logmass).

core_dir <- Sys.getenv("W3RM2R_CORE", Sys.getenv("W3RM2_CORE", "/home/fb31/BVS-wt/W3-RM2-R/Scripts/SMC_BVS/core"))
suppressMessages(source(file.path(core_dir, "v3.R")))

std_cols <- function(X) {
  Xc <- sweep(X, 2, colMeans(X))
  s <- sqrt(colSums(Xc^2) / (nrow(X) - 1))
  sweep(Xc, 2, s, "/")
}
std_vec <- function(y) { yc <- y - mean(y); yc / sqrt(sum(yc^2) / (length(y) - 1)) }
ell_n <- function(n, p) ceiling(log2(n + p + 1))

.pc_cache <- new.env()
popcount_tab <- function(m) {
  key <- as.character(m)
  if (is.null(.pc_cache[[key]])) {
    x <- 0:(2^m - 1); c <- integer(length(x))
    for (i in 0:(m - 1)) c <- c + bitwAnd(bitwShiftR(x, i), 1L)
    .pc_cache[[key]] <- split(seq_along(x), c)          # indices (code + 1) by popcount 0..m
  }
  .pc_cache[[key]]
}

# Start mode by the block DP on the production tables. Returns sorted 1-based column indices.
start_mode_dp <- function(su) {
  ctx <- su$ctx; K <- ctx$K; logw <- ctx$log_w; J <- length(su$blocks)
  best <- matrix(-Inf, J, 17); arg <- matrix(0L, J, 17); msz <- integer(J)
  for (b in seq_len(J)) {
    lr <- su$tables[[b]]$log_r; m <- length(su$blocks[[b]]); msz[b] <- m
    idx <- popcount_tab(m)
    for (j in 0:m) { ii <- idx[[j + 1]]; w <- ii[which.max(lr[ii])]; best[b, j + 1] <- lr[w]; arg[b, j + 1] <- w - 1L }
  }
  Fm <- rep(-Inf, K + 1); Fm[1] <- 0
  choice <- matrix(0L, J, K + 1)
  for (b in seq_len(J)) {
    Fn <- rep(-Inf, K + 1)
    for (j in 0:min(msz[b], K)) {
      tgt <- (j + 1):(K + 1)
      cand <- best[b, j + 1] + Fm[1:(K + 1 - j)]
      upd <- cand > Fn[tgt]
      if (any(upd)) { Fn[tgt[upd]] <- cand[upd]; choice[b, tgt[upd]] <- j }
    }
    Fm <- Fn
  }
  vals <- logw[1:(K + 1)] + Fm
  k <- which.max(vals) - 1L
  S <- integer(0); r <- k
  for (b in J:1) {
    j <- choice[b, r + 1]
    if (j > 0) { code <- arg[b, j + 1]; mem <- su$blocks[[b]]
      S <- c(S, mem[bitwAnd(bitwShiftR(code, 0:(length(mem) - 1)), 1L) == 1L]) }
    r <- r - j
  }
  stopifnot(r == 0, length(S) == k)
  list(S = sort(S), log_gamma0 = max(vals), size = k)
}

# One LS0 scan at centre S: exact scores F of the centre and of every neighbour.
# P: list(XtX, Xty, yty, n, p, K, logw (length K+1, entry k+1 = log prior of size k), dg = diag(XtX)).
scan_at <- function(P, S, swaps = TRUE) {
  n <- P$n; p <- P$p; nu <- 0.01 + n / 2; k <- length(S); lw <- P$logw
  if (k == 0) {
    s1 <- (n + 1) * P$dg + 1; s2 <- P$dg + 1; tt <- P$Xty
    FS <- lw[1] - nu * log(0.02 + P$yty)
    Fadd <- lw[2] - 0.5 * (log(s1) - log(s2)) - nu * log(0.02 + P$yty - n * tt^2 / s1)
    return(list(FS = FS, Fadd = Fadd, Fdel = numeric(0), Fsw = NULL))
  }
  G <- P$XtX[S, S, drop = FALSE]
  cH <- chol((n + 1) * G + diag(k)); Hi <- chol2inv(cH); ld1 <- 2 * sum(log(diag(cH)))
  cA <- chol(G + diag(k)); Ai <- chol2inv(cA); ld2 <- 2 * sum(log(diag(cA)))
  z <- P$Xty[S]; Hz <- as.vector(Hi %*% z); quad <- sum(z * Hz)
  C2 <- P$XtX[S, , drop = FALSE]
  M1 <- (n + 1) * (Hi %*% C2)
  s1 <- (n + 1) * P$dg + 1 - (n + 1) * colSums(C2 * M1)
  tt <- P$Xty - (n + 1) * as.vector(crossprod(C2, Hz))
  M2 <- Ai %*% C2
  s2 <- P$dg + 1 - colSums(C2 * M2)
  FS <- lw[k + 1] - 0.5 * (ld1 - ld2) - nu * log(0.02 + P$yty - n * quad)
  Fadd <- rep(-Inf, p)
  if (k < P$K) {
    Fadd <- lw[k + 2] - 0.5 * (ld1 + log(s1) - ld2 - log(s2)) - nu * log(0.02 + P$yty - n * (quad + tt^2 / s1))
    Fadd[S] <- -Inf
  }
  dH <- diag(Hi); dA <- diag(Ai)
  Fdel <- lw[k] - 0.5 * (ld1 + log(dH) - ld2 - log(dA)) - nu * log(0.02 + P$yty - n * (quad - Hz^2 / dH))
  Fsw <- NULL
  if (swaps) {
    s1s <- (M1^2) / dH + matrix(s1, k, p, byrow = TRUE)
    ts <- M1 * (Hz / dH) + matrix(tt, k, p, byrow = TRUE)
    s2s <- (M2^2) / dA + matrix(s2, k, p, byrow = TRUE)
    quads <- (quad - Hz^2 / dH) + ts^2 / s1s
    Fsw <- lw[k + 1] - 0.5 * ((ld1 + log(dH)) + log(s1s) - (ld2 + log(dA)) - log(s2s)) - nu * log(0.02 + P$yty - n * quads)
    Fsw[, S] <- -Inf
  }
  list(FS = FS, Fadd = Fadd, Fdel = Fdel, Fsw = Fsw)
}


# LS0 re-implementation (complete scans; improvement > 1e-9; cap = moves allowed; at the cap the CURRENT CENTRE is
# returned, production returns the best neighbour of the last scan). Ties: first maximum (measure zero here). [SW1-3]
# Departures from the production LS0 (cpp/v3_engine.h:379-419): (i) a move needs an improvement > 1e-9 (production: any
# strict improvement); (ii) at the cap the current centre is returned (production: the best improving neighbour of the
# last completed scan); (iii) ties go to the first maximum (production: lexicographic). validate.R does not exercise them.
# Records, at every visited centre T that lies in the lattice [S0, Q], the three path-level no-addition margins:
#   naC = max_l F(T+l) - F(T);  naD = max_{e extra, l} F(T-e+l) - F(T-e);  naE = max_{e extra} F(T) - F(T-e)
# (NA on the lattice implies all three < 0 at every lattice centre), and, at every visited centre T with S0 <= T,
# the truth-removal margin  tl(T) = F(T) - max over truth-removing neighbours A of F(A)  (deletion of a truth, or a swap
# that removes a truth); TL on the lattice means tl(T) > 0.
ls0_fast <- function(P, centre, cap, S0, Q, tol = 1e-9) {
  S <- sort(centre); moves <- 0L; S0 <- sort(S0)
  inQ <- logical(P$p); inQ[Q] <- TRUE; isT <- logical(P$p); isT[S0] <- TRUE
  types <- character(0); naC <- naD <- naE <- -Inf; nscan <- 0L; limit <- FALSE; lattice_all <- TRUE
  tl_all <- numeric(0); tl_first <- NA_real_
  sizes <- length(S)
  repeat {
    sc <- scan_at(P, S); nscan <- nscan + 1L; k <- length(S)
    has_S0 <- all(S0 %in% S)
    in_lat <- has_S0 && all(isT[S] | inQ[S])
    lattice_all <- lattice_all && in_lat
    if (has_S0) {                                   # truth-removal margin at this centre
      it <- match(S0, S)
      rem <- c(sc$Fdel[it], if (!is.null(sc$Fsw)) as.vector(sc$Fsw[it, , drop = FALSE]))
      tl <- sc$FS - max(rem); tl_all <- c(tl_all, tl); if (is.na(tl_first)) tl_first <- tl
    }
    if (in_lat) {
      naC <- max(naC, max(sc$Fadd) - sc$FS)
      ex <- which(!isT[S])
      if (length(ex)) {
        naE <- max(naE, max(sc$FS - sc$Fdel[ex]))
        naD <- max(naD, max(sc$Fsw[ex, , drop = FALSE] - sc$Fdel[ex]))
      }
    }
    ba <- which.max(sc$Fadd); fa <- sc$Fadd[ba]
    if (k > 0) { bd <- which.max(sc$Fdel); fd <- sc$Fdel[bd]; bs <- which.max(sc$Fsw); fs <- sc$Fsw[bs] } else { fd <- -Inf; fs <- -Inf }
    best <- max(fa, fd, fs)
    if (!(best > sc$FS + tol)) break
    if (moves >= cap) { limit <- TRUE; break }
    if (best == fd) { e <- S[bd]; types <- c(types, if (isT[e]) "del_truth" else "del_extra"); S <- S[-bd] }
    else if (best == fa) { types <- c(types, if (isT[ba]) "add_truth" else if (inQ[ba]) "add_leak" else "add_out"); S <- sort(c(S, ba)) }
    else { i <- (bs - 1L) %% k + 1L; l <- (bs - 1L) %/% k + 1L; e <- S[i]
      types <- c(types, paste0("swap_", if (isT[e]) "T" else "x", "_", if (isT[l]) "T" else if (inQ[l]) "leak" else "out"))
      S <- sort(c(S[-i], l)) }
    moves <- moves + 1L; sizes <- c(sizes, length(S))
  }
  list(final = S, moves = moves, limit = limit, certified = !limit, types = types, nscan = nscan,
       naC = naC, naD = naD, naE = naE, lattice_all = lattice_all, sizes = sizes,
       tl_min = if (length(tl_all)) min(tl_all) else NA_real_, tl_first = tl_first,
       tl_last = if (length(tl_all)) tl_all[length(tl_all)] else NA_real_, n_tl = length(tl_all))
}

make_problem <- function(Xs, ys, ctx) {
  XtX <- crossprod(Xs)
  list(XtX = XtX, Xty = as.vector(crossprod(Xs, ys)), yty = sum(ys^2), n = nrow(Xs), p = ncol(Xs), K = ctx$K,
       logw = ctx$log_w - ctx$log_W_K + ctx$log_Cn,   # log prior varpi(k) plus the model-free constant log C_n of log m
       dg = diag(XtX))
}


# ------------------------------------------------------------------ designs
# Design P (Ex-Proxy, FIXED design, exact Gram; STATEMENT section 5 / PARENT lemmas/L6_examples.md:334-347):
#   p = floor(n/3), q = floor(n^b), r^2 = C0 log n / n (C0 = 1), S0 = {1}, Q = {1..q}; e_1..e_p centred orthonormal
#   (QR of a centred Gaussian matrix, seed 1000 + n: fixed per n, the same for every b and seed), z_1 = e_1,
#   z_j = r e_1 + sqrt(1-r^2) e_j (2 <= j <= q), z_j = e_j (j > q), x_j = sqrt(n-1) z_j.  mu = theta_n x_1, sigma = 1.
#   Seeds change the noise only.
design_P_X <- function(n, b, C0 = 1) {
  p <- floor(n / 3); q <- floor(n^b + 1e-9); r <- sqrt(C0 * log(n) / n)
  set.seed(1000L + n)
  Z0 <- matrix(rnorm(n * p), n, p); Z0 <- sweep(Z0, 2, colMeans(Z0))
  E <- qr.Q(qr(Z0))                                    # n x p, orthonormal, orthogonal to 1
  Z <- E
  if (q >= 2) for (j in 2:q) Z[, j] <- r * E[, 1] + sqrt(1 - r^2) * E[, j]
  list(Xs = std_cols(sqrt(n - 1) * Z), p = p, q = q, r = r, S0 = 1L, Q = seq_len(q))
}
# Design G (Gaussian rows, two truths): PARENT design B1 (rm2_common.R gen_design) with the weak truth swept:
#   theta = (3, theta2); the proxy strength r is FIXED by the parent's (3, 1) value of tau0^2, so that the leak set is
#   identical across the sweep (same seed => same X and same noise for every kappa; only theta2 changes).
gen_G <- function(n, p, m, theta2, G = 3, sigma = 1, seed = 1L) {
  set.seed(seed)
  s0 <- 2L; S0 <- 1:s0; theta <- c(3, theta2)
  tau02 <- sigma^2 + sum(c(3, 1)^2)
  r <- sqrt(min(0.81, G * (log(n) + 2 * log(p)) * tau02 / (n * theta[1]^2)))
  XT <- matrix(rnorm(n * s0), n, s0)
  E <- matrix(rnorm(n * m), n, m)
  XL <- r * XT[, 1] + sqrt(1 - r^2) * E
  po <- p - s0 - m
  W <- matrix(rnorm(n * po), n, po)
  X <- cbind(XT, XL, W); rm(XT, XL, W, E)
  Xs <- std_cols(X); rm(X)
  eps <- rnorm(n, sd = sigma)
  mu <- as.vector(Xs[, S0, drop = FALSE] %*% theta)
  list(Xs = Xs, y = mu + eps, eps = eps, mu = mu, S0 = S0, Q = 1:(s0 + m), theta = theta, sigma = sigma, r = r)
}

# Realised delta^2_{U,j} = (u_{U,j}' mu)^2, u_{U,j} = (I - P_U) x_j / ||(I - P_U) x_j||  (PARENT lemmas/L1_sandF_b.md section 0).
delta2 <- function(Xs, mu, j, U) {
  xj <- Xs[, j]
  if (length(U) == 0) { num <- sum(xj * mu); den <- sum(xj^2) }
  else { XU <- Xs[, U, drop = FALSE]; G <- crossprod(XU); sol <- solve(G, cbind(crossprod(XU, xj), crossprod(XU, mu)))
         num <- sum(xj * mu) - sum(crossprod(XU, xj) * sol[, 2]); den <- sum(xj^2) - sum(crossprod(XU, xj) * sol[, 1]) }
  num^2 / den
}
# min over ALL U within the block of j (U subset of C_b(j) \ {j}, |U| <= 15 automatically): the (V_b) quantity.
# Fast form: block Gram with the extra columns j and mu.
delta2_blockmin <- function(Xs, mu, j, blk) {
  B <- setdiff(blk, j); m <- length(B)
  if (m == 0) return(delta2(Xs, mu, j, integer(0)))
  XB <- Xs[, B, drop = FALSE]; G <- crossprod(XB); gj <- as.vector(crossprod(XB, Xs[, j])); cm <- as.vector(crossprod(XB, mu))
  xjmu <- sum(Xs[, j] * mu); xjj <- sum(Xs[, j]^2)
  best <- xjmu^2 / xjj
  for (code in 1:(2^m - 1)) {
    idx <- which(bitwAnd(code, bitwShiftL(1L, 0:(m - 1))) > 0)
    sol <- solve(G[idx, idx, drop = FALSE], cbind(gj[idx], cm[idx]))
    d <- (xjmu - sum(gj[idx] * sol[, 2]))^2 / (xjj - sum(gj[idx] * sol[, 1]))
    if (d < best) best <- d
  }
  best
}

# Mode-margin proxy (design P, n = 400): F(S0) - max over ALL S != S0 with |S| <= 3 of F(S)  (exhaustive, exact scores):
# the empty set, every singleton, every pair, every triple of [p].  Returns F(S0) and the max over the others.
mode_margin_le3 <- function(P, S0) {
  p <- P$p; F0 <- scan_at(P, S0, swaps = FALSE)$FS
  e0 <- scan_at(P, integer(0), swaps = FALSE)
  c1 <- e0$Fadd; c1[S0] <- -Inf                              # singletons other than S0
  best <- max(e0$FS, c1); best1 <- best
  for (i in 1:(p - 1)) {
    s1 <- scan_at(P, i, swaps = FALSE)
    best <- max(best, s1$Fadd[(i + 1):p])                    # pairs {i, j}, j > i
    if (i < p - 1) for (j in (i + 1):(p - 1)) {
      s2 <- scan_at(P, c(i, j), swaps = FALSE)
      best <- max(best, s2$Fadd[(j + 1):p])                  # triples {i, j, k}, k > j
    }
  }
  list(F0 = F0, mm_le1 = F0 - best1, mm_le3 = F0 - best)
}

# ------------------------------------------------------------------ one run
# design: "P" (b given, theta from kappa) or "G" (b = 0.375 fixed, theta2 from kappa).
run_one <- function(design, n, b, kappa, seed, mode_margin = FALSE) {
  t0 <- proc.time()[3]
  lg <- log(n); theta_n <- sqrt(kappa * lg / n)
  if (design == "P") {
    D <- design_P_X(n, b); Xs <- D$Xs; p <- D$p; S0 <- D$S0; Q <- D$Q
    set.seed(5000000L + 1000L * seed + as.integer(n %% 1000))   # noise only; same noise across kappa for a seed
    eps <- rnorm(n); theta <- theta_n; mu <- as.vector(Xs[, 1] * theta_n); y <- mu + eps; theta_min <- theta_n
    rr <- D$r
  } else {
    p <- 2L * n; m <- as.integer(ceiling(n^b))
    D <- gen_G(n, p, m, theta2 = theta_n, seed = seed); Xs <- D$Xs; S0 <- D$S0; Q <- D$Q; y <- D$y; mu <- D$mu
    theta_min <- theta_n; rr <- D$r
  }
  ys <- std_vec(y)
  ctx <- v3_context(Xs, ys, return_gram = FALSE)
  su <- v3_setup(ctx)
  base <- data.frame(design = design, n = n, p = p, b = b, kappa = kappa, seed = seed, stringsAsFactors = FALSE)
  if (inherits(su, "v3_setup_failed")) return(cbind(base, status = "setup_failed"))
  t1 <- proc.time()[3]
  sm <- start_mode_dp(su); St <- sm$S
  P <- make_problem(Xs, ys, ctx)
  blk <- integer(p); for (bb in seq_along(su$blocks)) blk[su$blocks[[bb]]] <- bb
  leakset <- setdiff(Q, S0)
  n_leak <- sum(St %in% leakset); n_out <- sum(!(St %in% Q)); n_miss <- sum(!(S0 %in% St))
  ell <- ell_n(n, p); cap <- ell + length(St)
  ls <- ls0_fast(P, St, cap, S0, Q)
  # lambda_n = (n-1) phi0^2 theta_min^2 / sigma^2 with phi0^2 := lambda_min of the correlation Gram of Q (realised)
  phi02 <- min(eigen(cor(Xs[, Q, drop = FALSE]), symmetric = TRUE, only.values = TRUE)$values)
  lam <- (n - 1) * phi02 * theta_min^2
  # visibility of each truth j: (a) U* = S~0 cap block(j) \ {j};  (b) min over all U within the block of j
  vis_start <- vis_blk <- numeric(length(S0))
  for (a in seq_along(S0)) {
    j <- S0[a]; Ub <- setdiff(intersect(St, su$blocks[[blk[j]]]), j)
    vis_start[a] <- delta2(Xs, mu, j, Ub) / lg
    vis_blk[a] <- delta2_blockmin(Xs, mu, j, su$blocks[[blk[j]]]) / lg
  }
  # weak truth = the swept one (P: truth 1; G: truth 2)
  wk <- if (design == "P") 1L else 2L
  mm <- c(mm_le3 = NA_real_, mm_le1 = NA_real_)
  if (mode_margin) { r3 <- mode_margin_le3(P, S0); mm <- c(mm_le3 = r3$mm_le3, mm_le1 = r3$mm_le1) }
  t2 <- proc.time()[3]
  nd <- sum(ls$types == "del_extra")
  out <- cbind(base, data.frame(status = "ok", q = length(Q), m_leak = length(leakset), K = ctx$K, B = su$B, r_proxy = rr,
    theta_min = theta_min, phi02 = phi02, lam_over_logn = lam / lg, vis_start_wk = vis_start[wk] , vis_blk_wk = vis_blk[wk],
    vis_start_t1 = vis_start[1], vis_blk_t1 = vis_blk[1], stringsAsFactors = FALSE))
  out$vis_start_min <- min(vis_start); out$vis_blk_min <- min(vis_blk)
  out$start_size <- length(St); out$start_leak <- n_leak; out$start_out <- n_out; out$start_miss <- n_miss
  out$truth_incl <- (n_miss == 0); out$sandwich <- (n_out == 0 && n_miss == 0); out$start_in_Q <- (n_out == 0)
  out$wk_in_start <- (S0[wk] %in% St)
  out$moves <- ls$moves; out$cap <- cap; out$ell <- ell; out$limit <- ls$limit; out$certified <- ls$certified
  out$final_eq_S0 <- identical(as.integer(ls$final), as.integer(S0)); out$final_size <- length(ls$final)
  out$end_ok <- out$final_eq_S0 && ls$certified
  out$all_del_extra <- (ls$moves == nd); out$n_del_extra <- nd; out$n_other <- ls$moves - nd
  out$moveseq_other <- paste(ls$types[ls$types != "del_extra"], collapse = " ")
  out$path_in_lattice <- ls$lattice_all; out$naC <- ls$naC; out$naD <- ls$naD; out$naE <- ls$naE
  out$path_NA_ok <- (max(ls$naC, ls$naD, ls$naE) < 0)
  out$tl_min <- ls$tl_min; out$tl_first <- ls$tl_first; out$tl_last <- ls$tl_last; out$n_tl <- ls$n_tl
  out$tl_ok <- isTRUE(ls$tl_min > 0)
  out$mm_le3 <- mm[["mm_le3"]]; out$mm_le1 <- mm[["mm_le1"]]
  out$sec_setup <- as.numeric(t1 - t0); out$sec_ls0 <- as.numeric(t2 - t1)
  out
}
