# rm2_common.R -- W3-RM2 sharpness-gate numerics: shared helpers.
# OBSERVATIONS ONLY, never proofs; all theorems are asymptotic.
# Method objects: the partition, the block tables, the prior and the score are read from the PRODUCTION core
# (Scripts/SMC_BVS/core, compiled locally with Rcpp; nothing in the core is edited; no NOTS).
# Two objects are re-implemented here because the production core has no export for them (README.md of the core:
# the start-mode export was removed) and because the coded LS0 rescoring is too slow at |start mode| ~ 100-300:
#   * start_mode_dp(): the start mode S~0 = argmax of gamma_0 on Omega, by the block DP over the production tables
#     (ties broken by first maximum; ties have probability zero in these designs);
#   * ls0_fast(): LS0 re-implemented after cpp/v3_engine.h:379-419 [SW1-3: three boundary departures, see SPEC.md] (one scan = every single flip and every swap; move to
#     the best neighbour on a strict F improvement; cap = ell_n + |centre|), with every neighbour's score obtained
#     from the centre's by exact rank-one updates of the production score
#        log m(U) = -1/2 [log det((n+1) G_U + I) - log det(G_U + I)] - nu log(0.02 + y'y - n z_U' ((n+1)G_U + I)^-1 z_U).
# Both are validated against the production core in validate.R (v3_score on random neighbours; v3_start_logmass).

core_dir <- Sys.getenv("W3RM2_CORE", "C:/Users/felip/BVS-wt/W3-RM2/Scripts/SMC_BVS/core")
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
# Records, at every visited centre that lies in the lattice [S0, Q], the three path-level no-addition margins:
#   naC = max_l F(T+l) - F(T)                    (an improving addition at the centre)
#   naD = max_{e extra, l} F(T-e+l) - F(T-e)     (an addition improving a deletion child = a swap beating its deletion)
#   naE = max_{e extra} F(T) - F(T-e)            (a deletion of an extra that does not improve)
# NA on the lattice implies all three are < 0 at every lattice centre.
ls0_fast <- function(P, centre, cap, S0, Q, tol = 1e-9) {
  S <- sort(centre); moves <- 0L; S0 <- sort(S0)
  inQ <- logical(P$p); inQ[Q] <- TRUE; isT <- logical(P$p); isT[S0] <- TRUE
  types <- character(0); naC <- naD <- naE <- -Inf; nscan <- 0L; limit <- FALSE; lattice_all <- TRUE
  sizes <- length(S)
  repeat {
    sc <- scan_at(P, S); nscan <- nscan + 1L; k <- length(S)
    in_lat <- all(isT[S] | inQ[S]) && all(S0 %in% S)
    lattice_all <- lattice_all && in_lat
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
       naC = naC, naD = naD, naE = naE, lattice_all = lattice_all, sizes = sizes)
}

make_problem <- function(Xs, ys, ctx) {
  XtX <- crossprod(Xs)
  list(XtX = XtX, Xty = as.vector(crossprod(Xs, ys)), yty = sum(ys^2), n = nrow(Xs), p = ncol(Xs), K = ctx$K,
       logw = ctx$log_w - ctx$log_W_K + ctx$log_Cn,   # log prior varpi(k) plus the model-free constant log C_n of log m
       dg = diag(XtX))
}

# Whole-lattice probe: adversarial lattice sets T_tau = S0 + {t in Q \ S0 : noise coordinate of t <= tau} and the
# largest addition margin F(T+l) - F(T) over l not in T (a positive value is a true violation of NA on the lattice).
lattice_probe <- function(P, Xs, eps, S0, Q, taus = c(-1, -0.5, 0, 0.3, 0.61, 1, 1.5)) {
  E <- setdiff(Q, S0); if (!length(E)) return(list(max_margin = NA_real_, at_size = NA_integer_))
  qrS <- qr(Xs[, S0, drop = FALSE]); XE <- qr.resid(qrS, Xs[, E, drop = FALSE])
  ehat <- as.vector(crossprod(XE, eps)) / sqrt(colSums(XE^2))
  best <- -Inf; at <- NA_integer_
  for (tau in taus) for (sgn in c(1, -1)) {
    Tset <- sort(c(S0, E[sgn * ehat <= tau]))
    if (length(Tset) >= P$K) next
    sc <- scan_at(P, Tset, swaps = FALSE)
    mg <- max(sc$Fadd) - sc$FS
    if (mg > best) { best <- mg; at <- length(Tset) }
  }
  list(max_margin = best, at_size = at)
}

