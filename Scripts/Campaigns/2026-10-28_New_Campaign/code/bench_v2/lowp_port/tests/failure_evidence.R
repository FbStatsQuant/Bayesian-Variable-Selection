camp <- 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign'; source(file.path(camp,'code/bench_lowp/R/common.R'))
X <- diag(3); y <- c(1,2,3)
row <- data.frame(rule_id='ebic1',status='failed',support=NA_character_,support_audit=NA_character_,k=NA_integer_)
for (id in c('F4','F5')) {
 z <- lowp_coefficients(list(diagnostics=NULL),row,id,X,y,1e-10)[[1]]; stopifnot(all(is.na(z$beta_pen)),all(is.na(z$beta_ols)),is.na(z$support),is.na(z$k)); cat(id,'whole-fit failure NA evidence passed\n')
 row$support_audit <- '1'; path <- data.frame(key='1',passes=FALSE,lambda=1)
 d <- list(path=path,path_beta=matrix(c(1,0,0),ncol=1),coefficients=list(1))
 z <- lowp_coefficients(list(diagnostics=d),row,id,X,y,1e-10)[[1]]
 stopifnot(identical(z$beta_pen,c(1,0,0)),is.na(z$support),is.na(z$k),identical(z$status,'failed')); cat(id,'failed-rule audit vector passed\n')
 row$support_audit <- NA_character_
}
