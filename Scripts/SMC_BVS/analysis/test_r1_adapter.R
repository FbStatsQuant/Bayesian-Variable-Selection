# D-OWNED R-1 SCHEMA MOCK tests. NOT execution/certification of A's updated adapter.
a <- commandArgs(TRUE); source(a[1]); source(a[2]); source(a[3]); out <- a[4]
dir.create(out,recursive=TRUE,showWarnings=FALSE)
policy <- mock_r1_policy()
cases <- list()
add <- function(name,native="completed",flags=list(),extra=list(),warnings=character(),messages=character(),
                status=if(native %in% c("exact","completed")) "ok" else "failed",diag=FALSE,codes=character()) {
  cases[[length(cases)+1]] <<- list(name=name,native=native,flags=flags,extra=extra,warnings=warnings,messages=messages,
    status=status,diag=diag,codes=codes)
}
add("completed clean")
add("exact clean","exact",codes="exact_branch")
add("captured warning",warnings="literal R warning: detail",status="warning")
add("captured message",messages="literal R message: detail",status="warning")
add("warning and message",warnings=c("one","two"),messages="three",status="warning")
for(code in c("E1","E2","E3")) add(paste("final",code),flags=setNames(list(TRUE,FALSE),c(code,"checks_passed_final")),
  diag=TRUE,codes=paste0("final_check_",code))
for(code in c("low_empirical_ESS","grid_unconverged","local_limit")) add(code,flags=setNames(list(TRUE),code),diag=TRUE,codes=code)
for(code in c("escalated","cut_group","near_tie_truncated","global_certified"))
  add(paste("informational",code),flags=setNames(list(TRUE),code),codes=code)
add("informational forced steps",flags=list(forced_pilot_steps=2L),codes="forced_pilot_steps")
add("informational local uncertified",extra=list(local_certified=FALSE),codes="local_certified_false")
add("flag alone never warning",flags=list(local_limit=TRUE),diag=TRUE,codes="local_limit")
add("flag plus captured condition",flags=list(local_limit=TRUE),messages="captured",status="warning",diag=TRUE,codes="local_limit")
for(native in c("schedule_limit","numerical_failure","resource_limit","y_constant","no_predictors","invalid_input"))
  add(paste("failed",native),native,flags=list(grid_unconverged=TRUE),diag=TRUE,codes="grid_unconverged")
add("failed early adapter_error","adapter_error")
checks <- list()
for(i in seq_along(cases)) {
  ca <- cases[[i]]; flags <- modifyList(list(E1=FALSE,E2=FALSE,E3=FALSE,checks_passed_final=TRUE,
    low_empirical_ESS=FALSE,grid_unconverged=FALSE,local_limit=FALSE),ca$flags)
  fit <- mock_native_fit(20L,1L,ca$native,flags)
  if(length(ca$extra)) for(nm in names(ca$extra)) fit[[nm]] <- ca$extra[[nm]]
  if(ca$native %in% c("y_constant","no_predictors")) fit$hpm <- integer()
  outputs <- if(is.null(fit)) list(hpm=NULL,mpm=NULL,pip=setNames(rep(NA_real_,20),as.character(1:20)),estimates_available=FALSE) else smcbvs_outputs(fit,20L)
  design <- list(fold_seed=NA,fold_sha256=NA,adapter_mapping_status=policy$mapping_status,
    adapter_policy_id=policy$id,adapter_policy_sha256=digest::digest(serialize(policy,NULL,version=3),algo="sha256",serialize=FALSE))
  rows <- mock_r1_rule_rows(fit,outputs,design,policy,warnings=ca$warnings,messages=ca$messages,native_status=ca$native)
  record <- list(rows=rows,fit=fit,pip=outputs$pip,pip_primary_original=outputs$pip,hpm=outputs$hpm,mpm=outputs$mpm,
    estimates_available=outputs$estimates_available,error=if(is.null(fit)) "documented early adapter setup failure" else NULL,
    warnings=ca$warnings,messages=ca$messages,native_status=ca$native)
  before <- serialize(record,NULL)
  # Read CSV exactly as the scoring interface does: NA differs from blank support.
  path <- file.path(out,paste0("branch_",i,".csv")); write.csv(rows,path,row.names=FALSE,na="NA")
  parsed <- read.csv(path,colClasses="character",na.strings="NA",check.names=FALSE)
  native_validate(parsed,record,20L);r1_validate(parsed,record)
  ok <- all(rows$status==ca$status) && all(rows$diag_flag==ca$diag) && all(is.na(rows$converged)) &&
    all(is.na(rows$fold_seed)) && all(is.na(rows$fold_sha256)) && identical(before,serialize(record,NULL))
  for(j in seq_len(nrow(rows))) {
    codes <- strsplit(rows$diag_codes[j],";",fixed=TRUE)[[1]]
    ok <- ok && setequal(codes[nzchar(codes)],ca$codes)
  }
  if(ca$status=="failed") {
    ok <- ok && all(is.na(rows$support)) && all(is.na(rows$k)) && identical(rows$support_audit[1],smcbvs_support_key(outputs$hpm))
  } else {ok <- ok && all(rows$support=="1") && all(rows$k==1L)}
  checks[[i]] <- data.frame(check=ca$name,passed=ok,status=ca$status,diag_flag=ca$diag)
  if(!ok) stop("R-1 branch failed: ",ca$name)
}
write.csv(do.call(rbind,checks),file.path(out,"r1_checks.csv"),row.names=FALSE)
writeLines(c(capture.output(sessionInfo()),paste("policy",policy$id)),file.path(out,"R_environment.txt"))
cat("D R-1 SCHEMA MOCK branches PASS:",length(checks),"; final A integration pending\n")
