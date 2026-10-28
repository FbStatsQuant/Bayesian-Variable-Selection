# Benchmarks/Exact_reference/compare_to_exact.R — join a run's fits with the exact posterior references.
#   Rscript --vanilla Exact_reference/compare_to_exact.R RUN_DIR [EXACT_DIR] [METHOD ...]     (from the Benchmarks root)
# For every method folder found in RUN_DIR (any of the six; whichever are present) and every case with a
# fit_summary.rds, writes under RUN_DIR/exact_comparison/:
#   supports_vs_exact.csv   one row per (method, case, rule): the support, agreement with the exact MPM {PIP>0.5} and
#                           the exact HPM, exact recovery, FP / FN, and whether the exact MPM / HPM recover the truth
#   pip_vs_exact.csv        PIP methods only: MAE, max AE, RMSE, MAE on signals / proxies / nulls, MPM agreement
#   parni_repeats_vs_exact.csv  PARNI: the same per repeat for plain and RB PIPs, plus the SD across repeats
#   exact_ceilings.csv      per scenario: exact MPM / HPM recovery rates (the Bayes-decision ceilings)
#   summary_vs_exact.csv    per scenario x method x rule: agreement rates, median PIP errors
#   SUMMARY_EXACT.md
# Safe on partial runs: cases without an exact file or a fit are listed as missing.
args <- commandArgs(TRUE)
if (length(args) < 1L) stop("Usage: compare_to_exact.R RUN_DIR [EXACT_DIR] [METHOD ...]")
root <- normalizePath(".", mustWork = TRUE)
source("shared/design.R"); source("shared/io.R")
run_dir <- args[1]
exact_dir <- if (length(args) >= 2L && dir.exists(args[2])) args[2] else file.path(root, "Exact_reference", "output", "exact")
methods <- if (length(args) >= 3L) args[-(1:2)] else { d <- list.dirs(run_dir, recursive = FALSE, full.names = FALSE); d[!d %in% c("logs", "aggregation", "exact_comparison")] }
out <- file.path(run_dir, "exact_comparison"); dir.create(out, recursive = TRUE, showWarnings = FALSE)
roots <- data_roots(root)
set_str <- function(s) paste(sort(as.integer(s)), collapse = ",")
groups_of <- function(truth, p = 30L) { block <- ceiling(seq_len(p) / 5); sb <- unique(block[truth]); nulls <- setdiff(seq_len(p), truth)
  list(signals = truth, proxies = nulls[block[nulls] %in% sb], nulls = nulls[!(block[nulls] %in% sb)]) }
pip_err <- function(est, ex, g) { e <- est - ex; gm <- function(i) if (length(i)) mean(abs(e[i])) else NA_real_
  c(mae = mean(abs(e)), maxae = max(abs(e)), rmse = sqrt(mean(e^2)), mae_signals = gm(g$signals), mae_proxies = gm(g$proxies), mae_nulls = gm(g$nulls)) }

