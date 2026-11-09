# diag_tecator.R -- run: Rscript diag_tecator.R > out_tecator.txt 2>&1   (from data_diag/)
source("diag_lib.R")
d <- readRDS("data/tecator.rds"); X <- d$X; prov <- d$prov; y <- NULL
run_design("tecator", X, y = y, source_note = prov)
