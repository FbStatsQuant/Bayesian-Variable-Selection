args <- commandArgs(TRUE)
stopifnot(length(args) == 5L)
core <- normalizePath(args[1], mustWork = TRUE)
side <- args[2]; out <- args[3]; id <- as.integer(args[4]); testdir <- normalizePath(args[5])
source(file.path(testdir, "common.R"))
dir.create(out, recursive = TRUE, showWarnings = FALSE)
before <- sha_tree(core)
tests_before <- sha_tree(testdir)
v2_units <- c("v2_preprocess_units.R", "v2_runtime_units.R")
if (side == "production") need(all(v2_units %in% names(tests_before)), "required R-5 v2 unit source missing")
# Retain the literal source bytes alongside hashes, not only parsed R expressions.
test_bytes <- setNames(lapply(names(tests_before), function(f)
  readBin(file.path(testdir, f), what = "raw", n = file.info(file.path(testdir, f))$size)), names(tests_before))
saveRDS(test_bytes, file.path(out, "test_source_bytes.rds"), version = 3)
seeds <- read.delim(file.path(testdir, "seeds.tsv"))
need(id %in% seeds$index, "unknown fixed seed row")
seed <- seeds$seed[match(id, seeds$index)]
meta <- list(core = core, side = side, index = id, seed = seed,
             utc = format(Sys.time(), tz = "UTC", usetz = TRUE), host = Sys.info(),
             pid = Sys.getpid(), priority = system2("ps", c("-o", "ni=", "-p", Sys.getpid()), stdout=TRUE),
             execution = "Owls sequential persistent runner (AMENDMENT 1)",
             source_sha256 = before, test_source_sha256 = tests_before,
             session = capture.output(sessionInfo()), command = commandArgs())
saveRDS(meta, file.path(out, "metadata.rds"), version = 3)
load_test_core(core, file.path(out, "build"), testdir)
results <- list()
unit_catalog <- list(); current_unit_source <- "worker.R"
add <- function(label, expr) {
  need(!(label %in% names(results)), paste("duplicate unit label", label))
  unit_catalog[[label]] <<- list(source = current_unit_source,
    sha256 = unname(tests_before[[current_unit_source]]))
  r <- record(label, expr); results[[label]] <<- r
  saveRDS(results, file.path(out, "unit_results.rds"), version = 3)
  saveRDS(unit_catalog, file.path(out, "unit_catalog.rds"), version = 3)
  cat(if (r$ok) "PASS" else "FAIL", label, if (!r$ok) r$error else "", "\n")
  r$value
}
dat <- fixture(id); saveRDS(dat, file.path(out, "input.rds"), version = 3)
pre <- v3_preprocess(dat$X, dat$y)
ctx <- v3_context(pre$X, pre$y, orig = pre$kept)
setup <- v3_setup(ctx)
need(inherits(setup, "v3_setup"), "synthetic setup failed")
ro <- list(N = 7L + id %% 3L, L = 1L, measured_rounds = 4L, islands = 4L, tier = 0L,
           ell = 3L, dump_scored = FALSE, resampler_trace = FALSE,
           cache_capacity = as.numeric(max(500 * ctx$p, 2^15)))
grid <- c(0, .125, .5, .875, 1)
fr <- v3_frozen(grid, 0, N = ro$N, L = ro$L, budgets = setup$budgets)
# Observe the real resolver separately from the original micro-run override.
policy_fr <- v3_frozen(c(0, 1), 0, budgets = setup$budgets)
policy_ro <- if ("opts" %in% names(formals(v3_run_settings)))
  v3_run_settings(setup, policy_fr, list()) else v3_run_settings(setup, policy_fr)
