# wp4_golden.R -- TEST CODE ONLY. WP4 golden bit tests against core/ (revision D), compat mode.
#   Rscript wp4_golden.R <core_dir> <engine_v4_dir> <work_dir> [quick|full] [threads] [case id] [--keep]
# <work_dir> is removed at exit unless --keep is given (clean-tmp rule, BUILD_COMMON); empty directories held by the
# mapped module (NFS) are removed by run_tests.sh after R exits.
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
keep <- "--keep" %in% args; args <- args[args != "--keep"]   # --keep: leave <work_dir> (cache, core copy, TU) for debugging
core_dir <- normalizePath(args[1]); eng_dir <- normalizePath(args[2]); work <- args[3]
level <- if (length(args) >= 4) args[4] else "quick"
threads <- if (length(args) >= 5) as.integer(args[5]) else 3L
only <- if (length(args) >= 6) args[6] else ""   # optional: run one case id only (debugging)
dir.create(work, recursive = TRUE, showWarnings = FALSE); work <- normalizePath(work)
# Clean-up: unload the module's shared objects first (an open mapping leaves NFS .nfs* files that block the rmdir).
clean_work <- function() {
  for (d in getLoadedDLLs()) { pth <- d[["path"]]; if (startsWith(normalizePath(pth, mustWork = FALSE), work)) try(dyn.unload(pth), silent = TRUE) }
  unlink(work, recursive = TRUE, force = TRUE)
}
if (!keep) reg.finalizer(environment(), function(e) clean_work(), onexit = TRUE)
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
# the engine library, position-independent, for linking into the R module
libdir <- file.path(work, "v4pic")
st1 <- system2("cmake", c("-S", shQuote(eng_dir), "-B", shQuote(libdir), "-DCMAKE_BUILD_TYPE=Release", "-DCMAKE_POSITION_INDEPENDENT_CODE=ON", "-DV4_TESTS=OFF"), stdout = FALSE)
st2 <- system2("make", c("-C", shQuote(libdir), "-j3", "v4_bit"), stdout = FALSE)
if (st1 != 0 || st2 != 0 || !file.exists(file.path(libdir, "libv4_bit.a"))) stop("could not build libv4_bit.a (PIC)")
Sys.setenv(PKG_CPPFLAGS = paste0("-I", file.path(ref, "cpp"), " -I", file.path(eng_dir, "include"), " -fopenmp"),
           PKG_LIBS = paste("-fopenmp", shQuote(file.path(libdir, "libv4_bit.a"))), R_MAKEVARS_USER = file.path(ref, "cpp", "Makevars.v3"), MAKEFLAGS = "-j1")
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
fixture <- function(n, p, rho, seed, s0 = c(3, 7, 11, 19, 23), beta = c(1, -0.8)) {
  set.seed(seed)
  X <- matrix(0, n, p); X[, 1] <- rnorm(n)
  for (j in 2:p) X[, j] <- rho * X[, j - 1] + sqrt(1 - rho^2) * rnorm(n)
  s0 <- s0[s0 <= p]
  y <- drop(X[, s0, drop = FALSE] %*% rep(beta, length.out = length(s0))) + rnorm(n)
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
       sum_mode = sum_mode, threads = as.integer(th), tiers = tiers, N0 = as.integer(b$tiers$N[1]), N1 = as.integer(b$tiers$N[2]))
}
# The calibration through the v4 backend (core islands via CoreRunner; calibration ledger, local searches, V and the
# inherited export in v4 code; calib.bin written and read back): equal to v3_calibrate, the ledger included.
ledger_calib <- function(r, setup, seed, tag, st = settings_for(setup), th = 1L) {
  st$threads <- as.integer(th)
  cp <- file.path(work, paste0("calib_", gsub("[^A-Za-z0-9]", "_", tag), ".bin"))
  m <- .v3cpp$wp4_calibrate_ledger(setup$ptr, seed, st, cp)
  compare_calib(r, m, paste(tag, "[v4 backend]"))
  if (identical(r$status, "ok") && length(m$calib_bin)) {
    cb <- m$calib_bin; tg <- paste(tag, "[calib.bin]")
    same(cb$grid, r$frozen$grid, paste(tg, "frozen grid")); same(as.integer(cb$tier), r$frozen$tier, paste(tg, "tier"))
    same(as.integer(cb$N), as.integer(r$frozen$N), paste(tg, "N"))
    same(cb$inherited, r$frozen$inherited$models, paste(tg, "inherited models (order and content)"))
    same(cb$hpm, r$hpm$model, paste(tg, "calibration HPM")); same(cb$hpm_provenance, r$hpm$provenance, paste(tg, "calibration HPM provenance"))
    nt <- sum(vapply(r$tiers, function(t) 1L + 4L * length(t$iterations), 1L))
    same(as.integer(cb$n_stage_islands), as.integer(nt), paste(tg, "stage records: one per calibration island"))
    unlink(cp)
  }
  invisible(m)
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
  # v3's final-run leader stores (r$leaders_gamma0/1) are on the exclusion list: INTERFACES v0.1.7 -- final-run leaders
  # are not outputs in any mode (final ledgers use leaders = false). Calibration leaders are compared in compare_calib.
  n_checks <<- n_checks + 1L; if (m$leaders_gamma0$capacity != 0 || length(m$leaders_gamma0$models)) { failures <<- c(failures, paste(tag, "final leaders present")); cat("  FAIL:", tag, "final leaders present\n") }
  same(r$score_counts$logical, m$logical, paste(tag, "logical counters"))
}

