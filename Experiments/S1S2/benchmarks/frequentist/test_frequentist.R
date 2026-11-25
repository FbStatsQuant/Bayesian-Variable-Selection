# =============================================================================
# PROVENANCE  test_frequentist.R  (unit test for fit_lasso_cv.R and fit_scad.R)
# -----------------------------------------------------------------------------
# Purpose: show that both adapters (a) never error, (b) honour the INTERFACE.md
# contract, (c) are EXACTLY the package authors' default calls, (d) depend on
# method_seed only, (e) give sane selected sets and timings.
# Software under test: glmnet (cv.glmnet) and ncvreg (cv.ncvreg), versions
# printed at run time; see the PROVENANCE blocks of the two adapters.
# Everything in this file is test scaffolding and is OURS:
#   - data generators below are local to the test (the harness generator is
#     harness/generate.R, not written by this builder). Designs follow
#       S1: Griffin, Latuszynski & Steel (2021), DOI 10.1093/biomet/asaa055,
#           Sec 4.1: beta* = SNR*sqrt(sigma^2 log(p)/n)*(2,-3,2,2,-3,3,-2,3,-2,3,0,..),
#           sigma^2 = 1, Sigma_jk = rho^|j-k|, rho = 0.6;  test size n=200, p=500.
#       S2: Hastie, Tibshirani & Tibshirani (2020), DOI 10.1214/19-STS733,
#           Sec 3.1 (arXiv:1707.08692v2): rows N(0, Sigma), Sigma_ij = rho^|i-j|,
#           beta-type 2 (first s entries 1), sigma^2 = beta' Sigma beta / SNR;
#           "high-5" size n=50, p=1000, s=5, rho = 0.35.
#   - test seeds are arbitrary fixed numbers; method_seed follows the INTERFACE
#     formula data_seed + 10000000*method_code (lasso_cv 2, scad 3).
# Run (Owls only, lean):
#   OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 19 Rscript test_frequentist.R [--full]
#   --full adds one fit per method at the largest S1 size (n=1000, p=5000) for timing.
# Exit status 0 = all checks passed; 1 = at least one check failed.
# =============================================================================

args <- commandArgs(trailingOnly = FALSE)
here <- dirname(normalizePath(sub("^--file=", "", args[grep("^--file=", args)][1])))
full <- "--full" %in% commandArgs(trailingOnly = TRUE)
RLIB <- "/home/fb31/Bayesian-Variable-Selection/_local/engineering/Rlib"
.libPaths(c(RLIB, .libPaths()))
source(file.path(here, "fit_lasso_cv.R"))
source(file.path(here, "fit_scad.R"))

n_fail <- 0L
check <- function(ok, what) {
  ok <- isTRUE(ok)
  if (!ok) n_fail <<- n_fail + 1L
  cat(sprintf("  [%s] %s\n", if (ok) "PASS" else "FAIL", what))
  invisible(ok)
}

# ---- test data generators (OURS, test only) ---------------------------------
ar1_design <- function(n, p, rho) {
  Z <- matrix(rnorm(n * p), n, p)
  X <- Z
  if (rho != 0) for (j in 2:p) X[, j] <- rho * X[, j - 1] + sqrt(1 - rho^2) * Z[, j]
  X
}
gen_s1 <- function(n, p, snr, rho = 0.6, seed) {
  set.seed(seed)
  X <- ar1_design(n, p, rho)
  beta <- numeric(p)
  beta[1:10] <- snr * sqrt(log(p) / n) * c(2, -3, 2, 2, -3, 3, -2, 3, -2, 3)
  list(X = X, y = as.numeric(X %*% beta + rnorm(n)), support = 1:10, data_seed = seed)
}
gen_s2 <- function(n, p, s, snr, rho, seed) {
  set.seed(seed)
  X <- ar1_design(n, p, rho)
  beta <- numeric(p); beta[1:s] <- 1
  Sig_ss <- rho^abs(outer(1:s, 1:s, "-"))
  sigma2 <- as.numeric(t(beta[1:s]) %*% Sig_ss %*% beta[1:s]) / snr
  list(X = X, y = as.numeric(X %*% beta + sqrt(sigma2) * rnorm(n)), support = 1:s, data_seed = seed)
}

