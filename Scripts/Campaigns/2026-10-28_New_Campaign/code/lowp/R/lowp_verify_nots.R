# Check 4(b) of LOWP_SPEC L.6, for the NOTS pilot bundle (P0a): a CROSS-PLATFORM GENERATOR CHECK, not an identity check (HQ decision D44,
# 2026-10-30). Regenerate every LOWP dataset on NOTS and compare it with the LOCAL seal. Nothing is written under inputs/ or truth/.
#
#   Rscript lowp_verify_nots.R --manifests <dir with inputs_manifest_lowp.csv, truth_manifest_lowp.csv>
#                              --dev-manifests <dir with the dev manifests>      (default: <manifests>/../dev/manifests if it exists)
#                              --study <sealed study root>                      (REQUIRED: truth/, dev/truth/ and the six pilot input copies)
#                              --out <output dir>
#
# Why not bit identity: R's normal draws (Inversion: qnorm via the platform libm) differ by 1-3 ulp between R 4.4.1/Windows (the sealing
# platform) and R 4.5.2/Linux (NOTS) for the same seed (OPS-4, ops/PILOT_FAIL_20261030T0313Z.md). The laptop-sealed files stay CANONICAL:
# the fits consume the sealed copies, never regenerated data. So:
#   EXACT (what the fits consume, and everything that is not floating point):
#     - manifests: structure, the exact expected grid, every seed field (lowp_validate_manifests);
#     - foldid: the regenerated fold hash equals the manifest's (integers, platform independent);
#     - every truth file (1,200 + 60) and each of the six pilot input copies: file SHA-256 equal to its manifest row, and its stored float64
#       arrays hash to the manifest's array hashes (the sealed content IS the manifest);
#     - pilot copies and truth files: names, dims, column names and every non-float field identical() to the regenerated record;
#   TOLERANCE (the generator on this platform reproduces the seal up to rounding):
#     - regenerated eps, signal and beta (all 1,260 truth files) and X, the five Y columns (six pilot copies) against the SEALED values:
#       |regenerated - sealed| <= 1e-12 * max(1, |sealed|), element by element, all values finite. The observed maxima are reported.
#   Bit-identical regenerated arrays are counted for information only.
# Gate semantics (full check only; there is no partial PASS):
#   exit 0  PASS        every exact check holds and every tolerance comparison is within the bound, over all 1,200 production + 60 dev rows
#                       and all six pilot copies.
#   exit 1  MISMATCH    some exact check fails or some value exceeds the tolerance. STOP: keep the evidence and diagnose. The sealed local
#                       files stay canonical; any change of canonical source is an explicit HQ decision followed by a new audited seal.
#   exit 3  INCOMPLETE  a prerequisite is missing or malformed (missing/short manifest, wrong schema, out-of-grid ids, a truth file or
#                       pilot copy missing, --study not supplied, ...). What could be compared is still reported; INCOMPLETE is never a PASS.
# Needs only R + digest. Writes <out>/NOTS_REGEN_REPORT.md, <out>/NOTS_REGEN_MISMATCHES.csv and <out>/NOTS_REGEN_MAXIMA.csv. About 1-2 minutes.

.nots_dir <- local({
  a <- grep("^--file=", commandArgs(FALSE), value = TRUE)
  if (length(a)) dirname(normalizePath(sub("^--file=", "", a[1L]), winslash = "/"))
  else { p <- NULL; for (fr in rev(sys.frames())) if (!is.null(fr$ofile)) { p <- dirname(normalizePath(fr$ofile, winslash = "/")); break }
         if (is.null(p)) getwd() else p }
})
if (!exists("generate_dataset", mode = "function")) source(file.path(.nots_dir, "lowp_generate.R"))

LOWP_PILOT_CELLS <- list(c(1L, 1L), c(4L, 50L), c(6L, 100L))      # S1 r1, S4 r50, S6 r100 (per p)
LOWP_REGEN_TOL   <- 1e-12                                            # D44: |delta| <= 1e-12 * max(1, |sealed|)

