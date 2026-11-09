# Windows workaround: Rcpp::sourceCpp(cacheDir=...) cannot create the nested cache/sourceCpp-<arch>-<ver> level.
# Create the content-hash key directory via load_test_core (fails fast), then pre-create the nested directory.
a <- commandArgs(TRUE); testdir <- a[1]; core <- a[2]
source(file.path(testdir, "common.R"))
try(load_test_core(core, tempfile("warm"), testdir), silent = TRUE)
cr <- Sys.getenv("V3_TEST_COMPILE_CACHE")
for (k in list.dirs(cr, recursive = FALSE))
  dir.create(file.path(k, "cache", paste0("sourceCpp-", R.version$platform, "-", as.character(packageVersion("Rcpp")))), recursive = TRUE, showWarnings = FALSE)
cat("warmed", list.dirs(cr, recursive = FALSE), sep = "\n")
