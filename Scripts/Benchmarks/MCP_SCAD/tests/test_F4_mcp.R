#!/usr/bin/env Rscript
# test_F4_mcp.R -- G3 unit tests for F4 MCP and F4_SCAD (master §III.3.4 i; §IV.3 unit tests 1-7;
# §III.3.0 EBIC/registry/capture rules; §III.3.9 no-oracle checks). Every test that does not need
# the pilot. Runs on NOTS inside a SLURM job (see slurm/unit_tests.slurm).
#
# Usage: Rscript tests/test_F4_mcp.R <code_dir> <dev_inputs_dir> <out_dir>
#   dev_inputs_dir = /projects/ml75/fb31/BVS/bench20261019/dev/inputs (inputs only; never truth/)

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3L) stop("usage: test_F4_mcp.R <code_dir> <dev_inputs_dir> <out_dir>")
code_dir <- normalizePath(args[1L], mustWork = TRUE)
inputs_dir <- normalizePath(args[2L], mustWork = TRUE)
out_dir <- args[3L]; dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
out_dir <- normalizePath(out_dir, mustWork = TRUE)

source(file.path(code_dir, "config.R"))
.libPaths(c(STUDY_LIB, .Library))
E <- new.env(parent = asNamespace("stats"))                # same isolation as the runner
sys.source(file.path(code_dir, "common.R"), envir = E)
sys.source(file.path(code_dir, "methods", "fit_F4_mcp.R"), envir = E)

results <- list(); details <- list()
record <- function(name, expr) {
  a <- tryCatch(force(expr), error = function(e) e)
  ok <- !inherits(a, "error")
  results[[name]] <<- data.frame(test = name, passed = ok,
                                 detail = if (ok) paste(format(a), collapse = " ") else conditionMessage(a),
                                 stringsAsFactors = FALSE)
  if (ok) details[[name]] <<- a
  cat(if (ok) "PASS " else "FAIL ", name, if (!ok) paste0(": ", conditionMessage(a)), "\n", sep = "")
  flush.console()
}
check <- function(cond, msg) if (!isTRUE(cond)) stop(msg, call. = FALSE)
settings_for <- function(mid, cfg = CONFIG) {
  s <- cfg; s$variant <- cfg$METHODS$variant[cfg$METHODS$method_id == mid]; s
}
fn_for <- function(mid) get(CONFIG$METHODS$fn[CONFIG$METHODS$method_id == mid], envir = E)
# Mimics the runner's outer capture layer and status rule (run_case.R) for wrapper-level tests.
run_like_runner <- function(mid, X, y, foldid, seed, cfg = CONFIG) {
  st <- settings_for(mid, cfg)
  cap <- E$with_captured_conditions(fn_for(mid)(X, y, foldid, seed, st))
  if (!is.na(cap$error)) {
    res <- list(rules = E$fail_rows(E$registry_row(st, mid), st$F4_EXTRA_COLS, cap$error),
                beta = rep(NA_real_, ncol(X)), pip = NULL, converged = FALSE,
                diagnostics = list(error = cap$error), warnings = character(), messages = character())
  } else res <- cap$value
  res$all_warnings <- c(res$warnings, cap$warnings); res$all_messages <- c(res$messages, cap$messages)
  if (length(res$all_warnings) + length(res$all_messages) > 0L)
    res$rules$status[res$rules$status == "ok"] <- "warning"
  res
}
read_dev <- function(p, s) readRDS(file.path(inputs_dir, sprintf("p%04d", p), sprintf("dev_p%04d_S%d_r001.rds", p, s)))
grid_for <- function(X, y) {                                # the wrapper's grid (§III.3.4 e step 1)
  CONFIG$GRID$max_mult * max(abs(crossprod(X, y))) / nrow(X) * E$lambda_fraction(CONFIG$GRID)
}
n <- 200L; s <- sqrt((n - 1) / n)

# Orthogonal design (§IV.3 item 1): X centred with X'X = (n - 1) I, p = 30, strong signal on 5.
RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(TEST_SEED)
Z <- scale(matrix(rnorm(n * 30), n), center = TRUE, scale = FALSE)
Xo <- qr.Q(qr(Z)) * sqrt(n - 1); attributes(Xo) <- list(dim = c(n, 30L))
act_o <- c(3L, 7L, 14L, 16L, 25L)
bo <- numeric(30); bo[act_o] <- c(1.4, -1.0, 1.8, -1.2, 0.8)
yo <- drop(Xo %*% bo) + rnorm(n) + 2                      # uncentred response
fold_o <- sample(rep(1:10, length.out = n))

