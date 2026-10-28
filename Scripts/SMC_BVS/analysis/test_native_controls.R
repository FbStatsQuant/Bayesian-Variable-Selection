# Branch-aware controls and F4 PIP/null/unavailable audit regressions. No fit or truth.
a <- commandArgs(TRUE);source(a[1]);source(a[2]);source(a[3]);out <- a[4]
dir.create(out,recursive=TRUE,showWarnings=FALSE)
policy <- mock_r1_policy(); checks <- list()
for(name in c("dropped_columns","reordered_native_pip","exact_no_SMC","partial_returned_mpm","partial_null_mpm",
              "failed_null_hpm","failed_unavailable_hpm","invalid_input_early","adapter_error_early")) {
  status <- if(name=="exact_no_SMC") "exact" else if(startsWith(name,"partial") || startsWith(name,"failed")) "schedule_limit"
    else if(name=="invalid_input_early") "invalid_input" else if(name=="adapter_error_early") "adapter_error" else "completed"
  fit <- mock_native_fit(20L,1L,status,dropped=if(name=="dropped_columns") 2L else integer())
  if(name=="reordered_native_pip") fit$pip_primary <- rev(fit$pip_primary)
  if(startsWith(name,"partial")) {
    fit$pip_primary <- setNames(numeric(20),as.character(1:20))
    fit$mpm <- if(name=="partial_null_mpm") integer() else 1:3
    fit$pip_primary[fit$mpm] <- .9
  }
  if(name=="failed_null_hpm") fit$hpm <- integer()
  if(name %in% c("failed_unavailable_hpm","invalid_input_early")) fit$hpm <- NULL
  outputs <- if(is.null(fit)) list(hpm=NULL,mpm=NULL,pip=setNames(rep(NA_real_,20),as.character(1:20)),estimates_available=FALSE) else smcbvs_outputs(fit,20)
  design <- list(p=20L,fold_seed=NA,fold_sha256=NA,adapter_mapping_status="adopted",adapter_policy_id=policy$id,
    adapter_policy_sha256=digest::digest(serialize(policy,NULL,version=3),algo="sha256",serialize=FALSE))
  rows <- mock_r1_rule_rows(fit,outputs,design,policy,native_status=status)
  record <- list(rows=rows,fit=fit,pip=outputs$pip,pip_primary_original=outputs$pip,hpm=outputs$hpm,mpm=outputs$mpm,
    estimates_available=outputs$estimates_available,native_status=status,warnings=character(),messages=character(),
    error=if(is.null(fit)) "documented adapter failure before core returned" else NULL)
  path <- file.path(out,paste0(name,".csv"));write.csv(rows,path,row.names=FALSE,na="NA")
  parsed <- read.csv(path,colClasses="character",na.strings="NA",check.names=FALSE)
  native_validate(parsed,record,20);r1_validate(parsed,record)
  checks[[length(checks)+1]] <- data.frame(check=name,passed=TRUE)
  if(startsWith(name,"partial")) {
    bad <- parsed;bad$support_audit[bad$rule_id=="pip05"] <- NA_character_
    error <- tryCatch({native_validate(bad,record,20);"ACCEPTED"},error=function(e) conditionMessage(e))
    ok <- grepl("native failed support_audit mismatch",error,fixed=TRUE)
    checks[[length(checks)+1]] <- data.frame(check=paste0(name,"_audit_removed"),passed=ok)
    if(!ok) stop("F4 PIP audit regression failed: ",error)
  }
}
bad <- record;bad$fit <- list(status="adapter_error",timings=list(total=0))
error <- tryCatch({native_validate(parsed,bad,20);"ACCEPTED"},error=function(e) conditionMessage(e))
ok <- grepl("retained-fit adapter_error",error,fixed=TRUE)
checks[[length(checks)+1]] <- data.frame(check="adapter_error_retained_fit_rejected",passed=ok)
if(!ok) stop("retained-fit adapter failure exception too broad")
bad <- record;bad$error <- NULL
error <- tryCatch({native_validate(parsed,bad,20);"ACCEPTED"},error=function(e) conditionMessage(e))
ok <- grepl("undocumented early adapter failure",error,fixed=TRUE)
checks[[length(checks)+1]] <- data.frame(check="adapter_error_undocumented_rejected",passed=ok)
if(!ok) stop("undocumented adapter failure accepted")
write.csv(do.call(rbind,checks),file.path(out,"native_control_checks.csv"),row.names=FALSE)
cat("Native controls PASS; no truth or fit\n")