# ---- inherited-HPM provenance, INTERFACES v0.1.6 (core/cpp/v3_core.cpp:416-441): the calibration HPM model is
# (i) also a table model, (ii) in the inherited list only, (iii) in neither. Each must give v3's provenance.
fake_prov <- list(phase = "pilot", mechanism = "gibbs_flip", tier = 0L, island = 0L, stage = 3L, round = 3L,
                  particle = 7L, position = 11L, phi = 0.5, iter = 0L)
same_model <- function(a, b) identical(as.integer(a), as.integer(b))
provenance_cases <- function(setup, frozen, seed, fr, tag) {
  Sstar <- as.integer(fr$hpm); Fstar <- fr$hpm_F
  base <- Filter(function(m) !same_model(m, Sstar), frozen$inherited$models)
  is_table <- any(vapply(setup$blocks, function(b) all(Sstar %in% b), TRUE))
  mk <- function(models, hpm_model) list(models = models, hpm = list(model = hpm_model, F = Fstar, provenance = fake_prov))
  variants <- list(
    ii = list(inh = mk(c(base, list(Sstar)), Sstar), want = if (is_table) "table" else "fake"),
    iii = list(inh = mk(base, Sstar), want = if (is_table) "table" else "island"))
  if (is_table) variants$i <- list(inh = mk(c(list(Sstar), base), Sstar), want = "table")
  cat(sprintf("   provenance cases: HPM {%s} is %sa table model\n", paste(Sstar, collapse = ","), if (is_table) "" else "not "))
  for (nm in names(variants)) {
    v <- variants[[nm]]
    fz <- v3_frozen(frozen$grid, tier = frozen$tier, N = frozen$N, L = frozen$L, inherited = v$inh)
    fz$rho_V <- frozen$rho_V; fz$grid_label <- frozen$grid_label
    ro <- v3_run_settings(setup, fz, ls0 = TRUE)
    f2 <- v3_final_run(setup, fz, seed, runtime = NULL, ls0 = TRUE)
    m2 <- .v3cpp$wp4_final_merge(setup$ptr, fz$grid, ro, as.numeric(seed), fz$inherited, threads, 64L, "", 0L)
    compare_final(f2, m2, sprintf("%s provenance(%s)", tag, nm))
    pv <- f2$hpm_provenance
    got <- if (identical(pv[names(fake_prov)], fake_prov)) "fake" else if (identical(pv$phase, "table")) "table" else "island"
    if (same_model(f2$hpm, Sstar)) expect(identical(got, v$want), sprintf("%s provenance(%s): v3 gives %s, expected %s", tag, nm, got, v$want))
  }
}