# ---- 1. common helpers --------------------------------------------------------------------------
record("common_ebic_fixtures", {
  X <- cbind(c(-2, -1, 0, 1, 2), c(1, -2, 2, -2, 1), c(0.5, 0, -1, 0, 0.5)); y <- c(1, 3, -2, 4, 7)
  check(E$ols_rss(X, y, integer(), 1e-10)$rss == sum(y^2), "null RSS != sum(y^2)")
  bh <- solve(crossprod(X[, 1:2]), crossprod(X[, 1:2], y)); rss2 <- sum((y - X[, 1:2] %*% bh)^2)
  cand <- E$ebic_candidates(X, y, list(1:2, 1L, c(2L, 1L)), kmax = 3, gammas = c(ebic1 = 1, bic = 0), tol = 1e-10)
  check(nrow(cand) == 3L && identical(cand$key, c("", "1;2", "1")), "deduplication/null candidate wrong")
  check(abs(cand$ebic1[2] - (5 * log(rss2 / 5) + 2 * log(5) + 2 * lchoose(3, 2))) < 1e-12, "two-variable EBIC(1) wrong")
  check(abs(cand$bic[2] - (5 * log(rss2 / 5) + 2 * log(5))) < 1e-12, "two-variable BIC wrong")
  r1 <- E$ols_rss(X, y, 1L, 1e-10)                         # singleton support (drop = FALSE)
  check(abs(r1$rss - sum(lm.fit(matrix(X[, 1]), y)$residuals^2)) < 1e-12 && r1$rank == 1L, "singleton RSS wrong")
  cd <- E$ebic_candidates(cbind(X[, 1], X[, 1]), y, list(1:2), kmax = 3, gammas = c(ebic1 = 1), tol = 1e-10)
  check(is.infinite(cd$ebic1[2]) && !cd$valid[2], "rank-deficient support not Inf")
  cap <- E$ebic_candidates(X, y, list(1:3), kmax = 2, gammas = c(ebic1 = 1), tol = 1e-10)
  check(!("1;2;3" %in% cap$key), "kmax cap not applied")
  tie <- data.frame(key = c("9", "10", "2;3", ""), k = c(1L, 1L, 2L, 0L), crit = c(1, 1, 1, 2),
                    stringsAsFactors = FALSE)
  check(E$ebic_pick(tie, "crit") == 2L, "tie order: equal crit and k must break by C-locale key ('10' < '9')")
  check(identical(E$support_key(c(10L, 2L, 9L)), "2;9;10") && identical(E$parse_key(""), integer()) &&
        identical(E$parse_key("2;9;10"), c(2L, 9L, 10L)), "support keys wrong")
  check(identical(E$join_codes(c("ebic_at_largest", "kkt_path", "kkt_path")), "kkt_path;ebic_at_largest"),
        "code order wrong")
  check(inherits(tryCatch(E$join_codes("not_a_code"), error = function(e) e), "error"), "vocabulary not closed")
  TRUE
})

record("registry_and_fail_rows", {
  for (mid in CONFIG$METHODS$method_id) {
    mrow <- E$registry_row(CONFIG, mid)
    fr <- E$fail_rows(mrow, CONFIG$F4_EXTRA_COLS, "forced")
    check(identical(fr$rule_id, mrow$rule_ids[[1]]) && identical(fr$role, mrow$roles[[1]]), "fail rows != registry")
    check(all(fr$status == "failed") && all(is.na(fr$support)) && all(is.na(fr$k)) &&
          all(is.na(fr$support_audit)) && all(!fr$converged), "fail row fields wrong")
    check(all(c("lambda", "rss", "crit_value", "path_index", "k_valid_max", "k_path_max") %in% names(fr)),
          "extra columns missing")
  }
  check(identical(CONFIG$METHODS$roles[[1]], c("primary", "S0", "S0")) &&
        identical(CONFIG$METHODS$roles[[2]], c("S1", "S1", "S1")), "registered roles differ from §III.3.4 f")
  TRUE
})

