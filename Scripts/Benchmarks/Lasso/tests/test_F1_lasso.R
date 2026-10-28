#!/usr/bin/env Rscript
# test_F1_lasso.R -- G3 unit tests for F1 (master §III.3.1 i and §IV.3 unit tests 1-3, 5-7), all that do
# not need the pilot. Reads dev inputs only (never the dev truth files).
# Usage: Rscript --vanilla tests/test_F1_lasso.R <code_dir> <dev_inputs_root> <out_dir>
#   dev_inputs_root = .../bench20261019/dev/inputs (holds p0500/, p1000/)

if (nzchar(Sys.getenv("BENCH_LIB"))) .libPaths(c(Sys.getenv("BENCH_LIB"), .Library))
args <- commandArgs(trailingOnly = TRUE)
code_dir <- normalizePath(args[[1]]); inputs_root <- normalizePath(args[[2]]); out_dir <- args[[3]]
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
cfg <- new.env(parent = baseenv()); sys.source(file.path(code_dir, "config.R"), envir = cfg)
settings <- as.list(cfg); settings$variant <- "primary"
e <- new.env(parent = asNamespace("stats"))
for (f in c("common.R", "methods/glmnet_helpers.R", "methods/fit_F1_lasso.R"))
  sys.source(file.path(code_dir, f), envir = e)
G <- settings$GLMNET; TEST_SEED <- settings$TEST_SEED

checks <- list(); info <- list()
record <- function(name, expr) {
  t0 <- proc.time()[["elapsed"]]
  a <- tryCatch(force(expr), error = function(err) err); ok <- !inherits(a, "error")
  checks[[name]] <<- list(passed = ok, detail = if (ok) a else conditionMessage(a),
                          seconds = proc.time()[["elapsed"]] - t0)
  cat(if (ok) "PASS" else "FAIL", name, if (!ok) paste("--", conditionMessage(a)), "\n"); flush(stdout())
}
dev <- function(p, s) readRDS(file.path(inputs_root, sprintf("p%04d", p), sprintf("dev_p%04d_S%d_r001.rds", p, s)))
fit <- function(X, y, foldid, st = settings, seed = 1L) e$fit_F1_lasso(X, y, foldid, seed, st)
grid_for <- function(X, y) settings$GRID$max_mult * max(abs(crossprod(X, y))) / nrow(X) * e$lambda_fraction(settings$GRID)
soft <- function(z, l) sign(z) * pmax(abs(z) - l, 0)

# ---- 1. orthogonal canary (n = 200, p = 30, X'X = (n - 1) I, X centred) ---------------------------
set.seed(TEST_SEED)
n <- 200L; p0 <- 30L
M <- scale(matrix(rnorm(n * p0), n), center = TRUE, scale = FALSE)
Xo <- sqrt(n - 1) * qr.Q(qr(M))                          # columns orthogonal, orthogonal to 1
b0 <- numeric(p0); b0[c(3, 7, 14, 16, 25)] <- c(1.4, -1.0, 1.8, -1.2, 0.8)
yo <- drop(Xo %*% b0) + rnorm(n)
fo <- sample(rep(1:10, length.out = n))

