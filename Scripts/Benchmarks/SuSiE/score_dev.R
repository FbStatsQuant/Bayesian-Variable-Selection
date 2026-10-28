# score_dev.R -- scoring step for the A1 dev test (master §IV.1.2): reads the fit-time rule rows
# and the dev truth, fills tp, fp, fn, exact, error_type, sel_a01.., pip_a01.. and max_pip_null,
# and writes scored copies plus a summary table. Separate from fitting; the only A1 script that
# reads truth/. Fit outputs are not modified.
# Usage: Rscript score_dev.R <results_run_dir> <truth_root> <out_dir> [--exclude_dev]
#   truth_root = /projects/ml75/fb31/BVS/bench20261019/dev/truth

main <- function(run_dir, truth_root, out_dir, exclude_dev = FALSE) {
  dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
  # Only bundles at the canonical path <run_dir>/p<pppp>/<case_id>/<method_id>.csv with a .done
  # marker; quarantine directories and stray files are never scored. With exclude_dev = TRUE the
  # dev-prefixed production canaries are skipped (production scoring).
  csvs <- Sys.glob(file.path(run_dir, "p[0-9][0-9][0-9][0-9]", "*_c100", "*.csv"))
  csvs <- csvs[file.exists(sub("\\.csv$", ".done", csvs))]
  if (exclude_dev) csvs <- csvs[!grepl("^dev_", basename(dirname(csvs)))]
  scored <- lapply(csvs, function(f) {
    x <- utils::read.csv(f, colClasses = "character")
    did <- x$dataset_id[1]
    tr <- readRDS(file.path(truth_root, sprintf("p%04d", as.integer(x$p[1])), paste0(did, ".rds")))
    stopifnot(identical(tr$dataset_id, did))
    act <- as.integer(tr$active); s0 <- length(act); p <- as.integer(x$p[1])
    rds <- readRDS(sub("\\.csv$", ".rds", f))
    pip <- rds$fit$pip
    for (j in seq_len(nrow(x))) {
      failed <- x$status[j] %in% c("failed", "timeout", "not_run")
      sel <- if (failed || is.na(x$support[j])) integer() else
        if (x$support[j] == "") integer() else as.integer(strsplit(x$support[j], ";")[[1]])
      if (failed) {
        x$tp[j] <- x$fp[j] <- x$fn[j] <- x$exact[j] <- NA
        x$error_type[j] <- "failed"
      } else {
        tp <- length(intersect(sel, act)); fp <- length(setdiff(sel, act)); fn <- s0 - tp
        x$tp[j] <- tp; x$fp[j] <- fp; x$fn[j] <- fn; x$exact[j] <- as.character(fp == 0 && fn == 0)
        x$error_type[j] <- if (fp == 0 && fn == 0) "exact" else if (fn == 0) "extra_only" else
          if (fp == 0) "missed_only" else "mixed"
      }
      for (a in seq_len(14L)) {
        x[[sprintf("sel_a%02d", a)]][j] <- if (a > s0 || failed) NA else as.character(act[a] %in% sel)
        x[[sprintf("pip_a%02d", a)]][j] <- if (a > s0 || is.null(pip)) NA else format(pip[act[a]], digits = 6)
      }
      x$max_pip_null[j] <- if (is.null(pip)) NA else format(max(pip[setdiff(seq_len(p), act)]), digits = 6)
    }
    x
  })
  S <- do.call(rbind, scored)
  utils::write.csv(S, file.path(out_dir, "dev_scored_rule_rows.csv"), row.names = FALSE)
  tab <- data.frame(dataset = S$dataset_id, method = S$method_id, rule = S$rule_id, role = S$role,
                    status = S$status, k = S$k, TP = S$tp, FP = S$fp, FN = S$fn, exact = S$exact,
                    runtime_s = sprintf("%.2f", as.numeric(S$runtime_s)), max_pip_null = S$max_pip_null,
                    stringsAsFactors = FALSE)
  tab <- tab[order(tab$method, tab$dataset, match(tab$rule, c("pip05", "cslead", "bfdr10"))), ]
  utils::write.csv(tab, file.path(out_dir, "dev_score_table.csv"), row.names = FALSE)
  print(tab, row.names = FALSE)
  invisible(tab)
}

if (sys.nframe() == 0L) {
  a <- commandArgs(trailingOnly = TRUE); stopifnot(length(a) %in% 3:4)
  main(a[1], a[2], a[3], exclude_dev = length(a) == 4L && a[4] == "--exclude_dev")
}
