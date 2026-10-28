# Local development checks explicitly authorized by managing-lead SSH hold notice.
# This is NOT the required GCC14.3/R4.5.2 NOTS validation.
a <- commandArgs(TRUE)
stopifnot(length(a) == 2L)
core <- normalizePath(a[[1]], winslash = "/", mustWork = TRUE)
out <- a[[2]]
dir.create(out, recursive = TRUE, showWarnings = FALSE)
writeLines(capture.output(sessionInfo()), file.path(out, "environment.txt"))
files <- list.files(core, pattern = "\\.R$", full.names = TRUE)
for (f in files) { parse(f); cat("PARSE_OK", basename(f), "\n") }
source(file.path(core, "v3.R"))
cat("LOCAL_BUILD_OK", V3_CPP_KEY, "\n")
# One deterministic synthetic case/seed, mandatory exact branch. Full formal
# prototype regression remains the separately submitted NOTS suite.
n <- 20L; p <- 6L
X <- outer(seq_len(n), seq_len(p), function(i, j) sin(i * j / 7) + cos(i * (j + 1) / 11))
y <- X[, 1] - 0.6 * X[, 2] + sin(seq_len(n) * 0.7)
fit <- v3_fit(X, y, seed = 19001L, allocation = list(mem_gb = 8, hours = 1))
saveRDS(list(X = X, y = y, method_seed = 19001L, fit = fit,
             environment = sessionInfo(), command = commandArgs(FALSE)), file.path(out, "single_case.rds"))
stopifnot(identical(fit$status, "exact"), isTRUE(fit$estimates_available),
          is.null(fit$pip_secondary), is.na(fit$cut_group), length(fit$pip_primary) == p)
cat("LOCAL_SINGLE_CASE_OK", fit$status, "log_Z", format(fit$log_Z, digits = 17), "\n")
