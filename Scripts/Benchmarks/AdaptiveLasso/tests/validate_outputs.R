#!/usr/bin/env Rscript
# validate_outputs.R: checks the per (case, method) files of a run against master §IV.1.1,
# the §IV.1.2 rule-row schema, the F3 registry and the §III.3.0 status/flag/code semantics.
# Reads only the run's results tree and the code folder; never reads scoring inputs.
#
# Usage: Rscript tests/validate_outputs.R --results <out>/results/<run_id> [--expect N]
# Prints one line per (case, method) and "VALIDATION PASS" or "VALIDATION FAIL".

validate_one <- function(prefix, meth, settings, engine, schema_head) {
  probs <- character()
  add <- function(...) probs <<- c(probs, paste0(...))
  files <- paste0(prefix, c(".rds", ".csv", ".sha256", ".done"))
  if (!all(file.exists(files))) return(paste("missing:", paste(basename(files[!file.exists(files)]), collapse = ",")))
  sha <- strsplit(readLines(files[3L]), "  ", fixed = TRUE)
  listed <- vapply(sha, function(x) if (length(x) == 2L) x[2L] else NA_character_, "")
  if (length(sha) != 2L || anyNA(listed) ||
      !setequal(listed, paste0(basename(prefix), c(".rds", ".csv"))))
    add("sha256 file must list exactly ", basename(prefix), ".rds and .csv")
  for (x in sha) if (length(x) == 2L &&
                     !identical(engine$file_sha256(file.path(dirname(prefix), x[2L])), x[1L]))
    add("hash mismatch for ", x[2L])
  rows <- utils::read.csv(files[2L], stringsAsFactors = FALSE, na.strings = "NA",
                          colClasses = c(support = "character", support_audit = "character",
                                         diag_codes = "character", warnings = "character",
                                         messages = "character", error = "character"))
  extra <- meth$extra_cols[[1L]]
  if (!identical(names(rows), c(schema_head, extra))) add("CSV columns differ from the schema")
  ids <- meth$rule_ids[[1L]]; roles <- meth$roles[[1L]]
  if (!identical(rows$rule_id, ids)) add("rule ids differ from the registry")
  if (!identical(rows$role, roles)) add("roles differ from the registry")
  if (sum(rows$role == "primary") != 1L) add("not exactly one primary row")
  if (any(rows$method_id != meth$method_id) || any(rows$method_label != meth$method_label) ||
      any(rows$package != meth$package) || any(rows$package_version != meth$pkg_version))
    add("method columns differ from the registry")
  if (!all(rows$status %in% c("ok", "warning", "failed"))) add("status outside ok/warning/failed")
  noisy <- rows$n_warnings > 0 | (!is.na(rows$messages) & nzchar(rows$messages))
  live <- rows$status != "failed"
  if (any(live & noisy & rows$status != "warning") || any(live & !noisy & rows$status != "ok"))
    add("status does not match the captured conditions")
  p <- rows$p[1L]
  for (i in seq_len(nrow(rows))) {
    if (rows$status[i] == "failed") {
      if (!is.na(rows$support[i]) || !is.na(rows$k[i])) add("failed row ", i, " has a support or k")
      if (is.na(rows$error[i]) || !nzchar(rows$error[i])) add("failed row ", i, " has no error text")
    } else {
      s <- engine$parse_key(rows$support[i])
      if (anyNA(s)) { add("live row ", i, " has NA support"); next }
      if (length(s) != rows$k[i]) add("row ", i, " k differs from the support")
      if (length(s) && (any(diff(s) <= 0) || min(s) < 1L || max(s) > p)) add("row ", i, " bad support")
      if (!is.na(rows$support_audit[i])) add("live row ", i, " has support_audit")
    }
    codes <- if (is.na(rows$diag_codes[i]) || !nzchar(rows$diag_codes[i])) character() else
      strsplit(rows$diag_codes[i], ";", fixed = TRUE)[[1L]]
    if (length(setdiff(codes, c(settings$DIAG_FLAG_CODES, settings$DIAG_INFO_CODES))))
      add("row ", i, " code outside the vocabulary")
    if (!is.na(rows$diag_flag[i]) && rows$diag_flag[i] != ("kkt_path" %in% codes))
      add("row ", i, " diag_flag and kkt_path code disagree")
  }
  if (length(unique(rows$diag_flag)) != 1L) add("diag_flag differs across rows of one fit")
  if (length(unique(rows$converged)) != 1L) add("converged differs across rows of one fit")
  fit_failed <- all(rows$status == "failed") && all(is.na(rows$diag_flag))
  if (fit_failed && !identical(rows$converged[1L], FALSE)) add("failed fit must have converged = FALSE")
  if (!fit_failed && !isTRUE(rows$converged[1L])) add("live F3 fit must have converged = TRUE")
  scoring <- c("tp", "fp", "fn", "exact", "error_type", sprintf("sel_a%02d", 1:14),
               sprintf("pip_a%02d", 1:14), "max_pip_null")
  if (!all(is.na(rows[, scoring]))) add("scoring columns filled at fit time")
  if (length(unique(rows$runtime_s)) != 1L || any(!is.finite(rows$runtime_s)) || any(rows$runtime_s <= 0))
    add("runtime_s not one positive value per fit")
  rds <- readRDS(files[1L])
  if (!identical(nrow(rds$rows), nrow(rows)) || !identical(rds$rows$support, rows$support) ||
      !identical(rds$rows$status, rows$status)) add("RDS rows differ from the CSV")
  if (length(rds$fit$beta) != p) add("beta has wrong length")
  if (!is.null(rds$fit$pip)) add("F3 must return pip = NULL")
  if (!fit_failed) {
    d <- rds$fit$diagnostics
    need <- c("ridge", "kappa_min", "b", "w", "v", "eps_floor", "n_floored", "path", "fold_mse",
              "fits", "candidates", "heldout", "foldid", "zmax", "index")
    if (length(setdiff(need, names(d)))) add("diagnostics missing: ", paste(setdiff(need, names(d)), collapse = ","))
    if (nrow(d$ridge) != length(settings$F3$kappa) || nrow(d$path) != settings$GRID$nlambda ||
        nrow(d$fits) != 1L + settings$COMMON$nfolds) add("diagnostic dimensions")
  }
  probs
}

