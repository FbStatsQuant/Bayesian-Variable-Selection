# md5_index.R -- reference index of the SMC-BVS data identities: one row per (suite, setting_id, rep) with the record's
# data_md5 (md5 of list(X, y), harness/run_one.R). The benchmark checks (slurm/check_bench.sh) compare every benchmark
# record with it, so NOTS scratch can be freed once the SMC-BVS batches are offloaded. OURS (operational).
#   Rscript harness/md5_index.R --roots DIR[,DIR...] --dest FILE [--require-r 4.5.2]
# Each root is a runs directory holding smcbvs/S1_xx/rep_RRR.json and/or smcbvs/S2_xxx/rep_RRR.json (only those setting
# folders are read; _superseded/, _manifests/ and any other folder are ignored). A json enters the index only if
#   - it carries a data_md5 (timeout stubs written by the sbatch do not; their reps stay out and the check falls back to
#     the live json),
#   - its setting_id and rep fields match its path (else: error),
#   - its R_version contains --require-r (default 4.5.2 = NOTS; an Owls smoke record, R 4.6.0, would carry a different
#     md5 for the same data; such records are skipped with a warning).
# The same key in two roots must carry the same md5 (else: error). Output: tsv suite, setting_id, rep, data_md5,
# R_version, source_root; sorted; written via tmp + rename.
suppressPackageStartupMessages(library(jsonlite))
a <- commandArgs(TRUE); opt <- list(`require-r` = "4.5.2")
if (length(a)) for (i in seq(1, length(a), by = 2)) opt[[sub("^--", "", a[i])]] <- a[i + 1]
if (is.null(opt$roots) || is.null(opt$dest)) stop("usage: --roots DIR[,DIR...] --dest FILE [--require-r 4.5.2]")
rows <- list(); skipped_r <- 0L; no_md5 <- 0L
for (root in strsplit(opt$roots, ",")[[1]]) {
  sdirs <- list.files(file.path(root, "smcbvs"), pattern = "^S(1_[0-9]{2}|2_[0-9]{3})$", full.names = TRUE)
  for (sd in sdirs) {
    fs <- list.files(sd, pattern = "^rep_[0-9]{3}\\.json$", full.names = TRUE)
    for (f in fs) {
      j <- fromJSON(f, simplifyVector = FALSE)
      sid <- basename(sd); rp <- as.integer(sub("^rep_([0-9]{3})\\.json$", "\\1", basename(f)))
      if (!identical(j$setting_id, sid) || !identical(as.integer(j$rep), rp)) stop("record fields do not match the path: ", f)
      if (is.null(j$data_md5)) { no_md5 <- no_md5 + 1L; next }
      if (!grepl(opt$`require-r`, j$R_version %||% "", fixed = TRUE)) { skipped_r <- skipped_r + 1L; next }
      rows[[length(rows) + 1]] <- data.frame(suite = as.integer(substr(sid, 2, 2)), setting_id = sid, rep = rp,
                                             data_md5 = j$data_md5, R_version = j$R_version, source_root = root, stringsAsFactors = FALSE)
    }
  }
}
if (!length(rows)) stop("no records found under ", opt$roots)
D <- do.call(rbind, rows)
key <- paste(D$setting_id, D$rep)
conf <- tapply(D$data_md5, key, function(v) length(unique(v)) > 1)
if (any(conf)) stop("conflicting data_md5 between roots for: ", paste(head(names(conf)[conf], 10), collapse = ", "))
D <- D[!duplicated(key), ]
D <- D[order(D$suite, D$setting_id, D$rep), ]
tmp <- paste0(opt$dest, ".tmp")
write.table(D, tmp, sep = "\t", quote = FALSE, row.names = FALSE)
invisible(file.rename(tmp, opt$dest))
cat(sprintf("md5 index: %d rows (S1 %d, S2 %d) -> %s; skipped: %d without data_md5, %d not R %s\n", nrow(D), sum(D$suite == 1),
            sum(D$suite == 2), opt$dest, no_md5, skipped_r, opt$`require-r`))
if (skipped_r) warning(skipped_r, " records skipped: R_version does not contain ", opt$`require-r`)
