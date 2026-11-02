# Preliminary tests; consult TEST_REPORT.md for missing required tests.
root <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2"
e <- new.env(parent = globalenv())
for (f in c("config.R", "common.R", "methods/glmnet_helpers.R", "methods/fit_F3_alasso.R"))
  sys.source(file.path(root, "F3_AdaptiveLasso", f), e)
s <- e$study_settings()
s$GRID$nlambda <- 24L
e$assert_pkg_version <- function(...) invisible(TRUE)
results <- list()
check <- function(name, expr, expect_failure = FALSE) {
  result <- tryCatch({ force(expr); NULL }, error = function(x) conditionMessage(x))
  ok <- if (expect_failure) !is.null(result) else is.null(result)
  results[[length(results)+1L]] <<- data.frame(name = name, outcome = if (ok) "PASS" else "FAIL",
    expected = if (expect_failure) "failure" else "success",
    observed = if (is.null(result)) "success" else result)
}
assert <- function(x) if (!isTRUE(x)) stop("assertion failed")
mutate_function <- function(fun, from, to) {
  count <- 0L
  walk <- function(z) {
    if (identical(z, from)) { count <<- count + 1L; return(to) }
    if (is.call(z)) return(as.call(lapply(as.list(z), walk)))
    z
  }
  body(fun) <- walk(body(fun))
  if (count != 1L) stop("mutation did not match exactly one expression: ", count)
  original_env <- environment(fun)
  test_env <- new.env(parent = original_env)
  code <- paste0("implementation <- ", paste(deparse(fun, width.cutoff = 500L), collapse = "\n"))
  con <- textConnection(code)
  on.exit(close(con), add = TRUE)
  source(con, local = test_env)
  environment(test_env$implementation) <- original_env
  test_env$implementation
}

check("weight overflow: stable normalization", {
  z <- e$alasso_weights(c(1e-308, 1e-308), s$F3)
  assert(all(is.finite(z$v)) && identical(z$v, c(1, 1)))
})
check("weight overflow negative control: naive normalization", {
  w <- abs(c(1e-308, 1e-308))^(-1)
  v <- 2 * w / sum(w)
  assert(all(is.finite(v)) && all(v > 0))
}, TRUE)
check("weight 1e-12", {
  z <- e$alasso_weights(c(1e-12, 1), s$F3)
  assert(all(is.finite(z$v)) && all(z$v > 0) && abs(sum(z$v) - 2) <= 2e-10)
})
check("weight underflow rejected", e$alasso_weights(c(1e-308, 1e308), s$F3), TRUE)
check("unrepresentable reciprocal rejected", e$alasso_weights(c(1e-320, 1), s$F3), TRUE)

set.seed(20261029)
n <- 40L; p <- 30L
X <- scale(matrix(rnorm(n*p), n, p))
attributes(X) <- list(dim = c(n, p))
y <- as.numeric(X[, 3] * 2 + rnorm(n))
fold <- rep(1:10, length.out = n)
rank_guard <- function() {
  Z <- cbind(X[, 1], X[, 1])
  a <- e$ebic_candidates(Z, y, list(1:2), 100, c(ebic1 = 1), 1e-10)
  j <- which(a$k == 2)
  assert(!a$valid[j] && is.infinite(a$ebic1[j]))
}
check("rank-deficient candidate rejected", rank_guard())
saved_rank <- e$ebic_candidates
e$ebic_candidates <- mutate_function(saved_rank,
  quote(valid <- rank == k & is.finite(rss) & rss > 0),
  quote(valid <- is.finite(rss) & rss > 0))
check("implementation mutation: remove EBIC rank gate", rank_guard(), TRUE)
e$ebic_candidates <- saved_rank
tie_guard <- function() {
  a <- data.frame(key = c("2", "1", ""), k = c(1L, 1L, 0L), ebic1 = c(1, 1, 2))
  assert(a$key[e$ebic_pick(a, "ebic1")] == "1")
}
check("tie order criterion, k, key", tie_guard())
saved_pick <- e$ebic_pick
e$ebic_pick <- mutate_function(saved_pick,
  quote(order(cand[[column]], cand$k, cand$key, method = "radix")),
  quote(order(cand[[column]], cand$k, -xtfrm(cand$key), method = "radix")))
