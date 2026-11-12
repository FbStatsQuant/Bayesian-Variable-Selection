# bitid_compare.R -- compare the fingerprints of two labels over every unit found in DIR (files <unit>__<label>.rec.rds).
# Fail-closed (review R02 finding 1). A unit passes only if: both records exist and name the same unit; both carry a
# version-2 fingerprint with a 64-hex whole-fit hash and a non-empty field table; the two admission decisions (initial
# preflight, pre-escalation preflight) are equal; and the whole-fit hashes agree. Verdicts:
#   IDENTICAL, DIFFERENT (hashes differ), ADMISSION_DIFFERS (the versions did not take the same admission decisions:
#   outside the identity claim, reported separately), INVALID (malformed record), MISSING_A / MISSING_B (unpaired).
# Exit status 0 only if every unit is IDENTICAL, at least one unit exists, and the number of units equals EXPECT.
# Usage: Rscript --vanilla bitid_compare.R DIR LABEL_A LABEL_B OUT.tsv EXPECT
one <- function(x) if (is.null(x) || !length(x)) NA else x[[1]]
a <- commandArgs(trailingOnly = TRUE)
if (length(a) < 5) { cat("usage: bitid_compare.R DIR LABEL_A LABEL_B OUT.tsv EXPECT\n"); quit(status = 2) }
dir <- a[1]; la <- a[2]; lb <- a[3]; out <- a[4]; expect <- as.integer(a[5])
stem <- function(l) sub(paste0("__", l, "\\.rec\\.rds$"), "", list.files(dir, pattern = paste0("__", l, "\\.rec\\.rds$")))
sa <- stem(la); sb <- stem(lb)
valid_fp <- function(fp) is.list(fp) && identical(fp$version, 2L) && is.character(fp$all) && length(fp$all) == 1 && !is.na(fp$all) &&
  grepl("^[0-9a-f]{64}$", fp$all) && is.character(fp$top) && length(fp$top) >= 1 && !is.null(names(fp$top)) && is.list(fp$delivery)
# admission decisions: refused before the run, refused before an escalation, refused by the post-setup LS0 charge
adm <- function(fp) list(fp$delivery$preflight$exceeds, fp$delivery$preflight_escalation$exceeds, isTRUE(fp$delivery$preflight_ls0$exceeds))
rows <- list()
for (s in sort(union(sa, sb))) {
  fa <- file.path(dir, paste0(s, "__", la, ".rec.rds")); fb <- file.path(dir, paste0(s, "__", lb, ".rec.rds"))
  if (!file.exists(fa) || !file.exists(fb)) {
    rows[[length(rows) + 1]] <- data.frame(unit = s, verdict = if (file.exists(fa)) "MISSING_B" else "MISSING_A", stringsAsFactors = FALSE); next }
  ra <- readRDS(fa); rb <- readRDS(fb)
  ok <- valid_fp(ra$fingerprint) && valid_fp(rb$fingerprint) && is.character(ra$unit) && identical(ra$unit, rb$unit)
  if (!ok) { rows[[length(rows) + 1]] <- data.frame(unit = s, verdict = "INVALID", stringsAsFactors = FALSE); next }
  same <- identical(ra$fingerprint$all, rb$fingerprint$all)
  admission_same <- identical(adm(ra$fingerprint), adm(rb$fingerprint))
  nm <- union(names(ra$fingerprint$top), names(rb$fingerprint$top))
  difft <- nm[vapply(nm, function(k) !identical(unname(ra$fingerprint$top[k]), unname(rb$fingerprint$top[k])), TRUE)]
  sc <- ra$scalars; tc <- rb$scalars
  rows[[length(rows) + 1]] <- data.frame(unit = ra$unit, verdict = if (!admission_same) "ADMISSION_DIFFERS" else if (same) "IDENTICAL" else "DIFFERENT",
    status_a = one(sc$status), status_b = one(tc$status), branch = one(sc$branch), tier = one(sc$tier), escalated = one(sc$escalated),
    T_final = one(sc$T_final), log_Z = one(sc$log_Z), sd_log_Z_r = one(sc$sd_log_Z_r), hpm_size = length(sc$hpm), hpm_phase = one(sc$hpm_phase),
    routes = paste(unlist(sc$numerical_routes), collapse = "/"), routes_same = identical(sc$numerical_routes, tc$numerical_routes),
    start_mode_ties = one(sc$start_mode_ties), near_ties = one(sc$near_ties), fresh_total = one(sc$fresh_total),
    n_fields = length(ra$fingerprint$top), differing_fields = paste(difft, collapse = ","), hash = substr(ra$fingerprint$all, 1, 16),
    admission_same = admission_same, preflight_record_same = identical(ra$fingerprint$delivery, rb$fingerprint$delivery),
    exceeds_a = one(sc$preflight_exceeds), exceeds_b = one(tc$preflight_exceeds), ls0_wc_s_a = one(sc$ls0_wc_seconds), ls0_wc_s_b = one(tc$ls0_wc_seconds),
    core_a = substr(one(ra$core_key), 1, 12), core_b = substr(one(rb$core_key), 1, 12),
    wall_a = one(ra$wall_s), wall_b = one(rb$wall_s), setup_s_a = one(ra$timings$setup_total), setup_s_b = one(rb$timings$setup_total),
    stringsAsFactors = FALSE)
}
if (!length(rows)) { cat("COMPARE FAILED: no units\n"); quit(status = 1) }
all_names <- unique(unlist(lapply(rows, names)))
tab <- do.call(rbind, lapply(rows, function(r) { for (k in setdiff(all_names, names(r))) r[[k]] <- NA; r[all_names] }))
write.table(tab, out, sep = "\t", quote = FALSE, row.names = FALSE)
print(tab[, intersect(c("unit", "verdict", "status_a", "status_b", "tier", "T_final", "routes", "differing_fields"), names(tab))], row.names = FALSE)
v <- table(factor(tab$verdict, levels = c("IDENTICAL", "DIFFERENT", "ADMISSION_DIFFERS", "INVALID", "MISSING_A", "MISSING_B")))
cat(sprintf("units %d (expected %d)  %s\n", nrow(tab), expect, paste(names(v), v, collapse = "  ")))
bad <- any(tab$verdict != "IDENTICAL") || is.na(expect) || nrow(tab) != expect || length(unique(tab$core_a)) != 1 || length(unique(tab$core_b)) != 1 ||
       identical(unique(tab$core_a), unique(tab$core_b))
if (bad) { cat("COMPARE FAILED\n"); quit(status = 1) }
cat(sprintf("COMPARE PASSED: %d units, cores %s vs %s\n", nrow(tab), unique(tab$core_a), unique(tab$core_b)))
