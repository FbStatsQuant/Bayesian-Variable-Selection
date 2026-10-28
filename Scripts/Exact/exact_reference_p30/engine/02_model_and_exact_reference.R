# PART I continued: integrated Gaussian scores and exhaustive reference.
# "Exact PIPs" means exact under the fitted posterior, not 0/1 generating truth.

log_sum_exp <- function(x) {
  largest <- max(x)
  if (!is.finite(largest)) return(largest)
  largest + log(sum(exp(x - largest)))
}

model_context <- function(X, y, cfg) {
  n <- nrow(X)
  list(p = ncol(X), n = n, gram = crossprod(X),
       xy = drop(crossprod(X, y)), yy = sum(y^2),
       a = cfg$variance_shape, b = cfg$variance_scale,
       ridge = cfg$prior_ridge,
       log_constant = lgamma(n / 2 + cfg$variance_shape) -
         lgamma(cfg$variance_shape) + cfg$variance_shape * log(2 * cfg$variance_scale) -
         n / 2 * log(pi))
}

# A model is stored as an integer code. Bit j-1 says whether predictor j is in.
# This is simply a compact label, not an approximation to the model.
model_members <- function(code, p) which(bitwAnd(as.integer(code), bitwShiftL(1L, 0:(p - 1L))) != 0L)

log_marginal_likelihood <- function(active, context) {
  k <- length(active)
  determinant_adjustment <- 0
  residual <- context$yy
  if (k > 0L) {
    G <- context$gram[active, active, drop = FALSE]
    prior_precision <- (G + context$ridge * diag(k)) / context$n
    posterior_precision <- G + prior_precision
    # R's chol returns an upper-triangular factor: A = t(R) %*% R.
    R_A <- chol(posterior_precision)
    z <- forwardsolve(t(R_A), context$xy[active])
    residual <- residual - sum(z^2)
    determinant_adjustment <- sum(log(diag(chol(prior_precision)))) -
      sum(log(diag(R_A)))
  }
  if (!is.finite(residual) || 2 * context$b + residual <= 0)
    stop("Invalid integrated residual. Inspect the data and numerical conditioning.")
  context$log_constant + determinant_adjustment -
    (context$n / 2 + context$a) * log(2 * context$b + residual)
}

log_model_prior <- function(size, p, inclusion_probability) {
  size * log(inclusion_probability) + (p - size) * log1p(-inclusion_probability)
}


# Only the exact reference uses compiled code. SMC never receives its tables.
.exact_cpp <- new.env(parent = globalenv())
load_exact_backend <- function(scripts_directory) {
  if (!requireNamespace("Rcpp", quietly = TRUE))
    stop("The p=30 exact backend needs Rcpp and an R-compatible C++ compiler.")
  cache_directory <- Sys.getenv("BVS_CPP_CACHE", unset = file.path(tempdir(), "bvs_exact_cpp"))
  dir.create(cache_directory, recursive = TRUE, showWarnings = FALSE)
  Rcpp::sourceCpp(file.path(scripts_directory, "modules", "exact_reference.cpp"),
                  env = .exact_cpp, cacheDir = cache_directory, showOutput = FALSE)
  invisible(TRUE)
}

# Add quantities represented by their logarithms, including log(0) = -Inf.
log_add <- function(a, b) {
  largest <- pmax(a, b)
  answer <- largest
  finite <- is.finite(largest)
  answer[finite] <- largest[finite] + log(exp(a[finite] - largest[finite]) +
                                       exp(b[finite] - largest[finite]))
  answer
}

