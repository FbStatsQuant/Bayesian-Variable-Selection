# O-CERT: compute the certificate card for each saved fit (deterministic; no randomness).
# Usage: Rscript cert_run.R <lib_dir> <study_root> <fits_dir> <out_file> [m_extra=16] [max_nodes=200000]
a <- commandArgs(TRUE)
source(file.path(a[1], "cert_lib.R"))
root <- a[2]; fdir <- a[3]; outf <- a[4]
m_extra <- if (length(a) >= 5) as.integer(a[5]) else 16L
max_nodes <- if (length(a) >= 6) as.numeric(a[6]) else 2e5
lse <- matrixStats_logsumexp
fits <- list.files(fdir, pattern = "^p0500_.*\\.rds$", full.names = TRUE)
sink(outf, split = TRUE)
for (f in fits) {
  fit <- readRDS(f)
  d <- readRDS(file.path(root, "inputs", "p0500", paste0(fit$dataset_id, ".rds")))
  tr <- readRDS(file.path(root, "truth", "p0500", paste0(fit$dataset_id, ".rds")))
  S0 <- sort(as.integer(tr$active)); dd <- cert_data(d$X, d$Y[, fit$scale_key])
  Sh <- sort(as.integer(fit$hpm)); Fh <- Fscore(dd, Sh); F0 <- Fscore(dd, S0)
  cat("\n==== ", fit$dataset_id, fit$scale_key, " status:", fit$status, " wall(s):", round(fit$wall), "\n")
  cat(sprintf("|S^|=%d  TP=%d FP=%d FN=%d  exact=%s\n", length(Sh), length(intersect(Sh, S0)),
              length(setdiff(Sh, S0)), length(setdiff(S0, Sh)), identical(Sh, S0)))
  # consistency of my score with the engine's (top store values; constant offset if any)
  top <- fit$top_store; tv <- top$value
  chk <- vapply(seq_len(min(5, length(tv))), function(i) Fscore(dd, sort(as.integer(top$models[[i]]))) - tv[i], 0)
  cat("score offset (mine - engine), top 5:", signif(chk, 6), "\n")
  off <- median(chk); Fh_eng <- fit$hpm_F + off
  cat(sprintf("F(S^)=%.4f  F(S0)=%.4f  F(S0)-F(S^)=%.4f  -> %s\n", Fh, F0, F0 - Fh,
              if (identical(Sh, S0)) "correct" else if (F0 <= Fh) "POSTERIOR miss" else "SEARCH miss"))
  # (C3) exact relative certificates
  ls <- local_scan(dd, Sh)
  cat(sprintf("engine local_certified=%s | recomputed: local max=%s, n_nbr=%d, gaps add/del/swap = %.3f/%.3f/%.3f nats\n",
              fit$local_certified, ls$local_max, ls$n_nbr, ls$g_add, ls$g_del, ls$g_swap))
  cat(sprintf("exact local share pi(S^ | closed nbhd) = %.4f\n", exp(ls$log_share)))
  ss <- subset_scan(dd, Sh)
  cat(sprintf("all %d proper subsets of S^: gap g_sub=%.3f, sum pi(S)/pi(S^) over subsets = %.3g\n", ss$n, ss$g_sub, exp(ss$log_ratio_sub)))
  g_top <- tv[1] - tv[2]
  cat(sprintf("best-of-scored gap (top store, %d models) g = %.4f nats  -> pi(S)/pi(S^) <= %.4f for every scored S\n",
              length(tv), g_top, exp(-g_top)))
  # (C1) one-sided global certificate. Z_T from the top store; Zhat from the run (engine scale -> mine via offset)
  lZT <- lse(tv + off); lZh <- fit$log_Z + off; la <- log(0.05)
  u_det <- exp(Fh - lZT); u95 <- exp(Fh - max(lZT, la + lZh))
  cat(sprintf("log Z_T=%.3f  log Zhat=%.3f  log(0.05 Zhat)=%.3f  log Zhat_r sd=%.3f\n", lZT, lZh, la + lZh, sd(fit$log_Z_r)))
  cat(sprintf("pi(S^) <= %.4f surely (top store);  pi(S^) <= %.4f w.p.>=0.95 (C1);  plug-in e^F/Zhat = %.4f\n", u_det, min(1, u95), exp(Fh - lZh)))
  cat(sprintf("posterior mass outside the top store >= %.4f w.p.>=0.95\n", max(0, 1 - exp(lZT - la - lZh))))
  for (v in c(0.25, 1, 4)) {   # (C2) conditional two-sided band under PW2 with B_T = v (NOT data-certified)
    eps <- 0.5; lev <- v / (v + 4 * eps^2)
    cat(sprintf("  [conditional on PW2, B_T=%.2f] pi(S^) >= %.4f except w.p. <= %.3f\n", v, (1 - eps) * exp(Fh - lZh), lev))
  }
  # (C4) box certificate over U = S^ + m_extra candidates ranked by single-addition score, plus whole-box mass bound
  cand <- names(sort(ls$fadd, decreasing = TRUE))[seq_len(m_extra)]
  U <- sort(unique(c(Sh, as.integer(cand))))
  imp <- c(setNames(Fh - ls$fdel, Sh), setNames(ls$fadd[cand] - Fh, cand))   # decisive variables first
  t0 <- Sys.time(); bo <- bnb(dd, Sh, U, "opt", max_nodes = max_nodes, order_score = abs(imp)); t1 <- Sys.time()
  cat(sprintf("box U = S^ + %d candidates (|U|=%d, %.3g models): S0 subset of U: %s; opt-B&B done=%s nodes=%d (%.1fs); better models found: %d\n",
              m_extra, length(U), 2^length(U), all(S0 %in% U), bo$done, bo$nodes, as.numeric(t1 - t0, units = "secs"), length(bo$better)))
  if (length(bo$better)) { b <- bo$better[[which.max(vapply(bo$better, `[[`, 0, "F"))]]
    cat("   best found in U:", b$S, " F - F(S^) =", b$F - Fh, "\n") }
  bm <- bnb(dd, Sh, U, "mass", tau = -12, max_nodes = max_nodes, order_score = abs(imp))
  if (bm$done) cat(sprintf("mass-B&B nodes=%d: sum_{S in 2^U, S!=S^} pi(S)/pi(S^) <= %.4g  =>  pi(S^ | 2^U) >= %.4f\n",
                          bm$nodes, exp(bm$log_rest), 1 / (1 + exp(bm$log_rest))))
  else cat(sprintf("mass-B&B not finished within %d nodes\n", max_nodes))
}
sink()
