# test_p0a_tolerance.R -- local test of P0a as the cross-platform generator check (B1, HQ decision D44; code/lowp/R/lowp_verify_nots.R).
#   Rscript tests/test_p0a_tolerance.R WORKDIR        (seals a study into WORKDIR/study once, about 2-4 min; then 7 cases of about 1 min each)
# The NOTS situation (R 4.5.2/Linux regenerates the laptop seal up to 1-3 ulp) is emulated by wrapping generate_dataset IN THIS TEST ONLY:
# production code has no hook. Expected:
#   A  unmodified regeneration                                         -> PASS (0)
#   B  deterministic 1-3 ulp noise on every regenerated float array    -> PASS (0), maxima > 0 and far below the bound, most arrays not bit-identical
#   C  one eps value of one dataset perturbed by 1e-9 (relative)       -> MISMATCH (1), "truth eps (tolerance"
#   D  one X value of a pilot dataset perturbed by 1e-9                -> MISMATCH (1), "pilot X (tolerance"
#   E  two foldid entries swapped in the regeneration                  -> MISMATCH (1), "foldid (exact)"
#   F  a sealed truth file altered (study copy)                        -> MISMATCH (1), "truth file_sha256 (exact)"
#   G  a truth file missing (study copy)                               -> INCOMPLETE (3)
a <- commandArgs(TRUE); if (length(a) != 1L) stop("usage: test_p0a_tolerance.R WORKDIR")
W <- a[1L]; dir.create(W, recursive = TRUE, showWarnings = FALSE); W <- normalizePath(W, winslash = "/")
here <- dirname(normalizePath(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1L]), winslash = "/"))
RDIR <- normalizePath(file.path(here, "..", "..", "R"), winslash = "/")
source(file.path(RDIR, "lowp_generate.R"))
ST <- file.path(W, "study")
if (!file.exists(file.path(ST, "SEALED_OK"))) {
  unlink(ST, recursive = TRUE)
  rs <- file.path(R.home("bin"), if (.Platform$OS.type == "windows") "Rscript.exe" else "Rscript")
  rc <- system2(rs, c("--vanilla", shQuote(file.path(RDIR, "lowp_seal.R")), shQuote(ST)), stdout = file.path(W, "seal.log"), stderr = file.path(W, "seal.log"))
  if (!identical(as.integer(rc), 0L)) stop("sealing failed, see ", file.path(W, "seal.log"))
  writeLines(format(Sys.time()), file.path(ST, "SEALED_OK"))
}
ORIG <- generate_dataset
MODE <- "none"
ulp <- function(x) { k <- (seq_along(x) %% 7L) - 3L; x * (1 + k * 2^-52) }            # deterministic, cycles -3..+3 ulp (R7D-4), no RNG use
generate_dataset <- function(p, scenario, replicate, kind = c("prod", "dev")) {
  d <- ORIG(p, scenario, replicate, kind)
  if (MODE == "ulp") { dm <- dim(d$inputs$X); d$inputs$X <- ulp(d$inputs$X); dim(d$inputs$X) <- dm
                       d$inputs$Y[] <- ulp(d$inputs$Y); d$truth$signal <- ulp(d$truth$signal); d$truth$eps <- ulp(d$truth$eps) }
  if (MODE == "eps1e9" && d$truth$dataset_id == "p0020_S3_r017") d$truth$eps[5] <- d$truth$eps[5] * (1 + 1e-9)
  if (MODE == "x1e9" && d$inputs$dataset_id == "p0030_S4_r050") d$inputs$X[7, 3] <- d$inputs$X[7, 3] * (1 + 1e-9)
  if (MODE == "xnames" && d$inputs$dataset_id == "p0030_S4_r050") colnames(d$inputs$X) <- paste0("changed_", seq_len(ncol(d$inputs$X)))
  if (MODE == "fold" &&d$inputs$dataset_id == "p0020_S2_r002") { f <- d$inputs$foldid; i <- which(f != f[1L])[1L]; f[c(1L, i)] <- f[c(i, 1L)]; d$inputs$foldid <- f }
  d
}
source(file.path(RDIR, "lowp_verify_nots.R"))
run <- function(mode, study = ST, tag = mode) {
  MODE <<- mode
  out <- file.path(W, paste0("out_", tag)); unlink(out, recursive = TRUE)
  r <- tryCatch(suppressMessages(utils::capture.output(res <- lowp_verify_nots(file.path(study, "manifests"), out, file.path(study, "dev", "manifests"), study))),
                error = function(e) NULL)
  MODE <<- "none"; res
}
rows <- list(); allok <- TRUE
chk <- function(name, ok, detail = "") { allok <<- allok && isTRUE(ok); rows[[length(rows) + 1L]] <<- sprintf("| %s | %s | %s |", name, if (isTRUE(ok)) "ok" else "**WRONG**", detail) }
has <- function(res, pat) any(grepl(pat, res$mismatches$array, fixed = TRUE))

