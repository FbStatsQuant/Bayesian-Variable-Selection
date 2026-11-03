# summarise.R -- tables from results/fit_*.rds (METH-AUDIT). Usage: Rscript scripts/summarise.R > results/summary.md
fs <- sort(list.files("results", "^fit_.*\\.rds$", full.names = TRUE))
lse <- function(x) { m <- max(x); m + log(sum(exp(x - m))) }
se_logZ <- function(lz) { w <- exp(lz - max(lz)); sqrt(var(w) / length(w)) / mean(w) }   # delta-method SE of log pooled Zhat
cat("## Table 6.1 Bitwise check: 4 final islands as independent workers vs the serial production loop\n\n")
cat("| design | log Zhat_r identical | PIP_r identical | HPM identical | max abs d log Zhat_r |\n|---|---|---|---|---|\n")
for (f in fs) { r <- readRDS(f); b <- r$bitwise
  cat(sprintf("| %s %s | %s | %s | %s | %.1e |\n", r$id, r$scale, b$log_Z_r, b$pip_r, b$hpm, b$max_abs_dlogZ)) }
cat("\n## Table 6.2 Phase timings (s, one core unless stated; Owls, nice 19, shared machine)\n\n")
cat("| design | setup | calibration: pilot / diag islands / local / grid / total | tier | T_pil | rebuilds | T (final) | serial final (4 islands) | sum of 4 island times | R=4 wall, 2 workers | R=32 wall, 2 workers | ms per particle-round (final) |\n|---|---|---|---|---|---|---|---|---|---|---|---|\n")
for (f in fs) { r <- readRDS(f); a <- r$cal$tiers[[length(r$cal$tiers)]]; s <- a$seconds
  per_round <- 1000 * mean(r$r4$island_seconds) / (r$r4$N * (r$cal$T + 8 + 4) + r$r4$N)
  cat(sprintf("| %s %s | %.1f | %.0f / %.0f / %.1f / %.2f / %.0f | %d | %d | %d | %d | %.0f | %.0f | %.0f | %.0f | %.2f |\n",
    r$id, r$scale, r$t_setup, s[["pilot"]], s[["rebuild_islands"]], s[["rebuild_local"]], s[["grid_construction"]], r$t_cal,
    r$cal$tier, a$pilot_T, a$rebuilds, r$cal$T, r$t_final_serial, sum(r$r4$island_seconds), r$r4$wall, r$rbig$wall, per_round)) }
cat("\n## Table 6.3 Same total particles: R = 4 x N_e vs R = 32 x floor(N_e/8), same frozen grid\n\n")
cat("| design | log Zhat R=4 (SE) | log Zhat R=32 (SE) | diff / SE_diff | sd log Zhat_r: R=4 / R=32 | max abs dPIP: eq(32) vs eq(4) / zw(32) vs eq(4) / zw(4) vs eq(4) | max abs dPIP on S0: eq / zw | HPM: R4==S0, R32==S0, same | E1 islands (>1 nat below best): R4 / R32 | min ESS/N: R4 / R32 |\n|---|---|---|---|---|---|---|---|---|---|\n")
for (f in fs) { r <- readRDS(f); a <- r$r4; b <- r$rbig
  s4 <- se_logZ(a$log_Z_r); s32 <- se_logZ(b$log_Z_r); S0 <- r$S0
  orig <- as.integer(rownames(r$prod$pip_r)); i0 <- match(S0, orig)
  cat(sprintf("| %s %s | %.3f (%.3f) | %.3f (%.3f) | %.2f | %.2f / %.2f | %.3f / %.3f / %.3f | %.3f / %.3f | %s, %s, %s | %d/4 / %d/32 | %.2f / %.2f |\n",
    r$id, r$scale, a$log_Z, s4, b$log_Z, s32, (b$log_Z - a$log_Z) / sqrt(s4^2 + s32^2), sd(a$log_Z_r), sd(b$log_Z_r),
    max(abs(b$pip_eq - a$pip_eq)), max(abs(b$pip_zw - a$pip_eq)), max(abs(a$pip_zw - a$pip_eq)),
    max(abs(b$pip_eq[i0] - a$pip_eq[i0])), max(abs(b$pip_zw[i0] - a$pip_eq[i0])),
    identical(a$hpm, S0), identical(b$hpm, S0), identical(a$hpm, b$hpm),
    sum(a$island_best < a$hpm_F - 1), sum(b$island_best < b$hpm_F - 1), a$ess_min_frac, b$ess_min_frac)) }
cat("\n## Table 6.4 HPM detail\n\n| design | |S0| | R4 HPM size, F | R32 HPM size, F | F(R32) - F(R4) |\n|---|---|---|---|---|\n")
for (f in fs) { r <- readRDS(f)
  cat(sprintf("| %s %s | %d | %d, %.3f | %d, %.3f | %.3g |\n", r$id, r$scale, length(r$S0), length(r$r4$hpm), r$r4$hpm_F,
              length(r$rbig$hpm), r$rbig$hpm_F, r$rbig$hpm_F - r$r4$hpm_F)) }
