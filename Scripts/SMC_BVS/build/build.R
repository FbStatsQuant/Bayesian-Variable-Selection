# Compile only. Execute on Owls in the Amendment 1 environment.
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 2L)
code <- normalizePath(args[[1]], mustWork = TRUE)
out <- args[[2]]
dir.create(out, recursive = TRUE, showWarnings = FALSE)
stopifnot(getRversion() == "4.6.0")
writeLines(capture.output(sessionInfo()), file.path(out, "sessionInfo.txt"))
for (pkg in c("Rcpp", "digest", "jsonlite")) {
  stopifnot(requireNamespace(pkg, quietly = TRUE))
}
source(file.path(code, "code", "core", "v3.R"))
writeLines(V3_CPP_KEY, file.path(out, "cpp_key.txt"))
writeLines(capture.output(sessionInfo()), file.path(out, "sessionInfo_loaded.txt"))
cat("BUILD_OK", V3_CPP_KEY, "\n")
