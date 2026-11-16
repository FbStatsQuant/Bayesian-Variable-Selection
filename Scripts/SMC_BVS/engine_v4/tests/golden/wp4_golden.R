# wp4_golden.R -- TEST CODE ONLY. WP4 golden bit tests against core/ (revision D), compat mode.
#   Rscript wp4_golden.R <core_dir> <engine_v4_dir> <work_dir> [quick|full] [threads]
# 1. Coded calibration (v4::calib::Driver, rule coded, SumMode::Serial) == core/v3_calib.R::v3_calibrate, bit for bit,
#    with threads 1 and k (V re-scoring and F_V terms threaded).
# 2. T9: final run as R' = 4 process islands + v4 merge + v4 threaded tail == core/v3_run.R::v3_final_run (v3.1, LS0
#    on), class B on every compared field (only `fresh` counters, cache statistics and timings are not compared).
# 3. T10 through the merge: missing / corrupt / hash-mismatch / numerically failed island, numerical failure in the
#    tail -> declared status, no estimate field.
# 4. Bounded rule (I_max = 0 and 1) and blocked sums run end to end (no reference: these are the V changes).
# core/ is copied to <work_dir> and never written. Budgets are reduced through setup$budgets (the same object is given
# to both implementations), as the core test suite does.
args <- commandArgs(TRUE)
core_dir <- normalizePath(args[1]); eng_dir <- normalizePath(args[2]); work <- args[3]
level <- if (length(args) >= 4) args[4] else "quick"
threads <- if (length(args) >= 5) as.integer(args[5]) else 3L
dir.create(work, recursive = TRUE, showWarnings = FALSE); work <- normalizePath(work)
`%||%` <- function(a, b) if (is.null(a)) b else a
options(warn = 1)

# ---- load core R code and compile core v3_core.cpp + the WP4 harness into one module ------------------------------
ref <- file.path(work, "core_ref"); unlink(ref, recursive = TRUE); dir.create(ref)
invisible(file.copy(list.files(core_dir, full.names = TRUE, all.files = FALSE), ref, recursive = TRUE))
unlink(file.path(ref, ".cpp_cache"), recursive = TRUE)
V3_CORE_DIR <- ref
for (f in c("v3_preprocess.R", "v3_setup.R", "v3_run.R", "v3_exact.R", "v3_calib.R", "v3_fit.R")) source(file.path(ref, f))
tu_dir <- file.path(work, "tu"); dir.create(tu_dir, showWarnings = FALSE)
tu <- file.path(tu_dir, "wp4_test_core.cpp")
writeLines(c(readLines(file.path(ref, "cpp", "v3_core.cpp")), "", readLines(file.path(eng_dir, "tests", "golden", "wp4_harness.cpp"))), tu)
Sys.setenv(PKG_CPPFLAGS = paste0("-I", file.path(ref, "cpp"), " -I", file.path(eng_dir, "include"), " -fopenmp"),
           PKG_LIBS = "-fopenmp", R_MAKEVARS_USER = file.path(ref, "cpp", "Makevars.v3"), MAKEFLAGS = "-j1")
.v3cpp <- new.env(parent = globalenv())
t_c <- proc.time()[["elapsed"]]
Rcpp::sourceCpp(tu, env = .v3cpp, cacheDir = file.path(work, "cache"), rebuild = FALSE, showOutput = FALSE)
cat(sprintf("compiled harness in %.1f s\n", proc.time()[["elapsed"]] - t_c))

# ---- strict comparison (as Scripts/SMC_BVS/tests/common.R: IEEE bits, no tolerance) --------------------------------
bits <- function(x) writeBin(as.double(x), raw(), size = 8L, endian = "little")
n_checks <- 0L; failures <- character()
same <- function(a, b, path) {
  ok <- if (is.null(a) || is.null(b)) is.null(a) && is.null(b)
        else if (is.list(a) && is.list(b)) {
          if (length(a) != length(b)) FALSE else { for (i in seq_along(a)) same(a[[i]], b[[i]], paste0(path, "[[", i, "]]")); TRUE }
        } else if (is.double(a) || is.double(b)) {
          length(a) == length(b) && identical(bits(unname(a)), bits(unname(b))) && identical(names(a), names(b))
        } else identical(unname(a), unname(b))
  n_checks <<- n_checks + 1L
  if (!isTRUE(ok)) { failures <<- c(failures, path); cat("  MISMATCH:", path, "\n") }
  invisible(ok)
}
expect <- function(cond, path) { n_checks <<- n_checks + 1L; if (!isTRUE(cond)) { failures <<- c(failures, path); cat("  FAIL:", path, "\n") } }

