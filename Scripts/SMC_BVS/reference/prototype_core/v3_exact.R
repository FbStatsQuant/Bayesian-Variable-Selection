# v3_exact.R -- exact branch and exact references (CORE_SPEC v2 §7 `v3_enumerate`, §8 "Exact references"; M §6.2; R9).

# v3_enumerate(ctx): streaming pass over every |S| <= K: log Z (log-sum-exp, long-double accumulators), PIPs, HPM
# (strict order of M §6.10), near ties (top-(40p+1) store), status `exact`. R9: `global_certified` iff
# F(HPM) - eta(HPM) > max_{S != HPM} [F(S) + eta(S)], eta = the scorer's documented error bound (v3_score.h).
v3_enumerate <- function(ctx) {
  r <- .v3cpp$cpp_enumerate(ctx)
  orig <- ctx$orig
  names(r$pip) <- orig
  near <- which(r$top$value >= r$hpm_F - 1e-9)
  r$near_ties <- r$top$models[near]; r$near_tie_F <- r$top$value[near]
  r$near_tie_truncated <- isTRUE(r$top$full) && min(r$top$value) >= r$hpm_F - 1e-9
  r$mpm <- as.integer(orig[r$pip > 0.5])
  r$log_Z_rel_m0 <- r$log_Z - ctx$log_m0
  r$local_certified <- r$status == "exact"   # the HPM is the exact maximiser, so no neighbour improves it
  r$R9 <- list(margin = r$margin, hpm_error_bound = r$hpm_error_bound, hpm_error_bound_kind = r$hpm_error_bound_kind, certificate_bound = r$certificate_bound,
               rule = "certified iff F(HPM) - eta(HPM) > max over other S of F(S) + eta(S)")
  r
}

# Exact reference for analysis (p <= 22): every |S| <= K with log gamma_0(S), d(S) and F(S); `code` has bit (i-1)
# for the i-th retained column. Written to `path` as .rds when given.
v3_reference <- function(setup, path = NULL) {
  r <- .v3cpp$cpp_reference(setup$ptr)
  r$blocks <- setup$blocks
  if (!is.null(path)) saveRDS(r, path)
  invisible(r)
}
