# Checker: injected KKT violations on F1/F2, deployed vs v2 on a small synthetic fixture (own code).
# The F1 adapted legacy suite never completed its six-rule 9f fixture; this independently covers failure semantics of the added code.
suppressPackageStartupMessages(library(glmnet))
glmnet::glmnet.control(fdev = 0, devmax = 1)
CAMP <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign"
V2 <- file.path(CAMP, "code/bench_v2"); DEP <- "C:/Users/felip/Documents/NOTS_BVS/NOTS_home/projects/BVS/Benchmarks"
OUTDIR <- file.path(V2, "review/checker")
zz <- file(file.path(OUTDIR, "check5_inject_out.txt"), open = "wt"); sink(zz, split = TRUE)
res <- data.frame(check = character(), pass = logical(), detail = character(), stringsAsFactors = FALSE)
rec <- function(check, pass, detail = "") { pass <- isTRUE(pass); res[nrow(res) + 1L, ] <<- list(check, pass, detail)
  cat(sprintf("[%s] %-78s %s\n", if (pass) "PASS" else "FAIL", check, detail)) }
key_of <- function(idx) paste(sort(as.integer(idx)), collapse = ";")

load_env <- function(root, method, tweak = NULL) {
  folder <- c(F1 = "F1_Lasso", F2 = "F2_ElasticNet")[[method]]; fitfile <- c(F1 = "fit_F1_lasso.R", F2 = "fit_F2_enet.R")[[method]]
  cfg <- new.env(parent = globalenv()); sys.source(file.path(root, folder, "config.R"), cfg)
  settings <- if (method == "F1") { s <- as.list(cfg); s$variant <- "primary"; s } else cfg$make_settings("primary")
  e <- new.env(parent = globalenv())
  for (f in c("common.R", "methods/glmnet_helpers.R", paste0("methods/", fitfile))) sys.source(file.path(root, folder, f), e)
  e$assert_pkg_version <- function(...) invisible(TRUE)
  e$glmnet_target_path <- function(Xd, yd, alpha, lam, pf, G) {
    s <- sqrt(mean(yd^2)); m <- alpha + s * (1 - alpha)
    fit <- glmnet::glmnet(Xd, yd, family = "gaussian", alpha = alpha / m, lambda = lam * m, penalty.factor = pf, intercept = FALSE,
                          standardize = FALSE, type.gaussian = G$type_gaussian, thresh = G$thresh, maxit = G$maxit)
    e$check_glmnet_path(fit, lam * m, G)
    B <- as.matrix(fit$beta); scale <- max(1, max(abs(crossprod(Xd, yd))) / nrow(Xd))
    k <- e$kkt_glmnet(Xd, yd, B, lam, alpha, pf, scale)
    if (!is.null(tweak)) k <- tweak(k, Xd, B)
    list(B = B, s = s, m = m, a = alpha / m, jerr = fit$jerr, npasses = fit$npasses, kkt = k)
  }
  list(e = e, settings = settings, fn = get(c(F1 = "fit_F1_lasso", F2 = "fit_F2_enet")[[method]], envir = e))
}
n <- 200L; p <- 60L
set.seed(11); X <- matrix(rnorm(n * p), n, p); X <- scale(X, TRUE, FALSE); X <- sweep(X, 2, sqrt(colSums(X^2) / (n - 1)), "/"); X <- unname(X); attr(X, "scaled:center") <- NULL
set.seed(12); y <- drop(X[, c(3, 7, 14, 16, 25)] %*% c(1.2, -1, 0.9, 1.1, -0.8)) + rnorm(n); foldid <- { set.seed(13); sample(rep(1:10, length.out = n)) }

