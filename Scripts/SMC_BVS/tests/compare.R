args <- commandArgs(TRUE); stopifnot(length(args) == 2L)
out <- args[1]; source(file.path(args[2], "common.R"))
checks <- list()
check <- function(label, expr) {
  checks[[label]] <<- record(label, expr)
  cat(if (checks[[label]]$ok) "PASS" else "FAIL", label,
      if (!checks[[label]]$ok) checks[[label]]$error else "", "\n")
}
paths <- file.path(out, c("prototype", "production"), "raw_results.rds")
if (!all(file.exists(paths))) {
  check("workers_produced_raw_results", stop("worker output missing; inspect prototype/worker.log and production/worker.log"))
} else {
  ref <- readRDS(paths[1]); prod <- readRDS(paths[2])
  validate_cache_policy <- function(a, b) {
    exact(a$cache_policy$p, b$cache_policy$p, "cache policy/p")
    p <- a$cache_policy$p
    need(is.numeric(p) && length(p) == 1L && is.finite(p) && p > 0, "invalid cache policy dimension")
    expected_ref <- as.numeric(max(500 * p, 32768))
    expected_prod <- as.numeric(500 * p)
    exact(a$cache_policy$run_settings_capacity, expected_ref, "prototype/run settings/cache capacity")
    exact(b$cache_policy$run_settings_capacity, expected_prod, "production/run settings/cache capacity")
    exact(a$calibration_full$cache[["capacity"]], expected_ref, "prototype/calibration/cache capacity")
    exact(b$calibration_full$cache[["capacity"]], expected_prod, "production/calibration/cache capacity")
    TRUE
  }
  check("R5_cache_capacity_expected_difference_before_normalization", {
    validate_cache_policy(ref, prod)
    bad <- prod; bad$calibration_full$cache[["capacity"]] <- ref$calibration_full$cache[["capacity"]]
    need(500 * ref$cache_policy$p < 32768, "ordinary small-p cache mutation fixture no longer distinguishes policies")
    rejected <- tryCatch({ validate_cache_policy(ref, bad); FALSE }, error = function(e) TRUE)
    need(rejected, "obsolete calibration cache floor escaped validation")
    bad <- prod; bad$cache_policy$run_settings_capacity <- ref$cache_policy$run_settings_capacity
    rejected <- tryCatch({ validate_cache_policy(ref, bad); FALSE }, error = function(e) TRUE)
    need(rejected, "obsolete run-settings cache floor escaped validation")
    TRUE
  })
  normalize_calibration_capacity <- function(a, b) {
    validate_cache_policy(a, b)
    # R-5 B-O1 changes precisely this one entry. The vector's names, type,
    # attributes and every hit/miss/insert/clear counter remain compared below.
    x <- b$calibration_full
    x$cache[["capacity"]] <- a$calibration_full$cache[["capacity"]]
    x
  }
  check("required_certificate_labels_before_normalization", {
    validate_labels <- function(x, label) {
      need(length(x$scores) > 0L, "scorer certificate fixtures missing")
      for (s in x$scores) exact(s$error_bound_kind, label, "score/error_bound_kind")
      exact(x$exact$hpm_error_bound_kind, label, "exact/hpm_error_bound_kind")
      exact(x$exact$R9$hpm_error_bound_kind, label, "exact/R9/hpm_error_bound_kind")
      TRUE
    }
    validate_labels(ref, "heuristic_condition_estimate")
    validate_labels(prod, "heuristic (not a validated interval bound)")
    mutated <- prod
    mutated$scores[[1]]$error_bound_kind <- "heuristic_condition_estimate"
    rejected <- tryCatch({ validate_labels(mutated, "heuristic (not a validated interval bound)"); FALSE },
                         error = function(e) TRUE)
    need(rejected, "obsolete production certificate label escaped validation")
    TRUE
  })
  # Explicit, reviewed differences only. A missing shared output is an error.
  # Per-event profiling and offspring trace were removed; phase labels/partial
  # records are additive operational metadata checked by changed_units.R.
  normalize <- function(x) {
    if (!is.list(x) || is.data.frame(x)) return(x)
    # Part I requires the explicit non-validated certificate label. Preserve all
    # numeric error estimates and certificate comparisons; map only these two
    # exact, documented string values to the prototype's label.
    for (nm in c("error_bound_kind", "hpm_error_bound_kind")) if (nm %in% names(x)) {
      need(x[[nm]] %in% c("heuristic_condition_estimate", "heuristic (not a validated interval bound)"),
           paste("unexpected certificate label", nm))
      x[[nm]] <- "heuristic_condition_estimate"
    }
    if (all(c("log_Z", "phi", "rb_round") %in% names(x))) {
      if (!is.null(x$partial)) need(!x$partial, "unexpected partial ordinary regression island")
      x[c("offspring", "partial", "phase", "tier", "iter", "island", "stream")] <- NULL
    }
    if (all(c("termination", "scanned_centres", "returned") %in% names(x)))
      x[c("phase", "tier", "iter", "island")] <- NULL
    if (all(c("tiers", "tier_final", "calibration_seed") %in% names(x))) x$stage_table <- NULL
    if (all(c("grid_source", "pilot") %in% names(x)) ||
        all(c("sha256", "grid", "inherited") %in% names(x))) x[c("rho_V", "grid_label")] <- NULL
    if (all(c("label", "grid", "F_V_evaluations") %in% names(x))) x$rho_appended <- NULL
    if (all(c("iteration", "grid", "calibration_estimate") %in% names(x))) x[c("rho_V", "grid_label")] <- NULL
    if ("calibration_estimate" %in% names(x) && !is.null(x$partial)) {
      need(!x$partial, "unexpected partial calibration archive"); x$partial <- NULL
    }
    if ("label" %in% names(x) && any(c("log_Z", "log_Z_r") %in% names(x)) &&
        grepl("calibration estimate", x$label, fixed = TRUE)) {
      if (!is.null(x$partial)) need(!x$partial, "unexpected partial calibration estimate")
      x[c("label", "partial")] <- NULL
    }
    # New full calibration stage archives are checked via the raw-island
    # comparisons and production checkpoint unit; reference has no such field.
    x[c("seconds", "seconds_local", "seconds_total", "timings", "stage_record")] <- NULL
    y <- lapply(x, normalize); attributes(y) <- attributes(x)
    # Named field insertion order is an output-layout change, not arithmetic.
    # Require identical field sets and values by sorting complete unique names.
    nm <- names(y)
    if (length(nm) && all(nzchar(nm)) && !anyDuplicated(nm)) {
      at <- attributes(y); y <- y[order(nm)]; at$names <- names(y); attributes(y) <- at
    }
    y
  }
  check("R5_cache_projection_preserves_every_counter", {
    b <- normalize_calibration_capacity(ref, prod)
    exact(ref$calibration_full$cache, b$cache, "calibration/cache/all counters")
    counters <- setdiff(names(prod$calibration_full$cache), "capacity")
    need(all(c("hits", "misses", "inserts", "clears") %in% counters), "calibration cache counters missing")
    # Each counter mutation must survive the capacity projection and fail the
    # byte comparator. This also covers any future additional cache counter.
    for (nm in counters) {
      bad <- prod
      bad$calibration_full$cache[[nm]] <- bad$calibration_full$cache[[nm]] + 1
      projected <- normalize_calibration_capacity(ref, bad)
      rejected <- tryCatch({ exact(ref$calibration_full$cache, projected$cache); FALSE },
                           error = function(e) TRUE)
      need(rejected, paste("capacity projection hid changed cache counter", nm))
    }
    TRUE
  })
  for (field in c("pre", "budgets", "blocks", "tables", "neighbours", "start", "scores", "locals", "exact",
                  "rng", "resampling", "micro", "pilot_micro", "cal_rules")) {
    check(paste0("bits_", field), {
      need(field %in% names(ref) && field %in% names(prod), paste("missing", field))
      exact(normalize(ref[[field]]), normalize(prod[[field]]), field); TRUE
    })
  }
  # The numeric calibration islands, V, all leaders, two stream-continuing
  # rebuilds and tier-1 pilot must match, including each RNG word/count/next draw.
  check("bits_calibration_raw", {
    a <- normalize(ref$calibration); b <- normalize(prod$calibration)
    # Aggregate operational ledgers remain; no event dump requested.
    exact(a, b, "calibration"); TRUE
  })
  for (field in c("raw_final", "final_inherited", "calibration_full", "calibrated_final")) check(paste0("bits_", field), {
    b <- if (field == "calibration_full") normalize_calibration_capacity(ref, prod) else prod[[field]]
    exact(normalize(ref[[field]]), normalize(b), field); TRUE
  })
  check("bits_final_outputs_and_flags", {
    a <- ref$final; b <- prod$final
    need(all(names(a$stage_table) %in% names(b$stage_table)), "shared final-stage columns missing")
    b$stage_table <- b$stage_table[, names(a$stage_table), drop = FALSE]
    # r2 adds validated operational stream/seed documentation; old map is a string.
    for (name in c("stream_map", "streams", "seeding_doc", "variate_order_doc")) { a[[name]] <- NULL; b[[name]] <- NULL }
    a <- normalize(a); b <- normalize(b)
    need("pip_secondary" %in% names(a) && !("pip_secondary" %in% names(b)), "secondary-output intentional difference not demonstrated")
    a$pip_secondary <- NULL
    expected <- isTRUE(ref$final$local_search$local_certified) &&
      identical(as.integer(ref$final$hpm), as.integer(ref$final$local_search$returned))
    need(identical(prod$final$local_certified, expected), "local certificate does not concern selected HPM")
    a$local_certified <- expected
    exact(normalize(a), normalize(b), "final"); TRUE
  })
  check("inputs_and_seed_identity", {
    exact(readRDS(file.path(out, "prototype", "input.rds")), readRDS(file.path(out, "production", "input.rds")))
    a <- readRDS(file.path(out, "prototype", "metadata.rds"))
    b <- readRDS(file.path(out, "production", "metadata.rds"))
    exact(a$seed, b$seed); exact(a$index, b$index)
    exact(a$test_source_sha256, b$test_source_sha256, "shared test source hashes"); TRUE
  })
}
for (side in c("prototype", "production")) {
  p <- file.path(out, side, "unit_results.rds")
  check(paste0(side, "_all_units"), {
    need(file.exists(p), paste(side, "unit evidence missing"))
    r <- readRDS(p); failed <- r[!vapply(r, `[[`, TRUE, "ok")]
    need(!length(failed), paste(vapply(failed, function(z) paste(z$test, z$error, sep = ": "), ""), collapse = "; "))
    TRUE
  })
  check(paste0(side, "_unit_and_source_inventory"), {
    r <- readRDS(p)
    catalog <- readRDS(file.path(out, side, "unit_catalog.rds"))
    meta <- readRDS(file.path(out, side, "metadata.rds"))
    bytes <- readRDS(file.path(out, side, "test_source_bytes.rds"))
    exact(names(catalog), names(r), paste0(side, "/registered unit labels"))
    exact(names(bytes), names(meta$test_source_sha256), paste0(side, "/source byte inventory"))
    exact(meta$test_source_sha256, meta$test_source_sha256_after, paste0(side, "/test sources unchanged"))
    for (f in names(bytes)) exact(digest::digest(bytes[[f]], algo = "sha256", serialize = FALSE),
      unname(meta$test_source_sha256[[f]]), paste0(side, "/source bytes/", f))
    for (u in names(catalog)) {
      entry <- catalog[[u]]
      need(entry$source %in% names(bytes), paste("unit source missing", u))
      exact(entry$sha256, unname(meta$test_source_sha256[[entry$source]]), paste0(side, "/unit source/", u))
    }
    if (side == "production") for (f in c("v2_preprocess_units.R", "v2_runtime_units.R"))
      need(any(vapply(catalog, function(x) identical(x$source, f), TRUE)), paste("required v2 units missing", f))
    TRUE
  })
}
saveRDS(checks, file.path(out, "comparison.rds"), version = 3)
summary <- lapply(checks, function(z) z[setdiff(names(z), "value")])
jsonlite::write_json(summary, file.path(out, "comparison.json"), auto_unbox = TRUE, pretty = TRUE, digits = NA)
failed <- sum(!vapply(checks, `[[`, TRUE, "ok"))
lines <- c("# A build regression evidence", "", paste("Checks:", length(checks), "Failures:", failed), "",
           "Numeric comparisons use IEEE-754 double bytes; no numeric tolerance. Source/seed/environment and raw outputs are saved beside this report.", "",
           vapply(checks, function(z) paste0("- ", if (z$ok) "PASS " else "FAIL ", z$test,
                                           if (!z$ok) paste0(": ", z$error) else ""), ""))
writeLines(lines, file.path(out, "REPORT.md"))
quit(status = if (failed) 1L else 0L)
