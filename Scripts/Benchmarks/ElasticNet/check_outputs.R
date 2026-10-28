#!/usr/bin/env Rscript
# check_outputs.R -- validates the F2 dev-test outputs against master §IV.1.1 (files),
# §IV.1.2 (rule-row schema) and §III.3.0 (status, diag_flag, diag_codes, converged), and
# summarises the per-case diagnostics. Does not read truth/.
# Usage: Rscript check_outputs.R <code_dir> <results/<run_id> dir> <inputs_manifest.csv> <out_dir> [dataset_ids]
# dataset_ids: optional comma-separated list (default: the 12 r001 datasets at p = 500, 1000).

args <- commandArgs(TRUE)
if (!length(args) %in% 4:5) stop("usage: check_outputs.R <code_dir> <results_run_dir> <manifest> <out_dir> [ids]")
code_dir <- normalizePath(args[1]); res_dir <- normalizePath(args[2]); out_dir <- args[4]
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
cfg <- new.env(parent = baseenv()); sys.source(file.path(code_dir, "config.R"), envir = cfg)
S <- cfg$make_settings(); .libPaths(c(S$COMMON$study_lib, .Library))
io <- new.env(); sys.source(file.path(code_dir, "common.R"), envir = io)
mf <- read.csv(args[3], stringsAsFactors = FALSE, colClasses = "character")
mf <- if (length(args) == 5L) mf[mf$dataset_id %in% strsplit(args[5], ",", fixed = TRUE)[[1]], ] else
  mf[as.integer(mf$p) %in% c(500L, 1000L) & grepl("_r001$", mf$dataset_id), ]
if (!nrow(mf)) stop("no manifest rows selected")
if (length(args) == 5L) {
  want <- strsplit(args[5], ",", fixed = TRUE)[[1]]
  if (!setequal(want, mf$dataset_id))
    stop("requested ids missing from the manifest: ", paste(setdiff(want, mf$dataset_id), collapse = ","))
}
reg <- S$METHODS[S$METHODS$method_id == "F2", ]
# Provenance reference: the code snapshot passed as code_dir (same convention as run_case.R).
runner <- new.env(); sys.source(file.path(code_dir, "run_case.R"), envir = runner)
snap <- runner$code_hashes(code_dir, io)

SCHEMA <- c("study", "run_id", "source_sha256", "regime", "p", "scenario", "replicate",
            "scale_key", "scale", "dataset_id", "case_id", "data_seed", "fold_seed", "method_seed",
            "inputs_sha256", "x_sha256", "y_sha256", "fold_sha256", "method_id", "method_label",
            "package", "package_version", "rule_id", "role", "status", "converged", "diag_flag",
            "diag_codes", "n_warnings", "warnings", "messages", "error", "k", "support",
            "support_audit", "tp", "fp", "fn", "exact", "error_type",
            sprintf("sel_a%02d", 1:14), sprintf("pip_a%02d", 1:14), "max_pip_null",
            "runtime_s", "host", "slurm_job_id", "slurm_array_task_id", "started_utc", "finished_utc")
EXTRA <- c("alpha", "lambda", "index", "cv_mean", "cv_se", "rss", "ebic1_value", "crit_value",
           "k_valid_max", "k_path_max")
VOCAB <- c("kkt_path", "path_truncated", "L_saturated", "elbo_drop", "sigma2_floor",
           "capped_intermediate", "tail_unstable", "fixed_point", "ess_tau", "ess_ci95",
           "crn_mismatch", "lambda_first", "lambda_last", "alpha_edge", "kappa_edge",
           "floored_selected", "ebic_at_largest")
F2_FLAGS <- "kkt_path"