cache_policy <- list(p = ctx$p, run_settings_capacity = policy_ro$cache_capacity)
raw <- .v3cpp$test_final(setup$ptr, grid, ro, seed, NULL)
assemble <- function(raw) {
  if ("opts" %in% names(formals(v3_assemble_final))) v3_assemble_final(raw, setup, fr, ro, seed, list())
  else v3_assemble_final(raw, setup, fr, ro, seed)
}
final <- assemble(raw)
need(final$status == "completed", "tiny actual final did not complete")
# Complete calibration at small internal settings, including continued diagnostic
# streams across two rebuilds and a tier-1 pilot. Production fit settings untouched.
calstate <- .v3cpp$cpp_cal_new(setup$ptr, seed, ro, NULL)
cal <- list()
cal$pilot <- .v3cpp$cpp_cal_pilot(calstate, 0L, 9L, 64L, 1L, 4L, 3L)
cal$rng_pilot <- .v3cpp$test_cal_rng(calstate)
for (it in 1:2) {
  V <- .v3cpp$cpp_cal_V(calstate)
  g <- .v3cpp$test_grid(V$log_gamma0, V$d, cal$pilot$schedule, 64L)
  need(g$ok, "calibration micro grid failed; fixture must be investigated")
  cal[[paste0("V", it)]] <- V; cal[[paste0("grid", it)]] <- g
  cal[[paste0("diag", it)]] <- .v3cpp$cpp_cal_diag(calstate, 0L, g$grid, 9L, 1L, 4L, 3L, it)
  cal[[paste0("rng_diag", it)]] <- .v3cpp$test_cal_rng(calstate)
}
cal$tier1_pilot <- .v3cpp$cpp_cal_pilot(calstate, 1L, 11L, 64L, 1L, 4L, 3L)
cal$rng_tier1 <- .v3cpp$test_cal_rng(calstate)
for (it in 1:2) {
  V <- .v3cpp$cpp_cal_V(calstate)
  g <- .v3cpp$test_grid(V$log_gamma0, V$d, cal$tier1_pilot$schedule, 64L)
  need(g$ok, "tier-1 micro grid failed; inspect fixture")
  cal[[paste0("tier1_V", it)]] <- V; cal[[paste0("tier1_grid", it)]] <- g
  cal[[paste0("tier1_diag", it)]] <- .v3cpp$cpp_cal_diag(calstate, 1L, g$grid, 11L, 1L, 4L, 3L, it)
  cal[[paste0("rng_tier1_diag", it)]] <- .v3cpp$test_cal_rng(calstate)
}
cal$export <- .v3cpp$cpp_cal_export(calstate)
inherited <- cal$export$inherited
aftercal <- .v3cpp$test_final(setup$ptr, grid, ro, seed, inherited)
# Run the actual R calibration/rebuild/escalation orchestrator in a testing-only
# function environment, substituting only its fixed-budget resolver. This keeps
# the full trigger aggregation/freeze logic under regression without new options.
ce <- new.env(parent = globalenv())
ce$v3_cal_settings <- function(setup, ...) {
  dots <- list(...)
  tier <- if ("tier" %in% names(dots)) dots$tier else tail(dots, 1)[[1]]
  # Reference calls (setup,opts,tier); production calls (setup,tier).
  list(tier = tier, H = as.integer(9 * 4^tier), T_e = 64L,
       L = 1L, Hm = 4L, ell = 2L)
}
ce$v3_cal_tier <- v3_cal_tier; environment(ce$v3_cal_tier) <- ce
calfun <- v3_calibrate; environment(calfun) <- ce
calibration_full <- if ("opts" %in% names(formals(calfun)))
  calfun(setup, seed, opts = list()) else calfun(setup, seed)
need(calibration_full$status %in% c("ok", "schedule_limit"), "full small calibration failed")
if (calibration_full$status == "ok") {
  # Final uses real inherited leaders and frozen grid from the whole orchestrator.
  calibrated_final <- .v3cpp$test_final(setup$ptr, calibration_full$frozen$grid, ro, seed,
                                       calibration_full$frozen$inherited)
} else calibrated_final <- NULL
micro <- .v3cpp$test_islands(setup$ptr, grid, seed, ro$N, ro$L, ro$ell, 10L, FALSE, 64L)
pilot_micro <- .v3cpp$test_islands(setup$ptr, grid, seed, 9L, 1L, 3L, 0L, TRUE, 64L)
models <- c(list(integer()), lapply(pre$kept, function(j) as.integer(j)),
            list(as.integer(head(pre$kept, ctx$K)), as.integer(tail(pre$kept, ctx$K))))