check("implementation mutation: reverse EBIC key tie order", tie_guard(), TRUE)
e$ebic_pick <- saved_pick
zero_rss_guard <- function() {
  a <- e$ebic_candidates(X, rep(0, n), list(), 100, c(ebic1 = 1), 1e-10)
  assert(!a$valid[1] && is.infinite(a$ebic1[1]))
}
nonfinite_rss_guard <- function() {
  original <- e$ols_rss
  on.exit(e$ols_rss <- original, add = TRUE)
  e$ols_rss <- function(X, y, idx, tol) if (length(idx)) list(rss = Inf, rank = length(idx)) else original(X, y, idx, tol)
  a <- e$ebic_candidates(X, y, list(1L), 100, c(ebic1 = 1), 1e-10)
  assert(!a$valid[2] && is.infinite(a$ebic1[2]))
}
check("nonpositive RSS scores Inf", zero_rss_guard())
check("nonfinite RSS rejected", nonfinite_rss_guard())
saved_rss <- e$ebic_candidates
e$ebic_candidates <- mutate_function(saved_rss,
  quote(valid <- rank == k & is.finite(rss) & rss > 0), quote(valid <- rank == k))
e$ebic_candidates <- mutate_function(e$ebic_candidates,
  quote(base <- n * log(rss / n) + k * log(n)),
  quote(base <- n * log(ifelse(is.finite(rss) & rss > 0, rss, 1) / n) + k * log(n)))
