#!/usr/bin/env Rscript
# Runner for benchmark A3: one dataset x the registered method ids x the requested scales,
# writing the four files of master §IV.1.1 atomically, with the rule-row schema of §IV.1.2.
# Opens only the inputs/ file it is given (and the inputs manifest, for hash checks);
# never opens truth. Holds no state across fits (§III.3.8 k).
#
# Usage (NOTS, after `module load GCC/14.3.0` and `module load R/4.5.2`):
#   Rscript run_case.R --input <inputs/.../dataset.rds> --manifest <manifests/dev_inputs_manifest.csv>
#                      --outroot <dir> --run-id <id> [--methods A3] [--scales c100]

CODE_DIR <- local({
  f <- grep("^--file=", commandArgs(FALSE), value = TRUE)
  if (length(f)) dirname(normalizePath(sub("^--file=", "", f[1]))) else getwd()
})
CODE_FILES <- c("config.R", "common.R", "methods/fit_A3_horseshoe.R", "run_case.R")

parse_args <- function(args) {
  out <- list(methods = "A3", scales = "c100")
  i <- 1L
  while (i <= length(args)) {
    if (!startsWith(args[i], "--") || i == length(args)) stop("bad arguments near ", args[i])
    out[[gsub("-", "_", sub("^--", "", args[i]))]] <- args[i + 1L]
    i <- i + 2L
  }
  for (k in c("input", "manifest", "outroot", "run_id"))
    if (is.null(out[[k]])) stop("missing --", gsub("_", "-", k))
  out$methods <- strsplit(out$methods, ",", fixed = TRUE)[[1]]
  out$scales <- strsplit(out$scales, ",", fixed = TRUE)[[1]]
  out
}

# Column order of the CSV: §IV.1.2 schema, then the method's extra columns.
schema_columns <- function(settings, extra_cols) {
  na <- settings$COMMON$N_ACTIVE_COLS
  c("study", "run_id", "source_sha256",
    "regime", "p", "scenario", "replicate", "scale_key", "scale", "dataset_id", "case_id",
    "data_seed", "fold_seed", "method_seed",
    "inputs_sha256", "x_sha256", "y_sha256", "fold_sha256",
    "method_id", "method_label", "package", "package_version",
    "rule_id", "role", "status",
    "converged", "diag_flag", "diag_codes", "n_warnings", "warnings", "messages", "error",
    "k", "support", "support_audit",
    "tp", "fp", "fn", "exact", "error_type",
    sprintf("sel_a%02d", seq_len(na)), sprintf("pip_a%02d", seq_len(na)), "max_pip_null",
    "runtime_s", "host", "slurm_job_id", "slurm_array_task_id", "started_utc", "finished_utc",
    extra_cols)
}

# The library guarantee of §III.3.0: every package used is loaded from the sealed study library.
assert_study_library <- function(settings, pkgs) {
  lib <- normalizePath(settings$COMMON$LIB, mustWork = TRUE)
  for (pk in pkgs) {
    path <- normalizePath(find.package(pk), mustWork = TRUE)
    if (!startsWith(path, paste0(lib, "/"))) stop("package ", pk, " is not loaded from ", lib, ": ", path)
  }
  invisible(TRUE)
}

# One fit inside the outer capture layer (§III.3.0 "One capture layer"): an uncaught error of
# the wrapper becomes the registered failed rows. Seeds and RNG kind are set immediately before.
run_fit_safely <- function(fn, X, y, foldid, seed, settings, method_id) {
  RNGkind(settings$COMMON$RNG_KIND[1], settings$COMMON$RNG_KIND[2], settings$COMMON$RNG_KIND[3])
  set.seed(seed)
  t0 <- proc.time()[["elapsed"]]
  res <- tryCatch(fn(X, y, foldid, seed, settings), error = function(e) {
    extra <- setNames(as.list(rep(NA, length(settings$A3$EXTRA_COLS))), settings$A3$EXTRA_COLS)
    list(rules = fail_rows(settings, method_id, error = paste("uncaught:", conditionMessage(e)),
                           extra = extra),
         pip = NULL, beta = rep(NA_real_, ncol(X)), converged = NA,
         diagnostics = list(uncaught_error = conditionMessage(e)), warnings = character(0))
  })
  res$runtime_s <- elapsed(t0)
  res
}

