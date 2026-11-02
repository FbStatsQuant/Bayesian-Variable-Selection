# extract_bench.R -- benchmark rule rows (INTERFACES I4) and the result-root scanner.
# Rows carry the master III.3.0 frame: rule_id, role, status, support, k, diag_flag, runtime_s, adaptation_ids, ...
RULE_COLS <- c("case_id", "dataset_id", "method_id", "rule_id", "role", "status", "support", "runtime_s", "diag_flag", "diag_codes", "adaptation_ids")

read_rule_rows <- function(path_rds) {
  x <- read_rds_safe(path_rds)
  if (is.null(x)) return(NULL)
  if (!is.data.frame(x) && is.list(x) && is.data.frame(x$rows)) x <- x$rows
  if (!is.data.frame(x)) return(NULL)
  x <- as.data.frame(x, stringsAsFactors = FALSE)
  for (nm in c("case_id", "method_id", "rule_id", "role", "status", "support", "adaptation_ids")) if (!nm %in% names(x)) x[[nm]] <- NA_character_
  if (!"runtime_s" %in% names(x)) x$runtime_s <- NA_real_
  if (!"diag_flag" %in% names(x)) x$diag_flag <- NA
  if (!"diag_codes" %in% names(x)) x$diag_codes <- NA_character_
  if (!"dataset_id" %in% names(x)) x$dataset_id <- sub("_c[0-9]{3}$", "", x$case_id)
  x[, RULE_COLS, drop = FALSE]
}

# Scan result roots (results/{run_id}/p{pppp}/{case or dataset dir}/...). A unit counts only if its .done marker exists
# (EXACT units are returned whenever an EXACT.rds exists; their readiness is checked by load_exact_checked()).
# Duplicates (same unit in several roots) are resolved BEFORE scoring: identical copies are merged; conflicting copies are an error unless
# on_conflict = "first_root" (explicit precedence = the order of `result_dirs`). Every duplicate is listed in $duplicates.
# Returns list(smc = list(file, case_id, rep, root), bench = data.frame, exact = named character (dataset_id -> path), duplicates = data.frame)
scan_results <- function(result_dirs, on_conflict = c("error", "first_root")) {
  on_conflict <- match.arg(on_conflict)
  smc <- list(); bench <- list(); exact <- list(); dups <- list()
  note <- function(kind, key, files, resolution) dups[[length(dups) + 1L]] <<- data.frame(kind = kind, key = key, n_copies = length(files), files = paste(files, collapse = " | "), resolution = resolution, stringsAsFactors = FALSE)
  for (ri in seq_along(result_dirs)) {
    rd <- result_dirs[ri]
    pdirs <- list.dirs(rd, recursive = FALSE, full.names = TRUE)
    pdirs <- pdirs[grepl("p[0-9]{4}$", basename(pdirs))]
    for (pd in pdirs) for (cd in list.dirs(pd, recursive = FALSE, full.names = TRUE)) {
      id <- basename(cd)
      for (f in list.files(cd, pattern = "\\.rds$", full.names = TRUE)) {
        b <- sub("\\.rds$", "", basename(f))
        if (b == "EXACT") { exact[[id]] <- c(exact[[id]], list(f)); next }
        if (!file.exists(sub("\\.rds$", ".done", f))) next
        m <- regmatches(b, regexec("^SMCBVS(_rep([0-9]+))?$", b))[[1L]]
        if (length(m)) {
          rp <- if (nzchar(m[3L])) as.integer(m[3L]) else 0L
          smc[[length(smc) + 1L]] <- list(file = f, case_id = id, rep = rp, root = ri)
        } else {
          rr <- read_rule_rows(f)
          if (!is.null(rr)) { rr$case_id <- ifelse(is.na(rr$case_id), id, rr$case_id); rr$.file <- f; rr$.root <- ri; bench[[length(bench) + 1L]] <- rr }
        }
      }
    }
  }
  resolve <- function(kind, key, files, identical_) {
    if (length(files) <= 1L) return(TRUE)
    if (identical_) { note(kind, key, files, "identical copies merged"); return(TRUE) }
    if (on_conflict == "error") stop("conflicting duplicate results for ", kind, " ", key, ": ", paste(files, collapse = " ; "), " (use on_conflict = 'first_root' to apply root precedence)")
    note(kind, key, files, "conflict: first root wins"); TRUE
  }
  # SMC: unit = (case_id, rep)
  if (length(smc)) {
    keys <- vapply(smc, function(x) paste(x$case_id, x$rep, sep = "#"), "")
    keep <- list()
    for (k in unique(keys)) {
      ix <- which(keys == k); cand <- smc[ix]; cand <- cand[order(vapply(cand, function(x) x$root, 0L))]
      hs <- vapply(cand, function(x) file_sha256(x$file), "")
      resolve("SMC", k, vapply(cand, function(x) x$file, ""), length(unique(hs)) == 1L)
      keep[[length(keep) + 1L]] <- cand[[1L]]
    }
    smc <- keep
  }
  # EXACT: unit = dataset_id
  ex_out <- character(0)
  for (id in names(exact)) {
    fs <- unlist(exact[[id]]); roots_ <- vapply(fs, function(f) which(vapply(result_dirs, function(r) startsWith(normalizePath(f, winslash = "/"), normalizePath(r, winslash = "/")), TRUE))[1L], 0L)
    fs <- fs[order(roots_)]
    hs <- vapply(fs, file_sha256, "")
    resolve("EXACT", id, fs, length(unique(hs)) == 1L)
    ex_out[id] <- fs[1L]
  }
  # benchmark rows: unit = (case_id, method_id, rule_id); identical = same status and support
  bdf <- NULL
  if (length(bench)) {
    bdf <- do.call(rbind, bench)
    bkey <- paste(bdf$case_id, bdf$method_id, bdf$rule_id, sep = "|")
    drop <- rep(FALSE, nrow(bdf))
    for (k in unique(bkey[duplicated(bkey)])) {
      ix <- which(bkey == k); ix <- ix[order(bdf$.root[ix])]
      same <- length(unique(do.call(paste, c(lapply(bdf[ix, RULE_COLS, drop = FALSE], as.character), sep = "\r")))) == 1L   # identity = the FULL row (status, support, role, flags, codes, runtime ...)
      resolve("BENCH", k, bdf$.file[ix], same)
      drop[ix[-1L]] <- TRUE
    }
    bdf <- bdf[!drop, , drop = FALSE]
    bdf <- bdf[, c(RULE_COLS), drop = FALSE]
  }
  list(smc = smc, bench = bdf, exact = ex_out, duplicates = if (length(dups)) do.call(rbind, dups) else data.frame(kind = character(0), key = character(0), n_copies = integer(0), files = character(0), resolution = character(0)))
}
