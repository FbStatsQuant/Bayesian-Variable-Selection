#!/usr/bin/env Rscript
# run_case.R: runner for one dataset x the registered method ids (this thread: F5) at the
# requested scales. Implements master §III.3.0 (fitting environment, RNG, library, one
# capture layer, files) and §IV.1.1-§IV.1.2 (atomic files, rule-row schema).
# Ported from Oct-14 scripts/run_case.R (atomic writes, separate fitting environment,
# environment record). It opens one inputs/ file and the inputs manifest only; it never
# opens truth/. Truth columns of §IV.1.2 are left NA here and filled by the scoring step.
#
# Usage (NOTS, after module load GCC/14.3.0; module load R/4.5.2):
#   Rscript --vanilla run_case.R --input <inputs/.../dev_p0500_S1_r001.rds> \
#     --manifest <manifests/dev_inputs_manifest.csv> --out-root <dir> --run-id <id> \
#     [--scales c100] [--methods F5] [--code-root <dir with config.R>]

SCHEMA_VERSION <- 1L
SCALE_VALUES <- c(c100 = 1, c075 = 0.75, c050 = 0.50, c035 = 0.35, c025 = 0.25)
CODE_FILES <- c("config.R", "common.R", "methods/fit_F5_abess.R", "run_case.R")

# ---- configuration and fitting environment ----

load_settings <- function(code_root) {
  cfg <- new.env(parent = baseenv())
  sys.source(file.path(code_root, "config.R"), envir = cfg)
  as.list(cfg)                                   # the whole configuration list (§III.3.0)
}

# Wrapper bodies live in an environment whose parent is the stats namespace (Oct-14).
load_engine <- function(code_root) {
  engine <- new.env(parent = asNamespace("stats"))
  sys.source(file.path(code_root, "common.R"), envir = engine)
  for (f in list.files(file.path(code_root, "methods"), pattern = "\\.R$", full.names = TRUE))
    sys.source(f, envir = engine)
  engine
}

use_study_library <- function(settings) {
  .libPaths(c(settings$STUDY_LIB, .Library))
  for (pkg in c(unique(settings$METHODS$package), "digest")) {
    loc <- normalizePath(find.package(pkg), mustWork = TRUE)
    if (!startsWith(loc, normalizePath(settings$STUDY_LIB, mustWork = TRUE)))
      stop("package ", pkg, " loaded from ", loc, ", not from the sealed study library")
    # Load the namespace now, so that runtime_s does not include the one-off namespace
    # load (about 1 s for abess + Matrix, dev diagnostic job 2275404).
    loadNamespace(pkg)
  }
  invisible(TRUE)
}

# ---- hashes and atomic IO ----

f64_sha256 <- function(x)       # float64 little-endian SHA-256 (the manifest convention)
  digest::digest(writeBin(as.double(as.vector(x)), raw(), endian = "little"),
                 algo = "sha256", serialize = FALSE)
file_sha256 <- function(path) digest::digest(file = path, algo = "sha256")

code_hashes <- function(code_root) {
  h <- vapply(file.path(code_root, CODE_FILES), file_sha256, "")
  tree <- digest::digest(paste(CODE_FILES, h, sep = "  ", collapse = "\n"),
                         algo = "sha256", serialize = FALSE)
  list(files = data.frame(path = CODE_FILES, sha256 = unname(h), stringsAsFactors = FALSE),
       tree = tree)
}

atomic_write <- function(path, writefun) {
  tmp <- paste0(path, ".tmp.", Sys.getpid()); on.exit(unlink(tmp), add = TRUE)
  writefun(tmp)
  if (!file.rename(tmp, path)) stop("atomic rename failed: ", path)
}

