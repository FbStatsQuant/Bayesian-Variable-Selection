# diag_lib.R -- design-only diagnostics for ticket W2-APP (Theory Wave 2).
# Everything here depends on X only (except the optional plug-in at the end, which is labelled as such).
# Usage: source("diag_lib.R"); res <- run_design("name", X, y = NULL, source_note = "...")
# Writes (next to the scripts): out_<name>_*.csv, out_<name>.rds ; prints a report to stdout (redirect to out_<name>.txt).

suppressPackageStartupMessages({ library(Rcpp) })
DD <- normalizePath(getwd())                      # run all scripts from data_diag/
stopifnot(file.exists(file.path(DD, "diag_lib.R")))
Sys.setenv(V3_CORE_DIR = file.path(DD, "core_copy"))   # byte-identical copy of Scripts/SMC_BVS/core (SHA256 in core_copy/SOURCE_SHA256.txt)

fmt <- function(x, d = 4) ifelse(is.na(x), "NA", formatC(x, digits = d, format = "g"))
hdr <- function(s) cat("\n", strrep("=", 78), "\n", s, "\n", strrep("=", 78), "\n", sep = "")

# ---- exact triple enumeration (closed form 3x3 min eigenvalue), Rcpp -------------------------------------------------
tripcpp <- file.path(DD, "diag_triples.cpp")
if (!file.exists(tripcpp)) writeLines(c(
'#include <Rcpp.h>',
'#include <cmath>',
'#include <algorithm>',
'#include <vector>',
'using namespace Rcpp;',
'static inline double lmin3(double a, double b, double c) {  // min eigenvalue of [[1,a,b],[a,1,c],[b,c,1]]',
'  double q = a*a + b*b + c*c, t = 2.0*a*b*c;',
'  if (q <= 0) return 1.0;',
'  double arg = (3.0*t/(2.0*q))*std::sqrt(3.0/q); if (arg > 1) arg = 1; if (arg < -1) arg = -1;',
'  double phi = std::acos(arg)/3.0, s = 2.0*std::sqrt(q/3.0), PI = 3.14159265358979323846, m = 1e300;',
'  for (int k = 0; k < 3; ++k) { double x = s*std::cos(phi - 2.0*PI*k/3.0); if (x < m) m = x; }',
'  return 1.0 + m;',
'}',
'// [[Rcpp::export]]',
'List triple_scan(NumericMatrix R, double tol) {',
'  int p = R.nrow(); double best = 1e300;',
'  for (int i = 0; i < p; ++i) for (int j = i+1; j < p; ++j) { double a = R(i,j);',
'    for (int k = j+1; k < p; ++k) { double v = lmin3(a, R(i,k), R(j,k)); if (v < best) best = v; } }',
'  std::vector<int> I, J, K; std::vector<double> V;',
'  for (int i = 0; i < p; ++i) for (int j = i+1; j < p; ++j) { double a = R(i,j);',
'    for (int k = j+1; k < p; ++k) { double v = lmin3(a, R(i,k), R(j,k)); if (v <= best + tol && I.size() < 2000) { I.push_back(i+1); J.push_back(j+1); K.push_back(k+1); V.push_back(v); } } }',
'  return List::create(_["best"] = best, _["i"] = I, _["j"] = J, _["k"] = K, _["v"] = V);',
'}',
'// Gershgorin-pruned exact scan: a triple with lambda_min <= ub has some vertex whose two edges satisfy |r1|+|r2| >= 1-ub,',
'// so it suffices to scan (v,u,w) with |r_vu|+|r_vw| >= thr = 1-ub (rigorous). maxvisit caps the work (returns aborted=TRUE).',
'// [[Rcpp::export]]',
'List triple_pruned(NumericMatrix R, double thr, double maxvisit) {',
'  int p = R.nrow(); double best = 1e300, visited = 0; bool aborted = false;',
'  std::vector<int> I, J, K; std::vector<double> V;',
'  std::vector<std::pair<double,int> > nb(p);',
'  for (int v = 0; v < p && !aborted; ++v) {',
'    int m = 0; for (int u = 0; u < p; ++u) if (u != v) nb[m++] = std::make_pair(-std::fabs(R(v,u)), u);',
'    std::sort(nb.begin(), nb.begin() + m);',
'    for (int a = 0; a < m && !aborted; ++a) { double ra = -nb[a].first; if (2.0*ra < thr) break;',
'      for (int b = a+1; b < m; ++b) { double rb = -nb[b].first; if (ra + rb < thr) break;',
'        visited += 1; if (visited > maxvisit) { aborted = true; break; }',
'        int u = nb[a].second, w = nb[b].second; double val = lmin3(R(v,u), R(v,w), R(u,w));',
'        if (val < best - 1e-6) { I.clear(); J.clear(); K.clear(); V.clear(); }',
'        if (val < best) best = val;',
'        if (val <= best + 1e-6 && I.size() < 2000) { I.push_back(v+1); J.push_back(u+1); K.push_back(w+1); V.push_back(val); } } } }',
'  return List::create(_["best"] = best, _["i"] = I, _["j"] = J, _["k"] = K, _["v"] = V, _["visited"] = visited, _["aborted"] = aborted);',
'}'), tripcpp)
sourceCpp(tripcpp, cacheDir = file.path(DD, ".sourcecpp_cache"), verbose = FALSE)

