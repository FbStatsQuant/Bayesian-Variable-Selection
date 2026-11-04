# summarise.R -- ABL-CONF: per-fit metrics against the FIXED reference (PREREG sections 5-6).
# Usage (under owls_run): Rscript summarise.R <queue.txt> <out_dir>      [ABL_WORK, default /home/fb31/ablconf_work]
# Reads $ABL_WORK/status/<name>.txt (terminal outcome + process wall time) and $ABL_WORK/fits/<name>.rds.
# Writes <out_dir>/per_fit.csv (one row per queued fit, incl. not-yet-run ones as status "pending") and
#        <out_dir>/reference.csv (one row per design: reference log Z, its error, guard check).
# Reference (per design, fixed in advance): pool of the DELIVERED role-refA fits (reserved seeds, arm A).
#   log Z_ref  = log mean of all pooled island Zhat_r (each island Zhat_r is unbiased for Z);
#   se_ref     = SD over pooled fits of the fit-level log Zhat / sqrt(K)   (K = delivered refA fits);
#   PIP_ref    = Zhat_r-weighted mean of all pooled island PIP vectors.
# Guard (S1 only): the same construction on the role-refB fits (arm B, reserved seeds) -> log Z_refB, se_refB.
# Best-known mode per design: argmax F over the HPMs of every delivered fit of the design (all roles/arms) and S0.
`%||%` <- function(a, b) if (is.null(a)) b else a
args <- commandArgs(TRUE)
W <- Sys.getenv("ABL_WORK", "/home/fb31/ablconf_work")
Q <- read.table(args[1], comment.char = "#", col.names = c("name", "id", "scale", "arm", "off", "role", "k"),
                stringsAsFactors = FALSE)
outdir <- args[2]; dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
lse <- function(x) { m <- max(x); m + log(sum(exp(x - m))) }
rd_status <- function(nm) {
  f <- file.path(W, "status", paste0(nm, ".txt"))
  if (!file.exists(f)) return(list(outcome = "pending", wall = NA_real_))
  tok <- strsplit(readLines(f, n = 1), " ")[[1]]
  kv <- setNames(sub("^[^=]*=", "", tok[-(1:2)]), sub("=.*", "", tok[-(1:2)]))
  list(outcome = tok[2], wall = as.numeric(kv[["wall_s"]]), rc = as.integer(kv[["rc"]]), cap = as.numeric(kv[["cap_s"]]))
}
fits <- list(); st <- list()
for (i in seq_len(nrow(Q))) {
  nm <- Q$name[i]; st[[nm]] <- rd_status(nm)
  f <- file.path(W, "fits", paste0(nm, ".rds"))
  if (st[[nm]]$outcome == "completed" && file.exists(f)) fits[[nm]] <- readRDS(f)
}
# delivered = process completed within the cap, fit status "completed", finite log Zhat
delivered <- function(nm) !is.null(fits[[nm]]) && identical(fits[[nm]]$status, "completed") &&
  is.finite(fits[[nm]]$log_Z %||% NA) && (st[[nm]]$wall %||% Inf) <= (st[[nm]]$cap %||% 4500)
