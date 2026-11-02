#!/usr/bin/env Rscript
# run_enum_dataset.R -- exact enumeration of one low-p dataset, both scales (c100, c050) in one pass; writes
#   OUTROOT/results/RUN_ID/p{pppp}/{dataset_id}/EXACT.{rds,sha256,done}   (INTERFACES §I2)
# Usage:
#   Rscript run_enum_dataset.R --dataset p0030_S4_r050 --study STUDYROOT --outroot OUT --run-id RID --threads T
#           [--core-dir CORE] [--scales c100,c050] [--force] [--development] [--unsealed-test-input]
# --development (as run_smc_case.R): ids dev_pPPPP_S*_r* are accepted only with it, prod ids only without it; pass --study <root>/dev.
# Inputs: only STUDY/inputs/p{pppp}/{dataset_id}.rds (X, Y); never the truth folder.  The inputs manifest
# STUDY/manifests/inputs_manifest_lowp.csv is REQUIRED and must hold exactly one row for the dataset whose file_sha256 equals
# the file's SHA-256.  --unsealed-test-input (tests only; not allowed with --development) permits a missing manifest; the
# output then records input_mode = "unsealed_test" and manifest_checked = FALSE.
#
# Completion protocol (crash safe; `.done` means "RDS and sidecar are complete and verified"):
#   * a skip happens only if EXACT.done, EXACT.sha256 and EXACT.rds exist and agree (marker hash = sidecar hash = SHA-256 of the RDS) and
#     the RDS meets the whole requested contract: this dataset and input bytes, the current source fingerprint (enum + vendored headers +
#     core scorer headers + preprocessing), exactly the requested scale set, all required fields, status exact / complete, full model
#     coverage, normalised size masses and the heuristic labels; otherwise the job says why and recomputes;
#   * publishing happens under a per-destination lock (directory `.lock`, stale after 10 minutes): remove any old `.done`, stage and
#     verify the new RDS and sidecar under temporary names, rename them in, re-verify the committed pair, and only then write `.done`;
#   * a job that cannot take the lock exits with status 3.
# Test-only failure injection: env LOWP_ENUM_FAIL_AT in {before_rds_rename, after_rds_rename, after_sha_rename, before_done}.

args <- commandArgs(trailingOnly = TRUE)
opt <- function(name, default = NULL) { i <- match(paste0("--", name), args); if (is.na(i)) default else args[i + 1] }
flag <- function(name) paste0("--", name) %in% args
dataset <- opt("dataset"); study <- opt("study"); outroot <- opt("outroot"); rid <- opt("run-id")
threads <- opt("threads", "1"); core_dir <- opt("core-dir", NULL); scales <- strsplit(opt("scales", "c100,c050"), ",")[[1]]
if (is.null(dataset) || is.null(study) || is.null(outroot) || is.null(rid))
  stop("usage: run_enum_dataset.R --dataset ID --study STUDYROOT --outroot OUT --run-id RID --threads T [--core-dir CORE] [--force] [--development] [--unsealed-test-input]")
if (!grepl("^[0-9]+$", threads) || as.integer(threads) < 1 || as.integer(threads) > 1024) stop("--threads must be an integer in 1..1024")
threads <- as.integer(threads)
if (!grepl("^[A-Za-z0-9_.-]+$", rid)) stop("--run-id may contain only letters, digits, '_', '.' and '-'")
if (!grepl("^(dev_)?p(0020|0030)_S[1-6]_r[0-9]{3}$", dataset)) stop("bad dataset id: ", dataset)
is_dev <- startsWith(dataset, "dev_")
if (is_dev != flag("development")) stop("development switch and dev_ prefix must agree (dev ids need --development; prod ids must not have it)")
unsealed <- flag("unsealed-test-input")
if (unsealed && is_dev) stop("--unsealed-test-input is not allowed with --development")

