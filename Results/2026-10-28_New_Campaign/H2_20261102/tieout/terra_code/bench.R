root <- 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian'
out <- file.path(root,'02_Experiments/I_2026-10-28_New_Campaign/analysis/H2_20261102/tieout')
base <- 'C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019'
verify <- file.path(root,'02_Experiments/F_2026-10-19_benchmark_study_n200/Benchmark_Study_20261019/verify/recount/c050/inputs')
cl <- read.csv(file.path(out,'CLAIMS.csv'),na.strings=c('','NA')); result <- list()
runs <- c('c100_F1'='20261019T2308Z_bench20261019_prod_F1_Lasso','c100_F2'='20261019T2232Z_bench20261019_prod_F2_ElasticNet','c050_F1'='20261021T1615Z_bench20261019_prodc050_F1_Lasso','c050_F2'='20261021T1540Z_bench20261019_prodc050_F2_ElasticNet')
for (i in 16:21) {
 c<-cl[i,]; dir<-if(c$scale=='c100') file.path(base,'derived') else file.path(verify,'derived')
 path<-file.path(dir,runs[[paste(c$scale,c$method,sep='_')]],'derived_rules/derived_rule_rows.csv')
 rows<-read.csv(path,stringsAsFactors=FALSE); rows<-rows[rows$method_id==c$method & rows$rule_id=='ebic1_K37',]
 count<-0; missing<-0; failed<-0
 for (s in if(c$scenario=='pooled') 1:6 else as.integer(c$scenario)) for(r in 1:100) {
  pd<-sprintf('p%04d',as.integer(c$p)); ds<-sprintf('%s_S%d_r%03d',pd,s,r); id<-paste(ds,c$scale,sep='_')
  t<-sort(as.integer(readRDS(file.path(verify,'truth_scoring',pd,paste0(ds,'.rds')))$active)); z<-rows[rows$case_id==id,,drop=FALSE]
  if(nrow(z)>1) stop('duplicate row'); if(nrow(z)==0) {missing<-missing+1; next}; if(!z$status %in% c('ok','warning')) {failed<-failed+1; next}
  support<-if(is.na(z$support)||z$support=='') integer() else as.integer(strsplit(z$support,';',fixed=TRUE)[[1]])
  count<-count+identical(sort(support),t)
 }
 result[[as.character(i)]]<-c(count=count,missing=missing,failed=failed)
}
saveRDS(result,file.path(out,'terra_code/bench.rds'))
