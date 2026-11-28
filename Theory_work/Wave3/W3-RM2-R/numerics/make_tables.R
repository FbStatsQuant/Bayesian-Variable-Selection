# make_tables.R -- markdown tables of RESULTS.md from summary.csv (so that no number is transcribed by hand). Usage: Rscript make_tables.R
d <- read.csv("summary.csv", stringsAsFactors = FALSE)
f <- function(x) ifelse(is.na(x), "–", format(x, trim = TRUE))
tab <- function(x, P) {
  cols <- if (P) c("κ", "λ_n/log n", "vis (U*)", "vis (block min)", "start size", "S0⊆S̃0", "S̃0⊆Q", "F(S0)−best truth-removal nbr > 0 (at T=S0)", "visited T⊇S0: runs with TL>0 of runs with such a T; min margin", "NA at lattice centres (visited / ok)", "LS0 ends at S0 (cert.)", "mode margin ≥3: >0 / median / min")
          else c("κ", "λ_n/log n", "vis wk (U*)", "vis wk (block min: median [min])", "start size", "S0⊆S̃0 (truth 2 in start)", "S̃0⊆Q", "F(S0)−best truth-removal nbr > 0 (at T=S0)", "visited T⊇S0: runs with TL>0 of runs with such a T; min margin", "NA at lattice centres (visited / ok)", "LS0 ends at S0 (cert.)", "non-deletion moves")
  r <- data.frame(x$kappa, f(x$lam_over_logn), f(x$vis_start_wk_med),
    if (P) f(x$vis_blk_wk_min) else sprintf("%s [%s]", f(x$vis_blk_wk_med), f(x$vis_blk_wk_min)),
    f(x$start_size_med), x$truth_incl, x$sandwich_inQ, x$tl_S0_pos,
    ifelse(x$tl_defined == paste0("0/", x$runs), "no visited T⊇S0", sprintf("%s of %s defined; min %s", sub("/.*", "", x$tl_ok), sub("/.*", "", x$tl_defined), f(x$tl_min_min))),
    sprintf("%s / %s", x$path_lat_visited, x$path_NA_ok), x$end_S0_cert,
    if (P) ifelse(is.na(x$mm_le3_pos), "–", sprintf("%s / %s / %s", x$mm_le3_pos, f(x$mm_le3_med), f(x$mm_le3_min))) else x$n_other_moves)
  names(r) <- cols
  cat("| ", paste(cols, collapse = " | "), " |\n|", paste(rep("---", length(cols)), collapse = "|"), "|\n", sep = "")
  for (i in seq_len(nrow(r))) cat("| ", paste(r[i, ], collapse = " | "), " |\n", sep = "")
}
r <- read.csv("arrays/results_raw.csv")
# S0 ⊆ S̃0 and S̃0 ⊆ Q separately
agg <- aggregate(cbind(start_in_Q) ~ design + n + b + kappa, data = r, FUN = function(v) sprintf("%d/%d", sum(v), length(v)))
names(agg)[5] <- "sandwich_inQ"
d <- merge(d, agg, by = c("design", "n", "b", "kappa"))
d <- d[order(d$design, d$n, d$b, d$kappa), ]
for (nn in c(400, 1600)) for (bb in c(0.3, 0.45)) { cat(sprintf("\n**Design P, n = %d, b = %s (p = %d, q = %d, r² = log n/n = %.4f)**\n\n", nn, bb, floor(nn/3), d$q[d$design=="P" & d$n==nn & d$b==bb][1], log(nn)/nn)); tab(d[d$design == "P" & d$n == nn & d$b == bb, ], TRUE) }
for (nn in c(400, 1600)) { cat(sprintf("\n**Design G, n = %d, b = 0.375 (p = %d, |Q| = %d)**\n\n", nn, 2*nn, d$q[d$design=="G" & d$n==nn][1])); tab(d[d$design == "G" & d$n == nn, ], FALSE) }
