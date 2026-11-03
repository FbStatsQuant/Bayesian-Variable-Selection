# score_f3.R -- score the BENCH_F3_PROD adaptive-lasso rerun (lasso cv_min pilot; run 20261102T1252Z_bench_f3v2_prod) against the truth
# with the campaign scoring code (code/scoring: read_rule_rows -> score_selection; failed / missing rows = non-recovery). Truth is read here only.
# Usage: Rscript score_f3.R OUT_DIR
# Writes OUT_DIR/f3_new_rows.csv (one row per case x rule), f3_new_recovery_long.csv (exact /100 per rule x scale x p x scenario),
#        f3_new_checks.txt (counts, statuses, D55 cv_min lambda_last rate). Refuses (exit 1) on anything but 2,400 cases x 6 rules.
out <- commandArgs(trailingOnly = TRUE)[1]
RES <- "C:/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign/results/20261102T1252Z_bench_f3v2_prod"
TRU <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/F_2026-10-19_benchmark_study_n200/Benchmark_Study_20261019/verify/recount/c050/inputs/truth_scoring"
SD <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/scoring"
Sys.setenv(SCORING_DIR = SD); source(file.path(SD, "R", "load_all.R"))
dir.create(out, showWarnings = FALSE, recursive = TRUE)
g <- expand.grid(scale_key = c("c050", "c100"), r = 1:100, s = 1:6, p = c(500L, 1000L), stringsAsFactors = FALSE)
cases <- sprintf("p%04d_S%d_r%03d_%s", g$p, g$s, g$r, g$scale_key)
RULES <- c("cv_min", "cv_1se", "ebic1", "ebic05", "ebic1_K37", "ebic05_K37")
rows <- list(); diag <- list(); nodone <- character(0)
for (cid in cases) {
  d <- file.path(RES, substr(cid, 1, 5), cid)
  if (!file.exists(file.path(d, "F3.done"))) { nodone <- c(nodone, cid); next }      # a unit counts only with its .done marker
  x <- read_rule_rows(file.path(d, "F3.rds"))
  rows[[cid]] <- x
  rr <- readRDS(file.path(d, "F3.rds"))$rows
  diag[[cid]] <- data.frame(case_id = cid, rule_id = rr$rule_id, diag_codes = rr$diag_codes, index = rr$index, stringsAsFactors = FALSE)
}
R <- do.call(rbind, rows); D <- do.call(rbind, diag)
registry <- data.frame(method_id = "F3", rule_id = RULES, role = c("primary", rep("S0", 5)), required = TRUE, in_h4 = TRUE, stringsAsFactors = FALSE)
truth <- list()
for (ds in unique(sub("_c[0-9]{3}$", "", cases))) truth[[ds]] <- sort(as.integer(readRDS(file.path(TRU, substr(ds, 1, 5), paste0(ds, ".rds")))$active))
S <- as.data.frame(score_selection(R, truth, cases, registry))
errs <- c(if (length(nodone)) sprintf("%d cases without F3.done", length(nodone)),
          if (nrow(S) != 2400L * 6L) sprintf("scored rows %d != 14400", nrow(S)),
          if (any(!S$in_expected | !S$in_registry)) "rows outside the expected grid / registry",
          if (anyDuplicated(paste(S$case_id, S$rule_id))) "duplicate case x rule")
if (length(errs)) { cat("SCORE_F3 FAILED:\n ", paste(errs, collapse = "\n  "), "\n"); quit(status = 1) }
utils::write.csv(S, file.path(out, "f3_new_rows.csv"), row.names = FALSE)
A <- aggregate(exact ~ rule_id + scale_key + p + scenario, data = transform(S, exact = as.integer(exact)), FUN = sum)
A$n <- aggregate(exact ~ rule_id + scale_key + p + scenario, data = S, FUN = length)$exact
A <- A[order(A$rule_id, A$scale_key, A$p, A$scenario), ]
stopifnot(all(A$n == 100L))
utils::write.csv(A, file.path(out, "f3_new_recovery_long.csv"), row.names = FALSE)
cvm <- D[D$rule_id == "cv_min", ]
ll <- grepl("lambda_last", cvm$diag_codes)
sink(file.path(out, "f3_new_checks.txt"))
cat("BENCH_F3_PROD scored rows:", nrow(S), " cases:", length(unique(S$case_id)), "\n")
print(table(S$rule_id, S$status))
cat("\npooled exact /600 by rule x scale x p:\n"); print(aggregate(exact ~ rule_id + scale_key + p, data = A, FUN = sum))
cat(sprintf("\nD55: cv_min at the last lambda grid point (diag code lambda_last): %d / %d\n", sum(ll), nrow(cvm)))
print(table(substr(cvm$case_id, 1, 5), sub(".*_", "", cvm$case_id), ll))
sink()
cat("SCORE_F3 OK\n"); cat(readLines(file.path(out, "f3_new_checks.txt")), sep = "\n")