# tolerance comparison of a regenerated array with the sealed one: same shape, all finite, |a - b| <= tol * max(1, |b|)
lowp_tol_cmp <- function(a, b, tol = LOWP_REGEN_TOL) {
  # names and dimnames are metadata, not floating point: exact (Sol PILOT7D R7D-1)
  if (!identical(names(a), names(b)) || !identical(dimnames(a), dimnames(b)))
    return(list(ok = FALSE, max_abs = NA_real_, max_scaled = NA_real_, why = "names / dimnames differ"))
  a <- unclass(a); b <- unclass(b)
  if (!is.numeric(a) || !is.numeric(b) || length(a) != length(b) || !identical(dim(a), dim(b)))
    return(list(ok = FALSE, max_abs = NA_real_, max_scaled = NA_real_, why = "type, length or dim differs"))
  a <- as.double(a); b <- as.double(b)
  if (!all(is.finite(a)) || !all(is.finite(b))) return(list(ok = FALSE, max_abs = NA_real_, max_scaled = NA_real_, why = "non-finite value"))
  d <- abs(a - b); sc <- d / pmax(1, abs(b))
  list(ok = all(d <= tol * pmax(1, abs(b))), max_abs = if (length(d)) max(d) else 0, max_scaled = if (length(sc)) max(sc) else 0, why = "")
}

