# extract_h2.R -- per-fit extraction of the PROD-H rerun + full reproduction check vs the 2026-10-23 fits (ANALYSIS-H2).
# Usage: Rscript extract_h2.R NEW_LIST OLD_LIST OUT_DIR WORKER NWORKERS
#   NEW_LIST / OLD_LIST: cases_new.tsv / cases_old.tsv from make_lists.R (same case order). OUT_DIR gets fit/<case>.csv and repro/<case>.tsv.
# Resumable: a case whose two outputs exist is skipped. Truth is read only here, after the fits (scoring), from the scoring truth copy.
# Reproduction fields (identical(), max |diff|): native_status, fit$log_Z, fit$log_Z_r, fit$hpm, fit$hpm_F, fit$pip_primary, fit$pip_r, fit$mpm,
#   record$pip (unnamed), record$hpm, record$mpm. Any FALSE is a defect (reported, not fixed).
a <- commandArgs(trailingOnly = TRUE)
NL <- utils::read.delim(a[1], stringsAsFactors = FALSE); OL <- utils::read.delim(a[2], stringsAsFactors = FALSE)
out <- a[3]; k <- as.integer(a[4]); N <- as.integer(a[5])
stopifnot(all(NL$case_id %in% OL$case_id)); OL <- OL[match(NL$case_id, OL$case_id), ]; stopifnot(identical(NL$case_id, OL$case_id))
TRU <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/F_2026-10-19_benchmark_study_n200/Benchmark_Study_20261019/verify/recount/c050/inputs/truth_scoring"
SD <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/scoring"
Sys.setenv(SCORING_DIR = SD); source(file.path(SD, "R", "load_all.R"))
for (d in c("fit", "repro")) dir.create(file.path(out, d), showWarnings = FALSE, recursive = TRUE)
`%|%` <- function(x, y) if (is.null(x) || !length(x)) y else x
s1 <- function(x) if (is.null(x) || !length(x)) NA else if (length(x) == 1L) x else paste(x, collapse = ";")
sup <- function(x) if (is.null(x) || !length(x)) "" else paste(sort(as.integer(x)), collapse = ";")
sel <- function(S, S0) { S <- as.integer(S %|% integer(0)); c(k = length(S), tp = sum(S %in% S0), fp = sum(!S %in% S0), fn = sum(!S0 %in% S), exact = setequal(S, S0) && length(S) == length(S0)) }
repro_fields <- list(native_status = function(r) r$native_status, `fit$log_Z` = function(r) r$fit$log_Z, `fit$log_Z_r` = function(r) r$fit$log_Z_r,
  `fit$hpm` = function(r) r$fit$hpm, `fit$hpm_F` = function(r) r$fit$hpm_F, `fit$pip_primary` = function(r) r$fit$pip_primary,
  `fit$pip_r` = function(r) r$fit$pip_r, `fit$mpm` = function(r) r$fit$mpm, `record$pip` = function(r) unname(r$pip),
  `record$hpm` = function(r) r$hpm, `record$mpm` = function(r) r$mpm)
