# Development (dev) datasets for the n = 200 benchmark study: one dataset (dev replicate 1)
# for each scenario S1-S6 at p = 500 and p = 1000 (12 datasets, 5 signal scales each).
# Implements master §II.2-§II.3, §II.7, §II.9-§II.10 (MASTER_Methodology_and_Plan.md, 2026-10-19).
# scenario_covariance() is copied verbatim from Oct-14 Experiments_October_14/scripts/design.R;
# the draw order (X first via chol, then noise) and RNG kind are those of design.R::generate_case().
#
# Usage (NOTS, module load GCC/14.3.0 R/4.5.2):
#   Rscript gen_dev_data.R /projects/ml75/fb31/BVS/bench20261019/dev
# Writes inputs/p{pppp}/<dataset_id>.rds, truth/p{pppp}/<dataset_id>.rds, manifests/*.csv.
# Fitting code must read inputs/ only.

N <- 200L
SCALES <- c(c100 = 1, c075 = 0.75, c050 = 0.50, c035 = 0.35, c025 = 0.25)
DEV_DATA_BASE <- c(`500` = 2410000L, `1000` = 2510000L)    # §II.7 development bases
DEV_FOLD_BASE <- c(`500` = 4410000L, `1000` = 4510000L)    # §II.7 proposed dev fold bases (O11)
METHOD_SEED_OFFSET <- 4000000L                              # §II.7 method seed = data seed + 4,000,000

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

# Port of tools/scenario_check.py::truth (§II.3, §II.9). Uses no random numbers.
truth <- function(p) {
  s0   <- c(`30` = 5L, `500` = 14L, `1000` = 14L)[[as.character(p)]]
  step <- c(`30` = 1L, `500` = 7L, `1000` = 13L)[[as.character(p)]]
  pos  <- c(3L, 2L, 4L, 1L, 5L, 3L)
  pattern <- c(1.4, -1.0, 1.8, -1.2, 0.8, -1.6)
  k <- 0:(s0 - 1L)
  block <- 1L + step * k
  active <- 5L * (block - 1L) + pos[(k %% 6L) + 1L]
  list(active = active, beta = pattern[(k %% 6L) + 1L], block = block)
}

f64_sha256 <- function(x) {
  digest::digest(writeBin(as.double(as.vector(x)), raw(), endian = "little"),
                 algo = "sha256", serialize = FALSE)
}

generate_dev_dataset <- function(p, scenario, replicate = 1L) {
  stopifnot(p %in% c(500L, 1000L), scenario %in% 1:6, replicate %in% 1:100)
  seed <- DEV_DATA_BASE[[as.character(p)]] + 10000L * scenario + replicate
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(seed)
  Sigma <- scenario_covariance(scenario, p)
  raw_X <- matrix(rnorm(N * p), nrow = N) %*% chol(Sigma)      # X first
  X <- scale(raw_X, center = TRUE, scale = TRUE)                # sd with n - 1
  attr(X, "scaled:center") <- NULL; attr(X, "scaled:scale") <- NULL
  eps <- rnorm(N, sd = 1)                                       # then noise
  tr <- truth(p)                                                # no RNG use
  beta <- numeric(p); beta[tr$active] <- tr$beta
  signal <- drop(X %*% beta)
  Y <- sapply(SCALES, function(cc) cc * signal + eps)
  colnames(Y) <- names(SCALES)
  fold_seed <- DEV_FOLD_BASE[[as.character(p)]] + 10000L * scenario + replicate
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(fold_seed)
  foldid <- sample(rep(1:10, length.out = N))
  dataset_id <- sprintf("dev_p%04d_S%d_r%03d", p, scenario, replicate)
  inputs <- list(X = X, Y = Y, foldid = foldid, dataset_id = dataset_id, p = p, n = N,
                 scenario = scenario, replicate = replicate, kind = "dev",
                 data_seed = seed, fold_seed = fold_seed, method_seed = seed + METHOD_SEED_OFFSET,
                 scales = SCALES)
  truth_obj <- list(active = tr$active, beta = beta, signal = signal, eps = eps,
                    scenario = scenario, dataset_id = dataset_id)
  list(inputs = inputs, truth = truth_obj)
}

main <- function(root) {
  stopifnot(requireNamespace("digest", quietly = TRUE))
  rows_in <- list(); rows_tr <- list()
  for (p in c(500L, 1000L)) for (s in 1:6) {
    d <- generate_dev_dataset(p, s, 1L)
    di <- file.path(root, "inputs", sprintf("p%04d", p)); dt <- file.path(root, "truth", sprintf("p%04d", p))
    dir.create(di, recursive = TRUE, showWarnings = FALSE); dir.create(dt, recursive = TRUE, showWarnings = FALSE)
    fi <- file.path(di, paste0(d$inputs$dataset_id, ".rds")); ft <- file.path(dt, paste0(d$inputs$dataset_id, ".rds"))
    if (file.exists(fi) || file.exists(ft)) stop("refusing to overwrite ", fi)
    saveRDS(d$inputs, fi, compress = FALSE); saveRDS(d$truth, ft, compress = FALSE)
    rows_in[[length(rows_in) + 1L]] <- data.frame(
      dataset_id = d$inputs$dataset_id, p = p, scenario = s, replicate = 1L,
      data_seed = d$inputs$data_seed, fold_seed = d$inputs$fold_seed, method_seed = d$inputs$method_seed,
      file_sha256 = digest::digest(file = fi, algo = "sha256"),
      x_sha256 = f64_sha256(d$inputs$X), foldid_sha256 = f64_sha256(d$inputs$foldid),
      t(setNames(vapply(names(SCALES), function(k) f64_sha256(d$inputs$Y[, k]), ""),
                 paste0("y_", names(SCALES), "_sha256"))), check.names = FALSE)
    rows_tr[[length(rows_tr) + 1L]] <- data.frame(
      dataset_id = d$inputs$dataset_id, file_sha256 = digest::digest(file = ft, algo = "sha256"),
      signal_sha256 = f64_sha256(d$truth$signal), eps_sha256 = f64_sha256(d$truth$eps),
      active = paste(d$truth$active, collapse = ";"))
    cat("wrote", d$inputs$dataset_id, "\n")
  }
  dm <- file.path(root, "manifests"); dir.create(dm, recursive = TRUE, showWarnings = FALSE)
  write.csv(do.call(rbind, rows_in), file.path(dm, "dev_inputs_manifest.csv"), row.names = FALSE)
  write.csv(do.call(rbind, rows_tr), file.path(dm, "dev_truth_manifest.csv"), row.names = FALSE)
  Sys.chmod(list.files(file.path(root, c("inputs", "truth")), recursive = TRUE, full.names = TRUE), "0444")
}

if (sys.nframe() == 0L) {
  args <- commandArgs(trailingOnly = TRUE)
  stopifnot(length(args) == 1L)
  main(args[[1]])
}
