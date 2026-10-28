# Inspect completed saved dev fit records; no fitting or truth access.
args <- commandArgs(TRUE)
stopifnot(length(args) %in% 3:4)
revision <- if (length(args)==4L) args[4] else ""
snapshot <- normalizePath(args[1]); aroot <- normalizePath(args[2]); out <- args[3]
source(file.path(snapshot, "code/study/adapter.R"))
report <- list()
for (p in c(500L, 1000L)) {
  name <- paste0(revision, "smoke", p)
  run <- file.path(aroot, "runs", name)
  exit <- readLines(file.path(run, "exit_status.txt"))
  paths <- list.files(file.path(aroot, paste0(revision,"dev", p), "output"),
    pattern = "^SMCBVS\\.rds$", recursive = TRUE, full.names = TRUE)
  stopifnot(length(paths) == 1L)
  prefix <- sub("\\.rds$", "", paths)
  stopifnot(smcbvs_done_valid(prefix, list()))
  record <- readRDS(paths)
  rows <- record$rows; fit <- record$fit
  stopifnot(nrow(rows) == 2L, identical(rows$rule_id, c("hpm", "pip05")),
    all(rows$method_id == "SMCBVS"), all(rows$p == p), fit$n == 200,
    all(rows$method_seed == if (p == 500L) 6420001L else 6520001L),
    all(grepl("^dev_", rows$dataset_id)), all(rows$scale_key == "c100"),
    all(nchar(rows$x_sha256) == 64L), all(nchar(rows$y_sha256) == 64L),
    length(unique(rows$x_sha256)) == 1L, length(unique(rows$y_sha256)) == 1L)
  if (nzchar(revision)) {
    stopifnot(identical(rows$role,c("primary","S0")),all(is.na(rows$converged)),
      all(is.na(rows$fold_seed)),all(is.na(rows$fold_sha256)),all(rows$adapter_mapping_status=="adopted"),
      all(rows$adapter_policy_id=="R-1-20261022"),identical(record$adapter_policy,smcbvs_r1_policy()))
    expected <- smcbvs_diagnostics(fit,fit$status)
    stopifnot(all(rows$diag_flag==expected$flag),all(rows$diag_codes==paste(expected$codes,collapse=";")))
  }
  success <- identical(exit, "0") && identical(fit$status, "completed")
  if (success) {
    stopifnot(all(rows$status == "ok"), is.finite(fit$log_Z),
      isTRUE(fit$estimates_available), !isTRUE(fit$partial_results),
      length(fit$pip_primary) == fit$p,
      all(is.finite(fit$pip_primary)), all(fit$pip_primary >= 0 & fit$pip_primary <= 1),
      is.logical(fit$cut_group), length(fit$cut_group) == 1L, !is.na(fit$cut_group),
      is.logical(fit$local_certified), length(fit$local_certified) == 1L,
      !"pip_secondary" %in% names(fit), is.data.frame(fit$stage_table),
      nrow(fit$stage_table) > 0L,
      all(c("phase", "tier", "iter", "island", "stage", "rho_V", "ess", "log_increment",
        "gibbs", "uswap_acc", "nswap_acc", "indep_acc") %in% names(fit$stage_table)),
      all(c("pilot", "diag", "final_bridge") %in% fit$stage_table$phase),
      is.data.frame(fit$stream_map), length(fit$seeding_doc) == 1L,
      all(vapply(c("local_search", "grid_construction", "bridge_stage"), function(k)
        any(vapply(fit$runtime_guard$checkpoints, function(x) x$checkpoint == k, TRUE)), TRUE)))
  }
  time <- readLines(file.path(run, "time.txt"))
  report[[name]] <- list(success = success, exit_status = exit, native_status = fit$status,
    n = fit$n, p = p, method_seed = unique(rows$method_seed), dataset_id = unique(rows$dataset_id),
    x_sha256 = unique(rows$x_sha256), y_sha256 = unique(rows$y_sha256),
    source_sha256 = unique(rows$source_sha256), log_Z = fit$log_Z,
    hpm = fit$hpm, pip05 = fit$mpm, pip_length = length(fit$pip_primary),
    flags = fit$flags, local_certified = fit$local_certified, cut_group = fit$cut_group,
    cut_group_count = fit$cut_group_count, stage_rows = nrow(fit$stage_table),
    stage_phases = as.list(table(fit$stage_table$phase)),
    allocation = fit$allocation, timings = fit$timings, fit_peak_rss_kib = fit$peak_memory_kb,
    process_time = time, record_sha256 = smcbvs_file_hash(paths), output_prefix = prefix)
}
dir.create(out, recursive=TRUE, showWarnings=FALSE)
jsonlite::write_json(report, file.path(out, "smoke_evidence.json"), auto_unbox=TRUE, pretty=TRUE, digits=NA, na="null")
saveRDS(report, file.path(out, "smoke_evidence.rds"), version=3)
cat("SMOKE_OUTPUT_AUDIT", if (all(vapply(report, `[[`, TRUE, "success"))) "PASS" else "FAILED_FIT", "\n")
quit(status=if (all(vapply(report, `[[`, TRUE, "success"))) 0L else 2L)
