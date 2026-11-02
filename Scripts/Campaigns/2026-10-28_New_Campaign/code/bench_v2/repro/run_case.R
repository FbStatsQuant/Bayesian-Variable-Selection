args <- commandArgs(TRUE)
stopifnot(length(args) == 2L)
id <- args[1L]; scale <- args[2L]
root <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2"
deployed <- "C:/Users/felip/Documents/NOTS_BVS/NOTS_home/projects/BVS/Benchmarks"
study <- "C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/dev"
out <- file.path(root, "repro")
pkey <- substr(id, 5L, 9L)
d <- readRDS(file.path(study, "inputs", pkey, paste0(id, ".rds")))
y <- unname(d$Y[, scale])
suppressPackageStartupMessages(library(glmnet))
glmnet::glmnet.control(fdev = 0, devmax = 1)
load_code <- function(root, method) {
  folder <- c(F1 = "F1_Lasso", F2 = "F2_ElasticNet", F3 = "F3_AdaptiveLasso")[[method]]
  fitfile <- c(F1 = "fit_F1_lasso.R", F2 = "fit_F2_enet.R", F3 = "fit_F3_alasso.R")[[method]]
  cfg <- new.env(parent = globalenv())
  sys.source(file.path(root, folder, "config.R"), cfg)
  settings <- switch(method, F1 = { s <- as.list(cfg); s$variant <- "primary"; s },
                     F2 = cfg$make_settings("primary"), F3 = cfg$study_settings("primary"))
  e <- new.env(parent = globalenv())
  for (f in c("common.R", "methods/glmnet_helpers.R", paste0("methods/", fitfile)))
    sys.source(file.path(root, folder, f), e)
  # Local-only compatibility with glmnet 4.1-10: same override as audit mgr_checks.
  e$assert_pkg_version <- function(...) invisible(TRUE)
  e$glmnet_target_path <- function(Xd, yd, alpha, lam, pf, G) {
    s <- sqrt(mean(yd^2)); m <- alpha + s * (1 - alpha)
    fit <- glmnet::glmnet(Xd, yd, family = "gaussian", alpha = alpha / m,
      lambda = lam * m, penalty.factor = pf, intercept = FALSE, standardize = FALSE,
      type.gaussian = G$type_gaussian, thresh = G$thresh, maxit = G$maxit)
    e$check_glmnet_path(fit, lam * m, G)
    B <- as.matrix(fit$beta); scale <- max(1, max(abs(crossprod(Xd, yd))) / nrow(Xd))
    list(B = B, s = s, m = m, a = alpha / m, jerr = fit$jerr, npasses = fit$npasses,
         kkt = e$kkt_glmnet(Xd, yd, B, lam, alpha, pf, scale))
  }
  environment(e$glmnet_target_path) <- environment()
  list(env = e, settings = settings, fn = get(c(F1 = "fit_F1_lasso", F2 = "fit_F2_enet",
                                                 F3 = "fit_F3_alasso")[[method]], envir = e))
}
fit <- function(code) {
  t <- proc.time()[["elapsed"]]
  val <- code$fn(d$X, y, as.integer(d$foldid), d$method_seed, code$settings)
  list(result = val, seconds = unname(proc.time()[["elapsed"]] - t))
}
cat("case:", id, scale, "start", format(Sys.time(), tz = "UTC", usetz = TRUE), "\n")
runs <- list()
for (method in c("F1", "F2")) {
  cat("fitting", method, "deployed\n"); flush.console()
  old <- fit(load_code(deployed, method))
  cat("fitting", method, "v2\n"); flush.console()
  new <- fit(load_code(root, method))
  rr <- new$result$rules[match(old$result$rules$rule_id, new$result$rules$rule_id), , drop = FALSE]
  rownames(rr) <- rownames(old$result$rules)
  checks <- c(rows = identical(rr, old$result$rules), beta = identical(new$result$beta, old$result$beta),
              diagnostics = identical(new$result$diagnostics, old$result$diagnostics),
              converged = identical(new$result$converged, old$result$converged))
  diffs <- lapply(names(checks)[!checks], function(z) switch(z,
    rows = all.equal(old$result$rules, rr, tolerance = 0),
    beta = all.equal(old$result$beta, new$result$beta, tolerance = 0),
    diagnostics = all.equal(old$result$diagnostics, new$result$diagnostics, tolerance = 0),
    converged = all.equal(old$result$converged, new$result$converged, tolerance = 0)))
  names(diffs) <- names(checks)[!checks]
  runs[[method]] <- list(old = old, new = new, checks = checks, differences = diffs)
}
cat("fitting F3 v2\n"); flush.console()
runs$F3 <- fit(load_code(root, "F3"))
runs$pilot_identical <- identical(runs$F3$result$diagnostics$pilot$beta, runs$F1$new$result$beta)
runs$case <- id; runs$scale <- scale
saveRDS(runs, file.path(out, paste0(id, "_", scale, ".rds")), version = 3)
cat("checks F1:", paste(runs$F1$checks, collapse = ","), "F2:", paste(runs$F2$checks, collapse = ","),
    "pilot:", runs$pilot_identical, "\n")
cat("F3:", paste(capture.output(print(runs$F3$result$rules[, c("rule_id", "status", "k")])), collapse = "\n"), "\n")
cat("finish", format(Sys.time(), tz = "UTC", usetz = TRUE), "\n")
