# Check 12: the shared strict EXACT validator (exact_contract.R::lowp_validate_exact) on a valid record and on one mutation per
# contract clause (every FC1/FC2/FC4/FC5 probe of FINAL_CONFIRM_sol.md), the CLI resume bound to input_mode / manifest, and the
# dropped-constant-column CLI case (p 20 -> 19 retained).
source("C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/lowp/enum/tests/helpers.R")
source(file.path(LOWP_ENUM_DIR, "exact_contract.R"))
res <- list(); chk <- function(name, ok, note = "") { res[[length(res) + 1]] <<- data.frame(test = name, pass = isTRUE(ok), note = note); cat(sprintf("%-4s %s %s\n", if (isTRUE(ok)) "PASS" else "FAIL", name, note)) }
rs <- "C:/Program Files/R/R-4.4.1/bin/Rscript.exe"; script <- file.path(LOWP_ENUM_DIR, "run_enum_dataset.R")

## ---- a real CLI record (sealed) as the base fixture --------------------------------------------------------------------
root <- file.path(TMP, "fake_study12"); unlink(root, recursive = TRUE); dir.create(file.path(root, "inputs/p0020"), recursive = TRUE); dir.create(file.path(root, "manifests"))
X <- gen_design(20, "block", seed = 3); Yc <- gen_response(X, c(3, 7, 14, 16), c(1.4, -1, 1.8, -1.2), cs = c(c100 = 1, c075 = .75, c050 = .5, c035 = .35, c025 = .25))
Xc <- X; Xc[, 5] <- 1                                    # constant column: dropped by preprocessing (p 20 -> 19 retained)
save_in <- function(id, Xm) { f <- file.path(root, sprintf("inputs/p0020/%s.rds", id)); saveRDS(list(X = Xm, Y = Yc, foldid = rep(1:10, 20), dataset_id = id, p = 20L), f, compress = FALSE); f }
f1 <- save_in("p0020_S3_r007", X); f2 <- save_in("p0020_S3_r008", Xc)
Xn <- gen_design(20, "indep", seed = 41); set.seed(42); Yc_save <- Yc; Yc <- matrix(rnorm(200), 200, 5, dimnames = list(NULL, colnames(Yc_save))); f3 <- save_in("p0020_S3_r009", Xn); Yc <- Yc_save   # pure-noise response
man <- file.path(root, "manifests/inputs_manifest_lowp.csv")
write_man <- function() write.csv(data.frame(dataset_id = c("p0020_S3_r007", "p0020_S3_r008", "p0020_S3_r009"), file = c("a", "b", "c"), file_sha256 = c(lowp_sha256(f1), lowp_sha256(f2), lowp_sha256(f3))), man, row.names = FALSE)
write_man()
out <- file.path(TMP, "fake_out12"); unlink(out, recursive = TRUE)
run <- function(rid, ds, extra = character()) {
  r <- suppressWarnings(system2(rs, c(shQuote(script), "--dataset", ds, "--study", shQuote(root), "--outroot", shQuote(out), "--run-id", rid, "--threads", "2", extra), stdout = TRUE, stderr = TRUE))
  st <- attr(r, "status"); list(status = if (is.null(st)) 0L else st, out = r) }
dest <- function(rid, ds) file.path(out, "results", rid, "p0020", ds)
rdsf <- function(rid, ds) file.path(dest(rid, ds), "EXACT.rds")
consistent <- function(rid, ds) { d <- dest(rid, ds); h <- lowp_sha256(file.path(d, "EXACT.rds")); identical(tolower(substr(readLines(file.path(d, "EXACT.sha256"), 1), 1, 64)), h) && identical(substr(readLines(file.path(d, "EXACT.done"), 1), 1, 64), h) }
rewrite <- function(rid, ds, fun) { f <- rdsf(rid, ds); rec <- fun(readRDS(f)); saveRDS(rec, f, compress = FALSE); h <- lowp_sha256(f); d <- dest(rid, ds)
  writeLines(paste0(h, "  EXACT.rds"), file.path(d, "EXACT.sha256")); writeLines(c(h, "fixture"), file.path(d, "EXACT.done")) }
