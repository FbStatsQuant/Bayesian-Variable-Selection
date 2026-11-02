#!/usr/bin/env Rscript
# summarize_pilot.R -- turn the downloaded LOWP pilot outputs into ONE PILOT_SUMMARY.md plus CSV tables, and ACCEPT or REJECT the pilot.
# Replaces RUN_DESIGN.md section 2 and gives a projected production cost table for the section 3 layout.
#
#   Rscript summarize_pilot.R --results <dir>[,<dir>...] --logs <logs/<pilot id> dir> --out <output dir>
#                             [--lists <dir with enum20.txt, enum30.txt, smc_cases.tsv, bench_cases.tsv>] [--bench-lib <pinned library path>] [--label TEXT]
#                             [--v221-dir <code/core/v2_2_1>] [--rscript <Rscript>]   (P5 scan: runs <v221-dir>/tools/p5_scan.R over the _smc results; default ../../core/v2_2_1)
#   --results  result run folders (results/<stamp>_lowp_pilot_<arm>); the arm is the folder-name suffix:
#              _enum20 _enum30 _scale_t08 _scale_t16 _scale_t32 _smc _bench
#   --logs     the pilot's log folder (timing/, launch/, accounting/, p0_verify/, truthlock/, bitid/, scaling/, jobids.tsv)
#
# ACCEPTANCE. The expected unit sets come from the lists (30 enum20, 6 enum30, 3 scaling, 24 SMC primary, 4 SMC repeat, 192 benchmark units). A unit is
# VALID only if its files exist with matching sha256 sidecar/marker, its timing row exists with rc 0, and its record passes the semantic checks. Failed or
# missing units never enter the sizing tables. Verdicts are PASS / WARN (accepted, flagged) / FAIL / INCOMPLETE (evidence absent). Exit status:
# 0 = PASS or WARN overall; 2 = some FAIL; 3 = some INCOMPLETE (no FAIL). The files are still written, labelled with the overall status.
# Base R + digest. Never opens a truth folder.

a <- commandArgs(trailingOnly = TRUE)
opt <- function(k, d = NULL) { i <- match(paste0("--", k), a); if (is.na(i) || i == length(a)) d else a[i + 1L] }
res_dirs <- strsplit(opt("results", ""), ",")[[1]]; res_dirs <- res_dirs[nzchar(res_dirs)]
logs <- opt("logs"); out <- opt("out"); label <- opt("label", "")
bench_lib <- opt("bench-lib", "/projects/ml75/fb31/BVS/bench20261019/lib/R452")
here <- local({ f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1L]); if (is.na(f)) getwd() else dirname(normalizePath(f, winslash = "/")) })
lists <- opt("lists", file.path(here, "lists"))
enum_dir <- opt("enum-dir", file.path(here, "..", "enum"))
if (!file.exists(file.path(enum_dir, "exact_contract.R"))) stop("exact_contract.R not found in ", enum_dir, " (the shared EXACT validator is required)")
source(file.path(enum_dir, "exact_contract.R"))   # lowp_validate_exact(): the one strict I2 validator, shared with the producers
if (is.null(out)) stop("usage: summarize_pilot.R --results DIR[,DIR] --logs DIR --out DIR [--lists DIR] [--bench-lib PATH]")
if (any(grepl("(^|[/\\\\])truth([/\\\\]|$)", c(res_dirs, logs)))) stop("a truth path was supplied")
stopifnot(requireNamespace("digest", quietly = TRUE))
dir.create(out, recursive = TRUE, showWarnings = FALSE)

# ---------------------------------------------------------------------------------------------------------------- helpers
`%||%` <- function(x, y) if (is.null(x) || (length(x) == 1L && is.na(x))) y else x
q90 <- function(x) if (length(x[is.finite(x)])) unname(quantile(x[is.finite(x)], 0.9, type = 7)) else NA_real_
med <- function(x) if (length(x[is.finite(x)])) median(x[is.finite(x)]) else NA_real_
mx  <- function(x) if (length(x[is.finite(x)])) max(x[is.finite(x)]) else NA_real_
mn  <- function(x) if (length(x[is.finite(x)])) mean(x[is.finite(x)]) else NA_real_
num <- function(x) suppressWarnings(as.numeric(x))
fsz <- function(files) sum(file.info(files)$size, na.rm = TRUE) / 1024
fmt <- function(x, d = 3) ifelse(is.na(x), "NA", formatC(signif(x, d), format = "fg", digits = d, flag = "#", drop0trailing = TRUE))
hms <- function(s) ifelse(is.na(s), "NA", sprintf("%02d:%02d", as.integer(s %/% 3600), as.integer((s %% 3600) %/% 60)))
md_table <- function(df) {
  if (!nrow(df)) return("(no rows)")
  df[] <- lapply(df, function(c) if (is.numeric(c)) fmt(c) else ifelse(is.na(c), "NA", as.character(c)))
  c(paste0("| ", paste(names(df), collapse = " | "), " |"), paste0("|", paste(rep("---", ncol(df)), collapse = "|"), "|"),
    apply(df, 1, function(r) paste0("| ", paste(r, collapse = " | "), " |")))
}
safe <- function(expr, default = NA) tryCatch(expr, error = function(e) default)
sha <- function(f) digest::digest(file = f, algo = "sha256")
rd_lines <- function(f) if (file.exists(f)) readLines(f, warn = FALSE) else NULL
rdl <- function(rel) if (!is.null(logs)) rd_lines(file.path(logs, rel)) else NULL
norm_path <- function(x) sub("/+$", "", gsub("\\\\", "/", x))

# ---------------------------------------------------------------------------------------------------------------- expected sets
read_list <- function(f) { x <- rd_lines(file.path(lists, f)); if (is.null(x)) stop("list not found: ", file.path(lists, f)); x }
enum20_ids <- trimws(read_list("enum20.txt")); enum20_ids <- enum20_ids[nzchar(enum20_ids)]
enum30_ids <- trimws(read_list("enum30.txt")); enum30_ids <- enum30_ids[nzchar(enum30_ids)]
smc_cases <- utils::read.delim(file.path(lists, "smc_cases.tsv"), stringsAsFactors = FALSE)
bench_cases <- utils::read.delim(file.path(lists, "bench_cases.tsv"), stringsAsFactors = FALSE)
METHODS <- c("F1", "F2", "F3", "F4", "F5", "A1", "A2", "A3")
pdir_of <- function(ds) paste0("p", substr(sub("^dev_", "", ds), 2, 5))
E <- rbind(
  data.frame(arm = "enum", run = "enum20", p = 20L, dir = enum20_ids, base = "EXACT", tarm = "enum20", tkey = enum20_ids, thr = 4L, kind = "enum", rep = 0L, ds = enum20_ids, scale = NA_character_, method = NA_character_, stringsAsFactors = FALSE),
  data.frame(arm = "enum", run = "enum30", p = 30L, dir = enum30_ids, base = "EXACT", tarm = "enum30", tkey = enum30_ids, thr = 16L, kind = "enum", rep = 0L, ds = enum30_ids, scale = NA_character_, method = NA_character_, stringsAsFactors = FALSE),
  data.frame(arm = "scale", run = sprintf("scale_t%02d", c(8, 16, 32)), p = 30L, dir = "dev_p0030_S4_r001", base = "EXACT", tarm = "scale", tkey = paste0("full_t", c(8, 16, 32)), thr = c(8L, 16L, 32L), kind = "enum", rep = 0L, ds = "dev_p0030_S4_r001", scale = NA_character_, method = NA_character_, stringsAsFactors = FALSE),
  data.frame(arm = ifelse(smc_cases$repeat. > 0, "smc_rep", "smc"), run = "smc", p = as.integer(substr(pdir_of(smc_cases$dataset), 2, 5)), dir = paste0(smc_cases$dataset, "_", smc_cases$scale),
             base = ifelse(smc_cases$repeat. > 0, paste0("SMCBVS_rep", smc_cases$repeat.), "SMCBVS"), tarm = "smc",
             tkey = paste0(smc_cases$dataset, "_", smc_cases$scale, ifelse(smc_cases$repeat. > 0, paste0("_rep", smc_cases$repeat.), "")), thr = 1L, kind = "smc",
             rep = as.integer(smc_cases$repeat.), ds = smc_cases$dataset, scale = smc_cases$scale, method = NA_character_, stringsAsFactors = FALSE))
bk <- merge(bench_cases, data.frame(method = METHODS), by = NULL)
E <- rbind(E, data.frame(arm = bk$method, run = "bench", p = as.integer(substr(pdir_of(bk$dataset), 2, 5)), dir = paste0(bk$dataset, "_", bk$scale), base = bk$method, tarm = "bench",
                         tkey = paste0(bk$dataset, "_", bk$scale, "_", bk$method), thr = 1L, kind = "bench", rep = 0L, ds = bk$dataset, scale = bk$scale, method = bk$method, stringsAsFactors = FALSE))
