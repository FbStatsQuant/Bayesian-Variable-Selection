#!/usr/bin/env Rscript
# G3 unit tests for A3 Horseshoe (master §III.3.8 i, tests 1-10, and the A3 parts of the
# §IV.3 unit-test list: null canary, failure path, no-oracle grep, runner-order determinism).
# Fixtures are frozen here (TEST_SEED = 20261019). Tests 1, 2 and 5 are stochastic: run once,
# outcome recorded, then used as a gate. Tests 3-8 and the canaries use the test budget
# (burnin 500 + 1,000 draws), labelled non-production; test 10 uses the production settings.
# Usage: Rscript tests/test_A3_horseshoe.R <output_dir>

A3_TEST_CODE_DIR <- local({
  f <- grep("^--file=", commandArgs(FALSE), value = TRUE)
  if (length(f)) dirname(dirname(normalizePath(sub("^--file=", "", f[1])))) else getwd()
})

a3_test_setup <- function(code_dir) {
  sys.source(file.path(code_dir, "config.R"), envir = globalenv())
  .libPaths(c(COMMON$LIB, .Library))
  sys.source(file.path(code_dir, "common.R"), envir = globalenv())
  sys.source(file.path(code_dir, "methods", "fit_A3_horseshoe.R"), envir = globalenv())
  sys.source(file.path(code_dir, "run_case.R"), envir = globalenv())   # run_fit_safely, main (not run)
  # check_outputs.R and score_dev.R define their own main(); load them apart and keep only the
  # functions the tests use (check_run, flag_crn; neither reads truth).
  e_chk <- new.env(); sys.source(file.path(code_dir, "check_outputs.R"), envir = e_chk)
  e_scr <- new.env(); sys.source(file.path(code_dir, "score_dev.R"), envir = e_scr)
  assign("check_run", e_chk$check_run, envir = globalenv())
  assign("flag_crn", e_scr$flag_crn, envir = globalenv())
  RNGkind(COMMON$RNG_KIND[1], COMMON$RNG_KIND[2], COMMON$RNG_KIND[3])
}

test_budget_settings <- function() {
  s <- make_settings("primary")
  s$A3$N_SAMPLES <- 1000L
  s$A3$BURNIN <- 500L
  s
}

# Test 5 fixture: n = 200, p = 500, independent N(0, 1) columns, centred and scaled;
# beta = +3 at {7, 250, 499}, -3 at {123, 401}; sigma = 1.
fixture_p500 <- function() {
  set.seed(TEST_SEED)
  n <- 200L; p <- 500L
  X <- scale(matrix(rnorm(n * p), n))
  attr(X, "scaled:center") <- NULL; attr(X, "scaled:scale") <- NULL
  b <- numeric(p); b[c(7, 250, 499)] <- 3; b[c(123, 401)] <- -3
  mu <- drop(X %*% b)
  e <- rnorm(n)
  list(X = X, mu = mu, e = e, y = mu + e, b = b, planted = c(7L, 123L, 250L, 401L, 499L),
       foldid = rep(1:10, length.out = n))
}

# Tests 1-2: kernel draws against the exact Gaussian N(m, Sigma), Sigma = (Phi'Phi + D^-1)^-1,
# m = Sigma Phi' alpha, with the calibrated acceptance of §III.3.8 i.1.
kernel_check <- function(draw_fun, Phi, alpha, d, M) {
  p <- ncol(Phi)
  Sigma <- solve(crossprod(Phi) + diag(1 / d, p))
  m <- drop(Sigma %*% crossprod(Phi, alpha))
  D <- matrix(0, p, M)
  for (i in seq_len(M)) D[, i] <- draw_fun()
  xbar <- rowMeans(D)
  Dc <- D - xbar
  S <- tcrossprod(Dc) / (M - 1)
  z <- (xbar - m) / sqrt(diag(Sigma) / M)
  rel_f <- norm(S - Sigma, "F") / norm(Sigma, "F")
  bound_f <- 4 * sqrt(((sum(diag(Sigma)))^2 / norm(Sigma, "F")^2 + 1) / (M - 1))
  list(pass = all(abs(z) <= 5) && rel_f <= bound_f,
       detail = sprintf("max|z| = %.3f (<= 5); relF = %.5f (<= %.5f)", max(abs(z)), rel_f, bound_f))
}

