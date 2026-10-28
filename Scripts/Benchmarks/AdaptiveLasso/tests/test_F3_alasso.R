#!/usr/bin/env Rscript
# test_F3_alasso.R: G3 unit tests for F3 (master §III.3.3 i and the §IV.3 unit-test list),
# plus the common.R EBIC fixtures F3 relies on (§III.3.1 k, test_common.R list).
# Pilot (G6) items of §III.3.3 i are not run here.
#
# Usage (compute node): Rscript tests/test_F3_alasso.R [--dev-root <dev dir>] [--tmp <dir>]
# Exit status 0 when every hard test passes. REVIEW lines are soft (G3 item 2).

args <- commandArgs(trailingOnly = TRUE)
get_arg <- function(k, default = NULL) { i <- match(k, args); if (is.na(i)) default else args[i + 1L] }
f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE))
CODE_ROOT <- dirname(dirname(normalizePath(f)))
DEV_ROOT <- get_arg("--dev-root", "/projects/ml75/fb31/BVS/bench20261019/dev")
TMP_ROOT <- get_arg("--tmp", tempdir())

rc <- new.env(); sys.source(file.path(CODE_ROOT, "run_case.R"), envir = rc)
code <- rc$load_code(CODE_ROOT)
cfg <- code$cfg; E <- code$engine
.libPaths(c(cfg$STUDY_LIB, .Library))
rc$check_library(cfg$STUDY_LIB, c("glmnet", "digest"))
S <- cfg$study_settings("primary")
METH <- S$METHODS[S$METHODS$method_id == "F3", , drop = FALSE]
cat("glmnet", as.character(packageVersion("glmnet")), "from", find.package("glmnet"), "\n")
cat("threads", Sys.getenv(c("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")), "\n")

RESULTS <- list()
check <- function(name, ok, detail = "") {
  ok <- isTRUE(ok)
  RESULTS[[length(RESULTS) + 1L]] <<- data.frame(test = name, pass = ok, detail = detail)
  cat(sprintf("[%s] %s %s\n", if (ok) "PASS" else "FAIL", name, detail))
}
review <- function(name, detail) cat(sprintf("[REVIEW] %s %s\n", name, detail))
safely <- function(name, expr) tryCatch(expr, error = function(e) check(name, FALSE, paste("ERROR:", conditionMessage(e))))

# Synthetic design: n x p, centred, sd 1 (n - 1); y = X beta + N(0, 1).
make_design <- function(n, p, active, beta_active, seed) {
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(seed)
  X <- scale(matrix(rnorm(n * p), n))
  attr(X, "scaled:center") <- NULL; attr(X, "scaled:scale") <- NULL
  beta <- numeric(p); beta[active] <- beta_active
  y <- drop(X %*% beta) + rnorm(n)
  foldid <- sample(rep(1:10, length.out = n))
  list(X = X, y = y, foldid = foldid, active = active)
}
# Orthogonal design: X'X = (n - 1) I, columns centred (G3 item 1).
make_orthogonal <- function(n, p, active, beta_active, seed) {
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(seed)
  M <- scale(matrix(rnorm(n * p), n), center = TRUE, scale = FALSE)
  X <- sqrt(n - 1) * qr.Q(qr(M))
  beta <- numeric(p); beta[active] <- beta_active
  y <- drop(X %*% beta) + rnorm(n)
  foldid <- sample(rep(1:10, length.out = n))
  list(X = X, y = y, foldid = foldid, active = active)
}
soft <- function(z, t) sign(z) * pmax(abs(z) - t, 0)
kappa_test <- c(1e-2, 1, 1e2)

