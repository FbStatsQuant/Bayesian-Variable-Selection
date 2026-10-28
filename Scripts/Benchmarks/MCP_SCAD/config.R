# config.R -- constants for benchmark F4 MCP (and its S1 variant F4_SCAD).
# Implements master §III.3.0 "Configuration and code layout" and §III.3.4 d, k
# (01_Methodology_and_Theory/MASTER_Methodology_and_Plan/MASTER_Methodology_and_Plan.md, 2026-10-19).
# Only the blocks F4 uses are defined here (COMMON, GRID, F4); the other methods' blocks live in
# their own folders and are merged later. Frozen before the pilot. No oracle-derived numbers (§III.3.9).

# Study-wide scalars (§III.3.0).
METHOD_SEED_OFFSET <- 4000000L
PIP_THRESHOLD      <- 0.5
TEST_SEED          <- 20261019L
SUPPORT_ZERO_TOL   <- 0          # supports are the exactly nonzero coefficients (§III.3.1 conventions)

# Pinned runtime (§III.3.0: GCC/14.3.0 + R/4.5.2) and sealed study library (§III.3.0 "Library"; brief).
R_VERSION <- "4.5.2"
STUDY_LIB <- "/projects/ml75/fb31/BVS/bench20261019/lib/R452"

COMMON <- list(
  n            = 200L,
  intercept    = FALSE,                               # §II.8
  standardize  = FALSE,                               # §II.8
  nfolds       = 10L,                                 # §II.9
  min_fold_size = 3L,                                 # §III.3.1 e step 1
  kmax_ebic    = 100L,                                # §III.3.0 EBIC cap = floor(n/2)
  ebic_gamma   = c(ebic1 = 1, ebic05 = 0.5, bic = 0), # §III.3.1 d
  ols_tol      = 1e-10,                               # lm.fit rank tolerance (Oct-14)
  design_tol   = 1e-10                                # input assertion tolerance (Oct-14)
)

# λ fraction grid shared by F1-F4 (§III.3.1 conventions, d):
# frac = exp(seq(0, log(min_ratio), length.out = nlambda)); grid = max_mult * entry * frac.
GRID <- list(nlambda = 200L, min_ratio = 1e-4, max_mult = 1.01)

# §III.3.4 k, plus lambda_rel_tol (§III.3.4 e step 3 uses "1e-12 relative (as GLMNET$lambda_rel_tol)";
# F4 has no GLMNET block, so the value is carried here; see ASSUMPTIONS.md A2).
F4 <- list(mcp_gamma = 3, scad_gamma = 3.7, alpha = 1, eps = 1e-8, maxit = 1e6,
           convex = TRUE, warn = TRUE, returnX = FALSE,
           kkt_abs_tol = 1e-4, loss_abs_tol = 1e-10, loss_rel_tol = 1e-8,
           lambda_rel_tol = 1e-12, pkg_version = "3.16.0")

# Method registry (§III.3.0 "Method registry and rule frame"): one row per method id, rule ids and
# roles in the order of §III.3.4 f.
METHODS <- data.frame(
  method_id    = c("F4", "F4_SCAD"),
  fn           = c("fit_F4_mcp", "fit_F4_scad"),
  variant      = c("primary", "scad"),
  method_label = c("MCP", "SCAD on X/s"),
  package      = c("ncvreg", "ncvreg"),
  pkg_version  = c("3.16.0", "3.16.0"),
  tier         = c("primary", "S1"),
  stringsAsFactors = FALSE
)
METHODS$rule_ids <- list(c("ebic1", "ebic05", "bic"), c("ebic1", "ebic05", "bic"))
METHODS$roles    <- list(c("primary", "S0", "S0"),    c("S1", "S1", "S1"))

# Method-specific extra rule-row columns (§III.3.4 g) and their types.
F4_EXTRA_COLS <- list(lambda = NA_real_, rss = NA_real_, crit_value = NA_real_,
                      path_index = NA_integer_, k_valid_max = NA_integer_, k_path_max = NA_integer_)

# The settings list passed to every wrapper is this whole configuration plus settings$variant (§III.3.0).
CONFIG <- list(METHOD_SEED_OFFSET = METHOD_SEED_OFFSET, PIP_THRESHOLD = PIP_THRESHOLD,
               TEST_SEED = TEST_SEED, SUPPORT_ZERO_TOL = SUPPORT_ZERO_TOL, STUDY_LIB = STUDY_LIB,
               R_VERSION = R_VERSION,
               COMMON = COMMON, GRID = GRID, F4 = F4, METHODS = METHODS,
               F4_EXTRA_COLS = F4_EXTRA_COLS)