r <- run("V", "p0020_S3_r007"); base <- readRDS(rdsf("V", "p0020_S3_r007"))
inp <- list(X = X, dataset_id = "p0020_S3_r007", file_sha256 = lowp_sha256(f1), manifest_sha256 = lowp_sha256(man))
v0 <- lowp_validate_exact(base, input = inp)
chk("valid sealed CLI record passes (with and without input)", r$status == 0 && v0$ok && lowp_validate_exact(base)$ok, paste(v0$reasons, collapse = "; "))
chk("signature: (record, requested_scales = c('c100','c050'), input = NULL, mode = c('sealed','unsealed_test'))",
    identical(names(formals(lowp_validate_exact))[1:4], c("record", "requested_scales", "input", "mode")) && identical(eval(formals(lowp_validate_exact)$requested_scales), c("c100", "c050")) && is.null(formals(lowp_validate_exact)$input))
rej <- function(name, fun, pattern = NULL, ..., input = inp, mode = "sealed") {   # a mutation must be rejected, with a reason matching `pattern`
  rec <- fun(base); v <- lowp_validate_exact(rec, input = input, mode = mode, ...)
  chk(name, !v$ok && (is.null(pattern) || any(grepl(pattern, v$reasons))), paste(substr(paste(v$reasons, collapse = " | "), 1, 110))) }
