#!/usr/bin/env Rscript
# test_F5_abess.R: G3 unit tests for F5 (master §III.3.5 i and the §IV.3 unit-test list):
#  1 orthogonal canary; 2 null canary; 3 no-intercept canary (a, b, c); 4 F5 consistency
#  checks on one dev case per p, deliberate-corruption tests, known-bug canary;
#  5 determinism and runner reseeding; 6 failure path; 7 no-oracle (grep; run with truth/
#  absent); plus a schema check of the runner's files. Pilot items (runtime, rates) are not here.
# Usage: Rscript --vanilla tests/test_F5_abess.R <code_root> <out_dir> <dev_root>

args <- commandArgs(trailingOnly = TRUE)
code_root <- normalizePath(args[1], mustWork = TRUE); out_dir <- args[2]; dev_root <- args[3]
prod_root <- if (length(args) >= 4) args[4] else NA_character_   # production data root (task-map test)
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
source(file.path(code_root, "run_case.R"))            # loaders only; main() is guarded
source(file.path(code_root, "validate_outputs.R"))
source(file.path(code_root, "run_task.R"))           # task map and run_chunk(); main() is guarded
settings <- load_settings(code_root); use_study_library(settings)
E <- load_engine(code_root)
TS <- settings$TEST_SEED

results <- list(); info <- new.env()   # info: an environment, filled by reference
check <- function(name, expr) {
  t0 <- proc.time()[["elapsed"]]
  a <- tryCatch(force(expr), error = function(e) e); ok <- !inherits(a, "error") && !identical(a, FALSE)
  results[[name]] <<- list(passed = ok, detail = if (inherits(a, "error")) conditionMessage(a) else a,
                           seconds = proc.time()[["elapsed"]] - t0)
  cat(if (ok) "PASS" else "FAIL", name, if (inherits(a, "error")) paste("--", conditionMessage(a)) else "", "\n")
  flush.console()
}
rejects <- function(expr) inherits(tryCatch(force(expr), error = function(e) e), "error")
fit5 <- function(X, y, st = settings, seed = 1L) E$fit_F5_abess(X, y, rep(1:10, length.out = nrow(X)), seed, st)
std_design <- function(n, p, seed) {                  # centred, sd 1 (n - 1), no attributes
  set.seed(seed); Z <- scale(matrix(rnorm(n * p), n))
  attr(Z, "scaled:center") <- NULL; attr(Z, "scaled:scale") <- NULL; Z
}
abess_raw <- function(X, yc, S, screening.num = NULL)   # the wrapper's call, for corruption tests
  abess::abess(X, yc, family = "gaussian", tune.path = "sequence", tune.type = "bic", normalize = 0,
               fit.intercept = FALSE, support.size = S, lambda = 0, screening.num = screening.num,
               important.search = ncol(X), warm.start = TRUE, early.stop = FALSE, c.max = 2L,
               max.splicing.iter = 100L, splicing.type = 2L, num.threads = 1L, seed = 1L)
n <- 200L

# ---- 1. orthogonal canary (n = 200, p = 30, X'X = (n - 1) I, sizes 0..29) ----
check("1 orthogonal canary: ABESS support of size k = k largest |X_j'y|, all k; 5 recovered", {
  set.seed(TS); Z <- scale(matrix(rnorm(n * 30), n), scale = FALSE)
  X <- qr.Q(qr(Z)) * sqrt(n - 1)                      # centred, orthogonal, sd 1
  stopifnot(max(abs(crossprod(X) - (n - 1) * diag(30))) < 1e-9)
  act <- c(3L, 7L, 14L, 16L, 25L); b <- numeric(30); b[act] <- c(1.4, -1.0, 1.8, -1.2, 0.8)
  y <- drop(X %*% b) + rnorm(n)
  st <- settings; st$F5$sizes <- 0:29
  f <- fit5(X, y, st)
  stopifnot(all(f$rules$status == "ok"))
  ord <- order(abs(crossprod(X, y)), decreasing = TRUE)
  want <- vapply(0:29, function(k) E$support_key(ord[seq_len(k)]), "")
  stopifnot(identical(f$diagnostics$path$key, want))
  stopifnot(f$rules$support[f$rules$rule_id == "ebic1"] == E$support_key(act))
  info$orthogonal <- f$rules[c("rule_id", "support", "k")]
  TRUE })

