# =============================================================================
# PROVENANCE  test_bayesian.R  (unit test for fit_bas_mc3.R, fit_asi.R, fit_susie.R)
# -----------------------------------------------------------------------------
# Purpose: show that the three adapters (a) never error, (b) honour the
# INTERFACE.md contract, (c) return exactly what the authors' own function
# returns for the documented call, (d) depend on method_seed only, (e) give sane
# PIPs and timings; with --full, (f) measure runtime and peak memory at the
# largest S1 size (n = 1000, p = 5000).  It also checks (g) that the BAS adapter
# runs bas.lm with the package's own default prior and model prior (owner's
# option (A), fit_bas_mc3.R OURS-1), (h) that the ASI adapter returns exactly
# what the authors' ORIGINAL ASI_sampler.m returns when called directly under
# Octave with the same 18 arguments, that the sampler file has the pinned
# sha256, and that the same seed gives identical PIPs, and (i) that the
# preprocessing X <- scale(X), y <- scale(y, scale = FALSE) is applied and
# recorded by all three adapters (HQ ruling b, 2026-11-25).
# Software under test: BAS (bas.lm, method = "MCMC"), ASI_sampler.m Version3.0
# under GNU Octave, susieR (susie); versions printed at run time.  See the
# PROVENANCE block of each adapter for papers, sections and settings.
# ASI run lengths in this test: one fit at the adapter defaults (2000 + 4000
# iterations, 25 chains) takes about 15 to 30 minutes under Octave at p = 500
# to 1000, so the quick test runs the four cases at 100 + 200 iterations, 25
# chains (the length of the authors' demo scripts run_tecator.m and
# run_concrete.m), and one default-length fit on a 40 x 30 problem to check the
# default settings.  --long runs the strong S1-like case and the S2 SNR 6 case
# at the default length; --full runs the (1000, 5000) case at the default
# length; --cases=<regex> limits section 1 to matching cases and skips
# sections 2 to 4 (so long fits can run as separate 1-core processes).
# Everything in this file is test scaffolding and is OURS:
#   - data generators are local to the test and identical to those of
#     ../frequentist/test_frequentist.R (same designs, same test seeds):
#       S1: Griffin, Latuszynski & Steel (2021), DOI 10.1093/biomet/asaa055,
#           Sec 4.1: beta* = SNR*sqrt(sigma^2 log(p)/n)*(2,-3,2,2,-3,3,-2,3,-2,3,0,..),
#           sigma^2 = 1, Sigma_jk = rho^|j-k|, rho = 0.6;  test size n=200, p=500.
#       S2: Hastie, Tibshirani & Tibshirani (2020), DOI 10.1214/19-STS733,
#           Sec 3.1: Sigma_ij = rho^|i-j|, beta-type 2 (first s entries 1),
#           sigma^2 = beta' Sigma beta / SNR; "high-5" size n=50, p=1000, s=5, rho=0.35.
#   - method_seed follows INTERFACE.md: data_seed + 10000000*method_code
#     (bas_mc3 4, asi 5, susie 6).
#   - "sanity" thresholds (exact recovery by BAS/ASI on the strong S1-like case)
#     are test expectations, not part of any method.
# Run (Owls only, lean; one core per process):
#   OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 19 Rscript test_bayesian.R [--only=bas_mc3|asi|susie] [--full] [--long] [--cases=<regex>]
#   --only   test one adapter (lets the three run as three 1-core processes)
#   --full   adds one fit per adapter at n=1000, p=5000 (S1 full size, SNR 2)
# Exit status 0 = all checks passed; 1 = at least one check failed.
# =============================================================================

args <- commandArgs(trailingOnly = FALSE)
here <- dirname(normalizePath(sub("^--file=", "", args[grep("^--file=", args)][1])))
targs <- commandArgs(trailingOnly = TRUE)
full <- "--full" %in% targs
long <- "--long" %in% targs                                  # ASI at the default run length on two quick cases
case_rx <- sub("^--cases=", "", grep("^--cases=", targs, value = TRUE))
ROOT <- "/home/fb31/Bayesian-Variable-Selection"
OCT_HOME <- file.path(ROOT, "_local/engineering/envs/octave")
ASI_DIR <- file.path(ROOT, "_local/engineering/ext/griffin_asi_original/Version3.0")
ASI_SUPP <- file.path(ROOT, "_local/papers/Benchmark_methods/Griffin2021_supplement/code/Version3.0")
ASI_SHA <- "4705c79523f4d772625764bcb880ed04852d83d121ea94fe46ef224d3b10dddb"
TMP_ROOT <- file.path(ROOT, "_local/tmp")
asi_quick <- list(burnin = 100, numbofits = 200)            # 25 chains; the authors' demo length
small <- list(burnin = 20, numbofits = 40, numbofreps = 5)  # shortest ASI run used for repeated checks
only <- sub("^--only=", "", grep("^--only=", targs, value = TRUE))
RLIB <- "/home/fb31/Bayesian-Variable-Selection/_local/engineering/Rlib"
.libPaths(c(RLIB, .libPaths()))
PARNI <- file.path("/home/fb31/Bayesian-Variable-Selection/_local/engineering/ext",
                   "The-PARNI-scheme@3b95d669e9bcf6df9e2ba46fb89fc536922e12e2")