setsc <- function(rec, f) { for (s in names(rec$scales)) rec$scales[[s]] <- f(rec$scales[[s]]); rec }
## top level
rej("wrong schema", function(x) { x$schema <- "lowp_exact_v0"; x }, "schema")
rej("malformed dataset_id", function(x) { x$dataset_id <- "foo"; x }, "dataset_id")
rej("dataset_id differs from the input's", function(x) { x$dataset_id <- "p0020_S3_r009"; x }, "dataset_id differs")
rej("missing top-level models_expected and complete (FC5)", function(x) { x$models_expected <- NULL; x$complete <- NULL; x }, "missing top-level")
rej("top-level complete FALSE (FC5)", function(x) { x$complete <- FALSE; x }, "complete is not TRUE")
rej("extra$complete FALSE", function(x) { x$extra$complete <- FALSE; x }, "complete is not TRUE")
rej("extra$status partial (FC5)", function(x) { x$extra$status <- "partial"; x }, "extra\\$status")
rej("models_scored != models_expected", function(x) { x$models_scored <- x$models_scored - 1; x }, "models_scored")
rej("re-signed zero counts (equal 0/0, FC4)", function(x) { x$models_scored <- 0; x$models_expected <- 0; x$extra$models_expected <- 0; x }, "models_expected")
rej("re-signed p = K = 1 / counts 2 on the unchanged p20 input (FC1)", function(x) { x$p <- 1; x$K <- 1; x$models_scored <- 2; x$models_expected <- 2; x$extra$models_expected <- 2; x$extra$retained_columns <- 1L; x }, "p = 1|retained_columns differ")
rej("K inconsistent with min(p_retained, floor(n/2))", function(x) { x$K <- 5; x }, "K = 5")
rej("models_expected not derived from retained p and K", function(x) { x$models_expected <- x$models_expected - 1; x$models_scored <- x$models_scored - 1; x$extra$models_expected <- x$models_expected; x }, "models_expected")
rej("n differs from the input", function(x) { x$n <- 199; x$K <- 99; x }, "rows")
rej("p differs from the input", function(x) { x$p <- 21; x }, "columns")
rej("retained map differs from the input's non-constant columns", function(x) { x$extra$retained_columns <- c(1L, 3:20); x }, "retained_columns differ|pip")
rej("source_sha256 not a 64-hex", function(x) { x$source_sha256 <- "abc"; x }, "source_sha256")
## input binding and mode
rej("record sealed but unsealed_test requested (FC1)", function(x) x, "input_mode", mode = "unsealed_test")
uns <- function(x) { x$extra$input_mode <- "unsealed_test"; x$extra$manifest_checked <- FALSE; x$extra$manifest_sha256 <- NA_character_; x }
rej("unsealed_test record where sealed is requested (FC1)", uns, "input_mode")
chk("unsealed_test record accepted when unsealed_test is requested", lowp_validate_exact(uns(base), input = list(X = X, dataset_id = "p0020_S3_r007", file_sha256 = lowp_sha256(f1)), mode = "unsealed_test")$ok)
rej("unsealed record claiming manifest_checked", function(x) { x <- uns(x); x$extra$manifest_checked <- TRUE; x }, "claims manifest_checked", mode = "unsealed_test")
rej("sealed record without manifest identity", function(x) { x$extra$manifest_sha256 <- NA_character_; x }, "manifest_sha256")
rej("sealed record with manifest_checked FALSE", function(x) { x$extra$manifest_checked <- FALSE; x }, "manifest_checked")
rej("manifest sha differs from the current manifest", function(x) { x$extra$manifest_sha256 <- strrep("a", 64); x }, "manifest SHA-256 differs")
rej("input file sha differs", function(x) { x$extra$input_file_sha256 <- strrep("b", 64); x }, "input file SHA-256 differs")
## scales
rej("requested scale c050 absent (FC4)", function(x) { x$scales$c050 <- NULL; x }, "scale c050 is absent")
rej("scale status partial", function(x) { x$scales$c100$status <- "partial"; x }, "status is not exact")
rej("scale scope restricted", function(x) { x$scales$c100$scope <- "restricted_to_scored_models"; x }, "scope is not full")
rej("scale scope 'all_models' (old baseline fixture)", function(x) { x$scales$c050$scope <- "all_models"; x }, "scope is not full")
rej("scale status/scope absent (FC5)", function(x) { x$scales$c100$status <- NULL; x$scales$c100$scope <- NULL; x }, "missing fields")
rej("heuristic label missing", function(x) { x$scales$c100$certificate_bound_kind <- NULL; x }, "missing fields")
rej("heuristic label altered", function(x) { x$scales$c050$hpm_eta_kind <- "rigorous"; x }, "labels")
rej("joint-valued size_logmass (FC5)", function(x) { x$scales$c100$size_logmass <- x$scales$c100$size_logjoint; x }, "normalised|log-probabilities")
rej("size_logmass not normalised (shifted by 1e-6)", function(x) { x$scales$c100$size_logmass <- x$scales$c100$size_logmass - 1e-6; x }, "not normalised")
rej("size_logmass of wrong length", function(x) { x$scales$c100$size_logmass <- x$scales$c100$size_logmass[-1]; x }, "length K\\+1")
rej("log_Z not finite", function(x) { x$scales$c050$log_Z <- NaN; x }, "log_Z")
rej("pip of the original length p = 20 when p_retained = 19 (constant column map)", function(x) { x$extra$retained_columns <- x$extra$retained_columns[-1]; x }, "retained")
rej("pip out of [0, 1]", function(x) { x$scales$c100$pip[3] <- 1.5; x }, "within \\[0, 1\\]")
rej("pip names do not match the map", function(x) { names(x$scales$c100$pip)[2] <- "99"; x }, "names\\(pip\\)")
rej("hpm not a subset of the retained columns", function(x) { x$scales$c100$hpm <- c(3L, 99L); x$scales$c100$hpm_size <- 2L; x }, "hpm")
rej("mpm inconsistent with pip > 0.5", function(x) { x$scales$c100$mpm <- integer(0); x }, "mpm")
rej("score re-check reported mismatches", function(x) { x$scales$c100$numerics$recheck_mismatch_F <- 3; x }, "re-check")
rej("top shorter than min(1000, models_expected)", function(x) { x$scales$c100$top <- x$scales$c100$top[1:10, ]; x }, "top has")
rej("negative margin", function(x) { x$scales$c100$margin <- -1; x }, "margin")
## empty model as HPM: coherent control (hpm, hpm_size, top[1] model/mask/size all describe the empty model) and incoherent variants
rn <- run("E", "p0020_S3_r009"); en <- readRDS(rdsf("E", "p0020_S3_r009"))   # genuine CLI record whose HPM is the empty model
veC <- lowp_validate_exact(en, input = list(X = Xn, dataset_id = "p0020_S3_r009", file_sha256 = lowp_sha256(f3), manifest_sha256 = lowp_sha256(man)))
chk("genuine empty-model HPM record (noise data, produced by the CLI) is valid: hpm integer(0), hpm_size 0, top[1] = empty model", rn$status == 0 && veC$ok && length(en$scales$c100$hpm) == 0 && identical(en$scales$c100$top$model[1], "") && en$scales$c100$top$mask[1] == 0, paste(veC$reasons, collapse = " | "))
rej("empty hpm while top[1] is still the non-empty model (hpm only edited)", function(x) { x$scales$c100$hpm <- integer(0); x$scales$c100$hpm_size <- 0L; x }, "hpm differs")
## Sol RC3 mutations (FINAL_CONFIRM2_sol.md)
rej("RC3-1: size_logjoint reversed (per-k identity broken, both log-sum-exp unchanged)", function(x) { x$scales$c100$size_logjoint <- rev(x$scales$c100$size_logjoint); x }, "size_logjoint\\[k\\]")
rej("RC3-2: HPM set to {1} while top[1] is {3}", function(x) { x$scales$c100$hpm <- 1L; x$scales$c100$hpm_size <- 1L; x }, "hpm differs from the support")
rej("RC3-3: log_Z = hpm_F - 10 (size_logjoint and log_Z_rel_m0 updated consistently)", function(x) { z <- x$scales$c100; z$log_Z <- z$hpm_F - 10; z$size_logjoint <- z$size_logmass + z$log_Z; z$log_Z_rel_m0 <- z$log_Z - z$log_m0; x$scales$c100 <- z; x }, "below the mass of one contained model")
## Sol FINAL_CONFIRM3 N2: impossible PIPs on a genuine p20 record
chk("genuine p20 record (control) passes the PIP moment and listed-mass feasibility checks", lowp_validate_exact(base, input = inp)$ok && abs(sum(base$scales$c100$pip) - sum((seq_along(base$scales$c100$size_logmass) - 1) * exp(base$scales$c100$size_logmass))) < 1e-10)
rej("N2: all PIPs = 1 and MPM = all retained columns", function(x) { for (s in names(x$scales)) { x$scales[[s]]$pip[] <- 1; x$scales[[s]]$mpm <- as.integer(x$extra$retained_columns) }; x }, "sum\\(PIP\\)|PIP_j above")
rej("N2: PIPs permuted between a signal and a null column (sum unchanged, mpm kept consistent)", function(x) { z <- x$scales$c100; p <- z$pip; i <- which.max(p); j <- which.min(p); p[c(i, j)] <- p[c(j, i)]; z$pip <- p; z$mpm <- as.integer(x$extra$retained_columns[p > 0.5]); x$scales$c100 <- z; x }, "PIP_j (above|below)")
rej("N2: a signal PIP set to 0 (below the share of the listed top models)", function(x) { z <- x$scales$c100; i <- which.max(z$pip); z$pip[i] <- 0; z$mpm <- as.integer(x$extra$retained_columns[z$pip > 0.5]); x$scales$c100 <- z; x }, "PIP_j below|sum\\(PIP\\)")
rej("N2: PIPs scaled by 0.9 (sum(PIP) != sum_k k exp(size_logmass[k]))", function(x) { z <- x$scales$c050; z$pip <- z$pip * 0.9; z$mpm <- as.integer(x$extra$retained_columns[z$pip > 0.5]); x$scales$c050 <- z; x }, "sum\\(PIP\\)|PIP_j below")
## further cross-field clauses
rej("size_logmass/size_logjoint with different -Inf patterns", function(x) { x$scales$c100$size_logjoint[2] <- -Inf; x }, "-Inf patterns|log-sum-exp differs")
rej("log_Z_rel_m0 != log_Z - log_m0", function(x) { x$scales$c050$log_Z_rel_m0 <- x$scales$c050$log_Z_rel_m0 + 1e-3; x }, "log_Z_rel_m0")
rej("hpm_size differs from top$size[1]", function(x) { x$scales$c100$top$size[1] <- 9L; x }, "top\\$size")
rej("top$mask of row 1 differs from the model text", function(x) { x$scales$c100$top$mask[1] <- x$scales$c100$top$mask[1] + 1; x }, "mask")
rej("duplicated model in top", function(x) { t <- x$scales$c100$top; t[3, c("model", "mask", "size")] <- t[2, c("model", "mask", "size")]; x$scales$c100$top <- t; x }, "duplicated")
rej("top not sorted by F (rows 2 and 3 swapped)", function(x) { t <- x$scales$c100$top; r <- t[2, ]; t[2, ] <- t[3, ]; t[3, ] <- r; x$scales$c100$top <- t; x }, "order")
rej("second_F != top$F[2]", function(x) { x$scales$c050$second_F <- x$scales$c050$second_F + 1e-6; x }, "second_F")
rej("log_Z below the total mass of the listed top models (log_Z = hpm_F, joint updated)", function(x) { z <- x$scales$c100; z$log_Z <- z$hpm_F; z$size_logjoint <- z$size_logmass + z$log_Z; z$log_Z_rel_m0 <- z$log_Z - z$log_m0; x$scales$c100 <- z; x }, "listed top|contained model")
chk("tie order: equal F, smaller size first then lexicographic is accepted; the reverse is rejected", { x <- base; t <- x$scales$c100$top; t$F[2:3] <- t$F[2]; t$size[2:3] <- 1L; t$model[2:3] <- c("3", "7"); t$mask[2:3] <- c(4, 64); t <- t[order(-t$F, t$size), ]; x$scales$c100$top <- t
  ok1 <- !any(grepl("section I.6", lowp_validate_exact(x, input = inp)$reasons)); t2 <- x$scales$c100$top; t2[2:3, ] <- t2[3:2, ]; x$scales$c100$top <- t2; ok1 && any(grepl("section I.6", lowp_validate_exact(x, input = inp)$reasons)) })
