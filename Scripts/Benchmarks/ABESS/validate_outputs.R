#!/usr/bin/env Rscript
# validate_outputs.R: checks the §IV.1.1 files of every (case, method) under a results tree
# against the §IV.1.2 rule-row schema and the §III.3.0 status/flag/convergence semantics.
# Infrastructure (reads outputs and the inputs manifest only; never truth/). Requires the
# functions of run_case.R (load_settings, sidecar_errors) in the calling environment.
# Usage: Rscript --vanilla validate_outputs.R <code_root> <results_dir> <manifest_csv> [expected_cases]

SCHEMA_COLS <- c("study", "run_id", "source_sha256", "regime", "p", "scenario", "replicate",
  "scale_key", "scale", "dataset_id", "case_id", "data_seed", "fold_seed", "method_seed",
  "inputs_sha256", "x_sha256", "y_sha256", "fold_sha256", "method_id", "method_label", "package",
  "package_version", "rule_id", "role", "status", "converged", "diag_flag", "diag_codes",
  "n_warnings", "warnings", "messages", "error", "k", "support", "support_audit",
  "tp", "fp", "fn", "exact", "error_type", sprintf("sel_a%02d", 1:14), sprintf("pip_a%02d", 1:14),
  "max_pip_null", "runtime_s", "host", "slurm_job_id", "slurm_array_task_id", "started_utc",
  "finished_utc")
DIAG_VOCAB <- c("kkt_path", "path_truncated", "L_saturated", "elbo_drop", "sigma2_floor",
  "capped_intermediate", "tail_unstable", "fixed_point", "ess_tau", "ess_ci95", "crn_mismatch",
  "lambda_first", "lambda_last", "alpha_edge", "kappa_edge", "floored_selected", "ebic_at_largest")
FLAG_CODES <- list(F5 = character())          # §III.3.0: F5 has no flag-setting checks

read_rule_csv <- function(path)
  utils::read.csv(path, stringsAsFactors = FALSE, na.strings = "NA",
                  colClasses = c(support = "character", support_audit = "character",
                                 diag_codes = "character", warnings = "character",
                                 messages = "character", error = "character",
                                 slurm_job_id = "character", slurm_array_task_id = "character",
                                 source_sha256 = "character", inputs_sha256 = "character",
                                 x_sha256 = "character", y_sha256 = "character",
                                 fold_sha256 = "character"))

# File-level checks (presence, strict .sha256 sidecar), then the object-level checks.
validate_one <- function(prefix, settings, manifest, inputs_root = NULL, trusted = NULL) {
  errs <- character()
  for (ext in c(".rds", ".csv", ".sha256", ".done"))
    if (!file.exists(paste0(prefix, ext))) errs <- c(errs, paste0("missing ", basename(prefix), ext))
  if (length(errs)) return(errs)
  errs <- c(errs, sidecar_errors(prefix))                     # run_case.R
  r <- read_rule_csv(paste0(prefix, ".csv")); o <- readRDS(paste0(prefix, ".rds"))
  if (!identical(r$case_id[1], basename(dirname(prefix)))) errs <- c(errs, "case directory differs from row case_id")
  c(errs, validate_objects(r, o, basename(prefix), settings, manifest,
                           load_case_inputs(inputs_root, r, manifest), trusted))
}

# Object-level checks on the rule rows `r` (as read from the CSV) and the RDS object `o`.
# Kept separate so that the deliberate-corruption tests can corrupt objects in memory
# (Oct-14 validate.R pattern; Sol finding 1).
# Reads the case's X and y from inputs/ (never truth/) and checks them against the
# manifest hashes, so that the saved path can be recomputed (Sol round 2). NULL when no
# inputs root is given.
load_case_inputs <- function(inputs_root, r, manifest) {
  if (is.null(inputs_root)) return(NULL)
  f <- file.path(inputs_root, sprintf("p%04d", r$p[1]), paste0(r$dataset_id[1], ".rds"))
  d <- readRDS(f); y <- unname(d$Y[, r$scale_key[1]])
  mr <- manifest[manifest$dataset_id == r$dataset_id[1], , drop = FALSE]
  if (nrow(mr) != 1L || !identical(f64_sha256(d$X), mr$x_sha256) ||
      !identical(f64_sha256(y), mr[[paste0("y_", r$scale_key[1], "_sha256")]]))
    stop("inputs for ", r$case_id[1], " do not match the manifest")
  list(X = d$X, y = y)
}

