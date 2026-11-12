# profile_fit.R -- W3-SCALE leg A profiling driver (time and peak memory by phase; stage counts).
# The core in --core-dir is used unmodified. mode = full: the v3_fit flow, phase by phase (same calls, same order, same
# arguments as v3_fit), except that only the shipped memory-only preflight gates the run; the LS0 worst-case preflight
# verdict of the core is computed and recorded ("preflight bypassed in a copy", SCALING_DESIGN_v0 section 6.1).
# mode = setup: stops after the setup (hashes of blocks, tables, start, neighbour graph). mode = island: setup + one adaptive pilot island with H = --n-island particles + one fixed-grid island with
# N = --n-island on the grid built from that pilot (for p where a full fit is out of reach).
# Usage: Rscript --vanilla profile_fit.R --core-dir D --design prodh:p1000_S3_r001_c100 | s3gen --p P --seed S
#          --mode full|island --n-island 2500 --mem-gb G --hours H --out FILE.rds [--save-fit 1]
local({
  a <- grep("^--file=", commandArgs(FALSE), value = TRUE)
  assign("WS_DIR", if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd(), envir = globalenv())
})
source(file.path(WS_DIR, "ws_common.R"))
arg <- ws_args(list(core_dir = NA, design = "s3gen", p = "1000", seed = "20261111", mode = "full", n_island = "2500",
                    mem_gb = "8", hours = "23", out = NA, save_fit = "0", gen_dir = "/home/fb31/projects/BVS/Data_Generation/high_p",
                    manifest = "/home/fb31/projects/BVS/Data_Generation/manifests/high_p/inputs_manifest.csv", ls0 = "1"))
stopifnot(!is.na(arg$core_dir), !is.na(arg$out))
p_arg <- as.integer(arg$p); seed <- as.numeric(arg$seed); mem_gb <- as.numeric(arg$mem_gb); hours <- as.numeric(arg$hours)
ls0 <- arg$ls0 == "1"

prof <- list(meta = list(args = arg, host = Sys.info()[["nodename"]], started_utc = ws_utc(), R = R.version.string,
                         cpu = tryCatch(sub(".*: ", "", grep("model name", readLines("/proc/cpuinfo"), value = TRUE)[1]), error = function(e) NA),
                         slurm_job = Sys.getenv("SLURM_JOB_ID"), mem_reset_works = ws_mem_reset()),
             phases = NULL)
t_origin <- proc.time()[["elapsed"]]
save_prof <- function() { tmp <- paste0(arg$out, ".tmp"); saveRDS(prof, tmp); file.rename(tmp, arg$out) }
# ph(name, expr): evaluate expr, record wall seconds, the peak resident memory during the phase and the resident
# memory after it; write the progress file.
ph <- function(name, expr) {
  ws_mem_reset(); t0 <- proc.time()[["elapsed"]]
  val <- force(expr)
  dt <- proc.time()[["elapsed"]] - t0; m <- ws_mem()
  prof$phases <<- rbind(prof$phases, data.frame(phase = name, seconds = dt, peak_kb = m[["hwm_kb"]], rss_after_kb = m[["rss_kb"]],
                                                 elapsed_end = proc.time()[["elapsed"]] - t_origin, stringsAsFactors = FALSE))
  cat(sprintf("[%s] %-28s %10.2f s  peak %8.1f MB  rss %8.1f MB\n", ws_utc(), name, dt, m[["hwm_kb"]] / 1024, m[["rss_kb"]] / 1024))
  save_prof()
  val
}

ph("compile_and_load", source(file.path(arg$core_dir, "v3.R")))
prof$meta$core_key <- V3_CPP_KEY

dat <- ph("generate_data", {
  if (grepl("^prodh:", arg$design)) {
    id <- sub("^prodh:", "", arg$design)
    m <- regmatches(id, regexec("^p(\\d+)_S(\\d)_r(\\d+)_(c\\d+)$", id))[[1]]
    stopifnot(length(m) == 5)
    d <- ws_prodh(as.integer(m[2]), as.integer(m[3]), as.integer(m[4]), m[5], arg$gen_dir, arg$manifest)
    seed <<- d$method_seed
    d
  } else ws_gen_s3(p_arg, 200L, as.integer(seed) %% 100000L + 7000000L)
})
X <- dat$X; y <- dat$y
prof$meta$dataset_id <- dat$dataset_id; prof$meta$manifest_match <- dat$manifest_match %||% NA
prof$meta$method_seed <- seed; prof$meta$active <- dat$active
cat("dataset", dat$dataset_id, "manifest_match", prof$meta$manifest_match, "method seed", seed, "\n")

