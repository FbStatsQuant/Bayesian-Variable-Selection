# Size-stratified exact enumeration wrapper. Usage:
#   source("exact_stratified.R"); load_strat_backend(dir_with_engine_copy_and_cpp)
#   st <- exact_stratified(X, y, cores = 60)   # control model: ridge 1, IG(0.01,0.01); Bernoulli(0.2) kept as reference
#   res <- apply_size_prior(st, logw)          # logw[k+1] = log prior of ONE model of size k, k = 0..p
log_add_vec <- function(a, b) {
  m <- pmax(a, b); out <- m; f <- is.finite(m)
  out[f] <- m[f] + log(exp(a[f] - m[f]) + exp(b[f] - m[f])); out
}
lse <- function(x) { m <- max(x); if (!is.finite(m)) m else m + log(sum(exp(x - m))) }

.strat <- new.env(parent = globalenv())
load_strat_backend <- function(dir, cache = file.path(tempdir(), paste0("strat_cpp_", Sys.getpid()))) {
  stopifnot(requireNamespace("Rcpp", quietly = TRUE), requireNamespace("parallel", quietly = TRUE))
  # model_context, log_marginal_likelihood, model_members from the frozen engine copy
  sys.source(file.path(dir, "engine_copy", "02_model_and_exact_reference.R"), envir = .strat)
  dir.create(cache, recursive = TRUE, showWarnings = FALSE)
  Rcpp::sourceCpp(file.path(dir, "exact_stratified.cpp"), env = .strat, cacheDir = cache, showOutput = FALSE)
  invisible(TRUE)
}

exact_stratified <- function(X, y, cores = 1L, low_bits = 20L, inclusion_probability = 0.2,
                             variance_shape = 0.01, variance_scale = 0.01, prior_ridge = 1) {
  started <- proc.time()[["elapsed"]]
  p <- ncol(X); stopifnot(p <= 30L)
  low <- min(p, low_bits); nch <- 2^(p - low)
  cfg <- list(variance_shape = variance_shape, variance_scale = variance_scale, prior_ridge = prior_ridge)
  context <- .strat$model_context(X, y, cfg)
  cc <- list(G = context$gram, Xty = context$xy, yty = context$yy, n = context$n, a0 = context$a,
             b0 = context$b, tau = context$ridge, log_Cn = context$log_constant)
  one <- function(h) .strat$exact_stratified_chunk_cpp(cc, inclusion_probability, low, as.integer(h))
  res <- if (cores > 1L) parallel::mclapply(seq.int(0L, nch - 1L), one, mc.cores = cores, mc.preschedule = FALSE)
         else lapply(seq.int(0L, nch - 1L), one)
  bad <- vapply(res, function(r) !is.list(r), TRUE)
  if (any(bad)) stop("chunk failures: ", sum(bad), "; first: ", as.character(res[[which(bad)[1]]]))
  # ---- merge ----
  n_models <- sum(vapply(res, function(r) r$n_models, 0))
  log_Z <- lse(vapply(res, function(r) r$log_Z, 0))
  lpn <- rep(-Inf, p); for (r in res) lpn <- log_add_vec(lpn, r$log_pip_numerator)
  pip <- exp(lpn - log_Z)
  map_log_score <- -Inf; map_code <- 0
  for (r in res) if (r$map_log_score > map_log_score || (r$map_log_score == map_log_score && r$map_code < map_code)) {
    map_log_score <- r$map_log_score; map_code <- r$map_code }
  logZ_k <- apply(do.call(rbind, lapply(res, function(r) r$logZ_k)), 2, lse)
  logN_jk <- matrix(-Inf, p + 1, p)
  for (r in res) logN_jk <- log_add_vec(logN_jk, r$logN_jk)
  dim(logN_jk) <- c(p + 1, p)
  count_k <- Reduce(`+`, lapply(res, function(r) r$count_k))
  top_by_size <- lapply(0:p, function(k) {
    s <- unlist(lapply(res, function(r) r$top_score[k + 1, ])); cd <- unlist(lapply(res, function(r) r$top_code[k + 1, ]))
    keep <- cd >= 0; s <- s[keep]; cd <- cd[keep]
    o <- order(-s, cd)[seq_len(min(20L, length(s)))]
    list(size = k, code = cd[o], log_m = s[o])
  })
  names(top_by_size) <- as.character(0:p)
  dimnames(logN_jk) <- list(paste0("k", 0:p), paste0("j", 1:p))
  list(p = p, logZ_k = logZ_k, logN_jk = logN_jk, count_k = count_k, top_by_size = top_by_size,
       models_evaluated = n_models,
       bernoulli = list(inclusion_probability = inclusion_probability, log_Z = log_Z, pip = pip,
         map_code = map_code, map_variables = .strat$model_members(as.integer(map_code), p), map_log_score = map_log_score),
       context = context, low_bits = low, chunks = nch, cores = cores, seconds = proc.time()[["elapsed"]] - started)
}

# logw[k+1] = log prior probability of ONE specific model of size k (k = 0..p). HPM ties: smaller code.
apply_size_prior <- function(strat, logw) {
  p <- strat$p; stopifnot(length(logw) == p + 1L)
  log_Z <- lse(logw + strat$logZ_k)
  pip <- vapply(seq_len(p), function(j) { v <- logw + strat$logN_jk[, j]; if (all(is.infinite(v))) 0 else exp(lse(v) - log_Z) }, 0)
  best_log_m <- vapply(strat$top_by_size, function(t) if (length(t$log_m)) t$log_m[1] else -Inf, 0)
  best_code <- vapply(strat$top_by_size, function(t) if (length(t$code)) t$code[1] else NA_real_, 0)
  score <- logw + best_log_m
  winners <- which(score == max(score)); kbest <- winners[which.min(best_code[winners])]
  list(log_Z = log_Z, pip = pip, mpm = which(pip > 0.5),
       hpm = .strat$model_members(as.integer(best_code[kbest]), p), hpm_code = best_code[kbest],
       hpm_log_score = score[kbest], hpm_size = kbest - 1L,
       size_posterior = exp(logw + strat$logZ_k - log_Z))
}
bernoulli_logw <- function(p, h) (0:p) * log(h) + (p - 0:p) * log1p(-h)