for (method in c("F1", "F2")) {
  cat("\n=====", method, "=====\n")
  run <- function(root, tweak = NULL) { ev <- load_env(root, method, tweak); ev$fn(X, y, foldid, 1L, ev$settings) }
  old0 <- run(DEP); new0 <- run(V2)
  idx_min <- if (method == "F1") new0$diagnostics$index[["min"]] else new0$diagnostics$chosen$i_min
  idx_1se <- if (method == "F1") new0$diagnostics$index[["one_se"]] else new0$diagnostics$chosen$i_1se
  key_e1 <- new0$rules$support[new0$rules$rule_id == "ebic1"]
  cat("   baseline: i_min =", idx_min, " i_1se =", idx_1se, " ebic1 support =", key_e1, "\n")
  compare <- function(tag, old, new) {
    four <- new$rules[match(old$rules$rule_id, new$rules$rule_id), ]; o <- old$rules; rownames(four) <- NULL; rownames(o) <- NULL
    rec(sprintf("%s %s: deployed vs v2 original 4 rule rows identical (all cols)", method, tag), identical(as.list(o), as.list(four)),
        sprintf("deployed status=%s | v2 status=%s", paste(o$status, collapse = ","), paste(new$rules$status, collapse = ",")))
    rec(sprintf("%s %s: beta / converged / diagnostics identical", method, tag), identical(old$beta, new$beta) && identical(old$converged, new$converged) &&
          identical(old$diagnostics, new$diagnostics))
    r <- new$rules; ok <- TRUE
    for (i in seq_len(nrow(r))) { if (anyNA(new$beta) || is.null(new$coefficients)) { ok <- FALSE; break }
      z <- new$coefficients[[r$rule_id[i]]]; ex <- if (r$status[i] == "failed") r$support_audit[i] else r$support[i]
      ok <- ok && identical(key_of(which(z$beta_pen != 0)), ex) && identical(z$status, r$status[i]) }
    rec(sprintf("%s %s: v2 beta_pen provenance == support / support_audit, all 6 rules", method, tag), ok)
  }
  compare("S0 no injection", old0, new0)
  # S1: violation at the full-data fit, CV-min column only
  t1 <- function(k, Xd, B) { if (nrow(Xd) == n) k[idx_min] <- k[idx_min] + 1; k }
  o1 <- run(DEP, t1); n1 <- run(V2, t1); compare("S1 full-data KKT at i_min", o1, n1)
  rec(sprintf("%s S1: cv_min failed (support NA, audit set), others unaffected unless same column", method), n1$rules$status[1] == "failed" && is.na(n1$rules$support[1]) && !is.na(n1$rules$support_audit[1]),
      paste(n1$rules$status, collapse = ","))
  # S2: violation at every full-data column whose support equals the ebic1 support
  t2 <- function(k, Xd, B) { if (nrow(Xd) == n) { kk <- vapply(seq_len(ncol(B)), function(j) key_of(which(B[, j] != 0)), ""); k[kk == key_e1] <- k[kk == key_e1] + 1 }; k }
  o2 <- run(DEP, t2); n2 <- run(V2, t2); compare("S2 full-data KKT at every ebic1-support column", o2, n2)
  r2 <- n2$rules; hit <- r2$support_audit[r2$rule_id %in% c("ebic1", "ebic05", "ebic1_K37", "ebic05_K37")]
  chosen <- ifelse(r2$status == "failed", r2$support_audit, r2$support)[3:6]
  rec(sprintf("%s S2: every EBIC-type rule that picked the violated support failed; others ok", method),
      all(r2$status[3:6] == ifelse(chosen == key_e1 & nzchar(key_e1), "failed", "ok")), paste(r2$rule_id[3:6], r2$status[3:6], collapse = " "))
  # S3: violation in a training-fold fit at the i_min column (fold 1)
  folds_seen <- 0L
  t3 <- function(k, Xd, B) { if (nrow(Xd) < n) { folds_seen <<- folds_seen + 1L; if (folds_seen %% 1L == 0L) k[idx_min] <- k[idx_min] + 1 }; k }
  folds_seen <- 0L; o3 <- run(DEP, t3); folds_seen <- 0L; n3 <- run(V2, t3); compare("S3 fold-fit KKT at i_min (all folds)", o3, n3)
  rec(sprintf("%s S3: cv_min and cv_1se failed by fold violation; EBIC rules unaffected", method), all(n3$rules$status[1:2] == "failed") && all(n3$rules$status[3:6] == "ok"), paste(n3$rules$status, collapse = ","))
  # K37 rows vs cap rows on baseline when supports coincide (consistency)
  k37 <- new0$rules[new0$rules$rule_id %in% c("ebic1_K37", "ebic05_K37"), ]
  rec(sprintf("%s baseline: K37 rows roles S0, k <= 37, ok", method), all(k37$role == "S0") && all(k37$k <= 37L) && all(k37$status == "ok"))
}
cat("\nSUMMARY: ", sum(res$pass), " PASS / ", sum(!res$pass), " FAIL of ", nrow(res), "\n")
write.csv(res, file.path(OUTDIR, "check5_inject_results.csv"), row.names = FALSE)
sink(); close(zz)