allocation <- list(mem_gb = mem_gb, hours = hours)
runtime <- .v3cpp$cpp_runtime_new(allocation$hours, proc.time()[["elapsed"]] - t_origin)
pre <- ph("preprocess", v3_preprocess(X, y, dup_components = FALSE))
stopifnot(pre$status == "ok")
n <- pre$n; p <- pre$p
b <- v3_budgets(n, p)
prof$budgets <- b[c("n", "p", "K", "B", "ell", "L", "N0", "H0", "T0")]
stopifnot(!b$exact_branch)
tcache <- list()
time_fun <- function(k) { key <- as.character(k); if (is.null(tcache[[key]])) tcache[[key]] <<- v3_time_scores(pre$X, pre$y, k); tcache[[key]] }
# The core's own v3.1 preflight (LS0 worst case charged) at the default allocation (8 GiB, 24 h) and at this job's.
prof$preflight <- ph("preflight_record", {
  pf24 <- v3_preflight(n, p, b, "smc", list(mem_gb = 8, hours = 24), time_fun = time_fun, ls0_worst_case = ls0)
  pfjob <- v3_preflight(n, p, b, "smc", list(mem_gb = mem_gb, hours = 24), time_fun = time_fun, ls0_worst_case = ls0)
  sK <- time_fun(b$K)
  list(default_8g_24h = pf24[c("est_bytes", "memory_components", "exceeds", "ls0_worst_case")],
       job_mem_24h = pfjob[c("est_bytes", "exceeds", "ls0_worst_case")], seconds_per_size_K_score = sK)
})
pf_mem <- v3_preflight(n, p, b, "smc", allocation, time_fun = time_fun, ls0_worst_case = FALSE)   # shipped: memory only
if (pf_mem$exceeds) { prof$status <- "memory_preflight_refused"; save_prof(); quit(status = 3) }

ctx <- ph("context_gram", v3_context(pre$X, pre$y, orig = pre$kept, return_gram = FALSE))
dup <- ph("dup_components", .v3cpp$cpp_dup_components(ctx))
setup <- ph("setup_total", v3_setup(ctx))
stopifnot(inherits(setup, "v3_setup"))
prof$setup <- list(seconds = setup$seconds, J = length(setup$blocks), block_sizes = table(lengths(setup$blocks)),
                   neighbours = summary(lengths(setup$neighbours)), log_Zbar0 = setup$start$log_Zbar0)
cg <- ph("cut_group", .v3cpp$cpp_cut_group(setup$ptr))

guard_table <- function() {
  g <- .v3cpp$cpp_runtime_report(runtime)$checkpoints
  if (!length(g)) return(NULL)
  do.call(rbind, lapply(g, function(x) as.data.frame(x[c("checkpoint", "phase", "tier", "iter", "island", "stage", "elapsed_seconds", "operation_seconds")], stringsAsFactors = FALSE)))
}
island_summary <- function(x) list(T = length(x$phi), seconds = x$seconds, log_Z = x$log_Z, min_ess = if (length(x$ess)) min(x$ess) else NA,
                                   phi = x$phi, ess = x$ess, distinct_moved = x$distinct_moved, partial = isTRUE(x$partial))

