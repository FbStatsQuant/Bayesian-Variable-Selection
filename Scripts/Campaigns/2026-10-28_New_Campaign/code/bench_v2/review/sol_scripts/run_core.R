base <- 'C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2'
cat('START', format(Sys.time(),tz='UTC'), '\n')
eval(parse(text=readLines(file.path(base,'tests/run_all_tests.R'),warn=FALSE)[1:431]), envir=globalenv())
print(do.call(rbind,results),row.names=FALSE)
stopifnot(all(vapply(results,function(z) z$outcome=='PASS',TRUE)))
cat('END', format(Sys.time(),tz='UTC'), 'PASS', length(results),'\n')
print(sessionInfo())
