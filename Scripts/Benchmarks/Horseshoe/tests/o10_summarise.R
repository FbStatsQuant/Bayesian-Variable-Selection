#!/usr/bin/env Rscript
# O10 summary of the long-chain diagnostic (diagnostics only; reads no truth).
# 1. Provenance: each long-chain result belongs to a dev input whose file hash matches the dev
#    inputs manifest; the job's script hash is printed.
# 2. Emulation check: the emulated budget 1k+5k must reproduce the ESS of log tau2 and log sigma2
#    saved by the production dev run (same seed, same iterations), as evidence that slicing the
#    long chain is what bayesreg stores for a given (burnin, n.samples, thin).
# 3. Per candidate budget and p: flag rates (ess_tau, ess_ci95), median and minimum ESS(log tau2),
#    and projected seconds per fit (iterations x measured seconds per iteration, plus the dev
#    run's fixed overhead).
# Usage: Rscript tests/o10_summarise.R <long_dir> <dev_results_dir> <dev_manifest.csv> <dev_inputs_root>
args <- commandArgs(trailingOnly = TRUE)
long_dir <- args[1]; dev_dir <- args[2]; man <- utils::read.csv(args[3], stringsAsFactors = FALSE); inroot <- args[4]
fl <- sort(list.files(long_dir, pattern = "_long\\.rds$", full.names = TRUE))
cat("long-chain results found:", length(fl), "\n")
tabs <- list(); emu <- list(); spi <- list()
for (f in fl) {
  r <- readRDS(f)
  m <- man[man$dataset_id == r$dataset_id, ]
  inp <- file.path(inroot, sprintf("p%04d", r$p), paste0(r$dataset_id, ".rds"))
  ok_in <- identical(digest::digest(file = inp, algo = "sha256"), m$file_sha256)
  b <- r$budgets
  stopifnot(all(b$burnin %% b$thin == 0))     # slicing formula valid only then (bayesreg stores iter %% thin == 0)
  b$ess_log_tau2[!is.finite(b$ess_log_tau2)] <- NA; b$min_ess_ci95[!is.finite(b$min_ess_ci95)] <- NA
  b$p <- r$p
  tabs[[r$dataset_id]] <- b
  dev <- readRDS(file.path(dev_dir, sprintf("p%04d", r$p), paste0(r$dataset_id, "_c100"), "A3.rds"))$diagnostics
  e1 <- b[b$budget == "1k+5k", ]
  emu[[r$dataset_id]] <- data.frame(dataset_id = r$dataset_id, input_hash_ok = ok_in,
    long_ess_log_tau2 = e1$ess_log_tau2, dev_ess_log_tau2 = round(dev$ess_log_tau2, 1),
    long_ess_log_sigma2 = e1$ess_log_sigma2, dev_ess_log_sigma2 = round(dev$ess_log_sigma2, 1),
    long_k = e1$k_ci95, ms_per_iter = round(1000 * r$s_per_iter, 2), host = r$host)
  spi[[r$dataset_id]] <- data.frame(p = r$p, s_per_iter = r$s_per_iter)
}
emu <- do.call(rbind, emu); rownames(emu) <- NULL
cat("\n== Emulation and provenance check (1k+5k from the long chain vs the production dev run) ==\n")
print(emu, row.names = FALSE)
cat("all inputs match the manifest:", all(emu$input_hash_ok),
    "; 1k+5k ESS equal to the dev run (to the 0.1 rounding):",
    all(abs(emu$long_ess_log_tau2 - emu$dev_ess_log_tau2) <= 0.1 & abs(emu$long_ess_log_sigma2 - emu$dev_ess_log_sigma2) <= 0.1), "\n")

all_b <- do.call(rbind, tabs)
spi <- do.call(rbind, spi)
ms <- tapply(spi$s_per_iter, spi$p, max)
cat("\n== Seconds per iteration (max over the 6 datasets of each p; includes post-processing of 60,000 draws) ==\n"); print(round(ms, 5))
summ <- do.call(rbind, lapply(split(all_b, list(all_b$budget, all_b$p), drop = TRUE), function(x) data.frame(
  budget = x$budget[1], p = x$p[1], iterations = x$iterations[1], kept = x$n[1],
  ess_tau_flag = sum(grepl("ess_tau", x$flags)), ess_ci95_flag = sum(grepl("ess_ci95", x$flags)), any_flag = sum(nzchar(x$flags)),
  n = nrow(x), median_ess_tau = median(x$ess_log_tau2, na.rm = TRUE), min_ess_tau = min(x$ess_log_tau2, na.rm = TRUE),
  min_ess_sigma = min(x$ess_log_sigma2, na.rm = TRUE), min_ess_ci95 = min(x$min_ess_ci95, na.rm = TRUE),
  proj_s = round(x$iterations[1] * ms[[as.character(x$p[1])]]))))
summ <- summ[order(summ$p, summ$iterations, summ$kept), ]
cat("\n== Per budget and p (6 datasets each) ==\n"); print(summ, row.names = FALSE)
cat("\n== Per dataset, ESS of log tau2 by budget ==\n")
w <- reshape(all_b[, c("dataset_id", "budget", "ess_log_tau2")], idvar = "dataset_id", timevar = "budget", direction = "wide")
names(w) <- sub("ess_log_tau2.", "", names(w), fixed = TRUE); print(w, row.names = FALSE)
cat("\n== Block means of log tau2 (20 blocks of 3,000 iterations) ==\n")
for (f in fl) { r <- readRDS(f); cat(sprintf("%-20s %s\n", r$dataset_id, paste(sprintf("%.1f", r$block_mean_log_tau2), collapse = " "))) }
cat("\n== Block means of sigma2 ==\n")
for (f in fl) { r <- readRDS(f); cat(sprintf("%-20s %s\n", r$dataset_id, paste(sprintf("%.2f", r$block_mean_sigma2), collapse = " "))) }
utils::write.csv(summ, file.path(long_dir, "o10_budget_summary.csv"), row.names = FALSE)
utils::write.csv(all_b, file.path(long_dir, "o10_budget_by_dataset.csv"), row.names = FALSE)
