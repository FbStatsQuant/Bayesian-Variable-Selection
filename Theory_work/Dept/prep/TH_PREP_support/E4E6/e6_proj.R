# E6 vs T3: is E[sigma2 | y, MPM] close to the KL-projection variance sigma2_C = sigma2 + beta_M' Sigma_{M|C} beta_M (C = MPM)?
suppressMessages(library(data.table))
TC <- "/home/fb31/Bayesian-Variable-Selection/_local/engineering/reports/S1S2/theory_checks"; H <- "/home/fb31/BVS-wt/P1M/Experiments/S1S2"
source(file.path(H, "harness/generate.R"))
st <- read.delim(file.path(H, "specs/settings.tsv"), colClasses = c(setting_id = "character", beta_type = "character"))
pf <- fread(file.path(TC, "p2_per_fit.tsv"))[status == "ok"]
recs <- readRDS(file.path(TC, "cache/records.rds")); key <- paste(vapply(recs, `[[`, "", "setting_id"), vapply(recs, `[[`, 0L, "rep"))
B <- lapply(split(st, st$setting_id), gen_beta)
Sig <- function(I, J, rho) if (rho == 0) outer(I, J, "==") * 1 else rho^abs(outer(I, J, "-"))
pf[, s2proj := {
  r <- recs[[match(paste(setting_id, rep), key)]]; b <- B[[setting_id]]; rho <- st$rho[st$setting_id == setting_id]
  C <- as.integer(r$mpm); M <- setdiff(which(b != 0), C); bM <- b[M]
  if (!length(M)) sigma2_true else {
    V <- Sig(M, M, rho); if (length(C)) V <- V - Sig(M, C, rho) %*% solve(Sig(C, C, rho), Sig(C, M, rho))
    sigma2_true + drop(t(bM) %*% V %*% bM) }
}, by = .(setting_id, rep)]
pf[, `:=`(r_true = sigma2_mpm_raw / sigma2_true, r_proj = sigma2_mpm_raw / s2proj, miss = s2proj > sigma2_true * (1 + 1e-9))]
st2 <- as.data.table(st)[, .(setting_id, suite, rho, snr, nu, beta_type)]
pf <- merge(pf, st2, by = "setting_id", suffixes = c("", ".st"))
out <- pf[, .(fits = .N, share_miss = mean(miss), med_r_true = median(r_true), med_r_proj = median(r_proj),
              q10_r_proj = quantile(r_proj, .1), q90_r_proj = quantile(r_proj, .9),
              med_r_proj_miss = if (any(miss)) median(r_proj[miss]) else NA_real_),
          by = .(suite.st, nu.st >= 2.07 | snr.st >= 2)]
print(out)
print(pf[miss == TRUE, .(fits = .N, med_r_true = median(r_true), med_r_proj = median(r_proj), q10 = quantile(r_proj, .1), q90 = quantile(r_proj, .9)), by = .(suite.st, n)])
print(pf[suite.st == 2 & nu.st %in% c(2.07, 3.52, 6), .(fits = .N, med_r_true = median(r_true), med_r_proj = median(r_proj)), by = .(nu.st, rho.st, beta_type.st)][order(nu.st, rho.st, beta_type.st)])
fwrite(pf[, .(setting_id, rep, sigma2_true, sigma2_mpm_raw, s2proj, r_true, r_proj, miss)], "e6_proj_per_fit.tsv", sep = "\t")
