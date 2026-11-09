t0 <- Sys.time()
source("d4_core/v3.R")
cat("compiled/loaded in", format(Sys.time()-t0), "\n")
print(ls(pattern="^v3_fit$"))