# ---- 1. common.R EBIC fixtures ----
safely("common_ebic", {
  d <- make_design(40L, 6L, c(1L, 2L), c(2, -1), S$TEST_SEED)
  X <- d$X; y <- d$y; n <- 40; p <- 6
  cand <- E$ebic_candidates(X, y, list(c(2L, 1L), 3L, c(1L, 2L)), 100L, c(ebic1 = 1, ebic05 = 0.5), 1e-10)
  check("ebic_null_rss", abs(cand$rss[cand$key == ""] - sum(y^2)) < 1e-12 * sum(y^2))
  check("ebic_dedup", identical(cand$key, c("", "1;2", "3")))
  r2 <- sum(lm.fit(X[, 1:2], y)$residuals^2)
  hand <- n * log(r2 / n) + 2 * log(n) + 2 * 1 * lchoose(p, 2)
  check("ebic_two_variable", abs(cand$ebic1[cand$key == "1;2"] - hand) < 1e-10)
  r1 <- sum(lm.fit(X[, 3, drop = FALSE], y)$residuals^2)
  check("ebic_singleton", abs(cand$rss[cand$key == "3"] - r1) < 1e-12 * r1)
  Xd <- cbind(X, X[, 1])                         # column 7 duplicates column 1
  cd <- E$ebic_candidates(Xd, y, list(c(1L, 7L)), 100L, c(ebic1 = 1), 1e-10)
  check("ebic_rank_deficient_inf", is.infinite(cd$ebic1[cd$key == "1;7"]) && !cd$valid[cd$key == "1;7"])
  tie <- data.frame(key = c("2;10", "1;23", "12;3", "", "4"), k = c(2L, 2L, 2L, 0L, 1L),
                    crit = c(5, 5, 5, 7, 5), stringsAsFactors = FALSE)
  check("ebic_tie_order_smaller_k", E$ebic_pick(tie, "crit") == 5L)
  tie <- tie[1:4, ]
  check("ebic_tie_order_c_locale", E$ebic_pick(tie, "crit") == 3L,
        "(criterion, then k, then C-locale key: '12;3' < '1;23' < '2;10')")
  check("support_key", identical(E$support_key(c(10L, 2L, 37L)), "2;10;37") &&
          identical(E$support_key(integer()), "") && identical(E$parse_key(""), integer()))
  check("occurrence_ok_null", E$occurrence_ok("", c("1", "1;2"), c(FALSE, FALSE)))
})

# ---- 2. ridge closed form (§III.3.3 i) ----
D500 <- make_design(200L, 500L, c(3L, 37L, 74L, 106L, 145L), c(1.4, -1, 1.8, -1.2, 0.8), S$TEST_SEED + 1L)
safely("ridge_closed_form", {
  X <- D500$X; y <- D500$y; n <- nrow(X); p <- ncol(X)
  B <- E$ridge_path_svd(X, y, kappa_test)
  XtX <- crossprod(X) / n; Xty <- crossprod(X, y) / n
  err <- vapply(seq_along(kappa_test), function(j)
    max(abs(B[, j] - solve(XtX + kappa_test[j] * diag(p), Xty))), 0)
  check("ridge_vs_solve", max(err) <= 1e-8, sprintf("max abs diff %.2e", max(err)))
  # Reference route only: glmnet's stopping rule (per-pass change < thresh) leaves an error of
  # about 3e-6 at kappa = 1e-2 with thresh = 1e-16 (diagnostic 2275655: 2.8e-6 -> 2.2e-10 as
  # thresh goes 1e-16 -> 1e-24, while the SVD gradient is 1.5e-15), so the reference uses 1e-24.
  Gref <- S$GLMNET; Gref$thresh <- 1e-24
  errg <- vapply(seq_along(kappa_test), function(j) {
    g <- E$glmnet_target_path(X, y, alpha = 0, lam = kappa_test[j], pf = rep(1, p), G = Gref)
    max(abs(g$B[, 1] - B[, j]))
  }, 0)
  check("ridge_vs_glmnet_alpha0_map", max(errg) <= 1e-6, sprintf("max abs diff %.2e", max(errg)))
  res <- E$ridge_normal_residual(X, y, E$ridge_path_svd(X, y, S$F3$kappa), S$F3$kappa)
  check("ridge_normal_equations_full_grid", max(res) <= S$F3$ridge_tol, sprintf("max rel residual %.2e", max(res)))
})

