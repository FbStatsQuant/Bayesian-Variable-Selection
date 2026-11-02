#!/usr/bin/env Rscript
# pilot_build.R -- compile the v2.2.1 core (byte-identical to v2.2) (into <core-dir>/.cpp_cache) and the enumerator (into LOWP_ENUM_CACHE), once, before the
# arrays start, so that array tasks never race on a build; report the toolchain and compile keys.
#   Rscript pilot_build.R --core-dir <code/core/v2_2_1/core> --enum-dir <code/lowp/enum> --out <dir>
# Writes <out>/BUILD_REPORT.txt. Exit 0 if both builds load.

a <- commandArgs(trailingOnly = TRUE)
opt <- function(k) { i <- match(paste0("--", k), a); if (is.na(i) || i == length(a)) NULL else a[i + 1L] }
core <- opt("core-dir"); enum <- opt("enum-dir"); out <- opt("out")
if (is.null(core) || is.null(enum) || is.null(out)) stop("usage: pilot_build.R --core-dir DIR --enum-dir DIR --out DIR")
dir.create(out, recursive = TRUE, showWarnings = FALSE)
core <- normalizePath(core, winslash = "/", mustWork = TRUE); enum <- normalizePath(enum, winslash = "/", mustWork = TRUE)
Sys.setenv(LOWP_ENUM_DIR = enum)
L <- c(sprintf("# pilot build report %s UTC", format(Sys.time(), tz = "UTC", "%Y-%m-%d %H:%M")),
       sprintf("host %s; %s; platform %s", Sys.info()[["nodename"]], R.version.string, R.version$platform),
       sprintf("BLAS %s; LAPACK %s", extSoftVersion()[["BLAS"]], La_library()),
       sprintf("libPaths: %s", paste(.libPaths(), collapse = " | ")),
       sprintf("CXX17 / flags: %s",
               paste(tryCatch(system2(file.path(R.home("bin"), "R"), c("CMD", "config", "CXX17", "CXX17FLAGS"), stdout = TRUE, stderr = FALSE), error = function(e) "n/a"), collapse = " ; ")))
t0 <- proc.time()[["elapsed"]]
source(file.path(core, "v3.R"), local = FALSE)       # compiles via v3_compile() with cpp/Makevars.v3
L <- c(L, sprintf("core compile+load: %.1f s; V3_CPP_KEY %s; cache %s", proc.time()[["elapsed"]] - t0, V3_CPP_KEY, file.path(core, ".cpp_cache")))
t0 <- proc.time()[["elapsed"]]
source(file.path(enum, "lowp_enum.R"), local = FALSE)
key <- lowp_load(core)                                 # vendor hash check against the core's headers, then compile
L <- c(L, sprintf("enumerator compile+load: %.1f s; key %s; cache %s", proc.time()[["elapsed"]] - t0, substr(key, 1, 16), Sys.getenv("LOWP_ENUM_CACHE", "(tempdir)")),
       "vendored headers equal the core's headers (checked by lowp_load): yes")
for (f in c("cpp/Makevars.v3")) L <- c(L, sprintf("%s: %s", f, paste(readLines(file.path(core, f))[!grepl("^#", readLines(file.path(core, f)))], collapse = " ; ")))
L <- c(L, sprintf("Makevars.lowp: %s", paste(readLines(file.path(enum, "Makevars.lowp"))[!grepl("^#", readLines(file.path(enum, "Makevars.lowp")))], collapse = " ; ")))
writeLines(L, file.path(out, "BUILD_REPORT.txt")); cat(paste(L, collapse = "\n"), "\n")