chk("a superset of the requested scales is accepted unless exact_scale_set = TRUE", { rec <- base; rec$scales$c075 <- rec$scales$c100; lowp_validate_exact(rec, input = inp)$ok && !lowp_validate_exact(rec, input = inp, exact_scale_set = TRUE)$ok })
chk("one-scale request on a two-scale record is accepted by the validator (consumer view)", lowp_validate_exact(base, requested_scales = "c100", input = inp)$ok)

## ---- CLI: resume bound to input_mode / manifest sha (FC1) -----------------------------------------------------------------
file.remove(man)
r <- run("U", "p0020_S3_r007", "--unsealed-test-input"); u <- readRDS(rdsf("U", "p0020_S3_r007"))
chk("CLI unsealed_test run recorded as such", r$status == 0 && identical(u$extra$input_mode, "unsealed_test") && lowp_validate_exact(u, mode = "unsealed_test")$ok)
write_man()
r <- run("U", "p0020_S3_r007")
u2 <- readRDS(rdsf("U", "p0020_S3_r007"))
chk("FC1: after a manifest is added the unsealed_test record is NOT reused; recomputed as sealed", r$status == 0 && any(grepl("input_mode", r$out)) && any(grepl("^OK ", r$out)) && identical(u2$extra$input_mode, "sealed") && identical(u2$extra$manifest_sha256, lowp_sha256(man)) && consistent("U", "p0020_S3_r007"))
r <- run("U", "p0020_S3_r007", "--unsealed-test-input")
chk("  --unsealed-test-input with a manifest present stays a sealed run (verified skip)", r$status == 0 && any(grepl("verified", r$out)) && identical(readRDS(rdsf("U", "p0020_S3_r007"))$extra$input_mode, "sealed"))
## manifest content changes (new manifest sha) -> recompute
m2 <- read.csv(man, colClasses = "character"); m2$file <- c("a2", "b2", "c2"); write.csv(m2, man, row.names = FALSE)
r <- run("U", "p0020_S3_r007")
chk("FC1: a changed manifest (new SHA-256, same file hash) -> recomputed with the new manifest identity", r$status == 0 && any(grepl("manifest SHA-256 differs", r$out)) && identical(readRDS(rdsf("U", "p0020_S3_r007"))$extra$manifest_sha256, lowp_sha256(man)))
## re-signed wrong-dimension record on unchanged input
rewrite("U", "p0020_S3_r007", function(x) { x$p <- 1; x$K <- 1; x$models_scored <- 2; x$models_expected <- 2; x$extra$models_expected <- 2; x$extra$retained_columns <- 1L; x })
r <- run("U", "p0020_S3_r007")
chk("FC1: re-signed p = K = 1 / counts 2 record on the unchanged p20 input -> recomputed", r$status == 0 && any(grepl("^OK ", r$out)) && readRDS(rdsf("U", "p0020_S3_r007"))$K == 20)
rewrite("U", "p0020_S3_r007", function(x) { x$complete <- FALSE; x })
r <- run("U", "p0020_S3_r007"); chk("FC1: a record whose top-level complete is FALSE (extra TRUE) -> recomputed", r$status == 0 && any(grepl("^OK ", r$out)) && isTRUE(readRDS(rdsf("U", "p0020_S3_r007"))$complete))
rewrite("U", "p0020_S3_r007", function(x) { x$models_expected <- NULL; x$complete <- NULL; x })
r <- run("U", "p0020_S3_r007"); chk("FC1/FC5: a record without the top-level completeness fields -> recomputed", r$status == 0 && any(grepl("^OK ", r$out)) && !is.null(readRDS(rdsf("U", "p0020_S3_r007"))$models_expected))

