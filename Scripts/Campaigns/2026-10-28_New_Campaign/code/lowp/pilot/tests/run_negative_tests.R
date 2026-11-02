#!/usr/bin/env Rscript
# run_negative_tests.R -- LOCAL TEST. Builds the fabricated pilot (make_fabricated_pilot.R, self-contained), checks that the baseline is accepted, then
# applies each deliberate defect (the review's reproduction cases and more) to a COPY and checks that summarize_pilot.R rejects it with the expected
# exit status (0 accepted, 2 FAIL, 3 INCOMPLETE) and that failed units never enter sizing.
#   Rscript run_negative_tests.R <work dir>        writes <work dir>/NEGATIVE_TESTS.md; exit 0 if every case behaves as expected
a <- commandArgs(trailingOnly = TRUE); work <- a[1]; stopifnot(!is.na(work)); dir.create(work, recursive = TRUE, showWarnings = FALSE)
here <- local({ f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1L]); dirname(normalizePath(f, winslash = "/")) })
rs <- file.path(R.home("bin"), "Rscript"); PID <- "20261029T0900Z_lowp_pilot"
base <- file.path(work, "baseline"); unlink(base, recursive = TRUE)
st <- system2(rs, c(shQuote(file.path(here, "make_fabricated_pilot.R")), shQuote(base)), stdout = FALSE, stderr = FALSE); stopifnot(st == 0)
summ <- function(root, drop = character(), extra = character()) {
  rdirs <- list.dirs(file.path(root, "results"), recursive = FALSE); for (d in drop) rdirs <- rdirs[!grepl(paste0(d, "$"), rdirs)]
  o <- file.path(root, "sum"); unlink(o, recursive = TRUE)
  rc <- suppressWarnings(system2(rs, c(shQuote(file.path(here, "..", "summarize_pilot.R")), "--results", shQuote(paste(rdirs, collapse = ",")), "--logs", shQuote(file.path(root, "logs", PID)),
                                       "--out", shQuote(o), extra), stdout = FALSE, stderr = FALSE))
  v <- if (file.exists(file.path(o, "pilot_verdicts.csv"))) read.csv(file.path(o, "pilot_verdicts.csv"), stringsAsFactors = FALSE) else NULL
  list(rc = rc, v = v, o = o)
}
cases <- list()
case <- function(name, expect_rc, mutate, drop = character(), check = NULL, extra = character()) cases[[length(cases) + 1L]] <<- list(name = name, rc = expect_rc, mutate = mutate, drop = drop, check = check, extra = extra)
logsof <- function(r) file.path(r, "logs", PID); resof <- function(r, s) file.path(r, "results", paste0(PID, "_", s))
edit_tsv <- function(f, fn) { x <- read.delim(f, stringsAsFactors = FALSE, colClasses = c(unit = "character")); x <- fn(x); write.table(x, f, sep = "\t", quote = FALSE, row.names = FALSE) }
rewrite_rds <- function(f, fn) { z <- readRDS(f); z <- fn(z); saveRDS(z, f, compress = FALSE) }

case("baseline accepted", 0L, function(r) NULL)
case("review (a): a benchmark timing row has rc 2", 2L, function(r) edit_tsv(file.path(logsof(r), "timing", "all.fab_0.tsv"), function(x) { i <- which(x$arm == "bench")[5]; x$rc[i] <- 2; x }))
case("review (b): all 192 benchmark completion markers and sidecars removed", 3L, function(r) unlink(list.files(resof(r, "bench"), pattern = "\\.(done|sha256)$", recursive = TRUE, full.names = TRUE)))
case("review (c): all four repeat CSV statuses failed", 2L, function(r) for (f in list.files(resof(r, "smc"), pattern = "_rep1\\.csv$", recursive = TRUE, full.names = TRUE)) { x <- read.csv(f); x$status <- "failed"; write.csv(x, f, row.names = FALSE) })
case("review (d): the whole benchmark arm omitted", 3L, function(r) NULL, drop = "bench")
case("enum record: models_scored = 1 and numerics removed", 2L, function(r) { f <- list.files(resof(r, "enum30"), pattern = "EXACT\\.rds$", recursive = TRUE, full.names = TRUE)[1]
  rewrite_rds(f, function(z) { z$models_scored <- 1; z$scales$c100$numerics <- NULL; z }); h <- digest::digest(file = f, algo = "sha256")
  writeLines(paste0(h, "  EXACT.rds"), sub("rds$", "sha256", f)); writeLines(c(h, "t"), sub("rds$", "done", f)) })
