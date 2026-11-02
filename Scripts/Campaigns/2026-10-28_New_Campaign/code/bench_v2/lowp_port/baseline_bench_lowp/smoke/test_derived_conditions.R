# test_derived_conditions.R -- derived-rule (LA-4) condition status and restricted-candidate diagnostics.
# Fixture after Sol's probes (RECHECK_c N1/N2, FINAL_CONFIRM FC3). Run: Rscript smoke/test_derived_conditions.R
.libPaths(c('C:/Users/felip/AppData/Local/Temp/lowp_Rlib', .libPaths()))
self <- sub('^--file=', '', grep('^--file=', commandArgs(FALSE), value = TRUE)[1])
bench <- dirname(dirname(normalizePath(self, winslash = '/')))
source(file.path(bench, 'R/config_lowp.R')); source(file.path(bench, 'R/common.R'))
cand <- data.frame(key = c('', '1', '1;2'), k = 0:2, rss = c(1000, 200, 100), valid = TRUE)
cand$ebic1 <- 200*log(cand$rss/200) + cand$k*log(200) + 2*lchoose(20, cand$k)
cand$ebic05 <- 200*log(cand$rss/200) + cand$k*log(200) + lchoose(20, cand$k)
cand$bic <- 200*log(cand$rss/200) + cand$k*log(200)
path <- data.frame(lambda = c(1, .1, .01), key = c('', '1', '1;2'), passes = c(TRUE, TRUE, FALSE))
base_rows <- data.frame(rule_id = c('ebic1','ebic05','bic'), role = c('primary','S0','S0'), status = 'failed',
  support = NA_character_, support_audit = '1;2', k = NA_integer_, converged = TRUE, diag_flag = TRUE, diag_codes = '',
  error = 'selected support has no passing occurrence', k_valid_max = 2L, k_path_max = 2L, lambda = .01, path_index = 3L,
  rss = 100, crit_value = cand$ebic1[3], n_warnings = 0L, warnings = '', messages = '', stringsAsFactors = FALSE)
run <- function(rows) { f <- list(rules = rows, diagnostics = list(candidates = cand, path = path, gate_failures = character()))
  o <- lowp_derive(f, 'F4', 20L, 200L, 'c050'); o[o$rule_id == 'ebic1_lam005', ] }
res <- list()
r <- run(base_rows); res$no_condition_ok <- r$status == 'ok' && r$support == '1' && r$k_valid_max == 1L && grepl('ebic_at_largest', r$diag_codes)
w <- base_rows; w$n_warnings <- 1L; w$warnings <- 'package warning'; res$warning_only <- run(w)$status == 'warning'
m <- base_rows; m$messages <- 'captured message'; res$message_only <- run(m)$status == 'warning'   # FC3
print(unlist(res)); if (!all(unlist(res))) quit(status = 1); cat('derived condition tests: all pass\n')