cases <- list(
  "S1-like n=200 p=500 rho=.6 SNR=3"    = gen_s1(200, 500, 3,   seed = 501001001),
  "S1-like n=200 p=500 rho=.6 SNR=0.5"  = gen_s1(200, 500, 0.5, seed = 501002001),
  "S2 hi-5 n=50 p=1000 rho=.35 SNR=6"   = gen_s2(50, 1000, 5, 6,    0.35, seed = 502001001),
  "S2 hi-5 n=50 p=1000 rho=.35 SNR=0.42"= gen_s2(50, 1000, 5, 0.42, 0.35, seed = 502002001)
)
if (full) cases[["S1 full n=1000 p=5000 rho=.6 SNR=2"]] <- gen_s1(1000, 5000, 2, seed = 501016001)

methods <- list(lasso_cv = list(f = fit_lasso_cv, code = 2L),
                scad     = list(f = fit_scad,     code = 3L))

cat("== versions ==\n")
cat(R.version.string, "\n")
cat("glmnet", as.character(packageVersion("glmnet")), " ncvreg", as.character(packageVersion("ncvreg")), "\n")
cat("host", Sys.info()[["nodename"]], " OMP_NUM_THREADS =", Sys.getenv("OMP_NUM_THREADS", "<unset>"), "\n\n")

# ---- 1. package defaults are the ones the PROVENANCE blocks cite -------------
cat("== 1. package defaults pinned ==\n")
fg <- formals(glmnet::glmnet); fc <- formals(glmnet::cv.glmnet); gc <- glmnet::glmnet.control()
check(eval(fc$nfolds) == 10, "cv.glmnet nfolds default = 10")
check(eval(fg$alpha) == 1 && eval(fg$nlambda) == 100, "glmnet alpha = 1, nlambda = 100")
check(isTRUE(eval(fg$standardize)) && isTRUE(eval(fg$intercept)), "glmnet standardize = TRUE, intercept = TRUE")
check(identical(deparse(fg$lambda.min.ratio), "ifelse(nobs < nvars, 0.01, 1e-04)"),
      "glmnet lambda.min.ratio = ifelse(nobs < nvars, 0.01, 1e-04)")
check(gc$thresh == 1e-07 && gc$maxit == 1e+05 && gc$fdev == 1e-05 && gc$devmax == 0.999,
      "glmnet.control at factory values (thresh 1e-7, maxit 1e5, fdev 1e-5, devmax 0.999)")
check(identical(eval(formals(glmnet:::coef.cv.glmnet)$s)[1], "lambda.1se"),
      "coef.cv.glmnet default s = 'lambda.1se'")
fn <- formals(ncvreg::ncvreg); fcn <- formals(ncvreg::cv.ncvreg)
check(eval(fcn$nfolds) == 10, "cv.ncvreg nfolds default = 10")
check(identical(deparse(fn$gamma), "switch(penalty, SCAD = 3.7, 3)"), "ncvreg gamma default: SCAD = 3.7")
check(eval(fn$alpha) == 1 && eval(fn$nlambda) == 100 && eval(fn$eps) == 1e-04 && eval(fn$max.iter) == 10000,
      "ncvreg alpha = 1, nlambda = 100, eps = 1e-4, max.iter = 10000")
check(identical(deparse(fn$lambda.min), "ifelse(n > p, 0.001, 0.05)"),
      "ncvreg lambda.min = ifelse(n > p, 0.001, 0.05)")
check(identical(deparse(formals(ncvreg:::coef.cv.ncvreg)$which), "object$min"),
      "coef.cv.ncvreg default = coefficients at lambda.min")

