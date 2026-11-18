# End-to-end check of LIST-R's pathwise clause on small designs through the real core (code of record = core at
# 029bb748 = 4676af6). The sampler path (setup -> calibrate -> final run, as v3_fit does after its branch decision) is run
# on problems small enough to enumerate Omega exactly (v3_enumerate on the same ctx). The list fields are computed from
# top_store by SPEC_LIST_PIP §2 (they are not yet implemented), then compared with the exact posterior.
# Usage: TMPDIR=<scratch> Rscript e2e_small.R <core dir copy> > numerics/e2e_small_out.txt
args <- commandArgs(TRUE); source(file.path(args[1], "v3.R"))
lse <- function(x) { m <- max(x); m + log(sum(exp(x - m))) }
list_fields <- function(ts, names_j) {           # SPEC §2, summed from the last entry to the first
  F <- ts$value; Fm <- max(F); u <- exp(F - Fm); m <- length(F); ord <- m:1
  den <- sum(u[ord]); pip <- setNames(numeric(length(names_j)), names_j)
  for (j in names_j) pip[[j]] <- sum((u * vapply(ts$models, function(S) as.integer(j) %in% S, TRUE))[ord]) / den
  list(pip = pip, mpm = as.integer(names_j[pip > 0.5]), logZ = Fm + log(den))
}
ar_design <- function(n, p, rho) { Z <- matrix(rnorm(n * p), n, p); X <- Z
  for (j in 2:p) X[, j] <- rho * X[, j - 1] + sqrt(1 - rho^2) * Z[, j]; X }
cat(sprintf("%-4s %-5s %-4s %-6s %-7s %-6s %-6s %-9s %-9s %-9s %-9s %-9s %-6s\n", "case", "rho", "n", "status", "S0inT", "hpmOK",
            "|T|", "eps", "errTruth", "errPIP", "dlogZ", "1-pi(T)", "mpmOK"))
set.seed(20261117); case <- 0; fails <- 0
for (rho in c(0, 0.5, 0.8)) for (n in c(40, 80, 160)) for (rep in 1:3) {
  case <- case + 1; p <- 12; S0 <- c(2L, 6L, 9L); th <- c(1, -1, 1)
  X <- ar_design(n, p, rho); y <- drop(X[, S0] %*% th) + rnorm(n)
  pre <- v3_preprocess(X, y, dup_components = FALSE); ctx <- v3_context(pre$X, pre$y, orig = pre$kept, return_gram = FALSE)
  e <- v3_enumerate(ctx); setup <- v3_setup(ctx)
  rt <- .v3cpp$cpp_runtime_new(24, 0)
  cal <- v3_calibrate(setup, seed = 1000 + case, preflight = function(e) FALSE, runtime = rt, grid_fallback = TRUE)
  if (cal$status != "ok") { cat(case, "calibration", cal$status, "\n"); next }
  fr <- v3_final_run(setup, cal$frozen, seed = 1000 + case, runtime = rt, ls0 = TRUE)
  if (fr$status != "completed") { cat(case, "final", fr$status, "\n"); next }
  ts <- fr$top_store; inT <- any(vapply(ts$models, function(S) identical(sort(as.integer(S)), S0), TRUE))
  lf <- list_fields(ts, names(fr$pip_primary))
  piS0 <- exp(e$top$value[vapply(e$top$models, function(S) identical(sort(as.integer(S)), S0), TRUE)] - e$log_Z)
  eps <- 1 - if (length(piS0)) piS0 else 0
  truth <- as.numeric(names(lf$pip) %in% S0); errT <- max(abs(lf$pip - truth)); errP <- max(abs(lf$pip - e$pip[names(lf$pip)]))
  dlogZ <- e$log_Z - lf$logZ; massT <- exp(lf$logZ - e$log_Z)
  hpmOK <- identical(as.integer(fr$hpm), S0); mpmOK <- identical(lf$mpm, S0)
  # LIST-K / LIST-R (i) checks, valid whenever S0 is in T; slack 1e-9 for binary64
  ok <- !inT || (errT <= eps + 1e-9 && errP <= (1 - massT) + 1e-9 && (1 - massT) <= eps + 1e-9 && dlogZ >= -1e-9 &&
                 dlogZ <= -log(1 - eps) + 1e-9 && (eps >= 0.5 || (mpmOK && hpmOK)))
  if (!ok) fails <- fails + 1
  cat(sprintf("%-4d %-5.2f %-4d %-6s %-7s %-6s %-6d %-9.2e %-9.2e %-9.2e %-9.2e %-9.2e %-6s%s\n", case, rho, n, "ok", inT, hpmOK,
              length(ts$models), eps, errT, errP, dlogZ, 1 - massT, mpmOK, if (ok) "" else "  <-- VIOLATION"))
}
cat("violations:", fails, "\n")
