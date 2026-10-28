#!/usr/bin/env Rscript
# Checks the dev-test outputs of A3 without reading truth: the four files of §IV.1.1 per case,
# their hashes, the §IV.1.2 column schema, registered rule ids and roles, the closed status and
# code vocabularies, the §III.3.0 semantics of status / diag_flag / diag_codes / converged, the
# input hashes against the manifest, and the A3 run conditions (n.cores 1, detectCores >= 2,
# Bhattacharya sampler at p/n >= 2).
# Usage: Rscript check_outputs.R --outroot <dir> --run-id <id> --manifest <inputs manifest.csv> [--scales c100] [--datasets id1,id2] [--checkdir dir]

CODE_DIR <- local({
  f <- grep("^--file=", commandArgs(FALSE), value = TRUE)
  if (length(f)) dirname(normalizePath(sub("^--file=", "", f[1]))) else getwd()
})

# Checks every (dataset in `man`) x scale case of one run; returns the per-rule table and the
# list of problems. Needs config.R, common.R and run_case.R (schema_columns) loaded.
check_run <- function(outroot, run_id, man, scales) {
  s <- make_settings("primary")
  reg <- registry_row(s, "A3")
  cols <- schema_columns(s, s$A3$EXTRA_COLS)
  out <- list(); problems <- character(0); missing <- character(0)
  bad <- function(case, msg) problems <<- c(problems, paste0(case, ": ", msg))
  for (i in seq_len(nrow(man))) for (sk in scales) {
    m <- man[i, ]
    case <- paste0(m$dataset_id, "_", sk)
    prefix <- file.path(outroot, "results", run_id, sprintf("p%04d", m$p), case, "A3")
    f <- paste0(prefix, c(".rds", ".csv", ".sha256", ".done"))
    if (!all(file.exists(f))) {
      bad(case, paste("missing", paste(basename(f[!file.exists(f)]), collapse = ",")))
      missing <- c(missing, m$dataset_id)
    } else tryCatch({        # an unreadable file is reported for this case and the inventory goes on
    sh <- strsplit(readLines(f[3]), "  ", fixed = TRUE)
    listed <- vapply(sh, function(x) if (length(x) == 2L) x[2] else NA_character_, "")
    if (length(listed) != 2L || !setequal(listed, c("A3.rds", "A3.csv"))) bad(case, "checksum list does not cover exactly A3.rds and A3.csv")
    for (x in sh) if (length(x) == 2L) if (!identical(file_sha256(file.path(dirname(prefix), x[2])), x[1])) bad(case, paste("hash mismatch", x[2]))
    r <- utils::read.csv(f[2], stringsAsFactors = FALSE, colClasses = c(support = "character", support_audit = "character"))
    rec <- readRDS(f[1])
    if (!identical(names(r), cols)) bad(case, "CSV columns differ from the schema")
    if (!identical(r$rule_id, reg$rule_ids[[1]]) || !identical(r$role, reg$roles[[1]])) bad(case, "rule ids or roles differ from the registry")
    if (!all(r$status %in% s$COMMON$STATUS_VALUES)) bad(case, "status outside vocabulary")
    codes <- unlist(strsplit(ifelse(is.na(r$diag_codes), "", r$diag_codes), ";"))
    if (!all(codes %in% c(s$COMMON$FLAG_CODES, s$COMMON$INFO_CODES))) bad(case, "diag code outside vocabulary")
    has_flag_code <- vapply(strsplit(ifelse(is.na(r$diag_codes), "", r$diag_codes), ";"),
                            function(z) any(z %in% s$COMMON$FLAG_CODES), TRUE)
    ok <- r$status != "failed"
    if (any(ok & (is.na(r$diag_flag) | r$diag_flag != has_flag_code))) bad(case, "diag_flag inconsistent with diag_codes")
    if (length(unique(r$diag_flag[ok])) > 1L) bad(case, "diag_flag not method-wide")
    if (!all(is.na(r$converged))) bad(case, "converged not NA (A3)")
    if (!all(is.na(r[, c("tp", "fp", "fn", "exact", "error_type")]))) bad(case, "truth columns filled at fit time")
    kk <- ifelse(is.na(r$support), NA_integer_, ifelse(r$support == "", 0L, lengths(strsplit(r$support, ";"))))
    if (!identical(as.integer(kk), as.integer(r$k))) bad(case, "k != |support|")
    if (any(r$status == "failed" & !is.na(r$support))) bad(case, "failed rule with a support")
    if (any(r$status == "warning" & r$n_warnings == 0)) bad(case, "status warning without a captured condition")
    if (any(r$status == "ok" & r$n_warnings > 0)) bad(case, "status ok with captured conditions")
    if (!identical(r$x_sha256[1], m$x_sha256) || !identical(r$y_sha256[1], m[[paste0("y_", sk, "_sha256")]]) ||
        !identical(r$fold_sha256[1], m$foldid_sha256) || !identical(r$inputs_sha256[1], m$file_sha256)) bad(case, "input hashes differ from manifest")
    if (!identical(as.integer(r$method_seed[1]), as.integer(m$method_seed))) bad(case, "method_seed differs from manifest")
    dg <- rec$diagnostics
    # Failed fits carry only part of the diagnostics; absent fields are reported as NA.
    val <- function(x) if (is.null(x) || length(x) != 1L) NA else x
    if (any(ok)) {
      if (!identical(as.numeric(dg$n_cores), 1)) bad(case, "n_cores != 1")
      if (!isTRUE(val(dg$detect_cores) >= 2)) bad(case, "detectCores < 2")
      if (!identical(dg$sampler, "bhattacharya")) bad(case, "sampler is not bhattacharya")
      if (!identical(dim(dg$coef), c(as.integer(m$p), 7L))) bad(case, "coef table is not p x 7")
      if (length(dg$trace_log_tau2) != s$A3$N_SAMPLES) bad(case, "trace length")
    }
    out[[length(out) + 1L]] <- data.frame(case_id = case, rule_id = r$rule_id, status = r$status, k = r$k,
      diag_flag = r$diag_flag, diag_codes = r$diag_codes, n_warnings = r$n_warnings,
      runtime_s = round(r$runtime_s, 1), diag_s = round(r$diag_s, 2),
      ess_log_tau2 = round(val(dg$ess_log_tau2), 1), ess_log_sigma2 = round(val(dg$ess_log_sigma2), 1),
      min_ess_ci95 = round(val(dg$min_ess_ci95), 1), min_ess_km2 = round(val(dg$min_ess_km2), 1),
      split_rhat_log_tau2 = round(val(dg$split_rhat_log_tau2), 3), split_rhat_log_sigma2 = round(val(dg$split_rhat_log_sigma2), 3),
      detect_cores = val(dg$detect_cores), host = r$host, rng_after = substr(r$rng_after, 1, 12),
      stringsAsFactors = FALSE)
    }, error = function(e) {
      bad(case, paste("unreadable or inconsistent files:", conditionMessage(e)))
      missing <<- c(missing, m$dataset_id)
    })
  }
  list(table = do.call(rbind, out), problems = problems, missing = unique(missing))
}