# ---- fixtures -------------------------------------------------------------------------------------------------------
fixture <- function(n, p, rho, seed, s0 = c(3, 7, 11, 19, 23)) {
  set.seed(seed)
  X <- matrix(0, n, p); X[, 1] <- rnorm(n)
  for (j in 2:p) X[, j] <- rho * X[, j - 1] + sqrt(1 - rho^2) * rnorm(n)
  s0 <- s0[s0 <= p]
  y <- drop(X[, s0, drop = FALSE] %*% rep(c(1, -0.8), length.out = length(s0))) + rnorm(n)
  list(X = X, y = y)
}
make_setup <- function(fx, H, Te, N, ell = NULL) {
  pre <- v3_preprocess(fx$X, fx$y, dup_components = FALSE)
  ctx <- v3_context(pre$X, pre$y, orig = pre$kept, return_gram = FALSE)
  st <- v3_setup(ctx)
  st$budgets$tiers$H <- as.integer(H); st$budgets$tiers$T <- as.integer(Te); st$budgets$tiers$N <- as.integer(N)
  if (!is.null(ell)) st$budgets$ell <- as.integer(ell)
  st
}
settings_for <- function(setup, rule = "coded", I_max = 3L, refine_m = 1L, sum_mode = "serial", th = 1L) {
  b <- setup$budgets
  tiers <- lapply(0:1, function(e) list(H = b$tiers$H[e + 1], T_e = b$tiers$T[e + 1], L = b$L, Hm = 4L, ell = b$ell))
  list(rule = rule, tier0 = 0L, grid_fallback = TRUE, I_max = as.integer(I_max), refine_m = as.integer(refine_m),
       sum_mode = sum_mode, threads = as.integer(th), tiers = tiers)
}

# ---- 1. coded calibration vs v3_calibrate -----------------------------------------------------------------------------
compare_calib <- function(r, m, tag) {
  same(r$status, m$status, paste(tag, "status")); same(as.integer(r$tier_final), m$tier_final, paste(tag, "tier_final"))
  same(r$escalated, m$escalated, paste(tag, "escalated"))
  same(length(r$tiers), length(m$tiers), paste(tag, "n_tiers"))
  for (i in seq_len(min(length(r$tiers), length(m$tiers)))) {
    a <- r$tiers[[i]]; b <- m$tiers[[i]]; tt <- paste0(tag, " tier", i - 1)
    same(a$status, b$status, paste(tt, "status")); same(a$triggers, b$triggers, paste(tt, "triggers"))
    same(a$pilot$schedule, b$schedule, paste(tt, "pilot schedule"))
    same(length(a$grids), length(b$grids), paste(tt, "n_grids"))
    for (g in seq_len(min(length(a$grids), length(b$grids)))) {
      ga <- a$grids[[g]]; gb <- b$grids[[g]]; gt <- paste0(tt, " grid", g)
      for (nm in c("label", "grid", "rho_appended", "ok", "reason", "intervals", "F_V_evaluations")) same(ga[[nm]], gb[[nm]], paste(gt, nm))
    }
    same(length(a$iterations), length(b$iterations), paste(tt, "n_iter"))
    for (k in seq_len(min(length(a$iterations), length(b$iterations)))) {
      ia <- a$iterations[[k]]; ib <- b$iterations[[k]]; it <- paste0(tt, " iter", k)
      for (nm in c("iteration", "grid", "rho_V", "grid_label", "log_Z_r", "island_best", "overall_best", "E1", "E2", "E3"))
        same(ia[[nm]], ib[[nm]], paste(it, nm))
    }
    for (nm in c("converged", "rebuilds", "grid", "rho_V", "grid_label", "grid_source")) same(a[[nm]], b[[nm]], paste(tt, nm))
  }
  for (nm in c("escalated", "escalation_blocked", "checks_passed_calibration", "forced_pilot_steps", "grid_unconverged",
               "triggers_fired", "grid_fallback")) same(r$flags[[nm]], m$flags[[nm]], paste(tag, "flags", nm))
  if (r$status == "ok") {
    same(r$frozen$grid, m$frozen$grid, paste(tag, "frozen grid")); same(r$frozen$tier, m$frozen$tier, paste(tag, "frozen tier"))
    same(r$frozen$rho_V, m$frozen$rho_V, paste(tag, "frozen rho_V")); same(r$frozen$grid_label, m$frozen$grid_label, paste(tag, "frozen label"))
  }
  same(r$hpm, m$hpm, paste(tag, "calibration HPM + provenance"))
  same(r$ledger$top, m$ledger$top, paste(tag, "calibration top store"))
  same(r$ledger$leaders_gamma0, m$ledger$leaders_gamma0, paste(tag, "leaders gamma0"))
  same(r$ledger$leaders_gamma1, m$ledger$leaders_gamma1, paste(tag, "leaders gamma1"))
  same(r$ledger$logical, m$ledger$logical, paste(tag, "logical counters"))
  same(r$ledger$island_best, m$ledger$island_best, paste(tag, "island_best"))
}

