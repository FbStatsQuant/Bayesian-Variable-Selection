# run_fit.R -- one v3_fit on a small study-design dataset (S1-S6 covariance and truth pattern of the study generator,
# at the generator's p = 30 truth: s0 = 5). Local regression input only (not a study dataset).
# Usage: Rscript run_fit.R <core_dir> <work_dir> <ls0: TRUE|FALSE|NA> <scenario> <replicate> <n> <scale> <out.rds>
#   ls0 = NA: call v3_fit(X, y, seed, allocation) with the old 4-argument signature (old core).
args <- commandArgs(TRUE)
stopifnot(length(args) == 8)
core <- args[1]; work <- args[2]; ls0 <- as.logical(args[3]); scen <- as.integer(args[4]); rep <- as.integer(args[5])
n <- as.integer(args[6]); scale <- as.numeric(args[7]); out <- args[8]
here <- dirname(normalizePath(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE))))
source(file.path(here, "ceng_load.R"))
ceng_load(core, work, exports = FALSE, reuse = TRUE)

# verbatim from Scripts/SMC_BVS/smoke/reference/gen_dev_data.R (scenario_covariance, truth at p = 30)
scenario_covariance <- function(scenario, p=500L) {
  group <- ceiling(seq_len(p)/5); H <- outer(group,group,"=="); I <- diag(p)
  switch(as.integer(scenario), I, 0.5^abs(outer(seq_len(p),seq_len(p),"-")), 0.7*H+0.3*I, 0.85*H+0.15*I,
    0.3*matrix(1,p,p)+0.4*H+0.3*I,
    {rho <- 0.4+0.1*((group-1L)%%6L); S <- H*matrix(rho,p,p); diag(S)<-1; S})
}
p <- 30L
s0 <- 5L; step <- 1L; pos <- c(3L, 2L, 4L, 1L, 5L, 3L); pattern <- c(1.4, -1.0, 1.8, -1.2, 0.8, -1.6)
k <- 0:(s0 - 1L); block <- 1L + step * k; active <- 5L * (block - 1L) + pos[(k %% 6L) + 1L]
beta <- numeric(p); beta[active] <- pattern[(k %% 6L) + 1L]
data_seed <- 2300000L + 10000L * scen + rep
RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(data_seed)
X <- scale(matrix(rnorm(n * p), nrow = n) %*% chol(scenario_covariance(scen, p)))
attr(X, "scaled:center") <- NULL; attr(X, "scaled:scale") <- NULL
y <- drop(scale * (X %*% beta) + rnorm(n))
method_seed <- data_seed + 4000000L
t0 <- proc.time()[["elapsed"]]
fit <- if (is.na(ls0)) v3_fit(X, y, method_seed) else v3_fit(X, y, method_seed, ls0 = ls0)
wall <- proc.time()[["elapsed"]] - t0
saveRDS(list(fit = fit, scenario = scen, replicate = rep, n = n, p = p, scale = scale, data_seed = data_seed,
             method_seed = method_seed, active = active, ls0 = ls0, core = normalizePath(core), wall = wall,
             x_sha = digest::digest(X), y_sha = digest::digest(y)), out)
cat(sprintf("S%d r%d n=%d scale=%g ls0=%s status=%s hpm={%s} wall=%.1fs\n", scen, rep, n, scale, args[3], fit$status,
            paste(fit$hpm, collapse = ","), wall))