if (arg$mode == "full") {
  pf_fun <- function(e) v3_preflight(n, p, b, "smc", allocation, tier = e, time_fun = time_fun, ls0_worst_case = FALSE)$exceeds
  cal <- ph("calibration", v3_calibrate(setup, seed, preflight = pf_fun, runtime = runtime,
                                        grid_fallback = isTRUE(ls0) && isTRUE(getOption("v3.grid_fallback", TRUE))))
  prof$calibration <- list(status = cal$status, tier_final = cal$tier_final, escalated = cal$escalated, seconds = cal$seconds,
    flags = cal$flags[c("escalated", "forced_pilot_steps", "grid_unconverged", "triggers_fired")], cache = cal$cache,
    tiers = lapply(cal$tiers, function(t) list(tier = t$tier, status = t$status, seconds = t$seconds, rebuilds = t$rebuilds,
      converged = t$converged, triggers = t$triggers, T_pilot = length(t$pilot$schedule) - 1L, forced_pilot_steps = t$pilot$forced_pilot_steps,
      pilot = island_summary(t$pilot$stage_record), pilot_seconds = t$pilot$seconds,
      T_grid = if (is.null(t$grid)) NA else length(t$grid) - 1L,
      grids = lapply(t$grids, function(g) list(label = g$label, intervals = g$intervals, ok = g$ok, seconds = g$seconds, F_V_evaluations = g$F_V_evaluations)),
      V_sizes = vapply(t$snapshots, function(s) s$size, 0),
      iterations = lapply(t$iterations, function(it) list(iteration = it$iteration, T = length(it$grid) - 1L, seconds = it$seconds,
        log_Z_r = it$log_Z_r, E1 = it$E1, E2 = it$E2, E3 = it$E3, islands = lapply(it$stage_record, island_summary),
        local_moves = it$local_search$moves, local_n_evaluated = it$local_search$n_evaluated)))))
  prof$guard <- guard_table(); save_prof()
  fit_tail <- NULL
  if (cal$status == "ok") {
    frozen <- cal$frozen
    fr <- ph("final_run", v3_final_run(setup, frozen, seed, runtime, ls0 = ls0))
    prof$final <- list(status = fr$status, T = length(frozen$grid) - 1L, tier = frozen$tier, N = fr$settings$N, grid = frozen$grid,
      islands = lapply(fr$stage_record, function(x) if (is.null(x)) NULL else island_summary(x)),
      timings = fr$timings, log_Z = fr$log_Z, log_Z_r = fr$log_Z_r,
      sd_log_Z_r = if (length(fr$log_Z_r) >= 2 && !anyNA(fr$log_Z_r)) stats::sd(fr$log_Z_r) else NA,
      hpm = fr$hpm, hpm_F = fr$hpm_F, hpm_provenance = fr$hpm_provenance, hpm_equals_truth = identical(as.integer(fr$hpm), as.integer(sort(dat$active))),
      mpm = fr$mpm, flags = fr$flags, cache = fr$cache, score_counts = fr$score_counts,
      local = fr$local_search[c("moves", "n_evaluated", "termination", "scan_size")],
      ls0 = fr$ls0[c("moves", "n_evaluated", "termination", "scan_size", "move_cap")], start_mode = fr$start_mode[c("ties", "truncated", "tie_dp_used")],
      top_store_size = length(fr$top_store$value))
    fit_tail <- fr
  }
  prof$guard <- guard_table()
  prof$numerical_routes <- .v3cpp$cpp_numerical_routes(ctx)
  # A fit object with the fields of v3_fit (for the fingerprint: identical inputs give identical bits across cores).
  fit <- list(seed = seed, status = if (is.null(fit_tail)) cal$status else fit_tail$status, n = n, p = p, budgets = b, B = b$B,
              preprocessing = c(pre[setdiff(names(pre), c("X", "y"))], list(dup_components = dup)),
              blocks = setup$blocks, neighbours = setup$neighbours, log_Zbar0 = setup$start$log_Zbar0,
              cut_group = cg$cut_group, cut_group_count = cg$count, cut_group_components = cg$components,
              calibration = cal, numerical_routes = prof$numerical_routes)
  if (!is.null(fit_tail)) for (nm in names(fit_tail)) fit[[nm]] <- fit_tail[[nm]]
  prof$fingerprint <- ph("fingerprint", ws_fingerprint(fit))
  prof$tables_sha <- ph("tables_hash", ws_sha(setup$tables))
  if (arg$save_fit == "1") ph("save_fit", saveRDS(fit, sub("\\.rds$", "_fit.rds", arg$out)))
} else if (arg$mode == "setup") {
  # Setup only (data, Gram, blocks, tables, start, neighbour graph): times, memory and hashes of the setup objects.
  prof$numerical_routes <- .v3cpp$cpp_numerical_routes(ctx)
  prof$tables_sha <- ph("tables_hash", ws_sha(setup$tables))
} else {
  # One adaptive pilot island with H particles, then one fixed-grid island with N particles on the grid built from it.
  Nisl <- as.integer(arg$n_island)
  state <- .v3cpp$cpp_cal_new(setup$ptr, as.numeric(seed), list(cache_capacity = as.numeric(500 * p)), runtime)
  pil <- ph("pilot_island", .v3cpp$cpp_cal_pilot(state, 0L, Nisl, as.integer(b$tiers$T[1]), as.integer(b$L), 4L, as.integer(b$ell)))
  prof$pilot <- list(status = pil$status, T = length(pil$schedule) - 1L, forced = pil$forced_pilot_steps, seconds = pil$seconds,
                     island = island_summary(pil$island), schedule = pil$schedule,
                     local_moves = pil$local_search$moves, local_n_evaluated = pil$local_search$n_evaluated,
                     best_before_local = pil$best_before_local$F, best_after_local = pil$best_after_local$F)
  prof$guard <- guard_table(); save_prof()
  if (identical(pil$status, "ok")) {
    V <- ph("cal_V", .v3cpp$cpp_cal_V(state))
    g <- ph("build_grid", v3_build_grid(V$log_gamma0, V$d, pil$schedule, as.integer(b$tiers$T[1])))
    prof$grid <- list(ok = g$ok, intervals = g$intervals, F_V_evaluations = g$F_V_evaluations, V_size = length(V$d), seconds = g$seconds)
    ex <- ph("cal_export", .v3cpp$cpp_cal_export(state))
    prof$calibration_cache <- ex$cache
    rm(state, V); invisible(gc())
    grid <- if (isTRUE(g$ok)) g$grid else pil$schedule
    frozen <- v3_frozen(grid, tier = 0, N = Nisl, L = b$L, inherited = ex$inherited, budgets = b)
    ro <- v3_run_settings(setup, frozen, ls0); ro$N <- Nisl; ro$islands <- 1L
    raw <- ph("final_island", .v3cpp$cpp_final_run(setup$ptr, frozen[["grid"]], ro, as.numeric(seed), frozen[["inherited"]], runtime))
    isl <- raw$islands[[1]]
    prof$final <- list(status = raw$status, T = length(grid) - 1L, N = Nisl, grid = grid, island = island_summary(isl),
      seconds_local = raw$seconds_local, seconds_ls0 = raw$seconds_ls0, seconds_total = raw$seconds_total, cache = raw$cache,
      hpm = raw$ledger$hpm$model, hpm_F = raw$ledger$hpm$F, hpm_equals_truth = identical(as.integer(raw$ledger$hpm$model), as.integer(sort(dat$active))),
      fresh = raw$ledger$fresh, logical = raw$ledger$logical, local = raw$local_search[c("moves", "n_evaluated", "scan_size")],
      ls0 = raw$ls0[c("moves", "n_evaluated", "scan_size", "move_cap")], start_mode = raw$start_mode[c("ties", "truncated", "tie_dp_used")],
      top_store_size = length(raw$ledger$top$value))
    prof$fingerprint_island <- list(pilot = ws_sha(ws_strip(pil)), final = ws_sha(ws_strip(raw)))
  }
  prof$guard <- guard_table()
  prof$numerical_routes <- .v3cpp$cpp_numerical_routes(ctx)
  prof$tables_sha <- ph("tables_hash", ws_sha(setup$tables))
}
prof$setup_hash <- list(blocks = ws_sha(setup$blocks), neighbours = ws_sha(setup$neighbours), start = ws_sha(setup$start[setdiff(names(setup$start), "ptr")]),
                        dup = ws_sha(dup), cut_group = ws_sha(cg), z = ws_sha(ctx$z))
prof$status <- "done"; prof$meta$finished_utc <- ws_utc(); prof$total_seconds <- proc.time()[["elapsed"]] - t_origin
save_prof()
cat("DONE", prof$total_seconds, "s\n")
