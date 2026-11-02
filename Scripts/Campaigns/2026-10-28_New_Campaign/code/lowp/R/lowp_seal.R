# Seal the LOWP datasets (INTERFACES I1, LOWP_SPEC L.5): 1,200 production datasets (p 20, 30 x S1-S6 x r 1..100)
# and 60 dev datasets (r 1..5) under a study root.
#
#   Rscript lowp_seal.R <STUDY root> [--no-dev]
#
# Layout written (same names locally and on NOTS):
#   <root>/inputs/p0020|p0030/p{pppp}_S{s}_r{rrr}.rds          fitting jobs open only this
#   <root>/truth/p0020|p0030/p{pppp}_S{s}_r{rrr}.rds           generator checks and scoring only
#   <root>/manifests/inputs_manifest_lowp.csv, truth_manifest_lowp.csv
#   <root>/dev/{inputs,truth,manifests}/...                    same layout; ids carry the dev_ prefix (dev_p0020_S1_r001)
#
# Files: saveRDS(version = 3, compress = FALSE). Read-only after sealing:
#   * this script: Sys.chmod(file, "0444"). On Windows R honours only the write bit, i.e. it sets the read-only
#     attribute; on Linux it is chmod 0444 (= a-w).
#   * Linux/NOTS only (not enforceable on Windows): directories stay 0755; during fitting waves the truth/ tree is
#     set to mode 000 (lowp_truth_lock(root, TRUE): directories and files, ordinary user) and restored by scoring
#     (lowp_truth_lock(root, FALSE): dirs 0755, files 0444, root first, each directory opened before descending, every
#     chmod checked and modes read back). lowp_truth_lock() refuses to act on Windows and as root.
#     tests/test_truth_lock_linux.sh exercises it on the production and dev truth trees (pilot).
# The file SHA-256 in the manifest depends on the R version that wrote the RDS header (serialization header carries
# the R version); sealed files are therefore COPIED to NOTS, never regenerated there, whenever file hashes matter.
# The float64 hashes (x, y_*, signal, eps, foldid) are independent of R version and platform.

.seal_dir <- local({
  a <- grep("^--file=", commandArgs(FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1L]), winslash = "/"))
  else { p <- NULL; for (fr in rev(sys.frames())) if (!is.null(fr$ofile)) { p <- dirname(normalizePath(fr$ofile, winslash = "/")); break }
         if (is.null(p)) getwd() else p }
})
if (!exists("generate_dataset", mode = "function")) source(file.path(.seal_dir, "lowp_generate.R"))

lowp_input_row <- function(inp, rel_file, file_sha) {
  data.frame(dataset_id = inp$dataset_id, p = inp$p, scenario = inp$scenario, replicate = inp$replicate,
             data_seed = inp$data_seed, fold_seed = inp$fold_seed, method_seed = inp$method_seed,
             file = rel_file, file_sha256 = file_sha, x_sha256 = f64_sha256(inp$X),
             t(setNames(vapply(names(LOWP_SCALES), function(k) f64_sha256(inp$Y[, k]), ""),
                        paste0("y_", names(LOWP_SCALES), "_sha256"))),
             fold_sha256 = f64_sha256(inp$foldid), check.names = FALSE, stringsAsFactors = FALSE)
}
lowp_truth_row <- function(tr, rel_file, file_sha) {
  data.frame(dataset_id = tr$dataset_id, file = rel_file, file_sha256 = file_sha,
             signal_sha256 = f64_sha256(tr$signal), eps_sha256 = f64_sha256(tr$eps),
             active = paste(tr$active, collapse = ";"), beta = paste(tr$beta, collapse = ";"),
             stringsAsFactors = FALSE)
}

