# Benchmarks/Exact_best_sub/fit.R — benchmark 3 of the methodology: exact best subset with BIC.
# Sourcing this file defines functions only. See METHOD.md for the frozen protocol and sources.
#
# Classical subset search (Hocking & Leslie 1967) by the Furnival & Wilson (1974) leaps-and-bounds
# branch-and-bound as compiled in leaps::regsubsets(method = "exhaustive"); for each size k the
# minimum-RSS subset without intercept, then BIC(k) = n log(RSS_k / n) + k log n (Schwarz 1978) over
# k = 0..p. No size cap (nvmax = p), empty model eligible, true support size never supplied.
# Contract: fit_method(X, y, foldid, seed, control) -> list(selected, beta, pip = NULL, converged,
# diagnostics, sensitivity, raw). Deterministic: seed and foldid are recorded but unused.

best_subset_settings <- function(p) {
  list(kmax = as.integer(p),            # = p: unrestricted search, no size cap
       crosscheck_kmax = min(6L, p),    # sizes 1..6 re-solved by an independent exact enumeration
       tol = 1e-9,                      # tie / agreement tolerance relative to y'y
       primary_rule = "BIC",
       sensitivity_rules = c("EBIC_0.5", "EBIC_1"),   # EBIC(gamma) = BIC + 2 gamma log choose(p, k), reported only
       leaps_version_min = "3.1")
}

bs_set_string <- function(s) if (length(s)) paste(sort(as.integer(s)), collapse = ",") else ""

bs_validate <- function(X, y) {
  if (!is.matrix(X) || !is.numeric(X) || nrow(X) < 3L || ncol(X) < 1L || any(!is.finite(X)))
    stop("X must be a finite numeric matrix with n >= 3 and p >= 1")
  if (!is.numeric(y) || !is.null(dim(y)) || length(y) != nrow(X) || any(!is.finite(y)) || sum(y^2) == 0)
    stop("y must be a finite nonzero numeric vector of length nrow(X)")
  if (any(colSums(X^2) <= 0)) stop("X columns must have positive squared norms")
  if (nrow(X) <= ncol(X)) stop("Exact best subset without a cap needs n > p (full model must be estimable)")
  invisible(TRUE)
}

# RSS of one support without intercept (QR). NA if rank deficient.
bs_rss <- function(X, y, support) {
  if (!length(support)) return(sum(y^2))
  f <- stats::lm.fit(X[, support, drop = FALSE], y)
  if (f$rank < length(support)) return(NA_real_)
  sum(f$residuals^2)
}
bs_ols <- function(X, y, support) {
  beta <- numeric(ncol(X))
  if (length(support)) beta[support] <- stats::lm.fit(X[, support, drop = FALSE], y)$coefficients
  beta
}

# ---- primary: leaps branch-and-bound over all sizes ------------------------------------------------------
bs_leaps_path <- function(X, y, kmax) {
  if (!requireNamespace("leaps", quietly = TRUE)) stop("package 'leaps' is required")
  p <- ncol(X); kmax <- as.integer(min(kmax, p)); stopifnot(kmax >= 1L)
  Xn <- X; attributes(Xn) <- list(dim = dim(X)); colnames(Xn) <- paste0("x", seq_len(p))
  started <- proc.time()[["elapsed"]]
  warn <- character()
  fit <- withCallingHandlers(
    leaps::regsubsets(x = Xn, y = as.numeric(y), method = "exhaustive", intercept = FALSE,
                      nvmax = kmax, nbest = 1L, really.big = TRUE),
    warning = function(w) { warn <<- c(warn, conditionMessage(w)); invokeRestart("muffleWarning") })
  s <- summary(fit)
  W <- s$which
  if (nrow(W) != kmax) stop(sprintf("leaps returned %d sizes instead of %d (linear dependencies?)", nrow(W), kmax))
  W <- W[, paste0("x", seq_len(p)), drop = FALSE]
  supports <- c(list(integer()), lapply(seq_len(kmax), function(k) which(W[k, ])))
  if (!identical(as.integer(lengths(supports)), 0:kmax)) stop("leaps returned supports of the wrong size")
  if (any(fit$lindep)) stop("leaps flagged linear dependencies among the columns")
  list(supports = lapply(supports, as.integer), rss_leaps = c(sum(y^2), as.numeric(s$rss)),
       warnings = warn, seconds = proc.time()[["elapsed"]] - started,
       method = "leaps::regsubsets exhaustive (Furnival-Wilson branch-and-bound), intercept = FALSE, nbest = 1",
       leaps_version = as.character(utils::packageVersion("leaps")))
}

