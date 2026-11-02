camp <- 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign'
lowp <- file.path(camp,'code/bench_lowp')
v2 <- file.path(camp,'code/bench_v2/repro/snapshot_2a8362b2f348')
e <- new.env(parent=globalenv()); sys.source(file.path(lowp,'R/config_lowp.R'),e); sys.source(file.path(lowp,'R/common.R'),e)
dirs <- c(F1='F1_Lasso', F2='F2_ElasticNet', F3='F3_AdaptiveLasso')
for (id in names(dirs)) {
  v <- new.env(parent=globalenv()); sys.source(file.path(v2,dirs[[id]],'config.R'),v)
  keys <- names(e$LOWP_PRODUCTION[[id]])
  for (key in keys) if (!identical(e$LOWP_PRODUCTION[[id]][[key]], get(key,envir=v,inherits=FALSE))) stop(id, ': ', key, ' differs')
  for (p in c(20L,30L)) {
    loaded <- e$lowp_load_method(id,lowp,p)$settings
    expected <- e$LOWP_PRODUCTION[[id]]; expected$variant <- 'primary'; expected$METHODS <- expected$METHODS[expected$METHODS$method_id == id,,drop=FALSE]; expected$COMMON$kmax_ebic <- min(100L,p)
    if (!identical(loaded,expected)) stop(id, ': low-p override differs for p=',p)
  }
  cat(id, 'config and p overrides identical\n')
}
