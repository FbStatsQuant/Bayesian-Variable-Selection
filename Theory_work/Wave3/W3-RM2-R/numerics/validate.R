# validate.R (W3-RM2-R copy of the parent validate.R; gen_design(B1, theta=(3,1)) -> gen_G(theta2 = 1), same construction; V4-V5 added)
# checks of the two re-implemented objects against the PRODUCTION core.
#  V1: scan_at() scores (centre, additions, deletions, swaps) vs v3_score on random neighbours.
#  V2: start_mode_dp(): its log gamma_0 vs the production v3_start_logmass (differences across models), and no model
#      among 2000 perturbations of the mode has larger production start mass.
#  V3: ls0_fast() vs a brute-force LS0 that scores every neighbour with v3_score (small instance).
args <- commandArgs(trailingOnly = TRUE)
here <- if (length(args)) args[1] else "."
source(file.path(here, "rm2r_common.R"))
set.seed(7)
out <- character(0); say <- function(...) { s <- sprintf(...); cat(s, "\n"); out <<- c(out, s) }

# ---- V1
d <- gen_G(300, 600, 30, theta2 = 1, seed = 11L); ys <- std_vec(d$y)
ctx <- v3_context(d$Xs, ys, return_gram = FALSE); P <- make_problem(d$Xs, ys, ctx)
maxerr <- 0; ntest <- 0
for (rep in 1:6) {
  k <- c(0, 1, 5, 12, 25, 40)[rep]; S <- sort(sample(600, k)); sc <- scan_at(P, S)
  maxerr <- max(maxerr, abs(sc$FS - v3_score(ctx, S)$F)); ntest <- ntest + 1
  for (l in sample(setdiff(1:600, S), 15)) { maxerr <- max(maxerr, abs(sc$Fadd[l] - v3_score(ctx, sort(c(S, l)))$F)); ntest <- ntest + 1 }
  if (k > 0) for (i in sample(k, min(k, 8))) {
    maxerr <- max(maxerr, abs(sc$Fdel[i] - v3_score(ctx, S[-i])$F)); ntest <- ntest + 1
    for (l in sample(setdiff(1:600, S), 6)) { maxerr <- max(maxerr, abs(sc$Fsw[i, l] - v3_score(ctx, sort(c(S[-i], l)))$F)); ntest <- ntest + 1 }
  }
}
say("V1 scan_at vs production v3_score: %d scores compared, max |F difference| = %.3e", ntest, maxerr)

# ---- V2
su <- v3_setup(ctx); sm <- start_mode_dp(su)
lm_mode <- v3_start_logmass(su$start, sm$S)
worse <- 0; nper <- 0; maxgain <- -Inf
blk <- integer(600); for (b in seq_along(su$blocks)) blk[su$blocks[[b]]] <- b
for (i in 1:2000) {
  S <- sm$S; a <- sample(3, 1)
  if (a == 1 && length(S) > 0) S <- S[-sample(length(S), 1)] else if (a == 2) S <- sort(unique(c(S, sample(600, 1)))) else if (length(S) > 0) { S <- S[-sample(length(S), 1)]; S <- sort(unique(c(S, sample(600, 1)))) }
  if (identical(S, sm$S)) next
  g <- v3_start_logmass(su$start, S) - lm_mode; nper <- nper + 1; maxgain <- max(maxgain, g); if (g > 1e-9) worse <- worse + 1
}
say("V2 start mode: size %d (leak %d, outside %d); %d perturbations, %d with larger production start mass, max log-mass gain = %.3e",
    length(sm$S), sum(sm$S %in% 3:32), sum(sm$S > 32), nper, worse, maxgain)
# exhaustive single flips
mg <- -Inf
for (j in 1:600) { S <- if (j %in% sm$S) setdiff(sm$S, j) else sort(c(sm$S, j)); mg <- max(mg, v3_start_logmass(su$start, S) - lm_mode) }
say("V2 all 600 single flips of the DP mode: max production log-mass gain = %.3e (must be <= 0)", mg)

