# common.R -- shared helpers used by F4 (MCP, SCAD), with the master's names and signatures.
# Implements master §III.3.0 (input assertions, EBIC/BIC scorer, registry, rule frame, one capture
# layer, status/flags/codes) and the F1-F5 conventions of §III.3.1 (OLS refit, support keys,
# λ fraction grid). The same helpers are duplicated in each method folder on purpose; a later
# step merges them. No function here reads anything but its arguments.

# ---- input checks and versions --------------------------------------------------------------

# §III.3.0 "Input assertions" and §III.3.1 e step 1: X finite, centred, sd 1 (denominator n - 1)
# to within design_tol (checked on the variance, as Oct-14 benchmark_fit does); no scaled:*
# attributes; foldid of length n with labels 1..nfolds, each fold with at least min_fold_size rows.
assert_inputs <- function(X, y, foldid, common) {
  if (!is.matrix(X) || !is.double(X)) stop("X must be a double matrix")
  if (!is.numeric(y) || !is.null(dim(y))) stop("y must be a numeric vector")
  n <- nrow(X)
  if (length(y) != n) stop("length(y) != nrow(X)")
  if (any(!is.finite(X)) || any(!is.finite(y))) stop("non-finite X or y")
  if (any(startsWith(names(attributes(X)), "scaled:"))) stop("X carries scaled:* attributes")
  if (max(abs(colMeans(X))) >= common$design_tol) stop("X columns are not centred")
  if (max(abs(colSums(X^2) / (n - 1) - 1)) >= common$design_tol) stop("X columns do not have sd 1")
  if (length(foldid) != n) stop("length(foldid) != n")
  if (any(!is.finite(foldid)) || any(foldid != round(foldid))) stop("foldid must be integer-valued")
  if (!identical(sort(unique(as.integer(foldid))), seq_len(common$nfolds)))
    stop("fold labels must be 1..", common$nfolds)
  if (any(tabulate(as.integer(foldid), common$nfolds) < common$min_fold_size))
    stop("a fold has fewer than ", common$min_fold_size, " rows")
  invisible(TRUE)
}

# §III.3.1 b: exact version assertion.
assert_pkg_version <- function(pkg, version) {
  got <- as.character(utils::packageVersion(pkg))
  if (!identical(got, version)) stop("package ", pkg, " version ", got, " != pinned ", version)
  invisible(TRUE)
}

# ---- grid, supports, OLS refit, EBIC --------------------------------------------------------

# §III.3.1 conventions: frac = exp(seq(0, log(min_ratio), length.out = nlambda)).
lambda_fraction <- function(grid) exp(seq(0, log(grid$min_ratio), length.out = grid$nlambda))

# Support key: sorted indices joined by ";"; the null support is "".
support_key <- function(idx) paste(sort(as.integer(idx)), collapse = ";")
parse_key <- function(key) {
  if (is.na(key)) return(NA_integer_)
  if (!nzchar(key)) return(integer())
  as.integer(strsplit(key, ";", fixed = TRUE)[[1L]])
}

# §III.3.1 conventions "OLS refit": zero-intercept OLS on the original y. drop = FALSE keeps a
# one-variable support a matrix (Oct-14 methods.R l.4-7).
ols_rss <- function(X, y, idx, tol) {
  if (length(idx) == 0L) return(list(rss = sum(y^2), rank = 0L))
  z <- lm.fit(X[, idx, drop = FALSE], y, tol = tol)
  list(rss = sum(z$residuals^2), rank = z$rank)
}

