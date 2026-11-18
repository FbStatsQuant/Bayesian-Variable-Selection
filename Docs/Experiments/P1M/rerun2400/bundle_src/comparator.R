#!/usr/bin/env Rscript
# comparator.R -- paired OLD (v2.2.1) vs NEW (v3.1) comparison of the rerun2400 fits (RERUN_2400_PLAN section 6, manager decision).
# Usage: Rscript comparator.R --old-root DIR --new-root DIR --run-id ID --out DIR [--expect-grid] [--tol-cell 1.25] [--tol-pooled 1.10] [--tol-rss 1.2]
#   OLD record: <old-root>/results/<run-id>/pPPPP/<case_id>/SMCBVS.rds        (study adapter record; record$fit = native fit, record$runtime_s)
#   NEW record: <new-root>/results/<run-id>/pPPPP/<case_id>/NEWFIT.rds        (new_fit.R record; record$fit, record$runtime_s)
# Output (in --out): per_fit.csv (one row per fit pair = one dataset x scale; S1-S6 detail), verdict.csv and verdict.md (one row per p x c, plus a
# pooled row per p and the overall verdict). Exit status 0 = NO REGRESSION, 1 = at least one pass criterion failed, 2 = usage/IO error.
# Per-fit rule (completed = status exact|completed):
#   * both completed: identical() on log_Z, log_Z_r, hpm, hpm_F, pip_primary, pip_r and status. An HPM change is DISCLOSED (not failed) iff the new
#     fit has ls0_improved TRUE and hpm_F strictly larger; that excuses hpm and hpm_F only, every other field must still be identical.
#   * old completed, new stopped: FAIL (completed->stopped). Old stopped, new completed: disclosed. Both stopped: disclosed if the status differs.
#   * X and y SHA-256 of the two sides must match; a missing record on either side is a FAIL; a resource_limit in < 2 s (admission refusal) is a FAIL.
# Per-row rule: 0 failed fits (above); every cell (p x c x S) runtime ratio  median(new)/median(old) <= tol-cell; pooled per p <= tol-pooled;
#   peak RSS ratio max(new)/max(old) <= tol-rss (peak_memory_kb of the fit, VmHWM at its end; the same definition in both cores).
args <- commandArgs(TRUE); opt <- list(`tol-cell` = "1.25", `tol-pooled` = "1.10", `tol-rss` = "1.2"); i <- 1L
while (i <= length(args)) {
  if (args[i] == "--expect-grid") { opt[["expect-grid"]] <- TRUE; i <- i + 1L; next }
  if (!startsWith(args[i], "--") || i == length(args)) { message("bad argument ", args[i]); quit(status = 2L) }
  opt[[substring(args[i], 3L)]] <- args[i + 1L]; i <- i + 2L
}
for (k in c("old-root", "new-root", "run-id", "out")) if (is.null(opt[[k]])) { message("missing --", k); quit(status = 2L) }
TOL_CELL <- as.numeric(opt[["tol-cell"]]); TOL_POOL <- as.numeric(opt[["tol-pooled"]]); TOL_RSS <- as.numeric(opt[["tol-rss"]])
LEGACY <- c("log_Z", "log_Z_r", "hpm", "hpm_F", "pip_primary", "pip_r", "status")
DONE_STATUS <- c("exact", "completed")

rec_path <- function(root, run_id, case_id, file) {
  p <- as.integer(sub("^p([0-9]{4})_.*$", "\\1", case_id))
  file.path(root, "results", run_id, sprintf("p%04d", p), case_id, file)
}
read_rec <- function(path) if (file.exists(path)) tryCatch(readRDS(path), error = function(e) NULL) else NULL
sc <- function(x) if (is.null(x) || !length(x)) NA else x[[1L]]            # scalar or NA
num <- function(x) { v <- suppressWarnings(as.numeric(sc(x))); if (length(v) != 1L) NA_real_ else v }
chr <- function(x) { v <- sc(x); if (is.null(v) || is.na(v)) NA_character_ else as.character(v) }
lgl <- function(x) { v <- sc(x); if (is.logical(v) && length(v) == 1L) v else NA }

case_ids <- function() {
  if (isTRUE(opt[["expect-grid"]])) {
    ds <- c(sprintf("p%04d_S%d_r%03d", rep(c(500L, 1000L), each = 30L), rep(rep(1:6, each = 5L), 2L), rep(c(1L, 25L, 50L, 75L, 100L), 12L)))
    both <- unlist(lapply(ds, function(d) paste0(d, c("_c100", "_c050"))))
    return(c(both, "p0500_S5_r088_c100"))   # 120 + 1 pairs
  }
  found <- character()
  for (r in c(opt[["old-root"]], opt[["new-root"]])) {
    base <- file.path(r, "results", opt[["run-id"]])
    for (pd in list.dirs(base, recursive = FALSE, full.names = TRUE)) found <- c(found, basename(list.dirs(pd, recursive = FALSE, full.names = TRUE)))
  }
  sort(unique(found))
}

