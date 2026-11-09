# proto_load.R -- load the O-LS0 prototype integration (reference for the merged-LS0 replay, SPEC section 6 item 2):
# a testing copy of the OLD production core with the O-LS0 test exports (o_ls0_exports.cpp = verbatim
# `git show origin/theory/O-LS0:theory_campaign/O-LS0/scripts/ls0_exports.cpp`) appended, and v3_final_run replaced as
# in ls0_core.R::ls0_enable_integrated (production final run + LS0 after the final local search, same ledger/cache).
proto_load <- function(core_src, work_dir) {
  if (dir.exists(work_dir)) unlink(work_dir, recursive = TRUE)
  dir.create(file.path(work_dir, "cpp"), recursive = TRUE)
  for (f in list.files(core_src, pattern = "[.]R$")) file.copy(file.path(core_src, f), file.path(work_dir, f))
  for (f in list.files(file.path(core_src, "cpp"))) file.copy(file.path(core_src, "cpp", f), file.path(work_dir, "cpp", f))
  core_cpp <- file.path(work_dir, "cpp", "v3_core.cpp")
  writeLines(c(readLines(core_cpp), readLines(file.path(CENG_TESTS, "o_ls0_exports.cpp"))), core_cpp)
  source(file.path(work_dir, "v3.R"))
  # verbatim body of ls0_core.R::ls0_enable_integrated (origin/theory/O-LS0)
  assign("v3_final_run", function(setup, frozen, seed, runtime = NULL) {
    stopifnot(inherits(setup, "v3_setup"), inherits(frozen, "v3_frozen"))
    v3_check_grid(frozen[["grid"]]); v3_check_seed(seed)
    ro <- v3_run_settings(setup, frozen)
    raw <- .v3cpp$cpp_final_run_ls0(setup$ptr, frozen[["grid"]], ro, as.numeric(seed), frozen[["inherited"]], runtime)
    out <- v3_assemble_final(raw, setup, frozen, ro, seed)
    out$ls0 <- raw$ls0; out$hpm_before_ls0 <- raw$hpm_before_ls0; out$start_mode <- raw$start_mode
    out$seconds_ls0 <- raw$seconds_ls0
    out
  }, envir = globalenv())
  invisible(work_dir)
}
