# common.R -- shared helpers used by F1 (master §III.3.0 and §III.3.1 k), with the master's names
# and signatures. Duplicated per method folder on purpose; a later step merges the copies.
# Ported pieces keep a pointer to their Oct-14 origin (Experiments_October_14_Benchmarks/scripts/methods.R).

# ---- input checks ---------------------------------------------------------------------------------

# §III.3.0 "Input assertions" + §III.3.1 e step 1: finite, centred X with sd 1 (n - 1) to within
# design_tol; no scaled:* attributes; y finite of length n; folds labelled 1..nfolds, >= 3 rows each.
assert_inputs <- function(X, y, foldid, common) {
  if (!is.matrix(X) || !is.numeric(X)) stop("X must be a numeric matrix")
  n <- nrow(X)
  if (any(startsWith(names(attributes(X)), "scaled:"))) stop("X carries scaled:* attributes")
  if (!all(is.finite(X))) stop("X has non-finite entries")
  if (max(abs(colMeans(X))) >= common$design_tol) stop("X columns are not centred")
  if (max(abs(colSums(X^2) / (n - 1) - 1)) >= common$design_tol) stop("X columns do not have sd 1")
  if (!is.numeric(y) || !is.null(dim(y)) || length(y) != n || !all(is.finite(y)))
    stop("y must be a finite numeric vector of length nrow(X)")
  if (length(foldid) != n || anyNA(foldid) || any(foldid != round(foldid)))
    stop("foldid must be an integer vector of length n")
  if (!identical(sort(unique(as.integer(foldid))), seq_len(common$nfolds)))
    stop("fold labels must be exactly 1..", common$nfolds)
  if (any(tabulate(as.integer(foldid), common$nfolds) < common$min_fold_rows))
    stop("a fold has fewer than ", common$min_fold_rows, " rows")
  invisible(TRUE)
}

# §III.3.1 b: exact package version.
assert_pkg_version <- function(pkg, version) {
  stopifnot(identical(as.character(utils::packageVersion(pkg)), version))
  invisible(TRUE)
}

# ---- grid and supports ----------------------------------------------------------------------------

# §III.3.1 conventions: frac = exp(seq(0, log(min_ratio), length.out = nlambda)), decreasing from 1.
lambda_fraction <- function(grid) {
  exp(seq(0, log(grid$min_ratio), length.out = grid$nlambda))
}

# Support key: sorted indices joined by ";"; the null support is "" (Oct-14 bench_key).
support_key <- function(idx) {
  paste(sort(as.integer(idx)), collapse = ";")
}

# Inverse of support_key; "" gives integer(0). Rejects malformed keys.
parse_key <- function(key) {
  if (length(key) != 1L || is.na(key)) stop("parse_key: key must be one non-NA string")
  if (!nzchar(key)) return(integer())
  if (!grepl("^[0-9]+(;[0-9]+)*$", key)) stop("parse_key: malformed key '", key, "'")
  idx <- as.integer(strsplit(key, ";", fixed = TRUE)[[1L]])
  if (any(idx < 1L) || is.unsorted(idx, strictly = TRUE)) stop("parse_key: unsorted or invalid key")
  idx
}

# ---- OLS refit and EBIC ---------------------------------------------------------------------------

# Zero-intercept OLS refit on the original y (§III.3.1 conventions; Oct-14 bench_rss).
# drop = FALSE keeps a one-column support a matrix (lm.fit fails on a vector).
ols_rss <- function(X, y, idx, tol) {
  if (!length(idx)) return(list(rss = sum(y^2), rank = 0L))
  z <- stats::lm.fit(X[, idx, drop = FALSE], y, tol = tol)
  list(rss = sum(z$residuals^2), rank = z$rank)
}

# EBIC_γ(S) = n log(RSS_S / n) + k log n + 2γ log C(p, k)   (§III.3.0 "EBIC/BIC").
# Candidates: the null support plus the distinct supports with k <= kmax; supports are
# deduplicated before scoring. Invalid (rank < k, RSS not finite or not > 0) scores Inf.
# `gammas` is a named vector; one score column per name (e.g. ebic1, ebic05).
ebic_candidates <- function(X, y, supports, kmax, gammas, tol) {
  n <- nrow(X); p <- ncol(X)
  supports <- c(list(integer()), supports)
  keys <- vapply(supports, support_key, "")
  keep <- !duplicated(keys) & lengths(supports) <= kmax
  supports <- supports[keep]; keys <- keys[keep]
  fits <- lapply(supports, function(s) ols_rss(X, y, s, tol))
  k    <- lengths(supports)
  rss  <- vapply(fits, `[[`, 0.0, "rss")
  rank <- vapply(fits, `[[`, 0L, "rank")
  valid <- rank == k & is.finite(rss) & rss > 0
  cand <- data.frame(key = keys, k = k, rank = rank, rss = rss, valid = valid,
                     stringsAsFactors = FALSE)
  for (g in names(gammas))
    cand[[g]] <- ifelse(valid, ebic_value(rss, k, n, p, gammas[[g]]), Inf)
  cand
}

ebic_value <- function(rss, k, n, p, gamma) {
  n * log(rss / n) + k * log(n) + 2 * gamma * lchoose(p, k)
}

# Minimiser of one score column: criterion, then smaller k, then key in C-locale byte order
# (method = "radix" sorts strings in the C locale, so the order does not depend on the node).
ebic_pick <- function(cand, column) {
  i <- order(cand[[column]], cand$k, cand$key, method = "radix")[1L]
  if (!is.finite(cand[[column]][i])) stop("ebic_pick: no valid candidate for ", column)
  k_valid_max <- max(cand$k[cand$valid])
  list(row = i, key = cand$key[i], k = cand$k[i], value = cand[[column]][i],
       k_valid_max = k_valid_max, at_largest = cand$k[i] == k_valid_max)
}

