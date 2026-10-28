# NOTS-only compile/toolchain verification. No production fit is called.
# Arguments: private scratch snapshot, evidence root, launch.json, explicit R library.
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 4L)
code <- normalizePath(args[[1]], mustWork = TRUE)
out <- normalizePath(args[[2]], mustWork = TRUE)
lib <- normalizePath(args[[4]], mustWork = TRUE)
stopifnot(getRversion() == "4.5.2", nzchar(Sys.getenv("SLURM_JOB_ID")),
          Sys.getenv("SLURM_CPUS_PER_TASK") == "1")
stopifnot(grepl("^/scratch/fb31/smcbvs_v3_deploy_20261022/A_build/", code))
.libPaths(c(lib, .Library))
writeLines(capture.output(sessionInfo()), file.path(out, "sessionInfo_before.txt"))
for (pkg in c("Rcpp", "digest", "jsonlite")) {
  # Explicit installed library, no install.packages/network or module-library assumption.
  stopifnot(dir.exists(file.path(lib, pkg)))
  loadNamespace(pkg, lib.loc = lib)
  stopifnot(normalizePath(getNamespaceInfo(asNamespace(pkg), "path")) ==
            normalizePath(file.path(lib, pkg)))
}
config <- jsonlite::fromJSON(args[[3]], simplifyVector = FALSE)
packages <- lapply(c("Rcpp", "digest", "jsonlite"), function(pkg) {
  version <- as.character(utils::packageVersion(pkg, lib.loc = lib))
  stopifnot(identical(version, config$deps[[pkg]]))
  desc <- utils::packageDescription(pkg, lib.loc = lib)
  list(package = pkg, version = version, library = lib,
       built = desc$Built, path = getNamespaceInfo(asNamespace(pkg), "path"))
})
for (compiler in c("gcc", "g++")) {
  stopifnot(identical(system2(compiler, "-dumpfullversion", stdout = TRUE), "14.3.0"))
}
# Prove Rcpp actually compiles/links/loads using this R/C++17 environment.
probe <- file.path(out, "toolchain_probe.cpp")
writeLines(c("// [[Rcpp::plugins(cpp17)]]", "#include <Rcpp.h>",
             "// [[Rcpp::export]]", "int nots_gcc_major() { return __GNUC__; }",
             "// [[Rcpp::export]]", "int nots_gcc_minor() { return __GNUC_MINOR__; }"), probe)
probe_env <- new.env(parent = globalenv())
Sys.setenv(R_MAKEVARS_USER = file.path(code, "code/core/cpp/Makevars.v3"))
Rcpp::sourceCpp(probe, env = probe_env, cacheDir = file.path(out, "toolchain_probe_cache"),
                rebuild = TRUE, showOutput = TRUE, verbose = TRUE)
stopifnot(probe_env$nots_gcc_major() == 14L, probe_env$nots_gcc_minor() == 3L)
receipt <- list(status = "toolchain_check_pass", R = as.character(getRversion()),
                GCC = "14.3.0", packages = packages, source_manifest_sha256 = config$manifest_sha256,
                job_id = Sys.getenv("SLURM_JOB_ID"), pid = Sys.getpid(),
                utc = format(Sys.time(), tz = "UTC", usetz = TRUE), production_go = FALSE)
jsonlite::write_json(receipt, file.path(out, "TOOLCHAIN_PASS.json"), auto_unbox = TRUE, pretty = TRUE)
# This uses the same v3 entry point as build/build.R, without its Owls version assertion.
source(file.path(code, "code/core/v3.R"))
writeLines(V3_CPP_KEY, file.path(out, "cpp_key.txt"))
writeLines(capture.output(sessionInfo()), file.path(out, "sessionInfo_loaded.txt"))
cat("NOTS_BUILD_OK", V3_CPP_KEY, "\n")
