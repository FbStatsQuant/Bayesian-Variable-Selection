# =============================================================================
# PROVENANCE  fit_bas_mc3.R  (S1/S2 Bayesian benchmark: add-delete-swap MC3,
#             BAS::bas.lm(method = "MCMC"))
# -----------------------------------------------------------------------------
# METHOD PAPER
#   [CGL11] Clyde, Ghosh & Littman (2011) "Bayesian adaptive sampling for
#           variable selection and model averaging", J. Comput. Graph. Statist.
#           20(1):80-101, DOI 10.1198/jcgs.2010.09049.
#           Page numbers are those of the authors' preprint, the copy on Owls
#           (Core_bibliography/27_2011_Clyde_Ghosh_Littman...pdf).
#           Sec 4 pp.14-15: the "Random-Swap (RS)" comparator = the MC3
#           proposal (flip one uniformly chosen coordinate: add or delete)
#           with probability omega, otherwise a swap of a randomly chosen
#           included variable with a randomly chosen excluded one; their
#           simulations used Zellner's g-prior with g = n and a uniform model
#           prior (p.14).  Sec 4.2 p.16: "a thinned version of RS (RS-Thin),
#           based on running p times longer and saving every pth draw".
#   [GLS21] Griffin, Latuszynski & Steel (2021), Biometrika 108(1):53-69,
#           DOI 10.1093/biomet/asaa055; read as the published article (PDF
#           pages 1-17; journal page = 52 + PDF page).
#           Sec 2.1 p.3, prior (1): flat intercept, p(sigma^2) prop. sigma^-2,
#           beta_g | sigma^2, gamma ~ N(0, sigma^2 V_g), gamma_j ~ Bernoulli(h).
#           Sec 4.1 p.11: "We use the prior in (1) with V_gamma = 9I and
#           h = 10/p" (INDEPENDENT prior); the paper's own baseline, the
#           add-delete-swap Metropolis-Hastings algorithm of Table 1 (p.12),
#           was run under this same prior (1).
# SOFTWARE (authors' own; nothing reimplemented)
#   BAS 2.1.0 (CRAN; maintainer M. Clyde), installed in
#   /home/fb31/Bayesian-Variable-Selection/_local/engineering/Rlib.
#   Read: ?bas.lm, ?Bernoulli, R/bas_lm.R, src/lm_mcmc_grow.c, src/MH-funs.c,
#   src/bayesreg.c, src/tree_structures.c of the 2.1.0 source tarball.
#   [REPO]  github.com/XitongLiang/The-PARNI-scheme, commit 3b95d669e9bcf6df9e2b
#           a46fb89fc536922e12e2 (Liang, Livingstone & Griffin 2022; Griffin is
#           a co-author), the authors' R code for the S1 design.  NOT run here;
#           used only as the source of the preprocessing and of the run length:
#           R/simulation/simulation_example.R l.12-13 (X <- scale(dataset$X);
#           y <- scale(dataset$y, scale = FALSE)) and l.47-57, the alg_par of
#           its own add-delete-swap sampler ADS(): N = 180000, Nb = 60000,
#           n_chain = 1 (R/sampler/ADS.R: N iterations in total, the first Nb
#           discarded, start gamma_j ~ Bernoulli(h)).
#   method = "MCMC" is, per ?bas.lm, "MCMC ... combines a random walk
#   Metropolis Hastings (as in MC3 of Raftery et al 1997) with a random swap of
#   a variable included with a variable that is currently excluded" = the RS
#   algorithm of [CGL11] = add-delete-swap MC3.
#
# THE CALL (everything not listed is left at the bas.lm default, INCLUDING the
#           coefficient prior and the model prior: owner's decision "option (A)")
#   X <- scale(X); y <- scale(y, scale = FALSE)          # PRE
#   set.seed(method_seed)
#   fit <- BAS::bas.lm(y ~ X, method = "MCMC",
#                      MCMC.iterations = 120000, burnin.iterations = 60000)
#   pip <- fit$probne0[-1]        # drop the intercept
#
# SETTINGS  (value | source | tag)
#   method             "MCMC" (add-delete-swap MC3)   | task; ?bas.lm; [CGL11] Sec 4 | author
#   The rows tagged "author" are bas.lm 2.1.0 defaults; the value quoted is
#   formals(BAS::bas.lm)$<name>, and the argument is NOT passed (OURS-1).
#   prior              "ZS-null": Zellner-Siow Cauchy prior on the coefficients,
#                      beta_g | g, sigma^2 ~ N(0, g sigma^2 (X_g'X_g)^-1),
#                      1/g ~ Gamma(1/2, n/2); flat intercept, p(sigma^2) prop.
#                      sigma^-2.  Bayes factor against the null model by the
#                      Laplace approximation LogBF_ZS_null(R2, n, d)
#                      (src/bayesreg.c l.96-97)        | formals: "ZS-null"           | author
#   alpha              NULL; bas.lm then sets alpha = 1 for "ZS-null"
#                      (R/bas_lm.R l.723-739).  LogBF_ZS_null takes no alpha
#                      argument                        | formals: NULL                | author
#   modelprior         beta.binomial(1, 1): inclusion probability ~ Uniform(0, 1),
#                      i.e. uniform on the model size  | formals: beta.binomial(1, 1) | author
#   include.always     ~1: only the intercept is forced in
#                                                      | formals: ~1                  | author
#   update             NULL (tree updates of the sampling probabilities; for
#                      method "BAS" / "MCMC+BAS" only) | formals: NULL                | author
#   prob.rw            0.5: MCMC proposal mix, flip of one coordinate (add or
#                      delete) with probability 0.5, else swap; [CGL11] Sec 4
#                      (omega)                         | formals: 0.5                 | author
#   preprocess         X <- scale(X); y centred        | [REPO] script l.12-13, dataset_generation.R
#                                                        l.28-29; HQ ruling b, 2026-11-25 | OURS (PRE)
#   MCMC.iterations    120000                          | run length based on the authors' repo ADS
#                                                        alg_par (N = 180000 in total, of which
#                                                        Nb = 60000 burn-in); bas.lm default
#                                                        is (p + 1) * 1000              | OURS-8
#   burnin.iterations  60000                           | the same alg_par (Nb = 60000); BAS does
#                                                        not discard burn-in (NOTE-a); bas.lm
#                                                        default is (p + 1) * 25        | OURS-8
#   start              null model                      | bas.lm default (bestmodel = NULL) | author
#   initprobs          "Uniform"                       | bas.lm default (unused by MCMC proposals) | author
#   renormalize        FALSE: PIP = MCMC frequencies (probne0.MCMC) | bas.lm default  | author
#   thin               1 (every MH step is recorded)   | bas.lm default (see OURS-3)   | author
#   pivot              TRUE                            | bas.lm default (see OURS-4)   | author
#   intercept, centring  intercept always in; X centred inside bas.lm | bas.lm        | author
#   GROW/expand/n.models.init/tol  TRUE / 1.05 / 2500 / 1e-7 | bas.lm defaults         | author
#   seed               set.seed(method_seed)           | INTERFACE.md "Seeds"          | OURS-5
#   selection          {j : PIP_j > 0.5}               | INTERFACE.md "Selection rule" | OURS-6
#   threads            BLAS/OpenMP capped (default 1)  | Owls compute rule             | OURS-7
#
# OURS FLAGS (reasons)
#   OURS-1  PRIORS = THE PACKAGE DEFAULTS (owner's decision 2026-11-25, "option
#           (A)", relayed by the manager; it replaces the earlier ruling that
#           matched BAS to the ASI prior with a g-prior, g = 9 (n - 1), and
#           Bernoulli(10/p)).  bas.lm is called without `prior`, `alpha` and
#           `modelprior`, so it uses prior = "ZS-null" and modelprior =
#           beta.binomial(1, 1) (formals of bas.lm, BAS 2.1.0).  Both are the
#           authors' defaults and are tagged "author".
#           CONSEQUENCE.  BAS MC3 and ASI do NOT target the same posterior.
#           ASI ([GLS21] Sec 4.1 p.11): independent prior N(0, 9 sigma^2 I) and
#           gamma_j ~ Bernoulli(10/p), prior mean model size 10.  BAS: Zellner-
#           Siow mixture of g-priors and a uniform prior on the model size.
#           BAS cannot express N(0, 9 sigma^2 I) at all: bas.lm(prior = ) offers
#           "AIC", "BIC", "g-prior", "JZS", "ZS-null", "ZS-full", "hyper-g",
#           "hyper-g-laplace", "hyper-g-n", "EB-local", "EB-global", all with
#           covariance prop. (X_g'X_g)^-1.
#           ALTERNATIVE CONSIDERED, OWNER CHOSE (A): a call matched to the ASI
#           prior, ctrl = list(prior = "g-prior", alpha = 9 * (n - 1), h =
#           10/p).  It stays reachable through ctrl, OFF by default.  It is
#           not identical to the ASI prior either: for correlated included
#           columns its covariance is 9 R_g^-1, not 9 I.
#   OURS-2  SUITES.  The same call is used in S1 and S2.  ctrl$suite ("S1"
#           default, or "S2", passed by the harness) is recorded only.  For
#           n <= p, bas.lm may warn about the model prior; warnings are kept in
#           extra$warnings.
#   OURS-3  (no longer a deviation)  thin = 1, the bas.lm default.  Earlier
#           rounds ran thin = p because the default run length (p + 1) * 1025
#           steps at thin = 1 needed more than 12 GB.  At the ruled run length
#           (OURS-8) thin = 1 fits: measured on Owls, BAS 2.1.0, one core, at
#           240000 steps under the earlier g-prior call, (n, p) = (1000, 5000):
#           33 s, peak RSS 0.9 GB with pivot = FALSE and 34 s, 1.2 GB with
#           pivot = TRUE; (50, 1000): 10 s, 0.66 / 0.89 GB.  Figures for the
#           final call (180000 steps, package-default priors) are in README.md.
#           thin = p would leave only 180000 / p recorded states (36 at
#           p = 5000), too few for a PIP.  With thin = 1 every MH step enters
#           the PIP average, as in the repo's ADS.  ctrl$thin overrides (OURS).
#   OURS-4  (no longer a deviation)  pivot = TRUE, the bas.lm default.  Earlier
#           rounds ran pivot = FALSE because cholregpivot() R_alloc()s work
#           arrays per model fit that are not released until bas.lm returns
#           (src/bayesreg.c l.146-151): 10 GB at p = 5000 with the default run
#           length.  At the ruled run length the cost is 0.3 GB (figures in
#           OURS-3).  PIPs were identical with pivot = TRUE and FALSE in every
#           comparison made (g-prior call: (1000, 5000) and (50, 1000)).  The
#           adapter records fit$rank_deficient.  ctrl$pivot overrides (OURS).
#   OURS-5  All randomness (unif_rand in the C sampler) follows
#           set.seed(method_seed), Mersenne-Twister / Inversion / Rejection.
#   OURS-6  Median probability model, as fixed by INTERFACE.md.
#   OURS-7  RhpcBLASctl caps BLAS/OpenMP threads to ctrl$threads (default 1,
#           max 4); the cap stays in force for the rest of the R process.
#           No effect on results.
#   OURS-8  RUN LENGTH (manager's latest ruling 2026-11-25): MCMC.iterations =
#           120000 and burnin.iterations = 60000, based on the single-chain
#           add-delete-swap run in the authors' repo script ([REPO]): N =
#           180000 iterations in total, of which Nb = 60000 are burn-in.
#           The total number of steps is the same; the use of burn-in is not:
#             repo ADS: 180000 iterations, the first 60000 discarded,
#                       120000 recorded; start gamma_j ~ Bernoulli(h).
#             BAS:      120000 + 60000 = 180000 MH steps, none discarded,
#                       180000 states in the PIP average; start = null model
#                       (NOTE-a).
#           One ADS iteration is not one BAS step.  Both are one MH proposal,
#           but ADS draws swap, add or delete with probability 1/3 each when
#           all three are possible (ADS.R l.183-197), and BAS a flip of one
#           uniformly chosen coordinate or a swap with probability 1/2 each
#           (prob.rw = 0.5).
#           So the early steps, when the chain is still climbing from the null
#           model, are part of every PIP.  The bas.lm defaults, (p + 1) * 1000
#           and (p + 1) * 25, are 3 to 28 times longer (514k to 5.1M steps).
#           Fixed for every setting, S1 and S2 alike.  ctrl$MCMC.iterations and
#           ctrl$burnin.iterations override (OURS).
#   PRE     PREPROCESSING (HQ corrected ruling 2026-11-25, all three Bayesian
#           adapters): X <- scale(X) (centre, unit sample sd) and y centred,
#           as the authors' repo does for this design.  bas.lm always fits an
#           intercept and centres X itself, and the Zellner-Siow prior (like
#           every g-prior) does not depend on the scale of a column, so this
#           step changes the BAS posterior only by rounding; it is applied so
#           that all three methods receive the same input.
#
# NOTES on what the authors' code does (BAS 2.1.0, src/lm_mcmc_grow.c)
#   NOTE-a  "Burn-in" is NOT discarded: the loop runs MCMC.iterations +
#           burnin.iterations MH steps (l.223) and every recorded state from
#           step 0 on enters probne0.MCMC (l.304-312, l.367).  So the nominal
#           60000 burn-in steps are INCLUDED in the PIP average.  Run as
#           shipped; recorded as burn_in_discarded = FALSE and
#           burnin_steps_in_average = 60000.
#   NOTE-c  iid_se_at_pip_half = sqrt(0.25 / recorded_states) is the standard
#           error a PIP of 0.5 would have IF the recorded states were
#           independent draws.  It is a scale reference (OURS), not an estimate
#           of the Monte Carlo error: the states are autocorrelated, so the
#           true error is larger by an unknown factor.
#   NOTE-b  thin counts single MH steps (m %% thin == 0).  At the default
#           thin = 1 every step is recorded.  With ctrl$thin > 1 the per-model
#           visit counts (fit$freq, postprobs) are not meaningful.  The adapter
#           reports probne0.MCMC only (renormalize = FALSE, the default).
#
# ctrl (optional; every use is recorded in `settings` with tag "OURS")
#   ctrl$prior, ctrl$alpha    coefficient prior family / hyperparameter (default:
#                             bas.lm's own, "ZS-null")
#   ctrl$h                    model prior Bernoulli(h) instead of bas.lm's
#                             beta.binomial(1, 1)
#   ctrl$suite                "S1" (default) or "S2", passed by the harness; sets
#                             recorded only, never changes the fit
#   ctrl$thin, ctrl$pivot     overrides of the bas.lm defaults 1 and TRUE
#   ctrl$MCMC.iterations, ctrl$burnin.iterations   run-length overrides (OURS-8)
#   ctrl$threads              1..4 (default 1)
#   ctrl$rlib                 R library path (default: the S1S2 Rlib)
# =============================================================================

