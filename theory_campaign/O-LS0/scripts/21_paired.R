# 21_paired.R -- per-dataset pairing of the LS0 records with the PRODUCTION per-fit ledger (S-ELS), aggregation only.
# Usage: Rscript 21_paired.R <OUT dir of 11_run.R (full run)> <S-ELS ledger_per_fit.csv> <results dir>
# The S-ELS ledger (branch theory/S-ELS, theory_campaign/S-ELS/tables/ledger_per_fit.csv) holds, per production fit:
# the reported HPM S_hat and F_hat, F(S0) = F_truth (the fit's own scorer), the class (exact / posterior miss / stopped).
# Question answered here: if LS0 had been added to the production fit (its scored models join the fit's ledger and the
# HPM is re-taken over the union with the production tie rule), would the reported HPM change, and would exact
# recovery be gained or lost? HPM after LS0 = better(prod S_hat, LS0 best-scored model).
# Caveat built in: the LS0 records are on the Owls-regenerated data (bit-level BLAS differences from NOTS, REPORT.md
# "Data"), the production F values on the NOTS data. Cross-data F comparisons are trusted only when the margin exceeds
# TOL = 1e3 * max |F_S0(Owls) - F_truth(NOTS)| (reported); closer calls are counted as "undetermined".
# No engine call: everything comes from the stored RDS records and the ledger CSV.
args <- commandArgs(TRUE)
out <- args[1]; sels <- args[2]; res <- args[3]
fs <- list.files(out, "\\.rds$", recursive = TRUE, full.names = TRUE)
key <- function(v) paste(sort(as.integer(v)), collapse = ";")
L <- do.call(rbind, lapply(fs, function(f) {
  r <- readRDS(f); w <- r$row; a <- r$detail$ls0
  data.frame(case_id = paste0(w$dataset_id, "_", w$scale_key), p = w$p, scenario = w$scenario, scale_key = w$scale_key,
             F_S0 = w$F_S0, F_best = w$F_best, F_end = w$F_endpoint, best = key(a$best_scored), end = key(a$returned),
             S0 = key(r$detail$S0), scored_S0 = w$scored_S0, certified_S0 = w$certified_S0, best_eq_S0 = w$best_eq_S0,
             endpoint_eq_S0 = w$endpoint_eq_S0, start = key(r$detail$start), ell = w$ell, stringsAsFactors = FALSE)
}))
P <- read.csv(sels, stringsAsFactors = FALSE, colClasses = c(S_hat = "character", S0 = "character"))
P$S_hat[is.na(P$S_hat)] <- ""
m <- match(L$case_id, P$case_id)
stopifnot(!anyNA(m))
P <- P[m, ]
stopifnot(identical(L$S0, P$S0))                         # same truth in both
dF0 <- L$F_S0 - P$F_truth
TOL <- max(1e-9, 1e3 * max(abs(dF0)))
lexless <- function(a, b) {                              # HPM tie rule: plain lexicographic, prefix first
  a <- as.integer(strsplit(a, ";")[[1]]); b <- as.integer(strsplit(b, ";")[[1]]); k <- min(length(a), length(b))
  for (i in seq_len(k)) if (a[i] != b[i]) return(a[i] < b[i]); length(a) < length(b)
}
# compare model A (F_A) against model B (F_B): 1 = A strictly better, -1 = B better or equal model, 0 = undetermined
cmp <- function(FA, A, FB, B) {
  if (A == B) return(-1L)
  d <- FA - FB
  if (abs(d) <= TOL) return(if (d == 0) (if (lexless(A, B)) 1L else -1L) else 0L)
  if (d > 0) 1L else -1L
}
done <- P$native_status == "completed"
prod_exact <- done & P$S_hat == P$S0
# HPM with LS0: LS0's best-scored model replaces S_hat iff it beats it
chg <- vapply(seq_len(nrow(L)), function(i) if (!done[i]) NA_integer_ else cmp(L$F_best[i], L$best[i], P$F_hat[i], P$S_hat[i]), 0L)
new_hpm <- ifelse(is.na(chg), NA, ifelse(chg == 1L, L$best, P$S_hat))
ls0_exact <- done & !is.na(chg) & chg != 0L & new_hpm == L$S0
x <- data.frame(L[, c("case_id", "p", "scenario", "scale_key")], prod_class = P$klass, prod_exact = prod_exact,
                F_hat = P$F_hat, F_truth = P$F_truth, F_S0_owls = L$F_S0, dF_S0 = dF0, F_ls0_best = L$F_best,
                F_ls0_end = L$F_end, ls0_best_eq_S0 = L$best_eq_S0, ls0_end_eq_S0 = L$endpoint_eq_S0,
                ls0_scored_S0 = L$scored_S0, ls0_certified_S0 = L$certified_S0, ls0_best_eq_prod = L$best == P$S_hat,
                ls0_changes_hpm = chg == 1L, undetermined = !is.na(chg) & chg == 0L,
                harm = prod_exact & !is.na(chg) & chg == 1L, gain = !prod_exact & ls0_exact,
                end_beats_S0_in_prod_exact = prod_exact & L$F_end > L$F_S0 & L$end != L$S0,
                stringsAsFactors = FALSE)
write.csv(x, file.path(res, "paired_per_fit.csv"), row.names = FALSE)
cells <- unique(x[, c("scale_key", "p", "scenario")])
cells <- cells[order(-match(cells$scale_key, c("c050", "c100")), cells$p, cells$scenario), ]
S <- do.call(rbind, lapply(seq_len(nrow(cells)), function(i) {
  cc <- cells[i, ]; y <- x[x$scale_key == cc$scale_key & x$p == cc$p & x$scenario == cc$scenario, ]
  data.frame(cc, n = nrow(y), prod_completed = sum(!is.na(y$ls0_changes_hpm)),
             prod_exact = sum(y$prod_exact), ls0_alone_exact = sum(y$ls0_best_eq_S0),
             ls0_best_eq_prod = sum(y$ls0_best_eq_prod), ls0_changes_hpm = sum(y$ls0_changes_hpm, na.rm = TRUE),
             undetermined = sum(y$undetermined), harm = sum(y$harm), gain = sum(y$gain),
             with_ls0_exact = sum(y$prod_exact) - sum(y$harm) + sum(y$gain),
             end_beats_S0_in_prod_exact = sum(y$end_beats_S0_in_prod_exact),
             max_abs_dF_S0 = max(abs(y$dF_S0)))
}))
write.csv(S, file.path(res, "paired_cell_summary.csv"), row.names = FALSE)
tot <- colSums(S[, -(1:3)]); tot["max_abs_dF_S0"] <- max(S$max_abs_dF_S0)
writeLines(c(sprintf("fits paired: %d (S-ELS ledger rows matched: %d); same S0 in all", nrow(x), sum(!is.na(m))),
             sprintf("max |F_S0(Owls regenerated) - F_truth(NOTS production)| = %.3g; TOL for cross-data F comparisons = %.3g", max(abs(dF0)), TOL),
             sprintf("min |F_ls0_best - F_hat| over fits where LS0 best != prod S_hat: %.3g",
                     min(abs(x$F_ls0_best - x$F_hat)[!x$ls0_best_eq_prod & !is.na(x$ls0_changes_hpm)])),
             paste(names(tot), tot, sep = " = ", collapse = "; ")), file.path(res, "paired_totals.txt"))
print(S); cat(readLines(file.path(res, "paired_totals.txt")), sep = "\n")
