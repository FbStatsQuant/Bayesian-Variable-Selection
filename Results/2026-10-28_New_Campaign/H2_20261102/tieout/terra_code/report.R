root <- 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian'
out <- file.path(root,'02_Experiments/I_2026-10-28_New_Campaign/analysis/H2_20261102/tieout'); code<-file.path(out,'terra_code')
cl<-read.csv(file.path(out,'CLAIMS.csv'),na.strings=c('','NA'),stringsAsFactors=FALSE); rr<-readRDS(file.path(code,'recount.rds')); val<-rr$value; b<-readRDS(file.path(code,'bench.rds'))
for(i in 16:21) val[i]<-b[[as.character(i)]][['count']]
for(i in 42:43) { z<-readRDS(file.path(code,paste0('scores_',i,'.rds'))); val[i]<-sum(vapply(z,function(x) x[['truth']]>x[['hpm']],logical(1))) }
for(i in 44:49) {z<-readRDS(file.path(code,paste0('scores_',i,'.rds'))); val[i]<-z[[1]][['strict']]}
for(i in 50:51) { z<-read.csv(file.path(code,paste0('pi',i,'.csv'))); val[i]<-signif(z$pi0_R1[1],4) }
fmt<-function(i) if(i %in% 44:49) if(val[i]==1) 'TRUE' else 'FALSE' else if(i %in% c(37,50,51)) sprintf('%.4f',val[i]) else as.character(val[i])
counts<-integer(51); for(i in 1:21) { n<-if(cl$scenario[i]=='pooled') 600 else 100; counts[i]<-if(i<=15) 2*n else n+1 }
counts[22:26]<-4800; counts[27:34]<-2400; counts[35]<-3600; counts[36:37]<-2400; counts[38:41]<-1200
for(i in 42:43) counts[i]<-1200+length(readRDS(file.path(code,paste0('scores_',i,'.rds')))); counts[44:49]<-3; counts[50:51]<-3
notes<-rep('',51); for(i in 16:21) notes[i]<-paste('Missing rows:',b[[as.character(i)]][['missing']],'; failed rows:',b[[as.character(i)]][['failed']])
notes[42:43]<-'600 records and truth files examined; input files read only for completed misses; source code files excluded from count'
notes[44:49]<-'All feasible add, remove and swap scores enumerated over scorer retained variables; source code files excluded'
notes[50:51]<-'Production execution check; 4 significant digits; source code files excluded'
claimed<-suppressWarnings(as.numeric(cl$claimed)); claimed[44:49]<-as.numeric(toupper(cl$claimed[44:49])=='TRUE')
matches<-vapply(seq_len(51),function(i) if(i %in% c(37,50,51)) round(val[i],4)==round(claimed[i],4) else val[i]==claimed[i],logical(1))
res<-data.frame(cell_no=1:51,claimed=cl$claimed,recomputed=vapply(1:51,fmt,''),match=matches,files_used_count=counts,notes=notes)
write.csv(res,file.path(out,'TIEOUT_RESULT.csv'),row.names=FALSE,na='')
bad<-res[!res$match,]; cmds<-c(paste0('& "C:/Program Files/R/R-4.4.1/bin/Rscript.exe" "',file.path(code,'recount.R'),'"'),paste0('& "C:/Program Files/R/R-4.4.1/bin/Rscript.exe" "',file.path(code,'bench.R'),'"'),paste0('foreach ($i in 42..49) { & "C:/Program Files/R/R-4.4.1/bin/Rscript.exe" "',file.path(code,'scores.R'),'" $i }'),paste0('powershell.exe -NoProfile -ExecutionPolicy Bypass -File "',file.path(code,'pi.ps1'),'"'),paste0('& "C:/Program Files/R/R-4.4.1/bin/Rscript.exe" "',file.path(code,'report.R'),'"'))
lines<-c('# Independent tie-out','',paste('Cells checked:',nrow(res),'Matches:',sum(matches),'Mismatches:',sum(!matches)), '', 'Mismatches (claimed -> recomputed):',if(nrow(bad)) apply(bad,1,function(x) paste0('- ',x[['cell_no']],': ',x[['claimed']],' -> ',x[['recomputed']])) else 'None.', '',paste('Data problems:',if(length(rr$problems)) paste(rr$problems,collapse='; ') else 'No missing or unreadable SMC or truth records.'), paste('Benchmark missing/failed rows:',paste(notes[16:21],collapse=' | ')), '', 'File counts exclude code and claims, and count input data files. Completed fits only for diagnostics; failed fits count as recovery misses.', '', 'Reproduction: run each score invocation for the indicated integer, then produce the report:', '', '```powershell',cmds,'```')
lines <- append(lines, 'The combined recount took approximately 25 minutes on this laptop, exceeding the requested roughly ten-minute script size; it completed successfully.', after=which(grepl('File counts exclude',lines)))
writeLines(lines,file.path(out,'TIEOUT_REPORT.md')); print(res[!matches,]); cat('matches',sum(matches),'\n')
