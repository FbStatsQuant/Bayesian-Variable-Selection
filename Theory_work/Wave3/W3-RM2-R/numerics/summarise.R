# summarise.R -- cell summaries of the W3-RM2-R numerics from the per-run row files. Usage: Rscript summarise.R <numerics dir>
args <- commandArgs(trailingOnly = TRUE); here <- if (length(args)) args[1] else "."
fs <- list.files(file.path(here, "arrays", "rows"), pattern = "[.]rds$", full.names = TRUE)
rows <- lapply(fs, readRDS); allc <- unique(unlist(lapply(rows, names)))
rows <- lapply(rows, function(r) { for (c in setdiff(allc, names(r))) r[[c]] <- NA; r[, allc] })
d <- do.call(rbind, rows); d <- d[order(d$design, d$n, d$b, d$kappa, d$seed), ]
write.csv(d, file.path(here, "arrays", "results_raw.csv"), row.names = FALSE)
cat("runs:", nrow(d), " not ok:", sum(d$status != "ok"), "\n"); d <- d[d$status == "ok", ]
cnt <- function(x) sprintf("%d/%d", sum(x), length(x))
key <- interaction(d$design, d$n, d$b, d$kappa, drop = TRUE, lex.order = TRUE)
out <- do.call(rbind, lapply(split(d, key), function(x) data.frame(
  design = x$design[1], n = x$n[1], b = x$b[1], q = x$q[1], kappa = x$kappa[1], runs = nrow(x),
  lam_over_logn = round(mean(x$lam_over_logn), 2), phi02 = round(mean(x$phi02), 2),
  vis_start_wk_med = round(median(x$vis_start_wk), 2), vis_blk_wk_med = round(median(x$vis_blk_wk), 2), vis_blk_wk_min = round(min(x$vis_blk_wk), 2),
  start_size_med = median(x$start_size), start_out_max = max(x$start_out),
  truth_incl = cnt(x$truth_incl), wk_in_start = cnt(x$wk_in_start), sandwich = cnt(x$sandwich),
  tl_S0_pos = cnt(x$tl_S0 > 0), tl_S0_med = round(median(x$tl_S0), 2), na_S0_neg = cnt(x$na_S0 < 0), tl_defined = cnt(x$n_tl > 0), tl_ok = cnt(x$tl_ok), tl_min_med = if (all(x$n_tl == 0)) NA_real_ else round(median(x$tl_min[x$n_tl > 0]), 2), tl_min_min = if (all(x$n_tl == 0)) NA_real_ else round(min(x$tl_min[x$n_tl > 0]), 2),
  end_S0_cert = cnt(x$end_ok), end_miss_truth = sum(x$final_miss > 0), end_extra = sum(x$final_extra > 0), certified = cnt(x$certified), all_del_extra = cnt(x$all_del_extra), n_other_moves = sum(x$n_other),
  path_lat_visited = cnt(is.finite(x$naC)), path_NA_ok = cnt(x$path_NA_ok), max_moves = max(x$moves),
  mm_le3_pos = if (all(is.na(x$mm_le3))) NA_character_ else cnt(x$mm_le3 > 0),
  mm_le3_med = if (all(is.na(x$mm_le3))) NA_real_ else round(median(x$mm_le3), 2),
  mm_le3_min = if (all(is.na(x$mm_le3))) NA_real_ else round(min(x$mm_le3), 2),
  sec_med = round(median(x$sec_setup + x$sec_ls0), 1), stringsAsFactors = FALSE)))
out <- out[order(out$design, out$n, out$b, out$kappa), ]
write.csv(out, file.path(here, "summary.csv"), row.names = FALSE)
options(width = 300); print(out[, 1:27], row.names = FALSE)
print(out[, c(1:6, 28:34)], row.names = FALSE)
