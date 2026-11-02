# Checker: run the v2 F3 wrapper (read-only, sourced) on constructed inputs for the branches the dev data never reach
# (m = 0, m = 1), pilot failure, second-stage KKT failure, weight extremes, permuted columns. Judge against OWN code.
suppressPackageStartupMessages(library(glmnet))
glmnet::glmnet.control(fdev = 0, devmax = 1)
CAMP <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign"
ROOT <- file.path(CAMP, "code/bench_v2/F3_AdaptiveLasso")
OUTDIR <- file.path(CAMP, "code/bench_v2/review/checker")
zz <- file(file.path(OUTDIR, "check2_edges_out.txt"), open = "wt"); sink(zz, split = TRUE)
res <- data.frame(check = character(), pass = logical(), detail = character(), stringsAsFactors = FALSE)
rec <- function(check, pass, detail = "") { pass <- isTRUE(pass); res[nrow(res) + 1L, ] <<- list(check, pass, detail)
  cat(sprintf("[%s] %-70s %s\n", if (pass) "PASS" else "FAIL", check, detail)) }
key_of <- function(idx) paste(sort(as.integer(idx)), collapse = ";")
parse_k <- function(key) if (is.na(key)) NA_integer_ else if (!nzchar(key)) integer() else as.integer(strsplit(key, ";", fixed = TRUE)[[1]])

make_env <- function(kkt_tweak = NULL, engine_error = FALSE) {
  cfg <- new.env(parent = globalenv()); sys.source(file.path(ROOT, "config.R"), cfg)
  settings <- cfg$study_settings("primary")
  e <- new.env(parent = globalenv())
  for (f in c("common.R", "methods/glmnet_helpers.R", "methods/fit_F3_alasso.R")) sys.source(file.path(ROOT, f), e)
  e$assert_pkg_version <- function(...) invisible(TRUE)          # local glmnet 4.1-10 (documented test-only override)
  e$glmnet_target_path <- function(Xd, yd, alpha, lam, pf, G) {
    if (engine_error) stop("injected engine failure")
    s <- sqrt(mean(yd^2)); m <- alpha + s * (1 - alpha)
    fit <- glmnet::glmnet(Xd, yd, family = "gaussian", alpha = alpha / m, lambda = lam * m, penalty.factor = pf, intercept = FALSE,
                          standardize = FALSE, type.gaussian = G$type_gaussian, thresh = G$thresh, maxit = G$maxit)
    e$check_glmnet_path(fit, lam * m, G)
    B <- as.matrix(fit$beta); scale <- max(1, max(abs(crossprod(Xd, yd))) / nrow(Xd))
    list(B = B, s = s, m = m, a = alpha / m, jerr = fit$jerr, npasses = fit$npasses, kkt = e$kkt_glmnet(Xd, yd, B, lam, alpha, pf, scale))
  }
  if (!is.null(kkt_tweak)) { orig <- e$kkt_glmnet; e$kkt_glmnet <- function(Xd, yd, B, lam, alpha, pf, scale) kkt_tweak(orig(Xd, yd, B, lam, alpha, pf, scale), pf) }
  list(e = e, settings = settings)
}
std_design <- function(n, p, seed) { set.seed(seed); X <- matrix(rnorm(n * p), n, p); X <- scale(X, TRUE, FALSE); X <- sweep(X, 2, sqrt(colSums(X^2) / (n - 1)), "/"); attr(X, "scaled:center") <- NULL; X <- unname(X); X }
mk_fold <- function(n, seed) { set.seed(seed); sample(rep(1:10, length.out = n)) }
run_fit <- function(env, X, y, foldid) env$e$fit_F3_alasso(X, y, foldid, 1L, env$settings)

env <- make_env(); n <- 200L; p <- 30L

