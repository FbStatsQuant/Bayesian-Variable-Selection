# compare_replay.R -- merged-LS0 replay: new core (LS0 on) vs the O-LS0 prototype integration (cpp_final_run_ls0) on the
# p = 500 replay designs written by run_replay.R. Usage: Rscript compare_replay.R <replay_dir> <out_txt>
args <- commandArgs(TRUE); dir <- args[1]; out <- args[2]
TIMING <- c("timings", "seconds", "seconds_local", "seconds_total", "seconds_ls0", "peak_memory_kb", "elapsed_seconds",
            "projected_seconds", "operation_seconds", "final_detail", "seconds_per_score", "wall")
strip <- function(x) {
  if (is.list(x) && !is.data.frame(x)) { if (!is.null(names(x))) x <- x[!(names(x) %in% TIMING)]; x[] <- lapply(x, strip); x }
  else if (is.data.frame(x)) x[, !(names(x) %in% TIMING), drop = FALSE] else x
}
normprov <- function(v) { if (identical(v$phase, "local") && identical(v$iter, -2L)) { v$phase <- "ls0"; v$iter <- -1L }; v }
lsf <- c("centre", "centre_F", "path", "path_F", "scanned_centres", "scanned_F", "scan_complete", "scan_size", "termination",
         "local_limit", "local_certified", "returned", "returned_F", "moves", "n_evaluated")
ids <- unique(sub("_(on|proto)\\.rds$", "", list.files(dir, pattern = "_(on|proto)\\.rds$")))
sink(out, split = TRUE)
cat("C-ENG merged-LS0 replay (p = 500, n = 200, c100, dev generator), new core vs O-LS0 prototype,", format(Sys.time()), "\n\n")
for (id in sort(ids)) {
  fn <- file.path(dir, paste0(id, "_on.rds")); fp <- file.path(dir, paste0(id, "_proto.rds"))
  if (!file.exists(fn) || !file.exists(fp)) { cat(id, ": missing", if (!file.exists(fn)) "on", if (!file.exists(fp)) "proto", "\n"); next }
  a <- readRDS(fn); b <- readRDS(fp); N <- a$fit; P <- b$fit
  stopifnot(a$x_sha == b$x_sha, a$y_sha == b$y_sha)
  lgN <- N$score_counts$logical; lgP <- P$score_counts$logical; frN <- N$score_counts$fresh; frP <- P$score_counts$fresh
  chk <- list(
    status_same = identical(N$status, P$status) && N$status == "completed",
    islands_Z_pips_same = identical(strip(P$stage_record), strip(N$stage_record)) && identical(P$log_Z, N$log_Z) &&
      identical(P$pip_primary, N$pip_primary) && identical(P$mpm, N$mpm),
    streams_same = identical(P$streams, N$streams),
    calibration_frozen_same = identical(strip(P$calibration), strip(N$calibration)) && identical(P$frozen, N$frozen),
    final_local_same = identical(strip(P$local_search), strip(N$local_search)[names(strip(P$local_search))]),
    hpm_same = identical(P$hpm, N$hpm) && identical(P$hpm_F, N$hpm_F) && identical(normprov(P$hpm_provenance), N$hpm_provenance),
    stores_same = identical(P$top_store, N$top_store) && identical(P$leaders_gamma0, N$leaders_gamma0) && identical(P$leaders_gamma1, N$leaders_gamma1),
    near_ties_same = identical(P$near_ties, N$near_ties) && identical(P$near_tie_truncated, N$near_tie_truncated),
    ls0_archive_same = identical(P$ls0[lsf], N$ls0[lsf]),
    start_mode_same = identical(P$start_mode$model, N$start_mode$model) && identical(P$start_mode$log_gamma0, N$start_mode$log_gamma0) &&
      identical(P$start_mode$ties, N$start_mode$ties) && identical(P$start_mode$truncated, N$start_mode$truncated),
    counts_same = identical(lgP["local", ], lgN["local", ] + lgN["ls0", ]) && identical(frP["local", ], frN["local", ] + frN["ls0", ]) &&
      identical(lgP[rownames(lgP) != "local", ], lgN[!(rownames(lgN) %in% c("local", "ls0")), ]),
    cache_same = identical(P$cache, N$cache),
    hpm_before_ls0_same = identical(P$hpm_before_ls0$model, N$hpm_before_ls0$model) && identical(P$hpm_before_ls0$F, N$hpm_before_ls0$F),
    E1_E2_lowESS_same = identical(P$flags$E1, N$flags$E1) && identical(P$flags$E2, N$flags$E2) && identical(P$flags$low_empirical_ESS, N$flags$low_empirical_ESS),
    E3_new_is_final_search_only = identical(N$flags$E3, N$hpm_before_ls0$F > N$hpm_before_local$F),
    E3_diff_explained = identical(P$flags$E3, N$flags$E3) || isTRUE(N$flags$ls0_improved))
  cat(sprintf("%s  status %s  wall on %.0fs proto %.0fs  HPM {%s}  start mode {%s} ties %g trunc %s  LS0 %s moves %d n_eval %d  ls0_improved %s  ls0_hpm_changed %s  cert %s (%s)\n",
              id, N$status, a$wall, b$wall, paste(N$hpm, collapse = ","), paste(N$start_mode$model, collapse = ","), N$start_mode$ties,
              N$start_mode$truncated, N$ls0$termination, N$ls0$moves, N$ls0$n_evaluated, N$flags$ls0_improved, N$flags$ls0_hpm_changed,
              N$local_certified, N$local_certified_by))
  for (nm in names(chk)) cat(sprintf("  [%s] %s\n", if (isTRUE(chk[[nm]])) "PASS" else "FAIL", nm))
}
sink()
