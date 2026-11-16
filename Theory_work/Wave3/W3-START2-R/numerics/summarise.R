# summarise.R -- tables for RESULTS.md from out/raw_runs*.csv (OBSERVATIONS ONLY). Writes summary.csv (small).
here <- dirname(normalizePath(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)[1])))
fs <- list.files(file.path(here, "out"), "^raw_runs(12|34)\\.csv$", full.names = TRUE)
d <- do.call(rbind, lapply(fs, function(f) { x <- read.csv(f, stringsAsFactors = FALSE); x }))
cols <- Reduce(union, lapply(fs, function(f) names(read.csv(f, nrows = 1)))); 
d <- do.call(rbind, lapply(fs, function(f) { x <- read.csv(f, stringsAsFactors = FALSE); for (k in setdiff(cols, names(x))) x[[k]] <- NA; x[cols] }))
cat("rows", nrow(d), " non-ok", sum(d$status != "ok"), "\n"); print(table(d$exp, d$status))
d <- d[d$status == "ok", ]
q <- function(x) { v <- quantile(x, c(.25, .5, .75), na.rm = TRUE); c(q25 = v[[1]], med = v[[2]], q75 = v[[3]]) }
d$o0s <- d$o0 * sqrt(d$n / log(d$n)); d$o0T1 <- d$o0 / d$T1
rows <- list()
add <- function(exp, key, grp) {
  for (v in c("pi0", "o0", "o0T1", "o0s")) { qq <- q(grp[[v]]); rows[[length(rows) + 1]] <<- data.frame(exp = exp, n = grp$n[1], p_med = median(grp$p), key = key, stat = v, k = nrow(grp), t(qq)) }
}
for (e in c("vcp", "F2", "g1", "lg0a", "lg0b")) { x <- d[d$exp == e, ]; if (!nrow(x)) next
  if (e == "vcp") for (n in sort(unique(x$n))) for (pe in sort(unique(x$pe))) for (cc in sort(unique(x$par))) { g <- x[x$n == n & x$pe == pe & x$par == cc, ]; if (nrow(g)) add(e, sprintf("A=%.1f c=%.1f", pe, cc), g) }
  else for (n in sort(unique(x$n))) add(e, "", x[x$n == n, ]) }
s <- do.call(rbind, rows); s[, 7:ncol(s)] <- lapply(s[, 7:ncol(s)], function(z) signif(z, 4))
write.csv(s, file.path(here, "summary.csv"), row.names = FALSE)
options(width = 200); print(s[s$stat %in% c("pi0", "o0T1", "o0s") & s$exp %in% c("vcp", "F2", "g1", "lg0a", "lg0b"), ], row.names = FALSE)
