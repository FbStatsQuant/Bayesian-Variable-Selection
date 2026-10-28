# One (dataset, scale) study adapter. No truth/holdout/fold use by the fit.
# Source this file without compiling or fitting; smcbvs_study_fit loads the core.
.smcbvs_adapter_dir <- local({
  frames <- rev(sys.frames())
  paths <- lapply(frames, function(fr) fr$ofile)
  paths <- Filter(Negate(is.null), paths)
  if (!length(paths)) stop("source adapter.R by its path")
  dirname(normalizePath(paths[[1L]], winslash = "/", mustWork = TRUE))
})
smcbvs_native_statuses <- c("exact", "completed", "schedule_limit", "numerical_failure",
  "resource_limit", "y_constant", "no_predictors", "invalid_input", "adapter_error")
smcbvs_utc <- function() format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC")
smcbvs_file_hash <- function(path) digest::digest(file = path, algo = "sha256")
# Exactly common.R / gen_dev_data.R: column-major, double, little-endian, no serialization.
smcbvs_f64_hash <- function(x) digest::digest(
  writeBin(as.double(as.vector(x)), raw(), endian = "little"), algo = "sha256", serialize = FALSE)
smcbvs_collapse <- function(x, sep = " | ") if (!length(x)) NA_character_ else paste(x, collapse = sep)
smcbvs_support_key <- function(x) if (is.null(x)) NA_character_ else paste(sort(as.integer(x)), collapse = ";")
smcbvs_atomic <- function(path, writer) {
  tmp <- paste0(path, ".tmp.", Sys.getpid())
  on.exit(unlink(tmp), add = TRUE)
  writer(tmp)
  if (!file.rename(tmp, path)) stop("atomic rename failed: ", path)
  invisible(path)
}
smcbvs_safe_path <- function(path, mustWork = TRUE) {
  if (length(path) != 1L || is.na(path) || !nzchar(path)) stop("path must be one nonempty string")
  if (grepl("(^|/)(truth|holdout)(/|$)", tolower(gsub("\\\\", "/", path))))
    stop("refusing truth/holdout path: ", path)
  path <- normalizePath(path, winslash = "/", mustWork = mustWork)
  # Inspect both lexical and canonical components (the latter resolves symlinks on NOTS).
  if (grepl("(^|/)(truth|holdout)(/|$)", tolower(gsub("\\\\", "/", path))))
    stop("refusing truth/holdout path: ", path)
  path
}
# Resolve the nearest existing parent before creating anything. This catches a symlink
# ancestor into truth/holdout/frozen STUDY even when the final output root does not exist.
smcbvs_resolve_future <- function(path) {
  lexical <- smcbvs_safe_path(path, mustWork = FALSE)
  parent <- lexical; suffix <- character()
  while (!dir.exists(parent)) {
    suffix <- c(basename(parent), suffix)
    next_parent <- dirname(parent)
    if (identical(next_parent, parent)) stop("output path has no existing directory parent")
    parent <- next_parent
  }
  if (any(suffix %in% c(".", ".."))) stop("nonexistent output suffix must not contain dot segments")
  resolved <- smcbvs_safe_path(parent)
  if (length(suffix)) resolved <- do.call(file.path, as.list(c(resolved, suffix)))
  smcbvs_safe_path(resolved, mustWork = FALSE)
}
smcbvs_output_root <- function(path, forbidden_root) {
  resolved <- smcbvs_resolve_future(path)
  forbidden_roots <- unique(c(forbidden_root, "/projects/ml75/fb31/BVS/bench20261019", "/home/fb31/projects/BVS/Benchmarks"))
  for (root in forbidden_roots) {
    forbidden <- smcbvs_safe_path(root, mustWork = FALSE)
    if (identical(resolved, forbidden) || startsWith(resolved, paste0(forbidden, "/")))
      stop("output must be outside the input/frozen study: ", resolved)
  }
  dir.create(resolved, recursive = TRUE, showWarnings = FALSE)
  smcbvs_safe_path(resolved)
}
smcbvs_contained <- function(path, root) {
  path <- smcbvs_safe_path(path); root <- smcbvs_safe_path(root)
  if (!startsWith(path, paste0(root, "/"))) stop("path escapes allowed root: ", path)
  path
}
smcbvs_scale_key <- function(scale) {
  if (is.numeric(scale) && length(scale) == 1L && is.finite(scale)) {
    if (scale == 1) return("c100")
    if (scale == 0.5) return("c050")
  }
  if (is.character(scale) && length(scale) == 1L && scale %in% c("c100", "c050")) return(scale)
  stop("scale must be c100/1 or c050/0.5")
}
smcbvs_case_spec <- function(case, scale, development = FALSE) {
  scale <- smcbvs_scale_key(scale)
  if (!is.character(case) || length(case) != 1L || is.na(case)) stop("case must be one dataset/case ID")
  pat <- "^(dev_)?p(0500|1000)_S([1-6])_r([0-9]{3})(_c100|_c050)?$"
  g <- regmatches(case, regexec(pat, case))[[1L]]
  if (!length(g)) stop("invalid dataset/case ID: ", case)
  dev <- identical(g[2L], "dev_")
  if (!identical(dev, isTRUE(development))) stop("development switch and dev_ prefix must agree")
  if (nzchar(g[6L]) && !identical(sub("^_", "", g[6L]), scale)) stop("case ID/scale mismatch")
  p <- as.integer(g[3L]); scenario <- as.integer(g[4L]); replicate <- as.integer(g[5L])
  if (!replicate %in% 1:100) stop("replicate outside 1..100")
  dataset_id <- sprintf("%sp%04d_S%d_r%03d", if (dev) "dev_" else "", p, scenario, replicate)
  data_base <- if (dev) c(`500` = 2410000L, `1000` = 2510000L) else c(`500` = 1410000L, `1000` = 1510000L)
  fold_base <- if (dev) c(`500` = 4410000L, `1000` = 4510000L) else c(`500` = 3410000L, `1000` = 3510000L)
  ds <- unname(data_base[[as.character(p)]] + 10000L * scenario + replicate)
  list(dataset_id = dataset_id, case_id = paste0(dataset_id, "_", scale), p = p,
    scenario = scenario, replicate = replicate, scale_key = scale,
    scale = if (scale == "c100") 1 else 0.5, development = dev,
    data_seed = ds, fold_seed = unname(fold_base[[as.character(p)]] + 10000L * scenario + replicate),
    method_seed = ds + 4000000L)
}
# Binding study mapping, RULINGS_LEAD.md R-1 (2026-10-22 19:25Z).
# This is provenance data, not a configurable method or mapping policy.
smcbvs_r1_policy <- function() {
  statuses <- setNames(rep("failed", length(smcbvs_native_statuses)), smcbvs_native_statuses)
  statuses[c("exact", "completed")] <- "ok"
  list(id = "R-1-20261022", adopted = TRUE,
    authority = "RULINGS_LEAD.md R-1 (2026-10-22 19:25Z)",
    mapping_status = "adopted", roles = c(hpm = "primary", pip05 = "S0"),
    status_map = statuses, converged_map = setNames(rep(NA, length(statuses)), names(statuses)),
    diag_true_flags = c("low_empirical_ESS", "grid_unconverged", "local_limit"),
    diag_false_flags = "checks_passed_final", flagged_status = "ok")
}
# Keep the policy argument for callers and archived policy files, but accept only R-1.
# Development uses the same mapping; it cannot silently exercise a production override.
smcbvs_validate_policy <- function(policy, development = FALSE) {
  if (!identical(policy, smcbvs_r1_policy())) stop("adapter policy is fixed by RULINGS_LEAD.md R-1; override refused")
  invisible(policy)
}
smcbvs_schema <- function() c("study", "run_id", "source_sha256", "regime", "p", "scenario", "replicate",
  "scale_key", "scale", "dataset_id", "case_id", "data_seed", "fold_seed", "method_seed",
  "inputs_sha256", "x_sha256", "y_sha256", "fold_sha256", "method_id", "method_label", "package", "package_version",
  "rule_id", "role", "status", "converged", "diag_flag", "diag_codes", "n_warnings", "warnings", "messages", "error",
  "k", "support", "support_audit", "tp", "fp", "fn", "exact", "error_type", sprintf("sel_a%02d", 1:14),
  sprintf("pip_a%02d", 1:14), "max_pip_null", "runtime_s", "host", "slurm_job_id", "slurm_array_task_id",
  "started_utc", "finished_utc", "v3_version", "v3_source_sha256", "v3_status", "v3_estimates_available",
  "v3_partial_results", "v3_p_retained", "v3_target_scale", "v3_flags_json", "allocation_sha256",
  "input_manifest_sha256", "adapter_mapping_status", "adapter_policy_id", "adapter_policy_sha256")
