C <- 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign'
S <- file.path(C,'code/bench_v2/review/sol_scripts_r2')
code <- file.path(C,'code/bench_v2/F3_AdaptiveLasso')
sys.source(file.path(C,'bench_audit/jobs/BENCH_F3_PROD/runner/validate.R'),.GlobalEnv)
ctx <- load_frozen_validator(code)
prefix <- file.path(C,'code/bench_v2/tests/runner_output/results/v2_local_e2e/p0500/dev_p0500_S1_r001_c100/F3')
input <- 'C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/dev/inputs/p0500/dev_p0500_S1_r001.rds'
manifest <- 'C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/dev/manifests/dev_inputs_manifest.csv'
x <- readRDS(paste0(prefix,'.rds')); inp <- readRDS(input); man <- read.csv(manifest)
mr <- man[man$dataset_id==inp$dataset_id,,drop=FALSE]
source_hash <- x$prov$source_sha256
expected <- list(run_id='v2_local_e2e',dataset_id=inp$dataset_id,case_id=paste0(inp$dataset_id,'_c100'),p=500L,scenario=1L,replicate=1L,scale_key='c100',method_id='F3')
cat('START',format(Sys.time(),tz='UTC'),'\n')
stopifnot(validate_prefix(prefix,source_hash,input,manifest,code,'v2_local_e2e',inp$dataset_id,500L,1L,1L,'c100'))
cat('POSITIVE_REAL PASS\n'); print(names(x$case)); print(names(x$prov)); print(names(x$fit$rules)); print(x$case)
saved_check <- function(a,rows,label) {
  folder <- file.path(S,'corruptions',label); dir.create(folder,recursive=TRUE,showWarnings=FALSE)
  pre <- file.path(folder,'F3')
  saveRDS(a,paste0(pre,'.rds'),version=3); write.csv(rows,paste0(pre,'.csv'),row.names=FALSE,na='NA')
  writeLines(c(paste(ctx$engine$file_sha256(paste0(pre,'.rds')),'F3.rds',sep='  '),paste(ctx$engine$file_sha256(paste0(pre,'.csv')),'F3.csv',sep='  ')),paste0(pre,'.sha256'))
  writeLines('review synthetic corruption',paste0(pre,'.done'))
  tryCatch({validate_prefix(pre,source_hash,input,manifest,code,'v2_local_e2e',inp$dataset_id,500L,1L,1L,'c100');'ACCEPTED'},error=function(e)conditionMessage(e))
}
faults <- c('missing_OLS','bad_index','bad_k','missing_pilot','retired_code','wrong_role','wrong_input_hash','wrong_numeric_beta','wrong_csv_criterion','bad_failed_vector')
reasons <- c('coefficient','coefficient','metadata','pilot','vocabulary','roles','manifest_inputs_sha256','coefficient','CSV_RDS_crit_value','penalized support')
for(i in seq_along(faults)) {
  fault <- faults[i]; a <- x; csv <- a$rows
  if(fault=='missing_OLS') a$coefficients[[3]]$beta_ols <- NULL
  if(fault=='bad_index') a$coefficients[[1]]$index <- -999L
  if(fault=='bad_k') a$rows$k[1] <- csv$k[1] <- 999L
  if(fault=='missing_pilot') a$fit$diagnostics$pilot <- NULL
  if(fault=='retired_code') a$rows$diag_codes[1] <- csv$diag_codes[1] <- 'kappa_edge'
  if(fault=='wrong_role') a$rows$role[1] <- csv$role[1] <- 'S0'
  if(fault=='wrong_input_hash') a$rows$inputs_sha256 <- csv$inputs_sha256 <- strrep('0',64)
  if(fault=='wrong_numeric_beta') a$coefficients[[1]]$beta_pen <- 2*a$coefficients[[1]]$beta_pen
  if(fault=='wrong_csv_criterion') csv$crit_value[3] <- 123456
  if(fault=='bad_failed_vector') { a$rows$status[1] <- csv$status[1] <- a$coefficients[[1]]$status <- 'failed';a$rows$support[1] <- csv$support[1] <- a$coefficients[[1]]$support <- NA_character_;a$coefficients[[1]]$beta_pen <- rep(Inf,a$rows$p[1]) }
  why <- tryCatch({validate_object(a,csv,source_hash,inp,mr,expected,ctx);'ACCEPTED'},error=function(e)conditionMessage(e))
  full <- saved_check(a,csv,fault)
  cat('OWN_TEN',fault,'OBJECT',why,'SAVED',full,'\n')
  # Some complete-file checks reject sooner for the same invalid metadata/support.
  stopifnot(grepl(reasons[i],why,fixed=TRUE),full!='ACCEPTED')
}
cat('OWN_TEN PASS 10/10 object and saved rehashed controls\n')
for(fault in c('data_seed','fold_seed','method_seed','scale','p','scenario','replicate','x_sha256','y_sha256','fold_sha256','OLS_both','beta_both','CV_OLS','OLS_RSS','EBIC_criterion','pilot_keep','pilot_weights')) {
  a <- x; csv <- a$rows
  if(fault %in% c('data_seed','fold_seed','method_seed','scale','p','scenario','replicate','x_sha256','y_sha256','fold_sha256')) {
    value <- if(grepl('sha256',fault))strrep('0',64) else a$rows[[fault]][1]+1
    a$rows[[fault]] <- csv[[fault]] <- rep(value,6L)
    if(fault %in% names(a$case)) a$case[[fault]] <- value
    if(fault %in% names(a$prov)) a$prov[[fault]] <- value
    if(fault %in% names(a$fit$rules)) a$fit$rules[[fault]] <- rep(value,6L)
  }
  if(fault=='OLS_both') {a$coefficients[[3]]$beta_ols[1] <- a$coefficients[[3]]$beta_ols[1]+1;a$fit$coefficients<-a$coefficients}
  if(fault=='beta_both') {a$coefficients[[1]]$beta_pen <- 2*a$coefficients[[1]]$beta_pen;a$fit$coefficients<-a$coefficients}
  if(fault=='CV_OLS') {a$coefficients[[1]]$beta_ols <- numeric(500);a$fit$coefficients<-a$coefficients}
  if(fault=='OLS_RSS') a$rows$rss[3] <- csv$rss[3] <- a$fit$rules$rss[3] <- 100
  if(fault=='EBIC_criterion') a$rows$crit_value[3] <- csv$crit_value[3] <- a$fit$rules$crit_value[3] <- 123456
  if(fault=='pilot_keep') a$fit$diagnostics$keep <- integer()
  if(fault=='pilot_weights') a$fit$diagnostics$v[1] <- 2*a$fit$diagnostics$v[1]
  full <- saved_check(a,csv,paste0('extra_',fault));cat('EXTRA',fault,full,'\n')
}
cat('END',format(Sys.time(),tz='UTC'),'\n');print(sessionInfo())