# ---- reference 1: pure-R brute force over all supports (tests only, p <= 16) -----------------------------
bs_brute_force_path <- function(X, y, kmax, tol = 1e-9) {
  p <- ncol(X); kmax <- min(kmax, p); yy <- sum(y^2); eps <- tol * yy
  stopifnot(p <= 16L)
  out <- list(supports = list(integer()), rss = yy, n_ties = 1L)
  for (k in seq_len(kmax)) {
    S <- utils::combn(p, k)
    r <- apply(S, 2L, function(s) bs_rss(X, y, s))
    best <- min(r, na.rm = TRUE); first <- which(r <= best + eps)[1]
    out$supports[[k + 1L]] <- as.integer(S[, first]); out$rss[k + 1L] <- best
    out$n_ties[k + 1L] <- sum(r <= best + eps, na.rm = TRUE)
  }
  out
}

# ---- reference 2: exact enumeration of one size by rank-one updates on X'X ---------------------------------
# Supports T u {j}, T a (k-1)-subset in lexicographic order, j > max(T): every k-set once.
# RSS(T u j) = RSS(T) - (x_j'Q_T y)^2 / (x_j'Q_T x_j), Q_T the projector off span(X_T). Uses X'X, X'y, y'y only.
bs_rankone_size_k <- function(X, y, k, tol = 1e-9) {
  stopifnot(is.matrix(X), length(y) == nrow(X), k >= 1L, k <= ncol(X))
  p <- ncol(X); G <- crossprod(X); b <- drop(crossprod(X, y)); yy <- sum(y^2); dG <- diag(G)
  eps <- tol * yy; collinear_tol <- 1e-10 * max(dG)
  total <- choose(p, k)
  rss_all <- numeric(total); t_all <- integer(total); j_all <- integer(total); filled <- 0L
  if (k == 1L) {
    rss_all <- yy - b^2 / dG; rss_all[dG <= collinear_tol] <- Inf
    t_all <- rep(0L, p); j_all <- seq_len(p); filled <- p; Ts <- matrix(integer(), 0L, 0L)
  } else {
    Ts <- utils::combn(p, k - 1L)
    for (t in seq_len(ncol(Ts))) {
      Tset <- Ts[, t]; m <- Tset[k - 1L]
      if (m >= p) next
      J <- (m + 1L):p
      R <- tryCatch(chol(G[Tset, Tset, drop = FALSE]), error = function(e) NULL)
      if (is.null(R)) rss_J <- rep(Inf, length(J)) else {
        z <- backsolve(R, b[Tset], transpose = TRUE)
        W <- backsolve(R, G[Tset, J, drop = FALSE], transpose = TRUE)
        num <- b[J] - drop(crossprod(W, z)); den <- dG[J] - colSums(W^2)
        rss_J <- (yy - sum(z^2)) - num^2 / den
        rss_J[den <= collinear_tol] <- Inf
      }
      idx <- filled + seq_along(J)
      rss_all[idx] <- rss_J; t_all[idx] <- t; j_all[idx] <- J; filled <- filled + length(J)
    }
  }
  stopifnot(filled == total)
  fin <- is.finite(rss_all); if (!any(fin)) stop("every support of size ", k, " is collinear")
  best <- min(rss_all[fin]); first <- which(rss_all <= best + eps)[1]
  support <- if (k == 1L) j_all[first] else sort(c(Ts[, t_all[first]], j_all[first]))
  list(support = as.integer(support), rss = best, n_supports = total,
       n_within_tolerance = sum(rss_all <= best + eps), n_collinear_skipped = sum(!fin))
}

# ---- single-swap optimality: min over one-for-one exchanges of RSS(swap) - RSS(support) ----------------------
bs_swap_check <- function(X, y, support, rss = bs_rss(X, y, support), tol = 1e-9) {
  p <- ncol(X); k <- length(support); eps <- tol * sum(y^2)
  if (k == 0L || k == p) return(list(min_gap = NA_real_, n_improving = 0L, n_ties = 0L, n_swaps = 0L))
  out <- setdiff(seq_len(p), support); gaps <- numeric(0)
  for (i in support) for (j in out) gaps <- c(gaps, bs_rss(X, y, sort(c(setdiff(support, i), j))) - rss)
  list(min_gap = min(gaps), n_improving = sum(gaps < -eps), n_ties = sum(abs(gaps) <= eps), n_swaps = length(gaps))
}

# ---- criteria ------------------------------------------------------------------------------------------------
bs_bic <- function(rss, n) { k <- seq_along(rss) - 1L; n * log(rss / n) + k * log(n) }
bs_ebic <- function(rss, n, p, gamma) bs_bic(rss, n) + 2 * gamma * lchoose(p, seq_along(rss) - 1L)
bs_argmin_k <- function(values) which.min(values) - 1L      # first minimum = smaller k

