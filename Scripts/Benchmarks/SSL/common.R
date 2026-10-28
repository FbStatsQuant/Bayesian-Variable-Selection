# common.R -- shared helpers used by A2 (master §III.3.0; names and signatures of §III.3.1 k,
# §III.3.6 k). Only the helpers A2 uses are here; the study-wide common.R is merged later.
# No helper reads anything outside its arguments.

# --- Input assertions (§III.3.0 "Input assertions"; §III.3.1 e.1) ------------------------
# X finite, centred and with sd 1 to within common$design_tol, no scaled:* attributes;
# y a finite numeric vector of length n; foldid of length n with labels exactly 1..10,
# each label on at least common$min_fold_n rows.
assert_inputs <- function(X, y, foldid, common = NULL) {
  tol     <- if (is.null(common$design_tol)) 1e-10 else common$design_tol
  n_folds <- if (is.null(common$n_folds)) 10L else common$n_folds
  min_n   <- if (is.null(common$min_fold_n)) 3L else common$min_fold_n
  if (!is.matrix(X) || !is.numeric(X)) stop("assert_inputs: X must be a numeric matrix")
  if (any(!is.finite(X))) stop("assert_inputs: X has non-finite entries")
  if (any(grepl("^scaled:", names(attributes(X))))) stop("assert_inputs: X carries scaled:* attributes")
  n <- nrow(X)
  if (max(abs(colMeans(X))) > tol) stop("assert_inputs: X is not centred to within ", tol)
  if (max(abs(apply(X, 2, stats::sd) - 1)) > tol) stop("assert_inputs: X columns do not have sd 1 to within ", tol)
  if (!is.numeric(y) || !is.null(dim(y)) || length(y) != n) stop("assert_inputs: y must be a numeric vector of length n")
  if (any(!is.finite(y))) stop("assert_inputs: y has non-finite entries")
  if (length(foldid) != n) stop("assert_inputs: length(foldid) != n")
  if (!identical(sort(unique(as.integer(foldid))), seq_len(n_folds)) || any(foldid != as.integer(foldid)))
    stop("assert_inputs: fold labels must be exactly 1..", n_folds)
  if (min(tabulate(as.integer(foldid), n_folds)) < min_n) stop("assert_inputs: a fold has fewer than ", min_n, " rows")
  invisible(TRUE)
}

# --- Package version assertion (§III.3.0 "Library"; §III.3.1 b) --------------------------
assert_pkg_version <- function(pkg, version) {
  installed <- as.character(utils::packageVersion(pkg))
  if (!identical(installed, version))
    stop("assert_pkg_version: ", pkg, " ", installed, " found, ", version, " required")
  invisible(TRUE)
}

# --- Condition capture (§III.3.6 k) ------------------------------------------------------
# Evaluates expr with every warning and message recorded verbatim and muffled, inside a
# tryCatch that records an error. Returns list(value, warnings, messages, error); on error
# value = NULL and error is the message string, otherwise error = NULL.
with_captured_conditions <- function(expr) {
  warns <- character(); msgs <- character()
  value <- tryCatch(
    withCallingHandlers(expr,
      warning = function(w) { warns <<- c(warns, conditionMessage(w)); invokeRestart("muffleWarning") },
      message = function(m) { msgs  <<- c(msgs, conditionMessage(m)); invokeRestart("muffleMessage") }),
    error = function(e) structure(list(msg = conditionMessage(e)), class = "captured_error"))
  if (inherits(value, "captured_error"))
    return(list(value = NULL, warnings = warns, messages = msgs, error = value$msg))
  list(value = value, warnings = warns, messages = msgs, error = NULL)
}

# --- Support keys (§III.3.0 "EBIC/BIC": sorted indices joined by ";") ---------------------
# The empty support (null model) has key "".
support_key <- function(idx) paste(sort(as.integer(idx)), collapse = ";")
parse_key <- function(key) {
  if (is.na(key)) return(NA_integer_)
  if (!nzchar(key)) return(integer(0))
  as.integer(strsplit(key, ";", fixed = TRUE)[[1]])
}

# --- Rule frame (§III.3.0 "Method registry and rule frame") -------------------------------
# Columns returned by every wrapper; the runner adds the §IV.1.2 provenance columns.
RULE_FRAME_COLUMNS <- c("rule_id", "role", "status", "support", "support_audit", "k",
                        "converged", "diag_flag", "diag_codes", "error")