# ---- preprocessing --------------------------------------------------------------------------------------------------
clean_design <- function(X) {
  X <- as.matrix(X); storage.mode(X) <- "double"
  stopifnot(all(is.finite(X)))
  n <- nrow(X); p0 <- ncol(X)
  const <- apply(X, 2, function(x) all(x == x[1]))
  X1 <- X[, !const, drop = FALSE]
  Z <- scale(X1)                                  # unit sample variance (n-1), centred
  Z <- Z / sqrt(n - 1)                            # now colSums(Z^2) = 1 and R = crossprod(Z)
  R <- crossprod(Z)
  A <- (abs(R) > 1 - 1e-10); diag(A) <- FALSE
  dup <- which(colSums(A & upper.tri(A)) > 0)     # column l is a duplicate of an earlier column
  keep <- setdiff(seq_len(ncol(X1)), dup)
  Z <- Z[, keep, drop = FALSE]; R <- R[keep, keep, drop = FALSE]
  diag(R) <- 1
  orig_idx <- which(!const)[keep]
  list(n = n, p0 = p0, n_const = sum(const), n_dup = length(dup), p = ncol(Z), Z = Z, R = R, orig_idx = orig_idx,
       names = colnames(X)[orig_idx])
}

# ---- m_sharp (capped beta-binomial prior) -------------------------------------------------------------------------------
lse <- function(v) { if (!length(v)) return(-Inf); m <- max(v); if (!is.finite(m)) return(m); m + log(sum(exp(v - m))) }
msharp <- function(n, p, s0) {
  K <- min(p, floor(n / 2)); k <- 0:K
  lw <- function(k) -log(2) - lchoose(2 * p - 1, k)
  term <- lchoose(p, k) + lw(k) - lw(s0)
  thr <- -(s0 + 2) / 2 * log(n)
  for (m in s0:max(K, s0)) {
    idx <- (max(m + 1, 0)):K
    lR <- if (max(m + 1, 0) > K) -Inf else lse(term[idx + 1])
    if (lR <= thr) return(list(m = m, logR = lR, K = K))
  }
  list(m = NA, logR = NA, K = K)
}

# ---- sparse minimum eigenvalues ----------------------------------------------------------------------------------------
lam_min <- function(R, S) min(eigen(R[S, S, drop = FALSE], symmetric = TRUE, only.values = TRUE)$values)

