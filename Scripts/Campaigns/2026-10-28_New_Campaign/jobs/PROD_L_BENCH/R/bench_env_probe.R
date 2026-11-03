args <- commandArgs(TRUE)
main <- function(args) {
  opt <- list(); i <- 1L
  while (i <= length(args)) {
    k <- args[[i]]
    if (k == "--local-test") { opt[[k]] <- TRUE; i <- i + 1L; next }
    if (!k %in% c("--code", "--library") || !is.null(opt[[k]]) || i == length(args)) stop("Invalid argument: ", k)
    opt[[k]] <- args[[i + 1L]]; i <- i + 2L
  }
  if (is.null(opt[["--code"]]) || is.null(opt[["--library"]])) stop("--code and --library required")
  if (!isTRUE(opt[["--local-test"]]) && as.character(getRversion()) != "4.5.2") stop("R 4.5.2 required")
  code <- normalizePath(opt[["--code"]], winslash="/", mustWork=TRUE)
  lib <- normalizePath(opt[["--library"]], winslash="/", mustWork=TRUE)
  if (!dir.exists(lib) || file.access(lib, 4L) != 0L) stop("Library is not readable")
  .libPaths(c(lib, .libPaths()))
  source(file.path(code, "R", "config_lowp.R")); source(file.path(code, "R", "common.R"))
  pinned <- character()
  for (mid in c("F1", "F2", "F3", "F4", "F5", "A1", "A2", "A3")) {
    # frozen signature (code/bench_lowp/R/common.R:2): lowp_load_method(id, code_dir, p, test_versions = FALSE). HQ D82: the earlier
    # keyword test_library= does not exist there and stopped s0_verify (job 2510090); test_versions = FALSE keeps the strict pin check.
    mod <- lowp_load_method(mid, code, p=20, test_versions=FALSE)
    pins <- if (mid == "A3") mod$settings$A3$PKG_VERSIONS else setNames(mod$registry$pkg_version, mod$registry$package)
    for (pkg in names(pins)) mod$env$assert_pkg_version(pkg, unname(pins[[pkg]]))
    pinned <- c(pinned, names(pins))
  }
  # HQ D82 test PR08: a pin satisfied by a package OUTSIDE the pinned library passed the version check. Same location rule as the frozen CLI
  # (run_bench_case.R, "Package outside sealed library"): every pinned package, digest, and their installed dependency closure must resolve inside
  # the pinned library, except base/recommended packages of .Library.
  db <- utils::installed.packages()
  deps <- unique(c(pinned, "digest", unlist(tools::package_dependencies(c(pinned, "digest"), db = db, recursive = TRUE))))
  for (pkg in c(pinned, "digest")) if (!pkg %in% rownames(db)) stop("Package missing: ", pkg)
  base_lib <- normalizePath(.Library, winslash = "/", mustWork = TRUE)
  for (pkg in sort(intersect(deps, rownames(db)))) {
    loc <- normalizePath(find.package(pkg), winslash = "/", mustWork = TRUE); dir <- normalizePath(dirname(loc), winslash = "/")
    is_base <- identical(dir, base_lib) && db[pkg, "Priority"] %in% c("base", "recommended")
    if (!is_base && !identical(dir, lib)) stop("Package outside sealed library: ", pkg, " ", loc)
  }
  cat("PASS benchmark environment\n")
}
status <- tryCatch({ main(args); 0L }, error=function(e) { message("FAIL: ", conditionMessage(e)); 1L })
quit(save="no", status=status)