test_1_bhat <- function() {
  set.seed(TEST_SEED)
  n <- 20L; p <- 50L
  Phi <- matrix(rnorm(n * p), n); alpha <- rnorm(n); d <- runif(p, 0.5, 2)
  set.seed(TEST_SEED + 1L)
  kernel_check(function() as.vector(bayesreg:::bayesreg.fastmvg_bhat(Phi, alpha, d)$x),
               Phi, alpha, d, 200000L)
}

test_2_rue <- function() {
  set.seed(TEST_SEED)
  n <- 50L; p <- 20L
  Phi <- matrix(rnorm(n * p), n); alpha <- rnorm(n); d <- runif(p, 0.5, 2)
  PtP <- crossprod(Phi); Pta <- crossprod(Phi, alpha)
  set.seed(TEST_SEED + 1L)
  kernel_check(function() as.vector(bayesreg:::bayesreg.fastmvg2_rue.gaussian(Phi, alpha, d,
                 PtP = PtP, Ptalpha = Pta, sigma2 = 1, PrecomputedXtX = TRUE)$x),
               Phi, alpha, d, 200000L)
}

summ_mat <- function(fit, s) as.matrix(a3_summaries(fit, s)[, c("mean", "q025", "q50", "q975")])

# Shared fits of the p = 500 fixture (test budget), computed once.
shared_fits <- function(fx, s) {
  f <- list()
  f$y      <- a3_call(fx$X, fx$y, TEST_SEED, s)
  f$y_rep  <- a3_call(fx$X, fx$y, TEST_SEED, s)                     # test 7
  f$y_plus <- a3_call(fx$X, fx$y + 5, TEST_SEED, s)                 # test 3
  f$y_half <- a3_call(fx$X, 0.5 * fx$mu + fx$e, TEST_SEED, s)       # test 6
  f$X3     <- a3_call(3 * fx$X, fx$y, TEST_SEED, s)                 # test 4
  for (nm in names(f)) if (!is.null(f[[nm]]$error)) stop("fixture fit ", nm, " failed: ", f[[nm]]$error)
  f
}

test_3_shift <- function(f, s) {
  a <- summ_mat(f$y$fit, s); b <- summ_mat(f$y_plus$fit, s)
  d_sum <- max(abs(a - b))
  d_b0 <- abs((mean(f$y_plus$fit$beta0) - mean(f$y$fit$beta0)) - 5)
  d_draw <- max(abs(f$y$fit$beta - f$y_plus$fit$beta))
  list(pass = d_sum <= 1e-6 && d_b0 <= 1e-6,
       detail = sprintf("max|summary diff| = %.3g; |mean b0 shift - 5| = %.3g; max draw diff (recorded) = %.3g",
                        d_sum, d_b0, d_draw))
}

# Per entry (every coefficient's mean and three quantiles): |a - b| <= 1e-6 |a| + 1e-12, the
# absolute floor 1e-12 covering entries that are exactly or nearly 0.
test_4_scale <- function(f, s) {
  a <- summ_mat(f$y$fit, s) / 3; b <- summ_mat(f$X3$fit, s)
  ok <- abs(a - b) <= 1e-6 * abs(a) + 1e-12
  rel <- max(abs(a - b) / pmax(abs(a), 1e-12))
  d_draw <- max(abs(f$y$fit$beta / 3 - f$X3$fit$beta)) / max(abs(f$y$fit$beta / 3))
  list(pass = all(ok),
       detail = sprintf("entries within 1e-6 relative (+1e-12): %d of %d; max per-entry relative diff = %.3g; max abs diff = %.3g; max relative draw diff (recorded) = %.3g",
                        sum(ok), length(ok), rel, max(abs(a - b)), d_draw))
}