## ---- FC2: constant column, p 20 -> 19 retained -----------------------------------------------------------------------------
r <- run("C", "p0020_S3_r008"); rc <- readRDS(rdsf("C", "p0020_S3_r008"))
chk("FC2: CLI completes on a p = 20 input with one constant column (19 retained), writes .done", r$status == 0 && file.exists(file.path(dest("C", "p0020_S3_r008"), "EXACT.done")) && consistent("C", "p0020_S3_r008"), paste(tail(r$out, 1)))
chk("  record: p = 20 (original), K = 19, retained map of 19 columns without column 5, models 2^19 = 524288 scored = expected (top level and extra)",
    rc$p == 20 && rc$K == 19 && length(rc$extra$retained_columns) == 19 && !(5L %in% rc$extra$retained_columns) && rc$models_scored == 524288 && rc$models_expected == 524288 && rc$extra$models_expected == 524288 && isTRUE(rc$complete))
chk("  names(pip) = the 19 retained columns, size_logmass of length 20, normalised; validator (with the input) accepts it",
    identical(names(rc$scales$c100$pip), as.character(rc$extra$retained_columns)) && length(rc$scales$c100$size_logmass) == 20 &&
    lowp_validate_exact(rc, input = list(X = Xc, dataset_id = "p0020_S3_r008", file_sha256 = lowp_sha256(f2), manifest_sha256 = lowp_sha256(man)))$ok)
r <- run("C", "p0020_S3_r008"); chk("  rerun: verified skip (the post-commit check and the resume agree on retained-p coverage)", r$status == 0 && any(grepl("verified", r$out)) && !any(grepl("^OK ", r$out)))
lowp_load(); ap <- attr(lowp_exact(Xc, list(c100 = Yc[, "c100"], c050 = Yc[, "c050"]), threads = 2), "run")
chk("  API agrees with the CLI: 524288 models, status exact, complete", ap$models_scored == 524288 && ap$models_expected == 524288 && identical(ap$status, "exact"))
chk("  same record with the original-p coverage (2^20 - 1) is rejected by the validator", { x <- rc; x$models_expected <- sum(choose(20, 0:19)); x$models_scored <- x$models_expected; x$extra$models_expected <- x$models_expected; !lowp_validate_exact(x)$ok })
R <- do.call(rbind, res); cat(sprintf("\n%d of %d checks passed\n", sum(R$pass), nrow(R)))