mine <- which((seq_len(nrow(NL)) - 1L) %% N == k - 1L)
cat(sprintf("%s worker %d/%d: %d cases\n", format(Sys.time(), "%FT%TZ", tz = "UTC"), k, N, length(mine)))
for (i in mine) {
  id <- NL$case_id[i]; ff <- file.path(out, "fit", paste0(id, ".csv")); fr <- file.path(out, "repro", paste0(id, ".tsv"))
  if (file.exists(ff) && file.exists(fr)) next
  res <- tryCatch({
    rn <- readRDS(NL$record[i]); ro <- readRDS(OL$record[i])
    # ---- reproduction
    rp <- do.call(rbind, lapply(names(repro_fields), function(f) { x <- repro_fields[[f]](ro); y <- repro_fields[[f]](rn)
      d <- if (is.numeric(x) && is.numeric(y) && length(x) == length(y) && length(x)) suppressWarnings(max(abs(as.double(x) - as.double(y)), na.rm = TRUE)) else NA_real_
      data.frame(case_id = id, field = f, identical = identical(x, y), max_abs_diff = d, old = substr(paste(format(x), collapse = ";"), 1, 60),
                 new = substr(paste(format(y), collapse = ";"), 1, 60), stringsAsFactors = FALSE) }))
    # ---- per-fit fields (new record)
    sm <- extract_smc(rn); tr <- readRDS(file.path(TRU, sprintf("p%04d", NL$p[i]), paste0(NL$dataset_id[i], ".rds"))); S0 <- sort(as.integer(tr$active))
    ins <- rn$instrumentation %|% rn$fit$instrumentation %|% list()
    hpm <- if (isTRUE(sm$hpm_ok)) sm$hpm else integer(0); mrb <- sm$mpm %|% integer(0); mpl <- sm$mpm_plain %|% integer(0)
    sh <- sel(hpm, S0); sr <- sel(mrb, S0); spl <- sel(mpl, S0)
    rb <- sm$pip_rb; pl <- sm$pip_plain
    ls <- rn$fit$local_search %|% list(); bb <- ins$best_before_local$model; ba <- ins$best_after_local$model
    fr_m <- rn$fit$score_counts$fresh; ph <- if (is.matrix(fr_m)) rowSums(fr_m) else NULL; mc <- if (is.matrix(fr_m)) colSums(fr_m) else NULL
    stp <- ins$stop; stop_cols <- if (is.list(stp) && length(stp)) { v <- lapply(stp, function(z) if (is.atomic(z)) s1(z) else NA); v <- v[!vapply(v, function(z) is.na(z[1]), TRUE)]; setNames(v, paste0("stop_", names(v))) } else list()
    hrow <- rn$rows[rn$rows$rule_id == "hpm", , drop = FALSE]
    row <- c(list(case_id = id, dataset_id = NL$dataset_id[i], p = NL$p[i], scenario = as.integer(sub("^p[0-9]{4}_S([0-9])_.*", "\\1", id)),
      replicate = as.integer(sub(".*_r([0-9]{3})_.*", "\\1", id)), scale_key = NL$scale_key[i], S0 = sup(S0),
      native_status = sm$native_status, ok = sm$ok, runtime_s = sm$runtime_s, tier = sm$tier, escalated = sm$escalated,
      escalation_reasons = s1(ins$escalation$reasons), diag_flag = s1(hrow$diag_flag), diag_codes = if ("diag_codes" %in% names(hrow)) s1(hrow$diag_codes) else NA,
      support_audit = if ("support_audit" %in% names(hrow)) s1(hrow$support_audit) else NA,
      hpm = sup(hpm), hpm_k = sh[["k"]], hpm_tp = sh[["tp"]], hpm_fp = sh[["fp"]], hpm_fn = sh[["fn"]], hpm_exact = as.logical(sh[["exact"]]) & isTRUE(sm$hpm_ok),
      mpm_rb = sup(mrb), mpm_rb_k = sr[["k"]], mpm_rb_fp = sr[["fp"]], mpm_rb_fn = sr[["fn"]], mpm_rb_exact = as.logical(sr[["exact"]]) & isTRUE(sm$rb_ok),
      mpm_plain = sup(mpl), mpm_plain_k = spl[["k"]], mpm_plain_fp = spl[["fp"]], mpm_plain_fn = spl[["fn"]], mpm_plain_exact = as.logical(spl[["exact"]]) & isTRUE(sm$plain_ok),
      mpm_rb_eq_plain = if (isTRUE(sm$rb_ok) && isTRUE(sm$plain_ok)) setequal(mrb, mpl) else NA,
      pip_rb_plain_maxabs = if (!is.null(rb) && !is.null(pl)) max(abs(rb - pl)) else NA,
      pip_rb_plain_n_side = if (!is.null(rb) && !is.null(pl)) sum((rb > 0.5) != (pl > 0.5)) else NA,
      pip_plain_truth_min = if (!is.null(pl)) min(pl[S0]) else NA, pip_plain_null_max = if (!is.null(pl)) max(pl[-S0]) else NA,
      pip_rb_truth_min = if (!is.null(rb)) min(rb[S0]) else NA, pip_rb_null_max = if (!is.null(rb)) max(rb[-S0]) else NA,
      log_Z_stored = sm$log_Z, log_Z_r_sd_stored = if (length(sm$log_Z_r) == 4L) stats::sd(sm$log_Z_r) else NA, hpm_F = sm$hpm_F,
      hpm_prov_phase = s1(rn$fit$hpm_provenance$phase), hpm_prov_mech = s1(rn$fit$hpm_provenance$mechanism), hpm_prov_tier = s1(rn$fit$hpm_provenance$tier),
      hpm_prov_stage = s1(rn$fit$hpm_provenance$stage), n_stages_final = sm$n_stages_final, min_ess = sm$min_ess, cut_group = sm$cut_group,
      stages_tier_final = s1(ins$stages$tier_final), ins_version = s1(ins$version),
      reg_mode = s1(ins$scored$mode), reg_n_distinct = s1(ins$scored$n_distinct), reg_n_distinct_hll = s1(ins$scored$n_distinct_hll),
      reg_n_distinct_hll_after_cal = s1(ins$scored$after_calibration$n_distinct_hll), reg_log_sum_exp_F = s1(ins$scored$log_sum_exp_F),
      reg_first_scored_present = !is.null(ins$scored$first_scored),
      score_fresh_total = sm$score_fresh, score_logical_total = sm$score_logical,
      t_calibration = s1(rn$fit$timings$calibration), t_final = s1(rn$fit$timings$final), t_total = s1(rn$fit$timings$total),
      ls_centre_eq_truth = if (!is.null(ls$centre)) setequal(as.integer(ls$centre), S0) && length(ls$centre) == length(S0) else NA,
      ls_returned_eq_truth = if (!is.null(ls$returned)) setequal(as.integer(ls$returned), S0) && length(ls$returned) == length(S0) else NA,
      ls_centre = sup(ls$centre), ls_returned = sup(ls$returned),
      ls_centre_n_true = if (!is.null(ls$centre)) sum(as.integer(ls$centre) %in% S0) else NA,
      ls_centre_n_null = if (!is.null(ls$centre)) sum(!as.integer(ls$centre) %in% S0) else NA,   # centre in R_d  <=>  n_null <= d
      ls_centre_dist = if (!is.null(ls$centre)) length(setdiff(as.integer(ls$centre), S0)) + length(setdiff(S0, as.integer(ls$centre))) else NA,
      ls_n_scanned_centres = length(ls$scanned_centres %|% list()),
      ls_moves = s1(ls$moves), ls_termination = s1(ls$termination), ls_certified = s1(ls$local_certified), ls_limit = s1(ls$local_limit),
      ls_n_evaluated = s1(ls$n_evaluated), ls_centre_F = s1(ls$centre_F), ls_returned_F = s1(ls$returned_F),
      before_local_eq_truth = if (!is.null(bb)) setequal(as.integer(bb), S0) && length(bb) == length(S0) else NA,
      after_local_eq_truth = if (!is.null(ba)) setequal(as.integer(ba), S0) && length(ba) == length(S0) else NA,
      local_changed = s1(ins$best_after_local$changed), stop_present = length(stp) > 0),
      if (!is.null(ph)) setNames(as.list(ph), paste0("fresh_ph_", names(ph))) else list(),
      if (!is.null(mc)) setNames(as.list(mc), paste0("fresh_mech_", names(mc))) else list(), stop_cols)
    row <- lapply(row, function(v) if (is.null(v) || !length(v)) NA else v)
    list(rp = rp, row = as.data.frame(row, stringsAsFactors = FALSE, check.names = FALSE))
  }, error = function(e) e)
  if (inherits(res, "error")) { writeLines(conditionMessage(res), file.path(out, paste0(id, ".err"))); cat("ERR", id, conditionMessage(res), "\n"); next }
  utils::write.table(res$rp, paste0(fr, ".tmp"), sep = "\t", row.names = FALSE, quote = FALSE); file.rename(paste0(fr, ".tmp"), fr)
  utils::write.csv(res$row, paste0(ff, ".tmp"), row.names = FALSE, na = "NA"); file.rename(paste0(ff, ".tmp"), ff)
}
cat(sprintf("%s WORKER_DONE %d\n", format(Sys.time(), "%FT%TZ", tz = "UTC"), k))
