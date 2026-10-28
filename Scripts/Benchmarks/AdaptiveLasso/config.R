# config.R: all constants for benchmark F3 (adaptive lasso), n = 200 benchmark study.
# Implements master §III.3.0 ("Configuration and code layout", "Method registry"),
# §III.3.1 d (COMMON, GRID, GLMNET) and §III.3.3 d/k (F3). Frozen before the pilot.
# This folder holds only the blocks F3 uses; the other methods' blocks live in their
# own folders and are merged later. Sourcing this file computes nothing.

# Study-wide scalars (§III.3.0).
METHOD_SEED_OFFSET <- 4000000L
PIP_THRESHOLD <- 0.5
TEST_SEED <- 20261019L

# Sealed study library (§III.3.0 "Library"; gate G1).
STUDY_LIB <- "/projects/ml75/fb31/BVS/bench20261019/lib/R452"

COMMON <- list(
  n = 200L,
  nfolds = 10L,
  min_fold_rows = 3L,            # §III.3.1 e step 1: each fold label has at least 3 rows
  intercept = FALSE,
  standardize = FALSE,
  kmax_ebic = 100L,              # EBIC candidate cap = floor(n/2) (§III.3.0)
  ebic_gamma = c(ebic1 = 1, ebic05 = 0.5, bic = 0),  # F3 uses ebic1 and ebic05 only
  ols_tol = 1e-10,
  design_tol = 1e-10,
  support_zero_tol = 0           # support = exactly nonzero coefficients
)

GRID <- list(
  nlambda = 200L,
  min_ratio = 1e-4,
  max_mult = 1.01
)

GLMNET <- list(
  type_gaussian = "naive",
  thresh = 1e-16,
  maxit = 1e7,   # §IV.2.2 pre-declared action (was 1e6): dev fits hit jerr at 1e6; lead decision 2026-10-19
  fdev = 0,
  devmax = 1,
  lambda_rel_tol = 1e-12,
  kkt_rel_tol = 1e-5,
  pkg_version = "5.1"
)

F3 <- list(
  kappa = 10^seq(3, -6, length.out = 61),   # ridge pilot grid, decreasing
  kappa_ties = "larger",
  ridge_tol = 1e-7,
  gamma = 1,
  floor_abs = 1e-8,
  floor_rel = 1e-6
)

# Method registry (§III.3.0). One row per method id; list columns hold the registered
# rule ids and roles (order of §III.3.3 f) and the method's extra rule-row columns
# (§III.3.3 g), so that make_rule_rows() and fail_rows() always emit the same frame.
METHODS <- data.frame(
  method_id = "F3",
  fn = "fit_F3_alasso",
  variant = "primary",
  method_label = "Adaptive lasso",
  package = "glmnet",
  pkg_version = "5.1",
  tier = "primary",
  stringsAsFactors = FALSE
)
METHODS$rule_ids <- list(c("cv_min", "cv_1se", "ebic1", "ebic05"))
METHODS$roles <- list(c("primary", "S0", "S0", "S0"))
METHODS$extra_cols <- list(c("lambda", "cv_mean", "cv_se", "rss", "ebic1_value", "crit_value",
                             "index", "k_valid_max", "k_path_max", "kappa"))

# Closed vocabulary of diag_codes (§III.3.0 "Codes").
DIAG_FLAG_CODES <- c("kkt_path", "path_truncated", "L_saturated", "elbo_drop", "sigma2_floor",
                     "capped_intermediate", "tail_unstable", "fixed_point",
                     "ess_tau", "ess_ci95", "crn_mismatch")
DIAG_INFO_CODES <- c("lambda_first", "lambda_last", "alpha_edge", "kappa_edge",
                     "floored_selected", "ebic_at_largest")

# The settings list passed to every wrapper: the whole configuration plus the variant.
study_settings <- function(variant = "primary") {
  list(METHOD_SEED_OFFSET = METHOD_SEED_OFFSET, PIP_THRESHOLD = PIP_THRESHOLD,
       TEST_SEED = TEST_SEED, STUDY_LIB = STUDY_LIB,
       COMMON = COMMON, GRID = GRID, GLMNET = GLMNET, F3 = F3, METHODS = METHODS,
       DIAG_FLAG_CODES = DIAG_FLAG_CODES, DIAG_INFO_CODES = DIAG_INFO_CODES,
       variant = variant)
}
