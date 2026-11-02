#!/usr/bin/env Rscript
# test_scoring.R -- asserts every scoring metric against values computed independently from the injection table / the exact posterior.
# Usage: Rscript tests/test_scoring.R [workdir]     (default workdir = a fresh folder under tempdir(); writes TEST_REPORT.md next to this file)
args <- commandArgs(trailingOnly = TRUE)
here <- local({ f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1L]); normalizePath(dirname(f), winslash = "/") })
SC <- dirname(here)
Sys.setenv(SCORING_DIR = SC)
source(file.path(SC, "R", "load_all.R")); sc_load_core(); enum_ok <- sc_load_enum() && tryCatch({ lowp_score_models(matrix(rnorm(200), 50), rnorm(50), list(1L)); TRUE }, error = function(e) { message("enumerator unusable: ", substr(conditionMessage(e), 1, 200)); FALSE })
source(file.path(here, "make_fixtures.R"))
source(file.path(SC, "run_scoring.R"))
source(file.path(SC, "run_theory_H.R"))
work <- if (length(args)) args[1L] else file.path(tempdir(), "scoring_fx")
unlink(work, recursive = TRUE); dir.create(work, recursive = TRUE)

RES <- data.frame(group = character(), name = character(), pass = logical(), note = character(), stringsAsFactors = FALSE)
chk <- function(group, name, cond, note = "") { ok <- isTRUE(all(cond)) && length(cond) > 0L; RES[nrow(RES) + 1L, ] <<- list(group, name, ok, note); if (!ok) message("FAIL [", group, "] ", name, " ", note); invisible(ok) }
near <- function(a, b, tol = 1e-9) { if (length(a) != length(b)) return(FALSE); both_na <- is.na(a) & is.na(b); ok <- both_na | (!is.na(a) & !is.na(b) & abs(a - b) <= tol * pmax(1, abs(b))); all(ok) }
skip <- function(group, name, why) { RES[nrow(RES) + 1L, ] <<- list(group, name, NA, paste("SKIPPED:", why)); message("SKIP [", group, "] ", name, ": ", why) }

t0 <- Sys.time()
FX <- make_fixtures(work)
message("fixtures built in ", round(as.numeric(difftime(Sys.time(), t0, units = "secs")), 1), " s")
out <- file.path(work, "analysis")
REG <- file.path(work, "registry_fixture.csv")
res <- run_scoring(work, file.path(work, "results", c("exact", "smc", "bench")), out, td_d = c(1L, 2L), verbose = FALSE, registry = REG, partial = TRUE)
acc <- res$acc; sel <- res$sel; thy <- res$theory; stb <- res$stability

# ---- independent expectations -----------------------------------------------------------------------------------------------
S0_of <- function(ds) FX$datasets[[ds]]$S0
exact_of <- function(ds, sk) readRDS(file.path(work, "results/exact", sprintf("p%04d", as.integer(substr(ds, 2, 5))), ds, "EXACT.rds"))$scales[[sk]]
case_info <- function(cid) FX$cases[FX$cases$case_id == cid, ]
expect_for <- function(inj) {
  ci <- case_info(inj$case_id); ds <- ci$dataset_id; p <- ci$p; S0 <- S0_of(ds); ex <- exact_of(ds, ci$scale_key)
  Fm <- FX$Fall[[inj$case_id]]                       # full 2^p score table (the stored top list holds the best 1000 only)
  logZ <- lse(Fm); lzr <- logZ + inj$off; lz <- lse(lzr) - log(4)
  F_truth <- Fm[sum(2^(S0 - 1)) + 1]
  row <- switch(inj$hpm_mode, exact = 1L, second = 2L, below_truth = which(ex$top$F < F_truth - 1e-9)[1L])
  hpm <- parse_support(ex$top$model[row]); Fh <- ex$top$F[row]
  pip_rb <- ex$pip + inj$delta_rb; pip_pl <- ex$pip + inj$delta_plain
  failed <- inj$status != "completed"
  list(ci = ci, ds = ds, p = p, S0 = S0, ex = ex, Fm = Fm, logZ = logZ, e = lz - logZ, e_r = lzr - logZ, sd = stats::sd(lzr), F_truth = F_truth,
       hpm = hpm, Fh = Fh, hpm_exact = parse_support(ex$top$model[1L]), mpm_ex = which(ex$pip > 0.5), mpm_rb = which(pip_rb > 0.5), mpm_pl = which(pip_pl > 0.5),
       pip_rb = pip_rb, pip_pl = pip_pl, failed = failed)
}
all_inj <- c(FX$injs, FX$reps)
EXP <- lapply(all_inj, expect_for)

# ================================ G1 extraction =================================================================================
g <- "G1 extract_smc"
recA <- readRDS(file.path(work, "results/smc/p0008", FX$special$A, "SMCBVS.rds")); smA <- extract_smc(recA)
chk(g, "ids and ok", smA$case_id == FX$special$A && smA$p == 8L && smA$ok && smA$scale_key == "c100")
chk(g, "log_Z, island log Z, lower95", near(smA$log_Z, recA$fit$log_Z) && length(smA$log_Z_r) == 4 && near(smA$log_Z_lower95, recA$fit$log_Z + log(0.05)))
chk(g, "RB and plain PIP full length", length(smA$pip_rb) == 8 && length(smA$pip_plain) == 8 && nrow(smA$pip_rb_r) == 8 && ncol(smA$pip_rb_r) == 4 && ncol(smA$pip_plain_r) == 4)
chk(g, "flags", identical(smA$escalated, FX$injs[[FX$special$A]]$flags$escalated) && identical(smA$cut_group, FX$injs[[FX$special$A]]$flags$cut_group))
chk(g, "min ESS uses final rows only (diag row ess = 1 ignored)", near(smA$min_ess, FX$injs[[FX$special$A]]$min_ess) && smA$n_stages_final == 2)
chk(g, "score counts and tier", near(smA$score_fresh, FX$injs[[FX$special$A]]$score_fresh) && near(smA$score_logical, FX$injs[[FX$special$A]]$score_logical) && smA$tier == as.integer(FX$injs[[FX$special$A]]$flags$escalated))
chk(g, "registry log mass and distinct count", near(smA$log_mass_scored, recA$fit$instrumentation$scored$log_sum_exp_F) && smA$n_distinct_scored == 200)
recD <- readRDS(file.path(work, "results/smc/p0010", FX$special$D, "SMCBVS.rds")); smD <- extract_smc(recD)
chk(g, "failed fit: not ok, estimates NA/NULL, HPM audit kept", !smD$ok && is.na(smD$log_Z) && is.null(smD$pip_rb) && !is.null(smD$hpm) && is.null(smD$mpm))
rec0 <- recA; rec0$fit$instrumentation <- NULL; rec0$instrumentation <- NULL; rec0$pip_plain <- NULL; rec0$fit$pip_plain <- NULL; rec0$fit$pip_plain_r <- NULL
sm0 <- extract_smc(rec0)
chk(g, "absent v2.2 fields give NA / NULL (log_mass_scored, scored_set, plain PIP)", is.na(sm0$log_mass_scored) && is.null(sm0$scored_set) && is.null(sm0$pip_plain) && is.null(sm0$pip_plain_r) && sm0$ok)
recK <- recA; recK$pip <- NULL; recK$pip_primary_original <- NULL; recK$case$p <- 4L; recK$fit$pip_primary <- c(`1` = 0.9, `4` = 0.2); recK$fit$pip_r <- NULL; recK$pip_plain <- NULL; recK$fit$pip_plain <- NULL; recK$fit$pip_plain_r <- NULL; recK$fit$preprocessing$kept <- c(1L, 4L)
smK <- extract_smc(recK)
chk(g, "retained-only PIP expanded with zeros for dropped columns", identical(unname(smK$pip_rb), c(0.9, 0, 0, 0.2)) && identical(names(smK$pip_rb), as.character(1:4)))
chk(g, "FIELD_MAP covers every name used and statuses are code/provisional", all(c("log_Z", "pip_plain_r", "log_mass_scored", "truth_trace") %in% FIELD_MAP$name) && all(grepl("^code|^provisional", FIELD_MAP$status)))

