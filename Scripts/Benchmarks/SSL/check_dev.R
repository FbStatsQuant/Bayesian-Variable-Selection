# check_dev.R -- validates the A2 dev-test outputs (brief step 4): every expected file exists,
# hashes verify, the CSV matches the §IV.1.2 schema, rule ids and roles are as registered, and
# status / diag_flag / diag_codes / converged follow §III.3.0 and §III.3.7 h. The failure gates,
# the flags and convergence are re-derived here from the saved per-point table, beta-hat, theta_L,
# sigma_L and audit (RDS) and the config constants, not taken from the wrapper's own verdicts.
# Every (case, method) row has the same set of checks; a check that cannot be evaluated counts
# as failed, except the numerical checks of a fit that returned no native path (native-call
# error or runner-level error), which are NA (not applicable); such a fit must instead satisfy
# the §III.3.0 failure contract (fit_object_contract). The script exits with status 1 if any
# applicable check fails.
# Provenance: every row must carry this run's id (the results folder name) and, when given, the
# expected source tree hash; the CSV must agree with the rows saved in the RDS. An error while
# reading one output is recorded on its row (check_error) and the inventory continues. With
# --expected_datasets N the manifest must list N distinct datasets and every (dataset, method)
# must be present exactly once; all outputs must share one source_sha256.
# Reads only the results tree, the inputs manifest(s) and the code (config.R, common.R).
# Usage: Rscript check_dev.R --code <code dir> --results <results/<run_id>> --manifest <csv or dir> --out <dir>
#          [--source_sha256 <tree hash>] [--expected_datasets <N>] [--scale c100|c050] [--datasets id1,id2,...]
# (c = 0.5 copy: --scale selects the scale key of the outputs checked, default c100; --datasets restricts
# the check to the listed dataset ids of the manifest, e.g. for a pilot or reproduction run.)

CHECKS <- c("files", "sha256", "schema", "registry", "ids_hashes", "scoring_cols_na", "status_vocab",
            "status_semantics", "failed_rows", "support_k", "codes_vocab", "flag_iff_codes",
            "n_points", "failure_gates_rederived", "converged_rederived", "codes_rederived",
            "audit_tol_rederived", "support_from_beta", "fit_object_contract", "settings_match_config",
            "provenance", "csv_matches_rds", "audit_required_ran")
PATH_CHECKS <- c("n_points", "failure_gates_rederived", "converged_rederived", "codes_rederived",
                 "audit_tol_rederived", "support_from_beta", "settings_match_config", "audit_required_ran")

# CSV rows against the rows saved in the RDS: every schema column, compared as written by
# write.csv (15 significant digits), so only formatting-level differences are tolerated.
csv_matches_rds <- function(rows, saved, schema) {
  if (is.null(saved) || nrow(saved) != nrow(rows) || !identical(names(saved), schema)) return(FALSE)
  tmp <- tempfile(fileext = ".csv")
  on.exit(unlink(tmp))
  utils::write.csv(saved, tmp, row.names = FALSE, na = "NA")
  again <- utils::read.csv(tmp, stringsAsFactors = FALSE, colClasses = "character")
  now <- rows; now[] <- lapply(now, as.character)
  isTRUE(all.equal(again, now, check.attributes = FALSE))
}

# The exact production population (§II.6, D3): p in {500, 1000} x S1-S6 x replicates 1-100.
PROD_DATASETS <- as.vector(outer(sprintf("S%d", 1:6), sprintf("r%03d", 1:100), paste, sep = "_"))
PROD_DATASETS <- c(paste0("p0500_", PROD_DATASETS), paste0("p1000_", PROD_DATASETS))
SCALE_KEY <- "c100"                          # set from --scale in the command-line block
SCALE_VALUE <- c(c100 = 1, c050 = 0.5)       # signal scale factor of each supported scale key

