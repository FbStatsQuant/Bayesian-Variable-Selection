C <- 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign'
S <- file.path(C,'code/bench_v2/review/sol_scripts_r2')
code <- file.path(C,'code/bench_v2/F3_AdaptiveLasso')
sys.source(file.path(C,'bench_audit/jobs/BENCH_F3_PROD/runner/validate.R'),.GlobalEnv);ctx<-load_frozen_validator(code)
prefix<-file.path(C,'code/bench_v2/tests/runner_output/results/v2_local_e2e/p0500/dev_p0500_S1_r001_c100/F3')
input<-'C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/dev/inputs/p0500/dev_p0500_S1_r001.rds'
manifest<-'C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/dev/manifests/dev_inputs_manifest.csv'
x<-readRDS(paste0(prefix,'.rds'));d<-x$fit$diagnostics
print(x$rows[,c('rule_id','support','index','lambda','crit_value')],row.names=FALSE)
cat('ACTUAL_CV_CHOICES',which.min(d$path$cvm),min(which(d$path$cvm<=min(d$path$cvm)+d$path$cvsd[which.min(d$path$cvm)])),'\n')
a<-x;fields<-setdiff(names(a$fit$rules),c('rule_id','role'))
for(nm in fields) a$fit$rules[[nm]][1]<-a$rows[[nm]][1]<-x$rows[[nm]][2]
a$coefficients[[1]]<-x$coefficients[[2]];a$coefficients[[1]]$rule_id<-'cv_min';a$fit$coefficients<-a$coefficients;a$fit$beta<-a$coefficients[[1]]$beta_pen
stopifnot(!identical(a$rows$support[1],x$rows$support[1]),a$rows$index[1]!=which.min(d$path$cvm))
folder<-file.path(S,'corruptions','cv_min_replaced_by_cv_1se');dir.create(folder,recursive=TRUE,showWarnings=FALSE);p<-file.path(folder,'F3')
saveRDS(a,paste0(p,'.rds'),version=3);write.csv(a$rows,paste0(p,'.csv'),row.names=FALSE,na='NA')
writeLines(c(paste(ctx$engine$file_sha256(paste0(p,'.rds')),'F3.rds',sep='  '),paste(ctx$engine$file_sha256(paste0(p,'.csv')),'F3.csv',sep='  ')),paste0(p,'.sha256'));writeLines('review corruption',paste0(p,'.done'))
why<-tryCatch({validate_prefix(p,x$prov$source_sha256,input,manifest,code,'v2_local_e2e','dev_p0500_S1_r001',500L,1L,1L,'c100');'ACCEPTED'},error=function(e)conditionMessage(e))
cat('PRIMARY_SUPPORT_CHANGED',why,'old_k',x$rows$k[1],'new_k',a$rows$k[1],'old_index',x$rows$index[1],'new_index',a$rows$index[1],'\n')
cat('END',format(Sys.time(),tz='UTC'),'\n')
