#!/usr/bin/env Rscript
# new_fit.R -- the NEW side (frozen method v3.1) for ONE (dataset, scale): the list_pip_ab/ab_run.R route, no study adapter:
#   generate_prod_dataset(p, s, r)  ->  v3_fit(X, y, method_seed, allocation)  ->  save the fit (+ X/y sha256, runtime, host).
# Usage: new_fit.R --case p0500_S1_r001 --scale c100|c050 --gen-dir DIR --core-dir DIR --outroot DIR --run-id ID --mem-gb 2 --hours 1.75
# Seeds are never passed: method seed = data seed + 4,000,000 comes from the generator (identical to the old adapter's derivation).
# Output: OUTROOT/results/RUN_ID/pPPPP/<case>_<scale>/NEWFIT.{rds,sha256,done}. Last stdout line: tab-separated key=value.
a <- commandArgs(TRUE); opt <- list(); i <- 1L
while (i <= length(a)) { stopifnot(startsWith(a[i], "--"), i < length(a)); opt[[gsub("-", "_", substring(a[i], 3L))]] <- a[i + 1L]; i <- i + 2L }
for (k in c("case", "scale", "gen_dir", "core_dir", "outroot", "run_id", "mem_gb", "hours")) if (is.null(opt[[k]])) stop("missing --", k)
here <- dirname(normalizePath(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])))
source(file.path(here, "common_gen.R"))
stopifnot(opt$scale %in% c("c100", "c050"))
cs <- parse_case(opt$case); case_id <- paste0(opt$case, "_", opt$scale)
outdir <- file.path(opt$outroot, "results", opt$run_id, sprintf("p%04d", cs$p), case_id)
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
prefix <- file.path(outdir, "NEWFIT")
if (file.exists(paste0(prefix, ".done"))) { cat("prefix=", prefix, "\tskipped=TRUE\tv3_status=NA\n", sep = ""); quit(save = "no", status = 0L) }
utc <- function() format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC")
g <- load_prod_generator(opt$gen_dir)
d <- g$generate_prod_dataset(cs$p, cs$s, cs$r)
X <- d$inputs$X; y <- unname(d$inputs$Y[, opt$scale])
x_sha <- g$f64_sha256(X); y_sha <- g$f64_sha256(y)
seed <- d$inputs$method_seed
stopifnot(identical(seed, d$inputs$data_seed + 4000000L))
allocation <- list(mem_gb = as.double(opt$mem_gb), hours = as.double(opt$hours))   # same parsing as the old CLI (as.numeric)
core_dir <- normalizePath(opt$core_dir, mustWork = TRUE)
source(file.path(core_dir, "v3.R"), local = FALSE)
stopifnot(is.function(v3_fit))
started <- utc(); t0 <- proc.time()[["elapsed"]]
warns <- character(); err <- NULL; fit <- NULL
withCallingHandlers(tryCatch(fit <- v3_fit(X, y, seed, allocation = allocation), error = function(e) err <<- conditionMessage(e)),
  warning = function(w) { warns <<- c(warns, conditionMessage(w)); invokeRestart("muffleWarning") },
  message = function(m) invokeRestart("muffleMessage"))
runtime <- as.numeric(proc.time()[["elapsed"]] - t0); finished <- utc()
if (is.null(fit)) fit <- list(status = "R_error", message = err)
rec <- list(schema = "rerun2400-new-1", side = "new", case_id = case_id, dataset_id = cs$dataset_id, p = cs$p, scenario = cs$s,
  replicate = cs$r, scale_key = opt$scale, data_seed = d$inputs$data_seed, method_seed = seed,
  x_sha256 = x_sha, y_sha256 = y_sha, allocation = allocation, fit = fit, runtime_s = runtime, error = err, warnings = warns,
  core_dir = core_dir, v3_cpp_key = V3_CPP_KEY, host = Sys.info()[["nodename"]], pid = Sys.getpid(), started_utc = started, finished_utc = finished,
  R = R.version.string, RNGkind = RNGkind(),
  slurm = as.list(Sys.getenv(c("SLURM_JOB_ID", "SLURM_ARRAY_JOB_ID", "SLURM_ARRAY_TASK_ID", "SLURM_CPUS_PER_TASK"), unset = NA_character_)))
tmp <- paste0(prefix, ".rds.tmp.", Sys.getpid())
saveRDS(rec, tmp, compress = "xz", version = 3); stopifnot(file.rename(tmp, paste0(prefix, ".rds")))
writeLines(paste(digest::digest(file = paste0(prefix, ".rds"), algo = "sha256"), "NEWFIT.rds", sep = "  "), paste0(prefix, ".sha256"))
writeLines(c(paste("status", fit$status), paste("finished_utc", finished)), paste0(prefix, ".done"))
cat("prefix=", prefix, "\tskipped=FALSE\tv3_status=", fit$status, "\truntime_s=", format(runtime, digits = 8), "\n", sep = "")
quit(save = "no", status = 0L)
