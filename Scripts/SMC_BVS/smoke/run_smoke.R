#!/usr/bin/env Rscript
# Root launches this on Owls, nice19, one p/scale per persistent process; no Slurm.
# Usage: Rscript run_smoke.R GENERATOR INPUT_ROOT OUTPUT_ROOT P SCALE [MEM_GB] [HOURS]
# INPUT_ROOT is a NEW, private smoke directory, never the frozen production STUDY.
if (sys.nframe() == 0L) {
  a <- commandArgs(trailingOnly = TRUE)
  if (!length(a) %in% 5:7) stop("usage: run_smoke.R GENERATOR INPUT_ROOT OUTPUT_ROOT P SCALE [MEM_GB] [HOURS]")
  this <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1L])
  here <- dirname(normalizePath(this, mustWork = TRUE))
  source(file.path(here, "generate_smoke.R"), local = FALSE)
  # generate_smcbvs_smoke loads adapter helpers. It always generates dev replicate 1 / S1.
  id <- generate_smcbvs_smoke(a[1L], a[2L], as.integer(a[4L]), 1L)
  # Smoke declares 2 GiB, matching root's 2 GiB virtual-address-space limit.
  allocation <- list(mem_gb = if (length(a) >= 6L) as.numeric(a[6L]) else 2,
    hours = if (length(a) >= 7L) as.numeric(a[7L]) else 24)
  st <- tryCatch({
    res <- smcbvs_study_fit(id, a[5L], study = a[2L], outroot = a[3L],
      run_id = sprintf("dev_smoke_p%04d_%s", as.integer(a[4L]), a[5L]),
      development = TRUE, allocation = allocation)
    cat(res$prefix, "status=", paste(res$rows$status, collapse = ","), "\n")
    if (any(res$rows$status %in% c("failed", "timeout", "not_run"))) 2L else 0L
  }, error = function(e) { message("FATAL: ", conditionMessage(e)); 1L })
  quit(save = "no", status = st)
}
