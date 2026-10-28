#!/usr/bin/env Rscript
# score_dev.R -- scoring of the F1 dev test (separate from fitting; master §IV.1.2 "Scoring is a separate
# script, run after fitting"). It is the only F1 file that reads the dev truth files. It never edits the fit
# CSVs; it writes a scored copy and a summary table to the summary directory.
# Usage: Rscript --vanilla score_dev.R <results/<run_id> dir> <dev truth root> <summary dir>

args <- commandArgs(trailingOnly = TRUE)
res_dir <- args[[1]]; truth_root <- args[[2]]; out <- args[[3]]
dir.create(out, recursive = TRUE, showWarnings = FALSE)

files <- list.files(res_dir, pattern = "^F1\\.csv$", recursive = TRUE, full.names = TRUE)
if (!length(files)) stop("no F1.csv under ", res_dir)
scored <- list()
for (f in files) {
  r <- read.csv(f, stringsAsFactors = FALSE, na.strings = "NA",
                colClasses = c(support = "character", support_audit = "character", diag_codes = "character",
                               warnings = "character", messages = "character", error = "character",
                               slurm_job_id = "character", slurm_array_task_id = "character"))
  tr <- readRDS(file.path(truth_root, sprintf("p%04d", r$p[1]), paste0(r$dataset_id[1], ".rds")))
  active <- as.integer(tr$active); s0 <- length(active)
  for (i in seq_len(nrow(r))) {
    if (r$status[i] %in% c("failed", "timeout", "not_run")) { r$error_type[i] <- "failed"; next }
    S <- if (nzchar(r$support[i])) as.integer(strsplit(r$support[i], ";", fixed = TRUE)[[1]]) else integer()
    r$tp[i] <- sum(S %in% active); r$fp[i] <- length(S) - r$tp[i]; r$fn[i] <- s0 - r$tp[i]
    r$exact[i] <- r$fp[i] == 0 && r$fn[i] == 0
    r$error_type[i] <- if (r$exact[i]) "exact" else if (r$fn[i] == 0) "extra_only" else if (r$fp[i] == 0) "missed_only" else "mixed"
    for (a in seq_len(s0)) r[[sprintf("sel_a%02d", a)]][i] <- as.integer(active[a] %in% S)
  }
  scored[[f]] <- r
}
all <- do.call(rbind, scored); rownames(all) <- NULL
all <- all[order(all$p, all$scenario, match(all$rule_id, c("cv_min", "cv_1se", "ebic1", "ebic05"))), ]
write.csv(all, file.path(out, "F1_dev_scored.csv"), row.names = FALSE, na = "NA")

tab <- data.frame(dataset = all$dataset_id, rule = all$rule_id, role = all$role, status = all$status, k = all$k,
                  TP = all$tp, FP = all$fp, FN = all$fn, exact = all$exact, error_type = all$error_type,
                  diag_flag = all$diag_flag, diag_codes = all$diag_codes, runtime_s = round(all$runtime_s, 2),
                  stringsAsFactors = FALSE)
write.csv(tab, file.path(out, "F1_dev_table.csv"), row.names = FALSE, na = "NA")
md <- c(paste("|", paste(names(tab), collapse = " | "), "|"), paste0("|", strrep("---|", ncol(tab))),
        apply(tab, 1, function(x) paste("|", paste(ifelse(is.na(x), "NA", trimws(x)), collapse = " | "), "|")))
by_rule <- aggregate(exact ~ p + rule_id, data = data.frame(p = all$p, rule_id = all$rule_id, exact = all$exact %in% TRUE),
                     FUN = sum)
writeLines(md, file.path(out, "F1_dev_table.md"))
cat(md, sep = "\n"); cat("\nExact recoveries by p and rule (out of 6):\n"); print(by_rule[, c("p", "rule_id", "exact")])
