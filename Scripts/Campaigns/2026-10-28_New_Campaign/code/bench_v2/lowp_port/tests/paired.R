camp <- 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign'
old <- file.path(camp,'code/bench_v2/lowp_port/baseline_bench_lowp'); new <- file.path(camp,'code/bench_lowp')
study <- 'C:/Users/felip/AppData/Local/Temp/lowp_work/bench_study'
.libPaths(c('C:/Users/felip/AppData/Local/Temp/lowp_Rlib',.libPaths()))
env <- function(dir) { e <- new.env(parent=globalenv()); sys.source(file.path(dir,'R/config_lowp.R'),e); sys.source(file.path(dir,'R/common.R'),e); e }
a <- env(old); b <- env(new)
for (case in c('p0020_S1_r001','p0030_S4_r050','p0030_S6_r100')) for (scale in c('c100','c050')) {
  z <- readRDS(file.path(study,'inputs',substr(case,1,5),paste0(case,'.rds'))); p <- ncol(z$X)
  for (id in c('F1','F2','F4','F5','A1','A2','A3')) {
    ma <- a$lowp_load_method(id,old,p,TRUE); mb <- b$lowp_load_method(id,new,p,TRUE)
    x <- ma$fn(z$X,z$Y[,scale],z$foldid,z$method_seed,ma$settings)
    y <- mb$fn(z$X,z$Y[,scale],z$foldid,z$method_seed,mb$settings)
    xr <- x$rules; yr <- y$rules[match(xr$rule_id,y$rules$rule_id),names(xr),drop=FALSE]; rownames(xr) <- NULL; rownames(yr) <- NULL
    if (id=='A3') { xr$diag_s <- NULL; yr$diag_s <- NULL } # measured diagnostic wall time
    if (!identical(xr,yr)) { cat('ROW DIFFERENCE',case,scale,id,'\n'); print(all.equal(xr,yr)); stop('paired rule difference') }
    if (!identical(x$beta,y$beta)) { cat('BETA DIFFERENCE',case,scale,id,'\n'); print(all.equal(x$beta,y$beta)); stop('paired beta difference') }
    if (id=='F4') { d <- y$diagnostics; d$path_beta <- NULL; stopifnot(identical(x$diagnostics,d)) }
    cat(case,scale,id,'paired rows and beta identical\n'); flush.console()
  }
}
