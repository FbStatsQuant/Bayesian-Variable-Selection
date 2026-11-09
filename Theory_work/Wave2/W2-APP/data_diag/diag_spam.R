# diag_spam.R -- run: Rscript diag_spam.R > out_spam.txt 2>&1   (from data_diag/)
source("diag_lib.R")
d <- readRDS("data/spam.rds"); X <- d$X; prov <- d$prov; y <- NULL
run_design("spam", X, y = y, source_note = prov)
