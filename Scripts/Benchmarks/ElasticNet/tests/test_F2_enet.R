#!/usr/bin/env Rscript
# test_F2_enet.R -- G3 unit tests for F2 (master §III.3.2 i; §IV.3 unit tests 1-7) plus the
# common.R EBIC fixtures (§III.3.1 k) and the engine cross-check at alpha = 1 (§III.3.1 i)
# for this thread's copy of the shared helpers. Run on NOTS only (SLURM job).
# Usage: Rscript tests/test_F2_enet.R <code_dir> <dev_inputs_root> <out_dir>
# Reads dev inputs/ files only (never truth/).

args <- commandArgs(TRUE)
if (length(args) != 3L) stop("usage: test_F2_enet.R <code_dir> <dev_inputs_root> <out_dir>")
code_dir <- normalizePath(args[1]); inputs_root <- normalizePath(args[2]); out_dir <- args[3]
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
if (.Platform$OS.type == "windows") stop("run on NOTS")

cfg <- new.env(parent = baseenv()); sys.source(file.path(code_dir, "config.R"), envir = cfg)
S <- cfg$make_settings("primary")
.libPaths(c(S$COMMON$study_lib, .Library))
stopifnot(startsWith(find.package("glmnet"), S$COMMON$study_lib), packageVersion("glmnet") == "5.1")
E <- new.env(parent = asNamespace("stats"))
for (f in c("common.R", "methods/glmnet_helpers.R", "methods/fit_F2_enet.R"))
  sys.source(file.path(code_dir, f), envir = E)
G <- S$GLMNET; n <- 200L

results <- list(); details <- list()
record <- function(name, expr) {
  t0 <- proc.time()[["elapsed"]]
  v <- tryCatch(force(expr), error = function(e) e)
  ok <- !inherits(v, "error")
  results[[name]] <<- data.frame(test = name, passed = ok,
                                 seconds = round(proc.time()[["elapsed"]] - t0, 2),
                                 note = if (ok) "" else conditionMessage(v), stringsAsFactors = FALSE)
  if (ok) details[[name]] <<- v
  cat(if (ok) "PASS" else "FAIL", name, if (!ok) paste("--", conditionMessage(v)), "\n")
  flush.console()
}
check <- function(cond, msg) if (!isTRUE(cond)) stop(msg, call. = FALSE)
load_dev <- function(p, s) readRDS(file.path(inputs_root, sprintf("p%04d", p),
                                             sprintf("dev_p%04d_S%d_r001.rds", p, s)))
soft <- function(z, t) sign(z) * pmax(abs(z) - t, 0)

# Orthogonal design: centred, X'X = (n - 1) I (§IV.3 item 1).
set.seed(S$TEST_SEED)
Z <- scale(matrix(rnorm(n * 30), n), center = TRUE, scale = FALSE)
Xo <- qr.Q(qr(Z)) * sqrt(n - 1); attributes(Xo) <- list(dim = c(n, 30L))
bo <- numeric(30); bo[c(3, 8, 14, 21, 27)] <- c(1.5, -1.2, 1.0, -0.8, 1.3)
yo <- drop(Xo %*% bo) + rnorm(n)
fo <- rep(1:10, length.out = n)

# ---- 1. Orthogonal canary: closed form at every (α, λ) ------------------------------------
record("orthogonal_closed_form", {
  check(max(abs(crossprod(Xo) - (n - 1) * diag(30))) < 1e-9, "design is not orthogonal")
  E$assert_inputs(Xo, yo, fo, S$COMMON)
  z <- drop(crossprod(Xo, yo)) / n; zmax <- max(abs(z)); sx2 <- (n - 1) / n
  frac <- E$lambda_fraction(S$GRID); worst <- 0
  for (a in S$F2$alphas) {
    lam <- S$GRID$max_mult * zmax / a * frac
    pth <- E$glmnet_target_path(Xo, yo, a, lam, rep(1, 30), G)
    closed <- sapply(lam, function(l) soft(z, l * a) / (sx2 + l * (1 - a)))
    worst <- max(worst, max(abs(pth$B - closed)))
  }
  check(worst <= 1e-8 * max(1, zmax), sprintf("max deviation %.3g", worst))
  list(max_abs_dev = worst, zmax = zmax)
})

