setwd("C:/Users/felip/Bayesian-Variable-Selection/Theory_work/Wave1C/C-DLV/numerics")
rd <- function(pat) { f <- list.files("n4parts", pattern = pat, full.names = TRUE)
  do.call(rbind, lapply(f, function(x) { d <- read.csv(x, stringsAsFactors = FALSE, colClasses = c(design = "character", hpm = "character", S0 = "character")); d })) }
fits <- rd("_fit[.]csv$"); cons <- rd("_cons[.]csv$")
fits <- fits[order(fits$design, fits$n, fits$seed), ]; cons <- cons[order(cons$design, cons$n, cons$seed, cons$tier), ]
write.csv(fits, "N4_stress.csv", row.names = FALSE); write.csv(cons, "N4_constructions.csv", row.names = FALSE)
out <- c("# N4 stress test summary (numbers only)", "",
 "Designs: S1 (c=3, psi .2, beta 1,1,1, theta[b]=-psi*beta, visible group beta .7; S0 = 3 a-hubs + 3 b-hubs + vis hub), S2 (c=2, psi .5, betas 1,.6), S3 (c=1, beta .35, psi .2). g=9, rho=.4; seeds as listed; method seed 1000+seed; allocation 16 GB/24 h. peak_mem = process peak working set (one process per design x (n,p)).", "",
 "| design | n | p | fits | status counts | non-smc | esc rate | hpm==S0 | mean N_p | max N_p | max pilot step (tier0) | max N_b | max intervals | T_0 / T_1 | frac cons S0 in V | frac Lambda_V<log(10/9) (n eval) | max sec | max peak MB |", paste(rep("|---", 18), collapse = ""), "|")
out <- out[-length(out)]; out <- c(out, paste0(paste(rep("---", 18), collapse = "|"), "|")); out[length(out)] <- paste0("|", out[length(out)])
for (d in c("S1","S2","S3")) for (n in sort(unique(fits$n))) {
  f <- fits[fits$design == d & fits$n == n, ]; if (!nrow(f)) next
  c0 <- cons[cons$design == d & cons$n == n, ]; p <- f$p[1]
  T0 <- max(1000, ceiling(log2(n + p + 1))^2)
  st <- paste(names(table(f$status)), table(f$status), sep = ":", collapse = ", ")
  npf <- tapply(c0$N_p, paste(c0$seed, c0$tier), max); lam <- c0$Lambda_V[!is.na(c0$Lambda_V)]
  c00 <- c0[c0$tier == 0, ]
  out <- c(out, sprintf("| %s | %d | %d | %d | %s | %d | %.3f | %d/%d | %.2f | %d | %.4f | %d | %d | %d / %d | %.3f (%d/%d) | %.3f (%d/%d) | %.1f | %.0f |",
    d, n, p, nrow(f), st, sum(f$branch_run != "smc", na.rm = TRUE), mean(f$escalated %in% TRUE), sum(f$hpm_eq_S0), nrow(f),
    mean(npf), max(npf), max(c00$max_pilot_step), max(c0$N_b), max(c0$intervals), T0, 4 * T0,
    mean(c0$S0_in_V), sum(c0$S0_in_V), nrow(c0), mean(lam < log(10/9)), sum(lam < log(10/9)), length(lam),
    max(f$total_seconds, na.rm = TRUE), max(f$peak_ws_kb, na.rm = TRUE) / 1024))
}
pr <- function(x, ...) c("```", capture.output(print(x, row.names = FALSE, ...)), "```")
out <- c(out, "", "Max intervals vs T_e per (design, n, tier):", pr(aggregate(intervals ~ design + n + tier + T_e, cons, max)))
bad <- fits[fits$status != "completed", c("design","n","p","seed","status","message")]
out <- c(out, "", "Non-completed statuses:", if (nrow(bad)) pr(bad) else "none")
bc <- cons[!cons$ok, c("design","n","seed","tier","construction","reason","intervals","T_e")]
out <- c(out, "", "Constructions with ok == FALSE:", if (nrow(bc)) pr(bc) else "none")
es <- fits[fits$escalated %in% TRUE, c("design","n","seed","status","tier_final","triggers_by_tier","tier_status","max_pilot_step","hpm","S0","hpm_eq_S0")]
out <- c(out, "", "Escalated fits:", if (nrow(es)) pr(es) else "none")
out <- c(out, "", "Trigger strings:", pr(as.data.frame(table(design = fits$design, n = fits$n, trig = fits$triggers_by_tier))[as.data.frame(table(design = fits$design, n = fits$n, trig = fits$triggers_by_tier))$Freq > 0, ]))
out <- c(out, "", sprintf("Fits: %d. estimates_available FALSE: %d. guard exceeded: %d. final tier not converged: %d. forced_pilot_steps>0 constructions: %d.", nrow(fits), sum(!fits$estimates_available), sum(fits$guard_exceeded), sum(!(fits$converged_final_tier %in% TRUE)), sum(cons$forced_pilot_steps > 0)))
out <- c(out, "", "Fits with hpm != S0:", pr(fits[!fits$hpm_eq_S0, c("design","n","seed","hpm","S0")]))
writeLines(out, "N4_SUMMARY.md")