# smallest eigenvalue of R_{S u {j}} for every column j, via the secular equation on (-inf, lambda_min(R_S)); vectorised
# bisection with rigorous bracket pruning (a candidate whose lower bracket exceeds the smallest upper bracket cannot be the argmin;
# pruned candidates get value Inf).  Only the argmin / smallest value is used by the callers.
new_lmin_all <- function(R, S, iters = 50) {
  m <- length(S); p <- ncol(R)
  e <- eigen(R[S, S, drop = FALSE], symmetric = TRUE)
  d <- rev(e$values); Q <- e$vectors[, rev(seq_len(m)), drop = FALSE]
  act <- setdiff(seq_len(p), S)
  W <- crossprod(Q, R[S, act, drop = FALSE])^2        # m x |act|
  lo <- rep(min(0, d[1]) - 1e-6, length(act)); hi <- rep(d[1], length(act))
  for (it in seq_len(iters)) {
    mid <- (lo + hi) / 2
    f <- 1 - mid - colSums(W / (d - rep(mid, each = m)))
    up <- f > 0
    lo <- ifelse(up, mid, lo); hi <- ifelse(up, hi, mid)
    if (it %% 4 == 0 && length(act) > 1) {
      keep <- lo <= min(hi) + 1e-15
      if (!all(keep)) { act <- act[keep]; W <- W[, keep, drop = FALSE]; lo <- lo[keep]; hi <- hi[keep] }
    }
  }
  v <- rep(Inf, p); v[act] <- (lo + hi) / 2
  list(val = v, lmin_S = d[1])
}

greedy_chain <- function(R, start, kmax) {
  S <- start; lam <- numeric(0)
  while (length(S) < kmax) {
    nl <- new_lmin_all(R, S)
    lam[length(S)] <- nl$lmin_S
    S <- c(S, which.min(nl$val))
  }
  lam[length(S)] <- lam_min(R, S)
  list(S = S, lam = lam)                           # lam[k] = exact lambda_min of the first k elements (computed by eigen)
}

# 1-swap local refinement of a set S (steepest improvement), returns improved set.
swap_refine <- function(R, S, maxit = 10, tlimit = 60) {
  t0 <- proc.time()[["elapsed"]]; cur <- lam_min(R, S)
  for (it in seq_len(maxit)) {
    best <- cur; bestS <- NULL
    for (i in seq_along(S)) {
      Sm <- S[-i]
      if (length(Sm) < 1) next
      nl <- if (length(Sm) == 1) { v <- 1 - abs(R[Sm, ]); v[Sm] <- Inf; list(val = v) } else new_lmin_all(R, Sm, iters = 40)
      v <- nl$val; v[S[i]] <- Inf                   # excluding the removed element itself
      j <- which.min(v)
      if (v[j] < best - 1e-12) { cand <- c(Sm, j); lv <- lam_min(R, cand); if (lv < best - 1e-12) { best <- lv; bestS <- cand } }
      if (proc.time()[["elapsed"]] - t0 > tlimit) break
    }
    if (is.null(bestS)) break
    S <- bestS; cur <- best
    if (proc.time()[["elapsed"]] - t0 > tlimit) break
  }
  list(S = S, lam = cur)
}

top_pairs <- function(R, npair = 500) {
  p <- ncol(R); ut <- which(upper.tri(R), arr.ind = FALSE)
  a <- abs(R[ut]); o <- order(a, decreasing = TRUE)[seq_len(min(npair, length(a)))]
  idx <- ut[o]; cbind(i = (idx - 1) %% p + 1, j = (idx - 1) %/% p + 1, r = a[o])
}

