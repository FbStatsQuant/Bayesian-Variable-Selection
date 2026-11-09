# loc_prod_extract.R -- read one production RDS written by loc_prod_fit.R and write a compact JSON with the start mode,
# the LS0 centre, the full LS0 path (centre prepended: the core's ls0$path lists the models AFTER each move), the move
# types, the returned model and HPM (1-based original indices), so that LS0 is compared move by move with the port.
# Usage: Rscript --vanilla loc_prod_extract.R RDS OUT_JSON
a <- commandArgs(trailingOnly = TRUE)
suppressMessages(library(jsonlite))
k <- readRDS(a[1]); l <- k$ls0
mod <- function(x) if (is.list(x)) x$model else x
full <- c(list(as.integer(l$centre)), lapply(l$path, as.integer))
types <- if (length(full) >= 2) vapply(2:length(full), function(i) {
  A <- full[[i - 1]]; B <- full[[i]]; ins <- length(setdiff(B, A)); outs <- length(setdiff(A, B))
  if (ins == 1 && outs == 1) "swap" else if (ins == 1 && outs == 0) "add" else if (outs == 1 && ins == 0) "del" else "other" }, "") else character(0)
rec <- list(tag = k$rec$tag, status = k$status, start_mode = sort(as.integer(mod(k$start_mode))), ls0_centre = sort(as.integer(l$centre)),
  ls0_moves = l$moves, ls0_cap = l$move_cap, ls0_termination = l$termination, ls0_local_limit = l$local_limit,
  ls0_types = types, n_del = sum(types == "del"), n_swap = sum(types == "swap"), n_add = sum(types == "add"),
  ls0_returned = sort(as.integer(l$returned)), hpm = sort(as.integer(k$hpm)), hpm_before_ls0 = sort(as.integer(mod(k$hpm_before_ls0))),
  path = lapply(full, sort))
cat(toJSON(rec, auto_unbox = TRUE, null = "null", na = "null", digits = NA), "\n", file = a[2])
