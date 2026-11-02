# p0a_magnitude.R GENERATE_R STUDY : size of the NOTS-regeneration vs sealed-copy differences for the six staged pilot datasets (OPS-4 diagnosis, read-only).
a <- commandArgs(trailingOnly = TRUE); suppressMessages(source(a[1], chdir = TRUE)); study <- a[2]
cat(sprintf("R %s | BLAS %s\n", getRversion(), extSoftVersion()[["BLAS"]]))
for (id in c("p0020_S1_r001", "p0020_S4_r050", "p0020_S6_r100", "p0030_S1_r001", "p0030_S4_r050", "p0030_S6_r100")) {
  p <- as.integer(substr(id, 2, 5)); s <- as.integer(substr(id, 8, 8)); r <- as.integer(substr(id, 11, 13))
  d <- generate_dataset(p, s, r, "prod")
  si <- readRDS(file.path(study, "inputs", substr(id, 1, 5), paste0(id, ".rds")))
  st <- readRDS(file.path(study, "truth", substr(id, 1, 5), paste0(id, ".rds")))
  f <- function(u, v) { u <- as.double(u); v <- as.double(v); sprintf("ndiff=%d/%d maxabs=%.3g maxrel=%.3g", sum(u != v), length(u), max(abs(u - v)), max(abs(u - v) / pmax(abs(v), 1e-300))) }
  cat(sprintf("%s | X %s | Y %s | foldid %s | eps %s | signal %s\n", id, f(d$inputs$X, si$X), f(d$inputs$Y, si$Y), f(d$inputs$foldid, si$foldid), f(d$truth$eps, st$eps), f(d$truth$signal, st$signal)))
}