problems <- character(); summ <- list()
bad <- function(case, msg) problems <<- c(problems, paste0(case, ": ", msg))
for (i in seq_len(nrow(mf))) {
  m <- mf[i, ]; case_id <- paste0(m$dataset_id, "_c100")
  prefix <- file.path(res_dir, sprintf("p%04d", as.integer(m$p)), case_id, "F2")
  files <- paste0(prefix, c(".rds", ".csv", ".sha256", ".done"))
  if (!all(file.exists(files))) { bad(case_id, "missing output files"); next }
  sha <- readLines(files[3]); want <- sub("  .*$", "", sha)
  if (!identical(want, unname(vapply(files[1:2], io$file_sha256, "")))) bad(case_id, "sha256 mismatch")
  r <- read.csv(files[2], stringsAsFactors = FALSE, na.strings = "NA",
                colClasses = c(support = "character", support_audit = "character",
                               diag_codes = "character", warnings = "character",
                               messages = "character", error = "character"))
  o <- readRDS(files[1]); p <- as.integer(m$p)
  # All schema and extra columns present, nothing else; schema columns in §IV.1.2 order.
  if (!setequal(names(r), c(SCHEMA, EXTRA)) || !identical(names(r)[names(r) %in% SCHEMA], SCHEMA))
    bad(case_id, "column set/order")
  # The CSV must be exactly the RDS rows written by write.csv (compared as text, so column
  # types such as the character slurm_job_id do not matter).
  tmp_csv <- tempfile(fileext = ".csv"); utils::write.csv(o$rows, tmp_csv, row.names = FALSE, na = "NA")
  if (!identical(readLines(tmp_csv), readLines(files[2]))) bad(case_id, "CSV differs from the rows stored in the RDS")
  unlink(tmp_csv)
  if (!identical(r$rule_id, reg$rule_ids[[1]]) || !identical(r$role, reg$roles[[1]])) bad(case_id, "rule ids/roles")
  if (!all(r$status %in% c("ok", "warning", "failed"))) bad(case_id, "status vocabulary")
  # Failure takes precedence over a warning; non-failed rows are "warning" iff a condition was captured.
  nf <- r$status != "failed"
  cond <- r$n_warnings > 0 | (!is.na(r$messages) & nzchar(r$messages))
  if (any(nf) && !all((r$status[nf] == "warning") == cond[nf]))
    bad(case_id, "warning status inconsistent with captured conditions")
  if (!all(r$x_sha256 == m$x_sha256) || !all(r$y_sha256 == m$y_c100_sha256) ||
      !all(r$fold_sha256 == m$foldid_sha256) || !all(r$inputs_sha256 == m$file_sha256)) bad(case_id, "input hashes")
  if (!all(r$method_seed == as.integer(m$data_seed) + 4000000L)) bad(case_id, "method_seed")
  if (!all(r$source_sha256 == snap$tree) || !identical(o$source_hashes, snap$files))
    bad(case_id, "outputs were not produced by the supplied code snapshot")
  if (!identical(o$settings[c("COMMON", "GRID", "GLMNET", "F2")], S[c("COMMON", "GRID", "GLMNET", "F2")]))
    bad(case_id, "settings stored in the RDS differ from the snapshot's config.R")
  if (!all(r$method_id == "F2") || !all(r$package_version == "5.1") || !all(r$regime == "H")) bad(case_id, "method cols")
  if (!all(is.na(r[, c("tp", "fp", "fn", "exact", "error_type", sprintf("sel_a%02d", 1:14))]))) bad(case_id, "truth cols filled")
  fitfail <- all(r$status == "failed") && all(is.na(r$support_audit))
  if (!fitfail && !all(r$converged)) bad(case_id, "converged must be TRUE when the fit did not fail")
  if (length(unique(r$diag_flag)) != 1L) bad(case_id, "diag_flag not method-wide")
  toks <- unlist(strsplit(r$diag_codes[nzchar(r$diag_codes)], ";", fixed = TRUE))
  if (!all(toks %in% VOCAB)) bad(case_id, "diag_codes vocabulary")
  for (j in seq_len(nrow(r))) {
    codes <- strsplit(r$diag_codes[j], ";", fixed = TRUE)[[1]]
    if (isTRUE(r$diag_flag[j]) != any(codes %in% F2_FLAGS)) bad(case_id, "flag/code mismatch")
    if (r$status[j] == "failed") {
      if (!is.na(r$support[j]) || !is.na(r$k[j])) bad(case_id, "failed row has support or k")
    } else {
      s <- io$parse_key(r$support[j])
      if (is.na(r$support[j]) || length(s) != r$k[j] || anyDuplicated(s) || is.unsorted(s) ||
          any(s < 1 | s > p) || !identical(io$support_key(s), r$support[j])) bad(case_id, "support format")
    }
  }
  if (!(length(unique(r$runtime_s)) == 1L && r$runtime_s[1] > 0)) bad(case_id, "runtime")
  d <- o$diagnostics
  if (fitfail) {
    if (!all(is.na(o$beta)) || length(o$beta) != p || any(r$converged) || !all(is.na(r$diag_flag)) ||
        any(is.na(r$error)) || !is.null(o$pip)) bad(case_id, "failed-fit semantics")
  } else {
    if (nrow(d$cv_table) != 1000L || nrow(d$fits) != 55L || !identical(dim(d$kkt), c(55L, 200L)) ||
        !identical(dim(d$fold_mse), c(5L, 10L, 200L)) || !identical(dim(d$heldout), c(200L, 2L)))
      bad(case_id, "diagnostic dimensions")
    if (length(o$beta) != p || !is.null(o$pip)) bad(case_id, "beta/pip")
    cm <- o$rows[o$rows$rule_id == "cv_min", ]           # exact values (CSV rounds to 15 digits)
    key_beta <- io$support_key(which(o$beta != 0))
    key_path <- d$paths[[d$chosen$alpha_index]][d$chosen$i_min]
    if (!identical(key_beta, key_path) || (cm$status != "failed" && !identical(cm$support, key_beta)))
      bad(case_id, "cv_min support != beta support")
    if (any(d$fits$jerr != 0)) bad(case_id, "nonzero jerr")
    if (max(d$kkt) > S$GLMNET$kkt_rel_tol && !all(r$diag_flag)) bad(case_id, "KKT violation not flagged")
    best <- which.min(d$cv_table$cvm)
    if (d$cv_table$cvm[best] != min(d$cv_table$cvm) || cm$cv_mean != min(d$cv_table$cvm)) bad(case_id, "cv_min not at the minimum")
  }
  ch <- if (fitfail) list(alpha = NA, i_min = NA, i_1se = NA) else d$chosen
  summ[[case_id]] <- data.frame(case_id = case_id, p = p, alpha_star = ch$alpha,
                                i_min = ch$i_min, i_1se = ch$i_1se,
                                k_cv_min = r$k[1], k_cv_1se = r$k[2], k_ebic1 = r$k[3], k_ebic05 = r$k[4],
                                max_kkt = if (!fitfail) max(d$kkt) else NA,
                                n_fits_kkt_viol = if (!fitfail) sum(apply(d$kkt, 1, max) > S$GLMNET$kkt_rel_tol) else NA,
                                max_npasses = if (!fitfail) max(d$fits$npasses) else NA,
                                diag_flag = r$diag_flag[1], codes_cv_min = r$diag_codes[1],
                                statuses = paste(r$status, collapse = ","),
                                error = if (fitfail) r$error[1] else "",
                                n_warn = r$n_warnings[1], runtime_s = round(r$runtime_s[1], 2),
                                rds_kb = round(file.size(files[1]) / 1024, 1),
                                host = r$host[1], job = paste0(r$slurm_job_id[1], "_", r$slurm_array_task_id[1]))
}
tab <- do.call(rbind, summ); rownames(tab) <- NULL
write.csv(tab, file.path(out_dir, "check_summary.csv"), row.names = FALSE)
writeLines(if (length(problems)) problems else "no problems", file.path(out_dir, "check_problems.txt"))
options(width = 220); print(tab, row.names = FALSE)
cat(sprintf("\n%d cases checked, %d problems\n", nrow(tab), length(problems)))
if (length(problems)) { cat(problems, sep = "\n"); quit(status = 1L) }
