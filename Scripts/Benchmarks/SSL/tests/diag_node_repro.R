# diag_node_repro.R -- cross-node reproducibility of A2 (diagnostic; not a unit test).
# Fits A2 and SSL-RS on the dev fixture (p = 500, S4, r1, c100) with the study-library build and
# saves the rule rows, beta-hat, the per-point table and the CPU model. Run once per node type
# (slurm/diag_node.slurm with --constraint); then compare the saved files with --compare.
# Usage: Rscript tests/diag_node_repro.R --code <dir> --out <file.rds> --dev_input <rds>
#        Rscript tests/diag_node_repro.R --compare <a.rds> <b.rds>
a <- commandArgs(trailingOnly = TRUE)
if (identical(a[1], "--compare")) {
  x <- readRDS(a[2]); y <- readRDS(a[3])
  cat("nodes:", x$node, "/", y$node, "\ncpus:", x$cpu, "/", y$cpu, "\n")
  for (v in c("primary", "RS")) {
    fx <- x$fits[[v]]; fy <- y$fits[[v]]
    cat(sprintf("%-7s rules identical: %s | beta identical: %s (max |d| %.3g) | path table identical: %s | iter identical: %s | RSS max rel diff %.3g\n",
                v, identical(fx$rules, fy$rules), identical(fx$diagnostics$beta_final, fy$diagnostics$beta_final),
                max(abs(fx$diagnostics$beta_final - fy$diagnostics$beta_final)),
                identical(fx$diagnostics$path, fy$diagnostics$path),
                identical(fx$diagnostics$path$iter, fy$diagnostics$path$iter),
                max(abs(fx$diagnostics$path$rss - fy$diagnostics$path$rss) / fx$diagnostics$path$rss)))
  }
  quit(status = 0)
}
get_arg <- function(k) { i <- match(paste0("--", k), a); if (is.na(i)) stop("missing --", k); a[i + 1L] }
code_dir <- normalizePath(get_arg("code"))
Sys.setenv(A2_CODE_DIR = code_dir)
source(file.path(code_dir, "run_case.R"))
.libPaths(c(STUDY_LIB, .Library))
env <- load_fit_env(code_dir); settings <- build_settings(env)
d <- readRDS(get_arg("dev_input")); y <- unname(d$Y[, "c100"])
fits <- list()
for (v in c("primary", "RS")) { s <- settings; s$variant <- v; fits[[v]] <- env$fit_A2_ssl(d$X, y, d$foldid, d$method_seed, s) }
saveRDS(list(node = Sys.info()[["nodename"]], cpu = system("grep -m1 'model name' /proc/cpuinfo", intern = TRUE),
             blas = extSoftVersion()[["BLAS"]], fits = fits), get_arg("out"))
cat("saved", get_arg("out"), "on", Sys.info()[["nodename"]], "\n")
