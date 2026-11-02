# cmp2.R -- hardened bit-identity comparator, v2.1 (x) vs v2.2 (y).  Round 2 (CONF thread).
# Amendment D20 (2026-10-29, CONF-2b): shape_cmp skips the length check for record$environment$command only. Pre-D20 copy: conformance/work/regression2/cmp2.R.
#
# Rules (REGRESSION_REVIEW_sol.md findings 2, 3, 7):
#  * leaves: identical(x, y, num.eq = FALSE, single.NA = FALSE, attrib.as.set = FALSE)  (+ bytewise
#    writeBin() comparison for double/complex vectors) and typeof() equality for every container;
#    attributes are compared recursively and in order.
#  * additions: a path of y absent from x is allowed ONLY if it is in CMP2_ADD below (container path ->
#    ordered vector of allowed names).  The full name vector of every pre-existing named list must be a
#    PREFIX of y's name vector (so no insertion before an old element, no drop, no reorder), and the
#    appended names must follow the allowlist order.  Unnamed lists/vectors/data frames may not change
#    length; data-frame columns may not change.
#  * exemptions: ONLY the exact generalised paths listed in CMP2_EXEMPT_* ([[3]] -> [*]).  Their values are
#    not compared, but typeof / length / names / attributes (recursively for lists) are.  The
#    exact-branch-only preflight estimates are exempt only when the v2.1 fit's branch_run is "exact";
#    on SMC fits they are compared and must be identical (NA).
#  * round 3 (N2/N3): the FULL attribute-name vector (incl. "names") is compared in order before any value;
#    the names VALUE is compared by the prefix/allowlist rule; the suffix of extra names is taken explicitly
#    (works for empty named baseline lists); record$code$files is checked as a provenance vector:
#    unique names, deterministic expected name vector (v2.1 names + core/cpp/v3_registry.h at its radix/C-locale
#    sorted position among the core/ labels; or unchanged in mode "identity"), equal length/attributes, every hash a
#    scalar character of 64 lowercase hex chars; parent attributes compared.
# Every exemption actually used is returned (and printed by cmp2_print_exemptions()).

cmp2_gp <- function(p) gsub("\\[\\[[0-9]+\\]\\]", "[*]", p)

# ---- additions allowlist (paths relative to the root "fit"; "record$fit..." is derived automatically)
ISLAND_ADD <- c("pip_plain", "plain_acc", "plain_round")
FIT_ADD    <- c("pip_plain_r", "pip_plain", "mpm_plain", "instrumentation")
REC_ADD    <- c("pip_plain", "mpm_plain", "instrumentation")
CMP2_ISLAND_CONTAINERS <- c(
  "fit$stage_record[*]",
  "fit$partial_final$islands[*]",
  "fit$calibration$tiers[*]$pilot$stage_record",
  "fit$calibration$tiers[*]$iterations[*]$stage_record[*]",
  "fit$calibration$tiers[*]$partial_operation$island",
  "fit$calibration$tiers[*]$partial_operation$islands[*]")
cmp2_add_table <- function() {
  tb <- list()
  tb[["fit"]] <- FIT_ADD; tb[["record$fit"]] <- FIT_ADD; tb[["record"]] <- REC_ADD
  for (cc in CMP2_ISLAND_CONTAINERS) { tb[[cc]] <- ISLAND_ADD; tb[[sub("^fit", "record$fit", cc)]] <- ISLAND_ADD }
  tb
}
CMP2_ADD <- cmp2_add_table()

# ---- exemptions (exact generalised paths, relative to "fit"; copied for "record$fit")
# time leaves (value not compared)
CMP2_EXEMPT_FIT <- c(
  "fit$peak_memory_kb",
  "fit$runtime_guard$elapsed_seconds",
  "fit$runtime_guard$checkpoints[*]$elapsed_seconds",
  "fit$runtime_guard$checkpoints[*]$operation_seconds",
  "fit$runtime_guard$checkpoints[*]$projected_seconds")
CMP2_EXEMPT_FIT_TREES <- c("fit$timings")        # whole subtree, shape only
CMP2_EXEMPT_EXACT_ONLY <- c("fit$preflight$est_seconds", "fit$preflight$seconds_per_score")  # only if branch_run == "exact"
# 'seconds' elements: filled from discovery (see CMP2_SECONDS below)
CMP2_SECONDS <- c(
  "fit$calibration$seconds",
  "fit$calibration$tiers[*]$grid_construction$seconds",
  "fit$calibration$tiers[*]$grids[*]$seconds",
  "fit$calibration$tiers[*]$iterations[*]$seconds",
  "fit$calibration$tiers[*]$iterations[*]$stage_record[*]$seconds",
  "fit$calibration$tiers[*]$partial_operation$seconds",
  "fit$calibration$tiers[*]$partial_operation$island$seconds",
  "fit$calibration$tiers[*]$partial_operation$islands[*]$seconds",
  "fit$calibration$tiers[*]$pilot$seconds",
  "fit$calibration$tiers[*]$pilot$stage_record$seconds",
  "fit$calibration$tiers[*]$seconds",
  "fit$calibration$tiers[*]$seconds_total",
  "fit$partial_final$islands[*]$seconds",
  "fit$partial_final$seconds_local",
  "fit$partial_final$seconds_total",
  "fit$stage_record[*]$seconds")
