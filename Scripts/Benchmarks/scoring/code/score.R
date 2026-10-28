# score.R: the scoring step of master §IV.1.2 for one run (thread S, 2026-10-19).
#
# Reads every rule-row CSV under results/<run_id>/, checks the .sha256 sidecars, the coverage and
# the provenance of every row, joins the truth, and fills the truth columns
#   tp, fp, fn, exact, error_type, sel_a01..sel_a14, pip_a01..pip_a14, max_pip_null.
# It is the only step that reads truth. It never modifies the results tree.
#
# Usage (inside a SLURM job):
#   Rscript --vanilla score.R --results <STUDY>/results/<run_id> --manifest <inputs_manifest.csv> \
#     --truth <truth dir with p0500/, p1000/> --truth-manifest <truth_manifest.csv> --out <dir> \
#     [--methods F4,F4_SCAD] [--expect prod|dev] [--scale c100] [--p 500,1000]
#
# Outputs in --out: scored_rows.csv (the §IV.1.2 columns, truth columns filled), coverage.csv
# (one row per expected (case, method_id)), problems.csv (every failed check), files_extra.csv
# (files that belong to no expected (case, method_id)), score_log.txt.

find_code_dir <- function() {
  a <- grep("^--file=", commandArgs(FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
}
if (!exists("REGISTRY")) source(file.path(find_code_dir(), "registry.R"))

# ---------------------------------------------------------------------------------------------
# Small helpers

parse_cli <- function(args) {
  out <- list()
  i <- 1
  while (i <= length(args)) {
    key <- sub("^--", "", args[i])
    out[[key]] <- args[i + 1]
    i <- i + 2
  }
  out
}

# SHA-256 of files, as lowercase hex. tools::sha256sum exists from R 4.5.0; digest is the fallback.
file_sha256 <- function(paths) {
  if (exists("sha256sum", envir = asNamespace("tools"))) {
    return(unname(tools::sha256sum(paths)))
  }
  vapply(paths, function(f) digest::digest(file = f, algo = "sha256"), "", USE.NAMES = FALSE)
}

# Parse a support string: "" is the null model, NA is no support, otherwise sorted indices joined
# by ";". Returns list(idx = integer vector or NULL, problem = NA or a description).
parse_support <- function(s, p) {
  if (is.na(s)) return(list(idx = NULL, problem = NA_character_))
  if (s == "") return(list(idx = integer(0), problem = NA_character_))
  if (!grepl("^[0-9]+(;[0-9]+)*$", s)) return(list(idx = NULL, problem = "malformed"))
  idx <- as.numeric(strsplit(s, ";", fixed = TRUE)[[1]])   # numeric first: very long digit runs would overflow integer
  if (any(idx < 1 | idx > p)) return(list(idx = NULL, problem = "index out of 1..p"))
  idx <- as.integer(idx)
  if (any(idx < 1L | idx > p)) return(list(idx = NULL, problem = "index out of 1..p"))
  if (anyDuplicated(idx)) return(list(idx = NULL, problem = "duplicate index"))
  if (is.unsorted(idx, strictly = TRUE)) return(list(idx = NULL, problem = "not sorted"))
  list(idx = idx, problem = NA_character_)
}

read_rule_csv <- function(path) {
  # All columns as character so that "" (null support, empty code list) stays distinct from NA.
  utils::read.csv(path, colClasses = "character", na.strings = "NA", check.names = FALSE)
}

new_problems <- function() {
  data.frame(check = character(0), case_id = character(0), method_id = character(0),
             rule_id = character(0), detail = character(0), stringsAsFactors = FALSE)
}

# ---------------------------------------------------------------------------------------------
# Expected cases and inventory of the results tree

expected_cases <- function(manifest, expect, scale_key, ps = DESIGN_P) {
  m <- manifest[as.integer(manifest$p) %in% ps, ]
  if (expect == "dev") m <- m[as.integer(m$replicate) == 1L, ]
  m$case_id <- paste0(m$dataset_id, "_", scale_key)
  m$pdir <- sprintf("p%04d", as.integer(m$p))
  m
}

# Lists every file of the run tree and splits it into p folder, case folder, method id, extension.
inventory_files <- function(results_dir) {
  rel <- list.files(results_dir, recursive = TRUE, all.files = TRUE, no.. = TRUE)
  parts <- strsplit(rel, "/", fixed = TRUE)
  depth <- lengths(parts)
  f <- data.frame(rel = rel, stringsAsFactors = FALSE)
  f$pdir <- ifelse(depth == 3, vapply(parts, `[`, "", 1), NA)
  f$case_id <- ifelse(depth == 3, vapply(parts, function(x) x[2], ""), NA)
  base <- ifelse(depth == 3, vapply(parts, function(x) x[3], ""), NA)
  f$ext <- ifelse(grepl("\\.(rds|csv|sha256|done)$", base), sub("^.*\\.", "", base), NA)
  f$method_id <- ifelse(is.na(f$ext), NA, sub("\\.(rds|csv|sha256|done)$", "", base))
  f
}

# Checks one .sha256 sidecar: it must list <m>.rds and <m>.csv, and both hashes must recompute.
check_sidecar <- function(case_dir, method_id) {
  side <- file.path(case_dir, paste0(method_id, ".sha256"))
  lines <- readLines(side, warn = FALSE)
  lines <- lines[nzchar(lines)]
  hash <- sub("^([0-9a-f]{64}) [ *](.*)$", "\\1", lines)
  name <- sub("^([0-9a-f]{64}) [ *](.*)$", "\\2", lines)
  bad <- character(0)
  if (any(hash == lines)) bad <- c(bad, "unparsable sidecar line")
  for (need in paste0(method_id, c(".rds", ".csv"))) {
    if (!need %in% name) {
      bad <- c(bad, paste("sidecar does not list", need))
      next
    }
    target <- file.path(case_dir, need)
    if (!file.exists(target)) {
      bad <- c(bad, paste(need, "missing"))
      next
    }
    if (!identical(file_sha256(target), hash[match(need, name)])) bad <- c(bad, paste(need, "hash mismatch"))
  }
  extra <- setdiff(name, paste0(method_id, c(".rds", ".csv")))
  if (length(extra)) bad <- c(bad, paste("sidecar lists other files:", paste(extra, collapse = ",")))
  bad
}

# ---------------------------------------------------------------------------------------------
# Truth

# Reads and verifies one truth file against the truth manifest (file hash and active set).
load_truth <- function(truth_dir, truth_manifest, dataset_id, p) {
  path <- file.path(truth_dir, sprintf("p%04d", p), paste0(dataset_id, ".rds"))
  tm <- truth_manifest[truth_manifest$dataset_id == dataset_id, ]
  if (nrow(tm) != 1) stop("truth manifest has ", nrow(tm), " rows for ", dataset_id)
  if (!identical(file_sha256(path), tm$file_sha256)) stop("truth file hash mismatch: ", path)
  tr <- readRDS(path)
  active <- as.integer(tr$active)
  if (!identical(paste(active, collapse = ";"), tm$active)) stop("truth active differs from manifest: ", dataset_id)
  if (length(active) != S0_SIZE || is.unsorted(active, strictly = TRUE)) stop("truth active malformed: ", dataset_id)
  if (length(tr$beta) != p || !identical(which(tr$beta != 0), active)) stop("truth beta/active disagree: ", dataset_id)
  if (!is.null(tr$dataset_id) && tr$dataset_id != dataset_id) stop("truth dataset_id differs: ", dataset_id)
  list(active = active, beta = tr$beta)
}

# ---------------------------------------------------------------------------------------------
# PIPs (A1 and SuSiE-L100 only): the full PIP vector saved in the RDS.

read_pip <- function(rds_path) {
  obj <- readRDS(rds_path)
  if (!is.null(obj$pip)) return(as.numeric(obj$pip))
  if (!is.null(obj$fit) && !is.null(obj$fit$pip)) return(as.numeric(obj$fit$pip))
  NULL
}

# ---------------------------------------------------------------------------------------------
# Scoring of one fit's rule rows (§IV.1.2 definitions)

score_fit_rows <- function(rows, active, pip, p) {
  sel_cols <- sprintf("sel_a%02d", 1:14)
  pip_cols <- sprintf("pip_a%02d", 1:14)
  out <- rows
  out$tp <- NA_integer_; out$fp <- NA_integer_; out$fn <- NA_integer_
  out$exact <- NA; out$error_type <- NA_character_
  for (cc in sel_cols) out[[cc]] <- NA_integer_
  for (cc in pip_cols) out[[cc]] <- NA_real_
  out$max_pip_null <- NA_real_
  for (i in seq_len(nrow(out))) {
    if (out$status[i] %in% FAILED_STATUSES) {
      # A failed, timed-out or not-run rule is non-recovery; support_audit is never scored.
      out$exact[i] <- FALSE
      out$error_type[i] <- "failed"
      next
    }
    ps <- parse_support(out$support[i], p)
    if (is.null(ps$idx)) next          # malformed or NA support on a non-failed row: left NA, reported
    S <- ps$idx
    tp <- sum(S %in% active)
    fp <- length(S) - tp
    fn <- length(active) - tp
    out$tp[i] <- tp; out$fp[i] <- fp; out$fn[i] <- fn
    out$exact[i] <- (fp == 0 && fn == 0)
    out$error_type[i] <- if (fp == 0 && fn == 0) "exact" else if (fn == 0) "extra_only" else
                         if (fp == 0) "missed_only" else "mixed"
    for (a in seq_along(active)) out[[sel_cols[a]]][i] <- as.integer(active[a] %in% S)
  }
  if (!is.null(pip)) {
    for (a in seq_along(active)) out[[pip_cols[a]]] <- pip[active[a]]
    out$max_pip_null <- max(pip[-active])
  }
  out
}

# ---------------------------------------------------------------------------------------------
# Row checks for one (case, method_id) CSV: provenance, rule set, status, support, flags.

check_fit_rows <- function(rows, run_id, case, method_id, scale_key, p, with_derived = FALSE) {
  pr <- new_problems()
  add <- function(check, rule_id, detail) {
    pr[nrow(pr) + 1, ] <<- list(check, case$case_id, method_id, rule_id, detail)
  }
  missing_cols <- setdiff(BASE_COLUMNS, names(rows))
  if (length(missing_cols)) add("schema_missing_columns", NA, paste(missing_cols, collapse = ","))
  reg <- rules_of(method_id, with_derived)
  same <- function(col, value) !is.na(rows[[col]]) & rows[[col]] == value
  # Numeric fields are compared as numbers: write.csv may print a double such as 2e+06.
  same_num <- function(col, value) {
    x <- suppressWarnings(as.numeric(rows[[col]]))
    !is.na(x) & x == as.numeric(value)
  }
  ychk <- paste0("y_", scale_key, "_sha256")
  checks <- list(
    run_id_mismatch    = same("run_id", run_id),
    case_id_mismatch   = same("case_id", case$case_id),
    dataset_id_mismatch = same("dataset_id", case$dataset_id),
    method_id_mismatch = same("method_id", method_id),
    design_mismatch    = same_num("p", p) & same_num("scenario", case$scenario) &
                         same_num("replicate", case$replicate) & same("scale_key", scale_key),
    x_sha256_mismatch  = same("x_sha256", case$x_sha256),
    y_sha256_mismatch  = same("y_sha256", case[[ychk]]),
    fold_sha256_mismatch = same("fold_sha256", case$foldid_sha256),
    inputs_sha256_mismatch = same("inputs_sha256", case$file_sha256),
    seed_mismatch      = same_num("data_seed", case$data_seed) & same_num("fold_seed", case$fold_seed) &
                         same_num("method_seed", case$method_seed))
  for (nm in names(checks)) {
    bad <- which(!checks[[nm]])
    for (i in bad) add(nm, rows$rule_id[i], "")
  }
  # Rule set: each registered rule exactly once, with its registered role.
  dup <- rows$rule_id[duplicated(rows$rule_id)]
  for (r in unique(dup)) add("duplicate_rule_row", r, "")
  for (r in setdiff(reg$rules, rows$rule_id)) add("missing_rule_row", r, "")
  for (r in setdiff(rows$rule_id, reg$rules)) add("unregistered_rule_row", r, "")
  for (i in seq_len(nrow(rows))) {
    r <- rows$rule_id[i]
    if (r %in% reg$rules && !identical(rows$role[i], reg$roles[match(r, reg$rules)])) add("role_mismatch", r, rows$role[i])
    st <- rows$status[i]
    if (!(st %in% STATUS_VALUES)) { add("status_invalid", r, st); next }
    if (st %in% FAILED_STATUSES) {
      if (!is.na(rows$support[i])) add("failed_with_support", r, rows$support[i])
      if (!is.na(rows$k[i])) add("failed_with_k", r, rows$k[i])
    } else {
      ps <- parse_support(rows$support[i], p)
      if (is.na(rows$support[i])) add("support_missing", r, "")
      else if (!is.na(ps$problem)) add("support_malformed", r, ps$problem)
      else {
        k_num <- suppressWarnings(as.numeric(rows$k[i]))
        if (is.na(k_num) || k_num != length(ps$idx)) add("k_mismatch", r, paste(rows$k[i], length(ps$idx)))
      }
    }
    if (!(rows$diag_flag[i] %in% c("TRUE", "FALSE"))) add("diag_flag_invalid", r, rows$diag_flag[i])
    codes <- if (is.na(rows$diag_codes[i]) || rows$diag_codes[i] == "") character(0) else
             strsplit(rows$diag_codes[i], ";", fixed = TRUE)[[1]]
    unknown <- setdiff(codes, c(FLAG_CODES, INFO_CODES))
    if (length(unknown)) add("diag_code_unknown", r, paste(unknown, collapse = ";"))
    has_flag_code <- any(codes %in% FLAG_CODES)
    if (rows$diag_flag[i] %in% c("TRUE", "FALSE") && (rows$diag_flag[i] == "TRUE") != has_flag_code)
      add("diag_flag_code_disagree", r, paste(rows$diag_flag[i], rows$diag_codes[i]))
    prefilled <- TRUTH_COLUMNS[TRUTH_COLUMNS %in% names(rows)]
    prefilled <- prefilled[!is.na(unlist(rows[i, prefilled])) & unlist(rows[i, prefilled]) != ""]
    if (length(prefilled)) add("truth_columns_prefilled", r, paste(prefilled, collapse = ","))
  }
  # diag_flag is method-wide: identical on every rule row of the fit (§III.3.0).
  if (length(unique(rows$diag_flag)) > 1) add("diag_flag_not_fitwide", NA, paste(rows$diag_flag, collapse = ","))
  pr
}

# ---------------------------------------------------------------------------------------------
# A3 common-random-numbers check (§III.3.8 e step 3): set by the scoring step on all A3 rows of a
# dataset whose non-failed rng_after values differ across scales. Under D3 (c = 1 only) each
# dataset has one A3 fit, so the check cannot fire; it is kept so that the step matches the master.

apply_crn_check <- function(scored, raw_rng) {
  if (!"A3" %in% scored$method_id) return(list(scored = scored, n_flagged = 0L))
  a3 <- which(scored$method_id == "A3" & !(scored$status %in% FAILED_STATUSES))
  n_flagged <- 0L
  for (d in unique(scored$dataset_id[a3])) {
    rows_d <- a3[scored$dataset_id[a3] == d]
    vals <- unique(stats::na.omit(raw_rng[rows_d]))   # NA rng_after on a non-failed row is reported by score_run
    if (length(vals) > 1) {
      all_d <- which(scored$method_id == "A3" & scored$dataset_id == d)
      scored$diag_flag[all_d] <- "TRUE"
      scored$diag_codes[all_d] <- ifelse(is.na(scored$diag_codes[all_d]) | scored$diag_codes[all_d] == "",
                                         "crn_mismatch", paste0(scored$diag_codes[all_d], ";crn_mismatch"))
      n_flagged <- n_flagged + length(all_d)
    }
  }
  list(scored = scored, n_flagged = n_flagged)
}

# ---------------------------------------------------------------------------------------------
# Main: one run

score_run <- function(results_dir, manifest_path, truth_dir, truth_manifest_path, out_dir,
                      method_ids = NULL, expect = "prod", scale_key = "c100", ps = DESIGN_P,
                      derived_csv = NULL) {
  results_dir <- normalizePath(results_dir, mustWork = TRUE)
  run_id <- basename(results_dir)
  if (scale_key == "auto") {
    # The scale key comes from the run's own case folders (c100 or c050); truth is the same support.
    folders <- unlist(lapply(file.path(results_dir, c("p0500", "p1000")), list.files))
    folders <- folders[!grepl("^dev_", folders)]
    keys <- unique(sub("^.*_(c[0-9]{3})$", "\\1", folders))
    if (length(keys) != 1 || !grepl("^c[0-9]{3}$", keys)) stop("cannot determine one scale key from the case folders: ", paste(keys, collapse = ","))
    scale_key <- keys
  }
  derived <- NULL
  if (!is.null(derived_csv)) {
    derived <- read_rule_csv(derived_csv)
    derived_key <- paste(derived$case_id, derived$method_id)
  }
  if (is.null(method_ids)) {
    folder <- sub("^.*_prod(c[0-9]{3})?_", "", run_id)       # _prod_<m> (c = 1) or _prodc050_<m>
    method_ids <- RUN_METHODS[[folder]]
    if (is.null(method_ids)) stop("cannot infer method ids from run id ", run_id, "; pass --methods")
  }
  stopifnot(all(method_ids %in% names(REGISTRY)))
  dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

  manifest <- utils::read.csv(manifest_path, colClasses = "character")
  truth_manifest <- utils::read.csv(truth_manifest_path, colClasses = "character")
  cases <- expected_cases(manifest, expect, scale_key, ps)
  files <- inventory_files(results_dir)
  problems <- new_problems()

  # Files that belong to no expected (case, method_id).
  expected_keys <- paste(rep(cases$pdir, each = length(method_ids)), rep(cases$case_id, each = length(method_ids)),
                         rep(method_ids, nrow(cases)), sep = "|")
  file_keys <- paste(files$pdir, files$case_id, files$method_id, sep = "|")
  extra <- files[is.na(files$ext) | !(file_keys %in% expected_keys), ]
  # Dev canary bundles that production arrays re-run inside the run tree (a "dev_*" case folder at
  # any depth, e.g. p0500/dev_.../ or canary/p0500/dev_.../) are excluded from the production
  # counts and labelled; anything else is an orphan.
  # Production-pattern case folders at another scale (canary reproduction checks inside a run of a
  # different scale) are excluded the same way.
  other_scale <- !is.na(extra$case_id) & grepl("^p[0-9]{4}_S[0-9]+_r[0-9]{3}_c[0-9]{3}$", extra$case_id) &
                 !endsWith(extra$case_id, paste0("_", scale_key))
  extra$kind <- ifelse(grepl("(^|/)dev_p[0-9]{4}_S[0-9]+_r[0-9]{3}_c[0-9]{3}/", extra$rel), "dev_canary",
                       ifelse(other_scale, "other_scale_canary", "orphan"))
  write_table(extra[, c("rel", "pdir", "case_id", "method_id", "ext", "kind")], file.path(out_dir, "files_extra.csv"))

  coverage <- list()
  scored <- list()
  raw_rng <- list()
  truth_cache <- new.env()
  for (ci in seq_len(nrow(cases))) {
    case <- cases[ci, ]
    p <- as.integer(case$p)
    case_dir <- file.path(results_dir, case$pdir, case$case_id)
    for (m in method_ids) {
      present <- file.exists(file.path(case_dir, paste0(m, c(".rds", ".csv", ".sha256", ".done"))))
      state <- if (all(present)) "complete" else if (any(present)) "incomplete" else "missing"
      sidecar_problems <- character(0)
      if (present[3]) sidecar_problems <- check_sidecar(case_dir, m)
      coverage[[length(coverage) + 1]] <- data.frame(
        case_id = case$case_id, dataset_id = case$dataset_id, p = p, scenario = as.integer(case$scenario),
        replicate = as.integer(case$replicate), method_id = m, state = state,
        has_rds = present[1], has_csv = present[2], has_sha256 = present[3], has_done = present[4],
        sha256_ok = present[3] && length(sidecar_problems) == 0, n_rows = NA_integer_, stringsAsFactors = FALSE)
      if (state != "complete") problems[nrow(problems) + 1, ] <- list(paste0("case_", state), case$case_id, m, NA,
                                                                    paste(c("rds", "csv", "sha256", "done")[!present], collapse = ","))
      for (sp in sidecar_problems) problems[nrow(problems) + 1, ] <- list("sha256_check", case$case_id, m, NA, sp)
      if (!present[2]) next

      rows <- tryCatch(read_rule_csv(file.path(case_dir, paste0(m, ".csv"))), error = function(e) NULL)
      if (is.null(rows) || nrow(rows) == 0 || !all(c("rule_id", "status", "support") %in% names(rows))) {
        problems[nrow(problems) + 1, ] <- list("csv_unreadable_or_empty", case$case_id, m, NA, "")
        next
      }
      with_derived <- !is.null(derived) && !is.null(DERIVED_REGISTRY[[m]])
      if (with_derived) {
        # Derived rows of this case: they must come from this case's saved fit (sidecar RDS hash).
        dr <- derived[derived_key == paste(case$case_id, m), ]
        if (nrow(dr) == 0) problems[nrow(problems) + 1, ] <- list("derived_rows_missing", case$case_id, m, NA, "")
        side <- readLines(file.path(case_dir, paste0(m, ".sha256")), warn = FALSE)
        rds_hash <- sub(" .*$", "", side[grepl(paste0(" [ *]?", m, "\\.rds$"), side)])
        if (nrow(dr) && !all(dr$derived_from == rds_hash))
          problems[nrow(problems) + 1, ] <- list("derived_from_differs_from_rds_hash", case$case_id, m, NA, "")
        cols <- union(names(rows), names(dr))
        for (cc in setdiff(cols, names(rows))) rows[[cc]] <- NA_character_
        for (cc in setdiff(cols, names(dr))) dr[[cc]] <- NA_character_
        rows <- rbind(rows[, cols], dr[, cols])
      }
      coverage[[length(coverage)]]$n_rows <- nrow(rows)
      problems <- rbind(problems, check_fit_rows(rows, run_id, case, m, scale_key, p, with_derived))
      # Identity and design columns are taken from the folder and the manifest; any disagreement
      # with the CSV was reported above as a blocking problem.
      rows$run_id <- run_id; rows$case_id <- case$case_id; rows$dataset_id <- case$dataset_id
      rows$method_id <- m; rows$p <- as.character(p); rows$scenario <- as.character(as.integer(case$scenario))
      rows$replicate <- as.character(as.integer(case$replicate)); rows$scale_key <- scale_key

      key <- case$dataset_id
      if (is.null(truth_cache[[key]])) truth_cache[[key]] <- load_truth(truth_dir, truth_manifest, key, p)
      tr <- truth_cache[[key]]

      pip <- NULL
      fit_failed <- all(rows$status %in% FAILED_STATUSES)
      if (m %in% PIP_METHODS && present[1] && !fit_failed) {
        pip <- read_pip(file.path(case_dir, paste0(m, ".rds")))
        if (is.null(pip) || length(pip) != p || any(!is.finite(pip)) || any(pip < 0 | pip > 1)) {
          problems[nrow(problems) + 1, ] <- list("pip_invalid", case$case_id, m, NA, "")
          pip <- NULL
        } else {
          i05 <- which(rows$rule_id == "pip05" & !(rows$status %in% FAILED_STATUSES))
          for (i in i05) {
            if (!identical(rows$support[i], paste(which(pip > 0.5), collapse = ";")))
              problems[nrow(problems) + 1, ] <- list("pip05_support_differs_from_rds_pip", case$case_id, m, "pip05", "")
          }
        }
      }
      for (cc in setdiff(BASE_COLUMNS, names(rows))) rows[[cc]] <- NA_character_
      rng <- if ("rng_after" %in% names(rows)) rows$rng_after else rep(NA_character_, nrow(rows))
      if (m == "A3") for (i in which(!(rows$status %in% FAILED_STATUSES) & is.na(rng)))
        problems[nrow(problems) + 1, ] <- list("rng_after_missing", case$case_id, m, rows$rule_id[i], "")
      s <- score_fit_rows(rows[, BASE_COLUMNS], tr$active, pip, p)
      scored[[length(scored) + 1]] <- s
      raw_rng[[length(raw_rng) + 1]] <- rng
    }
  }
  coverage <- do.call(rbind, coverage)
  if (!length(scored)) stop("no rule rows found under ", results_dir)
  if (!is.null(derived)) {
    expected_d <- unlist(lapply(method_ids[method_ids %in% names(DERIVED_REGISTRY)], function(m) paste(cases$case_id, m)))
    for (k in unique(setdiff(derived_key, expected_d))) problems[nrow(problems) + 1, ] <- list("derived_rows_unmatched", NA, NA, NA, k)
  }
  scored <- do.call(rbind, scored)
  raw_rng <- unlist(raw_rng)

  # Duplicates across the whole run (each (case, method_id, rule_id) once).
  dkey <- paste(scored$case_id, scored$method_id, scored$rule_id)
  for (k in unique(dkey[duplicated(dkey)])) problems[nrow(problems) + 1, ] <- list("duplicate_case_method_rule", NA, NA, NA, k)
  unscored <- which(is.na(scored$error_type))
  for (i in unscored) problems[nrow(problems) + 1, ] <- list("row_not_scorable", scored$case_id[i], scored$method_id[i], scored$rule_id[i], "")

  crn <- apply_crn_check(scored, raw_rng)
  scored <- crn$scored

  # Truth signals per p (for T4): identical across datasets of the same p (§II.3); checked here.
  sig <- list()
  for (key in ls(truth_cache)) {
    tr <- truth_cache[[key]]
    p <- length(tr$beta)
    one <- data.frame(p = p, signal = sprintf("a%02d", seq_along(tr$active)), index = tr$active,
                      beta = tr$beta[tr$active], stringsAsFactors = FALSE)
    if (is.null(sig[[as.character(p)]])) sig[[as.character(p)]] <- one
    else if (!identical(sig[[as.character(p)]], one)) stop("truth differs across datasets at p = ", p, ": ", key)
  }
  write_table(do.call(rbind, sig), file.path(out_dir, "truth_signals.csv"))

  write_table(scored, file.path(out_dir, "scored_rows.csv"))
  write_table(coverage, file.path(out_dir, "coverage.csv"))
  write_table(problems, file.path(out_dir, "problems.csv"))

  log <- c(
    paste("run_id:", run_id),
    paste("results_dir:", results_dir),
    paste("method_ids:", paste(method_ids, collapse = ",")),
    paste("expect:", expect, "| p:", paste(ps, collapse = ",")),
    paste("scale_key:", scale_key, "| derived rows:", if (is.null(derived_csv)) "none" else paste(derived_csv, nrow(derived), "rows")),
    paste("expected cases:", nrow(cases), "| expected (case, method) pairs:", nrow(cases) * length(method_ids)),
    paste("coverage states:", paste(names(table(coverage$state)), table(coverage$state), sep = "=", collapse = " ")),
    paste("sha256 ok:", sum(coverage$sha256_ok), "of", nrow(coverage)),
    paste("files outside expected pairs:", nrow(extra), "| dev canary files (excluded):", sum(extra$kind == "dev_canary"), "| other-scale canary files (excluded):", sum(extra$kind == "other_scale_canary"),
          "in", length(unique(sub("/[^/]*$", "", extra$rel[extra$kind == "dev_canary"]))), "case folders | orphan files:",
          sum(extra$kind == "orphan")),
    paste("scored rows:", if (is.null(scored)) 0 else nrow(scored)),
    paste("rows per method/rule:", paste(names(table(paste(scored$method_id, scored$rule_id))),
                                         table(paste(scored$method_id, scored$rule_id)), sep = "=", collapse = " ")),
    paste("status:", paste(names(table(scored$status)), table(scored$status), sep = "=", collapse = " ")),
    paste("A3 crn_mismatch rows flagged:", crn$n_flagged),
    paste("truth files verified:", length(ls(truth_cache))),
    paste("problems:", nrow(problems)),
    if (nrow(problems)) paste("problem checks:", paste(names(table(problems$check)), table(problems$check), sep = "=", collapse = " ")) else "problem checks: none")
  writeLines(log, file.path(out_dir, "score_log.txt"))
  cat(log, sep = "\n")
  invisible(list(scored = scored, coverage = coverage, problems = problems, extra = extra))
}

if (sys.nframe() == 0L) {
  a <- parse_cli(commandArgs(TRUE))
  score_run(results_dir = a$results, manifest_path = a$manifest, truth_dir = a$truth,
            truth_manifest_path = a[["truth-manifest"]], out_dir = a$out,
            method_ids = if (is.null(a$methods)) NULL else strsplit(a$methods, ",")[[1]],
            expect = if (is.null(a$expect)) "prod" else a$expect,
            scale_key = if (is.null(a$scale)) "c100" else a$scale,
            ps = if (is.null(a$p)) DESIGN_P else as.integer(strsplit(a$p, ",")[[1]]),
            derived_csv = a$derived)
}
