# test_tdp.R -- unit tests of the e4 fallback (TDP-E) in start_mode versus brute force.
# Usage: Rscript test_tdp.R <core_dir> <work_dir> <out_txt> [seed] [n_instances]
args <- commandArgs(TRUE)
core <- args[1]; work <- args[2]; out <- args[3]
seed <- if (length(args) >= 4) as.integer(args[4]) else 20261108L
n_inst <- if (length(args) >= 5) as.integer(args[5]) else 3000L
source(file.path(dirname(normalizePath(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)))), "ceng_load.R"))
ceng_load(core, work)
sink(out, split = TRUE)
cat("C-ENG test_tdp.R  seed =", seed, " instances =", n_inst, " date =", format(Sys.time()), "\n")
cat("core =", normalizePath(core), "\n\n")

mk <- function(inst) .v3cpp$t_make_start(inst$p, inst$K, inst$lambda, inst$blocks, inst$logr)
same <- function(a, b) identical(as.integer(a), as.integer(b))

rand_instance <- function(kind) {
  p <- sample(1:14, 1)
  perm <- sample(0:(p - 1))
  # random partition into blocks of size 1..5 (contiguous in a random permutation), then sorted within blocks;
  # block order = the random order of construction (not index order)
  blocks <- list(); i <- 1
  while (i <= p) { m <- min(sample(1:5, 1), p - i + 1); blocks[[length(blocks) + 1]] <- sort(perm[i:(i + m - 1)]); i <- i + m }
  K <- sample(0:p, 1)
  if (kind == "int") {
    lambda <- as.numeric(sample(-2:1, K + 1, replace = TRUE))
    logr <- lapply(blocks, function(b) { v <- as.numeric(sample(-2:2, 2^length(b), replace = TRUE)); v[1] <- 0; v })
  } else if (kind == "flat") {   # massive ties: every nonempty sub-model equal
    lambda <- rep(0, K + 1)
    logr <- lapply(blocks, function(b) { v <- rep(sample(c(-1, 0, 1), 1), 2^length(b)); v[1] <- 0; v })
  } else {                       # real-valued (rounded to 2 decimals: some exact ties, binary64 sums)
    lambda <- round(rnorm(K + 1), 2)
    logr <- lapply(blocks, function(b) { v <- round(rnorm(2^length(b)), sample(c(0, 1, 2), 1)); v[1] <- 0; v })
  }
  # entries with |U| > K are never read; mark them NaN as the production tables do
  logr <- lapply(seq_along(blocks), function(bi) {
    v <- logr[[bi]]; m <- length(blocks[[bi]])
    sz <- vapply(0:(2^m - 1), function(c) sum(bitwAnd(c, 2^(0:(m - 1))) > 0), 0)
    v[sz > K] <- NaN; v })
  list(p = p, K = K, lambda = lambda, blocks = lapply(blocks, as.integer), logr = logr, kind = kind)
}