test_5_strong <- function(fx, f, s) {
  fit <- f$y$fit
  chk <- a3_fit_checks(fit, ncol(fx$X), s)
  coef <- a3_summaries(fit, s)
  r <- a3_rules(coef, TEST_SEED, s)
  mu <- rowMeans(fit$beta)[fx$planted]
  ok_mu <- all(sign(mu) == sign(fx$b[fx$planted])) && all(abs(mu - fx$b[fx$planted]) <= 0.5)
  w <- fit_A3_horseshoe(fx$X, fx$y, fx$foldid, TEST_SEED, s)
  w_ci95 <- w$rules$support[w$rules$rule_id == "ci95"]
  pass <- is.null(chk) && identical(r$ci95, fx$planted) && ok_mu &&
    identical(w_ci95, support_key(fx$planted))
  list(pass = pass, wrapper = w,
       detail = sprintf("checks=%s; ci95={%s}; wrapper ci95={%s}; means at planted = %s; km2 k=%s; rownames[c(1,2,p)] = %s",
                        if (is.null(chk)) "pass" else chk, support_key(r$ci95), w_ci95,
                        paste(sprintf("%.3f", mu), collapse = ","),
                        if (r$km2$failed) "failed" else length(r$km2$selected),
                        paste(rownames(fit$beta)[c(1, 2, nrow(fit$beta))], collapse = ",")))
}

test_6_crn <- function(f) {
  h <- c(y = f$y$rng_after, y_plus = f$y_plus$rng_after, y_half = f$y_half$rng_after)
  list(pass = length(unique(h)) == 1L,
       detail = sprintf("rng_after equal across y, y+5, 0.5*mu+e: %s (%s...)", length(unique(h)) == 1L,
                        substr(h[1], 1, 16)))
}

test_7_determinism <- function(f) {
  same <- identical(f$y$fit$beta, f$y_rep$fit$beta)
  list(pass = same, detail = sprintf("identical(fit$beta) for two runs with the same seed: %s", same))
}

test_8_interval <- function(f, s) {
  fit <- f$y$fit; p <- fit$p
  coef <- a3_summaries(fit, s)
  utils::capture.output(sm <- summary(fit))
  d <- max(abs(sm$CI.coef[1:p, 1] - coef$q025), abs(sm$CI.coef[1:p, 2] - coef$q975))
  list(pass = d <= 1e-12, detail = sprintf("max|wrapper CI - summary CI| = %.3g (<= 1e-12)", d))
}

test_9_rules <- function(s) {
  coef <- data.frame(mean = c(0.5, 0.1, 0.4, -0.4, -0.5),
                     q025 = c(1e-12, -1e-12, 0, -1, -2), q975 = c(1, 1, 1, 0, -1e-12))
  ci <- a3_rules(coef, TEST_SEED, s)$ci95
  ok_ci <- identical(ci, c(1L, 5L))
  absmu <- c(seq(0, 0.05, length.out = 20), c(1.9, 2.0, 2.1, 2.2, 2.3))
  km <- a3_kmeans2(absmu, TEST_SEED, s)
  ok_km <- !km$failed && identical(km$selected, 21:25)
  kc <- a3_kmeans2(rep(0.3, 10), TEST_SEED, s)
  ok_const <- kc$failed && is.null(kc$selected)
  # A rule-level km2 failure leaves ci95 intact in the rule frame.
  rows <- make_rule_rows(s, "A3", list(
    ci95 = list(status = "ok", support = c(5L, 1L), warnings = character(0), messages = character(0)),
    km2 = list(status = "failed", support = NULL, warnings = character(0), messages = character(0),
               error = kc$error)),
    converged = NA, diag_flag = FALSE, diag_codes = character(0),
    extra = list(rng_after = "x", diag_s = 0))
  ok_rows <- identical(rows$rule_id, c("ci95", "km2")) && identical(rows$role, c("primary", "S0")) &&
    identical(rows$status, c("ok", "failed")) && identical(rows$support[1], "1;5") &&
    is.na(rows$support[2]) && is.na(rows$k[2]) && identical(rows$k[1], 2L) && all(is.na(rows$converged))
  list(pass = ok_ci && ok_km && ok_const && ok_rows,
       detail = sprintf("ci95 endpoints {%s} (expect 1;5): %s; km2 two clusters: %s; km2 constant fails: %s; km2-only failure rows: %s",
                        support_key(ci), ok_ci, ok_km, ok_const, ok_rows))
}

