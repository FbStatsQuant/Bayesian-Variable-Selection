# a3_flags.R: A3 horseshoe ESS-flag listing and all-fits vs passing-fits recovery (PREREG_c050 R6).
# Thread S, 2026-10-21.
# Usage: Rscript --vanilla a3_flags.R --c050 <scored A3 c050 run dir> --c100 <scored A3 c100 run dir> --out <dir>
# Writes <out>/A3_ess_flagged_cases.csv (one row per flagged fit, both scales) and
# <out>/A3_ess_flags_by_cell.csv (per scale x p x scenario and pooled: fits, flags by code, exact on all
# fits and on passing fits for ci95 and km2; denominators stay the expected cases, §IV.1.3).

find_code_dir <- function() {
  a <- grep("^--file=", commandArgs(FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd()
}
if (!exists("REGISTRY")) source(file.path(find_code_dir(), "registry.R"))

a3_flags <- function(dir050, dir100, out_dir) {
  s <- do.call(rbind, lapply(c(dir050, dir100), function(d)
    utils::read.csv(file.path(d, "scored_rows.csv"), colClasses = "character", na.strings = "NA")))
  s <- s[s$method_id == "A3", ]
  ci <- s[s$rule_id == "ci95", ]; km <- s[s$rule_id == "km2", ]
  km <- km[match(paste(ci$scale_key, ci$case_id), paste(km$scale_key, km$case_id)), ]
  has <- function(codes, code) {
    codes <- as.character(codes); codes[is.na(codes)] <- ""
    vapply(strsplit(codes, ";", fixed = TRUE), function(v) code %in% v, TRUE)
  }
  flagged <- ci$diag_flag == "TRUE"
  cases <- data.frame(scale_key = ci$scale_key, run_id = ci$run_id, case_id = ci$case_id, dataset_id = ci$dataset_id,
                      p = as.integer(ci$p), scenario = as.integer(ci$scenario), replicate = as.integer(ci$replicate),
                      diag_codes = ci$diag_codes, ess_tau = has(ci$diag_codes, "ess_tau"), ess_ci95 = has(ci$diag_codes, "ess_ci95"),
                      ci95_k = ci$k, ci95_exact = ci$exact, km2_exact = km$exact, stringsAsFactors = FALSE)[flagged, ]
  cases <- cases[order(cases$scale_key, cases$p, cases$scenario, cases$replicate), ]
  write_table(cases, file.path(out_dir, "A3_ess_flagged_cases.csv"))
  cells <- list()
  for (sk in c("c100", "c050")) for (p in DESIGN_P) for (sc in c(DESIGN_SCENARIOS, NA)) {
    i <- which(ci$scale_key == sk & as.integer(ci$p) == p & (is.na(sc) | as.integer(ci$scenario) == sc))
    f <- ci$diag_flag[i] == "TRUE"
    cells[[length(cells) + 1]] <- data.frame(
      scale_key = sk, p = p, scenario = if (is.na(sc)) "pooled" else as.character(sc), n_fits = length(i),
      n_flagged = sum(f), n_ess_tau = sum(has(ci$diag_codes[i], "ess_tau")), n_ess_ci95 = sum(has(ci$diag_codes[i], "ess_ci95")),
      ci95_exact_all = sum(ci$exact[i] == "TRUE"), ci95_exact_passing = sum(ci$exact[i] == "TRUE" & !f),
      km2_exact_all = sum(km$exact[i] == "TRUE"), km2_exact_passing = sum(km$exact[i] == "TRUE" & !f),
      stringsAsFactors = FALSE)
  }
  cells <- do.call(rbind, cells)
  write_table(cells, file.path(out_dir, "A3_ess_flags_by_cell.csv"))
  cat("a3_flags: flagged fits c100", sum(cases$scale_key == "c100"), "| c050", sum(cases$scale_key == "c050"), "\n")
  invisible(list(cases = cases, cells = cells))
}

if (sys.nframe() == 0L) {
  a <- commandArgs(TRUE)
  get <- function(k) a[which(a == k) + 1]
  a3_flags(get("--c050"), get("--c100"), get("--out"))
}
