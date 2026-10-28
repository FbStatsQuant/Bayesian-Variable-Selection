# summarise_dev_paths.R -- per-fit ladder diagnostics of an A2 dev run (descriptive; from the RDS).
# Usage: Rscript tests/summarise_dev_paths.R --results <results/<run_id>> --out <csv>
a <- commandArgs(trailingOnly = TRUE)
get_arg <- function(k) { i <- match(paste0("--", k), a); if (is.na(i)) stop("missing --", k); a[i + 1L] }
f <- list.files(get_arg("results"), pattern = "[.]rds$", recursive = TRUE, full.names = TRUE)
out <- do.call(rbind, lapply(f, function(x) {
  r <- readRDS(x); d <- r$fit$diagnostics; t <- d$path; L <- nrow(t)
  data.frame(case_id = r$rows$case_id, method_id = r$rows$method_id, n_points = L,
             capped_points = paste(d$capped_index, collapse = ","), n_capped_intermediate = d$n_capped,
             last_capped_point = if (length(d$capped_index)) max(d$capped_index) else NA,
             k_point1 = t$k[1], sweeps_point1 = t$iter[1],
             max_sweeps_uncapped = if (any(!t$capped)) max(t$iter[!t$capped]) else NA,
             median_sweeps = stats::median(t$iter), total_sweeps = sum(t$iter),
             n_theta_sigma_not_written = sum(is.na(t$sigma)),
             sigma0 = d$sigma0, sigma_L = d$sigma_L, theta_L = d$theta_L, k_L = t$k[L], rss_L = d$rss_L,
             fixed_point_error = d$audit$max_abs_fixed_point_error, fixed_point_tol = d$audit$tolerance,
             support_mismatch = d$audit$support_mismatch, tail_stable = d$audit$tail_stable,
             first_point_tail_support = which(rev(cumprod(rev(t$support_key == t$support_key[L]))) == 1)[1],
             runtime_s = r$runtime_s, source_sha256 = r$rows$source_sha256)
}))
utils::write.csv(out, get_arg("out"), row.names = FALSE)
print(out[, c("case_id", "method_id", "capped_points", "k_point1", "max_sweeps_uncapped", "first_point_tail_support",
              "sigma_L", "k_L", "fixed_point_error", "runtime_s")], row.names = FALSE)