smcbvs_load_input <- function(spec, study, manifest = NULL) {
  study <- smcbvs_safe_path(study)
  input_root <- smcbvs_safe_path(file.path(study, "inputs"))
  input <- smcbvs_contained(file.path(input_root, sprintf("p%04d", spec$p), paste0(spec$dataset_id, ".rds")), input_root)
  manifest_root <- smcbvs_safe_path(file.path(study, "manifests"))
  if (is.null(manifest)) manifest <- file.path(manifest_root,
    if (spec$development) "dev_inputs_manifest.csv" else "inputs_manifest.csv")
  manifest <- smcbvs_contained(manifest, manifest_root)
  if (!grepl("inputs", basename(manifest), fixed = TRUE)) stop("only an inputs manifest is accepted")
  man <- utils::read.csv(manifest, stringsAsFactors = FALSE, colClasses = "character")
  m <- man[!is.na(man$dataset_id) & man$dataset_id == spec$dataset_id, , drop = FALSE]
  if (nrow(m) != 1L) stop("dataset must have one inputs-manifest row")
  # Check the on-disk container BEFORE deserializing it.
  file_hash <- smcbvs_file_hash(input)
  if (!identical(file_hash, m$file_sha256)) stop("input file hash differs from manifest")
  d <- readRDS(input)
  required <- c("X", "Y", "foldid", "dataset_id", "p", "n", "scenario", "replicate", "kind", "data_seed", "fold_seed", "method_seed", "scales")
  if (!is.list(d) || !all(required %in% names(d))) stop("input record missing benchmark fields")
  if (!identical(as.character(d$dataset_id), spec$dataset_id) ||
      !identical(as.character(d$kind), if (spec$development) "dev" else "prod")) stop("input identity/kind mismatch")
  for (nm in c("p", "scenario", "replicate", "data_seed", "fold_seed", "method_seed")) {
    expected <- as.character(spec[[nm]])
    if (!identical(as.character(d[[nm]]), expected) || !identical(m[[nm]], expected)) stop("input/manifest seed or design mismatch: ", nm)
  }
  if (!identical(as.integer(d$n), 200L) || !is.matrix(d$X) || !is.numeric(d$X) ||
      !identical(dim(d$X), c(200L, spec$p)) || !is.matrix(d$Y) || !is.numeric(d$Y) ||
      nrow(d$Y) != 200L || !spec$scale_key %in% colnames(d$Y) || length(d$foldid) != 200L)
    stop("input dimensions differ from n200 benchmark design")
  if (!identical(unname(as.numeric(d$scales[spec$scale_key])), spec$scale)) stop("input scale value mismatch")
  y <- unname(d$Y[, spec$scale_key])
  hashes <- list(inputs_sha256 = file_hash, x_sha256 = smcbvs_f64_hash(d$X),
    y_sha256 = smcbvs_f64_hash(y), fold_sha256 = smcbvs_f64_hash(d$foldid))
  for (pair in list(c("x_sha256", "x_sha256"), c("y_sha256", paste0("y_", spec$scale_key, "_sha256")),
                   c("fold_sha256", "foldid_sha256")))
    if (!identical(hashes[[pair[1L]]], m[[pair[2L]]])) stop("stored-array hash mismatch: ", pair[1L])
  list(X = d$X, y = y, hashes = hashes, input_path = input, manifest_path = manifest,
    manifest_sha256 = smcbvs_file_hash(manifest), manifest_row = m)
}
smcbvs_source_record <- function(core_dir) {
  core_dir <- normalizePath(core_dir, winslash = "/", mustWork = TRUE)
  files <- c(list.files(core_dir, "\\.R$", full.names = TRUE),
    list.files(file.path(core_dir, "cpp"), "\\.(cpp|h|v3)$", full.names = TRUE),
    list.files(.smcbvs_adapter_dir, "\\.(R|md)$", full.names = TRUE))
  # v2.1 (A-CODE F1): radix sort is C-locale byte order, so the aggregate source hash
  # is the same on every host whatever its collation locale.
  files <- sort(unique(files), method = "radix")
  labels <- ifelse(startsWith(files, paste0(core_dir, "/")),
    paste0("core/", substring(files, nchar(core_dir) + 2L)), paste0("study/", basename(files)))
  hashes <- setNames(vapply(files, smcbvs_file_hash, ""), labels)
  aggregate <- function(h) digest::digest(paste(names(h), h, collapse = "\n"), algo = "sha256", serialize = FALSE)
  list(core_dir = core_dir, study_dir = .smcbvs_adapter_dir, files = hashes,
    source_sha256 = aggregate(hashes), v3_source_sha256 = aggregate(hashes[startsWith(names(hashes), "core/")]))
}
smcbvs_check_support <- function(x, p, name) {
  if (is.null(x)) return(NULL)
  if (!is.numeric(x) || anyNA(x) || any(!is.finite(x)) || any(x != as.integer(x)) ||
      any(x < 1L | x > p) || anyDuplicated(x)) stop("invalid original-index ", name)
  sort(as.integer(x))
}
# Full original-index vector: dropped columns are zero only when retained PIPs were computed.
# Unavailable PIPs remain NA, including in no_predictors/y_constant fits.
smcbvs_outputs <- function(fit, p) {
  if (!is.list(fit) || !is.character(fit$status) || length(fit$status) != 1L ||
      !fit$status %in% setdiff(smcbvs_native_statuses, "adapter_error")) stop("core returned an invalid native status")
  if (!is.null(fit$pip_secondary)) stop("core returned excluded secondary PIP")
  hpm <- smcbvs_check_support(fit$hpm, p, "HPM")
  available <- fit$status %in% c("exact", "completed") && !identical(fit$estimates_available, FALSE)
  pip <- setNames(rep(NA_real_, p), as.character(seq_len(p)))
  mpm <- smcbvs_check_support(fit$mpm, p, "MPM")
  if (available && is.null(hpm)) stop("completed core fit is missing HPM")
  # Failed fits can still supply primary PIPs and supports. Preserve them for audit,
  # independently of estimates_available and benchmark selection eligibility.
  if (available || !is.null(fit$pip_primary)) {
    keep <- fit$preprocessing$kept
    drop <- fit$preprocessing$dropped
    if (is.null(keep) || is.null(drop)) stop("completed fit missing preprocessing index map")
    keep <- smcbvs_check_support(keep, p, "kept columns")
    drop <- smcbvs_check_support(drop, p, "dropped columns")
    if (!identical(sort(c(keep, drop)), seq_len(p))) stop("preprocessing map does not partition original columns")
    q <- fit$pip_primary
    if (!is.numeric(q) || is.null(names(q)) || anyDuplicated(names(q)) ||
        !setequal(names(q), as.character(keep)) || any(!is.finite(q)) || any(q < 0 | q > 1))
      stop("primary PIPs must be finite, named by every retained original index")
    pip[] <- 0; pip[names(q)] <- q
    derived <- unname(which(pip > 0.5))
    if (available && (is.null(mpm) || !identical(mpm, derived)))
      stop("core MPM differs from strict primary PIP > .5")
    if (is.null(mpm)) mpm <- derived
    if (available && length(intersect(hpm, drop))) stop("HPM includes a dropped column")
  }
  list(hpm = hpm, mpm = unname(mpm), pip = pip, estimates_available = available)
}
smcbvs_flag_value <- function(fit, nm) {
  x <- if (is.list(fit$flags)) fit$flags[[nm]] else NULL
  if (is.null(x)) x <- fit[[nm]]
  if (is.null(x) && is.list(fit$calibration) && is.list(fit$calibration$flags))
    x <- fit$calibration$flags[[nm]]
  if (is.null(x)) return(NA)
  if (identical(nm, "forced_pilot_steps") && is.numeric(x) && length(x) == 1L &&
      (is.na(x) || (is.finite(x) && x >= 0))) return(x > 0)
  if (!is.logical(x) || length(x) != 1L) stop("diagnostic flag is not scalar logical: ", nm)
  x
}
smcbvs_local_limit <- function(fit) {
  # R-1's named quality check applies wherever it fired. Early failed final
  # assembly does not promote the archived search flag to the top-level flags.
  cal <- fit$calibration
  values <- list(fit$local_limit, fit$flags$local_limit, fit$local_search$local_limit,
    fit$partial_final$local_search$local_limit, cal$flags$local_limit)
  for (triggers in cal$flags$triggers_by_tier) values <- c(values, list(triggers$local_limit))
  for (tier in cal$tiers) {
    values <- c(values, list(tier$triggers$local_limit, tier$pilot$local_search$local_limit,
      tier$partial_operation$local_search$local_limit))
    for (iteration in tier$iterations) values <- c(values, list(iteration$local_search$local_limit))
  }
  any(vapply(values, isTRUE, TRUE))
}
smcbvs_diagnostics <- function(fit, native_status) {
  # Absent/NA checks did not fail. In particular exact fits need no SMC diagnostics.
  final_failed <- identical(smcbvs_flag_value(fit, "checks_passed_final"), FALSE)
  final <- paste0("final_check_E", 1:3)[vapply(paste0("E", 1:3), function(nm)
    final_failed && isTRUE(smcbvs_flag_value(fit, nm)), TRUE)]
  numerical <- c("low_empirical_ESS", "grid_unconverged", "local_limit")
  fired <- numerical[vapply(numerical, function(nm)
    if (nm == "local_limit") smcbvs_local_limit(fit) else isTRUE(smcbvs_flag_value(fit, nm)), TRUE)]
  info <- c("escalated", "cut_group", "near_tie_truncated", "forced_pilot_steps")
  informational <- info[vapply(info, function(nm) isTRUE(smcbvs_flag_value(fit, nm)), TRUE)]
  exact_branch <- identical(native_status, "exact") || identical(fit$branch_run, "exact") ||
    isTRUE(smcbvs_flag_value(fit, "exact_branch"))
  if (exact_branch) informational <- c(informational, "exact_branch")
  if (identical(smcbvs_flag_value(fit, "local_certified"), FALSE))
    informational <- c(informational, "local_certified_false")
  if (isTRUE(smcbvs_flag_value(fit, "global_certified"))) informational <- c(informational, "global_certified")
  list(flag = final_failed || length(fired) > 0L, codes = c(final, fired, informational))
}
smcbvs_rule_rows <- function(fit, outputs, design, policy, warnings = character(), messages = character(), error = NULL,
                             native_status = fit$status) {
  smcbvs_validate_policy(policy)
  if (!is.list(fit)) fit <- list()
  diagnostics <- smcbvs_diagnostics(fit, native_status)
  policy_hash <- digest::digest(serialize(policy, NULL, version = 3), algo = "sha256", serialize = FALSE)
  native_flags <- list(flags = fit$flags, cut_group = fit$cut_group, cut_group_count = fit$cut_group_count,
    cut_group_components = fit$cut_group_components, local_limit = fit$local_limit,
    local_certified = fit$local_certified, global_certified = fit$global_certified,
    near_tie_truncated = fit$near_tie_truncated)
  rows <- lapply(c("hpm", "pip05"), function(rule) {
    support <- outputs[[if (rule == "hpm") "hpm" else "mpm"]]
    status <- unname(policy$status_map[[native_status]])
    # Missing rule estimates are failures even if the other rule has a legitimate empty support.
    if (is.null(support)) status <- "failed"
    if (status == "ok" && length(c(warnings, messages))) status <- "warning"
    failed <- status %in% c("failed", "timeout", "not_run")
    err <- error
    if (failed && is.null(err)) err <- paste0("v3_status=", native_status,
      if (is.null(support)) "; rule estimate unavailable" else "; incomplete fit; support is audit only")
    r <- list(rule_id = rule, role = unname(policy$roles[[rule]]), status = status,
      converged = NA, diag_flag = diagnostics$flag,
      diag_codes = paste(diagnostics$codes, collapse = ";"), n_warnings = length(warnings) + length(messages),
      warnings = smcbvs_collapse(warnings), messages = smcbvs_collapse(messages),
      error = if (is.null(err)) NA_character_ else err,
      k = if (failed) NA_integer_ else length(support),
      support = if (failed) NA_character_ else smcbvs_support_key(support),
      support_audit = if (failed) smcbvs_support_key(support) else NA_character_,
      v3_status = native_status, v3_estimates_available = outputs$estimates_available,
      v3_partial_results = isTRUE(fit$partial_results) || native_status %in% c("schedule_limit", "numerical_failure", "resource_limit"),
      v3_p_retained = if (!is.null(fit$p)) fit$p else if (is.list(fit$preprocessing) &&
        !is.null(fit$preprocessing$p)) fit$preprocessing$p else NA_integer_,
      v3_flags_json = as.character(jsonlite::toJSON(native_flags, auto_unbox = TRUE, null = "null", na = "null")),
      adapter_mapping_status = policy$mapping_status, adapter_policy_id = policy$id,
      adapter_policy_sha256 = policy_hash)
    # Remapping historical designs cannot replace computed fields or R-1 provenance.
    for (nm in setdiff(names(design), names(r))) r[[nm]] <- design[[nm]]
    r$fold_seed <- NA_integer_; r$fold_sha256 <- NA_character_
    for (nm in setdiff(smcbvs_schema(), names(r))) r[[nm]] <- NA
    as.data.frame(r[smcbvs_schema()], stringsAsFactors = FALSE)
  })
  do.call(rbind, rows)
}
smcbvs_done_valid <- function(prefix, expect) {
  if (!file.exists(paste0(prefix, ".done")) || !file.exists(paste0(prefix, ".sha256"))) return(FALSE)
  tryCatch({
    parts <- strsplit(readLines(paste0(prefix, ".sha256"), warn = FALSE), "  ", fixed = TRUE)
    if (length(parts) != 2L || any(lengths(parts) != 2L)) return(FALSE)
    listed <- vapply(parts, `[`, "", 2L)
    if (!setequal(listed, paste0(basename(prefix), c(".rds", ".csv")))) return(FALSE)
    if (!all(vapply(parts, function(z) {
      f <- file.path(dirname(prefix), z[2L]); file.exists(f) && identical(smcbvs_file_hash(f), z[1L])
    }, TRUE))) return(FALSE)
    rows <- utils::read.csv(paste0(prefix, ".csv"), colClasses = "character", stringsAsFactors = FALSE)
    if (nrow(rows) != 2L || !setequal(rows$rule_id, c("hpm", "pip05"))) return(FALSE)
    all(vapply(names(expect), function(nm) !is.null(rows[[nm]]) &&
      all(!is.na(rows[[nm]]) & rows[[nm]] == as.character(expect[[nm]])), TRUE))
  }, error = function(e) FALSE)
}
smcbvs_write_record <- function(prefix, record) {
  smcbvs_atomic(paste0(prefix, ".rds"), function(f) saveRDS(record, f, compress = "xz", version = 3))
  smcbvs_atomic(paste0(prefix, ".csv"), function(f) utils::write.csv(record$rows, f, row.names = FALSE, na = "NA"))
  paths <- paste0(prefix, c(".rds", ".csv"))
  smcbvs_atomic(paste0(prefix, ".sha256"), function(f) writeLines(
    paste(vapply(paths, smcbvs_file_hash, ""), basename(paths), sep = "  "), f))
  smcbvs_atomic(paste0(prefix, ".done"), function(f) writeLines(c(
    paste("status", paste(record$rows$status, collapse = ",")), paste("finished_utc", record$finished_utc)), f))
}

