# stage_measure.R -- P1M gate G0, Part S: stage-level island records with the existing, UNMODIFIED code (revision D).
# A MEASUREMENT: no method change; the core is sourced from --core-dir exactly as deployed and is never edited. Same
# protocol as W3-SCALE B3 (scripts/census_measure.R at origin/theory/W3-SCALE 299cbc58), on the same dataset and seed:
#  1. S3-type dataset ws_gen_s3(p, n = 200, seed %% 100000 + 7000000) (= the B3 census dataset at this p); setup;
#  2. one tier-0 calibration with the fixed-size budget (N0 = --n-cal, H0 = ceiling(512 N0 / 2500)), no escalation;
#     its grid is frozen;
#  3. ONE final run of R = --islands islands of N = --n-isl particles on that grid, streams 10 .. 9 + R, production L
#     and 4 measured rounds, then the final local search (no LS0). Islands are run in one call, as in B3, so island r is
#     the same computation as B3's island r (checked against --b3-rds when given).
#
# What census_measure.R dropped and this driver keeps (per island, from the core's own return value):
#  * the full stage table: stage, phi, log increment, cumulative log Z, ESS, distinct_resampled, distinct_moved and the
#    per-stage move counts (gibbs, gibbs_state_changes = `gibbs_change`, unit/neighbour swaps, independence moves);
#  * the terminal table (burn-in and measured rounds: move counts, distinct supports), RB arrays, PIPs, timings;
#  * the calibration's pilot and diagnostic-island stage tables (every iteration; `rb_round` dropped there);
#  * the top store of the final run: every F value (for log sum exp F) and its models.
# NOT reachable without changing the core (stated in the record):
#  * per-island top stores: the core keeps ONE ledger per final-run call (all islands + block-table models + the
#    inherited calibration models), so the store is the run's merged store, not island r's;
#  * terminal particle supports: the population is local to Engine::run_island_s (v3_engine.h) and island_to_list
#    (v3_core.cpp) does not return it; no exported function gives it.
# Usage: Rscript --vanilla stage_measure.R --core-dir D --p P [--seed 20261111] [--n-cal 2500] [--n-isl 2500]
#          --islands R --hours H --out FILE.rds [--b3-rds FILE] [--manifest revD_SHA256SUMS] [--store-models all|K]
local({
  a <- grep("^--file=", commandArgs(FALSE), value = TRUE)
  assign("WS_DIR", if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd(), envir = globalenv())
})
source(file.path(WS_DIR, "ws_common.R"))
arg <- ws_args(list(core_dir = NA, p = NA, seed = "20261111", n_cal = "2500", n_isl = "2500", islands = "16", hours = "23",
                    out = NA, b3_rds = "", manifest = file.path(WS_DIR, "revD_SHA256SUMS"), store_models = "all"))
stopifnot(!is.na(arg$core_dir), !is.na(arg$p), !is.na(arg$out))
p_arg <- as.integer(arg$p); seed <- as.numeric(arg$seed); R <- as.integer(arg$islands); Nisl <- as.integer(arg$n_isl); Ncal <- as.integer(arg$n_cal)
say <- function(...) cat(sprintf("[%s] ", ws_utc()), sprintf(...), "\n", sep = "")

# --- 0. the code under test is revision D, unmodified: every source file against the manifest (fail closed) ---------
man <- read.table(arg$manifest, header = FALSE, col.names = c("sha256", "file"), stringsAsFactors = FALSE)
got <- vapply(file.path(arg$core_dir, man$file), function(f) if (file.exists(f)) digest::digest(file = f, algo = "sha256") else NA_character_, "")
src_now <- sort(c(file.path("cpp", list.files(file.path(arg$core_dir, "cpp"))), list.files(arg$core_dir, pattern = "\\.(R|md)$")))
code_check <- list(manifest = normalizePath(arg$manifest), files = nrow(man), all_match = all(!is.na(got) & got == man$sha256),
                   mismatched = man$file[is.na(got) | got != man$sha256], extra_files = setdiff(src_now, man$file))
if (!code_check$all_match || length(code_check$extra_files)) stop("core dir is not revision D as in the manifest: ",
  paste(c(code_check$mismatched, code_check$extra_files), collapse = ", "))
say("core check: %d files match %s", nrow(man), basename(arg$manifest))

