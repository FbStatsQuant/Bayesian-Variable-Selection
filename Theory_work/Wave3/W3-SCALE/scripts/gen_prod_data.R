# Production datasets for the n = 200 benchmark study (Regime H): p in {500, 1000} x S1-S6 x
# replicates 1-100 = 1,200 datasets, 5 signal scales each. Master §II.2-§II.10 and §II.12.
# Same generator as gen_dev_data.R (verified 93/93 on the dev data); only the seed bases and ids differ:
#   data seed = base + 10000*s + r, base 1,410,000 (p = 500, = Oct-14) / 1,510,000 (p = 1000)
#   fold seed = 3,410,000 / 3,510,000 + 10000*s + r;  method seed = data seed + 4,000,000
# Usage (NOTS, module load GCC/14.3.0; module load R/4.5.2):
#   Rscript gen_prod_data.R <STUDY root> <p> <scenario>      # one (p, s) cell = 100 datasets
# Writes <root>/inputs/p{pppp}/p{pppp}_S{s}_r{rrr}.rds, <root>/truth/p{pppp}/..., and a per-cell
# manifest fragment <root>/manifests/cells/p{pppp}_S{s}_{inputs,truth}.csv. Refuses to overwrite.

N <- 200L
SCALES <- c(c100 = 1, c075 = 0.75, c050 = 0.50, c035 = 0.35, c025 = 0.25)
DATA_BASE <- c(`500` = 1410000L, `1000` = 1510000L)
FOLD_BASE <- c(`500` = 3410000L, `1000` = 3510000L)
METHOD_SEED_OFFSET <- 4000000L

gen_dev_env <- new.env()
here <- function() {
  a <- grep("^--file=", commandArgs(FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
}
# scenario_covariance(), truth() and f64_sha256() are reused verbatim from the verified dev generator.
sys.source(file.path(here(), "gen_dev_data.R"), envir = gen_dev_env)
scenario_covariance <- gen_dev_env$scenario_covariance
truth <- gen_dev_env$truth
f64_sha256 <- gen_dev_env$f64_sha256

generate_prod_dataset <- function(p, scenario, replicate, Sigma_chol = NULL) {
  stopifnot(p %in% c(500L, 1000L), scenario %in% 1:6, replicate %in% 1:100)
  seed <- DATA_BASE[[as.character(p)]] + 10000L * scenario + replicate
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(seed)
  if (is.null(Sigma_chol)) Sigma_chol <- chol(scenario_covariance(scenario, p))
  raw_X <- matrix(rnorm(N * p), nrow = N) %*% Sigma_chol       # X first (design.R order)
  X <- scale(raw_X, center = TRUE, scale = TRUE)
  attr(X, "scaled:center") <- NULL; attr(X, "scaled:scale") <- NULL
  eps <- rnorm(N, sd = 1)                                       # then noise
  tr <- truth(p)
  beta <- numeric(p); beta[tr$active] <- tr$beta
  signal <- drop(X %*% beta)
  Y <- sapply(SCALES, function(cc) cc * signal + eps); colnames(Y) <- names(SCALES)
  fold_seed <- FOLD_BASE[[as.character(p)]] + 10000L * scenario + replicate
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(fold_seed)
  foldid <- sample(rep(1:10, length.out = N))
  dataset_id <- sprintf("p%04d_S%d_r%03d", p, scenario, replicate)
  list(inputs = list(X = X, Y = Y, foldid = foldid, dataset_id = dataset_id, p = p, n = N,
                     scenario = scenario, replicate = replicate, kind = "prod",
                     data_seed = seed, fold_seed = fold_seed, method_seed = seed + METHOD_SEED_OFFSET,
                     scales = SCALES),
       truth = list(active = tr$active, beta = beta, signal = signal, eps = eps,
                    scenario = scenario, dataset_id = dataset_id))
}

main <- function(root, p, s) {
  stopifnot(requireNamespace("digest", quietly = TRUE))
  di <- file.path(root, "inputs", sprintf("p%04d", p)); dt <- file.path(root, "truth", sprintf("p%04d", p))
  dm <- file.path(root, "manifests", "cells")
  for (d in c(di, dt, dm)) dir.create(d, recursive = TRUE, showWarnings = FALSE)
  # chol(Sigma) is deterministic; computing it once per cell gives the same bits as per dataset
  # (verify_prod_data.R regenerates datasets with a fresh chol and compares with identical()).
  L <- chol(scenario_covariance(s, p))
  rows_in <- list(); rows_tr <- list()
  for (r in 1:100) {
    d <- generate_prod_dataset(p, s, r, L)
    fi <- file.path(di, paste0(d$inputs$dataset_id, ".rds")); ft <- file.path(dt, paste0(d$inputs$dataset_id, ".rds"))
    if (file.exists(fi) || file.exists(ft)) stop("refusing to overwrite ", fi)
    saveRDS(d$inputs, fi, compress = FALSE); saveRDS(d$truth, ft, compress = FALSE)
    Sys.chmod(c(fi, ft), "0444")
    rows_in[[r]] <- data.frame(
      dataset_id = d$inputs$dataset_id, p = p, scenario = s, replicate = r,
      data_seed = d$inputs$data_seed, fold_seed = d$inputs$fold_seed, method_seed = d$inputs$method_seed,
      file_sha256 = digest::digest(file = fi, algo = "sha256"),
      x_sha256 = f64_sha256(d$inputs$X), foldid_sha256 = f64_sha256(d$inputs$foldid),
      t(setNames(vapply(names(SCALES), function(k) f64_sha256(d$inputs$Y[, k]), ""),
                 paste0("y_", names(SCALES), "_sha256"))), check.names = FALSE)
    rows_tr[[r]] <- data.frame(
      dataset_id = d$inputs$dataset_id, file_sha256 = digest::digest(file = ft, algo = "sha256"),
      signal_sha256 = f64_sha256(d$truth$signal), eps_sha256 = f64_sha256(d$truth$eps),
      active = paste(d$truth$active, collapse = ";"))
  }
  write.csv(do.call(rbind, rows_in), file.path(dm, sprintf("p%04d_S%d_inputs.csv", p, s)), row.names = FALSE)
  write.csv(do.call(rbind, rows_tr), file.path(dm, sprintf("p%04d_S%d_truth.csv", p, s)), row.names = FALSE)
  cat(sprintf("cell p=%d S%d: 100 datasets written\n", p, s))
}

if (sys.nframe() == 0L) {
  a <- commandArgs(trailingOnly = TRUE); stopifnot(length(a) == 3L)
  main(a[[1]], as.integer(a[[2]]), as.integer(a[[3]]))
}
