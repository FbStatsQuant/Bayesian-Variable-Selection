# Sealed HELD-OUT datasets (same design as production, new seed range), for the final comparison of the
# person's own algorithm against the baselines. Never used for tuning. 1,200 datasets: p in {500, 1000} x
# S1-S6 x replicates 1-100. Reuses gen_prod_data.R (verified) with different seed bases and ids:
#   data seed = 7,610,000 (p 500) / 7,710,000 (p 1000) + 10000*s + r
#   fold seed = 8,610,000 / 8,710,000 + 10000*s + r;  method seed = data seed + 4,000,000
#   dataset_id = "hold_p{pppp}_S{s}_r{rrr}", kind = "holdout"
# Usage: Rscript gen_holdout_data.R <HOLDOUT root> <p> <scenario> <path to gen_prod_data.R>

a <- commandArgs(trailingOnly = TRUE); stopifnot(length(a) == 4L)
root <- a[[1]]; p <- as.integer(a[[2]]); s <- as.integer(a[[3]]); gen <- a[[4]]
h <- new.env(); sys.source(gen, envir = h)            # defines generate_prod_dataset() and its globals in h
h$DATA_BASE <- c(`500` = 7610000L, `1000` = 7710000L)
h$FOLD_BASE <- c(`500` = 8610000L, `1000` = 8710000L)
stopifnot(requireNamespace("digest", quietly = TRUE))
di <- file.path(root, "inputs", sprintf("p%04d", p)); dt <- file.path(root, "truth", sprintf("p%04d", p))
dm <- file.path(root, "manifests", "cells"); for (d in c(di, dt, dm)) dir.create(d, recursive = TRUE, showWarnings = FALSE)
L <- chol(h$scenario_covariance(s, p))
rows_in <- list(); rows_tr <- list()
for (r in 1:100) {
  d <- h$generate_prod_dataset(p, s, r, L)
  id <- sprintf("hold_p%04d_S%d_r%03d", p, s, r)
  d$inputs$dataset_id <- id; d$inputs$kind <- "holdout"; d$truth$dataset_id <- id
  stopifnot(d$inputs$data_seed == h$DATA_BASE[[as.character(p)]] + 10000L * s + r)
  fi <- file.path(di, paste0(id, ".rds")); ft <- file.path(dt, paste0(id, ".rds"))
  if (file.exists(fi) || file.exists(ft)) stop("refusing to overwrite ", fi)
  saveRDS(d$inputs, fi, compress = FALSE); saveRDS(d$truth, ft, compress = FALSE); Sys.chmod(c(fi, ft), "0444")
  rows_in[[r]] <- data.frame(dataset_id = id, p = p, scenario = s, replicate = r,
    data_seed = d$inputs$data_seed, fold_seed = d$inputs$fold_seed, method_seed = d$inputs$method_seed,
    file_sha256 = digest::digest(file = fi, algo = "sha256"), x_sha256 = h$f64_sha256(d$inputs$X),
    foldid_sha256 = h$f64_sha256(d$inputs$foldid), y_c100_sha256 = h$f64_sha256(d$inputs$Y[, "c100"]))
  rows_tr[[r]] <- data.frame(dataset_id = id, file_sha256 = digest::digest(file = ft, algo = "sha256"),
    eps_sha256 = h$f64_sha256(d$truth$eps), active = paste(d$truth$active, collapse = ";"))
}
write.csv(do.call(rbind, rows_in), file.path(dm, sprintf("p%04d_S%d_inputs.csv", p, s)), row.names = FALSE)
write.csv(do.call(rbind, rows_tr), file.path(dm, sprintf("p%04d_S%d_truth.csv", p, s)), row.names = FALSE)

# Checks (G2 items 1-3, 5 adapted): truth, standardisation, response, folds; regeneration of r = 1, 50, 100;
# no X shared with the production datasets of the same cell.
cs <- c(c100 = 1, c075 = .75, c050 = .5, c035 = .35, c025 = .25); nfail <- 0L
for (r in 1:100) {
  id <- sprintf("hold_p%04d_S%d_r%03d", p, s, r)
  inp <- readRDS(file.path(di, paste0(id, ".rds"))); tr <- readRDS(file.path(dt, paste0(id, ".rds"))); X <- inp$X
  ok <- identical(tr$active, h$truth(p)$active) &&
    max(abs(colMeans(X))) < 1e-10 && max(abs(colSums(X^2) / 199 - 1)) < 1e-10 &&
    max(sapply(names(cs), function(k) max(abs(inp$Y[, k] - (cs[[k]] * tr$signal + tr$eps))))) <= 1e-12 * max(1, max(abs(inp$Y))) &&
    identical(sort(unique(inp$foldid)), 1:10) && all(tabulate(inp$foldid, 10) == 20)
  if (!ok) { nfail <- nfail + 1L; cat("FAIL", id, "\n") }
}
for (r in c(1L, 50L, 100L)) {
  d <- h$generate_prod_dataset(p, s, r)          # fresh chol
  old <- readRDS(file.path(di, sprintf("hold_p%04d_S%d_r%03d.rds", p, s, r)))
  if (!identical(d$inputs$X, old$X) || !identical(d$inputs$Y, old$Y)) { nfail <- nfail + 1L; cat("FAIL regeneration", r, "\n") }
}
prod_hash <- read.csv(file.path(dirname(root), "manifests", "inputs_manifest.csv"))$x_sha256
if (any(vapply(rows_in, function(z) z$x_sha256, "") %in% prod_hash)) { nfail <- nfail + 1L; cat("FAIL X shared with production\n") }
cat(sprintf("holdout p=%d S%d: %s (%d failures)\n", p, s, if (nfail == 0L) "ALL CHECKS PASSED" else "CHECKS FAILED", nfail))
quit(status = if (nfail == 0L) 0 else 1)