# ---- 2. null canary (beta = 0), production sizes 0..100 at p = 500 ----
# EBIC(1) adds k log n + 2 log C(p, k), about 17.7 per variable for small k at n = 200,
# p = 500, while the best single noise variable lowers n log RSS by about 2 log p = 12.4
# (max of p chi-square(1)), so the primary rule should return the null model or almost
# so. The bound k <= 2 is the "small support" assertion (Sol finding 3). The 30%-of-p review
# rule of §IV.3 is also applied; it cannot fire for F5 (sizes <= 100), so BIC's size is
# reported, not asserted.
check("2 null canary: primary ebic1 support k <= 2; no rule above 30% of p", {
  X <- std_design(n, 500L, TS + 1L); set.seed(TS + 2L); y <- rnorm(n)
  f <- fit5(X, y); stopifnot(all(f$rules$status == "ok"))
  info$null <- f$rules[c("rule_id", "k", "diag_codes")]
  cat("   null canary sizes:", paste(f$rules$rule_id, f$rules$k, collapse = ", "), "\n")
  stopifnot(f$rules$k[f$rules$rule_id == "ebic1"] <= 2L, all(f$rules$k <= 0.3 * 500))
  f$rules$k })

# ---- 3. no-intercept canary (y with mean 3, X centred), p = 500 ----
local({
  X <- std_design(n, 500L, TS + 3L); set.seed(TS + 4L)
  b <- numeric(500); b[c(3, 37, 74, 106, 145)] <- c(1.4, -1.0, 1.8, -1.2, 0.8)
  y0 <- drop(X %*% b) + rnorm(n); y <- y0 - mean(y0) + 3; yc <- y - mean(y)
  f1 <- fit5(X, y); f2 <- fit5(X, yc)
  check("3a no-intercept: supports and slopes identical on y and y - mean(y)", {
    stopifnot(all(f1$rules$status == "ok"), all(f2$rules$status == "ok"),
              identical(f1$diagnostics$path$key, f2$diagnostics$path$key))
    d <- max(abs(unlist(f1$diagnostics$coefficients) - unlist(f2$diagnostics$coefficients)))
    stopifnot(d <= 1e-8); d })
  check("3b no-intercept: RSS(y) = RSS(y - mean(y)) + n ybar^2 for every path support", {
    sup <- lapply(f1$diagnostics$path$key, E$parse_key)
    r1 <- vapply(sup, function(s) E$ols_rss(X, y, s, 1e-10)$rss, 0)
    r2 <- vapply(sup, function(s) E$ols_rss(X, yc, s, 1e-10)$rss, 0)
    dev <- max(abs(r1 - (r2 + n * mean(y)^2)) / r1); stopifnot(dev <= 1e-10); dev })
  check("3c no-intercept: EBIC choices on y and y - mean(y) reported (not a failure)", {
    info$no_intercept_choices <- data.frame(rule_id = f1$rules$rule_id, k_y = f1$rules$k,
      k_yc = f2$rules$k, same_support = f1$rules$support == f2$rules$support)
    print(info$no_intercept_choices); TRUE })
})