E$pdir <- sprintf("p%04d", E$p)
EXPECT_N <- c(enum20 = 30L, enum30 = 6L, scale = 3L, smc = 24L, smc_rep = 4L, bench = 192L)
stopifnot(sum(E$run == "enum20") == EXPECT_N[["enum20"]], sum(E$run == "enum30") == EXPECT_N[["enum30"]], sum(E$arm == "scale") == 3L,
          sum(E$arm == "smc") == EXPECT_N[["smc"]], sum(E$arm == "smc_rep") == EXPECT_N[["smc_rep"]], sum(E$run == "bench") == EXPECT_N[["bench"]])

run_dir <- list()
for (d in res_dirs) { b <- basename(normalizePath(d, winslash = "/", mustWork = FALSE)); m <- regmatches(b, regexpr("(enum20|enum30|scale_t[0-9]+|smc|bench)$", b)); if (length(m) && dir.exists(d)) run_dir[[m]] <- d else message("skipping ", d) }

# ---------------------------------------------------------------------------------------------------------------- timing and accounting
timing <- NULL
if (!is.null(logs) && dir.exists(file.path(logs, "timing"))) {
  tf <- list.files(file.path(logs, "timing"), pattern = "\\.tsv$", full.names = TRUE)
  if (length(tf)) timing <- do.call(rbind, lapply(tf, function(f) utils::read.delim(f, stringsAsFactors = FALSE, na.strings = "NA", colClasses = c(unit = "character", arm = "character"))))
}
trow <- function(arm, unit) { if (is.null(timing)) return(data.frame(rc = numeric(), wall_s = numeric(), user_s = numeric(), sys_s = numeric(), maxrss_kb = numeric(), jobid = character(), taskid = character())); timing[timing$arm == arm & timing$unit == unit, , drop = FALSE] }

parse_sacct <- function(f) {
  x <- safe(utils::read.delim(f, sep = "|", stringsAsFactors = FALSE, check.names = FALSE, colClasses = "character"), NULL)
  if (is.null(x) || !all(c("JobID", "State", "ExitCode") %in% names(x))) return(NULL)
  x
}
sacct_final <- if (!is.null(logs)) parse_sacct(file.path(logs, "accounting", "sacct_final.tsv")) else NULL
sacct_coll <- if (!is.null(logs)) parse_sacct(file.path(logs, "accounting", "sacct_collector.tsv")) else NULL
sacct <- if (!is.null(sacct_final)) sacct_final else sacct_coll
jobids <- if (!is.null(logs) && file.exists(file.path(logs, "jobids.tsv"))) utils::read.delim(file.path(logs, "jobids.tsv"), stringsAsFactors = FALSE, colClasses = "character") else NULL
batch_mb <- function(jobid, taskid) {      # MaxRSS (MB) of the batch step of a job/array task, or NA
  if (is.null(sacct)) return(NA_real_)
  for (key in c(paste0(jobid, "_", taskid, ".batch"), paste0(jobid, ".batch"))) {
    r <- sacct[sacct$JobID == key, , drop = FALSE]
    if (nrow(r)) { v <- num(sub("[MK]$", "", r$MaxRSS[1])); if (is.finite(v)) return(v) }
  }
  NA_real_
}

# ---------------------------------------------------------------------------------------------------------------- unit validation
OKSTAT <- "ok"; WARNSTAT <- "warning"
check_hash_files <- function(dir, base, exts, kind) {
  r <- character()
  fs <- file.path(dir, paste0(base, ".", exts))
  miss <- exts[!file.exists(fs)]
  if (length(miss)) return(paste0("missing file(s): ", paste0(base, ".", miss, collapse = ", ")))
  rds <- file.path(dir, paste0(base, ".rds")); h <- sha(rds)
  sidecar <- rd_lines(file.path(dir, paste0(base, ".sha256"))); dn <- rd_lines(file.path(dir, paste0(base, ".done")))
  tok <- function(l) tolower(sub("^([0-9a-fA-F]{64}).*$", "\\1", l))
  if (kind == "enum") {
    if (!length(sidecar) || !identical(tok(sidecar[1]), h)) r <- c(r, "sidecar sha256 differs from the RDS")
    if (!length(dn) || !identical(tok(dn[1]), h)) r <- c(r, ".done marker hash differs from the RDS")
  } else {
    for (e in c("rds", "csv")) {
      line <- sidecar[grepl(paste0("[ *]", base, "\\.", e, "$"), sidecar)]
      if (length(line) != 1L || !identical(tok(line), sha(file.path(dir, paste0(base, ".", e))))) r <- c(r, paste0("sidecar sha256 missing or differs for .", e))
    }
    if (!length(dn) || !any(grepl("^status", dn))) r <- c(r, ".done marker lacks a status line")
  }
  r
}
req <- function(z, nm) setdiff(nm, names(z))
status_ok <- function(s) all(s %in% c(OKSTAT, WARNSTAT)); has_warn <- function(s) any(s == WARNSTAT)

check_enum <- function(z, id, p, thr) {
  # the shared strict contract (INTERFACES I2): every readiness field, full exact scope on both scales, normalised size masses, retained-column coverage
  v <- lowp_validate_exact(z, requested_scales = c("c100", "c050"), input = list(dataset_id = id), mode = "sealed", exact_scale_set = TRUE)
  r <- if (isTRUE(v$ok)) character() else paste0("bad: contract: ", v$reasons)
  if (!is.list(z)) return(r)
  # pilot-specific expectations on top of the contract
  if (!identical(as.integer(z$p), as.integer(p)) || !identical(as.integer(z$n), 200L)) r <- c(r, "bad: p or n differs from the design")
  if (!identical(as.integer(z$threads), as.integer(thr))) r <- c(r, "bad: threads")
  if (!is.finite(num(z$runtime_s)) || num(z$runtime_s) <= 0) r <- c(r, "bad: runtime_s")
  for (s in c("c100", "c050")) { N <- z$scales[[s]]$numerics
    if (is.list(N)) { if (!isTRUE(num(N$recheck_count) > 0)) r <- c(r, paste0("bad: ", s, " no internal re-check coverage")); if (!isTRUE(num(N$n_fallback_v3) == 0)) r <- c(r, paste0("bad: ", s, " fallbacks to Scorer::score")) } }
  r
}
# the .done marker, the CSV and the RDS rows must tell the same story (a marker saying failed while the CSV says ok, or the reverse, is rejected)
status_consistency <- function(dn, csv, z) {
  r <- character(); line <- dn[grepl("^status", dn)][1]
  if (is.na(line)) return("bad: .done marker has no status line")
  if (!identical(trimws(sub("^status", "", line)), paste(csv$status, collapse = ","))) r <- c(r, sprintf("bad: .done status (%s) differs from the CSV rule statuses (%s)", trimws(sub("^status", "", line)), paste(csv$status, collapse = ",")))
  rs <- if (is.data.frame(z$rows) && "status" %in% names(z$rows)) as.character(z$rows$status) else NULL
  if (is.null(rs)) r <- c(r, "missing: rds rows$status") else if (!identical(rs, as.character(csv$status))) r <- c(r, "bad: RDS rows$status differs from the CSV statuses")
  r
}
check_smc <- function(z, csv, ds, scale, rep, dir, dn) {
  r <- character()
  mc <- req(csv, c("case_id", "scale_key", "regime", "study", "data_seed", "method_seed", "status", "role"))
  if (length(mc)) return(paste("missing: csv columns", paste(mc, collapse = ",")))
  if (nrow(csv) < 2L) r <- c(r, "bad: fewer than two rule rows")
  if (!all(csv$case_id == dir) || !all(csv$scale_key == scale)) r <- c(r, "bad: case or scale in csv")
  if (!all(csv$regime == "L") || !all(csv$study == "newcampaign_lowp")) r <- c(r, "bad: regime/study")
  if (length(unique(csv$method_seed)) != 1L || length(unique(csv$data_seed)) != 1L || !isTRUE(num(csv$method_seed[1]) == num(csv$data_seed[1]) + 4000000 + 1000 * rep))
    r <- c(r, sprintf("bad: method seed is not data seed + 4,000,000 + 1,000 x %d", rep))
  if (!status_ok(csv$status)) r <- c(r, paste0("bad: rule status ", paste(unique(csv$status[!csv$status %in% c(OKSTAT, WARNSTAT)]), collapse = "/")))
  r <- c(r, status_consistency(dn, csv, z)); if ("runtime_s" %in% names(csv) && is.finite(num(z$runtime_s)) && !isTRUE(all(abs(num(csv$runtime_s) - num(z$runtime_s)) <= 1e-6 * max(1, abs(num(z$runtime_s)))))) r <- c(r, "bad: CSV runtime_s differs from the RDS runtime_s")
  mz <- req(z, c("runtime_s", "fit", "estimates_available")); if (length(mz)) return(c(r, paste("missing: rds", paste(mz, collapse = ","))))
  if (!is.finite(num(z$runtime_s)) || num(z$runtime_s) <= 0) r <- c(r, "bad: runtime_s")
  if (!isTRUE(z$estimates_available)) r <- c(r, "bad: no estimates")
  f <- z$fit; mf <- req(f, c("status", "log_Z", "hpm", "calibration", "runtime_guard"))
  if (length(mf)) return(c(r, paste("missing: fit$", paste(mf, collapse = ","))))
  if (!as.character(f$status) %in% c("completed", "exact")) r <- c(r, paste0("bad: native status ", f$status))
  # v2.2.1: the CSV v3_status column (read by tools/p5_scan.R) must equal the RDS native status (a CSV that disagrees with its RDS is an inconsistent unit)
  if ("v3_status" %in% names(csv) && !isTRUE(all(as.character(csv$v3_status) == as.character(f$status)))) r <- c(r, sprintf("bad: CSV v3_status (%s) differs from the RDS native status (%s)", paste(unique(csv$v3_status), collapse = "/"), f$status))
  if (!is.finite(num(f$log_Z))) r <- c(r, "bad: log_Z not finite")
  pd <- as.integer(substr(sub("^dev_", "", ds), 2, 5))      # original number of columns of the dataset
  h <- f$hpm
  if (is.null(h)) r <- c(r, "missing: fit$hpm")   # absent is not the same as empty: integer(0) is the valid null model
  else if (!is.numeric(h) || anyNA(h) || any(h != round(h))) r <- c(r, "bad: fit$hpm is malformed (not an integer vector without NA)")
  else if (length(h) && (any(h < 1 | h > pd) || is.unsorted(h, strictly = TRUE))) r <- c(r, sprintf("bad: fit$hpm is not a strictly increasing set of original indices within 1..%d", pd))
  if (!isFALSE(f$runtime_guard$exceeded)) r <- c(r, "bad: runtime guard exceeded or absent")
  if (is.null(f$calibration$tier_final)) r <- c(r, "missing: fit$calibration$tier_final")
  r
}
BASE_PKGS <- c("base", "compiler", "datasets", "graphics", "grDevices", "grid", "methods", "parallel", "splines", "stats", "stats4", "tcltk", "tools", "utils",
               "MASS", "Matrix", "boot", "class", "cluster", "codetools", "foreign", "KernSmooth", "lattice", "mgcv", "nlme", "nnet", "rpart", "spatial", "survival")
