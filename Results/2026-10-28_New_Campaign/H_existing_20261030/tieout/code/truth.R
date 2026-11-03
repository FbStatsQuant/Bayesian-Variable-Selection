args <- commandArgs(trailingOnly=TRUE)
truthroot <- args[1]
out <- args[2]
rows <- list()
for (p in c(500,1000)) for (s in 1:6) for (r in 1:100) {
  id <- sprintf('p%04d_S%d_r%03d',p,s,r)
  path <- file.path(truthroot,sprintf('p%04d',p),paste0(id,'.rds'))
  x <- readRDS(path)
  if (!identical(x$dataset_id,id) || length(x$active)!=14 || anyDuplicated(x$active)) stop(paste('Invalid truth',id))
  rows[[length(rows)+1]] <- data.frame(dataset_id=id,active=paste(sort(x$active),collapse=';'))
}
write.csv(do.call(rbind,rows),out,row.names=FALSE,quote=TRUE)