# Seal one tree (kind = "prod" under <base>, kind = "dev" under <base>/dev). Returns the two manifests.
.lowp_seal_tree <- function(base, kind, reps) {
  for (d in c("inputs", "truth", "manifests")) dir.create(file.path(base, d), recursive = TRUE, showWarnings = FALSE)
  rows_in <- list(); rows_tr <- list(); written <- character()
  for (p in LOWP_PS) {
    di <- file.path(base, "inputs", sprintf("p%04d", p)); dt <- file.path(base, "truth", sprintf("p%04d", p))
    dir.create(di, showWarnings = FALSE); dir.create(dt, showWarnings = FALSE)
    for (s in 1:6) for (r in reps) {
      d <- generate_dataset(p, s, r, kind)
      id <- d$inputs$dataset_id
      fi <- file.path(di, paste0(id, ".rds")); ft <- file.path(dt, paste0(id, ".rds"))
      if (file.exists(fi) || file.exists(ft)) stop("refusing to overwrite ", fi)
      saveRDS(d$inputs, fi, version = 3, compress = FALSE); saveRDS(d$truth, ft, version = 3, compress = FALSE)
      written <- c(written, fi, ft)
      rows_in[[length(rows_in) + 1L]] <- lowp_input_row(d$inputs, sprintf("inputs/p%04d/%s.rds", p, id),
                                                        digest::digest(file = fi, algo = "sha256"))
      rows_tr[[length(rows_tr) + 1L]] <- lowp_truth_row(d$truth, sprintf("truth/p%04d/%s.rds", p, id),
                                                        digest::digest(file = ft, algo = "sha256"))
    }
  }
  mi <- do.call(rbind, rows_in); mt <- do.call(rbind, rows_tr)
  fm1 <- file.path(base, "manifests", "inputs_manifest_lowp.csv"); fm2 <- file.path(base, "manifests", "truth_manifest_lowp.csv")
  if (file.exists(fm1) || file.exists(fm2)) stop("refusing to overwrite manifests in ", base)
  utils::write.csv(mi, fm1, row.names = FALSE); utils::write.csv(mt, fm2, row.names = FALSE)
  ro <- c(written, fm1, fm2)
  if (!all(Sys.chmod(ro, "0444"))) stop("chmod 0444 failed on some sealed files")
  wr <- bitwAnd(as.integer(file.info(ro)$mode), .lowp_oct("222"))      # write bits must be clear (Windows: read-only attribute)
  if (anyNA(wr) || any(wr != 0L)) stop("sealed files are still writable: ", paste(utils::head(ro[is.na(wr) | wr != 0L], 3), collapse = ", "))
  list(inputs = mi, truth = mt, n_files = length(written) + 2L)
}

lowp_seal <- function(root, dev = TRUE) {
  stopifnot(requireNamespace("digest", quietly = TRUE), length(root) == 1L)
  dir.create(root, recursive = TRUE, showWarnings = FALSE)
  prod <- .lowp_seal_tree(root, "prod", 1:100)
  cat(sprintf("sealed %d production datasets under %s\n", nrow(prod$inputs), root))
  devr <- if (dev) { x <- .lowp_seal_tree(file.path(root, "dev"), "dev", 1:5)
                     cat(sprintf("sealed %d dev datasets under %s/dev\n", nrow(x$inputs), root)); x } else NULL
  invisible(list(prod = prod, dev = devr))
}

# ---- truth lock / unlock (Linux/NOTS, ordinary user) --------------------------------------------------------------
# Fitting waves: every truth tree (<root>/truth and <root>/dev/truth) is mode 000 (directories AND files); scoring restores
# directories 0755 and files 0444. A 000 directory cannot be listed, so the walk is ORDERED: chmod the directory open FIRST,
# list it, then descend; files are set after their directory is open. Locking first runs the same walk (so a partially locked
# tree is repaired and a complete inventory exists), then chmods files 000, then directories deepest-first, then the top.
# Every chmod result is checked and the resulting modes are read back; any failure stops with an error.
# The file-system primitives are injectable (`fs`) so that the algorithm can be exercised on a modelled POSIX tree
# (tests/test_adversarial.R); the real primitives are used by default. Root (uid 0) bypasses permissions: refuse to run.
lowp_real_fs <- function() list(
  chmod  = function(path, mode) isTRUE(suppressWarnings(Sys.chmod(path, mode, use_umask = FALSE))),
  ls     = function(dir) {      # NULL when the directory cannot be read and searched
    if (suppressWarnings(file.access(dir, 4L)) != 0L || suppressWarnings(file.access(dir, 1L)) != 0L) return(NULL)
    tryCatch(suppressWarnings(list.files(dir, all.files = TRUE, no.. = TRUE)), error = function(e) NULL) },
  isdir  = function(path) { i <- suppressWarnings(file.info(path)); if (is.na(i$isdir)) NA else i$isdir },
  mode   = function(path) { m <- suppressWarnings(file.info(path)$mode); if (is.na(m)) NA_integer_ else as.integer(m) },
  can_read = function(path) isTRUE(suppressWarnings(file.access(path, 4L)) == 0L))

