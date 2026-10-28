# Regression gate. Rscript gate.R <case_id> <data.rds> <reference.rds> <outdir> [cores]
# data.rds has X,y (S1-S5 precheck objects or S6 sealed); reference.rds = Experiment_2 exact reference.
args <- commandArgs(TRUE)
case <- args[1]; data_rds <- args[2]; ref_rds <- args[3]; outdir <- args[4]
cores <- if (length(args) >= 5) as.integer(args[5]) else 60L
here <- normalizePath(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])))
source(file.path(here, "exact_stratified.R")); load_strat_backend(here)
d <- readRDS(data_rds); ref <- readRDS(ref_rds)
X <- d$X; y <- d$y
t0 <- proc.time()[["elapsed"]]
st <- exact_stratified(X, y, cores = cores)
wall <- proc.time()[["elapsed"]] - t0
p <- st$p
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
saveRDS(st[setdiff(names(st), "context")], file.path(outdir, paste0(case, "__strat.rds")))

ap <- apply_size_prior(st, bernoulli_logw(p, 0.2))
chk <- list()
chk$models_evaluated <- st$models_evaluated == 2^30 && all(st$count_k == choose(30, 0:30))
d_logZ <- ap$log_Z - ref$log_Z; d_logZ_cpp <- st$bernoulli$log_Z - ref$log_Z
d_pip <- max(abs(ap$pip - ref$pip)); d_pip_cpp <- max(abs(st$bernoulli$pip - ref$pip))
chk$logZ_1e8 <- abs(d_logZ) < 1e-8
chk$pip_1e9 <- d_pip < 1e-9
chk$mpm_identical <- identical(as.integer(ap$mpm), as.integer(ref$mpm))
chk$hpm_identical <- identical(as.integer(sort(ap$hpm)), as.integer(sort(ref$map_variables)))
d_map <- ap$hpm_log_score - ref$map_log_score
# (3) internal consistency
rel_N <- vapply(1:p, function(k) lse(st$logN_jk[k + 1, ]) - log(k) - st$logZ_k[k + 1], 0)   # sum_j N_jk = k Z_k, in log scale == relative error
chk$sumN_eq_kZ_1e9 <- max(abs(expm1(rel_N))) < 1e-9
pk <- exp(st$logZ_k - lse(st$logZ_k)); chk$uniform_prob_sum <- abs(sum(pk) - 1) < 1e-12
Ek <- sum((0:p) * ap$size_posterior); chk$sum_pip_eq_Esize <- abs(sum(ap$pip) - Ek) < 1e-9
chk$bern_cpp_vs_apply <- abs(st$bernoulli$log_Z - ap$log_Z) < 1e-8 && d_pip_cpp < 1e-9
# independent check of stored top models with R's log_marginal_likelihood (first and last of each list)
ctx <- st$context; dm <- 0
for (k in 0:p) { tt <- st$top_by_size[[k + 1]]
  for (i in unique(c(1, length(tt$code)))) { if (!length(tt$code)) next
    a <- .strat$model_members(as.integer(tt$code[i]), p); stopifnot(length(a) == k)
    dm <- max(dm, abs(.strat$log_marginal_likelihood(a, ctx) - tt$log_m[i])) } }
chk$top_models_vs_R_1e8 <- dm < 1e-8
chk$top_sorted <- all(vapply(st$top_by_size, function(t) !is.unsorted(rev(t$log_m)), TRUE))
chk$top_len20 <- all(vapply(st$top_by_size, function(t) length(t$code) == min(20, choose(30, t$size)), TRUE))
cat("\n==== GATE", case, "====\n")
cat(sprintf("data %s\nref  %s\n", data_rds, ref_rds))
cat(sprintf("models_evaluated %.0f; cores %d; chunks %d; wall %.1f s (enumeration+merge)\n", st$models_evaluated, cores, st$chunks, wall))
cat(sprintf("logZ(apply_size_prior Bern .2) - ref = %+.3e ; (in-C++ Bernoulli) - ref = %+.3e\n", d_logZ, d_logZ_cpp))
cat(sprintf("max|PIP(apply) - ref| = %.3e ; max|PIP(in-C++) - ref| = %.3e\n", d_pip, d_pip_cpp))
cat(sprintf("MPM stratified {%s} ref {%s}\n", paste(ap$mpm, collapse = ","), paste(ref$mpm, collapse = ",")))
cat(sprintf("HPM stratified {%s} (size %d) ref MAP {%s}; log score diff %+.3e\n", paste(sort(ap$hpm), collapse = ","), ap$hpm_size, paste(ref$map_variables, collapse = ","), d_map))
cat(sprintf("max |sum_j N_jk / (k Z_k) - 1| = %.3e ; max|top model logm - R logm| = %.3e\n", max(abs(expm1(rel_N))), dm))
cat(sprintf("sum_j PIP = %.12f, E|S| from size posterior = %.12f\n", sum(ap$pip), Ek))
cat("size posterior (Bern .2), k=0..30 nonneg mass >1e-6:", paste(sprintf("%d:%.4f", which(ap$size_posterior > 1e-6) - 1L, ap$size_posterior[ap$size_posterior > 1e-6]), collapse = " "), "\n")
print(unlist(chk))
cat("GATE_PASS:", all(unlist(chk)), "\n")
cat("sessionInfo R", as.character(getRversion()), " Rcpp", as.character(packageVersion("Rcpp")), "host", Sys.info()[["nodename"]], "\n")
