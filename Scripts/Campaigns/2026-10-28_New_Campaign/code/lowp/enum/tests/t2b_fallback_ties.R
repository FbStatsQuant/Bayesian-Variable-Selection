# Check 2 (fallback routing) and tie/dropped-column cases against the core's v3_enumerate.
source("C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/lowp/enum/tests/helpers.R")
lowp_load(); cpp <- .lowp$cpp; load_core_ref()
## --- forced fallback (test hooks) at p = 12 -------------------------------------------------------------------
p <- 12; X <- gen_design(p, "block", seed = 5); Y <- gen_response(X, c(2, 7, 11), c(1.4, -1, 1.8))
Yl <- list(c100 = Y[, 1], c050 = Y[, 2])
base <- lowp_exact(X, Yl, collect_F = TRUE, return_raw = TRUE, task_bits = 4)
pr <- attr(base, "run")$prep; masks <- as.numeric(0:(2^p - 1))
sref <- lapply(1:2, function(s) cpp$cpp_score_masks(pr$X, pr$Y[, s], pr$orig, masks, 2L)$F)
cat("-- pivot-failure hook: variables 3 and 6 (1-based) forced to fail\n")
h1 <- lowp_exact(X, Yl, collect_F = TRUE, fail_vars = c(2L, 5L), task_bits = 4)
n_with <- sum(bitwAnd(0:(2^p - 1), bitwOr(2^2, 2^5)) != 0)
for (s in 1:2) { nn <- h1[[s]]$numerics; Fa <- attr(h1, "run")$F_all[[s]]
  cat(sprintf("scale %s: fallback=%d (expected models containing var 3 or 6: %d), slow_subtree=%d, nonidentical F vs Scorer=%d, logZ diff vs no-hook=%.3g, hpm same=%s\n",
      names(h1)[s], nn$n_fallback_v3, n_with, nn$n_fallback_slow_subtree, sum(Fa != sref[[s]]), abs(h1[[s]]$log_Z - base[[s]]$log_Z), identical(h1[[s]]$hpm, base[[s]]$hpm))) }
cat("-- Q-threshold hook: qthr = 0.2 (every model with Q/y'y < 0.2 is rescored by Scorer::score)\n")
h2 <- lowp_exact(X, Yl, collect_F = TRUE, qthr = 0.2, task_bits = 4)
for (s in 1:2) { nn <- h2[[s]]$numerics; Fa <- attr(h2, "run")$F_all[[s]]
  cat(sprintf("scale %s: fallback=%d, of which Q-rule=%d, slow=%d, nonidentical F vs Scorer=%d\n", names(h2)[s], nn$n_fallback_v3, nn$q_recomputed, nn$n_fallback_slow_subtree, sum(Fa != sref[[s]]))) }
d <- cpp$cpp_dfs_F(pr$X, pr$Y, pr$orig, masks, 1e-8, c(2L, 5L))
cat("cpp_dfs_F with failing vars: fallback flag set exactly for models containing var 3 or 6: ",
    identical(as.integer(d$fallback[, 1]), as.integer(bitwAnd(0:(2^p - 1), bitwOr(2^2, 2^5)) != 0)), "; nonidentical F vs Scorer:", sum(d$F[, 1] != sref[[1]]), "\n")
## --- exact ties: a duplicated column; dropped constant column -------------------------------------------------
cat("-- ties: column 10 = column 3 (exact duplicate), column 6 constant (dropped), p_raw = 12\n")
X2 <- gen_design(12, "block", seed = 8); X2[, 10] <- X2[, 3]; X2[, 6] <- 1
Y2 <- gen_response(X2, c(3, 8, 11), c(1.4, -1, 1.8), seed = 6)
ex <- lowp_exact(X2, list(c100 = Y2[, 1], c050 = Y2[, 2]), threads = 3, task_bits = 3)
for (sc in c("c100", "c050")) {
  pre <- v3_preprocess(X2, Y2[, sc], dup_components = FALSE)
  ctx <- v3_context(pre$X, pre$y, orig = pre$kept, return_gram = FALSE); ref <- v3_enumerate(ctx); e <- ex[[sc]]
  topref <- vapply(ref$top$models, function(m) paste(m, collapse = ";"), ""); nt <- length(topref)
  ties <- sum(duplicated(e$top$F[1:nt]) | duplicated(e$top$F[1:nt], fromLast = TRUE))
  cat(sprintf("%s: p_ret=%d models=%g==%g; logZ diff=%.2g; max dPIP=%.2g; hpm=%s same=%s; top(%d) models same=%s F bits=%s (tied-F entries in compared top: %d); names(pip)=%s\n",
    sc, length(e$pip), attr(ex, "run")$models_scored, ref$models_scored, abs(e$log_Z - ref$log_Z), max(abs(e$pip - ref$pip)), paste(e$hpm, collapse = ";"),
    identical(as.integer(e$hpm), as.integer(ref$hpm)), nt, identical(topref, e$top$model[1:nt]), same_bits(ref$top$value, e$top$F[1:nt]), ties,
    paste(names(e$pip), collapse = ",")))
}
cat("bitmask order vs v3::hpm_better mismatches (3e6 random pairs, ties in F forced):", cpp$cpp_order_check(3e6L, 30L, 5L), "\n")
