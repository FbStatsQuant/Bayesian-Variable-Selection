#!/usr/bin/env Rscript
# run_case.R -- runner for one dataset x the registered method ids at one scale (master §III.3.0,
# §IV.1.1, §IV.1.2). Opens only the inputs file it is given. Writes, per (case, method_id),
# <method_id>.{rds,csv,sha256,done} atomically under <out_root>/results/<run_id>/p{pppp}/<case_id>/.
#
# Usage:
#   Rscript --vanilla run_case.R --code-dir DIR --input FILE --scale c100 --out-root DIR --run-id ID
#                                [--manifest CSV] [--lib DIR] [--methods F1]   (--lib defaults to $BENCH_LIB; required)
# --manifest: the inputs manifest; when given, the input file and array hashes must match its row.
# --lib: sealed study library; every registered package must load from it (§III.3.0 "Library").

parse_args <- function(args) {
  out <- list(); i <- 1L
  while (i <= length(args)) {
    if (!startsWith(args[i], "--") || i == length(args)) stop("bad argument list at '", args[i], "'")
    out[[gsub("-", "_", sub("^--", "", args[i]))]] <- args[i + 1L]; i <- i + 2L
  }
  for (k in c("code_dir", "input", "scale", "out_root", "run_id"))
    if (is.null(out[[k]])) stop("missing --", gsub("_", "-", k))
  out
}

# Loads config.R into its own environment and returns it as the settings list (§III.3.0).
load_settings <- function(code_dir) {
  cfg <- new.env(parent = baseenv())
  sys.source(file.path(code_dir, "config.R"), envir = cfg)
  as.list(cfg, all.names = FALSE)
}

# Fitting environment: parent asNamespace("stats"), as in Oct-14 run_case.R. It holds the shared
# helpers and the method files; it never holds case metadata beyond the call arguments.
load_engine <- function(code_dir) {
  engine <- new.env(parent = asNamespace("stats"))
  for (f in c("common.R", file.path("methods", c("glmnet_helpers.R", "fit_F1_lasso.R"))))
    sys.source(file.path(code_dir, f), envir = engine)
  engine
}

source_files <- function(code_dir) {
  file.path(code_dir, c("config.R", "common.R", "methods/glmnet_helpers.R",
                        "methods/fit_F1_lasso.R", "run_case.R"))
}

# Tree hash: SHA-256 of the "sha256  relative-path" lines of the source files.
source_tree_sha256 <- function(code_dir, h) {
  files <- source_files(code_dir)
  lines <- paste(vapply(files, h$file_sha256, ""), sub(paste0("^", code_dir, "/?"), "", files), sep = "  ")
  list(per_file = data.frame(path = files, sha256 = vapply(files, h$file_sha256, ""), row.names = NULL),
       tree = digest::digest(paste(lines, collapse = "\n"), algo = "sha256", serialize = FALSE))
}

# Calls one registered method. The wrapper captures its own conditions; this outer tryCatch only turns
# an uncaught error into the registered failed rows (§III.3.0 "One capture layer").
call_method <- function(fn, X, y, foldid, seed, settings, methods, method_id, h) {
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(seed)   # §III.3.0 "RNG"
  tryCatch(fn(X, y, foldid, seed, settings), error = function(e)
    list(rules = h$fail_rows(methods, method_id), pip = NULL, beta = rep(NA_real_, ncol(X)),
         converged = methods$converged_on_failure[methods$method_id == method_id],
         diagnostics = list(), warnings = character(), messages = character(),
         error = paste("runner:", conditionMessage(e))))
}

# Checks the wrapper's return value against the registry and the rule-frame columns (§III.3.0).
check_result <- function(res, reg, p) {
  base <- c("rule_id", "role", "status", "support", "support_audit", "k", "converged",
            "diag_flag", "diag_codes")
  r <- res$rules
  stopifnot(is.data.frame(r), identical(names(r), c(base, reg$extra_cols[[1L]])),
            identical(r$rule_id, reg$rule_ids[[1L]]), identical(r$role, reg$roles[[1L]]),
            all(r$status %in% c("ok", "warning", "failed")),
            length(res$beta) == p, is.null(res$pip) || length(res$pip) == p)
  invisible(TRUE)
}

