# run_all.R -- W3-RM2-R boundary numerics driver (one worker process; start as many as allowed, <= 8; ramp up).
# Usage: W3RM2R_CORE=<core copy> nice -n 10 Rscript run_all.R <numerics dir>
# Each worker claims a job by an atomic mkdir in arrays/locks/ and writes arrays/rows/<job>.rds; resumable (a job with an
# .rds is skipped); a crashed worker leaves a lock without .rds (remove it by hand to re-run).
args <- commandArgs(trailingOnly = TRUE); here <- args[1]
source(file.path(here, "rm2r_common.R"))
rows <- file.path(here, "arrays", "rows"); locks <- file.path(here, "arrays", "locks")
dir.create(rows, recursive = TRUE, showWarnings = FALSE); dir.create(locks, recursive = TRUE, showWarnings = FALSE)
kappas <- c(0.5, 1, 2, 4, 8, 16, 32)
jobs <- rbind(
  expand.grid(design = "G", n = 1600, b = 0.375, kappa = kappas, seed = 1:6, stringsAsFactors = FALSE),
  expand.grid(design = "P", n = 1600, b = c(0.3, 0.45), kappa = kappas, seed = 1:6, stringsAsFactors = FALSE),
  expand.grid(design = "G", n = 400, b = 0.375, kappa = kappas, seed = 1:10, stringsAsFactors = FALSE),
  expand.grid(design = "P", n = 400, b = c(0.3, 0.45), kappa = kappas, seed = 1:10, stringsAsFactors = FALSE))
jobs$id <- sprintf("%s_n%d_b%s_k%s_s%d", jobs$design, jobs$n, jobs$b, jobs$kappa, jobs$seed)
for (i in seq_len(nrow(jobs))) {
  j <- jobs[i, ]; f <- file.path(rows, paste0(j$id, ".rds"))
  if (file.exists(f)) next
  if (!dir.create(file.path(locks, j$id), showWarnings = FALSE)) next        # claimed by another worker
  r <- tryCatch(run_one(j$design, j$n, j$b, j$kappa, j$seed, mode_margin = (j$design == "P" && j$n == 400)),
                error = function(e) data.frame(design = j$design, n = j$n, b = j$b, kappa = j$kappa, seed = j$seed,
                                               status = paste("error:", conditionMessage(e))))
  saveRDS(r, f); cat(format(Sys.time(), "%H:%M:%S"), j$id, r$status, "\n"); gc()
}
cat("worker finished\n")
