# config.R -- constants for benchmark F1 (lasso), n = 200 BVS benchmark study.
# Implements master §III.3.0 ("Configuration and code layout", "Method registry and rule frame")
# and the F1 parameter table of §III.3.1 d. Frozen before the pilot; holds no data-derived numbers.
# Wrappers read every constant through `settings` (this whole list plus settings$variant).
# F1-only thread copy: only the blocks F1 uses (COMMON, GRID, GLMNET, F1) and the F1 registry row.

METHOD_SEED_OFFSET <- 4000000L     # §II.7: method seed = data seed + 4,000,000
PIP_THRESHOLD      <- 0.5          # §II.8 (unused by F1)
TEST_SEED          <- 20261019L    # seed for synthetic unit-test designs

COMMON <- list(
  n            = 200L,
  intercept    = FALSE,            # §II.8: no intercept
  standardize  = FALSE,            # X is already centred and scaled (sd with n - 1)
  nfolds       = 10L,              # common folds, 10 x 20 (§II.9)
  min_fold_rows = 3L,              # §III.3.1 e step 1: each fold label has at least 3 rows
  kmax_ebic    = 100L,             # EBIC candidate cap, floor(n/2) (§III.3.0)
  ebic_gamma   = c(ebic1 = 1, ebic05 = 0.5, bic = 0),
  ols_tol      = 1e-10,            # lm.fit rank tolerance (Oct-14)
  design_tol   = 1e-10,            # centring / unit-sd tolerance on X (Oct-14)
  support_zero_tol = 0,            # support = exactly nonzero coefficients
  # closed vocabulary of diag_codes (§III.3.0 "Codes"): flag codes, then informational codes
  flag_codes   = c("kkt_path", "path_truncated", "L_saturated", "elbo_drop", "sigma2_floor",
                   "tail_unstable", "fixed_point",
                   "ess_tau", "ess_ci95", "crn_mismatch"),
  info_codes   = c("lambda_first", "lambda_last", "alpha_edge", "kappa_edge",
                   "floored_selected", "ebic_at_largest", "capped_intermediate"),
  study        = "bench20261019",
  regime       = "H",
  scale_keys   = c(c100 = 1, c075 = 0.75, c050 = 0.50, c035 = 0.35, c025 = 0.25)
)

GRID <- list(
  nlambda   = 200L,                # λ grid length (Oct-14)
  min_ratio = 1e-4,                # last fraction of the grid (pilot action, §III.3.1 i)
  max_mult  = 1.01                 # first grid point = 1.01 * entry value (null model, strict)
)

GLMNET <- list(
  type_gaussian  = "naive",
  thresh         = 1e-16,          # passed through control = list(...), never top level
  maxit          = 1e7,            # passes, total over the path. Master §III.3.1 d had 1e6; raised to 1e7 by the
                                   # lead's decision of 2026-10-19 (the pre-declared action of §III.3.1 i: dev fold
                                   # fits needed up to 1.59e6 passes at thresh 1e-16, jerr -167/-198/-139 at 1e6)
  fdev           = 0,
  devmax         = 1,              # inert with a user grid (§III.3.1 e step 5); kept as a guard
  lambda_rel_tol = 1e-12,          # returned-λ relative tolerance
  kkt_rel_tol    = 1e-5,           # relative to max(1, max_j |X_j'y| / n_fit)
  pkg_version    = "5.1"
)

F1 <- list(
  alpha = 1                        # lasso
)

# Method registry (§III.3.0). One row per method id; this thread registers F1 only.
# `extra_cols` (the item-g extra columns, in output order) is an addition to the master's
# column list so that fail_rows() can emit the same columns as a successful fit (ASSUMPTIONS.md A3).
METHODS <- data.frame(
  method_id    = "F1",
  fn           = "fit_F1_lasso",
  variant      = "primary",
  method_label = "Lasso",
  package      = "glmnet",
  pkg_version  = "5.1",
  tier         = "primary",
  stringsAsFactors = FALSE
)
METHODS$rule_ids   <- list(c("cv_min", "cv_1se", "ebic1", "ebic05"))
METHODS$roles      <- list(c("primary", "S0", "S0", "S0"))
METHODS$extra_cols <- list(c("lambda", "cv_mean", "cv_se", "rss", "ebic1_value", "crit_value",
                             "index", "k_valid_max", "k_path_max"))
METHODS$converged_on_failure <- FALSE   # §III.3.0: a failed fit has converged = FALSE (NA for F5, A3)
