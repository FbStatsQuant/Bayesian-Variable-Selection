# make_tables.R -- markdown tables for RESULTS.md from out/raw_runs*.csv (OBSERVATIONS ONLY)
here <- dirname(normalizePath(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)[1])))
rd <- function(f) read.csv(file.path(here, "out", f), stringsAsFactors = FALSE)
a <- rd("raw_runs12.csv"); b <- rd("raw_runs34.csv"); cols <- union(names(a), names(b))
for (k in setdiff(cols, names(a))) a[[k]] <- NA; for (k in setdiff(cols, names(b))) b[[k]] <- NA
d <- rbind(a[cols], b[cols]); stopifnot(all(d$status == "ok"))
f <- function(x, dg = 3) formatC(x, digits = dg, format = "fg")
iqr <- function(x) { v <- quantile(x, c(.25, .5, .75)); sprintf("%s [%s, %s]", f(v[2]), f(v[1]), f(v[3])) }
d$o0s <- d$o0 * sqrt(d$n / log(d$n)); d$r <- d$o0 / d$T1
cat("### Run 1 (V-cp): median pi0(S0) [IQR] and median o0, 10 seeds\n\n| nominal A | n | p | c | target delta^2/tau^2 | ratio to v1.4 level (1+2A)log n | median pi0 [IQR] | median o0 | #seeds pi0>0.5 |\n|---|---|---|---|---|---|---|---|---|\n")
x <- d[d$exp == "vcp", ]
for (pe in sort(unique(x$pe))) for (n in sort(unique(x$n))) for (cc in sort(unique(x$par))) { g <- x[x$pe == pe & x$n == n & x$par == cc, ]; p <- g$p[1]
  tg <- cc * log(n) + 2 * log(p)
  cat(sprintf("| %.1f | %d | %d | %.1f | %.2f | %.2f | %s | %s | %d/10 |\n", pe, n, p, cc, tg, tg / ((1 + 2 * pe) * log(n)), iqr(g$pi0), f(median(g$o0)), sum(g$pi0 > 0.5))) }
cat("\n### Run 2 (F-2, A = 0.9): o0/T1 and pi0, 10 seeds\n\n| n | p | median o0/T1 [IQR] | median o0 [IQR] | median pi0 |\n|---|---|---|---|---|\n")
x <- d[d$exp == "F2", ]
for (n in sort(unique(x$n))) { g <- x[x$n == n, ]; cat(sprintf("| %d | %d | %s | %s | %s |\n", n, g$p[1], iqr(g$r), iqr(g$o0), f(median(g$pi0)))) }
cat("\n### Runs 3-4: o0*sqrt(n/log n), median [IQR] (10 seeds each); also median o0/T1\n\n| n | p | G-1 (rho=0) | lg0a rho=2/sqrt(n log n) | lg0b rho=2/sqrt(n) | G-1 o0/T1 | max over seeds (G-1 / lg0a / lg0b) |\n|---|---|---|---|---|---|---|\n")
for (n in sort(unique(d$n[d$exp == "g1"]))) { g <- d[d$exp == "g1" & d$n == n, ]; a1 <- d[d$exp == "lg0a" & d$n == n, ]; b1 <- d[d$exp == "lg0b" & d$n == n, ]
  cat(sprintf("| %d | %d | %s | %s | %s | %s | %s / %s / %s |\n", n, 2 * n, iqr(g$o0s), iqr(a1$o0s), iqr(b1$o0s), f(median(g$r)), f(max(g$o0s)), f(max(a1$o0s)), f(max(b1$o0s)))) }
