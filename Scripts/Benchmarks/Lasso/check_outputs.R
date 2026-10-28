#!/usr/bin/env Rscript
# check_outputs.R -- validates the F1 dev-test outputs against master §IV.1.1 (files), §IV.1.2 (rule-row
# schema) and §III.3.0 (status, diag_flag, diag_codes, converged semantics; registry), and recomputes the
# rule choices from the saved diagnostics. Reads no truth.
# Usage: Rscript --vanilla check_outputs.R <code_dir> <results/<run_id> dir> <inputs manifest> <summary dir> [dataset ids]
#   dataset ids: comma-separated (default: the 12 dev datasets dev_p{0500,1000}_S{1..6}_r001)

args <- commandArgs(trailingOnly = TRUE)
code_dir <- args[[1]]; res_dir <- args[[2]]; manifest <- args[[3]]; out <- args[[4]]
dir.create(out, recursive = TRUE, showWarnings = FALSE)
if (nzchar(Sys.getenv("BENCH_LIB"))) .libPaths(c(Sys.getenv("BENCH_LIB"), .Library))
cfg <- new.env(parent = baseenv()); sys.source(file.path(code_dir, "config.R"), envir = cfg)
h <- new.env(parent = asNamespace("stats")); sys.source(file.path(code_dir, "common.R"), envir = h)
COMMON <- cfg$COMMON; reg <- cfg$METHODS[cfg$METHODS$method_id == "F1", ]
man <- read.csv(manifest, stringsAsFactors = FALSE, colClasses = "character")

schema <- c("study", "run_id", "source_sha256", "regime", "p", "scenario", "replicate", "scale_key", "scale",
            "dataset_id", "case_id", "data_seed", "fold_seed", "method_seed",
            "inputs_sha256", "x_sha256", "y_sha256", "fold_sha256",
            "method_id", "method_label", "package", "package_version", "rule_id", "role", "status",
            "converged", "diag_flag", "diag_codes", "n_warnings", "warnings", "messages", "error",
            "k", "support", "support_audit", "tp", "fp", "fn", "exact", "error_type",
            sprintf("sel_a%02d", 1:14), sprintf("pip_a%02d", 1:14), "max_pip_null",
            "runtime_s", "host", "slurm_job_id", "slurm_array_task_id", "started_utc", "finished_utc")
expected <- if (length(args) >= 5L) strsplit(args[[5]], ",", fixed = TRUE)[[1]] else
  c(sprintf("dev_p0500_S%d_r001", 1:6), sprintf("dev_p1000_S%d_r001", 1:6))

