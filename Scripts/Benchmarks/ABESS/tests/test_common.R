#!/usr/bin/env Rscript
# test_common.R: G3 fixtures for the common.R helpers used by F5 (master §III.3.0 EBIC/BIC,
# §III.3.1 k: null RSS = sum(y^2), a hand-computed two-variable score, rank deficiency -> Inf,
# singleton support, tie order), plus the rule frame, failure rows, capture layer and
# input assertions. Fixtures ported from Oct-14 scripts/validate.R.
# Usage: Rscript --vanilla tests/test_common.R <code_root> <out_dir>

args <- commandArgs(trailingOnly = TRUE)
code_root <- normalizePath(args[1], mustWork = TRUE); out_dir <- args[2]
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
source(file.path(code_root, "run_case.R"))            # loaders only; main() is guarded
settings <- load_settings(code_root); use_study_library(settings)
E <- load_engine(code_root)

results <- list()
check <- function(name, expr) {
  a <- tryCatch(force(expr), error = function(e) e); ok <- !inherits(a, "error") && !identical(a, FALSE)
  results[[name]] <<- list(passed = ok, detail = if (inherits(a, "error")) conditionMessage(a) else a)
  cat(if (ok) "PASS" else "FAIL", name, if (inherits(a, "error")) paste("--", conditionMessage(a)) else "", "\n")
}
rejects <- function(expr) inherits(tryCatch(force(expr), error = function(e) e), "error")
near <- function(a, b, tol = 1e-12) isTRUE(all(abs(a - b) <= tol * pmax(1, abs(a), abs(b))))

X <- cbind(c(-2, -1, 0, 1, 2), c(1, -2, 2, -2, 1)); y <- c(1, 3, -2, 4, 7); n <- 5
G <- c(ebic1 = 1, ebic05 = 0.5, bic = 0)

check("ols_rss: null support gives sum(y^2) and rank 0", {
  r <- E$ols_rss(X, y, integer(), 1e-10); stopifnot(r$rss == sum(y^2), r$rank == 0L); TRUE })
check("ols_rss: singleton support (drop = FALSE)", {
  r <- E$ols_rss(X, y, 2L, 1e-10)
  b <- sum(X[, 2] * y) / sum(X[, 2]^2); stopifnot(near(r$rss, sum((y - X[, 2] * b)^2)), r$rank == 1L); TRUE })
check("ebic_candidates: hand-computed two-variable EBIC/BIC scores", {
  beta <- solve(crossprod(X), crossprod(X, y)); rss <- sum((y - X %*% beta)^2)
  c2 <- E$ebic_candidates(X, y, list(1:2), kmax = 2L, gammas = G, tol = 1e-10)
  r <- c2[c2$key == "1;2", ]
  # p = 2, k = 2: log C(2, 2) = 0, so all three gammas give n log(rss/n) + 2 log n.
  stopifnot(near(r$rss, rss), near(r$bic, n * log(rss / n) + 2 * log(n)),
            near(r$ebic1, r$bic), near(r$ebic05, r$bic))
  r0 <- c2[c2$key == "", ]; stopifnot(near(r0$ebic1, n * log(sum(y^2) / n))); TRUE })
check("ebic_candidates: gamma term 2 gamma log C(p, k) at p = 3", {
  X3 <- cbind(X, c(0.5, -1, 0.3, 2, -1.8)); c3 <- E$ebic_candidates(X3, y, list(1L), 3L, G, 1e-10)
  r <- c3[c3$key == "1", ]; stopifnot(near(r$ebic1 - r$bic, 2 * log(3)), near(r$ebic05 - r$bic, log(3))); TRUE })
check("ebic_candidates: rank-deficient support scores Inf and is invalid", {
  Xd <- cbind(X[, 1], X[, 1]); c4 <- E$ebic_candidates(Xd, y, list(1:2), 2L, G, 1e-10)
  r <- c4[c4$key == "1;2", ]; stopifnot(!r$valid, is.infinite(r$ebic1), is.infinite(r$bic)); TRUE })
check("ebic_candidates: null included, duplicates removed, cap applied", {
  c5 <- E$ebic_candidates(X, y, list(1L, 1L, integer(), 1:2), kmax = 1L, gammas = G, tol = 1e-10)
  stopifnot(identical(c5$key, c("", "1"))); TRUE })