# ---------------------------------------------------------------- designs (Gaussian rows; classification NOMINAL)
# s0 = 2 independent truths, theta = (3, 1) (B3: theta_2 weak, n theta_2^2 = wk log n). sigma = 1.
# Leak set: m columns, all weak proxies of truth 1:  x_t = r x_1 + sqrt(1 - r^2) e_t, e_t iid N(0,1), with
#   r = r_n chosen so that the population gain of one proxy given the empty set is G times the start-mode entry level:
#   n r^2 theta_1^2 / tau0^2 = G (log n + 2 log p),  tau0^2 = sigma^2 + |theta|^2,  G = 3.
#   (All proxies on one truth: at most 15 of them can share the truth's block, where they are not visible.)
# type "B1": outside columns iid N(0,1)                                   (leak set orthogonal given S0).
# type "B2": outside columns x_l = cos(a) w_l + sin(a) m^{-1/2} sum_t e_t  (every outside column loads on the common
#            direction of the leak innovations; lattice width large by construction when m >> log n). sin^2(a) = sin2.
# type "B3": B1 with a weak second truth.
# type "B4": B1 plus every outside column leaking from truth 1: x_l = r_eta x_1 + sqrt(1 - r_eta^2) w_l with
#            n r_eta^2 theta_1^2 / tau0^2 = eta log n  (nominal tau-normalised leak level eta at U = empty set).
gen_design <- function(n, p, m, type = "B1", G = 3, sin2 = 0.5, wk = 12, eta = 0, sigma = 1, seed = 1L) {
  set.seed(seed)
  s0 <- 2L; S0 <- 1:s0; theta <- c(3, 1)
  if (type == "B3") theta[2] <- sqrt(wk * log(n) / n)
  tau02 <- sigma^2 + sum(theta^2)
  r <- sqrt(min(0.81, G * (log(n) + 2 * log(p)) * tau02 / (n * theta[1]^2)))
  XT <- matrix(rnorm(n * s0), n, s0)
  E <- matrix(rnorm(n * m), n, m)
  XL <- r * XT[, 1] + sqrt(1 - r^2) * E
  po <- p - s0 - m
  W <- matrix(rnorm(n * po), n, po)
  if (type == "B2") { f <- rowSums(E) / sqrt(m); W <- sqrt(1 - sin2) * W + sqrt(sin2) * f }
  re <- 0
  if (type == "B4" && eta > 0) {
    re <- sqrt(min(0.81, eta * log(n) * tau02 / (n * theta[1]^2)))
    W <- re * XT[, 1] + sqrt(1 - re^2) * W
  }
  X <- cbind(XT, XL, W); rm(XT, XL, W, E)
  Xs <- std_cols(X); rm(X)
  eps <- rnorm(n, sd = sigma)
  mu <- as.vector(Xs[, S0, drop = FALSE] %*% theta)
  list(Xs = Xs, y = mu + eps, eps = eps, S0 = S0, Q = 1:(s0 + m), theta = theta, sigma = sigma, r = r, r_eta = re)
}

# One run: production setup, start mode, LS0 with the shipped cap, old-cap result derived from the same path.
run_one <- function(n, p, b, type, seed, ...) {
  t0 <- proc.time()[3]
  m <- as.integer(ceiling(n^b))
  d <- gen_design(n, p, m, type = type, seed = seed, ...)
  ys <- std_vec(d$y)
  ctx <- v3_context(d$Xs, ys, return_gram = FALSE)
  su <- v3_setup(ctx)
  if (inherits(su, "v3_setup_failed")) return(data.frame(n = n, p = p, b = b, type = type, seed = seed, status = "setup_failed"))
  t1 <- proc.time()[3]
  sm <- start_mode_dp(su)
  P <- make_problem(d$Xs, ys, ctx)
  S0 <- d$S0; Q <- d$Q; St <- sm$S
  n_leak <- sum(St %in% setdiff(Q, S0)); n_out <- sum(!(St %in% Q)); n_miss <- sum(!(S0 %in% St))
  ell <- ell_n(n, p); cap <- ell + length(St)
  ls <- ls0_fast(P, St, cap, S0, Q)
  t2 <- proc.time()[3]
  pr <- lattice_probe(P, d$Xs, d$eps, S0, Q)
  tb <- table(factor(ls$types, levels = unique(c("del_extra", "del_truth", "add_truth", "add_leak", "add_out", ls$types))))
  nd <- sum(ls$types == "del_extra")
  data.frame(n = n, p = p, b = b, type = type, seed = seed, status = "ok", m = m, K = ctx$K, B = su$B, r_proxy = d$r,
             r_eta = d$r_eta, theta2 = d$theta[2], sqrt_n = sqrt(n), log_n = log(n),
             feas = (ctx$K >= 2 * length(Q) + 32 * length(S0) + 1),
             start_size = length(St), start_leak = n_leak, start_out = n_out, start_miss = n_miss,
             sandwich = (n_out == 0 && n_miss == 0),
             moves = ls$moves, cap = cap, ell = ell, limit = ls$limit, certified = ls$certified,
             final_eq_S0 = identical(as.integer(ls$final), as.integer(S0)), final_size = length(ls$final),
             all_del_extra = (ls$moves == nd), n_del_extra = nd, n_other = ls$moves - nd,
             moveseq_other = paste(ls$types[ls$types != "del_extra"], collapse = " "),
             old_cap_ok = (ls$moves <= ell && identical(as.integer(ls$final), as.integer(S0))),
             path_in_lattice = ls$lattice_all, naC = ls$naC, naD = ls$naD, naE = ls$naE,
             path_NA_ok = (max(ls$naC, ls$naD, ls$naE) < 0),
             probe_margin = pr$max_margin, probe_size = pr$at_size, probe_NA_violated = isTRUE(pr$max_margin > 0),
             sec_setup = as.numeric(t1 - t0), sec_ls0 = as.numeric(t2 - t1), stringsAsFactors = FALSE)
}
