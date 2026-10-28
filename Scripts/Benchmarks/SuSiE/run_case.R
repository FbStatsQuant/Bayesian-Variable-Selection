# run_case.R -- runner for A1 SuSiE (master §III.3.0, §IV.1.1, §IV.1.2): one dataset x the
# registered A1 method ids x the requested scale(s); writes <method_id>.{rds,csv,sha256,done}
# atomically under <out_root>/<run_id>/p{pppp}/<case_id>/. Reads only the input file it is given
# (an `inputs/` file); it never opens `truth/`.
#
# Usage (NOTS compute node; module load GCC/14.3.0; module load R/4.5.2):
#   Rscript run_case.R --code_dir=DIR --input=FILE --out_root=DIR --run_id=ID \
#     [--methods=A1,SuSiE-L100] [--scales=c100] [--env_baseline=<run_dir>/env_fingerprint.rds]
# With --env_baseline (production), the current environment fingerprint must equal the run's
# frozen baseline before any fit or reuse; otherwise the runner stops without fitting.

parse_args <- function(args) {
  kv <- regmatches(args, regexec("^--([^=]+)=(.*)$", args))
  ok <- lengths(kv) == 3L
  if (any(!ok)) stop("bad argument(s): ", paste(args[!ok], collapse = " "))
  stats::setNames(vapply(kv, `[`, "", 3L), vapply(kv, `[`, "", 2L))
}

f64_sha256 <- function(x)
  digest::digest(writeBin(as.double(as.vector(x)), raw(), endian = "little"),
                 algo = "sha256", serialize = FALSE)
file_sha256 <- function(f) digest::digest(file = f, algo = "sha256")
utc_now <- function() format(Sys.time(), "%Y-%m-%dT%H:%M:%OS3Z", tz = "UTC")
vm_hwm_kb <- function() {
  s <- tryCatch(readLines("/proc/self/status"), error = function(e) character())
  h <- grep("^VmHWM:", s, value = TRUE)
  if (length(h)) as.numeric(gsub("[^0-9]", "", h)) else NA_real_
}

CODE_FILES <- c("config.R", "common.R", "methods/fit_A1_susie.R", "run_case.R")
source_tree_sha256 <- function(code_dir) {
  h <- vapply(file.path(code_dir, CODE_FILES), file_sha256, "")
  digest::digest(paste0(CODE_FILES, "  ", h, collapse = "\n"), algo = "sha256",
                 serialize = FALSE)
}

# §III.3.0 Library: every loaded namespace other than R's base-priority packages comes from the
# sealed study library. Returns the resolved namespace paths (saved as provenance).
BASE_PKGS <- c("base", "compiler", "datasets", "grDevices", "graphics", "grid", "methods",
               "parallel", "splines", "stats", "stats4", "tcltk", "tools", "utils")
assert_library <- function(lib) {
  lib <- normalizePath(lib)
  paths <- vapply(loadedNamespaces(), function(ns) normalizePath(
    if (ns == "base") file.path(.Library, "base") else getNamespaceInfo(ns, "path")), "")
  other <- paths[!names(paths) %in% BASE_PKGS]
  bad <- other[!startsWith(other, paste0(lib, "/"))]
  if (length(bad)) stop("library: namespaces outside the study library: ",
                        paste(names(bad), bad, sep = "=", collapse = ", "))
  invisible(paths)
}

# Atomic write (temporary file in the same directory, then rename). The temporary name carries
# host, PID and a tempfile() suffix (C-level randomness; the R RNG stream is not touched).
atomic_write <- function(path, writer) {
  tmp <- paste0(path, ".tmp.", Sys.info()[["nodename"]], ".", Sys.getpid(), ".",
                basename(tempfile("")))
  writer(tmp)
  if (!file.rename(tmp, path)) stop("rename failed: ", path)
}

