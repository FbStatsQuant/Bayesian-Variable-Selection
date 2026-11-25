# aggregate.R -- successes/100 per setting x method from the run records (for later; never launches fits).
#   Rscript harness/aggregate.R [--out DIR] [--dest specs/results_successes.tsv]
# success = selected support equals the true support exactly (OURS, INTERFACE.md). A failed or missing record counts as
# a non-success and is reported in n_failed / n_missing (expected reps = 100). Monte Carlo SE = sqrt(p(1-p)/n_reps).
BASE <- local({ f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)); normalizePath(file.path(dirname(f), "..")) })
source(file.path(BASE, "harness", "methods.R")); source(file.path(BASE, "harness", "generate.R"))
suppressPackageStartupMessages(library(jsonlite))
a <- commandArgs(TRUE); opt <- list(out = S1S2_RUNS, dest = file.path(BASE, "specs", "results_successes.tsv"), reps = "100")
if (length(a)) for (i in seq(1, length(a), by = 2)) opt[[sub("^--", "", a[i])]] <- a[i + 1]
R <- as.integer(opt$reps)
tab <- read_settings(file.path(BASE, "specs", "settings.tsv"))
out <- list()
for (m in names(S1S2_METHODS)) for (s in tab$setting_id) {
  files <- file.path(opt$out, m, s, sprintf("rep_%03d.json", seq_len(R)))
  have <- file.exists(files)
  if (!any(have)) next
  recs <- lapply(files[have], function(f) tryCatch(fromJSON(f), error = function(e) list(status = "failed: unreadable")))
  okv <- vapply(recs, function(r) identical(r$status, "ok"), TRUE)
  suc <- vapply(recs, function(r) isTRUE(r$success) && identical(r$status, "ok"), TRUE)
  num <- function(k) mean(vapply(recs[okv], function(r) as.numeric(r[[k]] %||% NA), 0), na.rm = TRUE)
  out[[length(out) + 1]] <- data.frame(setting_id = s, method = m, successes = sum(suc), n_records = sum(have),
    n_failed = sum(!okv), n_missing = R - sum(have), success_rate = sum(suc) / R, mc_se = sqrt((sum(suc) / R) * (1 - sum(suc) / R) / R),
    mean_TP = num("TP"), mean_FP = num("FP"), mean_FN = num("FN"), mean_size = num("n_selected"), mean_runtime_sec = num("runtime_sec"))
}
res <- if (length(out)) do.call(rbind, out) else data.frame()
if (nrow(res)) res <- merge(tab[, c("setting_id", "label")], res, by = "setting_id")
write.table(res, opt$dest, sep = "\t", quote = FALSE, row.names = FALSE, na = "NA")
cat("wrote", nrow(res), "rows to", opt$dest, "\n")

