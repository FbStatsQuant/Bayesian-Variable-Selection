# Benchmarks/Exact_best_sub/scripts/run_task.R
#   Rscript run_task.R <task_id 1..600> [output_root] [force=TRUE] [compute_exact=TRUE]
# One task = one dataset: exact best subset at every size (leaps branch-and-bound, no cap) + BIC choice.
# Reads data/datasets and data/exact; writes Benchmarks/Exact_best_sub/output/{runs,rows}.
this <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])
root <- Sys.getenv("BVS_ROOT", unset = normalizePath(file.path(dirname(this), "..", "..", ".."), mustWork = TRUE))
Sys.setenv(BVS_ROOT = root)
source(file.path(root, "data", "scripts", "common", "00_bootstrap.R"))
source(file.path(dirname(this), "best_subset_bic.R"))
e2_run_method_cli("best_subset_bic")
