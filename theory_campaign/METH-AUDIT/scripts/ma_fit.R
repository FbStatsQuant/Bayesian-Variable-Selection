# ma_fit.R -- METH-AUDIT empirical check on one study design (production engine only).
# Usage: Rscript ma_fit.R <dataset_id> <scale_key> <out.rds> [R_big=32]
# 1. production path: preprocess -> context -> setup -> v3_calibrate(seed) [timed by phase] -> v3_final_run (serial, R=4)
# 2. the same 4 final islands (streams 10..13, N_e) run as independent workers (own cache + ledger) with mclapply:
#    bitwise check of log Zhat_r and PIP_r against step 1; wall-clock with islands concurrent
# 3. R_big islands of floor(4 N_e / R_big) particles, streams 1001.., same frozen grid: pooled log Zhat, PIPs, HPM
# Seed = method_seed of the study manifest (assumed to be the production seed). Fixed seeds throughout.
suppressMessages({ library(parallel) })
args <- commandArgs(TRUE)
id <- args[1]; sk <- args[2]; out <- args[3]; Rbig <- if (length(args) >= 4) as.integer(args[4]) else 32L
source(file.path(dirname(normalizePath(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)))), "ma_core.R"))
ma_load()
cores <- as.integer(Sys.getenv("OWLS_JOB_CORES", "1"))
study <- "/home/fb31/ls0_work/study"
pp <- sub("_.*", "", id); sc <- sub("^[^_]*_(S[0-9]).*", "\\1", id)
if (id == "smoke") {            # small synthetic problem for a compile/logic test (fixed seed)
  set.seed(20261103); n <- 100; p <- 60; Z <- matrix(rnorm(n * p), n); X <- Z + 0.6 * Z[, rep(1:12, 5)]
  S0 <- c(3L, 17L, 40L); y <- drop(X[, S0] %*% c(1, -0.8, 0.7)) + rnorm(n); seed <- 12345L
} else {
man <- read.csv(file.path(study, "manifests", "cells", paste0(pp, "_", sc, "_inputs.csv")))
seed <- man$method_seed[man$dataset_id == id]
inp <- readRDS(file.path(study, "inputs", pp, paste0(id, ".rds")))
tru <- read.csv(file.path(study, "manifests", "cells", paste0(pp, "_", sc, "_truth.csv")))
S0 <- sort(as.integer(strsplit(tru$active[tru$dataset_id == id], ";")[[1]]))
X <- inp$X; y <- unname(inp$Y[, sk])
}
lse <- function(x) { m <- max(x); m + log(sum(exp(x - m))) }
el <- function() proc.time()[["elapsed"]]
res <- list(id = id, scale = sk, seed = seed, S0 = S0, cores = cores)

t0 <- el(); pre <- v3_preprocess(X, y, dup_components = FALSE); res$t_pre <- el() - t0
b <- v3_budgets(pre$n, pre$p)
t0 <- el(); ctx <- v3_context(pre$X, pre$y, orig = pre$kept, return_gram = FALSE); res$t_context <- el() - t0
t0 <- el(); setup <- v3_setup(ctx); res$t_setup <- el() - t0; res$setup_seconds <- setup$seconds
t0 <- el(); cal <- v3_calibrate(setup, seed); res$t_cal <- el() - t0
stopifnot(cal$status == "ok")
fz <- cal$frozen
res$cal <- list(tier = fz$tier, T = length(fz$grid) - 1, grid = fz$grid,
  tiers = lapply(cal$tiers, function(a) list(tier = a$tier, rebuilds = a$rebuilds, converged = a$converged,
     pilot_T = length(a$pilot$schedule) - 1, seconds = a$seconds, triggers = a$triggers,
     grid_T = vapply(a$grids, function(g) length(g$grid) - 1, 0))))
N <- as.integer(fz$N); L <- as.integer(fz$L); ell <- as.integer(b$ell); capc <- 500 * setup$ctx$p
cat(sprintf("%s %s seed=%d cal=%.1fs tier=%d T=%d rebuilds=%s\n", id, sk, seed, res$t_cal, fz$tier, res$cal$T,
            paste(vapply(res$cal$tiers, function(a) a$rebuilds, 0), collapse = "/")))