# adapters are loaded the way harness/methods.R::load_method does it
load_adapter <- function(name) {
  env <- new.env(parent = globalenv())
  sys.source(file.path(here, paste0("fit_", name, ".R")), envir = env, chdir = TRUE)
  get(paste0("fit_", name), envir = env)
}
methods <- list(bas_mc3 = list(f = load_adapter("bas_mc3"), code = 4L),
                asi     = list(f = load_adapter("asi"),     code = 5L),
                susie   = list(f = load_adapter("susie"),   code = 6L))
if (length(only)) methods <- methods[intersect(names(methods), only)]
if (!length(methods)) stop("--only must be one of bas_mc3, asi, susie")

n_fail <- 0L
check <- function(ok, what) {
  ok <- isTRUE(ok)
  if (!ok) n_fail <<- n_fail + 1L
  cat(sprintf("  [%s] %s\n", if (ok) "PASS" else "FAIL", what))
  invisible(ok)
}
info <- function(...) cat(sprintf("  [INFO] %s\n", sprintf(...)))
peak_rss_mb <- function() {
  x <- tryCatch(grep("^VmHWM", readLines("/proc/self/status"), value = TRUE), error = function(e) character(0))
  if (length(x)) as.numeric(gsub("[^0-9]", "", x)) / 1024 else NA_real_
}
mseed <- function(data_seed, code) data_seed + 10000000 * code
SEEDKIND <- function(s) set.seed(s, kind = "Mersenne-Twister", normal.kind = "Inversion", sample.kind = "Rejection")

# ---- test data generators (OURS, test only; same as test_frequentist.R) -----
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
  "S1-like n=200 p=500 rho=.6 SNR=3"     = gen_s1(200, 500, 3,   seed = 501001001),
  "S1-like n=200 p=500 rho=.6 SNR=0.5"   = gen_s1(200, 500, 0.5, seed = 501002001),
  "S2 hi-5 n=50 p=1000 rho=.35 SNR=6"    = gen_s2(50, 1000, 5, 6,    0.35, seed = 502001001),
  "S2 hi-5 n=50 p=1000 rho=.35 SNR=0.42" = gen_s2(50, 1000, 5, 0.42, 0.35, seed = 502002001)
)
if (full) cases[["S1 full n=1000 p=5000 rho=.6 SNR=2"]] <- gen_s1(1000, 5000, 2, seed = 501016001)
all_cases <- cases
if (length(case_rx)) cases <- cases[grepl(case_rx, names(cases))]
if (!length(cases)) stop("--cases matches no case")

cat("== versions ==\n")
cat(sprintf("  %s | BAS %s | susieR %s | Octave env %s | ASI_sampler.m sha256 %s\n", R.version.string,
            as.character(packageVersion("BAS")), as.character(packageVersion("susieR")), OCT_HOME,
            if (file.exists(file.path(ASI_DIR, "ASI_sampler.m"))) unname(tools::sha256sum(file.path(ASI_DIR, "ASI_sampler.m"))) else "FILE MISSING"))
cat(sprintf("  threads: OMP_NUM_THREADS=%s OPENBLAS_NUM_THREADS=%s; host %s\n",
            Sys.getenv("OMP_NUM_THREADS", "unset"), Sys.getenv("OPENBLAS_NUM_THREADS", "unset"), Sys.info()[["nodename"]]))

NAMES <- c("selected", "pip", "runtime_sec", "software", "settings", "extra")
contract_checks <- function(r, p, label) {
  check(identical(names(r), NAMES), paste(label, "returns exactly", paste(NAMES, collapse = ", ")))
  check(identical(r$extra$status, "ok"), paste0(label, " status ok (got: ", r$extra$status, ")"))
  check(is.numeric(r$pip) && length(r$pip) == p && !anyNA(r$pip) && all(r$pip >= 0 & r$pip <= 1),
        paste(label, "pip is numeric, length p, in [0, 1]"))
  check(is.integer(r$selected) && identical(r$selected, which(r$pip > 0.5)),
        paste(label, "selected == which(pip > 0.5), sorted integer"))
  check(is.numeric(r$runtime_sec) && length(r$runtime_sec) == 1L && is.finite(r$runtime_sec) && r$runtime_sec >= 0,
        paste(label, "runtime_sec finite"))
  check(is.character(r$software$name) && is.character(r$software$version) && !is.na(r$software$version),
        paste(label, "software name + version recorded"))
  st_ok <- length(r$settings) > 0 && all(vapply(r$settings, function(s)
    is.list(s) && all(c("value", "tag", "source") %in% names(s)) && s$tag %in% c("author", "OURS") && nzchar(s$source), TRUE))
  check(st_ok, paste(label, "every setting has value / tag (author|OURS) / source"))
  check(is.list(r$extra$json_summary) && all(lengths(r$extra$json_summary) == 1L),
        paste(label, "extra$json_summary is a flat list of scalars"))
}

