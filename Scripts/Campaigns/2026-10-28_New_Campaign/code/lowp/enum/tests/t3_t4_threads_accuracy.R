# Check 3 (thread invariance) and check 4 (streaming accumulation accuracy vs an independent R computation), p = 20.
source("C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/lowp/enum/tests/helpers.R")
lowp_load()
for (kind in c("block", "ar1")) {
  X <- gen_design(20, kind, seed = 31); Y <- gen_response(X, c(3, 7, 14, 16), c(1.4, -1, 1.8, -1.2))
  Yl <- list(c100 = Y[, 1], c050 = Y[, 2])
  r <- lapply(c(1, 4, 8), function(th) lowp_exact(X, Yl, threads = th, collect_F = (th == 4), return_raw = (th == 4)))
  strip <- function(e) { a <- unclass(e); a[c("c100", "c050")] }
  cat(sprintf("[%s] thread invariance (identical() of all outputs, threads 1 vs 4 vs 8): 1==4 %s, 1==8 %s, models_scored %g %g %g\n", kind,
      identical(strip(r[[1]]), strip(r[[2]])), identical(strip(r[[1]]), strip(r[[3]])),
      attr(r[[1]], "run")$models_scored, attr(r[[2]], "run")$models_scored, attr(r[[3]], "run")$models_scored))
  alt <- lowp_exact(X, Yl, threads = 4, task_bits = 6)
  cat(sprintf("[%s] other task split (6 bits vs 10): same HPM %s, |dlogZ|=%.2e, max|dPIP|=%.2e, top identical %s\n", kind,
      identical(alt$c100$hpm, r[[1]]$c100$hpm), abs(alt$c100$log_Z - r[[1]]$c100$log_Z), max(abs(alt$c100$pip - r[[1]]$c100$pip)),
      identical(alt$c100$top$model, r[[1]]$c100$top$model)))
  ## check 4: independent R computation from the full vector of 2^20 F values
  run <- attr(r[[2]], "run"); N <- 2^20; mk <- 0:(N - 1)
  for (sc in c("c100", "c050")) {
    F <- run$F_all[[sc]]; stopifnot(!anyNA(F), length(F) == N)
    o <- order(F); Fs <- F[o]; mx <- Fs[N]
    logZ_R <- mx + log(sum(exp(Fs - mx)))                 # ascending (smallest first); R's sum() accumulates in long double
    # Higher-precision cross-check: Neumaier-compensated sum in double
    comp_sum <- function(x) { s <- 0; cc <- 0; for (v in x) { t <- s + v; cc <- cc + if (abs(s) >= abs(v)) (s - t) + v else (v - t) + s; s <- t }; s + cc }
    logZ_R2 <- mx + log(comp_sum(exp(Fs - mx)))
    w <- exp(F - mx); pip_R <- vapply(0:19, function(j) sum(w[bitwAnd(mk, 2^j) != 0]) / sum(w), 0)
    sz <- vapply(mk, function(m) sum(bitwAnd(m, 2^(0:19)) != 0), 0L)
    szm_R <- vapply(0:20, function(k) { ww <- w[sz == k]; if (length(ww)) mx + log(sum(ww)) - logZ_R else -Inf }, 0); szj_R <- szm_R + logZ_R; norm_R <- log(sum(exp(szm_R)))
    e <- r[[2]][[sc]]
    cat(sprintf("[%s %s] logZ stream=%.15f R(sorted)=%.15f R(compensated)=%.15f |diff|=%.2e / %.2e; max|dPIP|=%.2e; max|d size_logmass|=%.2e; hpm F rel R max: %s; top1 matches R max: %s\n",
        kind, sc, e$log_Z, logZ_R, logZ_R2, abs(e$log_Z - logZ_R), abs(e$log_Z - logZ_R2), max(abs(e$pip - pip_R)),
        max(abs(e$size_logmass - szm_R)[is.finite(szm_R)]), same_bits(e$hpm_F, mx), same_bits(e$top$F[1], mx)))
    cat(sprintf("   posterior size masses: log sum exp(size_logmass) = %.2e (R: %.2e); max|d size_logjoint| = %.2e; all p_k in [0,1]: %s
", log(sum(exp(e$size_logmass))), norm_R, max(abs(e$size_logjoint - szj_R)[is.finite(szj_R)]), all(exp(e$size_logmass) <= 1)))
  }
}
