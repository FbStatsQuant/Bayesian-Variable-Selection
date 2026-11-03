# abl_fit.R -- ABL-START: one production v3 fit of one study design with one start arm.
# Usage: Rscript abl_fit.R <dataset_id> <scale_key> <arm A|B|C|D> <out.rds> [seed_offset=0]
# Everything is the production v3_fit (preprocess, budgets, calibration with its caps/tiers, final 4 islands x N_e,
# kernel, local search, HPM, seeds) except the setup, which is replaced by abl_setup(ctx, mode) (see abl_exports.cpp).
# Seed = study manifest method_seed + seed_offset.  Arm D reads backfit tables from $ABL_WORK/backfit/<id>_<sk>.rds.
args <- commandArgs(TRUE)
id <- args[1]; sk <- args[2]; arm <- args[3]; out <- args[4]; soff <- if (length(args) >= 5) as.integer(args[5]) else 0L
source(file.path(dirname(normalizePath(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)))), "abl_core.R"))
abl_load()
mode <- c(A = 0L, B = 1L, C = 2L, D = 3L)[[arm]]
study <- "/home/fb31/ls0_work/study"
pp <- sub("_.*", "", id); sc <- sub("^[^_]*_(S[0-9]).*", "\\1", id)
if (id == "smoke") {
  set.seed(20261103); n <- 100; p <- 150; Z <- matrix(rnorm(n * p), n); X <- Z + 0.6 * Z[, rep(1:30, 5)]
  S0 <- c(3L, 17L, 40L); y <- drop(X[, S0] %*% c(1, -0.8, 0.7)) + rnorm(n); seed <- 12345L
} else {
  man <- read.csv(file.path(study, "manifests", "cells", paste0(pp, "_", sc, "_inputs.csv")))
  seed <- man$method_seed[man$dataset_id == id]
  inp <- readRDS(file.path(study, "inputs", pp, paste0(id, ".rds")))
  tru <- read.csv(file.path(study, "manifests", "cells", paste0(pp, "_", sc, "_truth.csv")))
  S0 <- sort(as.integer(strsplit(tru$active[tru$dataset_id == id], ";")[[1]]))
  X <- inp$X; y <- unname(inp$Y[, sk])
}
seed <- as.integer(seed + soff)
BF <- if (arm == "D") readRDS(file.path(ABL_WORK, "backfit", paste0(id, "_", sk, ".rds"))) else NULL
logr_D <- BF$logr
SETUP <- NULL
v3_setup <- function(ctx) { s <- abl_setup(ctx, mode, logr_D); SETUP <<- s; s }   # replaces the production setup
lse <- function(x) { m <- max(x); m + log(sum(exp(x - m))) }
t0 <- proc.time()[["elapsed"]]
fit <- v3_fit(X, y, seed)
wall <- proc.time()[["elapsed"]] - t0
st <- SETUP; ctx <- st$ctx
if (arm == "D") stopifnot(identical(lapply(BF$blocks, as.integer), lapply(st$blocks, as.integer)))
sc0 <- tryCatch(v3_score(ctx, S0[S0 %in% ctx$orig]), error = function(e) NULL)
cal <- fit$calibration
res <- list(id = id, scale = sk, arm = arm, mode = mode, seed = seed, S0 = S0, wall = wall, status = fit$status,
  B = st$B, B_start = st$B_start, J = length(st$blocks), log_Zbar0 = st$start$log_Zbar0, log_m0 = fit$log_m0,
  log_pi0_S0 = v3_start_logmass(st$start, S0[S0 %in% ctx$orig]), F_S0 = if (is.null(sc0)) NA else sc0$F,
  timings = fit$timings[c("setup_total", "calibration", "final", "total")],
  final_detail = fit$timings$final_detail,
  cal = if (!is.null(cal)) list(status = cal$status, tier_final = cal$tier_final, escalated = cal$escalated,
     flags = cal$flags, seconds = cal$seconds,
     tiers = lapply(cal$tiers, function(a) list(tier = a$tier, status = a$status, rebuilds = a$rebuilds,
        converged = a$converged, pilot_T = length(a$pilot$schedule) - 1, seconds = a$seconds, triggers = a$triggers,
        grid_T = vapply(a$grids, function(g) length(g$grid) - 1, 0))),
     ledger_counts = list(logical = cal$ledger$logical, fresh = cal$ledger$fresh)) else NULL,
  T_final = if (!is.null(fit$frozen)) length(fit$frozen$grid) - 1 else NA, tier = fit$frozen$tier %||% NA,
  grid = fit$frozen$grid,
  score_counts = fit$score_counts, flags = fit$flags,
  hpm = sort(as.integer(fit$hpm)), hpm_F = fit$hpm_F, hpm_provenance = fit$hpm_provenance,
  hpm_before_local = fit$hpm_before_local, island_best = fit$island_best,
  log_Z_r = fit$log_Z_r, log_Z = fit$log_Z, pip_r = fit$pip_r,
  ess_min = if (!is.null(fit$stage_record)) vapply(fit$stage_record, function(x) min(x$ess), 0) else NULL,
  N = fit$settings$N)
if (!is.null(fit$pip_r)) {
  w <- exp(fit$log_Z_r - max(fit$log_Z_r)); w <- w / sum(w)
  res$pip_eq <- rowMeans(fit$pip_r); res$pip_zw <- as.vector(fit$pip_r %*% w)
}
res$log_pi0_hpm <- if (length(res$hpm) <= ctx$K) v3_start_logmass(st$start, res$hpm) else NA
res$orig <- ctx$orig
dir.create(dirname(out), recursive = TRUE, showWarnings = FALSE)
saveRDS(res, out)
cat(sprintf("%s %s arm=%s seed=%d status=%s wall=%.0fs T=%s tier=%s logZ=%s sdlogZ=%s hpm==S0=%s log10pi0(S0)=%.2f\n",
  id, sk, arm, seed, res$status, wall, res$T_final, res$tier, format(res$log_Z, digits = 8),
  if (length(res$log_Z_r)) format(sd(res$log_Z_r), digits = 3) else NA, identical(res$hpm, S0), res$log_pi0_S0 / log(10)))
