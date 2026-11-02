# Local acceptance for CONF_NOTS_IDENTITY (CONF). Exit 0 and "ACCEPT" only if every criterion holds; else exit 1.
# Usage: Rscript compare_identity.R <download root containing p0500/<case>/SMCBVS.*> <downloaded run_env_<jobid>.txt>
args <- commandArgs(TRUE)
if (length(args) != 2L) stop("usage: compare_identity.R <results root containing p0500/> <run_env_<jobid>.txt>")
here <- dirname(normalizePath(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE))))
source(file.path(here, "cmp2.R"))
hist <- "C:/Users/felip/Documents/NOTS_BVS/smcbvs_v3_deploy_20261022/claude/prod_p0500_20261023T1227Z/p0500"
sha <- function(f) digest::digest(file = f, algo = "sha256")
fails <- character()
chk <- function(ok, what) { cat(if (isTRUE(ok)) "  ok   " else "  FAIL ", what, "\n", sep = ""); if (!isTRUE(ok)) fails <<- c(fails, what) }
# Pinned provenance: v2.1 historical records; v2.2 frozen tree (adapter aggregate source hashes computed from the tree bytes)
PIN <- list(
  v21_source = "b28719e65383bd23b29f1ae496c2bd83668e6aee318061e852b9ee33dc394e23", v21_v3_source = "8d03d3649cffe68527ed71efb824c644d3a6245a6109f2929029f1c86cace1f8",
  v22_source = "2e39575aa31d82797bac4f80108dd4340c9b6eac96a1b70a53c68c2918108d9c", v22_v3_source = "c0aebe86bfd07525bc97e2fd2bcacf4608142c778d25d584a38119e96ef82517",
  cases = list(
    p0500_S3_r044_c100 = list(rds = "27b7c546359196c5cb6a5e2aafc74c586c61520fc89585d25315ba175460f4a5", csv = "7389e55333169e045cf3e8219c3d28989aa7a55b632989793260839cd64ccea3",
      inputs = "fa7dcc1b215b978bc231e7d8cd810657c1946130ab1dee578856e066e05a4d4f", data_seed = 1440044, method_seed = 5440044, escalated = FALSE, reasons = character(0)),
    p0500_S5_r059_c100 = list(rds = "83254f90f44258e226b73ddd0a33808a628a275da4ba2af1c2074da002d97dd5", csv = "367ee74bf9101b9488a9cc6ef3bb08830a8f1ede9669a0eff894fc90d5facd2e",
      inputs = "f27ca8667f1f79d57f6be7dbfb5a687df0825b901acc362d589deb1153d249c2", data_seed = 1460059, method_seed = 5460059, escalated = TRUE, reasons = "E2")))