scores <- lapply(models, function(S) v3_score(ctx, S))
locals <- lapply(models, function(S) .v3cpp$test_local(setup$ptr, S, 1L))
resampling <- list()
for (j in 1:5) {
  lw <- switch(j, c(-Inf, 0, -Inf, -Inf, 0, -Inf), rep(0, 7),
               c(0, -745, -Inf, -30, -.1, -Inf), c(-1e3, -500, 0, -Inf, -1e3),
               c(-Inf, -Inf, 0, -Inf))
  w <- .v3cpp$test_resample(setup$ptr, lw, numeric(), seed)$W_reference
  u <- c(0, .Machine$double.xmin * .Machine$double.eps, w[w < 1],
         .v3cpp$test_adjacent(w[w > 0 & w < 1], FALSE),
         .v3cpp$test_adjacent(w[w > 0 & w < 1], TRUE), 1 - .Machine$double.eps/2)
  probes <- rep(u, length.out = length(lw) * ceiling(length(u)/length(lw)))
  rr <- lapply(split(probes, ceiling(seq_along(probes)/length(lw))), function(q)
    .v3cpp$test_resample(setup$ptr, lw, unname(q), seed))
  for (r in rr) {
    need(r$prescribed_count == length(lw), "resampler did not consume exactly N uniforms")
    need(r$draw_count == 0, "resampler drew RNG when supplied complete testing uniforms")
  }
  resampling[[j]] <- list(logw = lw, uniforms = probes, prescribed = rr,
                          seeded = .v3cpp$test_resample(setup$ptr, lw, numeric(), seed))
}
cal_rules <- list()
for (te in c(2000L, 4000L, 16000L)) {
  z <- .v3cpp$test_schedule(c(0, 1e15), 2, te)
  cal_rules[[paste0("fully_forced_", te)]] <- z
  add(paste0("RC2_forced_count_", te), {
    need(tail(z$grid %||% z$schedule, 1) == 1, "forced pilot failed exact endpoint")
    need(z$forced_pilot_steps == te, "fully forced pilot has wrong forced count")
    TRUE
  })
}
add("RC2_unforced_near_one_never_snaps", {
  z <- lapply(c(1, 2, 3, 5, 7, 9) * 1e-13, function(e)
    .v3cpp$test_pilot(c(0, log(2) * (1 + e)), 0, 2, 1000L))
  need(any(vapply(z, function(r) !r$forced && r$phi >= 1 - 1e-12 && r$phi < 1, TRUE)),
       "no unsnapped non-forced endpoint in snap window")
  cal_rules$unforced <- z; TRUE
})
add("RC2_forced_snap_retains_forced_flag", {
  z <- .v3cpp$test_pilot(c(0, 1e15), 1 - 1/2000 - 5e-13, 2, 2000L)
  need(z$forced && z$phi == 1, "forced near-one endpoint not snapped/countable")
  cal_rules$forced_endpoint <- z; TRUE
})
add("RC2_grid_validates_after_snap", {
  z <- lapply(c(1, 2, 3, 5, 7, 9) * 1e-13, function(e)
    .v3cpp$test_grid(c(0, 0), c(0, log(2) * (1 + e)), c(0, 1), 100L))
  need(any(vapply(z, function(r) !r$ok && r$reason == "validation_failed", TRUE)),
       "snapped grid endpoint bypassed restricted-ESS validation")
  cal_rules$grid_invalid <- z; TRUE
})
add("RC2_grid_interval_count_after_append", {
  z <- .v3cpp$test_grid(c(0, 0), c(0, 0), c(0, .5, 1), 1L)
  need(!z$ok && z$reason == "too_many_intervals" && length(z$grid) == 3,
       "interval limit not tested after append")
  cal_rules$grid_limit <- z; TRUE
})
bundle <- list(pre = pre, budgets = setup$budgets, blocks = setup$blocks, tables = setup$tables,
               neighbours = setup$neighbours, start = setup$start[setdiff(names(setup$start), "ptr")],
               scores = scores, locals = locals, exact = v3_enumerate(ctx),
               rng = lapply(0:13, function(st) .v3cpp$test_rng(seed, st, 41L)),
               resampling = resampling, micro = micro, pilot_micro = pilot_micro,
               raw_final = raw, final = final, calibration = cal, final_inherited = aftercal,
               calibration_full = calibration_full, calibrated_final = calibrated_final,
               cal_rules = cal_rules, cache_policy = cache_policy)
saveRDS(bundle, file.path(out, "raw_results.rds"), version = 3)
if (side == "production") {
  current_unit_source <- "changed_units.R"
  source(file.path(testdir, current_unit_source), local = globalenv())
  for (unit_file in v2_units) {
    current_unit_source <- unit_file; previous <- names(results)
    source(file.path(testdir, unit_file), local = globalenv())
    need(length(setdiff(names(results), previous)) > 0L, paste("unit source registered no tests", unit_file))
  }
}
current_unit_source <- "worker.R"
after <- sha_tree(core)
add("source_tree_unchanged", { exact(before, after); TRUE })
add("test_source_bytes_unchanged", {
  exact(tests_before, sha_tree(testdir), "tests/source hashes")
  saved <- readRDS(file.path(out, "test_source_bytes.rds"))
  exact(names(saved), names(tests_before), "tests/source byte inventory")
  for (f in names(saved)) exact(digest::digest(saved[[f]], algo = "sha256", serialize = FALSE),
    unname(tests_before[[f]]), paste0("tests/source bytes/", f))
  TRUE
})
meta$session_after <- capture.output(sessionInfo()); meta$source_sha256_after <- after
meta$test_source_sha256_after <- sha_tree(testdir)
saveRDS(meta, file.path(out, "metadata.rds"), version = 3)
saveRDS(results, file.path(out, "unit_results.rds"), version = 3)
quit(status = if (all(vapply(results, `[[`, TRUE, "ok"))) 0L else 1L)