smcbvs_study_fit <- function(case, scale, study, outroot, run_id, policy = smcbvs_r1_policy(),
                             allocation = list(mem_gb = 8, hours = 24),
                             core_dir = file.path(.smcbvs_adapter_dir, "..", "core"),
                             manifest = NULL, development = FALSE) {
  for (pk in c("digest", "jsonlite")) if (!requireNamespace(pk, quietly = TRUE)) stop("missing package: ", pk)
  spec <- smcbvs_case_spec(case, scale, development)
  if (!is.character(run_id) || length(run_id) != 1L || !grepl("^[A-Za-z0-9][A-Za-z0-9_.-]*$", run_id)) stop("invalid run_id")
  smcbvs_validate_policy(policy, development)
  if (!is.list(allocation) || !all(c("mem_gb", "hours") %in% names(allocation)) ||
      !all(vapply(allocation[c("mem_gb", "hours")], function(x)
        is.numeric(x) && length(x) == 1L && is.finite(x) && x > 0, TRUE))) stop("bad allocation")
  allocation <- list(mem_gb = as.double(allocation$mem_gb), hours = as.double(allocation$hours))
  allocation_hash <- digest::digest(serialize(allocation, NULL, version = 3), algo = "sha256", serialize = FALSE)
  policy_hash <- digest::digest(serialize(policy, NULL, version = 3), algo = "sha256", serialize = FALSE)
  input <- smcbvs_load_input(spec, study, manifest)
  source_record <- smcbvs_source_record(core_dir)
  # Do not allow results beneath the frozen input study, even for an accidental outroot.
  study_path <- smcbvs_safe_path(study)
  outroot <- smcbvs_output_root(outroot, study_path)
  outdir <- file.path(outroot, "results", run_id, sprintf("p%04d", spec$p), spec$case_id)
  future_outdir <- smcbvs_resolve_future(outdir)
  if (!startsWith(future_outdir, paste0(outroot, "/"))) stop("output directory symlink escapes outroot")
  dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
  outdir <- smcbvs_contained(outdir, outroot)
  prefix <- file.path(outdir, "SMCBVS")
  expect <- c(list(run_id = run_id, method_id = "SMCBVS", case_id = spec$case_id, source_sha256 = source_record$source_sha256,
    method_seed = spec$method_seed, adapter_policy_sha256 = policy_hash, allocation_sha256 = allocation_hash,
    input_manifest_sha256 = input$manifest_sha256), input$hashes[setdiff(names(input$hashes), "fold_sha256")])
  # A valid saved unit has immutable run identity. Require a new run ID when any
  # allocation/source/policy/input identity changes; retain the historical output.
  if (smcbvs_done_valid(prefix, list()) && !smcbvs_done_valid(prefix, expect)) {
    saved <- utils::read.csv(paste0(prefix, ".csv"), colClasses = "character", stringsAsFactors = FALSE)
    mismatch <- names(expect)[!vapply(names(expect), function(nm) !is.null(saved[[nm]]) &&
      all(!is.na(saved[[nm]]) & saved[[nm]] == as.character(expect[[nm]])), TRUE)]
    stop("saved unit identity mismatch (", paste(mismatch, collapse = ", "), "); use a new run_id")
  }
  if (smcbvs_done_valid(prefix, expect)) return(invisible(list(prefix = prefix, skipped = TRUE,
    rows = utils::read.csv(paste0(prefix, ".csv"), stringsAsFactors = FALSE))))
  # Do not permit concurrent writers to the same unit. Stale locks require operator inspection.
  lock <- paste0(prefix, ".lock")
  if (!dir.create(lock, showWarnings = FALSE)) stop("unit lock exists: ", lock)
  on.exit(unlink(lock, recursive = TRUE), add = TRUE)
  writeLines(c(paste("pid", Sys.getpid()), paste("host", Sys.info()[["nodename"]]), paste("utc", smcbvs_utc())), file.path(lock, "owner.txt"))
  unlink(paste0(prefix, ".done"))
  # Compilation/loading is outside runtime_s. Only X/y/seed/allocation reach the core.
  source(file.path(source_record$core_dir, "v3.R"), local = FALSE)
  if (!is.function(v3_fit)) stop("core loader did not expose v3_fit")
  started <- smcbvs_utc(); t0 <- proc.time()[["elapsed"]]
  warnings <- messages <- character(); fit <- NULL; outputs <- NULL; error <- NULL
  withCallingHandlers(tryCatch({
    fit <- v3_fit(input$X, input$y, spec$method_seed, allocation = allocation)
    outputs <- smcbvs_outputs(fit, spec$p)
  }, error = function(e) { error <<- conditionMessage(e) }),
  warning = function(w) { warnings <<- c(warnings, conditionMessage(w)); invokeRestart("muffleWarning") },
  message = function(m) { messages <<- c(messages, conditionMessage(m)); invokeRestart("muffleMessage") })
  runtime <- as.numeric(proc.time()[["elapsed"]] - t0); finished <- smcbvs_utc()
  # v2.1 (A-CODE F3): an R-level memory-allocation error is recorded like any other R error
  # from the fit (native adapter_error, both rules failed, message verbatim), as the benchmark's
  # outer tryCatch records it. Kills by the scheduler (no .done) remain infrastructure events.
  native <- if (is.null(error)) fit$status else "adapter_error"
  if (is.null(outputs)) outputs <- list(hpm = NULL, mpm = NULL,
    pip = setNames(rep(NA_real_, spec$p), as.character(seq_len(spec$p))), estimates_available = FALSE)
  # Recover independently valid audit outputs after validation errors. The raw fit
  # remains unchanged; a shadow failure status disables successful-rule consistency checks.
  if (native == "adapter_error" && is.list(fit)) {
    audit <- fit; audit$status <- "numerical_failure"; audit$estimates_available <- FALSE
    outputs <- tryCatch(smcbvs_outputs(audit, spec$p), error = function(e) outputs)
    outputs$hpm <- tryCatch(smcbvs_check_support(fit$hpm, spec$p, "audit HPM"), error = function(e) NULL)
    outputs$mpm <- tryCatch(smcbvs_check_support(fit$mpm, spec$p, "audit MPM"), error = function(e) outputs$mpm)
  }
  host <- Sys.info()[["nodename"]]
  design <- c(list(study = "bench20261019", run_id = run_id, source_sha256 = source_record$source_sha256, regime = "H"),
    spec[c("p", "scenario", "replicate", "scale_key", "scale", "dataset_id", "case_id", "data_seed", "fold_seed", "method_seed")],
    input$hashes, list(method_id = "SMCBVS", method_label = "SMC-BVS v3", package = "SMCBVS-v3", package_version = "3",
      runtime_s = runtime, host = host, slurm_job_id = Sys.getenv("SLURM_JOB_ID", NA_character_),
      slurm_array_task_id = Sys.getenv("SLURM_ARRAY_TASK_ID", NA_character_), started_utc = started, finished_utc = finished,
      v3_version = "3", v3_source_sha256 = source_record$v3_source_sha256,
      v3_target_scale = "standardised working model; not raw-data marginal likelihood",
      allocation_sha256 = allocation_hash, input_manifest_sha256 = input$manifest_sha256,
      adapter_mapping_status = policy$mapping_status, adapter_policy_id = policy$id, adapter_policy_sha256 = policy_hash))
  # Folds are validated as input provenance, but this sampler never uses them.
  design$fold_seed <- NA_integer_; design$fold_sha256 <- NA_character_
  rows <- smcbvs_rule_rows(fit, outputs, design, policy, warnings, messages, error, native)
  thread_vars <- c("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS")
  record <- list(schema_version = 2L, adapter_version = "2.1-R1", rows = rows, fit = fit,
    pip = outputs$pip, pip_primary_original = outputs$pip, hpm = outputs$hpm, mpm = outputs$mpm,
    native_status = native, estimates_available = outputs$estimates_available,
    warnings = warnings, messages = messages, error = error, runtime_s = runtime,
    case = spec, input = c(input[c("input_path", "manifest_path", "manifest_sha256", "manifest_row")], input$hashes),
    code = source_record, adapter_policy = policy, adapter_policy_sha256 = policy_hash,
    allocation = allocation, allocation_sha256 = allocation_hash,
    target_scale = design$v3_target_scale,
    environment = list(R = R.version.string, session_info = utils::capture.output(utils::sessionInfo()),
      lib_paths = .libPaths(), host = host, pid = Sys.getpid(), RNGkind = RNGkind(),
      command = commandArgs(FALSE), threads = as.list(Sys.getenv(thread_vars, unset = NA_character_)),
      slurm = as.list(Sys.getenv(c("SLURM_JOB_ID", "SLURM_ARRAY_JOB_ID", "SLURM_ARRAY_TASK_ID", "SLURM_CPUS_PER_TASK",
        "SLURM_MEM_PER_NODE", "SLURM_MEM_PER_CPU", "SLURM_TIMELIMIT"), unset = NA_character_)),
      compiler = Sys.getenv(c("CC", "CXX", "CXX17", "LOADEDMODULES"), unset = NA_character_)),
    started_utc = started, finished_utc = finished)
  smcbvs_write_record(prefix, record)
  invisible(list(prefix = prefix, skipped = FALSE, rows = rows, native_status = native))
}
