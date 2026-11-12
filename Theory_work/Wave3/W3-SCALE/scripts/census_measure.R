# census_measure.R -- leg B item B3: dispersion of island evidences against p and N on a frozen grid.
# A MEASUREMENT with the unmodified core exports: no method change, nothing shipped. For one S3-type dataset:
#  1. setup; one tier-0 calibration with the fixed-size budget (N0 = --n-cal, H0 = ceiling(512 N0 / 2500)), no
#     escalation: its grid is frozen (if the grid construction failed, the pilot schedule is used and recorded);
#  2. for every N in --n-islands: R = --islands final islands of N particles on that same frozen grid, streams
#     10 .. 9 + R, with the production L and 4 measured rounds, followed by the final local search (no LS0).
# Recorded per N: log Zhat_r, sd, R_eff, the largest weight, equal-weight and evidence-weighted PIPs (at the true
# variables and the largest null), per-island PIPs at the true variables, time per island, HPM = truth.
# Usage: Rscript --vanilla census_measure.R --core-dir D --p P --seed S --n-cal 2500 --n-islands 2500,10000
#          --islands 16 --mem-gb G --hours H --out FILE.rds
local({
  a <- grep("^--file=", commandArgs(FALSE), value = TRUE)
  assign("WS_DIR", if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd(), envir = globalenv())
})
source(file.path(WS_DIR, "ws_common.R"))
arg <- ws_args(list(core_dir = NA, p = NA, seed = "20261111", n_cal = "2500", n_islands = "2500", islands = "16", mem_gb = "8", hours = "23", out = NA))
stopifnot(!is.na(arg$core_dir), !is.na(arg$p), !is.na(arg$out))
p_arg <- as.integer(arg$p); seed <- as.numeric(arg$seed); R <- as.integer(arg$islands)
Ns <- as.integer(strsplit(arg$n_islands, ",")[[1]]); Ncal <- as.integer(arg$n_cal)
source(file.path(arg$core_dir, "v3.R"))
t_origin <- proc.time()[["elapsed"]]
rec <- list(meta = list(args = arg, host = Sys.info()[["nodename"]], started_utc = ws_utc(), core_key = V3_CPP_KEY, slurm_job = Sys.getenv("SLURM_JOB_ID")), runs = list())
save_rec <- function() { tmp <- paste0(arg$out, ".tmp"); saveRDS(rec, tmp); file.rename(tmp, arg$out) }
say <- function(...) cat(sprintf("[%s] ", ws_utc()), sprintf(...), "\n", sep = "")
dat <- ws_gen_s3(p_arg, 200L, as.integer(seed) %% 100000L + 7000000L)     # the dataset of the leg A profile at this p
pre <- v3_preprocess(dat$X, dat$y, dup_components = FALSE); stopifnot(pre$status == "ok")
n <- pre$n; p <- pre$p
ctx <- v3_context(pre$X, pre$y, orig = pre$kept, return_gram = FALSE)
t0 <- proc.time()[["elapsed"]]; setup <- v3_setup(ctx); stopifnot(inherits(setup, "v3_setup"))
rec$meta$dataset_id <- dat$dataset_id; rec$meta$active <- dat$active; rec$meta$setup_seconds <- proc.time()[["elapsed"]] - t0
# fixed-size budget for the calibration (the production rule would give N0 = max(2500, n, p))
b <- setup$budgets
H0 <- (512 * Ncal + 2499) %/% 2500
b$N0 <- Ncal; b$H0 <- H0; b$tiers <- data.frame(e = 0:1, N = c(Ncal, 4 * Ncal), H = c(H0, 4 * H0), T = b$tiers$T)
setup$budgets <- b
rec$meta$budgets <- b[c("n", "p", "K", "B", "ell", "L", "N0", "H0", "T0")]
runtime <- .v3cpp$cpp_runtime_new(as.numeric(arg$hours), proc.time()[["elapsed"]] - t_origin)
state <- .v3cpp$cpp_cal_new(setup$ptr, as.numeric(seed), list(cache_capacity = as.numeric(500 * p)), runtime)
t0 <- proc.time()[["elapsed"]]
tier <- v3_cal_tier(state, setup, 0, runtime, grid_fallback = FALSE)
cal_s <- proc.time()[["elapsed"]] - t0
grid <- tier$grid; grid_source <- "candidate grid"
if (is.null(grid)) { grid <- tier$pilot$schedule; grid_source <- "pilot schedule (grid construction failed or calibration stopped)" }
rec$calibration <- list(status = tier$status, seconds = cal_s, H = H0, T_pilot = length(tier$pilot$schedule) - 1L, rebuilds = tier$rebuilds, converged = tier$converged,
  triggers = tier$triggers, grid = grid, grid_source = grid_source, T_grid = length(grid) - 1L,
  diag_sd = vapply(tier$iterations, function(it) if (length(it$log_Z_r) == 4) stats::sd(it$log_Z_r) else NA_real_, 0),
  diag_seconds = vapply(tier$iterations, function(it) it$seconds[["islands"]], 0))
