# runtime_estimate.R -- full-grid runtime estimate (136 settings x 100 reps x methods) from harness/smoke_table.tsv.
#   Rscript harness/runtime_estimate.R [--jobs 16] [--reps 100]  -> specs/RUNTIME_ESTIMATE.md
# Scaling (OURS): every setting inherits the smoke runtime of the smoke combo with the same (n, p) (S1: the 4 (n,p) pairs
# at SNR 2; S2: the 2 (n,p,s) configs at rho .35, type 1, nu .71). The smoke covers every (n, p) of the grid, so no
# extrapolation in n or p is needed; the unmeasured factors are SNR / nu / rho / beta-type (signal strength changes the
# SMC stage count and the MCMC acceptance), and run-to-run variation; the low/high band is x0.5 / x3 on each fit.
# Single-threaded fits, <= `jobs` at once on Owls (nice 19, shared host): wall = core-h / jobs (perfect packing).
BASE <- local({ f <- sub("^--file=", "", grep("^--file=", commandArgs(FALSE), value = TRUE)); normalizePath(file.path(dirname(f), "..")) })
a <- commandArgs(TRUE); opt <- list(jobs = "16", reps = "100", pending = "asi")
if (length(a)) for (i in seq(1, length(a), by = 2)) opt[[sub("^--", "", a[i])]] <- a[i + 1]
J <- as.numeric(opt$jobs); R <- as.numeric(opt$reps)
sm <- read.delim(file.path(BASE, "harness", "smoke_table.tsv"), stringsAsFactors = FALSE)
st <- read.delim(file.path(BASE, "specs", "settings.tsv"), stringsAsFactors = FALSE)
combo_np <- c(S1_03 = "S1 500x500", S1_07 = "S1 500x5000", S1_11 = "S1 1000x500", S1_15 = "S1 1000x5000",
              S2_016 = "S2 50x1000 s5", S2_076 = "S2 100x1000 s10")
key_of <- function(r) if (r$suite == 1) sprintf("S1 %dx%d", r$n, r$p) else sprintf("S2 %dx%d s%d", r$n, r$p, r$s0)
st$key <- vapply(seq_len(nrow(st)), function(i) key_of(st[i, ]), "")
cnt <- table(st$key)
sm$key <- combo_np[sm$combo]
methods <- unique(sm$method)
pending <- strsplit(opt$pending, ",")[[1]]   # methods whose smoke timing is not final (e.g. ASI moving to the Octave sampler)
lines <- c("# Runtime estimate for the full S1/S2 grid (harness/runtime_estimate.R)", "",
  sprintf("From `harness/smoke_table.tsv` (%s, 1 fit per (method, smoke combo)), %g reps per setting, at most %g single-threaded jobs on Owls.",
          format(file.info(file.path(BASE, "harness", "smoke_table.tsv"))$mtime, "%Y-%m-%d %H:%M"), R, J),
  "Scaling (OURS): each setting takes the smoke runtime of the combo with the same (n, p[, s]); the smoke covers every (n, p) in the grid.",
  "Not measured: the effect of SNR/ν/ρ/beta-type and of seed-to-seed variation. Band: ×0.5 (low) to ×3 (high) per fit.",
  "Owls was shared during the smoke (load average 50–120 on 80 cores), so the timings include contention.", "",
  "## Per fit (seconds, smoke)", "", paste("| method |", paste(combo_np, collapse = " | "), "|"),
  paste0("|---|", paste(rep("---", length(combo_np)), collapse = "|"), "|"))
for (m in methods) {
  v <- vapply(names(combo_np), function(cmb) { x <- sm$runtime_sec[sm$method == m & sm$combo == cmb]; if (length(x)) x[1] else NA }, 0)
  lines <- c(lines, paste0("| ", m, " | ", paste(ifelse(is.na(v), "–", format(round(v, 1), big.mark = ",")), collapse = " | "), " |"))
}
lines <- c(lines, "", "## Full grid", "", "| method | fits | core-h (central) | low | high | wall at 16 jobs (days, central) |", "|---|---|---|---|---|---|")
tot <- 0
for (m in methods) {
  if (m %in% pending) { lines <- c(lines, sprintf("| %s | %s | pending | pending | pending | pending |", m, format(R * nrow(st), big.mark = ","))); next }
  sec <- sum(vapply(names(cnt), function(k) { x <- sm$runtime_sec[sm$method == m & sm$key == k]; if (length(x)) x[1] * cnt[[k]] else NA }, 0)) * R
  ch <- sec / 3600; tot <- tot + ch
  lines <- c(lines, sprintf("| %s | %s | %s | %s | %s | %.2f |", m, format(R * nrow(st), big.mark = ","), format(round(ch, 1), big.mark = ","),
                            format(round(0.5 * ch, 1), big.mark = ","), format(round(3 * ch, 1), big.mark = ","), ch / J / 24))
}
lines <- c(lines, sprintf("| **all (excl. %s)** | %s | **%s** | %s | %s | **%.1f** |", paste(pending, collapse = ","), format(R * nrow(st) * length(setdiff(methods, pending)), big.mark = ","),
                          format(round(tot, 1), big.mark = ","), format(round(0.5 * tot, 1), big.mark = ","), format(round(3 * tot, 1), big.mark = ","), tot / J / 24))
lines <- c(lines, "", sprintf("## By (n, p) class, all methods except %s (core-h, central)", paste(pending, collapse = ",")), "", "| class | settings | core-h |", "|---|---|---|")
for (k in names(cnt)) {
  x <- sum(sm$runtime_sec[sm$key == k & !(sm$method %in% pending)], na.rm = TRUE) * cnt[[k]] * R / 3600
  lines <- c(lines, sprintf("| %s | %d | %s |", k, cnt[[k]], format(round(x, 1), big.mark = ",")))
}
writeLines(lines, file.path(BASE, "specs", "RUNTIME_ESTIMATE.md"))
cat(sprintf("total %.1f core-h; %.1f days at %g jobs\n", tot, tot / J / 24, J))
