# make_synth.R SRC_CASE_DIR OUT_ROOT : synthetic benchmark root for the Sol R1 finding-1 test (test data only, never a result).
# Copies the 8 pilot benchmark records of one dev case to two PRODUCTION cases in different chunks
# (p0020_S1_r001_c050 in chunk_00, p0020_S1_r051_c050 in chunk_01), relabelling case_id / dataset_id in the rule rows; writes .done markers.
a <- commandArgs(trailingOnly = TRUE); src <- a[1]; out <- a[2]
for (case in c("p0020_S1_r001_c050", "p0020_S1_r051_c050")) {
  d <- file.path(out, "p0020", case); dir.create(d, recursive = TRUE, showWarnings = FALSE)
  for (f in list.files(src, pattern = "\\.rds$", full.names = TRUE)) {
    x <- readRDS(f)
    relabel <- function(df) { df$case_id <- case; df$dataset_id <- sub("_c[0-9]{3}$", "", case); df }
    if (is.data.frame(x)) x <- relabel(x) else if (is.list(x) && is.data.frame(x$rows)) x$rows <- relabel(x$rows) else stop("unknown record shape: ", f)
    saveRDS(x, file.path(d, basename(f)))
    file.create(file.path(d, sub("\\.rds$", ".done", basename(f))))
  }
}
cat("synthetic root written:", out, "\n")
