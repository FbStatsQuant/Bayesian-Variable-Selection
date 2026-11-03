# check_armA_bitwise.R -- arm A (cpp_abl_setup mode 0) must reproduce the production v3_setup/v3_fit bitwise (smoke design).
source("abl_core.R"); abl_load()
set.seed(20261103); n <- 100; p <- 150; Z <- matrix(rnorm(n * p), n); X <- Z + 0.6 * Z[, rep(1:30, 5)]
S0 <- c(3L, 17L, 40L); y <- drop(X[, S0] %*% c(1, -0.8, 0.7)) + rnorm(n)
f1 <- v3_fit(X, y, 12345L)
prod_setup <- v3_setup
v3_setup <- function(ctx) abl_setup(ctx, 0L)
f2 <- v3_fit(X, y, 12345L)
cat("log_Z_r identical:", identical(f1$log_Z_r, f2$log_Z_r), " pip_r identical:", identical(f1$pip_r, f2$pip_r),
    " hpm identical:", identical(f1$hpm, f2$hpm), " grid identical:", identical(f1$frozen$grid, f2$frozen$grid), "\n")
