# e0_e3_e4_e5_e6.R -- E0 regime table, E3 (Song-Liang Cond 3, Gaussian AR(1)), E4 (bounded signal), E5 (eigenvalue floors),
# E6 (dimension regimes).  Analytic / retabulation; one numerical confirmation for E3 (setting S1_03) and one brute-force R(S) check.
# Run: (thread vars exported)  nice -n 19 Rscript scripts/e0_e3_e4_e5_e6.R
suppressMessages(library(data.table))
args <- commandArgs(FALSE); sf <- sub("--file=", "", args[grep("--file=", args)])
base <- normalizePath(file.path(dirname(sf), ".."))
source(file.path(base, "scripts", "pop_lib.R"))
st <- read_settings(SETTINGS_TSV)
p1s <- read.delim(file.path(ENG, "theory_checks", "p1_by_setting.tsv"), stringsAsFactors = FALSE)
pf <- fread(file.path(ENG, "theory_checks", "p1_per_fit.tsv"), data.table = FALSE)
mg <- read.delim(file.path(base, "tables", "e1_margin_by_setting.tsv"), stringsAsFactors = FALSE)

# ---------------- E0 ----------------
ft <- as.data.frame.matrix(table(pf$setting_id, pf$failure_type))     # failure_type counts per setting (FALSE = no failure label)
ft$setting_id <- rownames(ft)
k <- aggregate(success ~ setting_id, pf, function(x) sum(as.logical(x))); names(k)[2] <- "k_exact"
nn <- aggregate(success ~ setting_id, pf, length); names(nn)[2] <- "n_fits"
e0 <- Reduce(function(a, b) merge(a, b, by = "setting_id"), list(st[, c("setting_id", "suite", "n", "p", "s0", "rho", "snr", "nu", "beta_type", "nu_pop")], k, nn, ft))
w <- t(mapply(wilson, e0$k_exact, e0$n_fits)); e0$exact_lo <- w[, 1]; e0$exact_hi <- w[, 2]; e0$exact_share <- e0$k_exact / e0$n_fits
e0$A <- log(e0$p) / log(e0$n); e0$s0logp_n <- e0$s0 * log(e0$p) / e0$n; e0$logp_n <- log(e0$p) / e0$n
e0$logp2_n <- log(e0$p)^2 / e0$n; e0$loglogp_logn <- log(log(e0$p)) / log(e0$n)
e0$eps_n <- sqrt(e0$s0logp_n); e0$sqrt_logn_n <- sqrt(log(e0$n) / e0$n)
e0$kappa_eff_SLcorS1 <- log(e0$p) / log(e0$n)^2           # p = n^{kappa log n}  <=>  kappa = log p / (log n)^2 ; SL Cor S1 needs kappa < 1/4
e0$logp_over_sqrtn <- log(e0$p) / sqrt(e0$n)
write_tsv(e0, file.path(base, "tables", "e0_regime_by_setting.tsv"))

cellsum <- function(d, by) { a <- aggregate(d[, c("A", "s0logp_n", "logp_n", "logp2_n", "eps_n", "sqrt_logn_n", "kappa_eff_SLcorS1", "logp_over_sqrtn", "exact_share")], d[by], median)
  a$n_settings <- aggregate(setting_id ~ ., d[c("setting_id", by)], length)$setting_id; a }
write_tsv(cellsum(e0[e0$suite == 1, ], c("n", "p")), file.path(base, "tables", "e0_regime_S1_by_np.tsv"))
write_tsv(cellsum(e0[e0$suite == 2, ], c("n", "p", "s0")), file.path(base, "tables", "e0_regime_S2_by_np.tsv"))