# Production task id (slurm/prod_A3.slurm, c = 0.5 copy: map "prod", 400 tasks x 3 datasets) of a
# dataset id p{pppp}_S{s}_r{rrr}.
prod_task_id <- function(dataset_id) {
  p <- as.integer(substr(dataset_id, 2, 5)); s <- as.integer(sub(".*_S([0-9]+)_.*", "\\1", dataset_id))
  r <- as.integer(sub(".*_r([0-9]+)$", "\\1", dataset_id))
  (if (p == 1000L) 200L else 0L) + (100L * (s - 1L) + r - 1L) %/% 3L + 1L
}

main <- function(args) {
  kv <- setNames(args[c(FALSE, TRUE)], sub("^--", "", args[c(TRUE, FALSE)]))
  scales <- if (is.na(kv["scales"])) "c100" else strsplit(kv[["scales"]], ",")[[1]]
  sys.source(file.path(CODE_DIR, "config.R"), envir = globalenv())
  .libPaths(c(COMMON$LIB, .Library))
  sys.source(file.path(CODE_DIR, "common.R"), envir = globalenv())
  sys.source(file.path(CODE_DIR, "run_case.R"), envir = globalenv())   # schema_columns()
  man <- utils::read.csv(kv[["manifest"]], stringsAsFactors = FALSE)
  if (!is.na(kv["datasets"])) man <- man[man$dataset_id %in% strsplit(kv[["datasets"]], ",")[[1]], , drop = FALSE]
  res <- check_run(kv[["outroot"]], kv[["run-id"]], man, scales)
  tab <- res$table; problems <- res$problems
  od <- if (!is.na(kv["checkdir"])) kv[["checkdir"]] else file.path(kv[["outroot"]], "checks", kv[["run-id"]])
  dir.create(od, recursive = TRUE, showWarnings = FALSE)
  if (length(res$missing)) {
    ids <- if (all(!startsWith(res$missing, "dev_"))) sort(unique(vapply(res$missing, prod_task_id, 0L))) else integer(0)
    writeLines(c(res$missing, if (length(ids)) paste("production task ids:", paste(ids, collapse = ","))),
               file.path(od, "missing_cases.txt"))
  }
  if (!is.null(tab)) utils::write.csv(tab, file.path(od, "check_table.csv"), row.names = FALSE)
  writeLines(if (length(problems)) problems else "no problems", file.path(od, "check_problems.txt"))
  print(tab, row.names = FALSE)
  cat(sprintf("\ncases expected %d, rule rows found %d, problems %d, missing or unreadable cases %d\n",
              nrow(man) * length(scales), if (is.null(tab)) 0L else nrow(tab), length(problems), length(res$missing)))
  if (length(problems)) cat(problems, sep = "\n")
  if (length(problems)) 1L else 0L
}

if (sys.nframe() == 0L) quit(save = "no", status = main(commandArgs(trailingOnly = TRUE)))
