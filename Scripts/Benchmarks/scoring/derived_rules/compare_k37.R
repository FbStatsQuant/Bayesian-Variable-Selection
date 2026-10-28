# compare_k37.R: compares this unit's ebic1_K37 rows with the existing, independently derived K37
# rows at c = 1 (outputs only; the other derivation's code is not read). Thread S, 2026-10-21.
# Usage: Rscript --vanilla compare_k37.R --mine <derived_rule_rows.csv> --theirs <csv> --out <dir> --tag <name>

parse_cli <- function(args) { out <- list(); for (i in seq(1, length(args), 2)) out[[sub("^--", "", args[i])]] <- args[i + 1]; out }
a <- parse_cli(commandArgs(TRUE))
mine <- utils::read.csv(a$mine, colClasses = "character", na.strings = "NA")
theirs <- utils::read.csv(a$theirs, colClasses = "character", na.strings = "NA")
mine <- mine[mine$rule_id == "ebic1_K37", ]
theirs <- theirs[theirs$rule_id == "ebic1_K37", ]
key_m <- paste(mine$case_id, mine$method_id); key_t <- paste(theirs$case_id, theirs$method_id)
stopifnot(!anyDuplicated(key_m), !anyDuplicated(key_t))

TEXT <- c("status", "support", "support_audit", "run_id", "case_id", "dataset_id", "method_id",
          "x_sha256", "y_sha256", "fold_sha256", "inputs_sha256", "source_sha256")
NUM_EXACT <- c("k", "k_valid_max", "data_seed", "fold_seed", "method_seed", "runtime_s")
NUM_TOL <- c("crit_value", "rss", "lambda")          # |a - b| <= 1e-9 * max(1, |a|)

common <- intersect(key_t, key_m)
j_m <- match(common, key_m); j_t <- match(common, key_t)
diffs <- list()
counts <- c()
for (cc in c(TEXT, NUM_EXACT, NUM_TOL)) {
  if (!(cc %in% names(mine)) || !(cc %in% names(theirs))) { counts[cc] <- NA; next }
  x <- mine[[cc]][j_m]; y <- theirs[[cc]][j_t]
  bad <- if (cc %in% TEXT) !mapply(identical, x, y) else {
    xn <- suppressWarnings(as.numeric(x)); yn <- suppressWarnings(as.numeric(y))
    both_na <- is.na(xn) & is.na(yn)
    tol <- if (cc %in% NUM_TOL) 1e-9 * pmax(1, abs(xn)) else 0
    !(both_na | (!is.na(xn) & !is.na(yn) & abs(xn - yn) <= tol))
  }
  counts[cc] <- sum(bad)
  if (any(bad)) diffs[[cc]] <- data.frame(key = common[bad], field = cc, mine = x[bad], theirs = y[bad], stringsAsFactors = FALSE)
}
equal_cases <- length(common) - length(unique(unlist(lapply(diffs, function(d) d$key[d$field %in% c("status", "support", "support_audit", "k")]))))
log <- c(paste("tag:", a$tag), paste("mine:", a$mine), paste("theirs:", a$theirs),
         paste("cases: mine", length(key_m), "| theirs", length(key_t), "| common", length(common),
               "| only mine", length(setdiff(key_m, key_t)), "| only theirs", length(setdiff(key_t, key_m))),
         paste("cases equal on status, support, support_audit and k:", equal_cases, "of", length(common)),
         paste("fields differing (cases):", paste(names(counts), counts, sep = "=", collapse = " ")))
dir.create(a$out, recursive = TRUE, showWarnings = FALSE)
writeLines(log, file.path(a$out, paste0("compare_K37_", a$tag, ".txt")))
utils::write.csv(if (length(diffs)) do.call(rbind, diffs) else data.frame(key = character(0), field = character(0), mine = character(0), theirs = character(0)),
                 file.path(a$out, paste0("compare_K37_", a$tag, "_diffs.csv")), row.names = FALSE)
cat(log, sep = "\n")