# ---------------- E3: Song-Liang Condition 3 (identifiability) for Gaussian AR(1), unit variance ----------------
# Z = x_k + sum_i b_i x_{j_i} ~ N(0, V),  V >= v_min = Var(x_k | others) ;  E exp(-Z^2) = (1+2V)^(-1/2)  =>  delta_SL = 1 - (1+2 v_min)^(-1/2).
# For AR(1): Var(x_k | all others) = 1/[Sigma^-1]_kk = (1-rho^2)/(1+rho^2) (interior k, >= 2 others), 1-rho^2 (end column), 1 (no others).
e3 <- do.call(rbind, lapply(seq_len(nrow(st)), function(i) { r <- st$rho[i]; n <- st$n[i]; s0 <- st$s0[i]; p <- st$p[i]
  v <- (1 - r^2) / (1 + r^2); dl <- 1 - (1 + 2 * v)^(-0.5); eps2 <- s0 * log(p) / n
  rb <- c(s0 = s0, s0x2 = 2 * s0, logn_s0 = ceiling(log(n)) * s0)
  data.frame(setting_id = st$setting_id[i], suite = st$suite[i], n = n, p = p, s0 = s0, rho = r, v_min = v, delta_SL = dl, eps2_n = eps2,
    eps2_over_delta = eps2 / dl, rbar_s0_eps2 = rb[1] * eps2, rbar_2s0_eps2 = rb[2] * eps2, rbar_logn_s0_eps2 = rb[3] * eps2,
    r1_s0_over_delta = rb[1] * eps2 / dl, r2_s0_over_delta = rb[2] * eps2 / dl, r3_logn_s0_over_delta = rb[3] * eps2 / dl) }))
write_tsv(e3, file.path(base, "tables", "e3_condition3.tsv"))
# numerical confirmation on S1_03 (n=500,p=500,rho=.6): (i) exact conditional variances from Sigma^-1 and over random sets, (ii) Monte Carlo of E exp(-Z^2)
set.seed(20261127)
i3 <- which(st$setting_id == "S1_03"); r <- st$rho[i3]; p <- st$p[i3]; n <- st$n[i3]
Sg <- ar1(1:p, 1:p, r); Pm <- solve(Sg); cv_all <- 1 / diag(Pm)
chk <- list()
chk$cv_interior <- cv_all[250]; chk$cv_end <- cv_all[1]; chk$theory_interior <- (1 - r^2) / (1 + r^2); chk$theory_end <- 1 - r^2
rand_min <- Inf; nb_min <- Inf
for (rr in 1:12) for (rep in 1:300) { k0 <- sample(2:(p - 1), 1); oth <- sample(setdiff(1:p, k0), rr)
  cvv <- Sg[k0, k0] - Sg[k0, oth, drop = FALSE] %*% solve(Sg[oth, oth, drop = FALSE], Sg[oth, k0]); rand_min <- min(rand_min, cvv)
  oth2 <- unique(c(k0 - 1, k0 + 1, oth))[seq_len(max(rr, 2))]; cvv2 <- Sg[k0, k0] - Sg[k0, oth2, drop = FALSE] %*% solve(Sg[oth2, oth2, drop = FALSE], Sg[oth2, k0]); nb_min <- min(nb_min, cvv2) }
chk$min_cv_random_sets <- rand_min; chk$min_cv_neighbour_sets <- nb_min
S3 <- ar1(249:251, 249:251, r); L <- chol(S3); NN <- 2e6
Xm <- matrix(rnorm(NN * 3), NN, 3) %*% L; b <- -solve(S3[2:3, 2:3], S3[2:3, 1])   # Z = x_249 + b1 x_250 + b2 x_251 ... choose k = 249? use k=250 below
S3b <- ar1(c(250, 249, 251), c(250, 249, 251), r); Lb <- chol(S3b); Xb <- matrix(rnorm(NN * 3), NN, 3) %*% Lb
bb <- -solve(S3b[2:3, 2:3], S3b[2:3, 1]); Z <- Xb[, 1] + Xb[, 2:3] %*% bb
chk$MC_E_exp_negZ2_opt <- mean(exp(-Z^2)); chk$formula_E_exp_negZ2 <- (1 + 2 * (1 - r^2) / (1 + r^2))^(-0.5); chk$MC_var_Z <- var(Z)
# generator check: residual variance of column 250 on columns 249,251 in one generated dataset (S1_03 rep 1, n = 500)
gd <- gen_data(st[i3, ], 1); Xg <- gd$X; chk$gen_resid_var_col250_on_249_251 <- summary(lm(Xg[, 250] ~ Xg[, 249] + Xg[, 251]))$sigma^2
chk$gen_resid_var_se_approx <- chk$theory_interior * sqrt(2 / (n - 3))
chk_df <- data.frame(quantity = names(chk), value = unlist(chk)); write_tsv(chk_df, file.path(base, "tables", "e3_numeric_check_S1_03.tsv"))
print(chk_df)