check("implementation mutation: nonpositive RSS finite score", zero_rss_guard(), TRUE)
check("implementation mutation: nonfinite RSS finite score", nonfinite_rss_guard(), TRUE)
e$ebic_candidates <- saved_rss
check("full-p EBIC hand calculation and differing screened-p pick", {
  set.seed(772)
  q <- qr.Q(qr(scale(matrix(rnorm(n*30), n, 30), center = TRUE, scale = FALSE)))
  z <- q * sqrt(n - 1)
  residual <- rnorm(n); residual <- residual - q[,1:2] %*% crossprod(q[,1:2], residual)
  residual <- as.numeric(residual / sqrt(sum(residual^2)) * sqrt(n))
  yy <- as.numeric(3*z[,1] + .4*z[,2] + residual)
  cand <- e$ebic_candidates(z, yy, list(1L, 1:2), 100, c(ebic1 = 1), 1e-10)
  hand <- n*log(cand$rss/n) + cand$k*log(n) + 2*lchoose(ncol(z), cand$k)
  assert(isTRUE(all.equal(hand, cand$ebic1, tolerance = 1e-12)))
  wrong <- n*log(cand$rss/n) + cand$k*log(n) + 2*lchoose(2, cand$k)
  assert(cand$key[e$ebic_pick(cand, "ebic1")] == "1")
  assert(cand$key[order(wrong, cand$k, cand$key, method = "radix")[1]] == "1;2")
})
# Inject a deterministic pilot only; the singleton second-stage path is real scalar code.
pilot_engine <- function(beta, fail_kkt = FALSE) function(X, y, foldid, alpha, lam, pf, G) {
  L <- length(lam); K <- max(foldid)
  B <- matrix(rep(beta, L), nrow = length(beta))
  k <- rep(if (fail_kkt) 1 else 0, L)
  list(full = list(B = B, s = 1, jerr = 0L, npasses = 0, kkt = k),
       cvm = seq_len(L), cvsd = rep(0, L), kkt_fold = matrix(0, K, L),
       fold_diag = rep(list(list(s = 1, jerr = 0L, npasses = 0)), K))
}
for (p in c(20L, 30L, 120L)) {
  set.seed(200L + p)
  x <- scale(matrix(rnorm(n*p), n, p))
  attributes(x) <- list(dim = c(n, p))
  yy <- as.numeric(2*x[, 3] + rnorm(n))
  e$glmnet_cv_engine <- pilot_engine(rep(0, p))
  null <- e$fit_F3_alasso(x, yy, fold, 1, s)
  check(paste("pilot null p", p), {
    assert(all(null$rules$status == "ok") && all(null$rules$k == 0) &&
           all(null$rules$diag_codes == "pilot_null") && all(null$beta == 0) &&
           nrow(null$diagnostics$candidates) == 1)
  })
  b <- rep(0, p); b[3] <- 2
  e$glmnet_cv_engine <- pilot_engine(b)
  single <- e$fit_F3_alasso(x, yy, fold, 1, s)
  check(paste("pilot single p", p), {
    assert(all(single$rules$status == "ok") && all(grepl("pilot_single", single$rules$diag_codes)) &&
           identical(single$diagnostics$keep, 3L))
    ll <- single$diagnostics$path$lambda
    z <- sum(x[,3]*yy)/n; gram <- sum(x[,3]^2)/n
    expected <- sign(z)*pmax(abs(z)-ll, 0)/gram
    assert(isTRUE(all.equal(single$beta[3], expected[single$rules$index[1]], tolerance = 1e-14)))
  })
  check(paste("independent scalar CV p", p), {
    ll <- single$diagnostics$path$lambda
    mse <- sapply(1:10, function(k) {
      tr <- fold != k; te <- !tr
      z <- sum(x[tr,3]*yy[tr])/sum(tr)
      g <- sum(x[tr,3]^2)/sum(tr)
      coef <- sign(z)*pmax(abs(z)-ll, 0)/g
      colMeans((yy[te] - outer(x[te,3], coef))^2)
    })
    avg <- rowMeans(mse)
    se <- sqrt(rowSums((mse - avg)^2) / 10 / 9)
    imin <- which.min(avg); i1 <- min(which(avg <= avg[imin] + se[imin]))
    assert(isTRUE(all.equal(avg, single$diagnostics$path$cvm, tolerance = 1e-12)))
    assert(isTRUE(all.equal(se, single$diagnostics$path$cvsd, tolerance = 1e-12)))
    assert(single$rules$index[1] == imin && single$rules$index[2] == i1)
  })
  check(paste("scalar CV wrong denominator negative control p", p), {
    ll <- single$diagnostics$path$lambda
    wrong <- sapply(1:10, function(k) {
      tr <- fold != k; te <- !tr
      z <- sum(x[tr,3]*yy[tr])/sum(tr)
      g <- sum(x[,3]^2)/n
      coef <- sign(z)*pmax(abs(z)-ll, 0)/g
      colMeans((yy[te] - outer(x[te,3], coef))^2)
    })
    assert(isTRUE(all.equal(rowMeans(wrong), single$diagnostics$path$cvm, tolerance = 1e-12)))
  }, TRUE)
  {
    perm <- c(3L, seq_len(p)[-3L]); bp <- rep(0, p); bp[1] <- 2
    e$glmnet_cv_engine <- pilot_engine(bp)
    mapped <- e$fit_F3_alasso(x[, perm, drop = FALSE], yy, fold, 1, s)
    check(paste("permuted singleton maps support p", p), {
      assert(identical(mapped$diagnostics$keep, 1L))
      for (j in seq_len(nrow(single$rules))) {
        orig <- e$parse_key(single$rules$support[j])
        back <- sort(perm[e$parse_key(mapped$rules$support[j])])
        assert(identical(orig, back))
      }
    })
    check(paste("mapping negative control: wrong inverse map p", p), {
      orig <- e$parse_key(single$rules$support[1])
      wrong <- e$parse_key(mapped$rules$support[1])
      assert(length(orig) > 0 && identical(orig, wrong))
    }, TRUE)
    e$glmnet_cv_engine <- pilot_engine(b)
    real_scalar <- e$scalar_cv_engine
    e$scalar_cv_engine <- local({ original <- real_scalar; function(...) {
      z <- original(...); ii <- e$cv_choose(z$cvm, z$cvsd)[["min"]]
      z$full$kkt[ii] <- 1; z
    }})
    bad_second <- e$fit_F3_alasso(x, yy, fold, 1, s)
    second_kkt_guard <- function(result) {
      assert(result$rules$status[1] == "failed")
      pen <- result$coefficients$cv_min$beta_pen
      assert(all(is.finite(pen)))
      assert(identical(e$support_key(which(pen != 0)), result$rules$support_audit[1]))
    }
    check(paste("selected second-stage KKT failure p", p), second_kkt_guard(bad_second))
    saved_body <- e$alasso_fit_body
    e$alasso_fit_body <- mutate_function(saved_body,
      quote(!full_ok[imin] || any(!fold_ok[, imin])), quote(FALSE))
    masked_second <- e$fit_F3_alasso(x, yy, fold, 1, s)
    check(paste("implementation mutation: selected second-stage KKT p", p),
          second_kkt_guard(masked_second), TRUE)
    e$alasso_fit_body <- saved_body
    e$scalar_cv_engine <- real_scalar
  }
  e$glmnet_cv_engine <- pilot_engine(b, TRUE)
  failed <- e$fit_F3_alasso(x, yy, fold, 1, s)
  check(paste("pilot KKT failure p", p), assert(all(failed$rules$status == "failed")))
  check(paste("pilot failure negative control p", p), {
    fake <- failed; fake$rules$status <- "ok"
    assert(all(fake$rules$status == "failed"))
  }, TRUE)
}
# Mutation controls replace actual function expressions, then run the same guards.
saved <- e$alasso_weights
e$alasso_weights <- mutate_function(saved, quote(r <- w / max(w)), quote(r <- w))
check("implementation mutation: unstable weights", {
  v <- e$alasso_weights(c(1e-308, 1e-308), s$F3)$v
  assert(all(is.finite(v)) && all(v > 0))
}, TRUE)
e$alasso_weights <- saved

