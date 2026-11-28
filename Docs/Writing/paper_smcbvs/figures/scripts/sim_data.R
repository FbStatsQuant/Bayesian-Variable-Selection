# sim_data.R -- data layer for the S1/S2 figures and tables of Sections 2 and 4.
# Owner: Writing Department, Task Lead 2.  Sourced by build_sim_outputs.R; never run on its own.
#
# Reads ONLY the Engineering per-fit record tables on Owls (read-only) and, for wall times, the per-fit
# JSON records those tables point to. Nothing here is copied into the repository: the build writes
# only figures (pdf), LaTeX tables and a provenance file (SOURCES.md) with sha256 sums of every input.
#
# Per-fit metrics (one row per method x setting x replicate):
#   exact      = 1{S_hat == S0}                      (from the record; MPM for the Bayesian methods)
#   FP, FN, TP = |S_hat \ S0|, |S0 \ S_hat|, |S_hat ∩ S0|
#   hamming    = FP + FN
#   prec       = 1 - FP / max(|S_hat|, 1)            (precision; an empty selection has precision 1)
#   rec        = TP / s0                             (recall)
#   F1         = 2 TP / (2 TP + FP + FN)
# A failed fit counts as S_hat = empty (Engineering's counting rule), so prec = 1, rec = 0, exact = 0.
suppressPackageStartupMessages({ library(data.table); library(jsonlite) })

ENG  <- "/home/fb31/Bayesian-Variable-Selection/_local/engineering/"
REP  <- paste0(ENG, "reports/S1S2/")
SRC <- list(
  s1_records   = paste0(REP, "S1_comparison_final_records.tsv"),     # FINAL, reps 1-100, 6 methods
  s1_permethod = paste0(REP, "S1_comparison_final_permethod.tsv"),
  s1_paired    = paste0(REP, "S1_comparison_final_paired.tsv"),
  s1_runtime   = paste0(REP, "final/runtime_S1_smcbvs_asi.tsv"),
  s2_records   = paste0(REP, "S2_comparison_records.tsv"),           # 5 methods final, reps 1-100 (no ASI)
  s2_permethod = paste0(REP, "S2_comparison_permethod.tsv"),
  s2_asi_records   = paste0(REP, "hq_s2asi_b1/S2_comparison_asi_b1_records.tsv"),   # INTERIM, reps 1-25, 6 methods
  s2_asi_permethod = paste0(REP, "hq_s2asi_b1/S2_comparison_asi_b1_permethod.tsv"),
  s2_asi_paired    = paste0(REP, "hq_s2asi_b1/S2_comparison_asi_b1_paired.tsv"),
  s2_smc_final = paste0(REP, "final/results_S2_smcbvs.tsv"),
  s1_smc_final = paste0(REP, "final/results_S1_smcbvs.tsv"),
  bt2_diag     = paste0(REP, "diagnostics/bt2_diagnostic_per_rep.tsv")     # LOG-ONLY diagnostic of the S2 SMC-BVS fits, rho > 0
)

METHODS <- c("smcbvs", "asi", "bas_mc3", "susie", "scad", "lasso_cv")
LABELS  <- c(smcbvs = "SMC-BVS", asi = "ASI", bas_mc3 = "BAS (MC3)", susie = "SuSiE",
             scad = "SCAD", lasso_cv = "Lasso (CV)")

# The record tables hold one row per fit; a failed BAS fit carries its error message, with embedded
# newlines, in the status field. Rejoin continuation lines before parsing.
read_records <- function(f) {
  L <- readLines(f)
  start <- grepl("^(setting_id|S[12]_[0-9]+)\t", L)
  J <- vapply(split(L, cumsum(start)), paste, "", collapse = " ")
  d <- fread(text = J, sep = "\t", quote = "")
  stopifnot(ncol(d) == 19L, all(d$status == "ok" | grepl("^failed", d$status)))
  d
}

settings_of <- function(pm_file, suite) {
  pm <- fread(pm_file)
  if (suite == 1) unique(pm[scope == "setting", .(setting_id = group, n, p, snr, s0 = 10L)])
  else unique(pm[scope == "setting", .(setting_id = group, n, p, s0, rho, nu, beta_type)])
}

add_metrics <- function(d) {
  d[, exact := as.logical(exact)]
  d[, prec := 1 - FP / pmax(n_selected, 1)]
  d[, rec  := TP / s0]
  d[, failed := status != "ok"]
  d[]
}

load_s1 <- function() {
  d <- read_records(SRC$s1_records)[settings_of(SRC$s1_permethod, 1), on = "setting_id"]
  stopifnot(nrow(d) == 6L * 1600L, all(d$in_permethod))
  add_metrics(d)
}

load_s2 <- function(which = c("final5", "asi25")) {
  which <- match.arg(which)
  f  <- if (which == "final5") SRC$s2_records else SRC$s2_asi_records
  pm <- if (which == "final5") SRC$s2_permethod else SRC$s2_asi_permethod
  d <- read_records(f)[settings_of(pm, 2), on = "setting_id"]
  if (which == "final5") stopifnot(nrow(d) == 5L * 12000L) else stopifnot(nrow(d) == 6L * 3000L)
  stopifnot(all(d$in_permethod))
  add_metrics(d)
}

# Wall time per fit (seconds): wall_sec_harness of each JSON record (harness wall time on one core,
# data generation and diagnostics included; Engineering's definition in final/runtime_S1_smcbvs_asi.md).
# Cached in the private build folder, keyed by the sha256 of the record table it came from.
wall_times <- function(d, cache_dir, tag) {
  f <- file.path(cache_dir, sprintf("wall_%s.tsv", tag))
  if (file.exists(f)) return(fread(f))
  files <- ifelse(startsWith(d$file, "/"), d$file, paste0(ENG, d$file))
  w <- vapply(files, function(x) {
    r <- tryCatch(fromJSON(x, simplifyVector = FALSE)$wall_sec_harness, error = function(e) NULL)
    if (is.null(r)) NA_real_ else as.numeric(r)
  }, 0)
  out <- data.table(setting_id = d$setting_id, rep = d$rep, method = d$method, wall_sec = unname(w))
  fwrite(out, f, sep = "\t")
  out
}

wilson <- function(x, n, z = 1.959964) {
  ph <- x / n; den <- 1 + z^2 / n
  ctr <- (ph + z^2 / (2 * n)) / den
  hw  <- z * sqrt(ph * (1 - ph) / n + z^2 / (4 * n^2)) / den
  list(lo = pmax(0, ctr - hw), hi = pmin(1, ctr + hw))
}

sha256 <- function(f) sub(" .*", "", system2("sha256sum", shQuote(f), stdout = TRUE))

# Note on the verification against Engineering's tables: build_sim_outputs.R stops unless the recomputed
# per-setting counts and means equal the *_permethod.tsv values (see SOURCES.md, "Checks").
