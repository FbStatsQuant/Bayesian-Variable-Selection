# diag_diabetes_quad.R -- run: Rscript diag_diabetes_quad.R > out_diabetes_quad.txt 2>&1   (from data_diag/)
source("diag_lib.R")
d <- read.csv("data/diabetes_quad.csv", check.names = FALSE); y <- d$y; X <- as.matrix(d[, names(d) != "y"]); prov <- "scikit-learn 1.4.2 load_diabetes(scaled=True) (diabetes_data_raw.csv.gz md5 5a4dae33d045eae5db445e5260a3287c), quadratic model of Efron et al. 2004: 10 main effects + 45 pairwise products + 9 squares (no sex^2), built by prep_sklearn.py from unit-variance main effects"
run_design("diabetes_quad", X, y = y, source_note = prov)