# ---- deliverable table per setting for one method and suite (manager brief 2026-11-25) ----------------------------------
#   Rscript harness/aggregate.R --method smcbvs --suite 1 [--out DIR] [--reps 100]  -> specs/results_S<suite>_<method>.{tsv,md}
# success = MPM equals S0 exactly (OURS); Wilson 95% interval over the expected reps (missing / failed = non-success).
# Failure split from rec$failure_type (harness/diagnostics.R): statistical (the method's own score prefers its selection
# to S0), search (it prefers S0 but selected something else), other (failed fit, or no scorer to classify).
# pi_S0 = diag_post$pi_S0; min ESS/N = summary$min_ess_over_N (SMC-BVS only); runtime = adapter runtime_sec;
# core-h = sum over records of (wall_sec_harness + diag_sec) / 3600, single-threaded fits.
if (!is.null(opt$method)) {
  source(file.path(BASE, "harness", "diagnostics.R"))
  m <- opt$method; su <- as.integer(opt$suite %||% "1")
  rows <- list()
  for (s in tab$setting_id[tab$suite == su]) {
    files <- file.path(opt$out, m, s, sprintf("rep_%03d.json", seq_len(R)))
    have <- file.exists(files)
    recs <- lapply(files[have], function(f) tryCatch(fromJSON(f, simplifyVector = FALSE), error = function(e) list(status = "failed: unreadable")))
    g <- function(r, ...) { x <- r; for (k in c(...)) { x <- x[[k]]; if (is.null(x)) return(NA_real_) }; as.numeric(x) }
    okv <- vapply(recs, function(r) identical(r$status, "ok"), TRUE)
    suc <- vapply(recs, function(r) isTRUE(r$success) && identical(r$status, "ok"), TRUE)
    ft <- vapply(recs, function(r) if (identical(r$status, "ok")) as.character(r$failure_type %||% "other") else "other", "")
    ft[suc] <- "none"
    pis <- vapply(recs[okv], g, 0, "diag_post", "pi_S0")
    ess <- vapply(recs[okv], g, 0, "summary", "min_ess_over_N")
    rt <- vapply(recs[okv], g, 0, "runtime_sec")
    wall <- vapply(recs, function(r) sum(c(g(r, "wall_sec_harness"), g(r, "diag_sec")), na.rm = TRUE), 0)
    ef <- vapply(recs, function(r) isTRUE(r$eflag_any), TRUE)
    q <- function(x, pr) if (all(is.na(x))) NA_real_ else unname(stats::quantile(x, pr, na.rm = TRUE))
    w <- wilson(sum(suc), R); row <- tab[tab$setting_id == s, ]
    rows[[length(rows) + 1]] <- data.frame(setting_id = s, label = row$label, n = row$n, p = row$p, snr = row$snr,
      n_records = sum(have), n_ok = sum(okv), n_failed = sum(!okv), n_missing = R - sum(have),
      successes = sum(suc), reps = R, success_rate = sum(suc) / R, wilson_lo = w[1], wilson_hi = w[2],
      fail_statistical = sum(ft == "statistical"), fail_search = sum(ft == "search"), fail_other = sum(!suc & !(ft %in% c("statistical", "search"))),
      eflag_n = sum(ef), pi_S0_median = q(pis, .5), pi_S0_q25 = q(pis, .25), pi_S0_q75 = q(pis, .75),
      min_ess_over_N_median = q(ess, .5), runtime_median_sec = q(rt, .5), core_h_total = sum(wall) / 3600,
      stringsAsFactors = FALSE)
  }
  D <- do.call(rbind, rows)
  stem <- file.path(BASE, "specs", sprintf("results_S%d_%s", su, m))
  write.table(D, paste0(stem, ".tsv"), sep = "\t", quote = FALSE, row.names = FALSE, na = "NA")
  f2 <- function(x, d = 2) ifelse(is.na(x), "–", formatC(x, format = "f", digits = d))
  md <- c(sprintf("# %s on S%d: %d settings x %d reps (harness/aggregate.R, %s)", m, su, nrow(D), R, format(Sys.time(), "%Y-%m-%d %H:%M")), "",
          "Success = MPM equals S0 exactly; 95% Wilson interval over the expected reps (missing and failed count as non-success).", "",
          "| setting | (n, p, SNR) | success | Wilson 95% | stat / search / other | E-flags | π̂(S0) median [IQR] | min ESS/N median | runtime median (s) | core-h | ok / failed / missing |",
          "|---|---|---|---|---|---|---|---|---|---|---|")
  for (i in seq_len(nrow(D))) with(D[i, ], md <<- c(md, sprintf("| %s | (%d, %d, %g) | %d/%d | [%s, %s] | %d / %d / %d | %d | %s [%s, %s] | %s | %s | %s | %d / %d / %d |",
    setting_id, n, p, snr, successes, reps, f2(wilson_lo, 3), f2(wilson_hi, 3), fail_statistical, fail_search, fail_other, eflag_n,
    f2(pi_S0_median, 3), f2(pi_S0_q25, 3), f2(pi_S0_q75, 3), f2(min_ess_over_N_median, 3), f2(runtime_median_sec, 0), f2(core_h_total, 2),
    n_ok, n_failed, n_missing)))
  writeLines(md, paste0(stem, ".md"))
  cat("wrote", nrow(D), "rows to", paste0(stem, ".tsv"), "and .md\n")
}
