#!/usr/bin/env Rscript
# merge_chunks.R STUDY LISTDIR CHUNKDIR OUT [THEORYDIR] : merges the per-chunk run_scoring.R outputs (CHUNKDIR/out_XX/; case lists in
# LISTDIR/chunk_XX.txt) into one scoring output OUT. With THEORYDIR, case_theory.csv is taken from THEORYDIR's chunks (theory pass),
# after checking that the main-fit (rep 0) accuracy rows of both passes are identical.
# recomputing every aggregate with the pipeline's own functions (tables.R, metrics_smc.R) over the FULL roster
# (build_roster in production mode: manifest x c100,c050, 6 scenarios x 100 replicates per p). Refuses unless every chunk rc is 0,
# the chunks' case ids partition the roster exactly, and the registry is identical across chunks.
a <- commandArgs(trailingOnly = TRUE); study <- a[1]; ldir <- a[2]; cdir <- a[3]; out <- a[4]; tdir <- if (length(a) >= 5) a[5] else NA_character_
A <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign"
Sys.setenv(SCORING_DIR = file.path(A, "code/scoring"))
source(file.path(A, "code/scoring/R/load_all.R"))
source_lines <- readLines(file.path(A, "code/scoring/run_scoring.R"))
eval(parse(text = source_lines[grep("^build_roster <- function", source_lines):(grep("^run_scoring <- function", source_lines) - 1L)]))
library(data.table)
chunks <- sort(sub("^chunk_([0-9]+)\\.txt$", "\\1", list.files(ldir, pattern = "^chunk_[0-9]+\\.txt$")))
rcs <- function(d) vapply(chunks, function(k) { f <- file.path(d, paste0("out_", k, ".rc")); if (file.exists(f)) trimws(readLines(f, 1L)) else "absent" }, "")
for (d in na.omit(c(cdir, tdir))) { rc <- rcs(d); if (any(rc != "0")) stop("chunks not finished/ok in ", d, ": ", paste(chunks[rc != "0"], rc[rc != "0"], collapse = "; ")) }
ro <- build_roster(study, c("c100", "c050"), partial = FALSE, expect_reps = 100L)
expected <- ro$expected
listed <- unlist(lapply(chunks, function(k) readLines(file.path(ldir, paste0("chunk_", k, ".txt")))))
if (anyDuplicated(listed) || !setequal(listed, expected$case_id)) stop("chunk case lists do not partition the roster")
rd <- function(k, f, d = cdir) { p <- file.path(d, paste0("out_", k), f); if (file.exists(p)) fread(p, na.strings = "NA") else NULL }
cat_all <- function(f, d = cdir) rbindlist(lapply(chunks, rd, f = f, d = d), fill = TRUE)
regs <- lapply(chunks, rd, f = "registry_used.csv")
if (!all(vapply(regs, function(r) isTRUE(all.equal(r, regs[[1]])), TRUE))) stop("registry differs across chunks")
# Each chunk scans the whole result roots, so its selection table also holds rows of OTHER chunks' cases, scored without their truth
# (Sol R1 finding 1). Keep only the rows of the chunk's own cases, before concatenation.
own <- function(dt, k) { if (is.null(dt) || !nrow(dt)) return(dt); ids <- readLines(file.path(ldir, paste0("chunk_", k, ".txt"))); dt[case_id %in% ids] }
cat_own <- function(f, d = cdir) rbindlist(lapply(chunks, function(k) own(rd(k, f, d), k)), fill = TRUE)
acc <- cat_own("case_smc_accuracy.csv"); sel <- cat_own("case_selection.csv"); ref <- cat_own("case_reference.csv")
thy <- cat_own("case_theory.csv"); stab <- cat_own("case_stability.csv"); exd <- unique(cat_all("exact_diagnostics.csv")); dup <- unique(cat_all("duplicates.csv"))
rost <- cat_all("roster.csv")
theory_check <- "theory from the same pass"
if (!is.na(tdir)) {
  thy <- cat_own("case_theory.csv", d = tdir); accT <- cat_own("case_smc_accuracy.csv", d = tdir)
  x <- acc[rep == 0L][order(case_id)]; y <- accT[rep == 0L][order(case_id)]
  if (!identical(names(x), names(y)) || nrow(x) != nrow(y) || !isTRUE(all.equal(as.data.frame(x), as.data.frame(y), check.attributes = FALSE)))
    stop("main-fit accuracy rows differ between the stability pass and the theory pass")
  theory_check <- sprintf("theory from %s; main-fit accuracy rows identical across passes (%d rows)", tdir, nrow(x))
}
# in_expected was computed per chunk against the chunk roster; recompute against the full roster (same result when the partition holds)
if ("in_expected" %in% names(sel)) sel[, in_expected := case_id %in% expected$case_id]
for (nm in c("ok", "has_exact")) if (nm %in% names(acc)) acc[, (nm) := as.logical(get(nm))]
stopifnot(!anyDuplicated(acc[rep == 0L, case_id]), !anyDuplicated(ref$case_id), nrow(ref) == nrow(expected), setequal(rost$case_id, expected$case_id))
# key assertions (Sol R1 finding 1 and the review note on stronger checks)
if (anyDuplicated(acc[, .(case_id, rep)])) stop("duplicate (case_id, rep) in accuracy rows")
if (nrow(thy) && (anyDuplicated(thy$case_id) || !setequal(thy$case_id, expected$case_id))) stop("theory rows do not cover the roster exactly once")
if (nrow(stab) && anyDuplicated(stab$case_id)) stop("duplicate case_id in stability rows")
if (anyDuplicated(sel[, .(case_id, method_id, rule_id)])) stop("duplicate (case_id, method_id, rule_id) in selection rows")
req <- regs[[1]][required == TRUE, .(method_id, rule_id)]
cov <- merge(CJ(case_id = expected$case_id, k = seq_len(nrow(req)))[, `:=`(method_id = req$method_id[k], rule_id = req$rule_id[k])][, k := NULL],
             unique(sel[, .(case_id, method_id, rule_id, hit = TRUE)]), by = c("case_id", "method_id", "rule_id"), all.x = TRUE)
