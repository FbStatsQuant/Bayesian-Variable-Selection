camp <- 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign'
code <- file.path(camp,'code/bench_lowp')
source(file.path(code,'R/config_lowp.R')); source(file.path(code,'R/common.R'))
rejects <- function(expr) inherits(tryCatch({force(expr); NULL},error=identity),'error')
pilot_engine <- function(beta) function(X,y,foldid,alpha,lam,pf,G) {
  L <- length(lam); K <- max(foldid)
  list(full=list(B=matrix(rep(beta,L),nrow=length(beta)),s=1,jerr=0L,npasses=0,kkt=rep(0,L)),
       cvm=seq_len(L),cvsd=rep(0,L),kkt_fold=matrix(0,K,L),
       fold_diag=rep(list(list(s=1,jerr=0L,npasses=0)),K))
}
for (p in c(20L,30L)) {
  set.seed(200L+p); n <- 200L; X <- scale(matrix(rnorm(n*p),n,p)); attributes(X) <- list(dim=c(n,p)); y <- as.numeric(2*X[,3]+rnorm(n)); fold <- rep(1:10,length.out=n)
  m <- lowp_load_method('F3',code,p,TRUE); m$settings$GRID$nlambda <- 24L
  m$env$assert_pkg_version <- function(...) invisible(TRUE)
  m$env$glmnet_cv_engine <- pilot_engine(rep(0,p))
  zero <- m$fn(X,y,fold,1L,m$settings)
  stopifnot(all(zero$rules$status=='ok'),all(zero$rules$diag_codes=='pilot_null'),all(zero$beta==0))
  b <- numeric(p); b[3] <- 2; m$env$glmnet_cv_engine <- pilot_engine(b)
  one <- m$fn(X,y,fold,1L,m$settings)
  stopifnot(all(one$rules$status=='ok'),all(grepl('pilot_single',one$rules$diag_codes)),identical(one$diagnostics$keep,3L))
  lam <- one$diagnostics$path$lambda
  mse <- sapply(1:10,function(k) { tr <- fold!=k; te <- !tr; z <- sum(X[tr,3]*y[tr])/sum(tr); g <- sum(X[tr,3]^2)/sum(tr); coef <- sign(z)*pmax(abs(z)-lam,0)/g; colMeans((y[te]-outer(X[te,3],coef))^2) })
  avg <- rowMeans(mse); se <- sqrt(rowSums((mse-avg)^2)/10/9); imin <- which.min(avg); i1 <- min(which(avg<=avg[imin]+se[imin]))
  stopifnot(isTRUE(all.equal(avg,one$diagnostics$path$cvm,tolerance=1e-12)),isTRUE(all.equal(se,one$diagnostics$path$cvsd,tolerance=1e-12)),one$rules$index[1]==imin,one$rules$index[2]==i1)
  real_scalar <- m$env$scalar_cv_engine
  m$env$scalar_cv_engine <- local({ original <- real_scalar; engine <- m$env; function(...) { q <- original(...); ii <- engine$cv_choose(q$cvm,q$cvsd)[['min']]; q$full$kkt[ii] <- 1; q } })
  broken <- m$fn(X,y,fold,1L,m$settings); pen <- broken$coefficients$cv_min$beta_pen
  stopifnot(broken$rules$status[1]=='failed',all(is.finite(pen)),identical(m$env$support_key(which(pen!=0)),broken$rules$support_audit[1]))
  cat('F3 failed-rule audit vector passed p=',p,'\n')
  for (fit in list(zero,one)) {
    rows <- lowp_derive(fit,'F3',p,n,'c100')
    stopifnot(!anyDuplicated(rows$rule_id))
    bad <- fit; bad$rules <- rbind(bad$rules,bad$rules[bad$rules$rule_id=='ebic1_K37',]); stopifnot(rejects(lowp_derive(bad,'F3',p,n,'c100')))
    bad <- fit; bad$rules$role[bad$rules$rule_id=='ebic1_K37'] <- 'primary'; stopifnot(rejects(lowp_derive(bad,'F3',p,n,'c100')))
    bad <- fit; bad$rules$support[bad$rules$rule_id=='ebic1_K37'] <- '1'; stopifnot(rejects(lowp_derive(bad,'F3',p,n,'c100')))
  }
  cat('edge and LA-4 controls passed p=',p,'\n')
}
X <- diag(3); y <- c(1,2,3)
rows <- data.frame(rule_id='ebic1',status='ok',support='1',support_audit=NA_character_)
fit <- list(diagnostics=list(path=data.frame(key='1',passes=TRUE,lambda=1),path_beta=matrix(c(1,0,0),ncol=1)))
stopifnot(identical(lowp_coefficients(fit,rows,'F4',X,y,1e-10)$ebic1$beta_pen,c(1,0,0)))
fit$diagnostics$path_beta[1,1] <- 0
stopifnot(rejects(lowp_coefficients(fit,rows,'F4',X,y,1e-10)))
cat('support/beta corruption rejected\n')