# ---- 3. ridge CV against a naive per-fold solve ----
safely("ridge_cv_naive", {
  X <- D500$X; y <- D500$y; fo <- D500$foldid; n <- nrow(X); p <- ncol(X)
  rcv <- E$ridge_cv(X, y, fo, S$F3$kappa)
  jj <- c(1L, 20L, 31L, 45L)                        # kappa = 1e3, ~1, ~1e-1/2, ~1e-3
  oof <- matrix(NA_real_, n, length(jj))
  for (k in 1:10) {
    te <- fo == k; Xt <- X[!te, ]; nt <- sum(!te)
    for (a in seq_along(jj)) {
      b <- solve(crossprod(Xt) / nt + S$F3$kappa[jj[a]] * diag(p), crossprod(Xt, y[!te]) / nt)
      oof[te, a] <- X[te, ] %*% b
    }
  }
  mse <- t(sapply(1:10, function(k) colMeans((y[fo == k] - oof[fo == k, , drop = FALSE])^2)))
  cvm <- colSums(mse * tabulate(fo, 10)) / n
  err <- max(abs(cvm - rcv$cvm[jj]) / rcv$cvm[jj])
  check("ridge_cv_vs_naive", err <= 1e-8, sprintf("max rel diff in cvm %.2e", err))
  check("ridge_cv_tie_larger", rcv$i_min == min(which(rcv$cvm <= min(rcv$cvm))))
})

# ---- 4. penalty-factor invariance (§III.3.3 i) ----
safely("pf_invariance", {
  X <- D500$X; y <- D500$y; p <- ncol(X)
  rcv <- E$ridge_cv(X, y, D500$foldid, S$F3$kappa)
  wt <- E$alasso_weights(rcv$B[, rcv$i_min], S$F3)
  check("pf_sum_is_p", abs(sum(wt$v) - p) < 1e-9 * p)
  lam <- S$GRID$max_mult * max(abs(drop(crossprod(X, y))) / nrow(X) / wt$v) * E$lambda_fraction(S$GRID)
  G <- S$GLMNET
  fit1 <- glmnet::glmnet(X, y, alpha = 1, lambda = lam, penalty.factor = wt$v, intercept = FALSE,
                         standardize = FALSE, type.gaussian = "naive",
                         control = list(thresh = G$thresh, maxit = G$maxit, fdev = 0, devmax = 1))
  fit7 <- glmnet::glmnet(X, y, alpha = 1, lambda = lam, penalty.factor = 7 * wt$v, intercept = FALSE,
                         standardize = FALSE, type.gaussian = "naive",
                         control = list(thresh = G$thresh, maxit = G$maxit, fdev = 0, devmax = 1))
  err <- max(abs(as.matrix(fit1$beta) - as.matrix(fit7$beta)))
  check("pf_7v_equals_v", err <= 1e-10, sprintf("max abs diff %.2e", err))
})

# ---- 5. orthogonal canary (§III.3.3 i; G3 item 1) ----
safely("orthogonal_canary", {
  O <- make_orthogonal(200L, 30L, c(3L, 7L, 14L, 16L, 25L), c(1.4, -1, 1.8, -1.2, 0.8), S$TEST_SEED + 2L)
  X <- O$X; y <- O$y; n <- 200; p <- 30; s2 <- (n - 1) / n
  check("orth_design", max(abs(crossprod(X) - (n - 1) * diag(p))) < 1e-9 && max(abs(colMeans(X))) < 1e-12)
  rcv <- E$ridge_cv(X, y, O$foldid, S$F3$kappa)
  z <- drop(crossprod(X, y)) / n
  bclosed <- outer(z, S$F3$kappa, function(zz, kk) zz / (s2 + kk))
  check("orth_ridge_closed_form", max(abs(rcv$B - bclosed)) < 1e-10)
  wt <- E$alasso_weights(rcv$B[, rcv$i_min], S$F3)
  lam <- S$GRID$max_mult * max(abs(z) / wt$v) * E$lambda_fraction(S$GRID)
  path <- E$glmnet_target_path(X, y, 1, lam, wt$v, S$GLMNET)
  closed <- sapply(lam, function(l) soft(z, l * wt$v) / s2)
  err <- max(abs(path$B - closed))
  check("orth_weighted_soft_threshold", err <= 1e-8 * max(1, max(abs(z))), sprintf("max abs diff %.2e", err))
  check("grid_first_point_null_orth", all(path$B[, 1] == 0))
  fit <- E$fit_F3_alasso(X, y, O$foldid, 1L, S)
  sel <- fit$rules$support[fit$rules$rule_id == "cv_min"]
  all_rules <- paste("| all rules:", paste(fit$rules$rule_id, fit$rules$support, collapse = ", "))
  # G3 item 1 as written: the primary rule recovers the 5 exactly (hard check, kept as the
  # master states it; see MASTER_CHANGES item 10). Two informative checks follow it.
  check("orth_primary_recovers_5", identical(sel, E$support_key(O$active)), paste("cv_min support:", sel, all_rules))
  check("orth_primary_contains_5", all(O$active %in% E$parse_key(sel)), paste("cv_min support:", sel))
  check("orth_some_rule_exact", any(fit$rules$support == E$support_key(O$active)), all_rules)
})

