# W3-P6: one production SMC-BVS v3.1 fit (core as on main, deployed by git archive; no source modified) on a
# strong-factor design with iid Gaussian rows. Derived from W2-SIM scripts/prod_fit.R.
# Usage: Rscript --vanilla p6_fit.R CORE_DIR OUT_JSONL RDS_DIR key=value ...
#   design = cs | fac2 | s5     cs: one-factor compound symmetry, x = sqrt(rho) f + sqrt(1-rho) e
#                               fac2: two strong factors, x_j = sqrt(.35) f1 + sqrt(.25) (-1)^j f2 + sqrt(.40) e_j
#                                     (corr .60 within parity class, .10 across)
#                               s5: block CS, x_j = sqrt(.3) f + sqrt(.4) g_{group(j)} + sqrt(.3) e_j, groups of 5
#                                     consecutive columns (corr .7 within group, .3 across) = W2-SIM "S5" correlations
#   n, p, rho (cs), s0 (4 | 8), rep, arm = mr1 | wide, hours, mem_gb, savefull = 0 | 1
# arm = wide: documented testing option v3.ls0_ell = ell_n + K (K = min(p, floor(n/2))), so the merged cap rule gives
#   LS0 cap ell_n + K + |S~0| >= ell_n + 2|S~0|. LS0 is deterministic, reads no uniforms and runs last, so the wide run
#   contains the MR1 run (cap ell_n + |S~0|) and the cap-2 run (ell_n + 2|S~0|) as prefixes: their LS0 outcome and HPM
#   are derived here from the recorded path (validated against paired arm = mr1 runs, see DESIGN.md).
# Truth: S0_k = (k-1) step + 3 + ((k-1) mod 2), step = floor(p/s0) rounded down to even (p6_common.R p6_truth; v1 used
#   floor(p/s0), identical when it is even);
#   beta = (1.4, 1.0, 1.8, 1.2) repeated, aligned signs; sigma = 1.
# Seeds: data_seed = (7919 rep + 13 n + p + 1000003 dcode + 50021 s0 + 7 round(1000 rho)) mod (2^31 - 4e6 - 2);
#   method_seed = data_seed + 4,000,000 (study convention). Paired arms share data and method seed.
args <- commandArgs(trailingOnly = TRUE)
CORE <- args[1]; OUT <- args[2]; RDSDIR <- args[3]
source(file.path(CORE, "v3.R"))
source("p6_common.R")   # frozen next to this script in the run's scripts dir
kv <- strsplit(args[-(1:3)], "=", fixed = TRUE)
A <- setNames(lapply(kv, `[`, 2), vapply(kv, `[`, "", 1))
g <- function(k, d) if (is.null(A[[k]])) d else A[[k]]
design <- g("design", "cs"); n <- as.integer(g("n", 100)); p <- as.integer(g("p", 250))
rho <- as.numeric(g("rho", if (design == "cs") 0.5 else 0)); s0 <- as.integer(g("s0", 4)); rep <- as.integer(g("rep", 1))
arm <- g("arm", "wide"); hours <- as.numeric(g("hours", 22.5)); mem_gb <- as.numeric(g("mem_gb", 8))
tag <- g("tag", "")
suppressMessages(library(jsonlite))
stopifnot(design %in% c("cs", "fac2", "s5"), arm %in% c("mr1", "wide"), s0 >= 1)
S0 <- p6_truth(p, s0)   # v2 (R01-8): even step, alternating parity
if (design == "s5" && length(unique((S0 - 1L) %/% 5L)) < s0) stop("s5: truths share a group")
beta0 <- rep_len(c(1.4, 1.0, 1.8, 1.2), s0)
dcode <- match(design, c("cs", "fac2", "s5"))
data_seed <- as.integer((7919 * rep + 13 * n + p + 1000003 * dcode + 50021 * s0 + 7 * round(1000 * rho)) %% (2^31 - 4e6 - 2))
method_seed <- data_seed + 4000000L

