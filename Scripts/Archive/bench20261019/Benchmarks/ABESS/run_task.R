#!/usr/bin/env Rscript
# run_task.R: production task of the F5 array (PROD_READINESS_BRIEF §2). One task = 10
# datasets of one p at scale c100. Tasks 1-60 are p = 500, tasks 61-120 are p = 1000. Within
# a p block, t' = 1..60 covers scenario s = ceiling(t'/10) and replicates
# 10*((t'-1) %% 10) + 1 ... + 10. Each dataset is run by run_case() (run_case.R) with its own
# error capture, so one fatal dataset does not stop the others. The task exits 1 if any
# dataset was fatal. A durable status file is written per case (.started, then .finished or
# .fatal), so that after a crash, OOM or timeout the attempted and unattempted cases can be
# told apart (Astra prod finding 7). Opens inputs/ and input manifests only; never truth/.
#
# Usage: Rscript --vanilla run_task.R --task <1..120> --data-root <bench root> \
#          --manifest-dir <dir of p{pppp}_S{s}_inputs.csv> --out-root <bench root> \
#          --run-id <id> --code-root <snapshot> --status-dir <dir> [--only <dataset_id>]
#        Rscript --vanilla run_task.R --dev 1 --data-root <dev root> ... (the 12 dev datasets,
#          dev manifest; for the dev chunk test)

task_datasets <- function(task) {
  stopifnot(length(task) == 1L, task %in% 1:120)
  p <- if (task <= 60L) 500L else 1000L
  tp <- if (task <= 60L) task else task - 60L
  s <- as.integer(ceiling(tp / 10))
  reps <- 10L * ((tp - 1L) %% 10L) + 1:10
  data.frame(p = p, scenario = s, replicate = reps,
             dataset_id = sprintf("p%04d_S%d_r%03d", p, s, reps), stringsAsFactors = FALSE)
}

# Input and manifest paths of a production task, or of the 12 dev datasets.
task_items <- function(task, data_root, manifest_dir, dev = FALSE) {
  if (dev) {
    ds <- expand.grid(scenario = 1:6, p = c(500L, 1000L))
    ids <- sprintf("dev_p%04d_S%d_r001", ds$p, ds$scenario)
    return(data.frame(dataset_id = ids,
      input = file.path(data_root, "inputs", sprintf("p%04d", ds$p), paste0(ids, ".rds")),
      manifest = file.path(data_root, "manifests", "dev_inputs_manifest.csv"), stringsAsFactors = FALSE))
  }
  ds <- task_datasets(task); pp <- sprintf("p%04d", ds$p)
  data.frame(dataset_id = ds$dataset_id,
             input = file.path(data_root, "inputs", pp, paste0(ds$dataset_id, ".rds")),
             manifest = file.path(manifest_dir, sprintf("%s_S%d_inputs.csv", pp, ds$scenario)),
             stringsAsFactors = FALSE)
}

write_status <- function(status_dir, dataset_id, kind, text) {
  f <- file.path(status_dir, paste0(dataset_id, "_c100.", kind))
  writeLines(c(format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC"), Sys.info()[["nodename"]],
               paste("job", Sys.getenv("SLURM_JOB_ID"), "task", Sys.getenv("SLURM_ARRAY_TASK_ID")), text), f)
}

# Runs the items one by one; returns the number of fatal datasets.
run_chunk <- function(items, out_root, run_id, code_root, status_dir) {
  dir.create(status_dir, recursive = TRUE, showWarnings = FALSE)
  fatal <- 0L
  for (j in seq_len(nrow(items))) {
    id <- items$dataset_id[j]
    write_status(status_dir, id, "started", "")
    t0 <- proc.time()[["elapsed"]]
    out <- tryCatch(run_case(items$input[j], items$manifest[j], out_root, run_id, scales = "c100",
                             methods = NULL, code_root = code_root),
                    error = function(e) structure(conditionMessage(e), class = "fatal"))
    wall <- proc.time()[["elapsed"]] - t0
    if (inherits(out, "fatal")) {
      fatal <- fatal + 1L; write_status(status_dir, id, "fatal", unclass(out))
      cat(sprintf("FATAL %s %s [wall %.2f s]\n", id, unclass(out), wall))
    } else {
      write_status(status_dir, id, "finished", out)
      cat(paste(out, collapse = "\n"), sprintf(" [wall %.2f s]\n", wall))
    }
    flush.console()
  }
  fatal
}

if (sys.nframe() == 0L) {
  args <- commandArgs(trailingOnly = TRUE)
  a <- list(); i <- 1L
  while (i <= length(args)) { a[[gsub("-", "_", sub("^--", "", args[i]))]] <- args[i + 1L]; i <- i + 2L }
  dev <- identical(a$dev, "1")
  for (k in c(if (!dev) c("task", "manifest_dir"), "data_root", "out_root", "run_id", "code_root", "status_dir"))
    if (is.null(a[[k]])) stop("missing --", gsub("_", "-", k))
  code_root <- normalizePath(a$code_root, mustWork = TRUE)
  source(file.path(code_root, "run_case.R"))          # run_case(); its main() is guarded
  items <- task_items(if (dev) NA else as.integer(a$task), a$data_root, a$manifest_dir, dev)
  if (!is.null(a$only) && !is.na(a$only) && nzchar(a$only)) items <- items[items$dataset_id == a$only, , drop = FALSE]
  if (!nrow(items)) stop("no dataset selected for task ", a$task)
  cat(sprintf("task %s: %d dataset(s): %s\n", if (dev) "dev" else a$task, nrow(items),
              paste(items$dataset_id, collapse = ",")))
  fatal <- run_chunk(items, a$out_root, a$run_id, code_root, a$status_dir)
  cat(sprintf("task done: %d fatal of %d\n", fatal, nrow(items)))
  quit(save = "no", status = if (fatal) 1L else 0L)
}
