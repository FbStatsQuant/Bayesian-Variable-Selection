# run_start.R -- W3-START sharpness-gate numerics driver (OBSERVATIONS ONLY; production core; local, no NOTS).
# Usage: Rscript run_start.R <out.csv> [workers] [exp1,exp2,...]
# Experiments (p = 2n unless noted; s0, theta per experiment; seeds per cell in the job table):
#   base_iid   inside the assumptions (Setting R, independent columns, s0 = 3, theta = (1,-1,1))
#   base_orth  inside the assumptions (Setting F, nulls orthogonal to the truth: exact zero leakage, strong signals)
#   vis        boundary of (V-c): one truth with delta^2 = c tau^2 log n, c from below to above 1 + 2 log p/log n
#   leak1      boundary of (AL): structured design gen_sat; ONE null with delta^2 = c tau^2 log n
#   leakall    boundary of (AL): structured design gen_sat; ALL free nulls with delta^2 = eta tau^2 log n (eta = 0: inside)
#   twin       outside (FL-16): every second null is a near-twin (corr 1 - 1/n) of another null
#   energy     outside (E): theta = n^(1/4) (1,-1,1), so ||mu||^2/n is unbounded
#   s0grow     outside "s0 fixed": s0 in {1,4,16,32}
#   gleak      boundary of (L-gain-R): Gaussian rows, every null has population correlation rho with truth 1,
#              rho = cL/sqrt(n) (inside) or sqrt(eta log n/n) (outside)
#   ar1        lattice form: AR(1) rows, rho = 0.5; pi0(S0) and the lattice mass pi0(L(Q)) by 20000 coded draws
args <- commandArgs(trailingOnly = TRUE)
out <- args[1]; workers <- if (length(args) >= 2) as.integer(args[2]) else 6L
only <- if (length(args) >= 3) strsplit(args[3], ",")[[1]] else NULL
here <- dirname(normalizePath(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)[1])))

jobs <- list()
add <- function(exp, par, ns, seeds) for (n in ns) for (s in seeds) jobs[[length(jobs) + 1]] <<- list(exp = exp, par = par, n = n, seed = s)
# n <= 800: every cell, 10 seeds. n = 1600 (about 40-60 s per run): a reduced layer, 6 seeds, for the cells that carry
# the asymptotic reading (baselines, the leakage transition, the visibility transition, twin, one gleak cell).
NS <- c(200, 400, 800); SD <- 1:10; BIG <- 1600; SB <- 1:6
add("base_iid", 0, c(100, NS), SD); add("base_iid", 0, BIG, SB)
add("base_orth", 0, c(100, NS), SD); add("base_orth", 0, BIG, SB)
for (c in c(1, 2, 3, 4.5, 6, 9)) add("vis", c, NS, SD)
for (c in c(2, 4.5)) add("vis", c, BIG, SB)
for (c in c(1, 2, 3, 4.5, 6)) add("leak1", c, NS, SD)
for (e in c(0, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0)) add("leakall", e, NS, SD)
for (e in c(0, 0.4, 0.8)) add("leakall", e, BIG, SB)
add("twin", 1, NS, SD); add("twin", 1, BIG, SB)
add("energy", 0.25, NS, SD)
for (s in c(1, 4, 16, 32)) add("s0grow", s, c(200, 800), SD)
for (cl in c(1, 2, 4)) add("gleak", cl, NS, SD)
add("gleak", 2, BIG, SB)
for (e in c(0.25, 0.5, 1)) add("gleak", -e, NS, SD)       # negative par = eta (outside)
add("ar1", 0.5, c(200, 400, 800), 1:8)
if (!is.null(only)) jobs <- Filter(function(j) j$exp %in% only, jobs)

run_job <- function(j) {
  n <- j$n; p <- 2 * n; set.seed(100000 * match(j$exp, c("base_iid","base_orth","vis","leak1","leakall","twin","energy","s0grow","gleak","ar1")) + 1000 * j$seed + n %% 997)
  th3 <- c(1, -1, 1)
  d <- switch(j$exp,
    base_iid = gen_iid(n, p, th3),
    base_orth = gen_orth(n, p, th3),
    vis = gen_iid(n, p, sqrt(j$par * log(n) / ((n - 1) - j$par * log(n)))),
    leak1 = gen_sat(n, p, c(1, -1), leak = list(c = j$par, which = "one")),
    leakall = gen_sat(n, p, c(1, -1), leak = list(c = j$par, which = "all")),
    twin = gen_twin(n, p, th3, gam = 1),
    energy = gen_iid(n, p, n^j$par * th3),
    s0grow = gen_iid(n, p, rep(c(1, -1), length.out = j$par)),
    gleak = gen_gleak(n, p, c(1, -1), rho = if (j$par > 0) j$par / sqrt(n) else sqrt(-j$par * log(n) / n)),
    ar1 = gen_ar1(n, p, c(1, -1), rho = j$par))
  t0 <- proc.time()[[3]]
  r <- tryCatch(start_stats(d$Xs, d$y, d$S0, d$sigma, d$mu, lattice_Q = d$Q, ndraw = if (j$exp == "ar1") 20000 else 0, draw_seed = j$seed, full_vis = (j$seed <= 2)),
                error = function(e) list(status = paste("error:", conditionMessage(e))))
  if (!identical(r$status, "ok")) return(data.frame(exp = j$exp, par = j$par, n = n, p = p, seed = j$seed, status = r$status))
  row <- data.frame(exp = j$exp, par = j$par, n = n, p = p, seed = j$seed, status = "ok", s0 = r$s0, B = r$B, logpi0 = r$logpi0,
             pi0 = r$pi0, o0 = r$o0, T1 = r$T1, fn = r$fn, U = r$U, en = r$en, Lb0 = r$Lb0, pred = r$pred,
             cnull_max = r$cnull_max, ctruth_min = r$ctruth_min, lat = r$lat, nblk_truth = r$nblk_truth,
             Xi_del = r$Xi_del, Xi_in = r$Xi_in, cvis_all = r$cvis_all,
             sec = proc.time()[[3]] - t0)
  # safeguard: each worker appends its finished rows to its own file (partial results survive an interrupted run)
  fn <- file.path(here, sprintf("rows_%d.csv", Sys.getpid()))
  write.table(row, fn, sep = ",", row.names = FALSE, col.names = !file.exists(fn), append = file.exists(fn))
  row
}

library(parallel)
jobs <- jobs[order(-vapply(jobs, function(j) j$n, 0))]               # big first
cl <- makeCluster(workers)
clusterExport(cl, c("here"))
invisible(clusterEvalQ(cl, { source(file.path(here, "start_common.R")); NULL }))
clusterExport(cl, "run_job")
t0 <- proc.time()[[3]]
res <- clusterApplyLB(cl, jobs, run_job)                            # one job per dispatch (true load balancing)
stopCluster(cl)
allcols <- unique(unlist(lapply(res, names)))
res <- lapply(res, function(d) { for (k in setdiff(allcols, names(d))) d[[k]] <- NA; d[allcols] })
tab <- do.call(rbind, res)
write.csv(tab, out, row.names = FALSE)
cat("jobs", length(jobs), "elapsed", round(proc.time()[[3]] - t0), "s; non-ok:", sum(tab$status != "ok"), "\n")
