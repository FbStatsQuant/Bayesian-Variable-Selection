# make_lists.R -- case lists for the theory runner (ANALYSIS-H2).
# Usage: Rscript make_lists.R OUT_DIR ROOT_P0500 ROOT_P1000 TAG
#   writes OUT_DIR/cases_<TAG>.tsv (all 2,400) and, for TAG = old, OUT_DIR/td0_sample.tsv (fixed TD d=0 sample, see below).
# TD d=0 sample (fixed before any TD result is seen): replicates {1,25,50,75,100} in every p x S x c cell (120 cases) plus every case whose
# 2026-10-23 HPM missed the truth at c = 1 (from analysis/H_existing_20261030/tables/smc_per_fit.csv, rule hpm, exact == False).
a <- commandArgs(trailingOnly = TRUE); out <- a[1]; roots <- c(`500` = a[2], `1000` = a[3]); tag <- a[4]
g <- expand.grid(scale_key = c("c050", "c100"), r = 1:100, s = 1:6, p = c(500L, 1000L), stringsAsFactors = FALSE)
g$dataset_id <- sprintf("p%04d_S%d_r%03d", g$p, g$s, g$r); g$case_id <- paste0(g$dataset_id, "_", g$scale_key)
g$record <- file.path(roots[as.character(g$p)], g$case_id, "SMCBVS.rds")
L <- g[, c("case_id", "dataset_id", "p", "scale_key", "record")]
stopifnot(nrow(L) == 2400L, !anyDuplicated(L$case_id))
miss_rec <- L$case_id[!file.exists(L$record)]
if (length(a) >= 5 && a[5] == "partial") {   # early start on the folders already pulled + verified; the full list is rebuilt strictly later
  L <- L[file.exists(L$record), ]; tag <- paste0(tag, "_partial"); cat(sprintf("partial: %d records present, %d missing\n", nrow(L), length(miss_rec)))
} else if (length(miss_rec)) stop(sprintf("%d records missing, e.g. %s", length(miss_rec), miss_rec[1]))
utils::write.table(L, file.path(out, paste0("cases_", tag, ".tsv")), sep = "\t", row.names = FALSE, quote = FALSE)
if (tag == "old") {
  pf <- utils::read.csv("C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/analysis/H_existing_20261030/tables/smc_per_fit.csv", stringsAsFactors = FALSE)
  miss <- pf$case_id[pf$rule_id == "hpm" & pf$scale_key == "c100" & pf$exact != "True"]
  fixed <- L$case_id[as.integer(sub(".*_r([0-9]{3})_.*", "\\1", L$case_id)) %in% c(1L, 25L, 50L, 75L, 100L)]
  S <- L[L$case_id %in% union(fixed, miss), ]
  S$sample_reason <- ifelse(S$case_id %in% fixed, ifelse(S$case_id %in% miss, "fixed+c100_miss", "fixed"), "c100_miss")
  S <- S[order(-S$p, S$case_id), ]   # p1000 first (slowest) for load balance
  utils::write.table(S, file.path(out, "td0_sample.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)
  cat(sprintf("td0 sample: %d cases (%d fixed, %d c100 misses, %d both)\n", nrow(S), length(fixed), length(miss), length(intersect(fixed, miss))))
}
cat(sprintf("cases_%s: %d\n", tag, nrow(L)))
