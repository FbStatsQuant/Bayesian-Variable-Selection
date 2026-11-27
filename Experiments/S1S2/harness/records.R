# records.R -- read run records with the identity checks shared by aggregate.R and paired.R. No statistical content.
# A method folder holds <setting>/rep_RRR.json (+ .rds). Only those exact paths are read: never _superseded/ (pull_to_owls.sh
# --backup-dir) or any audit folder, and a root inside one is refused. Errors (stop) on:
#   - a json whose setting_id or rep (or method, when present) differs from its path;
#   - two jsons for one (setting, rep) in a folder (rep_12.json next to rep_012.json) or a non-canonical name.
# An unreadable json reads as list(status = "failed: unreadable") (a failed record), as aggregate.R always did.
suppressPackageStartupMessages(library(jsonlite))
if (!exists("%||%")) `%||%` <- function(a, b) if (is.null(a)) b else a

rec_guard_root <- function(path) {
  if (grepl("(^|/)(_superseded|[^/]*audit[^/]*)(/|$)", normalizePath(path, mustWork = FALSE), ignore.case = TRUE))
    stop("records root lies in a _superseded or audit folder: ", path)
  invisible(path)
}
rec_file <- function(mdir, s, r) file.path(mdir, s, sprintf("rep_%03d.json", r))
.rec_checked <- new.env()
rec_check_dups <- function(d) {
  if (!is.null(.rec_checked[[d]]) || !dir.exists(d)) return(invisible())
  f <- list.files(d, pattern = "^rep_[0-9]+\\.json$")          # top level only: never descends into sub-folders
  k <- as.integer(sub("^rep_([0-9]+)\\.json$", "\\1", f))
  if (anyDuplicated(k)) stop(sprintf("duplicate records in %s: %s", d, paste(f[k %in% k[duplicated(k)]], collapse = ", ")))
  if (any(f != sprintf("rep_%03d.json", k))) stop(sprintf("non-canonical record names in %s: %s", d, paste(f[f != sprintf("rep_%03d.json", k)], collapse = ", ")))
  assign(d, TRUE, envir = .rec_checked)
}
# mdir = the method folder (e.g. runs/S1S2/lasso_cv); m = the method name the records must carry
rec_read <- function(mdir, m, s, r, simplify = FALSE) {
  rec_check_dups(file.path(mdir, s)); f <- rec_file(mdir, s, r)
  x <- tryCatch(fromJSON(f, simplifyVector = simplify), error = function(e) NULL)
  if (is.null(x)) return(list(status = "failed: unreadable"))
  bad <- c(if (!identical(as.character(x$setting_id %||% NA), s)) sprintf("setting_id %s", x$setting_id %||% "NULL"),
           if (!identical(suppressWarnings(as.integer(x$rep %||% NA)), as.integer(r))) sprintf("rep %s", x$rep %||% "NULL"),
           if (!is.null(x$method) && !identical(as.character(x$method), m)) sprintf("method %s", x$method))
  if (length(bad)) stop(sprintf("record identity mismatch: %s has %s", f, paste(bad, collapse = ", ")))
  x
}
# TP / FP / FN / exact of an ok record from selected vs support, checked against the record's own fields (stop if not)
rec_ivec <- function(x) if (is.null(x) || !length(x)) integer(0) else as.integer(unlist(x))
rec_confusion <- function(x, f) {
  sel <- rec_ivec(x$selected); sup <- rec_ivec(x$support)
  re <- c(TP = length(intersect(sel, sup)), FP = length(setdiff(sel, sup)), FN = length(setdiff(sup, sel)))
  own <- suppressWarnings(as.numeric(c(x$TP %||% NA, x$FP %||% NA, x$FN %||% NA)))
  if (!length(sup) || !isTRUE(all(own == re)) || isTRUE(x$success) != (re[["FP"]] + re[["FN"]] == 0))
    stop(sprintf("TP/FP/FN/success fields disagree with selected vs support in %s", f))
  c(re, n_selected = length(sel))
}
rec_F1 <- function(TP, FP, FN) ifelse(2 * TP + FP + FN > 0, 2 * TP / (2 * TP + FP + FN), 1)
