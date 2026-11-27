# aggregate.R -- successes/100 per setting x method from the run records (for later; never launches fits).
#   Rscript harness/aggregate.R [--out DIR] [--dest specs/results_successes.tsv]
# Record rules (both sections): only <out>/<method>/<setting>/rep_RRR.json is read, never _superseded/ (pull_to_owls.sh
# --backup-dir) or any audit folder, and --out itself may not lie in one; every json's setting_id, rep (and method, when
# present) must match its path, and a (setting, rep) may have only one json (rep_12.json next to rep_012.json = duplicate):
# the script stops with an error otherwise.
# success = selected support equals the true support exactly (OURS, INTERFACE.md). A failed or missing record counts as
# a non-success and is reported in n_failed / n_missing (expected reps = 100). Monte Carlo SE = sqrt(p(1-p)/n_reps).
BASE <- local({ f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)); normalizePath(file.path(dirname(f), "..")) })
source(file.path(BASE, "harness", "methods.R")); source(file.path(BASE, "harness", "generate.R")); source(file.path(BASE, "harness", "records.R"))
suppressPackageStartupMessages(library(jsonlite))
a <- commandArgs(TRUE); opt <- list(out = S1S2_RUNS, dest = file.path(BASE, "specs", "results_successes.tsv"), reps = "100",
                                      specs = file.path(BASE, "specs"), final = FALSE)
