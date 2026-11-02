C <- 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign';V <- file.path(C,'code/bench_v2')
# Exact baseline/current configuration objects after legitimate D3 overrides.
cfg <- new.env();sys.source(file.path(C,'code/bench_lowp/R/config_lowp.R'),cfg)
for (p in c(20L,30L)) for(m in c('F1','F2','F3')) {
 folder <- c(F1='F1_Lasso',F2='F2_ElasticNet',F3='F3_AdaptiveLasso')[[m]]
 e <- new.env();sys.source(file.path(V,folder,'config.R'),e)
 a <- switch(m,F1={s <- as.list(e);s$variant <- 'primary';s},F2=e$make_settings(),F3=e$study_settings())
 b <- cfg$LOWP_PRODUCTION[[m]]
 for(nm in c('COMMON','GRID','GLMNET',m))stopifnot(identical(a[[nm]],b[[nm]]))
 cat('CONFIG_EQUAL',m,'p',p,'\n')
}