check_bench <- function(z, csv, dir, m, dn) {
  r <- character()
  mc <- req(csv, c("rule_id", "role", "status", "method_id", "case_id", "scale_key", "data_seed", "method_seed", "test_library", "runtime_s"))
  if (length(mc)) return(paste("missing: csv columns", paste(mc, collapse = ",")))
  if (!nrow(csv) || !any(csv$role == "primary")) r <- c(r, "bad: no primary rule row")
  if (!all(csv$method_id == m) || !all(csv$case_id == dir)) r <- c(r, "bad: method or case in csv")
  if (!status_ok(csv$status)) r <- c(r, paste0("bad: rule status ", paste(unique(csv$status[!csv$status %in% c(OKSTAT, WARNSTAT)]), collapse = "/")))
  if (!all(as.character(csv$test_library) %in% c("FALSE", "false", "F"))) r <- c(r, "bad: test_library is not FALSE (an unpinned library was allowed)")
  if (!isTRUE(all(num(csv$method_seed) == num(csv$data_seed) + 4000000))) r <- c(r, "bad: method seed")
  r <- c(r, status_consistency(dn, csv, z))
  # the per-fit runtime is rows$runtime_s of the record (the writer has no top-level runtime_s); it must be finite, positive and equal to the CSV
  rr <- if (is.data.frame(z$rows) && "runtime_s" %in% names(z$rows)) num(z$rows$runtime_s) else NULL
  if (is.null(rr)) r <- c(r, "missing: rds rows$runtime_s") else if (!all(is.finite(rr) & rr > 0)) r <- c(r, "bad: rows$runtime_s not finite and positive") else if (length(rr) != nrow(csv) || !isTRUE(all(abs(rr - num(csv$runtime_s)) <= 1e-6 * pmax(1, abs(rr))))) r <- c(r, "bad: rows$runtime_s differs from the CSV runtime_s")
  env <- z$environment
  if (is.null(env)) return(c(r, "missing: rds environment"))
  if (!isFALSE(env$test_library)) r <- c(r, "bad: rds test_library is not FALSE")
  lib <- norm_path(bench_lib)
  if (!identical(norm_path(env$sealed_library %||% ""), lib)) r <- c(r, "bad: sealed library is not the pinned library")
  # effective R: the saved session must be R 4.5.2 (the pinned library is an R 4.5.2 library), also for dev ids
  si <- as.character(env$sessionInfo %||% character()); rv <- si[grepl("^R version", si)][1]
  if (is.na(rv)) r <- c(r, "missing: sessionInfo R version") else if (!grepl("^R version 4[.]5[.]2( |$)", rv)) r <- c(r, paste0("bad: effective R is not 4.5.2 (", rv, ")"))
  pv <- env$package_provenance
  if (!length(pv)) r <- c(r, "missing: package provenance")
  else {
    nb <- names(pv)[!names(pv) %in% BASE_PKGS]
    if (!length(nb)) r <- c(r, "missing: no non-base package in the provenance")
    # EXACT library parent: dirname(path) must equal the pinned library (a sibling such as R452_UNAPPROVED or a prefix match is not enough)
    out_of <- nb[!vapply(nb, function(k) identical(norm_path(dirname(norm_path(pv[[k]]$path %||% ""))), lib), NA)]
    if (length(out_of)) r <- c(r, paste0("bad: package(s) not directly inside the pinned library: ", paste(out_of, collapse = ",")))
    nov <- nb[!vapply(nb, function(k) is.character(pv[[k]]$version) && length(pv[[k]]$version) == 1L && nzchar(pv[[k]]$version), NA)]
    if (length(nov)) r <- c(r, paste0("missing: package version for ", paste(nov, collapse = ",")))
    nob <- nb[!vapply(nb, function(k) is.character(pv[[k]]$built) && length(pv[[k]]$built) == 1L && grepl("^4[.]5[.]", pv[[k]]$built), NA)]
    if (length(nob)) r <- c(r, paste0("bad: package(s) not built under R 4.5.x: ", paste(nob, collapse = ",")))
    # the method's own package must be in the provenance with the version the CSV states
    if ("package" %in% names(csv) && "package_version" %in% names(csv)) { pk <- as.character(csv$package[1]); pvv <- as.character(csv$package_version[1])
      if (!pk %in% names(pv)) r <- c(r, paste0("bad: method package ", pk, " absent from the provenance")) else if (!identical(as.character(pv[[pk]]$version), pvv)) r <- c(r, paste0("bad: ", pk, " version ", pv[[pk]]$version, " differs from the CSV package_version ", pvv)) }
    else r <- c(r, "missing: csv package/package_version")
  }
  r
}

