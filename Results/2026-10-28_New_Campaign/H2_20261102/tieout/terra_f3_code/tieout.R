root <- 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian'
h2 <- file.path(root, '02_Experiments/I_2026-10-28_New_Campaign/analysis/H2_20261102/tieout')
fits <- 'C:/Users/felip/OneDrive - Rice University/NOTS Data/New_Campaign/results/20261102T1252Z_bench_f3v2_prod'
truthdir <- file.path(root, '02_Experiments/F_2026-10-19_benchmark_study_n200/Benchmark_Study_20261019/verify/recount/c050/inputs/truth_scoring')
claims <- read.csv(file.path(h2, 'F3_CLAIMS.csv'), stringsAsFactors=FALSE)
rules <- unique(claims$rule)
records <- list(); problems <- character(); k <- 0L
problem <- function(s) { problems <<- c(problems, s) }
for (p in c(500L,1000L)) for (scale in c('c100','c050')) for (s in 1:6) for (r in 1:100) {
  pid <- sprintf('p%04d',p); id <- sprintf('%s_S%d_r%03d',pid,s,r)
  case <- paste(id,scale,sep='_'); dir <- file.path(fits,pid,case)
  tr <- tryCatch(readRDS(file.path(truthdir,pid,paste0(id,'.rds')))$active, error=function(e) NULL)
  if (is.null(tr) || length(unique(tr)) != 14L || anyNA(tr)) { problem(paste(case,'invalid or missing truth')); tr <- NULL }
  done <- file.exists(file.path(dir,'F3.done'))
  if (!done) problem(paste(case,'missing F3.done'))
  fit <- tryCatch(readRDS(file.path(dir,'F3.rds'))$rows, error=function(e) NULL)
  if (is.null(fit) || !is.data.frame(fit) || !all(c('rule_id','status','support','diag_codes') %in% names(fit))) { problem(paste(case,'missing or malformed F3.rds')); fit <- NULL }
  for (rule in rules) {
    row <- if (!is.null(fit)) fit[!is.na(fit$rule_id) & fit$rule_id == rule,,drop=FALSE] else NULL
    if (is.null(row) || nrow(row) != 1L) { problem(paste(case,rule,'missing or duplicate rule row')); row <- NULL }
    exact <- FALSE; last <- FALSE; unknown <- is.null(tr)
    if (!is.null(row)) {
      if (!is.na(row$diag_codes)) last <- 'lambda_last' %in% trimws(strsplit(as.character(row$diag_codes), '[^A-Za-z0-9_]+')[[1]])
      if (done && !is.na(row$status) && row$status == 'ok') {
        supp <- as.character(row$support)
        if (is.na(supp)) { problem(paste(case,rule,'NA support on ok row')); unknown <- TRUE }
        else {
          parts <- if (trimws(supp) == '') character() else trimws(strsplit(supp,';',fixed=TRUE)[[1]])
          if (any(!grepl('^[0-9]+$',parts))) { problem(paste(case,rule,'invalid support')); unknown <- TRUE }
          else if (!is.null(tr)) exact <- setequal(as.integer(parts),as.integer(tr))
        }
      }
    }
    k <- k+1L; records[[k]] <- data.frame(p=p,scale=scale,scenario=s,rep=r,rule=rule,exact=exact,last=last,unknown=unknown)
  }
}
d <- do.call(rbind,records)
out <- data.frame(cell_no=claims$cell_no,claimed=claims$claimed,recomputed=NA_integer_,match=NA,notes='')
for (i in seq_len(nrow(claims))) {
  x <- claims[i,]; z <- d[d$p==x$p & d$scale==x$scale & d$rule==x$rule,,drop=FALSE]
  if (x$scenario != 'pooled') z <- z[z$scenario==as.integer(x$scenario),,drop=FALSE]
  if (grepl('lambda_last',x$quantity,fixed=TRUE)) out$recomputed[i] <- sum(z$last)
  else if (any(z$unknown)) out$notes[i] <- paste(sum(z$unknown),'cases have unscorable truth/support')
  else out$recomputed[i] <- sum(z$exact)
  out$match[i] <- if (is.na(out$recomputed[i])) NA else out$recomputed[i]==x$claimed
}
write.csv(out,file.path(h2,'F3_TIEOUT_RESULT.csv'),row.names=FALSE,na='')
bad <- out[!is.na(out$match) & !out$match,,drop=FALSE]
lines <- c('# F3 independent tie-out', '', paste('Cells checked:',nrow(out)), paste('Matches:',sum(out$match,na.rm=TRUE)), paste('Mismatches:',nrow(bad)), paste('Unscorable:',sum(is.na(out$match))), '', '## Mismatches (claimed -> recomputed)', if(nrow(bad)) sprintf('- Cell %s: %s -> %s',bad$cell_no,bad$claimed,bad$recomputed) else '- None', '', '## Data problems', if(length(problems)) paste0('- ',unique(problems)) else '- None detected.', '', 'Missing completion markers and non-ok rows count as misses. Diagnostic tokens are counted from cv_min rows regardless of status or completion marker.', '', '## Reproduce', '', '```powershell', paste0('& "C:/Program Files/R/R-4.4.1/bin/Rscript.exe" "',file.path(h2,'terra_f3_code/tieout.R'),'"'), '```')
writeLines(lines,file.path(h2,'F3_TIEOUT_REPORT.md'))
cat(paste(lines,collapse='\n'), '\n')