# Per-case lock: a directory created atomically, holding an owner token "<SLURM job id> <node> <pid> <usec>".
# It is held from the completion check through the commit and released only by its owner.
# Staleness: owner job equal to this job (cases of a task run sequentially, so an earlier runner of this task
# died), or owner job unknown to squeue ("Invalid job id"); a lock without a readable owner is stale only after
# 120 s; any other squeue failure counts as busy. Owner written outside SLURM (tests) counts as stale.
# Residual risk: two concurrent reruns reclaiming the same stale lock; prevented operationally (one submission).
lock_token <- function() {
  paste(Sys.getenv("SLURM_JOB_ID"), Sys.info()[["nodename"]], Sys.getpid(),
        format(as.numeric(Sys.time()) * 1e6, scientific = FALSE))
}
lock_is_stale <- function(lock) {
  own <- file.path(lock, "owner")
  tok <- if (file.exists(own)) tryCatch(readLines(own, n = 1L), error = function(e) character()) else character()
  if (!length(tok) || !nzchar(tok))
    return(isTRUE(difftime(Sys.time(), file.info(lock)$mtime, units = "secs") > 120))
  owner_job <- strsplit(tok, " ", fixed = TRUE)[[1]][1]
  me <- Sys.getenv("SLURM_JOB_ID")
  if (owner_job == "" || owner_job == me) return(TRUE)
  q <- suppressWarnings(system2("squeue", c("-h", "-j", owner_job), stdout = TRUE, stderr = TRUE))
  st <- attr(q, "status")
  if (!is.null(st) && st != 0) return(any(grepl("Invalid job id", q)))
  length(q) == 0L
}
acquire_lock <- function(lock) {
  for (attempt in 1:2) {
    if (dir.create(lock, showWarnings = FALSE)) {
      tok <- lock_token(); writeLines(tok, file.path(lock, "owner")); return(tok)
    }
    if (!lock_is_stale(lock)) return(NULL)
    unlink(lock, recursive = TRUE)
  }
  NULL
}
release_lock <- function(lock, tok) {
  own <- file.path(lock, "owner")
  if (file.exists(own) && identical(tryCatch(readLines(own, n = 1L), error = function(e) ""), tok))
    unlink(lock, recursive = TRUE)
}

# TRUE when <prefix>.{rds,csv,sha256,done} exist and the .sha256 lines match the rds and csv files.
outputs_valid <- function(prefix, h) {
  fs <- paste0(prefix, c(".rds", ".csv", ".sha256", ".done"))
  if (!all(file.exists(fs))) return(FALSE)
  sh <- tryCatch(utils::read.table(fs[3], col.names = c("sha", "file"), stringsAsFactors = FALSE),
                 error = function(e) NULL)
  if (is.null(sh) || !setequal(sh$file, basename(fs[1:2]))) return(FALSE)
  all(sh$sha == vapply(file.path(dirname(prefix), sh$file), h$file_sha256, ""))
}

