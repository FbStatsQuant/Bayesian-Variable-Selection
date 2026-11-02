# regressions_recheck.R -- regression tests for the second independent review (RECHECK_d_sol.md): N1, N2, N3 and the residuals of findings 6, 10, 11.
# Sourced by test_scoring.R after regressions_review.R (shares chk(), near(), FX, work, REG, res, recA, mk(), resn(), cp_study(), runq() ...).

# ============ G26 N1: the registry is derived from the benchmark code, not hand-copied ============
g <- "G26 registry derived from bench_lowp (N1)"
dreg <- build_registry()
SMOKE <- "C:/Users/felip/AppData/Local/Temp/lowp_work/bench_smoke_reviewfix_v6/results/smoke"
chk(g, "42 rows: SMCBVS 2 + EXACT 2 + 38 benchmark rules; in_h4 = the 8 primaries + SMC hpm/pip05 + EXACT hpm/mpm", nrow(dreg) == 42L && sum(dreg$in_h4) == 12L && all(dreg$required))
prim <- dreg[dreg$role == "primary" & dreg$method_id %in% c(paste0("F", 1:5), paste0("A", 1:3)), ]
chk(g, "primary rules: F1-F3 cv_min, F4/F5 ebic1_K37, A1 pip05, A2 ssl_final, A3 ci95", identical(setNames(prim$rule_id, prim$method_id)[c(paste0("F", 1:5), paste0("A", 1:3))],
    c(F1 = "cv_min", F2 = "cv_min", F3 = "cv_min", F4 = "ebic1_K37", F5 = "ebic1_K37", A1 = "pip05", A2 = "ssl_final", A3 = "ci95")))
rl <- function(m, r) dreg$role[dreg$method_id == m & dreg$rule_id == r]
chk(g, "LA-4 roles: cap rows secondary (F4/F5 ebic1, ebic05, bic; F1-F3 ebic1, ebic05); K37 companions and ebic1_lam005 / sic_smax S0; cslead, bfdr10, km2, cv_1se S0",
    all(sapply(c("ebic1", "ebic05", "bic"), function(r) rl("F4", r) == "secondary" && rl("F5", r) == "secondary")) && all(sapply(c("ebic1", "ebic05"), function(r) rl("F1", r) == "secondary")) &&
    rl("F4", "ebic05_K37") == "S0" && rl("F4", "bic_K37") == "S0" && rl("F4", "ebic1_lam005") == "S0" && rl("F5", "sic_smax") == "S0" && rl("F1", "ebic1_K37") == "S0" && rl("F1", "cv_1se") == "S0" &&
    rl("A1", "cslead") == "S0" && rl("A1", "bfdr10") == "S0" && rl("A3", "km2") == "S0")
if (dir.exists(SMOKE)) {
  fs <- list.files(SMOKE, pattern = "\\.rds$", recursive = TRUE, full.names = TRUE)
  sm_rows <- unique(do.call(rbind, lapply(fs, function(f) { x <- readRDS(f); x <- if (is.data.frame(x)) x else x$rows; data.frame(method_id = x$method_id, rule_id = x$rule_id, role = x$role, stringsAsFactors = FALSE) })))
  kd <- paste(dreg$method_id, dreg$rule_id, dreg$role)[dreg$method_id %in% BENCH_IDS]; ks <- paste(sm_rows$method_id, sm_rows$rule_id, sm_rows$role)
  chk(g, sprintf("derived rule set equals the %d (method, rule, role) rows of the real benchmark smoke output (p = 20 and 30, both scales)", length(ks)), length(fs) >= 40 && setequal(kd, ks) && length(kd) == length(ks))
} else skip(g, "derived registry vs real benchmark smoke output", "smoke directory not found")
# H4 picks the K37 primary, not the S0/secondary cap rows
mkb <- function(m, r, role, sup, flag = FALSE) data.frame(case_id = "p0008_S1_r001_c100", dataset_id = "p0008_S1_r001", method_id = m, rule_id = r, role = role, status = "ok", support = sup, runtime_s = 1, diag_flag = flag, diag_codes = NA_character_, adaptation_ids = NA_character_, stringsAsFactors = FALSE)
rowsN1 <- rbind(mkb("F4", "ebic1_K37", "primary", "2;6"), mkb("F4", "ebic1", "secondary", "2;6;1"), mkb("F4", "ebic05_K37", "S0", "2;6"), mkb("F5", "ebic1_K37", "primary", "2;6;3"), mkb("F5", "ebic1", "secondary", "2;6"))
selN1 <- score_selection(rowsN1, list(p0008_S1_r001 = c(2L, 6L)), "p0008_S1_r001_c100", dreg)
h4N1 <- H4_recovery(selN1)[scenario == "1" & method_id %in% c("F4", "F5")]
chk(g, "H4 reports ebic1_K37 as the F4/F5 primary (F4 1/1, F5 0/1) and never the cap rows; missing F4/F5 K37 rows would be not_run", all(h4N1$rule_id == "ebic1_K37") && h4N1[method_id == "F4", n_exact] == 1L && h4N1[method_id == "F5", n_exact] == 0L &&
    selN1[method_id == "F4" & rule_id == "bic_K37", status] == "not_run" && selN1[method_id == "F4" & rule_id == "ebic1", in_h4] == FALSE && selN1[method_id == "F4" & rule_id == "ebic1_K37", in_h4] == TRUE)