test_10_orthogonal <- function() {
  s <- make_settings("primary")                                     # production settings (Rue at p = 30)
  set.seed(TEST_SEED)
  n <- 200L; p <- 30L
  Z <- scale(matrix(rnorm(n * p), n), center = TRUE, scale = FALSE)
  X <- qr.Q(qr(Z)) * sqrt(n - 1)                                     # X'X = (n - 1) I, centred, sd 1
  act <- c(3L, 7L, 14L, 16L, 25L)
  b <- numeric(p); b[act] <- c(1.4, -1.0, 1.8, -1.2, 0.8)
  y <- drop(X %*% b) + rnorm(n)
  orth <- max(abs(crossprod(X) - (n - 1) * diag(p)))
  w <- fit_A3_horseshoe(X, y, rep(1:10, length.out = n), TEST_SEED, s)
  ci <- w$rules$support[w$rules$rule_id == "ci95"]
  km <- w$rules$support[w$rules$rule_id == "km2"]
  list(pass = identical(ci, support_key(act)) && w$diagnostics$sampler == "rue",
       detail = sprintf("max|X'X - 199 I| = %.2g; sampler = %s; ci95 = {%s}; km2 (recorded) = {%s}; flag = %s",
                        orth, w$diagnostics$sampler, ci, km, w$rules$diag_flag[1]))
}

test_11_null <- function(fx, s) {
  p <- ncol(fx$X)
  w <- fit_A3_horseshoe(fx$X, fx$e, fx$foldid, TEST_SEED, s)
  k <- setNames(w$rules$k, w$rules$rule_id)
  review <- names(k)[!is.na(k) & k > 0.3 * p]
  list(pass = !is.na(k[["ci95"]]) && k[["ci95"]] <= 0.3 * p,
       detail = sprintf("null y: k(ci95) = %s, k(km2) = %s, status = %s; rules above 30%% of p flagged for review: %s",
                        k[["ci95"]], k[["km2"]], paste(w$rules$status, collapse = ","),
                        if (length(review)) paste(review, collapse = ",") else "none"))
}

test_12_failure <- function(fx, f, s) {
  p <- ncol(fx$X)
  is_failed <- function(r) all(r$rules$status == "failed") && all(is.na(r$rules$support)) &&
    all(is.na(r$rules$k)) && all(is.na(r$rules$converged)) && identical(r$rules$rule_id, c("ci95", "km2")) &&
    is.null(r$pip) && length(r$beta) == p && all(is.na(r$beta))
  # (a) package error inside the capture layer
  sa <- s; sa$A3$PRIOR <- "bogus"
  ra <- run_fit_safely(fit_A3_horseshoe, fx$X, fx$y, fx$foldid, TEST_SEED, sa, "A3")
  ok_a <- is_failed(ra) && all(grepl("Unknown prior", ra$rules$error))
  # (b) version assertion outside the capture layer -> runner's outer tryCatch
  sb <- s; sb$A3$PKG_VERSIONS[["bayesreg"]] <- "9.9"
  rb <- run_fit_safely(fit_A3_horseshoe, fx$X, fx$y, fx$foldid, TEST_SEED, sb, "A3")
  ok_b <- is_failed(rb) && all(grepl("^uncaught: assert_pkg_version", rb$rules$error))
  # (c) bad input (X not centred)
  rc <- run_fit_safely(fit_A3_horseshoe, fx$X + 1, fx$y, fx$foldid, TEST_SEED, s, "A3")
  ok_c <- is_failed(rc) && all(grepl("not centred", rc$rules$error))
  # (d) fit-level checks on doctored fits
  fit <- f$y$fit
  f1 <- fit; f1$n.cores <- 2
  f2 <- fit; f2$beta[1, 1] <- NaN
  f3 <- fit; f3$mu.beta[1] <- f3$mu.beta[1] + 1e-3
  f4 <- fit; f4$p <- p - 1L
  f5 <- fit; f5$tau2[3] <- 0
  msgs <- vapply(list(f1, f2, f3, f4, f5), function(z) { m <- a3_fit_checks(z, p, s); if (is.null(m)) "PASSED" else m }, "")
  ok_d <- is.null(a3_fit_checks(fit, p, s)) && !any(msgs == "PASSED")
  list(pass = ok_a && ok_b && ok_c && ok_d,
       detail = sprintf("package error: %s; version assertion: %s; bad input: %s; doctored fits rejected: %s (%s)",
                        ok_a, ok_b, ok_c, ok_d, paste(msgs, collapse = " / ")))
}