record("1a orthogonal design is centred, unit sd, X'X = (n-1)I", {
  stopifnot(max(abs(crossprod(Xo) - (n - 1) * diag(p0))) < 1e-9, isTRUE(e$assert_inputs(Xo, yo, fo, settings$COMMON)))
  TRUE
})
record("1b orthogonal canary: full path equals soft-threshold closed form within 1e-8*max(1,zmax)", {
  lam <- grid_for(Xo, yo); z <- drop(crossprod(Xo, yo)) / n; s2 <- (n - 1) / n
  path <- e$glmnet_target_path(Xo, yo, 1, lam, rep(1, p0), G)
  cf <- vapply(lam, function(l) soft(z, l) / s2, numeric(p0))
  err <- max(abs(path$B - cf)); tol <- 1e-8 * max(1, max(abs(z)))
  if (err > tol) stop("max abs error ", err, " > ", tol)
  # KKT of the closed form is ~0; a perturbed solution must show a violation
  kcf <- e$kkt_glmnet(Xo, yo, cf, lam, 1, rep(1, p0), max(1, max(abs(z))))
  bad <- cf; bad[3, ] <- bad[3, ] + 0.01
  kbad <- e$kkt_glmnet(Xo, yo, bad, lam, 1, rep(1, p0), max(1, max(abs(z))))
  stopifnot(max(kcf) < 1e-12, min(kbad) > 1e-3, max(path$kkt) <= G$kkt_rel_tol)
  c(max_abs_err = err, tol = tol, max_kkt = max(path$kkt))
})
record("1c orthogonal canary: every rule recovers the 5 exactly (§IV.3 item 1)", {
  r <- fit(Xo, yo, fo)$rules
  target <- "3;7;14;16;25"
  info$orthogonal_rules <- r[, c("rule_id", "status", "k", "support")]
  if (!all(r$status == "ok") || !all(r$support == target))
    stop("not exact: ", paste(r$rule_id, r$status, r$support, collapse = " | "))
  setNames(r$support, r$rule_id)
})

# ---- 2. null canary (β = 0) ------------------------------------------------------------------------
# Configurations under test: the frozen config.R only (GLMNET$maxit = 1e7 since the 2026-10-19 decision;
# the runs with the master's 1e6 are kept in the records: jobs 2275376, 2276765).
VARIANTS <- list(config = settings)
for (vn in names(VARIANTS)) {
  record(sprintf("2 [%s] null canary (dev X p=500 S1, y = N(0,1)): fit ok, no rule above 30%% of p", vn), {
    d <- dev(500, 1); set.seed(TEST_SEED); yn <- rnorm(200)
    f0 <- fit(d$X, yn, d$foldid, VARIANTS[[vn]]); r <- f0$rules
    if (!all(r$status == "ok")) stop("fit not ok: ", f0$error)
    stopifnot(all(r$k <= 0.3 * 500))
    setNames(r$k, r$rule_id)
  })
}

# ---- 3. no-intercept canary (y with mean 3, X centred) ---------------------------------------------
d4 <- dev(500, 4); X4 <- d4$X; y4 <- unname(d4$Y[, "c100"]); f4 <- d4$foldid
record("3a no-intercept: full path for y + 3 and y - mean(y) equals path for y (same grid) within 1e-8", {
  lam <- grid_for(X4, y4)
  P0 <- e$glmnet_target_path(X4, y4, 1, lam, rep(1, 500), G)$B
  P3 <- e$glmnet_target_path(X4, y4 + 3, 1, lam, rep(1, 500), G)$B
  Pc <- e$glmnet_target_path(X4, y4 - mean(y4), 1, lam, rep(1, 500), G)$B
  e3 <- max(abs(P3 - P0)); ec <- max(abs(Pc - P0))
  if (e3 > 1e-8 || ec > 1e-8) stop("max diff y+3 ", e3, ", centred ", ec)
  c(max_diff_y_plus_3 = e3, max_diff_centred = ec)
})
record("3a' no-intercept on the orthogonal design: path for y + 3 and y - mean(y) equals path for y within 1e-8", {
  lam <- grid_for(Xo, yo)
  P0 <- e$glmnet_target_path(Xo, yo, 1, lam, rep(1, p0), G)$B
  P3 <- e$glmnet_target_path(Xo, yo + 3, 1, lam, rep(1, p0), G)$B
  Pc <- e$glmnet_target_path(Xo, yo - mean(yo), 1, lam, rep(1, p0), G)$B
  e3 <- max(abs(P3 - P0)); ec <- max(abs(Pc - P0))
  if (e3 > 1e-8 || ec > 1e-8) stop("max diff y+3 ", e3, ", centred ", ec)
  c(max_diff_y_plus_3 = e3, max_diff_centred = ec)
})
record("3b no-intercept: RSS(y) = RSS(y - ybar) + n ybar^2 for every path support (k <= 100)", {
  y3 <- y4 + 3; yb <- mean(y3)
  lam <- grid_for(X4, y3)
  B <- e$glmnet_target_path(X4, y3, 1, lam, rep(1, 500), G)$B
  sup <- unique(lapply(seq_len(ncol(B)), function(j) which(B[, j] != 0)))
  sup <- sup[lengths(sup) <= 100]
  err <- vapply(sup, function(s) {
    a <- e$ols_rss(X4, y3, s, 1e-10)$rss; b <- e$ols_rss(X4, y3 - yb, s, 1e-10)$rss + 200 * yb^2
    abs(a - b) / max(1, a)
  }, 0)
  stopifnot(max(err) < 1e-10)
  c(n_supports = length(sup), max_rel_err = max(err))
})
record("3c no-intercept: CV and EBIC choices for y vs y + 3 (reported, not a failure)", {
  r0 <- fit(X4, y4, f4)$rules; r3 <- fit(X4, y4 + 3, f4)$rules
  info$no_intercept_choices <- data.frame(rule_id = r0$rule_id, k_y = r0$k, k_y3 = r3$k,
                                          same_support = r0$support == r3$support)
  info$no_intercept_choices
})

