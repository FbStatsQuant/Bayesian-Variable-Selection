# prodh_repro_check.R OLD_ROOT NEW_ROOT RECONCILE_TSV OUT_DIR
# PROD-H reproduction spot-check (HQ D51 step 5): the frozen v2.2.1 core and the adapter's seeds are the same as the 2026-10-23 production, so the
# reproduced fits must be identical. Sample (fixed, not data-driven): p in {500,1000} x S1..S6 x replicates {1,25,50,75,100} x {c100,c050} = 120 fits,
# plus every case that is resource_limit in the new reconcile. For each: identical() of fit$log_Z (Z-hat), fit$log_Z_r, fit$hpm, fit$pip_primary,
# fit$pip_r, record$pip, and record$native_status; max |diff| for numeric fields. Any mismatch is a DEFECT (reported, not fixed).
a <- commandArgs(trailingOnly = TRUE)
old_root <- a[1]; new_root <- a[2]; rec <- a[3]; out <- a[4]
dir.create(out, showWarnings = FALSE, recursive = TRUE)
grid <- expand.grid(p = c(500L, 1000L), s = 1:6, r = c(1L, 25L, 50L, 75L, 100L), c = c("c100", "c050"), stringsAsFactors = FALSE)
ids <- sprintf("p%04d_S%d_r%03d_%s", grid$p, grid$s, grid$r, grid$c)
rt <- utils::read.delim(rec, stringsAsFactors = FALSE)
rl <- rt$case_id[rt$outcome == "resource_limit"]
ids <- unique(c(ids, rl))
pf <- function(id) sprintf("p%s", substr(id, 2, 5))
fields <- c("log_Z", "log_Z_r", "hpm", "pip_primary", "pip_r")
res <- lapply(ids, function(id) {
  o <- file.path(gsub("{p}", pf(id), old_root, fixed = TRUE), pf(id), id, "SMCBVS.rds"); n <-file.path(new_root, pf(id), id, "SMCBVS.rds")
  if (!file.exists(o) || !file.exists(n)) return(data.frame(case_id = id, field = "FILE", identical = FALSE, max_abs_diff = NA, note = paste("missing", if (!file.exists(o)) "old" else "", if (!file.exists(n)) "new" else "")))
  ro <- readRDS(o); rn <- readRDS(n)
  rows <- lapply(fields, function(f) { x <- ro$fit[[f]]; y <- rn$fit[[f]]
    d <- if (is.numeric(x) && is.numeric(y) && length(x) == length(y)) suppressWarnings(max(abs(as.double(x) - as.double(y)), 0, na.rm = TRUE)) else NA
    data.frame(case_id = id, field = paste0("fit$", f), identical = identical(x, y), max_abs_diff = d, note = "") })
  x <- ro$pip; y <- rn$pip
  rows[[length(rows) + 1]] <- data.frame(case_id = id, field = "pip", identical = identical(unname(x), unname(y)),
    max_abs_diff = if (is.numeric(x) && length(x) == length(y)) max(abs(x - y), 0) else NA, note = "")
  rows[[length(rows) + 1]] <- data.frame(case_id = id, field = "native_status", identical = identical(ro$native_status, rn$native_status),
    max_abs_diff = NA, note = paste(ro$native_status, "->", rn$native_status))
  do.call(rbind, rows)
})
tab <- do.call(rbind, res)
utils::write.table(tab, file.path(out, "repro_check_detail.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)
by_field <- aggregate(identical ~ field, data = tab, FUN = function(v) sprintf("%d/%d", sum(v), length(v)))
bad <- unique(tab$case_id[!tab$identical])
cat(sprintf("PROD-H reproduction spot-check: %d cases (%d sampled + %d resource_limit), %d field comparisons\n", length(ids), nrow(grid), length(rl), nrow(tab)))
print(by_field, row.names = FALSE)
cat(sprintf("cases with any mismatch: %d %s\n", length(bad), paste(head(bad, 20), collapse = " ")))
cat(sprintf("max |diff| over numeric fields: %s\n", format(max(tab$max_abs_diff, na.rm = TRUE))))
cat(if (length(bad) == 0) "VERDICT: IDENTICAL\n" else "VERDICT: MISMATCH (defect; report to HQ)\n")