A <- run("none"); chk("A unmodified regeneration -> PASS (0)", A$code == 0L, sprintf("code %d; maxima %s", A$code, paste(signif(A$maxima$max_scaled_delta, 3), collapse = " ")))
B <- run("ulp"); mxB <- max(B$maxima$max_scaled_delta)
chk("B 1-3 ulp noise on X, Y, signal, eps (the NOTS situation) -> PASS (0), observed maximum > 0 and < 1e-14", B$code == 0L && mxB > 0 && mxB < 1e-14, sprintf("code %d; max scaled delta %.3g", B$code, mxB))
chk("B the report states the cross-platform check and the bound", any(grepl("Not an identity check", readLines(file.path(W, "out_ulp", "NOTS_REGEN_REPORT.md")))) && file.exists(file.path(W, "out_ulp", "NOTS_REGEN_MAXIMA.csv")))
C <- run("eps1e9"); chk("C one eps value perturbed by 1e-9 -> MISMATCH (1) on 'truth eps (tolerance'", C$code == 1L && has(C, "truth eps (tolerance") && nrow(C$mismatches) == 1L, sprintf("code %d; %d failed", C$code, nrow(C$mismatches)))
D <- run("x1e9"); chk("D one pilot X value perturbed by 1e-9 -> MISMATCH (1) on 'pilot X (tolerance'", D$code == 1L && has(D, "pilot X (tolerance"), sprintf("code %d", D$code))
N <- run("xnames"); chk("N regenerated X column names changed only (values identical) -> MISMATCH (1) on 'pilot X (tolerance' with names/dimnames (R7D-1)", N$code == 1L && has(N, "pilot X (tolerance") && any(grepl("names / dimnames", N$mismatches$nots)), sprintf("code %d", N$code))
E <- run("fold"); chk("E two foldid entries swapped -> MISMATCH (1) on 'foldid (exact)'", E$code == 1L && has(E, "foldid (exact)"), sprintf("code %d", E$code))
# study copies for F and G (the canonical seal is never touched)
cp <- function(tag) { d <- file.path(W, paste0("study_", tag)); unlink(d, recursive = TRUE); dir.create(d)
  for (x in list.files(ST, full.names = TRUE, all.files = FALSE)) file.copy(x, d, recursive = TRUE)
  Sys.chmod(list.files(d, recursive = TRUE, full.names = TRUE), "0644"); d }
SF <- cp("F"); tf <- file.path(SF, "truth", "p0030", "p0030_S5_r060.rds"); z <- readRDS(tf); z$eps[1] <- z$eps[1] + 1e-3; saveRDS(z, tf, version = 3, compress = FALSE)
F <- run("none", SF, "F"); chk("F a sealed truth file altered -> MISMATCH (1) on 'truth file_sha256 (exact)'", F$code == 1L && has(F, "truth file_sha256 (exact)"), sprintf("code %d", F$code))
SG <- cp("G"); file.remove(file.path(SG, "dev", "truth", "p0020", "dev_p0020_S1_r001.rds"))
G <- run("none", SG, "G"); chk("G a truth file missing -> INCOMPLETE (3)", G$code == 3L && any(grepl("truth file missing", G$incomplete)), sprintf("code %d", G$code))
unlink(c(SF, SG), recursive = TRUE)
L <- c("# P0a cross-platform generator check (B1, D44): local test", "", "| Case | Result | Detail |", "|---|---|---|", unlist(rows), "",
       sprintf("test_p0a_tolerance: %d passed, %d failed", sum(grepl("\\| ok \\|", unlist(rows))), sum(grepl("WRONG", unlist(rows)))))
writeLines(L, file.path(W, "P0A_TOLERANCE_TESTS.md")); cat(paste(L, collapse = "\n"), "\n")
quit(save = "no", status = if (allok) 0L else 1L)
