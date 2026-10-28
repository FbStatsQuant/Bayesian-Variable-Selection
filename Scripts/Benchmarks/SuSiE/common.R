# common.R -- shared helpers used by A1 SuSiE (master §III.3.0, §III.3.6 k).
# Only the helpers A1 needs, with the master's names. A1 uses no EBIC or OLS refit, so
# `ols_rss` and the EBIC scorer are not included here. Only defines functions.

# Input assertions (§III.3.0): X finite, centred, sd 1 to within COMMON$DESIGN_TOL;
# y finite of length n; foldid of length n with labels 1..N_FOLDS.
assert_inputs <- function(X, y, foldid, tol = 1e-10, n_folds = 10L) {
  if (!is.matrix(X) || !is.numeric(X)) stop("inputs: X must be a numeric matrix")
  if (any(!is.finite(X))) stop("inputs: X has non-finite entries")
  n <- nrow(X)
  if (max(abs(colMeans(X))) >= tol) stop("inputs: X is not centred")
  sds <- sqrt(colSums(sweep(X, 2L, colMeans(X))^2) / (n - 1))
  if (max(abs(sds - 1)) >= tol) stop("inputs: X columns do not have sd 1")
  if (!is.numeric(y) || !is.null(dim(y)) || length(y) != n || any(!is.finite(y)))
    stop("inputs: y must be a finite numeric vector of length n")
  if (length(foldid) != n) stop("inputs: length(foldid) != n")
  if (!identical(sort(unique(as.integer(foldid))), seq_len(n_folds)) ||
      any(foldid != as.integer(foldid)))
    stop("inputs: foldid labels are not 1..", n_folds)
  invisible(TRUE)
}

# Exact package version assertion (§III.3.0 Library; §III.3.6 b).
assert_pkg_version <- function(pkg, version) {
  found <- as.character(utils::packageVersion(pkg))
  if (!identical(found, as.character(version)))
    stop("package version: ", pkg, " ", found, " found, ", version, " required")
  invisible(found)
}

# One capture layer (§III.3.0, §III.3.6 k): evaluate expr, muffle and record every warning and
# message, record an error. Returns list(value, warnings, messages, error); value = NULL and
# error a string when the call failed, else error = NULL.
with_captured_conditions <- function(expr) {
  warnings <- character()
  messages <- character()
  error <- NULL
  value <- tryCatch(
    withCallingHandlers(expr,
      warning = function(w) {
        warnings <<- c(warnings, conditionMessage(w))
        invokeRestart("muffleWarning")
      },
      message = function(m) {
        messages <<- c(messages, sub("\n$", "", conditionMessage(m)))
        invokeRestart("muffleMessage")
      }),
    error = function(e) {
      error <<- conditionMessage(e)
      NULL
    })
  list(value = if (is.null(error)) value else NULL,
       warnings = warnings, messages = messages, error = error)
}

# Support key (§III.3.0): sorted indices joined by ";"; the empty support is "".
support_key <- function(idx) {
  idx <- sort(unique(as.integer(idx)))
  paste(idx, collapse = ";")
}

# Registered rule ids and roles of a method id (§III.3.0 METHODS registry).
registry_rules <- function(settings, method_id) {
  M <- settings$METHODS
  i <- which(M$method_id == method_id)
  if (length(i) != 1L) stop("registry: method_id not registered: ", method_id)
  list(rule_ids = M$rule_ids[[i]], roles = M$roles[[i]])
}

# Rule frame (§III.3.0): rule_id, role, status, support, support_audit, k, converged,
# diag_flag, diag_codes, error, plus method extra columns (none for A1).
# `supports` is a list of integer index vectors, one per rule, in registry order.
make_rule_rows <- function(rule_ids, roles, supports, status, converged,
                           diag_flag, diag_codes) {
  stopifnot(length(rule_ids) == length(roles), length(supports) == length(rule_ids),
            status %in% c("ok", "warning"))
  data.frame(
    rule_id = rule_ids, role = roles, status = status,
    support = vapply(supports, support_key, ""),
    support_audit = NA_character_,
    k = vapply(supports, function(s) length(unique(s)), 0L),
    converged = converged, diag_flag = diag_flag, diag_codes = diag_codes,
    error = NA_character_, stringsAsFactors = FALSE)
}

# Failure rows (§III.3.0, §III.3.6 k): status "failed", support and k NA; support_audit holds
# the support the fit returned (character keys, one per rule, or NA when it returned nothing).
# A failed fit has converged = FALSE (§III.3.0 Convergence).
fail_rows <- function(rule_ids, roles, support = NA_character_, reason,
                      diag_flag = NA, diag_codes = NA_character_) {
  support <- rep_len(as.character(support), length(rule_ids))
  data.frame(
    rule_id = rule_ids, role = roles, status = "failed",
    support = NA_character_, support_audit = support, k = NA_integer_,
    converged = FALSE, diag_flag = diag_flag, diag_codes = diag_codes,
    error = paste(reason, collapse = "; "), stringsAsFactors = FALSE)
}

# Timing helper: elapsed seconds since t0 = proc.time()[["elapsed"]].
elapsed <- function(t0) as.numeric(proc.time()[["elapsed"]] - t0)