test_13_no_oracle <- function(code_dir) {
  files <- c(file.path(code_dir, c("config.R", "common.R")),
             list.files(file.path(code_dir, "methods"), pattern = "\\.R$", full.names = TRUE))
  pats <- c("truth", "\\$active", "\\$signal", "truth/")
  hits <- character(0)
  for (fl in files) {
    lines <- readLines(fl)
    for (pt in pats) {
      i <- grep(pt, lines)
      if (length(i)) hits <- c(hits, sprintf("%s:%d [%s]", basename(fl), i, pt))
    }
  }
  list(pass = length(hits) == 0L,
       detail = sprintf("%d files grepped for %s; hits: %s", length(files), paste(pats, collapse = " "),
                        if (length(hits)) paste(hits, collapse = ", ") else "none"))
}

# §IV.3 test 5 (runner part): A3 after an F5-like call (abess re-seeds from the clock on exit)
# must equal A3 alone, because the runner re-seeds before every method call.
test_14_runner_order <- function(fx, s, w5) {
  alone <- run_fit_safely(fit_A3_horseshoe, fx$X, fx$y, fx$foldid, TEST_SEED, s, "A3")
  invisible(abess::abess(fx$X, fx$y, support.size = 0:5))
  after <- run_fit_safely(fit_A3_horseshoe, fx$X, fx$y, fx$foldid, TEST_SEED, s, "A3")
  cols <- c("rule_id", "status", "support", "k", "diag_flag", "diag_codes", "rng_after")
  same <- identical(alone$rules[, cols], after$rules[, cols]) &&
    identical(alone$diagnostics$coef, after$diagnostics$coef) &&
    identical(alone$diagnostics$coef, w5$diagnostics$coef)
  list(pass = same, detail = sprintf("A3 alone == A3 after abess == direct wrapper call: %s", same))
}

# §III.3.9 (a unit test runs the wrapper with truth/ absent) and Sol review findings 1 and 3:
# the runner is run end to end on a copy of one dev input in a temporary tree that has inputs/
# and manifests/ but no truth/, with every R-level file-opening call traced; then the outputs
# are validated with check_run(), and the idempotence check is probed with damaged .sha256 files.
A3_TRACED_OPENERS <- c(readRDS = "file", load = "file", scan = "file", readLines = "con",
                       file = "description", gzfile = "description", readBin = "con")
a3_trace_openers <- function() {
  assign(".a3_opened", character(0), envir = globalenv())
  for (fn in names(A3_TRACED_OPENERS)) {
    arg <- as.name(A3_TRACED_OPENERS[[fn]])
    tr <- bquote(if (is.character(.(arg)))
      assign(".a3_opened", c(get(".a3_opened", envir = globalenv()), .(arg)), envir = globalenv()))
    suppressMessages(trace(fn, tracer = tr, print = FALSE, where = baseenv()))
  }
}
a3_untrace_openers <- function()
  for (fn in names(A3_TRACED_OPENERS)) suppressMessages(untrace(fn, where = baseenv()))

