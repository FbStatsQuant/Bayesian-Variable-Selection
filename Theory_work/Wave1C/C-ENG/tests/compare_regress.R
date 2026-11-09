# compare_regress.R -- regression comparison of old core vs new core (LS0 off / LS0 on) on saved run_fit.R outputs.
# Usage: Rscript compare_regress.R <runs_dir> <out_txt>
# runs_dir holds <tag>_old.rds, <tag>_off.rds, <tag>_on.rds for each dataset tag.
`%||%` <- function(a, b) if (is.null(a)) b else a
args <- commandArgs(TRUE); dir <- args[1]; out <- args[2]
TIMING <- c("timings", "seconds", "seconds_local", "seconds_total", "seconds_ls0", "peak_memory_kb", "elapsed_seconds",
            "projected_seconds", "operation_seconds", "final_detail", "seconds_per_score", "wall")
strip <- function(x) {
  if (is.list(x) && !is.data.frame(x)) {
    if (!is.null(names(x))) x <- x[!(names(x) %in% TIMING)]
    x[] <- lapply(x, strip); x
  } else if (is.data.frame(x)) x[, !(names(x) %in% TIMING), drop = FALSE] else x
}
lexless <- function(a, b) { n <- min(length(a), length(b)); for (i in seq_len(n)) if (a[i] != b[i]) return(a[i] < b[i]); length(a) < length(b) }
hpm_better <- function(F1, S1, F2, S2) { if (F1 != F2) return(F1 > F2); if (length(S1) != length(S2)) return(length(S1) < length(S2)); lexless(S1, S2) }
key <- function(S) paste(S, collapse = ",")
neighbours_of <- function(C, p, K) {   # all flips (additions only if |C| < K) and swaps of C, as keys
  ks <- character(0)
  for (j in seq_len(p)) { if (j %in% C) ks <- c(ks, key(setdiff(C, j))) else if (length(C) < K) ks <- c(ks, key(sort(c(C, j)))) }
  for (j in C) for (l in setdiff(seq_len(p), C)) ks <- c(ks, key(sort(c(setdiff(C, j), l))))
  ks
}
tags <- unique(sub("_(old|off|on)\\.rds$", "", list.files(dir, pattern = "_(old|off|on)\\.rds$")))
sink(out, split = TRUE)
cat("C-ENG regression comparison,", format(Sys.time()), "\nruns:", normalizePath(dir), "\ndatasets:", length(tags), "\n\n")
res <- list()
for (tg in sort(tags)) {
  o <- readRDS(file.path(dir, paste0(tg, "_old.rds"))); f <- readRDS(file.path(dir, paste0(tg, "_off.rds")))
  n <- readRDS(file.path(dir, paste0(tg, "_on.rds")))
  stopifnot(o$x_sha == f$x_sha, o$x_sha == n$x_sha, o$y_sha == n$y_sha)
  O <- o$fit; Fo <- f$fit; N <- n$fit
  r <- list(tag = tg, status_old = O$status, status_on = N$status)
  # (1) LS0 off == old, every field except measured times
  r$off_identical <- identical(strip(O), strip(Fo))
  if (!r$off_identical) {
    a <- strip(O); b <- strip(Fo)
    r$off_diff_fields <- paste(union(setdiff(names(a), names(b)), Filter(function(nm) !identical(a[[nm]], b[[nm]]), intersect(names(a), names(b)))), collapse = ";")
  }
  if (identical(O$status, "completed") && identical(N$status, "completed")) {
    # (2) sampler outputs unchanged by LS0
    same_fields <- c("stage_record", "stage_table", "streams", "log_Z", "log_Z_r", "log_Z_lower95", "log_Z_rel_m0", "pip_r",
                     "pip_primary", "mpm", "terminal_table", "island_best", "calibration", "frozen", "hpm_before_local",
                     "rb", "blocks", "neighbours", "budgets", "preprocessing", "cut_group")
    diffs <- Filter(function(nm) !identical(strip(O[[nm]]), strip(N[[nm]])), same_fields)
    r$sampler_identical <- length(diffs) == 0; if (length(diffs)) r$sampler_diff <- paste(diffs, collapse = ";")
    r$final_local_identical <- identical(strip(O$local_search), strip(N$local_search))
    # (3) flags: E2, low ESS, local_limit unchanged; E3 unchanged (LS0 does not fire E3)
    r$E3_identical <- identical(O$flags$E3, N$flags$E3)
    r$E2_lowESS_identical <- identical(O$flags$E2, N$flags$E2) && identical(O$flags$low_empirical_ESS, N$flags$low_empirical_ESS)
    r$local_limit_identical <- identical(O$flags$local_limit, N$flags$final_local_limit) &&
      identical(N$flags$local_limit, N$flags$final_local_limit || N$flags$ls0_local_limit)
    # (4) HPM can only move to a better-ranked model; F cannot fall
    r$hpm_changed <- !identical(as.integer(O$hpm), as.integer(N$hpm))
    r$hpm_ok <- if (r$hpm_changed) hpm_better(N$hpm_F, N$hpm, O$hpm_F, O$hpm) else identical(O$hpm_F, N$hpm_F) && identical(O$hpm_provenance, N$hpm_provenance)
    r$ls0_improved <- isTRUE(N$flags$ls0_improved); r$ls0_hpm_changed <- isTRUE(N$flags$ls0_hpm_changed)
    r$ls0_flag_consistent <- identical(r$ls0_improved, N$hpm_F > O$hpm_F) && identical(r$ls0_hpm_changed, r$hpm_changed)
    r$E1_changed <- !identical(O$flags$E1, N$flags$E1)
    # (5) LS0 record: centre = start mode, centre emitted, provenance
    ls0 <- N$ls0
    r$ls0_centre_is_mode <- identical(as.integer(ls0$centre), as.integer(N$start_mode$model))
    r$ls0_termination <- ls0$termination; r$ls0_moves <- ls0$moves; r$ls0_local_limit <- isTRUE(ls0$local_limit)
    r$mode_truncated <- isTRUE(N$start_mode$truncated); r$mode_ties <- N$start_mode$ties
    lg <- N$score_counts$logical; fr <- N$score_counts$fresh
    r$ls0_logical <- sum(lg["ls0", ]); r$ls0_fresh <- sum(fr["ls0", ])
    r$ls0_logical_matches_archive <- r$ls0_logical == ls0$n_evaluated + 1        # + the emitted centre
    r$counts_other_rows_identical <- identical(lg[rownames(lg) != "ls0", ], O$score_counts$logical) &&
                                     identical(fr[rownames(fr) != "ls0", ], O$score_counts$fresh)
    r$prov_ls0_iff_new_from_ls0 <- if (r$hpm_changed && identical(N$hpm_provenance$phase, "ls0")) TRUE else if (r$hpm_changed) NA else TRUE
    # (6) top store: new = top_c(old union LS0-scored); check (a) every new-only model is an LS0 centre or neighbour of one,
    #     (b) old models ranked above the new store's worst are retained
    p <- N$p; K <- N$budgets$K
    keys_old <- vapply(O$top_store$models, key, ""); keys_new <- vapply(N$top_store$models, key, "")
    ls0_keys <- unique(c(unlist(lapply(ls0$scanned_centres, function(C) c(key(C), neighbours_of(C, p, K))))))
    newonly <- setdiff(keys_new, keys_old)
    r$top_newonly <- length(newonly); r$top_newonly_from_ls0 <- all(newonly %in% ls0_keys)
    worst <- min(N$top_store$value)
    keep <- keys_old[O$top_store$value > worst]
    r$top_old_retained <- all(keep %in% keys_new)
    # (7) merged-LS0 replay: new core (on) vs the O-LS0 prototype export cpp_final_run_ls0 (proto), same data/seed.
    #     Intended metadata differences normalised: prototype LS0 events are phase "local" iter -2 (counted in the local row),
    #     the merged core uses phase "ls0" iter -1 (own row); prototype E3 is computed after LS0.
    pf <- file.path(dir, paste0(tg, "_proto.rds"))
    if (file.exists(pf)) {
      P <- readRDS(pf)$fit
      normprov <- function(v) { if (identical(v$phase, "local") && identical(v$iter, -2L)) { v$phase <- "ls0"; v$iter <- -1L }; v }
      lsf <- c("centre", "centre_F", "path", "path_F", "scanned_centres", "scanned_F", "scan_complete", "scan_size", "termination",
               "local_limit", "local_certified", "returned", "returned_F", "moves", "n_evaluated")
      lgN <- N$score_counts$logical; lgP <- P$score_counts$logical; frN <- N$score_counts$fresh; frP <- P$score_counts$fresh
      r$proto_status_same <- identical(P$status, N$status)
      r$proto_islands_same <- identical(strip(P$stage_record), strip(N$stage_record)) && identical(P$log_Z, N$log_Z) && identical(P$pip_primary, N$pip_primary)
      r$proto_hpm_same <- identical(P$hpm, N$hpm) && identical(P$hpm_F, N$hpm_F) && identical(normprov(P$hpm_provenance), N$hpm_provenance)
      r$proto_stores_same <- identical(P$top_store, N$top_store) && identical(P$leaders_gamma0, N$leaders_gamma0) && identical(P$leaders_gamma1, N$leaders_gamma1)
      r$proto_ls0_same <- identical(P$ls0[lsf], N$ls0[lsf])
      r$proto_mode_same <- identical(P$start_mode$model, N$start_mode$model) && identical(P$start_mode$log_gamma0, N$start_mode$log_gamma0) &&
        identical(P$start_mode$ties, N$start_mode$ties) && identical(P$start_mode$truncated, N$start_mode$truncated)
      r$proto_counts_same <- identical(lgP["local", ], lgN["local", ] + lgN["ls0", ]) && identical(frP["local", ], frN["local", ] + frN["ls0", ]) &&
        identical(lgP[rownames(lgP) != "local", ], lgN[!(rownames(lgN) %in% c("local", "ls0")), ]) &&
        identical(frP[rownames(frP) != "local", ], frN[!(rownames(frN) %in% c("local", "ls0")), ])
      r$proto_cache_same <- identical(P$cache, N$cache)
      r$proto_hpm_before_ls0_same <- identical(P$hpm_before_ls0$model, N$hpm_before_ls0$model) && identical(P$hpm_before_ls0$F, N$hpm_before_ls0$F)
      r$proto_E3_differs <- !identical(P$flags$E3, N$flags$E3)   # expected only when LS0 raised F (prototype E3 sees LS0)
      r$proto_E3_explained <- !r$proto_E3_differs || isTRUE(N$flags$ls0_improved)
    }
    r$local_certified_old <- O$local_certified; r$local_certified_new <- N$local_certified; r$cert_by <- N$local_certified_by %||% NA
  }
  res[[tg]] <- r
}
all_names <- unique(unlist(lapply(res, names)))
df <- do.call(rbind, lapply(res, function(r) as.data.frame(setNames(lapply(all_names, function(nm) if (is.null(r[[nm]])) NA else r[[nm]]), all_names), stringsAsFactors = FALSE)))
print(df[, c("tag", "status_old", "status_on", "off_identical")], row.names = FALSE)
cat("\n")
chk <- c("off_identical", "sampler_identical", "final_local_identical", "E3_identical", "E2_lowESS_identical", "local_limit_identical",
         "hpm_ok", "ls0_flag_consistent", "ls0_centre_is_mode", "ls0_logical_matches_archive", "counts_other_rows_identical",
         "top_newonly_from_ls0", "top_old_retained", "proto_status_same", "proto_islands_same", "proto_hpm_same",
         "proto_stores_same", "proto_ls0_same", "proto_mode_same", "proto_counts_same", "proto_cache_same",
         "proto_hpm_before_ls0_same", "proto_E3_explained")