record("library_and_version", {
  loc <- normalizePath(find.package("ncvreg"))
  check(startsWith(loc, normalizePath(STUDY_LIB)), paste("ncvreg loaded from", loc))
  check(identical(as.character(packageVersion("ncvreg")), "3.16.0"), "ncvreg version")
  check(inherits(tryCatch(E$assert_pkg_version("ncvreg", "3.15.0"), error = function(e) e), "error"),
        "version assertion does not fire")
  loc
})

# ---- 2. §III.3.4 i: compensation identity -----------------------------------------------------
record("compensation_identity", {
  pen <- function(b, lam, gam) ifelse(abs(b) <= gam * lam, lam * abs(b) - b^2 / (2 * gam), gam * lam^2 / 2)
  lam <- 0.7; gam <- 3
  bb <- c(0, 0.1, lam * gam, lam * gam + 1, -0.6, -3)
  check(max(abs(pen(bb, lam, gam) - pen(s * bb, lam / s, gam * s^2))) < 1e-12, "penalty identity")
  d <- read_dev(500L, 4L); X <- d$X; y <- unname(d$Y[, "c100"])
  XX <- ncvreg:::std(X)
  check(max(abs(attr(XX, "scale") - s)) < 1e-12, "std scale != s")
  check(max(abs(as.numeric(XX) - as.numeric(X / s))) < 1e-12, "std(X) != X/s")
  yc <- y - mean(y)
  for (b in list(numeric(ncol(X)), replace(numeric(ncol(X)), c(3, 37, 74), c(1.4, -1, 1.8)),
                 replace(numeric(ncol(X)), 1:5, c(gam * lam, -gam * lam, 0.9, 0.05, -2)))) {
    orig <- sum((y - X %*% b)^2) / (2 * n) + sum(pen(b, lam, gam))
    int  <- sum((yc - XX %*% (s * b))^2) / (2 * n) + sum(pen(s * b, lam / s, gam * s^2))
    check(abs((orig - int) - mean(y)^2 / 2) < 1e-10, "objectives do not differ by ybar^2/2")
  }
  TRUE
})

# ---- 3. orthogonal MCP canary and recovery ---------------------------------------------------
record("orthogonal_mcp_canary", {
  lam <- grid_for(Xo, yo)
  fit <- E$ncv_call(Xo, yo, lam, settings_for("F4"), "MCP")
  check(length(fit$lambda) == length(lam), "path truncated")
  b <- as.matrix(fit$beta[-1, , drop = FALSE]); z <- drop(crossprod(Xo, yo)) / n; gam <- CONFIG$F4$mcp_gamma
  maxerr <- 0
  for (l in seq_along(lam)) {
    la <- lam[l]
    cf <- ifelse(abs(z) <= la, 0,
          ifelse(abs(z) <= gam * la * s^2, sign(z) * (abs(z) - la) / (s^2 - 1 / gam), z / s^2))
    maxerr <- max(maxerr, abs(b[, l] - cf))
  }
  check(maxerr <= 1e-6, paste("max deviation from closed form", maxerr))
  res <- run_like_runner("F4", Xo, yo, fold_o, 1L)
  r <- res$rules
  check(all(r$status == "ok"), paste("status", paste(r$status, collapse = ",")))
  check(identical(r$support[r$rule_id == "ebic1"], paste(act_o, collapse = ";")), "ebic1 does not recover the 5")
  check(isTRUE(res$converged) && !any(r$diag_flag), "canary flagged or not converged")
  sprintf("max closed-form error %.2e", maxerr)
})

# ---- 4. orthogonal SCAD canary (documents the non-equivalence) -------------------------------
record("orthogonal_scad_canary", {
  lam <- grid_for(Xo, yo); a <- CONFIG$F4$scad_gamma
  fit <- E$ncv_call(Xo, yo, lam, settings_for("F4_SCAD"), "SCAD")
  check(length(fit$lambda) == length(lam), "path truncated")
  th <- s * as.matrix(fit$beta[-1, , drop = FALSE]); u <- drop(crossprod(Xo, yo)) / n / s
  maxerr <- 0; branch_count <- integer(4)
  for (l in seq_along(lam)) {
    lp <- lam[l] / s; au <- abs(u)
    br <- ifelse(au <= lp, 1L, ifelse(au <= 2 * lp, 2L, ifelse(au <= a * lp, 3L, 4L)))
    cf <- ifelse(br == 1L, 0, ifelse(br == 2L, sign(u) * (au - lp),
          ifelse(br == 3L, sign(u) * ((a - 1) * au - a * lp) / (a - 2), u)))
    maxerr <- max(maxerr, abs(th[, l] - cf)); branch_count <- branch_count + tabulate(br, 4)
  }
  check(all(branch_count > 0), paste("not every interval exercised:", paste(branch_count, collapse = ",")))
  check(maxerr <= 1e-6, paste("max deviation from threshold formula", maxerr))
  res <- run_like_runner("F4_SCAD", Xo, yo, fold_o, 1L)
  check(all(res$rules$status == "ok"), "SCAD status not ok")
  check(identical(res$rules$support[res$rules$rule_id == "ebic1"], paste(act_o, collapse = ";")),
        "SCAD ebic1 does not recover the 5")
  sprintf("max error %.2e; branch counts %s", maxerr, paste(branch_count, collapse = ","))
})

