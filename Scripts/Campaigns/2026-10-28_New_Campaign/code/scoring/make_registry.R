#!/usr/bin/env Rscript
# make_registry.R -- writes the derived expected registry (see R/registry.R) as a CSV, for audit.
# Usage: Rscript make_registry.R [--bench-dir code/bench_lowp] [--out registry_derived.csv]
args <- commandArgs(trailingOnly = TRUE)
get_arg <- function(k, default = NULL) { i <- match(paste0("--", k), args); if (is.na(i) || i == length(args)) default else args[i + 1L] }
here <- local({ f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1L]); if (is.na(f)) getwd() else dirname(normalizePath(f, winslash = "/")) })
Sys.setenv(SCORING_DIR = here)
source(file.path(here, "R", "load_all.R"))
reg <- build_registry(get_arg("bench-dir", default_bench_dir()))
utils::write.csv(reg, get_arg("out", file.path(here, "registry_derived.csv")), row.names = FALSE)
cat("wrote", nrow(reg), "registry rows (", sum(reg$in_h4), "in H4 )\n")