tab <- task_table(); exact_cache <- list(); missing <- list(); sup_rows <- list(); pip_rows <- list(); rep_rows <- list(); ceil_rows <- list()
load_exact <- function(id) { f <- file.path(exact_dir, paste0(id, ".rds")); if (!file.exists(f)) return(NULL); readRDS(f) }
for (i in seq_len(nrow(tab))) {
  id <- tab$case_id[i]; ex <- load_exact(id)
  if (is.null(ex)) next
  ceil_rows[[id]] <- data.frame(case_id = id, scenario = tab$scenario[i], log_Z = ex$log_Z, exact_mpm = set_str(ex$mpm), exact_hpm = set_str(ex$map_variables),
                                mpm_recovers_truth = ex$mpm_recovers_truth, hpm_recovers_truth = ex$hpm_recovers_truth, seconds = ex$seconds, stringsAsFactors = FALSE)
}
for (m in methods) for (i in seq_len(nrow(tab))) {
  id <- tab$case_id[i]; s <- tab$scenario[i]; r <- tab$replicate[i]
  fs <- file.path(run_dir, m, id, "fit_summary.rds")
  if (!file.exists(fs)) next
  ex <- load_exact(id)
  if (is.null(ex)) { missing[[length(missing) + 1L]] <- data.frame(method = m, case_id = id, problem = "no exact reference"); next }
  f <- readRDS(fs); truth <- ex$truth; g <- groups_of(truth); p <- length(ex$pip)
  supports <- c(list(primary = f$selected), f$sensitivity)
  for (nm in names(supports)) {
    sel <- which(supports[[nm]])
    sup_rows[[length(sup_rows) + 1L]] <- data.frame(method = m, scenario = s, replicate = r, case_id = id, rule = nm, primary_rule = if (is.null(f$primary_rule)) NA else f$primary_rule,
      selected = set_str(sel), n_selected = length(sel), fp = length(setdiff(sel, truth)), fn = length(setdiff(truth, sel)),
      exact_recovery = setequal(sel, truth), agrees_exact_mpm = setequal(sel, ex$mpm), agrees_exact_hpm = setequal(sel, ex$map_variables),
      exact_mpm_recovers_truth = ex$mpm_recovers_truth, exact_hpm_recovers_truth = ex$hpm_recovers_truth, stringsAsFactors = FALSE)
  }
  if (!is.null(f$pip)) {
    e <- pip_err(as.numeric(f$pip), ex$pip, g)
    pip_rows[[length(pip_rows) + 1L]] <- data.frame(method = m, scenario = s, replicate = r, case_id = id, estimator = "primary_pip", t(e),
      mpm_agrees_exact = setequal(which(f$pip > 0.5), ex$mpm), stringsAsFactors = FALSE)
  }
  if (m == "PARNI") {
    ff <- file.path(run_dir, m, id, "fit.rds"); if (!file.exists(ff)) next
    full <- readRDS(ff); plain <- full$diagnostics$pip_plain; rb <- full$diagnostics$pip_rb
    for (k in seq_len(nrow(plain))) for (est in c("plain", "rb")) {
      v <- if (est == "plain") plain[k, ] else rb[k, ]; e <- pip_err(v, ex$pip, g)
      rep_rows[[length(rep_rows) + 1L]] <- data.frame(method = m, scenario = s, replicate = r, case_id = id, repeat_index = k, estimator = est, t(e),
        mpm_agrees_exact = setequal(which(v > 0.5), ex$mpm), stringsAsFactors = FALSE)
    }
    if (nrow(plain) > 1L) {
      e_pool <- pip_err(colMeans(plain), ex$pip, g); e_poolrb <- pip_err(colMeans(rb), ex$pip, g)
      pip_rows[[length(pip_rows) + 1L]] <- data.frame(method = m, scenario = s, replicate = r, case_id = id, estimator = "pooled_plain", t(e_pool), mpm_agrees_exact = setequal(which(colMeans(plain) > 0.5), ex$mpm), stringsAsFactors = FALSE)
      pip_rows[[length(pip_rows) + 1L]] <- data.frame(method = m, scenario = s, replicate = r, case_id = id, estimator = "pooled_rb", t(e_poolrb), mpm_agrees_exact = setequal(which(colMeans(rb) > 0.5), ex$mpm), stringsAsFactors = FALSE)
      pip_rows[[length(pip_rows) + 1L]] <- data.frame(method = m, scenario = s, replicate = r, case_id = id, estimator = "repeat1_rb", t(pip_err(rb[1, ], ex$pip, g)), mpm_agrees_exact = setequal(which(rb[1, ] > 0.5), ex$mpm), stringsAsFactors = FALSE)
      sd_plain <- apply(plain, 2, sd); sd_rb <- apply(rb, 2, sd)
      rep_rows[[length(rep_rows) + 1L]] <- data.frame(method = m, scenario = s, replicate = r, case_id = id, repeat_index = NA_integer_, estimator = "sd_across_repeats_plain",
        mae = mean(sd_plain), maxae = max(sd_plain), rmse = sqrt(mean(sd_plain^2)), mae_signals = mean(sd_plain[g$signals]), mae_proxies = if (length(g$proxies)) mean(sd_plain[g$proxies]) else NA_real_,
        mae_nulls = if (length(g$nulls)) mean(sd_plain[g$nulls]) else NA_real_, mpm_agrees_exact = NA, stringsAsFactors = FALSE)
      rep_rows[[length(rep_rows) + 1L]] <- data.frame(method = m, scenario = s, replicate = r, case_id = id, repeat_index = NA_integer_, estimator = "sd_across_repeats_rb",
        mae = mean(sd_rb), maxae = max(sd_rb), rmse = sqrt(mean(sd_rb^2)), mae_signals = mean(sd_rb[g$signals]), mae_proxies = if (length(g$proxies)) mean(sd_rb[g$proxies]) else NA_real_,
        mae_nulls = if (length(g$nulls)) mean(sd_rb[g$nulls]) else NA_real_, mpm_agrees_exact = NA, stringsAsFactors = FALSE)
    }
  }
}
bind <- function(l) if (length(l)) do.call(rbind, l) else NULL
sup <- bind(sup_rows); pips <- bind(pip_rows); reps <- bind(rep_rows); ceil <- bind(ceil_rows); miss <- bind(missing)
wr <- function(df, name) if (!is.null(df)) write.csv(df, file.path(out, name), row.names = FALSE)
wr(sup, "supports_vs_exact.csv"); wr(pips, "pip_vs_exact.csv"); wr(reps, "parni_repeats_vs_exact.csv"); wr(ceil, "exact_ceilings.csv"); wr(miss, "missing.csv")
ceil_sum <- if (!is.null(ceil)) do.call(rbind, lapply(split(ceil, ceil$scenario), function(d) data.frame(scenario = d$scenario[1], n_exact = nrow(d),
  exact_mpm_recovery_rate = mean(d$mpm_recovers_truth), exact_hpm_recovery_rate = mean(d$hpm_recovers_truth), median_seconds = median(d$seconds)))) else NULL
