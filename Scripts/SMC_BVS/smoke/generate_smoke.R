#!/usr/bin/env Rscript
# One dev dataset using the actual frozen benchmark generator, not reimplemented numerics.
# Usage: Rscript generate_smoke.R BENCHMARK_GEN_DEV_R DEV_INPUT_ROOT P [SCENARIO]
# Does not call the generator's main(), read truth files, or save its returned truth object.
generate_smcbvs_smoke <- function(generator, root, p, scenario = 1L) {
  if (!p %in% c(500L, 1000L) || !scenario %in% 1:6) stop("only p500/p1000 and S1..S6 dev cases")
  generator <- normalizePath(generator, winslash = "/", mustWork = TRUE)
  if (grepl("(^|/)(truth|holdout)(/|$)", tolower(generator))) stop("invalid generator path")
  if (!requireNamespace("digest", quietly = TRUE)) stop("digest is required")
  expected_generator_sha256 <- "36b03c8c8bad0ca30e62fc896f81c8d630078f6567b9448aa493d053e2b1a8c6"
  if (!identical(digest::digest(file = generator, algo = "sha256"), expected_generator_sha256))
    stop("generator differs from the inspected frozen benchmark source")
  # This script lives in smoke/, so load adapter helpers without loading the production core.
  own <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1L])
  own_dir <- dirname(normalizePath(own, mustWork = TRUE))
  source(file.path(own_dir, "..", "code", "study", "adapter.R"), local = FALSE)
  root <- smcbvs_output_root(root, forbidden_root = "/projects/ml75/fb31/BVS/bench20261019")
  # Idempotence is verified from existing files, never by regenerating into an occupied root.
  id <- sprintf("dev_p%04d_S%d_r001", p, scenario)
  manifest <- file.path(root, "manifests", "dev_inputs_manifest.csv")
  if (file.exists(manifest)) {
    m <- utils::read.csv(manifest, stringsAsFactors = FALSE)
    expected_generator <- file.path(root, "generator.sha256")
    if (!file.exists(expected_generator) || !identical(readLines(expected_generator, warn = FALSE)[1L], smcbvs_file_hash(generator)))
      stop("existing smoke root has different/unknown generator provenance")
    spec <- smcbvs_case_spec(id, "c100", development = TRUE)
    smcbvs_load_input(spec, root, manifest)
    smcbvs_load_input(smcbvs_case_spec(id, "c050", TRUE), root, manifest)
    if (nrow(m) != 1L) stop("smoke root must contain exactly one dev case")
    cat("verified existing", id, "\n"); return(invisible(id))
  }
  if (length(list.files(root, all.files = TRUE, no.. = TRUE))) stop("new smoke root must be empty")
  env <- new.env(parent = globalenv())
  sys.source(generator, envir = env)
  if (!is.function(env$generate_dev_dataset) || !identical(env$N, 200L) ||
      !identical(env$DEV_DATA_BASE, c(`500` = 2410000L, `1000` = 2510000L)))
    stop("unexpected benchmark dev generator contract")
  started <- smcbvs_utc()
  d <- env$generate_dev_dataset(p, scenario, 1L)$inputs
  spec <- smcbvs_case_spec(id, "c100", development = TRUE)
  stopifnot(identical(d$dataset_id, id), identical(d$data_seed, spec$data_seed),
    identical(d$method_seed, spec$method_seed), d$n == 200L)
  di <- file.path(root, "inputs", sprintf("p%04d", p)); dm <- file.path(root, "manifests")
  dir.create(di, recursive = TRUE, showWarnings = FALSE); dir.create(dm, recursive = TRUE, showWarnings = FALSE)
  input <- file.path(di, paste0(id, ".rds"))
  smcbvs_atomic(input, function(f) saveRDS(d, f, compress = FALSE))
  row <- data.frame(dataset_id = id, p = p, scenario = scenario, replicate = 1L,
    data_seed = d$data_seed, fold_seed = d$fold_seed, method_seed = d$method_seed,
    file_sha256 = smcbvs_file_hash(input), x_sha256 = smcbvs_f64_hash(d$X),
    foldid_sha256 = smcbvs_f64_hash(d$foldid), stringsAsFactors = FALSE)
  for (key in names(d$scales)) row[[paste0("y_", key, "_sha256")]] <- smcbvs_f64_hash(d$Y[, key])
  smcbvs_atomic(manifest, function(f) utils::write.csv(row, f, row.names = FALSE))
  writeLines(smcbvs_file_hash(generator), file.path(root, "generator.sha256"))
  saveRDS(list(generator = generator, generator_sha256 = smcbvs_file_hash(generator),
    source = readLines(generator, warn = FALSE), case = spec, started_utc = started, finished_utc = smcbvs_utc(),
    environment = utils::capture.output(utils::sessionInfo()), command = commandArgs(FALSE),
    input_sha256 = smcbvs_file_hash(input), manifest_sha256 = smcbvs_file_hash(manifest)),
    file.path(root, "generation_record.rds"), version = 3)
  Sys.chmod(c(input, manifest), "0444")
  cat("generated inputs only:", id, "\n")
  invisible(id)
}
if (sys.nframe() == 0L) {
  a <- commandArgs(trailingOnly = TRUE)
  if (!length(a) %in% c(3L, 4L)) stop("usage: generate_smoke.R GENERATOR ROOT P [SCENARIO]")
  generate_smcbvs_smoke(a[1L], a[2L], as.integer(a[3L]), if (length(a) == 4L) as.integer(a[4L]) else 1L)
}
