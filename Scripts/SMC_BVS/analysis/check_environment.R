cat(R.version.string,"\n")
print(Sys.info())
print(.libPaths())
print(sapply(c("digest","jsonlite"),function(x) as.character(packageVersion(x))))
print(gc())
a <- commandArgs(TRUE)
for(i in seq_len(5)) {saveRDS(list(x=seq_len(1000)),file.path(a[1],paste0("xz_probe_",i,".rds")),compress="xz"); cat("xz probe",i,"OK\n"); gc()}