make_X <- function() {
  set.seed(data_seed)
  E <- matrix(rnorm(n * p), n, p)
  if (design == "cs") return(sqrt(rho) * rnorm(n) + sqrt(1 - rho) * E)
  if (design == "fac2") {
    f1 <- rnorm(n); f2 <- rnorm(n); sg <- ifelse(seq_len(p) %% 2L == 0L, 1, -1)
    return(outer(f1, rep(sqrt(0.35), p)) + outer(f2, sqrt(0.25) * sg) + sqrt(0.40) * E)
  }
  f <- rnorm(n); G <- matrix(rnorm(n * ceiling(p / 5)), n); grp <- (seq_len(p) - 1L) %/% 5L + 1L
  sqrt(0.3) * f + sqrt(0.4) * G[, grp, drop = FALSE] + sqrt(0.3) * E
}
X <- make_X()
beta <- numeric(p); beta[S0] <- beta0
set.seed(data_seed + 1L)
y <- as.vector(X %*% beta + rnorm(n))
ell <- ceiling(log2(n + p + 1)); K <- min(p, n %/% 2)
if (arm == "wide") options(v3.ls0_ell = ell + K)
t0 <- proc.time()[["elapsed"]]
fit <- tryCatch(v3_fit(X, y, seed = method_seed, allocation = list(mem_gb = mem_gb, hours = hours)),
                error = function(e) list(status = paste0("R_error: ", conditionMessage(e))))
el <- proc.time()[["elapsed"]] - t0
if (g("savefull", "0") == "1")
  saveRDS(fit, file.path(RDSDIR, sprintf("FULL_%s_r%.2f_n%d_p%d_s%d_r%03d_%s%s.rds", design, rho, n, p, s0, rep, arm, tag)))
key <- function(S) paste(sort(as.integer(S)), collapse = ",")
s0k <- key(S0)
mod <- function(x) if (is.list(x)) x$model else x
nz <- function(x) if (is.null(x)) NA else x
eqS0 <- function(S) if (is.null(S)) NA else key(S) == s0k

# Direct scores of S0 and of the reported HPM (same scorer as the fit; context rebuilt from the same inputs).
F_S0 <- F_hpm <- NA_real_
sc <- tryCatch({
  pre <- v3_preprocess(X, y, dup_components = FALSE)
  ctx <- v3_context(pre$X, pre$y, orig = pre$kept, return_gram = FALSE)
  list(S0 = v3_score(ctx, S0)$F, hpm = if (!is.null(fit$hpm)) v3_score(ctx, as.integer(fit$hpm))$F else NA_real_)
}, error = function(e) list(S0 = NA_real_, hpm = NA_real_, err = conditionMessage(e)))
F_S0 <- sc$S0; F_hpm <- sc$hpm

sm <- mod(fit$start_mode); ls0 <- fit$ls0
nbr <- function(C) { a <- setdiff(C, S0); b <- setdiff(S0, C); (length(a) + length(b) <= 1) || (length(a) == 1 && length(b) == 1) }
first_scoring <- first_arrival <- NA_integer_; moves <- character(0)
if (!is.null(ls0$scanned_centres)) {
  sc_c <- ls0$scanned_centres
  for (t in seq_along(sc_c)) {
    C <- as.integer(sc_c[[t]])
    if (is.na(first_arrival) && key(C) == s0k) first_arrival <- t
    if (is.na(first_scoring) && nbr(C)) first_scoring <- t
  }
  pth <- c(list(sc_c[[1]]), ls0$path)
  if (length(pth) >= 2) moves <- vapply(2:length(pth), function(i) {
    a <- as.integer(pth[[i - 1]]); b <- as.integer(pth[[i]])
    ins <- length(setdiff(b, a)); outs <- length(setdiff(a, b))
    if (ins == 1 && outs == 1) "swap" else if (ins == 1 && outs == 0) "add" else if (outs == 1 && ins == 0) "del" else "other"
  }, "")
}
lead_swaps <- if (length(moves)) { r <- rle(moves); if (r$values[1] == "swap") r$lengths[1] else 0L } else NA_integer_