if (any(is.na(cov$hit))) stop("selection rows miss ", sum(is.na(cov$hit)), " roster x required-registry keys")
dir.create(out, recursive = TRUE, showWarnings = FALSE)
W <- function(dt, f) if (!is.null(dt) && nrow(dt)) write_csv_na(dt, file.path(out, f))
W(expected, "roster.csv"); W(ref, "case_reference.csv"); W(acc, "case_smc_accuracy.csv"); W(sel, "case_selection.csv"); W(thy, "case_theory.csv")
W(stab, "case_stability.csv"); W(exd, "exact_diagnostics.csv"); W(dup, "duplicates.csv"); W(regs[[1]], "registry_used.csv")
W(flag_error_table(acc), "flag_error_2x2.csv"); W(se_calibration_table(acc), "se_calibration.csv")
H1 <- H1_logZ(acc, expected, ref); H2 <- H2_hpm(acc, expected, ref); H3 <- H3_pip(acc, expected, ref); H4 <- H4_recovery(sel)
W(H1, "H1_logZ.csv"); W(H2, "H2_hpm.csv"); W(H3, "H3_pip.csv"); W(H4, "H4_recovery.csv")
note <- sprintf("Roster: %s; %d datasets x 2 scales = %d cases; merged from %d chunks. Planned grid verified (6 scenarios x 100 replicates per p).",
                ro$mode, length(unique(expected$dataset_id)), nrow(expected), length(chunks))
write_headline(H1, H2, H3, H4, file.path(out, "HEADLINE.md"), roster_note = note)
logs <- unlist(lapply(chunks, function(k) c(paste0("## chunk ", k), readLines(file.path(cdir, paste0("out_", k), "SCORING_LOG.txt")))))
writeLines(c(paste("merge", format(Sys.time(), tz = "UTC", usetz = TRUE), "chunks", length(chunks), "cases", nrow(expected),
                   "acc rows", nrow(acc), "theory rows", nrow(thy), "stability rows", nrow(stab)), theory_check, logs), file.path(out, "SCORING_LOG.txt"))
cat(theory_check, "\n")
cat("MERGE_OK cases", nrow(expected), "acc", nrow(acc), "theory", nrow(thy), "stability", nrow(stab), "selection", nrow(sel), "\n")
