# Check 2: DFS F versus v3::Scorer::score (= the SMC scorer) at p = 20 (all 2^20 models) and p = 30 (random models, sampled
# enumerator nodes), both scales; plus the forced fallback paths.
source("C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/lowp/enum/tests/helpers.R")
lowp_load(); cpp <- .lowp$cpp
nid <- function(a, b) sum(writeBin(a, raw()) != writeBin(b, raw())) # not used
cmp <- function(a, b) { a <- as.numeric(a); b <- as.numeric(b); ne <- !(is.na(a) & is.na(b)) & (is.na(a) != is.na(b) | a != b); c(n = length(a), nonidentical = sum(ne), max_abs_diff = max(abs(a - b), na.rm = TRUE)) }
out <- list()
## (a) p = 20, every model, the enumerator's own F (collect_F) vs Scorer::score
for (kind in c("block", "ar1")) {
  X <- gen_design(20, kind, seed = 31); Y <- gen_response(X, c(3, 7, 14, 16), c(1.4, -1, 1.8, -1.2))
  ex <- lowp_exact(X, list(c100 = Y[, 1], c050 = Y[, 2]), threads = 4, collect_F = TRUE, return_raw = TRUE)
  run <- attr(ex, "run"); pr <- run$prep
  masks <- as.numeric(0:(2^20 - 1))
  for (sc in c("c100", "c050")) {
    sref <- cpp$cpp_score_masks(pr$X, pr$Y[, sc], pr$orig, masks, 4L)
    r <- cmp(run$F_all[[sc]], sref$F)
    out[[length(out) + 1]] <- data.frame(check = "p20_all_models_enumerator_F", design = kind, scale = sc, t(r), fallback = ex[[sc]]$numerics$n_fallback_v3, recheck = ex[[sc]]$numerics$recheck_count, recheck_mismatch = ex[[sc]]$numerics$recheck_mismatch_F)
    print(tail(out, 1)[[1]])
  }
}
## (b) p = 20 and 30, 1e5 random models (sizes uniform 0..p): row-append F (cpp_dfs_F) vs Scorer
set.seed(99)
for (p in c(20, 30)) for (kind in c("block", "ar1")) {
  X <- gen_design(p, kind, seed = 40 + p); idx <- c(3, 7, 14, 16, 25)[c(3, 7, 14, 16, 25) <= p]
  Y <- gen_response(X, idx, c(1.4, -1, 1.8, -1.2, 0.8)[seq_along(idx)])
  pr <- lowp_prepare(X, list(c100 = Y[, 1], c050 = Y[, 2]))
  m <- vapply(1:1e5, function(i) { k <- sample(0:p, 1); sum(2^(sample.int(p, k) - 1)) }, 0)
  d <- cpp$cpp_dfs_F(pr$X, pr$Y, pr$orig, m, 1e-8, integer(0))
  for (s in 1:2) {
    sref <- cpp$cpp_score_masks(pr$X, pr$Y[, s], pr$orig, m, 4L)
    r <- cmp(d$F[, s], sref$F); re <- cmp(d$eta[, s], sref$eta)
    out[[length(out) + 1]] <- data.frame(check = "random_1e5_models_rowappend_F", design = kind, scale = colnames(pr$Y)[s], p = p, t(r), eta_nonidentical = re[["nonidentical"]], fallback = sum(d$fallback[, s]))
    print(tail(out, 1)[[1]])
  }
}
## (c) p = 30: the production enumerator's own nodes vs Scorer (internal recheck on a 2% random subset of tasks)
for (kind in c("block", "ar1")) {
  X <- gen_design(30, kind, seed = 77); Y <- gen_response(X, c(3, 7, 14, 16, 25), c(1.4, -1, 1.8, -1.2, 0.8))
  ex <- lowp_exact(X, list(c100 = Y[, 1], c050 = Y[, 2]), threads = 8, prefix_fraction = 0.02, recheck_stride = 61L)
  for (sc in c("c100", "c050")) {
    nn <- ex[[sc]]$numerics
    out[[length(out) + 1]] <- data.frame(check = "p30_enumerator_nodes_recheck", design = kind, scale = sc, n = nn$recheck_count, nonidentical = nn$recheck_mismatch_F, max_abs_diff = nn$max_abs_dF_recheck, eta_nonidentical = nn$recheck_mismatch_eta, fallback = nn$n_fallback_v3, models = attr(ex, "run")$models_scored)
    print(tail(out, 1)[[1]])
  }
}
saveRDS(out, file.path(TMP, "t2_results.rds"))