# ---- V3 brute force LS0 with production scores
d <- gen_G(120, 80, 10, theta2 = 1, seed = 5L); ys <- std_vec(d$y)
ctx <- v3_context(d$Xs, ys, return_gram = FALSE); P <- make_problem(d$Xs, ys, ctx); su <- v3_setup(ctx); sm <- start_mode_dp(su)
brute <- function(centre, cap) {
  S <- sort(centre); moves <- 0; p <- 80
  repeat {
    FS <- v3_score(ctx, S)$F; best <- -Inf; bS <- NULL
    for (j in 1:p) { T2 <- if (j %in% S) setdiff(S, j) else if (length(S) < ctx$K) sort(c(S, j)) else NULL
      if (!is.null(T2)) { f <- v3_score(ctx, T2)$F; if (f > best) { best <- f; bS <- T2 } } }
    for (e in S) for (l in setdiff(1:p, S)) { T2 <- sort(c(setdiff(S, e), l)); f <- v3_score(ctx, T2)$F; if (f > best) { best <- f; bS <- T2 } }
    if (!(best > FS)) break
    if (moves >= cap) break
    S <- bS; moves <- moves + 1
  }
  list(final = S, moves = moves)
}
ok <- TRUE
for (cen in list(sm$S, sort(sample(80, 12)), sort(c(1:4, sample(5:80, 9))), integer(0))) {
  cap <- ell_n(120, 80) + length(cen)
  a <- ls0_fast(P, cen, cap, d$S0, d$Q); bb <- brute(cen, cap)
  same <- identical(as.integer(a$final), as.integer(bb$final)) && a$moves == bb$moves
  ok <- ok && same
  say("V3 centre size %d: fast LS0 final size %d, moves %d; brute-force (production scores) final size %d, moves %d; identical = %s",
      length(cen), length(a$final), a$moves, length(bb$final), bb$moves, same)
}
# ---- V4: truth-removal margin tl of ls0_fast (path) vs production scores, on a centre containing S0
d <- gen_G(120, 80, 10, theta2 = 1, seed = 5L); ys <- std_vec(d$y)
ctx <- v3_context(d$Xs, ys, return_gram = FALSE); P <- make_problem(d$Xs, ys, ctx)
cen <- sort(c(1:2, 5, 9, 17)); FS <- v3_score(ctx, cen)$F
rem <- c(); for (e in 1:2) { rem <- c(rem, v3_score(ctx, setdiff(cen, e))$F)
  for (l in setdiff(1:80, cen)) rem <- c(rem, v3_score(ctx, sort(c(setdiff(cen, e), l)))$F) }
tl_ref <- FS - max(rem)
a <- ls0_fast(P, cen, 0L, d$S0, d$Q)       # cap 0: the first scan only (centre = cen), so tl_first is its margin
tl4 <- abs(a$tl_first - tl_ref)
say("V4 truth-removal margin at a centre containing S0: ls0_fast %.6f, production-score brute force %.6f, |diff| = %.2e", a$tl_first, tl_ref, tl4)
# ---- V5: design P exact Gram, and delta2 / delta2_blockmin vs direct projection
D <- design_P_X(400, 0.45); X <- D$Xs; G <- crossprod(X) / 399
v5a <- max(abs(G[1:D$q, 1:D$q] - ((1 - D$r^2) * diag(D$q) + D$r^2 * matrix(1, D$q, D$q))[1:D$q, 1:D$q] - (matrix(0, D$q, D$q))))
Gt <- diag(D$q); Gt[1, 2:D$q] <- Gt[2:D$q, 1] <- D$r; Gt[2:D$q, 2:D$q] <- D$r^2 * (1 - diag(D$q - 1)) + diag(D$q - 1)   # exact target Gram on Q
v5a <- max(abs(G[1:D$q, 1:D$q] - Gt)); v5b <- max(abs(G[-(1:D$q), -(1:D$q)] - diag(D$p - D$q)))
mu <- 0.3 * X[, 1]; U <- c(3, 5, 8)
Pu <- X[, U] %*% solve(crossprod(X[, U]), t(X[, U])); ru <- as.vector((diag(400) - Pu) %*% X[, 1]); uu <- ru / sqrt(sum(ru^2))
v5c <- abs(delta2(X, mu, 1, U) - sum(uu * mu)^2)
bm <- delta2_blockmin(X, mu, 1, 1:5); bm2 <- min(sapply(0:15, function(cd) { idx <- which(bitwAnd(cd, bitwShiftL(1L, 0:3)) > 0); delta2(X, mu, 1, 1 + idx) }))
say("V5 design P: max |Gram - target| on Q %.2e, off Q %.2e; delta2 vs direct projection %.2e; block-min vs enumeration %.2e", v5a, v5b, v5c, abs(bm - bm2))
say("VALIDATION %s", if (maxerr < 1e-6 && worse == 0 && mg <= 1e-9 && ok && tl4 < 1e-6 && v5a < 1e-8 && v5b < 1e-8 && v5c < 1e-8 && abs(bm - bm2) < 1e-8) "PASSED" else "FAILED")
writeLines(out, file.path(here, "validate_out.txt"))
