#!/usr/bin/env Rscript
# diag_accuracy.R -- diagnostic (not a G3 test): explains the generic-backend and
# no-intercept tolerance failures of unit-test job 2275403. For each path point it compares
# our mapped fast-backend solution, the generic family = gaussian() solution and a certified
# optimum from the active-set normal equations
#   (X_A'X_A/n + λ(1-α) I) β_A = X_A'y/n - λ α sign(β_A),
# which is the exact minimiser when its signs agree and the inactive KKT holds.
# Usage: Rscript tests/diag_accuracy.R <code_dir> <dev_inputs_root> <out_dir>
args <- commandArgs(TRUE)
code_dir <- normalizePath(args[1]); inputs_root <- normalizePath(args[2]); out_dir <- args[3]
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
cfg <- new.env(parent = baseenv()); sys.source(file.path(code_dir, "config.R"), envir = cfg)
S <- cfg$make_settings(); .libPaths(c(S$COMMON$study_lib, .Library))
E <- new.env(parent = asNamespace("stats"))
for (f in c("common.R", "methods/glmnet_helpers.R")) sys.source(file.path(code_dir, f), envir = E)
G <- S$GLMNET; n <- 200L
d <- readRDS(file.path(inputs_root, "p0500", "dev_p0500_S4_r001.rds")); X <- d$X; p <- ncol(X)
y <- unname(d$Y[, "c100"])

objective <- function(b, yv, lam, a) sum((yv - X %*% b)^2) / (2 * n) + lam * (a * sum(abs(b)) + (1 - a) * sum(b^2) / 2)
certify <- function(b, yv, lam, a) {
  A <- which(b != 0); cert <- numeric(p)
  if (length(A)) {
    XA <- X[, A, drop = FALSE]
    cert[A] <- solve(crossprod(XA) / n + diag(lam * (1 - a), length(A)),
                     crossprod(XA, yv) / n - lam * a * sign(b[A]))
  }
  ok_sign <- all(sign(cert[A]) == sign(b[A]))
  kkt <- E$kkt_glmnet(X, yv, matrix(cert), lam, a, rep(1, p), max(1, max(abs(crossprod(X, yv))) / n))
  list(b = cert, ok = ok_sign && kkt <= 1e-12, kkt = kkt)
}
compare <- function(label, yv, a, lam, Bours, Bother, other_name) {
  scale <- max(1, max(abs(crossprod(X, yv))) / n)
  ko <- E$kkt_glmnet(X, yv, Bours, lam, a, rep(1, p), scale)
  kg <- E$kkt_glmnet(X, yv, Bother, lam, a, rep(1, p), scale)
  do.call(rbind, lapply(seq_along(lam), function(i) {
    ce <- certify(Bours[, i], yv, lam[i], a)
    fo <- objective(Bours[, i], yv, lam[i], a); fg <- objective(Bother[, i], yv, lam[i], a)
    fc <- if (ce$ok) objective(ce$b, yv, lam[i], a) else NA_real_   # no gap without a certificate
    data.frame(case = label, alpha = a, i = i, lambda = lam[i], ridge_curv = lam[i] * (1 - a),
               k_ours = sum(Bours[, i] != 0), k_other = sum(Bother[, i] != 0),
               diff_ours_other = max(abs(Bours[, i] - Bother[, i])),
               cert_ok = ce$ok, cert_kkt = ce$kkt,
               diff_ours_cert = if (ce$ok) max(abs(Bours[, i] - ce$b)) else NA_real_,
               diff_other_cert = if (ce$ok) max(abs(Bother[, i] - ce$b)) else NA_real_,
               kkt_ours = ko[i], kkt_other = kg[i],
               objgap_ours = fo - fc, objgap_other = fg - fc, other = other_name)
  }))
}

zmax <- max(abs(crossprod(X, y))) / n; frac <- E$lambda_fraction(S$GRID)
idx <- unique(round(seq(1, S$GRID$nlambda, length.out = 20)))
out <- list()
for (a in c(.1, .9)) {
  lam <- (S$GRID$max_mult * zmax / a * frac)[idx]
  ours <- E$glmnet_target_path(X, y, a, lam, rep(1, p), G)
  gen <- glmnet::glmnet(X, y, family = gaussian(), alpha = a, lambda = lam, intercept = FALSE,
                        standardize = FALSE, control = list(thresh = G$thresh, maxit = G$maxit))
  out[[length(out) + 1]] <- compare("generic", y, a, lam, ours$B, as.matrix(gen$beta), "generic")
  cat("generic alpha", a, "npasses ours", ours$npasses, "generic", gen$npasses, "\n")
}
yc <- y - mean(y); y3 <- yc + 3; zc <- max(abs(crossprod(X, yc))) / n
for (a in S$F2$alphas) {
  lam <- S$GRID$max_mult * zc / a * frac
  P3 <- E$glmnet_target_path(X, y3, a, lam, rep(1, p), G)
  Pc <- E$glmnet_target_path(X, yc, a, lam, rep(1, p), G)
  dd <- apply(abs(P3$B - Pc$B), 2, max)
  worst <- order(dd, decreasing = TRUE)[1:3]
  r <- compare("no_intercept_yc_vs_y3", yc, a, lam[worst], Pc$B[, worst, drop = FALSE], P3$B[, worst, drop = FALSE], "y3")
  r$i <- worst
  out[[length(out) + 1]] <- r
  cat("no-intercept alpha", a, "max diff", max(dd), "at index", worst[1], "npasses yc", Pc$npasses, "y3", P3$npasses,
      "max KKT yc", max(Pc$kkt), "y3", max(P3$kkt), "\n")
}
res <- do.call(rbind, out)
write.csv(res, file.path(out_dir, "diag_accuracy.csv"), row.names = FALSE)
options(width = 250)
num <- sapply(res, is.numeric); print(cbind(res[, c("case", "cert_ok")], signif(res[, num], 3)))
cat(sprintf("
certified reference points: %d of %d; max objective gap (certified only): ours %.3g, other %.3g
",
            sum(res$cert_ok), nrow(res), max(res$objgap_ours, na.rm = TRUE), max(res$objgap_other, na.rm = TRUE)))