script_dir <- local({
  a <- commandArgs(FALSE); f <- sub("^--file=", "", a[grep("^--file=", a)])
  if (length(f)) dirname(normalizePath(f[1], winslash = "/")) else Sys.getenv("LOWP_ENUM_DIR", unset = ".")
})
Sys.setenv(LOWP_ENUM_DIR = script_dir)
source(file.path(script_dir, "lowp_enum.R"))
source(file.path(script_dir, "exact_contract.R"))   # lowp_validate_exact: the one strict I2 validator

pdir <- sub("^(dev_)?(p[0-9]{4})_.*$", "\\2", dataset)
outdir <- file.path(outroot, "results", rid, pdir, dataset)
f_rds <- file.path(outdir, "EXACT.rds"); f_sha <- file.path(outdir, "EXACT.sha256"); f_done <- file.path(outdir, "EXACT.done")
lockdir <- file.path(outdir, ".lock")
fail_at <- Sys.getenv("LOWP_ENUM_FAIL_AT", unset = "")
inject <- function(point) if (identical(fail_at, point)) stop("injected failure at ", point)

## ---- input and manifest (sealed-input verification) --------------------------------------------------------------
infile <- file.path(study, "inputs", pdir, paste0(dataset, ".rds"))
if (!file.exists(infile)) stop("input not found: ", infile)
in_sha <- lowp_sha256(infile)
man <- file.path(study, "manifests", "inputs_manifest_lowp.csv")
manifest_checked <- FALSE; manifest_sha <- NA_character_
if (!file.exists(man)) {
  if (!unsealed) stop("the inputs manifest is required (", man, "); use --unsealed-test-input only for tests")
} else {
  m <- read.csv(man, stringsAsFactors = FALSE, colClasses = "character")
  row <- m[!is.na(m$dataset_id) & m$dataset_id == dataset, , drop = FALSE]
  if (nrow(row) != 1) stop("dataset ", dataset, " must appear exactly once in ", man, " (found ", nrow(row), ")")
  if (!identical(tolower(row$file_sha256), tolower(in_sha)))
    stop("input file SHA-256 differs from the manifest for ", dataset, ": ", in_sha, " vs ", row$file_sha256)
  manifest_checked <- TRUE; manifest_sha <- lowp_sha256(man)
}
input_mode <- if (manifest_checked) "sealed" else "unsealed_test"
d <- readRDS(infile)   # the dataset is needed by the resume check (dimensions, retained-column map)

## ---- source fingerprint: enum sources + vendored headers + the core's scorer headers + core preprocessing ----------------
cd0 <- lowp_core_dir(core_dir); lowp_check_vendor(cd0)   # vendored headers must equal the core's (stops otherwise)
srcs <- c(lowp_enum.cpp = file.path(script_dir, "lowp_enum.cpp"), lowp_enum.R = file.path(script_dir, "lowp_enum.R"),
          run_enum_dataset.R = file.path(script_dir, "run_enum_dataset.R"), Makevars.lowp = file.path(script_dir, "Makevars.lowp"),
          v3_preprocess.R = file.path(cd0, "v3_preprocess.R"), v3_score.h = file.path(script_dir, "vendor", "v3_score.h"),
          v3_util.h = file.path(script_dir, "vendor", "v3_util.h"),
          core_v3_score.h = file.path(cd0, "cpp", "v3_score.h"), core_v3_util.h = file.path(cd0, "cpp", "v3_util.h"))
src_hashes <- vapply(srcs, lowp_sha256, "")
fingerprint <- digest::digest(paste(src_hashes, collapse = ""), algo = "sha256", serialize = FALSE)

