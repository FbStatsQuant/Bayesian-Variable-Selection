# tables.R -- the four headline tables (charter 1) and the HEADLINE.md writer. Everything else stays in CSVs.
# DENOMINATORS (review findings 1, 4, 5): the unit is the EXPECTED CASE (roster = inputs manifest x scales), never an observed file.
# A missing or failed main SMC fit, a missing exact reference, a missing benchmark result stay in every denominator: rates divide by n_cases
# ("not equal"/"not recovered"); error statistics (bias, RMSE, ...) are conditional on the fits that supply the field, and the number of
# contributing fits is shown next to them (n_evidence, n_rb, n_plain). The counts of missing / failed fits and missing references are shown in H1-H3.

with_pooled <- function(dt) { a <- data.table::copy(dt); a[, scenario := as.character(scenario)]; b <- data.table::copy(a); b[, scenario := "all"]; data.table::rbindlist(list(a, b)) }
pct <- function(x, den) if (den > 0) 100 * sum(x, na.rm = TRUE) / den else NA_real_

ACC_NUM <- c("e", "rb_max", "rb_mean_true", "rb_mean_null", "plain_max", "plain_mean_true", "plain_mean_null")
ACC_LGL <- c("ok", "lb_cover", "hpm_eq_exact", "hpm_eq_truth", "mpm_rb_eq_exact", "mpm_plain_eq_exact")

# expected: roster (case_id, dataset_id, p, scenario, replicate, scale_key); ref: case_reference (case_id, has_exact, exact_hpm_eq_truth, ...);
# acc: case_smc_accuracy (main fit = rep 0 may be absent for any case, or acc may be empty)
case_base <- function(acc, expected, ref) {
  m <- data.table::copy(expected)
  if (!is.null(ref) && nrow(ref)) m <- merge(m, ref[, .(case_id, has_exact, exact_hpm_eq_truth)], by = "case_id", all.x = TRUE) else { m[, has_exact := FALSE]; m[, exact_hpm_eq_truth := NA] }
  m[is.na(has_exact), has_exact := FALSE]
  if (!is.null(acc) && nrow(acc) && anyDuplicated(acc[rep == 0L, case_id])) stop("duplicate main-fit rows in the accuracy table: ", paste(unique(acc[rep == 0L, case_id][duplicated(acc[rep == 0L, case_id])]), collapse = ", "))
  if (anyDuplicated(expected$case_id)) stop("duplicate case ids in the roster")
  a <- if (!is.null(acc) && nrow(acc)) acc[rep == 0L, c("case_id", intersect(c(ACC_NUM, ACC_LGL), names(acc))), with = FALSE] else data.table::data.table(case_id = character(0))
  for (nm in ACC_NUM) if (!nm %in% names(a)) a[, (nm) := NA_real_]
  for (nm in ACC_LGL) if (!nm %in% names(a)) a[, (nm) := NA]
  a[, smc_main_found := TRUE]
  m <- merge(m, a, by = "case_id", all.x = TRUE)
  m[is.na(smc_main_found), smc_main_found := FALSE]
  m[is.na(ok), ok := FALSE]
  m[, smc_state := ifelse(!smc_main_found, "missing", ifelse(ok, "ok", "failed"))]
  m
}
.avail <- function(m) list(n_cases = nrow(m), n_smc_missing = sum(m$smc_state == "missing"), n_smc_failed = sum(m$smc_state == "failed"), n_exact_missing = sum(!m$has_exact))