sparse_eigs <- function(R, n, ks, restarts = 200, seed = 20261109, tlimit_total = 480, swap_tlimit = 30, maxvisit = 3e9) {
  p <- ncol(R); ks <- sort(unique(ks[ks >= 2 & ks <= p])); kmax <- max(ks)
  t0 <- proc.time()[["elapsed"]]
  tp <- top_pairs(R, 500)
  best <- setNames(rep(Inf, kmax), seq_len(kmax)); bestS <- vector("list", kmax)
  fold <- function(ch) for (k in 2:kmax) if (!is.na(ch$lam[k]) && ch$lam[k] < best[k]) { best[k] <<- ch$lam[k]; bestS[[k]] <<- ch$S[seq_len(k)] }
  # --- chain 1: greedy from the most correlated pair
  ch1 <- greedy_chain(R, c(tp[1, 1], tp[1, 2]), kmax); fold(ch1); used <- 1
  # --- exact values (before the remaining chains, which are seeded with the exact minimisers)
  ex_tab <- list(); exact_sets <- list()
  for (k in ks) {
    ex <- NA_real_; ex_how <- NA_character_; exS <- NULL
    if (k == 2) { ex <- 1 - tp[1, 3]; ex_how <- "exact: 1-max|r|"; exS <- tp[1, 1:2] }
    else if (choose(p, k) <= 2e5) {
      cm <- combn(p, k); v <- apply(cm, 2, function(s) lam_min(R, s)); w <- which.min(v)
      ex <- v[w]; ex_how <- "exact: full enumeration"; exS <- cm[, w]
    } else if (k == 3) {
      sc <- NULL
      if (choose(p, 3) <= 5e7) { sc <- triple_scan(R, 1e-6); how <- "exact: enumeration of all triples" }
      else { sc <- triple_pruned(R, 1 - (best[3] + 1e-6), maxvisit); how <- sprintf("exact: Gershgorin-pruned enumeration (%.3g triples visited)", sc$visited)
             if (isTRUE(sc$aborted)) sc <- NULL }
      if (!is.null(sc) && length(sc$i)) {
        vv <- vapply(seq_along(sc$i), function(t) lam_min(R, c(sc$i[t], sc$j[t], sc$k[t])), 0); w <- which.min(vv)
        ex <- vv[w]; ex_how <- how; exS <- c(sc$i[w], sc$j[w], sc$k[w])
      }
    }
    ex_tab[[as.character(k)]] <- list(ex = ex, how = ex_how, S = exS)
    if (!is.na(ex) && length(exS) >= 2 && length(exS) < kmax) exact_sets[[length(exact_sets) + 1]] <- exS
  }
  # --- chains seeded by exact minimisers, then random restarts among the top-500 pairs
  set.seed(seed)
  starts <- exact_sets
  if (restarts > 0) { sel <- sample(nrow(tp), min(restarts, nrow(tp))); for (s in sel) starts[[length(starts) + 1]] <- c(tp[s, 1], tp[s, 2]) }
  for (ci in seq_along(starts)) {
    fold(greedy_chain(R, starts[[ci]], kmax)); used <- used + 1
    if (proc.time()[["elapsed"]] - t0 > tlimit_total) { cat("[sparse_eigs] time cap hit after", used, "greedy chains\n"); break }
  }
  greedy_best <- best
  # exact sets also witness upper bounds at their own size
  for (k in ks) { e <- ex_tab[[as.character(k)]]; if (!is.na(e$ex) && e$ex < best[k]) { best[k] <- e$ex; bestS[[k]] <- e$S } }
  rows <- list()
  for (k in ks) {
    e <- ex_tab[[as.character(k)]]
    ref <- if (is.na(e$ex)) swap_refine(R, bestS[[k]], tlimit = swap_tlimit) else list(S = bestS[[k]], lam = best[k])
    use_ref <- ref$lam < best[k] - 1e-12
    S <- if (use_ref) ref$S else bestS[[k]]; ub <- min(ref$lam, best[k])
    gers <- 1 - (k - 1) * max(abs(R[upper.tri(R)]))
    rows[[length(rows) + 1]] <- data.frame(k = k, exact = e$ex, exact_method = e$how, exact_set = if (is.null(e$S)) NA else paste(e$S, collapse = ","),
      upper_greedy = greedy_best[k], upper_best = ub, upper_method = if (!is.na(e$ex)) "= exact" else if (use_ref) "greedy+1swap" else "greedy",
      upper_set = paste(S, collapse = ","), gersh_simple = gers, stringsAsFactors = FALSE)
  }
  df <- do.call(rbind, rows)
  # refined Gershgorin: 1 - max_j (sum of the k-1 largest |r_jl|, l != j)
  A <- abs(R); diag(A) <- 0
  ord <- matrix(0, p, min(p - 1, kmax - 1))
  # row-wise partial sums of the sorted off-diagonal entries (chunked to bound memory)
  cs_max <- function(km) { out <- numeric(length(km)); for (a in seq(1, p, by = 512)) { ii <- a:min(p, a + 511); sub <- t(apply(A[ii, , drop = FALSE], 1, function(r) sort(r, decreasing = TRUE)[seq_len(max(km))])); cs <- t(apply(sub, 1, cumsum)); out <- pmax(out, sapply(km, function(m) max(cs[, m]))) }; out }
  km <- df$k - 1; km[km < 1] <- 1
  df$gersh_refined <- 1 - cs_max(km)
  df$lower_bound <- pmax(df$gersh_refined, df$gersh_simple)
  list(table = df, chains_used = used, firstchain = ch1, tp = tp[1:10, , drop = FALSE])
}