for (c in chk) if (c %in% names(df)) cat(sprintf("%-32s TRUE in %d / %d (NA %d)\n", c, sum(df[[c]] %in% TRUE), nrow(df), sum(is.na(df[[c]]))))
cat("\nHPM changed by LS0:", sum(df$hpm_changed %in% TRUE), "; ls0_improved:", sum(df$ls0_improved %in% TRUE),
    "; E1 changed:", sum(df$E1_changed %in% TRUE), "; LS0 move_limit:", sum(df$ls0_local_limit %in% TRUE),
    "; start-mode truncated:", sum(df$mode_truncated %in% TRUE), "\n")
cat("local_certified old -> new:\n"); print(table(old = df$local_certified_old, new = df$local_certified_new, useNA = "ifany"))
cat("certificate source:\n"); print(table(df$cert_by, useNA = "ifany"))
cat("LS0 termination:\n"); print(table(df$ls0_termination, useNA = "ifany"))
bad <- df[!(df$off_identical %in% TRUE) | (df$status_on == "completed" & !(df$sampler_identical %in% TRUE & df$E3_identical %in% TRUE & df$hpm_ok %in% TRUE)), ]
if (nrow(bad)) { cat("\nROWS WITH UNEXPECTED DIFFERENCES:\n"); print(bad) }
saveRDS(df, sub("\\.txt$", ".rds", out))
sink()
