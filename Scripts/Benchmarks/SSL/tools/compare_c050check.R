# compare_c050check.R -- oracle for the c = 0.5 infrastructure change: the outputs of a c050check
# run (new code copy, scale c100) must be bit-identical to the c = 1 production outputs of the same
# datasets, field by field, in both the rule rows (.csv) and the saved R object (.rds).
# Excluded (run- or host-specific, not scientific): rule-row columns run_id, runtime_s, host,
# slurm_job_id, slurm_array_task_id, started_utc, finished_utc (also inside the saved rows), and
# the saved-object fields listed in EXCL_RDS below (timings, timestamps, process memory, host, PID,
# SLURM ids, node core count, snapshot and frozen-manifest paths). The .done marker (a timestamp)
# and the .sha256 file (hashes of files that contain the excluded fields) are not compared; each
# side's .sha256 is verified instead.
# Reads only the two results trees. Usage:
#   Rscript compare_c050check.R --new <results/<c050check run id>> --ref <results/<c = 1 prod run id>>
#     --datasets p1000_S4_r001,p1000_S4_r002,p1000_S4_r003 --methods A1,SuSiE-L100 [--out <file.csv>]

EXCL_COLS <- c("run_id", "runtime_s", "host", "slurm_job_id", "slurm_array_task_id",
               "started_utc", "finished_utc")
EXCL_RDS <- c(
  paste0("^rows/", EXCL_COLS, "$"),
  "^runtime_s$", "^started_utc$", "^finished_utc$",        # timings and timestamps
  "^vm_hwm_kb$",                                            # A1: peak memory of the process
  "^code/dir$", "^input/manifest$",                         # A3: snapshot path, frozen-manifest path of the run
  "^environment/(host|pid|detect_cores)$", "^environment/slurm/")  # A3: node, process, SLURM ids

args <- commandArgs(trailingOnly = TRUE)
get_arg <- function(k, default = NULL) {
  i <- match(paste0("--", k), args)
  if (is.na(i)) { if (is.null(default)) stop("missing --", k); return(default) }
  args[i + 1L]
}
new_dir <- get_arg("new"); ref_dir <- get_arg("ref")
datasets <- strsplit(get_arg("datasets"), ",")[[1]]
methods <- strsplit(get_arg("methods"), ",")[[1]]
scale_key <- "c100"

sha_ok <- function(stem) {
  l <- readLines(paste0(stem, ".sha256"))
  h <- sub("^([0-9a-f]{64})  .*$", "\\1", l); f <- sub("^[0-9a-f]{64}  ", "", l)
  identical(sort(f), sort(basename(paste0(stem, c(".csv", ".rds"))))) &&
    all(vapply(seq_along(f), function(i) identical(h[i], digest_sha256(file.path(dirname(stem), f[i]))), TRUE))
}
digest_sha256 <- function(f) {
  if (requireNamespace("digest", quietly = TRUE)) return(digest::digest(file = f, algo = "sha256"))
  out <- system2("sha256sum", shQuote(f), stdout = TRUE)
  sub(" .*$", "", out)
}

# Flatten a saved object into named leaves ("a/b/c"); data frames and lists recurse by name
# (or [index] when unnamed); every leaf keeps its attributes for identical().
flatten <- function(x, path = "") {
  if (is.list(x) && !is.null(x) && length(x) > 0L) {
    nm <- names(x)
    out <- list()
    for (i in seq_along(x)) {
      key <- if (!is.null(nm) && nzchar(nm[i])) nm[i] else sprintf("[%d]", i)
      out <- c(out, flatten(x[[i]], if (nzchar(path)) paste0(path, "/", key) else key))
    }
    # the container's own attributes (names, class, row.names, dim) as one leaf
    a <- attributes(x)
    if (length(a)) out[[paste0(if (nzchar(path)) path else "", "@attributes")]] <- a
    out
  } else {
    stats::setNames(list(x), if (nzchar(path)) path else "<root>")
  }
}
excluded <- function(p) any(vapply(EXCL_RDS, function(rx) grepl(rx, p), TRUE))

