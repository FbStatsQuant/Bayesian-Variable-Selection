# make_real_lambda.R -- W2-SIM family X, question 4 (real-data-like covariances).
# Reads the design matrices exported by W2-APP (Theory_work/Wave2/W2-APP/data_diag/data/<name>.rds, list(X, y, prov)),
# computes the sample correlation R (columns centred, unit sample variance) and the SHRUNK correlation
#   Sigma_delta = (1 - delta) R + delta I   (delta = 0.1; regularisation needed: riboflavin R has rank 70 < p)
# and writes an exact factor representation Sigma_delta = L L' + delta I with L = V sqrt((1 - delta) lambda_+)
# (V, lambda_+ = eigenvectors / positive eigenvalues of R; k = rank R factors; psi_j = delta for every j since R_jj = 1).
# Output: X/data/<name>_L.csv (p x k, no header) and X/data/<name>_L_meta.txt (dims, delta, eigen summary, md5 of input).
args <- commandArgs(trailingOnly = TRUE)
src <- args[1]; outdir <- args[2]; delta <- if (length(args) > 2) as.numeric(args[3]) else 0.1
for (nm in c("riboflavin", "fred_md", "fred_qd")) {
  f <- file.path(src, paste0(nm, ".rds"))
  d <- readRDS(f); X <- as.matrix(d$X)
  X <- scale(X, center = TRUE, scale = TRUE)
  n <- nrow(X); p <- ncol(X)
  sv <- svd(X / sqrt(n - 1))
  lam <- sv$d^2
  keep <- lam > 1e-10 * max(lam)
  V <- sv$v[, keep, drop = FALSE]; lam <- lam[keep]
  L <- V %*% diag(sqrt((1 - delta) * lam), length(lam))
  rs <- rowSums(L^2)
  stopifnot(max(abs(rs - (1 - delta))) < 1e-8)
  write.table(format(L, digits = 17), file.path(outdir, paste0(nm, "_L.csv")), sep = ",", row.names = FALSE,
              col.names = FALSE, quote = FALSE)
  meta <- c(sprintf("name=%s n_data=%d p=%d k=%d delta=%g", nm, n, p, length(lam), delta),
            sprintf("input_md5=%s", unname(tools::md5sum(f))),
            sprintf("max|rowSums(L^2) - (1-delta)| = %.3g", max(abs(rs - (1 - delta)))),
            sprintf("top eigenvalues of R: %s", paste(signif(head(lam, 10), 5), collapse = " ")),
            sprintf("lambda1/p = %.4f ; trace share top1/5 = %.4f / %.4f", lam[1] / p, lam[1] / sum(lam), sum(head(lam, 5)) / sum(lam)),
            sprintf("prov: %s", d$prov))
  writeLines(meta, file.path(outdir, paste0(nm, "_L_meta.txt")))
  cat(meta, sep = "\n"); cat("\n")
}