source(file.path(arg$core_dir, "v3.R"))
t_origin <- proc.time()[["elapsed"]]
rec <- list(meta = list(args = arg, host = Sys.info()[["nodename"]], cpu = tryCatch(sub(".*: ", "", grep("model name", readLines("/proc/cpuinfo"), value = TRUE)[1]), error = function(e) NA),
                        started_utc = ws_utc(), core_key = V3_CPP_KEY, code_check = code_check, slurm_job = Sys.getenv("SLURM_JOB_ID"),
                        slurm_array = paste(Sys.getenv("SLURM_ARRAY_JOB_ID"), Sys.getenv("SLURM_ARRAY_TASK_ID"), sep = "_"),
                        R = R.version.string, driver = "stage_measure.R (P1M G0 Part S)",
                        not_reachable = c(per_island_store = "one ledger per final-run call: the store is the run's merged store (islands + block tables + inherited calibration models)",
                                          terminal_supports = "population local to Engine::run_island_s; not returned by island_to_list; no export")),
            calibration = NULL, final = NULL)
save_rec <- function() { tmp <- paste0(arg$out, ".tmp"); saveRDS(rec, tmp); file.rename(tmp, arg$out) }

# --- 1. dataset and setup (as census_measure.R) ----------------------------------------------------------------------
dat <- ws_gen_s3(p_arg, 200L, as.integer(seed) %% 100000L + 7000000L)
pre <- v3_preprocess(dat$X, dat$y, dup_components = FALSE); stopifnot(pre$status == "ok")
n <- pre$n; p <- pre$p
ctx <- v3_context(pre$X, pre$y, orig = pre$kept, return_gram = FALSE)
t0 <- proc.time()[["elapsed"]]; setup <- v3_setup(ctx); stopifnot(inherits(setup, "v3_setup"))
rec$meta$dataset_id <- dat$dataset_id; rec$meta$active <- dat$active; rec$meta$setup_seconds <- proc.time()[["elapsed"]] - t0
rec$meta$data_sha256 <- c(X = digest::digest(dat$X, algo = "sha256"), y = digest::digest(dat$y, algo = "sha256"))
b <- setup$budgets
H0 <- (512 * Ncal + 2499) %/% 2500
b$N0 <- Ncal; b$H0 <- H0; b$tiers <- data.frame(e = 0:1, N = c(Ncal, 4 * Ncal), H = c(H0, 4 * H0), T = b$tiers$T)
setup$budgets <- b
rec$meta$budgets <- b[c("n", "p", "K", "B", "ell", "L", "N0", "H0", "T0")]
say("dataset %s (n %d, p %d); setup %.0f s; L %d, ell %d", dat$dataset_id, n, p, rec$meta$setup_seconds, b$L, b$ell)

# --- helpers: island records -> tables ---------------------------------------------------------------------------------
stage_table <- function(x, N) {
  T <- length(x$phi)
  if (T == 0) return(NULL)
  sm <- as.data.frame(x$stage_moves)
  data.frame(stage = seq_len(T), phi = x$phi, log_increment = x$log_increment, cum_log_Z = x$cum_log_Z, ess = x$ess,
             ess_share = x$ess / N, distinct_resampled = x$distinct_resampled, distinct_moved = x$distinct_moved,
             sm[seq_len(T), , drop = FALSE], check.names = FALSE)
}
terminal_table <- function(x, L) {
  tm <- as.data.frame(x$terminal_moves); if (!nrow(tm)) return(NULL)
  data.frame(round = seq_len(nrow(tm)), kind = ifelse(seq_len(nrow(tm)) <= L, "burn_in", "measured"),
             distinct = x$terminal_distinct, tm, check.names = FALSE)
}
slim <- function(x) { x$rb_round <- NULL; x }   # calibration islands: drop the per-round RB matrices