# ---- 4. F5 consistency checks on one dev case per p; corruption tests; known-bug canary ----
for (pp in c(500L, 1000L)) local({
  inp <- file.path(dev_root, "inputs", sprintf("p%04d", pp), sprintf("dev_p%04d_S4_r001.rds", pp))
  check(sprintf("4 consistency checks pass on dev case p = %d (S4 r001, c100)", pp), {
    d <- readRDS(inp); f <- E$fit_F5_abess(d$X, unname(d$Y[, "c100"]), d$foldid, d$method_seed, settings)
    pa <- f$diagnostics$path
    stopifnot(all(f$rules$status %in% c("ok", "warning")), !length(f$diagnostics$consistency_failures),
              nrow(pa) == 101L, identical(pa$k, 0:100))
    v <- c(max_rel_rss_ols = max(abs(pa$rss_reconstructed - pa$rss_ols) / pa$rss_ols),
           max_rel_rss_dev = max(abs(pa$rss_reconstructed - (2 * n * pa$dev + n * f$diagnostics$response_center^2)) / pa$rss_reconstructed),
           max_stationarity = max(pa$stationarity), stat_tol = f$diagnostics$stat_tol,
           max_abs_intercept = max(abs(pa$intercept)))
    print(signif(v, 3)); v })
})
local({
  X <- std_design(n, 500L, TS + 5L); set.seed(TS + 6L)
  b <- numeric(500); b[c(3, 37, 74)] <- c(1.4, -1.0, 1.8); y <- drop(X %*% b) + rnorm(n) + 2
  yc <- y - mean(y); S <- 0:20; F5s <- settings$F5; F5s$sizes <- S
  fit <- abess_raw(X, yc, S)
  chk <- function(ff) E$abess_consistency(ff, X, y, yc, F5s, 1e-10)$failures
  check("4 corruption: the uncorrupted fit passes every consistency check", {
    stopifnot(!length(chk(fit))); TRUE })
  B <- as.matrix(fit$beta)
  # Each corruption must trigger the intended check(s), matched by their failure text
  # (Sol finding 4), not merely some failure.
  corrupt <- list(
    "support.size relabelled" = list(function(ff) { ff$support.size[3] <- 0L; ff },
                                     "support.size != requested sizes"),
    "coefficient zeroed (k-1 elements in column k)" = list(function(ff) { bb <- B; j <- which(bb[, 6] != 0)[1]; bb[j, 6] <- 0; ff$beta <- bb; ff },
                                     "support of column k does not have k elements"),
    "coefficient perturbed (RSS/OLS and stationarity)" = list(function(ff) { bb <- B; j <- which(bb[, 6] != 0)[1]; bb[j, 6] <- bb[j, 6] + 1e-3; ff$beta <- bb; ff },
                                     c("reconstructed RSS != OLS RSS", "active-set stationarity")),
    "package dev + 1"         = list(function(ff) { ff$dev[2] <- ff$dev[2] + 1; ff }, "2n dev"),
    "nonzero intercept 1e-6"  = list(function(ff) { ff$intercept[4] <- 1e-6; ff }, "intercept not zero"),
    "non-finite coefficient"  = list(function(ff) { bb <- B; bb[1, 2] <- NA; ff$beta <- bb; ff }, "non-finite coefficients"),
    "missing path column"     = list(function(ff) { ff$beta <- B[, -21, drop = FALSE]; ff }, "dim(beta)"))
  for (nm in names(corrupt)) check(paste("4 corruption detected:", nm), {
    fails <- chk(corrupt[[nm]][[1]](fit))
    for (pat in corrupt[[nm]][[2]]) if (!any(grepl(pat, fails, fixed = TRUE)))
      stop("expected failure '", pat, "' not reported; got: ", paste(fails, collapse = "; "))
    fails })
  check("4 stationarity gate is enforced on its own (tolerance forced negative)", {
    F5n <- F5s; F5n$stat_rel_tol <- -1
    fails <- E$abess_consistency(fit, X, y, yc, F5n, 1e-10)$failures
    stopifnot(identical(fails, "active-set stationarity above tolerance")); fails })
  check("4 RSS gates are enforced on their own (tolerance forced negative)", {
    F5n <- F5s; F5n$rss_rel_tol <- -1
    fails <- E$abess_consistency(fit, X, y, yc, F5n, 1e-10)$failures
    stopifnot(identical(fails, c("reconstructed RSS != OLS RSS of the support",
                                 "reconstructed RSS != 2n dev + n ybar^2"))); fails })
  check("4 known-bug canary: screening.num = ncol(X) returns an all-zero coefficient path", {
    fb <- abess_raw(X, yc, S, screening.num = ncol(X))
    stopifnot(all(as.matrix(fb$beta) == 0)); TRUE })
})