# ---- 5. KKT at p > n (one dev case per p), first grid point null, independent KKT check -------
kkt_loop_mcp <- function(X, y, b, la, gam) {                 # plain-loop re-implementation
  r <- y - X %*% b; worst <- 0
  for (j in seq_len(ncol(X))) {
    g <- sum(X[, j] * r) / nrow(X)
    v <- if (b[j] != 0) abs(g - sign(b[j]) * max(la - abs(b[j]) / gam, 0)) else max(abs(g) - la, 0)
    worst <- max(worst, v)
  }
  worst
}
kkt_loop_scad <- function(X, y, b, la, a, s) {
  r <- y - X %*% b; lp <- la / s; worst <- 0
  for (j in seq_len(ncol(X))) {
    g <- sum(X[, j] * r) / nrow(X) / s; t <- abs(s * b[j])
    if (b[j] != 0) {
      d <- if (t <= lp) lp else if (t <= a * lp) (a * lp - t) / (a - 1) else 0
      v <- abs(g - sign(b[j]) * d)
    } else v <- max(abs(g) - lp, 0)
    worst <- max(worst, v)
  }
  worst
}
for (p in c(500L, 1000L)) for (mid in c("F4", "F4_SCAD")) {
  record(sprintf("kkt_p%d_%s", p, mid), {
    d <- read_dev(p, 4L); X <- d$X; y <- unname(d$Y[, "c100"])
    res <- run_like_runner(mid, X, y, d$foldid, d$method_seed)
    path <- res$diagnostics$path
    check(nrow(path) == CONFIG$GRID$nlambda, paste("returned", nrow(path), "of", CONFIG$GRID$nlambda))
    check(path$k[1] == 0L, "first grid point is not the null model")
    check(all(path$kkt_max <= CONFIG$F4$kkt_abs_tol), sprintf("max KKT %.3e", max(path$kkt_max)))
    check(isTRUE(res$converged), "not converged")
    # Independent plain-loop KKT at 5 path points, compared with the vectorised helper.
    fit <- E$ncv_call(X, y, grid_for(X, y), settings_for(mid), if (mid == "F4") "MCP" else "SCAD")
    b <- as.matrix(fit$beta[-1, , drop = FALSE])
    for (l in unique(round(seq(1, ncol(b), length.out = 5)))) {
      la <- fit$lambda[l] * s
      ref <- if (mid == "F4") kkt_loop_mcp(X, y, b[, l], la, 3) else kkt_loop_scad(X, y, b[, l], la, 3.7, s)
      check(abs(ref - path$kkt_max[l]) <= 1e-12, sprintf("KKT helper differs from loop at l = %d", l))
    }
    sprintf("max KKT %.3e; max rec err %.3e; total iter %d; k_path_max %d",
            max(path$kkt_max), max(path$rec_err), res$diagnostics$total_iter, max(path$k))
  })
}