# ---- 2. contract, fidelity, determinism, sanity on each dataset --------------
contract_ok <- function(r, p) {
  identical(names(r), c("selected", "pip", "runtime_sec", "software", "settings", "extra")) &&
    is.integer(r$selected) && !is.unsorted(r$selected, strictly = TRUE) &&
    all(r$selected >= 1L & r$selected <= p) && is.null(r$pip) &&
    is.numeric(r$runtime_sec) && length(r$runtime_sec) == 1L && is.finite(r$runtime_sec) &&
    r$runtime_sec >= 0 && is.character(r$software$name) && is.character(r$software$version) &&
    length(r$settings) > 0L &&
    all(vapply(r$settings, function(s) isTRUE(s$tag %in% c("author", "OURS")), logical(1))) &&
    is.character(r$extra$status) && is.character(r$extra$warnings)
}
rows <- list()
for (cn in names(cases)) {
  d <- cases[[cn]]; p <- ncol(d$X); n <- nrow(d$X)
  for (mn in names(methods)) {
    cat(sprintf("\n== 2. %s | %s ==\n", cn, mn))
    m <- methods[[mn]]; mseed <- d$data_seed + 10000000L * m$code
    r <- tryCatch(m$f(d$X, d$y, mseed), error = function(e) e)
    if (!check(!inherits(r, "error"), "adapter returned without an R error")) next
    check(contract_ok(r, p), "return value matches the INTERFACE.md contract")
    check(identical(r$extra$status, "ok"), paste0("status ok (", r$extra$status, ")"))

    # determinism: only method_seed matters (global RNG state before the call is irrelevant)
    set.seed(1); invisible(runif(7))
    r2 <- m$f(d$X, d$y, mseed)
    check(identical(r$selected, r2$selected) && identical(r$extra$lambda.min, r2$extra$lambda.min),
          "same method_seed -> identical result, whatever the RNG state before the call")

    # fidelity: the adapter IS the authors' default call
    set.seed(mseed)
    if (mn == "lasso_cv") {
      cv <- suppressWarnings(glmnet::cv.glmnet(d$X, d$y))
      nz <- function(s) { v <- unlist(predict(cv, s = s, type = "nonzero"), use.names = FALSE)
                          if (is.null(v)) integer(0) else sort(as.integer(v)) }
      check(identical(r$selected, nz("lambda.1se")) && identical(r$extra$lambda.1se, cv$lambda.1se),
            "equals set.seed(s); cv.glmnet(X, y); predict(s='lambda.1se', type='nonzero')")
      check(identical(r$extra$selected_lambda_min, nz("lambda.min")) &&
              identical(r$extra$lambda.min, cv$lambda.min),
            "lambda.min alternative equals predict(s='lambda.min', type='nonzero')")
      rm_ <- m$f(d$X, d$y, mseed, ctrl = list(lambda_rule = "lambda.min"))
      check(identical(rm_$selected, r$extra$selected_lambda_min) && rm_$settings$lambda_rule$tag == "OURS",
            "ctrl$lambda_rule = 'lambda.min' switches the primary set")
    } else {
      cv <- suppressWarnings(ncvreg::cv.ncvreg(d$X, d$y, penalty = "SCAD"))
      v <- sort(unname(as.integer(predict(cv, type = "vars"))))
      check(identical(r$selected, v) && identical(r$extra$lambda.min, cv$lambda.min),
            "equals set.seed(s); cv.ncvreg(X, y, penalty='SCAD'); predict(type='vars')")
      check(cv$fit$gamma == 3.7 && r$settings$gamma$value == 3.7 && cv$fit$penalty == "SCAD",
            "SCAD fitted with gamma = 3.7")
    }

    tp <- length(intersect(r$selected, d$support)); fp <- length(setdiff(r$selected, d$support))
    row <- data.frame(case = cn, method = mn, n = n, p = p, s0 = length(d$support),
                      nsel = length(r$selected), TP = tp, FP = fp, FN = length(d$support) - tp,
                      exact = identical(r$selected, as.integer(d$support)),
                      lambda = signif(if (mn == "lasso_cv") r$extra$lambda.1se else r$extra$lambda.min, 4),
                      sec = round(r$runtime_sec, 2), n_warn = length(r$extra$warnings),
                      note = "", stringsAsFactors = FALSE)
    if (mn == "lasso_cv") {
      sm <- r$extra$selected_lambda_min
      row$note <- sprintf("at lambda.min: nsel=%d TP=%d FP=%d", length(sm),
                          length(intersect(sm, d$support)), length(setdiff(sm, d$support)))
    } else {
      row$note <- sprintf("convex.min=%s cv_min_nonconvex=%s max_iter=%s", r$extra$convex.min,
                          r$extra$cv_min_in_nonconvex_region, r$extra$max_iter_reached)
    }
    if (length(r$extra$warnings)) cat("  warnings:", paste(unique(r$extra$warnings), collapse = " | "), "\n")
    rows[[length(rows) + 1L]] <- row
  }
}

