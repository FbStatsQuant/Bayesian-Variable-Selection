# common.R -- shared helpers used by F2 (copy for the F2 thread; a later step merges the
# per-method copies into code/R/common.R). Names and signatures follow the master,
# §III.3.0 and §III.3.1 k. Fitting code: it never reads files; it sees only (X, y, foldid, seed, settings).

# ---- Input assertions (§III.3.0 "Input assertions"; §III.3.1 e step 1) -------------------
assert_inputs <- function(X, y, foldid, common) {
  if (!is.matrix(X) || !is.double(X)) stop("X must be a double matrix")
  if (any(grepl("^scaled:", names(attributes(X))))) stop("X carries scaled:* attributes")
  if (any(!is.finite(X))) stop("X has non-finite entries")
  n <- nrow(X)
  if (!is.double(y) || !is.null(dim(y)) || length(y) != n || any(!is.finite(y)))
    stop("y must be a finite double vector of length nrow(X)")
  # Centred columns and sample sd 1 (denominator n - 1), Oct-14 design tolerance.
  if (max(abs(colMeans(X))) >= common$design_tol) stop("X is not centred")
  if (max(abs(colSums(X^2) / (n - 1) - 1)) >= common$design_tol) stop("X columns do not have sd 1")
  if (!is.numeric(foldid) || !is.null(dim(foldid)) || length(foldid) != n ||
      any(!is.finite(foldid)) || any(foldid != round(foldid)))
    stop("foldid must be an integer vector of length n")
  if (!identical(sort(unique(as.integer(foldid))), seq_len(common$nfolds)))
    stop("foldid labels must be exactly 1..", common$nfolds)
  if (any(tabulate(as.integer(foldid), common$nfolds) < common$min_fold_size))
    stop("a fold has fewer than ", common$min_fold_size, " rows")
  invisible(TRUE)
}

assert_pkg_version <- function(pkg, version) {
  found <- as.character(utils::packageVersion(pkg))
  if (!identical(found, version)) stop(sprintf("%s version %s, expected %s", pkg, found, version))
  invisible(TRUE)
}

# ---- Grid and supports (§III.3.1 conventions) ----------------------------------------------
# λ fraction grid: frac = exp(seq(0, log(min_ratio), length.out = nlambda)).
lambda_fraction <- function(grid) exp(seq(0, log(grid$min_ratio), length.out = grid$nlambda))

# Support key: sorted indices joined by ";"; the null support is "".
support_key <- function(idx) paste(sort(as.integer(idx)), collapse = ";")

parse_key <- function(key) {
  if (is.na(key)) return(NA_integer_)
  if (!nzchar(key)) return(integer())
  as.integer(strsplit(key, ";", fixed = TRUE)[[1L]])
}

# ---- OLS refit and EBIC scorer (§III.3.0 "EBIC/BIC"; Oct-14 methods.R l.4-21) -------------
# Zero-intercept OLS on the original y. drop = FALSE keeps a one-variable support a matrix.
ols_rss <- function(X, y, idx, tol) {
  if (!length(idx)) return(list(rss = sum(y^2), rank = 0L))
  z <- lm.fit(X[, idx, drop = FALSE], y, tol = tol)
  list(rss = sum(z$residuals^2), rank = z$rank)
}

# EBIC_γ(S) = n log(RSS_S / n) + |S| log n + 2 γ log C(p, |S|).
# Candidates: the null support plus the distinct supports with k <= kmax. A candidate is
# valid only if rank == k, RSS finite and RSS > 0; an invalid candidate scores Inf.
# gammas is a named vector, e.g. c(ebic1 = 1, ebic05 = 0.5); one score column per name.
ebic_candidates <- function(X, y, supports, kmax, gammas, tol) {
  n <- nrow(X); p <- ncol(X)
  supports <- c(list(integer()), supports)
  keys <- vapply(supports, support_key, "")
  k <- lengths(supports)
  keep <- !duplicated(keys) & k <= kmax
  supports <- supports[keep]; keys <- keys[keep]; k <- k[keep]
  fits <- lapply(supports, function(s) ols_rss(X, y, s, tol))
  rss <- vapply(fits, `[[`, 0.0, "rss")
  rank <- vapply(fits, `[[`, 0L, "rank")
  valid <- rank == k & is.finite(rss) & rss > 0
  out <- data.frame(key = keys, k = k, rank = rank, rss = rss, valid = valid,
                    stringsAsFactors = FALSE)
  for (g in names(gammas)) {
    score <- n * log(rss / n) + k * log(n) + 2 * gammas[[g]] * lchoose(p, k)
    out[[g]] <- ifelse(valid, score, Inf)
  }
  out
}

