# common.R: shared helpers used by F3 (master §III.3.0 and §III.3.1 "Conventions" and k).
# Names and signatures follow the master; this copy holds only what F3 uses and is merged
# with the other method folders later. Sourcing this file computes nothing.

# ---- input and version assertions (§III.3.0 "Input assertions"; §III.3.1 e step 1) ----

assert_inputs <- function(X, y, foldid, common) {
  if (!is.matrix(X) || !is.double(X)) stop("X must be a double matrix")
  if (any(grepl("^scaled:", names(attributes(X))))) stop("X carries scaled:* attributes")
  if (any(!is.finite(X))) stop("X has non-finite entries")
  n <- nrow(X)
  if (max(abs(colMeans(X))) > common$design_tol) stop("X columns are not centred")
  # sd with denominator n - 1; X is centred, so sd_j^2 = sum(X_j^2) / (n - 1)
  if (max(abs(colSums(X^2) / (n - 1) - 1)) > common$design_tol) stop("X columns do not have sd 1")
  if (!is.numeric(y) || !is.null(dim(y)) || length(y) != n || any(!is.finite(y)))
    stop("y must be a finite numeric vector of length nrow(X)")
  if (!is.numeric(foldid) || length(foldid) != n || anyNA(foldid) ||
      any(foldid != round(foldid))) stop("foldid must hold n integer labels")
  if (!identical(sort(unique(as.integer(foldid))), seq_len(common$nfolds)))
    stop("fold labels must be exactly 1..", common$nfolds)
  if (any(tabulate(as.integer(foldid), common$nfolds) < common$min_fold_rows))
    stop("every fold needs at least ", common$min_fold_rows, " rows")
  invisible(TRUE)
}

assert_pkg_version <- function(pkg, version) {
  found <- as.character(utils::packageVersion(pkg))
  if (!identical(found, version)) stop(pkg, " version ", found, " found, ", version, " required")
  invisible(TRUE)
}

# ---- grid and supports (§III.3.1 "Conventions") ----

# Decreasing fraction grid exp(seq(0, log(min_ratio), length.out = nlambda)).
lambda_fraction <- function(grid) {
  exp(seq(0, log(grid$min_ratio), length.out = grid$nlambda))
}

# Sorted indices joined by ";"; the null support is "".
support_key <- function(idx) paste(sort(as.integer(idx)), collapse = ";")

parse_key <- function(key) {
  if (is.na(key)) return(NA_integer_)
  if (!nzchar(key)) return(integer())
  as.integer(strsplit(key, ";", fixed = TRUE)[[1L]])
}

# ---- OLS refit and EBIC scorer (§III.3.0 "EBIC/BIC"; Oct-14 methods.R l.4-7) ----

# Zero-intercept OLS refit on support idx. drop = FALSE keeps a one-column matrix.
ols_rss <- function(X, y, idx, tol) {
  if (!length(idx)) return(list(rss = sum(y^2), rank = 0L))
  z <- stats::lm.fit(X[, idx, drop = FALSE], y, tol = tol)
  list(rss = sum(z$residuals^2), rank = as.integer(z$rank))
}

# EBIC_gamma(S) = n log(RSS_S / n) + |S| log n + 2 gamma log C(p, |S|).
# Candidates: the null support plus the distinct supports with k <= kmax.
# A candidate is valid only if rank == k, RSS finite and RSS > 0; otherwise it scores Inf.
ebic_candidates <- function(X, y, supports, kmax, gammas, tol) {
  n <- nrow(X); p <- ncol(X)
  supports <- c(list(integer()), supports)
  keys <- vapply(supports, support_key, "")
  keep <- !duplicated(keys) & lengths(supports) <= kmax
  supports <- supports[keep]; keys <- keys[keep]
  k <- lengths(supports)
  fits <- lapply(supports, function(s) ols_rss(X, y, s, tol))
  rss <- vapply(fits, `[[`, 0.0, "rss")
  rank <- vapply(fits, `[[`, 0L, "rank")
  valid <- rank == k & is.finite(rss) & rss > 0
  cand <- data.frame(key = keys, k = k, rank = rank, rss = rss, valid = valid,
                     stringsAsFactors = FALSE)
  base <- n * log(rss / n) + k * log(n)
  for (g in names(gammas))
    cand[[g]] <- ifelse(valid, base + 2 * gammas[[g]] * lchoose(p, k), Inf)
  cand
}