chk(g, "an observed role that disagrees with the registry is an error", expect_err(score_selection(rbind(mkb("F4", "ebic1_K37", "S0", "2;6")), list(p0008_S1_r001 = c(2L, 6L)), "p0008_S1_r001_c100", dreg), "role differs"))
st <- cp_study("s_derived"); r8 <- run_scoring(st, file.path(st, "results", c("exact", "smc", "bench")), file.path(st, "analysis"), td_d = integer(0), theory = FALSE, verbose = FALSE, partial = TRUE)
chk(g, "default run uses the derived registry (registry_used.csv = build_registry()); absent benchmark methods are 0/n in H4; the SMC and EXACT rows are scored", {
  ru <- read.csv(file.path(st, "analysis/registry_used.csv"), stringsAsFactors = FALSE)
  identical(paste(ru$method_id, ru$rule_id, ru$role), paste(dreg$method_id, dreg$rule_id, dreg$role)) && all(r8$H4[method_id == "F4" & rule_id == "ebic1_K37" & scenario == "all", n_exact == 0 & n_cases > 0]) &&
    all(r8$H4[method_id == "SMCBVS" & rule_id == "hpm" & scenario == "all", n_cases > 0]) && !any(r8$H4$rule_id == "ebic1" & r8$H4$method_id == "F4") })

# ============ G27 N2: genuine exact-branch SMC record ============
g <- "G27 exact-branch evidence (N2)"
cX <- "p0008_S1_r002_c100"; lzX <- lse(FX$Fall[[cX]])
recX <- readRDS(file.path(work, "results/smc/p0008", cX, "SMCBVS.rds"))
recX$native_status <- "exact"; recX$fit$status <- "exact"; recX$fit$log_Z <- lzX; recX$fit$log_Z_lower95 <- lzX + log(0.05); recX$fit$log_Z_r <- NULL; recX$fit$log_Z_rel_m0 <- NULL
recX$fit$pip_plain <- NULL; recX$fit$pip_plain_r <- NULL; recX$fit$pip_r <- NULL; recX$pip_plain <- NULL; recX$mpm_plain <- NULL; recX$fit$mpm_plain <- NULL; recX$fit$flags <- NULL; recX$fit$stage_table <- NULL
smX <- extract_smc(recX)
chk(g, "exact branch: ok, pooled evidence kept (finite log Z), no islands, no plain PIPs", smX$ok && smX$evidence_ok && !smX$islands_ok && near(smX$log_Z, lzX) && length(smX$log_Z_r) == 0L && is.null(smX$pip_plain) && smX$rb_ok && !smX$plain_ok)
rowX <- smc_accuracy_row(smX, exact_scale(readRDS(file.path(work, "results/exact/p0008/p0008_S1_r002/EXACT.rds")), "c100"), S0_of("p0008_S1_r002"), NULL)
chk(g, "error, relative error and lower-bound comparison are retained (e = 0, covered); island errors and SE stay unavailable", near(rowX$e, 0, 1e-10) && isTRUE(rowX$lb_cover) && near(rowX$lb_native_diff, 0, 1e-12) && is.na(rowX$se) && is.na(rowX$e_isl1) && is.na(rowX$isl_sd))
recC <- readRDS(file.path(work, "results/smc/p0008", cX, "SMCBVS.rds")); recC$fit$log_Z_r <- NULL
chk(g, "a completed (non-exact) record without islands still has no evidence", { s <- extract_smc(recC); s$ok && !s$evidence_ok && !s$islands_ok && is.na(s$log_Z) })
st <- cp_study("s_exactbranch"); saveRDS(recX, file.path(st, "results/smc/p0008", cX, "SMCBVS.rds"))
r9 <- runq(st); c9 <- cell(r9$H1, 8L, "c100", "1")
chk(g, "H1 keeps the exact-branch fit as an evidence contributor (n_evidence 3 of 3 in its cell)", c9$n_evidence == 3 && c9$n_cases == 3 && r9$acc[case_id == cX & rep == 0L, near(e, 0, 1e-10)])