# Minimiser of one score column. Ties: criterion, then smaller k, then the key in C-locale
# byte order (radix sort does not depend on the node's locale).
ebic_pick <- function(cand, column) {
  i <- order(cand[[column]], cand$k, cand$key, method = "radix")[1L]
  if (!is.finite(cand[[column]][i])) stop("no valid EBIC candidate for ", column)
  k_valid_max <- max(cand$k[cand$valid])
  list(row = i, key = cand$key[i], k = cand$k[i], rss = cand$rss[i],
       crit = cand[[column]][i], k_valid_max = k_valid_max,
       at_largest = cand$k[i] == k_valid_max)
}

# An EBIC choice is valid if some full-data path occurrence of its support passes KKT.
# The null support is always valid (§III.3.1 f).
occurrence_ok <- function(key, path_keys, path_ok) {
  if (!nzchar(key)) return(TRUE)
  any(path_keys == key & path_ok)
}

# ---- Rule rows (§III.3.0 "Method registry and rule frame") ---------------------------------
RULE_FRAME_COLUMNS <- c("rule_id", "role", "status", "support", "support_audit", "k",
                        "converged", "diag_flag", "diag_codes", "error")

# rows: a list named by rule_id; each element a list with status, support, support_audit, k,
# converged, diag_flag, diag_codes, error and any of extra_cols. Rows come out in registry
# order and the set of rule ids must equal the registered set exactly.
make_rule_rows <- function(meth, rows, extra_cols) {
  ids <- meth$rule_ids[[1L]]; roles <- meth$roles[[1L]]
  if (!setequal(names(rows), ids) || length(rows) != length(ids))
    stop("rule rows do not match the registry for ", meth$method_id)
  one <- function(id, role) {
    r <- rows[[id]]
    field <- function(nm, na) if (is.null(r[[nm]])) na else r[[nm]]
    base <- data.frame(rule_id = id, role = role,
                       status = field("status", NA_character_),
                       support = field("support", NA_character_),
                       support_audit = field("support_audit", NA_character_),
                       k = as.integer(field("k", NA_integer_)),
                       converged = as.logical(field("converged", NA)),
                       diag_flag = as.logical(field("diag_flag", NA)),
                       diag_codes = field("diag_codes", ""),
                       error = field("error", NA_character_), stringsAsFactors = FALSE)
    for (nm in extra_cols) base[[nm]] <- field(nm, NA)
    base
  }
  out <- do.call(rbind, Map(one, ids, roles))
  rownames(out) <- NULL
  out
}

# Registered rows for a failed fit: status failed, support, support_audit and k NA,
# converged FALSE (methods whose converged is NA pass converged = NA), diag_flag NA (no
# check ran). Never the null model.
fail_rows <- function(meth, error, extra_cols, converged = FALSE) {
  ids <- meth$rule_ids[[1L]]
  rows <- setNames(lapply(ids, function(id)
    list(status = "failed", support = NA_character_, support_audit = NA_character_,
         k = NA_integer_, converged = converged, diag_flag = NA, diag_codes = "",
         error = error)), ids)
  make_rule_rows(meth, rows, extra_cols)
}

# ---- Condition capture (§III.3.0 "Status", "One capture layer") ---------------------------
# Evaluates expr; stores every warning and message verbatim (muffled), and turns an error
# into a value instead of propagating it.
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
  error <- if (inherits(value, "captured_error")) value$message else NA_character_
  if (!is.na(error)) value <- NULL
  list(value = value, warnings = warnings, messages = messages, error = error)
}

# ---- Timing and IO -------------------------------------------------------------------------
elapsed <- function() unname(proc.time()[["elapsed"]])

utc_now <- function() format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC")

# Write to a temporary file in the same directory, then rename (Oct-14 bench_atomic).
atomic_write <- function(path, writefun) {
  tmp <- paste0(path, ".tmp.", Sys.getpid())
  on.exit(unlink(tmp), add = TRUE)
  writefun(tmp)
  if (!file.rename(tmp, path)) stop("atomic rename failed: ", path)
  invisible(path)
}

file_sha256 <- function(path) digest::digest(file = path, algo = "sha256")

# float64 little-endian SHA-256 (the generator's f64_sha256 / Oct-14 weak_response_sha256).
f64_sha256 <- function(x) {
  digest::digest(writeBin(as.double(as.vector(x)), raw(), endian = "little"),
                 algo = "sha256", serialize = FALSE)
}
