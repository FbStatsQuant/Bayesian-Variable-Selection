#!/usr/bin/env Rscript
# run_case.R: runner for one dataset x the registered F3 method ids x one scale.
# Implements master §III.3.0 (registry loop, RNG, library check, one capture layer,
# files) and §IV.1.1-§IV.1.2 (per (case, method) files written atomically; rule-row schema).
# It opens only the inputs/ file it is given (and, optionally, the inputs manifest).
#
# Usage:
#   Rscript run_case.R --input <inputs/pXXXX/<dataset_id>.rds> --out <output root>
#                      --run-id <run id> [--scale c100] [--methods F3] [--manifest <csv>]
# Writes <out>/results/<run_id>/p{pppp}/<case_id>/<method_id>.{rds,csv,sha256,done}.

SCORING_COLS <- c("tp", "fp", "fn", "exact", "error_type",
                  sprintf("sel_a%02d", 1:14), sprintf("pip_a%02d", 1:14), "max_pip_null")
SCHEMA_HEAD <- c("study", "run_id", "source_sha256",
                 "regime", "p", "scenario", "replicate", "scale_key", "scale", "dataset_id", "case_id",
                 "data_seed", "fold_seed", "method_seed",
                 "inputs_sha256", "x_sha256", "y_sha256", "fold_sha256",
                 "method_id", "method_label", "package", "package_version",
                 "rule_id", "role", "status",
                 "converged", "diag_flag", "diag_codes", "n_warnings", "warnings", "messages", "error",
                 "k", "support", "support_audit", SCORING_COLS,
                 "runtime_s", "host", "slurm_job_id", "slurm_array_task_id",
                 "started_utc", "finished_utc")
CODE_FILES <- c("config.R", "common.R", "methods/glmnet_helpers.R", "methods/fit_F3_alasso.R",
                "run_case.R")
FIT_FILES <- c("common.R", "methods/glmnet_helpers.R", "methods/fit_F3_alasso.R")

parse_args <- function(args) {
  out <- list(scale = "c100", methods = NULL, manifest = NULL)
  i <- 1L
  while (i <= length(args)) {
    if (!startsWith(args[i], "--") || i == length(args)) stop("bad argument list near ", args[i])
    out[[gsub("-", "_", sub("^--", "", args[i]))]] <- args[i + 1L]
    i <- i + 2L
  }
  for (k in c("input", "out", "run_id")) if (is.null(out[[k]])) stop("missing --", k)
  if (!is.null(out$methods)) out$methods <- strsplit(out$methods, ",", fixed = TRUE)[[1L]]
  out
}

script_dir <- function() {
  f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE))
  if (length(f) != 1L) stop("run_case.R must be run with Rscript")
  dirname(normalizePath(f, mustWork = TRUE))
}

# Loads the configuration and the fitting code. The fitting code is sourced into an
# environment whose parent is the stats namespace (Oct-14 run_case.R), so it cannot see
# the runner's local variables.
load_code <- function(code_root) {
  cfg <- new.env(parent = globalenv())
  sys.source(file.path(code_root, "config.R"), envir = cfg)
  engine <- new.env(parent = asNamespace("stats"))
  for (f in FIT_FILES) sys.source(file.path(code_root, f), envir = engine)
  list(cfg = cfg, engine = engine)
}

check_library <- function(study_lib, pkgs) {
  lib <- normalizePath(study_lib, mustWork = TRUE)
  for (pkg in pkgs) {
    where <- normalizePath(find.package(pkg), mustWork = TRUE)
    if (!startsWith(where, paste0(lib, "/"))) stop(pkg, " is loaded from ", where, ", not ", lib)
  }
  invisible(TRUE)
}

source_hashes <- function(code_root, digest_fn) {
  h <- vapply(CODE_FILES, function(f) digest_fn(file.path(code_root, f)), "")
  tree <- digest::digest(paste(names(h), h, sep = "  ", collapse = "\n"), algo = "sha256",
                         serialize = FALSE)
  list(files = data.frame(path = names(h), sha256 = unname(h), stringsAsFactors = FALSE), tree = tree)
}

# One fit inside the runner's outer capture: an uncaught error (assertion, version
# check) becomes the registered failed rows with the message in `error` (§III.3.0).
run_one_fit <- function(meth, engine, X, y, foldid, seed, settings) {
  fn <- get(meth$fn, envir = engine, inherits = FALSE)
  s <- settings; s$variant <- meth$variant
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(seed)
  t0 <- engine$elapsed()
  res <- tryCatch(fn(X, y, foldid, seed, s), error = function(e)
    list(rules = engine$fail_rows(meth, conditionMessage(e)), pip = NULL,
         beta = rep(NA_real_, ncol(X)), converged = FALSE,
         diagnostics = list(error = conditionMessage(e)), warnings = character(),
         messages = character()))
  res$runtime_s <- engine$elapsed() - t0
  res
}

