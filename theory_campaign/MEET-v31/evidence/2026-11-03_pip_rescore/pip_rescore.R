# pip_rescore.R -- equal-weight vs Zhat-weighted PIP (METHODOLOGY_v3 §6.11), read-only on all inputs.
# Part A: every locally available fit object that carries per-island log_Z_r and pip_r for a study design.
# Part B: per-cell MPM_eq (pip05) and HPM exact counts for the 2,400-fit study from the scored production tables
#         + per-fit HPM==S0 recount from the S-ELS ledger (no per-island data exist locally for these fits).
OUT  <- "/tmp/claude-71711/-home-fb31--t3-worktrees-Bayesian-Variable-Selection-theory-MEET-v31/14bcdd62-deb0-4c36-99c9-68518a64c746/scratchpad/pip_rescore"
REPO <- "/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/theory-MEET-v31"
MA   <- "/home/fb31/api_workers/METH-AUDIT/theory_campaign/METH-AUDIT/results"
ABL  <- "/home/fb31/abl_work/fits"
TRUTH <- "/home/fb31/ls0_work/study/truth"

score_one <- function(src, id, scale, variant, logZr, P, S0, hpm, saved_eq = NULL, saved_zw = NULL) {
  orig <- if (!is.null(rownames(P))) as.integer(rownames(P)) else seq_len(nrow(P))
  R <- ncol(P)
  pip_eq <- rowMeans(P)
  w <- exp(logZr - max(logZr)); W <- w / sum(w)
  pip_zw <- as.vector(P %*% W)
  d <- abs(pip_zw - pip_eq)
  mpm_eq <- sort(orig[pip_eq > 0.5]); mpm_zw <- sort(orig[pip_zw > 0.5])
  S0 <- sort(as.integer(S0)); hpm <- sort(as.integer(hpm))
  ham <- function(a, b) length(setdiff(a, b)) + length(setdiff(b, a))
  data.frame(source = src, id = id, scale = scale, variant = variant, R = R, p = nrow(P),
    eq_vs_saved_maxabs = if (is.null(saved_eq)) NA else max(abs(pip_eq - saved_eq)),
    zw_vs_saved_maxabs = if (is.null(saved_zw)) NA else max(abs(pip_zw - saved_zw)),
    logZr_range = diff(range(logZr)), W_max = max(W), ESS_isl = 1 / sum(W^2),
    max_abs_dPIP = max(d), argmax_j = orig[which.max(d)],
    n_near_half_eq = sum(abs(pip_eq - 0.5) < 0.1), n_near_half_zw = sum(abs(pip_zw - 0.5) < 0.1),
    mpm_eq_eq_S0 = identical(mpm_eq, S0), mpm_zw_eq_S0 = identical(mpm_zw, S0),
    mpms_differ = !identical(mpm_eq, mpm_zw),
    ham_eq = ham(mpm_eq, S0), ham_zw = ham(mpm_zw, S0),
    hpm_eq_S0 = identical(hpm, S0), stringsAsFactors = FALSE)
}

## ---------------- Part A ----------------
rows <- list()
for (f in sort(list.files(MA, pattern = "^fit_.*\\.rds$", full.names = TRUE))) {
  x <- readRDS(f)
  # prod: production-configuration serial re-run (R = 4); r4: concurrent R = 4 (bitwise check); rbig: R = 32
  rows[[length(rows) + 1]] <- score_one(f, x$id, x$scale, "prod(R=4,serial)", x$prod$log_Z_r, x$prod$pip_r,
                                        x$S0, x$prod$hpm, saved_eq = x$prod$pip)
  rows[[length(rows) + 1]] <- score_one(f, x$id, x$scale, "r4(R=4,concurrent)", x$r4$log_Z_r, x$r4$pip_r,
                                        x$S0, x$r4$hpm, saved_eq = x$r4$pip_eq, saved_zw = x$r4$pip_zw)
  rows[[length(rows) + 1]] <- score_one(f, x$id, x$scale, "rbig(R=32,N=312)", x$rbig$log_Z_r, x$rbig$pip_r,
                                        x$S0, x$rbig$hpm, saved_eq = x$rbig$pip_eq, saved_zw = x$rbig$pip_zw)
}
for (f in sort(list.files(ABL, pattern = "\\.rds$", full.names = TRUE))) {
  x <- readRDS(f)
  if (is.null(x$pip_r) || is.null(x$log_Z_r)) next
  P <- x$pip_r; if (is.null(rownames(P)) && !is.null(x$orig)) rownames(P) <- x$orig
  rows[[length(rows) + 1]] <- score_one(f, x$id, x$scale, paste0("ABL arm ", x$arm, " (mode ", x$mode, ")"),
                                        x$log_Z_r, P, x$S0, x$hpm, saved_eq = x$pip_eq, saved_zw = x$pip_zw)
}
A <- do.call(rbind, rows)
# truth cross-check against study truth files
A$S0_matches_truth_file <- NA
for (i in seq_len(nrow(A))) {
  tf <- file.path(TRUTH, substr(A$id[i], 1, 5), paste0(A$id[i], ".rds"))
  if (file.exists(tf)) {
    t <- readRDS(tf); s <- if (is.list(t)) (t$S0 %||% t$support %||% t$active) else t
    if (!is.null(s)) {
      x <- readRDS(A$source[i]); A$S0_matches_truth_file[i] <- identical(sort(as.integer(s)), sort(as.integer(x$S0)))
    }
  }
}
write.csv(A, file.path(OUT, "partA_per_island_subset.csv"), row.names = FALSE)

## ---------------- Part B ----------------
er <- do.call(rbind, lapply(c("p0500", "p1000"), function(p)
  read.csv(file.path(REPO, "Results/SMC_BVS_v3_production", p, "exact_recovery_long.csv"), stringsAsFactors = FALSE)))
er <- er[er$method_id == "SMCBVS" & er$n_success > 0, ]
B <- merge(
  setNames(er[er$rule_id == "pip05", c("p","scale_key","scenario","n_expected","n_success","exact_all_sum")],
           c("p","scale_key","scenario","n_expected","n_completed","MPM_eq_eq_S0")),
  setNames(er[er$rule_id == "hpm", c("p","scale_key","scenario","exact_all_sum")],
           c("p","scale_key","scenario","HPM_eq_S0_table")))
led <- read.csv("/home/fb31/ls0_work/sels_ledger_per_fit.csv", stringsAsFactors = FALSE)
led$hpm_ok <- led$native_status == "completed" & led$S_hat == led$S0
agg <- aggregate(cbind(n_led = 1, completed_led = led$native_status == "completed", HPM_eq_S0_ledger = led$hpm_ok) ~
                   p + scale_key + scenario, data = led, FUN = sum)
aggP <- aggregate(cbind(n_led = 1, completed_led = led$native_status == "completed", HPM_eq_S0_ledger = led$hpm_ok) ~
                    p + scale_key, data = led, FUN = sum); aggP$scenario <- "pooled"
B <- merge(B, rbind(agg, aggP[, names(agg)]), all.x = TRUE)
B <- B[order(B$p, -as.numeric(sub("c", "", B$scale_key)), B$scenario), ]
write.csv(B, file.path(OUT, "partB_cell_counts_2400.csv"), row.names = FALSE)
print(A); print(B)
