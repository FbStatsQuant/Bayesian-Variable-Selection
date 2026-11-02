# regressions_review.R -- one regression test per adversarial probe of the independent review (REVIEW_d_scoring_sol.md, findings 1-12).
# Sourced by test_scoring.R (shares chk(), near(), FX, work, REG, res, acc ...).
expect_err <- function(expr, pattern = NULL) { r <- try(expr, silent = TRUE); inherits(r, "try-error") && (is.null(pattern) || grepl(pattern, as.character(r))) }
cp_study <- function(name) {
  d <- file.path(work, name); unlink(d, recursive = TRUE); dir.create(d)
  for (sub in c("inputs", "truth", "manifests", "results")) file.copy(file.path(work, sub), d, recursive = TRUE)
  file.copy(REG, file.path(d, "registry_fixture.csv")); d
}
runq <- function(study, results = file.path(study, "results", c("exact", "smc", "bench")), registry = file.path(study, "registry_fixture.csv"), ...)
  run_scoring(study, results, file.path(study, "analysis"), td_d = integer(0), theory = FALSE, verbose = FALSE, registry = registry, partial = TRUE, ...)
A_ <- FX$special$A; main_acc <- res$acc[rep == 0L]

# ============ G13 finding 1: missing main fits stay in every headline denominator ============
g <- "G13 missing main fit (finding 1)"
st <- cp_study("s_missing"); file.remove(file.path(st, "results/smc/p0008", A_, c("SMCBVS.rds", "SMCBVS.done")))
r1 <- runq(st)
cell <- function(H, p_, sc_, scn) H[p == p_ & scale_key == sc_ & scenario == scn]
c1 <- cell(r1$H1, 8L, "c100", "1"); c2 <- cell(r1$H2, 8L, "c100", "1")
hits_others <- main_acc[p == 8 & scale_key == "c100" & scenario == 1 & case_id != A_, sum(hpm_eq_exact %in% TRUE)]
chk(g, "absent main (repeats still present): n_cases stays 3, n_smc_missing = 1, n_evidence = 2", c1$n_cases == 3 && c1$n_smc_missing == 1 && c1$n_evidence == 2 && c2$n_cases == 3 && c2$n_smc_missing == 1)
chk(g, "H2 divides by 3 expected cases (not 2 observed): pct = hits / 3", near(c2$pct_smc_hpm_eq_exact, 100 * hits_others / 3))
h4 <- r1$H4[method_id == "SMCBVS" & rule_id == "hpm" & scenario != "all"]
chk(g, "H1, H2, H3 and H4 agree on the cell sizes", {
  all(sapply(seq_len(nrow(r1$H1)), function(i) { x <- r1$H1[i]; if (x$scenario == "all") return(TRUE)
    x$n_cases == h4[p == x$p & scale_key == x$scale_key & scenario == x$scenario, n_cases] && x$n_cases == r1$H2[p == x$p & scale_key == x$scale_key & scenario == x$scenario, n_cases] &&
    x$n_cases == r1$H3[p == x$p & scale_key == x$scale_key & scenario == x$scenario, n_cases] })) })
chk(g, "the repeat-only case keeps its repeat rows in case_smc_accuracy but no main row", nrow(r1$acc[case_id == A_ & rep == 0L]) == 0L && nrow(r1$acc[case_id == A_ & rep > 0L]) == 2L)
st2 <- cp_study("s_nosmc"); unlink(file.path(st2, "results/smc"), recursive = TRUE)
r2 <- runq(st2, results = file.path(st2, "results", c("exact", "bench")))
chk(g, "no SMC output at all: H1-H3 and HEADLINE still produced, every case counted missing", file.exists(file.path(st2, "analysis/HEADLINE.md")) && nrow(r2$H1) > 0 &&
    all(r2$H1$n_smc_missing == r2$H1$n_cases) && all(r2$H2$pct_smc_hpm_eq_exact == 0) && all(r2$H3$n_rb == 0) && all(r2$H4[method_id == "SMCBVS" & scenario == "all", n_exact == 0]))

