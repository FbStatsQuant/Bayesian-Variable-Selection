# run_case.R -- runner for A2: one dataset x the registered A2 method ids at one scale.
# Implements master §III.3.0 (RNG, library, one capture layer, files) and §IV.1.1-§IV.1.2
# (per (case, method) files written atomically; rule-row schema).
# Fitting code is sourced into an environment whose parent is asNamespace("stats").
# The runner opens only the inputs/ file it is given (and the inputs manifest for hashes).
#
# Usage (NOTS, after module load GCC/14.3.0 R/4.5.2; OMP/OPENBLAS/MKL_NUM_THREADS=1):
#   Rscript run_case.R --input <.../dev/inputs/p0500/dev_p0500_S1_r001.rds> \
#     --manifest <.../dev/manifests/dev_inputs_manifest.csv> --out <results root> \
#     --run_id <id> [--scale c100] [--methods A2,SSL-RS]

STUDY_LIB <- "/projects/ml75/fb31/BVS/bench20261019/lib/R452"
FIT_SOURCES <- c("config.R", "common.R", "methods/fit_A2_ssl.R")
CODE_FILES  <- c(FIT_SOURCES, "run_case.R")

this_code_dir <- function() {
  f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE))
  if (length(f) == 1L) return(normalizePath(dirname(f)))
  if (nzchar(Sys.getenv("A2_CODE_DIR"))) return(normalizePath(Sys.getenv("A2_CODE_DIR")))
  stop("cannot determine the code directory; set A2_CODE_DIR")
}

# Source config, common and the wrapper into one environment (parent: stats namespace).
load_fit_env <- function(code_dir) {
  env <- new.env(parent = asNamespace("stats"))
  for (f in FIT_SOURCES) sys.source(file.path(code_dir, f), envir = env, keep.source = FALSE)
  env
}

# settings = the whole configuration list (§III.3.0); settings$variant is set per method.
build_settings <- function(env) {
  mget(c("METHOD_SEED_OFFSET", "PIP_THRESHOLD", "TEST_SEED", "COMMON", "A2", "A2RS", "METHODS",
         "STATUS_VALUES", "FLAG_CODES", "INFO_CODES", "RULE_ID_VALUES"), envir = env)
}

# Per-file SHA-256 and a tree hash (sha256 of the "hash  path" lines) of the code.
source_hashes <- function(code_dir) {
  h <- vapply(CODE_FILES, function(f) digest::digest(file = file.path(code_dir, f), algo = "sha256"), "")
  tree <- digest::digest(paste(sprintf("%s  %s", h, CODE_FILES), collapse = "\n"),
                         algo = "sha256", serialize = FALSE)
  list(files = h, tree = tree)
}

# §III.3.0 "Library": every package used must load from the sealed study library.
assert_study_library <- function(pkgs, lib = STUDY_LIB) {
  for (pkg in pkgs) {
    loc <- normalizePath(find.package(pkg))
    if (!startsWith(loc, normalizePath(lib)))
      stop("assert_study_library: ", pkg, " loaded from ", loc, ", not from ", lib)
  }
  invisible(TRUE)
}

# One method id on one case: RNG reset, outer tryCatch (one capture layer), timing.
run_method <- function(mrow, X, y, foldid, seed, settings, env) {
  rule_ids <- mrow$rule_ids[[1]]; roles <- mrow$roles[[1]]
  s <- settings; s$variant <- mrow$variant
  fn <- get(mrow$fn, envir = env, inherits = FALSE)
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(seed)
  started <- env$utc_now(); t0 <- env$elapsed()
  out <- tryCatch(fn(X, y, foldid, seed, s), error = function(e)
    list(rules = env$fail_rows(rule_ids, roles, NULL, paste("uncaught error:", conditionMessage(e))),
         pip = NULL, beta = rep(NA_real_, ncol(X)), converged = FALSE,
         diagnostics = list(), warnings = character(), messages = character()))
  runtime <- env$elapsed() - t0
  finished <- env$utc_now()
  if (!identical(out$rules$rule_id, unlist(rule_ids)) || !identical(out$rules$role, unlist(roles)))
    # Whole failure contract (§III.3.0): failed rows, beta NA, pip NULL, converged FALSE;
    # the wrapper's own return value is kept for audit only.
    out <- list(rules = env$fail_rows(rule_ids, roles, NULL, "wrapper rule rows do not match the METHODS registry"),
                pip = NULL, beta = rep(NA_real_, ncol(X)), converged = FALSE,
                diagnostics = list(unregistered_return = out), warnings = out$warnings, messages = out$messages)
  list(out = out, runtime = runtime, started = started, finished = finished)
}

