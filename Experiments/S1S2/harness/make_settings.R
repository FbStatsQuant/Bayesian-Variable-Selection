# make_settings.R -- writes specs/settings.tsv (136 rows: S1 16 + S2 120). Deterministic; rerun to regenerate.
# PROVENANCE
#   S1: Griffin, Latuszynski & Steel (2021), Biometrika 108(1):53-69, doi:10.1093/biomet/asaa055; arXiv:1708.05678v3,
#       Sec 4.1 p.13 (DGP) and Table 1 p.14 ((n,p) grid, SNR grid). Local PDF: _local/theory/BENCH_DESIGN/papers/BVS_Griffin2021.pdf
#   S2: Hastie, Tibshirani & Tibshirani (2020), Statist. Sci. 35(4):579-592, doi:10.1214/19-STS733; arXiv:1707.08692v2,
#       Sec 3.1 pp.8-10 (steps i-iii, beta-types, "high-5"/"high-10", nu grid). Local PDF: .../papers/Hastie2020.pdf
#   Cell numbering and setting_id format: OURS (SPEC.md §3).
# Usage: Rscript harness/make_settings.R   (from Experiments/S1S2)
args <- commandArgs(FALSE); f <- sub("^--file=", "", args[grep("^--file=", args)])
base <- if (length(f)) normalizePath(file.path(dirname(f), "..")) else getwd()

ar1_quad <- function(beta, rho) {            # beta' Sigma beta with Sigma_jk = rho^|j-k|, using the support only
  S <- which(beta != 0); b <- beta[S]
  if (rho == 0) return(sum(b^2))
  sum(outer(b, b) * rho^abs(outer(S, S, "-")))
}
cit1 <- "Griffin2021 arXiv:1708.05678v3 Sec4.1 p13 + Table1 p14"
cit2 <- "Hastie2020 arXiv:1707.08692v2 Sec3.1 pp8-10"
rows <- list()
# ---- S1: (n,p) in Table 1 row order x SNR in Table 1 column order
np1 <- list(c(500, 500), c(500, 5000), c(1000, 500), c(1000, 5000)); snr1 <- c(0.5, 1, 2, 3)
cell <- 0
for (k in seq_along(np1)) for (snr in snr1) {
  cell <- cell + 1; n <- np1[[k]][1]; p <- np1[[k]][2]
  beta <- c(snr * sqrt(1 * log(p) / n) * c(2, -3, 2, 2, -3, 3, -2, 3, -2, 3), rep(0, p - 10))
  rows[[length(rows) + 1]] <- data.frame(setting_id = sprintf("S1_%02d", cell), suite = 1L, cell = cell, n = n, p = p,
    s0 = 10L, rho = 0.6, snr = snr, nu = NA_real_, beta_type = "griffin", sigma2_rule = "fixed_1", citation = cit1,
    label = sprintf("S1 n=%d p=%d SNR=%g", n, p, snr), nu_pop = signif(ar1_quad(beta, 0.6) / 1, 6))
}
# ---- S2: config (high-5, high-10) x beta-type (1, 2) x rho (0, .35, .7) x nu (10-point grid)
cfg <- list(c(50, 1000, 5), c(100, 1000, 10)); cfgname <- c("high-5", "high-10")
nus <- c(0.05, 0.09, 0.14, 0.25, 0.42, 0.71, 1.22, 2.07, 3.52, 6.00); rhos <- c(0, 0.35, 0.7)
cell <- 0
for (k in seq_along(cfg)) for (bt in 1:2) for (rho in rhos) for (nu in nus) {
  cell <- cell + 1; n <- cfg[[k]][1]; p <- cfg[[k]][2]; s <- cfg[[k]][3]
  rows[[length(rows) + 1]] <- data.frame(setting_id = sprintf("S2_%03d", cell), suite = 2L, cell = cell, n = n, p = p,
    s0 = as.integer(s), rho = rho, snr = NA_real_, nu = nu, beta_type = as.character(bt),
    sigma2_rule = "pop_Sigma_over_nu", citation = cit2,
    label = sprintf("S2 %s bt=%d rho=%g nu=%g", cfgname[k], bt, rho, nu), nu_pop = nu)
}
tab <- do.call(rbind, rows)
stopifnot(nrow(tab) == 136, !anyDuplicated(tab$setting_id))
write.table(tab, file.path(base, "specs", "settings.tsv"), sep = "\t", quote = FALSE, row.names = FALSE, na = "NA")
cat("wrote", nrow(tab), "rows to", file.path(base, "specs", "settings.tsv"), "\n")
