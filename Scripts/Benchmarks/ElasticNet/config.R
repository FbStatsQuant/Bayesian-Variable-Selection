# config.R -- constants for benchmark F2 (Elastic net), bench20261019.
# Master: 01_Methodology_and_Theory/MASTER_Methodology_and_Plan/MASTER_Methodology_and_Plan.md,
# §III.3.0 (configuration and code layout) and §III.3.1 d, §III.3.2 d (parameter tables).
# This file holds only the blocks F2 uses (COMMON, GRID, GLMNET, F2) and the F2 row of METHODS.
# A later step merges the per-method config files into code/R/config.R.
# Sourcing this file defines constants only. No constant here is derived from the data-generating parameters (§III.3.9).

# Study-wide scalars (§III.3.0).
METHOD_SEED_OFFSET <- 4000000L
PIP_THRESHOLD <- 0.5
TEST_SEED <- 20261019L

COMMON <- list(
  study = "bench20261019",
  study_root = "/projects/ml75/fb31/BVS/bench20261019",
  study_lib = "/projects/ml75/fb31/BVS/bench20261019/lib/R452",
  n = 200L,
  intercept = FALSE,            # §II.8: no intercept
  standardize = FALSE,          # X is already centred and scaled (sd, n - 1)
  nfolds = 10L,                 # common folds, 10 x 20 (§II.9)
  min_fold_size = 3L,           # §III.3.1 e step 1
  kmax_ebic = 100L,             # EBIC candidate cap = floor(n/2) (§III.3.0)
  ebic_gamma = c(ebic1 = 1, ebic05 = 0.5, bic = 0),  # F2 uses ebic1 and ebic05
  ols_tol = 1e-10,              # lm.fit rank tolerance (Oct-14)
  design_tol = 1e-10,           # centring / unit-sd tolerance (Oct-14 design_tolerance)
  support_zero_tol = 0,         # support = exactly nonzero coefficients
  scale_keys = c(c100 = 1, c075 = 0.75, c050 = 0.50, c035 = 0.35, c025 = 0.25)
)

GRID <- list(
  nlambda = 200L,               # λ grid length (Oct-14)
  min_ratio = 1e-4,             # λ grid ratio (Oct-14)
  max_mult = 1.01               # first point strictly gives the null model
)

GLMNET <- list(
  type_gaussian = "naive",
  thresh = 1e-16,
  maxit = 1e7,                  # lead decision 2026-10-19 (master G6 action; 1e6 hit jerr < 0 on S5 dev cases)
  fdev = 0,
  devmax = 1,
  lambda_rel_tol = 1e-12,
  kkt_rel_tol = 1e-5,
  pkg_version = "5.1"
)

F2 <- list(
  alphas = c(.1, .25, .5, .75, .9),   # target α grid (O8)
  ties = "alpha_desc_lambda_desc"     # exact cvm ties: largest α, then largest λ
)

# Method registry (§III.3.0): only the F2 row here.
METHODS <- data.frame(
  method_id = "F2",
  fn = "fit_F2_enet",
  variant = "primary",
  method_label = "Elastic net",
  package = "glmnet",
  pkg_version = "5.1",
  tier = "primary",
  stringsAsFactors = FALSE
)
METHODS$rule_ids <- list(c("cv_min", "cv_1se", "ebic1", "ebic05"))
METHODS$roles    <- list(c("primary", "S0", "S0", "S0"))

# The settings list passed to every wrapper: the whole configuration plus settings$variant.
make_settings <- function(variant = "primary") {
  list(COMMON = COMMON, GRID = GRID, GLMNET = GLMNET, F2 = F2, METHODS = METHODS,
       METHOD_SEED_OFFSET = METHOD_SEED_OFFSET, PIP_THRESHOLD = PIP_THRESHOLD,
       TEST_SEED = TEST_SEED, variant = variant)
}