# ---- engine checks on one dev case per p -----------------------------------------------------------
for (vn in names(VARIANTS)) for (pp in c(500L, 1000L)) {
  st <- VARIANTS[[vn]]; Gv <- st$GLMNET
  d <- dev(pp, 4); X <- d$X; y <- unname(d$Y[, "c100"]); fid <- d$foldid
  lam <- grid_for(X, y)
  res <- NULL
  record(sprintf("4 [%s, p=%d] cross-check against cv.glmnet: cvm, cvsd (1e-10 rel), fit.preval (1e-10), indices exact", vn, pp), {
    eng <- e$glmnet_cv_engine(X, y, fid, 1, lam, rep(1, pp), Gv)
    cvg <- glmnet::cv.glmnet(X, y, alpha = 1, lambda = lam, foldid = fid, intercept = FALSE, standardize = FALSE,
                             type.gaussian = "naive", type.measure = "mse", grouped = TRUE, keep = TRUE,
                             control = list(thresh = Gv$thresh, maxit = Gv$maxit, fdev = Gv$fdev, devmax = Gv$devmax))
    rel <- function(a, b) max(abs(a - b) / pmax(abs(b), .Machine$double.xmin))
    e_cvm <- rel(eng$cvm, cvg$cvm); e_cvsd <- rel(eng$cvsd, cvg$cvsd)
    e_pre <- max(abs(eng$oof - cvg$fit.preval))
    idx <- e$cv_choose(eng$cvm, eng$cvsd)
    stopifnot(length(cvg$lambda) == length(lam), e_cvm <= 1e-10, e_cvsd <= 1e-10, e_pre <= 1e-10,
              identical(unname(idx), as.integer(cvg$index[, 1])),
              max(abs(as.matrix(cvg$glmnet.fit$beta) - eng$full$B)) <= 1e-12)
    c(cvm_rel = e_cvm, cvsd_rel = e_cvsd, preval_abs = e_pre, i_min = idx[[1]], i_1se = idx[[2]])
  })
  record(sprintf("5 [%s, p=%d] KKT at p > n: all 11 fits, every grid point <= 1e-5; first grid point null; converged", vn, pp), {
    res <- fit(X, y, fid, st)
    if (pp == 500L) base500 <- res                      # baseline for the end-to-end no-oracle run (10b)
    if (!is.na(res$error)) stop("fit failed: ", res$error)
    dg <- res$diagnostics
    stopifnot(nrow(dg$fits) == 11L, all(dg$fits$jerr == 0L), isTRUE(res$converged),
              dg$path$k[1] == 0L, dg$path$key[1] == "")
    if (max(dg$fits$kkt_max) > G$kkt_rel_tol) stop("max KKT ", max(dg$fits$kkt_max))
    stopifnot(!any(res$rules$diag_flag), all(res$rules$status == "ok"))
    c(max_kkt = max(dg$fits$kkt_max), max_npasses = max(dg$fits$npasses))
  })
  record(sprintf("6 [%s, p=%d] rule definitions recomputed from saved diagnostics", vn, pp), {
    if (!is.na(res$error)) stop("not run: fit failed (", res$error, ")")
    dg <- res$diagnostics; r <- res$rules; L <- nrow(dg$path)
    i_min <- min(which(dg$path$cvm == min(dg$path$cvm)))
    i_1se <- min(which(dg$path$cvm <= dg$path$cvm[i_min] + dg$path$cvsd[i_min]))
    stopifnot(r$index[1] == i_min, r$index[2] == i_1se, r$support[1] == dg$path$key[i_min],
              r$support[2] == dg$path$key[i_1se], identical(dg$index, c(min = i_min, one_se = i_1se)))
    # EBIC rows: brute-force minimum over the candidate table with the stated tie order
    cd <- dg$candidates
    for (g in c("ebic1", "ebic05")) {
      o <- order(cd[[g]], cd$k, cd$key, method = "radix")[1]
      stopifnot(r$support[r$rule_id == g] == cd$key[o], r$crit_value[r$rule_id == g] == cd[[g]][o],
                r$k_path_max[r$rule_id == g] == max(dg$path$k),
                r$k_valid_max[r$rule_id == g] == max(cd$k[cd$valid]))
    }
    # candidates = null + distinct path supports with k <= 100
    keys <- unique(c("", dg$path$key[dg$path$k <= 100]))
    stopifnot(setequal(cd$key, keys), nrow(cd) == length(keys))
    # beta is the full-data coefficient vector at i_min
    stopifnot(e$support_key(which(res$beta != 0)) == dg$path$key[i_min])
    # CV-row diagnostics: RSS and EBIC(1) of the support
    s <- e$parse_key(r$support[1]); f <- e$ols_rss(X, y, s, 1e-10)
    stopifnot(abs(r$rss[1] - f$rss) <= 1e-12 * f$rss)
    setNames(r$k, r$rule_id)
  })
  record(sprintf("7 [%s, p=%d] determinism: identical supports and bit-identical cvm", vn, pp), {
    if (!is.na(res$error)) stop("not run: fit failed (", res$error, ")")
    res2 <- fit(X, y, fid, st)
    stopifnot(identical(res$rules$support, res2$rules$support), identical(res$diagnostics$path$cvm, res2$diagnostics$path$cvm),
              identical(res$beta, res2$beta))
    TRUE
  })
}

