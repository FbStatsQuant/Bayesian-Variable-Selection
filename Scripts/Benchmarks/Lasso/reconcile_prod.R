#!/usr/bin/env Rscript
# reconcile_prod.R -- accounting of an F1 run against the full expected inventory (every dataset of the inputs
# manifest at scale c100): which (case, F1) outputs are complete and verified, missing, or invalid; fit-level
# failures, rule failures, flags and boundary codes. Reads no truth. Writes inventory.csv, missing.txt and
# summary.txt to <out dir>. Missing cases are reruns (resubmit the same sbatch command; the runner skips done cases);
# method failures are results and are never retried.
# Usage: Rscript --vanilla reconcile_prod.R <code_dir> <results/<run_id> dir> <inputs manifest> <out dir>

args <- commandArgs(trailingOnly = TRUE)
code_dir <- args[[1]]; res_dir <- args[[2]]; manifest <- args[[3]]; out <- args[[4]]
dir.create(out, recursive = TRUE, showWarnings = FALSE)
if (nzchar(Sys.getenv("BENCH_LIB"))) .libPaths(c(Sys.getenv("BENCH_LIB"), .Library))
cfg <- new.env(parent = baseenv()); sys.source(file.path(code_dir, "config.R"), envir = cfg)
h <- new.env(parent = asNamespace("stats")); sys.source(file.path(code_dir, "common.R"), envir = h)
reg <- cfg$METHODS[cfg$METHODS$method_id == "F1", ]
man <- read.csv(manifest, stringsAsFactors = FALSE, colClasses = "character")

rc <- new.env(); sys.source(file.path(code_dir, "run_case.R"), envir = rc)   # defines functions only
src_tree <- rc$source_tree_sha256(normalizePath(code_dir), h)$tree            # expected fitting-source hash
run_id <- basename(normalizePath(res_dir))

# One case: state "done" only when the files verify AND the rows are this run's computation for this input.
case_state <- function(i) {
  ds <- man$dataset_id[i]; p <- as.integer(man$p[i]); case_id <- paste0(ds, "_c100")
  pre <- file.path(res_dir, sprintf("p%04d", p), case_id, "F1")
  row <- data.frame(dataset_id = ds, p = p, scenario = as.integer(man$scenario[i]), case_id = case_id,
                    state = "missing", reason = "", fit_failed = NA, n_rule_failed = NA, diag_flag = NA,
                    lambda_last_cvmin = NA, ebic_at_largest = NA, runtime_s = NA, k_cv_min = NA, stringsAsFactors = FALSE)
  if (dir.exists(paste0(pre, ".lock"))) row$reason <- "lock present"
  if (!file.exists(paste0(pre, ".done"))) return(row)
  bad <- function(why) { row$state <- "invalid"; row$reason <- why; row }
  if (!rc$outputs_valid(pre, h)) return(bad("files missing or sha256 mismatch"))
  csv <- read.csv(paste0(pre, ".csv"), stringsAsFactors = FALSE, na.strings = "NA",
                  colClasses = c(support = "character", diag_codes = "character", error = "character"))
  need <- c("rule_id", "run_id", "source_sha256", "inputs_sha256", "x_sha256", "y_sha256", "fold_sha256",
            "data_seed", "method_seed", "scale_key", "case_id", "method_id", "status", "error", "diag_flag",
            "diag_codes", "runtime_s", "k")
  if (!all(need %in% names(csv))) return(bad("columns missing"))
  if (nrow(csv) != 4L || !identical(csv$rule_id, reg$rule_ids[[1]])) return(bad("rule rows differ from the registry"))
  ident <- all(csv$run_id == run_id) && all(csv$source_sha256 == src_tree) && all(csv$case_id == case_id) &&
    all(csv$method_id == "F1") && all(csv$scale_key == "c100") &&
    all(csv$inputs_sha256 == man$file_sha256[i]) && all(csv$x_sha256 == man$x_sha256[i]) &&
    all(csv$y_sha256 == man$y_c100_sha256[i]) && all(csv$fold_sha256 == man$foldid_sha256[i]) &&
    all(as.character(csv$data_seed) == man$data_seed[i]) && all(as.character(csv$method_seed) == man$method_seed[i])
  if (!ident) return(bad("not this run's computation (run, source, case, inputs or seed differ)"))
  obj <- readRDS(paste0(pre, ".rds"))
  if (!identical(obj$rows$rule_id, csv$rule_id) || !identical(obj$rows$status, csv$status)) return(bad("RDS and CSV differ"))
  row$state <- "done"
  row$fit_failed <- nzchar(csv$error[1]); row$n_rule_failed <- sum(csv$status == "failed")
  row$diag_flag <- csv$diag_flag[1]; row$runtime_s <- csv$runtime_s[1]
  row$lambda_last_cvmin <- grepl("lambda_last", csv$diag_codes[1])
  row$ebic_at_largest <- sum(grepl("ebic_at_largest", csv$diag_codes[3:4]))
  row$k_cv_min <- csv$k[1]
  row
}
inv <- lapply(seq_len(nrow(man)), function(i) tryCatch(case_state(i), error = function(e) {
  data.frame(dataset_id = man$dataset_id[i], p = as.integer(man$p[i]), scenario = as.integer(man$scenario[i]),
             case_id = paste0(man$dataset_id[i], "_c100"), state = "invalid",
             reason = paste("unreadable:", conditionMessage(e)), fit_failed = NA, n_rule_failed = NA, diag_flag = NA,
             lambda_last_cvmin = NA, ebic_at_largest = NA, runtime_s = NA, k_cv_min = NA, stringsAsFactors = FALSE)
}))
inv <- do.call(rbind, inv)
write.csv(inv, file.path(out, "inventory.csv"), row.names = FALSE, na = "NA")
# missing.txt: resumable by resubmitting the same command; invalid.txt: needs investigation (the runner refuses
# to overwrite a .done whose files do not verify or belong to another computation; move the case folder aside first)
writeLines(inv$case_id[inv$state == "missing"], file.path(out, "missing.txt"))
writeLines(paste(inv$case_id, inv$reason, sep = "	")[inv$state == "invalid"], file.path(out, "invalid.txt"))
d <- inv[inv$state == "done", ]
q <- function(x) if (length(x)) paste(sprintf("%.1f", quantile(x, c(.5, .95, 1), na.rm = TRUE)), collapse = " / ") else "-"
lines <- c(sprintf("expected cases: %d (rule rows %d)", nrow(inv), 4L * nrow(inv)),
           sprintf("state: %s", paste(names(table(inv$state)), table(inv$state), sep = " = ", collapse = ", ")),
           sprintf("done: fit failures %d; rule failures %d; diag_flag TRUE %d; cv_min at lambda_last %d; ebic_at_largest (rows) %d",
                   sum(d$fit_failed), sum(d$n_rule_failed), sum(d$diag_flag %in% TRUE), sum(d$lambda_last_cvmin),
                   sum(d$ebic_at_largest)),
           sprintf("expected run_id %s, fitting-source sha256 %s", run_id, src_tree),
           sprintf("runtime_s median / p95 / max: p500 %s; p1000 %s", q(d$runtime_s[d$p == 500]), q(d$runtime_s[d$p == 1000])))
writeLines(lines, file.path(out, "summary.txt")); cat(lines, sep = "\n")