# Errors in the .sha256 sidecar of one (case, method): it must list exactly the RDS and the
# CSV of that method, each once, with well-formed hashes that match the files (Sol finding 2:
# an empty or partial sidecar must never certify a completed fit).
sidecar_errors <- function(prefix) {
  sc <- paste0(prefix, ".sha256")
  if (!file.exists(sc)) return("missing .sha256")
  parts <- strsplit(readLines(sc), "  ", fixed = TRUE)
  if (!all(lengths(parts) == 2L)) return("malformed .sha256 line")
  hashes <- vapply(parts, `[`, "", 1L); names <- vapply(parts, `[`, "", 2L)
  want <- paste0(basename(prefix), c(".rds", ".csv"))
  if (length(names) != 2L || !setequal(names, want)) return(".sha256 does not list exactly the RDS and CSV")
  if (!all(grepl("^[0-9a-f]{64}$", hashes))) return("malformed hash in .sha256")
  errs <- character()
  for (i in seq_along(names)) {
    f <- file.path(dirname(prefix), names[i])
    if (!file.exists(f)) errs <- c(errs, paste("missing", names[i]))
    else if (!identical(file_sha256(f), hashes[i])) errs <- c(errs, paste("sha256 mismatch for", names[i]))
  }
  errs
}

done_is_valid <- function(prefix)
  file.exists(paste0(prefix, ".done")) && !length(sidecar_errors(prefix))

# ---- inputs ----

read_inputs <- function(input_path, manifest_path) {
  d <- readRDS(input_path)
  man <- utils::read.csv(manifest_path, stringsAsFactors = FALSE, colClasses = "character")
  m <- man[man$dataset_id == d$dataset_id, , drop = FALSE]
  if (nrow(m) != 1L) stop("dataset ", d$dataset_id, " not in manifest exactly once")
  d$inputs_sha256 <- file_sha256(input_path)
  d$x_sha256 <- f64_sha256(d$X); d$fold_sha256 <- f64_sha256(d$foldid)
  if (!identical(d$inputs_sha256, m$file_sha256)) stop("input file hash differs from manifest")
  if (!identical(d$x_sha256, m$x_sha256)) stop("X hash differs from manifest")
  if (!identical(d$fold_sha256, m$foldid_sha256)) stop("foldid hash differs from manifest")
  if (as.integer(m$method_seed) != as.integer(d$method_seed)) stop("method_seed differs from manifest")
  d$manifest_row <- m
  d
}

# ---- one (case, method) ----

# RNG is reset to the method seed immediately before every method call (§III.3.0 RNG).
# The outer tryCatch only turns an uncaught error into the registered failed rows.
run_method <- function(engine, settings, mrow, X, y, foldid, method_seed) {
  st <- settings; st$variant <- mrow$variant
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(method_seed)
  t0 <- engine$elapsed()
  res <- tryCatch(engine[[mrow$fn]](X, y, foldid, method_seed, st), error = function(e)
    list(rules = engine$fail_rows(st, mrow$method_id,
                                  converged = if (isTRUE(mrow$converged_na)) NA else FALSE,
                                  diag_flag = NA),
         pip = NULL, beta = rep(NA_real_, ncol(X)),
         converged = if (isTRUE(mrow$converged_na)) NA else FALSE,
         diagnostics = list(), warnings = character(), messages = character(),
         error = paste("runner:", conditionMessage(e))))
  res$runtime_s <- engine$elapsed() - t0
  res
}

