options(width=180)
suppressPackageStartupMessages(library(glmnet))
D <- 'C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019'
cat('UTC:',format(Sys.time(),tz='UTC',usetz=TRUE),'\n'); print(sessionInfo())
truth <- read.csv(file.path(D,'manifests/truth_manifest.csv'),stringsAsFactors=FALSE)
decode <- function(x) if(is.na(x)||!nzchar(x)) integer() else sort(as.integer(strsplit(x,';',fixed=TRUE)[[1]]))
tr <- function(id) decode(truth$active[match(id,truth$dataset_id)])
if (!('cv_only' %in% commandArgs(TRUE))) {
run3 <- file.path(D,'results/20261019T2157Z_bench20261019_prod_F3_AdaptiveLasso/p0500')
counts <- list()
for(cs in list.files(run3)) {
 a <- readRDS(file.path(run3,cs,'F3.rds'))$rows
 id <- sub('_c100$','',cs)
 counts[[length(counts)+1L]] <- data.frame(rule=a$rule_id,scenario=a$scenario,status=a$status,exact=vapply(a$support,function(s) identical(decode(s),tr(id)),TRUE))
}
counts <- do.call(rbind,counts)
cat('\nCHECK 1: independent F3 p500 c100 recount\n'); print(xtabs(exact~rule+scenario,counts)); print(table(counts$status))
run5 <- file.path(D,'results/20261019T2157Z_bench20261019_prod_F5_ABESS')
rss <- function(X,y,s) if(!length(s)) sum(y*y) else sum(lm.fit(X[,s,drop=FALSE],y,tol=1e-10)$residuals^2)
ab <- list()
for(pp in c('p0500','p1000')) for(sc in c(1,4)) for(j in 1:100) {
 id <- sprintf('%s_S%d_r%03d',pp,sc,j)
 d <- readRDS(file.path(D,'inputs',pp,paste0(id,'.rds')))
 f <- readRDS(file.path(run5,pp,paste0(id,'_c100'),'F5.rds'))
 path <- f$diagnostics$path; ct <- f$diagnostics$candidates
 t <- tr(id); s <- decode(path$key[path$size==14]); y <- d$Y[,'c100']
 q <- which(ct$valid & ct$k<=37 & is.finite(ct$ebic1)); q <- q[order(ct$ebic1[q],ct$k[q],ct$key[q])][1]
 ab[[length(ab)+1L]] <- data.frame(p=pp,sc=sc,exact=identical(decode(f$rows$support[f$rows$rule_id=='ebic1']),t),K37=identical(decode(ct$key[q]),t),truth14=identical(s,t),truth_better=rss(d$X,y,t)<rss(d$X,y,s)-1e-9)
}
cat('\nCHECK 2: independent ABESS RSS/recount (400 datasets, c100)\n')
print(aggregate(cbind(exact,K37,truth14,truth_better)~p+sc,do.call(rbind,ab),sum))
}
cat('\nCHECK 3: independent F1 same-grid cv.glmnet (two datasets) and default-pilot comparison\n')
for(id in c('p0500_S1_r001','p0500_S2_r001')) {
 d <- readRDS(file.path(D,'inputs/p0500',paste0(id,'.rds'))); X<-d$X; y<-d$Y[,'c100']
 f<-readRDS(file.path(D,'results/20261019T2308Z_bench20261019_prod_F1_Lasso/p0500',paste0(id,'_c100'),'F1.rds'))
 path<-f$diagnostics$path
 stopifnot(length(path$lambda)==200, length(f$beta)==ncol(X))
 glmnet.control(factory=TRUE)
 pilot<-cv.glmnet(X,y,alpha=1,foldid=d$foldid,intercept=FALSE,standardize=FALSE,thresh=1e-10)
 bdefault<-as.numeric(coef(pilot,s='lambda.min'))[-1]
 glmnet.control(fdev=0,devmax=1)
 cv<-cv.glmnet(X,y,alpha=1,foldid=d$foldid,lambda=path$lambda,intercept=FALSE,standardize=FALSE,type.gaussian='naive',thresh=1e-16,maxit=10000000)
 for(rule in c('cv_min','cv_1se')) {
  lab<-if(rule=='cv_min') 'lambda.min' else 'lambda.1se'; s<-which(as.numeric(coef(cv,s=lab))[-1]!=0)
  row<-f$rows[f$rows$rule_id==rule,]
  cat(id,rule,'k=',length(s),'exact=',identical(s,tr(id)),'stored_support_match=',identical(s,decode(row$support)),'lambda_rel_error=',abs(cv[[lab]]/row$lambda-1),'\n')
 }
 stored_b<-f$beta
 cat(id,'default pilot k=',sum(bdefault!=0),'F1 stored k=',sum(stored_b!=0),'support_equal=',identical(which(bdefault!=0),which(stored_b!=0)),'max_abs_beta_difference=',max(abs(bdefault-stored_b)),'\n')
}
cat('END UTC:',format(Sys.time(),tz='UTC',usetz=TRUE),'\n')
