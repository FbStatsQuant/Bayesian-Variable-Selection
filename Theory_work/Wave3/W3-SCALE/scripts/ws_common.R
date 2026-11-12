# ws_common.R -- shared helpers of the W3-SCALE leg A drivers (profiling and bit-identity).
# No production file is touched: the core is sourced from --core-dir exactly as deployed.

`%||%` <- function(a, b) if (is.null(a)) b else a

ws_args <- function(defaults) {
  a <- commandArgs(trailingOnly = TRUE)
  out <- defaults
  i <- 1
  while (i <= length(a)) {
    k <- sub("^--", "", a[i]); k <- gsub("-", "_", k)
    if (!k %in% names(defaults)) stop("unknown argument --", k)
    out[[k]] <- a[i + 1]; i <- i + 2
  }
  out
}

# Memory of this process in kB (Linux): peak resident (VmHWM) and current resident (VmRSS).
ws_mem <- function() {
  s <- tryCatch(readLines("/proc/self/status"), error = function(e) character(0))
  g <- function(key) { l <- grep(paste0("^", key, ":"), s, value = TRUE); if (length(l)) as.numeric(gsub("[^0-9]", "", l)) else NA_real_ }
  c(hwm_kb = g("VmHWM"), rss_kb = g("VmRSS"))
}
# Reset the peak-resident counter, so the next VmHWM is the peak of the next phase only (Linux >= 4.0; own process).
ws_mem_reset <- function() invisible(tryCatch({ writeLines("5", "/proc/self/clear_refs"); TRUE }, error = function(e) FALSE, warning = function(w) FALSE))

ws_utc <- function() format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC")

# S3-type design at general p (the law of PROD-H scenario 3: Sigma = 0.7 H + 0.3 I, population groups of 5), generated
# in O(np) from a group factor instead of chol(Sigma): x_j = sqrt(0.7) f_g(j) + sqrt(0.3) e_j, then scale().
# Truth: 14 signals, one per active group, groups spaced floor(G/14) apart, positions and coefficients as in PROD-H
# (pos 3,2,4,1,5,3 cycled; beta 1.4,-1.0,1.8,-1.2,0.8,-1.6 cycled). y = c * X beta + eps, sigma = 1.
# This is a profiling generator: it is NOT the PROD-H generator (different draws), only the same design family.
ws_gen_s3 <- function(p, n = 200L, seed, scale_c = 1) {
  stopifnot(p %% 5 == 0, p >= 70)
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(seed)
  G <- p %/% 5; group <- rep(seq_len(G), each = 5)
  f <- matrix(rnorm(n * G), nrow = n)
  X <- sqrt(0.7) * f[, group, drop = FALSE] + sqrt(0.3) * matrix(rnorm(n * p), nrow = n)
  rm(f)
  X <- scale(X, center = TRUE, scale = TRUE)
  attr(X, "scaled:center") <- NULL; attr(X, "scaled:scale") <- NULL
  eps <- rnorm(n)
  k <- 0:13; step <- G %/% 14
  pos <- c(3L, 2L, 4L, 1L, 5L, 3L); pattern <- c(1.4, -1.0, 1.8, -1.2, 0.8, -1.6)
  active <- 5L * (step * k) + pos[(k %% 6L) + 1L]
  beta <- numeric(p); beta[active] <- pattern[(k %% 6L) + 1L]
  y <- scale_c * drop(X %*% beta) + eps
  list(X = X, y = y, active = active, dataset_id = sprintf("s3gen_p%d_seed%d", p, seed), design = "s3gen")
}

# PROD-H dataset regenerated with the frozen study generator (gen_prod_data.R next to this file, which sources
# gen_dev_data.R), checked against the frozen input manifest (x and y sha256). Returns manifest_match.
ws_prodh <- function(p, s, r, scale = "c100", gen_dir, manifest = NULL) {
  env <- new.env()
  # gen_prod_data.R locates gen_dev_data.R through --file=; give it the directory explicitly
  dev <- new.env(); sys.source(file.path(gen_dir, "gen_dev_data.R"), envir = dev)
  src <- readLines(file.path(gen_dir, "gen_prod_data.R"))
  src <- src[!grepl("^sys\\.source\\(file\\.path\\(here\\(\\)", src)]
  env$gen_dev_env <- dev
  eval(parse(text = sub("^gen_dev_env <- new\\.env\\(\\)$", "", src)), envir = env)
  d <- env$generate_prod_dataset(as.integer(p), as.integer(s), as.integer(r))
  inp <- d$inputs
  match <- NA
  if (!is.null(manifest) && file.exists(manifest)) {
    m <- read.csv(manifest, stringsAsFactors = FALSE)
    row <- m[m$dataset_id == inp$dataset_id, , drop = FALSE]
    if (nrow(row) == 1)
      match <- identical(env$f64_sha256(inp$X), row$x_sha256) &&
               identical(env$f64_sha256(inp$Y[, scale]), row[[paste0("y_", scale, "_sha256")]])
  }
  list(X = inp$X, y = unname(inp$Y[, scale]), active = d$truth$active, dataset_id = paste0(inp$dataset_id, "_", scale),
       design = "prodh", method_seed = inp$method_seed, manifest_match = match)
}

