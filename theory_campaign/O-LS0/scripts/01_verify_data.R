# 01_verify_data.R -- byte-level checks of the generator pipeline against EVERY input-file hash stored in the repository.
# Per-dataset production manifests live on NOTS (inputs_manifest sha 1a42b919...), not in git. Stored in git are:
#  (A) two Owls dev inputs (C's dev inputs, R 4.6.0 on Owls): dev_p0500_S4_r001 = 2ba5c283..., dev_p1000_S4_r001 =
#      c4724d92... (Docs/Records/SMC_BVS_v3_deploy/NOTS_READINESS.md §5, prefixes only);
#  (B) four NOTS dev inputs (bench20261019/dev, R 4.5.2 on NOTS): full sha256 in
#      Scripts/Campaigns/2026-10-28_New_Campaign/code/bench_v2/review/checker/check3_results.csv (check3_recompute.R);
#  (C) one NOTS production input: p1000_S4_r001 = 6d4b8b5f... (NOTS_READINESS.md §7, the e2e fit).
# gen_prod_data.R reuses gen_dev_data.R's generator verbatim (only seeds/ids differ). Each dataset is generated in this
# process (BLAS = whatever the caller pinned; 00_regen_data.sh pins FlexiBLAS OPENBLAS-OPENMP, 1 thread), saved with
# saveRDS(compress = FALSE) as the generators do, and hashed with the XDR header's writer-R-version field (bytes 7-10)
# set to 4.6.0, 4.5.2, 4.5.1, 4.5.0, 4.4.1 (every other byte is data). Writes results/data_hash_check.csv.
# Usage: OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 Rscript 01_verify_data.R
repo <- system("git rev-parse --show-toplevel", intern = TRUE)
outdir <- file.path(dirname(normalizePath(sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)[1]))), "..", "results")
gd <- new.env(); sys.source(file.path(repo, "Scripts/Data_generators/gen_dev_data.R"), envir = gd)
src <- readLines(file.path(repo, "Scripts/Data_generators/gen_prod_data.R"))
src <- src[seq_len(grep("^main <- function", src) - 1L)]
src <- sub('sys.source(file.path(here(), "gen_dev_data.R"), envir = gen_dev_env)',
           sprintf('sys.source("%s", envir = gen_dev_env)', file.path(repo, "Scripts/Data_generators/gen_dev_data.R")), src, fixed = TRUE)
gp <- new.env(); eval(parse(text = src), envir = gp)
ck <- read.csv(file.path(repo, "Scripts/Campaigns/2026-10-28_New_Campaign/code/bench_v2/review/checker/check3_results.csv"))
ck <- ck[ck$check == "input sha matches RDS record", ]
targets <- rbind(
  data.frame(source = "A: Owls dev (NOTS_READINESS s5)", kind = "dev", p = c(500L, 1000L), s = 4L, r = 1L, ref = c("2ba5c283", "c4724d92")),
  data.frame(source = "B: NOTS dev (bench_v2 checker)", kind = "dev",
             p = as.integer(substr(ck$case, 2, 5)), s = as.integer(substr(ck$case, 8, 8)), r = 1L, ref = ck$detail),
  data.frame(source = "C: NOTS production (NOTS_READINESS s7)", kind = "prod", p = 1000L, s = 4L, r = 1L, ref = "6d4b8b5f"))
vers <- list(c(4, 6, 0), c(4, 5, 2), c(4, 5, 1), c(4, 5, 0), c(4, 4, 1))
res <- do.call(rbind, lapply(seq_len(nrow(targets)), function(i) {
  t <- targets[i, ]
  d <- if (t$kind == "dev") gd$generate_dev_dataset(t$p, t$s, t$r) else gp$generate_prod_dataset(t$p, t$s, t$r)
  f <- tempfile(fileext = ".rds"); saveRDS(d$inputs, f, compress = FALSE)
  b <- readBin(f, "raw", file.info(f)$size); unlink(f)
  hit <- NA_character_
  for (v in vers) { b2 <- b; b2[7:10] <- as.raw(c(0, v))
    if (startsWith(digest::digest(b2, algo = "sha256", serialize = FALSE), t$ref)) hit <- paste(v, collapse = ".") }
  data.frame(t, dataset_id = d$inputs$dataset_id, match = !is.na(hit), header_version = hit)
}))
res$blas <- paste(Sys.getenv("FLEXIBLAS", "default"), "threads", Sys.getenv("OPENBLAS_NUM_THREADS", "default"))
print(res[, c("source", "dataset_id", "match", "header_version", "blas")])
write.csv(res, file.path(outdir, "data_hash_check.csv"), row.names = FALSE)