saved <- e$ebic_candidates
e$ebic_candidates <- mutate_function(saved, quote(p <- ncol(X)),
  quote(p <- length(unique(unlist(supports)))))
check("implementation mutation: screened-p EBIC", {
  a <- e$ebic_candidates(X, y, list(1L, 1:2), 100, c(ebic1 = 1), 1e-10)
  correct <- n*log(a$rss/n) + a$k*log(n) + 2*lchoose(ncol(X), a$k)
  assert(isTRUE(all.equal(correct, a$ebic1, tolerance = 1e-12)))
}, TRUE)
e$ebic_candidates <- saved

saved <- e$scalar_cv_engine
e$scalar_cv_engine <- mutate_function(saved,
  quote(gram <- sum(xx * xx) / length(yy)), quote(gram <- (n - 1) / n))
e$glmnet_cv_engine <- pilot_engine(b)
wrong_fold <- e$fit_F3_alasso(x, yy, fold, 1, s)
check("implementation mutation: fold Gram", {
  ll <- wrong_fold$diagnostics$path$lambda
  mse <- sapply(1:10, function(k) {
    tr <- fold != k; te <- !tr
    z <- sum(x[tr,3]*yy[tr])/sum(tr); g <- sum(x[tr,3]^2)/sum(tr)
    coef <- sign(z)*pmax(abs(z)-ll, 0)/g
    colMeans((yy[te] - outer(x[te,3], coef))^2)
  })
  assert(isTRUE(all.equal(rowMeans(mse), wrong_fold$diagnostics$path$cvm, tolerance = 1e-12)))
}, TRUE)
e$scalar_cv_engine <- saved

saved <- e$alasso_fit_body
e$alasso_fit_body <- mutate_function(saved, quote(B[keep, ] <- cv$full$B),
                                      quote(B[seq_len(m), ] <- cv$full$B))
e$glmnet_cv_engine <- pilot_engine(b)
wrong_map <- e$fit_F3_alasso(x, yy, fold, 1, s)
check("implementation mutation: index mapping", {
  assert(identical(wrong_map$diagnostics$keep, 3L))
  assert(3L %in% e$parse_key(wrong_map$rules$support[1]))
}, TRUE)
e$alasso_fit_body <- mutate_function(saved,
  quote(cv1$full$kkt[ip] > G$kkt_rel_tol), quote(FALSE))
