# longfits.R -- read-only report on long SMC-BVS fits (HQ ruling 2026-11-26, after S1 batch 1). Runs on Owls on pulled data.
#   Rscript harness/longfits.R [--out DIR] [--hours 6] [--suite 1] [--tag b1]
#   -> specs/longfits_<tag>.tsv (one row per fit longer than --hours, ok or timed out)
#      specs/longfits_<tag>_all_p5000.tsv (every p = 5000 fit, the population the summary is computed on)
#      specs/longfits_<tag>.md (tables and the summary)
# Never fits and never writes into the runs tree. Per-fit fields come from the json and rds records only. A timed-out fit
# has only the minimal json written by slurm/s1_smcbvs_array.sbatch (status, host, slurm job): its runtime is censored at
# the limit and its stage data are in the Slurm log on NOTS, which this script does not read.
# Definitions (OURS): calibration iterations = distinct `iter` of phase "diag" per tier in extra$stage_table; time per
# stage = phase seconds (extra$timings) / stage rows of that phase (all islands; the islands run one after another).
BASE <- local({ f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)); normalizePath(file.path(dirname(f), "..")) })
source(file.path(BASE, "harness", "methods.R")); source(file.path(BASE, "harness", "generate.R"))
suppressPackageStartupMessages(library(jsonlite))
a <- commandArgs(TRUE); opt <- list(out = S1S2_RUNS, hours = "6", suite = "1", tag = "b1")
if (length(a)) for (i in seq(1, length(a), by = 2)) opt[[sub("^--", "", a[i])]] <- a[i + 1]
H <- as.numeric(opt$hours)
tab <- read_settings(file.path(BASE, "specs", "settings.tsv")); tab <- tab[tab$suite == as.integer(opt$suite), ]
g <- function(x, ...) { for (k in c(...)) { if (is.null(x[[k]])) return(NA); x <- x[[k]] }; x }
num <- function(x) if (is.null(x) || !length(x)) NA_real_ else as.numeric(x[1])

one <- function(jf, row) {
  j <- tryCatch(fromJSON(jf, simplifyVector = FALSE), error = function(e) list(status = "failed: unreadable json"))
  rf <- sub("\\.json$", ".rds", jf); r <- if (file.exists(rf)) tryCatch(readRDS(rf), error = function(e) NULL) else NULL
  e <- r$extra
  timeout <- grepl("timeout", j$status %||% "", ignore.case = TRUE)
  lim <- if (timeout) num(sub(".*timeout ([0-9]+)s.*", "\\1", j$status)) else NA_real_
  out <- data.frame(setting_id = row$setting_id, n = row$n, p = row$p, snr = row$snr, rep = as.integer(j$rep %||% NA),
    status = j$status %||% NA, timed_out = timeout, runtime_h = num(j$runtime_sec) / 3600, censored_at_h = lim / 3600,
    host = j$host %||% NA, slurm_job = j$slurm_job %||% NA, stringsAsFactors = FALSE)
  st <- e$stage_table
  if (!is.null(st)) {
    cal <- st[st$phase != "final_bridge" & !grepl("^final", st$phase), , drop = FALSE]; fin <- st[grepl("^final", st$phase), , drop = FALSE]
    it <- function(t) length(unique(st$iter[st$phase == "diag" & st$tier == t]))
    out <- cbind(out, data.frame(tier = num(e$tier), escalated = isTRUE(e$escalated), N_final = num(e$N_particles),
      calib_iters_t0 = it(0), calib_iters_t1 = it(1), stage_rows_calib = nrow(cal), stage_rows_final = nrow(fin),
      final_stages_per_island = if (nrow(fin)) max(fin$stage) else NA,
      sec_calib = num(e$timings$calibration), sec_final = num(e$timings$final),
      sec_per_calib_stage = num(e$timings$calibration) / max(1, nrow(cal)), sec_per_final_stage = num(e$timings$final) / max(1, nrow(fin)),
      grid_unconverged = isTRUE(e$flags$grid_unconverged), forced_pilot_steps = num(e$flags$forced_pilot_steps),
      calib_triggers = paste(unlist(e$flags$calibration_triggers), collapse = ","), stringsAsFactors = FALSE))
  }
  dp <- j$diag_post
  out <- cbind(out, data.frame(success = isTRUE(j$success), failure_type = j$failure_type %||% (if (timeout) "computational" else NA),
    pi_S0 = num(g(dp, "pi_S0")), gap_logpost = num(g(dp, "gap_logpost")), mass_size_gt_2s0 = num(g(dp, "mass_size_gt_2s0")),
    max_null_pip = num(g(dp, "max_null_pip")), min_true_pip = num(g(dp, "min_true_pip")),
    min_ess_over_N = num(g(j, "summary", "min_ess_over_N")), log_Z_r_sd = num(g(j, "summary", "log_Z_r_sd")),
    eflags = paste(unlist(j$eflags), collapse = ","), snr_realised = num(g(j, "diag_data", "snr_realised")),
    lambda_min_S0 = num(g(j, "diag_data", "lambda_min_S0")), max_abs_corr = num(g(j, "diag_data", "max_abs_corr_null_true")),
    stringsAsFactors = FALSE))
  out
}