rule_csv_rows <- function(res, mrow, case, prov) {
  r <- res$rules
  extras <- mrow$extra_cols[[1L]]
  na_chr <- NA_character_
  out <- data.frame(
    study = prov$study, run_id = prov$run_id, source_sha256 = prov$source_sha256,
    regime = "H", p = case$p, scenario = case$scenario, replicate = case$replicate,
    scale_key = case$scale_key, scale = case$scale, dataset_id = case$dataset_id,
    case_id = case$case_id, data_seed = case$data_seed, fold_seed = case$fold_seed,
    method_seed = case$method_seed, inputs_sha256 = case$inputs_sha256,
    x_sha256 = case$x_sha256, y_sha256 = case$y_sha256, fold_sha256 = case$fold_sha256,
    method_id = mrow$method_id, method_label = mrow$method_label, package = mrow$package,
    package_version = mrow$pkg_version, rule_id = r$rule_id, role = r$role,
    status = r$status, converged = r$converged, diag_flag = r$diag_flag,
    diag_codes = r$diag_codes, n_warnings = length(res$warnings),
    warnings = if (length(res$warnings)) paste(res$warnings, collapse = " | ") else na_chr,
    messages = if (length(res$messages)) paste(res$messages, collapse = " | ") else na_chr,
    error = if (is.null(res$error)) na_chr else res$error,
    k = r$k, support = r$support, support_audit = r$support_audit,
    tp = NA_integer_, fp = NA_integer_, fn = NA_integer_, exact = NA, error_type = na_chr,
    stringsAsFactors = FALSE)
  for (a in sprintf("sel_a%02d", 1:14)) out[[a]] <- NA
  for (a in sprintf("pip_a%02d", 1:14)) out[[a]] <- NA_real_
  out$max_pip_null <- NA_real_
  out$runtime_s <- res$runtime_s
  out$host <- prov$host; out$slurm_job_id <- prov$slurm_job_id
  out$slurm_array_task_id <- prov$slurm_array_task_id
  out$started_utc <- prov$started_utc; out$finished_utc <- prov$finished_utc
  for (x in extras) out[[x]] <- r[[x]]
  out
}

utc_now <- function() format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC")