e$glmnet_cv_engine <- pilot_engine(b, TRUE)
masked <- e$fit_F3_alasso(x, yy, fold, 1, s)
check("implementation mutation: pilot KKT propagation", {
  assert(all(masked$rules$status == "failed"))
}, TRUE)
e$alasso_fit_body <- saved
sys.source(file.path(root, "F3_AdaptiveLasso", "methods/glmnet_helpers.R"), e)
e$glmnet_target_path <- function(Xd, yd, alpha, lam, pf, G) {
  scale_y <- sqrt(mean(yd^2)); mult <- alpha + scale_y * (1 - alpha)
  f <- glmnet::glmnet(Xd, yd, family = "gaussian", alpha = alpha / mult,
    lambda = lam * mult, penalty.factor = pf, intercept = FALSE, standardize = FALSE,
    type.gaussian = G$type_gaussian, thresh = G$thresh, maxit = G$maxit)
  e$check_glmnet_path(f, lam * mult, G)
  B <- as.matrix(f$beta); sc <- max(1, max(abs(crossprod(Xd, yd))) / nrow(Xd))
  list(B = B, s = scale_y, m = mult, a = alpha / mult, jerr = f$jerr,
       npasses = f$npasses, kkt = e$kkt_glmnet(Xd, yd, B, lam, alpha, pf, sc))
}
glmnet::glmnet.control(fdev = 0, devmax = 1)
set.seed(903)
xx <- scale(matrix(rnorm(n * 30L), n, 30L)); attributes(xx) <- list(dim = c(n, 30L))
yy <- as.numeric(3 * xx[, 3] - 2 * xx[, 9] + rnorm(n))
check("real glmnet screened fit and coefficient consistency", {
  fit <- e$fit_F3_alasso(xx, yy, fold, 1, s)
  if (all(fit$rules$status == "failed")) stop(fit$diagnostics$error)
  assert(all(fit$rules$status != "failed"))
  assert(length(fit$diagnostics$keep) >= 2L)
  for (j in seq_len(nrow(fit$rules)))
    assert(identical(e$support_key(which(fit$coefficients[[j]]$beta_pen != 0)), fit$rules$support[j]))
  assert(abs(sum(fit$diagnostics$v) - length(fit$diagnostics$keep)) <= 1e-10 * length(fit$diagnostics$keep))
})
check("F3 determinism of rule rows and pilot CV", {
  again <- e$fit_F3_alasso(xx, yy, fold, 1, s)
  assert(identical(fit$rules, again$rules))
  assert(identical(fit$beta, again$beta))
  assert(identical(fit$diagnostics$pilot$cvm, again$diagnostics$pilot$cvm))
})
check("F3 penalty factor rescaling invariance", {
  keep <- fit$diagnostics$keep
  factors <- fit$diagnostics$v
  lambda <- fit$diagnostics$path$lambda
  a <- e$glmnet_target_path(xx[, keep, drop = FALSE], yy, 1, lambda, factors, s$GLMNET)
  b <- e$glmnet_target_path(xx[, keep, drop = FALSE], yy, 1, lambda, 7*factors, s$GLMNET)
  assert(isTRUE(all.equal(a$B, b$B, tolerance = 1e-12)))
})
check("F3 fitting source has no truth input", {
  files <- file.path(root, "F3_AdaptiveLasso", c("config.R", "common.R", "methods/glmnet_helpers.R", "methods/fit_F3_alasso.R"))
  assert(!any(vapply(files, function(f) any(grepl("truth|\\$active|\\$signal|truth/", readLines(f), perl = TRUE)), logical(1))))
})
validator <- new.env(parent = globalenv())
sys.source(file.path(root, "F3_AdaptiveLasso", "tests", "validate_outputs.R"), validator)
vr <- fit$rules; vr$p <- ncol(xx)
payload <- list(schema_version = 2L, fit = fit, coefficients = fit$coefficients)
check("validator accepts v2 evidence fixture", assert(length(validator$validate_payload(payload, vr, s, e)) == 0L))
for (fault in c("schema", "id", "role", "extra", "coefficient", "metadata", "support", "retired", "code")) {
  bad <- payload; rows_bad <- vr
  if (fault == "schema") bad$schema_version <- 1L
  if (fault == "id") rows_bad$rule_id[1] <- "bogus"
  if (fault == "role") rows_bad$role[1] <- "S0"
  if (fault == "extra") rows_bad$pilot_k <- NULL
  if (fault == "coefficient") bad$coefficients[[1]]$beta_pen <- numeric()
  if (fault == "metadata") bad$coefficients[[1]]$index <- -999L
  if (fault == "support") rows_bad$support[1] <- "999"
  if (fault == "retired") bad$fit$diagnostics$ridge <- TRUE
  if (fault == "code") rows_bad$diag_codes[1] <- "kappa_edge"
  check(paste("validator corrupt", fault), assert(length(validator$validate_payload(bad, rows_bad, s, e)) > 0L))
}
load_method <- function(folder, fit_file) {
  cfg <- new.env(parent = globalenv())
  sys.source(file.path(root, folder, "config.R"), cfg)
  env <- new.env(parent = globalenv())
  for (f in c("common.R", "methods/glmnet_helpers.R", paste0("methods/", fit_file)))
    sys.source(file.path(root, folder, f), env)
  env$assert_pkg_version <- function(...) invisible(TRUE)
  env$glmnet_target_path <- e$glmnet_target_path
  list(cfg = cfg, env = env)
}
f1 <- load_method("F1_Lasso", "fit_F1_lasso.R")
s1 <- as.list(f1$cfg); s1$variant <- "primary"; s1$GRID <- s$GRID
f2 <- load_method("F2_ElasticNet", "fit_F2_enet.R")
s2 <- f2$cfg$make_settings(); s2$GRID <- s$GRID
check("real pilot equals F1 cv_min beta", {
  a <- f1$env$fit_F1_lasso(xx, yy, fold, 1, s1)
  c <- e$fit_F3_alasso(xx, yy, fold, 1, s)
  assert(identical(a$beta, c$diagnostics$pilot$beta))
})
check("real F1 and F2 coefficient evidence", {
  a <- f1$env$fit_F1_lasso(xx, yy, fold, 1, s1)
  b <- f2$env$fit_F2_enet(xx, yy, fold, 1, s2)
  for (o in list(a, b)) {
    assert(all(o$rules$status != "failed"))
    for (j in seq_len(nrow(o$rules)))
      assert(identical(e$support_key(which(o$coefficients[[j]]$beta_pen != 0)), o$rules$support[j]))
  }
})
check("F1 and F2 failed-rule coefficients match support_audit", {
  bad1 <- s1; bad2 <- s2
  bad1$GLMNET$kkt_rel_tol <- -1
  bad2$GLMNET$kkt_rel_tol <- -1
  a <- f1$env$fit_F1_lasso(xx, yy, fold, 1, bad1)
  b <- f2$env$fit_F2_enet(xx, yy, fold, 1, bad2)
  for (o in list(a,b)) {
    for (j in which(o$rules$status == "failed")) {
      beta <- o$coefficients[[j]]$beta_pen
      assert(all(is.finite(beta)))
      assert(identical(e$support_key(which(beta != 0)), o$rules$support_audit[j]))
    }
    assert(all(o$rules$status[1:2] == "failed"))
  }
})
check("K37 agrees with frozen derive_rules on F1 F2 F3", {
  set.seed(991)
  N <- 200L; P <- 20L
  z <- scale(matrix(rnorm(N*P), N, P)); attributes(z) <- list(dim = c(N, P))
  yz <- as.numeric(3*z[,2] - 2*z[,8] + rnorm(N))
  ff <- rep(1:10, length.out = N)
  fits <- list(F1 = f1$env$fit_F1_lasso(z, yz, ff, 1, s1),
               F2 = f2$env$fit_F2_enet(z, yz, ff, 1, s2),
               F3 = e$fit_F3_alasso(z, yz, ff, 1, s))
  frozen <- new.env(parent = globalenv())
  sys.source("C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/F_2026-10-19_benchmark_study_n200/Benchmark_Study_20261019/scoring/derived_rules/derive_rules.R", frozen)
  for (method in names(fits)) {
    o <- fits[[method]]
    assert(all(o$rules$status != "failed"))
    settings <- switch(method, F1 = s1, F2 = s2, F3 = s)
    tb <- frozen$method_tables(list(diagnostics = o$diagnostics, settings = settings), method)
    dr <- frozen$derive_case(tb, method, P)$rules
    for (rid in c("ebic1_K37", "ebic05_K37")) {
      row <- o$rules[o$rules$rule_id == rid, ]
      assert(identical(row$support, dr[[rid]]$key))
      assert(isTRUE(all.equal(row$crit_value, dr[[rid]]$crit, tolerance = 0)))
      assert(identical(row$k_valid_max, dr[[rid]]$k_valid_max))
    }
  }
  frozen$K_CAP <- 0L
  wrong <- frozen$derive_case(tb, "F3", P)$rules$ebic1_K37$key
  assert(!identical(wrong, fits$F3$rules$support[fits$F3$rules$rule_id == "ebic1_K37"]))
})
set.seed(8821)
nn <- 40L; pp <- 160L; blocks <- 8L; per_block <- pp / blocks
latent <- matrix(rnorm(nn * blocks), nn, blocks)
zz <- sapply(seq_len(pp), function(j) .7 * latent[, ceiling(j / per_block)] + sqrt(1-.7^2) * rnorm(nn))
zz <- scale(zz); attributes(zz) <- list(dim = c(nn, pp))
truth <- c(1L, 21L, 41L, 61L)
yz <- as.numeric(zz[, truth] %*% c(5, -5, 5, -5) + rnorm(nn, sd = .4))
ff <- rep(1:10, length.out = nn)
v2synthetic <- e$fit_F3_alasso(zz, yz, ff, 1, s)
dep <- load_method_from_deployed <- NULL
dep_root <- "C:/Users/felip/Documents/NOTS_BVS/NOTS_home/projects/BVS/Benchmarks/F3_AdaptiveLasso"
cfg_dep <- new.env(parent = globalenv()); sys.source(file.path(dep_root, "config.R"), cfg_dep)
dep <- new.env(parent = globalenv())
for (f in c("common.R", "methods/glmnet_helpers.R", "methods/fit_F3_alasso.R"))
  sys.source(file.path(dep_root, f), dep)