set.seed(seed)
# C-PACK MR2: the fallback (tie_dp = TRUE) requires cap >= 2; cap 1 is checked separately below
caps <- c(2, 3, 4, 5, 17, 1e6)
mr2 <- list(cap1_rejected = 0, n1_instances = 0, n1_tie_dp_used = 0, n1_not_mode = 0)
tab <- list()
fails <- list()
for (it in seq_len(n_inst)) {
  kind <- c("int", "flat", "real")[(it %% 3) + 1]
  inst <- rand_instance(kind)
  xp <- mk(inst)
  bf <- .v3cpp$t_brute_mode(xp)
  unc <- .v3cpp$t_start_mode(xp, 2e9, FALSE)         # uncapped enumeration = lex-min of E (cap < 2^31: `long` is 32-bit on Windows)
  td <- .v3cpp$t_tdp(xp)
  rec <- list(kind = kind, p = inst$p, K = inst$K, N = bf$N,
              tdp_eq_uncapped = same(td, unc$S), uncapped_eq_brute = same(unc$S, bf$S), tdp_eq_brute = same(td, bf$S))
  for (cap in caps) {
    nw <- .v3cpp$t_start_mode(xp, cap, TRUE); od <- .v3cpp$t_start_mode(xp, cap, FALSE)
    key <- paste0("cap", format(cap, scientific = FALSE))
    rec[[paste0(key, "_trunc")]] <- nw$truncated
    rec[[paste0(key, "_new_eq_uncapped")]] <- same(nw$S, unc$S)
    rec[[paste0(key, "_old_eq_uncapped")]] <- same(od$S, unc$S)
    rec[[paste0(key, "_new_eq_old_when_untrunc")]] <- nw$truncated || (same(nw$S, od$S) && identical(nw$ties, od$ties) && !nw$tie_dp_used)
    rec[[paste0(key, "_lg0_ok")]] <- identical(nw$lg0, bf$lg0) && identical(nw$lg0_direct, bf$lg0) && length(nw$S) == length(bf$S)
    if (!rec[[paste0(key, "_new_eq_uncapped")]] || !rec[[paste0(key, "_new_eq_old_when_untrunc")]] || !rec[[paste0(key, "_lg0_ok")]])
      fails[[length(fails) + 1]] <- list(it = it, cap = cap, inst = inst, new = nw, old = od, unc = unc, bf = bf)
  }
  # MR2: cap = 1 with the fallback is rejected; a unique maximiser (|E| = 1) never takes the fallback at cap >= 2
  if (inherits(tryCatch(.v3cpp$t_start_mode(xp, 1, TRUE), error = function(e) e), "error")) mr2$cap1_rejected <- mr2$cap1_rejected + 1
  if (.v3cpp$t_start_mode(xp, 2e9, FALSE)$ties == 1) {
    mr2$n1_instances <- mr2$n1_instances + 1
    for (cap in caps) { nw1 <- .v3cpp$t_start_mode(xp, cap, TRUE)
      if (nw1$tie_dp_used) mr2$n1_tie_dp_used <- mr2$n1_tie_dp_used + 1
      if (!same(nw1$S, unc$S)) mr2$n1_not_mode <- mr2$n1_not_mode + 1 }
  }
  if (!rec$tdp_eq_uncapped || (kind != "real" && !rec$uncapped_eq_brute))
    fails[[length(fails) + 1]] <- list(it = it, inst = inst, td = td, unc = unc, bf = bf)
  tab[[it]] <- as.data.frame(rec, check.names = FALSE)
}
tab <- do.call(rbind, tab)
cat("instances by kind:\n"); print(table(tab$kind))
cat("\nN (number of smallest-size ghat-maximisers) summary by kind:\n"); print(tapply(tab$N, tab$kind, summary))
cat("\n[A] TDP-E == uncapped enumeration (lex-min E), all kinds:", sum(tab$tdp_eq_uncapped), "/", nrow(tab), "\n")
cat("[B] uncapped enumeration == brute force (ghat), int+flat (exact binary64 sums):",
    sum(tab$uncapped_eq_brute[tab$kind != "real"]), "/", sum(tab$kind != "real"), "\n")
cat("    real-valued kind (FP rounding ties possible; informational):", sum(tab$uncapped_eq_brute[tab$kind == "real"]), "/", sum(tab$kind == "real"), "\n")
cat("[C] TDP-E == brute force, int+flat:", sum(tab$tdp_eq_brute[tab$kind != "real"]), "/", sum(tab$kind != "real"), "\n")
for (cap in caps) {
  key <- paste0("cap", format(cap, scientific = FALSE))
  tr <- tab[[paste0(key, "_trunc")]]
  cat(sprintf("\ncap = %g: truncated in %d instances\n", cap, sum(tr)))
  cat("  [D] new start_mode == lex-min E (all):", sum(tab[[paste0(key, "_new_eq_uncapped")]]), "/", nrow(tab), "\n")
  cat("  [E] new == old bit-for-bit (S, ties, no tie_dp) when not truncated:", sum(tab[[paste0(key, "_new_eq_old_when_untrunc")]]), "/", nrow(tab), "\n")
  cat("  [F] lg0 == brute max and log_gamma0(S) == max, |S| == k*:", sum(tab[[paste0(key, "_lg0_ok")]]), "/", nrow(tab), "\n")
  cat("  old (frozen rule) wrong on truncated instances:", sum(tr & !tab[[paste0(key, "_old_eq_uncapped")]]), "/", sum(tr), "\n")
}
cat("\n[MR2] cap = 1 with tie_dp rejected (error):", mr2$cap1_rejected, "/", nrow(tab),
    "; instances with |E| = 1:", mr2$n1_instances, "; fallback used on them (any cap >= 2):", mr2$n1_tie_dp_used,
    "; returned set != the unique maximiser:", mr2$n1_not_mode, "\n")
