#!/usr/bin/env Rscript
# O10 diagnostic (diagnostics only; reads no truth; not a gate). One long bayesreg chain per dev
# dataset at c100 with the production model and seed, burnin = 0, thin = 1, N_LONG kept
# iterations, so the trace starts at iteration 1. Any candidate budget (burn-in B, kept draws N,
# thinning t) is then emulated by taking iterations B + t, B + 2t, ..., B + N t of this chain,
# which is exactly what bayesreg would store with those arguments and the same seed (the
# random-number stream does not depend on burnin or thin, bayesreg.R l. 865-1182).
# Per candidate budget it reports coda ESS of log tau2 and log sigma2, the ci95 set size, the
# minimum coda ESS over the ci95 set, and the flag codes the wrapper would set. It also saves
# the traces of log tau2 and sigma2 and 20 block means, and the time per iteration.
# Usage: Rscript tests/diag_long_chain.R <input.rds> <out_dir> [N_LONG]
args <- commandArgs(trailingOnly = TRUE)
code_dir <- dirname(dirname(normalizePath(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1]))))
sys.source(file.path(code_dir, "config.R"), envir = globalenv())
.libPaths(c(COMMON$LIB, .Library))
sys.source(file.path(code_dir, "common.R"), envir = globalenv())
sys.source(file.path(code_dir, "methods", "fit_A3_horseshoe.R"), envir = globalenv())
for (pk in c("bayesreg", "coda", "digest")) loadNamespace(pk)
RNGkind(COMMON$RNG_KIND[1], COMMON$RNG_KIND[2], COMMON$RNG_KIND[3])

inp <- args[1]; out_dir <- args[2]
N_LONG <- if (length(args) >= 3) as.integer(args[3]) else 60000L
stopifnot(!grepl("/truth/", normalizePath(inp), fixed = TRUE))
d <- readRDS(inp)
y <- unname(d$Y[, "c100"])
s <- make_settings("primary")
s$A3$BURNIN <- 0L; s$A3$N_SAMPLES <- N_LONG; s$A3$THIN <- 1L
t0 <- proc.time()[["elapsed"]]
r <- a3_call(d$X, y, as.integer(d$method_seed), s)
mcmc_s <- elapsed(t0)
if (!is.null(r$error)) stop("bayesreg failed: ", r$error)
B <- r$fit$beta; lt <- log(as.vector(r$fit$tau2)); s2 <- as.vector(r$fit$sigma2)
ess <- function(x) tryCatch(unname(coda::effectiveSize(x)), error = function(e) NA_real_)

budgets <- data.frame(
  label = c("1k+5k", "2k+10k", "5k+10k", "5k+10k/t2", "5k+10k/t5", "10k+10k/t5", "5k+20k", "10k+20k/t2", "10k+50k"),
  burnin = c(1000, 2000, 5000, 5000, 5000, 10000, 5000, 10000, 10000),
  n = c(5000, 10000, 10000, 10000, 10000, 10000, 20000, 20000, 50000),
  thin = c(1, 1, 1, 2, 5, 5, 1, 2, 1))
budgets <- budgets[budgets$burnin + budgets$n * budgets$thin <= N_LONG, ]
rows <- list()
for (i in seq_len(nrow(budgets))) {
  b <- budgets[i, ]
  idx <- b$burnin + b$thin * seq_len(b$n)
  q <- apply(B[, idx, drop = FALSE], 1, stats::quantile, probs = c(0.025, 0.975), names = FALSE, type = 7)
  sel <- which(q[1, ] > 0 | q[2, ] < 0)
  e_sel <- vapply(sel, function(j) ess(B[j, idx]), 0)
  e_tau <- ess(lt[idx]); e_sig <- ess(log(s2[idx]))
  min_sel <- if (length(sel)) min(e_sel) else NA_real_
  codes <- c(if (is.na(e_tau) || e_tau < s$A3$ESS_MIN) "ess_tau",
             if (length(sel) && (is.na(min_sel) || min_sel < s$A3$ESS_MIN)) "ess_ci95")
  rows[[i]] <- data.frame(dataset_id = d$dataset_id, budget = b$label, burnin = b$burnin, n = b$n, thin = b$thin,
                          iterations = b$burnin + b$n * b$thin, ess_log_tau2 = round(e_tau, 1),
                          ess_log_sigma2 = round(e_sig, 1), k_ci95 = length(sel), min_ess_ci95 = round(min_sel, 1),
                          flags = paste(codes, collapse = ";"), stringsAsFactors = FALSE)
}
tab <- do.call(rbind, rows)
blk <- rep(1:20, each = N_LONG / 20)
res <- list(dataset_id = d$dataset_id, p = ncol(d$X), n_long = N_LONG, mcmc_s = mcmc_s,
            s_per_iter = mcmc_s / N_LONG, budgets = tab,
            block_mean_log_tau2 = tapply(lt, blk, mean), block_mean_sigma2 = tapply(s2, blk, mean),
            trace_log_tau2 = lt, trace_sigma2 = s2, host = Sys.info()[["nodename"]])
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
saveRDS(res, file.path(out_dir, paste0(d$dataset_id, "_long.rds")), compress = "xz")
utils::write.csv(tab, file.path(out_dir, paste0(d$dataset_id, "_budgets.csv")), row.names = FALSE)
cat(sprintf("%s p=%d: %d iterations in %.1f s (%.2f ms/iter)\n", d$dataset_id, ncol(d$X), N_LONG, mcmc_s, 1000 * mcmc_s / N_LONG))
cat("block means log tau2 (20 x", N_LONG / 20, "):", sprintf("%.2f", res$block_mean_log_tau2), "\n")
cat("block means sigma2:", sprintf("%.3f", res$block_mean_sigma2), "\n")
print(tab, row.names = FALSE)
