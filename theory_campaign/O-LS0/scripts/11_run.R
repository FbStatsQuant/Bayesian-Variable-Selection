# 11_run.R -- run LS0 (10_ls0_fit.R) over a list of (p, scenario, replicate, scale) fits; one RDS per fit, resumable.
# Usage: Rscript 11_run.R <STUDY root> <OUT dir> <task spec> [shard] [nshards]
#   task spec: "pilot" = r = 1 for every p x scenario, both scales (24 fits);
#              "full"  = all 1,200 datasets x {c100, c050} (2,400 fits);
#              or a CSV with columns p, scenario, replicate, scale_key.
#   shard/nshards: this process runs tasks i with (i - 1) %% nshards == shard - 1 (default 1 of 1).
# Environment: LS0_WORK (testing copy of the core, default /home/fb31/ls0_work), LS0_LAT_MAX (lattice cap, default 64).
args <- commandArgs(TRUE)
study <- args[1]; out <- args[2]; spec <- args[3]
shard <- if (length(args) >= 4) as.integer(args[4]) else 1L
nshards <- if (length(args) >= 5) as.integer(args[5]) else 1L
sd <- dirname(normalizePath(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1])))
source(file.path(sd, "ls0_core.R"))
ls0_load()
source(file.path(sd, "10_ls0_fit.R"))
scales <- c("c100", "c050")
tasks <- if (spec == "pilot") {
  expand.grid(scale_key = scales, replicate = 1L, scenario = 1:6, p = c(500L, 1000L), stringsAsFactors = FALSE)
} else if (spec == "full") {
  expand.grid(scale_key = scales, replicate = 1:100, scenario = 1:6, p = c(500L, 1000L), stringsAsFactors = FALSE)
} else read.csv(spec, stringsAsFactors = FALSE)
tasks <- tasks[, c("p", "scenario", "replicate", "scale_key")]
mine <- tasks[(seq_len(nrow(tasks)) - 1L) %% nshards == shard - 1L, , drop = FALSE]
dir.create(out, recursive = TRUE, showWarnings = FALSE)
logf <- file.path(out, sprintf("run_shard%02d.log", shard))
cat(sprintf("%s shard %d/%d: %d tasks, R %s, BLAS threads %s\n", format(Sys.time()), shard, nshards, nrow(mine),
            R.version.string, Sys.getenv("OPENBLAS_NUM_THREADS")), file = logf, append = TRUE)
cur <- ""; inp <- tru <- NULL
for (i in seq_len(nrow(mine))) {
  t <- mine[i, ]
  id <- sprintf("p%04d_S%d_r%03d", t$p, t$scenario, t$replicate)
  f <- file.path(out, sprintf("p%04d", t$p), paste0(id, "_", t$scale_key, ".rds"))
  if (file.exists(f)) next
  if (id != cur) {
    inp <- readRDS(file.path(study, "inputs", sprintf("p%04d", t$p), paste0(id, ".rds")))
    tru <- readRDS(file.path(study, "truth", sprintf("p%04d", t$p), paste0(id, ".rds")))
    cur <- id
  }
  r <- tryCatch(ls0_one(inp, tru, t$scale_key), error = function(e) e)
  if (inherits(r, "error")) {
    cat(sprintf("%s ERROR %s %s: %s\n", format(Sys.time()), id, t$scale_key, conditionMessage(r)), file = logf, append = TRUE)
    next
  }
  dir.create(dirname(f), recursive = TRUE, showWarnings = FALSE)
  saveRDS(r, paste0(f, ".tmp")); file.rename(paste0(f, ".tmp"), f)
  w <- r$row
  cat(sprintf("%s %s %s cpu=%.1fs setup=%.1fs ls0=%.2fs scan0=%.2fs lat=%.1fs(n=%s) moves=%d scored_S0=%s cert_S0=%s Phi_start=%d\n",
              format(Sys.time()), id, t$scale_key, w$cpu_total, w$sec_setup, w$sec_ls0, w$sec_scan0, w$sec_lat, w$lat_n,
              w$ls_moves, w$scored_S0, w$certified_S0, w$Phi_start), file = logf, append = TRUE)
}
cat(sprintf("%s shard %d done\n", format(Sys.time()), shard), file = logf, append = TRUE)
