# refingerprint.R -- recompute the fingerprint of saved fits with the current ws_fingerprint (version 2) and rewrite
# their records. For every <stem>.fit.rds in the given directories with a <stem>.rec.rds next to it.
# Usage: Rscript --vanilla refingerprint.R DIR [DIR ...]
local({
  a <- grep("^--file=", commandArgs(FALSE), value = TRUE)
  assign("WS_DIR", if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1]))) else getwd(), envir = globalenv())
})
source(file.path(WS_DIR, "ws_common.R"))
n <- 0L
for (d in commandArgs(trailingOnly = TRUE)) for (f in sort(list.files(d, pattern = "\\.fit\\.rds$", full.names = TRUE))) {
  r <- sub("\\.fit\\.rds$", ".rec.rds", f)
  if (!file.exists(r)) next
  fit <- readRDS(f); rec <- readRDS(r)
  rec$fingerprint_v1 <- rec$fingerprint_v1 %||% rec$fingerprint
  rec$fingerprint <- ws_fingerprint(fit)
  rec$scalars <- ws_scalars(fit)
  rec$guard_summary <- list(exceeded = fit$runtime_guard$exceeded, checkpoints = length(fit$runtime_guard$checkpoints))
  rec$escalation_blocked <- fit$calibration$escalation_blocked
  saveRDS(rec, r); n <- n + 1L
  cat(sprintf("%-44s %s\n", basename(f), substr(rec$fingerprint$all, 1, 16)))
}
cat("REFINGERPRINTED", n, "\n")