# ---- 5. determinism and runner reseeding ----
local({
  inp <- file.path(dev_root, "inputs", "p0500", "dev_p0500_S5_r001.rds"); d <- readRDS(inp)
  y <- unname(d$Y[, "c100"])
  check("5 determinism: two calls give identical supports, coefficients and paths", {
    a <- E$fit_F5_abess(d$X, y, d$foldid, d$method_seed, settings)
    b <- E$fit_F5_abess(d$X, y, d$foldid, d$method_seed, settings)
    # Both fits must be successful and populated before comparing (Sol finding 5).
    stopifnot(all(a$rules$status == "ok"), all(b$rules$status == "ok"), nrow(a$diagnostics$path) == 101L,
              length(a$diagnostics$coefficients) == 101L, all(is.finite(a$beta)), any(a$beta != 0))
    stopifnot(identical(a$rules, b$rules), identical(a$beta, b$beta),
              identical(a$diagnostics$path, b$diagnostics$path),
              identical(a$diagnostics$coefficients, b$diagnostics$coefficients)); TRUE })
  check("5 runner reseeding: a method run after F5 sees the same RNG stream as when run alone", {
    E$fit_PROBE <- function(X, y, foldid, seed, settings) list(draws = runif(5))
    probe <- data.frame(method_id = "PROBE", fn = "fit_PROBE", variant = "primary", converged_na = TRUE)
    m5 <- settings$METHODS[1, , drop = FALSE]
    r5 <- run_method(E, settings, m5, d$X, y, d$foldid, d$method_seed)
    after <- run_method(E, settings, probe, d$X, y, d$foldid, d$method_seed)$draws
    alone <- run_method(E, settings, probe, d$X, y, d$foldid, d$method_seed)$draws
    rm("fit_PROBE", envir = E)
    stopifnot(all(r5$rules$status == "ok"), length(after) == 5L, all(is.finite(after)),
              length(alone) == 5L, all(is.finite(alone)), identical(after, alone)); TRUE })
})

# ---- 6. failure path: forced errors give status = failed rows, never null-model successes ----
local({
  inp <- file.path(dev_root, "inputs", "p0500", "dev_p0500_S1_r001.rds"); d <- readRDS(inp)
  y <- unname(d$Y[, "c100"]); m5 <- settings$METHODS[1, , drop = FALSE]
  is_failed <- function(r, audit) {
    stopifnot(identical(r$rules$rule_id, c("ebic1", "ebic05", "bic")), all(r$rules$status == "failed"),
              all(is.na(r$rules$support)), all(is.na(r$rules$k)), all(is.na(r$beta)), !is.na(r$error),
              all(is.na(r$rules$converged)))
    if (audit) stopifnot(all(!is.na(r$rules$support_audit))) else stopifnot(all(is.na(r$rules$support_audit)))
    TRUE }
  check("6 failure: invalid input (NaN in X) -> runner fail_rows", {
    Xb <- d$X; Xb[1, 1] <- NaN; is_failed(run_method(E, settings, m5, Xb, y, d$foldid, d$method_seed), FALSE) })
  check("6 failure: package error inside the capture (bad tune.path) -> failed rows", {
    st <- settings; st$F5$tune_path <- "not_a_path"
    r <- run_method(E, st, m5, d$X, y, d$foldid, d$method_seed); print(r$error); is_failed(r, FALSE) })
  check("6 failure: consistency gate failure -> failed rows, supports kept in support_audit", {
    st <- settings; st$F5$rss_rel_tol <- -1
    r <- run_method(E, st, m5, d$X, y, d$foldid, d$method_seed); is_failed(r, TRUE) })
  check("6 failure: screening_num not NULL is refused (0.4.11 bug guard)", {
    st <- settings; st$F5$screening_num <- 500L
    is_failed(run_method(E, st, m5, d$X, y, d$foldid, d$method_seed), FALSE) })
  check("6 failure: pinned version mismatch -> failed rows", {
    st <- settings; st$F5$pkg_version <- "0.4.10"
    is_failed(run_method(E, st, m5, d$X, y, d$foldid, d$method_seed), FALSE) })
})

