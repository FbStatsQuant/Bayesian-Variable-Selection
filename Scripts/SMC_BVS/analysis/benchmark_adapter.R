# Adapter only. The benchmark files are sourced without edits; their scoring arithmetic is used.
args <- commandArgs(TRUE)
mode <- args[1]; code <- args[2]; out <- args[3]
source(file.path(code, "registry.R"))
source(file.path(code, "score.R"))
source(file.path(code, "aggregate.R"))
dir.create(out, recursive = TRUE, showWarnings = FALSE)
if (mode == "registry") {
  rows <- list()
  for (m in names(REGISTRY)) {
    reg <- rules_of(m, TRUE)
    for (j in seq_along(reg$rules)) for (sk in c("c100", "c050"))
      rows[[length(rows)+1]] <- data.frame(method_id=m, rule_id=reg$rules[j],
        role=reg$roles[j], scale_key=sk, label=rule_label(m, reg$rules[j], sk))
  }
  write_table(do.call(rbind, rows), file.path(out, "registry.csv"))
} else if (mode == "reproduce") {
  # Only copied scoring outputs in out are mutated by aggregate_run, never the source directory.
  aggregate_run(out)
} else if (mode == "combine") {
  source(file.path(code, "combine.R"))
  combine_runs(out, args[4:length(args)])
} else if (mode == "compare") {
  # R type inference and identical() preserve the declared published cell types.
  actual <- args[4]; expected <- args[5]; keys <- strsplit(args[6], ",", fixed=TRUE)[[1]]
  a <- utils::read.csv(actual, check.names=FALSE, stringsAsFactors=FALSE)
  b <- utils::read.csv(expected, check.names=FALSE, stringsAsFactors=FALSE)
  if (!all(keys %in% names(a)) || !all(keys %in% names(b))) stop("comparison key absent")
  if (anyDuplicated(a[,keys,drop=FALSE]) || anyDuplicated(b[,keys,drop=FALSE])) stop("duplicate table key")
  ordered <- function(x) {
    if (nrow(x)) x <- x[do.call(order, c(x[,keys,drop=FALSE], list(na.last=TRUE, method="radix"))),,drop=FALSE]
    rownames(x) <- NULL
    x
  }
  cell_equal <- identical(ordered(a), ordered(b))
  byte_equal <- identical(file_sha256(actual), file_sha256(expected))
  write_table(data.frame(actual=actual, expected=expected, sort_keys=paste(keys, collapse=","),
    cell_and_type_equal=cell_equal, byte_equal=byte_equal), file.path(out, "comparison.csv"))
  if (!cell_equal) stop("published table cells/types differ: ", expected)
} else if (mode == "validate_native") {
  # Real dev smoke integration: native/schema validation only, never truth or scoring.
  script <- sub("^--file=", "", grep("^--file=",commandArgs(FALSE),value=TRUE)[1])
  source(file.path(dirname(normalizePath(script)),"r1_contract.R"))
  rds <- args[4]; csv <- args[5]; profile <- args[6]
  problems <- check_sidecar(dirname(csv),"SMCBVS")
  if(length(problems)) stop(paste(problems,collapse=";"))
  rows <- read_rule_csv(csv);record <- readRDS(rds);p <- unique(as.integer(rows$p))
  if(length(p)!=1 || !all(BASE_COLUMNS %in% names(rows))) stop("actual smoke base schema invalid")
  if(profile=="r1") r1_validate(rows,record)
  integrity <- native_validate(rows,record,p,require_bound_label=profile=="r1")
  legacy <- if(profile=="legacy") tryCatch({r1_validate(rows,record);NA_character_},error=function(e) conditionMessage(e)) else NULL
  jsonlite::write_json(list(profile=profile,p=p,native_status=integrity$native_status,
    stage_rows=nrow(record$fit$stage_table),native_hpm_k=length(integrity$hpm),native_mpm_k=length(integrity$mpm),
    original_bound_label=record$fit$bound_label,annotation=record$native_annotations,
    legacy_r1_rejection=legacy,truth_or_scoring_performed=FALSE),file.path(out,"native_validation.json"),
    auto_unbox=TRUE,pretty=TRUE,null="null",na="null")
} else if (mode == "smc") {
  results <- args[4]; manifest_path <- args[5]; truth_dir <- args[6]
  truth_manifest_path <- args[7]; sk <- args[8]
  script <- sub("^--file=", "", grep("^--file=",commandArgs(FALSE),value=TRUE)[1])
  source(file.path(dirname(normalizePath(script)),"r1_contract.R"))
  manifest <- read_rule_csv(manifest_path)
  tm <- read_rule_csv(truth_manifest_path)
  all_scored <- list(); signals <- list(); native <- list()
  for (ci in seq_len(nrow(manifest))) {
    ca <- manifest[ci, ]; p <- as.integer(ca$p)
    case_id <- paste0(ca$dataset_id, "_", sk)
    cd <- file.path(results, sprintf("p%04d", p), case_id)
    path <- file.path(cd, "SMCBVS.csv")
    if (!file.exists(path)) next  # missing rows remain in the external expected-case denominator
    required <- file.path(cd, paste0("SMCBVS", c(".rds", ".sha256", ".done")))
    if (!all(file.exists(required))) stop("incomplete SMC bundle: ", cd)
    problems <- check_sidecar(cd, "SMCBVS")
    if (length(problems)) stop(paste(problems, collapse=";"), ": ", cd)
    rows <- read_rule_csv(path)
    if (!all(BASE_COLUMNS %in% names(rows))) stop("missing IV.1.2 columns: ", path)
    if (!all(c("v3_status", "v3_flags_json", "adapter_mapping_status", "adapter_policy_id", "adapter_policy_sha256") %in% names(rows)))
      stop("A native status/flags/policy fields absent")
    if (anyNA(rows$adapter_mapping_status) || any(rows$adapter_mapping_status != "adopted") ||
        anyNA(rows$adapter_policy_id) || any(!nzchar(rows$adapter_policy_id)) ||
        anyNA(rows$adapter_policy_sha256) || any(!grepl("^[0-9a-f]{64}$",rows$adapter_policy_sha256)))
      stop("unresolved or unadopted adapter policy")
    if (any(!vapply(rows$v3_flags_json, jsonlite::validate, TRUE))) stop("invalid native flags JSON")
    if (!nrow(rows) || anyDuplicated(rows$rule_id) || !all(rows$rule_id %in% c("hpm", "pip05")))
      stop("SMC bundle has empty/duplicate/unregistered rules: ", path)
    equal <- function(column, value) all(!is.na(rows[[column]]) & rows[[column]] == value)
    number_equal <- function(column, value) {
      x <- suppressWarnings(as.numeric(rows[[column]]))
      all(!is.na(x) & x == as.numeric(value))
    }
    checks <- c(equal("case_id", case_id), equal("dataset_id", ca$dataset_id),
      equal("method_id", "SMCBVS"), equal("run_id", basename(results)), equal("regime", "H"),
      equal("scale_key", sk), number_equal("scale", as.numeric(sub("c", "", sk))/100),
      number_equal("p", p), number_equal("scenario", ca$scenario), number_equal("replicate", ca$replicate),
      equal("x_sha256", ca$x_sha256), equal("y_sha256", ca[[paste0("y_",sk,"_sha256")]]),
      equal("inputs_sha256", ca$file_sha256), all(is.na(rows$fold_sha256)),
      number_equal("data_seed", ca$data_seed), all(is.na(rows$fold_seed)),
      number_equal("method_seed", as.numeric(ca$data_seed)+4000000))
    if (!all(checks)) stop("SMC provenance/design/seed/hash mismatch: ", path)
    if (!all(rows$status %in% STATUS_VALUES)) stop("invalid status: ", path)
    if (any(!is.na(rows$diag_flag) & !rows$diag_flag %in% c("TRUE", "FALSE"))) stop("invalid diag_flag: ", path)
    if (!all(grepl("^[0-9a-f]{64}$", rows$source_sha256))) stop("source hash missing: ", path)
    for (cc in TRUTH_COLUMNS) if (any(!is.na(rows[[cc]]) & rows[[cc]] != ""))
      stop("prefilled truth column ", cc, ": ", path)
    for (i in seq_len(nrow(rows))) {
      if (rows$status[i] %in% FAILED_STATUSES) {
        if (!is.na(rows$support[i]) || !is.na(rows$k[i])) stop("failed row with support/k")
      } else {
        z <- parse_support(rows$support[i], p)
        k <- suppressWarnings(as.numeric(rows$k[i]))
        if (!is.na(z$problem) || is.null(z$idx) || is.na(k) || k != length(z$idx))
          stop("invalid support/k: ", path)
      }
    }
    pip <- NULL
    record <- readRDS(file.path(cd, "SMCBVS.rds"))
    if (length(args)>=9 && args[9]=="assessment" &&
        (isTRUE(record$adapter_policy$mock_only) || any(rows$study=="SYNTHETIC_NOT_PRODUCTION")))
      stop("assessment refuses D schema mock policy/output")
    if (is.null(record$pip) || length(record$pip) != p) stop("A RDS top-level pip absent or wrong length")
    if (any(rows$adapter_policy_sha256 != record$adapter_policy_sha256)) stop("RDS policy identity differs")
    ri <- match(rows$rule_id, record$rows$rule_id)
    if (anyNA(ri) || anyDuplicated(record$rows$rule_id)) stop("RDS rule rows absent or duplicated")
    for (nm in c("status","role","converged","diag_flag","k","support","support_audit",
                 "v3_status","v3_flags_json","adapter_mapping_status","adapter_policy_id","adapter_policy_sha256")) {
      if (!identical(as.character(rows[[nm]]),as.character(record$rows[[nm]][ri]))) stop("RDS/CSV rows differ: ",nm)
    }
    integrity <- native_validate(rows,record,p)
    r1_validate(rows,record)
    if (any(!rows$status %in% FAILED_STATUSES)) {
      # Current A adapter exposes primary original-index PIPs at top-level pip.
      if (isTRUE(record$estimates_available)) pip <- read_pip(file.path(cd, "SMCBVS.rds"))
      if (!is.null(pip) && (length(pip) != p || any(!is.finite(pip)) || any(pip<0 | pip>1)))
        stop("SMCBVS RDS must expose the sole primary RB PIP as pip or fit$pip: ", cd)
      i <- which(rows$rule_id == "pip05" & !rows$status %in% FAILED_STATUSES)
      if (length(i) && is.null(pip)) stop("successful pip05 requires available primary PIP")
      if (length(i) && !identical(rows$support[i], paste(which(pip>0.5), collapse=";")))
        stop("pip05 differs from primary RDS PIP: ", cd)
    }
    # All native/derivation/mapping checks complete BEFORE any truth is opened.
    tr <- load_truth(truth_dir, tm, ca$dataset_id, p)
    native[[length(native)+1]] <- rows
    all_scored[[length(all_scored)+1]] <- score_fit_rows(rows, tr$active, pip, p)
    one <- data.frame(p=p, signal=sprintf("a%02d", 1:14), index=tr$active, beta=tr$beta[tr$active])
    old <- signals[[as.character(p)]]
    if (!is.null(old) && !identical(old, one)) stop("truth differs across datasets")
    signals[[as.character(p)]] <- one
  }
  if (length(all_scored)) {
    # Native extras are preserved, including v3 status and flags.
    cols <- unique(unlist(lapply(all_scored, names)))
    all_scored <- lapply(all_scored, function(x) {
      for (cc in setdiff(cols, names(x))) x[[cc]] <- NA_character_
      x[, cols, drop=FALSE]
    })
    write_table(do.call(rbind, all_scored), file.path(out, "scored_rows.csv"))
    write_table(do.call(rbind, signals), file.path(out, "truth_signals.csv"))
  } else {
    write_table(as.data.frame(setNames(replicate(length(BASE_COLUMNS), character(), simplify=FALSE), BASE_COLUMNS)),
      file.path(out, "scored_rows.csv"))
  }
} else stop("unknown adapter mode")
writeLines(c(capture.output(sessionInfo()), paste("UTC", format(Sys.time(), tz="UTC", usetz=TRUE))),
  file.path(out, "R_environment.txt"))
