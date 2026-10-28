#!/usr/bin/env Rscript
# run_case.R -- runner for one dataset x the registered method ids x the requested scales.
# Master §III.3.0 (interface, one capture layer, files, RNG, library), §IV.1.1 (files),
# §IV.1.2 (rule-row schema). It opens only the inputs/ file (and, optionally, the inputs
# manifest); it never opens truth/. Scoring is a separate script (score_dev.R).
#
# Usage:
#   Rscript run_case.R --input <.../inputs/pXXXX/<dataset_id>.rds> --out <results root>
#                      --run-id <run_id> [--scales c100] [--methods F2]
#                      [--manifest <dev_inputs_manifest.csv>] [--code-dir <dir>]
# Outputs: <out>/<run_id>/p{pppp}/<case_id>/<method_id>.{rds,csv,sha256,done}

SCHEMA_VERSION <- 1L
CODE_FILES <- c("config.R", "common.R", "methods/glmnet_helpers.R", "methods/fit_F2_enet.R",
                "run_case.R")
FIT_FILES <- c("common.R", "methods/glmnet_helpers.R", "methods/fit_F2_enet.R")

parse_args <- function(args) {
  out <- list(); i <- 1L
  while (i <= length(args)) {
    if (!startsWith(args[i], "--") || i == length(args)) stop("bad argument list near ", args[i])
    out[[gsub("-", "_", sub("^--", "", args[i]))]] <- args[i + 1L]; i <- i + 2L
  }
  for (k in c("input", "out", "run_id")) if (is.null(out[[k]])) stop("missing --", k)
  if (is.null(out$scales)) out$scales <- "c100"
  out$scales <- strsplit(out$scales, ",", fixed = TRUE)[[1L]]
  if (!is.null(out$methods)) out$methods <- strsplit(out$methods, ",", fixed = TRUE)[[1L]]
  out
}

script_dir <- function() {
  f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE))
  if (length(f) != 1L) stop("cannot locate run_case.R; pass --code-dir")
  dirname(normalizePath(f, mustWork = TRUE))
}

# The runner asserts every package is loaded from the sealed study library (§III.3.0).
# After loading the method packages, every loaded namespace that is not a base package
# (Priority "base", shipped with R) must come from the study library, imports included.
assert_study_library <- function(pkgs, lib) {
  lib <- normalizePath(lib, mustWork = TRUE)
  for (pkg in pkgs) loadNamespace(pkg)
  for (ns in loadedNamespaces()) {
    if (identical(utils::packageDescription(ns)$Priority, "base")) next
    path <- normalizePath(getNamespaceInfo(ns, "path"), mustWork = TRUE)
    if (!startsWith(path, paste0(lib, "/"))) stop(ns, " is loaded from ", path, ", not ", lib)
  }
  invisible(TRUE)
}

code_hashes <- function(code_dir, io) {
  h <- vapply(file.path(code_dir, CODE_FILES), io$file_sha256, "")
  tree <- digest::digest(paste(h, CODE_FILES, sep = "  ", collapse = "\n"),
                         algo = "sha256", serialize = FALSE)
  list(files = data.frame(path = CODE_FILES, sha256 = unname(h), stringsAsFactors = FALSE),
       tree = tree)
}

# A valid .done: the four files exist, the payload hashes match, and the stored record was
# produced by this code tree, these settings, this run id and this input file. A complete
# record from a different context is never skipped silently and never overwritten: stop.
done_is_valid <- function(prefix, io, ctx, settings) {
  files <- paste0(prefix, c(".rds", ".csv", ".sha256", ".done"))
  if (!all(file.exists(files))) return(FALSE)
  lines <- readLines(files[3L])
  want <- setNames(sub("  .*$", "", lines), sub("^[0-9a-f]+  ", "", lines))
  got <- vapply(files[1:2], io$file_sha256, "")
  if (!identical(unname(want[basename(files[1:2])]), unname(got))) return(FALSE)
  old <- readRDS(files[1L])
  blocks <- c("COMMON", "GRID", "GLMNET", "F2")
  same <- identical(old$source_tree_sha256, ctx$code$tree) && identical(old$rows$run_id[1], ctx$run_id) &&
    identical(old$input$file, ctx$hash$file) && identical(old$settings[blocks], settings[blocks])
  if (!same) stop("existing complete output was produced in a different context: ", prefix)
  TRUE
}