## ---------- find an m = 0 and an m = 1 case ----------
found0 <- found1 <- NULL
for (s in 1:400) {
  if (is.null(found0)) { X <- std_design(n, p, 1000 + s); set.seed(5000 + s); y <- rnorm(n)
    f <- run_fit(env, X, y, mk_fold(n, s)); if (identical(unique(f$rules$pilot_k), 0L)) found0 <- list(X = X, y = y, foldid = mk_fold(n, s), f = f, seed = s) }
  if (is.null(found1)) { X <- std_design(n, p, 2000 + s); set.seed(6000 + s); y <- 0.3 * X[, 1] + rnorm(n)
    f <- run_fit(env, X, y, mk_fold(n, 7000 + s)); if (identical(unique(f$rules$pilot_k), 1L)) found1 <- list(X = X, y = y, foldid = mk_fold(n, 7000 + s), f = f, seed = s) }
  if (!is.null(found0) && !is.null(found1)) break
}
cat("search: m0 seed =", if (is.null(found0)) NA else found0$seed, " m1 seed =", if (is.null(found1)) NA else found1$seed, "\n")
rec("found a genuine m = 0 fixture (pure noise, p = 30)", !is.null(found0))
rec("found a genuine m = 1 fixture (p = 30)", !is.null(found1))

## ---------- m = 0 ----------
if (!is.null(found0)) {
  f <- found0$f; X <- found0$X; y <- found0$y; r <- f$rules
  rec("m0: all 6 rows status ok, support '', k 0", all(r$status == "ok") && all(r$support == "") && all(r$k == 0L), paste(r$status, collapse = ","))
  rec("m0: diag_codes == pilot_null on every row", all(r$diag_codes == "pilot_null"), paste(unique(r$diag_codes), collapse = "|"))
  rec("m0: rss == sum(y^2) on every row", all(abs(r$rss - sum(y^2)) <= 1e-12 * sum(y^2)), sprintf("%.6f", unique(r$rss)))
  rec("m0: lambda/index/cv_mean/cv_se NA", all(is.na(r$lambda)) && all(is.na(r$index)) && all(is.na(r$cv_mean)) && all(is.na(r$cv_se)))
  rec("m0: pilot_k 0, pilot_index/lambda finite", all(r$pilot_k == 0L) && all(is.finite(r$pilot_index)) && all(is.finite(r$pilot_lambda)))
  co <- f$coefficients
  rec("m0: beta_pen zero p-vectors, ebic beta_ols zero, cv beta_ols NA",
      all(vapply(co, function(z) length(z$beta_pen) == p && all(z$beta_pen == 0), TRUE)) &&
        all(vapply(co[c("ebic1", "ebic05", "ebic1_K37", "ebic05_K37")], function(z) all(z$beta_ols == 0), TRUE)) && all(vapply(co[c("cv_min", "cv_1se")], function(z) all(is.na(z$beta_ols)), TRUE)))
  cd <- f$diagnostics$candidates
  rec("m0: candidate table = null model only; path = one null row", nrow(cd) == 1L && cd$key == "" && cd$k == 0L && nrow(f$diagnostics$path) == 1L && f$diagnostics$path$key == "")
  n0 <- n * log(sum(y^2) / n); rec("m0: null ebic1 == n log(RSS/n)", abs(cd$ebic1 - n0) < 1e-9 * abs(n0), sprintf("%.6f vs %.6f", cd$ebic1, n0))
  rec("m0: crit_value ebic rows = null EBIC, CV rows NA", all(abs(r$crit_value[3:6] - n0) < 1e-9 * abs(n0)) && all(is.na(r$crit_value[1:2])))
  rec("m0: converged TRUE; fit$beta zeros", isTRUE(f$converged) && all(f$beta == 0))
}

