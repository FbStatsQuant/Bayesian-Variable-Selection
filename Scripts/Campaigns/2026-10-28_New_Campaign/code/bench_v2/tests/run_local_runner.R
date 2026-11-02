# Local-only harness: executes the production runner's main() and substitutes
# the audit's glmnet 4.1-10 compatibility gates in memory. No production source changes.
root <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2"
code_root <- file.path(root, "F3_AdaptiveLasso")
e <- new.env(parent = globalenv())
sys.source(file.path(code_root, "run_case.R"), e)
e$script_dir <- function() code_root
e$check_library <- function(...) invisible(TRUE)
e$.libPaths <- function(...) base::.libPaths()
original_load <- e$load_code
e$load_code <- function(path) {
  result <- original_load(path)
  engine <- result$engine
  engine$assert_pkg_version <- function(...) invisible(TRUE)
  engine$glmnet_target_path <- function(Xd, yd, alpha, lam, pf, G) {
    s <- sqrt(mean(yd^2)); m <- alpha + s * (1 - alpha)
    fit <- glmnet::glmnet(Xd, yd, family = "gaussian", alpha = alpha / m, lambda = lam * m,
      penalty.factor = pf, intercept = FALSE, standardize = FALSE, type.gaussian = G$type_gaussian,
      thresh = G$thresh, maxit = G$maxit)
    engine$check_glmnet_path(fit, lam * m, G)
    B <- as.matrix(fit$beta); scale <- max(1, max(abs(crossprod(Xd, yd))) / nrow(Xd))
    list(B = B, s = s, m = m, a = alpha / m, jerr = fit$jerr, npasses = fit$npasses,
         kkt = engine$kkt_glmnet(Xd, yd, B, lam, alpha, pf, scale))
  }
  result
}
Sys.setenv(OMP_NUM_THREADS = "1", OPENBLAS_NUM_THREADS = "1", MKL_NUM_THREADS = "1")
glmnet::glmnet.control(fdev = 0, devmax = 1)
status <- e$main(c("--input", "C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/dev/inputs/p0500/dev_p0500_S1_r001.rds",
  "--out", file.path(root, "tests", "runner_output"), "--run-id", "v2_local_e2e",
  "--manifest", "C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/dev/manifests/dev_inputs_manifest.csv"))
quit(status = status)
