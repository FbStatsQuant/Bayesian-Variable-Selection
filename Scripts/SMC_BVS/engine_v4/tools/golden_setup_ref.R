# golden_setup_ref.R -- reference outputs from core/ (revision D) through its own R entry points, for the WP2 golden
# test `golden_R_reference` (tests/test_setup.cpp). Covers what exists only in the Rcpp layer (cpp_dup_components,
# cpp_cut_group, cpp_setup) plus v3_preprocess standardisation.
#   Rscript tools/golden_setup_ref.R <core dir> <out dir> [<work dir>]
# core/ is copied to <work dir>/core_copy first (default <out dir>/../core_copy_wp2), so the compiled cache is never
# written inside core/ or the fixtures. Writes <out dir>/SHA256SUMS.
args <- commandArgs(trailingOnly = TRUE)
core <- normalizePath(args[1]); out <- args[2]
work <- if (length(args) >= 3) args[3] else file.path(dirname(out), "core_copy_wp2")
dir.create(out, recursive = TRUE, showWarnings = FALSE); dir.create(work, recursive = TRUE, showWarnings = FALSE)
cc <- file.path(work, "core_copy")
unlink(cc, recursive = TRUE); dir.create(cc)
file.copy(list.files(core, full.names = TRUE), cc, recursive = TRUE)
source(file.path(cc, "v3.R"), chdir = TRUE)

wr_int_rows <- function(L, f) writeLines(vapply(L, function(v) paste(v, collapse = ","), ""), f)
mk <- function(design, n, p, seed) {
  set.seed(seed)
  X <- matrix(0, n, p)
  if (design == "AR") { X[, 1] <- rnorm(n); for (j in 2:p) X[, j] <- 0.6 * X[, j - 1] + sqrt(1 - 0.36) * rnorm(n) }
  if (design == "BLK") { for (j in 1:p) { if ((j - 1) %% 20 == 0) f <- rnorm(n); X[, j] <- sqrt(0.5) * f + sqrt(0.5) * rnorm(n) } }
  if (design == "TIE") {
    X[, 1] <- rnorm(n); for (j in 2:p) X[, j] <- 0.6 * X[, j - 1] + sqrt(1 - 0.36) * rnorm(n)
    for (j in seq(2, p, by = 7)) X[, j] <- if (j %% 2) X[, j - 1] else -2 * X[, j - 1] + 3   # exact (affine) duplicates
  }
  y <- X[, max(1, p %/% 7)] - 0.8 * X[, max(1, 3 * p %/% 7)] + rnorm(n)
  list(X = X, y = y)
}
cases <- list(c("AR", 200, 300, 1), c("BLK", 100, 400, 2), c("TIE", 120, 350, 3), c("TIE", 60, 90, 4))
idx <- character(0)
for (cs in cases) {
  d <- cs[1]; n <- as.integer(cs[2]); p <- as.integer(cs[3]); seed <- as.integer(cs[4])
  g <- mk(d, n, p, seed)
  pp <- v3_preprocess(g$X, g$y, dup_components = FALSE)
  stopifnot(pp$status == "ok", pp$p == p)
  ctx <- v3_context(pp$X, pp$y)
  s <- v3_setup(ctx)
  stopifnot(inherits(s, "v3_setup"))
  dup <- .v3cpp$cpp_dup_components(ctx)
  cg <- .v3cpp$cpp_cut_group(s$ptr)
  tag <- sprintf("%s_n%d_p%d", d, n, p); dd <- file.path(out, tag); dir.create(dd, showWarnings = FALSE)
  writeBin(as.numeric(pp$X), file.path(dd, "Xs.f64")); writeBin(as.numeric(pp$y), file.path(dd, "ys.f64"))
  writeLines(as.character(c(n, p, s$B)), file.path(dd, "dims.txt"))
  wr_int_rows(unname(s$neighbours), file.path(dd, "neighbours.txt"))
  wr_int_rows(s$blocks, file.path(dd, "blocks.txt"))
  wr_int_rows(dup, file.path(dd, "dup.txt"))
  wr_int_rows(lapply(cg$components, function(x) x$members), file.path(dd, "cut.txt"))
  writeBin(unlist(lapply(s$tables, function(t) t$log_r)), file.path(dd, "logr.f64"))
  writeBin(s$start$log_Zbar0, file.path(dd, "logZbar0.f64"))
  idx <- c(idx, tag)
}
writeLines(idx, file.path(out, "INDEX"))
fs <- sort(setdiff(list.files(out, recursive = TRUE), "SHA256SUMS"))
writeLines(paste0(vapply(fs, function(f) digest::digest(file = file.path(out, f), algo = "sha256"), ""), "  ./", fs), file.path(out, "SHA256SUMS"))
cat("wrote", length(idx), "reference cases to", out, "\n")