U <- list(); exact_objs <- list(); smc_seed <- list(); dir_extra <- character()
for (i in seq_len(nrow(E))) {
  e <- E[i, ]; rd <- run_dir[[e$run]]; why <- character(); zz <- NULL; csv <- NULL
  dir <- if (is.null(rd)) NA_character_ else file.path(rd, e$pdir, e$dir)
  if (is.null(rd)) why <- "result folder not supplied"
  else if (!dir.exists(dir)) why <- "unit folder missing"
  else {
    exts <- if (e$kind == "enum") c("rds", "sha256", "done") else c("rds", "csv", "sha256", "done")
    why <- check_hash_files(dir, e$base, exts, e$kind)
    if (!length(why)) {
      zz <- safe(readRDS(file.path(dir, paste0(e$base, ".rds"))), NULL)
      csv <- if (e$kind != "enum") safe(utils::read.csv(file.path(dir, paste0(e$base, ".csv")), stringsAsFactors = FALSE), NULL) else NULL
      if (is.null(zz) || (e$kind != "enum" && is.null(csv))) why <- "unreadable record"
      else why <- switch(e$kind, enum = check_enum(zz, e$dir, e$p, e$thr), smc = check_smc(zz, csv, e$ds, e$scale, e$rep, e$dir, rd_lines(file.path(dir, paste0(e$base, ".done")))), bench = check_bench(zz, csv, e$dir, e$method, rd_lines(file.path(dir, paste0(e$base, ".done")))))
      if (e$kind == "smc" && !is.null(csv)) smc_seed[[e$tkey]] <- list(ds = paste(e$ds, e$scale), rep = e$rep, seed = num(csv$method_seed[1]), logZ = num(zz$fit$log_Z), hpm = paste(zz$fit$hpm, collapse = ";"))
    }
  }
  absent <- is.null(rd) || is.na(dir) || !dir.exists(dir) || any(grepl("^missing file", why))
  tr <- trow(e$tarm, e$tkey)
  if (nrow(tr) != 1L) { why <- c(why, if (nrow(tr) == 0L) "no timing row" else "duplicate timing rows"); if (nrow(tr) == 0L) absent <- TRUE }
  else if (!isTRUE(num(tr$rc) == 0)) why <- c(why, paste0("unit exit status rc=", tr$rc))
  wall <- if (nrow(tr) == 1L) num(tr$wall_s) else NA_real_
  cpu <- if (nrow(tr) == 1L) num(tr$user_s) + num(tr$sys_s) else NA_real_
  # RC1 policy. WALL: every required unit needs a finite POSITIVE process wall time (missing -> the unit is absent evidence, INCOMPLETE; zero or negative -> invalid, FAIL).
  # CPU: enumeration units (multi-thread, CPU-bound) need observed user+sys (finite, not negative); its absence is absent evidence (INCOMPLETE). Single-thread SMC and
  # benchmark units are costed as wall x 1 CPU, so their CPU time is informational only.
  if (nrow(tr) == 1L && isTRUE(num(tr$rc) == 0)) {
    if (!is.finite(wall)) { why <- c(why, "no finite wall time in the timing row"); absent <- TRUE } else if (wall <= 0) why <- c(why, "bad: wall time is zero or negative")
    if (e$kind == "enum") { if (!is.finite(cpu)) { why <- c(why, "no observed CPU time (user+sys) for an enumeration unit (policy: required)"); absent <- TRUE } else if (cpu < 0) why <- c(why, "bad: negative CPU time") }
  }
  gnu <- if (nrow(tr) == 1L) num(tr$maxrss_kb) / 1024 else NA_real_
  bound <- if (nrow(tr) == 1L) batch_mb(tr$jobid, tr$taskid) else NA_real_
  core_mb <- if (e$kind == "smc" && !is.null(zz)) num(zz$fit$peak_memory_kb) / 1024 else NA_real_
  # N1: a memory figure is usable only if finite AND positive (an R process always has a footprint; 0 or negative is a broken measurement). Order: GNU time, then the
  # batch-step MaxRSS of the job (job-level bound), then the core's own VmHWM (SMC). A fallback is labelled with the reason; with no usable source the unit is absent evidence.
  posf <- function(v) is.finite(v) && v > 0
  if (posf(gnu)) { mem <- gnu; msrc <- "gnu_time" }
  else if (posf(bound)) { mem <- bound; msrc <- if (is.finite(gnu)) "sacct_job_bound (GNU RSS unusable)" else "sacct_job_bound" }
  else if (posf(core_mb)) { mem <- core_mb; msrc <- if (is.finite(gnu) || is.finite(bound)) "core_vmhwm (GNU/sacct RSS unusable)" else "core_vmhwm" }
  else { mem <- NA_real_; msrc <- "none"; if (!length(why)) { why <- c(why, "no positive memory evidence (GNU RSS, batch MaxRSS and core figure are absent, zero or negative)"); absent <- TRUE } }
  warn <- e$kind != "enum" && !length(why) && !is.null(csv) && has_warn(csv$status)
  rt_unit <- if (e$kind == "bench" && !is.null(zz) && is.data.frame(zz$rows) && "runtime_s" %in% names(zz$rows)) num(zz$rows$runtime_s)[1] else if (!is.null(zz) && !is.null(zz$runtime_s)) num(zz$runtime_s) else NA_real_
  U[[i]] <- data.frame(arm = e$arm, run = e$run, p = e$p, unit = e$tkey, threads = e$thr, valid = !length(why), absent = absent, warn = isTRUE(warn), why = paste(why, collapse = "; "),
                       runtime_s = rt_unit, wall_s = wall, cpu_s = cpu, maxrss_mb = mem, mem_source = msrc,
                       size_kb = if (!is.na(dir) && dir.exists(dir)) fsz(list.files(dir, pattern = paste0("^", e$base, "\\."), full.names = TRUE)) else NA_real_,
                       escalated = if (e$kind == "smc" && !is.null(zz)) isTRUE(zz$fit$calibration$escalated) || isTRUE(num(zz$fit$calibration$tier_final) > 0) else NA,
                       stringsAsFactors = FALSE)
  if (e$kind == "enum" && !length(why)) exact_objs[[paste(e$run, e$tkey)]] <- zz

}
UN <- do.call(rbind, U)
# unexpected units on disk (never accepted silently)
for (nm in names(run_dir)) { k <- E[E$run == nm, ]; for (pd in list.dirs(run_dir[[nm]], recursive = FALSE)) for (ud in list.dirs(pd, recursive = FALSE))
  if (!basename(ud) %in% k$dir) dir_extra <- c(dir_extra, file.path(nm, basename(pd), basename(ud))) }
utils::write.csv(UN, file.path(out, "pilot_units.csv"), row.names = FALSE)
VAL <- UN[UN$valid, ]       # only valid units enter sizing

# ---------------------------------------------------------------------------------------------------------------- table per arm and p (valid units only)
arm_levels <- c("enum", "smc", "smc_rep", METHODS)
T0 <- VAL[VAL$arm %in% arm_levels, , drop = FALSE]
tab <- data.frame()
if (nrow(T0)) {
  keys <- unique(T0[, c("arm", "p")]); keys <- keys[order(match(keys$arm, arm_levels), keys$p), ]
  tab <- do.call(rbind, lapply(seq_len(nrow(keys)), function(i) {
    s <- T0[T0$arm == keys$arm[i] & T0$p == keys$p[i], ]; nexp <- sum(UN$arm == keys$arm[i] & UN$p == keys$p[i] & UN$run != "scale")
    data.frame(arm = keys$arm[i], p = keys$p[i], threads = med(s$threads), n_valid = nrow(s), n_expected = nexp,
               run_med_s = med(s$runtime_s), run_p90_s = q90(s$runtime_s), run_max_s = mx(s$runtime_s),
               wall_med_s = med(s$wall_s), wall_p90_s = q90(s$wall_s), wall_max_s = mx(s$wall_s), cpu_med_s = med(s$cpu_s),
               peak_mem_max_mb = mx(s$maxrss_mb), mem_source = paste(sort(unique(s$mem_source)), collapse = "+"),
               size_mean_kb = mn(s$size_kb), size_max_kb = mx(s$size_kb),
               escalations = if (all(is.na(s$escalated))) NA else sum(s$escalated, na.rm = TRUE), warnings = sum(s$warn), stringsAsFactors = FALSE)
  }))
}
utils::write.csv(tab, file.path(out, "pilot_table.csv"), row.names = FALSE)

# ---------------------------------------------------------------------------------------------------------------- thread scaling
scal <- data.frame(); t1_full <- NA_real_
SS <- if (!is.null(logs) && file.exists(file.path(logs, "scaling", "scaling_subset.csv"))) utils::read.csv(file.path(logs, "scaling", "scaling_subset.csv"), stringsAsFactors = FALSE) else NULL
# RC2: the scaling rows must be the expected problem with full retained coverage, the declared fraction/task split, consistent task/model counts and ONE common task subset.
# EVERY row is checked (not just the first); nothing is extrapolated from rows that fail.
scaling_check <- function(S) {
  if (is.null(S)) return(list(ok = FALSE, absent = TRUE, why = "scaling/scaling_subset.csv missing"))
  need <- c("dataset", "threads", "rep", "fraction", "n_tasks", "tasks_run", "models_scored", "models_total", "wall_s", "tasks_sha256")
  m <- setdiff(need, names(S)); if (length(m)) return(list(ok = FALSE, absent = TRUE, why = paste("missing columns:", paste(m, collapse = ","))))
  tryCatch({
    r <- character()
    allv <- function(ok) length(ok) > 0L && !anyNA(ok) && all(ok)          # NA anywhere means the comparison fails (never an error)
    N <- lapply(S[c("threads", "rep", "fraction", "n_tasks", "tasks_run", "models_scored", "models_total", "wall_s")], num)
    bad_na <- names(N)[vapply(N, function(v) anyNA(v) || any(!is.finite(v)), NA)]
    if (length(bad_na) || anyNA(S$dataset) || anyNA(S$tasks_sha256)) r <- c(r, paste0("missing, NA or non-numeric values in: ", paste(c(bad_na, if (anyNA(S$dataset)) "dataset", if (anyNA(S$tasks_sha256)) "tasks_sha256"), collapse = ",")))
    if (nrow(S) != 4L || !allv(setequal(paste(N$threads, N$rep), c("1 1", "1 2", "8 1", "8 2")))) r <- c(r, "rows are not exactly threads 1 and 8 x repetitions 1 and 2")
    if (!allv(as.character(S$dataset) == "dev_p0030_S4_r001")) r <- c(r, "a row is not dev_p0030_S4_r001")
    if (!allv(N$models_total == 2^30)) r <- c(r, "models_total is not 2^30 in every row (full retained coverage)")
    if (!allv(N$n_tasks == 1024)) r <- c(r, "n_tasks is not 1024 in every row")
    if (!allv(abs(N$fraction - 0.03) < 1e-12)) r <- c(r, "fraction is not the declared 0.03 in every row")
    if (!allv(N$tasks_run == ceiling(0.03 * 1024))) r <- c(r, "tasks_run is not the declared split ceiling(0.03 x 1024) = 31 in every row")
    if (!allv(N$models_scored == N$tasks_run * N$models_total / N$n_tasks)) r <- c(r, "models_scored is not tasks_run x models_total / n_tasks in every row")
    h <- as.character(S$tasks_sha256)
    if (!allv(grepl("^[0-9a-f]{64}$", h))) r <- c(r, "tasks_sha256 is not a 64-hex digest in every row")
    else if (length(unique(h)) != 1L) r <- c(r, "the four rows did not run one common task subset (tasks_sha256 differs)")
    if (!allv(N$wall_s > 0)) r <- c(r, "wall_s is not finite and positive in every row")
    list(ok = !length(r), absent = FALSE, why = if (length(r)) paste(r, collapse = "; ") else "4 rows: dev_p0030_S4_r001, 2^30 models, 31 of 1,024 tasks, one common subset (64-hex digest)")
  }, error = function(e) list(ok = FALSE, absent = FALSE, why = paste("malformed scaling evidence:", conditionMessage(e))))
}
sc_res <- scaling_check(SS)
if (isTRUE(sc_res$ok)) {
  g <- aggregate(wall_s ~ threads, SS, mean); mt <- SS$models_total[1] / SS$models_scored[1]
  base1 <- g$wall_s[g$threads == 1]; if (length(base1)) t1_full <- base1 * mt
  scal <- rbind(scal, data.frame(source = "3% task subset", threads = g$threads, wall_s = g$wall_s, reps = as.integer(table(SS$threads)[as.character(g$threads)]),
                                 speedup_vs_1 = if (length(base1)) base1 / g$wall_s else NA, efficiency = if (length(base1)) base1 / g$wall_s / g$threads else NA, stringsAsFactors = FALSE))
}
fulls <- VAL[VAL$run %in% c("scale_t08", "scale_t16", "scale_t32") | (VAL$run == "enum30" & grepl("S4_r001$", VAL$unit)), , drop = FALSE]
if (nrow(fulls)) {
  fulls <- fulls[order(fulls$threads), ]
  scal <- rbind(scal, data.frame(source = ifelse(fulls$run == "enum30", "full (enum30 task)", "full enumeration"), threads = fulls$threads, wall_s = fulls$runtime_s, reps = 1L,
                                 speedup_vs_1 = if (is.finite(t1_full)) t1_full / fulls$runtime_s else NA, efficiency = if (is.finite(t1_full)) t1_full / fulls$runtime_s / fulls$threads else NA, stringsAsFactors = FALSE))
}
utils::write.csv(scal, file.path(out, "pilot_scaling.csv"), row.names = FALSE)

