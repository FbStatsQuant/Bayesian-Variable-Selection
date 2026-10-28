#!/usr/bin/env Rscript
# test_common.R -- G3 fixtures for the common.R helpers F1 uses (master §III.3.1 k "test_common.R":
# null RSS = Σy², a hand-computed two-variable score, rank deficiency -> Inf, singleton support,
# tie order), plus support keys, condition capture and the rule-frame builders.
# Usage: Rscript --vanilla tests/test_common.R <code_dir> <out_dir>

if (nzchar(Sys.getenv("BENCH_LIB"))) .libPaths(c(Sys.getenv("BENCH_LIB"), .Library))
args <- commandArgs(trailingOnly = TRUE); code_dir <- args[[1]]; out_dir <- args[[2]]
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
cfg <- new.env(parent = baseenv()); sys.source(file.path(code_dir, "config.R"), envir = cfg)
settings <- as.list(cfg)
e <- new.env(parent = asNamespace("stats")); sys.source(file.path(code_dir, "common.R"), envir = e)

checks <- list()
record <- function(name, expr) {
  a <- tryCatch(force(expr), error = function(err) err); ok <- !inherits(a, "error")
  checks[[name]] <<- list(passed = ok, detail = if (ok) a else conditionMessage(a))
  cat(if (ok) "PASS" else "FAIL", name, if (!ok) paste("--", conditionMessage(a)), "\n")
}
rejects <- function(expr) inherits(tryCatch(force(expr), error = function(err) err), "error")
near <- function(a, b, tol = 1e-12) stopifnot(all(abs(a - b) <= tol * pmax(1, abs(a), abs(b))))

# Oct-14 validate.R fixture: X 5 x 2, y; independent normal-equation solution
X <- cbind(c(-2, -1, 0, 1, 2), c(1, -2, 2, -2, 1)); y <- c(1, 3, -2, 4, 7); n <- 5; p <- 2

