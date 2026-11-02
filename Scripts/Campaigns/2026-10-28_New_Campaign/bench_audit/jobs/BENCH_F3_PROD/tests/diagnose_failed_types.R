args <- commandArgs(trailingOnly=TRUE)
x <- readRDS(paste0(args[1],".rds"))
rows <- read.csv(paste0(args[1],".csv"),stringsAsFactors=FALSE,
  colClasses=c(support="character",support_audit="character",diag_codes="character",
               warnings="character",messages="character",error="character"))
for(nm in c("support","k","index","lambda")) {
  a <- x$coefficients[[1]][[nm]]; b <- rows[[nm]][1]
  cat(nm,"co_type",typeof(a),"csv_type",typeof(b),"all.equal",
      paste(all.equal(a,b,tolerance=1e-12,check.attributes=FALSE),collapse="|"),"\n")
}