# Row index of the minimiser: criterion, then smaller k, then key in C-locale byte
# order (radix sorts character vectors in the C locale, independent of the node).
ebic_pick <- function(cand, column) {
  i <- order(cand[[column]], cand$k, cand$key, method = "radix")[1L]
  if (!is.finite(cand[[column]][i])) stop("no valid EBIC candidate for ", column)
  i
}

# TRUE if the support occurs somewhere on the path at a point that passed its check.
# The null support is always valid (§III.3.1 f).
occurrence_ok <- function(key, path_keys, path_ok) {
  if (!nzchar(key)) return(TRUE)
  any(path_keys == key & path_ok)
}

# ---- rule rows (§III.3.0 "Method registry and rule frame"; "Failures") ----

RULE_CORE_COLS <- c("rule_id", "role", "status", "support", "support_audit", "k",
                    "converged", "diag_flag", "diag_codes", "error")

# values: named list with one element per registered rule id; each element is a named
# list of fields (core columns other than rule_id/role, plus the method's extra columns).
# Missing fields are NA. The frame always has exactly the registered rows, in order.
make_rule_rows <- function(method_row, values) {
  ids <- method_row$rule_ids[[1L]]; roles <- method_row$roles[[1L]]
  extra <- method_row$extra_cols[[1L]]
  if (!setequal(names(values), ids)) stop("rule values do not match the registry")
  cols <- c(RULE_CORE_COLS, extra)
  rows <- lapply(seq_along(ids), function(i) {
    v <- values[[ids[i]]]
    if (length(setdiff(names(v), cols))) stop("unregistered rule field: ",
                                              paste(setdiff(names(v), cols), collapse = ","))
    v$rule_id <- ids[i]; v$role <- roles[i]
    row <- lapply(cols, function(cn) if (is.null(v[[cn]])) NA else v[[cn]])
    names(row) <- cols
    as.data.frame(row, stringsAsFactors = FALSE)
  })
  out <- do.call(rbind, rows)
  out$support <- as.character(out$support); out$support_audit <- as.character(out$support_audit)
  out$status <- as.character(out$status); out$diag_codes <- as.character(out$diag_codes)
  out$error <- as.character(out$error); out$k <- as.integer(out$k)
  out$converged <- as.logical(out$converged); out$diag_flag <- as.logical(out$diag_flag)
  out
}

# A failed fit: every registered rule is failed, support and k NA, never the null model.
# diag_flag is NA because the numerical-quality checks did not complete.
fail_rows <- function(method_row, error, support_audit = NA_character_, converged = FALSE) {
  ids <- method_row$rule_ids[[1L]]
  values <- lapply(ids, function(id)
    list(status = "failed", support = NA_character_, support_audit = support_audit,
         k = NA_integer_, converged = converged, diag_flag = NA, diag_codes = "",
         error = error))
  names(values) <- ids
  make_rule_rows(method_row, values)
}

# ---- condition capture (§III.3.0 "Status"; "One capture layer") ----

# Evaluates expr, storing every warning and message verbatim (muffled) and any error.
with_captured_conditions <- function(expr) {
  warnings <- character(); messages <- character()
  value <- tryCatch(
    withCallingHandlers(expr,
      warning = function(w) {
        warnings <<- c(warnings, conditionMessage(w)); invokeRestart("muffleWarning")
      },
      message = function(m) {
        messages <<- c(messages, conditionMessage(m)); invokeRestart("muffleMessage")
      }),
    error = function(e) structure(list(message = conditionMessage(e)), class = "captured_error"))
  error <- NA_character_
  if (inherits(value, "captured_error")) { error <- value$message; value <- NULL }
  list(value = value, warnings = warnings, messages = messages, error = error)
}

# ---- IO and timing ----

elapsed <- function() unname(proc.time()[["elapsed"]])

utc_now <- function() format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC")

file_sha256 <- function(path) digest::digest(file = path, algo = "sha256")

# float64 little-endian SHA-256 (the weak_response_sha256 convention of Oct-14).
f64_sha256 <- function(x) {
  digest::digest(writeBin(as.double(as.vector(x)), raw(), endian = "little"),
                 algo = "sha256", serialize = FALSE)
}

# Write via a temporary file, then rename (Oct-14 bench_atomic).
atomic_write <- function(path, writefun) {
  tmp <- paste0(path, ".tmp.", Sys.getpid())
  on.exit(unlink(tmp), add = TRUE)
  writefun(tmp)
  if (!file.rename(tmp, path)) stop("atomic rename failed: ", path)
  invisible(path)
}