rows <- list()
for (i in seq_len(nrow(tab))) {
  fs <- Sys.glob(file.path(opt$out, "smcbvs", tab$setting_id[i], "rep_*.json"))
  for (f in fs) rows[[length(rows) + 1]] <- one(f, tab[i, ])
}
all <- do.call(rbind, lapply(rows, function(r) { miss <- setdiff(names(rows[[which.max(sapply(rows, ncol))]]), names(r)); for (m in miss) r[[m]] <- NA; r }))
long <- all[all$timed_out | (!is.na(all$runtime_h) & all$runtime_h > H), ]
long <- long[order(long$setting_id, -ifelse(long$timed_out, Inf, long$runtime_h)), ]
p5 <- all[all$p == 5000, ]
dir <- file.path(BASE, "specs")
write.table(long, file.path(dir, sprintf("longfits_%s.tsv", opt$tag)), sep = "\t", quote = FALSE, row.names = FALSE, na = "NA")
write.table(p5, file.path(dir, sprintf("longfits_%s_all_p5000.tsv", opt$tag)), sep = "\t", quote = FALSE, row.names = FALSE, na = "NA")

# ---- summary over the p = 5000 fits ---------------------------------------------------------------------------------
f2 <- function(x, d = 2) ifelse(is.na(x), "–", formatC(x, format = "f", digits = d))
ok <- p5[p5$status == "ok", ]
bys <- do.call(rbind, lapply(split(p5, p5$setting_id), function(d) { o <- d[d$status == "ok", ]
  data.frame(setting_id = d$setting_id[1], n = d$n[1], snr = d$snr[1], fits = nrow(d), timeouts = sum(d$timed_out),
    over_H = sum(o$runtime_h > H), med_h = median(o$runtime_h), max_h = max(o$runtime_h), escalated = sum(o$escalated, na.rm = TRUE),
    med_calib_iters = median(o$calib_iters_t0 + o$calib_iters_t1), med_calib_share = median(o$sec_calib / (o$sec_calib + o$sec_final)),
    med_sec_final_stage = median(o$sec_per_final_stage), med_pi_S0 = median(o$pi_S0, na.rm = TRUE), success = sum(o$success)) }))
sp <- function(v) { x <- ok[[v]]; k <- is.finite(x) & is.finite(ok$runtime_h); if (sum(k) < 5) NA else suppressWarnings(stats::cor(x[k], ok$runtime_h[k], method = "spearman")) }
vars <- c("snr", "calib_iters_t0", "calib_iters_t1", "escalated", "stage_rows_calib", "stage_rows_final", "sec_per_final_stage",
          "pi_S0", "gap_logpost", "mass_size_gt_2s0", "max_null_pip", "min_ess_over_N", "snr_realised", "lambda_min_S0", "max_abs_corr")