# ============ G14 finding 5: roster comes from the manifest and the registry, never from observed files ============
g <- "G14 roster (finding 5)"
st <- cp_study("s_roster")
mf <- file.path(st, "manifests/inputs_manifest_lowp.csv"); man <- read.csv(mf)
for (sub in c("inputs", "truth")) file.copy(file.path(st, sub, "p0008", paste0("p0008_S1_r003.rds")), file.path(st, sub, "p0008", "p0008_S1_r004.rds"))
write.csv(rbind(man, data.frame(dataset_id = "p0008_S1_r004", p = 8L, scenario = 1L, replicate = 4L)), mf, row.names = FALSE)
regf <- file.path(st, "registry_ghost.csv"); writeLines(c(readLines(REG), "GHOST,rule1,primary,TRUE,TRUE"), regf)
r3 <- runq(st, registry = regf)
c3 <- cell(r3$H2, 8L, "c100", "1")
chk(g, "a manifest dataset with no result at all is counted (4 cases: 1 missing SMC); the changed manifest SHA-256 invalidates the sealed EXACT records bound to the old manifest (all 4 count as no exact, reason logged)", c3$n_cases == 4 && c3$n_smc_missing == 1 && c3$n_exact_missing == 4 &&
    any(grepl("manifest SHA-256 differs", r3$exact_diagnostics$detail)) && any(r3$exact_diagnostics$reason == "no_exact_file"))
gh <- r3$H4[method_id == "GHOST" & p == 8 & scale_key == "c100"]
chk(g, "a registry method with no result file anywhere reports 0/n per scenario and 0/n pooled", nrow(gh) == 3L && all(gh$n_exact == 0) && all(gh$recovery == sprintf("0/%d", gh$n_cases)) && gh[scenario == "all", n_cases] == 7L)
st <- cp_study("s_notruth"); file.remove(file.path(st, "truth/p0008/p0008_S1_r001.rds"))
chk(g, "a rostered dataset without a truth file is a scoring-completeness error (not a smaller denominator)", expect_err(runq(st), "no truth file"))
st <- cp_study("s_nomanifest"); file.remove(file.path(st, "manifests/inputs_manifest_lowp.csv"))
chk(g, "no manifest: error in production mode; partial mode lists inputs/ and labels HEADLINE as partial", expect_err(run_scoring(st, file.path(st, "results", c("exact", "smc", "bench")), file.path(st, "a1"), td_d = integer(0), theory = FALSE, verbose = FALSE, registry = file.path(st, "registry_fixture.csv"), partial = FALSE), "manifest") &&
    { r <- runq(st); any(grepl("PARTIAL", readLines(file.path(st, "analysis/HEADLINE.md")))) })
st <- cp_study("s_grid")
chk(g, "production mode checks the planned grid (6 scenarios x 100 replicates)", expect_err(run_scoring(st, file.path(st, "results", c("exact", "smc", "bench")), file.path(st, "a2"), td_d = integer(0), theory = FALSE, verbose = FALSE, registry = file.path(st, "registry_fixture.csv")), "completeness"))
chk(g, "an unknown id in the case subset is an error", expect_err(runq(st, cases = "p0001_S1_r001_c100"), "outside the roster"))

# ============ G15 finding 2: empty supports ============
g <- "G15 empty supports (finding 2)"
chk(g, "parse_support: integer(0) and numeric(0) stay empty; '' is empty; NA / NULL / character(0) are unavailable", identical(parse_support(integer(0)), integer(0)) && identical(parse_support(numeric(0)), integer(0)) &&
    identical(parse_support(""), integer(0)) && is.null(parse_support(NA_character_)) && is.null(parse_support(NA_integer_)) && is.null(parse_support(NULL)) && is.null(parse_support(character(0))) && identical(parse_support(c(7L, 3L)), c(3L, 7L)))