pool <- function(nms) {
  nms <- nms[vapply(nms, delivered, TRUE)]
  if (!length(nms)) return(NULL)
  lzr <- unlist(lapply(nms, function(n) fits[[n]]$log_Z_r)); P <- do.call(cbind, lapply(nms, function(n) fits[[n]]$pip_r))
  w <- exp(lzr - max(lzr)); w <- w / sum(w)
  lzf <- vapply(nms, function(n) fits[[n]]$log_Z, 0)
  list(K = length(nms), n_islands = length(lzr), log_Z = lse(lzr) - log(length(lzr)),
       se = if (length(lzf) > 1) sd(lzf) / sqrt(length(lzf)) else NA_real_, sd_fit = if (length(lzf) > 1) sd(lzf) else NA_real_,
       pip = as.vector(P %*% w), names = nms)
}
designs <- unique(paste(Q$id, Q$scale))
REF <- list(); refrows <- list(); best <- list()
for (d in designs) {
  dq <- Q[paste(Q$id, Q$scale) == d, ]
  ra <- pool(dq$name[dq$role == "refA"]); rb <- pool(dq$name[dq$role == "refB"])
  REF[[d]] <- ra
  # best-known mode
  dn <- dq$name[vapply(dq$name, delivered, TRUE)]
  cand <- lapply(dn, function(n) list(S = fits[[n]]$hpm, F = fits[[n]]$hpm_F))
  if (length(dn)) cand <- c(cand, list(list(S = fits[[dn[1]]]$S0, F = fits[[dn[1]]]$F_S0)))
  Fs <- vapply(cand, function(x) if (is.null(x$F) || is.na(x$F)) -Inf else x$F, 0)
  best[[d]] <- if (length(cand)) cand[[which.max(Fs)]] else NULL
  refrows[[d]] <- data.frame(design = d, scen = sub("^[^_]*_(S[0-9]).*", "\\1", d),
    K = ra$K %||% 0L, n_islands = ra$n_islands %||% 0L, log_Zref = ra$log_Z %||% NA, se_ref = ra$se %||% NA,
    sd_fit_ref = ra$sd_fit %||% NA,
    KB = rb$K %||% 0L, log_ZrefB = rb$log_Z %||% NA, se_refB = rb$se %||% NA,
    refA_vs_refB = if (!is.null(ra) && !is.null(rb)) ra$log_Z - rb$log_Z else NA,
    pipref_A_vs_B_max = if (!is.null(ra) && !is.null(rb)) max(abs(ra$pip - rb$pip)) else NA,
    best_F = if (length(Fs)) max(Fs) else NA, best_size = length(best[[d]]$S),
    best_is_S0 = if (length(dn)) identical(best[[d]]$S, fits[[dn[1]]]$S0) else NA, stringsAsFactors = FALSE)
}
rows <- list()
for (i in seq_len(nrow(Q))) {
  q <- Q[i, ]; nm <- q$name; s <- st[[nm]]; f <- fits[[nm]]; d <- paste(q$id, q$scale); ref <- REF[[d]]
  dl <- delivered(nm)
  status <- if (s$outcome == "completed") (if (dl) "completed" else paste0("fit_", f$status %||% "noresult")) else s$outcome
  cal <- f$cal
  ev_cal <- if (!is.null(cal$ledger_counts$fresh)) sum(cal$ledger_counts$fresh) else NA
  ev_fin <- if (!is.null(f$score_counts$fresh)) sum(f$score_counts$fresh) - sum(f$score_counts$fresh["table", ]) else NA
  pe <- if (dl && !is.null(ref)) abs(f$pip_eq - ref$pip) else NULL
  pz <- if (dl && !is.null(ref)) abs(f$pip_zw - ref$pip) else NULL
  rows[[i]] <- data.frame(name = nm, design = d, scen = sub("^[^_]*_(S[0-9]).*", "\\1", q$id), role = q$role,
    arm = q$arm, k = q$k, seed = if (!is.null(f)) f$seed else NA, status = status,
    wall_s = s$wall, wall_fit_s = f$wall %||% NA, sec_cal = f$timings$calibration %||% NA, sec_final = f$timings$final %||% NA,
    evals_cal = ev_cal, evals_final = ev_fin, evals_total = ev_cal + ev_fin,
    rebuilds = if (!is.null(cal)) sum(vapply(cal$tiers, function(a) as.numeric(a$rebuilds %||% NA), 0)) else NA,
    tier = f$tier %||% NA, T_final = f$T_final %||% NA, escalated = if (!is.null(cal)) isTRUE(cal$escalated) else NA,
    log_Z = if (dl) f$log_Z else NA, sd_logZ_r = if (dl) sd(f$log_Z_r) else NA,
    log_Zref = ref$log_Z %||% NA, se_ref = ref$se %||% NA,
    err_logZ = if (dl && !is.null(ref)) f$log_Z - ref$log_Z else NA,
    pip_eq_max = if (length(pe)) max(pe) else NA, pip_eq_mean = if (length(pe)) mean(pe) else NA,
    pip_zw_max = if (length(pz)) max(pz) else NA, pip_zw_mean = if (length(pz)) mean(pz) else NA,
    hpm_size = if (dl) length(f$hpm) else NA, hpm_eq_best = if (dl) identical(f$hpm, best[[d]]$S) else NA,
    hpm_eq_S0 = if (dl) identical(f$hpm, f$S0) else NA, hpm_F = if (dl) f$hpm_F else NA,
    ess_min_frac = if (dl && length(f$ess_min)) min(f$ess_min) / f$N else NA,
    E1 = isTRUE(f$flags$E1), E2 = isTRUE(f$flags$E2), E3 = isTRUE(f$flags$E3), stringsAsFactors = FALSE)
}
d <- do.call(rbind, rows)
write.csv(d, file.path(outdir, "per_fit.csv"), row.names = FALSE)
write.csv(do.call(rbind, refrows), file.path(outdir, "reference.csv"), row.names = FALSE)
cat(sprintf("fits queued %d | completed %d capped %d failed %d other %d pending %d\n", nrow(d),
  sum(d$status == "completed"), sum(d$status == "capped"), sum(d$status == "failed"),
  sum(!d$status %in% c("completed", "capped", "failed", "pending")), sum(d$status == "pending")))
print(do.call(rbind, refrows)[, c("design", "K", "log_Zref", "se_ref", "KB", "log_ZrefB", "se_refB", "refA_vs_refB")], digits = 5)
