C <- 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign'
V <- file.path(C,'code/bench_v2'); D <- 'C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019/dev'
cat('START',format(Sys.time(),tz='UTC'),'\n')
key <- function(b) paste(which(b != 0),collapse=';')
near <- function(a,b) stopifnot(isTRUE(all.equal(unname(a),unname(b),tolerance=1e-10,check.attributes=FALSE)))
files <- list.files(file.path(V,'repro/controlled_2a8362b2f348'),pattern='^dev_.*[.]rds$',full.names=TRUE)
stopifnot(length(files)==24L)
for (file in files) {
 z <- readRDS(file); d <- readRDS(file.path(D,'inputs',substr(z$case,5,9),paste0(z$case,'.rds')))
 stopifnot(identical(z$input_sha256,digest::digest(file=file.path(D,'inputs',substr(z$case,5,9),paste0(z$case,'.rds')),algo='sha256')))
 y <- unname(d$Y[,z$scale]); X <- d$X; n <- nrow(X); p <- ncol(X)
 for (m in c('F1','F2')) {
   old <- z[[m]]$old$result; new <- z[[m]]$new$result
   rr <- new$rules[match(old$rules$rule_id,new$rules$rule_id),names(old$rules),drop=FALSE]
   stopifnot(identical(as.list(rr),as.list(old$rules)),identical(old$beta,new$beta),identical(old$diagnostics,new$diagnostics),identical(old$converged,new$converged))
 }
 o <- z$F3$result; b <- o$diagnostics$pilot$beta
 stopifnot(identical(b,z$F1$new$result$beta),identical(which(b!=0),o$diagnostics$keep))
 w <- 1/abs(b[b!=0]); near(w,o$diagnostics$w); near(length(w)*(w/max(w))/sum(w/max(w)),o$diagnostics$v)
 for (m in c('F1','F2','F3')) {
   f <- if(m=='F3') o else z[[m]]$new$result
   for(i in seq_len(nrow(f$rules))) {
     r <- f$rules[i,]; co <- f$coefficients[[r$rule_id]]
     stopifnot(identical(key(co$beta_pen),r$support),identical(co$status,r$status),identical(co$support,r$support))
     near(co$index,r$index);near(co$lambda,r$lambda);near(co$k,r$k)
     if(startsWith(r$rule_id,'ebic')) {
       idx <- which(co$beta_pen!=0); beta <- numeric(p)
       if(length(idx)) beta[idx] <- lm.fit(X[,idx,drop=FALSE],y,tol=1e-10)$coefficients
       near(beta,co$beta_ols)
     } else stopifnot(all(is.na(co$beta_ols)))
   }
   ca <- f$diagnostics$candidates
   for(g in c('ebic1','ebic05')) {
     gamma <- if(g=='ebic1') 1 else .5
     expected <- n*log(ca$rss/n)+ca$k*log(n)+2*gamma*lchoose(p,ca$k); expected[!ca$valid] <- Inf
     near(expected,ca[[g]])
     for(cap in c(100,37)) {
       eligible <- which(ca$valid & ca$k<=cap)
       pick <- eligible[order(expected[eligible],ca$k[eligible],ca$key[eligible],method='radix')[1]]
       rid <- paste0(g,if(cap==37)'_K37' else '')
       rr <- f$rules[f$rules$rule_id==rid,]
       stopifnot(identical(rr$support,ca$key[pick]));near(rr$crit_value,expected[pick])
     }
   }
 }
 cat('SAVED_PASS',basename(file),'\n')
}
cat('24/24 independent saved identity, pilot, all-rule evidence, OLS, full-p EBIC and K37 PASS\n')
# Own direct second-stage calls; no wrapper/helper fitting code is used here.
glmnet::glmnet.control(fdev=0,devmax=1)
for(nm in c('dev_p0500_S1_r001_c100.rds','dev_p1000_S4_r001_c050.rds')) {
 z <- readRDS(file.path(V,'repro/controlled_2a8362b2f348',nm));o <- z$F3$result;di <- o$diagnostics
 d <- readRDS(file.path(D,'inputs',substr(z$case,5,9),paste0(z$case,'.rds')))
 x <- d$X[,di$keep,drop=FALSE];y <- unname(d$Y[,z$scale]);v <- di$v
 lam <- 1.01*max(abs(drop(crossprod(x,y)))/nrow(x)/v)*exp(seq(0,log(1e-4),length.out=200))
 near(lam,di$path$lambda)
 fit <- function(xx,yy) as.matrix(glmnet::glmnet(xx,yy,alpha=1,lambda=lam,penalty.factor=v,intercept=FALSE,standardize=FALSE,type.gaussian='naive',thresh=1e-16,maxit=1e7)$beta)
 B <- fit(x,y);stopifnot(identical(vapply(seq_len(200),function(i)paste(di$keep[which(B[,i]!=0)],collapse=';'),''),di$path$key))
 oof <- matrix(NA_real_,nrow(x),200)
 for(k in 1:10) { te <- d$foldid==k;oof[te,] <- x[te,,drop=FALSE]%*%fit(x[!te,,drop=FALSE],y[!te]) }
 mse <- sapply(1:10,function(k)colMeans((y[d$foldid==k]-oof[d$foldid==k,,drop=FALSE])^2))
 cvm <- rowMeans(mse); se <- sqrt(rowSums((mse-cvm)^2)/10/9)
 near(cvm,di$path$cvm);near(se,di$path$cvsd)
 for(co in o$coefficients) { expected <- numeric(ncol(d$X));if(!is.na(co$index))expected[di$keep] <- B[,co$index];near(expected,co$beta_pen) }
 cat('DIRECT_SECOND_STAGE_PASS',nm,'\n')
}
# Independently inspect low-p F1--F5 saved smoke evidence, including derived rows.
lf <- list.files(file.path(V,'lowp_port/smoke_output/results/smoke'),pattern='^F[1-5][.]rds$',recursive=TRUE,full.names=TRUE)
stopifnot(length(lf)==30)
for(f in lf) {
 z <- readRDS(f); rows <- z$rows; p <- rows$p[1]
 d <- readRDS(z$input$path); y <- d$Y[,rows$scale_key[1]];X <- d$X
 stopifnot(identical(z$schema_version,2L),identical(names(z$coefficients),rows$rule_id),sum(rows$role=='primary')==1)
 for(i in seq_len(nrow(rows))) {
   r <- rows[i,];co <- z$coefficients[[r$rule_id]]
   stopifnot(length(co$beta_pen)==p,length(co$beta_ols)==p,identical(key(co$beta_pen),r$support))
   if(startsWith(r$rule_id,'ebic')||r$rule_id %in% c('bic','bic_K37','sic_smax')) {
     beta <- numeric(p); idx <- which(co$beta_pen!=0)
     if(length(idx))beta[idx] <- lm.fit(X[,idx,drop=FALSE],y,tol=1e-10)$coefficients
     near(beta,co$beta_ols)
   }
   if(rows$method_id[1]=='F4'&&!is.na(co$index)) near(co$beta_pen,z$fit$diagnostics$path_beta[,co$index])
 }
 for(rid in intersect(c('ebic1','ebic05','bic'),rows$rule_id)) {
   a <- which(rows$rule_id==rid);b <- which(rows$rule_id==paste0(rid,'_K37'))
   stopifnot(length(b)==1,identical(rows$support[a],rows$support[b]),identical(z$coefficients[[a]]$beta_pen,z$coefficients[[b]]$beta_pen))
 }
 cat('LOWP_PASS',sub('.*smoke/','',f),'\n')
}
cat('30/30 low-p smoke records independently checked\n')
# Demonstrate the actual bundle validator's acceptance gaps on real runner output.
ve <- new.env();sys.source(file.path(C,'bench_audit/jobs/BENCH_F3_PROD/runner/validate.R'),ve)
real <- list.files(file.path(V,'tests/runner_output'),pattern='^F3[.]rds$',recursive=TRUE,full.names=TRUE)[1]
x <- readRDS(real);stopifnot(ve$validate_object(x,x$rows,x$prov$source_sha256))
for(fault in c('missing_OLS','bad_index','bad_k','missing_pilot','retired_code','wrong_role','wrong_input_hash','wrong_numeric_beta','wrong_csv_criterion','bad_failed_vector')) {
 a <- x;csv <- a$rows
 if(fault=='missing_OLS') a$coefficients[[3]]$beta_ols <- NULL
 if(fault=='bad_index') a$coefficients[[1]]$index <- -999L
 if(fault=='bad_k') a$rows$k[1] <- csv$k[1] <- 999L
 if(fault=='missing_pilot') a$fit$diagnostics$pilot <- NULL
 if(fault=='retired_code') a$rows$diag_codes[1] <- csv$diag_codes[1] <- 'kappa_edge'
 if(fault=='wrong_role') a$rows$role[1] <- csv$role[1] <- 'S0'
 if(fault=='wrong_input_hash') a$rows$inputs_sha256 <- csv$inputs_sha256 <- strrep('0',64)
 if(fault=='wrong_numeric_beta') a$coefficients[[1]]$beta_pen <- 2*a$coefficients[[1]]$beta_pen
 if(fault=='wrong_csv_criterion') csv$crit_value[3] <- 123456
 if(fault=='bad_failed_vector') { a$rows$status[1] <- csv$status[1] <- a$coefficients[[1]]$status <- 'failed';a$rows$support[1] <- csv$support[1] <- a$coefficients[[1]]$support <- NA_character_;a$coefficients[[1]]$beta_pen <- rep(Inf,a$rows$p[1]) }
 accepted <- tryCatch(ve$validate_object(a,csv,a$prov$source_sha256),error=function(e)FALSE)
 cat('BUNDLE_VALIDATOR_CORRUPTION',fault,'accepted',accepted,'\n')
}
cat('END',format(Sys.time(),tz='UTC'),'\n')