## ---- completion verification and lock -------------------------------------------------------------------------------
read_hash_line <- function(f) { l <- tryCatch(readLines(f, n = 1L, warn = FALSE), error = function(e) character(0)); if (length(l)) tolower(sub("^([0-9a-fA-F]{64}).*$", "\\1", l[1])) else NA_character_ }
verify_committed <- function() {   # TRUE only for a complete, consistent, current result
  if (!all(file.exists(f_rds, f_sha, f_done)) || dir.exists(f_rds) || dir.exists(f_sha) || dir.exists(f_done)) return(list(ok = FALSE, why = "marker, sidecar or RDS missing"))
  h <- lowp_sha256(f_rds); hs <- read_hash_line(f_sha); hd <- read_hash_line(f_done)
  if (is.na(hs) || is.na(hd) || !identical(h, hs) || !identical(h, hd)) return(list(ok = FALSE, why = "RDS hash differs from sidecar or marker"))
  rec <- tryCatch(readRDS(f_rds), error = function(e) NULL)
  if (is.null(rec) || !identical(rec$schema, "lowp_exact_v1") || !identical(rec$dataset_id, dataset)) return(list(ok = FALSE, why = "RDS unreadable or of another dataset"))
  if (!identical(rec$extra$input_file_sha256, in_sha)) return(list(ok = FALSE, why = "RDS was computed from different input bytes"))
  # the full requested contract, not just the bytes: current sources, then the shared strict I2 validator bound to this input and mode
  if (!identical(rec$source_sha256, fingerprint)) return(list(ok = FALSE, why = "record was produced by different sources (enum, vendored headers, core scorer headers or preprocessing)"))
  vv <- lowp_validate_exact(rec, requested_scales = scales, input = list(X = d$X, dataset_id = dataset, file_sha256 = in_sha, manifest_sha256 = manifest_sha),
                            mode = input_mode, exact_scale_set = TRUE)
  if (!vv$ok) return(list(ok = FALSE, why = paste(vv$reasons, collapse = "; ")))
  list(ok = TRUE, why = "")
}
acquire_lock <- function() {
  dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
  for (attempt in 1:2) {
    if (dir.create(lockdir, showWarnings = FALSE)) {
      writeLines(c(paste("pid", Sys.getpid()), paste("host", Sys.info()[["nodename"]]), format(Sys.time(), usetz = TRUE)), file.path(lockdir, "owner"))
      return(invisible(TRUE))
    }
    age <- as.numeric(difftime(Sys.time(), file.info(lockdir)$mtime, units = "secs"))
    if (is.finite(age) && age > 600) unlink(lockdir, recursive = TRUE) else break
  }
  message("another writer holds the destination lock: ", lockdir); quit(status = 3)
}
release_lock <- function() unlink(lockdir, recursive = TRUE)

v <- verify_committed()
if (v$ok && !flag("force")) { cat("EXACT.done verified (hashes, dataset, input bytes, source fingerprint, requested scales, complete/exact, required fields), nothing to do:", outdir, "\n"); quit(status = 0) }
if (file.exists(f_done) && !v$ok) message("existing EXACT.done is not valid (", v$why, "): recomputing")
if (file.exists(f_done)) { acquire_lock(); tryCatch(unlink(f_done), finally = release_lock()) }   # invalidate before any work

## ---- compute -------------------------------------------------------------------------------------------------------
if (!all(c("X", "Y") %in% names(d))) stop("input lacks X or Y")
if (!is.null(d$dataset_id) && !identical(as.character(d$dataset_id), dataset)) stop("input dataset_id differs from --dataset")
if (!is.null(d$kind) && !identical(as.character(d$kind), if (is_dev) "dev" else "prod")) stop("input kind mismatch")
if (!all(scales %in% colnames(d$Y))) stop("scale column(s) missing in Y: ", paste(setdiff(scales, colnames(d$Y)), collapse = ","))
X <- d$X; Ylist <- setNames(lapply(scales, function(s) as.numeric(d$Y[, s])), scales)