fit_bas_mc3 <- function(X, y, method_seed, ctrl = list()) {
  t_start <- proc.time()[["elapsed"]]
  out <- list(
    selected    = integer(0),
    pip         = NULL,
    runtime_sec = NA_real_,
    software    = list(name = "BAS", version = NA_character_),
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
    if (!requireNamespace("BAS", quietly = TRUE)) stop("package BAS not installed")
    out$software <- list(name = "BAS", version = as.character(utils::packageVersion("BAS")),
                         R = R.version.string)

    # ---- input checks -----------------------------------------------------
    if (!is.matrix(X) || !is.numeric(X)) stop("X must be a numeric matrix")
    y <- as.numeric(y)
    n <- nrow(X); p <- ncol(X)
    if (length(y) != n) stop("length(y) != nrow(X)")
    if (n < 4L || p < 2L) stop("need n >= 4 and p >= 2")
    if (anyNA(X) || anyNA(y) || any(!is.finite(X)) || any(!is.finite(y))) stop("non-finite values in X or y")
    if (length(method_seed) != 1L || !is.finite(method_seed) ||
        method_seed != floor(method_seed) || abs(method_seed) > .Machine$integer.max)
      stop("method_seed must be one whole number within integer range")

    # ---- settings ---------------------------------------------------------
    ov <- function(nm) !is.null(ctrl[[nm]])
    # suite of the setting, passed by harness/run_one.R as ctrl$suite ("S1" or "S2"); default "S1".
    # It is recorded only; the call is the same in both suites (OURS-2).
    suite <- if (is.null(ctrl$suite)) "S1" else toupper(trimws(as.character(ctrl$suite)[1L]))
    fm <- formals(BAS::bas.lm)
    # OURS-1 (option A): prior, alpha and modelprior are bas.lm's own defaults unless ctrl overrides them.
    prior <- if (ov("prior")) as.character(ctrl$prior) else as.character(eval(fm$prior))
    alpha <- if (ov("alpha")) as.numeric(ctrl$alpha) else NULL
    if (!is.null(alpha) && (length(alpha) != 1L || !is.finite(alpha) || alpha <= 0)) stop("ctrl$alpha must be one positive number")
    h <- if (ov("h")) as.numeric(ctrl$h) else NA_real_
    if (ov("h") && (length(h) != 1L || !is.finite(h) || h <= 0 || h >= 1)) stop("ctrl$h must lie in (0, 1)")
    thin <- if (ov("thin")) as.integer(ctrl$thin) else 1L                       # bas.lm default (OURS-3)
    pivot <- if (ov("pivot")) isTRUE(as.logical(ctrl$pivot)) else TRUE            # bas.lm default (OURS-4)
    if (is.na(thin) || thin < 1L) stop("ctrl$thin must be a positive integer")
    pm <- p + 1L                                            # bas.lm's p: columns of the model matrix incl. intercept
    n_mcmc <- if (ov("MCMC.iterations")) as.integer(ctrl$MCMC.iterations) else 120000L     # OURS-8: repo ADS alg_par N - Nb
    n_burn <- if (ov("burnin.iterations")) as.integer(ctrl$burnin.iterations) else 60000L  # OURS-8: repo ADS alg_par Nb
    if (is.na(n_mcmc) || is.na(n_burn) || n_mcmc < 1L || n_burn < 0L) stop("iteration counts must be positive integers within integer range")

    sdx <- apply(X, 2L, stats::sd)
    if (any(!is.finite(sdx)) || any(sdx <= 0)) stop("X has a constant column; scale(X) would give NaN")
    X <- scale(X)                                           # PRE: repo simulation_example.R l.12
    y <- as.numeric(scale(y, scale = FALSE))                # PRE: repo simulation_example.R l.13

    args <- list(formula = y ~ X, method = "MCMC",
                 MCMC.iterations = n_mcmc, burnin.iterations = n_burn)
    if (ov("prior")) args$prior <- prior                    # otherwise bas.lm's own default ("ZS-null")
    if (!is.null(alpha)) args$alpha <- alpha
    if (ov("h")) args$modelprior <- BAS::Bernoulli(probs = h)   # otherwise bas.lm's own default (beta.binomial(1, 1))
    if (ov("thin")) args$thin <- thin                       # otherwise bas.lm's own default (1)
    if (ov("pivot")) args$pivot <- pivot                    # otherwise bas.lm's own default (TRUE)

    # ---- threads (OURS-7) -------------------------------------------------
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
    fit <- do.call(BAS::bas.lm, args)
    t_fit1 <- proc.time()[["elapsed"]]

    if (length(fit$probne0) != pm) stop("probne0 length != p + 1")
    pip <- as.numeric(fit$probne0[-1L])
    if (anyNA(pip) || any(pip < 0 | pip > 1)) stop("BAS returned PIPs outside [0, 1] or NA")
    if (!isTRUE(all.equal(pip, as.numeric(fit$probne0.MCMC[-1L])))) stop("probne0 is not probne0.MCMC")

    # ---- record what was actually used --------------------------------------
    tag <- function(value, tag, source) list(value = value, tag = tag, source = source)
    # source text of an argument left at its shipped default: quotes formals(bas.lm)
    dflt <- function(nm, note = "") paste0("author (bas.lm ", out$software$version, " default): formals(bas.lm)$", nm, " = ",
                                           paste(deparse(fm[[nm]]), collapse = " "), if (nzchar(note)) paste0("; ", note) else "")
    mp <- fit$modelprior
    mp_txt <- if (ov("h")) sprintf("Bernoulli(probs = %.10g)", h) else
      sprintf("%s(%s)", if (identical(mp$family, "Beta-Binomial")) "beta.binomial" else as.character(mp$family),
              paste(format(mp$hyper.parameters), collapse = ", "))
    if (!ov("prior") && !identical(as.character(fit$prior), prior)) stop("bas.lm did not use its documented default prior")
    alpha_used <- if (is.null(fit$alpha)) NA_real_ else as.numeric(fit$alpha)
    out$settings <- list(
      suite             = tag(suite, "OURS", if (is.null(ctrl$suite)) "default S1 (no ctrl$suite given)" else "ctrl$suite from harness/run_one.R; recorded only, the call is the same in S1 and S2 (OURS-2)"),
      preprocess        = tag("X <- scale(X); y <- scale(y, scale = FALSE), applied in the adapter before bas.lm", "OURS",
                              "PRE: authors' repo R/simulation/simulation_example.R l.12-13 and dataset_generation.R l.28-29 @3b95d66 (HQ ruling b, 2026-11-25); bas.lm centres X itself and the Zellner-Siow prior (like every g-prior) is scale-free, so the BAS posterior is unchanged beyond rounding"),
      method            = tag("MCMC", "author", "task; ?bas.lm (MC3 random walk + random swap); CGL11 Sec 4 'RS'"),
      prior             = tag(prior, if (ov("prior")) "OURS" else "author",
                              if (ov("prior")) "ctrl$prior override (bas.lm default: ZS-null)"
                              else dflt("prior", "not passed (OURS-1, owner's option A); this is NOT the ASI prior N(0, 9 sigma^2 I) of GLS21 Sec 4.1")),
      alpha             = tag(alpha_used, if (ov("alpha")) "OURS" else "author",
                              if (ov("alpha")) "ctrl$alpha override"
                              else dflt("alpha", "not passed; value shown is what bas.lm set for the prior family (1 for ZS-null, R/bas_lm.R l.723-739; LogBF_ZS_null takes no alpha)")),
      modelprior        = tag(mp_txt, if (ov("h")) "OURS" else "author",
                              if (ov("h")) "ctrl$h override (bas.lm default: beta.binomial(1, 1))"
                              else dflt("modelprior", "not passed (OURS-1, owner's option A); this is NOT the ASI model prior Bernoulli(10/p) of GLS21 Sec 4.1")),
      include.always    = tag(paste(deparse(fm$include.always), collapse = " "), "author", dflt("include.always", "only the intercept is forced in")),
      update            = tag(if (is.null(fm$update)) "NULL" else paste(deparse(fm$update), collapse = " "), "author",
                              dflt("update", "tree updates of sampling probabilities, methods BAS and MCMC+BAS only")),
      prob.rw           = tag(eval(fm$prob.rw), "author", dflt("prob.rw", "MCMC proposal mix: flip of one coordinate with this probability, else swap; omega of CGL11 Sec 4 p.14")),
      MCMC.iterations   = tag(n_mcmc, "OURS",
                              if (ov("MCMC.iterations")) "ctrl override (adapter default 120000; bas.lm default (p + 1) * 1000)"
                              else "OURS-8: run length based on the authors' repo ADS alg_par (N = 180000 in total, Nb = 60000 of them burn-in; R/simulation/simulation_example.R l.48-49 @3b95d66), so 120000 + 60000 steps; BAS does not discard burn-in but averages over it (NOTE-a); one ADS iteration is not one BAS step: both are one MH proposal, but ADS draws swap, add or delete with probability 1/3 each (ADS.R l.183-197) and BAS a coordinate flip or a swap with probability 1/2 each (prob.rw); bas.lm default is (p + 1) * 1000"),
      burnin.iterations = tag(n_burn, "OURS",
                              if (ov("burnin.iterations")) "ctrl override (adapter default 60000; bas.lm default (p + 1) * 25)"
                              else "OURS-8: run length from the authors' repo ADS alg_par (Nb = 60000; simulation_example.R l.49 @3b95d66); BAS does not discard burn-in (NOTE-a): BAS runs 120000 + 60000 = 180000 steps and averages over all of them, the repo ADS runs 180000 and discards the first 60000"),
      start             = tag("null model", "author", "bas.lm default (bestmodel = NULL)"),
      initprobs         = tag(eval(fm$initprobs), "author", dflt("initprobs")),
      renormalize       = tag(eval(fm$renormalize), "author", dflt("renormalize", "probne0 = MCMC frequencies")),
      thin              = tag(thin, if (ov("thin")) "OURS" else "author",
                              if (ov("thin")) "ctrl$thin override (bas.lm default 1)" else dflt("thin", "not passed")),
      pivot             = tag(pivot, if (ov("pivot")) "OURS" else "author",
                              if (ov("pivot")) "ctrl$pivot override (bas.lm default TRUE)" else dflt("pivot", "not passed")),
      GROW              = tag(eval(fm$GROW), "author", dflt("GROW")),
      expand            = tag(eval(fm$expand), "author", dflt("expand")),
      n.models.init     = tag(eval(fm$n.models.init), "author", dflt("n.models.init")),
      tol               = tag(eval(fm$tol), "author", dflt("tol")),
      intercept         = tag("always included; X centred inside bas.lm", "author", "bas.lm"),
      seed              = tag(as.integer(method_seed), "OURS", "OURS-5: INTERFACE.md Seeds; set.seed(method_seed) before bas.lm"),
      selection         = tag("median probability model: PIP > 0.5", "OURS", "OURS-6: INTERFACE.md Selection rule"),
      threads           = tag(threads, "OURS", paste0("OURS-7: Owls compute rule; ", thread_cap))
    )

    total_steps <- as.numeric(n_mcmc) + as.numeric(n_burn)
    n_recorded <- ceiling(total_steps / thin)
    sel <- sort(which(pip > 0.5))
    conv <- list(
      mh_steps_total = total_steps, MCMC.iterations = n_mcmc, burnin.iterations = n_burn,
      burn_in_discarded = FALSE, burnin_steps_in_average = n_burn,       # NOTE-a: as shipped
      thin = thin, recorded_states = n_recorded,
      iid_se_at_pip_half = sqrt(0.25 / n_recorded),                        # NOTE-c: s.e. under independence, a scale reference only
      n_unique_models_stored = as.integer(fit$n.models),
      sum_pip = sum(pip), n_pip_in_0.4_0.6 = sum(pip > 0.4 & pip < 0.6),
      rank_deficient = isTRUE(fit$rank_deficient)
    )
    out$selected <- as.integer(sel)
    out$pip <- pip
    out$runtime_sec <- t_fit1 - t_fit0
    out$extra <- c(list(status = "ok"), conv, list(
      thread_cap = thread_cap,
      convergence_note = paste("BAS returns no chain. The chain starts at the null model and the nominal burn-in steps are part of the",
                               "PIP average (BAS 2.1.0 src/lm_mcmc_grow.c). PIP = probne0.MCMC, the visit frequencies.",
                               "No convergence test is applied."),
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
  out$extra$warnings <- unique(gsub("\\s+", " ", warns))
  out[c("selected", "pip", "runtime_sec", "software", "settings", "extra")]
}