test_15_runner_truth_absent <- function(code_dir) {
  src_root <- "/projects/ml75/fb31/BVS/bench20261019/dev"
  ds <- "dev_p0500_S1_r001"
  tmp <- file.path(tempdir(), "a3_no_oracle_run")
  unlink(tmp, recursive = TRUE)
  dir.create(file.path(tmp, "inputs", "p0500"), recursive = TRUE); dir.create(file.path(tmp, "manifests"))
  inp <- file.path(tmp, "inputs", "p0500", paste0(ds, ".rds"))
  file.copy(file.path(src_root, "inputs", "p0500", paste0(ds, ".rds")), inp)
  man <- utils::read.csv(file.path(src_root, "manifests", "dev_inputs_manifest.csv"), stringsAsFactors = FALSE)
  man <- man[man$dataset_id == ds, ]
  manf <- file.path(tmp, "manifests", "dev_inputs_manifest.csv")
  utils::write.csv(man, manf, row.names = FALSE)
  out <- file.path(tmp, "out")

  CODE_DIR <<- code_dir
  a3_trace_openers()
  st <- tryCatch(main(c("--input", inp, "--manifest", manf, "--outroot", out, "--run-id", "unit_no_oracle")),
                 finally = a3_untrace_openers())
  opened <- unique(get(".a3_opened", envir = globalenv()))
  no_truth_dir <- !dir.exists(file.path(tmp, "truth"))
  truth_opened <- grep("(^|/)truth(/|$)", opened, value = TRUE)   # a truth/ path component
  input_opened <- any(grepl(ds, opened, fixed = TRUE))
  chk <- check_run(out, "unit_no_oracle", man, "c100")

  prefix <- file.path(out, "results", "unit_no_oracle", "p0500", paste0(ds, "_c100"), "A3")
  sha <- paste0(prefix, ".sha256"); keep <- readLines(sha)
  rr <- utils::read.csv(paste0(prefix, ".csv"), stringsAsFactors = FALSE)
  expect <- list(case_id = rr$case_id[1], source_sha256 = rr$source_sha256[1], x_sha256 = rr$x_sha256[1],
                 y_sha256 = rr$y_sha256[1], method_seed = rr$method_seed[1])
  v_ok <- done_is_valid(prefix, expect)
  v_other_code <- done_is_valid(prefix, modifyList(expect, list(source_sha256 = "other")))
  writeLines(character(0), sha); v_empty <- done_is_valid(prefix, expect)
  writeLines(keep[grepl("A3.csv$", keep)], sha); v_csv_only <- done_is_valid(prefix, expect)
  writeLines(keep, sha)
  list(pass = identical(st, 0L) && no_truth_dir && length(truth_opened) == 0L && input_opened &&
         length(chk$problems) == 0L && nrow(chk$table) == 2L && v_ok && !v_other_code && !v_empty && !v_csv_only,
       detail = sprintf("runner exit %s; truth/ absent from tree: %s; %d distinct paths opened (input among them: %s), with a truth/ component: %s; check_run problems: %d %s; done_is_valid valid/other-code/empty/csv-only = %s/%s/%s/%s",
                        st, no_truth_dir, length(opened), input_opened,
                        if (length(truth_opened)) paste(truth_opened, collapse = ",") else "none",
                        length(chk$problems), paste(chk$problems, collapse = "; "), v_ok, v_other_code, v_empty, v_csv_only))
}