# Builds the §IV.1.2 CSV rows for one fit.
build_rows <- function(res, meth, case, prov, compute) {
  r <- res$rules
  n <- nrow(r)
  out <- data.frame(study = rep(prov$study, n), stringsAsFactors = FALSE)
  out$run_id <- prov$run_id; out$source_sha256 <- prov$source_sha256
  for (k in c("regime", "p", "scenario", "replicate", "scale_key", "scale", "dataset_id",
              "case_id", "data_seed", "fold_seed", "method_seed", "inputs_sha256", "x_sha256",
              "y_sha256", "fold_sha256")) out[[k]] <- case[[k]]
  out$method_id <- meth$method_id; out$method_label <- meth$method_label
  out$package <- meth$package; out$package_version <- meth$pkg_version
  out$rule_id <- r$rule_id; out$role <- r$role; out$status <- r$status
  out$converged <- r$converged; out$diag_flag <- r$diag_flag; out$diag_codes <- r$diag_codes
  out$n_warnings <- length(res$warnings)
  out$warnings <- paste(res$warnings, collapse = " | ")
  out$messages <- paste(res$messages, collapse = " | ")
  out$error <- r$error
  out$k <- r$k; out$support <- r$support; out$support_audit <- r$support_audit
  for (k in SCORING_COLS) out[[k]] <- NA
  out$runtime_s <- res$runtime_s
  for (k in c("host", "slurm_job_id", "slurm_array_task_id", "started_utc", "finished_utc"))
    out[[k]] <- compute[[k]]
  extra <- meth$extra_cols[[1L]]
  for (k in extra) out[[k]] <- r[[k]]
  stopifnot(identical(names(out), c(SCHEMA_HEAD, extra)))
  out
}

# A completed (case, method) has .done and a .sha256 listing exactly <method>.rds and
# <method>.csv, both present with matching hashes.
# When `expect` is given (run_id, case_id, inputs_sha256, source_sha256), an intact result must
# also belong to this run, case, input file and code (Astra finding 2); an intact result that
# does not is an error, never a silent skip or overwrite.
done_is_valid <- function(prefix, engine, expect = NULL) {
  if (!file.exists(paste0(prefix, ".done")) || !file.exists(paste0(prefix, ".sha256"))) return(FALSE)
  parts <- strsplit(readLines(paste0(prefix, ".sha256")), "  ", fixed = TRUE)
  if (length(parts) != 2L || any(lengths(parts) != 2L)) return(FALSE)
  names_listed <- vapply(parts, `[`, "", 2L)
  if (!setequal(names_listed, paste0(basename(prefix), c(".rds", ".csv")))) return(FALSE)
  intact <- all(vapply(parts, function(x) {
    f <- file.path(dirname(prefix), x[2L])
    file.exists(f) && identical(engine$file_sha256(f), x[1L])
  }, TRUE))
  if (!intact || is.null(expect)) return(intact)
  rows <- utils::read.csv(paste0(prefix, ".csv"), stringsAsFactors = FALSE,
                          colClasses = c(support = "character"))
  for (k in names(expect))
    if (!all(rows[[k]] == expect[[k]]))
      stop("existing result ", prefix, " has a different ", k, "; refusing to skip or overwrite")
  TRUE
}

