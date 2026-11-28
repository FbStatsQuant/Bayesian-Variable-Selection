# e7_bt2diag_crosscheck.R -- cross-check of the proxy shares in e7 against Engineering's bt2 diagnostic per-rep table (bt1/bt2, rho in {.35,.7}); also totals by failure type for E0
suppressMessages(library(data.table))
args <- commandArgs(FALSE); sf <- sub("--file=", "", args[grep("--file=", args)]); base <- normalizePath(file.path(dirname(sf), ".."))
source(file.path(base, "scripts", "pop_lib.R"))
d <- fread(file.path(ENG, "diagnostics", "bt2_diagnostic_per_rep.tsv"), data.table = FALSE)
f <- d[!as.logical(d$success), ]
o <- do.call(rbind, lapply(split(f, list(f$beta_type, f$rho), drop = TRUE), function(x) data.frame(beta_type = x$beta_type[1], rho = x$rho[1], failed = nrow(x), share_FN_with_selected_neighbour_gt0 = mean(x$FN_with_selected_neighbour > 0),
  share_FP_adjacent_gt0 = mean(x$FP_adjacent > 0), share_FP_any_gt0 = mean(x$FP > 0), share_size_mpm_lt_s = mean(x$size_minus_s < 0), share_empty = mean(x$size_mpm == 0))))
write_tsv(o, file.path(base, "tables", "e7_bt2diag_crosscheck.tsv")); print(o, digits = 3)
e0 <- read.delim(file.path(base, "tables", "e0_regime_by_setting.tsv"))
tt <- aggregate(cbind(k_exact, statistical, search, none) ~ suite, e0, sum); write_tsv(tt, file.path(base, "tables", "e0_failure_totals.tsv")); print(tt)