# ================================ G2 log Z metrics ==============================================================================
g <- "G2 log Z"
Z <- sapply(names(EXP), function(k) {
  inj <- all_inj[[k]]; x <- EXP[[k]]; r <- acc[case_id == inj$case_id & rep == inj$rep]
  if (nrow(r) != 1L) return(FALSE)
  if (x$failed) return(!r$ok && is.na(r$e))
  se <- x$sd / 2
  near(r$log_Z_exact, x$logZ, 1e-12) && near(r$e, x$e, 1e-10) && near(r$rel_err, expm1(x$e), 1e-10) && near(c(r$e_isl1, r$e_isl2, r$e_isl3, r$e_isl4), x$e_r, 1e-10) &&
    identical(r$lb_cover, (x$e + log(0.05) <= 0)) && near(r$isl_sd, x$sd, 1e-10) && near(r$se, se, 1e-10) &&
    identical(r$within2se, abs(x$e) <= 2 * se) && identical(r$e_gt_2se, abs(x$e) > 2 * se) && near(r$e_over_se, abs(x$e) / se, 1e-9) && near(r$lb_native_diff, 0, 1e-9)
})
chk(g, "every fit (24 main + 6 repeat rows): log Z exact, e, relative error, island errors, lb coverage, SE, within 2 SE", Z, paste(sum(!Z), "mismatching fits"))
rA <- acc[case_id == FX$special$A & rep == 0L]
chk(g, "hand value, case A: e = log mean exp(0, .2, .4, .6)", near(rA$e, log(mean(exp(c(0, 0.2, 0.4, 0.6)))), 1e-10) && near(rA$se, stats::sd(c(0, 0.2, 0.4, 0.6)) / 2, 1e-10) && isTRUE(rA$e_gt_2se) && isTRUE(rA$lb_cover))
rB <- acc[case_id == FX$special$B & rep == 0L]
chk(g, "hand value, case B: e ~ 4 so the 0.05 lower bound is violated", rB$e > 3.99 && rB$e < 4.11 && isTRUE(rB$lb_violated) && !isTRUE(rB$lb_cover))
chk(g, "failed fit (case D) has NA metrics but a row", acc[case_id == FX$special$D & rep == 0L, !ok & is.na(e) & is.na(rb_max)])
chk(g, "coverage of scored set = injected fraction (0.999; 0.5 for the Fc case)", {
  r <- acc[rep == 0L & ok == TRUE]; exp_cov <- ifelse(r$case_id == FX$special$Fc, 0.5, 0.999); near(r$scored_coverage, exp_cov, 1e-9) && near(r$log_scored_coverage, log(exp_cov), 1e-9) })

# ================================ G3 PIP errors =================================================================================
g <- "G3 PIP"
P <- sapply(names(EXP), function(k) {
  inj <- all_inj[[k]]; x <- EXP[[k]]; if (x$failed) return(TRUE); r <- acc[case_id == inj$case_id & rep == inj$rep]
  tr <- seq_len(x$p) %in% x$S0; er <- abs(inj$delta_rb); ep <- abs(inj$delta_plain)
  clip <- function(v) pmin(1, pmax(0, v)); isl <- sapply(1:4, function(i) max(abs(clip(x$ex$pip + inj$delta_rb + (i - 2.5) * 0.002) - x$ex$pip))); isp <- sapply(1:4, function(i) max(abs(clip(x$ex$pip + inj$delta_plain + (i - 2.5) * 0.004) - x$ex$pip)))
  near(c(r$rb_max, r$rb_mean, r$rb_mean_true, r$rb_mean_null, r$rb_max_true, r$rb_max_null), c(max(er), mean(er), mean(er[tr]), mean(er[!tr]), max(er[tr]), max(er[!tr])), 1e-8) &&
  near(c(r$plain_max, r$plain_mean, r$plain_mean_true, r$plain_mean_null, r$plain_max_true, r$plain_max_null), c(max(ep), mean(ep), mean(ep[tr]), mean(ep[!tr]), max(ep[tr]), max(ep[!tr])), 1e-8) &&
  near(c(r$rb_isl1_max, r$rb_isl2_max, r$rb_isl3_max, r$rb_isl4_max), isl, 1e-8) && near(c(r$plain_isl1_max, r$plain_isl4_max), isp[c(1, 4)], 1e-8) && near(r$rb_isl_max_mean, mean(isl), 1e-8)
})
chk(g, "RB and plain: max, mean, true/null split, per island, island mean (all fits)", P, paste(sum(!P), "mismatches"))
chk(g, "hand values, case A (p=8, S0={2,6}; +/-0.05 on vars 1,2 RB; 0.10 on var 1 plain)",
    near(c(rA$rb_max, rA$rb_mean, rA$rb_mean_true, rA$rb_mean_null, rA$plain_max, rA$plain_mean_true, rA$plain_mean_null), c(0.05, 0.1 / 8, 0.025, 0.05 / 6, 0.10, 0, 0.10 / 6), 1e-9))
M <- sapply(names(EXP), function(k) {
  inj <- all_inj[[k]]; x <- EXP[[k]]; if (x$failed) return(TRUE); r <- acc[case_id == inj$case_id & rep == inj$rep]
  identical(r$mpm_rb_eq_exact, setequal(x$mpm_rb, x$mpm_ex)) && identical(r$mpm_plain_eq_exact, setequal(x$mpm_pl, x$mpm_ex)) && identical(r$mpm_ne_exact, !setequal(x$mpm_rb, x$mpm_ex)) &&
  identical(r$exact_mpm_eq_truth, setequal(x$mpm_ex, x$S0)) && identical(r$mpm_rb_eq_truth, setequal(x$mpm_rb, x$S0)) && identical(r$mpm_plain_eq_truth, setequal(x$mpm_pl, x$S0))
})
chk(g, "MPM = exact MPM (RB, plain), exact MPM = truth, SMC MPM = truth", M)