ok$escalated <- as.numeric(ok$escalated)
cors <- data.frame(variable = vars, spearman_with_runtime = vapply(vars, sp, 0))
# within-setting correlation (removes the SNR / n effect): median over settings with >= 8 ok fits
wsp <- function(v) { r <- vapply(split(ok, ok$setting_id), function(d) { x <- as.numeric(d[[v]]); k <- is.finite(x) & is.finite(d$runtime_h)
  if (sum(k) < 8 || stats::sd(x[k]) == 0) NA else suppressWarnings(stats::cor(x[k], d$runtime_h[k], method = "spearman")) }, 0); stats::median(r, na.rm = TRUE) }
cors$median_within_setting <- vapply(vars, wsp, 0)
esc <- if (any(ok$escalated == 1)) sprintf("escalated (tier 1) fits: %d of %d ok p = 5000 fits; median runtime %.2f h vs %.2f h not escalated",
  sum(ok$escalated == 1), nrow(ok), median(ok$runtime_h[ok$escalated == 1]), median(ok$runtime_h[ok$escalated == 0])) else "no escalated fit"
md <- c(sprintf("# Long SMC-BVS fits, S%s (%s; harness/longfits.R, %s)", opt$suite, opt$tag, format(Sys.time(), "%Y-%m-%d %H:%M")), "",
  sprintf("Fits longer than %g h or timed out: %d of %d records (%d timed out). Timed-out fits have no stage data on Owls (Slurm log on NOTS).", H, nrow(long), nrow(all), sum(all$timed_out)), "",
  "## Fits over the limit", "",
  "| setting | (n, SNR) | rep | status | runtime h | tier | calib iters t0+t1 | stage rows calib / final | s per stage calib / final | calib share | π̂(S0) | gap | mass >2s0 | max null PIP | success |",
  "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for (i in seq_len(nrow(long))) with(long[i, ], md <<- c(md, sprintf("| %s | (%d, %g) | %d | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |",
  setting_id, n, snr, rep, if (timed_out) "TIMEOUT" else "ok", if (timed_out) paste0("≥ ", f2(censored_at_h, 1)) else f2(runtime_h),
  ifelse(is.na(tier), "–", tier), if (is.na(calib_iters_t0)) "–" else paste0(calib_iters_t0, "+", calib_iters_t1),
  if (is.na(stage_rows_calib)) "–" else paste0(stage_rows_calib, " / ", stage_rows_final),
  if (is.na(sec_per_calib_stage)) "–" else paste0(f2(sec_per_calib_stage, 1), " / ", f2(sec_per_final_stage, 1)),
  f2(sec_calib / (sec_calib + sec_final)), f2(pi_S0, 3), f2(gap_logpost), f2(mass_size_gt_2s0, 3), f2(max_null_pip, 3), if (timed_out) "–" else success)))
md <- c(md, "", "## By p = 5000 setting (ok fits for the medians)", "",
  "| setting | (n, SNR) | fits | timeouts | ok > limit | median h | max h | escalated | median calib iters | median calib share | median s/final stage | median π̂(S0) | exact |",
  "|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for (i in seq_len(nrow(bys))) with(bys[i, ], md <<- c(md, sprintf("| %s | (%d, %g) | %d | %d | %d | %s | %s | %d | %s | %s | %s | %s | %d |",
  setting_id, n, snr, fits, timeouts, over_H, f2(med_h), f2(max_h), escalated, f2(med_calib_iters, 1), f2(med_calib_share), f2(med_sec_final_stage, 1), f2(med_pi_S0, 3), success)))
md <- c(md, "", "## Spearman correlation with runtime (ok p = 5000 fits; timed-out fits excluded, so these understate the tail)", "",
  "| variable | pooled | median within setting |", "|---|---|---|",
  sprintf("| %s | %s | %s |", cors$variable, f2(cors$spearman_with_runtime), f2(cors$median_within_setting)), "", esc)
writeLines(md, file.path(dir, sprintf("longfits_%s.md", opt$tag)))
cat(sprintf("%d long fits (%d timed out) of %d records; wrote specs/longfits_%s{.tsv,_all_p5000.tsv,.md}\n", nrow(long), sum(all$timed_out), nrow(all), opt$tag))