# =============================================================================
# 1. Fits on the test cases
# =============================================================================
results <- list()
for (cn in names(cases)) {
  d <- cases[[cn]]; p <- ncol(d$X)
  cat(sprintf("\n== %s ==\n", cn))
  for (m in names(methods)) {
    suite <- if (grepl("^S2", cn)) "S2" else "S1"            # what harness/run_one.R passes as ctrl$suite
    # ASI: default length only with --long (two cases) or for the --full case; otherwise the demo length
    asi_default_len <- m == "asi" && ((long && grepl("SNR=3$|SNR=6$", cn)) || grepl("^S1 full", cn))
    ctrl1 <- c(list(suite = suite), if (m == "asi" && !asi_default_len) asi_quick)
    if (m == "asi") info("asi run length for this case: %s", if (asi_default_len) "adapter default (2000 + 4000, 25 chains)" else "100 + 200, 25 chains (ctrl; demo length)")
    r <- tryCatch(methods[[m]]$f(d$X, d$y, mseed(d$data_seed, methods[[m]]$code), ctrl1),
                  error = function(e) structure(list(msg = conditionMessage(e)), class = "adapter_error"))
    if (inherits(r, "adapter_error")) { check(FALSE, paste0(m, " did not error (ERROR: ", r$msg, ")")); next }
    check(TRUE, paste(m, "did not error"))
    contract_checks(r, p, m)
    results[[paste(cn, m)]] <- r
    # per-run provenance: the S1 prior is "author" in suite S1 and "OURS" once transferred to suite S2
    tg1 <- function(nm) r$settings[[nm]]$tag
    want <- if (suite == "S1") "author" else "OURS"
    if (identical(r$extra$status, "ok")) {
      check(identical(r$settings$suite$value, suite), paste0(m, " settings record suite ", suite))
      check(is.character(r$settings$preprocess$value) && grepl("scale(X)", r$settings$preprocess$value, fixed = TRUE) &&
              grepl("simulation_example.R", r$settings$preprocess$source, fixed = TRUE),
            paste0(m, " settings record the preprocessing X <- scale(X), y centred, with its source"))
      if (m == "asi") {
        wl <- if (asi_default_len) want else "OURS"            # burnin and numbofits are ctrl overrides at the demo length
        check(all(vapply(c("g", "hparam", "tau", "numbofreps"), tg1, "") == want) && tg1("burnin") == wl && tg1("numbofits") == wl &&
                all(vapply(c("gprior", "mode", "RB_adap", "RB", "nu", "thin", "heat", "adap_type", "kappa", "eps"), tg1, "") == "author") &&
                tg1("data_fixed") == "OURS" && tg1("updateg") == "OURS",
              paste0("asi: g, hparam, tau, numbofreps tagged ", want, " in suite ", suite, "; burnin, numbofits tagged ", wl,
                     "; gprior, mode, RB_adap, RB, nu, thin, heat, adap_type tagged author; data_fixed, updateg tagged OURS"))
        check(is.numeric(r$extra$accept_final) && r$extra$accept_final >= 0 && r$extra$accept_final <= 1 &&
                is.numeric(r$extra$zeta_final) && r$extra$zeta_final > 0 && r$extra$zeta_final < 1 &&
                length(r$extra$zetaAS_final) == p && length(r$extra$zetaDS_final) == p && length(r$extra$pi_final) == p &&
                isTRUE(r$extra$prob_inclusion2_all_zero) && grepl("^10\\.", r$software$octave_version),
              "asi: extra holds the code's acceptance rate, final zeta, final A and D (length p) and the derived pi; prob_inclusion2 is all zero; Octave version recorded")
        info("asi     acceptance %.3f | zeta_final %.4f | R-hat(log posterior) %.3f | mean model size %.2f | Octave call %.1f s = sampler %.1f s + startup/io %.2f s",
             r$extra$accept_final, r$extra$zeta_final, r$extra$rhat_logpost, r$extra$mean_model_size,
             r$extra$octave_call_sec, r$extra$sampler_sec, r$extra$octave_startup_io_sec)
      }
      if (m == "bas_mc3") check(tg1("modelprior") == "author" && tg1("prior") == "author" && tg1("alpha") == "author" &&
                                  identical(r$settings$prior$value, "ZS-null") && identical(r$settings$modelprior$value, "beta.binomial(1, 1)"),
                                paste0("bas_mc3: prior ZS-null and modelprior beta.binomial(1, 1), the bas.lm defaults, tagged author in suite ", suite))
      if (m == "bas_mc3") check(isTRUE(all.equal(r$extra$json_summary$iid_se_at_pip_half, sqrt(0.25 / r$extra$json_summary$recorded_states))) &&
                                  is.null(r$extra$json_summary$mc_se_at_pip_half_lower_bound) &&
                                  r$extra$json_summary$mh_steps_total == 180000 && r$extra$json_summary$recorded_states == 180000 &&
                                  r$extra$json_summary$burnin_steps_in_average == 60000L && identical(r$extra$json_summary$burn_in_discarded, FALSE),
                                "bas_mc3: 120000 + 60000 = 180000 MH steps, all recorded (thin 1); the 60000 burn-in steps are recorded as part of the average")
      if (m == "susie") check(r$settings$L$value == 20L && tg1("L") == "OURS" &&
                                isTRUE(all.equal(r$settings$residual_variance_lowerbound$value, var(d$y) / 1e4)) &&
                                identical(r$settings$residual_variance_upperbound$value, "Inf") && grepl("0.4.29", r$software$paper_version),
                              paste0("susie: L = 20 (OURS) in suite ", suite, "; residual-variance bounds var(y)/1e4 and Inf recorded; paper version 0.4.29 noted"))
    }
    S <- d$support
    if (is.numeric(r$pip)) {
      tp <- length(intersect(r$selected, S)); fp <- length(setdiff(r$selected, S))
      info("%-7s runtime %7.1f s | |sel| %2d TP %2d FP %2d exact %-5s | PIP: min signal %.3f, max null %.3f, sum %.2f",
           m, r$runtime_sec, length(r$selected), tp, fp, identical(r$selected, as.integer(S)),
           min(r$pip[S]), max(r$pip[-S]), sum(r$pip))
      js <- r$extra$json_summary
      info("%-7s %s", m, paste(sprintf("%s=%s", names(js), vapply(js, function(v) format(v, digits = 4), "")), collapse = " "))
      if (length(r$extra$warnings)) info("%-7s warnings: %s", m, paste(r$extra$warnings, collapse = " | "))
      # sum(PIP) = posterior expected model size; exactly 0 is legitimate for SuSiE (all prior variances estimated 0)
      check(sum(r$pip) >= 0 && sum(r$pip) < 60, paste(m, "sanity: 0 <= sum(PIP) < 60"))
      if (grepl("^S1-like.*SNR=3$", cn) && m %in% c("bas_mc3", "asi"))
        check(identical(r$selected, as.integer(S)), paste(m, "sanity: exact support at the strong S1-like case"))
      if (grepl("^S1 full", cn)) info("%-7s FULL SIZE n=1000 p=5000: runtime %.1f s, R process peak RSS so far %.0f MB%s", m, r$runtime_sec, peak_rss_mb(),
                                      if (m == "asi") " (the Octave process is separate and not included)" else "")
    }
  }
}