check_one <- function(env, man, results_dir, ds, mid, source_sha256 = NULL) {
  M <- env$METHODS; A2 <- env$A2
  chk <- setNames(as.list(rep(FALSE, length(CHECKS))), CHECKS)
  info <- list(n_capped_intermediate = NA_integer_, fp_error = NA_real_, fp_tol = NA_real_, max_sweeps = NA_integer_,
               source_sha256 = NA_character_, check_error = NA_character_)
  p <- man$p[man$dataset_id == ds]
  case_id <- paste0(ds, "_", SCALE_KEY)
  base <- file.path(results_dir, sprintf("p%04d", p), case_id, mid)
  chk$files <- all(file.exists(paste0(base, c(".rds", ".csv", ".sha256", ".done"))))
  if (!chk$files) return(c(list(dataset = ds, method_id = mid), chk, info))
  sums <- readLines(paste0(base, ".sha256"))
  chk$sha256 <- identical(sums, sprintf("%s  %s", c(env$file_sha256(paste0(base, ".rds")), env$file_sha256(paste0(base, ".csv"))),
                                        paste0(mid, c(".rds", ".csv"))))
  chr <- c(support = "character", support_audit = "character", diag_codes = "character",
           warnings = "character", messages = "character", error = "character")
  rows <- utils::read.csv(paste0(base, ".csv"), stringsAsFactors = FALSE, colClasses = chr)
  rds <- readRDS(paste0(base, ".rds"))
  reg <- M[M$method_id == mid, ]
  chk$schema <- identical(names(rows), env$RULE_ROW_SCHEMA)
  chk$registry <- identical(rows$rule_id, unlist(reg$rule_ids)) && identical(rows$role, unlist(reg$roles)) &&
                  all(rows$method_id == mid, rows$package == reg$package, rows$package_version == reg$pkg_version,
                      rows$method_label == reg$method_label)
  mr <- man[man$dataset_id == ds, ]
  chk$ids_hashes <- all(rows$case_id == case_id, rows$dataset_id == ds, rows$scale_key == SCALE_KEY, rows$scale == SCALE_VALUE[[SCALE_KEY]],
                        rows$p == mr$p, rows$scenario == mr$scenario, rows$replicate == mr$replicate,
                        rows$fold_seed == mr$fold_seed,
                        rows$x_sha256 == mr$x_sha256, rows$y_sha256 == mr[[paste0("y_", SCALE_KEY, "_sha256")]],
                        rows$fold_sha256 == mr$foldid_sha256, rows$inputs_sha256 == mr$file_sha256,
                        rows$method_seed == mr$method_seed, rows$data_seed == mr$data_seed)
  chk$scoring_cols_na <- all(is.na(rows[, env$SCORING_COLUMNS]))
  chk$provenance <- all(rows$run_id == basename(normalizePath(results_dir))) &&
                    (is.null(source_sha256) || all(rows$source_sha256 == source_sha256))
  chk$csv_matches_rds <- csv_matches_rds(rows, rds$rows, env$RULE_ROW_SCHEMA)
  info$source_sha256 <- rows$source_sha256[1]
  st <- rows$status
  chk$status_vocab <- all(st %in% c("ok", "warning", "failed"))
  failed <- st == "failed"
  n_cond <- rows$n_warnings + ifelse(is.na(rows$messages), 0L, 1L)
  chk$status_semantics <- all(failed | ((st == "warning") == (n_cond > 0)))
  chk$failed_rows <- all(!failed | (is.na(rows$support) & is.na(rows$k) & rows$converged %in% FALSE & !is.na(rows$error)))
  keys <- lapply(rows$support, env$parse_key)
  chk$support_k <- all(failed | (vapply(keys, length, 1L) == rows$k &
                                  vapply(keys, function(s) !is.unsorted(s, strictly = TRUE), TRUE)))
  codes <- strsplit(ifelse(is.na(rows$diag_codes), "", rows$diag_codes), ";", fixed = TRUE)
  chk$codes_vocab <- all(unlist(codes) %in% c(env$FLAG_CODES, env$INFO_CODES))
  # diag_flag is NA only on a failed row whose checks could not run (native error; ASSUMPTIONS 8).
  no_checks <- failed & is.na(rows$diag_flag) & is.na(rows$diag_codes)
  chk$flag_iff_codes <- all(no_checks | (!is.na(rows$diag_flag) &
                                         rows$diag_flag == vapply(codes, function(cc) any(cc %in% env$FLAG_CODES), TRUE)))

  dg <- rds$fit$diagnostics
  fit <- rds$fit
  p_x <- man$p[man$dataset_id == ds]
  if (is.null(dg$path) || is.null(dg$beta_final)) {
    # No native path: the whole failure contract (§III.3.0 "Failures", "One capture layer").
    chk$fit_object_contract <- all(failed) && all(!is.na(rows$error)) && all(is.na(rows$support)) &&
      all(is.na(rows$k)) && all(is.na(rows$support_audit)) && all(rows$converged %in% FALSE) &&
      length(fit$beta) == p_x && all(is.na(fit$beta)) && is.null(fit$pip) && identical(fit$converged, FALSE)
    out <- c(list(dataset = ds, method_id = mid), lapply(chk, isTRUE), info)
    out[PATH_CHECKS] <- NA
    return(out)
  }
  {
    # The settings the fit used (echo) must equal config.R, including the lambda0 ladder
    # recomputed here; the derivations below use the echoed settings, so a deliberately
    # altered test fit is still checked for internal consistency.
    echo <- dg$settings_echo
    blk <- if (mid == "A2") A2 else env$A2RS
    lmax <- if (identical(blk$LAMBDA0_MAX, "n")) env$COMMON$n else p_x
    ladder <- seq(1, lmax, length.out = blk$NLAMBDA)
    chk$settings_match_config <- identical(echo$A2, A2) && (mid == "A2" || identical(echo$A2RS, env$A2RS)) &&
      identical(echo$lambda0, ladder) && identical(echo$lambda1, blk$LAMBDA1)
    A2 <- echo$A2
    tab <- dg$path; L <- nrow(tab)
    capped <- tab$iter >= A2$MAX_ITER                           # from native iterations and the echoed max_iter
    chk$n_points <- L == length(echo$lambda0) && identical(tab$lambda0, echo$lambda0)
    b <- dg$beta_final; th <- dg$theta_L; sg <- dg$sigma_L
    exp_failed <- any(!is.finite(b)) || capped[L] || !is.finite(th) || th <= 0 || th >= 1 || !is.finite(sg) || sg <= 0
    chk$failure_gates_rederived <- all(failed == exp_failed)
    chk$converged_rederived <- all(rows$converged == (!capped[L] && !exp_failed))
    tol <- A2$FP_TOL_MULT * A2$EPS * (1 + max(abs(b)))
    audit_run <- isTRUE(dg$audit$run)
    # The audit must have run, with finite statistics, whenever beta-hat, theta_L and sigma_L allow it.
    eligible <- all(is.finite(b)) && is.finite(th) && th > 0 && th < 1 && is.finite(sg) && sg > 0
    chk$audit_required_ran <- !eligible || (audit_run && is.finite(dg$audit$max_abs_fixed_point_error) &&
                                            is.finite(dg$audit$support_mismatch))
    chk$audit_tol_rederived <- !audit_run || isTRUE(all.equal(dg$audit$tolerance, tol, tolerance = 0))
    fp <- audit_run && (dg$audit$support_mismatch > 0 || dg$audit$max_abs_fixed_point_error > tol)
    tail_idx <- seq(max(1L, L - A2$STABLE_TAIL + 1L), L)
    exp_codes <- c(capped_intermediate = L > 1L && any(capped[-L]),
                   tail_unstable = length(unique(tab$support_key[tail_idx])) > 1L, fixed_point = fp)
    chk$codes_rederived <- all(rows$diag_codes == paste(names(exp_codes)[exp_codes], collapse = ";"))
    sel <- env$support_key(which(b != 0))
    chk$support_from_beta <- all(ifelse(failed, rows$support_audit == sel, rows$support == sel))
    # Returned object: failed fit -> beta NA, pip NULL, converged FALSE; else beta = beta-hat.
    chk$fit_object_contract <- is.null(fit$pip) && length(fit$beta) == p_x &&
      if (any(failed)) all(is.na(fit$beta)) && identical(fit$converged, FALSE) else
                       identical(fit$beta, b) && identical(fit$converged, !capped[L])
    info$n_capped_intermediate <- sum(capped[-L])
    info$fp_error <- if (audit_run) signif(dg$audit$max_abs_fixed_point_error, 3) else NA_real_
    info$fp_tol <- signif(tol, 3); info$max_sweeps <- max(tab$iter)
  }
  c(list(dataset = ds, method_id = mid), lapply(chk, isTRUE), info)
}

