#!/usr/bin/env Rscript
# validate_dev.R -- checks F4 outputs (dev test, smoke test or production) against master §IV.1.1-§IV.1.2
# and §III.3.0: files and hashes, schema columns, registered rule ids and roles, status / flag / code /
# converged semantics, scoring columns empty at fit time, CSV rows equal to the RDS rows, identity of each
# output set with its directory, run id and input manifest, point passes and the candidate table
# re-derived from the saved diagnostics, EBIC choices recomputed. Reads only the results tree, config.R
# and (optionally) the inputs manifest; never truth/.
# Usage: Rscript validate_dev.R <code_dir> <results_root> <cases> <out_file> [run_id] [inputs_manifest]
#   cases: "-" = the 12 dev cases; "PROD" = the 1,200 production cases (c100); or a comma-separated list
#   of case paths under results_root (e.g. p1000/p1000_S4_r001_c100).
# A case-method pair with none of its four files is listed as missing (in <out_file>.missing.csv) and
# is not a problem; any other defect is a problem. Exits 1 if any problem is found.

args <- commandArgs(trailingOnly = TRUE)
code_dir <- normalizePath(args[1L]); root <- normalizePath(args[2L]); out_file <- args[4L]
expect_run <- if (length(args) >= 5L && args[5L] != "-") args[5L] else NA_character_
man <- if (length(args) >= 6L) utils::read.csv(args[6L], stringsAsFactors = FALSE) else NULL
source(file.path(code_dir, "config.R")); .libPaths(c(STUDY_LIB, .Library))
source(file.path(code_dir, "common.R"))
schema <- c("study", "run_id", "source_sha256", "regime", "p", "scenario", "replicate", "scale_key",
  "scale", "dataset_id", "case_id", "data_seed", "fold_seed", "method_seed", "inputs_sha256",
  "x_sha256", "y_sha256", "fold_sha256", "method_id", "method_label", "package", "package_version",
  "rule_id", "role", "status", "converged", "diag_flag", "diag_codes", "n_warnings", "warnings",
  "messages", "error", "k", "support", "support_audit", "tp", "fp", "fn", "exact", "error_type",
  sprintf("sel_a%02d", 1:14), sprintf("pip_a%02d", 1:14), "max_pip_null", "runtime_s", "host",
  "slurm_job_id", "slurm_array_task_id", "started_utc", "finished_utc",
  "lambda", "rss", "crit_value", "path_index", "k_valid_max", "k_path_max")
cases <- if (identical(args[3L], "-")) {
  c(sprintf("p0500/dev_p0500_S%d_r001_c100", 1:6), sprintf("p1000/dev_p1000_S%d_r001_c100", 1:6))
} else if (identical(args[3L], "PROD")) {
  g <- expand.grid(r = 1:100, s = 1:6, p = c(500L, 1000L))
  sprintf("p%04d/p%04d_S%d_r%03d_c100", g$p, g$p, g$s, g$r)
} else strsplit(args[3L], ",", fixed = TRUE)[[1L]]
problems <- character(); missing <- character(); nchecked <- 0L
bad <- function(...) problems <<- c(problems, paste0(...))
same_txt <- function(a, b) identical(ifelse(is.na(a), "<NA>", as.character(a)), ifelse(is.na(b), "<NA>", as.character(b)))

