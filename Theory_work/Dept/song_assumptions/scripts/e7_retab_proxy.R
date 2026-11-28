# e7_retab_proxy.R -- E7: re-tabulate (not recompute) P2's E4/E5/E6 and P1's E2/E3 headline numbers with provenance; E6 sigma^2_C check
# recomputed from stored MPMs (replicating Theory's e6_proj.R logic with pop_lib); proxy-behaviour share among failed fits.
# Inputs (READ ONLY): ENG/theory_checks/{p1_by_setting,p2_by_setting,p2_per_fit}.tsv, ENG/theory_checks/cache/records.rds,
#                     Theory_work/Dept/prep/TH_PREP_support/E4E6/e4_dh_by_setting.tsv
# Run: (thread vars exported) nice -n 19 Rscript scripts/e7_retab_proxy.R
suppressMessages(library(data.table))
args <- commandArgs(FALSE); sf <- sub("--file=", "", args[grep("--file=", args)]); base <- normalizePath(file.path(dirname(sf), ".."))
source(file.path(base, "scripts", "pop_lib.R")); st <- read_settings(SETTINGS_TSV)
TC <- file.path(ENG, "theory_checks")
DH <- "/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Dept/prep/TH_PREP_support/E4E6/e4_dh_by_setting.tsv"
p1 <- read.delim(file.path(TC, "p1_by_setting.tsv"), stringsAsFactors = FALSE); p2 <- read.delim(file.path(TC, "p2_by_setting.tsv"), stringsAsFactors = FALSE)
dh <- read.delim(DH, stringsAsFactors = FALSE)
grp <- function(d) ifelse(d$suite == 1, ifelse(d$snr >= 2, "S1 SNR>=2", "S1 SNR<=1"), ifelse(d$nu >= 2.07, ifelse(d$nu == 6, "S2 nu=6", "S2 nu in [2.07,3.52]"), "S2 nu<2.07"))
# ---- E4 (Hellinger d_H/eps_n): by group; source e4_dh_by_setting.tsv columns med_ratio (= med d_mix/eps_n), q90_d_mix, eps_n
dh$g <- grp(dh); dh$q90_ratio <- dh$q90_d_mix / dh$eps_n
e4 <- aggregate(cbind(med_ratio, q90_ratio, eps_n) ~ g, dh, function(x) c(min = min(x), med = median(x), max = max(x)))
e4f <- do.call(data.frame, e4); write_tsv(e4f, file.path(base, "tables", "e7_E4_dH_by_group.tsv"))
e4a <- data.frame(n_settings = nrow(dh), n_dH_lt_eps = sum(dh$med_d_mix < dh$eps_n & dh$q90_d_mix < dh$eps_n), max_q90_ratio = max(dh$q90_ratio), min_med_ratio = min(dh$med_ratio), max_med_ratio = max(dh$med_ratio))
write_tsv(e4a, file.path(base, "tables", "e7_E4_dH_overall.tsv"))
# ---- E5 (size cap): p2_by_setting columns K, n_cap_binds_store, n_cap_binds_top50, max_size_pos_mass, max_over_K, max_mass_size_ge_Km2
p2$g <- grp(p2)
e5 <- do.call(rbind, lapply(split(p2, p2$g), function(d) data.frame(group = d$g[1], n_settings = nrow(d), cap_binds_store_total = sum(d$n_cap_binds_store), cap_binds_top50_total = sum(d$n_cap_binds_top50),
  max_mass_size_ge_Km2 = max(d$max_mass_size_ge_Km2), max_size_pos_mass = max(d$max_size_pos_mass), K_min = min(d$K), K_max = max(d$K), max_over_K = max(d$max_over_K), med_over_K = median(d$max_over_K))))
write_tsv(e5, file.path(base, "tables", "e7_E5_size_cap.tsv"))
# ---- E6 (sigma^2): p2_by_setting med_ratio_Esig2_list, med_ratio_sigma2_mpm
e6 <- do.call(rbind, lapply(split(p2, p2$g), function(d) data.frame(group = d$g[1], n_settings = nrow(d), Esig2_list_ratio_min = min(d$med_ratio_Esig2_list), Esig2_list_ratio_med = median(d$med_ratio_Esig2_list), Esig2_list_ratio_max = max(d$med_ratio_Esig2_list),
  Esig2_mpm_ratio_min = min(d$med_ratio_sigma2_mpm), Esig2_mpm_ratio_med = median(d$med_ratio_sigma2_mpm), Esig2_mpm_ratio_max = max(d$med_ratio_sigma2_mpm))))