.lowp_oct <- function(x) strtoi(x, 8L)

# Open every directory under `top` (0755), files 0444; returns the inventory. Stops on any failure.
lowp_truth_open_walk <- function(top, fs = lowp_real_fs()) {
  inv <- list(dirs = character(), files = character())
  rec <- function(d) {
    if (!fs$chmod(d, "755")) stop("chmod 755 failed on directory ", d)
    inv$dirs <<- c(inv$dirs, d)
    nm <- fs$ls(d)
    if (is.null(nm)) stop("cannot list ", d, " after chmod 755")
    for (n in sort(nm)) {
      pth <- file.path(d, n); isd <- fs$isdir(pth)
      if (is.na(isd)) stop("cannot stat ", pth)
      if (isd) rec(pth) else { if (!fs$chmod(pth, "444")) stop("chmod 444 failed on ", pth); inv$files <<- c(inv$files, pth) }
    }
  }
  rec(top); inv
}
lowp_truth_verify_open <- function(inv, fs = lowp_real_fs()) {
  bad <- c(inv$dirs[vapply(inv$dirs, function(d) !identical(fs$mode(d), .lowp_oct("755")), TRUE)],
           inv$files[vapply(inv$files, function(f) !identical(fs$mode(f), .lowp_oct("444")) || !fs$can_read(f), TRUE)])
  if (length(bad)) stop("after unlock these paths do not have mode 755/444 or are unreadable: ", paste(utils::head(bad, 5), collapse = ", "))
  invisible(TRUE)
}
lowp_truth_unlock_tree <- function(top, fs = lowp_real_fs()) {
  inv <- lowp_truth_open_walk(top, fs); lowp_truth_verify_open(inv, fs); invisible(inv)
}
lowp_truth_lock_tree <- function(top, fs = lowp_real_fs()) {
  inv <- lowp_truth_open_walk(top, fs); lowp_truth_verify_open(inv, fs)       # complete inventory while everything is reachable
  for (f in inv$files) if (!fs$chmod(f, "000")) stop("chmod 000 failed on ", f)
  depth <- lengths(strsplit(inv$dirs, "/", fixed = TRUE))
  for (d in inv$dirs[order(depth, decreasing = TRUE)]) if (!fs$chmod(d, "000")) stop("chmod 000 failed on directory ", d)
  if (!identical(fs$mode(top), 0L)) stop("top directory ", top, " is not mode 000 after locking")
  if (!is.null(fs$ls(top))) stop("locked directory ", top, " can still be listed")
  if (length(inv$files) && !is.na(fs$mode(inv$files[1L]))) stop("a file below the locked tree is still reachable: ", inv$files[1L])
  invisible(inv)
}
# lock = TRUE: fitting wave; lock = FALSE: scoring. Acts on <root>/truth and <root>/dev/truth when present.
lowp_truth_lock <- function(root, lock = TRUE, fs = NULL) {
  if (is.null(fs)) {
    if (.Platform$OS.type == "windows") stop("truth mode 000 is not enforceable on Windows; run it on NOTS (Linux)")
    if (identical(Sys.info()[["effective_user"]], "root")) stop("running as root bypasses permissions; use the ordinary user")
    fs <- lowp_real_fs()
  }
  res <- list()
  for (tr in c(file.path(root, "truth"), file.path(root, "dev", "truth"))) {
    # a locked top cannot be seen as a directory by listing, but its parent is readable: stat the top itself
    if (is.na(fs$isdir(tr))) next
    inv <- if (lock) lowp_truth_lock_tree(tr, fs) else lowp_truth_unlock_tree(tr, fs)
    res[[tr]] <- c(dirs = length(inv$dirs), files = length(inv$files))
  }
  if (!length(res)) stop("no truth tree found under ", root)
  invisible(res)
}

if (sys.nframe() == 0L) {
  a <- commandArgs(trailingOnly = TRUE)
  stopifnot(length(a) >= 1L)
  lowp_seal(a[[1L]], dev = !("--no-dev" %in% a))
}
