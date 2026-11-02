args <- commandArgs(TRUE)
stopifnot(length(args) == 2L)
cat("worker_pid", Sys.getpid(), "started_utc", format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC"), "\n")
flush.console()
run_case <- function() {
id <- args[1L]; scale <- args[2L]
root <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/repro/snapshot_2a8362b2f348"
deployed <- "C:/Users/felip/Documents/NOTS_BVS/NOTS_home/projects/BVS/Benchmarks"
study <- "C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/dev"
out <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/repro/controlled_2a8362b2f348"
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
  checks <- c(rows = identical(as.list(rr), as.list(old$result$rules)), beta = identical(new$result$beta, old$result$beta),
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
runs$case <- id; runs$scale <- scale; runs$process_id <- Sys.getpid()
runs$finished_utc <- format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC")
runs$input_sha256 <- digest::digest(file = file.path(study, "inputs", pkey, paste0(id, ".rds")), algo = "sha256")
runs$snapshot_tree <- "2a8362b2f348f45bbce4a547ed95ef6455cc704e148d1d799adb804f3acdaa67"
runs$session_info <- capture.output(sessionInfo())
original_path <- file.path("C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/repro", paste0(id, "_", scale, ".rds"))
original <- if (file.exists(original_path)) readRDS(original_path) else NULL
runs$pilot_identity_original_F1 <- !is.null(original) &&
  identical(runs$F3$result$diagnostics$pilot$beta, original$F1$new$result$beta)
frozen <- new.env(parent = globalenv())
sys.source("C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/F_2026-10-19_benchmark_study_n200/Benchmark_Study_20261019/scoring/derived_rules/derive_rules.R", frozen)
runs$checks <- list()
for (method in c("F1", "F2", "F3")) {
  obj <- if (method == "F3") runs$F3$result else runs[[method]]$new$result
  setting <- load_code(root, method)$settings
  tb <- frozen$method_tables(list(diagnostics = obj$diagnostics, settings = setting), method)
  if (is.null(tb)) {
    runs$checks[[method]] <- list(k37 = c(FALSE, FALSE), support = rep(FALSE, nrow(obj$rules)))
    next
  }
  dr <- frozen$derive_case(tb, method, ncol(d$X))$rules
  k37 <- vapply(c("ebic1_K37", "ebic05_K37"), function(rid) {
    row <- obj$rules[obj$rules$rule_id == rid, ]
    identical(row$support, dr[[rid]]$key) && identical(row$k_valid_max, dr[[rid]]$k_valid_max) &&
      isTRUE(all.equal(row$crit_value, dr[[rid]]$crit, tolerance = 0))
  }, logical(1))
  evidence <- vapply(seq_len(nrow(obj$rules)), function(i) {
    row <- obj$rules[i, ]; beta <- obj$coefficients[[i]]$beta_pen
    key <- if (row$status == "failed") row$support_audit else row$support
    identical(paste(which(beta != 0), collapse = ";"), key)
  }, logical(1))
  runs$checks[[method]] <- list(k37 = k37, support = evidence)
}
if (scale == "c100") {
  cat("fitting deployed ridge F3\\n"); flush.console()
  ridge <- fit(load_code(deployed, "F3"))
  truth <- readRDS(file.path(study, "truth", pkey, paste0(id, ".rds")))$active
  key <- paste(sort(truth), collapse = ";")
  rdiag <- function(o, version) {
    if (is.null(o$diagnostics$candidates)) return(list(noise_below_weakest_truth = NA_integer_,
      truth_inside_screen = NA, truth_on_path = NA, ebic1_K37_exact = NA))
    if (version == "ridge") {
      w <- o$diagnostics$w; keep <- seq_len(ncol(d$X))
      cand <- o$diagnostics$candidates; j <- which(cand$valid & cand$k <= 37)
      j <- j[order(cand$ebic1[j], cand$k[j], cand$key[j], method = "radix")[1]]
      chosen <- cand$key[j]
    } else {
      w <- rep(Inf, ncol(d$X)); keep <- o$diagnostics$keep; w[keep] <- o$diagnostics$w
      chosen <- o$rules$support[o$rules$rule_id == "ebic1_K37"]
    }
    list(noise_below_weakest_truth = sum(w[-truth] < max(w[truth])),
         truth_inside_screen = all(truth %in% keep),
         truth_on_path = key %in% o$diagnostics$path$key,
         ebic1_K37_exact = identical(chosen, key))
  }
  runs$ridge <- ridge
  runs$truth_diagnostic <- list(ridge = rdiag(ridge$result, "ridge"), v2 = rdiag(runs$F3$result, "v2"))
}
saveRDS(runs, file.path(out, paste0(id, "_", scale, ".rds")), version = 3)
cat("checks F1:", paste(runs$F1$checks, collapse = ","), "F2:", paste(runs$F2$checks, collapse = ","),
    "pilot:", runs$pilot_identical, "\n")
cat("F3:", paste(capture.output(print(runs$F3$result$rules[, c("rule_id", "status", "k")])), collapse = "\n"), "\n")
cat("finish", format(Sys.time(), tz = "UTC", usetz = TRUE), "\n")
}
status <- tryCatch({ run_case(); 0L }, error = function(err) {
  message("FATAL: ", conditionMessage(err)); 1L
})
outdir <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/repro/controlled_2a8362b2f348"
writeLines(as.character(status), file.path(outdir, paste0(args[1], "_", args[2], ".script_exit")))
quit(save = "no", status = status)