# Assemble the §IV.1.2 rule rows for one fit.
build_rows <- function(res, mrow, meta, env) {
  r <- res$out$rules
  w <- res$out$warnings; m <- res$out$messages
  df <- data.frame(
    study = meta$study, run_id = meta$run_id, source_sha256 = meta$source_sha256,
    regime = meta$regime, p = meta$p, scenario = meta$scenario, replicate = meta$replicate,
    scale_key = meta$scale_key, scale = meta$scale, dataset_id = meta$dataset_id, case_id = meta$case_id,
    data_seed = meta$data_seed, fold_seed = meta$fold_seed, method_seed = meta$method_seed,
    inputs_sha256 = meta$inputs_sha256, x_sha256 = meta$x_sha256, y_sha256 = meta$y_sha256,
    fold_sha256 = meta$fold_sha256,
    method_id = mrow$method_id, method_label = mrow$method_label, package = mrow$package,
    package_version = as.character(utils::packageVersion(mrow$package)),
    rule_id = r$rule_id, role = r$role, status = r$status,
    converged = r$converged, diag_flag = r$diag_flag, diag_codes = r$diag_codes,
    n_warnings = length(w),
    warnings = if (length(w)) paste(w, collapse = " | ") else NA_character_,
    messages = if (length(m)) paste(m, collapse = " | ") else NA_character_,
    error = r$error, k = r$k, support = r$support, support_audit = r$support_audit,
    runtime_s = res$runtime, host = meta$host, slurm_job_id = meta$slurm_job_id,
    slurm_array_task_id = meta$slurm_array_task_id,
    started_utc = res$started, finished_utc = res$finished, stringsAsFactors = FALSE)
  for (col in env$SCORING_COLUMNS) df[[col]] <- NA          # filled by the scoring step only
  df[, env$RULE_ROW_SCHEMA]
}

# Write <method>.rds, .csv, .sha256 and finally .done (§IV.1.1), each atomically.
write_outputs <- function(case_dir, method_id, rows, rds_obj, env) {
  dir.create(case_dir, recursive = TRUE, showWarnings = FALSE)
  base <- file.path(case_dir, method_id)
  if (file.exists(paste0(base, ".done"))) stop("refusing to overwrite ", base, ".done")
  env$write_atomic(function(f) saveRDS(rds_obj, f, compress = FALSE), paste0(base, ".rds"))
  env$write_atomic(function(f) utils::write.csv(rows, f, row.names = FALSE, na = "NA"), paste0(base, ".csv"))
  sums <- sprintf("%s  %s", c(env$file_sha256(paste0(base, ".rds")), env$file_sha256(paste0(base, ".csv"))),
                  paste0(method_id, c(".rds", ".csv")))
  env$write_atomic(function(f) writeLines(sums, f), paste0(base, ".sha256"))
  env$write_atomic(function(f) writeLines(env$utc_now(), f), paste0(base, ".done"))
  invisible(base)
}

# A (case, method) output is valid when .done exists, .sha256 matches the current .rds and .csv,
# and the CSV has exactly the registered rule rows, each carrying this run, this code, this case,
# this method and this input (run_id, source_sha256, case_id, method_id, rule_id and the four
# input hashes), all non-missing; a copied, stale or malformed output is never skipped.
valid_done <- function(case_dir, method_id, env, expect, rule_ids) {
  base <- file.path(case_dir, method_id)
  f <- paste0(base, c(".rds", ".csv", ".sha256", ".done"))
  if (!all(file.exists(f))) return(FALSE)
  want <- sprintf("%s  %s", c(env$file_sha256(f[1]), env$file_sha256(f[2])), paste0(method_id, c(".rds", ".csv")))
  if (!identical(readLines(f[3]), want)) return(FALSE)
  rows <- tryCatch(utils::read.csv(f[2], stringsAsFactors = FALSE, colClasses = "character"), error = function(e) NULL)
  if (is.null(rows) || nrow(rows) != length(rule_ids) || !all(c(names(expect), "rule_id") %in% names(rows))) return(FALSE)
  if (!identical(rows$rule_id, unlist(rule_ids))) return(FALSE)
  ok <- vapply(names(expect), function(k) {
    v <- rows[[k]]; !anyNA(v) && all(v == expect[[k]])
  }, logical(1))
  isTRUE(all(ok))
}

# Read one inputs/ file and check it against the inputs manifest (file, X, y_c and fold hashes).
# manifest: a CSV file, or a directory of per-cell manifests <pppp>_S<s>_inputs.csv (production).
read_case <- function(input, manifest, scale_key, env) {
  if (!grepl("/inputs/", input, fixed = TRUE)) stop("read_case: fitting reads inputs/ files only")
  d <- readRDS(input)
  y <- unname(d$Y[, scale_key])
  meta <- list(inputs_sha256 = env$file_sha256(input), x_sha256 = env$f64_sha256(d$X),
               y_sha256 = env$f64_sha256(y), fold_sha256 = env$f64_sha256(d$foldid))
  if (!is.null(manifest)) {
    if (dir.exists(manifest)) manifest <- file.path(manifest, sprintf("p%04d_S%d_inputs.csv", d$p, d$scenario))
    man <- utils::read.csv(manifest, stringsAsFactors = FALSE)
    mr <- man[man$dataset_id == d$dataset_id, , drop = FALSE]
    if (nrow(mr) != 1L) stop("read_case: dataset ", d$dataset_id, " not in the manifest")
    chk <- c(file = mr$file_sha256 == meta$inputs_sha256, x = mr$x_sha256 == meta$x_sha256,
             y = mr[[paste0("y_", scale_key, "_sha256")]] == meta$y_sha256,
             fold = mr$foldid_sha256 == meta$fold_sha256)
    if (!all(chk)) stop("read_case: hash mismatch against the manifest: ", paste(names(chk)[!chk], collapse = ","))
  }
  list(d = d, y = y, hashes = meta)
}

