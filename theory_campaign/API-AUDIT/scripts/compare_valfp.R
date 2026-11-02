# Compare the production (double) fits with the long-double replays. Usage: Rscript compare_valfp.R <out_dir> <results_dir>
args <- commandArgs(TRUE); out <- args[1]; resd <- args[2]
lse <- function(x) { m <- max(x); m + log(sum(exp(x - m))) }
rd <- function(id, m) { f <- file.path(out, sprintf("fit%02d_%s.rds", id, m)); if (file.exists(f)) readRDS(f) else NULL }
lo_parts <- function(f) {           # low-order parts of the ld log Zhat_r (0 for the double core)
  ti <- if (!is.null(f$timings$final_detail)) f$timings$final_detail$islands else f$timings$islands
  if (!is.null(ti) && "log_Z_lo" %in% colnames(ti)) as.numeric(ti[, "log_Z_lo"]) else rep(0, length(f$log_Z_r))
}
same <- function(a, b) isTRUE(all.equal(a, b, tolerance = 0)) && identical(length(a), length(b))
moves_cols <- c("gibbs", "gibbs_state_changes", "uswap_exec", "uswap_acc", "uswap_self", "nswap_exec", "nswap_acc",
                "nswap_reject_noscore", "nswap_self", "indep_exec", "indep_acc")
path_signature <- function(f) {     # every discrete record of the final run's path
  st <- f$stage_table; st <- st[st$phase %in% c("final", "final_bridge", "bridge") | grepl("final", st$phase), , drop = FALSE]
  st <- as.matrix(st[, intersect(c(moves_cols, "distinct_resampled", "distinct_moved", "stage", "island"), names(st)), drop = FALSE])
  tt <- f$terminal_table; tt <- as.matrix(tt[, setdiff(names(tt), "seconds"), drop = FALSE])
  rownames(st) <- NULL; rownames(tt) <- NULL      # row names differ (the fit's stage table also holds calibration rows)
  list(streams = lapply(f$streams, function(s) c(s$position_end, s$init_draws_hash)),
       stage_moves = st, terminal = tt,
       counts = f$score_counts, cache = f$cache, hpm = f$hpm, mpm = f$mpm, hpm_before = f$hpm_before_local$model,
       ls_path = f$local_search$path, ls_scanned = f$local_search$scanned_centres, ls_term = f$local_search$termination,
       top = f$top_store$models, near = f$near_ties, prov = f$hpm_provenance[c("phase", "island", "stage", "round", "particle", "position")])
}
rows <- list(); detail <- list()
for (id in 1:10) {
  fp <- rd(id, "fp"); lr <- rd(id, "ld_replay"); lf <- rd(id, "ld_full")
  if (is.null(fp)) next
  r <- data.frame(id = id, p = fp$design$p, scen = fp$design$scen, scale = fp$design$scale, status_fp = fp$status,
                  tier = fp$frozen$tier, T = length(fp$frozen$grid) - 1, n_inherited = length(fp$frozen$inherited$models),
                  log_Z_fp = fp$log_Z, sec_fp = fp$seconds)
  if (!is.null(lr)) {
    sa <- path_signature(fp); sb <- path_signature(lr)
    agree <- vapply(names(sa), function(k) identical(sa[[k]], sb[[k]]), TRUE)
    lo <- lo_parts(lr)
    dZr <- (fp$log_Z_r - lr$log_Z_r) - lo                     # log Zhat_r^fp - log Zhat_r^ld (ld = hi + lo)
    # pooled: log Zhat^ld from hi+lo, evaluated as fp-pooled minus a first-order correction
    w <- exp(lr$log_Z_r - lse(lr$log_Z_r))
    dZ <- (lse(fp$log_Z_r) - lse(lr$log_Z_r)) - sum(w * lo)
    r$setup_same <- identical(fp$blocks, lr$blocks) && identical(fp$neighbours, lr$neighbours)
    r$path_same <- all(agree); r$path_diff <- paste(names(agree)[!agree], collapse = ",")
    r$eta_r_max <- max(abs(dZr)); r$eta_pooled <- abs(dZ)
    r$dlogZbar0 <- fp$log_Zbar0 - lr$log_Zbar0; r$dlogm0 <- fp$log_m0 - lr$log_m0
    r$pip_maxdiff <- max(abs(fp$pip_r - lr$pip_r)); r$hpmF_diff <- fp$hpm_F - lr$hpm_F
    r$sec_ld <- lr$seconds
    detail[[length(detail) + 1]] <- data.frame(id = id, island = seq_along(dZr), log_Z_r_fp = fp$log_Z_r, dlogZr = dZr)
  }
  if (!is.null(lf)) {
    r$full_status_same <- identical(fp$status, lf$status)
    r$full_tier_same <- identical(fp$frozen$tier, lf$frozen$tier)
    r$full_T_same <- length(fp$frozen$grid) == length(lf$frozen$grid)
    r$full_grid_maxdiff <- if (r$full_T_same) max(abs(fp$frozen$grid - lf$frozen$grid)) else NA
    r$full_inherited_same <- identical(fp$frozen$inherited$models, lf$frozen$inherited$models)
    r$full_cal_hpm_same <- identical(fp$calibration$hpm$model, lf$calibration$hpm$model)
    if (identical(lf$status, "completed")) {
      sa <- path_signature(fp); sb <- path_signature(lf)
      agree <- vapply(names(sa), function(k) identical(sa[[k]], sb[[k]]), TRUE)
      r$full_path_same <- all(agree); r$full_path_diff <- paste(names(agree)[!agree], collapse = ",")
      lo <- lo_parts(lf); w <- exp(lf$log_Z_r - lse(lf$log_Z_r))
      r$full_eta_pooled <- abs((lse(fp$log_Z_r) - lse(lf$log_Z_r)) - sum(w * lo))
      r$full_hpm_same <- identical(fp$hpm, lf$hpm)
    }
  }
  rows[[length(rows) + 1]] <- r
}
tab <- do.call(rbind, lapply(rows, function(r) { r[setdiff(Reduce(union, lapply(rows, names)), names(r))] <- NA; r }))
dir.create(resd, showWarnings = FALSE, recursive = TRUE)
write.csv(tab, file.path(resd, "valfp_table.csv"), row.names = FALSE)
if (length(detail)) write.csv(do.call(rbind, detail), file.path(resd, "valfp_islands.csv"), row.names = FALSE)
options(width = 250); print(tab)
k <- sum(!tab$path_same, na.rm = TRUE); n <- sum(!is.na(tab$path_same))
cat(sprintf("\nreplays: %d, path disagreements: %d; Clopper-Pearson 95%% upper bound on eps: %.4f\n", n, k,
            if (n) qbeta(0.95, k + 1, n - k) else NA))