# ---- 6. full wrapper on the p = 500 synthetic case: frame, grid, hygiene ----
safely("wrapper_p500", {
  ctrl_before <- glmnet::glmnet.control()
  cap <- E$with_captured_conditions(E$fit_F3_alasso(D500$X, D500$y, D500$foldid, 7L, S))
  fit <- cap$value
  check("wrapper_no_error", is.na(cap$error), cap$error)
  check("control_unchanged", identical(glmnet::glmnet.control(), ctrl_before))
  check("no_deprecation_warning", !any(grepl("deprecat", c(fit$warnings, cap$warnings), ignore.case = TRUE)),
        paste(c(fit$warnings, cap$warnings), collapse = " | "))
  r <- fit$rules
  check("frame_columns", identical(names(r), c(E$RULE_CORE_COLS, METH$extra_cols[[1]])))
  check("frame_registered_rules", identical(r$rule_id, METH$rule_ids[[1]]) && identical(r$role, METH$roles[[1]]))
  check("status_ok_no_conditions", all(r$status == "ok") && length(fit$warnings) == 0 && length(fit$messages) == 0,
        paste(r$status, collapse = ","))
  check("converged_true", isTRUE(fit$converged) && all(r$converged))
  d <- fit$diagnostics
  check("grid_first_point_null", d$path$k[1] == 0 && d$path$key[1] == "")
  check("grid_length", nrow(d$path) == S$GRID$nlambda)
  check("pf_normalised", abs(sum(d$v) - ncol(D500$X)) < 1e-9 * ncol(D500$X))
  check("kkt_all_fits_p500", max(d$fits$kkt_max) <= S$GLMNET$kkt_rel_tol,
        sprintf("max relative KKT over 11 fits %.2e; npasses %s", max(d$fits$kkt_max),
                paste(d$fits$npasses, collapse = ",")))
  check("diag_flag_consistent", all(r$diag_flag == (max(d$fits$kkt_max) > S$GLMNET$kkt_rel_tol)))
  ebic_rows <- r[r$rule_id %in% c("ebic1", "ebic05"), ]
  check("ebic_rows_kmax", all(ebic_rows$k <= S$COMMON$kmax_ebic) && all(!is.na(ebic_rows$k_valid_max)))
  i1 <- E$ebic_pick(d$candidates, "ebic1")
  check("ebic1_matches_candidates", identical(r$support[r$rule_id == "ebic1"], d$candidates$key[i1]))
  check("beta_at_cv_min", identical(E$support_key(which(fit$beta != 0)), r$support[r$rule_id == "cv_min"]))
  cat("  p500 synthetic rules:", paste(r$rule_id, r$k, sep = "=", collapse = " "),
      "| kappa_min", d$kappa_min, "| n_floored", d$n_floored, "| codes", paste(r$diag_codes, collapse = ","), "\n")
})

