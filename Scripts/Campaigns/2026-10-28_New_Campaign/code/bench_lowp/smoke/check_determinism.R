root <- 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2/lowp_port/smoke_output/results'
case <- 'p0020/p0020_S1_r001_c100'; ids <- c(paste0('F',1:5),paste0('A',1:3))
for(id in ids) {
 a <- readRDS(file.path(root,'smoke',case,paste0(id,'.rds'))); b <- readRDS(file.path(root,'repeat',case,paste0(id,'.rds')))
 x <- a$rows; y <- b$rows; omit <- c('run_id','runtime_s','started_utc','finished_utc','diag_s'); x <- x[,setdiff(names(x),omit),drop=FALSE]; y <- y[,setdiff(names(y),omit),drop=FALSE]
 strip_time <- function(z) { if(is.data.frame(z)) return(z[,setdiff(names(z),'diag_s'),drop=FALSE]); if(is.list(z)) { z$diag_s <- NULL; return(lapply(z,strip_time)) }; z }
 stopifnot(identical(x,y),identical(strip_time(a$fit),strip_time(b$fit)),identical(a$coefficients,b$coefficients))
 cat(id,'deterministic rows, fit and coefficients\n')
}
