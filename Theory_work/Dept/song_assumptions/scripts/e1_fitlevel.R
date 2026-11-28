# e1_fitlevel.R -- E1 fit level: 2x2 tables / AUCs of population margin predictors vs exact recovery (MPM = S0), 13,600 fits.
# Inputs : Engineering theory_checks/p1_per_fit.tsv (READ ONLY), tables/e1_margin_by_setting.tsv (from e1_margin.R)
# Run    : (thread vars exported)  nice -n 19 Rscript scripts/e1_fitlevel.R
suppressMessages(library(data.table))
args <- commandArgs(FALSE); sf <- sub("--file=", "", args[grep("--file=", args)])
base <- normalizePath(file.path(dirname(sf), ".."))
source(file.path(base, "scripts", "pop_lib.R"))
pf <- fread(file.path(ENG, "theory_checks", "p1_per_fit.tsv"), data.table = FALSE)
mg <- read.delim(file.path(base, "tables", "e1_margin_by_setting.tsv"), stringsAsFactors = FALSE)
st <- read_settings(SETTINGS_TSV)
# per-setting pass probability: prod_j P(ncchisq_1(t2_j) > 2*price), t2_j = pop single-deletion t^2  (independence approx.)
pp <- vapply(seq_len(nrow(st)), function(i) { ps <- setting_pop(st[i, ])
  t2 <- vapply(seq_len(ps$s0), function(j) RS(ps, j) / ps$sigma2, 0)
  prod(pchisq(2 * ps$price, df = 1, ncp = t2, lower.tail = FALSE)) }, 0)
mg$passprob <- pp
d <- merge(pf[, c("setting_id", "rep", "suite", "rho", "nu", "beta_type", "n", "success", "gt2price", "gt2price_pop",
                  "ratio_min_t2_price", "min_t2_pop", "price", "margin_mpm")],
           mg[, c("setting_id", "kappa_del", "kappa_multi", "kappa_swap", "kappa_pop", "Lambda_min", "Lambda_min_over_logn", "kappa_adj_pop", "Lambda_adj_min_over_logn", "kappa_full", "kappa_adj_full", "Lambda_full_min_over_logn", "Lambda_adj_full_min_over_logn", "passprob")],
           by = "setting_id")
stopifnot(nrow(d) == 13600)
d$exact <- as.logical(d$success)
d$ratio_pop <- d$min_t2_pop / d$price
d$sample_ratio <- d$ratio_min_t2_price
cat("exact total:", sum(d$exact), " S1:", sum(d$exact[d$suite == 1]), " S2:", sum(d$exact[d$suite == 2]), "\n")

groups <- list(
  all = rep(TRUE, nrow(d)), S1 = d$suite == 1, S2 = d$suite == 2,
  S2_bt1 = d$suite == 2 & d$beta_type == "1", S2_bt2 = d$suite == 2 & d$beta_type == "2",
  S2_nu_ge_2.07 = d$suite == 2 & d$nu >= 2.07, S2_nu_ge_2.07_bt1 = d$suite == 2 & d$nu >= 2.07 & d$beta_type == "1",
  S2_nu_ge_2.07_bt2 = d$suite == 2 & d$nu >= 2.07 & d$beta_type == "2",
  S2_n50 = d$suite == 2 & d$n == 50, S2_n100 = d$suite == 2 & d$n == 100)
for (b in c("1", "2")) for (r in c(0, 0.35, 0.7)) {
  groups[[sprintf("S2_bt%s_rho%s", b, r)]] <- d$suite == 2 & d$beta_type == b & d$rho == r
  groups[[sprintf("S2_bt%s_rho%s_nu_ge_2.07", b, r)]] <- d$suite == 2 & d$beta_type == b & d$rho == r & d$nu >= 2.07 }

preds <- list(P1_sample_mint2_gt_2price = d$gt2price == 1 | d$gt2price == TRUE,
              P1_pop_mint2_gt_2price = d$gt2price_pop == 1 | d$gt2price_pop == TRUE)
for (eta in c(0, 0.1, 0.25, 0.5, 1)) {
  preds[[sprintf("kappa_del_gt_%g", 1 + eta)]] <- d$kappa_del > 1 + eta
  preds[[sprintf("kappa_multi_gt_%g", 1 + eta)]] <- pmin(d$kappa_del, d$kappa_multi) > 1 + eta
  preds[[sprintf("kappa_pop_gt_%g", 1 + eta)]] <- d$kappa_pop > 1 + eta
  preds[[sprintf("kappa_adj_gt_%g", 1 + eta)]] <- d$kappa_adj_pop > 1 + eta
  preds[[sprintf("kappa_full_gt_%g", 1 + eta)]] <- d$kappa_full > 1 + eta
  preds[[sprintf("kappa_adj_full_gt_%g", 1 + eta)]] <- d$kappa_adj_full > 1 + eta }
for (cc in c(-1, 0, 0.25, 0.5, 1, 1.5, 2, 3, 4, 6, 8)) preds[[sprintf("Lambda_min_gt_%g_logn", cc)]] <- d$Lambda_min > cc * log(d$n)
for (cc in c(0, 0.5, 1, 2)) { preds[[sprintf("Lambda_adj_gt_%g_logn", cc)]] <- d$Lambda_adj_min_over_logn > cc; preds[[sprintf("Lambda_adj_full_gt_%g_logn", cc)]] <- d$Lambda_adj_full_min_over_logn > cc }
preds[["passprob_gt_0.5"]] <- d$passprob > 0.5
preds[["passprob_gt_0.25"]] <- d$passprob > 0.25