record("ols_rss: null support gives RSS = sum(y^2), rank 0", {
  r <- e$ols_rss(X, y, integer(), 1e-10)
  stopifnot(identical(r$rss, sum(y^2)), identical(r$rank, 0L)); TRUE
})
record("ols_rss: singleton support (drop = FALSE) matches closed form", {
  r <- e$ols_rss(X, y, 2L, 1e-10)
  b <- sum(X[, 2] * y) / sum(X[, 2]^2)
  near(r$rss, sum((y - X[, 2] * b)^2)); stopifnot(r$rank == 1L); r$rss
})
record("EBIC: hand-computed two-variable scores (gamma 1, 0.5, 0)", {
  beta <- solve(crossprod(X), crossprod(X, y)); rss <- sum((y - X %*% beta)^2)
  cand <- e$ebic_candidates(X, y, list(1:2), 100, c(ebic1 = 1, ebic05 = 0.5, bic = 0), 1e-10)
  i <- match("1;2", cand$key)
  near(cand$rss[i], rss)
  near(cand$ebic05[i], 5 * log(rss / 5) + 2 * log(5) + 2 * 0.5 * lchoose(2, 2))   # lchoose(2,2) = 0
  near(cand$bic[i], 5 * log(rss / 5) + 2 * log(5))
  # a case with lchoose > 0: p = 10, k = 2 -> 2*gamma*log(45)
  X10 <- cbind(X, matrix(0, 5, 8))
  cand10 <- e$ebic_candidates(X10, y, list(1:2), 100, c(ebic1 = 1, ebic05 = 0.5, bic = 0), 1e-10)
  i10 <- cand10$key == "1;2"
  near(cand10$ebic1[i10],  5 * log(rss / 5) + 2 * log(5) + 2 * 1.0 * log(45))
  near(cand10$ebic05[i10], 5 * log(rss / 5) + 2 * log(5) + 2 * 0.5 * log(45))
  near(cand10$bic[i10],    5 * log(rss / 5) + 2 * log(5))
  # null candidate: n log(sum(y^2)/n), no size or combinatorial term
  near(cand10$ebic05[cand10$key == ""], 5 * log(sum(y^2) / 5))
  c(rss = rss, ebic05 = cand$ebic05[i])
})
record("EBIC: rank-deficient support scores Inf; null is eligible", {
  Xd <- cbind(X[, 1], X[, 1])
  cand <- e$ebic_candidates(Xd, y, list(1:2), 100, c(ebic1 = 1), 1e-10)
  stopifnot(is.infinite(cand$ebic1[cand$key == "1;2"]), !cand$valid[cand$key == "1;2"],
            cand$key[1] == "", cand$valid[1], is.finite(cand$ebic1[1]))
  pk <- e$ebic_pick(cand, "ebic1"); stopifnot(pk$key == ""); TRUE
})
record("EBIC: dedup and cap k <= kmax", {
  cand <- e$ebic_candidates(X, y, list(2L, c(2L), 1:2, c(2L, 1L)), 1, c(ebic1 = 1), 1e-10)
  stopifnot(identical(cand$key, c("", "2"))); TRUE
})
record("EBIC tie order: criterion, then smaller k, then key in C-locale byte order", {
  cand <- data.frame(key = c("2;10", "10;20", "3", "1;5", "1;10", ""), k = c(2, 2, 1, 2, 2, 0),
                     valid = TRUE, s = c(5, 5, 5, 5, 5, 6), stringsAsFactors = FALSE)
  stopifnot(e$ebic_pick(cand, "s")$key == "3")
  cand2 <- cand[cand$k == 2, ]
  # C-locale byte order: "10;20" < "1;10" < "1;5" < "2;10" (digits 0x30-0x39 sort before ';' 0x3B)
  ord <- cand2$key[order(cand2$s, cand2$k, cand2$key, method = "radix")]
  stopifnot(identical(ord, c("10;20", "1;10", "1;5", "2;10")), e$ebic_pick(cand2, "s")$key == "10;20")
  stopifnot(e$ebic_pick(cand, "s")$k_valid_max == 2)
  ord
})
record("support_key / parse_key round trip and rejection", {
  stopifnot(identical(e$support_key(integer()), ""), identical(e$support_key(c(10L, 2L)), "2;10"),
            identical(e$parse_key(""), integer()), identical(e$parse_key("2;10"), c(2L, 10L)))
  stopifnot(all(vapply(c("1;1", "0", "2;1", "1;", "-1", "a"), function(k) rejects(e$parse_key(k)), TRUE)))
  TRUE
})
record("occurrence_ok", {
  stopifnot(e$occurrence_ok("1;2", c("", "1", "1;2", "1;2"), c(TRUE, TRUE, FALSE, TRUE)),
            !e$occurrence_ok("1;2", c("", "1", "1;2"), c(TRUE, TRUE, FALSE))); TRUE
})
record("with_captured_conditions: warnings, messages, error", {
  a <- e$with_captured_conditions({ warning("w1"); message("m1"); warning("w2"); 7 })
  stopifnot(identical(a$value, 7), identical(a$warnings, c("w1", "w2")), identical(a$messages, "m1\n"),
            is.na(a$error))
  b <- e$with_captured_conditions({ warning("w0"); stop("boom") })
  stopifnot(is.null(b$value), identical(b$error, "boom"), identical(b$warnings, "w0")); TRUE
})
record("make_rule_rows and fail_rows follow the registry", {
  M <- settings$METHODS; C <- settings$COMMON
  v <- list(cv_min = list(status = "ok", support = "3;7", codes = "lambda_last", extras = list(lambda = 0.1, index = 200L)),
            cv_1se = list(status = "failed", support = "3", codes = character(), extras = list()),
            ebic1 = list(status = "ok", support = "", codes = "ebic_at_largest", extras = list(crit_value = 1)),
            ebic05 = list(status = "ok", support = "3", codes = NULL, extras = list()))
  r <- e$make_rule_rows(M, "F1", v[c(3, 1, 2, 4)], TRUE, "kkt_path", C)
  stopifnot(identical(r$rule_id, M$rule_ids[[1]]), identical(r$role, M$roles[[1]]),
            identical(r$k, c(2L, NA, 0L, 1L)), identical(r$support, c("3;7", NA, "", "3")),
            identical(r$support_audit, c(NA, "3", NA, NA)), all(r$diag_flag),
            identical(r$diag_codes, c("kkt_path;lambda_last", "kkt_path", "kkt_path;ebic_at_largest", "kkt_path")),
            identical(names(r), c("rule_id", "role", "status", "support", "support_audit", "k", "converged",
                                  "diag_flag", "diag_codes", M$extra_cols[[1]])))
  stopifnot(rejects(e$make_rule_rows(M, "F1", v[1:3], TRUE, character(), C)))
  stopifnot(rejects(e$format_codes("not_a_code", C)))
  f <- e$fail_rows(M, "F1")
  stopifnot(all(f$status == "failed"), all(is.na(f$support)), all(is.na(f$k)), identical(f$converged, rep(FALSE, 4)),
            identical(names(f), names(r)))
  TRUE
})
record("assert_inputs accepts a valid design and rejects bad ones", {
  set.seed(1); Z <- scale(matrix(rnorm(200 * 5), 200)); attributes(Z)[c("scaled:center", "scaled:scale")] <- NULL
  f <- rep(1:10, 20); yy <- rnorm(200); C <- settings$COMMON
  stopifnot(isTRUE(e$assert_inputs(Z, yy, f, C)))
  Zs <- scale(Z)
  stopifnot(rejects(e$assert_inputs(Zs, yy, f, C)), rejects(e$assert_inputs(Z + 1, yy, f, C)),
            rejects(e$assert_inputs(Z * 2, yy, f, C)), rejects(e$assert_inputs(Z, yy[-1], f, C)),
            rejects(e$assert_inputs(Z, yy, replace(f, 1:20, 11L), C)),
            rejects(e$assert_inputs(Z, replace(yy, 3, NA), f, C)),
            rejects(e$assert_inputs(Z, yy, c(rep(1:9, length.out = 198), 10L, 10L), C)))
  TRUE
})

passed <- all(vapply(checks, `[[`, FALSE, "passed"))
saveRDS(list(passed = passed, checks = checks, host = Sys.info()[["nodename"]], time = Sys.time()),
        file.path(out_dir, "test_common.rds"))
cat(sprintf("test_common: %d of %d passed\n", sum(vapply(checks, `[[`, FALSE, "passed")), length(checks)))
if (!passed) quit(status = 1L)