H1_logZ <- function(acc, expected, ref) {
  m <- with_pooled(case_base(acc, expected, ref))
  m[, {
    ev <- !is.na(e)
    c(.avail(.SD), list(n_evidence = sum(ev), bias = safe_mean(e), rmse = if (any(ev)) sqrt(mean(e[ev]^2)) else NA_real_,
         median_abs_e = if (any(ev)) stats::median(abs(e[ev])) else NA_real_, p90_abs_e = q90(abs(e[ev])),
         lb_coverage = if (any(ev)) mean(lb_cover[ev]) else NA_real_))
  }, by = .(p, scenario, scale_key), .SDcols = c("smc_state", "has_exact")][order(p, scale_key, scenario)]
}
H2_hpm <- function(acc, expected, ref) {
  m <- with_pooled(case_base(acc, expected, ref))
  m[, c(.avail(.SD), list(
           pct_smc_hpm_eq_exact = pct(hpm_eq_exact %in% TRUE, .N),
           pct_exact_hpm_eq_truth = pct(exact_hpm_eq_truth %in% TRUE, .N),
           pct_smc_hpm_eq_truth = pct(hpm_eq_truth %in% TRUE, .N))),
    by = .(p, scenario, scale_key), .SDcols = c("smc_state", "has_exact")][order(p, scale_key, scenario)]
}
H3_pip <- function(acc, expected, ref) {
  m <- with_pooled(case_base(acc, expected, ref))
  m[, {
    rbv <- !is.na(rb_max); plv <- !is.na(plain_max)
    c(.avail(.SD), list(n_rb = sum(rbv), n_plain = sum(plv),
         rb_mean_max_err = safe_mean(rb_max), rb_p90_max_err = q90(rb_max),
         rb_mean_err_true = safe_mean(rb_mean_true), rb_mean_err_null = safe_mean(rb_mean_null),
         plain_mean_max_err = safe_mean(plain_max), plain_p90_max_err = q90(plain_max),
         plain_mean_err_true = safe_mean(plain_mean_true), plain_mean_err_null = safe_mean(plain_mean_null),
         pct_mpm_rb_eq_exact = pct(mpm_rb_eq_exact %in% TRUE, .N), pct_mpm_plain_eq_exact = pct(mpm_plain_eq_exact %in% TRUE, .N)))
  }, by = .(p, scenario, scale_key), .SDcols = c("smc_state", "has_exact")][order(p, scale_key, scenario)]
}
# H4: exact recovery per p x c x method/rule x scenario and pooled, ALL-SAVED and PASSING-ONLY (master IV.1.3: both with the same fixed denominator).
# Passing-only = exact AND not flagged (diag_flag TRUE removes it from the count; the denominator stays the number of expected cases).
H4_recovery <- function(sel) {
  s <- sel[in_expected == TRUE & in_h4 == TRUE]
  with_pooled(s)[, list(n_cases = .N, n_exact = sum(exact == TRUE, na.rm = TRUE), n_exact_passing = sum(exact == TRUE & !(diag_flag %in% TRUE), na.rm = TRUE),
                        n_flagged = sum(diag_flag %in% TRUE), n_failed = sum(error_type == "failed"),
                        recovery = sprintf("%d/%d", sum(exact == TRUE, na.rm = TRUE), .N),
                        recovery_passing = sprintf("%d/%d", sum(exact == TRUE & !(diag_flag %in% TRUE), na.rm = TRUE), .N)),
                 by = .(p, scale_key, method_id, rule_id, scenario)][order(p, scale_key, method_id, rule_id, scenario)]
}

md_table <- function(df, digits = 3) {
  df <- as.data.frame(df, stringsAsFactors = FALSE)
  fmt <- function(v) if (is.numeric(v)) vapply(v, function(x) if (is.na(x)) "NA" else format(signif(x, digits), scientific = FALSE, trim = TRUE), "") else ifelse(is.na(v), "NA", as.character(v))
  body <- vapply(seq_len(nrow(df)), function(i) paste0("| ", paste(vapply(df, function(col) fmt(col)[i], ""), collapse = " | "), " |"), "")
  c(paste0("| ", paste(names(df), collapse = " | "), " |"), paste0("|", paste(rep("---", ncol(df)), collapse = "|"), "|"), body)
}

