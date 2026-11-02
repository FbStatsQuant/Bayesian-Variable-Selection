# exact_contract.R -- the ONE strict validator of the EXACT record contract (INTERFACES §I2). Base R only; no compilation, no core.
# Used by run_enum_dataset.R (resume and post-commit check) and meant to be called by the scoring and pilot code.
#
#   source("<enum dir>/exact_contract.R")
#   v <- lowp_validate_exact(record, requested_scales = c("c100", "c050"), input = NULL, mode = c("sealed", "unsealed_test"))
#   v$ok        TRUE only if every check below passes
#   v$reasons   character vector, one entry per failed check (character(0) when ok)
#
# record            the EXACT record (readRDS of EXACT.rds)
# requested_scales  scale keys the caller needs; each must be present with status "exact" and scope "full".  The record's scale set
#                   must equal this set exactly when `exact_scale_set = TRUE` (the CLI resume uses that; consumers can pass FALSE to accept a
#                   superset).  Default: c("c100", "c050")
# input             NULL, or the dataset the record must belong to: a list with `X` (the n x p input matrix, original columns) and optionally
#                   `dataset_id`, `file_sha256` (SHA-256 of the input file) and `manifest_sha256` (SHA-256 of the inputs manifest).  Every
#                   element that is given is compared with the record
# mode              "sealed" (default) or "unsealed_test": the record's extra$input_mode must equal it; sealed records must also carry
#                   manifest_checked = TRUE, a 64-hex manifest_sha256 and a 64-hex input_file_sha256
#
# Coverage is derived from the RETAINED columns (extra$retained_columns, after constant columns were dropped): p_ret = their number,
# K = min(p_ret, floor(n/2)), models_expected = sum_{k<=K} choose(p_ret, k); record$p is the ORIGINAL number of input columns.
# The source fingerprint is not checked here (the validator does not know the current sources); callers compare record$source_sha256
# with their own fingerprint.  An empty HPM (integer(0)) is valid.

