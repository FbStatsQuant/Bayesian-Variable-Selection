# Source defines functions only. Compile/install PARNI/engine during bootstrap.
parni_dependencies <- function() {
  for (pkg in c("bvsparni", "Rcpp", "posterior")) {
    if (!requireNamespace(pkg, quietly = TRUE)) stop("Missing required package: ", pkg)
  }
  if (utils::packageVersion("bvsparni") != "0.1.0") stop("Unsupported bvsparni engine version")
  if (utils::packageVersion("posterior") < "1.4.0") stop("posterior >= 1.4.0 required")
}

parni_check_data <- function(X, y, foldid, seed) {
  if (!is.matrix(X) || !is.numeric(X) || nrow(X) < 2L ||
      ncol(X) < 1L || ncol(X) > 30L || any(!is.finite(X)))
    stop("X must be a finite numeric matrix, n >= 2 and 1 <= p <= 30")
  if (!is.numeric(y) || !is.null(dim(y)) || length(y) != nrow(X) || any(!is.finite(y)))
    stop("y must be a finite numeric vector of length nrow(X)")
  if (length(foldid) != nrow(X) || !is.numeric(foldid) || anyNA(foldid) ||
      any(!is.finite(foldid)) || any(foldid != floor(foldid)) || any(foldid < 1L))
    stop("foldid must contain a positive integer per observation")
  if (length(seed) != 1L || !is.numeric(seed) || !is.finite(seed) ||
      seed < 0 || seed > 2147483646 || seed != floor(seed)) stop("Invalid scalar RNG seed")
  invisible(TRUE)
}

parni_tail_events <- function(x) {
  qs <- as.numeric(stats::quantile(x, c(.05, .95), names = FALSE, type = 7))
  events <- list(q05_le = x <= qs[1L], q05_ge = x >= qs[1L],
    q95_le = x <= qs[2L], q95_ge = x >= qs[2L])
  table <- do.call(rbind, lapply(seq_along(events), function(i) {
    event <- events[[i]]
    probability <- mean(event)
    constant <- all(event == event[1L])
    values <- if (constant) c(NA_real_, NA_real_) else suppressWarnings(c(
      posterior::ess_bulk(event * 1), posterior::rhat(event * 1)))
    data.frame(event = names(events)[i], threshold = qs[if (i <= 2L) 1L else 2L],
      probability = probability, ess_bulk = values[1L], rhat = values[2L],
      constant = constant, status = if (constant) "constant_event_unassessable" else
        if (all(is.finite(values))) "estimated" else "unassessable", stringsAsFactors = FALSE)
  }))
  required <- table[!table$constant, , drop = FALSE]
  estimable <- nrow(required) > 0L && all(required$status == "estimated")
  list(table = table, ess = if (estimable) min(required$ess_bulk) else NA_real_,
    rhat = if (estimable) max(required$rhat) else NA_real_)
}

parni_one_diagnostic <- function(x, label, boundary_exempt = FALSE) {
  if (!is.matrix(x) || any(!is.finite(x))) stop("Invalid diagnostic trace")
  constant <- all(x == x[1L])
  event_diagnostics <- parni_tail_events(x)
  if (constant) {
    result <- data.frame(variable = label, rhat = NA_real_, ess_bulk = NA_real_, ess_mean = NA_real_,
      ess_tail = NA_real_, mcse_mean = NA_real_, constant = TRUE,
      ess_tail_event = NA_real_, tail_event_rhat = NA_real_,
      boundary_exempt = boundary_exempt, status = if (boundary_exempt)
        "constant_boundary_unassessable" else "constant_unassessable",
      stringsAsFactors = FALSE)
    result$tail_events <- I(list(event_diagnostics$table))
    return(result)
  }
  values <- suppressWarnings(c(posterior::rhat(x), posterior::ess_bulk(x),
    posterior::ess_tail(x), posterior::mcse_mean(x), posterior::ess_basic(x)))
  # Standard quantile ESS is retained verbatim, including NA at discrete atoms.
  # Its availability does not overwrite the status of estimable mean/bulk checks.
  result <- data.frame(variable = label, rhat = values[1L], ess_bulk = values[2L],
    ess_tail = values[3L], mcse_mean = values[4L], constant = FALSE,
    ess_mean = values[5L], ess_tail_event = event_diagnostics$ess,
    tail_event_rhat = event_diagnostics$rhat,
    boundary_exempt = FALSE, status = if (all(is.finite(values[c(1L, 2L, 4L, 5L)])))
      "estimated" else "unassessable",
    stringsAsFactors = FALSE)
  result$tail_events <- I(list(event_diagnostics$table))
  result
}

