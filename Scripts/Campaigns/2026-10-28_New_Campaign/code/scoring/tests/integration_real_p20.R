#!/usr/bin/env Rscript
# integration_real_p20.R -- ONE real end-to-end check (not in the fast test suite): a genuine v2.2 SMC fit at p = 20, the real exact enumeration
# (lowp_exact, 2^20 models) and the scoring functions on top. Confirms extract_smc() against the real native field structure, the registry
# coverage identity, the scored-set truth trace, the block equality and the TD audit on real output. Writes INTEGRATION_REPORT.md.
here <- local({ f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1L]); normalizePath(dirname(f), winslash = "/") })
SC <- dirname(here); Sys.setenv(SCORING_DIR = SC)
source(file.path(SC, "R", "load_all.R")); sc_load_core(); enum_ok <- sc_load_enum()
L <- character(0); P <- function(...) { s <- paste0(...); L <<- c(L, s); message(s) }
# Dataset: the production low-p dataset p0020_S1_r001 (generate_dataset(20, 1, 1, "prod") of lowp/R/lowp_generate.R), scale c100, truth {3, 7, 14, 16}.
LOWP_ROOT <- file.path(dirname(SC), "lowp")
local({ gp <- file.path(LOWP_ROOT, "R", "lowp_generate.R"); source(gp, local = FALSE) })
gd <- generate_dataset(20L, 1L, 1L, "prod"); X <- gd$inputs$X; n <- nrow(X); p <- ncol(X); S0 <- sort(as.integer(gd$truth$active)); y <- as.numeric(gd$inputs$Y[, "c100"])
P("dataset ", gd$inputs$dataset_id, " c100: n=", n, " p=", p, " truth=", enc_support(S0), " method_seed=", gd$inputs$method_seed)
t0 <- Sys.time(); fit <- v3_fit(X, y, seed = as.integer(gd$inputs$method_seed), allocation = list(mem_gb = 4, hours = 1)); tfit <- as.numeric(difftime(Sys.time(), t0, units = "secs"))
P("v3_fit status ", fit$status, " in ", round(tfit), " s; branch ", fit$branch_run, "; names(fit) include pip_plain: ", "pip_plain" %in% names(fit), "; instrumentation: ", paste(names(fit$instrumentation), collapse = ","))
stopifnot(identical(fit$status, "completed"))
record <- list(fit = fit, native_status = fit$status, estimates_available = fit$estimates_available, runtime_s = tfit,
               pip = setNames(as.numeric(fit$pip_primary), names(fit$pip_primary)), pip_plain = fit$pip_plain, mpm_plain = fit$mpm_plain, instrumentation = fit$instrumentation,
               case = list(dataset_id = "p0020_S1_r001", case_id = "p0020_S1_r001_c100", p = p, scenario = 1L, replicate = 1L, scale_key = "c100", method_seed = as.integer(gd$inputs$method_seed)))