# ---------------------------------------------------------------------------------------------------------------- verdicts
V <- list(); addv <- function(item, verdict, detail) V[[length(V) + 1L]] <<- data.frame(item = item, verdict = verdict, detail = detail, stringsAsFactors = FALSE)
# V1 launch receipt
need_launch <- c("launch/pilot.env", "launch/pilot.env.sha256", "launch/effective_env.txt", "launch/guard_receipt_submit.txt", "launch/sbatch_args.tsv", "launch/STAGED_SHA256.txt")
if (is.null(logs)) addv("Launch receipt (final pilot.env, hashes, guard receipt, sbatch vectors, effective environment)", "INCOMPLETE", "no log folder") else {
  miss <- need_launch[!file.exists(file.path(logs, need_launch))]
  if (length(miss)) addv("Launch receipt (final pilot.env, hashes, guard receipt, sbatch vectors, effective environment)", "INCOMPLETE", paste("missing:", paste(miss, collapse = ", ")))
  else {
    probs <- character()
    sh <- rd_lines(file.path(logs, "launch/pilot.env.sha256"))[1]
    if (!identical(tolower(sub("^([0-9a-f]{64}).*$", "\\1", sh)), sha(file.path(logs, "launch/pilot.env")))) probs <- c(probs, "pilot.env hash differs from its record")
    ee <- rd_lines(file.path(logs, "launch/effective_env.txt"))
    if (any(grepl("^MODULES=\\[\\]", ee)) || any(grepl("^MODULES_BENCH=\\[\\]", ee))) probs <- c(probs, "MODULES empty in the recorded environment")
    if (any(grepl("^PILOT_(DRYRUN|SKIP_MODULES|LIMIT|BENCH_METHODS|BENCH_EXTRA|TIME_BIN)=\\[.+\\]", ee))) probs <- c(probs, "a test hook was set at submission")
    if (!any(grepl("^GUARD_CHECK_OK", rd_lines(file.path(logs, "launch/guard_receipt_submit.txt"))))) probs <- c(probs, "guard receipt does not show GUARD_CHECK_OK")
    if (length(rd_lines(file.path(logs, "launch/sbatch_args.tsv"))) != 12L) probs <- c(probs, "sbatch_args.tsv does not have 12 submissions")
    addv("Launch receipt (final pilot.env, hashes, guard receipt, sbatch vectors, effective environment)", if (length(probs)) "FAIL" else "PASS", if (length(probs)) paste(probs, collapse = "; ") else "pilot.env hash, 12 sbatch vectors, guard receipt with the D7 limits, no test hook")
  }
}
# V2 P0 regeneration
l <- rdl("p0_verify/NOTS_REGEN_REPORT.md"); tv <- trow("verify", "nots_regen")
if (is.null(l)) addv("P0 regeneration on NOTS (lowp_verify_nots.R: exit 0 PASS / 1 MISMATCH / 3 INCOMPLETE)", "INCOMPLETE", "no NOTS_REGEN_REPORT.md") else {
  v <- if (any(grepl("^\\*\\*PASS\\*\\*", l))) "PASS" else if (any(grepl("^\\*\\*MISMATCH\\*\\*", l))) "FAIL" else "INCOMPLETE"
  det <- gsub("\\*", "", paste(stats::na.omit(c(grep("^\\*\\*(PASS|MISMATCH|INCOMPLETE)\\*\\*", l, value = TRUE)[1], grep("^- ", l, value = TRUE)[1:2])), collapse = " "))
  if (v == "PASS" && !(nrow(tv) == 1L && isTRUE(num(tv$rc) == 0))) { v <- "FAIL"; det <- paste(det, "(timing rc is not 0)") }
  if (v == "PASS" && !any(grepl("1200 production and 60 dev", l))) { v <- "FAIL"; det <- paste(det, "(report does not show 1,200 + 60 rows)") }
  addv("P0 regeneration on NOTS (lowp_verify_nots.R: exit 0 PASS / 1 MISMATCH / 3 INCOMPLETE)", if (v == "INCOMPLETE") "INCOMPLETE (STOP)" else if (v == "FAIL") "FAIL (STOP)" else "PASS", det)
}
# V3 truth lock: permission test, wave lock, wave unlock
fs <- rdl("truthlock/evidence/final_status.txt"); rl <- rdl("truthlock/evidence/run.log")
if (is.null(fs) || is.null(rl)) addv("P0 truth-lock test (ordinary user, production + dev truth; evidence final_status.txt)", "INCOMPLETE", "truthlock/evidence/final_status.txt or run.log missing") else {
  fes <- sub("^final_exit_status ", "", grep("^final_exit_status", fs, value = TRUE)); fl <- sub("^failed ", "", grep("^failed ", fs, value = TRUE)); ck <- sub("^checks ", "", grep("^checks ", fs, value = TRUE))
  aft <- rdl("truthlock/TRUTHLOCK_AFTER.txt"); rest <- !is.null(aft) && any(grepl("truth 755 dev/truth 755; dirs not 755: 0; files not 444: 0", aft, fixed = TRUE))
  ok <- identical(fes, "0") && identical(fl, "0") && isTRUE(num(ck) > 0) && rest
  addv("P0 truth-lock test (ordinary user, production + dev truth; evidence final_status.txt)", if (ok) "PASS" else "FAIL",
       sprintf("FINAL_EXIT_STATUS %s, %s checks, %s failed; trees after the test %s", fes, ck, fl, if (rest) "755/444" else "NOT confirmed 755/444"))
}
wl <- rdl("truthlock/WAVE_LOCK.txt"); wu <- rdl("truthlock/WAVE_UNLOCK.txt")
if (is.null(wl)) addv("Wave lock: both truth trees mode 000 and verified before any fit", "INCOMPLETE", "truthlock/WAVE_LOCK.txt missing") else addv("Wave lock: both truth trees mode 000 and verified before any fit", if (any(grepl("^WAVE_LOCK_VERIFIED", wl))) "PASS" else "FAIL", paste(grep("^LOCK_STATE|^WAVE_LOCK", wl, value = TRUE)[1:2], collapse = " | "))
if (is.null(wu)) addv("Wave unlock: trees restored to 755/444 after the last fitting job, hashes unchanged", "INCOMPLETE", "truthlock/WAVE_UNLOCK.txt missing") else addv("Wave unlock: trees restored to 755/444 after the last fitting job, hashes unchanged", if (any(grepl("^WAVE_UNLOCK_VERIFIED.*sha=equal", wu))) "PASS" else "FAIL", paste(grep("^OPEN_STATE|^SHA256|^WAVE_UNLOCK", wu, value = TRUE), collapse = " | "))
# V4 score and aggregate checks
l <- rdl("bitid/BITID_REPORT.md"); bc <- if (!is.null(logs) && file.exists(file.path(logs, "bitid/bitid_results.csv"))) utils::read.csv(file.path(logs, "bitid/bitid_results.csv"), stringsAsFactors = FALSE) else NULL
if (is.null(l) || is.null(bc)) addv("Enumerator vs scorer: bytes for scores, tolerance for aggregates, exact decisions, thread invariance", "INCOMPLETE", "BITID_REPORT.md or bitid_results.csv missing") else {
  have <- vapply(paste0("T", 1:5), function(t) any(startsWith(bc$check, t)), NA)
  ok <- any(grepl("VERDICT: PASS", l)) && all(as.logical(bc$pass)) && all(have) && sum(bc$byte_mismatches[grepl("^T[23]", bc$check)]) == 0
  addv("Enumerator vs scorer: bytes for scores, tolerance for aggregates, exact decisions, thread invariance", if (!all(have)) "INCOMPLETE" else if (ok) "PASS" else "FAIL",
       sprintf("%d rows, %d pass; checks present: %s; byte mismatches in T2/T3: %d", nrow(bc), sum(as.logical(bc$pass)), paste(names(have)[have], collapse = ","), sum(bc$byte_mismatches[grepl("^T[23]", bc$check)])))
}
# V5 unit sets
cnt <- function(sel) c(valid = sum(UN$valid & sel), present = sum(sel & !UN$absent), expected = sum(sel))
rows <- list(enum20 = UN$run == "enum20", enum30 = UN$run == "enum30", scaling = UN$arm == "scale", smc_primary = UN$arm == "smc", smc_repeat = UN$arm == "smc_rep", benchmarks = UN$run == "bench")
cn <- t(vapply(rows, cnt, c(valid = 0, present = 0, expected = 0)))
want <- c(enum20 = 30, enum30 = 6, scaling = 3, smc_primary = 24, smc_repeat = 4, benchmarks = 192)
exact_ok <- all(cn[, "expected"] == want[rownames(cn)])
allvalid <- all(cn[, "valid"] == cn[, "expected"])
addv("Exact unit sets valid (30 enum20, 6 enum30, 3 scaling, 24 SMC, 4 repeats, 192 benchmark units)", if (allvalid && exact_ok && !length(dir_extra)) "PASS" else if (all(cn[, "present"] == cn[, "expected"]) && length(dir_extra) == 0 && any(!UN$valid & !UN$absent)) "FAIL" else "INCOMPLETE",
     paste0(paste(sprintf("%s %d/%d", rownames(cn), cn[, "valid"], cn[, "expected"]), collapse = "; "), if (length(dir_extra)) paste0("; UNEXPECTED units: ", paste(head(dir_extra, 5), collapse = ", ")) else ""))
