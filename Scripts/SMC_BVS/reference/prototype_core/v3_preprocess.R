# v3_preprocess.R -- preprocessing, statuses and budgets (CORE_SPEC v2 §1; M §§2-4, §6.2).

`%||%` <- function(a, b) if (is.null(a)) b else a

# Seed validation for every entry point that takes a seed (M §2: integer seed s in [1, 2^31 - 1]; code review R-1).
# The C++ seeding x = seed * 2^32 + stream needs exactly this range; fractional, negative or larger values error.
v3_check_seed <- function(seed, what = "seed") {
  if (!is.numeric(seed) || !length(seed) || any(!is.finite(seed)) || any(seed != round(seed)) || any(seed < 1) || any(seed > 2^31 - 1))
    stop(what, " must be integer-valued in [1, 2^31 - 1]")
  invisible(as.numeric(seed))
}

# Exact integer helpers (no floating log2/sqrt rounding at the integer boundaries of M §3).
v3_isqrt <- function(x) { r <- floor(sqrt(x)); while ((r + 1)^2 <= x) r <- r + 1; while (r^2 > x) r <- r - 1; r }
v3_ceil_log2 <- function(x) { c <- 0; while (2^c < x) c <- c + 1; c }   # smallest c with 2^c >= x

# Budgets (M §3): K, B, ell, L, N0, H0, T0, R = 4, tiers e in {0, 1} with (N_e, H_e, T_e) = 4^e (N0, H0, T0);
# exact-branch decision (M §6.2): sum_{k<=K} C(p,k) <= (5 H0 + 4 N0) p, counted with saturating integer arithmetic.
v3_budgets <- function(n, p) {
  n <- as.numeric(n); p <- as.numeric(p)
  K <- min(p, n %/% 2)
  B <- min(v3_isqrt(n), v3_isqrt(p), 16)            # B* = 16 (implementation limit)
  ell <- v3_ceil_log2(n + p + 1)
  L <- max(4, v3_ceil_log2(n + 1))
  N0 <- max(2500, n, p)
  H0 <- (512 * N0 + 2499) %/% 2500                    # ceiling(512 N0 / 2500) in exact integer arithmetic
  T0 <- max(1000, ell^2)
  ex <- .v3cpp$cpp_exact_count(n, p, N0, H0)
  list(n = n, p = p, K = K, B = B, ell = ell, L = L, N0 = N0, H0 = H0, T0 = T0, R = 4,
       tiers = data.frame(e = 0:1, N = c(N0, 4 * N0), H = c(H0, 4 * H0), T = c(T0, 4 * T0)),
       exact_count = ex$count, exact_count_saturated = ex$saturated, exact_threshold = ex$threshold,
       exact_branch = ex$exact_branch)
}

# Standardise one vector (M §4.4): divide by max |x|, compute the mean, centre, divide by the sample SD (n - 1).
# Dividing by max|x| first protects the sums of squares against overflow/underflow for badly scaled inputs.
v3_standardise <- function(x) {
  mx <- max(abs(x))
  x1 <- x / mx
  mu <- mean(x1)
  x2 <- x1 - mu
  s <- sqrt(sum(x2^2) / (length(x) - 1))
  list(z = x2 / s, max = mx, mean = mu, sd = s)
}

# Connected components of {|r_jl| >= 1 - 1e-10} (M §4.5), as lists of original indices (components of size >= 2).
# Column-chunked (chunk x chunk cross-products), so no dense p x p temporary is formed (code review D-1). v3_fit uses
# the C++ version on the context's Gram instead (cpp_dup_components), after the preflight.
v3_dup_components <- function(Xs, orig, chunk = 512) {
  p <- ncol(Xs)
  if (p < 2) return(list())
  s <- sqrt(colSums(Xs^2))
  parent <- seq_len(p)
  find <- function(i) { while (parent[i] != i) i <- parent[i]; i }
  starts <- seq(1, p, by = chunk)
  for (a in starts) for (b in starts[starts >= a]) {
    ia <- a:min(p, a + chunk - 1); ib <- b:min(p, b + chunk - 1)
    r <- crossprod(Xs[, ia, drop = FALSE], Xs[, ib, drop = FALSE]) / outer(s[ia], s[ib])
    hit <- which(abs(r) >= 1 - 1e-10, arr.ind = TRUE)
    for (k in seq_len(nrow(hit))) {
      i <- ia[hit[k, 1]]; j <- ib[hit[k, 2]]
      if (i < j) { x <- find(i); y <- find(j); if (x != y) parent[max(x, y)] <- min(x, y) }
    }
  }
  root <- vapply(seq_len(p), find, 1L)
  comps <- split(seq_len(p), root)
  comps <- comps[lengths(comps) >= 2]
  unname(lapply(comps, function(cc) sort(orig[cc])))
}

# v3_preprocess(X, y) (CORE_SPEC §1; M §4). Status precedence: invalid_input, then no_predictors, then y_constant.
# dup_components = FALSE skips the duplicate check (v3_fit computes it after the preflight).
v3_preprocess <- function(X, y, dup_components = TRUE) {
  bad <- function(reason) list(status = "invalid_input", reason = reason)
  if (is.data.frame(X)) X <- as.matrix(X)
  if (is.null(dim(X)) && is.numeric(X)) X <- matrix(X, ncol = 1)
  if (!is.matrix(X) || !is.numeric(X)) return(bad("X is not a numeric matrix"))
  if (!is.numeric(y) || !is.null(dim(y)) && min(dim(y)) > 1) return(bad("y is not a numeric vector"))
  y <- as.numeric(y)
  n <- nrow(X); p_raw <- ncol(X)
  if (length(y) != n) return(bad("length(y) != nrow(X)"))
  if (any(!is.finite(X)) || any(!is.finite(y))) return(bad("non-finite entry in X or y"))
  if (n < 3) return(bad("n < 3"))
  if (p_raw < 1) return(bad("p < 1"))
  storage.mode(X) <- "double"
  constant <- apply(X, 2, function(x) all(x == x[1]))   # dropped only if all entries are exactly equal
  kept <- which(!constant); dropped <- which(constant)
  base <- list(n = n, p_raw = p_raw, p = length(kept), kept = kept, dropped = dropped)
  if (!length(kept)) return(c(list(status = "no_predictors", hpm = integer(0)), base))
  if (all(y == y[1])) return(c(list(status = "y_constant", hpm = integer(0)), base))
  Xs <- matrix(0, n, length(kept)); cm <- cmu <- csd <- numeric(length(kept))
  for (a in seq_along(kept)) { s <- v3_standardise(X[, kept[a]]); Xs[, a] <- s$z; cm[a] <- s$max; cmu[a] <- s$mean; csd[a] <- s$sd }
  sy <- v3_standardise(y)
  c(list(status = "ok"), base,
    list(X = Xs, y = sy$z, col_max = cm, col_mean = cmu, col_sd = csd,
         y_max = sy$max, y_mean = sy$mean, y_sd_scaled = sy$sd,
         s_y = sy$max * sy$sd,                  # s_y on the raw scale: s_y^2 = ||C y||^2 / (n - 1)
         dup_components = if (isTRUE(dup_components)) v3_dup_components(Xs, kept) else NULL))
}