lowp_validate_exact <- function(record, requested_scales = c("c100", "c050"), input = NULL, mode = c("sealed", "unsealed_test"),
                                exact_scale_set = FALSE) {
  mode <- match.arg(mode)
  reasons <- character(0)
  bad <- function(...) reasons <<- c(reasons, paste0(...))
  hex64 <- function(x) is.character(x) && length(x) == 1L && !is.na(x) && grepl("^[0-9a-f]{64}$", x)
  num1 <- function(x) is.numeric(x) && length(x) == 1L && is.finite(x)
  KIND <- "heuristic (not a validated interval bound)"
  lse <- function(x) { if (!length(x) || anyNA(x) || any(is.infinite(x) & x > 0)) return(NaN); m <- max(x); if (!is.finite(m)) return(-Inf); m + log(sum(exp(x - m))) }
  if (!is.list(record)) return(list(ok = FALSE, reasons = "record is not a list"))
  need_top <- c("schema", "dataset_id", "p", "n", "K", "source_sha256", "v3_score_sha256", "runtime_s", "host", "started_utc", "finished_utc",
                "models_scored", "models_expected", "complete", "threads", "extra", "scales")
  miss <- setdiff(need_top, names(record))
  if (length(miss)) { bad("missing top-level fields: ", paste(miss, collapse = ",")); return(list(ok = FALSE, reasons = reasons)) }
  if (!identical(record$schema, "lowp_exact_v1")) bad("schema is not lowp_exact_v1")
  if (!is.character(record$dataset_id) || length(record$dataset_id) != 1L || !grepl("^(dev_)?p[0-9]{4}_S[1-6]_r[0-9]{3}$", record$dataset_id)) bad("dataset_id malformed")
  for (nm in c("p", "n", "K", "models_scored", "models_expected", "threads", "runtime_s")) if (!num1(record[[nm]])) bad(nm, " is not a finite number")
  for (nm in c("source_sha256", "v3_score_sha256")) if (!hex64(record[[nm]])) bad(nm, " is not a 64-hex SHA-256")
  for (nm in c("host", "started_utc", "finished_utc")) if (!is.character(record[[nm]]) || length(record[[nm]]) != 1L || is.na(record[[nm]]) || !nzchar(record[[nm]])) bad(nm, " is missing or empty")
  ex <- record$extra
  if (!is.list(ex)) { bad("extra is not a list"); return(list(ok = FALSE, reasons = reasons)) }
  need_ex <- c("input_mode", "manifest_checked", "manifest_sha256", "input_file_sha256", "status", "complete", "models_expected", "retained_columns")
  miss <- setdiff(need_ex, names(ex))
  if (length(miss)) { bad("missing extra fields: ", paste(miss, collapse = ",")); return(list(ok = FALSE, reasons = reasons)) }
  ## ---- dimensions and coverage, derived from the retained columns ----
  ret <- ex$retained_columns
  if (!is.numeric(ret) || !length(ret) || anyNA(ret) || any(ret != round(ret)) || is.unsorted(ret, strictly = TRUE) || any(ret < 1)) {
    bad("retained_columns is not a non-empty strictly increasing integer vector"); return(list(ok = FALSE, reasons = reasons)) }
  ret <- as.integer(ret); pret <- length(ret)
  if (num1(record$p) && (max(ret) > record$p || pret > record$p)) bad("retained_columns exceed the original p")
  Kx <- NA_integer_; nexp <- NA_real_
  if (num1(record$n) && num1(record$K)) {
    Kx <- min(pret, floor(record$n / 2))
    if (record$K != Kx) bad("K = ", record$K, " but min(p_retained = ", pret, ", floor(n/2)) = ", Kx)
    nexp <- sum(choose(pret, 0:Kx))
    if (!(record$models_expected == nexp)) bad("models_expected = ", record$models_expected, " but sum_{k<=K} choose(p_retained, k) = ", nexp)
    if (!(nexp > 0)) bad("models_expected is not positive")
  }
  if (!(isTRUE(record$complete) && isTRUE(ex$complete))) bad("complete is not TRUE in both the top level and extra")
  if (!identical(ex$status, "exact")) bad("extra$status is not exact")
  if (num1(record$models_scored) && num1(record$models_expected)) {
    if (!(record$models_scored == record$models_expected && record$models_scored > 0)) bad("models_scored (", record$models_scored, ") != models_expected (", record$models_expected, ") or not positive")
  }
  if (!isTRUE(ex$models_expected == record$models_expected)) bad("extra$models_expected differs from the top-level models_expected")
  ## ---- input binding ----
  if (!identical(ex$input_mode, mode)) bad("input_mode is '", paste(ex$input_mode, collapse = ""), "' but '", mode, "' was requested")
  if (mode == "sealed") {
    if (!isTRUE(ex$manifest_checked)) bad("sealed record without manifest_checked = TRUE")
    if (!hex64(ex$manifest_sha256)) bad("sealed record without a 64-hex manifest_sha256")
    if (!hex64(ex$input_file_sha256)) bad("sealed record without a 64-hex input_file_sha256")
  } else if (isTRUE(ex$manifest_checked)) bad("unsealed_test record claims manifest_checked")
  if (!is.null(input)) {
    if (!is.list(input)) bad("input must be a list") else {
      if (!is.null(input$dataset_id) && !identical(as.character(input$dataset_id), record$dataset_id)) bad("dataset_id differs from the input's")
      if (!is.null(input$file_sha256) && !identical(tolower(input$file_sha256), ex$input_file_sha256)) bad("input file SHA-256 differs from the record's")
      if (!is.null(input$manifest_sha256) && !is.na(input$manifest_sha256) && !identical(tolower(input$manifest_sha256), ex$manifest_sha256)) bad("manifest SHA-256 differs from the record's")
      if (!is.null(input$X)) {
        X <- input$X
        if (!is.matrix(X)) bad("input$X is not a matrix") else {
          if (record$n != nrow(X)) bad("n = ", record$n, " but the input has ", nrow(X), " rows")
          if (record$p != ncol(X)) bad("p = ", record$p, " but the input has ", ncol(X), " columns")
          keep <- which(!apply(X, 2, function(x) all(x == x[1])))
          if (!identical(as.integer(keep), ret)) bad("retained_columns differ from the non-constant columns of the input")
        }
      }
    }
  }
  ## ---- scales ----
  sc <- record$scales
  if (!is.list(sc) || is.null(names(sc))) { bad("scales is not a named list"); return(list(ok = FALSE, reasons = reasons)) }
  if (exact_scale_set) { if (!identical(names(sc), requested_scales)) bad("scale set {", paste(names(sc), collapse = ","), "} differs from the requested {", paste(requested_scales, collapse = ","), "}") }
  for (s in requested_scales) {
    z <- sc[[s]]
    if (is.null(z)) { bad("scale ", s, " is absent"); next }
    pre <- paste0("scale ", s, ": ")
    need_sc <- c("status", "scope", "log_Z", "log_m0", "log_Z_rel_m0", "pip", "hpm", "hpm_F", "hpm_size", "hpm_eta", "hpm_eta_kind", "second_F", "margin",
                 "certificate_bound", "certificate_bound_kind", "global_certified", "certified_over_scored_models", "mpm", "size_logmass", "size_logjoint", "top", "numerics")
    miss <- setdiff(need_sc, names(z))
    if (length(miss)) { bad(pre, "missing fields: ", paste(miss, collapse = ",")); next }
    if (!identical(z$status, "exact")) bad(pre, "status is not exact")
    if (!identical(z$scope, "full")) bad(pre, "scope is not full")
    if (!identical(z$certificate_bound_kind, KIND) || !identical(z$hpm_eta_kind, KIND)) bad(pre, "heuristic bound labels missing or altered")
    for (nm in c("log_Z", "log_m0", "log_Z_rel_m0", "hpm_F", "hpm_eta", "second_F", "margin", "certificate_bound")) if (!num1(z[[nm]])) bad(pre, nm, " is not finite")
    if (num1(z$margin) && z$margin < 0) bad(pre, "margin is negative")
    if (!is.logical(z$global_certified) || length(z$global_certified) != 1L || is.na(z$global_certified)) bad(pre, "global_certified is not TRUE/FALSE")
    if (!is.logical(z$certified_over_scored_models) || length(z$certified_over_scored_models) != 1L || is.na(z$certified_over_scored_models)) bad(pre, "certified_over_scored_models is not TRUE/FALSE")
    pip <- z$pip
    if (!is.numeric(pip) || length(pip) != pret || anyNA(pip) || any(pip < 0 | pip > 1)) bad(pre, "pip must be numeric, length p_retained = ", pret, ", within [0, 1]")
    else if (!identical(names(pip), as.character(ret))) bad(pre, "names(pip) do not match the retained-column map")
    if (!is.numeric(z$hpm) || (length(z$hpm) && (anyNA(z$hpm) || is.unsorted(z$hpm, strictly = TRUE) || !all(z$hpm %in% ret)))) bad(pre, "hpm is not a sorted subset of the retained columns")
    else if (!(num1(z$hpm_size) && z$hpm_size == length(z$hpm))) bad(pre, "hpm_size != length(hpm)")
    else if (!is.na(Kx) && length(z$hpm) > Kx) bad(pre, "hpm larger than K")
    if (!is.numeric(z$mpm) || (length(z$mpm) && (anyNA(z$mpm) || !all(z$mpm %in% ret)))) bad(pre, "mpm is not a subset of the retained columns")
    else if (is.numeric(pip) && length(pip) == pret && !anyNA(pip) && !identical(as.integer(ret[pip > 0.5]), as.integer(z$mpm))) bad(pre, "mpm != {pip > 0.5}")
    sm <- z$size_logmass; sj <- z$size_logjoint
    if (!is.na(Kx) && (!is.numeric(sm) || length(sm) != Kx + 1L || anyNA(sm) || any(sm > 1e-12))) bad(pre, "size_logmass must be numeric of length K+1 without NA or log-probabilities > 0")
    else if (!(abs(lse(sm)) <= 1e-10)) bad(pre, "size_logmass is not normalised: |log-sum-exp| = ", format(abs(lse(sm)), digits = 3), " > 1e-10")
    if (!is.na(Kx) && (!is.numeric(sj) || length(sj) != Kx + 1L || anyNA(sj))) bad(pre, "size_logjoint must be numeric of length K+1")
    else if (num1(z$log_Z) && !(abs(lse(sj) - z$log_Z) <= 1e-8)) bad(pre, "size_logjoint log-sum-exp differs from log_Z")
    tp <- z$top
    if (!is.data.frame(tp) || !all(c("rank", "F", "size", "model", "mask") %in% names(tp))) bad(pre, "top is not a data.frame(rank, F, size, model, mask)")
    else {
      if (!is.na(nexp) && nrow(tp) != min(1000, nexp)) bad(pre, "top has ", nrow(tp), " rows, expected ", min(1000, nexp))
      if (nrow(tp) && (anyNA(tp$F) || is.unsorted(rev(tp$F)))) bad(pre, "top F missing or not in decreasing order")
      if (nrow(tp) && num1(z$hpm_F) && !identical(tp$F[1], z$hpm_F)) bad(pre, "hpm_F differs from the best entry of top")
    }
    ## ---- cross-field consistency (a record whose fields contradict each other is not a posterior) ----
    if (is.numeric(sm) && is.numeric(sj) && length(sm) == length(sj) && length(sm) > 0L && num1(z$log_Z)) {
      fin <- is.finite(sm) & is.finite(sj)
      if (any(is.infinite(sm) != is.infinite(sj)) || any(sm[is.infinite(sm)] > 0) || any(sj[is.infinite(sj)] > 0)) bad(pre, "size_logjoint and size_logmass have different -Inf patterns")
      else if (any(fin) && max(abs(sj[fin] - (sm[fin] + z$log_Z))) > 1e-9) bad(pre, "size_logjoint[k] != size_logmass[k] + log_Z (max abs error ", format(max(abs(sj[fin] - (sm[fin] + z$log_Z))), digits = 3), ")")
    }
    if (num1(z$log_Z) && num1(z$log_m0) && num1(z$log_Z_rel_m0) && abs(z$log_Z_rel_m0 - (z$log_Z - z$log_m0)) > 1e-9) bad(pre, "log_Z_rel_m0 != log_Z - log_m0")
    if (num1(z$log_Z) && num1(z$hpm_F) && z$log_Z < z$hpm_F - 1e-9) bad(pre, "log_Z (", format(z$log_Z, digits = 8), ") is below the mass of one contained model, hpm_F (", format(z$hpm_F, digits = 8), ")")
    if (is.data.frame(tp) && all(c("F", "size", "model", "mask") %in% names(tp)) && nrow(tp) >= 1L) {
      idx <- lapply(strsplit(as.character(tp$model), ";", fixed = TRUE), as.integer)
      okmodel <- !anyNA(unlist(idx)) && all(vapply(idx, function(i) !length(i) || (all(i %in% ret) && !is.unsorted(i, strictly = TRUE)), TRUE))
      if (!okmodel) bad(pre, "top$model entries are not sorted subsets of the retained columns")
      else {
        if (!identical(as.integer(lengths(idx)), as.integer(tp$size))) bad(pre, "top$size != number of variables in top$model")
        if (!isTRUE(all(tp$mask == vapply(idx, function(i) sum(2^(i - 1)), 0)))) bad(pre, "top$mask does not match top$model")
        if (anyDuplicated(tp$mask)) bad(pre, "top contains duplicated models")
        if (nrow(tp) > 1L) {
          dF <- diff(tp$F); tie <- which(dF == 0)
          bad_order <- any(dF > 0, na.rm = TRUE)
          for (i in tie) {
            if (tp$size[i + 1L] < tp$size[i]) { bad_order <- TRUE; break }
            if (tp$size[i + 1L] == tp$size[i]) {
              a <- idx[[i]]; b <- idx[[i + 1L]]; k <- which(a != b)[1L]
              if (is.na(k) || a[k] > b[k]) { bad_order <- TRUE; break }
            }
          }
          if (bad_order) bad(pre, "top is not in the section I.6 order (F decreasing, then smaller size, then lexicographic)")
        }
        hp <- if (is.numeric(z$hpm)) as.integer(z$hpm) else NA_integer_
        if (!identical(hp, idx[[1L]])) bad(pre, "hpm differs from the support of the best entry of top")
        if (!isTRUE(z$hpm_size == tp$size[1L])) bad(pre, "hpm_size differs from top$size[1]")
        if (!isTRUE(sum(2^(hp - 1)) == tp$mask[1L])) bad(pre, "hpm differs from top$mask[1]")
        if (nrow(tp) >= 2L && !isTRUE(z$second_F == tp$F[2L])) bad(pre, "second_F != top$F[2]")
        if (num1(z$log_Z) && !anyNA(tp$F) && lse(tp$F) > z$log_Z + 1e-9) bad(pre, "log_Z is below the total mass of the listed top models")
        ## PIP feasibility given the listed models: share_j <= PIP_j <= share_j + (unlisted mass), and the size/PIP moment identity
        if (num1(z$log_Z) && !anyNA(tp$F) && is.numeric(pip) && length(pip) == pret && !anyNA(pip)) {
          wl <- exp(tp$F - z$log_Z)                                        # posterior mass of each listed model
          M <- vapply(idx, function(i) as.numeric(ret %in% i), numeric(pret)) # pret x nrow membership
          share <- as.vector(matrix(M, nrow = pret) %*% wl); unl <- 1 - sum(wl)
          if (any(pip < share - 1e-9)) bad(pre, "PIP_j below the posterior share of the listed top models containing j (j = ", paste(ret[which(pip < share - 1e-9)], collapse = ","), ")")
          if (any(pip > share + max(unl, 0) + 1e-9)) bad(pre, "PIP_j above the share of the listed models plus the unlisted mass 1 - sum(listed) = ", format(unl, digits = 4), " (j = ", paste(ret[which(pip > share + max(unl, 0) + 1e-9)], collapse = ","), ")")
        }
        if (is.numeric(pip) && length(pip) == pret && !anyNA(pip) && is.numeric(sm) && length(sm) == length(sj) && !anyNA(sm) &&
            abs(sum(pip) - sum((seq_along(sm) - 1) * exp(sm))) > 1e-8 * pret) bad(pre, "sum(PIP) = ", format(sum(pip), digits = 8), " != sum_k k exp(size_logmass[k]) = ", format(sum((seq_along(sm) - 1) * exp(sm)), digits = 8))
      }
    }
    nu <- z$numerics
    need_nu <- c("n_rescale", "n_fallback_v3", "max_abs_dF_recheck", "recheck_count", "q_recomputed", "recheck_mismatch_F", "recheck_mismatch_eta")
    if (!is.list(nu) || !all(need_nu %in% names(nu))) bad(pre, "numerics lacks: ", paste(setdiff(need_nu, names(nu)), collapse = ","))
    else if (!identical(as.numeric(nu$recheck_mismatch_F), 0) || !identical(as.numeric(nu$recheck_mismatch_eta), 0)) bad(pre, "the score re-check reported mismatches")
  }
  list(ok = length(reasons) == 0L, reasons = reasons)
}