# ---- control hygiene --------------------------------------------------------------------------------
record("8 control hygiene: glmnet.control() unchanged by a fit; no warning or message captured", {
  before <- glmnet::glmnet.control()
  r <- fit(Xo, yo, fo)
  after <- glmnet::glmnet.control()
  stopifnot(identical(before, after), length(r$warnings) == 0L, length(r$messages) == 0L,
            !any(grepl("deprecat", r$warnings, ignore.case = TRUE)))
  TRUE
})

# ---- 6. failure path ---------------------------------------------------------------------------------
rejects <- function(expr) inherits(tryCatch(force(expr), error = function(err) err), "error")
is_failed_fit <- function(r) {
  all(r$rules$status == "failed") && all(is.na(r$rules$support)) && all(is.na(r$rules$k)) &&
    all(is.na(r$beta)) && !is.na(r$error) && nzchar(r$error) && identical(r$rules$converged, rep(FALSE, 4))
}
record("9a failure: non-finite X gives failed rows, never a null-model success", {
  Xb <- Xo; Xb[1, 1] <- NA
  r <- fit(Xb, yo, fo); stopifnot(is_failed_fit(r)); r$error
})
record("9b failure: glmnet maxit reached (jerr != 0) gives failed rows (failure over warning)", {
  st <- settings; st$GLMNET$maxit <- 5
  r <- fit(Xo, yo, fo, st)
  stopifnot(is_failed_fit(r), grepl("jerr", r$error))
  list(error = r$error, warnings = r$warnings)
})
record("9c failure: wrong pinned version gives failed rows", {
  st <- settings; st$GLMNET$pkg_version <- "0.0"
  r <- fit(Xo, yo, fo, st); stopifnot(is_failed_fit(r)); r$error
})
record("9d rule failure: KKT tolerance unattainable -> CV rules failed with support_audit, diag_flag on all rows", {
  st <- settings; st$GLMNET$kkt_rel_tol <- 1e-300
  r <- fit(Xo, yo, fo, st)$rules
  stopifnot(all(r$diag_flag), all(grepl("^kkt_path", r$diag_codes)),
            all(r$status[1:2] == "failed"), all(is.na(r$support[1:2])), all(!is.na(r$support_audit[1:2])),
            all(is.na(r$k[1:2])))
  # EBIC rows fail unless the chosen support is the null support
  stopifnot(all((r$status[3:4] == "failed") == (r$support_audit[3:4] != "" & !is.na(r$support_audit[3:4]))))
  r[, c("rule_id", "status", "support", "support_audit", "diag_codes")]
})
# Engine fixtures with one isolated KKT violation at a time (§III.3.1 f, h). The wrapper runs in a copy of the
# fitting environment whose glmnet_cv_engine() returns a fixed, edited engine result for the orthogonal canary.
lam_o <- grid_for(Xo, yo)
cv0 <- e$glmnet_cv_engine(Xo, yo, fo, 1, lam_o, rep(1, p0), G)
with_engine <- function(cv_mod) {
  e2 <- new.env(parent = asNamespace("stats"))
  for (nm in ls(e)) { obj <- get(nm, envir = e); if (is.function(obj)) environment(obj) <- e2; assign(nm, obj, envir = e2) }
  e2$glmnet_cv_engine <- function(...) cv_mod
  e2$fit_F1_lasso(Xo, yo, fo, 1L, settings)
}
ch0 <- e$cv_choose(cv0$cvm, cv0$cvsd); im <- ch0[["min"]]; i1 <- ch0[["one_se"]]
record("9f isolated KKT violations: each rule fails exactly when its own points fail; flag is method-wide", {
  base <- with_engine(cv0)$rules
  stopifnot(all(base$status == "ok"), !any(base$diag_flag), im != i1)
  out <- list()
  # (a) one fold at i_min: cv_min and cv_1se fail (cv_1se's threshold uses i_min); EBIC rows unaffected
  cv <- cv0; cv$kkt_fold[3, im] <- 1; r <- with_engine(cv)$rules
  stopifnot(identical(r$status, c("failed", "failed", "ok", "ok")), all(r$diag_flag),
            identical(r$support_audit[1:2], base$support[1:2]), identical(r$support[3:4], base$support[3:4]))
  out$a <- r$status
  # (b) one fold at i_1se only: cv_1se fails, cv_min stays ok
  cv <- cv0; cv$kkt_fold[3, i1] <- 1; r <- with_engine(cv)$rules
  stopifnot(identical(r$status, c("ok", "failed", "ok", "ok")), all(r$diag_flag)); out$b <- r$status
  # (c) one fold at an unselected index: every rule ok, flag TRUE with code kkt_path on every row
  j <- setdiff(seq_along(lam_o), c(im, i1))[50]
  cv <- cv0; cv$kkt_fold[3, j] <- 1; r <- with_engine(cv)$rules
  stopifnot(all(r$status == "ok"), all(r$diag_flag), all(grepl("kkt_path", r$diag_codes)),
            identical(r$support, base$support)); out$c <- r$status
  # (d) full data at every occurrence of the ebic1 support: ebic1 fails; other rules fail only if they share points
  key <- base$support[3]; keys <- vapply(seq_along(lam_o), function(l) e$support_key(which(cv0$full$B[, l] != 0)), "")
  occ <- which(keys == key); stopifnot(nzchar(key), length(occ) > 0)
  cv <- cv0; cv$full$kkt[occ] <- 1; r <- with_engine(cv)$rules
  exp_fail <- c(im %in% occ, i1 %in% occ, TRUE, base$support[4] == key)
  stopifnot(identical(r$status == "failed", exp_fail), r$support_audit[3] == key, all(r$diag_flag)); out$d <- r$status
  # (e) a full-data violation only at an index whose support is not chosen by any rule: all ok, flag TRUE
  free <- which(!(keys %in% base$support) & seq_along(lam_o) != 1L)[1]
  cv <- cv0; cv$full$kkt[free] <- 1; r <- with_engine(cv)$rules
  stopifnot(all(r$status == "ok"), all(r$diag_flag)); out$e <- r$status
  out
})
record("9g path rejection: check_glmnet_path stops on each malformed returned fit", {
  L <- 5; lamr <- c(1, .5, .25, .125, .0625)
  good <- list(jerr = 0L, lambda = lamr, a0 = rep(0, L), beta = matrix(0, 3, L))
  stopifnot(isTRUE(e$check_glmnet_path(good, lamr, G)))
  bad <- list(jerr_neg = modifyList(good, list(jerr = -3L)),
              short = modifyList(good, list(lambda = lamr[1:4], beta = matrix(0, 3, 4), a0 = rep(0, 4))),
              altered = modifyList(good, list(lambda = lamr * (1 + 1e-9))),
              intercept = modifyList(good, list(a0 = c(0, 0, 1e-12, 0, 0))),
              nonfinite = modifyList(good, list(beta = replace(matrix(0, 3, L), 4, NaN))))
  hit <- vapply(bad, function(f) rejects(e$check_glmnet_path(f, lamr, G)), TRUE)
  if (!all(hit)) stop("not rejected: ", paste(names(hit)[!hit], collapse = ", "))
  hit
})
record("9e runner: an uncaught error outside the wrapper's capture becomes registered failed rows", {
  rc <- new.env(); sys.source(file.path(code_dir, "run_case.R"), envir = rc)
  h <- new.env(parent = asNamespace("stats")); sys.source(file.path(code_dir, "common.R"), envir = h)
  boom <- function(X, y, foldid, seed, settings) stop("forced")
  r <- rc$call_method(boom, Xo, yo, fo, 1L, settings, settings$METHODS, "F1", h)
  rc$check_result(r, settings$METHODS[1, ], p0)
  stopifnot(is_failed_fit(r), grepl("^runner: forced", r$error)); TRUE
})

