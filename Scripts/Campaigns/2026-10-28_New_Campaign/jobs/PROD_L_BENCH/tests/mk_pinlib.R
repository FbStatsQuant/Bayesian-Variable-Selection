# mk_pinlib.R DIR pkg=version ... -- test helper (HQ D82): a throwaway R library of metadata-only packages (DESCRIPTION + Meta/package.rds, no code),
# enough for packageVersion(), installed.packages() and find.package(). DIR must not exist.
a <- commandArgs(TRUE); dir <- a[[1L]]
if (file.exists(dir)) stop("exists: ", dir)
dir.create(dir, recursive = TRUE)
for (kv in a[-1L]) {
  pkg <- sub("=.*", "", kv); ver <- sub("^[^=]*=", "", kv)
  d <- file.path(dir, pkg); dir.create(file.path(d, "Meta"), recursive = TRUE)
  built <- paste0("R ", getRversion(), "; ; 2026-11-02 00:00:00 UTC; windows")
  desc <- c(Package = pkg, Version = ver, Title = "pin stub", License = "none", Built = built)
  write.dcf(t(desc), file.path(d, "DESCRIPTION"))
  saveRDS(list(DESCRIPTION = desc, Built = list(R = getRversion(), Platform = "", Date = "2026-11-02 00:00:00 UTC", OStype = "windows")),
          file.path(d, "Meta", "package.rds"))
}
cat("pinlib", dir, length(a) - 1L, "packages\n")
