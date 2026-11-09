# diag_digits.R -- run: Rscript diag_digits.R > out_digits.txt 2>&1   (from data_diag/)
source("diag_lib.R")
d <- read.csv("data/digits.csv"); X <- as.matrix(d[, names(d) != "y"]); y <- NULL; prov <- "scikit-learn 1.4.2 load_digits (digits.csv.gz md5 9b335364a7bfd63947c7480a5bd51f2d): 1797 x 64 pixels, constant columns dropped by clean_design"
run_design("digits", X, y = y, source_note = prov)