check_dev <- function(code_dir, results_dir, manifest, out_dir, source_sha256 = NULL, expected_datasets = NULL,
                      datasets = NULL) {
  env <- new.env()
  for (f in c("config.R", "common.R")) sys.source(file.path(code_dir, f), envir = env)
  # manifest: one CSV, or a directory of per-cell manifests *_inputs.csv (production).
  man <- if (dir.exists(manifest))
    do.call(rbind, lapply(sort(list.files(manifest, pattern = "_inputs[.]csv$", full.names = TRUE)),
                          utils::read.csv, stringsAsFactors = FALSE)) else utils::read.csv(manifest, stringsAsFactors = FALSE)
  if (!is.null(datasets)) {
    if (!all(datasets %in% man$dataset_id)) stop("--datasets: ids not in the manifest")
    man <- man[man$dataset_id %in% datasets, , drop = FALSE]
  }
  one <- function(ds, mid) {
    r <- tryCatch(check_one(env, man, results_dir, ds, mid, source_sha256), error = function(e) {
      out <- c(list(dataset = ds, method_id = mid), setNames(as.list(rep(FALSE, length(CHECKS))), CHECKS),
               list(n_capped_intermediate = NA_integer_, fp_error = NA_real_, fp_tol = NA_real_, max_sweeps = NA_integer_,
                    source_sha256 = NA_character_, check_error = conditionMessage(e)))
      out$files <- all(file.exists(file.path(results_dir, sprintf("p%04d", man$p[man$dataset_id == ds][1]),
                                             paste0(ds, "_", SCALE_KEY), paste0(mid, c(".rds", ".csv", ".sha256", ".done")))))
      out
    })
    as.data.frame(r, stringsAsFactors = FALSE)
  }
  res <- do.call(rbind, lapply(man$dataset_id, function(ds) do.call(rbind, lapply(env$METHODS$method_id, function(mid) one(ds, mid)))))
  res$all_pass <- vapply(seq_len(nrow(res)), function(i) {
    r <- unlist(res[i, CHECKS]); na_ok <- names(r) %in% PATH_CHECKS & is.na(r)
    all(r[!na_ok] %in% TRUE)
  }, TRUE)
  dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
  utils::write.csv(res, file.path(out_dir, "check_dev.csv"), row.names = FALSE)
  run_lines <- character()
  failing <- res[!res$all_pass, , drop = FALSE]
  if (nrow(failing)) print(utils::head(failing, 20), row.names = FALSE)
  cat(sprintf("expected (case, method) outputs: %d; all %d applicable checks pass: %d\n", nrow(res), length(CHECKS), sum(res$all_pass)))
  # Run-level checks: one source tree for all outputs; the expected population, each pair once.
  srcs <- unique(stats::na.omit(res$source_sha256))
  run_ok <- length(srcs) <= 1L
  run_lines <- c(run_lines, sprintf("source_sha256 values across outputs: %d (%s)", length(srcs), paste(srcs, collapse = ",")))
  if (!is.null(expected_datasets)) {
    pop_ok <- !anyDuplicated(man$dataset_id) && length(unique(man$dataset_id)) == expected_datasets &&
              nrow(res) == expected_datasets * nrow(env$METHODS) && !anyDuplicated(paste(res$dataset, res$method_id))
    if (expected_datasets == length(PROD_DATASETS)) pop_ok <- pop_ok && setequal(man$dataset_id, PROD_DATASETS)
    run_lines <- c(run_lines, sprintf("manifest datasets %d (expected %d%s), (dataset, method) rows %d: %s",
                                      length(unique(man$dataset_id)), expected_datasets,
                                      if (expected_datasets == length(PROD_DATASETS)) ", exact production set" else "",
                                      nrow(res), if (pop_ok) "OK" else "MISMATCH"))
    run_ok <- run_ok && pop_ok
  }
  run_lines <- c(run_lines, sprintf("outputs passing all applicable checks: %d of %d", sum(res$all_pass), nrow(res)),
                 sprintf("RUN-LEVEL VERDICT: %s", if (run_ok && all(res$all_pass)) "PASS" else "FAIL"))
  writeLines(run_lines, file.path(out_dir, "run_level.txt"))
  cat(run_lines, sep = "\n")
  attr(res, "run_ok") <- run_ok
  invisible(res)
}