# ================================ G4 HPM and truth ==============================================================================
g <- "G4 HPM"
H <- sapply(names(EXP), function(k) {
  inj <- all_inj[[k]]; x <- EXP[[k]]; if (x$failed) return(TRUE); r <- acc[case_id == inj$case_id & rep == inj$rep]
  cls <- if (setequal(x$hpm, x$S0)) "hit" else if (x$F_truth > x$Fh) "search_miss" else "posterior_miss"
  identical(r$hpm_eq_exact, setequal(x$hpm, x$hpm_exact)) && identical(r$hpm_eq_truth, setequal(x$hpm, x$S0)) && identical(r$exact_hpm_eq_truth, setequal(x$hpm_exact, x$S0)) &&
  near(r$F_gap, x$ex$top$F[1L] - x$Fh, 1e-9) && near(r$F_truth, x$F_truth, 1e-9) && near(r$truth_mass, exp(x$F_truth - x$logZ), 1e-9) && near(r$log_truth_mass, x$F_truth - x$logZ, 1e-9) &&
  near(r$truth_minus_smc_hpm, x$F_truth - x$Fh, 1e-9) && near(r$truth_minus_exact_hpm, x$F_truth - x$ex$top$F[1L], 1e-9) && identical(r$miss_class, cls) && near(r$F_exact_hpm, x$ex$top$F[1L], 1e-9)
})
chk(g, "SMC HPM = exact HPM, exact HPM = truth, SMC HPM = truth, score gap, truth mass, truth-vs-HPM scores, miss class", H, paste(sum(!H), "mismatches"))
chk(g, "the injected wrong HPMs are detected (B second-best, C below truth, rep2 of A)",
    isFALSE(acc[case_id == FX$special$B & rep == 0L, hpm_eq_exact]) && isFALSE(acc[case_id == FX$special$C & rep == 0L, hpm_eq_exact]) && isFALSE(acc[case_id == FX$special$A & rep == 2L, hpm_eq_exact]) &&
    identical(acc[case_id == FX$special$C & rep == 0L, miss_class], "search_miss"))
chk(g, "both miss classes occur in the fixture", all(c("hit", "search_miss") %in% acc$miss_class))
chk(g, "native hpm_F shift 0.001 injected in case E is measured", near(acc[case_id == FX$special$E & rep == 0L, hpm_F_mismatch], 0.001, 1e-6) && acc[case_id != FX$special$E, all(is.na(hpm_F_mismatch) | hpm_F_mismatch < 1e-9)])
chk(g, "exact F from the stored top list equals the scorer F for the true model (consistency)", {
  ok <- TRUE; for (cid in FX$cases$case_id[1:6]) { x <- EXP[[cid]]; sco <- make_scorer(readRDS(file.path(work, "inputs", sprintf("p%04d", x$p), paste0(x$ds, ".rds")))$X,
    as.numeric(readRDS(file.path(work, "inputs", sprintf("p%04d", x$p), paste0(x$ds, ".rds")))$Y[, x$ci$scale_key])); ok <- ok && near(sco$F(x$S0), x$F_truth, 1e-9) }; ok })

# ================================ G5 stability ==================================================================================
g <- "G5 stability"
sA <- stb[case_id == FX$special$A]; sB <- stb[case_id == FX$special$B]; sC <- stb[case_id == FX$special$C]
lzfit <- function(cid, m) { inj <- if (m == 0L) FX$injs[[cid]] else FX$reps[[paste0(cid, "#", m)]]; x <- EXP[[if (m == 0L) cid else paste0(cid, "#", m)]]; x$logZ + x$e }
sdZ <- function(cid) stats::sd(sapply(0:2, function(m) lzfit(cid, m)))
chk(g, "only the three cases with repeat seeds have a stability row, 3 attempted / 3 completed fits each", nrow(stb) == 3L && all(stb$n_attempted == 3L) && all(stb$n_completed == 3L) && all(stb$n_evidence == 3L))
chk(g, "sd of log Z-hat across seeds", near(sA$sd_log_Z, sdZ(FX$special$A), 1e-9) && near(sB$sd_log_Z, sdZ(FX$special$B), 1e-9) && near(sC$sd_log_Z, sdZ(FX$special$C), 1e-9))
chk(g, "HPM agreement = 1/3 for A, B, C (main and repeat 1 share an HPM, repeat 2 differs; 2 distinct HPMs)", near(c(sA$hpm_agreement, sB$hpm_agreement, sC$hpm_agreement), rep(1 / 3, 3)) && all(c(sA$n_distinct_hpm, sB$n_distinct_hpm, sC$n_distinct_hpm) == 2L))
chk(g, "max PIP sd = 0.5 max|delta| (PIP scaled by 1, 1.5, 2 across seeds)",
    near(sA$max_pip_sd_rb, 0.5 * max(abs(FX$injs[[FX$special$A]]$delta_rb)), 1e-8) && near(sB$max_pip_sd_rb, 0.5 * max(abs(FX$injs[[FX$special$B]]$delta_rb)), 1e-8))

# ================================ G6 flags vs errors ============================================================================
g <- "G6 flag x error"
fe <- flag_error_table(acc)
ok_inj <- all_inj[!sapply(EXP, function(x) x$failed)]
ev <- do.call(rbind, lapply(names(ok_inj), function(k) { x <- EXP[[k]]; inj <- ok_inj[[k]]
  data.frame(hpm_ne_exact = !setequal(x$hpm, x$hpm_exact), mpm_ne_exact = !setequal(x$mpm_rb, x$mpm_ex), lb_violated = !(x$e + log(0.05) <= 0),
             e_gt_2se = abs(x$e) > 2 * x$sd / 2, escalated = inj$flags$escalated, checks_failed_final = !inj$flags$checks_passed_final, E1 = inj$flags$E1, E2 = inj$flags$E2,
             E3 = inj$flags$E3, low_ess = inj$flags$low_ess, cut_group = inj$flags$cut_group, local_limit = inj$flags$local_limit, grid_unconverged = inj$flags$grid_unconverged) }))
F2 <- sapply(seq_len(nrow(fe)), function(i) {
  f <- ev[[fe$flag[i]]]; v <- ev[[fe$event[i]]]; a <- sum(f & v); b <- sum(f & !v); c <- sum(!f & v); d <- sum(!f & !v)
  fe$n[i] == length(f) && fe$flag_and_event[i] == a && fe$flag_no_event[i] == b && fe$noflag_event[i] == c && fe$noflag_noevent[i] == d &&
    near(fe$sensitivity[i], if (a + c > 0) a / (a + c) else NA_real_) && near(fe$specificity[i], if (b + d > 0) d / (b + d) else NA_real_) && near(fe$ppv[i], if (a + b > 0) a / (a + b) else NA_real_)
})
chk(g, paste0("2x2 counts, sensitivity, specificity for all ", nrow(fe), " flag x event pairs"), F2, paste(sum(!F2), "mismatches"))
chk(g, "the table has 9 flags x 4 events", nrow(fe) == 36L)

