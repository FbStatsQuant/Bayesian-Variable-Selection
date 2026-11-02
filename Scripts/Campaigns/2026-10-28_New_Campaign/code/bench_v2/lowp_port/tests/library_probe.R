.libPaths(c('C:/Users/felip/AppData/Local/Temp/lowp_Rlib',.libPaths()))
print(.libPaths()); print(installed.packages()[,c('Package','Version')])
for (p in c('glmnet','abess','ncvreg','SSLASSO','susieR','bayesreg','digest')) { cat('package',p,'\n'); tryCatch(loadNamespace(p),error=function(e) cat('LOAD ERROR',conditionMessage(e),'\n')) }