lowp_verify_nots <- function(manifests, out, dev_manifests = NULL, study = NULL) {
  stopifnot(requireNamespace("digest", quietly = TRUE))
  dir.create(out, recursive = TRUE, showWarnings = FALSE)
  cs <- names(LOWP_SCALES); t0 <- proc.time()[["elapsed"]]
  incomplete <- character(); mism <- list(); n_ds <- c(prod = 0L, dev = 0L)
  addm <- function(id, what, nots, local) mism[[length(mism) + 1L]] <<- data.frame(dataset_id = id, array = what, nots = nots, local = local, stringsAsFactors = FALSE)
  rd <- function(f) tryCatch(utils::read.csv(f, stringsAsFactors = FALSE, colClasses = "character"), error = function(e) NULL)
  fsha <- function(f) digest::digest(file = f, algo = "sha256")
  # observed maxima per array, and bit-identity counts (information)
  mx <- list(); bit <- c(identical = 0L, compared = 0L)
  track <- function(what, r) { cur <- mx[[what]]; if (is.null(cur)) cur <- c(n = 0, max_abs = 0, max_scaled = 0)
    mx[[what]] <<- c(n = cur[["n"]] + 1, max_abs = max(cur[["max_abs"]], r$max_abs, na.rm = TRUE), max_scaled = max(cur[["max_scaled"]], r$max_scaled, na.rm = TRUE)) }
  tolchk <- function(id, what, regen, sealed) {
    r <- lowp_tol_cmp(regen, sealed); track(what, r)
    bit[["compared"]] <<- bit[["compared"]] + 1L; if (identical(f64_sha256(regen), f64_sha256(sealed))) bit[["identical"]] <<- bit[["identical"]] + 1L
    if (!isTRUE(r$ok)) addm(id, paste0(what, " (tolerance ", format(LOWP_REGEN_TOL), ")"),
                            if (nzchar(r$why)) r$why else sprintf("max |delta| %.3g, max scaled %.3g", r$max_abs, r$max_scaled), "sealed")
  }

  if (is.null(dev_manifests)) { cand <- file.path(dirname(manifests), "dev", "manifests"); if (dir.exists(cand)) dev_manifests <- cand }
  trees <- list(prod = manifests, dev = dev_manifests)
  man <- list()
  for (kind in c("prod", "dev")) {
    d <- trees[[kind]]
    if (is.null(d) || !dir.exists(d)) { incomplete <- c(incomplete, sprintf("%s manifests directory not supplied or missing", kind)); next }
    fi <- file.path(d, "inputs_manifest_lowp.csv"); ft <- file.path(d, "truth_manifest_lowp.csv")
    if (!file.exists(fi) || !file.exists(ft)) { incomplete <- c(incomplete, sprintf("%s manifests: inputs_manifest_lowp.csv / truth_manifest_lowp.csv not both present in %s", kind, d)); next }
    mi <- rd(fi); mt <- rd(ft)
    if (is.null(mi) || is.null(mt)) { incomplete <- c(incomplete, sprintf("%s manifests cannot be parsed", kind)); next }
    v <- lowp_validate_manifests(mi, mt, kind)
    if (length(v$structure)) { incomplete <- c(incomplete, paste0(kind, " manifests malformed: ", v$structure)); next }
    for (z in v$seed) addm(kind, "seed (exact)", "design", z)
    man[[kind]] <- list(mi = mi, mt = mt)
  }
  have_study <- !is.null(study) && dir.exists(study)
  if (is.null(study)) incomplete <- c(incomplete, "--study not supplied: truth files and pilot copies cannot be compared")
  else if (!have_study) incomplete <- c(incomplete, sprintf("--study directory %s does not exist", study))
  truth_root <- function(kind) if (kind == "prod") file.path(study, "truth") else file.path(study, "dev", "truth")
  n_truth <- c(prod = 0L, dev = 0L)

  # ---- every dataset: regenerate; exact foldid; truth file exact + tolerance --------------------------------------------------------------
  for (kind in names(man)) {
    mi <- man[[kind]]$mi; mt <- man[[kind]]$mt
    for (i in seq_len(nrow(mi))) {
      p <- as.integer(mi$p[i]); s <- as.integer(mi$scenario[i]); r <- as.integer(mi$replicate[i]); id <- mi$dataset_id[i]
      d <- generate_dataset(p, s, r, kind); n_ds[[kind]] <- n_ds[[kind]] + 1L
      if (!identical(f64_sha256(d$inputs$foldid), mi$fold_sha256[i])) addm(id, "foldid (exact)", f64_sha256(d$inputs$foldid), mi$fold_sha256[i])
      for (k in cs) { bit[["compared"]] <- bit[["compared"]] + 1L; if (identical(f64_sha256(d$inputs$Y[, k]), mi[[paste0("y_", k, "_sha256")]][i])) bit[["identical"]] <- bit[["identical"]] + 1L }
      bit[["compared"]] <- bit[["compared"]] + 1L; if (identical(f64_sha256(d$inputs$X), mi$x_sha256[i])) bit[["identical"]] <- bit[["identical"]] + 1L
      if (!have_study) next
      g <- file.path(truth_root(kind), sprintf("p%04d", p), paste0(id, ".rds"))
      trow <- mt[mt$dataset_id == id, , drop = FALSE]
      if (!file.exists(g)) { incomplete <- c(incomplete, sprintf("truth file missing: %s", g)); next }
      n_truth[[kind]] <- n_truth[[kind]] + 1L
      if (!identical(fsha(g), trow$file_sha256)) { addm(id, "truth file_sha256 (exact)", fsha(g), "manifest"); next }
      st <- tryCatch(readRDS(g), error = function(e) NULL)
      if (!is.list(st)) { addm(id, "truth file unreadable (exact)", "error", "manifest"); next }
      if (!identical(f64_sha256(st$signal), trow$signal_sha256)) addm(id, "sealed truth signal vs manifest hash (exact)", f64_sha256(st$signal), trow$signal_sha256)
      if (!identical(f64_sha256(st$eps), trow$eps_sha256)) addm(id, "sealed truth eps vs manifest hash (exact)", f64_sha256(st$eps), trow$eps_sha256)
      if (!identical(sort(names(st)), sort(names(d$truth)))) addm(id, "truth field names (exact)", paste(sort(names(d$truth)), collapse = ";"), paste(sort(names(st)), collapse = ";"))
      for (f in c("active", "scenario", "dataset_id")) if (!identical(d$truth[[f]], st[[f]])) addm(id, paste0("truth ", f, " (exact)"), "regenerated", "sealed")
      tolchk(id, "truth beta", d$truth$beta, st$beta)
      tolchk(id, "truth signal", d$truth$signal, st$signal)
      tolchk(id, "truth eps", d$truth$eps, st$eps)
    }
  }
  # ---- the six sealed pilot input copies (production tree): exact + tolerance -------------------------------------------------------------
  n_copies <- 0L
  if (have_study) for (p in LOWP_PS) for (sr in LOWP_PILOT_CELLS) {
    d <- generate_dataset(p, sr[1L], sr[2L], "prod"); id <- d$inputs$dataset_id
    f <- file.path(study, "inputs", sprintf("p%04d", p), paste0(id, ".rds"))
    if (!file.exists(f)) { incomplete <- c(incomplete, sprintf("pilot copy missing: %s (inputs)", id)); next }
    n_copies <- n_copies + 1L
    if (is.null(man$prod)) next
    row <- man$prod$mi[man$prod$mi$dataset_id == id, , drop = FALSE]
    if (!identical(fsha(f), row$file_sha256)) { addm(id, "pilot inputs file_sha256 (exact)", fsha(f), "manifest"); next }
    sc <- tryCatch(readRDS(f), error = function(e) NULL)
    if (!is.list(sc)) { addm(id, "pilot inputs unreadable (exact)", "error", "manifest"); next }
    if (!identical(names(sc), names(d$inputs))) addm(id, "pilot inputs field names/order (exact)", paste(names(d$inputs), collapse = ";"), paste(names(sc), collapse = ";"))
    if (!identical(dim(sc$X), dim(d$inputs$X)) || !identical(dim(sc$Y), dim(d$inputs$Y)) || !identical(colnames(sc$Y), colnames(d$inputs$Y)))
      addm(id, "pilot inputs dims / Y column names (exact)", "regenerated", "sealed")
    if (!identical(f64_sha256(sc$X), row$x_sha256)) addm(id, "sealed X vs manifest hash (exact)", f64_sha256(sc$X), row$x_sha256)
    for (k in cs) if (!identical(f64_sha256(sc$Y[, k]), row[[paste0("y_", k, "_sha256")]])) addm(id, paste0("sealed Y ", k, " vs manifest hash (exact)"), "sealed", "manifest")
    if (!identical(sc$foldid, d$inputs$foldid)) addm(id, "pilot foldid (exact)", "regenerated", "sealed")
    for (fld in setdiff(names(d$inputs), c("X", "Y", "foldid"))) if (!identical(sc[[fld]], d$inputs[[fld]])) addm(id, paste0("pilot ", fld, " (exact)"), "regenerated", "sealed")
    tolchk(id, "pilot X", d$inputs$X, sc$X)
    for (k in cs) tolchk(id, paste0("pilot Y ", k), d$inputs$Y[, k], sc$Y[, k])
  }
  if (n_ds[["prod"]] != 1200L && !any(grepl("^prod", incomplete))) incomplete <- c(incomplete, sprintf("only %d production rows compared", n_ds[["prod"]]))
  if (n_ds[["dev"]] != 60L && !any(grepl("^dev", incomplete))) incomplete <- c(incomplete, sprintf("only %d dev rows compared", n_ds[["dev"]]))
  if (have_study && (n_truth[["prod"]] != 1200L || n_truth[["dev"]] != 60L) && !any(grepl("^truth file missing", incomplete)))
    incomplete <- c(incomplete, sprintf("truth files compared: %d production, %d dev (expected 1,200 and 60)", n_truth[["prod"]], n_truth[["dev"]]))

  mm <- if (length(mism)) do.call(rbind, mism) else data.frame(dataset_id = character(), array = character(), nots = character(), local = character())
  utils::write.csv(mm, file.path(out, "NOTS_REGEN_MISMATCHES.csv"), row.names = FALSE)
  mxd <- if (length(mx)) data.frame(array = names(mx), comparisons = vapply(mx, `[[`, 0, "n"), max_abs_delta = vapply(mx, `[[`, 0, "max_abs"),
                                    max_scaled_delta = vapply(mx, `[[`, 0, "max_scaled"), bound = LOWP_REGEN_TOL, row.names = NULL, stringsAsFactors = FALSE)
         else data.frame(array = character(), comparisons = numeric(), max_abs_delta = numeric(), max_scaled_delta = numeric(), bound = numeric())
  utils::write.csv(mxd, file.path(out, "NOTS_REGEN_MAXIMA.csv"), row.names = FALSE)
  status <- if (nrow(mm) > 0L) "MISMATCH" else if (length(incomplete) > 0L || n_copies != 6L) "INCOMPLETE" else "PASS"
  code <- c(PASS = 0L, MISMATCH = 1L, INCOMPLETE = 3L)[[status]]
  bl <- paste0({b <- tryCatch(extSoftVersion()[["BLAS"]], error = function(e) ""); if (!nzchar(b)) "(none reported)" else b},
               " / LAPACK ", {l <- tryCatch(La_library(), error = function(e) ""); if (!nzchar(l)) "(none reported)" else l})
  L <- c("# LOWP check 4(b), P0a: cross-platform generator check (NOTS regeneration vs the local seal)", "",
         sprintf("Host `%s`; %s; platform %s; BLAS %s; %s UTC; elapsed %.0f s.", Sys.info()[["nodename"]], R.version.string, R.version$platform, bl,
                 format(Sys.time(), "%Y-%m-%d %H:%M", tz = "UTC"), proc.time()[["elapsed"]] - t0),
         "", sprintf("**%s** (exit status %d). Regenerated %d production and %d dev datasets; %d + %d truth files and %d of 6 pilot copies compared; %d failed checks.",
                     status, code, n_ds[["prod"]], n_ds[["dev"]], n_truth[["prod"]], n_truth[["dev"]], n_copies, nrow(mm)),
         "", "Not an identity check (D44): exact on what the fits consume (file SHA-256, manifest hashes of the sealed arrays, seeds, foldid, names, dims, non-float fields); regenerated floating-point arrays within |delta| <= 1e-12 * max(1, |sealed|).",
         "", sprintf("Bit-identical regenerated arrays (information only): %d of %d.", bit[["identical"]], bit[["compared"]]),
         "", "Observed maxima (regenerated vs sealed):", "", "| Array | Comparisons | max abs delta | max scaled delta | bound |", "|---|---|---|---|---|",
         if (nrow(mxd)) sprintf("| %s | %d | %.3g | %.3g | %.0e |", mxd$array, as.integer(mxd$comparisons), mxd$max_abs_delta, mxd$max_scaled_delta, mxd$bound) else "| (none) | | | | |")
  if (length(incomplete)) L <- c(L, "", "Missing or malformed prerequisites (INCOMPLETE is never a PASS):", paste0("- ", utils::head(incomplete, 30)))
  if (nrow(mm)) L <- c(L, "", "**STOP.** Keep the evidence (this report, the mismatch and maxima CSVs, the local manifests and sealed files) and diagnose. The sealed local files stay canonical; changing the canonical source is an explicit HQ decision followed by a new audited seal, manifest and transfer. Do not regenerate.",
                    "", "First failed checks:", utils::capture.output(print(utils::head(mm, 10), row.names = FALSE)))
  writeLines(L, file.path(out, "NOTS_REGEN_REPORT.md")); cat(paste(L, collapse = "\n"), "\n")
  invisible(list(status = status, code = code, mismatches = mm, incomplete = incomplete, maxima = mxd))
}

if (sys.nframe() == 0L) {
  a <- commandArgs(trailingOnly = TRUE); opt <- list()
  i <- 1L; ok <- TRUE
  while (i <= length(a)) { if (!startsWith(a[i], "--") || i == length(a)) { ok <- FALSE; break }; opt[[sub("^--", "", a[i])]] <- a[i + 1L]; i <- i + 2L }
  if (!ok || is.null(opt$manifests) || is.null(opt$out) || !all(names(opt) %in% c("manifests", "dev-manifests", "study", "out"))) {
    message("usage: lowp_verify_nots.R --manifests DIR --out DIR --study DIR [--dev-manifests DIR]"); quit(status = 3L) }
  res <- tryCatch(lowp_verify_nots(opt$manifests, opt$out, opt[["dev-manifests"]], opt$study),
                  error = function(e) { message("FATAL (malformed input): ", conditionMessage(e)); list(code = 3L) })
  quit(status = res$code)
}
