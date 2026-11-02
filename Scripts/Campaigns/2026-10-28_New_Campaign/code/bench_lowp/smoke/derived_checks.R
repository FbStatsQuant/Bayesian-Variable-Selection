.libPaths(c('C:/Users/felip/AppData/Local/Temp/lowp_Rlib',.libPaths()))
base <- 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/lowp_port/smoke_output'
self <- sub('^--file=','',grep('^--file=',commandArgs(FALSE),value=TRUE)[1]); code <- dirname(dirname(normalizePath(self,winslash='/')))
args <- commandArgs(TRUE); if(length(args)) base <- args[1]
source(file.path(code,'R/config_lowp.R'))
stopifnot(identical(LOWP_PRODUCTION$F3$F3,list(pilot='lasso_cv_min',gamma=1,K_size_bound=37L)))
ids <- c('F1','F2','F3','F4','F5','A1','A2','A3')
cases <- c('p0020_S1_r001','p0030_S4_r050','p0030_S6_r100')
schema <- c('tp','fp','fn','exact','error_type',sprintf('sel_a%02d',1:14),sprintf('pip_a%02d',1:14),'max_pip_null')
checks <- list(); check <- function(name,x) { checks[[length(checks)+1L]] <<- data.frame(test=name,pass=isTRUE(x)); if(!isTRUE(x)) cat('FAILED',name,'\n') }
for(case in cases) for(scale in c('c100','c050')) for(id in ids) {
 f <- file.path(base,'results/smoke',substr(case,1,5),paste0(case,'_',scale),paste0(id,'.rds'))
 if(!file.exists(f)) {check(paste(case,scale,id,'exists'),FALSE); next}
 r <- readRDS(f)$rows
 check(paste(case,scale,id,'schema'),all(schema %in% names(r)) && all(vapply(r[schema],function(z) all(is.na(z)),TRUE)) && sum(r$role=='primary')==1 && all(r$test_library))
 if(id %in% paste0('F',1:5)) for(a in intersect(c('ebic1','ebic05','bic'),r$rule_id)) {
  one <- r[r$rule_id==a,,drop=FALSE]; two <- r[r$rule_id==paste0(a,'_K37'),,drop=FALSE]
  fields <- setdiff(names(r),c('rule_id','role','rule_label'))
  check(paste(case,scale,id,a,'alias'),nrow(two)==1 && all(vapply(fields,function(x) identical(one[[x]],two[[x]]),TRUE)) && one$role=='secondary')
 }
}
for(id in c('F4','F5')) {
 f <- file.path(base,'results/smoke/p0020/p0020_S1_r001_c100',paste0(id,'.rds')); rec <- readRDS(f)
 cand <- rec$fit$diagnostics$candidates; path <- rec$fit$diagnostics$path
 if(id=='F4') { eligible <- cand$valid & cand$key %in% c('',path$key[path$lambda>=.05*max(path$lambda)]); crit <- cand$ebic1; rid <- 'ebic1_lam005' }
 else { n<-200; p<-20; eligible <- cand$valid & cand$k <= min(p,floor(n/(log(p)*log(log(n))))); crit <- n*log(cand$rss/n)+cand$k*log(p)*log(log(n)); rid <- 'sic_smax' }
 crit[!eligible] <- Inf; j<-order(crit,cand$k,cand$key,method='radix')[1]; row<-rec$rows[rec$rows$rule_id==rid,]
 check(paste(id,'independent saved path'),identical(row$support,cand$key[j]) && identical(row$crit_value,crit[j]))
}
write.csv(do.call(rbind,checks),file.path(base,'derived_checks.csv'),row.names=FALSE)
cat('checks',sum(vapply(checks,function(x)x$pass,TRUE)),'of',length(checks),'\n')
quit(status=if(all(vapply(checks,function(x)x$pass,TRUE))) 0 else 1)
