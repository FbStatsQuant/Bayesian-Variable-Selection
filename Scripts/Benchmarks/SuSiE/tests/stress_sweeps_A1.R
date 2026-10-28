# stress_sweeps_A1.R -- forced-sweep timing measurement for sizing --time of the production array
# (Astra production consult). Dev data only; diagnostics only; never used for any reported result.
# The fit uses the production settings except `tol = -Inf`, so IBSS never meets its stopping rule
# and runs exactly `max_iter = 1000` sweeps (the wrapper then fails the fit: not converged). This
# measures the cost of 1,000 sweeps on one settled dev fit; it is not an upper bound on optimizer
# cost for every dataset, so the production --time adds an explicit margin on top of it.
# Acceptance (else exit 1): both variants run exactly 1,000 sweeps with a finite ELBO trace and end
# in the expected "not converged" failure. Saves timings, diagnostics and hashes to <out_rds>.
# Usage (compute node, same thread/locale settings as production):
#   Rscript --vanilla tests/stress_sweeps_A1.R <code_dir> <dev_input_rds> <out_rds>
a <- commandArgs(trailingOnly = TRUE); stopifnot(length(a) == 3L)
code_dir <- normalizePath(a[1])
cfg <- new.env(); sys.source(file.path(code_dir, "config.R"), envir = cfg)
.libPaths(c(cfg$COMMON$LIB, .Library))
E <- new.env(parent = asNamespace("stats"))
sys.source(file.path(code_dir, "common.R"), envir = E)
sys.source(file.path(code_dir, "methods", "fit_A1_susie.R"), envir = E)
R <- new.env(); sys.source(file.path(code_dir, "run_case.R"), envir = R)
loadNamespace("susieR"); loadNamespace("digest")
d <- readRDS(a[2]); y <- unname(as.numeric(d$Y[, "c100"]))
out <- list(input = a[2], input_sha256 = R$file_sha256(a[2]), source_sha256 = R$source_tree_sha256(code_dir),
            env_fingerprint = R$env_fingerprint(cfg$COMMON$LIB), host = Sys.info()[["nodename"]],
            slurm_job_id = Sys.getenv("SLURM_JOB_ID", NA), locale = Sys.getlocale(),
            threads = Sys.getenv(c("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "FLEXIBLAS_NUM_THREADS")),
            fits = list())
ok <- TRUE
for (v in c("primary", "L100")) {
  S <- cfg$make_settings(v); S$A1$TOL <- -Inf
  RNGkind("Mersenne-Twister", "Inversion", "Rejection"); set.seed(d$method_seed)
  t0 <- proc.time()[["elapsed"]]
  r <- E$fit_A1_susie(d$X, y, d$foldid, d$method_seed, S)
  el <- proc.time()[["elapsed"]] - t0
  dg <- r$diagnostics
  pass <- identical(as.integer(dg$niter), 1000L) && length(dg$elbo) == 1000L && all(is.finite(dg$elbo)) &&
    all(r$rules$status == "failed") && all(grepl("not converged", r$rules$error))
  ok <- ok && pass
  out$fits[[v]] <- list(elapsed_s = el, niter = dg$niter, per_sweep_s = el / max(1, dg$niter),
                        accepted = pass, error = r$rules$error[1], elbo_last = utils::tail(dg$elbo, 1),
                        n_active = dg$n_active, warnings = r$warnings, messages = r$messages)
  cat(sprintf("FORCED-SWEEP %s %s L=%d niter=%s accepted=%s elapsed=%.1f s per_sweep=%.4f s\n",
              d$dataset_id, v, if (v == "L100") S$A1$L_S1 else S$A1$L,
              if (is.null(dg$niter)) "NULL" else dg$niter, pass, el, el / max(1, dg$niter)))
}
saveRDS(out, a[3])
cat("saved", a[3], "accepted:", ok, "\n")
quit(status = if (ok) 0L else 1L)
