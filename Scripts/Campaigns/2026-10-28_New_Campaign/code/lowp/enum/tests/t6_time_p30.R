# Check 6b: p = 30 timing on a random subset of tasks (task_bits = 10 -> 1024 tasks of 2^20 models). Args: threads fraction design
args <- commandArgs(TRUE); th <- as.integer(args[1]); fr <- as.numeric(args[2]); kind <- if (length(args) > 2) args[3] else "block"
T_DIR <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/lowp/enum/tests"
source(file.path(T_DIR, "helpers.R")); source(file.path(T_DIR, "timing_helpers.R"))
lowp_load()
X <- gen_design(30, kind, seed = 77); Y <- gen_response(X, c(3, 7, 14, 16, 25), c(1.4, -1, 1.8, -1.2, 0.8))
tm <- suppressWarnings(timed(function() lowp_exact(X, list(c100 = Y[, 1], c050 = Y[, 2]), threads = th, prefix_fraction = fr, subset_seed = 11L)))
ex <- tm$value; r <- attr(ex, "run")
cat(sprintf("TIMING p=30 design=%s threads=%d tasks=%g/%g models=%g elapsed_s=%.2f cpu_s=%.2f sum_task_elapsed_s=%.2f models_per_elapsed_s=%.3g cpu_ns_per_model=%.0f cpu_load_before=%s%%\n", kind, th, r$tasks_run, r$n_tasks, r$models_scored, tm$elapsed_s, tm$cpu_s, sum(r$task_seconds), r$models_scored / tm$elapsed_s, tm$cpu_s / r$models_scored * 1e9, tm$env$cpu_load_percent_before))
save_timing(sprintf("p30_%s_th%d_frac%g", kind, th, fr), list(settings = list(p = 30, design = kind, threads = th, fraction = fr, subset_seed = 11L, task_bits = r$task_bits, recheck_stride = 1009L, scales = c("c100", "c050")),
  tasks = r$tasks, task_elapsed_s = r$task_seconds, task_models = r$task_models, elapsed_s = tm$elapsed_s, cpu_s = tm$cpu_s, models = r$models_scored, env = tm$env))
