# score_dev.R -- scoring of the A2 dev-test rule rows against the dev truth (master §IV.1.2:
# "Scoring is a separate script, run after fitting"). The only A2 script that reads truth/.
# It never modifies the fit outputs; it writes a scored copy of the rows and a summary table.
#   tp = |S n A|, fp = |S \ A|, fn = |A \ S|, exact = (fp = 0 and fn = 0);
#   error_type: exact / extra_only (fp > 0, fn = 0) / missed_only (fp = 0, fn > 0) /
#   mixed (fp > 0, fn > 0) / failed (status in failed, timeout, not_run; tp, fp, fn NA);
#   sel_aNN = 1 if the NN-th true active index (in truth order) is selected, NA beyond s0.
# Usage: Rscript score_dev.R --results <results/<run_id>> --truth <dev/truth> --out <dir>

parse_support <- function(key) {
  if (is.na(key)) return(NA_integer_)
  if (!nzchar(key)) return(integer(0))
  as.integer(strsplit(key, ";", fixed = TRUE)[[1]])
}

score_rows <- function(rows, active) {
  for (i in seq_len(nrow(rows))) {
    failed <- rows$status[i] %in% c("failed", "timeout", "not_run")
    if (failed) {
      rows$tp[i] <- NA; rows$fp[i] <- NA; rows$fn[i] <- NA
      rows$exact[i] <- FALSE; rows$error_type[i] <- "failed"
      next
    }
    S <- parse_support(as.character(rows$support[i]))
    if (length(S) != rows$k[i]) stop("support size differs from k in row ", i)
    tp <- length(intersect(S, active)); fp <- length(setdiff(S, active)); fn <- length(setdiff(active, S))
    rows$tp[i] <- tp; rows$fp[i] <- fp; rows$fn[i] <- fn
    rows$exact[i] <- fp == 0L && fn == 0L
    rows$error_type[i] <- if (fp == 0L && fn == 0L) "exact" else if (fn == 0L) "extra_only" else
                          if (fp == 0L) "missed_only" else "mixed"
    for (a in seq_len(14L)) rows[[sprintf("sel_a%02d", a)]][i] <- if (a <= length(active)) as.integer(active[a] %in% S) else NA
  }
  rows
}

score_dev <- function(results_dir, truth_root, out_dir) {
  csvs <- list.files(results_dir, pattern = "\\.csv$", recursive = TRUE, full.names = TRUE)
  if (!length(csvs)) stop("no rule-row CSVs under ", results_dir)
  scored <- do.call(rbind, lapply(csvs, function(f) {
    rows <- utils::read.csv(f, stringsAsFactors = FALSE, colClasses = c(support = "character", support_audit = "character"))
    tr <- readRDS(file.path(truth_root, sprintf("p%04d", rows$p[1]), paste0(rows$dataset_id[1], ".rds")))
    score_rows(rows, as.integer(tr$active))
  }))
  scored <- scored[order(scored$p, scored$scenario, scored$method_id), ]
  dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
  utils::write.csv(scored, file.path(out_dir, "scored_rows.csv"), row.names = FALSE, na = "NA")
  tab <- data.frame(dataset = scored$dataset_id, method = scored$method_id, rule = scored$rule_id,
                    role = scored$role, status = scored$status, k = scored$k, TP = scored$tp,
                    FP = scored$fp, FN = scored$fn, exact = scored$exact, error_type = scored$error_type,
                    converged = scored$converged, diag_codes = scored$diag_codes,
                    runtime_s = round(scored$runtime_s, 2))
  utils::write.csv(tab, file.path(out_dir, "dev_table.csv"), row.names = FALSE, na = "NA")
  print(tab, row.names = FALSE)
  invisible(tab)
}

if (sys.nframe() == 0L) {
  a <- commandArgs(trailingOnly = TRUE)
  get_arg <- function(k) { i <- match(paste0("--", k), a); if (is.na(i)) stop("missing --", k); a[i + 1L] }
  score_dev(get_arg("results"), get_arg("truth"), get_arg("out"))
}
