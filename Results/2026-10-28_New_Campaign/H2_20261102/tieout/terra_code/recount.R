root <- 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian'
out <- file.path(root,'02_Experiments/I_2026-10-28_New_Campaign/analysis/H2_20261102/tieout')
claims <- read.csv(file.path(out,'CLAIMS.csv'), stringsAsFactors=FALSE, na.strings=c('','NA'))
new <- 'C:/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign/results/20261030T0934Z_prodH'
old <- 'C:/Users/felip/Documents/NOTS_BVS/smcbvs_v3_deploy_20261022/claude'
truth <- file.path(root,'02_Experiments/F_2026-10-19_benchmark_study_n200/Benchmark_Study_20261019/verify/recount/c050/inputs/truth_scoring')
val <- rep(NA_real_,51); val[c(1:15,22:36,38:41)] <- 0; mx <- 0; problems <- character()
eq <- function(a,b) identical(sort(as.integer(a)),sort(as.integer(b)))
for (p in c(500,1000)) for (s in 1:6) for (r in 1:100) {
 pd <- sprintf('p%04d',p); ds <- sprintf('%s_S%d_r%03d',pd,s,r)
 tf <- file.path(truth,pd,paste0(ds,'.rds')); t <- tryCatch(readRDS(tf)$active,error=function(e) NULL)
 for (scale in c('c050','c100')) {
  id <- paste(ds,scale,sep='_'); nf <- file.path(new,pd,id,'SMCBVS.rds'); of <- file.path(old,paste0('prod_',pd,'_20261023T1227Z'),pd,id,'SMCBVS.rds')
  a <- tryCatch(readRDS(nf),error=function(e) NULL); b <- tryCatch(readRDS(of),error=function(e) NULL)
  if (is.null(a)||is.null(b)||is.null(t)) { problems <- c(problems,paste('Missing or unreadable:',id)); next }
  fieldsA <- list(a$fit$log_Z,a$fit$hpm,a$fit$pip_primary,unname(a$pip),a$native_status)
  fieldsB <- list(b$fit$log_Z,b$fit$hpm,b$fit$pip_primary,unname(b$pip),b$native_status)
  for (j in 1:5) val[21+j] <- val[21+j]+identical(fieldsA[[j]],fieldsB[[j]])
  ok <- identical(a$native_status,'completed'); lim <- identical(a$native_status,'resource_limit')
  val[27] <- val[27]+lim; val[28] <- val[28]+(lim && identical(a$instrumentation$stop$phase,'diag'))
  if (p==1000 && scale=='c100') val[29] <- val[29]+isTRUE(a$fit$flags$escalated)
  if (p==500 && scale=='c050') val[30] <- val[30]+isTRUE(a$fit$flags$escalated)
  val[31] <- val[31]+identical(a$instrumentation$scored$mode,'hll'); val[32] <- val[32]+is.null(a$instrumentation$scored$first_scored)
  if (ok) {
   val[33] <- val[33]+isTRUE(a$fit$local_search$moves>0); val[34] <- val[34]+identical(a$fit$hpm_provenance$phase,'pilot')
   val[35] <- val[35]+eq(a$fit$local_search$centre,t); val[36] <- val[36]+eq(which(a$pip>0.5),which(a$pip_plain>0.5))
   mx <- max(mx,abs(a$pip-a$pip_plain))
   fp <- length(setdiff(a$hpm,t)); fn <- length(setdiff(t,a$hpm))
   if (p==500 && scale=='c100') val[38] <- val[38]+(fp>0 && fn==0)
   if (p==500 && scale=='c050') val[39] <- val[39]+(fp>0 && fp==fn)
   if (p==1000 && scale=='c050') { val[40] <- val[40]+(fp==0 && fn>0); val[41] <- val[41]+(fp>0 && fn>0 && fp!=fn) }
  }
  for (i in 1:15) if (p==claims$p[i] && scale==claims$scale[i] && (claims$scenario[i]=='pooled' || as.character(s)==claims$scenario[i])) {
   sel <- switch(claims$rule[i],hpm=a$hpm,mpm_rb=which(a$pip>0.5),mpm_plain=which(a$pip_plain>0.5))
   val[i] <- val[i]+(ok && eq(sel,t))
  }
 }
}
val[37] <- mx
saveRDS(list(value=val,problems=problems),file.path(out,'terra_code','recount.rds'))