lowp_load(core_dir)   # vendor-hash check, preprocessing source, compile (excluded from runtime_s)
started <- format(Sys.time(), tz = "UTC", usetz = FALSE, "%Y-%m-%dT%H:%M:%SZ")
t0 <- proc.time()[["elapsed"]]
ex <- lowp_exact(X, Ylist, top = 1000, threads = threads, core_dir = core_dir)
run <- attr(ex, "run")
runtime <- proc.time()[["elapsed"]] - t0
finished <- format(Sys.time(), tz = "UTC", usetz = FALSE, "%Y-%m-%dT%H:%M:%SZ")
if (!identical(run$status, "exact") || !isTRUE(run$complete)) stop("enumeration did not complete: ", run$status, " ", run$message)
expect <- sum(choose(run$p, 0:run$K))
if (run$models_scored != expect) stop("models scored ", run$models_scored, " != expected ", expect)

scales_out <- ex; attr(scales_out, "run") <- NULL
rec <- list(schema = "lowp_exact_v1", dataset_id = dataset, p = ncol(X), n = nrow(X), K = run$K,
            source_sha256 = fingerprint,
            v3_score_sha256 = src_hashes[["v3_score.h"]], runtime_s = runtime, host = Sys.info()[["nodename"]],
            started_utc = started, finished_utc = finished, models_scored = run$models_scored,
            models_expected = run$models_expected, complete = run$complete, threads = threads,
            scales = scales_out,
            extra = list(source_files_sha256 = src_hashes, input_file_sha256 = in_sha, input_mode = input_mode,
                         manifest_checked = manifest_checked, manifest_sha256 = manifest_sha,
                         r_version = R.version.string, compile_key = .lowp$key, task_bits = run$task_bits,
                         retained_columns = run$orig, status = run$status, complete = run$complete,
                         models_expected = run$models_expected))

vv <- lowp_validate_exact(rec, requested_scales = scales, input = list(X = d$X, dataset_id = dataset, file_sha256 = in_sha, manifest_sha256 = manifest_sha),
                          mode = input_mode, exact_scale_set = TRUE)
if (!vv$ok) stop("refusing to publish: the new record violates the EXACT contract: ", paste(vv$reasons, collapse = "; "))

## ---- publish (under the destination lock) ---------------------------------------------------------------------------
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
acquire_lock()
tag <- Sys.getpid()
tmp_rds <- file.path(outdir, paste0("EXACT.rds.tmp", tag)); tmp_sha <- file.path(outdir, paste0("EXACT.sha256.tmp", tag)); tmp_done <- file.path(outdir, paste0(".done.tmp", tag))
mv <- function(from, to) if (!isTRUE(suppressWarnings(file.rename(from, to)))) stop("could not rename ", basename(from), " to ", basename(to))
tryCatch({
if (file.exists(f_done)) unlink(f_done)                                   # 1. invalidate any old completion marker
if (file.exists(f_done)) stop("could not remove the old EXACT.done")
saveRDS(rec, tmp_rds, compress = FALSE)                                    # 2. stage and verify under temporary names
sha <- lowp_sha256(tmp_rds)
chk <- readRDS(tmp_rds)
stopifnot(identical(chk$scales[[1]]$log_Z, ex[[1]]$log_Z), identical(chk$dataset_id, dataset))
writeLines(paste0(sha, "  EXACT.rds"), tmp_sha)
inject("before_rds_rename")
mv(tmp_rds, f_rds)                                                         # 3. commit the pair
inject("after_rds_rename")
mv(tmp_sha, f_sha)
inject("after_sha_rename")
if (!identical(lowp_sha256(f_rds), sha) || !identical(read_hash_line(f_sha), sha)) stop("committed RDS/sidecar do not match the staged hash")
inject("before_done")
writeLines(c(sha, finished), tmp_done)                                     # 4. publish the marker last
mv(tmp_done, f_done)
v <- verify_committed()
if (!v$ok) { unlink(f_done); stop("post-commit verification failed: ", v$why) }
}, finally = { unlink(c(tmp_rds, tmp_sha, tmp_done)); release_lock() })
cat(sprintf("OK %s: %g models, %.1f s elapsed, %d threads, input_mode %s; %s\n", dataset, run$models_scored, runtime, threads, input_mode, outdir))