cat("\nFAILURES:", length(fails), "\n")
if (length(fails)) { saveRDS(fails, sub("\\.txt$", "_failures.rds", out)); str(fails[[1]], max.level = 2) }

# ---- W1-N3 counterexample: p = 44, K = 22, default cap 1e6 (N3/numerics/cex_default_cap.py) ----
cat("\n---- W1-N3 counterexample (p = 44, K = 22, cap = 1e6) ----\n")
blocks <- c(lapply(0:19, function(i) as.integer(c(2 * i, 2 * i + 1))), list(40:43))
logr <- c(lapply(0:19, function(i) c(0, 1, 1, -10)), list({ v <- rep(-3, 16); v[1] <- 0; v[10] <- 5; v[7] <- 5; v }))
xp <- .v3cpp$t_make_start(44L, 22L, rep(0, 23), blocks, logr)
t0 <- proc.time()[["elapsed"]]; od <- .v3cpp$t_start_mode(xp, 1e6, FALSE); t_old <- proc.time()[["elapsed"]] - t0
t0 <- proc.time()[["elapsed"]]; nw <- .v3cpp$t_start_mode(xp, 1e6, TRUE); t_new <- proc.time()[["elapsed"]] - t0
t0 <- proc.time()[["elapsed"]]; td <- .v3cpp$t_tdp(xp); t_td <- proc.time()[["elapsed"]] - t0
Sstar <- c(seq(0, 38, 2), 40L, 43L); Sold <- c(seq(0, 38, 2), 41L, 42L)
cat("old start_mode: S =", od$S, "\n  lg0 =", od$lg0, " ties =", od$ties, " truncated =", od$truncated, " time =", t_old, "s\n")
cat("old == predicted {0,2,..,38,41,42}:", same(od$S, Sold), "; old == S*:", same(od$S, Sstar), "\n")
cat("new start_mode: S =", nw$S, "\n  lg0 =", nw$lg0, " ties =", nw$ties, " truncated =", nw$truncated, " tie_dp_used =", nw$tie_dp_used, " time =", t_new, "s\n")
cat("new == S* = {0,2,..,38,40,43}:", same(nw$S, Sstar), "; TDP-E alone == S*:", same(td, Sstar), " (", t_td, "s)\n")
cat("log_gamma0(new S) == 25:", nw$lg0_direct == 25, "\n")