compare_one <- function(case_id) {
  m <- regmatches(case_id, regexec("^p([0-9]{4})_S([1-6])_r([0-9]{3})_(c100|c050)$", case_id))[[1]]
  out <- list(case_id = case_id, p = as.integer(m[2]), S = as.integer(m[3]), r = as.integer(m[4]), c = m[5])
  o <- read_rec(rec_path(opt[["old-root"]], opt[["run-id"]], case_id, "SMCBVS.rds"))
  n <- read_rec(rec_path(opt[["new-root"]], opt[["run-id"]], case_id, "NEWFIT.rds"))
  out$have_old <- !is.null(o); out$have_new <- !is.null(n)
  fo <- if (!is.null(o)) o$fit else NULL; fn <- if (!is.null(n)) n$fit else NULL
  out$old_status <- chr(fo$status); out$new_status <- chr(fn$status)
  out$old_completed <- out$old_status %in% DONE_STATUS; out$new_completed <- out$new_status %in% DONE_STATUS
  out$x_sha_old <- chr(o$input$x_sha256); out$x_sha_new <- chr(n$x_sha256)
  out$y_sha_old <- chr(o$input$y_sha256); out$y_sha_new <- chr(n$y_sha256)
  out$x_sha_match <- if (is.na(out$x_sha_old) || is.na(out$x_sha_new)) NA else identical(out$x_sha_old, out$x_sha_new)
  out$y_sha_match <- if (is.na(out$y_sha_old) || is.na(out$y_sha_new)) NA else identical(out$y_sha_old, out$y_sha_new)
  for (f in LEGACY) out[[paste0("id_", f)]] <- if (is.null(fo) || is.null(fn)) NA else identical(fo[[f]], fn[[f]])
  out$ls0_improved <- lgl(fn$ls0_improved); out$ls0_hpm_changed <- lgl(fn$ls0_hpm_changed)
  out$hpm_F_old <- num(fo$hpm_F); out$hpm_F_new <- num(fn$hpm_F)
  out$runtime_old <- num(o$runtime_s); out$runtime_new <- num(n$runtime_s)
  out$runtime_ratio <- out$runtime_new / out$runtime_old
  out$rss_old_mb <- num(fo$peak_memory_kb) / 1024; out$rss_new_mb <- num(fn$peak_memory_kb) / 1024
  out$rss_ratio <- out$rss_new_mb / out$rss_old_mb
  out$host_old <- chr(o$environment$host); out$host_new <- chr(n$host)
  out$same_node <- if (is.na(out$host_old) || is.na(out$host_new)) NA else identical(out$host_old, out$host_new)
  # outcome
  disclosed <- character(); fails <- character()
  if (is.null(o)) fails <- c(fails, "missing_old")
  if (is.null(n)) fails <- c(fails, "missing_new")
  if (!is.null(o) && !is.null(n)) {
    if (isFALSE(out$x_sha_match) || isFALSE(out$y_sha_match)) fails <- c(fails, "data_sha_mismatch")
    if (is.na(out$x_sha_match) || is.na(out$y_sha_match)) fails <- c(fails, "data_sha_missing")
    adm <- function(st, rt) identical(st, "resource_limit") && !is.na(rt) && rt < 2
    if (adm(out$old_status, out$runtime_old) || adm(out$new_status, out$runtime_new)) fails <- c(fails, "admission_refusal")
    if (out$old_completed && out$new_completed) {
      excused <- character()
      hpm_diff <- isFALSE(out$id_hpm) || isFALSE(out$id_hpm_F)
      if (hpm_diff && isTRUE(out$ls0_improved) && !is.na(out$hpm_F_new) && !is.na(out$hpm_F_old) && out$hpm_F_new > out$hpm_F_old) {
        excused <- c("hpm", "hpm_F"); disclosed <- c(disclosed, "ls0_improved_hpm_gain")
      }
      bad <- LEGACY[!vapply(LEGACY, function(f) isTRUE(out[[paste0("id_", f)]]), NA) & !(LEGACY %in% excused)]
      if (length(bad)) fails <- c(fails, paste0("legacy_differs:", paste(bad, collapse = "+")))
    } else if (out$old_completed && !out$new_completed) fails <- c(fails, "completed_to_stopped")
    else if (!out$old_completed && out$new_completed) disclosed <- c(disclosed, "stopped_to_completed")
    else if (!identical(out$old_status, out$new_status)) disclosed <- c(disclosed, "stopped_status_differs")
  }
  out$disclosed <- paste(disclosed, collapse = ";"); out$fails <- paste(fails, collapse = ";"); out$fit_pass <- !length(fails)
  out
}

