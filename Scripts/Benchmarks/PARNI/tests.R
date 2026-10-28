# Run only on NOTS compute nodes after sourcing PARNI/fit.R.
parni_test_permutations <- function(x) {
  if (!length(x)) return(list(integer()))
  unlist(lapply(seq_along(x), function(i)
    lapply(parni_test_permutations(x[-i]), function(z) c(x[i], z))), recursive = FALSE)
}

parni_test_bits <- function(code, p) as.integer(intToBits(as.integer(code)))[seq_len(p)]
parni_test_code <- function(bits) as.integer(sum(bits * 2^(seq_along(bits) - 1L)))

# Deliberately independent dense n x n covariance calculation of the integral.
parni_test_reference_score <- function(X, y, code) {
  n <- nrow(X); p <- ncol(X); ids <- which(parni_test_bits(code, p) == 1L)
  V <- diag(n)
  beta <- numeric(p)
  if (length(ids)) {
    Z <- X[, ids, drop = FALSE]
    Lambda <- (crossprod(Z) + diag(length(ids))) / n
    V <- V + Z %*% solve(Lambda, t(Z))
    beta[ids] <- as.numeric(solve(crossprod(Z) + Lambda, crossprod(Z, y)))
  }
  q <- as.numeric(crossprod(y, solve(V, y)))
  score <- -.5 * as.numeric(determinant(V, logarithm = TRUE)$modulus) -
    (.01 + n / 2) * log(.02 + q) + length(ids) * log(.2) + (p - length(ids)) * log(.8)
  list(score = score, beta = beta)
}

# Independent full random-neighborhood probability and explicitly reversed path.
parni_test_neighborhood_logprob <- function(state, k, pip) {
  bits <- parni_test_bits(state, length(pip))
  a <- pmin(1, pip / (1 - pip)); d <- pmin(1, (1 - pip) / pip)
  eta <- ifelse(bits == 1, d, a)
  if (any(eta[k == 0] == 1)) return(-Inf)
  sum(log(eta[k == 1])) + sum(log1p(-eta[k == 0]))
}

parni_test_path_R <- function(logs, initial, order, flips, pip, omega) {
  state <- initial; lq <- 0
  for (r in seq_along(order)) {
    j <- order[r]
    alternative <- bitwXor(state, bitwShiftL(1L, j - 1L))
    # Inclusion-coordinate odds are computed from A,D directly, rather than
    # from the C++ logit shortcut.
    A <- min(1, pip[j] / (1 - pip[j])); D <- min(1, (1 - pip[j]) / pip[j])
    bit <- parni_test_bits(state, length(pip))[j]
    ratio_eta <- if (bit == 0) D / A else A / D
    logratio <- logs[alternative + 1L] - logs[state + 1L] + log(ratio_eta)
    change <- omega * exp(min(0, logratio)); keep <- 1 - omega
    if (flips[r] == 1L) {
      lq <- lq + log(change / (change + keep)); state <- alternative
    } else lq <- lq + log(keep / (change + keep))
  }
  list(proposal = state, logq = lq)
}

parni_test_detailed_balance <- function(pip, omega) {
  p <- 3L; logs <- c(0, -1.4, .8, -.2, 1.6, -2.1, .4, 1.1)
  pi <- exp(logs - max(logs)); pi <- pi / sum(pi)
  transition <- matrix(0, 2^p, 2^p)
  for (initial in 0:(2^p - 1)) for (neigh in 0:(2^p - 1)) {
    k <- parni_test_bits(neigh, p)
    lpk <- parni_test_neighborhood_logprob(initial, k, pip)
    if (!is.finite(lpk)) next
    orders <- parni_test_permutations(which(k == 1L))
    for (order in orders) for (flipcode in 0:(2^length(order) - 1)) {
      flips <- if (length(order)) parni_test_bits(flipcode, length(order)) else integer()
      cpp <- bvsparni::parni_path_cpp(logs, as.integer(initial), as.integer(order),
        as.integer(flips), pip, omega)
      forward <- parni_test_path_R(logs, initial, order, flips, pip, omega)
      reverse <- parni_test_path_R(logs, forward$proposal, rev(order), rev(flips), pip, omega)
      stopifnot(cpp$proposal == forward$proposal, reverse$proposal == initial,
        abs(cpp$logq_forward - forward$logq) < 1e-11,
        abs(cpp$logq_reverse - reverse$logq) < 1e-11)
      lratio <- logs[forward$proposal + 1L] - logs[initial + 1L] +
        parni_test_neighborhood_logprob(forward$proposal, k, pip) - lpk +
        reverse$logq - forward$logq
      stopifnot(abs(cpp$log_acceptance_ratio - lratio) < 1e-10,
        abs(cpp$log_normalizer_ratio - lratio) < 1e-10)
      prob <- exp(lpk + forward$logq) / length(orders)
      accept <- exp(min(0, lratio))
      transition[initial + 1L, forward$proposal + 1L] <-
        transition[initial + 1L, forward$proposal + 1L] + prob * accept
      transition[initial + 1L, initial + 1L] <-
        transition[initial + 1L, initial + 1L] + prob * (1 - accept)
    }
  }
  flux <- sweep(transition, 1L, pi, `*`)
  stopifnot(max(abs(rowSums(transition) - 1)) < 1e-10,
    min(transition) >= 0, max(abs(flux - t(flux))) < 1e-11,
    max(abs(as.numeric(pi %*% transition) - pi)) < 1e-11)
  list(row_sum_error = max(abs(rowSums(transition) - 1)),
    detailed_balance_error = max(abs(flux - t(flux))))
}