run_case <- function(input, manifest, out_root, run_id, scales = "c100", methods = NULL,
                     code_root) {
  code_root <- normalizePath(code_root, mustWork = TRUE)
  settings <- load_settings(code_root)
  use_study_library(settings)
  engine <- load_engine(code_root)
  hashes <- code_hashes(code_root)
  d <- read_inputs(input, manifest)
  reg <- settings$METHODS
  if (!is.null(methods)) reg <- reg[reg$method_id %in% methods, , drop = FALSE]
  if (!nrow(reg)) stop("no registered method selected")
  # Production dimensions, asserted once (§III.3.5 e step 3; canaries pass other sizes).
  if ("F5" %in% reg$method_id && !identical(settings$F5$sizes, 0:settings$COMMON$kmax_ebic))
    stop("F5$sizes must be 0:kmax_ebic in production")
  env <- list(session_info = utils::capture.output(utils::sessionInfo()),
              packages = vapply(c(unique(reg$package), "digest"), function(p)
                as.character(utils::packageVersion(p)), ""),
              lib_paths = .libPaths(), RNGkind = RNGkind(), host = Sys.info()[["nodename"]],
              threads = Sys.getenv(c("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                                     "BLIS_NUM_THREADS", "FLEXIBLAS_NUM_THREADS")),
              locale = Sys.getlocale(), blas = extSoftVersion()[["BLAS"]], lapack = La_library(),
              r_version = R.version.string,
              # where every loaded namespace came from (Astra prod finding 5)
              namespaces = vapply(sort(loadedNamespaces()), function(ns)
                tryCatch(getNamespaceInfo(ns, "path"), error = function(e) NA_character_), ""),
              command = commandArgs())
  status_lines <- character()
  for (sk in scales) {
    if (!sk %in% names(SCALE_VALUES)) stop("unknown scale ", sk)
    y <- unname(d$Y[, sk])
    case <- list(p = as.integer(d$p), scenario = as.integer(d$scenario),
                 replicate = as.integer(d$replicate), scale_key = sk,
                 scale = unname(SCALE_VALUES[[sk]]), dataset_id = d$dataset_id,
                 case_id = paste0(d$dataset_id, "_", sk), data_seed = as.integer(d$data_seed),
                 fold_seed = as.integer(d$fold_seed), method_seed = as.integer(d$method_seed),
                 inputs_sha256 = d$inputs_sha256, x_sha256 = d$x_sha256,
                 y_sha256 = f64_sha256(y), fold_sha256 = d$fold_sha256)
    if (!identical(case$y_sha256, d$manifest_row[[paste0("y_", sk, "_sha256")]]))
      stop("y hash differs from manifest for ", case$case_id)
    if (case$method_seed != case$data_seed + settings$METHOD_SEED_OFFSET)
      stop("method_seed != data_seed + METHOD_SEED_OFFSET")
    outdir <- file.path(out_root, "results", run_id, sprintf("p%04d", case$p), case$case_id)
    dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
    for (i in seq_len(nrow(reg))) {
      mrow <- reg[i, , drop = FALSE]
      prefix <- file.path(outdir, mrow$method_id)
      if (done_is_valid(prefix)) {
        # Skip only output written by this exact code version (Astra prod finding 6).
        done_src <- utils::read.csv(paste0(prefix, ".csv"), colClasses = "character")$source_sha256
        if (length(done_src) != length(mrow$rule_ids[[1L]]) || anyNA(done_src) || !all(done_src == hashes$tree))
          stop("completed output from a different code version: ", prefix)
        status_lines <- c(status_lines, paste(case$case_id, mrow$method_id, "skipped (done)")); next
      }
      if (file.exists(paste0(prefix, ".done"))) stop("existing .done with invalid hashes: ", prefix)
      started <- utc_now()
      res <- run_method(engine, settings, mrow, d$X, y, d$foldid, case$method_seed)
      prov <- list(study = settings$STUDY_ID, run_id = run_id, source_sha256 = hashes$tree,
                   host = env$host, slurm_job_id = Sys.getenv("SLURM_JOB_ID", NA),
                   slurm_array_task_id = Sys.getenv("SLURM_ARRAY_TASK_ID", NA),
                   started_utc = started, finished_utc = utc_now())
      rows <- rule_csv_rows(res, mrow, case, prov)
      obj <- list(schema_version = SCHEMA_VERSION, case = case, method = as.list(mrow),
                  provenance = prov, source_hashes = hashes, rows = rows,
                  beta = res$beta, pip = res$pip, converged = res$converged,
                  diagnostics = res$diagnostics, warnings = res$warnings,
                  messages = res$messages, error = res$error, runtime_s = res$runtime_s,
                  settings = settings, environment = env)
      atomic_write(paste0(prefix, ".rds"), function(p) saveRDS(obj, p, compress = "xz"))
      atomic_write(paste0(prefix, ".csv"), function(p) utils::write.csv(rows, p, row.names = FALSE, na = "NA"))
      paths <- paste0(prefix, c(".rds", ".csv"))
      atomic_write(paste0(prefix, ".sha256"), function(p)
        writeLines(paste(vapply(paths, file_sha256, ""), basename(paths), sep = "  "), p))
      atomic_write(paste0(prefix, ".done"), function(p)
        writeLines(c(paste("finished_utc", prov$finished_utc),
                     paste("statuses", paste(rows$status, collapse = ","))), p))
      status_lines <- c(status_lines, sprintf("%s %s %s runtime_s=%.3f", case$case_id, mrow$method_id,
                                              paste(rows$status, collapse = ","), res$runtime_s))
    }
  }
  status_lines
}

parse_args <- function(args) {
  out <- list(); i <- 1L
  while (i <= length(args)) {
    if (!startsWith(args[i], "--") || i == length(args)) stop("expected --key value pairs")
    out[[gsub("-", "_", sub("^--", "", args[i]))]] <- args[i + 1L]; i <- i + 2L
  }
  for (k in c("input", "manifest", "out_root", "run_id"))
    if (is.null(out[[k]])) stop("missing --", gsub("_", "-", k))
  out
}

if (sys.nframe() == 0L) {
  a <- parse_args(commandArgs(trailingOnly = TRUE))
  self <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1L])
  code_root <- if (!is.null(a$code_root)) a$code_root else dirname(normalizePath(self))
  rc <- tryCatch({
    s <- run_case(a$input, a$manifest, a$out_root, a$run_id,
                  scales = strsplit(if (is.null(a$scales)) "c100" else a$scales, ",")[[1L]],
                  methods = if (is.null(a$methods)) NULL else strsplit(a$methods, ",")[[1L]],
                  code_root = code_root)
    writeLines(s); 0L
  }, error = function(e) { message("FATAL: ", conditionMessage(e)); 1L })
  quit(save = "no", status = rc)
}
