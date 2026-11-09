# D4: production core WITHOUT any LS0, one fit per (scenario, n, seed).  Rscript d4_run.R scen n seed
args <- commandArgs(trailingOnly = TRUE)
scen <- as.integer(args[1]); n <- as.integer(args[2]); sd <- as.integer(args[3])
source("d4_core/v3.R")
X <- as.matrix(read.csv(sprintf("d4_data/X_S%d_n%d_s%d.csv", scen, n, sd), header = FALSE))
y <- scan(sprintf("d4_data/y_S%d_n%d_s%d.csv", scen, n, sd), quiet = TRUE)
dimnames(X) <- NULL
t0 <- Sys.time()
fit <- v3_fit(X, y, seed = 1000L + sd, allocation = list(mem_gb = 8, hours = 1))
el <- as.numeric(difftime(Sys.time(), t0, units = "secs"))
dir.create("d4_out", showWarnings = FALSE)
# (full RDS not saved; summary JSON below)
cat(sprintf("S%d n=%d seed=%d status=%s branch=%s secs=%.1f\n", scen, n, sd, fit$status, fit$branch_run, el))
cat("hpm:", fit$hpm, " F:", fit$hpm_F, "\n")
ls_ <- fit$local_search
S <- list(scen = scen, n = n, seed = sd, rseed = 1000L + sd, status = fit$status, branch = fit$branch_run, secs = el,
  hpm = fit$hpm, hpm_F = fit$hpm_F, hpm_prov = fit$hpm_provenance[c("phase", "mechanism", "tier", "island", "stage")],
  hpm_before_local = fit$hpm_before_local$model, hpm_before_local_F = fit$hpm_before_local$F,
  ls_centre = ls_$centre, ls_returned = ls_$returned, ls_moves = ls_$moves, ls_termination = ls_$termination,
  ls_certified = ls_$local_certified, ls_limit = ls_$local_limit, ls_scan_size = ls_$scan_size, ls_n_eval = ls_$n_evaluated,
  ls_path = ls_$path, ls_scanned_centres = ls_$scanned_centres,
  top_models = fit$top_store$models, top_values = fit$top_store$value, top_capacity = fit$top_store$capacity, top_full = fit$top_store$full,
  near_ties = fit$near_ties, near_tie_F = fit$near_tie_F, near_tie_truncated = fit$near_tie_truncated,
  n_distinct = fit$instrumentation$scored$n_distinct, n_distinct_hll = fit$instrumentation$scored$n_distinct_hll, registry_mode = fit$instrumentation$scored$mode,
  local_certified = fit$local_certified, flags = fit$flags[c("E1", "E2", "E3", "low_empirical_ESS", "local_limit", "escalated", "grid_unconverged")],
  timings_total = fit$timings$total, timings_calibration = fit$timings$calibration, timings_final = fit$timings$final,
  pip_primary_top = head(sort(fit$pip_primary, decreasing = TRUE), 12), K = fit$budgets$K, ell = fit$budgets$ell, B = fit$B,
  leaders0 = fit$leaders_gamma0$models, leaders1 = fit$leaders_gamma1$models)
jsonlite::write_json(S, sprintf("d4_out/sum_S%d_n%d_s%d.json", scen, n, sd), auto_unbox = TRUE, digits = NA, null = "null")
