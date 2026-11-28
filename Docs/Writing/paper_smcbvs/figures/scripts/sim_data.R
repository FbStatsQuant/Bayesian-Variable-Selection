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
#   prec       = TP / |S_hat|, undefined (NA) when S_hat is empty   (precision; averaged over the k non-empty fits)
#   prec1      = 1 - FP / max(|S_hat|, 1)            (empty -> 1; sensitivity table only)
#   rec        = TP / s0                             (recall)
#   F1         = 2 TP / (2 TP + FP + FN)
# A failed fit counts as S_hat = empty (Engineering's counting rule), so prec = NA, rec = 0, exact = 0.
suppressPackageStartupMessages({ library(data.table); library(jsonlite) })

ENG  <- "/home/fb31/Bayesian-Variable-Selection/_local/engineering/"
REP  <- paste0(ENG, "reports/S1S2/")
SRC <- list(
  s1_records   = paste0(REP, "S1_comparison_final_records.tsv"),     # FINAL, reps 1-100, 6 methods
  s1_permethod = paste0(REP, "S1_comparison_final_permethod.tsv"),
  s1_paired    = paste0(REP, "S1_comparison_final_paired.tsv"),
  s1_runtime   = paste0(REP, "final/runtime_S1_smcbvs_asi.tsv"),
  s2_records   = paste0(REP, "S2_comparison_final_records.tsv"),     # FINAL, reps 1-100, 6 methods
  s2_permethod = paste0(REP, "S2_comparison_final_permethod.tsv"),
  s2_paired    = paste0(REP, "S2_comparison_final_paired.tsv"),
  s2_runtime   = paste0(REP, "final/runtime_S2_smcbvs_asi.tsv"),
  s2_records5  = paste0(REP, "S2_comparison_records.tsv"),           # earlier 5-method build (no ASI), cross-check only
  s2_smc_final = paste0(REP, "final/results_S2_smcbvs.tsv"),
  s1_smc_final = paste0(REP, "final/results_S1_smcbvs.tsv"),
  bt2_diag     = paste0(REP, "diagnostics/bt2_diagnostic_per_rep.tsv"),    # LOG-ONLY diagnostic of the S2 SMC-BVS fits, rho > 0
  s1_perfit    = paste0(REP, "final/perfit_precision_recall_S1.tsv"),       # Engineering per-fit TP/FP/FN/precision/recall
  s2_perfit    = paste0(REP, "final/perfit_precision_recall_S2.tsv")        # 6 methods x 12,000
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
  d[, prec := fifelse(n_selected > 0, TP / pmax(n_selected, 1), NA_real_)]
  d[, prec1 := 1 - FP / pmax(n_selected, 1)]
  d[, rec  := TP / s0]
  d[, failed := status != "ok"]
  d[]
}

load_s1 <- function() {
  d <- read_records(SRC$s1_records)[settings_of(SRC$s1_permethod, 1), on = "setting_id"]
  stopifnot(nrow(d) == 6L * 1600L, all(d$in_permethod))
  add_metrics(d)
}