# ---- 1b. Orthogonal canary: the wrapper recovers the 5 -------------------------------------
# §IV.3 item 1: "Every method must recover the 5 exactly". Checked per rule; the primary rule
# (cv_min) is a hard check with the master's wording (Sol review finding 1).
orth_fit <- tryCatch(E$fit_F2_enet(Xo, yo, fo, S$TEST_SEED, S), error = function(e) e)
truth5 <- paste(which(bo != 0), collapse = ";")
orth_rows <- function() {
  if (inherits(orth_fit, "error")) stop(conditionMessage(orth_fit))
  r <- orth_fit$rules
  check(all(r$status %in% c("ok", "warning")), "a rule failed on the orthogonal canary")
  r
}
record("orthogonal_recovery_cv_min_exact (master, primary rule)", {
  r <- orth_rows(); s <- r$support[r$rule_id == "cv_min"]
  check(identical(s, truth5), sprintf("cv_min support %s (k = %d) != the 5 (%s)", s, r$k[r$rule_id == "cv_min"], truth5))
  TRUE
})
record("orthogonal_recovery_S0_rules_exact", {
  r <- orth_rows()
  for (id in c("cv_1se", "ebic1", "ebic05"))
    check(identical(r$support[r$rule_id == id], truth5), paste(id, "did not recover the 5"))
  r[, c("rule_id", "status", "k", "support", "alpha", "lambda", "index", "diag_codes")]
})

# ---- 2. Map identities for every fit -------------------------------------------------------
record("map_identities", {
  d <- load_dev(500, 4); y <- unname(d$Y[, "c100"])
  f <- E$fit_F2_enet(d$X, y, d$foldid, d$method_seed, S)
  fits <- f$diagnostics$fits; ct <- f$diagnostics$cv_table
  check(nrow(fits) == 55L && nrow(ct) == 1000L, "expected 55 fits and a 1,000-row CV table")
  worst <- 0
  for (i in seq_len(nrow(fits))) {
    lam <- ct$lambda[ct$alpha == fits$alpha[i]]; a <- fits$alpha[i]
    l <- lam * fits$m[i]; an <- fits$native_a[i]; s <- fits$s[i]
    e1 <- max(abs(l * an - lam * a) / (lam * a))
    e2 <- max(abs(l * (1 - an) / s - lam * (1 - a)) / (lam * (1 - a)))
    check(abs(fits$m[i] - (a + s * (1 - a))) <= 1e-15 * fits$m[i], "m != alpha + s(1 - alpha)")
    worst <- max(worst, e1, e2)
  }
  check(worst <= 1e-14, sprintf("map identity relative error %.3g", worst))
  # s of each fold equals the RMS of that fold's own training response.
  s_fold <- sapply(1:10, function(k) sqrt(mean(y[d$foldid != k]^2)))
  check(max(abs(fits$s[fits$data != "full"] - rep(s_fold, 5))) == 0, "fold s is not the fold's own RMS")
  list(max_rel_err = worst)
})

