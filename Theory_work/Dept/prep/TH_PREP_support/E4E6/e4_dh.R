# E4: Hellinger distance to the truth, random design x ~ N(0, Sigma_AR1), raw scale (unit-variance columns).
# d_H^2 = 1 - sqrt(2 s1 s2/(s1^2+s2^2)) * (1 + tau^2/(2(s1^2+s2^2)))^(-1/2), tau^2 = delta' Sigma delta.
suppressMessages(library(data.table))
TC <- "/home/fb31/Bayesian-Variable-Selection/_local/engineering/reports/S1S2/theory_checks"
H  <- "/home/fb31/BVS-wt/P1M/Experiments/S1S2"
source(file.path(H, "harness/generate.R"))
st <- read.delim(file.path(H, "specs/settings.tsv"), colClasses = c(setting_id = "character", beta_type = "character"))
pf <- fread(file.path(TC, "p2_per_fit.tsv"))
bb <- fread(cmd = paste("zcat", file.path(TC, "p2_betabar_sparse.tsv.gz")))
tm <- fread(cmd = paste("zcat", file.path(TC, "p2_top50_models.tsv.gz")), select = c("setting_id","rep","weight_renorm_top50","Esig2_S_raw","beta_scale"))
bb[, sdj := ifelse(abs(betabar_raw) > 1e-12, betabar_std / betabar_raw, NA_real_)]
dh <- function(d, S, rho, s2a, s2b) {          # d: delta values on indices S
  tau2 <- if (!length(S)) 0 else if (rho == 0) sum(d^2) else sum(outer(d, d) * rho^abs(outer(S, S, "-")))
  v <- s2a + s2b; sqrt(max(0, 1 - sqrt(2 * sqrt(s2a * s2b) / v) * (1 + tau2 / (2 * v))^-0.5))
}
setkey(bb, setting_id, rep); setkey(tm, setting_id, rep)
B <- lapply(split(st, st$setting_id), gen_beta)
res <- pf[status == "ok", {
  sid <- setting_id; rp <- rep; row <- st[st$setting_id == sid, ]; b0 <- B[[setting_id]]; S0 <- which(b0 != 0); rho <- row$rho; s2 <- sigma2_true
  x <- bb[.(sid, rp)]
  # plug-in: betabar_raw, E[sigma2|y]_list
  S <- union(S0, x$j); bh <- numeric(length(S)); bh[match(x$j, S)] <- x$betabar_raw
  d_plug <- dh(bh - b0[S], S, rho, Esig2_list_raw, s2)
  # mixture over top-50: E_post d_H with per-model (beta_S, E[sigma2|S]); raw = std / sd_j (sd_j from betabar file, else 1)
  m <- tm[.(sid, rp)]; sdmap <- setNames(x$sdj, x$j)
  dm <- vapply(seq_len(nrow(m)), function(k) {
    bs <- m$beta_scale[k]; if (is.na(bs) || bs == "") { J <- integer(0); v <- numeric(0) } else {
      kv <- strsplit(strsplit(bs, ",")[[1]], ":"); J <- as.integer(vapply(kv, `[`, "", 1)); v <- as.numeric(vapply(kv, `[`, "", 2)) }
    sd <- sdmap[as.character(J)]; sd[is.na(sd)] <- 1; v <- v / sd
    SS <- union(S0, J); bh <- numeric(length(SS)); bh[match(J, SS)] <- v
    dh(bh - b0[SS], SS, rho, m$Esig2_S_raw[k], s2) }, 0)
  d_mix <- sum(m$weight_renorm_top50 * dm) / sum(m$weight_renorm_top50)
  .(suite = row$suite, n = n, p = p, rho = rho, snr = row$snr, nu = row$nu, beta_type = row$beta_type, exact = exact,
    eps_n = sqrt(row$s0 * log(p) / n), d_plug = d_plug, d_mix = d_mix)
}, by = .(setting_id, rep)]
fwrite(res, "e4_dh_per_fit.tsv", sep = "\t")
res[, grp := ifelse(suite == 1, sprintf("S1 n=%d p=%d SNR=%s", n, p, snr), sprintf("S2 n=%d rho=%s bt=%s nu=%s", n, rho, beta_type, nu))]
agg <- res[, .(fits = .N, exact = mean(exact), eps_n = eps_n[1], med_d_mix = median(d_mix), q90_d_mix = quantile(d_mix, .9),
               med_d_plug = median(d_plug), med_ratio = median(d_mix / eps_n),
               med_d_mix_exact = if (any(exact)) median(d_mix[exact]) else NA_real_, med_d_mix_fail = if (any(!exact)) median(d_mix[!exact]) else NA_real_),
           by = .(suite, n, p, rho, beta_type, snr, nu)][order(suite, n, p, rho, beta_type, snr, nu)]
fwrite(agg, "e4_dh_by_setting.tsv", sep = "\t")
options(width = 220); print(agg[, lapply(.SD, function(z) if (is.numeric(z)) signif(z, 3) else z)], nrows = 200)
