# Binding deployment RULINGS_LEAD.md R-1 validation. No fit or diagnostic is changed.
local({
  paths <- Filter(Negate(is.null),lapply(rev(sys.frames()),function(fr) fr$ofile))
  source(file.path(dirname(normalizePath(paths[[1]],winslash="/")),"native_contract.R"),local=FALSE)
})
r1_expected <- function(fit, native, warnings=character(), messages=character()) {
  get <- function(nm) {
    if (!is.null(fit[[nm]])) fit[[nm]] else if (is.list(fit$flags)) fit$flags[[nm]] else NULL
  }
  true <- function(nm) isTRUE(get(nm))
  diagnostic <- c(paste0("final_check_",c("E1","E2","E3"))[vapply(c("E1","E2","E3"),true,TRUE)],
    c("low_empirical_ESS","grid_unconverged","local_limit")[vapply(c("low_empirical_ESS","grid_unconverged","local_limit"),true,TRUE)])
  flag <- identical(get("checks_passed_final"),FALSE) || length(diagnostic)>0L
  info <- c("escalated","cut_group","near_tie_truncated")[vapply(c("escalated","cut_group","near_tie_truncated"),true,TRUE)]
  forced <- get("forced_pilot_steps")
  if (is.numeric(forced) && any(forced>0,na.rm=TRUE)) info <- c(info,"forced_pilot_steps")
  if (identical(native,"exact")) info <- c(info,"exact_branch")
  if (identical(get("local_certified"),FALSE)) info <- c(info,"local_certified_false")
  if (true("global_certified")) info <- c(info,"global_certified")
  list(status=if (!native %in% c("exact","completed")) "failed" else
      if(length(warnings)+length(messages)>0L) "warning" else "ok",
    diag_flag=flag, codes=c(diagnostic,info))
}
r1_validate <- function(rows,record) {
  if(anyNA(rows$adapter_mapping_status) || any(rows$adapter_mapping_status!="adopted")) stop("unresolved or unadopted adapter policy")
  native <- native_status_validate(rows,record)
  expected <- r1_expected(record$fit,native,record$warnings,record$messages)
  native_json_validate(rows,record$fit)
  roles <- c(hpm="primary",pip05="S0")[rows$rule_id]
  if (anyNA(roles) || !identical(unname(roles),rows$role)) stop("R-1 role mismatch")
  if (any(!is.na(rows$converged))) stop("R-1 converged must be NA")
  if (any(!is.na(rows$fold_seed)) || any(!is.na(rows$fold_sha256))) stop("R-1 fold fields must be NA")
  if (anyNA(rows$status) || any(rows$status != expected$status)) stop("R-1 captured condition/status mismatch")
  counts <- suppressWarnings(as.numeric(rows$n_warnings))
  if (anyNA(counts) || any(counts != length(record$warnings)+length(record$messages))) stop("R-1 captured condition count mismatch")
  if (anyNA(rows$diag_flag) || any(rows$diag_flag != as.character(expected$diag_flag))) stop("R-1 diagnostic flag mismatch")
  for (i in seq_len(nrow(rows))) {
    actual <- strsplit(rows$diag_codes[i],";",fixed=TRUE)[[1]]
    if (!setequal(actual[nzchar(actual)],expected$codes) || anyDuplicated(actual)) stop("R-1 diagnostic/informational codes mismatch")
    for (nm in c("warnings","messages")) {
      vals <- record[[nm]]
      text <- if(length(vals)) paste(vals,collapse=" | ") else NA_character_
      if (!identical(rows[[nm]][i],text)) stop("R-1 captured conditions not preserved verbatim")
    }
  }
  invisible(expected)
}