validate_run <- function(results_dir, code_root, expect = NA_integer_) {
  cfg <- new.env(); sys.source(file.path(code_root, "config.R"), envir = cfg)
  rc <- new.env(); sys.source(file.path(code_root, "run_case.R"), envir = rc)
  engine <- new.env(parent = asNamespace("stats"))
  for (f in c("common.R")) sys.source(file.path(code_root, f), envir = engine)
  settings <- cfg$study_settings()
  done <- list.files(results_dir, pattern = "\\.done$", recursive = TRUE, full.names = TRUE)
  all_ok <- TRUE
  for (d in done) {
    prefix <- sub("\\.done$", "", d)
    meth <- settings$METHODS[settings$METHODS$method_id == basename(prefix), , drop = FALSE]
    probs <- if (nrow(meth) != 1L) "unregistered method file" else
      validate_one(prefix, meth, settings, engine, rc$SCHEMA_HEAD)
    cat(sprintf("%-28s %-4s %s\n", basename(dirname(prefix)), basename(prefix),
                if (length(probs)) paste("FAIL:", paste(probs, collapse = "; ")) else "ok"))
    if (length(probs)) all_ok <- FALSE
  }
  cat("files checked:", length(done), "\n")
  if (!is.na(expect) && length(done) != expect) {
    cat("expected", expect, "(case, method) outputs\n"); all_ok <- FALSE
  }
  cat(if (all_ok) "VALIDATION PASS\n" else "VALIDATION FAIL\n")
  invisible(all_ok)
}