exact_posterior <- function(context, cfg, progress = TRUE) {
  if (cfg$exact_backend == "R") return(exact_posterior_R(context, cfg, progress))
  if (!exists("exact_chunk_cpp", envir = .exact_cpp, inherits = FALSE))
    stop("Call load_exact_backend(scripts_directory) before the compiled exact reference.")
  started <- proc.time()[["elapsed"]]
  p <- context$p
  low_bits <- min(p, cfg$exact_low_bits)
  number_of_chunks <- 2^(p - low_bits)
  # The historical compiled engine uses different field names for the same
  # sufficient statistics, precision prior, and integrated-likelihood constant.
  compiled_context <- list(G = context$gram, Xty = context$xy, yty = context$yy,
    n = context$n, a0 = context$a, b0 = context$b, tau = context$ridge,
    log_Cn = context$log_constant)
  chunk_log_Z <- numeric(number_of_chunks)
  log_Z <- -Inf
  log_pip_numerator <- rep(-Inf, p)
  models_evaluated <- 0
  map_code <- 0L
  map_log_score <- -Inf
  for (high_code in seq.int(0L, number_of_chunks - 1L)) {
    # Fix the high bits, then enumerate every combination of the low bits.
    # Chunks partition the entire model space; there is no pruning or sampling.
    chunk <- .exact_cpp$exact_chunk_cpp(compiled_context,
      cfg$inclusion_probability, low_bits, as.integer(high_code))
    stopifnot(chunk$n_models == 2^low_bits)
    chunk_log_Z[high_code + 1L] <- chunk$log_Z
    log_Z <- log_add(log_Z, chunk$log_Z)
    log_pip_numerator <- log_add(log_pip_numerator, chunk$log_pip_numerator)
    models_evaluated <- models_evaluated + chunk$n_models
    if (chunk$map_log_score > map_log_score ||
        (chunk$map_log_score == map_log_score && chunk$map_code < map_code)) {
      map_log_score <- chunk$map_log_score
      map_code <- as.integer(chunk$map_code)
    }
    if (progress && (high_code == 0L || (high_code + 1L) %% 16L == 0L ||
                     high_code + 1L == number_of_chunks)) {
      cat(sprintf("  Exact reference: %.0f / %.0f models (%.1f s)\n",
        models_evaluated, 2^p, proc.time()[["elapsed"]] - started))
      flush.console()
    }
  }
  pip <- exp(log_pip_numerator - log_Z)
  stopifnot(models_evaluated == 2^p, all(is.finite(pip)),
            all(pip >= 0), all(pip <= 1 + 1e-10))
  list(log_Z = log_Z, Z = exp(log_Z), pip = pip,
    models_evaluated = models_evaluated, map_code = map_code,
    map_variables = model_members(map_code, p), map_log_score = map_log_score,
    probability_sum = sum(exp(chunk_log_Z - log_Z)),
    backend = "cpp_exhaustive_cholesky", chunks = number_of_chunks,
    seconds = proc.time()[["elapsed"]] - started)
}

# Readable bounded-memory reference for checking the compiled implementation.
# It is exact at p=30 too, but the per-model R calls make it much slower.
exact_posterior_R <- function(context, cfg, progress = TRUE) {
  started <- proc.time()[["elapsed"]]
  p <- context$p
  number_of_models <- 2^p
  maximum <- -Inf
  total <- 0
  pip_numerator <- numeric(p)
  best_code <- 0L
  best_score <- -Inf
  models_evaluated <- 0
  starts <- seq.int(0L, number_of_models - 1L, by = cfg$exact_chunk_size)
  for (chunk in seq_along(starts)) {
    codes <- seq.int(starts[chunk], min(starts[chunk] + cfg$exact_chunk_size - 1L,
                                      number_of_models - 1L))
    log_weights <- vapply(codes, function(code) {
      active <- model_members(code, p)
      log_marginal_likelihood(active, context) +
        log_model_prior(length(active), p, cfg$inclusion_probability)
    }, numeric(1))
    local_best <- which.max(log_weights)
    if (log_weights[local_best] > best_score) {
      best_code <- as.integer(codes[local_best])
      best_score <- log_weights[local_best]
    }
    next_maximum <- max(maximum, log_weights)
    old_scale <- exp(maximum - next_maximum)
    weights <- exp(log_weights - next_maximum)
    total <- total * old_scale + sum(weights)
    pip_numerator <- pip_numerator * old_scale
    for (j in seq_len(p))
      pip_numerator[j] <- pip_numerator[j] + sum(weights[
        bitwAnd(codes, bitwShiftL(1L, j - 1L)) != 0L])
    maximum <- next_maximum
    models_evaluated <- models_evaluated + length(codes)
    if (progress && (chunk == 1L || chunk %% 32L == 0L || chunk == length(starts))) {
      cat(sprintf("  R exact reference: %.0f / %.0f models (%.1f s)\n",
        models_evaluated, number_of_models, proc.time()[["elapsed"]] - started))
      flush.console()
    }
  }
  log_Z <- maximum + log(total)
  pip <- pip_numerator / total
  stopifnot(models_evaluated == number_of_models, all(pip >= 0), all(pip <= 1 + 1e-12))
  list(log_Z = log_Z, Z = exp(log_Z), pip = pip, models_evaluated = models_evaluated,
    map_code = best_code, map_variables = model_members(best_code, p),
    map_log_score = best_score, probability_sum = total / exp(log_Z - maximum),
    backend = "R_exhaustive_streaming", seconds = proc.time()[["elapsed"]] - started)
}
