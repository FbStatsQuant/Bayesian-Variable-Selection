camp <- 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign'
root <- file.path(camp,'code/bench_v2/lowp_port'); target <- file.path(camp,'code/scoring/tests/test_scoring.R'); work <- file.path(root,'scoring_work')
Sys.setenv(SCORING_BENCH_DIR=file.path(camp,'code/bench_lowp'))
commandArgs <- function(trailingOnly=FALSE) if(trailingOnly) work else c('Rscript',paste0('--file=',target),'--args',work)
system2 <- function(command,args=character(),...) {
  if(grepl('Rscript',command,ignore.case=TRUE)) {
    query <- "@(Get-CimInstance Win32_Process -Filter \"Name = 'Rscript.exe'\" | Where-Object { $_.CommandLine -match 'bench_v2|bench_lowp|scoring' }).Count"
    repeat { n <- suppressWarnings(as.integer(base::system2('powershell.exe',c('-NoProfile','-Command',shQuote(query)),stdout=TRUE,stderr=FALSE))); if(length(n)!=1L || is.na(n)) stop('could not inspect process cap'); if(n<=10L) break; Sys.sleep(10) }
  }
  base::system2(command,args,...)
}
src <- readLines(target,warn=FALSE)
needle <- 'writeLines(L, file.path(here, "TEST_REPORT.md"), useBytes = TRUE)'
stopifnot(sum(src==needle)==1L)
src[src==needle] <- sprintf('writeLines(L, %s, useBytes = TRUE)',encodeString(file.path(root,'SCORING_TEST_REPORT.md'),quote='"'))
eval(parse(text=src),envir=globalenv())
