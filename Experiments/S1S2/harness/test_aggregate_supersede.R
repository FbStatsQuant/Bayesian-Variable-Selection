# test_aggregate_supersede.R -- offline test of harness/aggregate.R's record rules (temp folders only; no NOTS, no real runs).
#   Rscript harness/test_aggregate_supersede.R        (exit 0 = all pass)
# 1 a batch-1 timeout stub for (S1_08, rep 12), no rerun: counts as 1 computational failure (never dropped).
# 2 an ok rerun "pulled" over the stub with the rsync call of slurm/pull_to_owls.sh (--backup --backup-dir=_superseded/<ts>):
#   aggregate counts 1 ok record and 0 computational failures, and the stub is preserved under _superseded/<ts>/.
# 3 --final refuses while the stub's array task (json slurm_job) is in the (fake) queue (--queue-file), and runs when it
#   is not (the stub then counts as a computational failure).
# 4 refusals: a json whose rep differs from its path; two jsons for one rep; --out inside _superseded/.
BASE <- local({ f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)); normalizePath(file.path(dirname(f), "..")) })
AGG <- file.path(BASE, "harness", "aggregate.R")
suppressPackageStartupMessages(library(jsonlite))
tmp <- tempfile("agg_supersede_"); dir.create(tmp); on.exit(unlink(tmp, recursive = TRUE), add = TRUE)
nfail <- 0
check <- function(ok, what) { cat(if (isTRUE(ok)) "PASS" else "FAIL", what, "\n"); if (!isTRUE(ok)) nfail <<- nfail + 1 }
run_agg <- function(out, tag, ...) {   # returns list(status, output, row of S1_08)
  sp <- file.path(tmp, paste0("specs_", tag)); dir.create(sp, showWarnings = FALSE)
  o <- suppressWarnings(system2("Rscript", c(AGG, "--out", out, "--method", "smcbvs", "--suite", "1", "--specs", sp,
                                             "--dest", file.path(sp, "succ.tsv"), ...), stdout = TRUE, stderr = TRUE))
  st <- attr(o, "status") %||% 0L
  f <- file.path(sp, "results_S1_smcbvs.tsv")
  row <- if (st == 0 && file.exists(f)) { d <- read.delim(f, stringsAsFactors = FALSE); d[d$setting_id == "S1_08", ] } else NULL
  list(status = st, out = o, row = row)
}
stub <- list(setting_id = "S1_08", method = "smcbvs", rep = 12L, status = "failed: harness wall timeout 42900s",
             host = "bb3u20c1", slurm_job = "2902188_712")
okrec <- list(setting_id = "S1_08", method = "smcbvs", rep = 12L, status = "ok", suite = 1L, s0 = 10L, support = 1:10,
              data_md5 = "0123456789abcdef0123456789abcdef", selected = 1:10, n_selected = 10L, TP = 10L, FP = 0L, FN = 0L,
              success = TRUE, runtime_sec = 1.5, wall_sec_harness = 2)
put <- function(root, x) { d <- file.path(root, "smcbvs", x$setting_id); dir.create(d, recursive = TRUE, showWarnings = FALSE)
  f <- file.path(d, sprintf("rep_%03d.json", x$rep)); write_json(x, f, auto_unbox = TRUE, pretty = TRUE); f }

## 1 stub only: one computational failure
runsA <- file.path(tmp, "runsA"); invisible(put(runsA, stub))
r <- run_agg(runsA, "A")
check(r$status == 0, "1 aggregate runs on the stub-only folder")
check(!is.null(r$row) && r$row$n_records == 1 && r$row$n_ok == 0 && r$row$n_failed == 1 && r$row$n_computational == 1 && r$row$n_missing == 99,
      "1 stub = 1 record, 0 ok, 1 failed, 1 computational failure, 99 missing")
check(!is.null(r$row) && r$row$FN_mean == 10 && r$row$TP_mean == 0 && r$row$F1_mean == 0 && r$row$hamming_mean == 10,
      "1 failed / missing count as S-hat = {} (FN = s0 = 10, TP = 0, F1 = 0)")

