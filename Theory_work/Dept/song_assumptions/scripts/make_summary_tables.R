# make_summary_tables.R -- compact S1 / S2 range tables used in the report (reads only tables/*.tsv written by the other scripts)
args <- commandArgs(FALSE); sf <- sub("--file=", "", args[grep("--file=", args)]); base <- normalizePath(file.path(dirname(sf), ".."))
source(file.path(base, "scripts", "pop_lib.R")); T <- function(f) read.delim(file.path(base, "tables", f), stringsAsFactors = FALSE)
rng <- function(x) c(min = min(x), med = median(x), max = max(x))
e3 <- T("e3_condition3.tsv"); e4 <- T("e4_bounded_signal.tsv"); e5 <- T("e5_eigen_floors.tsv"); e0 <- T("e0_regime_by_setting.tsv"); e1 <- T("e1_margin_by_setting.tsv")
by <- function(d, key, cols) do.call(rbind, lapply(split(d, d[[key]]), function(x) { o <- unlist(lapply(cols, function(cn) { r <- rng(x[[cn]]); setNames(r, paste0(cn, ".", names(r))) })); data.frame(group = x[[key]][1], n_settings = nrow(x), t(o)) }))
e3$g <- ifelse(e3$suite == 1, "S1", paste0("S2 rho=", e3$rho)); e4$g <- ifelse(e4$suite == 1, "S1", "S2"); e5$g <- ifelse(e5$suite == 1, "S1", paste0("S2 rho=", e5$rho)); e0$g <- ifelse(e0$suite == 1, "S1", "S2"); e1$g <- ifelse(e1$suite == 1, "S1", "S2")
s3 <- by(e3, "g", c("v_min", "delta_SL", "eps2_n", "eps2_over_delta", "r1_s0_over_delta", "r2_s0_over_delta", "r3_logn_s0_over_delta")); write_tsv(s3, file.path(base, "tables", "summ_E3.tsv"))
s4 <- by(e4, "g", c("max_abs_beta_over_sigma", "min_abs_beta_over_sigma", "betaSigmaBeta_over_sigma2", "beta_min_over_sigma_sqrt_logp_n", "beta_min_over_sigma_sqrt_logn_n")); write_tsv(s4, file.path(base, "tables", "summ_E4.tsv"))
s5 <- by(e5, "g", c("pop_floor_any_T", "pop_lmin_S0", "n_times_floor", "sample_lmin_S0_median", "sample_greedy_m1_median", "sample_greedy_m2_median", "sample_greedy_m1_over_floor", "sample_greedy_m2_over_floor")); write_tsv(s5, file.path(base, "tables", "summ_E5.tsv"))
s0 <- by(e0, "g", c("A", "s0logp_n", "logp_n", "logp2_n", "loglogp_logn", "eps_n", "sqrt_logn_n", "kappa_eff_SLcorS1", "logp_over_sqrtn")); write_tsv(s0, file.path(base, "tables", "summ_E0.tsv"))
e1$gr <- ifelse(e1$suite == 1, "S1", paste0("S2 bt", e1$beta_type, " rho=", e1$rho))
s1 <- by(e1, "gr", c("kappa_del", "kappa_multi", "kappa_swap", "kappa_pop", "kappa_adj_pop", "kappa_full", "kappa_adj_full", "Lambda_min_over_logn", "e2_over_eps2")); write_tsv(s1, file.path(base, "tables", "summ_E1_E2.tsv"))
# shares of settings with kappa_pop > 1, kappa_del > 1, and exact recovery share in them
e1x <- T("e1_setting_exact_vs_margin.tsv"); e1x$suiteg <- ifelse(e1x$suite == 1, "S1", paste0("S2 bt", e1x$beta_type))
sh <- do.call(rbind, lapply(split(e1x, e1x$suiteg), function(x) data.frame(group = x$suiteg[1], n_settings = nrow(x), n_kdel_gt1 = sum(x$kappa_del > 1), n_kpop_gt1 = sum(x$kappa_pop > 1), n_kadj_gt1 = sum(x$kappa_adj_pop > 1), n_kadjfull_gt1 = sum(x$kappa_adj_full > 1), n_kadjfull_gt1p25 = sum(x$kappa_adj_full > 1.25), n_kadjfull_gt1_but_exact_lt_0.5 = sum(x$kappa_adj_full > 1 & x$exact_share < 0.5), n_kadjfull_lt1_exact_gt_0.05 = sum(x$kappa_adj_full < 1 & x$exact_share > 0.05), n_exact_share_gt_0.5 = sum(x$exact_share > 0.5),
  n_kpop_gt1_but_exact_lt_0.5 = sum(x$kappa_pop > 1 & x$exact_share < 0.5), n_kpop_lt1_exact_gt_0.05 = sum(x$kappa_pop < 1 & x$exact_share > 0.05)))); write_tsv(sh, file.path(base, "tables", "summ_E1_setting_counts.tsv"))
options(width = 250); for (nm in c("summ_E0", "summ_E3", "summ_E4", "summ_E5", "summ_E1_E2", "summ_E1_setting_counts")) { cat("\n##", nm, "\n"); print(T(paste0(nm, ".tsv")), digits = 3) }
