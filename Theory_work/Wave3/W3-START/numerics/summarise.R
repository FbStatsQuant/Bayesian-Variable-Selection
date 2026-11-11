# summarise.R -- W3-START sharpness-gate numerics: tables for RESULTS.md from results_raw.csv (OBSERVATIONS ONLY).
# Usage: Rscript summarise.R results_raw.csv summary.csv
args <- commandArgs(trailingOnly = TRUE)
d <- read.csv(args[1], stringsAsFactors = FALSE)
cat("rows", nrow(d), " non-ok", sum(d$status != "ok"), "\n")
d <- d[d$status == "ok", ]
med <- function(x) if (all(is.na(x))) NA_real_ else median(x, na.rm = TRUE)
key <- unique(d[, c("exp", "par", "n")]); key <- key[order(key$exp, key$par, key$n), ]
rows <- lapply(seq_len(nrow(key)), function(i) {
  s <- d[d$exp == key$exp[i] & d$par == key$par[i] & d$n == key$n[i], ]
  data.frame(exp = key$exp[i], par = key$par[i], n = key$n[i], p = s$p[1], s0 = s$s0[1], runs = nrow(s),
             pi0_med = med(s$pi0), pi0_min = min(s$pi0), o0_med = med(s$o0), o0_sqrtn = med(s$o0) * sqrt(key$n[i]),
             o0_over_T1 = med(s$o0 / s$T1), T1_over_fn_min = min(s$T1 / s$fn), T1_over_pred = med(s$T1 / s$pred),
             U_med = med(s$U), en_med = med(s$en), Xi_med = med(s$Xi_del), Lb0_med = med(s$Lb0),
             cnull_max_med = med(s$cnull_max), ctruth_min_med = med(s$ctruth_min), cvis_all_min = suppressWarnings(min(s$cvis_all, na.rm = TRUE)),
             lat_med = med(s$lat), A_n = log(s$p[1]) / log(key$n[i]))
})
tab <- do.call(rbind, rows)
tab$cvis_all_min[!is.finite(tab$cvis_all_min)] <- NA
# log-log slope of the median odds against n, per (exp, par)
sl <- unique(tab[, c("exp", "par")]); sl$slope_o0 <- NA_real_; sl$slope_T1pred <- NA_real_
for (i in seq_len(nrow(sl))) {
  s <- tab[tab$exp == sl$exp[i] & tab$par == sl$par[i], ]
  if (nrow(s) >= 3 && all(s$o0_med > 0)) sl$slope_o0[i] <- coef(lm(log(o0_med) ~ log(n), data = s))[2]
}
tab <- merge(tab, sl[, c("exp", "par", "slope_o0")], by = c("exp", "par"))
tab <- tab[order(tab$exp, tab$par, tab$n), ]
write.csv(tab, args[2], row.names = FALSE)
fmt <- function(x) ifelse(is.na(x), "", formatC(x, digits = 3, format = "g"))
show <- c("exp", "par", "n", "p", "runs", "pi0_med", "o0_med", "o0_sqrtn", "o0_over_T1", "T1_over_fn_min", "T1_over_pred",
          "U_med", "en_med", "Xi_med", "cnull_max_med", "ctruth_min_med", "cvis_all_min", "lat_med", "slope_o0")
out <- tab[, show]; for (k in setdiff(show, c("exp", "n", "p", "runs"))) out[[k]] <- fmt(out[[k]])
cat("| ", paste(show, collapse = " | "), " |\n", sep = ""); cat("|", paste(rep("---", length(show)), collapse = "|"), "|\n", sep = "")
for (i in seq_len(nrow(out))) cat("| ", paste(out[i, ], collapse = " | "), " |\n", sep = "")
cat("\nFLOOR check (claim T0): min over all runs of T1/fn =", min(d$T1 / d$fn), "; min of o0/T1 =", min(d$o0 / d$T1), "\n")
# (AGG-b) upper bound, on runs with U < 1 (prod_b (1 + Xi_b) <= exp(sum_b Xi_b); Xi_del = sum_b Xi_b):
u <- d[d$U < 1 & is.finite(d$Xi_del), ]; R2 <- (1 - u$U)^(-(u$s0 + 1)) - 1 - (u$s0 + 1) * u$U
ub <- u$T1 + R2 + expm1(pmin(u$Xi_del, 700)) * (1 - u$U)^(-(16 * u$s0 + 1))
cat("AGG-b upper bound: runs with U < 1:", nrow(u), "; violations (o0 > bound):", sum(u$o0 > ub * (1 + 1e-9)), "; max o0/bound =", max(u$o0 / ub), "
")
cat("AGG-b: T1 <= (s0+1) U violations:", sum(d$T1 > (d$s0 + 1) * d$U * (1 + 1e-9)), "of", nrow(d), "
")
cs <- (64 * pmax(d$s0, 1))^(-16)
cat("AGG-b lower bound o0 >= c_s * Xi (using sum_b Xi_b >= Xi): violations:", sum(d$o0 < cs * d$Xi_del / pmax(d$nblk_truth, 1)), "
")