# §III.3.0 "EBIC/BIC": EBIC_g(S) = n log(RSS_S / n) + |S| log n + 2 g log C(p, |S|).
# Candidates: the null support plus the distinct supports with k <= kmax. A candidate is valid
# only if rank == k, RSS is finite and RSS > 0; an invalid candidate scores Inf.
# One criterion column per entry of `gammas`, named by its name (ebic1, ebic05, bic).
ebic_candidates <- function(X, y, supports, kmax, gammas, tol) {
  n <- nrow(X); p <- ncol(X)
  supports <- c(list(integer()), supports)
  keys <- vapply(supports, support_key, "")
  k_all <- lengths(supports)
  keep <- !duplicated(keys) & k_all <= kmax
  supports <- supports[keep]; keys <- keys[keep]; k <- k_all[keep]
  fits <- lapply(supports, function(s) ols_rss(X, y, s, tol))
  rss  <- vapply(fits, function(f) f$rss, 0.0)
  rank <- vapply(fits, function(f) as.integer(f$rank), 0L)
  valid <- rank == k & is.finite(rss) & rss > 0
  out <- data.frame(key = keys, k = k, rank = rank, rss = rss, valid = valid,
                    stringsAsFactors = FALSE)
  for (g in names(gammas)) {
    crit <- n * log(rss / n) + k * log(n) + 2 * gammas[[g]] * lchoose(p, k)
    out[[g]] <- ifelse(valid, crit, Inf)
  }
  out
}

# §III.3.0: minimiser by criterion, then smaller size, then support key in C-locale byte order
# (method = "radix" sorts strings in the C locale, independent of the node's locale).
ebic_pick <- function(cand, column) {
  o <- order(cand[[column]], cand$k, cand$key, method = "radix")
  i <- o[1L]
  if (!is.finite(cand[[column]][i])) stop("no valid EBIC candidate for ", column)
  i
}

# Oct-14 MCP rule (§III.3.1 f, §III.3.4 f): a non-null support is usable only if some path
# occurrence of it passes the point checks; the null support is always valid.
occurrence_ok <- function(key, path_keys, path_ok) {
  if (!nzchar(key)) return(TRUE)
  any(path_keys == key & path_ok)
}

# ---- registry, codes, rule frame ------------------------------------------------------------

# Closed vocabulary of diag_codes (§III.3.0 "Flags" and "Codes"), in the order they are written.
DIAG_CODE_VOCAB <- c("kkt_path", "path_truncated", "L_saturated", "elbo_drop", "sigma2_floor",
                     "capped_intermediate", "tail_unstable", "fixed_point", "ess_tau", "ess_ci95",
                     "crn_mismatch", "lambda_first", "lambda_last", "alpha_edge", "kappa_edge",
                     "floored_selected", "ebic_at_largest")

join_codes <- function(codes) {
  codes <- unique(codes[!is.na(codes) & nzchar(codes)])
  bad <- setdiff(codes, DIAG_CODE_VOCAB)
  if (length(bad)) stop("diag code outside the closed vocabulary: ", paste(bad, collapse = ","))
  paste(DIAG_CODE_VOCAB[DIAG_CODE_VOCAB %in% codes], collapse = ";")
}

registry_row <- function(settings, method_id) {
  M <- settings$METHODS
  i <- which(M$method_id == method_id)
  if (length(i) != 1L) stop("method_id not registered exactly once: ", method_id)
  M[i, , drop = FALSE]
}

# Builds the wrapper's rule frame (§III.3.0): rule_id, role, status, support, support_audit, k,
# converged, diag_flag, diag_codes, error, then the method's extra columns (NA where not set).
# `rules` is a list named by rule_id, in registry order; each element has
#   failed (logical), key (support key chosen by the rule), codes (chr), error (chr or NA),
#   extra (named list of extra-column values).
make_rule_rows <- function(mrow, rules, converged, diag_flag, fit_codes, extra_cols) {
  ids <- mrow$rule_ids[[1L]]; roles <- mrow$roles[[1L]]
  if (!identical(names(rules), ids)) stop("rule ids differ from the registry for ", mrow$method_id)
  rows <- lapply(seq_along(ids), function(r) {
    ru <- rules[[r]]
    row <- data.frame(rule_id = ids[r], role = roles[r],
                      status = if (ru$failed) "failed" else "ok",
                      support = if (ru$failed) NA_character_ else ru$key,
                      support_audit = if (ru$failed) ru$key else NA_character_,
                      k = if (ru$failed) NA_integer_ else length(parse_key(ru$key)),
                      converged = converged, diag_flag = diag_flag,
                      diag_codes = join_codes(c(fit_codes, ru$codes)),
                      error = if (is.null(ru$error)) NA_character_ else ru$error,
                      stringsAsFactors = FALSE)
    for (nm in names(extra_cols))
      row[[nm]] <- if (!is.null(ru$extra[[nm]])) ru$extra[[nm]] else extra_cols[[nm]]
    row
  })
  do.call(rbind, rows)
}

