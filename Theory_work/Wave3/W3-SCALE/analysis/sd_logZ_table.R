# sd_logZ_table.R -- free task of leg A: sd(log Zhat_r) across islands, by p (evidence for the island-degeneracy
# question). Inputs: saved v3.1 fits of the bit-identity round (24 PROD-H units, replicate r001) and the profile records.
# For every fit: the 4 final islands (N particles) and, per calibration rebuild iteration, the 4 diagnostic islands
# (H particles). Usage: Rscript --vanilla sd_logZ_table.R FITS_DIR PROFILES_DIR OUT_PREFIX
a <- commandArgs(trailingOnly = TRUE)
fits <- list.files(a[1], pattern = "__v31\\.fit\\.rds$", recursive = TRUE, full.names = TRUE)
rows <- list()
add <- function(...) rows[[length(rows) + 1]] <<- data.frame(..., stringsAsFactors = FALSE)
for (f in fits) {
  x <- readRDS(f); id <- sub("__v31\\.fit\\.rds$", "", basename(f))
  m <- regmatches(id, regexec("^p(\\d+)_S(\\d)_r(\\d+)_(c\\d+)$", id))[[1]]
  design <- if (length(m) == 5) paste0("PROD-H S", m[3], " ", m[5]) else id
  tier <- x$settings$tier; N <- x$settings$N
  add(source = "final", unit = id, design = design, p = x$p, n = x$n, tier = tier, particles = N, T = length(x$grid) - 1L,
      iter = NA, sd = stats::sd(x$log_Z_r), range = diff(range(x$log_Z_r)), log_Z = x$log_Z)
  for (t in x$calibration$tiers) for (it in t$iterations) if (length(it$log_Z_r) == 4)
    add(source = "diag", unit = id, design = design, p = x$p, n = x$n, tier = t$tier, particles = t$settings$H, T = length(it$grid) - 1L,
        iter = it$iteration, sd = stats::sd(it$log_Z_r), range = diff(range(it$log_Z_r)), log_Z = NA)
}
for (f in list.files(a[2], pattern = "^prof_p(2k|5k)\\.rds$", recursive = TRUE, full.names = TRUE)) {
  p <- readRDS(f); id <- p$meta$dataset_id
  if (!is.null(p$final$log_Z_r)) add(source = "final", unit = id, design = "S3-type (profile)", p = p$budgets$p, n = p$budgets$n, tier = p$final$tier,
      particles = p$final$N, T = p$final$T, iter = NA, sd = stats::sd(p$final$log_Z_r), range = diff(range(p$final$log_Z_r)), log_Z = p$final$log_Z)
  for (t in p[["calibration"]]$tiers) for (it in t$iterations) if (length(it$log_Z_r) == 4)
    add(source = "diag", unit = id, design = "S3-type (profile)", p = p$budgets$p, n = p$budgets$n, tier = t$tier, particles = p$budgets$H0 * 4^t$tier, T = it$T,
        iter = it$iteration, sd = stats::sd(it$log_Z_r), range = diff(range(it$log_Z_r)), log_Z = NA)
}
tab <- do.call(rbind, rows)
write.table(tab, paste0(a[3], "_long.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
q <- function(v, pr) unname(stats::quantile(v, pr))
agg <- do.call(rbind, lapply(split(tab, list(tab$source, tab$p, tab$particles), drop = TRUE), function(d)
  data.frame(source = d$source[1], p = d$p[1], particles = d$particles[1], fits = length(unique(d$unit)), island_sets = nrow(d),
             sd_median = stats::median(d$sd), sd_mean = mean(d$sd), sd_q90 = q(d$sd, 0.9), sd_max = max(d$sd), share_sd_gt_1 = mean(d$sd > 1),
             # effective share of islands under evidence weights if log Z_r were normal with this sd: exp(-sd^2)
             Reff_share_at_median = exp(-stats::median(d$sd)^2), Reff_share_at_q90 = exp(-q(d$sd, 0.9)^2))))
agg <- agg[order(agg$source, agg$p, agg$particles), ]
write.table(format(agg, digits = 3), paste0(a[3], "_by_p.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
print(format(agg, digits = 3), row.names = FALSE)
fin <- tab[tab$source == "final", c("unit", "p", "tier", "particles", "T", "sd", "range")]
print(format(fin[order(fin$p, -fin$sd), ], digits = 3), row.names = FALSE)
