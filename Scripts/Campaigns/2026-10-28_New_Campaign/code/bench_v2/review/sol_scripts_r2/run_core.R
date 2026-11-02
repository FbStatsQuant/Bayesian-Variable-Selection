C <- 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign'
cat('START',format(Sys.time(),tz='UTC'),'\n')
statements <- parse(file.path(C,'code/bench_v2/tests/run_all_tests.R'))
for(z in statements) {
  if(is.call(z) && identical(z[[1L]],as.name('check')) && identical(z[[2L]],'adapted deployed F1 common suite')) break
  eval(z,.GlobalEnv)
}
report <- do.call(rbind,results)
print(report,row.names=FALSE)
stopifnot(all(report$outcome=='PASS'))
cat('END',format(Sys.time(),tz='UTC'),'PASS',nrow(report),'\n')
print(sessionInfo())