write_headline <- function(H1, H2, H3, H4, path, title = "Regime L (p << n) headline answers", roster_note = NULL) {
  L <- c(paste("#", title), "", roster_note, if (!is.null(roster_note)) "",
         "Unit: the main SMC fit of each EXPECTED case (inputs manifest x scales) against the exact posterior (full enumeration). Missing or failed fits and missing references stay in every denominator and are counted in the tables (miss = no main fit, fail = failed fit, no exact = no ready exact reference).", "",
         "## H1. Is the evidence estimate accurate?", "",
         "e = log Z-hat - log Z (same standardised working-model scale), over the n_evid cases with a valid fit and exact reference. Lower-bound coverage = share of those n_evid fits with log Z-hat + log 0.05 <= log Z.", "")
  for (pp in sort(unique(H1$p))) for (sk in sort(unique(H1$scale_key))) {
    d <- H1[p == pp & scale_key == sk, .(scenario, n_cases, miss = n_smc_missing, fail = n_smc_failed, no_exact = n_exact_missing, n_evid = n_evidence, bias, rmse, median_abs_e, p90_abs_e, lb_coverage)]
    L <- c(L, sprintf("**p = %d, %s**", pp, sk), "", md_table(d), "")
  }
  L <- c(L, "## H2. Is the HPM accurate?", "", "Percent of expected cases (missing or failed fits and missing references count as not equal).", "")
  for (pp in sort(unique(H2$p))) for (sk in sort(unique(H2$scale_key))) {
    d <- H2[p == pp & scale_key == sk, .(scenario, n_cases, miss = n_smc_missing, fail = n_smc_failed, no_exact = n_exact_missing, pct_smc_hpm_eq_exact, pct_exact_hpm_eq_truth, pct_smc_hpm_eq_truth)]
    setnames(d, c("scenario", "n_cases", "miss", "fail", "no_exact", "% SMC HPM = exact HPM", "% exact HPM = truth", "% SMC HPM = truth"))
    L <- c(L, sprintf("**p = %d, %s**", pp, sk), "", md_table(d, 3), "")
  }
  L <- c(L, "## H3. Are the PIPs accurate (RB and plain)?", "",
         "max err = max_j |PIP-hat_j - PIP_j| per fit; mean/p90 over the n_rb (RB) / n_plain (plain) fits that supply valid PIPs. err true / null = mean |error| over true / null variables. MPM = {PIP > 1/2}; % MPM = exact MPM is over all expected cases.", "")
  for (pp in sort(unique(H3$p))) for (sk in sort(unique(H3$scale_key))) {
    d <- H3[p == pp & scale_key == sk, .(scenario, n_cases, miss = n_smc_missing, fail = n_smc_failed, no_exact = n_exact_missing, n_rb, n_plain, rb_mean_max_err, rb_p90_max_err, rb_mean_err_true, rb_mean_err_null,
                                          plain_mean_max_err, plain_p90_max_err, plain_mean_err_true, plain_mean_err_null, pct_mpm_rb_eq_exact, pct_mpm_plain_eq_exact)]
    L <- c(L, sprintf("**p = %d, %s**", pp, sk), "", md_table(d, 3), "")
  }
  L <- c(L, "## H4. Exact recovery of the true support", "",
         "Cells are `all-saved (passing-only)`: exact recoveries out of the number of expected cases in the cell; passing-only removes fits whose diagnostic flag is TRUE (master IV.1.3); failed, timed-out and not-run results are non-recoveries in both. Primary rule of every method, plus SMC pip05 and the exact HPM/MPM references; pooled over scenarios = /600 in the full study.", "")
  for (pp in sort(unique(H4$p))) for (sk in sort(unique(H4$scale_key))) {
    d <- H4[p == pp & scale_key == sk]
    if (!nrow(d)) next
    d[, cell := sprintf("%s (%s)", recovery, recovery_passing)]
    w <- data.table::dcast(d, method_id + rule_id ~ scenario, value.var = "cell")
    sc <- setdiff(names(w), c("method_id", "rule_id", "all"))
    w <- w[, c("method_id", "rule_id", sort(sc), "all"), with = FALSE]
    setnames(w, c("method_id", "rule_id", paste0("S", sort(sc)), "pooled"))
    L <- c(L, sprintf("**p = %d, %s**", pp, sk), "", md_table(w), "")
  }
  writeLines(L, path, useBytes = TRUE)
  invisible(path)
}