# `trusted`: list(tree, settings) of the code that should have produced the output (the run
# snapshot), so that a stale but internally consistent result is rejected (Astra prod 6).
validate_objects <- function(r, o, mid, settings, manifest, inputs = NULL, trusted = NULL) {
  errs <- character(); add <- function(...) errs <<- c(errs, paste0(...))
  m <- settings$METHODS[settings$METHODS$method_id == mid, , drop = FALSE]
  if (nrow(m) != 1L) return(c(errs, paste("unregistered method", mid)))
  extras <- m$extra_cols[[1L]]
  if (!identical(names(r), c(SCHEMA_COLS, extras))) add("columns differ from schema + extras")
  if (!identical(r$rule_id, m$rule_ids[[1L]])) return(c(errs, "rule ids differ from registry"))
  if (!identical(r$role, m$roles[[1L]])) add("roles differ from registry")
  if (!all(r$method_id == mid) || !all(r$method_label == m$method_label) ||
      !all(r$package == m$package) || !all(r$package_version == m$pkg_version)) add("method columns")
  if (!all(r$status %in% c("ok", "warning", "failed"))) add("status outside ok/warning/failed")
  if (length(unique(r$runtime_s)) != 1L || any(!is.finite(r$runtime_s)) || any(r$runtime_s < 0)) add("runtime_s")
  if (isTRUE(m$converged_na) && !all(is.na(r$converged))) add("converged must be NA for ", mid)
  if (!is.logical(r$diag_flag) && !all(is.na(r$diag_flag))) add("diag_flag not logical")
  if (length(unique(r$diag_flag)) > 1L) add("diag_flag not method-wide")
  codes <- unlist(strsplit(ifelse(is.na(r$diag_codes), "", r$diag_codes), ";", fixed = TRUE))
  if (!all(codes %in% DIAG_VOCAB)) add("diag_codes outside the closed vocabulary")
  fired <- intersect(codes, FLAG_CODES[[mid]])
  if (any(r$diag_flag %in% TRUE) != (length(fired) > 0)) add("diag_flag inconsistent with flag codes")
  if (!all(r$n_warnings == ifelse(is.na(r$warnings), 0L, lengths(strsplit(r$warnings, " | ", fixed = TRUE)))))
    add("n_warnings inconsistent")
  w <- !is.na(r$warnings) | !is.na(r$messages)
  if (any(r$status == "ok" & w)) add("status ok with captured conditions")
  if (any(r$status == "warning" & !w)) add("status warning without captured conditions")
  p <- r$p[1]
  for (i in seq_len(nrow(r))) {
    if (r$status[i] == "failed") {
      if (!is.na(r$support[i]) || !is.na(r$k[i])) add("failed row ", r$rule_id[i], " has support or k")
      if (is.na(r$error[i])) add("failed row without error text")
    } else {
      if (is.na(r$support[i]) || is.na(r$k[i])) { add("successful row without support"); next }
      s <- if (nzchar(r$support[i])) as.integer(strsplit(r$support[i], ";", fixed = TRUE)[[1L]]) else integer()
      if (length(s) != r$k[i] || is.unsorted(s, strictly = TRUE) || any(s < 1L | s > p))
        add("support/k malformed for ", r$rule_id[i])
      if (!is.na(r$support_audit[i])) add("support_audit set on a successful row")
    }
  }
  if (!all(is.na(r[c("tp", "fp", "fn", "exact", "error_type")]))) add("truth columns filled at fit time")
  if (!all(is.na(r[c(sprintf("sel_a%02d", 1:14), sprintf("pip_a%02d", 1:14), "max_pip_null")]))) add("per-active columns filled at fit time")
  mr <- manifest[manifest$dataset_id == r$dataset_id[1], , drop = FALSE]
  if (nrow(mr) != 1L || r$x_sha256[1] != mr$x_sha256 || r$fold_sha256[1] != mr$foldid_sha256 ||
      r$y_sha256[1] != mr[[paste0("y_", r$scale_key[1], "_sha256")]] ||
      r$inputs_sha256[1] != mr$file_sha256) add("input hashes differ from manifest")
  if (r$case_id[1] != paste0(r$dataset_id[1], "_", r$scale_key[1]) ||
      !grepl("^(dev_)?p[0-9]{4}_S[1-6]_r[0-9]{3}$", r$dataset_id[1])) add("id format")
  if (length(o$beta) != p) add("beta length != p")
  ok_fit <- all(r$status != "failed")
  if (ok_fit && any(!is.finite(o$beta))) add("non-finite beta on a successful fit")
  if (!ok_fit && !all(is.na(o$beta))) add("failed fit must have NA beta")
  if (!is.null(o$pip)) add("pip must be NULL for ", mid)
  for (col in c("rule_id", "status", "support", "support_audit", "diag_codes"))
    if (!identical(as.character(o$rows[[col]]), as.character(r[[col]]))) add("RDS rows differ from CSV in ", col)
  if (!identical(as.integer(o$rows$k), as.integer(r$k))) add("RDS rows differ from CSV in k")
  # Provenance: the row hash is the tree hash of the per-file code hashes saved in the RDS.
  sh <- o$source_hashes
  tree <- digest::digest(paste(sh$files$path, sh$files$sha256, sep = "  ", collapse = "\n"),
                         algo = "sha256", serialize = FALSE)
  if (!identical(tree, sh$tree) || !all(r$source_sha256 == sh$tree)) add("source hashes inconsistent")
  for (h in c("x_sha256", "y_sha256", "fold_sha256", "inputs_sha256"))
    if (!identical(o$case[[h]], r[[h]][1])) add("RDS case ", h, " differs from rows")
  if (length(unique(r$case_id)) != 1L || !all(r$scale_key == "c100")) add("rows not a single c100 case")
  idcols <- c("study", "run_id", "source_sha256", "regime", "p", "scenario", "replicate", "scale_key", "scale",
              "dataset_id", "case_id", "data_seed", "fold_seed", "method_seed", "inputs_sha256", "x_sha256",
              "y_sha256", "fold_sha256", "method_id", "runtime_s")
  if (!all(vapply(idcols, function(cc) length(unique(r[[cc]])) == 1L && !anyNA(r[[cc]]), TRUE)))
    add("design/provenance columns not constant and complete across rows")
  if (!identical(r$case_id[1], paste0(r$dataset_id[1], "_", r$scale_key[1])) ||
      !identical(r$dataset_id[1], sprintf("%sp%04d_S%d_r%03d", if (startsWith(r$dataset_id[1], "dev_")) "dev_" else "",
                                          as.integer(r$p[1]), as.integer(r$scenario[1]), as.integer(r$replicate[1]))))
    add("dataset_id/case_id disagree with p, scenario, replicate")
  if (nrow(mr) == 1L && (r$p[1] != as.numeric(mr$p) || r$scenario[1] != as.numeric(mr$scenario) ||
      r$replicate[1] != as.numeric(mr$replicate))) add("design columns differ from manifest")
  if (!is.null(trusted$run_id) && !all(r$run_id == trusted$run_id)) add("run_id differs from the results directory")
  if (nrow(mr) == 1L && (!all(r$data_seed == as.numeric(mr$data_seed)) || !all(r$fold_seed == as.numeric(mr$fold_seed)) ||
      !all(r$method_seed == as.numeric(mr$method_seed)) ||
      !all(r$method_seed == r$data_seed + settings$METHOD_SEED_OFFSET))) add("seeds differ from manifest or offset rule")
  if (!is.null(trusted)) {
    if (!all(r$source_sha256 == trusted$tree)) add("source_sha256 differs from the trusted snapshot")
    if (!identical(o$settings, trusted$settings)) add("saved settings differ from the trusted snapshot")
  }
  if (ok_fit && mid == "F5") errs <- c(errs, validate_F5_diagnostics(r, o, inputs))
  errs
}

