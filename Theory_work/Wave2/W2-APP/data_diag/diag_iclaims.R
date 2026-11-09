# diag_iclaims.R -- run: Rscript diag_iclaims.R > out_iclaims.txt 2>&1   (from data_diag/)
source("diag_lib.R")
d <- readRDS("data/iclaims.rds"); X <- d$X; prov <- d$prov; y <- NULL
run_design("iclaims", X, y = y, source_note = prov)