# ---- 2. T9 merge vs v3_final_run -------------------------------------------------------------------------------------
compare_final <- function(r, m, tag) {
  same(r$status, m$status, paste(tag, "status"))
  for (nm in c("hpm", "hpm_F", "hpm_provenance", "log_Z_r", "log_Z", "log_Z_lower95", "log_Z_rel_m0", "log_Z_r_rel_m0",
               "pip_primary", "mpm", "near_ties", "near_tie_F", "near_tie_truncated", "hpm_before_local",
               "hpm_before_ls0", "local_certified", "local_certified_by", "island_best"))
    same(r[[nm]], m[[nm]], paste(tag, nm))
  same(r$start_mode$model, m$start_mode, paste(tag, "start_mode"))
  same(unname(r$pip_r), unname(m$pip_r), paste(tag, "pip_r"))
  lsr <- r$local_search[c("centre", "centre_F", "path", "path_F", "scanned_centres", "scanned_F", "scan_complete", "scan_size",
                          "termination", "local_limit", "local_certified", "returned", "returned_F", "moves", "n_evaluated")]
  same(lsr, m$local_search[names(lsr)], paste(tag, "final local search archive"))
  l0 <- r$ls0[c(names(lsr), "move_cap")]
  same(l0, m$ls0[names(l0)], paste(tag, "LS0 archive"))
  fl <- c("E1", "E2", "E3", "low_empirical_ESS", "local_limit", "near_tie_truncated", "checks_passed_final", "final_local_limit",
          "ls0_local_limit", "ls0_improved", "ls0_hpm_changed")
  same(r$flags[fl], m$flags[fl], paste(tag, "flags"))
  same(r$top_store, m$top_store, paste(tag, "top store"))
  same(r$leaders_gamma0, m$leaders_gamma0, paste(tag, "leaders gamma0"))
  same(r$leaders_gamma1, m$leaders_gamma1, paste(tag, "leaders gamma1"))
  same(r$score_counts$logical, m$logical, paste(tag, "logical counters"))
}

cases <- list(
  list(id = "AR0.6_n100_p40",   n = 100, p = 40,   rho = 0.6, seed = 11, H = c(64, 128),  Te = c(60, 120),  N = c(150, 300), ell = NULL),
  list(id = "AR0.9_n120_p120",  n = 120, p = 120,  rho = 0.9, seed = 12, H = c(48, 96),   Te = c(40, 80),   N = c(120, 240), ell = 3),
  list(id = "IND_n80_p60_Te3",  n = 80,  p = 60,   rho = 0.0, seed = 13, H = c(32, 64),   Te = c(3, 4),     N = c(100, 200), ell = 2),
  list(id = "AR0.5_n150_p300",  n = 150, p = 300,  rho = 0.5, seed = 14, H = c(64, 128),  Te = c(60, 120),  N = c(200, 400), ell = 4))
if (level == "full") cases <- c(cases, list(
  list(id = "AR0.7_n200_p1000", n = 200, p = 1000, rho = 0.7, seed = 15, H = c(64, 128), Te = c(100, 200), N = c(150, 300), ell = NULL, heavy = TRUE),
  list(id = "AR0.8_n200_p2000", n = 200, p = 2000, rho = 0.8, seed = 16, H = c(48, 96), Te = c(80, 160), N = c(100, 200), ell = 6, heavy = TRUE)))

