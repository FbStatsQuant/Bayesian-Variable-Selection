#!/usr/bin/env Rscript
# score_dev.R -- scoring step for the F4 dev test (master §IV.1.2 scoring columns, error types).
# Separate from fitting: this is the only F4 script that reads the truth/ tree. It never changes the
# fit outputs; it writes a scored copy of the rule rows and a summary table.
#
# Usage: Rscript score_dev.R <results_root> <truth_root> <out_dir>
#   results_root = .../dev_test/F4_MCP_SCAD/results/<run_id>   (holds p0500/, p1000/)
#   truth_root   = /projects/ml75/fb31/BVS/bench20261019/dev/truth

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3L) stop("usage: score_dev.R <results_root> <truth_root> <out_dir>")
results_root <- normalizePath(args[1L], mustWork = TRUE)
truth_root <- normalizePath(args[2L], mustWork = TRUE)
out_dir <- args[3L]; dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

parse_key <- function(key) {
  if (is.na(key)) return(NA_integer_)
  if (!nzchar(key)) return(integer())
  as.integer(strsplit(key, ";", fixed = TRUE)[[1L]])
}

csvs <- list.files(results_root, pattern = "[.]csv$", recursive = TRUE, full.names = TRUE)
# Only completed pairs (a .done beside the CSV) are scored; pairs without .done are left to the
# reconciliation step (timeout / not_run rows, §III.3.0) and are counted here, not dropped silently.
done <- file.exists(sub("[.]csv$", ".done", csvs))
cat(sprintf("CSV files %d; completed (with .done) %d; without .done (not scored) %d\n",
            length(csvs), sum(done), sum(!done)))
if (any(!done)) writeLines(csvs[!done], file.path(out_dir, "not_scored_without_done.txt"))
csvs <- csvs[done]
if (!length(csvs)) stop("no completed result CSVs under ", results_root)
rows <- do.call(rbind, lapply(csvs, function(f)
  read.csv(f, stringsAsFactors = FALSE, colClasses = c(support = "character", support_audit = "character"))))

tcache <- list()
for (i in seq_len(nrow(rows))) {
  did <- rows$dataset_id[i]
  if (is.null(tcache[[did]]))
    tcache[[did]] <- readRDS(file.path(truth_root, sprintf("p%04d", rows$p[i]), paste0(did, ".rds")))
  act <- tcache[[did]]$active
  failed <- rows$status[i] %in% c("failed", "timeout", "not_run")
  if (failed) {
    rows$tp[i] <- NA; rows$fp[i] <- NA; rows$fn[i] <- NA
    rows$exact[i] <- FALSE; rows$error_type[i] <- "failed"
  } else {
    sel <- parse_key(rows$support[i])
    tp <- sum(sel %in% act); fp <- length(sel) - tp; fn <- length(act) - tp
    rows$tp[i] <- tp; rows$fp[i] <- fp; rows$fn[i] <- fn; rows$exact[i] <- fp == 0 && fn == 0
    rows$error_type[i] <- if (fp == 0 && fn == 0) "exact" else if (fn == 0) "extra_only"
                          else if (fp == 0) "missed_only" else "mixed"
    for (a in seq_along(act)) rows[[sprintf("sel_a%02d", a)]][i] <- as.integer(act[a] %in% sel)
  }
}
rows <- rows[order(rows$p, rows$scenario, rows$method_id != "F4", match(rows$rule_id, c("ebic1", "ebic05", "bic"))), ]
write.csv(rows, file.path(out_dir, "scored_rule_rows.csv"), row.names = FALSE, na = "NA")

tab <- data.frame(dataset = rows$dataset_id, method = rows$method_id, rule = rows$rule_id,
                  role = rows$role, status = rows$status, k = rows$k, TP = rows$tp, FP = rows$fp,
                  FN = rows$fn, exact = rows$exact, runtime_s = round(rows$runtime_s, 2),
                  converged = rows$converged, diag_flag = rows$diag_flag,
                  diag_codes = ifelse(is.na(rows$diag_codes), "", rows$diag_codes),
                  stringsAsFactors = FALSE)
write.csv(tab, file.path(out_dir, "dev_table.csv"), row.names = FALSE, na = "NA")
md <- c(paste("|", paste(names(tab), collapse = " | "), "|"),
        paste("|", paste(rep("---", ncol(tab)), collapse = " | "), "|"),
        apply(tab, 1, function(r) paste("|", paste(trimws(r), collapse = " | "), "|")))
writeLines(md, file.path(out_dir, "dev_table.md"))
cat(md, sep = "\n")