if (length(case_rx)) {                                      # --cases: section 1 only
  cat(sprintf("\n== done (--cases, section 1 only): %d check(s) failed; process peak RSS %.0f MB ==\n", n_fail, peak_rss_mb()))
  quit(status = if (n_fail == 0L) 0L else 1L)
}

# =============================================================================
# 2. Fidelity: adapter output == the authors' own function, called directly
# =============================================================================
cat("\n== fidelity: adapter vs direct call of the authors' function ==\n")
d <- cases[["S1-like n=200 p=500 rho=.6 SNR=3"]]; X <- d$X; y <- d$y; p <- ncol(X)
if ("bas_mc3" %in% names(methods)) {
  s <- mseed(d$data_seed, 4L); SEEDKIND(s)
  n <- nrow(X)
  Xsc <- scale(X); ysc <- as.numeric(scale(y, scale = FALSE))          # the adapter's preprocessing (PRE)
  # THE CALL of fit_bas_mc3.R: no prior, alpha or modelprior argument (owner's option (A): package defaults)
  ref <- suppressWarnings(BAS::bas.lm(ysc ~ Xsc, method = "MCMC", MCMC.iterations = 120000, burnin.iterations = 60000))
  r <- results[["S1-like n=200 p=500 rho=.6 SNR=3 bas_mc3"]]
  check(identical(as.numeric(ref$probne0[-1]), r$pip),
        "bas_mc3: pip identical to bas.lm(method = \"MCMC\", MCMC.iterations = 120000, burnin.iterations = 60000), all else default, on scale(X), centred y")
  vb <- function(nm) r$settings[[nm]]
  fmb <- formals(BAS::bas.lm); mpd <- eval(fmb$modelprior, envir = asNamespace("BAS"))
  check(identical(eval(fmb$prior), "ZS-null") && identical(mpd$family, "Beta-Binomial") && identical(as.numeric(mpd$hyper.parameters), c(1, 1)) &&
          is.null(eval(fmb$alpha)) && identical(as.character(ref$prior), "ZS-null") && identical(ref$modelprior$family, "Beta-Binomial"),
        "bas_mc3: the installed bas.lm has defaults prior = \"ZS-null\", modelprior = beta.binomial(1, 1), alpha = NULL, and the direct fit used them")
  check(identical(vb("prior")$value, "ZS-null") && vb("prior")$tag == "author" && vb("alpha")$tag == "author" &&
          identical(vb("modelprior")$value, "beta.binomial(1, 1)") && vb("modelprior")$tag == "author" &&
          grepl("NOT the ASI", vb("prior")$source) && grepl("NOT the ASI", vb("modelprior")$source),
        "bas_mc3: default run records prior ZS-null and modelprior beta.binomial(1, 1) (bas.lm defaults, author) and states that this is not the ASI prior")
  dsrc <- function(nm) paste0("author (bas.lm ", as.character(packageVersion("BAS")), " default): formals(bas.lm)$", nm, " = ", paste(deparse(fmb[[nm]]), collapse = " "))
  dn <- c("prior", "alpha", "modelprior", "include.always", "update", "prob.rw")
  check(all(vapply(dn, function(nm) vb(nm)$tag == "author" && startsWith(vb(nm)$source, dsrc(nm)), NA)) &&
          identical(vb("include.always")$value, "~1") && identical(vb("update")$value, "NULL") && identical(vb("prob.rw")$value, 0.5) &&
          isTRUE(all.equal(vb("alpha")$value, as.numeric(ref$alpha))) && !any(c("prior", "alpha", "modelprior", "include.always", "update", "prob.rw") %in% names(ref$call)),
        "bas_mc3: prior, alpha, modelprior, include.always, update, prob.rw are recorded as author (bas.lm default), each source quoting formals(bas.lm); none is passed in the direct call")
  info("bas_mc3 shipped defaults as recorded: %s", paste(vapply(dn, function(nm) sprintf("%s = %s", nm, format(vb(nm)$value)), ""), collapse = "; "))
  check(vb("MCMC.iterations")$value == 120000L && vb("burnin.iterations")$value == 60000L &&
          vb("MCMC.iterations")$tag == "OURS" && vb("burnin.iterations")$tag == "OURS" &&
          grepl("ADS alg_par", vb("MCMC.iterations")$source) && grepl("does not discard burn-in", vb("burnin.iterations")$source) &&
          vb("thin")$value == 1L && vb("thin")$tag == "author" && identical(vb("pivot")$value, TRUE) && vb("pivot")$tag == "author" &&
          identical(eval(fmb$thin), 1) && identical(eval(fmb$pivot), TRUE),
        "bas_mc3: run length 120000 / 60000 tagged OURS (repo ADS alg_par; burn-in not discarded); thin = 1 and pivot = TRUE are bas.lm's own defaults, tagged author")
  SEEDKIND(s)                                              # the same fit on the RAW input: bas.lm centres X itself, ZS-null is scale-free
  refraw <- suppressWarnings(BAS::bas.lm(y ~ X, method = "MCMC", MCMC.iterations = 120000, burnin.iterations = 60000))
  info("bas_mc3 preprocessing: max |PIP(scaled input) - PIP(raw input)| = %.3g (the ZS-null prior is scale-free; any change comes from rounding in the MH steps)",
       max(abs(as.numeric(refraw$probne0[-1]) - r$pip)))
  SEEDKIND(s)                                              # ctrl overrides reach bas.lm unchanged
  ovr <- list(MCMC.iterations = 20000L, burnin.iterations = 5000L, thin = 5L, pivot = FALSE)
  refo <- suppressWarnings(BAS::bas.lm(ysc ~ Xsc, method = "MCMC",
                                       MCMC.iterations = 20000L, burnin.iterations = 5000L, thin = 5L, pivot = FALSE))
  ro <- methods$bas_mc3$f(X, y, s, ovr)
  check(identical(ro$extra$status, "ok") && identical(as.numeric(refo$probne0[-1]), ro$pip) &&
          all(vapply(c("MCMC.iterations", "burnin.iterations", "thin", "pivot"), function(nm) ro$settings[[nm]]$tag, "") == "OURS") &&
          ro$extra$json_summary$recorded_states == 5000,
        "bas_mc3: ctrl$MCMC.iterations, burnin.iterations, thin, pivot reach bas.lm unchanged and are tagged OURS")
  SEEDKIND(s)                                              # OFF by default: the earlier call matched to the ASI prior stays reachable through ctrl
  refg <- suppressWarnings(BAS::bas.lm(ysc ~ Xsc, method = "MCMC", prior = "g-prior", alpha = 9 * (n - 1),
                                       modelprior = BAS::Bernoulli(probs = 10 / p),
                                       MCMC.iterations = 120000, burnin.iterations = 60000))
  rg <- methods$bas_mc3$f(X, y, s, list(prior = "g-prior", alpha = 9 * (n - 1), h = 10 / p))
  check(identical(rg$extra$status, "ok") && identical(as.numeric(refg$probne0[-1]), rg$pip) &&
          identical(rg$settings$prior$value, "g-prior") && isTRUE(all.equal(rg$settings$alpha$value, 9 * (n - 1))) &&
          identical(rg$settings$modelprior$value, sprintf("Bernoulli(probs = %.10g)", 10 / p)) &&
          all(vapply(c("prior", "alpha", "modelprior"), function(nm) rg$settings[[nm]]$tag, "") == "OURS"),
        "bas_mc3: ctrl$prior, ctrl$alpha, ctrl$h reach bas.lm unchanged (g-prior 9(n-1), Bernoulli(10/p)) and are tagged OURS")
  info("bas_mc3 prior sensitivity (strong S1-like case): defaults (ZS-null, beta.binomial(1,1)) select {%s}, sum(PIP) %.2f; g-prior 9(n-1) + Bernoulli(10/p) select {%s}, sum(PIP) %.2f; max |PIP difference| %.3f",
       paste(r$selected, collapse = ","), sum(r$pip), paste(rg$selected, collapse = ","), sum(rg$pip), max(abs(r$pip - rg$pip)))
  rb <- methods$bas_mc3$f(X, y, s, list(h = 1.5))
  check(grepl("^failed: ctrl\\$h must lie in", rb$extra$status), "bas_mc3 / ctrl$h = 1.5 -> failed status, no error")

  # seed sensitivity of the default call (information only; no threshold): the same data, three method seeds
  for (cn2 in c("S1-like n=200 p=500 rho=.6 SNR=3", grep("^S2", names(cases), value = TRUE))) {
    d2 <- cases[[cn2]]
    pp <- sapply(0:2, function(k) {
      rk <- methods$bas_mc3$f(d2$X, d2$y, mseed(d2$data_seed, 4L) + k, list(suite = if (grepl("^S2", cn2)) "S2" else "S1"))
      if (is.numeric(rk$pip)) rk$pip else rep(NA_real_, ncol(d2$X))
    })
    info("bas_mc3 seed sensitivity, %s: sum(PIP) over 3 method seeds = %s; max over variables of the PIP range = %.3f; selections {%s}",
         cn2, paste(sprintf("%.2f", colSums(pp)), collapse = ", "), max(apply(pp, 1, function(v) diff(range(v)))),
         paste(apply(pp, 2, function(v) paste(which(v > 0.5), collapse = ",")), collapse = "} {"))
  }
}
if ("susie" %in% names(methods)) {
  s <- mseed(d$data_seed, 6L); SEEDKIND(s)
  Xsc <- scale(X); ysc <- as.numeric(scale(y, scale = FALSE))          # the adapter's preprocessing (PRE)
  ref <- susieR::susie(Xsc, ysc, L = 20)
  r <- results[["S1-like n=200 p=500 rho=.6 SNR=3 susie"]]
  check(identical(as.numeric(ref$pip), r$pip), "susie: pip identical to susie(scale(X), centred y, L = 20)$pip")
  check(identical(r$settings$standardize$value, TRUE) && identical(r$settings$intercept$value, TRUE) &&
          r$settings$standardize$tag == "author" && r$settings$preprocess$tag == "OURS",
        "susie: standardize = TRUE and intercept = TRUE (susie defaults, author) recorded next to the preprocessing (OURS)")
  for (cn in names(cases)[1:4]) {                         # susie's own standardize/intercept make the preprocessing a no-op
    dd <- cases[[cn]]
    raw <- susieR::susie(dd$X, dd$y, L = 20)
    dmax <- max(abs(as.numeric(raw$pip) - results[[paste(cn, "susie")]]$pip))
    check(dmax < 1e-6, sprintf("susie preprocessing, %s: PIPs equal those of susie() on the raw input (max difference %.2g)", cn, dmax))
  }
  for (cn in names(cases)[1:4]) {                         # L sensitivity, information only
    dd <- cases[[cn]]
    r10 <- methods$susie$f(dd$X, dd$y, mseed(dd$data_seed, 6L), list(L = 10))
    r20 <- results[[paste(cn, "susie")]]
    info("susie L sensitivity, %s: L=20 selects {%s}; L=10 (package default) selects {%s}", cn,
         paste(r20$selected, collapse = ","), paste(r10$selected, collapse = ","))
  }
}
if ("asi" %in% names(methods)) {
  s <- mseed(d$data_seed, 5L)
  n <- nrow(X)
  octave <- file.path(OCT_HOME, "bin", "octave-cli")
  mfile <- file.path(ASI_DIR, "ASI_sampler.m")
  # the sampler file: pinned sha256, identical to the owner's supplement copy, 18 arguments
  check(identical(unname(tools::sha256sum(mfile)), ASI_SHA) && identical(unname(tools::sha256sum(file.path(ASI_SUPP, "ASI_sampler.m"))), ASI_SHA),
        "asi: ASI_sampler.m has the pinned sha256, in the copy that runs and in the owner's supplement copy")
  l1 <- readLines(mfile, n = 1L, warn = FALSE)
  check(identical(trimws(l1), "function [output] = ASI_sampler(data_fixed, data, target, g, gprior, mode, RB_adap, RB, hparam, tau, nu, burnin, numbofits, thin, numbofreps, heat, adap_type, updateg)"),
        "asi: line 1 of ASI_sampler.m is the 18-argument signature the driver calls")
  drv <- readLines(file.path(here, "asi_octave", "run_asi.m"), warn = FALSE)
  code <- drv[!grepl("^\\s*%", drv)]
  call_txt <- gsub("\\s+|\\.\\.\\.", "", paste(code[grep("output = ASI_sampler\\(", code) + 0:1], collapse = ""))
  check(identical(call_txt, "output=ASI_sampler(data_fixed,data,target,P.g,P.gprior,P.mode,P.RB_adap,P.RB,P.hparam,P.tau,P.nu,P.burnin,P.numbofits,P.thin,P.numbofreps,P.heat,P.adap_type,P.updateg);"),
        "asi: the driver passes the 18 arguments in the order of the signature, each from params.txt")
  check(identical(list.files(file.path(here, "asi_octave"), pattern = "\\.m$", recursive = TRUE), "run_asi.m"),
        "asi: asi_octave/ holds the driver run_asi.m only (no shim, no copy of the sampler)")

  # direct call, independent of the adapter's driver: the test writes the data itself and calls ASI_sampler with literal arguments
  ra <- methods$asi$f(X, y, s, asi_quick)
  wd <- tempfile(pattern = paste0("asi_test_", Sys.getpid(), "_"), tmpdir = TMP_ROOT); dir.create(wd, mode = "0700")
  Xsc <- scale(X); ysc <- as.numeric(scale(y, scale = FALSE))          # the adapter's preprocessing (PRE)
  con <- file(file.path(wd, "X.bin"), "wb"); writeBin(as.double(Xsc), con, size = 8L); close(con)
  con <- file(file.path(wd, "y.bin"), "wb"); writeBin(as.double(ysc), con, size = 8L); close(con)
  prog <- sprintf(paste0(
    "addpath('%s'); fid = fopen('%s/X.bin'); data = fread(fid, [%d, %d], 'double'); fclose(fid); ",
    "fid = fopen('%s/y.bin'); target = fread(fid, [%d, 1], 'double'); fclose(fid); ",
    "rand('state', %d); randn('state', %d); ",
    "o = ASI_sampler(zeros(%d, 0), data, target, 9, 0, 1, 1, 1, 10/%d, 0.2, 1, 100, 200, 1, 25, 1, 1, 0); ",
    "fid = fopen('%s/pip.bin', 'w'); fwrite(fid, o.prob_inclusion(:), 'double'); fclose(fid); ",
    "fid = fopen('%s/nargin.txt', 'w'); fprintf(fid, '%%d\\n', nargin('ASI_sampler')); fclose(fid);"),
    ASI_DIR, wd, n, p, wd, n, s, s, n, p, wd, wd)
  rc <- system2(octave, c("--norc", "--no-history", "--quiet", "--no-window-system", "--eval", shQuote(prog)),
                stdout = file.path(wd, "out.log"), stderr = file.path(wd, "err.log"),
                env = c(paste0("OCTAVE_HOME=", shQuote(OCT_HOME)), "OMP_NUM_THREADS=1", "OPENBLAS_NUM_THREADS=1"))
  ref <- if (identical(as.integer(rc), 0L) && file.exists(file.path(wd, "pip.bin"))) readBin(file.path(wd, "pip.bin"), "double", n = p + 1L, size = 8L) else NULL
  check(identical(ra$extra$status, "ok") && !is.null(ref) && identical(ref, ra$pip),
        "asi: pip identical to a direct Octave call ASI_sampler(zeros(n,0), scale(X), y - mean(y), 9, 0, 1, 1, 1, 10/p, 0.2, 1, 100, 200, 1, 25, 1, 1, 0), same seed")
  check(identical(trimws(readLines(file.path(wd, "nargin.txt"), warn = FALSE)), "18"), "asi: Octave reports nargin('ASI_sampler') = 18")
  outl <- readLines(file.path(wd, "out.log"), warn = FALSE)
  check(any(grepl("^fixed = 1", outl)) && any(grepl("^it = 300", outl)) && any(grepl("^tau = 0.2", outl)),
        "asi: the sampler's own printed output shows fixed = 1 (h fixed), tau = 0.2 and the last iteration 300")
  unlink(wd, recursive = TRUE)

  # determinism (same seed, two separate Octave processes) and seed dependence
  rb <- methods$asi$f(X, y, s, asi_quick)
  check(identical(ra$pip, rb$pip) && identical(ra$extra$zeta_final, rb$extra$zeta_final) && identical(ra$extra$accept_final, rb$extra$accept_final),
        "asi determinism: the same method_seed in two separate Octave runs gives identical PIPs, final zeta and acceptance rate")

  # default settings, on a 40 x 30 problem (cheap at the default run length)
  Xd <- X[1:40, 1:30]; yd <- y[1:40]
  rdef <- methods$asi$f(Xd, yd, s, list(suite = "S1"))
  v <- function(nm) rdef$settings[[nm]]$value; tg <- function(nm) rdef$settings[[nm]]$tag; sr <- function(nm) rdef$settings[[nm]]$source
  check(identical(rdef$extra$status, "ok") &&
          identical(c(v("g"), v("gprior"), v("mode"), v("RB_adap"), v("RB"), v("tau"), v("nu"), v("burnin"), v("numbofits"), v("thin"), v("numbofreps"), v("heat"), v("adap_type"), v("updateg")),
                    c(9, 0, 1, 1, 1, 0.2, 1, 2000, 4000, 1, 25, 1, 1, 0)) && isTRUE(all.equal(v("hparam"), 10 / 30)) && identical(v("data_fixed"), "zeros(n, 0)"),
        "asi defaults: data_fixed = zeros(n,0), g = 9, gprior = 0, mode = 1, RB_adap = 1, RB = 1, hparam = 10/p, tau = 0.2, nu = 1, burnin = 2000, numbofits = 4000, thin = 1, numbofreps = 25, heat = 1, adap_type = 1, updateg = 0")
  REPO <- "authors' repo R/simulation/simulation_example.R @3b95d66; not stated in the Biometrika text"
  check(all(vapply(c("g", "gprior", "mode", "RB_adap", "RB", "hparam", "tau", "nu", "burnin", "numbofits", "thin", "numbofreps", "heat", "adap_type"), tg, "") == "author") &&
          all(vapply(c("tau", "burnin", "numbofits", "numbofreps"), function(nm) grepl(REPO, sr(nm), fixed = TRUE), TRUE)) &&
          grepl("^paper", sr("g")) && grepl("^paper", sr("hparam")) && grepl("instructions.pdf", sr("gprior")) && grepl("run scripts", sr("nu")) &&
          tg("data_fixed") == "OURS" && tg("updateg") == "OURS" && tg("preprocess") == "OURS" && tg("seed") == "OURS",
        "asi defaults (suite S1): every argument has a source (paper / instructions.pdf / run scripts / repo); tau, burnin, numbofits, numbofreps cite the repo script; data_fixed, updateg, preprocessing, seed are OURS")
  check(rdef$extra$json_summary$recorded_draws == 4000 * 25 && rdef$extra$json_summary$iterations_total == 6000 &&
          v("kappa") == 1e-4 && isTRUE(all.equal(v("eps"), 0.1 / 30)) && isTRUE(all.equal(v("zeta_start"), 0.1)),
        "asi defaults: 6000 iterations, PIP over 4000 x 25 recorded draws; the code's own kappa = 0.0001, eps = 0.1/p, zeta start 0.1 are recorded")
  info("asi default-length fit on the 40 x 30 problem: Octave call %.1f s (sampler %.1f s, startup/io %.2f s); acceptance %.3f; zeta_final %.4f",
       rdef$extra$octave_call_sec, rdef$extra$sampler_sec, rdef$extra$octave_startup_io_sec, rdef$extra$accept_final, rdef$extra$zeta_final)

  # ctrl overrides reach the sampler and are tagged OURS
  rt <- methods$asi$f(X, y, s, c(small, list(tau = 0.25, adap_type = 0)))
  check(identical(rt$extra$status, "ok") && rt$settings$tau$value == 0.25 && rt$settings$tau$tag == "OURS" &&
          rt$settings$adap_type$value == 0 && rt$settings$adap_type$tag == "OURS" && rt$settings$numbofreps$value == 5 && rt$settings$numbofreps$tag == "OURS",
        "asi: ctrl$tau, ctrl$adap_type, ctrl$numbofreps reach ASI_sampler and are tagged OURS")
  left <- list.files(TMP_ROOT, pattern = paste0("^asi_octave_", Sys.getpid(), "_"))
  check(length(left) == 0L, "asi: no temporary directory of this process is left under _local/tmp")
}