problems <- character(); rows_all <- list(); src_hashes <- character()
fail <- function(case, msg) problems <<- c(problems, paste(case, msg, sep = ": "))
for (ds in expected) {
  p <- as.integer(sub("^.*p([0-9]{4})_S.*$", "\\1", ds)); case_id <- paste0(ds, "_c100")
  dir <- file.path(res_dir, sprintf("p%04d", p), case_id); pre <- file.path(dir, "F1")
  fs <- paste0(pre, c(".rds", ".csv", ".sha256", ".done"))
  if (!all(file.exists(fs))) { fail(case_id, "missing file(s)"); next }
  sh <- read.table(fs[3], col.names = c("sha", "file"), stringsAsFactors = FALSE)
  if (!identical(sh$sha, unname(vapply(file.path(dir, sh$file), h$file_sha256, ""))) ||
      !setequal(sh$file, c("F1.rds", "F1.csv"))) fail(case_id, "sha256 mismatch")
  csv <- read.csv(fs[2], stringsAsFactors = FALSE, na.strings = "NA",
                  colClasses = c(support = "character", support_audit = "character", diag_codes = "character",
                                 warnings = "character", messages = "character", error = "character",
                                 slurm_job_id = "character", slurm_array_task_id = "character"))
  obj <- readRDS(fs[1]); r <- obj$rows
  ck <- function(cond, msg) if (!isTRUE(cond)) fail(case_id, msg)
  ck(identical(names(csv), c(schema, reg$extra_cols[[1]])), "column set/order differs from §IV.1.2 + extras")
  ck(nrow(csv) == 4L && identical(csv$rule_id, reg$rule_ids[[1]]) && identical(csv$role, reg$roles[[1]]),
     "rule ids / roles differ from the registry")
  ck(all(csv$method_id == "F1") && all(csv$method_label == "Lasso") && all(csv$package == "glmnet") &&
       all(csv$package_version == "5.1"), "method columns")
  ck(all(csv$status %in% c("ok", "warning", "failed")), "status outside ok/warning/failed")
  nf <- csv$status != "failed"
  ck(all(is.na(csv$support[!nf])) && all(is.na(csv$k[!nf])), "failed rows must have support = NA, k = NA")
  ck(all(is.na(csv$support_audit[nf])), "support_audit set on a non-failed row")
  for (i in which(nf)) {
    idx <- tryCatch(h$parse_key(csv$support[i]), error = function(e) -1L)
    ck(!identical(idx, -1L) && length(idx) == csv$k[i] && all(idx >= 1 & idx <= p), paste("bad support", csv$rule_id[i]))
  }
  has_cond <- csv$n_warnings[1] > 0 || nzchar(csv$messages[1])
  ck(all((csv$status[nf] == "warning") == has_cond), "warning status does not match captured conditions")
  ck(length(unique(csv$diag_flag)) == 1L, "diag_flag not method-wide")
  codes <- strsplit(ifelse(is.na(csv$diag_codes), "", csv$diag_codes), ";", fixed = TRUE)
  ck(all(unlist(codes) %in% c(COMMON$flag_codes, COMMON$info_codes)), "diag code outside the vocabulary")
  ck(all(vapply(codes, function(cc) "kkt_path" %in% cc, TRUE) == isTRUE(csv$diag_flag[1])) || all(!nf),
     "kkt_path code and diag_flag disagree")
  fit_failed <- nzchar(csv$error[1])
  ck(length(unique(csv$converged)) == 1L && length(unique(csv$error)) == 1L, "converged / error not fit-wide")
  for (i in 1:2) if (nf[i]) ck((("lambda_first" %in% codes[[i]]) == (csv$index[i] == 1L)) &&
                               (("lambda_last" %in% codes[[i]]) == (csv$index[i] == 200L)), "boundary codes")
  for (i in 3:4) if (nf[i]) ck((("ebic_at_largest" %in% codes[[i]]) == (csv$k[i] == csv$k_valid_max[i])), "ebic_at_largest code")
  ck(all(is.na(as.matrix(csv[, c("tp", "fp", "fn", "exact", "error_type", sprintf("sel_a%02d", 1:14),
                                  sprintf("pip_a%02d", 1:14), "max_pip_null")]))), "scoring columns filled at fit time")
  mr <- man[man$dataset_id == ds, ]
  ck(nrow(mr) == 1L && all(csv$inputs_sha256 == mr$file_sha256) && all(csv$x_sha256 == mr$x_sha256) &&
       all(csv$y_sha256 == mr$y_c100_sha256) && all(csv$fold_sha256 == mr$foldid_sha256), "input hashes vs manifest")
  ck(all(csv$method_seed == csv$data_seed + 4000000) && all(csv$method_seed == as.numeric(mr$method_seed)), "method seed")
  ck(length(unique(csv$runtime_s)) == 1L && csv$runtime_s[1] > 0, "runtime_s not shared or not positive")
  ck(all(csv$regime == "H") && all(csv$scale_key == "c100") && all(csv$scale == 1) && all(csv$p == p), "design columns")
  src_hashes <- c(src_hashes, unique(csv$source_sha256))
  # RDS consistency and recomputation of the rules from saved diagnostics
  ck(isTRUE(all.equal(r[, c("rule_id", "status", "k", "support")], csv[, c("rule_id", "status", "k", "support")],
                      check.attributes = FALSE)), "RDS rows differ from CSV")
  dg <- obj$diagnostics
  if (fit_failed) {
    # §III.3.0: a failed fit gives the registered rows, all failed, converged FALSE, beta NA
    ck(all(!nf) && all(!csv$converged) && all(is.na(csv$diag_flag)) && all(is.na(obj$beta)), "failed-fit rows")
  } else {
    ck(length(obj$beta) == p && nrow(dg$path) == 200L && nrow(dg$fits) == 11L && all(dim(dg$fold_mse) == c(10L, 200L)) &&
         all(dim(dg$heldout) == c(200L, 2L)), "diagnostic dimensions")
    i_min <- min(which(dg$path$cvm == min(dg$path$cvm)))
    i_1se <- min(which(dg$path$cvm <= dg$path$cvm[i_min] + dg$path$cvsd[i_min]))
    ck(csv$index[1] == i_min && csv$index[2] == i_1se, "CV indices do not recompute")
    ck(identical(dg$path$key[c(i_min, i_1se)], ifelse(nf[1:2], csv$support[1:2], csv$support_audit[1:2])), "CV supports")
    # converged: TRUE exactly when every one of the 11 glmnet fits returned jerr == 0 (§III.3.0)
    ck(all(dg$fits$jerr == 0L) && all(csv$converged), "a fit without error must have jerr == 0 in all 11 fits and converged TRUE")
    # EBIC criteria recomputed independently from the saved RSS, k and rank (§III.3.0 formula)
    cd <- dg$candidates; n <- 200
    valid <- cd$rank == cd$k & is.finite(cd$rss) & cd$rss > 0
    ck(identical(valid, cd$valid), "candidate validity does not recompute")
    for (g in c("ebic1", "ebic05")) {
      gam <- c(ebic1 = 1, ebic05 = 0.5)[[g]]
      crit <- ifelse(valid, n * log(cd$rss / n) + cd$k * log(n) + 2 * gam * lchoose(p, cd$k), Inf)
      ck(all(abs(crit - cd[[g]]) <= 1e-9 * pmax(1, abs(crit)) | (is.infinite(crit) & is.infinite(cd[[g]]))),
         paste(g, "criterion does not recompute"))
      o <- order(crit, cd$k, cd$key, method = "radix")[1]
      j <- match(g, csv$rule_id)
      ck(identical(cd$key[o], if (nf[j]) csv$support[j] else csv$support_audit[j]), paste(g, "does not recompute"))
    }
    ck(setequal(cd$key, unique(c("", dg$path$key[dg$path$k <= 100]))) && !anyDuplicated(cd$key), "candidate set")
    ck(isTRUE(dg$path$k[1] == 0L), "first grid point not null")
    # flag and expected rule failures derived from the saved KKT values (§III.3.1 f, h)
    tol <- cfg$GLMNET$kkt_rel_tol
    ok_full <- dg$path$kkt_full <= tol; ok_fold <- dg$path$kkt_fold_max <= tol
    ck((!all(ok_full) || !all(ok_fold)) == isTRUE(csv$diag_flag[1]), "diag_flag does not match saved KKT")
    chosen <- ifelse(nf, csv$support, csv$support_audit)
    expect_ok <- c(cv_min = ok_full[i_min] && ok_fold[i_min],
                   cv_1se = ok_full[i_1se] && ok_fold[i_1se] && ok_fold[i_min],
                   ebic1  = chosen[3] == "" || any(dg$path$key == chosen[3] & ok_full),
                   ebic05 = chosen[4] == "" || any(dg$path$key == chosen[4] & ok_full))
    ck(identical(unname(nf), unname(expect_ok)), paste("rule status does not match the KKT-derived expectation:",
                                                       paste(names(expect_ok), expect_ok, collapse = " ")))
  }
  rows_all[[ds]] <- csv
}
if (length(unique(src_hashes)) > 1L) problems <- c(problems, "source_sha256 differs across cases")
all_rows <- do.call(rbind, rows_all)
write.csv(all_rows, file.path(out, "F1_dev_rows.csv"), row.names = FALSE, na = "NA")
rep <- c(sprintf("check_outputs: %d of %d expected cases found; %d problem(s)", length(rows_all), length(expected), length(problems)),
         if (length(problems)) paste("PROBLEM", problems) else "ALL CHECKS PASSED",
         sprintf("source_sha256: %s", paste(unique(src_hashes), collapse = ", ")))
writeLines(rep, file.path(out, "check_report.txt")); cat(rep, sep = "\n")
if (length(problems)) quit(status = 1L)
