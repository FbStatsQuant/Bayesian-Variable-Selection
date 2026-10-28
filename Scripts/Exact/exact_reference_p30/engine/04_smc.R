# PART III: SMC from the exact composite start to the GLOBAL posterior.
# This function receives X/y-derived context and local tables, NEVER exact PIPs/Z.

make_likelihood_cache <- function(context, capacity) {
  values <- new.env(hash = TRUE, parent = emptyenv())
  entries <- 0L
  hits <- 0L
  misses <- 0L
  evaluate <- function(codes) {
    distinct <- unique(as.integer(codes))
    keys <- as.character(distinct)
    old <- mget(keys, envir = values, ifnotfound = list(NULL), inherits = FALSE)
    known <- !vapply(old, is.null, logical(1))
    scores <- numeric(length(distinct))
    if (any(known)) scores[known] <- unlist(old[known], use.names = FALSE)
    hits <<- hits + sum(known)
    for (i in which(!known)) {
      scores[i] <- log_marginal_likelihood(model_members(distinct[i], context$p), context)
      misses <<- misses + 1L
      if (entries < capacity) {
        assign(keys[i], scores[i], envir = values)
        entries <<- entries + 1L
      }
    }
    scores[match(codes, distinct)]
  }
  list(evaluate = evaluate, statistics = function()
    list(entries = entries, hits = hits, misses = misses, capacity = capacity))
}

effective_sample_size <- function(log_weights) {
  w <- exp(log_weights - max(log_weights))
  sum(w)^2 / sum(w^2)
}

choose_next_temperature <- function(phi, log_ratio, target_ess) {
  ess_at <- function(candidate) effective_sample_size((candidate - phi) * log_ratio)
  if (ess_at(1) >= target_ess) return(1)
  lower <- phi
  upper <- 1
  for (iteration in seq_len(60L)) {
    middle <- (lower + upper) / 2
    if (ess_at(middle) >= target_ess) lower <- middle else upper <- middle
  }
  if (lower <= phi) stop("SMC temperature stalled.")
  lower
}

systematic_resample <- function(weights) {
  n <- length(weights)
  positions <- (runif(1) + 0:(n - 1L)) / n
  cumulative <- cumsum(weights)
  cumulative[n] <- 1
  pmin(findInterval(positions, cumulative) + 1L, n)
}

gibbs_sweep <- function(codes, global_log_lik, phi, cache, composite, cfg) {
  # Loop over coordinates; update all particles for each coordinate.
  # Each particle still follows an ordinary sequential coordinate Gibbs sweep.
  # This ordering is reproducible, but differs from the historical C++ RNG order.
  p <- cfg$p
  pip_rb <- numeric(p)
  log_prior_odds <- qlogis(cfg$inclusion_probability)
  changes <- 0L
  for (j in seq_len(p)) {
    bit <- bitwShiftL(1L, j - 1L)
    included <- bitwAnd(codes, bit) != 0L
    candidate <- bitwXor(codes, bit)
    other_global <- cache$evaluate(candidate)
    block_number <- which(vapply(composite$tables, function(tab) j %in% tab$columns, logical(1)))
    tab <- composite$tables[[block_number]]
    position <- match(j, tab$columns)
    local_code <- local_codes_from_global(codes, tab$columns)
    other_local_code <- bitwXor(local_code, bitwShiftL(1L, position - 1L))
    local_difference <- tab$log_likelihood[other_local_code + 1L] -
      tab$log_likelihood[local_code + 1L]
    orientation <- ifelse(included, -1, 1) # Always form INCLUDE minus EXCLUDE.
    odds <- log_prior_odds + orientation *
      (phi * (other_global - global_log_lik) + (1 - phi) * local_difference)
    probability_included <- plogis(odds)
    pip_rb[j] <- mean(probability_included) # Before this coordinate's draws.
    new_included <- runif(length(codes)) < probability_included
    moved <- new_included != included
    codes[moved] <- candidate[moved]
    global_log_lik[moved] <- other_global[moved]
    changes <- changes + sum(moved)
  }
  list(codes = codes, global_log_lik = global_log_lik, pip_rb = pip_rb, changes = changes)
}

run_composite_smc <- function(context, composite, cfg, progress = TRUE) {
  started <- proc.time()[["elapsed"]]
  set.seed(cfg$seed_smc)
  N <- cfg$particles
  codes <- integer(N)
  for (tab in composite$tables) {
    rows <- sample.int(length(tab$codes), N, replace = TRUE, prob = tab$probability)
    for (position in seq_along(tab$columns))
      codes <- codes + tab$bits[rows, position] * bitwShiftL(1L, tab$columns[position] - 1L)
  }
  cache <- make_likelihood_cache(context, cfg$cache_capacity)
  global <- cache$evaluate(codes)
  phi <- 0
  log_Z <- composite$log_Z0
  diagnostics <- list()
  for (stage in seq_len(cfg$max_stages)) {
    log_ratio <- global - composite_log_likelihood(codes, composite)
    next_phi <- choose_next_temperature(phi, log_ratio, cfg$ess_fraction * N)
    log_weights <- (next_phi - phi) * log_ratio
    log_increment <- log_sum_exp(log_weights) - log(N)
    log_Z <- log_Z + log_increment # Accumulate BEFORE resampling.
    ess <- effective_sample_size(log_weights)
    weights <- exp(log_weights - log_sum_exp(log_weights))
    ancestors <- systematic_resample(weights)
    codes <- codes[ancestors]
    global <- global[ancestors]
    changes <- 0L
    for (sweep in seq_len(cfg$gibbs_sweeps)) {
      moved <- gibbs_sweep(codes, global, next_phi, cache, composite, cfg)
      codes <- moved$codes
      global <- moved$global_log_lik
      changes <- changes + moved$changes
    }
    diagnostics[[stage]] <- data.frame(stage = stage, phi_from = phi, phi_to = next_phi,
      ess = ess, ess_fraction = ess / N, log_ratio_increment = log_increment,
      log_Z = log_Z, changed_coordinates = changes, distinct_models = length(unique(codes)))
    phi <- next_phi
    if (progress) {
      cat(sprintf("  SMC stage %d: phi=%.6f, ESS=%.1f, distinct models=%d\n",
                  stage, phi, ess, length(unique(codes))))
      flush.console()
    }
    if (phi == 1) break
  }
  if (phi != 1) stop("SMC did not reach phi=1 within max_stages.")
  particles <- vapply(seq_len(cfg$p), function(j)
    as.integer(bitwAnd(codes, bitwShiftL(1L, j - 1L)) != 0L), integer(N))
  diagnostics <- do.call(rbind, diagnostics)
  stopifnot(all(diagnostics$ess >= cfg$ess_fraction * N - 1e-6))
  list(log_Z = log_Z, Z = exp(log_Z), pip_rb = moved$pip_rb,
       pip_plain = colMeans(particles), particles = particles,
       weights = rep(1 / N, N), model_codes = codes,
       log_global_likelihood = global, diagnostics = diagnostics,
       log_Z0 = composite$log_Z0, cache = cache$statistics(),
       seconds = proc.time()[["elapsed"]] - started)
}