exE <- list(schema = "lowp_exact_v1", dataset_id = "p0004_S1_r001", p = 4L, n = 50, K = 4L, extra = list(status = "exact", complete = TRUE, retained_columns = 1:4),
            scales = list(c100 = list(log_Z = -1, pip = c(`1` = 0.1, `2` = 0.2, `3` = 0.1, `4` = 0.05), hpm = integer(0), hpm_F = -1, mpm = integer(0), top = NULL)))
esE <- exact_scale(exE, "c100")
chk(g, "exact_scale keeps the integer(0) HPM and MPM from the real API (not NA)", identical(esE$hpm, integer(0)) && identical(esE$mpm, integer(0)))
rowsE <- exact_reference_rows(list(p0004_S1_r001_c100 = esE))
selE <- score_selection(rowsE, list(p0004_S1_r001 = integer(0)), "p0004_S1_r001_c100", data.frame(method_id = "EXACT", rule_id = c("hpm", "mpm"), role = "reference", required = TRUE, in_h4 = TRUE))
chk(g, "empty truth, empty exact HPM / MPM: two successful empty selections with exact recovery (k = 0), support text ''", nrow(selE) == 2L && all(selE$status == "ok") && all(selE$k == 0L) && all(selE$exact) && all(selE$error_type == "none") && all(rowsE$support == ""))
selF <- score_selection(rowsE, list(p0004_S1_r001 = c(2L, 3L)), "p0004_S1_r001_c100", data.frame(method_id = "EXACT", rule_id = c("hpm", "mpm"), role = "reference", required = TRUE, in_h4 = TRUE))
chk(g, "non-empty truth with an empty exact MPM: successful selection, missed_only (not failed)", all(selF$status == "ok") && all(selF$error_type == "missed_only") && all(selF$fn == 2L) && all(selF$k == 0L))
tf <- tempfile(fileext = ".csv"); write_csv_na(data.table::data.table(support = c("", NA, "3;7")), tf); rt <- data.table::fread(tf, colClasses = "character", na.strings = "NA")
chk(g, "CSV round trip keeps '' distinct from NA", identical(rt$support, c("", NA, "3;7")))

# ============ G16 finding 3: dropped true variable ============
g <- "G16 dropped truth (finding 3)"
D8 <- readRDS(file.path(work, "inputs/p0008/p0008_S1_r001.rds")); S0d <- c(2L, 6L)
Xd <- D8$X; Xd[, 6] <- 1; yd <- as.numeric(D8$Y[, "c100"])
scd <- make_scorer(Xd, yd)
chk(g, "a constant true column is dropped by preprocessing (kept = 1:8 without 6)", identical(as.integer(scd$kept), c(1:5, 7:8)))
setd <- rebuild_setup(scd)
brute <- function(S0r, d) {      # explicit summation over feasible retained supports U u P, U subset of the retained truths, P subset of the other retained, |P| <= d
  nul <- setdiff(scd$kept, S0r); tot <- numeric(0)
  for (u in 0:(2^length(S0r) - 1)) { U <- S0r[bitwAnd(u, 2^(seq_along(S0r) - 1)) > 0]
    for (sz in 0:min(d, length(nul))) for (P in if (sz == 0) list(integer(0)) else combn(nul, sz, simplify = FALSE)) tot <- c(tot, v3_start_logmass(setd$start, sort(c(U, P)))) }
  lse(tot) }
