# check_own_filter.R WORKDIR LISTDIR : after run_scoring.R has scored chunk_00 and chunk_01 with the synthetic benchmark root into
# WORKDIR/out_00 and WORKDIR/out_01, shows (a) the unfiltered concatenation duplicates benchmark keys with conflicting outcomes (the bug)
# and (b) the merge_chunks.R own-chunk filter keeps each key once, scored with its own truth.
library(data.table)
a <- commandArgs(trailingOnly = TRUE); w <- a[1]; ldir <- a[2]
rd <- function(k) fread(file.path(w, paste0("out_", k), "case_selection.csv"), na.strings = "NA")
own <- function(dt, k) { ids <- readLines(file.path(ldir, paste0("chunk_", k, ".txt"))); dt[case_id %in% ids] }  # same as merge_chunks.R
syn <- c("p0020_S1_r001_c050", "p0020_S1_r051_c050"); bm <- c("F1", "F2", "F3", "F4", "F5", "A1", "A2", "A3")
raw <- rbindlist(list(rd("00"), rd("01")), fill = TRUE)[case_id %in% syn & method_id %in% bm & status != "not_run"]
fil <- rbindlist(list(own(rd("00"), "00"), own(rd("01"), "01")), fill = TRUE)[case_id %in% syn & method_id %in% bm & status != "not_run"]
kr <- raw[, .N, by = .(case_id, method_id, rule_id)]; kf <- fil[, .N, by = .(case_id, method_id, rule_id)]
conf <- raw[, .(n_outcomes = uniqueN(paste(exact, error_type))), by = .(case_id, method_id, rule_id)][n_outcomes > 1]
cat("UNFILTERED: rows", nrow(raw), "keys", nrow(kr), "max copies per key", max(kr$N), "keys with conflicting outcomes", nrow(conf), "\n")
cat("FILTERED:   rows", nrow(fil), "keys", nrow(kf), "max copies per key", max(kf$N), "failed rows", sum(fil$error_type == "failed"), "\n")
cat("FILTERED exact recoveries by case:\n"); print(fil[, .(n_rules = .N, n_exact = sum(exact == TRUE)), by = case_id])
ok <- nrow(raw) > nrow(fil) && max(kf$N) == 1L && nrow(kf) == nrow(kr) && sum(fil$error_type == "failed") == 0L
cat(if (ok) "TEST_PASS" else "TEST_FAIL", "\n"); quit(status = if (ok) 0L else 1L)