# ---- 7. null canary (G3 item 2) ----
safely("null_canary", {
  N0 <- make_design(200L, 500L, integer(), numeric(), S$TEST_SEED + 3L)
  # G3 item 2 under the frozen settings (hard). A glmnet jerr here (maxit = 1e6 total passes
  # reached near the interpolating end of the path) is the pre-declared pilot item of
  # §III.3.1 i / §IV.2.2 (MASTER_CHANGES item 8); the failed frame must be the registered one.
  fit0 <- E$fit_F3_alasso(N0$X, N0$y, N0$foldid, 1L, S)
  check("null_canary_runs", all(fit0$rules$status %in% c("ok", "warning")),
        paste("frozen GLMNET$maxit =", S$GLMNET$maxit, "|", paste(fit0$rules$rule_id, fit0$rules$k, collapse = ", "),
              "|", fit0$rules$error[1]))
  if (all(fit0$rules$status == "failed"))
    check("null_canary_frozen_failed_frame", all(is.na(fit0$rules$support)) && grepl("jerr", fit0$rules$error[1]),
          fit0$rules$error[1])
  # Informative: the same canary with the pre-declared action value maxit = 1e7.
  S7 <- S; S7$GLMNET$maxit <- 1e7
  fit <- E$fit_F3_alasso(N0$X, N0$y, N0$foldid, 1L, S7)
  r <- fit$rules
  big <- r$k > 0.3 * 500
  check("null_canary_runs_maxit1e7", all(r$status %in% c("ok", "warning")), paste(r$rule_id, r$k, collapse = ", "))
  if (any(big, na.rm = TRUE)) review("null_canary", paste("rule(s) above 30% of p:", paste(r$rule_id[big], collapse = ",")))
  cat("  null canary (maxit 1e7) k:", paste(r$rule_id, r$k, sep = "=", collapse = " "),
      "| max npasses", max(fit$diagnostics$fits$npasses), "\n")
})

# ---- 8. no-intercept canary (G3 item 3) ----
safely("no_intercept", {
  X <- D500$X; y3 <- D500$y + 3; yc <- y3 - mean(y3); n <- nrow(X); p <- ncol(X)
  B3 <- E$ridge_path_svd(X, y3, S$F3$kappa); Bc <- E$ridge_path_svd(X, yc, S$F3$kappa)
  # The ridge difference lives in the one exactly-null direction of centred X (singular value
  # ~1e-14, left vector proportional to 1): term d/(d^2 + n kappa) * sqrt(n) * mean(y), 3e-10 at
  # kappa = 1e-6 (diagnostic 2275655). Tolerance 1e-8 as for the paths; fitted values must agree.
  check("noint_ridge_full_path", max(abs(B3 - Bc)) <= 1e-8, sprintf("max abs diff %.2e", max(abs(B3 - Bc))))
  check("noint_ridge_fitted", max(abs(X %*% (B3 - Bc))) <= 1e-10, sprintf("max abs diff %.2e", max(abs(X %*% (B3 - Bc)))))
  rcv <- E$ridge_cv(X, yc, D500$foldid, S$F3$kappa)
  wt <- E$alasso_weights(rcv$B[, rcv$i_min], S$F3)
  lam <- S$GRID$max_mult * max(abs(drop(crossprod(X, yc))) / n / wt$v) * E$lambda_fraction(S$GRID)
  S7 <- S; S7$GLMNET$maxit <- 1e7       # used below for the full fits on y + 3 (pilot item)
  P3 <- E$glmnet_target_path(X, y3, 1, lam, wt$v, S$GLMNET)
  Pc <- E$glmnet_target_path(X, yc, 1, lam, wt$v, S$GLMNET)
  # §III.3.1 i as written: whole path within 1e-8 (hard; MASTER_CHANGES item 11). At p > n the
  # lasso objective is nearly flat as k approaches n, so two runs that both meet thresh can
  # differ by ~1e-5 there (diagnostic 2275655: 1.3e-5 at k = 197, KKT 2e-8 for both).
  err_all <- max(abs(P3$B - Pc$B))
  check("noint_weighted_path", err_all <= 1e-8, sprintf("whole-path max abs diff %.2e", err_all))
  # Informative: (a) the y + 3 path solves the centred problem (KKT), (b) identical supports and
  # coefficients within 1e-6 wherever k <= kmax_ebic = 100.
  kc <- colSums(Pc$B != 0); keep <- kc <= S$COMMON$kmax_ebic
  sc <- max(1, max(abs(drop(crossprod(X, yc)))) / n)
  kkt3c <- E$kkt_glmnet(X, yc, P3$B, lam, 1, wt$v, sc)
  check("noint_path_solves_centred_problem", max(kkt3c) <= S$GLMNET$kkt_rel_tol, sprintf("max rel KKT %.2e", max(kkt3c)))
  err <- max(abs(P3$B[, keep] - Pc$B[, keep]))
  same_sup <- identical(colSums(P3$B[, keep] != 0), kc[keep]) && all((P3$B[, keep] != 0) == (Pc$B[, keep] != 0))
  check("noint_weighted_path_k_le_100", err <= 1e-6 && same_sup,
        sprintf("%d points; max abs diff %.2e; identical supports %s; whole-path max diff %.2e",
                sum(keep), err, same_sup, max(abs(P3$B - Pc$B))))
  sup <- unique(lapply(seq_len(ncol(Pc$B)), function(j) which(Pc$B[, j] != 0)))
  sup <- sup[lengths(sup) <= 100]
  rel <- vapply(sup, function(s) {
    a <- E$ols_rss(X, y3, s, 1e-10)$rss; b <- E$ols_rss(X, yc, s, 1e-10)$rss
    abs(a - (b + n * mean(y3)^2)) / a
  }, 0)
  check("noint_rss_identity", max(rel) <= 1e-9, sprintf("%d supports, max rel diff %.2e", length(sup), max(rel)))
  f3 <- E$fit_F3_alasso(X, y3, D500$foldid, 1L, S7); fc <- E$fit_F3_alasso(X, yc, D500$foldid, 1L, S7)
  f3frozen <- E$fit_F3_alasso(X, y3, D500$foldid, 1L, S)
  if (all(f3frozen$rules$status == "failed"))
    review("noint_frozen_settings", paste("PILOT ITEM: y + 3 fit failed under GLMNET$maxit =", S$GLMNET$maxit, ":",
                                          f3frozen$rules$error[1]))
  cat("  (reported, not a failure; maxit 1e7) CV/EBIC choices y+3 vs centred:",
      paste(f3$rules$rule_id, f3$rules$k, fc$rules$k, sep = ":", collapse = " "),
      "| kappa_min", f3$diagnostics$kappa_min, fc$diagnostics$kappa_min, "\n")
})

