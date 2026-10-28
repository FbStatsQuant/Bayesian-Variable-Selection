#!/usr/bin/env Rscript
# run_case.R -- runner for one dataset x the F4 method ids at one signal scale.
# Implements master §III.3.0 (registry loop, RNG reset before every method call, library assertion,
# outer capture layer, environment isolation) and §IV.1.1-§IV.1.2 (files written atomically,
# rule-row schema). Ported in spirit from Oct-14 Experiments_October_14_Benchmarks/scripts/run_case.R.
# Opens only the inputs/ file it is given (and, optionally, the inputs manifest); never the
# truth/ tree. Scoring columns are left NA (filled by the scoring step only, §IV.1.2).
#
# Usage:
#   Rscript run_case.R --input <inputs/.../dev_p0500_S1_r001.rds> --out-root <results/<run_id>>
#                      --run-id <run_id> [--scale c100] [--methods F4,F4_SCAD] [--manifest <csv>]

parse_args <- function(args) {
  out <- list(scale = "c100", methods = "F4,F4_SCAD", manifest = NA_character_)
  i <- 1L
  while (i <= length(args)) {
    if (!startsWith(args[i], "--") || i == length(args)) stop("bad argument list near ", args[i])
    out[[gsub("-", "_", sub("^--", "", args[i]))]] <- args[i + 1L]
    i <- i + 2L
  }
  for (k in c("input", "out_root", "run_id"))
    if (is.null(out[[k]])) stop("missing --", gsub("_", "-", k))
  out$methods <- strsplit(out$methods, ",", fixed = TRUE)[[1L]]
  out
}

# Columns of §IV.1.2 in schema order; the method's extra columns follow.
SCHEMA_COLS <- c("study", "run_id", "source_sha256",
  "regime", "p", "scenario", "replicate", "scale_key", "scale", "dataset_id", "case_id",
  "data_seed", "fold_seed", "method_seed",
  "inputs_sha256", "x_sha256", "y_sha256", "fold_sha256",
  "method_id", "method_label", "package", "package_version",
  "rule_id", "role", "status",
  "converged", "diag_flag", "diag_codes", "n_warnings", "warnings", "messages", "error",
  "k", "support", "support_audit",
  "tp", "fp", "fn", "exact", "error_type",
  sprintf("sel_a%02d", 1:14), sprintf("pip_a%02d", 1:14), "max_pip_null",
  "runtime_s", "host", "slurm_job_id", "slurm_array_task_id", "started_utc", "finished_utc")
SCORING_COLS <- c("tp", "fp", "fn", "exact", "error_type",
                  sprintf("sel_a%02d", 1:14), sprintf("pip_a%02d", 1:14), "max_pip_null")

utc_now <- function() format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC")

script_dir <- function() {
  f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE))
  if (length(f) != 1L) stop("run_case.R must be run with Rscript")
  dirname(normalizePath(f, mustWork = TRUE))
}

# Verifies an existing output set (sha = file hashing function from common.R): .done present, and
# the .sha256 file lists exactly the .rds and .csv of this method id, both present with those hashes.
outputs_valid <- function(prefix, sha) {
  if (!file.exists(paste0(prefix, ".done")) || !file.exists(paste0(prefix, ".sha256"))) return(FALSE)
  parts <- strsplit(readLines(paste0(prefix, ".sha256")), "  ", fixed = TRUE)
  if (length(parts) != 2L || any(lengths(parts) != 2L)) return(FALSE)
  listed <- vapply(parts, function(x) x[2L], "")
  if (!identical(sort(listed), sort(paste0(basename(prefix), c(".csv", ".rds"))))) return(FALSE)
  all(vapply(parts, function(x) {
    f <- file.path(dirname(prefix), x[2L])
    file.exists(f) && identical(sha(f), x[1L])
  }, TRUE))
}

# A completed output may be skipped only if it was produced for the same request: same run id,
# case, method id, code (source_sha256), input hashes, settings and execution environment
# (R, BLAS/LAPACK, package versions, study-library manifest). Otherwise the runner stops.
same_request <- function(prefix, run_id, case_id, mid, source_sha256, hashes, settings, env_id) {
  old <- readRDS(paste0(prefix, ".rds"))
  r <- old$rows
  identical(unique(r$run_id), run_id) && identical(old$case_id, case_id) &&
    identical(old$method_id, mid) && identical(unique(r$source_sha256), source_sha256) &&
    identical(old$hashes, hashes) && identical(old$settings, settings) && identical(old$env_id, env_id)
}