sm <- extract_smc(record)
P("extract_smc: ok=", sm$ok, " log_Z=", round(sm$log_Z, 4), " islands=", paste(round(sm$log_Z_r, 3), collapse = ","), " hpm=", enc_support(sm$hpm), " mpm=", enc_support(sm$mpm), " mpm_plain=", enc_support(sm$mpm_plain))
P("registry: log_mass_scored=", round(sm$log_mass_scored, 4), " n_distinct=", sm$n_distinct_scored, " scored_set rows=", if (is.data.frame(sm$scored_set)) nrow(sm$scored_set) else NA, " score_fresh=", sm$score_fresh, " stages_final=", sm$n_stages_final, " min_ess=", round(sm$min_ess, 1), " tier=", sm$tier)
P("flags: escalated=", sm$escalated, " checks_passed_final=", sm$checks_passed_final, " E1/E2/E3=", sm$E1, "/", sm$E2, "/", sm$E3, " low_ess=", sm$low_ess, " cut_group=", sm$cut_group, " local_limit=", sm$local_limit, " grid_unconverged=", sm$grid_unconverged)
stopifnot(isTRUE(sm$evidence_ok), is.finite(sm$min_ess), sm$min_ess > 0, is.finite(sm$n_stages_final), is.finite(sm$score_fresh))   # real field names: final phase is "final_bridge"
ex_raw <- NULL
if (enum_ok) {
  t0 <- Sys.time(); ex <- lowp_exact(X, list(c100 = y), top = 1000, threads = 2L); texact <- as.numeric(difftime(Sys.time(), t0, units = "secs"))
  P("lowp_exact: ", round(texact), " s; names of the per-scale list: ", paste(names(ex[[1L]]), collapse = ","))
  run_ <- attr(ex, "run"); P("lowp_exact run status: ", run_$status, "; complete: ", run_$complete)
  stopifnot(identical(run_$status, "exact"), isTRUE(run_$complete))
  es <- exact_scale(list(dataset_id = "p0020_S1_r001", p = p, K = run_$K, scales = ex, extra = list(status = run_$status, complete = run_$complete, retained_columns = run_$orig)), "c100")
  stopifnot(!is.null(es), length(es$pip) == p, identical(es$kept, as.integer(run_$orig)))
  scorer <- make_scorer(X, y)
  row <- smc_accuracy_row(sm, es, S0, scorer)
  P("accuracy row: e=", round(row$e, 4), " relative error=", round(row$rel_err, 4), " lb_cover=", row$lb_cover, " se=", round(row$se, 4), " hpm_eq_exact=", row$hpm_eq_exact, " exact_hpm_eq_truth=", row$exact_hpm_eq_truth,
    " F_gap=", signif(row$F_gap, 3), " hpm_F_mismatch=", signif(row$hpm_F_mismatch, 3), " truth_mass=", signif(row$truth_mass, 4))
  P("PIP errors RB: max=", signif(row$rb_max, 3), " mean=", signif(row$rb_mean, 3), " true=", signif(row$rb_mean_true, 3), " null=", signif(row$rb_mean_null, 3), "; plain: max=", signif(row$plain_max, 3), " mean=", signif(row$plain_mean, 3),
    "; MPM RB = exact: ", row$mpm_rb_eq_exact, "; plain = exact: ", row$mpm_plain_eq_exact)
  P("scored coverage = exp(log_mass_scored - log Z) = ", signif(row$scored_coverage, 6), " (log ", signif(row$log_scored_coverage, 4), "); must be <= 1: ", row$scored_coverage <= 1 + 1e-9)
  P("exact vs scorer: log_Z (enumerator) = ", signif(es$log_Z, 12), "; exact HPM F = ", signif(es$hpm_F, 12), " vs scorer F(exact HPM) = ", signif(scorer$F(es$hpm), 12), "; SMC native hpm_F vs scorer: ", signif(row$hpm_F_mismatch, 3))
  th <- theory_case_row(X, y, S0, list(case_id = "p0020_S1_r001_c100", dataset_id = "p0020_S1_r001", p = p, scenario = 1L, replicate = 1L, scale_key = "c100"), sm = sm, es = es, scorer = scorer,
                        td = list(d = c(1L, 2L), engine = "auto"))
  P("theory: pi0(S0)=", signif(th$pi0_S0, 4), " pi0(R0)=", signif(th$pi0_R0, 4), " pi0(R1)=", signif(th$pi0_R1, 4), " pi0(R2)=", signif(th$pi0_R2, 4), "; blocks_match (record vs recomputed)=", th$blocks_match, "; truth_scored=", th$truth_scored,
    " first phase/mech=", th$truth_first_phase, "/", th$truth_first_mech, "; miss_class=", th$miss_class)
  for (dd in 1:2) P("TD d=", dd, " (", th[[paste0("td", dd, "_engine")]], "), literal: clause-a centres ", th[[paste0("td", dd, "_literal_add_true_n")]], ", violating ", th[[paste0("td", dd, "_literal_add_true_viol")]],
      ", clause b ", th[[paste0("td", dd, "_literal_remove_extra_viol")]], "/", th[[paste0("td", dd, "_literal_remove_extra_n")]], ", total ", th[[paste0("td", dd, "_literal_violations")]], ", min margin ", signif(th[[paste0("td", dd, "_literal_min_margin")]], 5),
      ", violators beaten by a truth-in swap ", th[[paste0("td", dd, "_literal_viol_truthin_swap")]], "; toward: violations ", th[[paste0("td", dd, "_toward_violations")]], ", min margin ", signif(th[[paste0("td", dd, "_toward_min_margin")]], 5),
      ", holds_strict ", th[[paste0("td", dd, "_toward_holds_strict")]], "; scores ", th[[paste0("td", dd, "_scores")]])
  sl1 <- td_slow(scorer, S0, 1); P("R stand-in td_slow, same dataset, d=1: literal violating clause a ", sl1$literal$clauses$n_violations[1], " of ", sl1$literal$clauses$n_centres[1], ", min margin ", signif(min(sl1$literal$clauses$min_margin), 5), "; toward violations ", sum(sl1$toward$clauses$n_violations), ", min margin ", signif(min(sl1$toward$clauses$min_margin), 5), "; truth-in-swap violators ", sum(sl1$diagnosis$n[sl1$diagnosis$o_label == "swap_null_out_truth_in"]))
  P("Reference (enumerator worker, VALIDATION.md, same dataset): d=1 literal 240 violating clause-a centres of 255, min margin -5.5884; d=2 2040 of 2055; toward 0 violations, min margins 10.7527 / 3.0716 / 3.0716 (d=1).")
  # assertions (these stop the script on failure)
  stopifnot(isTRUE(row$ok), isTRUE(row$evidence_ok), isTRUE(row$rb_ok), isTRUE(row$plain_ok), isTRUE(row$kept_match))
  stopifnot(row$scored_coverage > 0, row$scored_coverage <= 1 + 1e-9)
  stopifnot(isTRUE(th$blocks_match), row$hpm_F_mismatch < 1e-9, abs(row$lb_native_diff) < 1e-12)
  stopifnot(th$td1_literal_add_true_n == 255, th$td1_literal_add_true_viol == 240, th$td2_literal_add_true_n == 2055, th$td2_literal_add_true_viol == 2040,
            th$td1_toward_violations == 0, th$td2_toward_violations == 0, th$td1_literal_viol_truthin_swap == 240)
  P("ASSERTIONS PASSED: SMC record valid; kept maps agree; coverage in (0,1]; blocks equal; native hpm_F = scorer F; lower-bound identity; TD literal 240/255 and 2040/2055 (all beaten by a truth-in swap), toward 0 violations")
  # Reconciliation of the earlier report (180 / 1885): that run used an AD HOC dataset (set.seed(2026), within-block correlation .4 in blocks of 5, own eps), NOT p0020_S1_r001.
  set.seed(2026); Sig <- diag(p); for (b in seq(1, p, by = 5)) { ix <- b:(b + 4); Sig[ix, ix] <- 0.4; diag(Sig) <- 1 }
  Xo <- matrix(as.numeric(scale(matrix(rnorm(n * p), n) %*% chol(Sig))), n, p); yo <- as.numeric(Xo[, S0] %*% c(1.4, -1, 1.8, -1.2) + rnorm(n))
  for (dd in 1:2) { r <- run_td(Xo, yo, scorer, S0, dd, engine = "enum"); P("ad hoc dataset (earlier report), d=", dd, ": literal violating clause a ", r$literal$clauses$n_violations[1], " of ", r$literal$clauses$n_centres[1], ", all clauses ", sum(r$literal$clauses$n_violations), ", min margin ", signif(min(r$literal$clauses$min_margin), 5)) }
} else P("enumerator unavailable: exact comparison skipped")
writeLines(c("# Integration check: one real p = 20 fit", "", "```", L, "```"), file.path(here, "INTEGRATION_REPORT.md"))
