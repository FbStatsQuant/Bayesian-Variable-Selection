# run_strat_task.R SCENARIO REPLICATE DATA_DIR OUT_DIR [CORES=1]
# One stratified enumeration for sealed dataset S<scenario>_r<rep>. Verifies the data sha256 against DATA_DIR/manifest.csv
# (column case_id, sha256), runs exact_stratified (serial by default), checks the 2^30 count and the size-count identity,
# writes OUT_DIR/<case_id>__strat.rds atomically. Refuses to overwrite. Script dir must hold exact_stratified.{R,cpp}, engine_copy/.
args <- commandArgs(TRUE); stopifnot(length(args) >= 4)
scenario <- as.integer(args[1]); replicate <- as.integer(args[2]); data_dir <- args[3]; out_dir <- args[4]
cores <- if (length(args) >= 5) as.integer(args[5]) else 1L
here <- normalizePath(dirname(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])))
source(file.path(here, "exact_stratified.R"))
cache <- file.path(Sys.getenv("TMPDIR", "/tmp"), paste0("strat_cpp_", Sys.getenv("USER"), "_", Sys.getenv("SLURM_JOB_ID", "0"), "_", Sys.getenv("SLURM_ARRAY_TASK_ID", "0")))
load_strat_backend(here, cache = cache); on.exit(unlink(cache, recursive = TRUE), add = TRUE)
id <- sprintf("S%d_r%03d", scenario, replicate)
target <- file.path(out_dir, paste0(id, "__strat.rds"))
if (file.exists(target)) { cat("exists:", target, "\n"); quit(status = 0) }
dpath <- file.path(data_dir, paste0(id, ".rds"))
sha <- strsplit(system2("sha256sum", shQuote(dpath), stdout = TRUE), " ")[[1]][1]
man <- read.csv(file.path(data_dir, "manifest.csv"), stringsAsFactors = FALSE)
if (!identical(sha, man$sha256[man$case_id == id])) stop("data hash mismatch for ", id)
d <- readRDS(dpath); stopifnot(ncol(d$X) == 30L)
cat(sprintf("[%s] %s start, cores %d, host %s\n", format(Sys.time(), "%H:%M:%S"), id, cores, Sys.info()[["nodename"]]))
st <- exact_stratified(d$X, d$y, cores = cores, low_bits = 18L)
stopifnot(st$models_evaluated == 2^30, all(st$count_k == choose(30, 0:30)), is.finite(st$bernoulli$log_Z))
st$context <- NULL
st$case_id <- id; st$data_path <- dpath; st$data_sha256 <- sha
st$code_sha256 <- list(cpp = strsplit(system2("sha256sum", shQuote(file.path(here, "exact_stratified.cpp")), stdout = TRUE), " ")[[1]][1],
                       R = strsplit(system2("sha256sum", shQuote(file.path(here, "exact_stratified.R")), stdout = TRUE), " ")[[1]][1])
st$host <- Sys.info()[["nodename"]]; st$slurm_job <- Sys.getenv("SLURM_JOB_ID"); st$slurm_task <- Sys.getenv("SLURM_ARRAY_TASK_ID")
st$R_version <- as.character(getRversion()); st$Rcpp_version <- as.character(packageVersion("Rcpp")); st$finished_utc <- format(Sys.time(), tz = "UTC")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
tmp <- paste0(target, ".tmp", Sys.getpid()); saveRDS(st, tmp); file.rename(tmp, target)
cat(sprintf("[%s] %s done: %.0f s, Bernoulli log Z %.6f -> %s\n", format(Sys.time(), "%H:%M:%S"), id, st$seconds, st$bernoulli$log_Z, target))
