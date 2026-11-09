# diag_fred_md.R -- run: Rscript diag_fred_md.R > out_fred_md.txt 2>&1   (from data_diag/)
source("diag_lib.R")
d <- readRDS("data/fred_md.rds"); X <- d$X; prov <- d$prov; y <- NULL
run_design("fred_md", X, y = y, source_note = prov)
