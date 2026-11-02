# Run the adapted deployed F2 suite with a local Windows path normalization shim.
# The production runner and the saved deployed-test file are not modified.
root <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2"
file <- file.path(root, "F2_ElasticNet", "tests", "test_F2_enet.R")
src <- readLines(file, warn = FALSE)
needle <- '  runner$R.version.string <- "R version 4.5.2 (2025-10-31)"'
i <- which(src == needle)
stopifnot(length(i) == 1L)
src <- append(src, '  runner$normalizePath <- function(path, ...) base::normalizePath(path, winslash = "/", ...)', after = i)
con <- textConnection(src)
source(con, local = globalenv(), chdir = FALSE)
close(con)
