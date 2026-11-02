camp <- 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign'
code <- file.path(camp,'code/bench_lowp'); out <- file.path(camp,'code/bench_v2/lowp_port/smoke_output/results/smoke')
e <- new.env(parent=globalenv()); sys.source(file.path(code,'R/config_lowp.R'),e); sys.source(file.path(code,'R/common.R'),e)
v <- new.env(parent=globalenv()); sys.source(file.path(camp,'code/bench_v2/F3_AdaptiveLasso/tests/validate_outputs.R'),v)
for (case in c('p0020_S1_r001','p0030_S4_r050','p0030_S6_r100')) for (scale in c('c100','c050')) for(id in paste0('F',1:5)) {
  rec <- readRDS(file.path(out,substr(case,1,5),paste0(case,'_',scale),paste0(id,'.rds'))); rows <- rec$rows; p <- rows$p[1]
  stopifnot(identical(rec$schema_version,2L),identical(names(rec$coefficients),rows$rule_id),identical(rec$coefficients,rec$fit$coefficients),!anyDuplicated(rows$rule_id))
  for (i in seq_len(nrow(rows))) {
    z <- rec$coefficients[[i]]; stopifnot(identical(z$rule_id,rows$rule_id[i]),identical(z$status,rows$status[i]),length(z$beta_pen)==p,length(z$beta_ols)==p)
    if (rows$status[i] != 'failed') stopifnot(identical(paste(which(z$beta_pen!=0),collapse=';'),rows$support[i]))
  }
  for (rid in c('ebic1','ebic05')) {
    x <- rows[rows$rule_id==rid,,drop=FALSE]; y <- rows[rows$rule_id==paste0(rid,'_K37'),,drop=FALSE]
    stopifnot(nrow(x)==1L,nrow(y)==1L,x$role=='secondary',y$role==if(id %in% c('F4','F5') && rid=='ebic1') 'primary' else 'S0',identical(x$support,y$support),identical(x$k,y$k),identical(x$crit_value,y$crit_value))
  }
  if (id=='F3') {
    mod <- e$lowp_load_method(id,code,p,TRUE); rr <- rows
    rr$role <- mod$registry$roles[[1]]
    problems <- v$validate_payload(rec,rr,mod$settings,mod$env)
    if(length(problems)) stop(paste(problems,collapse='; '))
  }
  if (id=='F4') {
    inp <- readRDS(file.path('C:/Users/felip/AppData/Local/Temp/lowp_work/bench_study/inputs',substr(case,1,5),paste0(case,'.rds')))
    mod <- e$lowp_load_method(id,code,p,TRUE); d <- rec$fit$diagnostics
    check_path <- function(B) isTRUE(all.equal(mod$env$kkt_mcp(inp$X,inp$Y[,scale],B,d$path$lambda,mod$settings$F4$mcp_gamma),d$path$kkt_max,tolerance=1e-12))
    stopifnot(check_path(d$path_beta)); corrupt <- d$path_beta; corrupt[1,1] <- corrupt[1,1]+10; stopifnot(!check_path(corrupt))
    cat('F4 path_beta tampering rejected\n')
  }
  cat(case,scale,id,'evidence and aliases valid\n')
}
