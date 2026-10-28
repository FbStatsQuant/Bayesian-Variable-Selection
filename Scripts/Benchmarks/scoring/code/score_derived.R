# score_derived.R: scoring of a derived post-hoc rule (thread S, 2026-10-19).
#
# The lead derived `ebic1_K37` (EBIC(1) with candidate cap floor(n / log n) = 37) for F5 and
# F4/F4_SCAD from the saved candidate tables, AFTER seeing the production cap-hit diagnostics.
# It is not a pre-declared rule. This script scores it as a separate, labelled S-table and never
# touches T1 or the run's other tables.
#
# Usage (inside a SLURM job):
#   Rscript --vanilla score_derived.R --derived <derived rule-row CSV> --prod-out <scoring/out/<run_id>> \
#     --manifest <inputs_manifest.csv> --truth <truth dir> --truth-manifest <truth_manifest.csv> \
#     --out <dir> --rule ebic1_K37 --role S0_posthoc --cap 37 --methods F4,F4_SCAD
#
# Checks: each expected (case, method_id) exactly once; rule_id and role as stated; provenance,
# design, seed, hash, method and compute columns equal to the production `ebic1` row of the same
# case and to the inputs manifest; support well formed, k consistent, k <= cap.
# Outputs in --out: scored_rows_posthoc.csv, problems_posthoc.csv, S_table_posthoc.csv,
# changes_vs_ebic1.csv, summary_posthoc.md.

