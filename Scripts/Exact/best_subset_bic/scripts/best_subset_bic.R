# BVS benchmark campaign / Benchmarks/Exact_best_sub/scripts/best_subset_bic.R
# Benchmark 3 of the methodology: exact best subset with BIC.
#   Classical subset search (Hocking & Leslie 1967, Technometrics 9:531-540) implemented by the
#   Furnival & Wilson (1974, Technometrics 16:499-511) leaps-and-bounds branch-and-bound, as compiled in
#   leaps::regsubsets(method = "exhaustive"); for each size k the subset with minimum RSS (no intercept:
#   the design has none), then
#       BIC(k) = n log(RSS_k / n) + k log n              (Schwarz 1978, Ann. Statist. 6:461-464; constants dropped)
#   minimised over k = 0..p. The empty model is eligible; the true support size is never supplied.
#   No size cap: nvmax = p = 30, so the BIC minimum is the unrestricted optimum and the methodology's
#   "any size cap must be reported" clause is void (kmax_used = 30 is still recorded).
# Exactness refers to the RSS optimum at each size: branch-and-bound prunes only subtrees whose RSS
# lower bound already exceeds the incumbent (Furnival & Wilson Sec. 3), so the returned support is the
# exact L0 optimum of its size. Independent verification, recorded per dataset:
#   (a) the RSS of every returned support is recomputed by QR and is the value used in BIC (rss);
#       leaps' own value is kept as rss_leaps and must agree to 1e-8 relative;
#   (b) sizes 1..crosscheck_kmax (6) are re-solved by a second exact enumeration of all choose(p, k)
#       supports (bs_rankone_size_k, vectorised rank-one updates on X'X; the algorithm of the earlier
#       campaigns' best_subset.R, itself verified against brute force);
#   (c) every returned support is checked for single-swap optimality (no one-for-one exchange lowers RSS);
#   (d) the RSS path is non-increasing in k.
# Ties: exact RSS ties have probability zero under the continuous design; leaps returns one tied support,
# the references the lexicographically first, so agreement is checked on RSS values and tie counts are
# reported. A BIC tie across sizes goes to the smaller k (which.min).
# Code lineage: Others/1_Latest_work_cycle1_and_next/heterogeneous_1v1/scripts/benchmarks/best_subset.R
# (kmax = 12 with extension; EBIC and size-oracle rows), reduced here to the methodology's single rule.

BS_TOL <- 1e-9

