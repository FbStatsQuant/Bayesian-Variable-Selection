#!/usr/bin/env Rscript
args <- commandArgs(trailingOnly = TRUE)
opt <- function(k) { i <- match(k, args); if (is.na(i) || i == length(args)) NULL else args[[i + 1L]] }
study <- opt("--study"); out <- opt("--out")
if (is.null(study) || is.null(out)) { message("usage: --study DIR --out DIR"); quit(status=3) }
dir.create(out, recursive=TRUE, showWarnings=FALSE)
problems <- data.frame(dataset_id=character(), file=character(), issue=character(), expected=character(), actual=character())
add <- function(id="", file="", issue, expected="", actual="") {
  problems <<- rbind(problems, data.frame(dataset_id=id, file=file, issue=issue, expected=expected, actual=actual))
}
incomplete <- FALSE
manifest <- file.path(study, "manifests", "inputs_manifest_lowp.csv")
m <- tryCatch(read.csv(manifest, colClasses="character", check.names=FALSE), error=function(e) NULL)
if (!requireNamespace("digest", quietly=TRUE) || is.null(m) || !all(c("dataset_id","file","file_sha256") %in% names(m))) {
  incomplete <- TRUE; add(issue="manifest_or_digest_unavailable")
} else {
  if (nrow(m) != 1200L || anyNA(m[,c("dataset_id","file","file_sha256")]) ||
      anyDuplicated(m$dataset_id) || anyDuplicated(m$file) ||
      any(!grepl("^p(0020|0030)_S[1-6]_r[0-9]{3}$", m$dataset_id)) ||
      any(!grepl("^[0-9a-fA-F]{64}$", m$file_sha256))) {
    incomplete <- TRUE; add(issue="malformed_manifest")
  } else {
    for (i in seq_len(nrow(m))) {
      id <- m$dataset_id[i]; rel <- m$file[i]; expected <- paste0("inputs/", substr(id,1,5), "/", id, ".rds")
      if (!identical(rel, expected)) { add(id, rel, "wrong_manifest_path", expected, rel); next }
      f <- file.path(study, rel)
      if (!file.exists(f)) { add(id, rel, "missing"); next }
      h <- tryCatch(digest::digest(file=f, algo="sha256"), error=function(e) NA_character_)
      if (is.na(h)) { incomplete <- TRUE; add(id, rel, "unreadable") }
      else if (tolower(h) != tolower(m$file_sha256[i])) add(id, rel, "sha256", m$file_sha256[i], h)
    }
    actual <- list.files(file.path(study, "inputs"), recursive=TRUE, all.files=TRUE, no..=TRUE, include.dirs=FALSE)
    extras <- setdiff(paste0("inputs/", gsub("\\\\", "/", actual)), m$file)
    for (f in extras) add(file=f, issue="extra")
  }
}
status <- if (incomplete) "INCOMPLETE" else if (nrow(problems)) "MISMATCH" else "PASS"
write.csv(problems, file.path(out, "P0B_INPUTS_MISMATCH.csv"), row.names=FALSE, na="")
writeLines(c("# P0b input verification", "", paste0("Status: **", status, "**"), paste0("Manifest rows: ", if (is.null(m)) "unavailable" else nrow(m)), paste0("Issues: ", nrow(problems))), file.path(out, "P0B_INPUTS_REPORT.md"))
cat(status, "\n")
quit(save="no", status=if (incomplete) 3L else if (nrow(problems)) 1L else 0L)
