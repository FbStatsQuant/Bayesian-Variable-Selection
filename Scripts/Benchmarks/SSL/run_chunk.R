# run_chunk.R -- production driver for A2 (c = 0.5 copy): one SLURM array task = 3 datasets of one p,
# one scale (--scale, default c100), both registered method ids (A2, SSL-RS).
# Map "prod": tasks 1-200: p = 500; 201-400: p = 1000; within each p, task k = (task - 1) mod 200
# covers positions 3k .. 3k + 2 of the scenario-major order (position i: scenario i %/% 100 + 1,
# replicate i %% 100 + 1), the same dataset order as c = 1.
# Map "pilot": tasks 1-4 = p0500 S1-S3, p0500 S4-S6, p1000 S1-S3, p1000 S4-S6, replicate 1.
# Idempotent: a (case, method) with valid outputs (.done + matching .sha256) is skipped.
# One dataset's error is logged and does not stop the others; the task exits 1 if any failed.
# Usage: Rscript run_chunk.R --task <1..400> --run_id <id> --inputs <.../inputs> \
#          --manifests <.../manifests/cells> --out <.../results> [--scale c100|c050] [--map prod|pilot]
#          [--datasets id1,id2] [--methods A2,SSL-RS]

chunk_datasets <- function(task, map = "prod", chunk = 3L) {
  if (identical(map, "pilot")) {
    stopifnot(task %in% 1:4)
    p <- if (task <= 2L) 500L else 1000L
    return(sprintf("p%04d_S%d_r001", p, 3L * ((task - 1L) %% 2L) + 1:3))
  }
  stopifnot(identical(map, "prod"), task %in% 1:400)
  p <- if (task <= 200L) 500L else 1000L
  k <- (task - 1L) %% 200L
  i <- chunk * k + seq_len(chunk) - 1L
  sprintf("p%04d_S%d_r%03d", p, i %/% 100L + 1L, i %% 100L + 1L)
}

if (sys.nframe() == 0L) {
  th <- Sys.getenv(c("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"))
  if (!all(th == "1")) stop("set OMP_NUM_THREADS = OPENBLAS_NUM_THREADS = MKL_NUM_THREADS = 1 (§III.3.0)")
  a <- commandArgs(trailingOnly = TRUE)
  get_arg <- function(k, default = NULL) {
    i <- match(paste0("--", k), a)
    if (is.na(i)) { if (is.null(default)) stop("missing --", k); return(default) }
    a[i + 1L]
  }
  file_arg <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE))
  code_dir <- normalizePath(dirname(file_arg))
  source(file.path(code_dir, "run_case.R"))
  ds_arg <- get_arg("datasets", "")
  datasets <- if (nzchar(ds_arg)) strsplit(ds_arg, ",")[[1]] else
    chunk_datasets(as.integer(get_arg("task")), get_arg("map", "prod"))
  scale_key <- get_arg("scale", "c100")
  methods <- strsplit(get_arg("methods", "A2,SSL-RS"), ",")[[1]]
  cat(sprintf("task %s (scale %s): %s\n", get_arg("task", "NA"), scale_key, paste(datasets, collapse = " ")))
  errors <- character()
  for (ds in datasets) {
    p_dir <- sub("^(p[0-9]{4})_.*$", "\\1", ds)
    input <- file.path(get_arg("inputs"), p_dir, paste0(ds, ".rds"))
    r <- tryCatch(run_case(input, out_root = get_arg("out"), run_id = get_arg("run_id"), scale_key = scale_key,
                           method_ids = methods, manifest = get_arg("manifests"), code_dir = code_dir,
                           skip_valid = TRUE),
                  error = function(e) { cat(sprintf("ERROR %s: %s\n", ds, conditionMessage(e))); e })
    if (inherits(r, "error")) errors <- c(errors, ds)
  }
  cat(sprintf("task done: %d datasets, %d with errors%s\n", length(datasets), length(errors),
              if (length(errors)) paste0(" (", paste(errors, collapse = ","), ")") else ""))
  quit(status = if (length(errors)) 1L else 0L)
}