# Independent re-check of the saved F5 diagnostics (§III.3.5 e step 3, f, g): the path, the
# coefficients, the RSS identities, stationarity, the candidate scores and the rule choices.
validate_F5_diagnostics <- function(r, o, inputs = NULL) {
  errs <- character(); add <- function(...) errs <<- c(errs, paste0(...))
  F5 <- o$settings$F5; C <- o$settings$COMMON; d <- o$diagnostics; pa <- d$path
  n <- C$n; p <- r$p[1]; S <- as.integer(F5$sizes)
  if (is.null(pa) || nrow(pa) != length(S)) return("diagnostics path missing or wrong length")
  # Every mandatory column must be present, of full length and finite before any identity is
  # checked, so that a missing column cannot pass through a zero-length comparison.
  need <- c("size", "key", "k", "dev", "rss_reconstructed", "rss_ols", "rss_centred", "stationarity", "intercept")
  miss <- setdiff(need, names(pa))
  if (length(miss)) return(paste("diagnostics path lacks column(s):", paste(miss, collapse = ", ")))
  num <- setdiff(need, "key")
  if (!all(vapply(pa[num], function(v) length(v) == length(S) && all(is.finite(v)), TRUE)))
    return("diagnostics path has non-finite or short columns")
  for (sc in c("response_center", "zmax", "stat_tol"))
    if (length(d[[sc]]) != 1L || !is.finite(d[[sc]])) return(paste("diagnostics scalar missing:", sc))
  cneed <- c("key", "k", "rank", "rss", "valid", names(C$ebic_gamma))
  if (!is.data.frame(d$candidates) || length(setdiff(cneed, names(d$candidates))))
    return("candidate table missing or lacks columns")
  if (!identical(as.integer(pa$size), S) || !identical(as.integer(pa$k), S)) add("path sizes or k differ from requested sizes")
  keys <- lapply(pa$key, function(k) if (nzchar(k)) as.integer(strsplit(k, ";", fixed = TRUE)[[1L]]) else integer())
  if (!identical(lengths(keys), S)) add("path key lengths differ from sizes")
  cf <- d$coefficients
  if (length(cf) != length(S) || !identical(lengths(cf), S) ||
      any(!is.finite(unlist(cf))) || any(unlist(cf) == 0)) add("saved coefficients inconsistent with path sizes")
  close <- function(a, b) all(is.finite(a) & is.finite(b) & abs(a - b) <= F5$rss_rel_tol * pmax(1, abs(a), abs(b)))
  if (!close(pa$rss_reconstructed, pa$rss_ols)) add("saved reconstructed RSS != OLS RSS")
  if (!close(pa$rss_reconstructed, 2 * n * pa$dev + n * d$response_center^2)) add("saved RSS != 2n dev + n ybar^2")
  if (!close(pa$rss_reconstructed, pa$rss_centred + n * d$response_center^2)) add("saved RSS != centred RSS + n ybar^2")
  if (any(!is.finite(pa$stationarity)) || any(pa$stationarity > d$stat_tol) ||
      !isTRUE(all.equal(d$stat_tol, F5$stat_rel_tol * max(1, d$zmax)))) add("saved stationarity above tolerance")
  if (any(abs(pa$intercept) > F5$intercept_tol)) add("saved intercept not zero")
  cand <- d$candidates
  want_keys <- unique(c("", pa$key[pa$k <= C$kmax_ebic]))
  if (!setequal(cand$key, want_keys) || anyDuplicated(cand$key)) add("candidate keys differ from the path supports")
  cand_rss <- pa$rss_ols[match(cand$key, pa$key)]
  if (!close(cand$rss, cand_rss)) add("candidate RSS differs from the path OLS RSS")
  ck <- vapply(cand$key, function(k) if (nzchar(k)) length(strsplit(k, ";", fixed = TRUE)[[1L]]) else 0L, 0L)
  if (!identical(unname(ck), as.integer(cand$k))) add("candidate k differs from its key")
  if (any(cand$rank > cand$k) || any(cand$rank < 0) ||
      !identical(as.logical(cand$valid), cand$rank == cand$k & is.finite(cand$rss) & cand$rss > 0))
    add("candidate validity inconsistent with rank and RSS")
  for (id in names(C$ebic_gamma)) {
    sc <- ifelse(cand$valid, n * log(cand$rss / n) + cand$k * log(n) + 2 * C$ebic_gamma[[id]] * lchoose(p, cand$k), Inf)
    if (!isTRUE(all.equal(sc, cand[[id]], tolerance = 1e-12))) add("candidate ", id, " scores do not recompute")
    i <- order(cand[[id]], cand$k, cand$key, method = "radix")[1L]
    row <- r[r$rule_id == id, , drop = FALSE]
    kv <- max(cand$k[cand$valid])
    if (!identical(row$support, cand$key[i]) || !identical(as.integer(row$k), as.integer(cand$k[i])) ||
        !isTRUE(all.equal(row$crit_value, cand[[id]][i])) || !isTRUE(all.equal(row$rss, cand$rss[i])) ||
        row$k_valid_max != kv || row$k_path_max != max(pa$k))
      add("rule ", id, " does not match the re-picked candidate")
    has_code <- "ebic_at_largest" %in% strsplit(row$diag_codes, ";", fixed = TRUE)[[1L]]
    if (has_code != (cand$k[i] == kv)) add("rule ", id, " ebic_at_largest code wrong")
  }
  j1 <- match(r$support[r$rule_id == "ebic1"], pa$key)
  b1 <- which(o$beta != 0)
  if (is.na(j1) || !identical(paste(b1, collapse = ";"), pa$key[j1]) ||
      !isTRUE(all.equal(unname(o$beta[b1]), unname(cf[[j1]])))) add("beta differs from the ebic1 path coefficients")
  # Independent recomputation of every path point from the verified inputs: residual RSS,
  # OLS RSS and rank, stationarity, and the candidate ranks (Sol round 2).
  if (!is.null(inputs) && !length(errs)) {
    X <- inputs$X; y <- inputs$y; tol <- C$ols_tol
    rec <- t(vapply(seq_along(S), function(j) {
      s <- keys[[j]]
      if (!length(s)) return(c(sum(y^2), sum(y^2), 0, 0))
      res <- y - drop(X[, s, drop = FALSE] %*% cf[[j]])
      z <- lm.fit(X[, s, drop = FALSE], y, tol = tol)
      c(sum(res^2), sum(z$residuals^2), z$rank, max(abs(crossprod(X[, s, drop = FALSE], res))) / n)
    }, numeric(4)))
    if (!close(rec[, 1], pa$rss_reconstructed)) add("recomputed path RSS differs from saved (coefficients changed?)")
    if (!close(rec[, 2], pa$rss_ols)) add("recomputed OLS RSS differs from saved")
    if (any(abs(rec[, 4] - pa$stationarity) > d$stat_tol)) add("recomputed stationarity differs from saved")
    if (!isTRUE(all.equal(d$zmax, max(abs(crossprod(X, y))) / n))) add("recomputed zmax differs from saved")
    if (!isTRUE(all.equal(d$response_center, mean(y)))) add("recomputed response centre differs from saved")
    errs <- c(errs, rank_errors(as.integer(rec[match(cand$key, pa$key), 3]), cand))
  }
  errs
}