run_one <- function(d, scale_key, row, settings, engine, io, ctx) {
  method_id <- row$method_id
  case_id <- paste0(d$dataset_id, "_", scale_key)
  outdir <- file.path(ctx$out, ctx$run_id, sprintf("p%04d", d$p), case_id)
  dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
  prefix <- file.path(outdir, method_id)
  # One writer per (run, case, method): an exclusive lock directory (Oct-14 pattern).
  lock <- paste0(prefix, ".lock")
  if (!dir.create(lock, showWarnings = FALSE)) stop("lock exists (another writer or a crashed attempt): ", lock)
  on.exit(unlink(lock, recursive = TRUE), add = TRUE)
  if (done_is_valid(prefix, io, ctx, settings)) { cat(case_id, method_id, "skip (valid .done)\n"); return(invisible("skip")) }
  unlink(paste0(prefix, ".done"))   # an incomplete earlier attempt: invalidate its marker before rewriting

  X <- d$X; y <- unname(d$Y[, scale_key]); foldid <- d$foldid
  settings$variant <- row$variant
  fn <- get(row$fn, envir = engine, inherits = FALSE)
  extra_cols <- get0(paste0(method_id, "_EXTRA_COLS"), envir = engine, inherits = FALSE,
                     ifnotfound = character())

  # RNG (§III.3.0): reset immediately before every method call.
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(d$method_seed)
  started <- io$utc_now(); t0 <- io$elapsed()
  fit <- tryCatch(fn(X, y, foldid, d$method_seed, settings), error = function(e) {
    msg <- conditionMessage(e)
    list(rules = io$fail_rows(row, msg, extra_cols), pip = NULL, beta = rep(NA_real_, ncol(X)),
         converged = FALSE, diagnostics = list(error = msg),
         warnings = character(), messages = character(), outer_error = msg)
  })
  runtime <- io$elapsed() - t0; finished <- io$utc_now()

  r <- fit$rules
  if (!identical(r$rule_id, row$rule_ids[[1L]]) || !identical(r$role, row$roles[[1L]]))
    stop("wrapper rule rows differ from the registry for ", method_id)
  nr <- nrow(r)
  NAs <- function(v) rep(v, nr)
  out <- data.frame(
    study = settings$COMMON$study, run_id = ctx$run_id, source_sha256 = ctx$code$tree,
    regime = if (d$p >= 500L) "H" else "L", p = d$p, scenario = d$scenario,
    replicate = d$replicate, scale_key = scale_key,
    scale = unname(settings$COMMON$scale_keys[[scale_key]]),
    dataset_id = d$dataset_id, case_id = case_id,
    data_seed = d$data_seed, fold_seed = d$fold_seed, method_seed = d$method_seed,
    inputs_sha256 = ctx$hash$file, x_sha256 = ctx$hash$x, y_sha256 = ctx$hash$y[[scale_key]],
    fold_sha256 = ctx$hash$fold,
    method_id = method_id, method_label = row$method_label, package = row$package,
    package_version = as.character(utils::packageVersion(row$package)),
    rule_id = r$rule_id, role = r$role, status = r$status,
    converged = r$converged, diag_flag = r$diag_flag, diag_codes = r$diag_codes,
    n_warnings = length(fit$warnings),
    warnings = paste(fit$warnings, collapse = " | "),
    messages = paste(fit$messages, collapse = " | "),
    error = r$error,
    k = r$k, support = r$support, support_audit = r$support_audit,
    stringsAsFactors = FALSE)
  # Truth columns: filled by the scoring step only (§IV.1.2).
  for (nm in c("tp", "fp", "fn", "exact", "error_type")) out[[nm]] <- NAs(NA)
  for (nm in sprintf("sel_a%02d", 1:14)) out[[nm]] <- NAs(NA)
  for (nm in sprintf("pip_a%02d", 1:14)) out[[nm]] <- NAs(NA)
  out$max_pip_null <- NAs(NA)
  for (nm in extra_cols) out[[nm]] <- r[[nm]]
  out$runtime_s <- runtime; out$host <- ctx$host
  out$slurm_job_id <- Sys.getenv("SLURM_JOB_ID"); out$slurm_array_task_id <- Sys.getenv("SLURM_ARRAY_TASK_ID")
  out$started_utc <- started; out$finished_utc <- finished

  result <- list(schema_version = SCHEMA_VERSION, case_id = case_id, dataset_id = d$dataset_id,
                 method_id = method_id, rows = out, beta = fit$beta, pip = fit$pip,
                 converged = fit$converged, diagnostics = fit$diagnostics,
                 warnings = fit$warnings, messages = fit$messages,
                 outer_error = fit$outer_error, runtime_s = runtime,
                 input = c(list(path = ctx$input_path), ctx$hash, list(manifest = ctx$manifest)),
                 source_hashes = ctx$code$files, source_tree_sha256 = ctx$code$tree,
                 settings = settings, environment = ctx$env,
                 started_utc = started, finished_utc = finished)
  io$atomic_write(paste0(prefix, ".rds"), function(f) saveRDS(result, f, compress = "xz"))
  io$atomic_write(paste0(prefix, ".csv"), function(f) utils::write.csv(out, f, row.names = FALSE, na = "NA"))
  paths <- paste0(prefix, c(".rds", ".csv"))
  hashes <- vapply(paths, io$file_sha256, "")
  io$atomic_write(paste0(prefix, ".sha256"),
                  function(f) writeLines(paste(hashes, basename(paths), sep = "  "), f))
  io$atomic_write(paste0(prefix, ".done"), function(f)
    writeLines(c(paste("statuses", paste(out$status, collapse = ",")),
                 sprintf("runtime_s %.3f", runtime), paste("finished_utc", finished)), f))
  cat(sprintf("%s %s %s runtime %.2f s\n", case_id, method_id,
              paste(out$rule_id, out$status, collapse = " "), runtime))
  invisible("done")
}