# ================================ G7 selection and H4 ===========================================================================
g <- "G7 selection"
cases <- FX$cases
sel_ex <- function(cid, method, rule) sel[case_id == cid & method_id == method & rule_id == rule]
bs <- FX$bench
kind_of <- function(cid, m) bs$kind[bs$case_id == cid & bs$method_id == m]
chk(g, "row count: 24 cases x (LASSO 2 rules + SUSIE 1 + SMC 2 + EXACT 2) = 168", nrow(sel) == 24L * 7L)
S1 <- sapply(seq_len(nrow(cases)), function(i) {
  cid <- cases$case_id[i]; s0 <- length(S0_of(cases$dataset_id[i])); res <- TRUE
  exp_ <- function(kind) switch(kind, exact = list(10L, TRUE, "none", s0, 0L, 0L), extra = list(11L, FALSE, "extra_only", s0, 1L, 0L), missed = list(12L, FALSE, "missed_only", s0 - 1L, 0L, 1L),
                                mixed = list(13L, FALSE, "mixed", s0 - 1L, 1L, 1L), list(NA, FALSE, "failed", NA_integer_, NA_integer_, NA_integer_))
  chk1 <- function(r, e) nrow(r) == 1L && identical(r$exact, e[[2L]]) && identical(r$error_type, e[[3L]]) && identical(r$tp, e[[4L]]) && identical(r$fp, e[[5L]]) && identical(r$fn, e[[6L]])
  kl <- kind_of(cid, "LASSO"); ks <- kind_of(cid, "SUSIE")
  res <- res && chk1(sel_ex(cid, "LASSO", "cvmin"), exp_(kl)) && chk1(sel_ex(cid, "LASSO", "ebic1"), exp_(if (kl %in% c("failed", "timeout")) "failed" else "exact")) && chk1(sel_ex(cid, "SUSIE", "L10"), exp_(ks))
  res
})
chk(g, "LASSO/SUSIE: TP, FP, FN, exact, error type per row (exact, extra_only, missed_only, mixed, failed/timeout/not_run)", S1, paste(sum(!S1), "cases mismatch"))
chk(g, "timeout and not_run rows are present as failed non-recovery (denominator)", {
  r <- sel[method_id == "SUSIE"]; nt <- sum(bs$method_id == "SUSIE" & bs$kind == "timeout"); nn <- sum(bs$method_id == "SUSIE" & bs$kind == "not_run")
  nt > 0 && nn > 0 && sum(r$status == "timeout") == nt && sum(r$status == "not_run") == nn && all(r$error_type[r$status %in% c("timeout", "not_run")] == "failed") && all(!r$exact[r$status %in% c("timeout", "not_run")]) })
Sm <- sapply(names(ok_inj), function(k) TRUE)
chk(g, "SMC hpm / pip05 rows: exact recovery matches the injected supports; failed fit (case D) is a failed row",
    all(sapply(FX$injs, function(inj) { x <- EXP[[inj$case_id]]; rh <- sel_ex(inj$case_id, "SMCBVS", "hpm"); rp <- sel_ex(inj$case_id, "SMCBVS", "pip05")
      if (x$failed) return(rh$error_type == "failed" && rp$error_type == "failed" && !rh$exact)
      identical(rh$exact, setequal(x$hpm, x$S0)) && identical(rp$exact, setequal(x$mpm_rb, x$S0)) })))
chk(g, "EXACT reference rows: exact HPM / exact MPM recover the truth iff they equal S0", all(sapply(FX$cases$case_id, function(cid) { x <- EXP[[cid]]
  identical(sel_ex(cid, "EXACT", "hpm")$exact, setequal(x$hpm_exact, x$S0)) && identical(sel_ex(cid, "EXACT", "mpm")$exact, setequal(x$mpm_ex, x$S0)) })))
chk(g, "repeat-seed fits add no selection rows (only the main fit is scored for selection)", nrow(sel[method_id == "SMCBVS" & rule_id == "hpm"]) == 24L)
g <- "G7b H4 recovery"
H4 <- res$H4
H4ok <- sapply(c("LASSO|cvmin", "SUSIE|L10"), function(key) {
  m <- strsplit(key, "|", fixed = TRUE)[[1L]]; ok <- TRUE
  for (pp in c(8L, 10L)) for (sk in c("c100", "c050")) {
    cc <- cases[cases$p == pp & cases$scale_key == sk, ]
    ex1 <- sapply(cc$case_id, function(cid) { kl <- kind_of(cid, m[1L]); kl == "exact" })
    tot <- H4[p == pp & scale_key == sk & method_id == m[1L] & rule_id == m[2L] & scenario == "all"]
    ok <- ok && tot$n_exact == sum(ex1) && tot$n_cases == length(ex1) && tot$recovery == sprintf("%d/%d", sum(ex1), length(ex1))
    for (s in 1:2) { cs <- cc$case_id[cc$scenario == s]; e1 <- ex1[cs]; r1 <- H4[p == pp & scale_key == sk & method_id == m[1L] & rule_id == m[2L] & scenario == as.character(s)]; ok <- ok && r1$n_exact == sum(e1) && r1$n_cases == length(cs) }
  }
  ok })
chk(g, "per-scenario and pooled recovery counts for LASSO cvmin and SUSIE (p x c)", H4ok)
chk(g, "H4 contains primary rules, SMC pip05 and the EXACT references; S0-role rules of benchmarks (ebic1) excluded from H4 only via role", {
  k <- unique(H4[, .(method_id, rule_id)]); all(c("SMCBVS|hpm", "SMCBVS|pip05", "EXACT|hpm", "EXACT|mpm", "LASSO|cvmin", "SUSIE|L10") %in% paste(k$method_id, k$rule_id, sep = "|")) && !("LASSO|ebic1" %in% paste(k$method_id, k$rule_id, sep = "|")) })
chk(g, "H4 n_failed counts failed/timeout/not_run", {
  r <- H4[method_id == "SUSIE" & scenario == "all"]; sum(r$n_failed) == sum(bs$method_id == "SUSIE" & bs$kind %in% c("failed", "timeout", "not_run")) })

# ================================ G8 headline tables H1-H3 ======================================================================
g <- "G8 headline H1-H3"
main_names <- names(FX$injs)
mm <- do.call(rbind, lapply(main_names, function(cid) { x <- EXP[[cid]]; inj <- FX$injs[[cid]]; ci <- x$ci
  data.frame(cid = cid, p = ci$p, scen = ci$scenario, sk = ci$scale_key, failed = x$failed, e = if (x$failed) NA else x$e, lb = if (x$failed) NA else (x$e + log(0.05) <= 0),
             hpm_eq_ex = !x$failed && setequal(x$hpm, x$hpm_exact), ex_eq_tr = setequal(x$hpm_exact, x$S0), hpm_eq_tr = !x$failed && setequal(x$hpm, x$S0),
             rb_max = if (x$failed) NA else max(abs(inj$delta_rb)), plain_max = if (x$failed) NA else max(abs(inj$delta_plain)),
             rb_true = if (x$failed) NA else mean(abs(inj$delta_rb)[x$S0]), rb_null = if (x$failed) NA else mean(abs(inj$delta_rb)[-x$S0]),
             pl_true = if (x$failed) NA else mean(abs(inj$delta_plain)[x$S0]), pl_null = if (x$failed) NA else mean(abs(inj$delta_plain)[-x$S0]),
             mpm_rb = !x$failed && setequal(x$mpm_rb, x$mpm_ex), mpm_pl = !x$failed && setequal(x$mpm_pl, x$mpm_ex), stringsAsFactors = FALSE) }))