smD <- extract_smc(recA); smD$hpm <- c(2L, 3L); smD$hpm_F <- scd$F(c(2L, 3L)); smD$kept <- scd$kept; smD$blocks <- lapply(setd$blocks, as.integer)
thd <- theory_case_row(Xd, yd, S0d, list(case_id = "dropped"), sm = smD, scorer = scd, td = list(d = 1L))
chk(g, "no error with a completed fit; S0_retained FALSE, n_true_dropped 1, status labelled, F_truth NA, miss_class NA", isFALSE(thd$S0_retained) && thd$n_true_dropped == 1 && thd$theory_status == "truth_dropped" && is.na(thd$F_truth) && is.na(thd$miss_class) && is.na(thd$truth_minus_smc_hpm))
chk(g, "pi0(S0) = 0 (infeasible truth) but pi0(R_d) is the mass of the FEASIBLE retained region, not zero", thd$pi0_S0 == 0 && thd$log_pi0_S0 == -Inf &&
    near(c(thd$log_pi0_R0, thd$log_pi0_R1, thd$log_pi0_R2), sapply(0:2, function(d) brute(2L, d)), 1e-10) && thd$pi0_R0 > 0 && thd$pi0_R1 > thd$pi0_R0 && thd$region_basis == "retained_truth_subsets")
chk(g, "TD is undefined for a dropped truth and labelled so (no TD columns, no silent zeros)", identical(thd$td_status, "undefined_truth_dropped") && !any(grepl("^td1_", names(thd))))
chk(g, "blocks are matched through original indices on the dropped-column design", isTRUE(thd$blocks_match))

# ============ G17 finding 4: unavailable evidence / two-island records ============
g <- "G17 evidence validity (finding 4)"
st <- cp_study("s_nae")
mod_rec <- function(cid, f, rep_ = "SMCBVS") { pth <- file.path(st, "results/smc", sprintf("p%04d", as.integer(substr(cid, 2, 5))), cid, paste0(rep_, ".rds")); r <- readRDS(pth); r <- f(r); saveRDS(r, pth) }
cB <- "p0008_S1_r002_c100"; cC <- "p0008_S1_r003_c100"
mod_rec(cB, function(r) { r$fit$log_Z <- NA_real_; r })
mod_rec(cC, function(r) { r$fit$log_Z_r <- r$fit$log_Z_r[1:2]; r })
r4 <- runq(st)
smB <- extract_smc(readRDS(file.path(st, "results/smc/p0008", cB, "SMCBVS.rds")))
chk(g, "completed record with log_Z = NA: ok, HPM usable, evidence unavailable", smB$ok && smB$hpm_ok && !smB$evidence_ok && is.na(smB$log_Z))
a2 <- r4$acc[rep == 0L & case_id %in% c(cB, cC)]
chk(g, "two-island record: no SE, no island statistic (four valid islands required)", all(a2$ok) && all(!a2$evidence_ok) && all(is.na(a2$se)) && all(is.na(a2$e)) && all(a2$hpm_ok))
c1 <- cell(r4$H1, 8L, "c100", "1"); c2 <- cell(r4$H2, 8L, "c100", "1")
chk(g, "H1 reports n_evidence = 1 and every statistic is finite (consistent NA handling); coverage defined on those fits", c1$n_evidence == 1 && all(is.finite(c(c1$bias, c1$rmse, c1$median_abs_e, c1$p90_abs_e, c1$lb_coverage))))
chk(g, "the unavailable evidence does not invalidate the HPM: H2 unchanged", near(c2$pct_smc_hpm_eq_exact, cell(res$H2, 8L, "c100", "1")$pct_smc_hpm_eq_exact))

# ============ G18 finding 6: duplicate result roots ============
g <- "G18 duplicates (finding 6)"
st <- cp_study("s_dup"); dupr <- file.path(st, "rd"); dir.create(dupr); file.copy(list.files(file.path(st, "results"), full.names = TRUE), dupr, recursive = TRUE)
roots_all <- c(file.path(st, "results", c("exact", "smc", "bench")), file.path(dupr, c("exact", "smc", "bench")))
r5 <- runq(st, results = roots_all)
chk(g, "identical copies in two roots are merged: same accuracy rows, same H2, duplicates logged", nrow(r5$acc) == nrow(res$acc) && identical(r5$H2$n_cases, res$H2$n_cases) && near(r5$H2$pct_smc_hpm_eq_exact, res$H2$pct_smc_hpm_eq_exact) &&
    nrow(r5$duplicates) > 0 && all(r5$duplicates$resolution == "identical copies merged") && nrow(r5$stability) == 3L && all(r5$stability$n_attempted == 3L))
