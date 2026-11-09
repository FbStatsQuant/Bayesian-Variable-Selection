# diag_fred_qd.R -- run: Rscript diag_fred_qd.R > out_fred_qd.txt 2>&1   (from data_diag/)
source("diag_lib.R")
d <- readRDS("data/fred_qd.rds"); X <- d$X; prov <- d$prov; y <- NULL
run_design("fred_qd", X, y = y, source_note = prov)