# ---- primary: leaps branch-and-bound over all sizes --------------------------------------------------
bs_leaps_path <- function(X, y, kmax) {
  bench_require("leaps")
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

# ---- reference 1: pure-R brute force over all supports (tests only, p <= 16) ---------------------------
bs_brute_force_path <- function(X, y, kmax, tol = BS_TOL) {
  p <- ncol(X); kmax <- min(kmax, p); yy <- sum(y^2); eps <- tol * yy
  stopifnot(p <= 16L)
  out <- list(supports = list(integer()), rss = yy, n_ties = 1L)
  for (k in seq_len(kmax)) {
    S <- utils::combn(p, k)
    r <- apply(S, 2L, function(s) rss_of(X, y, s))
    best <- min(r, na.rm = TRUE); first <- which(r <= best + eps)[1]
    out$supports[[k + 1L]] <- as.integer(S[, first]); out$rss[k + 1L] <- best
    out$n_ties[k + 1L] <- sum(r <= best + eps, na.rm = TRUE)
  }
  out
}

# ---- reference 2: exact enumeration of one size by rank-one updates on X'X --------------------------------
# Supports T u {j}, T a (k-1)-subset in lexicographic order, j > max(T): every k-set once.
# RSS(T u j) = RSS(T) - (x_j'Q_T y)^2 / (x_j'Q_T x_j), Q_T the projector off span(X_T). Only X'X, X'y, y'y used.
bs_rankone_size_k <- function(X, y, k, tol = BS_TOL) {
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

# ---- single-swap optimality: min over one-for-one exchanges of RSS(swap) - RSS(support) -------------------
bs_swap_check <- function(X, y, support, rss = rss_of(X, y, support), tol = BS_TOL) {
  p <- ncol(X); k <- length(support); eps <- tol * sum(y^2)
  if (k == 0L || k == p) return(list(min_gap = NA_real_, n_improving = 0L, n_ties = 0L, n_swaps = 0L))
  out <- setdiff(seq_len(p), support); gaps <- numeric(0)
  for (i in support) for (j in out) gaps <- c(gaps, rss_of(X, y, sort(c(setdiff(support, i), j))) - rss)
  list(min_gap = min(gaps), n_improving = sum(gaps < -eps), n_ties = sum(abs(gaps) <= eps), n_swaps = length(gaps))
}

# ---- the criterion (Methodology, benchmark 3) -------------------------------------------------------------
bs_bic <- function(rss, n) { k <- seq_along(rss) - 1L; n * log(rss / n) + k * log(n) }
bs_argmin_k <- function(values) which.min(values) - 1L      # first minimum = smaller k

# ---- the benchmark -------------------------------------------------------------------------------------------
best_subset_bic_fit <- function(X, y, kmax = 30L, crosscheck_kmax = 6L, tol = BS_TOL, swap_check = TRUE, path_fun = bs_leaps_path) {
  X <- as.matrix(X); y <- as.numeric(y); n <- nrow(X); p <- ncol(X); yy <- sum(y^2)
  started <- proc.time()[["elapsed"]]
  K <- as.integer(min(kmax, p))
  lp <- path_fun(X, y, K)
  rss <- vapply(lp$supports, function(s) rss_of(X, y, s), numeric(1))
  if (anyNA(rss)) stop("a returned support is rank deficient")
  bic <- bs_bic(rss, n); kb <- bs_argmin_k(bic)
  path <- data.frame(k = 0:K, support = vapply(lp$supports, set_string, character(1)), rss = rss, rss_leaps = lp$rss_leaps,
                     bic = bic, stringsAsFactors = FALSE)
  path$rss_rel_diff_leaps <- abs(path$rss - path$rss_leaps) / pmax(1, path$rss)
  # (b) independent exact enumeration for k = 1..crosscheck_kmax
  t0 <- proc.time()[["elapsed"]]
  path$crosscheck_rss <- NA_real_; path$crosscheck_support <- NA_character_; path$crosscheck_ties <- NA_integer_
  for (k in seq_len(min(crosscheck_kmax, K))) {
    cc <- bs_rankone_size_k(X, y, k, tol)
    path$crosscheck_rss[k + 1L] <- cc$rss; path$crosscheck_support[k + 1L] <- set_string(cc$support); path$crosscheck_ties[k + 1L] <- cc$n_within_tolerance
  }
  path$crosscheck_agree <- ifelse(is.na(path$crosscheck_rss), NA, abs(path$crosscheck_rss - path$rss) <= tol * yy)
  seconds_crosscheck <- proc.time()[["elapsed"]] - t0
  # (c) single-swap optimality at every size
  t0 <- proc.time()[["elapsed"]]
  path$swap_min_gap <- NA_real_; path$swap_n_improving <- NA_integer_; path$swap_n_ties <- NA_integer_
  if (swap_check) for (i in seq_len(nrow(path))[-1L]) {
    sc <- bs_swap_check(X, y, lp$supports[[i]], path$rss[i], tol)
    path$swap_min_gap[i] <- sc$min_gap; path$swap_n_improving[i] <- sc$n_improving; path$swap_n_ties[i] <- sc$n_ties
  }
  seconds_swap <- proc.time()[["elapsed"]] - t0
  list(path = path, selected = lp$supports[[kb + 1L]], bic_k = kb, bic_min = bic[kb + 1L], rss_bic = rss[kb + 1L],
       kmax_used = K, bic_at_kmax = kb == K, n = n, p = p, yy = yy,
       monotone_rss = all(diff(path$rss) <= tol * yy),
       crosscheck_kmax = as.integer(min(crosscheck_kmax, K)), crosscheck_all_agree = all(path$crosscheck_agree, na.rm = TRUE),
       swap_all_optimal = if (swap_check) all(path$swap_n_improving[-1L] == 0L) else NA,
       leaps_rss_max_rel_diff = max(path$rss_rel_diff_leaps), n_leaps_warnings = length(lp$warnings),
       warnings = lp$warnings, method = lp$method, leaps_version = lp$leaps_version,
       seconds = c(search = lp$seconds, crosscheck = seconds_crosscheck, swap = seconds_swap, total = proc.time()[["elapsed"]] - started))
}

bench_best_subset_bic <- function(data, cfg, variant = NULL, run = NULL, par = E2$best_subset) {
  X <- bench_X(data); y <- bench_y(data); n <- nrow(X)
  started <- proc.time()[["elapsed"]]
  fit <- best_subset_bic_fit(X, y, kmax = par$kmax, crosscheck_kmax = par$crosscheck_kmax, tol = par$tol)
  seconds <- proc.time()[["elapsed"]] - started
  # reporting-only context (uses the truth AFTER the fit): BIC of the true support and whether the truth is
  # the RSS minimiser of its own size.
  truth <- sort(as.integer(cfg$active)); rss_truth <- rss_of(X, y, truth)
  bic_truth <- n * log(rss_truth / n) + length(truth) * log(n)
  checks <- list(
    bs_leaps_rss_matches_qr = fit$leaps_rss_max_rel_diff < 1e-8,
    bs_crosscheck_agrees = isTRUE(fit$crosscheck_all_agree),
    bs_swap_optimal = isTRUE(fit$swap_all_optimal),
    bs_rss_monotone = isTRUE(fit$monotone_rss),
    bs_no_leaps_warnings = fit$n_leaps_warnings == 0L)
  extra <- list(
    bic_k = fit$bic_k, bic_min = fit$bic_min, rss_bic = fit$rss_bic, kmax_used = fit$kmax_used, bic_at_kmax = fit$bic_at_kmax,
    rss_truth = rss_truth, bic_truth = bic_truth, bic_gap_truth_minus_selected = bic_truth - fit$bic_min,
    rss_best_at_truth_size = fit$path$rss[length(truth) + 1L],
    truth_is_rss_best_at_its_size = setequal(parse_set(fit$path$support[length(truth) + 1L]), truth),
    crosscheck_kmax = fit$crosscheck_kmax, leaps_rss_max_rel_diff = fit$leaps_rss_max_rel_diff,
    crosscheck_ties_max = max(fit$path$crosscheck_ties, na.rm = TRUE), swap_ties_total = sum(fit$path$swap_n_ties, na.rm = TRUE),
    leaps_version = fit$leaps_version,
    seconds_search = unname(fit$seconds[["search"]]), seconds_crosscheck = unname(fit$seconds[["crosscheck"]]),
    seconds_swap = unname(fit$seconds[["swap"]]))
  bench_result("best_subset_bic", fit$selected, pip = NULL, seconds = seconds, extra = extra, checks = checks,
               detail = fit[c("path", "method", "warnings", "seconds")], variant = "", run = NA_integer_, seed = NA_integer_)
}