# ---- 6. RSS(y) = RSS(yc) + n ybar^2 (G3 one-off, §III.3.4 e step 4) and no-intercept canary ---
record("no_intercept_canary", {
  d <- read_dev(500L, 4L); X <- d$X; y0 <- unname(d$Y[, "c100"])
  yc <- y0 - mean(y0); y3 <- yc + 3                          # response with mean 3
  out <- character()
  for (mid in c("F4", "F4_SCAD")) {
    pen <- if (mid == "F4") "MCP" else "SCAD"
    lam <- grid_for(X, y3)                                   # same fixed grid for both fits
    f3 <- E$ncv_call(X, y3, lam, settings_for(mid), pen); fc <- E$ncv_call(X, yc, lam, settings_for(mid), pen)
    b3 <- as.matrix(f3$beta[-1, , drop = FALSE]); bc <- as.matrix(fc$beta[-1, , drop = FALSE])
    check(identical(dim(b3), dim(bc)), "path lengths differ")
    dev <- max(abs(b3 - bc))
    check(dev <= 1e-8 * max(1, max(abs(bc))), sprintf("%s paths differ by %.3e", mid, dev))
    check(identical(b3 != 0, bc != 0), "supports differ along the path")
    # (b) per-support OLS RSS relation on the path supports with k <= 100.
    sup <- unique(lapply(seq_len(ncol(bc)), function(l) which(bc[, l] != 0)))
    sup <- sup[lengths(sup) <= CONFIG$COMMON$kmax_ebic]
    rel <- vapply(sup, function(S) {
      r3 <- E$ols_rss(X, y3, S, 1e-10)$rss; rc <- E$ols_rss(X, yc, S, 1e-10)$rss
      abs(r3 - (rc + n * mean(y3)^2)) / r3 }, 0.0)
    check(max(rel) <= 1e-8, sprintf("RSS relation off by %.3e (relative)", max(rel)))
    # Fitted-coefficient form on the original y (the relation behind e step 4).
    rss_y  <- colSums((y3 - X %*% b3)^2); rss_yc <- colSums((y3 - mean(y3) - X %*% b3)^2)
    check(max(abs(rss_y - rss_yc - n * mean(y3)^2) / rss_y) <= 1e-10, "path RSS relation fails")
    # (c) EBIC choices may differ (n ybar^2 enters log(RSS/n)); reported, not a failure.
    r3 <- run_like_runner(mid, X, y3, d$foldid, 1L)$rules; rc <- run_like_runner(mid, X, yc, d$foldid, 1L)$rules
    out <- c(out, sprintf("%s path dev %.1e; EBIC choices identical (y+3 vs yc): %s", mid, dev,
                          paste(r3$rule_id, r3$support == rc$support, sep = "=", collapse = ",")))
  }
  paste(out, collapse = " | ")
})

# ---- 7. null canary (beta = 0) ----------------------------------------------------------------
record("null_canary", {
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(TEST_SEED + 1L)
  X <- scale(matrix(rnorm(n * 500), n)); attributes(X) <- list(dim = c(n, 500L))
  y <- rnorm(n); fid <- sample(rep(1:10, length.out = n))
  out <- character()
  for (mid in c("F4", "F4_SCAD")) {
    r <- run_like_runner(mid, X, y, fid, 1L)$rules
    check(all(r$status %in% c("ok", "warning")), paste(mid, "failed on the null canary"))
    check(all(r$k <= 0.3 * 500), paste(mid, "a rule selects more than 30% of p (flag for review)"))
    out <- c(out, sprintf("%s k = %s", mid, paste(r$rule_id, r$k, sep = ":", collapse = ",")))
  }
  paste(out, collapse = " | ")
})

# ---- 8. determinism -----------------------------------------------------------------------------
record("determinism", {
  d <- read_dev(1000L, 3L); X <- d$X; y <- unname(d$Y[, "c100"])
  for (mid in c("F4", "F4_SCAD")) {
    r1 <- run_like_runner(mid, X, y, d$foldid, d$method_seed); r2 <- run_like_runner(mid, X, y, d$foldid, d$method_seed)
    check(identical(r1$rules, r2$rules) && identical(r1$beta, r2$beta) &&
          identical(r1$diagnostics$path, r2$diagnostics$path), paste(mid, "not bit-identical"))
  }
  TRUE
})

# ---- 9. failure paths (§IV.3 item 6) and flags -----------------------------------------------
record("failure_input_error", {
  Xb <- Xo; Xb[, 1] <- Xb[, 1] + 1                           # not centred: assert_inputs stops
  for (mid in c("F4", "F4_SCAD")) {
    res <- run_like_runner(mid, Xb, yo, fold_o, 1L)
    r <- res$rules
    check(all(r$status == "failed") && all(is.na(r$support)) && all(is.na(r$k)) && all(!r$converged),
          "input error did not give failed rows")
    check(identical(r$rule_id, CONFIG$METHODS$rule_ids[[1]]), "not the registered rows")
    check(all(is.na(res$beta)) && length(res$beta) == ncol(Xo) && is.null(res$pip), "failed beta not NA")
    check(all(grepl("not centred", r$error)), "error message not recorded")
  }
  TRUE
})