if (sys.nframe() == 0L) {
  a <- commandArgs(trailingOnly = TRUE)
  get_arg <- function(k, optional = FALSE) {
    i <- match(paste0("--", k), a)
    if (is.na(i)) { if (optional) return(NA_character_); stop("missing --", k) }
    a[i + 1L]
  }
  .libPaths(c("/projects/ml75/fb31/BVS/bench20261019/lib/R452", .Library))
  src <- get_arg("source_sha256", TRUE); n_exp <- get_arg("expected_datasets", TRUE)
  sk <- get_arg("scale", TRUE); if (!is.na(sk)) SCALE_KEY <- sk
  if (!SCALE_KEY %in% names(SCALE_VALUE)) stop("--scale must be one of ", paste(names(SCALE_VALUE), collapse = ", "))
  ds_sel <- get_arg("datasets", TRUE)
  if (!is.na(n_exp) && is.na(src)) stop("--expected_datasets (production check) requires --source_sha256")
  res <- check_dev(get_arg("code"), get_arg("results"), get_arg("manifest"), get_arg("out"),
                   source_sha256 = if (is.na(src)) NULL else src,
                   expected_datasets = if (is.na(n_exp)) NULL else as.integer(n_exp),
                   datasets = if (is.na(ds_sel)) NULL else strsplit(ds_sel, ",")[[1]])
  quit(status = if (all(res$all_pass) && isTRUE(attr(res, "run_ok"))) 0L else 1L)
}