# ---- coded-rule paths not reached by the plain cases (review PR16 F2), each compared bit for bit with v3_calibrate on
# the same forced inputs: the R reference runs with wrappers around the same core entry points that the harness backend
# perturbs (pilot local_limit, V numerical failure, diagnostic failure, grid-runtime stop, a forced construction failure).
with_faults <- function(f, opts) {
  saved <- list(pilot = .v3cpp$cpp_cal_pilot, V = .v3cpp$cpp_cal_V, diag = .v3cpp$cpp_cal_diag, rt = .v3cpp$cpp_runtime_check, bg = v3_build_grid)
  on.exit({ assign("cpp_cal_pilot", saved$pilot, envir = .v3cpp); assign("cpp_cal_V", saved$V, envir = .v3cpp)
            assign("cpp_cal_diag", saved$diag, envir = .v3cpp); assign("cpp_runtime_check", saved$rt, envir = .v3cpp)
            assign("v3_build_grid", saved$bg, envir = globalenv()) })
  n <- new.env(); n$V <- 0; n$diag <- 0; n$rt <- 0; n$bg <- 0
  if (isTRUE(opts$force_ll_pilot)) assign("cpp_cal_pilot", function(...) { x <- saved$pilot(...); if (!is.null(x$local_search)) x$local_search$local_limit <- TRUE; x }, envir = .v3cpp)
  if (!is.null(opts$fail_V_at)) assign("cpp_cal_V", function(...) { n$V <- n$V + 1; if (n$V == opts$fail_V_at) list(status = "numerical_failure", message = "forced") else saved$V(...) }, envir = .v3cpp)
  if (!is.null(opts$fail_diag_at)) assign("cpp_cal_diag", function(...) { x <- saved$diag(...); n$diag <- n$diag + 1; if (n$diag == opts$fail_diag_at) list(status = "numerical_failure", message = "forced") else x }, envir = .v3cpp)
  if (!is.null(opts$stop_grid_at)) assign("cpp_runtime_check", function(...) { n$rt <- n$rt + 1; n$rt == opts$stop_grid_at }, envir = .v3cpp)
  if (!is.null(opts$force_build_failure)) assign("v3_build_grid", function(...) { g <- saved$bg(...); n$bg <- n$bg + 1; if (n$bg == opts$force_build_failure) { g$ok <- FALSE; g$reason <- "forced" }; g }, envir = globalenv())
  f()
}
coded_path <- function(setup, seed, tag, opts = list(), expect_status = NULL) {
  rt <- if (!is.null(opts$stop_grid_at)) .v3cpp$cpp_runtime_new(24, 0) else NULL
  pf <- if (isTRUE(opts$preflight)) function(e) TRUE else NULL
  r <- with_faults(function() v3_calibrate(setup, seed, tier = opts$tier0 %||% 0, preflight = pf, runtime = rt, grid_fallback = opts$grid_fallback %||% TRUE), opts)
  st <- settings_for(setup); st$tier0 <- as.integer(opts$tier0 %||% 0L); st$grid_fallback <- opts$grid_fallback %||% TRUE
  for (k in c("preflight", "force_ll_pilot")) if (!is.null(opts[[k]])) st[[k]] <- opts[[k]]
  for (k in c("fail_V_at", "fail_diag_at", "stop_grid_at", "force_build_failure")) if (!is.null(opts[[k]])) st[[k]] <- as.integer(opts[[k]])
  m <- .v3cpp$wp4_calibrate(setup$ptr, seed, st)
  compare_calib(r, m, tag)
  if (!is.null(expect_status)) expect(identical(r$status, expect_status), sprintf("%s reaches %s (got %s)", tag, expect_status, r$status))
  invisible(list(r = r, m = m))
}
extra_coded_paths <- function(setup, seed, id, r0) {
  coded_path(setup, seed, paste(id, "P2 tier-1 start"), list(tier0 = 1L))
  { r2 <- v3_calibrate(setup, seed, tier = 1, grid_fallback = TRUE); st2 <- settings_for(setup); st2$tier0 <- 1L
    ledger_calib(r2, setup, seed, paste(id, "P2 tier-1 start"), st2) }
  for (el in c(1L, 0L)) { sb <- setup; sb$budgets$ell <- el
    ledger_calib(v3_calibrate(sb, seed, tier = 0, grid_fallback = TRUE), sb, seed, paste0(id, " P", 5L - el, " ell=", el)) }
  sb <- setup; sb$budgets$ell <- 1L; coded_path(sb, seed, paste(id, "P4 ell=1"))
  sb$budgets$ell <- 0L; coded_path(sb, seed, paste(id, "P5 ell=0"))
  x <- coded_path(setup, seed, paste(id, "local_limit (forced)"), list(force_ll_pilot = TRUE))
  expect(isTRUE(x$r$tiers[[1]]$triggers$local_limit) && x$r$escalated, paste(id, "local_limit fires and escalates"))
  k <- length(x$r$tiers[[1]]$grids) + 2L     # the tier-1 rebuild_1 construction (after a tier-1 preliminary)
  y <- coded_path(setup, seed, paste(id, "last_successful_construction"), list(force_ll_pilot = TRUE, force_build_failure = k))
  expect(identical(y$r$flags$grid_fallback, "last_successful_construction"), paste(id, "fallback = last_successful_construction"))
  coded_path(setup, seed, paste(id, "grid-runtime stop"), list(stop_grid_at = 2L), "resource_limit")
  coded_path(setup, seed, paste(id, "V numerical failure"), list(fail_V_at = 2L), "numerical_failure")
  coded_path(setup, seed, paste(id, "diagnostic numerical failure"), list(fail_diag_at = 1L), "numerical_failure")
  coded_path(setup, seed, paste(id, "P3 preflight blocks escalation"), list(force_ll_pilot = TRUE, preflight = TRUE), "resource_limit")
  # bounded (Serial, I_max = ell) equals the coded tier 0 when tier 0 constructs every grid (reviewer's check)
  if (!isTRUE(r0$tiers[[1]]$triggers$grid_failure)) {
    b <- .v3cpp$wp4_calibrate(setup$ptr, seed, settings_for(setup, rule = "bounded", I_max = setup$budgets$ell))
    a <- r0$tiers[[1]]; t <- b$tiers[[1]]; tg <- paste(id, "bounded(I_max=ell) == coded tier 0")
    same(a$triggers, t$triggers, paste(tg, "triggers")); same(a$converged, t$converged, paste(tg, "converged")); same(a$rebuilds, t$rebuilds, paste(tg, "rebuilds"))
    same(length(a$grids), length(t$grids), paste(tg, "n grids"))
    for (g in seq_len(min(length(a$grids), length(t$grids)))) same(a$grids[[g]]$grid, t$grids[[g]]$grid, paste(tg, "grid", g))
    same(a$grid, b$frozen$grid, paste(tg, "frozen grid"))
  }
  # D-26 paths of the bounded rule (no core reference: V's variant rule), one test each
  b <- .v3cpp$wp4_calibrate(setup$ptr, seed, c(settings_for(setup, rule = "bounded", I_max = 2L), list(force_build_failure = 1L)))
  expect(b$status == "ok" && length(b$tiers) == 1L && identical(b$flags$grid_fallback, "pilot_schedule") &&
         identical(b$frozen$grid, b$tiers[[1]]$schedule), paste(id, "D-26 preliminary failure -> pilot schedule, no escalation"))
  b <- .v3cpp$wp4_calibrate(setup$ptr, seed, c(settings_for(setup, rule = "bounded", I_max = 2L), list(force_build_failure = 2L)))
  expect(b$status == "ok" && length(b$tiers) == 1L && identical(b$flags$grid_fallback, "last_successful_construction") &&
         identical(b$frozen$grid, b$tiers[[1]]$grids[[1]]$grid), paste(id, "D-26 rebuild failure -> last good grid"))
  b <- .v3cpp$wp4_calibrate(setup$ptr, seed, c(settings_for(setup, rule = "bounded", I_max = 2L), list(force_ll_pilot = TRUE)))
  expect(b$status == "ok" && length(b$tiers) == 1L && isTRUE(b$tiers[[1]]$triggers$local_limit), paste(id, "D-26 triggers recorded, no escalation"))
  b <- .v3cpp$wp4_calibrate(setup$ptr, seed, c(settings_for(setup, rule = "bounded", I_max = setup$budgets$ell + 1L)))
  expect(identical(b$status, "refused") && identical(b$task_status, "invalid_input"), paste(id, "D-26 I_max > ell refused"))
  b <- .v3cpp$wp4_calibrate(setup$ptr, seed, settings_for(setup, rule = "coded", sum_mode = "blocked"))
  expect(identical(b$status, "refused"), paste(id, "F7 coded + blocked refused"))
  b <- .v3cpp$wp4_calibrate(setup$ptr, seed, settings_for(setup, rule = "coded", refine_m = 4L))
  expect(identical(b$status, "refused"), paste(id, "F7 coded + refine_m > 1 refused"))
}