# Sol review finding 1: a failed-fit record written by the runner's own functions must pass
# through check_run() (failed rows, NA diagnostics) without error.
test_16_failed_record_check <- function() {
  src_root <- "/projects/ml75/fb31/BVS/bench20261019/dev"
  ds <- "dev_p0500_S1_r001"
  inp <- file.path(src_root, "inputs", "p0500", paste0(ds, ".rds"))
  d <- readRDS(inp)
  man <- utils::read.csv(file.path(src_root, "manifests", "dev_inputs_manifest.csv"), stringsAsFactors = FALSE)
  man <- man[man$dataset_id == ds, ]
  s <- make_settings("primary"); s$A3$PRIOR <- "bogus"
  y <- unname(d$Y[, "c100"])
  res <- run_fit_safely(fit_A3_horseshoe, d$X, y, d$foldid, as.integer(d$method_seed), s, "A3")
  design <- list(study = s$COMMON$STUDY, run_id = "unit_failed", source_sha256 = "test", regime = "H",
    p = ncol(d$X), scenario = as.integer(d$scenario), replicate = as.integer(d$replicate),
    scale_key = "c100", scale = 1, dataset_id = ds, case_id = paste0(ds, "_c100"),
    data_seed = as.integer(d$data_seed), fold_seed = as.integer(d$fold_seed), method_seed = as.integer(d$method_seed),
    inputs_sha256 = file_sha256(inp), x_sha256 = f64_sha256(d$X), y_sha256 = f64_sha256(y),
    fold_sha256 = f64_sha256(d$foldid), method_id = "A3", method_label = "Horseshoe (bayesreg)",
    package = "bayesreg", package_version = "1.3", runtime_s = res$runtime_s, host = "test",
    slurm_job_id = NA, slurm_array_task_id = NA, started_utc = "t0", finished_utc = "t1")
  rows <- assemble_rows(res$rules, design, s)
  out <- file.path(tempdir(), "a3_failed_record")
  unlink(out, recursive = TRUE)
  prefix <- file.path(out, "results", "unit_failed", "p0500", paste0(ds, "_c100"), "A3")
  dir.create(dirname(prefix), recursive = TRUE)
  write_case_files(prefix, rows, list(rows = rows, diagnostics = res$diagnostics), "t1")
  chk <- tryCatch(check_run(out, "unit_failed", man, "c100"), error = function(e) e)
  ok <- !inherits(chk, "error") && length(chk$problems) == 0L && nrow(chk$table) == 2L &&
    all(chk$table$status == "failed") && all(is.na(chk$table$ess_log_tau2))
  list(pass = ok,
       detail = if (inherits(chk, "error")) paste("check_run error:", conditionMessage(chk)) else
         sprintf("failed-fit record: check_run rows %d, statuses %s, problems %d %s", nrow(chk$table),
                 paste(chk$table$status, collapse = ","), length(chk$problems), paste(chk$problems, collapse = "; ")))
}

# Sol review finding 2: crn_mismatch is method-wide. Dataset D: scale c100 fit (ci95 ok, km2
# failed at rule level, rng "a"), scale c050 fit (rng "b"), scale c025 failed fit (rng NA);
# dataset E: two fits with equal rng. Expected: all four rows of the two non-failed D fits
# flagged; the failed D fit and all E rows untouched.
test_17_crn_method_wide <- function() {
  rows <- data.frame(dataset_id = c(rep("D", 6), rep("E", 4)),
                     scale_key = c("c100", "c100", "c050", "c050", "c025", "c025", "c100", "c100", "c050", "c050"),
                     rule_id = rep(c("ci95", "km2"), 5),
                     status = c("ok", "failed", "ok", "ok", "failed", "failed", rep("ok", 4)),
                     rng_after = c("a", "a", "b", "b", NA, NA, "e", "e", "e", "e"),
                     diag_flag = c(FALSE, FALSE, TRUE, TRUE, NA, NA, rep(FALSE, 4)),
                     diag_codes = c("", "", "ess_tau", "ess_tau", "", "", rep("", 4)), stringsAsFactors = FALSE)
  r <- flag_crn(rows)
  want <- c(rep(TRUE, 4), FALSE, FALSE, rep(FALSE, 4))
  ok <- identical(r$crn_mismatch, want) && all(r$diag_flag[1:4]) && all(is.na(r$diag_flag[5:6])) &&
    !any(r$diag_flag[7:10]) &&
    identical(r$diag_codes[1:4], c("crn_mismatch", "crn_mismatch", "ess_tau;crn_mismatch", "ess_tau;crn_mismatch"))
  list(pass = ok, detail = sprintf("crn_mismatch = %s; diag_codes of D = %s", paste(r$crn_mismatch, collapse = ","),
                                   paste(r$diag_codes[1:6], collapse = "|")))
}

