# ma_core.R -- load the PRODUCTION v3 core plus the METH-AUDIT test-only exports (pattern of O-LS0's ls0_core.R).
# Copies Scripts/SMC_BVS/core to $MA_WORK/core_ma (outside git), verifies every file against core/source_manifest.json,
# appends ma_exports.cpp to the COPY of cpp/v3_core.cpp, and sources the copy's v3.R.
local({
  this <- NA_character_
  for (fr in rev(sys.frames())) if (!is.null(fr$ofile)) { this <- normalizePath(fr$ofile); break }
  sd <- if (!is.na(this)) dirname(this) else getwd()
  assign("MA_SCRIPTS", sd, envir = globalenv())
  assign("MA_REPO", normalizePath(file.path(sd, "..", "..", "..")), envir = globalenv())
})
MA_WORK <- Sys.getenv("MA_WORK", "/home/fb31/ma_work")
ma_load <- function(work = MA_WORK) {
  src <- file.path(MA_REPO, "Scripts", "SMC_BVS", "core")
  man <- jsonlite::fromJSON(file.path(src, "source_manifest.json"))$production_source
  dst <- file.path(work, "core_ma"); addon <- file.path(MA_SCRIPTS, "ma_exports.cpp")
  key <- digest::digest(c(vapply(names(man), function(f) man[[f]]$sha256, ""),
                          digest::digest(file = addon, algo = "sha256")), algo = "sha256")
  stamp <- file.path(dst, paste0("MA_READY_", substr(key, 1, 16)))
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
  source(file.path(dst, "v3.R"))
  invisible(dst)
}
