# test_A2_ssl.R -- G3 unit tests for A2 (master §III.3.7 i, items 1-8; §IV.3 unit tests 1-7).
# Run on a NOTS compute node (slurm/run_tests.slurm):
#   Rscript tests/test_A2_ssl.R --code <code dir> --out <output dir> --dev_input <dev p500 S4 r001 .rds>
# Every test returns PASS, FAIL or RECORDED (a recorded measurement that is not a gate).
# The dev fixture is read from inputs/ only.

run_A2_tests <- function(code_dir, out_dir, dev_input,
                         upstream_tarball = file.path(code_dir, "vendor", "SSLASSO_1.2.3.tar.gz"),
                         patched_tarball = "/projects/ml75/fb31/BVS/bench20261019/lib/tarballs/SSLASSO_1.2.3.9001.tar.gz") {
  Sys.setenv(A2_CODE_DIR = code_dir)
  source(file.path(code_dir, "run_case.R"), local = TRUE)        # load_fit_env, build_settings, run_method
  .libPaths(c(STUDY_LIB, .Library))
  env <- load_fit_env(code_dir)
  settings <- build_settings(env)
  stopifnot(requireNamespace("SSLASSO", quietly = TRUE), requireNamespace("digest", quietly = TRUE))
  assert_study_library(c("SSLASSO", "digest"))
  dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

  tenv <- new.env(parent = env)                                  # tests see the fitting functions
  tenv$settings <- settings; tenv$code_dir <- code_dir; tenv$out_dir <- out_dir
  tenv$dev_input <- dev_input; tenv$upstream_tarball <- upstream_tarball; tenv$patched_tarball <- patched_tarball
  tenv$run_method <- run_method; tenv$env <- env
  local(envir = tenv, {
    results <- list()
    record <- function(id, status, details) {
      results[[id]] <<- list(id = id, status = status, details = details)
      cat(sprintf("[%s] %s\n", status, id)); utils::str(details, give.attr = FALSE, vec.len = 6)
    }
    run_test <- function(id, f) {
      t0 <- elapsed()
      r <- tryCatch(f(), error = function(e) list(status = "FAIL", details = list(error = conditionMessage(e))))
      r$details$seconds <- elapsed() - t0
      record(id, r$status, r$details)
    }
    with_a2 <- function(s, ...) { m <- list(...); for (nm in names(m)) s$A2[[nm]] <- m[[nm]]; s }
    verdict <- function(ok) if (isTRUE(ok)) "PASS" else "FAIL"
    set_rng <- function(seed) { RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(seed) }

    dev <- readRDS(dev_input)
    Xd <- dev$X; yd <- unname(dev$Y[, "c100"]); fd <- dev$foldid; sd_seed <- dev$method_seed
    n_d <- nrow(Xd); p_d <- ncol(Xd)
    lad_d <- a2_ladder(n_d, p_d, "primary", settings)
    prim <- settings; prim$variant <- "primary"
    rs <- settings; rs$variant <- "RS"

    # i.1 Analytic lasso limit (port of Oct-7 SSL/tests.R): lambda0 = lambda1, separable,
    # fixed variance, orthogonal uncentred columns of unequal norms, nonzero first observation.
    run_test("i1_analytic_lasso_limit", function() {
      X <- matrix(0, 8L, 2L); X[1L, 1L] <- 4; X[2L, 2L] <- 3
      y <- c(8, -6, 1, 2, -1, 3, 0, 1); lam <- 0.7; sig <- 1.2
      s <- with_a2(settings, PENALTY = "separable", VARIANCE = "fixed", THETA_INIT = 0.3, EPS = 1e-9)
      soft <- function(yy) { xty <- as.vector(crossprod(X, yy)); sign(xty) * pmax(abs(xty) - sig^2 * lam, 0) / colSums(X^2) }
      p1 <- a2_native_path(X, y, lam, lam, s, sigma0 = sig)
      p2 <- a2_native_path(X, y + 5, lam, lam, s, sigma0 = sig)
      e1 <- max(abs(p1$beta[, 1] - soft(y))); e2 <- max(abs(p2$beta[, 1] - soft(y + 5)))
      moved <- max(abs(p2$beta[, 1] - p1$beta[, 1]))
      list(status = verdict(e1 <= 1e-10 && e2 <= 1e-10 && moved > 0.5 && p1$iter < p1$max_iter && p2$iter < p2$max_iter),
           details = list(max_err_y = e1, max_err_shifted = e2, shift_moves_beta_by = moved,
                          beta = p1$beta[, 1], analytic = soft(y)))
    })

    # i.2 Patched (1.2.3.9001) against upstream (1.2.3) at p = 500 on the dev fixture.
    # R on NOTS compiles C with -O2 -ftree-vectorize -march=native. The study library was built
    # on login node loginx1, where -march=native resolves to cascadelake (+abm, -sgx, -xsaves;
    # gcc -Q --help=target), so a compute-node build is a different binary (job 2275397:
    # identical iterations and theta, beta and sigma within 2e-14; diagnosis job 2275900).
    # Upstream and patched are built into temporary libraries (deleted after use) and each is
    # run in its own Rscript --vanilla process.
    # i2  (gate, the master's test): the study-library binary against upstream built with the
    #      study build's flags (STUDY_CFLAGS); paths, iterations, theta, sigma identical().
    # i2a (gate): upstream and patched built in this job with the node's default flags; identical().
    # i2b (recorded): the study-library binary against the default-flag job build of the same source.
    tarballs <- c(upstream = upstream_tarball, patched = patched_tarball)
    want_sha <- c(upstream = "67fb4a881d0b274b2cf00ce7f40d9e6f964aa7f051094078e0bc1b058cd540c1",
                  patched  = "f82bf8db6bb4145a26aa69d1d8f39ac842706df02aa9c10729153f68e16bf589")
    STUDY_CFLAGS <- "-O2 -ftree-vectorize -march=cascadelake -mabm -mno-sgx -mno-xsaves -fno-math-errno"
    run_build <- function(lib, want_version) {
      out <- tempfile(fileext = ".rds"); script <- tempfile(fileext = ".R")
      writeLines(c(
        sprintf('.libPaths(c("%s", .Library))', lib),
        sprintf('stopifnot(requireNamespace("SSLASSO", quietly = TRUE), as.character(utils::packageVersion("SSLASSO")) == "%s")', want_version),
        'env <- new.env(parent = asNamespace("stats"))',
        sprintf('for (f in c("config.R", "common.R", "methods/fit_A2_ssl.R")) sys.source(file.path("%s", f), envir = env)', code_dir),
        'settings <- mget(c("COMMON", "A2", "A2RS", "METHODS"), envir = env)',
        sprintf('d <- readRDS("%s"); y <- unname(d$Y[, "c100"])', dev_input),
        'lad <- env$a2_ladder(nrow(d$X), ncol(d$X), "primary", settings)',
        'path <- env$a2_native_path(d$X, y, lad$lambda0, lad$lambda1, settings)',
        sprintf('saveRDS(list(path = path, version = as.character(utils::packageVersion("SSLASSO")), loc = find.package("SSLASSO")), "%s")', out)),
        script)
      log <- system2(file.path(R.home("bin"), "Rscript"), c("--vanilla", shQuote(script)), stdout = TRUE, stderr = TRUE)
      if (!file.exists(out)) stop("run with ", lib, " failed: ", paste(utils::tail(log, 5), collapse = " / "))
      readRDS(out)
    }
    build_and_run <- function(k, cflags = NULL) {
      sha <- digest::digest(file = tarballs[[k]], algo = "sha256")
      if (sha != want_sha[[k]]) stop(k, " tarball hash mismatch: ", sha)
      lib <- tempfile(paste0("sslasso_", k, "_")); dir.create(lib)
      on.exit(unlink(lib, recursive = TRUE), add = TRUE)
      env_vars <- character()
      if (!is.null(cflags)) {
        mk <- tempfile("Makevars_"); writeLines(paste0("CFLAGS=", cflags), mk)
        env_vars <- paste0("R_MAKEVARS_USER=", mk)
      }
      inst <- system2(file.path(R.home("bin"), "R"), c("CMD", "INSTALL", "--no-test-load", "-l", shQuote(lib), shQuote(tarballs[[k]])),
                      stdout = TRUE, stderr = TRUE, env = env_vars)
      if (!dir.exists(file.path(lib, "SSLASSO"))) stop(k, " install failed: ", paste(utils::tail(inst, 5), collapse = " / "))
      res <- run_build(lib, if (k == "upstream") "1.2.3" else "1.2.3.9001")
      cl <- grep("-c SSL_gaussian.c", inst, value = TRUE, fixed = TRUE)
      res$compile_flags <- if (length(cl)) sub("^.*-fpic +", "", sub(" +-c SSL_gaussian.c.*$", "", cl[1])) else NA_character_
      res
    }
    same_path <- function(a, b) c(beta = identical(a$beta, b$beta), iter = identical(a$iter, b$iter),
                                  theta = identical(a$theta, b$theta), sigma = identical(a$sigma, b$sigma))
    builds <- tryCatch(list(upstream_study_flags = build_and_run("upstream", STUDY_CFLAGS),
                            upstream_job = build_and_run("upstream"),
                            patched_job = build_and_run("patched")), error = function(e) e)
    pa_study <- a2_native_path(Xd, yd, lad_d$lambda0, lad_d$lambda1, settings)
    run_test("i2_study_patched_vs_upstream_study_flags_p500", function() {
      if (inherits(builds, "error")) stop(conditionMessage(builds))
      ok <- same_path(pa_study, builds$upstream_study_flags$path)
      list(status = verdict(all(ok) && builds$upstream_study_flags$version == "1.2.3"),
           details = list(identical = ok, upstream_compile_flags = builds$upstream_study_flags$compile_flags,
                          final_k = sum(pa_study$beta[, length(lad_d$lambda0)] != 0), node = Sys.info()[["nodename"]]))
    })
    run_test("i2a_patched_vs_upstream_same_job_build_p500", function() {
      if (inherits(builds, "error")) stop(conditionMessage(builds))
      ok <- same_path(builds$patched_job$path, builds$upstream_job$path)
      list(status = verdict(all(ok)),
           details = list(identical = ok, versions = c(builds$upstream_job$version, builds$patched_job$version),
                          compile_flags = c(builds$upstream_job$compile_flags, builds$patched_job$compile_flags)))
    })
    run_test("i2b_study_build_vs_default_job_build_p500", function() {
      if (inherits(builds, "error")) stop(conditionMessage(builds))
      jb <- builds$patched_job$path
      list(status = "RECORDED",
           details = list(identical = same_path(pa_study, jb), same_support_every_point = identical(pa_study$beta != 0, jb$beta != 0),
                          max_abs_dbeta = max(abs(pa_study$beta - jb$beta)),
                          max_abs_dsigma = max(abs(pa_study$sigma - jb$sigma), na.rm = TRUE)))
    })

    # i.3 Native against wrapper. (a) The native path on the wrapper's internal inputs
    # (scale(X, center = TRUE, scale = FALSE), y - mean(y)) must be identical() to
    # SSLASSO::SSLASSO(X, y, penalty = "adaptive", variance = "unknown"). (b) Recorded tolerance
    # check (not a gate): native on (stored X, centred y) against the wrapper, same final
    # support and max |delta beta-hat| <= 1e-8, dev fixture p = 500, S4, r1, c100.
    w_cap <- with_captured_conditions(SSLASSO::SSLASSO(Xd, yd, penalty = "adaptive", variance = "unknown"))
    run_test("i3a_native_vs_wrapper_identical", function() {
      if (!is.null(w_cap$error)) stop("wrapper error: ", w_cap$error)
      w <- w_cap$value
      XX <- scale(Xd, center = TRUE, scale = FALSE); yy <- yd - mean(yd)
      pa <- a2_native_path(XX, yy, lad_d$lambda0, lad_d$lambda1, settings)
      ok <- c(beta = identical(unname(w$beta), pa$beta), iter = identical(w$iter, pa$iter),
              theta = identical(w$thetas, pa$theta), sigma = identical(w$sigmas, pa$sigma),
              ladder = identical(w$lambda0, lad_d$lambda0), lambda1 = identical(w$lambda1, lad_d$lambda1))
      list(status = verdict(all(ok)), details = list(identical = ok, wrapper_warnings = w_cap$warnings,
                                                     final_k = length(w$model)))
    })
    run_test("i3b_storedX_centredy_vs_wrapper_tolerance", function() {
      w <- w_cap$value
      pb <- a2_native_path(Xd, yd - mean(yd), lad_d$lambda0, lad_d$lambda1, settings)
      L <- length(lad_d$lambda0)
      same_support <- identical(which(pb$beta[, L] != 0), as.integer(w$model))
      dmax <- max(abs(pb$beta[, L] - unname(w$beta[, L])))
      list(status = "RECORDED", details = list(same_final_support = same_support, max_abs_dbeta_final = dmax,
                                               within_1e8 = dmax <= 1e-8,
                                               max_abs_dbeta_path = max(abs(pb$beta - unname(w$beta)))))
    })

    # i.4 No-intercept canary (and §IV.3 test 3 a-b): variance = "fixed" with the same explicit
    # sigma0 = 1; native on y and y + 3 (X centred) gives beta-hat equal to 1e-10; the path on
    # ya = y + 3 equals the path on ya - mean(ya), and per-point RSS(ya) = RSS(ya - mean) + n mean^2.
    run_test("i4_no_intercept_canary", function() {
      s <- with_a2(settings, VARIANCE = "fixed")
      L <- length(lad_d$lambda0)
      p0 <- a2_native_path(Xd, yd, lad_d$lambda0, lad_d$lambda1, s, sigma0 = 1)
      ya <- yd + 3
      p3 <- a2_native_path(Xd, ya, lad_d$lambda0, lad_d$lambda1, s, sigma0 = 1)
      pc <- a2_native_path(Xd, ya - mean(ya), lad_d$lambda0, lad_d$lambda1, s, sigma0 = 1)
      e_final <- max(abs(p3$beta[, L] - p0$beta[, L]))
      e_path_c <- max(abs(p3$beta - pc$beta))
      ta <- a2_path_table(Xd, ya, p3, lad_d$lambda0); tc <- a2_path_table(Xd, ya - mean(ya), pc, lad_d$lambda0)
      rss_rel <- max(abs(ta$rss - (tc$rss + n_d * mean(ya)^2)) / ta$rss)
      list(status = verdict(e_final <= 1e-10 && e_path_c <= 1e-10 && rss_rel <= 1e-10 && p0$iter[L] < p0$max_iter),
           details = list(max_abs_dbeta_final_y_vs_y3 = e_final, max_abs_dbeta_path_y3_vs_centred = e_path_c,
                          max_rel_rss_identity_error = rss_rel, final_k = sum(p0$beta[, L] != 0),
                          mean_ya = mean(ya)))
    })

    # i.5 Audit code check on an analytic fixture: separable, fixed variance, sigma0 = 1,
    # theta = 0.3, lambda1 = 0.5, lambda0 = 20, eps = 1e-12, max_iter = 1e5, n = 50, p = 120,
    # seed TEST_SEED. With theta and sigma fixed, the audit must report a fixed-point error
    # <= 1e-9 and a support identical to the map's.
    run_test("i5_audit_analytic_fixture", function() {
      set_rng(settings$TEST_SEED)
      X <- matrix(stats::rnorm(50 * 120), 50, 120)
      b0 <- c(2, -1.5, 1, rep(0, 117))
      y <- as.vector(X %*% b0 + stats::rnorm(50))
      s <- with_a2(settings, PENALTY = "separable", VARIANCE = "fixed", THETA_INIT = 0.3, EPS = 1e-12, MAX_ITER = 100000L)
      pa <- a2_native_path(X, y, 20, 0.5, s, sigma0 = 1)
      au <- a2_fixed_point_audit(X, y, pa$beta[, 1], 1, 0.3, 20, 0.5)
      list(status = verdict(au$max_abs_fixed_point_error <= 1e-9 && au$support_mismatch == 0 &&
                              pa$iter < pa$max_iter && identical(pa$theta, 0.3)),
           details = list(fixed_point_error = au$max_abs_fixed_point_error, support_mismatch = au$support_mismatch,
                          k = sum(pa$beta[, 1] != 0), sweeps = pa$iter, theta_exported = pa$theta,
                          fixture_sha256 = f64_sha256(c(X, y))))
    })

    # i.6 Determinism (§IV.3 test 5): two runs are identical(), for both variants; run from an
    # empty working directory with no data tree present (§III.3.9: wrapper runs without truth/).
    run_test("i6_determinism", function() {
      wd <- getwd(); tmp <- tempfile("a2_empty_wd_"); dir.create(tmp); setwd(tmp)
      on.exit({ setwd(wd); unlink(tmp, recursive = TRUE) }, add = TRUE)
      f1 <- fit_A2_ssl(Xd, yd, fd, sd_seed, prim); f2 <- fit_A2_ssl(Xd, yd, fd, sd_seed, prim)
      g1 <- fit_A2_ssl(Xd, yd, fd, sd_seed, rs);   g2 <- fit_A2_ssl(Xd, yd, fd, sd_seed, rs)
      list(status = verdict(identical(f1, f2) && identical(g1, g2) && f1$rules$status != "failed" && g1$rules$status != "failed"),
           details = list(primary_identical = identical(f1, f2), rs_identical = identical(g1, g2),
                          primary_row = f1$rules, rs_row = g1$rules, working_dir_files = list.files(tmp)))
    })

    # i.7 Failure path (§IV.3 test 6): max_iter = 1 caps the final point -> status "failed" with
    # the returned support kept in support_audit, never the null model; and an uncaught error
    # (version assertion) becomes registered failed rows through the runner's outer tryCatch.
    run_test("i7_failure_path", function() {
      s <- with_a2(prim, MAX_ITER = 1L)
      f <- fit_A2_ssl(Xd, yd, fd, sd_seed, s)
      r <- f$rules
      ok1 <- nrow(r) == 1L && r$status == "failed" && is.na(r$support) && is.na(r$k) &&
             !is.na(r$support_audit) && nzchar(r$support_audit) &&
             identical(r$support_audit, support_key(which(f$diagnostics$beta_final != 0))) &&
             identical(f$converged, FALSE) && all(is.na(f$beta)) &&
             grepl("capped", r$error) && is.null(f$pip)
      s2 <- settings; s2$A2$PKG_VERSION <- "0.0.0"
      mrow <- settings$METHODS[settings$METHODS$method_id == "A2", , drop = FALSE]
      rr <- run_method(mrow, Xd, yd, fd, sd_seed, s2, env)
      r2 <- rr$out$rules
      ok2 <- nrow(r2) == 1L && r2$status == "failed" && is.na(r2$support) && is.na(r2$support_audit) &&
             grepl("^uncaught error:", r2$error) && r2$rule_id == "ssl_final" && r2$role == "primary"
      list(status = verdict(ok1 && ok2),
           details = list(capped_row = r, capped_k_audit = length(parse_key(r$support_audit)), runner_row = r2))
    })

    # i.8 Orthogonal canary (§IV.3 test 1): n = 200, p = 30, X'X = (n - 1) I, five strong
    # signals; production settings must recover the five exactly (primary and SSL-RS).
    set_rng(settings$TEST_SEED + 1L)
    Z <- scale(matrix(stats::rnorm(200 * 30), 200, 30), center = TRUE, scale = FALSE)
    Xo <- qr.Q(qr(Z)) * sqrt(199)
    sig_idx <- c(3L, 7L, 14L, 16L, 25L); b_o <- numeric(30); b_o[sig_idx] <- c(1.4, -1.0, 1.8, -1.2, 0.8)
    eo <- stats::rnorm(200)
    yo <- as.vector(Xo %*% b_o) + eo
    fo <- rep(1:10, length.out = 200)
    run_test("i8_orthogonal_canary", function() {
      ortho_err <- max(abs(crossprod(Xo) - 199 * diag(30)))
      f1 <- fit_A2_ssl(Xo, yo, fo, 1L, prim); f2 <- fit_A2_ssl(Xo, yo, fo, 1L, rs)
      ok <- identical(parse_key(f1$rules$support), sig_idx) && identical(parse_key(f2$rules$support), sig_idx)
      list(status = verdict(ok && ortho_err < 1e-9),
           details = list(orthogonality_error = ortho_err, primary_support = f1$rules$support,
                          rs_support = f2$rules$support, primary_status = f1$rules$status, rs_status = f2$rules$status,
                          primary_codes = f1$rules$diag_codes, rs_codes = f2$rules$diag_codes))
    })

    # §IV.3 test 2: null canary (beta = 0) on the orthogonal design; a rule returning more than
    # 30% of p is flagged for review (RECORDED, not a gate).
    run_test("iv3_null_canary", function() {
      f1 <- fit_A2_ssl(Xo, eo, fo, 1L, prim); f2 <- fit_A2_ssl(Xo, eo, fo, 1L, rs)
      list(status = "RECORDED", details = list(primary_k = f1$rules$k, rs_k = f2$rules$k,
                                               flag_over_30pct = c(f1$rules$k, f2$rules$k) > 0.3 * 30,
                                               primary_status = f1$rules$status, rs_status = f2$rules$status))
    })

    # §III.3.9 / §IV.3 test 7: code grep of the fitting sources for truth-bearing identifiers.
    run_test("iv3_no_oracle_grep", function() {
      files <- c(file.path(code_dir, c("config.R", "common.R", "run_case.R")),
                 list.files(file.path(code_dir, "methods"), pattern = "\\.R$", full.names = TRUE))
      pat <- "truth|\\$active|\\$signal|truth/"
      hits <- unlist(lapply(files, function(f) { l <- readLines(f); i <- grep(pat, l); if (length(i)) paste0(basename(f), ":", i) }))
      list(status = verdict(length(hits) == 0L), details = list(files = basename(files), hits = hits))
    })

    st <- vapply(results, `[[`, "", "status")
    saveRDS(results, file.path(out_dir, "unit_test_results.rds"))
    summary <- data.frame(test = names(st), status = unname(st),
                          seconds = vapply(results, function(r) round(r$details$seconds, 2), 0))
    utils::write.csv(summary, file.path(out_dir, "unit_test_summary.csv"), row.names = FALSE)
    print(summary, row.names = FALSE)
    cat(sprintf("A2 unit tests: %d PASS, %d FAIL, %d RECORDED\n", sum(st == "PASS"), sum(st == "FAIL"), sum(st == "RECORDED")))
    invisible(all(st != "FAIL"))
  })
}

if (sys.nframe() == 0L) {
  a <- commandArgs(trailingOnly = TRUE)
  get_arg <- function(k) { i <- match(paste0("--", k), a); if (is.na(i)) stop("missing --", k); a[i + 1L] }
  ok <- run_A2_tests(code_dir = normalizePath(get_arg("code")), out_dir = get_arg("out"), dev_input = get_arg("dev_input"))
  quit(status = if (isTRUE(ok)) 0L else 1L)
}
