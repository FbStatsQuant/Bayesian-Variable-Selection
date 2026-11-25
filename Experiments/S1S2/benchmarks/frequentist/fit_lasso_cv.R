# =============================================================================
# PROVENANCE  fit_lasso_cv.R  (S1/S2 frequentist benchmark: lasso + 10-fold CV)
# -----------------------------------------------------------------------------
# METHOD PAPERS (read before writing; section numbers are where each setting is)
#   [T96]   Tibshirani (1996) "Regression shrinkage and selection via the lasso",
#           JRSS-B 58(1):267-288, DOI 10.1111/j.2517-6161.1996.tb02080.x.
#           Sec 2.1: lasso definition; x_ij standardized; intercept = ybar.
#           Sec 4:   tuning by fivefold CV / GCV / risk estimate; picks the value
#                    with the LOWEST estimated prediction error.
#   [FHT10] Friedman, Hastie & Tibshirani (2010) "Regularization paths for
#           generalized linear models via coordinate descent", JSS 33(1):1-22,
#           DOI 10.18637/jss.v033.i01.
#           Sec 2 eq (1): objective, standardized x.  Sec 2.5: lambda path,
#           K = 100 values on the log scale.  Sec 2.6: predictors always
#           centred, intercept unpenalized.  Sec 6: K-fold CV (Fig 2 uses
#           ten-fold) and "we often use the one-standard-error rule".
# SOFTWARE (authors' own; nothing reimplemented)
#   glmnet 5.2 (CRAN, Date 2026-10-26; maintainer T. Hastie), installed in
#   /home/fb31/Bayesian-Variable-Selection/_local/engineering/Rlib.
#   Docs read: ?cv.glmnet, ?glmnet, ?predict.cv.glmnet, ?glmnet.control,
#   vignette "An Introduction to glmnet" (doc/glmnet.Rmd), NEWS.md (5.0-5.2:
#   "Non-Cox families unchanged and bit-identical" vs 4.1-10).
# HOW THE S1/S2 SOURCE PAPERS RAN THE LASSO (recorded; see OURS-2, OURS-3)
#   [HTT20] Hastie, Tibshirani & Tibshirani (2020), Statist. Sci. 35(4):579-592,
#           DOI 10.1214/19-STS733 (read as arXiv:1707.08692v2, Sec 3.1 "Tuning
#           of procedures") and their code github.com/ryantibs/best-subset
#           @796e8171 (sims/sim.hi5.R, bestsubset/R/lasso.R, R/sim.R):
#           glmnet.control(fdev=0); lasso(x, y, intercept=FALSE, nlam=100)
#           [nlam=50 in the "low" setting], standardize=TRUE; lambda chosen by
#           MINIMUM prediction error on an independent validation set of size n.
#   [GLS21] Griffin, Latuszynski & Steel (2021), Biometrika 108(1):53-69,
#           DOI 10.1093/biomet/asaa055 (read as arXiv:1708.05678v3, Sec 4.1):
#           no frequentist comparator was run (lasso appears only as an MCMC
#           starting point in the real-data supplement). Nothing to replicate.
#
# THE CALL (everything not listed is left at the glmnet default)
#   set.seed(method_seed); cvfit <- glmnet::cv.glmnet(x = X, y = y)
#   selected <- which(coef(cvfit, s = "lambda.1se")[-1] != 0)
#
# SETTINGS  (value | source | tag)
#   family            "gaussian"                | glmnet default            | author
#   alpha             1 (lasso)                 | glmnet default; [T96] 2.1 | author
#   nlambda           100                       | glmnet default; [FHT10] 2.5 | author
#   lambda.min.ratio  0.01 if n < p else 1e-4   | glmnet default            | author
#   standardize       TRUE (coef on orig. scale)| glmnet default; [FHT10] 2, [T96] 2.1 | author
#   intercept         TRUE (unpenalized)        | glmnet default; [FHT10] 2.6 | author
#   thresh, maxit     1e-7, 1e5                 | glmnet.control() factory  | author
#   fdev, devmax      1e-5, 0.999 (path stopping)| glmnet.control() factory | author
#   control isolation factory controls forced for the fit, caller's restored on exit | OURS-6
#   type.measure      "default" = MSE (gaussian)| cv.glmnet default         | author
#   nfolds            10                        | cv.glmnet default; [FHT10] Sec 6 Fig 2 | author
#   folds             sample(rep(seq(nfolds), length = N)) inside cv.glmnet | author
#   grouped           TRUE; cv.glmnet itself enforces FALSE when n/nfolds < 3;
#                     the effective value (n/nfolds >= 3) is recorded | cv.glmnet | author
#   alignment/relax   "lambda" / FALSE          | cv.glmnet defaults        | author
#   lambda rule       "lambda.1se"              | default `s` of coef/predict.cv.glmnet;
#                                                 [FHT10] Sec 6             | OURS-1
#   tuning protocol   nfolds-fold CV on (X, y) only | cv.glmnet default     | OURS-2
#   intercept vs S2   TRUE (S2 paper: FALSE)    | glmnet default            | OURS-3
#   path stop vs S2   factory fdev = 1e-5 (S2 paper: fdev = 0) | glmnet default | OURS-6
#   seed              set.seed(method_seed)     | INTERFACE.md "Seeds"      | OURS-4
#   selection         {j : coef_j != 0}         | INTERFACE.md "Selection rule" | OURS-5
#
# OURS FLAGS (reasons)
#   OURS-1  lambda.1se, not lambda.min.  Documented rationale: lambda.1se is
#           the default `s` of coef/predict on a cv.glmnet object, and it favours
#           parsimony when CV errors are close ([FHT10] Sec 6, DOI
#           10.18637/jss.v033.i01: the one-standard-error rule "errs on the side
#           of parsimony").  Using it as the rule for EXACT SUPPORT RECOVERY is
#           OURS; the authors give it as a model-choice rule under CV error.
#           [T96] Sec 4 and [HTT20] used the minimum-error rule, so the
#           lambda.min selection is ALSO returned (extra$selected_lambda_min)
#           from the same fit; ctrl$lambda_rule = "lambda.min" makes it primary.
#   OURS-2  [HTT20] tuned on an external validation set of size n.  The adapter
#           contract gives a method only (X, y); an extra n fresh observations
#           would hand the lasso data the other methods never see.  We use the
#           software authors' default, 10-fold CV.
#   OURS-3  [HTT20]'s scripts pass intercept = FALSE; we keep glmnet's default
#           intercept = TRUE as INTERFACE.md directs ("each adapter does
#           whatever its author does").
#   OURS-4  Fold randomness comes only from set.seed(method_seed) (Mersenne-
#           Twister / Inversion / Rejection), called immediately before the fit.
#   OURS-5  Selected set = nonzero coefficients at the chosen lambda.
#   OURS-6  Path stopping and control isolation.  [HTT20]'s scripts set
#           glmnet.control(fdev = 0) (no early stop of the path); we keep the
#           glmnet factory stopping rules (fdev = 1e-5, devmax = 0.999).  So that
#           no ambient glmnet.control() setting of the calling session can change
#           the fit, the adapter saves the caller's controls, applies
#           glmnet.control(factory = TRUE) for the fit, and restores the caller's
#           controls on exit.  thresh, maxit, fdev, devmax in effect are recorded.
#   DEPARTURES FROM THE S2 PAPER'S LASSO, all recorded as OURS in `settings`:
#     (a) nfolds-fold CV instead of a size-n validation set        (OURS-2)
#     (b) one-standard-error rule instead of minimum error          (OURS-1)
#     (c) intercept = TRUE instead of FALSE                         (OURS-3)
#     (d) factory path stopping instead of fdev = 0                 (OURS-6)
#   SAME AS THE S2 PAPER: standardize = TRUE, and 100 lambda values (their
#   "low" setting n=100, p=10 used 50; we use the glmnet default 100 throughout).
#   Not used: relaxed lasso (relax = TRUE), elastic net, adaptive weights, any
#   screening or refit.
#
# ctrl (optional; every use is recorded in `settings` with tag "OURS")
#   ctrl$lambda_rule  "lambda.1se" (default) | "lambda.min"
#   ctrl$nfolds       integer >= 3 (default: cv.glmnet's own default, 10)
#   ctrl$rlib         R library path (default: the S1S2 Rlib above)
# =============================================================================