parni_diagnostics <- function(chains, pip) {
  p <- ncol(chains[[1L]]$rb)
  rb <- vector("list", p); empirical <- vector("list", p)
  for (j in seq_len(p)) {
    x <- do.call(cbind, lapply(chains, function(z) z$rb[, j]))
    b <- do.call(cbind, lapply(chains, function(z) z$indicator[, j]))
    # Identical boundary RB values contain no mixing information. They are
    # explicitly exempted, not given fabricated Rhat=1 or ESS=number of draws.
    exempt <- all(b == b[1L]) && all(x == x[1L]) &&
      ((b[1L] == 0L && x[1L] <= 1e-8) || (b[1L] == 1L && x[1L] >= 1 - 1e-8))
    rb[[j]] <- parni_one_diagnostic(x, paste0("rb_pip_", j), exempt)
    empirical[[j]] <- parni_one_diagnostic(b, paste0("indicator_", j), FALSE)
  }
  structural <- lapply(c("model_size", "log_target"), function(nm)
    parni_one_diagnostic(do.call(cbind, lapply(chains, `[[`, nm)), nm, FALSE))
  rb <- do.call(rbind, rb); empirical <- do.call(rbind, empirical)
  structural <- do.call(rbind, structural)
  adequate <- function(d, pip_check = FALSE) {
    v <- d$boundary_exempt | (d$status == "estimated" & is.finite(d$rhat) &
      d$rhat <= 1.01 & is.finite(d$ess_bulk) & d$ess_bulk >= 400 &
      is.finite(d$ess_mean) & d$ess_mean >= 400 &
      is.finite(d$ess_tail_event) & d$ess_tail_event >= 400 &
      is.finite(d$tail_event_rhat) & d$tail_event_rhat <= 1.01)
    if (pip_check) v <- v & (d$boundary_exempt | (is.finite(d$mcse_mean) & d$mcse_mean <= .01))
    v[is.na(v)] <- FALSE
    v
  }
  rb$passed <- adequate(rb, TRUE); structural$passed <- adequate(structural)
  # A nonconstant indicator offers an additional mode-exploration diagnostic.
  # If constant within some chains but not all, it is unassessable and fails.
  empirical$passed <- ifelse(empirical$constant, NA, adequate(empirical))
  empirical_gate <- all(empirical$passed[!is.na(empirical$passed)])
  list(rb = rb, empirical = empirical, structural = structural,
    passed = all(rb$passed) && all(structural$passed) && empirical_gate,
    thresholds = list(rhat = 1.01, ess_bulk = 400, ess_mean = 400,
      ess_tail_event = 400, tail_event_rhat = 1.01, rb_mcse = .01),
    tail_diagnostic = paste("Standard posterior::ess_tail is reported without modification.",
      "The gate uses ESS and Rhat of each nonconstant <= and >= event at pooled 5%/95%",
      "quantiles, retaining thresholds and actual probabilities. These are discrete-event",
      "diagnostics, not standard quantile ESS. Nonconstant unassessable events fail."),
    boundary_exemptions = rb$variable[rb$boundary_exempt],
    caveat = "Diagnostics cannot exclude undiscovered modes; constant indicators have undefined Rhat/ESS.")
}

