# N0 -- Lemma R'(a''): invariance of the CODED method under y -> a + c*y, checked on the compiled code path.
# Runs the production entry point v3_fit (preprocess -> context -> score) on rescaled responses and compares outputs.
# Local only (no NOTS). Usage, from the repository root:
#   Rscript Theory_work/Wave3/W3-MISR/numerics/N0_code_invariance.R > Theory_work/Wave3/W3-MISR/numerics/N0_out.txt
args <- commandArgs(trailingOnly = FALSE)
here <- dirname(normalizePath(sub("^--file=", "", args[grep("^--file=", args)])))
root <- normalizePath(file.path(here, "..", "..", "..", ".."))
source(file.path(root, "Scripts", "SMC_BVS", "core", "v3.R"))
cat("core dir:", V3_CORE_DIR, "\ncpp key:", V3_CPP_KEY, "\n", R.version.string, "\n\n")

transforms <- list(c(a = 0, c = 1), c(a = 5, c = 3.7), c(a = -2, c = 1e-6), c(a = 1e3, c = 1e8),
                   c(a = 0, c = 4), c(a = 0.3, c = -2.5), c(a = 0, c = 1e-150), c(a = 0, c = 1e150))

make_data <- function(n, p, seed) {
  set.seed(seed)
  Z <- matrix(rnorm(n * p), n, p); f <- rnorm(n)
  X <- 0.6 * Z + 0.8 * f                       # equicorrelated columns
  y <- 0.7 * X[, 1] - 0.5 * X[, 2] + rnorm(n)
  list(X = X, y = y)
}

report <- function(tag, base, fit, tr) {
  same_status <- identical(base$status, fit$status)
  same_hpm <- identical(sort(as.integer(base$hpm)), sort(as.integer(fit$hpm)))
  dpip <- if (!is.null(base$pip_primary) && !is.null(fit$pip_primary)) max(abs(base$pip_primary - fit$pip_primary)) else NA
  dF <- if (!is.null(base$hpm_F) && !is.null(fit$hpm_F)) abs(base$hpm_F - fit$hpm_F) else NA
  dZ <- if (!is.null(base$log_Z_rel_m0) && !is.null(fit$log_Z_rel_m0)) abs(base$log_Z_rel_m0 - fit$log_Z_rel_m0) else NA
  cat(sprintf("%-6s a=%-8g c=%-8g status=%-8s same_status=%s same_hpm=%s max|dPIP|=%.3e |dF(hpm)|=%.3e |d logZ_rel|=%.3e\n",
              tag, tr[["a"]], tr[["c"]], fit$status, same_status, same_hpm, dpip, dF, dZ))
  c(ok = same_status && same_hpm, dpip = dpip)
}

# --- Part 1: the standardised response itself (v3_preprocess) ---------------------------------------------------
d <- make_data(60, 10, 11)
p0 <- v3_preprocess(d$X, d$y)
cat("Part 1: v3_preprocess(X, a + c*y)$y against v3_preprocess(X, y)$y (expected: sign(c) * y up to rounding)\n")
for (tr in transforms) {
  p1 <- v3_preprocess(d$X, tr[["a"]] + tr[["c"]] * d$y)
  cat(sprintf("  a=%-8g c=%-8g max|y' - sign(c) y| = %.3e   s_y'/(|c| s_y) - 1 = %.3e\n", tr[["a"]], tr[["c"]],
              max(abs(p1$y - sign(tr[["c"]]) * p0$y)), p1$s_y / (abs(tr[["c"]]) * p0$s_y) - 1))
}

# --- Part 2: exact branch (enumeration): PIPs, HPM, log Z --------------------------------------------------------
cat("\nPart 2: v3_fit, exact branch (n = 60, p = 10; three data sets)\n")
res <- NULL
for (ds in 11:13) {
  d <- make_data(60, 10, ds)
  base <- v3_fit(d$X, d$y, seed = 7)
  cat(sprintf(" data %d: branch=%s status=%s hpm={%s}\n", ds, base$branch_run, base$status, paste(base$hpm, collapse = ",")))
  for (tr in transforms[-1]) res <- rbind(res, report("exact", base, v3_fit(d$X, tr[["a"]] + tr[["c"]] * d$y, seed = 7), tr))
}
cat(sprintf(" exact branch: all status/HPM equal = %s; max over runs of max|dPIP| = %.3e\n", all(res[, "ok"] == 1), max(res[, "dpip"], na.rm = TRUE)))

# --- Part 3: SMC branch (p >> exact threshold), same seed ---------------------------------------------------------
cat("\nPart 3: v3_fit, SMC branch (n = 80, p = 120), same seed\n")
d <- make_data(80, 120, 21)
t0 <- proc.time()[["elapsed"]]
base <- v3_fit(d$X, d$y, seed = 7)
cat(sprintf(" baseline: branch=%s status=%s hpm={%s} (%.1f s)\n", base$branch_run, base$status, paste(base$hpm, collapse = ","), proc.time()[["elapsed"]] - t0))
res3 <- NULL
for (tr in transforms[c(2, 3, 5, 6)]) res3 <- rbind(res3, report("smc", base, v3_fit(d$X, tr[["a"]] + tr[["c"]] * d$y, seed = 7), tr))
cat(sprintf(" SMC branch: all status/HPM equal = %s; max over runs of max|dPIP| = %.3e\n", all(res3[, "ok"] == 1), max(res3[, "dpip"], na.rm = TRUE)))
cat("\nDONE\n")