csv_prov <- c("run_id", "source_sha256", "v3_source_sha256", "runtime_s", "started_utc", "finished_utc", "host", "slurm_job_id", "slurm_array_task_id")
si <- function(r) grep("^(R version|Platform|Running under|BLAS|LAPACK|Matrix products)|Rcpp_", r$environment$session_info, value = TRUE)
mods <- function(r) strsplit(r$environment$compiler[["LOADEDMODULES"]], ":", fixed = TRUE)[[1]]
okv <- function(x) is.double(x) && length(x) > 0L && all(is.finite(x) & x >= 0 & x <= 1)
for (case in names(PIN$cases)) {
  p <- PIN$cases[[case]]; cat(case, "\n")
  hd <- file.path(hist, case); nd <- file.path(args[1], "p0500", case)
  chk(all(file.exists(file.path(nd, paste0("SMCBVS.", c("rds", "csv", "sha256", "done"))))), "new unit files present (rds, csv, sha256, done)")
  if (!file.exists(file.path(nd, "SMCBVS.rds")) || !file.exists(file.path(nd, "SMCBVS.sha256"))) next
  sl <- strsplit(readLines(file.path(nd, "SMCBVS.sha256"), warn = FALSE), "  ", fixed = TRUE)
  nm <- vapply(sl, function(z) z[length(z)], ""); dg <- vapply(sl, `[`, "", 1L)
  man_ok <- length(sl) == 2L && all(lengths(sl) == 2L) && setequal(nm, c("SMCBVS.rds", "SMCBVS.csv")) && !anyDuplicated(nm) && all(grepl("^[0-9a-f]{64}$", dg))
  chk(man_ok && all(vapply(seq_along(sl), function(i) identical(sha(file.path(nd, nm[i])), dg[i]), TRUE)), "new unit sha256 file: exactly SMCBVS.rds + SMCBVS.csv, both verify")
  chk(identical(sha(file.path(hd, "SMCBVS.rds")), p$rds) && identical(sha(file.path(hd, "SMCBVS.csv")), p$csv), "historical v2.1 files match pinned sha256")
  a <- readRDS(file.path(hd, "SMCBVS.rds")); b <- readRDS(file.path(nd, "SMCBVS.rds"))
  chk(identical(a$code$source_sha256, PIN$v21_source) && identical(a$code$v3_source_sha256, PIN$v21_v3_source), "historical record is v2.1 (pinned source hashes)")
  chk(identical(b$code$source_sha256, PIN$v22_source) && identical(b$code$v3_source_sha256, PIN$v22_v3_source), "new record is the frozen v2.2 tree (pinned source hashes)")
  chk(identical(b$adapter_version, "2.2-R1"), "adapter_version 2.2-R1")
  # Numerical environment = the historical production environment (exact, not substrings)
  chk(identical(b$environment$R, "R version 4.5.2 (2025-10-31)") && identical(b$environment$R, a$environment$R), "R version exactly 4.5.2 (2025-10-31), as historical")
  chk(identical(mods(b), mods(a)) && all(c("GCC/14.3.0", "R/4.5.2") %in% mods(b)), "loaded modules identical to historical (incl. GCC/14.3.0, R/4.5.2)")
  chk(identical(si(b), si(a)) && any(grepl("Rcpp_1.1.0", si(b), fixed = TRUE)) && any(grepl("FlexiBLAS OPENBLAS", si(b), fixed = TRUE)),
      "session: platform, OS, BLAS/LAPACK, Rcpp 1.1.0 identical to historical")
  chk(identical(b$environment$threads, a$environment$threads) && length(b$environment$threads) == 5L && all(unlist(b$environment$threads) == "1"),
      "all recorded numerical thread variables = 1, as historical")
  chk(identical(b$environment$RNGkind, a$environment$RNGkind), "RNGkind identical to historical")
  chk(identical(b$input$inputs_sha256, p$inputs) && identical(a$input$inputs_sha256, p$inputs), "same input file (pinned sha256)")
  chk(identical(as.numeric(b$case$data_seed), p$data_seed) && identical(as.numeric(b$case$method_seed), p$method_seed) && identical(b$fit$seed, a$fit$seed), "same seeds")
  chk(identical(unlist(b$allocation), c(mem_gb = 2, hours = 1.75)), "same allocation (2 GB, 1.75 h)")
  f <- b$fit
  chk(identical(f$status, "completed") && identical(f$branch_run, "smc"), "status completed, SMC branch")
  chk(identical(isTRUE(f$flags$escalated), p$escalated) && identical(as.integer(f$frozen$tier), as.integer(p$escalated)), "escalation state and frozen tier as expected")
  t0 <- unlist(f$calibration$flags$triggers_by_tier[[1]]); t0a <- unlist(a$fit$calibration$flags$triggers_by_tier[[1]])
  chk(identical(names(t0)[t0], p$reasons) && identical(names(t0a)[t0a], p$reasons), "tier-0 triggers fired = expected (new and historical)")
  chk(identical(f$instrumentation$escalation$reasons, p$reasons) && identical(isTRUE(f$instrumentation$escalation$escalated), p$escalated) &&
      is.null(f$instrumentation$escalation$blocked), "instrumentation$escalation (reasons, escalated, not blocked)")
  # Required new fields: present, right shape, sane
  pr <- length(f$pip_primary)
  chk(pr == 500L && identical(names(f$pip_plain), names(f$pip_primary)) && okv(f$pip_plain) &&
      identical(dim(f$pip_plain_r), c(pr, 4L)) && identical(rownames(f$pip_plain_r), names(f$pip_primary)) && okv(as.vector(f$pip_plain_r)) &&
      identical(unname(rowMeans(f$pip_plain_r)), unname(f$pip_plain)) &&
      is.integer(f$mpm_plain) && identical(f$mpm_plain, as.integer(names(f$pip_plain)[f$pip_plain > 0.5])), "fit plain PIPs: 500 retained, names, [0,1], island mean, MPM")
  full <- setNames(rep(0, 500), as.character(1:500)); if (!is.null(f$pip_plain)) full[names(f$pip_plain)] <- f$pip_plain
  chk(identical(b$pip_plain, full) && "mpm_plain" %in% names(b) && identical(b$mpm_plain, f$mpm_plain), "record plain summaries (original-index pip_plain, mpm_plain)")
  need <- c("stages", "best_before_local", "best_after_local", "stop", "escalation", "cut_group_large", "cut_group_large_any", "version", "scored")
  sc <- f$instrumentation$scored
  chk(all(need %in% names(f$instrumentation)) && identical(f$instrumentation$version, "v2.2") &&
      all(c("mode", "n_distinct", "n_distinct_hll", "log_sum_exp_F", "after_calibration") %in% names(sc)), "instrumentation: all required fields, version v2.2")
  chk(!is.null(b$instrumentation) && identical(b$instrumentation, f$instrumentation), "record instrumentation present and = fit instrumentation")
  ins <- f$instrumentation; ac <- sc$after_calibration; st <- ins$stages
  chk(is.list(ins$best_before_local) && identical(ins$best_before_local, f$hpm_before_local) &&
      is.list(ins$best_after_local) && identical(ins$best_after_local$model, f$hpm) && identical(ins$best_after_local$F, f$hpm_F) &&
      identical(ins$best_after_local$changed, !identical(f$hpm_before_local$model, f$hpm)), "best before/after final local search populated and = fit fields")
  chk(is.list(ac) && identical(names(ac), c("n_distinct", "n_distinct_hll", "log_sum_exp_F")) && is.na(ac$n_distinct) && is.na(ac$log_sum_exp_F) &&
      is.numeric(ac$n_distinct_hll) && length(ac$n_distinct_hll) == 1L && ac$n_distinct_hll > 0 && ac$n_distinct_hll <= sc$n_distinct_hll &&
      is.na(sc$log_sum_exp_F) && is.numeric(sc$memory_bytes_estimate) && sc$memory_bytes_estimate > 0, "scored report populated (HLL mode, after-calibration <= final)")
  tiers <- f$calibration$tiers
  exp_pilot <- vapply(tiers, function(x) as.integer(length(x$pilot$schedule) - 1L), 0L)
  exp_diag <- lapply(tiers, function(x) vapply(x$iterations, function(it) as.integer(length(it$grid) - 1L), 0L))
  chk(length(tiers) == 1L + p$escalated && all(exp_pilot > 0L) && all(vapply(exp_diag, function(v) length(v) > 0L && all(v > 0L), TRUE)) &&
      identical(st$final, length(f$grid) - 1L) && identical(st$pilot, exp_pilot) && identical(st$diag_grid_intervals, exp_diag) &&
      identical(as.integer(st$tier_final), as.integer(p$escalated)), "stages populated and = retained calibration schedules/grids (final, pilot and diag per tier, tier_final)")
  chk(is.integer(ins$cut_group_large) && length(ins$cut_group_large) == 1L &&
      identical(ins$cut_group_large, sum(vapply(f$cut_group_components, function(x) x$size > f$B, FALSE))) &&
      identical(ins$cut_group_large_any, ins$cut_group_large > 0L) && identical(ins$escalation$escalated, p$escalated), "cut_group_large and escalation fields populated and consistent")
  chk(identical(sc$mode, "hll") && is.na(sc$n_distinct) && isTRUE(sc$n_distinct_hll > 0) && is.null(f$instrumentation$scored_set) &&
      identical(f$instrumentation$stages$final, length(f$grid) - 1L) && is.null(f$instrumentation$stop), "instrumentation sane (hll mode, stages, no stop)")
  r <- cmp2_run(a, b, "record")
  chk(r$n_diff == 0L && length(r$added_bad) == 0L, sprintf("cmp2: %d paths compared, %d differing, %d non-allowlisted additions", r$n_compared, r$n_diff, length(r$added_bad)))
  if (r$n_diff) cat(head(r$diffs, 30), sep = "\n")
  ca <- read.csv(file.path(hd, "SMCBVS.csv"), colClasses = "character"); cb <- read.csv(file.path(nd, "SMCBVS.csv"), colClasses = "character")
  keep <- setdiff(names(ca), csv_prov)
  chk(identical(names(ca), names(cb)) && identical(ca[keep], cb[keep]), "CSV: same columns; all non-provenance cells identical")
}
# Job environment evidence (run_env_<jobid>.txt, written by job.sh)
cat("job environment\n")
ev <- if (file.exists(args[2])) readLines(args[2], warn = FALSE) else character()
chk(any(grepl("amx_tile", ev, fixed = TRUE)), "CPU is Sapphire Rapids (lscpu flags contain amx_tile)")
chk(any(ev == "gcc 14.3.0") && any(ev == "R version 4.5.2 (2025-10-31)") && any(ev == "Rcpp 1.1.0"), "job recorded GCC 14.3.0, R 4.5.2, Rcpp 1.1.0")
fs <- grep("^final_status ", ev, value = TRUE)
chk(length(grep("^job [0-9]+ host ", ev)) == 1L && length(grep("^end ", ev)) == 1L && identical(fs, "final_status 0") &&
    identical(grep("^failed_case ", ev, value = TRUE), "failed_case none"), "job record: one header, one end, exactly one final_status 0, no failed case")
chk(all(vapply(names(PIN$cases), function(cs) sum(grepl(paste0("^run Rscript .*--case ", cs, " "), ev)) == 1L &&
    sum(ev == paste("case", cs, "exit 0")) == 1L, TRUE)), "job record: one launch command and one exit-0 line per unit")
chk(any(grepl("^compiled_key [0-9a-f]{64}$", ev)) && any(grepl("^so_sha256 [0-9a-f]{64} ", ev)), "job record: fresh compile recorded (cache key and shared-object hash)")
if (length(fails)) { cat("FAIL:", length(fails), "criteria\n"); quit(status = 1) }
cat("ACCEPT: v2.2 reproduces both historical units on NOTS (pre-existing outputs bit-identical; escalation path confirmed)\n")