res <- list()
add <- function(ds, mid, part, field, status, note = "")
  res[[length(res) + 1L]] <<- data.frame(dataset = ds, method_id = mid, part = part, field = field,
                                          status = status, note = note, stringsAsFactors = FALSE)
for (ds in datasets) for (mid in methods) {
  pdir <- sub("^(p[0-9]{4})_.*$", "\\1", ds); cid <- paste0(ds, "_", scale_key)
  a <- file.path(new_dir, pdir, cid, mid); b <- file.path(ref_dir, pdir, cid, mid)
  for (side in c("new", "ref")) {
    stem <- if (side == "new") a else b
    ok <- all(file.exists(paste0(stem, c(".csv", ".rds", ".sha256", ".done")))) && sha_ok(stem)
    add(ds, mid, "integrity", paste0(side, ": 4 files present, .sha256 verifies"), if (ok) "PASS" else "FAIL")
  }
  xa <- utils::read.csv(paste0(a, ".csv"), colClasses = "character")
  xb <- utils::read.csv(paste0(b, ".csv"), colClasses = "character")
  if (!identical(names(xa), names(xb))) add(ds, mid, "csv", "<column names>", "FAIL")
  if (nrow(xa) != nrow(xb)) add(ds, mid, "csv", "<row count>", "FAIL")
  for (col in union(names(xa), names(xb))) {
    if (col %in% EXCL_COLS) { add(ds, mid, "csv", col, "EXCLUDED"); next }
    add(ds, mid, "csv", col, if (identical(xa[[col]], xb[[col]])) "PASS" else "FAIL")
  }
  fa <- flatten(readRDS(paste0(a, ".rds"))); fb <- flatten(readRDS(paste0(b, ".rds")))
  for (p in union(names(fa), names(fb))) {
    if (excluded(p)) { add(ds, mid, "rds", p, "EXCLUDED"); next }
    if (!p %in% names(fa) || !p %in% names(fb)) { add(ds, mid, "rds", p, "FAIL", "present on one side only"); next }
    add(ds, mid, "rds", p, if (identical(fa[[p]], fb[[p]])) "PASS" else "FAIL")
  }
}
R <- do.call(rbind, res)
out <- get_arg("out", "")
if (nzchar(out)) utils::write.csv(R, out, row.names = FALSE)
# Per field over all (dataset, method): PASS only if every comparison passed.
agg <- stats::aggregate(status ~ part + field, R, function(s)
  if (all(s == "EXCLUDED")) "EXCLUDED" else if (all(s == "PASS")) "PASS" else "FAIL")
cat(sprintf("compared %d (dataset, method) pairs: %s x %s\n", length(datasets) * length(methods),
            paste(datasets, collapse = ","), paste(methods, collapse = ",")))
cat(sprintf("fields compared: csv %d, rds %d; excluded: %d\n", sum(agg$part == "csv" & agg$status != "EXCLUDED"),
            sum(agg$part == "rds" & agg$status != "EXCLUDED"), sum(agg$status == "EXCLUDED")))
cat("excluded csv columns:", paste(EXCL_COLS, collapse = ", "), "\n")
cat("excluded rds fields:", paste(sort(unique(agg$field[agg$part == "rds" & agg$status == "EXCLUDED"])), collapse = ", "), "\n")
fails <- agg[agg$status == "FAIL", ]
if (nrow(fails)) { cat("FAILING fields:\n"); print(fails, row.names = FALSE) }
cat(sprintf("VERDICT: %s (%d PASS fields, %d FAIL fields)\n", if (nrow(fails)) "FAIL" else "PASS",
            sum(agg$status == "PASS"), nrow(fails)))
quit(status = if (nrow(fails)) 1L else 0L)
