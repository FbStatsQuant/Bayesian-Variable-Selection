# a3_longchain.R: A3 8x long-chain sensitivity for the ESS-flagged fits (PREREG_c050 R6; reported
# beside A3, never substituted). Thread S, 2026-10-21.
#
# Scores the long-chain run trees with the scorer's own functions (sidecar, provenance and row checks
# against the inputs manifest, verified truth), checks that the long-chain cases are exactly the
# production fits flagged by an ESS check, and compares ci95 and km2 at the production budget and at 8x.
#
# Usage: Rscript --vanilla a3_longchain.R --long050 <results dir> --long100 <results dir> \
#   --prod050 <scored A3 c050 run dir> --prod100 <scored A3 c100 run dir> --manifest <inputs_manifest.csv> \
#   --truth <truth dir> --truth-manifest <truth_manifest.csv> --out <dir>
# Writes <out>/A3_longchain_sensitivity.csv (per scale x p x scenario and pooled), .md, and
# <out>/A3_longchain_per_case.csv (one row per flagged fit and rule).

find_code_dir <- function() {
  a <- grep("^--file=", commandArgs(FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
}
if (!exists("REGISTRY")) source(file.path(find_code_dir(), "registry.R"))
if (!exists("score_run")) source(file.path(find_code_dir(), "score.R"))

LABEL <- "A3 (8× chain, flagged fits)"
SENS_LABEL <- "sensitivity only: production fit replaced by its 8x fit for the ESS-flagged fits; never substituted for A3"

score_long_run <- function(results_dir, manifest, truth_dir, truth_manifest) {
  run_id <- basename(normalizePath(results_dir))
  problems <- new_problems(); out <- list()
  for (pdir in c("p0500", "p1000")) {
    if (!dir.exists(file.path(results_dir, pdir))) next
    for (case_id in list.files(file.path(results_dir, pdir))) {
      cd <- file.path(results_dir, pdir, case_id)
      sk <- sub("^.*_(c[0-9]{3})$", "\\1", case_id)
      case <- manifest[paste0(manifest$dataset_id, "_", sk) == case_id, ]
      if (nrow(case) != 1) { problems[nrow(problems) + 1, ] <- list("case_not_in_manifest", case_id, "A3", NA, ""); next }
      case$case_id <- case_id
      p <- as.integer(case$p)
      for (sp in check_sidecar(cd, "A3")) problems[nrow(problems) + 1, ] <- list("sha256_check", case_id, "A3", NA, sp)
      rows <- read_rule_csv(file.path(cd, "A3.csv"))
      problems <- rbind(problems, check_fit_rows(rows, run_id, case, "A3", sk, p))
      tr <- load_truth(truth_dir, truth_manifest, case$dataset_id, p)
      for (cc in setdiff(BASE_COLUMNS, names(rows))) rows[[cc]] <- NA_character_
      out[[length(out) + 1]] <- score_fit_rows(rows[, BASE_COLUMNS], tr$active, NULL, p)
    }
  }
  list(scored = do.call(rbind, out), problems = problems)
}

a3_longchain <- function(long050, long100, prod050, prod100, manifest_path, truth_dir, truth_manifest_path, out_dir) {
  manifest <- utils::read.csv(manifest_path, colClasses = "character")
  truth_manifest <- utils::read.csv(truth_manifest_path, colClasses = "character")
  L <- lapply(c(long050, long100), score_long_run, manifest, truth_dir, truth_manifest)
  long <- do.call(rbind, lapply(L, `[[`, "scored")); problems <- do.call(rbind, lapply(L, `[[`, "problems"))
  prod <- do.call(rbind, lapply(c(prod050, prod100), function(d)
    utils::read.csv(file.path(d, "scored_rows.csv"), colClasses = "character", na.strings = "NA")))
  prod <- prod[prod$method_id == "A3", ]
  # The long-chain cases must be exactly the production fits flagged by an ESS check.
  flagged_prod <- unique(prod$case_id[prod$rule_id == "ci95" & prod$diag_flag == "TRUE"])
  long_cases <- unique(long$case_id)
  for (k in setdiff(flagged_prod, long_cases)) problems[nrow(problems) + 1, ] <- list("flagged_fit_without_long_chain", k, "A3", NA, "")
  for (k in setdiff(long_cases, flagged_prod)) problems[nrow(problems) + 1, ] <- list("long_chain_for_unflagged_fit", k, "A3", NA, "")

  # Per case and rule: production vs 8x.
  key_l <- paste(long$case_id, long$rule_id); key_p <- paste(prod$case_id, prod$rule_id)
  j <- match(key_l, key_p)
  pc <- data.frame(scale_key = long$scale_key, case_id = long$case_id, p = as.integer(long$p), scenario = as.integer(long$scenario),
                   rule_id = long$rule_id, codes_prod = prod$diag_codes[j], codes_long = long$diag_codes,
                   flag_long = long$diag_flag, k_prod = prod$k[j], k_long = long$k,
                   tp_prod = as.integer(prod$tp[j]), tp_long = long$tp, fp_prod = as.integer(prod$fp[j]), fp_long = long$fp,
                   exact_prod = prod$exact[j] == "TRUE", exact_long = long$exact,
                   support_changed = !mapply(identical, prod$support[j], long$support), stringsAsFactors = FALSE)
  pc <- pc[order(pc$scale_key, pc$rule_id, pc$p, pc$scenario, pc$case_id), ]
  write_table(pc, file.path(out_dir, "A3_longchain_per_case.csv"))

  cells <- list()
  for (sk in c("c100", "c050")) for (rule in c("ci95", "km2")) for (p in DESIGN_P) for (sc in c(DESIGN_SCENARIOS, NA)) {
    i <- which(pc$scale_key == sk & pc$rule_id == rule & pc$p == p & (is.na(sc) | pc$scenario == sc))
    a <- which(prod$scale_key == sk & prod$rule_id == rule & as.integer(prod$p) == p & (is.na(sc) | as.integer(prod$scenario) == sc))
    if (!length(i) && !is.na(sc)) next                      # only cells with flagged fits, plus the pooled row
    all_prod <- sum(prod$exact[a] == "TRUE")
    cells[[length(cells) + 1]] <- data.frame(
      method_label = LABEL, scale_key = sk, rule_id = rule, p = p, scenario = if (is.na(sc)) "pooled" else as.character(sc),
      n_flagged_fits = length(i), still_flagged_8x = sum(pc$flag_long[i] == "TRUE"),
      exact_prod = sum(pc$exact_prod[i]), exact_8x = sum(pc$exact_long[i]),
      gained = sum(pc$exact_long[i] & !pc$exact_prod[i]), lost = sum(pc$exact_prod[i] & !pc$exact_long[i]),
      supports_changed = sum(pc$support_changed[i]),
      tp_prod = sum(pc$tp_prod[i]), tp_8x = sum(pc$tp_long[i]), fp_prod = sum(pc$fp_prod[i]), fp_8x = sum(pc$fp_long[i]),
      all_fits_n = length(a), all_fits_exact_prod = all_prod,
      all_fits_exact_implied = all_prod - sum(pc$exact_prod[i]) + sum(pc$exact_long[i]),
      implied_label = SENS_LABEL, stringsAsFactors = FALSE)
  }
  cells <- do.call(rbind, cells)
  write_table(cells, file.path(out_dir, "A3_longchain_sensitivity.csv"))
  write_table(problems, file.path(out_dir, "A3_longchain_problems.csv"))

  md <- c(paste0("# ", LABEL, ": long-chain sensitivity (PREREG_c050 R6)"), "",
          "Reported beside A3, never substituted. Long chains: 8x the production budget, same seeds and settings otherwise (engineers' runs).",
          paste0("Fits: ", sum(pc$rule_id == "ci95" & pc$scale_key == "c050"), " at c = 0.5, ", sum(pc$rule_id == "ci95" & pc$scale_key == "c100"),
                 " at c = 1 (exactly the production fits with an ESS flag). Scoring problems: ", nrow(problems), "."),
          paste0("The `implied` columns are a ", SENS_LABEL, "."), "",
          "| scale | rule | p | scenario | flagged fits | still flagged at 8x | exact prod | exact 8x | gained | lost | supports changed | TP prod / 8x | FP prod / 8x | all-fits exact prod | implied all-fits exact (sensitivity) |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
          sprintf("| %s | %s | %d | %s | %d | %d | %d | %d | %d | %d | %d | %d / %d | %d / %d | %d/%d | %d/%d |", cells$scale_key, cells$rule_id,
                  cells$p, cells$scenario, cells$n_flagged_fits, cells$still_flagged_8x, cells$exact_prod, cells$exact_8x, cells$gained,
                  cells$lost, cells$supports_changed, cells$tp_prod, cells$tp_8x, cells$fp_prod, cells$fp_8x, cells$all_fits_exact_prod,
                  cells$all_fits_n, cells$all_fits_exact_implied, cells$all_fits_n), "",
          "Per-fit rows: A3_longchain_per_case.csv. Provisional (G5).")
  writeLines(md, file.path(out_dir, "A3_longchain_sensitivity.md"))
  cat("a3_longchain: fits", nrow(pc) / 2, "| problems", nrow(problems), "\n")
  invisible(list(cells = cells, per_case = pc, problems = problems))
}

if (sys.nframe() == 0L) {
  a <- commandArgs(TRUE)
  get <- function(k) a[which(a == k) + 1]
  a3_longchain(get("--long050"), get("--long100"), get("--prod050"), get("--prod100"), get("--manifest"),
               get("--truth"), get("--truth-manifest"), get("--out"))
}