msize <- length(sm)
cap_mr1 <- ell + msize; cap_2 <- ell + 2L * msize
hb0 <- if (is.null(fit$hpm_before_ls0)) NULL else list(model = fit$hpm_before_ls0$model, F = fit$hpm_before_ls0$F)
d_mr1 <- p6_derive(cap_mr1, ls0, hb0, first_scoring, s0k); d_2 <- p6_derive(cap_2, ls0, hb0, first_scoring, s0k)
hb <- fit$hpm_before_ls0; hl <- fit$hpm_before_local
cal <- fit$calibration
prov <- function(pv) if (is.null(pv)) NA else paste(pv$phase, pv$mechanism, sep = "/")
rec <- list(design = design, rho = rho, n = n, p = p, p_over_n = p / n, s0 = s0, S0 = S0, rep = rep, arm = arm, tag = tag,
  data_seed = data_seed, method_seed = method_seed, hours = hours, mem_gb = mem_gb,
  status = nz(fit$status), message = nz(fit$message), elapsed_sec = round(el, 1), branch = nz(fit$branch_run),
  ell = nz(fit$budgets$ell), K = nz(fit$budgets$K), B = nz(fit$budgets$B), N0 = nz(fit$budgets$N0),
  preflight_exceeds = nz(fit$preflight$exceeds), preflight_est_bytes = nz(fit$preflight$est_bytes),
  preflight_ls0_est_seconds = nz(fit$preflight$ls0_worst_case$est_seconds),
  preflight_ls0_sec_per_score = nz(fit$preflight$ls0_worst_case$seconds_per_score),
  cal_status = nz(cal$status), cal_tier_final = nz(cal$tier_final), cal_escalated = nz(cal$escalated),
  cal_grid_fallback = nz(cal$grid_fallback), cal_triggers = nz(cal$flags$triggers_fired),
  cal_hpm_eq_S0 = eqS0(cal$hpm$model), cal_hpm_prov = prov(cal$hpm$provenance),
  hpm = sort(as.integer(fit$hpm)), hpm_size = length(fit$hpm), hpm_eq_S0 = if (length(fit$hpm)) key(fit$hpm) == s0k else FALSE,
  hpm_incomplete = isTRUE(fit$hpm_incomplete), hpm_F = nz(fit$hpm_F), hpm_prov = prov(fit$hpm_provenance),
  hpm_prov_tier = nz(fit$hpm_provenance$tier), hpm_prov_phi = nz(fit$hpm_provenance$phi),
  F_S0 = F_S0, F_hpm_direct = F_hpm, S0_beats_hpm = isTRUE(F_S0 > F_hpm + 1e-8), score_err = nz(sc$err),
  hpm_before_local_eq_S0 = eqS0(mod(hl)), hpm_before_local_F = nz(hl$F),
  hpm_before_ls0_eq_S0 = eqS0(mod(hb)), hpm_before_ls0_F = nz(hb$F), hpm_before_ls0_prov = prov(hb$provenance),
  final_ls_moves = nz(fit$local_search$moves), final_ls_limit = nz(fit$local_search$local_limit),
  local_certified = nz(fit$local_certified), local_certified_by = nz(fit$local_certified_by), local_limit = nz(fit$local_limit),
  flags_checks_passed_final = nz(fit$flags$checks_passed_final), flags_E1 = nz(fit$flags$E1), flags_E2 = nz(fit$flags$E2),
  flags_E3 = nz(fit$flags$E3), flags_lowESS = nz(fit$flags$low_empirical_ESS),
  start_mode_size = msize, start_mode_has_S0 = if (msize) all(S0 %in% sm) else NA,
  start_mode_truths_missing = if (msize) setdiff(S0, sm) else NA,
  ls0_move_cap = nz(ls0$move_cap), ls0_moves = nz(ls0$moves), ls0_termination = nz(ls0$termination),
  ls0_local_limit = nz(ls0$local_limit), ls0_returned_eq_S0 = eqS0(ls0$returned), ls0_n_evaluated = nz(ls0$n_evaluated),
  ls0_first_scoring_scan = first_scoring, ls0_first_arrival_scan = first_arrival, ls0_lead_swaps = lead_swaps,
  ls0_n_swap = sum(moves == "swap"), ls0_n_del = sum(moves == "del"), ls0_n_add = sum(moves == "add"),
  ls0_moves_seq = if (length(moves)) { r <- rle(moves); paste0(substr(r$values, 1, 1), r$lengths, collapse = " ") } else "",
  cap_mr1 = cap_mr1, cap_2 = cap_2,
  mr1_ls0_scores_S0 = d_mr1$scores, mr1_hpm_eq_S0 = d_mr1$hpm_eq_S0, mr1_status = d_mr1$status, mr1_hpm = d_mr1$model,
  mr1_hpm_F = d_mr1$F, mr1_class = p6_class(d_mr1$hpm_eq_S0, d_mr1$F, F_S0),
  cap2_ls0_scores_S0 = d_2$scores, cap2_hpm_eq_S0 = d_2$hpm_eq_S0, cap2_status = d_2$status, cap2_hpm = d_2$model,
  cap2_hpm_F = d_2$F, cap2_class = p6_class(d_2$hpm_eq_S0, d_2$F, F_S0),
  wide_class = p6_class(if (is.null(fit$hpm)) NA else key(fit$hpm) == s0k, if (is.null(fit$hpm_F)) NA else fit$hpm_F, F_S0),
  F_direct_vs_ledger = if (is.na(F_hpm) || is.null(fit$hpm_F)) NA else abs(F_hpm - fit$hpm_F),
  preflight_escalation_exceeds = nz(fit$preflight_escalation$exceeds), cal_escalation_blocked = nz(cal$escalation_blocked),
  ls0_improved = nz(fit$ls0_improved), ls0_hpm_changed = nz(fit$ls0_hpm_changed),
  t_total = nz(fit$timings$total), t_setup = nz(fit$timings$setup_total), t_calibration = nz(fit$timings$calibration),
  t_final = nz(fit$timings$final), t_local = nz(fit$timings$final_detail$local), t_ls0 = nz(fit$timings$final_detail$ls0),
  peak_mem_kb = nz(fit$peak_memory_kb),
  core_dir = CORE, host = Sys.info()[["nodename"]], slurm_job = Sys.getenv("SLURM_JOB_ID"),
  slurm_array_task = Sys.getenv("SLURM_ARRAY_TASK_ID"), R = R.version.string)
