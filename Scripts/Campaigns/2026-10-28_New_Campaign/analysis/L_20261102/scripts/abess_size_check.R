#!/usr/bin/env Rscript
# abess_size_check.R STUDY BENCHROOT OUTCSV [CASEFILE] : HQ D54.3, ABESS (F5) exact size-k check at p <= 30, from the saved fits.
# F5 fits abess on column-centred X (1'X = 0, asserted by fit_F5_abess.R) and centred y (yc), no intercept; for each size k it returns a support
# whose centred RSS ||yc - X b||^2 should be the minimum over all supports of size k. Exact reference: leaps::regsubsets exhaustive
# (Furnival-Wilson branch and bound), intercept = FALSE, on the same X and yc, all sizes 1..p. Alignment check: our OLS RSS of each ABESS
# support must equal the stored path rss_centred. A size is SUBOPTIMAL if rss_abess - rss_best > tol * max(1, rss_best) (tol 1e-8; ties allowed:
# only RSS is compared, not the support). Output: one row per fit (case) with per-size counts and the headline (ebic1_K37) support's status.
# Truth is read only to say whether the exact best subset at the selected size equals S0 (scoring use only).
suppressPackageStartupMessages(library(leaps))
a <- commandArgs(trailingOnly = TRUE); study <- a[1]; broot <- a[2]; out <- a[3]
cases <- if (length(a) >= 4) readLines(a[4]) else NULL
man <- utils::read.csv(file.path(study, "manifests", "inputs_manifest_lowp.csv"), stringsAsFactors = FALSE)
if (is.null(cases)) cases <- as.vector(t(outer(sort(man$dataset_id), c("c100", "c050"), paste, sep = "_")))
tol <- 1e-8
ols_rss <- function(X, y, s) if (!length(s)) sum(y^2) else sum(stats::lm.fit(X[, s, drop = FALSE], y)$residuals^2)
key2s <- function(k) if (is.na(k) || !nzchar(k)) integer(0) else as.integer(strsplit(k, ";")[[1]])
rows <- vector("list", length(cases))
for (i in seq_along(cases)) {
  cid <- cases[i]; ds <- sub("_c[0-9]{3}$", "", cid); sk <- sub(".*_", "", cid); pp <- substr(ds, 1, 5)
  inp <- readRDS(file.path(study, "inputs", pp, paste0(ds, ".rds"))); X <- as.matrix(inp$X); y <- as.numeric(inp$Y[, sk])
  S0 <- sort(as.integer(readRDS(file.path(study, "truth", pp, paste0(ds, ".rds")))$active))
  f <- readRDS(file.path(broot, pp, cid, "F5.rds"))
  path <- f$fit$diagnostics$path; yc <- y - mean(y); p <- ncol(X)
  xc_max <- max(abs(colMeans(X)))
  rs <- summary(regsubsets(x = X, y = yc, intercept = FALSE, nvmax = p, method = "exhaustive", really.big = TRUE))
  best_rss <- c(sum(yc^2), rs$rss); best_sup <- c(list(integer(0)), lapply(seq_len(nrow(rs$which)), function(k) sort(unname(which(rs$which[k, ])))))
  ks <- path$size; sup <- lapply(path$key, key2s)
  my_rss <- vapply(sup, function(s) ols_rss(X, yc, s), 0)
  align_err <- max(abs(my_rss - path$rss_centred) / pmax(1, abs(path$rss_centred)))
  gap <- path$rss_centred - best_rss[ks + 1L]
  subopt <- gap > tol * pmax(1, best_rss[ks + 1L])
  better <- gap < -1e-6 * pmax(1, best_rss[ks + 1L])          # ABESS below the exact minimum would mean a broken reference
  stopifnot(ncol(rs$which) == p)                               # regsubsets columns = X columns 1..p (intercept = FALSE)
  h <- f$fit$coefficients$ebic1_K37; hs <- sort(key2s(h$support)); hk <- length(hs)
  h_gap <- ols_rss(X, yc, hs) - best_rss[hk + 1L]
  h_sub <- h_gap > tol * max(1, best_rss[hk + 1L])
  rows[[i]] <- data.frame(case_id = cid, p = p, scale_key = sk, scenario = as.integer(substr(ds, 8, 8)), xc_max = xc_max, align_err = align_err,
    n_sizes = length(ks), n_sizes_suboptimal = sum(subopt[ks >= 1]), max_rel_gap = max(gap / pmax(1, best_rss[ks + 1L])), n_below_exact = sum(better),
    sizes_suboptimal = paste(ks[subopt], collapse = ";"),
    head_k = hk, head_support = paste(hs, collapse = ";"), head_suboptimal = h_sub, head_rel_gap = h_gap / max(1, best_rss[hk + 1L]),
    head_eq_truth = identical(hs, S0), best_at_head_k = paste(best_sup[[hk + 1L]], collapse = ";"), best_at_head_k_eq_truth = identical(best_sup[[hk + 1L]], S0),
    best_at_s0_size_eq_truth = identical(best_sup[[length(S0) + 1L]], S0), stringsAsFactors = FALSE)
  if (i %% 100 == 0) message(i, "/", length(cases), " ", format(Sys.time(), "%H:%M:%S"))
}
res <- do.call(rbind, rows)
# hard checks (Sol pass-C note iii): finite values, centred X, exact alignment with the stored path, nothing below the exact minimum
stopifnot(all(is.finite(res$align_err)), all(is.finite(res$max_rel_gap)), all(is.finite(res$head_rel_gap)),
          max(res$xc_max) < 1e-10, max(res$align_err) < 1e-8, sum(res$n_below_exact) == 0L)
utils::write.csv(res, out, row.names = FALSE)
cat("cases", nrow(res), "| max align_err", signif(max(res$align_err), 3), "| max |colMeans X|", signif(max(res$xc_max), 3),
    "| (fit,size) suboptimal", sum(res$n_sizes_suboptimal), "of", sum(res$n_sizes - 1L), "| fits with any suboptimal size", sum(res$n_sizes_suboptimal > 0),
    "| headline support suboptimal", sum(res$head_suboptimal), "| below exact (should be 0)", sum(res$n_below_exact), "\n")