case("enum p30 record carries p20 dimensions (K / model count wrong)", 2L, function(r) { f <- list.files(resof(r, "enum30"), pattern = "EXACT\\.rds$", recursive = TRUE, full.names = TRUE)[2]
  rewrite_rds(f, function(z) { z$K <- 20L; z$models_scored <- 2^20; z$extra$models_expected <- 2^20; z }); h <- digest::digest(file = f, algo = "sha256")
  writeLines(paste0(h, "  EXACT.rds"), sub("rds$", "sha256", f)); writeLines(c(h, "t"), sub("rds$", "done", f)) })
case("enum record: no internal re-check coverage (recheck_count 0)", 2L, function(r) { f <- list.files(resof(r, "enum20"), pattern = "EXACT\\.rds$", recursive = TRUE, full.names = TRUE)[3]
  rewrite_rds(f, function(z) { z$scales$c050$numerics$recheck_count <- 0; z }); h <- digest::digest(file = f, algo = "sha256")
  writeLines(paste0(h, "  EXACT.rds"), sub("rds$", "sha256", f)); writeLines(c(h, "t"), sub("rds$", "done", f)) })
case("enum RDS altered after the sidecar was written (hash mismatch)", 2L, function(r) { f <- list.files(resof(r, "enum20"), pattern = "EXACT\\.rds$", recursive = TRUE, full.names = TRUE)[4]
  rewrite_rds(f, function(z) { z$runtime_s <- 99; z }) })
case("thread-invariance defect (a 32-thread output differs)", 2L, function(r) { f <- list.files(resof(r, "scale_t32"), pattern = "EXACT\\.rds$", recursive = TRUE, full.names = TRUE)[1]
  rewrite_rds(f, function(z) { z$scales$c100$log_Z <- z$scales$c100$log_Z + 1e-9; z }); h <- digest::digest(file = f, algo = "sha256")
  writeLines(paste0(h, "  EXACT.rds"), sub("rds$", "sha256", f)); writeLines(c(h, "t"), sub("rds$", "done", f)) })
case("repeat seed offset wrong (repeat uses the primary seed)", 2L, function(r) { f <- list.files(resof(r, "smc"), pattern = "_rep1\\.csv$", recursive = TRUE, full.names = TRUE)[1]
  x <- read.csv(f); x$method_seed <- x$data_seed + 4000000; write.csv(x, f, row.names = FALSE)
  b <- sub("\\.csv$", "", f); rds <- paste0(b, ".rds"); writeLines(c(paste0(digest::digest(file = rds, algo = "sha256"), "  ", basename(rds)), paste0(digest::digest(file = f, algo = "sha256"), "  ", basename(f))), paste0(b, ".sha256")) })
case("benchmark ran with test_library TRUE", 2L, function(r) { f <- list.files(resof(r, "bench"), pattern = "A1\\.csv$", recursive = TRUE, full.names = TRUE)[1]
  x <- read.csv(f); x$test_library <- TRUE; write.csv(x, f, row.names = FALSE); b <- sub("\\.csv$", "", f); rds <- paste0(b, ".rds")
  writeLines(c(paste0(digest::digest(file = rds, algo = "sha256"), "  ", basename(rds)), paste0(digest::digest(file = f, algo = "sha256"), "  ", basename(f))), paste0(b, ".sha256")) })
case("benchmark packages resolved outside the pinned library", 2L, function(r) { f <- list.files(resof(r, "bench"), pattern = "F2\\.rds$", recursive = TRUE, full.names = TRUE)[1]
  rewrite_rds(f, function(z) { z$environment$package_provenance$glmnet$path <- "/usr/lib/R/site-library/glmnet"; z })
  b <- sub("\\.rds$", "", f); csv <- paste0(b, ".csv"); writeLines(c(paste0(digest::digest(file = f, algo = "sha256"), "  ", basename(f)), paste0(digest::digest(file = csv, algo = "sha256"), "  ", basename(csv))), paste0(b, ".sha256")) })
case("unexpected extra unit folder present", 3L, function(r) dir.create(file.path(resof(r, "smc"), "p0020", "dev_p0020_S9_r099_c100"), recursive = TRUE))
case("a Slurm task FAILED in the terminal snapshot", 2L, function(r) { f <- file.path(logsof(r), "accounting", "sacct_final.tsv"); x <- read.delim(f, sep = "|", stringsAsFactors = FALSE, colClasses = "character")
  i <- which(x$JobID == "5009_3"); x$State[i] <- "FAILED"; x$ExitCode[i] <- "1:0"; write.table(x, f, sep = "|", quote = FALSE, row.names = FALSE) })