# ---- block leakage using the production core ---------------------------------------------------------------------------
load_core <- function() {
  if (!exists("v3_blocks", mode = "function")) source(file.path(DD, "core_copy", "v3.R"), local = FALSE)
}
block_diag <- function(Z, R, y = NULL, seed = 1) {
  n <- nrow(Z); p <- ncol(Z)
  out <- list(ok = FALSE)
  tryCatch({
    load_core()
    B <- v3_budgets(n, p)$B
    sv <- svd(Z, nu = 1, nv = 0)
    set.seed(seed)
    ys <- if (is.null(y)) as.numeric(sv$u[, 1] * sv$d[1] * sqrt(n - 1)) + rnorm(n) else (y - mean(y))
    ys <- ys / sd(ys)
    # v3_context expects standardised columns (centred, sample SD 1): rescale Z by sqrt(n-1)
    Xs <- unname(Z * sqrt(n - 1))
    ctx <- v3_context(Xs, ys, return_gram = FALSE)
    bl <- v3_blocks(ctx, B)
    mem <- integer(p); for (b in seq_along(bl)) mem[bl[[b]]] <- b
    stopifnot(all(mem > 0), sum(lengths(bl)) == p)
    A <- abs(R); diag(A) <- 0
    leak <- vapply(seq_len(p), function(j) { o <- mem != mem[j]; if (!any(o)) NA_real_ else max(A[j, o]) }, 0)
    pr <- which(upper.tri(A) & A > 0.5, arr.ind = TRUE)
    split_frac <- if (nrow(pr) == 0) NA_real_ else mean(mem[pr[, 1]] != mem[pr[, 2]])
    within_max <- vapply(seq_len(p), function(j) { o <- (mem == mem[j]); o[j] <- FALSE; if (!any(o)) NA_real_ else max(A[j, o]) }, 0)
    out <- list(ok = TRUE, B = B, nblocks = length(bl), sizes = lengths(bl), size_hist = table(lengths(bl)), mem = mem, blocks = bl,
                leak = leak, leak_q = quantile(leak, c(.5, .9, 1), na.rm = TRUE), n_pairs_gt05 = nrow(pr), split_frac = split_frac,
                within_max_med = median(within_max, na.rm = TRUE), core_key = V3_CPP_KEY)
  }, error = function(e) { out$err <<- conditionMessage(e); cat("[block_diag] ERROR:", conditionMessage(e), "\n") })
  out
}

# ---- main driver --------------------------------------------------------------------------------------------------------
partner_stats <- function(A, taus = c(.3, .5, .7, .9)) {
  p <- ncol(A); diag(A) <- 0
  t(sapply(taus, function(tau) { cnt <- rowSums(A > tau); c(tau = tau, median = median(cnt), q90 = unname(quantile(cnt, .9)), max = max(cnt)) }))
}