# ---- 9. determinism (G3 item 5) ----
safely("determinism", {
  a <- E$fit_F3_alasso(D500$X, D500$y, D500$foldid, 11L, S)
  b <- E$fit_F3_alasso(D500$X, D500$y, D500$foldid, 11L, S)
  check("determinism_supports", identical(a$rules$support, b$rules$support))
  check("determinism_cvm_bitwise", identical(a$diagnostics$path$cvm, b$diagnostics$path$cvm) &&
          identical(a$diagnostics$ridge$cvm, b$diagnostics$ridge$cvm) && identical(a$beta, b$beta))
})

# ---- 10. failure path (G3 item 6) ----
safely("failure_path", {
  is_failed_frame <- function(r) all(r$status == "failed") && all(is.na(r$support)) && all(is.na(r$k)) &&
    identical(r$rule_id, METH$rule_ids[[1]]) && all(nzchar(r$error))
  S1 <- S; S1$GLMNET$maxit <- 1
  f1 <- E$fit_F3_alasso(D500$X, D500$y, D500$foldid, 1L, S1)
  check("fail_maxit_jerr", is_failed_frame(f1$rules) && identical(f1$converged, FALSE) && all(is.na(f1$beta)),
        f1$rules$error[1])
  check("fail_jerr_message_names_fit", grepl("^(full-data fit|fold [0-9]+): glmnet jerr = .*npasses", f1$rules$error[1]),
        f1$rules$error[1])
  S2 <- S; S2$F3$ridge_tol <- 0
  f2 <- E$fit_F3_alasso(D500$X, D500$y, D500$foldid, 1L, S2)
  check("fail_ridge_check", is_failed_frame(f2$rules), f2$rules$error[1])
  Xbad <- D500$X; Xbad[, 1] <- Xbad[, 1] + 1                 # not centred: assertion outside capture
  f3 <- rc$run_one_fit(METH, E, Xbad, D500$y, D500$foldid, 1L, S)
  check("fail_runner_outer_capture", is_failed_frame(f3$rules) && identical(f3$converged, FALSE), f3$rules$error[1])
  S4 <- S; S4$GLMNET$pkg_version <- "0.0"
  f4 <- rc$run_one_fit(METH, E, D500$X, D500$y, D500$foldid, 1L, S4)
  check("fail_version_assertion", is_failed_frame(f4$rules), f4$rules$error[1])
  check("fail_never_null_success", !any(c(f1$rules$support, f2$rules$support, f3$rules$support) %in% ""))
})