# ---- 7. no-oracle: grep of the fitting sources; runner and wrapper with truth/ absent ----
check("7 no-oracle grep: config.R, common.R, methods/*.R contain no truth identifiers", {
  files <- c(file.path(code_root, c("config.R", "common.R")),
             list.files(file.path(code_root, "methods"), pattern = "\\.R$", full.names = TRUE))
  hits <- unlist(lapply(files, function(f) { l <- readLines(f)
    i <- grep("truth|\\$active|\\$signal|truth/", l); if (length(i)) paste0(basename(f), ":", i) }))
  if (length(hits)) stop("hits: ", paste(hits, collapse = ", ")); TRUE })
check("7 no-oracle run: runner + wrapper on a data root with no truth/, files validate", {
  tmp <- file.path(tempdir(), "noorc"); unlink(tmp, recursive = TRUE)
  dir.create(file.path(tmp, "data", "inputs", "p0500"), recursive = TRUE)
  dir.create(file.path(tmp, "data", "manifests"))
  src <- file.path(dev_root, "inputs", "p0500", "dev_p0500_S2_r001.rds")
  file.copy(src, file.path(tmp, "data", "inputs", "p0500"))
  file.copy(file.path(dev_root, "manifests", "dev_inputs_manifest.csv"), file.path(tmp, "data", "manifests"))
  stopifnot(!dir.exists(file.path(tmp, "data", "truth")))
  s <- run_case(file.path(tmp, "data", "inputs", "p0500", "dev_p0500_S2_r001.rds"),
                file.path(tmp, "data", "manifests", "dev_inputs_manifest.csv"),
                file.path(tmp, "out"), "unit_test", "c100", NULL, code_root)
  v <- validate_tree(code_root, file.path(tmp, "out", "results", "unit_test"),
                     file.path(tmp, "data", "manifests", "dev_inputs_manifest.csv"), "dev_p0500_S2_r001_c100",
                     file.path(tmp, "data", "inputs"))
  print(v$table); s2 <- run_case(file.path(tmp, "data", "inputs", "p0500", "dev_p0500_S2_r001.rds"),
                file.path(tmp, "data", "manifests", "dev_inputs_manifest.csv"),
                file.path(tmp, "out"), "unit_test", "c100", NULL, code_root)
  stopifnot(v$passed, grepl("skipped", s2))           # idempotent rerun skips a valid .done
  c(s, s2) })