t0 <- el(); fr <- v3_final_run(setup, fz, seed); res$t_final_serial <- el() - t0
res$prod <- list(log_Z_r = fr$log_Z_r, log_Z = fr$log_Z, pip = fr$pip_primary, pip_r = fr$pip_r, hpm = sort(fr$hpm),
                 hpm_F = fr$hpm_F, flags = fr$flags, island_seconds = fr$timings$islands, local_seconds = fr$timings$local,
                 ess = lapply(fr$stage_record, function(x) x$ess))
cat(sprintf("  serial final %.1fs logZ=%.4f hpm==S0 %s\n", res$t_final_serial, fr$log_Z, identical(sort(fr$hpm), S0)))

run_islands <- function(R, Nr, streams) {
  t0 <- el()
  isl <- mclapply(seq_len(R), function(r) .v3cpp$cpp_ma_island(setup$ptr, fz$grid, Nr, L, 4L, fz$tier, as.numeric(seed),
                    as.numeric(streams[r]), r, capc, TRUE), mc.cores = cores, mc.preschedule = FALSE)
  wall <- el() - t0
  lz <- vapply(isl, function(x) x$island$log_Z, 0)
  P <- sapply(isl, function(x) x$island$pip)
  w <- exp(lz - max(lz)); w <- w / sum(w)
  bestF <- -Inf; best <- NULL
  for (x in c(list(list(ledger = list(hpm = cal$hpm))), isl)) {
    h <- x$ledger$hpm; if (is.null(h$F)) next
    if (h$F > bestF) { bestF <- h$F; best <- sort(as.integer(h$model)) }
  }
  t1 <- el(); ls <- .v3cpp$cpp_ma_local(setup$ptr, best, ell, fz$tier); tl <- el() - t1
  hpm <- if (!is.na(ls$best_scored_F) && ls$best_scored_F > bestF) sort(as.integer(ls$best_scored)) else best
  list(R = R, N = Nr, wall = wall, island_seconds = vapply(isl, function(x) x$seconds_total, 0), log_Z_r = lz,
       log_Z = lse(lz) - log(R), pip_eq = rowMeans(P), pip_zw = as.vector(P %*% w), pip_r = P, best_before_local = best,
       best_before_local_F = bestF, hpm = hpm, hpm_F = max(bestF, ls$best_scored_F, na.rm = TRUE), local_seconds = tl,
       island_best = vapply(isl, function(x) max(x$ledger$island_best), 0),
       ess = lapply(isl, function(x) x$island$ess), ess_min_frac = min(unlist(lapply(isl, function(x) x$island$ess))) / Nr,
       cache_clears = vapply(isl, function(x) x$cache_clears, 0))
}
r4 <- run_islands(4L, N, 10:13)
res$r4 <- r4
res$bitwise <- list(log_Z_r = identical(r4$log_Z_r, unname(fr$log_Z_r)), pip_r = identical(unname(r4$pip_r), unname(fr$pip_r)),
                    hpm = identical(r4$hpm, sort(as.integer(fr$hpm))), max_abs_dlogZ = max(abs(r4$log_Z_r - fr$log_Z_r)))
cat(sprintf("  R=4 workers wall %.1fs (sum island %.1fs) bitwise logZ %s pip %s hpm %s\n", r4$wall, sum(r4$island_seconds),
            res$bitwise$log_Z_r, res$bitwise$pip_r, res$bitwise$hpm))
Nb <- as.integer(floor(4 * N / Rbig))
rb <- run_islands(Rbig, Nb, 1000L + seq_len(Rbig))
res$rbig <- rb
cat(sprintf("  R=%d N=%d wall %.1fs logZ=%.4f (R4 %.4f) maxdPIP_eq %.4f maxdPIP_zw %.4f hpm same %s hpm==S0 %s\n", Rbig, Nb,
            rb$wall, rb$log_Z, r4$log_Z, max(abs(rb$pip_eq - r4$pip_eq)), max(abs(rb$pip_zw - r4$pip_eq)),
            identical(rb$hpm, r4$hpm), identical(rb$hpm, S0)))
saveRDS(res, out)