fit_lasso_cv <- function(X, y, method_seed, ctrl = list()) {
  t_start <- proc.time()[["elapsed"]]
  out <- list(
    selected    = integer(0),
    pip         = NULL,
    runtime_sec = NA_real_,
    software    = list(name = "glmnet", version = NA_character_),
    settings    = list(),
    extra       = list(status = "failed: not run")
  )
  warns <- character(0)
  t_fit0 <- NA_real_
  gc_caller <- NULL   # the calling session's glmnet.control(), restored on exit (OURS-6)
  on.exit(if (!is.null(gc_caller))
            try(do.call(glmnet::glmnet.control, gc_caller), silent = TRUE), add = TRUE)

  res <- tryCatch(withCallingHandlers({
    # ---- library --------------------------------------------------------
    rlib <- if (is.null(ctrl$rlib))
      "/home/fb31/Bayesian-Variable-Selection/_local/engineering/Rlib" else ctrl$rlib
    if (dir.exists(rlib) && !(rlib %in% .libPaths())) .libPaths(c(rlib, .libPaths()))
    if (!requireNamespace("glmnet", quietly = TRUE)) stop("package glmnet not installed")
    out$software <- list(name = "glmnet",
                         version = as.character(utils::packageVersion("glmnet")),
                         R = R.version.string)

    # ---- input checks (method-level failure, never an R error) -----------
    if (!is.matrix(X) || !is.numeric(X)) stop("X must be a numeric matrix")
    y <- as.numeric(y)
    n <- nrow(X); p <- ncol(X)
    if (length(y) != n) stop("length(y) != nrow(X)")
    if (p < 2L) stop("glmnet needs at least 2 columns in X")
    if (any(!is.finite(X)) || any(!is.finite(y))) stop("non-finite values in X or y")
    if (length(method_seed) != 1L || !is.finite(method_seed) ||
        method_seed != floor(method_seed) || abs(method_seed) > .Machine$integer.max)
      stop("method_seed must be one whole number within integer range")

    rule <- if (is.null(ctrl$lambda_rule)) "lambda.1se" else as.character(ctrl$lambda_rule)
    if (!(rule %in% c("lambda.1se", "lambda.min")))
      stop("ctrl$lambda_rule must be 'lambda.1se' or 'lambda.min'")
    nfolds_default <- eval(formals(glmnet::cv.glmnet)$nfolds)          # 10
    nfolds <- if (is.null(ctrl$nfolds)) nfolds_default else as.integer(ctrl$nfolds)

    # ---- isolate from ambient glmnet.control(): factory controls for the fit
    gc_caller <- glmnet::glmnet.control()
    gc_factory <- glmnet::glmnet.control(factory = TRUE)
    ctrl_names <- c("fdev", "devmax", "eps", "mnlam", "thresh", "maxit", "dfmax", "pmax")
    ambient_differed <- !isTRUE(all.equal(gc_caller[ctrl_names], gc_factory[ctrl_names]))

    # ---- the authors' fit: cv.glmnet at its defaults ----------------------
    set.seed(as.integer(method_seed), kind = "Mersenne-Twister",
             normal.kind = "Inversion", sample.kind = "Rejection")
    t_fit0 <- proc.time()[["elapsed"]]
    cvfit <- if (is.null(ctrl$nfolds)) glmnet::cv.glmnet(x = X, y = y)
             else glmnet::cv.glmnet(x = X, y = y, nfolds = nfolds)
    b_1se <- as.numeric(as.matrix(stats::coef(cvfit, s = "lambda.1se")))[-1]
    b_min <- as.numeric(as.matrix(stats::coef(cvfit, s = "lambda.min")))[-1]
    t_fit1 <- proc.time()[["elapsed"]]

    if (length(b_1se) != p || length(b_min) != p) stop("coefficient length != p")
    sel_1se <- sort(which(b_1se != 0))
    sel_min <- sort(which(b_min != 0))

    # ---- record what was actually used ------------------------------------
    gf  <- cvfit$glmnet.fit
    gc  <- glmnet::glmnet.control()                  # in effect for the fit (= factory)
    grouped_eff <- (n / nfolds >= 3)                 # cv.glmnet enforces FALSE below 3 obs per fold
    tag <- function(value, tag, source) list(value = value, tag = tag, source = source)
    out$settings <- list(
      family           = tag("gaussian", "author", "glmnet default"),
      alpha            = tag(eval(formals(glmnet::glmnet)$alpha), "author",
                             "glmnet default (lasso); Tibshirani 1996 Sec 2.1"),
      nlambda          = tag(eval(formals(glmnet::glmnet)$nlambda), "author",
                             "glmnet default; FHT 2010 Sec 2.5 (K = 100)"),
      lambda.min.ratio = tag(if (n < p) 0.01 else 1e-04, "author",
                             "glmnet default ifelse(nobs < nvars, 0.01, 1e-04)"),
      standardize      = tag(eval(formals(glmnet::glmnet)$standardize), "author",
                             "glmnet default; FHT 2010 Sec 2; Tibshirani 1996 Sec 2.1"),
      intercept        = tag(eval(formals(glmnet::glmnet)$intercept), "author",
                             "glmnet default; FHT 2010 Sec 2.6 (S2 paper scripts used FALSE: OURS-3)"),
      thresh           = tag(gc$thresh, "author", "glmnet.control() value in effect (factory 1e-07)"),
      maxit            = tag(gc$maxit,  "author", "glmnet.control() value in effect (factory 1e+05)"),
      fdev             = tag(gc$fdev,   "author",
                             "glmnet.control() value in effect (factory 1e-05): path stops when the fractional deviance change is below it"),
      devmax           = tag(gc$devmax, "author",
                             "glmnet.control() value in effect (factory 0.999): path stops at this fraction of null deviance explained"),
      control_isolation = tag("caller's glmnet.control() saved, glmnet.control(factory = TRUE) applied for the fit, caller's restored on exit",
                             "OURS", "OURS-6: the fit must not depend on ambient session controls"),
      type.measure     = tag(unname(names(cvfit$name)), "author",
                             "cv.glmnet default ('default' = mse for gaussian)"),
      nfolds           = tag(nfolds, if (is.null(ctrl$nfolds)) "author" else "OURS",
                             if (is.null(ctrl$nfolds)) "cv.glmnet default; FHT 2010 Sec 6 Fig 2"
                             else "ctrl$nfolds override"),
      folds            = tag("sample(rep(seq(nfolds), length = N)) inside cv.glmnet", "author",
                             "cv.glmnet source"),
      grouped          = tag(grouped_eff, "author",
                             "cv.glmnet default TRUE; cv.glmnet itself enforces FALSE when n/nfolds < 3 (effective value recorded)"),
      alignment        = tag("lambda", "author", "cv.glmnet default"),
      relax            = tag(FALSE, "author", "cv.glmnet default"),
      lambda_rule      = tag(rule, "OURS",
                             if (rule == "lambda.1se")
                               "OURS-1: default s of coef/predict.cv.glmnet; favours parsimony when CV errors are close (FHT 2010 Sec 6, doi 10.18637/jss.v033.i01); its use for exact support recovery is OURS; S2 paper used minimum validation error"
                             else "OURS-1: ctrl override; minimum-CV-error rule (Tibshirani 1996 Sec 4)"),
      tuning_protocol  = tag(sprintf("%d-fold CV on (X, y); no external validation set", nfolds), "OURS",
                             "OURS-2: departure from S2 paper (Hastie et al. 2020 Sec 3.1: validation set of size n)"),
      intercept_vs_S2  = tag("intercept = TRUE (glmnet default); S2 paper scripts: intercept = FALSE", "OURS",
                             "OURS-3: departure from S2 paper (best-subset@796e8171 sims/sim.*.R)"),
      path_stopping_vs_S2 = tag(sprintf("factory stopping fdev = %g, devmax = %g; S2 paper scripts: glmnet.control(fdev = 0)",
                                        gc$fdev, gc$devmax), "OURS",
                             "OURS-6: departure from S2 paper (best-subset@796e8171 sims/sim.*.R)"),
      same_as_S2       = tag("standardize = TRUE and nlambda = 100 in both (S2 'low' setting n=100, p=10 used 50)", "author",
                             "glmnet defaults; best-subset@796e8171 bestsubset/R/lasso.R and sims/sim.*.R"),
      seed             = tag(as.integer(method_seed), "OURS",
                             "OURS-4: INTERFACE.md Seeds; set.seed(method_seed) before cv.glmnet"),
      selection        = tag("nonzero coefficients at lambda_rule", "OURS",
                             "OURS-5: INTERFACE.md Selection rule")
    )

    i_min <- unname(cvfit$index[1, 1]); i_1se <- unname(cvfit$index[2, 1])
    out$selected <- as.integer(if (rule == "lambda.1se") sel_1se else sel_min)
    out$runtime_sec <- t_fit1 - t_fit0
    out$extra <- list(
      status               = "ok",
      lambda_rule          = rule,
      lambda.min           = cvfit$lambda.min,
      lambda.1se           = cvfit$lambda.1se,
      index_min            = i_min,
      index_1se            = i_1se,
      n_lambda_fit         = length(cvfit$lambda),
      lambda_max           = max(cvfit$lambda),
      lambda_path_min      = min(cvfit$lambda),
      lambda_min_at_path_end = isTRUE(i_min == length(cvfit$lambda)),
      cvm_min              = cvfit$cvm[i_min],
      cvm_1se              = cvfit$cvm[i_1se],
      cvsd_min             = cvfit$cvsd[i_min],
      selected_lambda_1se  = as.integer(sel_1se),
      selected_lambda_min  = as.integer(sel_min),
      n_selected_lambda_1se = length(sel_1se),
      n_selected_lambda_min = length(sel_min),
      intercept_at_rule    = as.numeric(as.matrix(stats::coef(cvfit, s = rule)))[1],
      jerr                 = gf$jerr,
      grouped_effective    = grouped_eff,
      ambient_glmnet_control_differed = ambient_differed,
      n = n, p = p
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
