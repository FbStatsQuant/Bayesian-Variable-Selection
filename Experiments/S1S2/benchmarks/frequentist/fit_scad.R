# =============================================================================
# PROVENANCE  fit_scad.R  (S1/S2 frequentist benchmark: SCAD + 10-fold CV)
# -----------------------------------------------------------------------------
# METHOD PAPERS (read before writing; section numbers are where each setting is)
#   [FL01]  Fan & Li (2001) "Variable selection via nonconcave penalized
#           likelihood and its oracle properties", JASA 96(456):1348-1360,
#           DOI 10.1198/016214501753382273 (open copy from the first author's
#           Princeton page).
#           Sec 2.1 eq (2.7): SCAD penalty, a > 2; Bayes-risk argument gives
#                    a ~ 3.7, which "works similarly to that chosen by GCV".
#           Sec 4.2: tuning of (lambda, a) by fivefold CV or GCV (results shown
#                    with GCV); their own fits used local quadratic
#                    approximation in MATLAB.
#   [BH11]  Breheny & Huang (2011) "Coordinate descent algorithms for nonconvex
#           penalized regression, with applications to biological feature
#           selection", Ann. Appl. Stat. 5(1):232-253, DOI 10.1214/10-AOAS388.
#           Sec 2: x standardized, y centred, intercept restored afterwards.
#           Sec 2.2 eq (2.5)-(2.6): SCAD and its coordinate-descent update.
#           Sec 2.4: path of 100 lambda values equally spaced on the log scale.
#           Sec 4.2: local convexity diagnostic (lambda*).
#           Sec 4.3: hybrid choice of gamma (BIC + convexity diagnostic, iterated
#                    by hand), then CV for lambda.
#           Sec 5.2: "Tenfold cross-validation was used to choose lambda."
# SOFTWARE (authors' own; nothing reimplemented)
#   ncvreg 3.16.0 (CRAN, published 2025-11-06; maintainer P. Breheny), installed
#   in /home/fb31/Bayesian-Variable-Selection/_local/engineering/Rlib.
#   Docs read: ?ncvreg, ?cv.ncvreg, vignette "Getting started with ncvreg"
#   (doc/ncvreg.rmd), and the R source of cv.ncvreg, coef.cv.ncvreg,
#   predict.ncvreg, assign_fold, convexMin.
# HOW THE S1/S2 SOURCE PAPERS RAN SCAD
#   Neither ran it.  Hastie, Tibshirani & Tibshirani (2020), DOI
#   10.1214/19-STS733, compare lasso / relaxed lasso / forward stepwise / best
#   subset only; Griffin, Latuszynski & Steel (2021), DOI 10.1093/biomet/asaa055,
#   Sec 4.1, run no frequentist comparator.  Protocol = the package authors'.
#
# THE CALL (everything not listed is left at the ncvreg default)
#   set.seed(method_seed)
#   cvfit <- ncvreg::cv.ncvreg(X, y, penalty = "SCAD")
#   selected <- which(coef(cvfit)[-1] != 0)          # coef() is at lambda.min
#
# SETTINGS  (value | source | tag)
#   family        "gaussian"                    | ncvreg default             | author
#   penalty       "SCAD"                        | the method; [FL01] eq (2.7), [BH11] eq (2.5) | author
#   gamma         3.7                           | ncvreg default for SCAD; [FL01] Sec 2.1,
#                                                 and Sec 4.3 Table 1 (SCAD2: a fixed at 3.7) | author (see OURS-1)
#   alpha         1 (no ridge part)             | ncvreg default             | author
#   nlambda       100                           | ncvreg default; [BH11] 2.4 | author
#   lambda.min    0.001 if n > p_eff else 0.05  | ncvreg default (fraction of lambda.max) | author
#   eps, max.iter 1e-4, 10000                   | ncvreg defaults            | author
#   dfmax, penalty.factor  p_eff + 1, all 1     | ncvreg defaults            | author
#     (p_eff = number of non-constant columns: ncvreg evaluates both defaults
#      after dropping constant columns; recorded from length(fit$penalty.factor))
#   standardize / intercept  always (not options) | ?ncvreg; [BH11] Sec 2   | author
#   nfolds        10                            | cv.ncvreg default; [BH11] 5.2 | author
#   folds         ncvreg:::assign_fold -> sample(1:n %% nfolds) | cv.ncvreg source | author
#   CV loss       deviance (= squared error)    | ?cv.ncvreg                 | author
#   lambda rule   lambda.min (minimum CV error) | default of coef/predict.cv.ncvreg; vignette | author
#   gamma tuning  none, fixed at 3.7            | see below                  | OURS-1
#   seed          set.seed(method_seed)         | INTERFACE.md "Seeds"       | OURS-2
#   selection     {j : coef_j != 0}             | INTERFACE.md "Selection rule" | OURS-3
#
# OURS FLAGS (reasons)
#   OURS-1  gamma is NOT tuned; it is fixed at 3.7.  3.7 is the ncvreg default
#           for SCAD and the value [FL01] recommend (Sec 2.1) and test as a
#           fixed choice (Sec 4.3, Table 1, "SCAD2": a = 3.7, against "SCAD1"
#           with a chosen by GCV; DOI 10.1198/016214501753382273).
#           Not done: [FL01] Sec 4.2's 2-d (lambda, a) search, and [BH11]
#           Sec 4.3's hybrid choice (select lambda by AIC/BIC, compare it with
#           the convexity boundary lambda*, raise or lower gamma, iterate "a few
#           times", then CV for lambda).  ncvreg automates neither, and writing
#           our own gamma search would be a reimplementation.
#           As [BH11] Sec 4.2 ask ("practitioners ... should know which region
#           their solution resides in"), the Sec 4.2 diagnostic is reported for
#           the CV-chosen lambda: extra$convex.min and
#           extra$cv_min_in_nonconvex_region.  It is information only: it is NOT
#           the [BH11] Sec 4.3 criterion (that one uses the AIC/BIC-selected
#           lambda, which we do not compute), and no action is taken on it.
#   OURS-2  Fold randomness comes only from set.seed(method_seed) (Mersenne-
#           Twister / Inversion / Rejection), called immediately before the fit
#           (cv.ncvreg 3.16.0 has no seed argument).
#   OURS-3  Selected set = nonzero coefficients at lambda.min.
#   Differences from [FL01] that come with using the authors' current
#   software: 10-fold CV instead of fivefold CV / GCV, coordinate descent
#   instead of local quadratic approximation.
#   Note: ncvreg has no one-standard-error rule, so SCAD is at lambda.min while
#   the lasso adapter's primary rule is lambda.1se (each at its own software's
#   default); the lasso adapter also returns its lambda.min selection.
#
# ctrl (optional; every use is recorded in `settings` with tag "OURS")
#   ctrl$nfolds   integer >= 2 (default: cv.ncvreg's own default, 10)
#   ctrl$rlib     R library path (default: the S1S2 Rlib above)
# =============================================================================

