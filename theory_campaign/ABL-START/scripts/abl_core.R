# abl_core.R -- load the PRODUCTION v3 core plus the ABL-START test-only export (pattern of METH-AUDIT's ma_core.R).
# Copies Scripts/SMC_BVS/core to $ABL_WORK/core_abl (outside git), verifies every file against core/source_manifest.json,
# appends abl_exports.cpp to the COPY of cpp/v3_core.cpp, and sources the copy's v3.R.
local({
  this <- NA_character_
  for (fr in rev(sys.frames())) if (!is.null(fr$ofile)) { this <- normalizePath(fr$ofile); break }
  sd <- if (!is.na(this)) dirname(this) else getwd()
  assign("ABL_SCRIPTS", sd, envir = globalenv())
  assign("ABL_REPO", normalizePath(file.path(sd, "..", "..", "..")), envir = globalenv())
})
ABL_WORK <- Sys.getenv("ABL_WORK", "/home/fb31/abl_work")
abl_load <- function(work = ABL_WORK) {
  src <- file.path(ABL_REPO, "Scripts", "SMC_BVS", "core")
  man <- jsonlite::fromJSON(file.path(src, "source_manifest.json"))$production_source
  dst <- file.path(work, "core_abl"); addon <- file.path(ABL_SCRIPTS, "abl_exports.cpp")
  key <- digest::digest(c(vapply(names(man), function(f) man[[f]]$sha256, ""),
                          digest::digest(file = addon, algo = "sha256")), algo = "sha256")
  stamp <- file.path(dst, paste0("ABL_READY_", substr(key, 1, 16)))
  if (!file.exists(stamp)) {
    lock <- paste0(dst, ".lock")
    while (!dir.create(lock, showWarnings = FALSE)) Sys.sleep(2)
    on.exit(unlink(lock, recursive = TRUE))
    if (!file.exists(stamp)) {
      unlink(dst, recursive = TRUE); dir.create(file.path(dst, "cpp"), recursive = TRUE)
      for (f in names(man)) {
        ok <- file.copy(file.path(src, f), file.path(dst, f), overwrite = TRUE)
        h <- digest::digest(file = file.path(dst, f), algo = "sha256")
        if (!ok || !identical(h, man[[f]]$sha256)) stop("production source hash mismatch: ", f)
      }
      core_cpp <- file.path(dst, "cpp", "v3_core.cpp")
      writeLines(c(readLines(core_cpp), readLines(addon)), core_cpp)
      writeLines(key, stamp)
    }
  }
  source(file.path(dst, "v3.R"))
  invisible(dst)
}

# Arm-specific setup with the production interface (class v3_setup), used in place of v3_setup inside v3_fit.
# mode: 0 = A (production), 1 = B (blocks of size 1), 2 = C (prior), 3 = D (production blocks, supplied log r tables).
abl_setup <- function(ctx, mode, logr = NULL) {
  b <- v3_budgets(ctx$n, ctx$p)
  r <- .v3cpp$cpp_abl_setup(ctx, as.integer(b$B), as.integer(mode), logr)
  start <- r$start; start$ptr <- r$ptr; class(start) <- "v3_start"
  names(r$neighbours) <- ctx$orig
  structure(list(ptr = r$ptr, ctx = ctx, budgets = b, B = b$B, B_start = r$B_start, mode = mode, blocks = r$blocks,
                 tables = r$tables, start = start, neighbours = r$neighbours, seconds = r$seconds), class = "v3_setup")
}