# sanity on the high-SNR cases. The gate only catches what would indicate a BUG:
# at least half of the true signals are selected and the set is not degenerate
# (fewer than n/2 variables). Exact TP / FP / FN are REPORTED, not gated: section 2
# already proves the adapter output is identical to the authors' own call, so the
# counts are the method's statistical behaviour. Observed on 2026-11-25: the
# CV-tuned lasso keeps many false positives when strong signals are correlated
# (rho = 0.6), and at lambda.1se it missed 2 of 10 signals at n=1000, p=5000, SNR=2.
cat("\n== 3. sanity on the high-SNR cases ==\n")
tab <- do.call(rbind, rows)
easy <- tab[grepl("SNR=(2|3|6)$", tab$case), ]
for (i in seq_len(nrow(easy)))
  check(easy$TP[i] >= ceiling(easy$s0[i] / 2) && easy$nsel[i] < easy$n[i] / 2,
        sprintf("%s | %s: TP=%d/%d (>= half), FP=%d, |selected|=%d < n/2", easy$case[i],
                easy$method[i], easy$TP[i], easy$s0[i], easy$FP[i], easy$nsel[i]))

# ---- 4. never-error: bad or awkward inputs return a well-formed failure ------
cat("\n== 4. never-error on bad or awkward inputs ==\n")
d <- cases[[1]]; X <- d$X[1:60, 1:40]; y <- d$y[1:60]
Xna <- X; Xna[3, 4] <- NA
Xpi <- X; Xpi[3, 4] <- Inf
Xmi <- X; Xmi[3, 4] <- -Inf
ypi <- y; ypi[5] <- Inf
ymi <- y; ymi[5] <- -Inf
Xzv <- X; Xzv[, 7] <- 1
bad <- list(
  "NA in X"             = list(X = Xna, y = y, seed = 11, fail = TRUE),
  "Inf in X"            = list(X = Xpi, y = y, seed = 11, fail = TRUE),
  "-Inf in X"           = list(X = Xmi, y = y, seed = 11, fail = TRUE),
  "Inf in y"            = list(X = X, y = ypi, seed = 11, fail = TRUE),
  "-Inf in y"           = list(X = X, y = ymi, seed = 11, fail = TRUE),
  "NA in y"             = list(X = X, y = replace(y, 5, NA), seed = 11, fail = TRUE),
  "y wrong length"      = list(X = X, y = y[-1], seed = 11, fail = TRUE),
  "y constant"          = list(X = X, y = rep(2, 60), seed = 11, fail = TRUE),
  "X is a data.frame"   = list(X = as.data.frame(X), y = y, seed = 11, fail = TRUE),
  "X is character"      = list(X = matrix("a", 60, 40), y = y, seed = 11, fail = TRUE),
  "seed NA"             = list(X = X, y = y, seed = NA, fail = TRUE),
  "seed NULL"           = list(X = X, y = y, seed = NULL, fail = TRUE),
  "seed not a number"   = list(X = X, y = y, seed = "abc", fail = TRUE),
  "seed beyond integer" = list(X = X, y = y, seed = 1e12, fail = TRUE),
  "one column"          = list(X = X[, 1, drop = FALSE], y = y, seed = 11, fail = NA),
  "zero-variance column"= list(X = Xzv, y = y, seed = 11, fail = FALSE),
  "tiny n=12 p=40"      = list(X = X[1:12, ], y = y[1:12], seed = 11, fail = NA)
)
for (bn in names(bad)) for (mn in names(methods)) {
  b <- bad[[bn]]
  r <- tryCatch(methods[[mn]]$f(b$X, b$y, b$seed), error = function(e) e)
  ok <- !inherits(r, "error") &&
    identical(names(r), c("selected", "pip", "runtime_sec", "software", "settings", "extra")) &&
    is.integer(r$selected) && is.character(r$extra$status) && is.finite(r$runtime_sec)
  failed <- ok && grepl("^failed: ", r$extra$status)
  if (ok && failed) ok <- length(r$selected) == 0L
  if (ok && !is.na(b$fail)) ok <- identical(failed, b$fail)
  if (ok && bn == "zero-variance column") ok <- !(7L %in% r$selected)
  check(ok, sprintf("%-22s %-8s -> %s", bn, mn, if (inherits(r, "error")) paste("R ERROR:", conditionMessage(r))
                                                 else r$extra$status))
}
r <- tryCatch(fit_lasso_cv(X, y, 11, ctrl = list(lambda_rule = "bogus")), error = function(e) e)
check(!inherits(r, "error") && grepl("^failed: ", r$extra$status), "lasso bogus ctrl$lambda_rule -> failed, no error")
r <- tryCatch(fit_scad(X, y, 11, ctrl = list(nfolds = 5)), error = function(e) e)
check(!inherits(r, "error") && r$extra$status == "ok" && r$settings$nfolds$tag == "OURS",
      "scad ctrl$nfolds override runs and is tagged OURS")