fit_scad <- function(X, y, method_seed, ctrl = list()) {
  t_start <- proc.time()[["elapsed"]]
  out <- list(
    selected    = integer(0),
    pip         = NULL,
    runtime_sec = NA_real_,
    software    = list(name = "ncvreg", version = NA_character_),
    settings    = list(),
    extra       = list(status = "failed: not run")
  )
  warns <- character(0)
  t_fit0 <- NA_real_

  res <- tryCatch(withCallingHandlers({
    # ---- library --------------------------------------------------------
    rlib <- if (is.null(ctrl$rlib))
      "/home/fb31/Bayesian-Variable-Selection/_local/engineering/Rlib" else ctrl$rlib
    if (dir.exists(rlib) && !(rlib %in% .libPaths())) .libPaths(c(rlib, .libPaths()))
    if (!requireNamespace("ncvreg", quietly = TRUE)) stop("package ncvreg not installed")
    out$software <- list(name = "ncvreg",
                         version = as.character(utils::packageVersion("ncvreg")),
                         R = R.version.string)

    # ---- input checks (method-level failure, never an R error) -----------
    if (!is.matrix(X) || !is.numeric(X)) stop("X must be a numeric matrix")
    y <- as.numeric(y)
    n <- nrow(X); p <- ncol(X)
    if (length(y) != n) stop("length(y) != nrow(X)")
    if (p < 1L) stop("X has no columns")
    if (any(!is.finite(X)) || any(!is.finite(y))) stop("non-finite values in X or y")
    if (stats::var(y) == 0) stop("y is constant")
    if (length(method_seed) != 1L || !is.finite(method_seed) ||
        method_seed != floor(method_seed) || abs(method_seed) > .Machine$integer.max)
      stop("method_seed must be one whole number within integer range")

    nfolds_default <- eval(formals(ncvreg::cv.ncvreg)$nfolds)          # 10
    nfolds <- if (is.null(ctrl$nfolds)) nfolds_default else as.integer(ctrl$nfolds)

    # ---- the authors' fit: cv.ncvreg at its defaults, SCAD penalty --------
    set.seed(as.integer(method_seed), kind = "Mersenne-Twister",
             normal.kind = "Inversion", sample.kind = "Rejection")
    t_fit0 <- proc.time()[["elapsed"]]
    cvfit <- if (is.null(ctrl$nfolds)) ncvreg::cv.ncvreg(X, y, penalty = "SCAD")
             else ncvreg::cv.ncvreg(X, y, penalty = "SCAD", nfolds = nfolds)
    b <- stats::coef(cvfit)                      # at lambda.min (which = cvfit$min)
    t_fit1 <- proc.time()[["elapsed"]]

    if (length(b) != p + 1L) stop("coefficient length != p + 1")
    sel <- sort(unname(which(b[-1] != 0)))

    # ---- record what was actually used ------------------------------------
    fit <- cvfit$fit
    fm  <- formals(ncvreg::ncvreg)
    p_eff <- length(fit$penalty.factor)            # columns ncvreg kept (constant columns dropped)
    tag <- function(value, tag, source) list(value = value, tag = tag, source = source)
    out$settings <- list(
      family         = tag(fit$family, "author", "ncvreg default"),
      penalty        = tag(fit$penalty, "author",
                           "the method: Fan & Li 2001 eq (2.7); Breheny & Huang 2011 eq (2.5)"),
      gamma          = tag(fit$gamma, "author",
                           "ncvreg default for SCAD; Fan & Li 2001 Sec 2.1 and Sec 4.3 Table 1 (SCAD2: a fixed at 3.7), doi 10.1198/016214501753382273"),
      alpha          = tag(fit$alpha, "author", "ncvreg default (no L2 penalty)"),
      nlambda        = tag(eval(fm$nlambda), "author",
                           "ncvreg default; Breheny & Huang 2011 Sec 2.4"),
      lambda.min     = tag(if (n > p_eff) 0.001 else 0.05, "author",
                           "ncvreg default ifelse(n > p, 0.001, 0.05) with p = non-constant columns; fraction of lambda.max"),
      eps            = tag(eval(fm$eps), "author", "ncvreg default"),
      max.iter       = tag(eval(fm$max.iter), "author", "ncvreg default (total over the path)"),
      dfmax          = tag(p_eff + 1L, "author", "ncvreg default p + 1 with p = non-constant columns (no bound)"),
      standardize    = tag(TRUE, "author", "?ncvreg: always standardizes; Breheny & Huang 2011 Sec 2"),
      intercept      = tag(TRUE, "author", "?ncvreg: always fits an intercept; Breheny & Huang 2011 Sec 2"),
      nfolds         = tag(nfolds, if (is.null(ctrl$nfolds)) "author" else "OURS",
                           if (is.null(ctrl$nfolds)) "cv.ncvreg default; Breheny & Huang 2011 Sec 5.2"
                           else "ctrl$nfolds override"),
      folds          = tag("ncvreg:::assign_fold: sample(1:n %% nfolds) inside cv.ncvreg", "author",
                           "cv.ncvreg source"),
      cv_loss        = tag("deviance (squared error)", "author", "?cv.ncvreg Details"),
      lambda_rule    = tag("lambda.min", "author",
                           "default of coef/predict.cv.ncvreg; ncvreg vignette (ncvreg has no 1se rule)"),
      gamma_tuning   = tag("none (fixed at package default)", "OURS",
                           "OURS-1: fixed gamma = 3.7 as Fan & Li 2001 Sec 4.3 Table 1 (SCAD2); Breheny & Huang 2011 Sec 4.3 hybrid gamma choice (from the AIC/BIC-selected lambda) is manual, not automated in ncvreg"),
      seed           = tag(as.integer(method_seed), "OURS",
                           "OURS-2: INTERFACE.md Seeds; set.seed(method_seed) before cv.ncvreg"),
      selection      = tag("nonzero coefficients at lambda.min", "OURS",
                           "OURS-3: INTERFACE.md Selection rule")
    )

    cmin <- fit$convex.min                         # NULL = locally convex on the whole path
    out$selected <- as.integer(sel)
    out$runtime_sec <- t_fit1 - t_fit0
    out$extra <- list(
      status            = "ok",
      lambda_rule       = "lambda.min",
      lambda.min        = cvfit$lambda.min,
      index_min         = cvfit$min,
      n_lambda_fit      = length(fit$lambda),       # path length on the full data
      n_lambda_cv       = length(cvfit$lambda),     # values with a finite CV error in every fold
      lambda_max        = max(fit$lambda),
      lambda_path_min   = min(fit$lambda),
      lambda_min_at_path_end = isTRUE(cvfit$min == length(cvfit$lambda)),
      cve_min           = cvfit$cve[cvfit$min],
      cvse_min          = cvfit$cvse[cvfit$min],
      n_selected        = length(sel),
      intercept         = unname(b[1]),
      convex.min        = if (is.null(cmin)) NA_integer_ else as.integer(cmin),
      lambda_convex_min = if (is.null(cmin)) NA_real_ else fit$lambda[cmin],
      cv_min_in_nonconvex_region = if (is.null(cmin)) FALSE else isTRUE(cvfit$min > cmin),
      total_iter        = sum(fit$iter),
      max_iter_reached  = isTRUE(sum(fit$iter) >= eval(fm$max.iter)),
      n = n, p = p, p_eff = p_eff
    )
    invisible(TRUE)
  }, warning = function(w) {
    warns <<- c(warns, conditionMessage(w))
    invokeRestart("muffleWarning")
  }), error = function(e) e)

  if (inherits(res, "error")) {
    out$selected <- integer(0)
    out$extra <- list(status = paste0("failed: ", conditionMessage(res)))
    t_end <- proc.time()[["elapsed"]]
    out$runtime_sec <- if (is.finite(t_fit0)) t_end - t_fit0 else t_end - t_start
  }
  out$extra$warnings <- warns
  out["pip"] <- list(NULL)   # frequentist: no PIPs (keep the element, value NULL)
  out[c("selected", "pip", "runtime_sec", "software", "settings", "extra")]
}