# ---- saved-output corruption (Oct-14 validate.R pattern; Sol findings 1 and 2) ----
local({
  tmp <- file.path(tempdir(), "noorc")
  man_path <- file.path(tmp, "data", "manifests", "dev_inputs_manifest.csv")
  prefix <- file.path(tmp, "out", "results", "unit_test", "p0500", "dev_p0500_S2_r001_c100", "F5")
  man <- utils::read.csv(man_path, stringsAsFactors = FALSE, colClasses = "character")
  r0 <- read_rule_csv(paste0(prefix, ".csv")); o0 <- readRDS(paste0(prefix, ".rds"))
  inp <- load_case_inputs(file.path(tmp, "data", "inputs"), r0, man)
  vo <- function(r, o) validate_objects(r, o, "F5", settings, man, inp)
  check("saved output: the uncorrupted objects validate", {
    e <- vo(r0, o0); if (length(e)) stop(paste(e, collapse = "; ")); TRUE })
  alt <- o0$diagnostics$path$key[o0$diagnostics$path$k == r0$k[1] + 1L]   # another path support
  bad <- list(
    "row support '1;1'"            = function(r, o) { r$support[1] <- "1;1"; list(r, o) },
    "a rule row removed"           = function(r, o) { list(r[-1, ], o) },
    "x_sha256 changed"             = function(r, o) { r$x_sha256 <- strrep("0", 64); list(r, o) },
    "a code-file hash changed"     = function(r, o) { o$source_hashes$files$sha256[1] <- strrep("0", 64); list(r, o) },
    "path k[2] set to 0"           = function(r, o) { o$diagnostics$path$k[2] <- 0L; list(r, o) },
    "coefficients[[2]] set to 0"   = function(r, o) { o$diagnostics$coefficients[[2]] <- 0; list(r, o) },
    "package dev[2] + 1"           = function(r, o) { o$diagnostics$path$dev[2] <- o$diagnostics$path$dev[2] + 1; list(r, o) },
    "stationarity above tolerance" = function(r, o) { o$diagnostics$path$stationarity[5] <- 1; list(r, o) },
    "ebic1 support swapped (CSV and RDS)" = function(r, o) {
      r$support[1] <- alt; r$k[1] <- r$k[1] + 1L; o$rows$support[1] <- alt; o$rows$k[1] <- r$k[1]; list(r, o) },
    "candidate score changed"      = function(r, o) {
      o$diagnostics$candidates$ebic05[3] <- o$diagnostics$candidates$ebic05[3] - 1; list(r, o) },
    "beta changed"                 = function(r, o) { j <- which(o$beta != 0)[1]; o$beta[j] <- o$beta[j] * 2; list(r, o) },
    # Sol round 2: missing columns, a nonselected path coefficient, a candidate rank.
    "path column dev deleted"      = function(r, o) { o$diagnostics$path$dev <- NULL; list(r, o) },
    "path column stationarity deleted" = function(r, o) { o$diagnostics$path$stationarity <- NULL; list(r, o) },
    "path column intercept deleted" = function(r, o) { o$diagnostics$path$intercept <- NULL; list(r, o) },
    "nonselected coefficient perturbed" = function(r, o) {
      j <- which(o$diagnostics$path$k == 50L); o$diagnostics$coefficients[[j]][1] <- o$diagnostics$coefficients[[j]][1] + 1e-3; list(r, o) },
    "candidate rank changed"       = function(r, o) { o$diagnostics$candidates$rank[4] <- o$diagnostics$candidates$rank[4] - 1L; list(r, o) },
    "candidate valid flag flipped" = function(r, o) { o$diagnostics$candidates$valid[4] <- FALSE; list(r, o) })
  for (nm in names(bad)) check(paste("saved-output corruption rejected:", nm), {
    z <- bad[[nm]](r0, o0)
    e <- tryCatch(vo(z[[1]], z[[2]]), error = function(err) paste("error:", conditionMessage(err)))
    stopifnot(length(e) > 0); e })
  check("sidecar: empty, partial or duplicated .sha256 never certifies a fit", {
    d2 <- file.path(tmp, "sidecar"); unlink(d2, recursive = TRUE); dir.create(d2)
    for (ext in c(".rds", ".csv", ".sha256", ".done")) file.copy(paste0(prefix, ext), d2)
    p2 <- file.path(d2, "F5"); stopifnot(done_is_valid(p2))
    good <- readLines(paste0(p2, ".sha256"))
    writeLines(character(), paste0(p2, ".sha256"))
    stopifnot(!done_is_valid(p2), length(sidecar_errors(p2)) > 0)
    writeLines(c(good, good[1]), paste0(p2, ".sha256")); stopifnot(!done_is_valid(p2))
    writeLines(good[grepl("csv$", good)], paste0(p2, ".sha256")); unlink(paste0(p2, ".rds"))
    stopifnot(!done_is_valid(p2), length(validate_one(p2, settings, man)) > 0)
    TRUE })
})