bad <- UN[!UN$valid, ]
if (nrow(bad)) { bf <- bad[1:min(nrow(bad), 8), c("run", "unit", "why")]; addv("Invalid or missing units (first 8; all in pilot_units.csv)", if (any(!bad$absent)) "FAIL" else "INCOMPLETE", paste(sprintf("%s %s: %s", bf$run, bf$unit, bf$why), collapse = " || ")) }
# V6 execution of the non-unit steps
steps <- rbind(c("build", "compile"), c("verify", "nots_regen"), c("truthlock", "test"), c("lock", "apply"), c("unlock", "apply"), c("bitid", "all"),
               c("scale", "subset_t1_rep1"), c("scale", "subset_t8_rep1"), c("scale", "subset_t1_rep2"), c("scale", "subset_t8_rep2"))
sv <- vapply(seq_len(nrow(steps)), function(i) { t <- trow(steps[i, 1], steps[i, 2]); if (nrow(t) != 1L) NA else isTRUE(num(t$rc) == 0) }, NA)
addv("Step commands executed with exit status 0 (build, verify, truth test, wave lock/unlock, bit identity, scaling subsets)", if (any(!sv, na.rm = TRUE)) "FAIL" else if (anyNA(sv)) "INCOMPLETE" else "PASS",
     sprintf("%d of %d timing rows with rc 0%s", sum(sv, na.rm = TRUE), length(sv), if (anyNA(sv)) paste0("; absent: ", paste(paste(steps[is.na(sv), 1], steps[is.na(sv), 2]), collapse = ", ")) else ""))
# V7 enumeration properties
ev <- exact_objs
if (length(ev)) {
  inv <- ev[grepl("^scale_t|^enum30 dev_p0030_S4_r001$", names(ev))]
  if (length(inv) == 4L) { ref <- inv[[1]]$scales; same <- vapply(inv, function(z) identical(z$scales, ref), NA)
    addv("Thread invariance: dev_p0030_S4_r001 outputs identical at 8, 16, 16, 32 threads", if (all(same)) "PASS" else "FAIL", paste(ifelse(same, "identical", "DIFFERENT"), collapse = ", ")) }
  else addv("Thread invariance: dev_p0030_S4_r001 outputs identical at 8, 16, 16, 32 threads", "INCOMPLETE", sprintf("%d of 4 valid outputs", length(inv)))
} else addv("Thread invariance: dev_p0030_S4_r001 outputs identical at 8, 16, 16, 32 threads", "INCOMPLETE", "no valid enumeration")
# V8 SMC repeats
reps <- smc_seed[vapply(smc_seed, function(z) z$rep > 0L, NA)]; prim <- smc_seed[vapply(smc_seed, function(z) z$rep == 0L, NA)]
pairs <- do.call(rbind, lapply(reps, function(r) { p0 <- prim[[paste0(sub(" ", "_", r$ds), "")]]; if (is.null(p0)) NULL else data.frame(case = r$ds, seed_primary = p0$seed, seed_repeat = r$seed, dlogZ = r$logZ - p0$logZ, same_hpm = identical(r$hpm, p0$hpm), stringsAsFactors = FALSE) }))
if (!is.null(pairs) && nrow(pairs) == 4L) {
  ok <- all(pairs$seed_repeat == pairs$seed_primary + 1000)
  utils::write.csv(pairs, file.path(out, "pilot_repeat_vs_primary.csv"), row.names = FALSE)
  addv("SMC repeat fits: valid, seed = primary + 1,000, Monte Carlo spread vs the primary fit", if (ok) "PASS" else "FAIL", sprintf("%d pairs; |dlogZ| median %.3f max %.3f; same HPM %d of %d", nrow(pairs), median(abs(pairs$dlogZ)), max(abs(pairs$dlogZ)), sum(pairs$same_hpm), nrow(pairs)))
} else addv("SMC repeat fits: valid, seed = primary + 1,000, Monte Carlo spread vs the primary fit", "INCOMPLETE", sprintf("%d of 4 valid repeat/primary pairs", if (is.null(pairs)) 0L else nrow(pairs)))
# V9 fit statuses (warnings accepted but flagged)
nw <- sum(UN$warn)
addv("Fit statuses: no failed, timeout or unknown rule row (a captured R warning is accepted and counted)", if (any(grepl("rule status", UN$why))) "FAIL" else if (nw > 0) "WARN" else "PASS", sprintf("%d valid units carry status 'warning'", nw))
# V10 scheduler
steps_exp <- data.frame(step = c("s0_build", "s0_verify", "s0_truthlock", "s0_lock", "s1_enum20", "s1_enum30", "s1_scale", "s1_bitid", "s2_smc", "s3_bench", "s8_unlock", "s9_collect"),
                        n = c(1, 1, 1, 1, 1, 6, 1, 1, 28, 24, 1, 1), stringsAsFactors = FALSE)
if (is.null(jobids) || is.null(sacct)) addv("Slurm: every job and array task COMPLETED with exit 0:0 (terminal snapshot)", "INCOMPLETE", "jobids.tsv or accounting snapshot missing") else {
  probs <- character(); miss <- character()
  for (k in seq_len(nrow(steps_exp))) {
    jr <- jobids[jobids$step == steps_exp$step[k], ]
    if (nrow(jr) != 1L) { miss <- c(miss, paste(steps_exp$step[k], "not recorded")); next }
    keys <- if (steps_exp$n[k] == 1L && jr$array == "-") jr$jobid else paste0(jr$jobid, "_", seq_len(steps_exp$n[k]) - 1L)
    for (key in keys) { r <- sacct[sacct$JobID == key, , drop = FALSE]
      if (!nrow(r)) miss <- c(miss, paste(steps_exp$step[k], key, "no accounting row"))
      else if (r$State[1] != "COMPLETED" || r$ExitCode[1] != "0:0") probs <- c(probs, sprintf("%s %s %s %s", steps_exp$step[k], key, r$State[1], r$ExitCode[1])) }
  }
  coll_row <- !is.null(sacct_final)
  v <- if (length(probs)) "FAIL" else if (length(miss) || !coll_row) "INCOMPLETE" else "PASS"
  addv("Slurm: every job and array task COMPLETED with exit 0:0 (terminal snapshot)", v,
       paste0(if (length(probs)) paste0("not completed: ", paste(head(probs, 6), collapse = "; "), ". ") else "", if (length(miss)) paste0("no row: ", paste(head(miss, 6), collapse = "; "), ". ") else "",
if (v == "PASS") sprintf("all %d steps and %d jobs/array tasks", nrow(steps_exp), sum(steps_exp$n)) else ""))
}
# V11 memory evidence for sizing
if (nrow(tab)) { nomem <- tab[!(is.finite(tab$peak_mem_max_mb) & tab$peak_mem_max_mb > 0), c("arm", "p")]
  addv("Memory evidence for every arm and p used in sizing (GNU time, else sacct job-level bound, else core VmHWM)", if (nrow(nomem)) "INCOMPLETE" else "PASS",
       if (nrow(nomem)) paste("no memory figure for:", paste(paste(nomem$arm, nomem$p), collapse = ", ")) else paste("sources:", paste(sort(unique(unlist(strsplit(tab$mem_source, "[+]")))), collapse = ", "))) } else addv("Memory evidence for every arm and p used in sizing (GNU time, else sacct job-level bound, else core VmHWM)", "INCOMPLETE", "no valid unit")