summ <- if (!is.null(sup)) do.call(rbind, lapply(split(sup, interaction(sup$scenario, sup$method, sup$rule, drop = TRUE)), function(d) data.frame(
  scenario = d$scenario[1], method = d$method[1], rule = d$rule[1], n = nrow(d), exact_recovery_rate = mean(d$exact_recovery), mean_fp = mean(d$fp), mean_fn = mean(d$fn),
  agrees_exact_mpm_rate = mean(d$agrees_exact_mpm), agrees_exact_hpm_rate = mean(d$agrees_exact_hpm), stringsAsFactors = FALSE))) else NULL
pip_sum <- if (!is.null(pips)) do.call(rbind, lapply(split(pips, interaction(pips$scenario, pips$method, pips$estimator, drop = TRUE)), function(d) data.frame(
  scenario = d$scenario[1], method = d$method[1], estimator = d$estimator[1], n = nrow(d), mae_median = median(d$mae), mae_max = max(d$mae), maxae_median = median(d$maxae),
  mae_signals_median = median(d$mae_signals, na.rm = TRUE), mpm_agrees_exact_rate = mean(d$mpm_agrees_exact), stringsAsFactors = FALSE))) else NULL
rep_sum <- if (!is.null(reps)) do.call(rbind, lapply(split(reps, interaction(reps$scenario, reps$estimator, drop = TRUE)), function(d) data.frame(
  scenario = d$scenario[1], estimator = d$estimator[1], n = nrow(d), mae_median = median(d$mae), mae_max = max(d$mae), maxae_median = median(d$maxae), stringsAsFactors = FALSE))) else NULL
wr(summ, "summary_vs_exact.csv"); wr(pip_sum, "summary_pip_vs_exact.csv"); wr(ceil_sum, "summary_exact_ceilings.csv"); wr(rep_sum, "summary_parni_repeats.csv")
md <- function(df, digits = 4) { if (is.null(df) || !nrow(df)) return("(none)"); df[] <- lapply(df, function(x) if (is.numeric(x)) signif(x, digits) else x)
  c(paste0("| ", paste(names(df), collapse = " | "), " |"), paste0("|", paste(rep("---", ncol(df)), collapse = "|"), "|"), apply(df, 1, function(r) paste0("| ", paste(r, collapse = " | "), " |"))) }
writeLines(c(sprintf("# Comparison with the exact posterior (%s UTC)", format(Sys.time(), "%Y-%m-%d %H:%M", tz = "UTC")), "",
  sprintf("run: %s; exact references: %s (%d available); methods: %s; fits without a reference: %d", run_dir, exact_dir, if (is.null(ceil)) 0L else nrow(ceil), paste(methods, collapse = ", "), if (is.null(miss)) 0L else nrow(miss)), "",
  "## Exact decision ceilings per scenario (MPM = {PIP > 0.5}, HPM = highest posterior model)", "", md(ceil_sum), "",
  "## Supports vs the exact decisions, per scenario x method x rule", "", md(summ), "",
  "## PIP error against the exact PIPs (PIP methods)", "", md(pip_sum), "",
  "## PARNI repeats: PIP error per estimator and SD across the 5 repeats", "", md(rep_sum)), file.path(out, "SUMMARY_EXACT.md"))
cat(sprintf("exact comparison written to %s (%d support rows, %d pip rows, %d references)\n", out, if (is.null(sup)) 0L else nrow(sup), if (is.null(pips)) 0L else nrow(pips), if (is.null(ceil)) 0L else nrow(ceil)))
