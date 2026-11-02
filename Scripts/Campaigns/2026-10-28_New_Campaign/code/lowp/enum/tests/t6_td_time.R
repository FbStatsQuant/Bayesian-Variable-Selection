# Check 6c: lowp_td timing (p = 30, s0 = 5, d = 1, 2) and p = 1000 (s0 = 14, d = 0) incl. dry-run counts.
args <- commandArgs(TRUE); th <- as.integer(args[1]); do1000 <- length(args) > 1 && args[2] == "1000"
source("C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/lowp/enum/tests/helpers.R")
lowp_load()
X <- gen_design(30, "block", seed = 77); S0 <- c(3L, 7L, 14L, 16L, 25L); Y <- gen_response(X, S0, c(1.4, -1, 1.8, -1.2, 0.8), cs = c(c100 = 1))
for (d in 1:2) { r <- lowp_td(X, Y[, 1], S0, d, margin = 0, threads = th)
  cat(sprintf("TD p=30 s0=5 d=%d threads=%d: centres %g, scores %g (formula %g), %.2f s, %.2g scores/s; violating a/b/c = %s, min margin a/b/c = %s; TD(d,0) holds: %s\n", d, th, r$n_centres, r$scores_used, r$scores_needed, r$seconds, r$scores_used / r$seconds,
      paste(vapply(r$clauses, `[[`, 0, "n_violating"), collapse = "/"), paste(signif(vapply(r$clauses, `[[`, 0, "min_margin"), 5), collapse = "/"), r$td_holds)) }
cat("dry-run counts p=1000, K=100, s0=14, pool=986:\n")
for (d in 0:1) { x <- lowp_td_count(1000, 100, 14, 986, d); cat(sprintf("TDCOUNT d=%d: centres %.0f, scores %.0f (%.4g)\n", d, x[["centres"]], x[["scores"]], x[["scores"]])) }
if (do1000) {
  X <- gen_design(1000, "block", seed = 5); S0 <- as.integer(5 * (0:13) + c(3, 2, 4, 1, 5, 3, 3, 2, 4, 1, 5, 3, 3, 2)); S0 <- S0 + 0L
  beta <- rep(c(1.4, -1.0, 1.8, -1.2, 0.8, -1.6), length.out = 14)
  Y <- gen_response(X, S0, beta, cs = c(c100 = 1))
  dr <- lowp_td(X, Y[, 1], S0, 0, max_scores = 1e6); cat("dry run p=1000 d=0 returns:", dr$dry_run, format(dr$scores_needed, big.mark = ","), "scores\n")
  r <- lowp_td(X, Y[, 1], S0, 0, margin = 0, threads = th)
  cat(sprintf("TD p=1000 s0=14 d=0 threads=%d: centres %g, scores %g (formula %g), %.1f s, %.3g scores/s; violating a/b/c = %s, min margin a/b/c = %s\n", th, r$n_centres, r$scores_used, r$scores_needed, r$seconds, r$scores_used / r$seconds,
      paste(vapply(r$clauses, `[[`, 0, "n_violating"), collapse = "/"), paste(signif(vapply(r$clauses, `[[`, 0, "min_margin"), 5), collapse = "/")))
}
