# run_all.R -- W3-RM2 boundary-violation numerics driver (local machine, no NOTS). Usage: Rscript run_all.R <dir> <layer> <workers>
args <- commandArgs(trailingOnly = TRUE); here <- args[1]; layer <- args[2]; nw <- as.integer(args[3])
grid <- function(n, seeds) {
  g <- rbind(
    expand.grid(type = "B1", b = c(0.25, 0.375, 0.5, 0.625, 0.75), eta = 0, stringsAsFactors = FALSE),
    expand.grid(type = "B2", b = c(0.25, 0.375, 0.5), eta = 0, stringsAsFactors = FALSE),
    expand.grid(type = "B3", b = c(0.5, 0.625), eta = 0, stringsAsFactors = FALSE),
    expand.grid(type = "B4", b = 0.375, eta = c(0.05, 0.2, 1), stringsAsFactors = FALSE))
  g <- merge(g, data.frame(seed = seeds)); g$n <- n; g$p <- 2 * n; g
}
jobs <- switch(layer,
  n400 = grid(400, 1:10), n1600 = grid(1600, 1:6),
  n3200 = { g <- grid(3200, 1:3); g[g$type == "B1", ] },
  stop("unknown layer"))
jobs <- jobs[order(-jobs$b, jobs$type, jobs$seed), ]
outdir <- file.path(here, paste0("rows_", layer)); dir.create(outdir, showWarnings = FALSE)
library(parallel)
cl <- makeCluster(nw, outfile = file.path(here, paste0("log_", layer, ".txt")))
clusterExport(cl, c("here", "outdir"))
invisible(clusterEvalQ(cl, { source(file.path(here, "rm2_common.R")); NULL }))
res <- clusterApplyLB(cl, split(jobs, seq_len(nrow(jobs))), function(j) {
  f <- file.path(outdir, sprintf("%s_b%s_eta%s_n%d_s%d.rds", j$type, j$b, j$eta, j$n, j$seed))
  if (file.exists(f)) return(readRDS(f))
  r <- tryCatch(run_one(j$n, j$p, j$b, j$type, j$seed, eta = j$eta),
                error = function(e) data.frame(n = j$n, p = j$p, b = j$b, type = j$type, seed = j$seed, status = paste("error:", conditionMessage(e))))
  r$eta <- j$eta; saveRDS(r, f); gc(); r
})
stopCluster(cl)
allc <- unique(unlist(lapply(res, names)))
res <- lapply(res, function(r) { for (c in setdiff(allc, names(r))) r[[c]] <- NA; r[, allc] })
out <- do.call(rbind, res)
write.csv(out, file.path(here, paste0("results_", layer, ".csv")), row.names = FALSE)
cat("done", layer, nrow(out), "rows\n")
