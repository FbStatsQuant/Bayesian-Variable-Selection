# config.R: frozen constants for benchmark F5 Best subset (ABESS), n = 200 study bench20261019.
# Implements master §III.3.0 ("Configuration and code layout", "Method registry and rule frame")
# and §III.3.5 d/k (MASTER_Methodology_and_Plan.md, revision of 2026-10-19).
# This thread's copy holds COMMON, F5 and the F5 row of METHODS only; the other method
# blocks are written by their own threads and merged later.
# No constant here is derived from the data-generating model (no-oracle rule, §III.3.9).

# ---- study-wide scalars (§III.3.0) ----
STUDY_ID           <- "bench20261019"
METHOD_SEED_OFFSET <- 4000000L        # §II.7: method seed = data seed + 4,000,000
PIP_THRESHOLD      <- 0.5
TEST_SEED          <- 20261019L
STUDY_LIB          <- "/projects/ml75/fb31/BVS/bench20261019/lib/R452"   # sealed study library (G1)

# ---- COMMON (§III.3.0; §III.3.1 d, conventions shared by F1-F5) ----
COMMON <- list(
  n             = 200L,
  intercept     = FALSE,
  standardize   = FALSE,
  nfolds        = 10L,
  min_fold_rows = 3L,          # §III.3.1 e step 1: each fold label has at least 3 rows
  kmax_ebic     = 100L,        # EBIC candidate cap, Regime H (= floor(n/2))
  ebic_gamma    = c(ebic1 = 1, ebic05 = 0.5, bic = 0),
  ols_tol       = 1e-10,       # lm.fit rank tolerance
  design_tol    = 1e-10,       # centring and sd-1 tolerance of the design
  support_zero_tol = 0         # supports are exactly nonzero coefficients
)

# ---- F5 Best subset (ABESS), §III.3.5 d and k ----
# list() keeps the named NULL element screening_num; the wrapper asserts it (§III.3.5 k).
F5 <- list(tune_path = "sequence", tune_type = "bic", sizes = 0:100, normalize = 0,
           fit_intercept = FALSE, lambda = 0, screening_num = NULL, c_max = 2L,
           max_splicing_iter = 100L, splicing_type = 2L, warm_start = TRUE,
           early_stop = FALSE, threads = 1L, seed = 1L, rss_rel_tol = 1e-7,
           stat_rel_tol = 1e-6, intercept_tol = 1e-12, pkg_version = "0.4.11")

# ---- Method registry (§III.3.0): this thread registers F5 only ----
METHODS <- data.frame(
  method_id    = "F5",
  fn           = "fit_F5_abess",
  variant      = "primary",
  method_label = "Best subset (ABESS)",
  package      = "abess",
  pkg_version  = "0.4.11",
  tier         = "primary",
  converged_na = TRUE,         # F5 has no convergence criterion: converged is always NA (§III.3.0)
  stringsAsFactors = FALSE)
METHODS$rule_ids <- list(c("ebic1", "ebic05", "bic"))     # order of §III.3.5 f
METHODS$roles    <- list(c("primary", "S0", "S0"))
# Method-specific extra rule-row columns (§III.3.5 g, plus k_path_max of §III.3.0 EBIC/BIC).
METHODS$extra_cols <- list(c("rss", "crit_value", "k_valid_max", "k_path_max"))