say("calibration H=%d: status %s, T_pilot %d, rebuilds %s, T_grid %d (%s), %.0f s; diagnostic sd: %s", H0, tier$status, rec$calibration$T_pilot,
    format(tier$rebuilds), rec$calibration$T_grid, grid_source, cal_s, paste(round(rec$calibration$diag_sd, 2), collapse = " "))
save_rec()
stopifnot(identical(tier$status, "ok"))
ex <- .v3cpp$cpp_cal_export(state); rm(state); invisible(gc())
act <- match(dat$active, pre$kept)
for (Nisl in Ns) {
  frozen <- v3_frozen(grid, tier = 0, N = Nisl, L = b$L, inherited = ex$inherited, budgets = b)
  ro <- v3_run_settings(setup, frozen, ls0 = FALSE); ro$N <- as.integer(Nisl); ro$islands <- R
  t0 <- proc.time()[["elapsed"]]
  raw <- .v3cpp$cpp_final_run(setup$ptr, frozen[["grid"]], ro, as.numeric(seed), frozen[["inherited"]], runtime)
  secs <- proc.time()[["elapsed"]] - t0
  isl <- Filter(function(x) !is.null(x) && !isTRUE(x$partial), raw$islands)
  lz <- vapply(isl, function(x) x$log_Z, 0); P <- do.call(cbind, lapply(isl, function(x) x$pip))
  w <- exp(lz - max(lz)); w <- w / sum(w); eq <- rowMeans(P); zw <- drop(P %*% w)
  out <- list(N = Nisl, islands_requested = R, islands_done = length(isl), status = raw$status, seconds = secs,
    island_seconds = vapply(isl, function(x) sum(x$seconds), 0), T = length(grid) - 1L, log_Z_r = lz,
    sd_log_Z_r = if (length(lz) >= 2) stats::sd(lz) else NA, R_eff = 1 / sum(w^2), max_W = max(w), weights = w,
    min_ess_share = min(vapply(isl, function(x) min(x$ess), 0)) / Nisl,
    pip_eq_active = eq[act], pip_Z_active = zw[act], pip_r_active = P[act, , drop = FALSE],
    pip_eq_max_null = max(eq[-act]), pip_Z_max_null = max(zw[-act]), max_abs_diff = max(abs(zw - eq)),
    sd_pip_r_max = max(apply(P, 1, stats::sd)), mpm_eq = pre$kept[eq > 0.5], mpm_Z = pre$kept[zw > 0.5],
    hpm = raw$ledger$hpm$model, hpm_F = raw$ledger$hpm$F, hpm_equals_truth = identical(as.integer(raw$ledger$hpm$model), as.integer(sort(dat$active))),
    island_best = raw$ledger$island_best, cache = raw$cache)
  rec$runs[[as.character(Nisl)]] <- out
  say("N=%d: %d of %d islands, status %s, %.0f s (%.0f s per island); sd(log Z_r) %.3f, R_eff %.2f of %d, max W %.3f; HPM = truth %s; max |PIP_Z - PIP_eq| %.4f",
      Nisl, length(isl), R, raw$status, secs, mean(out$island_seconds), out$sd_log_Z_r, out$R_eff, length(isl), out$max_W, out$hpm_equals_truth, out$max_abs_diff)
  save_rec()
  if (!identical(raw$status, "completed")) break
}
rec$meta$finished_utc <- ws_utc(); rec$meta$total_seconds <- proc.time()[["elapsed"]] - t_origin; rec$meta$peak_gib <- ws_mem()[["hwm_kb"]] / 2^20
rec$status <- "done"; save_rec(); cat("DONE\n")