# ---- 4b. recorded settings are the effective ones ------------------------------
cat("\n== 4b. recorded settings are the effective ones ==\n")
r10 <- fit_lasso_cv(X, y, 11)
check(isTRUE(r10$settings$grouped$value) && identical(r10$settings$tuning_protocol$value,
        "10-fold CV on (X, y); no external validation set"),
      "lasso n=60: grouped = TRUE recorded, protocol string says 10-fold")
r5 <- fit_lasso_cv(X, y, 11, ctrl = list(nfolds = 5))
check(r5$extra$status == "ok" && r5$settings$nfolds$tag == "OURS" &&
        grepl("^5-fold CV", r5$settings$tuning_protocol$value),
      "lasso ctrl$nfolds = 5: tagged OURS and protocol string says 5-fold")
rt <- fit_lasso_cv(X[1:12, ], y[1:12], 11)
check(rt$extra$status == "ok" && identical(rt$settings$grouped$value, FALSE) &&
        any(grepl("grouped=FALSE enforced", rt$extra$warnings)),
      "lasso n=12, 10 folds: effective grouped = FALSE recorded (glmnet's own warning captured)")
dep <- c("lambda_rule", "tuning_protocol", "intercept_vs_S2", "path_stopping_vs_S2")
check(all(dep %in% names(r10$settings)) &&
        all(vapply(r10$settings[dep], function(z) z$tag, "") == "OURS") &&
        r10$settings$same_as_S2$tag == "author",
      "lasso: the four departures from the S2 paper are recorded as OURS (CV, 1-SE rule, intercept, path stopping)")
check(r10$settings$fdev$value == 1e-05 && r10$settings$devmax$value == 0.999 &&
        r10$settings$thresh$value == 1e-07 && r10$settings$maxit$value == 1e+05,
      "lasso: fdev, devmax, thresh, maxit recorded at factory values")

