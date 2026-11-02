# extract_ledger.R -- S-ELS: per-fit local-search ledger extraction from the PROD-H SMCBVS.rds records.
# Usage: Rscript extract_ledger.R CASES_TSV OUT_CSV [WORKER NWORKERS]
#   CASES_TSV : case_id, dataset_id, p, scale_key, record  (the H2 list theory/cases_new.tsv; 2,400 rows)
#   OUT_CSV   : one row per fit. With NWORKERS > 1, OUT_CSV gets the suffix .partK and combine_ledger.py merges.
# Reads only the fit record (rn$fit: hpm, hpm_F, local_search, hpm_before_local, flags, top_store, local_certified)
# and, for scoring only, the truth set S0 from the scoring truth copy. No F(S0) is computed here: F(S0) is merged in
# analyse_ledger.py from the H2 scoring output (F_truth), and cross-checked against the top store.
a <- commandArgs(trailingOnly = TRUE)
L <- utils::read.delim(a[1], stringsAsFactors = FALSE); out <- a[2]
k <- if (length(a) >= 4) as.integer(a[3]) else 1L; N <- if (length(a) >= 4) as.integer(a[4]) else 1L
TRU <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/F_2026-10-19_benchmark_study_n200/Benchmark_Study_20261019/verify/recount/c050/inputs/truth_scoring"
`%|%` <- function(x, y) if (is.null(x) || !length(x)) y else x
sup <- function(x) if (is.null(x) || !length(x)) "" else paste(sort(as.integer(x)), collapse = ";")
num <- function(x) if (is.null(x) || !length(x)) NA_real_ else as.numeric(x)[1]
lgl <- function(x) if (is.null(x) || !length(x)) NA else as.logical(x)[1]
mine <- which((seq_len(nrow(L)) - 1L) %% N == k - 1L)
rows <- vector("list", length(mine))
for (ii in seq_along(mine)) {
  i <- mine[ii]; id <- L$case_id[i]
  rn <- readRDS(L$record[i]); f <- rn$fit
  S0 <- sort(as.integer(readRDS(file.path(TRU, sprintf("p%04d", L$p[i]), paste0(L$dataset_id[i], ".rds")))$active))
  ls <- f$local_search %|% list(); hb <- f$hpm_before_local %|% list(); fl <- f$flags %|% list()
  ts <- f$top_store %|% list(); tv <- num(ts$value); tvv <- as.numeric(ts$value %|% numeric(0))
  hit <- which(vapply(ts$models %|% list(), function(m) length(m) == length(S0) && all(sort(as.integer(m)) == S0), TRUE))
  rows[[ii]] <- data.frame(
    case_id = id, dataset_id = L$dataset_id[i], p = L$p[i], scale_key = L$scale_key[i],
    scenario = as.integer(sub("^p[0-9]{4}_S([0-9])_.*", "\\1", id)), replicate = as.integer(sub(".*_r([0-9]{3})_.*", "\\1", id)),
    native_status = rn$native_status %|% NA_character_, fit_status = f$status %|% NA_character_,
    S0 = sup(S0), s0 = length(S0),
    S_hat = sup(f$hpm), F_hat = num(f$hpm_F), k_hat = length(f$hpm),
    S_before_local = sup(hb$model), F_before_local = num(hb$F),
    S_c = sup(ls$centre), F_c = num(ls$centre_F), S_ret = sup(ls$returned), F_ret = num(ls$returned_F),
    ls_moves = num(ls$moves), ls_termination = ls$termination %|% NA_character_,
    ls_n_evaluated = num(ls$n_evaluated), ls_n_scans = length(ls$scanned_centres %|% list()),
    local_limit = lgl(ls$local_limit), local_certified_raw = lgl(ls$local_certified), local_certified = lgl(f$local_certified),
    E1 = lgl(fl$E1), E2 = lgl(fl$E2), E3 = lgl(fl$E3), flag_local_limit = lgl(fl$local_limit), checks_passed_final = lgl(fl$checks_passed_final),
    escalated = lgl(fl$escalated), ell = num(f$budgets$ell), K = num(f$budgets$K),
    store_n = length(tvv), store_full = lgl(ts$full), store_min_F = if (length(tvv)) min(tvv) else NA_real_,
    store_max_F = if (length(tvv)) max(tvv) else NA_real_,
    S0_in_store = length(hit) > 0, S0_store_F = if (length(hit)) tvv[hit[1]] else NA_real_,
    stringsAsFactors = FALSE)
  if (ii %% 100 == 0) cat(format(Sys.time(), "%T"), "worker", k, ii, "/", length(mine), "\n")
}
D <- do.call(rbind, rows)
utils::write.csv(D, if (N > 1) paste0(out, ".part", k) else out, row.names = FALSE, na = "NA")
cat("WORKER_DONE", k, nrow(D), "\n")