# Rows for a fit that did not fail. supports: list of integer index vectors, one per rule.
make_rule_rows <- function(rule_ids, roles, supports, status, converged, diag_flag, diag_codes,
                           extra = NULL) {
  stopifnot(length(rule_ids) == length(roles), length(rule_ids) == length(supports),
            status %in% c("ok", "warning"))
  keys <- vapply(supports, support_key, character(1))
  out <- data.frame(rule_id = unlist(rule_ids), role = unlist(roles), status = status,
                    support = keys, support_audit = NA_character_,
                    k = vapply(supports, length, integer(1)),
                    converged = converged, diag_flag = diag_flag, diag_codes = diag_codes,
                    error = NA_character_, stringsAsFactors = FALSE)
  if (!is.null(extra)) out <- cbind(out, extra)
  out
}

# Failed rows (§III.3.0 "Failures"): support = NA, k = NA; a returned support is kept in
# support_audit (NA when the fit returned nothing); reason goes to the error column.
fail_rows <- function(rule_ids, roles, support = NULL, reason, converged = FALSE,
                      diag_flag = NA, diag_codes = NA_character_) {
  audit <- if (is.null(support)) NA_character_ else support_key(support)
  data.frame(rule_id = unlist(rule_ids), role = unlist(roles), status = "failed",
             support = NA_character_, support_audit = audit, k = NA_integer_,
             converged = converged, diag_flag = diag_flag, diag_codes = diag_codes,
             error = as.character(reason), stringsAsFactors = FALSE)
}

# Registered rule ids and roles of a method id (§III.3.0: rows always match the registry).
registry_row <- function(settings, method_id = NULL, fn = NULL, variant = NULL) {
  M <- settings$METHODS
  sel <- if (!is.null(method_id)) M$method_id == method_id else M$fn == fn & M$variant == variant
  if (sum(sel) != 1L) stop("registry_row: no unique METHODS row for ", method_id, fn, "/", variant)
  r <- M[sel, , drop = FALSE]
  list(method_id = r$method_id, fn = r$fn, variant = r$variant, method_label = r$method_label,
       package = r$package, pkg_version = r$pkg_version, tier = r$tier,
       rule_ids = r$rule_ids[[1]], roles = r$roles[[1]])
}

# --- Timing and hashes -------------------------------------------------------------------
elapsed <- function() proc.time()[["elapsed"]]
utc_now <- function() format(Sys.time(), "%Y-%m-%dT%H:%M:%OS3Z", tz = "UTC")

# float64 little-endian SHA-256 (§IV.1.2 input hashes; same as _shared/gen_dev_data.R).
f64_sha256 <- function(x) {
  digest::digest(writeBin(as.double(as.vector(x)), raw(), endian = "little"),
                 algo = "sha256", serialize = FALSE)
}
file_sha256 <- function(path) digest::digest(file = path, algo = "sha256")

# --- Rule-row schema of the CSV (§IV.1.2), in column order ---------------------------------
RULE_ROW_SCHEMA <- c(
  "study", "run_id", "source_sha256",
  "regime", "p", "scenario", "replicate", "scale_key", "scale", "dataset_id", "case_id",
  "data_seed", "fold_seed", "method_seed",
  "inputs_sha256", "x_sha256", "y_sha256", "fold_sha256",
  "method_id", "method_label", "package", "package_version",
  "rule_id", "role",
  "status",
  "converged", "diag_flag", "diag_codes", "n_warnings", "warnings", "messages", "error",
  "k", "support", "support_audit",
  "tp", "fp", "fn", "exact", "error_type",
  sprintf("sel_a%02d", 1:14), sprintf("pip_a%02d", 1:14), "max_pip_null",
  "runtime_s", "host", "slurm_job_id", "slurm_array_task_id", "started_utc", "finished_utc")
# Columns filled only by the scoring step (§IV.1.2); NA at fit time.
SCORING_COLUMNS <- c("tp", "fp", "fn", "exact", "error_type",
                     sprintf("sel_a%02d", 1:14), sprintf("pip_a%02d", 1:14), "max_pip_null")

# --- IO: atomic writes (§IV.1.1: temporary file, then rename) ----------------------------
write_atomic <- function(writer, path) {
  # Host name and process id make the temporary name unique across nodes (no RNG is used).
  tmp <- paste0(path, ".tmp.", Sys.info()[["nodename"]], ".", Sys.getpid())
  writer(tmp)
  if (!file.rename(tmp, path)) stop("write_atomic: rename failed for ", path)
  invisible(path)
}
