# prep_data.R -- exports the raw design matrices of the R-sourced data sets to data/<name>.rds (list: X, y, prov).
# Data come only through load()/lazyLoad of data files (no code from downloaded folders is run).
L44 <- "C:/Users/felip/AppData/Local/R/win-library/4.4"
ver <- function(pkg) as.character(read.dcf(file.path(L44, pkg, "DESCRIPTION"), "Version"))
md5f <- function(f) unname(tools::md5sum(f))
getd <- function(name, pkg) { e <- new.env(); data(list = name, package = pkg, lib.loc = L44, envir = e); e }
save1 <- function(nm, X, y, prov) { saveRDS(list(X = X, y = y, prov = prov), file.path("data", paste0(nm, ".rds"))); cat(nm, ": X", dim(X), "\n") }

# 1 riboflavin (hdi 0.1-10, CRAN Archive)
e <- new.env(); load("downloads/hdi/hdi/data/riboflavin.RData", e); r <- e$riboflavin
save1("riboflavin", unclass(r$x), r$y, sprintf("hdi 0.1-10 (https://cran.r-project.org/src/contrib/Archive/hdi/hdi_0.1-10.tar.gz, tarball md5 %s), data/riboflavin.RData (md5 %s); X=riboflavin$x, y=riboflavin$y",
  "e7cf1f703e575b5ac3acfdef79b2aa84", md5f("downloads/hdi/hdi/data/riboflavin.RData")))

# 2 tecator / Fat spectrum (fds 1.8): Fatspectrum$y is 100 wavelengths x 215 samples -> X = t(y)
e <- getd("Fatspectrum", "fds"); X <- t(e$Fatspectrum$y)
save1("tecator", X, NULL, sprintf("fds %s (R 4.4 library, data/Rdata.rdb md5 %s): Fatspectrum$y transposed (n=215 samples x p=100 wavelengths 850-1050nm)", ver("fds"), md5f(file.path(L44, "fds/data/Rdata.rdb"))))

# 3 iclaims (bsts 0.9.10): predictors = the 10 Google-Trends columns (all but iclaimsNSA); y = iclaimsNSA (not used for the design)
e <- getd("iclaims", "bsts"); ic <- e$initial.claims
cn <- colnames(ic); M <- matrix(as.numeric(unclass(ic)), nrow(ic), ncol(ic), dimnames = list(NULL, cn))
X <- M[, -1, drop = FALSE]; print(colnames(X))
save1("iclaims", X, M[, 1], sprintf("bsts %s (R 4.4 library, data/iclaims.RData md5 %s): initial.claims[,-1] (10 Google-Trends columns), weekly %s..%s, predictor columns only", ver("bsts"), md5f(file.path(L44, "bsts/data/iclaims.RData")), format(attr(ic, "index")[1]), format(tail(attr(ic, "index"), 1))))

# 4 FRED-QD / FRED-MD (BVAR 1.0.5): drop columns with NA in the raw data, apply the BVAR transformation code (fred_trans.csv),
# re-implemented here because the BVAR namespace cannot be loaded under R 4.6 (semantics copied from BVAR:::get_transformation, lag=1, scale=100)
tr <- read.csv(file.path(L44, "BVAR/fred_trans.csv"), stringsAsFactors = FALSE)
tf <- function(x, code, scale = 100) switch(code,
  "none" = x, "1st-diff" = c(NA, diff(x)), "log" = log(x), "log-diff" = c(NA, diff(log(x))) * scale,
  "log-2nd-diff" = c(NA, NA, diff(log(x), differences = 2)) * scale,
  "pct-ch-diff" = c(NA, NA, diff(x[-1] / head(x, -1) - 1)) * scale, stop("code ", code))
do_fred <- function(dsname, col) {
  e <- getd(dsname, "BVAR"); x <- e[[dsname]]
  nacols <- colnames(x)[colSums(is.na(x)) > 0]; xx <- x[, colSums(is.na(x)) == 0, drop = FALSE]
  codes <- tr[[col]][match(colnames(xx), tr$variable)]
  stopifnot(!anyNA(codes))
  Y <- sapply(seq_len(ncol(xx)), function(j) tf(xx[, j], codes[j])); colnames(Y) <- colnames(xx)
  bad <- colSums(!is.finite(Y[-(1:2), , drop = FALSE])) > 0       # e.g. log of a non-positive value
  Y <- Y[, !bad, drop = FALSE]; Y <- Y[-(1:2), , drop = FALSE]    # drop the first two rows lost to differencing for every column
  stopifnot(all(is.finite(Y)))
  cat(dsname, ": raw", dim(x), "; NA columns dropped:", length(nacols), "; non-finite after transform:", sum(bad), "; rows", rownames(x)[3], "..", tail(rownames(x), 1), "\n")
  print(table(codes))
  save1(dsname, Y, NULL, sprintf("BVAR %s (R 4.4 library; data/Rdata.rdb md5 %s; fred_trans.csv md5 %s): %s, %d NA-columns dropped of %d, %d columns non-finite after transform dropped; transformed by BVAR code table (%s) re-implemented; rows %s..%s",
    ver("BVAR"), md5f(file.path(L44, "BVAR/data/Rdata.rdb")), md5f(file.path(L44, "BVAR/fred_trans.csv")), dsname, length(nacols), ncol(x), sum(bad), col, rownames(x)[3], tail(rownames(x), 1)))
}
do_fred("fred_qd", "fred_qd")
do_fred("fred_md", "fred_md")

# 6 spam (kernlab 0.9-33): 57 predictors, raw
e <- new.env(); load(file.path(L44, "kernlab/data/spam.rda"), e); sp <- e$spam
save1("spam", as.matrix(sp[, 1:57]), as.numeric(sp$type == "spam"), sprintf("kernlab %s (R 4.4 library, data/spam.rda md5 %s): spam[,1:57] raw (no transformation); y = type=='spam' (not used)", ver("kernlab"), md5f(file.path(L44, "kernlab/data/spam.rda"))))