# Rank-deficient supports are allowed on the path; they must be recorded with their true rank
# and be excluded from selection (invalid, criterion Inf), as the EBIC scorer of §III.3.0 does
# (Astra prod finding 2). `crank` = ranks recomputed from the inputs, in candidate order.
rank_errors <- function(crank, cand) {
  errs <- character()
  if (!identical(as.integer(crank), as.integer(cand$rank))) errs <- c(errs, "recomputed candidate ranks differ from saved")
  deficient <- crank < cand$k
  if (any(cand$valid[deficient])) errs <- c(errs, "rank-deficient candidate marked valid")
  crit <- intersect(names(cand), c("ebic1", "ebic05", "bic"))
  if (any(is.finite(unlist(cand[deficient, crit])))) errs <- c(errs, "rank-deficient candidate has a finite criterion")
  errs
}

# Expected production population: 1,200 (case_id) values (S1-S6 x r001-r100 x p, c100).
prod_case_ids <- function()
  as.vector(outer(sprintf("S%d_r%03d", rep(1:6, each = 100), rep(1:100, 6)), c("p0500", "p1000"),
                  function(sr, pp) paste0(pp, "_", sr, "_c100")))

# manifest: one inputs-manifest CSV, or a directory of them (production: the 12 frozen cell
# manifests). inputs_root is required: without it the path recomputation cannot run and the
# validation fails (Astra prod finding 1). expected_cases: the exact population; missing,
# extra and duplicate cases fail (Astra prod finding 6). code_root is the trusted snapshot.
validate_tree <- function(code_root, results_dir, manifest, expected_cases = NULL, inputs_root) {
  settings <- load_settings(code_root)                        # run_case.R
  trusted <- list(tree = code_hashes(code_root)$tree, settings = settings, run_id = basename(normalizePath(results_dir)))
  csvs <- if (dir.exists(manifest)) list.files(manifest, pattern = "_inputs?_manifest\\.csv$|_inputs\\.csv$", full.names = TRUE) else manifest
  man <- do.call(rbind, lapply(csvs, utils::read.csv, stringsAsFactors = FALSE, colClasses = "character"))
  if (missing(inputs_root) || is.null(inputs_root) || !dir.exists(inputs_root))
    return(list(table = NULL, missing = character(), extra = character(), inputs_root = NULL,
                passed = FALSE, note = "inputs root unavailable: path recomputation impossible"))
  dirs <- list.dirs(results_dir, recursive = TRUE)
  prefixes <- unlist(lapply(dirs, function(dd) {
    f <- list.files(dd, pattern = "\\.csv$", full.names = TRUE); sub("\\.csv$", "", f) }))
  found <- basename(dirname(prefixes))
  other <- prefixes[!basename(prefixes) %in% settings$METHODS$method_id]
  # Orphans: any file that is not one of the four files of a registered method in a case
  # directory p{pppp}/<case_id>/ (Astra prod follow-up, point 6).
  allf <- list.files(results_dir, recursive = TRUE, all.files = TRUE, no.. = TRUE)
  okf <- grepl(paste0("^p[0-9]{4}/[^/]+/(", paste(settings$METHODS$method_id, collapse = "|"),
                      ")\\.(rds|csv|sha256|done)$"), allf)
  orphans <- allf[!okf]
  out <- lapply(prefixes, function(px) {
    e <- tryCatch(validate_one(px, settings, man, inputs_root, trusted),  # a malformed object is an error entry
                  error = function(err) paste("validator error:", conditionMessage(err)))
    data.frame(case_id = basename(dirname(px)), method_id = basename(px), n_errors = length(e),
               errors = paste(e, collapse = " | "), stringsAsFactors = FALSE) })
  tab <- do.call(rbind, out)
  missing <- setdiff(expected_cases, found)
  extra <- c(if (!is.null(expected_cases)) setdiff(found, expected_cases), found[duplicated(found)],
             if (length(other)) paste("unregistered method file", other),
             if (length(orphans)) paste("orphan file", orphans))
  list(table = tab, missing = missing, extra = extra, inputs_root = inputs_root, n_found = length(found),
       passed = !is.null(tab) && all(tab$n_errors == 0L) && !length(missing) && !length(extra))
}