write_tsv(e6, file.path(base, "tables", "e7_E6_sigma2_ratio.tsv"))
# ---- P1 E2 / E3 by group (p1_by_setting columns med_lmin_S0, med_lmin_greedy_m1/m2, med_lmin_T, med_pi_ratio_given_exact, med_pi_S0)
p1$g <- grp(p1)
e23 <- do.call(rbind, lapply(split(p1, p1$g), function(d) data.frame(group = d$g[1], n_settings = nrow(d), lmin_S0_med = median(d$med_lmin_S0), greedy_m1_med = median(d$med_lmin_greedy_m1), greedy_m1_min = min(d$med_lmin_greedy_m1),
  greedy_m2_med = median(d$med_lmin_greedy_m2), greedy_m2_min = min(d$med_lmin_greedy_m2), lmin_T_med = median(d$med_lmin_T),
  pi_ratio_exact_min = suppressWarnings(min(d$med_pi_ratio_given_exact, na.rm = TRUE)), pi_ratio_exact_max = suppressWarnings(max(d$med_pi_ratio_given_exact, na.rm = TRUE)))))
write_tsv(e23, file.path(base, "tables", "e7_P1_E2E3_by_group.tsv"))

# ---- E6 sigma^2_C (KL projection onto MPM) and proxy shares, from stored MPMs
rec <- readRDS(file.path(TC, "cache", "records.rds"))
pf2 <- fread(file.path(TC, "p2_per_fit.tsv"), data.table = FALSE); pf2 <- pf2[pf2$status == "ok", ]
key <- paste(vapply(rec, `[[`, "", "setting_id"), vapply(rec, `[[`, 0L, "rep"))
pf2$ri <- match(paste(pf2$setting_id, pf2$rep), key)
stI <- setNames(seq_len(nrow(st)), st$setting_id)
POP <- lapply(st$setting_id, function(s) setting_pop(st[stI[s], ])); names(POP) <- st$setting_id
rowf <- function(i) {
  r <- rec[[pf2$ri[i]]]; ps <- POP[[pf2$setting_id[i]]]; C <- as.integer(r$mpm); S0 <- ps$S0
  M <- setdiff(S0, C); nulls <- setdiff(C, S0)
  s2c <- ps$sigma2
  if (length(M)) { bM <- ps$b0[match(M, S0)]; s2c <- ps$sigma2 + cvar(M, bM, C, ps$rho) }
  # proxy: failed fit, misses >=1 true, includes >=1 null within distance 1 (or <=3) of a MISSED true variable
  nb1 <- length(M) > 0 && length(nulls) > 0 && any(vapply(M, function(m) any(abs(nulls - m) == 1), TRUE))
  nb3 <- length(M) > 0 && length(nulls) > 0 && any(vapply(M, function(m) any(abs(nulls - m) <= 3), TRUE))
  c(s2c = s2c, nM = length(M), nNull = length(nulls), nb1 = nb1, nb3 = nb3, nTrueSel = length(intersect(C, S0)), size = length(C))
}
mm <- t(vapply(seq_len(nrow(pf2)), rowf, numeric(7)))
pf2 <- cbind(pf2[, c("setting_id", "rep", "suite", "rho", "snr", "nu", "beta_type", "n", "s0", "sigma2_true", "sigma2_mpm_raw", "exact")], as.data.frame(mm))
pf2$r_true <- pf2$sigma2_mpm_raw / pf2$sigma2_true; pf2$r_proj <- pf2$sigma2_mpm_raw / pf2$s2c
pf2$g <- grp(pf2)
write_tsv(pf2[pf2$rep <= 3, ], file.path(base, "tables", "e7_per_fit_sample_rep1to3.tsv"))
e6c <- do.call(rbind, lapply(split(pf2, pf2$g), function(d) { m <- d$nM > 0
  data.frame(group = d$g[1], fits = nrow(d), share_MPM_misses_true = mean(m), med_Esig2MPM_over_sigma2 = median(d$r_true), med_Esig2MPM_over_sigma2C = median(d$r_proj),
    q10_over_sigma2C = quantile(d$r_proj, .1), q90_over_sigma2C = quantile(d$r_proj, .9), med_over_sigma2C_given_miss = if (any(m)) median(d$r_proj[m]) else NA, med_over_sigma2_given_miss = if (any(m)) median(d$r_true[m]) else NA) }))