cat(sprintf("eta (pooled log Zhat, max over fits): %.3e ; eta_r (max over fits and islands): %.3e\n",
            max(tab$eta_pooled, na.rm = TRUE), max(tab$eta_r_max, na.rm = TRUE)))

# ---- GUARD checks: guarded production fit vs the guard-free run (runtime = NULL, no preflight), bitwise ----
g <- list()
for (id in 1:10) {
  fp <- rd(id, "fp"); ng <- rd(id, "fp_nullguard"); stp <- rd(id, "fp_stop")
  if (is.null(fp) || is.null(ng)) next
  sa <- path_signature(fp); sb <- path_signature(ng)
  agree <- vapply(names(sa), function(k) identical(sa[[k]], sb[[k]]), TRUE)
  fz <- function(z) z[c("tier", "grid", "inherited")]
  g[[length(g) + 1]] <- data.frame(id = id, frozen_identical = identical(fz(fp$frozen), fz(ng$frozen)),
    path_identical = all(agree), log_Z_r_identical = identical(fp$log_Z_r, ng$log_Z_r),
    pip_r_identical = identical(unname(fp$pip_r), unname(ng$pip_r)), hpm_F_identical = identical(fp$hpm_F, ng$hpm_F),
    stop_status = if (is.null(stp)) NA else stp$status,
    stop_estimates_available = if (is.null(stp)) NA else isTRUE(stp$estimates_available),
    stop_hpm_incomplete = if (is.null(stp)) NA else isTRUE(stp$hpm_incomplete),
    stop_has_log_Z = if (is.null(stp)) NA else ("log_Z" %in% names(stp)),
    stop_dollar_log_Z_equals_log_Zbar0 = if (is.null(stp)) NA else identical(stp$log_Z, stp[["log_Zbar0"]]),
    stop_checkpoint = if (is.null(stp) || !length(stp$last_checkpoint)) NA else stp$last_checkpoint[[1]]$checkpoint,
    stop_phase = if (is.null(stp) || !length(stp$last_checkpoint)) NA else stp$last_checkpoint[[1]]$phase)
}
if (length(g)) { g <- do.call(rbind, g); write.csv(g, file.path(resd, "guard_table.csv"), row.names = FALSE); cat("\nGUARD\n"); print(g) }
# ---- multi-seed final-run replays (10 extra final seeds per frozen C) ----
m <- list()
for (id in 1:10) {
  a <- rd(id, "fp_seeds"); b <- rd(id, "ld_seeds")
  if (is.null(a) || is.null(b)) next
  for (k in seq_along(a$runs)) {
    x <- a$runs[[k]]; y <- b$runs[[k]]
    sa <- path_signature(x); sb <- path_signature(y)
    agree <- vapply(names(sa), function(z) identical(sa[[z]], sb[[z]]), TRUE)
    lo <- lo_parts(y); w <- exp(y$log_Z_r - lse(y$log_Z_r))
    m[[length(m) + 1]] <- data.frame(id = id, final_seed = x$final_seed, status_fp = x$status, status_ld = y$status,
      path_same = all(agree), path_diff = paste(names(agree)[!agree], collapse = ","),
      eta_r_max = max(abs((x$log_Z_r - y$log_Z_r) - lo)),
      eta_pooled = abs((lse(x$log_Z_r) - lse(y$log_Z_r)) - sum(w * lo)),
      pip_maxdiff = max(abs(x$pip_r - y$pip_r)), hpm_same = identical(x$hpm, y$hpm))
  }
}
if (length(m)) {
  m <- do.call(rbind, m); write.csv(m, file.path(resd, "valfp_seeds.csv"), row.names = FALSE)
  k <- sum(!m$path_same); n <- nrow(m)
  cat(sprintf("\nmulti-seed: %d final-run replays, %d path disagreements, CP95 upper on eps %.4f; eta pooled max %.3e, eta_r max %.3e, pip maxdiff %.3e\n",
              n, k, qbeta(0.95, k + 1, n - k), max(m$eta_pooled), max(m$eta_r_max), max(m$pip_maxdiff)))
  print(m[!m$path_same, ])
}
