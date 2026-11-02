# VAL-FP replay driver (API-AUDIT, task R10).
# Usage: Rscript valfp_fit.R <core_dir> <mode: fp | ld_replay | ld_full> <fit_id 1..10> <out_dir>
#   fp        : production v3_fit (double) on dataset <fit_id>; saves the compact fit incl. the frozen object C.
#   ld_replay : long-double core; same data, same seed; v3_setup + v3_final_run on the fp fit's frozen C (read from
#               out_dir/fit<id>_fp.rds). Measures the final-run floating-point error given C.
#   ld_full   : long-double core; full v3_fit (calibration + final run) to check that calibration freezes the same C.
# Data: n = 200, scenario covariances copied verbatim from Scripts/Data_generators/gen_dev_data.R
# (scenario_covariance), s0 = 5 true predictors, fixed seeds (data seed 7100 + id, method seed 9100 + id).
args <- commandArgs(TRUE)
core <- args[1]; mode <- args[2]; id <- as.integer(args[3]); out <- args[4]
dir.create(out, showWarnings = FALSE, recursive = TRUE)
source(file.path(core, "v3.R"))
scenario_covariance <- function(scenario, p=500L) {          # verbatim from gen_dev_data.R
  stopifnot(length(scenario)==1L, scenario %in% 1:6, p>=1L, p==as.integer(p))
  group <- ceiling(seq_len(p)/5)
  H <- outer(group,group,"==")
  I <- diag(p)
  switch(as.integer(scenario),
    I,
    0.5^abs(outer(seq_len(p),seq_len(p),"-")),
    0.7*H+0.3*I,
    0.85*H+0.15*I,
    0.3*matrix(1,p,p)+0.4*H+0.3*I,
    {rho <- 0.4+0.1*((group-1L)%%6L); S <- H*matrix(rho,p,p); diag(S)<-1; S})
}
design <- data.frame(id = 1:10, p = c(20, 20, 20, 20, 30, 30, 30, 40, 40, 40),
                     scen = c(1, 2, 4, 5, 3, 4, 6, 2, 4, 5), scale = c(1, .5, .5, .35, .75, .5, .5, .5, .35, .5))
