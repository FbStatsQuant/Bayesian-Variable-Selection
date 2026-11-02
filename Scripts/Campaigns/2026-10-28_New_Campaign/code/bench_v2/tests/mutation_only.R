# Execute the revised implementation-mutation controls and their fixture setup.
root <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2"
src <- readLines(file.path(root,"tests","run_all_tests.R"),warn=FALSE)
end <- which(grepl('^sys.source\\(file.path\\(root, "F3_AdaptiveLasso", "methods/glmnet_helpers.R"\\), e\\)',src))
stopifnot(length(end)==1L, end > 200L)
con <- textConnection(src[seq_len(end-1L)])
source(con,local=globalenv())
close(con)
report <- do.call(rbind,results)
controls <- report[grepl("^implementation mutation:",report$name),,drop=FALSE]
print(controls,row.names=FALSE)
cat("implementation mutations",nrow(controls),"pass",sum(controls$outcome=="PASS"),"fail",sum(controls$outcome=="FAIL"),"\n")
if (nrow(controls)!=5L || any(controls$outcome!="PASS")) quit(save="no",status=1L)