main <- function(args) {
  a <- parse_args(args)
  code_dir <- if (is.null(a$code_dir)) script_dir() else normalizePath(a$code_dir, mustWork = TRUE)
  cfg <- new.env(parent = baseenv())
  sys.source(file.path(code_dir, "config.R"), envir = cfg)
  settings <- cfg$make_settings("primary")
  .libPaths(c(settings$COMMON$study_lib, .Library))     # sealed study library first
  if (!identical(R.version.string, "R version 4.5.2 (2025-10-31)")) stop("unexpected R: ", R.version.string)
  io <- new.env(parent = globalenv())
  sys.source(file.path(code_dir, "common.R"), envir = io)

  # Library and threads.
  assert_study_library(c("glmnet", "digest"), settings$COMMON$study_lib)
  threads <- Sys.getenv(c("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"))
  if (!all(threads == "1")) stop("thread variables must all be 1: ", paste(names(threads), threads, collapse = ", "))

  # Fitting environment: parent is the stats namespace (Oct-14 run_case.R); it receives only
  # function definitions, never data or truth.
  engine <- new.env(parent = asNamespace("stats"))
  for (f in FIT_FILES) sys.source(file.path(code_dir, f), envir = engine)

  # Input: inputs/ only.
  input_path <- normalizePath(a$input, mustWork = TRUE)
  if (grepl("/truth/", input_path, fixed = TRUE) || !grepl("/inputs/", input_path, fixed = TRUE))
    stop("the runner reads only files under an inputs/ directory: ", input_path)
  d <- readRDS(input_path)
  for (nm in c("X", "Y", "foldid", "dataset_id", "data_seed", "fold_seed", "method_seed", "p",
               "scenario", "replicate"))
    if (is.null(d[[nm]])) stop("input lacks ", nm)
  if (!all(a$scales %in% colnames(d$Y)) || !all(a$scales %in% names(settings$COMMON$scale_keys)))
    stop("unknown scale key")
  hash <- list(file = io$file_sha256(input_path), x = io$f64_sha256(d$X),
               y = setNames(lapply(a$scales, function(s) io$f64_sha256(d$Y[, s])), a$scales),
               fold = io$f64_sha256(d$foldid))
  manifest <- NULL
  if (!is.null(a$manifest)) {
    mf <- utils::read.csv(a$manifest, stringsAsFactors = FALSE, colClasses = "character")
    m <- mf[mf$dataset_id == d$dataset_id, , drop = FALSE]
    if (nrow(m) != 1L) stop("dataset not in manifest: ", d$dataset_id)
    ok <- c(file = m$file_sha256 == hash$file, x = m$x_sha256 == hash$x,
            fold = m$foldid_sha256 == hash$fold,
            setNames(vapply(a$scales, function(s) m[[paste0("y_", s, "_sha256")]] == hash$y[[s]], TRUE),
                     paste0("y_", a$scales)),
            method_seed = as.integer(m$method_seed) == d$method_seed)
    if (!all(ok)) stop("input hash mismatch against manifest: ", paste(names(ok)[!ok], collapse = ","))
    manifest <- list(path = normalizePath(a$manifest), checks = ok)
  }
  if (d$method_seed != d$data_seed + settings$METHOD_SEED_OFFSET) stop("method_seed != data_seed + offset")

  methods <- settings$METHODS
  if (!is.null(a$methods)) methods <- methods[methods$method_id %in% a$methods, , drop = FALSE]
  if (!nrow(methods)) stop("no registered method selected")

  ctx <- list(out = a$out, run_id = a$run_id, input_path = input_path, hash = hash,
              manifest = manifest, code = code_hashes(code_dir, io),
              host = Sys.info()[["nodename"]],
              env = list(R = R.version.string, session = utils::capture.output(utils::sessionInfo()),
                         lib_paths = .libPaths(), blas = extSoftVersion()[["BLAS"]],
                         lapack = La_library(), threads = threads,
                         packages = vapply(c("glmnet", "digest"), function(p)
                           as.character(utils::packageVersion(p)), ""),
                         package_paths = vapply(c("glmnet", "digest"), find.package, ""),
                         slurm = Sys.getenv(c("SLURM_JOB_ID", "SLURM_ARRAY_JOB_ID",
                                              "SLURM_ARRAY_TASK_ID", "SLURM_JOB_NODELIST")),
                         command = commandArgs(), code_dir = code_dir))
  for (scale_key in a$scales) for (i in seq_len(nrow(methods)))
    run_one(d, scale_key, methods[i, , drop = FALSE], settings, engine, io, ctx)
  invisible(0L)
}

if (sys.nframe() == 0L) {
  status <- tryCatch({ main(commandArgs(trailingOnly = TRUE)); 0L },
                     error = function(e) { message("FATAL: ", conditionMessage(e)); 1L })
  quit(save = "no", status = status)
}
