# Benchmarks/Exact_reference/compute_exact.R — exact posterior of the control model for one sealed dataset.
#   Rscript --vanilla Exact_reference/compute_exact.R SCENARIO REPLICATE [OUT_DIR] [force]     (from the Benchmarks root)
# Enumerates all 2^30 models with the frozen engine's compiled backend (Exact_reference/engine/exact_reference.cpp,
# byte-identical to Experiment 1's; hashes in engine/SHA256SUMS) and writes
#   OUT_DIR/exact/<case_id>.rds   log Z, PIPs, HPM, bookkeeping, data hash, engine hashes, versions
#   OUT_DIR/exact/<case_id>.json  receipt
# Default OUT_DIR = Exact_reference/output. Refuses to overwrite unless "force" is given. ~8 min, < 1 GB on NOTS.
# This is NOT a benchmark: it is the reference every PIP method is compared against afterwards
# (compare_to_exact.R), and it gives the exact MPM / HPM ceilings for every scenario.
args <- commandArgs(TRUE)
if (length(args) < 2L) stop("Usage: compute_exact.R SCENARIO REPLICATE [OUT_DIR] [force]")
root <- normalizePath(".", mustWork = TRUE)
source("shared/design.R"); source("shared/io.R")
scenario <- as.integer(args[1]); replicate <- as.integer(args[2])
out_dir <- if (length(args) >= 3L && !identical(args[3], "force")) args[3] else file.path(root, "Exact_reference", "output")
force <- any(args == "force")
stopifnot(scenario %in% seq_len(N_SCENARIOS), replicate %in% seq_len(N_REPLICATES))
id <- case_id(scenario, replicate)
target <- file.path(out_dir, "exact", paste0(id, ".rds"))
if (file.exists(target) && !force) { cat("exists:", target, "\n"); quit(status = 0) }
say <- function(...) { cat(sprintf("[%s] ", format(Sys.time(), "%H:%M:%S")), sprintf(...), "\n", sep = ""); flush.console() }

engine <- file.path(root, "Exact_reference", "engine")
sums <- readLines(file.path(engine, "SHA256SUMS")); sums <- sums[nzchar(sums)]
for (line in sums) { h <- sub("\\s.*$", "", line); f <- sub("^[0-9a-f]+\\s+\\*?", "", line)
  if (sha256_file(file.path(engine, f)) != h) stop("Engine hash mismatch: ", f) }
for (f in c("01_configuration_and_data.R", "02_model_and_exact_reference.R")) source(file.path(engine, f))

roots <- data_roots(root); data_dir <- data_dir_for(scenario, roots)
data_path <- file.path(data_dir, paste0(id, ".rds"))
manifest <- read.csv(file.path(data_dir, "manifest.csv"), stringsAsFactors = FALSE)
data_sha <- sha256_file(data_path)
if (data_sha != manifest$sha256[manifest$case_id == id]) stop("Dataset hash mismatch for ", id)
d <- readRDS(data_path)
stopifnot(identical(as.integer(d$scenario), scenario), identical(as.integer(d$replicate), replicate), ncol(d$X) == 30L)
say("%s: data %s (sha %s)", id, data_path, substr(data_sha, 1, 12))

cfg <- list(n = nrow(d$X), p = ncol(d$X), inclusion_probability = 0.2, variance_shape = 0.01, variance_scale = 0.01,
            prior_ridge = 1, exact_backend = "cpp", exact_low_bits = 18L, exact_chunk_size = 4096L)
context <- model_context(d$X, d$y, cfg)
cache <- Sys.getenv("E2_CPP_CACHE", unset = file.path(tempdir(), paste0("exact_cpp_", Sys.getpid())))
dir.create(cache, recursive = TRUE, showWarnings = FALSE)
Rcpp::sourceCpp(file.path(engine, "exact_reference.cpp"), env = .exact_cpp, cacheDir = cache, showOutput = FALSE)
started <- utc_now()
say("enumeration of %.0f models starts", 2^cfg$p)
exact <- exact_posterior(context, cfg, progress = TRUE)
ok <- list(models = exact$models_evaluated == 2^cfg$p, prob_sum = abs(exact$probability_sum - 1) < 1e-8,
           pips = all(is.finite(exact$pip)) && all(exact$pip >= 0 & exact$pip <= 1 + 1e-10), logZ = is.finite(exact$log_Z))
if (!all(unlist(ok))) stop("Exact reference failed checks: ", paste(names(ok)[!unlist(ok)], collapse = ", "))
truth <- d$truth$active
mpm <- which(exact$pip > 0.5); hpm <- sort(as.integer(exact$map_variables))
res <- list(case_id = id, scenario = scenario, replicate = replicate, data_path = data_path, data_sha256 = data_sha,
            model = "control: Lambda_S = (X_S'X_S + I)/n, sigma^2 ~ IG(0.01, 0.01), Bernoulli(0.2), no intercept",
            log_Z = exact$log_Z, pip = exact$pip, map_variables = hpm, map_log_score = exact$map_log_score,
            mpm = mpm, truth = truth, mpm_recovers_truth = setequal(mpm, truth), hpm_recovers_truth = setequal(hpm, truth),
            models_evaluated = exact$models_evaluated, probability_sum = exact$probability_sum, backend = exact$backend,
            seconds = exact$seconds, checks = ok,
            engine_sha256 = setNames(as.list(sub("\\s.*$", "", sums)), sub("^[0-9a-f]+\\s+\\*?", "", sums)),
            started_utc = started, ended_utc = utc_now(), host = Sys.info()[["nodename"]],
            slurm_job = Sys.getenv("SLURM_JOB_ID"), slurm_array_task = Sys.getenv("SLURM_ARRAY_TASK_ID"),
            R_version = as.character(getRversion()), Rcpp_version = as.character(utils::packageVersion("Rcpp")))
dir.create(dirname(target), recursive = TRUE, showWarnings = FALSE)
if (force && file.exists(target)) file.remove(target)
atomic_rds(res, target)
receipt <- res[setdiff(names(res), c("pip"))]; receipt$rds_sha256 <- sha256_file(target)
jf <- sub("\\.rds$", ".json", target); if (file.exists(jf)) file.remove(jf)
atomic_json(receipt, jf)
unlink(cache, recursive = TRUE)
say("done: log Z = %.6f, MPM {%s}, HPM {%s}, truth {%s}, %.0f s", exact$log_Z, paste(mpm, collapse = ","), paste(hpm, collapse = ","), paste(truth, collapse = ","), exact$seconds)