# ---------------- E4: bounded signal ----------------
e4 <- do.call(rbind, lapply(seq_len(nrow(st)), function(i) { ps <- setting_pop(st[i, ])
  data.frame(setting_id = st$setting_id[i], suite = st$suite[i], n = ps$n, p = ps$p, s0 = ps$s0, rho = ps$rho, sigma2 = ps$sigma2,
    max_abs_beta_over_sigma = max(abs(ps$b0)) / sqrt(ps$sigma2), min_abs_beta_over_sigma = min(abs(ps$b0)) / sqrt(ps$sigma2),
    betaSigmaBeta_over_sigma2 = ps$vmu / ps$sigma2, beta_min_over_sigma_sqrt_logp_n = min(abs(ps$b0)) / sqrt(ps$sigma2) / sqrt(log(ps$p) / ps$n),
    beta_min_over_sigma_sqrt_logn_n = min(abs(ps$b0)) / sqrt(ps$sigma2) / sqrt(log(ps$n) / ps$n)) }))
write_tsv(e4, file.path(base, "tables", "e4_bounded_signal.tsv"))

# ---------------- E5: eigenvalue floors ----------------
e5 <- do.call(rbind, lapply(seq_len(nrow(st)), function(i) { ps <- setting_pop(st[i, ])
  lmin_S0 <- min(eigen(ar1(ps$S0, ps$S0, ps$rho), symmetric = TRUE, only.values = TRUE)$values)
  q <- p1s[p1s$setting_id == st$setting_id[i], ]
  fl <- (1 - ps$rho) / (1 + ps$rho)
  data.frame(setting_id = st$setting_id[i], suite = st$suite[i], n = ps$n, p = ps$p, s0 = ps$s0, rho = ps$rho, beta_type = st$beta_type[i],
    pop_floor_any_T = fl, pop_lmin_S0 = lmin_S0, pop_lmin_S0_over_floor = lmin_S0 / fl,
    n_times_floor = ps$n * fl, sample_lmin_S0_median = q$med_lmin_S0, m1 = q$m1, sample_greedy_m1_median = q$med_lmin_greedy_m1,
    m2 = q$m2, sample_greedy_m2_median = q$med_lmin_greedy_m2, sample_greedy_m1_over_floor = q$med_lmin_greedy_m1 / fl,
    sample_greedy_m2_over_floor = q$med_lmin_greedy_m2 / fl, med_size_T = q$med_size_T, med_lmin_T = q$med_lmin_T, min_lmin_T = q$min_lmin_T) }))
write_tsv(e5, file.path(base, "tables", "e5_eigen_floors.tsv"))

# ---------------- E6: dimension regimes ----------------
reg <- function(n, p, lab) data.frame(label = lab, n = n, p = p, A = log(p) / log(n), p_le_n1.5 = p <= n^1.5, p_le_n2 = p <= n^2, p_le_n3 = p <= n^3,
  kappa_eff = log(p) / log(n)^2, SL_CorS1_ok = log(p) / log(n)^2 < 0.25, logp_over_sqrtn = log(p) / sqrt(n), logp_le_sqrtn = log(p) <= sqrt(n),
  logp_over_n = log(p) / n, logp2_over_n = log(p)^2 / n)
usr <- rbind(reg(100, 1e3, "(100,1e3)"), reg(500, 1e4, "(500,1e4)"), reg(1000, 1e5, "(1000,1e5)"), reg(5000, 1e6, "(5000,1e6)"),
             reg(300, 2e4, "(300,2e4) gene expression"), reg(1e4, 5e5, "(1e4,5e5) GWAS"))
write_tsv(usr, file.path(base, "tables", "e6_typical_regimes.tsv"))
np <- unique(st[, c("suite", "n", "p")])
s6 <- do.call(rbind, lapply(seq_len(nrow(np)), function(i) { x <- reg(np$n[i], np$p[i], sprintf("S%d (n=%d,p=%d)", np$suite[i], np$n[i], np$p[i])); x }))
write_tsv(s6, file.path(base, "tables", "e6_S1S2_regimes.tsv"))
print(s6, digits = 3); print(usr, digits = 3)