dpth <- file.path(dupr, "smc/p0008", A_, "SMCBVS.rds"); rr <- readRDS(dpth); rr$fit$hpm <- c(1L, 2L, 6L); saveRDS(rr, dpth)
chk(g, "conflicting copies are refused", expect_err(runq(st, results = roots_all), "conflicting duplicate"))
r6 <- runq(st, results = roots_all, on_conflict = "first_root")
chk(g, "explicit precedence 'first_root' keeps the first root and records the conflict", any(grepl("conflict: first root wins", r6$duplicates$resolution)) && nrow(r6$acc) == nrow(res$acc))
file.copy(file.path(st, "results/smc/p0008", A_, "SMCBVS.rds"), dpth, overwrite = TRUE)
bpth <- file.path(dupr, "bench/p0008/p0008_S1_r001_c100/LASSO.rds"); br <- readRDS(bpth); br$support[1] <- "1;2;3;4;5"; saveRDS(br, bpth)
chk(g, "conflicting benchmark rows are refused (no silent last-wins)", expect_err(runq(st, results = roots_all[c(1, 2, 3, 4, 5, 6)], on_conflict = "error"), "BENCH"))
chk(g, "repeat fits that share a method seed are refused", { smA2 <- extract_smc(recA); smA3 <- extract_smc(recA, rep = 1L); expect_err(stability_row(list(smA2, smA3)), "share a method seed") })

# ============ G19 finding 7: exact PIPs through the original-index map ============
g <- "G19 exact PIP map (finding 7)"
exD <- exE; exD$p <- 4L; exD$extra$retained_columns <- c(1L, 4L); exD$scales$c100$pip <- c(`1` = 0.8, `4` = 0.2); esD <- exact_scale(exD, "c100")
chk(g, "retained PIPs named by original index are expanded: (.8, 0, 0, .2), kept = {1, 4}", identical(unname(esD$pip), c(0.8, 0, 0, 0.2)) && identical(esD$kept, c(1L, 4L)))
smP <- extract_smc(recA); smP$pip_rb <- setNames(c(0.8, 0, 0, 0.2), 1:4); smP$pip_rb_r <- NULL; smP$pip_plain <- NULL; smP$pip_plain_r <- NULL; smP$kept <- c(1L, 4L); smP$p <- 4L
rowP <- smc_accuracy_row(smP, esD, c(1L, 4L), NULL)
chk(g, "SMC and exact PIP errors are 0 (not NA) on the dropped-column design; kept maps agree", near(rowP$rb_max, 0) && near(rowP$rb_mean_null, 0) && isTRUE(rowP$kept_match))
exD2 <- exD; exD2$scales$c100$pip <- c(`1` = 0.8, `3` = 0.2)
chk(g, "exact PIP names that disagree with the retained-column map are rejected", is.null(exact_scale(exD2, "c100")))