# isolation from ambient glmnet.control(): result unchanged, caller's controls restored
amb <- glmnet::glmnet.control(fdev = 0, thresh = 1e-4, devmax = 0.5)
ra <- tryCatch(fit_lasso_cv(X, y, 11), error = function(e) e)
after <- glmnet::glmnet.control()
glmnet::glmnet.control(factory = TRUE)
check(!inherits(ra, "error") && identical(ra$selected, r10$selected) &&
        identical(ra$extra$lambda.1se, r10$extra$lambda.1se) &&
        identical(ra$extra$lambda.min, r10$extra$lambda.min) &&
        identical(ra$extra$n_lambda_fit, r10$extra$n_lambda_fit) &&
        isTRUE(ra$extra$ambient_glmnet_control_differed) && ra$settings$fdev$value == 1e-05,
      "lasso under ambient glmnet.control(fdev=0, thresh=1e-4, devmax=0.5): identical fit, factory values recorded")
check(after$fdev == 0 && after$thresh == 1e-4 && after$devmax == 0.5,
      "lasso: the caller's glmnet.control() is restored after the call")
glmnet::glmnet.control(fdev = 0)
rf <- tryCatch(fit_lasso_cv(X, y[-1], 11), error = function(e) e)       # failure path
after_f <- glmnet::glmnet.control(); glmnet::glmnet.control(factory = TRUE)
check(!inherits(rf, "error") && grepl("^failed: ", rf$extra$status) && after_f$fdev == 0,
      "lasso: caller's glmnet.control() intact after a failed call")
check(isFALSE(r10$extra$ambient_glmnet_control_differed), "lasso: ambient flag FALSE in a factory session")

# SCAD: lambda.min ratio and dfmax follow ncvreg's effective p (constant columns dropped)
rz <- fit_scad(Xzv, y, 11)                         # 40 columns, one constant
check(rz$extra$status == "ok" && rz$extra$p_eff == 39L && rz$settings$dfmax$value == 40L &&
        rz$settings$lambda.min$value == 0.001,
      "scad n=60, p=40 with one constant column: p_eff = 39, dfmax = 40, lambda.min = 0.001")
Xb <- cbind(X[1:40, ], 1)                          # n = 40, 41 columns, 40 non-constant: n > p_eff is FALSE
rb <- fit_scad(Xb, y[1:40], 11)
set.seed(11); cvb <- suppressWarnings(ncvreg::cv.ncvreg(Xb, y[1:40], penalty = "SCAD"))
check(rb$extra$status == "ok" && rb$extra$p_eff == 40L && rb$settings$lambda.min$value == 0.05 &&
        isTRUE(all.equal(min(cvb$fit$lambda) / max(cvb$fit$lambda), 0.05)),
      "scad n=40, p_eff=40: recorded lambda.min = 0.05 equals the fitted path ratio")
Xc <- cbind(X[1:40, 1:39], 1)                      # n = 40, 40 columns, 39 non-constant: n > p_eff is TRUE
rc <- fit_scad(Xc, y[1:40], 11)
set.seed(11); cvc <- suppressWarnings(ncvreg::cv.ncvreg(Xc, y[1:40], penalty = "SCAD"))
check(rc$extra$status == "ok" && rc$extra$p_eff == 39L && rc$settings$lambda.min$value == 0.001 &&
        isTRUE(all.equal(min(cvc$fit$lambda) / max(cvc$fit$lambda), 0.001)),
      "scad n=40, p=40 with one constant column: recorded lambda.min = 0.001 equals the fitted path ratio (p_eff, not p)")

# ---- 5. summary ---------------------------------------------------------------
cat("\n== 5. selected sets and timing (lasso primary = lambda.1se, SCAD = lambda.min) ==\n")
print(tab, row.names = FALSE, right = FALSE)
cat(sprintf("\nRESULT: %s (%d failed check%s)\n", if (n_fail == 0L) "ALL CHECKS PASSED" else "FAILURES",
            n_fail, if (n_fail == 1L) "" else "s"))
quit(save = "no", status = if (n_fail == 0L) 0L else 1L)
