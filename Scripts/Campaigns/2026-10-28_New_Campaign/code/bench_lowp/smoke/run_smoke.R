# Entry point for the current sealed-study smoke suite.
self <- sub('^--file=','',grep('^--file=',commandArgs(FALSE),value=TRUE)[1])
source(file.path(dirname(normalizePath(self,winslash='/')),'smoke3.R'))
