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
  for (mid in c("F1", "F2", "F3", "F4", "F5", "A1", "A2", "A3")) {
    mod <- lowp_load_method(mid, code, p=20, test_library=FALSE)
    pins <- if (mid == "A3") mod$settings$A3$PKG_VERSIONS else setNames(mod$registry$pkg_version, mod$registry$package)
    for (pkg in names(pins)) mod$env$assert_pkg_version(pkg, unname(pins[[pkg]]))
  }
  cat("PASS benchmark environment\n")
}
status <- tryCatch({ main(args); 0L }, error=function(e) { message("FAIL: ", conditionMessage(e)); 1L })
quit(save="no", status=status)
