.libPaths(c('C:/Users/felip/AppData/Local/Temp/lowp_Rlib', .libPaths()))
root <- 'C:/Users/felip/AppData/Local/Temp/lowp_work/bench_smoke'
ids <- c('F1','F2','F3','F4','F5','A1','A2','A3')
cases <- c('p0020_S1_r001','p0030_S4_r002','p0030_S6_r003')
results <- list()
for(id in ids) for(case in cases) for(scale in c('c100','c050')) {
 base <- file.path(root,'results','smoke',substr(case,1,5),paste0(case,'_',scale),id)
 x <- readRDS(paste0(base,'.rds')); rr <- x$rules
 stopifnot(identical(readLines(paste0(base,'.sha256')),digest::digest(file=paste0(base,'.rds'),algo='sha256')),sum(rr$role=='primary')==1L,all(c('rule_id','role','status','support','support_audit','k','converged','diag_flag','diag_codes','runtime_s','adaptation_ids') %in% names(rr)))
 for(j in which(rr$status != 'failed')) { k <- if(is.na(rr$support[j]) || !nzchar(rr$support[j])) integer() else as.integer(strsplit(rr$support[j],';',fixed=TRUE)[[1]]); stopifnot(identical(k,sort(unique(k))),length(k)==rr$k[j]) }
 results[[length(results)+1]] <- data.frame(id,case,scale,status=if(any(rr$status=='failed')) 'failed' else if(any(rr$status=='warning')) 'warning' else 'ok',runtime=x$runtime_s,flags=any(rr$diag_flag %in% TRUE), warnings=paste(c(x$runner_warnings,x$warnings),collapse=' | '),error=if(is.null(x$error)) '' else paste(x$error,collapse=' | '))
}
r <- do.call(rbind,results); write.csv(r,file.path(root,'validation.csv'),row.names=FALSE); print(aggregate(runtime~id,r,function(x)c(median=median(x),max=max(x)))); print(with(r,table(id,status))); print(with(r,table(id,flags))); print(r[nzchar(r$warnings)|nzchar(r$error),c('id','case','scale','warnings','error')]); cat('All hashes, frames, and supports verified.\n')