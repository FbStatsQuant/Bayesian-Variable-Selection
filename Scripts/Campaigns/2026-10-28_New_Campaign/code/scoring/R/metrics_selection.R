# metrics_selection.R -- selection outcomes for every method and rule, both regimes (master II.8, IV.1.3).
# Failed / timeout / not_run rows stay in the denominator as non-recovery (error_type "failed", exact = FALSE).
# The expected grid is ROSTER x REGISTRY (never the observed files): a missing result is a not_run row.
FAIL_STATUS <- c("failed", "timeout", "not_run")

# method/rule registry: data.frame(method_id, rule_id, role, required, in_h4); read from CSV
read_registry <- function(path) {
  r <- utils::read.csv(path, stringsAsFactors = FALSE, na.strings = "NA")
  need <- c("method_id", "rule_id", "role", "required", "in_h4")
  if (!all(need %in% names(r))) stop("registry ", path, " must have columns ", paste(need, collapse = ", "))
  r$required <- as.logical(r$required); r$in_h4 <- as.logical(r$in_h4)
  if (anyDuplicated(r[, c("method_id", "rule_id")])) stop("duplicate (method_id, rule_id) in the registry")
  r
}

# exact reference rows (method_id EXACT): rule hpm = exact HPM, rule mpm = exact MPM. An unavailable exact reference gives NO row (the grid makes it not_run).
exact_reference_rows <- function(exact_by_case) {
  rows <- list()
  for (cid in names(exact_by_case)) {
    es <- exact_by_case[[cid]]
    if (is.null(es)) next
    for (ru in c("hpm", "mpm")) {
      S <- if (ru == "hpm") es[["hpm"]] else es[["mpm"]]
      if (is.null(S)) next
      rows[[length(rows) + 1L]] <- data.frame(case_id = cid, dataset_id = sub("_c[0-9]{3}$", "", cid), method_id = "EXACT", rule_id = ru,
        role = "reference", status = "ok", support = enc_support(S), runtime_s = NA_real_, diag_flag = FALSE, diag_codes = NA_character_, adaptation_ids = NA_character_, stringsAsFactors = FALSE)
    }
  }
  if (length(rows)) do.call(rbind, rows) else NULL
}

# rows: data.frame(RULE_COLS) from SMC records, benchmarks and EXACT references (already de-duplicated; a duplicate key is an error)
# truth_by_dataset: named list dataset_id -> integer support S0;  expected_cases: roster case ids;  registry: read_registry()
score_selection <- function(rows, truth_by_dataset, expected_cases, registry) {
  if (!is.null(rows)) for (nm in setdiff(RULE_COLS, names(rows))) rows[[nm]] <- NA
  rows <- if (is.null(rows)) data.frame(matrix(ncol = length(RULE_COLS), nrow = 0, dimnames = list(NULL, RULE_COLS)), stringsAsFactors = FALSE) else unique(rows[, RULE_COLS, drop = FALSE])
  key <- paste(rows$case_id, rows$method_id, rows$rule_id, sep = "|")
  if (anyDuplicated(key)) stop("conflicting duplicate selection rows for: ", paste(unique(key[duplicated(key)]), collapse = ", "))
  need <- registry[registry$required, c("method_id", "rule_id"), drop = FALSE]
  grid <- merge(data.frame(case_id = expected_cases, stringsAsFactors = FALSE), need, by = NULL)
  allrows <- merge(grid, rows, by = c("case_id", "method_id", "rule_id"), all = TRUE)
  allrows$dataset_id <- ifelse(is.na(allrows$dataset_id), sub("_c[0-9]{3}$", "", allrows$case_id), allrows$dataset_id)
  nr <- is.na(allrows$status)
  allrows$status[nr] <- "not_run"
  rk <- paste(registry$method_id, registry$rule_id); ak <- paste(allrows$method_id, allrows$rule_id)
  reg_role <- registry$role[match(ak, rk)]
  bad_role <- !is.na(allrows$role) & !is.na(reg_role) & allrows$role != reg_role
  if (any(bad_role)) stop("observed role differs from the registry role for: ", paste(unique(paste0(ak[bad_role], " (", allrows$role[bad_role], " vs ", reg_role[bad_role], ")")), collapse = ", "))
  allrows$role <- ifelse(is.na(allrows$role), reg_role, allrows$role)
  allrows$in_registry <- ak %in% rk
  allrows$in_h4 <- ifelse(allrows$in_registry, registry$in_h4[match(ak, rk)], FALSE)
  allrows$in_expected <- allrows$case_id %in% expected_cases
  out <- vector("list", nrow(allrows))
  for (i in seq_len(nrow(allrows))) {
    r <- allrows[i, ]
    pc <- parse_case_id(r$case_id)
    S0 <- truth_by_dataset[[r$dataset_id]]
    S <- parse_support(r$support)
    failed <- r$status %in% FAIL_STATUS || is.null(S)
    if (failed || is.null(S0)) {
      tp <- fp <- fn <- NA_integer_; ex <- FALSE; et <- "failed"; k <- NA_integer_
    } else {
      tp <- length(intersect(S, S0)); fp <- length(setdiff(S, S0)); fn <- length(setdiff(S0, S)); k <- length(S)
      ex <- fp == 0L && fn == 0L
      et <- if (ex) "none" else if (fn == 0L) "extra_only" else if (fp == 0L) "missed_only" else "mixed"
    }
    out[[i]] <- list(case_id = r$case_id, dataset_id = r$dataset_id, p = pc$p %||% NA_integer_, scenario = pc$scenario %||% NA_integer_,
                     replicate = pc$replicate %||% NA_integer_, scale_key = pc$scale_key %||% NA_character_,
                     method_id = r$method_id, rule_id = r$rule_id, role = r$role, status = r$status, diag_flag = as.logical(r$diag_flag),
                     k = k, tp = tp, fp = fp, fn = fn, exact = ex, error_type = et, runtime_s = as.numeric(r$runtime_s),
                     adaptation_ids = r$adaptation_ids, in_expected = r$in_expected, in_registry = r$in_registry, in_h4 = r$in_h4)
  }
  data.table::rbindlist(lapply(out, function(l) lapply(l, function(v) if (is.null(v)) NA else v)))
}