case("terminal snapshot incl. the collector is missing (only the collector's own snapshot)", 3L, function(r) unlink(file.path(logsof(r), "accounting", "sacct_final.tsv")))
case("GNU-time RSS unavailable but batch MaxRSS present: memory comes from sacct, still accepted", 0L, function(r) edit_tsv(file.path(logsof(r), "timing", "all.fab_0.tsv"), function(x) { x$maxrss_kb[x$arm %in% c("enum20", "enum30", "bench")] <- NA; x }),
     check = function(o) { p <- read.csv(file.path(o, "pilot_projection.csv")); all(is.finite(p$suggested_mem_request_mb[p$piece != "TOTAL"])) })
case("GNU-time RSS unavailable and no sacct at all: no memory evidence", 3L, function(r) { edit_tsv(file.path(logsof(r), "timing", "all.fab_0.tsv"), function(x) { x$maxrss_kb[x$arm %in% c("enum20", "enum30", "bench")] <- NA; x }); unlink(file.path(logsof(r), "accounting", "sacct_final.tsv")); unlink(file.path(logsof(r), "accounting", "sacct_collector.tsv")) })
case("truth-lock test reports a failed check", 2L, function(r) writeLines(c("script_sha256 x", "checks 40", "failed 3", "final_exit_status 1"), file.path(logsof(r), "truthlock", "evidence", "final_status.txt")))
case("wave unlock record missing", 3L, function(r) unlink(file.path(logsof(r), "truthlock", "WAVE_UNLOCK.txt")))
case("wave lock not verified", 2L, function(r) writeLines(c("# wave lock", "WAVE_LOCK_FAILED rc=0 verify=1"), file.path(logsof(r), "truthlock", "WAVE_LOCK.txt")))
case("launch receipt missing", 3L, function(r) unlink(file.path(logsof(r), "launch"), recursive = TRUE))
case("P0 report says MISMATCH", 2L, function(r) writeLines(c("# LOWP check 4(b)", "", "**MISMATCH** (exit status 1). Compared 1200 production and 60 dev datasets; 2 mismatches."), file.path(logsof(r), "p0_verify", "NOTS_REGEN_REPORT.md")))
case("P0 report says INCOMPLETE", 3L, function(r) writeLines(c("# LOWP check 4(b)", "", "**INCOMPLETE** (exit status 3). Compared 0 production and 60 dev datasets."), file.path(logsof(r), "p0_verify", "NOTS_REGEN_REPORT.md")))
case("score/aggregate report FAIL", 2L, function(r) { x <- read.csv(file.path(logsof(r), "bitid", "bitid_results.csv")); x$pass[2] <- FALSE; write.csv(x, file.path(logsof(r), "bitid", "bitid_results.csv"), row.names = FALSE)
  writeLines("**VERDICT: FAIL** (6 of 7 rows pass).", file.path(logsof(r), "bitid", "BITID_REPORT.md")) })
case("a test hook was set at submission", 2L, function(r) { f <- file.path(logsof(r), "launch", "effective_env.txt"); x <- readLines(f); x[x == "PILOT_BENCH_EXTRA=[]"] <- "PILOT_BENCH_EXTRA=[--test-library]"; writeLines(x, f) })

## ---- final-confirmation cases (FC5 enum contract and .done statuses, FC7 runtime/scaling/wall, FC8 library and provenance) ----
resign_enum <- function(f) { h <- digest::digest(file = f, algo = "sha256"); writeLines(paste0(h, "  EXACT.rds"), sub("rds$", "sha256", f)); writeLines(c(h, "t"), sub("rds$", "done", f)) }
resign_pair <- function(f) { b <- sub("[.]rds$", "", f); writeLines(c(paste0(digest::digest(file = f, algo = "sha256"), "  ", basename(f)), paste0(digest::digest(file = paste0(b, ".csv"), algo = "sha256"), "  ", basename(b), ".csv")), paste0(b, ".sha256")) }
enum_unit <- function(r, run, k) list.files(resof(r, run), pattern = "EXACT[.]rds$", recursive = TRUE, full.names = TRUE)[k]
bench_unit <- function(r, m, k = 1) list.files(resof(r, "bench"), pattern = paste0("^", m, "[.]rds$"), recursive = TRUE, full.names = TRUE)[k]
case("FC5: empty HPM (integer(0)) is a legitimate record and is accepted (baseline unit 7 is valid)", 0L, function(r) NULL,
     check = function(o) { u <- read.csv(file.path(o, "pilot_units.csv")); isTRUE(u$valid[u$unit == "dev_p0020_S2_r002"]) })
