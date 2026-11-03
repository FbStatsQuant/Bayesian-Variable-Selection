root <- 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian'
sc <- file.path(root,'02_Experiments/I_2026-10-28_New_Campaign/code/scoring')
Sys.setenv(SCORING_DIR=sc); source(file.path(sc,'R/load_all.R')); sc_load_core()
out <- file.path(root,'02_Experiments/I_2026-10-28_New_Campaign/analysis/H2_20261102/tieout/terra_code')
new <- 'C:/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign/results/20261030T0934Z_prodH'
inp <- 'C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/inputs'
truth <- file.path(root,'02_Experiments/F_2026-10-19_benchmark_study_n200/Benchmark_Study_20261019/verify/recount/c050/inputs/truth_scoring')
arg <- commandArgs(TRUE)[1]; claims <- read.csv(file.path(dirname(out),'CLAIMS.csv'),na.strings=c('','NA'))
if (arg %in% c('42','43')) { i<-as.integer(arg); pp<-claims$p[i]; scale<-claims$scale[i]; ids<-unlist(lapply(1:6,function(s) sprintf('p%04d_S%d_r%03d_%s',pp,s,1:100,scale))) } else { i<-as.integer(arg); ids<-claims$case[i] }
result <- list(); for (id in ids) {
 ds<-sub('_c[0-9]+$','',id); pd<-substr(ds,1,5); scale<-sub('^.*_','',id)
 rec<-readRDS(file.path(new,pd,id,'SMCBVS.rds')); t<-sort(as.integer(readRDS(file.path(truth,pd,paste0(ds,'.rds')))$active))
 if (i %in% c(42,43) && (!identical(rec$native_status,'completed') || identical(sort(as.integer(rec$hpm)),t))) next
 dat<-readRDS(file.path(inp,pd,paste0(ds,'.rds'))); scorer<-make_scorer(dat$X,as.numeric(dat$Y[,scale])); f<-scorer$F; base<-f(t)
 if (i %in% c(42,43)) { result[[id]]<-c(truth=base,hpm=f(rec$hpm)); next }
 if (!all(t %in% scorer$kept)) stop('truth dropped')
 null<-setdiff(scorer$kept,t); best <- -Inf; moves <- 0L
 test <- function(z) { v<-f(z); if (is.na(v)) stop('invalid score'); best <<- max(best,v); moves <<- moves+1L }
 if (length(t)<scorer$K) for (j in null) test(c(t,j))
 for (j in t) test(setdiff(t,j))
 for (j in t) for (k in null) test(c(setdiff(t,j),k))
 result[[id]]<-c(truth=base,best=best,moves=moves,strict=as.numeric(base>best))
}
saveRDS(result,file.path(out,paste0('scores_',i,'.rds')))
