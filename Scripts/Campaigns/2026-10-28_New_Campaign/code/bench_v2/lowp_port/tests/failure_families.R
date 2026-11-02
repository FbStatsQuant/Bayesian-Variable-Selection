camp <- 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign'; code <- file.path(camp,'code/bench_lowp')
source(file.path(code,'R/config_lowp.R')); source(file.path(code,'R/common.R'))
z <- readRDS('C:/Users/felip/AppData/Local/Temp/lowp_work/bench_study/inputs/p0020/p0020_S1_r001.rds')
for(id in c('F1','F2','F3')) {
 m <- lowp_load_method(id,code,20L,TRUE); m$env$glmnet_cv_engine <- function(...) stop('injected engine failure')
 f <- m$fn(z$X,z$Y[,'c100'],z$foldid,z$method_seed,m$settings)
 stopifnot(all(f$rules$status=='failed'),length(f$coefficients)==6L,all(vapply(f$coefficients,function(x)all(is.na(x$beta_pen)) && all(is.na(x$beta_ols)),TRUE)))
 cat(id,'injected engine failure yields six NA coefficient pairs\n')
}
for(id in c('F1','F2')) {
 m <- lowp_load_method(id,code,20L,TRUE); m$settings$GLMNET$kkt_rel_tol <- -1
 f <- m$fn(z$X,z$Y[,'c100'],z$foldid,z$method_seed,m$settings)
 stopifnot(all(f$rules$status[1:2]=='failed'))
 for(i in which(f$rules$status=='failed')) stopifnot(all(is.finite(f$coefficients[[i]]$beta_pen)),identical(m$env$support_key(which(f$coefficients[[i]]$beta_pen!=0)),f$rules$support_audit[i]))
 cat(id,'failed-rule audit vectors passed\n')
}