# ---- 11. rule-level failure from KKT (a forced tolerance; §III.3.1 f) ----
safely("rule_level_failure", {
  S5 <- S; S5$GLMNET$kkt_rel_tol <- 0                       # every point counts as a violation
  f <- E$fit_F3_alasso(D500$X, D500$y, D500$foldid, 1L, S5)
  r <- f$rules
  # cv rules fail (no exact KKT); an EBIC rule fails unless it chose the always-valid null.
  ok_cv <- all(r$status[1:2] == "failed") && all(!is.na(r$support_audit[1:2]))
  ok_eb <- all(ifelse(r$support_audit[3:4] %in% "" | r$support[3:4] %in% "", TRUE, r$status[3:4] == "failed"))
  check("rule_fail_kkt", ok_cv && ok_eb && all(r$diag_flag) && all(grepl("kkt_path", r$diag_codes)),
        paste(r$rule_id, r$status, r$diag_codes, collapse = " | "))
})

# ---- 12. no-oracle (§III.3.9; G3 item 7) ----
safely("no_oracle", {
  srcs <- c(file.path(CODE_ROOT, c("config.R", "common.R")),
            list.files(file.path(CODE_ROOT, "methods"), pattern = "\\.R$", full.names = TRUE))
  hits <- unlist(lapply(srcs, function(f) {
    L <- readLines(f)
    i <- grep("truth|\\$active|\\$signal|truth/", L, ignore.case = TRUE)
    if (length(i)) paste0(basename(f), ":", i) else character()
  }))
  check("no_oracle_grep", length(hits) == 0L, paste(c(length(srcs), "files;", hits), collapse = " "))
  # Runner on a copied dev input in a tree with no truth directory.
  src_in <- file.path(DEV_ROOT, "inputs", "p0500", "dev_p0500_S4_r001.rds")
  work <- file.path(TMP_ROOT, paste0("noracle_", Sys.getpid()))
  dir.create(file.path(work, "inputs", "p0500"), recursive = TRUE)
  file.copy(src_in, file.path(work, "inputs", "p0500"))
  rscript <- file.path(R.home("bin"), "Rscript")
  out <- system2(rscript, c(file.path(CODE_ROOT, "run_case.R"), "--input",
                            file.path(work, "inputs", "p0500", "dev_p0500_S4_r001.rds"),
                            "--out", file.path(work, "out"), "--run-id", "unit_test",
                            "--manifest", file.path(DEV_ROOT, "manifests", "dev_inputs_manifest.csv")),
                 stdout = TRUE, stderr = TRUE)
  cat(paste("  runner:", out), sep = "\n")
  csv <- file.path(work, "out", "results", "unit_test", "p0500", "dev_p0500_S4_r001_c100", "F3.csv")
  check("no_oracle_runner_without_truth_dir", file.exists(csv) && !dir.exists(file.path(work, "truth")))
  vs <- new.env(); sys.source(file.path(CODE_ROOT, "tests", "validate_outputs.R"), envir = vs)
  check("runner_output_validates", vs$validate_run(file.path(work, "out", "results", "unit_test"), CODE_ROOT, 1L))
  # Idempotency: a second call skips the completed (case, method).
  out2 <- system2(rscript, c(file.path(CODE_ROOT, "run_case.R"), "--input",
                             file.path(work, "inputs", "p0500", "dev_p0500_S4_r001.rds"),
                             "--out", file.path(work, "out"), "--run-id", "unit_test"), stdout = TRUE, stderr = TRUE)
  check("runner_idempotent_skip", any(grepl("already done", out2)), paste(out2, collapse = " "))
  # Completion check (Sol finding 3): an empty or incomplete .sha256 is not a valid completion.
  prefix <- file.path(dirname(csv), "F3")
  check("done_valid_complete", rc$done_is_valid(prefix, E))
  shaf <- paste0(prefix, ".sha256"); keep_sha <- readLines(shaf)
  writeLines(character(), shaf)
  ok_empty <- !rc$done_is_valid(prefix, E)
  writeLines(keep_sha[c(2L, 2L)], shaf)
  ok_dup <- !rc$done_is_valid(prefix, E)
  ok_val_dup <- !isTRUE(suppressWarnings(vs$validate_run(file.path(work, "out", "results", "unit_test"), CODE_ROOT, 1L)))
  writeLines(keep_sha, shaf)
  check("done_invalid_empty_or_duplicate_sha256", ok_empty && ok_dup && ok_val_dup)
  check("done_valid_restored", rc$done_is_valid(prefix, E))
  # Provenance (Astra finding 2): an intact result of another run is an error, not a skip.
  csv_rows <- utils::read.csv(paste0(prefix, ".csv"), stringsAsFactors = FALSE)
  check("done_provenance_match", rc$done_is_valid(prefix, E, list(run_id = "unit_test", case_id = csv_rows$case_id[1])))
  prov_err <- tryCatch({ rc$done_is_valid(prefix, E, list(run_id = "other_run")); "no error" },
                       error = function(e) conditionMessage(e))
  check("done_provenance_mismatch_refused", grepl("different run_id", prov_err), prov_err)
})