main <- function(args) {
  a <- parse_args(args)
  code_root <- script_dir()
  code <- load_code(code_root)
  cfg <- code$cfg; engine <- code$engine
  .libPaths(c(cfg$STUDY_LIB, .Library))
  check_library(cfg$STUDY_LIB, c("glmnet", "digest"))
  # Load every namespace the fit uses before any timer starts, so runtime_s excludes loading.
  for (pkg in c("glmnet", "Matrix", "digest")) loadNamespace(pkg)
  threads <- Sys.getenv(c("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"))
  if (!all(threads == "1")) stop("thread variables must all be 1")
  settings <- cfg$study_settings("primary")
  methods <- settings$METHODS
  if (!is.null(a$methods)) {
    if (length(setdiff(a$methods, methods$method_id))) stop("unregistered method id")
    methods <- methods[methods$method_id %in% a$methods, , drop = FALSE]
  }

  input_path <- normalizePath(a$input, mustWork = TRUE)
  inp <- readRDS(input_path)
  X <- inp$X; foldid <- inp$foldid
  if (!a$scale %in% colnames(inp$Y)) stop("unknown scale key ", a$scale)
  y <- unname(inp$Y[, a$scale])
  if (inp$method_seed != inp$data_seed + settings$METHOD_SEED_OFFSET) stop("method seed mismatch")
  case <- list(regime = if (inp$p %in% c(500L, 1000L)) "H" else "L", p = inp$p,
               scenario = inp$scenario, replicate = inp$replicate, scale_key = a$scale,
               scale = unname(inp$scales[[a$scale]]), dataset_id = inp$dataset_id,
               case_id = paste0(inp$dataset_id, "_", a$scale),
               data_seed = inp$data_seed, fold_seed = inp$fold_seed, method_seed = inp$method_seed,
               inputs_sha256 = engine$file_sha256(input_path), x_sha256 = engine$f64_sha256(X),
               y_sha256 = engine$f64_sha256(y), fold_sha256 = engine$f64_sha256(foldid))
  if (!is.null(a$manifest)) {
    man <- utils::read.csv(a$manifest, stringsAsFactors = FALSE)
    row <- man[man$dataset_id == inp$dataset_id, , drop = FALSE]
    if (nrow(row) != 1L) stop("dataset not in manifest")
    if (row$file_sha256 != case$inputs_sha256 || row$x_sha256 != case$x_sha256 ||
        row$foldid_sha256 != case$fold_sha256 ||
        row[[paste0("y_", a$scale, "_sha256")]] != case$y_sha256)
      stop("input hashes differ from the manifest")
  }
  src <- source_hashes(code_root, engine$file_sha256)
  prov <- list(study = "bench20261019", run_id = a$run_id, source_sha256 = src$tree)
  env_info <- list(
    session_info = utils::capture.output(utils::sessionInfo()), lib_paths = .libPaths(),
    glmnet_path = find.package("glmnet"), rng_kind = RNGkind(), threads = threads,
    host = Sys.info()[["nodename"]], la_library = La_library(),
    blas = tryCatch(extSoftVersion()[["BLAS"]], error = function(e) NA_character_),
    command = commandArgs(), input_path = input_path)

  outdir <- file.path(a$out, "results", a$run_id, sprintf("p%04d", inp$p), case$case_id)
  dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
  exit <- 0L
  for (i in seq_len(nrow(methods))) {
    meth <- methods[i, , drop = FALSE]
    prefix <- file.path(outdir, meth$method_id)
    expect <- list(run_id = a$run_id, case_id = case$case_id, method_id = meth$method_id,
                   inputs_sha256 = case$inputs_sha256, source_sha256 = src$tree)
    if (done_is_valid(prefix, engine, expect)) { cat(case$case_id, meth$method_id, "already done\n"); next }
    started <- engine$utc_now()
    res <- run_one_fit(meth, engine, X, y, foldid, inp$method_seed, settings)
    compute <- list(host = env_info$host, slurm_job_id = Sys.getenv("SLURM_JOB_ID"),
                    slurm_array_task_id = Sys.getenv("SLURM_ARRAY_TASK_ID"),
                    started_utc = started, finished_utc = engine$utc_now())
    rows <- build_rows(res, meth, case, prov, compute)
    status <- if (all(rows$status == "failed")) "fit_failed" else
      if (any(rows$status == "failed")) "rule_failed" else
      if (any(rows$status == "warning")) "warning" else "ok"
    result <- list(schema_version = 1L, prov = prov, case = case, method = meth, rows = rows,
                   fit = res, source_files = src$files, environment = env_info,
                   settings = settings, compute = compute)
    engine$atomic_write(paste0(prefix, ".rds"),
                        function(p) saveRDS(result, p, compress = "xz", version = 3))
    engine$atomic_write(paste0(prefix, ".csv"),
                        function(p) utils::write.csv(rows, p, row.names = FALSE, na = "NA"))
    paths <- paste0(prefix, c(".rds", ".csv"))
    hashes <- vapply(paths, engine$file_sha256, "")
    engine$atomic_write(paste0(prefix, ".sha256"), function(p)
      writeLines(paste(hashes, basename(paths), sep = "  "), p))
    engine$atomic_write(paste0(prefix, ".done"), function(p)
      writeLines(c(paste("status", status), paste("runtime_s", format(res$runtime_s, digits = 6)),
                   paste("finished_utc", compute$finished_utc)), p))
    cat(case$case_id, meth$method_id, status, "runtime_s", format(res$runtime_s, digits = 4), "\n")
  }
  exit
}

if (sys.nframe() == 0L) {
  status <- tryCatch(main(commandArgs(trailingOnly = TRUE)), error = function(e) {
    message("FATAL: ", conditionMessage(e)); 1L
  })
  quit(save = "no", status = status)
}
