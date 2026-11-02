# Check 6a: p = 20 full enumeration timing, two designs, both scales per pass. Arg: threads (0 = baseline: load + compile only).
args <- commandArgs(TRUE); th <- as.integer(args[1])
T_DIR <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/lowp/enum/tests"
source(file.path(T_DIR, "helpers.R")); source(file.path(T_DIR, "timing_helpers.R"))
lowp_load()
if (th > 0) for (kind in c("block", "ar1")) {
  X <- gen_design(20, kind, seed = 31); Y <- gen_response(X, c(3, 7, 14, 16), c(1.4, -1, 1.8, -1.2))
  tm <- timed(function() lowp_exact(X, list(c100 = Y[, 1], c050 = Y[, 2]), threads = th)); ex <- tm$value
  r <- attr(ex, "run")
  cat(sprintf("TIMING p=20 design=%s threads=%d elapsed_s=%.3f cpu_s=%.3f models=%g models_per_elapsed_s=%.3g (both scales, one pass) logZ_c100=%.12f\n", kind, th, tm$elapsed_s, tm$cpu_s, r$models_scored, r$models_scored / tm$elapsed_s, ex$c100$log_Z))
  save_timing(sprintf("p20_%s_th%d", kind, th), list(settings = list(p = 20, design = kind, threads = th, scales = c("c100", "c050"), task_bits = r$task_bits, recheck_stride = 1009L), elapsed_s = tm$elapsed_s, cpu_s = tm$cpu_s, models = r$models_scored, env = tm$env))
}