# ---- production orchestration (Astra production-readiness findings 1-8) ----
check("prod: task map covers 1,200 distinct datasets exactly once; smoke task 91 holds p1000_S4_r001", {
  ids <- unlist(lapply(1:120, function(t) task_datasets(t)$dataset_id))
  stopifnot(length(ids) == 1200L, !anyDuplicated(ids), setequal(paste0(ids, "_c100"), prod_case_ids()),
            "p1000_S4_r001" %in% task_datasets(91L)$dataset_id,
            identical(task_datasets(1L)$dataset_id[c(1, 10)], c("p0500_S1_r001", "p0500_S1_r010")),
            identical(task_datasets(120L)$dataset_id[10], "p1000_S6_r100"))
  if (!is.na(prod_root)) {              # every production input and cell manifest exists
    items <- do.call(rbind, lapply(1:120, function(t) task_items(t, prod_root, file.path(prod_root, "manifests", "cells"))))
    stopifnot(all(file.exists(items$input)), all(file.exists(unique(items$manifest))), length(unique(items$manifest)) == 12L)
  }
  TRUE })
check("prod: rank-deficient path supports allowed only if excluded from selection", {
  cand <- data.frame(key = c("", "1", "1;2"), k = 0:2, rank = c(0L, 1L, 1L), rss = c(10, 5, 5),
                     valid = c(TRUE, TRUE, FALSE), ebic1 = c(1, 0.5, Inf), ebic05 = c(1, 0.4, Inf), bic = c(1, 0.3, Inf))
  stopifnot(!length(rank_errors(c(0L, 1L, 1L), cand)))                      # deficient and excluded: fine
  bad <- cand; bad$valid[3] <- TRUE; bad$ebic1[3] <- 0.1
  stopifnot(length(rank_errors(c(0L, 1L, 1L), bad)) == 2L)                  # deficient but selectable
  stopifnot(length(rank_errors(c(0L, 1L, 2L), cand)) == 1L)                 # saved rank wrong
  TRUE })