case("FC5: .done marker says 'failed,failed' while the CSV says ok,ok", 2L, function(r) { f <- list.files(resof(r, "smc"), pattern = "SMCBVS[.]done$", recursive = TRUE, full.names = TRUE)[2]; writeLines(c("status failed,failed", "finished_utc x"), f) })
case("FC5: .done marker status differs on a benchmark unit", 2L, function(r) { f <- list.files(resof(r, "bench"), pattern = "^A3[.]done$", recursive = TRUE, full.names = TRUE)[1]; writeLines(c("status ok,failed", "finished_utc x"), f) })
case("FC5: re-signed enum record with complete = FALSE at the top level", 2L, function(r) { f <- enum_unit(r, "enum20", 2); rewrite_rds(f, function(z) { z$complete <- FALSE; z }); resign_enum(f) })
case("FC5: re-signed enum record without the top-level coverage fields", 2L, function(r) { f <- enum_unit(r, "enum20", 3); rewrite_rds(f, function(z) { z$models_expected <- NULL; z$complete <- NULL; z }); resign_enum(f) })
case("FC5: re-signed enum record with a scale lacking status and scope", 2L, function(r) { f <- enum_unit(r, "enum30", 2); rewrite_rds(f, function(z) { z$scales$c050$status <- NULL; z$scales$c050$scope <- NULL; z }); resign_enum(f) })
case("FC5: re-signed enum record with non-normalised size masses", 2L, function(r) { f <- enum_unit(r, "enum20", 4); rewrite_rds(f, function(z) { z$scales$c100$size_logmass <- z$scales$c100$size_logmass + 1; z }); resign_enum(f) })
case("FC5: re-signed enum record whose size_logjoint disagrees with log Z", 2L, function(r) { f <- enum_unit(r, "enum20", 5); rewrite_rds(f, function(z) { z$scales$c100$size_logjoint <- z$scales$c100$size_logjoint + 0.5; z }); resign_enum(f) })
case("FC5: enum record with a short top list (not min(1000, 2^p) rows)", 2L, function(r) { f <- enum_unit(r, "enum20", 6); rewrite_rds(f, function(z) { z$scales$c050$top <- z$scales$c050$top[1:10, ]; z }); resign_enum(f) })
case("FC7: benchmark rows$runtime_s differs from the CSV runtime", 2L, function(r) { f <- bench_unit(r, "F1"); rewrite_rds(f, function(z) { z$rows$runtime_s <- z$rows$runtime_s * 2; z }); resign_pair(f) })
case("FC7: benchmark record without rows$runtime_s", 2L, function(r) { f <- bench_unit(r, "F2"); rewrite_rds(f, function(z) { z$rows$runtime_s <- NULL; z }); resign_pair(f) })
case("FC7: saved scaling-subset file missing", 3L, function(r) unlink(file.path(logsof(r), "scaling", "scaling_subset.csv")))
case("FC7: scaling-subset file has only two of the four rows", 2L, function(r) { f <- file.path(logsof(r), "scaling", "scaling_subset.csv"); x <- read.csv(f); write.csv(x[1:2, ], f, row.names = FALSE) })
case("FC7: enum30 wall times missing (no silent fallback to in-process time)", 3L, function(r) edit_tsv(file.path(logsof(r), "timing", "all.fab_0.tsv"), function(x) { x$wall_s[x$arm == "enum30"] <- NA; x }))
case("FC8: package directory in a sibling of the pinned library (R452_UNAPPROVED)", 2L, function(r) { f <- bench_unit(r, "F3"); rewrite_rds(f, function(z) { z$environment$package_provenance$glmnet$path <- "/projects/ml75/fb31/BVS/bench20261019/lib/R452_UNAPPROVED/glmnet"; z }); resign_pair(f) })
case("FC8: effective R is 4.4.1, not 4.5.2", 2L, function(r) { f <- bench_unit(r, "F4"); rewrite_rds(f, function(z) { z$environment$sessionInfo[1] <- "R version 4.4.1 (2024-06-14 ucrt)"; z }); resign_pair(f) })
case("FC8: package version in the provenance differs from the CSV package_version", 2L, function(r) { f <- bench_unit(r, "F5"); rewrite_rds(f, function(z) { z$environment$package_provenance$glmnet$version <- "0.0"; z }); resign_pair(f) })
case("FC8: package built under R 4.4.3", 2L, function(r) { f <- bench_unit(r, "A1"); rewrite_rds(f, function(z) { z$environment$package_provenance$digest$built <- "4.4.3"; z }); resign_pair(f) })
case("FC8: package version absent from the provenance", 2L, function(r) { f <- bench_unit(r, "A2"); rewrite_rds(f, function(z) { z$environment$package_provenance$digest$version <- NULL; z }); resign_pair(f) })
## ---- RC1 / RC2 / RC4 cases (second final confirmation) ----
tim <- function(r) file.path(logsof(r), "timing", "all.fab_0.tsv")
scf <- function(r) file.path(logsof(r), "scaling", "scaling_subset.csv")
edit_sc <- function(fn) function(r) { x <- read.csv(scf(r)); x <- fn(x); write.csv(x, scf(r), row.names = FALSE) }
proj_status <- function(o) unique(read.csv(file.path(o, "pilot_projection.csv"))$status)
case("RC1 baseline: projections are labelled accepted", 0L, function(r) NULL, check = function(o) identical(proj_status(o), "accepted"))
case("RC1: ONE enum30 unit has no wall/user/sys measurement -> INCOMPLETE and projections NOT ACCEPTED", 3L,
     function(r) edit_tsv(tim(r), function(x) { i <- which(x$arm == "enum30")[2]; x$wall_s[i] <- NA; x$user_s[i] <- NA; x$sys_s[i] <- NA; x }),
     check = function(o) any(grepl("NOT ACCEPTED", proj_status(o))) && any(grepl("NOT ACCEPTED", readLines(file.path(o, "PILOT_SUMMARY.md")))))
