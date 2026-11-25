# generate.R -- data generators for the S1/S2 suites.  gen_data(setting_row, rep) -> list(X, y, beta, support, sigma2,
# data_seed, meta).
# PROVENANCE
#   S1 = Griffin, Latuszynski & Steel (2021), "In search of lost mixing time: adaptive Markov chain Monte Carlo schemes
#        for Bayesian variable selection with very large p", Biometrika 108(1):53-69, doi:10.1093/biomet/asaa055;
#        arXiv:1708.05678v3, Sec 4.1, p.13 (the DGP is that of Yang, Wainwright & Jordan 2016):
#        "Y = X beta* + e where e ~ N(0, sigma^2 I) for sigma^2 = 1. The first 10 regression coefficients are non-zero and
#         we use beta* = SNR sqrt(sigma^2 log p / n) (2,-3,2,2,-3,3,-2,3,-2,3,0,...,0)^T. The i-th vector of regressors is
#         generated as x_i ~ N(0, Sigma) where Sigma_jk = rho^|j-k| ... we use the value rho = 0.6".
#        Grid: Table 1, p.14: (n,p) in {(500,500),(500,5000),(1000,500),(1000,5000)}, SNR in {0.5,1,2,3}.
#   S2 = Hastie, Tibshirani & Tibshirani (2020), "Best subset, forward stepwise or lasso? Analysis and recommendations
#        based on extensive comparisons", Statist. Sci. 35(4):579-592, doi:10.1214/19-STS733; arXiv:1707.08692v2,
#        Sec 3.1, pp.8-10, steps i-iii: rows of X i.i.d. N_p(0, Sigma), Sigma_ij = rho^|i-j|; Y ~ N_n(X beta0, sigma^2 I),
#        sigma^2 = beta0' Sigma beta0 / nu (POPULATION Sigma). beta-type 1: "s components equal to 1, occurring at
#        (roughly) equally-spaced indices between 1 and p"; beta-type 2: "first s components equal to 1".
#        The authors' code (R package bestsubset, github.com/ryantibs/best-subset @ 796e81713634aef8b66363f9740efed5df3ba213,
#        bestsubset/R/sim.R, function sim.xy) fixes "roughly equally spaced" as beta[round(seq(1, p, length = s))] = 1 and
#        sigma = sqrt(t(beta) %*% Sigma %*% beta / snr). We use exactly those two lines (R's round(), half-to-even).
#   Seeds: INTERFACE.md "Seeds": data_seed = 5e8 + 1e6*suite + 1e3*cell + rep; RNGkind Mersenne-Twister/Inversion/Rejection.
#   OURS (flagged in SPEC.md): (a) the N(0, Sigma) draw uses the exact AR(1) recursion
#        x_1 = z_1, x_j = rho x_{j-1} + sqrt(1 - rho^2) z_j  (same law as the papers; sim.xy instead multiplies by an SVD
#        square root of Sigma, so realisations differ from bestsubset's for the same seed); (b) draw order: Z (n x p,
#        column-major) then eps (n); (c) no validation set (HTT draw one for tuning; our methods tune per their authors);
#        (d) X is neither centred nor scaled (neither paper does so in the DGP); no intercept.

gen_beta <- function(row) {
  p <- as.integer(row$p); n <- as.integer(row$n); s <- as.integer(row$s0)
  beta <- numeric(p)
  if (row$suite == 1) {
    beta[1:10] <- row$snr * sqrt(1 * log(p) / n) * c(2, -3, 2, 2, -3, 3, -2, 3, -2, 3)   # sigma^2 = 1
  } else if (as.character(row$beta_type) == "1") {
    beta[round(seq(1, p, length = s))] <- 1                                               # sim.xy, beta.type == 1
  } else if (as.character(row$beta_type) == "2") {
    beta[1:s] <- 1                                                                        # sim.xy, beta.type == 2
  } else stop("unknown beta_type ", row$beta_type)
  beta
}

# beta' Sigma beta for Sigma_jk = rho^|j-k| (exact; support only)
quad_ar1 <- function(beta, rho) {
  S <- which(beta != 0); b <- beta[S]
  if (rho == 0) return(sum(b^2))
  sum(outer(b, b) * rho^abs(outer(S, S, "-")))
}

data_seed_of <- function(suite, cell, rep) 500000000 + 1000000 * suite + 1000 * cell + rep

gen_data <- function(setting_row, rep) {
  row <- as.list(setting_row)
  n <- as.integer(row$n); p <- as.integer(row$p); rho <- as.numeric(row$rho)
  data_seed <- data_seed_of(as.integer(row$suite), as.integer(row$cell), as.integer(rep))
  RNGkind("Mersenne-Twister", "Inversion", "Rejection")
  set.seed(data_seed)
  X <- matrix(rnorm(n * p), n, p)
  if (rho != 0) {                                  # exact AR(1) recursion: rows ~ N_p(0, Sigma), Sigma_jk = rho^|j-k|
    a <- sqrt(1 - rho^2)
    for (j in 2:p) X[, j] <- rho * X[, j - 1] + a * X[, j]
  }
  beta <- gen_beta(row)
  support <- which(beta != 0)
  vmu <- quad_ar1(beta, rho)                       # beta' Sigma beta (population)
  sigma2 <- if (row$suite == 1) 1 else vmu / as.numeric(row$nu)
  eps <- rnorm(n) * sqrt(sigma2)
  mu <- drop(X[, support, drop = FALSE] %*% beta[support])
  y <- mu + eps
  meta <- list(setting_id = row$setting_id, suite = as.integer(row$suite), cell = as.integer(row$cell), rep = as.integer(rep),
               n = n, p = p, s0 = length(support), rho = rho, snr = row$snr, nu = row$nu, beta_type = row$beta_type,
               nu_pop = vmu / sigma2,                    # population SNR  beta' Sigma beta / sigma^2
               nu_sample = stats::var(mu) / sigma2,      # sample SNR      Var_n(X beta) / sigma^2
               pve_pop = vmu / (vmu + sigma2),
               generator = "S1S2/harness/generate.R (AR(1) recursion)")
  list(X = X, y = y, beta = beta, support = support, sigma2 = sigma2, data_seed = data_seed, meta = meta)
}

read_settings <- function(path) {
  tab <- utils::read.delim(path, colClasses = c(setting_id = "character", beta_type = "character"), na.strings = "NA")
  tab
}