# Rows for a fit that errored before any support was available (§III.3.0 "Failures"):
# exactly the registered rule rows, status failed, support, support_audit and k NA,
# converged FALSE (F4 has a convergence criterion), diag_flag NA (no check was evaluated).
fail_rows <- function(mrow, extra_cols, error) {
  ids <- mrow$rule_ids[[1L]]
  rules <- setNames(lapply(ids, function(id) list(failed = TRUE, key = NA_character_,
                                                  codes = character(), error = error,
                                                  extra = list())), ids)
  rows <- make_rule_rows(mrow, rules, converged = FALSE, diag_flag = NA,
                         fit_codes = character(), extra_cols = extra_cols)
  rows$support_audit <- NA_character_
  rows
}

# A fit-level gate failed after supports were computed (§III.3.0 "Failures"): every rule fails;
# the support each rule chose is kept in support_audit; converged is FALSE.
fail_fit_rows <- function(rows, error) {
  chosen <- ifelse(is.na(rows$support_audit), rows$support, rows$support_audit)
  rows$status <- "failed"; rows$support <- NA_character_; rows$support_audit <- chosen
  rows$k <- NA_integer_; rows$converged <- FALSE
  rows$error <- ifelse(is.na(rows$error), error, paste(error, rows$error, sep = " | "))
  rows
}

# ---- condition capture ------------------------------------------------------------------------

# §III.3.0 "One capture layer": evaluates expr, records every warning and message verbatim (and
# muffles it), and turns an error into a returned message instead of a stop.
with_captured_conditions <- function(expr) {
  warnings <- character(); messages <- character()
  value <- tryCatch(
    withCallingHandlers(expr,
      warning = function(w) { warnings <<- c(warnings, conditionMessage(w)); invokeRestart("muffleWarning") },
      message = function(m) { messages <<- c(messages, conditionMessage(m)); invokeRestart("muffleMessage") }),
    error = function(e) e)
  err <- NA_character_
  if (inherits(value, "error")) { err <- conditionMessage(value); value <- NULL }
  list(value = value, warnings = warnings, messages = messages, error = err)
}

# ---- IO, hashes, timing ---------------------------------------------------------------------

elapsed <- function() proc.time()[["elapsed"]]

# float64 little-endian SHA-256 (the weak_response_sha256 convention of Oct-14; §II.10).
f64_sha256 <- function(x) {
  digest::digest(writeBin(as.double(as.vector(x)), raw(), endian = "little"),
                 algo = "sha256", serialize = FALSE)
}
file_sha256 <- function(path) digest::digest(file = path, algo = "sha256")

# Atomic write (§IV.1.1): temporary file in the same directory, then rename. Each file is atomic;
# the four-file set is protected by the runner's per-pair lock.
atomic_write <- function(path, writefun) {
  tmp <- paste0(path, ".tmp.", Sys.info()[["nodename"]], ".", Sys.getpid())   # unique across nodes
  on.exit(unlink(tmp), add = TRUE)
  writefun(tmp)
  if (!file.rename(tmp, path)) stop("atomic rename failed: ", path)
  invisible(path)
}