# ---------------- brute-force validation of R(S) (one setting) ----------------
# Setting S2_080 (bt1, n=100, rho=.35, nu=6): D = {j}, N = its two neighbours; and S1_03 with D={1,2}, N={11,12}.  Large simulated X (N = 2e5 rows) from the generator's AR(1) recursion.
bf <- list()
for (sid in c("S2_080", "S1_03", "S2_117")) {
  i <- which(st$setting_id == sid); ps <- setting_pop(st[i, ]); set.seed(777)
  Dtest <- if (sid == "S1_03") c(1, 2) else if (sid == "S2_117") c(1, 2, 3) else 3
  Ntest <- if (sid == "S1_03") c(11, 12) else if (sid == "S2_117") integer(0) else { j <- ps$S0[3]; c(j - 1, j + 1) }
  cols <- sort(unique(c(ps$S0, Ntest)))
  Nn <- 2e5; Z <- matrix(rnorm(Nn * length(cols)), Nn, length(cols))
  # AR(1) draws restricted to the needed columns: use chol of the population Sigma on those columns (equal in law to the generator's recursion)
  Xs <- Z %*% chol(ar1(cols, cols, ps$rho)); colnames(Xs) <- cols
  mu <- Xs[, as.character(ps$S0)] %*% ps$b0
  S <- c(ps$S0[-Dtest], Ntest)
  fit <- lm(mu ~ Xs[, as.character(S)] - 1)                    # population: mu exact linear in x_S0; residual var = Var(x'b | x_S)
  Rbf <- ps$n * mean(residuals(fit)^2) * (Nn / (Nn - length(S)))
  Rth <- RS(ps, Dtest, Ntest)
  bf[[sid]] <- data.frame(setting_id = sid, D = paste(ps$S0[Dtest], collapse = ","), N = paste(Ntest, collapse = ","), R_formula = Rth, R_bruteforce_2e5rows = Rbf, rel_diff = Rbf / Rth - 1)
}
bf <- do.call(rbind, bf); write_tsv(bf, file.path(base, "tables", "validation_RS_bruteforce.tsv")); print(bf)
# also: gen_data realised sample check for R(S): regress sample mu = X b on columns S in ONE generated dataset (n = 100) is noisy; use S1_03 (n=500, p=500) rep 1..20 mean
i <- which(st$setting_id == "S1_03"); ps <- setting_pop(st[i, ]); vv <- numeric(20)
for (rp in 1:20) { gd <- gen_data(st[i, ], rp); Xg <- gd$X; mu <- drop(Xg[, ps$S0] %*% ps$b0); S <- c(ps$S0[-c(1, 2)], 3, 11)
  # D = {S0 positions 1,2} = columns 1,2 ; N = columns 3, 11 ; x_3 is in S0? S0 = 1..10 so column 3 is already in S0 -> use nulls 11,12
  S <- c(ps$S0[-c(1, 2)], 11, 12); vv[rp] <- ps$n * mean(residuals(lm(mu ~ Xg[, S] - 1))^2) * (500 / (500 - length(S))) }
bf2 <- data.frame(setting_id = "S1_03", D = "1,2", N = "11,12", R_formula = RS(ps, c(1, 2), c(11, 12)), R_gen_data_mean20 = mean(vv), R_gen_data_se = sd(vv) / sqrt(20))
write_tsv(bf2, file.path(base, "tables", "validation_RS_gendata.tsv")); print(bf2)

# cross-check kappa_del vs P1 population min t^2 (must agree < 2%): P1 column med_min_t2_pop (per-setting median of population min t^2, constant within setting)
cx <- merge(mg[, c("setting_id", "min_t2_pop", "kappa_del", "price", "sigma2")], p1s[, c("setting_id", "med_min_t2_pop", "price")], by = "setting_id", suffixes = c("", "_P1"))
cx$rel_diff_t2 <- cx$min_t2_pop / cx$med_min_t2_pop - 1; cx$rel_diff_price <- cx$price / cx$price_P1 - 1
cx$kappa_del_from_P1 <- cx$med_min_t2_pop / (2 * cx$price_P1); cx$rel_diff_kappa <- cx$kappa_del / cx$kappa_del_from_P1 - 1
write_tsv(cx, file.path(base, "tables", "validation_kappa_del_vs_P1.tsv"))
cat("max |rel diff| min t2 pop vs P1:", max(abs(cx$rel_diff_t2)), "; price:", max(abs(cx$rel_diff_price)), "; kappa_del:", max(abs(cx$rel_diff_kappa)), "\n")