run_design <- function(name, X, y = NULL, source_note = "", restarts = 200, tlimit_total = 480, swap_tlimit = 30, maxvisit = 3e9, do_plugin = !is.null(y)) {
  t_start <- proc.time()[["elapsed"]]
  hdr(paste("DESIGN:", name))
  cat("Source:", source_note, "\n")
  cd <- clean_design(X); n <- cd$n; p <- cd$p; R <- cd$R; Z <- cd$Z
  cat(sprintf("raw: n=%d, p0=%d; dropped constant=%d, duplicate(|r|>1-1e-10)=%d; used p=%d\n", n, cd$p0, cd$n_const, cd$n_dup, p))
  Ahat <- log(p) / log(n)
  cat(sprintf("(a) n=%d p=%d A_hat=log p/log n=%.4f\n", n, p, Ahat))
  res <- list(name = name, source = source_note, n = n, p = p, p0 = cd$p0, n_const = cd$n_const, n_dup = cd$n_dup, Ahat = Ahat)

  # (b) spectrum
  hdr("(b) correlation spectrum")
  sv <- svd(Z, nu = min(10, n, p), nv = 0)
  ev <- sv$d^2                                          # eigenvalues of R (nonzero part when p > n); sum = p
  kk <- min(10, length(ev)); top <- ev[1:kk]
  share <- sapply(c(1, 3, 5, 10), function(k) sum(ev[seq_len(min(k, length(ev)))]) / p)
  names(share) <- c("top1", "top3", "top5", "top10")
  ratios <- ev[1:min(9, length(ev) - 1)] / ev[2:min(10, length(ev))]
  kfac <- which.max(ratios)
  lam_minR <- if (p < n) ev[p] else NA_real_
  cat("top eigenvalues:", paste(fmt(top, 5), collapse = " "), "\n")
  cat("trace share top1/3/5/10:", paste(fmt(share, 4), collapse = " / "), "\n")
  cat(sprintf("lambda_1/p = %.4f\n", ev[1] / p))
  cat("ratios lambda_k/lambda_{k+1}, k=1..9:", paste(fmt(ratios, 4), collapse = " "), "\n")
  cat(sprintf("Ahn-Horenstein ER argmax k = %d (ratio %.3f)\n", kfac, ratios[kfac]))
  cat(sprintf("smallest eigenvalue of R (only if p<n): %s\n", if (is.na(lam_minR)) "NA (p>=n, R singular)" else format(lam_minR, digits = 5)))
  res <- c(res, list(eig_top = top, share = share, ratios = ratios, kfac = kfac, lam_minR = lam_minR, lam1_over_p = ev[1] / p))
  write.csv(data.frame(k = seq_along(top), eigenvalue = top, ratio_to_next = c(ratios, rep(NA, length(top) - length(ratios))),
                       cum_share = cumsum(top) / p), sprintf("out_%s_eigs.csv", name), row.names = FALSE)

  # (c) pairwise structure
  hdr("(c) pairwise structure")
  A <- abs(R); diag(A) <- 0
  maxr <- max(A); fr03 <- sum(A > 0.3) / (p * (p - 1))
  ps <- partner_stats(A)
  cat(sprintf("max|r_jk| = %.4f ; fraction of pairs with |r|>0.3 = %.5f\n", maxr, fr03))
  cat("strong partners per variable (before factor removal):\n"); print(round(ps, 3), row.names = FALSE)
  # residual after removing top-kfac PCs
  U <- sv$u[, seq_len(kfac), drop = FALSE]
  Zr <- Z - U %*% crossprod(U, Z)
  rv <- colSums(Zr^2)                                   # residual share of each column's variance
  okc <- rv > 1e-8
  Zr2 <- sweep(Zr[, okc, drop = FALSE], 2, sqrt(rv[okc]), "/")
  Rr <- crossprod(Zr2); Ar <- abs(Rr); diag(Ar) <- 0
  ps_r <- partner_stats(Ar)
  maxr_r <- max(Ar); fr03_r <- sum(Ar > 0.3) / (ncol(Ar) * (ncol(Ar) - 1))
  cat(sprintf("after removing top-%d PCs: columns kept %d/%d (residual variance share > 1e-8; median share %.4f, min %.2e)\n", kfac, sum(okc), p, median(rv), min(rv)))
  cat(sprintf("residual max|r| = %.4f ; fraction pairs |r|>0.3 = %.5f\n", maxr_r, fr03_r))
  print(round(ps_r, 3), row.names = FALSE)
  res <- c(res, list(maxr = maxr, frac03 = fr03, partners = ps, partners_resid = ps_r, maxr_resid = maxr_r, frac03_resid = fr03_r,
                     resid_cols_kept = sum(okc), resid_share_median = median(rv)))
  write.csv(data.frame(stage = rep(c("raw", sprintf("minus_top%d_PC", kfac)), each = 4), rbind(ps, ps_r)), sprintf("out_%s_partners.csv", name), row.names = FALSE)

  # m_sharp
  hdr("m_sharp (capped beta-binomial prior)")
  Aj <- max(1, Ahat)
  ms <- lapply(c(1, 2, 3, 5), function(s0) msharp(n, p, s0)); names(ms) <- paste0("s0=", c(1, 2, 3, 5))
  j0 <- sapply(c(1, 2, 3, 5), function(s0) ceiling((2 * Aj + 1) * s0) + 1); names(j0) <- names(ms)
  for (i in seq_along(ms)) cat(sprintf("%s: m_sharp=%s (K=%d, log R_m=%s) ; j0=ceil((2A+1)s0)+1=%d (A=%.3f)\n", names(ms)[i], ms[[i]]$m, ms[[i]]$K, fmt(ms[[i]]$logR, 4), j0[i], Aj))
  res$msharp <- sapply(ms, `[[`, "m"); res$j0 <- j0

  # (d) sparse minimum eigenvalues
  hdr("(d) sparse minimum eigenvalues phi^2(k) = min_{|S|=k} lambda_min(R_S)")
  ks <- c(2, 3, 5, 7, 10, ceiling(log(n)), ceiling(2 * log(n)), res$msharp[c("s0=1", "s0=3")] + 1, j0[c("s0=1", "s0=3")])
  kmap <- data.frame(k = ks, label = c("2", "3", "5", "7", "10", "ceil(log n)", "ceil(2 log n)", "m#(s0=1)+1", "m#(s0=3)+1", "j0(s0=1)", "j0(s0=3)"))
  ks_use <- sort(unique(ks[ks <= p & ks >= 2]))
  cat("requested k:", paste(paste0(kmap$label, "=", kmap$k), collapse = "; "), "\n")
  if (any(ks > p)) cat("k > p skipped (NA):", paste(unique(ks[ks > p]), collapse = ","), "\n")
  t1 <- proc.time()[["elapsed"]]
  se <- sparse_eigs(R, n, ks_use, restarts = restarts, tlimit_total = tlimit_total, swap_tlimit = swap_tlimit, maxvisit = maxvisit)
  cat(sprintf("greedy chains used: %d (1 from the most correlated pair + %d random restarts requested); time %.1fs\n", se$chains_used, restarts, proc.time()[["elapsed"]] - t1))
  tb <- se$table; tb$labels <- sapply(tb$k, function(k) paste(kmap$label[kmap$k == k], collapse = "/"))
  tb$lambda_minR_lower <- if (p < n) lam_minR else NA
  cat("Legend: EXACT = true phi^2(k); UPPER = a witness set's lambda_min (phi^2(k) <= value); LOWER = rigorous lower bound.\n")
  cat("        gersh_simple = 1-(k-1)max|r|; gersh_refined = 1-max_j(sum of k-1 largest |r_jl|); lambda_min(R) (Cauchy interlacing, p<n only).\n")
  pr <- tb[, c("k", "labels", "exact", "exact_method", "upper_best", "upper_method", "upper_greedy", "gersh_simple", "gersh_refined", "lambda_minR_lower")]
  print(pr, row.names = FALSE, digits = 4)
  cat("\nWitness sets (upper bounds; original column indices in the raw X below, positions in the cleaned design above):\n")
  for (i in seq_len(nrow(tb))) cat(sprintf("  k=%d: lambda_min=%.5g  set(cleaned idx)=%s ; names: %s\n", tb$k[i], tb$upper_best[i], tb$upper_set[i],
        paste(head(cd$names[as.integer(strsplit(tb$upper_set[i], ",")[[1]])], 12), collapse = ",")))
  for (i in which(!is.na(tb$exact))) cat(sprintf("  k=%d EXACT=%.5g (%s) minimiser(cleaned idx)=%s\n", tb$k[i], tb$exact[i], tb$exact_method[i], tb$exact_set[i]))
  # consistency check: exact <= upper
  chk <- tb$exact <= tb$upper_best + 1e-8; if (any(!chk, na.rm = TRUE)) cat("WARNING: exact > upper bound somewhere (numerical or bug)\n") else cat("check: exact <= upper bound wherever exact is available: OK\n")
  write.csv(tb, sprintf("out_%s_sparse_eig.csv", name), row.names = FALSE)
  res$sparse <- tb; res$kmap <- kmap

  # (e) the method's own blocks
  hdr("(e) production block partition (core_copy/v3.R == Scripts/SMC_BVS/core/v3.R, SHA256 verified)")
  t2 <- proc.time()[["elapsed"]]
  bd <- block_diag(Z, R, y)
  if (bd$ok) {
    cat(sprintf("B = min(floor(sqrt n), floor(sqrt p), 16) = %d ; number of blocks = %d ; time %.1fs ; compiled-core key %s\n", bd$B, bd$nblocks, proc.time()[["elapsed"]] - t2, substr(bd$core_key, 1, 12)))
    cat("block-size histogram (size: count):\n"); print(bd$size_hist)
    cat(sprintf("between-block leakage (max |r| to any variable outside own block): median %.4f, 90%% %.4f, max %.4f\n", bd$leak_q[1], bd$leak_q[2], bd$leak_q[3]))
    cat(sprintf("median within-block max|r| = %.4f ; pairs with |r|>0.5: %d ; fraction split across blocks: %s\n", bd$within_max_med, bd$n_pairs_gt05, fmt(bd$split_frac, 4)))
    write.csv(data.frame(var = seq_len(p), name = cd$names, block = bd$mem, leakage = bd$leak), sprintf("out_%s_blocks.csv", name), row.names = FALSE)
  } else cat("Block diagnostics FAILED:", bd$err, "\n")
  res$blocks <- bd[setdiff(names(bd), c("blocks", "mem", "leak"))]

  # (f) optional plug-in (OMP; NOT verification)
  if (do_plugin && !is.null(y)) {
    hdr("(f) PLUG-IN, NOT VERIFICATION: 5-step orthogonal matching pursuit on the real response")
    yc <- y - mean(y); r <- yc; S <- integer(0)
    for (st in 1:5) {
      sc <- abs(crossprod(Z, r)); sc[S] <- -Inf; j <- which.max(sc); S <- c(S, j)
      fit <- lm.fit(cbind(1, Z[, S, drop = FALSE]), yc); r <- fit$residuals
      cat(sprintf("  step %d: add %s ; R^2 = %.3f\n", st, if (is.null(cd$names[j])) j else cd$names[j], 1 - sum(r^2) / sum(yc^2)))
    }
    cat(sprintf("  lambda_min(R_S) of the OMP support (|S|=2..5): %s\n", paste(sapply(2:5, function(k) fmt(lam_min(R, S[1:k]), 4)), collapse = " ")))
    if (bd$ok) cat("  blocks of OMP support:", paste(bd$mem[S], collapse = ","), "; max|r| of each OMP variable with variables outside its block:", paste(fmt(bd$leak[S], 3), collapse = ","), "\n")
    res$plugin <- list(S = S, names = cd$names[S], lam = sapply(2:5, function(k) lam_min(R, S[1:k])))
  }
  res$seconds <- proc.time()[["elapsed"]] - t_start
  cat(sprintf("\n[done] total %.1f s\n", res$seconds))
  saveRDS(res, sprintf("out_%s.rds", name))
  invisible(res)
}
