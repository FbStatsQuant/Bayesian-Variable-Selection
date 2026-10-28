#!/usr/bin/env Rscript
# compare_c050check.R -- c050 infrastructure oracle (BRIEF_C050_ENG task 3). Compares the outputs of
# the c050 code copy run at scale c100 with the c = 1 production outputs of the same datasets, and
# requires them to be bit-identical except for the run-identity fields below. Reads results only
# (never inputs, truth or scoring). Infrastructure tool; not part of any fit.
#
#   Rscript --vanilla compare_c050check.R <new_results_dir> <ref_results_dir> <dataset_ids,> <method_ids,> <out_txt>
#
# Compared, per dataset x method id: every element of <m>.rds (recursively, attributes included,
# identical() at the leaves) and every column of <m>.csv (read as text). Not compared: <m>.sha256
# (hash of the .rds bytes, which embed run_id) and <m>.done (completion stamp).
# Excluded fields (matched by name at any depth of the .rds, and as .csv columns):
EXCLUDED <- c("run_id",                                    # run identity
              "started_utc", "finished_utc",               # timestamps
              "runtime_s",                                 # runtimes
              "host", "slurm_job_id", "slurm_array_task_id",  # host / scheduler fields
              "command")                                   # process command line (holds run id and snapshot path)

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 5L) stop("usage: compare_c050check.R <new_dir> <ref_dir> <ids,> <methods,> <out_txt>")
new_dir <- args[1]; ref_dir <- args[2]
ids <- strsplit(args[3], ",", fixed = TRUE)[[1]]; mids <- strsplit(args[4], ",", fixed = TRUE)[[1]]
out_txt <- args[5]

res <- list()
add <- function(case, file, path, status, note = "")
  res[[length(res) + 1L]] <<- data.frame(case = case, file = file, field = path, status = status,
                                         note = note, stringsAsFactors = FALSE)

# Recursive comparison; one result row per compared leaf or excluded field.
walk <- function(a, b, path, case, file) {
  if (is.list(a) && is.list(b)) {
    oa <- attributes(a); ob <- attributes(b); oa$names <- NULL; ob$names <- NULL
    if (!identical(oa, ob)) add(case, file, paste0(path, "@attributes"), "FAIL", "attributes differ")
    na <- names(a); nb <- names(b)
    if (is.null(na) && is.null(nb)) {
      if (length(a) != length(b)) { add(case, file, path, "FAIL", "list lengths differ"); return(invisible()) }
      for (i in seq_along(a)) walk(a[[i]], b[[i]], sprintf("%s[[%d]]", path, i), case, file)
      return(invisible())
    }
    if (!identical(na, nb)) add(case, file, paste0(path, "@names"), "FAIL", "element names/order differ")
    for (nm in union(na, nb)) {
      p <- if (nzchar(path)) paste0(path, "$", nm) else nm
      if (!(nm %in% na) || !(nm %in% nb)) { add(case, file, p, "FAIL", "present in one object only"); next }
      if (nm %in% EXCLUDED) { add(case, file, p, "EXCLUDED", if (identical(a[[nm]], b[[nm]])) "equal" else "differs"); next }
      walk(a[[nm]], b[[nm]], p, case, file)
    }
    return(invisible())
  }
  add(case, file, path, if (identical(a, b)) "PASS" else "FAIL", if (identical(a, b)) "" else "values differ")
}

for (id in ids) for (m in mids) {
  pp <- sub("^(p[0-9]{4})_.*$", "\\1", id); case <- paste0(id, "_c100")
  fn <- file.path(new_dir, pp, case, paste0(m, c(".rds", ".csv")))
  fr <- file.path(ref_dir, pp, case, paste0(m, c(".rds", ".csv")))
  ok <- file.exists(c(fn, fr))
  if (!all(ok)) { add(case, m, "files", "FAIL", paste("missing:", paste(c(fn, fr)[!ok], collapse = " "))); next }
  walk(readRDS(fn[1]), readRDS(fr[1]), "", case, paste0(m, ".rds"))
  cn <- read.csv(fn[2], colClasses = "character", check.names = FALSE, na.strings = character(0))
  cr <- read.csv(fr[2], colClasses = "character", check.names = FALSE, na.strings = character(0))
  if (!identical(names(cn), names(cr)) || nrow(cn) != nrow(cr)) {
    add(case, paste0(m, ".csv"), "columns/rows", "FAIL", "csv shape or column names differ"); next }
  for (k in names(cn)) {
    if (k %in% EXCLUDED) { add(case, paste0(m, ".csv"), k, "EXCLUDED", if (identical(cn[[k]], cr[[k]])) "equal" else "differs"); next }
    add(case, paste0(m, ".csv"), k, if (identical(cn[[k]], cr[[k]])) "PASS" else "FAIL",
        if (identical(cn[[k]], cr[[k]])) "" else "values differ")
  }
}

tab <- do.call(rbind, res)
n_fail <- sum(tab$status == "FAIL"); n_pass <- sum(tab$status == "PASS"); n_ex <- sum(tab$status == "EXCLUDED")
con <- file(out_txt, "w")
w <- function(...) { cat(..., "\n", sep = ""); cat(..., "\n", sep = "", file = con) }
w("compare_c050check  new=", new_dir, "  ref=", ref_dir)
w("datasets: ", paste(ids, collapse = ","), "  methods: ", paste(mids, collapse = ","))
w("excluded fields: ", paste(EXCLUDED, collapse = ", "))
w(sprintf("compared leaves: PASS %d  FAIL %d  EXCLUDED %d", n_pass, n_fail, n_ex))
w("per case x file: ")
agg <- aggregate(cbind(pass = tab$status == "PASS", fail = tab$status == "FAIL", excluded = tab$status == "EXCLUDED") ~
                   case + file, data = tab, FUN = sum)
for (i in seq_len(nrow(agg))) w(sprintf("  %-22s %-14s pass %4d  fail %3d  excluded %2d", agg$case[i], agg$file[i],
                                        agg$pass[i], agg$fail[i], agg$excluded[i]))
w("excluded fields observed (equal/differs): ")
ex <- unique(tab[tab$status == "EXCLUDED", c("file", "field", "note")])
for (i in seq_len(nrow(ex))) w(sprintf("  %-14s %-40s %s", ex$file[i], ex$field[i], ex$note[i]))
if (n_fail) { w("FAILURES: "); f <- tab[tab$status == "FAIL", ]
  for (i in seq_len(nrow(f))) w(sprintf("  %s %s %s : %s", f$case[i], f$file[i], f$field[i], f$note[i])) }
w(if (n_fail == 0L && n_pass > 0L) "VERDICT: PASS (bit-identical outside the excluded fields)" else "VERDICT: FAIL")
close(con)
write.csv(tab, sub("\\.txt$", "_detail.csv", out_txt), row.names = FALSE)
quit(save = "no", status = if (n_fail == 0L && n_pass > 0L) 0L else 1L)
