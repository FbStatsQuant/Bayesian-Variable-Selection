# ls0_core.R -- load the PRODUCTION v3 core plus the O-LS0 test-only exports.
# 1. Copy Scripts/SMC_BVS/core (R files, cpp/ headers, Makevars.v3) to a testing copy outside git
#    ($LS0_WORK/core_ls0, default /home/fb31/ls0_work/core_ls0).
# 2. Verify every copied file against core/source_manifest.json "production_source" sha256 (abort on mismatch).
# 3. Append scripts/ls0_exports.cpp to the COPY of cpp/v3_core.cpp (production text above it unchanged).
# 4. source() the copy's v3.R: production preprocessing, budgets, blocks, tables, pi_0, scorer, local search, v3_fit.
# Defines: LS0_REPO, ls0_* helpers (start mode, standalone local search, pi_0(R_d), integrated final run).

local({
  this <- NA_character_
  for (fr in rev(sys.frames())) if (!is.null(fr$ofile)) { this <- normalizePath(fr$ofile); break }
  sd <- if (!is.na(this)) dirname(this) else getwd()
  assign("LS0_SCRIPTS", sd, envir = globalenv())
  assign("LS0_REPO", normalizePath(file.path(sd, "..", "..", "..")), envir = globalenv())
})
LS0_WORK <- Sys.getenv("LS0_WORK", "/home/fb31/ls0_work")

ls0_prepare_core <- function(work = LS0_WORK) {
  src <- file.path(LS0_REPO, "Scripts", "SMC_BVS", "core")
  man <- jsonlite::fromJSON(file.path(src, "source_manifest.json"))$production_source
  dst <- file.path(work, "core_ls0")
  addon <- file.path(LS0_SCRIPTS, "ls0_exports.cpp")
  key <- digest::digest(c(vapply(names(man), function(f) man[[f]]$sha256, ""),
                          digest::digest(file = addon, algo = "sha256")), algo = "sha256")
  stamp <- file.path(dst, paste0("LS0_READY_", substr(key, 1, 16)))
  if (file.exists(stamp)) return(invisible(dst))
  lock <- paste0(dst, ".lock")
  repeat { if (dir.create(lock, showWarnings = FALSE)) break; Sys.sleep(1); if (file.exists(stamp)) return(invisible(dst)) }
  on.exit(unlink(lock, recursive = TRUE), add = TRUE)
  if (file.exists(stamp)) return(invisible(dst))
  unlink(dst, recursive = TRUE); dir.create(file.path(dst, "cpp"), recursive = TRUE)
  for (f in names(man)) {
    ok <- file.copy(file.path(src, f), file.path(dst, f), overwrite = TRUE)
    h <- digest::digest(file = file.path(dst, f), algo = "sha256")
    if (!ok || !identical(h, man[[f]]$sha256)) stop("production source hash mismatch: ", f)
  }
  core_cpp <- file.path(dst, "cpp", "v3_core.cpp")
  writeLines(c(readLines(core_cpp), readLines(addon)), core_cpp)
  writeLines(key, stamp)
  invisible(dst)
}

ls0_load <- function(work = LS0_WORK) {
  dst <- ls0_prepare_core(work)
  source(file.path(dst, "v3.R"))
  invisible(dst)
}

# ---- helpers (all computation is in the production engine; these only call it) ----
ls0_start_mode <- function(setup) .v3cpp$cpp_ls0_start_mode(setup$ptr)
ls0_local_search <- function(setup, centre, ell, emit_centre = TRUE)
  .v3cpp$cpp_ls0_local_search(setup$ptr, as.integer(centre), as.integer(ell), isTRUE(emit_centre))
ls0_pi0_Rd <- function(setup, S0, d_max = 2L) .v3cpp$cpp_ls0_pi0_Rd(setup$ptr, as.integer(S0), as.integer(d_max))

# F(S) = log varpi(|S|) + log m(S) from the production scorer (v3_score)
ls0_F <- function(ctx, S) v3_score(ctx, as.integer(S))$F

# Integrated LS0 (step 5): replaces v3_final_run by a version that calls cpp_final_run_ls0 (production final run +
# LS0 after the final local search, same ledger/cache). v3_assemble_final (production) is reused unchanged; the LS0
# records are attached afterwards.
ls0_enable_integrated <- function() {
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
}
