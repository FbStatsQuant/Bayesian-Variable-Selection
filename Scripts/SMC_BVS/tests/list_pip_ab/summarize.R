# summarize.R <out_new_dir> <summary.tsv>: one row per unit of the A1/A2 comparison (ab_run.R new), and the totals.
a <- commandArgs(TRUE); d <- a[1]; outtsv <- a[2]
fs <- sort(list.files(d, pattern = "\\.new\\.rds$", full.names = TRUE))
rows <- lapply(fs, function(f) { r <- readRDS(f)
  data.frame(unit = sub("\\.new\\.rds$", "", basename(f)), status_old = r$status_old, status_new = r$status_new, identical = r$identical_stripped,
             fingerprint_equal = r$fingerprint_equal, names_order_same = r$names_order_same, attributes_same = r$attributes_same,
             element_attributes_same = r$element_attributes_same, new_fields_last = r$new_fields_last,
             fields = if (length(r$new_fields_present)) paste0(length(r$new_fields_present), " of 7") else "none (status path)",
             flag = if (is.null(r$new$pip_list_flag)) "-" else r$new$pip_list_flag,
             log_Z_list = if (is.null(r$new$log_Z_list)) NA else signif(r$new$log_Z_list, 12), list_size = if (is.null(r$new$list_size)) NA else r$new$list_size,
             list_full = if (is.null(r$new$list_full)) NA else r$new$list_full, source = if (is.null(r$new$pip_list_source)) "-" else r$new$pip_list_source,
             stringsAsFactors = FALSE) })
t <- do.call(rbind, rows)
write.table(t, outtsv, sep = "\t", quote = FALSE, row.names = FALSE)
print(t, row.names = FALSE)
ok <- t$identical & t$fingerprint_equal & t$names_order_same & t$attributes_same & t$element_attributes_same & t$new_fields_last
cat(sprintf("\n%d units; all checks passed: %d; identical: %d; fingerprint equal: %d; names/order: %d; attributes: %d; element attributes: %d; new fields last: %d\n",
            nrow(t), sum(ok), sum(t$identical), sum(t$fingerprint_equal), sum(t$names_order_same), sum(t$attributes_same), sum(t$element_attributes_same), sum(t$new_fields_last)))