## ---------- m = 1 ----------
if (!is.null(found1)) {
  f <- found1$f; X <- found1$X; y <- found1$y; foldid <- found1$foldid; r <- f$rules; p1 <- ncol(X)
  j <- which(f$diagnostics$pilot$beta != 0)
  rec("m1: status ok on all 6 rows; pilot_single on every row", all(r$status == "ok") && all(grepl("pilot_single", r$diag_codes)), paste(unique(r$diag_codes), collapse = "|"))
  rec("m1: keep == the single pilot nonzero; v == 1", identical(as.integer(f$diagnostics$keep), j) && isTRUE(all.equal(f$diagnostics$v, 1, tolerance = 1e-14)), sprintf("j=%d", j))
  x <- X[, j]; lam <- 1.01 * (abs(sum(x * y)) / n) * exp(seq(0, log(1e-4), length.out = 200L))
  rec("m1: lambda grid == own (rel 1e-12)", max(abs(lam - f$diagnostics$path$lambda) / lam) < 1e-12)
  S <- function(z, t) sign(z) * pmax(abs(z) - t, 0)
  path1 <- function(xx, yy) S(sum(xx * yy) / length(yy), lam) / (sum(xx * xx) / length(yy))
  bfull <- path1(x, y); oof <- matrix(NA_real_, n, 200)
  for (k in 1:10) { te <- foldid == k; bk <- path1(x[!te], y[!te]); oof[te, ] <- outer(x[te], bk) }
  nk <- tabulate(foldid, 10); mse <- t(vapply(1:10, function(k) colMeans((y[foldid == k] - oof[foldid == k, , drop = FALSE])^2), numeric(200)))
  cvm <- drop(nk %*% mse) / n; cvsd <- sqrt(drop(nk %*% sweep(mse, 2, cvm)^2) / n / 9)
  rec("m1: own scalar CV cvm/cvsd == saved path (rel 1e-12)", max(abs(cvm - f$diagnostics$path$cvm) / cvm) < 1e-12 && max(abs(cvsd - f$diagnostics$path$cvsd) / cvsd) < 1e-10,
      sprintf("rel cvm %.1e cvsd %.1e", max(abs(cvm - f$diagnostics$path$cvm) / cvm), max(abs(cvsd - f$diagnostics$path$cvsd) / cvsd)))
  imin <- min(which(cvm <= min(cvm))); i1 <- min(which(cvm <= cvm[imin] + cvsd[imin]))
  rec("m1: cv_min and cv_1se indices == own scalar solution", r$index[1] == imin && r$index[2] == i1, sprintf("own %d/%d saved %d/%d", imin, i1, r$index[1], r$index[2]))
  rec("m1: cv supports/beta_pen at those indices == own", identical(r$support[1], if (bfull[imin] != 0) as.character(j) else "") && identical(r$support[2], if (bfull[i1] != 0) as.character(j) else "") &&
        isTRUE(all.equal(f$coefficients$cv_min$beta_pen[j], bfull[imin], tolerance = 1e-14)) && isTRUE(all.equal(f$coefficients$cv_1se$beta_pen[j], bfull[i1], tolerance = 1e-14)),
      sprintf("beta_min=%.6f beta_1se=%.6f", bfull[imin], bfull[i1]))
  # EBIC with p = ncol(X)
  keys <- c("", as.character(j)); rss <- c(sum(y^2), sum(lm.fit(cbind(x), y)$residuals^2)); ks <- c(0L, 1L)
  e1 <- n * log(rss / n) + ks * log(n) + 2 * 1 * lchoose(p1, ks); e05 <- n * log(rss / n) + ks * log(n) + 2 * 0.5 * lchoose(p1, ks)
  pick1 <- keys[order(e1, ks, keys, method = "radix")[1]]; pick05 <- keys[order(e05, ks, keys, method = "radix")[1]]
  rec("m1: ebic1/ebic05 (+K37) picks == own (full p)", identical(r$support[3], pick1) && identical(r$support[5], pick1) && identical(r$support[4], pick05) && identical(r$support[6], pick05), sprintf("own '%s','%s'", pick1, pick05))
  rec("m1: path supports == own (sign(bfull))", identical(f$diagnostics$path$key, ifelse(bfull != 0, as.character(j), "")))
}

## ---------- pilot failure propagates ----------
X <- std_design(n, p, 4242); set.seed(4243); y <- X[, 1] * 1 + X[, 2] * 0.8 + rnorm(n); foldid <- mk_fold(n, 4244)
base <- run_fit(env, X, y, foldid)
rec("baseline fixture fits ok (m >= 2)", all(base$rules$status == "ok") && base$rules$pilot_k[1] >= 2, sprintf("pilot_k=%d", base$rules$pilot_k[1]))
envP <- make_env(); envP$settings$GLMNET$kkt_rel_tol <- 0           # pilot KKT cannot pass at the selected point
fP <- run_fit(envP, X, y, foldid)
rec("pilot KKT failure -> whole fit failed (6 rows failed, support NA, never null)", all(fP$rules$status == "failed") && all(is.na(fP$rules$support)) && !isTRUE(fP$converged) && all(is.na(fP$beta)),
    paste(unique(fP$rules$error), collapse = "|"))
rec("pilot failure: coefficients all-NA vectors with failed status", all(vapply(fP$coefficients, function(z) all(is.na(z$beta_pen)) && all(is.na(z$beta_ols)) && z$status == "failed", TRUE)))
envE <- make_env(engine_error = TRUE); fE <- run_fit(envE, X, y, foldid)
rec("engine error in pilot -> whole fit failed", all(fE$rules$status == "failed") && all(is.na(fE$rules$support)), paste(unique(fE$rules$error), collapse = "|"))

