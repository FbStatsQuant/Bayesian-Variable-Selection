# Native derivation integrity (review F1-F4). No scoring, fitting or field repair.
native_support <- function(x,p,field) {
  if(is.null(x)) return(NULL)
  if(!is.numeric(x) || anyNA(x) || any(!is.finite(x)) || any(x!=as.integer(x)) ||
     any(x<1 | x>p) || anyDuplicated(x)) stop("invalid native support: ",field)
  sort(as.integer(x))
}
native_key <- function(x) if(is.null(x)) NA_character_ else paste(x,collapse=";")
native_status_validate <- function(rows,record) {
  native <- unique(as.character(rows$v3_status))
  allowed <- c("exact","completed","schedule_limit","numerical_failure","resource_limit","y_constant","no_predictors","invalid_input","adapter_error")
  if(length(native)!=1L || is.na(native) || !native %in% allowed) stop("invalid R-1 native status")
  if(!is.character(record$native_status) || !identical(record$native_status,native)) stop("RDS native status differs")
  if(native=="adapter_error" && !is.null(record$fit)) stop("retained-fit adapter_error is not a documented early adapter failure")
  # Sole exception: a documented adapter error before any core fit returned.
  # Retained-fit/output-validation errors are not silently reclassified or accepted.
  if(native=="adapter_error" && is.null(record$fit)) {
    if(!is.character(record$error) || length(record$error)!=1L || is.na(record$error) || !nzchar(record$error) ||
       !identical(record$estimates_available,FALSE)) stop("undocumented early adapter failure")
  } else if(!is.list(record$fit) || !is.character(record$fit$status) ||
            !identical(record$fit$status,native)) stop("native fit/status/export mismatch")
  native
}
native_json_validate <- function(rows,fit) {
  represented <- list(flags=fit$flags,cut_group=fit$cut_group,cut_group_count=fit$cut_group_count,
    cut_group_components=fit$cut_group_components,local_limit=fit$local_limit,local_certified=fit$local_certified,
    global_certified=fit$global_certified,near_tie_truncated=fit$near_tie_truncated)
  normalize <- function(x) jsonlite::fromJSON(as.character(jsonlite::toJSON(x,auto_unbox=TRUE,null="null",na="null")),simplifyVector=FALSE)
  expected <- normalize(represented)
  for(json in rows$v3_flags_json) {
    actual <- jsonlite::fromJSON(json,simplifyVector=FALSE)
    if(!setequal(names(actual),names(expected))) stop("native flags JSON differs: represented fields")
    for(nm in names(expected)) if(!identical(actual[[nm]],expected[[nm]])) stop("native flags JSON differs: ",nm)
  }
}
native_validate <- function(rows,record,p,require_bound_label=TRUE) {
  native <- native_status_validate(rows,record); fit <- record$fit
  complete <- native %in% c("exact","completed")
  scalar <- function(x) is.numeric(x) && length(x)==1L && is.finite(x)
  if(!identical(record$estimates_available,complete)) stop("native/export estimates availability mismatch")
  if(anyNA(rows$v3_estimates_available) || any(as.character(rows$v3_estimates_available)!=as.character(complete))) stop("native/export availability flag mismatch")
  if(!all(c("pip","pip_primary_original","hpm","mpm") %in% names(record))) stop("native interface payload missing")
  native_json_validate(rows,fit)
  if(!is.null(fit)) {
    if(!is.list(fit$timings) || !scalar(fit$timings$total) || fit$timings$total<0) stop("native timings payload missing/invalid")
    if(complete && !identical(fit$estimates_available,TRUE)) stop("native completed estimates unavailable")
  }
  hpm <- native_support(fit$hpm,p,"HPM")
  if(!identical(native_support(record$hpm,p,"retained HPM"),hpm)) stop("native HPM/retained HPM mismatch")
  pip <- NULL; mpm <- NULL
  # A returned MPM, even on a failed fit, must be derived from retained native PIPs.
  derive <- complete || !is.null(fit$mpm)
  if(derive) {
    pre <- fit$preprocessing
    if(!is.list(pre) || !all(c("kept","dropped","p_raw","p") %in% names(pre))) stop("native preprocessing map missing")
    keep <- native_support(pre$kept,p,"kept"); drop <- native_support(pre$dropped,p,"dropped")
    if(is.null(keep) || is.null(drop) || !identical(sort(c(keep,drop)),seq_len(p)) ||
       !scalar(pre$p_raw) || !scalar(pre$p) || pre$p_raw!=p || pre$p!=length(keep) || !scalar(fit$p) || fit$p!=length(keep)) stop("native preprocessing map invalid")
    q <- fit$pip_primary
    if(!is.numeric(q) || is.null(names(q)) || anyDuplicated(names(q)) || length(q)!=length(keep) ||
       !setequal(names(q),as.character(keep)) || any(!is.finite(q)) || any(q<0 | q>1)) stop("native primary PIP missing/invalid")
    pip <- setNames(numeric(p),as.character(seq_len(p)));pip[names(q)] <- q
    mpm <- which(pip>.5);mpm <- unname(as.integer(mpm))
    if(!identical(native_support(fit$mpm,p,"MPM"),mpm)) stop("native MPM/primary PIP mismatch")
    if(complete && (is.null(hpm) || any(hpm %in% drop))) stop("native HPM/preprocessing mismatch")
  }
  exported <- record$pip
  if(!is.numeric(exported) || length(exported)!=p || !identical(names(exported),as.character(seq_len(p)))) stop("native full original-index PIP interface invalid")
  if(!is.numeric(record$pip_primary_original) || length(record$pip_primary_original)!=p ||
     !identical(names(record$pip_primary_original),as.character(seq_len(p)))) stop("native original primary PIP copy invalid")
  if(complete) {
    if(!identical(as.numeric(exported),as.numeric(pip)) ||
       !identical(as.numeric(record$pip_primary_original),as.numeric(pip))) stop("native primary PIP/export mismatch")
    if(!identical(native_support(record$mpm,p,"retained MPM"),mpm)) stop("native MPM/retained MPM mismatch")
  } else {
    if(!all(is.na(exported)) || !is.numeric(record$pip_primary_original) || length(record$pip_primary_original)!=p ||
       !all(is.na(record$pip_primary_original))) stop("unavailable native PIP must remain NA")
    if(!is.null(record$mpm) && !identical(native_support(record$mpm,p,"audit MPM"),mpm)) stop("native audit MPM mismatch")
  }
  if(complete) {
    branch <- fit$branch_run
    if(!is.character(branch) || length(branch)!=1L || !branch %in% c("smc","exact") ||
       (native=="exact")!=(branch=="exact")) stop("native branch/status payload invalid")
    if(!scalar(fit$log_Z) || !scalar(fit$log_Z_lower95)) stop("native pooled evidence/bound payload missing")
    # D-F1 (AUDIT_SUMMARY decision 2): the heuristic label is required only when a global
    # certificate bound is reported (exact branch). Its absence is accepted when global_certified is FALSE.
    if(require_bound_label && isTRUE(fit$global_certified)) {
      labels <- c(fit$bound_label,record$native_annotations$log_Z_lower95$label,
                  fit$exact$hpm_error_bound_kind,fit$exact$R9$kind)
      if(!any(labels %in% c("heuristic","heuristic (not a validated interval bound)")))
        stop("native heuristic bound label missing")
    }
    if(branch=="smc") {
      required_flags <- c("E1","E2","E3","checks_passed_final","low_empirical_ESS","grid_unconverged","local_limit")
      if(!is.list(fit$flags) || !all(required_flags %in% names(fit$flags)) ||
         !all(vapply(fit$flags[required_flags],function(x) is.logical(x) && length(x)==1L && !is.na(x),TRUE)))
        stop("native final diagnostic payload missing/invalid")
      if(!is.data.frame(fit$stage_table) || !nrow(fit$stage_table) ||
         !all(c("phase","island","ess","cum_log_Z") %in% names(fit$stage_table)) ||
         !is.numeric(fit$stage_table$ess) || !any(is.finite(fit$stage_table$ess)) ||
         any(is.infinite(fit$stage_table$ess) | is.nan(fit$stage_table$ess))) stop("native SMC stage payload missing/invalid")
      if(!is.numeric(fit$log_Z_r) || length(fit$log_Z_r)!=4L || any(!is.finite(fit$log_Z_r)) ||
         !is.list(fit$streams) || length(fit$streams)!=4L) stop("native island evidence/streams payload missing")
    } else {
      if(!is.null(fit$stage_table) || !is.null(fit$log_Z_r) || !is.null(fit$streams)) stop("exact branch must not fabricate SMC payload")
      if(!is.list(fit$exact) || !identical(fit$exact$status,"exact") ||
         !identical(as.numeric(fit$exact$pip),as.numeric(fit$pip_primary)) ||
         !identical(native_support(fit$exact$hpm,p,"exact HPM"),hpm) || !identical(fit$exact$log_Z,fit$log_Z)) stop("native exact payload missing/inconsistent")
    }
  } else {
    if(!is.null(fit$stage_table) && !is.data.frame(fit$stage_table)) stop("native partial stage payload invalid")
    if(!is.null(fit$streams) && !is.list(fit$streams)) stop("native partial streams payload invalid")
    if((!is.null(fit$calibration) || !is.null(fit$timings$calibration)) && !is.data.frame(fit$stage_table)) stop("native calibrated failure lost stage payload")
    if(native %in% c("invalid_input","y_constant","no_predictors","adapter_error")) {
      for(nm in c("stage_table","log_Z","log_Z_r","log_Z_lower95","pip_primary","mpm","streams","exact"))
        if(!is.null(fit[[nm]])) stop("early native failure must not fabricate payload: ",nm)
    }
  }
  for(i in seq_len(nrow(rows))) {
    expected <- if(rows$rule_id[i]=="hpm") hpm else mpm
    if(complete) {
      if(!identical(as.character(rows$support[i]),native_key(expected))) stop("native ",rows$rule_id[i],"/exported support mismatch")
    } else if(!identical(as.character(rows$support_audit[i]),native_key(expected))) stop("native failed support_audit mismatch: ",rows$rule_id[i])
  }
  invisible(list(native_status=native,hpm=hpm,mpm=mpm,pip=if(complete) pip else NULL))
}
