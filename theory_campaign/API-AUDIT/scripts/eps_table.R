# Combine the threshold-log first-order eps (thr_table.csv) with the exact index-draw bound:
# eps_index <= U * max_{k <= m} P_k, U = all uniforms read by the 4 final streams (an over-count of index draws),
# m = p + B + 2 the round length (largest multiplier of any index draw). Usage: Rscript eps_table.R <out_dir> <results_dir>
a <- commandArgs(TRUE); out <- a[1]; rs <- a[2]
thr <- read.csv(file.path(rs, "thr_table.csv")); idx <- read.csv(file.path(rs, "index_draw_flips.csv"))
rows <- lapply(1:10, function(i) {
  f <- readRDS(file.path(out, sprintf("fit%02d_fp.rds", i)))
  U <- sum(sapply(f$streams, function(s) s$position_end)); B <- min(floor(sqrt(200)), floor(sqrt(f$design$p)), 16); m <- f$design$p + B + 2  # v3_preprocess.R:22, n = 200
  stopifnot(m <= max(idx$k))
  data.frame(id = i, p = f$design$p, B = B, m = m, U = U, Pk_max = max(idx$prob[idx$k <= m]),
             eps_index_bound = U * max(idx$prob[idx$k <= m]))
})
d <- merge(thr[, c("id", "n_comparisons", "gibbs_sum", "uswap_sum", "nswap_sum", "indep_sum", "resample_sum", "pi0_sum",
                   "eps_first_order")], do.call(rbind, rows), by = "id")
d$eps_total <- d$eps_first_order + d$eps_index_bound
write.csv(d, file.path(rs, "eps_table.csv"), row.names = FALSE)
print(signif(d, 3)); cat("max eps_total over the 10 fits:", signif(max(d$eps_total), 3), "\n")
