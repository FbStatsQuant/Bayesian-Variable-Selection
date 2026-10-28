# config.R -- constants for benchmark A2 (spike-and-slab lasso) of the n = 200 BVS study.
# Implements master §III.3.0 ("Configuration and code layout", "Method registry")
# and §III.3.7 (d) (parameter table, `config.R` names). Frozen before the pilot.
# This thread's copy holds COMMON plus the A2 / A2RS blocks and the two A2 METHODS rows;
# the blocks of the other seven methods live in their own folders and are merged later.

# Study-wide scalars (§III.3.0).
METHOD_SEED_OFFSET <- 4000000L
PIP_THRESHOLD      <- 0.5
TEST_SEED          <- 20261019L

# Common block: only the fields A2 uses (§III.3.0 input assertions; §III.3.1 d names).
COMMON <- list(
  study       = "bench20261019",
  regime      = "H",
  n           = 200L,
  n_folds     = 10L,
  min_fold_n  = 3L,       # each fold label 1..10 has at least 3 rows (§III.3.1 e.1)
  design_tol  = 1e-10     # centring and sd-1 tolerance for X (§III.3.0)
)

# A2 primary: package defaults except variance = "unknown" (§III.3.7 d).
A2 <- list(
  PKG_VERSION  = "1.2.3.9001",
  N_PARAMS     = 15L,           # registered parameters of SSL_gaussian (§III.3.7 b)
  PENALTY      = "adaptive",    # theta ~ Beta(A, B), updated
  VARIANCE     = "unknown",     # sigma^2 estimated
  LAMBDA1      = 1,             # = lambda0[1]
  NLAMBDA      = 100L,          # lambda0 = seq(1, LAMBDA0_MAX, length.out = NLAMBDA)
  LAMBDA0_MAX  = "n",           # resolved to n by a2_ladder()
  THETA_INIT   = 0.5,
  SIGMA_DF     = 3,             # sigma0 = sqrt(df * ncp / (df + 2))
  SIGMA_QUANT  = 0.9,           # ncp = sd(y)^2 * qchisq(1 - quant, df) / df
  A            = 1,
  B            = "p",           # resolved to p by the native-call helper
  EPS          = 0.001,         # relative coefficient change per sweep
  MAX_ITER     = 500L,          # sweeps per ladder point
  COUNTER      = 10L,           # theta / sigma^2 update every COUNTER coordinate updates
  STABLE_TAIL  = 5L,            # tail-stability window (flag only)
  FP_TOL_MULT  = 10             # fixed-point audit tolerance = FP_TOL_MULT * EPS * (1 + max|beta|)
)

# A2RS: S1 Ray-Szabo ladder (§III.3.7 d, f); every other field is taken from A2.
A2RS <- list(
  LAMBDA1     = 0.01,
  NLAMBDA     = 200L,
  LAMBDA0_MAX = "p"
)

# Method registry (§III.3.0): this thread registers only the A2 rows.
# rule_ids and roles are lists, in the order of §III.3.7 (f).
METHODS <- data.frame(
  method_id    = c("A2", "SSL-RS"),
  fn           = c("fit_A2_ssl", "fit_A2_ssl"),
  variant      = c("primary", "RS"),
  method_label = c("Spike-and-slab lasso", "Spike-and-slab lasso (Ray-Szabo ladder)"),
  package      = c("SSLASSO", "SSLASSO"),
  pkg_version  = c("1.2.3.9001", "1.2.3.9001"),
  tier         = c("primary", "S1"),
  stringsAsFactors = FALSE
)
METHODS$rule_ids <- I(list("ssl_final", "ssl_final"))
METHODS$roles    <- I(list("primary", "S1"))

# Closed vocabularies (§III.3.0, §IV.1.2).
STATUS_VALUES  <- c("ok", "warning", "failed", "timeout", "not_run")
# capped_intermediate is informational, not a flag (lead decision 2026-10-19, production brief).
FLAG_CODES     <- c("kkt_path", "path_truncated", "L_saturated", "elbo_drop", "sigma2_floor",
                    "tail_unstable", "fixed_point",
                    "ess_tau", "ess_ci95", "crn_mismatch")
INFO_CODES     <- c("lambda_first", "lambda_last", "alpha_edge", "kappa_edge", "capped_intermediate",
                    "floored_selected", "ebic_at_largest")
RULE_ID_VALUES <- c("cv_min", "cv_1se", "ebic1", "ebic05", "bic", "pip05", "cslead", "bfdr10",
                    "ssl_final", "ci95", "km2")