case("RC1: all six enum30 wall times are zero -> invalid", 2L, function(r) edit_tsv(tim(r), function(x) { x$wall_s[x$arm == "enum30"] <- 0; x }))
case("RC1: one enum20 wall time is negative -> invalid", 2L, function(r) edit_tsv(tim(r), function(x) { x$wall_s[which(x$arm == "enum20")[4]] <- -1; x }))
case("RC1: all enum30 CPU times (user+sys) missing -> INCOMPLETE (CPU policy for enumeration units)", 3L, function(r) edit_tsv(tim(r), function(x) { i <- x$arm == "enum30"; x$user_s[i] <- NA; x$sys_s[i] <- NA; x }))
case("RC1: one enum20 unit has negative CPU time -> invalid", 2L, function(r) edit_tsv(tim(r), function(x) { x$user_s[which(x$arm == "enum20")[5]] <- -3; x }))
case("RC1: one SMC unit has no wall time -> INCOMPLETE", 3L, function(r) edit_tsv(tim(r), function(x) { x$wall_s[which(x$arm == "smc")[7]] <- NA; x }))
case("RC1: one benchmark unit has wall time zero -> invalid", 2L, function(r) edit_tsv(tim(r), function(x) { x$wall_s[which(x$arm == "bench")[50]] <- 0; x }))
case("RC1: single-thread SMC/benchmark CPU times missing are accepted (costed as wall x 1 CPU)", 0L, function(r) edit_tsv(tim(r), function(x) { i <- x$arm %in% c("smc", "bench"); x$user_s[i] <- NA; x$sys_s[i] <- NA; x }))
case("RC2: scaling file names the wrong dataset (a p = 20 one)", 2L, edit_sc(function(x) { x$dataset <- "dev_p0020_S1_r001"; x }))
case("RC2: models_total = 1 in every row (wrong coverage)", 2L, edit_sc(function(x) { x$models_total <- 1; x }))
case("RC2: models_total wrong in ONE row only (every row is checked)", 2L, edit_sc(function(x) { x$models_total[3] <- 2^20; x }))
case("RC2: tasks_run = 1 in the first row, 31 in the others", 2L, edit_sc(function(x) { x$tasks_run[1] <- 1; x }))
case("RC2: models_scored inconsistent with tasks_run x models_total / n_tasks (all rows)", 2L, edit_sc(function(x) { x$models_scored <- x$models_scored - 1; x }))
case("RC2: declared fraction differs in one row", 2L, edit_sc(function(x) { x$fraction[4] <- 0.05; x }))
case("RC2: the rows did not run one common task subset (tasks_sha256 differs)", 2L, edit_sc(function(x) { x$tasks_sha256[2] <- digest::digest("other", algo = "sha256", serialize = FALSE); x }))
case("RC2: the task-subset hash column is absent (old scaling script) -> INCOMPLETE", 3L, edit_sc(function(x) { x$tasks_sha256 <- NULL; x }))
case("RC2: a scaling wall time is zero", 2L, edit_sc(function(x) { x$wall_s[2] <- 0; x }))
smc_unit <- function(r, k = 1, rep = FALSE) list.files(resof(r, "smc"), pattern = if (rep) "SMCBVS_rep1[.]rds$" else "^SMCBVS[.]rds$", recursive = TRUE, full.names = TRUE)[k]
case("RC4: SMC HPM = integer(0) (null model) is a valid fit (baseline unit 3) and keeps its timing", 0L, function(r) NULL,
     check = function(o) { u <- read.csv(file.path(o, "pilot_units.csv")); isTRUE(u$valid[u$unit == "dev_p0020_S2_r001_c100"]) })