H1 <- res$H1; H2 <- res$H2; H3 <- res$H3
G <- list(); for (pp in c(8L, 10L)) for (sk in c("c100", "c050")) for (sc in c("1", "2", "all")) {
  d <- mm[mm$p == pp & mm$sk == sk & (sc == "all" | mm$scen == suppressWarnings(as.integer(sc))), ]; okd <- d[!d$failed, ]
  h1 <- H1[p == pp & scale_key == sk & scenario == sc]; h2 <- H2[p == pp & scale_key == sk & scenario == sc]; h3 <- H3[p == pp & scale_key == sk & scenario == sc]
  G[[length(G) + 1L]] <- c(
    h1$n_cases == nrow(d), h1$n_smc_failed == sum(d$failed), h1$n_smc_missing == 0, h1$n_exact_missing == 0, h1$n_evidence == nrow(okd), near(h1$bias, mean(okd$e)), near(h1$rmse, sqrt(mean(okd$e^2))), near(h1$median_abs_e, median(abs(okd$e))),
    near(h1$p90_abs_e, unname(quantile(abs(okd$e), 0.9))), near(h1$lb_coverage, mean(okd$lb)),
    near(h2$pct_smc_hpm_eq_exact, 100 * sum(d$hpm_eq_ex) / nrow(d)), near(h2$pct_exact_hpm_eq_truth, 100 * sum(d$ex_eq_tr) / nrow(d)), near(h2$pct_smc_hpm_eq_truth, 100 * sum(d$hpm_eq_tr) / nrow(d)),
    near(h3$rb_mean_max_err, mean(okd$rb_max), 1e-8), near(h3$rb_p90_max_err, unname(quantile(okd$rb_max, 0.9)), 1e-8), near(h3$rb_mean_err_true, mean(okd$rb_true), 1e-8), near(h3$rb_mean_err_null, mean(okd$rb_null), 1e-8),
    near(h3$plain_mean_max_err, mean(okd$plain_max), 1e-8), near(h3$plain_p90_max_err, unname(quantile(okd$plain_max, 0.9)), 1e-8), near(h3$plain_mean_err_true, mean(okd$pl_true), 1e-8), near(h3$plain_mean_err_null, mean(okd$pl_null), 1e-8),
    near(h3$pct_mpm_rb_eq_exact, 100 * sum(d$mpm_rb) / nrow(d)), near(h3$pct_mpm_plain_eq_exact, 100 * sum(d$mpm_pl) / nrow(d)))
}
chk(g, "H1 (n, failed, bias, RMSE, median|e|, 90th pct |e|, lower-bound coverage) for 12 cells", sapply(G, function(v) all(v[1:7])))
chk(g, "H2 (% SMC HPM = exact, % exact = truth, % SMC = truth; failed counted as not equal) for 12 cells", sapply(G, function(v) all(v[8:10])))
chk(g, "H3 (RB and plain mean/p90 of max error, true/null mean error, % MPM = exact MPM) for 12 cells", sapply(G, function(v) all(v[11:20])))
chk(g, "failed fit (D, p=10 S2 c100) stays in the denominator", H1[p == 10 & scale_key == "c100" & scenario == "2", n_smc_failed == 1 & n_cases == 3] && H2[p == 10 & scale_key == "c100" & scenario == "2", pct_smc_hpm_eq_exact <= 200 / 3 + 1e-9])
hl <- readLines(file.path(out, "HEADLINE.md"))
chk(g, "HEADLINE.md has exactly the four questions H1-H4 and nothing else at level 2", identical(grep("^## ", hl, value = TRUE), c("## H1. Is the evidence estimate accurate?", "## H2. Is the HPM accurate?", "## H3. Are the PIPs accurate (RB and plain)?", "## H4. Exact recovery of the true support")))
chk(g, "HEADLINE.md H4 shows LASSO cvmin pooled count for p=8, c100", {
  cc <- cases[cases$p == 8 & cases$scale_key == "c100", ]; n_ex <- sum(sapply(cc$case_id, function(cid) kind_of(cid, "LASSO") == "exact"))
  h4 <- hl[grep("^## H4", hl):length(hl)]; i <- grep("p = 8, c100", h4)[1L]; blk <- h4[i:(i + 8L)]
  any(grepl(sprintf("^\\| LASSO \\| cvmin .*\\| %d/6 \\(%d/6\\) \\|$", n_ex, n_ex), blk)) })
chk(g, "all output files written", all(file.exists(file.path(out, c("case_smc_accuracy.csv", "case_selection.csv", "case_theory.csv", "H1_logZ.csv", "H2_hpm.csv", "H3_pip.csv", "H4_recovery.csv", "HEADLINE.md", "case_stability.csv", "flag_error_2x2.csv", "se_calibration.csv")))))

# ================================ G9 theory measures ============================================================================
g <- "G9 theory"
chk(g, "one case_theory row per case", nrow(thy) == 24L && !anyDuplicated(thy$case_id))
T9 <- sapply(FX$cases$case_id, function(cid) {
  x <- EXP[[cid]]; inp <- readRDS(file.path(work, "inputs", sprintf("p%04d", x$p), paste0(x$ds, ".rds")))
  sco <- make_scorer(inp$X, as.numeric(inp$Y[, x$ci$scale_key])); setup <- rebuild_setup(sco); tr <- thy[case_id == cid]
  bf <- sapply(0:2, function(d) pi0_Rd_bruteforce(setup, x$S0, d))
  near(c(tr$log_pi0_R0, tr$log_pi0_R1, tr$log_pi0_R2), bf, 1e-9) && near(tr$log_pi0_S0, v3_start_logmass(setup$start, x$S0), 1e-12) && abs(tr$pi0_S0_tables_diff) < 1e-9 &&
    near(tr$pi0_R1, exp(bf[2]), 1e-9) && tr$pi0_R0 <= tr$pi0_R1 + 1e-12 && tr$pi0_R1 <= tr$pi0_R2 + 1e-12 && tr$pi0_S0 <= tr$pi0_R0 + 1e-12 && near(tr$log_Zbar0, setup$start$log_Zbar0, 1e-12)
})
chk(g, "pi0(S0) and pi0(R_d), d = 0, 1, 2: DP equals brute-force summation of v3_start_logmass (24 cases); pi0(S0) via tables; monotone in d", T9)
chk(g, "blocks_match: TRUE except case E (blocks altered in the record)", {
  b <- thy[, .(case_id, blocks_match)]; all(b$blocks_match[b$case_id != FX$special$E] %in% TRUE) && isFALSE(b$blocks_match[b$case_id == FX$special$E]) })
chk(g, "scored-set coverage in case_theory equals the injected fraction", near(thy[case_id != FX$special$D, scored_coverage], ifelse(thy$case_id[thy$case_id != FX$special$D] == FX$special$Fc, 0.5, 0.999), 1e-9) && is.na(thy[case_id == FX$special$D, scored_coverage]))
chk(g, "truth trace from the scored set: scored iff injected or the HPM equals the truth; first phase 'pilot'", {
  tt <- thy[match(names(FX$injs), case_id)]; inj_ts <- sapply(FX$injs, function(i) i$truth_scored); okm <- !sapply(EXP[names(FX$injs)], function(x) x$failed)
  identical(as.logical(tt$truth_scored[okm]), unname(inj_ts[okm] | sapply(EXP[names(FX$injs)], function(x) setequal(x$hpm, x$S0))[okm])) && all(tt$truth_first_phase[okm & tt$truth_scored %in% TRUE] == "pilot") && all(is.na(tt$truth_first_phase[okm & tt$truth_scored %in% FALSE])) && all(is.na(tt$truth_scored[!okm])) })
chk(g, "truth vs HPM score and miss class in case_theory", all(sapply(names(FX$injs), function(cid) { x <- EXP[[cid]]; tr <- thy[case_id == cid]
  if (x$failed) return(is.na(tr$miss_class)); near(tr$truth_minus_smc_hpm, x$F_truth - x$Fh, 1e-9) && near(tr$truth_minus_exact_hpm, x$F_truth - x$ex$top$F[1L], 1e-9) &&
    identical(tr$miss_class, if (setequal(x$hpm, x$S0)) "hit" else if (x$F_truth > x$Fh) "search_miss" else "posterior_miss") && near(tr$log_truth_mass, x$F_truth - x$logZ, 1e-9) })))
