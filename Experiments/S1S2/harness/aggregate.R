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
#   S2 also writes specs/results_S2_<method>_by_nsrhonu.{tsv,md}: groups (n, s, rho, nu), pooled over beta-type.
# success = MPM equals S0 exactly (OURS); Wilson 95% interval over the expected reps (missing / failed = non-success).
# Failure split from rec$failure_type (harness/diagnostics.R): statistical (the method's own score prefers its selection
# to S0), search (it prefers S0 but selected something else), computational (wall-time limit hit; HQ ruling 2026-11-26:
# counted against the 100 tasks, never dropped), other (any other failed fit, or no scorer to classify).
# pi_S0 = diag_post$pi_S0; min ESS/N = summary$min_ess_over_N (SMC-BVS only); runtime = adapter runtime_sec;
# core-h = sum over records of (wall_sec_harness + diag_sec) / 3600, single-threaded fits.
# E-flags by type (HQ 2026-11-26): E1, E2, E3, low_empirical_ESS and escalated, read from the rds extra$flags as
# slurm/check_batch.sh does (ok fits only); eflag_n = fits with any of E1/E2/E3/low_empirical_ESS (json eflag_any).
if (!is.null(opt$method)) {
  source(file.path(BASE, "harness", "diagnostics.R"))
  m <- opt$method; su <- as.integer(opt$suite %||% "1")
  FL <- c("E1", "E2", "E3", "low_empirical_ESS", "escalated")
  g <- function(r, ...) { x <- r; for (k in c(...)) { x <- x[[k]]; if (is.null(x)) return(NA_real_) }; as.numeric(x) }
  # one row per existing record
  per_rec <- function(s) {
    files <- file.path(opt$out, m, s, sprintf("rep_%03d.json", seq_len(R)))
    files <- files[file.exists(files)]
    if (!length(files)) return(NULL)
    do.call(rbind, lapply(files, function(f) {
      r <- tryCatch(fromJSON(f, simplifyVector = FALSE), error = function(e) list(status = "failed: unreadable"))
      ok <- identical(r$status, "ok"); suc <- ok && isTRUE(r$success)
      ft <- if (suc) "none" else if (ok) as.character(r$failure_type %||% "other") else failure_type_of(FALSE, r$status)
      fl <- setNames(rep(NA, length(FL)), FL)
      if (ok) {
        rf <- sub("\\.json$", ".rds", f)
        x <- if (file.exists(rf)) tryCatch(readRDS(rf)$extra$flags, error = function(e) NULL) else NULL
        if (!is.null(x)) for (k in FL) fl[[k]] <- isTRUE(x[[k]])
      }
      data.frame(setting_id = s, ok = ok, suc = suc, ft = ft, eflag = isTRUE(r$eflag_any),
                 pi = if (ok) g(r, "diag_post", "pi_S0") else NA_real_, ess = if (ok) g(r, "summary", "min_ess_over_N") else NA_real_,
                 rt = if (ok) g(r, "runtime_sec") else NA_real_, wall = sum(c(g(r, "wall_sec_harness"), g(r, "diag_sec")), na.rm = TRUE),
                 t(fl), stringsAsFactors = FALSE, check.names = FALSE)
    }))
  }
  P <- do.call(rbind, lapply(tab$setting_id[tab$suite == su], per_rec))
  q <- function(x, pr) if (all(is.na(x))) NA_real_ else unname(stats::quantile(x, pr, na.rm = TRUE))
  # summary of the records d of `tasks` expected tasks
  summ <- function(d, tasks) {
    if (is.null(d) || !nrow(d)) d <- P[0, ]
    k <- sum(d$suc); w <- wilson(k, tasks); o <- d[d$ok, ]
    data.frame(n_records = nrow(d), n_ok = sum(d$ok), n_failed = sum(!d$ok), n_missing = tasks - nrow(d),
      successes = k, reps = tasks, success_rate = k / tasks, wilson_lo = w[1], wilson_hi = w[2],
      fail_statistical = sum(d$ft == "statistical"), fail_search = sum(d$ft == "search"), n_computational = sum(d$ft == "computational"),
      fail_other = sum(!d$suc & !(d$ft %in% c("statistical", "search", "computational"))),
      eflag_n = sum(d$eflag), pi_S0_median = q(o$pi, .5), pi_S0_q25 = q(o$pi, .25), pi_S0_q75 = q(o$pi, .75),
      min_ess_over_N_median = q(o$ess, .5), runtime_median_sec = q(o$rt, .5), core_h_total = sum(d$wall) / 3600,
      E1 = sum(o$E1 %in% TRUE), E2 = sum(o$E2 %in% TRUE), E3 = sum(o$E3 %in% TRUE),
      low_empirical_ESS = sum(o$low_empirical_ESS %in% TRUE), escalated = sum(o$escalated %in% TRUE))
  }
  f2 <- function(x, d = 2) ifelse(is.na(x), "–", formatC(x, format = "f", digits = d))
  efs <- function(z) sprintf("%d / %d / %d / %d / %d", z$E1, z$E2, z$E3, z$low_empirical_ESS, z$escalated)
  ts <- tab[tab$suite == su, ]
  D <- do.call(rbind, lapply(seq_len(nrow(ts)), function(i) { row <- ts[i, ]
    cbind(data.frame(setting_id = row$setting_id, label = row$label, n = row$n, p = row$p, snr = row$snr, stringsAsFactors = FALSE),
          summ(P[P$setting_id == row$setting_id, ], R)) }))
  stem <- file.path(BASE, "specs", sprintf("results_S%d_%s", su, m))
  write.table(D, paste0(stem, ".tsv"), sep = "\t", quote = FALSE, row.names = FALSE, na = "NA")
  coord <- function(row) if (su == 1) sprintf("(%d, %d, %g)", row$n, row$p, row$snr) else
    sprintf("(%d, %d, s=%d, ρ=%g, ν=%g, type %s)", row$n, row$p, row$s0, row$rho, row$nu, row$beta_type)
  md <- c(sprintf("# %s on S%d: %d settings x %d reps (harness/aggregate.R, %s)", m, su, nrow(D), R, format(Sys.time(), "%Y-%m-%d %H:%M")), "",
          "Success = MPM equals S0 exactly; 95% Wilson interval over the expected reps (missing and failed count as non-success).",
          "E-flags = ok fits with any engine E-check (E1/E2/E3/low_empirical_ESS); by type from the rds extra$flags (ok fits): E1 / E2 / E3 / lowESS / escalated.", "",
          sprintf("| setting | %s | success | Wilson 95%% | stat / search / computational / other | E-flags | E1 / E2 / E3 / lowESS / esc | π̂(S0) median [IQR] | min ESS/N median | runtime median (s) | core-h | ok / failed / missing |",
                  if (su == 1) "(n, p, SNR)" else "(n, p, s, ρ, ν, beta-type)"),
          "|---|---|---|---|---|---|---|---|---|---|---|---|")
  for (i in seq_len(nrow(D))) { z <- D[i, ]; md <- c(md, sprintf("| %s | %s | %d/%d | [%s, %s] | %d / %d / %d / %d | %d | %s | %s [%s, %s] | %s | %s | %s | %d / %d / %d |",
    z$setting_id, coord(ts[i, ]), z$successes, z$reps, f2(z$wilson_lo, 3), f2(z$wilson_hi, 3), z$fail_statistical, z$fail_search, z$n_computational,
    z$fail_other, z$eflag_n, efs(z), f2(z$pi_S0_median, 3), f2(z$pi_S0_q25, 3), f2(z$pi_S0_q75, 3), f2(z$min_ess_over_N_median, 3),
    f2(z$runtime_median_sec, 0), f2(z$core_h_total, 2), z$n_ok, z$n_failed, z$n_missing)) }
  writeLines(md, paste0(stem, ".md"))
  cat("wrote", nrow(D), "rows to", paste0(stem, ".tsv"), "and .md\n")
  if (su == 2) {   # grouped table: (n, s, rho, nu), pooled over beta-type
    key <- interaction(ts$n, ts$s0, ts$rho, ts$nu, drop = TRUE, lex.order = TRUE)
    G <- do.call(rbind, lapply(split(seq_len(nrow(ts)), key), function(ii) { r0 <- ts[ii[1], ]
      cbind(data.frame(n = r0$n, p = r0$p, s = r0$s0, rho = r0$rho, nu = r0$nu, beta_types = paste(sort(unique(ts$beta_type[ii])), collapse = ","),
                       settings = paste(ts$setting_id[ii], collapse = ","), stringsAsFactors = FALSE),
            summ(P[P$setting_id %in% ts$setting_id[ii], ], R * length(ii))) }))
    G <- G[order(G$n, G$rho, G$nu), ]
    gs <- paste0(stem, "_by_nsrhonu")
    write.table(G, paste0(gs, ".tsv"), sep = "\t", quote = FALSE, row.names = FALSE, na = "NA")
    gm <- c(sprintf("# %s on S2 grouped by (n, s, ρ, ν), pooled over beta-type (types %s; %d settings per group, %d reps each) (harness/aggregate.R, %s)",
                    m, paste(sort(unique(ts$beta_type)), collapse = " and "), length(unique(ts$beta_type)), R, format(Sys.time(), "%Y-%m-%d %H:%M")), "",
            "Pooled factor: beta-type (1 = equally spaced support, 2 = first s). Tasks = settings in the group x reps; Wilson 95% over the tasks.", "",
            "| (n, s) | ρ | ν | success / tasks | Wilson 95% | stat / search / computational / other | E-flags | E1 / E2 / E3 / lowESS / esc | π̂(S0) median | min ESS/N median |",
            "|---|---|---|---|---|---|---|---|---|---|")
    for (i in seq_len(nrow(G))) { z <- G[i, ]; gm <- c(gm, sprintf("| (%d, %d) | %g | %g | %d/%d | [%s, %s] | %d / %d / %d / %d | %d | %s | %s | %s |",
      z$n, z$s, z$rho, z$nu, z$successes, z$reps, f2(z$wilson_lo, 3), f2(z$wilson_hi, 3), z$fail_statistical, z$fail_search, z$n_computational,
      z$fail_other, z$eflag_n, efs(z), f2(z$pi_S0_median, 3), f2(z$min_ess_over_N_median, 3))) }
    writeLines(gm, paste0(gs, ".md"))
    cat("wrote", nrow(G), "groups to", paste0(gs, ".tsv"), "and .md\n")
  }
}