# study-record provenance (relative to "record")
CMP2_EXEMPT_REC <- c("record$started_utc", "record$finished_utc", "record$runtime_s", "record$adapter_version",
                     "record$input$manifest_path", "record$input$input_path",   # file-system paths of the (hash-identical) inputs copy; manifest_sha256 / inputs_sha256 / x_sha256 / y_sha256 ARE compared
                     "record$rows$started_utc", "record$rows$finished_utc", "record$rows$runtime_s", "record$rows$run_id",
                     "record$rows$source_sha256", "record$rows$v3_source_sha256", "record$rows$host",
                     "record$rows$slurm_job_id", "record$rows$slurm_array_task_id")
CMP2_EXEMPT_REC_TREES <- c("record$environment")   # host, pid, slurm_*, session, command ... (shape only)
# record$code: shape only, except code$files (sha256 per source file; v2.2 has one extra file entry core/cpp/v3_registry.h; see cmp2_code_files)
CMP2_CODE_FILES_EXTRA <- "core/cpp/v3_registry.h"
source_cmp2_lists <- function(file) { if (file.exists(file)) sys.source(file, envir = globalenv()) }

cmp2_exempt_sets <- function() {
  rel <- c(CMP2_EXEMPT_FIT, CMP2_SECONDS); relT <- CMP2_EXEMPT_FIT_TREES; ex <- CMP2_EXEMPT_EXACT_ONLY
  add <- function(v) c(v, sub("^fit", "record$fit", v))
  list(leaf = c(add(rel), CMP2_EXEMPT_REC), tree = c(add(relT), CMP2_EXEMPT_REC_TREES), exact_only = add(ex))
}

# ---------------------------------------------------------------------------------------------------
cmp2_new <- function(exact, code_files = "cross") { e <- new.env(); e$code_files <- code_files; e$n <- 0L; e$diffs <- character(); e$added <- character()
  e$added_bad <- character(); e$exempt <- character(); e$exact <- exact; e$S <- cmp2_exempt_sets(); e }
cmp2_diff <- function(e, path, why) e$diffs <- c(e$diffs, paste0(path, " [", why, "]"))

is_data_leaf <- function(x) is.atomic(x) || is.null(x)
bits_equal <- function(x, y) {
  if (!(is.double(x) || is.complex(x))) return(TRUE)
  r <- tryCatch(identical(writeBin(as.vector(x), raw()), writeBin(as.vector(y), raw())), error = function(e) FALSE)
  isTRUE(r)
}
leaf_identical <- function(x, y)
  identical(x, y, num.eq = FALSE, single.NA = FALSE, attrib.as.set = FALSE, ignore.bytecode = FALSE,
            ignore.environment = FALSE, ignore.srcref = FALSE) && bits_equal(x, y)

# shape-only comparison used under exemptions: typeof, length, names, attribute names/order and (for lists)
# recursion; atomic attributes (dim, dimnames, class, ...) must be identical.
shape_cmp <- function(x, y, path, e) {
  e$n <- e$n + 1L
  if (!identical(typeof(x), typeof(y))) return(cmp2_diff(e, path, "exempt value: typeof differs"))
  # D20 (Sol, SOL_IDENTITY_RESULT.md): the CLI argv vector is recorded provenance whose length depends on the option form; skip ONLY its length check.
  if (length(x) != length(y) && path != "record$environment$command") return(cmp2_diff(e, path, "exempt value: length differs"))
  if (!identical(names(x), names(y))) return(cmp2_diff(e, path, "exempt value: names differ"))
  ax <- attributes(x); ay <- attributes(y)
  if (!identical(names(ax), names(ay))) return(cmp2_diff(e, path, "exempt value: attribute names/order differ"))
  if (is.list(x)) {
    for (n in setdiff(names(ax), "names")) if (!leaf_identical(ax[[n]], ay[[n]])) cmp2_diff(e, paste0(path, "@", n), "exempt value: attribute differs")
    for (i in seq_along(x)) shape_cmp(x[[i]], y[[i]], paste0(path, if (!is.null(names(x)) && nzchar(names(x)[i])) paste0("$", names(x)[i]) else paste0("[[", i, "]]")), e)
  } else if (!identical(ax, ay)) cmp2_diff(e, path, "exempt value: attributes differ")
  invisible()
}