# ============ G28 N3: full-vector index validation and exact probability validation ============
g <- "G28 PIP index validation (N3)"
chk(g, "full vector with names 4,3,2,1 is reordered to the canonical original-index order", identical(canon_full_vec(c(`4` = 0.1, `3` = 0.2, `2` = 0.3, `1` = 0.4), 4L), setNames(c(0.4, 0.3, 0.2, 0.1), as.character(1:4))))
chk(g, "duplicate names, unknown names and out-of-range values are rejected", is.null(canon_full_vec(c(`1` = 0.1, `1` = 0.2, `2` = 0.3, `3` = 0.4), 4L)) && is.null(canon_full_vec(c(`1` = 0.1, `2` = 0.2, `3` = 0.3, `9` = 0.4), 4L)) &&
    is.null(canon_full_vec(c(`1` = 0.1, `2` = 0.2, `3` = 0.3, `4` = 1.4), 4L)) && is.null(canon_full_vec(c(0.1, NA, 0.3, 0.4), 4L)))
chk(g, "confirmed dropped columns must carry 0: a nonzero entry for a column outside `kept` is rejected, zero accepted", is.null(canon_full_vec(c(0.1, 0.2, 0.3, 0.4), 4L, kept = c(1L, 4L))) && !is.null(canon_full_vec(c(0.1, 0, 0, 0.4), 4L, kept = c(1L, 4L))))
recP <- recA; recP$pip <- rev(recP$pip)                  # names 8..1
smPerm <- extract_smc(recP); smOrig <- extract_smc(recA)
chk(g, "end to end: a permuted adapter vector gives the same canonical PIPs and the same error against the exact reference", identical(smPerm$pip_rb, smOrig$pip_rb) &&
    near(smc_accuracy_row(smPerm, exact_scale(readRDS(file.path(work, "results/exact/p0008/p0008_S1_r001/EXACT.rds")), "c100"), S0_of("p0008_S1_r001"), NULL)$rb_max, acc[case_id == A_ & rep == 0L, rb_max]))
for (bad in list(c(1.8, 0.2, 0.1, 0.05), c(NaN, 0.2, 0.1, 0.05), c(Inf, 0.2, 0.1, 0.05), c(-0.2, 0.2, 0.1, 0.05))) {
  exB <- exE; exB$scales$c100$pip <- setNames(bad, as.character(1:4))
  chk(g, sprintf("exact PIP %s rejected", format(bad[1L])), is.null(exact_scale(exB, "c100")))
}
exB <- exE; exB$scales$c100$log_Z <- NA_real_
chk(g, "exact log Z must be finite", is.null(exact_scale(exB, "c100")))

