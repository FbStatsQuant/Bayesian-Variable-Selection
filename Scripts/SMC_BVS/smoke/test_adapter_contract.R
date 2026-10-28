#!/usr/bin/env Rscript
# Root runs on Owls (nice19): Rscript smoke/test_adapter_contract.R OUTPUT_DIR
# Deterministic adapter fixtures only: no generation, inference or C++ compilation.
if (sys.nframe() == 0L) {
  args <- commandArgs(trailingOnly = TRUE)
  if (length(args) != 1L) stop("supply an empty evidence/output directory")
  this <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1L])
  here <- dirname(normalizePath(this, mustWork = TRUE))
  source(file.path(here, "..", "code", "study", "adapter.R"), local = FALSE)
  for (pk in c("digest", "jsonlite")) stopifnot(requireNamespace(pk, quietly = TRUE))
  root <- smcbvs_output_root(args[1L], "/projects/ml75/fb31/BVS/bench20261019")
  if (length(list.files(root, all.files = TRUE, no.. = TRUE))) stop("test output directory must be empty")
  started <- smcbvs_utc(); tests <- character(); rejection_evidence <- list()
  check <- function(label, expr) { force(expr); tests <<- c(tests, label); cat("PASS", label, "\n") }
  expect_error <- function(expr, message) {
    err <- tryCatch({ force(expr); NULL }, error = identity)
    stopifnot(inherits(err, "error"), identical(conditionMessage(err), message))
    invisible(message)
  }
  unit_hashes <- function(prefix) {
    paths <- paste0(prefix, c(".rds", ".csv", ".sha256", ".done"))
    stopifnot(all(file.exists(paths)))
    setNames(vapply(paths, smcbvs_file_hash, ""), paths)
  }
  expect_immutable <- function(label, expr, fields, prefixes) {
    before <- lapply(prefixes, unit_hashes)
    expected <- paste0("saved unit identity mismatch (", paste(fields, collapse = ", "), "); use a new run_id")
    expect_error(expr, expected)
    after <- lapply(prefixes, unit_hashes)
    stopifnot(identical(before, after), !any(file.exists(paste0(prefixes, ".lock"))))
    rejection_evidence[[label]] <<- list(error = expected, before = before, after = after)
    invisible(TRUE)
  }
  old_fixture <- Sys.getenv("SMCBVS_ADAPTER_FIXTURE", unset = NA_character_)
  old_scale <- Sys.getenv("SMCBVS_ADAPTER_EXPECT_SCALE", unset = NA_character_)
  study <- file.path(root, "dev_inputs"); out <- file.path(root, "fit_outputs"); core <- file.path(root, "fixture_core")
  dir.create(file.path(study, "inputs", "p0500"), recursive = TRUE)
  dir.create(file.path(study, "manifests"), recursive = TRUE); dir.create(core)
  file.copy(file.path(here, "fixtures", "core", "v3.R"), file.path(core, "v3.R"))
  spec <- smcbvs_case_spec("dev_p0500_S1_r001", "c100", TRUE)
  X <- matrix(rep(as.double(seq_len(200L)), 500L), 200L); X[, 1L] <- 1
  d <- list(X = X, Y = cbind(c100 = as.double(seq_len(200L)), c050 = as.double(201:400)),
    foldid = rep(1:10, 20), dataset_id = spec$dataset_id, p = 500L, n = 200L,
    scenario = 1L, replicate = 1L, kind = "dev", data_seed = spec$data_seed,
    fold_seed = spec$fold_seed, method_seed = spec$method_seed, scales = c(c100 = 1, c050 = 0.5))
  input <- file.path(study, "inputs", "p0500", paste0(spec$dataset_id, ".rds")); saveRDS(d, input, compress = FALSE)
  manifest <- file.path(study, "manifests", "dev_inputs_manifest.csv")
  m <- data.frame(dataset_id = spec$dataset_id, p = 500L, scenario = 1L, replicate = 1L,
    data_seed = spec$data_seed, fold_seed = spec$fold_seed, method_seed = spec$method_seed,
    file_sha256 = smcbvs_file_hash(input), x_sha256 = smcbvs_f64_hash(X), foldid_sha256 = smcbvs_f64_hash(d$foldid),
    y_c100_sha256 = smcbvs_f64_hash(d$Y[, "c100"]), y_c050_sha256 = smcbvs_f64_hash(d$Y[, "c050"]))
  write_manifest <- function() utils::write.csv(m, manifest, row.names = FALSE)
  write_manifest()
  run <- function(mode, key = mode, scale = "c100", ...) {
    Sys.setenv(SMCBVS_ADAPTER_FIXTURE = mode, SMCBVS_ADAPTER_EXPECT_SCALE = scale)
    smcbvs_study_fit(spec$dataset_id, scale, study, out, key, core_dir = core, development = TRUE, ...)
  }
  # Independent byte convention, including literal IEEE754 encoding of 1.0.
  check("float64 LE byte hash", stopifnot(identical(smcbvs_f64_hash(1), digest::digest(
    as.raw(c(0, 0, 0, 0, 0, 0, 240, 63)), algo = "sha256", serialize = FALSE))))
  check("column-major array bytes", stopifnot(identical(smcbvs_f64_hash(matrix(1:6, 2)),
    digest::digest(writeBin(as.double(1:6), raw(), endian = "little"), algo = "sha256", serialize = FALSE))))
  check("production and dev seed ranges", {
    stopifnot(smcbvs_case_spec("p1000_S6_r100", "c050")$method_seed == 5570100L,
      smcbvs_case_spec("dev_p1000_S1_r001", "c100", TRUE)$method_seed == 6520001L)
  })
  check("dev/production and scale guards", {
    expect_error(smcbvs_case_spec(spec$dataset_id, "c100"), "development switch and dev_ prefix must agree")
    expect_error(smcbvs_case_spec("p0500_S1_r001", "c100", TRUE), "development switch and dev_ prefix must agree")
    expect_error(smcbvs_case_spec(paste0(spec$dataset_id, "_c050"), "c100", TRUE), "case ID/scale mismatch")
    expect_error(smcbvs_case_spec("p0500_S1_r000", "c100"), "replicate outside 1..100")
  })
  result <- run("completed"); r <- readRDS(paste0(result$prefix, ".rds"))
  check("two rows, original columns, strict threshold and stored hashes", stopifnot(
    identical(names(r$rows), smcbvs_schema()), identical(r$rows$rule_id, c("hpm", "pip05")),
    all(r$rows$support == "5;500"), all(r$rows$k == 2L), length(r$pip) == 500L,
    r$pip["1"] == 0, r$pip["3"] == 0.5, identical(r$mpm, c(5L, 500L)),
    all(r$rows$x_sha256 == m$x_sha256), all(r$rows$y_sha256 == m$y_c100_sha256)))
  check("all native diagnostics retained under binding R-1", stopifnot(
    isTRUE(r$fit$flags$E2), isTRUE(r$fit$cut_group),
    identical(r$fit$fixture_nested_record$sentinel, "must survive unchanged"),
    identical(r$rows$role, c("primary", "S0")), all(is.na(r$rows$converged)), all(r$rows$diag_flag),
    all(r$rows$diag_codes == "final_check_E2;cut_group"),
    all(r$rows$adapter_mapping_status == "adopted"), all(r$rows$adapter_policy_id == "R-1-20261022"),
    all(r$rows$status == "ok"), all(is.na(r$rows$fold_seed)), all(is.na(r$rows$fold_sha256)),
    identical(r$input$fold_sha256, m$foldid_sha256), identical(r$case$fold_seed, spec$fold_seed),
    all(r$rows$method_seed == r$rows$data_seed + 4000000L),
    identical(r$schema_version, 2L), identical(r$adapter_version, "2.1-R1")))
  check("entire native fit retained verbatim", stopifnot(identical(r$fit,
    v3_fit(d$X, unname(d$Y[, "c100"]), spec$method_seed, allocation = r$allocation))))
  check("saved R-1 policy provenance agrees in rows and RDS", {
    expected_hash <- digest::digest(serialize(smcbvs_r1_policy(), NULL, version = 3),
      algo = "sha256", serialize = FALSE)
    stopifnot(identical(r$adapter_policy, smcbvs_r1_policy()),
      identical(r$adapter_policy_sha256, expected_hash), all(r$rows$adapter_policy_sha256 == expected_hash),
      all(r$rows$source_sha256 == r$code$source_sha256))
    historical <- as.list(r$rows[1L, , drop = FALSE])
    historical$adapter_mapping_status <- "unresolved"; historical$adapter_policy_id <- "I.7-unresolved"
    historical$adapter_policy_sha256 <- "historical"; historical$role <- NA_character_
    historical$diag_flag <- FALSE; historical$fold_seed <- spec$fold_seed
    historical$fold_sha256 <- m$foldid_sha256
    remapped <- smcbvs_rule_rows(r$fit, smcbvs_outputs(r$fit, 500L), historical, smcbvs_r1_policy())
    stopifnot(all(remapped$adapter_mapping_status == "adopted"),
      all(remapped$adapter_policy_id == "R-1-20261022"), all(remapped$adapter_policy_sha256 == expected_hash),
      identical(remapped$role, c("primary", "S0")), all(remapped$diag_flag),
      all(is.na(remapped$fold_seed)), all(is.na(remapped$fold_sha256)))
  })
  scoring <- c("tp", "fp", "fn", "exact", "error_type", sprintf("sel_a%02d", 1:14), sprintf("pip_a%02d", 1:14), "max_pip_null")
  check("truth-only columns unavailable", stopifnot(all(is.na(r$rows[scoring]))))
  check("native exact status is preserved", {
    er <- run("exact")
    stopifnot(all(er$rows$status == "ok"), all(er$rows$v3_status == "exact"))
  })
  check("checksummed resume", stopifnot(isTRUE(run("completed")$skipped)))
  check("changed allocation requires new immutable run ID", expect_immutable("allocation",
    run("completed", allocation = list(mem_gb = 16, hours = 24)), "allocation_sha256", result$prefix))
  check("copied foreign run is rejected without altering either unit", {
    foreign_dir <- file.path(out, "results", "copied_run", "p0500", spec$case_id)
    dir.create(foreign_dir, recursive = TRUE)
    foreign_prefix <- file.path(foreign_dir, "SMCBVS")
    suffix <- c(".rds", ".csv", ".sha256", ".done")
    stopifnot(all(file.copy(paste0(result$prefix, suffix), paste0(foreign_prefix, suffix))))
    expect_immutable("copied_run", run("completed", "copied_run"), "run_id", c(result$prefix, foreign_prefix))
  })
  check("aliased foreign run is rejected without altering original unit", {
    alias <- file.path(out, "results", "aliased_run")
    stopifnot(file.symlink(file.path(out, "results", "completed"), alias))
    alias_prefix <- file.path(alias, "p0500", spec$case_id, "SMCBVS")
    expect_immutable("aliased_run", run("completed", "aliased_run"), "run_id", c(result$prefix, alias_prefix))
  })
  check("fixed method identity rejects a valid checksummed foreign method", {
    foreign <- run("completed", "foreign_method")
    record <- readRDS(paste0(foreign$prefix, ".rds")); record$rows$method_id <- "OTHER"
    smcbvs_write_record(foreign$prefix, record)
    stopifnot(smcbvs_done_valid(foreign$prefix, list()))
    expect_immutable("foreign_method", run("completed", "foreign_method"), "method_id",
      c(result$prefix, foreign$prefix))
  })
  check("changed source requires new immutable run ID", {
    source_path <- file.path(core, "v3.R"); source_backup <- file.path(root, "fixture_v3.original.R")
    stopifnot(file.copy(source_path, source_backup)); source_hash <- smcbvs_file_hash(source_path)
    cat("\n# fixture source-identity mutation only\n", file = source_path, append = TRUE)
    stopifnot(smcbvs_file_hash(source_path) != source_hash)
    expect_immutable("source", run("completed"), "source_sha256", result$prefix)
    stopifnot(file.copy(source_backup, source_path, overwrite = TRUE), smcbvs_file_hash(source_path) == source_hash)
  })
  check("R-1 policy is fixed for production and development", {
    policy <- smcbvs_r1_policy()
    for (field in names(policy)) {
      changed <- policy; changed[[field]] <- NULL
      for (dev in c(FALSE, TRUE)) expect_error(smcbvs_validate_policy(changed, dev),
        "adapter policy is fixed by RULINGS_LEAD.md R-1; override refused")
      expect_error(run("completed", paste0("bad_policy_", field), policy = changed),
        "adapter policy is fixed by RULINGS_LEAD.md R-1; override refused")
      stopifnot(!dir.exists(file.path(out, "results", paste0("bad_policy_", field))))
    }
    changed <- policy; changed$status_map["completed"] <- "timeout"
    expect_error(smcbvs_validate_policy(changed),
      "adapter policy is fixed by RULINGS_LEAD.md R-1; override refused")
    stopifnot(isTRUE(run("completed", policy = policy)$skipped))
  })
  check("historical mapping checksum requires a new immutable run ID", {
    historical <- run("completed", "historical_policy")
    record <- readRDS(paste0(historical$prefix, ".rds"))
    record$rows$adapter_policy_sha256 <- paste(rep("0", 64L), collapse = "")
    smcbvs_write_record(historical$prefix, record)
    expect_immutable("historical_policy", run("completed", "historical_policy"),
      "adapter_policy_sha256", historical$prefix)
  })
  check("valid changed input and manifest cannot reuse prior unit", {
    input_backup <- file.path(root, "input.original.rds"); manifest_backup <- file.path(root, "manifest.original.csv")
    stopifnot(file.copy(input, input_backup), file.copy(manifest, manifest_backup))
    old_m <- m; original_input_hash <- smcbvs_file_hash(input); original_manifest_hash <- smcbvs_file_hash(manifest)
    changed <- d; changed$Y[1L, "c100"] <- changed$Y[1L, "c100"] + 1
    saveRDS(changed, input, compress = FALSE)
    m$file_sha256 <- smcbvs_file_hash(input); m$y_c100_sha256 <- smcbvs_f64_hash(changed$Y[, "c100"])
    write_manifest()
    # Prove the changed pair is independently valid, so failure must be resume identity.
    loaded <- smcbvs_load_input(spec, study)
    stopifnot(identical(loaded$y, unname(changed$Y[, "c100"])), m$file_sha256 != original_input_hash,
      loaded$manifest_sha256 != original_manifest_hash)
    expect_immutable("valid_changed_input", run("completed"),
      c("input_manifest_sha256", "inputs_sha256", "y_sha256"), result$prefix)
    stopifnot(file.copy(input_backup, input, overwrite = TRUE), file.copy(manifest_backup, manifest, overwrite = TRUE),
      smcbvs_file_hash(input) == original_input_hash, smcbvs_file_hash(manifest) == original_manifest_hash)
    m <- old_m
  })
  check("same-run resume survives all rejected identity requests", stopifnot(isTRUE(run("completed")$skipped)))
  writeLines("corrupt csv", paste0(result$prefix, ".csv"))
  check("corrupt output is recomputed", stopifnot(!isTRUE(run("completed")$skipped)))
  weak <- run("completed", "weak", "c050")
  check("paired scales share seed/X; y differs", stopifnot(weak$rows$method_seed == spec$method_seed,
    all(weak$rows$status == "ok"),
    all(weak$rows$x_sha256 == m$x_sha256), all(weak$rows$y_sha256 == m$y_c050_sha256),
    m$y_c100_sha256 != m$y_c050_sha256))
  check("c050 entire native fit retained with exact forwarded y", {
    record <- readRDS(paste0(weak$prefix, ".rds"))
    stopifnot(identical(record$fit,
      v3_fit(d$X, unname(d$Y[, "c050"]), spec$method_seed, allocation = record$allocation)))
  })
  # Mutate the existing saved fixture in memory; never invoke the production core.
  clean_fit <- r$fit
  clean_fit$flags <- list(); clean_fit$cut_group <- FALSE
  mapped <- function(fit = clean_fit, warnings = character(), messages = character()) {
    outputs <- if (fit$status == "adapter_error") smcbvs_outputs(clean_fit, 500L) else smcbvs_outputs(fit, 500L)
    smcbvs_rule_rows(fit, outputs, list(), smcbvs_r1_policy(), warnings, messages)
  }
  for (native in smcbvs_native_statuses) {
    check(paste("R-1 status and convergence", native), {
      fit <- clean_fit; fit$status <- native
      rows <- mapped(fit)
      failed <- !native %in% c("exact", "completed")
      stopifnot(all(rows$status == if (failed) "failed" else "ok"),
        identical(rows$role, c("primary", "S0")), all(is.na(rows$converged)),
        all(!rows$diag_flag), all(rows$v3_status == native),
        if (failed) all(is.na(rows$support) & is.na(rows$k)) else all(rows$support == "5;500"))
      conditioned <- mapped(fit, warnings = "warning\n", messages = "message\n\n")
      stopifnot(all(conditioned$status == if (failed) "failed" else "warning"),
        all(conditioned$n_warnings == 2L), identical(rows$diag_flag, conditioned$diag_flag),
        identical(rows$support, conditioned$support))
    })
  }
  quality <- c(paste0("final_check_E", 1:3), "low_empirical_ESS", "grid_unconverged", "local_limit")
  for (code in quality) {
    check(paste("individual numerical diagnostic is independent of status", code), {
      fit <- clean_fit
      if (startsWith(code, "final_check_")) {
        fit$flags$checks_passed_final <- FALSE
        fit$flags[[sub("final_check_", "", code, fixed = TRUE)]] <- TRUE
      } else fit$flags[[code]] <- TRUE
      for (native in c("completed", "exact", "numerical_failure")) {
        fit$status <- native; rows <- mapped(fit)
        expected_codes <- if (native == "exact") paste(code, "exact_branch", sep = ";") else code
        stopifnot(all(rows$diag_flag), all(rows$diag_codes == expected_codes),
          all(rows$status == if (native == "numerical_failure") "failed" else "ok"),
          all(is.na(rows$converged)))
      }
    })
  }
  check("failed final summary alone flags without inventing a code", {
    fit <- clean_fit; fit$flags$checks_passed_final <- FALSE
    rows <- mapped(fit)
    stopifnot(all(rows$diag_flag), all(rows$diag_codes == ""), all(rows$status == "ok"))
  })
  check("absent and NA checks do not fail; calibration E flags are not final E checks", {
    fit <- clean_fit
    fit$flags <- list(E1 = TRUE, E2 = NA, E3 = FALSE, checks_passed_final = NA,
      low_empirical_ESS = NA, grid_unconverged = FALSE, local_limit = NA,
      checks_passed_calibration = FALSE, escalation_blocked = "resource_limit",
      triggers_fired = c("E1", "E3"))
    rows <- mapped(fit)
    stopifnot(all(!rows$diag_flag), all(rows$diag_codes == ""), all(rows$status == "ok"))
  })
  informational <- c("escalated", "cut_group", "near_tie_truncated", "forced_pilot_steps",
    "exact_branch", "local_certified_false", "global_certified")
  for (code in informational) {
    check(paste("informational code never sets diagnostic flag or changes selection", code), {
      fit <- clean_fit
      if (code == "local_certified_false") fit$local_certified <- FALSE else
        if (code == "forced_pilot_steps") fit$flags$forced_pilot_steps <- 3 else
          fit[[code]] <- TRUE
      for (native in c("completed", "resource_limit")) {
        fit$status <- native; rows <- mapped(fit)
        stopifnot(all(!rows$diag_flag), all(rows$diag_codes == code),
          all(rows$status == if (native == "completed") "ok" else "failed"),
          if (native == "completed") all(rows$support == "5;500") else all(rows$support_audit == "5;500"))
      }
    })
  }
  check("native forced-pilot count zero and positive numeric/integer", {
    for (count in list(0, 0L, 2, 2L, NA_real_)) {
      fit <- clean_fit; fit$flags$forced_pilot_steps <- count
      rows <- mapped(fit)
      stopifnot(all(!rows$diag_flag), all(rows$status == "ok"),
        all(rows$diag_codes == if (isTRUE(count > 0)) "forced_pilot_steps" else ""),
        identical(fit$flags$forced_pilot_steps, count))
    }
  })
  check("exact branch without SMC flags has only informational codes", {
    fit <- clean_fit; fit$status <- "exact"; fit$branch_run <- "exact"
    fit$local_certified <- TRUE; fit$global_certified <- TRUE
    rows <- mapped(fit)
    stopifnot(all(!rows$diag_flag), all(rows$status == "ok"),
      all(rows$diag_codes == "exact_branch;global_certified"))
    fit$status <- "resource_limit"
    rows <- mapped(fit)
    stopifnot(all(!rows$diag_flag), all(rows$status == "failed"),
      all(rows$diag_codes == "exact_branch;global_certified"))
  })
  check("failed nested calibration flags retained and mapped without final E inference", {
    fit <- clean_fit; fit$status <- "schedule_limit"
    fit$flags <- NULL
    fit$calibration <- list(flags = list(grid_unconverged = TRUE, forced_pilot_steps = 4,
      escalated = TRUE, checks_passed_calibration = FALSE,
      triggers_by_tier = list(list(E1 = TRUE, E2 = TRUE, E3 = TRUE))))
    before <- serialize(fit, NULL, version = 3)
    rows <- mapped(fit)
    stopifnot(all(rows$diag_flag), all(rows$status == "failed"),
      all(rows$diag_codes == "grid_unconverged;escalated;forced_pilot_steps"),
      identical(before, serialize(fit, NULL, version = 3)))
  })
  check("actual failed final-local-search shape retains local_limit diagnostic", {
    fit <- clean_fit; fit$status <- "resource_limit"; fit$branch_run <- "smc"
    fit$estimates_available <- FALSE; fit$pip_primary <- NULL; fit$mpm <- NULL
    fit$partial_results <- TRUE; fit$local_certified <- FALSE; fit$global_certified <- FALSE
    fit$flags <- list(forced_pilot_steps = 0, grid_unconverged = FALSE)
    fit$local_search <- list(phase = "final", local_limit = TRUE,
      local_certified = FALSE, termination = "move_limit", returned = c(5L, 500L))
    before <- serialize(fit, NULL, version = 3)
    rows <- mapped(fit)
    stopifnot(is.null(fit$local_limit), is.null(fit$flags$local_limit),
      all(rows$diag_flag), all(rows$diag_codes == "local_limit;local_certified_false"),
      all(rows$status == "failed"), all(is.na(rows$support)), all(is.na(rows$k)),
      rows$support_audit[1L] == "5;500", is.na(rows$support_audit[2L]),
      identical(before, serialize(fit, NULL, version = 3)))
  })
  for (where in c("triggers_by_tier", "tier_triggers", "pilot_search", "iteration_search", "partial_operation")) {
    check(paste("calibration local_limit anywhere is a named quality failure", where), {
      fit <- clean_fit; fit$flags$local_limit <- FALSE
      fit$local_limit <- FALSE; fit$local_search <- list(local_limit = FALSE)
      fit$calibration <- switch(where,
        triggers_by_tier = list(flags = list(triggers_by_tier = list(list(local_limit = TRUE)))),
        tier_triggers = list(tiers = list(list(triggers = list(local_limit = TRUE)))),
        pilot_search = list(tiers = list(list(pilot = list(local_search = list(local_limit = TRUE))))),
        iteration_search = list(tiers = list(list(iterations = list(list(local_search = list(local_limit = TRUE)))))),
        partial_operation = list(tiers = list(list(partial_operation = list(local_search = list(local_limit = TRUE))))))
      for (native in c("completed", "resource_limit", "schedule_limit")) {
        fit$status <- native; before <- serialize(fit, NULL, version = 3); rows <- mapped(fit)
        stopifnot(all(rows$diag_flag), all(rows$diag_codes == "local_limit"),
          all(rows$status == if (native == "completed") "ok" else "failed"),
          identical(before, serialize(fit, NULL, version = 3)))
      }
    })
  }
  check("each condition alone sets warning; neither diagnostics nor native text do", {
    stopifnot(all(mapped(warnings = "one warning\n")$status == "warning"),
      all(mapped(messages = "one message\n")$status == "warning"))
    fit <- clean_fit; fit$message <- "native explanatory text, not an R condition"
    stopifnot(all(mapped(fit)$status == "ok"))
  })
  check("failed provided PIPs and both supports survive as audit", {
    for (native in c("schedule_limit", "numerical_failure", "resource_limit", "invalid_input",
                     "y_constant", "no_predictors")) {
      fit <- clean_fit; fit$status <- native; fit$estimates_available <- FALSE
      outputs <- smcbvs_outputs(fit, 500L); rows <- mapped(fit)
      stopifnot(identical(outputs$pip, r$pip), identical(outputs$mpm, r$mpm),
        !outputs$estimates_available, all(rows$status == "failed"),
        all(rows$support_audit == "5;500"), all(is.na(rows$support)), all(is.na(rows$k)))
      fit$mpm <- NULL
      stopifnot(identical(smcbvs_outputs(fit, 500L)$mpm, r$mpm))
    }
  })
  # Wrap the copied existing core fixture only, for end-to-end condition/audit persistence.
  check("verbatim warning/message capture and failed PIP audit in saved CSV/RDS", {
    wrapped_backup <- file.path(root, "fixture_before_conditions.R")
    stopifnot(file.copy(file.path(core, "v3.R"), wrapped_backup))
    wrapper <- c("", "fixture_base_fit <- v3_fit", "v3_fit <- function(X, y, seed, allocation) {",
      '  warning(simpleWarning("first warning\\n\\n"))',
      '  warning(simpleWarning("second warning | literal separator"))',
      '  message(simpleMessage("first message\\n\\n"))',
      '  message(simpleMessage("second message\\n"))',
      '  out <- fixture_base_fit(X, y, seed, allocation)',
      '  if (out$status == "resource_limit") {',
      '    out$pip_primary <- setNames(rep(0.1, 499L), as.character(2:500))',
      '    out$pip_primary[c("5", "500")] <- 0.75; out$pip_primary["3"] <- 0.5',
      '    out$mpm <- c(5L, 500L)',
      '    out$calibration <- list(flags = list(forced_pilot_steps = 2), nested_sentinel = "retain")',
      '  }', '  out$flags$forced_pilot_steps <- 2', '  out', '}')
    cat(paste(wrapper, collapse = "\n"), "\n", file = file.path(core, "v3.R"), append = TRUE)
    for (mode in c("completed", "exact", "resource_limit")) {
      rr <- run(mode, paste0("conditions_", mode)); record <- readRDS(paste0(rr$prefix, ".rds"))
      csv <- utils::read.csv(paste0(rr$prefix, ".csv"), stringsAsFactors = FALSE, colClasses = "character")
      stopifnot(identical(record$warnings, c("first warning\n\n", "second warning | literal separator")),
        identical(record$messages, c("first message\n\n", "second message\n")),
        all(rr$rows$n_warnings == 4L), all(csv$warnings == rr$rows$warnings), all(csv$messages == rr$rows$messages),
        all(rr$rows$status == if (mode == "resource_limit") "failed" else "warning"),
        identical(record$pip, r$pip), identical(record$pip_primary_original, r$pip),
        identical(record$fit$flags$forced_pilot_steps, 2), all(rr$rows$diag_flag),
        all(is.na(rr$rows$converged)), all(is.na(rr$rows$fold_seed)), all(is.na(rr$rows$fold_sha256)))
      if (mode == "resource_limit") stopifnot(all(rr$rows$support_audit == "5;500"),
        all(is.na(rr$rows$support)), all(is.na(rr$rows$k)),
        identical(record$fit$calibration$nested_sentinel, "retain"))
      stopifnot(isTRUE(run(mode, paste0("conditions_", mode))$skipped))
    }
    stopifnot(file.copy(wrapped_backup, file.path(core, "v3.R"), overwrite = TRUE),
      isTRUE(run("completed")$skipped))
  })
  for (mode in c("schedule_limit", "numerical_failure", "resource_limit", "invalid_input")) {
    rr <- run(mode); record <- readRDS(paste0(rr$prefix, ".rds"))
    check(paste("failed support audit", mode), stopifnot(all(rr$rows$status == "failed"),
      all(is.na(rr$rows$support)), all(is.na(rr$rows$k)), rr$rows$support_audit[1L] == "5;500",
      identical(record$fit$status, mode), all(is.na(record$pip))))
  }
  for (mode in c("y_constant", "no_predictors")) {
    rr <- run(mode)
    check(paste("unexpected study native status fails both rules", mode), stopifnot(
      all(rr$rows$status == "failed"), all(rr$rows$v3_status == mode),
      all(is.na(rr$rows$support)), all(is.na(rr$rows$k)), rr$rows$support_audit[1L] == "",
      is.na(rr$rows$support_audit[2L]), all(is.na(rr$rows$converged)), all(rr$rows$diag_flag)))
  }
  for (mode in c("throw", "malformed", "bad_pip", "bad_mpm")) {
    rr <- run(mode)
    check(paste("adapter exception/malformed output", mode), stopifnot(all(rr$rows$v3_status == "adapter_error"),
      all(rr$rows$status == "failed"), file.exists(paste0(rr$prefix, ".done"))))
  }
  check("v2.1 F3: R-level OOM is a recorded failed unit", {
    rr <- run("oom"); record <- readRDS(paste0(rr$prefix, ".rds"))
    stopifnot(file.exists(paste0(rr$prefix, ".done")), all(rr$rows$status == "failed"),
      all(rr$rows$v3_status == "adapter_error"), is.null(record$fit),
      identical(record$error, "cannot allocate vector of size fixture"),
      all(rr$rows$error == "cannot allocate vector of size fixture"),
      all(is.na(rr$rows$support)), all(is.na(rr$rows$k)), isTRUE(run("oom")$skipped))
  })
  check("v2.1 F1: aggregate source hash is independent of the collation locale", {
    old <- Sys.getlocale("LC_COLLATE"); on.exit(Sys.setlocale("LC_COLLATE", old), add = TRUE)
    hashes <- character()
    for (loc in c("C", "en_US.UTF-8", "en_US.utf8", "C.UTF-8")) {
      if (identical(suppressWarnings(Sys.setlocale("LC_COLLATE", loc)), "")) next
      hashes[loc] <- smcbvs_source_record(core)$source_sha256
    }
    Sys.setlocale("LC_COLLATE", old)
    # The check has power only if some tested locale collates the hashed paths differently from C.
    paths <- c("core/v3.R", "core/v3_calib.R", "study/README.md", "study/adapter.R", "study/SCHEMA.md")
    differs <- FALSE
    for (loc in setdiff(names(hashes), "C")) {
      Sys.setlocale("LC_COLLATE", loc)
      differs <- differs || !identical(sort(paths), sort(paths, method = "radix"))
    }
    Sys.setlocale("LC_COLLATE", old)
    stopifnot("C" %in% names(hashes), length(hashes) >= 2L, differs, length(unique(hashes)) == 1L)
    cat("locales tested:", paste(names(hashes), collapse = ","), "\n")
  })
  m$x_sha256 <- paste(rep("0", 64), collapse = ""); write_manifest()
  check("manifest array mismatch stops before fit", {
    expect_error(run("throw", "bad_manifest"), "stored-array hash mismatch: x_sha256")
    stopifnot(!dir.exists(file.path(out, "results", "bad_manifest")))
  })
  m$x_sha256 <- smcbvs_f64_hash(X); write_manifest()
  check("truth and holdout path guards", {
    for (part in c("truth", "holdout")) {
      bad <- file.path(root, part, "x")
      expect_error(smcbvs_safe_path(bad, FALSE), paste0("refusing truth/holdout path: ", bad))
      stopifnot(!dir.exists(dirname(bad)))
    }
  })
  expect_path_refusal <- function(label, bad, resolved) {
    before <- unit_hashes(result$prefix)
    input_before <- vapply(c(input, manifest), smcbvs_file_hash, "")
    expected <- paste0("output must be outside the input/frozen study: ", resolved)
    expect_error(smcbvs_output_root(bad, study), expected)
    after <- unit_hashes(result$prefix)
    stopifnot(identical(before, after), identical(input_before, vapply(c(input, manifest), smcbvs_file_hash, "")))
    rejection_evidence[[label]] <<- list(error = expected, before = before, after = after,
      input_hashes = input_before)
  }
  check("refuse output within input tree before mkdir", {
    bad <- file.path(study, "never_create")
    expect_path_refusal("direct_nonexistent", bad, bad)
    stopifnot(!dir.exists(bad))
  })
  check("existing symlink ancestor into input study is rejected", {
    target <- file.path(study, "existing_output_trap"); dir.create(target)
    alias <- file.path(root, "study_alias"); stopifnot(file.symlink(study, alias))
    before <- list.files(target, all.files = TRUE, no.. = TRUE)
    expect_path_refusal("symlink_existing", file.path(alias, basename(target)), target)
    stopifnot(identical(before, list.files(target, all.files = TRUE, no.. = TRUE)))
  })
  check("nonexistent suffix under symlink ancestor is rejected before mkdir", {
    bad <- file.path(root, "study_alias", "never_created_parent", "child")
    target <- file.path(study, "never_created_parent", "child")
    expect_path_refusal("symlink_nonexistent", bad, target)
    stopifnot(!dir.exists(dirname(target)), !dir.exists(target))
  })
  check("run-directory symlink escaping outroot is rejected before mkdir", {
    private_target <- file.path(root, "private_outside_outputs"); dir.create(private_target)
    alias <- file.path(out, "results", "escaped_run"); stopifnot(file.symlink(private_target, alias))
    before <- unit_hashes(result$prefix)
    expect_error(run("completed", "escaped_run"), "output directory symlink escapes outroot")
    stopifnot(!dir.exists(file.path(private_target, "p0500")), identical(before, unit_hashes(result$prefix)))
  })
  if (is.na(old_fixture)) Sys.unsetenv("SMCBVS_ADAPTER_FIXTURE") else Sys.setenv(SMCBVS_ADAPTER_FIXTURE = old_fixture)
  if (is.na(old_scale)) Sys.unsetenv("SMCBVS_ADAPTER_EXPECT_SCALE") else Sys.setenv(SMCBVS_ADAPTER_EXPECT_SCALE = old_scale)
  saveRDS(list(status = "passed", checks = tests, rejection_evidence = rejection_evidence,
    started_utc = started, finished_utc = smcbvs_utc(),
    source = smcbvs_source_record(core), session_info = utils::capture.output(utils::sessionInfo())),
    file.path(root, "adapter_test_evidence.rds"), version = 3)
  writeLines(c(paste("PASS", length(tests)), tests,
    "Immutable-rejection errors and SHA-256 before/after:",
    utils::capture.output(dput(rejection_evidence))), file.path(root, "adapter_test_evidence.txt"))
  cat("PASS adapter fixture contract", length(tests), "checks\n")
}
