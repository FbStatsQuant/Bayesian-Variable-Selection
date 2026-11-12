# bitid_compare.R -- compare the fingerprints of two labels over every unit found in DIR (files <unit>__<label>.rec.rds).
# Verdict per unit: IDENTICAL iff the hash of the whole stripped fit agrees; otherwise the differing fields are listed.
# Usage: Rscript --vanilla bitid_compare.R DIR v31 v32 [OUT.tsv]
`%||%` <- function(a, b) if (is.null(a)) b else a
one <- function(x) if (is.null(x) || !length(x)) NA else x[[1]]
a <- commandArgs(trailingOnly = TRUE); dir <- a[1]; la <- a[2]; lb <- a[3]; out <- if (length(a) >= 4) a[4] else NA
expect <- if (length(a) >= 5) as.integer(a[5]) else NA   # expected number of units; the script fails if it differs
fa <- list.files(dir, pattern = paste0("__", la, "\\.rec\\.rds$"), full.names = TRUE)
rows <- list()
for (f in sort(fa)) {
  g <- sub(paste0("__", la, "\\.rec\\.rds$"), paste0("__", lb, ".rec.rds"), f)
  ra <- readRDS(f); unit <- ra$unit
  if (!file.exists(g)) { rows[[length(rows) + 1]] <- data.frame(unit = unit, verdict = "MISSING_B", stringsAsFactors = FALSE); next }
  rb <- readRDS(g)
  stopifnot(identical(ra$fingerprint$version, rb$fingerprint$version))
  same <- identical(ra$fingerprint$all, rb$fingerprint$all)
  nm <- union(names(ra$fingerprint$top), names(rb$fingerprint$top))
  difft <- nm[vapply(nm, function(k) !identical(unname(ra$fingerprint$top[k]), unname(rb$fingerprint$top[k])), TRUE)]
  s <- ra$scalars; t <- rb$scalars
  rows[[length(rows) + 1]] <- data.frame(unit = unit, verdict = if (same) "IDENTICAL" else "DIFFERENT",
    status_a = one(s$status), status_b = one(t$status), branch = one(s$branch), tier = one(s$tier), escalated = one(s$escalated),
    T_final = one(s$T_final), log_Z = one(s$log_Z), sd_log_Z_r = one(s$sd_log_Z_r), hpm_size = length(s$hpm), hpm_phase = one(s$hpm_phase),
    routes = paste(unlist(s$numerical_routes), collapse = "/"), routes_same = identical(s$numerical_routes, t$numerical_routes),
    start_mode_ties = one(s$start_mode_ties), near_ties = one(s$near_ties), fresh_total = one(s$fresh_total),
    n_fields = length(ra$fingerprint$top), differing_fields = paste(difft, collapse = ","),
    fp_version = one(ra$fingerprint$version), preflight_record_same = identical(ra$fingerprint$delivery, rb$fingerprint$delivery),
    admission_same = identical(ra$fingerprint$delivery$preflight$exceeds, rb$fingerprint$delivery$preflight$exceeds) &&
                     identical(ra$fingerprint$delivery$preflight_escalation$exceeds, rb$fingerprint$delivery$preflight_escalation$exceeds),
    exceeds_a = one(s$preflight_exceeds), exceeds_b = one(t$preflight_exceeds), ls0_wc_s_a = one(s$ls0_wc_seconds), ls0_wc_s_b = one(t$ls0_wc_seconds),
    wall_a = ra$wall_s, wall_b = rb$wall_s, setup_s_a = one(ra$timings$setup_total), setup_s_b = one(rb$timings$setup_total),
    stringsAsFactors = FALSE)
}
all_names <- unique(unlist(lapply(rows, names)))
tab <- do.call(rbind, lapply(rows, function(r) { for (k in setdiff(all_names, names(r))) r[[k]] <- NA; r[all_names] }))
if (!is.na(out)) write.table(tab, out, sep = "\t", quote = FALSE, row.names = FALSE)
print(tab[, intersect(c("unit", "verdict", "status_a", "status_b", "tier", "T_final", "routes", "differing_fields", "wall_a", "wall_b"), names(tab))], row.names = FALSE)
cat(sprintf("units %d  IDENTICAL %d  DIFFERENT %d  missing %d  admission decisions equal %d\n", nrow(tab), sum(tab$verdict == "IDENTICAL"),
            sum(tab$verdict == "DIFFERENT"), sum(tab$verdict == "MISSING_B"), sum(tab$admission_same %in% TRUE)))
bad <- nrow(tab) == 0 || any(tab$verdict != "IDENTICAL") || (!is.na(expect) && nrow(tab) != expect)
if (bad) { cat("COMPARE FAILED\n"); quit(status = 1) }
cat("COMPARE PASSED\n")