find_code_dir <- function() {
  a <- grep("^--file=", commandArgs(FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
}
code_dir <- find_code_dir()
if (!exists("REGISTRY")) source(file.path(code_dir, "registry.R"))
if (!exists("score_run")) source(file.path(code_dir, "score.R"))
if (!exists("summarise_cell")) source(file.path(code_dir, "aggregate.R"))

POSTHOC_LABEL <- "post hoc, chosen after seeing the production cap-hit diagnostics; not a pre-declared rule"

# Columns copied from the production row of the same case (strings compared exactly, numbers as numbers).
COPIED_TEXT <- c("study", "run_id", "source_sha256", "regime", "scale_key", "dataset_id", "case_id",
                 "inputs_sha256", "x_sha256", "y_sha256", "fold_sha256", "method_id", "method_label",
                 "package", "package_version", "host", "slurm_job_id", "slurm_array_task_id",
                 "started_utc", "finished_utc")
COPIED_NUM <- c("p", "scenario", "replicate", "scale", "data_seed", "fold_seed", "method_seed", "runtime_s")
# Fit-level fields that may legitimately differ for a derived rule (reported as counts, not problems).
FIT_FIELDS <- c("status", "converged", "diag_flag")

score_derived <- function(derived_csv, prod_out, manifest_path, truth_dir, truth_manifest_path, out_dir,
                          rule, role, cap, method_ids, scale_key = "c100") {
  dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
  d <- read_rule_csv(derived_csv)
  prod <- utils::read.csv(file.path(prod_out, "scored_rows.csv"), colClasses = "character", na.strings = "NA")
  prod <- prod[prod$rule_id == "ebic1", ]
  manifest <- utils::read.csv(manifest_path, colClasses = "character")
  truth_manifest <- utils::read.csv(truth_manifest_path, colClasses = "character")
  cases <- expected_cases(manifest, "prod", scale_key)
  problems <- new_problems()
  add <- function(check, case_id, m, detail) problems[nrow(problems) + 1, ] <<- list(check, case_id, m, rule, detail)

  # Coverage: each expected (case, method_id) exactly once, nothing else.
  key_d <- paste(d$case_id, d$method_id)
  key_e <- paste(rep(cases$case_id, each = length(method_ids)), rep(method_ids, nrow(cases)))
  for (k in unique(key_d[duplicated(key_d)])) add("duplicate_row", NA, NA, k)
  for (k in setdiff(key_e, key_d)) add("missing_row", NA, NA, k)
  for (k in setdiff(key_d, key_e)) add("unexpected_row", NA, NA, k)
  if (any(d$rule_id != rule)) add("rule_id_mismatch", NA, NA, paste(unique(d$rule_id), collapse = ","))
  if (any(d$role != role)) add("role_mismatch", NA, NA, paste(unique(d$role), collapse = ","))

  fit_diff <- setNames(integer(length(FIT_FIELDS)), FIT_FIELDS)
  scored <- list()
  truth_cache <- new.env()
  for (i in seq_len(nrow(d))) {
    r <- d[i, ]
    ci <- match(r$case_id, cases$case_id)
    if (is.na(ci)) next
    case <- cases[ci, ]
    p <- as.integer(case$p)
    pr <- prod[prod$case_id == r$case_id & prod$method_id == r$method_id, ]
    if (nrow(pr) != 1) { add("no_production_row", r$case_id, r$method_id, ""); next }
    # Copied columns against the production row.
    for (cc in COPIED_TEXT) if (!identical(r[[cc]], pr[[cc]])) add("provenance_differs_from_production", r$case_id, r$method_id, cc)
    for (cc in COPIED_NUM) {
      a <- suppressWarnings(as.numeric(r[[cc]])); b <- suppressWarnings(as.numeric(pr[[cc]]))
      if (!isTRUE(a == b)) add("provenance_differs_from_production", r$case_id, r$method_id, cc)
    }
    for (cc in FIT_FIELDS) if (!identical(r[[cc]], pr[[cc]])) fit_diff[cc] <- fit_diff[cc] + 1L
    # Against the manifest: the same checks as for production rows (hashes, seeds, design, ids).
    chk <- check_fit_rows(r, pr$run_id, case, r$method_id, scale_key, p)
    chk <- chk[!chk$check %in% c("missing_rule_row", "unregistered_rule_row", "role_mismatch",
                                 "schema_missing_columns"), ]       # the derived rule is not in the registry
    problems <- rbind(problems, chk)
    if (!(r$status %in% FAILED_STATUSES) && !is.na(r$k) && suppressWarnings(as.numeric(r$k)) > cap)
      add("k_above_cap", r$case_id, r$method_id, r$k)
    key <- case$dataset_id
    if (is.null(truth_cache[[key]])) truth_cache[[key]] <- load_truth(truth_dir, truth_manifest, key, p)
    for (cc in setdiff(BASE_COLUMNS, names(r))) r[[cc]] <- NA_character_
    scored[[length(scored) + 1]] <- score_fit_rows(r[, BASE_COLUMNS], truth_cache[[key]]$active, NULL, p)
  }
  scored <- do.call(rbind, scored)
  for (i in which(is.na(scored$error_type))) add("row_not_scorable", scored$case_id[i], scored$method_id[i], "")
  write_table(scored, file.path(out_dir, "scored_rows_posthoc.csv"))
  write_table(problems, file.path(out_dir, "problems_posthoc.csv"))

  # The S-table, same layout and denominators as rules_long, labelled.
  s <- scored
  s$p <- as.integer(s$p); s$scenario <- as.integer(s$scenario); s$flagged <- s$diag_flag == "TRUE"
  long <- list(); changes <- list()
  for (m in method_ids) for (pp in DESIGN_P) for (sc in c(DESIGN_SCENARIOS, NA)) {
    n_exp <- sum(as.integer(cases$p) == pp & (is.na(sc) | as.integer(cases$scenario) == sc))
    r <- s[which(s$method_id == m & s$p == pp & (is.na(sc) | s$scenario == sc)), ]
    lab <- if (is.na(sc)) "pooled" else as.character(sc)
    long[[length(long) + 1]] <- cbind(data.frame(method_id = m, rule_id = rule, role = role, p = pp, scenario = lab,
                                                 label = POSTHOC_LABEL, stringsAsFactors = FALSE), summarise_cell(r, n_exp))
    pr <- prod[which(prod$method_id == m & as.integer(prod$p) == pp & (is.na(sc) | as.integer(prod$scenario) == sc)), ]
    jj <- match(r$case_id, pr$case_id)
    same_support <- mapply(function(a, b) identical(a, b), r$support, pr$support[jj])
    changes[[length(changes) + 1]] <- data.frame(
      method_id = m, p = pp, scenario = lab, n_cases = nrow(r), n_support_changed = sum(!same_support),
      exact_ebic1 = sum(pr$exact[jj] == "TRUE"), exact_posthoc = sum(r$exact),
      gained = sum(r$exact & pr$exact[jj] != "TRUE"), lost = sum(!r$exact & pr$exact[jj] == "TRUE"),
      stringsAsFactors = FALSE)
  }
  long <- do.call(rbind, long); changes <- do.call(rbind, changes)
  if (nrow(problems) == 0 && any(long$n_missing != 0)) stop("posthoc: missing rows without a reported problem")
  write_table(long, file.path(out_dir, "S_table_posthoc.csv"))
  write_table(changes, file.path(out_dir, "changes_vs_ebic1.csv"))

  L <- c(paste0("# Post-hoc S-table: `", rule, "` (", basename(prod_out), ")"), "",
         paste0("**", POSTHOC_LABEL, ".** Not part of T1; the primary rule stays the pre-declared `ebic1` (cap 100). Provisional (G5, G9)."), "",
         paste0("- derived file: `", derived_csv, "` (sha256 ", file_sha256(derived_csv), ")"),
         paste0("- rows: ", nrow(d), "; scored: ", nrow(scored), "; problems: ", nrow(problems),
                if (nrow(problems)) paste0(" (", paste(names(table(problems$check)), table(problems$check), sep = "=", collapse = " "), ")") else ""),
         paste0("- fit-level fields differing from the production `ebic1` row (not problems): ",
                paste(names(fit_diff), fit_diff, sep = "=", collapse = " ")), "")
  for (m in method_ids) {
    x <- long[long$method_id == m, ]
    tab <- data.frame(p = x$p, scenario = x$scenario, exact = paste0(x$exact_all, "/", x$n_expected),
                      failures = x$n_fail_total, mean_FP = sprintf("%.2f", x$mean_fp), mean_FN = sprintf("%.2f", x$mean_fn))
    ch <- changes[changes$method_id == m, ]
    tab$ebic1_exact <- ch$exact_ebic1; tab$supports_changed <- ch$n_support_changed; tab$gained <- ch$gained; tab$lost <- ch$lost
    L <- c(L, paste0("## ", m, " `", rule, "`"), "", md_table(tab), "")
  }
  writeLines(L, file.path(out_dir, "summary_posthoc.md"))
  cat(L, sep = "\n")
  invisible(list(scored = scored, problems = problems, long = long, changes = changes))
}

if (sys.nframe() == 0L) {
  a <- parse_cli(commandArgs(TRUE))
  score_derived(derived_csv = a$derived, prod_out = a[["prod-out"]], manifest_path = a$manifest,
                truth_dir = a$truth, truth_manifest_path = a[["truth-manifest"]], out_dir = a$out,
                rule = a$rule, role = a$role, cap = as.numeric(a$cap), method_ids = strsplit(a$methods, ",")[[1]])
}