run_case <- function(args) {
  a <- parse_args(args)
  code_dir <- script_dir()
  source(file.path(code_dir, "config.R"), local = TRUE)
  .libPaths(c(STUDY_LIB, .Library))
  source(file.path(code_dir, "common.R"), local = TRUE)

  # §III.3.0 runtime stack, "Threads" and "Library": R 4.5.2; one thread; every package from the
  # sealed study library, loaded before any fit is timed.
  if (!identical(as.character(getRversion()), R_VERSION)) stop("R ", getRversion(), " != pinned ", R_VERSION)
  thr <- Sys.getenv(c("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"))
  if (!all(thr == "1")) stop("thread variables must all be 1: ", paste(names(thr), thr, collapse = ", "))
  lib_root <- normalizePath(STUDY_LIB, mustWork = TRUE)
  for (pkg in c("ncvreg", "digest")) {
    loc <- normalizePath(find.package(pkg), mustWork = TRUE)
    if (!startsWith(loc, paste0(lib_root, "/"))) stop(pkg, " not loaded from the sealed library: ", loc)
    loadNamespace(pkg)                     # preload, so runtime_s does not include namespace loading
  }
  env_id <- list(R = R.version.string, blas = extSoftVersion()[["BLAS"]], lapack = La_library(),
                 packages = vapply(c("ncvreg", "digest"), function(p) as.character(utils::packageVersion(p)), ""),
                 lib_manifest_sha256 = file_sha256(file.path(dirname(lib_root), "environment_manifest.txt")))

  # Fitting code is sourced into an environment whose parent is the stats namespace (§III.3.0);
  # it never sees the runner's variables. It receives only (X, y, foldid, seed, settings).
  engine <- new.env(parent = asNamespace("stats"))
  sys.source(file.path(code_dir, "common.R"), envir = engine)
  sys.source(file.path(code_dir, "methods", "fit_F4_mcp.R"), envir = engine)

  src_files <- file.path(code_dir, c("config.R", "common.R", "methods/fit_F4_mcp.R", "run_case.R"))
  src_hash <- vapply(src_files, file_sha256, "")
  source_sha256 <- digest::digest(paste(basename(src_files), src_hash, collapse = "\n"),
                                  algo = "sha256", serialize = FALSE)

  # Inputs (§II.10): the one file named on the command line.
  input <- normalizePath(a$input, mustWork = TRUE)
  dat <- readRDS(input)
  need <- c("X", "Y", "foldid", "dataset_id", "data_seed", "fold_seed", "method_seed", "p",
            "scenario", "replicate", "scales")
  if (!all(need %in% names(dat))) stop("input lacks fields: ", paste(setdiff(need, names(dat)), collapse = ","))
  if (!(a$scale %in% colnames(dat$Y))) stop("scale not in Y: ", a$scale)
  X <- dat$X; y <- unname(dat$Y[, a$scale]); foldid <- dat$foldid
  if (dat$method_seed != dat$data_seed + METHOD_SEED_OFFSET) stop("method_seed != data_seed + offset")
  hashes <- list(inputs_sha256 = file_sha256(input), x_sha256 = f64_sha256(X),
                 y_sha256 = f64_sha256(y), fold_sha256 = f64_sha256(foldid))
  if (!is.na(a$manifest)) {                                  # integrity check against the manifest
    man <- utils::read.csv(a$manifest, stringsAsFactors = FALSE)
    m <- man[man$dataset_id == dat$dataset_id, , drop = FALSE]
    if (nrow(m) != 1L) stop("dataset not in manifest exactly once: ", dat$dataset_id)
    ok <- c(m$file_sha256 == hashes$inputs_sha256, m$x_sha256 == hashes$x_sha256,
            m$foldid_sha256 == hashes$fold_sha256, m[[paste0("y_", a$scale, "_sha256")]] == hashes$y_sha256)
    if (!all(ok)) stop("input hashes differ from the manifest for ", dat$dataset_id)
  }
  case_id <- paste0(dat$dataset_id, "_", a$scale)
  outdir <- file.path(a$out_root, sprintf("p%04d", as.integer(dat$p)), case_id)
  dir.create(outdir, recursive = TRUE, showWarnings = FALSE)

  # One (case, method) pair: completion check, fit and the four files; called under the pair lock.
  do_pair <- function(mid) {
    mrow <- registry_row(CONFIG, mid)
    prefix <- file.path(outdir, mid)
    settings <- CONFIG; settings$variant <- mrow$variant
    if (file.exists(paste0(prefix, ".done"))) {
      if (!outputs_valid(prefix, file_sha256))
        stop("existing .done with invalid or incomplete hashes; refusing to overwrite: ", prefix)
      if (!same_request(prefix, a$run_id, case_id, mid, source_sha256, hashes, settings, env_id))
        stop("existing .done was produced for a different request (run id, code, inputs, settings or environment): ", prefix)
      cat(case_id, mid, "skipped (valid .done for the same request)\n"); return(invisible())
    }
    fitfun <- get(mrow$fn, envir = engine, inherits = FALSE)

    # §III.3.0 RNG: reset immediately before every method call.
    RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(dat$method_seed)
    started <- utc_now(); t0 <- elapsed()
    cap <- with_captured_conditions(fitfun(X, y, foldid, dat$method_seed, settings))
    runtime <- elapsed() - t0
    finished <- utc_now()

    # Outer capture layer: an uncaught error becomes the registered failed rows.
    res <- cap$value
    if (!is.na(cap$error)) {
      res <- list(rules = fail_rows(mrow, CONFIG$F4_EXTRA_COLS, cap$error), pip = NULL,
                  beta = rep(NA_real_, ncol(X)), converged = FALSE,
                  diagnostics = list(error = cap$error), warnings = character(), messages = character())
    }
    warns <- c(res$warnings, cap$warnings); msgs <- c(res$messages, cap$messages)
    rows <- res$rules
    if (!identical(rows$rule_id, mrow$rule_ids[[1L]]) || !identical(rows$role, mrow$roles[[1L]]))
      stop("wrapper rule frame does not match the registry for ", mid)
    # §III.3.0 "Status": warning when any warning or message was captured; failure takes precedence.
    if (length(warns) + length(msgs) > 0L) rows$status[rows$status == "ok"] <- "warning"

    rows$study <- "bench20261019"; rows$run_id <- a$run_id; rows$source_sha256 <- source_sha256
    rows$regime <- "H"; rows$p <- as.integer(dat$p); rows$scenario <- as.integer(dat$scenario)
    rows$replicate <- as.integer(dat$replicate); rows$scale_key <- a$scale
    rows$scale <- unname(dat$scales[[a$scale]]); rows$dataset_id <- dat$dataset_id
    rows$case_id <- case_id; rows$data_seed <- as.integer(dat$data_seed)
    rows$fold_seed <- as.integer(dat$fold_seed); rows$method_seed <- as.integer(dat$method_seed)
    for (h in names(hashes)) rows[[h]] <- hashes[[h]]
    rows$method_id <- mid; rows$method_label <- mrow$method_label
    rows$package <- mrow$package; rows$package_version <- mrow$pkg_version
    rows$n_warnings <- length(warns)
    rows$warnings <- if (length(warns)) paste(unique(warns), collapse = " | ") else NA_character_
    rows$messages <- if (length(msgs)) paste(unique(msgs), collapse = " | ") else NA_character_
    for (sc in SCORING_COLS) rows[[sc]] <- NA
    rows$runtime_s <- runtime; rows$host <- Sys.info()[["nodename"]]
    rows$slurm_job_id <- Sys.getenv("SLURM_JOB_ID", NA_character_)
    rows$slurm_array_task_id <- Sys.getenv("SLURM_ARRAY_TASK_ID", NA_character_)
    rows$started_utc <- started; rows$finished_utc <- finished
    extra_names <- setdiff(names(rows), SCHEMA_COLS)
    rows <- rows[, c(SCHEMA_COLS, extra_names)]

    result <- list(schema_version = 1L, rows = rows, beta = res$beta, pip = res$pip,
                   converged = res$converged, diagnostics = res$diagnostics,
                   warnings = warns, messages = msgs, case_id = case_id, method_id = mid,
                   input_path = input, hashes = hashes,
                   source_files = data.frame(file = basename(src_files), sha256 = unname(src_hash)),
                   settings = settings, env_id = env_id, session = utils::sessionInfo(),
                   lib_paths = .libPaths(), threads = thr, started_utc = started, finished_utc = finished)
    atomic_write(paste0(prefix, ".rds"), function(f) saveRDS(result, f, compress = "xz", version = 3))
    atomic_write(paste0(prefix, ".csv"), function(f) utils::write.csv(rows, f, row.names = FALSE, na = "NA"))
    files <- paste0(prefix, c(".rds", ".csv"))
    atomic_write(paste0(prefix, ".sha256"), function(f)
      writeLines(paste(vapply(files, file_sha256, ""), basename(files), sep = "  "), f))
    atomic_write(paste0(prefix, ".done"), function(f)
      writeLines(c(paste("finished_utc", finished), paste("status", paste(rows$status, collapse = ","))), f))
    cat(sprintf("%s %s runtime %.2fs status %s k %s\n", case_id, mid, runtime,
                paste(rows$status, collapse = ","), paste(rows$k, collapse = ",")))
  }

  for (mid in a$methods) {
    # Exclusive per-pair lock (mkdir is atomic on the shared file system), held from the completion
    # check through .done. A lock left by a killed job is removed only by slurm/clear_stale_locks.sh,
    # which refuses while any job of this method is queued or running.
    lock <- file.path(outdir, paste0(mid, ".lock"))
    if (!dir.create(lock, showWarnings = FALSE))
      stop("pair is locked (another writer, or a stale lock from a killed job): ", lock)
    writeLines(c(Sys.info()[["nodename"]], Sys.getpid(), Sys.getenv("SLURM_JOB_ID"), utc_now()),
               file.path(lock, "owner"))
    tryCatch(do_pair(mid), finally = unlink(lock, recursive = TRUE))
  }
  invisible(0L)
}

if (sys.nframe() == 0L) {
  st <- tryCatch({ run_case(commandArgs(trailingOnly = TRUE)); 0L },
                 error = function(e) { message("FATAL: ", conditionMessage(e)); 1L })
  quit(save = "no", status = st)
}
