#!/usr/bin/env Rscript
# pilot_bitid.R -- re-run, on NOTS and on real dev datasets, the enumerator-vs-scorer checks of enum/VALIDATION.md with this machine's compiler.
# TWO KINDS OF EQUALITY ARE KEPT APART (enum/README.md contract):
#   * BIT equality (serialised float64 bytes, little endian, any non-finite value is a failure) is claimed ONLY for model SCORES: F(S) and eta(S)
#     (the enumerator appends rows with the scorer's operation order), and for the HPM F value and the top-list F values, which are scores;
#   * AGGREGATES (log Z, PIPs, certificate margin/bound) are accumulated in a different order than the core, so they are compared with a declared
#     numerical tolerance; model decisions (HPM, MPM, top-list models and order) must be exactly equal; same-split thread invariance is exact.
# Every row records the number of byte mismatches AND the largest numerical difference.
#   T1  enumerator vs the NOTS-COMPILED CORE (v3_enumerate on v3_context): p = 14 sub-designs of 3 dev p = 20 datasets, both scales
#   T2  every one of the 2^20 models of dev_p0020_S4_r001, both scales: enumerator F vs Scorer::score, BYTES
#   T3  20,000 random models of dev_p0030_S4_r001, both scales: row-append F and eta vs Scorer::score, BYTES
#   T4  production enumerator on dev_p0030_S4_r001 (2% of the tasks, a `partial` hook run): internal re-check of every 61st node vs Scorer::score
#   T5  thread invariance on dev_p0020_S1_r001 with the same task split at 1 and 4 threads: exact
#
#   Rscript pilot_bitid.R --dev-study <dir with inputs/> --core-dir <core> --enum-dir <enum> --out <dir> [--threads 16]
# Reads inputs/ only. Writes <out>/BITID_REPORT.md and <out>/bitid_results.csv. Exit 0 = all PASS, 1 = any FAIL.

TOL_LOGZ_ABS <- 1e-9; TOL_LOGZ_REL <- 1e-12; TOL_PIP <- 1e-12; TOL_CERT <- 1e-9
a <- commandArgs(trailingOnly = TRUE)
opt <- function(k, d = NULL) { i <- match(paste0("--", k), a); if (is.na(i) || i == length(a)) d else a[i + 1L] }
study <- opt("dev-study"); core <- opt("core-dir"); enum <- opt("enum-dir"); out <- opt("out"); thr <- as.integer(opt("threads", "4"))
if (is.null(study) || is.null(core) || is.null(enum) || is.null(out)) stop("usage: pilot_bitid.R --dev-study DIR --core-dir DIR --enum-dir DIR --out DIR [--threads N]")
dir.create(out, recursive = TRUE, showWarnings = FALSE)
Sys.setenv(LOWP_ENUM_DIR = normalizePath(enum, winslash = "/"))
source(file.path(enum, "lowp_enum.R"))
core <- normalizePath(core, winslash = "/", mustWork = TRUE)
suppressWarnings(source(file.path(core, "v3.R"), local = FALSE))     # the core, compiled with its own Makevars.v3 (cached by pilot_build.R)
lowp_load(core)
cpp <- .lowp$cpp
rd <- function(id) readRDS(file.path(study, "inputs", substr(sub("^dev_", "", id), 1, 5), paste0(id, ".rds")))

# ---- comparison helpers -------------------------------------------------------------------------------------------------
# byte-level: number of float64 VALUES whose 8 serialised bytes differ; non-finite values in either vector are counted separately and always fail
byte_cmp <- function(x, y) {
  x <- as.numeric(x); y <- as.numeric(y)
  if (length(x) != length(y)) return(list(n = max(length(x), length(y)), bytes = max(length(x), length(y)), nonfinite = NA_integer_, num = Inf))
  bx <- writeBin(x, raw(), endian = "little"); by <- writeBin(y, raw(), endian = "little")
  bad <- if (length(x)) colSums(matrix(bx != by, nrow = 8L)) > 0L else logical(0)
  nf <- sum(!is.finite(x) | !is.finite(y))
  fin <- is.finite(x) & is.finite(y)
  list(n = length(x), bytes = sum(bad), nonfinite = nf, num = if (any(fin)) max(abs(x[fin] - y[fin])) else 0)
}
R <- list()
add <- function(check, case, n, bytes, nonfinite, numdiff, pass, note = "")
  R[[length(R) + 1L]] <<- data.frame(check = check, case = case, n = n, byte_mismatches = bytes, nonfinite = nonfinite, max_abs_diff = numdiff,
                                     pass = isTRUE(pass), note = note, stringsAsFactors = FALSE)
t_start <- proc.time()[["elapsed"]]