# --- 2. tier-0 calibration, frozen grid ----------------------------------------------------------------------------------
runtime <- .v3cpp$cpp_runtime_new(as.numeric(arg$hours), proc.time()[["elapsed"]] - t_origin)
state <- .v3cpp$cpp_cal_new(setup$ptr, as.numeric(seed), list(cache_capacity = as.numeric(500 * p)), runtime)
t0 <- proc.time()[["elapsed"]]
tier <- v3_cal_tier(state, setup, 0, runtime, grid_fallback = FALSE)
cal_s <- proc.time()[["elapsed"]] - t0
grid <- tier$grid; grid_source <- "candidate grid"
if (is.null(grid)) { grid <- tier$pilot$schedule; grid_source <- "pilot schedule (grid construction failed or calibration stopped)" }
rec$calibration <- list(status = tier$status, seconds = cal_s, H = H0, T_pilot = length(tier$pilot$schedule) - 1L, rebuilds = tier$rebuilds,
  converged = tier$converged, triggers = tier$triggers, grid = grid, grid_source = grid_source, T_grid = length(grid) - 1L,
  tier_seconds = tier$seconds,
  diag_sd = vapply(tier$iterations, function(it) if (length(it$log_Z_r) == 4) stats::sd(it$log_Z_r) else NA_real_, 0),
  diag_seconds = vapply(tier$iterations, function(it) it$seconds[["islands"]], 0),
  pilot_stage_table = if (!is.null(tier$pilot$stage_record)) stage_table(tier$pilot$stage_record, Ncal) else NULL,
  iterations = lapply(tier$iterations, function(it) list(iteration = it$iteration, grid = it$grid, grid_label = it$grid_label,
    streams = it$streams, log_Z_r = it$log_Z_r, island_best = it$island_best, seconds = it$seconds,
    stage_tables = lapply(it$stage_record, stage_table, N = H0), islands = lapply(it$stage_record, slim))))
say("calibration H=%d: status %s, T_pilot %d, rebuilds %s, T_grid %d (%s), %.0f s; diagnostic sd: %s", H0, tier$status,
    rec$calibration$T_pilot, format(tier$rebuilds), rec$calibration$T_grid, grid_source, cal_s, paste(round(rec$calibration$diag_sd, 2), collapse = " "))
save_rec()
stopifnot(identical(tier$status, "ok"))
ex <- .v3cpp$cpp_cal_export(state); rm(state); invisible(gc())

# --- 3. final islands on the frozen grid: one call (islands 1..R = streams 10..9+R, as B3) ------------------------------
frozen <- v3_frozen(grid, tier = 0, N = Nisl, L = b$L, inherited = ex$inherited, budgets = b)
ro <- v3_run_settings(setup, frozen, ls0 = FALSE); ro$N <- as.integer(Nisl); ro$islands <- R
rec$final_settings <- list(N = Nisl, islands = R, L = ro$L, measured_rounds = ro$measured_rounds, ell = ro$ell, tier = ro$tier,
                           T = length(grid) - 1L, inherited_models = length(ex$inherited$models))
say("final run: %d islands of N = %d on T = %d stages (guard %.2f h, %.2f h used)", R, Nisl, length(grid) - 1L, as.numeric(arg$hours),
    (proc.time()[["elapsed"]] - t_origin) / 3600)
t0 <- proc.time()[["elapsed"]]
raw <- .v3cpp$cpp_final_run(setup$ptr, frozen[["grid"]], ro, as.numeric(seed), frozen[["inherited"]], runtime)
secs <- proc.time()[["elapsed"]] - t0
all_isl <- Filter(Negate(is.null), raw$islands)
isl <- Filter(function(x) !isTRUE(x$partial), all_isl)
lz <- vapply(isl, function(x) x$log_Z, 0)
st_tabs <- lapply(all_isl, stage_table, N = Nisl)
term_tabs <- lapply(all_isl, terminal_table, L = ro$L)
P <- if (length(isl)) do.call(cbind, lapply(isl, function(x) x$pip)) else NULL
act <- match(dat$active, pre$kept)
top <- raw$ledger$top
Fv <- as.numeric(top$value); lse <- function(v) { m <- max(v); m + log(sum(exp(v - m))) }
keepK <- if (identical(arg$store_models, "all")) length(top$models) else min(length(top$models), as.integer(arg$store_models))
store <- list(F = Fv, size = lengths(top$models), models = top$models[seq_len(keepK)], models_kept = keepK, capacity = top$capacity, full = top$full,
              log_sum_exp_F = if (length(Fv)) lse(Fv) else NA_real_, scope = rec$meta$not_reachable[["per_island_store"]],
              leaders_gamma0_value = as.numeric(raw$ledger$leaders_gamma0$value))