# =============================================================================
# 3. Randomness comes only from method_seed
# =============================================================================
cat("\n== seeds ==\n")
ctrl_of <- list(bas_mc3 = list(), asi = small, susie = list())
for (m in names(methods)) {
  f <- methods[[m]]$f; s <- mseed(d$data_seed, methods[[m]]$code)
  set.seed(1);   a <- f(X, y, s, ctrl_of[[m]])
  set.seed(999); invisible(runif(17)); b <- f(X, y, s, ctrl_of[[m]])
  check(identical(a$pip, b$pip) && identical(a$selected, b$selected),
        paste(m, "same method_seed, different global RNG state -> identical pip"))
  e2 <- f(X, y, s, c(ctrl_of[[m]], list(suite = "S2", setting_id = "S2_001")))     # ctrl as the harness passes it
  check(identical(a$pip, e2$pip) && identical(e2$settings$suite$value, "S2"),
        paste(m, "ctrl$suite (and the harness's ctrl$setting_id) change the tags only, never the fit"))
  if (m != "susie") {
    c2 <- f(X, y, s + 1, ctrl_of[[m]])
    check(!identical(a$pip, c2$pip), paste(m, "different method_seed -> different MCMC draws"))
  }
}

# =============================================================================
# 4. Never error: bad input and broken set-up give status 'failed: ...'
# =============================================================================
cat("\n== failure paths (must return, not error) ==\n")
Xs <- X[1:40, 1:30]; ys <- y[1:40]
bad <- list(
  "NA in X"            = function(f) { Xb <- Xs; Xb[1, 1] <- NA; f(Xb, ys, 1) },
  "length(y) != n"     = function(f) f(Xs, ys[-1], 1),
  "X not a matrix"     = function(f) f(as.data.frame(Xs), ys, 1),
  "bad method_seed"    = function(f) f(Xs, ys, NA),
  "constant column"    = function(f) { Xb <- Xs; Xb[, 3] <- 1; f(Xb, ys, 1) },
  "missing Octave"     = function(f) f(Xs, ys, 1, list(octave_home = "/nonexistent")),
  "missing sampler"    = function(f) f(Xs, ys, 1, list(sampler_dir = "/nonexistent")),
  "missing tmp root"   = function(f) f(Xs, ys, 1, list(tmp_root = "/nonexistent"))
)
for (m in names(methods)) for (bn in names(bad)) {
  if (grepl("^missing ", bn) && m != "asi") next
  r <- tryCatch(bad[[bn]](methods[[m]]$f), error = function(e) NULL)
  check(!is.null(r) && identical(names(r), NAMES) && grepl("^failed: ", r$extra$status) &&
          identical(r$selected, integer(0)) && is.null(r$pip),
        sprintf("%s / %s -> %s", m, bn, if (is.null(r)) "ERROR" else substr(r$extra$status, 1, 70)))
}
if ("asi" %in% names(methods)) {                            # an edited sampler file must be refused
  tmp <- file.path(dirname(dirname(dirname(dirname(here)))), ".rc_tmp", "fableB", "fake_asi")
  unlink(tmp, recursive = TRUE); dir.create(tmp, recursive = TRUE)
  file.copy(file.path(ASI_DIR, "ASI_sampler.m"), file.path(tmp, "ASI_sampler.m"))
  r <- methods$asi$f(Xs, ys, 1, c(small, list(sampler_dir = tmp)))
  check(identical(r$extra$status, "ok"), "asi / byte-identical copy of ASI_sampler.m in another folder -> runs")
  cat("\n% edited\n", file = file.path(tmp, "ASI_sampler.m"), append = TRUE)
  r <- methods$asi$f(Xs, ys, 1, c(small, list(sampler_dir = tmp)))
  check(grepl("^failed: ASI_sampler.m differs from the pinned file", r$extra$status), "asi / edited ASI_sampler.m -> refused (sha256 pin)")
  unlink(tmp, recursive = TRUE)
  r <- methods$asi$f(Xs, ys, 1, c(small, list(adap_type = 2)))
  check(grepl("^failed: adap_type must be", r$extra$status), "asi / ctrl$adap_type = 2 (documented in instructions.pdf, broken in the code) -> refused")
  left <- list.files(TMP_ROOT, pattern = paste0("^asi_octave_", Sys.getpid(), "_"))
  check(length(left) == 0L, "asi: no temporary directory is left after the failure paths")
}
# small-p edge: h = 10/p needs p > 10 (ASI); bas_mc3 has no such limit under the package defaults
if ("asi" %in% names(methods)) {
  r <- tryCatch(methods$asi$f(Xs[, 1:8], ys, 1), error = function(e) NULL)
  check(!is.null(r) && grepl("^failed: ", r$extra$status), "asi / p = 8 (h = 10/p > 1) -> failed status, no error")
}
if ("bas_mc3" %in% names(methods)) {
  r <- tryCatch(methods$bas_mc3$f(Xs[, 1:8], ys, 1, list(MCMC.iterations = 2000L, burnin.iterations = 500L)), error = function(e) NULL)
  check(!is.null(r) && identical(r$extra$status, "ok") && length(r$pip) == 8L, "bas_mc3 / p = 8 -> ok (the package-default model prior needs no p > 10)")
}

cat(sprintf("\n== done: %d check(s) failed; process peak RSS %.0f MB ==\n", n_fail, peak_rss_mb()))
quit(status = if (n_fail == 0L) 0L else 1L)