## T1: enumerator vs core (p = 14 sub-design)
for (id in c("dev_p0020_S1_r001", "dev_p0020_S4_r001", "dev_p0020_S6_r001")) {
  d <- rd(id); X <- d$X[, 1:14]
  ex <- lowp_exact(X, list(c100 = d$Y[, "c100"], c050 = d$Y[, "c050"]), top = 1000, threads = min(thr, 4L), task_bits = 4, core_dir = core)
  for (sc in c("c100", "c050")) {
    pre <- v3_preprocess(X, as.numeric(d$Y[, sc]), dup_components = FALSE)
    ref <- v3_enumerate(v3_context(pre$X, pre$y, orig = pre$kept, return_gram = FALSE))
    e <- ex[[sc]]
    topm <- vapply(ref$top$models, function(m) paste(m, collapse = ";"), ""); nt <- min(length(topm), nrow(e$top))
    # exact decisions
    dec <- c(models_scored = attr(ex, "run")$models_scored == ref$models_scored, hpm = identical(as.integer(e$hpm), as.integer(ref$hpm)),
             mpm = identical(e$mpm, as.integer(ref$mpm)), top_models_and_order = identical(topm[1:nt], e$top$model[1:nt]),
             certified_flag = identical(e$global_certified, ref$global_certified))
    # scores: BYTES (F and eta are scorer outputs)
    sF <- byte_cmp(c(e$hpm_F, e$second_F, e$top$F[1:nt]), c(ref$hpm_F, ref$second_F, ref$top$value[1:nt]))
    sE <- byte_cmp(e$hpm_eta, ref$hpm_error_bound)
    # aggregates: tolerance
    dlogZ <- abs(e$log_Z - ref$log_Z); dpip <- max(abs(e$pip - ref$pip))
    dcert <- max(abs(e$margin - ref$margin), abs(e$certificate_bound - ref$certificate_bound), na.rm = TRUE)
    agg_ok <- is.finite(dlogZ) && dlogZ <= max(TOL_LOGZ_ABS, TOL_LOGZ_REL * abs(ref$log_Z)) && dpip <= TOL_PIP && dcert <= TOL_CERT
    add("T1 scores (HPM F, second F, top-list F, eta): BYTES vs NOTS-compiled core", paste(id, sc), sF$n + sE$n, sF$bytes + sE$bytes, sum(sF$nonfinite, sE$nonfinite, na.rm = TRUE),
        max(sF$num, sE$num), sF$bytes + sE$bytes == 0 && sF$nonfinite == 0 && sE$nonfinite == 0)
    add("T1 decisions (models scored, HPM, MPM, top-list models and order, certified flag): exact", paste(id, sc), length(dec), sum(!dec), 0, 0, all(dec),
        if (any(!dec)) paste("failing:", paste(names(dec)[!dec], collapse = ",")) else "")
    add(sprintf("T1 aggregates: |dlogZ| <= %.0e (abs) or %.0e (rel), max|dPIP| <= %.0e, certificate <= %.0e", TOL_LOGZ_ABS, TOL_LOGZ_REL, TOL_PIP, TOL_CERT), paste(id, sc),
        2L + length(ref$pip), 0, 0, max(dlogZ, dpip, dcert), agg_ok, sprintf("dlogZ=%.2e dPIP=%.2e dcert=%.2e (accumulation order may differ in the last bits; not a score)", dlogZ, dpip, dcert))
  }
}
## T2: all 2^20 models at p = 20
d <- rd("dev_p0020_S4_r001")
ex <- lowp_exact(d$X, list(c100 = d$Y[, "c100"], c050 = d$Y[, "c050"]), threads = thr, collect_F = TRUE, return_raw = TRUE, core_dir = core)
run <- attr(ex, "run"); pr <- run$prep; masks <- as.numeric(0:(2^20 - 1))
for (sc in c("c100", "c050")) {
  sref <- cpp$cpp_score_masks(pr$X, pr$Y[, sc], pr$orig, masks, as.integer(thr))
  b <- byte_cmp(run$F_all[[sc]], sref$F)
  add("T2 all 2^20 models: enumerator F vs Scorer::score, BYTES", paste("dev_p0020_S4_r001", sc), b$n, b$bytes, b$nonfinite, b$num, b$bytes == 0 && b$nonfinite == 0,
      sprintf("fallbacks %d, recheck mismatches %d", ex[[sc]]$numerics$n_fallback_v3, ex[[sc]]$numerics$recheck_mismatch_F))
}
rm(ex, run, pr, masks)
## T3: 20,000 random models at p = 30, row-append F/eta vs Scorer::score (bytes)
d <- rd("dev_p0030_S4_r001")
pr <- lowp_prepare(d$X, list(c100 = d$Y[, "c100"], c050 = d$Y[, "c050"]), core)
set.seed(20261029); p <- ncol(pr$X)
m <- vapply(1:20000, function(i) { k <- sample(0:p, 1); sum(2^(sample.int(p, k) - 1)) }, 0)
dd <- cpp$cpp_dfs_F(pr$X, pr$Y, pr$orig, m, 1e-8, integer(0))
for (s in 1:2) {
  sref <- cpp$cpp_score_masks(pr$X, pr$Y[, s], pr$orig, m, as.integer(thr))
  bF <- byte_cmp(dd$F[, s], sref$F); bE <- byte_cmp(dd$eta[, s], sref$eta)
  add("T3 20,000 random models p=30: row-append F and eta vs Scorer::score, BYTES", paste("dev_p0030_S4_r001", colnames(pr$Y)[s]), bF$n + bE$n, bF$bytes + bE$bytes,
      sum(bF$nonfinite, bE$nonfinite, na.rm = TRUE), max(bF$num, bE$num), bF$bytes + bE$bytes == 0 && bF$nonfinite == 0 && bE$nonfinite == 0,
      sprintf("F byte mismatches %d, eta byte mismatches %d", bF$bytes, bE$bytes))
}
## T4: production enumerator, internal re-check at p = 30 (a partial hook run)
ex <- suppressWarnings(lowp_exact(d$X, list(c100 = d$Y[, "c100"], c050 = d$Y[, "c050"]), threads = thr, prefix_fraction = 0.02, recheck_stride = 61L, core_dir = core))
for (sc in c("c100", "c050")) {
  nn <- ex[[sc]]$numerics
  add("T4 production enumerator nodes re-scored by Scorer::score (every 61st node, 2% of tasks)", paste("dev_p0030_S4_r001", sc), nn$recheck_count,
      nn$recheck_mismatch_F + nn$recheck_mismatch_eta, 0, nn$max_abs_dF_recheck, nn$recheck_count > 0 && nn$recheck_mismatch_F + nn$recheck_mismatch_eta == 0,
      sprintf("fallbacks %d; models %g (partial hook run)", nn$n_fallback_v3, attr(ex, "run")$models_scored))
}
## T5: thread invariance, same task split, exact
d <- rd("dev_p0020_S1_r001")
e1 <- lowp_exact(d$X, list(c100 = d$Y[, "c100"], c050 = d$Y[, "c050"]), threads = 1, task_bits = 6, core_dir = core)
e4 <- lowp_exact(d$X, list(c100 = d$Y[, "c100"], c050 = d$Y[, "c050"]), threads = 4, task_bits = 6, core_dir = core)
for (sc in c("c100", "c050")) {
  b <- byte_cmp(c(e1[[sc]]$log_Z, e1[[sc]]$pip), c(e4[[sc]]$log_Z, e4[[sc]]$pip))
  same <- identical(e1[[sc]], e4[[sc]])
  add("T5 thread invariance (1 vs 4 threads, same task split): all outputs identical", paste("dev_p0020_S1_r001", sc), b$n, b$bytes, b$nonfinite, b$num, same && b$bytes == 0)
}
res <- do.call(rbind, R)
utils::write.csv(res, file.path(out, "bitid_results.csv"), row.names = FALSE)
ok <- all(res$pass)
L <- c("# Pilot score and aggregate checks: enumerator vs scorer on NOTS", "",
       sprintf("**VERDICT: %s** (%d of %d rows pass). Host `%s`; %s; %s UTC; elapsed %.0f s; threads %d.", if (ok) "PASS" else "FAIL", sum(res$pass), nrow(res),
               Sys.info()[["nodename"]], R.version.string, format(Sys.time(), tz = "UTC", "%Y-%m-%d %H:%M"), proc.time()[["elapsed"]] - t_start, thr), "",
       "Bit equality (serialised float64 bytes; non-finite values fail) is claimed only for scores (F, eta, HPM F, top-list F). Aggregates (log Z, PIPs, certificate) use the stated tolerances; decisions are exact.", "",
       "| Check | Case | Values | Byte mismatches | Non-finite | Max abs diff | Pass | Note |", "|---|---|---|---|---|---|---|---|",
       sprintf("| %s | %s | %g | %g | %s | %.3g | %s | %s |", res$check, res$case, res$n, res$byte_mismatches, res$nonfinite, res$max_abs_diff, ifelse(res$pass, "yes", "NO"), res$note))
writeLines(L, file.path(out, "BITID_REPORT.md")); cat(paste(L, collapse = "\n"), "\n")
quit(save = "no", status = if (ok) 0L else 1L)