# DP at p = 20 against brute force (the brief's validation size): one n = 200 dataset with blocks of 5, S0 = {3, 7, 14, 16}
set.seed(2026); n20 <- 200L; p20 <- 20L; S20 <- c(3L, 7L, 14L, 16L)
Sig <- diag(p20); for (b in seq(1, p20, by = 5)) { ix <- b:(b + 4); Sig[ix, ix] <- 0.4; diag(Sig) <- 1 }
X20 <- matrix(as.numeric(scale(matrix(rnorm(n20 * p20), n20) %*% chol(Sig))), n20, p20); y20 <- as.numeric(X20[, S20] %*% c(1.4, -1, 1.8, -1.2) + rnorm(n20))
sco20 <- make_scorer(X20, y20); set20 <- rebuild_setup(sco20)
dp20 <- pi0_dp(set20, S20, 2L); bf20 <- sapply(0:2, function(d) pi0_Rd_bruteforce(set20, S20, d))
chk(g, "p = 20 (n = 200, B = 4, 6 blocks): DP equals brute-force sum over R_d for d = 0, 1, 2", near(unname(dp20), bf20, 1e-10), paste(format(unname(dp20)), collapse = " "))
chk(g, "p = 20: pi0(S0) from v3_start_logmass equals the table product", abs(pi0_S0_tables(set20, S20) - v3_start_logmass(set20$start, S20)) < 1e-10)
chk(g, "p = 20: log varpi(k) read from the scorer equals ctx$log_w - ctx$log_W_K", near(log_varpi_by_size(set20$ctx), set20$ctx$log_w - set20$ctx$log_W_K, 1e-10))
# a dropped true variable: pi0 = 0 (log -Inf)
X20d <- X20; X20d[, 14] <- X20d[, 13]
rowd <- tryCatch(theory_case_row(X20d, y20, S20, list(case_id = "dup"), td = NULL), error = function(e) NULL)
chk(g, "true variable dropped by preprocessing (duplicate column): S0_retained FALSE and pi0 = 0 (or the duplicate handled)", !is.null(rowd) && (isFALSE(rowd$S0_retained) && rowd$pi0_S0 == 0 || isTRUE(rowd$S0_retained)))

# ---- TD audit: engine (lowp_td), R stand-in, and an independent mask-based reference -----------------------------------------------
g <- "G10 TD audit"
td_ref <- function(Fm, p, K, S0, d, margin = 0, pool = NULL) {     # independent implementation on the full F table (index = mask + 1), both variants
  S0m <- sum(2^(S0 - 1)); nulls <- setdiff(seq_len(p), S0); pool <- if (is.null(pool)) nulls else pool
  Ps <- list(integer(0)); if (d >= 1) for (sz in 1:min(d, length(pool))) Ps <- c(Ps, combn(pool, sz, simplify = FALSE))
  new_acc <- function() list(cnt = c(0, 0, 0), viol = c(0, 0, 0), tight = c(0, 0, 0), mn = c(Inf, Inf, Inf))
  acc_ <- list(literal = new_acc(), toward = new_acc()); truthin <- 0
  upd <- function(a, cl, m) { a$cnt[cl] <- a$cnt[cl] + 1; if (m < margin) a$viol[cl] <- a$viol[cl] + 1 else if (m == margin) a$tight[cl] <- a$tight[cl] + 1; a$mn[cl] <- min(a$mn[cl], m); a }
  for (u in 0:(2^length(S0) - 1)) for (P in Ps) {
    U <- S0[bitwAnd(u, 2^(seq_along(S0) - 1)) > 0]; S <- c(U, P); sm <- sum(2^(S - 1)); k <- length(S); F0 <- Fm[sm + 1]
    if (k > K) next
    mv <- list()
    if (k < K) for (l in setdiff(seq_len(p), S)) mv[[length(mv) + 1L]] <- list(kind = "a", j = 0, l = l, nm = sm + 2^(l - 1))
    for (j in S) mv[[length(mv) + 1L]] <- list(kind = "r", j = j, l = 0, nm = sm - 2^(j - 1))
    for (j in S) for (l in setdiff(seq_len(p), S)) mv[[length(mv) + 1L]] <- list(kind = "s", j = j, l = l, nm = sm - 2^(j - 1) + 2^(l - 1))
    gv <- vapply(mv, function(m) Fm[m$nm + 1] - F0, 0)
    miss <- setdiff(S0, S); extra <- setdiff(S, S0); cl <- if (length(miss)) 1 else if (length(extra)) 2 else 3
    if (cl == 3) { m <- -max(gv); acc_$literal <- upd(acc_$literal, 3, m); acc_$toward <- upd(acc_$toward, 3, m); next }
    isT <- vapply(mv, function(m) if (cl == 1) m$kind == "a" && m$l %in% S0 else m$kind == "r" && !(m$j %in% S0), TRUE)
    best <- -Inf; bi <- NA
    for (i in which(isT)) { mo <- if (length(gv) > 1) max(gv[-i]) else -Inf; mi <- gv[i] - mo; if (mi > best) { best <- mi; bi <- i } }
    mlit <- if (!any(isT)) -Inf else best
    if (mlit < margin && any(isT)) { oi <- setdiff(seq_along(gv), bi)[which.max(gv[-bi])]; o <- mv[[oi]]; if (o$kind == "s" && !(o$j %in% S0) && o$l %in% S0) truthin <- truthin + 1 }
    redu <- vapply(mv, function(m) popcount_int(as.integer(bitwXor(as.integer(m$nm), as.integer(S0m)))) < popcount_int(as.integer(bitwXor(as.integer(sm), as.integer(S0m)))), TRUE)
    mtow <- if (!any(redu)) -Inf else if (all(redu)) Inf else max(gv[redu]) - max(gv[!redu])
    acc_$literal <- upd(acc_$literal, cl, mlit); acc_$toward <- upd(acc_$toward, cl, mtow)
  }
  c(acc_$literal, list(literal = acc_$literal, toward = acc_$toward, truthin = truthin))
}
td_match <- function(res, ref) {      # res = td_slow / run_td result; ref = td_ref result
  one <- function(a, b) identical(a$clauses$n_centres, as.integer(b$cnt)) && identical(a$clauses$n_violations, as.integer(b$viol)) && identical(a$clauses$n_tight, as.integer(b$tight)) &&
    near(ifelse(is.na(a$clauses$min_margin), Inf, a$clauses$min_margin), b$mn, 1e-7)
  one(res$literal, ref$literal) && one(res$toward, ref$toward) && isTRUE(res$complete) &&
    identical(sum(res$diagnosis$n[res$diagnosis$o_label == "swap_null_out_truth_in"]), as.integer(ref$truthin))
}
for (cid in c("p0008_S1_r001_c100", "p0008_S2_r002_c050", "p0010_S1_r003_c100", "p0010_S2_r001_c050")) {
  x <- EXP[[cid]]; inp <- readRDS(file.path(work, "inputs", sprintf("p%04d", x$p), paste0(x$ds, ".rds"))); yy <- as.numeric(inp$Y[, x$ci$scale_key]); sco <- make_scorer(inp$X, yy)
  for (d in 1:2) {
    ref <- td_ref(x$Fm, x$p, x$p, x$S0, d)
    sl <- td_slow(sco, x$S0, d)
    chk(g, sprintf("%s d=%d: R stand-in equals independent reference (literal and toward: centres, violations, ties, min margins; truth-in-swap diagnosis)", cid, d), td_match(sl, ref))
    if (enum_ok) {
      en <- run_td(inp$X, yy, sco, x$S0, d, engine = "enum")
      chk(g, sprintf("%s d=%d: lowp_td (C++) literal and toward equal the independent reference", cid, d), td_match(en, ref), paste("engine:", en$engine))
    }
  }
}
if (!enum_ok) skip(g, "lowp_td (C++) vs reference", "lowp_enum.R not available")
# swaps at |S| = K: n = 10, p = 8 gives K = 5; d = 3 reaches centres of size 5 = K
set.seed(5); XK <- matrix(as.numeric(scale(matrix(rnorm(10 * 8), 10))), 10, 8); S0K <- c(2L, 6L); yK <- as.numeric(XK[, S0K] %*% c(1.5, -1.2) + rnorm(10, 0, 0.7))
scK <- make_scorer(XK, yK); FmK <- rep(NA_real_, 2^8); for (m in 0:(2^8 - 1)) { S <- which(bitwAnd(m, 2^(0:7)) > 0); if (length(S) <= scK$K) FmK[m + 1] <- scK$F(S) }
for (d in 2:3) {
  refK <- td_ref(FmK, 8, scK$K, S0K, d); slK <- td_slow(scK, S0K, d)
  chk(g, sprintf("K < p (n = 10, p = 8, K = 5), d = %d: stand-in equals reference (swaps feasible at |S| = K)", d), scK$K == 5L && td_match(slK, refK))
  if (enum_ok) chk(g, sprintf("K < p, d = %d: lowp_td (C++) equals reference (swaps feasible at |S| = K)", d), td_match(run_td(XK, yK, scK, S0K, d, engine = "enum"), refK))
}
chk(g, "TD restricted null pool: d = 1 with a pool of 3 nulls equals the reference with that pool", {
  x <- EXP[["p0010_S1_r001_c100"]]; inp <- readRDS(file.path(work, "inputs/p0010", paste0(x$ds, ".rds"))); sco <- make_scorer(inp$X, as.numeric(inp$Y[, "c100"]))
  pool <- setdiff(1:10, x$S0)[1:3]; ref <- td_ref(x$Fm, 10, 10, x$S0, 1, pool = pool); sl <- td_slow(sco, x$S0, 1, null_pool = pool)
  td_match(sl, ref) && isTRUE(sl$restricted) && sl$null_pool_size == 3L })
