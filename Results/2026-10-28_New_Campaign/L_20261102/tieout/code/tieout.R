root <- 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/analysis/L_20261102/tieout'
d <- 'C:/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign'
claims <- read.csv(file.path(root,'CLAIMS.csv'), colClasses='character')
manifest <- read.csv(file.path(d,'inputs/lowp_study/manifests/inputs_manifest_lowp.csv'))
source(file.path(root,'code/core/v3.R'))
eq <- function(a,b) identical(sort(as.integer(a)),sort(as.integer(b)))
records <- list(); z <- 0L; issues <- character()
for (p in c(20,30)) for (scale in c('c050','c100')) {
 needed <- claims[as.integer(claims$p)==p & claims$scale_key==scale,]
 dat <- manifest[manifest$p==p & (manifest$scenario %in% as.integer(needed$scenario[needed$scenario!='all']) | 'all' %in% needed$scenario),]
 for (i in seq_len(nrow(dat))) {
  id <- dat$dataset_id[i]; sc <- dat$scenario[i]; cid <- paste0(id,'_',scale); pp <- sprintf('p%04d',p)
  ep <- file.path(d,'results',paste0('20261030T1811Z_lowp_enum',p),pp,id,'EXACT.rds')
  fp <- file.path(d,'results/20261030T1811Z_lowp_smc',pp,cid,'SMCBVS.rds')
  tp <- file.path(d,'inputs/lowp_study/truth',pp,paste0(id,'.rds'))
  z <- z+1L; row <- list(p=p,scale=scale,scenario=sc,id=id,ok=FALSE)
  tryCatch({
   exall <- readRDS(ep); ex <- exall$scales[[scale]]; fit <- readRDS(fp); truth <- readRDS(tp)$active
   stopifnot(exall$dataset_id==id, fit$case$case_id==cid, ex$status=='exact', isTRUE(exall$complete),length(ex$pip)==p,length(fit$pip)==p,length(fit$pip_plain)==p)
   row$ok <- TRUE; row$e <- fit$fit$log_Z-ex$log_Z
   row$h_eq <- eq(fit$fit$hpm,ex$hpm); row$ex_truth <- eq(ex$hpm,truth); row$sm_truth <- eq(fit$fit$hpm,truth)
   row$exmpm_truth <- eq(which(ex$pip>0.5),truth); row$mpm_eq <- eq(which(fit$pip>0.5),which(ex$pip>0.5))
   row$rb <- max(abs(unname(fit$pip)-unname(ex$pip))); row$plain <- max(abs(unname(fit$pip_plain)-unname(ex$pip)))
   if (sc==1 && scale=='c050') {
    if (row$sm_truth) row$miss <- FALSE else if (row$h_eq && isTRUE(ex$certified_over_scored_models) && exall$models_scored==exall$models_expected) row$miss <- TRUE else {
      input <- readRDS(file.path(d,'inputs/lowp_study/inputs',pp,paste0(id,'.rds'))); pre <- v3_preprocess(input$X,input$Y[,scale],FALSE); ctx <- v3_context(pre$X,pre$y,pre$kept)
      row$miss <- v3_score(ctx,truth)$F <= v3_score(ctx,fit$fit$hpm)$F
    }
   }
   if (p==20 && scale=='c100' && sc==5) {
    input <- readRDS(file.path(d,'inputs/lowp_study/inputs',pp,paste0(id,'.rds'))); pre <- v3_preprocess(input$X,input$Y[,scale],FALSE); ctx <- v3_context(pre$X,pre$y,pre$kept)
    blocks <- fit$fit$blocks; st <- v3_start(ctx,blocks,v3_tables(ctx,blocks)); stopifnot(abs(st$logZbar0-fit$fit$log_Zbar0)<1e-7)
    row$pi0 <- exp(v3_start_logmass(st,truth))
   }
   needsrep <- any(needed$cell_type=='stability' & (needed$scenario==as.character(sc) | needed$scenario=='all'))
   if (needsrep) {
    fs <- c(list(fit),lapply(1:5,function(k) readRDS(file.path(d,'results/20261030T1811Z_lowp_smcrep',pp,cid,paste0('SMCBVS_rep',k,'.rds')))))
    row$sdlog <- sd(vapply(fs,function(a) a$fit$log_Z,0.0)); row$same <- all(vapply(fs,function(a) eq(a$fit$hpm,fit$fit$hpm),TRUE)); row$sdpi <- max(apply(do.call(cbind,lapply(fs,function(a) unname(a$pip))),1,sd))
   }
  },error=function(e) {issues <<- c(issues,paste(cid,conditionMessage(e))); row$ok <- FALSE})
  records[[z]] <- row
  if (z%%100==0) cat('Processed',z,'\n')
 }
}
value <- function(x,key) vapply(x,function(r) if(is.null(r[[key]])) NA_real_ else as.numeric(r[[key]]),0.0)
res <- data.frame(cell_no=as.integer(claims$cell_no),claimed=claims$claimed,recomputed=NA_character_,verdict='UNVERIFIED',n_cases_used=0L,note='',stringsAsFactors=FALSE)
for (i in seq_len(nrow(claims))) {
 c <- claims[i,]; xs <- Filter(function(r) r$p==as.integer(c$p) && r$scale==c$scale_key && (c$scenario=='all' || r$scenario==as.integer(c$scenario)),records)
 xs <- Filter(function(r) isTRUE(r$ok),xs); n <- length(xs); res$n_cases_used[i] <- n
 expected <- if(c$scenario=='all') 600 else 100
 if(n!=expected) {res$note[i] <- paste('Expected',expected,'complete cases; see report.'); next}
 k <- as.integer(c$cell_no); e <- value(xs,'e')
 v <- if(k<=4) mean(e) else if(k<=7) sqrt(mean(e^2)) else if(k<=10) unname(quantile(abs(e),.9,type=7)) else if(k<=12) mean(e+log(.05)<=0) else if(k<=15) 100*mean(value(xs,'h_eq')) else if(k<=17) 100*mean(value(xs,'ex_truth')) else if(k<=19) 100*mean(value(xs,'sm_truth')) else if(k<=22) mean(value(xs,'rb')) else if(k<=25) mean(value(xs,'plain')) else if(k<=27) unname(quantile(value(xs,'plain'),.9,type=7)) else if(k<=29) 100*mean(value(xs,'mpm_eq')) else if(k %in% c(30,33)) sum(value(xs,'ex_truth')) else if(k %in% c(31,34,35)) sum(value(xs,'exmpm_truth')) else if(k==32) sum(value(xs,'sm_truth')) else if(k<=37) mean(value(xs,'sdlog')) else if(k<=39) 100*mean(value(xs,'same')) else if(k==40) mean(value(xs,'sdpi')) else if(k<=42) sum(value(xs,'miss')) else median(value(xs,'pi0'))
 if (!is.finite(v)) {res$note[i] <- 'Missing quantity'; next}
 res$recomputed[i] <- sprintf('%.12g',v)
 rounded <- if(k %in% c(1:10)) round(v,6) else if(k<=12) round(v,4) else if(k %in% c(13:19,28:29,38:39)) round(v,2) else if(k %in% c(30:35,41:42)) v else signif(v,6)
 res$verdict[i] <- if(isTRUE(all.equal(rounded,as.numeric(c$claimed),tolerance=1e-12))) 'MATCH' else 'MISMATCH'
}
write.csv(res,file.path(root,'TIEOUT_RESULT.csv'),row.names=FALSE,na='')
mis <- res[res$verdict=='MISMATCH',]
lines <- c('# Independent tie-out report','', 'Computed locally with R 4.4.1 from the input manifest, truth active indices, primary and repeat SMC records, and corresponding exact enumeration records. Dataset ID and scale key select exact scale and SMC case; log evidence uses fit$log_Z and scales[[scale]]$log_Z. Full-length adapter pip and pip_plain are compared with exact pip; sets use strict PIP > 0.5. Sample standard deviations use six seeds; quantiles use R type 7. Missing cases cause UNVERIFIED.', '', 'Posterior miss uses exact complete enumeration and certified-over-scored-models when the SMC HPM equals exact HPM; otherwise the core scorer evaluates both truth and SMC HPM. Start mass is independently reconstructed from raw X and matching Y, core preprocessing, recorded blocks, core block tables and start distribution; reconstructed log normalizer is checked against the saved fit.', '', '## Mismatches','',if(nrow(mis)) sprintf('- Cell %s: claimed %s; recomputed %s.',mis$cell_no,mis$claimed,mis$recomputed) else 'None.', '', '## Data observations','',if(length(issues)) issues else 'No missing, failed, or misaligned records encountered in the selected cases.', '', paste('Overall:',paste(names(table(res$verdict)),as.integer(table(res$verdict)),collapse=', '),'.'))
writeLines(lines,file.path(root,'TIEOUT_REPORT.md'),useBytes=TRUE)
print(res); print(table(res$verdict))