# ---- 7. no-oracle -------------------------------------------------------------------------------------
record("10a no-oracle grep: fitting sources contain no truth-bearing identifiers", {
  files <- file.path(code_dir, c("config.R", "common.R",
                                 file.path("methods", list.files(file.path(code_dir, "methods"), pattern = "\\.R$"))))
  hits <- unlist(lapply(files, function(f) {
    s <- readLines(f); i <- grep("truth|\\$active|\\$signal|truth/", s); if (length(i)) paste0(f, ":", i) }))
  if (length(hits)) stop("hits: ", paste(hits, collapse = ", "))
  basename(files)
})
record("10b no-oracle + reruns: runner end to end on an inputs-only tree with no truth/ directory; skip / refuse / refit", {
  tmp <- file.path(tempdir(), "f1_no_oracle"); unlink(tmp, recursive = TRUE)
  dir.create(file.path(tmp, "inputs", "p0500"), recursive = TRUE)
  src <- file.path(inputs_root, "p0500", "dev_p0500_S4_r001.rds")
  file.copy(src, file.path(tmp, "inputs", "p0500"))
  stopifnot(!dir.exists(file.path(tmp, "truth")))
  cmd <- c("--vanilla", file.path(code_dir, "run_case.R"), "--code-dir", code_dir,
           "--input", file.path(tmp, "inputs", "p0500", basename(src)), "--scale", "c100",
           "--out-root", file.path(tmp, "out"), "--run-id", "unit_no_oracle", "--lib", Sys.getenv("BENCH_LIB"))
  rc <- system2(file.path(R.home("bin"), "Rscript"), cmd, stdout = TRUE, stderr = TRUE)
  status <- attr(rc, "status"); if (!is.null(status) && status != 0) stop(paste(rc, collapse = "\n"))
  od <- file.path(tmp, "out", "results", "unit_no_oracle", "p0500", "dev_p0500_S4_r001_c100")
  stopifnot(all(file.exists(file.path(od, paste0("F1", c(".rds", ".csv", ".sha256", ".done"))))))
  csv <- read.csv(file.path(od, "F1.csv"), stringsAsFactors = FALSE, na.strings = "NA",
                  colClasses = c(support = "character", error = "character"))
  stopifnot(nrow(csv) == 4L, all(is.na(csv$tp)), identical(csv$rule_id, settings$METHODS$rule_ids[[1]]))
  # the fit must have succeeded and agree with the in-process fit of the same case (test 5, p = 500)
  obj <- readRDS(file.path(od, "F1.rds"))
  if (any(csv$status == "failed") || nzchar(csv$error[1])) stop("runner fit failed: ", csv$error[1])
  stopifnot(all(csv$converged), nrow(obj$diagnostics$fits) == 11L,
            identical(csv$support, base500$rules$support), identical(obj$beta, base500$beta),
            identical(obj$diagnostics$path$cvm, base500$diagnostics$path$cvm))
  # idempotent rerun: valid outputs are skipped and left byte-identical
  h0 <- tools::md5sum(file.path(od, paste0("F1", c(".rds", ".csv", ".sha256", ".done"))))
  rc2 <- suppressWarnings(system2(file.path(R.home("bin"), "Rscript"), cmd, stdout = TRUE, stderr = TRUE))
  stopifnot(is.null(attr(rc2, "status")) || attr(rc2, "status") == 0, any(grepl("skip: valid outputs exist", rc2)),
            identical(h0, tools::md5sum(names(h0))))
  # a .done whose files no longer verify is an error, and the files are not overwritten
  cat("corrupt\n", file =file.path(od, "F1.csv"), append = TRUE)
  h1 <- tools::md5sum(names(h0))
  rc3 <- suppressWarnings(system2(file.path(R.home("bin"), "Rscript"), cmd, stdout = TRUE, stderr = TRUE))
  stopifnot(!is.null(attr(rc3, "status")) && attr(rc3, "status") != 0, any(grepl("do not verify", rc3)),
            identical(h1, tools::md5sum(names(h0))))
  # without .done the case is refitted (a partial earlier attempt is replaced)
  unlink(file.path(od, c("F1.done", "F1.sha256")))
  rc4 <- suppressWarnings(system2(file.path(R.home("bin"), "Rscript"), cmd, stdout = TRUE, stderr = TRUE))
  stopifnot(is.null(attr(rc4, "status")) || attr(rc4, "status") == 0,
            all(file.exists(names(h0))), !grepl("corrupt", paste(readLines(file.path(od, "F1.csv")), collapse = "")))
  c(rc, rc2)
})

passed <- all(vapply(checks, `[[`, FALSE, "passed"))
saveRDS(list(passed = passed, checks = checks, info = info, host = Sys.info()[["nodename"]], time = Sys.time(),
             glmnet = as.character(packageVersion("glmnet")), lib = .libPaths()),
        file.path(out_dir, "test_F1_lasso.rds"))
cat(sprintf("test_F1_lasso: %d of %d passed\n", sum(vapply(checks, `[[`, FALSE, "passed")), length(checks)))
if (!passed) quit(status = 1L)
