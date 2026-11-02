# p0a_probe.R GENERATE_R : localise the P0a regeneration mismatch (OPS-4 diagnosis, read-only). Mirrors generate_dataset() step by step for
# p0020_S1_r001 and p0030_S4_r050 and prints the float64 SHA-256 (first 16 hex) of each intermediate. Run on the laptop and on NOTS; compare.
a <- commandArgs(trailingOnly = TRUE); src <- a[1]
suppressMessages(source(src, chdir = TRUE))
h <- function(x) substr(f64_sha256(x), 1, 16)
cat(sprintf("R %s | BLAS %s | LAPACK %s | FLEXIBLAS=%s\n", getRversion(), extSoftVersion()[["BLAS"]], La_library(), Sys.getenv("FLEXIBLAS")))
for (cs in list(c(20, 1, 1), c(30, 4, 50))) {
  p <- as.integer(cs[1]); s <- as.integer(cs[2]); r <- as.integer(cs[3])
  sd_ <- lowp_seeds(p, s, r, "prod")
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(sd_$data_seed)
  Sigma <- scenario_covariance(s, p); z <- matrix(rnorm(LOWP_N * p), nrow = LOWP_N); C <- chol(Sigma)
  raw <- z %*% C; X <- scale(raw, center = TRUE, scale = TRUE); eps <- rnorm(LOWP_N)
  d <- generate_dataset(p, s, r, "prod")
  cat(sprintf("%s seed=%d | Sigma %s | z %s | chol %s | raw_X %s | X %s | eps %s | dataset X %s | identity_Sigma=%s\n",
              d$inputs$dataset_id, sd_$data_seed, h(Sigma), h(z), h(C), h(raw), h(X), h(eps), h(d$inputs$X), isTRUE(all(Sigma == diag(p)))))
}