# ---- the path with its verification ---------------------------------------------------------------------------
best_subset_path <- function(X, y, settings, swap_check = TRUE, path_fun = bs_leaps_path) {
  n <- nrow(X); p <- ncol(X); yy <- sum(y^2); tol <- settings$tol
  started <- proc.time()[["elapsed"]]
  K <- as.integer(min(settings$kmax, p))
  lp <- path_fun(X, y, K)
  rss <- vapply(lp$supports, function(s) bs_rss(X, y, s), numeric(1))
  if (anyNA(rss)) stop("a returned support is rank deficient")
  path <- data.frame(k = 0:K, support = vapply(lp$supports, bs_set_string, character(1)), rss = rss, rss_leaps = lp$rss_leaps,
                     BIC = bs_bic(rss, n), EBIC_0.5 = bs_ebic(rss, n, p, 0.5), EBIC_1 = bs_ebic(rss, n, p, 1), stringsAsFactors = FALSE)
  path$rss_rel_diff_leaps <- abs(path$rss - path$rss_leaps) / pmax(1, path$rss)
  t0 <- proc.time()[["elapsed"]]
  path$crosscheck_rss <- NA_real_; path$crosscheck_support <- NA_character_; path$crosscheck_ties <- NA_integer_
  for (k in seq_len(min(settings$crosscheck_kmax, K))) {
    cc <- bs_rankone_size_k(X, y, k, tol)
    path$crosscheck_rss[k + 1L] <- cc$rss; path$crosscheck_support[k + 1L] <- bs_set_string(cc$support); path$crosscheck_ties[k + 1L] <- cc$n_within_tolerance
  }
  path$crosscheck_agree <- ifelse(is.na(path$crosscheck_rss), NA, abs(path$crosscheck_rss - path$rss) <= tol * yy)
  seconds_crosscheck <- proc.time()[["elapsed"]] - t0
  t0 <- proc.time()[["elapsed"]]
  path$swap_min_gap <- NA_real_; path$swap_n_improving <- NA_integer_; path$swap_n_ties <- NA_integer_
  if (swap_check) for (i in seq_len(nrow(path))[-1L]) {
    sc <- bs_swap_check(X, y, lp$supports[[i]], path$rss[i], tol)
    path$swap_min_gap[i] <- sc$min_gap; path$swap_n_improving[i] <- sc$n_improving; path$swap_n_ties[i] <- sc$n_ties
  }
  seconds_swap <- proc.time()[["elapsed"]] - t0
  checks <- list(leaps_rss_matches_qr = max(path$rss_rel_diff_leaps) < 1e-8,
                 crosscheck_agrees = all(path$crosscheck_agree, na.rm = TRUE),
                 swap_optimal = if (swap_check) all(path$swap_n_improving[-1L] == 0L) else NA,
                 rss_monotone = all(diff(path$rss) <= tol * yy),
                 no_leaps_warnings = length(lp$warnings) == 0L,
                 full_search = K == p)
  list(path = path, supports = lp$supports, kmax_used = K, checks = checks, warnings = lp$warnings,
       method = lp$method, leaps_version = lp$leaps_version,
       seconds = c(search = lp$seconds, crosscheck = seconds_crosscheck, swap = seconds_swap, total = proc.time()[["elapsed"]] - started))
}

fit_method <- function(X, y, foldid = NULL, seed = NA_integer_, control = list()) {
  bs_validate(X, y)
  n <- nrow(X); p <- ncol(X)
  settings <- best_subset_settings(p)
  swap_check <- !isTRUE(control$skip_swap_check)   # tests only; production always checks
  res <- best_subset_path(X, y, settings, swap_check = swap_check)
  rules <- list(BIC = bs_argmin_k(res$path$BIC), `EBIC_0.5` = bs_argmin_k(res$path$EBIC_0.5), EBIC_1 = bs_argmin_k(res$path$EBIC_1))
  supports <- lapply(rules, function(k) res$supports[[k + 1L]])
  primary <- settings$primary_rule
  selected <- rep(FALSE, p); selected[supports[[primary]]] <- TRUE
  beta <- bs_ols(X, y, supports[[primary]])
  sensitivity <- lapply(settings$sensitivity_rules, function(nm) { v <- rep(FALSE, p); v[supports[[nm]]] <- TRUE; v })
  names(sensitivity) <- settings$sensitivity_rules
  converged <- all(unlist(res$checks[c("leaps_rss_matches_qr", "crosscheck_agrees", "rss_monotone", "no_leaps_warnings", "full_search")])) &&
    (!swap_check || isTRUE(res$checks$swap_optimal))
  list(selected = selected, beta = beta, pip = NULL, converged = converged,
       diagnostics = list(method = "Exact_best_sub", seed = as.integer(seed), settings = settings,
                          primary_rule = primary,
                          decision = list(rule = primary, k = rules[[primary]], criterion_value = min(res$path$BIC),
                                          support = bs_set_string(supports[[primary]]), rss = res$path$rss[rules[[primary]] + 1L]),
                          rule_decisions = lapply(names(rules), function(nm) list(rule = nm, k = rules[[nm]],
                                          criterion_value = min(res$path[[nm]]), support = bs_set_string(supports[[nm]]))),
                          kmax_used = res$kmax_used, bic_at_kmax = rules$BIC == res$kmax_used,
                          checks = res$checks, path = res$path, warnings = res$warnings,
                          leaps_version = res$leaps_version, search = res$method, seconds = as.list(res$seconds),
                          swap_check_performed = swap_check,
                          foldid_used = FALSE),
       sensitivity = sensitivity,
       raw = list(supports = res$supports))
}
