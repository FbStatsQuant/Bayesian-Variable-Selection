# compare_versions.R: cell-by-cell diff of two table folders (old vs new version), thread S, 2026-10-22.
# Usage: Rscript --vanilla compare_versions.R --old <dir> --new <dir> --out <prefix>
# Compares every CSV and MD file at the folder root and under runs/<run_id>/ (hash files excluded).
# A CSV cell change is "allowed" only if it is the k_gt_K fix: column k_gt_K or n_k_gt_K, method F1-F3,
# rule cv_min or cv_1se, old value NA, new value a count. Everything else is "other" (a finding).
# Writes <prefix>_cells.csv (every differing cell), <prefix>_md.txt (differing MD lines), <prefix>_summary.txt.

a <- commandArgs(TRUE); get <- function(k) a[which(a == k) + 1]
old <- get("--old"); new <- get("--new"); prefix <- get("--out")

rel_files <- function(root) {
  f <- c(list.files(root, pattern = "\\.(csv|md)$"),
         file.path("runs", list.files(file.path(root, "runs"), recursive = TRUE, pattern = "\\.(csv|md)$")))
  f[!grepl("runs/$", f) & file.exists(file.path(root, f))]
}
f_old <- rel_files(old); f_new <- rel_files(new)
cells <- list(); md <- character(0); notes <- character(0)
for (f in setdiff(f_old, f_new)) notes <- c(notes, paste("only in old:", f))
for (f in setdiff(f_new, f_old)) notes <- c(notes, paste("only in new:", f))
n_csv <- 0; n_md <- 0
for (f in intersect(f_old, f_new)) {
  if (grepl("\\.md$", f)) {
    lo <- readLines(file.path(old, f), warn = FALSE); ln <- readLines(file.path(new, f), warn = FALSE)
    n_md <- n_md + 1
    if (!identical(lo, ln)) {
      d_old <- setdiff(lo, ln); d_new <- setdiff(ln, lo)
      md <- c(md, paste0("== ", f, " (", length(d_old), " lines only in old, ", length(d_new), " only in new)"),
              paste0("- ", d_old), paste0("+ ", d_new))
    }
    next
  }
  n_csv <- n_csv + 1
  x <- utils::read.csv(file.path(old, f), colClasses = "character", na.strings = "NA", check.names = FALSE)
  y <- utils::read.csv(file.path(new, f), colClasses = "character", na.strings = "NA", check.names = FALSE)
  if (!identical(names(x), names(y)) || nrow(x) != nrow(y)) {
    notes <- c(notes, sprintf("structure differs: %s (old %d x %d, new %d x %d)", f, nrow(x), ncol(x), nrow(y), ncol(y)))
    next
  }
  for (cc in names(x)) {
    bad <- unname(which(!mapply(identical, x[[cc]], y[[cc]], USE.NAMES = FALSE)))
    if (!length(bad)) next
    key <- function(col) if (col %in% names(x)) x[[col]][bad] else NA_character_
    allowed <- cc %in% c("k_gt_K", "n_k_gt_K") & key("method_id") %in% c("F1", "F2", "F3") &
               key("rule_id") %in% c("cv_min", "cv_1se") & is.na(x[[cc]][bad]) & !is.na(y[[cc]][bad])
    cells[[length(cells) + 1]] <- data.frame(file = f, row = bad, run_id = key("run_id"), method_id = key("method_id"),
                                             rule_id = key("rule_id"), p = key("p"), scenario = key("scenario"),
                                             column = cc, old = x[[cc]][bad], new = y[[cc]][bad],
                                             class = ifelse(allowed, "allowed_k_gt_K_fix", "other"), stringsAsFactors = FALSE)
  }
}
cells <- if (length(cells)) do.call(rbind, cells) else
  data.frame(file = character(0), row = integer(0), run_id = character(0), method_id = character(0), rule_id = character(0),
             p = character(0), scenario = character(0), column = character(0), old = character(0), new = character(0), class = character(0))
utils::write.csv(cells, paste0(prefix, "_cells.csv"), row.names = FALSE)
writeLines(md, paste0(prefix, "_md.txt"))
al <- cells[cells$class == "allowed_k_gt_K_fix", ]
keys <- unique(paste(ifelse(is.na(al$run_id), basename(dirname(al$file)), al$run_id), al$method_id, al$rule_id, al$p, al$scenario, sep = "|"))
summ <- c(paste("old:", old), paste("new:", new),
          paste("files compared: csv", n_csv, "| md", n_md),
          paste("differing csv cells:", nrow(cells), "| allowed (k_gt_K fix):", nrow(al), "| other:", sum(cells$class == "other")),
          paste("distinct allowed keys (run|method|rule|p|scenario):", length(keys)),
          paste("allowed cells by file:", paste(names(table(al$file)), table(al$file), sep = "=", collapse = " ")),
          paste("other cells by file/column:", if (any(cells$class == "other"))
            paste(names(table(paste(cells$file, cells$column)[cells$class == "other"])), table(paste(cells$file, cells$column)[cells$class == "other"]), sep = "=", collapse = " ") else "none"),
          paste("md files with differing lines:", sum(grepl("^== ", md))), notes)
writeLines(summ, paste0(prefix, "_summary.txt"))
cat(summ, sep = "\n")