run_case <- function(a) {
  code_dir <- normalizePath(a$code_dir, mustWork = TRUE)
  settings0 <- load_settings(code_dir)
  h <- new.env(parent = asNamespace("stats")); sys.source(file.path(code_dir, "common.R"), envir = h)
  COMMON <- settings0$COMMON; METHODS <- settings0$METHODS
  if (!is.null(a$methods)) METHODS <- METHODS[METHODS$method_id %in% strsplit(a$methods, ",")[[1L]], , drop = FALSE]
  if (!nrow(METHODS)) stop("no registered method selected")

  # library: every registered package (and digest) must come from the sealed study library
  # (--lib, else $BENCH_LIB; one of them is required)
  if (is.null(a$lib)) a$lib <- Sys.getenv("BENCH_LIB")
  if (!nzchar(a$lib)) stop("the study library is required: pass --lib or set BENCH_LIB")
  {
    lib <- normalizePath(a$lib, mustWork = TRUE)
    .libPaths(c(lib, .Library))
    for (pkg in unique(c(METHODS$package, "digest")))
      if (!startsWith(normalizePath(find.package(pkg)), paste0(lib, "/")))
        stop("package ", pkg, " is not loaded from the study library ", lib)
  }
  for (v in c("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"))
    if (Sys.getenv(v) != "1") stop(v, " must be 1")

  # inputs (only this file is opened)
  input <- normalizePath(a$input, mustWork = TRUE)
  d <- readRDS(input)
  scale_key <- a$scale
  if (!scale_key %in% names(COMMON$scale_keys)) stop("unknown scale key ", scale_key)
  X <- d$X; y <- unname(d$Y[, scale_key]); foldid <- d$foldid; p <- ncol(X)
  stopifnot(d$method_seed == d$data_seed + settings0$METHOD_SEED_OFFSET)
  hashes <- list(inputs_sha256 = h$file_sha256(input), x_sha256 = h$f64_sha256(X),
                 y_sha256 = h$f64_sha256(y), fold_sha256 = h$f64_sha256(foldid))
  if (!is.null(a$manifest)) {
    man <- utils::read.csv(a$manifest, stringsAsFactors = FALSE, colClasses = "character")
    row <- man[man$dataset_id == d$dataset_id, , drop = FALSE]
    stopifnot(nrow(row) == 1L, row$file_sha256 == hashes$inputs_sha256, row$x_sha256 == hashes$x_sha256,
              row[[paste0("y_", scale_key, "_sha256")]] == hashes$y_sha256,
              row$foldid_sha256 == hashes$fold_sha256)
  }
  case_id <- paste0(d$dataset_id, "_", scale_key)                 # §IV.1.1 (dev ids carry dev_)
  outdir <- file.path(a$out_root, "results", a$run_id, sprintf("p%04d", p), case_id)
  dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
  src <- source_tree_sha256(code_dir, h)
  engine <- load_engine(code_dir)
  # preload the package namespaces so that first-call load time is not counted in runtime_s
  for (pkg in unique(METHODS$package)) loadNamespace(pkg)

  for (j in seq_len(nrow(METHODS))) {
    reg <- METHODS[j, , drop = FALSE]; mid <- reg$method_id
    prefix <- file.path(outdir, mid)
    # idempotent reruns: a (case, method) with a .done whose .sha256 verifies is skipped; a .done with
    # missing or mismatching files is an error (never overwritten); without .done the case is (re)fitted
    lock <- paste0(prefix, ".lock")
    tok <- acquire_lock(lock)
    if (is.null(tok)) stop("case is locked by an active job: ", lock)
    if (file.exists(paste0(prefix, ".done"))) {
      if (!outputs_valid(prefix, h)) stop("existing .done but outputs do not verify; not overwriting: ", prefix)
      old <- utils::read.csv(paste0(prefix, ".csv"), stringsAsFactors = FALSE, colClasses = "character")
      need <- c("rule_id", "source_sha256", "run_id", "inputs_sha256", "x_sha256", "y_sha256", "fold_sha256",
                "method_seed", "scale_key")
      same <- all(need %in% names(old)) && nrow(old) == length(reg$rule_ids[[1L]]) &&
        identical(old$rule_id, reg$rule_ids[[1L]]) && all(old$source_sha256 == src$tree) && all(old$run_id == a$run_id) &&
        all(old$inputs_sha256 == hashes$inputs_sha256) && all(old$x_sha256 == hashes$x_sha256) &&
        all(old$y_sha256 == hashes$y_sha256) && all(old$fold_sha256 == hashes$fold_sha256) &&
        all(old$method_seed == as.character(d$method_seed)) && all(old$scale_key == scale_key)
      release_lock(lock, tok)
      if (!same) stop("existing outputs belong to a different computation (source, run, inputs or seed); not overwriting: ", prefix)
      cat(case_id, mid, "skip: valid outputs exist\n"); next
    }
    settings <- settings0; settings$variant <- reg$variant
    started <- h$utc_now(); t0 <- proc.time()[["elapsed"]]
    res <- call_method(engine[[reg$fn]], X, y, foldid, d$method_seed, settings, METHODS, mid, h)
    runtime <- h$elapsed(t0); finished <- h$utc_now()
    check_result(res, reg, p)

    # §IV.1.2 rows: provenance, design, seeds, hashes, method, rule frame, diagnostics, scoring (NA), compute
    r <- res$rules; nr <- nrow(r)
    rows <- data.frame(study = COMMON$study, run_id = a$run_id, source_sha256 = src$tree,
                       regime = COMMON$regime, p = p, scenario = d$scenario, replicate = d$replicate,
                       scale_key = scale_key, scale = unname(COMMON$scale_keys[[scale_key]]),
                       dataset_id = d$dataset_id, case_id = case_id,
                       data_seed = d$data_seed, fold_seed = d$fold_seed, method_seed = d$method_seed,
                       hashes, method_id = mid, method_label = reg$method_label,
                       package = reg$package, package_version = reg$pkg_version,
                       stringsAsFactors = FALSE)[rep(1L, nr), , drop = FALSE]
    rows <- cbind(rows, r[, c("rule_id", "role", "status", "converged", "diag_flag", "diag_codes")])
    rows$n_warnings <- length(res$warnings)
    rows$warnings <- paste(res$warnings, collapse = " | ")
    rows$messages <- paste(res$messages, collapse = " | ")
    rows$error <- if (is.na(res$error)) "" else res$error
    rows <- cbind(rows, r[, c("k", "support", "support_audit")])
    for (cc in c("tp", "fp", "fn", "exact", "error_type", sprintf("sel_a%02d", 1:14),
                 sprintf("pip_a%02d", 1:14), "max_pip_null")) rows[[cc]] <- NA
    rows$runtime_s <- runtime
    rows$host <- Sys.info()[["nodename"]]
    rows$slurm_job_id <- Sys.getenv("SLURM_JOB_ID")
    rows$slurm_array_task_id <- Sys.getenv("SLURM_ARRAY_TASK_ID")
    rows$started_utc <- started; rows$finished_utc <- finished
    rows <- cbind(rows, r[, reg$extra_cols[[1L]], drop = FALSE])
    rownames(rows) <- NULL

    obj <- list(schema_version = 1L, rows = rows, beta = res$beta, pip = res$pip,
                converged = res$converged, diagnostics = res$diagnostics,
                warnings = res$warnings, messages = res$messages, error = res$error,
                case = list(dataset_id = d$dataset_id, case_id = case_id, scale_key = scale_key,
                            input = input, hashes = hashes),
                config = settings, source = src,
                environment = list(R = R.version.string, packages = vapply(unique(c(reg$package, "digest")),
                                   function(x) as.character(utils::packageVersion(x)), ""),
                                   lib_paths = .libPaths(), blas = extSoftVersion()[["BLAS"]],
                                   la_library = La_library(), host = Sys.info()[["nodename"]],
                                   RNGkind = RNGkind()))
    h$write_atomic(paste0(prefix, ".rds"), function(f) saveRDS(obj, f, compress = "xz"))
    h$write_atomic(paste0(prefix, ".csv"), function(f) utils::write.csv(rows, f, row.names = FALSE, na = "NA"))
    fs <- paste0(prefix, c(".rds", ".csv"))
    h$write_atomic(paste0(prefix, ".sha256"), function(f)
      writeLines(paste(vapply(fs, h$file_sha256, ""), basename(fs), sep = "  "), f))
    st <- if (all(rows$status == "failed")) "failed" else "ok"
    h$write_atomic(paste0(prefix, ".done"), function(f)
      writeLines(c(paste("fit_status", st), paste("finished_utc", finished)), f))
    release_lock(lock, tok)
    cat(case_id, mid, "runtime_s", sprintf("%.3f", runtime), "status", paste(rows$status, collapse = ","),
        "k", paste(rows$k, collapse = ","), "\n")
  }
  invisible(TRUE)
}

if (sys.nframe() == 0L) {
  status <- tryCatch({ run_case(parse_args(commandArgs(trailingOnly = TRUE))); 0L },
                     error = function(e) { message("FATAL: ", conditionMessage(e)); 1L })
  quit(save = "no", status = status)
}