cases <- list(
  list(id = "AR0.9_n100_p30_s34", n = 100, p = 30,   rho = 0.9, seed = 21, H = c(48, 96),   Te = c(40, 80),   N = c(100, 200), ell = NULL, s0 = c(3, 4), beta = c(2, 1.5), prov = TRUE),
  list(id = "AR0.6_n100_p40",   n = 100, p = 40,   rho = 0.6, seed = 11, H = c(64, 128),  Te = c(60, 120),  N = c(150, 300), ell = NULL),
  list(id = "AR0.9_n120_p120",  n = 120, p = 120,  rho = 0.9, seed = 12, H = c(48, 96),   Te = c(40, 80),   N = c(120, 240), ell = 3),
  list(id = "IND_n80_p60_Te3",  n = 80,  p = 60,   rho = 0.0, seed = 13, H = c(32, 64),   Te = c(3, 4),     N = c(100, 200), ell = 2),
  list(id = "AR0.5_n150_p300",  n = 150, p = 300,  rho = 0.5, seed = 14, H = c(64, 128),  Te = c(60, 120),  N = c(200, 400), ell = 4))
if (level == "full") cases <- c(cases, list(
  list(id = "AR0.7_n200_p1000", n = 200, p = 1000, rho = 0.7, seed = 15, H = c(64, 128), Te = c(100, 200), N = c(150, 300), ell = NULL, heavy = TRUE),
  list(id = "AR0.8_n200_p2000", n = 200, p = 2000, rho = 0.8, seed = 16, H = c(48, 96), Te = c(80, 160), N = c(100, 200), ell = 6, heavy = TRUE)))