# ---- 3. Generic-backend cross-check at p = 500 (§IV.3 item 4) ------------------------------
# The master's coefficient tolerances are kept as hard checks (they fail at small λ, where
# the only curvature left is the ridge term λ(1 - α); see diag_accuracy.R, MASTER_CHANGES.md).
# Separate checks record what does hold: identical supports and KKT certificates.
gb <- tryCatch({
  d <- load_dev(500, 4); X <- d$X; y <- unname(d$Y[, "c100"]); p <- ncol(X)
  zmax <- max(abs(crossprod(X, y))) / n; frac <- E$lambda_fraction(S$GRID)
  idx <- unique(round(seq(1, S$GRID$nlambda, length.out = 20)))
  lapply(setNames(c(.1, .9), c("alpha_0.1", "alpha_0.9")), function(a) {
    lam <- (S$GRID$max_mult * zmax / a * frac)[idx]
    ours <- E$glmnet_target_path(X, y, a, lam, rep(1, p), G)
    gen <- glmnet::glmnet(X, y, family = gaussian(), alpha = a, lambda = lam,
                          intercept = FALSE, standardize = FALSE,
                          control = list(thresh = G$thresh, maxit = G$maxit))
    Bg <- as.matrix(gen$beta)
    list(alpha = a, lam = lam, B = ours$B, Bg = Bg, kkt_ours = ours$kkt,
         kkt_gen = E$kkt_glmnet(X, y, Bg, lam, a, rep(1, p), max(1, zmax)),
         diff = apply(abs(Bg - ours$B), 2, max), tol = 1e-6 * max(1, max(abs(ours$B))))
  })
}, error = function(e) e)
record("generic_backend_p500_coef_1e-6 (master tolerance)", {
  if (inherits(gb, "error")) stop(conditionMessage(gb))
  for (g in gb) check(max(g$diff) <= g$tol, sprintf("alpha %.2f: max |diff| %.3g > %.3g (first index over: %d of 20)",
                                                   g$alpha, max(g$diff), g$tol, which(g$diff > g$tol)[1]))
  lapply(gb, function(g) signif(g$diff, 3))
})
record("generic_backend_p500_kkt_and_supports", {
  if (inherits(gb, "error")) stop(conditionMessage(gb))
  for (g in gb) {
    check(max(g$kkt_ours) <= 1e-6, sprintf("alpha %.2f: our KKT %.3g", g$alpha, max(g$kkt_ours)))
    check(max(g$kkt_gen) <= 1e-6, sprintf("alpha %.2f: generic KKT %.3g", g$alpha, max(g$kkt_gen)))
    check(identical(g$B != 0, g$Bg != 0), sprintf("alpha %.2f: supports differ", g$alpha))
  }
  lapply(gb, function(g) c(max_kkt_ours = max(g$kkt_ours), max_kkt_generic = max(g$kkt_gen),
                           max_abs_diff = max(g$diff)))
})

# ---- 4. No-intercept canary (§IV.3 item 3) -------------------------------------------------
ni <- tryCatch({
  d <- load_dev(500, 4); X <- d$X; p <- ncol(X)
  yc <- unname(d$Y[, "c100"]); yc <- yc - mean(yc); y3 <- yc + 3
  zmax <- max(abs(crossprod(X, yc))) / n
  check(abs(max(abs(crossprod(X, y3))) / n - zmax) <= 1e-12 * zmax, "X'y changed with the shift")
  frac <- E$lambda_fraction(S$GRID)
  per_alpha <- lapply(S$F2$alphas, function(a) {
    lam <- S$GRID$max_mult * zmax / a * frac
    P3 <- E$glmnet_target_path(X, y3, a, lam, rep(1, p), G)
    Pc <- E$glmnet_target_path(X, yc, a, lam, rep(1, p), G)
    # (b) RSS(y) = RSS(y - ybar) + n ybar^2 for every distinct path support with k <= 100.
    sup <- unique(lapply(seq_len(ncol(Pc$B)), function(i) which(Pc$B[, i] != 0)))
    sup <- sup[lengths(sup) <= S$COMMON$kmax_ebic]
    rss_err <- max(vapply(sup, function(s) {
      r3 <- E$ols_rss(X, y3, s, 1e-10)$rss; rc <- E$ols_rss(X, yc, s, 1e-10)$rss
      abs(r3 - (rc + n * 9)) / (rc + n * 9) }, 0))
    list(alpha = a, rel_diff = max(abs(P3$B - Pc$B)) / max(1, max(abs(Pc$B))),
         same_support = identical(P3$B != 0, Pc$B != 0),
         max_kkt = max(P3$kkt, Pc$kkt), rss_err = rss_err)
  })
  f3 <- E$fit_F2_enet(X, y3, d$foldid, d$method_seed, S)
  fc <- E$fit_F2_enet(X, yc, d$foldid, d$method_seed, S)
  list(per_alpha = do.call(rbind, lapply(per_alpha, as.data.frame)),
       choices = data.frame(rule = f3$rules$rule_id, k_y3 = f3$rules$k, k_yc = fc$rules$k,
                            alpha_y3 = f3$rules$alpha, alpha_yc = fc$rules$alpha,
                            same_support = f3$rules$support == fc$rules$support))
}, error = function(e) e)
record("no_intercept_paths_1e-8 (master tolerance)", {
  if (inherits(ni, "error")) stop(conditionMessage(ni))
  w <- max(ni$per_alpha$rel_diff)
  check(w <= 1e-8, sprintf("paths differ by %.3g (relative); per alpha: %s", w,
                           paste(signif(ni$per_alpha$rel_diff, 3), collapse = ", ")))
  ni$per_alpha
})
record("no_intercept_supports_kkt_rss", {
  if (inherits(ni, "error")) stop(conditionMessage(ni))
  check(all(ni$per_alpha$same_support), "path supports differ between y - ybar and y - ybar + 3")
  check(all(ni$per_alpha$max_kkt <= 1e-6), "KKT above 1e-6")
  check(all(ni$per_alpha$rss_err <= 1e-10), "RSS identity off")
  # (c) CV and EBIC choices are reported, not required to agree.
  list(per_alpha = ni$per_alpha, choices = ni$choices)
})

