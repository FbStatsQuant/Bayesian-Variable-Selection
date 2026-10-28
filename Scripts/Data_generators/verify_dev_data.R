# Checks of the dev datasets written by gen_dev_data.R (master §II.13 items 1-3, 6 adapted to one replicate).
# The truth oracle is tools/scenario_check.out (independent Python), hard-coded below; nothing is re-derived
# from gen_dev_data.R except the regeneration check, which re-runs the generator in a fresh process state.
# Usage: Rscript verify_dev_data.R <dev root> <path to gen_dev_data.R>

args <- commandArgs(trailingOnly = TRUE); root <- args[[1]]; gen <- args[[2]]
ok <- TRUE; chk <- function(cond, msg) { cat(if (isTRUE(cond)) "PASS" else "FAIL", msg, "\n"); if (!isTRUE(cond)) ok <<- FALSE }

oracle <- list(
  `500`  = list(active = c(3, 37, 74, 106, 145, 178, 213, 247, 284, 316, 355, 388, 423, 457),
                rho = c(.4, .5, .6, .7, .8, .9, .4, .5, .6, .7, .8, .9, .4, .5)),
  `1000` = list(active = c(3, 67, 134, 196, 265, 328, 393, 457, 524, 586, 655, 718, 783, 847),
                rho = c(.4, .5, .6, .7, .8, .9, .4, .5, .6, .7, .8, .9, .4, .5)))
beta_or <- c(1.4, -1.0, 1.8, -1.2, 0.8, -1.6, 1.4, -1.0, 1.8, -1.2, 0.8, -1.6, 1.4, -1.0)
mineig_or <- c(1.0000, 0.3333, 0.3000, 0.1500, 0.3000, 0.1000)
pop_r <- list(`3` = 0.7, `4` = 0.85, `5` = 0.7)

source(gen, local = (genv <- new.env()))
for (p in c(500L, 1000L)) {
  for (s in 1:6) {
    id <- sprintf("dev_p%04d_S%d_r001", p, s)
    inp <- readRDS(file.path(root, "inputs", sprintf("p%04d", p), paste0(id, ".rds")))
    tr  <- readRDS(file.path(root, "truth",  sprintf("p%04d", p), paste0(id, ".rds")))
    X <- inp$X; n <- nrow(X)
    chk(identical(dim(X), c(200L, p)) && is.null(attributes(X)$`scaled:center`), paste(id, "dims, attributes stripped"))
    chk(identical(as.numeric(tr$active), oracle[[as.character(p)]]$active), paste(id, "active = scenario_check.out"))
    chk(isTRUE(all.equal(tr$beta[tr$active], beta_or, tolerance = 0)) && sum(tr$beta != 0) == 14, paste(id, "beta"))
    chk(max(abs(colMeans(X))) < 1e-10 && max(abs(colSums(X^2) / (n - 1) - 1)) < 1e-10, paste(id, "standardisation"))
    cs <- c(c100 = 1, c075 = .75, c050 = .5, c035 = .35, c025 = .25)
    err <- max(sapply(names(cs), function(k) max(abs(inp$Y[, k] - (cs[[k]] * tr$signal + tr$eps)))))
    chk(err <= 1e-12 * max(1, max(abs(inp$Y))) && max(abs(tr$signal - drop(X %*% tr$beta))) < 1e-10, paste(id, "response construction"))
    chk(identical(sort(unique(inp$foldid)), 1:10) && all(tabulate(inp$foldid, 10) == 20), paste(id, "folds 10 x 20"))
    chk(inp$data_seed == c(`500` = 2410000, `1000` = 2510000)[[as.character(p)]] + 10000 * s + 1 &&
        inp$method_seed == inp$data_seed + 4e6, paste(id, "seeds"))
    if (s %in% 3:5) {   # average within-block sample correlation of the 5 x 5 blocks (descriptive, §II.13 item 6)
      R <- cor(X); g <- ceiling(seq_len(p) / 5); W <- outer(g, g, "==") & row(R) != col(R)
      cat(sprintf("INFO %s mean within-block r = %.3f (population %.2f)\n", id, mean(R[W]), pop_r[[as.character(s)]]))
    }
    if (p == 500L) {
      ev <- min(eigen(genv$scenario_covariance(s, p), symmetric = TRUE, only.values = TRUE)$values)
      chk(abs(ev - mineig_or[s]) < 1e-4, sprintf("S%d min eigenvalue %.4f", s, ev))
    }
  }
}
# Bit-identical regeneration of three datasets
for (a in list(c(500, 1), c(500, 4), c(1000, 6))) {
  d <- genv$generate_dev_dataset(as.integer(a[1]), as.integer(a[2]), 1L)
  id <- d$inputs$dataset_id
  old <- readRDS(file.path(root, "inputs", sprintf("p%04d", a[1]), paste0(id, ".rds")))
  chk(identical(d$inputs$X, old$X) && identical(d$inputs$Y, old$Y) && identical(d$inputs$foldid, old$foldid), paste(id, "regenerates bit-identically"))
}
cat(if (ok) "ALL CHECKS PASSED\n" else "SOME CHECKS FAILED\n")
quit(status = if (ok) 0 else 1)