# ---- family D_m at small caps (N3 L6): 2^m+... ties; check new == brute for m = 0..8 and caps 2..2^m ----
cat("\n---- family: m inner pairs + last block, caps 2..2^(m+1) ----\n")
bad <- 0; tot <- 0
for (m in 0:8) {
  p <- 2 * m + 4; K <- m + 2
  blocks <- c(lapply(seq_len(m) - 1, function(i) as.integer(c(2 * i, 2 * i + 1))), list(as.integer((2 * m):(2 * m + 3))))
  logr <- c(lapply(seq_len(m), function(i) c(0, 1, 1, -10)), list({ v <- rep(-3, 16); v[1] <- 0; v[10] <- 5; v[7] <- 5; v }))
  xp <- .v3cpp$t_make_start(as.integer(p), as.integer(K), rep(0, K + 1), blocks, logr)
  bf <- .v3cpp$t_brute_mode(xp)
  for (cap in 2:(2^(m + 1) + 1)) {
    nw <- .v3cpp$t_start_mode(xp, cap, TRUE); tot <- tot + 1
    if (!same(nw$S, bf$S)) bad <- bad + 1
  }
}
cat("family checks: new != brute in", bad, "of", tot, "(m, cap) pairs\n")
# ---- rounding fixtures (R01 #2): binary64 rounding ties at the prior and prefix additions ----
cat("
---- rounding fixtures (contract = lex-min E, not lex-min over all rounded ghat-maximisers) ----
")
fx <- list(
  list(name = "R01#2 prior rounding: block {0,1}, K=1, lambda(1)=2^54, rho=(1,2)", p = 2L, K = 1L, lambda = c(0, 2^54),
       blocks = list(0:1), logr = list(c(0, 1, 2, NaN))),
  list(name = "prefix rounding: blocks {0},{1}, K=2, rho0=2^53, rho1=1", p = 2L, K = 2L, lambda = c(0, 0, 0),
       blocks = list(0L, 1L), logr = list(c(0, 2^53), c(0, 1))),
  list(name = "block-sum rounding: blocks {1},{0}, K=2, rho({1})=2^53, rho({0})=1, lambda=0", p = 2L, K = 2L, lambda = c(0, 0, 0),
       blocks = list(1L, 0L), logr = list(c(0, 2^53), c(0, 1))))
for (f in fx) {
  xp <- .v3cpp$t_make_start(f$p, f$K, f$lambda, f$blocks, f$logr)
  bf <- .v3cpp$t_brute_mode(xp); unc <- .v3cpp$t_start_mode(xp, 2e9, FALSE); nw <- .v3cpp$t_start_mode(xp, 2, TRUE)
  cat(f$name, "
  brute(ghat) S = {", bf$S, "} N =", bf$N, "; uncapped E-enumeration S = {", unc$S, "}; new (cap 2) S = {", nw$S,
      "} tie_dp_used =", nw$tie_dp_used, "; new == lex-min E:", same(nw$S, unc$S), "; same value:", identical(nw$lg0_direct, bf$lg0), "
")
}
# ---- boundary fixtures (R01 #6): K = 0, K binding inside a block, interleaved blocks, size-0 optimum ----
cat("
---- boundary fixtures ----
")
bx <- list(
  list(name = "K = 0", p = 3L, K = 0L, lambda = 0, blocks = list(c(0L, 2L), 1L), logr = list(c(0, NaN, NaN, NaN), c(0, NaN))),
  list(name = "K binding inside a block (|C|=3, K=1, all singletons tie)", p = 3L, K = 1L, lambda = c(-5, 0),
       blocks = list(0:2), logr = list(c(0, 7, 7, NaN, 7, NaN, NaN, NaN))),
  list(name = "interleaved blocks {1,3},{0,2}, all pairs tie", p = 4L, K = 2L, lambda = c(0, 0, 0),
       blocks = list(c(1L, 3L), c(0L, 2L)), logr = list(c(0, 1, 1, 0), c(0, 1, 1, 0))),
  list(name = "empty optimum (all rho < 0)", p = 4L, K = 4L, lambda = rep(0, 5), blocks = list(0:1, 2:3),
       logr = list(c(0, -1, -1, -2), c(0, -1, -1, -2))))
for (f in bx) {
  xp <- .v3cpp$t_make_start(f$p, f$K, f$lambda, f$blocks, f$logr)
  bf <- .v3cpp$t_brute_mode(xp); res <- vapply(c(2, 3, 4), function(cap) same(.v3cpp$t_start_mode(xp, cap, TRUE)$S, bf$S), TRUE)
  cat(sprintf("%-60s brute S = {%s}  N = %d  new == brute at caps 2,3,4: %s  TDP-E == brute: %s
", f$name,
      paste(bf$S, collapse = ","), as.integer(bf$N), paste(res, collapse = ","), same(.v3cpp$t_tdp(xp), bf$S)))
}
sink()
