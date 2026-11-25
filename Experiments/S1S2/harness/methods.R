# methods.R -- registry: method name -> adapter file (relative to Experiments/S1S2), fit function, method_code.
# PROVENANCE: INTERFACE.md "Seeds" (method_code) and "Folder tree" (adapter paths). No statistical content.
S1S2_METHODS <- list(
  smcbvs   = list(file = "smc/fit_smcbvs.R",                       fun = "fit_smcbvs",   code = 1L, kind = "bayes"),
  lasso_cv = list(file = "benchmarks/frequentist/fit_lasso_cv.R",  fun = "fit_lasso_cv", code = 2L, kind = "freq"),
  scad     = list(file = "benchmarks/frequentist/fit_scad.R",      fun = "fit_scad",     code = 3L, kind = "freq"),
  bas_mc3  = list(file = "benchmarks/bayesian/fit_bas_mc3.R",      fun = "fit_bas_mc3",  code = 4L, kind = "bayes"),
  asi      = list(file = "benchmarks/bayesian/fit_asi.R",          fun = "fit_asi",      code = 5L, kind = "bayes"),
  susie    = list(file = "benchmarks/bayesian/fit_susie.R",        fun = "fit_susie",    code = 6L, kind = "bayes")
)
S1S2_ROOT <- "/home/fb31/Bayesian-Variable-Selection/_local/engineering"
S1S2_RUNS <- file.path(S1S2_ROOT, "runs", "S1S2")

method_seed_of <- function(data_seed, method) data_seed + 10000000 * S1S2_METHODS[[method]]$code
method_available <- function(method, base) file.exists(file.path(base, S1S2_METHODS[[method]]$file))
load_method <- function(method, base) {
  m <- S1S2_METHODS[[method]]
  if (is.null(m)) stop("unknown method ", method)
  env <- new.env(parent = globalenv())
  sys.source(file.path(base, m$file), envir = env, chdir = TRUE)
  get(m$fun, envir = env)
}