local({
  tmp <- file.path(tempdir(), "noorc")
  res <- file.path(tmp, "out", "results", "unit_test"); man <- file.path(tmp, "data", "manifests", "dev_inputs_manifest.csv")
  inp <- file.path(tmp, "data", "inputs"); exp <- "dev_p0500_S2_r001_c100"
  check("prod: validation fails when the inputs root is unavailable", {
    v <- validate_tree(code_root, res, man, exp, file.path(tmp, "no_such_inputs"))
    stopifnot(!v$passed, grepl("inputs root unavailable", v$note)); v$note })
  check("prod: validation fails on an extra case directory and on a missing expected case", {
    stopifnot(!validate_tree(code_root, res, man, character(), inp)$passed)       # found case not expected
    stopifnot(!validate_tree(code_root, res, man, c(exp, "dev_p0500_S3_r001_c100"), inp)$passed)
    TRUE })
  check("prod: output from another code version is rejected (validator) and never skipped (runner)", {
    d2 <- file.path(tmp, "stale", "results", "unit_test", "p0500", exp); dir.create(d2, recursive = TRUE)
    prefix <- file.path(res, "p0500", exp, "F5")
    for (ext in c(".rds", ".csv", ".sha256", ".done")) file.copy(paste0(prefix, ext), d2)
    p2 <- file.path(d2, "F5"); r <- read_rule_csv(paste0(p2, ".csv")); r$source_sha256 <- strrep("a", 64)
    utils::write.csv(r, paste0(p2, ".csv"), row.names = FALSE, na = "NA")
    fs <- paste0(p2, c(".rds", ".csv"))
    writeLines(paste(vapply(fs, file_sha256, ""), basename(fs), sep = "  "), paste0(p2, ".sha256"))
    stopifnot(done_is_valid(p2))                                                 # sidecar is consistent
    e <- validate_one(p2, settings, utils::read.csv(man, colClasses = "character"), inp,
                      list(tree = code_hashes(code_root)$tree, settings = settings))
    stopifnot(any(grepl("trusted snapshot", e)))
    rr <- tryCatch(run_case(file.path(inp, "p0500", "dev_p0500_S2_r001.rds"), man, file.path(tmp, "stale"),
                            "unit_test", "c100", NULL, code_root), error = function(err) conditionMessage(err))
    stopifnot(grepl("different code version", rr)); e })
})
check("prod: a chunk continues past a fatal dataset, records status files, and a rerun completes only what is missing", {
  tmp <- file.path(tempdir(), "chunk"); unlink(tmp, recursive = TRUE)
  di <- file.path(tmp, "data", "inputs", "p0500"); dm <- file.path(tmp, "data", "manifests"); dir.create(di, recursive = TRUE); dir.create(dm)
  ids <- sprintf("dev_p0500_S%d_r001", c(1, 3, 6))
  for (id in ids) file.copy(file.path(dev_root, "inputs", "p0500", paste0(id, ".rds")), di)
  good <- utils::read.csv(file.path(dev_root, "manifests", "dev_inputs_manifest.csv"), colClasses = "character")
  badm <- good; badm$x_sha256[badm$dataset_id == ids[2]] <- strrep("0", 64)          # middle dataset fails its hash check
  utils::write.csv(good, file.path(dm, "good.csv"), row.names = FALSE); utils::write.csv(badm, file.path(dm, "bad.csv"), row.names = FALSE)
  items <- data.frame(dataset_id = ids, input = file.path(di, paste0(ids, ".rds")),
                      manifest = file.path(dm, c("good.csv", "bad.csv", "good.csv")), stringsAsFactors = FALSE)
  st <- file.path(tmp, "status")
  f1 <- run_chunk(items, file.path(tmp, "out"), "chunk_test", code_root, st)
  done <- file.exists(file.path(tmp, "out", "results", "chunk_test", "p0500", paste0(ids, "_c100"), "F5.done"))
  stopifnot(f1 == 1L, identical(done, c(TRUE, FALSE, TRUE)),
            all(file.exists(file.path(st, paste0(ids, "_c100.started")))),
            identical(file.exists(file.path(st, paste0(ids, "_c100.fatal"))), c(FALSE, TRUE, FALSE)))
  m1 <- file.mtime(file.path(tmp, "out", "results", "chunk_test", "p0500", paste0(ids[1], "_c100"), "F5.rds"))
  # Interrupted commit of case 3: rds and csv present, no sidecar and no .done -> redone on rerun.
  c3 <- file.path(tmp, "out", "results", "chunk_test", "p0500", paste0(ids[3], "_c100"))
  unlink(file.path(c3, c("F5.sha256", "F5.done")))
  items$manifest[2] <- file.path(dm, "good.csv")
  f2 <- run_chunk(items, file.path(tmp, "out"), "chunk_test", code_root, st)
  stopifnot(f2 == 0L, all(file.exists(file.path(tmp, "out", "results", "chunk_test", "p0500", paste0(ids, "_c100"), "F5.done"))),
            identical(m1, file.mtime(file.path(tmp, "out", "results", "chunk_test", "p0500", paste0(ids[1], "_c100"), "F5.rds"))))
  v <- validate_tree(code_root, file.path(tmp, "out", "results", "chunk_test"), file.path(dm, "good.csv"),
                     paste0(ids, "_c100"), file.path(tmp, "data", "inputs"))
  stopifnot(v$passed); c(f1, f2) })

passed <- all(vapply(results, `[[`, FALSE, "passed"))
saveRDS(list(passed = passed, results = results, info = as.list(info), host = Sys.info()[["nodename"]],
             job = Sys.getenv("SLURM_JOB_ID"), time = format(Sys.time(), tz = "UTC", usetz = TRUE),
             session = utils::capture.output(utils::sessionInfo())),
        file.path(out_dir, "test_F5_abess.rds"))
cat(sprintf("test_F5_abess: %d/%d passed\n", sum(vapply(results, `[[`, FALSE, "passed")), length(results)))
if (!passed) quit(save = "no", status = 1L)
