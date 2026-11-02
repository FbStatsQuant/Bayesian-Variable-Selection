# Adapt the deployed four-rule KKT fixture to six v2 rules in memory.
root <- "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2"
src <- readLines(file.path(root,"F1_Lasso","tests","test_F1_lasso.R"),warn=FALSE)
replace_once <- function(from, to) {
  i <- which(grepl(from, src, fixed=TRUE))
  stopifnot(length(i)==1L)
  src[i] <<- sub(from, to, src[i], fixed=TRUE)
}
replace_once('identical(r$status, c("failed", "failed", "ok", "ok"))',
             'identical(r$status, c("failed", "failed", "ok", "ok", "ok", "ok"))')
replace_once('identical(r$status, c("ok", "failed", "ok", "ok"))',
             'identical(r$status, c("ok", "failed", "ok", "ok", "ok", "ok"))')
replace_once('exp_fail <- c(im %in% occ, i1 %in% occ, TRUE, base$support[4] == key)',
             'exp_fail <- c(im %in% occ, i1 %in% occ, TRUE, base$support[4:6] == key)')
con <- textConnection(src)
source(con, local=globalenv(), chdir=FALSE)
close(con)
