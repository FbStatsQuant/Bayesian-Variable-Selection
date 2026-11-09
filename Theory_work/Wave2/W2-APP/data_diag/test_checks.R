# test_checks.R -- unit checks of the sparse-eigenvalue machinery (run: Rscript test_checks.R > out_test_checks.txt)
source("diag_lib.R")
d <- readRDS("data/fred_qd.rds"); cd <- clean_design(d$X); R <- cd$R; p <- ncol(R)
a <- triple_scan(R, 1e-6); b <- triple_pruned(R, 1 - (5.257e-5 + 1e-6), 3e9)
cat(sprintf("fred_qd p=%d: full triple scan best=%.6e ; Gershgorin-pruned best=%.6e (visited %.3g of %.3g triples)\n", p, a$best, b$best, b$visited, choose(p, 3)))
# secular solver vs eigen
set.seed(1); S <- sample(p, 6); nl <- new_lmin_all(R, S, 60)
j <- which.min(nl$val); ref <- sapply(setdiff(seq_len(p), S), function(j) lam_min(R, c(S, j)))
cat(sprintf("secular argmin value %.6e vs brute-force min %.6e (argmin match: %s)\n", nl$val[j], min(ref), identical(j, setdiff(seq_len(p), S)[which.min(ref)])))
# closed form 3x3 vs eigen on random triples
tr <- replicate(2000, sample(p, 3)); err <- max(apply(tr, 2, function(s) abs(lam_min(R, s) - triple_scan(R[s, s], 1e9)$best)))
cat(sprintf("closed-form 3x3 vs eigen: max abs error over 2000 random triples (via scan of 3x3 matrix) = %.2e\n", err))
