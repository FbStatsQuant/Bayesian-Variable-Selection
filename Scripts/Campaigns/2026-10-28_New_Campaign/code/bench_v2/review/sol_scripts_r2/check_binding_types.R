C<-'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign';S<-file.path(C,'code/bench_v2/review/sol_scripts_r2')
code<-file.path(C,'code/bench_v2/F3_AdaptiveLasso');sys.source(file.path(C,'bench_audit/jobs/BENCH_F3_PROD/runner/validate.R'),.GlobalEnv);ctx<-load_frozen_validator(code)
prefix<-file.path(C,'code/bench_v2/tests/runner_output/results/v2_local_e2e/p0500/dev_p0500_S1_r001_c100/F3');x<-readRDS(paste0(prefix,'.rds'))
input<-'C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/dev/inputs/p0500/dev_p0500_S1_r001.rds';manifest<-'C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/dev/manifests/dev_inputs_manifest.csv'
for(nm in c('inputs_sha256','x_sha256','y_sha256','fold_sha256')) {
  a<-x;a$case[[nm]]<-strrep('f',64);a$rows[[nm]]<-rep(strrep('f',64),6)
  folder<-file.path(S,'corruptions',paste0('binding_',nm));dir.create(folder,recursive=TRUE,showWarnings=FALSE);p<-file.path(folder,'F3')
  saveRDS(a,paste0(p,'.rds'),version=3);write.csv(a$rows,paste0(p,'.csv'),row.names=FALSE,na='NA')
  writeLines(c(paste(ctx$engine$file_sha256(paste0(p,'.rds')),'F3.rds',sep='  '),paste(ctx$engine$file_sha256(paste0(p,'.csv')),'F3.csv',sep='  ')),paste0(p,'.sha256'));writeLines('review corruption',paste0(p,'.done'))
  why<-tryCatch({validate_prefix(p,x$prov$source_sha256,input,manifest,code,'v2_local_e2e','dev_p0500_S1_r001',500L,1L,1L,'c100');'ACCEPTED'},error=function(e)conditionMessage(e))
  cat('SELF_CONSISTENT_HASH_BINDING',nm,why,'\n');stopifnot(identical(why,paste0('manifest_',nm)))
}
f<-file.path(C,'bench_audit/jobs/BENCH_F3_PROD/tests/fixtures/results/branch_failure/p0005/fixture_p0005_S3_r001_c100/F3');z<-readRDS(paste0(f,'.rds'))
rows<-read.csv(paste0(f,'.csv'),stringsAsFactors=FALSE,colClasses=c(support='character',support_audit='character',diag_codes='character',warnings='character',messages='character',error='character'))
bare<-new.env(parent=globalenv());sys.source(file.path(code,'tests/validate_outputs.R'),bare)
before<-bare$validate_payload(z,rows,ctx$cfg$study_settings(),ctx$engine);after<-ctx$checker$validate_payload(z,rows,ctx$cfg$study_settings(),ctx$engine)
cat('ALL_NA_K_TYPE',typeof(rows$k),'BEFORE',paste(before,collapse=';'),'AFTER',length(after),'problems\n')
stopifnot(typeof(rows$k)=='logical',length(before)==6L,all(grepl('coefficient metadata mismatch',before,fixed=TRUE)),length(after)==0L,identical(as.integer(rows$k),z$rows$k))
cat('END',format(Sys.time(),tz='UTC'),'PASS\n')
