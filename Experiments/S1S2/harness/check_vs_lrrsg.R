# check_vs_lrrsg.R -- (1) our S1 generator against the authors' reference lrrsg() (XitongLiang/The-PARNI-scheme
# @ 3b95d669e9bcf6df9e2ba46fb89fc536922e12e2, R/simulation/linear regression random sample generator.R), same seed;
# (2) the SMC-BVS engine's internal preprocessing (v3_preprocess) on raw data vs on the repo-preprocessed data
# (X <- scale(X); y <- scale(y, scale = FALSE), R/simulation/dataset_generation.R:28-29).
# Appends a section (rerunning appends again; delete the old section first) to specs/generator_check.md.   Rscript harness/check_vs_lrrsg.R
BASE <- local({ f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)); normalizePath(file.path(dirname(f), "..")) })
source(file.path(BASE, "harness", "generate.R"))
REPO <- "/home/fb31/Bayesian-Variable-Selection/_local/engineering/ext/The-PARNI-scheme@3b95d669e9bcf6df9e2ba46fb89fc536922e12e2"
source(file.path(REPO, "R", "simulation", "linear regression random sample generator.R"))
core <- "/home/fb31/Bayesian-Variable-Selection/_local/engineering/ext/smcbvs_core@7100bb3b"
source(file.path(core, "v3_preprocess.R"))     # pure R preprocessing; no compile needed for v3_standardise / v3_preprocess(dup = FALSE)
tab <- read_settings(file.path(BASE, "specs", "settings.tsv"))
rows <- c(); rows2 <- c()
for (id in tab$setting_id[tab$suite == 1]) {
  row <- tab[tab$setting_id == id, ]
  for (rep in c(1, 2)) {
    d <- gen_data(row, rep)
    RNGkind("Mersenne-Twister", "Inversion", "Rejection")
    L <- lrrsg(n = row$n, p = row$p, rho = 0.6, SNR = row$snr, seed = d$data_seed)
    rows <- c(rows, sprintf("| %s | %d | %s | %s | %.1e | %s |", id, rep, identical(d$X, L$X), identical(d$beta, L$beta),
                            max(abs(d$y - drop(L$y))), identical(d$support, L$position)))
    if (rep == 1 && id %in% c("S1_03", "S1_15")) {
      a <- v3_preprocess(d$X, d$y, dup_components = FALSE)
      Xr <- scale(d$X); yr <- drop(scale(d$y, scale = FALSE)); attributes(Xr) <- list(dim = dim(d$X))
      b <- v3_preprocess(Xr, yr, dup_components = FALSE)
      rows2 <- c(rows2, sprintf("| %s | %.1e | %.1e | %.1e |", id, max(abs(a$X - b$X)), max(abs(a$y - b$y)),
                                max(abs(a$X)) ))
    }
  }
}
md <- c("", "## S1 generator against the authors' reference `lrrsg()` (HQ ruling 2026-11-25)", "",
  "Reference: XitongLiang/The-PARNI-scheme @ `3b95d669e9bcf6df9e2ba46fb89fc536922e12e2` (Griffin is a co-author), clone at `ROOT/ext/The-PARNI-scheme@3b95d669…`.",
  "- `R/simulation/dataset_generation.R:3-5,27`: n ∈ {500, 1000}, p ∈ {500, 5000, 50000}, SNR ∈ {0.5, 1, 2, 3}, `lrrsg(n, p, rho = 0.6, SNR, seed = NULL)`; lines 28-29: `X <- scale(dataset$X)`, `y <- scale(dataset$y, scale = FALSE)`.",
  "- `R/simulation/linear regression random sample generator.R`: `beta_basis = c(2,-3,2,2,-3,3,-2,3,-2,3)` (l.5), `sigma2 = 1` default (l.7), positions `1:b_n` = 1..10 (l.15-17), `beta <- SNR * sqrt(sigma2 * log(p)/n) * beta` (l.19, natural log, σ² = 1), `X <- matrix(rnorm(n*p), n, p)` then the AR(1) recursion `X[,j] <- rho * X[,j-1] + sqrt(1-rho^2) * X[,j]` (l.21-27), `y <- a + X %*% beta + rnorm(n)` with a = 0 (l.31; the noise is N(0, 1), i.e. σ² = 1).",
  "- Ours (`harness/generate.R`): the same Σ (AR(1), ρ = 0.6), the same β (σ² = 1, natural log p, positions 1..10), the same recursion and the same draw order (Z n×p column-major, then ε = rnorm(n)). So it is **not only the same law but the same draws**: called with `seed = data_seed`, `lrrsg()` returns our X, β and y bit for bit (table: max |Δy| = 0 at all 16 settings × reps 1–2). The seeds themselves are ours (INTERFACE). Our generator returns raw X and y (INTERFACE); the repo's `scale()` step is applied in the Bayesian adapters (HQ ruling (b)).",
  "", "| setting | rep | X identical | β identical | max abs Δy | support = position |", "|---|---|---|---|---|---|", rows,
  "", "## SMC-BVS: engine-internal preprocessing vs the repo preprocessing", "",
  "`v3_fit` always calls `v3_preprocess` (core `v3_preprocess.R`, M §4.4, `v3_standardise`): every X column and y are divided by max|x|, centred and divided by the sample SD (n − 1). There is no intercept parameter; centring stands in for it. Feeding the engine the repo-preprocessed data (`scale(X)`, `scale(y, scale = FALSE)`) instead of raw data changes the engine's working input only by floating-point rounding:",
  "", "| setting (rep 1) | max abs Δ standardised X | max abs Δ standardised y | max abs standardised X |", "|---|---|---|---|", rows2,
  "", "So the engine already does the equivalent of the repo preprocessing (it also scales y; because it standardises whatever y it receives, raw y and the repo's centred y reach the engine's model identically to rounding). The adapter passes raw X, y; no SMC smoke rerun is needed.")
cat(md, sep = "\n", file = file.path(BASE, "specs", "generator_check.md"), append = TRUE)
cat(rows, rows2, sep = "\n")