parni_bfdr <- function(pip, q = .1) {
  ord <- order(-pip, seq_along(pip))
  averages <- cumsum(1 - pip[ord]) / seq_along(pip)
  valid <- which(averages <= q + 64 * .Machine$double.eps)
  selected <- rep(FALSE, length(pip))
  if (length(valid)) selected[ord[seq_len(max(valid))]] <- TRUE
  selected
}

parni_compact_chains <- function(chains) {
  # RB conditionals depend on the model, X and y, not on the MCMC path.
  # Keep every model draw and one exact double-precision RB row per model.
  models <- unlist(lapply(chains, `[[`, "model"), use.names = FALSE)
  unique_models <- unique(models)
  first <- match(unique_models, models)
  p <- ncol(chains[[1L]]$rb)
  lookup <- matrix(NA_real_, length(unique_models), p)
  offset <- 0L
  for (chain in chains) {
    take <- which(first > offset & first <= offset + length(chain$model))
    if (length(take)) lookup[take, ] <- chain$rb[first[take] - offset, , drop = FALSE]
    offset <- offset + length(chain$model)
  }
  packed <- lapply(chains, function(chain) {
    reconstructed <- lookup[match(chain$model, unique_models), , drop = FALSE]
    if (!identical(unname(reconstructed), unname(chain$rb)))
      stop("Lossless RB compaction failed: model does not determine conditional PIPs")
    expected_indicator <- vapply(seq_len(p), function(j)
      as.integer(bitwAnd(chain$model, bitwShiftL(1L, j - 1L)) != 0L), integer(length(chain$model)))
    if (!identical(unname(expected_indicator), unname(chain$indicator)))
      stop("Lossless indicator compaction failed")
    chain$rb <- NULL
    chain$indicator <- NULL
    chain
  })
  list(chains = packed, rb_lookup = list(model = unique_models, conditional_pip = lookup),
    representation = "lossless_model_lookup_v1", p = p,
    retained_draws = length(models), unique_retained_models = length(unique_models))
}

parni_expand_raw <- function(raw) {
  # Also reads historical, uncompressed pilot output.
  if (is.null(raw$representation)) return(raw$chains)
  if (!identical(raw$representation, "lossless_model_lookup_v1")) stop("Unknown raw representation")
  lookup <- raw$rb_lookup
  if (anyDuplicated(lookup$model) || nrow(lookup$conditional_pip) != length(lookup$model) ||
      ncol(lookup$conditional_pip) != raw$p || any(!is.finite(lookup$conditional_pip)))
    stop("Invalid RB lookup")
  lapply(raw$chains, function(chain) {
    pos <- match(chain$model, lookup$model)
    if (anyNA(pos)) stop("Model absent from RB lookup")
    chain$rb <- lookup$conditional_pip[pos, , drop = FALSE]
    chain$indicator <- vapply(seq_len(raw$p), function(j)
      as.integer(bitwAnd(chain$model, bitwShiftL(1L, j - 1L)) != 0L), integer(length(chain$model)))
    chain
  })
}