run_A3_tests <- function(code_dir = A3_TEST_CODE_DIR, out_dir = NULL) {
  a3_test_setup(code_dir)
  s <- test_budget_settings()
  results <- list()
  run <- function(name, expr) {
    t0 <- proc.time()[["elapsed"]]
    r <- tryCatch(expr, error = function(e) list(pass = FALSE, detail = paste("ERROR:", conditionMessage(e))))
    results[[name]] <<- data.frame(test = name, pass = isTRUE(r$pass), seconds = round(elapsed(t0), 1),
                                   detail = r$detail, stringsAsFactors = FALSE)
    cat(sprintf("[%s] %s (%.1f s): %s\n", if (isTRUE(r$pass)) "PASS" else "FAIL", name, elapsed(t0), r$detail))
    r
  }
  run("i1_bhattacharya_kernel", test_1_bhat())
  run("i2_rue_kernel", test_2_rue())
  fx <- fixture_p500()
  t0 <- proc.time()[["elapsed"]]
  f <- tryCatch(shared_fits(fx, s), error = function(e) e)
  cat(sprintf("shared p = 500 fixture fits (5 x test budget): %.1f s\n", elapsed(t0)))
  if (inherits(f, "error")) {
    run("shared_fixture_fits", list(pass = FALSE, detail = conditionMessage(f)))
  } else {
    run("i3_shift_canary", test_3_shift(f, s))
    run("i4_scale_canary", test_4_scale(f, s))
    r5 <- run("i5_strong_signal_p500", test_5_strong(fx, f, s))
    run("i6_crn_invariant", test_6_crn(f))
    run("i7_determinism", test_7_determinism(f))
    run("i8_interval_vs_summary", test_8_interval(f, s))
    run("iv3_6_failure_path", test_12_failure(fx, f, s))
    if (!is.null(r5$wrapper)) run("iv3_5_runner_order_determinism", test_14_runner_order(fx, s, r5$wrapper))
  }
  run("i9_rules", test_9_rules(s))
  run("i10_orthogonal_canary_p30", test_10_orthogonal())
  run("iv3_2_null_canary", test_11_null(fx, s))
  run("iv3_7_no_oracle_grep", test_13_no_oracle(code_dir))
  run("iv3_7b_runner_truth_absent", test_15_runner_truth_absent(code_dir))
  run("sol1_failed_record_check", test_16_failed_record_check())
  run("sol2_crn_flag_method_wide", test_17_crn_method_wide())
  tab <- do.call(rbind, results); rownames(tab) <- NULL
  cat(sprintf("\n%d of %d tests passed\n", sum(tab$pass), nrow(tab)))
  if (!is.null(out_dir)) {
    dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
    utils::write.csv(tab, file.path(out_dir, "test_results.csv"), row.names = FALSE)
    saveRDS(list(results = tab, session = utils::capture.output(utils::sessionInfo()),
                 detect_cores = parallel::detectCores(), host = Sys.info()[["nodename"]]),
            file.path(out_dir, "test_results.rds"))
  }
  invisible(tab)
}

if (sys.nframe() == 0L) {
  args <- commandArgs(trailingOnly = TRUE)
  tab <- run_A3_tests(A3_TEST_CODE_DIR, if (length(args)) args[1] else NULL)
  quit(save = "no", status = if (all(tab$pass)) 0L else 1L)
}