i <- 1
while (i <= length(a)) {
  if (a[i] == "--final") { opt$final <- TRUE; i <- i + 1; next }
  if (!grepl("^--", a[i]) || i == length(a)) stop("bad argument: ", a[i])
  opt[[gsub("-", "_", sub("^--", "", a[i]))]] <- a[i + 1]; i <- i + 2
}
R <- as.integer(opt$reps)
tab <- read_settings(file.path(BASE, "specs", "settings.tsv"))
rec_guard_root(opt$out)   # harness/records.R: never _superseded/ or audit folders; identity + duplicate checks
rec_path <- function(m, s, r) rec_file(file.path(opt$out, m), s, r)
read_rec <- function(m, s, r, simplify) rec_read(file.path(opt$out, m), m, s, r, simplify)
out <- list()
for (m in names(S1S2_METHODS)) for (s in tab$setting_id) {
  files <- rec_path(m, s, seq_len(R))
  have <- file.exists(files)
  if (!any(have)) next
  recs <- lapply(seq_len(R)[have], function(r) read_rec(m, s, r, TRUE))
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
#   Rscript harness/aggregate.R --method smcbvs --suite 1 [--out DIR] [--reps 100] [--specs DIR] [--final [--queue-file F]]
#     -> specs/results_S<suite>_<method>.{tsv,md}   (--method: smcbvs or a benchmark, lasso_cv|scad|susie|bas_mc3|asi)
#   S2 also writes specs/results_S2_<method>_by_nsrhonu.{tsv,md}: groups (n, s, rho, nu), pooled over beta-type.
# success = MPM equals S0 exactly (OURS); Wilson 95% interval over the expected reps (missing / failed = non-success).
# Failure split from rec$failure_type (harness/diagnostics.R): statistical (the method's own score prefers its selection
# to S0), search (it prefers S0 but selected something else), computational (wall-time limit hit; HQ ruling 2026-11-26:
# counted against the 100 tasks, never dropped), other (any other failed fit, or no scorer to classify).
# pi_S0 = diag_post$pi_S0; min ESS/N = summary$min_ess_over_N (SMC-BVS only); runtime = adapter runtime_sec;
# core-h = sum over records of (wall_sec_harness + diag_sec) / 3600, single-threaded fits.
# E-flags by type (HQ 2026-11-26): E1, E2, E3, low_empirical_ESS and escalated, read from the rds extra$flags as
# slurm/check_batch.sh does (ok fits only); eflag_n = fits with any of E1/E2/E3/low_empirical_ESS (json eflag_any).
# Benchmarks (--method lasso_cv|scad|susie|bas_mc3|asi): no E-flags, so eflag_n and E1..escalated are NA (md: –).
# Appended columns (after the existing ones; existing columns unchanged): hamming_mean, TP_mean, FP_mean, FN_mean, F1_mean
# over the expected reps, from the json TP/FP/FN (checked against selected vs support); a failed or missing record counts
# as S-hat = {} (TP = FP = 0, FN = s0, F1 = 0); F1 per fit = 2TP / (2TP + FP + FN); Hamming = FP + FN.
#   [--specs DIR] output folder (default specs/).
#   --final: refuse (exit 1) if any record of (method, suite) is a "failed: harness wall timeout" stub whose array task
#   (json slurm_job, e.g. 2902188_712) is still in the queue: ssh nots squeue -h -u fb31 -r -o %i (read-only), or the
#   ids listed one per line in --queue-file FILE (offline/tests). A stub whose task has ended is a computational
#   failure and is counted, never dropped.
if (isTRUE(opt$final) && is.null(opt$method)) stop("--final needs --method")
if (!is.null(opt$method)) {
  source(file.path(BASE, "harness", "diagnostics.R"))
  m <- opt$method; su <- as.integer(opt$suite %||% "1")
  if (!m %in% names(S1S2_METHODS)) stop("unknown --method ", m)
  is_smc <- m == "smcbvs"
  FL <- c("E1", "E2", "E3", "low_empirical_ESS", "escalated")
  g <- function(r, ...) { x <- r; for (k in c(...)) { x <- x[[k]]; if (is.null(x)) return(NA_real_) }; as.numeric(x) }
  # one row per existing record
  per_rec <- function(s) {
    reps <- seq_len(R)[file.exists(rec_path(m, s, seq_len(R)))]
    if (!length(reps)) return(NULL)
    s0 <- tab$s0[tab$setting_id == s]
    do.call(rbind, lapply(reps, function(rp) {
      f <- rec_path(m, s, rp)
      r <- read_rec(m, s, rp, FALSE)
      ok <- identical(r$status, "ok"); suc <- ok && isTRUE(r$success)
      if (ok) { cf <- rec_confusion(r, f); tp <- cf[["TP"]]; fp <- cf[["FP"]]; fn <- cf[["FN"]] }   # checked vs the json fields
      else { tp <- 0; fp <- 0; fn <- s0 }
      stub <- !ok && grepl("^failed: harness wall timeout", as.character(r$status %||% ""))
      ft <- if (suc) "none" else if (ok) as.character(r$failure_type %||% "other") else failure_type_of(FALSE, r$status)
      fl <- setNames(rep(NA, length(FL)), FL)
      if (ok) {
        rf <- sub("\\.json$", ".rds", f)
        x <- if (file.exists(rf)) tryCatch(readRDS(rf)$extra$flags, error = function(e) NULL) else NULL
        if (!is.null(x)) for (k in FL) fl[[k]] <- isTRUE(x[[k]])
      }
      data.frame(setting_id = s, rep = rp, ok = ok, suc = suc, ft = ft, eflag = isTRUE(r$eflag_any),
                 TP = tp, FP = fp, FN = fn, F1 = rec_F1(tp, fp, fn),
                 stub = stub, slurm_job = if (stub) as.character(r$slurm_job %||% NA) else NA_character_,
                 pi = if (ok) g(r, "diag_post", "pi_S0") else NA_real_, ess = if (ok) g(r, "summary", "min_ess_over_N") else NA_real_,
                 rt = if (ok) g(r, "runtime_sec") else NA_real_, wall = sum(c(g(r, "wall_sec_harness"), g(r, "diag_sec")), na.rm = TRUE),
                 t(fl), stringsAsFactors = FALSE, check.names = FALSE)
    }))
  }
  P <- do.call(rbind, lapply(tab$setting_id[tab$suite == su], per_rec))
  if (is.null(P)) stop(sprintf("no %s records for S%d under %s", m, su, opt$out))
  if (anyDuplicated(P[, c("setting_id", "rep")])) stop("duplicate (setting, rep) records")
  if (isTRUE(opt$final)) {   # refuse while any timeout stub's task is still queued (it may yet be overwritten)
    st <- P[P$stub, ]
    if (nrow(st)) {
      q <- if (!is.null(opt[["queue_file"]])) readLines(opt[["queue_file"]]) else {
        x <- suppressWarnings(system2("ssh", c("nots", "squeue -h -u fb31 -r -o %i"), stdout = TRUE, stderr = FALSE))
        if (!is.null(attr(x, "status"))) stop("--final: squeue on NOTS failed (status ", attr(x, "status"), "); refusing")
        x }
      q <- trimws(q); q <- q[nzchar(q)]
      live <- is.na(st$slurm_job) | st$slurm_job %in% q
      if (any(live)) stop(sprintf("--final refused: %d timeout stub(s) whose task is still queued (or has no slurm_job): %s",
                                  sum(live), paste(sprintf("%s rep %d (%s)", st$setting_id[live], st$rep[live], st$slurm_job[live]), collapse = "; ")))
    }
    cat(sprintf("--final: %d timeout stub(s), none with a queued task; counted as computational failures\n", nrow(st)))
  }
  q <- function(x, pr) if (all(is.na(x))) NA_real_ else unname(stats::quantile(x, pr, na.rm = TRUE))
  # summary of the records d of `tasks` expected tasks
  s0_of <- setNames(tab$s0, tab$setting_id)
  summ <- function(d, sids) {
    tasks <- R * length(sids)
    if (is.null(d) || !nrow(d)) d <- P[0, ]
    k <- sum(d$suc); w <- wilson(k, tasks); o <- d[d$ok, ]
    nmiss_s0 <- sum(vapply(sids, function(s) (R - sum(d$setting_id == s)) * s0_of[[s]], 0))   # missing: FN = s0
    fpm <- sum(d$FP) / tasks; fnm <- (sum(d$FN) + nmiss_s0) / tasks
    data.frame(n_records = nrow(d), n_ok = sum(d$ok), n_failed = sum(!d$ok), n_missing = tasks - nrow(d),
      successes = k, reps = tasks, success_rate = k / tasks, wilson_lo = w[1], wilson_hi = w[2],
      fail_statistical = sum(d$ft == "statistical"), fail_search = sum(d$ft == "search"), n_computational = sum(d$ft == "computational"),
      fail_other = sum(!d$suc & !(d$ft %in% c("statistical", "search", "computational"))),
      eflag_n = sum(d$eflag), pi_S0_median = q(o$pi, .5), pi_S0_q25 = q(o$pi, .25), pi_S0_q75 = q(o$pi, .75),
      min_ess_over_N_median = q(o$ess, .5), runtime_median_sec = q(o$rt, .5), core_h_total = sum(d$wall) / 3600,
      E1 = sum(o$E1 %in% TRUE), E2 = sum(o$E2 %in% TRUE), E3 = sum(o$E3 %in% TRUE),
      low_empirical_ESS = sum(o$low_empirical_ESS %in% TRUE), escalated = sum(o$escalated %in% TRUE),
      hamming_mean = fpm + fnm, TP_mean = sum(d$TP) / tasks, FP_mean = fpm, FN_mean = fnm, F1_mean = sum(d$F1) / tasks)
  }
  summ_m <- function(d, sids) { z <- summ(d, sids)   # benchmarks: no E-flags
    if (!is_smc) z[c("eflag_n", "E1", "E2", "E3", "low_empirical_ESS", "escalated")] <- NA_integer_
    z }
  f2 <- function(x, d = 2) ifelse(is.na(x), "–", formatC(x, format = "f", digits = d))
  efs <- function(z) if (is.na(z$E1)) "–" else sprintf("%d / %d / %d / %d / %d", z$E1, z$E2, z$E3, z$low_empirical_ESS, z$escalated)
  fi <- function(x) ifelse(is.na(x), "–", as.character(x))
  sel_md <- function(z) sprintf("%s | %s | %s / %s | %s", f2(z$hamming_mean), f2(z$TP_mean), f2(z$FP_mean), f2(z$FN_mean), f2(z$F1_mean, 3))
  ts <- tab[tab$suite == su, ]
  D <- do.call(rbind, lapply(seq_len(nrow(ts)), function(i) { row <- ts[i, ]
    cbind(data.frame(setting_id = row$setting_id, label = row$label, n = row$n, p = row$p, snr = row$snr, stringsAsFactors = FALSE),
          summ_m(P[P$setting_id == row$setting_id, ], row$setting_id)) }))
  dir.create(opt$specs, recursive = TRUE, showWarnings = FALSE)
  stem <- file.path(opt$specs, sprintf("results_S%d_%s", su, m))
  write.table(D, paste0(stem, ".tsv"), sep = "\t", quote = FALSE, row.names = FALSE, na = "NA")
  coord <- function(row) if (su == 1) sprintf("(%d, %d, %g)", row$n, row$p, row$snr) else
    sprintf("(%d, %d, s=%d, ρ=%g, ν=%g, type %s)", row$n, row$p, row$s0, row$rho, row$nu, row$beta_type)
  md <- c(sprintf("# %s on S%d: %d settings x %d reps (harness/aggregate.R, %s)", m, su, nrow(D), R, format(Sys.time(), "%Y-%m-%d %H:%M")), "",
          "Success = MPM equals S0 exactly; 95% Wilson interval over the expected reps (missing and failed count as non-success).",
          "Selection accuracy over the expected reps: **a failed or missing record counts as Ŝ = ∅** (TP = FP = 0, FN = s0, F1 = 0); Hamming = FP + FN; F1 per fit = 2TP / (2TP + FP + FN).",
          if (is_smc) "E-flags = ok fits with any engine E-check (E1/E2/E3/low_empirical_ESS); by type from the rds extra$flags (ok fits): E1 / E2 / E3 / lowESS / escalated."
          else "E-flags: not applicable to benchmarks (–).", "",
          sprintf("| setting | %s | success | Wilson 95%% | mean Hamming | mean TP | mean FP / FN | mean F1 | stat / search / computational / other | E-flags | E1 / E2 / E3 / lowESS / esc | π̂(S0) median [IQR] | min ESS/N median | runtime median (s) | core-h | ok / failed / missing |",
                  if (su == 1) "(n, p, SNR)" else "(n, p, s, ρ, ν, beta-type)"),
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
  for (i in seq_len(nrow(D))) { z <- D[i, ]; md <- c(md, sprintf("| %s | %s | %d/%d | [%s, %s] | %s | %d / %d / %d / %d | %s | %s | %s [%s, %s] | %s | %s | %s | %d / %d / %d |",
    z$setting_id, coord(ts[i, ]), z$successes, z$reps, f2(z$wilson_lo, 3), f2(z$wilson_hi, 3), sel_md(z), z$fail_statistical, z$fail_search, z$n_computational,
    z$fail_other, fi(z$eflag_n), efs(z), f2(z$pi_S0_median, 3), f2(z$pi_S0_q25, 3), f2(z$pi_S0_q75, 3), f2(z$min_ess_over_N_median, 3),
    f2(z$runtime_median_sec, 0), f2(z$core_h_total, 2), z$n_ok, z$n_failed, z$n_missing)) }
  writeLines(md, paste0(stem, ".md"))
  cat("wrote", nrow(D), "rows to", paste0(stem, ".tsv"), "and .md\n")
  if (su == 2) {   # grouped table: (n, s, rho, nu), pooled over beta-type
    key <- interaction(ts$n, ts$s0, ts$rho, ts$nu, drop = TRUE, lex.order = TRUE)
    G <- do.call(rbind, lapply(split(seq_len(nrow(ts)), key), function(ii) { r0 <- ts[ii[1], ]
      cbind(data.frame(n = r0$n, p = r0$p, s = r0$s0, rho = r0$rho, nu = r0$nu, beta_types = paste(sort(unique(ts$beta_type[ii])), collapse = ","),
                       settings = paste(ts$setting_id[ii], collapse = ","), stringsAsFactors = FALSE),
            summ_m(P[P$setting_id %in% ts$setting_id[ii], ], ts$setting_id[ii])) }))
    G <- G[order(G$n, G$rho, G$nu), ]
    gs <- paste0(stem, "_by_nsrhonu")
    write.table(G, paste0(gs, ".tsv"), sep = "\t", quote = FALSE, row.names = FALSE, na = "NA")
    gm <- c(sprintf("# %s on S2 grouped by (n, s, ρ, ν), pooled over beta-type (types %s; %d settings per group, %d reps each) (harness/aggregate.R, %s)",
                    m, paste(sort(unique(ts$beta_type)), collapse = " and "), length(unique(ts$beta_type)), R, format(Sys.time(), "%Y-%m-%d %H:%M")), "",
            "Pooled factor: beta-type (1 = equally spaced support, 2 = first s). Tasks = settings in the group x reps; Wilson 95% over the tasks.",
            "Selection accuracy over the tasks: **a failed or missing record counts as Ŝ = ∅** (TP = FP = 0, FN = s0, F1 = 0); Hamming = FP + FN; F1 per fit = 2TP / (2TP + FP + FN).", "",
            "| (n, s) | ρ | ν | success / tasks | Wilson 95% | mean Hamming | mean TP | mean FP / FN | mean F1 | stat / search / computational / other | E-flags | E1 / E2 / E3 / lowESS / esc | π̂(S0) median | min ESS/N median |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for (i in seq_len(nrow(G))) { z <- G[i, ]; gm <- c(gm, sprintf("| (%d, %d) | %g | %g | %d/%d | [%s, %s] | %s | %d / %d / %d / %d | %s | %s | %s | %s |",
      z$n, z$s, z$rho, z$nu, z$successes, z$reps, f2(z$wilson_lo, 3), f2(z$wilson_hi, 3), sel_md(z), z$fail_statistical, z$fail_search, z$n_computational,
      z$fail_other, fi(z$eflag_n), efs(z), f2(z$pi_S0_median, 3), f2(z$min_ess_over_N_median, 3))) }
    writeLines(gm, paste0(gs, ".md"))
    cat("wrote", nrow(G), "groups to", paste0(gs, ".tsv"), "and .md\n")
  }
}