case("RC4: SMC fit$hpm absent -> invalid", 2L, function(r) { f <- smc_unit(r, 4); rewrite_rds(f, function(z) { z$fit$hpm <- NULL; z }); resign_pair(f) })
case("RC4: SMC fit$hpm malformed (NA / non-integer)", 2L, function(r) { f <- smc_unit(r, 5); rewrite_rds(f, function(z) { z$fit$hpm <- c(3, 7.5); z }); resign_pair(f) })
case("RC4: SMC fit$hpm index above p (original-index bound)", 2L, function(r) { f <- smc_unit(r, 6); rewrite_rds(f, function(z) { z$fit$hpm <- c(3L, 99L); z }); resign_pair(f) })
case("RC4: SMC fit$hpm index zero / negative", 2L, function(r) { f <- smc_unit(r, 7); rewrite_rds(f, function(z) { z$fit$hpm <- c(0L, 3L); z }); resign_pair(f) })
case("RC4: SMC fit$hpm unsorted or duplicated", 2L, function(r) { f <- smc_unit(r, 8); rewrite_rds(f, function(z) { z$fit$hpm <- c(7L, 3L); z }); resign_pair(f) })
case("RC4: a repeat fit with an empty HPM and a different primary HPM is still valid (different seeds)", 0L, function(r) { f <- smc_unit(r, 1, TRUE); rewrite_rds(f, function(z) { z$fit$hpm <- integer(0); z }); resign_pair(f) })
## ---- N1 / N2 / N3 cases (third final confirmation) ----
all_pos <- function(o) { p <- read.csv(file.path(o, "pilot_projection.csv")); all(is.na(p$suggested_mem_request_mb[p$piece != "TOTAL"]) | p$suggested_mem_request_mb[p$piece != "TOTAL"] > 0) }
accepted_all_pos <- function(o) { p <- read.csv(file.path(o, "pilot_projection.csv")); q <- p[p$piece != "TOTAL", ]; all(q$suggested_mem_request_mb > 0) && all(q$status == "accepted") }
set_rss <- function(val, arms = c("enum20", "enum30", "scale", "smc", "bench")) function(r) edit_tsv(tim(r), function(x) { x$maxrss_kb[x$arm %in% arms] <- val; x })
zero_batch <- function(r) { for (nm in c("sacct_final.tsv", "sacct_collector.tsv")) { f <- file.path(logsof(r), "accounting", nm); x <- read.delim(f, sep = "|", stringsAsFactors = FALSE, colClasses = "character"); i <- grepl("[.]batch$", x$JobID); x$MaxRSS[i] <- "0M"; write.table(x, f, sep = "|", quote = FALSE, row.names = FALSE) } }
case("N1: every GNU RSS is 0 but positive batch/core figures exist -> fallback with an explicit label, requests > 0, accepted", 0L, set_rss(0),
     check = function(o) { u <- read.csv(file.path(o, "pilot_units.csv")); accepted_all_pos(o) && all(grepl("unusable", u$mem_source[u$unit %in% c("dev_p0020_S1_r001", "dev_p0030_S1_r001")])) && all(u$mem_source != "gnu_time") })
case("N1: every GNU RSS is negative, positive fallbacks exist -> accepted with the fallback label", 0L, set_rss(-5000), check = accepted_all_pos)
case("N1: GNU RSS 0 and batch MaxRSS 0 for enumerations and benchmarks (no positive source) -> INCOMPLETE and NOT ACCEPTED, no accepted request <= 0", 3L,
     function(r) { set_rss(0, c("enum20", "enum30", "scale", "bench"))(r); zero_batch(r) },
     check = function(o) { p <- read.csv(file.path(o, "pilot_projection.csv")); q <- p[p$piece != "TOTAL", ]; all(grepl("NOT ACCEPTED", p$status)) && !any(q$status == "accepted" & !(q$suggested_mem_request_mb > 0)) })
