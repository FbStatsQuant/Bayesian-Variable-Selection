# W3-P6: re-derive per-fit outcomes from the saved RDS files (driver v1 or v2), with p6_common.R (R01 fixes 2, 4, 5).
# Usage: Rscript --vanilla rederive.R OUT_JSONL RUN_TAG RDS_DIR [RDS_DIR ...]
# One JSON line per RDS (not the FULL_* safety copies): identity, status, reported HPM (+F), derived MR1 / cap2 HPMs (+F,
# status ok|tie|censored|unavailable), outcome classes vs F(S0), pre-LS0 / pre-local snapshots, start mode, LS0 path stats.
suppressMessages(library(jsonlite))
a <- commandArgs(trailingOnly = TRUE)
OUT <- a[1]; RUN <- a[2]; dirs <- a[-(1:2)]
here <- dirname(normalizePath(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE))))
source(file.path(here, "p6_common.R"))
mod <- function(x) if (is.list(x)) x$model else x
nz <- function(x) if (is.null(x)) NA else x
arr <- function(x) if (is.null(x)) NULL else I(as.integer(x))
files <- unlist(lapply(dirs, function(d) list.files(d, pattern = "\\.rds$", full.names = TRUE)))
files <- files[!grepl("^FULL_", basename(files))]
con <- file(OUT, "w")
for (f in files) {
  k <- tryCatch(readRDS(f), error = function(e) NULL)
  if (is.null(k)) { writeLines(toJSON(list(file = basename(f), run = RUN, read_error = TRUE), auto_unbox = TRUE), con); next }
  r <- k$rec; S0 <- as.integer(r$S0); s0k <- p6_key(S0); FS0 <- if (is.null(r$F_S0)) NA else r$F_S0
  ls0 <- k$ls0; hbl <- k$hpm_before_ls0
  hb <- if (is.null(hbl)) NULL else list(model = hbl$model, F = hbl$F)
  msize <- length(mod(k$start_mode)); ell <- r$ell
  fs <- r$ls0_first_scoring_scan; fs <- if (is.null(fs) || is.na(fs)) NA_integer_ else as.integer(fs)
  completed <- identical(k$status, "completed")
  dm <- if (completed && msize > 0) p6_derive(ell + msize, ls0, hb, fs, s0k) else list(status = "unavailable", model = NULL, F = NA, hpm_eq_S0 = NA, scores = NA)
  d2 <- if (completed && msize > 0) p6_derive(ell + 2L * msize, ls0, hb, fs, s0k) else list(status = "unavailable", model = NULL, F = NA, hpm_eq_S0 = NA, scores = NA)
  hpm <- if (is.null(k$hpm)) NULL else sort(as.integer(k$hpm))
  hpm_eq <- if (is.null(hpm)) NA else p6_key(hpm) == s0k
  # the arm's own reported outcome; for arm mr1 this IS the merged-cap method
  rep_cls <- p6_class(hpm_eq, nz(k$hpm_F), FS0)
  # method as coded (merged cap): arm mr1 -> reported; arm wide -> derived
  if (identical(r$arm, "mr1")) { asc_eq <- hpm_eq; asc_cls <- rep_cls; asc_status <- if (completed) "reported" else "not_completed" }
  else { asc_eq <- dm$hpm_eq_S0; asc_cls <- p6_class(dm$hpm_eq_S0, dm$F, FS0); asc_status <- dm$status }
  hl <- k$hpm_before_local
  out <- list(file = basename(f), run = RUN, design = r$design, rho = r$rho, n = r$n, p = r$p, s0 = r$s0, rep = r$rep, arm = r$arm,
    S0 = arr(S0), status = k$status, elapsed_sec = r$elapsed_sec, K = r$K, ell = ell, data_seed = r$data_seed, method_seed = r$method_seed,
    hpm = arr(hpm), hpm_F = nz(k$hpm_F), hpm_eq_S0 = hpm_eq, hpm_incomplete = isTRUE(r$hpm_incomplete), reported_class = rep_cls,
    hpm_prov = r$hpm_prov, hpm_prov_phi = r$hpm_prov_phi, F_S0 = FS0, F_direct_vs_ledger = if (is.null(r$F_hpm_direct) || is.na(r$F_hpm_direct) || is.null(k$hpm_F)) NA else abs(r$F_hpm_direct - k$hpm_F),
    ascoded_eq_S0 = asc_eq, ascoded_class = asc_cls, ascoded_status = asc_status,
    mr1_status = dm$status, mr1_hpm = arr(dm$model), mr1_F = dm$F, mr1_eq_S0 = dm$hpm_eq_S0, mr1_ls0_scores = dm$scores,
    mr1_class = p6_class(dm$hpm_eq_S0, dm$F, FS0),
    cap2_status = d2$status, cap2_hpm = arr(d2$model), cap2_F = d2$F, cap2_eq_S0 = d2$hpm_eq_S0, cap2_ls0_scores = d2$scores,
    cap2_class = p6_class(d2$hpm_eq_S0, d2$F, FS0),
    before_local_eq_S0 = if (is.null(hl)) NA else p6_key(mod(hl)) == s0k, before_local_F = if (is.null(hl)) NA else hl$F,
    before_ls0 = if (is.null(hb)) NULL else arr(sort(as.integer(hb$model))), before_ls0_F = if (is.null(hb)) NA else hb$F,
    before_ls0_eq_S0 = if (is.null(hb)) NA else p6_key(hb$model) == s0k, before_ls0_prov = r$hpm_before_ls0_prov,
    start_mode = arr(sort(as.integer(mod(k$start_mode)))), start_size = msize, start_has_S0 = if (msize) all(S0 %in% mod(k$start_mode)) else NA,
    cap_mr1 = ell + msize, cap_2 = ell + 2L * msize, ls0_cap_run = nz(ls0$move_cap), ls0_moves = nz(ls0$moves),
    ls0_scans = if (is.null(ls0$scanned_F)) NA else length(ls0$scanned_F), ls0_first_scoring = fs, ls0_local_limit = nz(ls0$local_limit),
    ls0_lead_swaps = r$ls0_lead_swaps, ls0_n_swap = r$ls0_n_swap, ls0_n_del = r$ls0_n_del, ls0_n_add = r$ls0_n_add, ls0_seq = r$ls0_moves_seq,
    cal_tier_final = r$cal_tier_final, cal_triggers = r$cal_triggers, cal_grid_fallback = r$cal_grid_fallback,
    t_calibration = r$t_calibration, t_final = r$t_final, t_ls0 = r$t_ls0, peak_mem_kb = r$peak_mem_kb)
  writeLines(toJSON(out, auto_unbox = TRUE, null = "null", na = "null", digits = NA), con)
}
close(con)
cat(length(files), "RDS processed ->", OUT, "\n")