med <- function(x) if (all(is.na(x))) NA_real_ else stats::median(x, na.rm = TRUE)
ratio_of_medians <- function(d) med(d$runtime_new) / med(d$runtime_old)
verdict <- function(pf) {
  rows <- list()
  for (p in sort(unique(pf$p))) for (cc in c("c100", "c050")) {
    d <- pf[pf$p == p & pf$c == cc, , drop = FALSE]; if (!nrow(d)) next
    cells <- sort(unique(d$S)); cr <- vapply(cells, function(s) ratio_of_medians(d[d$S == s, , drop = FALSE]), 0)
    worst <- which.max(replace(cr, is.na(cr), -Inf))
    rss_ratio <- max(d$rss_new_mb, na.rm = TRUE) / max(d$rss_old_mb, na.rm = TRUE)
    nf <- function(pat) sum(grepl(pat, d$fails))
    row <- data.frame(p = p, c = cc, n_pairs = nrow(d), n_both_completed = sum(d$old_completed & d$new_completed, na.rm = TRUE),
      n_legacy_differs = nf("legacy_differs"), n_ls0_hpm_gain_disclosed = sum(grepl("ls0_improved_hpm_gain", d$disclosed)),
      n_completed_to_stopped = nf("completed_to_stopped"), n_stopped_to_completed = sum(grepl("stopped_to_completed", d$disclosed)),
      n_data_sha_problem = nf("data_sha"), n_missing = nf("missing_"), n_admission_refusal = nf("admission"),
      rt_median_old_s = med(d$runtime_old), rt_median_new_s = med(d$runtime_new), rt_ratio_row = ratio_of_medians(d),
      rt_worst_cell = paste0("S", cells[worst]), rt_worst_cell_ratio = cr[worst], n_cells_over_tol = sum(cr > TOL_CELL, na.rm = TRUE),
      rss_max_old_mb = max(d$rss_old_mb, na.rm = TRUE), rss_max_new_mb = max(d$rss_new_mb, na.rm = TRUE), rss_ratio = rss_ratio,
      n_same_node = sum(d$same_node, na.rm = TRUE), stringsAsFactors = FALSE)
    row$pass <- row$n_legacy_differs == 0 && row$n_completed_to_stopped == 0 && row$n_data_sha_problem == 0 && row$n_missing == 0 &&
      row$n_admission_refusal == 0 && row$n_cells_over_tol == 0 && isTRUE(rss_ratio <= TOL_RSS)
    rows[[length(rows) + 1L]] <- row
  }
  pooled <- do.call(rbind, lapply(sort(unique(pf$p)), function(p) {
    d <- pf[pf$p == p, , drop = FALSE]; r <- ratio_of_medians(d)
    data.frame(p = p, c = "all", n_pairs = nrow(d), rt_median_old_s = med(d$runtime_old), rt_median_new_s = med(d$runtime_new), rt_ratio_row = r,
               pooled_paired_median_ratio = med(d$runtime_ratio), pass = isTRUE(r <= TOL_POOL), stringsAsFactors = FALSE)
  }))
  list(rows = do.call(rbind, rows), pooled = pooled)
}

cases <- case_ids()
if (!length(cases)) { message("no cases found"); quit(status = 2L) }
pf <- do.call(rbind, lapply(cases, function(cid) as.data.frame(compare_one(cid), stringsAsFactors = FALSE)))
dir.create(opt$out, recursive = TRUE, showWarnings = FALSE)
utils::write.csv(pf, file.path(opt$out, "per_fit.csv"), row.names = FALSE, na = "")
v <- verdict(pf)
utils::write.csv(v$rows, file.path(opt$out, "verdict.csv"), row.names = FALSE, na = "")
utils::write.csv(v$pooled, file.path(opt$out, "verdict_pooled_p.csv"), row.names = FALSE, na = "")
overall <- all(v$rows$pass) && all(v$pooled$pass)
fmt <- function(x) if (is.numeric(x)) formatC(x, digits = 3, format = "g") else as.character(x)
tbl <- function(d) { d[] <- lapply(d, fmt); c(paste0("| ", paste(names(d), collapse = " | "), " |"), paste0("|", paste(rep("---", ncol(d)), collapse = "|"), "|"),
  apply(d, 1, function(r) paste0("| ", paste(r, collapse = " | "), " |"))) }
fail_rows <- pf[!pf$fit_pass, c("case_id", "fails"), drop = FALSE]; disc_rows <- pf[nzchar(pf$disclosed), c("case_id", "disclosed"), drop = FALSE]
md <- c("# rerun2400 verdict (OLD v2.2.1 vs NEW v3.1)", "", paste0("run_id: ", opt[["run-id"]], "; fit pairs: ", nrow(pf), "; same-node pairs: ", sum(pf$same_node, na.rm = TRUE)), "",
  paste0("**OVERALL: ", if (overall) "NO REGRESSION" else "REGRESSION / PASS CRITERIA NOT MET", "**"), "",
  paste0("Rule: legacy fields identical on completed fits; 0 completed->stopped; cell runtime ratio <= ", TOL_CELL, "; pooled per p <= ", TOL_POOL, "; RSS ratio <= ", TOL_RSS, "."), "",
  tbl(v$rows), "", "Pooled per p:", "", tbl(v$pooled), "", paste0("Failed fits: ", nrow(fail_rows)), if (nrow(fail_rows)) tbl(fail_rows),
  "", paste0("Disclosed (not failed): ", nrow(disc_rows)), if (nrow(disc_rows)) tbl(disc_rows))
writeLines(md, file.path(opt$out, "verdict.md")); cat(md, sep = "\n")
quit(save = "no", status = if (overall) 0L else 1L)
