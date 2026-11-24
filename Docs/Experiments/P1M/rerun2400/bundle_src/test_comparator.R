#!/usr/bin/env Rscript
# test_comparator.R -- fabricated OLD/NEW pairs with 3 planted differences (+ 2 benign, disclosed-only controls) and a data-sha / missing-record check.
# Usage: Rscript test_comparator.R  (writes to a temp dir; exits 0 iff the comparator flags exactly what was planted)
here <- dirname(normalizePath(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])))
tmp <- tempfile("cmp_test_"); dir.create(tmp)
RUN <- "rr_test"
mk_fit <- function(seed, status = "completed") {
  set.seed(seed); q <- runif(6); names(q) <- as.character(c(2, 5, 9, 11, 14, 20))
  list(status = status, log_Z = -100 - runif(1), log_Z_r = -100 - runif(4), hpm = c(5L, 9L), hpm_F = -90 - runif(1), pip_primary = q,
       pip_r = matrix(runif(12), 6, 2, dimnames = list(names(q), NULL)), peak_memory_kb = 300000 + 1000 * seed %% 7,
       ls0_improved = FALSE, ls0_hpm_changed = FALSE)
}
write_pair <- function(case_id, old, new, rt_old, rt_new, host_new = "nodeA", xs_new = NULL, drop_new = FALSE) {
  p <- as.integer(substr(case_id, 2, 5)); xs <- paste0("x", case_id); ys <- paste0("y", case_id)
  d1 <- file.path(tmp, "old", "results", RUN, sprintf("p%04d", p), case_id); dir.create(d1, recursive = TRUE)
  saveRDS(list(fit = old, runtime_s = rt_old, input = list(x_sha256 = xs, y_sha256 = ys), environment = list(host = "nodeA")), file.path(d1, "SMCBVS.rds"))
  if (drop_new) return(invisible())
  d2 <- file.path(tmp, "new", "results", RUN, sprintf("p%04d", p), case_id); dir.create(d2, recursive = TRUE)
  saveRDS(list(fit = new, runtime_s = rt_new, x_sha256 = if (is.null(xs_new)) xs else xs_new, y_sha256 = ys, host = host_new), file.path(d2, "NEWFIT.rds"))
}
cases <- expand.grid(p = c(500, 1000), c = c("c100", "c050"), S = 1:2, r = c(1, 25, 50), stringsAsFactors = FALSE)
PLANT <- list(A = "p0500_S1_r025_c100", B = "p1000_S1_r001_c100", C_cell = "p1000_S2_c050")
for (i in seq_len(nrow(cases))) {
  cs <- cases[i, ]; id <- sprintf("p%04d_S%d_r%03d_%s", cs$p, cs$S, cs$r, cs$c)
  old <- mk_fit(i); new <- old
  rt_old <- (if (cs$p == 500) 650 else 1800) * (1 + 0.01 * i); rt_new <- rt_old * (1 + 0.02 * ((i %% 3) - 1))   # +-2% noise
  if (id == PLANT$A) new$log_Z <- new$log_Z + 1e-13                                   # planted 1: one-ulp-scale difference on a completed fit
  if (id == PLANT$B) { new$status <- "resource_limit"; rt_new <- 24000 }                  # planted 2: completed -> stopped
  if (cs$p == 1000 && cs$S == 2 && cs$c == "c050") rt_new <- rt_old * 1.6                  # planted 3: runtime blow-up of one cell
  if (id == "p0500_S2_r050_c050") { new$hpm <- c(5L, 9L, 14L); new$hpm_F <- old$hpm_F + 0.5; new$ls0_improved <- TRUE; new$ls0_hpm_changed <- TRUE }  # benign
  if (id == "p1000_S1_r025_c050") { old$status <- "resource_limit"; old$log_Z <- NULL }   # benign: stopped -> completed
  write_pair(id, old, new, rt_old, rt_new)
}
run_cmp <- function(out) system2("Rscript", c("--vanilla", file.path(here, "comparator.R"), "--old-root", file.path(tmp, "old"), "--new-root", file.path(tmp, "new"),
  "--run-id", RUN, "--out", out), stdout = FALSE, stderr = FALSE)