# ---- 5. Null canary (§IV.3 item 2) ----------------------------------------------------------
record("null_canary", {
  d <- load_dev(500, 1); set.seed(S$TEST_SEED + 1L); y0 <- rnorm(n)
  f <- E$fit_F2_enet(d$X, y0, d$foldid, d$method_seed, S)
  r <- f$rules
  check(all(r$status %in% c("ok", "warning")), "a rule failed on the null canary")
  k <- ifelse(is.na(r$k), NA, r$k)
  list(rules = r[, c("rule_id", "status", "k", "alpha", "index", "diag_codes")],
       review_flag = r$rule_id[!is.na(k) & k > 0.3 * ncol(d$X)])
})

# ---- 6. Determinism (§IV.3 item 5) ---------------------------------------------------------
record("determinism", {
  d <- load_dev(500, 1); y <- unname(d$Y[, "c100"])
  f1 <- E$fit_F2_enet(d$X, y, d$foldid, d$method_seed, S)
  f2 <- E$fit_F2_enet(d$X, y, d$foldid, d$method_seed, S)
  check(identical(f1$rules, f2$rules), "rule rows differ")
  check(identical(f1$diagnostics$cv_table$cvm, f2$diagnostics$cv_table$cvm), "cvm not bit-identical")
  check(identical(f1$beta, f2$beta), "beta not bit-identical")
  TRUE
})

# ---- 7. Failure paths (§IV.3 item 6) -------------------------------------------------------
is_failed_fit <- function(f, p) {
  r <- f$rules
  nrow(r) == 4L && identical(r$rule_id, c("cv_min", "cv_1se", "ebic1", "ebic05")) &&
    all(r$status == "failed") && all(is.na(r$support)) && all(is.na(r$k)) &&
    all(is.na(r$support_audit)) && all(!r$converged) && length(f$beta) == p && all(is.na(f$beta)) &&
    is.null(f$pip)
}
record("failure_solver_maxit", {
  S2 <- S; S2$GLMNET$maxit <- 1
  f <- E$fit_F2_enet(Xo, yo, fo, S$TEST_SEED, S2)
  check(is_failed_fit(f, 30L), "maxit = 1 did not give four failed rows")
  list(error = f$rules$error[1], warnings = f$warnings)
})
record("failure_rule_level_kkt", {
  S2 <- S; S2$GLMNET$kkt_rel_tol <- -1          # every point "violates"
  f <- E$fit_F2_enet(Xo, yo, fo, S$TEST_SEED, S2)
  r <- f$rules
  check(all(r$diag_flag) && all(grepl("kkt_path", r$diag_codes)), "flag not method-wide")
  cv <- r[r$rule_id %in% c("cv_min", "cv_1se"), ]
  check(all(cv$status == "failed") && all(is.na(cv$support)) && all(!is.na(cv$support_audit)) &&
        all(is.na(cv$k)) && all(cv$converged), "CV rule failure semantics wrong")
  eb <- r[r$rule_id %in% c("ebic1", "ebic05"), ]
  # A non-null EBIC choice has no KKT-passing occurrence -> failed; a null choice stays valid.
  for (i in seq_len(nrow(eb))) {
    if (eb$status[i] == "failed")
      check(!is.na(eb$support_audit[i]) && nzchar(eb$support_audit[i]) && is.na(eb$support[i]) &&
            is.na(eb$k[i]), "failed EBIC row semantics wrong")
    else check(identical(eb$support[i], ""), "an EBIC row with a non-null support passed")
  }
  r[, c("rule_id", "status", "support", "support_audit", "k", "diag_flag", "diag_codes")]
})
record("failure_input_assertion_and_fail_rows", {
  Xb <- Xo; Xb[, 1] <- Xb[, 1] + 1                # not centred
  e <- tryCatch(E$fit_F2_enet(Xb, yo, fo, 1L, S), error = function(e) conditionMessage(e))
  check(is.character(e) && grepl("centred", e), "uncentred X was not rejected")
  fr <- E$fail_rows(S$METHODS[1, , drop = FALSE], e, E$F2_EXTRA_COLS)
  check(identical(fr$rule_id, S$METHODS$rule_ids[[1]]) && identical(fr$role, S$METHODS$roles[[1]]) &&
        all(fr$status == "failed") && all(is.na(fr$support)) && all(is.na(fr$k)), "fail_rows shape")
  e2 <- tryCatch(E$fit_F2_enet(Xo, yo, c(fo[-1], 11L), 1L, S), error = function(e) conditionMessage(e))
  check(is.character(e2), "bad fold labels were not rejected")
  e3 <- tryCatch({ S3 <- S; S3$GLMNET$pkg_version <- "0.0"; E$fit_F2_enet(Xo, yo, fo, 1L, S3) },
                 error = function(e) conditionMessage(e))
  check(is.character(e3) && grepl("version", e3), "version assertion did not fire")
  c(e, e2, e3)
})

