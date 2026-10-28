# Test code only. Never source this from the production fit.
options(warn = 1)
need <- function(ok, message) if (!isTRUE(ok)) stop(message, call. = FALSE)
bits <- function(x) writeBin(as.double(x), raw(), size = 8L, endian = "little")
exact <- function(a, b, path = "root") {
  need(identical(typeof(a), typeof(b)), paste(path, "storage type differs"))
  # Attribute insertion order is not data. Compare every named attribute,
  # including dimensions, row names and storage classes, in canonical order.
  aa <- attributes(a); ab <- attributes(b)
  if (length(aa)) aa <- aa[order(names(aa))]
  if (length(ab)) ab <- ab[order(names(ab))]
  need(identical(aa, ab), paste(path, "attributes differ"))
  if (is.double(a)) {
    need(identical(bits(a), bits(b)), paste(path, "IEEE-754 bits differ"))
  } else if (is.list(a)) {
    need(length(a) == length(b), paste(path, "length differs"))
    for (i in seq_along(a)) exact(a[[i]], b[[i]], paste0(path, "/", names(a)[i] %||% i))
  } else need(identical(a, b), paste(path, "value differs"))
  invisible(TRUE)
}
`%||%` <- function(a, b) if (is.null(a)) b else a
# Deliberately narrow: only measured wall times are removed here. Intentional method
# changes are asserted separately; no broad regex removing arbitrary numeric fields.
without_times <- function(x) {
  if (!is.list(x) || is.data.frame(x)) return(x)
  x[c("seconds", "seconds_local", "seconds_total", "timings")] <- NULL
  lapply(x, without_times)
}
fixture <- function(id) {
  # Deterministic synthetic development data, no production data or truth files.
  n <- c(9L, 12L, 17L, 21L, 8L, 32L)[(id - 1L) %% 6L + 1L]
  p <- c(6L, 7L, 8L, 9L, 6L, 11L)[(id - 1L) %% 6L + 1L]
  X <- outer(seq_len(n), seq_len(p), function(i, j)
    sin((i + id) * (j + 1) * .37) + cos(i * (j + 2) * .19) + ((i * j + id) %% 7) / 11)
  if (id %% 3 == 0) X[, 3] <- -X[, 2]
  if (id %% 4 == 0) X[, 4] <- X[, 1] + 1e-10 * X[, 5]
  y <- X[, 1] * 1.7 - X[, 2] * .8 + sin(seq_len(n) * 1.23 + id)
  # Nonconsecutive original indices after exact-constant removal.
  X <- cbind(13, X[, 1:2], -7, X[, -(1:2), drop = FALSE])
  list(X = X, y = y)
}
sha_tree <- function(dir) {
  f <- sort(list.files(dir, recursive = TRUE, full.names = TRUE, all.files = TRUE, no.. = TRUE))
  f <- f[!file.info(f)$isdir & !grepl("/\\.cpp_cache/", gsub("\\\\", "/", f))]
  setNames(vapply(f, function(z) digest::digest(file = z, algo = "sha256"), ""), substring(f, nchar(dir) + 2L))
}
load_test_core <- function(core, work, testdir) {
  dir.create(work, recursive = TRUE, showWarnings = FALSE)
  cpp <- normalizePath(file.path(core, "cpp"), mustWork = TRUE)
  production <- file.exists(file.path(cpp, "v3_runtime.h"))
  wrapper_files <- file.path(testdir, "wrappers.cpp")
  extra_exports <- file.path(testdir, "v2_runtime_exports.h")
  if (production && file.exists(extra_exports)) wrapper_files <- c(wrapper_files, extra_exports)
  wrappers <- unlist(lapply(wrapper_files, readLines, warn = FALSE), use.names = FALSE)
  if (!production) wrappers <- wrappers[seq_len(match("// PRODUCTION_ONLY_WRAPPERS", wrappers) - 1L)]
  src <- sort(list.files(cpp, pattern = "\\.(h|cpp|v3)$", full.names = TRUE))
  identity <- list(source_sha256 = setNames(vapply(src, function(f) digest::digest(file=f, algo="sha256"), ""), basename(src)),
    wrappers = wrappers,
    wrapper_sha256 = setNames(vapply(wrapper_files, function(f) digest::digest(file=f, algo="sha256"), ""), basename(wrapper_files)),
    production = production, R = R.version.string, platform = R.version$platform,
    Rcpp = as.character(utils::packageVersion("Rcpp")),
    compiler = system2("g++", "--version", stdout = TRUE, stderr = TRUE),
    environment = Sys.getenv(c("CC", "CXX", "CXX11", "CXX14", "CXX17", "CXX20", "CPPFLAGS", "PKG_CPPFLAGS")))
  key <- digest::digest(identity, algo = "sha256")
  cache_root <- Sys.getenv("V3_TEST_COMPILE_CACHE", file.path(work, "shared_compile_cache"))
  shared <- file.path(cache_root, key); headers <- file.path(shared, "headers")
  tu <- file.path(shared, "test_core.cpp")
  if (!file.exists(tu)) {
    dir.create(headers, recursive = TRUE, showWarnings = FALSE)
    need(all(file.copy(src, headers, overwrite = FALSE)), "could not freeze test compile headers")
    writeLines(c(if (production) "#define TEST_PRODUCTION 1" else "#define TEST_PRODUCTION 0",
                 readLines(file.path(cpp, "v3_core.cpp"), warn = FALSE), wrappers), tu)
    saveRDS(identity, file.path(shared, "build_identity.rds"), version = 3)
  }
  # Stable TU and header paths allow sourceCpp reuse across every sequential seed.
  # The content hash includes every header, flags, wrappers, R/Rcpp and compiler.
  Sys.setenv(PKG_CPPFLAGS = paste0("-I", shQuote(normalizePath(headers))),
             R_MAKEVARS_USER = file.path(headers, "Makevars.v3"), MAKEFLAGS = "-j1")
  .v3cpp <<- new.env(parent = globalenv())
  Rcpp::sourceCpp(tu, env = .v3cpp, cacheDir = file.path(shared, "cache"), rebuild = FALSE, showOutput = TRUE)
  V3_TEST_BUILD_IDENTITY <<- list(key = key, directory = shared, identity = identity)
  saveRDS(V3_TEST_BUILD_IDENTITY, file.path(work, "compile_cache_identity.rds"), version = 3)
  # No v3.R: its cache would write into the read-only source tree.
  for (f in c("v3_preprocess.R", "v3_setup.R", "v3_run.R", "v3_exact.R", "v3_calib.R", "v3_fit.R"))
    source(file.path(core, f), local = globalenv())
  invisible(.v3cpp)
}
record <- function(label, expr) {
  t <- Sys.time()
  tryCatch({ value <- force(expr); list(test = label, ok = TRUE, utc = format(t, tz = "UTC", usetz = TRUE), value = value) },
    error = function(e) list(test = label, ok = FALSE, utc = format(t, tz = "UTC", usetz = TRUE), error = conditionMessage(e)))
}