chk(g, "TD margin parameter: a margin above every observed margin makes every centre violate (both variants)", {
  x <- EXP[["p0008_S1_r001_c100"]]; inp <- readRDS(file.path(work, "inputs/p0008", paste0(x$ds, ".rds"))); sco <- make_scorer(inp$X, as.numeric(inp$Y[, "c100"]))
  sl <- td_slow(sco, x$S0, 1, margin = 1e6); all(sl$literal$clauses$n_violations == sl$literal$clauses$n_centres) && all(sl$toward$clauses$n_violations == sl$toward$clauses$n_centres) })
chk(g, "TD max_scores stops the stand-in with complete = FALSE", {
  x <- EXP[["p0008_S1_r001_c100"]]; inp <- readRDS(file.path(work, "inputs/p0008", paste0(x$ds, ".rds"))); sco <- make_scorer(inp$X, as.numeric(inp$Y[, "c100"]))
  sl <- td_slow(sco, x$S0, 2, max_scores = 50); !sl$complete && sl$n_centres_done < sl$n_centres_total })
chk(g, "literal fails when a truth-in swap exists and the diagnosis counts it (p0008_S1_r001_c100, d = 1)", {
  x <- EXP[["p0008_S1_r001_c100"]]; inp <- readRDS(file.path(work, "inputs/p0008", paste0(x$ds, ".rds"))); sco <- make_scorer(inp$X, as.numeric(inp$Y[, "c100"]))
  sl <- td_slow(sco, x$S0, 1); la <- sl$literal$clauses; ta <- sl$toward$clauses
  la$n_violations[1] > 0 && sum(sl$diagnosis$n[sl$diagnosis$o_label == "swap_null_out_truth_in"]) > 0 && la$n_violations[1] <= la$n_centres[1] })
chk(g, "case_theory TD columns (td{d}_literal_*, td{d}_toward_*, truth-in-swap counts) agree with the reference for d = 1, 2", {
  cid <- "p0008_S1_r001_c100"; x <- EXP[[cid]]; tr <- thy[case_id == cid]; r1 <- td_ref(x$Fm, 8, 8, x$S0, 1); r2 <- td_ref(x$Fm, 8, 8, x$S0, 2)
  tr$td1_literal_add_true_n == r1$cnt[1] && tr$td1_literal_at_S0_n == 1 && tr$td2_literal_add_true_viol == r2$literal$viol[1] && near(tr$td2_literal_min_margin, min(r2$literal$mn), 1e-7) &&
  tr$td1_literal_violations == sum(r1$literal$viol) && tr$td2_toward_violations == sum(r2$toward$viol) && near(tr$td2_toward_min_margin, min(r2$toward$mn), 1e-7) &&
  tr$td1_literal_viol_truthin_swap == r1$truthin && tr$td2_literal_viol_truthin_swap == r2$truthin && tr$td1_literal_viol_ab == r1$literal$viol[1] + r1$literal$viol[2] })
if (enum_ok) {
  fx_models <- list(integer(0), 1L, c(2L, 6L), c(1L, 3L, 5L, 7L))
  x <- EXP[["p0008_S1_r001_c100"]]; inp <- readRDS(file.path(work, "inputs/p0008", paste0(x$ds, ".rds"))); yy <- as.numeric(inp$Y[, "c100"]); sco <- make_scorer(inp$X, yy)
  lm <- lowp_score_models(inp$X, yy, fx_models)
  chk("G10 TD audit", "scorer F equals lowp_score_models F (same arithmetic)", near(lm$F, sapply(fx_models, sco$F), 1e-10), paste("max abs diff", format(max(abs(lm$F - sapply(fx_models, sco$F))))))
}

# ================================ G11 p >> n runner =============================================================================
g <- "G11 run_theory_H"
pH <- 60L; nH <- 100L; S0H <- c(5L, 31L)
set.seed(77); XH <- matrix(as.numeric(scale(matrix(rnorm(nH * pH), nH))), nH, pH); yH <- as.numeric(XH[, S0H] %*% c(1.5, -1.2) + rnorm(nH))
dirH <- file.path(work, "H"); dir.create(dirH)
saveRDS(list(X = XH, Y = cbind(c100 = yH, c075 = yH, c050 = yH, c035 = yH, c025 = yH), dataset_id = "p0060_S1_r001", p = pH, scenario = 1L, replicate = 1L), file.path(dirH, "inputs.rds"))
saveRDS(list(active = S0H), file.path(dirH, "truth.rds"))
scH <- make_scorer(XH, yH); setH <- rebuild_setup(scH)
recH <- list(rows = data.frame(case_id = "p0060_S1_r001_c100", dataset_id = "p0060_S1_r001", method_id = "SMCBVS", rule_id = c("hpm", "pip05"), role = c("primary", "S0"), status = "ok", support = "5;31", runtime_s = 1, diag_flag = FALSE, p = pH),
             fit = list(status = "completed", estimates_available = TRUE, hpm = S0H, hpm_F = scH$F(S0H), blocks = lapply(setH$blocks, as.integer), preprocessing = list(kept = 1:pH),
                        log_Z = -10, log_Z_r = rep(-10, 4), pip_primary = setNames(rep(0.01, pH), 1:pH)), native_status = "completed", estimates_available = TRUE,
             case = list(dataset_id = "p0060_S1_r001", case_id = "p0060_S1_r001_c100", p = pH, scenario = 1L, replicate = 1L, scale_key = "c100"), runtime_s = 1)
