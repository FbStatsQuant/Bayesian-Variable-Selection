# metrics_smc.R -- SMC-BVS accuracy against the exact posterior (low p) and the truth.
# One row per SMC fit (main fit rep = 0, repeat seeds rep = 1..) -> case_smc_accuracy.csv. Definitions: METRICS.md.

LOG005 <- log(0.05)
FLAG_NAMES <- c("escalated", "checks_failed_final", "E1", "E2", "E3", "low_ess", "cut_group", "local_limit", "grid_unconverged")
EVENT_NAMES <- c("hpm_ne_exact", "mpm_ne_exact", "lb_violated", "e_gt_2se")

pip_err_stats <- function(hat, ex, S0, prefix) {
  out <- list()
  nm <- c("max", "mean", "mean_true", "mean_null", "max_true", "max_null")
  if (is.null(hat) || is.null(ex) || length(hat) != length(ex) || anyNA(hat)) {
    for (n in nm) out[[paste0(prefix, "_", n)]] <- NA_real_
    return(out)
  }
  err <- abs(as.numeric(hat) - as.numeric(ex)); tr <- seq_along(err) %in% S0
  out[[paste0(prefix, "_max")]] <- max(err); out[[paste0(prefix, "_mean")]] <- mean(err)
  out[[paste0(prefix, "_mean_true")]] <- if (any(tr)) mean(err[tr]) else NA_real_
  out[[paste0(prefix, "_mean_null")]] <- if (any(!tr)) mean(err[!tr]) else NA_real_
  out[[paste0(prefix, "_max_true")]] <- if (any(tr)) max(err[tr]) else NA_real_
  out[[paste0(prefix, "_max_null")]] <- if (any(!tr)) max(err[!tr]) else NA_real_
  out
}
pip_island_stats <- function(M, ex, prefix, R = 4L) {
  out <- list()
  for (r in seq_len(R)) out[[sprintf("%s_isl%d_max", prefix, r)]] <- NA_real_
  out[[paste0(prefix, "_isl_max_mean")]] <- NA_real_; out[[paste0(prefix, "_isl_mean_mean")]] <- NA_real_
  if (is.null(M) || is.null(ex) || nrow(M) != length(ex) || anyNA(M)) return(out)
  err <- abs(M - ex)
  mx <- apply(err, 2L, max); mn <- colMeans(err)
  for (r in seq_len(min(R, ncol(M)))) out[[sprintf("%s_isl%d_max", prefix, r)]] <- mx[r]
  out[[paste0(prefix, "_isl_max_mean")]] <- mean(mx); out[[paste0(prefix, "_isl_mean_mean")]] <- mean(mn)
  out
}
eq_or_na <- function(a, b, ok = TRUE) if (!ok || is.null(a) || is.null(b)) NA else same_set(a, b)

