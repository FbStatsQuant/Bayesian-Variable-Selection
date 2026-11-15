# summarise.R -- cell summaries of the W3-RM2 numerics, from the per-run row files. Usage: Rscript summarise.R <dir>
args <- commandArgs(trailingOnly = TRUE); here <- if (length(args)) args[1] else "."
fs <- list.files(here, pattern = "[.]rds$", recursive = TRUE, full.names = TRUE)
rows <- lapply(fs, readRDS)
allc <- unique(unlist(lapply(rows, names)))
rows <- lapply(rows, function(r) { for (c in setdiff(allc, names(r))) r[[c]] <- NA; r[, allc] })
d <- do.call(rbind, rows)
d <- d[order(d$type, d$eta, d$n, d$b, d$seed), ]
write.csv(d, file.path(here, "results_raw.csv"), row.names = FALSE)
cat("runs:", nrow(d), " failed:", sum(d$status != "ok"), "\n")
d <- d[d$status == "ok", ]
cnt <- function(x) sprintf("%d/%d", sum(x), length(x))
key <- interaction(d$type, d$eta, d$b, d$n, drop = TRUE, lex.order = TRUE)
out <- do.call(rbind, lapply(split(d, key), function(x) data.frame(
  type = x$type[1], eta = x$eta[1], b = x$b[1], n = x$n[1], p = x$p[1], m = x$m[1], sqrt_n = round(sqrt(x$n[1]), 1),
  log_n = round(log(x$n[1]), 1), feas = cnt(x$feas),
  start_size = sprintf("%.0f [%d,%d]", median(x$start_size), min(x$start_size), max(x$start_size)),
  start_out = sprintf("%.1f [%d,%d]", mean(x$start_out), min(x$start_out), max(x$start_out)),
  start_miss = sum(x$start_miss),
  sandwich = cnt(x$sandwich), end_S0 = cnt(x$final_eq_S0 & x$certified), all_del = cnt(x$all_del_extra),
  n_other_moves = sum(x$n_other), path_NA_ok = cnt(x$path_NA_ok), probe_NA_viol = cnt(x$probe_NA_violated),
  probe_margin_med = round(median(x$probe_margin), 2), old_cap_ok = cnt(x$old_cap_ok),
  max_moves = max(x$moves), sec = round(median(x$sec_setup + x$sec_ls0)), stringsAsFactors = FALSE)))
out <- out[order(out$type, out$eta, out$n, out$b), ]
write.csv(out, file.path(here, "summary.csv"), row.names = FALSE)
options(width = 280); print(out, row.names = FALSE)
ok <- d$final_eq_S0 & d$certified
cat("\nLS0 ended at S0 (certified):", sum(ok), "of", nrow(d), "\n")
if (any(!ok)) print(d[!ok, c("type", "eta", "b", "n", "seed", "start_size", "start_out", "moves", "final_size", "limit", "moveseq_other")])
cat("\nnon-deletion move types by cell:\n")
oth <- d[d$n_other > 0, ]
print(aggregate(n_other ~ type + eta + b + n, data = oth, FUN = sum))
tt <- table(unlist(strsplit(paste(d$moveseq_other, collapse = " "), " +")))
print(tt[names(tt) != ""])