# An incomplete or invalid bundle (some of the four files, no valid .done) is moved aside to
# <stem>.quarantine_<UTC>/ before the case is refitted, so damaged artifacts stay for audit and
# can never be mixed with new files.
quarantine_partial <- function(stem) {
  files <- paste0(stem, c(".rds", ".csv", ".sha256", ".done"))
  tmps <- Sys.glob(paste0(stem, ".*.tmp.*"))
  present <- c(files[file.exists(files)], tmps)
  if (!length(present)) return(invisible(character()))
  qd <- paste0(stem, ".quarantine_", format(Sys.time(), "%Y%m%dT%H%M%SZ", tz = "UTC"), "_",
               Sys.info()[["nodename"]], "_", Sys.getpid(), "_", basename(tempfile("")))
  if (!dir.create(qd, showWarnings = FALSE)) stop("quarantine directory could not be created: ", qd)
  ok <- file.rename(present, file.path(qd, basename(present)))
  if (!all(ok)) stop("quarantine failed for ", stem)
  message("quarantined partial outputs: ", qd)
  invisible(qd)
}

# Environment fingerprint saved in provenance and required to match on resume.
env_fingerprint <- function(lib) {
  em <- file.path(dirname(normalizePath(lib)), "environment_manifest.txt")
  c(R = R.version.string,
    environment_manifest_sha256 = if (file.exists(em)) file_sha256(em) else
      stop("environment manifest missing: ", em),
    susieR = as.character(utils::packageVersion("susieR")),
    blas = extSoftVersion()[["BLAS"]])
}

# Bundle validity (same contract as slurm/bundles.sh::valid_bundle): all four files exist and the
# .sha256 file has exactly two lines, "<hash>  <method>.rds" and "<hash>  <method>.csv", both verifying.
done_is_valid <- function(stem) {
  files <- paste0(stem, c(".rds", ".csv", ".sha256", ".done"))
  if (!all(file.exists(files))) return(FALSE)
  lines <- readLines(files[3])
  if (length(lines) != 2L || !all(grepl("^[0-9a-f]{64}  ", lines))) return(FALSE)
  if (!identical(sub("^[0-9a-f]{64}  ", "", lines), basename(files[1:2]))) return(FALSE)
  want <- sub("^([0-9a-f]{64})  .*$", "\\1", lines)
  got <- vapply(files[1:2], file_sha256, "")
  identical(unname(want), unname(got))
}

# Resume guard: a valid .done is reused only if it was produced by the same code, input and
# seed as the current request; otherwise the run stops (use a new run id).
done_matches <- function(stem, src_sha, inputs_sha, method_seed, env_fp = NULL) {
  x <- utils::read.csv(paste0(stem, ".csv"), colClasses = "character")
  ok <- all(x$source_sha256 == src_sha) && all(x$inputs_sha256 == inputs_sha) &&
    all(as.numeric(x$method_seed) == method_seed)
  if (!ok) stop("resume: existing outputs at ", stem, " come from different code, input or ",
                "seed; use a new run id")
  if (!is.null(env_fp) &&
      !identical(readRDS(paste0(stem, ".rds"))$provenance$env_fingerprint, env_fp))
    stop("resume: existing outputs at ", stem, " come from a different environment ",
         "(R, study library, BLAS); use a new run id")
  TRUE
}

