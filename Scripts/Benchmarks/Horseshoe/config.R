# Constants for benchmark A3 Horseshoe (bayesreg) of the n = 200 BVS benchmark study.
# Implements master §III.3.0 ("Configuration and code layout", "Method registry") and the
# parameter table of §III.3.8 (d). Frozen before the pilot; no data-derived numbers.
# This folder holds only the COMMON block and the A3 block; the other blocks of the master
# (GRID, GLMNET, F1-F5, A1, A2, A2RS) live in the other method folders until the merge.

# Study-wide scalars (§III.3.0).
METHOD_SEED_OFFSET <- 4000000L
PIP_THRESHOLD      <- 0.5
TEST_SEED          <- 20261019L

COMMON <- list(
  STUDY      = "bench20261019",
  REGIME     = "H",
  N          = 200L,
  NFOLDS     = 10L,
  SCALES     = c(c100 = 1, c075 = 0.75, c050 = 0.50, c035 = 0.35, c025 = 0.25),
  RNG_KIND   = c("Mersenne-Twister", "Inversion", "Rejection"),
  LIB        = "/projects/ml75/fb31/BVS/bench20261019/lib/R452",
  R_VERSION  = "4.5.2",                             # asserted by the runner (module R/4.5.2)
  X_TOL      = 1e-10,                               # centring and sd-1 tolerance of assert_inputs
  THREAD_VARS = c("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"),
  # Closed vocabularies (§III.3.0 Status, Flags, Codes; §IV.1.2).
  STATUS_VALUES = c("ok", "warning", "failed", "timeout", "not_run"),
  FLAG_CODES = c("kkt_path", "path_truncated", "L_saturated", "elbo_drop", "sigma2_floor",
                 "tail_unstable", "fixed_point",
                 "ess_tau", "ess_ci95", "crn_mismatch"),
  # capped_intermediate (A2) is informational since the lead's production decision of 2026-10-19.
  INFO_CODES = c("capped_intermediate", "lambda_first", "lambda_last", "alpha_edge", "kappa_edge",
                 "floored_selected", "ebic_at_largest"),
  RULE_IDS   = c("cv_min", "cv_1se", "ebic1", "ebic05", "bic", "pip05", "cslead", "bfdr10",
                 "ssl_final", "ci95", "km2"),
  ROLES      = c("primary", "S0", "S1", "S2"),
  N_ACTIVE_COLS = 14L                               # sel_a01..sel_a14, pip_a01..pip_a14 (§IV.1.2)
)

# §III.3.8 (d). Field names as in the master's `config.R name` column.
A3 <- list(
  MODEL        = "normal",
  PRIOR        = "hs",
  # O10 re-plan, 2026-10-19 (MASTER_CHANGES 10): 1,000 + 5,000 (thin 1) flagged ess_tau in 12/12 dev
  # fits and the master's doubled 2,000 + 10,000 still in 12/12 (long-chain diagnostic); chosen
  # from diagnostics only with the GPT-6 Astra production consult: 85,000 iterations.
  # Longer-chain sensitivity copy (PREREG_c050 R6, lead decision 2026-10-21): 8 x the production budget
  # (10,000 + 15,000 kept, thin 5), one fixed multiple for every flagged fit: 80,000 + 120,000 kept,
  # thin 5 (680,000 iterations). Nothing else differs from production.
  N_SAMPLES    = 120000L,
  BURNIN       = 80000L,
  THIN         = 5L,
  T_DOF        = 5,
  N_CORES      = 1L,
  CI_PROBS     = c(0.025, 0.975),
  QTYPE        = 7L,
  ESS_MIN      = 100,
  KM_NSTART    = 10L,
  KM_ITER_MAX  = 10L,
  KM_ALGORITHM = "Hartigan-Wong",
  MU_TOL       = 1e-10,                             # step 4: max|mu.beta - rowMeans(B)| <= MU_TOL (1 + max|mu|)
  PKG_VERSIONS = c(bayesreg = "1.3", pgdraw = "1.1", doParallel = "1.0.17"),
  EXTRA_COLS   = c("rng_after", "diag_s")           # A3 columns added to the rule rows (§III.3.8 g, k)
)

# Method registry (§III.3.0). Only A3 is registered in this folder; the S2 ids HS+ and
# HS-pkg are not registered and emit no rows. `converged_na`: the method has no convergence
# criterion, so `converged` is NA on every row, failed or not (§III.3.0 Convergence).
METHODS <- data.frame(
  method_id    = "A3",
  fn           = "fit_A3_horseshoe",
  variant      = "primary",
  method_label = "Horseshoe (bayesreg)",
  package      = "bayesreg",
  pkg_version  = "1.3",
  tier         = "primary",
  converged_na = TRUE,
  stringsAsFactors = FALSE
)
METHODS$rule_ids <- list(c("ci95", "km2"))
METHODS$roles    <- list(c("primary", "S0"))

# The `settings` argument of every wrapper: the whole configuration plus `variant`.
make_settings <- function(variant = "primary") {
  list(METHOD_SEED_OFFSET = METHOD_SEED_OFFSET, PIP_THRESHOLD = PIP_THRESHOLD,
       TEST_SEED = TEST_SEED, COMMON = COMMON, A3 = A3, METHODS = METHODS,
       variant = variant)
}
