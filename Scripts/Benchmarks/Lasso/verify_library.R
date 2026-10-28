#!/usr/bin/env Rscript
# verify_library.R -- checks that every package listed in the frozen environment manifest is installed in the
# study library with exactly the listed version. Usage: Rscript --vanilla verify_library.R <lib> <environment_manifest.txt>
args <- commandArgs(trailingOnly = TRUE); lib <- args[[1]]; man <- args[[2]]
x <- readLines(man)
rows <- regmatches(x, regexec("^([^[:space:]]+)[[:space:]]+([^[:space:]]+)[[:space:]]+[^[:space:]]+[.]tar[.]gz[[:space:]]+[0-9a-f]{64}[[:space:]]*$", x))
rows <- do.call(rbind, lapply(rows[lengths(rows) == 3L], function(r) r[2:3]))
if (is.null(rows) || nrow(rows) < 10L) stop("could not parse the package inventory: ", man)
bad <- character()
for (i in seq_len(nrow(rows))) {
  v <- tryCatch(utils::packageDescription(rows[i, 1], lib.loc = lib, fields = "Version"), error = function(e) NA)
  if (is.na(v) || !identical(v, rows[i, 2])) bad <- c(bad, sprintf("%s: installed %s, inventory %s", rows[i, 1], v, rows[i, 2]))
}
if (length(bad)) { cat("LIBRARY MISMATCH\n", paste(bad, collapse = "\n"), "\n", sep = ""); quit(status = 1L) }
cat(sprintf("library verified: %d packages match %s\n", nrow(rows), man))