## ---------- second-stage KKT failure fails the rule, keeps audit provenance ----------
envK <- make_env(kkt_tweak = function(k, pf) if (any(pf != 1)) k + 1 else k)
fK <- run_fit(envK, X, y, foldid); rK <- fK$rules
rec("2nd-stage KKT failure: CV rules failed, support NA, support_audit set", all(rK$status[1:2] == "failed") && all(is.na(rK$support[1:2])) && all(!is.na(rK$support_audit[1:2])), paste(rK$status, collapse = ","))
okprov <- vapply(seq_len(6), function(i) { z <- fK$coefficients[[i]]; ex <- if (rK$status[i] == "failed") rK$support_audit[i] else rK$support[i]; identical(key_of(which(z$beta_pen != 0)), ex) }, TRUE)
rec("2nd-stage KKT failure: beta_pen provenance == support_audit for failed rules", all(okprov))
rec("2nd-stage KKT failure: EBIC rules fail iff chosen support non-null", all(rK$status[3:6] == ifelse(rK$support_audit[3:6] == "" | (is.na(rK$support_audit[3:6]) & rK$support[3:6] == ""), "ok", "failed")),
    paste(rK$status[3:6], collapse = ","))

## ---------- weight extremes (call alasso_weights from the sourced file) ----------
aw <- env$e$alasso_weights; F3c <- env$settings$F3
tr <- function(b) tryCatch(aw(b, F3c), error = function(err) conditionMessage(err))
w1 <- tr(c(1e-308, 1e-308)); rec("weights: b=(1e-308,1e-308) handled (no overflow), v=(1,1)", is.list(w1) && isTRUE(all.equal(w1$v, c(1, 1))), if (is.list(w1)) "ok" else w1)
w2 <- tr(c(1e-12, 1, 3)); rec("weights: |b| ~ 1e-12 -> v>0, sum(v)=3", is.list(w2) && all(w2$v > 0) && abs(sum(w2$v) - 3) < 1e-10, if (is.list(w2)) sprintf("v=%s", paste(signif(w2$v, 4), collapse = ",")) else w2)
w3 <- tr(c(1e-320, 1)); rec("weights: b=1e-320 (1/b = Inf) fails cleanly", is.character(w3), if (is.character(w3)) w3 else "NOT FAILED")
w4 <- tr(c(1e-300, 1e300)); rec("weights: underflowed factor (v=0) fails cleanly", is.character(w4), if (is.character(w4)) w4 else "NOT FAILED")
w5 <- tr(c(0.5, 0)); rec("weights: zero coefficient in keep rejected", is.character(w5), if (is.character(w5)) w5 else "NOT FAILED")
w6 <- tr(c(0.5, NA)); rec("weights: non-finite coefficient rejected", is.character(w6), if (is.character(w6)) w6 else "NOT FAILED")
F3g <- F3c; F3g$gamma <- 2; w7 <- tryCatch(aw(c(0.5, 1), F3g), error = function(err) conditionMessage(err)); rec("weights: gamma != 1 rejected", is.character(w7), if (is.character(w7)) w7 else "NOT FAILED")

## ---------- permuted columns: supports map back ----------
perm <- sample.int(p); set.seed(99)
fper <- run_fit(env, X[, perm, drop = FALSE], y, foldid)
mapb <- vapply(seq_len(6), function(i) { a <- parse_k(base$rules$support[i]); b <- parse_k(fper$rules$support[i]); identical(sort(a), sort(perm[b])) }, TRUE)
cat("   permuted-column support match per rule:", paste(base$rules$rule_id, mapb, collapse = "  "), "\n")
rec("permuted columns: all 6 rules' supports map back to original indices", all(mapb))
rec("permuted columns: pilot keep maps back", identical(sort(perm[fper$diagnostics$keep]), sort(base$diagnostics$keep)))

cat("\nSUMMARY: ", sum(res$pass), " PASS / ", sum(!res$pass), " FAIL of ", nrow(res), "\n")
write.csv(res, file.path(OUTDIR, "check2_edges_results.csv"), row.names = FALSE)
sink(); close(zz)