## 2 ok rerun pulled over the stub (pull_to_owls.sh step 2: rsync -a --files-from --backup --backup-dir=_superseded/<ts>)
runsB <- file.path(tmp, "runsB"); stubB <- put(runsB, stub); stub_bytes <- readLines(stubB)
src <- file.path(tmp, "nots"); invisible(put(src, okrec))
ts <- format(Sys.time(), "%Y%m%dT%H%M%SZ", tz = "UTC"); lst <- file.path(tmp, "list"); writeLines("smcbvs/S1_08/rep_012.json", lst)
rs <- system2("rsync", c("-a", paste0("--files-from=", lst), "--backup", paste0("--backup-dir=_superseded/", ts), paste0(src, "/"), paste0(runsB, "/")))
check(rs == 0, "2 rsync pull with --backup-dir=_superseded/<ts> succeeded")
sup <- file.path(runsB, "_superseded", ts, "smcbvs", "S1_08", "rep_012.json")
check(file.exists(sup) && identical(readLines(sup), stub_bytes), "2 the stub is preserved byte-for-byte under _superseded/<ts>/")
check(identical(fromJSON(file.path(runsB, "smcbvs", "S1_08", "rep_012.json"))$status, "ok"), "2 the live record is the ok rerun")
r <- run_agg(runsB, "B")
check(r$status == 0, "2 aggregate runs after the pull")
check(!is.null(r$row) && r$row$n_records == 1 && r$row$n_ok == 1 && r$row$n_failed == 0 && r$row$n_computational == 0 && r$row$successes == 1,
      "2 aggregate counts 1 ok record, 0 failed, 0 computational failures (the superseded stub is not read)")
check(!is.null(r$row) && abs(r$row$TP_mean - 0.1) < 1e-12 && abs(r$row$FN_mean - 9.9) < 1e-12 && abs(r$row$F1_mean - 0.01) < 1e-12,
      "2 appended means: TP 0.1, FN 9.9 (99 missing = S-hat {}), F1 0.01")

## 3 --final with a fake queue
q_live <- file.path(tmp, "queue_live"); writeLines(c("2902188_700", "2902188_712", "2999999"), q_live)
q_done <- file.path(tmp, "queue_done"); writeLines(c("2902188_700", "2999999"), q_done)
r <- run_agg(runsA, "C1", "--final", "--queue-file", q_live)
check(r$status != 0 && any(grepl("--final refused", r$out)), "3 --final refuses: the stub's task 2902188_712 is still queued")
r <- run_agg(runsA, "C2", "--final", "--queue-file", q_done)
check(r$status == 0 && !is.null(r$row) && r$row$n_computational == 1, "3 --final runs once the task has left the queue; the stub = 1 computational failure")
r <- run_agg(runsB, "C3", "--final", "--queue-file", q_live)
check(r$status == 0 && !is.null(r$row) && r$row$n_ok == 1, "3 --final runs after the rerun replaced the stub (only _superseded holds it)")

## 4 refusals
runsD <- file.path(tmp, "runsD"); bad <- okrec; bad$rep <- 13L; f <- put(runsD, bad); invisible(file.rename(f, sub("rep_013", "rep_012", f)))
r <- run_agg(runsD, "D1"); check(r$status != 0 && any(grepl("identity mismatch", r$out)), "4 a json whose rep differs from its path stops aggregate")
runsE <- file.path(tmp, "runsE"); f <- put(runsE, okrec); invisible(file.copy(f, sub("rep_012", "rep_12", f)))
r <- run_agg(runsE, "E1"); check(r$status != 0 && any(grepl("duplicate records", r$out)), "4 two jsons for one (setting, rep) stop aggregate")
r <- run_agg(file.path(runsB, "_superseded", ts), "F1"); check(r$status != 0 && any(grepl("_superseded or audit", r$out)), "4 --out inside _superseded/ is refused")

cat(if (nfail) sprintf("%d FAILED\n", nfail) else "ALL PASS\n")
quit(status = if (nfail) 1 else 0)
