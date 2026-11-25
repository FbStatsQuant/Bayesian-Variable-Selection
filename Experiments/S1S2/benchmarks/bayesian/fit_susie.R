# =============================================================================
# PROVENANCE  fit_susie.R  (S1/S2 Bayesian benchmark: SuSiE, Sum of Single
#             Effects regression fitted by IBSS)
# -----------------------------------------------------------------------------
# METHOD PAPER
#   [WSCS20] Wang, Sarkar, Carbonetto & Stephens (2020) "A simple new approach
#            to variable selection in regression, with application to genetic
#            fine mapping", JRSS-B 82(5):1273-1300, DOI 10.1111/rssb.12388
#            (citation("susieR") gives the preprint DOI 10.1101/501114).
#            Page numbers below are those of the copy on Owls (Core_bibliography
#            /29_2020_Wang_et_al...pdf, paged 1-28).
#            Sec 3.3 p.12 "Choice of L": "key inferences are often robust to
#              overstating L; ... the simulated number of effects was between 1
#              and 5, whereas we still obtain good results with L = 10".
#            Sec 4 p.13: first scenario S in {1,...,5} effects, second
#              scenario S = 10 effects.
#            Sec 4.2 p.16: "For SuSiE, we set L = 10 for all the data sets
#              that were generated in the first simulation scenario, and L = 20
#              for the second scenario."  (Their displayed results fixed the
#              prior variance at 0.1 var(y) and estimated sigma^2; they report
#              that estimating both gave similar performance.)
#            Sec 3.2.1 p.12, eq. (3.12): PIP_j = 1 - prod_{l: sigma0l^2 > 0}
#              (1 - alpha_lj).  Sec 3.2.2 p.12: credible sets.
# SOFTWARE (authors' own; nothing reimplemented)
#   susieR 0.14.2 (CRAN; maintainer P. Carbonetto), installed in
#   /home/fb31/Bayesian-Variable-Selection/_local/engineering/Rlib.
#   Read: ?susie, ?susie_get_pip, vignettes "mwe" (minimal working example,
#   susie(X, y, L = 10)) and "finemapping" (L = 10; "no harm to over-estimate L").
#   NOTE: this is the CRAN release 0.14.2, i.e. the [WSCS20] algorithm.  It is
#   NOT "SuSiE 2.0" (McCreight et al. 2025), which CRAN did not deliver.
#
# THE CALL (everything not listed is left at the susie() default)
#   X <- scale(X); y <- scale(y, scale = FALSE)          # PRE
#   set.seed(method_seed)
#   fit <- susieR::susie(X, y, L = 20)
#   pip <- fit$pip
#
# SETTINGS  (value | source | tag)
#   L                          20, every setting  | [WSCS20] Sec 4.2 p.16 (their 10-effect
#                                                   scenario); susie() default min(10, p) | OURS-1
#   scaled_prior_variance      0.2 (initial value)| susie() default                 | author
#   estimate_prior_variance    TRUE               | susie() default                 | author
#   estimate_prior_method      "optim"            | susie() default                 | author
#   check_null_threshold       0                  | susie() default                 | author
#   residual_variance          NULL -> var(y) start | susie() default               | author
#   estimate_residual_variance TRUE               | susie() default                 | author
#   residual_variance_lowerbound  var(y)/1e4      | susie() default                 | author
#   residual_variance_upperbound  Inf             | susie() default                 | author
#   prior_weights / null_weight  NULL (uniform 1/p) / 0 | susie() default           | author
#   preprocess                 X <- scale(X); y centred | authors' repo of the S1 design
#                              (The-PARNI-scheme @3b95d66, R/simulation/simulation_example.R
#                              l.12-13); HQ corrected ruling 2026-11-25      | OURS (PRE)
#   standardize / intercept    TRUE / TRUE        | susie() default                 | author
#                              On the preprocessed input both do nothing new: susie()
#                              centres X and y again and divides each column by its
#                              sample sd, which is already 1 (PRE).
#   max_iter / tol             100 / 1e-3 (ELBO)  | susie() default                 | author
#   refine                     FALSE              | susie() default                 | author
#   coverage / min_abs_corr / n_purity  0.95 / 0.5 / 100 (credible sets only;
#                              do not affect PIPs)| susie() default                 | author
#   prior_tol                  1e-9 (single effects with V < prior_tol are dropped
#                              from the PIP)      | susie() / susie_get_pip default | author
#   PIP                        fit$pip            | susie(); [WSCS20] Sec 3.2.1     | author
#   seed                       set.seed(method_seed) | INTERFACE.md "Seeds"         | OURS-2
#   selection                  {j : PIP_j > 0.5}  | INTERFACE.md "Selection rule"   | OURS-3
#   threads                    BLAS/OpenMP capped (default 1) | Owls compute rule   | OURS-4
#
# OURS FLAGS (reasons)
#   OURS-1  L = 20 for ALL settings (HQ ruling 2026-11-25); the package
#           default is min(10, p).  [WSCS20] Sec 4.2 p.16 used L = 20 in their
#           10-effect scenario and L = 10 in their 1-to-5-effect scenario.  L is
#           NOT set from the true number of effects s0: the adapter never sees
#           s0, and choosing L by s0 would give SuSiE oracle knowledge that the
#           other methods do not get.  One fixed value is used, the larger of
#           the authors' two, with Sec 3.3 p.12 (inferences "often robust to
#           overstating L").  ctrl$L overrides (recorded).
#   PAPER vs THIS RUN (recorded, nothing changed):
#           (i) [WSCS20] Sec 4.2 p.15 ran susieR version 0.4.29; this is the
#           CRAN release 0.14.2.  (ii) Their displayed results fixed the prior
#           variance, sigma0l^2 = 0.1 var(y), and estimated sigma^2 (Sec 4.2
#           p.16; they report that estimating both was similar).  Here both are
#           estimated, which is the susie() default of 0.14.2
#           (estimate_prior_variance = TRUE, starting from
#           scaled_prior_variance = 0.2).  (iii) The estimated residual variance
#           is bounded by the susie() defaults residual_variance_lowerbound =
#           var(y)/1e4 and residual_variance_upperbound = Inf.
#   OURS-2  The IBSS fit is deterministic; set.seed(method_seed) is still called
#           (susieR samples only when computing credible-set purity for sets
#           larger than n_purity, which does not touch the PIPs).
#   OURS-3  Median probability model on the marginal PIPs, as fixed by
#           INTERFACE.md.  This is NOT the authors' reporting unit: [WSCS20]
#           report 95% credible sets (Sec 3.2.2); the sets are stored in
#           extra$credible_sets for reference and are not used for selection.
#   OURS-4  RhpcBLASctl caps BLAS/OpenMP threads to ctrl$threads (default 1,
#           max 4); the cap stays in force for the rest of the R process.  No
#           effect on results beyond floating-point summation order.
#   Non-convergence within max_iter = 100 is recorded (extra$converged = FALSE)
#   and is NOT treated as a failure: the authors' function returns its last
#   iterate with a warning, and so does the adapter.
#
#   PRE     PREPROCESSING (HQ corrected ruling 2026-11-25, all three Bayesian
#           adapters): X <- scale(X) (centre, unit sample sd) and
#           y <- scale(y, scale = FALSE), as the authors' repo of the S1 design
#           does (not a susieR or [WSCS20] step, hence OURS).  susie()'s defaults
#           standardize = TRUE and intercept = TRUE then repeat the same
#           operations: columns are centred and divided by their sample sd
#           (now 1), y is centred (mean now 0).  The fit is the same as on the
#           raw input up to rounding (checked by test_bayesian.R).  The
#           coefficients and the intercept susie reports refer to the scaled
#           columns and the centred y; PIPs do not depend on that.
#
# ctrl (optional; every use is recorded in `settings` with tag "OURS")
#   ctrl$suite      "S1" (default) or "S2", passed by the harness; recorded
#                   only (L = 20 is OURS in every suite)
#   ctrl$L          number of single effects (default 20)
#   ctrl$max_iter   IBSS iteration cap (default: susie()'s 100)
#   ctrl$threads    1..4 (default 1)
#   ctrl$rlib       R library path (default: the S1S2 Rlib)
# =============================================================================

