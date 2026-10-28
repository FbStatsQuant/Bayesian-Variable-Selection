# test_A1_susie.R -- G3 unit tests for A1 SuSiE, master §III.3.6 (i) items 1-9, plus the
# §IV.3 common items that apply to A1 (failure path through the runner, determinism, no-oracle
# grep, runner run with no truth/ present). Every fixture is synthetic and seeded (TEST_SEED);
# none uses the study's data or truth. Item 1 is ported from Oct-7 `SuSiE/tests.R`.
#
# Usage (NOTS compute node): Rscript tests/test_A1_susie.R <code_dir> <scratch_out_dir>
# Prints one line per check and writes <scratch_out_dir>/test_results.csv.
# Items 4 and 5 have stochastic fixtures: their first G3 outcome is recorded (not yet a gate).

run_A1_tests <- function(code_dir, out_dir) {
  cfg <- new.env()
  sys.source(file.path(code_dir, "config.R"), envir = cfg)
  .libPaths(c(cfg$COMMON$LIB, .Library))
  E <- new.env(parent = asNamespace("stats"))
  sys.source(file.path(code_dir, "common.R"), envir = E)
  sys.source(file.path(code_dir, "methods", "fit_A1_susie.R"), envir = E)
  S <- cfg$make_settings("primary")
  TS <- cfg$TEST_SEED
  dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

  results <- list()
  check <- function(item, name, ok, detail = "", gate = TRUE) {
    ok <- isTRUE(ok)
    results[[length(results) + 1L]] <<- data.frame(item = item, check = name, pass = ok,
      gate = gate, detail = as.character(detail), stringsAsFactors = FALSE)
    cat(sprintf("[%s] %-4s %s %s\n", if (ok) "PASS" else if (gate) "FAIL" else "NOTE",
                item, name, detail))
  }
  maxabs <- function(a, b) if (length(a) != length(b)) Inf else max(abs(a - b))
  susie_fixed <- function(X, y, V, sigma2, L = 1L) {
    # L effects, fixed V and sigma^2, no estimation: the wrapper's explicit argument list
    # with the estimation switches turned off.
    args <- E$a1_args(X, y, L, S)
    args$scaled_prior_variance <- V / stats::var(y)
    args$residual_variance <- sigma2
    args$estimate_prior_variance <- FALSE
    args$estimate_residual_variance <- FALSE
    do.call(susieR::susie, args)
  }
  ser_exact <- function(X, y, V, sigma2) {
    d <- colSums(X^2); t <- as.numeric(crossprod(X, y)); p <- ncol(X)
    logbf <- 0.5 * (log(sigma2 / (sigma2 + V * d)) + V * t^2 / (sigma2 * (sigma2 + V * d)))
    a <- exp(logbf - max(logbf)); a <- a / sum(a)
    mu <- V * t / (sigma2 + V * d)
    loglik <- -length(y) / 2 * log(2 * pi * sigma2) - sum(y^2) / (2 * sigma2) +
      max(logbf) + log(mean(exp(logbf - max(logbf))))
    list(alpha = a, mu = mu, pm = a * mu,
         elbo = loglik + log(1 + p * sqrt(.Machine$double.eps)))
  }
  std_design <- function(n, p, seed) {
    RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(seed)
    X <- scale(matrix(rnorm(n * p), n, p)); attr(X, "scaled:center") <- NULL
    attr(X, "scaled:scale") <- NULL
    list(X = X, eps = rnorm(n))
  }
  folds <- function(n) rep(seq_len(10L), length.out = n)

  # ---- Item 1: single-effect closed form (two fixtures) -------------------------------
  i <- seq_len(12L)
  X1 <- cbind(i / 5, sin(i) + 0.4, (-1)^i * 1.7 + 0.2)
  y1 <- 1.2 + 0.4 * X1[, 1L] - 0.6 * X1[, 2L] + cos(2 * i) / 7
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(TS)
  X1b <- sweep(matrix(rnorm(50 * 120), 50, 120), 2L, runif(120, 0.3, 3), "*") +
    rep(runif(120, -1, 1), each = 50)                     # uncentred, unequal norms
  y1b <- 0.5 + 0.9 * X1b[, 17L] + rnorm(50)
  for (fx in list(list("n12p3", X1, y1, 0.8, 1.7), list("n50p120", X1b, y1b, 0.6, 1.3))) {
    f <- susie_fixed(fx[[2]], fx[[3]], fx[[4]], fx[[5]])
    ex <- ser_exact(fx[[2]], fx[[3]], fx[[4]], fx[[5]])
    check("1", paste0("SER alpha ", fx[[1]]), maxabs(as.numeric(f$alpha), ex$alpha) <= 1e-10,
          sprintf("maxdiff=%.2e", maxabs(as.numeric(f$alpha), ex$alpha)))
    check("1", paste0("SER mu ", fx[[1]]), maxabs(as.numeric(f$mu), ex$mu) <= 1e-10,
          sprintf("maxdiff=%.2e", maxabs(as.numeric(f$mu), ex$mu)))
    pm <- susieR::susie_get_posterior_mean(f, prior_tol = S$A1$PRIOR_TOL)
    check("1", paste0("SER posterior mean ", fx[[1]]), maxabs(pm, ex$pm) <= 1e-10,
          sprintf("maxdiff=%.2e", maxabs(pm, ex$pm)))
    check("1", paste0("SER ELBO = exact + log(1+p*sqrt(eps)) ", fx[[1]]),
          abs(tail(f$elbo, 1L) - ex$elbo) <= 1e-8,
          sprintf("diff=%.2e (offset=%.2e)", tail(f$elbo, 1L) - ex$elbo,
                  log(1 + ncol(fx[[2]]) * sqrt(.Machine$double.eps))))
  }
  fit_ser <- susie_fixed(X1, y1, 0.8, 1.7)

  # ---- Fixtures for items 2, 4, 5, 6, 7 (n = 200, p = 500) ----------------------------
  D <- std_design(200L, 500L, TS)
  act <- c(7L, 123L, 250L, 401L, 499L)
  b <- numeric(500L); b[act] <- 1.5
  y_strong <- drop(D$X %*% b) + D$eps
  y_null <- D$eps
  fd <- folds(200L)

  # ---- Item 4: strong-signal canary at p > n (recorded on first G3 run) ---------------
  t0 <- proc.time()[["elapsed"]]
  r4 <- E$fit_A1_susie(D$X, y_strong, fd, 101L, S)
  t4 <- proc.time()[["elapsed"]] - t0
  pip05 <- r4$rules$support[r4$rules$rule_id == "pip05"]
  check("4", "strong canary pip05 == {7,123,250,401,499}", identical(pip05, E$support_key(act)),
        sprintf("pip05=%s status=%s niter=%s n_active=%s n_cs=%s runtime=%.1fs", pip05,
                r4$rules$status[1], r4$diagnostics$niter, r4$diagnostics$n_active,
                r4$diagnostics$n_cs, t4))
  check("4", "strong canary converged", isTRUE(r4$converged))
  check("4", "strong canary L_saturated FALSE", identical(r4$diagnostics$L_saturated, FALSE))
  check("4", "strong canary rules cslead/bfdr10 recorded", TRUE,
        paste(r4$rules$rule_id, r4$rules$support, sep = "=", collapse = " "), gate = FALSE)

  # ---- Item 2: PIP recomputation, coded independently of susieR -----------------------
  fit_strong <- do.call(susieR::susie, E$a1_args(D$X, y_strong, S$A1$L, S))
  act_eff <- which(fit_strong$V > 1e-9)
  pip_ind <- rep(1, 500L)
  for (l in act_eff) pip_ind <- pip_ind * (1 - fit_strong$alpha[l, ])
  pip_ind <- 1 - pip_ind
  check("2", "PIP = 1 - prod(1 - alpha) over V > 1e-9", maxabs(pip_ind, unname(fit_strong$pip)) <= 1e-12,
        sprintf("maxdiff=%.2e active=%d", maxabs(pip_ind, unname(fit_strong$pip)), length(act_eff)))
  check("2", "wrapper PIP equals direct-call PIP", identical(r4$pip, unname(fit_strong$pip)))

  # ---- Item 3: no-intercept canary ------------------------------------------------------
  D3 <- std_design(50L, 20L, TS + 3L)
  y3 <- drop(D3$X[, c(2L, 9L)] %*% c(1, -0.8)) + D3$eps
  fa <- susie_fixed(D3$X, y3, 0.7, 1.1); fb <- susie_fixed(D3$X, y3 + 3, 0.7, 1.1)
  check("3", "fixed V, sigma2: alpha(y) == alpha(y+3)", maxabs(fa$alpha, fb$alpha) <= 1e-12,
        sprintf("maxdiff=%.2e", maxabs(fa$alpha, fb$alpha)))
  check("3", "fixed V, sigma2: mu(y) == mu(y+3)", maxabs(fa$mu, fb$mu) <= 1e-12,
        sprintf("maxdiff=%.2e", maxabs(fa$mu, fb$mu)))
  ga <- do.call(susieR::susie, E$a1_args(D3$X, y3, 5L, S))
  gb <- do.call(susieR::susie, E$a1_args(D3$X, y3 + 3, 5L, S))
  check("3", "sigma2 estimated: intercept == 0 for y and y+3",
        identical(as.numeric(ga$intercept), 0) && identical(as.numeric(gb$intercept), 0))

  # ---- Item 5: null canary (reported; not a gate) ---------------------------------------
  r5 <- E$fit_A1_susie(D$X, y_null, fd, 101L, S)
  check("5", "null canary pip05 empty", identical(r5$rules$support[1], ""),
        sprintf("pip05='%s' status=%s n_active=%s", r5$rules$support[1], r5$rules$status[1],
                r5$diagnostics$n_active), gate = FALSE)

  # ---- Item 6: determinism and seed scope ------------------------------------------------
  r4b <- E$fit_A1_susie(D$X, y_strong, fd, 101L, S)
  check("6", "same seed: identical() wrapper output (strong)", identical(r4, r4b))
  r4c <- E$fit_A1_susie(D$X, y_strong, fd, 999L, S)
  check("6", "other seed: identical() PIPs (strong)", identical(r4$pip, r4c$pip))
  r5c <- E$fit_A1_susie(D$X, y_null, fd, 999L, S)
  check("6", "other seed: identical() PIPs (null)", identical(r5$pip, r5c$pip))
  big <- function(r) sum(r$diagnostics$alpha_saved$set_size > 100 & !duplicated(r$diagnostics$alpha_saved$effect))
  # Fixture that exercises purity subsampling (an active effect whose 95% set has > n_purity
  # members): independent X (200 x 500), 14 signals; seed TEST_SEED + 101 found by a search over
  # TEST_SEED + 100 + k (k = 0, 1) on 2026-10-19.
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(TS + 101L)
  X6 <- scale(matrix(rnorm(200 * 500), 200, 500)); attr(X6, "scaled:center") <- NULL
  attr(X6, "scaled:scale") <- NULL
  b6 <- numeric(500L); b6[seq(3, 460, length.out = 14)] <- rep(c(1.4, -1, 1.8, -1.2, 0.8, -1.6), 3)[1:14]
  y6 <- drop(X6 %*% b6) + rnorm(200)
  r6a <- E$fit_A1_susie(X6, y6, fd, 101L, S)
  r6b <- E$fit_A1_susie(X6, y6, fd, 101L, S)
  r6c <- E$fit_A1_susie(X6, y6, fd, 999L, S)
  check("6", "seed-scope fixture has an active effect with 95% set > 100 (sampling exercised)",
        big(r6a) > 0L, sprintf("large sets=%d (strong=%d null=%d)", big(r6a), big(r4), big(r5)))
  check("6", "sampling fixture: same seed identical() wrapper output", identical(r6a, r6b))
  check("6", "sampling fixture: other seed identical() PIPs and pip05", identical(r6a$pip, r6c$pip) &&
          identical(r6a$rules$support[1], r6c$rules$support[1]))
  check("6", "sampling fixture: credible sets under the two seeds", TRUE,
        sprintf("n_cs %d vs %d; identical sets: %s", r6a$diagnostics$n_cs, r6c$diagnostics$n_cs,
                identical(r6a$diagnostics$sets$cs, r6c$diagnostics$sets$cs)), gate = FALSE)

  # ---- Item 7: gate tests -----------------------------------------------------------------
  S7 <- S; S7$A1$MAX_ITER <- 1L
  r7 <- E$fit_A1_susie(D$X, y_strong, fd, 101L, S7)
  check("7", "max_iter = 1: every rule failed", all(r7$rules$status == "failed"))
  check("7", "max_iter = 1: support NA, k NA, support_audit kept",
        all(is.na(r7$rules$support)) && all(is.na(r7$rules$k)) && !anyNA(r7$rules$support_audit),
        paste(r7$rules$support_audit, collapse = " | "))
  check("7", "max_iter = 1: reason recorded, converged FALSE, pip NULL, beta NA",
        all(grepl("not converged", r7$rules$error)) && identical(r7$converged, FALSE) &&
          is.null(r7$pip) && all(is.na(r7$beta)), r7$rules$error[1])
  check("7", "max_iter = 1: package warning captured", any(grepl("did not converge", r7$warnings)))
  # Recording failure: if the item (g) objects cannot be built, the fit fails (support kept).
  E2 <- new.env(parent = asNamespace("stats"))
  sys.source(file.path(code_dir, "common.R"), envir = E2)
  sys.source(file.path(code_dir, "methods", "fit_A1_susie.R"), envir = E2)
  E2$a1_compact <- function(...) stop("forced compact failure")
  r7c <- E2$fit_A1_susie(D$X, y_strong, fd, 101L, S)
  check("7", "compact failure: rows failed, support_audit kept, reason recorded",
        all(r7c$rules$status == "failed") && !anyNA(r7c$rules$support_audit) &&
          all(grepl("recording: compact diagnostics failed", r7c$rules$error)), r7c$rules$error[1])
  syn <- fit_ser
  pip_syn <- susieR::susie_get_pip(syn, prior_tol = 1e-9)
  pm_syn <- susieR::susie_get_posterior_mean(syn)
  lb_syn <- stats::var(y1) / 1e4
  syn$elbo <- c(-10, -10 - 1e-5)
  g <- E$a1_gates(syn, NULL, S, pip_syn, pm_syn, lb_syn)
  check("7", "ELBO drop 1e-5: flag elbo_drop, not failed",
        !g$failed && "elbo_drop" %in% g$flags, paste(g$flags, collapse = ";"))
  syn$elbo <- c(-10, -10 - 2e-3)
  g <- E$a1_gates(syn, NULL, S, pip_syn, pm_syn, lb_syn)
  check("7", "ELBO drop 2e-3 (> TOL): gate 3 fails", g$failed && any(grepl("ELBO decrease", g$reasons)),
        paste(g$reasons, collapse = ";"))
  syn$elbo <- c(-10, NA_real_)
  g <- E$a1_gates(syn, NULL, S, pip_syn, pm_syn, lb_syn)
  check("7", "non-finite ELBO: gate 3 fails", g$failed && any(grepl("non-finite", g$reasons)))
  syn$elbo <- c(-10, -9); syn$sigma2 <- lb_syn
  g <- E$a1_gates(syn, NULL, S, pip_syn, pm_syn, lb_syn)
  check("7", "sigma2 at floor: flag sigma2_floor (L = 1 active: L_saturated)",
        !g$failed && identical(g$flags, c("L_saturated", "sigma2_floor")), paste(g$flags, collapse = ";"))
  syn$sigma2 <- 1.7; syn$V <- -1
  g <- E$a1_gates(syn, NULL, S, pip_syn, pm_syn, lb_syn)
  check("7", "negative V: gate 4 fails", g$failed && any(grepl("prior variance", g$reasons)))
  syn$V <- 0.8; syn$intercept <- 0.1
  g <- E$a1_gates(syn, NULL, S, pip_syn, pm_syn, lb_syn)
  check("7", "nonzero intercept: gate 5 (contract) fails", g$failed && any(grepl("contract", g$reasons)))

  # ---- Item 8: rule tests ------------------------------------------------------------------
  check("8", "BFDR c(0.99,0.95,0.75,0.1) -> {1,2}",
        identical(E$a1_bfdr_support(c(0.99, 0.95, 0.75, 0.1), 0.1, 64), 1:2))
  check("8", "BFDR c(.95,.85,.2) -> {1,2}", identical(E$a1_bfdr_support(c(.95, .85, .2), 0.1, 64), 1:2))
  check("8", "BFDR rep(0.3,4) -> empty", identical(E$a1_bfdr_support(rep(0.3, 4), 0.1, 64), integer()))
  check("8", "BFDR tie order by index", identical(E$a1_bfdr_support(c(0.2, 0.95, 0.95), 0.1, 64), 2:3))
  check("8", "BFDR tie crossing the cutoff c(.8,1,.8) -> {1,2}",
        identical(E$a1_bfdr_support(c(0.8, 1, 0.8), 0.1, 64), 1:2))
  pip8 <- c(0.1, 0.4, 0.05, 0.9, 0.4, 0.2, 0.1, 0.1, 0.3)
  sets8 <- list(cs = list(L1 = c(5L, 2L, 9L), L2 = 4L, L3 = c(9L, 6L)))
  check("8", "CS-lead tie -> smallest index; sorted union",
        identical(E$a1_cslead_support(sets8, pip8), c(2L, 4L, 9L)))
  check("8", "CS-lead no sets -> empty", identical(E$a1_cslead_support(list(cs = NULL), pip8), integer()))

  # ---- Item 9: orthogonal canary (n = 200, p = 30, X'X = (n-1) I) -------------------------
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(TS + 9L)
  Z <- scale(matrix(rnorm(200 * 30), 200, 30), scale = FALSE)
  Q <- qr.Q(qr(Z)) * sqrt(199)
  Q <- Q - rep(colMeans(Q), each = 200)                  # already ~0; exact centring
  Q <- sweep(Q, 2L, sqrt(colSums(Q^2) / 199), "/")
  act9 <- c(3L, 7L, 14L, 16L, 25L)
  b9 <- numeric(30L); b9[act9] <- c(1.4, -1.0, 1.8, -1.2, 0.8)
  y9 <- drop(Q %*% b9) + rnorm(200)
  check("9", "orthogonal design: X'X = (n-1) I", max(abs(crossprod(Q) - 199 * diag(30))) < 1e-8,
        sprintf("maxdev=%.2e", max(abs(crossprod(Q) - 199 * diag(30)))))
  r9 <- E$fit_A1_susie(Q, y9, folds(200L), 101L, S)
  check("9", "orthogonal canary pip05 recovers the 5 signals",
        identical(r9$rules$support[1], E$support_key(act9)), r9$rules$support[1])

  # ---- §IV.3 items 6 (failure path) and 7 (no-oracle), runner end to end ------------------
  src <- c("config.R", "common.R", list.files(file.path(code_dir, "methods"), full.names = FALSE,
                                              pattern = "\\.R$"))
  paths <- c(file.path(code_dir, c("config.R", "common.R")),
             list.files(file.path(code_dir, "methods"), full.names = TRUE, pattern = "\\.R$"))
  hits <- unlist(lapply(paths, function(f) {
    l <- readLines(f); w <- grep("truth|\\$active|\\$signal|truth/", l)
    if (length(w)) paste0(basename(f), ":", w) else character()
  }))
  check("IV7", "no-oracle grep of config.R, common.R, methods/*.R", !length(hits),
        paste(c(src, hits), collapse = " "))

  root <- file.path(out_dir, "runner_test")
  unlink(root, recursive = TRUE)
  inp <- file.path(root, "inputs", "p0060"); dir.create(inp, recursive = TRUE)
  D10 <- std_design(200L, 60L, TS + 10L)
  b10 <- numeric(60L); b10[c(5L, 30L)] <- c(1.2, -1.5)
  sig10 <- drop(D10$X %*% b10)
  Y10 <- sapply(cfg$COMMON$SCALES, function(cc) cc * sig10 + D10$eps)
  fake <- list(X = D10$X, Y = Y10, foldid = folds(200L), dataset_id = "dev_p0060_S1_r001",
               p = 60L, n = 200L, scenario = 1L, replicate = 1L, kind = "dev",
               data_seed = 77L, fold_seed = 78L, method_seed = 77L + cfg$METHOD_SEED_OFFSET)
  fin <- file.path(inp, "dev_p0060_S1_r001.rds"); saveRDS(fake, fin, compress = FALSE)
  check("IV7", "runner fixture has no truth/ directory", !dir.exists(file.path(root, "truth")))
  R <- new.env(); sys.source(file.path(code_dir, "run_case.R"), envir = R)
  run <- function(cd, rid) R$main(c(paste0("--code_dir=", cd), paste0("--input=", fin),
                                    paste0("--out_root=", file.path(root, "results")),
                                    paste0("--run_id=", rid), "--scales=c100"))
  run(code_dir, "ok")
  od <- file.path(root, "results", "ok", "p0060", "dev_p0060_S1_r001_c100")
  csv <- lapply(cfg$METHODS$method_id, function(m)
    utils::read.csv(file.path(od, paste0(m, ".csv")), colClasses = "character"))
  check("IV", "runner writes 4 files per method id",
        all(file.exists(file.path(od, paste0(rep(cfg$METHODS$method_id, each = 4),
                                             c(".rds", ".csv", ".sha256", ".done"))))))
  check("IV", "runner CSV columns follow the schema", all(vapply(csv, function(x) identical(names(x), R$SCHEMA), TRUE)))
  check("IV", "runner rule ids/roles as registered",
        identical(csv[[1]]$rule_id, c("pip05", "cslead", "bfdr10")) &&
          identical(csv[[1]]$role, c("primary", "S0", "S0")) &&
          identical(csv[[2]]$rule_id, "pip05") && identical(csv[[2]]$role, "S1"))
  check("IV", "runner fixture result", TRUE, paste(csv[[1]]$rule_id, csv[[1]]$status, csv[[1]]$support,
                                                     sep = ":", collapse = " "), gate = FALSE)
  m1 <- file.info(file.path(od, "A1.done"))$mtime
  Sys.sleep(1.1); run(code_dir, "ok")
  check("IV", "runner is idempotent (valid .done skipped)", identical(file.info(file.path(od, "A1.done"))$mtime, m1))
  # Resume guard: same run id, changed code -> the runner refuses to reuse the old outputs.
  chg <- file.path(root, "code_changed"); dir.create(file.path(chg, "methods"), recursive = TRUE)
  for (f in c("config.R", "common.R", "run_case.R", "methods/fit_A1_susie.R"))
    file.copy(file.path(code_dir, f), file.path(chg, f))
  cat("\n# changed\n", file = file.path(chg, "config.R"), append = TRUE)
  msg <- tryCatch({ run(chg, "ok"); "no error" }, error = conditionMessage)
  check("IV", "resume guard: changed code with an existing run id stops", grepl("^resume:", msg), msg)
  # Quarantine: a bundle with .done removed and a stray temp file is moved aside and refitted.
  qstem <- file.path(od, "A1")
  file.remove(paste0(qstem, ".done")); writeLines("junk", paste0(qstem, ".rds.tmp.x.1.y"))
  run(code_dir, "ok")
  qd <- list.files(od, pattern = "^A1\\.quarantine_", full.names = TRUE)
  check("IV", "quarantine: partial bundle moved aside, case refitted to a valid bundle",
        length(qd) == 1L && all(file.exists(file.path(qd, c("A1.rds", "A1.csv", "A1.sha256", "A1.rds.tmp.x.1.y")))) &&
          R$done_is_valid(qstem), paste(basename(qd), collapse = ","))
  # Bundle contract: a .sha256 with only the CSV line is not a valid bundle.
  sh <- readLines(paste0(qstem, ".sha256")); writeLines(sh[2], paste0(qstem, ".sha256"))
  check("IV", "bundle contract: one-entry .sha256 is invalid", !R$done_is_valid(qstem))
  writeLines(sh, paste0(qstem, ".sha256"))
  # Environment baseline: a run with a mismatched baseline stops before fitting anything.
  eb <- file.path(root, "env_bad.rds")
  saveRDS(c(R = "R version 0.0.0", environment_manifest_sha256 = "0", susieR = "0", blas = "0"), eb)
  msg <- tryCatch({ R$main(c(paste0("--code_dir=", code_dir), paste0("--input=", fin),
                             paste0("--out_root=", file.path(root, "results")), "--run_id=envbad",
                             "--scales=c100", paste0("--env_baseline=", eb))); "no error" },
                  error = conditionMessage)
  check("IV", "environment baseline mismatch stops the runner before any fit",
        grepl("environment differs from the run baseline", msg) &&
          !length(list.files(file.path(root, "results", "envbad"), recursive = TRUE, pattern = "\\.done$")),
        substr(msg, 1, 120))
  eg <- file.path(root, "env_good.rds"); saveRDS(R$env_fingerprint(cfg$COMMON$LIB), eg)
  R$main(c(paste0("--code_dir=", code_dir), paste0("--input=", fin),
           paste0("--out_root=", file.path(root, "results")), "--run_id=envgood", "--scales=c100",
           paste0("--env_baseline=", eg)))
  check("IV", "environment baseline match: fits run and the fingerprint is saved",
        identical(readRDS(file.path(root, "results", "envgood", "p0060", "dev_p0060_S1_r001_c100", "A1.rds"))$provenance$env_fingerprint,
                  readRDS(eg)))
  # Library assertion: every non-base namespace loaded now resolves under the sealed library.
  nsp <- R$assert_library(cfg$COMMON$LIB)
  nb <- nsp[!names(nsp) %in% R$BASE_PKGS]
  check("IV", "library: non-base namespaces under the study library",
        length(nb) > 0L && all(startsWith(nb, normalizePath(cfg$COMMON$LIB))),
        paste(names(nb), collapse = ","))
  # Forced error: a code copy whose pinned version is wrong -> failed rows, never a null model.
  bad <- file.path(root, "code_badversion"); dir.create(file.path(bad, "methods"), recursive = TRUE)
  for (f in c("config.R", "common.R", "run_case.R", "methods/fit_A1_susie.R"))
    file.copy(file.path(code_dir, f), file.path(bad, f))
  cf <- readLines(file.path(bad, "config.R"))
  cf <- sub('PKG_VERSION = "0.14.2"', 'PKG_VERSION = "0.0.0"', cf, fixed = TRUE)
  writeLines(cf, file.path(bad, "config.R"))
  run(bad, "badversion")
  fb <- utils::read.csv(file.path(root, "results", "badversion", "p0060", "dev_p0060_S1_r001_c100", "A1.csv"),
                        colClasses = "character")
  check("IV6", "forced error -> status failed, support NA, support_audit NA, k NA",
        all(fb$status == "failed") && all(is.na(fb$support)) && all(is.na(fb$support_audit)) &&
          all(is.na(fb$k)), fb$error[1])
  check("IV6", "forced error message names the version assertion", all(grepl("package version", fb$error)))

  # ---- S2 variants exist and run (not registered; smoke only) -----------------------------
  for (v in c("auto", "refine")) {
    Sv <- cfg$make_settings(v)
    rv <- E$fit_A1_susie(D10$X, unname(Y10[, "c100"]), folds(200L), 101L, Sv)
    check("S2", paste("variant", v, "runs and emits pip05/S2"),
          identical(rv$rules$rule_id, "pip05") && identical(rv$rules$role, "S2"),
          paste(rv$rules$status, rv$rules$support), gate = FALSE)
  }

  res <- do.call(rbind, results)
  utils::write.csv(res, file.path(out_dir, "test_results.csv"), row.names = FALSE)
  cat(sprintf("\nSUMMARY: %d checks, %d gate failures, %d notes not passing\n", nrow(res),
              sum(res$gate & !res$pass), sum(!res$gate & !res$pass)))
  invisible(res)
}

if (sys.nframe() == 0L) {
  a <- commandArgs(trailingOnly = TRUE)
  stopifnot(length(a) == 2L)
  res <- run_A1_tests(normalizePath(a[1]), a[2])
  quit(status = if (any(res$gate & !res$pass)) 1L else 0L)
}