rec$final <- list(status = raw$status, message = raw$message, seconds = secs, islands_requested = R, islands_done = length(isl),
  islands_returned = length(all_isl), log_Z_r = lz, sd_log_Z_r = if (length(lz) >= 2) stats::sd(lz) else NA_real_,
  island_seconds = vapply(all_isl, function(x) sum(x$seconds), 0), island_partial = vapply(all_isl, function(x) isTRUE(x$partial), FALSE),
  stage_tables = st_tabs, terminal_tables = term_tabs,
  islands = all_isl,                                   # complete core records (phi, log_increment, ess, ..., rb_round, pip, stream)
  pip_eq_active = if (!is.null(P)) rowMeans(P)[act] else NULL,
  hpm = raw$ledger$hpm, hpm_equals_truth = identical(as.integer(raw$ledger$hpm$model), as.integer(sort(dat$active))),
  hpm_before_local = raw$hpm_before_local, local_search = raw$local_search[setdiff(names(raw$local_search), c("path", "scanned_centres"))],
  island_best = raw$ledger$island_best, logical = raw$ledger$logical, fresh = raw$ledger$fresh, cache = raw$cache,
  seconds_local = raw$seconds_local, seconds_total = raw$seconds_total, log_m0 = raw$log_m0, log_Zbar0 = raw$log_Zbar0,
  store = store)

# per-stage dispersion over the islands that finished (the quantity G0 asks for)
if (length(isl) >= 2) {
  done <- which(!rec$final$island_partial)
  S <- st_tabs[done]; T <- min(vapply(S, nrow, 0L))
  M <- function(col) sapply(S, function(d) d[[col]][seq_len(T)])
  inc <- M("log_increment")
  rec$final$stage_dispersion <- data.frame(stage = seq_len(T), phi = S[[1]]$phi[seq_len(T)], mean_inc = rowMeans(inc), var_inc = apply(inc, 1, stats::var),
    cum_var = apply(M("cum_log_Z"), 1, stats::var), mean_ess_share = rowMeans(M("ess_share")), min_ess_share = apply(M("ess_share"), 1, min),
    mean_distinct_resampled = rowMeans(M("distinct_resampled")), mean_distinct_moved = rowMeans(M("distinct_moved")),
    mean_gibbs_change_per_particle = rowMeans(M("gibbs_state_changes")) / Nisl)
}

# --- 4. line-up with the B3 census record (read-only; optional) ------------------------------------------------------------
if (nzchar(arg$b3_rds) && file.exists(arg$b3_rds)) {
  b3 <- readRDS(arg$b3_rds); r3 <- b3$runs[[as.character(Nisl)]]
  m <- if (is.null(r3)) 0L else min(length(lz), length(r3$log_Z_r))
  rec$b3_lineup <- list(file = arg$b3_rds, grid_identical = identical(b3$calibration$grid, grid),
    T_grid_b3 = b3$calibration$T_grid, islands_compared = m,
    log_Z_r_identical = if (m > 0) identical(lz[seq_len(m)], r3$log_Z_r[seq_len(m)]) else NA,
    max_abs_diff_log_Z_r = if (m > 0) max(abs(lz[seq_len(m)] - r3$log_Z_r[seq_len(m)])) else NA_real_)
  say("B3 line-up: grid identical %s; log Z_r identical on %d islands: %s (max |diff| %.3g)", rec$b3_lineup$grid_identical, m,
      rec$b3_lineup$log_Z_r_identical, rec$b3_lineup$max_abs_diff_log_Z_r)
}

say("final: status %s, %d of %d islands (%d returned), %.0f s (%.0f s per island); sd(log Z_r) %.3f; HPM = truth %s; store %d of %.0f (log sum e^F %.3f)",
    raw$status, length(isl), R, length(all_isl), secs, mean(rec$final$island_seconds), rec$final$sd_log_Z_r, rec$final$hpm_equals_truth,
    length(Fv), top$capacity, store$log_sum_exp_F)
if (!is.null(rec$final$stage_dispersion)) {
  d <- rec$final$stage_dispersion
  say("per-stage var(log increment) over islands: sum %.4f, largest %.4f at stage %d (phi %.4g); var(log Z_r) %.4f",
      sum(d$var_inc), max(d$var_inc), which.max(d$var_inc), d$phi[which.max(d$var_inc)], stats::var(lz))
}
rec$meta$finished_utc <- ws_utc(); rec$meta$total_seconds <- proc.time()[["elapsed"]] - t_origin; rec$meta$peak_gib <- ws_mem()[["hwm_kb"]] / 2^20
rec$status <- if (identical(raw$status, "completed")) "done" else paste0("final_run_", raw$status)
save_rec(); cat("DONE\n")