# ---- 13. engine cross-check against cv.glmnet with the adaptive penalty factors ----
for (pp in c(500L, 1000L)) safely(paste0("cvglmnet_", pp), {
  inp <- readRDS(file.path(DEV_ROOT, "inputs", sprintf("p%04d", pp), sprintf("dev_p%04d_S4_r001.rds", pp)))
  X <- inp$X; y <- unname(inp$Y[, "c100"]); fo <- inp$foldid
  fit <- E$fit_F3_alasso(X, y, fo, inp$method_seed, S)
  d <- fit$diagnostics
  G <- S$GLMNET
  cvg <- glmnet::cv.glmnet(X, y, alpha = 1, lambda = d$path$lambda, foldid = fo, penalty.factor = d$v,
                           intercept = FALSE, standardize = FALSE, type.gaussian = "naive",
                           type.measure = "mse", grouped = TRUE, keep = TRUE,
                           control = list(thresh = G$thresh, maxit = G$maxit, fdev = 0, devmax = 1))
  e_cvm <- max(abs(cvg$cvm / d$path$cvm - 1)); e_sd <- max(abs(cvg$cvsd / d$path$cvsd - 1))
  check(paste0("cvglmnet_cvm_cvsd_p", pp), e_cvm <= 1e-10 && e_sd <= 1e-10,
        sprintf("rel diff cvm %.2e, cvsd %.2e", e_cvm, e_sd))
  check(paste0("cvglmnet_index_p", pp), identical(unname(as.integer(cvg$index[, 1])), unname(as.integer(d$index))),
        paste("cv.glmnet", paste(cvg$index[, 1], collapse = ","), "engine", paste(d$index, collapse = ",")))
  ipre <- d$index[["min"]]
  e_pre <- max(abs(cvg$fit.preval[, ipre] - d$heldout[, "cv_min"]))
  check(paste0("cvglmnet_fitpreval_p", pp), e_pre <= 1e-10, sprintf("max abs diff %.2e", e_pre))
  cat(sprintf("  p=%d dev S4: KKT max over 11 fits %.2e (tol %.0e); kappa_min %g; n_floored %d; rules %s\n",
              pp, max(d$fits$kkt_max), G$kkt_rel_tol, d$kappa_min, d$n_floored,
              paste(fit$rules$rule_id, fit$rules$k, sep = "=", collapse = " ")))
})

res <- do.call(rbind, RESULTS)
cat("\nSUMMARY:", sum(res$pass), "passed,", sum(!res$pass), "failed of", nrow(res), "\n")
if (any(!res$pass)) cat("FAILED:", paste(res$test[!res$pass], collapse = ", "), "\n")
quit(save = "no", status = if (all(res$pass)) 0L else 1L)