# ============ G20 finding 8: extraction never manufactures values ============
g <- "G20 extraction safety (finding 8)"
recM <- recA; recM$case$p <- 4L; recM$pip <- NULL; recM$fit$pip_primary <- c(`1` = 0.2, `4` = 0.8); recM$fit$preprocessing$kept <- 1:4; recM$fit$pip_r <- NULL; recM$pip_plain <- NULL; recM$fit$pip_plain <- NULL; recM$fit$pip_plain_r <- NULL
smM <- extract_smc(recM)
chk(g, "a named partial PIP that does not cover every retained variable is unavailable (no invented zeros)", is.null(smM$pip_rb) && !smM$rb_ok)
recS <- recA; recS$fit$stage_table <- data.frame(phase = "diag", tier = 0L, iter = 1L, island = 1L, stage = 1L, ess = 1); recS$fit$instrumentation$stages$final <- NULL; recS$instrumentation <- NULL
smS <- extract_smc(recS)
chk(g, "a stage table with no final rows gives min_ess = NA (no fallback to calibration)", is.na(smS$min_ess))
recN <- recA; recN$fit$stage_table$ess <- NA_real_; recN$fit$score_counts <- list(fresh = matrix(NA_real_, 2, 2), logical = matrix(NA_real_, 2, 2))
smN <- extract_smc(recN)
chk(g, "all-NA ESS and score counts stay NA (not Inf / 0)", is.na(smN$min_ess) && is.na(smN$score_fresh) && is.na(smN$score_logical))
esU <- exact_scale(exD, "c100"); esU$hpm <- NULL; esU$mpm <- NULL
rowU <- smc_accuracy_row(extract_smc(recA), esU, S0_of(smA$dataset_id), NULL)
chk(g, "unavailable exact HPM / MPM: exact-vs-truth equalities are NA (not FALSE), like the SMC-vs-exact ones", is.na(rowU$exact_hpm_eq_truth) && is.na(rowU$exact_mpm_eq_truth) && is.na(rowU$hpm_eq_exact))
recF <- recA; recF$fit$pip_primary[1] <- 1.7; recF$pip[1] <- 1.7
chk(g, "out-of-range PIPs are rejected", is.null(extract_smc(recF)$pip_rb))

# ============ G21 finding 9: passing-only recovery ============
g <- "G21 passing-only recovery (finding 9)"
rowsP <- data.frame(case_id = c("p0008_S1_r001_c100", "p0008_S1_r002_c100", "p0008_S1_r003_c100"), dataset_id = c("p0008_S1_r001", "p0008_S1_r002", "p0008_S1_r003"), method_id = "LASSO", rule_id = "cvmin",
                    role = "primary", status = "ok", support = "2;6", runtime_s = 1, diag_flag = c(TRUE, FALSE, NA), adaptation_ids = NA_character_, stringsAsFactors = FALSE)
regP <- data.frame(method_id = "LASSO", rule_id = "cvmin", role = "primary", required = TRUE, in_h4 = TRUE)
selP <- score_selection(rowsP, setNames(rep(list(c(2L, 6L)), 3), unique(rowsP$dataset_id)), rowsP$case_id, regP)
H4P <- H4_recovery(selP)[scenario == "1"]
chk(g, "a flagged exact success is in the all-saved count but not the passing-only count; same fixed denominator; NA flag counts as not flagged", H4P$recovery == "3/3" && H4P$recovery_passing == "2/3" && H4P$n_flagged == 1 && H4P$n_cases == 3)
chk(g, "HEADLINE H4 shows both versions in each cell", any(grepl("3/3 \\(2/3\\)", { f <- tempfile(); write_headline(res$H1, res$H2, res$H3, H4_recovery(selP), f); readLines(f) })))

