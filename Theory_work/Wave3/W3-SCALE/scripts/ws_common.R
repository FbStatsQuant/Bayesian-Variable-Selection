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

# ---- Fit fingerprint -------------------------------------------------------------------------------------------
# Every output field of a fit, hashed (sha256 of R serialisation), after removing the fields that hold wall-clock
# times, memory, or the operational preflight record. Two fits are "output identical" iff their fingerprints agree.
WS_TIMING_NAMES <- c("seconds", "seconds_total", "timings", "runtime_guard", "peak_memory_kb", "seconds_per_score",
                     "est_seconds", "preflight", "preflight_escalation", "allocation")
ws_strip <- function(x) {
  if (is.data.frame(x)) return(x)
  if (is.list(x)) {
    nm <- names(x)
    if (!is.null(nm)) x <- x[!(nm %in% WS_TIMING_NAMES)]
    a <- attributes(x)
    x <- lapply(x, ws_strip)
    attributes(x) <- a[intersect(names(a), c("names", "class"))]
    return(x)
  }
  x
}
ws_sha <- function(x) digest::digest(x, algo = "sha256")
ws_fingerprint <- function(fit) {
  f <- ws_strip(fit)
  top <- vapply(f, ws_sha, "")
  sub <- character(0)
  for (nm in intersect(names(f), c("calibration", "flags", "frozen", "local_search", "ls0", "exact"))) {
    if (is.list(f[[nm]]) && !is.null(names(f[[nm]]))) {
      s <- vapply(f[[nm]], ws_sha, ""); names(s) <- paste0(nm, "$", names(f[[nm]])); sub <- c(sub, s)
    }
  }
  list(all = ws_sha(f), top = top, sub = sub,
       delivery = list(preflight = ws_sha(ws_drop_times(fit$preflight)), preflight_escalation = ws_sha(ws_drop_times(fit$preflight_escalation))))
}
ws_drop_times <- function(x) {
  if (!is.list(x)) return(x)
  x <- x[!(names(x) %in% c("seconds_per_score", "est_seconds", "timing_procedure"))]
  lapply(x, ws_drop_times)
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