# ---- 8. Runner end to end: outer failure layer and no-oracle run (§III.3.0, §III.3.9) ------
runner <- new.env(); sys.source(file.path(code_dir, "run_case.R"), envir = runner)
tmp <- file.path(out_dir, "tmp"); dir.create(tmp, showWarnings = FALSE)
record("runner_outer_failure", {
  bad <- file.path(tmp, "code_badversion"); dir.create(file.path(bad, "methods"), recursive = TRUE,
                                                       showWarnings = FALSE)
  for (f in runner$CODE_FILES) file.copy(file.path(code_dir, f), file.path(bad, f), overwrite = TRUE)
  cf <- readLines(file.path(bad, "config.R"))
  cf <- sub('pkg_version = "5.1"$', 'pkg_version = "0.0"', cf)   # GLMNET block only
  writeLines(cf, file.path(bad, "config.R"))
  inp <- file.path(tmp, "inputs", "p0500"); dir.create(inp, recursive = TRUE, showWarnings = FALSE)
  file.copy(file.path(inputs_root, "p0500", "dev_p0500_S1_r001.rds"), inp, overwrite = TRUE)
  runner$main(c("--input", file.path(inp, "dev_p0500_S1_r001.rds"), "--out", file.path(tmp, "res_bad"),
                "--run-id", "unit_bad", "--code-dir", bad))
  csv <- read.csv(file.path(tmp, "res_bad", "unit_bad", "p0500", "dev_p0500_S1_r001_c100", "F2.csv"),
                  stringsAsFactors = FALSE)
  check(nrow(csv) == 4L && all(csv$status == "failed") && all(is.na(csv$support)) &&
        all(grepl("version", csv$error)), "runner did not write registered failed rows")
  csv[, c("rule_id", "status", "error")]
})
record("no_oracle_grep", {
  files <- file.path(code_dir, c("config.R", "common.R", "methods/glmnet_helpers.R",
                                 "methods/fit_F2_enet.R"))
  hits <- unlist(lapply(files, function(f) {
    src <- readLines(f)
    i <- grep("truth|\\$active|\\$signal|truth/", src)
    if (length(i)) paste0(basename(f), ":", i, ": ", src[i]) else character()
  }))
  check(!length(hits), paste("truth-bearing identifiers found:", paste(hits, collapse = " || ")))
  TRUE
})
record("no_oracle_run_without_truth", {
  # The wrapper and runner run on a copy of an input file in a tree with no truth/ directory;
  # every file-opening base function errors if a path containing "truth" is opened.
  guard <- quote({
    f0 <- c(if (exists("file", inherits = FALSE)) file,
            if (exists("description", inherits = FALSE)) description)
    if (is.character(f0) && any(grepl("truth", f0))) stop("attempted to open a truth path")
  })
  for (fn in c("readRDS", "file", "gzfile", "load")) trace(fn, tracer = guard, where = baseenv(), print = FALSE)
  on.exit(for (fn in c("readRDS", "file", "gzfile", "load")) untrace(fn, where = baseenv()), add = TRUE)
  check(!dir.exists(file.path(tmp, "truth")), "temporary tree has a truth directory")
  inp <- file.path(tmp, "inputs", "p0500", "dev_p0500_S1_r001.rds")
  runner$main(c("--input", inp, "--out", file.path(tmp, "res_ok"), "--run-id", "unit_ok",
                "--code-dir", code_dir))
  csv <- read.csv(file.path(tmp, "res_ok", "unit_ok", "p0500", "dev_p0500_S1_r001_c100", "F2.csv"),
                  stringsAsFactors = FALSE)
  check(nrow(csv) == 4L && all(csv$status %in% c("ok", "warning")), "clean runner call failed")
  check(all(is.na(csv$tp)) && all(is.na(csv$exact)), "truth columns filled at fit time")
  csv[, c("rule_id", "status", "k", "alpha", "runtime_s")]
})