cat(toJSON(rec, auto_unbox = TRUE, null = "null", na = "null", digits = NA), "\n", file = OUT, append = TRUE, sep = "")
keep <- fit[intersect(names(fit), c("status", "message", "budgets", "preflight", "start_mode", "hpm", "hpm_F", "hpm_provenance",
  "hpm_before_ls0", "hpm_before_local", "local_limit", "local_certified", "local_certified_by", "timings", "flags", "branch_run"))]
keep$ls0 <- ls0[setdiff(names(ls0), "scanned_centres")]
keep$cal_summary <- list(status = cal$status, tier_final = cal$tier_final, escalated = cal$escalated, flags = cal$flags,
                         hpm = cal$hpm, seconds = cal$seconds)
keep$rec <- rec
saveRDS(keep, file.path(RDSDIR, sprintf("%s_r%.2f_n%d_p%d_s%d_r%03d_%s%s.rds", design, rho, n, p, s0, rep, arm, tag)), compress = "xz")
cat(sprintf("%s rho=%.2f n=%d p=%d s0=%d rep=%d arm=%s status=%s %.0fs hpm==S0 %s (before_local %s, before_ls0 %s) start %d ls0 moves %s cap %s first_scoring %s | mr1 %s cap2 %s\n",
  design, rho, n, p, s0, rep, arm, rec$status, el, rec$hpm_eq_S0, rec$hpm_before_local_eq_S0, rec$hpm_before_ls0_eq_S0, msize,
  rec$ls0_moves, rec$ls0_move_cap, first_scoring, d_mr1$hpm_eq_S0, d_2$hpm_eq_S0))
