# v3.R -- entry point of the SMC-BVS v3 core layer (CORE_SPEC v2 §§0-9) and calibration layer (§10).
# Usage:  source("<core dir>/v3.R")
# Sources the R files of this directory and compiles the C++ (cpp/v3_core.cpp and its headers) with Rcpp::sourceCpp.
# The compiled code is cached in .cpp_cache/<hash of all C++ sources and Makevars.v3>/, so any edit of a header forces
# a rebuild (sourceCpp's own cache only watches the .cpp file).
#
# Concurrency (many Slurm tasks sourcing v3.R at once): the shared cache is written by exactly one process, under an
# atomic lock (mkdir of <cache>.lock), and marked complete by a READY file. Every process, the builder included, then
# loads from its own private copy of the cache in tempdir(), so no process ever reads the shared sourceCpp index while
# another writes it (sourceCpp rewrites its index on every call). Waiting processes poll for READY; a lock older than
# 2 h without READY is treated as stale (crashed builder) and removed.

local({
  this_file <- NA_character_
  for (fr in rev(sys.frames())) if (!is.null(fr$ofile)) { this_file <- normalizePath(fr$ofile); break }  # innermost source()
  dir <- if (!is.na(this_file)) dirname(this_file) else
    Sys.getenv("V3_CORE_DIR", path.expand("~/smcbvs_v3_deploy_20261022/A_build/code/core"))
  assign("V3_CORE_DIR", dir, envir = globalenv())
})

v3_compile <- function(dir = V3_CORE_DIR, quiet = TRUE, wait_seconds = 3600) {
  cppdir <- file.path(dir, "cpp")
  cppfile <- file.path(cppdir, "v3_core.cpp")
  srcs <- sort(list.files(cppdir, pattern = "\\.(h|cpp|v3)$", full.names = TRUE))   # sources and Makevars.v3
  key <- digest::digest(paste(vapply(srcs, function(f) digest::digest(file = f, algo = "sha256"), ""), collapse = ""),
                        algo = "sha256", serialize = FALSE)
  shared <- file.path(dir, ".cpp_cache", substr(key, 1, 16))
  ready <- file.path(shared, "READY")
  old <- Sys.getenv(c("PKG_CPPFLAGS", "R_MAKEVARS_USER"), unset = NA)
  Sys.setenv(PKG_CPPFLAGS = paste0("-I", cppdir))                    # headers live next to v3_core.cpp
  Sys.setenv(R_MAKEVARS_USER = file.path(cppdir, "Makevars.v3"))     # pinned compiler flags (see cpp/Makevars.v3)
  on.exit(for (k in names(old)) if (is.na(old[[k]])) Sys.unsetenv(k) else do.call(Sys.setenv, setNames(list(old[[k]]), k)), add = TRUE)
  # 1. build the shared cache once (one process under the lock; the others wait for READY)
  if (!file.exists(ready)) {
    dir.create(dirname(shared), recursive = TRUE, showWarnings = FALSE)
    lock <- paste0(shared, ".lock")
    t0 <- Sys.time()
    repeat {
      if (file.exists(ready)) break
      if (dir.create(lock, showWarnings = FALSE)) {                  # atomic: exactly one process succeeds
        ok <- FALSE
        tryCatch({
          if (!file.exists(ready)) {
            unlink(shared, recursive = TRUE)                         # remove a partial cache left by a crashed builder
            dir.create(shared, recursive = TRUE, showWarnings = FALSE)
            Rcpp::sourceCpp(cppfile, env = new.env(), cacheDir = shared, showOutput = !quiet, verbose = FALSE)
            writeLines(key, file.path(shared, "READY.tmp")); file.rename(file.path(shared, "READY.tmp"), ready)
          }
          ok <- TRUE
        }, finally = unlink(lock, recursive = TRUE))
        if (ok) break
      }
      info <- file.info(lock)
      if (!is.na(info$mtime) && difftime(Sys.time(), info$mtime, units = "secs") > 7200) unlink(lock, recursive = TRUE)
      if (difftime(Sys.time(), t0, units = "secs") > wait_seconds) stop("v3_compile: timed out waiting for the build lock ", lock)
      Sys.sleep(2)
    }
  }
  # 2. load from a private copy of the shared cache (read-only use of the shared directory)
  priv <- file.path(tempdir(), paste0("v3cpp_", substr(key, 1, 16)))
  if (!file.exists(file.path(priv, "READY"))) {
    unlink(priv, recursive = TRUE); dir.create(priv, recursive = TRUE)
    ok <- file.copy(list.files(shared, full.names = TRUE, all.files = TRUE, no.. = TRUE), priv, recursive = TRUE, copy.date = TRUE)
    if (!all(ok)) stop("v3_compile: could not copy the compiled cache to ", priv)
  }
  env <- new.env(parent = globalenv())
  Rcpp::sourceCpp(cppfile, env = env, cacheDir = priv, showOutput = !quiet, verbose = FALSE)
  assign(".v3cpp", env, envir = globalenv())
  invisible(key)
}

for (f in c("v3_preprocess.R", "v3_setup.R", "v3_run.R", "v3_exact.R", "v3_calib.R", "v3_fit.R"))
  source(file.path(V3_CORE_DIR, f), local = FALSE)
V3_CPP_KEY <- v3_compile()
