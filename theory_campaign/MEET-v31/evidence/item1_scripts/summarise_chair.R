# summarise.R -- ABL-START: per-fit and paired summaries from $ABL_WORK/fits/*.rds -> results/per_fit.csv.
`%||%` <- function(a, b) if (is.null(a)) b else a
# Reference per design (leave-one-arm-out): for arm X, the islands of all OTHER completed arms of the same design are
# pooled: log Zref = log mean_r Zhat_r (each island's Zhat_r is unbiased for Z, whatever its start), PIPref = Zhat-weighted
# mean of island PIPs. "best-known mode" = argmax F over all arms' HPMs and S0 (F = log prior + log m).
# Masking proxy (operational definition of this run): log2 A0 = log2[ pi(S^) / pi0(S^) ] at the best-known mode S^,
# pi(S^) = exp(F(S^) - log Zref_all).
W <- Sys.getenv("ABL_WORK", "/home/fb31/abl_work")
fs <- list.files(file.path(W, "fits"), pattern = "\\.rds$", full.names = TRUE)
fits <- lapply(fs, readRDS)
key <- vapply(fits, function(f) paste(f$id, f$scale), "")
lse <- function(x) { m <- max(x); m + log(sum(exp(x - m))) }
rows <- list()
for (k in unique(key)) {
  fk <- fits[key == k]; arms <- vapply(fk, function(f) f$arm, "")
  ok <- vapply(fk, function(f) length(f$log_Z_r) > 0, TRUE)
  allLZ <- unlist(lapply(fk[ok], function(f) f$log_Z_r))
  lzall <- if (length(allLZ)) lse(allLZ) - log(length(allLZ)) else NA
  # best-known mode
  cand <- c(lapply(fk, function(f) list(S = f$hpm, F = f$hpm_F)), list(list(S = fk[[1]]$S0, F = fk[[1]]$F_S0)))
  Fs <- vapply(cand, function(x) if (is.null(x$F) || is.na(x$F)) -Inf else x$F, 0)
  best <- cand[[which.max(Fs)]]
  for (i in seq_along(fk)) {
    f <- fk[[i]]
    oth <- fk[ok & arms != f$arm]
    lz <- unlist(lapply(oth, function(g) g$log_Z_r)); lzref <- if (length(lz)) lse(lz) - log(length(lz)) else NA
    P <- do.call(cbind, lapply(oth, function(g) g$pip_r))
    pref <- if (length(lz)) { w <- exp(lz - max(lz)); as.vector(P %*% (w / sum(w))) } else NULL
    cal <- f$cal; t0 <- if (!is.null(cal)) cal$tiers[[1]] else NULL; tl <- if (!is.null(cal)) cal$tiers[[length(cal$tiers)]] else NULL
    fresh_cal <- if (!is.null(cal$ledger_counts$fresh)) sum(unlist(cal$ledger_counts$fresh)) else NA
    fresh_fin <- if (!is.null(f$score_counts$fresh)) sum(unlist(f$score_counts$fresh)) else NA
    lpb <- NA  # log pi0(best-known mode) needs the setup; recorded only when the arm's HPM is the best mode
    if (identical(f$hpm, best$S)) lpb <- f$log_pi0_hpm
    rows[[length(rows) + 1]] <- data.frame(id = f$id, scale = f$scale, scen = sub("^[^_]*_(S[0-9]).*", "\\1", f$id),
      arm = f$arm, seed = f$seed, status = f$status, tier = f$tier, T_final = f$T_final,
      pilot_T0 = if (!is.null(t0)) t0$pilot_T else NA, rebuilds0 = if (!is.null(t0)) t0$rebuilds else NA,
      pilot_T_last = if (!is.null(tl)) tl$pilot_T else NA, rebuilds_last = if (!is.null(tl)) tl$rebuilds else NA,
      rebuilds_total = if (!is.null(cal)) sum(vapply(cal$tiers, function(a) as.numeric(a$rebuilds %||% NA), 0)) else NA,
      grid_T_all = if (!is.null(cal)) paste(unlist(lapply(cal$tiers, function(a) a$grid_T)), collapse = "/") else NA,
      escalated = isTRUE(cal$escalated), fresh_cal = fresh_cal, fresh_final = fresh_fin,
      sec_setup = f$timings$setup_total %||% NA, sec_cal = f$timings$calibration %||% NA, sec_final = f$timings$final %||% NA,
      sec_total = f$wall, N = f$N %||% NA,
      log_Z = f$log_Z %||% NA, sd_logZ_r = if (length(f$log_Z_r)) sd(f$log_Z_r) else NA,
      range_logZ_r = if (length(f$log_Z_r)) diff(range(f$log_Z_r)) else NA,
      log_Zref_loo = lzref, dlogZ = (f$log_Z %||% NA) - lzref, log_Zref_all = lzall, n_ref_islands = length(lz),
      pip_eq_maxerr = if (!is.null(pref) && !is.null(f$pip_eq)) max(abs(f$pip_eq - pref)) else NA,
      pip_eq_l1 = if (!is.null(pref) && !is.null(f$pip_eq)) sum(abs(f$pip_eq - pref)) else NA,
      pip_zw_maxerr = if (!is.null(pref) && !is.null(f$pip_zw)) max(abs(f$pip_zw - pref)) else NA,
      pip_zw_l1 = if (!is.null(pref) && !is.null(f$pip_zw)) sum(abs(f$pip_zw - pref)) else NA,
      hpm_size = length(f$hpm), hpm_eq_S0 = identical(f$hpm, f$S0), hpm_eq_best = identical(f$hpm, best$S),
      hpm_F = f$hpm_F %||% NA, best_F = max(Fs), F_S0 = f$F_S0, best_is_S0 = identical(best$S, f$S0),
      hpm_from = paste(unlist(f$hpm_provenance[c("phase", "mechanism")]), collapse = ":"),
      log10_pi0_S0 = f$log_pi0_S0 / log(10), log10_pi0_hpm = f$log_pi0_hpm / log(10),
      log2_A0 = if (!is.na(lpb)) (max(Fs) - lzall - lpb) / log(2) else NA,
      ess_min_frac = if (length(f$ess_min)) min(f$ess_min) / f$N else NA,
      E1 = isTRUE(f$flags$E1), E2 = isTRUE(f$flags$E2), E3 = isTRUE(f$flags$E3), stringsAsFactors = FALSE)
  }
}
`%||%` <- function(a, b) if (is.null(a)) b else a
d <- do.call(rbind, rows); d <- d[order(d$scen, d$id, d$scale, d$arm), ]
out <- Sys.getenv("ABL_OUT")
write.csv(d, out, row.names = FALSE)
print(d[, c("id", "scale", "arm", "status", "tier", "T_final", "pilot_T0", "rebuilds_total", "fresh_cal", "fresh_final",
            "sec_cal", "sec_final", "sd_logZ_r", "dlogZ", "pip_eq_maxerr", "hpm_eq_S0", "hpm_eq_best", "log10_pi0_S0")], digits = 3)
