.libPaths(c('C:/Users/felip/AppData/Local/Temp/lowp_Rlib',.libPaths()))
root <- 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/lowp_port/smoke_output'
self <- sub('^--file=','',grep('^--file=',commandArgs(FALSE),value=TRUE)[1]); code <- dirname(dirname(normalizePath(self,winslash='/')))
source(file.path(code,'R/config_lowp.R'))
ids <- c(paste0('F',1:5),paste0('A',1:3)); cases <- c('p0020_S1_r001','p0030_S4_r050','p0030_S6_r100'); count <- 0L
for(id in ids) for(case in cases) for(scale in c('c100','c050')) {
 prefix <- file.path(root,'results','smoke',substr(case,1,5),paste0(case,'_',scale),id)
 paths <- paste0(prefix,c('.rds','.csv','.sha256','.done')); stopifnot(all(file.exists(paths)))
 stopifnot(identical(readLines(paths[3],warn=FALSE),paste(vapply(paths[1:2],function(f) digest::digest(file=f,algo='sha256'),''),basename(paths[1:2]),sep='  ')))
 rec <- readRDS(paths[1]); rr <- rec$rows; stopifnot(identical(rec$schema_version,2L),sum(rr$role=='primary')==1L,!anyDuplicated(rr$rule_id))
 reg <- LOWP_PRODUCTION[[id]]$METHODS; reg <- reg[reg$method_id==id,,drop=FALSE]
 stopifnot(all(reg$rule_ids[[1]] %in% rr$rule_id))
 for(j in which(rr$status != 'failed')) { s <- if(nzchar(rr$support[j])) as.integer(strsplit(rr$support[j],';',fixed=TRUE)[[1]]) else integer(); stopifnot(identical(s,sort(unique(s))),length(s)==rr$k[j]) }
 if(id %in% paste0('F',1:5)) stopifnot(identical(names(rec$coefficients),rr$rule_id),identical(rec$coefficients,rec$fit$coefficients))
 count <- count+1L
}
cat('validated',count,'records\n')
