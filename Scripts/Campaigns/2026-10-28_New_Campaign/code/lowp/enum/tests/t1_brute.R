# Check 1: brute force vs CORE v3_enumerate(v3_context(...)) at p = 8, 12, 16.
source("C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/lowp/enum/tests/helpers.R")
load_core_ref()
res <- list()
for (p in c(8, 12, 16)) for (kind in c("block", "ar1", "indep")) {
  X <- gen_design(p, kind, seed = 100 + p)
  Y <- gen_response(X, c(2, 5, 7), c(1.4, -1.0, 1.8), seed = 5)
  ex <- lowp_exact(X, list(c100 = Y[, 1], c050 = Y[, 2]), top = 1000, threads = 2, task_bits = 4)
  for (sc in c("c100", "c050")) {
    y <- Y[, sc]
    pre <- v3_preprocess(X, y, dup_components = FALSE)
    ctx <- v3_context(pre$X, pre$y, orig = pre$kept, return_gram = FALSE)
    ref <- v3_enumerate(ctx)
    e <- ex[[sc]]
    topref <- data.frame(F = ref$top$value, model = vapply(ref$top$models, function(m) paste(m, collapse = ";"), ""))
    nt <- min(nrow(topref), nrow(e$top))
    # core's top has cap 40p+1: compare the first min(...) entries; ours has up to 1000
    top_same <- identical(topref$model[1:nt], e$top$model[1:nt]) && same_bits(topref$F[1:nt], e$top$F[1:nt])
    res[[length(res) + 1]] <- data.frame(p = p, design = kind, scale = sc,
      models = attr(ex, "run")$models_scored == ref$models_scored,
      dlogZ = abs(e$log_Z - ref$log_Z), maxdPIP = max(abs(e$pip - ref$pip)),
      hpm_same = identical(as.integer(e$hpm), as.integer(ref$hpm)), hpmF_bits = same_bits(e$hpm_F, ref$hpm_F),
      top_n = nt, top_same = top_same,
      second_F_bits = same_bits(e$second_F, ref$second_F), margin_dif = abs(e$margin - ref$margin),
      eta_bits = same_bits(e$hpm_eta, ref$hpm_error_bound), cert_dif = abs(e$certificate_bound - ref$certificate_bound),
      cert_same = identical(e$global_certified, ref$global_certified), hpmsz = e$hpm_size,
      mpm_same = identical(e$mpm, as.integer(ref$mpm)), logZrel = abs(e$log_Z_rel_m0 - ref$log_Z_rel_m0),
      sizemass_norm = abs(log(sum(exp(e$size_logmass)))), sizejoint_minus_logZ = abs(log(sum(exp(e$size_logjoint - max(e$size_logjoint)))) + max(e$size_logjoint) - e$log_Z), kinds_ok = identical(e$certificate_bound_kind, "heuristic (not a validated interval bound)") && identical(e$hpm_eta_kind, e$certificate_bound_kind) && identical(e$status, "exact") && identical(e$scope, "full"),
      recheck = e$numerics$recheck_count, mismatch = e$numerics$recheck_mismatch_F + e$numerics$recheck_mismatch_eta,
      fallback = e$numerics$n_fallback_v3)
  }
}
R <- do.call(rbind, res)
options(width = 250); print(R)
saveRDS(R, file.path(TMP, "t1_brute.rds"))
cat("size masses: max |log sum exp(size_logmass)| =", max(R$sizemass_norm), "; max joint identity defect =", max(R$sizejoint_minus_logZ), "; kind labels/status/scope ok:", all(R$kinds_ok), "
")
cat("ALL: models", all(R$models), " hpm", all(R$hpm_same), " hpmF bits", all(R$hpmF_bits), " top", all(R$top_same),
    " second_F bits", all(R$second_F_bits), " eta bits", all(R$eta_bits), " cert", all(R$cert_same), " mpm", all(R$mpm_same), "\n")
cat("max dlogZ", max(R$dlogZ), " max dPIP", max(R$maxdPIP), " max cert diff", max(R$cert_dif), " max margin diff", max(R$margin_dif), "\n")
