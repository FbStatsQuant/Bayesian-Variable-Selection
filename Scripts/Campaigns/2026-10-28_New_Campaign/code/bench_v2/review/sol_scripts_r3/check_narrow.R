options(warn=1)
cat('START UTC',format(Sys.time(),tz='UTC'), '\n')
C <- 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign'
S <- file.path(C,'code/bench_v2/review/sol_scripts_r3')
old <- file.path(C,'code/bench_v2/review/sol_scripts_r2')
T <- file.path(C,'bench_audit/jobs/BENCH_F3_PROD/tests')
code <- file.path(C,'code/bench_v2/F3_AdaptiveLasso')
sys.source(file.path(C,'bench_audit/jobs/BENCH_F3_PROD/runner/validate.R'),.GlobalEnv)
ctx <- load_frozen_validator(code)
real <- file.path(C,'code/bench_v2/tests/runner_output/results/v2_local_e2e/p0500/dev_p0500_S1_r001_c100/F3')
study <- 'C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/dev'
real_input <- file.path(study,'inputs/p0500/dev_p0500_S1_r001.rds')
real_manifest <- file.path(study,'manifests/dev_inputs_manifest.csv')
x <- readRDS(paste0(real,'.rds')); source_hash <- x$prov$source_sha256
params <- function(kind) {
 if(kind=='real') return(list(source_hash,real_input,real_manifest,code,'v2_local_e2e','dev_p0500_S1_r001',500L,1L,1L,'c100'))
 sc <- switch(kind,null=1L,singleton=2L,failure=3L)
 id <- sprintf('fixture_p0005_S%d_r001',sc)
 list(source_hash,file.path(T,'fixtures/inputs/p0005',paste0(id,'.rds')),file.path(T,'fixtures/inputs_manifest.csv'),code,
      if(kind=='failure') 'branch_failure' else 'branch_fixture',id,5L,sc,1L,'c100')
}
fixture <- function(kind) {
 p <- params(kind)
 file.path(T,'fixtures/results',p[[5]],'p0005',paste0(p[[6]],'_c100'),'F3')
}
count <- 0L
check <- function(prefix,kind,label,expected='ACCEPTED') {
 why <- tryCatch({do.call(validate_prefix,c(list(prefix),params(kind))); 'ACCEPTED'},error=function(e)conditionMessage(e))
 cat('CHECK',label,'=>',why,'\n')
 stopifnot(identical(why,expected)); count <<- count+1L
}
for(kind in c('real','null','singleton','failure')) check(if(kind=='real') real else fixture(kind),kind,paste0('positive_',kind))
controls <- c(extra_data_seed='seed_binding_data_seed',extra_fold_seed='seed_binding_fold_seed',
 extra_method_seed='seed_binding_method_seed',null_index_lambda='null_sentinels',null_path='null_path',
 null_candidates='null_candidates',null_CV_RSS='null_rss',cv_min_replaced_by_cv_1se='CV_choice_cv_min',
 extra_EBIC_criterion='EBIC_score_ebic1')
for(label in names(controls)) check(file.path(old,'corruptions',label,'F3'),if(startsWith(label,'null_')) 'null' else 'real',label,controls[[label]])
save_control <- function(a,label,kind,expected) {
 dir <- file.path(S,'corruptions',label); dir.create(dir,recursive=TRUE,showWarnings=FALSE)
 p <- file.path(dir,'F3')
 saveRDS(a,paste0(p,'.rds'),version=3)
 write.csv(a$rows,paste0(p,'.csv'),row.names=FALSE,na='NA')
 writeLines(c(paste(ctx$engine$file_sha256(paste0(p,'.rds')),'F3.rds',sep='  '),paste(ctx$engine$file_sha256(paste0(p,'.csv')),'F3.csv',sep='  ')),paste0(p,'.sha256'))
 writeLines('independent narrow review control',paste0(p,'.done'))
 check(p,kind,label,expected)
}
fx <- readRDS(paste0(fixture('failure'),'.rds'))
for(seed in c('data_seed','fold_seed','method_seed')) {
 a <- fx; a$rows[[seed]] <- a$rows[[seed]]+1L; a$case[[seed]] <- a$case[[seed]]+1L
 save_control(a,paste0('failure_',seed),'failure',paste0('seed_binding_',seed))
}
# One new independent substitution: take an actual KKT-passing CV support >37
# and attribute its coefficients, OLS RSS and true full-p EBIC score to ebic1_K37.
inp <- readRDS(real_input); X <- inp$X; y <- inp$Y[,'c100']; cfg <- ctx$cfg$study_settings()
stopifnot(ncol(X)==500L,cfg$COMMON$kmax_ebic==100L,floor(nrow(X)/log(nrow(X)))==37L)
a <- x; i <- match('ebic1_K37',a$rows$rule_id); j <- match('cv_1se',a$rows$rule_id)
candidate <- a$fit$diagnostics$candidates
cc <- candidate[match(a$rows$support[j],candidate$key),,drop=FALSE]
stopifnot(nrow(cc)==1L,cc$valid,cc$k>37L,cc$k<=100L,a$rows$support[i]!=a$rows$support[j])
cat('NEW_SUBSTITUTION source cv_1se k=',cc$k,' index=',a$rows$index[j],'; original ebic1_K37 k=',a$rows$k[i],' index=',a$rows$index[i],'\n',sep='')
for(nm in c('status','support','support_audit','k','index','lambda','error')) a$rows[[nm]][i] <- a$fit$rules[[nm]][i] <- x$rows[[nm]][j]
for(nm in c('rss','ebic1_value','crit_value')) {
 value <- if(nm=='rss') cc$rss else cc$ebic1
 a$rows[[nm]][i] <- a$fit$rules[[nm]][i] <- value
}
co <- x$coefficients[[j]]; co$rule_id <- 'ebic1_K37'; co$beta_ols <- numeric(ncol(X))
ix <- which(co$beta_pen!=0); co$beta_ols[ix] <- lm.fit(X[,ix,drop=FALSE],y,tol=cfg$COMMON$ols_tol)$coefficients
a$coefficients[[i]] <- co; a$fit$coefficients <- a$coefficients
save_control(a,'K37_from_actual_k51_cv1se','real','EBIC_pick_ebic1_K37')
# Targeted later-occurrence control required by R2-3's original acceptance check.
a <- x; i <- match('ebic1',a$rows$rule_id); path <- a$fit$diagnostics$path
later <- which(path$key==a$rows$support[i] & path$kkt_full<=cfg$GLMNET$kkt_rel_tol & seq_len(nrow(path))>a$rows$index[i])
stopifnot(length(later)>0L); ix <- later[1]
cat('LATER_OCCURRENCE original=',a$rows$index[i],' substituted=',ix,'\n',sep='')
a$rows$index[i] <- a$fit$rules$index[i] <- a$coefficients[[i]]$index <- ix
a$rows$lambda[i] <- a$fit$rules$lambda[i] <- a$coefficients[[i]]$lambda <- path$lambda[ix]
a$fit$coefficients <- a$coefficients
save_control(a,'later_ebic1_occurrence','real','EBIC_occurrence_ebic1')
cat('REAL_RULES\n'); print(x$rows[,c('rule_id','k','index','rss','crit_value')],row.names=FALSE)
cat('PASS',count,'targeted saved-record checks\n')
print(sessionInfo())
cat('END UTC',format(Sys.time(),tz='UTC'),'\n')
