# probe2.R: structure of a v2.2.x p500 record (identity gate) -- instrumentation, plain PIPs, stop record.
f <- "C:/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign/results/conf_identity/results/conf_identity/p0500/p0500_S5_r059_c100/SMCBVS.rds"
r <- readRDS(f)
cat("record names:", names(r), "\n"); cat("fit names:", names(r$fit), "\n")
ins <- r$instrumentation %||% r$fit$instrumentation
cat("instrumentation (record):", names(r$instrumentation), "\n"); cat("instrumentation (fit):", names(r$fit$instrumentation), "\n")
str(ins, max.level = 2, list.len = 40)
cat("pip_plain length:", length(r$pip_plain), " mpm_plain:", r$mpm_plain, "\n")
cat("mpm:", r$mpm, "\nhpm:", r$hpm, "\n")
