# check_frozen_calls.R -- HQ D82 static check: every call from bundle R code into a function DEFINED in the frozen code tree must match that
# function's formals (match.call), so an argument name the frozen code does not have (e.g. test_library= for test_versions=) is caught before NOTS.
#   Rscript check_frozen_calls.R <frozen code dir (code/bench_lowp)> <bundle R file> [<bundle R file> ...]
# Prints one line per checked call ("OK|BAD <file>:<line> <call>") and a final "checked=<n> bad=<m>"; exit 0 iff m == 0 and n >= 1 when any frozen
# name is called. Calls are found by walking the parse tree: plain f(...) and x$...$f(...) heads whose last name is a frozen function. A name the
# bundle file itself defines as a function is skipped (local helper, not a frozen call). A frozen name defined more than once (e.g.
# assert_pkg_version in several production_helpers) passes if the call matches ANY definition.
args <- commandArgs(TRUE)
if (length(args) < 2L) { message("usage: check_frozen_calls.R FROZEN_DIR FILE..."); quit(save = "no", status = 64L) }
frozen <- args[[1L]]; files <- args[-1L]
is_fun_assign <- function(e) is.call(e) && length(e) == 3L && as.character(e[[1L]])[1L] %in% c("<-", "=", "<<-") && is.name(e[[2L]]) &&
  is.call(e[[3L]]) && identical(e[[3L]][[1L]], as.name("function"))
defs <- list()
walk_defs <- function(e) {
  if (is_fun_assign(e)) { nm <- as.character(e[[2L]]); defs[[nm]] <<- c(defs[[nm]], list(eval(e[[3L]], baseenv()))) }
  if (is.call(e)) for (k in seq_along(e)) if (!is.null(e[[k]]) && !missing_arg(e[[k]])) walk_defs(e[[k]])
}
missing_arg <- function(x) is.name(x) && identical(as.character(x), "")
for (f in list.files(file.path(frozen, "R"), pattern = "[.][Rr]$", recursive = TRUE, full.names = TRUE)) for (e in parse(f, keep.source = FALSE)) walk_defs(e)
for (f in list.files(frozen, pattern = "[.][Rr]$", full.names = TRUE)) for (e in parse(f, keep.source = FALSE)) walk_defs(e)
if (!length(defs)) { message("no frozen function definitions found under ", frozen); quit(save = "no", status = 2L) }
checked <- 0L; bad <- 0L
head_name <- function(h) {
  if (is.name(h)) return(as.character(h))
  if (is.call(h) && as.character(h[[1L]])[1L] %in% c("$", "::", ":::") && is.name(h[[length(h)]])) return(as.character(h[[length(h)]]))
  NA_character_
}
for (f in files) {
  ex <- parse(f, keep.source = TRUE); sr <- attr(ex, "srcref")
  local_defs <- character(); collect <- function(e) { if (is_fun_assign(e)) local_defs <<- c(local_defs, as.character(e[[2L]]))
    if (is.call(e)) for (k in seq_along(e)) if (!is.null(e[[k]]) && !missing_arg(e[[k]])) collect(e[[k]]) }
  for (e in ex) collect(e)
  visit <- function(e, line) {
    if (!is.call(e)) return(invisible())
    nm <- head_name(e[[1L]])
    if (!is.na(nm) && nm %in% names(defs) && !(nm %in% local_defs)) {
      ok <- FALSE; err <- ""
      for (d in defs[[nm]]) { r <- tryCatch({ match.call(d, e); TRUE }, error = function(z) { err <<- conditionMessage(z); FALSE }); if (r) { ok <- TRUE; break } }
      checked <<- checked + 1L; if (!ok) bad <<- bad + 1L
      cat(if (ok) "OK " else "BAD", " ", basename(f), ":", line, " ", paste(deparse(e, width.cutoff = 500L), collapse = " "), if (!ok) paste0("  -- ", err), "\n", sep = "")
    }
    for (k in seq_along(e)) if (!is.null(e[[k]]) && !missing_arg(e[[k]])) visit(e[[k]], line)
  }
  for (i in seq_along(ex)) visit(ex[[i]], if (!is.null(sr)) sr[[i]][1L] else NA)
}
cat("checked=", checked, " bad=", bad, "\n", sep = "")
quit(save = "no", status = if (bad == 0L) 0L else 1L)