d <- design[id, ]
set.seed(7100 + id, kind = "Mersenne-Twister", normal.kind = "Inversion")
n <- 200L; p <- d$p
X <- matrix(rnorm(n * p), n, p) %*% chol(scenario_covariance(d$scen, p))
S0 <- sort(sample.int(p, 5)); beta <- numeric(p); beta[S0] <- d$scale * c(1, -1, 1, -1, 1)
y <- drop(X %*% beta + rnorm(n))
seed <- 9100L + id
data_hash <- digest::digest(list(X, y), algo = "sha256")
compact <- function(f, extra = list()) {
  keep <- c("status", "message", "branch_run", "frozen", "log_Z", "log_Z_r", "log_Z_rel_m0", "pip_primary", "pip_r",
            "mpm", "hpm", "hpm_F", "hpm_provenance", "near_ties", "near_tie_F", "streams", "stage_table", "score_counts",
            "cache", "local_search", "hpm_before_local", "island_best", "flags", "log_m0", "log_Zbar0", "top_store",
            "blocks", "neighbours", "rb", "terminal_table", "timings", "calibration")
  c(f[intersect(keep, names(f))], list(data_hash = data_hash, id = id, design = d, S0 = S0, mode = mode), extra)
}
t0 <- proc.time()[["elapsed"]]
if (mode %in% c("fp", "ld_full")) {
  f <- v3_fit(X, y, seed, allocation = list(mem_gb = 8, hours = 24))
  if (!is.null(f$calibration)) f$calibration <- f$calibration[c("status", "frozen", "flags", "hpm")]
  res <- compact(f)
} else if (mode == "ld_replay") {
  fp <- readRDS(file.path(out, sprintf("fit%02d_fp.rds", id)))
  stopifnot(identical(fp$data_hash, data_hash), identical(fp$status, "completed"))
  pre <- v3_preprocess(X, y, dup_components = FALSE)
  ctx <- v3_context(pre$X, pre$y, orig = pre$kept, return_gram = FALSE)
  setup <- v3_setup(ctx)
  fr <- v3_final_run(setup, fp$frozen, seed, NULL)
  fr$frozen <- fp$frozen; fr$blocks <- setup$blocks; fr$neighbours <- setup$neighbours
  fr$log_Zbar0 <- setup$start$log_Zbar0
  res <- compact(fr)
} else if (mode == "fp_nullguard") {
  # GUARD empirical check: the potential uninterrupted run R-bar = the same pipeline with runtime = NULL and no
  # preflight (every `guard && ...` short-circuits). Compared bitwise with the guarded production fit.
  pre <- v3_preprocess(X, y, dup_components = FALSE)
  ctx <- v3_context(pre$X, pre$y, orig = pre$kept, return_gram = FALSE)
  setup <- v3_setup(ctx)
  cal <- v3_calibrate(setup, seed, preflight = NULL, runtime = NULL)
  fr <- v3_final_run(setup, cal$frozen, seed, NULL)
  fr$frozen <- cal$frozen; fr$blocks <- setup$blocks; fr$neighbours <- setup$neighbours
  fr$log_Zbar0 <- setup$start$log_Zbar0
  fr$calibration <- cal[c("status", "frozen", "flags", "hpm")]
  res <- compact(fr)
} else if (mode == "fp_stop") {
  # GUARD stop path: allocation of 0.05 s (hours = 0.05/3600): the fit must end with status resource_limit.
  f <- v3_fit(X, y, seed, allocation = list(mem_gb = 8, hours = 0.05 / 3600))
  if (!is.null(f$calibration)) f$calibration <- f$calibration[c("status", "frozen", "flags", "hpm")]
  res <- compact(f, list(estimates_available = f$estimates_available, hpm_incomplete = f$hpm_incomplete,
                         partial_results = f$partial_results, n_checkpoints = NROW(f$runtime_guard$checkpoints),
                         last_checkpoint = tail(f$runtime_guard$checkpoints, 1)))
} else if (mode %in% c("fp_seeds", "ld_seeds")) {
  # Extra final-run replays on the fp fit's frozen C with final seeds 50000 + 100 id + k, k = 1..10. Streams 10..13
  # of any seed are independent of C, so these are draws of the final run given C (used to tighten the eps bound).
  fp <- readRDS(file.path(out, sprintf("fit%02d_fp.rds", id)))
  stopifnot(identical(fp$data_hash, data_hash))
  pre <- v3_preprocess(X, y, dup_components = FALSE)
  ctx <- v3_context(pre$X, pre$y, orig = pre$kept, return_gram = FALSE)
  setup <- v3_setup(ctx)
  res <- lapply(1:10, function(k) {
    fr <- v3_final_run(setup, fp$frozen, 50000L + 100L * id + k, NULL)
    fr$frozen <- fp$frozen; fr$log_Zbar0 <- setup$start$log_Zbar0
    c(compact(fr), list(final_seed = 50000L + 100L * id + k))
  })
  res <- list(runs = res, status = "multi", log_Z = NA)
} else if (mode == "thr") {
  # Threshold logging (instrumented cores from make_log_cores.sh): final run on the fp frozen C, original seed.
  fp <- readRDS(file.path(out, sprintf("fit%02d_fp.rds", id)))
  stopifnot(identical(fp$data_hash, data_hash))
  pre <- v3_preprocess(X, y, dup_components = FALSE)
  ctx <- v3_context(pre$X, pre$y, orig = pre$kept, return_gram = FALSE)
  setup <- v3_setup(ctx)
  Sys.setenv(V3_THR_LOG = file.path(out, sprintf("thr%02d_%s.bin", id, basename(core))))
  fr <- v3_final_run(setup, fp$frozen, seed, NULL)
  Sys.unsetenv("V3_THR_LOG")
  res <- list(status = fr$status, log_Z = fr$log_Z, log_Z_r = fr$log_Z_r, same_as_fp_fit = identical(fr$log_Z_r, fp$log_Z_r),
              settings = fr$settings, T = length(fp$frozen$grid) - 1, p = setup$ctx$p, B = setup$B)
  cat(sprintf("thr fit %d core %s: log_Z_r identical to the fp fit's: %s\n", id, basename(core), res$same_as_fp_fit))
} else stop("mode")
res$seconds <- proc.time()[["elapsed"]] - t0
saveRDS(res, file.path(out, sprintf("fit%02d_%s.rds", id, mode)))
cat(sprintf("fit %d mode %s status %s log_Z %.17g seconds %.1f\n", id, mode, res$status, res$log_Z %||% NA, res$seconds))