# ============ G29 residual of finding 6: benchmark identity is the full row; unique main key ============
g <- "G29 duplicate identity (finding 6 residual)"
st <- cp_study("s_dupbench"); dupr <- file.path(st, "rd"); dir.create(dupr); file.copy(list.files(file.path(st, "results"), full.names = TRUE), dupr, recursive = TRUE)
roots6 <- c(file.path(st, "results", c("exact", "smc", "bench")), file.path(dupr, c("exact", "smc", "bench")))
bp <- file.path(dupr, "bench/p0008/p0008_S1_r001_c100/LASSO.rds"); b0 <- readRDS(bp); b1 <- b0; b1$diag_flag <- !b1$diag_flag; saveRDS(b1, bp)
chk(g, "copies that differ only in diag_flag are a conflict (not 'identical copies merged')", expect_err(runq(st, results = roots6), "BENCH"))
b2 <- b0; b2$diag_codes <- "kkt_path"; saveRDS(b2, bp)
chk(g, "copies that differ only in diag_codes are a conflict", expect_err(runq(st, results = roots6), "BENCH"))
saveRDS(b0, bp)
chk(g, "bit-identical benchmark copies are merged", { r <- runq(st, results = roots6); any(r$duplicates$kind == "BENCH") && all(r$duplicates$resolution == "identical copies merged") })
saveRDS(b1, bp); r10 <- runq(st, results = roots6, on_conflict = "first_root")
chk(g, "explicit first_root precedence resolves the flag conflict and records it in duplicates.csv", any(grepl("conflict: first root wins", r10$duplicates$resolution)))
accD <- rbind(res$acc, res$acc[case_id == A_ & rep == 0L])
chk(g, "case_base() asserts a unique main-fit row per case", expect_err(H2_hpm(accD, res$expected, res$ref), "duplicate main-fit rows"))