check_pair <- function(cs, mid) {
  pre <- file.path(root, cs, mid)
  f <- paste0(pre, c(".rds", ".csv", ".sha256", ".done"))
  if (!any(file.exists(f))) { missing <<- c(missing, paste(cs, mid, sep = ",")); return(invisible()) }
  if (!all(file.exists(f))) { bad(cs, " ", mid, ": incomplete file set"); return(invisible()) }

  h <- strsplit(readLines(f[3]), "  ", fixed = TRUE)
  if (length(h) != 2L || !identical(sort(vapply(h, `[`, "", 2L)), sort(paste0(mid, c(".csv", ".rds")))))
    bad(cs, " ", mid, ": .sha256 does not list exactly the .rds and .csv")
  for (x in h) if (!identical(file_sha256(file.path(dirname(pre), x[2])), x[1])) bad(cs, " ", mid, ": hash ", x[2])
  r <- read.csv(f[2], stringsAsFactors = FALSE, colClasses = c(support = "character", support_audit = "character",
                diag_codes = "character", warnings = "character", messages = "character", error = "character"))
  o <- readRDS(f[1]); mrow <- METHODS[METHODS$method_id == mid, ]
  # Identity: CSV rows equal the RDS rows; the set belongs to its directory, method, run and inputs.
  rr <- o$rows
  for (cn in c("run_id", "case_id", "dataset_id", "method_id", "rule_id", "role", "status", "support",
               "support_audit", "k", "diag_codes", "source_sha256", "inputs_sha256", "x_sha256",
               "y_sha256", "fold_sha256", "path_index"))
    if (!same_txt(r[[cn]], rr[[cn]])) bad(cs, " ", mid, ": CSV and RDS differ in ", cn)
  for (cn in c("crit_value", "rss", "lambda", "runtime_s"))
    if (any(xor(is.na(r[[cn]]), is.na(rr[[cn]]))) ||
        any(abs(r[[cn]] - rr[[cn]]) > 1e-12 * pmax(1, abs(rr[[cn]])), na.rm = TRUE)) bad(cs, " ", mid, ": CSV and RDS differ in ", cn)
  if (!all(r$case_id == basename(dirname(pre))) || !identical(o$case_id, basename(dirname(pre))) ||
      !identical(o$method_id, mid) || !all(r$method_id == mid) ||
      !all(sprintf("p%04d", r$p) == basename(dirname(dirname(pre)))))
    bad(cs, " ", mid, ": output set does not belong to its directory")
  if (!is.na(expect_run) && !all(r$run_id == expect_run)) bad(cs, " ", mid, ": run id differs from ", expect_run)
  if (!is.null(man)) {
    m <- man[man$dataset_id == r$dataset_id[1], , drop = FALSE]
    if (nrow(m) != 1L || m$file_sha256 != r$inputs_sha256[1] || m$x_sha256 != r$x_sha256[1] ||
        m$foldid_sha256 != r$fold_sha256[1] || m[[paste0("y_", r$scale_key[1], "_sha256")]] != r$y_sha256[1])
      bad(cs, " ", mid, ": input hashes differ from the inputs manifest")
  }
  if (!identical(names(r), schema)) bad(cs, " ", mid, ": columns differ from schema")
  if (!identical(r$rule_id, mrow$rule_ids[[1]]) || !identical(r$role, mrow$roles[[1]])) bad(cs, " ", mid, ": rule ids/roles")
  if (!all(r$method_id == mid & r$method_label == mrow$method_label & r$package == "ncvreg" &
           r$package_version == "3.16.0")) bad(cs, " ", mid, ": method columns")
  if (!all(r$status %in% c("ok", "warning", "failed"))) bad(cs, " ", mid, ": status value")
  if (any(r$status == "warning" & r$n_warnings == 0 & is.na(r$messages))) bad(cs, " ", mid, ": warning without condition")
  if (any(r$status == "ok" & (r$n_warnings > 0 | !is.na(r$messages)))) bad(cs, " ", mid, ": ok despite condition")
  okr <- r$status != "failed"
  if (any(is.na(r$support[okr])) || any(!is.na(r$support[!okr])) || any(is.na(r$k[okr])) || any(!is.na(r$k[!okr])) ||
      any(r$k[okr] != lengths(lapply(r$support[okr], parse_key)))) bad(cs, " ", mid, ": support/k")
  if (length(unique(r$diag_flag)) != 1L || length(unique(r$converged)) != 1L || length(unique(r$runtime_s)) != 1L)
    bad(cs, " ", mid, ": fit-level column not constant across rules")
  if (!all(is.na(r[, c("tp", "fp", "fn", "exact", "error_type")]))) bad(cs, " ", mid, ": scoring columns filled")
  codes <- unlist(strsplit(ifelse(is.na(r$diag_codes), "", r$diag_codes), ";"))
  if (!all(codes %in% c("kkt_path", "path_truncated", "ebic_at_largest"))) bad(cs, " ", mid, ": code outside F4 set")
  # Three kinds of failure (§III.3.0): the fit errored (no path saved), a fit-level gate failed
  # (path saved, every rule failed), or individual rules failed (fit otherwise valid).
  path <- o$diagnostics$path
  if (is.null(path)) {                                        # fit errored
    if (!all(r$status == "failed") || any(!is.na(r$support_audit)) || any(r$converged) ||
        any(!is.na(o$beta)) || length(o$beta) != r$p[1] || !is.null(o$pip) || any(is.na(r$error)))
      bad(cs, " ", mid, ": errored fit rows not in the failed-fit form")
    return(invisible())
  }
  gate <- length(o$diagnostics$gate_failures) > 0L
  flag_expected <- any(path$kkt_max > CONFIG$F4$kkt_abs_tol) || nrow(path) < CONFIG$GRID$nlambda
  if (!identical(unique(r$diag_flag), flag_expected)) bad(cs, " ", mid, ": diag_flag inconsistent with path")
  conv_expected <- !gate && nrow(path) == CONFIG$GRID$nlambda && o$diagnostics$total_iter < CONFIG$F4$maxit
  if (!identical(unique(r$converged), conv_expected)) bad(cs, " ", mid, ": converged inconsistent")
  if (gate && (!all(r$status == "failed") || any(is.na(r$support_audit)) || any(!is.na(o$beta))))
    bad(cs, " ", mid, ": gate-failed fit rows not in the failed form")
  # Point passes derived here from kkt_max, the tolerance and the total-iteration check (§III.3.4 e
  # step 5), not taken from the saved `passes`; the saved column must agree.
  passes_d <- path$kkt_max <= CONFIG$F4$kkt_abs_tol
  if (o$diagnostics$total_iter >= CONFIG$F4$maxit) passes_d[length(passes_d)] <- FALSE
  if (!identical(as.logical(path$passes), passes_d)) bad(cs, " ", mid, ": saved passes differ from derived passes")
  if (!identical(path$k, lengths(lapply(path$key, parse_key)))) bad(cs, " ", mid, ": path k differs from key")
  # Candidate table re-derived (§III.3.0 EBIC/BIC): sizes from keys, validity from rank and RSS, the set
  # equal to the null support plus the distinct path supports with k <= kmax, no duplicates. RSS values
  # themselves are taken as saved (their recomputation needs X; G5 does it).
  cand <- o$diagnostics$candidates
  k_d <- lengths(lapply(cand$key, parse_key))
  valid_d <- cand$rank == k_d & is.finite(cand$rss) & cand$rss > 0
  expect_keys <- unique(c("", path$key[path$k <= CONFIG$COMMON$kmax_ebic]))
  if (!identical(cand$k, k_d) || !identical(cand$valid, valid_d) || anyDuplicated(cand$key) > 0L ||
      !setequal(cand$key, expect_keys) || length(cand$key) != length(expect_keys))
    bad(cs, " ", mid, ": candidate table inconsistent (size, validity, cap, dedup or membership)")
  for (j in seq_len(nrow(r))) {                                # independent recomputation of the EBIC pick
    g <- CONFIG$COMMON$ebic_gamma[[r$rule_id[j]]]
    crit <- ifelse(valid_d, 200 * log(cand$rss / 200) + k_d * log(200) + 2 * g * lchoose(r$p[j], k_d), Inf)
    best <- order(crit, k_d, cand$key, method = "radix")[1]
    chosen <- if (okr[j]) r$support[j] else r$support_audit[j]
    if (!identical(cand$key[best], chosen)) bad(cs, " ", mid, ": EBIC pick differs for ", r$rule_id[j])
    if (abs(crit[best] - r$crit_value[j]) > 1e-8 * max(1, abs(crit[best]))) bad(cs, " ", mid, ": crit_value")
    lc <- grepl("ebic_at_largest", r$diag_codes[j])
    if (lc != (k_d[best] == max(k_d[valid_d]))) bad(cs, " ", mid, ": ebic_at_largest code")
    if (!gate) {                                               # rule failure <=> no passing occurrence
      should_fail <- nzchar(chosen) && !any(path$key == chosen & passes_d)
      if (should_fail != !okr[j]) bad(cs, " ", mid, ": rule failure inconsistent with path for ", r$rule_id[j])
    }
  }
  if (okr[1]) {
    nz <- which(o$beta != 0)
    if (anyNA(o$beta) || !identical(support_key(nz), r$support[1])) bad(cs, " ", mid, ": beta support != ebic1 support")
  } else if (any(!is.na(o$beta))) bad(cs, " ", mid, ": beta not NA although ebic1 failed")
}

for (cs in cases) for (mid in METHODS$method_id) {
  nchecked <- nchecked + 1L
  e <- tryCatch({ check_pair(cs, mid); NULL }, error = function(e) conditionMessage(e))
  if (!is.null(e)) bad(cs, " ", mid, ": unreadable or malformed output (", e, ")")
}
txt <- c(sprintf("checked %d (case, method) pairs; missing %d; problems %d", nchecked, length(missing), length(problems)),
         if (length(problems)) problems else "no problems found")
writeLines(txt, out_file); cat(txt, sep = "\n")
writeLines(c("case,method_id", missing), paste0(out_file, ".missing.csv"))
quit(save = "no", status = if (length(problems)) 1L else 0L)
