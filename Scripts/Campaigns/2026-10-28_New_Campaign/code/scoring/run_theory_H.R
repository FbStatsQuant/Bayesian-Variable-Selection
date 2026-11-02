#!/usr/bin/env Rscript
# run_theory_H.R -- theory measures for ONE p >> n SMC record (no exact Z there: coverage is NA).
# Usage: Rscript run_theory_H.R --record SMCBVS.rds --inputs inputs/p0500/<dataset>.rds --truth truth/p0500/<dataset>.rds
#                               --scale c100 --out case_theory_row.csv [--td-d 0] [--restricted-d1 1] [--max-scores N] [--engine auto|slow|enum] [--core DIR]
# Default: TD with d = 0 and all nulls only (d = 1 costs ~1.4e11 scorer calls per fit at p = 1000). OPT-IN: --restricted-d1 1 adds d = 1 with the null pool
# restricted to the union of the core neighbour lists of the true variables (columns td1r_*, labelled restricted). Use --max-scores to bound the work.
args <- commandArgs(trailingOnly = TRUE)
get_arg <- function(k, default = NULL) { i <- match(paste0("--", k), args); if (is.na(i) || i == length(args)) default else args[i + 1L] }
th_here <- if (nzchar(Sys.getenv("SCORING_DIR"))) Sys.getenv("SCORING_DIR") else local({ f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1L]); if (is.na(f)) getwd() else dirname(normalizePath(f, winslash = "/")) })
Sys.setenv(SCORING_DIR = th_here)
if (!is.null(get_arg("core"))) Sys.setenv(SCORING_CORE_DIR = get_arg("core"))
source(file.path(th_here, "R", "load_all.R"))
sc_load_core(); sc_load_enum()

theory_H_run <- function(record_path, inputs_path, truth_path, scale_key, td_d = 0L, restricted_d1 = FALSE, max_scores = Inf, engine = "auto") {
  rec <- readRDS(record_path); inp <- readRDS(inputs_path); tr <- readRDS(truth_path)
  sm <- extract_smc(rec)
  ids <- list(case_id = sm$case_id %||% paste0(inp$dataset_id, "_", scale_key), dataset_id = inp$dataset_id, p = inp$p,
              scenario = inp$scenario, replicate = inp$replicate, scale_key = scale_key)
  td <- if (length(td_d) || isTRUE(restricted_d1)) list(d = td_d, restricted_d = if (isTRUE(restricted_d1)) 1L else integer(0), max_scores = max_scores, engine = engine) else NULL
  theory_case_row(inp$X, as.numeric(inp$Y[, scale_key]), sort(as.integer(tr$active)), ids, sm = sm, es = NULL, td = td)
}

if (sys.nframe() == 0L && !is.null(get_arg("record"))) {
  td_d <- as.integer(strsplit(get_arg("td-d", "0"), ",")[[1L]]); if (identical(get_arg("td-d"), "none")) td_d <- integer(0)
  ms <- as.numeric(get_arg("max-scores", "Inf"))
  row <- theory_H_run(get_arg("record"), get_arg("inputs"), get_arg("truth"), get_arg("scale", "c100"), td_d, identical(get_arg("restricted-d1", "0"), "1"), ms, get_arg("engine", "auto"))
  write_csv_na(row, get_arg("out", "case_theory_row.csv"))
  cat("wrote", get_arg("out", "case_theory_row.csv"), "\n")
}