# sm = extract_smc(); es = exact_scale() or NULL; S0 = true support; scorer = make_scorer(X, y) or NULL
smc_accuracy_row <- function(sm, es, S0, scorer = NULL) {
  ok <- isTRUE(sm$ok); has_ex <- !is.null(es); ev <- isTRUE(sm$evidence_ok); isl <- isTRUE(sm$islands_ok); hp <- isTRUE(sm$hpm_ok)
  R <- 4L
  lz_ex <- if (has_ex) es$log_Z else NA_real_
  e <- if (ev && has_ex) sm$log_Z - lz_ex else NA_real_
  er <- rep(NA_real_, R)
  if (isl && has_ex && length(sm$log_Z_r)) { k <- min(R, length(sm$log_Z_r)); er[seq_len(k)] <- (sm$log_Z_r - lz_ex)[seq_len(k)] }
  isl_sd <- if (isl && length(sm$log_Z_r) == 4L) stats::sd(sm$log_Z_r) else NA_real_   # four valid islands required
  se <- isl_sd / 2
  lb_cover <- if (is.na(e)) NA else (sm$log_Z + LOG005 <= lz_ex)
  # F values
  F_truth <- if (!is.null(scorer)) scorer$F(S0) else NA_real_
  F_exact_hpm <- if (has_ex) es$hpm_F else NA_real_
  F_smc_hpm <- if (!is.null(scorer) && !is.null(sm$hpm)) scorer$F(sm$hpm) else if (hp) sm$hpm_F else NA_real_
  hpm_F_mismatch <- if (!is.null(scorer) && is.finite(sm$hpm_F) && is.finite(F_smc_hpm)) abs(sm$hpm_F - F_smc_hpm) else NA_real_
  hpm_eq_ex <- eq_or_na(sm$hpm, if (has_ex) es[["hpm"]], hp && has_ex)
  hpm_eq_tr <- eq_or_na(sm$hpm, S0, hp)
  mpm_eq_ex <- eq_or_na(sm$mpm, if (has_ex) es[["mpm"]], ok && has_ex && !is.null(sm$mpm))
  mpmp_eq_ex <- eq_or_na(sm$mpm_plain, if (has_ex) es[["mpm"]], ok && has_ex && !is.null(sm$mpm_plain))
  miss <- if (!hp || is.na(F_truth) || is.na(F_smc_hpm) || is.null(sm$hpm)) NA_character_ else
    if (same_set(sm$hpm, S0)) "hit" else if (F_truth > F_smc_hpm) "search_miss" else "posterior_miss"
  cov_log <- if (has_ex && !is.na(sm$log_mass_scored)) sm$log_mass_scored - lz_ex else NA_real_
  row <- c(list(
    case_id = sm$case_id, dataset_id = sm$dataset_id, p = sm$p, scenario = sm$scenario, replicate = sm$replicate, scale_key = sm$scale_key,
    rep = sm$rep, method_seed = sm$method_seed, native_status = sm$native_status, ok = ok, evidence_ok = ev, islands_ok = isl, hpm_ok = hp, rb_ok = isTRUE(sm$rb_ok), plain_ok = isTRUE(sm$plain_ok), has_exact = has_ex,
    kept_match = if (!is.null(sm$kept) && has_ex) identical(sort(as.integer(sm$kept)), as.integer(es$kept)) else NA,
    log_Z_hat = sm$log_Z, log_Z_exact = lz_ex, e = e, abs_e = abs(e), rel_err = if (is.na(e)) NA_real_ else expm1(e),
    e_isl1 = er[1], e_isl2 = er[2], e_isl3 = er[3], e_isl4 = er[4],
    lb_cover = lb_cover, lb_violated = if (is.na(lb_cover)) NA else !lb_cover,
    lb_native_diff = if (ev && is.finite(sm$log_Z_lower95)) sm$log_Z_lower95 - (sm$log_Z + LOG005) else NA_real_,
    isl_sd = isl_sd, se = se, e_over_se = if (is.na(e) || !is.finite(se) || se == 0) NA_real_ else abs(e) / se,
    within2se = if (is.na(e) || is.na(se)) NA else abs(e) <= 2 * se, e_gt_2se = if (is.na(e) || is.na(se)) NA else abs(e) > 2 * se,
    hpm = enc_support(sm$hpm), hpm_k = if (is.null(sm$hpm)) NA_integer_ else length(sm$hpm),
    exact_hpm = if (has_ex) enc_support(es[["hpm"]]) else NA_character_,
    hpm_eq_exact = hpm_eq_ex, hpm_ne_exact = if (is.na(hpm_eq_ex)) NA else !hpm_eq_ex,
    exact_hpm_eq_truth = if (has_ex && !is.null(es[["hpm"]])) same_set(es[["hpm"]], S0) else NA, hpm_eq_truth = hpm_eq_tr,
    F_exact_hpm = F_exact_hpm, F_smc_hpm = F_smc_hpm, F_gap = if (hp && has_ex) F_exact_hpm - F_smc_hpm else NA_real_, hpm_F_mismatch = hpm_F_mismatch,
    F_truth = F_truth, log_truth_mass = if (has_ex) F_truth - lz_ex else NA_real_, truth_mass = if (has_ex) exp(F_truth - lz_ex) else NA_real_,
    truth_minus_smc_hpm = if (hp) F_truth - F_smc_hpm else NA_real_, truth_minus_exact_hpm = if (has_ex) F_truth - F_exact_hpm else NA_real_,
    miss_class = miss,
    mpm_rb_eq_exact = mpm_eq_ex, mpm_ne_exact = if (is.na(mpm_eq_ex)) NA else !mpm_eq_ex, mpm_plain_eq_exact = mpmp_eq_ex,
    exact_mpm_eq_truth = if (has_ex && !is.null(es[["mpm"]])) same_set(es[["mpm"]], S0) else NA,
    mpm_rb_eq_truth = eq_or_na(sm$mpm, S0, ok), mpm_plain_eq_truth = eq_or_na(sm$mpm_plain, S0, ok && !is.null(sm$mpm_plain))),
    pip_err_stats(sm$pip_rb, if (has_ex) es$pip, S0, "rb"), pip_island_stats(sm$pip_rb_r, if (has_ex) es$pip, "rb"),
    pip_err_stats(sm$pip_plain, if (has_ex) es$pip, S0, "plain"), pip_island_stats(sm$pip_plain_r, if (has_ex) es$pip, "plain"),
    list(escalated = sm$escalated, checks_failed_final = if (is.na(sm$checks_passed_final)) NA else !sm$checks_passed_final,
         E1 = sm$E1, E2 = sm$E2, E3 = sm$E3, low_ess = sm$low_ess, cut_group = sm$cut_group, local_limit = sm$local_limit,
         grid_unconverged = sm$grid_unconverged, near_tie_truncated = sm$near_tie_truncated, local_certified = sm$local_certified,
         runtime_s = sm$runtime_s, score_fresh = sm$score_fresh, score_logical = sm$score_logical, n_stages_final = sm$n_stages_final,
         min_ess = sm$min_ess, tier = sm$tier, n_distinct_scored = sm$n_distinct_scored,
         log_mass_scored = sm$log_mass_scored, log_scored_coverage = cov_log,
         scored_coverage = if (is.na(cov_log)) NA_real_ else exp(cov_log)))
  data.table::as.data.table(lapply(row, function(v) if (is.null(v)) NA else v))
}

