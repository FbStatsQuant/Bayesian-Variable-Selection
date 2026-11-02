# Check 6d: full p = 30 enumeration (2^30 models, both scales), measured. Arg: threads
args <- commandArgs(TRUE); th <- as.integer(args[1])
T_DIR <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/lowp/enum/tests"
source(file.path(T_DIR, "helpers.R")); source(file.path(T_DIR, "timing_helpers.R"))
lowp_load()
X <- gen_design(30, "block", seed = 77); Y <- gen_response(X, c(3, 7, 14, 16, 25), c(1.4, -1, 1.8, -1.2, 0.8))
tm <- timed(function() lowp_exact(X, list(c100 = Y[, 1], c050 = Y[, 2]), threads = th)); ex <- tm$value
r <- attr(ex, "run")
cat(sprintf("FULL p=30 threads=%d models=%.0f status=%s elapsed_s=%.1f cpu_s=%.1f models_per_elapsed_s=%.3g sum_task_elapsed_s=%.1f cpu_load_before=%s%%\n", th, r$models_scored, r$status, tm$elapsed_s, tm$cpu_s, r$models_scored / tm$elapsed_s, sum(r$task_seconds), tm$env$cpu_load_percent_before))
for (sc in names(ex)) { e <- ex[[sc]]; cat(sprintf("  %s logZ=%.12f hpm=%s F=%.6f certified=%s bound=%.4f margin=%.4f recheck=%g mismatches=%g,%g rescales=%g fallbacks=%g log_sum_exp_size_logmass=%.2e\n", sc, e$log_Z, paste(e$hpm, collapse = ";"), e$hpm_F, e$global_certified, e$certificate_bound, e$margin, e$numerics$recheck_count, e$numerics$recheck_mismatch_F, e$numerics$recheck_mismatch_eta, e$numerics$n_rescale, e$numerics$n_fallback_v3, log(sum(exp(e$size_logmass))))) }
save_timing(sprintf("p30_full_th%d", th), list(settings = list(p = 30, design = "block", threads = th, task_bits = r$task_bits, recheck_stride = 1009L, scales = c("c100", "c050")),
  tasks = r$tasks, task_elapsed_s = r$task_seconds, task_models = r$task_models, elapsed_s = tm$elapsed_s, cpu_s = tm$cpu_s, models = r$models_scored, env = tm$env))
