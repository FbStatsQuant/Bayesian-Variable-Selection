# PART I: settings and a fresh simulated regression dataset.
# n = observations; p = candidate predictors; particles = Monte Carlo models.
# SMC uses base R; the exact reference can use the compiled Rcpp backend.

scenario_configuration <- function(scenario) {
  stopifnot(scenario %in% c("independent", "mild_correlation", "strong_correlation"))
  list(
    scenario = scenario, n = 100L, p = 30L,
    particles = 10000L, ess_fraction = 0.90, gibbs_sweeps = 1L,
    inclusion_probability = 0.20,
    variance_shape = 0.01, variance_scale = 0.01, prior_ridge = 1,
    noise_sd = 1, block_size = 5L, fdr_budget = 0.05,
    exact_backend = "cpp", exact_low_bits = 18L,
    exact_chunk_size = 4096L, cache_capacity = 100000L,
    max_stages = 1000L,
    seed_data = switch(scenario, independent = 102001L,
                       mild_correlation = 103001L, strong_correlation = 104001L),
    seed_blocks = switch(scenario, independent = 202001L,
                         mild_correlation = 203001L, strong_correlation = 204001L),
    seed_smc = switch(scenario, independent = 302001L,
                      mild_correlation = 303001L, strong_correlation = 304001L),
    # Original signal locations are retained at p = 30.
    active = switch(scenario, independent = c(1L, 4L, 8L, 13L, 18L),
                    mild_correlation = c(2L, 6L, 10L, 15L, 20L),
                    strong_correlation = c(2L, 3L, 8L, 14L, 19L)),
    effects = switch(scenario, independent = c(1, -1, 1.25, -1.25, 0.75),
                     mild_correlation = c(0.8, -0.7, 0.6, -0.9, 0.5),
                     strong_correlation = c(1, -1, 0.6, -0.8, 0.5))
  )
}

check_configuration <- function(cfg) {
  whole <- function(x) length(x) == 1L && is.finite(x) && x == as.integer(x)
  for (key in c("n", "p", "particles", "gibbs_sweeps", "block_size",
                "exact_chunk_size", "exact_low_bits", "cache_capacity", "max_stages",
                "seed_data", "seed_blocks", "seed_smc"))
    if (!whole(cfg[[key]])) stop("Expected a whole number for ", key)
  stopifnot(cfg$n >= 2L, cfg$p >= 1L, cfg$p <= 30L,
            cfg$particles >= 2L, cfg$gibbs_sweeps >= 1L,
            cfg$block_size >= 1L, cfg$block_size <= cfg$p,
            cfg$exact_chunk_size >= 1L, cfg$cache_capacity >= 0L,
            cfg$max_stages >= 1L, cfg$ess_fraction > 0, cfg$ess_fraction < 1,
            cfg$inclusion_probability > 0, cfg$inclusion_probability < 1,
            cfg$variance_shape > 0, cfg$variance_scale > 0, cfg$prior_ridge > 0,
            cfg$noise_sd > 0, cfg$fdr_budget >= 0, cfg$fdr_budget <= 1,
            length(cfg$active) == length(cfg$effects),
            !anyDuplicated(cfg$active), all(cfg$active %in% seq_len(cfg$p)),
            all(is.finite(cfg$effects)))
  stopifnot(cfg$exact_backend %in% c("cpp", "R"),
            cfg$exact_low_bits >= 1L, cfg$exact_low_bits <= 30L)
  invisible(cfg)
}

generate_regression_data <- function(cfg) {
  check_configuration(cfg)
  p <- cfg$p
  covariance <- switch(cfg$scenario,
    independent = diag(p),
    mild_correlation = 0.5^abs(outer(seq_len(p), seq_len(p), "-")),
    strong_correlation = {
      group <- ceiling(seq_len(p) / 5)
      0.85 * outer(group, group, "==") + 0.15 * diag(p)
    })
  set.seed(cfg$seed_data)
  raw_X <- matrix(rnorm(cfg$n * p), nrow = cfg$n) %*% chol(covariance)
  X <- scale(raw_X, center = TRUE, scale = TRUE)
  beta <- numeric(p)
  beta[cfg$active] <- cfg$effects
  y <- drop(X %*% beta) + rnorm(cfg$n, sd = cfg$noise_sd)
  # Do not center y: the fitted intercept is fixed at zero.
  list(X = X, y = y, beta = beta, active = sort(cfg$active),
       covariance = covariance, noise_sd = cfg$noise_sd)
}
