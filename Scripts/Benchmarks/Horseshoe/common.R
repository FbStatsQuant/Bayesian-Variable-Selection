# Shared helpers used by A3 (master §III.3.0, §IV.1.1, §IV.1.2). Names and roles follow the
# master's common.R list; only the helpers A3 needs are here (A3 uses no OLS refit and no
# EBIC/BIC scorer). Duplicated across method folders on purpose; merged later.

# ---- Input assertions (§III.3.0 "Input assertions") ------------------------------------
# X finite, centred, sd 1 to within X_TOL; y finite of length n; foldid of length n with
# labels 1..NFOLDS.
assert_inputs <- function(X, y, foldid, tol = 1e-10, nfolds = 10L) {
  if (!is.matrix(X) || !is.numeric(X)) stop("assert_inputs: X must be a numeric matrix")
  n <- nrow(X)
  if (!all(is.finite(X))) stop("assert_inputs: X has non-finite entries")
  if (max(abs(colMeans(X))) > tol) stop("assert_inputs: X is not centred")
  if (max(abs(apply(X, 2, stats::sd) - 1)) > tol) stop("assert_inputs: X columns do not have sd 1")
  if (!is.numeric(y) || length(y) != n || !all(is.finite(y))) stop("assert_inputs: bad y")
  if (length(foldid) != n) stop("assert_inputs: length(foldid) != n")
  if (!identical(sort(unique(as.integer(foldid))), seq_len(nfolds)) ||
      any(foldid != as.integer(foldid))) stop("assert_inputs: fold labels are not 1..", nfolds)
  invisible(TRUE)
}

# ---- Package version assertion (§III.3.0 "Library") -------------------------------------
assert_pkg_version <- function(pkg, version) {
  v <- as.character(utils::packageVersion(pkg))
  if (!identical(v, version)) stop("assert_pkg_version: ", pkg, " is ", v, ", expected ", version)
  invisible(TRUE)
}

# ---- One capture layer (§III.3.0 "One capture layer", "Status") -------------------------
# Evaluates expr, recording every warning and message verbatim (and muffling them) and
# turning an error into a recorded message instead of a stop.
with_captured_conditions <- function(expr) {
  warnings <- character(0)
  messages <- character(0)
  error <- NULL
  value <- withCallingHandlers(
    tryCatch(expr, error = function(e) {
      error <<- conditionMessage(e)
      NULL
    }),
    warning = function(w) {
      warnings <<- c(warnings, conditionMessage(w))
      invokeRestart("muffleWarning")
    },
    message = function(m) {
      messages <<- c(messages, sub("\n$", "", conditionMessage(m)))
      invokeRestart("muffleMessage")
    })
  list(value = value, error = error, warnings = warnings, messages = messages)
}

# ---- Support keys (§III.3.0 EBIC tie-break; §IV.1.2 `support`) --------------------------
# Sorted indices joined by ";"; the empty support is "".
support_key <- function(idx) {
  idx <- sort(as.integer(idx))
  if (length(idx) == 0L) "" else paste(idx, collapse = ";")
}

# ---- Rule rows (§III.3.0 "Method registry and rule frame") ------------------------------
registry_row <- function(settings, method_id) {
  row <- settings$METHODS[settings$METHODS$method_id == method_id, , drop = FALSE]
  if (nrow(row) != 1L) stop("registry_row: method_id not registered: ", method_id)
  row
}

collapse_conditions <- function(x) if (length(x) == 0L) NA_character_ else paste(x, collapse = " | ")

# Builds the rule frame of one fit with exactly the registered rule ids, in registry order.
# per_rule: named list by rule_id; each element a list with
#   status (ok / warning / failed), support (integer vector, or NULL for a failed rule),
#   support_audit (integer vector or NULL), warnings, messages (character), error (character or NA).
# Fit-level: converged, diag_flag, diag_codes (character vector of codes), extra (named list of
# scalars, the method's extra columns, repeated on every row).
make_rule_rows <- function(settings, method_id, per_rule, converged, diag_flag, diag_codes,
                           extra = list()) {
  reg <- registry_row(settings, method_id)
  rule_ids <- reg$rule_ids[[1]]
  roles <- reg$roles[[1]]
  if (!setequal(names(per_rule), rule_ids)) stop("make_rule_rows: rules differ from the registry")
  rows <- lapply(seq_along(rule_ids), function(i) {
    r <- per_rule[[rule_ids[i]]]
    failed <- identical(r$status, "failed")
    sup <- if (failed || is.null(r$support)) NA_character_ else support_key(r$support)
    k <- if (failed || is.null(r$support)) NA_integer_ else length(r$support)
    aud <- if (is.null(r$support_audit)) NA_character_ else support_key(r$support_audit)
    err <- if (is.null(r$error)) NA_character_ else as.character(r$error)
    data.frame(rule_id = rule_ids[i], role = roles[i], status = r$status,
               support = sup, support_audit = aud, k = k,
               converged = as.logical(converged), diag_flag = as.logical(diag_flag),
               diag_codes = paste(diag_codes, collapse = ";"),
               n_warnings = length(r$warnings) + length(r$messages),
               warnings = collapse_conditions(r$warnings),
               messages = collapse_conditions(r$messages),
               error = err, stringsAsFactors = FALSE)
  })
  out <- do.call(rbind, rows)
  for (nm in names(extra)) out[[nm]] <- extra[[nm]]
  out
}

# Failed fit (§III.3.0 "Failures"): every registered rule has status "failed", support and k NA;
# support_audit kept when the fit produced one (named list by rule id), else NA. converged is NA
# for methods without a convergence criterion, else FALSE. diag_flag is NA (no diagnostics).
fail_rows <- function(settings, method_id, error, warnings = character(0), messages = character(0),
                      support_audit = NULL, extra = list()) {
  reg <- registry_row(settings, method_id)
  per_rule <- lapply(reg$rule_ids[[1]], function(rid)
    list(status = "failed", support = NULL, support_audit = support_audit[[rid]],
         warnings = warnings, messages = messages, error = error))
  names(per_rule) <- reg$rule_ids[[1]]
  make_rule_rows(settings, method_id, per_rule,
                 converged = if (isTRUE(reg$converged_na)) NA else FALSE,
                 diag_flag = NA, diag_codes = character(0), extra = extra)
}

# ---- Timing ----------------------------------------------------------------------------
elapsed <- function(t0) as.numeric(proc.time()[["elapsed"]] - t0)

# ---- Hashes and IO (§IV.1.1, §IV.1.2; Oct-14 conventions) -------------------------------
# float64 little-endian SHA-256 of a numeric vector or matrix (column-major).
f64_sha256 <- function(x) {
  digest::digest(writeBin(as.double(as.vector(x)), raw(), endian = "little"),
                 algo = "sha256", serialize = FALSE)
}
file_sha256 <- function(path) digest::digest(file = path, algo = "sha256")

# Write via a temporary file in the same directory, then rename (atomic on one filesystem).
atomic_write <- function(path, writefun) {
  tmp <- paste0(path, ".tmp.", Sys.getpid())
  on.exit(unlink(tmp), add = TRUE)
  writefun(tmp)
  if (!file.rename(tmp, path)) stop("atomic_write: rename failed for ", path)
  invisible(path)
}