timing <- list()
if (nzchar(only)) cases <- Filter(function(cs) cs$id == only, cases)
for (cs in cases) {
  cat(sprintf("== case %s\n", cs$id))
  fx <- if (is.null(cs$s0)) fixture(cs$n, cs$p, cs$rho, cs$seed) else fixture(cs$n, cs$p, cs$rho, cs$seed, cs$s0, cs$beta)
  setup <- make_setup(fx, cs$H, cs$Te, cs$N, cs$ell)
  seed <- 1000L + cs$seed
  t0 <- proc.time()[["elapsed"]]; r <- v3_calibrate(setup, seed, tier = 0, preflight = NULL, runtime = NULL, grid_fallback = TRUE)
  t_ref <- proc.time()[["elapsed"]] - t0
  for (th in unique(c(1L, threads))) ledger_calib(r, setup, seed, sprintf("%s calib[th=%d]", cs$id, th), th = th)
  for (th in unique(c(1L, threads))) {
    m <- .v3cpp$wp4_calibrate(setup$ptr, seed, settings_for(setup, th = th))
    compare_calib(r, m, sprintf("%s calib[th=%d]", cs$id, th))
    timing[[length(timing) + 1]] <- data.frame(case = cs$id, what = sprintf("calibrate coded th=%d", th), ref_s = t_ref, wp4_s = m$seconds)
  }
  cat(sprintf("   calibration: status %s, tier %d, escalated %s, triggers {%s}, fallback %s\n", r$status, r$tier_final,
              r$escalated, paste(r$flags$triggers_fired, collapse = ","), r$flags$grid_fallback %||% "none"))
  if (cs$id == "AR0.6_n100_p40") extra_coded_paths(setup, seed, cs$id, r)
  if (cs$id == "IND_n80_p60_Te3") {
    coded_path(setup, seed, paste(cs$id, "P1 no fallback"), list(grid_fallback = FALSE), "schedule_limit")
    st1 <- settings_for(setup); st1$grid_fallback <- FALSE
    ledger_calib(v3_calibrate(setup, seed, tier = 0, grid_fallback = FALSE), setup, seed, paste(cs$id, "P1 no fallback"), st1)
  }
  if (cs$id == "AR0.9_n120_p120") coded_path(setup, seed, paste(cs$id, "P3 preflight blocks escalation"), list(preflight = TRUE), "resource_limit")
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
  if (isTRUE(cs$prov) || cs$id == "AR0.6_n100_p40") provenance_cases(setup, r$frozen, seed, fr, cs$id)
  # T9 through files: data/setup/calib/island files -> smcbvs4 merge (in process, streaming) -> fit.bin read back == v3
  fdir <- file.path(work, paste0("files_", cs$id)); unlink(fdir, recursive = TRUE); dir.create(fdir)
  mf <- .v3cpp$wp4_files_merge(setup$ptr, r$frozen$grid, ro, as.numeric(seed), r$frozen$inherited, fdir, threads)
  tg <- paste(cs$id, "T9-files")
  same(mf$status, "completed", paste(tg, "status"))
  if (identical(mf$status, "completed")) {
    for (nm in c("hpm", "hpm_F", "hpm_provenance", "log_Z", "log_Z_r", "pip_primary", "mpm", "near_ties", "near_tie_F",
                 "hpm_before_local", "top_store", "local_certified", "local_certified_by"))
      same(fr[[nm]], mf[[nm]], paste(tg, nm))
    same(unname(fr$pip_r), unname(mf$pip_r), paste(tg, "pip_r"))
    same(fr$start_mode$model, mf$start_mode, paste(tg, "start_mode"))
    same(fr$local_search$scanned_centres, mf$ls_scanned, paste(tg, "local scanned")); same(fr$local_search$scanned_F, mf$ls_scanned_F, paste(tg, "local scanned F"))
    same(fr$local_search$path, mf$ls_path, paste(tg, "local path"))
    same(fr$ls0$scanned_centres, mf$ls0_scanned, paste(tg, "ls0 scanned")); same(fr$ls0$scanned_F, mf$ls0_scanned_F, paste(tg, "ls0 scanned F"))
    fl <- names(mf$flags); same(fr$flags[fl], mf$flags, paste(tg, "flags"))
    same(unname(fr$score_counts$logical), unname(mf$logical), paste(tg, "logical counters"))
  } else cat("  files merge record:", mf$record, "\n")
  unlink(fdir, recursive = TRUE)
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
    b <- .v3cpp$wp4_calibrate(setup$ptr, seed, settings_for(setup, rule = "bounded", I_max = min(im, setup$budgets$ell), refine_m = 4L, sum_mode = "blocked", th = threads))
    expect(b$status == "ok", sprintf("%s bounded I_max=%d status %s", cs$id, im, b$status))
    if (b$status == "ok") {
      expect(b$I_used <= im, sprintf("%s bounded I_used <= I_max", cs$id))
      expect(length(b$frozen$grid) == 4L * (length(b$frozen$grid_unrefined) - 1L) + 1L, sprintf("%s refine x4 length", cs$id))
      expect(all(diff(b$frozen$grid) > 0) && b$frozen$grid[1] == 0 && tail(b$frozen$grid, 1) == 1, sprintf("%s refined grid valid", cs$id))
      expect(all(b$frozen$grid_unrefined %in% b$frozen$grid), sprintf("%s refined grid contains the calibrated grid", cs$id))
      expect(length(b$tiers) == 1L, sprintf("%s bounded never escalates (D-26)", cs$id))
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
if (!keep) clean_work()
if (length(failures)) { cat(paste(" -", failures), sep = "\n"); quit(status = 1) }