saveRDS(recH, file.path(dirH, "rec.rds"))
rH <- theory_H_run(file.path(dirH, "rec.rds"), file.path(dirH, "inputs.rds"), file.path(dirH, "truth.rds"), "c100", td_d = 0L, restricted_d1 = TRUE)
rH0 <- theory_H_run(file.path(dirH, "rec.rds"), file.path(dirH, "inputs.rds"), file.path(dirH, "truth.rds"), "c100")
bfH <- sapply(0:1, function(d) pi0_Rd_bruteforce(setH, S0H, d))
chk(g, "p = 60 record: pi0(S0), pi0(R_0), pi0(R_1) equal brute force; coverage NA (no exact Z)", near(c(rH$log_pi0_R0, rH$log_pi0_R1), bfH, 1e-9) && near(rH$log_pi0_S0, v3_start_logmass(setH$start, S0H), 1e-12) && is.na(rH$scored_coverage) && is.na(rH$log_truth_mass))
chk(g, "blocks of the record equal the recomputed blocks; HPM = truth gives a hit", isTRUE(rH$blocks_match) && identical(rH$miss_class, "hit") && isTRUE(rH$hpm_eq_truth))
poolH <- td_null_pool_neighbours(scH, S0H)
chk(g, "TD d = 0 (all nulls) and opt-in restricted d = 1 (union of core neighbour lists, columns td1r_*) are labelled", isFALSE(rH$td0_restricted) && isTRUE(rH$td1r_restricted) && length(poolH) > 0 && length(poolH) < pH - 2L && !is.na(rH$td0_literal_min_margin) && !is.na(rH$td1r_literal_min_margin) && !is.na(rH$td1r_toward_min_margin))
refH <- td_slow(scH, S0H, 1, null_pool = poolH)
chk(g, "restricted d = 1 TD equals the R stand-in with the same pool", identical(as.integer(rH$td1r_literal_add_true_n), refH$literal$clauses$n_centres[1]) && near(rH$td1r_literal_min_margin, min(refH$literal$clauses$min_margin), 1e-7) && near(rH$td1r_toward_min_margin, min(refH$toward$clauses$min_margin), 1e-7))
chk(g, "default p >> n run: TD d = 0 only (no d = 1 columns, no restricted columns)", !any(grepl("^td1", names(rH0))) && "td0_literal_min_margin" %in% names(rH0) && "td0_toward_min_margin" %in% names(rH0))
cli_out <- file.path(dirH, "cli.csv")
st <- suppressWarnings(system2(file.path(R.home("bin"), "Rscript.exe"), c(shQuote(file.path(SC, "run_theory_H.R")), "--record", shQuote(file.path(dirH, "rec.rds")), "--inputs", shQuote(file.path(dirH, "inputs.rds")),
        "--truth", shQuote(file.path(dirH, "truth.rds")), "--scale", "c100", "--out", shQuote(cli_out), "--td-d", "0"), stdout = TRUE, stderr = TRUE))
chk(g, "CLI Rscript run_theory_H.R writes case_theory row", file.exists(cli_out) && near(data.table::fread(cli_out)$log_pi0_S0, rH$log_pi0_S0, 1e-9))

# ================================ G12 CLI end to end ============================================================================
g <- "G12 CLI"
out2 <- file.path(work, "analysis_cli")
st <- suppressWarnings(system2(file.path(R.home("bin"), "Rscript.exe"), c(shQuote(file.path(SC, "run_scoring.R")), "--study", shQuote(work), "--results",
        shQuote(paste(file.path(work, "results", c("exact", "smc", "bench")), collapse = ",")), "--out", shQuote(out2), "--td-d", "none", "--registry", shQuote(REG), "--partial", "1"), stdout = TRUE, stderr = TRUE))
chk(g, "Rscript run_scoring.R runs and writes the headline files", file.exists(file.path(out2, "HEADLINE.md")) && file.exists(file.path(out2, "case_selection.csv")))
a2 <- data.table::fread(file.path(out2, "case_smc_accuracy.csv")); a1 <- data.table::fread(file.path(out, "case_smc_accuracy.csv"))
chk(g, "CLI output equals the in-process output (accuracy table)", nrow(a1) == nrow(a2) && near(a1$e, a2$e, 1e-12) && identical(a1$hpm_eq_exact, a2$hpm_eq_exact))
chk(g, "HEADLINE.md is identical between runs", identical(readLines(file.path(out, "HEADLINE.md")), readLines(file.path(out2, "HEADLINE.md"))))
chk(g, "CSV round trip keeps NA vs empty support in selection table (failed rows have NA k)", {
  s2 <- data.table::fread(file.path(out, "case_selection.csv")); all(is.na(s2$k[s2$error_type == "failed"])) })

source(file.path(here, "regressions_review.R"))
source(file.path(here, "regressions_recheck.R"))

# ================================ report ===========================================================================================
tot <- RES; npass <- sum(tot$pass, na.rm = TRUE); nfail <- sum(!tot$pass, na.rm = TRUE); nskip <- sum(is.na(tot$pass))
grp <- unique(tot$group)
L <- c("# Scoring tests: report", "", sprintf("Run: %s UTC. R %s. Enumerator library (lowp_enum.R): %s.", format(Sys.time(), tz = "UTC", "%Y-%m-%d %H:%M"), getRversion(), if (enum_ok) "loaded, C++ lowp_td exercised" else "NOT available, C++ checks skipped"),
       sprintf("Fixture: p in {8, 10}, S1-S2, 3 replicates, c100/c050 = 24 cases, 12 exact posteriors by brute force (2^p models), 30 mock SMC records (24 main + 6 repeat seeds), 68 benchmark rule rows. Assertions: %d, passed %d, failed %d, skipped %d.", nrow(tot), npass, nfail, nskip), "",
       "| Group | Assertions | PASS | FAIL | SKIP | Verdict |", "|---|---|---|---|---|---|")
for (gg in grp) { d <- tot[tot$group == gg, ]; L <- c(L, sprintf("| %s | %d | %d | %d | %d | %s |", gg, nrow(d), sum(d$pass, na.rm = TRUE), sum(!d$pass, na.rm = TRUE), sum(is.na(d$pass)), if (any(!d$pass, na.rm = TRUE)) "FAIL" else "PASS")) }
L <- c(L, "", "## Every assertion", "", "| Group | Assertion | Result | Note |", "|---|---|---|---|")
for (i in seq_len(nrow(tot))) L <- c(L, sprintf("| %s | %s | %s | %s |", tot$group[i], gsub("\\|", "/", tot$name[i]), if (is.na(tot$pass[i])) "SKIP" else if (tot$pass[i]) "PASS" else "FAIL", gsub("\\|", "/", tot$note[i])))
writeLines(L, file.path(here, "TEST_REPORT.md"), useBytes = TRUE)
invisible(file.copy(file.path(out, "HEADLINE.md"), file.path(here, "EXAMPLE_HEADLINE_fixture.md"), overwrite = TRUE))
cat(sprintf("TESTS: %d assertions, %d passed, %d failed, %d skipped\n", nrow(tot), npass, nfail, nskip))
cat("elapsed", format(round(as.numeric(difftime(Sys.time(), t0, units = "mins")), 1)), "min\n")
if (nfail > 0) { print(tot[!is.na(tot$pass) & !tot$pass, c("group", "name", "note")]); quit(status = 1L) }
