# diag_riboflavin.R -- run: Rscript diag_riboflavin.R > out_riboflavin.txt 2>&1   (from data_diag/)
source("diag_lib.R")
d <- readRDS("data/riboflavin.rds"); X <- d$X; prov <- d$prov; y <- d$y
run_design("riboflavin", X, y = y, source_note = prov, restarts = 60, tlimit_total = 360, swap_tlimit = 15, maxvisit = 2e8)