dep$assert_pkg_version <- function(...) invisible(TRUE)
dep$glmnet_target_path <- e$glmnet_target_path
sd <- cfg_dep$study_settings(); sd$GRID <- s$GRID
oldsynthetic <- dep$fit_F3_alasso(zz, yz, ff, 1, sd)
for (version in c("v2", "deployed")) {
  o <- if (version == "v2") v2synthetic else oldsynthetic
  w <- if (version == "v2") { a <- rep(Inf, pp); a[o$diagnostics$keep] <- o$diagnostics$w; a } else o$diagnostics$w
  cat("ridge fixture", version, "max_true_weight", max(w[truth]), "min_noise_weight", min(w[-truth]),
      "truth_on_path", any(o$diagnostics$path$key == e$support_key(truth)), "\n")
}
ridge_guard <- function(o, version) {
  if (version == "v2") {
    w <- rep(Inf, pp); w[o$diagnostics$keep] <- o$diagnostics$w
  } else w <- o$diagnostics$w
  assert(all(is.finite(w[truth])))
  assert(max(w[truth]) < min(w[-truth]))
  assert(any(o$diagnostics$path$key == e$support_key(truth)))
}
check("ridge weakness synthetic: v2 passes", ridge_guard(v2synthetic, "v2"))
check("ridge weakness synthetic: deployed fails", ridge_guard(oldsynthetic, "deployed"), TRUE)
check("adapted deployed F1 common suite", {
  out <- file.path(root, "tests", "legacy_common_runner")
  status <- system2(file.path(R.home("bin"), "Rscript.exe"),
    c("--vanilla", shQuote(file.path(root, "F1_Lasso", "tests", "test_common.R")),
      shQuote(file.path(root, "F1_Lasso")), shQuote(out)))
  assert(identical(status, 0L))
})
check("F1 and F2 deployed orthogonal rows identical", {
  test <- file.path(root, "tests", "compare_orthogonal_canaries.R")
  status <- system2(file.path(R.home("bin"), "Rscript.exe"), c("--vanilla", shQuote(test)))
  assert(identical(status, 0L))
})
check("migrated F3 canary suite", {
  test <- file.path(root, "F3_AdaptiveLasso", "tests", "test_F3_alasso.R")
  previous <- Sys.getenv("BENCH_V2_LOCAL_TEST", unset = NA_character_)
  Sys.setenv(BENCH_V2_LOCAL_TEST = "1")
  status <- system2(file.path(R.home("bin"), "Rscript.exe"), c("--vanilla", shQuote(test)))
  if (is.na(previous)) Sys.unsetenv("BENCH_V2_LOCAL_TEST") else Sys.setenv(BENCH_V2_LOCAL_TEST = previous)
  assert(identical(status, 0L))
})
report <- do.call(rbind, results)
print(report, row.names = FALSE)
cat("checks", nrow(report), "pass", sum(report$outcome == "PASS"), "fail", sum(report$outcome == "FAIL"), "\n")
if (any(report$outcome == "FAIL")) quit(status = 1L)
if (identical(Sys.getenv("BENCH_V2_LOCAL_TEST"), "1")) {
  test <- file.path(root, "tests", "run_local_f2_suite.R")
  inputs <- "C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/dev/inputs"
  out <- file.path(root, "tests", "legacy_runs", "F2_capped")
  log <- file.path(root, "tests", "legacy_runs", "F2_capped.log")
  err <- file.path(root, "tests", "legacy_runs", "F2_capped.stderr.log")
  status <- system2(file.path(R.home("bin"), "Rscript.exe"),
    c("--vanilla", shQuote(test), shQuote(file.path(root,"F2_ElasticNet")),
      shQuote(inputs), shQuote(out)), stdout=log, stderr=err)
  cat("F2 local path-shim suite exit", status, "\n")
  if (!identical(status, 0L)) quit(status=1L)
}