fit_method <- function(X, y, foldid, seed, control = list()) {
  parni_check_data(X, y, foldid, seed)
  parni_dependencies()
  if (!is.list(control)) stop("control must be a list")
  allowed <- c("smoke", "warmup", "samples", "cache_limit")
  if (length(setdiff(names(control), allowed))) stop("Unknown PARNI control")
  smoke <- control$smoke
  if (is.null(smoke)) smoke <- FALSE
  if (!is.logical(smoke) || length(smoke) != 1L || is.na(smoke)) stop("smoke must be TRUE or FALSE")
  defaults <- if (smoke) c(warmup = 300L, samples = 600L) else c(warmup = 5000L, samples = 80000L)
  int_control <- function(name, default, minimum) {
    z <- control[[name]]
    if (is.null(z)) z <- default
    if (length(z) != 1L || !is.numeric(z) || !is.finite(z) || z != floor(z) ||
        z < minimum || z > 1e7) stop("Invalid control: ", name)
    as.integer(z)
  }
  warmup <- int_control("warmup", defaults[["warmup"]], 0L)
  samples <- int_control("samples", defaults[["samples"]], 4L)
  cache_limit <- int_control("cache_limit", 200000L, 1L)
  # Budget overrides are explicitly labeled and never silently called frozen production.
  production_settings <- !smoke && warmup == 5000L && samples == 80000L
  RNGkind("Mersenne-Twister", "Inversion", "Rejection")
  set.seed(as.integer(seed))
  chain_seeds <- as.integer((as.double(seed) + 104729 * seq_len(4L)) %% 2147483646 + 1)
  p <- ncol(X)
  out <- bvsparni::parni_run_cpp(X, y, chain_seeds, warmup, samples, .001, .1 / p, cache_limit)
  chains <- out$chains
  pip_by_chain <- do.call(rbind, lapply(chains, function(z) colMeans(z$rb)))
  emp_by_chain <- do.call(rbind, lapply(chains, function(z) colMeans(z$indicator)))
  pip <- colMeans(pip_by_chain)
  diag <- parni_diagnostics(chains, pip)
  if (any(!is.finite(pip)) || any(pip < 0 | pip > 1) || any(!is.finite(out$beta)))
    stop("Invalid PARNI posterior summary")
  acceptance <- data.frame(chain = seq_len(4L),
    mean_acceptance_probability = vapply(chains, function(z) mean(z$acceptance_probability), numeric(1)),
    acceptance_rate_including_self = vapply(chains, function(z) mean(z$accepted), numeric(1)),
    mutation_rate = vapply(chains, function(z) mean(z$hamming_jump > 0), numeric(1)),
    mean_hamming_jump = vapply(chains, function(z) mean(z$hamming_jump), numeric(1)),
    frozen_omega = vapply(chains, `[[`, numeric(1), "frozen_omega"))
  warnings <- character()
  if (smoke) warnings <- c(warnings, "Smoke budget: not evidence of production MCMC accuracy")
  if (!production_settings && !smoke) warnings <- c(warnings, "Non-frozen budget override: validation only")
  if (!diag$passed) warnings <- c(warnings, "MCMC diagnostics failed; retain and flag this fit")
  if (length(diag$boundary_exemptions)) warnings <- c(warnings,
    "Constant boundary RB coordinates exempted; their mixing is unassessable")
  raw <- parni_compact_chains(chains)
  raw$target_constants_omitted <- "Only constants independent of model"
  list(selected = pip > .5, beta = as.numeric(out$beta), pip = pip,
    converged = isTRUE(diag$passed),
    diagnostics = list(method = "PARNI-B-RM", seed = as.integer(seed), chain_seeds = chain_seeds,
      RNGkind = RNGkind(), budget = list(chains = 4L, warmup = warmup, retained_per_chain = samples),
      production_settings = production_settings, smoke = smoke,
      adaptation = list(target_acceptance = .65, exponent = -.7, pi0 = .001,
        epsilon = .1 / p, independent_chains = TRUE, frozen_after_warmup = TRUE),
      target = list(intercept = FALSE, h = .2, ig_shape = .01, ig_rate = .01,
        precision = "(crossprod(X_S)+I)/n", model_size_cap = NULL),
      pip_estimator = "post-warmup Rao-Blackwell conditional inclusion probabilities",
      pip_by_chain = pip_by_chain, empirical_pip_by_chain = emp_by_chain,
      empirical_pip = colMeans(emp_by_chain), mcmc = diag, acceptance = acceptance,
      foldid_unused = foldid, warnings = warnings,
      cache = out[c("cache_size", "cache_hits", "cache_misses", "cache_limit")],
      package_versions = vapply(c("bvsparni", "Rcpp", "posterior"), function(z)
        as.character(utils::packageVersion(z)), character(1))),
    sensitivity = list(posterior_bfdr_0.1 = parni_bfdr(pip, .1),
      empirical_pip_gt_0.5 = colMeans(emp_by_chain) > .5),
    raw = raw)
}
