# T37 diagnosis on the real p = 20 S1 r001 c100 dataset (regenerated with lowp_generate.R); literal and toward variants, d = 1, 2.
source("C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/lowp/enum/tests/helpers.R")
source(file.path(CAMP_CODE, "lowp/R/lowp_generate.R"))
g <- generate_dataset(20, 1, 1, "prod"); S0 <- truth(20)$active; X <- g$inputs$X; y <- g$inputs$Y[, "c100"]
cat("dataset", g$inputs$dataset_id, " truth", S0, "\n")
options(width = 200)
for (d in 1:2) {
  r <- lowp_td(X, y, S0, d, margin = 0, threads = 8)
  cat(sprintf("\n== d = %d: centres %g, scores %g (formula %g), %.2f s\n", d, r$n_centres, r$scores_used, r$scores_needed, r$seconds))
  f <- function(cl) sapply(cl, function(z) c(centres = z$n_centres, viol = z$n_violating, viol_strict = z$n_violating_strict, min_margin = round(z$min_margin, 4)))
  cat("literal:\n"); print(f(r$clauses)); cat("  TD holds:", r$td_holds, " strict:", r$td_holds_strict, "\n")
  cat("toward:\n"); print(f(r$toward$clauses)); cat("  TD holds:", r$toward$td_holds, " strict:", r$toward$td_holds_strict, "\n")
  cat("literal violators: best move that beats the best target move (counts)\n"); print(r$diagnosis)
  v <- r$violators; v <- v[v$margin < 0 & v$clause != "c", ]
  w <- v[which.min(v$margin), ]; cat("worst literal violator: centre", w$centre, "clause", w$clause, "margin", round(w$margin, 3), "| target", w$g_move, round(w$g_star, 3), "| beaten by", w$o_move, "(", w$o_label, ")", round(w$o_star, 3), "\n")
  vt <- r$toward$violators; vt <- vt[vt$margin < 0, ]
  if (nrow(vt)) { print(table(clause = vt$clause, best_non_reducing_move = vt$o_label)); w <- vt[which.min(vt$margin), ]
    cat("worst toward violator: centre", w$centre, "clause", w$clause, "margin", round(w$margin, 3), "| best reducing", w$g_move, round(w$g_star, 3), "| beaten by", w$o_move, "(", w$o_label, ")", round(w$o_star, 3), "\n") }
}
cat("\nDry-run counts for p = 1000, K = 100, s0 = 14:\n")
for (d in 0:2) { x <- lowp_td_count(1000, 100, 14, 986, d); cat(sprintf("  d=%d: centres %.0f, scores %.0f\n", d, x[["centres"]], x[["scores"]])) }