# ---- 9. Control hygiene and grid check (§III.3.1 i) ----------------------------------------
record("control_hygiene", {
  before <- glmnet::glmnet.control()
  f <- E$fit_F2_enet(Xo, yo, fo, 1L, S)
  check(identical(before, glmnet::glmnet.control()), "glmnet.control() changed")
  check(!any(grepl("deprecat", c(f$warnings, f$messages), ignore.case = TRUE)), "deprecation warning")
  check(length(f$warnings) == 0L && length(f$messages) == 0L, "unexpected conditions")
  TRUE
})
record("grid_first_point_null", {
  out <- c()
  for (p in c(500, 1000)) {
    d <- load_dev(p, 3); y <- unname(d$Y[, "c100"])
    zmax <- max(abs(crossprod(d$X, y))) / n; frac <- E$lambda_fraction(S$GRID)
    for (a in S$F2$alphas) {
      lam <- S$GRID$max_mult * zmax / a * frac
      pth <- E$glmnet_target_path(d$X, y, a, lam[1:3], rep(1, p), G)
      check(all(pth$B[, 1] == 0), sprintf("p %d alpha %.2f: first point not null", p, a))
    }
    out[paste0("p", p)] <- TRUE
  }
  out
})

# ---- 10. Engine at alpha = 1 against cv.glmnet (one dev case per p) ------------------------
record("engine_vs_cv_glmnet_alpha1", {
  out <- list()
  for (p in c(500, 1000)) {
    d <- load_dev(p, 2); X <- d$X; y <- unname(d$Y[, "c100"])
    zmax <- max(abs(crossprod(X, y))) / n
    lam <- S$GRID$max_mult * zmax * E$lambda_fraction(S$GRID)
    eng <- E$glmnet_cv_engine(X, y, d$foldid, 1, lam, rep(1, p), G)
    ref <- glmnet::cv.glmnet(X, y, alpha = 1, lambda = lam, foldid = d$foldid, intercept = FALSE,
                             standardize = FALSE, type.gaussian = "naive", type.measure = "mse",
                             grouped = TRUE, keep = TRUE,
                             control = list(thresh = G$thresh, maxit = G$maxit, fdev = G$fdev,
                                            devmax = G$devmax))
    rel <- function(a, b) max(abs(a - b) / pmax(abs(b), 1e-300))
    e_cvm <- rel(eng$cvm, ref$cvm); e_sd <- rel(eng$cvsd, ref$cvsd)
    e_pre <- max(abs(eng$oof - ref$fit.preval)) / max(1, max(abs(ref$fit.preval)))
    ch <- E$cv_choose(eng$cvm, eng$cvsd)
    check(e_cvm <= 1e-10 && e_sd <= 1e-10 && e_pre <= 1e-10,
          sprintf("p %d: cvm %.2g cvsd %.2g preval %.2g", p, e_cvm, e_sd, e_pre))
    check(identical(unname(ch), as.integer(ref$index[, 1])), sprintf("p %d: index differs", p))
    out[[paste0("p", p)]] <- c(cvm = e_cvm, cvsd = e_sd, preval = e_pre, i_min = ch[[1]], i_1se = ch[[2]],
                               max_kkt_full = max(eng$full$kkt), max_kkt_fold = max(eng$kkt_fold))
  }
  out
})