if (sys.nframe() == 0L) {
  a <- commandArgs(trailingOnly = TRUE)
  source(file.path(a[1], "run_case.R"))                     # loaders, sidecar_errors
  .libPaths(c(load_settings(a[1])$STUDY_LIB, .Library))
  # args: code_root results_dir manifest(file|dir) expected(comma list | "prod" | "-") inputs_root
  if (length(a) != 5L) stop("usage: validate_outputs.R <code_root> <results_dir> <manifest> <expected|prod|-> <inputs_root>")
  exp_cases <- if (a[4] == "prod") prod_case_ids() else if (a[4] == "-") NULL else strsplit(a[4], ",")[[1L]]
  v <- validate_tree(a[1], a[2], a[3], exp_cases, a[5])
  if (!is.null(v$note)) cat(v$note, "\n")
  if (!is.null(v$table)) print(v$table[v$table$n_errors > 0 | seq_len(nrow(v$table)) <= 12, ], right = FALSE)
  cat("cases found:", if (is.null(v$n_found)) 0 else v$n_found, "; with errors:",
      if (is.null(v$table)) NA else sum(v$table$n_errors > 0), "; path recomputed from", v$inputs_root, "\n")
  if (length(v$missing)) cat("MISSING (", length(v$missing), "):", head(v$missing, 50), "\n")
  if (length(v$extra)) cat("EXTRA/DUPLICATE (", length(v$extra), "):", head(v$extra, 50), "\n")
  cat("VALIDATION", if (v$passed) "PASSED" else "FAILED", "\n")
  quit(save = "no", status = if (v$passed) 0L else 1L)
}