# Production acceptance (Astra finding 2): the exact expected case set, and every result's
# provenance (directory = case_id, run_id, input hashes = cell manifest, source = snapshot).
# expected_ids: dataset ids (default: all 1,200 = p500/p1000 x S1-S6 x r001-r100).
validate_production <- function(study, run_id, code_root, snapshot_root, expected_ids = NULL) {
  if (is.null(expected_ids))
    expected_ids <- as.vector(outer(c("p0500", "p1000"), sprintf("_S%d_r%03d", rep(1:6, each = 100), rep(1:100, 6)),
                                    paste0))
  results <- file.path(study, "results", run_id)
  ok <- validate_run(results, code_root, length(expected_ids))
  rc <- new.env(); sys.source(file.path(code_root, "run_case.R"), envir = rc)
  engine <- new.env(parent = asNamespace("stats"))
  sys.source(file.path(code_root, "common.R"), envir = engine)
  tree <- rc$source_hashes(snapshot_root, engine$file_sha256)$tree
  found <- basename(dirname(list.files(results, pattern = "^F3\\.done$", recursive = TRUE, full.names = TRUE)))
  want <- paste0(expected_ids, "_c100")
  if (length(setdiff(want, found))) { ok <- FALSE; cat("MISSING cases:", length(setdiff(want, found)), head(setdiff(want, found)), "\n") }
  if (length(setdiff(found, want))) { ok <- FALSE; cat("UNEXPECTED cases:", head(setdiff(found, want)), "\n") }
  man_cache <- list()
  bad <- 0L
  for (cid in intersect(want, found)) {
    did <- sub("_c100$", "", cid); p <- substr(did, 1, 5); s <- sub("^p[0-9]+_(S[0-9])_.*$", "\\1", did)
    r <- utils::read.csv(file.path(results, p, cid, "F3.csv"), stringsAsFactors = FALSE,
                         colClasses = c(support = "character", support_audit = "character"))
    key <- paste0(p, "_", s)
    if (is.null(man_cache[[key]]))
      man_cache[[key]] <- utils::read.csv(file.path(study, "manifests", "cells", paste0(key, "_inputs.csv")),
                                          stringsAsFactors = FALSE)
    m <- man_cache[[key]][man_cache[[key]]$dataset_id == did, ]
    probs <- c(
      if (!all(r$case_id == cid)) "case_id differs from directory",
      if (!all(r$dataset_id == did)) "dataset_id",
      if (!all(r$run_id == run_id)) "run_id",
      if (!all(r$scale_key == "c100")) "scale_key",
      if (!all(r$source_sha256 == tree)) "source_sha256 differs from the snapshot",
      if (nrow(m) != 1L) "dataset not in cell manifest" else c(
        if (!all(r$inputs_sha256 == m$file_sha256)) "inputs_sha256",
        if (!all(r$x_sha256 == m$x_sha256)) "x_sha256",
        if (!all(r$y_sha256 == m$y_c100_sha256)) "y_sha256",
        if (!all(r$fold_sha256 == m$foldid_sha256)) "fold_sha256",
        if (!all(r$method_seed == m$method_seed) || !all(r$data_seed == m$data_seed)) "seeds"))
    if (length(probs)) { bad <- bad + 1L; cat(cid, "PROVENANCE FAIL:", paste(probs, collapse = "; "), "\n") }
  }
  cat("provenance checked:", length(intersect(want, found)), "cases;", bad, "failing\n")
  ok <- ok && bad == 0L
  cat(if (ok) "PRODUCTION VALIDATION PASS\n" else "PRODUCTION VALIDATION FAIL\n")
  invisible(ok)
}

if (sys.nframe() == 0L) {
  args <- commandArgs(trailingOnly = TRUE)
  get_arg <- function(k, default = NULL) {
    i <- match(k, args); if (is.na(i)) default else args[i + 1L]
  }
  f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE))
  code_root <- dirname(dirname(normalizePath(f)))
  lib <- "/projects/ml75/fb31/BVS/bench20261019/lib/R452"
  if (dir.exists(lib)) .libPaths(c(lib, .Library))
  if ("--production" %in% args) {
    # Rscript tests/validate_outputs.R --production --run-id <id> [--ids id1,id2] [--study <dir>]
    study <- get_arg("--study", "/projects/ml75/fb31/BVS/bench20261019")
    run_id <- get_arg("--run-id")
    ids <- get_arg("--ids"); if (!is.null(ids)) ids <- strsplit(ids, ",", fixed = TRUE)[[1L]]
    ok <- validate_production(study, run_id, code_root, file.path(study, "runs", run_id, "code"), ids)
  } else {
    ok <- validate_run(get_arg("--results"), code_root, as.integer(get_arg("--expect", NA)))
  }
  quit(save = "no", status = if (ok) 0L else 1L)
}