# ============ G22 finding 10: EXACT readiness ============
g <- "G22 EXACT readiness (finding 10)"
ds8 <- "p0008_S1_r001"; src <- file.path(work, "results/exact/p0008", ds8)
mk <- function(nm) { d <- file.path(work, "exready", nm); unlink(d, recursive = TRUE); dir.create(d, recursive = TRUE); file.copy(list.files(src, full.names = TRUE), d); d }
resn <- function(d) load_exact_checked(file.path(d, "EXACT.rds"), ds8, 8L)
d0 <- mk("ok"); d1 <- mk("nodone"); file.remove(file.path(d1, "EXACT.done"))
d2 <- mk("badsha"); writeLines(paste0(strrep("0", 64), "  EXACT.rds"), file.path(d2, "EXACT.sha256"))
d3 <- mk("partial"); xx <- readRDS(file.path(d3, "EXACT.rds")); xx$extra$status <- "partial"; xx$extra$complete <- FALSE; saveRDS(xx, file.path(d3, "EXACT.rds")); hh <- file_sha256(file.path(d3, "EXACT.rds")); writeLines(paste0(hh, "  EXACT.rds"), file.path(d3, "EXACT.sha256")); writeLines(hh, file.path(d3, "EXACT.done"))
d4 <- mk("nosha"); file.remove(file.path(d4, "EXACT.sha256"))
d5 <- mk("wrongds"); xx <- readRDS(file.path(d5, "EXACT.rds")); xx$dataset_id <- "p0008_S1_r002"; saveRDS(xx, file.path(d5, "EXACT.rds")); hh <- file_sha256(file.path(d5, "EXACT.rds")); writeLines(paste0(hh, "  EXACT.rds"), file.path(d5, "EXACT.sha256")); writeLines(hh, file.path(d5, "EXACT.done"))
chk(g, "complete, hashed, status exact: ready", resn(d0)$ok)
chk(g, "no .done marker: refused (no_done_marker)", identical(resn(d1)$reason, "no_done_marker"))
chk(g, "sidecar hash differs from the RDS: refused", identical(resn(d2)$reason, "sha256_sidecar_mismatch"))
chk(g, "status partial / incomplete subset run: refused even with valid hashes (validator reasons logged)", !resn(d3)$ok && grepl("extra\\$status is not exact", resn(d3)$detail) && grepl("^contract:", resn(d3)$reason))
chk(g, "missing sha256 sidecar: refused; envelope of another dataset: refused", identical(resn(d4)$reason, "no_sha256_sidecar") && identical(resn(d5)$reason, "dataset_id_mismatch"))
st <- cp_study("s_exnodone"); file.remove(file.path(st, "results/exact/p0008", ds8, "EXACT.done"))
r7 <- runq(st)
chk(g, "end to end: an uncommitted EXACT unit is not used (no_done_marker in exact_diagnostics, both scales count as no exact reference, EXACT rows not_run)",
    r7$exact_diagnostics[dataset_id == ds8, reason] == "no_done_marker" && is.character(r7$exact_diagnostics$detail) && !any(r7$ref[dataset_id == ds8, has_exact]) && all(r7$sel[dataset_id == ds8 & method_id == "EXACT", status] == "not_run") && cell(r7$H2, 8L, "c100", "1")$n_exact_missing == 1)

# ============ G23 finding 11: repeat-seed eligibility ============
g <- "G23 repeat seeds (finding 11)"
s0 <- extract_smc(recA); s1 <- extract_smc(recA, rep = 1L); s1$method_seed <- s0$method_seed + 1000; s1$ok <- FALSE; s1$evidence_ok <- FALSE; s1$hpm_ok <- FALSE; s1$rb_ok <- FALSE; s1$plain_ok <- FALSE
st1 <- stability_row(list(s0, s1))
chk(g, "one completed main + one failed repeat: no SD / agreement is reported (>= 2 eligible seeds required), counts shown", st1$n_attempted == 2 && st1$n_completed == 1 && is.na(st1$sd_log_Z) && is.na(st1$hpm_agreement) && is.na(st1$max_pip_sd_rb))
s2 <- extract_smc(recA, rep = 1L); s2$method_seed <- s0$method_seed + 1000; s2$log_Z <- s0$log_Z + 1; s3 <- extract_smc(recA, rep = 2L); s3$method_seed <- s0$method_seed + 2000; s3$log_Z <- s0$log_Z + 2
s3$pip_rb <- NULL; s3$pip_plain <- NULL; s3$rb_ok <- FALSE; s3$plain_ok <- FALSE; s2$pip_rb <- s0$pip_rb + 0.1; s2$pip_plain <- pmin(1, s0$pip_plain + 0.2)
st3 <- stability_row(list(s0, s2, s3))
chk(g, "ragged fields: each statistic reports its own seed count (3 evidence, 2 PIP vectors)", st3$n_evidence == 3 && st3$n_rb == 2 && st3$n_plain == 2 && near(st3$sd_log_Z, 1) && near(st3$max_pip_sd_rb, stats::sd(c(0, 0.1)), 1e-9) && near(st3$max_pip_sd_plain, max(apply(cbind(s0$pip_plain, s2$pip_plain), 1L, stats::sd)), 1e-9))
chk(g, "two completed seeds baseline: SD of log Z, agreement 1, PIP SD", {
  s4 <- extract_smc(recA, rep = 1L); s4$method_seed <- s0$method_seed + 1000; s4$log_Z <- s0$log_Z + 1; s4$pip_rb <- pmin(1, s0$pip_rb + 0.1); x <- stability_row(list(s0, s4))
  near(x$sd_log_Z, sqrt(0.5), 1e-9) && near(x$hpm_agreement, 1) && x$n_completed == 2 })

