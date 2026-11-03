base <- 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/analysis/L_20261102/tieout_bench'
d <- 'C:/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign'
claims <- read.csv(file.path(base,'CLAIMS_BENCH.csv'), stringsAsFactors=FALSE)
man <- read.csv(file.path(d,'inputs/lowp_study/manifests/inputs_manifest_lowp.csv'), stringsAsFactors=FALSE)
stopifnot(nrow(claims)==25, !anyDuplicated(man$dataset_id))
library(leaps)
parse_support <- function(s,p) {
  if(length(s)!=1 || is.na(s)) stop('missing support')
  if(s=='') return(integer())
  parts <- strsplit(s,';',fixed=TRUE)[[1]]
  if(any(!grepl('^[0-9]+$',parts))) stop('malformed support')
  z <- as.integer(parts)
  if(any(z<1 | z>p) || anyDuplicated(z)) stop('invalid support')
  sort(z)
}
out <- vector('list',nrow(claims)); odd <- character()
for(i in seq_len(nrow(claims))) {
 cl <- claims[i,]; m <- man[man$p==cl$p & (cl$scenario=='all' | man$scenario==as.integer(cl$scenario)),]
 expected <- if(cl$scenario=='all') 600L else 100L
 if(nrow(m)!=expected) stop(paste('manifest unexpected count cell',cl$cell_no))
 val <- 0L; used <- 0L; failures <- 0L; unknown <- 0L; reasons <- character(); flagged <- character()
 for(j in seq_len(nrow(m))) {
  id <- m$dataset_id[j]; pp <- sprintf('p%04d',cl$p); case <- paste0(id,'_',cl$scale_key)
  result <- tryCatch({
   truth <- readRDS(file.path(d,'inputs/lowp_study/truth',pp,paste0(id,'.rds')))$active
   if(anyNA(truth) || anyDuplicated(truth) || any(truth<1 | truth>cl$p)) stop('invalid truth')
   if(cl$method_id=='SMCBVS') {
    path <- file.path(d,'results/20261030T1811Z_lowp_smc',pp,case,'SMCBVS.rds')
    if(!file.exists(path)) list(count=0L, failure='missing SMC record') else {
     pip <- readRDS(path)$pip_plain
     if(length(pip)!=cl$p || anyNA(pip) || any(!is.finite(pip))) stop('invalid plain PIP')
     list(count=as.integer(setequal(which(pip>0.5),truth)),failure='')
    }
   } else {
    path <- file.path(d,'results/20261102T2309Z_lowp_benchres',pp,case,paste0(cl$method_id,'.rds'))
    if(!file.exists(path)) {
      if(cl$cell_type=='abess_size') stop('missing benchmark record for size check')
      list(count=0L,failure='missing record')
    } else {
     rows <- readRDS(path)$rows; row <- rows[!is.na(rows$rule_id) & rows$rule_id==cl$rule_id,,drop=FALSE]
     if(nrow(row)>1) stop('duplicate rule rows')
     if(nrow(row)==0 || is.na(row$status) || row$status!='ok') {
      if(cl$cell_type=='abess_size') stop('missing or failed row for size check')
      list(count=0L,failure=if(nrow(row)==0) 'missing rule' else paste0('status=',row$status))
     } else {
      s <- parse_support(row$support,cl$p)
      if(cl$cell_type=='recovery') list(count=as.integer(setequal(s,truth)),failure='') else {
       dat <- readRDS(file.path(d,'inputs/lowp_study/inputs',pp,paste0(id,'.rds')))
       x <- dat$X; y <- dat$Y[,cl$scale_key]; y <- y-mean(y); k <- length(s)
       rss <- if(k==0) sum(y*y) else sum(qr.resid(qr(x[,s,drop=FALSE]),y)^2)
       if(k==0) best <- sum(y*y) else {
        fit <- regsubsets(x,y,nvmax=k,intercept=FALSE,method='exhaustive',really.big=TRUE)
        best <- summary(fit)$rss[k]
       }
       if(!is.finite(rss) || !is.finite(best) || rss < best - 1e-8*max(1,best)) stop('invalid exhaustive RSS comparison')
       list(count=as.integer(rss-best>1e-8*max(1,best)),failure='',detail=sprintf('%s k=%d RSS=%.12g best=%.12g',case,k,rss,best))
      }
     }
    }
   }
  },error=function(e) list(error=conditionMessage(e)))
  if(!is.null(result$error)) {unknown <- unknown+1L; reasons <- c(reasons,paste(case,result$error))} else {
    used <- used+1L; val <- val+result$count
    if(nzchar(result$failure)) {failures <- failures+1L; reasons <- c(reasons,paste(case,result$failure))}
    if(cl$cell_type=='abess_size' && result$count==1L) flagged <- c(flagged,result$detail)
  }
 }
 verdict <- if(unknown>0) 'UNVERIFIED' else if(val==cl$claimed) 'MATCH' else 'MISMATCH'
 note <- paste0('expected=',expected,'; unknown=',unknown,'; failed/missing counted as unrecovered=',failures)
 out[[i]] <- data.frame(cell_no=cl$cell_no,claimed=cl$claimed,recomputed=if(unknown>0) NA_integer_ else val,verdict=verdict,n_cases_used=used,note=note)
 if(length(reasons)) odd <- c(odd,paste0('Cell ',cl$cell_no,': ',paste(reasons,collapse=' | ')))
 if(length(flagged)) odd <- c(odd,paste0('Cell ',cl$cell_no,' above optimum: ',paste(flagged,collapse=' | ')))
 cat('Cell',cl$cell_no,verdict,'value',val,'unknown',unknown,'\n'); flush.console()
}
res <- do.call(rbind,out)
write.csv(res,file.path(base,'TIEOUT_RESULT.csv'),row.names=FALSE,na='')
mis <- res[res$verdict=='MISMATCH',]
lines <- c('# Independent benchmark tie-out','', 'Recovery: read the manifest dataset IDs, p and scenario; truth `active`; benchmark `rows` fields `rule_id`, `status`, and `support`; and SMC `pip_plain`. Compare supports as sets; failed or missing benchmark rows and missing SMC records count as unrecovered. SMC selects PIP strictly greater than 0.5.', '', 'ABESS: read X and the named Y scale, center Y, calculate no-intercept least-squares RSS for the selected support, and compare it with `leaps::regsubsets` exhaustive minimum RSS at the same size, using the specified tolerance. Empty supports use sum of squares directly. The manifest supplies 100 or 600 expected cases. Missing truth, malformed fields, or unavailable size comparisons produce UNVERIFIED.', '', '## Mismatches', if(nrow(mis)) sprintf('- Cell %d: claimed %d; recomputed %d.',mis$cell_no,mis$claimed,mis$recomputed) else '- None.', '', '## Data observations', if(length(odd)) paste0('- ',odd) else '- No missing, failed, malformed, or exceptional cases observed.', '', sprintf('Verdict: %d MATCH / %d MISMATCH / %d UNVERIFIED.',sum(res$verdict=='MATCH'),sum(res$verdict=='MISMATCH'),sum(res$verdict=='UNVERIFIED')))
writeLines(lines,file.path(base,'TIEOUT_REPORT.md'),useBytes=TRUE)
