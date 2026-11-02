C <- 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign'
S <- file.path(C,'code/bench_v2/review/sol_scripts_r2'); out <- file.path(S,'regenerated_branches')
dir.create(out,recursive=TRUE,showWarnings=FALSE)
tests <- file.path(C,'bench_audit/jobs/BENCH_F3_PROD/tests')
cat('START',format(Sys.time(),tz='UTC'),'\n')
for(script in c('make_branch_fixtures.R','make_timed_failure.R')) {
  scope <- new.env(parent=globalenv());scope$commandArgs <- function(...) c(C,out)
  eval(parse(file.path(tests,script)),scope)
}
# Run shipped branch controls against a review-local copy only.
copy <- file.path(S,'branch_fixture_copy');dir.create(copy,showWarnings=FALSE)
file.copy(list.files(file.path(tests,'fixtures'),full.names=TRUE),copy,recursive=TRUE)
scope <- new.env(parent=globalenv());scope$commandArgs <- function(...) c(C,copy,file.path(C,'bench_audit/jobs/BENCH_F3_PROD/runner/validate.R'))
eval(parse(file.path(tests,'test_branch_fixtures.R')),scope)
sys.source(file.path(C,'bench_audit/jobs/BENCH_F3_PROD/runner/validate.R'),.GlobalEnv)
code <- file.path(C,'code/bench_v2/F3_AdaptiveLasso');ctx<-load_frozen_validator(code)
for(i in 1:3) {
  label<-c('null','singleton','failed')[i]; id<-sprintf('fixture_p0005_S%d_r001',i)
  run<-if(i==3)'branch_failure' else 'branch_fixture'; rel<-file.path('results',run,'p0005',paste0(id,'_c100'),'F3')
  saved<-readRDS(paste0(file.path(tests,'fixtures',rel),'.rds'));regen<-readRDS(paste0(file.path(out,rel),'.rds'))
  sf<-saved$fit;rf<-regen$fit;sf$runtime_s<-rf$runtime_s<-NULL
  stopifnot(identical(sf,rf),identical(saved$coefficients,regen$coefficients),identical(saved$case,regen$case))
  cat('FROZEN_RUNNER_REGEN_IDENTITY',label,'PASS\n')
  inp<-readRDS(file.path(out,'inputs','p0005',paste0(id,'.rds')));y<-unname(inp$Y[,1]);X<-inp$X
  rows<-saved$rows
  if(i==1) {
    d<-saved$fit$diagnostics
    stopifnot(all(rows$status=='ok'),all(rows$support==''),all(rows$k==0),all(saved$fit$beta==0),all(rows$rss==sum(y^2)),all(is.na(rows$lambda)),all(is.na(rows$index)),nrow(d$path)==1L,is.na(d$path$lambda),d$path$key=='',d$path$k==0,nrow(d$candidates)==1L,d$candidates$key=='',d$candidates$k==0,all(d$heldout==0))
    cat('INDEPENDENT_NULL_FULL_CONTRACT PASS\n')
  }
  if(i==2) {
    d<-saved$fit$diagnostics;j<-d$keep;ll<-d$path$lambda;n<-nrow(X)
    soft<-function(z,pen)sign(z)*pmax(abs(z)-pen,0)
    B<-soft(sum(X[,j]*y)/n,ll*d$v)/(sum(X[,j]^2)/n)
    for(k in 1:6) stopifnot(isTRUE(all.equal(unname(saved$coefficients[[k]]$beta_pen[j]),B[rows$index[k]],tolerance=1e-12)))
    mse<-sapply(1:10,function(k){tr<-inp$foldid!=k;te<-!tr;bb<-soft(sum(X[tr,j]*y[tr])/sum(tr),ll*d$v)/(sum(X[tr,j]^2)/sum(tr));colMeans((y[te]-outer(X[te,j],bb))^2)})
    avg<-rowMeans(mse);se<-sqrt(rowSums((mse-avg)^2)/10/9)
    stopifnot(isTRUE(all.equal(avg,d$path$cvm,tolerance=1e-12)),isTRUE(all.equal(se,d$path$cvsd,tolerance=1e-12)),rows$index[1]==which.min(avg),rows$index[2]==min(which(avg<=min(avg)+se[which.min(avg)])))
    cat('INDEPENDENT_SINGLETON_FULL_FOLD_AND_BOTH_CV PASS\n')
  }
  if(i==3) {
    stopifnot(all(rows$status=='failed'),all(is.na(rows$diag_flag)),all(is.na(rows$support)),all(is.na(rows$k)),all(is.na(saved$fit$beta)),all(vapply(saved$coefficients,function(z)all(is.na(z$beta_pen))&&all(is.na(z$beta_ols)),TRUE)))
    cat('INDEPENDENT_WHOLE_FAILURE_NA PASS runtime',saved$fit$runtime_s,'\n')
  }
}
# Isolate branch contracts that mere evidence presence cannot certify.
id<-'fixture_p0005_S1_r001'; input<-file.path(copy,'inputs/p0005',paste0(id,'.rds'));manifest<-file.path(copy,'inputs_manifest.csv')
pre<-file.path(copy,'results/branch_fixture/p0005',paste0(id,'_c100'),'F3');x<-readRDS(paste0(pre,'.rds'))
for(fault in c('null_index_lambda','null_path','null_candidates','null_CV_RSS')) {
  a<-x;rows<-a$rows
  if(fault=='null_index_lambda') {a$rows$index<-rows$index<-a$fit$rules$index<-rep(1L,6);a$rows$lambda<-rows$lambda<-a$fit$rules$lambda<-rep(1,6);for(k in 1:6){a$coefficients[[k]]$index<-1L;a$coefficients[[k]]$lambda<-1};a$fit$coefficients<-a$coefficients}
  if(fault=='null_path') a$fit$diagnostics$path<-data.frame(bogus=1:7)
  if(fault=='null_candidates') a$fit$diagnostics$candidates<-data.frame(bogus=1:7)
  if(fault=='null_CV_RSS') a$rows$rss[1]<-rows$rss[1]<-a$fit$rules$rss[1]<-123456
  folder<-file.path(S,'corruptions',fault);dir.create(folder,recursive=TRUE,showWarnings=FALSE);p<-file.path(folder,'F3')
  saveRDS(a,paste0(p,'.rds'),version=3);write.csv(rows,paste0(p,'.csv'),row.names=FALSE,na='NA')
  writeLines(c(paste(ctx$engine$file_sha256(paste0(p,'.rds')),'F3.rds',sep='  '),paste(ctx$engine$file_sha256(paste0(p,'.csv')),'F3.csv',sep='  ')),paste0(p,'.sha256'));writeLines('review corruption',paste0(p,'.done'))
  why<-tryCatch({validate_prefix(p,x$prov$source_sha256,input,manifest,code,'branch_fixture',id,5L,1L,1L,'c100');'ACCEPTED'},error=function(e)conditionMessage(e))
  cat('NULL_CONTRACT_CORRUPTION',fault,why,'\n')
}
cat('END',format(Sys.time(),tz='UTC'),'\n');print(sessionInfo())