# V12 wall-time evidence: every arm and p used in sizing needs process wall times from the unit timing rows
if (nrow(tab)) { nowall <- tab[!is.finite(tab$wall_med_s), c("arm", "p")]
  addv("Wall-time evidence for every arm and p used in sizing (unit timing rows; no fallback to in-process time)", if (nrow(nowall)) "INCOMPLETE" else "PASS",
       if (nrow(nowall)) paste("no wall time for:", paste(paste(nowall$arm, nowall$p), collapse = ", ")) else "all arms and p have process wall times") } else addv("Wall-time evidence for every arm and p used in sizing (unit timing rows; no fallback to in-process time)", "INCOMPLETE", "no valid unit")
# V13 thread-scaling measurements: the saved file with the four expected subset rows
addv("Thread-scaling subset measurements: expected problem, full coverage, declared split, one common subset (every row checked)", if (isTRUE(sc_res$ok)) "PASS" else if (isTRUE(sc_res$absent)) "INCOMPLETE" else "FAIL", sc_res$why)
# V14 P5 scan (DECISIONS D11), v2.2.1 tools/p5_scan.R over the pilot's SMC result folder. INFORMATIVE ONLY: no existing gate is touched. The pilot allocation
# (2 GB / 4 h inside a 4 h Slurm wall) leaves no room for an in-task P5 retry, so no retry is run automatically: any `eligible` unit (primary ended native
# resource_limit, no valid P5_retry record) is a finding for HQ, which decides. (A resource_limit unit is also invalid under the SMC native-status check above.)
v221_dir <- opt("v221-dir", file.path(here, "..", "..", "core", "v2_2_1"))
rscript_bin <- opt("rscript", file.path(R.home("bin"), if (.Platform$OS.type == "windows") "Rscript.exe" else "Rscript"))
p5_tsv <- file.path(out, "pilot_p5_scan.tsv"); p5 <- list(ran = FALSE, units = NA_integer_, rl = NA_integer_, el = NA_integer_, line = "", why = "")
scan_r <- file.path(v221_dir, "tools", "p5_scan.R")
if (file.exists(p5_tsv)) unlink(p5_tsv)
if (is.null(run_dir[["smc"]])) { p5$why <- "no _smc results folder was supplied"
} else if (!file.exists(scan_r)) { p5$why <- paste("tools/p5_scan.R not found under", v221_dir)
} else {
  o <- tryCatch(suppressWarnings(system2(rscript_bin, c(shQuote(normalizePath(scan_r, winslash = "/")), "--run-dir", shQuote(normalizePath(run_dir[["smc"]], winslash = "/")),
                                                       "--out", shQuote(file.path(normalizePath(out, winslash = "/", mustWork = FALSE), "pilot_p5_scan.tsv"))), stdout = TRUE, stderr = TRUE)),
                error = function(e) structure(conditionMessage(e), status = 127L))
  st <- attr(o, "status") %||% 0L; ln <- grep("^p5_scan units=", o, value = TRUE)
  if (!identical(as.integer(st), 0L) || length(ln) != 1L || !file.exists(p5_tsv)) p5$why <- paste0("p5_scan failed (status ", st, "): ", paste(utils::tail(o, 3), collapse = " / "))
  else {
    g <- function(k) as.integer(sub(paste0(".*", k, "=([0-9]+).*"), "\\1", ln))
    p5 <- list(ran = TRUE, units = g("units"), rl = g("primary_resource_limit"), el = g("eligible"), line = ln, why = "")
  }
}
if (!p5$ran) { addv("P5 scan of the SMC results (DECISIONS D11; informative, no gate)", "WARN", paste0("scan NOT run: ", p5$why, ". Run `Rscript <v2_2_1>/tools/p5_scan.R --run-dir <results>/<PID>_smc --out <file.tsv>` by hand and report primary_resource_limit and eligible to HQ"))
} else { addv("P5 scan of the SMC results (DECISIONS D11; informative, no gate)", if (p5$rl > 0L || p5$el > 0L) "WARN" else "PASS",
          sprintf("%d SMC units scanned: primary_resource_limit = %d, eligible = %d.%s", p5$units, p5$rl, p5$el,
                  if (p5$rl > 0L || p5$el > 0L) " FINDING FOR HQ: P5 retries are not run automatically at the pilot; HQ decides (pilot_p5_scan.tsv lists the units)." else ""))
}
Vd <- do.call(rbind, V)
verd <- sub(" \\(STOP\\)", "", Vd$verdict)
overall <- if (any(verd == "FAIL")) "FAIL" else if (any(verd == "INCOMPLETE")) "INCOMPLETE" else if (any(verd == "WARN")) "WARN" else "PASS"
utils::write.csv(rbind(data.frame(item = "OVERALL", verdict = overall, detail = ""), Vd), file.path(out, "pilot_verdicts.csv"), row.names = FALSE)

# ---------------------------------------------------------------------------------------------------------------- projection (RUN_DESIGN section 3 layout), valid units only
gst <- function(arm, p, col, f) { s <- T0[T0$arm == arm & T0$p == p, ]; if (!nrow(s)) NA_real_ else f(s[[col]]) }
unit_wall <- function(arm, p, f) gst(arm, p, "wall_s", f)    # NO fallback to the in-process time: a missing wall measurement is a verdict (INCOMPLETE), never silently replaced
pieces <- list(
  list(piece = "enum30", p = 30, tasks = 24, per_task = 25, units = 600, cpus = 16, arms = "enum"),
  list(piece = "enum20", p = 20, tasks = 1, per_task = 600, units = 600, cpus = 4, arms = "enum"),
  list(piece = "smc p=20", p = 20, tasks = 48, per_task = 25, units = 1200, cpus = 1, arms = "smc"), list(piece = "smc p=30", p = 30, tasks = 48, per_task = 25, units = 1200, cpus = 1, arms = "smc"),
  list(piece = "smcrep p=20", p = 20, tasks = 60, per_task = 20, units = 1200, cpus = 1, arms = "smc"), list(piece = "smcrep p=30", p = 30, tasks = 60, per_task = 20, units = 1200, cpus = 1, arms = "smc"),
  list(piece = "bench p=20", p = 20, tasks = 48, per_task = 25, units = 1200, cpus = 1, arms = METHODS), list(piece = "bench p=30", p = 30, tasks = 48, per_task = 25, units = 1200, cpus = 1, arms = METHODS))
proj <- do.call(rbind, lapply(pieces, function(pc) {
  # enum rows of the right p and thread count only (enum20 = 4 threads, enum30 = 16 threads)
  uw_mean <- sum(vapply(pc$arms, function(a) unit_wall(a, pc$p, mn), 0)); uw_p90 <- sum(vapply(pc$arms, function(a) unit_wall(a, pc$p, q90), 0))
  mems <- vapply(pc$arms, function(a) gst(a, pc$p, "maxrss_mb", mx), 0); mem <- if (any(is.finite(mems) & mems > 0)) max(mems[is.finite(mems) & mems > 0]) else NA_real_
  sz <- sum(vapply(pc$arms, function(a) gst(a, pc$p, "size_kb", mn), 0))
  esc <- sum(vapply(pc$arms, function(a) { v <- gst(a, pc$p, "escalated", function(x) sum(x, na.rm = TRUE)); if (is.na(v)) 0 else v }, 0))
  tw <- pc$per_task * uw_mean; tw90 <- pc$per_task * uw_p90
  data.frame(piece = pc$piece, tasks = pc$tasks, units_per_task = pc$per_task, cpus_per_task = pc$cpus, unit_wall_mean_s = uw_mean, unit_wall_p90_s = uw_p90,
             task_wall_expected = hms(tw), task_wall_conservative = hms(tw90), suggested_time_request = hms(ceiling(1.5 * tw90 / 900) * 900 + 900),
             suggested_mem_request_mb = if (is.finite(mem) && mem > 0) ceiling(1.5 * mem / 512) * 512 else NA, core_hours = pc$tasks * tw * pc$cpus / 3600,
             scratch_gb = pc$units * sz / 1024 / 1024, pilot_escalations = esc, stringsAsFactors = FALSE)
}))
projT <- rbind(proj, data.frame(piece = "TOTAL", tasks = sum(proj$tasks), units_per_task = NA, cpus_per_task = NA, unit_wall_mean_s = NA, unit_wall_p90_s = NA, task_wall_expected = NA,
                                task_wall_conservative = NA, suggested_time_request = NA, suggested_mem_request_mb = NA, core_hours = sum(proj$core_hours, na.rm = TRUE),
                                scratch_gb = sum(proj$scratch_gb, na.rm = TRUE), pilot_escalations = NA, stringsAsFactors = FALSE))