case("N1: SMC GNU RSS 0, no sacct snapshots: the core's own VmHWM is the labelled fallback for SMC (other arms keep GNU time)", 3L,
     function(r) { set_rss(0, "smc")(r); unlink(file.path(logsof(r), "accounting", "sacct_final.tsv")); unlink(file.path(logsof(r), "accounting", "sacct_collector.tsv")) },
     check = function(o) { u <- read.csv(file.path(o, "pilot_units.csv")); all(u$mem_source[u$arm %in% c("smc", "smc_rep")] == "core_vmhwm (GNU/sacct RSS unusable)") })
case("N1: one benchmark unit with GNU RSS 0 and its batch MaxRSS 0 -> that unit is absent evidence (INCOMPLETE)", 3L,
     function(r) { edit_tsv(tim(r), function(x) { i <- which(x$arm == "bench")[9]; x$maxrss_kb[i] <- 0; assign("tk", x$taskid[i], envir = globalenv()); assign("jk", x$jobid[i], envir = globalenv()); x })
                   for (nm in c("sacct_final.tsv", "sacct_collector.tsv")) { f <- file.path(logsof(r), "accounting", nm); x <- read.delim(f, sep = "|", stringsAsFactors = FALSE, colClasses = "character"); x$MaxRSS[x$JobID == paste0(jk, "_", tk, ".batch")] <- "0M"; write.table(x, f, sep = "|", quote = FALSE, row.names = FALSE) } })
case("N2: re-signed enum record with impossible PIPs (all 1, mpm = all variables) is rejected", 2L, function(r) { f <- enum_unit(r, "enum20", 8); rewrite_rds(f, function(z) { z$scales$c100$pip[] <- 1; z$scales$c100$mpm <- seq_len(z$p); z }); resign_enum(f) })
case("N2: re-signed enum record whose PIPs do not match the size distribution (sum PIP != E|S|)", 2L, function(r) { f <- enum_unit(r, "enum20", 9); rewrite_rds(f, function(z) { z$scales$c050$pip <- pmin(1, z$scales$c050$pip + 0.01); z$scales$c050$mpm <- as.integer(seq_len(z$p)[z$scales$c050$pip > 0.5]); z }); resign_enum(f) })
case("N3: scaling tasks_sha256 is the same placeholder string in every row (not a 64-hex digest)", 2L, edit_sc(function(x) { x$tasks_sha256 <- "not-a-sha256"; x }))
case("N3: scaling dataset is NA -> a full FAIL report, not a crash", 2L, edit_sc(function(x) { x$dataset <- NA; x }), check = function(o) file.exists(file.path(o, "PILOT_SUMMARY.md")) && file.exists(file.path(o, "pilot_projection.csv")))
case("N3: scaling numeric column holds text -> FAIL report", 2L, edit_sc(function(x) { x$n_tasks <- as.character(x$n_tasks); x$n_tasks[2] <- "many"; x }), check = function(o) file.exists(file.path(o, "PILOT_SUMMARY.md")))
case("N3: scaling wall_s is NA in one row -> FAIL report", 2L, edit_sc(function(x) { x$wall_s[3] <- NA; x }), check = function(o) file.exists(file.path(o, "PILOT_SUMMARY.md")))
case("N3: a 64-hex digest in capital letters is not what the producer writes -> FAIL", 2L, edit_sc(function(x) { x$tasks_sha256 <- toupper(x$tasks_sha256); x }))
## ---- v2.2.1: P5 scan (DECISIONS D11), informative row; no existing gate changes ----
p5row <- function(o) { v <- read.csv(file.path(o, "pilot_verdicts.csv"), stringsAsFactors = FALSE); v[grepl("^P5 scan", v$item), , drop = FALSE] }
set_v3 <- function(f, val) { b <- sub("[.]rds$", "", f); x <- read.csv(paste0(b, ".csv"), colClasses = "character"); x$v3_status <- val; write.csv(x, paste0(b, ".csv"), row.names = FALSE); resign_pair(f) }
case("v2.2.1 P5: baseline (no resource_limit) -> P5 row PASS with 0/0, TSV and summary section written", 0L, function(r) NULL,
     check = function(o) { p <- p5row(o); nrow(p) == 1L && p$verdict == "PASS" && grepl("primary_resource_limit = 0, eligible = 0", p$detail) && file.exists(file.path(o, "pilot_p5_scan.tsv")) &&
                           any(grepl("^## P5 scan of the SMC results", readLines(file.path(o, "PILOT_SUMMARY.md")))) })
