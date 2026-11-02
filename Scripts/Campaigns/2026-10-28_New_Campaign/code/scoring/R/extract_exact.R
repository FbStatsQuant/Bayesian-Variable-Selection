# extract_exact.R -- reads EXACT.rds (INTERFACES I2) and returns one normalised list per scale.
# top: data.frame(rank, F, size, model (text), mask (double, bit j-1 = variable j)).
# Readiness (review finding 10): an EXACT unit is used only if EXACT.done and EXACT.sha256 exist and agree with the SHA-256 of the RDS, the envelope
# is schema lowp_exact_v1 for this dataset and p, and its run status is "exact" and complete (a "partial" subset run is refused).
exact_path <- function(results_dir, dataset_id) {
  p <- as.integer(substr(dataset_id, 2, 5))
  file.path(results_dir, sprintf("p%04d", p), dataset_id, "EXACT.rds")
}
.first_hash <- function(f) { l <- tryCatch(readLines(f, n = 1L, warn = FALSE), error = function(e) character(0)); if (length(l)) tolower(sub("^([0-9a-fA-F]{64}).*$", "\\1", l[1L])) else NA_character_ }

# The strict shared EXACT-record validator (code/lowp/enum/exact_contract.R::lowp_validate_exact, INTERFACES I2), sourced on demand.
exact_contract_file <- function() { e <- Sys.getenv("SCORING_ENUM_DIR", ""); file.path(if (nzchar(e)) e else file.path(dirname(SC_DIR), "lowp", "enum"), "exact_contract.R") }
ensure_exact_contract <- function() {
  if (!exists("lowp_validate_exact", mode = "function")) { f <- exact_contract_file(); if (!file.exists(f)) stop("exact_contract.R not found at ", f); source(f, local = FALSE) }
  invisible(TRUE)
}

# returns list(ok, reason, detail, ex). Layers: .done marker + SHA-256 sidecar agree with the RDS (this file); then the record must pass
# lowp_validate_exact(record, requested_scales, input, mode = "sealed") -- complete counts derived from the retained p and K, every requested
# scale present with status exact / scope full, input binding (n, p, retained = non-constant columns, file and manifest SHA-256 when given).
# `reason` is a short code; `detail` carries ALL validator reasons (logged in exact_diagnostics.csv).
load_exact_checked <- function(path, dataset_id, p, input = NULL, requested_scales = c("c100", "c050"), mode = "sealed") {
  bad <- function(why, detail = why) list(ok = FALSE, reason = why, detail = detail, ex = NULL)
  d <- dirname(path)
  f_done <- file.path(d, "EXACT.done"); f_sha <- file.path(d, "EXACT.sha256")
  if (!file.exists(path)) return(bad("rds_missing"))
  if (!file.exists(f_done)) return(bad("no_done_marker"))
  if (!file.exists(f_sha)) return(bad("no_sha256_sidecar"))
  h <- file_sha256(path)
  if (!identical(.first_hash(f_sha), h)) return(bad("sha256_sidecar_mismatch"))
  hd <- .first_hash(f_done)
  if (!is.na(hd) && !identical(hd, h)) return(bad("done_marker_hash_mismatch"))
  ex <- read_rds_safe(path)
  if (is.null(ex) || !is.list(ex$scales)) return(bad("unreadable_or_no_scales"))
  if (!identical(as.character(ex$dataset_id), dataset_id)) return(bad("dataset_id_mismatch"))
  if (!is.null(p) && !is.na(p) && !identical(as.integer(ex$p), as.integer(p))) return(bad("p_mismatch"))
  ensure_exact_contract()
  inp <- if (is.null(input)) list(dataset_id = dataset_id) else c(list(dataset_id = dataset_id), input)
  v <- lowp_validate_exact(ex, requested_scales = requested_scales, input = inp, mode = mode)
  if (!isTRUE(v$ok)) return(bad(paste0("contract: ", v$reasons[1L], if (length(v$reasons) > 1L) paste0(" (+", length(v$reasons) - 1L, " more)") else ""), paste(v$reasons, collapse = " | ")))
  list(ok = TRUE, reason = "ok", detail = "", ex = ex)
}
read_exact <- function(path) { x <- read_rds_safe(path); if (is.null(x) || is.null(x$scales)) NULL else x }

# normalise <S> of one scale. PIPs are expanded to the input p through the retained-column map (names = original indices, as lowp_exact returns them).
exact_scale <- function(ex, scale_key) {
  S <- ex$scales[[scale_key]]
  if (is.null(S)) return(NULL)
  p <- as.integer(ex$p)
  kept <- ex$extra$retained_columns
  pv <- as.numeric(S$pip); nm <- names(S$pip)
  pip <- NULL
  if (!is.null(nm)) {
    idx <- suppressWarnings(as.integer(nm))
    if (!anyNA(idx) && all(idx >= 1L & idx <= p) && !anyDuplicated(idx) && (is.null(kept) || setequal(idx, as.integer(kept)))) {
      pip <- setNames(rep(0, p), as.character(seq_len(p))); pip[as.character(idx)] <- pv
    }
  } else if (length(pv) == p) { pip <- setNames(pv, as.character(seq_len(p))); idx <- seq_len(p) }
  if (is.null(pip) || !valid_prob_vec(unname(pip), p)) return(NULL)                      # finite probabilities in [0, 1]
  if (!is.finite(as.numeric(S$log_Z))) return(NULL)
  list(dataset_id = ex$dataset_id, p = p, scale_key = scale_key, log_Z = as.numeric(S$log_Z),
       log_m0 = as.numeric(S$log_m0 %||% NA), pip = pip, kept = sort(as.integer(idx)),
       hpm = parse_support(S[["hpm"]]), hpm_F = as.numeric(S$hpm_F), mpm = parse_support(S[["mpm"]]),
       margin = as.numeric(S$margin %||% NA), global_certified = S$global_certified %||% NA,
       size_logmass = S$size_logmass, top = S$top, K = ex$K %||% NA)
}
# F of model S if it is in the stored top list (NA otherwise)
exact_top_F <- function(es, S) {
  if (is.null(es$top) || !nrow(es$top)) return(NA_real_)
  i <- match(support_mask(S), es$top$mask)
  if (is.na(i)) NA_real_ else es$top$F[i]
}