# A completed (case, method) is valid only if its .done exists, its .sha256 lists exactly the RDS
# and the CSV with matching hashes, and its CSV rows belong to the expected case, code version
# and inputs (`expect`: named list of case_id, source_sha256, x_sha256, y_sha256, method_seed).
done_is_valid <- function(prefix, expect = NULL) {
  f_done <- paste0(prefix, ".done"); f_sha <- paste0(prefix, ".sha256")
  if (!file.exists(f_done) || !file.exists(f_sha)) return(FALSE)
  if (!is.null(expect)) {
    rows <- tryCatch(utils::read.csv(paste0(prefix, ".csv"), stringsAsFactors = FALSE,
                                     colClasses = "character"), error = function(e) NULL)
    if (is.null(rows) || nrow(rows) == 0L) return(FALSE)
    for (nm in names(expect)) if (!all(rows[[nm]] == as.character(expect[[nm]]))) return(FALSE)
  }
  lines <- readLines(f_sha)
  parts <- strsplit(lines, "  ", fixed = TRUE)
  # The checksum list must cover exactly the RDS and the CSV of this (case, method).
  listed <- vapply(parts, function(x) if (length(x) == 2L) x[2] else NA_character_, "")
  if (!setequal(listed, paste0(basename(prefix), c(".rds", ".csv"))) || length(listed) != 2L) return(FALSE)
  all(vapply(parts, function(x) {
    f <- file.path(dirname(prefix), x[2])
    file.exists(f) && identical(file_sha256(f), x[1])
  }, TRUE))
}

# Adds the provenance, design, seed, hash, method and compute columns to a wrapper's rule frame
# and puts the columns in schema order; the scoring-only columns stay NA (§IV.1.2).
assemble_rows <- function(rows, design, settings) {
  for (nm in names(design)) rows[[nm]] <- design[[nm]]
  cols <- schema_columns(settings, settings$A3$EXTRA_COLS)
  for (nm in setdiff(cols, names(rows))) rows[[nm]] <- NA
  if (length(setdiff(names(rows), cols))) stop("unregistered columns: ", paste(setdiff(names(rows), cols), collapse = ","))
  rows[, cols]
}

# The four files of §IV.1.1, each written atomically; .sha256 lists the RDS and the CSV, and
# .done is written last.
write_case_files <- function(prefix, rows, record, finished) {
  atomic_write(paste0(prefix, ".rds"), function(f) saveRDS(record, f, compress = "xz", version = 3))
  atomic_write(paste0(prefix, ".csv"), function(f) utils::write.csv(rows, f, row.names = FALSE, na = "NA"))
  paths <- paste0(prefix, c(".rds", ".csv"))
  atomic_write(paste0(prefix, ".sha256"), function(f)
    writeLines(paste(vapply(paths, file_sha256, ""), basename(paths), sep = "  "), f))
  atomic_write(paste0(prefix, ".done"), function(f)
    writeLines(c(paste("status", paste(rows$status, collapse = ",")), paste("finished_utc", finished)), f))
  invisible(prefix)
}

