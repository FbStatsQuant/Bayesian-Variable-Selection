# Benchmarks/Exact_best_sub/tests.R — run after sourcing Exact_best_sub/fit.R (shared/run_tests.R).
run_method_tests <- function() {
  check <- function(ok, msg) if (!isTRUE(ok)) stop(msg, call. = FALSE)
  expect_error <- function(expr) { r <- tryCatch({ force(expr); NULL }, error = identity); check(inherits(r, "error"), "Invalid input was silently accepted") }
  check(requireNamespace("leaps", quietly = TRUE), "leaps unavailable")
  settings <- best_subset_settings(30L)
  check(settings$kmax == 30L && settings$primary_rule == "BIC" && settings$crosscheck_kmax == 6L, "Frozen settings changed")
  # Toy design: correlated columns, n = 60, p = 12, truth {2, 5, 9, 11}.
  set.seed(4242L)
  n <- 60L; p <- 12L
  Sig <- 0.7^abs(outer(seq_len(p), seq_len(p), "-"))
  X <- matrix(rnorm(n * p), n) %*% chol(Sig); X <- scale(X, center = TRUE, scale = TRUE); attributes(X) <- list(dim = dim(X))
  beta <- numeric(p); beta[c(2, 5, 9, 11)] <- c(1, -0.8, 0.6, 0.5)
  y <- drop(X %*% beta) + rnorm(n)
  bf <- bs_brute_force_path(X, y, p)
  lp <- bs_leaps_path(X, y, p)
  check(identical(lengths(lp$supports), 0:p), "leaps did not return sizes 0..p")
  rss_lp <- vapply(lp$supports, function(s) bs_rss(X, y, s), numeric(1))
  check(all(abs(rss_lp - bf$rss) <= 1e-9 * (1 + bf$rss)), "leaps RSS path differs from brute force")
  check(all(vapply(seq_len(p + 1L), function(i) bf$n_ties[i] > 1 || identical(lp$supports[[i]], bf$supports[[i]]), logical(1))), "leaps supports differ from brute force")
  for (k in 1:4) { cc <- bs_rankone_size_k(X, y, k); check(identical(cc$support, bf$supports[[k + 1]]) && abs(cc$rss - bf$rss[k + 1]) < 1e-9 * (1 + cc$rss), paste("rank-one enumeration differs at k =", k)) }
  # Criterion and the contract.
  f <- fit_method(X, y, foldid = rep(1:10, length.out = n), seed = 1L)
  bic_ref <- n * log(bf$rss / n) + (0:p) * log(n)
  check(max(abs(f$diagnostics$path$BIC - bic_ref)) < 1e-9, "BIC formula differs from n log(RSS/n) + k log n")
  kb <- which.min(bic_ref) - 1L
  check(f$diagnostics$decision$k == kb && identical(which(f$selected), bf$supports[[kb + 1L]]), "BIC argmin or its support is wrong")
  check(is.logical(f$selected) && length(f$selected) == p && is.numeric(f$beta) && length(f$beta) == p && is.null(f$pip), "Contract fields")
  check(all(abs(f$beta[f$selected] - stats::lm.fit(X[, f$selected, drop = FALSE], y)$coefficients) < 1e-12) && all(f$beta[!f$selected] == 0), "beta is not the OLS refit on the selected support")
  check(isTRUE(f$converged) && all(unlist(f$diagnostics$checks)), "Consistency checks failed on the toy")
  check(f$diagnostics$primary_rule == "BIC" && setequal(names(f$sensitivity), c("EBIC_0.5", "EBIC_1")), "Rule bookkeeping changed")
  check(f$diagnostics$kmax_used == p && isTRUE(f$diagnostics$checks$full_search), "Search was capped")
  ebic_ref <- bic_ref + 2 * 0.5 * lchoose(p, 0:p)
  check(identical(which(f$sensitivity$`EBIC_0.5`), bf$supports[[which.min(ebic_ref)]]), "EBIC_0.5 sensitivity support is wrong")
  check(f$diagnostics$path$k[1] == 0 && f$diagnostics$path$rss[1] == sum(y^2), "Empty model row missing")
  # Noise-only response: BIC should pick a tiny model (the k = 0 branch is reachable).
  set.seed(7L); y0 <- rnorm(n)
  f0 <- fit_method(X, y0, seed = 2L, control = list(skip_swap_check = TRUE))
  check(f0$diagnostics$decision$k <= 2L, "Noise response: BIC selected more than two variables")
  # Determinism and invariance to seed / folds.
  f2 <- fit_method(X, y, foldid = sample(rep(1:10, length.out = n)), seed = 99L)
  check(identical(f$selected, f2$selected) && identical(f$beta, f2$beta), "Result depends on seed or folds")
  # Invalid inputs.
  expect_error(fit_method(X[1:10, ], y[1:10]))                  # n <= p
  expect_error(fit_method(X, c(y[-1], NA)))
  expect_error(fit_method(cbind(X, 0), y))                       # zero column
  list(status = "PASS", tests = c("leaps path == brute force (RSS and supports)", "rank-one enumeration == brute force",
    "BIC formula and argmin", "OLS refit coefficients", "consistency checks", "EBIC sensitivities", "empty model eligible",
    "noise response", "deterministic", "invalid inputs rejected"))
}