check("ebic_pick: ties broken by smaller k, then key in C byte order (radix)", {
  cand <- data.frame(key = c("1;23", "12;3", "4"), k = c(2L, 2L, 1L), rank = c(2L, 2L, 1L),
                     rss = 1, valid = TRUE, ebic1 = c(5, 5, 5), stringsAsFactors = FALSE)
  stopifnot(E$ebic_pick(cand, "ebic1")$key == "4")
  cand$ebic1[3] <- 6
  pk <- E$ebic_pick(cand, "ebic1")
  # C order: "12;3" < "1;23" because "2" (0x32) < ";" (0x3B).
  stopifnot(pk$key == "12;3", pk$k_valid_max == 2L, identical(pk$codes, "ebic_at_largest")); TRUE })
check("ebic_pick: no valid candidate is an error, never a null-model success", {
  cand <- data.frame(key = c("", "1"), k = 0:1, rank = 0:1, rss = 1, valid = FALSE,
                     ebic1 = Inf, stringsAsFactors = FALSE)
  rejects(E$ebic_pick(cand, "ebic1")) })
check("support_key / parse_key round trip", {
  stopifnot(E$support_key(c(10L, 2L, 7L)) == "2;7;10", E$support_key(integer()) == "",
            identical(E$parse_key("2;7;10"), c(2L, 7L, 10L)), identical(E$parse_key(""), integer()),
            is.na(E$parse_key(NA_character_))); TRUE })
check("with_captured_conditions: warnings, messages and errors captured verbatim", {
  a <- E$with_captured_conditions({ warning("w1"); message("m1"); 42 })
  b <- E$with_captured_conditions(stop("boom"))
  stopifnot(a$value == 42, identical(a$warnings, "w1"), identical(a$messages, "m1\n"), is.na(a$error),
            is.null(b$value), b$error == "boom"); TRUE })
check("make_rule_rows / fail_rows: registered ids, roles and columns", {
  st <- settings
  f <- E$fail_rows(st, "F5", converged = NA, diag_flag = FALSE,
                   support_audit = list(ebic1 = "1;2", ebic05 = "1;2;3", bic = ""))
  stopifnot(identical(f$rule_id, c("ebic1", "ebic05", "bic")), identical(f$role, c("primary", "S0", "S0")),
            all(f$status == "failed"), all(is.na(f$support)), all(is.na(f$k)),
            identical(f$support_audit, c("1;2", "1;2;3", "")),
            identical(names(f), c("rule_id", "role", "status", "support", "support_audit", "k",
                                  "converged", "diag_flag", "diag_codes", "rss", "crit_value",
                                  "k_valid_max", "k_path_max")))
  rejects(E$make_rule_rows(st, "F5", list(ebic1 = list()), NA, FALSE, "ok")) })
check("assert_inputs: accepts a valid design, rejects violations", {
  set.seed(1); Z <- scale(matrix(rnorm(200 * 4), 200)); attr(Z, "scaled:center") <- NULL; attr(Z, "scaled:scale") <- NULL
  fo <- rep(1:10, 20); yy <- rnorm(200); C <- settings$COMMON
  stopifnot(isTRUE(E$assert_inputs(Z, yy, fo, C)))
  Zs <- scale(matrix(rnorm(200 * 4), 200))                         # keeps scaled:* attributes
  stopifnot(rejects(E$assert_inputs(Zs, yy, fo, C)), rejects(E$assert_inputs(Z + 1, yy, fo, C)),
            rejects(E$assert_inputs(Z * 2, yy, fo, C)), rejects(E$assert_inputs(Z, yy, fo[-1], C)),
            rejects(E$assert_inputs(Z, yy, replace(fo, 1:20, 11L), C)),
            rejects(E$assert_inputs(Z, replace(yy, 3, NA), fo, C)),
            rejects(E$assert_inputs(Z, yy, fo + 0.5, C)))      # fractional labels (Sol finding 6)
  TRUE })
check("assert_pkg_version: exact match only", {
  stopifnot(isTRUE(E$assert_pkg_version("abess", "0.4.11")), rejects(E$assert_pkg_version("abess", "0.4.1"))); TRUE })

passed <- all(vapply(results, `[[`, FALSE, "passed"))
saveRDS(list(passed = passed, results = results, host = Sys.info()[["nodename"]],
             job = Sys.getenv("SLURM_JOB_ID"), time = format(Sys.time(), tz = "UTC", usetz = TRUE)),
        file.path(out_dir, "test_common.rds"))
cat(sprintf("test_common: %d/%d passed\n", sum(vapply(results, `[[`, FALSE, "passed")), length(results)))
if (!passed) quit(save = "no", status = 1L)