# ---- 11. EBIC scorer fixtures (common.R; Oct-14 validate.R) --------------------------------
record("ebic_fixtures", {
  X <- cbind(c(-2, -1, 0, 1, 2), c(1, -2, 2, -2, 1)); y <- c(1, 3, -2, 4, 7)
  check(E$ols_rss(X, y, integer(), 1e-10)$rss == sum(y^2), "null RSS")
  b <- solve(crossprod(X), crossprod(X, y)); rss <- sum((y - X %*% b)^2)
  cand <- E$ebic_candidates(X, y, list(1L, 1:2, c(2L, 1L)), 100L, c(ebic1 = 1, ebic05 = .5), 1e-10)
  check(nrow(cand) == 3L && identical(cand$key, c("", "1", "1;2")), "dedup / null candidate")
  check(abs(cand$rss[3] - rss) <= 1e-12 * rss, "two-variable RSS")
  check(abs(cand$ebic1[3] - (5 * log(rss / 5) + 2 * log(5) + 2 * lchoose(2, 2))) <= 1e-12, "two-variable score")
  r1 <- sum(lm.fit(X[, 1, drop = FALSE], y)$residuals^2)
  check(abs(cand$ebic05[2] - (5 * log(r1 / 5) + log(5) + lchoose(2, 1))) <= 1e-12, "singleton score")
  cd <- E$ebic_candidates(cbind(X[, 1], X[, 1]), y, list(1:2), 100L, c(ebic1 = 1), 1e-10)
  check(is.infinite(cd$ebic1[2]) && !cd$valid[2], "rank deficiency -> Inf")
  tie <- data.frame(key = c("2", "10", "1;2", ""), k = c(1L, 1L, 2L, 0L), valid = TRUE,
                    ebic1 = c(1, 1, 1, 2), stringsAsFactors = FALSE)
  check(E$ebic_pick(tie, "ebic1")$key == "10", "C-locale tie order ('10' < '2')")
  check(E$occurrence_ok("", c("1", "2"), c(FALSE, FALSE)), "null support must be valid")
  check(!E$occurrence_ok("1", c("1", "2"), c(FALSE, TRUE)), "occurrence check")
  TRUE
})

# ---- 12. enet_choose tie rule ----------------------------------------------------------------
record("enet_choose_ties", {
  ct <- data.frame(alpha = rep(c(.1, .5, .9), each = 3), lambda = c(3, 2, 1, 6, 4, 2, 9, 6, 3),
                   cvm = c(1, 0.5, 0.5, 0.6, 0.5, 0.5, 0.8, 0.6, 0.55), cvsd = 0.1)
  # min cvm 0.5 at rows 2, 3, 5, 6 (rows 7-9 have alpha .9 but larger cvm): largest alpha
  # among the ties is .5, then the largest lambda -> row 5. 1se threshold 0.5 + 0.1 = 0.6;
  # within alpha .5 rows 4 (0.6, boundary included), 5, 6 qualify -> largest lambda: row 4.
  ch <- E$enet_choose(ct)
  check(ch[["min"]] == 5L, "ties: largest alpha then largest lambda")
  check(ch[["one_se"]] == 4L, "1se: largest lambda within alpha* with cvm <= cvm_min + cvsd_min")
  TRUE
})

res <- do.call(rbind, results); rownames(res) <- NULL
saveRDS(list(results = res, details = details,
             precomputed = list(generic = if (!inherits(gb, "error"))
                                  lapply(gb, function(g) g[c("alpha", "lam", "kkt_ours", "kkt_gen", "diff", "tol")]),
                                no_intercept = if (!inherits(ni, "error")) ni),
             session = capture.output(sessionInfo()),
             host = Sys.info()[["nodename"]], job = Sys.getenv("SLURM_JOB_ID"),
             time = format(Sys.time(), tz = "UTC", usetz = TRUE)),
        file.path(out_dir, "unit_test_results.rds"))
write.csv(res, file.path(out_dir, "unit_test_results.csv"), row.names = FALSE)
print(res, right = FALSE)
cat("\nDETAILS\n"); str(details, max.level = 3, vec.len = 6)
cat(sprintf("\n%d of %d tests passed\n", sum(res$passed), nrow(res)))
if (!all(res$passed)) quit(status = 1L)