# ---- Fit fingerprint (version 2, after review R01 finding 3) -----------------------------------------------------
# Every output field of a fit, hashed (sha256 of R serialisation) after removing ONLY wall-clock and memory numbers:
#  * list elements named seconds, seconds_total, seconds_local, seconds_ls0 (timing vectors of islands, tiers, grids,
#    setup, raw final run), timings, peak_memory_kb -- at any depth;
#  * inside runtime_guard: elapsed_seconds, and per checkpoint elapsed_seconds, operation_seconds, projected_seconds
#    (the guard's label, decisions `exceeded`, allocation and the identity/order of every checkpoint are KEPT);
#  * inside preflight / preflight_escalation: seconds_per_score, est_seconds, timing_procedure (timing benchmark),
#    and the two fields that the v3.2-dev delivery change may alter by design: ls0_worst_case and exceeds. These two
#    go to the separate `delivery` record, compared and reported on its own (equal-admission condition).
# Everything else is kept: allocation, every attribute of every list, the memory part of the preflight.
# Data frames are hashed whole (none of the fit's data frames holds a time).
# Two fits are "output identical" iff fingerprint$all agrees.
WS_FP_VERSION <- 2L
# preflight_ls0 (v3.2-dev B4: the LS0 charge made after the setup) is an admission record that v3.1 does not have; it
# is dropped from the whole-fit hash and reported in the delivery record.
WS_TIME_NAMES <- c("seconds", "seconds_total", "seconds_local", "seconds_ls0", "timings", "peak_memory_kb", "preflight_ls0")
ws_keep <- function(x, drop) { nm <- names(x); if (is.null(nm)) return(x); a <- attributes(x); k <- !(nm %in% drop); x <- unclass(x)[k]
  a$names <- nm[k]; attributes(x) <- a; x }
ws_strip <- function(x, ctx = "") {
  if (is.data.frame(x) || !is.list(x)) return(x)
  drop <- WS_TIME_NAMES
  if (ctx == "guard") drop <- c(drop, "elapsed_seconds")
  if (ctx == "checkpoint") drop <- c(drop, "elapsed_seconds", "operation_seconds", "projected_seconds")
  if (ctx == "preflight") drop <- c(drop, "seconds_per_score", "est_seconds", "timing_procedure", "ls0_worst_case", "exceeds")
  x <- ws_keep(x, drop)
  a <- attributes(x); nm <- names(x)
  y <- lapply(seq_along(x), function(i) {
    ni <- if (is.null(nm)) "" else nm[i]
    sub <- if (ni == "runtime_guard") "guard" else if (ctx == "guard" && ni == "checkpoints") "checkpoints" else if (ctx == "checkpoints") "checkpoint"
           else if (ni %in% c("preflight", "preflight_escalation")) "preflight" else ""
    ws_strip(x[[i]], sub)
  })
  attributes(y) <- a
  y
}
ws_sha <- function(x) digest::digest(x, algo = "sha256")
ws_delivery <- function(pf) {
  if (is.null(pf)) return(NULL)
  l <- pf$ls0_worst_case
  list(exceeds = pf$exceeds, ls0_worst_case = if (is.null(l)) NULL else l[setdiff(names(l), c("seconds_per_score", "est_seconds", "timed"))])
}
ws_fingerprint <- function(fit) {
  f <- ws_strip(fit)
  top <- vapply(f, ws_sha, "")
  sub <- character(0)
  for (nm in intersect(names(f), c("calibration", "flags", "frozen", "local_search", "ls0", "exact", "runtime_guard", "preflight"))) {
    if (is.list(f[[nm]]) && !is.null(names(f[[nm]]))) {
      s <- vapply(f[[nm]], ws_sha, ""); names(s) <- paste0(nm, "$", names(f[[nm]])); sub <- c(sub, s)
    }
  }
  list(version = WS_FP_VERSION, all = ws_sha(f), top = top, sub = sub,
       delivery = list(preflight = ws_delivery(fit$preflight), preflight_escalation = ws_delivery(fit$preflight_escalation),
                       preflight_ls0 = fit$preflight_ls0[setdiff(names(fit$preflight_ls0), c("seconds_per_score", "est_seconds"))]))
}