timing <- list()
for (cs in cases) {
  cat(sprintf("== case %s\n", cs$id))
  fx <- fixture(cs$n, cs$p, cs$rho, cs$seed)
  setup <- make_setup(fx, cs$H, cs$Te, cs$N, cs$ell)
  seed <- 1000L + cs$seed
  t0 <- proc.time()[["elapsed"]]; r <- v3_calibrate(setup, seed, tier = 0, preflight = NULL, runtime = NULL, grid_fallback = TRUE)
  t_ref <- proc.time()[["elapsed"]] - t0
  for (th in unique(c(1L, threads))) {
    m <- .v3cpp$wp4_calibrate(setup$ptr, seed, settings_for(setup, th = th))
    compare_calib(r, m, sprintf("%s calib[th=%d]", cs$id, th))
    timing[[length(timing) + 1]] <- data.frame(case = cs$id, what = sprintf("calibrate coded th=%d", th), ref_s = t_ref, wp4_s = m$seconds)
  }
  cat(sprintf("   calibration: status %s, tier %d, escalated %s, triggers {%s}, fallback %s\n", r$status, r$tier_final,
              r$escalated, paste(r$flags$triggers_fired, collapse = ","), r$flags$grid_fallback %||% "none"))
  if (r$status != "ok") next
  ro <- v3_run_settings(setup, r$frozen, ls0 = TRUE)
  t0 <- proc.time()[["elapsed"]]; fr <- v3_final_run(setup, r$frozen, seed, runtime = NULL, ls0 = TRUE)
  t_fr <- proc.time()[["elapsed"]] - t0
  variants <- if (isTRUE(cs$heavy)) list(c(threads, 64L)) else list(c(1L, 64L), c(1L, 4096L), c(threads, 64L), c(threads, 4096L))
  for (v in variants) { th <- v[1]; ch <- v[2]
    mm <- .v3cpp$wp4_final_merge(setup$ptr, r$frozen$grid, ro, as.numeric(seed), r$frozen$inherited, th, ch, "", 0L)
    compare_final(fr, mm, sprintf("%s T9[th=%d,chunk=%d]", cs$id, th, ch))
    timing[[length(timing) + 1]] <- data.frame(case = cs$id, what = sprintf("final th=%d chunk=%d (merge+tail part)", th, ch),
                                               ref_s = t_fr, wp4_s = sum(mm$seconds_islands) + mm$seconds_merge_tail)
  }
  if (isTRUE(cs$heavy)) next   # T10 and the bounded rule are size-independent logic: quick cases only
  # 3. T10 through the merge
  for (fault in c("missing", "corrupt", "hash_mismatch", "island_numerical", "tail_numerical")) {
    mm <- .v3cpp$wp4_final_merge(setup$ptr, r$frozen$grid, ro, as.numeric(seed), r$frozen$inherited, threads, 256L, fault, 3L)
    want <- switch(fault, missing = "io_error", corrupt = "invalid_input", hash_mismatch = "invalid_input",
                   island_numerical = "numerical_failure", tail_numerical = "numerical_failure")
    expect(identical(mm$status, want), sprintf("%s T10 %s status (%s)", cs$id, fault, mm$status))
    expect(!isTRUE(mm$estimates_available) && is.null(mm$log_Z) && is.null(mm$pip_primary) && is.null(mm$mpm),
           sprintf("%s T10 %s no estimate fields", cs$id, fault))
    if (fault == "tail_numerical") expect(isTRUE(mm$hpm_incomplete), sprintf("%s T10 tail HPM labelled incomplete", cs$id))
  }
  # 4. bounded rule and blocked sums: run, structural checks only
  for (im in c(0L, 1L)) {
    b <- .v3cpp$wp4_calibrate(setup$ptr, seed, settings_for(setup, rule = "bounded", I_max = im, refine_m = 4L, sum_mode = "blocked", th = threads))
    expect(b$status == "ok", sprintf("%s bounded I_max=%d status %s", cs$id, im, b$status))
    if (b$status == "ok") {
      expect(b$I_used <= im, sprintf("%s bounded I_used <= I_max", cs$id))
      expect(length(b$frozen$grid) == 4L * (length(b$frozen$grid_unrefined) - 1L) + 1L, sprintf("%s refine x4 length", cs$id))
      expect(all(diff(b$frozen$grid) > 0) && b$frozen$grid[1] == 0 && tail(b$frozen$grid, 1) == 1, sprintf("%s refined grid valid", cs$id))
      expect(all(b$frozen$grid_unrefined %in% b$frozen$grid), sprintf("%s refined grid contains the calibrated grid", cs$id))
      ntiers_esc <- vapply(b$tiers, function(t) isTRUE(t$triggers$grid_failure), TRUE)
      expect(length(b$tiers) == 1L || ntiers_esc[1], sprintf("%s bounded escalates only on grid failure", cs$id))
      last_gf <- isTRUE(b$tiers[[length(b$tiers)]]$triggers$grid_failure)
      if (im == 0L && !last_gf) expect(isTRUE(b$flags$grid_unconverged), sprintf("%s bounded I_max=0 flags grid_unconverged", cs$id))
    }
  }
  b1 <- .v3cpp$wp4_calibrate(setup$ptr, seed, settings_for(setup, rule = "bounded", I_max = 1L, sum_mode = "blocked", th = 1L))
  b3 <- .v3cpp$wp4_calibrate(setup$ptr, seed, settings_for(setup, rule = "bounded", I_max = 1L, sum_mode = "blocked", th = threads))
  same(b1$frozen, b3$frozen, sprintf("%s bounded+blocked thread invariance (frozen)", cs$id))
  same(b1$tiers, b3$tiers, sprintf("%s bounded+blocked thread invariance (tiers)", cs$id))
}

tim <- do.call(rbind, timing)
print(tim, row.names = FALSE)
write.table(tim, file.path(work, "wp4_golden_timing.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
cat(sprintf("\nWP4 golden: %d checks, %d failures\n", n_checks, length(failures)))
if (length(failures)) { cat(paste(" -", failures), sep = "\n"); quit(status = 1) }