load_s2 <- function(f = SRC$s2_records, n_methods = 6L) {
  d <- read_records(f)[settings_of(SRC$s2_permethod, 2), on = "setting_id"]
  stopifnot(nrow(d) == n_methods * 12000L, all(d$in_permethod))
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

# SMC-BVS run summaries per fit (escalation of the particle number, min ESS/N, E-flags), from the JSON records.
smc_summaries <- function(d, cache_dir, tag) {
  f <- file.path(cache_dir, sprintf("smcsum_%s.tsv", tag))
  if (file.exists(f)) return(fread(f))
  d <- d[method == "smcbvs"]
  files <- ifelse(startsWith(d$file, "/"), d$file, paste0(ENG, d$file))
  L <- lapply(files, function(x) { s <- fromJSON(x, simplifyVector = FALSE)$summary
    data.table(escalated = isTRUE(s$escalated), min_ess_over_N = as.numeric(s$min_ess_over_N), eflag_any = isTRUE(s$eflag_any)) })
  out <- cbind(d[, .(setting_id, rep, method)], rbindlist(L))
  fwrite(out, f, sep = "\t")
  out
}

# ---------------------------------------------------------------------------------------------------------
# Engineering's per-fit precision/recall tables (final/perfit_precision_recall_S{1,2}.tsv). Precision there is
# TP/(TP+FP) with NA for an empty selection; exact is the record's success flag.
read_perfit <- function(f) {
  d <- fread(f, na.strings = c("NA", ""))
  d[, exact := as.character(exact) %in% c("True", "TRUE")]
  d[]
}

# Stop unless our records and the per-fit table agree fit by fit (|S_hat|, TP, FP, FN, exact), and unless the
# per-fit precision equals TP/|S_hat| wherever |S_hat| > 0.
check_perfit <- function(d, pf, tag) {
  m <- merge(d[, .(setting_id, rep, method, n_selected, TP, FP, FN, exact)],
             pf[, .(setting_id, rep, method, n2 = n_selected, TP2 = TP, FP2 = FP, FN2 = FN, ex2 = exact, pr2 = precision)],
             by = c("setting_id", "rep", "method"))
  # Fits killed before writing a selection (BAS, rc=137) carry NA counts in the per-fit table; we count them as
  # empty selections (Engineering's counting rule), so check that and then fill the NAs accordingly.
  na <- is.na(m$n2)
  stopifnot(nrow(m) == nrow(d), all(m$n_selected[na] == 0L), all(!m$exact[na]))
  if (any(na)) m[na, `:=`(n2 = 0L, TP2 = 0L, FP2 = 0L, FN2 = FN)]
  if (any(na)) message(sprintf("  %s: %d fits with NA counts in the per-fit table (killed fits), counted as empty", tag, sum(na)))
  stopifnot(all(m$n_selected == m$n2), all(m$TP == m$TP2), all(m$FP == m$FP2), all(m$FN == m$FN2),
            all(m$exact == m$ex2), all(is.na(m$pr2) == (m$n2 == 0)),
            all(abs(m$pr2 - m$TP / pmax(m$n2, 1))[m$n2 > 0] < 1e-6))   # the table rounds to 6 significant digits
  message(sprintf("verified %s: %d fits agree with Engineering's per-fit table", tag, nrow(m)))
  invisible(nrow(m))
}

# ASI in design S2, from the per-fit table: reps 1..R, where R is the largest r such that every one of the 120
# settings has reps 1..r. R = 100 once the S2 ASI campaign is final; then nothing is marked interim.
load_s2_asi <- function(pf) {
  a <- pf[method == "asi"]
  cnt <- a[, .(r = { x <- sort(unique(rep)); k <- which(x != seq_along(x))[1]; if (is.na(k)) length(x) else k - 1L }), by = setting_id]
  st <- settings_of(SRC$s2_permethod, 2)
  stopifnot(nrow(cnt) == nrow(st))
  R <- min(cnt$r)
  a <- a[rep <= R, .(setting_id, rep, method, status, n_selected, TP, FP, FN, hamming = FP + FN, F1 = as.numeric(F1), exact, file)]
  a <- a[st, on = "setting_id"]
  stopifnot(nrow(a) == nrow(st) * R)
  a <- add_metrics(a)
  setattr(a, "R", R)
  a
}

# Wall time and data checksum per fit from the JSON records (used for ASI in S2, whose per-fit table has no md5).
json_wall_md5 <- function(d, cache_dir, tag) {
  f <- file.path(cache_dir, sprintf("wallmd5_%s.tsv", tag))
  if (file.exists(f)) return(fread(f))
  files <- ifelse(startsWith(d$file, "/"), d$file, paste0(ENG, d$file))
  L <- lapply(files, function(x) { j <- fromJSON(x, simplifyVector = FALSE)
    data.table(wall_sec = as.numeric(j$wall_sec_harness), data_md5 = as.character(j$data_md5)) })
  out <- cbind(d[, .(setting_id, rep, method)], rbindlist(L))
  fwrite(out, f, sep = "\t")
  out
}

# Conditional precision of a group of fits: the mean over its k non-empty fits, reported only when k >= KMIN.
KMIN <- 20L
cprec <- function(x) { k <- sum(!is.na(x)); if (k >= KMIN) mean(x, na.rm = TRUE) else NA_real_ }
fmt_na <- function(fmt, v) ifelse(is.na(v), "--", sprintf(fmt, v))
