# O-CERT: run the production v3 engine on a regenerated study dataset and keep what the certificates need.
# Usage: Rscript run_fit.R <core_dir> <study_inputs_dir> <out_dir> <dataset_id> <scale_key> [...more id scale pairs]
# Seeds: the study's method seed (inputs$method_seed). Fixed; no other randomness.
a <- commandArgs(TRUE)
core <- a[1]; indir <- a[2]; outdir <- a[3]; jobs <- matrix(a[-(1:3)], ncol = 2, byrow = TRUE)
source(file.path(core, "v3.R"))
for (i in seq_len(nrow(jobs))) {
  id <- jobs[i, 1]; sk <- jobs[i, 2]
  d <- readRDS(file.path(indir, sprintf("p%04d", 500L), paste0(id, ".rds")))
  t0 <- Sys.time()
  fit <- v3_fit(d$X, d$Y[, sk], d$method_seed, allocation = list(mem_gb = 8, hours = 24))
  keep <- fit[intersect(names(fit), c("status", "hpm", "hpm_F", "hpm_provenance", "log_Z", "log_Z_r", "log_Z_lower95",
    "log_m0", "log_Zbar0", "local_certified", "local_limit", "flags", "near_ties", "near_tie_F", "island_best",
    "hpm_before_local", "top_store", "score_counts", "pip_primary", "mpm", "B", "grid"))]
  keep$local_search <- fit$local_search[intersect(names(fit$local_search),
    c("centre", "returned", "returned_F", "local_certified", "local_limit", "moves", "n_evaluated", "termination"))]
  keep$dataset_id <- id; keep$scale_key <- sk; keep$wall <- as.numeric(difftime(Sys.time(), t0, units = "secs"))
  saveRDS(keep, file.path(outdir, sprintf("%s_%s.rds", id, sk)))
  cat(id, sk, fit$status, "hpm_F", fit$hpm_F, "logZ", fit$log_Z, "wall", keep$wall, "\n")
}