case("v2.2.1 P5: one SMC unit whose CSV says v3_status = resource_limit but the RDS native status is fine (re-signed) -> the CSV/RDS native-status gate FAILS (exit 2); P5 scan REFUSES the inconsistent unit (CONF-2b F3): row WARN 'scan NOT run' naming the CSV/RDS mismatch", 2L,
     function(r) set_v3(smc_unit(r, 3), "resource_limit"),
     check = function(o) { p <- p5row(o); nrow(p) == 1L && p$verdict == "WARN" && grepl("scan NOT run", p$detail) && grepl("differs from the RDS native status", p$detail) &&
                           any(grepl("The P5 scan was NOT run", readLines(file.path(o, "PILOT_SUMMARY.md")))) })
case("v2.2.1 P5: every SMC CSV carries v3_status equal to the RDS native status -> accepted (exit 0), P5 row PASS", 0L,
     function(r) for (f in list.files(resof(r, "smc"), pattern = "[.]rds$", recursive = TRUE, full.names = TRUE)) if (!grepl("P5_retry", f)) set_v3(f, readRDS(f)$fit$status),
     check = function(o) { p <- p5row(o); nrow(p) == 1L && p$verdict == "PASS" })
case("v2.2.1 P5 (Sol review 2, R2-3): one SMC record WITHOUT top-level native_status (re-signed; fit$status and CSV v3_status fine) -> the scan no longer falls back to fit$status: it refuses, P5 row WARN 'scan NOT run' naming 'absent' (summarizer gates unchanged: exit 0)", 0L,
     function(r) { f <- smc_unit(r, 3); rewrite_rds(f, function(z) { z$native_status <- NULL; z }); resign_pair(f) },
     check = function(o) { p <- p5row(o); nrow(p) == 1L && p$verdict == "WARN" && grepl("scan NOT run", p$detail) && grepl("absent", p$detail) })
case("v2.2.1 P5: a real resource_limit unit (RDS fit$status and CSV) -> the existing native-status gate FAILS (exit 2) and the P5 row reports eligible = 1", 2L,
     function(r) { f <- smc_unit(r, 4); rewrite_rds(f, function(z) { z$fit$status <- "resource_limit"; z$native_status <- "resource_limit"; z }); set_v3(f, "resource_limit") },
     check = function(o) { p <- p5row(o); nrow(p) == 1L && p$verdict == "WARN" && grepl("eligible = 1", p$detail) })
case("v2.2.1 P5: tools/p5_scan.R not found (--v221-dir wrong) -> P5 row WARN 'scan NOT run', accepted, no other verdict changes", 0L, function(r) NULL, extra = c("--v221-dir", file.path(tempdir(), "no_such_v221")),
     check = function(o) { p <- p5row(o); nrow(p) == 1L && p$verdict == "WARN" && grepl("scan NOT run", p$detail) })
case("v2.2.1 P5: no _smc results folder supplied -> unit sets INCOMPLETE (exit 3), P5 row WARN 'scan NOT run'", 3L, function(r) NULL, drop = "smc",
     check = function(o) { p <- p5row(o); nrow(p) == 1L && grepl("scan NOT run", p$detail) })
lines <- c("# Negative tests of summarize_pilot.R (fabricated trees; expected exit 0 accepted / 2 FAIL / 3 INCOMPLETE)", "", "| Case | Expected exit | Got | Result |", "|---|---|---|---|"); allok <- TRUE
for (cs in cases) {
  k <- length(lines) - 4L; r <- file.path(work, sprintf("case_%02d", k)); unlink(r, recursive = TRUE); dir.create(r); file.copy(list.files(base, full.names = TRUE), r, recursive = TRUE)
  cs$mutate(r); s <- summ(r, cs$drop, cs$extra); ok <- identical(as.integer(s$rc), cs$rc) && (is.null(cs$check) || isTRUE(cs$check(s$o)))
  # failed units must not enter sizing
  allok <- allok && ok; lines <- c(lines, sprintf("| %s | %d | %s | %s |", cs$name, cs$rc, s$rc, if (ok) "ok" else "**WRONG**"))
  unlink(r, recursive = TRUE)
}
writeLines(c(lines, "", if (allok) "All cases behaved as expected." else "SOME CASES WRONG."), file.path(work, "NEGATIVE_TESTS.md")); cat(paste(lines, collapse = "\n"), "\n")
quit(save = "no", status = if (allok) 0L else 1L)
