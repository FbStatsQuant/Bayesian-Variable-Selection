# D-OWNED SCHEMA MOCK, NOT A'S UPDATED ADAPTER. Binding R-1 defines this fixture.
# Old immutable A helpers supply field layout/native diagnostics and PIP extraction only.
mock_native_fit <- function(p,support,status="completed",flags=list(),dropped=integer()) {
  if(status=="adapter_error") return(NULL)
  flags <- modifyList(list(E1=FALSE,E2=FALSE,E3=FALSE,checks_passed_final=TRUE,low_empirical_ESS=FALSE,
    grid_unconverged=FALSE,local_limit=FALSE),flags)
  keep <- setdiff(seq_len(p),dropped); q <- setNames(numeric(length(keep)),as.character(keep));q[as.character(support)] <- .9
  if("16" %in% names(q) && !16 %in% support) q["16"] <- .5
  complete <- status %in% c("exact","completed")
  fit <- list(status=status,hpm=support,mpm=if(complete) support else NULL,
    estimates_available=complete,pip_primary=if(complete) q else NULL,
    preprocessing=list(p_raw=as.integer(p),p=length(keep),kept=as.integer(keep),dropped=as.integer(dropped)),
    p=length(keep),flags=flags,timings=list(total=1))
  if(complete) {
    fit$branch_run <- if(status=="exact") "exact" else "smc"
    fit$log_Z <- 1;fit$log_Z_lower95 <- 0;fit$bound_label <- "heuristic"
    if(status=="exact") fit$exact <- list(status="exact",hpm=support,mpm=support,pip=q,log_Z=1)
    else {
      fit$stage_table <- data.frame(phase="SYNTHETIC",island=1L,ess=10,cum_log_Z=1)
      fit$log_Z_r <- rep(1,4);fit$streams <- rep(list(list(state="SYNTHETIC")),4)
    }
  }
  fit
}
mock_r1_policy <- function() {
  list(id="D_SCHEMA_R1_MOCK_NOT_A_ADAPTER",adopted=TRUE,mapping_status="adopted",mock_only=TRUE,
    authority="Binding RULINGS_LEAD.md R-1; D schema fixture ONLY; final A integration pending",
    roles=c(hpm="primary",pip05="S0"))
}
mock_r1_rule_rows <- function(fit,outputs,design,policy,warnings=character(),messages=character(),native_status=fit$status) {
  rows <- smcbvs_rule_rows(fit,outputs,design,smcbvs_unresolved_policy(),warnings,messages,native_status=native_status)
  yes <- function(nm) isTRUE(fit[[nm]]) || (is.list(fit$flags) && isTRUE(fit$flags[[nm]]))
  f <- fit$flags
  diag <- identical(f$checks_passed_final,FALSE) || any(vapply(c("E1","E2","E3","low_empirical_ESS","grid_unconverged","local_limit"),yes,TRUE))
  codes <- c(paste0("final_check_",c("E1","E2","E3"))[vapply(c("E1","E2","E3"),yes,TRUE)],
    c("low_empirical_ESS","grid_unconverged","local_limit")[vapply(c("low_empirical_ESS","grid_unconverged","local_limit"),yes,TRUE)])
  for(nm in c("escalated","cut_group","near_tie_truncated")) if(yes(nm)) codes <- c(codes,nm)
  if(is.numeric(f$forced_pilot_steps) && any(f$forced_pilot_steps>0,na.rm=TRUE)) codes <- c(codes,"forced_pilot_steps")
  if(native_status=="exact") codes <- c(codes,"exact_branch")
  if(identical(fit$local_certified,FALSE)) codes <- c(codes,"local_certified_false")
  if(yes("global_certified")) codes <- c(codes,"global_certified")
  failed <- !native_status %in% c("exact","completed")
  rows$role <- unname(policy$roles[rows$rule_id])
  rows$status <- if(failed) "failed" else if(length(warnings)+length(messages)) "warning" else "ok"
  rows$converged <- NA; rows$diag_flag <- diag; rows$diag_codes <- paste(codes,collapse=";")
  rows$fold_seed <- NA; rows$fold_sha256 <- NA
  for(i in seq_len(nrow(rows))) {
    support <- outputs[[if(rows$rule_id[i]=="hpm") "hpm" else "mpm"]]
    if(failed && rows$rule_id[i]=="pip05" && !is.null(fit$mpm)) support <- sort(as.integer(fit$mpm))
    rows$support[i] <- if(failed) NA_character_ else smcbvs_support_key(support)
    rows$k[i] <- if(failed) NA_integer_ else length(support)
    rows$support_audit[i] <- if(failed) smcbvs_support_key(support) else NA_character_
  }
  rows
}
mock_write_record <- function(prefix,record) {
  # gzip is deliberately a schema-level mock encoding, avoiding xz encoder memory pressure.
  saveRDS(record,paste0(prefix,".rds"),compress="gzip",version=3)
  utils::write.csv(record$rows,paste0(prefix,".csv"),row.names=FALSE,na="NA")
  paths <- paste0(prefix,c(".rds",".csv"))
  writeLines(paste(vapply(paths,smcbvs_file_hash,""),basename(paths),sep="  "),paste0(prefix,".sha256"))
  writeLines("D SCHEMA MOCK ONLY; no updated A adapter executed",paste0(prefix,".done"))
}