cmp2_attrs <- function(x, y, path, e) {
  ax <- attributes(x); ay <- attributes(y)
  # the full attribute-name vector (including "names") must agree in order; the names VALUE is compared by the
  # prefix/allowlist rule in the list branch, so it is dropped from the value loop only.
  if (!identical(names(ax), names(ay))) { cmp2_diff(e, path, "attribute names/order differ"); return(invisible()) }
  ax$names <- NULL; ay$names <- NULL
  for (n in names(ax)) cmp2_obj(ax[[n]], ay[[n]], paste0(path, "@", n), e)
}

# record$code$files: named vector (or list) of per-file sha256 labels.  Values are not compared; structure is.
cmp2_hash_ok <- function(h) {
  one <- function(v) is.null(attributes(v)) && is.character(v) && length(v) == 1L && !is.na(v) && nchar(v) == 64L && grepl("^[0-9a-f]{64}$", v)
  if (is.list(h)) length(h) > 0L && all(vapply(h, one, TRUE)) else is.character(h) && length(h) > 0L && !anyNA(h) && all(nchar(h) == 64L) && all(grepl("^[0-9a-f]{64}$", h))
}
cmp2_code_expected_names <- function(nx, mode) {
  if (mode == "identity") return(nx)
  new <- CMP2_CODE_FILES_EXTRA
  ic <- which(startsWith(nx, "core/"))
  if (!length(ic)) return(c(nx, new))
  srt <- sort(c(nx[ic], new), method = "radix")          # C-locale byte order, as the adapter sorts
  k <- min(ic) - 1L + match(new, srt)                    # position of the new label in the full vector
  append(nx, new, after = k - 1L)
}
cmp2_code_files <- function(fx, fy, path, e) {
  bad <- function(why) { cmp2_diff(e, path, paste0("exempt value: code files: ", why)); invisible() }
  if (!identical(typeof(fx), typeof(fy))) return(bad("typeof differs"))
  nx <- names(fx); ny <- names(fy)
  if (is.null(nx) || is.null(ny) || anyNA(nx) || anyNA(ny)) return(bad("files unnamed / NA names"))
  if (anyDuplicated(nx)) return(bad("duplicate file names in the baseline"))
  if (anyDuplicated(ny)) return(bad(paste0("duplicate file names: ", paste(unique(ny[duplicated(ny)]), collapse = ","))))
  if (e$code_files == "cross" && CMP2_CODE_FILES_EXTRA %in% nx) return(bad("baseline already contains the registry header"))
  expect <- cmp2_code_expected_names(nx, e$code_files)
  if (length(fy) != length(expect)) return(bad(sprintf("length %d, expected %d (%s mode)", length(fy), length(expect), e$code_files)))
  if (!identical(ny, expect)) return(bad("name vector differs from the expected one (baseline names + registry header at its sorted position)"))
  ax <- attributes(fx); ay <- attributes(fy)
  if (!identical(names(ax), names(ay))) return(bad("attribute names/order differ"))
  for (n in setdiff(names(ax), "names")) if (!leaf_identical(ax[[n]], ay[[n]])) bad(paste0("attribute '", n, "' differs"))
  if (!cmp2_hash_ok(fx)) bad("baseline hash element(s) not scalar 64-hex character")
  if (!cmp2_hash_ok(fy)) bad("hash element(s) not scalar 64-hex character")
  invisible()
}

