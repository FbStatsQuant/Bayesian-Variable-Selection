#!/usr/bin/env Rscript
# Two-chain stability check of master §III.3.8 (i) and Appendix A O10 (diagnostics only; reads
# no truth). Runs the production wrapper on one dev dataset at c100 with seed = method seed +
# 1,000,000 and the current config.R budget, and compares its ci95 support with the primary
# chain's support saved by a dev run: Jaccard J (J(empty, empty) = 1; a failed chain gives J = 0)
# and the number of coefficients whose ci95 decision differs.
# Usage: Rscript tests/second_chain.R <input.rds> <primary_results_dir> <out_dir>
args <- commandArgs(trailingOnly = TRUE)
code_dir <- dirname(dirname(normalizePath(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1]))))
sys.source(file.path(code_dir, "config.R"), envir = globalenv())
.libPaths(c(COMMON$LIB, .Library))
sys.source(file.path(code_dir, "common.R"), envir = globalenv())
sys.source(file.path(code_dir, "methods", "fit_A3_horseshoe.R"), envir = globalenv())
for (pk in c("bayesreg", "pgdraw", "doParallel", "coda", "digest", "parallel")) loadNamespace(pk)
stopifnot(!grepl("/truth/", normalizePath(args[1]), fixed = TRUE))
d <- readRDS(args[1])
s <- make_settings("primary")
seed2 <- as.integer(d$method_seed) + 1000000L
RNGkind(COMMON$RNG_KIND[1], COMMON$RNG_KIND[2], COMMON$RNG_KIND[3]); set.seed(seed2)
t0 <- proc.time()[["elapsed"]]
w <- fit_A3_horseshoe(d$X, unname(d$Y[, "c100"]), d$foldid, seed2, s)
rt <- elapsed(t0)
prim <- utils::read.csv(file.path(args[2], sprintf("p%04d", ncol(d$X)), paste0(d$dataset_id, "_c100"), "A3.csv"),
                        stringsAsFactors = FALSE, colClasses = c(support = "character"))
to_set <- function(x) if (is.na(x)) NULL else if (x == "") integer(0) else as.integer(strsplit(x, ";")[[1]])
a <- to_set(prim$support[prim$rule_id == "ci95"]); b <- to_set(w$rules$support[w$rules$rule_id == "ci95"])
J <- if (is.null(a) || is.null(b)) 0 else if (length(union(a, b)) == 0L) 1 else length(intersect(a, b)) / length(union(a, b))
n_diff <- if (is.null(a) || is.null(b)) NA_integer_ else length(setdiff(union(a, b), intersect(a, b)))
res <- data.frame(dataset_id = d$dataset_id, p = ncol(d$X), seed2 = seed2, status2 = w$rules$status[1],
                  k_primary = length(a), k_second = length(b), jaccard = J, n_decisions_differ = n_diff,
                  ess_log_tau2_second = round(w$diagnostics$ess_log_tau2, 1),
                  split_rhat_log_tau2_second = round(w$diagnostics$split_rhat_log_tau2, 3),
                  split_rhat_log_sigma2_second = round(w$diagnostics$split_rhat_log_sigma2, 3),
                  support_primary = paste(a, collapse = ";"), support_second = paste(b, collapse = ";"),
                  flags_second = w$rules$diag_codes[1], runtime_s = round(rt, 1))
dir.create(args[3], recursive = TRUE, showWarnings = FALSE)
utils::write.csv(res, file.path(args[3], paste0(d$dataset_id, "_second_chain.csv")), row.names = FALSE)
print(res, row.names = FALSE)