# Human-readable scalars of a fit (for tables; the fingerprint is the identity test).
ws_scalars <- function(fit) {
  g <- function(x) if (is.null(x)) NA else x
  list(status = g(fit$status), branch = g(fit$branch_run), p = g(fit$p), n = g(fit$n),
       tier = g(fit$settings$tier), escalated = g(fit$flags$escalated), T_final = if (is.null(fit$grid)) NA else length(fit$grid) - 1L,
       log_Z = g(fit$log_Z), log_Z_r = g(fit$log_Z_r), sd_log_Z_r = if (length(fit$log_Z_r) >= 2 && !anyNA(fit$log_Z_r)) stats::sd(fit$log_Z_r) else NA,
       hpm = g(fit$hpm), hpm_F = g(fit$hpm_F), mpm = g(fit$mpm), hpm_phase = g(fit$hpm_provenance$phase),
       numerical_routes = g(fit$numerical_routes), start_mode_ties = g(fit$start_mode$ties),
       near_ties = length(fit$near_ties), ls0_improved = g(fit$ls0_improved),
       fresh_total = if (is.null(fit$score_counts)) NA else sum(fit$score_counts$fresh),
       logical_total = if (is.null(fit$score_counts)) NA else sum(fit$score_counts$logical),
       preflight_exceeds = g(fit$preflight$exceeds), ls0_wc_seconds = g(fit$preflight$ls0_worst_case$est_seconds),
       ls0_wc_requests = g(fit$preflight$ls0_worst_case$requests), runtime_s = g(fit$timings$total),
       peak_memory_kb = g(fit$peak_memory_kb))
}

# ---- Supplementary bit-identity units (not PROD-H): exact branch, ties, small-n budgets, status paths ------------
# Each returns list(X, y, seed, allocation). Inputs are raw (not standardised): v3_fit preprocesses them.
ws_supp <- function(name) {
  RNGkind("Mersenne-Twister", "Inversion", "Rejection")
  gen <- function(n, p, seed, rho = 0.5, s0 = 3) {
    set.seed(seed)
    G <- ceiling(p / 4); f <- matrix(rnorm(n * G), n)
    X <- sqrt(rho) * f[, rep(seq_len(G), each = 4)[seq_len(p)], drop = FALSE] + sqrt(1 - rho) * matrix(rnorm(n * p), n)
    act <- unique(pmin(p, round(seq(1, p, length.out = s0))))
    y <- drop(X[, act, drop = FALSE] %*% rep(c(1.2, -1, 0.8), length.out = length(act))) + rnorm(n)
    list(X = X, y = y)
  }
  dup <- function(d, pairs) { for (k in seq_len(nrow(pairs))) d$X[, pairs[k, 2]] <- pairs[k, 3] * d$X[, pairs[k, 1]]; d }
  alloc <- list(mem_gb = 4, hours = 2)
  d <- switch(name,
    exact_p10 = c(gen(50, 10, 101), seed = 9101),
    exact_p12_dup_const = { d <- gen(40, 12, 102); d <- dup(d, rbind(c(2, 3, 1), c(7, 8, -1))); d$X[, 5] <- 3.5; c(d, seed = 9102) },
    exact_p14_integer = { set.seed(103); X <- matrix(sample(-1:1, 30 * 14, TRUE), 30); storage.mode(X) <- "integer"
                          list(X = X, y = as.integer(X[, 2] - X[, 9] + sample(-2:2, 30, TRUE)), seed = 9103) },
    smc_p40_dup = { d <- gen(60, 40, 104, 0.6, 4); d <- dup(d, rbind(c(1, 2, 1), c(13, 14, -1), c(27, 30, 1), c(39, 40, 1))); c(d, seed = 9104) },
    smc_p60_n30 = c(gen(30, 60, 105, 0.4, 3), seed = 9105),
    smc_p48_integer = { set.seed(106); X <- matrix(sample(-1:1, 80 * 48, TRUE), 80); X[, 48] <- X[, 1]
                        list(X = X + 0, y = drop(X[, c(1, 20, 33)] %*% c(2, -2, 1.5)) + rnorm(80), seed = 9106) },
    # 22 strong signals, each next to an exact copy: the start mode has about 2^22 exactly tied maximisers, so the
    # enumeration is truncated at 1e6 and the e4 tie-aware DP returns the mode (LS0 centre).
    tie_dp_p400 = { set.seed(107); n <- 200; p <- 400; X <- matrix(rnorm(n * p), n)
                    sig <- seq(5, by = 18, length.out = 22); X[, sig + 1] <- X[, sig]
                    list(X = X, y = drop(X[, sig] %*% rep(c(1.5, -1.5), 11)) + rnorm(n), seed = 9107) },
    near_constant = { d <- gen(50, 30, 108); d$X[, 4] <- 1e8 + 1e-7 * d$X[, 4]; d$X[, 9] <- 1 + 2^-40 * round(d$X[, 9] * 8); c(d, seed = 9108) },
    y_constant = { d <- gen(20, 8, 109); d$y <- rep(2, 20); c(d, seed = 9109) },
    no_predictors = list(X = matrix(1, 10, 3), y = rnorm(10), seed = 9110),
    stop("unknown supplementary unit ", name))
  list(X = d$X, y = d$y, seed = d$seed, allocation = alloc, dataset_id = paste0("supp_", name), design = "supp")
}
WS_SUPP_UNITS <- c("exact_p10", "exact_p12_dup_const", "exact_p14_integer", "smc_p40_dup", "smc_p60_n30", "smc_p48_integer",
                   "near_constant", "y_constant", "no_predictors", "tie_dp_p400")