accepted <- overall %in% c("PASS", "WARN")
projT$status <- ifelse(accepted & stats::complete.cases(projT[, c("unit_wall_mean_s", "core_hours", "suggested_mem_request_mb")]) & (is.na(projT$suggested_mem_request_mb) | projT$suggested_mem_request_mb > 0) | (projT$piece == "TOTAL" & accepted), "accepted", "NOT ACCEPTED (required evidence absent, invalid or failed)")
utils::write.csv(projT, file.path(out, "pilot_projection.csv"), row.names = FALSE)
if (nrow(tab)) { tab$accepted <- accepted; utils::write.csv(tab, file.path(out, "pilot_table.csv"), row.names = FALSE) }

# ---------------------------------------------------------------------------------------------------------------- sample coverage (what the fit-time sample is, and is not)
cov <- data.frame(arm = c("Exact enumeration p = 20", "Exact enumeration p = 30", "SMC-BVS primary", "SMC-BVS repeat", "Benchmarks (8 methods)", "Regeneration check (not timing)"),
                  datasets = c(length(enum20_ids), length(enum30_ids), length(unique(smc_cases$dataset[smc_cases$repeat. == 0])), length(unique(smc_cases$dataset[smc_cases$repeat. > 0])), length(unique(bench_cases$dataset)), 60),
                  what = c("S1..S6 x r1..r5 at p = 20 (both scales in one pass)", "S1..S6, r1 only, at p = 30", "p in {20,30} x S1..S6, r1 only, c100 and c050 (24 fits)",
                           "4 of those cases, repeat 1 (seed + 1,000)", "the same 24 cases, one fit per method", "all 60 dev manifest rows regenerated and hashed; gives no fit-time measurement"),
                  stringsAsFactors = FALSE)

# ---------------------------------------------------------------------------------------------------------------- markdown
pretty_arm <- c(enum = "Exact enumeration (both scales, one pass)", smc = "SMC-BVS v2.2.1, primary seed", smc_rep = "SMC-BVS v2.2.1, repeat seed", F1 = "F1 Lasso", F2 = "F2 Elastic net",
                F3 = "F3 Adaptive lasso", F4 = "F4 MCP", F5 = "F5 ABESS", A1 = "A1 SuSiE", A2 = "A2 SSL", A3 = "A3 Horseshoe")
ptab <- if (nrow(tab)) { x <- tab; x$arm <- pretty_arm[x$arm]; x[, c("arm", "p", "threads", "n_valid", "n_expected", "run_med_s", "run_p90_s", "run_max_s", "wall_med_s", "wall_max_s", "peak_mem_max_mb", "mem_source", "size_mean_kb", "escalations", "warnings")] } else tab
if (nrow(ptab)) names(ptab) <- c("Arm", "p", "Threads", "Valid", "Expected", "In-process median s", "90th s", "Max s", "Wall median s (incl. start-up)", "Wall max s", "Peak RSS MB (max)", "Memory source", "Output KB / unit", "Escalations", "Warnings")
sacct_txt <- character()
if (!is.null(sacct)) { top <- sacct[!grepl("\\.", sacct$JobID), ]; top$job <- sub("_.*", "", top$JobID); st <- aggregate(JobID ~ JobName + State, top, length); names(st)[3] <- "rows"
  sacct_txt <- c("### Slurm accounting", "", sprintf("Snapshot: %s.", if (!is.null(sacct_final)) "sacct_final.tsv (terminal, incl. the collector)" else "sacct_collector.tsv ONLY (the collector's own row is absent: run final_accounting.sh)"), "", md_table(st), "") }
L <- c(sprintf("# LOWP pilot summary: OVERALL %s", overall), "",
       sprintf("Generated %s UTC by `pilot/summarize_pilot.R`%s. %s", format(Sys.time(), tz = "UTC", "%Y-%m-%d %H:%M"), if (nzchar(label)) paste0(" ", label) else "",
               if (overall %in% c("PASS", "WARN")) "All required evidence is present and valid." else "**This summary is labelled INCOMPLETE or FAILED: do not use it to size production.** Tables below are descriptive and use only valid units."),
       "", "Dev datasets only (excluded from all counts); every arm ran on the real dev ids through the production CLIs with `--development`.", "",
       "## Verdicts", "", md_table(Vd), "", "## Unit sets", "", md_table(data.frame(set = rownames(cn), valid = cn[, "valid"], present = cn[, "present"], expected = cn[, "expected"])), "",
       "## Cost per unit, by arm and p (valid units only)", "",
       "Policy: every required unit needs a finite positive process wall time (missing: INCOMPLETE, zero or negative: invalid); enumeration units also need observed CPU time user+sys (absence: INCOMPLETE), single-thread units are costed as wall x 1 CPU. In-process = `runtime_s` of the runner; wall = whole process (start-up, cache load, fit) from GNU time; peak RSS from GNU time, else the batch-step MaxRSS of the job (**a job-level conservative bound**, for jobs that run several units it covers all of them), else the core's VmHWM.", "",
       md_table(ptab), "", "## Thread scaling of the enumerator (dev_p0030_S4_r001)", "",
       if (nrow(scal)) c(sprintf("Single-thread full-run time extrapolated from the 3%% subset: %s s.", fmt(t1_full)), "", md_table(scal)) else "(not available)", "",
       if (accepted) "## Projected production cost (RUN_DESIGN section 3 layout): accepted" else "## Projected production cost (RUN_DESIGN section 3 layout): **NOT ACCEPTED, do not use for sizing** (required evidence is absent, invalid or failed)", "",
       "Per-task wall = units per task x mean unit wall (expected) or x 90th-percentile unit wall (conservative); time request = 1.5 x conservative + 15 min rounded to 15 min; memory request = 1.5 x the largest pilot peak RSS, rounded up to 512 MB; core-hours = allocated CPUs x expected wall; scratch = units x mean pilot output size. Failed or missing pilot units are excluded.", "",
       md_table(projT), "", "## Sample coverage and its limits", "", md_table(cov), "",
       "Timing and memory come from these subsets only: p = 30 enumeration and all SMC/benchmark timings use replicate 1 of six scenarios; production extrapolation assumes that replicates within a cell cost alike and that rare SMC escalations are absent from 28 fits. Keep a margin. The 60-row regeneration check proves the generator, not fit cost.", "")
if (length(sacct_txt)) L <- c(L, sacct_txt)
dsk <- rdl("accounting/disk_after.txt"); if (!is.null(dsk)) L <- c(L, "## Disk after the pilot", "", "```", dsk, "```", "")
if (any(!UN$valid)) L <- c(L, "## Units that are not valid", "", md_table(UN[!UN$valid, c("run", "unit", "why")][seq_len(min(sum(!UN$valid), 60)), ]), "")
esc <- UN[which(UN$valid & UN$escalated %in% TRUE), c("arm", "p", "unit", "runtime_s")]
p5_txt <- if (!p5$ran) c(sprintf("**The P5 scan was NOT run:** %s.", p5$why), "") else {
  tb <- tryCatch(utils::read.delim(p5_tsv, stringsAsFactors = FALSE, colClasses = "character"), error = function(e) data.frame())
  c(sprintf("`%s`", p5$line), "",
    sprintf("`primary_resource_limit` = **%d**, `eligible` = **%d** (SMC units scanned: %d). Full table: `pilot_p5_scan.tsv`.", p5$rl, p5$el, p5$units), "",
    if (p5$rl > 0L || p5$el > 0L) c("**FINDING FOR HQ.** Pilot SMC fits use 2 GB / 4 h inside a 4 h Slurm wall, so an in-task P5 retry (double allocation) is impossible and no retry is run automatically: HQ decides what to do with each eligible unit.", "",
                                    if (nrow(tb) && "eligible" %in% names(tb)) md_table(tb[tb$eligible %in% "TRUE" | tb$primary_v3_status %in% "resource_limit", intersect(c("case_id", "base", "primary_v3_status", "primary_stop_phase", "primary_stop_where", "primary_stop_checkpoint", "retry_state", "eligible"), names(tb)), drop = FALSE]) else NULL, "")
    else c("No SMC unit ended `resource_limit`: nothing for HQ to decide under P5.", ""))
}
L <- c(L, "## P5 scan of the SMC results (DECISIONS D11)", "", "Informative: not an acceptance gate. Produced by `core/v2_2_1/tools/p5_scan.R` over the SMC result folder.", "", p5_txt)
L <- c(L, "## SMC escalations", "", if (nrow(esc)) md_table(esc) else "None among the valid pilot fits.", "",
       "Files: `pilot_table.csv`, `pilot_units.csv`, `pilot_scaling.csv`, `pilot_projection.csv`, `pilot_verdicts.csv`, `pilot_repeat_vs_primary.csv`, `pilot_p5_scan.tsv`.")
writeLines(L, file.path(out, "PILOT_SUMMARY.md"))
cat(sprintf("OVERALL %s: wrote %s (%d expected units, %d valid; %d verdicts)\n", overall, file.path(out, "PILOT_SUMMARY.md"), nrow(UN), sum(UN$valid), nrow(Vd)))
quit(save = "no", status = switch(overall, PASS = 0L, WARN = 0L, FAIL = 2L, INCOMPLETE = 3L))
