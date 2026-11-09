# run_batch.R -- v3_fit on small study-design datasets (S1-S6 covariance and truth pattern of the study generator, at
# the generator's p = 30 truth: s0 = 5), all in ONE R process (one compiled core). Local regression inputs only.
# Usage: Rscript run_batch.R <core_dir> <work_dir> <mode: old|off|on|proto> <out_dir> [n] [replicates] [scales] [scenarios]
#   old   : old core, v3_fit(X, y, seed) (4-argument signature)
#   off/on: new core, v3_fit(..., ls0 = FALSE/TRUE)
#   proto : old core + O-LS0 prototype export cpp_final_run_ls0 (ls0_enable_integrated; see proto_load.R)
args <- commandArgs(TRUE)
core <- args[1]; work <- args[2]; mode <- args[3]; outdir <- args[4]
n <- if (length(args) >= 5) as.integer(args[5]) else 100L
reps <- if (length(args) >= 6) eval(parse(text = args[6])) else 1:4
scales <- if (length(args) >= 7) eval(parse(text = args[7])) else c(1, 0.5)
scens <- if (length(args) >= 8) eval(parse(text = args[8])) else 1:6
here <- dirname(normalizePath(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE))))
source(file.path(here, "ceng_load.R"))
if (mode == "proto") { source(file.path(here, "proto_load.R")); proto_load(core, work) } else ceng_load(core, work, exports = FALSE)
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)

# verbatim from Scripts/SMC_BVS/smoke/reference/gen_dev_data.R (scenario_covariance; truth() at p = 30)
scenario_covariance <- function(scenario, p=500L) {
  stopifnot(length(scenario)==1L, scenario %in% 1:6, p>=1L, p==as.integer(p))
  group <- ceiling(seq_len(p)/5)
  H <- outer(group,group,"==")
  I <- diag(p)
  switch(as.integer(scenario),
    I,
    0.5^abs(outer(seq_len(p),seq_len(p),"-")),
    0.7*H+0.3*I,
    0.85*H+0.15*I,
    0.3*matrix(1,p,p)+0.4*H+0.3*I,
    {rho <- 0.4+0.1*((group-1L)%%6L); S <- H*matrix(rho,p,p); diag(S)<-1; S})
}
p <- 30L
s0 <- 5L; step <- 1L; pos <- c(3L, 2L, 4L, 1L, 5L, 3L); pattern <- c(1.4, -1.0, 1.8, -1.2, 0.8, -1.6)
k <- 0:(s0 - 1L); block <- 1L + step * k; active <- 5L * (block - 1L) + pos[(k %% 6L) + 1L]
beta <- numeric(p); beta[active] <- pattern[(k %% 6L) + 1L]

one_fit <- function(scen, rep, n, scale) {
  data_seed <- 2300000L + 10000L * scen + rep
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(data_seed)
  X <- scale(matrix(rnorm(n * p), nrow = n) %*% chol(scenario_covariance(scen, p)))
  attr(X, "scaled:center") <- NULL; attr(X, "scaled:scale") <- NULL
  y <- drop(scale * (X %*% beta) + rnorm(n))
  method_seed <- data_seed + 4000000L
  t0 <- proc.time()[["elapsed"]]
  fit <- switch(mode, old = , proto = v3_fit(X, y, method_seed),
                off = v3_fit(X, y, method_seed, ls0 = FALSE), on = v3_fit(X, y, method_seed, ls0 = TRUE))
  wall <- proc.time()[["elapsed"]] - t0
  saveRDS(list(fit = fit, scenario = scen, replicate = rep, n = n, p = p, scale = scale, data_seed = data_seed,
               method_seed = method_seed, active = active, mode = mode, core = normalizePath(core), wall = wall,
               x_sha = digest::digest(X), y_sha = digest::digest(y)),
          file.path(outdir, sprintf("S%d_r%d_c%s_%s.rds", scen, rep, format(scale), mode)))
  cat(sprintf("S%d r%d n=%d scale=%g mode=%s status=%s branch=%s hpm={%s} wall=%.1fs\n", scen, rep, n, scale, mode,
              fit$status, fit$branch_run, paste(fit$hpm, collapse = ","), wall))
}
for (s in scens) for (r in reps) for (c in scales) one_fit(s, r, n, c)