main <- function(args) {
  a <- parse_args(args)
  # The runner's own copies of the constants and helpers (global environment of this script).
  sys.source(file.path(CODE_DIR, "config.R"), envir = globalenv())
  sys.source(file.path(CODE_DIR, "common.R"), envir = globalenv())
  .libPaths(c(COMMON$LIB, .Library))
  settings_base <- make_settings("primary")
  if (grepl("/truth/", normalizePath(a$input), fixed = TRUE)) stop("refusing to open a truth file")

  # Fitting environment: parent is the stats namespace (§III.3.0); it sees only the helpers,
  # the wrappers and what is passed as arguments.
  engine <- new.env(parent = asNamespace("stats"))
  sys.source(file.path(CODE_DIR, "common.R"), envir = engine)
  sys.source(file.path(CODE_DIR, "methods", "fit_A3_horseshoe.R"), envir = engine)

  # Every namespace the fit uses is loaded here, before any fit timer starts, so runtime_s
  # excludes package loading (PROD_READINESS_BRIEF, runner timing). parallel is a base package.
  pkgs <- c(names(settings_base$A3$PKG_VERSIONS), "coda", "digest", "foreach", "iterators")
  for (pk in c(pkgs, "parallel")) loadNamespace(pk)
  assert_study_library(settings_base, pkgs)
  r_ver <- paste(R.version$major, R.version$minor, sep = ".")
  if (!identical(r_ver, settings_base$COMMON$R_VERSION))
    stop("R version ", r_ver, ", expected ", settings_base$COMMON$R_VERSION)
  thr <- Sys.getenv(settings_base$COMMON$THREAD_VARS)
  if (!all(thr == "1")) stop("thread variables must be 1: ", paste(names(thr), thr, collapse = ", "))

  code_hashes <- vapply(file.path(CODE_DIR, CODE_FILES), file_sha256, "")
  names(code_hashes) <- CODE_FILES
  source_sha256 <- digest::digest(paste(CODE_FILES, code_hashes, collapse = "\n"),
                                  algo = "sha256", serialize = FALSE)

  d <- readRDS(a$input)
  # The inputs manifest must be the copy frozen with the run, when the job says which one it is.
  if (nzchar(Sys.getenv("A3_MANIFEST_SHA256")) &&
      !identical(file_sha256(a$manifest), Sys.getenv("A3_MANIFEST_SHA256")))
    stop("inputs manifest differs from the frozen copy: ", a$manifest)
  man <- utils::read.csv(a$manifest, stringsAsFactors = FALSE)
  m <- man[man$dataset_id == d$dataset_id, , drop = FALSE]
  if (nrow(m) != 1L) stop("dataset not in manifest: ", d$dataset_id)
  inputs_sha256 <- file_sha256(a$input)
  x_sha256 <- f64_sha256(d$X); fold_sha256 <- f64_sha256(d$foldid)
  if (!identical(inputs_sha256, m$file_sha256)) stop("input file hash differs from manifest")
  if (!identical(x_sha256, m$x_sha256)) stop("X hash differs from manifest")
  if (!identical(fold_sha256, m$foldid_sha256)) stop("foldid hash differs from manifest")
  if (!identical(as.integer(d$method_seed), as.integer(d$data_seed) + METHOD_SEED_OFFSET))
    stop("method_seed != data_seed + METHOD_SEED_OFFSET")
  p <- ncol(d$X)
  host <- Sys.info()[["nodename"]]
  status_all <- 0L

  for (scale_key in a$scales) {
    y <- unname(d$Y[, scale_key])
    y_sha256 <- f64_sha256(y)
    if (!identical(y_sha256, m[[paste0("y_", scale_key, "_sha256")]])) stop("y hash differs from manifest")
    case_id <- paste0(d$dataset_id, "_", scale_key)
    outdir <- file.path(a$outroot, "results", a$run_id, sprintf("p%04d", p), case_id)
    dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
    for (mid in a$methods) {
      reg <- registry_row(settings_base, mid)
      prefix <- file.path(outdir, mid)
      expect <- list(case_id = case_id, source_sha256 = source_sha256, x_sha256 = x_sha256,
                     y_sha256 = y_sha256, method_seed = as.integer(d$method_seed))
      if (done_is_valid(prefix, expect)) { cat(case_id, mid, "already done; skipped\n"); next }
      unlink(paste0(prefix, ".done"))       # a stale marker never survives a rewrite
      settings <- make_settings(reg$variant)
      started <- format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC")
      res <- run_fit_safely(engine[[reg$fn]], d$X, y, d$foldid, as.integer(d$method_seed), settings, mid)
      finished <- format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC")

      rows <- res$rules
      # Memory exhaustion is an infrastructure failure (master §IV.2.4), not a method failure:
      # write nothing, so the case stays missing and is resubmitted with more memory.
      if (any(grepl("cannot allocate", rows$error, fixed = TRUE)))
        stop("infrastructure: memory allocation failed in ", case_id, ": ", rows$error[1])
      design <- list(study = settings$COMMON$STUDY, run_id = a$run_id, source_sha256 = source_sha256,
        regime = settings$COMMON$REGIME, p = p, scenario = as.integer(d$scenario),
        replicate = as.integer(d$replicate), scale_key = scale_key,
        scale = unname(settings$COMMON$SCALES[[scale_key]]), dataset_id = d$dataset_id,
        case_id = case_id, data_seed = as.integer(d$data_seed), fold_seed = as.integer(d$fold_seed),
        method_seed = as.integer(d$method_seed), inputs_sha256 = inputs_sha256,
        x_sha256 = x_sha256, y_sha256 = y_sha256, fold_sha256 = fold_sha256,
        method_id = mid, method_label = reg$method_label, package = reg$package,
        package_version = reg$pkg_version,
        runtime_s = res$runtime_s, host = host,
        slurm_job_id = Sys.getenv("SLURM_JOB_ID", NA), slurm_array_task_id = Sys.getenv("SLURM_ARRAY_TASK_ID", NA),
        started_utc = started, finished_utc = finished)
      rows <- assemble_rows(rows, design, settings)

      record <- list(schema_version = 1L, rows = rows, beta = res$beta, pip = res$pip,
        converged = res$converged, diagnostics = res$diagnostics, warnings = res$warnings,
        runtime_s = res$runtime_s,
        case = design[c("dataset_id", "case_id", "p", "scenario", "replicate", "scale_key", "scale",
                        "data_seed", "fold_seed", "method_seed")],
        input = list(path = normalizePath(a$input), inputs_sha256 = inputs_sha256, x_sha256 = x_sha256,
                     y_sha256 = y_sha256, fold_sha256 = fold_sha256, manifest = normalizePath(a$manifest)),
        code = list(dir = CODE_DIR, files = code_hashes, source_sha256 = source_sha256),
        environment = list(R = R.version.string, session_info = utils::capture.output(utils::sessionInfo()),
          lib_paths = .libPaths(), RNGkind = RNGkind(), host = host, pid = Sys.getpid(),
          detect_cores = parallel::detectCores(),
          packages = vapply(pkgs, function(pk) as.character(utils::packageVersion(pk)), ""),
          threads = as.list(Sys.getenv(settings$COMMON$THREAD_VARS)),
          slurm = as.list(Sys.getenv(c("SLURM_JOB_ID", "SLURM_ARRAY_JOB_ID", "SLURM_ARRAY_TASK_ID")))),
        started_utc = started, finished_utc = finished)
      write_case_files(prefix, rows, record, finished)
      cat(sprintf("%s %s rules=%s status=%s k=%s runtime_s=%.1f\n", case_id, mid,
                  paste(rows$rule_id, collapse = ","), paste(rows$status, collapse = ","),
                  paste(rows$k, collapse = ","), res$runtime_s))
      if (any(rows$status == "failed")) status_all <- 2L
    }
  }
  status_all
}

if (sys.nframe() == 0L) {
  st <- tryCatch(main(commandArgs(trailingOnly = TRUE)), error = function(e) {
    message("FATAL: ", conditionMessage(e)); 1L
  })
  quit(save = "no", status = st)
}
