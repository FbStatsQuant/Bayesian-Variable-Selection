args <- commandArgs(TRUE); source(file.path(args[1], "v3.R"))
set.seed(3); n <- 60; p <- 40; X <- matrix(rnorm(n * p), n, p); y <- X[, 1] - X[, 2] + rnorm(n)
real <- .v3cpp$cpp_final_run
assign("cpp_final_run", function(...) { r <- real(...); r$status <- "resource_limit"; r }, envir = .v3cpp)  # emulate a guard stop in the final run
fit <- v3_fit(X, y, seed = 7L)
NEWF <- c("pip_list", "mpm_list", "log_Z_list", "list_size", "list_full", "pip_list_source", "pip_list_flag")
cat("branch:", fit$branch_run, " status:", fit$status, " estimates_available:", fit$estimates_available, "\n")
cat("list fields present:", paste(NEWF[NEWF %in% names(fit)], collapse = ", "), "\n")
cat("pip_list_flag:", fit$pip_list_flag, " list_size:", fit$list_size, " log_Z_list:", fit$log_Z_list, "\n")