record("failure_fit_gate", {
  cfg <- CONFIG; cfg$F4$lambda_rel_tol <- -1                 # forces the "altered lambda" gate
  res <- run_like_runner("F4", Xo, yo, fold_o, 1L, cfg)
  r <- res$rules
  check(all(r$status == "failed") && all(is.na(r$support)) && all(is.na(r$k)), "gate did not fail the fit")
  check(identical(r$support_audit[r$rule_id == "ebic1"], paste(act_o, collapse = ";")), "support_audit not kept")
  check(all(!r$converged) && all(is.na(res$beta)), "converged/beta wrong after gate failure")
  check(all(grepl("altered lambda", r$error)), "gate message missing")
  cfg2 <- CONFIG; cfg2$F4$loss_abs_tol <- -1                 # forces the residual-reconstruction gate
  r2 <- run_like_runner("F4_SCAD", Xo, yo, fold_o, 1L, cfg2)$rules
  check(all(r2$status == "failed") && all(grepl("residual reconstruction", r2$error)), "reconstruction gate")
  TRUE
})

record("failure_rule_kkt", {
  cfg <- CONFIG; cfg$F4$kkt_abs_tol <- -1                    # every point fails KKT
  res <- run_like_runner("F4", Xo, yo, fold_o, 1L, cfg)
  r <- res$rules
  nonnull <- !is.na(r$support_audit) & nzchar(r$support_audit)
  check(any(nonnull), "expected a non-null selection")
  check(all(r$status[nonnull] == "failed") && all(is.na(r$support[nonnull])), "non-null rule not failed")
  check(all(r$diag_flag) && all(grepl("kkt_path", r$diag_codes)), "kkt_path flag not on every row")
  check(all(is.na(res$beta)), "beta should be NA when ebic1 failed")
  TRUE
})

record("flag_path_truncated_warning", {
  cfg <- CONFIG; cfg$F4$maxit <- 200                          # total-iteration cap reached early
  res <- run_like_runner("F4", Xo, yo, fold_o, 1L, cfg)
  r <- res$rules
  check(any(grepl("Maximum number of iterations reached", res$all_warnings)), "ncvreg warning not captured")
  check(all(r$diag_flag) && all(grepl("path_truncated", r$diag_codes)), "path_truncated not flagged")
  check(all(!r$converged), "converged should be FALSE")
  check(all(r$status %in% c("warning", "failed")) && !any(r$status == "ok"), "status should be warning")
  check(res$diagnostics$n_lambda_returned < CONFIG$GRID$nlambda, "path not truncated")
  sprintf("returned %d points; statuses %s", res$diagnostics$n_lambda_returned, paste(r$status, collapse = ","))
})

record("failure_after_call_keeps_warnings", {
  cfg <- CONFIG; cfg$F4$maxit <- 200                          # ncvreg warns (iteration cap) ...
  names(cfg$COMMON$ebic_gamma) <- c("g1", "g05", "g0")        # ... and post-processing then errors
  res <- run_like_runner("F4", Xo, yo, fold_o, 1L, cfg)
  r <- res$rules
  check(all(r$status == "failed") && all(is.na(r$support)) && all(!r$converged), "post-call error not failed rows")
  check(any(grepl("Maximum number of iterations reached", res$warnings)), "package warning lost after the error")
  check(all(is.na(res$beta)) && !is.null(res$diagnostics$error), "failed-fit fields wrong")
  res$diagnostics$error
})

# ---- 10. no-oracle (§III.3.9) and runner end to end with no truth/ tree --------------------------
record("no_oracle_grep", {
  src <- c(file.path(code_dir, c("config.R", "common.R")),
           list.files(file.path(code_dir, "methods"), pattern = "[.]R$", full.names = TRUE))
  hits <- unlist(lapply(src, function(f) {
    L <- readLines(f); i <- grep("truth|\\$active|\\$signal|truth/", L)
    if (length(i)) paste0(basename(f), ":", i) else character()
  }))
  check(length(hits) == 0L, paste("hits:", paste(hits, collapse = ",")))
  paste(length(src), "files clean")
})