# §IV.1.2 column order.
SCHEMA <- c("study", "run_id", "source_sha256",
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
RULE_FRAME_COLS <- c("rule_id", "role", "status", "support", "support_audit", "k",
                     "converged", "diag_flag", "diag_codes", "error")

main <- function(argv = commandArgs(trailingOnly = TRUE)) {
  a <- parse_args(argv)
  for (k in c("code_dir", "input", "out_root", "run_id"))
    if (is.na(a[k])) stop("missing --", k)
  code_dir <- normalizePath(a[["code_dir"]])
  input <- normalizePath(a[["input"]])
  if (!grepl("/inputs/", input) || grepl("truth", input))
    stop("runner reads inputs/ files only: ", input)
  Sys.setenv(OMP_NUM_THREADS = "1", OPENBLAS_NUM_THREADS = "1", MKL_NUM_THREADS = "1")

  cfg <- new.env()
  sys.source(file.path(code_dir, "config.R"), envir = cfg)
  .libPaths(c(cfg$COMMON$LIB, .Library))
  fit_env <- new.env(parent = asNamespace("stats"))
  sys.source(file.path(code_dir, "common.R"), envir = fit_env)
  sys.source(file.path(code_dir, "methods", "fit_A1_susie.R"), envir = fit_env)

  M <- cfg$METHODS
  methods <- if (is.na(a["methods"])) M$method_id else strsplit(a[["methods"]], ",")[[1]]
  if (!all(methods %in% M$method_id)) stop("unregistered method id(s)")
  scales <- if (is.na(a["scales"])) names(cfg$COMMON$SCALES) else strsplit(a[["scales"]], ",")[[1]]
  if (!all(scales %in% names(cfg$COMMON$SCALES))) stop("unknown scale key(s)")
  # Load every package namespace (and its imports) before any fit timer starts, so runtime_s
  # excludes package loading; namespaces loaded during a fit are recorded in provenance.
  for (pkg in unique(M$package[M$method_id %in% methods])) loadNamespace(pkg)
  loadNamespace("digest")
  assert_library(cfg$COMMON$LIB)
  env_fp <- env_fingerprint(cfg$COMMON$LIB)
  if (!is.na(a["env_baseline"]) && !identical(env_fp, readRDS(a[["env_baseline"]])))
    stop("environment differs from the run baseline ", a[["env_baseline"]], ": ",
         paste(names(env_fp), env_fp, sep = "=", collapse = "; "))

  d <- readRDS(input)
  stopifnot(d$method_seed == d$data_seed + cfg$METHOD_SEED_OFFSET, ncol(d$X) == d$p)
  X <- d$X
  inputs_sha <- file_sha256(input)
  x_sha <- f64_sha256(X)
  fold_sha <- f64_sha256(d$foldid)
  src_sha <- source_tree_sha256(code_dir)
  host <- Sys.info()[["nodename"]]
  job <- Sys.getenv("SLURM_ARRAY_JOB_ID", Sys.getenv("SLURM_JOB_ID", NA))
  task <- Sys.getenv("SLURM_ARRAY_TASK_ID", NA)

  for (scale_key in scales) {
    y <- unname(as.numeric(d$Y[, scale_key]))
    case_id <- paste0(d$dataset_id, "_", scale_key)
    out_dir <- file.path(a[["out_root"]], a[["run_id"]], sprintf("p%04d", d$p), case_id)
    dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
    for (mid in methods) {
      row <- M[M$method_id == mid, ]
      stem <- file.path(out_dir, mid)
      if (done_is_valid(stem) && done_matches(stem, src_sha, inputs_sha, d$method_seed, env_fp)) {
        message("skip (valid .done): ", stem); next
      }
      quarantine_partial(stem)
      settings <- cfg$make_settings(row$variant)
      reg <- list(rule_ids = row$rule_ids[[1]], roles = row$roles[[1]])
      RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(d$method_seed)
      ns_before <- loadedNamespaces()
      started <- utc_now()
      t0 <- proc.time()[["elapsed"]]
      fit <- tryCatch(
        fit_env[[row$fn]](X, y, d$foldid, d$method_seed, settings),
        error = function(e) list(
          rules = fit_env$fail_rows(reg$rule_ids, reg$roles, NA_character_,
                                    paste("uncaught:", conditionMessage(e))),
          pip = NULL, beta = rep(NA_real_, d$p), converged = FALSE,
          diagnostics = list(), warnings = character(), messages = character()))
      runtime <- fit_env$elapsed(t0)
      finished <- utc_now()
      ns_paths <- assert_library(cfg$COMMON$LIB)
      r <- fit$rules
      if (!identical(names(r), RULE_FRAME_COLS) || !identical(r$rule_id, reg$rule_ids) ||
          !identical(r$role, reg$roles))
        stop("rule frame does not match the registry for ", mid)
      conds <- c(fit$warnings, fit$messages)
      pkg_ver <- tryCatch(as.character(utils::packageVersion(row$package)),
                          error = function(e) NA_character_)
      n <- nrow(r)
      rows <- data.frame(
        study = cfg$COMMON$STUDY, run_id = a[["run_id"]], source_sha256 = src_sha,
        regime = cfg$COMMON$REGIME, p = d$p, scenario = d$scenario, replicate = d$replicate,
        scale_key = scale_key, scale = cfg$COMMON$SCALES[[scale_key]],
        dataset_id = d$dataset_id, case_id = case_id,
        data_seed = d$data_seed, fold_seed = d$fold_seed, method_seed = d$method_seed,
        inputs_sha256 = inputs_sha, x_sha256 = x_sha, y_sha256 = f64_sha256(y),
        fold_sha256 = fold_sha,
        method_id = mid, method_label = row$method_label, package = row$package,
        package_version = pkg_ver,
        r[, c("rule_id", "role", "status", "converged", "diag_flag", "diag_codes")],
        n_warnings = length(conds),
        warnings = if (length(fit$warnings)) paste(fit$warnings, collapse = " || ") else NA_character_,
        messages = if (length(fit$messages)) paste(fit$messages, collapse = " || ") else NA_character_,
        error = r$error, k = r$k, support = r$support, support_audit = r$support_audit,
        stringsAsFactors = FALSE)
      for (col in c("tp", "fp", "fn", "exact", "error_type", sprintf("sel_a%02d", 1:14),
                    sprintf("pip_a%02d", 1:14), "max_pip_null")) rows[[col]] <- NA
      rows$runtime_s <- runtime; rows$host <- host; rows$slurm_job_id <- job
      rows$slurm_array_task_id <- task; rows$started_utc <- started; rows$finished_utc <- finished
      stopifnot(identical(names(rows), SCHEMA), nrow(rows) == n)
      rds <- list(rows = rows, fit = fit[setdiff(names(fit), "rules")], runtime_s = runtime,
                  vm_hwm_kb = vm_hwm_kb(),
                  provenance = list(R = R.version.string, blas = extSoftVersion()[["BLAS"]],
                                    la_library = La_library(), libPaths = .libPaths(),
                                    namespace_paths = ns_paths,
                                    ns_loaded_during_fit = setdiff(loadedNamespaces(), ns_before),
                                    namespaces = vapply(loadedNamespaces(), function(ns)
                                      as.character(getNamespaceVersion(ns)), ""),
                                    rng_kind = RNGkind(), env_fingerprint = env_fp,
                                    locale = Sys.getlocale(),
                                    thread_env = Sys.getenv(c("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS",
                                                              "MKL_NUM_THREADS", "FLEXIBLAS_NUM_THREADS")), code_files = CODE_FILES,
                                    source_sha256 = src_sha, input = input))
      atomic_write(paste0(stem, ".rds"), function(f) saveRDS(rds, f, compress = "xz"))
      atomic_write(paste0(stem, ".csv"), function(f) utils::write.csv(rows, f, row.names = FALSE, na = "NA"))
      h <- vapply(paste0(stem, c(".rds", ".csv")), file_sha256, "")
      atomic_write(paste0(stem, ".sha256"), function(f)
        writeLines(paste0(h, "  ", basename(names(h))), f))
      atomic_write(paste0(stem, ".done"), function(f) writeLines(finished, f))
      message(sprintf("%s %s: status=%s k=%s runtime=%.2fs", case_id, mid,
                      r$status[1], paste(r$k, collapse = ","), runtime))
    }
  }
  invisible(TRUE)
}

if (sys.nframe() == 0L) main()
