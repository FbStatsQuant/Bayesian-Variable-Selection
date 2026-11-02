# common.R: shared helpers used by F5 (ABESS), with the master's names and signatures.
# Implements master §III.3.0 (input assertions, EBIC/BIC scorer, rule frame, capture layer,
# failure rows) and the F1-F5 conventions of §III.3.1 (support keys, OLS refit).
# Ported from Oct-14 scripts/methods.R (bench_key, bench_rss, bench_candidates,
# bench_ebic_rows); differences: radix tie order, gamma-named columns, rule-frame columns.
# This file is duplicated across method folders on purpose; a later step merges them.
# It never reads files and receives no oracle information (§III.3.9).

# ---- assertions ----

# §III.3.0 "Input assertions" and §III.3.1 e step 1.
assert_inputs <- function(X, y, foldid, common) {
  stopifnot(is.matrix(X), is.double(X), is.numeric(y), is.null(dim(y)),
            nrow(X) == length(y), all(is.finite(X)), all(is.finite(y)))
  if (any(grepl("^scaled:", names(attributes(X)))))
    stop("X carries scaled:* attributes")
  n <- nrow(X)
  if (max(abs(colMeans(X))) > common$design_tol) stop("X is not centred")
  if (max(abs(sqrt(colSums(X^2) / (n - 1)) - 1)) > common$design_tol)
    stop("X columns do not have sd 1 (denominator n - 1)")
  if (length(foldid) != n) stop("length(foldid) != n")
  # Reject non-integral labels before coercion (as.integer would truncate 1.5 to 1).
  if (!is.numeric(foldid) || any(!is.finite(foldid)) || any(foldid != round(foldid)))
    stop("fold labels must be finite integers")
  if (!identical(sort(unique(as.integer(foldid))), seq_len(common$nfolds)))
    stop("fold labels are not 1..", common$nfolds)
  if (any(tabulate(as.integer(foldid), common$nfolds) < common$min_fold_rows))
    stop("a fold has fewer than ", common$min_fold_rows, " rows")
  invisible(TRUE)
}

# §III.3.1 b: stopifnot(identical(as.character(packageVersion(pkg)), version)).
assert_pkg_version <- function(pkg, version) {
  got <- as.character(utils::packageVersion(pkg))
  if (!identical(got, version)) stop("package ", pkg, " version ", got, " != pinned ", version)
  invisible(TRUE)
}

# ---- supports ----

# Support key: sorted indices joined by ";"; the null support is "" (§III.3.1 conventions).
support_key <- function(idx) paste(sort(as.integer(idx)), collapse = ";")

parse_key <- function(key) {
  if (is.na(key)) return(NA_integer_)
  if (!nzchar(key)) return(integer())
  as.integer(strsplit(key, ";", fixed = TRUE)[[1L]])
}

# ---- OLS refit and EBIC/BIC scorer (§III.3.0 "EBIC/BIC") ----

# Zero-intercept OLS refit on the original y. drop = FALSE keeps a one-variable
# support a matrix (Oct-14 methods.R l.4-7).
ols_rss <- function(X, y, idx, tol) {
  if (!length(idx)) return(list(rss = sum(y^2), rank = 0L))
  z <- lm.fit(X[, idx, drop = FALSE], y, tol = tol)
  list(rss = sum(z$residuals^2), rank = z$rank)
}

# Candidates: the null support plus the distinct supports with k <= kmax.
# EBIC_gamma(S) = n log(RSS_S / n) + k log n + 2 gamma log C(p, k); gamma = 0 is BIC.
# A candidate is valid only if rank == k, RSS is finite and RSS > 0; invalid scores Inf.
# One column per named gamma (ebic1, ebic05, bic).
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
  base <- n * log(rss / n) + k * log(n)
  for (g in names(gammas))
    cand[[g]] <- ifelse(valid, base + 2 * gammas[[g]] * lchoose(p, k), Inf)
  cand
}

# Minimiser of one criterion column. Ties: criterion, then smaller size, then the
# support key in C-locale byte order (order(..., method = "radix"), locale-free).
# Returns the chosen row, k_valid_max, and the informational code ebic_at_largest.
ebic_pick <- function(cand, column) {
  crit <- cand[[column]]
  i <- order(crit, cand$k, cand$key, method = "radix")[1L]
  if (!is.finite(crit[i])) stop("no valid EBIC candidate for ", column)
  k_valid_max <- max(cand$k[cand$valid])
  list(row = i, key = cand$key[i], k = cand$k[i], rss = cand$rss[i], crit = crit[i],
       k_valid_max = k_valid_max,
       codes = if (cand$k[i] == k_valid_max) "ebic_at_largest" else character())
}

# ---- condition capture (§III.3.0 "One capture layer") ----

# Evaluates expr, collecting every warning and message verbatim (muffled) and any error.
with_captured_conditions <- function(expr) {
  warns <- character(); msgs <- character()
  value <- tryCatch(
    withCallingHandlers(expr,
      warning = function(w) { warns <<- c(warns, conditionMessage(w)); invokeRestart("muffleWarning") },
      message = function(m) { msgs  <<- c(msgs,  conditionMessage(m)); invokeRestart("muffleMessage") }),
    error = function(e) e)
  err <- if (inherits(value, "error")) conditionMessage(value) else NA_character_
  list(value = if (inherits(value, "error")) NULL else value,
       warnings = warns, messages = msgs, error = err)
}

# ---- rule frame (§III.3.0 "Method registry and rule frame") ----

method_row <- function(settings, method_id) {
  m <- settings$METHODS[settings$METHODS$method_id == method_id, , drop = FALSE]
  if (nrow(m) != 1L) stop("method ", method_id, " not registered exactly once")
  m
}

# Builds exactly the registered rule rows of a method. `fill` is a named list of
# per-rule lists (keyed by rule_id) with any of: status, support, support_audit, k,
# diag_codes and the method's extra columns. Fit-level values are recycled.
make_rule_rows <- function(settings, method_id, fill, converged, diag_flag, fit_status) {
  m <- method_row(settings, method_id)
  ids <- m$rule_ids[[1L]]; roles <- m$roles[[1L]]; extras <- m$extra_cols[[1L]]
  if (!setequal(names(fill), ids)) stop("rule fill does not match registry for ", method_id)
  rows <- lapply(seq_along(ids), function(j) {
    f <- fill[[ids[j]]]
    get <- function(name, default) if (!is.null(f[[name]])) f[[name]] else default
    r <- data.frame(rule_id = ids[j], role = roles[j],
                    status = get("status", fit_status),
                    support = get("support", NA_character_),
                    support_audit = get("support_audit", NA_character_),
                    k = as.integer(get("k", NA_integer_)),
                    converged = as.logical(converged), diag_flag = as.logical(diag_flag),
                    diag_codes = get("diag_codes", ""), stringsAsFactors = FALSE)
    for (x in extras) r[[x]] <- as.numeric(get(x, NA_real_))
    r
  })
  do.call(rbind, rows)
}

# Failed rows: status "failed", support and k NA; support_audit kept if given (§III.3.0).
fail_rows <- function(settings, method_id, converged, diag_flag, support_audit = NULL) {
  m <- method_row(settings, method_id)
  fill <- lapply(m$rule_ids[[1L]], function(id)
    list(status = "failed", support = NA_character_, k = NA_integer_,
         support_audit = if (is.null(support_audit)) NA_character_ else support_audit[[id]]))
  names(fill) <- m$rule_ids[[1L]]
  make_rule_rows(settings, method_id, fill, converged, diag_flag, "failed")
}

# ---- timing ----

elapsed <- function() proc.time()[["elapsed"]]
