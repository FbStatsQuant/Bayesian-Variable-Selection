#!/usr/bin/env Rscript
# pilot_scaling_subset.R -- thread-scaling probe through the enumerator's test hook (prefix_fraction): enumerate a fixed random
# subset of the 1,024 first-level tasks (default 3%, subset_seed 1: the same tasks for every thread count) and append one row to a CSV.
#   Rscript pilot_scaling_subset.R --input <dev study>/inputs/p0030/dev_p0030_S4_r001.rds --threads T [--fraction 0.03] [--rep 1]
#                                  --core-dir <core> --out <scaling_subset.csv>
# Partial result: nothing here is a posterior; only the timing is used. Reads X and Y only.

a <- commandArgs(trailingOnly = TRUE)
opt <- function(k, d = NULL) { i <- match(paste0("--", k), a); if (is.na(i) || i == length(a)) d else a[i + 1L] }
input <- opt("input"); thr <- as.integer(opt("threads")); frac <- as.numeric(opt("fraction", "0.03")); rep <- as.integer(opt("rep", "1"))
core <- opt("core-dir"); out <- opt("out")
if (is.null(input) || is.na(thr) || is.null(core) || is.null(out)) stop("usage: pilot_scaling_subset.R --input RDS --threads T --core-dir DIR --out CSV [--fraction 0.03] [--rep 1]")
if (grepl("truth", basename(dirname(input)))) stop("refusing a truth path")
f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1L])
enum_dir <- Sys.getenv("LOWP_ENUM_DIR", unset = normalizePath(file.path(dirname(normalizePath(f, winslash = "/")), "..", "..", "enum"), winslash = "/"))
Sys.setenv(LOWP_ENUM_DIR = enum_dir)
source(file.path(enum_dir, "lowp_enum.R"))
d <- readRDS(input)
lowp_load(core)
ex <- lowp_exact(d$X, list(c100 = as.numeric(d$Y[, "c100"]), c050 = as.numeric(d$Y[, "c050"])), threads = thr, core_dir = core, prefix_fraction = frac)
run <- attr(ex, "run")
row <- data.frame(dataset = d$dataset_id, threads = thr, rep = rep, fraction = frac, n_tasks = run$n_tasks, tasks_run = run$tasks_run,
                  models_scored = run$models_scored, wall_s = run$wall_s, wall_r_s = run$wall_r_s, sum_task_s = sum(run$task_seconds),
                  models_total = sum(choose(run$p, 0:run$K)), tasks_sha256 = digest::digest(as.integer(sort(run$tasks)), algo = "sha256"), host = Sys.info()[["nodename"]], stringsAsFactors = FALSE)
dir.create(dirname(out), recursive = TRUE, showWarnings = FALSE)
utils::write.table(row, out, sep = ",", row.names = FALSE, col.names = !file.exists(out), append = file.exists(out), qmethod = "double")
print(row)