st <- run_cmp(file.path(tmp, "out1"))
pf <- read.csv(file.path(tmp, "out1", "per_fit.csv"), stringsAsFactors = FALSE, na.strings = ""); vd <- read.csv(file.path(tmp, "out1", "verdict.csv"), stringsAsFactors = FALSE)
ok <- TRUE; chk <- function(cond, msg) { cat(if (cond) "PASS  " else "FAIL  ", msg, "\n", sep = ""); if (!cond) ok <<- FALSE }
chk(st == 1L, "exit status 1 (regression found)")
chk(nrow(pf) == 24L, "24 fit pairs read")
chk(setequal(pf$case_id[!pf$fit_pass], c(PLANT$A, PLANT$B)), "failed fits are exactly the two planted fit-level differences")
chk(grepl("legacy_differs:log_Z", pf$fails[pf$case_id == PLANT$A]), "planted 1 (log_Z last-bit) detected as legacy_differs:log_Z")
chk(grepl("completed_to_stopped", pf$fails[pf$case_id == PLANT$B]), "planted 2 detected as completed_to_stopped")
chk(grepl("ls0_improved_hpm_gain", pf$disclosed[pf$case_id == "p0500_S2_r050_c050"]) && pf$fit_pass[pf$case_id == "p0500_S2_r050_c050"], "benign ls0 HPM gain disclosed, not failed")
chk(grepl("stopped_to_completed", pf$disclosed[pf$case_id == "p1000_S1_r025_c050"]) && pf$fit_pass[pf$case_id == "p1000_S1_r025_c050"], "benign stopped->completed disclosed, not failed")
v <- function(p, c) vd[vd$p == p & vd$c == c, ]
chk(!v(500, "c100")$pass && v(500, "c100")$n_legacy_differs == 1, "row p500 c100 fails on 1 legacy difference")
chk(!v(1000, "c100")$pass && v(1000, "c100")$n_completed_to_stopped == 1, "row p1000 c100 fails on completed->stopped")
chk(!v(1000, "c050")$pass && v(1000, "c050")$n_cells_over_tol == 1 && v(1000, "c050")$rt_worst_cell == "S2", "row p1000 c050 fails on the planted S2 runtime cell (ratio 1.6)")
chk(v(500, "c050")$pass && v(500, "c050")$n_ls0_hpm_gain_disclosed == 1, "row p500 c050 passes with the disclosed ls0 gain")
# second run: data-sha mismatch + a missing NEW record are failures too
write_pair("p0500_S3_r001_c100", mk_fit(99), mk_fit(99), 600, 600, xs_new = "different")
write_pair("p0500_S3_r001_c050", mk_fit(98), mk_fit(98), 600, 600, drop_new = TRUE)
st2 <- run_cmp(file.path(tmp, "out2"))
pf2 <- read.csv(file.path(tmp, "out2", "per_fit.csv"), stringsAsFactors = FALSE, na.strings = "")
chk(grepl("data_sha_mismatch", pf2$fails[pf2$case_id == "p0500_S3_r001_c100"]), "x-sha mismatch detected")
chk(grepl("missing_new", pf2$fails[pf2$case_id == "p0500_S3_r001_c050"]), "missing NEW record detected")
# clean run: remove the planted differences -> NO REGRESSION, exit 0
unlink(file.path(tmp, c("old", "new", "out1", "out2")), recursive = TRUE)
for (i in seq_len(nrow(cases))) { cs <- cases[i, ]; id <- sprintf("p%04d_S%d_r%03d_%s", cs$p, cs$S, cs$r, cs$c); f <- mk_fit(i)
  write_pair(id, f, f, 650, 650 * 1.03) }
st3 <- run_cmp(file.path(tmp, "out3"))
chk(st3 == 0L, "clean pairs -> exit 0 (NO REGRESSION)")
cat(if (ok) "ALL TESTS PASSED\n" else "TESTS FAILED\n"); unlink(tmp, recursive = TRUE); quit(status = if (ok) 0L else 1L)