record("runner_end_to_end_no_truth", {
  sandbox <- file.path(out_dir, "runner_sandbox"); unlink(sandbox, recursive = TRUE)
  dir.create(file.path(sandbox, "inputs"), recursive = TRUE)
  src_in <- file.path(inputs_dir, "p0500", "dev_p0500_S2_r001.rds")
  inp <- file.path(sandbox, "inputs", basename(src_in)); file.copy(src_in, inp)
  check(!dir.exists(file.path(sandbox, "truth")), "sandbox has a truth/ tree")
  outr <- file.path(sandbox, "results", "unit_runner")
  rs <- file.path(R.home("bin"), "Rscript")
  st <- system2(rs, c(file.path(code_dir, "run_case.R"), "--input", inp, "--out-root", outr,
                      "--run-id", "unit_runner", "--scale", "c100"), stdout = TRUE, stderr = TRUE)
  check(is.null(attr(st, "status")), paste("runner failed:", paste(st, collapse = " / ")))
  cdir <- file.path(outr, "p0500", "dev_p0500_S2_r001_c100")
  for (mid in c("F4", "F4_SCAD")) {
    f <- file.path(cdir, paste0(mid, c(".rds", ".csv", ".sha256", ".done")))
    check(all(file.exists(f)), paste("missing outputs for", mid))
    csv <- read.csv(f[2], stringsAsFactors = FALSE)
    check(nrow(csv) == 3L && identical(csv$method_id, rep(mid, 3)), "csv rows wrong")
    check(all(is.na(csv$tp)) && all(is.na(csv$exact)), "scoring columns filled at fit time")
  }
  st2 <- system2(rs, c(file.path(code_dir, "run_case.R"), "--input", inp, "--out-root", outr,
                       "--run-id", "unit_runner", "--scale", "c100"), stdout = TRUE, stderr = TRUE)
  check(sum(grepl("skipped", st2)) == 2L, "rerun did not skip completed outputs")
  # Validator on the two good outputs: exit 0.
  vout <- file.path(sandbox, "validation_good.txt")
  v1 <- system2(rs, c(file.path(code_dir, "validate_dev.R"), code_dir, outr, "p0500/dev_p0500_S2_r001_c100", vout),
                stdout = TRUE, stderr = TRUE)
  check(is.null(attr(v1, "status")), paste("validator rejected good outputs:", paste(v1, collapse = " / ")))
  # A rerun under a different run id must refuse to reuse the completed outputs.
  st3 <- system2(rs, c(file.path(code_dir, "run_case.R"), "--input", inp, "--out-root", outr,
                       "--run-id", "another_run", "--scale", "c100"), stdout = TRUE, stderr = TRUE)
  check(!is.null(attr(st3, "status")) && any(grepl("different request", st3)), "stale .done was reused")
  # Errored fit through the runner (X not centred): failed rows; the validator accepts the failed-fit form.
  dbad <- readRDS(inp); dbad$X[, 1] <- dbad$X[, 1] + 1; dbad$dataset_id <- "dev_p0500_S9_r001"
  inp_bad <- file.path(sandbox, "inputs", "dev_p0500_S9_r001.rds"); saveRDS(dbad, inp_bad)
  st4 <- system2(rs, c(file.path(code_dir, "run_case.R"), "--input", inp_bad, "--out-root", outr,
                       "--run-id", "unit_runner", "--scale", "c100"), stdout = TRUE, stderr = TRUE)
  check(is.null(attr(st4, "status")), "runner did not complete on an errored fit")
  bcsv <- read.csv(file.path(outr, "p0500", "dev_p0500_S9_r001_c100", "F4.csv"), stringsAsFactors = FALSE)
  check(all(bcsv$status == "failed") && all(is.na(bcsv$support)) && all(grepl("not centred", bcsv$error)),
        "errored fit not written as failed rows")
  v2 <- system2(rs, c(file.path(code_dir, "validate_dev.R"), code_dir, outr, "p0500/dev_p0500_S9_r001_c100",
                      file.path(sandbox, "validation_errored.txt")), stdout = TRUE, stderr = TRUE)
  check(is.null(attr(v2, "status")), paste("validator rejected an errored fit:", paste(v2, collapse = " / ")))
  # Tampered diagnostics (hashes rewritten so only the content checks can catch them): the validator
  # must re-derive point passes and candidate validity rather than trust the saved columns.
  # Copies go under another root; `case` is the directory name they are placed in.
  tamper <- function(tag, edit, case = "dev_p0500_S2_r001_c100") {
    troot <- file.path(sandbox, paste0("tamper_", tag))
    td <- file.path(troot, "p0500", case); dir.create(td, recursive = TRUE, showWarnings = FALSE)
    for (ext in c(".rds", ".csv", ".done")) file.copy(file.path(cdir, paste0("F4", ext)), td, overwrite = TRUE)
    o <- readRDS(file.path(td, "F4.rds")); o <- edit(o); saveRDS(o, file.path(td, "F4.rds"))
    fl <- file.path(td, c("F4.rds", "F4.csv"))
    writeLines(paste(vapply(fl, E$file_sha256, ""), basename(fl), sep = "  "), file.path(td, "F4.sha256"))
    vf <- file.path(sandbox, paste0("validation_tamper_", tag, ".txt"))
    v <- system2(rs, c(file.path(code_dir, "validate_dev.R"), code_dir, troot, paste0("p0500/", case), vf),
                 stdout = TRUE, stderr = TRUE)
    list(status = if (is.null(attr(v, "status"))) 0L else attr(v, "status"), txt = readLines(vf))
  }
  tc <- tamper("control", function(o) o)                     # unedited copy, rehashed: valid
  check(tc$status == 0L, paste("control copy rejected:", paste(tc$txt, collapse = " / ")))
  tp <- tamper("passes", function(o) { o$diagnostics$path$passes[] <- FALSE; o })
  check(tp$status == 1L && any(grepl("saved passes differ", tp$txt)), "validator trusted tampered passes")
  tv <- tamper("valid", function(o) {
    i <- which(o$diagnostics$candidates$key == o$rows$support[1]); o$diagnostics$candidates$rank[i] <- 0L; o })
  check(tv$status == 1L && any(grepl("candidate table inconsistent", tv$txt)), "validator trusted tampered validity")
  tm <- tamper("moved", function(o) o, case = "dev_p0500_S3_r001_c100")   # valid set in another case's directory
  check(tm$status == 1L && any(grepl("does not belong", tm$txt)), "validator accepted a moved output set")
  # A pair held by another writer (lock directory present) is refused, and the lock is left in place.
  dlock <- readRDS(inp); dlock$dataset_id <- "dev_p0500_S8_r001"
  inp_lock <- file.path(sandbox, "inputs", "dev_p0500_S8_r001.rds"); saveRDS(dlock, inp_lock)
  lockdir <- file.path(outr, "p0500", "dev_p0500_S8_r001_c100", "F4.lock")
  dir.create(lockdir, recursive = TRUE)
  st6 <- system2(rs, c(file.path(code_dir, "run_case.R"), "--input", inp_lock, "--out-root", outr,
                       "--run-id", "unit_runner", "--scale", "c100"), stdout = TRUE, stderr = TRUE)
  check(!is.null(attr(st6, "status")) && any(grepl("locked", st6)) && dir.exists(lockdir) &&
        !file.exists(file.path(dirname(lockdir), "F4.done")), "locked pair was not refused")
  # Incomplete checksum list: the runner refuses it and the validator exits 1.
  writeLines(readLines(file.path(cdir, "F4.sha256"))[1], file.path(cdir, "F4.sha256"))
  st5 <- system2(rs, c(file.path(code_dir, "run_case.R"), "--input", inp, "--out-root", outr,
                       "--run-id", "unit_runner", "--scale", "c100"), stdout = TRUE, stderr = TRUE)
  check(!is.null(attr(st5, "status")) && any(grepl("incomplete hashes", st5)), "incomplete .sha256 accepted by runner")
  v3 <- system2(rs, c(file.path(code_dir, "validate_dev.R"), code_dir, outr, "p0500/dev_p0500_S2_r001_c100",
                      file.path(sandbox, "validation_bad.txt")), stdout = TRUE, stderr = TRUE)
  check(identical(attr(v3, "status"), 1L), "validator did not exit 1 on an incomplete .sha256")
  paste(st, collapse = " / ")
})

res <- do.call(rbind, results)
write.csv(res, file.path(out_dir, "unit_test_results.csv"), row.names = FALSE)
saveRDS(list(results = res, details = details, session = sessionInfo()), file.path(out_dir, "unit_test_results.rds"))
cat(sprintf("\n%d of %d tests passed\n", sum(res$passed), nrow(res)))
quit(save = "no", status = if (all(res$passed)) 0L else 1L)