write_tsv(e6c, file.path(base, "tables", "e7_E6_sigma2C.tsv"))
# proxy shares among FAILED fits
fl <- pf2[!pf2$exact, ]
fl$cat <- ifelse(fl$nM == 0, "superset of S0 (no miss, has FP)", ifelse(fl$size == 0, "empty MPM", ifelse(fl$nNull == 0, "pure under-selection (miss, no FP)", ifelse(fl$nb1 == 1, "miss + FP adjacent to a missed true", ifelse(fl$nb3 == 1, "miss + FP within 2-3 of a missed true", "miss + FP elsewhere")))))
pr <- do.call(rbind, lapply(split(fl, list(fl$suite, fl$beta_type, fl$rho), drop = TRUE), function(d) { t <- table(factor(d$cat, levels = c("empty MPM", "pure under-selection (miss, no FP)", "miss + FP adjacent to a missed true", "miss + FP within 2-3 of a missed true", "miss + FP elsewhere", "superset of S0 (no miss, has FP)")))
  data.frame(suite = d$suite[1], beta_type = d$beta_type[1], rho = d$rho[1], failed_fits = nrow(d), t(as.matrix(t / nrow(d))), check.names = FALSE) }))
write_tsv(pr, file.path(base, "tables", "e7_proxy_shares_failed_fits.tsv"))
allf <- data.frame(group = c("S1 failed", "S2 failed", "S2 failed, nu>=2.07", "S2 bt1 failed rho>0", "S2 bt2 failed rho>0"),
  failed = c(sum(fl$suite == 1), sum(fl$suite == 2), sum(fl$suite == 2 & fl$nu >= 2.07), sum(fl$suite == 2 & fl$beta_type == "1" & fl$rho > 0), sum(fl$suite == 2 & fl$beta_type == "2" & fl$rho > 0)),
  miss_and_adjacent_FP = c(sum(fl$suite == 1 & fl$nb1 == 1), sum(fl$suite == 2 & fl$nb1 == 1), sum(fl$suite == 2 & fl$nu >= 2.07 & fl$nb1 == 1), sum(fl$suite == 2 & fl$beta_type == "1" & fl$rho > 0 & fl$nb1 == 1), sum(fl$suite == 2 & fl$beta_type == "2" & fl$rho > 0 & fl$nb1 == 1)),
  miss_and_FP_within3 = c(sum(fl$suite == 1 & fl$nb3 == 1), sum(fl$suite == 2 & fl$nb3 == 1), sum(fl$suite == 2 & fl$nu >= 2.07 & fl$nb3 == 1), sum(fl$suite == 2 & fl$beta_type == "1" & fl$rho > 0 & fl$nb3 == 1), sum(fl$suite == 2 & fl$beta_type == "2" & fl$rho > 0 & fl$nb3 == 1)),
  miss_any = c(sum(fl$suite == 1 & fl$nM > 0), sum(fl$suite == 2 & fl$nM > 0), sum(fl$suite == 2 & fl$nu >= 2.07 & fl$nM > 0), sum(fl$suite == 2 & fl$beta_type == "1" & fl$rho > 0 & fl$nM > 0), sum(fl$suite == 2 & fl$beta_type == "2" & fl$rho > 0 & fl$nM > 0)),
  any_FP = c(sum(fl$suite == 1 & fl$nNull > 0), sum(fl$suite == 2 & fl$nNull > 0), sum(fl$suite == 2 & fl$nu >= 2.07 & fl$nNull > 0), sum(fl$suite == 2 & fl$beta_type == "1" & fl$rho > 0 & fl$nNull > 0), sum(fl$suite == 2 & fl$beta_type == "2" & fl$rho > 0 & fl$nNull > 0)))
allf$share_miss_adjacentFP <- allf$miss_and_adjacent_FP / allf$failed; allf$share_miss_FPwithin3 <- allf$miss_and_FP_within3 / allf$failed
allf$share_of_misses_with_adjacent_FP <- allf$miss_and_adjacent_FP / allf$miss_any
write_tsv(allf, file.path(base, "tables", "e7_proxy_summary.tsv"))
options(width = 220); print(e4a); print(e4f); print(e5); print(e6); print(e23); print(e6c, digits = 3); print(allf, digits = 3); print(pr, digits = 3)

# failure composition by regime (failed fits): misses a true predictor / superset of S0 (no miss, >=1 null) / empty MPM
fl$reg <- ifelse(fl$suite == 1, ifelse(fl$snr >= 2, "S1 SNR>=2", "S1 SNR<=1"), ifelse(fl$nu == 6, "S2 nu=6", ifelse(fl$nu == 3.52, "S2 nu=3.52", ifelse(fl$nu == 2.07, "S2 nu=2.07", "S2 nu<=1.22"))))
fc <- do.call(rbind, lapply(split(fl, fl$reg), function(d) data.frame(regime = d$reg[1], failed = nrow(d), share_miss_true = mean(d$nM > 0), share_superset_no_miss = mean(d$nM == 0), share_empty_MPM = mean(d$size == 0), share_any_FP = mean(d$nNull > 0), share_exactly_one_FP_no_miss = mean(d$nM == 0 & d$nNull == 1), med_size_MPM = median(d$size))))
write_tsv(fc, file.path(base, "tables", "e7_failure_composition.tsv")); print(fc, digits = 3)
