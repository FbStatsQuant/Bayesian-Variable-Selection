setwd("C:/Users/felip/Bayesian-Variable-Selection/Theory_work/Wave1C/C-DLV/numerics")
rd <- function(pat) do.call(rbind, lapply(list.files("parts", pattern = pat, full.names = TRUE), read.csv, stringsAsFactors = FALSE, colClasses = c(design = "character")))
fits <- rd("_fit[.]csv$"); cons <- rd("_cons[.]csv$")
fits <- fits[order(fits$design, fits$n, fits$seed), ]; cons <- cons[order(cons$design, cons$n, cons$seed, cons$tier), ]
write.csv(fits, "dlv_runs.csv", row.names = FALSE); write.csv(cons, "dlv_constructions.csv", row.names = FALSE)
out <- c("# C-DLV numerics summary (numbers only)", "",
 "Core: byte-identical copy of Scripts/SMC_BVS/core (hashes in core_copy_hashes.txt). Per fit: data seed = seed, method seed = 1000 + seed, allocation mem_gb 16 / hours 24. Designs M, F as in the brief; S0 = {1,10} (M), {1,19} (F) (1-based; F second signal = hub of 0-based group 2, the first unlinked group).",
 "Per-construction detail: dlv_constructions.csv. Per-fit: dlv_runs.csv, rds/.",
 "peak_mem = process-lifetime peak working set (Windows, one R process runs 16 fits in sequence, so it is a running maximum); fit$peak_memory_kb is NA on Windows.", "",
 "| design | n | p | fits | status counts | non-smc | esc rate | hpm==S0 | mean N_p | max N_p | max N_b | max intervals | T_0 / T_1 | frac cons S0 in V | frac Lambda_V<log(10/9) (n eval) | max Lambda_V | max sec | max peak_mem MB |",
 "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for (d in c("M", "F")) for (n in sort(unique(fits$n))) {
  f <- fits[fits$design == d & fits$n == n, ]; if (!nrow(f)) next
  c0 <- cons[cons$design == d & cons$n == n, ]; p <- f$p[1]
  ell <- ceiling(log2(n + p + 1)); T0 <- max(1000, ell^2)
  st <- paste(names(table(f$status)), table(f$status), sep = ":", collapse = ", ")
  # N_p per fit (tier-0 pilot, and all tiers)
  npf <- tapply(c0$N_p, paste(c0$seed, c0$tier), max)
  lam <- c0$Lambda_V[!is.na(c0$Lambda_V)]
  ev <- sum(!is.na(c0$Lambda_V))
  ints <- max(c0$intervals, na.rm = TRUE)
  tiers_used <- sort(unique(c0$tier))
  out <- c(out, sprintf("| %s | %d | %d | %d | %s | %d | %.3f | %d/%d | %.2f | %d | %d | %d | %d / %d | %.3f (%d/%d) | %.3f (%d/%d) | %s | %.1f | %.0f |",
    d, n, p, nrow(f), st, sum(f$branch_run != "smc"), mean(f$escalated %in% TRUE), sum(f$hpm_eq_S0), nrow(f),
    mean(npf), max(npf), max(c0$N_b), ints, T0, 4 * T0,
    mean(c0$S0_in_V), sum(c0$S0_in_V), nrow(c0), mean(lam < log(10 / 9)), sum(lam < log(10 / 9)), ev,
    format(signif(max(lam), 4)), max(f$total_seconds, na.rm = TRUE), max(f$peak_memory_kb, na.rm = TRUE) / 1024))
}
out <- c(out, "", "Tier-wise max intervals vs T_e (all constructions):")
tt <- aggregate(intervals ~ design + n + tier + T_e, cons, max); out <- c(out, "```", capture.output(print(tt, row.names = FALSE)), "```")
out <- c(out, "", "Constructions with ok == FALSE:", "```", capture.output(print(cons[!cons$ok, c("design","n","seed","tier","construction","reason","intervals")], row.names = FALSE)), "```")
out <- c(out, "", "Trigger strings (tier:fired) counts:", "```", capture.output(print(table(fits$design, fits$n, fits$triggers_by_tier))), "```")
out <- c(out, "", "Escalated fits:", "```", capture.output(print(fits[fits$escalated %in% TRUE, c("design","n","seed","status","tier_final","triggers_by_tier","hpm","hpm_eq_S0")], row.names = FALSE)), "```")
bad <- fits[fits$status != "completed", c("design","n","p","seed","status","message")]
out <- c(out, "", "Non-completed statuses:", if (nrow(bad)) c("```", capture.output(print(bad, row.names = FALSE)), "```") else "none",
  "", sprintf("Guard exceeded in any fit: %s. Fits with estimates_available FALSE: %d. Converged (final tier) false: %d.", any(fits$guard_exceeded %in% TRUE), sum(!fits$estimates_available), sum(!(fits$converged_final_tier %in% TRUE))),
  "", "hpm by (design, n):", "```", capture.output(print(table(fits$design, fits$n, fits$hpm))), "```")
writeLines(out, "SUMMARY_dlv.md")