fit_susie <- function(X, y, method_seed, ctrl = list()) {
  t_start <- proc.time()[["elapsed"]]
  out <- list(
    selected    = integer(0),
    pip         = NULL,
    runtime_sec = NA_real_,
    software    = list(name = "susieR", version = NA_character_),
    settings    = list(),
    extra       = list(status = "failed: not run")
  )
  warns <- character(0)
  t_fit0 <- NA_real_

  res <- tryCatch(withCallingHandlers({
    # ---- library ----------------------------------------------------------
    rlib <- if (is.null(ctrl$rlib))
      "/home/fb31/Bayesian-Variable-Selection/_local/engineering/Rlib" else ctrl$rlib
    if (dir.exists(rlib) && !(rlib %in% .libPaths())) .libPaths(c(rlib, .libPaths()))
    if (!requireNamespace("susieR", quietly = TRUE)) stop("package susieR not installed")
    out$software <- list(name = "susieR", version = as.character(utils::packageVersion("susieR")),
                         paper_version = "0.4.29 (WSCS20 Sec 4.2 p.15); this run uses the CRAN release named in `version`",
                         R = R.version.string)

    # ---- input checks -----------------------------------------------------
    if (!is.matrix(X) || !is.numeric(X)) stop("X must be a numeric matrix")
    y <- as.numeric(y)
    n <- nrow(X); p <- ncol(X)
    if (length(y) != n) stop("length(y) != nrow(X)")
    if (n < 3L || p < 2L) stop("need n >= 3 and p >= 2")
    if (anyNA(X) || anyNA(y) || any(!is.finite(X)) || any(!is.finite(y))) stop("non-finite values in X or y")
    if (length(method_seed) != 1L || !is.finite(method_seed) ||
        method_seed != floor(method_seed) || abs(method_seed) > .Machine$integer.max)
      stop("method_seed must be one whole number within integer range")

    # ---- settings ---------------------------------------------------------
    ov <- function(nm) !is.null(ctrl[[nm]])
    suite <- if (is.null(ctrl$suite)) "S1" else toupper(trimws(as.character(ctrl$suite)[1L]))   # recorded only
    fm <- formals(susieR::susie)
    L <- if (ov("L")) as.integer(ctrl$L) else 20L
    if (is.na(L) || L < 1L) stop("ctrl$L must be a positive integer")
    L <- min(L, p)
    max_iter <- if (ov("max_iter")) as.integer(ctrl$max_iter) else as.integer(eval(fm$max_iter))
    if (is.na(max_iter) || max_iter < 1L) stop("ctrl$max_iter must be a positive integer")
    sdx <- apply(X, 2L, stats::sd)
    if (any(!is.finite(sdx)) || any(sdx <= 0)) stop("X has a constant column; scale(X) would give NaN")
    X <- scale(X)                                           # PRE: repo simulation_example.R l.12
    y <- as.numeric(scale(y, scale = FALSE))                # PRE: repo simulation_example.R l.13
    args <- list(X = X, y = y, L = L)
    if (ov("max_iter")) args$max_iter <- max_iter

    # ---- threads (OURS-4) -------------------------------------------------
    threads <- if (ov("threads")) as.integer(ctrl$threads) else 1L
    if (is.na(threads) || threads < 1L) threads <- 1L
    threads <- min(threads, 4L)
    thread_cap <- "not applied (RhpcBLASctl not installed; rely on OMP_NUM_THREADS)"
    if (requireNamespace("RhpcBLASctl", quietly = TRUE)) {
      # the cap is left in force for the rest of this R process (RhpcBLASctl cannot read back the
      # current BLAS thread count, so "restoring" could raise it above the caller's own limit)
      RhpcBLASctl::blas_set_num_threads(threads); RhpcBLASctl::omp_set_num_threads(threads)
      thread_cap <- paste0("RhpcBLASctl ", as.character(utils::packageVersion("RhpcBLASctl")))
    }

    # ---- the authors' fit ---------------------------------------------------
    set.seed(as.integer(method_seed), kind = "Mersenne-Twister",
             normal.kind = "Inversion", sample.kind = "Rejection")
    t_fit0 <- proc.time()[["elapsed"]]
    fit <- do.call(susieR::susie, args)
    t_fit1 <- proc.time()[["elapsed"]]

    pip <- as.numeric(fit$pip)
    if (length(pip) != p) stop("fit$pip length != p")
    if (anyNA(pip) || any(pip < -1e-12 | pip > 1 + 1e-12)) stop("susie returned PIPs outside [0, 1] or NA")
    pip <- pmin(pmax(pip, 0), 1)

    # ---- record what was actually used --------------------------------------
    tag <- function(value, tag, source) list(value = value, tag = tag, source = source)
    dflt <- function(nm) { v <- eval(fm[[nm]]); if (is.null(v)) "NULL" else v }
    out$settings <- list(
      suite                      = tag(suite, "OURS", if (is.null(ctrl$suite)) "default S1 (no ctrl$suite given)" else "ctrl$suite from harness/run_one.R; recorded only"),
      preprocess                 = tag("X <- scale(X); y <- scale(y, scale = FALSE), applied in the adapter before susie()", "OURS",
                                       "PRE: authors' repo R/simulation/simulation_example.R l.12-13 and dataset_generation.R l.28-29 @3b95d66 (HQ ruling b, 2026-11-25); not a susieR step"),
      L                          = tag(L, "OURS",
                                       if (ov("L")) "OURS-1: ctrl$L override (adapter default 20 for all settings; susie default min(10, p))"
                                       else "OURS-1: L = 20 for all settings (HQ ruling 2026-11-25), not tuned from s0; WSCS20 Sec 4.2 p.16 used L = 20 in the 10-effect scenario (L = 10 for 1-5 effects) and Sec 3.3 p.12; susie default is min(10, p)"),
      scaled_prior_variance      = tag(dflt("scaled_prior_variance"), "author", "susie default (starting value; prior variance is estimated)"),
      estimate_prior_variance    = tag(dflt("estimate_prior_variance"), "author",
                                       "susie default; WSCS20 Sec 4.2 p.16 displayed results with the prior variance fixed at 0.1 var(y) and report similar performance when it is estimated"),
      estimate_prior_method      = tag(dflt("estimate_prior_method")[1L], "author", "susie default (first of optim/EM/simple)"),
      check_null_threshold       = tag(dflt("check_null_threshold"), "author", "susie default"),
      residual_variance          = tag(dflt("residual_variance"), "author", "susie default (NULL: initialised at var(y))"),
      estimate_residual_variance = tag(dflt("estimate_residual_variance"), "author", "susie default"),
      residual_variance_lowerbound = tag(stats::var(y) / 1e4, "author", "susie default var(drop(y))/10000"),
      residual_variance_upperbound = tag("Inf", "author", "susie default Inf (stored as text so that it survives the JSON record)"),
      prior_weights              = tag(dflt("prior_weights"), "author", "susie default (NULL: uniform 1/p)"),
      null_weight                = tag(dflt("null_weight"), "author", "susie default"),
      standardize                = tag(dflt("standardize"), "author", "susie default; on the preprocessed X it divides each column by its sample sd, which is already 1 (PRE)"),
      intercept                  = tag(dflt("intercept"), "author", "susie default; on the preprocessed input it centres X and y again, which are already centred (PRE)"),
      max_iter                   = tag(max_iter, if (ov("max_iter")) "OURS" else "author",
                                       if (ov("max_iter")) "ctrl$max_iter override (susie default 100)" else "susie default"),
      tol                        = tag(dflt("tol"), "author", "susie default (ELBO change)"),
      refine                     = tag(dflt("refine"), "author", "susie default"),
      prior_tol                  = tag(dflt("prior_tol"), "author", "susie default"),
      coverage                   = tag(dflt("coverage"), "author", "susie default (credible sets only)"),
      min_abs_corr               = tag(dflt("min_abs_corr"), "author", "susie default (credible sets only)"),
      n_purity                   = tag(dflt("n_purity"), "author", "susie default (credible sets only)"),
      pip_estimator              = tag("fit$pip = 1 - prod_l(1 - alpha_lj) over single effects with V > prior_tol", "author",
                                       "susie(); WSCS20 Sec 3.2.1 eq. (3.12)"),
      seed                       = tag(as.integer(method_seed), "OURS", "OURS-2: INTERFACE.md Seeds (the IBSS fit is deterministic)"),
      selection                  = tag("median probability model: PIP > 0.5", "OURS",
                                       "OURS-3: INTERFACE.md Selection rule (authors report 95% credible sets)"),
      threads                    = tag(threads, "OURS", paste0("OURS-4: Owls compute rule; ", thread_cap))
    )

    elbo <- as.numeric(fit$elbo)
    V <- as.numeric(fit$V)
    cs <- fit$sets$cs
    sel <- sort(which(pip > 0.5))
    conv <- list(
      niter = as.integer(fit$niter), max_iter = max_iter, converged = isTRUE(fit$converged),
      elbo_final = if (length(elbo)) elbo[length(elbo)] else NA_real_,
      elbo_last_change = if (length(elbo) >= 2L) elbo[length(elbo)] - elbo[length(elbo) - 1L] else NA_real_,
      sigma2 = as.numeric(fit$sigma2), L = L,
      n_effects_with_prior_var_gt_tol = sum(V > eval(fm$prior_tol)),
      n_credible_sets = length(cs),
      sum_pip = sum(pip), n_pip_in_0.4_0.6 = sum(pip > 0.4 & pip < 0.6)
    )
    out$selected <- as.integer(sel)
    out$pip <- pip
    out$runtime_sec <- t_fit1 - t_fit0
    out$extra <- c(list(status = "ok"), conv, list(
      prior_variance_V = V,
      elbo = elbo,
      credible_sets = if (length(cs)) lapply(cs, as.integer) else list(),
      credible_set_purity = if (!is.null(fit$sets$purity)) as.list(as.data.frame(fit$sets$purity)) else list(),
      intercept = as.numeric(fit$intercept),
      thread_cap = thread_cap,
      convergence_note = "converged = ELBO change < tol within max_iter (authors' criterion); FALSE is recorded, not a failure",
      n = n, p = p,
      json_summary = c(conv, list(n_selected = length(sel), max_pip = max(pip)))
    ))
    invisible(TRUE)
  }, warning = function(w) {
    warns <<- c(warns, conditionMessage(w))
    invokeRestart("muffleWarning")
  }), error = function(e) e)

  if (inherits(res, "error")) {
    out$selected <- integer(0)
    out["pip"] <- list(NULL)
    out$extra <- list(status = paste0("failed: ", conditionMessage(res)))
    t_end <- proc.time()[["elapsed"]]
    out$runtime_sec <- if (is.finite(t_fit0)) t_end - t_fit0 else t_end - t_start
  }
  out$extra$warnings <- unique(warns)
  out[c("selected", "pip", "runtime_sec", "software", "settings", "extra")]
}