# Seed-to-seed stability per case. `sms` = ALL attempted fits of the case (main + repeats, including failed ones).
# Eligible fits = completed with usable fields, distinct method seeds; every statistic needs >= 2 eligible seeds for ITS field and reports its own count.
stability_row <- function(sms) {
  if (!length(sms)) return(NULL)
  seeds <- vapply(sms, function(s) s$method_seed, 0)
  if (anyDuplicated(seeds[!is.na(seeds)])) stop("repeat fits of case ", sms[[1L]]$case_id, " share a method seed: ", paste(seeds, collapse = ","))
  known <- !is.na(seeds)                    # a fit with an unknown seed identity cannot be shown to be a distinct seed: excluded
  done <- Filter(function(s) isTRUE(s$ok) && !is.na(s$method_seed), sms)
  ev <- Filter(function(s) isTRUE(s$evidence_ok), done); hp <- Filter(function(s) isTRUE(s$hpm_ok), done)
  rb <- Filter(function(s) isTRUE(s$rb_ok), done); pl <- Filter(function(s) isTRUE(s$plain_ok), done)
  hpm_agree <- NA_real_; hh <- vapply(hp, function(s) enc_support(s$hpm), "")
  if (length(hp) >= 2L) { cmb <- utils::combn(length(hp), 2L); hpm_agree <- mean(hh[cmb[1L, ]] == hh[cmb[2L, ]]) }
  maxsd <- function(L, f) if (length(L) >= 2L) max(apply(do.call(cbind, lapply(L, f)), 1L, stats::sd)) else NA_real_
  data.table::data.table(case_id = sms[[1L]]$case_id, dataset_id = sms[[1L]]$dataset_id, p = sms[[1L]]$p, scenario = sms[[1L]]$scenario,
    replicate = sms[[1L]]$replicate, scale_key = sms[[1L]]$scale_key, n_attempted = length(sms), n_unknown_seed = sum(!known), n_completed = length(done),
    n_evidence = length(ev), n_hpm = length(hp), n_rb = length(rb), n_plain = length(pl),
    sd_log_Z = if (length(ev) >= 2L) stats::sd(vapply(ev, function(s) s$log_Z, 0)) else NA_real_,
    hpm_agreement = hpm_agree, n_distinct_hpm = if (length(hp)) length(unique(hh)) else NA_integer_,
    max_pip_sd_rb = maxsd(rb, function(s) s$pip_rb), max_pip_sd_plain = maxsd(pl, function(s) s$pip_plain))
}

# 2x2 of each flag against each error event. dt = case_smc_accuracy rows (ok fits with exact). Fits with NA in flag or event are dropped for that cell.
flag_error_table <- function(dt) {
  dt <- dt[ok == TRUE & has_exact == TRUE]
  rows <- list()
  for (fl in FLAG_NAMES) for (ev in EVENT_NAMES) {
    f <- as.logical(dt[[fl]]); v <- as.logical(dt[[ev]]); keep <- !is.na(f) & !is.na(v)
    f <- f[keep]; v <- v[keep]
    a <- sum(f & v); b <- sum(f & !v); c <- sum(!f & v); d <- sum(!f & !v)
    rows[[length(rows) + 1L]] <- data.table::data.table(flag = fl, event = ev, n = length(f), flag_and_event = a, flag_no_event = b,
      noflag_event = c, noflag_noevent = d, sensitivity = if (a + c > 0) a / (a + c) else NA_real_,
      specificity = if (b + d > 0) d / (b + d) else NA_real_, ppv = if (a + b > 0) a / (a + b) else NA_real_)
  }
  data.table::rbindlist(rows)
}

# Spearman between |e| and SE across fits (per p x scale), plus the 2-SE rate.
se_calibration_table <- function(dt) {
  dt <- dt[ok == TRUE & has_exact == TRUE & rep == 0L & !is.na(se)]
  dt[, {
    sp <- if (.N >= 3L && length(unique(se)) > 1L && length(unique(abs_e)) > 1L) suppressWarnings(stats::cor(abs_e, se, method = "spearman")) else NA_real_
    list(n = .N, spearman_abs_e_se = sp, median_ratio = stats::median(e_over_se, na.rm = TRUE), mean_within2se = mean(within2se, na.rm = TRUE))
  }, by = .(p, scale_key)]
}
