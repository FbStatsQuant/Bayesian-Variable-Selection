# diag_i2_build.R -- diagnosis of the unit test i.2 failure (job 2275397): is the difference
# between the study-library SSLASSO 1.2.3.9001 and a freshly built upstream 1.2.3 due to the
# patch or to the build (R's CFLAGS include -march=native; the study library was built on a
# login node, the test built upstream on a compute node)?
# Builds upstream 1.2.3 and patched 1.2.3.9001 from their tarballs into two temporary libraries
# in the same job with the same flags, runs a2_native_path on the dev fixture (p = 500, S4,
# r1, c100, primary ladder) with each build and with the study-library build (each in its own
# Rscript --vanilla process), and compares beta paths, iterations, theta and sigma.
# Usage: Rscript tests/diag_i2_build.R --code <code dir> --out <dir> --dev_input <rds>

a <- commandArgs(trailingOnly = TRUE)
get_arg <- function(k) { i <- match(paste0("--", k), a); if (is.na(i)) stop("missing --", k); a[i + 1L] }
code_dir <- normalizePath(get_arg("code")); out_dir <- get_arg("out"); dev_input <- get_arg("dev_input")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
study_lib <- "/projects/ml75/fb31/BVS/bench20261019/lib/R452"
tarballs <- c(upstream = file.path(code_dir, "vendor", "SSLASSO_1.2.3.tar.gz"),
              patched  = "/projects/ml75/fb31/BVS/bench20261019/lib/tarballs/SSLASSO_1.2.3.9001.tar.gz")
want_sha <- c(upstream = "67fb4a881d0b274b2cf00ce7f40d9e6f964aa7f051094078e0bc1b058cd540c1",
              patched  = "f82bf8db6bb4145a26aa69d1d8f39ac842706df02aa9c10729153f68e16bf589")
.libPaths(c(study_lib, .Library))
for (k in names(tarballs)) {
  s <- digest::digest(file = tarballs[[k]], algo = "sha256")
  if (s != want_sha[[k]]) stop(k, " tarball hash mismatch: ", s)
}
cat("node:", Sys.info()[["nodename"]], "\n")
cat("cpu:", system("grep -m1 'model name' /proc/cpuinfo", intern = TRUE), "\n")
cat("CFLAGS:", system2(file.path(R.home("bin"), "R"), c("CMD", "config", "CFLAGS"), stdout = TRUE), "\n")

run_build <- function(lib, label) {
  out <- file.path(out_dir, paste0("path_", label, ".rds")); script <- tempfile(fileext = ".R")
  writeLines(c(
    sprintf('.libPaths(c("%s", .Library))', lib),
    'stopifnot(requireNamespace("SSLASSO", quietly = TRUE))',
    'env <- new.env(parent = asNamespace("stats"))',
    sprintf('for (f in c("config.R", "common.R", "methods/fit_A2_ssl.R")) sys.source(file.path("%s", f), envir = env)', code_dir),
    'settings <- mget(c("COMMON", "A2", "A2RS", "METHODS"), envir = env)',
    sprintf('d <- readRDS("%s"); y <- unname(d$Y[, "c100"])', dev_input),
    'lad <- env$a2_ladder(nrow(d$X), ncol(d$X), "primary", settings)',
    'path <- env$a2_native_path(d$X, y, lad$lambda0, lad$lambda1, settings)',
    sprintf('saveRDS(list(path = path, version = as.character(utils::packageVersion("SSLASSO")), loc = find.package("SSLASSO")), "%s")', out)),
    script)
  log <- system2(file.path(R.home("bin"), "Rscript"), c("--vanilla", shQuote(script)), stdout = TRUE, stderr = TRUE)
  if (!file.exists(out)) stop(label, " run failed: ", paste(log, collapse = " / "))
  readRDS(out)
}

res <- list(study = run_build(study_lib, "study_lib_patched"))
for (k in names(tarballs)) {
  lib <- tempfile(paste0("sslasso_", k, "_")); dir.create(lib)
  inst <- system2(file.path(R.home("bin"), "R"), c("CMD", "INSTALL", "--no-test-load", "-l", shQuote(lib), shQuote(tarballs[[k]])),
                  stdout = TRUE, stderr = TRUE)
  writeLines(inst, file.path(out_dir, paste0("install_", k, ".log")))
  cat(k, "compile line:", grep("-c SSL_gaussian.c", inst, value = TRUE, fixed = TRUE)[1], "\n")
  res[[paste0(k, "_job")]] <- run_build(lib, paste0(k, "_job_build"))
  unlink(lib, recursive = TRUE)
}
cmp <- function(a, b) {
  c(beta_identical = identical(a$path$beta, b$path$beta), iter_identical = identical(a$path$iter, b$path$iter),
    theta_identical = identical(a$path$theta, b$path$theta), sigma_identical = identical(a$path$sigma, b$path$sigma),
    max_abs_dbeta = max(abs(a$path$beta - b$path$beta)), max_abs_dsigma = max(abs(a$path$sigma - b$path$sigma), na.rm = TRUE),
    same_supports_all_points = identical(a$path$beta != 0, b$path$beta != 0))
}
tab <- rbind(`patched_job vs upstream_job` = cmp(res$patched_job, res$upstream_job),
             `study_lib vs patched_job`   = cmp(res$study, res$patched_job),
             `study_lib vs upstream_job`  = cmp(res$study, res$upstream_job))
print(tab)
saveRDS(list(table = tab, versions = vapply(res, `[[`, "", "version"), locs = vapply(res, `[[`, "", "loc")),
        file.path(out_dir, "diag_i2_summary.rds"))
utils::write.csv(data.frame(comparison = rownames(tab), tab, check.names = FALSE), file.path(out_dir, "diag_i2_summary.csv"), row.names = FALSE)
