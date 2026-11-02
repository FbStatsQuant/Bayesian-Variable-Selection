# Compare all saved RDS fields after removing measured timing fields.
root <- 'C:/Users/felip/AppData/Local/Temp/lowp_work/bench_smoke/results'
case <- 'p0020/p0020_S1_r001_c100'; ids<-c('F1','F2','F3','F4','F5','A1','A2','A3')
strip_time <- function(x) {
 if (is.data.frame(x)) { x <- x[,!grepl('runtime|elapsed|(^|_)time(_|$)|^diag_s$',names(x),ignore.case=TRUE),drop=FALSE]; return(x) }
 if (is.list(x)) { keep <- !grepl('runtime|elapsed|(^|_)time(_|$)|^diag_s$',names(x),ignore.case=TRUE); if(!is.null(names(x)))x<-x[keep];return(lapply(x,strip_time)) }; x
}
for(id in ids) { a<-readRDS(file.path(root,'smoke',case,paste0(id,'.rds')));b<-readRDS(file.path(root,'repeat',case,paste0(id,'.rds')));cat(id,'supports=',identical(a$rules$support,b$rules$support),'all_except_timing=',identical(strip_time(a),strip_time(b)),'\n') }