# ============ G30 residual of finding 10: EXACT completeness at both levels, every scale exact/full ============
g <- "G30 EXACT completeness (finding 10 residual)"
resign <- function(d, xx) { saveRDS(xx, file.path(d, "EXACT.rds")); hh <- file_sha256(file.path(d, "EXACT.rds")); writeLines(paste0(hh, "  EXACT.rds"), file.path(d, "EXACT.sha256")); writeLines(hh, file.path(d, "EXACT.done")) }
variant <- function(nm, f) { d <- mk(nm); xx <- readRDS(file.path(d, "EXACT.rds")); resign(d, f(xx)); resn(d) }
det <- function(v) paste(v$detail, collapse = " | ")
v1 <- variant("c1", function(x) { x$extra$complete <- NULL; x$complete <- FALSE; x })
v2 <- variant("c2", function(x) { x$extra$complete <- NULL; x$complete <- NULL; x })
v3 <- variant("c3", function(x) { x$extra$complete <- NULL; x })
v4 <- variant("c4", function(x) { x$complete <- NULL; x })
v5 <- variant("c5", function(x) { x$scales$c050$status <- "partial"; x$scales$c050$scope <- "restricted_to_scored_models"; x })
v6 <- variant("c6", function(x) { x$models_scored <- x$models_expected - 1; x })
v7 <- variant("c7", function(x) { x$extra$complete <- FALSE; x })
chk(g, "extra$complete NULL with top-level FALSE: refused", !v1$ok && grepl("complete is not TRUE|missing extra fields: .*complete", det(v1)))
chk(g, "completeness unspecified at both levels: refused", !v2$ok && (grepl("complete is not TRUE", det(v2)) || grepl("missing top-level fields", det(v2))))
chk(g, "top-level TRUE but extra missing: refused; extra TRUE but top-level missing: refused", !v3$ok && !v4$ok && grepl("missing extra fields: .*complete|complete is not TRUE", det(v3)) && grepl("missing top-level fields: complete|complete is not TRUE", det(v4)))
chk(g, "a scale marked partial / restricted_to_scored_models under an exact envelope: refused (status and scope reasons)", !v5$ok && grepl("scale c050: status is not exact", det(v5)) && grepl("scale c050: scope is not full", det(v5)))
chk(g, "models_scored differing from models_expected, or extra$complete FALSE: refused", !v6$ok && grepl("models_scored", det(v6)) && !v7$ok && grepl("complete is not TRUE", det(v7)))
# ---- FC4 (final confirmation): counts missing, 0/0, absent requested scale; full-contract fields and input binding ----
f1 <- variant("f1", function(x) { x$models_scored <- NULL; x$models_expected <- NULL; x })
f2 <- variant("f2", function(x) { x$models_scored <- 0; x$models_expected <- 0; x$extra$models_expected <- 0; x })
f3 <- variant("f3", function(x) { x$scales$c050 <- NULL; x })
f4 <- variant("f4", function(x) { x$extra$models_expected <- NULL; x })
f5 <- variant("f5", function(x) { x$K <- x$K - 1; x })
f6 <- variant("f6", function(x) { x$scales$c100$top <- x$scales$c100$top[1:10, ]; x })
f7 <- variant("f7", function(x) { i <- which.max(x$scales$c100$size_logmass); x$scales$c100$size_logmass[i] <- x$scales$c100$size_logmass[i] - 0.3; x })
f8 <- variant("f8", function(x) { x$extra$input_mode <- "unsealed_test"; x })
chk(g, "FC4: both counts missing: refused (missing top-level fields)", !f1$ok && grepl("missing top-level fields: .*models_scored", det(f1)))
chk(g, "FC4: 0/0 counts: refused (expected count not the derived sum, not positive)", !f2$ok && grepl("models_expected = 0 but sum", det(f2)) && grepl("not positive", det(f2)))
chk(g, "FC4: absent requested scale c050: refused", !f3$ok && grepl("scale c050 is absent", det(f3)))
chk(g, "FC4: extra$models_expected missing, wrong K, truncated top list, unnormalised size_logmass, wrong input_mode: each refused", !f4$ok && !f5$ok && grepl("K = ", det(f5)) && !f6$ok && grepl("top has 10 rows", det(f6)) && !f7$ok && grepl("size_logmass", det(f7)) && !f8$ok && grepl("input_mode", det(f8)))
D8i <- readRDS(file.path(work, "inputs/p0008/p0008_S1_r001.rds")); man_f <- file.path(work, "manifests/inputs_manifest_lowp.csv")
inp_ok <- list(X = D8i$X, file_sha256 = file_sha256(file.path(work, "inputs/p0008/p0008_S1_r001.rds")), manifest_sha256 = file_sha256(man_f))
ld <- function(input) load_exact_checked(file.path(mk("bind"), "EXACT.rds"), ds8, 8L, input = input)
chk(g, "input binding: the matching X / input file hash / manifest hash pass", ld(inp_ok)$ok)
Xbad <- D8i$X; Xbad[, 3] <- 1
chk(g, "input binding: another input matrix (retained columns differ), a wrong input hash or a wrong manifest hash is refused", !ld(list(X = Xbad))$ok && grepl("retained_columns differ", ld(list(X = Xbad))$detail) &&
    !ld(modifyList(inp_ok, list(file_sha256 = strrep("0", 64))))$ok && !ld(list(X = D8i$X, manifest_sha256 = strrep("1", 64)))$ok)
chk(g, "a requested scale beyond those in the record (c075) is refused when asked for", { d <- mk("scale3"); r <- load_exact_checked(file.path(d, "EXACT.rds"), ds8, 8L, requested_scales = c("c100", "c050", "c075")); !r$ok && grepl("scale c075 is absent", r$detail) })
chk(g, "the untouched unit is still ready", resn(mk("c0"))$ok)

# ============ G31 residual of finding 11: unknown seed identities are excluded ============
g <- "G31 unknown seeds (finding 11 residual)"
u0 <- extract_smc(recA); u1 <- extract_smc(recA, rep = 1L); u0$method_seed <- NA_real_; u1$method_seed <- NA_real_; u1$log_Z <- u0$log_Z + 1
stU <- stability_row(list(u0, u1))
chk(g, "two completed records with NA method_seed: excluded (n_completed 0, n_unknown_seed 2), no SD or agreement", stU$n_attempted == 2 && stU$n_unknown_seed == 2 && stU$n_completed == 0 && is.na(stU$sd_log_Z) && is.na(stU$hpm_agreement) && stU$n_evidence == 0)
k0 <- extract_smc(recA); k1 <- extract_smc(recA, rep = 1L); k1$method_seed <- k0$method_seed + 1000; k1$log_Z <- k0$log_Z + 1; k2 <- extract_smc(recA, rep = 2L); k2$method_seed <- NA_real_
stK <- stability_row(list(k0, k1, k2))
chk(g, "one unknown among three: the two known distinct seeds are used", stK$n_completed == 2 && stK$n_unknown_seed == 1 && near(stK$sd_log_Z, sqrt(0.5), 1e-9))

