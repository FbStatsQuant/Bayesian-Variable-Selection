# run_numerics.R -- W3-START2-R boundary numerics driver (OBSERVATIONS ONLY; production core copy via W3START_CORE).
# Usage: Rscript run_numerics.R <workers> <runs, e.g. 1,2,3,4> [nmax]
# Run 1 vcp: orthogonal frame, one truth, delta^2/tau^2 = c log n + 2 log p.  Run 2 F2: A = 0.9, o0/T1.
# Run 3 g1: Sigma = I, s0 = 2, theta = (1,1), p = 2n.  Run 4 lg0: as 3 plus one null with corr C0/sqrt(n log n) (lg0a) or C_L/sqrt(n) (lg0b).
args <- commandArgs(trailingOnly = TRUE)
workers <- as.integer(args[1]); runs <- as.integer(strsplit(args[2], ",")[[1]]); nmax <- if (length(args) >= 3) as.numeric(args[3]) else Inf
here <- dirname(normalizePath(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)[1])))
jobs <- list(); add <- function(...) jobs[[length(jobs) + 1]] <<- list(...)
for (rn in runs) {
  if (rn == 1) for (n in c(200, 800, 3200)) for (pe in c(0.3, 0.9)) for (cc in c(0.6, 0.9, 1.1, 1.5)) for (s in 1:10) add(exp = "vcp", n = n, pe = pe, cc = cc, seed = s)
  if (rn == 2) for (n in c(200, 800, 3200)) for (s in 1:10) add(exp = "F2", n = n, seed = s)
  if (rn == 3) for (n in c(200, 400, 800, 1600, 3200)) for (s in 1:10) add(exp = "g1", n = n, seed = s)
  if (rn == 4) for (n in c(200, 400, 800, 1600, 3200)) for (s in 1:10) { add(exp = "lg0a", n = n, seed = s); add(exp = "lg0b", n = n, seed = s) }
}
jobs <- Filter(function(j) j$n <= nmax, jobs)
run_job <- function(j) {
  n <- j$n; ei <- match(j$exp, c("vcp", "F2", "g1", "lg0a", "lg0b"))
  set.seed(100000 * ei + 1000 * j$seed + n %% 997 + if (j$exp == "vcp") round(100 * j$cc + 7 * j$pe) else 0)
  t0 <- proc.time()[[3]]; par <- NA_real_
  d <- switch(j$exp,
    vcp = { p <- ceiling(n^j$pe); p <- max(p, 17L); par <- j$cc; gen_vcp(n, p, j$cc * log(n) + 2 * log(p)) },
    F2 = gen_F2(n, 0.9),
    g1 = gen_g1(n, 2 * n, c(1, 1)),
    lg0a = { par <- 2 / sqrt(n * log(n)); gen_g1(n, 2 * n, c(1, 1), rho = par) },
    lg0b = { par <- 2 / sqrt(n); gen_g1(n, 2 * n, c(1, 1), rho = par) })
  r <- tryCatch(start_stats(d$Xs, d$y, d$S0, d$sigma, d$mu), error = function(e) list(status = paste("error:", conditionMessage(e))))
  if (!identical(r$status, "ok")) return(data.frame(exp = j$exp, n = n, pe = if (is.null(j$pe)) NA else j$pe, par = par, seed = j$seed, status = r$status))
  data.frame(exp = j$exp, n = n, pe = if (is.null(j$pe)) NA else j$pe, par = par, seed = j$seed, status = "ok", p = r$p, s0 = r$s0, B = r$B,
             pi0 = r$pi0, o0 = r$o0, T1 = r$T1, cnull_max = r$cnull_max, ctruth_min = r$ctruth_min, sec = proc.time()[[3]] - t0)
}
library(parallel)
jobs <- jobs[order(-vapply(jobs, function(j) j$n, 0))]
cl <- makeCluster(workers)
clusterExport(cl, c("here"))
invisible(clusterEvalQ(cl, { Sys.setenv(W3START_CORE = file.path(Sys.getenv("TMPDIR"), "core")); source(file.path(here, "r_common.R")); source(file.path(here, "gens.R")); NULL }))
clusterExport(cl, "run_job")
t0 <- proc.time()[[3]]
res <- clusterApplyLB(cl, jobs, run_job)
stopCluster(cl)
allcols <- unique(unlist(lapply(res, names)))
res <- lapply(res, function(d) { for (k in setdiff(allcols, names(d))) d[[k]] <- NA; d[allcols] })
tab <- do.call(rbind, res)
fn <- file.path(here, "out", sprintf("raw_runs%s.csv", paste(runs, collapse = "")))
write.csv(tab, fn, row.names = FALSE)
cat("runs", runs, "jobs", length(jobs), "elapsed", round(proc.time()[[3]] - t0), "s; non-ok:", sum(tab$status != "ok"), "->", fn, "\n")