cmp2_obj <- function(x, y, path, e) {
  gp <- cmp2_gp(path)
  S <- e$S
  if (gp == "record$code") {   # custom: children shape-only; files = provenance vector (see cmp2_code_files)
    e$exempt <- c(e$exempt, paste0("record$code (shape only; files: ", if (e$code_files == "cross") "+core/cpp/v3_registry.h required" else "unchanged (identity mode)", ")")); e$n <- e$n + 1L
    if (!identical(typeof(x), typeof(y)) || !identical(names(x), names(y))) return(cmp2_diff(e, path, "exempt value: code typeof/names differ"))
    ax <- attributes(x); ay <- attributes(y)
    if (!identical(names(ax), names(ay))) cmp2_diff(e, path, "exempt value: code attribute names/order differ")
    else for (n in setdiff(names(ax), "names")) if (!leaf_identical(ax[[n]], ay[[n]])) cmp2_diff(e, paste0(path, "@", n), "exempt value: code attribute differs")
    for (nm in names(x)) {
      if (nm == "files") cmp2_code_files(x$files, y$files, paste0(path, "$files"), e)
      else shape_cmp(x[[nm]], y[[nm]], paste0(path, "$", nm), e)
    }
    return(invisible())
  }
  if (gp %in% S$tree || gp %in% S$leaf || (e$exact && gp %in% S$exact_only)) {
    e$exempt <- c(e$exempt, gp); return(shape_cmp(x, y, path, e))
  }
  if (is.environment(x) || is.function(x) || typeof(x) %in% c("externalptr", "S4", "language", "symbol", "builtin", "special", "closure")) {
    e$n <- e$n + 1L
    if (!identical(typeof(x), typeof(y)) || !identical(class(x), class(y))) cmp2_diff(e, path, "non-data object: type/class")
    e$exempt <- c(e$exempt, paste0("(non-data object, type/class only) ", gp)); return(invisible())
  }
  if (!is.list(x)) {   # leaf (atomic vector or NULL)
    e$n <- e$n + 1L
    if (!identical(typeof(x), typeof(y))) { cmp2_diff(e, path, "typeof"); return(invisible()) }
    if (!leaf_identical(x, y)) {
      why <- if (!identical(attributes(x), attributes(y))) "attributes" else if (length(x) != length(y)) "length" else "value/bits"
      cmp2_diff(e, path, why)
    }
    return(invisible())
  }
  # ---- list (incl. data frame)
  e$n <- e$n + 1L
  if (!identical(typeof(x), typeof(y))) { cmp2_diff(e, path, "typeof"); return(invisible()) }
  nx <- names(x); ny <- names(y)
  allowed <- CMP2_ADD[[gp]]
  pos_y <- seq_along(x)
  if (is.null(nx)) {
    if (!is.null(ny) || length(y) != length(x)) { cmp2_diff(e, path, sprintf("unnamed list: length %d -> %d / names", length(x), length(y))); if (length(y) < length(x)) return(invisible()) }
  } else {
    pref <- length(ny) >= length(nx) && identical(ny[seq_along(nx)], nx)
    if (!pref) {
      cmp2_diff(e, path, sprintf("old name vector is not a prefix of the new one (dropped: [%s]; inserted/reordered: [%s])",
                                 paste(setdiff(nx, ny), collapse = ","), paste(setdiff(ny, nx), collapse = ",")))
      pos_y <- match(nx, ny); pos_y[is.na(pos_y)] <- 0L   # keep going by name for diagnostics
    } else if (length(ny) > length(nx)) {
      extra <- ny[seq.int(length(nx) + 1L, length(ny))]   # explicit suffix (also correct when nx is an empty named list)
      ok <- extra %in% allowed
      for (k in seq_along(extra)) {
        pth <- paste0(path, "$", extra[k])
        if (ok[k]) e$added <- c(e$added, pth) else { e$added_bad <- c(e$added_bad, pth); cmp2_diff(e, pth, "added element not on the allowlist") }
      }
      if (any(ok)) {
        m <- match(extra[ok], allowed)
        if (anyDuplicated(m) || is.unsorted(m, strictly = TRUE)) cmp2_diff(e, path, sprintf("allowed additions in wrong order/duplicated: %s (required order: %s)", paste(extra[ok], collapse = ","), paste(allowed, collapse = ",")))
      }
    }
  }
  cmp2_attrs(x, y, path, e)
  for (i in seq_along(x)) {
    nm <- if (!is.null(nx) && nzchar(nx[i])) nx[i] else NA_character_
    p <- if (!is.na(nm)) paste0(path, "$", nm) else paste0(path, "[[", i, "]]")
    j <- pos_y[i]
    if (j == 0L || j > length(y)) { cmp2_diff(e, p, "missing in v2.2"); next }
    cmp2_obj(x[[i]], y[[j]], p, e)
  }
  invisible()
}

# x = v2.1 object, y = v2.2 object, root = "fit" or "record"
# code_files: "cross" (default; v2.1 vs v2.2 record: exactly one new entry, core/cpp/v3_registry.h) or
# "identity" (record compared with itself / same-version control: no new entry allowed).
cmp2_run <- function(x, y, root = "fit", code_files = c("cross", "identity")) {
  code_files <- match.arg(code_files)
  exact <- identical(if (root == "fit") x$branch_run else x$fit$branch_run, "exact")
  e <- cmp2_new(exact, code_files); cmp2_obj(x, y, root, e)
  list(n_compared = e$n, n_diff = length(e$diffs), diffs = e$diffs, added = e$added, added_bad = e$added_bad,
       exempt = sort(table(e$exempt), decreasing = TRUE))
}
cmp2_print_exemptions <- function(r) { if (length(r$exempt)) cat(paste0("  ", names(r$exempt), "  x", as.integer(r$exempt)), sep = "\n") else cat("  (none)\n") }