# settings_hook (tests only): function(settings, method_id) returning modified settings.
# skip_valid (production): skip a (case, method) whose outputs are valid (valid_done); a .done
# with a non-matching .sha256 is removed and the case refitted.
run_case <- function(input, out_root, run_id, scale_key = "c100", method_ids = NULL,
                     manifest = NULL, code_dir = this_code_dir(), settings_hook = NULL, skip_valid = FALSE) {
  .libPaths(c(STUDY_LIB, .Library))
  env <- load_fit_env(code_dir)
  settings <- build_settings(env)
  # Every package namespace is loaded here, before any fit timer starts, so runtime_s excludes loading.
  stopifnot(requireNamespace("digest", quietly = TRUE), requireNamespace("SSLASSO", quietly = TRUE))
  assert_study_library(c("SSLASSO", "digest"))
  hashes <- source_hashes(code_dir)
  rc <- read_case(input, manifest, scale_key, env)
  d <- rc$d
  scale <- unname(d$scales[[scale_key]])
  if (is.null(method_ids)) method_ids <- settings$METHODS$method_id
  case_id <- paste0(d$dataset_id, "_", scale_key)
  case_dir <- file.path(out_root, run_id, sprintf("p%04d", d$p), case_id)
  meta <- c(list(study = settings$COMMON$study, run_id = run_id, source_sha256 = hashes$tree,
                 regime = settings$COMMON$regime, p = d$p, scenario = d$scenario, replicate = d$replicate,
                 scale_key = scale_key, scale = scale, dataset_id = d$dataset_id, case_id = case_id,
                 data_seed = d$data_seed, fold_seed = d$fold_seed, method_seed = d$method_seed,
                 host = Sys.info()[["nodename"]],
                 slurm_job_id = Sys.getenv("SLURM_JOB_ID", NA), slurm_array_task_id = Sys.getenv("SLURM_ARRAY_TASK_ID", NA)),
            rc$hashes)
  stopifnot(d$method_seed == d$data_seed + settings$METHOD_SEED_OFFSET)
  for (mid in method_ids) {
    mrow <- settings$METHODS[settings$METHODS$method_id == mid, , drop = FALSE]
    if (nrow(mrow) != 1L) stop("run_case: method id ", mid, " is not registered")
    if (skip_valid) {
      expect <- c(run_id = run_id, source_sha256 = hashes$tree, case_id = case_id, method_id = mid,
                  unlist(rc$hashes))
      if (valid_done(case_dir, mid, env, expect, mrow$rule_ids[[1]])) {
        cat(sprintf("%s %s skipped (valid outputs exist)\n", case_id, mid)); next
      }
      stale <- file.path(case_dir, paste0(mid, c(".done", ".sha256")))
      if (any(file.exists(stale))) { cat(sprintf("%s %s invalid or partial outputs: refitting\n", case_id, mid)); unlink(stale) }
    }
    s_m <- if (is.null(settings_hook)) settings else settings_hook(settings, mid)
    res <- run_method(mrow, d$X, rc$y, d$foldid, d$method_seed, s_m, env)
    rows <- build_rows(res, mrow, meta, env)
    rds_obj <- list(rows = rows, fit = res$out, runtime_s = res$runtime,
                    code = list(files = hashes$files, tree = hashes$tree),
                    session = list(R = R.version.string, SSLASSO = as.character(utils::packageVersion("SSLASSO")),
                                   blas = extSoftVersion()[["BLAS"]], lapack = La_library(),
                                   threads = Sys.getenv(c("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"))))
    write_outputs(case_dir, mid, rows, rds_obj, env)
    cat(sprintf("%s %s %s status=%s k=%s runtime=%.3fs codes=%s\n", case_id, mid, rows$rule_id, rows$status,
                rows$k, res$runtime, rows$diag_codes))
  }
  invisible(case_dir)
}

parse_args <- function(args) {
  out <- list()
  i <- 1L
  while (i <= length(args)) {
    key <- sub("^--", "", args[i]); out[[key]] <- args[i + 1L]; i <- i + 2L
  }
  out
}

if (sys.nframe() == 0L) {
  th <- Sys.getenv(c("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"))
  if (!all(th == "1")) stop("set OMP_NUM_THREADS = OPENBLAS_NUM_THREADS = MKL_NUM_THREADS = 1 (§III.3.0)")
  a <- parse_args(commandArgs(trailingOnly = TRUE))
  run_case(input = a$input, out_root = a$out, run_id = a$run_id,
           scale_key = if (is.null(a$scale)) "c100" else a$scale,
           method_ids = if (is.null(a$methods)) NULL else strsplit(a$methods, ",")[[1]],
           manifest = a$manifest)
}
