# ceng_load.R -- load a TESTING COPY of a v3 core with the C-ENG test-only exports appended.
# Usage: source("ceng_load.R"); ceng_load(core_src, work_dir, exports = TRUE, force_stop = NULL)
#   core_src   : directory of a core (R files, cpp/, Makevars.v3), e.g. Scripts/SMC_BVS/core
#   work_dir   : fresh directory for the testing copy (outside git)
#   exports    : append tests/ceng_exports.cpp to the copy's cpp/v3_core.cpp
#   force_stop : NULL, or a guard checkpoint name ("ls0", "local_search", ...). The COPY's RuntimeGuard::check then
#                reports "exceeded" at the first check with that checkpoint (test injection for GUARD-W; production
#                sources are never modified).
CENG_TESTS <- local({
  this <- NA_character_
  for (fr in rev(sys.frames())) if (!is.null(fr$ofile)) { this <- normalizePath(fr$ofile); break }
  if (is.na(this)) getwd() else dirname(this)
})

ceng_load <- function(core_src, work_dir, exports = TRUE, force_stop = NULL, reuse = FALSE) {
  core_src <- normalizePath(core_src)
  # reuse = TRUE: a testing copy prepared earlier (READY stamp) is loaded as is (parallel workers share one build)
  if (reuse && file.exists(file.path(work_dir, "CENG_READY"))) { source(file.path(work_dir, "v3.R")); return(invisible(work_dir)) }
  if (dir.exists(work_dir)) unlink(work_dir, recursive = TRUE)
  dir.create(file.path(work_dir, "cpp"), recursive = TRUE)
  for (f in list.files(core_src, pattern = "\\.R$")) file.copy(file.path(core_src, f), file.path(work_dir, f))
  for (f in list.files(file.path(core_src, "cpp"))) file.copy(file.path(core_src, "cpp", f), file.path(work_dir, "cpp", f))
  core_cpp <- file.path(work_dir, "cpp", "v3_core.cpp")
  if (exports) writeLines(c(readLines(core_cpp), readLines(file.path(CENG_TESTS, "ceng_exports.cpp"))), core_cpp)
  if (!is.null(force_stop)) {
    rt <- file.path(work_dir, "cpp", "v3_runtime.h")
    x <- readLines(rt)
    i <- grep("bool stop = now \\+ operation > allocation;", x, fixed = FALSE)
    stopifnot(length(i) == 1L)
    x[i] <- sprintf('    bool stop = (now + operation > allocation) || checkpoint == "%s";  // C-ENG TEST INJECTION', force_stop)
    writeLines(x, rt)
  }
  source(file.path(work_dir, "v3.R"))
  writeLines(core_src, file.path(work_dir, "CENG_READY"))
  invisible(work_dir)
}
