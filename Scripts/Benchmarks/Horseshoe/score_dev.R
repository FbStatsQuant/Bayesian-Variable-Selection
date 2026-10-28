#!/usr/bin/env Rscript
# Scoring step for the A3 dev test (master §IV.1.2: truth columns are filled by scoring only;
# §III.3.8 e step 3 and h: crn_mismatch is set here). The only A3 script that reads truth.
# Writes scored copies; the fit files are never modified.
# Usage: Rscript score_dev.R --outroot <dir> --run-id <id> --truth-root <dev/truth>

# crn_mismatch: the rng_after values of the non-failed A3 fits of one dataset (all scales) must
# be identical. A fit whose MCMC succeeded has rng_after on every rule row (also on a km2 row
# that failed at the rule level); failed fits have rng_after = NA and are left out. The flag
# is method-wide, so it is set on every rule row of every non-failed fit of the dataset.
flag_crn <- function(rows) {
  rows$crn_mismatch <- FALSE
  for (ds in unique(rows$dataset_id)) {
    j <- rows$dataset_id == ds & !is.na(rows$rng_after)
    if (length(unique(rows$rng_after[j])) > 1L) {
      rows$crn_mismatch[j] <- TRUE
      rows$diag_flag[j] <- TRUE
      rows$diag_codes[j] <- ifelse(is.na(rows$diag_codes[j]) | rows$diag_codes[j] == "", "crn_mismatch",
                                   paste0(rows$diag_codes[j], ";crn_mismatch"))
    }
  }
  rows
}

main <- function(args) {
  kv <- setNames(args[c(FALSE, TRUE)], sub("^--", "", args[c(TRUE, FALSE)]))
  res_dir <- file.path(kv[["outroot"]], "results", kv[["run-id"]])
  csvs <- list.files(res_dir, pattern = "^A3\\.csv$", recursive = TRUE, full.names = TRUE)
  if (!length(csvs)) stop("no A3 CSVs under ", res_dir)
  rows <- do.call(rbind, lapply(csvs, function(f)
    utils::read.csv(f, stringsAsFactors = FALSE, colClasses = c(support = "character", support_audit = "character"))))

  rows <- flag_crn(rows)

  truth_cache <- list()
  for (i in seq_len(nrow(rows))) {
    ds <- rows$dataset_id[i]
    if (is.null(truth_cache[[ds]]))
      truth_cache[[ds]] <- readRDS(file.path(kv[["truth-root"]], sprintf("p%04d", rows$p[i]), paste0(ds, ".rds")))
    act <- truth_cache[[ds]]$active
    if (rows$status[i] %in% c("failed", "timeout", "not_run")) {
      rows$error_type[i] <- "failed"
      rows$exact[i] <- FALSE
      next
    }
    sel <- if (rows$support[i] == "") integer(0) else as.integer(strsplit(rows$support[i], ";")[[1]])
    rows$tp[i] <- sum(sel %in% act); rows$fp[i] <- sum(!(sel %in% act)); rows$fn[i] <- sum(!(act %in% sel))
    rows$exact[i] <- rows$fp[i] == 0 && rows$fn[i] == 0
    rows$error_type[i] <- if (rows$exact[i]) "exact" else if (rows$fn[i] == 0) "extra_only" else
      if (rows$fp[i] == 0) "missed_only" else "mixed"
    for (a in seq_along(act)) rows[[sprintf("sel_a%02d", a)]][i] <- act[a] %in% sel
  }
  od <- file.path(kv[["outroot"]], "score", kv[["run-id"]]); dir.create(od, recursive = TRUE, showWarnings = FALSE)
  utils::write.csv(rows, file.path(od, "scored_rows.csv"), row.names = FALSE, na = "NA")
  tab <- data.frame(dataset = rows$dataset_id, rule = rows$rule_id, status = rows$status, k = rows$k,
                    TP = rows$tp, FP = rows$fp, FN = rows$fn, exact = rows$exact,
                    error_type = rows$error_type, diag_flag = rows$diag_flag, diag_codes = rows$diag_codes,
                    runtime_s = round(rows$runtime_s, 1), stringsAsFactors = FALSE)
  tab <- tab[order(tab$rule != "ci95", tab$dataset), ]
  utils::write.csv(tab, file.path(od, "dev_score_table.csv"), row.names = FALSE, na = "NA")
  print(tab, row.names = FALSE)
  for (r in unique(tab$rule)) cat(sprintf("%s: exact %d of %d\n", r, sum(tab$exact[tab$rule == r]), sum(tab$rule == r)))
  0L
}

if (sys.nframe() == 0L) quit(save = "no", status = main(commandArgs(trailingOnly = TRUE)))