tt <- do.call(rbind, lapply(names(groups), function(g) { idx <- groups[[g]]
  do.call(rbind, lapply(names(preds), function(pn) { yes <- preds[[pn]][idx]; ex <- d$exact[idx]
    tp <- sum(yes & ex); fp <- sum(yes & !ex); fn <- sum(!yes & ex); tn <- sum(!yes & !ex)
    data.frame(group = g, predictor = pn, n = sum(idx), yes_exact = tp, yes_notexact = fp, no_exact = fn, no_notexact = tn,
      sens = tp / (tp + fn), spec = tn / (tn + fp), P_exact_given_yes = tp / (tp + fp), P_exact_given_no = fn / (fn + tn),
      acc = (tp + tn) / sum(idx), share_yes = (tp + fp) / sum(idx)) })) }))
write_tsv(tt, file.path(base, "tables", "e1_2x2_predictors.tsv"))

scores <- list(kappa_del = d$kappa_del, kappa_pop = d$kappa_pop, kappa_adj_pop = d$kappa_adj_pop, kappa_full = d$kappa_full, kappa_adj_full = d$kappa_adj_full, Lambda_adj_full_min_over_logn = d$Lambda_adj_full_min_over_logn, Lambda_adj_min_over_logn = d$Lambda_adj_min_over_logn, Lambda_min_over_logn = d$Lambda_min_over_logn,
               pop_min_t2_over_price = d$ratio_pop, sample_min_t2_over_price = d$sample_ratio, passprob = d$passprob)
au <- do.call(rbind, lapply(names(groups), function(g) { idx <- groups[[g]]
  data.frame(group = g, n = sum(idx), n_exact = sum(d$exact[idx]),
    do.call(cbind, lapply(names(scores), function(s) setNames(data.frame(auc_mw(scores[[s]][idx], d$exact[idx])), paste0("AUC_", s))))) }))
write_tsv(au, file.path(base, "tables", "e1_auc.tsv"))

# per-setting table with exact share (and Wilson CI), for transition / cell displays
ag <- aggregate(exact ~ setting_id, d, function(x) c(k = sum(x), n = length(x)))
ps_tab <- merge(mg, data.frame(setting_id = ag$setting_id, k = ag$exact[, "k"], nfit = ag$exact[, "n"]), by = "setting_id")
ps_tab$exact_share <- ps_tab$k / ps_tab$nfit
w <- t(mapply(wilson, ps_tab$k, ps_tab$nfit)); ps_tab$wil_lo <- w[, 1]; ps_tab$wil_hi <- w[, 2]
write_tsv(ps_tab, file.path(base, "tables", "e1_setting_exact_vs_margin.tsv"))

# S1 transition: per (n,p) the pair of SNR cells bracketing the transition, with kappa_pop; plus logit interpolation at 50% where bracketed
s1 <- ps_tab[ps_tab$suite == 1, ]
s1 <- s1[order(s1$n, s1$p, s1$snr), c("setting_id", "n", "p", "snr", "kappa_del", "kappa_multi", "kappa_swap", "kappa_pop", "kappa_adj_pop", "kappa_adj_full", "Lambda_min_over_logn", "passprob", "exact_share", "wil_lo", "wil_hi")]
write_tsv(s1, file.path(base, "tables", "e1_s1_cells.tsv"))
# logistic fit exact ~ log(kappa_pop) (fit level), per suite and per S2 group: kappa at P(exact)=0.5 and 0.9
lg <- do.call(rbind, lapply(c("S1", "S2", "S2_bt1", "S2_bt2", "S2_nu_ge_2.07", "S2_nu_ge_2.07_bt1", "S2_nu_ge_2.07_bt2", "S2_bt1_rho0", "S2_bt1_rho0.35", "S2_bt1_rho0.7", "S2_bt2_rho0", "S2_bt2_rho0.35"), function(g) {
  idx <- groups[[g]]; dd <- d[idx, ]; out <- list()
  for (sc in c("kappa_del", "kappa_pop", "kappa_adj_pop", "kappa_adj_full")) {
    f <- try(suppressWarnings(glm(exact ~ log(dd[[sc]]), family = binomial, data = dd)), silent = TRUE)
    if (inherits(f, "try-error")) next
    b <- coef(f); k50 <- exp(-b[1] / b[2]); k90 <- exp((qlogis(0.9) - b[1]) / b[2])
    out[[sc]] <- data.frame(group = g, score = sc, slope = b[2], kappa_at_P50 = unname(k50), kappa_at_P90 = unname(k90),
      aic = AIC(f), n_exact = sum(dd$exact), n = nrow(dd)) }
  do.call(rbind, out) }))
write_tsv(lg, file.path(base, "tables", "e1_logistic_kappa.tsv"))
cat("\n2x2 kappa_pop>1 vs P1 sample vs P1 pop:\n")
print(tt[tt$group %in% c("S1", "S2", "S2_nu_ge_2.07") & tt$predictor %in% c("P1_sample_mint2_gt_2price", "P1_pop_mint2_gt_2price", "kappa_pop_gt_1", "kappa_pop_gt_1.25", "kappa_pop_gt_2", "passprob_gt_0.5"), c("group", "predictor", "yes_exact", "yes_notexact", "no_exact", "no_notexact", "sens", "P_exact_given_yes", "P_exact_given_no")], digits = 3)
cat("\nAUC:\n"); print(au[au$group %in% c("all", "S1", "S2", "S2_nu_ge_2.07", "S2_bt1", "S2_bt2"), ], digits = 3)
cat("\nlogistic:\n"); print(lg, digits = 3)