# ============ G32 RC3 (final confirmation 2): internally inconsistent EXACT records are refused before the headline tables ============
g <- "G32 EXACT consistency (RC3)"
mut_rev <- function(x) { x$scales$c100$size_logjoint <- rev(x$scales$c100$size_logjoint); x }                       # same log-sum-exp, wrong per-k masses
mut_hpm <- function(x) { z <- x$scales$c100; v <- setdiff(1:8, as.integer(strsplit(z$top$model[1L], ";")[[1L]]))[1L]; z$hpm <- v; z$hpm_size <- 1L; x$scales$c100 <- z; x }   # HPM {v} vs top[1]
mut_lz <- function(x) { z <- x$scales$c100; z$log_Z <- z$hpm_F - 10; z$log_Z_rel_m0 <- z$log_Z - z$log_m0; x$scales$c100 <- z; x }         # log Z below one contained model
muts <- list(reversed_size_logjoint = list(f = mut_rev, pat = "size_logjoint"), hpm_vs_top = list(f = mut_hpm, pat = "hpm"), logZ_below_hpm_F = list(f = mut_lz, pat = "log_Z"))
for (nm in names(muts)) {
  m <- muts[[nm]]; vv <- variant(paste0("rc3_", nm), m$f)
  chk(g, sprintf("%s: refused by the shared validator (reason logged)", nm), !vv$ok && grepl(m$pat, det(vv)), det(vv))
  st <- cp_study(paste0("s_rc3_", nm)); xx <- readRDS(file.path(st, "results/exact/p0008", ds8, "EXACT.rds")); resign(file.path(st, "results/exact/p0008", ds8), m$f(xx))
  r <- runq(st)
  chk(g, sprintf("%s: end to end, the record never reaches the tables (no exact reference for p0008_S1_r001; its cases count as no_exact and give no e, EXACT rows not_run)", nm),
      !any(r$ref[dataset_id == ds8, has_exact]) && !r$exact_diagnostics[dataset_id == ds8, ready] && nchar(r$exact_diagnostics[dataset_id == ds8, detail]) > 0 && cell(r$H1, 8L, "c100", "1")$n_exact_missing == 1 &&
      cell(r$H1, 8L, "c100", "1")$n_evidence == 2 && all(r$sel[dataset_id == ds8 & method_id == "EXACT", status] == "not_run") && all(is.na(r$acc[dataset_id == ds8, e])))
}

# ============ G33 FINAL_CONFIRM3 N2: impossible PIPs on an otherwise real record ============
g <- "G33 EXACT PIP feasibility (FC3 N2)"
mut_pip1 <- function(x) { z <- x$scales$c100; z$pip[] <- 1; z$mpm <- as.integer(names(z$pip)); x$scales$c100 <- z; x }     # every PIP 1, MPM = all variables
vp <- variant("rc_pip1", mut_pip1)
chk(g, "all PIPs 1 and MPM = all variables (impossible for the stored posterior): refused by the shared validator, reason logged", !vp$ok && nchar(det(vp)) > 0, det(vp))
st <- cp_study("s_pip1"); xx <- readRDS(file.path(st, "results/exact/p0008", ds8, "EXACT.rds")); resign(file.path(st, "results/exact/p0008", ds8), mut_pip1(xx))
rp <- runq(st)
chk(g, "end to end: the record never reaches the tables (no exact reference, no e for the dataset, EXACT rows not_run, cell n_evidence 2 of 3)",
    !any(rp$ref[dataset_id == ds8, has_exact]) && !rp$exact_diagnostics[dataset_id == ds8, ready] && nchar(rp$exact_diagnostics[dataset_id == ds8, detail]) > 0 && cell(rp$H1, 8L, "c100", "1")$n_evidence == 2 &&
    all(rp$sel[dataset_id == ds8 & method_id == "EXACT", status] == "not_run") && all(is.na(rp$acc[dataset_id == ds8, e])))
