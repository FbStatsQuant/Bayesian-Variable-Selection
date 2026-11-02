# config.R -- constants for benchmark A1 SuSiE (n = 200 BVS benchmark study, bench20261019).
# Implements master §III.3.0 (configuration layout, METHODS registry) and §III.3.6 (d) (A1 block).
# Only defines objects; sourcing it runs nothing else. No constant depends on the generating model.
# This file holds COMMON plus the A1 block and the A1 METHODS rows only (thread A1); the
# lead's merge step combines the per-method config files into code/R/config.R.

# Study-wide scalars (§III.3.0, §II.7, §II.8).
METHOD_SEED_OFFSET <- 4000000L
PIP_THRESHOLD <- 0.5
TEST_SEED <- 20261019L

COMMON <- list(
  STUDY = "bench20261019",
  STUDY_ROOT = "/projects/ml75/fb31/BVS/bench20261019",
  LIB = "/projects/ml75/fb31/BVS/bench20261019/lib/R452",
  N = 200L,
  N_FOLDS = 10L,
  REGIME = "H",
  SCALES = c(c100 = 1, c075 = 0.75, c050 = 0.50, c035 = 0.35, c025 = 0.25),
  DESIGN_TOL = 1e-10,      # Oct-14 design_tolerance: |colMeans| and |sd - 1|
  S0_MAX = 14L             # number of sel_a / pip_a columns in the schema (scoring only)
)

# A1 SuSiE, §III.3.6 (d). Names follow the `config.R` column of that table.
A1 <- list(
  PKG = "susieR",
  PKG_VERSION = "0.14.2",
  L = 50L,                     # n/4, capacity fixed from n
  L_S1 = 100L,                 # S1 variant SuSiE-L100 (n/2)
  SCALED_PRIOR_VAR = 0.2,
  RESID_VAR_INIT = NULL,       # sigma^2 starts at var(y)
  PRIOR_WEIGHTS = NULL,        # pi_j = 1/p
  NULL_WEIGHT = 0,
  STANDARDIZE = FALSE,
  INTERCEPT = FALSE,
  EST_RESID_VAR = TRUE,
  EST_PRIOR_VAR = TRUE,
  EST_PRIOR_METHOD = "optim",
  CHECK_NULL_THRESHOLD = 0,
  PRIOR_TOL = 1e-9,
  RESID_LB_DIVISOR = 1e4,      # residual_variance_lowerbound = var(y) / 1e4
  RESID_UB = Inf,
  S_INIT = NULL,
  COVERAGE = 0.95,
  MIN_ABS_CORR = 0.5,
  N_PURITY = 100L,
  UNIV_Z = FALSE,
  NA_RM = FALSE,
  MAX_ITER = 1000L,
  TOL = 1e-3,
  VERBOSE = FALSE,
  TRACK_FIT = FALSE,
  REFINE = FALSE,
  CS_V_THRESHOLD = 1e-9,       # hard-coded active-effect threshold of susie_get_cs (susie_utils.R l. 279)
  ELBO_DROP_TOL = 1e-6,        # elbo_drop flag; a drop beyond TOL fails the fit
  BFDR_Q = 0.1,
  BFDR_EPS_MULT = 64,
  ALPHA_TOP = 20L,             # saved alpha entries: 95% set members when |set| <= ALPHA_CS_MAX, else top 20
  ALPHA_CS_MAX = 100L,
  # S2 susie_auto (not registered, not run unless approved)
  AUTO_L_INIT = 1,
  AUTO_L_MAX = 512,
  AUTO_INIT_TOL = 1,
  AUTO_MAX_ITER = 100,
  AUTO_TOL = 1e-2,
  S2_RULE_IDS = "pip05",       # S2 fits emit pip05 with role S2 (they have no registry row)
  S2_ROLES = "S2"
)

# Method registry, §III.3.0: one row per method id (A1 thread: A1 and its S1 variant).
# rule_ids and roles are in the order of §III.3.6 (f).
METHODS <- data.frame(
  method_id = c("A1", "SuSiE-L100"),
  fn = c("fit_A1_susie", "fit_A1_susie"),
  variant = c("primary", "L100"),
  method_label = c("SuSiE (L = 50)", "SuSiE (L = 100)"),
  package = c("susieR", "susieR"),
  pkg_version = c("0.14.2", "0.14.2"),
  tier = c("primary", "S1"),
  stringsAsFactors = FALSE
)
METHODS$rule_ids <- list(c("pip05", "cslead", "bfdr10"), "pip05")
METHODS$roles <- list(c("primary", "S0", "S0"), "S1")

# The `settings` argument of every wrapper: the whole configuration plus `variant`.
make_settings <- function(variant) {
  list(COMMON = COMMON, A1 = A1, METHODS = METHODS,
       METHOD_SEED_OFFSET = METHOD_SEED_OFFSET, PIP_THRESHOLD = PIP_THRESHOLD,
       TEST_SEED = TEST_SEED, variant = variant)
}