run_method_tests <- function() {
  parni_dependencies()
  results <- list()
  X <- cbind(sin(seq_len(12)), cos(seq_len(12) / 2), seq_len(12) / 13)
  y <- 1 + sin(seq_len(12) * .7) + .25 * X[, 1]
  models <- 0:7
  actual <- bvsparni::parni_scores_cpp(X, y, models)
  expected <- lapply(models, function(m) parni_test_reference_score(X, y, m))
  score_error <- max(abs(actual$log_score - vapply(expected, `[[`, numeric(1), "score")))
  beta_error <- max(abs(actual$beta_mean - do.call(rbind, lapply(expected, `[[`, "beta"))))
  stopifnot(score_error < 1e-9, beta_error < 1e-10)
  # A constant response shift must change the score, catching accidental y-centering.
  shifted <- bvsparni::parni_scores_cpp(X, y + 2, models)
  stopifnot(max(abs(shifted$log_score - actual$log_score)) > 1)
  results$target <- list(score_error = score_error, beta_error = beta_error)
  results$detailed_balance <- list(
    interior = parni_test_detailed_balance(c(.17, .5, .81), .61),
    extreme = parni_test_detailed_balance(c(.001, .999, .37), .94))

  bad <- try(fit_method(X, replace(y, 1, NA_real_), rep(1:3, 4), 2), silent = TRUE)
  stopifnot(inherits(bad, "try-error"))
  bad <- try(fit_method(X, y, rep(1:3, 4), -1), silent = TRUE)
  stopifnot(inherits(bad, "try-error"))
  constant <- parni_one_diagnostic(matrix(1, 20, 4), "constant", TRUE)
  stopifnot(is.na(constant$rhat), is.na(constant$ess_bulk), constant$boundary_exempt)
  inconsistent <- matrix(rep(c(0, 0, 1, 1), each = 20), 20, 4)
  inconsistent_diag <- parni_one_diagnostic(inconsistent, "inconsistent")
  stopifnot(!isTRUE(is.finite(inconsistent_diag$rhat) && inconsistent_diag$rhat <= 1.01))
  # Tail quantile ESS is undefined at a binary upper atom. The explicitly
  # named discrete-event diagnostics remain meaningful and keep real failures.
  set.seed(7341L)
  binary <- matrix(rbinom(16000L, 1L, .2), 4000L, 4L)
  binary_diag <- parni_one_diagnostic(binary, "binary")
  stopifnot(is.na(binary_diag$ess_tail), is.finite(binary_diag$ess_tail_event),
    binary_diag$ess_tail_event > 400, binary_diag$tail_event_rhat <= 1.01,
    all(binary_diag$tail_events[[1L]]$probability >= 0 &
      binary_diag$tail_events[[1L]]$probability <= 1))
  atom <- matrix(sample(c(-3,-2,-1,0),16000L,TRUE,prob=c(.1,.2,.2,.5)),4000L,4L)
  atom_diag <- parni_one_diagnostic(atom,"atom_at_maximum")
  stopifnot(is.na(atom_diag$ess_tail), atom_diag$ess_tail_event > 400,
    atom_diag$tail_event_rhat <= 1.01)
  mismatched <- binary
  mismatched[,4L] <- rbinom(nrow(mismatched), 1L, .8)
  mismatched_diag <- parni_one_diagnostic(mismatched,"bad_between_chain_mixing")
  stopifnot(mismatched_diag$rhat > 1.01, mismatched_diag$tail_event_rhat > 1.01)
  results$discrete_diagnostics <- list(binary=binary_diag,atom=atom_diag,bad=mismatched_diag)
  stopifnot(identical(parni_bfdr(c(.99, .91, .2)), c(TRUE, TRUE, FALSE)))
  stopifnot(identical(parni_bfdr(c(.95, .85, .2)), c(TRUE, TRUE, FALSE)))

  folds <- rep(1:3, 4)
  ctrl <- list(smoke = TRUE, warmup = 20L, samples = 40L)
  a <- fit_method(X, y, folds, 718L, ctrl)
  b <- fit_method(X, y, folds, 718L, ctrl)
  stopifnot(identical(a$raw$chains, b$raw$chains), identical(a$pip, b$pip),
    identical(a$beta, b$beta), !a$diagnostics$production_settings,
    length(unique(a$diagnostics$chain_seeds)) == 4L)
  expanded <- parni_expand_raw(a$raw)
  repacked <- parni_compact_chains(expanded)
  expanded_again <- parni_expand_raw(repacked)
  stopifnot(identical(expanded, expanded_again),
    all(vapply(expanded, function(z) nrow(z$rb) == 40L && nrow(z$indicator) == 40L, logical(1))),
    a$raw$retained_draws == 160L,
    a$raw$unique_retained_models == nrow(a$raw$rb_lookup$conditional_pip))
  results$deterministic <- TRUE
  seeds<-as.integer(c(101,202,303,404))
  first<-bvsparni::parni_run_cpp(X,y,seeds,30L,60L,.001,.1/ncol(X),1000L)
  seeds[2]<-205L
  second<-bvsparni::parni_run_cpp(X,y,seeds,30L,60L,.001,.1/ncol(X),1000L)
  stopifnot(all(vapply(c(1L,3L,4L),function(k)identical(first$chains[[k]],second$chains[[k]]),logical(1))),
            !identical(first$chains[[2]]$model,second$chains[[2]]$model))
  results$chain_seed_isolation<-TRUE

  exact <- exp(actual$log_score - max(actual$log_score)); exact <- exact / sum(exact)
  exact_pip <- colSums(do.call(rbind, lapply(models, parni_test_bits, p = 3)) * exact)
  exact_beta <- colSums(actual$beta_mean * exact)
  mc <- fit_method(X, y, folds, 38212L, list(smoke = TRUE, warmup = 2000L, samples = 6000L))
  err <- abs(mc$pip - exact_pip)
  mcse <- mc$diagnostics$mcmc$rb$mcse_mean
  tolerance <- pmax(.015, 6 * ifelse(is.finite(mcse), mcse, 0))
  stopifnot(all(err < tolerance), max(abs(mc$beta - exact_beta)) < .04,
    max(abs(mc$diagnostics$empirical_pip - exact_pip)) < .035)
  results$exact_mc <- list(exact_pip = exact_pip, rb_pip = mc$pip,
    error = err, tolerance = tolerance, beta_error = max(abs(mc$beta - exact_beta)),
    diagnostics = mc$diagnostics$mcmc)

  # Real production dimensionality, including bit 30 and the full model code.
  X30 <- outer(seq_len(40), seq_len(30), function(i, j) sin(i * (j + .7)) + cos(i / (j + 1)))
  y30 <- sin(seq_len(40) * .45) + .2
  codes <- as.integer(c(0, 2^29, 2^30 - 1, 2^29 + 3))
  cpp30 <- bvsparni::parni_scores_cpp(X30, y30, codes)
  ref30 <- vapply(codes, function(m) parni_test_reference_score(X30, y30, m)$score, numeric(1))
  stopifnot(max(abs(cpp30$log_score - ref30)) < 1e-7)
  edge <- fit_method(X30, y30, rep(1:10, 4), 213L,
    list(smoke = TRUE, warmup = 10L, samples = 20L, cache_limit = 10L))
  stopifnot(length(edge$pip) == 30L, length(edge$selected) == 30L,
    edge$raw$chains[[2L]]$initial_model == 2^30 - 1,
    edge$diagnostics$cache$cache_size <= 10,
    all(is.finite(edge$beta)), all(edge$pip >= 0 & edge$pip <= 1))
  results$p30_target_error <- max(abs(cpp30$log_score - ref30))
  results$passed <- TRUE
  results
}