# TRUE if the support `key` occurs at a path point whose own checks passed (Oct-14 MCP rule).
occurrence_ok <- function(key, path_keys, path_ok) {
  any(path_keys == key & path_ok)
}

# ---- rule frame -----------------------------------------------------------------------------------

registry_row <- function(methods, method_id) {
  r <- methods[methods$method_id == method_id, , drop = FALSE]
  if (nrow(r) != 1L) stop("method_id '", method_id, "' is not registered exactly once")
  r
}

# Orders diag codes: flag codes first, then informational codes, each in vocabulary order.
format_codes <- function(codes, common) {
  codes <- unique(codes[nzchar(codes)])
  bad <- setdiff(codes, c(common$flag_codes, common$info_codes))
  if (length(bad)) stop("diag code(s) outside the closed vocabulary: ", paste(bad, collapse = ", "))
  vocab <- c(common$flag_codes, common$info_codes)
  paste(vocab[vocab %in% codes], collapse = ";")
}

# Builds the registered rule rows of one fit (§III.3.0 "Method registry and rule frame").
# `values` is a list named by rule_id; each element has status ("ok" / "failed"), support (key),
# codes (character), and `extras` (a named list, subset of the registry's extra_cols).
# A failed rule has support = NA and k = NA; the support it would have chosen goes to support_audit.
# `flag_codes` (method-wide) are written on every row; diag_flag = length(flag_codes) > 0.
make_rule_rows <- function(methods, method_id, values, converged, flag_codes, common) {
  reg <- registry_row(methods, method_id)
  ids <- reg$rule_ids[[1L]]; roles <- reg$roles[[1L]]; extra <- reg$extra_cols[[1L]]
  if (!setequal(names(values), ids) || length(values) != length(ids))
    stop("rule values do not match the registered rule ids of ", method_id)
  rows <- lapply(seq_along(ids), function(j) {
    v <- values[[ids[j]]]
    failed <- identical(v$status, "failed")
    if (!v$status %in% c("ok", "failed")) stop("wrapper rule status must be ok or failed")
    r <- data.frame(rule_id = ids[j], role = roles[j], status = v$status,
                    support = if (failed) NA_character_ else v$support,
                    support_audit = if (failed) v$support else NA_character_,
                    k = if (failed) NA_integer_ else length(parse_key(v$support)),
                    converged = converged, diag_flag = length(flag_codes) > 0L,
                    diag_codes = format_codes(c(flag_codes, v$codes), common),
                    stringsAsFactors = FALSE)
    if (length(setdiff(names(v$extras), extra))) stop("unregistered extra column(s)")
    for (e in extra) r[[e]] <- if (is.null(v$extras[[e]])) NA else v$extras[[e]]
    r
  })
  do.call(rbind, rows)
}

# Registered rows of a failed fit: status failed, support and k NA, extras NA (§III.3.0 "Failures").
# diag_flag is NA: no numerical-quality check completed. support_audit may carry a support for audit.
fail_rows <- function(methods, method_id, support_audit = NA_character_) {
  reg <- registry_row(methods, method_id)
  ids <- reg$rule_ids[[1L]]
  r <- data.frame(rule_id = ids, role = reg$roles[[1L]], status = "failed",
                  support = NA_character_, support_audit = support_audit, k = NA_integer_,
                  converged = reg$converged_on_failure, diag_flag = NA, diag_codes = "",
                  stringsAsFactors = FALSE)
  for (e in reg$extra_cols[[1L]]) r[[e]] <- NA
  r
}

# ---- condition capture ----------------------------------------------------------------------------

# Evaluates `expr`, recording every warning and message verbatim (and muffling them) and
# catching an error. Returns list(value, warnings, messages, error); error is NA_character_
# when there was none, and value is NULL when there was one (§III.3.0 "Status").
with_captured_conditions <- function(expr) {
  warnings <- character(); messages <- character()
  value <- tryCatch(
    withCallingHandlers(expr,
      warning = function(w) { warnings <<- c(warnings, conditionMessage(w)); invokeRestart("muffleWarning") },
      message = function(m) { messages <<- c(messages, conditionMessage(m)); invokeRestart("muffleMessage") }),
    error = function(e) e)
  failed <- inherits(value, "error")
  list(value = if (failed) NULL else value, warnings = warnings, messages = messages,
       error = if (failed) conditionMessage(value) else NA_character_)
}

# ---- IO and timing --------------------------------------------------------------------------------

elapsed <- function(t0) {
  unname(proc.time()[["elapsed"]] - t0)
}

utc_now <- function() {
  format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC")
}

# SHA-256 of a vector as float64 little-endian bytes (the weak_response_sha256 convention).
f64_sha256 <- function(x) {
  digest::digest(writeBin(as.double(as.vector(x)), raw(), endian = "little"),
                 algo = "sha256", serialize = FALSE)
}

file_sha256 <- function(path) {
  digest::digest(file = path, algo = "sha256")
}

# Atomic write: temporary file in the same directory, then rename (Oct-14 bench_atomic).
write_atomic <- function(path, writefun) {
  tmp <- paste0(path, ".tmp.", Sys.info()[["nodename"]], ".", Sys.getpid(), ".",
                format(as.numeric(Sys.time()) * 1e6, scientific = FALSE))   # unique across nodes; no RNG use
  on.exit(unlink(tmp), add = TRUE)
  writefun(tmp)
  if (!file.rename(tmp, path)) stop("atomic rename failed: ", path)
  invisible(path)
}
