#!/usr/bin/env Rscript
# diag_maxit.R -- diagnostic only (not a production setting): refits the two S5 dev cases
# (c100) that failed with glmnet jerr < 0 at maxit = 1e6, with GLMNET$maxit = 1e7 (the
# master's pre-declared G6 action), and reports status, runtime and npasses per fit.
# Usage: Rscript tests/diag_maxit.R <code_dir> <dev_inputs_root> <out_dir>
args <- commandArgs(TRUE)
code_dir <- normalizePath(args[1]); inputs_root <- normalizePath(args[2]); out_dir <- args[3]
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
cfg <- new.env(parent = baseenv()); sys.source(file.path(code_dir, "config.R"), envir = cfg)
S <- cfg$make_settings(); .libPaths(c(S$COMMON$study_lib, .Library)); loadNamespace("glmnet")
E <- new.env(parent = asNamespace("stats"))
for (f in c("common.R", "methods/glmnet_helpers.R", "methods/fit_F2_enet.R")) sys.source(file.path(code_dir, f), envir = E)
S$GLMNET$maxit <- 1e7
out <- list()
for (p in c(500, 1000)) {
  d <- readRDS(file.path(inputs_root, sprintf("p%04d", p), sprintf("dev_p%04d_S5_r001.rds", p)))
  t0 <- proc.time()[["elapsed"]]
  f <- E$fit_F2_enet(d$X, unname(d$Y[, "c100"]), d$foldid, d$method_seed, S)
  rt <- proc.time()[["elapsed"]] - t0
  cat(sprintf("p %d runtime %.1f s statuses %s error %s\n", p, rt, paste(f$rules$status, collapse = ","), f$rules$error[1]))
  if (!is.null(f$diagnostics$fits)) {
    fi <- f$diagnostics$fits
    print(aggregate(npasses ~ alpha, fi, function(x) c(max = max(x), sum = sum(x))))
    cat("max npasses", max(fi$npasses), "max KKT", max(f$diagnostics$kkt), "alpha*", f$diagnostics$chosen$alpha, "\n")
    print(f$rules[, c("rule_id", "status", "k", "alpha", "index", "diag_flag", "diag_codes")])
  }
  out[[paste0("p", p)]] <- list(runtime = rt, rules = f$rules, fits = f$diagnostics$fits)
}
saveRDS(out, file.path(out_dir, "diag_maxit.rds"))
