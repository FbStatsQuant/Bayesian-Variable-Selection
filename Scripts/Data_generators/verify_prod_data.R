# Gate G2 checks of the production datasets (master §II.13), one (p, s) cell per call.
# Oracles: tools/scenario_check.out (truth placement, hard-coded below); the Oct-14 sealed components
# (p = 500: X and epsilon must be identical() to /scratch/fb31/BVS_Paired_October_14/production/components);
# regeneration in a fresh process with a per-dataset chol (3 datasets per cell).
# Usage: Rscript verify_prod_data.R <STUDY root> <p> <scenario> <path to gen_prod_data.R>

a <- commandArgs(trailingOnly = TRUE); root <- a[[1]]; p <- as.integer(a[[2]]); s <- as.integer(a[[3]]); gen <- a[[4]]
ok <- TRUE; nfail <- 0L
chk <- function(cond, msg) { if (!isTRUE(cond)) { cat("FAIL", msg, "\n"); ok <<- FALSE; nfail <<- nfail + 1L } }
oracle <- list(`500`  = c(3, 37, 74, 106, 145, 178, 213, 247, 284, 316, 355, 388, 423, 457),
               `1000` = c(3, 67, 134, 196, 265, 328, 393, 457, 524, 586, 655, 718, 783, 847))
beta_or <- c(1.4, -1.0, 1.8, -1.2, 0.8, -1.6, 1.4, -1.0, 1.8, -1.2, 0.8, -1.6, 1.4, -1.0)
OCT14 <- "/scratch/fb31/BVS_Paired_October_14/production/components"
cs <- c(c100 = 1, c075 = .75, c050 = .5, c035 = .35, c025 = .25)
genv <- new.env(); sys.source(gen, envir = genv)
wcor <- numeric(0)
for (r in 1:100) {
  id <- sprintf("p%04d_S%d_r%03d", p, s, r)
  inp <- readRDS(file.path(root, "inputs", sprintf("p%04d", p), paste0(id, ".rds")))
  tr  <- readRDS(file.path(root, "truth",  sprintf("p%04d", p), paste0(id, ".rds")))
  X <- inp$X; n <- nrow(X)
  chk(identical(dim(X), c(200L, p)) && is.null(attr(X, "scaled:center")), paste(id, "dims/attributes"))
  chk(identical(as.numeric(tr$active), oracle[[as.character(p)]]) &&
      identical(tr$beta[tr$active], beta_or) && sum(tr$beta != 0) == 14, paste(id, "truth"))
  chk(max(abs(colMeans(X))) < 1e-10 && max(abs(colSums(X^2) / (n - 1) - 1)) < 1e-10, paste(id, "standardisation"))
  err <- max(sapply(names(cs), function(k) max(abs(inp$Y[, k] - (cs[[k]] * tr$signal + tr$eps)))))
  chk(err <= 1e-12 * max(1, max(abs(inp$Y))), paste(id, "response"))
  chk(identical(sort(unique(inp$foldid)), 1:10) && all(tabulate(inp$foldid, 10) == 20), paste(id, "folds"))
  ds <- c(`500` = 1410000, `1000` = 1510000)[[as.character(p)]] + 10000 * s + r
  fs <- c(`500` = 3410000, `1000` = 3510000)[[as.character(p)]] + 10000 * s + r
  chk(inp$data_seed == ds && inp$fold_seed == fs && inp$method_seed == ds + 4e6, paste(id, "seeds"))
  if (p == 500L) {   # §II.13 item 4(b): bit-identical to the sealed Oct-14 draws
    old <- readRDS(file.path(dirname(OCT14), sprintf("S%d_r%03d.rds", s, r)))   # Oct-14 base input (X, y, truth)
    comp <- readRDS(file.path(OCT14, sprintf("S%d_r%03d.rds", s, r)))           # Oct-14 components
    oldX <- old$X; attributes(oldX) <- list(dim = dim(oldX))
    chk(old$seed_data == ds, paste(id, "Oct-14 seed equals data seed"))
    chk(identical(X, oldX), paste(id, "X identical to Oct-14"))
    # Oct-14 built y = drop(X %*% beta_old) + epsilon; the same expression with the new noise must give its y exactly
    chk(identical(drop(X %*% old$truth$beta) + tr$eps, old$y), paste(id, "noise reproduces Oct-14 y bit-identically"))
    chk(max(abs(tr$eps - comp$epsilon)) <= 1e-12, paste(id, "noise matches Oct-14 epsilon (1e-12)"))
  }
  if (s %in% 3:6 && r <= 100) { R <- cor(X[, 1:50]); g <- ceiling(1:50 / 5); W <- outer(g, g, "==") & row(R) != col(R); wcor <- c(wcor, mean(R[W])) }
}
for (r in c(1L, 50L, 100L)) {   # regeneration with a per-dataset chol, different process
  d <- genv$generate_prod_dataset(p, s, r)
  old <- readRDS(file.path(root, "inputs", sprintf("p%04d", p), sprintf("p%04d_S%d_r%03d.rds", p, s, r)))
  chk(identical(d$inputs$X, old$X) && identical(d$inputs$Y, old$Y) && identical(d$inputs$foldid, old$foldid),
      sprintf("regeneration r%03d", r))
}
if (length(wcor)) cat(sprintf("INFO p=%d S%d mean within-block r (first 10 blocks, 100 reps) = %.3f\n", p, s, mean(wcor)))
cat(sprintf("p=%d S%d: %s (%d failures)\n", p, s, if (ok) "ALL CHECKS PASSED" else "CHECKS FAILED", nfail))
quit(status = if (ok) 0 else 1)
