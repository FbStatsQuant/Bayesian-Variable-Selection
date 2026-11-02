args <- base::commandArgs(TRUE)
target <- args[1]; marker <- args[2]; rest <- args[-c(1,2)]
commandArgs <- function(trailingOnly=FALSE) if (trailingOnly) rest else c(base::commandArgs(FALSE)[1],paste0('--file=',target),'--args',rest)
quit <- function(save='default',status=0L,...) stop(structure(list(message='script quit',call=NULL,status=as.integer(status)),class=c('script_quit','error','condition')))
started <- format(Sys.time(),'%Y-%m-%dT%H:%M:%SZ',tz='UTC'); cat('started',started,'target',target,'\n')
status <- tryCatch({sys.source(target,envir=globalenv()); 0L},script_quit=function(e)e$status,error=function(e){cat('ERROR:',conditionMessage(e),'\n'); 1L})
cat('finished',format(Sys.time(),'%Y-%m-%dT%H:%M:%SZ',tz='UTC'),'status',status,'\n')
writeLines(as.character(status),marker)
base::quit(save='no',status=status)