# ============ G24 finding 12: slow TD skips infeasible centres ============
g <- "G24 TD above K (finding 12)"
set.seed(12); X4 <- matrix(as.numeric(scale(matrix(rnorm(4 * 4), 4))), 4, 4); y4 <- rnorm(4); sc4 <- make_scorer(X4, y4)
sl4 <- tryCatch(td_slow(sc4, c(1L, 2L), 1), error = function(e) e)
chk(g, "p = 4, n = 4 (K = 2), S0 = {1, 2}, d = 1: no error, 3-variable centres skipped and counted", !inherits(sl4, "error") && sc4$K == 2L && sl4$n_centres_skipped_over_K == 2L && sl4$n_centres_total == 10L && sl4$complete && sl4$n_centres_done == sl4$n_centres_total)
if (enum_ok) {
  en4 <- run_td(X4, y4, sc4, c(1L, 2L), 1, engine = "enum")
  chk(g, "the C++ audit and the stand-in agree on the feasible centre set", identical(sum(sl4$literal$clauses$n_centres), as.integer(sum(en4$literal$clauses$n_centres))) && identical(sl4$literal$clauses$n_centres, en4$literal$clauses$n_centres))
}

# ============ G25 review notes: PPV, posterior_miss, ties ============
g <- "G25 review notes"
fe2 <- fe[fe$flag == "escalated" & fe$event == "hpm_ne_exact", ]
f_ <- ev$escalated; v_ <- ev$hpm_ne_exact
chk(g, "PPV = P(event | flag) is asserted too", near(fe2$ppv, if (sum(f_) > 0) sum(f_ & v_) / sum(f_) else NA_real_))
F_tab <- function(S) { S <- sort(S); if (setequal(S, c(1L, 2L))) -1 else if (setequal(S, c(1L, 3L))) -1 else if (setequal(S, 5L)) -5 else if (setequal(S, c(1L, 2L, 3L))) -0.5 else -9 }
mockSc <- list(F = F_tab)
mk_row <- function(h) { s <- extract_smc(recA); s$hpm <- h; s$hpm_F <- F_tab(h); smc_accuracy_row(s, exact_scale(exE, "c100"), c(1L, 2L), mockSc) }
chk(g, "miss classes: hit, search_miss (F(S0) > F(HPM)), posterior_miss (F(S0) <= F(HPM), including an exact tie)",
    identical(mk_row(c(1L, 2L))$miss_class, "hit") && identical(mk_row(5L)$miss_class, "search_miss") && identical(mk_row(c(1L, 3L))$miss_class, "posterior_miss") && identical(mk_row(c(1L, 2L, 3L))$miss_class, "posterior_miss"))
chk(g, "a tied wrong HPM: support unequal to the truth, truth-minus-HPM score exactly 0", { r <- mk_row(c(1L, 3L)); isFALSE(r$hpm_eq_truth) && near(r$truth_minus_smc_hpm, 0) })
lex <- function(L) L[order(vapply(L, function(S) paste(sprintf("%02d", sort(S)), collapse = ""), ""))]
chk(g, "master tie order (lexicographic on original indices): {1,4} precedes {2,3} (fixture key)", identical(lex(list(c(2L, 3L), c(1L, 4L)))[[1L]], c(1L, 4L)))
